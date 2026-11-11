from __future__ import annotations

from src.live_execution.candle_extremes import completed_post_entry_extreme


class SecondsClient:
    def __init__(self, rows):
        self.rows = rows

    def klines(self, symbol, *, start_seconds, end_seconds):
        return self.rows


class MillisecondsClient:
    def __init__(self, rows):
        self.rows = rows

    def klines(self, symbol, *, start_ms, end_ms):
        return self.rows


def test_pre_fill_high_in_entry_candle_cannot_arm_model_f() -> None:
    base = 999_999_960  # exact one-minute boundary
    client = SecondsClient([
        {"candle_at": base, "high": 101.0, "low": 97.0},
        {"candle_at": base + 60, "high": 99.0, "low": 98.0},
    ])
    # Entry is 16 seconds into the first candle. At +80 seconds the second
    # candle is still open, so neither candle is safe OHLC evidence yet.
    assert completed_post_entry_extreme(
        client, "TEST_USDT", direction="long", entry_at=base + 16, observed_at=base + 80,
    ) is None


def test_only_completed_candles_started_after_fill_contribute_to_long_high() -> None:
    base = 999_999_960  # exact one-minute boundary
    client = SecondsClient([
        {"candle_at": base, "high": 101.0, "low": 97.0},
        {"candle_at": base + 60, "high": 99.0, "low": 98.0},
        {"candle_at": base + 120, "high": 105.0, "low": 96.0},
    ])
    assert completed_post_entry_extreme(
        client, "TEST_USDT", direction="long", entry_at=base + 16, observed_at=base + 121,
    ) == 99.0


def test_bybit_millisecond_rows_use_same_post_fill_rule_for_short_low() -> None:
    base = 999_999_960  # exact one-minute boundary
    client = MillisecondsClient([
        {"candle_at": base * 1000, "high": 102.0, "low": 90.0},
        {"candle_at": (base + 60) * 1000, "high": 101.0, "low": 98.0},
    ])
    assert completed_post_entry_extreme(
        client, "TESTUSDT", direction="short", entry_at=base + 16, observed_at=base + 121,
    ) == 98.0
