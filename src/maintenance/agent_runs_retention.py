"""Retention for the heavy ``agent_runs.summary_json`` blob (the real DB disk hog: ~1.66 GB / 83% of
the 2 GB DB across ~107k LLM-run log rows).

``summary_json`` is **write-only** — it is INSERTed by the run logger and never SELECTed anywhere in
the codebase; the real artifact is the file at ``output_path``. So for OLD rows we archive the blob to
parquet and then NULL it, **keeping the metadata row** (id / agent_name / run_at / output_path /
asset_class) so the audit trail and the artifact pointer survive intact.

NEVER touches trading data: no scoring, no signals/outcomes, no `final_r`, no routing/actionability, no
live. Default is DRY-RUN. Reclaiming the freed space to the OS requires a follow-up VACUUM (operator-gated).
"""
from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Any

from src.config import load_config

TABLE = "agent_runs"
DEFAULT_DAYS = 14
ARCHIVE_DIR = "data/archive/agent_runs"

# OLD rows whose heavy blob can be archived + cleared: older than cutoff AND still carrying a blob.
_CLEARABLE_WHERE = "run_at < :cutoff AND summary_json IS NOT NULL"


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


def plan(days: int = DEFAULT_DAYS, db: str | None = None, now: datetime | None = None) -> dict[str, Any]:
    cfg = load_config()
    path = db or cfg.db_path
    conn = _conn(path)
    try:
        cutoff = _cutoff_iso(days, now)
        total = conn.execute(f"SELECT COUNT(*) FROM {TABLE}").fetchone()[0]
        with_blob, blob_bytes = conn.execute(
            f"SELECT COUNT(*), COALESCE(SUM(LENGTH(summary_json)),0) FROM {TABLE} "
            "WHERE summary_json IS NOT NULL").fetchone()
        clearable, clearable_bytes = conn.execute(
            f"SELECT COUNT(*), COALESCE(SUM(LENGTH(summary_json)),0) FROM {TABLE} "
            f"WHERE {_CLEARABLE_WHERE}", {"cutoff": cutoff}).fetchone()
    finally:
        conn.close()
    return {
        "table": TABLE, "db_path": path, "db_size_mb": _db_size_mb(path),
        "days": days, "cutoff": cutoff,
        "total_rows": total, "rows_with_blob": with_blob,
        "blob_total_mb": round(blob_bytes / 1e6, 1),
        "clearable_rows": clearable, "clearable_mb": round(clearable_bytes / 1e6, 1),
        "kept_recent_blob_rows": with_blob - clearable,
        "note": "metadata rows (agent_name/run_at/output_path) are kept; only the write-only "
                "summary_json blob of OLD rows is archived + nulled. VACUUM (separate) reclaims the freed space.",
    }


def _archive_blobs(conn: sqlite3.Connection, cutoff: str, archive_dir: str, now: datetime | None) -> str:
    os.makedirs(archive_dir, exist_ok=True)
    stamp = (now or datetime.now(timezone.utc)).strftime("%Y%m%dT%H%M%S")
    rows = conn.execute(
        f"SELECT id, agent_name, run_at, output_path, asset_class, summary_json "
        f"FROM {TABLE} WHERE {_CLEARABLE_WHERE}", {"cutoff": cutoff}).fetchall()
    cols = ["id", "agent_name", "run_at", "output_path", "asset_class", "summary_json"]
    try:
        import pandas as pd
        df = pd.DataFrame([dict(r) for r in rows], columns=cols)
        path = os.path.join(archive_dir, f"agent_runs_summary_archive_{stamp}.parquet")
        df.to_parquet(path, index=False)
        return path
    except Exception:
        import csv
        import gzip
        path = os.path.join(archive_dir, f"agent_runs_summary_archive_{stamp}.csv.gz")
        with gzip.open(path, "wt", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(cols)
            for r in rows:
                w.writerow([r[c] for c in cols])
        return path


def run(days: int = DEFAULT_DAYS, *, archive: bool = True, dry_run: bool = True,
        do_vacuum: bool = False, db: str | None = None, archive_dir: str = ARCHIVE_DIR,
        now: datetime | None = None) -> dict[str, Any]:
    """Archive the old ``summary_json`` blobs then NULL them (metadata rows kept). DRY-RUN by default.
    Archive is written FIRST; the UPDATE is aborted if archiving fails, so blobs are never lost."""
    cfg = load_config()
    path = db or cfg.db_path
    before = plan(days, db=path, now=now)
    result: dict[str, Any] = {"dry_run": dry_run, "before": before, "archive_file": None,
                              "cleared_rows": 0, "vacuumed": False}
    if dry_run:
        result["note"] = "dry-run — nothing archived or cleared; re-run with dry_run=False to apply"
        return result
    if before["clearable_rows"] == 0:
        result["note"] = "nothing to clear"
        return result
    conn = _conn(path)
    try:
        cutoff = before["cutoff"]
        if archive:
            result["archive_file"] = _archive_blobs(conn, cutoff, archive_dir, now)
        cur = conn.execute(f"UPDATE {TABLE} SET summary_json = NULL WHERE {_CLEARABLE_WHERE}",
                           {"cutoff": cutoff})
        result["cleared_rows"] = cur.rowcount
        conn.commit()
        if do_vacuum:
            conn.execute("VACUUM")
            result["vacuumed"] = True
    finally:
        conn.close()
    result["after"] = plan(days, db=path, now=now)
    return result
