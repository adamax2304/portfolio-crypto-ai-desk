"""Shadow-only ticker monitor: normalizer + hypothetical touch + record/compare (2026-07-05).

Pure functions + a self-creating shadow table. NEVER trades; never touches signals/outcomes/alerts.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from src.signals import ws_shadow as ws

NOW = datetime(2026, 7, 5, 12, 0, tzinfo=timezone.utc)


def test_normalize_book_ticker():
    raw = {"symbol": "BTCUSDT", "bidPrice": "100.0", "askPrice": "100.2",
           "time": int(NOW.timestamp() * 1000)}
    row = ws.normalize_ticker(raw, symbol="BTC/USDT", now=NOW)
    assert row["bid"] == 100.0 and row["ask"] == 100.2
    assert row["last"] == 100.1                       # mid when no last given
    assert round(row["spread"], 3) == 0.2
    assert row["spread_bps"] is not None and row["data_age_sec"] == 0.0


def test_hypothetical_touch_band():
    assert ws.hypothetical_touch(entry_low=100.0, entry_high=101.0, last=100.5) is True
    assert ws.hypothetical_touch(entry_low=100.0, entry_high=101.0, last=99.0) is False
    assert ws.hypothetical_touch(entry_low=None, entry_high=101.0, last=100.5) is None
    # inverted band handled
    assert ws.hypothetical_touch(entry_low=101.0, entry_high=100.0, last=100.5) is True


def test_record_snapshot_self_creates_table(tmp_path):
    db = str(Path(tmp_path) / "s.sqlite")
    rows = [ws.normalize_ticker({"bidPrice": "10", "askPrice": "10.1"}, symbol="X/USDT", now=NOW)]
    rows[0]["signal_id"] = "sig1"
    rows[0]["in_entry_band"] = True
    n = ws.record_snapshot(db, rows)
    assert n == 1
    c = sqlite3.connect(db)
    got = c.execute("SELECT symbol, in_entry_band, signal_id FROM pending_ticker_shadow").fetchone()
    c.close()
    assert got == ("X/USDT", 1, "sig1")


def test_record_snapshot_fail_open_bad_db():
    assert ws.record_snapshot("/nonexistent_zzz/never/s.sqlite", [{"symbol": "X"}]) == 0


def _scope_db(tmp_path):
    """A DB with proposed_signals + signal_outcomes tables and one recent crypto A/B pending signal."""
    db = str(Path(tmp_path) / "s.sqlite")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, asset_class TEXT, tier TEXT, "
              "status TEXT, created_at TEXT)")
    c.execute("CREATE TABLE signal_outcomes (signal_id TEXT, entry_triggered INTEGER, "
              "entry_triggered_at TEXT)")
    c.execute("INSERT INTO proposed_signals VALUES ('sig1','crypto','A','triggered',?)",
              (NOW.isoformat(),))
    c.commit(); c.close()
    return db


def test_compare_touches_scoped(tmp_path):
    from datetime import timedelta
    db = _scope_db(tmp_path)
    # shadow saw the band 3 minutes BEFORE the candle tracker recorded the entry → 3 min saved
    ws.record_snapshot(db, [{"recorded_at": NOW.isoformat(), "symbol": "X/USDT",
                             "signal_id": "sig1", "in_entry_band": True}])
    c = sqlite3.connect(db)
    c.execute("INSERT INTO signal_outcomes VALUES ('sig1', 1, ?)",
              ((NOW + timedelta(minutes=3)).isoformat(),))
    c.commit(); c.close()
    cmp = ws.compare_touches(db, recent_hours=24, pending_only=True, asset_class="crypto",
                             now=NOW + timedelta(minutes=5))
    assert cmp["available"] is True
    assert cmp["scope_signals"] == 1 and cmp["signals_with_shadow_band"] == 1
    assert cmp["avg_minutes_saved"] == 3.0 and cmp["missed"] == 0


def test_historical_outside_window_not_counted_as_missed(tmp_path):
    from datetime import timedelta
    db = _scope_db(tmp_path)                      # only sig1 is in the recent scope
    c = sqlite3.connect(db)
    # a huge historical backlog of tracker entries OUTSIDE the recent window / scope
    for i in range(500):
        c.execute("INSERT INTO signal_outcomes VALUES (?, 1, ?)",
                  (f"old{i}", (NOW - timedelta(days=30)).isoformat()))
    c.commit(); c.close()
    cmp = ws.compare_touches(db, recent_hours=24, pending_only=True, asset_class="crypto", now=NOW)
    # missed must NOT balloon to 500 — only in-scope signals count (sig1 had no entry in window)
    assert cmp["scope_signals"] == 1
    assert cmp["missed"] == 0
    assert cmp["insufficient_sample"] is True     # scope < 3


def test_false_touch_only_within_scope(tmp_path):
    from datetime import timedelta
    db = _scope_db(tmp_path)                      # sig1 in scope, no tracker entry for it
    ws.record_snapshot(db, [
        {"recorded_at": NOW.isoformat(), "symbol": "X/USDT", "signal_id": "sig1", "in_entry_band": True},
        # a shadow band for a signal NOT in scope → must be ignored
        {"recorded_at": NOW.isoformat(), "symbol": "Y/USDT", "signal_id": "notscope", "in_entry_band": True},
    ])
    cmp = ws.compare_touches(db, recent_hours=24, pending_only=True, asset_class="crypto",
                             now=NOW + timedelta(minutes=1))
    assert cmp["false_touches"] == 1             # only sig1 (shadow band, no tracker entry); notscope ignored


def test_snapshot_is_shadow_only_no_trade_calls():
    src = Path(ws.__file__).read_text(encoding="utf-8").lower()
    for bad in ("create_order", "place_order", "submit_order", "manual_live_order",
                "auto_live", "manual_live"):
        assert bad not in src
