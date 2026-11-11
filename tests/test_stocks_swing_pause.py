"""P1-fix tests — stocks swing-mode pause (48h audit, Gate C).

The 48h post-fix audit found stocks SWING was the single biggest confirmed
loss bucket (−12R, 0W/12L). Gate C caps stocks-swing A/B candidates to C
(watchlist/research only) so they are no longer Telegram-pushed as actionable
A/B entries. Scope is strictly stocks + swing:
  - stocks intraday / invest are unaffected,
  - crypto (all modes, incl. swing) is unaffected,
  - the signal is NOT deleted — it stays visible as C/watchlist.

Validity/reporting only — no scoring/threshold/stop-TP/crypto changes.
"""
from __future__ import annotations

from datetime import datetime, timezone

from src.config import load_config
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore
from src.stocks import load_stocks_config
from src.stocks.agents.trade_idea_agent import StockTradeIdeaAgent

UTC = timezone.utc
OPEN_NOW = datetime(2026, 6, 4, 14, 0, tzinfo=UTC)   # Thu 10:00 ET → market open

CAP = "stocks_swing_paused_after_48h_audit"


def _agent(tmp_path):
    db = SQLiteStore(tmp_path / "t.sqlite")
    db.init_db()
    cfg = load_config()
    scfg = load_stocks_config()
    # This module tests the swing pause only; SI-1..5 is covered separately.
    scfg.risk["intraday_guards"]["actionability_gates"]["enabled"] = False
    return StockTradeIdeaAgent(cfg, scfg, FileStore(cfg), db), db


def _payloads(symbol="NVDA", tier="A"):
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
        earnings_payload={"risks": [{"symbol": symbol, "severity": "safe"}]},
        rs_payload={"rows": [{"symbol": symbol, "rs_vs_spy_20d": 6.0}]},
        regime_payload={"regime": {"label": "bullish"}},
        sector_payload={},
        risk_payload={"by_symbol": {symbol: {"risk_level": "low"}}},
    )


def _idea(out):
    return out["ideas"][0]


def _tier(out):
    return _idea(out)["tier"]


def _caps(out):
    return " | ".join(_idea(out)["cap_reasons"] or [])


# ---------------------------------------------------------------------------
# Gate C — swing demotion
# ---------------------------------------------------------------------------


def test_swing_Atier_demoted_to_C(tmp_path):
    agent, db = _agent(tmp_path)
    out = agent.run(**_payloads("NVDA", "A"), mode="swing", now=OPEN_NOW)
    assert _tier(out) == "C"
    assert CAP in _caps(out)


def test_swing_Btier_demoted_to_C(tmp_path):
    agent, db = _agent(tmp_path)
    out = agent.run(**_payloads("AMD", "B"), mode="swing", now=OPEN_NOW)
    assert _tier(out) == "C"
    assert CAP in _caps(out)


def test_swing_demotion_records_demote_reason(tmp_path):
    agent, db = _agent(tmp_path)
    out = agent.run(**_payloads("NVDA", "A"), mode="swing", now=OPEN_NOW)
    caps = _caps(out)
    assert "tier demoted A→C" in caps
    assert CAP in caps


def test_swing_existing_C_still_capped_not_deleted(tmp_path):
    """A swing idea already at C stays present (not deleted) and gets the cap."""
    agent, db = _agent(tmp_path)
    out = agent.run(**_payloads("NVDA", "C"), mode="swing", now=OPEN_NOW)
    assert len(out["ideas"]) == 1          # not deleted
    assert _tier(out) == "C"
    assert CAP in _caps(out)


def test_swing_carries_watchlist_avoid_note(tmp_path):
    agent, db = _agent(tmp_path)
    out = agent.run(**_payloads("NVDA", "A"), mode="swing", now=OPEN_NOW)
    avoid = " | ".join(_idea(out).get("avoid_conditions") or [])
    assert "watchlist/research only" in avoid


# ---------------------------------------------------------------------------
# Scope — intraday / invest / crypto-swing unaffected
# ---------------------------------------------------------------------------


def test_intraday_not_swing_paused(tmp_path):
    agent, db = _agent(tmp_path)
    out = agent.run(**_payloads("NVDA", "A"), mode="intraday", now=OPEN_NOW)
    assert _tier(out) == "A"
    assert CAP not in _caps(out)


def test_invest_not_affected_by_swing_cap(tmp_path):
    """Invest gets its own invest-pause cap (separate gate), but the SWING
    cap marker must not appear on an invest idea. Tier will be demoted by
    the invest gate; that is tested in test_stocks_invest_pause.py."""
    agent, db = _agent(tmp_path)
    out = agent.run(**_payloads("NVDA", "A"), mode="invest", now=OPEN_NOW)
    assert CAP not in _caps(out)


# ---------------------------------------------------------------------------
# Report rendering — swing watchlist-only banner
# ---------------------------------------------------------------------------


def test_report_renders_swing_watchlist_note():
    from src.stocks.pipelines.stocks_pipeline import StocksPipelineResult
    from src.stocks.reports.stocks_report_builder import build_stocks_report

    result = StocksPipelineResult(mode="swing")
    result.regime = {"regime": {"label": "bullish", "bias": "long"}}
    result.sectors = {}
    result.scoring = {"scores": []}
    result.ideas_payload = {"ideas": []}
    text = build_stocks_report(result)
    assert "STOCKS SWING — watchlist / research only" in text
    assert "−12R, 0W/12L" in text


def test_report_intraday_has_no_swing_note():
    from src.stocks.pipelines.stocks_pipeline import StocksPipelineResult
    from src.stocks.reports.stocks_report_builder import build_stocks_report

    result = StocksPipelineResult(mode="intraday")
    result.regime = {"regime": {"label": "bullish", "bias": "long"}}
    result.sectors = {}
    result.scoring = {"scores": []}
    result.ideas_payload = {"ideas": []}
    text = build_stocks_report(result)
    assert "STOCKS SWING — watchlist" not in text
