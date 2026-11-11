from __future__ import annotations

import argparse
import json
import math
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import requests

from src.data_collectors.crypto_invest_universe import load_selected_symbols
from research_labs.technical_trend_reclaim.src.engine import Bundle, Fold, evaluate_variant
from research_labs.technical_trend_reclaim.src.features import add_indicators
from research_labs.technical_trend_reclaim.src.simulator import simulate

from .common import ARTIFACT_ROOT, LAB_ROOT, connect, digest, load_config, stable_json, utc_now
from . import near_miss
from .regime import conditioned_gate
from .run_backtest import FROZEN_PROFILE_PATH, _load_frozen_variant


BINANCE_KLINES = "https://fapi.binance.com/fapi/v1/klines"
BYBIT_KLINES = "https://api.bybit.com/v5/market/kline"
MEXC_TICKERS = "https://api.mexc.com/api/v1/contract/ticker"
BINANCE_ALIASES = {
    "PEPE/USDT": "1000PEPEUSDT",
    "SHIB/USDT": "1000SHIBUSDT",
    "BONK/USDT": "1000BONKUSDT",
    "FLOKI/USDT": "1000FLOKIUSDT",
}
LOCK_PATH = LAB_ROOT / "forward_shadow.lock"
QUARTER_SECONDS = 15 * 60
SCAN_START_DELAY_SECONDS = 5


def _native(symbol: str) -> str:
    return BINANCE_ALIASES.get(symbol, symbol.replace("/", ""))


def _mexc_native(symbol: str) -> str:
    return symbol.replace("/", "_").upper()


def _closed_and_current(frame: pd.DataFrame, *, minutes: int, fetched_at: datetime,
                        source: str) -> tuple[pd.DataFrame, dict[str, Any] | None]:
    """Split a venue response without accidentally using an unfinished candle."""
    if frame.empty:
        return frame, None
    frame = frame.copy()
    frame["bar_open_at"] = pd.to_datetime(frame["bar_open_at"], utc=True)
    frame["bar_close_at"] = frame["bar_open_at"] + pd.Timedelta(minutes=minutes) - pd.Timedelta(milliseconds=1)
    frame["available_at"] = frame["bar_close_at"] + pd.Timedelta(milliseconds=1)
    frame["ingested_at"] = pd.Timestamp(fetched_at)
    frame = frame.sort_values("bar_open_at").drop_duplicates("bar_open_at")
    closed = frame[frame["bar_close_at"] < pd.Timestamp(fetched_at)].copy()
    current_rows = frame[frame["bar_close_at"] >= pd.Timestamp(fetched_at)]
    current = current_rows.iloc[-1].to_dict() if not current_rows.empty else None
    closed.attrs["source"] = source
    return closed, current


def _binance_bars(symbol: str, interval: str, limit: int) -> tuple[pd.DataFrame, dict[str, Any] | None]:
    response = requests.get(
        BINANCE_KLINES,
        params={"symbol": _native(symbol), "interval": interval, "limit": limit},
        timeout=12,
    )
    response.raise_for_status()
    rows = response.json()
    fetched_at = datetime.now(timezone.utc)
    parsed = [
        {
            "bar_open_at": pd.to_datetime(int(row[0]), unit="ms", utc=True),
            "open": float(row[1]), "high": float(row[2]), "low": float(row[3]),
            "close": float(row[4]), "volume": float(row[5]),
            "quote_volume": float(row[7]),
        }
        for row in rows
    ]
    return _closed_and_current(
        pd.DataFrame(parsed), minutes={"15m": 15, "1h": 60, "4h": 240}[interval],
        fetched_at=fetched_at, source="binance_fapi",
    )


