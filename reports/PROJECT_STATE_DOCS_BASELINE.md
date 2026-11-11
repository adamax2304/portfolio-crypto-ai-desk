# Project-State Docs — Baseline (PART 0)

**Date:** 2026-06-18 · **Type:** documentation sprint (no trading-logic change). Extracted from the latest decision reports.

## Sources read
- `reports/POST_FAST_SAFE_ACCELERATION_FINAL_DECISION.md`
- `reports/POST_BACKFILL_PROFIT_PROTECTION_REPLAY.md`
- `reports/OHLCV_HISTORICAL_BACKFILL_COVERAGE_REPORT.md`
- `reports/SHADOW_EXIT_LEDGER_SUMMARY.md`
- `reports/POST_OPERATIONAL_GUARDRAILS_DEPLOY_FINAL_DECISION.md`
- `reports/POST_PROFITABILITY_GUARDRAILS_FINAL_DECISION.md`

## Extracted state
- **Latest full test result:** 766 passed, 0 failed (last run 2026-06-18; prior 742; baseline 729/687).
- **Active verdicts:** FAST_SAFE_ACCELERATION_COMPLETE · STOCKS_C_TIER_SHADOW_APPLIED · OHLCV_BACKFILL_READY · SHADOW_EXIT_MANAGER_READY · SYSTEM_STABLE · PROFIT_PROTECTION_STILL_DISABLED · NO_PRODUCTION_TRADE_MATH_CHANGE · MICRO_LIVE_NOT_YET / MICRO_LIVE_CANARY_REVIEW_IN_7_10_DAYS.
- **Locked rules:** live/auto-live/exchange-exec, crypto scalp actionable, stocks scalp prod, TP/SL, scoring, thresholds, sector-cap value, BE/partial/trailing in trade logic, hard breaker/throttle/cap, leverage execution, force-close, historical outcomes, Control Plane commands/locks/safety.
- **Operational (alert-only / read-only):** circuit breaker alert-only; catalyst integrity scan; OHLCV archive + historical backfill; open intraday lifecycle review; sector-cap would-bind tracker; position/leverage advisor (label-only); Telegram + Control Plane risk fields.
- **Shadow-only / measurement:** shadow exit manager (BE+0.5R, BE+1R, partial-TP1, trailing, candle-close, re-entry); sector-cap would-bind; risk-off throttle label; profit-protection variants.
- **Current blockers:** (a) shadow A_current is pessimistic vs the real book (5m + conservative stop-first → −39R shadow vs +6R actual on same 146 trades) — must reconcile before trusting absolute shadow R; (b) the 30d tested window was net-losing, so no exit variant is profitable, only less-bleeding; (c) ASTER catalyst-integrity flag still trips on the pre-fix on-disk artifact — must clear after a fresh catalyst-scan.
- **Next 7–10 day goals:** confirm guardrail stability; ASTER flag clears; circuit-breaker/lifecycle signals useful; shadow exits behave forward; consider micro-live *canary review* only.
- **30-day goals:** is profit-protection useful across up+down regimes? can partial-TP1 / BE-after-1R become a paper-rule candidate? is risk-off throttle justified? paper→manual-micro-live→small-controlled-live path.
- **Micro-live gates:** tests green; scheduler stable; Telegram clean; Control Plane safe; ASTER cleared; CB dry-run reasonable; no scalp; no C-tier; no live automation; manual-only; tiny risk/trade; operator confirms each trade.
- **Open risks:** regime-specificity of the shadow result; timeframe-reconciliation gap; data depth only ~60d archived so far; crypto book ~breakeven, stocks-intraday carried by B-tier.

## Deliverables of this sprint
PROJECT_STATE.md · docs/DECISION_LOG.md · docs/decisions/ADR-0001..0005 + ADR-TEMPLATE.md · docs/AGENT_HANDOFF.md · docs/WEEKLY_FORWARD_METRICS.md · README pointer · scripts/check_project_state_docs.py · tests/test_project_state_docs.py · this baseline + implementation report.
