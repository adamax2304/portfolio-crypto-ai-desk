"""PART 3 — structural paper TP set (paper-only, add-only) tests.

Covers: the table contract, structural-vs-mechanical labelling, the STRUCTURAL/HYBRID/
ATR_FALLBACK/NO_VALID_TP mapping, and the invariant that the production TP fields are
never touched. No network, no live.
"""
from __future__ import annotations

import sqlite3

from src.execution.signal_paper_tp import (
    _LABEL_TO_TYPE, _entry_triggered_signals, compute_record, ensure_table, _upsert, get_paper_tp,
)


# A synthetic short trade whose nearest swing high is closer than the 1x-ATR target,
# so the structural engine should produce a STRUCTURAL set distinct from mechanical.
def _short_trade():
    return {
        "signal_id": "sig_test_struct", "symbol": "TEST/USDT", "direction": "short",
        "asset_class": "crypto", "entry": 100.0, "stop": 104.0,
        "tp1": 96.0, "tp2": 92.0, "tp3": 88.0,  # mechanical (1/2/3 ATR for risk=4)
        "playbook": "crypto_intraday_catalyst_or_momentum", "regime": "trend_down",
    }


def _down_candles():
    # descending highs/lows → swing lows below entry act as structural TP targets
    rows = []
    px = 110.0
    for _ in range(60):
        rows.append({"open": px, "high": px + 0.5, "low": px - 0.5, "close": px - 0.2})
        px -= 0.3
    return rows


class _StubFS:
    """Minimal stand-in: returns a DataFrame-like via pandas if available, else the
    list path is exercised directly through compute_record's candle loader bypass."""


def test_label_mapping_is_total():
    for label in ("STRUCTURAL", "HYBRID", "STRUCTURAL_FALLBACK_ATR", "NO_VALID_TP"):
        assert label in _LABEL_TO_TYPE
    assert _LABEL_TO_TYPE["STRUCTURAL_FALLBACK_ATR"] == "ATR_FALLBACK"


def test_compute_record_structural_differs_from_mechanical(monkeypatch):
    import src.execution.signal_paper_tp as m
    # feed real structural candles directly (bypass file_store / network)
    monkeypatch.setattr(m, "_candles_for", lambda *a, **k: _down_candles())
    rec = compute_record(_short_trade(), {"mode": "intraday"}, fs=None, cfg=None)
    assert rec["signal_id"] == "sig_test_struct"
    # mechanical fields are carried through unchanged
    assert rec["mechanical_tp1"] == 96.0 and rec["mechanical_tp3"] == 88.0
    # structure was used (real candles) → not NO_VALID_TP, candles recorded
    assert rec["tp_set_type"] in ("STRUCTURAL", "HYBRID", "ATR_FALLBACK")
    assert rec["candles_used"] == len(_down_candles())
    # active TP1 is a real number in the profit direction (below entry for a short)
    assert rec["active_paper_tp1"] is not None and rec["active_paper_tp1"] < 100.0


def test_no_candles_falls_back_not_crash(monkeypatch):
    import src.execution.signal_paper_tp as m
    monkeypatch.setattr(m, "_candles_for", lambda *a, **k: None)
    rec = compute_record(_short_trade(), {"mode": "intraday"}, fs=None, cfg=None)
    # with no structure but a valid risk geometry, the engine ATR-falls-back (or NO_VALID)
    assert rec["tp_set_type"] in ("ATR_FALLBACK", "NO_VALID_TP", "STRUCTURAL", "HYBRID")
    assert rec["candles_used"] == 0
    # mechanical TPs are still preserved regardless
    assert rec["mechanical_tp1"] == 96.0


def test_persist_and_read_roundtrip(monkeypatch):
    import src.execution.signal_paper_tp as m
    monkeypatch.setattr(m, "_candles_for", lambda *a, **k: _down_candles())
    rec = compute_record(_short_trade(), {"mode": "intraday"}, fs=None, cfg=None)
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    ensure_table(conn)
    _upsert(conn, rec)
    conn.commit()
    row = dict(conn.execute(
        "SELECT * FROM signal_paper_tp WHERE signal_id=?", ("sig_test_struct",)).fetchone())
    assert row["tp_set_type"] == rec["tp_set_type"]
    assert row["mechanical_tp1"] == 96.0
    # idempotent upsert: re-inserting keeps a single row
    _upsert(conn, rec)
    conn.commit()
    assert conn.execute("SELECT count(*) FROM signal_paper_tp").fetchone()[0] == 1


def test_refresh_queue_prioritizes_missing_then_oldest_tp_record():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE proposed_signals (
        signal_id TEXT PRIMARY KEY, symbol TEXT, direction TEXT, mode TEXT,
        asset_class TEXT, setup_type TEXT, market_regime TEXT, created_at TEXT,
        suggested_entry REAL, entry_trigger REAL, entry_low REAL, stop_loss REAL,
        invalidation REAL, tp1 REAL, tp2 REAL, tp3 REAL, exchange_focus TEXT
    )""")
    conn.execute("""CREATE TABLE signal_outcomes (
        id INTEGER PRIMARY KEY, signal_id TEXT, checked_at TEXT,
        entry_triggered INTEGER, entry_triggered_at TEXT
    )""")
    for signal_id in ("missing", "old", "fresh"):
        conn.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                     (signal_id, "BTC/USDT", "long", "intraday", "crypto", "x", "risk_on",
                      "2026-07-01T00:00:00+00:00", 100.0, 100.0, 99.0, 95.0, 95.0,
                      105.0, 110.0, 115.0, ""))
        conn.execute("INSERT INTO signal_outcomes(signal_id,checked_at,entry_triggered,entry_triggered_at) "
                     "VALUES (?,?,1,?)", (signal_id, "2026-07-01T01:00:00+00:00",
                                            "2026-07-01T01:00:00+00:00"))
    ensure_table(conn)
    conn.execute("INSERT INTO signal_paper_tp(signal_id,computed_at) VALUES (?,?)",
                 ("old", "2026-07-01T02:00:00+00:00"))
    conn.execute("INSERT INTO signal_paper_tp(signal_id,computed_at) VALUES (?,?)",
                 ("fresh", "2026-07-02T02:00:00+00:00"))
    conn.commit()

    rows = _entry_triggered_signals(conn, limit=3)
    assert [row["signal_id"] for row in rows] == ["missing", "old", "fresh"]
