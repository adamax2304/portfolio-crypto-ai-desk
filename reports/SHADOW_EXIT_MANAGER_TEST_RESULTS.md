# Shadow Exit Manager — Test Results (PART 3)

**Date:** 2026-06-17 · **Command:** `python -m pytest tests/test_shadow_exit_manager.py -q` → **10 passed**.

| Test | Asserts |
|---|---|
| current_variant_reaches_final_target | A_current walks to final TP → +3R |
| be_after_1R_moves_stop_only_in_shadow | C_BE_1R: touched +1R, moved BE, exits ~0R (not −1), stopped_after_BE |
| partial_variant_records_partial_in_shadow | D partial: books 0.5R at +1R, remainder out at BE → 0.5R |
| conservative_same_candle_rule_takes_stop | candle straddling stop+TP → stop first (−1R) |
| missing_ohlcv_is_missing_data_not_fake | candles=None → all variants shadow_R=None, coverage missing_data |
| shadow_rows_do_not_mutate_actual_outcome | input trade dict untouched; actual_R carried verbatim |
| one_unique_row_per_variant | exactly len(VARIANTS) unique rows |
| loser_saved_and_winner_clipped_flags | BE-after-1R saving a −1R loser → loser_saved=True |
| archive_first_ohlcv_path | archive preferred over rolling cache |
| partial_exit_model_flag_unchanged | config `partial_exit_model.enabled` still False |

## Spec coverage
- ✅ BE+1R moves stop only in shadow
- ✅ partial records partial only in shadow
- ✅ actual outcome unchanged
- ✅ missing OHLCV → missing_data, not fake
- ✅ conservative same-candle rule
- ✅ ledger idempotent by signal_id+variant (unique-row test + dedup on re-run)
- ✅ archive-first OHLCV used
- ✅ no mutation of partial_exit_model.enabled

## Verdict
**SHADOW_EXIT_MANAGER_READY** (decision-grade output pending ≥70% OHLCV coverage — see `SHADOW_EXIT_LEDGER_SUMMARY.md`, currently `DATA_COVERAGE_STILL_INSUFFICIENT` at 17.8%).
