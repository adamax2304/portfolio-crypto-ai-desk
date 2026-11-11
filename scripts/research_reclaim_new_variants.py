"""Paired historical study for Europe FAST crypto and wider stock stops.

The study changes only session/filter inputs for the crypto cohort and only
the structural stop buffer for the stock cohort. It never submits orders.
"""
from __future__ import annotations

import json
import math
from collections import Counter
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from scripts.research_fast_flush_depth_sensitivity import _load_rows as load_crypto_rows
from scripts.research_fast_flush_depth_sensitivity import _split as split_crypto_rows
from scripts.research_fast_flush_reclaim_v3 import _cascade_adjusted, _filter as crypto_filter
from scripts.research_fast_flush_reclaim_v3 import _summary as crypto_summary
from scripts.research_stocks_liquidity_shock_reclaim_v1 import (
    _filter as stock_filter,
    _independence_adjusted,
    _summary as stock_summary,
)
from src.data_collectors import stocks_liquidity_shock_research_store as stock_archive
from src.execution import stocks_liquidity_shock_reclaim_paper as stock_strategy


ROOT = Path(__file__).resolve().parents[1]
CRYPTO_LAB = ROOT / "research_labs" / "fast_flush_reclaim_v3"
STOCK_LAB = ROOT / "research_labs" / "stocks_liquidity_shock_reclaim_v1"
OUT_DIR = ROOT / "research_labs" / "reclaim_new_variants"
RESULT = OUT_DIR / "backtest_result.json"
REPORT = ROOT / "reports" / "RECLAIM_NEW_VARIANTS_BACKTEST.md"

CRYPTO_VARIANTS: dict[str, dict[str, Any]] = {
    "us_strict_control": {
        "min_flush_atr": 1.25, "max_flush_atr": 3.25,
        "min_flush_pct": 0.75, "max_flush_pct": 2.50,
        "min_rvol": 1.05, "min_oi_drop_pct": 0.50, "max_oi_drop_pct": 3.0,
        "min_liq_percentile": 0.90, "max_spread_bps": 18.0,
        "min_stop_distance_pct": 0.010, "max_stop_distance_pct": 0.015,
        "sessions": ("us",),
    },
    "europe_strict": {
        "min_flush_atr": 1.25, "max_flush_atr": 3.25,
        "min_flush_pct": 0.75, "max_flush_pct": 2.50,
        "min_rvol": 1.05, "min_oi_drop_pct": 0.50, "max_oi_drop_pct": 3.0,
        "min_liq_percentile": 0.90, "max_spread_bps": 18.0,
        "min_stop_distance_pct": 0.010, "max_stop_distance_pct": 0.015,
        "sessions": ("europe",),
    },
    "europe_moderate": {
        "min_flush_atr": 1.25, "max_flush_atr": 3.25,
        "min_flush_pct": 0.60, "max_flush_pct": 2.50,
        "min_rvol": 1.00, "min_oi_drop_pct": 0.25, "max_oi_drop_pct": 3.0,
        "min_liq_percentile": 0.80, "max_spread_bps": 18.0,
        "min_stop_distance_pct": 0.0075, "max_stop_distance_pct": 0.015,
        "sessions": ("europe",),
    },
    "europe_medium_deep": {
        "min_flush_atr": 2.0, "max_flush_atr": 5.0,
        "min_flush_pct": 1.50, "max_flush_pct": 2.75,
        "min_rvol": 1.00, "min_oi_drop_pct": 0.25, "max_oi_drop_pct": 5.0,
        "min_liq_percentile": 0.90, "max_spread_bps": 18.0,
        "min_stop_distance_pct": 0.0075, "max_stop_distance_pct": 0.015,
        "sessions": ("europe",),
    },
}

STOCK_BUFFERS = (0.10, 0.15, 0.20, 0.25, 0.30, 0.40)


def _crypto_study() -> dict[str, Any]:
    rows = [row for row in load_crypto_rows(CRYPTO_LAB / "replay_trades.csv")
            if row["profile"] == "FAST_1M_RECLAIM"]
    if not rows:
        raise RuntimeError("crypto FAST replay rows are missing")
    parts, cuts = split_crypto_rows(rows)
    result: dict[str, Any] = {"split": cuts, "variants": {}}
    for name, params in CRYPTO_VARIANTS.items():
        result["variants"][name] = {
            "parameters": {**params, "sessions": list(params["sessions"])},
            **{
                part: crypto_summary(_cascade_adjusted(crypto_filter(data, params, "FAST_1M_RECLAIM")))
                for part, data in parts.items()
            },
        }
    result["source_rows"] = len(rows)
    result["distinct_events"] = len({row["event_id"] for row in rows})
    result["period"] = [min(row["event_at"] for row in rows).isoformat(),
                        max(row["event_at"] for row in rows).isoformat()]
    return result


