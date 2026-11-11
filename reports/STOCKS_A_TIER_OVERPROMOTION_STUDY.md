# Stocks A-tier Overpromotion Study (PART 1)

**Date:** 2026-06-10 · Read-only analysis. No code/scoring/threshold/TP/SL changes proposed in this PR.

## 1. Headline: A vs B intraday closed-only

| Tier | n closed | W | L | **WR** | netR | avgR | avg MFE | avg MAE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **A** | **19** | **4** | **15** | **21%** | **−6.2R** | **−0.33** | +0.64 | **−0.98** |
| **B** | 77 | 43 | 34 | 56% | +24.9R | +0.32 | +0.91 | −0.78 |

A-tier is a **structurally weaker cohort** than B-tier on the same playbook (`stocks_intraday_rth_momentum`), by 35 WR points and 0.65R/trade. The avg MAE for A-tier is materially deeper (−0.98 vs −0.78), meaning A-tier entries get hit harder before either resolving.

## 2. A-tier by symbol (closed-only, all-time)

| Symbol | n | W | L | netR | Pattern |
|---|---:|---:|---:|---:|---|
| **AAPL** | 5 | 0 | 5 | **−3.2R** | 5 consecutive A-tier losses on AAPL longs |
| SMCI | 2 | 0 | 2 | −1.3R | 2 of 2 lost |
| XOM | 1 | 0 | 1 | −1.0R | the one A-tier XOM long in 48h audit |
| SMH | 1 | 0 | 1 | −1.0R | tech ETF chase |
| NVDA | 1 | 0 | 1 | −1.0R | NVDA-long pattern continues |
| XLK | 1 | 0 | 1 | −1.0R | tech sector ETF |
| MSFT | 1 | 0 | 1 | −0.1R | small loss |
| AMD | 3 | 1 | 2 | +0.5R | mixed |
| LLY | 3 | 2 | 1 | **+1.0R** | rare A-tier winner cluster |
| UNH | 1 | 1 | 0 | +1.0R | clean A-tier win |

**70% (13 of 19) of A-tier losses** are on the AAPL / SMCI / SMH / NVDA / XLK / AMD / MSFT / XOM **tech-and-mega-cap-long cluster**. The 14d audit's "NVDA/SMCI longs structurally lose" flag generalizes here.

## 3. A-tier by direction
- **A-tier intraday = 100% longs** (n=19, all long). No short ever made it to A-tier in this dataset.
- Stocks intraday shorts subset (B-tier) is the strongest stocks lane: 9W/4L, WR 69%, PF 3.00, +8R.
- **Conclusion: stocks scoring strongly biases A-tier upward in trending tech, exactly the regime where the chase fails.**

## 4. A-tier by hour-of-day (UTC) — closed-only

| Hour UTC | n closed | W | L | netR | Note |
|---|---:|---:|---:|---:|---|
| 00 | 1 | 0 | 1 | −0.1 | pre-Asian session A-tier; not stocks-relevant timing |
| 01 | 1 | 1 | 0 | +2.0 | AMD A-tier long +2R (post-close anomaly) |
| 09 | 2 | 1 | 1 | 0.0 | pre-market |
| 11 | 2 | 0 | 2 | −1.1 | pre-RTH |
| **13** | **4** | **0** | **4** | **−4.0** | **RTH open chase** |
| **14** | **7** | **1** | **6** | **−3.8** | **first-hour RTH** |
| 15 | 1 | 1 | 0 | +1.0 | second-hour RTH (rare clean) |
| 16 | 1 | 0 | 1 | −0.1 | mid-session |

**11 of 19 A-tier closures (58%) happen in the 13:00–14:59 UTC window** = pre/open-of-RTH. That two-hour window alone produced **−7.8R of the −6.2R total** A-tier netR. The other hours net-positive (+1.6R), so the **RTH-open chase is the dominant A-tier failure mode**.

## 5. MFE / MAE shape
- A-tier avg MFE +0.64 (lower than B-tier's +0.91) — A-tier entries get LESS favorable run before fail.
- A-tier avg MAE −0.98 (deeper than B-tier's −0.78) — A-tier stops are hit harder.
- Combined: A-tier setups go directly adverse from entry more often. This is consistent with "buy strength at the open" failing on mean-reversion days.

## 6. Earnings / legal / stale flags
- 0 of the 19 A-tier closures carried `legal_risk_high` or `stale_post_earnings_setup`. The existing gates correctly excluded those.
- The losses are NOT caused by data-quality issues; they're caused by entry-timing into chase moves.

## 7. Why is A-tier worse than B-tier? (Synthesis)
1. **Scoring stacks tech-momentum bonuses early in RTH.** A-tier score ≥ 80 is reached almost exclusively in the first 1–2h of US session on RS-leading tech names.
2. **The mean-revert pattern in the current tape** punishes that exact cohort: AAPL, NVDA, SMCI, SMH, XLK, AMD longs.
3. **B-tier (sc 65–80) is broader** — captures non-tech sectors (LLY, UNH, XLV, JPM) and intraday shorts (META, AMZN, SPY, QQQ) which carry the positive edge.

## 8. Possible mitigations (NOT implemented in this PR)

| Lever | Implementation type | Expected impact | Risk |
|---|---|---|---|
| **Half-size A-tier stocks longs** (size 0.5) | reporting/sizing only | recovers ~3R of A-tier losses on same dataset; preserves the rare A-tier winners (+1R LLY, +1R UNH) at half size | very low — no scoring change |
| Demote A-tier stocks longs to B during 13:00–14:59 UTC window | code change (gate) | would suppress 11 of 19 A-tier closures; high-impact but invasive | medium — gate logic change |
| Require corroborating short-side bias before A-tier long fires | scoring change | structurally rethinks A-tier criterion | high — out of scope |
| Flag AAPL/NVDA/SMCI/SMH-long with score ≥ 80 as "shadow A" in dashboard | reporting only | observability; lets user override before Telegram | low |

**Recommended for PART 6 ranking: option 1 (half-size A-tier stocks longs) — pure reporting-layer / sizing-simulation change with positive expected value and low overfit risk.**

## Verdict
```
A_TIER_OVERPROMOTION_CONFIRMED
```

A-tier intraday stocks longs are statistically worse than B-tier (21% vs 56% WR) and the loss is concentrated in the RTH-open chase on tech-mega-cap names. The cleanest fix is a position-sizing adjustment (covered in PART 5), not a scoring or gate change.
