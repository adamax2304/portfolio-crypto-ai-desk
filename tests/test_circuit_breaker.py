"""Alert-only circuit breaker (profitability guardrails PART 1).

Asserts the would-pause thresholds fire, the breaker never blocks/sizes, and the
store wrapper fails open.
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta

from src.risk.circuit_breaker import (
    CircuitBreakerConfig,
    circuit_breaker_for_signal,
    circuit_breaker_warning_line,
    evaluate_circuit_breaker,
    paper_circuit_breaker_for_signal,
)

NOW = datetime(2026, 6, 17, 15, 0, tzinfo=timezone.utc)


def _stop(*, asset="crypto", mode="intraday", direction="long", r=-1.0,
          regime="bullish trend", h=1):
    return {"final_outcome": "loss", "final_r": r, "stop_hit": 1,
            "asset_class": asset, "mode": mode, "direction": direction,
            "market_regime": regime, "exit_at": (NOW - timedelta(hours=h)).isoformat()}


def _win(*, asset="crypto", mode="intraday", direction="long", r=1.0, h=1):
    return {"final_outcome": "win", "final_r": r, "stop_hit": 0,
            "asset_class": asset, "mode": mode, "direction": direction,
            "market_regime": "bullish trend", "exit_at": (NOW - timedelta(hours=h)).isoformat()}


def test_daily_minus_2r_triggers_would_pause():
    rows = [_stop(r=-1, h=5), _stop(r=-1, h=4)]
    cb = evaluate_circuit_breaker(rows, scope_asset="crypto", scope_mode="intraday", now=NOW)
    assert cb["circuit_breaker_state"] == "would_pause"
    assert cb["circuit_breaker_level"] == 2
    assert cb["day_realized_r"] == -2.0
    assert cb["would_pause_new_entries"] is True
    assert cb["diagnostic_only"] is True


def test_three_stops_triggers_flag_even_if_r_above_2():
    # 3 small stops netting > -2R via a win, but stop COUNT alone trips.
    rows = [_stop(r=-0.5, h=5), _stop(r=-0.5, h=4), _stop(r=-0.5, h=3), _win(r=1.0, h=2)]
    cb = evaluate_circuit_breaker(rows, scope_asset="crypto", scope_mode="intraday", now=NOW)
    assert cb["stops_today"] == 3
    assert cb["would_pause_new_entries"] is True
    assert "stops today" in cb["circuit_breaker_reason"]


def test_minus_3r_is_level_3():
    rows = [_stop(h=6), _stop(h=5), _stop(h=4)]
    cb = evaluate_circuit_breaker(rows, scope_asset="crypto", scope_mode="intraday", now=NOW)
    assert cb["circuit_breaker_level"] == 3
    assert cb["consecutive_stops"] == 3
    assert cb["would_require_fresh_catalyst"] is True


def test_crypto_long_streak_same_regime():
    rows = [_stop(direction="long", h=4), _stop(direction="long", h=3)]
    cb = evaluate_circuit_breaker(rows, scope_asset="crypto", scope_mode="intraday",
                                  scope_regime="bullish trend", now=NOW)
    assert cb["crypto_long_streak_count"] == 2
    assert cb["would_throttle_crypto_longs"] is True


def test_size_stepdown_after_first_stop_is_flag_only():
    rows = [_stop(r=-1, h=3)]
    cb = evaluate_circuit_breaker(rows, scope_asset="crypto", scope_mode="intraday", now=NOW)
    assert cb["would_reduce_size"] is True       # candidate flag
    assert cb["would_pause_new_entries"] is False  # one stop is not a pause
    assert cb["circuit_breaker_state"] == "watch"


def test_clean_day_is_ok_and_no_warning_line():
    rows = [_win(h=3)]
    cb = evaluate_circuit_breaker(rows, scope_asset="crypto", scope_mode="intraday", now=NOW)
    assert cb["circuit_breaker_state"] == "ok"
    assert cb["would_pause_new_entries"] is False
    assert circuit_breaker_warning_line(cb) is None


def test_other_asset_or_other_day_excluded():
    rows = [
        _stop(asset="stocks", h=4), _stop(asset="stocks", h=3),  # different asset
        _stop(h=30),  # yesterday (30h ago)
    ]
    cb = evaluate_circuit_breaker(rows, scope_asset="crypto", scope_mode="intraday", now=NOW)
    assert cb["stops_today"] == 0
    assert cb["circuit_breaker_state"] == "ok"


def test_warning_line_present_when_would_pause():
    rows = [_stop(h=5), _stop(h=4)]
    cb = evaluate_circuit_breaker(rows, scope_asset="crypto", scope_mode="intraday", now=NOW)
    line = circuit_breaker_warning_line(cb)
    assert line and "would pause" in line.lower() and "diagnostic" in line.lower()


def test_store_wrapper_fails_open_on_bad_store():
    class BadStore:
        def load_recent_terminal_outcomes(self, since):
            raise RuntimeError("db down")
    cb = circuit_breaker_for_signal(BadStore(), {"asset_class": "crypto", "mode": "intraday"})
    assert cb["circuit_breaker_state"] == "ok"
    assert cb["would_pause_new_entries"] is False
    assert cb["diagnostic_only"] is True


def test_paper_wrapper_uses_accepted_ledger_rows_only():
    class PaperStore:
        def load_recent_paper_terminal_outcomes(self, since, *, fee_profile):
            return [_stop(h=5), _stop(h=4)]

    cb = paper_circuit_breaker_for_signal(
        PaperStore(), {"asset_class": "crypto", "mode": "intraday", "direction": "long"}, now=NOW
    )
    assert cb["paper_circuit_breaker_state"] == "would_pause"
    assert cb["paper_circuit_breaker_level"] == 2
    assert cb["paper_circuit_breaker_source"] == "accepted_point_in_time_paper_ledger"


def test_config_thresholds_are_alert_only_values():
    cfg = CircuitBreakerConfig()
    assert cfg.daily_r_l2 == -2.0 and cfg.daily_r_l3 == -3.0
    assert cfg.stops_per_day == 3 and cfg.crypto_long_streak == 2
