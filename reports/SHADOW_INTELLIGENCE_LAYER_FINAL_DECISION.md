# Shadow Intelligence Layer — Final Decision (PART 10)

**Date:** 2026-06-18 · **Type:** new shadow/diagnostic/add-only intelligence layer. **No trade-math / routing / live change.**

## The 14 questions
1. **All 5 modules implemented?** Yes — symbol timeline, derivatives trajectory, squeeze phase, thesis/invalidation formatter, on-chain risk + an aggregator (`src/intelligence/`).
2. **Shadow/diagnostic only?** Yes — every field `diagnostic_only=True`; payload via `setdefault` (never overwrites); never changes routing/score/TP-SL/size/leverage/exits.
3. **Aggregator avoids external calls in alert path?** Yes — reads only `intelligence.sqlite` caches + a pure deterministic thesis. No network/LLM (socket-block test asserts it). Heavy/external work is background only.
4. **Telegram still compact?** Yes — `intelligence_telegram_lines` returns ≤3 lines; SL/Stop line never replaced (asserted).
5. **Control Plane fields read-only?** Yes — `desk_adapter.py` `.get()` pass-through + optional TS fields; compiles; no command/lock change.
6. **Scheduler non-fatal?** Yes — `intelligence layer update` (every cycle) + `intelligence onchain risk update (daily)`; 24 steps, no duplicates, both `command_nonfatal`.
7. **Tests pass?** 21 intelligence tests + integration + perf all pass. Full suite: **790 passed, 1 failed** — the 1 failure is a **pre-existing, unrelated** stocks-telegram flake (real shared DB + live yfinance, disturbed by the concurrently-running live scheduler), not in the intelligence path. See `SHADOW_INTELLIGENCE_LAYER_TEST_RESULTS.md`.
8. **Performance overhead?** Cached enrichment p50 47ms / p95 63ms / p99 78ms (target met). Background updater does the compute.
9. **What data is missing?** Funding/OI numeric **history** (only a latest snapshot) → derivatives slopes mostly `unknown`, price-primary, accumulates forward. **No contract addresses / on-chain API config** → on-chain = `INTERFACE_READY_CONFIG_MISSING`.
10. **What to check Friday?** Does `squeeze_phase=phase_3_distribution_near_high` / `no_chase_warning` / `thesis_invalidation` / `funding_turning_down` / `timeline_recent_outcome_bias` predict outcomes? Use `SHADOW_INTELLIGENCE_FORWARD_COMPARISON_TEMPLATE.md` + `docs/SHADOW_INTELLIGENCE_FORWARD_METRICS.md`.
11. **Candidates for future soft influence?** `no_chase_warning` / `phase_3_distribution_near_high` (anti-chase), `thesis_invalidation` accuracy, `funding_turning_down`. Only after forward predictive value is shown + operator approval — still shadow now.
12. **What remains locked?** TP/SL, scoring, thresholds, routing/actionability, size, leverage, exits, hard breaker/throttle/cap, sector-cap value, force-close, historical outcomes, Control Plane commands/locks, scalp.
13. **Is live still locked?** Yes.
14. **Rollback plan?** Remove the intel block from `paper_entry.py` + the 2 scheduler steps; delete `src/intelligence/` + `data/intelligence/` + the 2 scripts + the test; revert the Control-Plane `.get()` keys + TS fields. Zero trade impact (it never touched trades).

## Verdicts
- **SHADOW_INTELLIGENCE_LAYER_READY**
- SYMBOL_TIMELINE_MEMORY_READY · DERIVATIVES_TRAJECTORY_READY (price-primary) · SQUEEZE_PHASE_CLASSIFIER_READY · THESIS_FORMATTER_READY · ONCHAIN_RISK_LAYER_INTERFACE_READY_CONFIG_MISSING
- INTELLIGENCE_SCHEDULER_READY · NO_TRADE_MATH_CHANGE · LIVE_REMAINS_LOCKED · FRIDAY_FORWARD_COMPARISON_REQUIRED

## Principle honored
A context layer, not a strategy change. The desk is smarter per signal (phase / derivatives / thesis / timeline / on-chain context) without a slower monitor (p95 63ms, cache-only, no network in path) or riskier trade logic (nothing influences decisions). Unstable/slow data (funding/OI history, on-chain) is background-only, cached, or marked unknown — it never blocks signals.
