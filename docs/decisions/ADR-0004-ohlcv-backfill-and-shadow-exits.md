# ADR-0004 — OHLCV Historical Backfill + Shadow Exit Manager

## Status
Accepted (2026-06-18)

## Context
The live OHLCV cache keeps only a rolling ~220-candle window (5m≈18h, 15m≈2.3d, 1h≈9d), so path-aware exit replays covered only ~17.8% of the recent crypto population — not decision-grade. To evaluate exit rules safely we need (a) deep history and (b) a way to measure alternative exits without touching trades.

## Decision
1. **Append-only deep archive** at `data/archive/ohlcv/{ex}/{tf}/{SYM}.csv` + `scripts/backfill_ohlcv_history.py` (ccxt, paginated, rate-limited, dedup, idempotent, resumable). Writes ONLY to the archive; the rolling cache `data/raw/ohlcv` is never modified. Replay + shadow read archive-first.
2. **Shadow exit manager** (`src/exits/shadow_exit_manager.py`) + ledger (`data/reports/shadow_exit_ledger.csv`) computing variants A–I candle-by-candle, conservative same-candle, honest coverage labels. Measurement only.

## Consequences
- Positive: path-aware replay coverage 17.8%→100% on 146 trades; exit evidence is now collectable across regimes.
- Negative: archive disk growth (~85 MB for 70 symbols × 60d); shadow absolute R is pessimistic vs the real book (5m + stop-first) and must be reconciled.
- Not allowed without a new ADR: letting the shadow ledger or backfill affect real exits, the rolling cache, or `partial_exit_model.enabled`.

## Evidence
- `reports/OHLCV_HISTORICAL_BACKFILL_IMPLEMENTATION.md` / `_COVERAGE_REPORT.md`
- `reports/SHADOW_EXIT_MANAGER_IMPLEMENTATION.md`
- `reports/POST_BACKFILL_PROFIT_PROTECTION_REPLAY.md`

## Review Date / Gate
Weekly: re-run the ledger/replay; reconcile the 5m-vs-tracker timeframe gap. Keep growing the archive via the per-cycle `ohlcv archive` step + occasional backfills.
