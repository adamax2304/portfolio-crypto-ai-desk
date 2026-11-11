"""P1-fix tests — market-closed intraday gate + post-earnings stale gate.

Pins the two stock signal-validity fixes from the 12h audit:
  Gate A — no actionable A/B intraday stock entry while US cash session closed.
  Gate B — news-confirmed earnings print + calendar UNKNOWN invalidates a
           stale pre-earnings setup (AVGO regression).
Reporting/validity only — no scoring/threshold/stop-TP/crypto changes.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from src.config import load_config
from src.models import NewsItem
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore
from src.stocks import load_stocks_config
from src.stocks.agents.trade_idea_agent import StockTradeIdeaAgent
from src.stocks.market_calendar import (
    is_us_cash_session_open,
    us_session_label,
)
from src.stocks.earnings_freshness import load_recent_earnings_news

UTC = timezone.utc
OPEN_NOW = datetime(2026, 6, 4, 14, 0, tzinfo=UTC)    # Thu 10:00 ET (DST) → open
CLOSED_NOW = datetime(2026, 6, 4, 1, 6, tzinfo=UTC)   # Wed 21:06 ET → closed (audit cluster)
WEEKEND_NOW = datetime(2026, 6, 6, 14, 0, tzinfo=UTC)  # Saturday
HOLIDAY_NOW = datetime(2026, 7, 3, 14, 0, tzinfo=UTC)  # NYSE holiday (observed Jul 4)


# ---------------------------------------------------------------------------
# market calendar
# ---------------------------------------------------------------------------


def test_session_open_during_rth():
    assert is_us_cash_session_open(OPEN_NOW) is True
    assert us_session_label(OPEN_NOW) == "regular session"


def test_session_closed_overnight():
    assert is_us_cash_session_open(CLOSED_NOW) is False


def test_session_closed_weekend():
    assert is_us_cash_session_open(WEEKEND_NOW) is False
    assert us_session_label(WEEKEND_NOW) == "weekend"


def test_session_closed_holiday():
    assert is_us_cash_session_open(HOLIDAY_NOW) is False
    assert us_session_label(HOLIDAY_NOW) == "holiday"


# ---------------------------------------------------------------------------
# agent harness
# ---------------------------------------------------------------------------


def _agent(tmp_path):
    db = SQLiteStore(tmp_path / "t.sqlite")
    db.init_db()
    cfg = load_config()
    scfg = load_stocks_config()
    # These tests isolate the market-closed / earnings-validity rules.  SI-1..5
    # has its own fixtures and requires a complete OHLCV/sector/catalyst packet.
    scfg.risk["intraday_guards"]["actionability_gates"]["enabled"] = False
    return StockTradeIdeaAgent(cfg, scfg, FileStore(cfg), db), db


def _payloads(symbol="AMD", tier="A", severity="safe"):
    return dict(
        scoring_payload={"scores": [{
            "symbol": symbol, "tier": tier, "direction": "long",
            "final_score": 88.0, "confidence": "high", "cap_reasons": [],
        }]},
        technical_payload={"setups": [{
            "symbol": symbol, "entry_low": 100.0, "entry_high": 101.0,
            "invalidation": 97.0, "tp1": 106.0, "tp2": 110.0, "tp3": 115.0,
            "rr_to_tp1": 2.0,
        }]},
        news_payload={"hits_by_symbol": {symbol: []}},
        earnings_payload={"risks": [{"symbol": symbol, "severity": severity}]},
        rs_payload={"rows": [{"symbol": symbol, "rs_vs_spy_20d": 6.0}]},
        regime_payload={"regime": {"label": "bullish"}},
        sector_payload={},
        risk_payload={"by_symbol": {symbol: {"risk_level": "low"}}},
    )


def _insert_earnings_news(db, symbol, title, hours_ago=2, now=OPEN_NOW):
    when = (now - timedelta(hours=hours_ago)).isoformat()
    db.save_news_items([NewsItem(
        title=title, source="Reuters",
        url=f"https://example.com/earn/{symbol}/{hours_ago}",
        published_at=when, detected_symbols=[symbol], detected_narratives=[],
        importance=2.0,
    )], asset_class="stocks")


def _tier(out):
    return out["ideas"][0]["tier"]


def _caps(out):
    return " | ".join(out["ideas"][0]["cap_reasons"] or [])


# ---------------------------------------------------------------------------
# Gate A — market-closed intraday
# ---------------------------------------------------------------------------


def test_intraday_Atier_demoted_when_market_closed(tmp_path):
    agent, db = _agent(tmp_path)
    out = agent.run(**_payloads("AMD", "A"), mode="intraday", now=CLOSED_NOW)
    assert _tier(out) == "C"
    assert "market_closed_intraday_planning_only" in _caps(out)


def test_intraday_Atier_kept_when_market_open(tmp_path):
    agent, db = _agent(tmp_path)
    out = agent.run(**_payloads("AMD", "A"), mode="intraday", now=OPEN_NOW)
    assert _tier(out) == "A"
    assert "market_closed" not in _caps(out)


def test_intraday_demoted_on_weekend(tmp_path):
    agent, db = _agent(tmp_path)
    out = agent.run(**_payloads("AMD", "B"), mode="intraday", now=WEEKEND_NOW)
    assert _tier(out) == "C"
    assert "market_closed_intraday_planning_only" in _caps(out)


def test_swing_not_affected_by_market_closed_gate(tmp_path):
    """Gate A (market-closed) targets intraday only — it must not be the reason
    swing is capped. Swing IS capped, but by Gate C (swing-pause), never by the
    market_closed_intraday reason."""
    agent, db = _agent(tmp_path)
    out = agent.run(**_payloads("AMD", "A"), mode="swing", now=CLOSED_NOW)
    # capped to C, but specifically NOT by the market-closed intraday gate.
    assert "market_closed_intraday_planning_only" not in _caps(out)


def test_invest_not_affected_by_market_closed_or_swing_caps(tmp_path):
    """The market-closed and swing-pause caps both ignore invest mode.
    Invest has its own pause gate (mode-viability audit 2026-06-09); the
    point of this test is only to verify that neither the market-closed
    cap nor the swing cap markers leak onto invest ideas."""
    agent, db = _agent(tmp_path)
    out = agent.run(**_payloads("AMD", "A"), mode="invest", now=CLOSED_NOW)
    # Invest IS capped to C by its own gate — that's expected and tested in
    # tests/test_stocks_invest_pause.py. We assert only that the OTHER caps
    # do not leak onto invest.
    assert "market_closed_intraday_planning_only" not in _caps(out)
    assert "stocks_swing_paused_after_48h_audit" not in _caps(out)


# ---------------------------------------------------------------------------
# Gate B — post-earnings stale (AVGO regression)
# ---------------------------------------------------------------------------


def test_avgo_stale_post_earnings_demoted(tmp_path):
    agent, db = _agent(tmp_path)
    _insert_earnings_news(db, "AVGO", "Broadcom reports Q2 FY2026 results, beats estimates")
    # market OPEN to isolate Gate B; calendar severity UNKNOWN (the bug).
    out = agent.run(**_payloads("AVGO", "A", severity="unknown"), mode="intraday", now=OPEN_NOW)
    assert _tier(out) == "C"
    assert "stale_post_earnings_setup" in _caps(out)


def test_unknown_calendar_does_not_override_without_news(tmp_path):
    """Earnings UNKNOWN but NO earnings news → not stale (normal unknown)."""
    agent, db = _agent(tmp_path)
    out = agent.run(**_payloads("AMD", "A", severity="unknown"), mode="intraday", now=OPEN_NOW)
    assert _tier(out) == "A"
    assert "stale_post_earnings_setup" not in _caps(out)


def test_known_safe_calendar_not_flagged_stale(tmp_path):
    """Calendar says safe (knows next earnings) + earnings news → news does NOT
    override a known-good calendar; only UNKNOWN is treated as blind."""
    agent, db = _agent(tmp_path)
    _insert_earnings_news(db, "AMD", "AMD reports Q1 results, beats estimates")
    out = agent.run(**_payloads("AMD", "A", severity="safe"), mode="intraday", now=OPEN_NOW)
    assert _tier(out) == "A"
    assert "stale_post_earnings_setup" not in _caps(out)


def test_etf_not_applicable_never_stale(tmp_path):
    """ETF earnings = not_applicable must never be flagged stale."""
    agent, db = _agent(tmp_path)
    _insert_earnings_news(db, "SMH", "Semiconductor ETF SMH Q2 results recap, revenue beats")
    out = agent.run(**_payloads("SMH", "A", severity="not_applicable"), mode="intraday", now=OPEN_NOW)
    assert _tier(out) == "A"
    assert "stale_post_earnings_setup" not in _caps(out)


def test_future_earnings_news_not_treated_as_print(tmp_path):
    """'X to report next week' is future-tense → not a print → no stale flag."""
    agent, db = _agent(tmp_path)
    _insert_earnings_news(db, "AVGO", "Broadcom to report Q2 earnings next week, preview")
    out = agent.run(**_payloads("AVGO", "A", severity="unknown"), mode="intraday", now=OPEN_NOW)
    assert _tier(out) == "A"
    assert "stale_post_earnings_setup" not in _caps(out)


def test_future_dated_earnings_news_is_not_visible_at_injected_now(tmp_path):
    """A replay at OPEN_NOW must not see a print published after OPEN_NOW."""
    agent, db = _agent(tmp_path)
    _insert_earnings_news(
        db,
        "AVGO",
        "Broadcom reports Q2 FY2026 results, beats estimates",
        now=OPEN_NOW + timedelta(days=1),
    )
    out = agent.run(**_payloads("AVGO", "A", severity="unknown"), mode="intraday", now=OPEN_NOW)
    assert _tier(out) == "A"
    assert "stale_post_earnings_setup" not in _caps(out)


def test_same_day_future_earnings_news_is_not_visible_at_injected_now(tmp_path):
    """The indexed coarse date range must still reject a later same-day row."""
    agent, db = _agent(tmp_path)
    _insert_earnings_news(
        db,
        "AVGO",
        "Broadcom reports Q2 FY2026 results, beats estimates",
        hours_ago=0,
        now=OPEN_NOW + timedelta(hours=2),
    )
    assert load_recent_earnings_news(db, ["AVGO"], now=OPEN_NOW) == {}
