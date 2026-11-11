"""PART 2 — Expired positive-MFE monitor.

Find every triggered A/B signal that expired flat after reaching positive MFE.
Classify by MFE bucket, estimate partial-TP value, estimate winner-cut cost.

Read-only.
"""

from __future__ import annotations

import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DB = ROOT / "db" / "crypto_ai_desk.sqlite"


def main() -> None:
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row

    rows = con.execute("""
        SELECT ps.asset_class, ps.mode, ps.tier, ps.direction, ps.symbol,
               o.final_outcome, o.final_r,
               o.max_favorable_excursion_r AS mfe,
               o.max_adverse_excursion_r AS mae,
               o.entry_triggered, o.entry_triggered_at,
               ps.tp1, ps.tp2, ps.tp3, ps.stop_loss, ps.invalidation,
               ps.created_at
        FROM proposed_signals ps
        JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.tier IN ('A','B') AND o.entry_triggered = 1
    """).fetchall()

    # Expired with positive MFE
    exp_pos = [r for r in rows
               if r["final_outcome"] == "expired" and (r["mfe"] or 0) > 0.05]
    # Buckets
    buckets = {"0-0.3R": 0, "0.3-0.5R": 0, "0.5-0.7R": 0, "0.7-1R": 0, ">=1R": 0}
    for r in exp_pos:
        m = float(r["mfe"] or 0)
        if m < 0.3: buckets["0-0.3R"] += 1
        elif m < 0.5: buckets["0.3-0.5R"] += 1
        elif m < 0.7: buckets["0.5-0.7R"] += 1
        elif m < 1.0: buckets["0.7-1R"] += 1
        else: buckets[">=1R"] += 1

    # Hypothetical partial-TP @ +0.5R, 50% off
    partial_05_uplift = sum(0.5 * 0.5 for r in exp_pos if (r["mfe"] or 0) >= 0.5)
    # Partial @ +0.3R 50% off
    partial_03_uplift = sum(0.3 * 0.5 for r in exp_pos if (r["mfe"] or 0) >= 0.3)

    # Winner cut risk: among trades that went to a clean TP win (final_r >= 0.8),
    # how many would have had 50% closed prematurely at +0.5R?
    winners = [r for r in rows
               if r["final_outcome"] == "win" and (r["final_r"] or 0) > 0.8]
    cut_winners = [r for r in winners if (r["mfe"] or 0) >= 0.5]
    cut_cost = sum(0.5 * ((r["final_r"] or 0) - 0.5) for r in cut_winners)

    # Trade later reversed to stop zone? (proxy: mae < -0.8)
    later_reversed = sum(1 for r in exp_pos if (r["mae"] or 0) < -0.8)

    out = []
    out.append("# Expired Positive-MFE Opportunity Audit (PART 2)")
    out.append("")
    out.append(f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    out.append(f"**Scope:** A/B triggered signals where `final_outcome='expired'` and MFE > +0.05R.")
    out.append("")
    out.append("## Headline")
    out.append("")
    out.append(f"- Triggered A/B trades total: **{len(rows)}**")
    out.append(f"- Expired with positive MFE > +0.05R: **{len(exp_pos)}** ({len(exp_pos)/max(1,len(rows)):.1%})")
    out.append(f"- Of those, MFE later reversed to deeply adverse (MAE < −0.8R): **{later_reversed}**")
    out.append("")
    out.append("## MFE bucket distribution")
    out.append("")
    out.append("| MFE bucket | n |")
    out.append("|---|---:|")
    for k, n in buckets.items():
        out.append(f"| {k} | {n} |")
    out.append("")
    out.append("## Hypothetical partial-TP uplift")
    out.append("")
    out.append("| Policy | Naive uplift | Caveat |")
    out.append("|---|---:|---|")
    out.append(f"| 50% close @ +0.3R | **{partial_03_uplift:+.1f}R** | catches more trades but each contributes only +0.15R |")
    out.append(f"| 50% close @ +0.5R | **{partial_05_uplift:+.1f}R** | catches fewer trades but each contributes +0.25R |")
    out.append("")
    out.append("## Winner-cut risk")
    out.append("")
    out.append(f"- Full winners (final_r > +0.8R): **{len(winners)}**")
    out.append(f"- Of those, MFE ≥ +0.5R BEFORE final TP: **{len(cut_winners)}** would have had 50% closed at +0.5R")
    out.append(f"- Estimated winner cut cost (50% × (final_r − 0.5R)): **{cut_cost:.1f}R**")
    out.append("")
    out.append("## Net of partial-TP @ +0.5R")
    out.append("")
    out.append(f"- Naive uplift: **+{partial_05_uplift:.1f}R**")
    out.append(f"- Naive cost: **−{cut_cost:.1f}R**")
    net = partial_05_uplift - cut_cost
    out.append(f"- **Net: {net:+.1f}R** across all A/B triggered trades over 20 days")
    out.append("")
    out.append("## Interpretation")
    out.append("")
    if net > 5:
        out.append(f"- Partial-TP @ +0.5R *could* add ~{net:+.1f}R over the 20-day sample. Material but needs walk-forward validation before any production change.")
    elif net > 0:
        out.append(f"- Partial-TP @ +0.5R is roughly **neutral**: +{net:.1f}R is within sample noise.")
    else:
        out.append(f"- Partial-TP @ +0.5R would have **lost** {-net:.1f}R net by cutting winners short.")
    out.append("")
    out.append("**No TP change is implemented.** This is research only.")

    out_md = ROOT / "reports" / "EXPIRED_POSITIVE_MFE_OPPORTUNITY_AUDIT.md"
    out_md.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {out_md}")


if __name__ == "__main__":
    main()
