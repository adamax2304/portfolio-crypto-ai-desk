# Live Funnel Report

- Generated: `2026-10-02T02:38:54.118654+00:00`
- Window: `2026-10-01T02:38:54.118654+00:00` -> `2026-10-02T02:38:54.118654+00:00`

## Proposed Signals

| asset_class | mode | n |
| --- | --- | --- |
| stocks | intraday | 145 |
| crypto | intraday | 9 |

## Paper Entry Alerts

| asset_class | mode | telegram_status | n |
| --- | --- | --- | --- |
| stocks | intraday | live_not_queued | 13 |
| crypto | intraday | live_not_queued | 6 |
| stocks | intraday | late_shadow | 6 |
| crypto | intraday | late_shadow | 3 |
| stocks | intraday | shadow_sector_cap | 2 |

## Close Alerts

| asset_class | mode | alert_type | telegram_status | n |
| --- | --- | --- | --- | --- |
| crypto | intraday | close_stop | shadow_only | 9 |
| stocks | intraday | close_expired | shadow_only | 7 |
| stocks | intraday | close_tp | shadow_only | 5 |
| crypto | swing | close_stop | shadow_only | 3 |
| crypto | intraday | close_tp | shadow_only | 2 |
| stocks | intraday | close_stop | shadow_only | 1 |

## MEXC Decisions

| mode | entry_mode | eligible | state | n |
| --- | --- | --- | --- | --- |
| intraday | BREAKOUT_CONTINUATION | 0 | REJECTED | 5 |
| intraday | PULLBACK_LIMIT | 0 | REJECTED | 4 |

## MEXC Rejection Reasons

| reason | n |
| --- | --- |
| LIVE_ROUTE_DISABLED | 9 |
| PAPER_STRATEGY_VERSION_MISSING | 5 |
| ENTRY_TOO_OLD | 4 |
| CURRENT_PRICE_NOT_REVALIDATED | 3 |
| ENTRY_NOT_POINT_IN_TIME | 3 |
| PAPER_NOT_ACTIONABLE | 3 |
| PAPER_SIZE_INVALID | 3 |
| PAPER_ACTION_NOT_LIVE_ENABLED | 1 |

## MEXC Outbox

_No rows._

## MEXC Orders

_No rows._

## Recent Rejections

| captured_at | signal_id | symbol | mode | entry_mode | state | rejection_reasons_json |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-10-01T14:00:24.833546+00:00 | sig_12702a352952c806 | PENGU/USDT | intraday | BREAKOUT_CONTINUATION | REJECTED | ["LIVE_ROUTE_DISABLED", "PAPER_ACTION_NOT_LIVE_ENABLED", "PAPER_SIZE_INVALID", "PAPER_NOT_ACTIONABLE", "ENTRY_NOT_POINT_IN_TIME", "CURRENT_PRICE_NOT_REVALIDATED", "ENTRY_TOO_OLD"] |
| 2026-10-01T07:20:07.265652+00:00 | sig_242184a68df76428 | RUNE/USDT | intraday | PULLBACK_LIMIT | REJECTED | ["LIVE_ROUTE_DISABLED", "PAPER_STRATEGY_VERSION_MISSING"] |
| 2026-10-01T07:09:03.358605+00:00 | sig_bbc6b2e40d783809 | ETH/USDT | intraday | PULLBACK_LIMIT | REJECTED | ["LIVE_ROUTE_DISABLED", "PAPER_SIZE_INVALID", "PAPER_NOT_ACTIONABLE", "PAPER_STRATEGY_VERSION_MISSING", "ENTRY_NOT_POINT_IN_TIME", "CURRENT_PRICE_NOT_REVALIDATED", "ENTRY_TOO_OLD"] |
| 2026-10-01T04:53:38.277890+00:00 | sig_cea2a73a1b07ffd9 | AERO/USDT | intraday | BREAKOUT_CONTINUATION | REJECTED | ["LIVE_ROUTE_DISABLED", "PAPER_STRATEGY_VERSION_MISSING"] |
| 2026-10-01T04:45:35.676493+00:00 | sig_644c669f30394b67 | MOVR/USDT | intraday | PULLBACK_LIMIT | REJECTED | ["LIVE_ROUTE_DISABLED", "PAPER_STRATEGY_VERSION_MISSING"] |
| 2026-10-01T04:36:37.933587+00:00 | sig_f4d62c319fd64ddb | NIGHT/USDT | intraday | BREAKOUT_CONTINUATION | REJECTED | ["LIVE_ROUTE_DISABLED", "ENTRY_TOO_OLD"] |
| 2026-10-01T04:15:21.936063+00:00 | sig_7ee6c595e20d45a1 | NEAR/USDT | intraday | BREAKOUT_CONTINUATION | REJECTED | ["LIVE_ROUTE_DISABLED", "PAPER_SIZE_INVALID", "PAPER_NOT_ACTIONABLE", "ENTRY_NOT_POINT_IN_TIME", "CURRENT_PRICE_NOT_REVALIDATED", "ENTRY_TOO_OLD"] |
| 2026-10-01T04:10:47.723785+00:00 | sig_c67ae91975dc9157 | DOT/USDT | intraday | PULLBACK_LIMIT | REJECTED | ["LIVE_ROUTE_DISABLED", "PAPER_STRATEGY_VERSION_MISSING"] |
| 2026-10-01T04:03:46.679612+00:00 | sig_0a300057056f3740 | ENA/USDT | intraday | BREAKOUT_CONTINUATION | REJECTED | ["LIVE_ROUTE_DISABLED"] |
