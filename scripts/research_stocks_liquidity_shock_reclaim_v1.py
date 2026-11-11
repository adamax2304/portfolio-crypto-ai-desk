"""Point-in-time historical replay for stock liquidity-shock reclaim v1."""
from __future__ import annotations

import argparse
import itertools
import json
import math
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from src.config import load_config
from src.data_collectors import stocks_liquidity_shock_research_store as archive
from src.execution import stocks_liquidity_shock_reclaim_paper as strategy
from src.execution.shadow_strategy_common import max_drawdown, profit_factor
from src.stocks.configs.loader import load_stocks_config


ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "research_labs" / "stocks_liquidity_shock_reclaim_v1"
REPORT = ROOT / "reports" / "STOCKS_LIQUIDITY_SHOCK_RECLAIM_V1_BACKTEST.md"


def _daily_frame(symbol: str) -> pd.DataFrame:
    path = ROOT / "data" / "raw" / "stocks" / "1d" / f"{symbol}.csv"
    if not path.exists():
        return pd.DataFrame()
    frame = pd.read_csv(path)
    if frame.empty:
        return frame
    frame = frame.rename(columns={str(frame.columns[0]): "timestamp"})
    frame.columns = [str(value).lower() for value in frame.columns]
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
    return frame.dropna(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)


def _liquidity(daily: pd.DataFrame, at: datetime) -> dict[str, Any]:
    if daily.empty:
        return {"ok": False, "reason": "DAILY_LIQUIDITY_MISSING"}
    visible = daily[daily["timestamp"] < pd.Timestamp(at)].tail(30)
    if len(visible) < 10:
        return {"ok": False, "reason": "DAILY_LIQUIDITY_MISSING"}
    values = (visible["close"] * visible["volume"]).dropna()
    return {"ok": bool(len(values)),
            "avg_dollar_volume_30d": float(values.mean()) if len(values) else None}


def _candidate_cfg(cfg: dict[str, Any]) -> dict[str, Any]:
    out = dict(cfg)
    out.update(min_flush_atr=0.80, max_flush_atr=5.0, min_flush_pct=0.30,
               min_rvol=1.0, min_level_breach_atr=0.0,
               min_idiosyncratic_drop_pct=0.0, max_market_drop_pct=1.50,
               max_sector_drop_pct=2.0, min_bar_dollar_volume=500_000.0)
    return out


