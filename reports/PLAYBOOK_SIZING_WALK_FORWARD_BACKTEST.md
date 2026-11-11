# Playbook Sizing — Walk-Forward Backtest (PART 5)

**Date:** 2026-06-10 23:31 UTC
**Total closed signals:** 1424

## Temporal split (60% / 30% / 10%)

- Train: 854 signals · 2026-05-22 → 2026-06-01
- Validation: 427 signals · 2026-06-01 → 2026-06-08
- Forward: 143 signals · 2026-06-08 → 2026-06-10

Weights for each config are chosen with awareness of TRAIN data only. Performance is reported on VALIDATION and FORWARD windows — out-of-sample.

## CRITICAL caveat

- Only **~20 days** of signal history. Statistical power is LOW. 
- Use this as a *direction check*, not a conclusive OOS validation.
- Do NOT optimize weights against validation outputs.

## Results — sum sized R per window

| Config | Train sum R | Val sum R | Forward sum R | Val WR | Val PF |
|---|---:|---:|---:|---:|---:|
| 1_equal_1R | +85.00 | -41.00 | -14.00 | 29% | 0.74 |
| 2_current_yaml | +114.00 | +30.00 | +4.50 | 43% | 1.78 |
| 3_conservative | +57.00 | +27.50 | +3.75 | 43% | 2.01 |
| 4_aggressive | +121.00 | +37.00 | +4.50 | 43% | 1.80 |

## Interpretation rules

- A config is OOS-positive if **both** validation and forward sums are positive.
- A config that improves train sum R but degrades forward sum R is overfit and rejected.
- `1_equal_1R` is the **baseline**; any other config must beat it OOS to justify the complexity.

## Verdict per config

- **1_equal_1R** — OOS not consistently positive
- **2_current_yaml** — OOS-positive; beats baseline both windows
- **3_conservative** — OOS-positive; beats baseline both windows
- **4_aggressive** — OOS-positive; beats baseline both windows

## Recommendation

- The current YAML config (`2_current_yaml`) is the deployed sizing layer. Its OOS performance above is the source of truth for whether to keep, retune, or revert it.
- Re-run this script weekly as the signal history grows beyond 6-8 weeks; only then will sample size give a real OOS verdict.
- Do NOT change weights based on a single OOS window of <100 signals.