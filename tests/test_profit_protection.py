"""profit_protection: mode-specific entry fills + Model-F protection + honest baselines.

Same OHLCV path, different entry_mode => different fill/no-fill/entry_price (item 1).
True no_protection baseline (item 2). Realistic net USD via implied exit notional (item 5).
"""
from __future__ import annotations

from pathlib import Path

from src.execution import profit_protection as pp
from src.execution.profit_protection import WalkResult

# One OHLCV path exercised by every mode.
PATH = [
    {"open": 100.2, "high": 100.5, "low": 99.8, "close": 100.1},
    {"open": 100.1, "high": 101.5, "low": 100.0, "close": 101.2},
    {"open": 101.0, "high": 101.0, "low": 99.0, "close": 99.2},
]
GEO = dict(entry_low=99.5, entry_high=100.0, entry_trigger=101.0, suggested=99.9,
           stop=98.0, tp1=104, tp2=106, tp3=110)


def _walk(em):
    return pp.walk(direction="long", entry_mode=em, candles=PATH, **GEO)


def test_momentum_taker_now_fills_first_bar_open():
    w = _walk("MOMENTUM_TAKER_NOW")
    assert w.entered and w.entry_price == 100.2 and w.entry_order_type == "taker" and w.bars_to_entry == 0


def test_pullback_limit_fills_on_trade_through_zone():
    w = _walk("PULLBACK_LIMIT")
    assert w.entered and w.entry_price == 100.0 and w.entry_order_type == "maker" and w.bars_to_entry == 0


def test_structural_retest_fills_at_suggested_level():
    w = _walk("STRUCTURAL_RETEST")
    assert w.entered and w.entry_price == 99.9 and w.entry_order_type == "maker"


def test_breakout_continuation_needs_trigger_cross():
    w = _walk("BREAKOUT_CONTINUATION")
    assert w.entered and w.entry_price == 101.0 and w.entry_order_type == "taker" and w.bars_to_entry == 1


def test_no_chase_skip_never_fills():
    w = _walk("NO_CHASE_SKIP")
    assert not w.entered and w.entry_price is None


def test_modes_produce_distinct_entries_on_same_path():
    entries = {em: _walk(em).entry_price for em in
               ("MOMENTUM_TAKER_NOW", "PULLBACK_LIMIT", "STRUCTURAL_RETEST", "BREAKOUT_CONTINUATION")}
    assert len(set(entries.values())) == 4, entries       # all four differ


def test_limit_then_taker_timeout_takes_taker_after_timeout():
    # a path that NEVER trades into the zone -> maker never fills -> taker fallback at timeout bar
    path = [{"open": 200, "high": 201, "low": 199, "close": 200} for _ in range(5)]
    w = pp.walk(direction="long", entry_mode="LIMIT_THEN_TAKER_TIMEOUT", entry_low=150, entry_high=151,
                entry_trigger=None, suggested=150.5, stop=140, tp1=170, tp2=180, tp3=190,
                candles=path, timeout_bars=2)
    assert w.entered and w.entry_order_type == "taker" and w.taker_fallback_used == 1 and w.bars_to_entry == 2


# ---- true no-protection baseline (item 2) ----

def _prot(mfe, hit_stop=False, expired=False, t1=False, t2=False, t3=False):
    wr = WalkResult(entered=True, entry_price=100.0, mfe_r=mfe, hit_stop=hit_stop, expired=expired,
                    reached_tp1=t1, reached_tp2=t2, reached_tp3=t3)
    return pp.protect(direction="long", entry=100.0, stop=98.0, tp1=104, tp2=106, tp3=110,
                      walk_result=wr, symbol="ETH/USDT", fee_profile="bybit_non_vip_usdt_perp")


def test_true_no_protection_full_loss_when_reversed():
    r = _prot(mfe=0.7, hit_stop=True)                     # +0.6R armed -> protected 0R
    assert r.net_r == 0.0                                 # protected = breakeven
    assert r.no_protection_r == -1.0                      # TRUE no-protection = original stop
    assert r.delta_vs_no_protection_r == 1.0              # protection saved +1R
    assert r.legacy_touch_r == -1.0 and r.delta_vs_legacy_touch_r == 1.0


def test_true_no_protection_partial_then_stop():
    r = _prot(mfe=2.5, hit_stop=True, t1=True)            # TP1 then reversed to stop
    # R1 = (104-100)/2 = 2 ; no_protection = 0.33*2 + 0.67*(-1) = -0.01 ; protected (locked) = +0.5
    assert abs(r.no_protection_r - (-0.01)) < 1e-6
    assert r.net_r == 0.5 and abs(r.delta_vs_no_protection_r - 0.51) < 1e-6


def test_no_protection_differs_from_legacy_touch():
    # TP1 touched then reversed: legacy_touch books the FULL R1 (=2.0); true no-protection does not.
    r = _prot(mfe=2.5, hit_stop=True, t1=True)
    assert r.legacy_touch_r == 2.0 and r.no_protection_r != r.legacy_touch_r


