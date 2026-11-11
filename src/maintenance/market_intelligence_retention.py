from __future__ import annotations

import gzip
import json
import shutil
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from src.config import load_config


# Runtime consumers use recent point-in-time context. Older observations are
# archived before deletion, so research evidence remains recoverable without
# forcing every live query to carry months of high-frequency snapshots.
TABLE_RETENTION = {
    "cross_exchange_quote_snapshots": (7, "provider_ts"),
    "derivative_snapshots": (14, "provider_ts"),
    "liquidity_snapshots": (14, "provider_ts"),
    "funding_rate_events": (30, "event_at"),
    "liquidation_events": (30, "event_at"),
    "stablecoin_peg_snapshots": (30, "provider_ts"),
}
TABLE_RETENTION_DAYS = {table: policy[0] for table, policy in TABLE_RETENTION.items()}


def default_db_path() -> Path:
    return Path(load_config().root) / "data" / "intelligence" / "market_intelligence.sqlite"


def default_archive_dir() -> Path:
    local = Path(load_config().root) / "data" / "archive" / "market_intelligence"
    candidates = (
        Path("F:/crypto-ai-desk-archives/market_intelligence"),
        Path("D:/crypto-ai-desk-archives/market_intelligence"),
        local,
    )
    available: list[tuple[int, Path]] = []
    for candidate in candidates:
        try:
            drive_root = Path(candidate.anchor)
            if drive_root.exists():
                free = int(shutil.disk_usage(drive_root).free)
                if free > 2 * 1024**3:
                    available.append((free, candidate))
        except OSError:
            pass
    return max(available, key=lambda item: item[0])[1] if available else local


def _cutoff(days: int, now: datetime) -> str:
    return (now - timedelta(days=days)).isoformat()


def _candidate_ceiling(
    conn: sqlite3.Connection, table: str, timestamp_column: str,
    cutoff: str, max_rows: int,
) -> tuple[int | None, int]:
    rows = conn.execute(
        f"SELECT id FROM {table} WHERE {timestamp_column}<? ORDER BY id LIMIT ?",
        (cutoff, max(1, int(max_rows))),
    ).fetchall()
    return (int(rows[-1][0]), len(rows)) if rows else (None, 0)


def plan(
    *, db: str | Path | None = None, max_rows_per_table: int = 250_000,
    now: datetime | None = None,
) -> dict[str, Any]:
    moment = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    path = Path(db) if db else default_db_path()
    result: dict[str, Any] = {"db": str(path), "tables": {}}
    with sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=30.0) as conn:
        existing = {row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        for table, (days, timestamp_column) in TABLE_RETENTION.items():
            if table not in existing:
                continue
            cutoff = _cutoff(days, moment)
            ceiling, rows = _candidate_ceiling(
                conn, table, timestamp_column, cutoff, max_rows_per_table,
            )
            result["tables"][table] = {
                "retention_days": days, "cutoff": cutoff,
                "timestamp_column": timestamp_column,
                "candidate_rows": rows, "max_id": ceiling,
            }
    return result


def _archive_batch(
    conn: sqlite3.Connection, *, table: str, timestamp_column: str,
    cutoff: str, max_id: int,
    archive_dir: Path, moment: datetime,
) -> tuple[Path, int]:
    archive_dir.mkdir(parents=True, exist_ok=True)
    stamp = moment.strftime("%Y%m%dT%H%M%SZ")
    target = archive_dir / f"{table}_{stamp}_{max_id}.jsonl.gz"
    columns = [str(row[1]) for row in conn.execute(f"PRAGMA table_info({table})")]
    count = 0
    with gzip.open(target, "wt", encoding="utf-8", compresslevel=6) as handle:
        handle.write(json.dumps({"_meta": {
            "table": table, "columns": columns, "cutoff": cutoff,
            "max_id": max_id, "archived_at": moment.isoformat(),
        }}, sort_keys=True) + "\n")
        cursor = conn.execute(
            f"SELECT * FROM {table} WHERE id<=? AND {timestamp_column}<? ORDER BY id",
            (max_id, cutoff),
        )
        while True:
            rows = cursor.fetchmany(5_000)
            if not rows:
                break
            for row in rows:
                handle.write(json.dumps(dict(zip(columns, row)), sort_keys=True) + "\n")
                count += 1
    return target, count


def run(
    *, db: str | Path | None = None, archive_dir: str | Path | None = None,
    max_rows_per_table: int = 250_000, delete_batch: int = 25_000,
    dry_run: bool = True, now: datetime | None = None,
) -> dict[str, Any]:
    moment = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    path = Path(db) if db else default_db_path()
    archive_root = Path(archive_dir) if archive_dir else default_archive_dir()
    planned = plan(db=path, max_rows_per_table=max_rows_per_table, now=moment)
    result: dict[str, Any] = {
        "dry_run": dry_run, "db": str(path), "archive_dir": str(archive_root),
        "tables": {},
    }
    if dry_run:
        result["tables"] = planned["tables"]
        return result

    with sqlite3.connect(path, timeout=30.0) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA busy_timeout=30000")
        for table, item in planned["tables"].items():
            max_id = item.get("max_id")
            if not max_id:
                result["tables"][table] = {**item, "archived": 0, "deleted": 0}
                continue
            archive_file, archived = _archive_batch(
                conn, table=table,
                timestamp_column=str(item["timestamp_column"]),
                cutoff=str(item["cutoff"]), max_id=int(max_id),
                archive_dir=archive_root, moment=moment,
            )
            deleted = 0
            while True:
                cursor = conn.execute(
                    f"DELETE FROM {table} WHERE id IN (SELECT id FROM {table} "
                    f"WHERE id<=? AND {item['timestamp_column']}<? ORDER BY id LIMIT ?)",
                    (int(max_id), str(item["cutoff"]), max(1, int(delete_batch))),
                )
                changed = max(0, int(cursor.rowcount or 0))
                conn.commit()
                deleted += changed
                if changed == 0:
                    break
            result["tables"][table] = {
                **item, "archive_file": str(archive_file),
                "archived": archived, "deleted": deleted,
            }
        conn.execute("PRAGMA wal_checkpoint(PASSIVE)")
    return result


__all__ = ["TABLE_RETENTION_DAYS", "default_archive_dir", "default_db_path", "plan", "run"]
