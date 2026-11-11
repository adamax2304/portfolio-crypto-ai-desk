from datetime import datetime, timezone

from src.stocks.market_calendar import stock_intraday_target_session


UTC = timezone.utc


def test_after_close_targets_next_cash_session():
    opened, closed = stock_intraday_target_session(
        datetime(2026, 7, 28, 22, 0, tzinfo=UTC)
    )
    assert opened == datetime(2026, 7, 29, 13, 30, tzinfo=UTC)
    assert closed == datetime(2026, 7, 29, 20, 0, tzinfo=UTC)


def test_premarket_targets_same_cash_session():
    opened, closed = stock_intraday_target_session(
        datetime(2026, 7, 29, 12, 0, tzinfo=UTC)
    )
    assert opened == datetime(2026, 7, 29, 13, 30, tzinfo=UTC)
    assert closed == datetime(2026, 7, 29, 20, 0, tzinfo=UTC)


def test_friday_after_close_skips_weekend():
    opened, _closed = stock_intraday_target_session(
        datetime(2026, 7, 31, 22, 0, tzinfo=UTC)
    )
    assert opened == datetime(2026, 8, 3, 13, 30, tzinfo=UTC)


def test_us_holiday_is_not_selected():
    opened, _closed = stock_intraday_target_session(
        datetime(2026, 7, 3, 12, 0, tzinfo=UTC)
    )
    assert opened == datetime(2026, 7, 6, 13, 30, tzinfo=UTC)
