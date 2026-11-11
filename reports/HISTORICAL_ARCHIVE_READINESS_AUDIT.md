# Historical Archive Readiness Audit (PART 5)

**Date:** 2026-07-14 08:54 UTC

## 1. OHLCV archive — current state

| Source | TF | n files | median rows | window | append-only? |
|---|---|---:|---:|---|---|
| binance | 1m | 216 | 220.0 | 2026-05-31..2026-07-14 | ❌ rolling (~220 rows) |
| binance | 5m | 216 | 220.0 | 2026-05-30..2026-07-14 | ❌ rolling (~220 rows) |
| binance | 15m | 235 | 220.0 | 2026-05-20..2026-07-14 | ❌ rolling (~220 rows) |
| binance | 1h | 235 | 220.0 | 2026-05-13..2026-07-14 | ❌ rolling (~220 rows) |
| binance | 1d | 204 | 180.0 | 2025-11-24..2026-07-14 | ❌ rolling (~220 rows) |
| bybit | 1m | 145 | 220.0 | 2026-05-25..2026-07-14 | ❌ rolling (~220 rows) |
| bybit | 5m | 145 | 220.0 | 2026-05-25..2026-07-14 | ❌ rolling (~220 rows) |
| bybit | 15m | 160 | 220.0 | 2026-05-20..2026-07-14 | ❌ rolling (~220 rows) |
| bybit | 1h | 160 | 220.0 | 2026-05-13..2026-07-14 | ❌ rolling (~220 rows) |
| bybit | 1d | 137 | 180.0 | 2025-11-24..2026-07-14 | ❌ rolling (~220 rows) |
| mexc | 1m | 248 | 220.0 | 2026-05-25..2026-07-14 | ❌ rolling (~220 rows) |
| mexc | 5m | 248 | 220.0 | 2026-05-25..2026-07-14 | ❌ rolling (~220 rows) |
| mexc | 15m | 265 | 220.0 | 2026-05-20..2026-07-14 | ❌ rolling (~220 rows) |
| mexc | 1h | 265 | 220.0 | 2026-05-13..2026-07-14 | ❌ rolling (~220 rows) |
| mexc | 1d | 218 | 180.0 | 2025-11-24..2026-07-14 | ❌ rolling (~220 rows) |
| stocks (yfinance) | 15m | 28 | 1560.0 | 2026-04-16..2026-07-13 | ✅ append-only |
| stocks (yfinance) | 1h | 29 | 5082 | 2023-08-14..2026-07-13 | ✅ append-only |
| stocks (yfinance) | 1d | 87 | 500.0 | 2021-07-14..2026-07-13 | ❌ rolling |
| stocks (yfinance) | 1wk | 80 | 105.0 | 2016-06-27..2026-07-13 | ❌ rolling |

## 2. Funding / OI snapshot archive

- Funding archive at `data\raw\derivatives\funding`: ❌ missing
- OI archive at `data\raw\derivatives\oi`: ❌ missing
- `proposed_signals.funding_context` / `oi_context` are **latest-cache string blobs**, not a time series.

## 3. Spread / depth snapshot

- No archive currently. Spread is implicitly estimated from candle (high-low)/close, no L2 order book stored.

## 4. Verdict

| Surface | Append-only? | Smallest safe change |
|---|---|---|
| Crypto 1m / 5m / 15m / 1h | ❌ rolling (~220 rows) | Switch `FileStore.save_ohlcv()` to **append + dedup-by-timestamp** for `1m` and `5m` first |
| Stocks 15m / 1h / 1d | ✅ append-only (yfinance returns long history) | no change needed |
| Funding | ❌ latest-cache only | new collector + new table `funding_snapshots(symbol, exchange, ts, rate)` |
| OI | ❌ latest-cache only | new table `oi_snapshots(symbol, exchange, ts, oi_usd)` |
| Spread / depth | ❌ none | optional `orderbook_snapshots(symbol, ts, bid_size_25bps, ask_size_25bps)` |

## 5. Smallest safe change proposal (NOT implemented in this pass)

```python
# src/storage/file_store.py
def save_ohlcv(self, exchange, symbol, timeframe, frame):
    path = self.ohlcv_path(exchange, symbol, timeframe)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and timeframe in ('1m', '5m'):
        # Append-only path: read old, concat, dedup by timestamp, write.
        old = pd.read_csv(path)
        old['timestamp'] = pd.to_datetime(old['timestamp'], utc=True)
        merged = pd.concat([old, frame]).drop_duplicates('timestamp', keep='last')
        merged = merged.sort_values('timestamp')
        merged.to_csv(path, index=False)
    else:
        frame.to_csv(path, index=False)  # legacy behavior
    return path
```

Risk: file size grows. Cap at 30 days rolling = ~43k rows per symbol per 1m, ~9k per 5m. Acceptable.

**Decision for this pass: document only.** A future task can implement after operator approval.