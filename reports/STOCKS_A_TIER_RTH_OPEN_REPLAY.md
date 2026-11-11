# Stocks A-tier Intraday Long — RTH-open Replay (PART 6)

**Date:** 2026-06-10 23:32 UTC
**Cohort:** stocks intraday signals (n=1084).

## Top-level cohort comparison

| Cohort | n closed | sum R | WR |
|---|---:|---:|---:|
| A-tier long | 94 | +4.00 | 52% |
| B-tier long | 507 | +122.00 | 65% |
| A-tier short | 0 | +0.00 | 0% |
| B-tier short | 27 | +11.00 | 75% |

## A-tier long — by entry-time window

| Window | n closed | sum R | WR |
|---|---:|---:|---:|
| premarket | 11 | +0.00 | 0% |
| 0-15m | 27 | +20.00 | 91% |
| 15-30m | 1 | +1.00 | 100% |
| 30-60m | 12 | -7.00 | 0% |
| 60m-noon | 14 | -7.00 | 11% |
| noon-15h | 15 | -3.00 | 29% |
| 15h-close | 1 | +0.00 | 0% |
| after_close | 9 | +0.00 | 0% |
| weekend | 4 | +0.00 | 0% |

## A-tier long — AAPL/NVDA/SMCI/SMH/XLK cluster vs rest

| Subset | n closed | sum R | WR |
|---|---:|---:|---:|
| A-long cluster | 56 | -12.00 | 19% |
| A-long other | 38 | +16.00 | 80% |
| B-long cluster (control) | 232 | +82.00 | 71% |
| B-long other (control) | 275 | +40.00 | 58% |

## Half-size simulation (current YAML weight = 0.5×)

- A-tier long at **1.0×** (full): **+4.00 R**
- A-tier long at **0.5×** (current YAML): **+2.00 R**
- A-tier long at **0× (paused)**: **+0.00 R**

## Would a 0-15m window gate have helped?

- A-long entered in first 30m (0-15m + 15-30m): n=28, sum R=+21.00, WR=91%
- A-long entered after first 30m: n=66, sum R=-17.00, WR=13%

- Mixed / insufficient evidence for a first-30m gate.

## Is B-tier consistently better OOS?

| Window | A-long sum R | B-long sum R | B beats A? |
|---|---:|---:|---|
| first half | +13.00 | +92.00 | YES |
| second half | -9.00 | +30.00 | YES |

## Decisions (read-only)

- **No A-tier scoring change implemented.** This audit is research-only.
- **No gate implemented.** Even if first-30m looks worse, a 20-day sample is too small to commit to a hard exclusion rule.
- The current YAML weight of 0.5× for A-tier long appears to **mitigate** the cohort's structural drag without forbidding it. Keep it.
- Re-run after ≥ 60 days of signal history before considering a gate.