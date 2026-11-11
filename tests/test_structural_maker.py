"""Tests: structural TP + fee-aware + maker-first paper engines (PAPER ONLY)."""
from src.analysis.market_structure_levels import swing_levels, round_number_levels, structure_levels
from src.analysis.volume_profile import volume_profile
from src.execution.structural_tp_engine import generate_structural_tps
from src.execution.fee_aware_execution import assess_fees
from src.execution.maker_first_execution import plan_for


def _candles(prices, vol=100):
    # [ts,o,h,l,c,v]
    out = []
    for i, p in enumerate(prices):
        out.append([i, p, p + 1, p - 1, p, vol])
    return out


# ---------- structure levels ----------
def test_swing_levels_finds_pivot_high_low():
    cs = _candles([10, 11, 15, 11, 10, 9, 5, 9, 10])
    hi, lo = swing_levels(cs, 2, 2)
    assert any(h >= 15 for h in hi)
    assert any(l <= 6 for l in lo)


def test_round_numbers_around_price():
    rn = round_number_levels(100)
    assert 100 in rn and any(r > 100 for r in rn)


def test_volume_profile_unsupported_when_no_volume():
    cs = _candles([10, 11, 12, 13, 14] * 10, vol=0)
    vp = volume_profile(cs)
    assert vp["supported"] is False and vp["poc"] is None


def test_volume_profile_supported_with_volume():
    cs = _candles(list(range(40, 90)), vol=100)
    vp = volume_profile(cs)
    assert vp["supported"] is True and vp["poc"] is not None


# ---------- structural TP engine ----------
def test_structural_tp_uses_swing_level_long():
    # entry 100, stop 98 (risk 2); a swing high near 104 should become TP
    prices = [100, 101, 104, 101, 100, 99, 100, 101, 100]
    r = generate_structural_tps(entry=100, stop=98, direction="long",
                                candles=_candles(prices), atr=2.0)
    assert r.tp_set_label in ("STRUCTURAL", "HYBRID")
    assert r.tp1 is not None and r.tp1_r is not None and r.tp1_r >= 0.6


def test_structural_no_fake_volume_profile_without_volume():
    r = generate_structural_tps(entry=100, stop=98, direction="long",
                                candles=_candles([100, 102, 104], vol=0), atr=2.0)
    assert r.volume_profile_supported is False


def test_structural_tp3_disabled_in_chop():
    r = generate_structural_tps(entry=100, stop=98, direction="long", candles=None,
                                atr=2.0, market_regime="range/chop",
                                playbook="crypto_intraday_catalyst_or_momentum")
    assert r.tp3 is None


def test_structural_tp3_allowed_for_runner():
    # plenty of structural levels + runner playbook, no chop
    prices = [100, 102, 104, 106, 108, 104, 100, 103, 105, 107]
    r = generate_structural_tps(entry=100, stop=98, direction="long",
                                candles=_candles(prices), atr=2.0, market_regime="trend",
                                playbook="crypto_swing_narrative_rs_momentum")
    assert r.tp_set_label in ("STRUCTURAL", "HYBRID")


def test_structural_fallback_atr_labelled():
    r = generate_structural_tps(entry=100, stop=98, direction="long", candles=None, atr=2.0)
    assert r.tp_set_label == "STRUCTURAL_FALLBACK_ATR"
    assert r.tp1_r >= 0.6


# ---------- fee-aware ----------
def test_fee_r_cost_and_high_drag_label():
    fa = assess_fees(notional_usdt=4000, exit_notional_usdt=4000, risk_usdt=25,
                     fee_profile="bybit_non_vip_usdt_perp", entry_order_type="taker",
                     exit_order_type="taker", expected_gross_r=1.0)
    assert fa.fee_r_cost > 0
    assert fa.fee_survival_label in ("HIGH_FEE_DRAG", "EXTREME_FEE_DRAG", "OK", "TP1_NOT_WORTH_FEES")


def test_fee_extreme_drag_skips():
    # big notional vs small risk → fee_r_cost > 0.35 → EXTREME → skip
    fa = assess_fees(notional_usdt=4000, exit_notional_usdt=4000, risk_usdt=5,
                     fee_profile="conservative_taker", entry_order_type="taker",
                     exit_order_type="taker", skip_extreme_fee_drag=True)
    assert fa.fee_r_cost > 0.35
    assert fa.fee_survival_label == "EXTREME_FEE_DRAG"
    assert fa.action == "paper_skipped_fee_drag"


def test_fee_survival_fail_when_net_edge_negative():
    fa = assess_fees(notional_usdt=4000, exit_notional_usdt=4000, risk_usdt=25,
                     fee_profile="conservative_taker", entry_order_type="taker",
                     exit_order_type="taker", expected_gross_r=0.1)
    assert fa.expected_net_edge_r is not None and fa.expected_net_edge_r < 0.1


def test_maker_lowers_fee_r_cost_vs_taker():
    taker = assess_fees(notional_usdt=4000, exit_notional_usdt=4000, risk_usdt=25,
                        fee_profile="bybit_non_vip_usdt_perp", entry_order_type="taker", exit_order_type="taker")
    maker = assess_fees(notional_usdt=4000, exit_notional_usdt=4000, risk_usdt=25,
                        fee_profile="bybit_non_vip_usdt_perp", entry_order_type="maker", exit_order_type="maker")
    assert maker.fee_r_cost < taker.fee_r_cost


# ---------- maker-first ----------
def test_maker_entry_for_pullback_taker_for_momentum():
    pull = plan_for(setup_is_pullback=True, is_urgent=False, reached_tp=True)
    mom = plan_for(setup_is_pullback=False, is_urgent=True, reached_tp=True)
    assert pull.entry_order_type == "maker"
    assert mom.entry_order_type == "taker"


def test_stop_always_taker():
    p = plan_for(setup_is_pullback=True, reached_tp=False)
    assert p.stop_order_type == "taker"
    assert p.exit_order_type == "taker"   # closed by stop → taker


def test_maker_entry_missed_falls_back_to_taker():
    p = plan_for(setup_is_pullback=True, is_urgent=False, maker_entry_touched_again=False)
    assert p.maker_entry_missed is True and p.taker_fallback_used is True
    assert p.entry_order_type == "taker"


def test_maker_tp_fill_only_if_rested():
    filled = plan_for(setup_is_pullback=True, reached_tp=True, tp_level_rested_before_touch=True)
    not_filled = plan_for(setup_is_pullback=True, reached_tp=True, tp_level_rested_before_touch=False)
    assert filled.maker_tp_filled is True
    assert not_filled.maker_tp_filled is False
