"""Tests for PART 10 signal-id stability fix.

Pre-fix: ``signal_id_for()`` hashed ``report_id`` (rotated every cycle)
and 10-digit-precision entry/SL floats (re-computed every cycle as
fresh OHLCV produced new ATR-based zones). Every 2 h cycle therefore
minted a new signal_id for the same setup, inflating row counts 5-15×
for stocks intraday and 1-25× for crypto popular setups.

Post-fix: trade identity = ``(symbol, mode, direction, tier,
calendar_day)``. Entry / SL / TP / report_id / HH:MM are all trading
metadata and live in the upserted row, not in the identity hash. Same
logical trade re-evaluated within the same day therefore maps to the
SAME signal_id, and ``upsert_proposed_signal`` refreshes the row.
"""
from __future__ import annotations

from src.signals.models import signal_id_for


def _id(**kw) -> str:
    defaults = dict(
        symbol="AAPL", mode="intraday", direction="long", tier="B",
        entry_low=459.7113, entry_high=462.43, invalidation=454.27,
        created_at="2026-06-01T10:00:00+00:00",
        report_id="stocks_intraday_20260601T1004",
    )
    defaults.update(kw)
    return signal_id_for(**defaults)


# ---------------------------------------------------------------------------
# Same setup, same day → SAME id (the whole point of PART 10).
# ---------------------------------------------------------------------------


def test_same_setup_same_day_collapses_to_one_id():
    """Cycle 1 (00:04) and cycle 7 (14:04) on the same day must collide."""
    a = _id(report_id="stocks_intraday_20260601T0004",
            created_at="2026-06-01T00:04:00+00:00")
    b = _id(report_id="stocks_intraday_20260601T1404",
            created_at="2026-06-01T14:04:00+00:00")
    assert a == b


def test_entry_zone_wobble_does_NOT_change_id():
    """Re-eval moved entry+SL by 0.5 % — same logical setup, same id."""
    a = _id(entry_low=459.71, entry_high=462.43, invalidation=454.27)
    b = _id(entry_low=462.10, entry_high=465.00, invalidation=456.50)
    assert a == b


def test_large_entry_move_still_same_id_same_day():
    """Same daily thesis even if zone moves materially — identity is the day, not the zone.

    Trader perspective: 'AAPL long intraday today' is one trade. The
    bot may reposition the entry zone multiple times — but it's still
    the same idea being refined, not a brand-new trade.
    """
    a = _id(entry_low=459.0, entry_high=462.0, invalidation=454.0)
    b = _id(entry_low=440.0, entry_high=445.0, invalidation=435.0)
    assert a == b


def test_report_id_does_NOT_affect_id():
    a = _id(report_id="report_A_20260601T0004")
    b = _id(report_id="report_B_20260601T2204")
    assert a == b


def test_versioned_paper_profiles_are_isolated_but_legacy_identity_is_unchanged():
    legacy = _id()
    assert legacy == _id(strategy_identity="")
    pullback = _id(strategy_identity="stocks_intraday_pullback_vwap_paper_v1")
    breakout = _id(strategy_identity="stocks_intraday_breakout_1bar_paper_v1")
    assert pullback != breakout
    assert pullback != legacy


def test_time_of_day_does_NOT_affect_id():
    """Only the calendar day matters, not HH:MM:SS."""
    a = _id(created_at="2026-06-01T00:00:00+00:00")
    b = _id(created_at="2026-06-01T23:59:59+00:00")
    assert a == b


# ---------------------------------------------------------------------------
# Distinct dimensions → DIFFERENT ids.
# ---------------------------------------------------------------------------


def test_different_day_gets_new_id():
    a = _id(created_at="2026-06-01T10:00:00+00:00")
    b = _id(created_at="2026-06-02T10:00:00+00:00")
    assert a != b


def test_different_symbol_distinct():
    assert _id(symbol="AAPL") != _id(symbol="MSFT")


def test_different_direction_distinct():
    assert _id(direction="long") != _id(direction="short")


def test_different_mode_distinct():
    """Scalp vs intraday vs swing on the same symbol-day are different trades."""
    assert _id(mode="intraday") != _id(mode="swing")
    assert _id(mode="scalp") != _id(mode="intraday")


def test_tier_change_forks_signal():
    """C→B promotion is a meaningful identity shift (different alerting policy)."""
    assert _id(tier="C") != _id(tier="B")
    assert _id(tier="A") != _id(tier="B")


# ---------------------------------------------------------------------------
# Format guarantee — downstream tools depend on the shape.
# ---------------------------------------------------------------------------


def test_signal_id_format_stable():
    """Must remain 'sig_<16hex>' for downstream consumers."""
    sid = _id()
    assert sid.startswith("sig_")
    assert len(sid) == 4 + 16
    hex_chars = "0123456789abcdef"
    assert all(c in hex_chars for c in sid[4:])


def test_signal_id_deterministic():
    """Identical inputs always produce identical ids — call twice, compare."""
    assert _id() == _id()
