# MAX 2X SAFE LEVERAGE POLICY — IMPLEMENTATION REPORT (PART 1)

**Scope:** PAPER ONLY. No live, no auto-live, no exchange execution, no real orders.
**Date:** 2026-06-24

## What changed
`config/paper_portfolio.yaml` now encodes the safe-leverage policy:

| field | old | new |
|---|---|---|
| max_leverage | 5 | **2** |
| max_margin_per_trade_pct | 0.20 | **0.40** |
| max_notional_per_trade_pct | 1.50 | **0.80** |
| liquidation_buffer_to_stop | 1.5 | **3.0** |
| leverage_policy | — | **max_2x_safe** |
| skip_if_risk_capped | — | false |
| too_tight_stop_pct / too_wide_stop_pct | — | 0.0035 / 0.08 |

`src/execution/position_sizing.py` rewritten to enforce it and emit the new fields:
`leverage_policy`, `desired_notional_usdt`, `capped_notional_usdt`, `risk_capped`,
`actual_risk_usdt`, `risk_utilization_pct`, `margin_cap_reason`,
`liquidation_buffer_distance_pct`, `leverage_reason`, plus `too_tight_stop` /
`too_wide_stop` flags.

## Sizing algorithm (unchanged math, new caps)
```
risk_usdt        = equity × 0.005
stop_dist_pct    = |entry − stop| / entry
desired_notional = risk_usdt / stop_dist_pct
notional_cap     = min(max_margin_usdt × max_lev, equity × max_notional_pct)   # = min(2000×2, 4000) = 4000 on 5k
notional         = min(desired_notional, notional_cap)
leverage_used    = clamp(ceil(notional / max_margin_usdt), 1, 2)
actual_risk      = notional × stop_dist_pct
risk_capped      = notional < desired  OR  actual_risk < 0.8 × target
liq_dist_pct     = 1 / leverage_used ; liq_buffer_ok = liq_dist_pct ≥ 3 × stop_dist_pct
```

## Why max 2x — and why that is NOT "stop at 50%"
- **Leverage ≠ risk.** Risk is `stop_distance × position_size`. A 2% stop with a
  $1,250 position risks $25 whether the account uses 1x or 2x. Leverage only sets the
  *margin* and the *liquidation* distance.
- At **2x, liquidation is ~50% away** from entry; normal technical stops are 0.5–8%.
  The stop is hit **first by a factor of 6–100×** — liquidation is never the exit.
- Max 2x removes any fake "leverage edge", caps the notional that a tiny stop can
  conjure, and forces cleaner, fee-aware geometry. If a setup only works at 5x it is
  not robust.
- When 0.5% risk cannot fit under 2x + the margin/notional caps, the position is
  **reduced** (`risk_capped=true`), never levered up. With `skip_if_risk_capped=true`
  it becomes review-only.

## Effect on the historical book ($5000 paper, 0.5% risk)
Re-sized under the 2x policy (mechanical-taker A book), Bybit profile:
`final $5185.91 · +3.72% · maxDD 18.28% · fees $1763 · avg leverage ≈ 1.0x · max 2x`.
Tighter stops that previously drew 5x now cap notional at $4,000 (80% of equity) and
mark `risk_capped` instead of inflating leverage.

## Tests
`tests/test_paper_portfolio.py` sizing cases updated for the 2x policy: notional caps,
`risk_capped` at 0.5% stop, `too_tight_stop` at 0.25%, `too_wide_stop` at 10%,
`leverage_used ≤ 2`, liquidation buffer. All pass.

## Verdict
**MAX_2X_SAFE_LEVERAGE_POLICY_ACTIVE_FOR_PAPER**
