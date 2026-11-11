"""Historical screening adapter for the exact Stocks Position Swing V2 rules.

The adapter is isolated from the scheduler and trading database. It reuses the
production detector, risk plan and outcome simulator on the archived Yahoo
daily bars. Historical corporate-event coverage is incomplete, so every result
is screening evidence only and can never satisfy the forward promotion gate.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import pandas as pd

from src.stocks.configs.loader import load_stocks_config
from src.stocks.position_framework import features
from src.stocks.position_framework.v2_config import load_config
from src.stocks.position_framework.v2_detector import detect
from src.stocks.position_framework.v2_outcome import simulate


ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = ROOT / "research_labs" / "technical_trend_reclaim" / "data" / "stocks" / "yahoo"
EARNINGS_ROOT = ROOT / "research_labs" / "stocks_pead_drift" / "data"
REPORT_PATH = ROOT / "reports" / "STOCKS_POSITION_V2_HISTORICAL.md"
ARTIFACT_PATH = ROOT / "research" / "stocks_backtest" / "artifacts" / "position_v2_historical.json"


def _load(symbol: str) -> pd.DataFrame:
    path = DATA_ROOT / symbol / "1d.parquet"
    if not path.exists():
        return pd.DataFrame()
    frame = pd.read_parquet(path).copy()
    if frame.empty:
        return frame
    frame["session_date"] = pd.to_datetime(frame["session_date"], errors="coerce")
    frame = frame.dropna(subset=["session_date", "open", "high", "low", "close", "volume"])
    frame = frame.drop_duplicates("session_date", keep="last").sort_values("session_date")
    return frame.set_index("session_date")[["open", "high", "low", "close", "volume"]].astype(float)


def _weekly(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return frame
    return frame.resample("W-FRI").agg({
        "open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum",
    }).dropna()


def _earnings_dates(symbol: str) -> list[pd.Timestamp]:
    path = EARNINGS_ROOT / symbol / "earnings.parquet"
    if not path.exists():
        return []
    frame = pd.read_parquet(path)
    values = pd.to_datetime(frame.get("announced_at"), utc=True, errors="coerce")
    return sorted(value.tz_convert(None).normalize() for value in values.dropna())


def _next_earnings_days(dates: list[pd.Timestamp], decision: pd.Timestamp) -> int | None:
    day = decision.tz_localize(None).normalize() if decision.tzinfo else decision.normalize()
    future = [value for value in dates if value >= day]
    return int((future[0] - day).days) if future else None


def _metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    pnl = [float(row["net_pnl_usd"]) for row in rows if row.get("status") == "closed"]
    wins = sum(value for value in pnl if value > 0)
    losses = abs(sum(value for value in pnl if value < 0))
    equity = peak = max_dd = 0.0
    for value in pnl:
        equity += value
        peak = max(peak, equity)
        max_dd = max(max_dd, peak - equity)
    symbols = {str(row["symbol"]) for row in rows if row.get("status") == "closed"}
    sessions = {str(row["entry_date"]) for row in rows if row.get("status") == "closed"}
    return {
        "closed": len(pnl), "net_pnl_usd": round(sum(pnl), 2),
        "profit_factor": round(wins / losses, 4) if losses else None,
        "winrate": round(sum(value > 0 for value in pnl) / len(pnl), 4) if pnl else None,
        "max_drawdown_usd": round(max_dd, 2), "unique_symbols": len(symbols),
        "unique_entry_sessions": len(sessions),
    }


def run() -> dict[str, Any]:
    cfg = load_config()
    stocks_cfg = load_stocks_config()
    benchmarks = {symbol: _load(symbol) for symbol in {"SPY", "QQQ", *stocks_cfg.sector_etfs.values()}}
    spy = benchmarks.get("SPY", pd.DataFrame())
    qqq = benchmarks.get("QQQ", pd.DataFrame())
    if spy.empty or qqq.empty:
        raise RuntimeError("SPY/QQQ daily archive is unavailable")

    context_symbols = {"SPY", "QQQ", "IWM", "DIA", *stocks_cfg.sector_etfs.values()}
    symbols = [path.name for path in DATA_ROOT.iterdir()
               if path.is_dir() and path.name not in context_symbols and (path / "1d.parquet").exists()]
    frames = {symbol: _load(symbol) for symbol in symbols}
    earnings = {symbol: _earnings_dates(symbol) for symbol in symbols}
    weekly = {symbol: _weekly(frame) for symbol, frame in frames.items()}
    all_days = sorted(set.intersection(*(set(frame.index) for frame in frames.values() if not frame.empty)))
    max_open = int((cfg.get("risk") or {}).get("max_open_positions", 5))
    active_until: dict[str, pd.Timestamp] = {}
    active_sector_until: dict[str, list[pd.Timestamp]] = defaultdict(list)
    rows: list[dict[str, Any]] = []
    rejects: dict[str, int] = defaultdict(int)

    for decision in all_days:
        spy_hist = spy.loc[:decision]
        qqq_hist = qqq.loc[:decision]
        if len(spy_hist) < 205 or decision not in qqq.index:
            continue
        next_days = spy.index[spy.index > decision]
        if len(next_days) == 0:
            continue
        next_session = next_days[0]
        active_until = {symbol: end for symbol, end in active_until.items() if end >= next_session}
        for sector in list(active_sector_until):
            active_sector_until[sector] = [end for end in active_sector_until[sector] if end >= next_session]

        spy50 = float(spy_hist["close"].tail(50).mean())
        spy200 = float(spy_hist["close"].tail(200).mean())
        market = {
            "spy_above_50d": float(spy_hist.iloc[-1]["close"]) > spy50,
            "spy_above_200d": float(spy_hist.iloc[-1]["close"]) > spy200,
            "vix": None,
        }
        detected: list[dict[str, Any]] = []
        for symbol, frame in frames.items():
            if symbol in active_until or decision not in frame.index:
                continue
            sector = stocks_cfg.sector_for(symbol)
            sector_etf = stocks_cfg.sector_etf_for(symbol)
            sector_frame = benchmarks.get(sector_etf, pd.DataFrame())
            if not sector_etf or sector_frame.empty or decision not in sector_frame.index:
                rejects["SECTOR_MAPPING_OR_DATA_UNAVAILABLE"] += 1
                continue
            hist = frame.loc[:decision]
            sector_hist = sector_frame.loc[:decision]
            if len(hist) < 205 or len(sector_hist) < 64:
                continue
            feats = features.compute_features(
                hist, spy_df=spy_hist, qqq_df=qqq_hist, sector_df=sector_hist,
                weekly_df=weekly[symbol].loc[:decision],
            )
            sector_rs = features.rs_vs(sector_hist, spy_hist, 63)
            candidate = detect(
                symbol, hist, feats,
                market_ctx=market,
                sector_ctx={
                    "sector": sector, "sector_etf": sector_etf,
                    "sector_above_50d": features.trend_up(sector_hist, 50),
                    "sector_rs_positive": sector_rs is not None and sector_rs > 0,
                },
                earnings={
                    "calendar_available": True,
                    "days": _next_earnings_days(earnings[symbol], decision),
                },
                event_ctx={"blocking": False, "blocking_types": [], "event_data_unavailable": False,
                           "event_types": []},
                cfg=cfg,
                data_ctx={"clean": True, "rejection_reasons": []},
            )
            if candidate.get("passed"):
                candidate["_frame"] = frame
                candidate["_decision"] = decision
                detected.append(candidate)
            else:
                for reason in candidate.get("rejection_reasons") or ["UNKNOWN"]:
                    rejects[str(reason)] += 1

        detected.sort(key=lambda item: (-int(item.get("score") or 0), str(item["symbol"])))
        capacity = max(0, max_open - len(active_until))
        for candidate in detected:
            if capacity <= 0:
                rejects["PORTFOLIO_MAX_OPEN"] += 1
                continue
            sector = str(candidate.get("sector") or "unknown")
            if active_sector_until.get(sector):
                rejects["PORTFOLIO_SECTOR_CAP_CONSERVATIVE"] += 1
                continue
            frame = candidate.pop("_frame")
            candidate.pop("_decision", None)
            plan = dict(candidate.get("risk_plan") or {})
            simulation_candidate = {**candidate, **plan}
            start_idx = int(frame.index.get_loc(next_session)) if next_session in frame.index else None
            if start_idx is None:
                rejects["NEXT_SESSION_MISSING"] += 1
                continue
            outcome = simulate(frame, start_idx, simulation_candidate, cfg.get("execution") or {})
            result = {
                "symbol": candidate["symbol"], "sector": sector,
                "setup_variant": candidate.get("setup_variant"), "score": candidate.get("score"),
                "decision_date": str(decision.date()),
                "evidence": "historical_reconstruction_event_risk_partial",
                **outcome,
            }
            rows.append(result)
            if outcome.get("status") in {"closed", "pending"} and outcome.get("entry_date"):
                end = pd.Timestamp(outcome.get("exit_date") or frame.index[-1])
                active_until[str(candidate["symbol"])] = end
                active_sector_until[sector].append(end)
                capacity -= 1

    closed = [row for row in rows if row.get("status") == "closed"]
    by_setup = {setup: _metrics([row for row in closed if row.get("setup_variant") == setup])
                for setup in sorted({str(row.get("setup_variant")) for row in closed})}
    return {
        "status": "HISTORICAL_SCREENING_ONLY", "symbols": len(frames),
        "start": str(min(all_days).date()) if all_days else None,
        "end": str(max(all_days).date()) if all_days else None,
        "metrics": _metrics(closed), "by_setup": by_setup,
        "outcomes": rows, "top_rejections": sorted(rejects.items(), key=lambda item: -item[1])[:15],
        "limitations": [
            "Current-universe/survivorship reconstruction.",
            "Historical legal/offering/FDA event-risk coverage is incomplete.",
            "VIX is unavailable; regime uses SPY 50d/200d only.",
            "Conservative one-active-position-per-sector approximation.",
        ],
    }


def write_report(result: dict[str, Any], path: str | Path | None = None) -> Path:
    target = Path(path) if path else REPORT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    metric = result["metrics"]
    lines = [
        "# Stocks Position V2 Historical Screening", "",
        "> Screening only. Incomplete historical corporate-event coverage prevents promotion claims.", "",
        f"- Archive: `{result['start']}` to `{result['end']}`; symbols: `{result['symbols']}`",
        f"- Closed: `{metric['closed']}`; net USD: `${metric['net_pnl_usd']:.2f}`; "
        f"PF: `{metric['profit_factor']}`; win rate: `{metric['winrate']}`; "
        f"max DD: `${metric['max_drawdown_usd']:.2f}`", "",
        "| Setup | Closed | Net USD | PF | Win rate |", "|---|---:|---:|---:|---:|",
    ]
    for setup, stat in result["by_setup"].items():
        lines.append(f"| {setup} | {stat['closed']} | {stat['net_pnl_usd']:.2f} | "
                     f"{stat['profit_factor']} | {stat['winrate']} |")
    lines += ["", "## Top rejections", ""]
    lines += [f"- `{reason}`: {count}" for reason, count in result["top_rejections"]]
    lines += ["", "## Limitations", ""] + [f"- {item}" for item in result["limitations"]]
    target.write_text("\n".join(lines), encoding="utf-8")
    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True, default=str), encoding="utf-8")
    return target


__all__ = ["run", "write_report"]
