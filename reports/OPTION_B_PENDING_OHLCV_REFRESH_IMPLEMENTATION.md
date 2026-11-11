# Pending-Symbol OHLCV Refresh — Implementation (PART 3)

**Date:** 2026-06-16 · `src/cli.py` (`monitor-watchlist` loop)

On each monitor tick, **before** `track_pending_entries` (and after `re_evaluate`):

1. `pending_symbols(store, asset_class="crypto")` → priority-ordered pending A/B symbols.
2. Bounded to **cap=60** with **round-robin** by `tick_index` (so >60 pending symbols still
   all get covered across consecutive ticks; actionable+recent prioritized first).
3. `BinanceOHLCVCollector(config, file_store).fetch(symbols=refresh_syms,
   timeframes=["1m","5m","15m","1h"])` — only OHLCV. **No** scanner, LLM, news, scoring, or
   signal generation.
4. Logs `pending OHLCV refresh: N symbols (M skipped: unsupported market/data)` — skips are
   surfaced from `CollectionSummary.failed` (e.g. a symbol not on Binance spot).
5. Then `track_pending_entries` runs against the now-fresh cache.

Wrapped in its own try/except → a refresh failure never blocks the tracker or the tick
(degrades to tracking on slightly-staler cache).

**Live confirmation (2026-06-16 23:33Z, fresh monitor):**
```
Tick 1 at 23:33:37
  pending OHLCV refresh: 23 symbols (1 skipped: unsupported market/data)
  pending tracker: checked=162 tp=156 stop=0 exp=0
```
Direct refresh-path smoke also confirmed cache mtimes update for live pending alts
(GPS/BCH/SOL/NIGHT → REFRESHED, 0 failed).

The scheduler's `monitor-watchlist --interval 300` picks this up automatically on its next
fresh monitor process (a running process must restart to load the new code).

**PART 3 status: DONE — pending symbols refreshed before the tracker, live-verified.**
