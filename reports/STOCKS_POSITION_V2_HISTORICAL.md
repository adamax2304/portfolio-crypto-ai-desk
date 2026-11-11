# Stocks Position V2 Historical Screening

> Screening only. Incomplete historical corporate-event coverage prevents promotion claims.

- Archive: `2025-02-03` to `2026-08-05`; symbols: `38`
- Closed: `9`; net USD: `$1.12`; PF: `1.0283`; win rate: `0.2222`; max DD: `$17.29`

| Setup | Closed | Net USD | PF | Win rate |
|---|---:|---:|---:|---:|
| BREAKOUT_RETEST | 1 | 23.09 | None | 1.0 |
| TREND_PULLBACK_RECLAIM | 8 | -21.97 | 0.4455 | 0.125 |

## Top rejections

- `RS_SECTOR_NOT_POSITIVE`: 3256
- `RS_SPY_NOT_POSITIVE`: 3248
- `SECTOR_RS_NOT_POSITIVE`: 2948
- `NOT_ABOVE_50D`: 2882
- `NOT_ABOVE_WEEKLY_30W`: 2578
- `NOT_ABOVE_200D`: 2335
- `SECTOR_NOT_ABOVE_50D`: 2040
- `TOO_FAR_FROM_HIGH`: 1895
- `NO_CONFIRMED_V2_SETUP`: 755
- `SECTOR_MAPPING_OR_DATA_UNAVAILABLE`: 692
- `EARNINGS_WITHIN_HOLD_WINDOW`: 496
- `MARKET_RISK_OFF`: 442
- `PORTFOLIO_SECTOR_CAP_CONSERVATIVE`: 4
- `STRUCTURAL_STOP_TOO_WIDE`: 2
- `STOP_DISTANCE_PCT_TOO_WIDE`: 2

## Limitations

- Current-universe/survivorship reconstruction.
- Historical legal/offering/FDA event-risk coverage is incomplete.
- VIX is unavailable; regime uses SPY 50d/200d only.
- Conservative one-active-position-per-sector approximation.