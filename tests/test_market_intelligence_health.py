from __future__ import annotations

import sqlite3

from src.intelligence.market_intelligence_health import _fast_row_high_watermark


def test_fast_row_high_watermark_uses_autoincrement_sequence():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE events (id INTEGER PRIMARY KEY AUTOINCREMENT, value TEXT)")
    conn.executemany("INSERT INTO events(value) VALUES (?)", [("a",), ("b",), ("c",)])
    conn.execute("DELETE FROM events WHERE id=2")

    assert _fast_row_high_watermark(conn, "events") == 3
    conn.close()


def test_fast_row_high_watermark_falls_back_for_plain_table():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE plain (value TEXT)")
    conn.executemany("INSERT INTO plain(value) VALUES (?)", [("a",), ("b",)])

    assert _fast_row_high_watermark(conn, "plain") == 2
    conn.close()
