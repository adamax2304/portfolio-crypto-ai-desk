"""PART 17 — persistent legal-flag carry tests.

The pre-fix gate (PART 3) only saw whatever rows ``CompanyNewsAgent``
surfaced via ``load_recent_news(limit=200)``. Once the news feed grew
past 200 rows/cycle, older legal facts (SMCI's March-2026 SDNY
indictment, the May-2026 class-action filings) were silently dropped
and the gate stopped firing for SMCI even though the news was right
there in the DB.

PART 17 adds ``load_active_legal_news()`` which queries news_items
directly across a 90-day window. ``StockTradeIdeaAgent`` unions the
result with the recent-news set BEFORE running ``detect_legal_risk``,
and demotes the tier from A/B → C when the result is blocking.

These tests pin both layers.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pytest

from src.config import load_config
from src.models import NewsItem
from src.storage.sqlite import SQLiteStore
from src.stocks.legal_risk import (
    LEGAL_RISK_PATTERNS,
    detect_legal_risk,
    load_active_legal_news,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_db(tmp_path) -> SQLiteStore:
    db = SQLiteStore(tmp_path / "test.sqlite")
    db.init_db()
    return db


def _insert_news(
    db: SQLiteStore,
    *,
    symbol: str,
    title: str,
    days_ago: int,
    source: str = "test_source_legal",
    url: str | None = None,
) -> None:
    url = url or f"https://example.com/legal/{symbol.lower()}/{days_ago}"
    when = (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()
    item = NewsItem(
        title=title,
        source=source,
        url=url,
        published_at=when,
        detected_symbols=[symbol.upper()],
        detected_narratives=[],
        importance=1.0,
        verification_status="single_source",
    )
    db.save_news_items([item], asset_class="stocks")


# ---------------------------------------------------------------------------
# Loader — basic correctness
# ---------------------------------------------------------------------------


def test_load_active_legal_news_returns_empty_when_no_matches(tmp_path):
    db = _make_db(tmp_path)
    _insert_news(db, symbol="AAPL", title="Apple reports Q3 earnings beat",
                 days_ago=10)
    out = load_active_legal_news(db, ["AAPL"], lookback_days=90)
    assert out["AAPL"] == []


def test_load_active_legal_news_catches_indictment(tmp_path):
    db = _make_db(tmp_path)
    _insert_news(
        db, symbol="SMCI",
        title="Super Micro Computer indictment: SDNY charges 3 executives "
              "with $2.5B Nvidia AI server smuggling",
        days_ago=80,
    )
    out = load_active_legal_news(db, ["SMCI"], lookback_days=90)
    assert len(out["SMCI"]) == 1
    assert "indictment" in out["SMCI"][0]["title"].lower()


def test_load_active_legal_news_excludes_future_of_injected_now(tmp_path):
    db = _make_db(tmp_path)
    as_of = datetime(2026, 6, 4, 14, 0, tzinfo=timezone.utc)
    item = NewsItem(
        title="SMCI indictment filed by DOJ",
        source="test_source_legal",
        url="https://example.com/legal/smci/future",
        published_at=(as_of + timedelta(days=1)).isoformat(),
        detected_symbols=["SMCI"],
        detected_narratives=[],
        importance=1.0,
        verification_status="single_source",
    )
    db.save_news_items([item], asset_class="stocks")

    out = load_active_legal_news(db, ["SMCI"], lookback_days=90, now=as_of)

    assert out["SMCI"] == []


def test_load_active_legal_news_excludes_same_day_future_of_injected_now(tmp_path):
    db = _make_db(tmp_path)
    as_of = datetime(2026, 6, 4, 14, 0, tzinfo=timezone.utc)
    item = NewsItem(
        title="SMCI indictment filed by DOJ",
        source="test_source_legal",
        url="https://example.com/legal/smci/future-same-day",
        published_at=(as_of + timedelta(hours=2)).isoformat(),
        detected_symbols=["SMCI"],
        detected_narratives=[],
        importance=1.0,
        verification_status="single_source",
    )
    db.save_news_items([item], asset_class="stocks")

    out = load_active_legal_news(db, ["SMCI"], lookback_days=90, now=as_of)

    assert out["SMCI"] == []


def test_load_active_legal_news_catches_class_action(tmp_path):
    db = _make_db(tmp_path)
    _insert_news(
        db, symbol="SMCI",
        title="Hagens Berman Files New Securities Class Action Against "
              "Super Micro Computer (SMCI)",
        days_ago=30,
    )
    out = load_active_legal_news(db, ["SMCI"], lookback_days=90)
    assert len(out["SMCI"]) == 1


def test_load_active_legal_news_catches_auditor_resignation(tmp_path):
    db = _make_db(tmp_path)
    _insert_news(
        db, symbol="SMCI",
        title="Ernst & Young resigns as Super Micro Computer auditor",
        days_ago=45,
    )
    out = load_active_legal_news(db, ["SMCI"], lookback_days=90)
    assert len(out["SMCI"]) == 1


def test_load_active_legal_news_respects_90day_window(tmp_path):
    db = _make_db(tmp_path)
    _insert_news(
        db, symbol="SMCI",
        title="Old SMCI accounting fraud allegation",
        days_ago=120,  # outside 90d window
    )
    out = load_active_legal_news(db, ["SMCI"], lookback_days=90)
    assert out["SMCI"] == []


def test_load_active_legal_news_inside_90day_boundary(tmp_path):
    db = _make_db(tmp_path)
    _insert_news(
        db, symbol="SMCI",
        title="SMCI class action lawsuit filed",
        days_ago=88,  # inside 90d window
    )
    out = load_active_legal_news(db, ["SMCI"], lookback_days=90)
    assert len(out["SMCI"]) == 1


def test_loader_persists_indictment_beyond_24h(tmp_path):
    """The whole point of the fix — old indictment must still come back."""
    db = _make_db(tmp_path)
    _insert_news(
        db, symbol="SMCI",
        title="Super Micro Computer Issues Statement on Action by U.S. "
              "Attorney's Office (indictment of 3 executives)",
        days_ago=75,
    )
    # Bury it under fresher non-legal headlines (the same flood pattern that
    # broke PART 3 in production — 200+ unrelated rows from Telegram + RSS).
    for d in range(60):
        _insert_news(
            db, symbol="OTHER",
            title=f"Routine market news item {d}",
            days_ago=0,
        )
    out = load_active_legal_news(db, ["SMCI"], lookback_days=90)
    assert len(out["SMCI"]) == 1, "indictment must survive the 200-row freshness ceiling"


def test_loader_ignores_unrelated_symbol(tmp_path):
    db = _make_db(tmp_path)
    _insert_news(
        db, symbol="AAPL",
        title="SMCI indictment may impact AAPL supplier relationships",
        days_ago=10,
    )
    out = load_active_legal_news(db, ["SMCI"], lookback_days=90)
    # detected_symbols only carries AAPL — the loader respects that mapping.
    assert out["SMCI"] == []


# ---------------------------------------------------------------------------
# Integration with detect_legal_risk
# ---------------------------------------------------------------------------


def test_persistent_news_feeds_blocking_assessment(tmp_path):
    db = _make_db(tmp_path)
    _insert_news(
        db, symbol="SMCI",
        title="Federal indictment unsealed against Super Micro Computer "
              "executives",
        days_ago=70,
    )
    persistent = load_active_legal_news(db, ["SMCI"], lookback_days=90)
    assessment = detect_legal_risk(persistent["SMCI"])
    assert assessment.blocking is True
    assert "indictment" in assessment.categories
    assert assessment.severity == "high"


def test_no_false_positive_on_routine_8k(tmp_path):
    db = _make_db(tmp_path)
    _insert_news(
        db, symbol="MSFT",
        title="Microsoft Corp. - Form 8-K - Item 7.01 Regulation FD Disclosure",
        days_ago=5,
    )
    persistent = load_active_legal_news(db, ["MSFT"], lookback_days=90)
    # Should not match any legal pattern (8-K alone is benign).
    assessment = detect_legal_risk(persistent["MSFT"])
    assert not assessment.blocking


# ---------------------------------------------------------------------------
# Tier demotion — verified end-to-end via the trade idea agent
# ---------------------------------------------------------------------------


def test_smci_a_tier_is_demoted_when_persistent_legal_flag_present(tmp_path):
    """End-to-end: register SMCI legal news → run trade-idea agent →
    SMCI ends up tier C, not A, with manual-review cap_reason."""
    db = _make_db(tmp_path)
    _insert_news(
        db, symbol="SMCI",
        title="SDNY federal indictment of SMCI executives; class action filed",
        days_ago=60,
    )
    # Build the minimal payloads the agent needs.
    from src.storage.file_store import FileStore
    from src.stocks import load_stocks_config
    from src.stocks.agents.trade_idea_agent import StockTradeIdeaAgent

    cfg = load_config()
    scfg = load_stocks_config()
    fs = FileStore(cfg)
    agent = StockTradeIdeaAgent(cfg, scfg, fs, db)

    score_row = {
        "symbol": "SMCI",
        "tier": "A",
        "direction": "long",
        "final_score": 82.26,
        "confidence": "high",
        "cap_reasons": [],
    }
    scoring_payload = {"scores": [score_row]}
    technical_payload = {
        "setups": [
            {
                "symbol": "SMCI",
                "entry_low": 45.0,
                "entry_high": 46.0,
                "invalidation": 43.0,
                "tp1": 50.0,
                "tp2": 52.0,
                "tp3": 55.0,
                "rr_to_tp1": 4.0,
            }
        ]
    }
    news_payload = {"hits_by_symbol": {"SMCI": []}}
    earnings_payload = {"risks": [{"symbol": "SMCI", "severity": "safe"}]}
    rs_payload = {"rows": [{"symbol": "SMCI", "rs_vs_spy_20d": 5.0}]}
    regime_payload = {"regime": {"label": "bullish"}}
    sector_payload = {}
    risk_payload = {"by_symbol": {"SMCI": {"risk_level": "low"}}}

    out = agent.run(
        scoring_payload=scoring_payload,
        technical_payload=technical_payload,
        news_payload=news_payload,
        earnings_payload=earnings_payload,
        rs_payload=rs_payload,
        regime_payload=regime_payload,
        sector_payload=sector_payload,
        risk_payload=risk_payload,
        mode="intraday",
    )
    assert out["ideas"], "agent must still emit the idea (visible for human review)"
    idea = out["ideas"][0]
    assert idea["symbol"] == "SMCI"
    assert idea["tier"] == "C", "active legal flag must demote A→C"
    cap_reasons = " | ".join(idea["cap_reasons"] or [])
    assert "legal_headline_risk" in cap_reasons or "active legal" in cap_reasons
    assert "demoted" in cap_reasons.lower(), cap_reasons


def test_clean_aapl_is_not_demoted(tmp_path):
    """Sanity — no legal news → no demotion."""
    db = _make_db(tmp_path)
    from src.storage.file_store import FileStore
    from src.stocks import load_stocks_config
    from src.stocks.agents.trade_idea_agent import StockTradeIdeaAgent

    cfg = load_config()
    scfg = load_stocks_config()
    # The assertion is about the absence of legal risk, not the independent
    # SI-1..5 packet which needs real-time market evidence.
    scfg.risk["intraday_guards"]["actionability_gates"]["enabled"] = False
    fs = FileStore(cfg)
    agent = StockTradeIdeaAgent(cfg, scfg, fs, db)

    score_row = {
        "symbol": "AAPL", "tier": "A", "direction": "long",
        "final_score": 80.0, "confidence": "high", "cap_reasons": [],
    }
    out = agent.run(
        scoring_payload={"scores": [score_row]},
        technical_payload={"setups": [{
            "symbol": "AAPL", "entry_low": 220, "entry_high": 222,
            "invalidation": 215, "tp1": 230, "tp2": 235, "tp3": 240,
            "rr_to_tp1": 1.5,
        }]},
        news_payload={"hits_by_symbol": {"AAPL": []}},
        earnings_payload={"risks": [{"symbol": "AAPL", "severity": "safe"}]},
        rs_payload={"rows": [{"symbol": "AAPL", "rs_vs_spy_20d": 3.0}]},
        regime_payload={"regime": {"label": "bullish"}},
        sector_payload={},
        risk_payload={"by_symbol": {"AAPL": {"risk_level": "low"}}},
        mode="intraday",
        # P1-fix: pin a market-OPEN clock so the new market-closed intraday
        # gate doesn't demote this clean-AAPL case (test asserts A-tier).
        now=datetime(2026, 6, 4, 14, 0, tzinfo=timezone.utc),
    )
    idea = out["ideas"][0]
    assert idea["tier"] == "A", "clean AAPL must keep A-tier"
