"""Execution-latency telemetry writer/read-model (2026-07-05). Read/append only; no live."""
from __future__ import annotations

import sqlite3
from pathlib import Path

from src.signals import latency_telemetry as t


def test_emit_creates_table_and_writes(tmp_path):
    db = str(Path(tmp_path) / "tel.sqlite")
    ok = t.emit(db, event_type="signal_created", signal_id="s1", symbol="BTC/USDT",
                asset_class="crypto", mode="intraday", source="pending-monitor",
                latency_from_signal_sec=12.0)
    assert ok is True
    rows = t.load_events(db)
    assert len(rows) == 1
    r = rows[0]
    assert r["event_type"] == "signal_created" and r["signal_id"] == "s1"
    assert r["latency_from_signal_sec"] == 12.0 and r["source"] == "pending-monitor"


def test_all_event_types_write_and_filter(tmp_path):
    db = str(Path(tmp_path) / "tel.sqlite")
    for et in t.EVENT_TYPES:
        assert t.emit(db, event_type=et, signal_id="s", asset_class="crypto") is True
    assert len(t.load_events(db)) == len(t.EVENT_TYPES)
    only = t.load_events(db, event_types=("paper_entry_alert_sent", "paper_entry_alert_failed"))
    assert {r["event_type"] for r in only} == {"paper_entry_alert_sent", "paper_entry_alert_failed"}


def test_emit_is_fail_open_on_bad_db():
    # a path that cannot be opened must NOT raise (telemetry never blocks the caller)
    assert t.emit("/nonexistent_dir_zzz/never/tel.sqlite", event_type="signal_created") is False
    assert t.load_events("/nonexistent_dir_zzz/never/tel.sqlite") == []


def test_recent_days_filter(tmp_path):
    db = str(Path(tmp_path) / "tel.sqlite")
    from datetime import datetime, timedelta, timezone
    now = datetime(2026, 7, 5, 12, 0, tzinfo=timezone.utc)
    t.emit(db, event_type="signal_created", event_at=(now - timedelta(days=1)).isoformat())
    t.emit(db, event_type="signal_created", event_at=(now - timedelta(days=30)).isoformat())
    assert len(t.load_events(db, recent_days=7, now=now)) == 1


def test_accepts_store_object(tmp_path):
    from src.storage.sqlite import SQLiteStore
    st = SQLiteStore(Path(tmp_path) / "s.sqlite")
    st.init_db()
    assert t.emit(st, event_type="pending_tracker_seen", asset_class="crypto") is True
    assert len(t.load_events(st)) == 1


def test_skipped_event_type_registered():
    assert "paper_entry_alert_skipped" in t.EVENT_TYPES
    assert "paper_entry_alert_sent" in t.TRANSITION_EVENTS
    assert "market_data_refreshed" not in t.TRANSITION_EVENTS   # repeatable, not deduped


def test_emit_once_dedupes_per_signal_event_source(tmp_path):
    db = str(Path(tmp_path) / "tel.sqlite")
    first = t.emit_once(db, event_type="entry_condition_detected", signal_id="s1",
                        source="pending-monitor")
    second = t.emit_once(db, event_type="entry_condition_detected", signal_id="s1",
                         source="pending-monitor")
    assert first is True and second is False
    assert len(t.load_events(db, event_types=("entry_condition_detected",))) == 1
    # a different source is a distinct key → written
    assert t.emit_once(db, event_type="entry_condition_detected", signal_id="s1",
                       source="track-signals") is True
    assert len(t.load_events(db, event_types=("entry_condition_detected",))) == 2


def test_clean_duplicate_transition_events(tmp_path):
    db = str(Path(tmp_path) / "tel.sqlite")
    # simulate pre-fix pollution: 4 identical sent rows for one signal (append, not emit_once)
    for _ in range(4):
        t.emit(db, event_type="paper_entry_alert_sent", signal_id="s1", source="track-signals")
    # a repeatable event is NEVER cleaned even if duplicated
    t.emit(db, event_type="market_data_refreshed", signal_id="s1", source="track-signals")
    t.emit(db, event_type="market_data_refreshed", signal_id="s1", source="track-signals")
    dry = t.clean_duplicate_transition_events(db, apply=False)
    assert dry["rows_to_delete"] == 3 and dry["deleted"] == 0        # keep earliest of the 4
    assert dry["by_event_type"]["paper_entry_alert_sent"] == 3
    applied = t.clean_duplicate_transition_events(db, apply=True)
    assert applied["deleted"] == 3
    assert len(t.load_events(db, event_types=("paper_entry_alert_sent",))) == 1
    assert len(t.load_events(db, event_types=("market_data_refreshed",))) == 2   # untouched
