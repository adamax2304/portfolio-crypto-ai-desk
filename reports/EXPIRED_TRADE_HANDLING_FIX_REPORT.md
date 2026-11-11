# Expired Trade Handling Fix (PART 3)

**Date:** 2026-06-24.

## Bug
Expired (and ALL) ledger rows had `exit_price = None` → no close price, no exit marker. Expired was represented only as `paper_execution_r` (0R / +0.5R via Model F) with no price attached.

## Policy (`paper_expiry_policy`)
- Default: an expired-after-entry trade closes at the **implied close price from `paper_execution_r`** (1R = |entry−stop| in price): `exit_price = entry ± paper_execution_r × |entry−stop|` (sign by direction). For a Model-F-protected expiry this is the protected level (BE/lock) — the honest paper close.
- If protection was armed and price crossed it, that protected level IS the close (already captured by `paper_execution_r`).
- If no resolvable R/price → `paper_execution_available=false`, **not** a silent 0 (sim skips; backend flags).
- `expiry_close_price_source = "implied_from_paper_execution_r"`.

## Fields added (ledger + chart-events)
`exit_price` (now populated for ALL rows — 0 NULL), `expiry_close_price`, `expiry_close_price_source`, plus a chart marker `marker_type = expired_exit` (price + R + net $).

## Result
586 ledger rows: `exit_price` NULL = **0**; **133 genuine expiry rows** carry `expiry_close_price` (narrowed from an over-broad 488 that wrongly included BE/lock *stop* closes — those are now `exit`, not `expired`). Chart-events return an `expired_exit` / `exit` marker with price + R + net $.

## Verdict
`EXPIRED_TRADES_CLOSE_WITH_MARK_PRICE_OR_EXPLICIT_UNAVAILABLE`
