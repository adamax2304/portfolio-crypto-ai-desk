# Realistic Execution Dataset — Summary (PART 3)

**Date:** 2026-06-23. CSV: `data/research/realistic_execution_simulation_2026-06-23.csv` (builder: `scripts/realistic_pnl_sim.py`). Read-only.

## Build
- Source: `signal_outcomes` latest-row-per-signal, `entry_triggered=1`, joined to `proposed_signals`. Window: entered in last 60d (OHLCV path coverage 100% via the 60d backfill).
- Dedup → **economic trades** by `(symbol, direction, mode, tier, rounded-entry, entry-day)`, most-resolved row kept.
- **N = 1406** economic trades → **actionable 583** (A/B, non-scalp, non-stocks-swing/invest) · **shadow 823**.
- Note: **entered trades concentrate in the last ~30 days** (live tracking age) → the 60d and 30d aggregates are identical; 7d/48h/today are nested subsets.

## Per-trade columns
economic_trade_key, signal_id, book, symbol, asset_class, mode, tier, direction, playbook, market_regime, catalyst_supported, entry_at, stop_at, reached_tp1/2/3, hit_stop, expired, tp1_then_stop, tp2_then_stop, mfe_r, mae_r, **recorded_final_r**, and the 10 model R columns (`m0_legacy_touch`, `m1_first_tp_close`, `m2_hold_tp3`, `m3_tp1_be`, `m4_tp1_lock02`, `m5_partial_be`, `m6_partial_tp1_tp2`, `dC_lock05`, `dD_tp1_after_tp2`, `dG_playbook`), ambiguous flag.

## Reach counts (60d)
- **Actionable (583):** TP1 133 · TP2 78 · TP3 45 · stop 276 · expired 201.
- **Shadow (823):** TP1 116 · TP2 35 · TP3 7 · stop 287 · expired 435.

## Reliability
- `m0_legacy_touch` reconstructs the production number and matches recorded `final_r` to 99.8% (prior validation) → **reliable**.
- M1–M6 / dynamic absolute R are **RELATIVE-ONLY** (5m/15m OHLCV granularity, same-candle stop-first, and the baseline itself is optimistic). Use for ranking + overstatement magnitude, not exact PnL.

## Verdict
`REALISTIC_EXECUTION_DATASET_READY`
