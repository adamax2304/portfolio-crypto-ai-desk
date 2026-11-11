"""PART 20 — relative-strength leader gate.

In bearish / high-volatility-danger regimes the desk used to reject EVERY
long, including coins that were *rising against* a weak BTC tape. These tests
pin the new behaviour:

* a coin with strong RS vs BTC AND a positive 24h return is a "leader";
* a leader's long gets fair regime alignment, a reduced (not zero) risk
  penalty, and may reach B-tier (capped — never a clean A against the tape);
* a non-leader long in the same regime is still demoted/rejected;
* the technical-setup agent surfaces a counter-tape note (no "conflict"
  keyword) for a leader and the old conflict warning for a non-leader.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.agents.risk_agent import RiskAgent
from src.agents.scoring_agent import ScoringAgent
from src.agents.technical_setup_agent import TechnicalSetupAgent
from src.analysis.relative_strength_gate import (
    gate_params,
    is_relative_strength_leader,
    is_trend_aligned_short,
)
from src.data_collectors.multi_exchange_universe_collector import (
    MultiExchangeUniverseCollector,
)
from src.config import load_config
from src.models import MarketRegime, MomentumCandidate, TechnicalSetup
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore


def _kit():
    config = load_config()
    return config, FileStore(config), SQLiteStore(config.db_path)


def _regime(label: str, btc_trend: str = "downtrend") -> MarketRegime:
    return MarketRegime(
        label=label,
        confidence=60.0,
        risk_mode="risk-off",
        recommended_style="reduce size",
        btc_trend=btc_trend,
        eth_trend=btc_trend,
        alt_breadth={"above_ema20_pct": 35, "above_ema50_pct": 35},
        volatility={"label": "elevated", "btc_atr_percentile": 100.0},
        key_levels={"BTC/USDT": {"support": 60000, "resistance": 70000}},
        explanation="test regime",
    )


def _leader(symbol: str = "NEAR/USDT") -> MomentumCandidate:
    return MomentumCandidate(
        symbol=symbol,
        direction_bias="long",
        score=80,
        return_24h=10.0,
        return_7d=18.0,
        relative_strength_btc=13.0,
        volume_ratio=1.4,
        atr_percentile=70,
        distance_from_ema20_atr=0.8,
        reason_tags=["relative_strength"],
    )


def _laggard(symbol: str = "ABC/USDT") -> MomentumCandidate:
    return MomentumCandidate(
        symbol=symbol,
        direction_bias="long",
        score=78,
        return_24h=-3.0,           # falling with the tape
        return_7d=-9.0,
        relative_strength_btc=1.0,  # barely outperforming
        volume_ratio=1.3,
        atr_percentile=60,
        distance_from_ema20_atr=0.7,
    )


def _setup(symbol: str, *, quality: float = 85.0) -> TechnicalSetup:
    return TechnicalSetup(
        symbol=symbol,
        direction="long",
        timeframe="1h",
        current_price=110.0,
        entry_low=108.0,
        entry_high=109.0,
        invalidation=104.0,
        tp1=115.0,
        tp2=120.0,
        tp3=125.0,
        atr=2.5,
        rr_to_tp1=2.0,
        setup_quality=quality,
        trend="uptrend",
        support=105.0,
        resistance=112.0,
    )


# ---------------------------------------------------------------------------
# 1. Gate helper
# ---------------------------------------------------------------------------


def test_leader_qualifies():
    assert is_relative_strength_leader(_leader()) is True


def test_low_rs_is_not_leader():
    c = _leader()
    c.relative_strength_btc = 2.0  # below 5% floor
    assert is_relative_strength_leader(c) is False


def test_negative_24h_is_not_leader():
    c = _leader()
    c.return_24h = -1.0  # falling, just less than BTC
    assert is_relative_strength_leader(c) is False


def test_missing_data_is_not_leader():
    assert is_relative_strength_leader(None) is False
    c = _leader()
    c.relative_strength_btc = None
    assert is_relative_strength_leader(c) is False


def test_gate_params_reads_config():
    config, _, _ = _kit()
    params = gate_params(config)
    assert params["min_rs_btc"] == 5.0
    assert params["require_positive_24h"] is True


# ---------------------------------------------------------------------------
# 2. Market-alignment boost
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("label", ["bearish trend", "high-volatility danger"])
def test_alignment_leader_beats_non_leader(label):
    config, store, db = _kit()
    agent = ScoringAgent(config, store, db)
    regime = _regime(label)
    leader_align = agent._market_alignment("long", regime, rs_leader=True)
    base_align = agent._market_alignment("long", regime, rs_leader=False)
    assert leader_align > base_align


# ---------------------------------------------------------------------------
# 3. Scoring — leader reaches B in adverse regimes
# ---------------------------------------------------------------------------


def test_danger_leader_long_reaches_b_tier():
    config, store, db = _kit()
    agent = ScoringAgent(config, store, db)
    scores = agent.run(
        [_setup("NEAR/USDT")],
        [_leader("NEAR/USDT")],
        _regime("high-volatility danger"),
        mode="intraday",
    )
    bd = scores["NEAR/USDT"]
    assert bd.tier == "B", (bd.tier, bd.final_score, bd.cap_reasons)
    assert bd.score_cap == 70.0
    assert any("rs-leader" in r.lower() for r in bd.cap_reasons)


def test_bearish_leader_capped_at_b_not_c():
    config, store, db = _kit()
    agent = ScoringAgent(config, store, db)
    scores = agent.run(
        [_setup("NEAR/USDT")],
        [_leader("NEAR/USDT")],
        _regime("bearish trend"),
        mode="intraday",
    )
    bd = scores["NEAR/USDT"]
    assert bd.score_cap == 70.0
    assert any("rs-leader" in r.lower() for r in bd.cap_reasons)


def test_bearish_non_leader_still_capped_at_c():
    config, store, db = _kit()
    agent = ScoringAgent(config, store, db)
    scores = agent.run(
        [_setup("ABC/USDT")],
        [_laggard("ABC/USDT")],
        _regime("bearish trend"),
        mode="intraday",
    )
    bd = scores["ABC/USDT"]
    assert bd.score_cap == 60.0
    assert any("audit cap" in r.lower() for r in bd.cap_reasons)


# ---------------------------------------------------------------------------
# 4. Risk agent — reduced penalty for leaders
# ---------------------------------------------------------------------------


def test_risk_leader_penalised_less_than_laggard():
    config, store, db = _kit()
    agent = RiskAgent(config, store, db)
    regime = _regime("high-volatility danger")
    leader_setup = _setup("NEAR/USDT")
    laggard_setup = _setup("ABC/USDT")
    risks = agent.run(
        [leader_setup, laggard_setup],
        [_leader("NEAR/USDT"), _laggard("ABC/USDT")],
        regime,
        derivatives={},
        catalysts={},
    )
    assert risks["NEAR/USDT"].risk_score < risks["ABC/USDT"].risk_score


# ---------------------------------------------------------------------------
# 5. Technical-setup agent — counter-tape note vs conflict warning
# ---------------------------------------------------------------------------


def _uptrend_frame(rows: int = 140) -> pd.DataFrame:
    base = np.linspace(100.0, 130.0, rows)
    ts = pd.date_range("2026-05-01", periods=rows, freq="1h", tz="UTC")
    return pd.DataFrame(
        {
            "timestamp": ts,
            "open": base,
            "high": base * 1.01,
            "low": base * 0.99,
            "close": base,
            "volume": np.full(rows, 1_000_000.0),
        }
    )


def test_technical_leader_gets_counter_tape_note_not_conflict():
    config, store, db = _kit()
    agent = TechnicalSetupAgent(config, store, db)
    md = {"NEAR/USDT": {"1h": _uptrend_frame()}}
    setups = agent.run([_leader("NEAR/USDT")], md, _regime("high-volatility danger"))
    warnings = " ".join(setups[0].warnings).lower()
    assert "relative-strength leader" in warnings
    assert "conflict" not in warnings


def test_technical_non_leader_gets_conflict_warning():
    config, store, db = _kit()
    agent = TechnicalSetupAgent(config, store, db)
    cand = _laggard("ABC/USDT")
    cand.return_24h = 0.5  # rising a touch, but RS only +1% → not a leader
    cand.relative_strength_btc = 1.0
    md = {"ABC/USDT": {"1h": _uptrend_frame()}}
    setups = agent.run([cand], md, _regime("high-volatility danger"))
    warnings = " ".join(setups[0].warnings).lower()
    assert "conflicts with current market regime" in warnings


# ===========================================================================
# PART 21 — short side: shorts that move WITH a falling tape
# ===========================================================================


def _short_candidate(symbol: str = "BCH/USDT") -> MomentumCandidate:
    return MomentumCandidate(
        symbol=symbol,
        direction_bias="short",
        score=80,
        return_24h=-9.0,
        return_7d=-14.0,
        relative_strength_btc=-10.0,
        volume_ratio=1.4,
        atr_percentile=70,
        distance_from_ema20_atr=-0.8,
        reason_tags=["weak_vs_market", "breakdown"],
    )


def _short_setup(symbol: str = "BCH/USDT") -> TechnicalSetup:
    return TechnicalSetup(
        symbol=symbol,
        direction="short",
        timeframe="1h",
        current_price=110.0,
        entry_low=111.0,
        entry_high=112.0,
        invalidation=116.0,
        tp1=105.0,
        tp2=100.0,
        tp3=95.0,
        atr=2.5,
        rr_to_tp1=2.0,
        setup_quality=85.0,
        trend="downtrend",
        support=95.0,
        resistance=114.0,
    )


# --- gate helper ---


def test_trend_aligned_short_in_downtrend():
    assert is_trend_aligned_short(_short_candidate(), _regime("high-volatility danger", "downtrend")) is True


def test_short_not_aligned_in_uptrend():
    assert is_trend_aligned_short(_short_candidate(), _regime("high-volatility danger", "uptrend")) is False


def test_outperformer_is_not_a_tape_aligned_short():
    c = _short_candidate()
    c.relative_strength_btc = 8.0  # rising vs BTC — never a tape-aligned short
    assert is_trend_aligned_short(c, _regime("high-volatility danger", "downtrend")) is False


def test_trend_aligned_short_none_regime():
    assert is_trend_aligned_short(_short_candidate(), None) is False


# --- alignment ---


def test_short_alignment_danger_downtrend_is_high():
    config, store, db = _kit()
    agent = ScoringAgent(config, store, db)
    danger_down = agent._market_alignment("short", _regime("high-volatility danger", "downtrend"))
    danger_up = agent._market_alignment("short", _regime("high-volatility danger", "uptrend"))
    assert danger_down == pytest.approx(0.84)
    assert danger_down > danger_up


# --- scoring reaches B ---


def test_clean_short_in_volatile_bear_reaches_b():
    config, store, db = _kit()
    agent = ScoringAgent(config, store, db)
    scores = agent.run(
        [_short_setup("BCH/USDT")],
        [_short_candidate("BCH/USDT")],
        _regime("high-volatility danger", "downtrend"),
        mode="intraday",
    )
    bd = scores["BCH/USDT"]
    assert bd.tier in {"A", "B"}, (bd.tier, bd.final_score, bd.cap_reasons)
    assert bd.final_score >= 65


# --- risk reduction ---


def test_risk_trend_aligned_short_penalised_less():
    config, store, db = _kit()
    agent = RiskAgent(config, store, db)
    aligned = agent.run(
        [_short_setup("BCH/USDT")],
        [_short_candidate("BCH/USDT")],
        _regime("high-volatility danger", "downtrend"),
        derivatives={},
        catalysts={},
    )
    not_aligned = agent.run(
        [_short_setup("BCH/USDT")],
        [_short_candidate("BCH/USDT")],
        _regime("high-volatility danger", "uptrend"),
        derivatives={},
        catalysts={},
    )
    assert aligned["BCH/USDT"].risk_score < not_aligned["BCH/USDT"].risk_score


# --- funnel reservation ---


def test_reserve_short_slots_appends_biggest_losers():
    selected = ["UP1/USDT", "UP2/USDT"]
    anchor = [
        {"symbol": "UP1/USDT", "change_24h": 12.0},
        {"symbol": "UP2/USDT", "change_24h": 8.0},
        {"symbol": "DN1/USDT", "change_24h": -12.0, "relative_strength_btc": -9.0},
        {"symbol": "DN2/USDT", "change_24h": -5.0, "relative_strength_btc": -3.0},
        {"symbol": "FLAT/USDT", "change_24h": 1.0},
    ]
    out = MultiExchangeUniverseCollector._reserve_short_slots(selected, anchor, reserve_n=8, cap=40)
    assert "DN1/USDT" in out and "DN2/USDT" in out
    assert out.index("DN1/USDT") < out.index("DN2/USDT")  # most negative first
    assert "FLAT/USDT" not in out  # not a faller


def test_reserve_short_slots_respects_cap_and_zero():
    selected = ["A/USDT"]
    anchor = [{"symbol": f"D{i}/USDT", "change_24h": -float(i)} for i in range(1, 6)]
    capped = MultiExchangeUniverseCollector._reserve_short_slots(selected, anchor, reserve_n=8, cap=3)
    assert len(capped) == 3
    unchanged = MultiExchangeUniverseCollector._reserve_short_slots(selected, anchor, reserve_n=0, cap=40)
    assert unchanged == selected
