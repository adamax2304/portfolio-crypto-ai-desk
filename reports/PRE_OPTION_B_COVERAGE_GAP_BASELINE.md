# Pre-Fix Baseline — Option B Coverage Gap (PART 1)

**Date:** 2026-06-16 · Read-only.

## Root cause (confirmed)

| Layer | Universe it touches |
|-------|---------------------|
| `WatchlistMonitor.re_evaluate` OHLCV refresh | **only** `BTC/USDT + ETH/USDT + C-tier/rejected watchlist` (`watch_symbols()`), via `BinanceOHLCVCollector.fetch(symbols=watch_universe, timeframes=mode_tfs)` |
| `track_pending_entries` (Option B) | tier A/B **non-terminal** signals (by `signal_id`) — reads **cached** OHLCV per signal |

**Gap:** the pending tracker's universe (A/B pending, incl. discovery alts) is a *superset*
of what the monitor refreshes. Discovery alts with A/B signals (ASTER, HMSTR, RIF, XPL,
ALLO …) are **not** in `watch_symbols()` (those are C-tier/rejected), so their OHLCV cache
is **not** refreshed on the tick. The tracker then reads stale candles and cannot see a
fresh entry-touch until the next ~2h full `track-signals` (which refreshes the broad
universe) — exactly the multi-hour detection lag observed
(ASTER/HMSTR/RIF/XPL/ALLO touched 13:00–17:00Z, detected 16:07/18:53Z).

## Evidence
- 26 distinct pending **A/B crypto** symbols currently (e.g. RIF, HMSTR, GPS, ZEC, ZRO,
  WLD, PUMP, SUI, TAO, NEAR, BABY, MEME …) — most are **not** in the monitor watch set.
- These alts ARE Binance-spot-listed (cache files exist under `data/raw/ohlcv/binance/…`),
  so a `BinanceOHLCVCollector.fetch` on the tick **can** refresh them.
- Pending tracker itself is healthy: 84 ticks, 0 DB-lock, no stale locks, no dup, no
  same-tick, scalp shadow_only (per the live sanity check).

## Expected fix
Refresh OHLCV for the **pending A/B crypto symbols** on the monitor tick **before**
`track_pending_entries`, so entry-touch on discovery alts is detected within one tick.

**PART 1 status: DONE — root cause = stale cache for unwatched pending alts; tracker logic
is fine.**