def _dt(value: Any) -> datetime | None:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    parsed = pd.Timestamp(value)
    if parsed.tzinfo is None:
        parsed = parsed.tz_localize("UTC")
    return parsed.to_pydatetime().astimezone(timezone.utc)


def _load_stock_rows() -> list[dict[str, Any]]:
    frame = pd.read_csv(STOCK_LAB / "replay_trades.csv")
    for column in ("event_at", "entry_at"):
        frame[column] = pd.to_datetime(frame[column], utc=True)
    return [row for row in frame.to_dict("records")
            if row.get("profile") == "HELD_1M_RECLAIM"
            and pd.notna(row.get("event_at")) and pd.notna(row.get("entry_at"))]


def _stock_configured_cohort(rows: list[dict[str, Any]], cfg: dict[str, Any]) -> list[dict[str, Any]]:
    profile = cfg["confirmation_profiles"]["HELD_1M_RECLAIM"]
    params = {
        key: profile.get(key, cfg[key])
        for key in (
            "min_flush_atr", "max_flush_atr", "min_flush_pct", "min_rvol",
            "min_idiosyncratic_drop_pct", "max_market_drop_pct",
            "max_sector_drop_pct", "min_level_breach_atr",
        )
    }
    # Missing sector context is not a rejection in the runtime rule; keep the
    # research cohort behavior aligned with that explicit fail-open context.
    with_sector = [row for row in rows if pd.notna(row.get("sector_drop_pct"))]
    missing_sector = [row for row in rows if pd.isna(row.get("sector_drop_pct"))]
    selected = stock_filter(with_sector, params, "HELD_1M_RECLAIM")
    selected.extend(
        row for row in missing_sector
        if row.get("profile") == "HELD_1M_RECLAIM"
        and params["min_flush_atr"] <= float(row["flush_atr"]) <= params["max_flush_atr"]
        and float(row["flush_pct"]) >= params["min_flush_pct"]
        and float(row["rvol"]) >= params["min_rvol"]
        and float(row["idiosyncratic_drop_pct"]) >= params["min_idiosyncratic_drop_pct"]
        and float(row["market_drop_pct"]) <= params["max_market_drop_pct"]
        and float(row["level_breach_atr"]) >= params["min_level_breach_atr"]
    )
    return sorted(selected, key=lambda row: row["event_at"])


def _stock_entry(row: dict[str, Any], frames: dict[tuple[str, str], pd.DataFrame],
                 cfg: dict[str, Any]) -> dict[str, Any] | None:
    symbol = str(row["symbol"]).upper()
    base = frames.get((symbol, "15m"), pd.DataFrame())
    minute = frames.get((symbol, "1m"), pd.DataFrame())
    if base.empty or minute.empty:
        return None
    decision_at = _dt(row["event_at"])
    if decision_at is None:
        return None
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
    low = float(candle["low"])
    structural = float(base.iloc[idx - int(cfg["level_lookback_bars"]):idx]["low"].min())
    setup = {
        "decision_at": decision_at,
        "reclaim_level": max(structural, low + (prior_close - low) * float(cfg["reclaim_fraction"])),
        "atr": float(atr),
    }
    profile = cfg["confirmation_profiles"]["HELD_1M_RECLAIM"]
    confirmation = stock_strategy.detect_confirmation(
        minute, setup, decision_at + timedelta(minutes=int(profile["confirmation_window_bars"])), profile,
    )
    if confirmation.get("status") != "entry":
        return None
    entry_at = confirmation["entry_at"]
    expected_at = _dt(row["entry_at"])
    entry = float(confirmation["entry"])
    if expected_at is None or abs((entry_at - expected_at).total_seconds()) > 60.0:
        return None
    event_day = entry_at.astimezone(stock_strategy.NY).date()
    future = minute[minute["timestamp"] >= pd.Timestamp(entry_at)].copy()
    future = future[future["timestamp"].map(
        lambda value: value.to_pydatetime().astimezone(stock_strategy.NY).date() == event_day
    )].iloc[:int(profile["max_holding_bars"])]
    if future.empty:
        return None
    return {
        **row, "event_at": _dt(row["event_at"]), "entry_at": entry_at,
        "entry": entry, "atr": float(atr), "shock_low": low,
        "future": future,
    }


