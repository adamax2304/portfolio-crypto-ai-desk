"""Integration-bug fix #2 — the SI-1..SI-5 gate hook must FAIL-CONSERVATIVE, not fail-open.

If the gate context builder / evaluation throws, an intraday A/B candidate MUST be demoted to C
(watchlist/review only) with an explainable `intraday_actionability_gate_error`, never left
actionable without a real gate check. Non-intraday (swing) is unaffected — the hook does not run.
"""
from __future__ import annotations

from datetime import datetime, timezone

from src.config import load_config
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore
from src.stocks import intraday_gate_context as igc
from src.stocks import intraday_guards as ig
from src.stocks import load_stocks_config
from src.stocks.agents import StockRiskAgent, StockScoringAgent, StockTradeIdeaAgent
from src.stocks.agents import trade_idea_agent as tia


def _payloads(mode):
    regime = {"regime": {"label": "bullish", "bias": "long", "risk_on": True, "high_volatility": False,
                         "vix_level": 14.0, "breadth_above_ema20": 0.8}, "indices": []}
    sectors = {"benchmark": "SPY", "benchmark_return_20d": 4.0,
               "sectors": [{"sector": "semiconductors", "etf": "SMH", "status": "strong",
                            "rs_vs_spy_20d": 6.0, "return_20d": 10.0, "above_ema50": True, "return_5d": 2.5}],
               "strongest": [], "weakest": []}
    rs = {"benchmarks_return_20d": {"SPY": 4.0, "QQQ": 5.0},
          "rows": [{"symbol": "NVDA", "sector": "semiconductors", "sector_etf": "SMH", "return_5d": 2.0,
                    "return_20d": 10.0, "rs_vs_spy_20d": 6.0, "rs_vs_qqq_20d": 5.0,
                    "rs_vs_sector_20d": 1.0, "classification": "leader"}]}
    earnings = {"mode": mode, "as_of_date": "2026-05-25",
                "risks": [{"symbol": "NVDA", "next_earnings_date": "2026-09-01", "days_ahead": 90,
                           "report_time": "AMC", "severity": "safe", "note": "safe",
                           "blocks_swing": False, "intraday_high_risk": False}],
                "blocks_swing": [], "intraday_warnings": []}
    tech = {"mode": mode, "setups": [{"symbol": "NVDA", "mode": mode, "direction": "long",
            "trend": "uptrend", "last_close": 800.0, "ema20": 780.0, "ema50": 750.0, "atr14": 15.0,
            "prev_day_high": 805.0, "prev_day_low": 790.0, "vwap": 795.0, "entry_low": 799.0,
            "entry_high": 800.0, "invalidation": 792.0, "tp1": 812.0, "tp2": 824.0, "tp3": 840.0,
            "rr_to_tp1": 1.6, "rr_to_structural_tp1": 1.6, "tp1_source": "structure",
            "quality_score": 85.0, "volume_ratio": 2.0, "notes": []}]}
    news = {"symbols": ["NVDA"], "lookback_limit": 50, "hits_by_symbol": {"NVDA": []}, "has_catalyst": []}
    return regime, sectors, rs, earnings, tech, news


def _run(mode):
    config = load_config(); scfg = load_stocks_config()
    fs = FileStore(config); db = SQLiteStore(config.db_path); db.init_db()
    regime, sectors, rs, earnings, tech, news = _payloads(mode)
    ra, sa, ia = (StockRiskAgent(config, scfg, fs, db), StockScoringAgent(config, scfg, fs, db),
                  StockTradeIdeaAgent(config, scfg, fs, db))
    risk = ra.run(regime_payload=regime, sector_payload=sectors, rs_payload=rs,
                  earnings_payload=earnings, technical_payload=tech, mode=mode)
    scoring = sa.run(regime_payload=regime, sector_payload=sectors, rs_payload=rs,
                     technical_payload=tech, news_payload=news, risk_payload=risk, mode=mode)
    ideas = ia.run(scoring_payload=scoring, technical_payload=tech, news_payload=news,
                   earnings_payload=earnings, rs_payload=rs, regime_payload=regime,
                   sector_payload=sectors, risk_payload=risk, mode=mode,
                   # Keep this gate-isolation test independent of wall-clock time.
                   # 2026-06-04 10:00 ET is a normal RTH session.
                   now=datetime(2026, 6, 4, 14, 0, tzinfo=timezone.utc))
    return ideas["ideas"][0]


def _boom(**k):
    raise RuntimeError("forced gate failure")


def test_intraday_gate_error_fails_conservative(monkeypatch):
    # Neutralize the earlier (market-closed + rolling-drawdown) gates so the actionability hook runs
    # on an A/B candidate, then force the gate to throw.
    monkeypatch.setattr(tia, "is_us_cash_session_open", lambda now: True)
    monkeypatch.setattr(ig, "guard_cap_reasons", lambda *a, **k: [])
    monkeypatch.setattr(igc, "build_context", _boom)
    idea = _run("intraday")
    assert idea["tier"] == "C"                                    # demoted, not left actionable
    ga = (idea.get("raw") or {}).get("intraday_actionability") or {}
    assert ga.get("gate_error") == "RuntimeError"                 # explainable error persisted
    assert ga.get("market_context_status") == "error"
    assert ga.get("demote_reasons") == ["intraday_actionability_gate_error"]
    assert "intraday_actionability_gate_error" in (idea.get("cap_reasons") or [])


def test_swing_unaffected_by_gate_error(monkeypatch):
    # The hook is intraday-only: a swing idea must never carry a gate_error even when build_context
    # would raise (it is never called for swing).
    monkeypatch.setattr(igc, "build_context", _boom)
    idea = _run("swing")
    ga = (idea.get("raw") or {}).get("intraday_actionability") or {}
    assert "gate_error" not in ga
    assert "intraday_actionability_gate_error" not in (idea.get("cap_reasons") or [])
