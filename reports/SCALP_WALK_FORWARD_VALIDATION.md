# Scalp Walk-Forward Validation (PART 7)

**Date:** 2026-06-15 · Policy A, temporal 60/25/15 split (no optimisation on full set).

## Windows

| Window | Period | n | WR | PF | avg R | total R |
|---|---|---:|---:|---:|---:|---:|
| TRAIN (60%) | 2025-06-21 → 2026-01-24 | 83,408 | 42% | 0.63 | −0.475 | −39,620 |
| VALIDATION (25%) | 2026-01-24 → 2026-04-22 | 34,753 | 44% | 0.68 | −0.375 | −13,017 |
| OOS (15%) | 2026-04-22 → 2026-06-15 | 20,853 | 42% | 0.56 | −0.582 | −12,128 |

## Reads

- **Net-negative in ALL three windows.** PF 0.56–0.68 throughout. This is the opposite of an overfit edge — the loss is *stable and consistent* out-of-sample.
- No window is positive; the OOS slice (−0.582R) is the worst, not the best, so there is no "decays only OOS" artifact and no rescue from recency.
- Because the headline result is consistently negative, there is no candidate policy to "select on train and confirm OOS" — every policy already failed on the full set, and A specifically fails in every sub-window.

## Conclusion

Walk-forward confirms the backtest is robust, not a fluke: **current scalp loses, consistently, across train / validation / OOS.** Any future positive variant would have to clear this bar in all three windows — none tested does.
