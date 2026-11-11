from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

from src.execution.paper_live_exit_path import VERSION as LIVE_EXIT_PARITY_VERSION
from src.live_execution import mode_audit


def test_live_compatible_paper_pf_excludes_legacy_exit_models(monkeypatch):
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE proposed_signals (
          signal_id TEXT PRIMARY KEY,
          created_at TEXT,
          asset_class TEXT,
          mode TEXT,
          entry_type TEXT,
          symbol TEXT,
          direction TEXT,
          tier TEXT,
          score REAL
        );
        CREATE TABLE paper_execution_outcomes (
          signal_id TEXT PRIMARY KEY,
          exit_at TEXT,
          paper_execution_r REAL,
          lifecycle_state TEXT,
          execution_validity TEXT,
          entry_time_basis TEXT,
          current_price_revalidated INTEGER,
          close_reason TEXT,
          paper_entry_profile TEXT,
          paper_execution_entry_mode TEXT,
          version TEXT
        );
        """
    )
    for signal_id in ("legacy", "v3"):
        conn.execute(
            "INSERT INTO proposed_signals VALUES (?,?,?,?,?,?,?,?,?)",
            (
                signal_id,
                "2026-09-27T10:00:00+00:00",
                "crypto",
                "intraday",
                "BREAKOUT_CONTINUATION",
                "BTC/USDT",
                "long",
                "B",
                80.0,
            ),
        )
    common = (
        "2026-09-27T11:00:00+00:00",
        "CLOSED",
        "valid",
        "point_in_time_current_bar",
        1,
        "tp3",
        "profile",
        "BREAKOUT_CONTINUATION",
    )
    conn.execute(
        "INSERT INTO paper_execution_outcomes VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        ("legacy", common[0], 9.0, *common[1:], "old_full_tp3_model"),
    )
    conn.execute(
        "INSERT INTO paper_execution_outcomes VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        ("v3", common[0], 0.5, *common[1:], LIVE_EXIT_PARITY_VERSION),
    )
    monkeypatch.setattr(
        mode_audit,
        "route",
        lambda **_: {"enabled": True, "route_key": "crypto_intraday_breakout"},
    )

    result = mode_audit._live_compatible_paper_pf(
        conn, datetime(2026, 9, 26, tzinfo=timezone.utc)
    )

    assert result["overall"]["closed"] == 1
    assert result["overall"]["net_r"] == 0.5
    assert {row["reason"]: row["n"] for row in result["excluded"]}[
        "LEGACY_PAPER_EXIT_MODEL"
    ] == 1

