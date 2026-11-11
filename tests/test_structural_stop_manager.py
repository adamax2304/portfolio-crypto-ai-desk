"""Tests: structural stop movement after TP (PAPER ONLY)."""
from src.execution.structural_stop_manager import structural_stop_after_tp


def _candles(prices, vol=100):
    return [[i, p, p + 1, p - 1, p, vol] for i, p in enumerate(prices)]


def test_long_moves_to_higher_low_after_tp1():
    # entry 100, stop 98; a swing low ~99 (higher low, above stop) becomes the structural stop
    prices = [100, 99, 101, 99, 102, 100, 103]
    r = structural_stop_after_tp(tp_index=1, entry=100, initial_stop=98, current_stop=98,
                                 direction="long", candles=_candles(prices))
    assert r.moved is True
    assert r.new_stop > 98          # tighter than initial
    assert r.protection_r >= 0.0    # never worse than BE after TP1


def test_fallback_to_be_after_tp1_when_no_structure():
    r = structural_stop_after_tp(tp_index=1, entry=100, initial_stop=98, current_stop=98,
                                 direction="long", candles=None)
    assert r.moved is True and r.structure_used in ("be", "lock")
    assert abs(r.new_stop - 100) < 1e-9   # BE


def test_lock_05r_after_tp2_fallback():
    r = structural_stop_after_tp(tp_index=2, entry=100, initial_stop=98, current_stop=100,
                                 direction="long", candles=None)
    assert r.protection_r >= 0.5   # +0.5R lock after TP2


def test_never_moves_worse_than_current():
    # current stop already at +1R (101); a weaker structure must not loosen it
    r = structural_stop_after_tp(tp_index=2, entry=100, initial_stop=98, current_stop=101,
                                 direction="long", candles=None)
    assert r.new_stop >= 101 - 1e-9


def test_short_moves_to_lower_high():
    # short entry 100, stop 102; swing high ~101 (below stop) → structural stop
    prices = [100, 101, 99, 101, 98, 100, 97]
    r = structural_stop_after_tp(tp_index=1, entry=100, initial_stop=102, current_stop=102,
                                 direction="short", candles=_candles(prices))
    assert r.moved is True and r.new_stop < 102
