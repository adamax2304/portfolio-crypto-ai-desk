"""Mode-Viability-Audit tests — stocks invest watchlist-only soft pause.

The 14d mode viability audit (2026-06-09) found stocks INVEST: 0W/7L A/B
over 14d; stops fire within 1–6 days despite a 30-day validity window;
same tickers/directions/failure anatomy as the already-paused stocks-swing
pipeline. The invest gate caps stocks-invest A/B candidates to C
(watchlist/research only) so they stay visible in reports but are not
Telegram-pushed as actionable A/B entries.

Scope is strictly stocks + invest:
  - stocks intraday is unaffected,
  - stocks swing has its own existing pause (untouched here),
  - crypto (all modes) is unaffected,
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
OPEN_NOW = datetime(2026, 6, 9, 14, 0, tzinfo=UTC)   # Tue 10:00 ET → market open

CAP = "stocks_invest_paused_after_mode_viability_audit"
SWING_CAP = "stocks_swing_paused_after_48h_audit"


def _agent(tmp_path):
    db = SQLiteStore(tmp_path / "t.sqlite")
    db.init_db()
    cfg = load_config()
    scfg = load_stocks_config()
    # This module tests the invest pause only; SI-1..5 has dedicated complete
    # market-context fixtures and must not make this unit test date-dependent.
    scfg.risk["intraday_guards"]["actionability_gates"]["enabled"] = False
    return StockTradeIdeaAgent(cfg, scfg, FileStore(cfg), db), db


def _payloads(symbol="LLY", tier="A"):
    return dict(
        scoring_payload={"scores": [{
            "symbol": symbol, "tier": tier, "direction": "long",
            "final_score": 82.0, "confidence": "high", "cap_reasons": [],
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
# Invest gate — A/B demotion
# ---------------------------------------------------------------------------


def test_invest_Atier_demoted_to_C(tmp_path):
    agent, _ = _agent(tmp_path)
    out = agent.run(**_payloads("LLY", "A"), mode="invest", now=OPEN_NOW)
    assert _tier(out) == "C"
    assert CAP in _caps(out)


def test_invest_Btier_demoted_to_C(tmp_path):
    agent, _ = _agent(tmp_path)
    out = agent.run(**_payloads("AMD", "B"), mode="invest", now=OPEN_NOW)
    assert _tier(out) == "C"
    assert CAP in _caps(out)


def test_invest_demotion_records_demote_reason(tmp_path):
    agent, _ = _agent(tmp_path)
    out = agent.run(**_payloads("LLY", "A"), mode="invest", now=OPEN_NOW)
    caps = _caps(out)
    assert "tier demoted A→C" in caps
    assert CAP in caps


def test_invest_existing_C_still_capped_not_deleted(tmp_path):
    """An invest idea already at C stays present (not deleted) and gets the cap."""
    agent, _ = _agent(tmp_path)
    out = agent.run(**_payloads("LLY", "C"), mode="invest", now=OPEN_NOW)
    assert len(out["ideas"]) == 1          # not deleted
    assert _tier(out) == "C"
    assert CAP in _caps(out)


def test_invest_carries_watchlist_avoid_note(tmp_path):
    agent, _ = _agent(tmp_path)
    out = agent.run(**_payloads("LLY", "A"), mode="invest", now=OPEN_NOW)
    avoid = " | ".join(_idea(out).get("avoid_conditions") or [])
    assert "watchlist-only" in avoid
    assert "mode viability audit" in avoid


# ---------------------------------------------------------------------------
# Scope — intraday / swing / crypto unaffected by INVEST cap
# ---------------------------------------------------------------------------


def test_intraday_not_invest_paused(tmp_path):
    agent, _ = _agent(tmp_path)
    out = agent.run(**_payloads("LLY", "A"), mode="intraday", now=OPEN_NOW)
    assert _tier(out) == "A"
    assert CAP not in _caps(out)


def test_swing_not_carrying_invest_cap_marker(tmp_path):
    """Swing gets its own swing pause, but the INVEST cap must not appear there."""
    agent, _ = _agent(tmp_path)
    out = agent.run(**_payloads("LLY", "A"), mode="swing", now=OPEN_NOW)
    assert _tier(out) == "C"  # swing pause demotes
    assert SWING_CAP in _caps(out)
    assert CAP not in _caps(out)  # the INVEST cap marker must not leak into swing


# ---------------------------------------------------------------------------
# Report rendering — invest watchlist-only banner
# ---------------------------------------------------------------------------


def test_report_renders_invest_watchlist_note():
    from src.stocks.pipelines.stocks_pipeline import StocksPipelineResult
    from src.stocks.reports.stocks_report_builder import build_stocks_report

    result = StocksPipelineResult(mode="invest")
    result.regime = {"regime": {"label": "bullish", "bias": "long"}}
    result.sectors = {}
    result.scoring = {"scores": []}
    result.ideas_payload = {"ideas": []}
    text = build_stocks_report(result)
    assert "STOCKS INVEST — watchlist / research only" in text
    assert "0W/7L over 14d" in text


def test_report_intraday_has_no_invest_note():
    from src.stocks.pipelines.stocks_pipeline import StocksPipelineResult
    from src.stocks.reports.stocks_report_builder import build_stocks_report

    result = StocksPipelineResult(mode="intraday")
    result.regime = {"regime": {"label": "bullish", "bias": "long"}}
    result.sectors = {}
    result.scoring = {"scores": []}
    result.ideas_payload = {"ideas": []}
    text = build_stocks_report(result)
    assert "STOCKS INVEST — watchlist" not in text


def test_report_swing_has_no_invest_note():
    from src.stocks.pipelines.stocks_pipeline import StocksPipelineResult
    from src.stocks.reports.stocks_report_builder import build_stocks_report

    result = StocksPipelineResult(mode="swing")
    result.regime = {"regime": {"label": "bullish", "bias": "long"}}
    result.sectors = {}
    result.scoring = {"scores": []}
    result.ideas_payload = {"ideas": []}
    text = build_stocks_report(result)
    assert "STOCKS INVEST — watchlist" not in text
    assert "STOCKS SWING — watchlist" in text   # swing pause banner persists
