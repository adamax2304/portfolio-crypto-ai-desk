# Signal Execution Replay — Summary

**Date:** 2026-06-10 23:33 UTC
**Total replayed:** 980
**Fees included:** True · **Slippage included:** True

## Headline

- Raw R (sum): **+33.94**
- Sized R (sum, playbook-aware): **+103.28**
- Fees/slippage R adjustment (sum): **-4.10**
- Wins / Losses: 315 / 383  ·  WR = 45.1%  ·  PF = 1.14
- Same-candle ambiguous: 0 (0.0%)

## Coverage quality
- high: 731
- medium: 249

## Replay outcome distribution
- stop: 284
- tp1: 196
- entry_moved_away: 179
- open_no_event: 118
- expired: 100
- stale_before_entry: 91
- no_entry_in_window: 12

## By asset class
- **stocks** — n=859, raw R=+30.74, sized R=+100.78
- **crypto** — n=121, raw R=+3.21, sized R=+2.51

## By playbook
| Playbook | n | raw R | sized R | WR |
|---|---:|---:|---:|---:|
| stocks_intraday_rth_momentum | 604 | +110.63 | +100.78 | 56% |
| crypto_failed_bounce_short | 21 | +4.28 | +4.10 | 100% |
| crypto_scalp_momentum_continuation | 65 | +0.28 | +0.01 | 67% |
| stocks_swing_watchlist_rs_rotation | 144 | -30.27 | +0.00 | 31% |
| stocks_invest_watchlist_30d_thesis | 111 | -49.62 | +0.00 | 19% |
| crypto_intraday_catalyst_or_momentum | 17 | -0.09 | -0.16 | 0% |
| crypto_swing_narrative_rs_momentum | 18 | -1.26 | -1.45 | 40% |

## Cross-check vs original tracker
- Replay-vs-tracker mean |Δraw R| = 0.430 (935 compared)

## Notes
- Replay uses **no look-ahead**: candles are processed strictly forward from `created_at`.
- Same-candle TP-vs-stop events on lower-resolution timeframes are marked **ambiguous** and resolved by policy (conservative=stop first).
- All outputs are write-only into reports/. `proposed_signals`, `signal_outcomes`, `signal_alerts`, `watchlist_alerts` are NOT touched.