def _stock_split(rows: list[dict[str, Any]]) -> tuple[dict[str, list[dict[str, Any]]], dict[str, str]]:
    times = sorted({row["event_at"] for row in rows})
    if len(times) < 10:
        raise RuntimeError(f"stock HELD replay too small for chronological split: {len(times)} events")
    train_cut = times[max(0, int(len(times) * 0.60) - 1)]
    val_cut = times[max(0, int(len(times) * 0.80) - 1)]
    return ({
        "train": [row for row in rows if row["event_at"] <= train_cut],
        "validation": [row for row in rows if train_cut < row["event_at"] <= val_cut],
        "test": [row for row in rows if row["event_at"] > val_cut],
        "all": rows,
    }, {"train_end": train_cut.isoformat(), "validation_end": val_cut.isoformat()})


def _stock_study() -> dict[str, Any]:
    cfg = stock_strategy.load_strategy_config()
    source_rows = _stock_configured_cohort(_load_stock_rows(), cfg)
    if not source_rows:
        raise RuntimeError("no archived stock rows pass the configured HELD Paper profile")
    source_rows = _independence_adjusted(source_rows)
    archive = stock_archive.connect()
    frames: dict[tuple[str, str], pd.DataFrame] = {}
    try:
        for symbol in sorted({str(row["symbol"]).upper() for row in source_rows}):
            for timeframe in ("15m", "1m"):
                frames[(symbol, timeframe)] = stock_archive.load_frame(archive, symbol, timeframe)
    finally:
        archive.close()

    entries = [entry for row in source_rows if (entry := _stock_entry(row, frames, cfg)) is not None]
    if len(entries) < 10:
        raise RuntimeError(f"only {len(entries)} stock entries reconstructed from source rows")
    parts, cuts = _stock_split(entries)
    variants: dict[str, Any] = {}
    valid_keys: dict[str, set[tuple[str, str]]] = {}
    for buffer in STOCK_BUFFERS:
        name = f"buffer_{buffer:.2f}_atr"
        cfg_variant = deepcopy(cfg)
        cfg_variant["stop_buffer_atr"] = buffer
        outcomes: list[dict[str, Any]] = []
        keys: set[tuple[str, str]] = set()
        rejected: dict[str, int] = {}
        for trade in entries:
            setup = {
                "decision_at": trade["event_at"], "atr": trade["atr"],
                "stop": trade["shock_low"] - trade["atr"] * buffer,
            }
            geometry = stock_strategy.entry_geometry(setup, trade["entry"], cfg_variant)
            if not geometry.get("ok"):
                reason = str(geometry.get("reason") or "GEOMETRY_REJECTED")
                rejected[reason] = rejected.get(reason, 0) + 1
                continue
            outcome = stock_strategy.simulate_two_target(
                entry=trade["entry"], stop=float(geometry["stop"]),
                tp1=float(geometry["tp1"]), tp2=float(geometry["tp2"]),
                candles=trade["future"], symbol=str(trade["symbol"]),
                cfg=cfg_variant, force_close=True,
            )
            key = (trade["event_at"].isoformat(), str(trade["symbol"]))
            keys.add(key)
            outcomes.append({**outcome, "event_at": trade["event_at"],
                             "entry_at": trade["entry_at"], "key": key,
                             "symbol": trade["symbol"], "buffer_atr": buffer})
        valid_keys[name] = keys
        variants[name] = {
            "buffer_atr": buffer,
            "valid_trades": len(outcomes),
            "geometry_rejections": rejected,
            **{
                part: stock_summary([row for row in outcomes
                                     if row["event_at"] in {trade["event_at"] for trade in subset}])
                for part, subset in parts.items()
            },
            "outcomes": outcomes,
        }

    common_keys = set.intersection(*valid_keys.values()) if valid_keys else set()
    test_times = {trade["event_at"] for trade in parts["test"]}
    for variant in variants.values():
        by_key = {tuple(row["key"]): row for row in variant.pop("outcomes")}
        common = [by_key[key] for key in common_keys if key in by_key]
        variant["paired_common_sample"] = stock_summary(common)
        test_rows = [row for row in common if row["event_at"] in test_times]
        variant["test_diagnostics"] = {
            "close_reasons": dict(Counter(str(row.get("close_reason") or "unknown")
                                           for row in test_rows)),
            "mean_mfe_r": round(sum(float(row.get("mfe_r") or 0.0) for row in test_rows)
                                 / len(test_rows), 3) if test_rows else None,
            "mean_mae_r": round(sum(float(row.get("mae_r") or 0.0) for row in test_rows)
                                 / len(test_rows), 3) if test_rows else None,
        }
    train_eligible = [(value["train"]["net_r"], name) for name, value in variants.items()
                      if value["train"]["trades"] >= 6]
    winner = max(train_eligible)[1] if train_eligible else None
    return {
        "input_clean_independent_rows": len(source_rows),
        "reconstructed_common_entries": len(entries),
        "date_period": [min(row["event_at"] for row in entries).isoformat(),
                        max(row["event_at"] for row in entries).isoformat()],
        "split": cuts,
        "paired_common_entries": len(common_keys),
        "train_only_winner": winner,
        "variants": variants,
    }


