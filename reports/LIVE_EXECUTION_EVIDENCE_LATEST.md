# Live Execution Evidence

## Fill parity

| mode | entry | venue | closed | live net USD | comparable | avg live-paper R |
|---|---|---|---:|---:|---:|---:|

## Rejected counterfactuals

Only closed `valid` rows produced by `live_exit_parity_v3_incremental` are counted as comparable.

| mode | entry | stage | rejected | audited closed | winners | paper R |
|---|---|---|---:|---:|---:|---:|
| intraday | BREAKOUT_CONTINUATION | capture | 43 | 25 | 6 | -0.632 |
| intraday | PULLBACK_LIMIT | capture | 18 | 14 | 4 | 2.967 |
| intraday | MOMENTUM_TAKER_NOW | capture | 3 | 3 | 1 | 0.738 |
| intraday | LIMIT_THEN_TAKER_TIMEOUT | capture | 1 | 1 | 1 | 1.297 |

## Rejection reasons

| reason | rejected | audited closed | winners | paper R |
|---|---:|---:|---:|---:|
| LIVE_ROUTE_DISABLED | 65 | 43 | 12 | 4.371 |
| PAPER_STRATEGY_VERSION_MISSING | 36 | 27 | 7 | 4.398 |
| PAPER_NOT_ACTIONABLE | 24 | 6 | 2 | -0.765 |
| CURRENT_PRICE_NOT_REVALIDATED | 15 | 0 | 0 | 0.0 |
| ENTRY_NOT_POINT_IN_TIME | 15 | 0 | 0 | 0.0 |
| PAPER_SIZE_INVALID | 15 | 0 | 0 | 0.0 |
| PAPER_ACTION_NOT_LIVE_ENABLED | 14 | 6 | 2 | -0.765 |
| ENTRY_TOO_OLD | 12 | 0 | 0 | 0.0 |
| ENTRY_MODE_NOT_ALLOWED | 4 | 4 | 2 | 2.035 |
| OVERLAY_SNAPSHOT_NOT_PERSISTED | 1 | 0 | 0 | 0.0 |
