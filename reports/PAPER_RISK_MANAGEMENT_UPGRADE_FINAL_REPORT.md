# Active Paper Risk-Management Upgrade — FINAL REPORT (PART 11)

**Date:** 2026-06-24. PAPER / ACCOUNTING ONLY. No live/exec. No historical `final_r` rewrite.
Supporting: PAPER_RISK_UPGRADE_BASELINE_AUDIT · PAPER_EXECUTION_ACCOUNTING_SPEC · PAPER_MODEL_F_IMPLEMENTATION_REPORT · HISTORICAL_PAPER_EXECUTION_RECALC_REPORT · CONTROL_PLANE_PNL_CORRECTION_REPORT · TELEGRAM_PAPER_RISK_DISPLAY_REPORT · BAD_COHORT_PROTECTION_PLAN · PAPER_RISK_UPGRADE_TEST_RESULTS · POST_PAPER_RISK_UPGRADE_SYSTEM_SANITY · PAPER_RISK_UPGRADE_DOC_UPDATE_REPORT.

## The 13 answers
1. **What changed?** A new authoritative paper PnL — `paper_execution_r` (Model F, early MFE-armed protection) — now sits beside the legacy touch-based `final_r`. New module + table + tracker hook + scheduler step + CLI + close-alert line + recalc CSV; Control Plane app/Telegram now lead with Paper Execution R and label Touch R "optimistic". Default-off cohort-guard config added (not forced).
2. **Is Model F now active?** Yes — `early_mfe_protection_v1` computes a paper outcome for every entered signal, live (tracker hook) + backfilled (CLI/scheduler).
3. **Active only for paper/accounting?** Yes. It never places orders, never changes exits/scoring/entry/routing/TP-SL; writes only the additive `paper_execution_outcomes` table.
4. **Did live/execution stay off?** Yes — `/api/health` → `live_locked:true, auto_live_locked:true`; scheduler has 0 live/exchange/order steps.
5. **Did historical `final_r` stay unchanged?** Yes — 315,610 `signal_outcomes` rows + `final_r` intact; no column added there; `m0/touch` reproduces it read-only.
6. **What does the app show now?** Headline **Today R · Paper Exec (Model F)**; secondary **Recorded Touch R** ("highest TP touched · optimistic"); 48h paper W/L + BE-scratch; "48h Protected · stops→BE/lock · giveback"; per-trade paper R + touch + protection badges; closed-detail old-vs-new explanation + protection timeline; ⚠ fallback warning if MFE missing.
7. **Today Paper Execution R vs Touch R?** Live Operator headline at restart: **today paper −1.0R vs touch −1.0R; 48h paper +20.0R vs touch +18.0R; 7d paper +21.5R**. (Operator = delivered subset; deduped.)
8. **48h / 7d / 30d recalc (actionable, deduped)?** 48h paper **+7.8R** (touch +6.4); 7d paper **+13.6R** (touch −5.0); 30d/all paper **+74.1R** (touch +6.2, no-risk-mgmt −104.8). Shadow negative throughout (excluded).
9. **What tests passed?** 74 crypto-ai-desk (incl. 10 new accounting + storage/no-mutation) + 53 backend (incl. paper-exec read-model) + frontend `npm run build` clean. Scheduler guard + docs validator OK.
10. **What files changed?**
   - crypto-ai-desk: `src/execution/__init__.py`, `src/execution/paper_execution_accounting.py` (new), `src/signals/tracker.py` (hook), `src/cli.py` (command), `scripts/run_default_market_schedule.py` (step), `scripts/paper_execution_recalc.py` (new), `src/notifiers/close_alert.py` (paper line), `tests/test_paper_execution_accounting.py` (new), `config/cohort_guard.yaml` (new, default-off), docs (PROJECT_STATE/DECISION_LOG/WEEKLY_FORWARD_METRICS/SHADOW_MODE_REGISTRY), DB table `paper_execution_outcomes`, `data/research/paper_execution_recalc_2026-06-23.csv`.
   - trading-desk-control: `backend/app/books.py`, `backend/app/desk_adapter.py`, `frontend/src/types.ts`, `frontend/src/screens.tsx`, `backend/tests/test_books.py`, README.
11. **What cohorts are still dangerous?** `crypto_intraday_catalyst_or_momentum` (chase-longs, +0.02R/trade even under Model F) — guarded default-OFF, not disabled. Already-shadow: crypto scalp, stocks swing/invest, C-tier.
12. **What to watch next 7 days?** Forward (post-2026-06-24) Operator `paper_execution_r` net-positive?; paper-vs-touch divergence + giveback/protected counts firing; `paper_unavailable_n` stays 0; apply a cost/slippage haircut (Model F is ~42% BE-scratch); the chase-long cohort's forward paper R.
13. **What remains blocked until approval?** Any **production** exit change (BE/partial/trailing in the real tracker), any live/auto-live/exchange execution, any actionability/routing change for the weak cohort (config is paper-only + default-off), and graduating Model F from "paper accounting" to a "paper trade-execution flag" — all require the gates in `RISK_MANAGEMENT_IMPLEMENTATION_GATES.md` + explicit sign-off.

## Bottom line
The desk now reports an **honest paper PnL**: the optimistic touch-based number is demoted to a labelled signal-quality metric, and the authoritative `paper_execution_r` applies early MFE-armed protection (BE @ +0.6R, lock +0.5R @ +1R) — the lever the viability audit identified. In replay this flips the actionable book from the touch illusion to **+74.1R**; the app, Telegram, and ledger all now lead with it. Nothing in production trading logic changed, `final_r` was never rewritten, and live stays locked. The +74R is a hindsight/30-day replay — the system is now instrumented to **forward-validate** it.

## Final verdicts
`PAPER_EXECUTION_ACCOUNTING_DEFINED` · `MODEL_F_ACTIVE_FOR_PAPER_ACCOUNTING` · `APP_USES_PAPER_EXECUTION_R` · `TOUCH_R_LABELLED_AS_OPTIMISTIC` · `HISTORICAL_FINAL_R_UNCHANGED` · `NO_LIVE_EXECUTION_ENABLED` · `NO_PRODUCTION_TRADE_LOGIC_CHANGE` · `READY_FOR_FORWARD_PAPER_VALIDATION`
