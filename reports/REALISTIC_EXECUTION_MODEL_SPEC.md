# Realistic Execution Model Spec (PART 2)

**Date:** 2026-06-23. Models implemented in `scripts/realistic_pnl_sim.py::compute_models` (pure, tested). All reconstruct R from the **recorded** TP/stop touch order; same-candle = stop-first conservative. R-multiple of level k = (level−entry)/|entry−stop| (sign-flipped for shorts). `c1/c2/c3`=TP touched, `st`=stop, `exp`=expired-without-resolution.

| Model | Definition | Formula (R) |
|---|---|---|
| **M0 LEGACY_TOUCH** (baseline = current tracker) | R of highest TP touched | `R3 if c3 else R2 if c2 else R1 if c1 else (−1 if st else 0)` |
| **M1 FIRST_TP_FULL_CLOSE** | exit 100% at TP1 when touched; TP2/3 irrelevant after | `R1 if c1 else (−1 if st else 0)` |
| **M2 HOLD_TO_TP3_FIXED_STOP** | hold for TP3, stop never moves → TP1/2 touch then stop = **−1R** | `R3 if c3 else (−1 if st else 0)` |
| **M3 TP1_THEN_BE** | TP1 touched → stop to entry; later stop = **0R**; TP3 still credited | `R3 if c3 else (0 if c1&(st\|exp) else (−1 if st else 0))` |
| **M4 TP1_THEN_PROFIT_LOCK(+0.2R)** | TP1 → stop to +0.2R | `R3 if c3 else (0.2 if c1&(st\|exp) else (−1 if st else 0))` |
| **M5 PARTIAL_TP1_BE_RUNNER** | 50% off at TP1, runner stop→BE, runner to TP3 | `0.5·R1 + 0.5·(R3 if c3 else 0)` if c1 else (−1 if st else 0) |
| **M6 PARTIAL_TP1_TP2_RUNNER** | 1/3 at TP1, 1/3 at TP2, 1/3 runner to TP3 (BE after TP1) | `(R1 + (R2 if c2 else 0) + (R3 if c3 else 0))/3` if c1 else (−1 if st else 0) |

**Dynamic-stop extras (PART 6):** dC = +0.5R lock after TP1; dD = stop→TP1-level after TP2 (`R3 if c3 else R1 if c2&(st\|exp) else −1 if st else 0`); dG = playbook-specific (M2 runner for crypto swing / failed-bounce-short / intraday-catalyst, else M3).

Per-trade outputs in the CSV: model_name R, close_reason (derived: tp3/tp2/tp1/be/lock/partial/stop/expired), first_event, first/highest TP touched, `stop_after_tp_hit`, `giveback_flag` (tp1/2_then_stop), `stop_moved`, `partial_taken`, `same_candle_ambiguous`, `reliability_flag` (legacy_touch=reliable; hold/BE/partial=relative-only).

## Verdict
`EXECUTION_MODELS_DEFINED`
