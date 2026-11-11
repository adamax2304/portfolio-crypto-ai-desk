# Paper Feature Promotion — Implementation Report (PART 6)

**Date:** 2026-06-24. Implemented ONLY display/accounting/advisory promotions. PAPER-ONLY, feature-flagged, reversible, tested. No live/exec, no production order logic, no historical `final_r` rewrite.

## Implemented
1. **Unified paper-feature registry — `config/paper_features.yaml` (NEW).** Single source of truth: per feature `state` (active_paper_accounting | active_paper_display | active_advisory | keep_measuring | keep_shadow | archived | dangerous_locked), `affects_trades` (all active = false), evidence, decision_date. Default-safe; flip any `active_*`→`off` to disable.
2. **Cohort guard promoted off → warn (display-only).** `config/cohort_guard.yaml` `mode: warn` = a dashboard label on `crypto_intraday_catalyst_or_momentum`; **no routing/actionability/scoring change**. `paper_review_only` (a paper routing change) stays gated behind `feature_flag: paper_cohort_guard.enabled` (default false) + operator sign-off.
3. **Backend Paper-Features read-model — `backend/app/paper_features.py` (NEW) + `GET /api/paper-features`.** Returns active / shadow-or-measuring / archived / dangerous-locked lists + counts + `live_locked/auto_live_locked: true`. Reads cohort mode best-effort. Verified live: 6 active, 3 shadow, 1 archived, 3 locked.
4. **Per-trade paper-feature tags — `books.paper_exec_flags`.** Adds `cohort_warning` + `paper_feature_tags` (`model_f`, `be_protected`, `profit_lock`, `giveback_protected`, `cohort_warn`). Surfaced on trade rows.
5. **Already-active (verified, no further action):** Model F / `paper_execution_r` (accounting), touch_r relabel (display), lifecycle status clarity, close-alert Model F line, risk-guard warnings (alert-only), catalyst label refresh/integrity, funding/OI archive.

## Not implemented (per decision table)
- KEEP_MEASURING: adaptive TP3, intelligence layer, position advisor, risk-off label.
- KEEP_SHADOW: circuit-breaker block, sector/concentration cap block.
- KILL/ARCHIVE: shadow_exit_manager variants (see PART 7).
- DANGEROUS/NEED_APPROVAL: scalp/C-tier/swing-invest actionable; cohort `paper_review_only`; Model F as a real-paper-stop execution flag.

## Safety
- All changes are config/read-model/display. Tracker exits, scoring, entry, routing, TP/SL generation, `signal_outcomes` — untouched. Scheduler unchanged (no new step needed; paper_execution_refresh already runs). `/api/health` stays `live_locked:true`.

## Verdict
`APPROVED_PAPER_FEATURES_IMPLEMENTED`
