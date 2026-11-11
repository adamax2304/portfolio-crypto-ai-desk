# MAX 5X SAFE LEVERAGE POLICY — REPORT (PART 2)

**Scope:** PAPER ONLY. Date: 2026-06-24. Reversible (config + sizing engine).

## Change
`config/paper_portfolio.yaml` + `src/execution/position_sizing.py`:

| field | prev (2x) | now (5x) |
|---|---|---|
| max_leverage | 2 | **5** |
| max_margin_per_trade_pct | 0.40 | **0.25** |
| max_notional_per_trade_pct | 0.80 | **1.50** |
| liquidation_buffer_to_stop | 3.0 | 3.0 |
| min_liquidation_distance_multiple_of_stop | — | **3.0** |
| skip_if_liquidation_too_close | — | **true** |
| leverage_policy | max_2x_safe | **max_5x_safe** |

New `SizingResult` fields: `liquidation_buffer_fail`, `skip_recommended`.

## Algorithm (risk-based; leverage is a consequence, not an input)
```
risk_usdt   = equity × 0.005                       # 0.5% = $25 on $5000
notional    = min(risk_usdt / stop_dist_pct, min(0.25·eq·5, 1.5·eq))   # cap 6250 on 5k
leverage    = clamp(ceil(notional / (0.25·eq)), 1, 5)
# liquidation safety:
safe_lev    = floor(1 / (stop_dist_pct × 3))       # liq distance ≥ 3× stop
if leverage > safe_lev:  leverage = safe_lev; notional = 0.25·eq·leverage  # reduce, never widen
if safe_lev < 1:  skip_recommended (stop ~>33%)
actual_risk = qty × stop_dist  (≤ target; risk_capped if < 0.8×target)
```

## Why max 5x is still safe under risk-based sizing
- **Leverage ≠ risk.** Risk = stop distance × size. A 2% stop on a $1,250 position is $25
  at 1x or 5x — the stop, not the margin, defines the loss.
- Leverage only sets margin (notional/lev) and the liquidation distance (≈ 1/lev).
- **Liquidation guard:** the engine forces `liq_distance ≥ 3 × stop_distance`. At 5x,
  liq ≈ 20% away; it only allows 5x when the stop is < ~6.7% (so 3×stop < 20%). Wider
  stops auto-reduce leverage (e.g. a 9% stop caps at 3x so liq 33% ≥ 27%). The stop is
  always hit far before liquidation.
- If 0.5% risk can't fit under the caps → `risk_capped` (reduce size), never lever up.
  If even 1x can't clear the liq buffer (stop ≳33%) → `skip_recommended`.

## Worked examples ($5000, 0.5%)
| stop | desired notional | notional | leverage | risk | liq dist | note |
|---|---|---|---|---|---|---|
| 2.0% | 1250 | 1250 | 1x | $25 | 100% | normal |
| 0.5% | 5000 | 5000 | 4x | $25 | 25% | fits, liq 25% ≥ 1.5% |
| 0.3% | 8333 | 6250 (cap) | 5x | $18.75 | 20% | risk_capped, too_tight |
| 9.0% | 278 | 278 | 1→cap 3x | $25 | 33% | leverage limited by liq buffer |

## UI exposure (PART 6)
Trade detail shows: leverage + `leverage_reason`, margin used, liquidation price,
liq-distance vs stop-distance, and `risk_capped` / `liquidation_buffer_fail` /
`skip_recommended` flags.

## Tests
`tests/test_paper_portfolio.py` (15 passed) — 5x notional/leverage, 0.5% fits at 4x,
0.3% caps+too_tight, wide-stop liquidation-safe leverage reduction, leverage≠risk.

## Verdict
**MAX_5X_SAFE_LEVERAGE_POLICY_ACTIVE_FOR_PAPER**
