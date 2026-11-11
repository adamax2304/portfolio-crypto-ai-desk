"""Target sensitivity for the best new crypto and stock liquidity-reclaim profiles.

Research only. Entries, initial stops, confirmation logic, holding periods,
partial exits, costs, and chronological splits stay frozen. Only target prices
change.
"""
from __future__ import annotations

import json
import math
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

import pandas as pd

from scripts.research_fast_flush_depth_sensitivity import _load_rows as load_crypto_rows
from scripts.research_fast_flush_reclaim_v3 import _cascade_adjusted, _filter as crypto_filter
from scripts.research_fast_flush_reclaim_v3 import _resample, _summary as crypto_summary
from scripts.research_stocks_liquidity_shock_reclaim_v1 import (
    _filter as stock_filter,
    _independence_adjusted,
    _summary as stock_summary,
)
from src.data_collectors.fast_flush_research_store import connect as crypto_connect
from src.data_collectors.fast_flush_research_store import load_frame as crypto_load_frame
from src.data_collectors import stocks_liquidity_shock_research_store as stock_archive
from src.execution import crypto_fast_flush_reclaim_paper as crypto_strategy
from src.execution import stocks_liquidity_shock_reclaim_paper as stock_strategy
from src.execution.structural_tp_engine import generate_structural_tps


ROOT = Path(__file__).resolve().parents[1]
CRYPTO_LAB = ROOT / "research_labs" / "fast_flush_reclaim_v3"
STOCK_LAB = ROOT / "research_labs" / "stocks_liquidity_shock_reclaim_v1"
OUTPUT = ROOT / "research" / "LIQUIDITY_SWEEP_BEST_TARGET_SENSITIVITY.json"
REPORT = ROOT / "reports" / "LIQUIDITY_SWEEP_BEST_TARGET_SENSITIVITY.md"

CRYPTO_SPLIT = datetime.fromisoformat("2026-09-24T15:50:00+00:00")
STOCK_SPLIT = datetime.fromisoformat("2026-09-14T15:30:00+00:00")

CRYPTO_PARAMS = {
    "min_flush_atr": 1.25, "max_flush_atr": 3.25,
    "min_flush_pct": 0.75, "max_flush_pct": 2.50,
    "min_rvol": 1.05, "min_oi_drop_pct": 0.50, "max_oi_drop_pct": 3.00,
    "min_liq_percentile": 0.90, "max_spread_bps": 18.0,
    "min_stop_distance_pct": 0.010, "max_stop_distance_pct": 0.015,
    "sessions": ("us",),
}

STOCK_PARAMS = {
    "min_flush_atr": 1.10, "max_flush_atr": 3.50,
    "min_flush_pct": 0.80, "min_rvol": 1.20,
    "min_idiosyncratic_drop_pct": 0.20,
    "max_market_drop_pct": 0.60, "max_sector_drop_pct": 1.10,
    "min_level_breach_atr": 0.15,
}


def _dt(value: Any) -> datetime | None:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    try:
        return pd.Timestamp(value).to_pydatetime().astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def _vwap(frame: pd.DataFrame, start: datetime, end: datetime) -> float | None:
    work = frame[(frame["timestamp"] >= pd.Timestamp(start))
                 & (frame["timestamp"] < pd.Timestamp(end))]
    if work.empty:
        return None
    volume = pd.to_numeric(work["volume"], errors="coerce").fillna(0.0)
    if float(volume.sum()) <= 0:
        return None
    typical = (pd.to_numeric(work["high"], errors="coerce")
               + pd.to_numeric(work["low"], errors="coerce")
               + pd.to_numeric(work["close"], errors="coerce")) / 3.0
    return float((typical * volume).sum() / volume.sum())


def _clamp_target(raw_price: float | None, *, entry: float, risk: float,
                  floor: float, cap: float, fallback: float) -> float:
    raw_r = fallback if raw_price is None or raw_price <= entry else (raw_price - entry) / risk
    return entry + min(max(raw_r, floor), cap) * risk


