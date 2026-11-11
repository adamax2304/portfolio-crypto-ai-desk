from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import store as ls
from .bybit_client import BybitAPIError, BybitFuturesClient
from .candle_extremes import completed_post_entry_extreme
from .config import LiveCanaryConfig
from .sizing import model_f_stop, rebase_filled_plan, stop_risk_components


def submit_entry(*, client: BybitFuturesClient, plan: dict[str, Any]) -> dict[str, Any]:
    client.set_leverage(str(plan["symbol"]), int(plan["leverage"]))
    return client.create_entry(
        symbol=str(plan["symbol"]), direction=str(plan["direction"]),
        qty=float(plan["volume_contracts"]), price=float(plan["limit_price"]),
        order_link_id=str(plan["external_oid"]), position_idx=int(plan.get("position_idx", 0)),
    )


def _write_order(conn: sqlite3.Connection, *, decision_id: str, plan: dict[str, Any],
                 status: str, exchange: dict[str, Any] | None = None,
                 error: str | None = None) -> None:
    now = ls.utc_now()
    conn.execute(
        "INSERT INTO mexc_canary_orders("
        "order_row_id,decision_id,external_oid,exchange_order_id,symbol,status,submitted_at,updated_at,"
        "plan_json,exchange_json,last_error,venue) VALUES(?,?,?,?,?,?,?,?,?,?,?,?) "
        "ON CONFLICT(decision_id) DO UPDATE SET "
        "external_oid=excluded.external_oid,symbol=excluded.symbol,plan_json=excluded.plan_json,"
        "exchange_order_id=COALESCE(excluded.exchange_order_id,exchange_order_id),"
        "status=excluded.status,updated_at=excluded.updated_at,exchange_json=excluded.exchange_json,"
        "last_error=excluded.last_error,venue='bybit'",
        (str(uuid.uuid4()), decision_id, plan["external_oid"],
         str((exchange or {}).get("orderId") or "") or None, plan["symbol"], status,
         now if status in {"SUBMITTING", "SUBMITTED", "FILLED"} else None, now,
         json.dumps(plan, sort_keys=True), json.dumps(exchange or {}, sort_keys=True),
         error, "bybit"),
    )


def _position_for_plan(client: BybitFuturesClient, plan: dict[str, Any]) -> dict[str, Any] | None:
    expected_type = 1 if str(plan.get("direction")) == "long" else 2
    expected_idx = int(plan.get("position_idx", 0))
    return next(
        (row for row in client.open_positions(str(plan["symbol"]))
         if int(row.get("positionType") or 0) == expected_type
         and int(row.get("positionIdx") or 0) == expected_idx),
        None,
    )


def _upsert_position(conn: sqlite3.Connection, *, decision_id: str, plan: dict[str, Any],
                     order: dict[str, Any], position: dict[str, Any]) -> None:
    now = ls.utc_now()
    entry = float(order.get("dealAvgPrice") or position.get("openAvgPrice") or plan["limit_price"])
    rebased = rebase_filled_plan(plan, fill_price=entry)
    plan.clear()
    plan.update(rebased)
    volume = float(order.get("dealVol") or position.get("holdVol") or plan["volume_contracts"])
    risk_detail = stop_risk_components(
        entry_price=entry, stop_price=float(plan["original_stop"]),
        volume_contracts=volume, contract_size=float(plan["contract_size"]),
        taker_fee_rate=float(plan.get("taker_fee_rate") or 0),
        slippage_rate=float(plan.get("slippage_rate") or 0),
    )
    notional = volume * float(plan["contract_size"]) * entry
    liquidation = position.get("liquidatePrice")
    conn.execute(
        "INSERT INTO mexc_canary_positions("
        "position_row_id,decision_id,exchange_position_id,symbol,direction,status,entry_price,original_stop,"
        "current_stop,tp3,volume_contracts,notional_usdt,risk_usdt,leverage,liquidation_price,"
        "highest_price,favorable_price,max_favorable_r,protection_stage,opened_at,updated_at,exchange_json,venue) "
        "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
        "ON CONFLICT(decision_id) DO UPDATE SET exchange_position_id=excluded.exchange_position_id,"
        "status='OPEN',entry_price=excluded.entry_price,volume_contracts=excluded.volume_contracts,"
        "notional_usdt=excluded.notional_usdt,risk_usdt=excluded.risk_usdt,"
        "liquidation_price=excluded.liquidation_price,updated_at=excluded.updated_at,"
        "exchange_json=excluded.exchange_json,venue='bybit'",
        (str(uuid.uuid4()), decision_id, str(position.get("positionId") or ""), plan["symbol"],
         plan["direction"], "OPEN", entry, float(plan["original_stop"]),
         float(plan["original_stop"]), float(plan["tp3"]), volume, notional,
         risk_detail["net_stop_risk_usdt"], int(plan["leverage"]),
         float(liquidation) if liquidation not in (None, "") else None,
         entry, entry, 0.0, "ORIGINAL_STOP", now, now,
         json.dumps(position, sort_keys=True), "bybit"),
    )
    conn.execute(
        "UPDATE mexc_canary_risk_reservations SET status='OPEN',risk_usdt=?,"
        "notional_usdt=?,updated_at=?,venue='bybit' WHERE decision_id=? AND status='RESERVED'",
        (risk_detail["net_stop_risk_usdt"], notional, now, decision_id),
    )
    ls.event(conn, "BYBIT_FILLED_RISK_RECALCULATED", decision_id=decision_id,
             payload={"fill_price": entry, **risk_detail})


