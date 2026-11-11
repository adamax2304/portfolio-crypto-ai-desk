# Stocks Research Backtest

This folder documents the isolated, point-in-time research process for stock
entry modes. It is not a Paper or live strategy directory.

## Data contract

The runner first reads a separate CSV archive under `data/history/stocks/` and
then falls back to the already isolated Parquet archives:

```text
data/history/stocks/
  15m/SPY.csv
  15m/XLK.csv
  15m/AAPL.csv
  1d/AAPL.csv
  ...
```

```text
research_labs/technical_trend_reclaim/data/stocks/
  yahoo/AAPL/15m.parquet
  yahoo/AAPL/1h.parquet
  yahoo/AAPL/1d.parquet
  mexc_contract/AAPL/15m.parquet
  ...
```

CSV files must contain `timestamp,open,high,low,close,volume`; Parquet files use
`bar_open_at` plus explicit `bar_close_at` and `available_at`. Timestamps are
UTC. Missing symbol, sector ETF, or daily history is retained as a rejection,
never filled from the rolling cache. The current 15m Yahoo archive covers the
point-in-time news window, while 18-month claims are reserved for 1h/1d modes.

Canonical news must retain `published_at` and `created_at`. A news event becomes
visible only at `available_at = max(published_at, created_at)`. This prevents
look-ahead bias from articles that were historically backfilled later.

## Initial families

- `catalyst_rs`: strict Catalyst RS continuation variants only; exploratory
  sources are off.
- `earnings_gap`: strictly `event_type=earnings`. The old mixed v1 evidence is
  deliberately excluded from this study.

The harness is adapter-based: Pullback and Position Framework need their own
deterministic archived-input adapters before they are added. It is preferable to
leave a family unsupported than to replay it with a different entry rule.

## Run

```powershell
python -m src.cli stocks-research-backtest `
  --study-start 2025-02-01T00:00:00+00:00 `
  --study-end 2026-08-01T00:00:00+00:00
```

Use `--dry-run` to validate coverage without writing any research result table
or report.

## Selection discipline

Each candidate is replayed using the existing deterministic entry, stop, three
target, realistic cost, and same-day exit logic. Duplicate source rows are
collapsed to one `symbol × event-type × session` observation. Parameter choice
uses only the earlier training window; it is then measured on a later test
window. No selected variant can change Paper/live automatically.
