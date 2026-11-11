# Funding / OI Append-Only Archive (PART 2)

**Date:** 2026-06-15 · Archive-only. No scoring read-path change.

## What was added

| Item | Detail |
|---|---|
| `funding_snapshots` table | id, fetched_at, exchange, symbol, normalized_symbol, funding_rate, next_funding_time, mark_price, index_price, long_short_ratio, crowding_label, raw_json, source_file, created_at. UNIQUE(exchange, symbol, fetched_at). |
| `oi_snapshots` table | id, fetched_at, exchange, symbol, normalized_symbol, oi_value, oi_value_usd, oi_change_pct, long_short_ratio, crowding_label, raw_json, source_file, created_at. UNIQUE(exchange, symbol, fetched_at). |
| `SQLiteStore.record_funding_snapshot()` / `record_oi_snapshot()` | `INSERT OR IGNORE` (append + dedup). Return True on insert, False on dup. |
| `src/data_collectors/derivatives_archive.py` | `archive_derivatives_records(store, records, exchange)` — parses the per-symbol derivatives dict, writes one funding + one OI row each. Best-effort: never raises; skips failed/`data_available=False` records. |
| `supervisor._build_crypto_market_context` hook | After `DerivativesAgent.run(...)`, a guarded best-effort call archives `derivatives_records` (binance) + `external_records` (multi). Wrapped in try/except → live scoring never blocked. |

## Rules honoured

- **Append-only + dedup** on (exchange, symbol, fetched_at). Never overwrites.
- **No scoring read-path change** — verified by `test_6`: scoring agents never import the archive helper or reference the snapshot tables.
- **Best-effort** — `test_5`: helper never raises; failed records skipped; `None` store handled.

## Tests

- `test_3` funding insert + dedup blocks duplicate
- `test_4` OI insert
- `test_5` helper best-effort (skips failed record, no raise, None store ok)
- `test_6` no scoring dependency on archive tables

## State

Tables created (0 rows until the next live derivatives fetch populates them — the running scheduler will append on its next crypto report cycle). This is the data foundation that unblocks future Level-B/C replay and funding-cost modelling (previously impossible — funding/OI was latest-cache only).
