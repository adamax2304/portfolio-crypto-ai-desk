# MAKER-FIRST PAPER EXECUTION — IMPLEMENTATION REPORT (PART 4)

**Scope:** PAPER ONLY. No live orders. Date: 2026-06-24.

## Module
`src/execution/maker_first_execution.py → plan_for(...)` → `ExecutionPlan`:
`plan, entry_order_type, exit_order_type, tp_order_type, stop_order_type,
expired_close_type, maker_fill_status, maker_entry_missed, maker_tp_filled,
taker_fallback_used, maker_first_reason`.

Default active plan: **MAKER_WHEN_SAFE_TAKER_WHEN_URGENT** (all 6 plans enumerated).

## Rules (conservative — no free maker fills)
1. **Stops are always taker/marketable** (safety).
2. **Entry**: maker limit for pullback/retest/bounce setups; **taker for
   breakout/momentum/urgent**. If the maker limit isn't touched again within the
   timeout (`maker_entry_touched_again=False`) → `maker_entry_missed` → taker fallback
   (if allowed).
3. **TP exits**: maker/post-only preferred; counts as a maker fill **only if the level
   was rested before/at the touch** (`tp_level_rested_before_touch`). Gaps through →
   no free maker.
4. **Expired**: maker close if non-urgent, taker if invalid/stale.

## Config `paper_maker_first`
`enabled: true · apply_to_paper: true · default_plan:
maker_when_safe_taker_when_urgent · entry_timeout_candles: 2 · allow_taker_fallback:
true · stop_order_type: taker · tp_order_type_preference: maker ·
expired_close_preference: maker_if_non_urgent · conservative_fill_model: true`.

## Backfill effect ($5000 book, Bybit profile)
- **177 maker entries** filled (pullback/bounce cohorts), 0 missed under the
  conservative fill model, **299 maker TP exits**.
- Fees fell **$1763 → $1585 (−$177.7)**, lifting Bybit return **+3.72% → +8.19%**
  (+4.47pp). Maker rate on Bybit perp is 0.02% vs 0.055% taker — a 2.75× fee cut on
  every maker side.

## Tests
`tests/test_structural_maker.py`: maker entry for pullback / taker for momentum, stop
always taker, maker-entry-missed→taker fallback, maker-TP fill only if rested. Pass.

## Verdict
**MAKER_FIRST_EXECUTION_ACTIVE_FOR_PAPER**