def _r_targets(first: float, second: float) -> Callable[[dict[str, Any]], tuple[float, float] | None]:
    def targets(trade: dict[str, Any]) -> tuple[float, float]:
        entry, risk = float(trade["entry"]), float(trade["risk"])
        return entry + first * risk, entry + second * risk
    return targets


def _atr_targets(trade: dict[str, Any]) -> tuple[float, float]:
    entry, atr = float(trade["entry"]), float(trade["atr"])
    return entry + atr, entry + 2.0 * atr


def _structural(trade: dict[str, Any]):
    entry, stop = float(trade["entry"]), float(trade["stop"])
    risk = float(trade["risk"])
    return generate_structural_tps(
        entry=entry, stop=stop, direction="long",
        candles=trade["history"].to_dict("records"), atr=float(trade["atr"]),
        market_regime="reversal_reclaim", playbook=str(trade["playbook"]),
        mechanical_tp1=entry + 0.80 * risk,
        mechanical_tp2=entry + 1.35 * risk,
        mechanical_tp3=entry + 2.00 * risk,
    )


def _pure_structure(trade: dict[str, Any]) -> tuple[float, float] | None:
    result = _structural(trade)
    if result.tp1 is None or result.tp2 is None:
        return None
    if result.tp1_source.startswith("atr_") or result.tp2_source.startswith("atr_"):
        return None
    return float(result.tp1), float(result.tp2)


def _bounded_structure(trade: dict[str, Any]) -> tuple[float, float]:
    result = _structural(trade)
    entry, risk = float(trade["entry"]), float(trade["risk"])
    tp1 = _clamp_target(result.tp1, entry=entry, risk=risk,
                        floor=0.60, cap=1.00, fallback=0.80)
    tp2 = _clamp_target(result.tp2, entry=entry, risk=risk,
                        floor=1.10, cap=1.80, fallback=1.35)
    return tp1, tp2


def _bounded_anchor(trade: dict[str, Any]) -> tuple[float, float]:
    entry, risk = float(trade["entry"]), float(trade["risk"])
    tp1 = _clamp_target(trade.get("anchor_vwap"), entry=entry, risk=risk,
                        floor=0.60, cap=1.00, fallback=0.80)
    tp2 = _clamp_target(trade.get("prior_close"), entry=entry, risk=risk,
                        floor=1.10, cap=1.80, fallback=1.35)
    return tp1, tp2


TARGETS: dict[str, Callable[[dict[str, Any]], tuple[float, float] | None]] = {
    "BASELINE_R_080_135": _r_targets(0.80, 1.35),
    "EXTENDED_R_100_175": _r_targets(1.00, 1.75),
    "ATR_1X_2X": _atr_targets,
    "PURE_STRUCTURE": _pure_structure,
    "BOUNDED_STRUCTURE": _bounded_structure,
    "BOUNDED_VWAP_PREVIOUS_CLOSE": _bounded_anchor,
}


