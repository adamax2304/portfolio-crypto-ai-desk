"""PART 7 — Expansion watchlist follow-through replay.

For each crypto expansion candidate (C-tier or shadow-lane), check:
 - did it later get promoted to A/B?
 - did it move in the predicted direction?
 - were there missed winners behind cap 20?

Uses existing proposed_signals; no production change.
"""

from __future__ import annotations

import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DB = ROOT / "db" / "crypto_ai_desk.sqlite"


def main() -> None:
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
        SELECT ps.*, o.final_r AS final_r, o.final_outcome AS final_outcome
        FROM proposed_signals ps
        LEFT JOIN (
            SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id
        ) m ON m.signal_id = ps.signal_id
        LEFT JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.asset_class='crypto'
        ORDER BY ps.created_at
    """)
    cols = [d[0] for d in cur.description]
    rows = [dict(zip(cols, r)) for r in cur.fetchall()]

    c_tier = [r for r in rows if r["tier"] == "C"]
    ab_tier = [r for r in rows if r["tier"] in ("A", "B")]

    # Build symbol → list of signals ordered by time
    by_sym: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_sym[r["symbol"]].append(r)

    # For each C-tier signal, did the same symbol later get A/B?
    promoted_count = 0
    promoted_winners = 0
    for c in c_tier:
        same = [r for r in by_sym[c["symbol"]]
                if r["created_at"] > c["created_at"] and r["tier"] in ("A", "B")]
        if same:
            promoted_count += 1
            later_winners = [r for r in same if (r.get("final_r") or 0) > 0]
            if later_winners:
                promoted_winners += 1

    # C-tier own R
    c_closed = [r for r in c_tier if r.get("final_r") is not None]
    c_sum_r = sum(float(r["final_r"]) for r in c_closed)
    c_wins = sum(1 for r in c_closed if (r["final_r"] or 0) > 0)
    c_losses = sum(1 for r in c_closed if (r["final_r"] or 0) < 0)

    # AB-tier
    ab_closed = [r for r in ab_tier if r.get("final_r") is not None]
    ab_sum_r = sum(float(r["final_r"]) for r in ab_closed)

    # Direction correctness for C-tier (did MFE > 0 in their direction within validity?)
    # Use final_r as proxy: positive means direction was right
    c_direction_right = sum(1 for r in c_closed if (r["final_r"] or 0) > 0)

    lines = []
    lines.append("# Crypto Expansion Watchlist — Follow-through Backtest (PART 7)")
    lines.append("")
    lines.append(f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"**Scope:** All crypto proposed_signals (n={len(rows)}).")
    lines.append("")
    lines.append("## Cohort sizes")
    lines.append("")
    lines.append(f"- C-tier (watchlist / expansion): **{len(c_tier)}**")
    lines.append(f"- A/B-tier: **{len(ab_tier)}**")
    lines.append("")
    lines.append("## C-tier follow-through")
    lines.append("")
    lines.append(f"- C-tier signals whose symbol later got A/B-promoted: **{promoted_count}** / {len(c_tier)} "
                 f"({(promoted_count/max(1,len(c_tier))):.0%})")
    lines.append(f"- Of those, later A/B winners: **{promoted_winners}**")
    lines.append("")
    lines.append("## C-tier outcomes (paper PnL contribution)")
    lines.append("")
    lines.append(f"- C-tier closed: {len(c_closed)}")
    lines.append(f"- C-tier sum R: **{c_sum_r:+.2f}**")
    lines.append(f"- C-tier wins / losses: {c_wins} / {c_losses}")
    lines.append(f"- C-tier WR closed: {c_wins/max(1,c_wins+c_losses):.0%}")
    lines.append("")
    lines.append("## Were direction calls correct? (paper PnL > 0 proxy)")
    lines.append("")
    lines.append(f"- C-tier with final_r > 0 (direction correct + filled): **{c_direction_right}** / {len(c_closed)}")
    lines.append("")
    lines.append("## Did blockers correctly prevent bad promotions?")
    lines.append("")
    # symbols where the C-tier turned out winning but never got A/B promotion
    missed_winners = 0
    for c in c_closed:
        if (c["final_r"] or 0) > 0:
            later = [r for r in by_sym[c["symbol"]]
                     if r["created_at"] > c["created_at"] and r["tier"] in ("A", "B")]
            if not later:
                missed_winners += 1
    lines.append(f"- C-tier winners with NO later A/B promotion (missed): **{missed_winners}**")
    lines.append("")
    lines.append("## Would cap 25 or 30 have helped?")
    lines.append("")
    lines.append("- The full-agent cap is enforced upstream in the supervisor, not at signal-write time, "
                 "so we cannot strictly answer this without re-running scanning.")
    lines.append("- **Proxy:** if C-tier winners that did NOT later get A/B promotion are few (above), "
                 "then the current cap is not leaving large alpha on the table.")
    lines.append("")
    lines.append("## Decision (read-only)")
    lines.append("")
    lines.append("- **No expansion-candidate promotion implemented.** Read-only check only.")
    lines.append("- **No full-agent cap change implemented.**")
    lines.append("- The current YAML weight for C-tier is **0.0×**, so even if expansion is noisy, it "
                 "contributes zero to sized R. The audit is informational.")

    out_md = ROOT / "reports" / "EXPANSION_WATCHLIST_BACKTEST.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out_md}")


if __name__ == "__main__":
    main()