def _tp_link_id(decision_id: str, index: int) -> str:
    return f"btp{index}_" + decision_id.replace("-", "")[:27]


def _emergency_close_link_id(decision_id: str) -> str:
    return "bclose_" + decision_id.replace("-", "")[:27]


def _ensure_protection(*, path: Path, client: BybitFuturesClient,
                       local: dict[str, Any], plan: dict[str, Any],
                       wanted_stop: float, install_stop: bool) -> None:
    decision_id = str(local["decision_id"])
    position_idx = int(plan.get("position_idx", 0))
    if install_stop:
        client.set_full_stop(
            symbol=str(local["symbol"]), stop_loss=wanted_stop, position_idx=position_idx
        )
        with ls.connect(path) as conn:
            conn.execute(
                "UPDATE mexc_canary_positions SET tpsl_order_id=?,updated_at=? "
                "WHERE decision_id=? AND venue='bybit'",
                ("bybit-full-position-stop", ls.utc_now(), decision_id),
            )
            conn.commit()
    legs = list(plan.get("partial_tp_legs") or [])
    if len(legs) != 3:
        raise BybitAPIError("Bybit plan does not contain three TP legs")
    with ls.connect(path) as conn:
        existing = {
            int(row["leg_index"]): dict(row)
            for row in conn.execute(
                "SELECT * FROM mexc_canary_exit_legs WHERE decision_id=? AND venue='bybit'",
                (decision_id,),
            ).fetchall()
        }
    for leg in legs:
        index = int(leg["leg"])
        link_id = _tp_link_id(decision_id, index)
        observed: dict[str, Any] | None = None
        stored = existing.get(index)
        if stored and str(stored.get("status") or "") in {"FILLED", "TERMINAL"}:
            continue
        if stored and stored.get("external_oid"):
            link_id = str(stored["external_oid"])
        if stored and stored.get("exchange_order_id"):
            try:
                observed = client.order_by_external_id(str(local["symbol"]), link_id)
            except BybitAPIError:
                observed = None
        if observed is None:
            # Resolve a prior unknown POST before creating anything new.
            try:
                observed = client.order_by_external_id(str(local["symbol"]), link_id)
            except BybitAPIError as lookup_error:
                if "missing" not in str(lookup_error).lower():
                    raise
                observed = client.place_reduce_only_limit(
                    symbol=str(local["symbol"]), direction=str(local["direction"]),
                    qty=float(leg["volume_contracts"]), price=float(leg["target"]),
                    order_link_id=link_id, position_idx=position_idx,
                )
        state = int(observed.get("state") or 2)
        leg_status = (
            "FILLED" if state == 3 else
            "PARTIAL_TERMINAL" if state == 5 else
            "CANCELED_OR_REJECTED" if state == 4 else
            "ACTIVE"
        )
        now = ls.utc_now()
        with ls.connect(path) as conn:
            conn.execute(
                "INSERT INTO mexc_canary_exit_legs("
                "decision_id,leg_index,exchange_tpsl_id,exchange_order_id,external_oid,order_kind,"
                "target_price,stop_price,volume_contracts,status,created_at,updated_at,exchange_json,venue) "
                "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
                "ON CONFLICT(decision_id,leg_index) DO UPDATE SET "
                "exchange_order_id=excluded.exchange_order_id,external_oid=excluded.external_oid,"
                "target_price=excluded.target_price,stop_price=excluded.stop_price,"
                "volume_contracts=excluded.volume_contracts,status=excluded.status,"
                "updated_at=excluded.updated_at,exchange_json=excluded.exchange_json,venue='bybit'",
                (decision_id, index, None, str(observed.get("orderId") or ""), link_id,
                 "BYBIT_REDUCE_ONLY_TP", float(leg["target"]), wanted_stop,
                 float(leg["volume_contracts"]), leg_status, now, now,
                 json.dumps(observed, sort_keys=True), "bybit"),
            )
            conn.commit()
        if state == 5:
            raise BybitAPIError(f"Bybit TP{index} partially filled and became terminal")
        if state == 4:
            raise BybitAPIError(f"Bybit TP{index} is canceled or rejected")


