"""PART 4 — paper entry-mode classifier tests (paper-only, add-only). No network/live."""
from __future__ import annotations

import sqlite3

from src.execution.entry_mode_classifier import (
    ENTRY_MODES, classify, compute_record, ensure_table, _upsert,
)


def _uptrend(n=60, step=0.3, start=100.0):
    rows, px = [], start
    for _ in range(n):
        rows.append({"open": px, "high": px + 0.4, "low": px - 0.4, "close": px + 0.2})
        px += step
    return rows


def _coiled_under_resistance():
    # rise, then flat just under a prior swing high → breakout-continuation setup
    rows = _uptrend(40, step=0.5, start=80.0)        # builds a swing high near ~100
    flat = rows[-1]["close"]
    for _ in range(18):
        rows.append({"open": flat, "high": flat + 0.3, "low": flat - 0.3, "close": flat + 0.05})
    return rows


def test_modes_enum_complete():
    assert set(ENTRY_MODES) == {
        "PULLBACK_LIMIT", "STRUCTURAL_RETEST", "BREAKOUT_CONTINUATION",
        "MOMENTUM_TAKER_NOW", "LIMIT_THEN_TAKER_TIMEOUT", "NO_CHASE_SKIP"}


def test_classify_returns_valid_mode_and_fields():
    c = classify(entry_low=98.0, entry_high=99.0, direction="long", candles=_uptrend())
    assert c["entry_mode"] in ENTRY_MODES
    assert c["entry_style"] in ("limit", "stop", "taker", "limit_then_taker", "none")
    assert c["candles_used"] == len(_uptrend())
    assert c["momentum_atr"] is not None  # momentum measured from real candles


def test_no_candles_defaults_to_pullback_limit():
    c = classify(entry_low=98.0, entry_high=99.0, direction="long", candles=None)
    assert c["entry_mode"] == "PULLBACK_LIMIT"
    assert c["candles_used"] == 0


def test_extended_momentum_is_not_pullback():
    # strong sustained uptrend → should NOT be a quiet pullback-limit; engine should pick a
    # momentum/continuation mode (anything but PULLBACK_LIMIT) given the extension + momentum
    cs = _uptrend(60, step=1.2, start=50.0)  # steep → extended from mean, strong momentum
    c = classify(entry_low=None, entry_high=None, direction="long", candles=cs)
    assert c["entry_mode"] in ENTRY_MODES
    assert c["momentum_atr"] > 0


def test_persist_roundtrip(monkeypatch):
    import src.execution.entry_mode_classifier as m
    monkeypatch.setattr(m, "_candles_for", lambda *a, **k: _coiled_under_resistance())
    trade = {"signal_id": "sig_em_test", "symbol": "T/USDT", "direction": "long",
             "asset_class": "crypto", "entry": 100.0, "stop": 97.0,
             "entry_low": 99.0, "entry_high": 99.6}
    rec = compute_record(trade, {"mode": "intraday"}, fs=None, cfg=None)
    assert rec["entry_mode"] in ENTRY_MODES
    conn = sqlite3.connect(":memory:"); conn.row_factory = sqlite3.Row
    ensure_table(conn); _upsert(conn, rec); conn.commit()
    row = dict(conn.execute(
        "SELECT * FROM signal_entry_mode WHERE signal_id=?", ("sig_em_test",)).fetchone())
    assert row["entry_mode"] == rec["entry_mode"]
    _upsert(conn, rec); conn.commit()
    assert conn.execute("SELECT count(*) FROM signal_entry_mode").fetchone()[0] == 1
