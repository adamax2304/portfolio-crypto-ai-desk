# Shadow Feature Promotion Decision Table (PART 5)

**Date:** 2026-06-24. Main metric = `paper_execution_r`.

| feature | current status | evidence | decision | paper implementation action | risk | tests needed |
|---|---|---|---|---|---|---|
| Model F / paper_execution_r | active paper accounting | replay +74.1R, PF 1.43 | **PROMOTE_TO_PAPER_ACCOUNTING_ONLY** (done) | verify only — already live | low | existing (pass) |
| touch_r relabel (optimistic) | active display | display correctness | **PROMOTE_TO_PAPER_DISPLAY_ONLY** (done) | verify only | low | existing |
| lifecycle status clarity | live-display | UNKNOWN 87→3 | **PROMOTE_TO_PAPER_DISPLAY_ONLY** (done) | none | low | existing |
| close-alert clarity + Model F line | live-display | — | already active | none | low | existing |
| risk-guard warnings (CB/sector/correlation/profit-hint) | alert-only advisory | advisory | **PROMOTE_TO_PAPER_DISPLAY_ONLY** | surface in Paper Features panel + per-trade tags | low | panel shape |
| catalyst label refresh + integrity | live-advisory | data-quality | already active | keep scheduler step | low | existing |
| funding/OI archive, risk-off label | live data/advisory | data | already active | keep | low | existing |
| **cohort guard (crypto_intraday_catalyst)** | default-off | +0.02R/trade weakest | **PROMOTE_TO_PAPER_DISPLAY_ONLY** | `mode: off → warn` (label only); per-trade "weak cohort" badge | low | config-safety + flag (added) |
| adaptive TP3 / TP policy | research | TP3 3.7%, ≈0 net | **KEEP_MEASURING** | none (advisory) | low | — |
| intelligence layer (timeline/derivatives/squeeze) | shadow | <30 closed | **KEEP_MEASURING** | none | low | — |
| circuit breaker as BLOCK | need_more_data | <10 fires | **KEEP_SHADOW** | none (warnings stay) | med | — |
| sector/concentration caps as BLOCK | need_more_data | weak | **KEEP_SHADOW** | none (warnings stay) | med | — |
| position/leverage advisor | shadow label | none | **KEEP_MEASURING** | none | low | — |
| shadow exit manager A–I (BE/partial/trailing) | shadow research | inferior to Model F | **KILL_OR_ARCHIVE** | `state: archived` (SUPERSEDED_BY_MODEL_F); kept for research | low | — |
| crypto scalp actionable | locked shadow | net-negative | **DANGEROUS_DO_NOT_USE** | stay locked | high | guard test |
| stocks C-tier actionable | locked shadow | −34R | **DANGEROUS_DO_NOT_USE** | stay locked | high | guard test |
| stocks swing/invest actionable | locked paused | policy | **DANGEROUS_DO_NOT_USE** | stay locked | high | guard test |
| cohort guard → `paper_review_only` (routing) | proposed | weak cohort | **NEED_OPERATOR_APPROVAL** | flag default-off; sign-off required | med | — |
| Model F → paper *execution* flag (move real paper stops) | proposed | replay only | **NEED_OPERATOR_APPROVAL** | not implemented; forward + cost gate first | med | — |

## Verdict
`SHADOW_PROMOTION_DECISIONS_READY`
