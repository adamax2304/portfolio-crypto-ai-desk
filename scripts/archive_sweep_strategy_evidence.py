"""Archive retired sweep/reclaim evidence and remove it from the hot DB.

The immutable live execution ledger is intentionally excluded. Archived rows
are written as gzip JSONL with a SHA-256 manifest before any DELETE commits.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import load_config

FULL_TABLES = (
    "crypto_liquidity_sweep_v1_shadow_outcomes",
    "crypto_liquidity_sweep_v1_shadow_evaluations",
    "crypto_liquidity_sweep_v1_shadow_observations",
    "crypto_liquidity_sweep_v1_shadow_meta",
    "crypto_liquidity_sweep_reclaim_v2_paper_outcomes",
    "crypto_liquidity_sweep_reclaim_v2_paper_evaluations",
    "crypto_liquidity_sweep_reclaim_v2_paper_observations",
    "crypto_liquidity_sweep_reclaim_v2_paper_meta",
    "crypto_htf_liquidity_reclaim_v1_shadow_outcomes",
    "crypto_htf_liquidity_reclaim_v1_shadow_evaluations",
    "crypto_htf_liquidity_reclaim_v1_shadow_observations",
    "crypto_htf_liquidity_reclaim_v1_shadow_meta",
)

PROFILE_FILTERS = {
    "crypto_fast_flush_reclaim_v3_paper_outcomes": (
        "profile_id",
        (
            "crypto_fast_flush_reclaim_balanced_1m_paper_v3",
            "crypto_fast_flush_reclaim_held_1m_paper_v3",
            "crypto_fast_flush_reclaim_control_5m_paper_v3",
        ),
    ),
    "crypto_fast_flush_reclaim_v3_paper_evaluations": (
        "profile_id",
        (
            "crypto_fast_flush_reclaim_balanced_1m_paper_v3",
            "crypto_fast_flush_reclaim_held_1m_paper_v3",
            "crypto_fast_flush_reclaim_control_5m_paper_v3",
        ),
    ),
    "stocks_liquidity_shock_reclaim_v1_paper_outcomes": (
        "profile_id", ("stocks_liquidity_shock_fast_1m_paper_v1",),
    ),
    "stocks_liquidity_shock_reclaim_v1_paper_evaluations": (
        "profile_id", ("stocks_liquidity_shock_fast_1m_paper_v1",),
    ),
}

SOURCE_FILES = (
    "config/shadow_crypto_liquidity_sweep.yaml",
    "config/crypto_liquidity_sweep_live.yaml",
    "config/paper/crypto/liquidity_sweep_reclaim_v2.yaml",
    "config/shadow_crypto_htf_liquidity_reclaim.yaml",
    "reports/CRYPTO_LIQUIDITY_SWEEP_V1_SHADOW.md",
    "reports/CRYPTO_LIQUIDITY_SWEEP_RECLAIM_V2_PAPER.md",
    "reports/CRYPTO_HTF_LIQUIDITY_RECLAIM_V1_SHADOW.md",
)


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    return bool(conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ).fetchone())


def _dump_rows(
    conn: sqlite3.Connection, *, table: str, output: Path,
    where: str = "", params: tuple[Any, ...] = (),
) -> dict[str, Any]:
    output.parent.mkdir(parents=True, exist_ok=True)
    query = f"SELECT * FROM {table}" + (f" WHERE {where}" if where else "")
    digest = hashlib.sha256()
    count = 0
    with gzip.open(output, "wt", encoding="utf-8", newline="\n") as handle:
        for row in conn.execute(query, params):
            encoded = json.dumps(dict(row), sort_keys=True, default=str) + "\n"
            handle.write(encoded)
            digest.update(encoded.encode("utf-8"))
            count += 1
    return {
        "table": table,
        "rows": count,
        "file": str(output.relative_to(ROOT)),
        "content_sha256": digest.hexdigest(),
        "compressed_bytes": output.stat().st_size,
    }


def archive(*, db: Path, output: Path, apply: bool) -> dict[str, Any]:
    output.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db), timeout=60.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=60000")
    records: list[dict[str, Any]] = []
    try:
        for table in FULL_TABLES:
            if not _table_exists(conn, table):
                continue
            record = _dump_rows(
                conn, table=table, output=output / f"{table}.jsonl.gz",
            )
            records.append(record)
            if apply and record["rows"]:
                conn.execute(f"DELETE FROM {table}")
                conn.commit()

        for table, (column, values) in PROFILE_FILTERS.items():
            if not _table_exists(conn, table):
                continue
            placeholders = ",".join("?" for _ in values)
            where = f"{column} IN ({placeholders})"
            record = _dump_rows(
                conn, table=table, output=output / f"{table}.jsonl.gz",
                where=where, params=tuple(values),
            )
            record["profiles"] = list(values)
            records.append(record)
            if apply and record["rows"]:
                conn.execute(f"DELETE FROM {table} WHERE {where}", tuple(values))
                conn.commit()

        if apply:
            conn.execute("PRAGMA wal_checkpoint(PASSIVE)")
    finally:
        conn.close()

    copied: list[str] = []
    for relative in SOURCE_FILES:
        source = ROOT / relative
        if not source.exists():
            continue
        target = output / "sources" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(str(target.relative_to(ROOT)))

    result = {
        "archived_at": datetime.now(timezone.utc).isoformat(),
        "applied": apply,
        "database": str(db),
        "records": records,
        "source_files": copied,
        "live_execution_ledger_retained": True,
        "rows_archived": sum(int(item["rows"]) for item in records),
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
    selected = args.output if args.output.is_absolute() else ROOT / args.output
    print(json.dumps(
        archive(db=args.db, output=selected, apply=args.apply),
        indent=2, sort_keys=True,
    ))


if __name__ == "__main__":
    main()
