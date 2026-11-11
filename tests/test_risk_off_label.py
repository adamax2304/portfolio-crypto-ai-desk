"""Intraday risk-off / long-bias visibility label (profitability guardrails PART 6).

Asserts the 06-15-like up day does NOT trigger, 06-16/17-like down days DO,
and the label never blocks/sizes (would_throttle_long is a flag only).
"""
from __future__ import annotations

import pandas as pd

from src.risk.risk_off import classify_risk_off, compute_risk_off, RISK_OFF_DAY_PCT


def test_up_day_does_not_trigger():
    out = classify_risk_off(0.89)  # 2026-06-15 BTC +0.89%
    assert out["btc_intraday_risk_off"] is False
    assert out["regime_context"] == "btc_up"
    assert out["would_throttle_long"] is False


def test_down_days_trigger():
    for pct in (-0.99, -0.96):  # 2026-06-16 / 06-17
        out = classify_risk_off(pct)
        assert out["btc_intraday_risk_off"] is True
        assert out["regime_context"] == "btc_risk_off"
        assert out["would_throttle_long"] is True


def test_flat_day_is_btc_flat():
    out = classify_risk_off(0.1)
    assert out["regime_context"] == "btc_flat"
    assert out["btc_intraday_risk_off"] is False


def test_threshold_boundary():
    assert classify_risk_off(RISK_OFF_DAY_PCT)["btc_intraday_risk_off"] is True
    assert classify_risk_off(RISK_OFF_DAY_PCT + 0.01)["btc_intraday_risk_off"] is False


def test_unknown_when_data_missing():
    out = classify_risk_off(None)
    assert out["btc_intraday_risk_off"] is None
    assert out["regime_context"] == "unknown"
    assert out["would_throttle_long"] is False  # never throttle on unknown


def test_1h_down_with_negative_day_triggers():
    out = classify_risk_off(-0.4, h1_trend="down")
    assert out["btc_intraday_risk_off"] is True


def test_compute_risk_off_from_frames():
    class FakeFS:
        def load_ohlcv(self, exchange, symbol, tf):
            if tf == "1d":
                return pd.DataFrame({"open": [100.0], "close": [99.0], "high": [100.5], "low": [98.5]})
            # flat-ish hourly
            closes = [100.0] * 8
            return pd.DataFrame({"open": closes, "close": closes, "high": closes, "low": closes})
    out = compute_risk_off(FakeFS())
    assert out["btc_day_change_pct"] == -1.0
    assert out["btc_intraday_risk_off"] is True


def test_compute_risk_off_fails_open():
    class BadFS:
        def load_ohlcv(self, *a, **k):
            raise RuntimeError("no data")
    out = compute_risk_off(BadFS())
    assert out["regime_context"] == "unknown"
