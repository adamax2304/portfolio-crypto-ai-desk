"""Archive retired strategy-only evidence before deleting hot copies.

Core signal, Paper execution, live decision and reconciliation ledgers are not
included. Those remain the immutable source for later forensic comparisons.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from src.config import load_config

ROOT = Path(__file__).resolve().parents[1]

TABLES = (
    "crypto_derivreset_v3_shadow_evaluations",
    "crypto_derivreset_v3_shadow_events",
    "crypto_derivreset_v3_shadow_meta",
    "crypto_derivreset_v3_shadow_outcomes",
    "crypto_short_retest_shadow_evaluations",
    "crypto_short_retest_shadow_events",
    "crypto_short_retest_shadow_meta",
    "crypto_short_retest_shadow_outcomes",
    "stocks_catalyst_rs_shadow_evaluations",
    "stocks_catalyst_rs_shadow_meta",
    "stocks_catalyst_rs_shadow_outcomes",
    "stocks_earnings_gap_shadow_meta",
    "stocks_earnings_gap_shadow_outcomes",
    "stocks_intraday_variant_shadow_evaluations",
    "stocks_intraday_variant_shadow_meta",
    "stocks_intraday_variant_shadow_outcomes",
    "stocks_position_candidates",
    "stocks_position_outcomes",
    "stocks_position_reviews",
    "stocks_position_scan_runs",
    "stocks_position_v2_candidates",
    "stocks_position_v2_outcomes",
    "stocks_position_v2_reviews",
    "stocks_position_v2_scan_runs",
)

RESEARCH_DATABASES = (
    "research_labs/regime_conditioned_continuation/research.sqlite",
    "research_labs/regime_conditioned_continuation/near_miss.sqlite",
    "research_labs/stocks_swing_event_rs_pullback/research.sqlite",
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _archive_table(conn: sqlite3.Connection, table: str, output: Path) -> dict:
    exists = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ).fetchone()
    if not exists:
        return {"table": table, "rows": 0, "status": "missing"}
    target = output / "tables" / f"{table}.jsonl.gz"
    target.parent.mkdir(parents=True, exist_ok=True)
    current_rows = int(conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0])
    if target.exists() and current_rows == 0:
        with gzip.open(target, "rt", encoding="utf-8") as handle:
            archived_rows = sum(1 for _ in handle)
        return {
            "table": table,
            "rows": archived_rows,
            "file": str(target.relative_to(ROOT)),
            "sha256": _sha256(target),
            "compressed_bytes": target.stat().st_size,
            "status": "existing_archive_retained",
        }
    rows = 0
    with gzip.open(target, "wt", encoding="utf-8", newline="\n") as handle:
        for row in conn.execute(f'SELECT * FROM "{table}"'):
            handle.write(json.dumps(dict(row), sort_keys=True, default=str) + "\n")
            rows += 1
    return {
        "table": table,
        "rows": rows,
        "file": str(target.relative_to(ROOT)),
        "sha256": _sha256(target),
        "compressed_bytes": target.stat().st_size,
    }


def archive(*, db: Path, output: Path, apply: bool) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db), timeout=60)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=60000")
    table_records = []
    try:
        for table in TABLES:
            record = _archive_table(conn, table, output)
            table_records.append(record)
            if apply and record.get("rows"):
                conn.execute(f'DELETE FROM "{table}"')
        if apply:
            conn.commit()
            conn.execute("PRAGMA wal_checkpoint(PASSIVE)")
    finally:
        conn.close()

    database_records = []
    for relative in RESEARCH_DATABASES:
        source = ROOT / relative
        target = output / "research_databases" / f"{relative.replace('/', '__')}.gz"
        if not source.exists():
            if target.exists():
                database_records.append({
                    "source": relative,
                    "file": str(target.relative_to(ROOT)),
                    "archive_sha256": _sha256(target),
                    "compressed_bytes": target.stat().st_size,
                    "status": "existing_archive_retained",
                })
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        original_sha = _sha256(source)
        archived_source_sha = None
        if target.exists():
            digest = hashlib.sha256()
            with gzip.open(target, "rb") as archived:
                for chunk in iter(lambda: archived.read(1024 * 1024), b""):
                    digest.update(chunk)
            archived_source_sha = digest.hexdigest()
        if archived_source_sha != original_sha:
            with source.open("rb") as src, gzip.open(target, "wb", compresslevel=6) as dst:
                shutil.copyfileobj(src, dst, length=1024 * 1024)
            archived_source_sha = original_sha
        record = {
            "source": relative,
            "file": str(target.relative_to(ROOT)),
            "original_bytes": source.stat().st_size,
            "original_sha256": original_sha,
            "archive_sha256": _sha256(target),
            "compressed_bytes": target.stat().st_size,
            "verified_source_sha256": archived_source_sha,
        }
        database_records.append(record)
        if apply:
            source.unlink()

    result = {
        "archived_at": datetime.now(timezone.utc).isoformat(),
        "applied": apply,
        "database": str(db),
        "tables": table_records,
        "research_databases": database_records,
        "rows_archived": sum(int(item.get("rows", 0)) for item in table_records),
        "immutable_execution_ledgers_retained": True,
    }
    manifest = output / "manifest.json"
    manifest.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    result["manifest"] = str(manifest.relative_to(ROOT))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, default=load_config(ROOT).db_path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    print(json.dumps(archive(db=args.db, output=output, apply=args.apply), indent=2))


if __name__ == "__main__":
    main()
