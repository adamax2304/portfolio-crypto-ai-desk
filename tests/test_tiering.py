from __future__ import annotations

from src.agents.scoring_agent import ScoringAgent
from src.config import load_config
from src.models import (
    ExchangeConfirmation,
    MarketRegime,
    MomentumCandidate,
    TechnicalSetup,
)
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore


def _kit():
    config = load_config()
    return config, FileStore(config), SQLiteStore(config.db_path)


def _regime() -> MarketRegime:
    return MarketRegime(
        label="bullish trend",
        confidence=72.0,
        risk_mode="risk-on",
        recommended_style="trend following",
        btc_trend="up",
        eth_trend="up",
        alt_breadth={"above_ema20_pct": 65, "above_ema50_pct": 55},
        volatility={"label": "normal", "atr_percent_median": 1.5},
        key_levels={"BTC/USDT": {"support": 60000, "resistance": 70000}},
        explanation="trend",
    )


def _setup(symbol: str = "SOL/USDT", *, invalidation: float | None = 100.0) -> TechnicalSetup:
    return TechnicalSetup(
        symbol=symbol,
        direction="long",
        timeframe="1h",
        current_price=110.0,
        entry_low=108.0,
        entry_high=109.0,
        invalidation=invalidation,
        tp1=115.0,
        tp2=120.0,
        tp3=125.0,
        atr=2.5,
        rr_to_tp1=2.0,
        setup_quality=78.0,
        trend="uptrend",
        support=105.0,
        resistance=112.0,
    )


def _candidate(symbol: str = "SOL/USDT") -> MomentumCandidate:
    return MomentumCandidate(
        symbol=symbol,
        direction_bias="long",
        score=72,
        return_24h=3.2,
        return_7d=12.0,
        relative_strength_btc=2.4,
        volume_ratio=1.6,
        atr_percentile=60,
        distance_from_ema20_atr=0.6,
        reason_tags=["relative_strength", "volume_expansion"],
    )


def test_no_invalidation_caps_score_at_50() -> None:
    config, store, db = _kit()
    agent = ScoringAgent(config, store, db)
    setup = _setup(invalidation=None)
    candidate = _candidate()
    scores = agent.run([setup], [candidate], _regime())
    breakdown = scores["SOL/USDT"]
    assert breakdown.final_score <= 50
    assert any("invalidation" in reason.lower() for reason in breakdown.cap_reasons)
    assert breakdown.tier == "rejected"


def test_mexc_only_setup_caps_at_b_tier() -> None:
    config, store, db = _kit()
    agent = ScoringAgent(config, store, db)
    setup = _setup()
    candidate = _candidate()
    confirmation = {
        "SOL/USDT": ExchangeConfirmation(
            symbol="SOL/USDT",
            exchanges_listed=["mexc"],
            anchor_listed=False,
            derivatives_listed=False,
            high_risk_only=True,
            confirmation_score=40.0,
            best_exchange_for_data="mexc",
            suggested_exchange_focus="mexc",
        )
    }
    scores = agent.run(
        [setup],
        [candidate],
        _regime(),
        exchange_confirmations=confirmation,
    )
    breakdown = scores["SOL/USDT"]
    assert breakdown.tier in {"B", "C", "rejected"}
    assert breakdown.score_cap is not None
    assert any("mexc" in reason.lower() for reason in breakdown.cap_reasons)


def test_anchor_plus_derivatives_can_reach_a_tier() -> None:
    config, store, db = _kit()
    agent = ScoringAgent(config, store, db)
    setup = _setup()
    setup.setup_quality = 90
    candidate = _candidate()
    candidate.score = 85
    confirmation = {
        "SOL/USDT": ExchangeConfirmation(
            symbol="SOL/USDT",
            exchanges_listed=["binance", "bybit"],
            anchor_listed=True,
            derivatives_listed=True,
            high_risk_only=False,
            confirmation_score=92.0,
            best_exchange_for_data="binance",
            suggested_exchange_focus="binance",
        )
    }
    scores = agent.run(
        [setup],
        [candidate],
        _regime(),
        exchange_confirmations=confirmation,
    )
    breakdown = scores["SOL/USDT"]
    # No caps -> tier reflects the score
    assert breakdown.score_cap is None
    assert breakdown.tier in {"A", "B"}


def test_stale_data_caps_score() -> None:
    config, store, db = _kit()
    agent = ScoringAgent(config, store, db)
    setup = _setup()
    candidate = _candidate()
    scores = agent.run(
        [setup],
        [candidate],
        _regime(),
        data_freshness_minutes=600,
    )
    breakdown = scores["SOL/USDT"]
    assert breakdown.final_score <= 50
    assert any("stale" in reason.lower() for reason in breakdown.cap_reasons)
