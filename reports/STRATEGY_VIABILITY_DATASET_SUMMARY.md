# Strategy Viability Dataset — Summary (PART 1)

**Date:** 2026-06-23. Read-only. CSV: `data/research/strategy_viability_dataset_2026-06-23.csv` (builder `scripts/strategy_viability.py`). No production change.

## Build
- Source: `signal_outcomes` latest-row-per-signal, `entry_triggered=1`, joined to `proposed_signals`; **all available tracked history**.
- **Full entered history range: 2026-05-25 → 2026-06-23 (~30 days)** — the live signal tracker is ~30d old, so "all history" ≈ "30d". 60d/30d windows are identical; 7d/48h/today are nested subsets; persistent-monitor-restart (2026-06-18) is a recent slice.
- Economic-trade dedup `(symbol, direction, mode, tier, rounded-entry, entry-day)`; latest/terminal outcome; no raw row duplication.
- **N = 1407** economic trades → **actionable 584** (A/B, non-scalp, non-stocks-swing/invest) · **shadow 823**.
- **MFE/MAE coverage = 100%** (`max_favorable/adverse_excursion_r` populated for all 1610 underlying rows), as R-multiples. Path coverage 100% (60d OHLCV backfill).

## Per-trade fields (CSV)
economic key, book, symbol, asset_class, mode, tier, direction, playbook, regime, catalyst, entry_at, reached_tp1/2/3, hit_stop, expired, **mfe_r, mae_r**, mfe_ge_05/1/2/3, never_positive, stop_first, giveback_mfe1, recorded_final_r, and 11 execution-model R columns (`m0_legacy_touch`, `m1_first_tp_close`, `m2_hold_tp3`, `m3_tp1_be`, `m4_tp1_lock02`, `m5_partial_be`, `m6_partial_tp1_tp2`, `dC_lock05`, `dD_tp1_after_tp2`, **`mF_mfe_protect`**).

## Books
- **Operator/Paper (actionable):** 584 — the cohort any viability decision affects.
- **Shadow:** 823 (C-tier / crypto-scalp / stocks-swing-invest) — reported separately, stays shadow.
- Research = the whole derived set.

## Reliability
- `m0_legacy_touch` reproduces recorded `final_r` (validated 99.8% in the prior audit) → reliable.
- Realistic models (incl. Model F) are **RELATIVE-LEANING**: 5m/15m granularity + same-candle ordering + 30-day single epoch. Use for ranking and magnitude, confirm with forward paper.

## Verdict
`STRATEGY_VIABILITY_DATASET_READY`
