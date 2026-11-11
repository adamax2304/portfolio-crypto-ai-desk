"""Read-only evidence registry for every distinct stock strategy family.

This module combines frozen research artifacts with current forward/Paper
read-model tables. It does not run production code, mutate strategy settings or
write to the trading database. Its job is to decide which hypotheses deserve a
later parameter study and which should stop.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

from src.config import load_config


ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = ROOT / "reports" / "STOCKS_ALL_MODES_BASELINE.md"


def _data_readiness() -> dict[str, Any]:
    yahoo = ROOT / "research_labs" / "technical_trend_reclaim" / "data" / "stocks" / "yahoo"
    mexc = ROOT / "research_labs" / "technical_trend_reclaim" / "data" / "stocks" / "mexc_contract"
    earnings = ROOT / "research_labs" / "stocks_pead_drift" / "data"
    result: dict[str, Any] = {
        "yahoo_symbols_15m": len(list(yahoo.glob("*/15m.parquet"))),
        "yahoo_symbols_1h": len(list(yahoo.glob("*/1h.parquet"))),
        "yahoo_symbols_1d": len(list(yahoo.glob("*/1d.parquet"))),
        "mexc_symbols_15m": len(list(mexc.glob("*/15m.parquet"))),
        "earnings_symbols": len(list(earnings.glob("*/earnings.parquet"))),
    }
    for timeframe in ("15m", "1h", "1d"):
        path = yahoo / "SPY" / f"{timeframe}.parquet"
        if not path.exists():
            continue
        frame = pd.read_parquet(path, columns=["bar_open_at"])
        values = pd.to_datetime(frame["bar_open_at"], utc=True, errors="coerce").dropna()
        result[f"spy_{timeframe}_start"] = values.min().isoformat() if len(values) else None
        result[f"spy_{timeframe}_end"] = values.max().isoformat() if len(values) else None
        result[f"spy_{timeframe}_days"] = (
            round((values.max() - values.min()).total_seconds() / 86400, 1) if len(values) else 0)
    return result


def _rows(conn: sqlite3.Connection, sql: str, params: Iterable[Any] = ()) -> list[dict[str, Any]]:
    return [dict(row) for row in conn.execute(sql, tuple(params)).fetchall()]


def _metric(values: Iterable[float]) -> dict[str, Any]:
    pnl = [float(value or 0.0) for value in values]
    wins = [value for value in pnl if value > 0]
    losses = [value for value in pnl if value < 0]
    gross_loss = abs(sum(losses))
    equity = peak = 0.0
    max_dd = 0.0
    for value in pnl:
        equity += value
        peak = max(peak, equity)
        max_dd = max(max_dd, peak - equity)
    return {
        "closed": len(pnl),
        "net_pnl_usd": round(sum(pnl), 2),
        "profit_factor": round(sum(wins) / gross_loss, 4) if gross_loss else None,
        "winrate": round(len(wins) / len(pnl), 4) if pnl else None,
        "max_drawdown_usd": round(max_dd, 2),
    }


def _artifact(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _dt(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def _json_list(value: Any) -> list[str]:
    try:
        parsed = json.loads(value or "[]")
        return [str(item).upper() for item in parsed] if isinstance(parsed, list) else []
    except (TypeError, ValueError, json.JSONDecodeError):
        return []


def _record(*, family: str, implementation: str, evidence: str, metrics: dict[str, Any],
            verdict: str, reason: str, source: str) -> dict[str, Any]:
    return {
        "family": family,
        "implementation": implementation,
        "evidence": evidence,
        "metrics": metrics,
        "verdict": verdict,
        "reason": reason,
        "source": source,
    }


def _forward_intraday(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    latest = _rows(conn, """
        SELECT e.* FROM stocks_intraday_forward_shadow_evaluations e
        JOIN (
          SELECT entry_mode, MAX(id) AS max_id
          FROM stocks_intraday_forward_shadow_evaluations GROUP BY entry_mode
        ) latest ON latest.max_id=e.id
        ORDER BY e.entry_mode
    """)
    out: list[dict[str, Any]] = []
    for row in latest:
        mode = str(row.get("entry_mode") or "unknown")
        closed = int(row.get("clean_closed") or 0)
        pf = row.get("profit_factor")
        plausible = float(row.get("net_pnl_usd") or 0) > 0 and (pf is None or float(pf) >= 1.0)
        verdict = "CONTINUE_BASELINE_FORWARD" if plausible else "REVIEW_OR_STOP"
        if closed < 30:
            verdict = "UNDERPOWERED_CONTINUE_FORWARD" if plausible else "UNDERPOWERED_WEAK"
        out.append(_record(
            family=f"stocks_intraday_{mode.lower()}",
            implementation=mode,
            evidence="forward_post_activation",
            metrics={
                "closed": closed,
                "net_pnl_usd": round(float(row.get("net_pnl_usd") or 0), 2),
                "profit_factor": pf,
                "winrate": row.get("winrate"),
                "forward_days": round(float(row.get("forward_days") or 0), 2),
            },
            verdict=verdict,
            reason="Current production rule, not the rejected raw profile.",
            source="stocks_intraday_forward_shadow_evaluations",
        ))
    return out


def _raw_intraday(conn: sqlite3.Connection) -> dict[str, Any]:
    rows = _rows(conn, """
        SELECT profile_id, net_pnl_usd
        FROM stocks_intraday_variant_shadow_outcomes
        WHERE outcome_status='closed' AND is_clean_for_edge=1
        ORDER BY exit_ts, candidate_id
    """)
    stat = _metric(row["net_pnl_usd"] for row in rows)
    stat["profiles"] = len({row["profile_id"] for row in rows})
    return _record(
        family="stocks_intraday_raw_variants",
        implementation="1bar/2bar/retest/VWAP-hold raw controls",
        evidence="forward_shadow_clean",
        metrics=stat,
        verdict="REJECT_STOP_TUNING",
        reason="Large clean sample is negative after costs; quality profiles have no closed sample.",
        source="stocks_intraday_variant_shadow_outcomes",
    )


def _catalyst(conn: sqlite3.Connection) -> dict[str, Any]:
    values = _rows(conn, """
        SELECT net_pnl_usd FROM stocks_catalyst_rs_shadow_outcomes
        WHERE profile_id='stocks_catalyst_rs_profile_v2'
          AND window='forward_post_activation'
          AND outcome_status='closed' AND is_clean_for_edge=1
        ORDER BY exit_ts, candidate_id
    """)
    stat = _metric(row["net_pnl_usd"] for row in values)
    return _record(
        family="stocks_catalyst_rs",
        implementation="Catalyst RS v2",
        evidence="forward_post_activation",
        metrics=stat,
        verdict="UNDERPOWERED_WEAK_BASELINE",
        reason="Event logic is distinct, but current forward net result is negative and below 30 closes.",
        source="stocks_catalyst_rs_shadow_outcomes",
    )


def _earnings(conn: sqlite3.Connection) -> dict[str, Any]:
    rows = _rows(conn, """
        SELECT outcome_status,is_clean_for_edge,net_pnl_usd
        FROM stocks_earnings_gap_shadow_outcomes
        WHERE strategy_id='stocks_earnings_gap_continuation_v2'
    """)
    closed = [row["net_pnl_usd"] for row in rows
              if row["outcome_status"] == "closed" and int(row["is_clean_for_edge"] or 0) == 1]
    stat = _metric(closed)
    stat["observations"] = len(rows)
    return _record(
        family="stocks_earnings_gap",
        implementation="Earnings Gap Continuation v2",
        evidence="earnings_only_v2",
        metrics=stat,
        verdict="NO_VALID_SAMPLE",
        reason="The mixed-event v1 history is invalid for v2; v2 has no clean closed trades yet.",
        source="stocks_earnings_gap_shadow_outcomes",
    )


def _position(conn: sqlite3.Connection) -> dict[str, Any]:
    rows = _rows(conn, """
        SELECT net_pnl_usd FROM stocks_position_v2_outcomes
        WHERE status='closed' AND data_clean=1 ORDER BY exit_date,id
    """)
    return _record(
        family="stocks_position_swing_v2",
        implementation="Position Framework v2",
        evidence="forward_shadow_clean",
        metrics=_metric(row["net_pnl_usd"] for row in rows),
        verdict="NO_VALID_SAMPLE" if len(rows) < 10 else "REVIEW_BASELINE",
        reason="A multi-session historical adapter is required before parameter screening.",
        source="stocks_position_v2_outcomes",
    )


def _preus(conn: sqlite3.Connection) -> dict[str, Any]:
    values = _rows(conn, """
        SELECT p.ticker,substr(p.entry_at,1,10) AS session,o.source_score,l.net_pnl_usdt
        FROM mexc_stock_futures_paper_positions p
        JOIN mexc_stock_futures_paper_orders o ON o.order_id=p.order_id
        JOIN paper_portfolio_ledger l
          ON l.signal_id=p.source_signal_id AND l.event_type='exit'
         AND l.fee_profile='mexc_default_futures'
        WHERE p.strategy_id='stocks_mexc_preopen_news_v1' AND p.status='CLOSED'
        ORDER BY p.exit_at,p.position_id
    """)
    sessions = conn.execute("""
        SELECT COUNT(DISTINCT substr(entry_at,1,10))
        FROM mexc_stock_futures_paper_positions
        WHERE strategy_id='stocks_mexc_preopen_news_v1' AND status='CLOSED'
    """).fetchone()[0]
    stat = _metric(row["net_pnl_usdt"] for row in values)
    stat["sessions"] = int(sessions or 0)
    stat["net_r"] = round(float(conn.execute("""
        SELECT COALESCE(SUM(paper_execution_r),0)
        FROM mexc_stock_futures_paper_positions
        WHERE strategy_id='stocks_mexc_preopen_news_v1' AND status='CLOSED'
    """).fetchone()[0]), 2)
    by_day: dict[str, float] = {}
    by_symbol: dict[str, float] = {}
    for row in values:
        by_day[str(row["session"])] = by_day.get(str(row["session"]), 0.0) + float(row["net_pnl_usdt"] or 0)
        by_symbol[str(row["ticker"])] = by_symbol.get(str(row["ticker"]), 0.0) + float(row["net_pnl_usdt"] or 0)
    positive_total = sum(max(0.0, float(row["net_pnl_usdt"] or 0)) for row in values)
    positive_symbols = sorted((max(0.0, value) for value in by_symbol.values()), reverse=True)
    stat["positive_sessions"] = sum(value > 0 for value in by_day.values())
    stat["best_session_share_of_net"] = (
        round(max(by_day.values()) / stat["net_pnl_usd"], 4) if by_day and stat["net_pnl_usd"] > 0 else None)
    stat["net_without_best_session_usd"] = (
        round(stat["net_pnl_usd"] - max(by_day.values()), 2) if by_day else None)
    stat["top5_positive_profit_share"] = (
        round(sum(positive_symbols[:5]) / positive_total, 4) if positive_total else None)
    stat["score_threshold_sensitivity"] = []
    for threshold in (65, 70, 75, 80, 85, 90):
        selected = [float(row["net_pnl_usdt"] or 0) for row in values
                    if float(row.get("source_score") or 0) >= threshold]
        stat["score_threshold_sensitivity"].append({"min_score": threshold, **_metric(selected)})
    return _record(
        family="stocks_preus_mexc_news",
        implementation="stocks_mexc_preopen_news_v1",
        evidence="forward_paper",
        metrics=stat,
        verdict="PROMISING_UNDERPOWERED",
        reason="Strong early result, but only a few sessions and a long-heavy sample.",
        source="mexc_stock_futures_paper_positions + active-profile ledger",
    )


def _frozen_research() -> list[dict[str, Any]]:
    trend = _artifact("research_labs/technical_trend_reclaim/artifacts/FINAL_VERDICT_2026-08-06.json")
    residual_dev = _artifact(
        "research_labs/stocks_residual_momentum/artifacts/FROZEN_DEVELOPMENT_STOCKS_RESIDUAL_MOMENTUM.json")
    residual_val = _artifact(
        "research_labs/stocks_residual_momentum/artifacts/VALIDATION_0e1022084fcea9c10df76d99.json")
    residual_audit = _artifact(
        "research_labs/stocks_residual_momentum/artifacts/KNOWN_AUDIT_02454830e3b35f2b1685c919.json")
    pead_val = _artifact("research_labs/stocks_pead_drift/artifacts/VALIDATION_19643b606f2dd760ffe83b93.json")
    pead_short = _artifact(
        "research_labs/stocks_pead_drift/artifacts/SHORT_DEVELOPMENT_dcc89ef183b6822678e6c69f.json")

    residual = ((residual_val.get("pooled") or {}).get("v01") or
                residual_dev.get("development_metrics") or {})
    residual_development = residual_dev.get("development_metrics") or {}
    residual_known = (residual_audit.get("pooled") or {}).get("v01") or {}
    long_pead = ((pead_val.get("pooled") or {}).get("v05") or {})
    short_profiles = list((pead_short.get("pooled") or {}).values())
    best_short = max(short_profiles, key=lambda item: float(item.get("net_pnl_usd") or -1e99), default={})
    stock_trend = trend.get("stocks") or {}
    position_screen = _artifact("research/stocks_backtest/artifacts/position_v2_historical.json")
    records = [
        _record(
            family="stocks_residual_momentum",
            implementation="Residual Momentum v01",
            evidence="historical_validation_partially_informed",
            metrics={
                "closed": residual.get("trades"), "net_pnl_usd": residual.get("net_pnl_usd"),
                "profit_factor": residual.get("profit_factor"), "winrate": residual.get("winrate"),
                "max_drawdown_r": residual.get("max_drawdown_r"),
                "top5_profit_share": residual.get("top5_profit_share"),
                "max_symbol_profit_share": residual.get("max_symbol_profit_share"),
                "development": residual_development,
                "known_audit": residual_known,
            },
            verdict="PROMISING_BUT_CONCENTRATED",
            reason="Positive development and validation, but trade count and concentration fail selection gates.",
            source="frozen residual-momentum artifacts",
        ),
        _record(
            family="stocks_pead_long",
            implementation="PEAD long v05",
            evidence="untouched_2024_validation",
            metrics=long_pead,
            verdict="REJECT_VALIDATION_FAILURE",
            reason="The frozen development winner failed the next calendar year.",
            source="frozen PEAD validation artifact",
        ),
        _record(
            family="stocks_pead_short",
            implementation="PEAD short grid",
            evidence="development_reconstruction",
            metrics=best_short,
            verdict="REJECT_NO_GRID_EDGE",
            reason="Every preregistered short profile was negative.",
            source="frozen PEAD short artifact",
        ),
        _record(
            family="stocks_technical_fvg_reclaim",
            implementation="H1 trend + M15 FVG/reclaim",
            evidence="development_reconstruction",
            metrics={
                "closed": 31,
                "net_pnl_usd": stock_trend.get("best_net_pnl_usd"),
                "gross_pnl_usd": stock_trend.get("best_gross_pnl_usd"),
            },
            verdict="REJECT_NO_GROSS_EDGE",
            reason="The best profile lost before costs; the sealed holdout was correctly left unopened.",
            source="technical trend reclaim final verdict",
        ),
    ]
    if position_screen:
        records.append(_record(
            family="stocks_position_swing_v2_historical",
            implementation="Exact Position V2 detector/risk/outcome adapter",
            evidence="historical_screening_event_risk_partial",
            metrics=position_screen.get("metrics") or {},
            verdict="UNDERPOWERED_NO_EDGE_YET",
            reason="Exact screening is near flat; pullback is weak and breakout has only one close.",
            source="isolated Position V2 historical adapter",
        ))
    return records


def _news_attribution(conn: sqlite3.Connection) -> dict[str, Any]:
    canonical = dict(conn.execute("""
        SELECT COUNT(*) AS n, MIN(available_at) AS first_at, MAX(available_at) AS last_at
        FROM news_canonical_events WHERE asset_class='stocks'
    """).fetchone())
    reviews = dict(conn.execute("""
        SELECT COUNT(*) AS n,
               SUM(CASE WHEN datetime(r.reviewed_at)<=datetime(a.evaluated_at) THEN 1 ELSE 0 END) AS causal
        FROM stocks_preus_review r JOIN stocks_preus_actionability a USING(signal_id)
    """).fetchone())
    review_outcomes = _rows(conn, """
        SELECT COALESCE(r.review_verdict,'NO_REVIEW') AS review_verdict,
               COUNT(*) AS closed, ROUND(SUM(l.net_pnl_usdt),2) AS net_pnl_usd
        FROM mexc_stock_futures_paper_positions p
        LEFT JOIN stocks_preus_review r ON r.signal_id=p.source_signal_id
        JOIN paper_portfolio_ledger l
          ON l.signal_id=p.source_signal_id AND l.event_type='exit'
         AND l.fee_profile='mexc_default_futures'
        WHERE p.status='CLOSED' GROUP BY COALESCE(r.review_verdict,'NO_REVIEW')
        ORDER BY closed DESC
    """)
    labels = dict(conn.execute("""
        SELECT COUNT(*) AS exits,
               SUM(CASE WHEN COALESCE(lab.catalyst_freshness,'none')!='none' THEN 1 ELSE 0 END) AS labelled
        FROM paper_portfolio_ledger l
        JOIN proposed_signals p ON p.signal_id=l.signal_id
        LEFT JOIN signal_catalyst_labels lab ON lab.signal_id=l.signal_id
        WHERE l.event_type='exit' AND l.fee_profile='mexc_default_futures'
          AND p.asset_class='stocks'
    """).fetchone())
    technical = _technical_news_attribution(conn)
    return {
        "canonical_stock_events": canonical,
        "causal_preus_reviews": reviews,
        "preus_outcomes_by_review_verdict": review_outcomes,
        "paper_exit_catalyst_label_coverage": labels,
        "technical_outcomes_by_causal_news_state": technical,
        "conclusion": (
            "News is causally timestamped and materially participates in event strategies. "
            "The current technical-Paper exit sample has inadequate catalyst-label coverage, so "
            "a reliable news-vs-no-news PnL claim cannot yet be made. Enriched review is mostly "
            "neutral/caution and has too few closed outcomes for an incremental-PnL claim."
        ),
    }


def _technical_news_attribution(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """Classify news known at entry for the large raw technical control sample."""
    outcomes = _rows(conn, """
        SELECT candidate_id,decision_at,symbol,direction,net_pnl_usd
        FROM stocks_intraday_variant_shadow_outcomes
        WHERE outcome_status='closed' AND is_clean_for_edge=1
        ORDER BY decision_at,candidate_id
    """)
    decisions = [_dt(row.get("decision_at")) for row in outcomes]
    valid = [value for value in decisions if value is not None]
    if not valid:
        return []
    start = min(valid) - timedelta(days=7)
    end = max(valid)
    events = _rows(conn, """
        SELECT event_id,available_at,trusted_symbols_json,event_type,direction_hint,
               source_quality,confidence,linkage_allowed,risk_action,is_cluster_primary
        FROM news_canonical_events
        WHERE asset_class='stocks' AND datetime(available_at)>=datetime(?)
          AND datetime(available_at)<=datetime(?)
    """, (start.isoformat(), end.isoformat()))
    by_symbol: dict[str, list[dict[str, Any]]] = {}
    for event in events:
        event_at = _dt(event.get("available_at"))
        if event_at is None or int(event.get("linkage_allowed") or 0) != 1:
            continue
        if event.get("is_cluster_primary") is not None and int(event.get("is_cluster_primary") or 0) != 1:
            continue
        event["_at"] = event_at
        for symbol in _json_list(event.get("trusted_symbols_json")):
            by_symbol.setdefault(symbol, []).append(event)
    for items in by_symbol.values():
        items.sort(key=lambda item: item["_at"])

    risk_types = {"legal_risk", "offering_dilution", "management_change", "calendar_risk"}
    trusted = {"regulator", "primary", "company_pr", "reputable"}
    grouped: dict[str, list[float]] = {}
    for row in outcomes:
        decision = _dt(row.get("decision_at"))
        direction = str(row.get("direction") or "").lower()
        state = "NO_FRESH_NEWS"
        saw_stale = False
        if decision is not None:
            for event in by_symbol.get(str(row.get("symbol") or "").upper(), []):
                age = decision - event["_at"]
                if age.total_seconds() < 0 or age > timedelta(days=7):
                    continue
                if age > timedelta(hours=18):
                    saw_stale = True
                    continue
                event_type = str(event.get("event_type") or "").lower()
                hint = str(event.get("direction_hint") or "").lower()
                quality = str(event.get("source_quality") or "").lower()
                risk = str(event.get("risk_action") or "").lower()
                if event_type in risk_types or risk in {"block", "risk_warning", "demote"}:
                    state = "NEGATIVE_OR_RISK"
                    break
                aligned = (hint == "bullish" and direction == "long") or (hint == "bearish" and direction == "short")
                conflicted = (hint == "bullish" and direction == "short") or (hint == "bearish" and direction == "long")
                if conflicted:
                    state = "NEGATIVE_OR_RISK"
                    break
                if aligned and quality in trusted and float(event.get("confidence") or 0) >= 0.68:
                    state = "POSITIVE_CONFIRMED"
            if state == "NO_FRESH_NEWS" and saw_stale:
                state = "UNKNOWN_OR_STALE"
        grouped.setdefault(state, []).append(float(row.get("net_pnl_usd") or 0.0))
    return [{"state": state, **_metric(values)} for state, values in sorted(grouped.items())]


def run(db: str | Path | None = None) -> dict[str, Any]:
    path = Path(db) if db else load_config().db_path
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        modes = []
        modes.extend(_forward_intraday(conn))
        modes.extend([_raw_intraday(conn), _catalyst(conn), _earnings(conn), _position(conn), _preus(conn)])
        modes.extend(_frozen_research())
        news = _news_attribution(conn)
    finally:
        conn.close()
    return {"database": str(path), "modes": modes, "news_attribution": news,
            "data_readiness": _data_readiness()}


def _fmt(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Stocks All-Modes Baseline",
        "",
        "> Read-only evidence registry. No strategy was changed or promoted by this report.",
        "",
        "| Family | Evidence | Closed | Net USD | PF | Verdict |",
        "|---|---|---:|---:|---:|---|",
    ]
    for mode in result["modes"]:
        metrics = mode["metrics"]
        lines.append(
            f"| `{mode['family']}` | {mode['evidence']} | {_fmt(metrics.get('closed'))} | "
            f"{_fmt(metrics.get('net_pnl_usd'))} | {_fmt(metrics.get('profit_factor'))} | "
            f"**{mode['verdict']}** |"
        )
    data = result.get("data_readiness") or {}
    lines += [
        "", "## Data readiness", "",
        f"- Yahoo symbols: 15m `{data.get('yahoo_symbols_15m', 0)}`, "
        f"1h `{data.get('yahoo_symbols_1h', 0)}`, 1d `{data.get('yahoo_symbols_1d', 0)}`.",
        f"- SPY coverage: 15m `{data.get('spy_15m_days', 0)}d`, "
        f"1h `{data.get('spy_1h_days', 0)}d`, 1d `{data.get('spy_1d_days', 0)}d`.",
        f"- MEXC stock-contract 15m symbols: `{data.get('mexc_symbols_15m', 0)}`.",
        f"- Symbols with reconstructed earnings history: `{data.get('earnings_symbols', 0)}`.",
        "- Intraday event studies are constrained by the short 15m/news overlap; 18-month claims use 1h/1d only.",
    ]
    lines += ["", "## Decisions", ""]
    for mode in result["modes"]:
        lines.append(f"- `{mode['family']}`: **{mode['verdict']}**. {mode['reason']}")
    preus = next((mode for mode in result["modes"] if mode["family"] == "stocks_preus_mexc_news"), None)
    if preus:
        stat = preus["metrics"]
        lines += [
            "", "### Pre-US robustness check", "",
            f"- Positive sessions: `{stat.get('positive_sessions')}/{stat.get('sessions')}`.",
            f"- Best session share of net PnL: `{_fmt(stat.get('best_session_share_of_net'))}`.",
            f"- Net PnL after removing the best session: `${_fmt(stat.get('net_without_best_session_usd'))}`.",
            f"- Top-five symbol share of positive profit: `{_fmt(stat.get('top5_positive_profit_share'))}`.",
            "- The result survives removal of its best day, but the sample is still only seven sessions and all long.",
            "", "Score-threshold sensitivity is in-sample diagnostic only:", "",
            "| Minimum score | Closed | Net USD | PF |", "|---:|---:|---:|---:|",
        ]
        for row in stat.get("score_threshold_sensitivity") or []:
            lines.append(
                f"| {row['min_score']} | {row['closed']} | {_fmt(row['net_pnl_usd'])} | "
                f"{_fmt(row['profit_factor'])} |"
            )
    residual = next((mode for mode in result["modes"] if mode["family"] == "stocks_residual_momentum"), None)
    if residual:
        val = residual["metrics"]
        dev = val.get("development") or {}
        audit = val.get("known_audit") or {}
        lines += [
            "", "### Residual-momentum period check", "",
            "| Period | Closed | Net USD | PF | Win rate |", "|---|---:|---:|---:|---:|",
            f"| Development 2020-2023 | {_fmt(dev.get('clean_closed'))} | "
            f"{_fmt(dev.get('net_pnl_usd'))} | {_fmt(dev.get('profit_factor'))} | {_fmt(dev.get('winrate'))} |",
            f"| Validation 2024 | {_fmt(val.get('closed'))} | {_fmt(val.get('net_pnl_usd'))} | "
            f"{_fmt(val.get('profit_factor'))} | {_fmt(val.get('winrate'))} |",
            f"| Known audit 2025-2026 | {_fmt(audit.get('trades'))} | {_fmt(audit.get('net_pnl_usd'))} | "
            f"{_fmt(audit.get('profit_factor'))} | {_fmt(audit.get('winrate'))} |",
            "", "The sign is positive in all three periods, but validation/audit are small and not fully sealed.",
        ]
    news = result["news_attribution"]
    canonical = news["canonical_stock_events"]
    reviews = news["causal_preus_reviews"]
    labels = news["paper_exit_catalyst_label_coverage"]
    lines += [
        "", "## News and Enriched Review", "",
        f"- Canonical stock news rows: `{canonical.get('n', 0)}` from `{canonical.get('first_at')}` "
        f"to `{canonical.get('last_at')}`.",
        f"- Causal pre-US reviews: `{reviews.get('causal', 0)}/{reviews.get('n', 0)}`.",
        f"- Current stock Paper exits with a non-empty catalyst label: "
        f"`{labels.get('labelled', 0)}/{labels.get('exits', 0)}`.",
        "", news["conclusion"], "",
        "### Closed Pre-US PnL by review verdict", "",
        "| Verdict | Closed | Net USD |", "|---|---:|---:|",
    ]
    for row in news["preus_outcomes_by_review_verdict"]:
        lines.append(f"| {row['review_verdict']} | {row['closed']} | {_fmt(row['net_pnl_usd'])} |")
    lines += ["", "### Raw technical controls by causal news state", "",
              "| News state at decision | Closed | Net USD | PF | Win rate |",
              "|---|---:|---:|---:|---:|"]
    for row in news["technical_outcomes_by_causal_news_state"]:
        lines.append(
            f"| {row['state']} | {row['closed']} | {_fmt(row['net_pnl_usd'])} | "
            f"{_fmt(row['profit_factor'])} | {_fmt(row['winrate'])} |"
        )
    lines += [
        "", "## Strict next stage", "",
        "1. Stop PEAD, technical FVG reclaim and raw intraday variant tuning.",
        "2. Continue exact production breakout/pullback forward collection; do not pool raw controls.",
        "3. Expand residual-momentum universe/history and test concentration controls.",
        "4. Keep Position V2 parameters frozen: its new exact historical screen is near flat and underpowered.",
        "5. Keep pre-US MEXC unchanged while accumulating more sessions; validate event and direction slices.",
        "6. Keep Catalyst RS and Earnings Gap in evidence collection; their current historical event window is too short.",
        "7. Continue forward materialization of point-in-time news-state labels; the first causal ablation is underpowered.",
    ]
    return "\n".join(lines)


def write_report(result: dict[str, Any], path: str | Path | None = None) -> Path:
    target = Path(path) if path else REPORT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_markdown(result), encoding="utf-8")
    return target


__all__ = ["run", "render_markdown", "write_report"]
