"""Replay alternative profit targets for the medium-deep fast-flush setup."""
from __future__ import annotations

import json
import math
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

import pandas as pd

from scripts.research_fast_flush_depth_sensitivity import (
    LAB,
    _evaluate,
    _load_rows,
    _params,
)
from scripts.research_fast_flush_reclaim_v3 import _dt, _resample, _summary
from src.data_collectors.fast_flush_research_store import connect, load_frame
from src.execution import crypto_fast_flush_reclaim_paper as strategy


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = LAB / "target_sensitivity_result.json"
REPORT = ROOT / "reports" / "CRYPTO_FAST_FLUSH_TARGET_SENSITIVITY.md"

TRAIN_END = datetime.fromisoformat("2026-09-21T07:30:00+00:00")
VALIDATION_END = datetime.fromisoformat("2026-09-26T13:10:00+00:00")


def _rolling_vwap(frame: pd.DataFrame, entry_at: datetime, hours: int) -> float | None:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    end = pd.Timestamp(entry_at)
    start = end - pd.Timedelta(hours=hours)
    eligible = frame[(timestamps < end) & (timestamps >= start)]
    if eligible.empty:
        return None
    volume = pd.to_numeric(eligible["volume"], errors="coerce").fillna(0.0)
    if float(volume.sum()) <= 0:
        return None
    typical = (
        pd.to_numeric(eligible["high"], errors="coerce")
        + pd.to_numeric(eligible["low"], errors="coerce")
        + pd.to_numeric(eligible["close"], errors="coerce")
    ) / 3.0
    return float((typical * volume).sum() / volume.sum())


def _reconstruct(row: dict[str, Any], archive: Any, cfg: dict[str, Any]) -> dict[str, Any] | None:
    at = row["event_at"]
    start_ms = int((at - timedelta(hours=6)).timestamp() * 1000)
    end_ms = int((at + timedelta(hours=3)).timestamp() * 1000)
    minute, exchange = load_frame(archive, str(row["symbol"]), start_ms, end_ms)
    if minute.empty:
        return None
    base = _resample(minute, "5m")
    indices = base.index[base["timestamp"] == pd.Timestamp(at)].tolist()
    if not indices:
        return None
    idx = int(indices[0])
    if idx < 15:
        return None
    candle = base.iloc[idx]
    prior_close = float(base.iloc[idx - 1]["close"])
    sweep_low = float(candle["low"])
    atr = strategy._atr(base, idx - 1)  # noqa: SLF001
    if atr is None or atr <= 0:
        return None
    decision_at = at + timedelta(minutes=5)
    setup = {
        "decision_at": decision_at,
        "reclaim_level": sweep_low + (prior_close - sweep_low) * float(cfg["reclaim_fraction"]),
        "stop": sweep_low - float(atr) * float(cfg["stop_buffer_atr"]),
    }
    profile = cfg["confirmation_profiles"]["FAST_1M_RECLAIM"]
    confirmation = strategy.detect_confirmation(
        _resample(minute, "1m"), setup, at + timedelta(hours=2), profile,
    )
    if confirmation.get("status") != "entry":
        return None
    entry = float(confirmation["entry"])
    geometry = strategy.entry_geometry(setup, entry, cfg)
    if not geometry.get("ok"):
        return None
    entry_at = confirmation["entry_at"]
    future = minute[minute["timestamp"] >= pd.Timestamp(entry_at)].iloc[: int(profile["max_holding_bars"])]
    if future.empty:
        return None
    risk = float(geometry["risk"])
    return {
        **row,
        "exchange": exchange,
        "entry": entry,
        "entry_at": entry_at,
        "stop": float(geometry["stop"]),
        "risk_distance": risk,
        "prior_close": prior_close,
        "reclaim_level": float(setup["reclaim_level"]),
        "sweep_open": float(candle["open"]),
        "sweep_high": float(candle["high"]),
        "vwap_1h": _rolling_vwap(minute, entry_at, 1),
        "vwap_4h": _rolling_vwap(minute, entry_at, 4),
        "future": future,
    }


def _r_targets(first: float, second: float) -> Callable[[dict[str, Any]], tuple[float, float] | None]:
    def targets(trade: dict[str, Any]) -> tuple[float, float]:
        entry, risk = float(trade["entry"]), float(trade["risk_distance"])
        return entry + first * risk, entry + second * risk
    return targets


