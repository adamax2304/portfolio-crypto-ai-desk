"""Point-in-time research replay for the three fast-flush v3 Paper profiles."""
from __future__ import annotations

import argparse
import itertools
import json
import math
import sqlite3
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from src.data_collectors.fast_flush_research_store import connect, load_frame
from src.execution import crypto_fast_flush_reclaim_paper as strategy
from src.execution import crypto_liquidity_sweep_shadow as sweep_v1


ROOT = Path(__file__).resolve().parents[1]
INTELLIGENCE_DB = ROOT / "data" / "intelligence" / "market_intelligence.sqlite"
LAB = ROOT / "research_labs" / "fast_flush_reclaim_v3"
REPORT = ROOT / "reports" / "CRYPTO_FAST_FLUSH_RECLAIM_V3_BACKTEST.md"


def _dt(value: Any) -> datetime:
    return datetime.fromisoformat(str(value).replace("Z", "+00:00")).astimezone(timezone.utc)


def _resample(frame: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    if timeframe == "1m":
        return frame.copy()
    minutes = strategy._minutes(timeframe)  # noqa: SLF001
    work = frame.set_index("timestamp")
    result = work.resample(f"{minutes}min", label="left", closed="left").agg(
        {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
    ).dropna().reset_index()
    return result


def _raw_context(conn: sqlite3.Connection, symbol: str, at: datetime, cfg: dict[str, Any]) -> dict[str, Any]:
    permissive = deepcopy(cfg)
    permissive["min_oi_drop_pct"] = -1000.0
    permissive["max_spread_bps"] = 100_000.0
    permissive["derivatives_freshness_minutes"] = 20
    permissive["liquidity_freshness_minutes"] = 20
    return sweep_v1._contexts(conn, symbol, at, permissive)  # noqa: SLF001


def _permissive_cfg(cfg: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(cfg)
    value.update(min_flush_atr=0.0, max_flush_atr=100.0, min_flush_pct=0.0,
                 min_rvol=0.0, min_liquidation_notional_usd=0.0,
                 min_liquidation_percentile=0.0, min_liquidation_history_episodes=0,
                 min_oi_drop_pct=-1000.0, max_oi_drop_pct=1000.0,
                 allowed_sessions=["asia", "europe", "us", "off"])
    return value


def _event_samples(limit: int | None = None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cfg = strategy.load_strategy_config()
    permissive = _permissive_cfg(cfg)
    archive = connect()
    intelligence = sqlite3.connect(INTELLIGENCE_DB)
    intelligence.row_factory = sqlite3.Row
    sql = "SELECT * FROM candidate_events ORDER BY event_at"
    if limit:
        sql += f" LIMIT {int(limit)}"
    events = [dict(row) for row in archive.execute(sql)]
    samples: list[dict[str, Any]] = []
    missing = {"ohlcv": 0, "context": 0, "base_bar": 0, "geometry": 0}
    try:
        for number, event in enumerate(events, start=1):
            at = _dt(event["event_at"])
            start_ms = int((at - timedelta(hours=6)).timestamp() * 1000)
            end_ms = int((at + timedelta(hours=3)).timestamp() * 1000)
            minute, exchange = load_frame(archive, event["symbol"], start_ms, end_ms)
            if minute.empty or len(minute) < 120:
                missing["ohlcv"] += 1
                continue
            base = _resample(minute, "5m")
            indices = base.index[base["timestamp"] == pd.Timestamp(at)].tolist()
            if not indices:
                missing["base_bar"] += 1
                continue
            idx = int(indices[0])
            decision_at = at + timedelta(minutes=5)
            context = _raw_context(intelligence, event["symbol"], decision_at, cfg)
            if not context.get("ok"):
                missing["context"] += 1
                continue
            setup = strategy.detect_flush(
                base, idx,
                [{"side": "SELL", "notional_usd": event["liquidation_notional_usd"],
                  "event_id": event["event_id"], "event_at": event["event_at"]}],
                context, permissive,
                liquidation_percentile=float(event.get("liquidation_percentile") or 0.0),
                liquidation_history_count=100,
            )
            if not setup.get("ok"):
                continue
            for profile_name, profile in cfg["confirmation_profiles"].items():
                tf = str(profile["confirmation_timeframe"])
                confirm_frame = _resample(minute, tf)
                confirmation = strategy.detect_confirmation(confirm_frame, setup, at + timedelta(hours=2), profile)
                if confirmation.get("status") != "entry":
                    continue
                geometry = strategy.entry_geometry(
                    setup, float(confirmation["entry"]), cfg, profile=profile,
                    frame=confirm_frame, entry_at=confirmation["entry_at"],
                )
                if not geometry.get("ok"):
                    missing["geometry"] += 1
                    continue
                entry_at = confirmation["entry_at"]
                future = confirm_frame[confirm_frame["timestamp"] >= pd.Timestamp(entry_at)]
                max_bars = int(profile["max_holding_bars"])
                outcome = strategy.simulate_two_target(
                    entry=float(confirmation["entry"]), stop=float(geometry["stop"]),
                    tp1=float(geometry["tp1"]), tp2=float(geometry["tp2"]),
                    candles=future.iloc[:max_bars], symbol=event["symbol"], cfg=cfg,
                    bar_minutes=strategy._minutes(tf), force_close=True,  # noqa: SLF001
                )
                samples.append({
                    "event_id": event["event_id"], "event_at": at, "decision_at": decision_at,
                    "symbol": event["symbol"], "exchange": exchange, "profile": profile_name,
                    "profile_id": profile["profile_id"], "session": strategy._session(decision_at),  # noqa: SLF001
                    "liquidation_notional_usd": float(event["liquidation_notional_usd"]),
                    "liquidation_percentile": float(event.get("liquidation_percentile") or 0.0),
                    "flush_atr": float(setup["flush_atr"]), "flush_pct": float(setup["flush_pct"]),
                    "rvol": float(setup["rvol"]), "oi_change_pct": float(setup["oi_change_pct"]),
                    "spread_bps": float(setup.get("spread_bps") or 0.0),
                    "stop_distance_pct": float(geometry["stop_distance_pct"]),
                    **outcome,
                })
            if number % 100 == 0:
                print(f"built {number}/{len(events)} events -> {len(samples)} profile trades", flush=True)
    finally:
        archive.close()
        intelligence.close()
    return samples, {"events": len(events), "missing": missing}


def _pf(values: list[float]) -> float | None:
    wins = sum(value for value in values if value > 0)
    losses = -sum(value for value in values if value < 0)
    return None if losses <= 0 else wins / losses


def _max_drawdown(values: list[float]) -> float:
    equity = peak = drawdown = 0.0
    for value in values:
        equity += value
        peak = max(peak, equity)
        drawdown = max(drawdown, peak - equity)
    return drawdown


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    pnl = [float(row["net_pnl_usd"]) for row in sorted(rows, key=lambda item: item["event_at"])]
    return {"trades": len(rows), "net_usd": round(sum(pnl), 2),
            "net_r": round(sum(float(row["net_r"]) for row in rows), 3),
            "pf": None if _pf(pnl) is None else round(float(_pf(pnl)), 3),
            "winrate": round(sum(value > 0 for value in pnl) / len(pnl), 3) if pnl else 0.0,
            "max_drawdown_usd": round(_max_drawdown(pnl), 2),
            "costs_usd": round(sum(float(row["fees_usd"] or 0) + float(row["slippage_usd"] or 0)
                                   for row in rows), 2)}


def _filter(rows: list[dict[str, Any]], params: dict[str, Any], profile: str) -> list[dict[str, Any]]:
    return [row for row in rows if row["profile"] == profile
            and row["session"] in params["sessions"]
            and params["min_flush_atr"] <= row["flush_atr"] <= params["max_flush_atr"]
            and params["min_flush_pct"] <= row["flush_pct"] <= params["max_flush_pct"]
            and row["rvol"] >= params["min_rvol"]
            and row["liquidation_percentile"] >= params["min_liq_percentile"]
            and -params["max_oi_drop_pct"] <= row["oi_change_pct"] <= -params["min_oi_drop_pct"]
            and row["spread_bps"] <= params["max_spread_bps"]
            and params["min_stop_distance_pct"] <= row["stop_distance_pct"] <= params["max_stop_distance_pct"]]


def _cascade_adjusted(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep one strongest symbol per 15m market cascade to avoid pseudo-sample inflation."""
    best: dict[datetime, dict[str, Any]] = {}
    for row in rows:
        at = row["event_at"].replace(minute=row["event_at"].minute - row["event_at"].minute % 15,
                                     second=0, microsecond=0)
        current = best.get(at)
        if current is None or row["liquidation_percentile"] > current["liquidation_percentile"]:
            best[at] = row
    return sorted(best.values(), key=lambda item: item["event_at"])


def _parameter_grid() -> list[dict[str, Any]]:
    grid = []
    flush_bands = ((0.75, 2.50), (1.00, 2.50), (1.50, 2.25))
    stop_bands = ((0.005, 0.015), (0.0075, 0.0125), (0.010, 0.015), (0.0125, 0.015))
    for min_atr, max_atr, min_oi, sessions, flush_band, stop_band in itertools.product(
        (1.25, 1.50), (2.75, 3.25), (0.25, 0.50),
        (("us",), ("europe", "us")), flush_bands, stop_bands,
    ):
        if min_atr >= max_atr:
            continue
        grid.append({"min_flush_atr": min_atr, "max_flush_atr": max_atr,
                     "min_flush_pct": flush_band[0], "max_flush_pct": flush_band[1],
                     "min_rvol": 1.05,
                     "min_oi_drop_pct": min_oi, "max_oi_drop_pct": 3.0,
                     "min_liq_percentile": 0.90, "max_spread_bps": 18.0,
                     "min_stop_distance_pct": stop_band[0],
                     "max_stop_distance_pct": stop_band[1],
                     "sessions": sessions})
    return grid


def _select(train: list[dict[str, Any]], profile: str) -> tuple[dict[str, Any], dict[str, Any]]:
    candidates = []
    for params in _parameter_grid():
        selected = _cascade_adjusted(_filter(train, params, profile))
        summary = _summary(selected)
        if summary["trades"] < 8:
            continue
        ordered_times = sorted({row["event_at"] for row in selected})
        fold_summaries = []
        for fold in range(3):
            left = int(len(ordered_times) * fold / 3)
            right = int(len(ordered_times) * (fold + 1) / 3)
            times = set(ordered_times[left:right])
            fold_summaries.append(_summary([row for row in selected if row["event_at"] in times]))
        if any(item["trades"] < 2 for item in fold_summaries):
            continue
        pf = float(summary["pf"] or 0.0)
        minimum_fold_net = min(item["net_usd"] for item in fold_summaries)
        # Prefer temporal stability inside train. No holdout data enters selection.
        score = (summary["net_usd"] - 0.25 * summary["max_drawdown_usd"]
                 + 2.0 * minimum_fold_net + math.log(summary["trades"] + 1))
        if pf < 0.8:
            score -= 100.0
        candidates.append((score, params, summary))
    if not candidates:
        fallback = _parameter_grid()[0]
        return fallback, _summary(_cascade_adjusted(_filter(train, fallback, profile)))
    _, params, summary = max(candidates, key=lambda item: item[0])
    return params, summary


def run(limit: int | None = None) -> dict[str, Any]:
    samples, coverage = _event_samples(limit)
    if not samples:
        raise RuntimeError("no replayable event samples; run scripts.backfill_fast_flush_1m first")
    event_times = sorted({row["event_at"] for row in samples})
    split = event_times[max(0, int(len(event_times) * 0.70) - 1)]
    train = [row for row in samples if row["event_at"] <= split]
    holdout = [row for row in samples if row["event_at"] > split]
    profiles = sorted({row["profile"] for row in samples})
    results = {}
    for profile in profiles:
        params, train_summary = _select(train, profile)
        train_rows = _cascade_adjusted(_filter(train, params, profile))
        holdout_rows = _cascade_adjusted(_filter(holdout, params, profile))
        all_rows = _cascade_adjusted(_filter(samples, params, profile))
        results[profile] = {"parameters": params, "train": _summary(train_rows),
                            "holdout": _summary(holdout_rows), "all": _summary(all_rows),
                            "raw_all": _summary(_filter(samples, params, profile))}
    output = {"generated_at": datetime.now(timezone.utc).isoformat(),
              "period": [min(event_times).isoformat(), max(event_times).isoformat()],
              "split_at": split.isoformat(), "coverage": coverage,
              "profile_results": results,
              "method": {"chronological_train_pct": 70, "holdout_pct": 30,
                         "intrabar_assumption": "stop_first",
                         "cascade_adjustment": "one strongest trade per market 15m episode",
                         "costs": "Bybit non-VIP taker entry; maker targets; taker stop/time exit; configured slippage"}}
    LAB.mkdir(parents=True, exist_ok=True)
    (LAB / "backtest_result.json").write_text(json.dumps(output, indent=2, default=str), encoding="utf-8")
    pd.DataFrame(samples).to_csv(LAB / "replay_trades.csv", index=False)
    _write_report(output)
    return output


def _fmt(summary: dict[str, Any]) -> str:
    return (f"n={summary['trades']}, net=${summary['net_usd']:.2f} ({summary['net_r']:+.2f}R), "
            f"PF={summary['pf']}, win={summary['winrate']:.1%}, DD=${summary['max_drawdown_usd']:.2f}, "
            f"cost=${summary['costs_usd']:.2f}")


def _write_report(result: dict[str, Any]) -> None:
    lines = ["# Crypto Fast Flush Reclaim v3 - Historical Replay", "",
             f"- generated: `{result['generated_at']}`",
             f"- event period: `{result['period'][0]}` to `{result['period'][1]}`",
             f"- chronological split: `{result['split_at']}` (70% train / 30% untouched holdout)",
             f"- source events: `{result['coverage']['events']}`",
             f"- missing: `{json.dumps(result['coverage']['missing'], sort_keys=True)}`", "",
             "Every result below is net of modeled fees and slippage. Simultaneous stop/target bars are stop-first. "
             "Correlated market cascades count once, using the strongest liquidation event."]
    for profile, block in result["profile_results"].items():
        lines.extend(["", f"## {profile}", "",
                      f"- selected on train only: `{json.dumps(block['parameters'], sort_keys=True)}`",
                      f"- train: {_fmt(block['train'])}",
                      f"- holdout: {_fmt(block['holdout'])}",
                      f"- all cascade-adjusted: {_fmt(block['all'])}",
                      f"- all raw trades (diagnostic): {_fmt(block['raw_all'])}"])
    positive = [name for name, block in result["profile_results"].items()
                if block["holdout"]["trades"] >= 5 and (block["holdout"]["pf"] or 0) > 1.0
                and block["holdout"]["net_usd"] > 0]
    lines.extend(["", "## Verdict", "",
                  ("Modest out-of-sample edge is present in: " + ", ".join(f"`{name}`" for name in positive)
                   if positive else "No profile demonstrated a positive holdout edge. Keep all profiles in Paper and collect more evidence."),
                  "", "This is Router-style evidence, not a promotion decision: 35 days is short and the candidate archive is event-selected."])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    result = run(args.limit)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
