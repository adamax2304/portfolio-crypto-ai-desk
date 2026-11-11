"""Reporting for Stocks Position Swing V2 shadow evidence."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import v2_store
from .v2_config import ROOT

REPORT_PATH = ROOT / "reports" / "stocks_position_swing_v2_latest.md"


def _fmt(value: Any, digits: int = 2) -> str:
    try:
        return "-" if value is None else f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def render(cfg: dict[str, Any], *, db_path=None, scan_result=None) -> str:
    candidates = v2_store.latest_candidates(limit=100, db_path=db_path)
    outcomes = v2_store.latest_outcomes(db_path=db_path)
    ready = v2_store.readiness(cfg, db_path=db_path)
    reviews = v2_store.latest_reviews(limit=20, db_path=db_path)
    rejection_counts = getattr(scan_result, "rejection_counts", {}) if scan_result else {}
    lines = [
        "# Stocks Position Swing V2",
        "",
        "> SHADOW ONLY. Separate tables and strategy identity. No proposed_signals, "
        "signal_outcomes, final_r, Paper ledger, Telegram, or live routing.",
        "",
        f"- strategy_id: `{cfg.get('strategy_id')}`",
        f"- shadow_lane: `{cfg.get('shadow_lane')}`",
        f"- profile: `{cfg.get('profile_version')}`",
        f"- execution profile: `{(cfg.get('execution') or {}).get('profile_id')}`",
        f"- scheduler_enabled: `{bool(cfg.get('scheduler_enabled'))}`",
        "",
        "## Implemented rules",
        "",
        "- Long-only v2.",
        "- Setups: confirmed BREAKOUT_RETEST and TREND_PULLBACK_RECLAIM.",
        f"- Entry begins on the next US cash session, expires after "
        f"{int((cfg.get('execution') or {}).get('entry_valid_sessions', 3))} sessions, "
        "and rejects gaps beyond the configured ATR chase limit.",
        "- Risk-on allows both setups; neutral allows half-size pullback/reclaim only; "
        "risk-off blocks new longs.",
        "- Earnings, legal/dilution/delisting/FDA risk, stale/missing data, sector trend, "
        "SPY/sector relative strength, weekly trend, and gap risk are deterministic gates.",
        "- Stop and target fills are gap-aware; same-bar ambiguity is stop-first.",
        "- Net USD PnL is authoritative; fees and slippage remain separate.",
        "",
        "## Readiness",
        "",
        f"- verdict: **{ready['verdict']}**",
        f"- candidates: {ready['candidate_count']}; clean closed: {ready['clean_closed']}; "
        f"pending: {ready['pending']}; no-entry: {ready['no_entry']}",
        f"- forward days: {ready['forward_days']}; net USD: ${ready['net_pnl_usd']:.2f}; "
        f"PF: {_fmt(ready['profit_factor'], 3)}; winrate: {_fmt(ready['winrate'], 3)}",
        f"- max drawdown: ${ready['max_drawdown_usd']:.2f} "
        f"({_fmt(ready['max_drawdown_pct'], 2)}% of model equity); "
        f"drawdown gate: {ready['drawdown_ok']}",
        f"- clean closed by setup: `{json.dumps(ready['by_setup'], sort_keys=True)}`",
        "",
    ]
    if rejection_counts:
        lines += [
            "## Latest rejection reasons",
            "",
            "| Reason | Count |",
            "|---|---:|",
        ]
        lines.extend(
            f"| {reason} | {count} |"
            for reason, count in sorted(
                rejection_counts.items(), key=lambda item: item[1], reverse=True
            )
        )
        lines.append("")

    lines += [
        "## Candidates",
        "",
        "| ID | Symbol | Setup | Regime | Score | Entry | Stop | TP1 | TP2 | Risk $ | Size | Status |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in candidates:
        lines.append(
            f"| {row['candidate_id']} | {row['symbol']} | {row['setup_variant']} | "
            f"{row.get('market_regime') or '-'} | {_fmt(row.get('score'), 0)} | "
            f"{_fmt(row.get('entry_price'))} | {_fmt(row.get('stop_price'))} | "
            f"{_fmt(row.get('tp1'))} | {_fmt(row.get('tp2'))} | "
            f"{_fmt(row.get('risk_usd'))} | {_fmt(row.get('size_weight'))} | "
            f"{row.get('status')} |"
        )
    if not candidates:
        lines.append("| - | - | - | - | - | - | - | - | - | - | - | no candidates yet |")

    lines += [
        "",
        "## Outcomes",
        "",
        "| Candidate | Symbol | Setup | Status | Net $ | Fees $ | Slip $ | MFE R | MAE R | Gap R | Clean |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in outcomes:
        lines.append(
            f"| {row['candidate_id']} | {row.get('symbol')} | {row.get('setup_variant')} | "
            f"{row.get('status')} | {_fmt(row.get('net_pnl_usd'))} | "
            f"{_fmt(row.get('fees_usd'))} | {_fmt(row.get('slippage_usd'))} | "
            f"{_fmt(row.get('max_favorable_excursion_r'))} | "
            f"{_fmt(row.get('max_adverse_excursion_r'))} | {_fmt(row.get('gap_loss_r'))} | "
            f"{bool(row.get('data_clean'))} |"
        )
    if not outcomes:
        lines.append("| - | - | - | pending | - | - | - | - | - | - | - |")

    lines += [
        "",
        "## Evidence gate",
        "",
        "- Minimum 28 forward days.",
        "- Minimum 30 clean closed trades and 10 per setup.",
        "- Positive net USD PnL and PF >= 1.25.",
        "- Maximum drawdown no greater than 8% of model equity.",
        "- No automatic promotion. A passing gate remains REVIEW_ONLY until manual review.",
        "",
        "## Advisory reviews",
        "",
        "| Candidate | Cycle | Verdict | Confidence |",
        "|---|---|---|---:|",
    ]
    for row in reviews:
        lines.append(
            f"| {row['candidate_id']} | {row['review_cycle']} | {row['verdict']} | "
            f"{_fmt(row.get('confidence'), 2)} |"
        )
    if not reviews:
        lines.append("| - | - | no reviews yet | - |")
    lines.append("")
    return "\n".join(lines)


def write_report(markdown: str, path: str | Path | None = None) -> Path:
    target = Path(path) if path else REPORT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(markdown, encoding="utf-8")
    return target


def ascii_summary(cfg: dict[str, Any], *, db_path=None) -> str:
    ready = v2_store.readiness(cfg, db_path=db_path)
    return (
        "Stocks Position Swing V2 -- SHADOW ONLY\n"
        f"  candidates={ready['candidate_count']} clean_closed={ready['clean_closed']} "
        f"pending={ready['pending']} no_entry={ready['no_entry']}\n"
        f"  net_usd={ready['net_pnl_usd']:.2f} PF={ready['profit_factor']} "
        f"winrate={ready['winrate']} forward_days={ready['forward_days']}\n"
        f"  verdict={ready['verdict']} no_auto_promotion=true"
    )
