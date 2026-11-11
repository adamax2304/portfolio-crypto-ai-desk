# POST — Catalyst Mapping Fix Verification (PART 1)

**Date:** 2026-06-17 · **Verdict:** **CATALYST_MAPPING_FIX_READY**

## What changed (final, code-level)
| File | Change | Risk |
|---|---|---|
| `src/catalysts/collector.py` | `CATALYST_MIN_IMPORTANCE=1.0`; `news_catalyst_symbols()` helper (schema-aware, importance+window gated, error-safe); wired into momentum block | label-only; degrades to `set()` on error |
| `src/catalysts/baskets.py` | `catalyst_symbols` param; catalyst-backed vs no-catalyst split + relabel; catalyst-backed → `wait_pullback` | label-only; no scoring/entry change |
| `tests/test_catalyst_aster_regression.py` | new (7 tests) | n/a (test) |

## Verification checklist
- [x] Live DB column confirmed `detected_symbols_json` (PRAGMA), no legacy column → collector query was already correct.
- [x] ASTER row present and high-importance (id 92223, imp 1.9, `["ASTER"]`).
- [x] Helper returns `{"ASTER"}` for the fresh high-importance row (unit test 1).
- [x] Basket no longer calls a catalyst-backed mover "no catalyst" (unit test 5).
- [x] Empty-set regression preserves original behavior (unit test 6).
- [x] 51/51 catalyst tests pass; 44 pre-existing tests unregressed.
- [x] No scoring / entry / tier / threshold change. No live action.

## Behavioral diff for ASTER (the intended outcome)
- **Before:** momentum basket → "Top gainers without confirmed news catalyst", framed as a blind chase.
- **After:** momentum basket → "CATALYST-BACKED: ASTER … watch pullback / do NOT chase; NOT a no-catalyst momentum chase", playbook `wait_pullback`.
- **Promotion:** unchanged. ASTER is **catalyst-backed but overextended → watch-on-pullback**, NOT promoted to actionable. This is the correct read and is enforced by test 7.

## Rollback
Revert the two source edits; delete the new test. Zero data migration, zero live state to unwind.

## Residual (noted, intentionally unchanged)
- Collector window filter excludes NULL-`published_at` rows (`COALESCE(published_at,'') >= ?`). Latent ingestion edge; out of scope for a label-only fix. Recommend a separate ingestion-hardening task.
