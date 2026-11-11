# Operational Catalyst Integrity Scan — Deployment (PART 2)

**Date:** 2026-06-17 · **Verdict:** **CATALYST_INTEGRITY_SCAN_OPERATIONAL_READY**

## Scheduler wiring
`scripts/run_default_market_schedule.py` → `build_cycle_steps()` now appends `catalyst_integrity_step()` **immediately after** `catalyst_scan_step()` (verified: in the cycle plan, "catalyst integrity scan" follows "catalyst / narrative scan"). It runs `python -m scripts.catalyst_integrity_scan` as a **non-fatal** step, so a failure logs and the cycle continues.

## What it does each cycle
- Re-reads `news_items` (live) + the just-written `data/catalysts/<date>/{catalyst_events,narrative_baskets}.jsonl`.
- Writes `reports/CATALYST_INTEGRITY_DAILY_SUMMARY.md`.
- Prints a WARNING line when it finds: high-importance symbol-tagged news unmapped into events, a **no-catalyst basket symbol with a direct news hit** (the ASTER regression signature), or low mapping confidence.

## Behavior on findings
- Writes the daily summary + emits a warning line (Telegram-hook ready — can be routed to the existing system-warning channel; currently surfaced in the report + stdout).
- Does **not** promote any symbol to actionable; does **not** change score/tier. Catalyst-backed + overextended stays watch-on-pullback.

## ASTER artifact handling
- The scan runs **after** the fresh `catalyst-scan`, so each cycle re-generates `narrative_baskets.jsonl` with the fixed builder. If the regression signature **clears** after a fresh scan → the fix is working. If ASTER (or any symbol) **persists** in a no-catalyst basket after a fresh scan → that is a genuine regression and the warning fires (see `POST_CATALYST_SCAN_INTEGRITY_VERIFICATION.md`).

## Safety
- Read-only; no trade promotion; honest `unknown` when `news_items` is unavailable.

## Tests (PART 8 suite)
`tests/test_catalyst_integrity.py` (6): per-signal catalyst-backed/no-direct/unknown, daily counts, regression-signature warning, missing-news-table → unknown. ASTER-like case stays catalyst-backed (`tests/test_catalyst_aster_regression.py`).
