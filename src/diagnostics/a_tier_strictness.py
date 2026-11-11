"""PART 5 — A-tier strictness diagnostic (READ-ONLY; never changes the threshold or any config).

A-tier requires ``score >= a_tier_threshold (=80) AND no cap reasons`` (scoring_agent). So A is rare
for two distinct reasons: (1) few signals reach 80, and (2) those that do are often *capped* (earnings
active / partial data / macro-event) and demoted. This diagnostic quantifies both so the operator can
see whether A-tier is "too strict" or "correctly rare" — WITHOUT touching the threshold.
"""
from __future__ import annotations

import sqlite3
from typing import Any

from src.config import load_config

A_TIER_THRESHOLD = 80.0   # scoring_agent default (config/stocks/scoring.yaml: a_tier=80)
OFFSETS = (0, -2, -5, -10)


def _conn(db: str | None = None) -> sqlite3.Connection:
    cfg = load_config()
    c = sqlite3.connect(db or cfg.db_path)
    c.row_factory = sqlite3.Row
    return c


def analyze(days: int = 30, db: str | None = None) -> dict[str, Any]:
    """Score distribution + would-be-A counts at threshold/-2/-5/-10 + cap-demotion gap.
    Optionally joins forward-shadow R for the high-score cohort if the shadow lane has rows."""
    conn = _conn(db)
    try:
        rows = [dict(r) for r in conn.execute(
            "SELECT signal_id, asset_class, tier, score FROM proposed_signals "
            "WHERE created_at >= datetime('now', ?) AND score IS NOT NULL",
            (f"-{days} day",)).fetchall()]
        # forward shadow net_r per signal (B branch) for the high-score cohort, if available
        shadow = {}
        try:
            for r in conn.execute(
                "SELECT signal_id, net_r FROM paper_shadow_execution_outcomes "
                "WHERE branch='new_logic_shadow' AND window='forward_since_activation' "
                "AND entry_fill_status='filled'"):
                shadow[r["signal_id"]] = (shadow.get(r["signal_id"], 0.0) + (r["net_r"] or 0))
        except sqlite3.OperationalError:
            pass
    finally:
        conn.close()

    def block(subset: list[dict]) -> dict:
        n = len(subset)
        actual_a = sum(1 for r in subset if r["tier"] == "A")
        thr_counts = {}
        for off in OFFSETS:
            thr = A_TIER_THRESHOLD + off
            ge = [r for r in subset if (r["score"] or 0) >= thr]
            capped = sum(1 for r in ge if r["tier"] != "A")   # >= threshold but NOT tier A => capped/demoted
            # forward shadow R for this cohort (where shadow rows exist)
            cohort_ids = [r["signal_id"] for r in ge if r["signal_id"] in shadow]
            shadow_r = round(sum(shadow[i] for i in cohort_ids), 2) if cohort_ids else None
            thr_counts[str(thr)] = {"would_be_A_by_score": len(ge), "actually_A": sum(1 for r in ge if r["tier"] == "A"),
                                    "demoted_by_caps": capped, "shadow_forward_R": shadow_r,
                                    "shadow_n": len(cohort_ids)}
        scores = sorted((r["score"] or 0) for r in subset)
        pctl = (lambda p: round(scores[min(len(scores) - 1, int(p * len(scores)))], 1)) if scores else (lambda p: None)
        return {"signals": n, "actual_A": actual_a, "actual_A_pct": round(100 * actual_a / n, 2) if n else 0.0,
                "score_p50": pctl(0.5), "score_p90": pctl(0.9), "score_max": round(max(scores), 1) if scores else None,
                "by_threshold": thr_counts}

    return {
        "days": days, "a_tier_threshold": A_TIER_THRESHOLD, "offsets": list(OFFSETS),
        "all": block(rows),
        "crypto": block([r for r in rows if r["asset_class"] == "crypto"]),
        "stocks": block([r for r in rows if r["asset_class"] == "stocks"]),
        "threshold_changed": False,
        "interpretation": ("A-tier rarity is driven by BOTH the >=80 bar AND the 'no caps' gate "
                           "(earnings/partial-data/macro demote high scorers). Lowering the bar alone "
                           "adds candidates that the cap gate still blocks — see demoted_by_caps."),
    }
