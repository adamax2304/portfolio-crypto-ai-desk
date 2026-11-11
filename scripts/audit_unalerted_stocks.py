"""One-off analysis: classify unalerted A/B stocks signals.

Read-only. No mutation. No Telegram. Prints a JSON-ish report that the
caller writes into UNALERTED_STOCKS_SIGNALS_AUDIT.md.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from src.config import load_config
from src.storage.sqlite import SQLiteStore


def main() -> None:
    config = load_config()
    db = SQLiteStore(config.db_path)
    db.init_db()
    now = datetime.now(timezone.utc)

    with db.connect() as conn:
        ab_rows = [
            dict(r)
            for r in conn.execute(
                """
                SELECT * FROM proposed_signals
                WHERE asset_class = 'stocks' AND tier IN ('A','B')
                ORDER BY created_at ASC
                """
            ).fetchall()
        ]
        alerted_signal_ids = {
            r["signal_id"]
            for r in conn.execute(
                "SELECT DISTINCT signal_id FROM signal_alerts "
                "WHERE asset_class = 'stocks'"
            ).fetchall()
        }
        # Setup-level alerts (any alert for this symbol/mode/direction).
        setup_alerts = [
            dict(r)
            for r in conn.execute(
                """
                SELECT symbol, mode, direction, MIN(sent_at) AS first_sent_at,
                       MAX(sent_at) AS last_sent_at, COUNT(*) AS n
                FROM signal_alerts
                WHERE asset_class = 'stocks'
                GROUP BY symbol, mode, direction
                """
            ).fetchall()
        ]
    setup_alert_index = {
        (r["symbol"], r["mode"], r["direction"]): r for r in setup_alerts
    }

    # Active vs closed.
    closed_statuses = {"stopped", "expired", "missed_no_entry"}
    active_statuses = {"generated", "waiting_for_entry", "triggered",
                       "tp1_hit", "tp2_hit"}

    # Group active signals by (symbol, mode, direction) so we can detect
    # supersession — multiple registry rows for the SAME setup, with
    # only the newest one being "current".
    by_setup: dict[tuple[str, str, str], list[dict]] = {}
    for row in ab_rows:
        key = (
            str(row.get("symbol") or ""),
            str(row.get("mode") or ""),
            str(row.get("direction") or ""),
        )
        by_setup.setdefault(key, []).append(row)
    # Sort each group newest first.
    for group in by_setup.values():
        group.sort(key=lambda r: r.get("created_at") or "", reverse=True)

    classification = {
        "unalerted_by_signal_id": [],     # not in signal_alerts by signal_id
        "unalerted_no_setup_alert": [],   # no prior alert for setup either
        "missing_invalidation": [],
        "closed_or_expired": [],
        "superseded_by_newer": [],
        "duplicate_of_alerted_setup": [],
        "active_valid_never_alerted_eligible": [],
    }
    summary = {
        "total_ab_stocks": len(ab_rows),
        "alerted_by_signal_id": 0,
        "unalerted_by_signal_id": 0,
        "active_valid_never_alerted_eligible_count": 0,
    }

    for row in ab_rows:
        sig_id = row.get("signal_id")
        status = str(row.get("status") or "").lower()
        sym = str(row.get("symbol") or "")
        mode = str(row.get("mode") or "")
        dirn = str(row.get("direction") or "")
        tier = str(row.get("tier") or "")
        score = row.get("score")
        inv = row.get("invalidation")
        created_at = row.get("created_at") or ""
        expires_at = row.get("expires_at") or ""

        age_hours = None
        try:
            dt = datetime.fromisoformat(str(created_at).replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            age_hours = (now - dt).total_seconds() / 3600.0
        except Exception:
            pass

        is_alerted = sig_id in alerted_signal_ids
        setup_key = (sym, mode, dirn)
        setup_alert = setup_alert_index.get(setup_key)

        if is_alerted:
            summary["alerted_by_signal_id"] += 1
            continue

        summary["unalerted_by_signal_id"] += 1
        item = {
            "signal_id": sig_id,
            "symbol": sym, "tier": tier, "mode": mode, "direction": dirn,
            "score": score, "status": status,
            "created_at": created_at,
            "expires_at": expires_at,
            "age_hours": round(age_hours, 1) if age_hours is not None else None,
            "invalidation": inv,
        }
        classification["unalerted_by_signal_id"].append(item)

        # Missing invalidation.
        if inv in (None, "", 0, 0.0):
            classification["missing_invalidation"].append(item)
            continue

        # Closed / expired.
        if status in closed_statuses:
            classification["closed_or_expired"].append(item)
            continue

        # Superseded? A newer signal exists for the same setup that is
        # active and ranked at least as high.
        group = by_setup.get(setup_key, [])
        newer_in_group = [g for g in group if (g.get("created_at") or "") >
                          (created_at or "") and g.get("signal_id") != sig_id]
        if newer_in_group:
            classification["superseded_by_newer"].append({
                **item,
                "newer_signal_id": newer_in_group[0].get("signal_id"),
                "newer_created_at": newer_in_group[0].get("created_at"),
                "newer_status": newer_in_group[0].get("status"),
            })
            continue

        # Setup already alerted (different signal_id, same symbol/mode/dir).
        if setup_alert:
            classification["duplicate_of_alerted_setup"].append({
                **item,
                "setup_first_alert_at": setup_alert.get("first_sent_at"),
                "setup_alert_count": setup_alert.get("n"),
            })
            continue

        # No prior alert for setup either — never told the user about
        # this idea, in any form.
        classification["unalerted_no_setup_alert"].append(item)

        # Eligible for a one-time initial alert if: active status,
        # has invalidation, A/B tier (already filtered), and no setup-
        # level alert.
        if status in active_statuses:
            classification["active_valid_never_alerted_eligible"].append(item)
            summary["active_valid_never_alerted_eligible_count"] += 1

    out = {
        "summary": summary,
        "classification": classification,
    }
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
