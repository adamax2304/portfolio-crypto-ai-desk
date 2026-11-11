"""Tests for the SHADOW-ONLY Stocks Position Framework enriched-analysis packet + review layer.

No network. Verifies the packet is read-only / shadow-only, surfaces candidates + outcomes, never
fabricates news, and that review ingestion validates candidate_id and writes ONLY the separate
stocks_position_reviews table (never proposed_signals / signal_outcomes / paper_*).
"""
from __future__ import annotations

import sqlite3

import pytest

from src.stocks.position_framework import llm_packet as pf_packet
from src.stocks.position_framework import shadow_store as pf_store


def _candidate(symbol="AAPL"):
    return {
        "passed": True, "symbol": symbol, "asset_class": "stocks", "mode": "swing",
        "playbook": "stocks_swing_growth_breakout", "setup_variant": "breakout", "direction": "long",
        "score": 80, "data_confidence": 0.9, "entry_price": 190, "entry_low": 188, "entry_high": 193,
        "risk_plan": {"stop_price": 182, "tp1": 206, "tp1_r": 2.0, "tp2": 214, "tp2_r": 3.0,
                      "risk_usd": 12.5, "trail_rule": "trail", "max_holding_days": 40,
                      "risk_pct_of_price": 0.04},
        "sector": "Technology", "sector_etf": "XLK", "rs_spy": 0.08, "rs_sector": 0.03,
        "volume_ratio": 1.3, "atr14": 3.0, "dollar_volume_30d": 5e9, "near_high_pct": 3.0,
        "market_regime": "risk_on", "earnings_risk": None, "thesis": "growth breakout thesis",
        "counter_thesis": "fails if SPY rolls over", "reasons": ["breakout"], "warnings": [],
        "rejection_reasons": [], "status": "shadow_open",
    }


