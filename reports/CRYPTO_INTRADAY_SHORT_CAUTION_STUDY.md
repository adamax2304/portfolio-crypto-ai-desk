# Crypto Intraday Short Caution Study (PART 3)

**Date:** 2026-06-14 11:11 UTC
**Scope:** all A/B crypto intraday short signals (n=19).

## Subgroup performance

| Subgroup | n | trig | W | L | WR | raw R |
|---|---:|---:|---:|---:|---:|---:|
| all_intraday_shorts | 19 | 12 | 4 | 8 | 33% | +4.0 |
| with_fresh_news | 8 | 6 | 2 | 4 | 33% | +2.0 |
| without_news | 11 | 6 | 2 | 4 | 33% | +2.0 |
| failed_reclaim_only | 0 | 0 | 0 | 0 | 0% | +0.0 |
| breakdown_retest_only | 19 | 12 | 4 | 8 | 33% | +4.0 |
| deriv_confirmed | 7 | 4 | 2 | 2 | 50% | +4.0 |
| no_deriv_confirmation | 12 | 8 | 2 | 6 | 25% | +0.0 |
| btc_aligned_bearish | 7 | 3 | 1 | 2 | 33% | +1.0 |
| btc_mean_reverting | 12 | 9 | 3 | 6 | 33% | +3.0 |

## Key findings

- Shorts without news support: n=11, R=+2.0
- Shorts WITH news support: n=8, R=+2.0

- Derivatives-confirmed shorts: n=7, R=+4.0
- No derivatives confirmation: n=12, R=+0.0

- Failed-reclaim setup: n=0, R=+0.0
- Breakdown-retest setup: n=19, R=+4.0

## Hypothetical filter: only ship shorts with fresh news + deriv confirmation

- Kept (would still trade): n=1, R=+3.0, WR=100%
- Rejected (would NOT trade): n=18, R=+1.0

- The hard filter rejects too much; would-be winners like TON might be cut. Do not implement.

## Winners that the hard filter would have removed (if any)

- Winning shorts total: **4**
- Would have been blocked by filter: **3**
  - ETH/USDT 2026-06-05 final_r=+3.0
  - PUMP/USDT 2026-06-05 final_r=+3.0
  - TON/USDT 2026-06-10 final_r=+3.0

## Recommendation

- **Do NOT implement a hard filter.** Sample n=33 is too small.
- **Add a Telegram caution label** to paper-entry alerts for crypto intraday shorts without fresh news AND without deriv confirmation. Label text: `⚠️ NO-NEWS-NO-DERIV SHORT — historically thin edge in this regime`.
- Re-evaluate after the cohort grows to n ≥ 60.