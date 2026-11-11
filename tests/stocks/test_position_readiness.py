"""Stocks Position Framework shadow readiness (item 5) — never writes proposed_signals."""
from __future__ import annotations

import sqlite3
from pathlib import Path

from src.stocks.position_framework import shadow_store as ss


def test_readiness_no_evidence_when_empty(tmp_path):
    db = str(Path(tmp_path) / "pf.sqlite")
    r = ss.readiness_summary(db)
    assert r["has_evidence"] is False
    assert r["verdict"] == "NO_EVIDENCE"
    assert "no evidence yet" in r["message"]
    # shadow-only guarantees surfaced from config (defaults are safe)
    assert r["shadow_only"] is True
    assert r["write_proposed_signals"] is False
    assert r["scheduler_enabled"] is True
    md = ss.render_readiness(db)
    assert "shadow readiness" in md and "NOT live" in md


def test_readiness_counts_and_gate(tmp_path):
    db = str(Path(tmp_path) / "pf2.sqlite")
    ss.ensure_tables(db)
    conn = sqlite3.connect(db)
    for i in range(3):
        conn.execute("INSERT INTO stocks_position_candidates (candidate_id, created_at, symbol, "
                     "status) VALUES (?,?,?, 'shadow_open')",
                     (f"c{i}", "2026-07-01T00:00:00+00:00", "AAPL"))
    conn.execute("INSERT INTO stocks_position_outcomes (candidate_id, checked_at, status, net_pnl_usd) "
                 "VALUES ('c0','2026-07-02T00:00:00+00:00','closed', 120.0)")
    conn.execute("INSERT INTO stocks_position_outcomes (candidate_id, checked_at, status, net_pnl_usd) "
                 "VALUES ('c1','2026-07-02T00:00:00+00:00','pending', NULL)")
    conn.commit(); conn.close()
    r = ss.readiness_summary(db)
    assert r["candidates_count"] == 3
    assert r["outcomes"]["closed"] == 1 and r["outcomes"]["pending"] == 1
    # the one closed outcome is CLEAN (gap_loss_r NULL) → clean_closed=1, dirty_closed=0
    assert r["outcomes"]["clean_closed"] == 1 and r["outcomes"]["dirty_closed"] == 0
    assert r["net_usd_closed"] == 120.0
    assert r["evidence_gate"]["clean_closed_sample"] == 1
    assert r["evidence_gate"]["sample_meets_gate"] is False   # 1 < min_forward_trades
    # has_evidence stays True, but 1 clean < min → NO good/bad conclusion: INSUFFICIENT_CLEAN_SAMPLE
    assert r["has_evidence"] is True and r["verdict"] == "INSUFFICIENT_CLEAN_SAMPLE"
    assert "INSUFFICIENT CLEAN SAMPLE" in r["message"] and "insufficient" in r["message"]


def test_framework_never_writes_proposed_signals(tmp_path):
    db = str(Path(tmp_path) / "pf3.sqlite")
    cand = {"passed": True, "symbol": "AAPL", "asset_class": "stocks", "mode": "swing",
            "playbook": "stocks_swing_growth_breakout", "score": 82.0, "risk_plan": {}}
    n = ss.insert_candidates([cand], created_at="2026-07-01T00:00:00+00:00", db_path=db)
    assert n == 1
    conn = sqlite3.connect(db)
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    conn.close()
    # the framework creates ONLY its own shadow tables — proposed_signals is never touched/created
    assert "stocks_position_candidates" in tables
    assert "proposed_signals" not in tables
