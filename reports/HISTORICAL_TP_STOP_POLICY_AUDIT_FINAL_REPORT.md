# Historical TP / Stop Management Audit + Counterfactual Replay — FINAL (PART 11)

**Date:** 2026-06-23. Read-only audit + replay. **No production / paper trade-logic changed.**
Supporting reports: STOP_AFTER_TP_ACTUAL_BEHAVIOR_AUDIT · TP_STOP_REPLAY_DATASET_SUMMARY · TP_REACH_RATE_ANALYSIS · TP_POLICY_COUNTERFACTUAL_REPLAY · STOP_MANAGEMENT_COUNTERFACTUAL_REPLAY · TP3_HELP_HURT_CLASSIFICATION · TP_STOP_POLICY_DECISION · ADAPTIVE_TP_POLICY_IMPLEMENTATION_PROPOSAL · TP_STOP_REPLAY_TEST_RESULTS. Data: `data/research/tp_stop_replay_dataset_2026-06-23.csv`.

## The 19 answers
1. **How many trades analyzed?** 1404 deduped entered economic trades (60d, 100% path coverage); actionable subset 582.
2. **Books?** Included = Operator/Paper (actionable A/B, non-scalp, non-stocks-swing/invest) = 582. Excluded from decision (reported separately) = Shadow (C-tier, crypto scalp, stocks swing/invest) = 822.
3. **Does the stop move after TP1/TP2?** **NO.** Stop is the fixed invalidation for the whole trade. No BE, no profit-lock, no trailing in production. (BE/partial/trailing exist only in the shadow exit manager, off.)
4. **Does TP1 close the whole paper trade or partial?** **Neither** — no partial, no remaining position. The model **books the R of the highest TP the price touched** (optimistic): TP1-then-stop is recorded as a **+TP1 win**, not a loss.
5. **Are TP2/TP3 actually used?** They are real levels the walker checks; the highest one touched sets `final_r`. There is **no hold-for-TP3 simulation** — the outcome already credits the best level reached.
6. **How often was TP3 reached?** **3.7% of all** entered (52/1404); **7.7% of actionable** (45/582). TP1 17.7% / TP2 8.0% (all).
7. **Net R from TP3?** Under production accounting TP3 **ADDS** R: **+45R** (actionable), +52R (all). Removing it saves no losers (losers never reach TP3).
8. **Risk-off — TP3 help shorts?** Yes, modestly — trend-aligned (risk-off/bearish-trend) **shorts** reach TP3 and add R (e.g. `crypto_failed_bounce_short` +9R, positive even under hold). Small n.
9. **Risk-off — TP3 hurt longs?** Counter-regime longs (risk-off longs) rarely extend to TP3; TP3 adds ≈0 and holding-for-it bleeds — but the loss is on entries, not the TP3 level.
10. **Chop/mixed — TP3 hurt?** TP3 essentially unreachable in chop (reached ~1–3×); capping at TP2 changes net R ≈0. TP3 is noise there, not a major drag.
11. **Which playbooks deserve TP3?** `crypto_swing_narrative_rs` (+16R), `crypto_failed_bounce_short` (+9R), `crypto_intraday_catalyst` (+11R, catalyst-gated). Trend/continuation setups.
12. **Which should max at TP2?** `stocks_intraday_rth_momentum`, `stocks_swing_watchlist_rs`, `stocks_invest_watchlist_30d`, `crypto_scalp` (shadow), and chop-regime trades — TP3 ~never reached there.
13. **Would "2 TP default, TP3 only trend-runner" improve results?** **No.** "2 TP default" is **−45R** (clips winners, saves nothing). "TP3 only trend-runner" reproduces baseline (≈0 R) because TP3 hits already cluster in exactly those trend cohorts — it would help *clarity*, not R.
14. **Would BE/profit-lock after TP1 improve results?** **Not provable.** Against the current optimistic accounting it's worse; against a hold-to-far-target baseline it helps (+27R). True operator behavior unknown → relative-only. Give-back set is small (3%).
15. **Replay reliability?** Reconstruction matches recorded `final_r` 99.8% (3 mismatches = the 3 same-candle-ambiguous trades). TP-count conclusions are **reliable** (they use the recorded best-TP outcomes). Hold/BE/partial absolute R is **RELATIVE-ONLY** (5m/15m granularity, same-candle stop-first, optimistic baseline).
16. **Enough to change paper rules?** **No** — the only TP-count gate that matters ("improves net R ≥+2R") fails (−45R); stop-mgmt evidence is relative-only.
17. **Enough to change production rules?** **No.**
18. **Exact recommendation:**
   - TP count → **NO_CHANGE_KEEP_CURRENT** (keep 3 TP levels; removing TP3 destroys realized upside).
   - Adaptive-TP3 + BE/partial → **KEEP SHADOW / MORE DATA** (optional shadow ledger + display-only annotation, default-off; see proposal).
   - **No paper-only flag yet; no production proposal.**
19. **Monitor next 7 days:** per-cohort TP3 reach-rate + add-R (esp. crypto swing / failed-bounce-short); give-back count (TP1→stop); whether forward actionable closes accumulate toward n≥30 per playbook; keep the shadow exit ledger current. Re-evaluate adaptive-TP3 only when a cohort clears n≥30 with ≥+2R shadow improvement.

## Bottom line
The system uses **3 fixed TP levels, a fixed stop that never moves, no partials, and an optimistic "best-TP-touched" outcome model.** TP3 is rarely reached but is pure upside as scored, so **removing it would only cut winners** — the "2 TP default" idea is not supported by the data. The genuine issue the idea targets — *giving back a winner while waiting for a far target* — is small (3%) and is a **stop/partial** question, not a TP-count one, and the evidence for stop-management is only relative. The only cohorts that truly earn TP3 are crypto swing-narrative and crypto failed-bounce shorts (+ catalyst intraday).

## Verdicts
`CURRENT_STOP_BEHAVIOR_CONFIRMED` · `TP_POLICY_REPLAY_COMPLETE` · `STOP_MANAGEMENT_REPLAY_COMPLETE` · `TP3_CONDITION_MAP_READY` · `TP_POLICY_DECISION_READY` · `NO_PRODUCTION_TRADE_LOGIC_CHANGE` · `READY_FOR_OPERATOR_DECISION`
