# Intraday Risk-Off Label — 30d Measurement (PART 6)

**Date:** 2026-06-17 · **Source:** BTC binance 1d OHLCV, last 30 days. **Diagnostic only.**

## Base rate
| Metric | Value |
|---|---|
| Days in window | 30 |
| Risk-off days (BTC day ≤ −0.75%) | **11 (36.7%)** |
| Mean daily change | −0.54% |
| Range | −6.51% … +4.02% |

Recent 8 days: 06-10 −0.35, 06-11 +3.44, 06-12 −0.07, 06-13 +1.38, 06-14 +2.00, 06-15 +0.89, **06-16 −0.99 RISK_OFF**, **06-17 −0.96 RISK_OFF**.

## What this means for acting on the label
- Risk-off fires on **~37% of days** — a high base rate. A hard long-throttle on that many days would skip a large share of trading, including winners.
- From the prior 7d throttle diagnostic: crypto longs on risk-off days netted only **−1.0R combined** (26 losers ≈ offset by 16 winners). So the **expected R saved from throttling is small** while the opportunity cost (skipped winners) is real.
- Conclusion: the label is **useful for visibility/context** (operator + Opus can see "long into red BTC"), but the data does **not** justify an automated throttle/half-size yet.

## Recommendation
- Ship the **label only** (done). Re-measure over a longer window that includes a sharper sustained downtrend (e.g. a −5%+ stretch like 02-05) — the loss-vs-winner asymmetry may grow there and change the calculus.
- Verdict for acting: **RISK_OFF_LABEL_NEEDS_MORE_DATA** before any throttle. The label itself is **READY** as a visibility field.

## Limitation
Day-change is a coarse proxy; intraday rollover within a green-close day isn't captured by a daily metric. The `btc_1h_trend`/`btc_4h_trend` fields add finer context but were not back-measured over 30d here (the 1h store covers only ~9d).