def _two_structure_levels(first_key: str, second_key: str) -> Callable[[dict[str, Any]], tuple[float, float] | None]:
    def targets(trade: dict[str, Any]) -> tuple[float, float] | None:
        entry = float(trade["entry"])
        levels = sorted({float(trade[key]) for key in (first_key, second_key)
                         if trade.get(key) is not None and float(trade[key]) > entry})
        if len(levels) < 2 or math.isclose(levels[0], levels[1]):
            return None
        return levels[0], levels[1]
    return targets


def _previous_close_recovery(trade: dict[str, Any]) -> tuple[float, float] | None:
    entry, prior = float(trade["entry"]), float(trade["prior_close"])
    if prior <= entry:
        return None
    return entry + 0.5 * (prior - entry), prior


def _clamp_r(raw_price: float | None, *, entry: float, risk: float,
             minimum: float, maximum: float, fallback: float) -> float:
    raw_r = fallback if raw_price is None or raw_price <= entry else (raw_price - entry) / risk
    return entry + min(max(raw_r, minimum), maximum) * risk


def _hybrid(first_key: str) -> Callable[[dict[str, Any]], tuple[float, float]]:
    def targets(trade: dict[str, Any]) -> tuple[float, float]:
        entry, risk = float(trade["entry"]), float(trade["risk_distance"])
        tp1 = _clamp_r(trade.get(first_key), entry=entry, risk=risk,
                       minimum=0.60, maximum=1.00, fallback=0.80)
        tp2 = _clamp_r(trade.get("prior_close"), entry=entry, risk=risk,
                       minimum=1.10, maximum=1.80, fallback=1.35)
        if tp2 <= tp1:
            tp2 = entry + min(1.80, max(1.10, (tp1 - entry) / risk + 0.20)) * risk
        return tp1, tp2
    return targets


VARIANTS: dict[str, Callable[[dict[str, Any]], tuple[float, float] | None]] = {
    "BASELINE_R_080_135": _r_targets(0.80, 1.35),
    "TIGHT_R_065_115": _r_targets(0.65, 1.15),
    "EXTENDED_R_100_175": _r_targets(1.00, 1.75),
    "PREVIOUS_CLOSE_RECOVERY": _previous_close_recovery,
    "VWAP1H_THEN_PREVIOUS_CLOSE": _two_structure_levels("vwap_1h", "prior_close"),
    "VWAP4H_THEN_PREVIOUS_CLOSE": _two_structure_levels("vwap_4h", "prior_close"),
    "HYBRID_VWAP1H_CLAMPED": _hybrid("vwap_1h"),
    "HYBRID_VWAP4H_CLAMPED": _hybrid("vwap_4h"),
}


def _part(at: datetime) -> str:
    if at <= TRAIN_END:
        return "train"
    if at <= VALIDATION_END:
        return "validation"
    return "test"


def _simulate(trades: list[dict[str, Any]], cfg: dict[str, Any],
              target_fn: Callable[[dict[str, Any]], tuple[float, float] | None]) -> dict[str, Any]:
    outcomes: list[dict[str, Any]] = []
    target_r_values: list[tuple[float, float]] = []
    unavailable = 0
    for trade in trades:
        targets = target_fn(trade)
        if targets is None:
            unavailable += 1
            continue
        tp1, tp2 = targets
        if tp1 <= float(trade["entry"]) or tp2 <= tp1:
            unavailable += 1
            continue
        risk = float(trade["risk_distance"])
        target_r_values.append(((tp1 - float(trade["entry"])) / risk,
                                (tp2 - float(trade["entry"])) / risk))
        outcome = strategy.simulate_two_target(
            entry=float(trade["entry"]), stop=float(trade["stop"]),
            tp1=tp1, tp2=tp2, candles=trade["future"], symbol=str(trade["symbol"]),
            cfg=cfg, bar_minutes=1, force_close=True,
        )
        outcomes.append({**outcome, "event_at": trade["event_at"], "symbol": trade["symbol"]})
    result: dict[str, Any] = {
        "available": len(outcomes),
        "unavailable": unavailable,
        "target_geometry": {
            "tp1_r_median": round(float(pd.Series([item[0] for item in target_r_values]).median()), 3)
            if target_r_values else None,
            "tp1_r_range": [round(min(item[0] for item in target_r_values), 3),
                            round(max(item[0] for item in target_r_values), 3)] if target_r_values else None,
            "tp2_r_median": round(float(pd.Series([item[1] for item in target_r_values]).median()), 3)
            if target_r_values else None,
            "tp2_r_range": [round(min(item[1] for item in target_r_values), 3),
                            round(max(item[1] for item in target_r_values), 3)] if target_r_values else None,
        },
        "close_reasons": dict(Counter(str(row.get("close_reason")) for row in outcomes)),
    }
    for name in ("train", "validation", "test"):
        result[name] = _summary([row for row in outcomes if _part(row["event_at"]) == name])
    result["all"] = _summary(outcomes)
    return result


