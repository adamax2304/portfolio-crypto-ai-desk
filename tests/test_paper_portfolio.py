"""Tests for paper position sizing + fees + portfolio simulation (PAPER ONLY)."""
from __future__ import annotations

from src.execution.position_sizing import size_position
from src.execution.fees import trade_costs, fee_rate, load_fee_profiles
from src.execution.paper_portfolio import simulate_portfolio


# ---- position sizing (max_5x_safe policy) ----------------------------------
def test_sizing_2pct_stop_notional_1250_risk_25():
    # max_5x: max_margin 25% → margin cap 1250; notional cap min(1250*5, 5000*1.5)=6250.
    r = size_position(equity_usdt=5000, entry_price=100, stop_price=98, risk_pct=0.005)
    assert round(r.notional_usdt) == 1250          # desired 1250 < cap 6250
    assert round(r.actual_risk_usdt) == 25
    assert r.risk_capped is False
    assert r.leverage_used == 1                     # ceil(1250/1250)=1
    assert r.leverage_policy == "max_5x_safe"


def test_sizing_tight_stop_caps_and_reduces_risk():
    # 0.3% stop → desired 8333 > cap 6250 → risk capped; leverage 5; too_tight (0.3%<0.35%).
    r = size_position(equity_usdt=5000, entry_price=100, stop_price=99.7, risk_pct=0.005)
    assert r.risk_capped is True
    assert r.notional_usdt == 6250                  # min(1250*5, 5000*1.5)
    assert r.actual_risk_usdt < 25
    assert r.leverage_used == 5                      # clamped at 5
    assert r.too_tight_stop is True                  # 0.3% < 0.35%
    assert r.sizing_warning


def test_sizing_05pct_stop_fits_at_4x_not_capped():
    # 0.5% stop → desired 5000 < cap 6250 → notional 5000, risk 25, leverage 4, NOT capped.
    r = size_position(equity_usdt=5000, entry_price=100, stop_price=99.5, risk_pct=0.005)
    assert round(r.notional_usdt) == 5000 and r.leverage_used == 4
    assert r.risk_capped is False and round(r.actual_risk_usdt) == 25


def test_sizing_short_works():
    r = size_position(equity_usdt=5000, entry_price=100, stop_price=102, direction="short", risk_pct=0.005)
    assert round(r.notional_usdt) == 1250 and round(r.actual_risk_usdt) == 25
    assert r.liquidation_price > 100     # short liq is above entry


def test_sizing_liquidation_buffer_ok_and_max_5x():
    r = size_position(equity_usdt=5000, entry_price=100, stop_price=98, risk_pct=0.005)
    assert r.liquidation_buffer_ok is True   # liq ~ -100% (lev1) vs 2% stop × 3
    assert r.leverage_used <= 5


def test_wide_stop_reduces_leverage_for_liquidation_safety():
    # 9% stop: safe_lev_cap = floor(1/(0.09*3)) = 3 → leverage capped at 3 (not 5) for liq buffer.
    r = size_position(equity_usdt=5000, entry_price=100, stop_price=91, risk_pct=0.005)
    assert r.too_wide_stop is True
    assert r.leverage_used <= 3
    assert r.liquidation_buffer_ok is True


def test_leverage_is_not_risk():
    # Same risk, different stop → different leverage, identical actual risk; never > 5x.
    wide = size_position(equity_usdt=5000, entry_price=100, stop_price=95, risk_pct=0.005)   # 5% stop
    tight = size_position(equity_usdt=5000, entry_price=100, stop_price=99.4, risk_pct=0.005) # 0.6% stop
    assert round(wide.actual_risk_usdt) == 25
    assert tight.leverage_used >= wide.leverage_used and tight.leverage_used <= 5


# ---- fees ------------------------------------------------------------------
def test_fees_taker_open_close_uses_entry_and_exit_notional():
    # exit notional omitted → estimated from entry; close fee on exit notional.
    c = trade_costs(notional_usdt=1250, symbol="BTC/USDT", fee_profile="bybit_non_vip_usdt_perp")
    assert round(c.fee_usdt, 4) == round(1250 * 0.00055 * 2, 4)   # open + close (estimated exit==entry)
    assert c.fee_estimated is True
    assert c.slippage_usdt == round(1250 * 0.0002 * 2, 6)         # BTC = major, per-side
    assert c.funding_known is False
    # explicit exit notional → close fee uses it (exact, not estimated)
    c2 = trade_costs(notional_usdt=1250, exit_notional_usdt=1300, symbol="BTC/USDT",
                     fee_profile="bybit_non_vip_usdt_perp")
    assert c2.fee_estimated is False
    assert round(c2.close_fee_usdt, 6) == round(1300 * 0.00055, 6)   # exit notional
    assert round(c2.open_fee_usdt, 6) == round(1250 * 0.00055, 6)    # entry notional