def _tables(db):
    conn = sqlite3.connect(str(db))
    try:
        return {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
    finally:
        conn.close()


# ---------------------------------------------------------------- packet ------
def test_packet_empty_db_builds_shadow_only(tmp_path, monkeypatch):
    db = tmp_path / "e.sqlite"
    monkeypatch.setattr(pf_packet, "ticker_context", lambda *a, **k: {"lines": []})
    md = pf_packet.build_packet(None, limit=10, db_path=db)
    assert "SHADOW ONLY" in md
    assert "stocks_swing_growth_breakout" in md
    assert "not actionable" in md.lower() or "must NOT make anything actionable" in md
    assert "NOT live" in md
    assert "no profitability conclusion" in md.lower()
    assert "No open shadow candidates" in md


def test_packet_includes_candidate_and_outcome_summary(tmp_path, monkeypatch):
    db = tmp_path / "c.sqlite"
    # AAPL stays OPEN (candidate block + news); MSFT gets a CLOSED outcome (feeds the summary and is
    # correctly excluded from the open list).
    pf_store.insert_candidates([_candidate("AAPL"), _candidate("MSFT")],
                               created_at="2026-07-02T12:00:00+00:00", db_path=db)
    pf_store.upsert_outcome("spf_MSFT_2026-07-02", checked_at="2026-07-10T00:00:00+00:00",
                            status="closed", fields={"net_pnl_usd": 15.0, "close_reason": "max_hold",
                                                      "notes": {"fees_usd": 0.1, "slippage_usd": 0.5}},
                            db_path=db)
    monkeypatch.setattr(pf_packet, "ticker_context", lambda *a, **k: {"lines": ["news: X (src, 2026-07-01)"]})
    md = pf_packet.build_packet(None, limit=10, db_path=db)
    # open candidate present with its data (MSFT is excluded — it has a terminal outcome)
    assert "AAPL" in md and "breakout" in md and "spf_AAPL_2026-07-02" in md
    # outcome summary is USD-net based; the disclaimer names USD net as authoritative
    assert "USD net" in md and "closed 1" in md
    assert "Authoritative profitability = **USD net**" in md
    # news context surfaced (from the reader, not fabricated)
    assert "news: X" in md


def test_packet_missing_news_is_explicit_not_fabricated(tmp_path, monkeypatch):
    db = tmp_path / "n.sqlite"
    pf_store.insert_candidates([_candidate("NVDA")], created_at="2026-07-02T12:00:00+00:00", db_path=db)
    monkeypatch.setattr(pf_packet, "ticker_context", lambda *a, **k: {"lines": []})   # no local news
    md = pf_packet.build_packet(None, limit=10, db_path=db)
    assert "No reliable ticker-specific news found in local cache" in md


# ---------------------------------------------------------------- reviews -----
def test_parse_reviews_json_and_fenced():
    fenced = ('Here is my review:\n```json\n{"candidate_id":"spf_AAPL_2026-07-02",'
              '"verdict":"wait_pullback","confidence":0.6}\n```\nDone.')
    r = pf_packet.parse_reviews(fenced)
    assert len(r) == 1 and r[0]["candidate_id"] == "spf_AAPL_2026-07-02"
    arr = '[{"candidate_id":"a","verdict":"approve_shadow"},{"candidate_id":"b","verdict":"reject_news_risk"}]'
    assert len(pf_packet.parse_reviews(arr)) == 2
    assert pf_packet.parse_reviews("no json here") == []


def test_ingest_rejects_unknown_and_writes_only_reviews(tmp_path):
    db = tmp_path / "r.sqlite"
    pf_store.insert_candidates([_candidate("AAPL")], created_at="2026-07-02T12:00:00+00:00", db_path=db)
    # unknown candidate_id → not stored
    assert pf_store.candidate_exists("spf_AAPL_2026-07-02", db_path=db) is True
    assert pf_store.candidate_exists("spf_NOPE_2000-01-01", db_path=db) is False
    # known candidate → review stored in the SEPARATE table only
    pf_store.upsert_review("spf_AAPL_2026-07-02", reviewed_at="2026-07-02T13:00:00+00:00",
                           verdict="wait_pullback", confidence=0.6, reasons=["extended"],
                           risk_notes=["earnings in 5d"], db_path=db)
    rv = pf_store.review_for("spf_AAPL_2026-07-02", db_path=db)
    assert rv["verdict"] == "wait_pullback" and rv["confidence"] == 0.6
    names = _tables(db)
    assert "stocks_position_reviews" in names
    assert "proposed_signals" not in names and "signal_outcomes" not in names
    assert "paper_execution_outcomes" not in names and "paper_shadow_execution_outcomes" not in names
    # candidate status is NEVER changed by a review
    row = pf_store.latest_candidates(only_open=True, db_path=db)[0]
    assert row["status"] == "shadow_open"


def test_ingest_cli_unknown_id_skips(tmp_path, monkeypatch):
    from typer.testing import CliRunner
    from src.cli import app
    monkeypatch.setattr(pf_store, "DEFAULT_DB_PATH", tmp_path / "cli.sqlite")
    f = tmp_path / "rev.md"
    f.write_text('```json\n{"candidate_id":"spf_UNKNOWN_2026-01-01","verdict":"approve_shadow"}\n```',
                 encoding="utf-8")
    res = CliRunner().invoke(app, ["ingest-stocks-position-review", "--file", str(f)])
    assert res.exit_code == 0, res.output
    assert "skip unknown candidate_id" in res.output
    assert "Ingested 0" in res.output


# ---------------------------------------------- prepare-analysis dispatch -----
def test_prepare_analysis_stocks_position_cli(tmp_path, monkeypatch):
    from typer.testing import CliRunner
    from src.cli import app
    monkeypatch.setattr(pf_packet, "PACKET_PATH", tmp_path / "pkt.md")
    monkeypatch.setattr(pf_packet, "ticker_context", lambda *a, **k: {"lines": []})
    res = CliRunner().invoke(app, ["prepare-analysis", "--asset-class", "stocks-position"])
    assert res.exit_code == 0, res.output
    assert (tmp_path / "pkt.md").exists()
    assert "SHADOW ONLY" in (tmp_path / "pkt.md").read_text(encoding="utf-8")
