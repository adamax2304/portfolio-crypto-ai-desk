# TP1→Stop Give-Back Case Study (PART 5)

**Date:** 2026-06-23. Actionable book, 60d. The trades where current accounting and reality diverge most.

## The give-back set
**27 actionable trades** touched TP1 (8 of them also TP2) and **then hit the stop** before TP3/expiry. Current model records all 27 as **wins** (+TP1/+TP2).

| metric on the 27 give-back trades | R |
|---|---|
| **M0 legacy touch (what current books)** | **+37.5** |
| M2 hold-to-TP3 fixed stop (rode it, gave it all back) | **−27.0** |
| M3 TP1→BE | 0.0 |
| M4 +0.2R lock | +5.4 |
| dC +0.5R lock | +13.5 |
| M5 partial50 + BE runner | +15.1 |
| **R *saved* by BE vs naive hold** | **+27.0** |
| **R *not captured* by BE vs legacy** | **−37.5** |

So these 27 trades are **the entire overstatement engine**: the touch model claims +37.5R; a realistic stop-managed exit yields **0 to +15R**; a naive hold yields **−27R**. The honest range for these is roughly **0…+15R, not +37.5R**.

## Where give-backs cluster
- **Mode:** crypto swing 14 · stocks intraday 11 · crypto intraday 2.
- **Playbook:** `crypto_swing_narrative_rs_momentum` 13 · `stocks_intraday_rth_momentum` 11 · crypto intraday catalyst 2 · failed-bounce-short 1.
- **Regime:** bullish / bullish-trend 20 of 27 (longs in an up-tape that pulled back through the stop after a first pop).
- **Symbols (recurring):** SMH ×6, WLD/USDT ×2, TAO/USDT ×2, AAPL ×2, plus ETH, ATOM, AVGO, FIL.

## Reading
- The pattern is mostly **long pops to TP1 in a bullish tape that then retrace to the original stop** — exactly the scenario where a **BE/partial after TP1 helps** (turns −1R-or-give-back into 0…+0.75R) but where the touch model pretends you banked the full TP.
- Dynamic stop here **saves +27R vs naive hold** and **partial books +15R** — meaningful relative to the 27-trade subset, but it does **not** recover the +37.5R the touch model imagined, and it does not make the overall book positive (the rest of the book is dominated by 276 stops).
- 8 of the 27 reached TP2 before reversing → `dD` (stop→TP1 after TP2) would lock +1R on those.

## Verdict
`TP1_GIVEBACK_CASES_ANALYZED` — 27 trades, +37.5R of recorded "profit" that realistic execution turns into 0…+15R; concentrated in bullish-tape long pops (crypto swing + stocks intraday momentum, esp. SMH).
