from __future__ import annotations

from src.stocks.agents.market_regime_agent import IndexSnapshot, StocksMarketRegimeAgent


def _snapshot(symbol: str, trend: str, *, above20: bool, above50: bool) -> IndexSnapshot:
    return IndexSnapshot(
        symbol=symbol,
        trend=trend,
        return_5d=0.0,
        return_20d=0.0,
        above_ema20=above20,
        above_ema50=above50,
        last_close=100.0,
    )


def test_shallow_pullback_above_ema50_is_transition_not_risk_off():
    """One weak short-term breadth print cannot manufacture a bearish stock regime."""
    snapshots = [
        _snapshot("SPY", "uptrend", above20=True, above50=True),
        _snapshot("QQQ", "range", above20=False, above50=True),
        _snapshot("IWM", "range", above20=False, above50=True),
        _snapshot("DIA", "range", above20=False, above50=True),
    ]

    regime = StocksMarketRegimeAgent.__new__(StocksMarketRegimeAgent)._classify(
        snapshots, vix_level=15.87, breadth20=0.25, breadth50=1.0,
    )

    assert regime.label == "transition"
    assert regime.bias == "neutral"
    assert regime.risk_on is False


def test_broad_multihorizon_weakness_remains_risk_off():
    snapshots = [
        _snapshot("SPY", "range", above20=False, above50=False),
        _snapshot("QQQ", "range", above20=False, above50=False),
        _snapshot("IWM", "range", above20=True, above50=False),
        _snapshot("DIA", "range", above20=False, above50=True),
    ]

    regime = StocksMarketRegimeAgent.__new__(StocksMarketRegimeAgent)._classify(
        snapshots, vix_level=18.0, breadth20=0.25, breadth50=0.25,
    )

    assert regime.label == "risk_off"
    assert regime.bias == "short"
