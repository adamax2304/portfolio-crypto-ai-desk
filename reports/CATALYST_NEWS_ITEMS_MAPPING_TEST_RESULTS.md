# Catalyst ↔ news_items Mapping — Test Results (PART 1)

**Date:** 2026-06-17 · **Command:** `python -m pytest tests/test_catalyst_aster_regression.py tests/test_catalyst_layer.py -q`
**Result:** **51 passed in 1.04s** (7 new regression tests + 44 existing catalyst-layer tests).

## New regression fixture: `tests/test_catalyst_aster_regression.py`
ASTER buyback (importance 1.9, `detected_symbols_json = ["ASTER"]`) drives an in-memory `news_items` table.

| # | Test | Asserts |
|---|---|---|
| 1 | `test_news_catalyst_symbols_finds_aster` | helper returns `ASTER` for a fresh high-importance row |
| 2 | `test_news_catalyst_symbols_importance_threshold_excludes_low` | importance 0.3 → excluded |
| 3 | `test_news_catalyst_symbols_schema_discovery_legacy_column` | works when DB has only legacy `detected_symbols` column |
| 4 | `test_news_catalyst_symbols_old_row_excluded_by_window` | row 72h old, 24h window → excluded |
| 5 | `test_momentum_basket_does_not_call_catalyst_backed_no_catalyst` | summary says `CATALYST-BACKED`, ASTER not in "without confirmed catalyst" clause, playbook `wait_pullback` |
| 6 | `test_momentum_basket_regression_no_catalyst_when_set_empty` | empty set → original "without confirmed news catalyst" label preserved |
| 7 | `test_momentum_basket_does_not_promote_to_actionable` | basket never sets entry/actionable; playbook ∈ {`wait_pullback`,`avoid_chase`}, never `enter`/`buy` |

## Regression safety
- All 44 pre-existing catalyst-layer tests still pass → the schema-discovery helper and new basket param did not regress existing classification, basket-building, or alias matching.
- Tests use only in-memory SQLite — the live DB is never touched.

## Coverage of the integrity requirements
- ✅ Mandatory per-symbol `news_items` lookup before "no catalyst" (tests 1, 5, 6).
- ✅ Defensive schema discovery / legacy fallback (test 3).
- ✅ Importance + recency gating (tests 2, 4).
- ✅ No promotion to actionable; catalyst-backed-but-extended → watch-on-pullback (tests 5, 7).
