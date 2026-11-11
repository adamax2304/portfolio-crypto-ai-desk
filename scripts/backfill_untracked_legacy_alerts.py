"""Backfill untracked legacy watchlist_alerts into proposed_signals.

PART 1 fix companion: for the 4 known untracked crypto alerts on 2026-05-29
(UNI/BCH/XLM/INJ), and any other A/B watchlist_alerts that lack a paired
proposed_signal, reconstruct a ``TradeIdea`` from the stored ``payload_json``
and register it via ``signals.registry.register_ideas``.

- Idempotent: ``upsert_proposed_signal`` dedupes by ``signal_id``, so running
  twice is safe.
- Uses the ORIGINAL ``sent_at`` for ``created_at`` so the validity window
  reflects when the alert was sent, not when this script ran.
- Writes ``signal_id`` back into the alert's ``payload_json`` for traceability.
- Pure backfill — no Telegram sends, no scoring/threshold changes.

Usage::

    python -m scripts.backfill_untracked_legacy_alerts --since 2026-05-29
    python -m scripts.backfill_untracked_legacy_alerts --since 2026-05-29 --dry-run
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.config import load_config
from src.models import TradeIdea
from src.signals.config import load_signal_tracking_config
from src.signals.registry import build_signal_from_idea
from src.storage.sqlite import SQLiteStore


def _row_to_idea(row: sqlite3.Row) -> TradeIdea | None:
    payload = json.loads(row["payload_json"] or "{}")
    if not payload or "symbol" not in payload:
        return None
    try:
        return TradeIdea(**payload)
    except Exception as exc:  # pragma: no cover — invalid stored payload
        print(f"  [warn] cannot rebuild TradeIdea for {row['symbol']}: {exc}")
        return None


def _already_tracked(db: SQLiteStore, signal_id: str) -> bool:
    with db.connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM proposed_signals WHERE signal_id = ? LIMIT 1",
            (signal_id,),
        ).fetchone()
    return row is not None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--since",
        type=str,
        default="2026-05-29",
        help="Only backfill alerts sent on/after this UTC date (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be inserted without writing.",
    )
    args = parser.parse_args()

    config = load_config()
    db = SQLiteStore(config.db_path)
    tracking = load_signal_tracking_config(config.root)
    if not tracking.enabled:
        print("signal tracking disabled — nothing to do.")
        return 0

    with db.connect() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT id, sent_at, symbol, previous_tier, new_tier, score,
                   direction, mode, asset_class, payload_json
              FROM watchlist_alerts
             WHERE sent_at >= ?
               AND new_tier IN ('A','B')
               AND direction IN ('long','short')
             ORDER BY sent_at
            """,
            (f"{args.since}T00:00:00+00:00",),
        ).fetchall()

    print(f"scanning {len(rows)} A/B watchlist_alerts since {args.since}")
    inserted = 0
    already = 0
    skipped = 0
    for row in rows:
        idea = _row_to_idea(row)
        if idea is None:
            skipped += 1
            continue
        # Reconstruct signal with the alert's original sent_at as created_at
        # so the validity window reflects reality.
        created_at = str(row["sent_at"])
        try:
            signal = build_signal_from_idea(
                idea,
                config=tracking,
                report_id=f"backfill-watchlist-{row['id']}",
                market_regime="",
                weekend_mode_active=False,
                created_at=created_at,
                asset_class=row["asset_class"] or "crypto",
            )
        except Exception as exc:
            print(f"  [warn] build_signal_from_idea failed for {row['symbol']}: {exc}")
            skipped += 1
            continue
        if signal is None:
            print(f"  [skip] {row['symbol']} {row['new_tier']} {row['direction']} — does not qualify")
            skipped += 1
            continue

        if _already_tracked(db, signal.signal_id):
            already += 1
            continue

        if args.dry_run:
            print(
                f"  [dry-run] would insert {signal.signal_id} "
                f"({row['symbol']} {row['new_tier']} {row['direction']} "
                f"{row['mode']} sent_at={row['sent_at']})"
            )
            inserted += 1
            continue

        ok = db.upsert_proposed_signal(signal.to_row())
        if not ok:
            already += 1
            continue
        # Write signal_id back into the alert payload for traceability.
        payload = json.loads(row["payload_json"] or "{}")
        payload["signal_id"] = signal.signal_id
        payload["_backfilled_at"] = datetime.now(timezone.utc).isoformat()
        with db.connect() as conn:
            conn.execute(
                "UPDATE watchlist_alerts SET payload_json = ? WHERE id = ?",
                (json.dumps(payload), row["id"]),
            )
        inserted += 1
        print(
            f"  [insert] {signal.signal_id} "
            f"({row['symbol']} {row['new_tier']} {row['direction']} "
            f"{row['mode']} sent_at={row['sent_at']})"
        )

    print("---")
    print(f"inserted={inserted} already_tracked={already} skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