def _fmt(summary: dict[str, Any]) -> str:
    return (f"n={summary['trades']}, {summary['net_r']:+.3f}R, PF={summary['pf']}, "
            f"win={summary['winrate']:.1%}, DD=${summary['max_drawdown_usd']:.2f}")


def _write_report(result: dict[str, Any]) -> None:
    lines = [
        "# Crypto Fast Flush - Profit Target Sensitivity",
        "",
        f"- generated: `{result['generated_at']}`",
        f"- medium-deep candidate trades: `{result['candidate_trades']}`",
        f"- reconstructed trades: `{result['reconstructed_trades']}`",
        f"- baseline replay max absolute delta: `{result['baseline_reproduction']['max_abs_net_r_delta']}`",
        "",
        "Entry, structural stop, 70/30 exits, breakeven-after-TP1, 45-minute timeout, fees, "
        "slippage, and stop-first intrabar handling are unchanged. Only TP prices differ.",
        "",
        "A reclaim level below a confirmed long entry is not treated as a target. Strict structural "
        "variants are reported with their availability so missing geometry cannot be hidden.",
        "",
        "| Variant | Coverage | Median TP R | Train | Validation | Latest test | All |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name, block in result["variants"].items():
        lines.append(
            f"| `{name}` | {block['available']}/{result['reconstructed_trades']} | "
            f"{block['target_geometry']['tp1_r_median']}/{block['target_geometry']['tp2_r_median']} | "
            f"{_fmt(block['train'])} | {_fmt(block['validation'])} | "
            f"{_fmt(block['test'])} | {_fmt(block['all'])} |"
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        result["interpretation"],
        "",
        "No production or Paper profile was changed by this research run.",
    ])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run() -> dict[str, Any]:
    rows = _load_rows(LAB / "replay_trades.csv")
    deep = _params(min_atr=2.0, max_atr=5.0, min_pct=1.50, max_pct=2.75)
    selected, _ = _evaluate(rows, deep)
    cfg = strategy.load_strategy_config()
    archive = connect()
    try:
        trades = [trade for row in selected if (trade := _reconstruct(row, archive, cfg)) is not None]
    finally:
        archive.close()

    variants = {name: _simulate(trades, cfg, fn) for name, fn in VARIANTS.items()}
    baseline_deltas = []
    for trade in trades:
        targets = VARIANTS["BASELINE_R_080_135"](trade)
        assert targets is not None
        replay = strategy.simulate_two_target(
            entry=float(trade["entry"]), stop=float(trade["stop"]), tp1=targets[0], tp2=targets[1],
            candles=trade["future"], symbol=str(trade["symbol"]), cfg=cfg, bar_minutes=1, force_close=True,
        )
        baseline_deltas.append(abs(float(replay["net_r"]) - float(trade["net_r"])))

    baseline = variants["BASELINE_R_080_135"]
    viable = {
        name: block for name, block in variants.items()
        if name != "BASELINE_R_080_135" and block["available"] == len(trades)
        and block["train"]["net_r"] > 0 and block["validation"]["net_r"] > 0
    }
    better = [
        name for name, block in viable.items()
        if block["test"]["net_r"] > baseline["test"]["net_r"]
        and block["all"]["net_r"] > baseline["all"]["net_r"]
    ]
    interpretation = (
        "A full-coverage alternative improved both the latest test and the complete sample: "
        + ", ".join(f"`{name}`" for name in better) + ". It should still be verified in a separate Paper lane."
        if better else
        "No full-coverage structural alternative beat the fixed-R baseline in both the latest test "
        "and the complete sample. Keep fixed-R targets until more independent data arrives."
    )
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "candidate_parameters": deep,
        "candidate_trades": len(selected),
        "reconstructed_trades": len(trades),
        "baseline_reproduction": {
            "max_abs_net_r_delta": round(max(baseline_deltas, default=0.0), 8),
            "exact_within_1e_4": all(value <= 0.0001 for value in baseline_deltas),
        },
        "reclaim_level_above_entry": sum(float(row["reclaim_level"]) > float(row["entry"]) for row in trades),
        "variants": variants,
        "interpretation": interpretation,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    _write_report(result)
    return result


def main() -> None:
    print(json.dumps(run(), indent=2, default=str))


if __name__ == "__main__":
    main()
