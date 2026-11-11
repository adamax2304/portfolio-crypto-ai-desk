# Live Funnel Report

- Generated: `2026-11-11T21:03:13.776958+00:00`
- Window: `2026-11-10T21:03:13.776958+00:00` -> `2026-11-11T21:03:13.776958+00:00`

## Proposed Signals

| asset_class | mode | n |
| --- | --- | --- |
| stocks | intraday | 104 |
| crypto | intraday | 3 |

## Paper Entry Alerts

| asset_class | mode | telegram_status | n |
| --- | --- | --- | --- |
| crypto | intraday | live_not_queued | 2 |
| crypto | intraday | shadow_crypto_quality | 1 |

## Close Alerts

| asset_class | mode | alert_type | telegram_status | n |
| --- | --- | --- | --- | --- |
| crypto | intraday | close_stop | shadow_only | 2 |

## MEXC Decisions

| mode | entry_mode | eligible | state | n |
| --- | --- | --- | --- | --- |
| intraday | PULLBACK_LIMIT | 0 | REJECTED | 2 |
| intraday | BREAKOUT_CONTINUATION | 0 | REJECTED | 1 |

## MEXC Rejection Reasons

| reason | n |
| --- | --- |
| LIVE_ROUTE_DISABLED | 3 |
| PAPER_STRATEGY_VERSION_MISSING | 3 |
| PAPER_ACTION_NOT_LIVE_ENABLED | 1 |
| PAPER_NOT_ACTIONABLE | 1 |

## MEXC Outbox

_No rows._

## MEXC Orders

_No rows._

## Recent Rejections

| captured_at | signal_id | symbol | mode | entry_mode | state | rejection_reasons_json |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-11T15:35:10.717055+00:00 | sig_4275932dbb6015c3 | ZEC/USDT | intraday | PULLBACK_LIMIT | REJECTED | ["LIVE_ROUTE_DISABLED", "PAPER_STRATEGY_VERSION_MISSING"] |
| 2026-11-11T15:14:34.247074+00:00 | sig_0c0a5b75057d9f0c | PEPE/USDT | intraday | BREAKOUT_CONTINUATION | REJECTED | ["LIVE_ROUTE_DISABLED", "PAPER_ACTION_NOT_LIVE_ENABLED", "PAPER_NOT_ACTIONABLE", "PAPER_STRATEGY_VERSION_MISSING"] |
| 2026-11-11T13:19:41.051500+00:00 | sig_fbfc3e7a6e5e810c | UNI/USDT | intraday | PULLBACK_LIMIT | REJECTED | ["LIVE_ROUTE_DISABLED", "PAPER_STRATEGY_VERSION_MISSING"] |