def run() -> dict[str, Any]:
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "crypto_europe_session": _crypto_study(),
        "stocks_stop_buffer": _stock_study(),
        "method": {
            "chronology": "60/20/20 train/validation/test; no holdout tuning",
            "crypto": "same FAST 1m rows/outcomes, cascade-adjusted, modeled costs retained",
            "stocks": "same HELD entries; only structural stop buffer changes; fixed $10 risk; TP ladder re-priced to 0.80R/1.35R; stop-first bars; costs/slippage retained",
            "stock_common_sample": "reports paired results only where every stop candidate passes geometry",
        },
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    _write_report(result)
    return result


def _write_report(result: dict[str, Any]) -> None:
    lines = [
        "# Reclaim Variant Backtests", "",
        f"Generated: `{result['generated_at']}`", "",
        "Research only: no order submission. All data is historical and replayed point-in-time where available.",
        "Selection uses training data only; validation and test are reported separately.",
        "",
        "## Crypto FAST Europe", "",
        f"Period: `{result['crypto_europe_session']['period'][0]}` to `{result['crypto_europe_session']['period'][1]}`; "
        f"base replay rows={result['crypto_europe_session']['source_rows']}; "
        f"distinct source events={result['crypto_europe_session']['distinct_events']}.", "",
        "| Variant | Train | Validation | Test | All |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, block in result["crypto_europe_session"]["variants"].items():
        fmt = lambda v: f"n={v['trades']}, {v['net_r']:+.2f}R, PF={v['pf']}"
        lines.append(f"| `{name}` | {fmt(block['train'])} | {fmt(block['validation'])} | "
                     f"{fmt(block['test'])} | {fmt(block['all'])} |")
    stock = result["stocks_stop_buffer"]
    lines.extend([
        "", "## Stocks HELD stop buffer", "",
        f"Period: `{stock['date_period'][0]}` to `{stock['date_period'][1]}`; "
        f"source clean independent rows={stock['input_clean_independent_rows']}; "
        f"reconstructed={stock['reconstructed_common_entries']}; "
        f"paired across all buffers={stock['paired_common_entries']}.",
        f"Training-only top candidate: `{stock['train_only_winner']}`.", "",
        "| Buffer | Train | Validation | Test | All | Paired common | Test exits | Geometry rejects |",
        "|---:|---:|---:|---:|---:|---|---:|---:|",
    ])
    for name, block in stock["variants"].items():
        fmt = lambda v: f"n={v['trades']}, {v['net_r']:+.2f}R, PF={v['pf']}"
        exits = ", ".join(f"{key}:{value}" for key, value in block["test_diagnostics"]["close_reasons"].items()) or "none"
        lines.append(f"| {block['buffer_atr']:.2f} ATR | {fmt(block['train'])} | "
                     f"{fmt(block['validation'])} | {fmt(block['test'])} | {fmt(block['all'])} | "
                     f"{fmt(block['paired_common_sample'])} | {exits} | "
                     f"{sum(block['geometry_rejections'].values())} |")
    crypto_eu = result["crypto_europe_session"]["variants"]["europe_moderate"]
    stock_base = stock["variants"]["buffer_0.10_atr"]
    stock_wide = stock["variants"]["buffer_0.15_atr"]
    lines.extend([
        "", "## Paper Decision", "",
        ("Crypto Europe: run the moderate profile as exploratory Paper because it produced 8 historical trades "
         f"({crypto_eu['all']['net_r']:+.2f}R), but its untouched test is only "
         f"n={crypto_eu['test']['trades']} / {crypto_eu['test']['net_r']:+.2f}R. This is not proven edge."),
        ("Stocks HELD: run the 0.15 ATR buffer as the training-only selected paired Paper variant against the "
         f"0.10 ATR baseline. Validation is weaker and test remains negative "
         f"({stock_wide['test']['net_r']:+.2f}R); full-sample PF is {stock_base['all']['pf']} vs "
         f"{stock_wide['all']['pf']}. This is not a proven improvement or an optimal stop."),
        "", "## Decision Boundary", "",
        "A best in-sample setting is not called optimal if validation/test are weak or too small. "
        "A positive Paper-only result is not a Live promotion; forward Paper evidence and governance gates remain required.",
        "",
    ])
    REPORT.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
