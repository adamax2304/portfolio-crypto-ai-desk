# Risk-Management Historical Replay Results (PART 4)

**Date:** 2026-06-23. All-history (~30d) replay of every model. Net R; **relative-leaning** absolute values (granularity + single epoch). No production change.

## Net R by model & book
| model | ALL (1407) | **ACTIONABLE (584)** | SHADOW (823) |
|---|---|---|---|
| recorded `final_r` (touch) | −114.0 | **+2.0** | −116.0 |
| m0 legacy touch | −119.3 | +6.2 | −125.5 |
| A first-TP full close | −260.6 | −104.8 | −155.8 |
| hold-to-TP3 | −405.1 | −136.8 | −268.3 |
| B/C TP1→BE | −361* | −109.8 | −253* |
| C +0.5R lock (after TP1) | −342.1 | −96.3 | −245.8 |
| B partial50 + BE runner | −311.9 | −107.3 | −204.6 |
| **F — MFE-armed protection** | **−7.2** | **+74.1** | −81.3 |

\* B/C-after-TP1 ≈ prior audit figures. **Model F dominates by a wide margin** on every book and is the only model that makes the actionable book solidly positive.

## Model F detail (ACTIONABLE, 584)
- **Total +74.1R · avg +0.127R/trade · PF 1.43 · win 28.3% / loss 29.6% / BE-scratch 42.1%.**
- Mechanism: **42% of trades exit at BE (0R)** instead of −1R — these are the +0.6R-favorable-then-reversed trades. 103 stopped trades (17.6%) reached ≥0.6R first and are rescued.
- vs first-TP-close: **+179R swing** (−104.8 → +74.1). vs hold-to-TP3: +211R.

## Model F by cohort (actionable)
| playbook | n | first-TP | +0.5lock | **Model F** | R/trade | MFE≥1R |
|---|---|---|---|---|---|---|
| crypto_failed_bounce_short | 31 | −1.6 | +13.3 | **+19.2** | +0.62 | 41.9% |
| crypto_swing_narrative_rs | 89 | −25.2 | −2.3 | **+29.2** | +0.33 | 42.7% |
| stocks_intraday_rth_momentum | 364 | −17.0 | −64.5 | **+23.7** | +0.07 | 23.6% |
| crypto_intraday_catalyst_or_momentum | 100 | −61.0 | −42.8 | +2.1 | +0.02 | 28.0% |

## By regime (Model F, actionable)
bearish-trend +12.0 (n11) · bullish-trend +20.9 (n75) · bullish +14.3 (n291) · risk_off +10.7 (n30) · unknown +8.8 (n120) · range/chop +3.4 (n9). **All regimes positive under F.**

## By direction (best realistic)
| dir | n | first-TP | +0.5lock | **Model F** | recorded |
|---|---|---|---|---|---|
| short | 66 | +0.4 | +5.0 | **+26.9** | +21.0 |
| long | 518 | −105.2 | −101.3 | **+47.3** | −19.0 |
Longs are the −105R disaster under fixed-stop models, but Model F flips them to **+47R** (early protection saves the bullish-tape give-back longs).

## Comparison vs reference exits (actionable)
legacy touch +6.2 · first-TP −104.8 · hold-TP3 −136.8 · TP1-BE −109.8 · +0.5lock −96.3 · partial −107.3 · **Model F +74.1**. The reference exits (all armed at/after TP1) confirm the prior audit's "dynamic stop doesn't make it profitable" — **but that was because they arm too late.** Model F arms at favorable excursion and is the outlier.

## Verdict
`RISK_MANAGEMENT_REPLAY_COMPLETE` — Model F (MFE-armed early protection) is the dominant model; flips the actionable book to +74.1R / PF 1.43.
