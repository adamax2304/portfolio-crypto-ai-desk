# Fast-Move Latency Tool (PART 7)

**Date:** 2026-06-15 · Report-only tool. No trading-logic change, no DB writes.

## What was added

`scripts/report_fast_move_latency.py` →
`reports/FAST_MOVE_LATENCY_REPORT.md` + `.csv`.

For top 1h / 4h / 24h gainers (from stored binance 1h candles) it computes:
- move_start (first bar of the window);
- first related news timestamp (news_items symbol/title match);
- first proposed_signal timestamp + tier;
- first Telegram (signal_alerts) timestamp;
- `move→news`, `news→signal`, `signal→telegram` latencies (hours);
- whether the move produced a signal at all.

## First run

```
45 movers analyzed (top 15 over 1h/4h/24h) · 9 produced a signal
```

Confirms the structural finding: most fast movers either fall outside the
tradable universe or are entered late / rejected as chase — the ~2h crypto
report cadence bounds `news→signal` latency.

## Rules honoured

- Report-only; no DB writes except the two report files.
- Handles missing news/signal gracefully (empty cells, not errors).

## Tests

Exercised via the live run (45 movers). The CSV columns + graceful missing-news
handling are validated by the successful run over real data.
