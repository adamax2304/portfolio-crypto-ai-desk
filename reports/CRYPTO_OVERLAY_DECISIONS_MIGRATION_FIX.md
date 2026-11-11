# crypto_quality_overlay_decisions — idempotent migration fix

Date: 2026-07-08 · READ-MODEL only. Live LOCKED · no live orders · `final_r` / `signal_outcomes` /
`proposed_signals` / `paper_portfolio_ledger` untouched by this fix.

## Bug
The real `crypto_quality_overlay_decisions` table was created (in an earlier run) **before** the
`decision_context_type` column was added to the DDL. `CREATE TABLE IF NOT EXISTS` does not alter an
existing table, so the live table had **28 columns** while the positional `INSERT ... VALUES (29 ?)`
supplied 29 values → a **persisted** `crypto-quality-refresh` / `crypto-overlay-report` would fail
(`--dry-run` masked it because it never inserts).

## Fix
1. **`ensure_tables(conn)`** in `src/execution/crypto_quality_overlay.py` — creates both overlay tables
   and does an **idempotent migration**: `ALTER TABLE … ADD COLUMN decision_context_type TEXT` when
   missing, then backfills existing rows to `'current_snapshot'`. Never drops, never deletes rows.
2. **Explicit column-list INSERT** — `INSERT … (col1,…,col29) VALUES (…)` using a shared `_DECISION_COLS`
   tuple, so a future nullable column can never break the write again.
3. Wired `ensure_tables` into **both** `refresh()` and `refresh_cooldowns()` (every persisted write path).

## Verification (real DB, persisted — not dry-run)
- `python -m src.cli crypto-quality-refresh` → **evaluated=483, persisted OK** (FULL=180 HALF=103
  SHADOW=200 BLOCK=0). Previously this would have raised a column-count error.
- `PRAGMA table_info` → `decision_context_type` present (29 columns).
- `SELECT decision_context_type, COUNT(*) … GROUP BY` → **all 489 rows `current_snapshot`** (483 fresh +
  6 pre-existing backfilled).
- `python -m src.cli crypto-overlay-report` → writes `reports/CRYPTO_QUALITY_OVERLAY.md` (no crash;
  counterfactual preserved; ledger not recomputed here).

## Invariants (before → after the persisted refresh)
| | before | after |
|---|---|---|
| `proposed_signals` | 3348 | **3348** |
| `signal_outcomes` | 804070 | **804070** |
| `SUM(final_r)` | 962966.0 | **962966.0** |
| active-profile ledger rows | 837 | **837** (untouched by this fix) |

## Tests
- `tests/test_crypto_overlay_migration.py` (new, 2): `ensure_tables` migrates an OLD 28-col schema
  (column added, old row preserved + labelled `current_snapshot`, new insert works, idempotent second
  call); **persisted `refresh(persist=True)` survives an old-schema DB** and labels rows `current_snapshot`.
- Regression: overlay + migration + paper_actionability + paper_portfolio + default_market_schedule —
  **75 passed**. Scheduler dry-run `--dry-run --crypto-only` — OK.
