# TP / Stop Policy Decision (PART 8)

**Date:** 2026-06-23. Gate-based. **No production or paper rule change made.**

## Gate evaluation — paper-only TP-policy test
| gate | required | actual | pass? |
|---|---|---|---|
| n relevant closed entered | ≥ 30 | 582 actionable (1404 all) | ✅ |
| path coverage | ≥ 90% | 100% (60d backfill) | ✅ |
| **counterfactual improves net R** | **≥ +2R** | **−45R** (remove-TP3) / ≈0 (conditional B–F) | ❌ |
| does not clip more winner R than it saves | — | clips 45 TP3 winners, saves 0 losers | ❌ |
| improvement in ≥2 symbols/playbooks | — | none (no improvement exists) | ❌ |
| same-candle ambiguity not decisive | — | ok (give-back only 3%) | ✅ |
| feature-flaggable & reversible | — | yes | ✅ |

**The "improves net R" gate FAILS decisively.** Removing/restricting TP3 reduces realized R (clips winners, saves no losers) under the production accounting; conditional variants ≈ break-even. **No TP-count variant earns a paper test.**

## Gate evaluation — stop-management (BE / partial / profit-lock)
- Evidence is **relative-only** (optimistic best-TP baseline + 5m/15m granularity + same-candle). Against current accounting every variant is worse; against a hold-to-TP3 baseline they help (+19…+33R). The true operator exit behavior is unknown → **cannot prove ≥+2R absolute improvement.**
- Give-back set is small (3%). Prior independent shadow-exit replay already concluded profit-protection is net-negative/regime-specific and is **disabled** (DECISION_LOG 2026-06-18).
- Per-cohort actionable n where it could matter is below the production gate (need ≥30 per playbook + forward validation).

## Decisions
| Question | Decision |
|---|---|
| **2 TP default / remove TP3** | **NO_CHANGE_KEEP_CURRENT** — removing TP3 is net-negative; TP3 is rare but pure upside in the current model. |
| **TP3 only trend-runner (adaptive)** | **SHADOW_ONLY_MORE_DATA** — conceptually sound (TP3 only earns in crypto-swing / failed-bounce-short / catalyst), but it reproduces baseline R (≈0 improvement); only worth it for *clarity/churn*, not R. Measure in shadow first. |
| **BE / partial / profit-lock after TP1** | **SHADOW_ONLY_MORE_DATA** — relative-only evidence; helps only under a hold-to-far-target assumption; profit-protection already shadow-disabled. Needs a proper per-cohort shadow ledger + forward data. |
| **Production change** | **NONE.** No gate for production passes. |

## Verdict
`TP_POLICY_DECISION_READY` — **NO_CHANGE_KEEP_CURRENT (TP count)** + **SHADOW_ONLY_MORE_DATA (adaptive-TP3 + stop-management)**. No production/paper trade-logic change.
