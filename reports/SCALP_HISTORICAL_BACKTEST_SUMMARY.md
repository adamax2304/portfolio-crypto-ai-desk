# Scalp Historical Backtest — Summary (PART 3)

**Date:** 2026-06-15 · Engine: `scripts/backtest_crypto_scalp_historical.py`. Data: 12mo 5m, 15 liquid symbols (1.55M candles). Full rows: `reports/SCALP_HISTORICAL_BACKTEST_RESULTS.csv`.

## Method (no-lookahead)

- Scan every 30 min (6×5m bars). Per scan, compute EMA20/EMA50/ATR14 at that bar only (precomputed arrays, no future data).
- Generate long if `close > EMA20 > EMA50` + within chase distance (|close−EMA20|/ATR ≤ 2); short if mirror.
- Apply production geometry: entry zone close∓[0.20,0.65]ATR, ATR/structure stop, TP1/2/3 at 1/2/3·ATR, 2h validity (24 bars).
- Entry fills only after signal bar; stop/TP only after entry; expiry/stale handled.
- Fees+slippage = 15 bps round-trip (production cost model). R = (exit−entry)/|entry−stop|; sized = raw × 0.5.
- A degenerate-risk guard floors stop at 0.30·ATR from entry (mirrors "no clean invalidation" rejection).

## Baseline (policy A = current production geometry)

| Metric | Value |
|---|---:|
| n trades | 139,014 |
| Wins / Losses / Expired | 59,277 / 79,737 / 1,665 |
| WR (closed) | **43%** |
| PF | **0.63** |
| **avg R / trade (incl. fees)** | **−0.466R** |
| Gross avg R (excl. fees) | **≈ +0.73R** |
| Total fees drag | −166,245R (≈ −1.2R/trade) |
| avg MFE | 2.43R · avg MAE −0.47R |
| Max drawdown | −64,853R (equity, raw, scan-frequency-inflated) |

## The decisive finding

**Scalp has a positive *gross* technical edge (~+0.73R/trade) that is destroyed by transaction costs (~−1.2R/trade), ending at −0.47R/trade net.**

Why fees dominate: the scalp risk distance is ~0.775·ATR. On liquid majors the 5m ATR is a tiny fraction of price, so 15 bps round-trip is large *relative to the stop distance* — each round-trip costs a big fraction of 1R. The geometry's far TP1 (~+1.84R) + 2h expiry means most trades don't reach TP to overcome that cost.

## Caveats on absolute magnitude

- Scan-every-30-min generates ~139k overlapping signals; production scans far less often, so **absolute R sums are inflated**. The scale-invariant metrics (**avg R/trade, WR, PF**) are the comparable figures and they are decisive: net-negative after fees.
- 5m granularity approximates 1m intrabar same-bar TP/stop adjudication.

Exit/entry variants, regime split, and walk-forward follow in the dedicated reports.
