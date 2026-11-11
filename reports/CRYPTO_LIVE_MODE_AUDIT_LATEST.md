# Crypto Live Mode Audit

- Generated: `2026-11-11T21:42:37.466272+00:00`
- Window: `2026-11-07T21:42:37.466272+00:00` -> `2026-11-11T21:42:37.466272+00:00`
- Live: capture `True`, submission `True`, mode `live`
- Allowed modes: `intraday, invest, swing`
- Risk: `$10.00` per full trade, `$50.00` concurrent cap
- Armed venues: `mexc, bybit`

## Enabled Routes

_No rows._

## Paper To Live Reconciliation

| paper_rows | live_routable | missing_live_decision | live_rejected | live_queued_or_processing | live_submitted_or_active | not_live_route |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | 0 | 0 | 0 | 0 | 0 | 5 |

### Missing Live Decision

_No rows._

### Live Rejected

_No rows._

## Live-Compatible Paper PF

| closed | wins | losses | winrate | net_r | gross_win_r | gross_loss_r | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | None | 0 | 0 | 0 | None |

### By Live Route

_No rows._

### Excluded From Live-Compatible PF

| reason | n |
| --- | --- |
| LEGACY_PAPER_EXIT_MODEL | 21 |
| CURRENT_LIVE_ROUTE_DISABLED | 3 |
| NON_ACTIONABLE_CLOSE_REASON | 1 |

## Live Decisions

| mode | entry_mode | eligible | state | n |
| --- | --- | --- | --- | --- |
| intraday | BREAKOUT_CONTINUATION | 0 | REJECTED | 3 |
| intraday | PULLBACK_LIMIT | 0 | REJECTED | 3 |

## Venue Attempts

_No rows._

## Limit Then Taker Timeout Quality

_No rows._

### LTT Missed Or Unfilled

_No rows._

## Stock Post-Filter Live Cohort

- Filter: `stock_live_structural_alignment_v2`
- Cohort start: `2026-11-07T21:42:37.466272+00:00`

### Stock Decisions

_No rows._

### Stock Positions

_No rows._

### Stock By Entry Mode

_No rows._

### Stock Recent Rejections

_No rows._

## Liquidity Sweep V2 Paper

_No rows._

### Sweep V2 Slices

_No rows._

### Latest Evaluations

_No rows._

## Crypto Invest

_Unavailable: research.sqlite missing_
