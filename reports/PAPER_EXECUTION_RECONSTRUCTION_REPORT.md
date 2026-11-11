# Paper Execution Reconstruction Report (PART 3)

**Date:** 2026-06-09  
**Sample:** 40 A/B signals (last 14d, crypto + stocks)  
**Method:** Read-only candle replay against the same cached OHLCV the tracker uses. No DB writes.

## 1. Aggregate match vs system

| Category | n | share |
|---|---:|---:|
| match (system & reconstruction agree on outcome) | 30 | 75% |
| ambiguous (intrabar entry+stop or entry+TP detected — system silently called it) | 3 | 8% |
| mismatch (real diff) | 7 | 18% |
| missing_data (no cached OHLCV) | 0 | 0% |

## 2. Execution-quality flags detected

- **intrabar_entry_stop** (entry and stop in the SAME candle, system did not flag): 2 / 40
- **intrabar_entry_tp** (entry and TP1 in the SAME candle, system did not flag): 1 / 40
- **intrabar_stop_tp** (stop and TP1 same candle, AFTER entry — system DOES flag this): 0 / 40
- **pre_entry_invalidation** (invalidation hit before entry): 0 / 40
- **gap_slip_stop > 10% of risk** (low/high pierced > 10% past stop): 11 / 40
- **gap_slip_tp1 > 10% of risk** (high/low pierced > 10% past TP1): 10 / 40

## 3. Per-signal table

Full row-level data is in `PAPER_EXECUTION_VALIDATION_DATASET.csv` (40 rows × 40 columns).

Notable signals:

### Intrabar-ambiguous signals (system reported a clean outcome but entry collided with stop/TP in one bar)

- **CHZ/USDT** (crypto swing long, created 2026-06-09T13:39) — system outcome: `loss` R=-1.0 · flags: `entry+stop` · ohlcv `binance/1h`
- **ALLO/USDT** (crypto intraday long, created 2026-06-08T12:04) — system outcome: `loss` R=-1.0 · flags: `entry+stop` · ohlcv `binance/15m`
- **BABY/USDT** (crypto swing long, created 2026-06-08T01:58) — system outcome: `win` R=1.0 · flags: `entry+TP1` · ohlcv `binance/1h`

### True mismatches (reconstruction differs from system on outcome)

- **CHIP/USDT** swing long (created 2026-06-09T14:01) · system: `None` · reconstruction: `expired`
- **NEAR/USDT** scalp long (created 2026-06-08T15:46) · system: `expired` · reconstruction: `not_triggered`
- **MSFT** intraday short (created 2026-06-09T14:29) · system: `None` · reconstruction: `expired`
- **META** intraday short (created 2026-06-09T14:29) · system: `None` · reconstruction: `expired`
- **XLF** intraday long (created 2026-06-09T14:13) · system: `expired` · reconstruction: `loss`
- **JPM** intraday long (created 2026-06-09T13:57) · system: `expired` · reconstruction: `loss`
- **AAPL** intraday long (created 2026-06-08T15:45) · system: `win` · reconstruction: `loss`

## 4. Conclusion

The reconstruction confirms the tracker's chronological logic on **30 of 40** signals.
It exposes **3** intrabar-entry-collision cases the existing tracker silently called a clean win/loss — these are the PART 1 §A/§B issues confirmed empirically.

**No outcome data was modified.** The diff CSV is a diagnostic artifact only.

## Verdict

```
RECONSTRUCTION_COMPLETE_WITH_FLAGS
```
