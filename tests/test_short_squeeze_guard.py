"""PART 22 — crypto short squeeze-risk guard (cap-to-C safety layer).

Pins: bounce / thin-liquidity / high-upper-wick shorts are capped to C; a liquid
clean short is NOT capped just for being short; longs are untouched; stop/TP and
global thresholds unchanged.
"""
from __future__ import annotations

import pytest

from src.agents.scoring_agent import ScoringAgent
from src.analysis.short_squeeze_gate import DEFAULTS, assess_short_squeeze
from src.config import load_config
from src.models import MarketRegime, MomentumCandidate, TechnicalSetup
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore


def _kit():
    c = load_config()
    return c, FileStore(c), SQLiteStore(c.db_path)


def _regime(label="bearish trend", btc="downtrend"):
    return MarketRegime(
        label=label, confidence=60.0, risk_mode="risk-off",
        recommended_style="short bias", btc_trend=btc, eth_trend=btc,
        alt_breadth={"above_ema20_pct": 30, "above_ema50_pct": 30},
        volatility={"label": "elevated", "btc_atr_percentile": 90.0},
        key_levels={"BTC/USDT": {"support": 1, "resistance": 2}},
        explanation="t",
    )


def _short_cand(symbol, **kw):
    base = dict(
        symbol=symbol, direction_bias="short", score=72,
        return_24h=-7.0, return_1h=-0.5, relative_strength_btc=-8.0,
        volume_ratio=1.0, atr_percentile=60, distance_from_ema20_atr=-1.0,
        quote_volume_24h_usd=200_000_000.0, upper_wick_atr_max=0.5,
    )
    base.update(kw)
    return MomentumCandidate(**base)


def _short_setup(symbol):
    return TechnicalSetup(
        symbol=symbol, direction="short", timeframe="1h", current_price=100.0,
        entry_low=100.5, entry_high=101.5, invalidation=104.0,
        tp1=95.0, tp2=90.0, tp3=85.0, atr=2.0, rr_to_tp1=2.0,
        setup_quality=85.0, trend="downtrend", support=90.0, resistance=104.0,
    )


# --- pure gate ---

def test_gate_bounce_caps():
    v = assess_short_squeeze(_short_cand("BCH/USDT", return_1h=2.2, distance_from_ema20_atr=0.39,
                                         quote_volume_24h_usd=84e6), params=DEFAULTS)
    assert v.cap and "short_bounce_guard" in v.flags


def test_gate_thin_caps():
    v = assess_short_squeeze(_short_cand("SAHARA/USDT", return_1h=-0.8, distance_from_ema20_atr=-1.8,
                                         quote_volume_24h_usd=5.4e6, upper_wick_atr_max=1.09), params=DEFAULTS)
    assert v.cap and "thin_liquidity_short_squeeze_risk" in v.flags


def test_gate_high_wick_caps():
    v = assess_short_squeeze(_short_cand("DEXE/USDT", return_1h=6.4, distance_from_ema20_atr=1.25,
                                         quote_volume_24h_usd=9e6, upper_wick_atr_max=2.01), params=DEFAULTS)
    assert v.cap
    assert "high_upper_wick_short_squeeze_risk" in v.flags
    assert "short_bounce_guard" in v.flags
    assert "thin_liquidity_short_squeeze_risk" in v.flags


def test_gate_liquid_clean_short_not_capped():
    v = assess_short_squeeze(_short_cand("ETH/USDT", return_1h=-0.9, distance_from_ema20_atr=-1.98,
                                         quote_volume_24h_usd=1.2e9, upper_wick_atr_max=0.63,
                                         volume_ratio=1.41), params=DEFAULTS)
    assert not v.cap  # exhaustion alone is only a warning
    assert "late_short_after_exhaustion" in v.flags


def test_gate_exhaustion_alone_is_warning_only():
    v = assess_short_squeeze(_short_cand("BTC/USDT", return_1h=-0.5, distance_from_ema20_atr=-2.5,
                                         quote_volume_24h_usd=5e9), params=DEFAULTS)
    assert not v.cap
    assert "late_short_after_exhaustion" in v.flags


# --- scoring end-to-end ---

def test_scoring_thin_bounce_short_capped_to_c():
    cfg, store, db = _kit()
    agent = ScoringAgent(cfg, store, db)
    cand = _short_cand("DEXE/USDT", return_1h=6.4, distance_from_ema20_atr=1.25,
                       quote_volume_24h_usd=9e6, upper_wick_atr_max=2.01)
    scores = agent.run([_short_setup("DEXE/USDT")], [cand], _regime(), mode="scalp")
    bd = scores["DEXE/USDT"]
    assert bd.tier == "C", (bd.tier, bd.final_score, bd.cap_reasons)
    assert any("squeeze" in r.lower() for r in bd.cap_reasons)


def test_scoring_liquid_clean_short_not_squeeze_capped():
    cfg, store, db = _kit()
    agent = ScoringAgent(cfg, store, db)
    cand = _short_cand("ETH/USDT", return_1h=-0.9, distance_from_ema20_atr=-1.98,
                       quote_volume_24h_usd=1.2e9, upper_wick_atr_max=0.63, volume_ratio=1.41)
    scores = agent.run([_short_setup("ETH/USDT")], [cand], _regime(), mode="scalp")
    bd = scores["ETH/USDT"]
    assert not any("squeeze" in r.lower() for r in bd.cap_reasons), bd.cap_reasons


def test_scoring_long_unaffected_by_squeeze_guard():
    cfg, store, db = _kit()
    agent = ScoringAgent(cfg, store, db)
    long_setup = TechnicalSetup(
        symbol="SOL/USDT", direction="long", timeframe="1h", current_price=110,
        entry_low=108, entry_high=109, invalidation=104, tp1=115, tp2=120, tp3=125,
        atr=2.5, rr_to_tp1=2.0, setup_quality=85, trend="uptrend", support=105, resistance=112,
    )
    cand = MomentumCandidate(symbol="SOL/USDT", direction_bias="long", score=80,
                             return_24h=4.0, relative_strength_btc=3.0, volume_ratio=1.5,
                             distance_from_ema20_atr=0.6, quote_volume_24h_usd=3e6,
                             upper_wick_atr_max=3.0, return_1h=8.0)
    scores = agent.run([long_setup], [cand], _regime("bullish trend", "uptrend"), mode="scalp")
    bd = scores["SOL/USDT"]
    # thin/high-wick/bounce values present but it's a LONG → no squeeze cap.
    assert not any("squeeze" in r.lower() for r in bd.cap_reasons), bd.cap_reasons


def test_global_thresholds_unchanged():
    cfg, _, _ = _kit()
    th = cfg.scoring.get("thresholds", {})
    assert th.get("a_tier") == 80 and th.get("b_tier") == 65 and th.get("c_tier") == 50
