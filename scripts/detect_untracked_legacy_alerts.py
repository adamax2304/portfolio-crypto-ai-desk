"""Read-only detector: legacy crypto alerts with no matching proposed_signal.

A crypto alert in ``watchlist_alerts`` is "untracked" when no row in
``proposed_signals`` shares its symbol within a small time window around the
alert. Such alerts went to Telegram but cannot contribute to signal-stats
(PF / winrate) because the tracker has nothing to follow.

Usage::

    python -m scripts.detect_untracked_legacy_alerts             # whole day
    python -m scripts.detect_untracked_legacy_alerts --since 2026-05-29

Prints a Markdown section that can be pasted into a cycle summary or the
final 12h review. Never writes to the DB. Never changes code.
"""

from __future__ import annotations

import argparse
import sqlite3
from datetime import datetime, timezone

from src.config import load_config

# How close (hours) a proposed_signal's created_at must be to the alert's
# sent_at, for the same symbol, to count as "matched".
MATCH_WINDOW_HOURS = 6.0


def _parse(ts: str) -> datetime | None:
    try:
        dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default=None, help="ISO date/time lower bound (UTC).")
    args = ap.parse_args()

    con = sqlite3.connect(load_config().db_path)
    con.row_factory = sqlite3.Row

    where = "WHERE asset_class='crypto'"
    params: list = []
    if args.since:
        where += " AND sent_at >= ?"
        params.append(args.since)

    alerts = con.execute(
        f"SELECT symbol, new_tier, score, direction, mode, sent_at "
        f"FROM watchlist_alerts {where} ORDER BY sent_at",
        params,
    ).fetchall()

    untracked: list[dict] = []
    for a in alerts:
        sent = _parse(a["sent_at"])
        sym = a["symbol"]
        # Look for any crypto proposed_signal for this symbol near the alert.
        rows = con.execute(
            "SELECT created_at FROM proposed_signals "
            "WHERE asset_class='crypto' AND symbol=?",
            (sym,),
        ).fetchall()
        matched = False
        for r in rows:
            ccreated = _parse(r["created_at"])
            if sent and ccreated and abs((sent - ccreated).total_seconds()) <= MATCH_WINDOW_HOURS * 3600:
                matched = True
                break
        if not matched:
            untracked.append({
                "symbol": sym, "tier": a["new_tier"], "mode": a["mode"],
                "score": a["score"], "direction": a["direction"],
                "sent_at": a["sent_at"],
            })

    # Emit Markdown.
    print("## Untracked Legacy Crypto Alerts")
    print()
    print(f"_Detector: watchlist_alerts (crypto) without a matching "
          f"proposed_signal within ±{MATCH_WINDOW_HOURS:.0f}h. Read-only._")
    print()
    if not untracked:
        print("- None. Every legacy crypto alert has a backing proposed_signal "
              "(or there were no crypto alerts).")
        return 0
    print("| symbol | tier | mode | score | direction | sent_at | trackable |")
    print("|--------|------|------|------:|-----------|---------|-----------|")
    for u in untracked:
        print(f"| {u['symbol']} | {u['tier']} | {u['mode']} | {u['score']} | "
              f"{u['direction']} | {u['sent_at']} | NO (no proposed_signal) |")
    print()
    print(f"**{len(untracked)} untracked legacy crypto alert(s).** These were "
          "sent to Telegram but will NOT contribute to PF / winrate / avgR "
          "because the tracker has no signal_id to follow.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
