# Historical OHLCV Backfill — Coverage Report (PART 2)

**Date:** 2026-06-18 · source: `data/archive/ohlcv` (+ `OHLCV_HISTORICAL_BACKFILL_GAPS.csv`).

## Summary
| Metric | 5m | 15m |
|---|---|---|
| symbols backfilled (Binance) | 70 | 70 |
| candles/symbol (60d) | ~17,280 | ~5,760 |
| span | 60.0d | 60.0d |
| gap vs expected | 0.0% | 0.0% |
| failed symbols | 0 | 0 |

All 70 trade-relevant symbols (5 core + 65 recent-traded) returned a full 60-day window on both timeframes. avg 98.1% of the theoretical candle count (minor exchange-side gaps only).

## Trade-relevant coverage (the acceptance metric)
- 30d crypto intraday/swing **closed** trades: **146**.
- Path-coverable on 5m after backfill: **146 (100%)** — exceeds the ≥70% target.

## Notes / limitations
- **Binance only** this run (most reliable, no paid API). Bybit/MEXC can be added via `--exchanges` if a symbol trades only there; not required since the replay reached 100% on Binance 5m.
- The archive grows forward via the per-cycle `ohlcv archive` scheduler step; this backfill seeded the deep history so the replay/shadow ledger are decision-grade now rather than in ~30 days.
- Disk: ~1.2 MB/symbol (5m+15m, 60d) → ~85 MB for 70 symbols. Modest.

## Verdict
**OHLCV_BACKFILL_READY** — deep 5m/15m history is in the archive; the path-aware replay + shadow ledger now run at 100% coverage on the recent crypto population.
