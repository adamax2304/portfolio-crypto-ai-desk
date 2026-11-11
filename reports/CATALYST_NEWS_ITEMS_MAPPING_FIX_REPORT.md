# Catalyst ↔ news_items Mapping Fix Report (PART 1, P0)

**Date:** 2026-06-17 · **Type:** label/enrichment bug fix (no scoring, entry, or promotion change).
**Verdict:** **CATALYST_MAPPING_FIX_READY**

## 1. Symptom
High-importance, symbol-tagged `news_items` rows (e.g. ASTER token-buyback) were not reflected in the momentum basket: top movers that *did* have a real, confirmed catalyst were still labeled **"Top gainers without confirmed news catalyst"**. That mislabel under-credits genuine catalyst names and frames them as blind momentum chases.

## 2. Root cause (precise)
Two candidate causes were investigated:

1. **Wrong column read in the collector** — *NOT the cause here.* The live DB exposes only `detected_symbols_json` (verified via `PRAGMA table_info(news_items)`); there is **no** legacy `detected_symbols` column, and the collector's existing query already selects `detected_symbols_json`. So the events themselves are built from the correct column.
2. **Momentum basket never consulted `news_items` at all** — **THE CAUSE.** `build_momentum_breakout_basket()` in `src/catalysts/baskets.py` hard-coded the string *"Top gainers without confirmed news catalyst"* unconditionally. There was no per-symbol news lookup before asserting "no catalyst." Any mover, catalyst-backed or not, got the no-catalyst label.

So the integrity gap was a **missing mandatory news_items lookup**, not a wrong column. The fix nonetheless implements column read *defensively* (schema discovery with legacy fallback) so a future schema rename cannot silently break it.

## 3. Mapping ratio (read-only, live DB)
| Metric | Value |
|---|---|
| Total `news_items` | 15,854 |
| Symbol-tagged (`detected_symbols_json` nonempty) | 3,052 (19.3%) |
| High-importance (≥1.0) symbol-tagged | 2,738 |
| High-importance symbol-tagged, last 24h | 250 |
| Catalyst events built from these | OK — events build correctly from `detected_symbols_json` |
| **Unmapped at the momentum-basket layer (pre-fix)** | **100% of movers** — basket consulted *zero* news_items rows before labeling |

ASTER evidence rows (confirmed present):
| id | published_at | importance | detected_symbols_json |
|---|---|---|---|
| 92223 | 2026-06-17T12:22:41Z | 1.9 | `["ASTER"]` |
| 81092 | 2026-06-15T14:43:53Z | 2.4 | `["BNB","ASTER"]` |
| 81053 | 2026-06-15T14:14:30Z | 2.4 | `["ASTER","HYPE"]` |

## 4. The fix (label-only)
**`src/catalysts/collector.py`**
- Added `CATALYST_MIN_IMPORTANCE = 1.0`.
- Added `news_catalyst_symbols(conn, *, lookback_hours=24, min_importance=1.0) -> set[str]`:
  - Defensive schema discovery: `PRAGMA table_info(news_items)` → prefer `detected_symbols_json`, fall back to legacy `detected_symbols` if a future/legacy DB has only that.
  - Filters `importance >= min_importance` and `published_at >= cutoff`.
  - Returns base tickers (e.g. `{"ASTER"}`); degrades to `set()` on any error (never throws into the pipeline).
- Wired into the momentum block: fetches `cat_syms` and passes it to the basket builder.

**`src/catalysts/baskets.py`**
- `build_momentum_breakout_basket(..., catalyst_symbols: set[str] | None = None)`.
- Splits qualified movers into `catalyst_backed` vs `no_catalyst` by base ticker.
- If catalyst-backed: summary reads *"CATALYST-BACKED: … treat as catalyst-backed, watch pullback / do NOT chase; NOT a no-catalyst momentum chase"*, and `suggested_playbook = "wait_pullback"`.
- Else: original "Top gainers without confirmed news catalyst" + `avoid_chase`/`wait_pullback`.

## 5. What the fix deliberately does NOT do
- Does **not** change scoring, entries, tiering, or thresholds.
- Does **not** promote ASTER (or any mover) to actionable. Catalyst-backed **and** overextended → **watch-on-pullback**, never chase.
- Does **not** touch the collector's correct-column query, the NULL-`published_at` COALESCE (noted latent issue, left as-is), or any live behavior.

## 6. Residual / latent (noted, not changed)
- Collector query uses `WHERE COALESCE(published_at,'') >= ?`: rows with NULL `published_at` are excluded by the window filter. Not changed in this stage (would alter ingestion behavior); flagged for a future ingestion-hardening pass.

See `CATALYST_NEWS_ITEMS_MAPPING_TEST_RESULTS.md` and `POST_CATALYST_MAPPING_FIX_VERIFICATION.md`.
