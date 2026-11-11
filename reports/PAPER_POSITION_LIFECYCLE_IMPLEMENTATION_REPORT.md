# PAPER POSITION LIFECYCLE + PARTIAL EXITS — IMPLEMENTATION (PART 3)

**Scope:** PAPER ONLY, read-model. Date: 2026-06-24. Live locked; `final_r` untouched.

## What was built
`trading-desk-control/backend/app/lifecycle.py` — `position_lifecycle(signal_id)` derives
a full exchange-style lifecycle **live** from `proposed_signals` + `signal_outcomes`
(not the batch ledger), so recent/active trades render correctly. Endpoint
`GET /api/trades/{id}/lifecycle`.

## Event sequence (per trade)
`signal_created → entry_filled | entry_missed → initial_stop_set → tp1_filled →
stop_moved_structural → tp2_filled → stop_moved_structural → tp3_filled / stop_filled /
expired_exit → position_active | position_closed`. Each event carries: timestamp, price,
qty, remaining_qty, realized_pnl_usdt, realized_r, fees_usdt, order_type (maker/taker),
reason, source.

## Partial-exit model (config-driven)
TP1 closes **33%**, TP2 **33%**, TP3 **34%** (`PARTIALS`). Blended R is the partial
accounting, distinct from the Model-F single-exit `paper_execution_r` (kept in the audit
panel). Sizing mirrors the desk **max-5x** policy ($5000, 0.5% = $25 risk).

## Worked example — ETH/USDT short +3R (`sig_c6df604c56ba3036`)
| fill | price | %closed | R | $ |
|---|---|---|---|---|
| TP1 | 1636.86 | 33% | 1.2 | +9.51 |
| TP2 | 1623.09 | 33% | 2.2 | +17.76 |
| TP3 | 1609.32 | 34% | 3.2 | +26.80 |

**Blended R = 2.21** (vs touch +3R kept in audit), **realized $54.07**, with
`stop_moved_structural` to BE after TP1, +0.5R after TP2, +2R after TP3. Three distinct
fills — no single misleading exit.

## Active-after-TP1
While `remaining_qty > 0` the status is `tp1_filled_active` / `tp2_filled_active` with a
`position_active` event ("TP1 filled · waiting next target") — the trade stays active,
realized + unrealized shown separately.

## Verdict
**PAPER_POSITION_LIFECYCLE_WITH_PARTIAL_EXITS_READY**
