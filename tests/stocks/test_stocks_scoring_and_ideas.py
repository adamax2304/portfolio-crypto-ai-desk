"""Tests for StockScoringAgent + StockTradeIdeaAgent with canned payloads.

No network. The payloads mirror the shape that the upstream agents would
produce, so we can exercise the scoring + idea-generation logic in
isolation.
"""

from __future__ import annotations

from src.config import load_config
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore
from src.stocks import load_stocks_config
from src.stocks.agents import (
    StockRiskAgent,
    StockScoringAgent,
    StockTradeIdeaAgent,
)


def _kit():
    config = load_config()
    scfg = load_stocks_config()
    fs = FileStore(config)
    db = SQLiteStore(config.db_path)
    db.init_db()
    return config, scfg, fs, db


def _regime(label="bullish", bias="long"):
    return {
        "regime": {
            "label": label,
            "bias": bias,
            "risk_on": label in ("bullish", "risk_on", "low_volatility"),
            "high_volatility": label == "high_volatility",
            "vix_level": 14.0,
            "breadth_above_ema20": 0.8,
        },
        "indices": [],
    }


def _sectors():
    return {
        "benchmark": "SPY",
        "benchmark_return_20d": 4.0,
        "sectors": [
            {"sector": "semiconductors", "etf": "SMH", "status": "strong",
             "rs_vs_spy_20d": 6.0, "return_20d": 10.0, "above_ema50": True,
             "return_5d": 2.5},
            {"sector": "energy", "etf": "XLE", "status": "weak",
             "rs_vs_spy_20d": -5.0, "return_20d": -1.0, "above_ema50": False,
             "return_5d": -2.0},
        ],
        "strongest": [], "weakest": [],
    }


def _rs():
    return {
        "benchmarks_return_20d": {"SPY": 4.0, "QQQ": 5.0},
        "rows": [
            {"symbol": "NVDA", "sector": "semiconductors", "sector_etf": "SMH",
             "return_5d": 2.0, "return_20d": 10.0, "rs_vs_spy_20d": 6.0,
             "rs_vs_qqq_20d": 5.0, "rs_vs_sector_20d": 1.0,
             "classification": "leader"},
        ],
    }


def _earnings_safe():
    return {
        "mode": "swing",
        "as_of_date": "2026-05-25",
        "risks": [
            {"symbol": "NVDA", "next_earnings_date": "2026-09-01",
             "days_ahead": 90, "report_time": "AMC", "severity": "safe",
             "note": "safe", "blocks_swing": False, "intraday_high_risk": False},
        ],
        "blocks_swing": [],
        "intraday_warnings": [],
    }


def _technical_clean(direction="long"):
    return {
        "mode": "swing",
        "setups": [{
            "symbol": "NVDA",
            "mode": "swing",
            "direction": direction,
            "trend": "uptrend" if direction == "long" else "downtrend",
            "last_close": 800.0,
            "ema20": 780.0,
            "ema50": 750.0,
            "atr14": 15.0,
            "prev_day_high": 805.0,
            "prev_day_low": 790.0,
            "vwap": None,
            "entry_low": 795.0,
            "entry_high": 800.0,
            "invalidation": 780.0 if direction == "long" else 820.0,
            "tp1": 830.0 if direction == "long" else 770.0,
            "tp2": 850.0 if direction == "long" else 750.0,
            "tp3": 880.0 if direction == "long" else 720.0,
            "rr_to_tp1": 1.5,
            "quality_score": 80.0,
            "notes": [],
        }],
    }


def _news_empty():
    return {"symbols": ["NVDA"], "lookback_limit": 50, "hits_by_symbol": {"NVDA": []}, "has_catalyst": []}


def test_a_or_b_tier_for_clean_long_in_bullish_regime():
    config, scfg, fs, db = _kit()
    risk_agent = StockRiskAgent(config, scfg, fs, db)
    scoring_agent = StockScoringAgent(config, scfg, fs, db)

    regime, sectors, rs, earnings, tech, news = (
        _regime(), _sectors(), _rs(), _earnings_safe(), _technical_clean("long"), _news_empty()
    )
    risk = risk_agent.run(
        regime_payload=regime, sector_payload=sectors, rs_payload=rs,
        earnings_payload=earnings, technical_payload=tech, mode="swing",
    )
    scoring = scoring_agent.run(
        regime_payload=regime, sector_payload=sectors, rs_payload=rs,
        technical_payload=tech, news_payload=news, risk_payload=risk, mode="swing",
    )
    row = scoring["scores"][0]
    assert row["symbol"] == "NVDA"
    # Clean long in a bullish regime with leader RS in a strong sector should
    # be at least B-tier (≥ 65).
    assert row["tier"] in ("A", "B")
    assert row["final_score"] >= 65


def test_rejected_when_no_invalidation():
    config, scfg, fs, db = _kit()
    risk_agent = StockRiskAgent(config, scfg, fs, db)
    scoring_agent = StockScoringAgent(config, scfg, fs, db)

    regime, sectors, rs, earnings, news = (
        _regime(), _sectors(), _rs(), _earnings_safe(), _news_empty()
    )
    tech = _technical_clean("long")
    tech["setups"][0]["invalidation"] = None  # remove invalidation
    risk = risk_agent.run(
        regime_payload=regime, sector_payload=sectors, rs_payload=rs,
        earnings_payload=earnings, technical_payload=tech, mode="swing",
    )
    scoring = scoring_agent.run(
        regime_payload=regime, sector_payload=sectors, rs_payload=rs,
        technical_payload=tech, news_payload=news, risk_payload=risk, mode="swing",
    )
    row = scoring["scores"][0]
    assert row["tier"] == "rejected"
    assert "no_invalidation" in row["blocks"]


def test_trade_idea_agent_produces_stocks_asset_class():
    config, scfg, fs, db = _kit()
    risk_agent = StockRiskAgent(config, scfg, fs, db)
    scoring_agent = StockScoringAgent(config, scfg, fs, db)
    idea_agent = StockTradeIdeaAgent(config, scfg, fs, db)

    regime, sectors, rs, earnings, tech, news = (
        _regime(), _sectors(), _rs(), _earnings_safe(), _technical_clean("long"), _news_empty()
    )
    risk = risk_agent.run(
        regime_payload=regime, sector_payload=sectors, rs_payload=rs,
        earnings_payload=earnings, technical_payload=tech, mode="swing",
    )
    scoring = scoring_agent.run(
        regime_payload=regime, sector_payload=sectors, rs_payload=rs,
        technical_payload=tech, news_payload=news, risk_payload=risk, mode="swing",
    )
    ideas = idea_agent.run(
        scoring_payload=scoring, technical_payload=tech, news_payload=news,
        earnings_payload=earnings, rs_payload=rs, regime_payload=regime,
        sector_payload=sectors, risk_payload=risk, mode="swing",
    )
    # Should produce one stocks-tagged idea. NOTE: stocks SWING is currently
    # capped to C by the swing-pause gate (48h audit), so the idea is C-tier
    # with the pause cap_reason — it stays present (watchlist), not deleted.
    assert ideas["asset_class"] == "stocks"
    assert len(ideas["ideas"]) == 1
    idea = ideas["ideas"][0]
    assert idea["asset_class"] == "stocks"
    assert idea["symbol"] == "NVDA"
    assert idea["mode"] == "swing"
    assert idea["tier"] in ("A", "B", "C")
    if idea["tier"] == "C":
        # When the swing pause is active, the cap_reason marker must be present.
        assert any(
            "stocks_swing_paused_after_48h_audit" in r
            for r in (idea.get("cap_reasons") or [])
        )
