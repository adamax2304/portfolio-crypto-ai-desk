# Realistic Execution Accounting — Tests & Validation (PART 9)

**Date:** 2026-06-23.

## Model unit tests — `tests/test_realistic_pnl_models.py` (6 tests, all pass)
| scenario | asserted |
|---|---|
| **TP1 then stop** | legacy=+1.0 · first-TP=+1.0 · hold-TP3=**−1.0** · TP1-BE=**0.0** · +0.2lock=0.2 · partial50+BE=**0.5** · +0.5lock=0.5 |
| **TP2 then stop** | legacy=+2.0 · hold-TP3=**−1.0** · stop→TP1-after-TP2=**+1.0** · partial 1/3·1/3·runner=(1+2+0)/3 |
| **TP3 hit** | all runner models capture TP3 (legacy/hold/BE=3.0; partial50=0.5·1+0.5·3; thirds=(1+2+3)/3) |
| **stop first (no TP)** | all models = −1.0 |
| **no TP / no stop** | all models = 0.0 (expired) |
| **give-back invariant** | partial & BE > hold-TP3 on a TP1-then-stop |

These lock exactly the behaviors the audit hinges on (esp. "TP1→stop is +1 under legacy but −1 / 0 / +0.5 under realistic models").

## Regression / safety sweep
- `pytest test_realistic_pnl_models + test_display_status + test_default_market_schedule + test_project_state_docs` → **58 passed**.
- **No mutation of `signal_outcomes.final_r`**: the simulation only reads; `m0_legacy_touch` reproduces recorded `final_r` to 99.8% (validation), proving the read path is faithful and untouched.
- **No production logic changed**: only new files added — `scripts/realistic_pnl_sim.py`, `tests/test_realistic_pnl_models.py`, `data/research/realistic_execution_simulation_2026-06-23.csv`, `reports/*`. `tracker.py`, scoring, routing, filters, validity, configs — untouched.
- **Scheduler dry-run guard** → `LLM-auto-invoke check OK (no Opus/Claude tokens in plan)` (no live/exec step).
- **Docs validator** → `PROJECT STATE DOCS: OK`.
- **Same-candle** handled stop-first (conservative), inherited from production; 3 ambiguous trades flagged.

## Verdict
`REALISTIC_EXECUTION_TESTS_PASS`
