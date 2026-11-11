# POST — Operational Guardrails Deploy Final Decision (PART 10)

**Date:** 2026-06-17 · **Stage:** operational deployment of safe diagnostics (alert-only / shadow-only / read-only / label-only / data-collection).
**Nothing changed live trading, auto-live, exchange execution, scalp enablement, scoring, TP/SL, thresholds, the sector-cap value, BE/partial/trailing trade logic, stop/TP widths, hard breaker/throttle/cap, force-close, history, or Control Plane safety/commands/locks.**

## Deliverables
Reports: `PRE_OPERATIONAL_GUARDRAILS_DEPLOY_BASELINE.md`, `OPERATIONAL_CIRCUIT_BREAKER_ALERT_ONLY_DEPLOYMENT.md` + `OPERATIONAL_CIRCUIT_BREAKER_DRY_RUN.md`, `OPERATIONAL_CATALYST_INTEGRITY_SCAN_DEPLOYMENT.md` + `POST_CATALYST_SCAN_INTEGRITY_VERIFICATION.md` + `CATALYST_INTEGRITY_DAILY_SUMMARY.md`, `OPERATIONAL_RISK_GUARD_VISIBILITY_VERIFICATION.md` + `CONTROL_PLANE_RISK_FIELDS_DISPLAY_PLAN.md`, `OPERATIONAL_INTRADAY_LIFECYCLE_LABELS_DEPLOYMENT.md` + `OPEN_INTRADAY_LIFECYCLE_REVIEW.md`, `OPERATIONAL_SECTOR_CAP_SHADOW_LOGGING_DEPLOYMENT.md` + `SECTOR_CAP_WOULD_BIND_FORWARD_TRACKER.md`, `OHLCV_ARCHIVE_IMPLEMENTATION.md` + `OHLCV_ARCHIVE_COVERAGE_REPORT.md` + `PROFIT_PROTECTION_REPLAY_DATA_READINESS.md`, `POSITION_LEVERAGE_ADVISOR_IMPLEMENTATION.md` + `_TEST_RESULTS.md`, `STOCKS_INTRADAY_REWORK_DIAGNOSTIC.md` + `STOCKS_INTRADAY_FILTER_COUNTERFACTUAL.csv` + `STOCKS_INTRADAY_SAFE_RESTRICTION_PLAN.md`, `POST_OPERATIONAL_GUARDRAILS_DEPLOY_TEST_RESULTS.md`, this report.
Code: `src/risk/position_advisor.py`; scheduler steps in `run_default_market_schedule.py`; scripts `archive_ohlcv_history.py`, `circuit_breaker_dry_run.py`, `sector_cap_forward_tracker.py`, `stocks_intraday_diagnostic.py`, `open_intraday_lifecycle_review.py`; advisor wiring in `risk_guards.py`; archive-first replay; Control-Plane display plan.

## The 15 questions
1. **Circuit breaker alert-only operational?** Yes — computed on every B/A alert payload + a deduped Telegram would-pause line; dry-run command added. Today: crypto books would_pause, stocks ok.
2. **Catalyst integrity scan scheduled?** Yes — non-fatal step right after `catalyst-scan`; writes the daily summary + warns on regression signature.
3. **Risk fields visible in Telegram?** Yes — compact diagnostic lines appended after the freshness line; SL always preserved; plain-text (no markdown/cp1252 crash).
4. **Fields visible in Control Plane?** Yes (read-only) — adapter passes them through, TS `Signal` has optional fields; UI display plan written (not built, no break).
5. **Lifecycle labels operational?** Yes — per-cycle `open intraday lifecycle review` (229 open, 12 need review); per-signal labels in payload; no force-close.
6. **Sector-cap would-bind tracking live?** Yes — logged per stocks-intraday A/B alert; forward tracker reads it. Accumulates from now (historical payloads lack the field).
7. **OHLCV archive started?** Yes — append-only 5m/15m, deduped, idempotent; seeded 407/469 symbols today; archive-first in the replay.
8. **Leverage advisor label-only ready?** Yes — `src/risk/position_advisor.py`, 8 tests; notional + max-safe-leverage + unsafe flag; never executes/sizes.
9. **What does stocks-intraday diagnostic say?** 30d net **+106R**; the drag is **C-tier (−34R)**, B-tier carries (+132R). Dropping C-tier → +140R. Catalyst/RTH filters don't help (catalyst too sparse; RTH counterproductive). Recommendation: **C-tier → shadow/review-only** (with approval), keep A/B.
10. **Did full tests pass?** Yes — **742 passed, 0 failed** (729 + 13 new).
11. **What remains locked?** Live, auto-live, exchange execution, scalp enablement, scoring, TP/SL, thresholds, sector-cap value, BE/partial/trailing trade logic, hard breaker/throttle/cap, force-close, history, Control Plane safety/commands/locks.
12. **What can be enabled next after 7–10 days?** (still paper, with approval) the **C-tier stocks-intraday → shadow** restriction (data-supported now, validate forward first); promote the catalyst-integrity + circuit-breaker warnings to the system Telegram channel.
13. **What needs 30d data?** Path-aware **profit protection** (BE-after-1R / partial-TP1) — needs the OHLCV archive to reach ≥70% coverage across up+down regimes; and the **risk-off throttle** decision.
14. **What should absolutely NOT be enabled yet?** Profit protection in trade logic, hard circuit breaker, risk-off hard throttle, sector-cap hard block, any leverage/auto-sizing execution, stocks-scalp, crypto-scalp-actionable.
15. **Is manual micro-live allowed now?** **No.** Diagnostics are deployed but no new profitable behavior is proven. Micro-live only after forward validation of the alert-only guardrails + a representative profit-protection replay.

## Next 3 actions
1. Let the scheduler run the new steps for **7–10 days**; review the circuit-breaker dry-run + open-intraday-review + catalyst-integrity daily summaries; confirm the ASTER flag clears after a fresh catalyst-scan.
2. After ~2–4 weeks, check `OHLCV_ARCHIVE_COVERAGE_REPORT.md` → re-run the path-aware profit replay at ≥70% coverage.
3. With your approval, apply the **C-tier stocks-intraday → shadow** restriction (the one data-supported, high-leverage safe change) and forward-measure it.

## Final verdict roll-up
- **OPERATIONAL_GUARDRAILS_DEPLOYED**
- CIRCUIT_BREAKER_ALERT_ONLY_OPERATIONAL · CATALYST_INTEGRITY_SCAN_OPERATIONAL · RISK_FIELDS_VISIBLE · OHLCV_ARCHIVE_STARTED · POSITION_ADVISOR_LABEL_ONLY_READY
- STOCKS_INTRADAY_KEEP_WITH_FILTERS (drop C-tier; review-only for C-tier) — *recommendation, not applied*
- PROFIT_PROTECTION_STILL_DISABLED · NO_PRODUCTION_STRATEGY_CHANGE · SYSTEM_NOT_READY_FOR_LIVE

## Principle honored
Dangerous states are now visible (breaker, carryover, risk-off, would-bind), missing data is being collected (OHLCV archive), catalyst/risk mistakes are caught automatically, and profit-protection proof is being prepared properly — without touching live trading.