def test_realistic_net_usd_and_implied_exit_price():
    r = _prot(mfe=1.3, hit_stop=True)                     # locked +0.5R
    assert r.risk_usd == 25.0 and r.net_usd is not None and r.net_usd < 0.5 * 25.0  # fees drag
    # exit price implied from R: entry + 0.5*|entry-stop| = 100 + 0.5*2 = 101.0
    assert abs(r.exit_price - 101.0) < 1e-6


def test_no_chase_skip_has_no_pnl():
    wr = WalkResult(entered=True, entry_price=100.0, mfe_r=1.0, reached_tp1=True)
    r = pp.protect(direction="long", entry=100.0, stop=98.0, tp1=104, tp2=106, tp3=110,
                   walk_result=wr, symbol="X", entry_mode="NO_CHASE_SKIP")
    assert r.skipped and r.net_r is None and r.net_usd is None


def test_every_entry_mode_uses_protection_in_sim():
    # +0.7R then reverse to stop for each fillable mode -> breakeven (0R), never -1R
    candles = [{"open": 100, "high": 100, "low": 100, "close": 100},
               {"open": 100, "high": 101.4, "low": 100, "close": 101.4},
               {"open": 101, "high": 101, "low": 97.9, "close": 98}]
    for em in ("PULLBACK_LIMIT", "STRUCTURAL_RETEST", "BREAKOUT_CONTINUATION",
               "MOMENTUM_TAKER_NOW", "LIMIT_THEN_TAKER_TIMEOUT"):
        res = pp.simulate_from_geometry(direction="long", entry_low=99.5, entry_high=100.5,
                                        entry_trigger=100.0, suggested=100.0, stop=98.0,
                                        tp1=104, tp2=106, tp3=110, candles=candles, entry_mode=em, symbol="X")
        assert res.entered, em
        assert res.close_reason == "breakeven_stop" and res.net_r == 0.0, (em, res.close_reason, res.net_r)


# ---- same-candle entry/exit realism (item 3) ----

def _walk_single(bar):
    # MOMENTUM_TAKER_NOW fills at the first bar open -> entry is deterministic on this one candle
    return pp.walk(direction="long", entry_mode="MOMENTUM_TAKER_NOW", entry_low=None, entry_high=None,
                   entry_trigger=None, suggested=100.0, stop=98.0, tp1=104, tp2=106, tp3=110, candles=[bar])


def test_entry_and_stop_same_candle():
    w = _walk_single({"open": 100, "high": 100.5, "low": 97.0, "close": 98})  # dips to stop, no TP
    assert w.entered and w.entry_price == 100 and w.hit_stop is True
    assert not (w.reached_tp1 or w.reached_tp2 or w.reached_tp3) and not w.same_candle_ambiguous


def test_entry_and_tp_same_candle():
    w = _walk_single({"open": 100, "high": 104.5, "low": 99.5, "close": 104})  # spikes to TP1, no stop
    assert w.entered and w.reached_tp1 is True and w.hit_stop is False and not w.same_candle_ambiguous


def test_entry_tp_and_stop_same_candle_ambiguous():
    w = _walk_single({"open": 100, "high": 104.5, "low": 97.0, "close": 101})  # both stop and TP in the bar
    assert w.entered and w.same_candle_ambiguous is True and w.hit_stop is True and w.reached_tp1 is True


# ---- same-candle realism for maker/limit fills (item 2, conservative) ----

def _walk_maker(bar, em="PULLBACK_LIMIT", **geo):
    d = dict(entry_low=99.5, entry_high=100.0, entry_trigger=None, suggested=99.9,
             stop=98.0, tp1=104, tp2=106, tp3=110)
    d.update(geo)
    return pp.walk(direction="long", entry_mode=em, candles=[bar], **d)


def test_momentum_open_same_candle_tp_counts():
    w = _walk_maker({"open": 100, "high": 104.5, "low": 99.5, "close": 104}, em="MOMENTUM_TAKER_NOW")
    assert w.entry_at_open is True and w.reached_tp1 is True and w.same_candle_ambiguous is False


def test_maker_tradethrough_plus_tp_is_ambiguous_not_clean_tp():
    # open ABOVE zone -> maker fills via low trade-through (NOT at open); same-candle high hits TP
    w = _walk_maker({"open": 101, "high": 104.5, "low": 99.8, "close": 102})
    assert w.entered and w.entry_at_open is False and w.entry_price == 100.0
    assert w.reached_tp1 is False and w.same_candle_ambiguous is True   # TP not credited


def test_maker_fill_at_open_inside_zone_can_count_tp():
    w = _walk_maker({"open": 99.8, "high": 104.5, "low": 99.5, "close": 104})
    assert w.entry_at_open is True and w.reached_tp1 is True and w.same_candle_ambiguous is False


def test_maker_fill_plus_stop_plus_tp_is_stop_first_ambiguous():
    w = _walk_maker({"open": 101, "high": 104.5, "low": 97.0, "close": 100})
    assert w.hit_stop is True and w.reached_tp1 is False and w.same_candle_ambiguous is True


def test_module_has_no_live_order_surface():
    src = Path(pp.__file__).read_text(encoding="utf-8").lower()
    for bad in ("create_order", "place_order", "submit_order", "auto_live", "manual_live", "final_r ="):
        assert bad not in src