def _emergency_close_unprotected(*, path: Path, client: BybitFuturesClient,
                                 local: dict[str, Any], plan: dict[str, Any],
                                 reason: str) -> None:
    decision_id = str(local["decision_id"])
    link_id = _emergency_close_link_id(decision_id)
    observed: dict[str, Any] | None = None
    try:
        observed = client.order_by_external_id(str(local["symbol"]), link_id)
    except BybitAPIError as lookup_error:
        if "missing" not in str(lookup_error).lower():
            raise
    if observed is None:
        try:
            observed = client.close_market(
                symbol=str(local["symbol"]), direction=str(local["direction"]),
                qty=float(local["volume_contracts"]), order_link_id=link_id,
                position_idx=int(plan.get("position_idx", 0)),
            )
        except Exception:
            # A POST timeout can happen after acceptance. Resolve the stable
            # orderLinkId before surfacing an unknown emergency-close state.
            observed = client.order_by_external_id(str(local["symbol"]), link_id)
    with ls.connect(path) as conn:
        ls.set_kill_switch(conn, "TRIPPED", "Bybit filled position was not safely protected")
        ls.event(
            conn, "BYBIT_UNPROTECTED_POSITION_EMERGENCY_CLOSE",
            decision_id=decision_id, severity="CRITICAL",
            payload={"reason": reason, "order": observed or {}, "venue": "bybit"},
        )
        conn.commit()


def _close_record(*, path: Path, client: BybitFuturesClient,
                  local: dict[str, Any]) -> None:
    decision_id = str(local["decision_id"])
    opened_at = datetime.fromisoformat(str(local["opened_at"]).replace("Z", "+00:00"))
    opened_ms = int(opened_at.timestamp() * 1000)
    for row in client.closed_pnl(str(local["symbol"])):
        if str(row.get("symbol") or "") != BybitFuturesClient.native_symbol(str(local["symbol"])):
            continue
        closed_ms = int(row.get("updatedTime") or row.get("createdTime") or 0)
        if closed_ms and closed_ms < opened_ms:
            continue
        pnl = float(row.get("closedPnl") or 0)
        fees = abs(float(row.get("openFee") or 0)) + abs(float(row.get("closeFee") or 0))
        with ls.connect(path) as conn:
            conn.execute(
                "UPDATE mexc_canary_positions SET status='CLOSED',closed_at=?,updated_at=?,"
                "last_reconciled_at=?,realized_pnl_usdt=?,fees_usdt=?,funding_usdt=0,"
                "exchange_json=? WHERE decision_id=? AND venue='bybit'",
                (ls.utc_now(), ls.utc_now(), ls.utc_now(), pnl, fees,
                 json.dumps(row, sort_keys=True), decision_id),
            )
            conn.execute(
                "UPDATE mexc_canary_exit_legs SET status='TERMINAL',updated_at=? "
                "WHERE decision_id=? AND venue='bybit' AND status='ACTIVE'",
                (ls.utc_now(), decision_id),
            )
            ls.release_risk(conn, decision_id, "Bybit position closed")
            conn.commit()
        return
    raise BybitAPIError("Bybit position disappeared without closed PnL record")


