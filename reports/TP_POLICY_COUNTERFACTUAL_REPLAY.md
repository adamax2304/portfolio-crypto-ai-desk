# TP Policy Counterfactual Replay (PART 5)

**Date:** 2026-06-23. Path-aware replay from recorded TP/stop timestamps. N=1404 (actionable 582). **No production change.**

## Framing (read first)
The production tracker books **the R of the highest TP the price touched** (optimistic; stop never moves). So a TP-count change can only **clip recorded winners** — it can never turn a recorded winner into a loss. The realistic "give-back" effect appears only under a **hold-to-single-target** model. Both views are shown; absolute R is **not reliable** (granularity + same-candle), use **relative ranking**.

## Variants — ACTIONABLE book (n=582), net R
| Variant | net R | Δ vs baseline | winners clipped | losers avoided |
|---|---|---|---|---|
| **BASELINE (current, best-TP)** | **+5.0** | — | — | — |
| **A — 2TP default (remove TP3)** | −40.0 | **−45.0** | 45 TP3 trades clipped to TP2 | 0 |
| B — TP3 only trend-runner¹ | ≈ +5.0 | ≈ 0 to −2 | few | 0 |
| C — no TP3 in chop/mixed | ≈ +4 | −1 | 1 (chop TP3=1) | 0 |
| D — no TP3 counter-regime (risk-off longs / risk-on shorts max TP2) | ≈ +3 | −2 | 2–3 | 0 |
| E — no TP3 late-entry / short window | ≈ +4 | −1 | 1–2 | 0 |
| F — playbook-specific (TP3 only where add-R>0) | **≈ +5.0** | ≈ 0 | 0 | 0 |

¹ Variant B keeps TP3 exactly for the cohorts that actually reach it (crypto swing, failed-bounce-short, intraday catalyst, trend/risk-off shorts) — which is where ~all 45 actionable TP3 hits already occur — so it reproduces baseline. It does **not** add R; it would only *reduce churn/clarity*, not improve R.

**Result:** every TP-count restriction is **≤ baseline** (A is −45R; B–F ≈ 0). **No TP-count variant improves net R.** Mechanism: TP3 is reached rarely (7.7% actionable) but is pure realized upside when it is; restricting it removes that upside and avoids no losses (losers never reached TP3).

## Per-mode Δ (Variant A, remove TP3)
- crypto swing: +22.8 → +2.8 (**−20R**, worst clip — swing is the TP3 engine).
- crypto intraday: −33.8 → −49.8 (−16R).
- stocks intraday: +16 → +7 (−9R).

## PF / WR / duration / drawdown
On the actionable book WR(resolved, win=TP-any)/loss is ~30–35% with PF≈1.0 (≈breakeven) under baseline; removing TP3 lowers gross-win R without lowering gross-loss R → PF falls below 1. Average trade duration and a max-drawdown proxy are dominated by the 35–47% expired/stop rate, unchanged by TP-count. (Full per-trade fields in the CSV.)

## False positives/negatives
- "False negative" of removing TP3 = the 45 actionable trades that DID reach TP3 and would be clipped (e.g. crypto swing narrative names). Concrete, recurring.
- "False positive" saved by removing TP3 = **none** (no trade that reached TP3 later became a loss in the recorded data).

## Verdict
`TP_POLICY_REPLAY_COMPLETE` — no TP-count variant beats current; removing TP3 is net-negative.
