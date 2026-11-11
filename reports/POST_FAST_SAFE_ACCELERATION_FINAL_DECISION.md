# POST — Fast Safe Acceleration Final Decision (PART 6)

**Date:** 2026-06-18 · **Stage:** apply the obvious C-tier leak as explicit policy + accelerate evidence (OHLCV backfill, shadow exits) + stability. **No live, no trade-math change.**
**Full suite: 766 passed, 0 failed** (742 baseline + 24 new). Exit 0.

## Deliverables
Code: `src/signals/tier_policy.py`, `src/exits/shadow_exit_manager.py`, `scripts/backfill_ohlcv_history.py`, `scripts/shadow_exit_ledger_update.py`, `scripts/shadow_exit_summary.py`; config flag `tier_policy.stocks_intraday_c_tier`; wiring in `paper_entry.py` + `risk_guards.py`; archive-first replay.
Reports: baseline (PART 0); C-tier impl/test/verification (PART 1); backfill impl + coverage + gaps.csv (PART 2); shadow-exit impl/test + ledger summary (PART 3); stability + scheduler/Telegram/Control-Plane checks (PART 4); post-backfill replay (PART 5); this (PART 6).
Tests: `test_stocks_c_tier_policy.py` (9), `test_shadow_exit_manager.py` (10), `test_ohlcv_backfill.py` (5).

## The 15 questions
1. **Was C-tier stocks intraday moved to shadow/review-only?** Yes — as an explicit, configurable, labeled policy (`tier_policy.stocks_intraday_c_tier: shadow_review_only`). Note: it was **already** non-actionable (`decide_paper_entry` blocks all C-tier), so the −34R was a tracking artifact, not live exposure — behavior unchanged, restriction now explicit.
2. **Did A/B stocks intraday remain unchanged?** Yes (tests confirm B-tier still actionable; crypto + swing/invest untouched).
3. **Was OHLCV backfill completed?** Yes — 70 symbols × {5m,15m} × 60d on Binance, 140/140 ok, 0 failures.
4. **What coverage did backfill achieve?** ~98.1% of expected candles; **0% gaps**; path-aware replay coverage **17.8% → 100% (146/146)**.
5. **Is shadow exit manager working?** Yes — `src/exits/shadow_exit_manager.py` + ledger (146 trades, 100% covered), 10 tests, archive-first, conservative same-candle, honest coverage labels.
6. **What did the shadow ledger show?** Relative to a (pessimistic 5m) shadow baseline of −39.2R, BE-after-+0.5R cuts drawdown most (−1.2R), partial-TP1+BE / BE-after-+1R next. **But** shadow A_current (−39.2R) is pessimistic vs the **real recorded book (+6.0R)** due to 5m + stop-first same-candle — so only RELATIVE deltas are valid. This 30d window is net-losing, so no variant is profitable, only less-bleeding.
7. **Did stability checks pass?** Yes — FAST_ACCELERATION_STABLE (19 scheduler steps, no dups, non-fatal; Telegram SL preserved; Control Plane compiles read-only).
8. **Did Telegram remain clean?** Yes — SL always present, diagnostics appended, plain-text, deduped, no crash.
9. **Did Control Plane remain safe?** Yes — read-only `.get()` pass-through, optional TS, no command/lock/routing change.
10. **Did catalyst integrity ASTER flag clear?** Not yet — the pre-fix on-disk artifact still trips it; it should clear after the next fresh `catalyst-scan` (the integrity step runs right after). Re-verify next cycle; if it persists post-scan, that's a real regression.
11. **Did full tests pass?** **766 passed, 0 failed.**
12. **What remains locked?** Live, auto-live, exchange execution, scalp enablement, scoring, TP/SL, thresholds, sector-cap value, BE/partial/trailing in trade logic, hard breaker/throttle/cap, leverage execution, force-close, history, Control Plane safety/commands/locks.
13. **Can we consider manual micro-live in 7–10 days?** Only a **canary review**, not a green light. After 7–10 days of forward data confirming the guardrails behave + the catalyst flag clears, we can *review* readiness. Profitability is still unproven.
14. **What still needs 30d?** A profit-protection enable decision needs the shadow candidate confirmed across an **up/trending** month (this was a losing window) + reconciliation of the 5m-shadow-vs-tracker timeframe gap; and the risk-off throttle decision.
15. **What is the next safest change?** Forward-measure the **partial-TP1 / BE-after-+1R** shadow rule (no enable); optionally stop *registering* C-tier stocks-intraday to clean the measured book (separate, needs approval).

## Next 3 actions
1. Let the scheduler run 7–10 days; confirm the catalyst ASTER flag clears after a fresh scan; watch the circuit-breaker dry-run + lifecycle review.
2. Re-run the shadow replay/ledger weekly; reconcile the 5m-vs-tracker timeframe discrepancy so absolute shadow R is trustworthy; confirm the BE/partial candidate on an up-month.
3. With approval, forward-measure partial-TP1 as a SHADOW rule (still no trade-logic change).

## Verdict roll-up
- **FAST_SAFE_ACCELERATION_COMPLETE** · **STOCKS_C_TIER_SHADOW_APPLIED** · **OHLCV_BACKFILL_READY** · **SHADOW_EXIT_MANAGER_READY** · **SYSTEM_STABLE**
- **PROFIT_PROTECTION_STILL_DISABLED** (partial-TP1 / BE-after-1R = shadow candidates) · **NO_PRODUCTION_TRADE_MATH_CHANGE**
- **MICRO_LIVE_NOT_YET** → **MICRO_LIVE_CANARY_REVIEW_IN_7_10_DAYS**

## Principle honored
Removed the obvious weak tier as an explicit policy (no behavior change since it was already non-actionable), backfilled the missing data so exit evidence is now decision-grade (100% coverage), measured exits in shadow with honest caveats, verified stability — and kept every real trade exit unchanged.
