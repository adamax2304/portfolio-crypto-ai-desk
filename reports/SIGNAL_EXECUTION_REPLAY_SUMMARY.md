# Signal Execution Replay — Summary

**Date:** 2026-06-10 23:29 UTC
**Total replayed:** 1470
**Fees included:** True · **Slippage included:** True

## Headline

- Raw R (sum): **+161.34**
- Sized R (sum, playbook-aware): **+215.95**
- Fees/slippage R adjustment (sum): **-6.73**
- Wins / Losses: 535 / 481  ·  WR = 52.7%  ·  PF = 1.51
- Same-candle ambiguous: 0 (0.0%)

## Coverage quality
- high: 1219
- medium: 251

## Replay outcome distribution
- stop: 366
- tp1: 338
- stale_before_entry: 238
- entry_moved_away: 204
- expired: 193
- open_no_event: 119
- no_entry_in_window: 12

## By asset class
- **stocks** — n=1340, raw R=+157.98, sized R=+213.32
- **crypto** — n=130, raw R=+3.36, sized R=+2.63

## By playbook
| Playbook | n | raw R | sized R | WR |
|---|---:|---:|---:|---:|
| stocks_intraday_rth_momentum | 1084 | +237.53 | +213.32 | 61% |
| crypto_failed_bounce_short | 22 | +4.28 | +4.10 | 100% |
| crypto_scalp_momentum_continuation | 69 | +0.28 | +0.01 | 67% |
| stocks_swing_watchlist_rs_rotation | 145 | -29.93 | +0.00 | 32% |
| stocks_invest_watchlist_30d_thesis | 111 | -49.62 | +0.00 | 19% |
| crypto_intraday_catalyst_or_momentum | 21 | +0.06 | -0.04 | 33% |
| crypto_swing_narrative_rs_momentum | 18 | -1.26 | -1.45 | 40% |

## Cross-check vs original tracker
- Replay-vs-tracker mean |Δraw R| = 0.428 (1425 compared)

## Notes
- Replay uses **no look-ahead**: candles are processed strictly forward from `created_at`.
- Same-candle TP-vs-stop events on lower-resolution timeframes are marked **ambiguous** and resolved by policy (conservative=stop first).
- All outputs are write-only into reports/. `proposed_signals`, `signal_outcomes`, `signal_alerts`, `watchlist_alerts` are NOT touched.