# OPUS ROUTINE → MARKET DASHBOARD — VERIFY/FIX (PART 10)

**Date:** 2026-06-24. PAPER/display. Enriched-review **body unchanged**.

## Verified flow (unchanged from prior task, now VIX-complete)
- Protocol §17 (`prompts/llm_review/enriched_market_review_protocol.md`) instructs the
  ~4h enriched review to append a trailing `market_dashboard_update` JSON block — a
  **final output only**, it does not alter the review narrative.
- `scripts/market_dashboard_from_review.py` parses the latest review → `parse_and_store`
  → `market_dashboard_snapshots`. Missing/invalid block → deterministic fallback (Market
  tab never empty).

## VIX fix in the routine
`parse_and_store(..., fill_extras=True)` now calls `_backfill_extras()` after building the
Opus snapshot, so **even if Opus leaves VIX/SPY/QQQ/ETH-BTC null, they are backfilled**
from `fetch_market_extras()` (deterministic). The deterministic fallback also backfills.
So the routine feeds VIX whether or not Opus provides it, without breaking the review.

## Stale handling
Reader exposes `age_hours` + `stale` (>6h) + `stale_warning` (>4h); the Market tab shows
the warning. Fail-open keeps the previous snapshot on parse failure.

## Tests
`tests/test_market_dashboard.py`: extras shape + fail-open; `parse_and_store` backfills
VIX when Opus null (monkeypatched); fallback path.

## Verdict
**OPUS_ROUTINE_FEEDS_MARKET_DASHBOARD**
