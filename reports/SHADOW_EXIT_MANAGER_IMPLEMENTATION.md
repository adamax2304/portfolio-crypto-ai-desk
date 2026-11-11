# Shadow Exit Manager — Implementation (PART 3)

**Date:** 2026-06-17 · **Verdict:** **SHADOW_EXIT_MANAGER_READY** (working; decision-grade pending coverage).
**Shadow measurement ONLY. Real exits unchanged. `partial_exit_model.enabled` stays false. Actual outcomes never mutated.**

## What was built
- **`src/exits/shadow_exit_manager.py`** — candle-by-candle alternative-exit simulator + ledger row builder.
  - Variants A–I: A current, B BE@+0.5R, C BE@+1R, D partial-50%@+1R, E partial-50%@+1R+BE, F trail-after-+1R, G candle-close stop, H no-reentry, I one-reentry.
  - **Conservative same-candle rule:** if stop and a target touch the same candle, the stop is taken first.
  - **Archive-first OHLCV** (`data/archive/ohlcv` → rolling cache), respecting path order.
  - Per-row flags: touched_0.5R/1R, moved_to_BE, partial_taken, stopped_after_BE, winner_clipped, loser_saved.
- **`scripts/shadow_exit_ledger_update.py`** — read-only over the DB; for each closed crypto intraday/swing trade computes all variants and **append-merges** into `data/reports/shadow_exit_ledger.csv`, **idempotent by (signal_id, variant)**. `--limit`, `--dry-run`.
- **`scripts/shadow_exit_summary.py`** — net R / PF / winrate / winners-clipped / losers-saved per variant + recommendation, → `reports/SHADOW_EXIT_LEDGER_SUMMARY.md`.

## Coverage honesty (important)
A trade is `covered` **only if** the OHLCV window spans the full entry→exit; a truncated window is `partial_data`; no OHLCV is `missing_data` (shadow_R=None, never faked). The summary's net-R stats count **only `covered`** rows. First full run: 146 trades, **26 covered (17.8%)** → summary verdict **DATA_COVERAGE_STILL_INSUFFICIENT** (honest; lifts as the backfill/archive grows).

## Ledger schema (one row per trade × variant)
signal_id, symbol, asset_class, mode, tier, direction, entry_time, exit_time, entry, stop, tp, actual_R, variant, shadow_R, exit_reason, touched_0_5R, touched_1R, moved_to_BE, partial_taken_time, stopped_after_BE, winner_clipped, loser_saved, data_timeframe_used, data_coverage_status.

## Safety (asserted by tests)
- BE/partial move the stop / book a partial **only in shadow**; actual outcome untouched.
- Missing OHLCV → `missing_data`, not a fake result.
- Conservative same-candle rule verified.
- Ledger idempotent (one unique row per signal_id×variant; dedup on re-run).
- Archive-first OHLCV verified.
- `partial_exit_model.enabled` remains false (asserted).

See `SHADOW_EXIT_MANAGER_TEST_RESULTS.md` + `SHADOW_EXIT_LEDGER_SUMMARY.md`.
