# CRITICAL — Realistic PnL Accounting + Dynamic Stop — FINAL REPORT (PART 10)

**Date:** 2026-06-23. Read-only audit + derived simulation. **No production / paper trade-logic changed; no `final_r` rewritten.**
Supporting: CURRENT_PNL_ACCOUNTING_CRITICAL_AUDIT · REALISTIC_EXECUTION_MODEL_SPEC · REALISTIC_EXECUTION_DATASET_SUMMARY · CURRENT_R_OVERSTATEMENT_ANALYSIS · TP1_GIVEBACK_CASE_STUDY · DYNAMIC_STOP_SIMULATION_RESULTS · PNL_ACCOUNTING_MODEL_DECISION · APP_REALISTIC_PNL_DISPLAY_PLAN · REALISTIC_EXECUTION_ACCOUNTING_TEST_RESULTS. Data: `data/research/realistic_execution_simulation_2026-06-23.csv`.

## The 12 answers
1. **Is the current system "wrong"?** Not *buggy* — it correctly computes "highest TP touched." But as a **PnL** metric it is **optimistic/misleading**: it books TP1/TP2 touches as wins even when the trade later hit the stop.
2. **Under what assumption is it right?** Only if "touching a TP = a real fill that fully closes the position at that level, with no remaining position to give back" — i.e. a perfect resting-limit exit at the best level price reaches. Fine as a *signal-quality* score.
3. **Under what assumption does it overestimate?** Any **single real position** that stays open after TP1 — the normal case. Then TP1→stop is a 0/−1R event, not a +TP1 win.
4. **How many trades affected by TP1→stop / TP2→stop?** **27** actionable give-back trades (8 of them reached TP2). Current books **+37.5R** on them; realistic = **0…+15R** (naive hold = −27R).
5. **How much R changes under realistic models (actionable, ~30–60d)?** Recorded **+2R** → first-TP-close **−105R** · hold-TP3 **−137R** · TP1-BE **−110R** · +0.2R-lock **−104R** · partial50+BE **−107R** · best (+0.5R-lock) **−96R**. **Overstatement ≈ +100…+143R.**
6. **Is the system profitable under each model?**
   | model | actionable 60d | profitable? |
   |---|---|---|
   | current touch | +2R (recorded) / +6R (recon) | ~breakeven (optimistic only) |
   | first-TP close | −105R | **No** |
   | hold-to-TP3 | −137R | **No** |
   | TP1→BE | −110R | **No** |
   | TP1→+0.2R lock | −104R | **No** |
   | partial TP1 + BE runner | −107R | **No** |
   | +0.5R lock (best) | −96R | **No** |
   Shadow book: negative under every model (−116 to −268R).
7. **Does dynamic stop improve results?** **Yes vs naive hold** (+27 to +40R; +0.5R-lock best) — it rescues the give-back cluster. **But it does not make the book positive** (entries are ~32% win rate, negative expectancy).
8. **Does partial TP improve results?** Marginally (partial ≈ first-TP-close, −104 to −107R); better than naive hold, not enough to turn positive.
9. **Which model should become the paper reporting model?** **None replaces `final_r` by rewrite.** Adopt **Option D**: keep legacy `final_r` (labelled "touch-based") and **show a derived `realistic_r` beside it** (default first-TP-close or +0.5R-lock).
10. **Should production/paper trade logic change now?** **No.** This is an accounting/display + research finding. Changing exits is a separate, approval-gated decision.
11. **What to implement next?**
    - **Display/read-model:** add labelled `realistic_r` beside `final_r` in app + reports (PART 8 proposal, default-off flag). **← the real fix for the honesty gap.**
    - **Shadow ledger:** persist the per-trade model R's (extend shadow exit manager) for forward validation.
    - **Paper dynamic-stop flag:** keep **off** — only revisit if/when real execution is considered, with +0.5R-lock / partial+BE as the candidate.
    - **Production:** no change.
12. **What must the operator approve?** (a) Implementing the `realistic_r` display + "touch-based" label in the app; (b) whether the dashboard headline stays Recorded-R-labelled or switches to Realistic-R; (c) standing up the shadow accounting ledger. Nothing else proceeds without it.

## Bottom line (the critical message)
The desk's recorded results are **optimistically overstated**. The actionable book reads ≈ **+2R**, but under **every realistic single-position execution model it is net negative (−96R to −137R over ~30–60 days)**. The positivity is an artifact of "best-TP-touched" accounting that never pays the give-back: 27 trades booked as +37.5R of wins were really 0…+15R. **The system is not profitable under honest execution accounting.** Dynamic stops (best: +0.5R lock / partial+BE after TP1) reduce give-back by +27…+40R but cannot fix negative entry expectancy. The correct, safe action is **accounting honesty (show realistic_r beside the touch number)** — not a trade-logic change.

## Final verdicts
`CURRENT_ACCOUNTING_IS_TOUCH_BASED` · `CURRENT_R_OVERSTATEMENT_QUANTIFIED` · `REALISTIC_EXECUTION_SIMULATION_COMPLETE` · `DYNAMIC_STOP_SIMULATION_COMPLETE` · `PNL_ACCOUNTING_MODEL_DECISION_READY` · `NO_PRODUCTION_TRADE_LOGIC_CHANGE` · `READY_FOR_OPERATOR_DECISION`
