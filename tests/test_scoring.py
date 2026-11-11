from __future__ import annotations

import pytest

from src.agents.scoring_agent import ScoringAgent
from src.config import load_config
from src.models import MarketRegime, MomentumCandidate, TechnicalSetup
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore


# ---------------------------------------------------------------------------
# Fixtures shared by PART 11 regime-cap tests
# ---------------------------------------------------------------------------


def _make_regime(label: str) -> MarketRegime:
    return MarketRegime(
        label=label,
        confidence=80,
        risk_mode="risk-off" if "bear" in label else "risk-on",
        recommended_style="short bias" if "bear" in label else "selective longs",
        btc_trend="downtrend" if "bear" in label else "uptrend",
        eth_trend="downtrend" if "bear" in label else "uptrend",
        alt_breadth={"above_ema20_pct": 30 if "bear" in label else 70},
        volatility={"state": "normal"},
        key_levels={},
        explanation="test regime",
    )


def _make_setup(direction: str = "long", symbol: str = "SOL/USDT") -> TechnicalSetup:
    return TechnicalSetup(
        symbol=symbol,
        direction=direction,
        timeframe="1h",
        current_price=100,
        entry_low=98,
        entry_high=99,
        invalidation=96,
        tp1=104,
        tp2=108,
        tp3=112,
        atr=2,
        rr_to_tp1=1.6,
        setup_quality=80,
        trend="uptrend",
    )


@pytest.fixture
def agent(tmp_path):
    config = load_config()
    db = SQLiteStore(tmp_path / "test.sqlite")
    db.init_db()
    return ScoringAgent(config, FileStore(config), db)


def test_scoring_agent_caps_incomplete_data(tmp_path) -> None:
    config = load_config()
    db = SQLiteStore(tmp_path / "test.sqlite")
    db.init_db()
    agent = ScoringAgent(config, FileStore(config), db)
    regime = MarketRegime(
        label="bullish trend",
        confidence=80,
        risk_mode="risk-on",
        recommended_style="selective longs",
        btc_trend="uptrend",
        eth_trend="uptrend",
        alt_breadth={"above_ema20_pct": 70},
        volatility={"state": "normal"},
        key_levels={},
        explanation="test",
    )
    setup = TechnicalSetup(
        symbol="SOL/USDT",
        direction="long",
        timeframe="1h",
        current_price=100,
        entry_low=98,
        entry_high=99,
        invalidation=96,
        tp1=104,
        tp2=108,
        tp3=112,
        atr=2,
        rr_to_tp1=1.6,
        setup_quality=80,
        trend="uptrend",
    )
    candidate = MomentumCandidate(symbol="SOL/USDT", direction_bias="long", score=80)
    scores = agent.run([setup], [candidate], regime)
    assert 0 <= scores["SOL/USDT"].final_score <= 100
    assert scores["SOL/USDT"].data_quality == "acceptable"


# ---------------------------------------------------------------------------
# PART 11 — regime cap for crypto intraday longs / shorts
#
# The audit (AUDIT_PAPER_TRADING.md §3.1) found crypto intraday B-tier longs
# returned -0.75 R avg when the regime was bearish-trend. The fix caps those
# at score 60 so they never reach B-tier (≥65) — they become watchlist-only.
# ---------------------------------------------------------------------------


def test_intraday_long_in_bearish_regime_is_capped(agent):
    """A strong long setup must NOT reach B-tier in a bearish-trend regime."""
    candidate = MomentumCandidate(symbol="SOL/USDT", direction_bias="long", score=85)
    scores = agent.run(
        [_make_setup(direction="long")],
        [candidate],
        _make_regime("bearish trend"),
        mode="intraday",
    )
    breakdown = scores["SOL/USDT"]
    assert breakdown.final_score <= 60, breakdown.final_score
    assert breakdown.tier in {"C", "rejected"}
    assert any("audit cap" in r for r in breakdown.cap_reasons), breakdown.cap_reasons


def test_intraday_short_in_bullish_regime_is_capped(agent):
    """Symmetric — strong short setup must NOT reach B-tier in bullish trend."""
    candidate = MomentumCandidate(symbol="SOL/USDT", direction_bias="short", score=85)
    setup = _make_setup(direction="short")
    scores = agent.run(
        [setup],
        [candidate],
        _make_regime("bullish trend"),
        mode="intraday",
    )
    breakdown = scores["SOL/USDT"]
    assert breakdown.final_score <= 60, breakdown.final_score
    assert any("audit cap" in r for r in breakdown.cap_reasons)


