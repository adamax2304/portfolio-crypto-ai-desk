# Position Sizing Engine — Implementation Report (PART 5)

**Date:** 2026-06-24. Module: `src/execution/position_sizing.py`. PAPER ONLY — no orders.

## Formula (linear USDT-perp)
```
risk_usdt        = equity × risk_pct                 # 5000 × 0.5% = 25
stop_dist_pct    = |entry − stop| / entry
desired_notional = risk_usdt / stop_dist_pct
notional         = min(desired_notional, cap)        # cap = min(max_margin×max_lev, equity×max_notional_pct)
qty              = notional / entry
loss_at_stop     = qty × |entry − stop| ≈ risk_usdt
leverage_used    = clamp( ceil(notional / (equity×max_margin_pct)), 1, max_leverage )   # MIN lev for margin cap
margin_used      = notional / leverage_used
liq_dist_pct     ≈ 1 / leverage_used                 # isolated approx
liquidation_buffer_ok = liq_dist_pct ≥ stop_dist_pct × 1.5
```
If `desired_notional > cap` → notional capped, `risk_capped=True`, `actual_risk < target` (happens when stop < 0.5%).

## Worked examples (verified by tests)
- 5000 equity, 0.5% risk, 2% stop → notional **1250**, risk **25**, leverage **2** (ceil 1250/1000), margin 625. ✓
- 0.5% stop → notional 5000 (=cap), risk 25, leverage 5 (maxed, not capped). ✓
- 0.4% stop → desired 6250 > cap 5000 → notional 5000, **risk capped** to ~20, warning. ✓
- short: symmetric; liquidation price above entry. ✓

## Outputs
target_risk_usdt, actual_risk_usdt, actual_risk_pct, qty, notional_usdt, margin_used_usdt, leverage_used, stop_distance_pct, liquidation_price, liquidation_buffer_ok, risk_capped, sizing_warning.

## Key principle (documented in-module)
**Leverage does NOT define risk.** Risk = stop distance × position size. Leverage only sets margin requirement + liquidation distance. The engine derives the *minimum* leverage that fits the margin cap (test `test_leverage_is_not_risk`: tighter stop → bigger notional → more leverage, identical $25 risk).

## Verdict
`POSITION_SIZING_ENGINE_READY`
