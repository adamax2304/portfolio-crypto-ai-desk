# FEE-AWARE PAPER EXECUTION — IMPLEMENTATION REPORT (PART 3)

**Scope:** PAPER ONLY. Does not affect production. Date: 2026-06-24.

## Module
`src/execution/fee_aware_execution.py → assess_fees(...)` → `FeeAware` dataclass:
`fee_profile, fee_r_cost, break_even_move_pct, min_viable_tp1_r,
fee_drag_pct_of_gross, expected_net_edge_r, fee_survival_label, action, reasons`.

`fee_r_cost = round-trip cost / risk_usdt` (cost from `trade_costs`, which now charges
the close fee on **exit notional** — the prior bugfix).

## Labels & thresholds
- `fee_r_cost > 0.20R` → **HIGH_FEE_DRAG**
- `fee_r_cost > 0.35R` (`max_fee_r_cost`) → **EXTREME_FEE_DRAG**
- `tp1_r ≤ fee_r_cost + 0.30R` → **TP1_NOT_WORTH_FEES**
- tight stop (<0.35%) + `fee_r_cost > 0.20` → **TIGHT_STOP_FEE_DRAG**
- `expected_net_edge_r ≤ 0` → **FEE_SURVIVAL_FAIL**
- viable on MEXC but not Bybit → **EXCHANGE_SENSITIVE** (diagnostic)

## Paper behaviour (config `paper_fee_aware_execution`)
`enabled: true · apply_to_paper: true · default_action: warn_and_cap ·
skip_fail_fee_survival: false · skip_extreme_fee_drag: true · max_fee_r_cost: 0.35`.
- EXTREME_FEE_DRAG / TIGHT_STOP_FEE_DRAG → `action = paper_skipped_fee_drag`
  (dropped from the paper book).
- Other non-OK labels → `warn_and_cap` (kept, annotated).
- Production is untouched.

## Backfill effect
On the $5000 historical book, the fee-aware gate skipped **2 conservative-profile
trades** (EXTREME_FEE_DRAG) and **0 on Bybit** — confirming the corrected, 2x-sized
notionals rarely blow past 0.35R on Bybit but can on the punitive conservative
profile. Combined with maker-first the fee drag fell materially (see PART 8).

## Tests
`tests/test_structural_maker.py`: fee_r_cost computed, EXTREME→skip, FEE_SURVIVAL_FAIL
on negative net edge, maker rate < taker rate. All pass.

## Verdict
**FEE_AWARE_EXECUTION_ACTIVE_FOR_PAPER**