def reconcile_once(*, db: str | Path, cfg: LiveCanaryConfig,
                   client: BybitFuturesClient) -> dict[str, Any]:
    path = Path(db)
    if not cfg.bybit_live_armed():
        return {"status": "BLOCKED_NOT_ARMED", "orders_checked": 0, "positions_checked": 0}
    stats: dict[str, Any] = {
        "status": "OK", "venue": "bybit", "orders_checked": 0,
        "positions_checked": 0, "filled": 0, "stops_moved": 0,
        "closed": 0, "errors": [],
    }
    with ls.connect(path) as conn:
        ls.ensure_tables(conn)
        orders = [dict(row) for row in conn.execute(
            "SELECT * FROM mexc_canary_orders WHERE venue='bybit' "
            "AND status IN ('SUBMITTED','PENDING','SUBMISSION_UNKNOWN')"
        ).fetchall()]
    for local in orders:
        stats["orders_checked"] += 1
        decision_id = str(local["decision_id"])
        plan = json.loads(str(local["plan_json"]))
        try:
            order = client.order_by_external_id(str(local["symbol"]), str(local["external_oid"]))
            state = int(order.get("state") or 0)
            with ls.connect(path) as conn:
                if state in {3, 5}:
                    position = _position_for_plan(client, plan)
                    if not position:
                        raise BybitAPIError("filled Bybit order has no matching open position")
                    _upsert_position(conn, decision_id=decision_id, plan=plan,
                                     order=order, position=position)
                    _write_order(conn, decision_id=decision_id, plan=plan,
                                 status="FILLED", exchange=order)
                    conn.commit()
                    stats["filled"] += 1
                elif state == 4:
                    _write_order(conn, decision_id=decision_id, plan=plan,
                                 status="CANCELED_OR_INVALID", exchange=order)
                    ls.release_risk(conn, decision_id, "Bybit entry canceled or rejected")
                    conn.commit()
                else:
                    _write_order(conn, decision_id=decision_id, plan=plan,
                                 status="PENDING", exchange=order)
                    conn.commit()
        except Exception as exc:
            stats["errors"].append(f"order:{decision_id}:{type(exc).__name__}:{str(exc)[:160]}")

    with ls.connect(path) as conn:
        positions = [dict(row) for row in conn.execute(
            "SELECT p.*,o.plan_json FROM mexc_canary_positions p JOIN mexc_canary_orders o "
            "ON o.decision_id=p.decision_id WHERE p.status='OPEN' AND p.venue='bybit'"
        ).fetchall()]
    for local in positions:
        stats["positions_checked"] += 1
        decision_id = str(local["decision_id"])
        plan = json.loads(str(local["plan_json"]))
        try:
            position = _position_for_plan(client, plan)
            if not position:
                _close_record(path=path, client=client, local=local)
                stats["closed"] += 1
                continue
            ticker = client.ticker(str(local["symbol"]))
            current = float(ticker.get("fairPrice") or ticker.get("lastPrice") or 0)
            if current <= 0:
                raise BybitAPIError("Bybit ticker has no usable price")
            direction = str(local["direction"])
            prior = float(local.get("favorable_price") or local["entry_price"])
            favorable = max(prior, current) if direction == "long" else min(prior, current)
            try:
                opened_at = datetime.fromisoformat(str(local["opened_at"]).replace("Z", "+00:00"))
                extreme = completed_post_entry_extreme(
                    client, str(local["symbol"]), direction=direction, entry_at=opened_at,
                    observed_at=datetime.now(timezone.utc),
                )
                if extreme is not None:
                    favorable = max(favorable, extreme) if direction == "long" else min(favorable, extreme)
            except Exception:
                pass
            stage, wanted_stop, mfe_r = model_f_stop(
                entry=float(local["entry_price"]), original_stop=float(local["original_stop"]),
                favorable_price=favorable, direction=direction, cfg=cfg,
            )
            tick = float(plan.get("price_tick") or 0)
            if tick > 0:
                units = int(wanted_stop / tick)
                wanted_stop = units * tick if direction == "long" else (units + 1) * tick
            current_stop = float(local["current_stop"])
            move = wanted_stop > current_stop + 1e-12 if direction == "long" else wanted_stop < current_stop - 1e-12
            remote_stop_raw = position.get("stopLoss")
            try:
                remote_stop = float(remote_stop_raw or 0)
            except (TypeError, ValueError):
                remote_stop = 0.0
            remote_stop_missing = (
                "stopLoss" in position
                and (remote_stop <= 0 or abs(remote_stop - (wanted_stop if move else current_stop)) > max(tick, 1e-8))
            )
            install_stop = move or not local.get("tpsl_order_id") or remote_stop_missing
            _ensure_protection(
                path=path, client=client, local=local, plan=plan,
                wanted_stop=wanted_stop if move else current_stop,
                install_stop=install_stop,
            )
            if move:
                current_stop = wanted_stop
                stats["stops_moved"] += 1
            now = ls.utc_now()
            with ls.connect(path) as conn:
                conn.execute(
                    "UPDATE mexc_canary_positions SET favorable_price=?,max_favorable_r=?,"
                    "protection_stage=?,current_stop=?,liquidation_price=?,updated_at=?,"
                    "last_reconciled_at=?,last_price_at=?,last_monitor_error_at=NULL,"
                    "monitor_error_count=0,exchange_json=? WHERE decision_id=? AND venue='bybit'",
                    (favorable, mfe_r, stage, current_stop,
                     float(position.get("liquidatePrice") or 0) or None,
                     now, now, now, json.dumps(position, sort_keys=True), decision_id),
                )
                if move:
                    conn.execute(
                        "UPDATE mexc_canary_exit_legs SET stop_price=?,updated_at=? "
                        "WHERE decision_id=? AND venue='bybit' AND status='ACTIVE'",
                        (current_stop, now, decision_id),
                    )
                    ls.event(conn, "BYBIT_MODEL_F_STOP_MOVED", decision_id=decision_id,
                             payload={"stage": stage, "stop": current_stop, "mfe_r": mfe_r})
                conn.commit()
        except Exception as exc:
            with ls.connect(path) as conn:
                protected_row = conn.execute(
                    "SELECT tpsl_order_id FROM mexc_canary_positions "
                    "WHERE decision_id=? AND venue='bybit'",
                    (decision_id,),
                ).fetchone()
            has_confirmed_stop = bool(protected_row and protected_row[0])
            if not has_confirmed_stop:
                try:
                    _emergency_close_unprotected(
                        path=path, client=client, local=local, plan=plan,
                        reason=f"{type(exc).__name__}:{str(exc)[:300]}",
                    )
                except Exception as close_exc:
                    with ls.connect(path) as conn:
                        ls.set_kill_switch(
                            conn, "TRIPPED",
                            "Bybit protection and emergency-close state are unknown",
                        )
                        ls.event(
                            conn, "BYBIT_EMERGENCY_CLOSE_UNKNOWN",
                            decision_id=decision_id, severity="CRITICAL",
                            payload={"protection_error": str(exc)[:300],
                                     "close_error": str(close_exc)[:300]},
                        )
                        conn.commit()
            stats["errors"].append(
                f"position:{decision_id}:{type(exc).__name__}:{str(exc)[:160]}"
            )
            with ls.connect(path) as conn:
                conn.execute(
                    "UPDATE mexc_canary_positions SET last_monitor_error_at=?,"
                    "monitor_error_count=monitor_error_count+1 WHERE decision_id=?",
                    (ls.utc_now(), decision_id),
                )
                ls.event_if_due(
                    conn, "BYBIT_POSITION_RECONCILE_ERROR", decision_id=decision_id,
                    severity="CRITICAL", payload={"error": str(exc)[:500]}, cooldown_seconds=60,
                )
                conn.commit()
    if stats["errors"]:
        stats["status"] = "DEGRADED"
    return stats
