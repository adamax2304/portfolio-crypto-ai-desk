from __future__ import annotations

import gzip
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

from src.maintenance import market_intelligence_retention as retention


def test_default_archive_dir_uses_drive_with_most_free_space(monkeypatch):
    monkeypatch.setattr(
        retention, "load_config", lambda: SimpleNamespace(root="C:/project")
    )
    monkeypatch.setattr(
        Path, "exists", lambda path: path.anchor.upper() in {"C:\\", "D:\\", "F:\\"}
    )
    free_by_drive = {"C:\\": 30, "D:\\": 5, "F:\\": 10}
    monkeypatch.setattr(
        retention.shutil,
        "disk_usage",
        lambda path: SimpleNamespace(free=free_by_drive[str(path).upper()] * 1024**3),
    )

    assert retention.default_archive_dir() == Path(
        "C:/project/data/archive/market_intelligence"
    )


def test_retention_archives_before_deleting_only_old_bounded_rows(tmp_path):
    db = tmp_path / "intelligence.sqlite"
    archive = tmp_path / "archive"
    now = datetime(2026, 8, 30, tzinfo=timezone.utc)
    old = (now - timedelta(days=40)).isoformat()
    fresh = (now - timedelta(days=1)).isoformat()
    with sqlite3.connect(db) as conn:
        conn.execute(
            "CREATE TABLE derivative_snapshots("
            "id INTEGER PRIMARY KEY,provider_ts TEXT,received_at TEXT,raw_json TEXT)"
        )
        conn.executemany(
            "INSERT INTO derivative_snapshots(provider_ts,received_at,raw_json) VALUES(?,?,?)",
            [(old, fresh, "old-1"), (old, fresh, "old-2"), (fresh, fresh, "fresh")],
        )
        conn.commit()

    result = retention.run(
        db=db, archive_dir=archive, max_rows_per_table=1,
        delete_batch=1, dry_run=False, now=now,
    )
    item = result["tables"]["derivative_snapshots"]
    assert item["archived"] == item["deleted"] == 1
    assert item["timestamp_column"] == "provider_ts"
    with gzip.open(item["archive_file"], "rt", encoding="utf-8") as handle:
        payloads = [json.loads(line) for line in handle]
    assert payloads[1]["raw_json"] == "old-1"
    with sqlite3.connect(db) as conn:
        assert conn.execute(
            "SELECT raw_json FROM derivative_snapshots ORDER BY id"
        ).fetchall() == [("old-2",), ("fresh",)]
