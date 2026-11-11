"""Sector-cap would-bind forward tracker (operational deploy PART 5).

Read-only. Reads stocks-intraday paper_entry alerts from signal_alerts.payload_json
over a window, tallies would_bind_sector_cap vs actual_concentration_status, joins
realized R, and writes reports/SECTOR_CAP_WOULD_BIND_FORWARD_TRACKER.md. No behavior
change — pure forward measurement of the shadow cap.
"""
from __future__ import annotations

import json
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DB = ROOT / "db" / "crypto_ai_desk.sqlite"
OUT = ROOT / "reports" / "SECTOR_CAP_WOULD_BIND_FORWARD_TRACKER.md"
WINDOW_DAYS = 14

BIND = {"shadow_sector_cap", "half_size", "shadow_proxy_duplicate"}


def main():
    now = datetime.now(timezone.utc)
    since = (now - timedelta(days=WINDOW_DAYS)).isoformat()
    conn = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT signal_id, symbol, sent_at, payload_json FROM signal_alerts "
        "WHERE asset_class='stocks' AND alert_type='paper_entry' AND sent_at >= ? "
        "ORDER BY sent_at ASC", (since,),
    ).fetchall()

    would = Counter()
    actual = Counter()
    would_bind_ids = []
    for r in rows:
        try:
            p = json.loads(r["payload_json"] or "{}")
        except Exception:
            continue
        wb = p.get("would_bind_sector_cap")
        ac = p.get("actual_concentration_status") or p.get("concentration_status")
        if wb:
            would[wb] += 1
            if wb in BIND:
                would_bind_ids.append((r["signal_id"], r["symbol"], wb,
                                       p.get("would_sector_bucket")))
        if ac:
            actual[ac] += 1

    # realized R of would-bound names
    net_r = 0.0
    rcount = 0
    for sid, *_ in would_bind_ids:
        o = conn.execute(
            "SELECT final_r FROM signal_outcomes WHERE signal_id=? "
            "AND final_outcome IN ('win','loss','partial_win') "
            "ORDER BY id DESC LIMIT 1", (sid,)).fetchone()
        if o and o["final_r"] is not None:
            net_r += float(o["final_r"]); rcount += 1
    conn.close()

    n_would_bind = sum(would[k] for k in BIND)
    n_actual_bind = sum(actual[k] for k in BIND)
    lines = [
        "# Sector-Cap Would-Bind — Forward Tracker (PART 5)", "",
        f"**Window:** last {WINDOW_DAYS}d (since {since[:10]}) · stocks-intraday paper_entry alerts: {len(rows)}",
        f"**Min forward window before any decision:** 10 trading days.", "",
        "## Would-bind (shadow day-batch cap) vs actual (live per-signal cap)",
        f"- **Would bind** (half/shadow): **{n_would_bind}**",
        f"- **Actually bound live**: **{n_actual_bind}**",
        f"- Gap (would − actual): **{n_would_bind - n_actual_bind}** ← the inert-live discrepancy",
        "",
        "### would_bind_sector_cap distribution",
    ]
    for k, v in would.most_common():
        lines.append(f"- {k}: {v}")
    if not would:
        lines.append("- (no would_bind data yet — accumulates as new stocks-intraday alerts fire)")
    lines += [
        "", "### actual concentration_status distribution",
    ]
    for k, v in actual.most_common():
        lines.append(f"- {k}: {v}")
    if not actual:
        lines.append("- (none yet)")
    lines += [
        "", "## Net R of would-bound names (outcome so far)",
        f"- would-bound names with a closed outcome: **{rcount}**",
        f"- net realized R of those names: **{round(net_r, 2)}R**",
        "  - if strongly negative → the shadow cap is targeting the losers (would help).",
        "  - if positive → the cap would clip winners (do NOT enable).",
        "",
        "## Decision gate",
        "Collect ≥10 trading days. Enable a batch-aware LIVE cap (still paper, with explicit "
        "approval) ONLY if would-bound names are net-negative AND the cap does not clip "
        "net-positive clusters. Until then: shadow-only, cap value unchanged.",
        "",
        "_Read-only forward measurement. No routing/size/cap-value change._",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} · alerts={len(rows)} · would_bind={n_would_bind} actual_bind={n_actual_bind}")


if __name__ == "__main__":
    main()