def _crypto_reconstruct(row: dict[str, Any], archive: Any,
                        cfg: dict[str, Any]) -> dict[str, Any] | None:
    at = row["event_at"]
    minute, exchange = crypto_load_frame(
        archive, str(row["symbol"]),
        int((at - timedelta(hours=6)).timestamp() * 1000),
        int((at + timedelta(hours=3)).timestamp() * 1000),
    )
    if minute.empty:
        return None
    base = _resample(minute, "5m")
    indices = base.index[base["timestamp"] == pd.Timestamp(at)].tolist()
    if not indices or int(indices[0]) < 15:
        return None
    idx = int(indices[0])
    candle = base.iloc[idx]
    prior_close = float(base.iloc[idx - 1]["close"])
    sweep_low = float(candle["low"])
    atr = crypto_strategy._atr(base, idx - 1)  # noqa: SLF001
    if atr is None or atr <= 0:
        return None
    setup = {
        "decision_at": at + timedelta(minutes=5),
        "reclaim_level": sweep_low + (prior_close - sweep_low) * float(cfg["reclaim_fraction"]),
        "stop": sweep_low - float(atr) * float(cfg["stop_buffer_atr"]),
    }
    profile = cfg["confirmation_profiles"]["FAST_1M_RECLAIM"]
    confirmation = crypto_strategy.detect_confirmation(
        _resample(minute, "1m"), setup, at + timedelta(hours=2), profile,
    )
    if confirmation.get("status") != "entry":
        return None
    geometry = crypto_strategy.entry_geometry(setup, float(confirmation["entry"]), cfg)
    if not geometry.get("ok"):
        return None
    entry_at = confirmation["entry_at"]
    future = minute[minute["timestamp"] >= pd.Timestamp(entry_at)].iloc[
        :int(profile["max_holding_bars"])
    ]
    if future.empty:
        return None
    return {
        **row, "exchange": exchange, "entry_at": entry_at,
        "entry": float(confirmation["entry"]), "stop": float(geometry["stop"]),
        "risk": float(geometry["risk"]), "atr": float(atr),
        "prior_close": prior_close,
        "anchor_vwap": _vwap(minute, entry_at - timedelta(hours=4), entry_at),
        "history": base.iloc[max(0, idx - 100):idx + 1].copy(), "future": future,
        "playbook": "crypto_fast_flush_reclaim_v3",
    }


def _load_stock_rows() -> list[dict[str, Any]]:
    frame = pd.read_csv(STOCK_LAB / "replay_trades.csv")
    for column in ("event_at", "entry_at"):
        frame[column] = pd.to_datetime(frame[column], utc=True)
    rows = frame.to_dict("records")
    for row in rows:
        row["event_at"] = row["event_at"].to_pydatetime()
        row["entry_at"] = row["entry_at"].to_pydatetime()
    return rows


def _stock_reconstruct(row: dict[str, Any], archive: Any,
                       cfg: dict[str, Any]) -> dict[str, Any] | None:
    symbol = str(row["symbol"])
    base = stock_archive.load_frame(archive, symbol, "15m")
    minute = stock_archive.load_frame(archive, symbol, "1m")
    if base.empty or minute.empty:
        return None
    decision_at = row["event_at"]
    shock_at = decision_at - timedelta(minutes=15)
    indices = base.index[base["timestamp"] == pd.Timestamp(shock_at)].tolist()
    if not indices:
        return None
    idx = int(indices[0])
    if idx < max(int(cfg["atr_periods"]), int(cfg["level_lookback_bars"])):
        return None
    candle = base.iloc[idx]
    atr = stock_strategy._atr(base, idx - 1, int(cfg["atr_periods"]))  # noqa: SLF001
    if atr is None or atr <= 0:
        return None
    prior_close = float(base.iloc[idx - 1]["close"])
    sweep_low = float(candle["low"])
    structural_level = float(base.iloc[idx - int(cfg["level_lookback_bars"]):idx]["low"].min())
    setup = {
        "decision_at": decision_at,
        "reclaim_level": max(
            structural_level,
            sweep_low + (prior_close - sweep_low) * float(cfg["reclaim_fraction"]),
        ),
        "stop": sweep_low - float(atr) * float(cfg["stop_buffer_atr"]),
    }
    profile = cfg["confirmation_profiles"]["HELD_1M_RECLAIM"]
    confirmation = stock_strategy.detect_confirmation(
        minute, setup,
        decision_at + timedelta(minutes=int(profile["confirmation_window_bars"])),
        profile,
    )
    if confirmation.get("status") != "entry":
        return None
    geometry = stock_strategy.entry_geometry(setup, float(confirmation["entry"]), cfg)
    if not geometry.get("ok"):
        return None
    entry_at = confirmation["entry_at"]
    event_day = entry_at.astimezone(stock_strategy.NY).date()
    future = minute[minute["timestamp"] >= pd.Timestamp(entry_at)].copy()
    future = future[future["timestamp"].map(
        lambda value: value.to_pydatetime().astimezone(stock_strategy.NY).date() == event_day
    )].iloc[:int(profile["max_holding_bars"])]
    if future.empty:
        return None
    market_open = datetime.combine(
        event_day, datetime.min.time(), tzinfo=stock_strategy.NY,
    ).replace(hour=9, minute=30).astimezone(timezone.utc)
    return {
        **row, "entry_at": entry_at, "entry": float(confirmation["entry"]),
        "stop": float(geometry["stop"]), "risk": float(geometry["risk"]),
        "atr": float(atr), "prior_close": prior_close,
        "anchor_vwap": _vwap(minute, market_open, entry_at),
        "history": base.iloc[max(0, idx - 100):idx + 1].copy(), "future": future,
        "playbook": "stocks_liquidity_shock_reclaim_v1",
    }


