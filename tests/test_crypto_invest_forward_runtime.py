from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd
import requests

from research_labs.regime_conditioned_continuation.src import forward_shadow as forward


def test_restart_mid_interval_waits_for_next_closed_bar() -> None:
    quarter = 15 * 60
    # 14 minutes after the latest 15m boundary is too late to manufacture a
    # point-in-time decision from that boundary.
    now = quarter + 14 * 60
    assert forward._seconds_until_next_scan(now) == 60 + forward.SCAN_START_DELAY_SECONDS


def test_restart_in_first_two_minutes_runs_the_current_closed_bar() -> None:
    quarter = 15 * 60
    now = quarter + 30
    assert forward._seconds_until_next_scan(now) == 0.0


def test_market_data_falls_back_to_bybit_when_binance_is_unavailable(monkeypatch) -> None:
    expected = pd.DataFrame({"bar_open_at": [pd.Timestamp("2026-08-18T00:00:00Z")]})
    expected.attrs["source"] = "bybit_v5_linear_fallback"

    def unavailable(*_args, **_kwargs):
        raise requests.HTTPError("451")

    monkeypatch.setattr(forward, "_binance_bars", unavailable)
    monkeypatch.setattr(forward, "_bybit_bars", lambda *_args, **_kwargs: (expected, {"open": 1.0}))
    bars, current = forward._bars("BTC/USDT", "15m", 10, datetime.now(timezone.utc))
    assert bars.attrs["source"] == "bybit_v5_linear_fallback"
    assert current == {"open": 1.0}


def test_late_decision_has_a_hard_non_actionable_boundary() -> None:
    cfg = {"max_decision_latency_seconds": 120.0}
    assert forward._decision_is_late(120.0, cfg) is False
    assert forward._decision_is_late(120.001, cfg) is True
