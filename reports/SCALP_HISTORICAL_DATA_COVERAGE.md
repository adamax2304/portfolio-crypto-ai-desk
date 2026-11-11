# Scalp Historical Data Coverage (PART 2)

**Date:** 2026-06-15 · Append-only archive: `db/scalp_history.sqlite` (separate from production DB).

## Download

- Source: Binance spot via ccxt 4.5.49 (public klines; no API key).
- Storage: SQLite `ohlcv(exchange, symbol, timeframe, ts, OHLCV)` with PRIMARY KEY dedup on (exchange, symbol, timeframe, ts) — append-only, resumable.
- Connectivity verified: Binance + Bybit both serve 1m candles back to ~370 days.

## 5-minute coverage (primary scalp timeframe) — 12 months

| Metric | Value |
|---|---:|
| Symbols | 15 (BTC, ETH, SOL, BNB, XRP, DOGE, ADA, AVAX, LINK, TON, NEAR, APT, ARB, OP, SUI) |
| Window | 2025-06-20 → 2026-06-15 (**12.0 months**) |
| Candles / symbol | ~103,685 (12mo of 5m ≈ 105,120 → ~98.6% coverage) |
| Total 5m candles | **1,555,275** |

All 15 symbols have near-complete coverage (103,681–103,688 each). Missing-candle rate < 1.5% (exchange downtime / maintenance gaps).

## Universe selection

- High-liquidity Binance USDT pairs only → minimal spread/slippage ambiguity and good data quality.
- Deliberately excludes thin / micro-cap / recently-listed alts (avoids the worst survivorship + bad-data problems).
- **Survivorship note:** all 15 are still-listed majors, so there IS a mild survivorship bias (no delisted names). Acceptable for a scalp-mechanics study (the question is whether the *geometry* has edge, not single-name selection). 1m archive was not bulk-downloaded for 12mo (storage/time); 5m is the operative scalp timeframe and the 2h validity = 24 5m-bars, enough resolution for entry/stop/TP adjudication. **1m intrabar same-bar TP-vs-stop ambiguity is therefore approximated at 5m** and flagged lower-confidence where it matters.

## Validation

- Timestamps monotonic, UTC, deduped by primary key.
- Per-symbol coverage row recorded in `coverage` table (first_ts, last_ts, n_candles).

## Sufficiency verdict

**Sufficient for a real 12-month scalp backtest at 5m granularity** (1.55M candles, 15 liquid symbols). This resolves the prior blocker (production archive was rolling ~3.7h). The one caveat is 5m-vs-1m intrabar precision, noted in the results.
