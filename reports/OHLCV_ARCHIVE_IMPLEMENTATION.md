# OHLCV Archive — Implementation (PART 6)

**Date:** 2026-06-17 · **Verdict:** **OHLCV_ARCHIVE_READY** (started; depth grows forward).

## Why
The live cache keeps only a rolling ~220-candle window (1m≈4h, 5m≈18h, 15m≈2.3d, 1h≈9d), so a path-aware profit-protection replay covered only ~19% of trades. The archive accumulates deep history forward so future replays cover ≥30d.

## What was built
- **`scripts/archive_ohlcv_history.py`** — append-only archival into `data/archive/ohlcv/{ex}/{tf}/{SYM}.csv`:
  - **Reads** the rolling cache `data/raw/ohlcv`; **never** overwrites/deletes it.
  - concat(existing archive, fresh rolling) → **dedup by timestamp** (keep last) → **sort** ascending → write archive.
  - Archive grows monotonically (idempotent: re-running with no new candles appends 0).
  - `--timeframes 5m,15m` (default), `--exchanges`, `--dry-run`, `--coverage-report`.
- **Scheduler step** `ohlcv archive (5m/15m)` (non-fatal) after the report steps, so each cycle appends the freshly-fetched candles.
- **Replay uses archive-first**: `scripts/replay_profit_protection_path_aware.py` now resolves OHLCV from `data/archive/ohlcv` first, then the rolling cache.

## First run (seeded today)
| tf | symbols archived | candles |
|---|---|---|
| 5m | 407 (binance 151 / bybit 103 / mexc 153) | ~89,540 |
| 15m | 469 (binance 175 / bybit 121 / mexc 173) | ~103,035 |

Idempotency verified: a second immediate run appended **0** candles; no duplicate timestamps in the archive.

## Coverage today
See `OHLCV_ARCHIVE_COVERAGE_REPORT.md`. Today the archive ≈ the current rolling window (it just started). Depth increases each cycle; after ~2–4 weeks the 5m/15m archive will span ≥30d for actively-collected symbols.

## Safety
- Trading pipeline keeps using `data/raw/ohlcv` exactly as before; the archive is a separate read-only-derived tree.
- No network calls, no paid APIs, no trading-logic change.

## Tests
`tests/test_operational_deploy.py`: append dedups + idempotent; dry-run writes nothing; coverage report honest when empty; replay prefers archive over cache.
