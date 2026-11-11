"""Paired target-policy replay for the best identified stock and crypto modes.

This is research-only. It preserves each recorded entry and initial stop, then
replays identical candles under current, fixed-R, ATR, structural, and bounded
hybrid target policies. No Paper or Live route is changed.
"""
from __future__ import annotations

import json
import math
import sqlite3
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from scripts.research_fast_flush_reclaim_v3 import _resample
from src.config import load_config
from src.data_collectors.fast_flush_research_store import connect as archive_connect
from src.data_collectors.fast_flush_research_store import load_frame as archive_load_frame
from src.execution.fees import trade_costs
from src.execution.structural_tp_engine import generate_structural_tps
from src.storage.file_store import FileStore


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "db" / "crypto_ai_desk.sqlite"
OUTPUT = ROOT / "research" / "best_modes_target_sensitivity.json"
REPORT = ROOT / "reports" / "BEST_MODES_TARGET_SENSITIVITY.md"
PARTIALS = (0.33, 0.33, 0.34)


def _dt(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def _atr(frame: pd.DataFrame, at: datetime, periods: int = 14) -> float | None:
    work = frame[frame["timestamp"] < pd.Timestamp(at)].tail(periods + 1)
    if len(work) < periods:
        return None
    previous = work["close"].shift(1)
    tr = pd.concat([
        work["high"] - work["low"],
        (work["high"] - previous).abs(),
        (work["low"] - previous).abs(),
    ], axis=1).max(axis=1).dropna().tail(periods)
    return float(tr.mean()) if len(tr) == periods else None


def _favorable_price(entry: float, risk: float, direction: str, multiple: float) -> float:
    return entry + risk * multiple if direction == "long" else entry - risk * multiple


def _target_r(price: float | None, entry: float, risk: float, direction: str) -> float | None:
    if price is None:
        return None
    return ((price - entry) if direction == "long" else (entry - price)) / risk


def _valid_targets(prices: list[float | None], entry: float, direction: str) -> list[float | None]:
    result: list[float | None] = []
    last_r = 0.0
    risk_unit = 1.0
    for price in prices[:3]:
        if price is None:
            result.append(None)
            continue
        favorable = price > entry if direction == "long" else price < entry
        distance = abs(price - entry) / risk_unit
        if not favorable or distance <= last_r:
            result.append(None)
            continue
        result.append(float(price))
        last_r = distance
    return result + [None] * (3 - len(result))


def _target_sets(trade: dict[str, Any]) -> dict[str, list[float | None]]:
    entry, stop = float(trade["entry"]), float(trade["stop"])
    direction = str(trade["direction"]).lower()
    risk = abs(entry - stop)
    atr = float(trade["atr"])
    fixed = [_favorable_price(entry, risk, direction, value) for value in (1.0, 2.0, 3.0)]
    atr_ladder = [_favorable_price(entry, atr, direction, value) for value in (1.0, 2.0, 3.0)]
    current = [trade.get("tp1"), trade.get("tp2"), trade.get("tp3")]

    structural = generate_structural_tps(
        entry=entry, stop=stop, direction=direction,
        candles=trade["history"].to_dict("records"), atr=atr,
        market_regime=trade.get("market_regime"), playbook=trade.get("playbook"),
        mechanical_tp1=fixed[0], mechanical_tp2=fixed[1], mechanical_tp3=fixed[2],
    )
    raw_r = [structural.tp1_r, structural.tp2_r, structural.tp3_r]
    bounds = ((0.75, 1.25, 1.0), (1.50, 2.50, 2.0), (2.50, 4.00, 3.0))
    hybrid_r = []
    for value, (floor, cap, fallback) in zip(raw_r, bounds):
        candidate = fallback if value is None else float(value)
        hybrid_r.append(min(max(candidate, floor), cap))
    hybrid = [_favorable_price(entry, risk, direction, value) for value in hybrid_r]
    return {
        "CURRENT_STORED": _valid_targets(current, entry, direction),
        "FIXED_R_1_2_3": fixed,
        "ATR_1X_2X_3X": atr_ladder,
        "STRUCTURE_ENGINE": _valid_targets([structural.tp1, structural.tp2, structural.tp3], entry, direction),
        "HYBRID_STRUCTURE_BOUNDED": hybrid,
    }


def _simulate(trade: dict[str, Any], targets: list[float | None]) -> dict[str, Any]:
    entry, stop = float(trade["entry"]), float(trade["stop"])
    direction = str(trade["direction"]).lower()
    long = direction == "long"
    risk = abs(entry - stop)
    remaining, gross_r = 1.0, 0.0
    active_stop = stop
    filled = [False, False, False]
    exit_slices: list[tuple[float, str, float]] = []
    reason = "time_exit"
    last_price = entry
    candles = trade["future"]
    for position, (_, candle) in enumerate(candles.iterrows()):
        high, low, close = (float(candle[key]) for key in ("high", "low", "close"))
        last_price = close
        stop_hit = low <= active_stop if long else high >= active_stop
        if stop_hit:
            stop_r = _target_r(active_stop, entry, risk, direction) or 0.0
            gross_r += remaining * stop_r
            exit_slices.append((remaining, "taker", active_stop))
            remaining = 0.0
            reason = "stop"
            break
        # Do not credit a favorable move on the partially elapsed entry bar.
        if position == 0 and trade.get("entry_inside_first_bar", True):
            continue
        for index, target in enumerate(targets):
            if target is None or filled[index]:
                continue
            hit = high >= target if long else low <= target
            if not hit:
                continue
            fraction = min(PARTIALS[index], remaining)
            multiple = _target_r(target, entry, risk, direction) or 0.0
            gross_r += fraction * multiple
            remaining -= fraction
            filled[index] = True
            exit_slices.append((fraction, "maker", float(target)))
            if index == 0:
                active_stop = entry
            elif index == 1:
                active_stop = _favorable_price(entry, risk, direction, 0.50)
        if remaining <= 1e-9:
            reason = "tp3"
            break
    if remaining > 1e-9:
        final_r = _target_r(last_price, entry, risk, direction) or 0.0
        gross_r += remaining * final_r
        exit_slices.append((remaining, "taker", last_price))
    risk_usd = 10.0
    qty = risk_usd / risk
    weighted_exit = sum(fraction * price for fraction, _, price in exit_slices)
    costs = trade_costs(
        notional_usdt=qty * entry, exit_notional_usdt=qty * weighted_exit,
        symbol=str(trade["symbol"]), fee_profile=str(trade["fee_profile"]),
        entry_order_type="taker", exit_order_type="taker",
        exit_slices=[(fraction, order_type) for fraction, order_type, _ in exit_slices],
    )
    return {
        "event_at": trade["entry_at"], "symbol": trade["symbol"],
        "net_r": gross_r - costs.total_cost_usdt / risk_usd,
        "net_pnl_usd": gross_r * risk_usd - costs.total_cost_usdt,
        "fees_usd": costs.fee_usdt, "slippage_usd": costs.slippage_usdt,
        "close_reason": reason, "targets_hit": sum(filled),
    }


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    ordered = sorted(rows, key=lambda row: row["event_at"])
    values = [float(row["net_r"]) for row in ordered]
    wins = sum(value for value in values if value > 0)
    losses = -sum(value for value in values if value < 0)
    equity = peak = drawdown = 0.0
    for value in values:
        equity += value
        peak = max(peak, equity)
        drawdown = max(drawdown, peak - equity)
    return {
        "trades": len(rows), "net_r": round(sum(values), 3),
        "pf": round(wins / losses, 3) if losses else None,
        "winrate": round(sum(value > 0 for value in values) / len(values), 3) if values else 0.0,
        "max_drawdown_r": round(drawdown, 3),
        "costs_usd": round(sum(float(row["fees_usd"]) + float(row["slippage_usd"]) for row in rows), 2),
        "close_reasons": dict(Counter(str(row["close_reason"]) for row in rows)),
    }


def _split_results(rows: list[dict[str, Any]]) -> dict[str, Any]:
    times = sorted(row["event_at"] for row in rows)
    train_cut = times[max(0, int(len(times) * 0.60) - 1)]
    validation_cut = times[max(0, int(len(times) * 0.80) - 1)]
    return {
        "split": {"train_end": train_cut.isoformat(), "validation_end": validation_cut.isoformat()},
        "train": _summary([row for row in rows if row["event_at"] <= train_cut]),
        "validation": _summary([row for row in rows if train_cut < row["event_at"] <= validation_cut]),
        "test": _summary([row for row in rows if row["event_at"] > validation_cut]),
        "all": _summary(rows),
    }


def _stock_rows(conn: sqlite3.Connection, store: FileStore) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    sql = """
    SELECT o.signal_id,o.symbol,o.side,o.entry_price,o.stop_initial,o.tp1,o.tp2,o.tp3,
           o.stop_plan,o.entry_fill_time,s.market_regime,o.playbook
      FROM paper_shadow_execution_outcomes o
      JOIN proposed_signals s ON s.signal_id=o.signal_id
     WHERE o.asset_class='stocks' AND o.branch='new_logic_shadow'
       AND o.entry_mode='BREAKOUT_CONTINUATION' AND o.is_clean_for_edge=1
       AND LOWER(o.outcome_status)='closed'
     ORDER BY o.entry_fill_time
    """
    rows, missing = [], []
    for raw in conn.execute(sql):
        row = dict(raw)
        at = _dt(row["entry_fill_time"])
        frame = store.load_stocks_ohlcv(str(row["symbol"]), "15m")
        if at is None or frame is None or frame.empty:
            missing.append(row["signal_id"])
            continue
        frame = frame.sort_values("timestamp")
        history = frame[frame["timestamp"] < pd.Timestamp(at)].tail(100)
        future = frame[(frame["timestamp"] <= pd.Timestamp(at.replace(hour=20, minute=0, second=0))) &
                       (frame["timestamp"] + pd.Timedelta(minutes=15) > pd.Timestamp(at))]
        atr = _atr(frame, at)
        if len(history) < 20 or future.empty or atr is None:
            missing.append(row["signal_id"])
            continue
        rows.append({
            "signal_id": row["signal_id"], "symbol": row["symbol"],
            "direction": str(row["side"]).lower(), "entry": float(row["entry_price"]),
            "stop": float(row["stop_initial"]), "tp1": row["tp1"], "tp2": row["tp2"], "tp3": row["tp3"],
            "entry_at": at, "history": history, "future": future, "atr": atr,
            "market_regime": row["market_regime"], "playbook": row["playbook"],
            "fee_profile": "stock_etf_default", "entry_inside_first_bar": True,
        })
    return rows, {"source_rows": len(rows) + len(missing), "missing_market_path": len(missing)}


def _crypto_rows(
    conn: sqlite3.Connection,
    archive: sqlite3.Connection,
    store: FileStore,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    sql = """
    SELECT s.signal_id,s.symbol,s.direction,s.market_regime,s.setup_type,s.expires_at,
           o.entry_at,o.entry_price_used,o.stop_initial,
           COALESCE(t.active_paper_tp1,s.tp1) tp1,
           COALESCE(t.active_paper_tp2,s.tp2) tp2,
           COALESCE(t.active_paper_tp3,s.tp3) tp3
      FROM paper_execution_outcomes o
      JOIN proposed_signals s ON s.signal_id=o.signal_id
 LEFT JOIN signal_paper_tp t ON t.signal_id=o.signal_id
     WHERE o.paper_entry_profile='crypto_intraday_breakout_paper_v1'
       AND o.paper_execution_entry_mode='BREAKOUT_CONTINUATION'
       AND o.lifecycle_state='CLOSED' AND o.evidence_class='forward_postfreeze'
       AND o.execution_validity='valid' AND o.entry_at>='2026-09-07'
     ORDER BY o.entry_at
    """
    rows, missing = [], []
    cache: dict[tuple[str, str, str], pd.DataFrame | None] = {}
    source_counts: Counter[str] = Counter()
    for raw in conn.execute(sql):
        row = dict(raw)
        at, expires = _dt(row["entry_at"]), _dt(row["expires_at"])
        if at is None:
            missing.append(row["signal_id"])
            continue
        end = min(expires or at + timedelta(hours=24), at + timedelta(hours=24))
        archived, archive_exchange = archive_load_frame(
            archive, str(row["symbol"]),
            int((at - timedelta(hours=24)).timestamp() * 1000), int(end.timestamp() * 1000),
        )
        candidates: list[tuple[int, pd.DataFrame, str, str, int]] = []
        if not archived.empty:
            candidates.append((1, archived, str(archive_exchange or "archive"), "research_archive_1m", 1))
        for timeframe, minutes in (("1m", 1), ("5m", 5)):
            for exchange in ("binance", "mexc", "bybit"):
                key = (exchange, str(row["symbol"]), timeframe)
                if key not in cache:
                    cache[key] = store.load_ohlcv(*key)
                cached = cache[key]
                if cached is None or cached.empty:
                    continue
                window = cached[
                    (cached["timestamp"] >= pd.Timestamp(at - timedelta(hours=24))) &
                    (cached["timestamp"] < pd.Timestamp(end))
                ]
                if not window.empty:
                    candidates.append((minutes, window, exchange, f"rolling_cache_{timeframe}", minutes))

        selected = None
        for _, candidate, exchange, source, minutes in candidates:
            fifteen = _resample(candidate, "15m")
            history = fifteen[fifteen["timestamp"] < pd.Timestamp(at)].tail(100)
            future = candidate[
                (candidate["timestamp"] + pd.Timedelta(minutes=minutes) > pd.Timestamp(at)) &
                (candidate["timestamp"] < pd.Timestamp(end))
            ]
            atr = _atr(fifteen, at)
            if len(history) < 20 or future.empty or atr is None:
                continue
            score = len(history) * 10_000 + len(future)
            if selected is None or score > selected[0]:
                selected = (score, history, future, atr, exchange, source)
        if selected is None:
            missing.append(row["signal_id"])
            continue
        _, history, future, atr, exchange, source = selected
        source_counts[source] += 1
        rows.append({
            "signal_id": row["signal_id"], "symbol": row["symbol"],
            "direction": str(row["direction"]).lower(), "entry": float(row["entry_price_used"]),
            "stop": float(row["stop_initial"]), "tp1": row["tp1"], "tp2": row["tp2"], "tp3": row["tp3"],
            "entry_at": at, "history": history, "future": future, "atr": atr,
            "market_regime": row["market_regime"], "playbook": row["setup_type"],
            "fee_profile": "bybit_non_vip_usdt_perp", "exchange": exchange,
            "entry_inside_first_bar": True,
        })
    return rows, {
        "source_rows": len(rows) + len(missing),
        "missing_market_path": len(missing),
        "path_sources": dict(source_counts),
    }


def _evaluate_mode(trades: list[dict[str, Any]], coverage: dict[str, Any]) -> dict[str, Any]:
    outcomes: dict[str, list[dict[str, Any]]] = {name: [] for name in (
        "CURRENT_STORED", "FIXED_R_1_2_3", "ATR_1X_2X_3X",
        "STRUCTURE_ENGINE", "HYBRID_STRUCTURE_BOUNDED",
    )}
    target_geometry: dict[str, list[list[float | None]]] = {name: [] for name in outcomes}
    for trade in trades:
        sets = _target_sets(trade)
        for name, targets in sets.items():
            outcomes[name].append(_simulate(trade, targets))
            target_geometry[name].append([
                None if target is None else round(float(_target_r(
                    target, float(trade["entry"]), abs(float(trade["entry"]) - float(trade["stop"])),
                    str(trade["direction"]),
                ) or 0.0), 3)
                for target in targets
            ])
    result = {"coverage": {**coverage, "replayed": len(trades)}, "variants": {}}
    for name, rows in outcomes.items():
        block = _split_results(rows)
        block["median_target_r"] = [
            round(float(pd.Series([value[index] for value in target_geometry[name]
                                   if value[index] is not None]).median()), 3)
            if any(value[index] is not None for value in target_geometry[name]) else None
            for index in range(3)
        ]
        result["variants"][name] = block
    return result


def _fmt(summary: dict[str, Any]) -> str:
    return (f"n={summary['trades']}, {summary['net_r']:+.2f}R, PF={summary['pf']}, "
            f"win={summary['winrate']:.1%}, DD={summary['max_drawdown_r']:.2f}R")


def _write_report(result: dict[str, Any]) -> None:
    lines = [
        "# Best Existing Modes - Target Sensitivity",
        "",
        f"Generated: `{result['generated_at']}`",
        "",
        "Research only. Recorded entries and initial stops are frozen. Every variant uses the same "
        "33/33/34 exits, stop-first candles, breakeven after TP1, +0.5R lock after TP2, time exit, "
        "fees, and slippage. The test therefore isolates target placement.",
    ]
    for mode, block in result["modes"].items():
        coverage = block["coverage"]
        lines.extend([
            "", f"## {mode}", "",
            f"Coverage: `{coverage['replayed']}/{coverage['source_rows']}` paths; "
            f"missing `{coverage['missing_market_path']}`.", "",
            "| Variant | Median target R | Train | Validation | Latest test | All |",
            "|---|---:|---:|---:|---:|---:|",
        ])
        for name, variant in block["variants"].items():
            lines.append(
                f"| `{name}` | `{variant['median_target_r']}` | {_fmt(variant['train'])} | "
                f"{_fmt(variant['validation'])} | {_fmt(variant['test'])} | {_fmt(variant['all'])} |"
            )
    lines.extend([
        "", "## Constraint", "",
        "These are local-path replays, not a new untouched market sample. Missing paths are disclosed "
        "and no result is promoted automatically. Forward Paper A/B remains the final check.",
    ])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run() -> dict[str, Any]:
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    archive = archive_connect()
    store = FileStore(load_config())
    try:
        stocks, stocks_coverage = _stock_rows(conn, store)
        crypto, crypto_coverage = _crypto_rows(conn, archive, store)
    finally:
        archive.close()
        conn.close()
    if len(stocks) < 20:
        raise RuntimeError(f"insufficient stock paths: {len(stocks)}")
    if len(crypto) < 10:
        raise RuntimeError(f"insufficient crypto paths: {len(crypto)}")
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "modes": {
            "stocks_intraday_BREAKOUT_CONTINUATION_new_logic_shadow": _evaluate_mode(stocks, stocks_coverage),
            "crypto_intraday_BREAKOUT_CONTINUATION_paper_v1": _evaluate_mode(crypto, crypto_coverage),
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    _write_report(result)
    return result


def main() -> None:
    print(json.dumps(run(), indent=2, default=str))


if __name__ == "__main__":
    main()
