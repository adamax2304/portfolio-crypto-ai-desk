"""Tests for audit fixes #2 + #3: real volume_relative_volume and
real data_confidence in the stocks scoring chain."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.stocks.agents.technical_agent import (
    _compute_data_confidence,
    _volume_ratio,
)


def _frame_with_volume(volumes: list[float]) -> pd.DataFrame:
    n = len(volumes)
    return pd.DataFrame(
        {
            "open": np.linspace(100, 100 + n, n),
            "high": np.linspace(101, 101 + n, n),
            "low": np.linspace(99, 99 + n, n),
            "close": np.linspace(100, 100 + n, n),
            "volume": volumes,
        }
    )


def test_volume_ratio_basic():
    # 20 bars of 100 volume, then a final spike of 200 → ratio ≈ 2.0
    base = [100.0] * 19 + [200.0]
    ratio = _volume_ratio(_frame_with_volume(base), window=20)
    # avg = (19*100 + 200)/20 = 105; last = 200; ratio = 200/105 ≈ 1.905
    assert ratio is not None
    assert 1.85 < ratio < 1.95


def test_volume_ratio_below_one():
    base = [200.0] * 19 + [100.0]
    ratio = _volume_ratio(_frame_with_volume(base), window=20)
    # avg = (19*200 + 100)/20 = 195; last = 100; ratio ≈ 0.513
    assert ratio is not None
    assert 0.50 < ratio < 0.55


def test_volume_ratio_short_history_returns_none():
    base = [100.0] * 10  # less than window
    assert _volume_ratio(_frame_with_volume(base), window=20) is None


def test_volume_ratio_zero_volume_returns_none():
    base = [0.0] * 25
    assert _volume_ratio(_frame_with_volume(base), window=20) is None


def test_data_confidence_full_inputs_intraday():
    ctx = _frame_with_volume([100.0] * 120)
    exec_ = _frame_with_volume([100.0] * 30)
    daily = _frame_with_volume([100.0] * 5)
    score, flags = _compute_data_confidence(
        mode="intraday",
        context_frame=ctx,
        exec_frame=exec_,
        daily_frame=daily,
        prev_h=101.0,
        prev_l=99.0,
        atr_last=1.5,
        volume_ratio=1.2,
        vwap_val=100.5,
    )
    assert score >= 0.95  # all components present
    assert flags == []


def test_data_confidence_swing_does_not_penalize_intraday_frame():
    ctx = _frame_with_volume([100.0] * 120)
    daily = _frame_with_volume([100.0] * 5)
    score, flags = _compute_data_confidence(
        mode="swing",
        context_frame=ctx,
        exec_frame=None,           # not required for swing
        daily_frame=daily,
        prev_h=101.0,
        prev_l=99.0,
        atr_last=1.5,
        volume_ratio=1.0,
        vwap_val=None,              # not required for swing
    )
    # swing should get the "not applicable" credit for exec_frame and VWAP
    assert score >= 0.95
    assert "missing_intraday_exec_frame" not in flags
    assert "missing_vwap" not in flags


def test_data_confidence_missing_inputs_penalize_and_flag():
    ctx = _frame_with_volume([100.0] * 35)  # short history
    score, flags = _compute_data_confidence(
        mode="intraday",
        context_frame=ctx,
        exec_frame=None,
        daily_frame=None,
        prev_h=None,
        prev_l=None,
        atr_last=None,
        volume_ratio=None,
        vwap_val=None,
    )
    assert score <= 0.20
    assert "short_context_history" in flags
    assert "missing_daily_history" in flags
    assert "missing_intraday_exec_frame" in flags
    assert "missing_prev_day_levels" in flags
    assert "missing_atr" in flags
    assert "missing_volume_ratio" in flags
    assert "missing_vwap" in flags


def test_scoring_uses_volume_ratio_and_data_confidence():
    """Round-trip: a setup with high volume_ratio + high data_confidence
    should score the volume + data_confidence components above the
    neutral 0.5 placeholder."""
    from src.config import load_config
    from src.storage.file_store import FileStore
    from src.storage.sqlite import SQLiteStore
    from src.stocks import load_stocks_config
    from src.stocks.agents import StockRiskAgent, StockScoringAgent

    config = load_config()
    scfg = load_stocks_config()
    fs = FileStore(config)
    db = SQLiteStore(config.db_path)
    db.init_db()
    risk_agent = StockRiskAgent(config, scfg, fs, db)
    scoring_agent = StockScoringAgent(config, scfg, fs, db)

    # Minimal canned upstream payloads
    regime = {
        "regime": {"label": "bullish", "bias": "long", "risk_on": True,
                   "high_volatility": False, "vix_level": 14.0,
                   "breadth_above_ema20": 0.8},
        "indices": [],
    }
    sectors = {
        "benchmark": "SPY", "benchmark_return_20d": 4.0,
        "sectors": [{"sector": "semiconductors", "etf": "SMH",
                     "status": "strong", "rs_vs_spy_20d": 6.0,
                     "return_20d": 10.0, "above_ema50": True,
                     "return_5d": 2.5}],
        "strongest": [], "weakest": [],
    }
    rs = {
        "benchmarks_return_20d": {"SPY": 4.0, "QQQ": 5.0},
        "rows": [{"symbol": "NVDA", "sector": "semiconductors",
                  "sector_etf": "SMH", "return_5d": 2.0, "return_20d": 10.0,
                  "rs_vs_spy_20d": 6.0, "rs_vs_qqq_20d": 5.0,
                  "rs_vs_sector_20d": 1.0, "classification": "leader"}],
    }
    earnings = {
        "mode": "swing", "as_of_date": "2026-05-25",
        "risks": [{"symbol": "NVDA", "next_earnings_date": "2026-09-01",
                   "days_ahead": 90, "report_time": "AMC", "severity": "safe",
                   "note": "safe", "blocks_swing": False,
                   "intraday_high_risk": False}],
        "blocks_swing": [], "intraday_warnings": [],
    }
    news = {"hits_by_symbol": {"NVDA": []}, "has_catalyst": []}

    # Two variants: one with a real volume_ratio + high data_confidence,
    # one with neither (fallback to neutral 0.5 placeholders).
    def setup(volume_ratio, data_conf):
        return {
            "symbol": "NVDA", "mode": "swing", "direction": "long",
            "trend": "uptrend", "last_close": 800.0, "ema20": 780.0,
            "ema50": 750.0, "atr14": 15.0, "prev_day_high": 805.0,
            "prev_day_low": 790.0, "vwap": None,
            "volume_ratio": volume_ratio,
            "entry_low": 795.0, "entry_high": 800.0, "invalidation": 780.0,
            "tp1": 830.0, "tp2": 850.0, "tp3": 880.0, "rr_to_tp1": 1.5,
            "quality_score": 80.0, "notes": [],
            "data_confidence_raw": data_conf, "data_flags": [],
        }

    rich_tech = {"mode": "swing", "setups": [setup(2.0, 1.0)]}
    poor_tech = {"mode": "swing", "setups": [setup(None, None)]}

    def run(tech_payload):
        risk = risk_agent.run(
            regime_payload=regime, sector_payload=sectors, rs_payload=rs,
            earnings_payload=earnings, technical_payload=tech_payload,
            mode="swing",
        )
        return scoring_agent.run(
            regime_payload=regime, sector_payload=sectors, rs_payload=rs,
            technical_payload=tech_payload, news_payload=news,
            risk_payload=risk, mode="swing",
        )

    rich = run(rich_tech)["scores"][0]
    poor = run(poor_tech)["scores"][0]

    # Rich version should have a strictly higher volume + data_confidence
    # component contribution than the placeholder fallback.
    assert rich["components"]["volume_relative_volume"] > poor["components"]["volume_relative_volume"]
    assert rich["components"]["data_confidence"] > poor["components"]["data_confidence"]
    # And the final score follows.
    assert rich["final_score"] > poor["final_score"]
