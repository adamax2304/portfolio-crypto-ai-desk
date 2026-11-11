"""Tests for the 2026-06-09 paper execution audit additions.

Covers:
- Intrabar entry+stop annotation (PART 1 §A).
- Intrabar entry+TP annotation (PART 1 §B).
- Gap-slip past stop annotation.
- Pre-entry invalidation flag (cosmetic — stop_hit no longer set).
- Headline R-model unchanged for clean cases.

All tests synthesize a tiny OHLCV frame and invoke `_evaluate_signal_walk`
directly (no DB, no file IO). No code path mutates real DB rows.
"""
from __future__ import annotations

import pandas as pd
from datetime import datetime, timezone

from src.signals.tracker import _evaluate_signal_walk


UTC = timezone.utc


def _candle(ts: datetime, o: float, h: float, l: float, c: float) -> dict:
    return {"timestamp": pd.Timestamp(ts), "open": o, "high": h, "low": l, "close": c}


def _frame(candles: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(candles)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    return df


def test_intrabar_entry_stop_long_flags_ambiguous():
    """Long: open inside zone triggers entry; same candle low pierces invalidation."""
    candles = _frame([
        _candle(datetime(2026, 6, 9, 12, 0, tzinfo=UTC), o=100.5, h=101.0, l=97.0, c=99.5),
    ])
    touches = _evaluate_signal_walk(
        direction="long",
        entry_low=100.0, entry_high=101.0, entry_trigger=None,
        invalidation=98.0, tp1=105.0, tp2=110.0, tp3=None,
        candles=candles, same_candle_conservative=True,
    )
    assert touches.triggered, "entry should fire on candle that opens inside zone"
    assert touches.stop_hit, "stop should fire on same candle (low pierced invalidation)"
    assert touches.intrabar_entry_stop is True, "intrabar entry+stop flag must be set"


def test_intrabar_entry_tp_long_flags_ambiguous():
    """Long: open inside zone triggers entry; same candle high reaches TP1."""
    candles = _frame([
        _candle(datetime(2026, 6, 9, 12, 0, tzinfo=UTC), o=100.5, h=106.0, l=100.0, c=105.5),
    ])
    touches = _evaluate_signal_walk(
        direction="long",
        entry_low=100.0, entry_high=101.0, entry_trigger=None,
        invalidation=97.0, tp1=105.0, tp2=110.0, tp3=None,
        candles=candles, same_candle_conservative=True,
    )
    assert touches.triggered and touches.tp1_hit
    assert touches.intrabar_entry_tp is True, "intrabar entry+TP1 flag must be set"


def test_pre_entry_invalidation_does_not_set_stop_hit():
    """Long: invalidation hit on a candle that did NOT touch entry zone.

    Setup: long with entry_zone=[95, 96], invalidation=93.5. Candle prints
    O=94 H=94.5 L=92 C=92.5 — high < entry_low (no overlap with zone) but
    low < invalidation. This must mark pre_entry_invalidation without
    setting stop_hit.
    """
    candles = _frame([
        _candle(datetime(2026, 6, 9, 12, 0, tzinfo=UTC), o=94.0, h=94.5, l=92.0, c=92.5),
    ])
    touches = _evaluate_signal_walk(
        direction="long",
        entry_low=95.0, entry_high=96.0, entry_trigger=None,
        invalidation=93.5, tp1=110.0, tp2=115.0, tp3=None,
        candles=candles, same_candle_conservative=True,
    )
    assert touches.triggered is False, "entry never triggered (zone never touched)"
    assert touches.stop_hit is False, "stop_hit must NOT be set on pre-entry invalidation"
    assert touches.pre_entry_invalidation is True, "pre_entry_invalidation flag must be set"


def test_gap_slip_stop_annotation():
    """Long: candle low pierces well below invalidation — slip annotation populates."""
    candles = _frame([
        _candle(datetime(2026, 6, 9, 12, 0, tzinfo=UTC), o=100.5, h=101.0, l=100.0, c=100.8),
        _candle(datetime(2026, 6, 9, 12, 5, tzinfo=UTC), o=100.0, h=100.0, l=90.0, c=92.0),
    ])
    touches = _evaluate_signal_walk(
        direction="long",
        entry_low=100.0, entry_high=101.0, entry_trigger=None,
        invalidation=98.0, tp1=105.0, tp2=110.0, tp3=None,
        candles=candles, same_candle_conservative=True,
    )
    assert touches.triggered and touches.stop_hit
    assert touches.intrabar_entry_stop is False, "second-candle stop is NOT intrabar entry+stop"
    # invalidation=98, low=90, entry_anchor≈100.5; risk≈2.5; slip = (98-90)/2.5 = 3.2 → 320%
    assert touches.gap_slip_stop_pct_of_risk > 1.0, (
        f"gap_slip_stop must be > 1.0 of risk; got {touches.gap_slip_stop_pct_of_risk}"
    )


def test_clean_win_no_intrabar_flags():
    """Long: entry on bar 1; TP1 on bar 2. Should be a clean win, no ambiguity flags."""
    candles = _frame([
        _candle(datetime(2026, 6, 9, 12, 0, tzinfo=UTC), o=100.5, h=101.0, l=100.0, c=100.8),
        _candle(datetime(2026, 6, 9, 12, 5, tzinfo=UTC), o=101.0, h=106.0, l=100.5, c=105.5),
    ])
    touches = _evaluate_signal_walk(
        direction="long",
        entry_low=100.0, entry_high=101.0, entry_trigger=None,
        invalidation=97.0, tp1=105.0, tp2=110.0, tp3=None,
        candles=candles, same_candle_conservative=True,
    )
    assert touches.triggered and touches.tp1_hit
    assert touches.stop_hit is False
    assert touches.intrabar_entry_stop is False
    assert touches.intrabar_entry_tp is False
    assert touches.pre_entry_invalidation is False


def test_short_intrabar_entry_stop_flags():
    """Short: entry triggers on bar; same bar high pierces invalidation."""
    candles = _frame([
        _candle(datetime(2026, 6, 9, 12, 0, tzinfo=UTC), o=99.5, h=103.0, l=99.0, c=100.5),
    ])
    touches = _evaluate_signal_walk(
        direction="short",
        entry_low=99.0, entry_high=100.0, entry_trigger=None,
        invalidation=102.0, tp1=95.0, tp2=90.0, tp3=None,
        candles=candles, same_candle_conservative=True,
    )
    assert touches.triggered, "short entry should fire (open inside zone)"
    assert touches.stop_hit, "short stop must fire on same bar (high=103 > invalidation=102)"
    assert touches.intrabar_entry_stop is True


def test_same_candle_tp_and_stop_after_entry_still_flagged_ambiguous():
    """Pre-existing behavior: TP and stop in one bar AFTER entry → ambiguous (conservative loss).
    This test re-asserts the audit additions did not regress that path."""
    candles = _frame([
        _candle(datetime(2026, 6, 9, 12, 0, tzinfo=UTC), o=100.5, h=101.0, l=100.0, c=100.8),
        _candle(datetime(2026, 6, 9, 12, 5, tzinfo=UTC), o=101.0, h=106.0, l=96.0, c=100.0),
    ])
    touches = _evaluate_signal_walk(
        direction="long",
        entry_low=100.0, entry_high=101.0, entry_trigger=None,
        invalidation=97.0, tp1=105.0, tp2=110.0, tp3=None,
        candles=candles, same_candle_conservative=True,
    )
    assert touches.triggered
    assert touches.ambiguous, "TP+stop in same bar after entry must remain ambiguous"
    assert touches.stop_hit and touches.tp1_hit
    # intrabar entry+stop/tp should NOT be set here — entry was on a prior bar.
    assert touches.intrabar_entry_stop is False
    assert touches.intrabar_entry_tp is False