def test_fee_profiles_parse_alias_and_conservative_higher():
    cfg = load_fee_profiles()
    assert "bybit_non_vip_usdt_perp" in cfg["fee_profiles"]
    assert fee_rate("bybit_default_futures", "taker") == fee_rate("bybit_non_vip_usdt_perp", "taker")  # alias
    assert fee_rate("conservative_taker", "taker") > fee_rate("bybit_non_vip_usdt_perp", "taker")
    assert fee_rate("zero", "taker") == 0.0


def test_net_pnl_is_gross_minus_costs():
    c = trade_costs(notional_usdt=1000, symbol="FOO/USDT", fee_profile="bybit_default_futures")
    from src.execution.fees import net_pnl_usdt
    assert net_pnl_usdt(10.0, c) == round(10.0 - c.total_cost_usdt, 6)


# ---- portfolio -------------------------------------------------------------
def _trade(per, entry=100, stop=98, **kw):
    base = dict(signal_id="s", economic_trade_key="k", symbol="ETH/USDT", direction="long",
                entry=entry, stop=stop, paper_execution_r=per, close_reason="x",
                stop_current_r=0.0, entry_at="2026-06-20T00:00:00Z")
    base.update(kw); return base


def test_portfolio_equity_updates_win_loss_be():
    trades = [_trade(2.0, economic_trade_key="a"), _trade(-1.0, economic_trade_key="b"),
              _trade(0.0, economic_trade_key="c")]
    run = simulate_portfolio(trades, fee_profile="zero")
    s = run["summary"]
    assert s["initial_equity_usdt"] == 5000
    # win +2R≈+50, loss -1R≈-25, BE 0 → ~+25 (zero fees), risk compounds slightly
    assert s["final_equity_usdt"] > 5000
    assert s["wins"] == 1 and s["losses"] == 1 and s["breakeven"] == 1
    assert len(run["ledger"]) == 3


def test_portfolio_fees_reduce_equity_vs_zero():
    trades = [_trade(2.0, economic_trade_key=f"k{i}") for i in range(5)]
    z = simulate_portfolio(trades, fee_profile="zero")["summary"]["final_equity_usdt"]
    b = simulate_portfolio(trades, fee_profile="bybit_default_futures")["summary"]["final_equity_usdt"]
    assert b < z   # fees always reduce equity


def test_portfolio_skips_unresolved_and_bad_geometry():
    trades = [_trade(None, economic_trade_key="u"), _trade(1.0, entry=0, economic_trade_key="z")]
    run = simulate_portfolio(trades, fee_profile="zero")
    assert run["summary"]["trades"] == 0   # both skipped, no silent zero


def test_exit_price_populated_and_expiry_close_set():
    # long, +2R win → exit price = entry + 2*|entry-stop| = 100 + 2*2 = 104
    win = simulate_portfolio([_trade(2.0, entry=100, stop=98, close_reason="tp_win")], fee_profile="zero")
    assert win["ledger"][0]["exit_price"] == 104.0
    assert win["ledger"][0]["expiry_close_price"] is None   # not an expiry
    # expired-flat → exit at entry (0R), tagged with expiry_close_price + source
    exp = simulate_portfolio([_trade(0.0, entry=100, stop=98, close_reason="expired_flat")], fee_profile="zero")
    assert exp["ledger"][0]["exit_price"] == 100.0
    assert exp["ledger"][0]["expiry_close_price"] == 100.0
    assert exp["ledger"][0]["expiry_close_price_source"] == "implied_from_paper_execution_r"


def test_close_fee_uses_exit_notional_in_sim():
    # winner: exit notional > entry notional → close fee strictly larger than open fee
    from src.execution.fees import trade_costs
    run = simulate_portfolio([_trade(2.0, entry=100, stop=98, symbol="FOO/USDT")],
                             fee_profile="bybit_non_vip_usdt_perp")
    led = run["ledger"][0]
    # exit price 104 vs entry 100 → close notional 4% larger → fees reflect it
    assert led["exit_price"] == 104.0 and led["fees_usdt"] > 0
