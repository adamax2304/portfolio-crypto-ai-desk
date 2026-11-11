# Medium-Deep Sweep Target Variants

Generated: `2026-09-29`

## Paper profiles

All three profiles share the same entry sample. They require a 2-5 ATR flush,
1.5-2.75% depth, liquidation percentile >= 0.90, OI decline of 0.25-5%,
Europe/US session, 0.75-1.5% stop distance, and a one-bar 1m green reclaim.
Only target placement differs.

| Profile | Profile ID | Target policy | Difference |
|---|---|---|---|
| `MEDIUM_DEEP_R_CONTROL` | `crypto_fast_flush_medium_deep_r_control_paper_v1` | Fixed R | TP1 0.80R, TP2 1.35R. Research control. |
| `MEDIUM_DEEP_R_EXTENDED` | `crypto_fast_flush_medium_deep_r_extended_paper_v1` | Fixed R | TP1 1.00R, TP2 1.75R. Tests whether runners pay for fewer fills. |
| `MEDIUM_DEEP_STRUCTURE_HYBRID` | `crypto_fast_flush_medium_deep_structure_hybrid_paper_v1` | Bounded structure | TP1 uses rolling 4h VWAP bounded to 0.60-1.00R; TP2 uses the pre-flush close bounded to 1.10-1.80R. Missing or invalid structure falls back to 0.80R/1.35R. |

The profiles are Paper-only and have no Live bridge.

## Medium-deep historical replay

The paired 25-trade replay kept entries, stops, costs, and hold time constant:

| Variant | Net R | PF | Latest test |
|---|---:|---:|---:|
| Fixed 0.80R / 1.35R | +10.015R | 3.791 | +3.334R |
| Fixed 1.00R / 1.75R | +12.751R | 4.553 | +4.393R |
| Bounded 4h VWAP / previous close | +11.275R | 4.142 | +3.835R |

This is a small local sample. The three-way Paper A/B is the forward test; no
variant is promoted automatically.

## Best existing modes target replay

The replay freezes every recorded entry and initial stop, then applies one
standardized 33/33/34 exit model with stop-first candles, breakeven after TP1,
+0.5R protection after TP2, fees, slippage, and a time exit.

### Stocks intraday BREAKOUT_CONTINUATION / new_logic_shadow

Coverage: 51 of 55 closed clean paths.

| Target policy | Net R | PF | Latest 9 trades |
|---|---:|---:|---:|
| Stored targets | +34.368R | 7.488 | +8.781R |
| Fixed 1R / 2R / 3R | +35.415R | 8.130 | +8.066R |
| ATR 1x / 2x / 3x | +26.294R | 8.377 | +3.730R |
| Pure structure | +34.314R | 7.478 | +7.960R |
| Bounded structure hybrid | +36.769R | 10.470 | +8.595R |

The bounded hybrid is the best full-sample candidate, but it did not beat the
stored targets in the latest nine trades. It belongs in a separate Paper A/B,
not as an immediate replacement. Plain ATR targets are too close relative to
the existing stock stops and materially reduce expectancy.

### Crypto intraday BREAKOUT_CONTINUATION / paper_v1

Coverage: 17 of 41 paths (9 research-archive 1m, 8 rolling-cache 5m).

| Target policy | Net R | PF | Latest 4 trades |
|---|---:|---:|---:|
| Stored targets | -3.411R | 0.611 | -1.130R |
| Fixed 1R / 2R / 3R | -5.068R | 0.537 | -4.032R |
| ATR 1x / 2x / 3x | -1.020R | 0.766 | -0.502R |
| Pure structure | -1.755R | 0.800 | -1.133R |
| Bounded structure hybrid | -2.629R | 0.700 | -1.506R |

ATR targets reduced the loss on this limited subset, but every target policy
remained negative. Target placement alone does not repair this recent crypto
cohort, and no target variant should be promoted from this result.

## Interpretation boundary

This is a target-policy comparison, not a reproduction of the legacy
`paper_execution_r` model. The legacy model holds the runner to TP3/BE/lock;
this experiment deliberately uses the same partial-exit mechanics for every
variant so target placement is the only changed variable.