def _bybit_bars(symbol: str, interval: str, limit: int) -> tuple[pd.DataFrame, dict[str, Any] | None]:
    minutes = {"15m": 15, "1h": 60, "4h": 240}[interval]
    response = requests.get(
        BYBIT_KLINES,
        params={"category": "linear", "symbol": symbol.replace("/", ""),
                "interval": str(minutes), "limit": min(limit, 1000)},
        timeout=12,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("retCode") != 0:
        raise RuntimeError(f"Bybit kline rejected: {payload.get('retCode')} {payload.get('retMsg')}")
    parsed = [
        {"bar_open_at": pd.to_datetime(int(row[0]), unit="ms", utc=True),
         "open": float(row[1]), "high": float(row[2]), "low": float(row[3]),
         "close": float(row[4]), "volume": float(row[5]), "quote_volume": float(row[6])}
        for row in ((payload.get("result") or {}).get("list") or [])
    ]
    return _closed_and_current(
        pd.DataFrame(parsed), minutes=minutes, fetched_at=datetime.now(timezone.utc),
        source="bybit_v5_linear_fallback",
    )


def _bars(symbol: str, interval: str, limit: int, observed: datetime) -> tuple[pd.DataFrame, dict[str, Any] | None]:
    """Use Binance when reachable and Bybit as a public perpetual-feed fallback."""
    try:
        return _binance_bars(symbol, interval, limit)
    except (requests.RequestException, ValueError, TypeError, KeyError) as binance_error:
        try:
            return _bybit_bars(symbol, interval, limit)
        except (requests.RequestException, ValueError, TypeError, KeyError) as bybit_error:
            raise RuntimeError(
                f"market data unavailable for {symbol} {interval}: "
                f"binance={type(binance_error).__name__}; bybit={type(bybit_error).__name__}"
            ) from bybit_error


def _mexc_tickers() -> dict[str, dict[str, Any]]:
    response = requests.get(MEXC_TICKERS, timeout=12)
    response.raise_for_status()
    payload = response.json()
    rows = payload.get("data") or []
    if isinstance(rows, dict):
        rows = [rows]
    return {str(row.get("symbol") or "").upper(): row for row in rows if row.get("symbol")}


def _mexc_quote(symbol: str, tickers: dict[str, dict[str, Any]]) -> dict[str, Any]:
    native = _mexc_native(symbol)
    row = tickers.get(native)
    if row is None:
        return {"status": "unavailable", "contract": native}
    def number(*keys: str) -> float | None:
        for key in keys:
            try:
                value = float(row.get(key))
                if value > 0:
                    return value
            except (TypeError, ValueError):
                pass
        return None
    bid = number("bid1Price", "bid1", "bidPrice", "bid")
    ask = number("ask1Price", "ask1", "askPrice", "ask")
    fair = number("fairPrice", "lastPrice")
    mid = (bid + ask) / 2 if bid and ask else fair
    spread = ((ask - bid) / mid * 10_000) if bid and ask and mid else None
    return {
        "status": "ok" if mid else "unavailable", "contract": native,
        "bid": bid, "ask": ask, "fair": fair, "mid": mid, "spread_bps": spread,
    }


def _bundle(symbol: str, observed: datetime) -> tuple[Bundle, pd.Timestamp, dict[str, str]]:
    strategy = load_config(LAB_ROOT / "config" / "crypto_v2.yaml")["strategy"]
    # The three independent public endpoints dominate scan latency. Fetch them
    # together so a 60-symbol pass stays close to the 15m bar boundary.
    with ThreadPoolExecutor(max_workers=3) as pool:
        entry_future = pool.submit(_bars, symbol, "15m", 1000, observed)
        h1_future = pool.submit(_bars, symbol, "1h", 600, observed)
        context_future = pool.submit(_bars, symbol, "4h", 500, observed)
        entry, current = entry_future.result()
        h1, _ = h1_future.result()
        context, _ = context_future.result()
    if current is None or entry.empty or h1.empty or context.empty:
        raise RuntimeError("closed/current bar coverage unavailable")
    sources = {
        "m15": str(entry.attrs.get("source") or "unknown"),
        "h1": str(h1.attrs.get("source") or "unknown"),
        "h4": str(context.attrs.get("source") or "unknown"),
    }
    current_open = pd.to_datetime(current["bar_open_at"], utc=True)
    synthetic = dict(current)
    open_price = float(current["open"])
    synthetic.update({
        "high": open_price, "low": open_price, "close": open_price, "volume": 0.0,
        "quote_volume": 0.0, "bar_close_at": current_open,
        "available_at": pd.Timestamp(observed), "ingested_at": pd.Timestamp(observed),
    })
    entry = pd.concat([entry, pd.DataFrame([synthetic])], ignore_index=True)
    entry = add_indicators(entry, strategy, session_vwap=False)
    h1 = add_indicators(h1, strategy, session_vwap=False)
    context = add_indicators(context, strategy, session_vwap=False)
    source_times = {
        "m15_last_closed": pd.to_datetime(entry.iloc[-2]["bar_close_at"], utc=True).isoformat(),
        "m15_current_open": current_open.isoformat(),
        "h1_last_closed": pd.to_datetime(h1.iloc[-1]["bar_close_at"], utc=True).isoformat(),
        "h4_last_closed": pd.to_datetime(context.iloc[-1]["bar_close_at"], utc=True).isoformat(),
        "m15_source": sources["m15"], "h1_source": sources["h1"], "h4_source": sources["h4"],
        "observed_at": observed.isoformat(),
    }
    empty = pd.DataFrame()
    return Bundle("crypto", symbol, h1, context, entry, "15m", sources["m15"], empty, empty), current_open, source_times


def _decision_is_late(latency_seconds: float, forward_cfg: dict[str, Any]) -> bool:
    return latency_seconds > float(forward_cfg.get("max_decision_latency_seconds", 120.0))


def _decision_rows(
    symbol: str, variant: dict[str, Any], profile_hash: str, strategy_id: str,
    observed: datetime, tickers: dict[str, dict[str, Any]], btc_context: pd.DataFrame,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cfg = load_config(LAB_ROOT / "config" / "crypto_v2.yaml")
    forward_cfg = cfg["forward"]
    bundle, current_open, source_times = _bundle(symbol, observed)
    decision_observed = datetime.now(timezone.utc)
    source_times["decision_observed_at"] = decision_observed.isoformat()
    fold = Fold("forward_point_in_time", current_open - pd.Timedelta(hours=36), current_open + pd.Timedelta(milliseconds=1))
    gate = lambda current, at, direction, params: conditioned_gate(
        current, btc_context, at, direction, params, cfg["strategy"]
    )
    candidates, fills = evaluate_variant(
        run_id="forward", bundle=bundle, variant=variant, fold=fold, cfg=cfg,
        regime_gate=gate, apply_fold_embargo=False,
    )
    fill_ids = {str(row["candidate_id"]): row for row in fills}
    quote = _mexc_quote(symbol, tickers)
    output: list[dict[str, Any]] = []
    cutoff = pd.Timestamp(observed) - pd.Timedelta(minutes=17)
    for candidate in candidates:
        decision_at = pd.to_datetime(candidate["decision_at"], utc=True, errors="coerce")
        entry_at = pd.to_datetime(candidate.get("entry_at"), utc=True, errors="coerce")
        actionable = str(candidate["candidate_id"]) in fill_ids and entry_at == current_open
        recent_rejection = candidate["status"] == "rejected" and pd.notna(decision_at) and decision_at >= cutoff
        if not actionable and not recent_rejection:
            continue
        latency = max(0.0, (pd.Timestamp(decision_observed) - (entry_at if actionable else decision_at)).total_seconds())
        features = json.loads(candidate["features_json"])
        features["mexc_quote"] = quote
        zone = features.get("zone") if isinstance(features.get("zone"), dict) else {}
        reference_bar = bundle.entry.iloc[-2]
        reference_price = float(reference_bar["close"])
        reference_at = pd.to_datetime(reference_bar["bar_close_at"], utc=True)
        features["near_miss_reference"] = {
            "at": reference_at.isoformat(),
            "price": reference_price,
            "source": "last_closed_15m_close",
            "risk_unit_price": zone.get("atr"),
            "risk_unit_source": "zone_atr_proxy",
            "targets_r": list(variant.get("targets_r", cfg["strategy"]["crypto_targets_r"])),
        }
        status = "REJECTED"
        clean = latency <= float(forward_cfg.get("clean_latency_seconds", 90.0))
        entry_price = stop_price = None
        targets: list[float] = []
        reason = candidate.get("rejection_reason")
        if actionable:
            geometry = json.loads(candidate["geometry_json"])
            strategy_entry = float(geometry["entry"])
            strategy_stop = float(geometry["stop"])
            mexc_entry = quote.get("mid")
            basis = abs(float(mexc_entry) / strategy_entry - 1.0) if mexc_entry else None
            unit_pct = abs(strategy_entry - strategy_stop) / strategy_entry
            too_late = _decision_is_late(latency, forward_cfg)
            clean = bool(
                not too_late and clean and mexc_entry and basis is not None and basis <= 0.02
                and quote.get("spread_bps") is not None and float(quote["spread_bps"]) <= 20.0
            )
            if mexc_entry:
                entry_price = float(mexc_entry)
                stop_price = entry_price * (1.0 - unit_pct if candidate["direction"] == "long" else 1.0 + unit_pct)
                risk = abs(entry_price - stop_price)
                targets = [
                    entry_price + value * risk if candidate["direction"] == "long" else entry_price - value * risk
                    for value in variant["targets_r"]
                ]
            features["binance_strategy_entry"] = strategy_entry
            features["mexc_basis_abs_pct"] = basis
            if too_late:
                status = "STALE_DECISION_NOT_ACTIONABLE"
                reason = "SCHEDULER_LATE_DECISION"
            else:
                status = "ELIGIBLE_FORWARD_ENTRY" if clean else "DIRTY_ELIGIBLE_NOT_EDGE"
                reason = None if clean else "FORWARD_EXECUTION_OR_LATENCY_DIRTY"
        decision_key = {
            "strategy_id": strategy_id, "profile_hash": profile_hash,
            "symbol": symbol, "candidate_id": candidate["candidate_id"],
            "decision_at": decision_at.isoformat(),
        }
        output.append({
            "decision_id": digest(decision_key)[:32], "strategy_id": strategy_id,
            "profile_hash": profile_hash, "symbol": symbol, "direction": candidate["direction"],
            "formed_at": candidate["fvg_formed_at"], "decision_at": decision_at.isoformat(),
            "observed_at": decision_observed.isoformat(), "latency_seconds": latency,
            "status": status, "rejection_reason": reason, "is_clean": int(clean),
            "entry_price": entry_price, "stop_price": stop_price,
            "targets_json": stable_json(targets), "features_json": stable_json(features),
            "source_times_json": stable_json(source_times), "created_at": decision_observed.isoformat(),
        })
    return output, {"symbol": symbol, "decisions": len(output), "source_times": source_times}


def _insert_decisions(rows: list[dict[str, Any]]) -> int:
    if not rows:
        return 0
    columns = list(rows[0])
    placeholders = ",".join("?" for _ in columns)
    with connect() as conn:
        before = conn.total_changes
        conn.executemany(
            f"INSERT OR IGNORE INTO forward_decisions ({','.join(columns)}) VALUES ({placeholders})",
            [[row.get(column) for column in columns] for row in rows],
        )
        return conn.total_changes - before


def _persist_scan_health(health: dict[str, Any]) -> None:
    observed_at = str(health["observed_at"])
    with connect() as conn:
        conn.execute(
            "INSERT INTO forward_meta(key,value_json,updated_at) VALUES('last_scan',?,?) "
            "ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json,updated_at=excluded.updated_at",
            (stable_json(health), observed_at),
        )
    (ARTIFACT_ROOT / "FORWARD_LAST_SCAN.json").write_text(stable_json(health) + "\n", encoding="utf-8")


def scan_once(workers: int = 6) -> dict[str, Any]:
    cfg = load_config(LAB_ROOT / "config" / "crypto_v2.yaml")
    variant, frozen = _load_frozen_variant(FROZEN_PROFILE_PATH)
    strategy_id = str(cfg["forward"]["strategy_id"])
    profile_hash = str(variant["parameter_hash"])
    symbols = load_selected_symbols()
    observed = datetime.now(timezone.utc)
    started = time.monotonic()
    try:
        tickers = _mexc_tickers()
        btc_context = _bundle("BTC/USDT", observed)[0].context
    except Exception as exc:
        health = {
            "observed_at": observed.isoformat(), "strategy_id": strategy_id,
            "profile_hash": profile_hash, "frozen_run_id": frozen.get("run_id"),
            "symbols": len(symbols), "evaluated": 0,
            "errors": [{"stage": "market_context", "error": f"{type(exc).__name__}: {exc}"}],
            "decisions_seen": 0, "decisions_inserted": 0,
            "scan_duration_seconds": round(time.monotonic() - started, 3),
            "status": "MARKET_DATA_UNAVAILABLE",
        }
        _persist_scan_health(health)
        return health
    rows: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = {
            pool.submit(
                _decision_rows, symbol, variant, profile_hash, strategy_id,
                observed, tickers, btc_context,
            ): symbol
            for symbol in symbols
        }
        for future in as_completed(futures):
            symbol = futures[future]
            try:
                decisions, diagnostic = future.result()
                rows.extend(decisions)
                diagnostics.append(diagnostic)
            except Exception as exc:
                errors.append({"symbol": symbol, "error": f"{type(exc).__name__}: {exc}"})
    inserted = _insert_decisions(rows)
    # The strategy ledger is the sole source for diagnostic IDs. Reading it after
    # insertion prevents one candidate from being recorded twice under a transient
    # candidate ID and then its persisted decision ID.
    with connect() as conn:
        persisted_rejections = [dict(row) for row in conn.execute(
            "SELECT * FROM forward_decisions WHERE status <> 'ELIGIBLE_FORWARD_ENTRY'"
        ).fetchall()]
    near_miss_sync = near_miss.record_decisions(
        persisted_rejections, frozen_run_id=str(frozen.get("run_id") or "") or None,
    )
    fallback_source_symbols = sorted({
        row["symbol"] for row in diagnostics
        if any(str(row["source_times"].get(key) or "").startswith("bybit_")
               for key in ("m15_source", "h1_source", "h4_source"))
    })
    late_decisions = sum(1 for row in rows if row["status"] == "STALE_DECISION_NOT_ACTIONABLE")
    health = {
        "observed_at": observed.isoformat(), "strategy_id": strategy_id,
        "profile_hash": profile_hash, "frozen_run_id": frozen.get("run_id"),
        "symbols": len(symbols), "evaluated": len(diagnostics), "errors": errors,
        "decisions_seen": len(rows), "decisions_inserted": inserted,
        "late_decisions": late_decisions,
        "near_miss": near_miss_sync,
        "fallback_source_symbols": fallback_source_symbols,
        "scan_duration_seconds": round(time.monotonic() - started, 3),
        "status": "OK" if not errors else "PARTIAL_MARKET_DATA",
    }
    _persist_scan_health(health)
    return health


def _recent_closed_bars(symbol: str, observed: datetime) -> pd.DataFrame:
    bars, _ = _bars(symbol, "15m", 500, observed)
    return bars


def refresh_outcomes() -> dict[str, Any]:
    cfg = load_config(LAB_ROOT / "config" / "crypto_v2.yaml")
    variant, _ = _load_frozen_variant(FROZEN_PROFILE_PATH)
    costs = cfg["costs"]["crypto"]
    now = datetime.now(timezone.utc)
    with connect() as conn:
        open_rows = conn.execute(
            "SELECT d.* FROM forward_decisions d LEFT JOIN forward_outcomes o ON o.decision_id=d.decision_id "
            "WHERE d.status IN ('ELIGIBLE_FORWARD_ENTRY','DIRTY_ELIGIBLE_NOT_EDGE') "
            "AND (o.decision_id IS NULL OR o.outcome_status='open')"
        ).fetchall()
    cache: dict[str, pd.DataFrame] = {}
    updates = []
    for raw in open_rows:
        row = dict(raw)
        symbol = str(row["symbol"])
        try:
            bars = cache.setdefault(symbol, _recent_closed_bars(symbol, now))
        except Exception:
            continue
        source_times = json.loads(row["source_times_json"])
        entry_at = pd.to_datetime(source_times["m15_current_open"], utc=True)
        future = bars[bars["bar_open_at"] >= entry_at].copy()
        if future.empty:
            continue
        age_hours = (pd.Timestamp(now) - entry_at).total_seconds() / 3600.0
        result = simulate(
            direction=str(row["direction"]), entry=float(row["entry_price"]), stop=float(row["stop_price"]),
            targets_r=list(variant["targets_r"]), bars=future,
            risk_usd=float(costs["risk_usd"]), taker_fee_rate=float(costs["taker_fee_rate"]),
            maker_fee_rate=float(costs["maker_fee_rate"]), slippage_bps=float(costs["slippage_bps_stress"]),
            model_f=cfg["strategy"]["model_f"], force_exit_at_end=age_hours >= 72.0,
        ).to_dict()
        closed = result["status"] == "closed"
        updates.append({
            "decision_id": row["decision_id"], "outcome_status": "closed" if closed else "open",
            "entry_at": entry_at.isoformat(), "exit_at": result["exit_at"] if closed else None,
            "close_reason": result["close_reason"] if closed else None,
            "gross_pnl_usd": result["gross_pnl_usd"] if closed else None,
            "net_pnl_usd": result["net_pnl_usd"] if closed else None,
            "fees_usd": result["fees_usd"] if closed else None,
            "slippage_usd": result["slippage_usd"] if closed else None,
            "funding_usd": result["funding_usd"] if closed else None,
            "updated_at": now.isoformat(),
        })
    if updates:
        columns = list(updates[0])
        with connect() as conn:
            conn.executemany(
                f"INSERT INTO forward_outcomes ({','.join(columns)}) VALUES ({','.join('?' for _ in columns)}) "
                "ON CONFLICT(decision_id) DO UPDATE SET outcome_status=excluded.outcome_status,"
                "entry_at=excluded.entry_at,exit_at=excluded.exit_at,close_reason=excluded.close_reason,"
                "gross_pnl_usd=excluded.gross_pnl_usd,net_pnl_usd=excluded.net_pnl_usd,"
                "fees_usd=excluded.fees_usd,slippage_usd=excluded.slippage_usd,"
                "funding_usd=excluded.funding_usd,updated_at=excluded.updated_at",
                [[row[column] for column in columns] for row in updates],
            )
    return {"checked": len(open_rows), "updated": len(updates), "at": now.isoformat()}


def _max_drawdown(values: list[float], risk_usd: float) -> float:
    equity = peak = drawdown = 0.0
    for value in values:
        equity += value / risk_usd
        peak = max(peak, equity)
        drawdown = max(drawdown, peak - equity)
    return drawdown


def readiness_report() -> dict[str, Any]:
    cfg = load_config(LAB_ROOT / "config" / "crypto_v2.yaml")
    with connect() as conn:
        rows = conn.execute(
            "SELECT d.*,o.* FROM forward_decisions d JOIN forward_outcomes o USING(decision_id) "
            "WHERE d.is_clean=1 AND d.status='ELIGIBLE_FORWARD_ENTRY' AND o.outcome_status='closed' "
            "ORDER BY o.exit_at"
        ).fetchall()
    data = [dict(row) for row in rows]
    pnl = [float(row["net_pnl_usd"]) for row in data]
    wins = sum(value > 0 for value in pnl)
    gross_win = sum(value for value in pnl if value > 0)
    gross_loss = -sum(value for value in pnl if value < 0)
    first = min((pd.to_datetime(row["decision_at"], utc=True) for row in data), default=None)
    days = (pd.Timestamp.now(tz="UTC") - first).days + 1 if first is not None else 0
    directions = sorted({str(row["direction"]) for row in data})
    metrics = {
        "clean_closed": len(data), "forward_days": days, "net_pnl_usd": sum(pnl),
        "profit_factor": gross_win / gross_loss if gross_loss else None,
        "winrate": wins / len(data) if data else None,
        "max_drawdown_r": _max_drawdown(pnl, float(cfg["costs"]["crypto"]["risk_usd"])),
        "directions": directions,
        "latency_p90_seconds": float(np.percentile([float(row["latency_seconds"]) for row in data], 90)) if data else None,
        "slippage_p90_bps": float(cfg["costs"]["crypto"]["slippage_bps_stress"]) if data else None,
    }
    gates = cfg["forward"]
    ready = bool(
        metrics["clean_closed"] >= int(gates["min_clean_closed"])
        and metrics["forward_days"] >= int(gates["min_forward_days"])
        and metrics["net_pnl_usd"] > 0
        and (metrics["profit_factor"] or 0) >= float(gates["min_profit_factor"])
        and metrics["max_drawdown_r"] <= float(gates["max_drawdown_r"])
        and set(metrics["directions"]) == {"long", "short"}
        and (metrics["latency_p90_seconds"] or math.inf) <= float(gates["max_latency_p90_seconds"])
        and (metrics["slippage_p90_bps"] or math.inf) <= float(gates["max_slippage_p90_bps"])
    )
    report = {
        "generated_at": utc_now().isoformat(), "strategy_id": gates["strategy_id"],
        "verdict": "REVIEW_ONLY" if ready else "ACCUMULATING_FORWARD_EVIDENCE",
        "paper_eligible": False, "live_eligible": False, "metrics": metrics,
        "operator_live_override": {
            "enabled": True,
            "route_id": "crypto_invest_regime_conditioned_live_v1",
            "does_not_change_evidence_verdict": True,
        },
    }
    (ARTIFACT_ROOT / "FORWARD_READINESS.json").write_text(stable_json(report) + "\n", encoding="utf-8")
    return report


def _lock() -> Any:
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    handle = LOCK_PATH.open("a+")
    if os.name == "nt":
        import msvcrt
        if handle.tell() == 0:
            handle.write("0")
            handle.flush()
        handle.seek(0)
        try:
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as exc:
            handle.close()
            raise RuntimeError("forward shadow loop is already running") from exc
    return handle


def run_cycle(workers: int, *, bridge_live: bool = True) -> dict[str, Any]:
    scan = scan_once(workers)
    outcomes = refresh_outcomes()
    near_miss_outcomes = near_miss.refresh_outcomes(_recent_closed_bars)
    readiness = readiness_report()
    bridge: dict[str, Any]
    if not bridge_live:
        bridge = {"status": "SKIPPED_NO_LIVE_BRIDGE"}
    else:
        try:
            from src.live_execution.crypto_invest_bridge import capture_forward_decisions
            with connect() as conn:
                rows = [dict(row) for row in conn.execute(
                    "SELECT * FROM forward_decisions WHERE created_at>=?",
                    (scan["observed_at"],),
                ).fetchall()]
            bridge = capture_forward_decisions(rows)
        except Exception as exc:
            bridge = {"status": "ERROR", "error": f"{type(exc).__name__}: {exc}"}
    result = {
        "scan": scan,
        "outcomes": outcomes,
        "near_miss": near_miss_outcomes,
        "readiness": readiness,
        "live_bridge": bridge,
    }
    print(json.dumps(result, indent=2), flush=True)
    return result


def _seconds_until_next_scan(now_epoch: float, *, start_delay_seconds: float = SCAN_START_DELAY_SECONDS,
                             max_decision_latency_seconds: float = 120.0) -> float:
    """Align loop starts with the first safe seconds after each closed 15m bar.

    A monitor restart in the middle of a bar must not manufacture a delayed
    point-in-time decision from a candle that has already aged out.
    """
    current_start = int(now_epoch // QUARTER_SECONDS) * QUARTER_SECONDS + start_delay_seconds
    if now_epoch <= current_start + max_decision_latency_seconds:
        return max(0.0, current_start - now_epoch)
    return (int(now_epoch // QUARTER_SECONDS) + 1) * QUARTER_SECONDS + start_delay_seconds - now_epoch


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--loop", action="store_true")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--no-live-bridge", action="store_true")
    args = parser.parse_args()
    if not args.loop:
        run_cycle(args.workers, bridge_live=not args.no_live_bridge)
        return
    lock = _lock()
    try:
        while True:
            forward_cfg = load_config(LAB_ROOT / "config" / "crypto_v2.yaml")["forward"]
            time.sleep(_seconds_until_next_scan(
                time.time(),
                start_delay_seconds=float(forward_cfg.get("scan_start_delay_seconds", SCAN_START_DELAY_SECONDS)),
                max_decision_latency_seconds=float(forward_cfg.get("max_decision_latency_seconds", 120.0)),
            ))
            try:
                run_cycle(args.workers, bridge_live=not args.no_live_bridge)
            except Exception as exc:
                print(json.dumps({"error": f"{type(exc).__name__}: {exc}"}), flush=True)
    finally:
        lock.close()


if __name__ == "__main__":
    main()
