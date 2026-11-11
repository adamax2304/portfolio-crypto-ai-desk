from __future__ import annotations

from src.agents.scoring_agent import ScoringAgent
from src.config import load_config
from src.models import (
    MarketRegime,
    MomentumCandidate,
    TechnicalSetup,
)
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore


def _kit():
    config = load_config()
    return config, FileStore(config), SQLiteStore(config.db_path)


def _regime(label: str) -> MarketRegime:
    return MarketRegime(
        label=label,
        confidence=70,
        risk_mode="risk-on" if "bull" in label else "neutral",
        recommended_style="trend",
        btc_trend="up",
        eth_trend="up",
        alt_breadth={"above_ema20_pct": 60, "above_ema50_pct": 55},
        volatility={"label": "normal", "atr_percent_median": 1.5},
        key_levels={"BTC/USDT": {"support": 0, "resistance": 0}},
        explanation="test",
    )


def _setup_and_candidate():
    setup = TechnicalSetup(
        symbol="SOL/USDT",
        direction="long",
        timeframe="1h",
        current_price=110,
        entry_low=108,
        entry_high=109,
        invalidation=105,
        tp1=115,
        tp2=120,
        tp3=125,
        atr=2,
        rr_to_tp1=2.0,
        setup_quality=70,
        trend="uptrend",
        support=105,
        resistance=112,
    )
    candidate = MomentumCandidate(
        symbol="SOL/USDT",
        direction_bias="long",
        score=70,
        return_24h=3,
        return_7d=12,
        relative_strength_btc=2,
        volume_ratio=1.5,
        atr_percentile=55,
        distance_from_ema20_atr=0.6,
        reason_tags=[],
    )
    return setup, candidate


def test_bullish_regime_boosts_momentum_relative_to_range() -> None:
    config, store, db = _kit()
    agent = ScoringAgent(config, store, db)
    setup, candidate = _setup_and_candidate()
    bull = agent.run([setup], [candidate], _regime("bullish trend"))
    chop = agent.run([setup], [candidate], _regime("range/chop"))
    assert bull["SOL/USDT"].components["momentum"] > chop["SOL/USDT"].components["momentum"]


def test_swing_mode_boosts_narrative_vs_scalp() -> None:
    config, store, db = _kit()
    agent = ScoringAgent(config, store, db)
    setup, candidate = _setup_and_candidate()
    scalp = agent.run([setup], [candidate], _regime("bullish trend"), mode="scalp")
    swing = agent.run([setup], [candidate], _regime("bullish trend"), mode="swing")
    assert swing["SOL/USDT"].components["narrative"] > scalp["SOL/USDT"].components["narrative"]
    # Scalp leans on momentum + execution_quality.
    assert scalp["SOL/USDT"].components["momentum"] > swing["SOL/USDT"].components["momentum"]
