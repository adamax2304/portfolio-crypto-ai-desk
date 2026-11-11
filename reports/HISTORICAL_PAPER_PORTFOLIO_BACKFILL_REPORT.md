# Historical Paper Portfolio Backfill (PART 10)

**Date:** 2026-06-24. Derived simulation (NOT a rewrite). Script: `scripts/paper_portfolio_backfill.py`. $5000 start, 0.5%-of-equity risk (compounding), chronological, actionable paper book, fees/slippage, dynamic leverage caps, risk-capped where stop < 0.5%.

## Result by fee profile (586 deduped actionable trades, ~30d)
| fee profile | final $ | net $ | return % | max DD % | fees+slip $ | W/L/BE |
|---|---|---|---|---|---|---|
| **zero (no-cost baseline)** | 7380 | +2380 | **+47.6%** | 9.24 | 0 | 168/174/244 |
| **bybit_default_futures** | 5147 | +147 | **+2.94%** | 18.31 | 1770 | 168/418/0 |
| mexc_default_futures | 5814 | +814 | +16.28% | 14.41 | 1245 | 168/418/0 |
| conservative | 4718 | −282 | **−5.65%** | 20.98 | 2106 | 168/418/0 |

(W/L/BE: with costs the 244 BE-in-R scratches each pay round-trip fees → become small $ losses, so they fold into "losses".)

## Reading
- **Model F's R-edge is real (+47.6% no-cost, maxDD 9.2%)** — but **fee-fragile**: under Bybit taker fees only +2.9%, and under conservative fees it goes **negative (−5.65%)**. Fees+slippage are $1770–$2106 because tight stops force large notional (high leverage) and the BE-heavy model round-trips ~240 scratch trades that still pay fees.
- Drawdown also worsens with fees (9.2% → 18–21%).

## Outputs
`data/research/paper_portfolio_equity_curve_2026-06-24.csv`, `data/research/paper_portfolio_ledger_2026-06-24.csv`; default-profile ledger persisted to `paper_portfolio_ledger` (586 rows). Equity uses net USD from `paper_execution_r`, never touch_r. `final_r` untouched.

## Implication (next, not done here)
To survive realistic fees: prefer maker fills, wider stops (fewer forced-large notionals), fewer BE round-trips, or fee-aware sizing. These are strategy changes → require separate approval.

## Verdict
`HISTORICAL_PORTFOLIO_BACKFILL_COMPLETE`
