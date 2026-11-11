from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

from src.analysis.live_execution_evidence import live_fill_parity


def test_live_fill_parity_does_not_double_count_exchange_fees_or_funding(tmp_path):
    db = tmp_path / "live.sqlite"
    with sqlite3.connect(db) as conn:
        conn.executescript(
            """
            CREATE TABLE mexc_canary_positions (
              decision_id TEXT, symbol TEXT, status TEXT, opened_at TEXT,
              realized_pnl_usdt REAL, fees_usdt REAL, funding_usdt REAL,
              risk_usdt REAL, venue TEXT
            );
            CREATE TABLE mexc_canary_decisions (
              decision_id TEXT, signal_id TEXT, mode TEXT, entry_mode TEXT,
              decision_json TEXT
            );
            CREATE TABLE paper_execution_outcomes (
              signal_id TEXT, paper_execution_r REAL, paper_entry_profile TEXT
            );
            """
        )
        conn.execute(
            "INSERT INTO mexc_canary_positions VALUES (?,?,?,?,?,?,?,?,?)",
            ("d1", "SOL_USDT", "CLOSED", "2026-09-27T10:00:00+00:00",
             3.24, 0.72, -0.05, 5.0, "mexc"),
        )
        conn.execute(
            "INSERT INTO mexc_canary_decisions VALUES (?,?,?,?,?)",
            ("d1", "s1", "liquidity_sweep", "LIQUIDITY_SWEEP", "{}"),
        )
        conn.execute(
            "INSERT INTO paper_execution_outcomes VALUES (?,?,?)",
            ("s1", 0.5, "sweep_v1"),
        )
    result = live_fill_parity(
        db=db, days=30, now=datetime(2026, 9, 27, 12, 0, tzinfo=timezone.utc),
    )
    assert result["trades"][0]["live_net_usd"] == 3.24
    assert result["trades"][0]["live_r"] == 0.648
    assert result["summary"][0]["live_net_usd"] == 3.24