def _event_samples(limit_symbols: int | None = None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cfg = strategy.load_strategy_config()
    stocks_cfg = load_stocks_config(ROOT)
    symbols = strategy.configured_symbols(cfg)
    if limit_symbols:
        symbols = symbols[:limit_symbols]
    context_symbols = sorted(set(symbols + ["SPY"] + list(stocks_cfg.sector_etfs.values())))
    archived = archive.archive_runtime_frames(context_symbols, ("1m", "15m"), root=ROOT)
    data = archive.connect()
    trading = sqlite3.connect(load_config(ROOT).db_path, timeout=30.0)
    trading.row_factory = sqlite3.Row
    market = archive.load_frame(data, "SPY", "15m")
    sector_frames = {value: archive.load_frame(data, value, "15m")
                     for value in set(stocks_cfg.sector_etfs.values())}
    permissive = _candidate_cfg(cfg)
    samples: list[dict[str, Any]] = []
    missing: Counter[str] = Counter()
    rejection: Counter[str] = Counter()
    news_status: Counter[str] = Counter()
    try:
        for number, symbol in enumerate(symbols, start=1):
            base = archive.load_frame(data, symbol, "15m")
            minute = archive.load_frame(data, symbol, "1m")
            daily = _daily_frame(symbol)
            if base.empty or minute.empty:
                missing["base_or_confirmation"] += 1
                continue
            overlap_start = max(base["timestamp"].min(), minute["timestamp"].min())
            overlap_end = min(base["timestamp"].max() + pd.Timedelta(minutes=15),
                              minute["timestamp"].max())
            if overlap_end <= overlap_start:
                missing["no_overlap"] += 1
                continue
            sector_etf = stocks_cfg.sector_etf_for(symbol)
            sector = sector_frames.get(sector_etf, pd.DataFrame())
            for idx in range(max(20, int(permissive["volume_lookback_bars"])), len(base)):
                shock_at = base.iloc[idx]["timestamp"]
                if shock_at < overlap_start or shock_at + pd.Timedelta(minutes=15) > overlap_end:
                    continue
                setup = strategy.detect_shock(
                    base, idx, market, sector,
                    _liquidity(daily, shock_at.to_pydatetime()), permissive,
                )
                if not setup.get("ok"):
                    rejection[str(setup.get("reason") or "unknown")] += 1
                    continue
                news = strategy.news_risk(trading, symbol, setup["decision_at"], cfg)
                news_status[str(news["status"])] += 1
                if news["blocked"]:
                    rejection["NEGATIVE_FUNDAMENTAL_CATALYST"] += 1
                    continue
                for profile_name, profile in dict(cfg["confirmation_profiles"]).items():
                    horizon = int(profile["confirmation_window_bars"])
                    confirmation = strategy.detect_confirmation(
                        minute, setup, setup["decision_at"] + timedelta(minutes=horizon), profile,
                    )
                    if confirmation["status"] != "entry":
                        rejection[f"{profile_name}:{confirmation.get('reason') or 'NO_CONFIRMATION'}"] += 1
                        continue
                    geometry_setup = strategy._profile_geometry_setup(setup, profile)  # noqa: SLF001
                    if geometry_setup is None:
                        rejection[f"{profile_name}:PROFILE_STOP_INPUT_MISSING"] += 1
                        continue
                    history = base.iloc[max(0, idx - 100):idx + 1].copy()
                    geometry = strategy.entry_geometry(
                        geometry_setup, float(confirmation["entry"]), cfg,
                        profile=profile, history=history,
                    )
                    if not geometry["ok"]:
                        rejection[f"{profile_name}:{geometry['reason']}"] += 1
                        continue
                    entry_at = confirmation["entry_at"]
                    future = minute[minute["timestamp"] >= pd.Timestamp(entry_at)].copy()
                    if future.empty:
                        missing["future"] += 1
                        continue
                    event_day = entry_at.astimezone(strategy.NY).date()
                    future = future[future["timestamp"].map(
                        lambda value: value.to_pydatetime().astimezone(strategy.NY).date() == event_day
                    )].iloc[:int(profile["max_holding_bars"])]
                    if future.empty:
                        missing["future"] += 1
                        continue
                    outcome = strategy.simulate_two_target(
                        entry=float(confirmation["entry"]), stop=float(geometry["stop"]),
                        tp1=float(geometry["tp1"]), tp2=float(geometry["tp2"]),
                        candles=future, symbol=symbol, cfg=cfg, force_close=True,
                    )
                    samples.append({
                        "symbol": symbol, "sector": sector_etf or "unknown",
                        "profile": profile_name, "profile_id": profile["profile_id"],
                        "event_at": setup["decision_at"], "entry_at": entry_at,
                        "flush_atr": float(setup["flush_atr"]),
                        "flush_pct": float(setup["flush_pct"]),
                        "rvol": float(setup["rvol"]),
                        "level_breach_atr": float(setup["level_breach_atr"]),
                        "market_drop_pct": float(setup.get("market_drop_pct") or 0.0),
                        "sector_drop_pct": float(setup.get("sector_drop_pct") or 0.0),
                        "idiosyncratic_drop_pct": float(setup["idiosyncratic_drop_pct"]),
                        "bar_dollar_volume": float(setup["bar_dollar_volume"]),
                        "avg_dollar_volume_30d": float(setup["avg_dollar_volume_30d"]),
                        "stop_distance_pct": float(geometry["stop_distance_pct"]),
                        "news_status": news["status"], **outcome,
                    })
            if number % 15 == 0:
                print(f"replayed {number}/{len(symbols)} symbols -> {len(samples)} profile trades",
                      flush=True)
    finally:
        data.close()
        trading.close()
    return samples, {"symbols": len(symbols), "archived_rows": archived,
                     "missing": dict(missing), "rejections": dict(rejection),
                     "news_status": dict(news_status)}


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    ordered = sorted(rows, key=lambda row: row["entry_at"])
    pnl = [float(row["net_pnl_usd"]) for row in ordered]
    pf = profit_factor(pnl)
    return {
        "trades": len(rows), "net_usd": round(sum(pnl), 2),
        "net_r": round(sum(float(row["net_r"]) for row in rows), 3),
        "pf": None if pf is None or math.isinf(pf) else round(float(pf), 3),
        "winrate": round(sum(value > 0 for value in pnl) / len(pnl), 3) if pnl else 0.0,
        "max_drawdown_usd": round(max_drawdown(pnl), 2),
        "costs_usd": round(sum(float(row.get("fees_usd") or 0.0)
                               + float(row.get("slippage_usd") or 0.0) for row in rows), 2),
    }


def _parameter_grid() -> list[dict[str, Any]]:
    rows = []
    for atr, flush_pct, rvol, idio, market, breach in itertools.product(
        (1.10, 1.30, 1.50), (0.45, 0.60, 0.80), (1.20, 1.40, 1.70),
        (0.20, 0.30, 0.45), (0.60, 0.80, 1.00), (0.0, 0.05, 0.15),
    ):
        rows.append({"min_flush_atr": atr, "max_flush_atr": 3.50,
                     "min_flush_pct": flush_pct, "min_rvol": rvol,
                     "min_idiosyncratic_drop_pct": idio,
                     "max_market_drop_pct": market, "max_sector_drop_pct": 1.10,
                     "min_level_breach_atr": breach})
    return rows


def _filter(rows: list[dict[str, Any]], params: dict[str, Any], profile: str) -> list[dict[str, Any]]:
    return [row for row in rows if row["profile"] == profile
            and params["min_flush_atr"] <= row["flush_atr"] <= params["max_flush_atr"]
            and row["flush_pct"] >= params["min_flush_pct"]
            and row["rvol"] >= params["min_rvol"]
            and row["idiosyncratic_drop_pct"] >= params["min_idiosyncratic_drop_pct"]
            and row["market_drop_pct"] <= params["max_market_drop_pct"]
            and row["sector_drop_pct"] <= params["max_sector_drop_pct"]
            and row["level_breach_atr"] >= params["min_level_breach_atr"]]


def _independence_adjusted(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """One event per symbol/day, one per sector/15m, at most three per market episode."""
    by_symbol_day: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        day = row["event_at"].astimezone(strategy.NY).date().isoformat()
        key = (row["symbol"], day)
        if key not in by_symbol_day or row["flush_atr"] > by_symbol_day[key]["flush_atr"]:
            by_symbol_day[key] = row
    by_sector_time: dict[tuple[str, datetime], dict[str, Any]] = {}
    for row in by_symbol_day.values():
        key = (row["sector"], row["event_at"])
        if key not in by_sector_time or row["idiosyncratic_drop_pct"] > by_sector_time[key]["idiosyncratic_drop_pct"]:
            by_sector_time[key] = row
    by_time: defaultdict[datetime, list[dict[str, Any]]] = defaultdict(list)
    for row in by_sector_time.values():
        by_time[row["event_at"]].append(row)
    selected = []
    for event_rows in by_time.values():
        selected.extend(sorted(event_rows, key=lambda row: row["idiosyncratic_drop_pct"],
                               reverse=True)[:3])
    return sorted(selected, key=lambda row: row["event_at"])


def _select(train: list[dict[str, Any]], profile: str) -> tuple[dict[str, Any], dict[str, Any]]:
    candidates = []
    for params in _parameter_grid():
        selected = _independence_adjusted(_filter(train, params, profile))
        if len(selected) < 8:
            continue
        ordered_times = sorted({row["event_at"] for row in selected})
        folds = []
        for fold in range(3):
            left = int(len(ordered_times) * fold / 3)
            right = int(len(ordered_times) * (fold + 1) / 3)
            times = set(ordered_times[left:right])
            folds.append(_summary([row for row in selected if row["event_at"] in times]))
        if any(block["trades"] < 2 for block in folds):
            continue
        summary = _summary(selected)
        minimum_fold_net = min(block["net_usd"] for block in folds)
        score = (summary["net_usd"] - 0.35 * summary["max_drawdown_usd"]
                 + 1.5 * minimum_fold_net + math.log(summary["trades"] + 1))
        if (summary["pf"] or 0.0) < 0.90:
            score -= 100.0
        candidates.append((score, params, summary))
    if not candidates:
        fallback = {"min_flush_atr": 1.30, "max_flush_atr": 3.50,
                    "min_flush_pct": 0.55, "min_rvol": 1.40,
                    "min_idiosyncratic_drop_pct": 0.30,
                    "max_market_drop_pct": 0.80, "max_sector_drop_pct": 1.10,
                    "min_level_breach_atr": 0.05}
        return fallback, _summary(_independence_adjusted(_filter(train, fallback, profile)))
    _, params, summary = max(candidates, key=lambda item: item[0])
    return params, summary


def run(limit_symbols: int | None = None) -> dict[str, Any]:
    samples, coverage = _event_samples(limit_symbols)
    if not samples:
        raise RuntimeError("no replayable stock liquidity-shock events in the local archive")
    event_times = sorted({row["event_at"] for row in samples})
    split = event_times[max(0, int(len(event_times) * 0.70) - 1)]
    train = [row for row in samples if row["event_at"] <= split]
    holdout = [row for row in samples if row["event_at"] > split]
    results: dict[str, Any] = {}
    for profile in sorted({row["profile"] for row in samples}):
        params, train_summary = _select(train, profile)
        results[profile] = {
            "parameters": params,
            "train": train_summary,
            "holdout": _summary(_independence_adjusted(_filter(holdout, params, profile))),
            "all": _summary(_independence_adjusted(_filter(samples, params, profile))),
            "raw_all": _summary(_filter(samples, params, profile)),
        }
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "period": [min(event_times).isoformat(), max(event_times).isoformat()],
        "split_at": split.isoformat(), "coverage": coverage,
        "profile_results": results,
        "method": {
            "chronological_train_pct": 70, "holdout_pct": 30,
            "intrabar_assumption": "stop_first",
            "independence_adjustment": "one symbol/day; one sector/15m; max three market-wide",
            "news_clock": "canonical available_at <= decision_at",
            "costs": "stock_etf_default plus configured two-sided slippage",
        },
    }
    LAB.mkdir(parents=True, exist_ok=True)
    (LAB / "backtest_result.json").write_text(json.dumps(output, indent=2, default=str),
                                                encoding="utf-8")
    export = pd.DataFrame(samples)
    export.to_csv(LAB / "replay_trades.csv", index=False)
    _write_report(output)
    return output


def _fmt(block: dict[str, Any]) -> str:
    return (f"n={block['trades']}, net=${block['net_usd']:.2f} ({block['net_r']:+.2f}R), "
            f"PF={block['pf']}, win={block['winrate']:.1%}, DD=${block['max_drawdown_usd']:.2f}, "
            f"cost=${block['costs_usd']:.2f}")


def _write_report(result: dict[str, Any]) -> None:
    lines = ["# Stocks Liquidity Shock Reclaim v1 - Historical Replay", "",
             f"- generated: `{result['generated_at']}`",
             f"- event period: `{result['period'][0]}` to `{result['period'][1]}`",
             f"- chronological split: `{result['split_at']}` (70% train / 30% untouched holdout)",
             f"- symbols inspected: `{result['coverage']['symbols']}`",
             f"- archive additions: `{json.dumps(result['coverage']['archived_rows'], sort_keys=True)}`", "",
             "All results include modeled fees/slippage. Same-minute stop/target ambiguity is stop-first. "
             "The replay caps correlated events so one broad selloff cannot inflate the sample."]
    for profile, block in result["profile_results"].items():
        lines.extend(["", f"## {profile}", "",
                      f"- selected on train only: `{json.dumps(block['parameters'], sort_keys=True)}`",
                      f"- train: {_fmt(block['train'])}",
                      f"- holdout: {_fmt(block['holdout'])}",
                      f"- all independent events: {_fmt(block['all'])}",
                      f"- raw diagnostic: {_fmt(block['raw_all'])}"])
    positive = [name for name, block in result["profile_results"].items()
                if block["holdout"]["trades"] >= 5 and (block["holdout"]["pf"] or 0) > 1.0
                and block["holdout"]["net_usd"] > 0]
    lines.extend(["", "## Verdict", "",
                  ("Preliminary holdout edge: " + ", ".join(f"`{name}`" for name in positive)
                   if positive else "No profile proved a positive holdout edge. Both remain Paper-only."),
                  "", "The local minute archive has non-uniform symbol coverage. This replay is an initial "
                  "screen, not a Live promotion decision; the forward Paper cohort remains authoritative."])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit-symbols", type=int)
    args = parser.parse_args()
    print(json.dumps(run(args.limit_symbols), indent=2, default=str))


if __name__ == "__main__":
    main()
