# Agent Handoff

This file orients the next agent. Read it before doing anything.

## Read This First (in order)
1. `../PROJECT_STATE.md` — current status, verdicts, locked rules, next actions.
2. `DECISION_LOG.md` — what was decided and why.
3. Latest final-decision report: `../reports/POST_FAST_SAFE_ACCELERATION_FINAL_DECISION.md`.
4. Latest profit-protection replay: `../reports/POST_BACKFILL_PROFIT_PROTECTION_REPLAY.md`.
5. Latest catalyst integrity: `../reports/CATALYST_INTEGRITY_DAILY_SUMMARY.md` (+ `POST_CATALYST_SCAN_INTEGRITY_VERIFICATION.md`).
6. ADRs: `decisions/ADR-0001..0005`.

## Do NOT Touch (locked — require explicit operator approval)
live / auto-live / exchange execution · crypto scalp actionable · stocks scalp production · TP/SL · scoring · thresholds · sector cap value · BE / partial / trailing in real trade logic · hard circuit breaker · hard risk-off throttle · hard sector-cap block · leverage execution · force-close logic · historical outcomes · Control Plane commands / locks / safety.

Everything operational today is **alert-only / shadow-only / read-only**. Keep it that way unless the operator explicitly approves a change.

## Current Task Queue
- **3–5 day checks:** scheduler runs clean; ASTER catalyst flag clears after a fresh `catalyst-scan`; Telegram + Control Plane stable; circuit-breaker dry-run sane; lifecycle review catches real carryover/stale.
- **7–10 day canary review:** evaluate the Manual Micro-Live Gate in `PROJECT_STATE.md` (review only — not a green light).
- **Tracker vs 5m shadow reconciliation:** explain/close the gap between shadow A_current (−39R, 5m + stop-first) and the actual recorded book (+6R) so absolute shadow R is trustworthy.
- **Weekly shadow exit replay:** `python -m scripts.shadow_exit_ledger_update && python -m scripts.shadow_exit_summary`; record in `WEEKLY_FORWARD_METRICS.md`.
- **Catalyst ASTER flag verification:** `python -m scripts.catalyst_integrity_scan` after a fresh scan. (Cleared 06-18.)
- **Friday shadow-intelligence forward comparison:** populate `docs/SHADOW_INTELLIGENCE_FORWARD_METRICS.md` + `reports/SHADOW_INTELLIGENCE_FORWARD_COMPARISON_TEMPLATE.md` from `signal_alerts.payload_json` (squeeze_phase / no_chase_warning / thesis_invalidation / derivatives) joined to outcomes. Keep all intelligence fields **shadow** unless they show forward predictive value AND the operator approves a soft-warning promotion.
- **Shadow-intelligence background update:** `python -m scripts.intelligence_update` (runs each scheduler cycle; manual run also fine).

## Useful commands (all safe / read-only or shadow)
- Docs check: `python -m scripts.check_project_state_docs`
- Circuit breaker dry-run: `python -m scripts.circuit_breaker_dry_run`
- OHLCV coverage: `python -m scripts.archive_ohlcv_history --coverage-report`
- Path-aware replay: `python -m scripts.replay_profit_protection_path_aware`
- Backfill more history: `python -m scripts.backfill_ohlcv_history --timeframes 5m,15m --lookback-days 60 --limit 70`

## Definition of Done for Any Future Agent
After doing work you MUST:
1. Run focused tests for what you touched.
2. Run the full suite (`python -m pytest tests/ -q`) when touching core code.
3. Write a report under `reports/`.
4. **Update `../PROJECT_STATE.md`** (status, verdicts, next actions, Last Updated).
5. **Update `DECISION_LOG.md`** if a decision was made/changed.
6. Add/Update an ADR under `decisions/` for any architectural/strategic decision.
7. Keep live / trade-math **locked** unless the operator explicitly approved a change (record that approval in the DECISION_LOG).
8. Run `python -m scripts.check_project_state_docs` to confirm the doc layer is intact.
