# Historical Paper Execution Recalc (PART 4)

**Date:** 2026-06-24. Derived, read-only. CSV: `data/research/paper_execution_recalc_2026-06-23.csv` (builder `scripts/paper_execution_recalc.py`). `final_r` NOT rewritten.

## Method
Deduped economic trades (latest/terminal, no raw row duplication) over all available history (~30d; 60d/30d identical — tracker is ~30d old). Per trade: `touch_r`, `first_tp_close_r`, `hold_tp3_r`, `paper_execution_r` (Model F). 1403 deduped economic trades.

## Net R by window × book
| window | book | n | touch_r | first_tp | hold_tp3 | **paper_exec (F)** |
|---|---|---|---|---|---|---|
| all (~30d) | actionable | 584 | +6.2 | −104.8 | −136.8 | **+74.1** |
| all | shadow | 819 | −128.5 | −158.8 | −269.3 | −84.3 |
| 7d | actionable | 105 | −5.0 | −36.0 | −28.2 | **+13.6** |
| 7d | shadow | 150 | −21.7 | −23.0 | −32.0 | −13.2 |
| 48h | actionable | 42 | +6.4 | −7.6 | −5.8 | **+7.8** |
| 48h | shadow | 71 | −8.3 | −9.0 | −11.0 | −4.8 |
| today | actionable | 10 | +0.4 | +0.4 | −2.0 | +0.4 |

## Reading
- **Touch (+6.2R) is the optimistic illusion**; with NO risk management (close at first TP) the actionable book is **−104.8R** — that is the real overstatement the prior audits flagged (~+111R).
- **Model F (early MFE-armed protection) recovers the book to +74.1R** (PF ~1.43 in the prior viability audit) by turning unprotected +0.6R-then-reverse stops into breakevens — broad across windows (7d +13.6, 48h +7.8).
- Shadow stays negative under every model (correctly excluded from the headline).
- **Caveat:** Model F is a 30-day, single-epoch, hindsight-trigger replay with no cost/slippage haircut — it is the *forward* paper model now being tracked, **pending forward validation**, not a realized live result.

## Verdict
`HISTORICAL_REALISTIC_RECALC_READY`
