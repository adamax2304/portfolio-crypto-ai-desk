# Scalp Entry Variant Backtest (PART 5)

**Date:** 2026-06-15 · Research-only. 12mo 5m, 15 symbols.

## What was directly simulated vs analysed

The engine ran the production entry (A) in full (139k trades) and split the results by **regime, session, direction, and symbol** — which directly answers the entry-gate variants that those splits represent. Pure momentum-confirmation variants (B/C/E/F) were not separately re-simulated; their verdict is derived from the fee-dominance mechanism the backtest established. This is stated transparently.

## Entry variants

| Variant | Simulated? | Result / reasoning |
|---|---|---|
| **A. current entry zone** | ✅ direct | net −0.466R/trade, PF 0.63 (baseline) |
| **B. enter on +0.3R momentum confirmation** | analysed | Entering later (after +0.3R) means a *worse* entry price and a *smaller* remaining move to TP, while the ~1.2R fee is unchanged → strictly raises the cost-to-edge ratio. Very unlikely to beat A. |
| **C. enter on +0.5R momentum confirmation** | analysed | Same as B, more extreme — chasing +0.5R before entry leaves little upside vs the fee. Worse. |
| **D. BTC/ETH alignment only** | ✅ via regime split | Regime split: downtrend −0.387R, uptrend −0.548R. "Aligned" (trend-following) subsets are **all still negative**. A regime/alignment gate does not rescue net R. |
| **E. volume-expansion only** | not simulated | No per-bar relative-volume stored in the 5m archive. Would reduce trade count; cannot change the per-trade fee math. Unlikely to flip net positive. |
| **F. reclaim / failed-reclaim confirmation** | not simulated | Adds a confirmation filter → fewer, possibly higher-quality entries, but each still pays ~1.2R fee on the tight ATR stop. Could improve WR but not clearly clear the cost hurdle. |
| **G. spread/liquidity threshold** | ✅ via symbol split | Symbol split IS a liquidity proxy: the most-liquid majors (BTC −1.85R, BNB −1.28R, ETH −0.81R) are the WORST because their ATR% is smallest → highest fee/risk. Higher-ATR mid-caps (NEAR −0.08, ARB −0.14) are near-breakeven but still negative. A liquidity gate that *prefers* higher-ATR names helps but does not reach positive. |
| **H. no scalp** | trivially | 0R, 0 fees. Strictly better than every actionable variant under current costs. |

## Key conclusion

**Entry is not the problem — the gross edge is positive (+0.73R/trade).** No entry gate tested (regime, session, direction, symbol/liquidity) produces a net-positive subset, because the binding constraint is the **per-trade fee (~1.2R) on the tight 5m ATR stop**, which entry timing cannot change. The only entry variant that avoids the loss is **H (no scalp / paper-only)**.

A genuinely different *instrument/cost* regime (maker-only fills, higher-ATR alts, wider stops) would be needed before any entry rework matters — that is a separate research track, not an entry-filter tweak.
