"""MEXC-native, isolated evidence for the live swing canary.

The production Paper ledger remains authoritative for Paper.  This module is a
separate MEXC price-path comparison: it reads only immutable canary decisions
and MEXC public one-minute candles, then writes only ``mexc_canary_parity_*``
tables.  It deliberately cannot submit, modify, or close a real order.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml

from src.config import load_config

from . import store as ls
from .mexc_client import MexcAPIError, MexcFuturesClient
from .sizing import model_f_stop
from .config import LiveCanaryConfig, load_live_canary_config


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "mexc_swing_exit_variants_shadow.yaml"
_CANDLE_BATCH_SECONDS = 900 * 60
_EPSILON = 1e-12


def _db_path(db: str | Path | None) -> Path:
    return Path(db) if db else load_config().db_path


def _utc(value: str | datetime | None) -> datetime:
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc)
    if value:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).astimezone(timezone.utc)
    return datetime.now(timezone.utc)


def _number(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def load_variant_config(path: str | Path | None = None) -> dict[str, Any]:
    config_path = Path(path) if path else CONFIG_PATH
    if not config_path.exists():
        return {"feature_flag": False}
    with config_path.open("r", encoding="utf-8") as handle:
        return (yaml.safe_load(handle) or {}).get("mexc_swing_exit_variants_shadow") or {}


def _profile_ids(config: dict[str, Any]) -> tuple[str, str]:
    return (
        str(config.get("baseline_profile_id") or "mexc_model_f_runner_v1"),
        str(config.get("partial_profile_id") or "mexc_partial_tp_33_33_34_v1"),
    )


def _path_to_rows(values: Iterable[dict[str, Any]]) -> list[dict[str, float | int]]:
    rows: list[dict[str, float | int]] = []
    for raw in values:
        candle_at = int(raw["candle_at"])
        op, hi, lo, cl = (_number(raw.get(key)) for key in ("open", "high", "low", "close"))
        if min(op or 0, hi or 0, lo or 0, cl or 0) <= 0 or hi < lo:
            continue
        rows.append({"candle_at": candle_at, "open": op, "high": hi, "low": lo, "close": cl})
    return sorted(rows, key=lambda row: int(row["candle_at"]))


def _costs(*, plan: dict[str, Any], entry: float, exits: list[tuple[float, float]],
           risk_usdt: float | None) -> dict[str, float | None]:
    """Conservative estimated costs; actual MEXC fills remain the live authority."""
    notional = _number(plan.get("notional_usdt"))
    if notional is None or entry <= 0:
        return {"gross_pnl_usdt": None, "fees_usdt": None, "slippage_usdt": None,
                "funding_usdt": None, "net_pnl_usdt": None}
    taker_fee = _number(plan.get("taker_fee_rate")) or 0.0
    slippage = _number(plan.get("slippage_rate")) or 0.0
    gross = 0.0
    direction = str(plan.get("direction") or "long").lower()
    volume = _number(plan.get("volume_contracts"))
    contract_size = _number(plan.get("contract_size"))
    if volume is not None and contract_size is not None:
        gross = sum(
            weight * volume * contract_size * (
                (price - entry) if direction == "long" else (entry - price)
            )
            for weight, price in exits
        )
    elif risk_usdt is not None:
        # Legacy parity plans did not retain contract metadata. Keep them
        # comparable without using this fallback for newly captured plans.
        stop = _number(plan.get("original_stop"))
        risk_per_unit = abs(entry - stop) if stop is not None else 0.0
        if risk_per_unit > 0:
            gross = sum(
                weight * ((price - entry) if direction == "long" else (entry - price))
                / risk_per_unit * risk_usdt
                for weight, price in exits
            )
    exit_turnover = sum(weight * notional * (price / entry) for weight, price in exits)
    fees = notional * taker_fee + exit_turnover * taker_fee
    slip = notional * slippage + exit_turnover * slippage
    return {
        "gross_pnl_usdt": gross if risk_usdt is not None else None,
        "fees_usdt": fees,
        "slippage_usdt": slip,
        "funding_usdt": 0.0,
        "net_pnl_usdt": (gross - fees - slip) if risk_usdt is not None else None,
    }


def _result(*, profile_id: str, status: str, clean: bool, entry_at: int, entry: float,
            stop: float, tp1: float | None, tp2: float | None, tp3: float,
            max_r: float, exits: list[tuple[float, float, int, str]],
            plan: dict[str, Any], detail: dict[str, Any]) -> dict[str, Any]:
    risk = _number(plan.get("actual_risk_usdt"))
    closed = bool(exits and abs(sum(weight for weight, *_ in exits) - 1.0) <= 1e-6)
    close_at = max(item[2] for item in exits) if closed else None
    close_reason = exits[-1][3] if closed else None
    cost = _costs(plan=plan, entry=entry, exits=[(weight, price) for weight, price, *_ in exits],
                  risk_usdt=risk) if closed else {
                      "gross_pnl_usdt": None, "fees_usdt": None, "slippage_usdt": None,
                      "funding_usdt": None, "net_pnl_usdt": None,
                  }
    return {
        "profile_id": profile_id,
        "entry_at": datetime.fromtimestamp(entry_at, timezone.utc).isoformat(),
        "entry_price": entry,
        "original_stop": stop,
        "tp1": tp1,
        "tp2": tp2,
        "tp3": tp3,
        "risk_usdt": risk,
        "closed": int(closed),
        "clean": int(clean),
        "status": status,
        "close_at": datetime.fromtimestamp(close_at, timezone.utc).isoformat() if close_at else None,
        "close_price": exits[-1][1] if closed else None,
        "close_reason": close_reason,
        "max_favorable_r": max_r,
        "execution_json": {
            "profile_id": profile_id,
            "exits": [{"weight": weight, "price": price,
                       "at": datetime.fromtimestamp(at, timezone.utc).isoformat(), "reason": reason}
                      for weight, price, at, reason in exits],
            "costs_estimated": True,
            **detail,
        },
        **cost,
    }


def simulate_profile(*, candles: Iterable[dict[str, Any]], decision: dict[str, Any],
                     plan: dict[str, Any], profile_id: str, partial_weights: tuple[float, float, float] | None,
                     now: datetime | None = None, max_hold_hours: int = 168,
                     live_cfg: LiveCanaryConfig | None = None) -> dict[str, Any]:
    """Simulate a deterministic exit on MEXC 1m bars.

    A candle that crosses an active stop and a new target/protection level has
    no known intra-minute order.  Such a path is retained as diagnostics but
    deliberately excluded from evidence rather than credited optimistically.
    """
    live_cfg = live_cfg or load_live_canary_config()
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    entry_at = int(_utc(decision.get("entry_triggered_at") or decision.get("captured_at")).timestamp())
    entry = _number(plan.get("reference_entry")) or _number(decision.get("entry_price"))
    stop = _number(plan.get("original_stop")) or _number(decision.get("original_stop"))
    tp1 = _number(decision.get("tp1"))
    tp2 = _number(decision.get("tp2"))
    tp3 = _number(plan.get("tp3")) or _number(decision.get("tp3"))
    direction = str(plan.get("direction") or decision.get("direction") or "long").lower()
    valid_geometry = (
        stop < entry < tp1 < tp2 < tp3 if direction == "long"
        else tp3 < tp2 < tp1 < entry < stop
    ) if all(value is not None for value in (entry, stop, tp1, tp2, tp3)) else False
    if not valid_geometry:
        return _result(profile_id=profile_id, status="INVALID_GEOMETRY", clean=False,
                       entry_at=entry_at, entry=entry or 0.0, stop=stop or 0.0, tp1=tp1, tp2=tp2,
                       tp3=tp3 or 0.0, max_r=0.0, exits=[], plan=plan, detail={})
    rows = [row for row in _path_to_rows(candles) if int(row["candle_at"]) >= entry_at + 60]
    if not rows or int(rows[0]["candle_at"]) > entry_at + 180:
        return _result(profile_id=profile_id, status="MISSING_ENTRY_COVERAGE", clean=False,
                       entry_at=entry_at, entry=entry, stop=stop, tp1=tp1, tp2=tp2, tp3=tp3,
                       max_r=0.0, exits=[], plan=plan, detail={"rows": len(rows)})

    current_stop = stop
    favorable = entry
    max_r = 0.0
    remaining = 1.0
    exits: list[tuple[float, float, int, str]] = []
    tp1_done = False
    tp2_done = False
    partial = partial_weights is not None
    weights = partial_weights or (0.0, 0.0, 1.0)
    deadline = entry_at + max(1, int(max_hold_hours)) * 3600

    for candle in rows:
        candle_at = int(candle["candle_at"])
        high, low = float(candle["high"]), float(candle["low"])
        if candle_at > deadline:
            break
        next_target = tp1 if partial and not tp1_done else tp2 if partial and not tp2_done else tp3
        stop_hit = low <= current_stop + _EPSILON if direction == "long" else high >= current_stop - _EPSILON
        target_hit = high >= next_target - _EPSILON if direction == "long" else low <= next_target + _EPSILON
        if stop_hit:
            if target_hit:
                return _result(profile_id=profile_id, status="AMBIGUOUS_INTRABAR", clean=False,
                               entry_at=entry_at, entry=entry, stop=stop, tp1=tp1, tp2=tp2, tp3=tp3,
                               max_r=max_r, exits=exits, plan=plan,
                               detail={"candle_at": candle_at, "stop_before": current_stop,
                                       "high": high, "low": low})
            exits.append((remaining, current_stop, candle_at, "model_f_stop"))
            return _result(profile_id=profile_id, status="CLOSED", clean=True,
                           entry_at=entry_at, entry=entry, stop=stop, tp1=tp1, tp2=tp2, tp3=tp3,
                           max_r=max_r, exits=exits, plan=plan, detail={"partial": partial})

        favorable = max(favorable, high) if direction == "long" else min(favorable, low)
        _stage, moved_stop, max_r = model_f_stop(
            entry=entry, original_stop=stop, favorable_price=favorable,
            direction=direction, cfg=live_cfg)

        if partial and tp1 is not None and not tp1_done and (
            high >= tp1 - _EPSILON if direction == "long" else low <= tp1 + _EPSILON
        ):
            exits.append((weights[0], tp1, candle_at, "tp1_partial"))
            remaining -= weights[0]
            tp1_done = True
        if partial and tp2 is not None and not tp2_done and (
            high >= tp2 - _EPSILON if direction == "long" else low <= tp2 + _EPSILON
        ):
            exits.append((weights[1], tp2, candle_at, "tp2_partial"))
            remaining -= weights[1]
            tp2_done = True
        if high >= tp3 - _EPSILON if direction == "long" else low <= tp3 + _EPSILON:
            exits.append((remaining, tp3, candle_at, "tp3_runner"))
            return _result(profile_id=profile_id, status="CLOSED", clean=True,
                           entry_at=entry_at, entry=entry, stop=stop, tp1=tp1, tp2=tp2, tp3=tp3,
                           max_r=max_r, exits=exits, plan=plan, detail={"partial": partial})

        stop_moved = moved_stop > current_stop + _EPSILON if direction == "long" else moved_stop < current_stop - _EPSILON
        if stop_moved:
            moved_stop_hit = low <= moved_stop + _EPSILON if direction == "long" else high >= moved_stop - _EPSILON
            if moved_stop_hit:
                return _result(profile_id=profile_id, status="AMBIGUOUS_INTRABAR", clean=False,
                               entry_at=entry_at, entry=entry, stop=stop, tp1=tp1, tp2=tp2, tp3=tp3,
                               max_r=max_r, exits=exits, plan=plan,
                               detail={"candle_at": candle_at, "stop_after": moved_stop,
                                       "high": high, "low": low})
            current_stop = moved_stop

    status = "OPEN" if int(now.timestamp()) <= deadline else "EXPIRED_UNRESOLVED"
    return _result(profile_id=profile_id, status=status, clean=status == "OPEN",
                   entry_at=entry_at, entry=entry, stop=stop, tp1=tp1, tp2=tp2, tp3=tp3,
                   max_r=max_r, exits=exits, plan=plan,
                   detail={"partial": partial, "last_candle_at": rows[-1]["candle_at"]})


def _store_candles(conn: sqlite3.Connection, *, symbol: str, interval: str,
                   candles: Iterable[dict[str, float | int]]) -> None:
    now = ls.utc_now()
    cols = ("symbol", "interval", "candle_at", "open", "high", "low", "close", "captured_at")
    rows = [(symbol, interval, int(item["candle_at"]), float(item["open"]), float(item["high"]),
             float(item["low"]), float(item["close"]), now) for item in candles]
    if not rows:
        return
    conn.executemany(
        f"INSERT INTO mexc_canary_parity_candles({','.join(cols)}) VALUES({','.join('?' for _ in cols)}) "
        "ON CONFLICT(symbol,interval,candle_at) DO UPDATE SET open=excluded.open,high=excluded.high,"
        "low=excluded.low,close=excluded.close,captured_at=excluded.captured_at",
        rows,
    )


def _fetch_incremental_candles(*, conn: sqlite3.Connection, client: MexcFuturesClient,
                               symbol: str, interval: str, start: int, end: int) -> int:
    row = conn.execute(
        "SELECT MAX(candle_at) FROM mexc_canary_parity_candles WHERE symbol=? AND interval=? AND candle_at>=?",
        (symbol, interval, start),
    ).fetchone()
    cursor = max(start, int(row[0] or start) - 120)
    fetched = 0
    while cursor < end:
        chunk_end = min(cursor + _CANDLE_BATCH_SECONDS, end)
        candles = client.klines(symbol, start_seconds=cursor, end_seconds=chunk_end, interval=interval)
        _store_candles(conn, symbol=symbol, interval=interval, candles=candles)
        fetched += len(candles)
        cursor = chunk_end + 60
    return fetched


def _persist_outcome(conn: sqlite3.Connection, *, decision_id: str, signal_id: str,
                     symbol: str, outcome: dict[str, Any], evidence_class: str) -> None:
    now = ls.utc_now()
    cols = (
        "decision_id", "profile_id", "signal_id", "symbol", "entry_at", "entry_price", "original_stop",
        "tp1", "tp2", "tp3", "risk_usdt", "closed", "clean", "status", "close_at", "close_price",
        "close_reason", "gross_pnl_usdt", "fees_usdt", "slippage_usdt", "funding_usdt", "net_pnl_usdt",
        "max_favorable_r", "evidence_class", "execution_json", "created_at", "updated_at",
    )
    data = {
        "decision_id": decision_id, "signal_id": signal_id, "symbol": symbol,
        "created_at": now, "updated_at": now, "evidence_class": evidence_class, **outcome,
    }
    data["execution_json"] = json.dumps(outcome["execution_json"], sort_keys=True)
    values = [data.get(column) for column in cols]
    conn.execute(
        f"INSERT INTO mexc_canary_parity_outcomes({','.join(cols)}) VALUES({','.join('?' for _ in cols)}) "
        "ON CONFLICT(decision_id,profile_id) DO UPDATE SET closed=excluded.closed,clean=excluded.clean,"
        "status=excluded.status,close_at=excluded.close_at,close_price=excluded.close_price,"
        "close_reason=excluded.close_reason,gross_pnl_usdt=excluded.gross_pnl_usdt,fees_usdt=excluded.fees_usdt,"
        "slippage_usdt=excluded.slippage_usdt,funding_usdt=excluded.funding_usdt,net_pnl_usdt=excluded.net_pnl_usdt,"
        "max_favorable_r=excluded.max_favorable_r,evidence_class=excluded.evidence_class,"
        "execution_json=excluded.execution_json,updated_at=excluded.updated_at",
        values,
    )


def refresh(*, db: str | Path | None = None, client: MexcFuturesClient | None = None,
            now: datetime | None = None, limit: int = 30) -> dict[str, int | str]:
    """Refresh isolated MEXC parity profiles from already-validated plans."""
    config = load_variant_config()
    if not config.get("feature_flag", False):
        return {"status": "DISABLED", "plans": 0, "outcomes": 0, "candles": 0}
    path = _db_path(db)
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    interval = str(config.get("interval") or "Min1")
    baseline_id, partial_id = _profile_ids(config)
    raw_weights = tuple(float(value) for value in (config.get("partial_weights") or (0.33, 0.33, 0.34)))
    if len(raw_weights) != 3 or abs(sum(raw_weights) - 1.0) > 1e-9 or min(raw_weights) <= 0:
        raise ValueError("partial_weights must contain three positive values totaling 1.0")
    live_cfg = load_live_canary_config()
    client = client or MexcFuturesClient(
        base_url=str(live_cfg.get("api_base_url", "https://api.mexc.com")),
        timeout_seconds=float(live_cfg.get("request_timeout_seconds", 8)),
        recv_window_seconds=int(live_cfg.get("recv_window_seconds", 10)),
    )
    with ls.connect(path) as conn:
        ls.ensure_tables(conn)
        # Plans existed before this isolated parity table was introduced.  Import
        # only immutable plans already persisted by the canary; never recreate
        # or submit an order, and never infer a plan for a rejected preflight.
        legacy_plans = conn.execute(
            "SELECT o.decision_id,d.signal_id,o.symbol,o.plan_json,d.captured_at "
            "FROM mexc_canary_orders o JOIN mexc_canary_decisions d ON d.decision_id=o.decision_id "
            "WHERE o.plan_json IS NOT NULL AND o.plan_json!=''"
        ).fetchall()
        for old in legacy_plans:
            try:
                exists = conn.execute(
                    "SELECT 1 FROM mexc_canary_parity_plans WHERE decision_id=?",
                    (str(old["decision_id"]),),
                ).fetchone()
                if exists:
                    continue
                ls.upsert_parity_plan(
                    conn,
                    decision_id=str(old["decision_id"]),
                    signal_id=str(old["signal_id"]),
                    symbol=str(old["symbol"]),
                    plan=json.loads(str(old["plan_json"])),
                    source="existing_canary_order",
                    captured_at=str(old["captured_at"]),
                )
            except (TypeError, ValueError, json.JSONDecodeError):
                continue
        conn.commit()
        plans = [dict(row) for row in conn.execute(
            "SELECT p.decision_id,p.signal_id,p.symbol,p.plan_json,p.captured_at,p.evidence_class,"
            "p.clean,d.decision_json "
            "FROM mexc_canary_parity_plans p JOIN mexc_canary_decisions d ON d.decision_id=p.decision_id "
            "ORDER BY p.updated_at DESC LIMIT ?", (max(1, int(limit)),)
        ).fetchall()]
    counts = {
        "status": "OK", "plans": len(plans), "outcomes": 0, "candles": 0,
        "skipped_non_crypto": 0, "skipped_unavailable_contract": 0,
        "skipped_source_error": 0,
    }
    for record in plans:
        # This comparison is crypto-only. Stock-futures canary rows share the
        # decision store, but are not valid inputs for MEXC's crypto kline API.
        if str(record["signal_id"] or "").startswith("stock_mexc:"):
            counts["skipped_non_crypto"] += 1
            continue
        decision = json.loads(record["decision_json"])
        plan = json.loads(record["plan_json"])
        entry_at = int(_utc(decision.get("entry_triggered_at") or decision.get("captured_at")).timestamp())
        end_at = min(int(now.timestamp()), entry_at + int(config.get("max_hold_hours", 168)) * 3600)
        with ls.connect(path) as conn:
            ls.ensure_tables(conn)
            try:
                counts["candles"] += _fetch_incremental_candles(
                    conn=conn, client=client, symbol=str(record["symbol"]), interval=interval,
                    start=entry_at, end=end_at,
                )
            except MexcAPIError as exc:
                if "contract does not exist" in str(exc).lower():
                    counts["skipped_unavailable_contract"] += 1
                else:
                    # Parity is a shadow evidence refresh. A transient public
                    # kline failure for one symbol must not discard the other
                    # valid plans or fail the scheduler cycle.
                    counts["skipped_source_error"] += 1
                continue
            conn.commit()
            candles = [dict(row) for row in conn.execute(
                "SELECT candle_at,open,high,low,close FROM mexc_canary_parity_candles "
                "WHERE symbol=? AND interval=? AND candle_at>=? AND candle_at<=? ORDER BY candle_at",
                (record["symbol"], interval, entry_at, end_at),
            ).fetchall()]
            baseline = simulate_profile(
                candles=candles, decision=decision, plan=plan, profile_id=baseline_id,
                partial_weights=None, now=now, max_hold_hours=int(config.get("max_hold_hours", 168)),
                live_cfg=live_cfg,
            )
            partial = simulate_profile(
                candles=candles, decision=decision, plan=plan, profile_id=partial_id,
                partial_weights=raw_weights, now=now, max_hold_hours=int(config.get("max_hold_hours", 168)),
                live_cfg=live_cfg,
            )
            for outcome in (baseline, partial):
                _persist_outcome(conn, decision_id=str(record["decision_id"]),
                                 signal_id=str(record["signal_id"]), symbol=str(record["symbol"]),
                                 outcome=outcome,
                                 evidence_class=str(record.get("evidence_class") or "historical_backfill"))
                counts["outcomes"] += 1
            conn.commit()
    return counts


def report(*, db: str | Path | None = None) -> dict[str, Any]:
    """Return compact profile-level diagnostics without touching the live or Paper ledger."""
    path = _db_path(db)
    with ls.connect(path) as conn:
        ls.ensure_tables(conn)
        rows = conn.execute(
            "SELECT profile_id,COUNT(*) AS n,SUM(CASE WHEN closed=1 AND clean=1 THEN 1 ELSE 0 END) AS closed_clean,"
            "SUM(CASE WHEN closed=1 AND clean=1 AND evidence_class='forward_post_activation' "
            "THEN 1 ELSE 0 END) AS forward_closed_clean,"
            "SUM(CASE WHEN clean=0 THEN 1 ELSE 0 END) AS excluded,"
            "SUM(CASE WHEN closed=1 AND clean=1 THEN COALESCE(net_pnl_usdt,0) ELSE 0 END) AS net_pnl_usdt,"
            "SUM(CASE WHEN closed=1 AND clean=1 AND evidence_class='forward_post_activation' "
            "THEN COALESCE(net_pnl_usdt,0) ELSE 0 END) AS forward_net_pnl_usdt,"
            "SUM(CASE WHEN closed=1 AND clean=1 AND net_pnl_usdt>0 THEN net_pnl_usdt ELSE 0 END) AS gross_win,"
            "SUM(CASE WHEN closed=1 AND clean=1 AND net_pnl_usdt<0 THEN -net_pnl_usdt ELSE 0 END) AS gross_loss,"
            "SUM(CASE WHEN closed=1 AND clean=1 AND evidence_class='forward_post_activation' "
            "AND net_pnl_usdt>0 THEN net_pnl_usdt ELSE 0 END) AS forward_gross_win,"
            "SUM(CASE WHEN closed=1 AND clean=1 AND evidence_class='forward_post_activation' "
            "AND net_pnl_usdt<0 THEN -net_pnl_usdt ELSE 0 END) AS forward_gross_loss "
            "FROM mexc_canary_parity_outcomes GROUP BY profile_id ORDER BY profile_id"
        ).fetchall()
    profiles = []
    for row in rows:
        gross_loss = float(row["gross_loss"] or 0.0)
        forward_closed = int(row["forward_closed_clean"] or 0)
        forward_pnl = float(row["forward_net_pnl_usdt"] or 0.0)
        forward_loss = float(row["forward_gross_loss"] or 0.0)
        forward_pf = (None if forward_loss == 0 else
                      round(float(row["forward_gross_win"] or 0.0) / forward_loss, 4))
        minimum_pf = float((load_live_canary_config().get("mexc_native_parity", {}) or {})
                           .get("minimum_profit_factor", 1.25))
        review_status = (
            "REVIEW_ONLY" if (forward_closed >= 30 and forward_pnl > 0
                              and (forward_pf is None or forward_pf >= minimum_pf))
            else "NOT_READY_EDGE" if forward_closed >= 30
            else "EARLY_REVIEW_WINDOW" if forward_closed >= 20
            else "ACCUMULATING_FORWARD_EVIDENCE"
        )
        profiles.append({
            "profile_id": row["profile_id"], "n": int(row["n"] or 0),
            "closed_clean": int(row["closed_clean"] or 0), "excluded": int(row["excluded"] or 0),
            "net_pnl_usdt": float(row["net_pnl_usdt"] or 0.0),
            "forward_closed_clean": forward_closed,
            "forward_net_pnl_usdt": forward_pnl,
            "forward_profit_factor": forward_pf,
            "review_status": review_status,
            "profit_factor": None if gross_loss == 0 else round(float(row["gross_win"] or 0.0) / gross_loss, 4),
        })
    return {"profiles": profiles}
