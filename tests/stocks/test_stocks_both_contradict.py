"""Tests for audit fix #4: 'both index AND sector contradict → reject'."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from src.config import load_config
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore
from src.stocks import load_stocks_config
from src.stocks.agents import StockRiskAgent


def _kit(tmp_path: Path):
    config = replace(load_config(), root=tmp_path)
    scfg = load_stocks_config()
    fs = FileStore(config)
    db = SQLiteStore(config.db_path)
    db.init_db()
    return config, scfg, fs, db


def _payloads(*, regime_label="risk_off", regime_bias="short", sector_status="weak", direction="long"):
    regime = {
        "regime": {"label": regime_label, "bias": regime_bias,
                   "risk_on": False, "high_volatility": False, "vix_level": 22.0,
                   "breadth_above_ema20": 0.2},
        "indices": [],
    }
    sectors = {
        "benchmark": "SPY", "benchmark_return_20d": -2.0,
        "sectors": [{"sector": "semiconductors", "etf": "SMH",
                     "status": sector_status, "rs_vs_spy_20d": -5.0,
                     "return_20d": -3.0, "above_ema50": False, "return_5d": -1.0}],
        "strongest": [], "weakest": [],
    }
    rs = {
        "benchmarks_return_20d": {"SPY": -2.0, "QQQ": -3.0},
        "rows": [{"symbol": "NVDA", "sector": "semiconductors", "sector_etf": "SMH",
                  "return_5d": 0.0, "return_20d": -1.0,
                  "rs_vs_spy_20d": 1.0, "rs_vs_qqq_20d": 2.0,
                  "rs_vs_sector_20d": 4.0, "classification": "follower"}],
    }
    earnings = {
        "mode": "swing", "as_of_date": "2026-05-25",
        "risks": [{"symbol": "NVDA", "next_earnings_date": "2026-09-01",
                   "days_ahead": 90, "report_time": "AMC", "severity": "safe",
                   "note": "safe", "blocks_swing": False,
                   "intraday_high_risk": False}],
        "blocks_swing": [], "intraday_warnings": [],
    }
    tech = {
        "mode": "swing",
        "setups": [{
            "symbol": "NVDA", "mode": "swing", "direction": direction,
            "trend": "uptrend" if direction == "long" else "downtrend",
            "last_close": 800.0, "ema20": 780.0, "ema50": 750.0,
            "atr14": 15.0, "prev_day_high": 805.0, "prev_day_low": 790.0,
            "vwap": None, "volume_ratio": 1.5,
            "entry_low": 795.0, "entry_high": 800.0,
            "invalidation": 780.0 if direction == "long" else 820.0,
            "tp1": 830.0 if direction == "long" else 770.0,
            "tp2": 850.0, "tp3": 880.0, "rr_to_tp1": 1.5,
            "quality_score": 70.0, "notes": [],
            "data_confidence_raw": 0.9, "data_flags": [],
        }],
    }
    return regime, sectors, rs, earnings, tech


def test_both_contradict_long_in_risk_off_weak_sector_rejects(tmp_path):
    config, scfg, fs, db = _kit(tmp_path)
    agent = StockRiskAgent(config, scfg, fs, db)
    regime, sectors, rs, earnings, tech = _payloads(
        regime_label="risk_off", regime_bias="short",
        sector_status="weak", direction="long",
    )
    payload = agent.run(
        regime_payload=regime, sector_payload=sectors, rs_payload=rs,
        earnings_payload=earnings, technical_payload=tech, mode="swing",
    )
    info = payload["by_symbol"]["NVDA"]
    assert "both_index_and_sector_contradict" in info["flags"]
    assert "both_index_and_sector_contradict" in info["blocks"]


def test_both_contradict_short_in_bullish_strong_sector_rejects(tmp_path):
    config, scfg, fs, db = _kit(tmp_path)
    agent = StockRiskAgent(config, scfg, fs, db)
    regime, sectors, rs, earnings, tech = _payloads(
        regime_label="bullish", regime_bias="long",
        sector_status="strong", direction="short",
    )
    payload = agent.run(
        regime_payload=regime, sector_payload=sectors, rs_payload=rs,
        earnings_payload=earnings, technical_payload=tech, mode="swing",
    )
    info = payload["by_symbol"]["NVDA"]
    assert "both_index_and_sector_contradict" in info["flags"]
    assert "both_index_and_sector_contradict" in info["blocks"]


def test_only_one_contradiction_does_not_trigger_block(tmp_path):
    """If only the index (or only the sector) disagrees, the trade gets
    penalty/flag but is NOT hard-blocked."""
    config, scfg, fs, db = _kit(tmp_path)
    agent = StockRiskAgent(config, scfg, fs, db)
    # Long in risk_off (index contradicts) but sector is strong (not weak).
    regime, sectors, rs, earnings, tech = _payloads(
        regime_label="risk_off", regime_bias="short",
        sector_status="strong", direction="long",
    )
    payload = agent.run(
        regime_payload=regime, sector_payload=sectors, rs_payload=rs,
        earnings_payload=earnings, technical_payload=tech, mode="swing",
    )
    info = payload["by_symbol"]["NVDA"]
    assert "both_index_and_sector_contradict" not in info["blocks"]


def test_aligned_trade_no_contradiction(tmp_path):
    config, scfg, fs, db = _kit(tmp_path)
    agent = StockRiskAgent(config, scfg, fs, db)
    regime, sectors, rs, earnings, tech = _payloads(
        regime_label="bullish", regime_bias="long",
        sector_status="strong", direction="long",
    )
    payload = agent.run(
        regime_payload=regime, sector_payload=sectors, rs_payload=rs,
        earnings_payload=earnings, technical_payload=tech, mode="swing",
    )
    info = payload["by_symbol"]["NVDA"]
    assert "both_index_and_sector_contradict" not in info["flags"]
    assert info["blocks"] == []
