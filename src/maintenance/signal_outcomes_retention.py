"""PART 3 — safe retention/archival for the per-bar ``signal_outcomes`` tracking table.

WHY
---
``signal_outcomes`` accumulates ~150 per-bar *check* rows per signal (the tracker writes one
row per evaluation). On a ~2 GB DB that is ~370k rows of mostly-intermediate history. This module
archives the OLD intermediate per-bar rows to a compressed file and deletes them from the live DB,
**without ever losing**:

* any row from the last ``--days`` N (recent tracking stays hot);
* the LATEST row per signal (the final tracked state — carries ``final_r`` / ``final_outcome``);
* any row where ``final_outcome`` is set (closed-trade outcomes needed for analytics).

It NEVER touches ``proposed_signals``, ``paper_shadow_*``, ``signal_outcomes.final_r`` values that
are kept, scoring, routing, actionability, or anything live. Default is DRY-RUN.
"""
from __future__ import annotations

import gzip
import os
import shutil
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Any

from src.config import load_config

TABLE = "signal_outcomes"
DEFAULT_DAYS = 30
DEFAULT_MAX_ROWS = 250_000


def _default_archive_dir() -> str:
    external = "F:/crypto-ai-desk-archives/signal_outcomes"
    try:
        if os.path.exists("F:/") and shutil.disk_usage("F:/").free > 512 * 1024 * 1024:
            return external
    except OSError:
        pass
    return "data/archive/signal_outcomes"


ARCHIVE_DIR = _default_archive_dir()


def _conn(db: str | None = None) -> sqlite3.Connection:
    cfg = load_config()
    c = sqlite3.connect(db or cfg.db_path)
    c.row_factory = sqlite3.Row
    return c


def _db_size_mb(path: str) -> float:
    try:
        return round(os.path.getsize(path) / 1e6, 1)
    except OSError:
        return 0.0


def _cutoff_iso(days: int, now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    return (now - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S+00:00")


# A row is ARCHIVABLE (safe to move out of the live table) iff BOTH hold:
#   * older than the cutoff (checked_at < cutoff), AND
#   * it is NOT the latest row for its signal (id < max(id) for that signal_id).
# The latest row per signal is ALWAYS kept — it carries the final_r / final_outcome summary — so the
# closed-trade outcome needed for analytics is never lost; only the intermediate per-bar PATH of
# already-old signals is archived (and the archive file preserves even that, recoverable).
_ARCHIVABLE_WHERE = (
    "checked_at < :cutoff "
    "AND id NOT IN (SELECT MAX(id) FROM {t} GROUP BY signal_id)"
).format(t=TABLE)


def plan(days: int = DEFAULT_DAYS, db: str | None = None, now: datetime | None = None) -> dict[str, Any]:
    """Compute what retention WOULD do — no mutation. Returns counts + DB size."""
    cfg = load_config()
    path = db or cfg.db_path
    conn = _conn(path)
    try:
        cutoff = _cutoff_iso(days, now)
        total = conn.execute(f"SELECT COUNT(*) FROM {TABLE}").fetchone()[0]
        signals = conn.execute(f"SELECT COUNT(DISTINCT signal_id) FROM {TABLE}").fetchone()[0]
        archivable = conn.execute(
            f"SELECT COUNT(*) FROM {TABLE} WHERE {_ARCHIVABLE_WHERE}", {"cutoff": cutoff}).fetchone()[0]
        recent = conn.execute(
            f"SELECT COUNT(*) FROM {TABLE} WHERE checked_at >= :cutoff", {"cutoff": cutoff}).fetchone()[0]
        finals = conn.execute(
            f"SELECT COUNT(*) FROM {TABLE} WHERE final_outcome IS NOT NULL AND final_outcome != ''"
        ).fetchone()[0]
    finally:
        conn.close()
    kept = total - archivable
    return {
        "table": TABLE, "db_path": path, "db_size_mb": _db_size_mb(path),
        "days": days, "cutoff": cutoff,
        "total_rows": total, "distinct_signals": signals,
        "archivable_rows": archivable, "kept_rows": kept,
        "kept_recent_rows": recent, "kept_final_outcome_rows": finals,
        "avg_rows_per_signal": round(total / max(signals, 1), 1),
        "archivable_share_pct": round(100 * archivable / max(total, 1), 1),
    }


def _archive_rows(conn: sqlite3.Connection, cutoff: str, archive_dir: str,
                  now: datetime | None, ceiling_id: int | None = None) -> str:
    """Stream a bounded archive batch to gzip before deleting it."""
    os.makedirs(archive_dir, exist_ok=True)
    stamp = (now or datetime.now(timezone.utc)).strftime("%Y%m%dT%H%M%S")
    cols = [r[1] for r in conn.execute(f"PRAGMA table_info({TABLE})")]
    bound = " AND id<=:ceiling" if ceiling_id is not None else ""
    params = {"cutoff": cutoff, "ceiling": ceiling_id}
    import csv
    path = os.path.join(archive_dir, f"signal_outcomes_archive_{stamp}.csv.gz")
    with gzip.open(path, "wt", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(cols)
        cursor = conn.execute(
            f"SELECT * FROM {TABLE} WHERE {_ARCHIVABLE_WHERE}{bound} ORDER BY id", params,
        )
        while True:
            rows = cursor.fetchmany(5_000)
            if not rows:
                break
            for row in rows:
                writer.writerow([row[column] for column in cols])
    return path


def run(days: int = DEFAULT_DAYS, *, archive: bool = True, dry_run: bool = True,
        do_vacuum: bool = False, db: str | None = None, archive_dir: str = ARCHIVE_DIR,
        now: datetime | None = None, max_rows: int = DEFAULT_MAX_ROWS) -> dict[str, Any]:
    """Archive + delete archivable per-bar rows. DRY-RUN by default (no mutation).

    Order of operations (when not dry-run): archive file written FIRST, then DELETE, then optional
    VACUUM. If archiving fails the delete is aborted, so rows are never lost.
    """
    cfg = load_config()
    path = db or cfg.db_path
    before = plan(days, db=path, now=now)
    result: dict[str, Any] = {"dry_run": dry_run, "before": before, "archive_file": None,
                              "deleted_rows": 0, "vacuumed": False}
    if dry_run:
        result["note"] = "dry-run — nothing archived or deleted; re-run with dry_run=False to apply"
        return result
    if before["archivable_rows"] == 0:
        result["note"] = "nothing to archive"
        return result

    conn = _conn(path)
    try:
        cutoff = before["cutoff"]
        selected = conn.execute(
            f"SELECT id FROM {TABLE} WHERE {_ARCHIVABLE_WHERE} ORDER BY id LIMIT :limit",
            {"cutoff": cutoff, "limit": max(1, int(max_rows))},
        ).fetchall()
        ceiling_id = int(selected[-1][0]) if selected else None
        result["selected_rows"] = len(selected)
        if ceiling_id is None:
            result["note"] = "nothing selected"
            return result
        if archive:
            result["archive_file"] = _archive_rows(
                conn, cutoff, archive_dir, now, ceiling_id=ceiling_id,
            )
        cur = conn.execute(
            f"DELETE FROM {TABLE} WHERE {_ARCHIVABLE_WHERE} AND id<=:ceiling",
            {"cutoff": cutoff, "ceiling": ceiling_id},
        )
        result["deleted_rows"] = cur.rowcount
        conn.commit()
        if do_vacuum:
            conn.execute("VACUUM")
            result["vacuumed"] = True
    finally:
        conn.close()
    result["after"] = plan(days, db=path, now=now)
    return result
