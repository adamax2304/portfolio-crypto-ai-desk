# Cohort-Filter × Risk-Model Search (PART 5)

**Date:** 2026-06-23. Actionable universe, ~30d. Does filtering + risk make it viable? **Relative-leaning; needs forward validation.**

## Step 1 — cohort expectancy ranking (best realistic model = Model F unless noted)
**Playbook (R/trade under best realistic):** crypto_failed_bounce_short +0.62 · crypto_swing_narrative +0.33 · stocks_intraday_momentum +0.07 · crypto_intraday_catalyst +0.02 (weakest).
**Direction:** short +0.41 · long +0.09 (long only positive *with* Model F).
**Catalyst:** catalyst-yes +0.06 · catalyst-no −0.18 under first-TP, but both positive under Model F.
**Regime:** bearish-trend & risk_off shorts strongest per-trade; chop weakest.
Under the **fixed-stop / after-TP1** family, the only positively-expectant cohort is `crypto_failed_bounce_short`. **Under Model F, almost all cohorts turn positive** — the differentiator is the risk model, not the cohort.

## Step 2 — candidate portfolios (net R by model)
| portfolio | n | first-TP | hold-TP3 | +0.5lock | partial | **Model F (best)** |
|---|---|---|---|---|---|---|
| A all-actionable | 584 | −104.8 | −136.8 | −96.3 | −107.3 | **+74.1** |
| B positive-realistic-cohorts (failed-bounce-short only, fixed-stop sense) | 31 | −1.6 | +11.8 | +13.3 | +5.6 | +19.2 |
| D crypto-only | 220 | −87.8 | −55.8 | −31.8 | −63.8 | (Model F ≈ +50) |
| E stocks-only | 364 | **−17.0** | −81.0 | −64.5 | −43.5 | **+23.7** |
| F catalyst-only | 55 | −10.4 | −7.0 | +3.5 | −5.2 | (positive) |
| G trend-aligned | 377 | −35.6 | −76.3 | −46.3 | −46.0 | (positive) |
| H risk-off-shorts | 41 | +6.0 | +5.7 | +5.7 | +5.8 | +6+ |
| I no-chop | 560 | −100.2 | −132.2 | −93.2 | −103.2 | ≈ +72 |
| **K hybrid (Model F + drop crypto_intraday_catalyst)** | **484** | — | — | — | — | **+72.1 (avg +0.149/trade)** |

## Robustness of the best combo (Model F on actionable / hybrid K)
- **PF 1.43**, avg +0.127R/trade (hybrid +0.149).
- **No single-symbol dependency:** top symbol SMCI +13.5R; remove it → still **+60.6R**; remove top-3 → **+44.7R**. No symbol >18% of profit.
- **Two-window stability (split at 2026-06-04):** window1 +17.6R · window2 +56.5R — **both positive** (but same 30d epoch, not independent regimes).
- **Overfit risk:** MODERATE-HIGH — 30 days, one market epoch (bullish/chop), MFE-trigger reconstruction, costs not modeled. Not a multi-regime out-of-sample result.

## Reading
- The biggest lever is **the risk model (Model F), applied broadly** — not aggressive cohort pruning. Filtering only `crypto_intraday_catalyst` (the weakest) is enough; deeper pruning shrinks n without improving per-trade much.
- The **cleanest standalone cohorts** (work even under simple fixed-stop exits) are **crypto_failed_bounce_short and risk-off shorts** — these are the safest "viable core" if one wants a tiny, high-confidence book before trusting Model F broadly.

## Verdict
`BEST_COHORT_RISK_COMBO_SEARCH_COMPLETE` — best = **Model F on actionable, drop crypto_intraday_catalyst** (n=484, +72R, PF~1.4, no symbol dependency); safest tiny core = failed-bounce-short + risk-off shorts.
