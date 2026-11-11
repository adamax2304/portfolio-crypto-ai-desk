# POST — Catalyst-Scan Integrity Verification (PART 2)

**Date:** 2026-06-17 · **Verdict:** **CATALYST_INTEGRITY_SCAN_OPERATIONAL_READY** (with one open regression flag to clear on the next fresh scan).

## Verification
- [x] Scheduler runs the integrity scan **after** the catalyst scan (cycle plan order: "catalyst / narrative scan" → "catalyst integrity scan").
- [x] The scan writes `reports/CATALYST_INTEGRITY_DAILY_SUMMARY.md` and prints a WARNING line on a regression signature.
- [x] Per-signal payload carries `catalyst_integrity_status` / `direct_news_items_checked` / `catalyst_mapping_confidence`.
- [x] Missing `news_items` → `unknown` (not a fake "no catalyst").
- [x] No trade promotion; catalyst-backed + overextended stays watch-pullback.

## Current live finding (HIGH-priority flag)
The most recent scan flagged: **no-catalyst basket contains a symbol with a direct news hit: ASTER** (regression signature), confidence `medium`, status `warning`.

**Diagnosis:** today's on-disk `data/catalysts/2026-06-17/narrative_baskets.jsonl` was written by a catalyst-scan that ran **before** the ASTER label fix landed in code. The fix is in `src/catalysts/baskets.py` (verified, 729 tests green), so the next scheduler cycle's `catalyst-scan` will regenerate the artifact with the fixed builder, and the integrity scan that follows should clear the flag.

**Action / acceptance:** on the **next fresh catalyst-scan**, re-run the integrity scan:
- If `no_catalyst_basket_news_hits` is **empty** → the fix is confirmed live; status returns to `ok`. ✅ expected.
- If ASTER (or any symbol) **still** appears → this is a real regression; this report is the HIGH-priority signal to investigate `build_momentum_breakout_basket`'s `catalyst_symbols` wiring in the collector.

This is exactly the monitoring value intended: the regression class is now *caught automatically*, not silently shipped.

## Tests
`tests/test_catalyst_integrity.py` (6) — see PART 8 results.