def _simulate(trades: list[dict[str, Any]], *, mode: str,
              target_fn: Callable[[dict[str, Any]], tuple[float, float] | None],
              cfg: dict[str, Any], split_at: datetime) -> dict[str, Any]:
    outcomes: list[dict[str, Any]] = []
    target_r: list[tuple[float, float]] = []
    unavailable = 0
    for trade in trades:
        targets = target_fn(trade)
        if targets is None:
            unavailable += 1
            continue
        tp1, tp2 = map(float, targets)
        entry, risk = float(trade["entry"]), float(trade["risk"])
        if tp1 <= entry or tp2 <= tp1:
            unavailable += 1
            continue
        target_r.append(((tp1 - entry) / risk, (tp2 - entry) / risk))
        if mode == "crypto":
            result = crypto_strategy.simulate_two_target(
                entry=entry, stop=float(trade["stop"]), tp1=tp1, tp2=tp2,
                candles=trade["future"], symbol=str(trade["symbol"]), cfg=cfg,
                bar_minutes=1, force_close=True,
            )
        else:
            result = stock_strategy.simulate_two_target(
                entry=entry, stop=float(trade["stop"]), tp1=tp1, tp2=tp2,
                candles=trade["future"], symbol=str(trade["symbol"]), cfg=cfg,
                force_close=True,
            )
        outcomes.append({
            **result,
            "event_at": trade["event_at"],
            "entry_at": trade["entry_at"],
            "symbol": trade["symbol"],
        })
    summary_fn = crypto_summary if mode == "crypto" else stock_summary
    return {
        "available": len(outcomes), "unavailable": unavailable,
        "median_target_r": [
            round(float(pd.Series([item[index] for item in target_r]).median()), 3)
            if target_r else None for index in range(2)
        ],
        "close_reasons": dict(Counter(str(row.get("close_reason")) for row in outcomes)),
        "train": summary_fn([row for row in outcomes if row["event_at"] <= split_at]),
        "holdout": summary_fn([row for row in outcomes if row["event_at"] > split_at]),
        "all": summary_fn(outcomes),
    }


def _baseline_delta(trades: list[dict[str, Any]], *, mode: str,
                    cfg: dict[str, Any]) -> dict[str, Any]:
    deltas = []
    for trade in trades:
        targets = TARGETS["BASELINE_R_080_135"](trade)
        assert targets is not None
        tp1, tp2 = targets
        if mode == "crypto":
            result = crypto_strategy.simulate_two_target(
                entry=float(trade["entry"]), stop=float(trade["stop"]),
                tp1=float(tp1), tp2=float(tp2), candles=trade["future"],
                symbol=str(trade["symbol"]), cfg=cfg, bar_minutes=1,
                force_close=True,
            )
        else:
            result = stock_strategy.simulate_two_target(
                entry=float(trade["entry"]), stop=float(trade["stop"]),
                tp1=float(tp1), tp2=float(tp2), candles=trade["future"],
                symbol=str(trade["symbol"]), cfg=cfg, force_close=True,
            )
        deltas.append(abs(float(result["net_r"]) - float(trade["net_r"])))
    return {
        "max_abs_net_r_delta": round(max(deltas, default=0.0), 8),
        "exact_within_1e_4": all(value <= 0.0001 for value in deltas),
    }


