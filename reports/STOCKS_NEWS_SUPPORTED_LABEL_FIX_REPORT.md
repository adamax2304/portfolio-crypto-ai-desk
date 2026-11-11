# Stocks news_supported Label Fix (PART 1)

**Date:** 2026-06-15 · Label-only. No score/tier/routing change.

## Root cause

`src/signals/registry.py` derived `news_supported` only from the crypto
catalyst-agent path (`idea.raw["catalyst"]["catalysts"]`). The stocks pipeline
attaches per-ticker news as `idea.raw["news_count"]` (count of
`CompanyNewsAgent.hits_by_symbol[symbol]`), which the registry ignored → all
1,542 stocks signals carried `news_supported=0`.

## Fix

In `build_signal_from_idea`, if the crypto path is empty, also recognise
`idea.raw["news_count"] > 0` (ticker-specific CompanyNewsAgent hits — NOT
generic market/sector headlines). The flag is display/measurement only — score,
tier, and routing are unchanged.

Added catalyst meta to the stocks idea (`_catalyst_meta_from_news`): freshest
hit's `headline_short`, `source`, `published_at`, `catalyst_type`,
`is_analyst_action`, `mapping="exact"`. This drives the catalyst labels.

## Scope

- Forward-only: applies to NEW stocks signals. Historical 1,542 rows are NOT
  rewritten (no history mutation). The derived `signal_catalyst_labels` table
  (PART 9) provides the display layer for past signals.
- Earnings/legal gates unchanged.
- Generic market/sector headlines are not marked (only per-ticker hits set the count).

## Tests (in `tests/test_catalyst_safe_fixes.py`)

- `test_1` stocks idea with news_count>0 → news_supported=1
- `test_2` stocks idea with news_count=0 → news_supported=0
- Score numeric value unchanged (the flag is read after scoring; scorer untouched).

14/14 catalyst tests pass.
