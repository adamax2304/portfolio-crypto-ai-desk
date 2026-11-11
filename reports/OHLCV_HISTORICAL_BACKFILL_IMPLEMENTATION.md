# Historical OHLCV Backfill — Implementation (PART 2)

**Date:** 2026-06-18 · **Verdict:** **OHLCV_BACKFILL_READY**
**Writes only to `data/archive/ohlcv`; rolling cache untouched; no trade-math change.**

## What was built
`scripts/backfill_ohlcv_history.py` — paginated historical OHLCV fetch via **ccxt** (rate-limited), append-only into the archive.
- **Symbols:** core liquid (BTC/ETH/SOL/BNB/XRP) + symbols with closed crypto intraday/swing trades in the last 60d. `--limit` caps the count.
- **Timeframes:** 5m, 15m (`--timeframes`); **lookback** `--lookback-days` (default 60).
- **Append-only / dedup / sort / idempotent:** concat(existing, fresh) → drop_duplicates(timestamp) → sort → write. Re-runs add 0.
- **Resumable / safe-on-interrupt:** fetches the full lookback window each run; dedup makes interrupted re-runs converge. (A bug where resume-from-newest only re-fetched today was fixed → it now fills the deep history.)
- **Rate-limited:** ccxt `enableRateLimit=True`; per-(symbol,tf) **retry with backoff**; a failed symbol/tf is skipped + reported, never crashes the run.
- **Pagination:** `fetch_ohlcv(since=…, limit=1000)` looped to now.
- **Dry-run:** prints the plan, writes nothing.

## Run result (70 symbols × {5m,15m} × 60d, Binance)
| Metric | Value |
|---|---|
| ok rows (symbol×tf) | **140 / 140** |
| skipped / failed | **0** |
| avg coverage of expected candles | **98.1%** |
| gaps | all **0.0%** (BTC/ETH/SOL etc.: 17,280 5m candles spanning 60.0d) |

Per-(symbol,tf) detail in `OHLCV_HISTORICAL_BACKFILL_GAPS.csv`; coverage in `OHLCV_HISTORICAL_BACKFILL_COVERAGE_REPORT.md`.

## Effect on replay coverage
Path-aware profit-protection replay coverage of the 30d crypto intraday/swing population jumped **17.8% → 100% (146/146)** on 5m — now decision-grade for the window (see PART 5).

## Safety / tests
- Writes only `data/archive/ohlcv`; `data/raw/ohlcv` (rolling cache) untouched (test).
- Append dedup + idempotent; dry-run writes nothing; broken fetch does not corrupt the archive (tests).
- Archive-first replay + shadow manager read the backfilled archive (tests).

**Verdict: OHLCV_BACKFILL_READY** — 5m/15m coverage for trade-relevant symbols now exceeds the 70% acceptance target (100% on the 146-trade population).
