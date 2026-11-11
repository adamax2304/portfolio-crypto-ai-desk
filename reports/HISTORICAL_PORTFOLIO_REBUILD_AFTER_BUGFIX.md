# Historical Portfolio Rebuild After Bugfix (PART 8)

**Date:** 2026-06-24. Re-ran `scripts/paper_portfolio_backfill.py` with corrected fee model (exit-notional close fee), expired close policy (exit_price populated), exact TP R, across 4 fee profiles. $5000 start, 0.5%/equity risk, 586 deduped actionable trades. Derived simulation — `final_r` not touched.

## New result by fee profile
| fee profile | final $ | net $ | return % | max DD % | fees+slip $ | W/L/BE |
|---|---|---|---|---|---|---|
| zero (no-cost) | 7372 | +2372 | +47.45% | 9.24 | 0 | 167/175/244 |
| **bybit_non_vip_usdt_perp** | 5141 | +141 | **+2.82%** | 18.3 | 1767 | 167/419/0 |
| mexc_default_futures | 5807 | +807 | +16.15% | 14.4 | 1243 | 167/419/0 |
| conservative_taker | 4712 | −288 | −5.76% | 20.97 | 2103 | 167/419/0 |

(Backend headline equity reads **$5136 / +2.72%** — the live read uses all 587 persisted exit rows per profile incl. the last partial; same picture.)

## Old vs new (what the fixes changed)
- **Fees:** close fee moved from entry-notional to **exit-notional** → bybit return +2.94% → **+2.82%** (winners pay slightly more on the larger exit notional). Magnitude small, direction correct.
- **Expired:** `exit_price` NULL on 100% of rows → **0 NULL**; `expiry_close_price` now set on **133** genuine expiries (was 0; the over-broad 488 BE/lock closes are correctly re-classed as `exit`).
- **TP R:** exact R now exposed (e.g. 1.2/2.2/3.2R) — previously implied "+1/2/3R" by name.
- **Profiles:** 4 distinct profiles persisted (was 1); `conservative` no longer collapses to bybit.
- Drawdown / W-L unchanged in shape; BE-in-R folds into "losses" after fees (zero-profile keeps 244 BE).

## Outputs
`data/research/paper_portfolio_equity_curve_2026-06-24.csv`, `data/research/paper_portfolio_ledger_2026-06-24.csv`; ledger table holds 4 profiles × 587 rows; `fee_estimated=0` (exit prices known).

## Verdict
`HISTORICAL_PORTFOLIO_REBUILT_WITH_CORRECTED_ACCOUNTING`
