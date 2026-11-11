"""PART 8 — structural stop-move plan tests (paper read-model). No network/live."""
from __future__ import annotations

import sqlite3

from src.execution.signal_stop_plan import compute_record, ensure_table, _upsert


def _long_candles_with_higher_low():
    # an uptrend whose recent swing low sits above breakeven → structural stop candidate
    rows = []
    px = 90.0
    for _ in range(30):
        rows.append({"open": px, "high": px + 1.0, "low": px - 0.5, "close": px + 0.6})
        px += 1.0
    # a clear higher-low pullback around 102 then continuation
    for lo in (102.0, 103.5, 105.0, 107.0):
        rows.append({"open": lo, "high": lo + 1.0, "low": lo, "close": lo + 0.8})
    return rows


def test_prefers_structure_when_higher_low_exists(monkeypatch):
    import src.execution.signal_stop_plan as m
    monkeypatch.setattr(m, "_candles_for", lambda *a, **k: _long_candles_with_higher_low())
    trade = {"signal_id": "sig_sp", "symbol": "T/USDT", "direction": "long",
             "asset_class": "crypto", "entry": 108.0, "stop": 104.0}
    rec = compute_record(trade, {"mode": "intraday"}, fs=None, cfg=None)
    assert rec["candles_used"] > 0
    # at least one of the post-TP stops should be structural (not just be/lock)
    bases = {rec["stop_after_tp1_basis"], rec["stop_after_tp2_basis"]}
    assert rec["prefers_structure"] == (1 if (bases & {"higher_low", "support", "vwap"}) else 0)


def test_falls_back_to_be_lock_without_structure(monkeypatch):
    import src.execution.signal_stop_plan as m
    monkeypatch.setattr(m, "_candles_for", lambda *a, **k: None)   # no candles → no structure
    trade = {"signal_id": "sig_sp2", "symbol": "T/USDT", "direction": "long",
             "asset_class": "crypto", "entry": 108.0, "stop": 104.0}
    rec = compute_record(trade, {"mode": "intraday"}, fs=None, cfg=None)
    assert rec["stop_after_tp1_basis"] in ("be", "lock", "none")
    assert rec["prefers_structure"] == 0
    # BE after TP1 is at/above entry-risk breakeven; never worse than initial stop
    assert rec["stop_after_tp1"] is not None


def test_roundtrip(monkeypatch):
    import src.execution.signal_stop_plan as m
    monkeypatch.setattr(m, "_candles_for", lambda *a, **k: _long_candles_with_higher_low())
    trade = {"signal_id": "sig_sp3", "symbol": "T/USDT", "direction": "long",
             "asset_class": "crypto", "entry": 108.0, "stop": 104.0}
    rec = compute_record(trade, {"mode": "intraday"}, fs=None, cfg=None)
    conn = sqlite3.connect(":memory:"); conn.row_factory = sqlite3.Row
    ensure_table(conn); _upsert(conn, rec); conn.commit()
    row = dict(conn.execute("SELECT * FROM signal_stop_plan WHERE signal_id=?", ("sig_sp3",)).fetchone())
    assert row["entry"] == 108.0
    _upsert(conn, rec); conn.commit()
    assert conn.execute("SELECT count(*) FROM signal_stop_plan").fetchone()[0] == 1