def _fmt(block: dict[str, Any]) -> str:
    return (f"n={block['trades']}, {block['net_r']:+.3f}R, PF={block['pf']}, "
            f"win={block['winrate']:.1%}, DD=${block['max_drawdown_usd']:.2f}")


def _write_report(result: dict[str, Any]) -> None:
    lines = [
        "# Best New Liquidity-Reclaim Profiles - Target Sensitivity", "",
        f"Generated: `{result['generated_at']}`", "",
        "Only the best new liquidity-reclaim profile in each asset class is tested. Entries, "
        "initial structural stops, confirmation, 70/30 exits, breakeven after TP1, holding time, "
        "fees, slippage, stop-first ambiguity handling, and the original chronological split are frozen.",
    ]
    for mode, block in result["modes"].items():
        lines.extend([
            "", f"## {mode}", "",
            f"Selected/reconstructed: `{block['selected_trades']}/{block['reconstructed_trades']}`; "
            f"baseline max delta `{block['baseline_reproduction']['max_abs_net_r_delta']}`.", "",
            "| Target policy | Coverage | Median TP R | Train | Holdout | All |",
            "|---|---:|---:|---:|---:|---:|",
        ])
        for name, variant in block["variants"].items():
            lines.append(
                f"| `{name}` | {variant['available']}/{block['reconstructed_trades']} | "
                f"`{variant['median_target_r']}` | {_fmt(variant['train'])} | "
                f"{_fmt(variant['holdout'])} | {_fmt(variant['all'])} |"
            )
    lines.extend([
        "", "## Boundary", "",
        "This is post-hoc target sensitivity on previously inspected history, not a fresh holdout. "
        "A winning alternative must receive a separate Paper profile before any promotion decision.",
    ])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run() -> dict[str, Any]:
    crypto_cfg = crypto_strategy.load_strategy_config()
    crypto_rows = load_crypto_rows(CRYPTO_LAB / "replay_trades.csv")
    crypto_selected = _cascade_adjusted(crypto_filter(
        crypto_rows, CRYPTO_PARAMS, "FAST_1M_RECLAIM",
    ))
    crypto_db = crypto_connect()
    try:
        crypto_trades = [trade for row in crypto_selected
                         if (trade := _crypto_reconstruct(row, crypto_db, crypto_cfg)) is not None]
    finally:
        crypto_db.close()

    stock_cfg = stock_strategy.load_strategy_config()
    stock_rows = _load_stock_rows()
    stock_selected = _independence_adjusted(stock_filter(
        stock_rows, STOCK_PARAMS, "HELD_1M_RECLAIM",
    ))
    stock_db = stock_archive.connect()
    try:
        stock_trades = [trade for row in stock_selected
                        if (trade := _stock_reconstruct(row, stock_db, stock_cfg)) is not None]
    finally:
        stock_db.close()

    modes = {}
    for name, trades, cfg, split, mode in (
        ("crypto_FAST_1M_RECLAIM", crypto_trades, crypto_cfg, CRYPTO_SPLIT, "crypto"),
        ("stocks_HELD_1M_RECLAIM", stock_trades, stock_cfg, STOCK_SPLIT, "stocks"),
    ):
        variants = {
            target_name: _simulate(trades, mode=mode, target_fn=target_fn,
                                   cfg=cfg, split_at=split)
            for target_name, target_fn in TARGETS.items()
        }
        modes[name] = {
            "selected_trades": len(crypto_selected if mode == "crypto" else stock_selected),
            "reconstructed_trades": len(trades),
            "baseline_reproduction": _baseline_delta(trades, mode=mode, cfg=cfg),
            "variants": variants,
        }
    result = {"generated_at": datetime.now(timezone.utc).isoformat(), "modes": modes}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    _write_report(result)
    return result


def main() -> None:
    print(json.dumps(run(), indent=2, default=str))


if __name__ == "__main__":
    main()