def test_swing_long_in_bearish_regime_NOT_capped(agent):
    """Swing bucket was +2.25R in the audit — must keep its scoring intact."""
    candidate = MomentumCandidate(symbol="SOL/USDT", direction_bias="long", score=85)
    scores = agent.run(
        [_make_setup(direction="long")],
        [candidate],
        _make_regime("bearish trend"),
        mode="swing",
    )
    # Swing must NOT pick up the audit cap text.
    assert not any("audit cap" in r for r in scores["SOL/USDT"].cap_reasons)


def test_scalp_long_in_bearish_regime_NOT_capped(agent):
    """Scalp bucket was +0.00R (breakeven) — left alone for now per audit."""
    candidate = MomentumCandidate(symbol="SOL/USDT", direction_bias="long", score=85)
    scores = agent.run(
        [_make_setup(direction="long")],
        [candidate],
        _make_regime("bearish trend"),
        mode="scalp",
    )
    assert not any("audit cap" in r for r in scores["SOL/USDT"].cap_reasons)




def test_intraday_long_in_bullish_regime_unaffected(agent):
    """Bullish regime + long = aligned trade — cap must NOT fire."""
    candidate = MomentumCandidate(symbol="SOL/USDT", direction_bias="long", score=85)
    scores = agent.run(
        [_make_setup(direction="long")],
        [candidate],
        _make_regime("bullish trend"),
        mode="intraday",
    )
    assert not any("audit cap" in r for r in scores["SOL/USDT"].cap_reasons)


def test_intraday_long_in_range_regime_unaffected(agent):
    """Range / chop is ambiguous — cap fires only on clear trend conflict."""
    candidate = MomentumCandidate(symbol="SOL/USDT", direction_bias="long", score=85)
    scores = agent.run(
        [_make_setup(direction="long")],
        [candidate],
        _make_regime("range/chop"),
        mode="intraday",
    )
    assert not any("audit cap" in r for r in scores["SOL/USDT"].cap_reasons)


# ---------------------------------------------------------------------------
# PART 14a — BTC-trend-aware market_alignment in ambiguous regimes
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def _scoring_agent_for_alignment(tmp_path_factory):
    """Module-scoped agent — created once, reused across alignment tests
    to avoid Windows SQLite file-handle cleanup failures."""
    from src.config import load_config
    from src.storage.file_store import FileStore
    from src.storage.sqlite import SQLiteStore
    from src.agents.scoring_agent import ScoringAgent

    cfg = load_config()
    db_path = tmp_path_factory.mktemp("scoring") / "t.sqlite"
    db = SQLiteStore(db_path)
    db.init_db()
    return ScoringAgent(cfg, FileStore(cfg), db)


def _alignment(_scoring_agent_for_alignment, direction: str, regime_label: str, btc_trend: str) -> float:
    """Helper — call the private _market_alignment with a minimal regime."""
    regime = MarketRegime(
        label=regime_label, confidence=70,
        risk_mode="risk-off" if "bear" in regime_label else "risk-on",
        recommended_style="x",
        btc_trend=btc_trend, eth_trend=btc_trend,
        alt_breadth={"above_ema20_pct": 50},
        volatility={"state": "normal"}, key_levels={}, explanation="t",
    )
    return _scoring_agent_for_alignment._market_alignment(direction, regime)


def test_short_in_high_vol_with_btc_downtrend_gets_boost(_scoring_agent_for_alignment):
    """The audit fix — short alignment must jump from 0.58 → 0.74 when BTC trends down."""
    boosted = _alignment(_scoring_agent_for_alignment, "short", "high-volatility danger", "downtrend")
    flat = _alignment(_scoring_agent_for_alignment, "short", "high-volatility danger", "sideways")
    assert boosted > flat
    assert boosted >= 0.7


def test_short_in_range_with_btc_downtrend_gets_boost(_scoring_agent_for_alignment):
    """Same boost for the `range/chop` ambiguous regime."""
    assert _alignment(_scoring_agent_for_alignment, "short", "range/chop", "downtrend") >= 0.7
    assert _alignment(_scoring_agent_for_alignment, "short", "range/chop", "uptrend") == 0.58


def test_long_in_range_with_btc_uptrend_gets_boost(_scoring_agent_for_alignment):
    """Symmetric — long alignment also gets the BTC-trend boost."""
    assert _alignment(_scoring_agent_for_alignment, "long", "range/chop", "uptrend") >= 0.7
    assert _alignment(_scoring_agent_for_alignment, "long", "range/chop", "downtrend") == 0.58


