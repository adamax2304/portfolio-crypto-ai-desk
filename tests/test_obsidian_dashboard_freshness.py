"""Smoke checks for the Obsidian Current State dashboard freshness banner.

These tests do NOT require a live DB — they exercise the small helper
functions in the dashboard writer and the header renderer directly.
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

# Allow the script-style module to be importable.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _make_db():
    """In-memory SQLite mirroring just enough columns for _compute_freshness."""
    db = sqlite3.connect(":memory:")
    db.executescript(
        """
        CREATE TABLE proposed_signals (
            signal_id TEXT, created_at TEXT, updated_at TEXT
        );
        CREATE TABLE signal_outcomes (
            id INTEGER PRIMARY KEY,
            signal_id TEXT, checked_at TEXT
        );
        CREATE TABLE signal_alerts (
            alert_id TEXT, sent_at TEXT
        );
        """
    )
    return db


def test_compute_freshness_returns_newest_iso():
    from scripts.write_obsidian_current_state_dashboard import _compute_freshness

    db = _make_db()
    db.execute(
        "INSERT INTO proposed_signals(signal_id, created_at, updated_at) VALUES (?, ?, ?)",
        ("sig_x", "2026-06-10T15:00:00+00:00", "2026-06-10T15:30:00+00:00"),
    )
    db.execute(
        "INSERT INTO signal_outcomes(signal_id, checked_at) VALUES (?, ?)",
        ("sig_x", "2026-06-10T15:20:00+00:00"),
    )
    db.execute(
        "INSERT INTO signal_alerts(alert_id, sent_at) VALUES (?, ?)",
        ("a1", "2026-06-10T15:40:00+00:00"),
    )
    db.commit()
    out = _compute_freshness(db)
    assert "2026-06-10 15:40" in out["newest_db_iso"], out
    assert out["data_age_minutes"] is not None
    db.close()


def test_section_header_warns_when_stale():
    from scripts.write_obsidian_current_state_dashboard import section_header

    fresh = {"newest_db_iso": "2026-06-10 16:00 UTC", "data_age_minutes": 90.0}
    lines = section_header("2026-06-10 18:00 EEST", "GREEN", freshness=fresh)
    body = "\n".join(lines)
    assert "STALE" in body
    assert "90" in body
    assert "Canonical dashboard file" in body


def test_section_header_ok_when_fresh():
    from scripts.write_obsidian_current_state_dashboard import section_header

    fresh = {"newest_db_iso": "2026-06-10 16:00 UTC", "data_age_minutes": 5.0}
    lines = section_header("2026-06-10 19:05 EEST", "GREEN", freshness=fresh)
    body = "\n".join(lines)
    assert "STALE" not in body
    assert "Data freshness" in body
    assert "Canonical dashboard file" in body


def test_section_header_handles_missing_freshness():
    from scripts.write_obsidian_current_state_dashboard import section_header

    lines = section_header("2026-06-10 19:05 EEST", "GREEN", freshness=None)
    body = "\n".join(lines)
    # Should not raise and should still render the canonical-path line.
    assert "Canonical dashboard file" in body
    assert "Refreshed:" in body
