# Shadow Intelligence — Forward Comparison Template (PART 8)

**Purpose:** Friday analysis — compare actual signals/trades + guardrail fields + new intelligence fields vs outcomes, and estimate what *would* have changed if a field influenced decisions. Fill from `signal_alerts.payload_json` + `signal_outcomes`. Observation-only.

## Coverage
| Metric | Value |
|---|---|
| signals analyzed | |
| timeline confidence coverage (% with med/high) | |
| derivatives confidence coverage | |
| squeeze phase coverage (% non-unknown) | |
| thesis generated coverage | |
| onchain coverage (% non-unknown) | |

## Phase / derivatives vs outcome
| Cut | winners | losers | net R |
|---|---|---|---|
| phase_3_distribution_near_high | | | |
| funding_peak + OI_stall | | | |
| no_chase_warning=True | | | |
| onchain high-risk | | | |

## Predictive checks
- thesis invalidation accuracy (did price actually break the stated invalidation?): 
- no-chase warning precision (of warned signals, % that then underperformed): 
- distribution_risk_score vs forward drawdown correlation: 
- timeline_recent_outcome_bias vs next outcome: 

## Hypothetical impact (if each field had influenced decisions — NOT applied)
- potential R saved (skipping phase_3 / no-chase longs): 
- potential winners missed (if those were skipped): 
- net hypothetical impact: 

## Recommendation (per field)
| Field | keep_shadow / soft_warning / review_only / discard_noisy | note |
|---|---|---|
| squeeze_phase / no_chase_warning | | |
| derivatives funding_turning_down | | |
| thesis invalidation | | |
| timeline outcome bias | | |
| onchain risk (if configured) | | |

> Default verdict stays **keep_shadow** for every field until forward data justifies promotion; nothing is wired to influence trades.
