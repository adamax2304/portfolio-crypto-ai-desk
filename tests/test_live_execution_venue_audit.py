from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone

from src.execution.paper_operational_audit import _mexc_handoff
from src.live_execution.service import _record_venue_route_attempts
from src.live_execution import store


def test_venue_attempts_are_append_only_and_reported(tmp_path):
    path = tmp_path / "live.sqlite"
    with sqlite3.connect(path) as conn:
        store.ensure_tables(conn)
        store.record_venue_attempt(
            conn,
            decision_id="decision-1",
            venue="mexc",
            stage="preflight",
            status="rejected",
            reason="MEXC_CONTRACT_MISSING",
            diagnostic={"symbol": "TEST_USDT"},
        )
        store.record_venue_attempt(
            conn,
            decision_id="decision-1",
            venue="bybit",
            stage="route_selection",
            status="selected",
            diagnostic={"symbol": "TESTUSDT"},
        )
        conn.commit()
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=1)
        report = _mexc_handoff(conn, cutoff=cutoff)

    assert report["venue_attempts"]["mexc:PREFLIGHT:REJECTED"] == 1
    assert report["venue_attempts"]["bybit:ROUTE_SELECTION:SELECTED"] == 1
    assert report["venue_rejections"] == [("mexc:MEXC_CONTRACT_MISSING", 1)]


def test_route_diagnostic_records_both_venues_and_selection(tmp_path):
    path = tmp_path / "route.sqlite"
    with sqlite3.connect(path) as conn:
        store.ensure_tables(conn)
        _record_venue_route_attempts(
            conn,
            decision_id="decision-2",
            diagnostic={
                "selected": "bybit",
                "selection_reason": "lowest_all_in_cost",
                "candidates": {"bybit": {"symbol": "AAPLUSDT"}},
                "rejected": {"mexc": {"reason": "MEXC_CONTRACT_MISSING"}},
            },
        )
        rows = conn.execute(
            "SELECT venue,stage,status,reason FROM mexc_canary_venue_attempts ORDER BY attempted_at,attempt_id"
        ).fetchall()

    assert ("bybit", "PREFLIGHT", "PASSED", None) in rows
    assert ("mexc", "PREFLIGHT", "REJECTED", "MEXC_CONTRACT_MISSING") in rows
    assert ("bybit", "ROUTE_SELECTION", "SELECTED", "lowest_all_in_cost") in rows
