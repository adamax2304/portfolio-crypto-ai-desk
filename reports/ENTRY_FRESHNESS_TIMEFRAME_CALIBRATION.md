# Entry-Freshness Timeframe Calibration (PART 4) — IMPLEMENTED

**Date:** 2026-06-16 · `src/notifiers/paper_entry.py::entry_freshness` (now `(asset_class,
mode)`-aware). Crypto intraday/short/scalp thresholds **unchanged** (not loosened).

| (asset, mode) | fresh ≤ | acceptable ≤ | late ≤ | very_late > | note |
|---------------|--------:|-------------:|-------:|------------:|------|
| crypto intraday / short / scalp | 2m | 5m | 15m | 15m | — (tight, unchanged) |
| crypto swing | 15m | 60m | 4h | 4h | price check before manual |
| **stocks intraday** | 20m | 30m | 45m | 45m | "(15m candle floor — price check required)" |
| stocks swing | 60m | 4h | 24h | 24h | — |
| default (unknown) | 2m | 5m | 15m | 15m | — |

**Why stocks intraday widened:** entries are tracked on **15-min candles** — a touch cannot
physically be *detected* in < ~15 min (the candle must close), so the universal 15m cutoff
wrongly flagged every stock intraday entry `very_late`. The 20/30/45 band reflects the
candle floor; a 16–24 min detection is now `acceptable`/`late` (actionable **with** the
mandatory price-check note), while a genuinely stale 50 min entry is still `very_late`
(→ late_shadow). Crypto is **not** touched.

**Time is necessary but not sufficient — manual warnings retained/required:**
- `late`/`acceptable` always carry "check price before manual entry"; stocks carry the
  "15m candle floor — price check required" note.
- Standing manual rules (unchanged): no manual entry if price worse than planned entry by
  >0.25R; if too close to stop; if stale/moved-away. (Enforced operationally; not a code
  auto-trade.)

Tests: `test_7` (crypto intraday unchanged), `test_8` (scalp tight), `test_9` (stocks
16/20/24m actionable + note, 50m very_late), `test_10` (unknown → default). **No** crypto
threshold change; **no** auto-trade; does not make stale entries look fresh (age clamped,
labels honest). **PART 4 status: DONE (implemented).**
