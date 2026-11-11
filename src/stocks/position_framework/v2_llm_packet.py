"""Read-only enriched-review packet for Stocks Position Swing V2."""
from __future__ import annotations

import json
from pathlib import Path

from . import v2_store
from .news_context import ticker_context
from .v2_config import ROOT, load_config

PACKET_PATH = ROOT / "data" / "processed" / "llm_stocks_position_swing_v2_packet.md"


def parse_reviews(text: str) -> list[dict]:
    from .llm_packet import parse_reviews as _parse_reviews

    return _parse_reviews(text)


def build_packet(project_config=None, *, limit: int = 12, db_path=None) -> str:
    cfg = load_config()
    candidates = [
        row for row in v2_store.latest_candidates(limit=100, db_path=db_path)
        if row.get("status") == "shadow_open"
    ][:limit]
    readiness = v2_store.readiness(cfg, db_path=db_path)
    lines = [
        "# Enriched Review: Stocks Position Swing V2",
        "",
        "> SHADOW ONLY. The review can only narrow or reject research candidates. "
        "It cannot change entry, stop, targets, score, Paper, or live routing.",
        "",
        f"- strategy: `{cfg.get('strategy_id')}`",
        f"- profile: `{cfg.get('profile_version')}`",
        f"- readiness: `{readiness['verdict']}`; clean closed={readiness['clean_closed']}; "
        f"net USD=${readiness['net_pnl_usd']:.2f}",
        "",
        "## Review instructions",
        "",
        "- Verify earnings timing, guidance, dilution/offering, SEC/legal/FDA risk, "
        "sector context, and whether the thesis remains current.",
        "- Use only information available at review time.",
        "- Verdicts: KEEP_TRACKING, WAIT, REJECT_EVENT_RISK, REJECT_THESIS_BROKEN, NEEDS_DATA.",
        "- Never improve entry geometry or override a deterministic rejection.",
        "- Return one JSON object per candidate with candidate_id, verdict, confidence, "
        "reasons, key_news, and risk_notes.",
        "- Ingest with `python -m src.cli ingest-stocks-position-v2-review --file <path>`; "
        "this writes only the isolated advisory review table.",
        "",
        "## Candidates",
        "",
    ]
    for candidate in candidates:
        context = ticker_context(
            candidate.get("symbol"), config=project_config, lookback_days=30
        )
        lines += [
            f"### {candidate['symbol']} | {candidate['setup_variant']} | `{candidate['candidate_id']}`",
            f"- regime={candidate.get('market_regime')} score={candidate.get('score')} "
            f"entry={candidate.get('entry_price')} stop={candidate.get('stop_price')}",
            f"- RS SPY={candidate.get('rs_spy')} RS sector={candidate.get('rs_sector')} "
            f"earnings_days={candidate.get('earnings_days')}",
            f"- event_types={candidate.get('event_types_json') or '[]'}",
            f"- thesis: {candidate.get('thesis')}",
            f"- counter-thesis: {candidate.get('counter_thesis')}",
        ]
        if context.get("lines"):
            lines.extend(f"- local context: {item}" for item in context["lines"])
        else:
            lines.append("- local context: no reliable ticker-specific rows")
        lines.append("")
    if not candidates:
        lines.append("_No open v2 candidates._")
    lines += [
        "",
        "```json",
        json.dumps(
            {
                "candidate_id": "spv2_SYMBOL_DATE_SETUP",
                "verdict": "KEEP_TRACKING",
                "confidence": 0.0,
                "reasons": [],
                "key_news": [],
                "risk_notes": [],
            },
            indent=2,
        ),
        "```",
        "",
    ]
    return "\n".join(lines)


def write_packet(project_config=None, *, limit: int = 12, db_path=None) -> Path:
    PACKET_PATH.parent.mkdir(parents=True, exist_ok=True)
    PACKET_PATH.write_text(
        build_packet(project_config, limit=limit, db_path=db_path),
        encoding="utf-8",
    )
    return PACKET_PATH
