# Risk-Management Framework Candidates (PART 3)

**Date:** 2026-06-23. Design only. R-formulas implemented in `scripts/realistic_pnl_sim.py` (`compute_models`, `model_f_mfe`). None enabled in production. Stop "arms" mean a real-time trigger (price reaches a level), not hindsight.

| Model | Rule | Stop movement | Partials | Runner | R formula (from recorded path) |
|---|---|---|---|---|---|
| **A — Conservative first-profit** | close 100% at TP1 | none | none | none | `R1 if TP1 else (−1 if stop else 0)` |
| **B — TP1 + BE runner** | 50% off at TP1, stop→BE on rest | BE after TP1 | 50% | to TP2/TP3 | `0.5·R1 + 0.5·(R3 if TP3 else 0)` |
| **C — TP1 + profit-lock runner** | after TP1, lock +0.2/+0.5R | +0.2 / +0.5R after TP1 | optional | to TP2/TP3 | `R3 if TP3 else (lock if TP1&reverse else −1/0)` |
| **D — Playbook-specific** | runner for crypto swing / failed-bounce-short / catalyst; earlier close for stocks-momentum / chop / counter-regime; scalp & C-tier shadow | per-playbook | per-playbook | conditional | `hold_tp3` for runner cohorts else `tp1_be` |
| **E — Regime-specific** | trend-aligned → runner; chop/mixed → TP1/TP2 max + lock; risk-off longs → fast exit; risk-off shorts → runner if trend confirmed | per-regime | — | conditional | regime-routed combination of A/C |
| **F — MFE-adaptive protection** ★ | **stop→BE once +0.6R favorable; lock +0.5R once +1R favorable; let TP3 run** | **armed at favorable excursion (BEFORE TP1)** | none | yes | `TP3→best; MFE≥1 & reverse→+0.5; MFE≥0.6 & reverse→0; else −1/0` |
| **G — Time-decay** | if not +0.5R within X candles → close stale; if +0.8R then stalls → take profit | none | — | — | (approximated by expiry handling; reduces near-winner expiries) |
| **H — Hybrid** | F (MFE protection) **+** cohort filter (shadow `crypto_intraday_catalyst`, keep failed-bounce-short/swing/stocks-intraday) **+** TP3 only for TP3-positive cohorts | as F | none | TP3-positive cohorts only | F applied to the filtered universe |

★ **Model F is the key candidate.** It differs from B/C in *when* protection arms: B/C only arm after TP1 (≈1R away, reached by 22.8%), whereas F arms at +0.6R favorable (reached by 54%) — capturing the large band of trades that pop then reverse before TP1. This is exactly the gap diagnosed in PART 2.

**What is NOT allowed in any candidate:** changing entries/scoring/routing/TP-SL in production, enabling BE/partial/trailing in production, live/auto-live execution, force-close, rewriting historical outcomes. All candidates are replay/paper-shadow only.

## Verdict
`RISK_FRAMEWORK_CANDIDATES_DEFINED`
