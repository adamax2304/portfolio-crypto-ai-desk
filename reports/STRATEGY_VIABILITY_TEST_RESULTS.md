# Strategy Viability — Tests & Validation (PART 10)

**Date:** 2026-06-23.

## Tests
- `tests/test_realistic_pnl_models.py` — **7 tests pass**, incl. new `test_model_f_mfe_protection`:
  - stopped but MFE≥0.6R → BE rescue = 0R; stopped MFE≥1R → +0.5R lock; stopped MFE<0.6R → −1R; TP3 → keep best-TP; clean win → keeps booked R.
  - plus the existing TP1→stop / TP2→stop / stop-first / expired / give-back invariants.
- Full sweep `test_realistic_pnl_models + test_display_status + test_default_market_schedule + test_project_state_docs` → **59 passed**.

## Replay / cohort-filter validation
- **Dedup consistency:** economic-trade keys unique; 1407 trades; reproduced via `scripts/strategy_viability.py` importing `compute_models`/`model_f_mfe` (single source of truth shared with PART-2 sim).
- **No mutation of historical outcomes:** simulation reads `signal_outcomes` only; `m0_legacy_touch` reproduces recorded `final_r` (99.8%, prior validation) → read path faithful and untouched.
- **Robustness checks run:** PF 1.43; avg +0.127R/trade; not single-symbol dependent (−SMCI → +60.6R; −top3 → +44.7R); two-window split both positive (+17.6 / +56.5R).

## Safety
- **No production logic changed.** Only new files: `scripts/strategy_viability.py`, `model_f_mfe` added to `scripts/realistic_pnl_sim.py`, `tests/test_realistic_pnl_models.py` (extended), `data/research/strategy_viability_dataset_2026-06-23.csv`, `reports/*`. Tracker/scoring/routing/filters/validity/configs untouched.
- **Scheduler dry-run guard** → `LLM-auto-invoke check OK (no Opus/Claude tokens in plan)`.
- **Docs validator** → `PROJECT STATE DOCS: OK`.
- Same-candle ambiguity (3 trades) flagged; Model F's MFE-trigger reliability noted as relative-leaning (granularity).

## Verdict
`STRATEGY_VIABILITY_TESTS_PASS`
