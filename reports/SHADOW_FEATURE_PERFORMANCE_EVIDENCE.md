# Shadow Feature Performance Evidence (PART 3)

**Date:** 2026-06-24. Main PnL metric = **`paper_execution_r`** (Model F), NOT legacy touch R. Evidence kind labelled: `replay` (historical), `forward` (post-implementation), `display` (read-model only), `none`.

| feature | evidence kind | n / period | net R impact (paper_execution_r) | other effect | reliability | notes |
|---|---|---|---|---|---|---|
| Model F / paper_execution_r | replay (+ forward starting now) | 584 actionable / 30d | actionable touch +6.2R → **+74.1R**; PF 1.43; +0.127R/trade | 42% BE-scratch; givebacks protected | replay-leaning (hindsight trigger, single epoch, no cost haircut) | forward validation pending |
| touch_r relabel | display | all | n/a | stops the touch illusion being read as PnL | reliable | touch overstated ~+100..+143R vs realistic |
| lifecycle status clarity | display | all | n/a | UNKNOWN_INCONSISTENT 87→3 | reliable | display correctness |
| risk-guard warnings | display/advisory | per entry | n/a (alert-only) | surfaces would_pause/sector-cap/correlation | reliable as advisory | block versions NOT evidenced |
| circuit breaker (block) | none-forward | would_pause fires < gate (need ≥10) | unknown | — | insufficient | keep shadow |
| sector/concentration caps (block) | replay weak | few binds | not net-positive demonstrated | — | insufficient | keep shadow |
| position advisor | none | — | — | label-only | none | keep measuring |
| shadow exit manager A–I | replay (negative/inferior) | 30–60d | armed at/after TP1 → −96..−137R band | worse than Model F | reliable-relative | **archive (superseded)** |
| adaptive TP3 | replay | TP3 reach 3.7% | ≈0 net (cohort-positive only) | clarity | replay | not an execution change |
| cohort guard (warn) | replay | crypto_intraday_catalyst n=100 | +0.02R/trade (weakest actionable) | label only | replay | warn = display, no routing |
| intelligence layer | none-forward | <30 closed actionable | unknown | context | insufficient | keep measuring |
| catalyst label refresh/integrity | display/data | continuous | n/a | fixes ~5h news under-fire | reliable | data-quality |
| funding/OI archive | data | continuous | n/a | enables path replay | reliable | keep |
| crypto scalp actionable | replay (negative) | 30d | net-negative every model | drag | reliable | **dangerous** |
| stocks C-tier actionable | replay (negative) | 30d | −34R drag | drag | reliable | **dangerous** |
| stocks swing/invest actionable | replay/policy | — | paused | — | policy | **dangerous** |

## Evidence separation
- **Historical replay evidence:** Model F (+74.1R), shadow-exit variants (inferior), scalp/C-tier (negative), cohort (weak). Reliable for *ranking*, not absolute live R.
- **Forward evidence after implementation:** Model F now tracked forward (since 2026-06-24) — **not yet accumulated**.
- **Display/read-model-only:** touch relabel, status clarity, close-alert, risk-guard warnings, catalyst labels, paper-features panel — correctness, no PnL claim.
- **No evidence:** circuit-breaker block, sector-cap block, position advisor, intelligence layer (all NEED_MORE_DATA).

## Verdict
`SHADOW_FEATURE_EVIDENCE_READY`