def test_clean_trend_regimes_unchanged(_scoring_agent_for_alignment):
    """Bullish + long stays 0.90, bearish + short stays 0.88."""
    assert _alignment(_scoring_agent_for_alignment, "long", "bullish trend", "uptrend") == 0.9
    assert _alignment(_scoring_agent_for_alignment, "short", "bearish trend", "downtrend") == 0.88


def test_high_volatility_trend_rewards_only_aligned_direction(_scoring_agent_for_alignment):
    long_aligned = _alignment(_scoring_agent_for_alignment, "long", "high-volatility trend", "uptrend")
    long_counter = _alignment(_scoring_agent_for_alignment, "long", "high-volatility trend", "downtrend")
    short_aligned = _alignment(_scoring_agent_for_alignment, "short", "high-volatility trend", "downtrend")
    assert long_aligned == 0.8
    assert short_aligned == 0.8
    assert long_counter < long_aligned


def test_counter_trend_in_clean_regime_stays_low(_scoring_agent_for_alignment):
    """Long against bearish trend stays 0.25 regardless of BTC trend."""
    assert _alignment(_scoring_agent_for_alignment, "long", "bearish trend", "downtrend") == 0.25
    assert _alignment(_scoring_agent_for_alignment, "short", "bullish trend", "uptrend") == 0.25


# ---------------------------------------------------------------------------
# PART 14b — MEXC / Bybit / OKX fallback in DerivativesAgent
# ---------------------------------------------------------------------------


def test_derivatives_agent_falls_back_to_mexc_when_binance_empty(tmp_path):
    """When Binance returns no record, the agent uses the MEXC fallback
    payload from external_records and marks data_available=True."""
    from src.agents.derivatives_agent import DerivativesAgent
    from src.config import load_config
    from src.storage.file_store import FileStore
    from src.storage.sqlite import SQLiteStore
    import pandas as pd

    cfg = load_config()
    db = SQLiteStore(tmp_path / "t.sqlite")
    db.init_db()
    agent = DerivativesAgent(cfg, FileStore(cfg), db)
    market_data = {
        "OBSCURE/USDT": {
            "1h": pd.DataFrame({"close": [1.0, 0.95, 0.90, 0.85]}),
        }
    }
    binance = {"OBSCURE/USDT": {}}  # no Binance data
    external = {
        "OBSCURE/USDT": {
            "exchanges": {
                "mexc": {
                    "funding_rate": -0.0008,
                    "open_interest": 1234567.0,
                    "price_24h_pct": -0.05,
                }
            }
        }
    }
    out = agent.run(market_data, binance, external_records=external)
    summary = out["OBSCURE/USDT"]
    assert summary.data_available is True, summary
    assert summary.funding_rate == -0.0008
    assert "fallback_via_mexc" in summary.interpretation


def test_derivatives_agent_prefers_mexc_over_bybit_over_okx(tmp_path):
    from src.agents.derivatives_agent import DerivativesAgent
    from src.config import load_config
    from src.storage.file_store import FileStore
    from src.storage.sqlite import SQLiteStore
    import pandas as pd

    cfg = load_config()
    db = SQLiteStore(tmp_path / "t.sqlite")
    db.init_db()
    agent = DerivativesAgent(cfg, FileStore(cfg), db)
    market_data = {"X/USDT": {"1h": pd.DataFrame({"close": [1.0, 1.05]})}}
    external = {
        "X/USDT": {
            "exchanges": {
                "okx":   {"funding_rate": 0.0003, "open_interest": 100.0},
                "bybit": {"funding_rate": 0.0002, "open_interest": 200.0},
                "mexc":  {"funding_rate": 0.0001, "open_interest": 300.0},
            }
        }
    }
    out = agent.run(market_data, {"X/USDT": {}}, external_records=external)
    assert "fallback_via_mexc" in out["X/USDT"].interpretation


def test_derivatives_agent_falls_back_when_all_three_missing(tmp_path):
    """If no venue has data, return data_available=False — no fabrication."""
    from src.agents.derivatives_agent import DerivativesAgent
    from src.config import load_config
    from src.storage.file_store import FileStore
    from src.storage.sqlite import SQLiteStore
    import pandas as pd

    cfg = load_config()
    db = SQLiteStore(tmp_path / "t.sqlite")
    db.init_db()
    agent = DerivativesAgent(cfg, FileStore(cfg), db)
    market_data = {"GHOST/USDT": {"1h": pd.DataFrame({"close": [1.0]})}}
    out = agent.run(market_data, {"GHOST/USDT": {}}, external_records={"GHOST/USDT": {"exchanges": {}}})
    assert out["GHOST/USDT"].data_available is False
