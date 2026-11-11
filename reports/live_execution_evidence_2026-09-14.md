# Live Execution Evidence

## Fill parity

| mode | entry | venue | closed | live net USD | comparable | avg live-paper R |
|---|---|---|---:|---:|---:|---:|
| liquidity_sweep | LIQUIDITY_SWEEP | mexc | 1 | -3.97 | 0 | None |
| stock_intraday | BREAKOUT_CONTINUATION | mexc | 35 | -37.3 | 5 | -0.3205 |
| swing | BREAKOUT_CONTINUATION | bybit | 1 | -2.53 | 1 | -1.0299 |
| swing | BREAKOUT_CONTINUATION | mexc | 16 | -11.75 | 13 | -0.53 |
| swing | LIMIT_THEN_TAKER_TIMEOUT | bybit | 1 | 0.59 | 0 | None |
| swing | LIMIT_THEN_TAKER_TIMEOUT | mexc | 1 | 1.09 | 0 | None |
| swing | PULLBACK_LIMIT | mexc | 1 | -2.45 | 1 | -1.003 |

## Rejected counterfactuals

| mode | entry | stage | rejected | closed | winners | paper R |
|---|---|---|---:|---:|---:|---:|
| swing | LIMIT_THEN_TAKER_TIMEOUT | capture | 27 | 24 | 4 | 14.784 |
| stock_intraday | BREAKOUT_CONTINUATION | capture | 23 | 6 | 2 | -0.243 |
| swing | PULLBACK_CONFIRMED_RETEST | capture | 22 | 19 | 5 | 8.1 |
| stock_intraday | BREAKOUT_CONTINUATION | preflight | 21 | 5 | 0 | 0.0 |
| swing | BREAKOUT_CONTINUATION | capture | 14 | 13 | 6 | 5.3 |
| stock_intraday | PULLBACK_LIMIT | capture | 11 | 3 | 0 | 0.0 |
| intraday | BREAKOUT_CONTINUATION | capture | 10 | 10 | 1 | -3.757 |
| intraday | LEVEL_HOLD_V2 | capture | 5 | 5 | 2 | 2.7 |
| swing | BREAKOUT_CONTINUATION | preflight | 5 | 5 | 2 | 4.3 |
| swing | MOMENTUM_TAKER_NOW | capture | 2 | 2 | 1 | 0.5 |
| intraday | MOMENTUM_TAKER_NOW | capture | 1 | 1 | 0 | 0.0 |
| intraday | PULLBACK_LIMIT | capture | 1 | 1 | 0 | -1.0 |
| swing | FIB_IMPULSE_RETEST | capture | 1 | 1 | 0 | -1.0 |
| swing | LIMIT_THEN_TAKER_TIMEOUT | preflight | 1 | 0 | 0 | 0.0 |
| swing | PULLBACK_LIMIT | preflight | 1 | 1 | 0 | 0.0 |

## Rejection reasons

| reason | rejected | closed | winners | paper R |
|---|---:|---:|---:|---:|
| LIVE_ROUTE_DISABLED | 66 | 60 | 11 | 16.627 |
| ENTRY_MODE_NOT_ALLOWED | 60 | 57 | 10 | 17.127 |
| PAPER_NOT_ACTIONABLE | 45 | 42 | 18 | 30.384 |
| CURRENT_PRICE_NOT_REVALIDATED | 34 | 31 | 18 | 31.384 |
| ENTRY_NOT_POINT_IN_TIME | 34 | 31 | 18 | 31.384 |
| PAPER_SIZE_INVALID | 34 | 31 | 18 | 31.384 |
| PAPER_STRATEGY_VERSION_NOT_LIVE_ENABLED | 33 | 30 | 6 | 3.343 |
| ENTRY_TOO_OLD | 31 | 28 | 15 | 23.884 |
| PAPER_ACTION_NOT_LIVE_ENABLED | 21 | 20 | 6 | 5.3 |
| SWING_POLICY_ACTION_NOT_LIVE_ENABLED | 17 | 16 | 5 | 5.8 |
| NO_ELIGIBLE_EXECUTION_VENUE | 13 | 5 | 1 | 0.5 |
| SOURCE_PROFILE_NOT_LIVE_ENABLED | 12 | 3 | 0 | 0.0 |
| CAPTURE_TOO_OLD | 9 | 3 | 1 | -0.122 |
| STOCK_LIVE_LOW_CONF_STOP_CONTRA_INTRADAY_BROAD | 7 | 3 | 1 | -0.122 |
| STALE_QUEUE_MAINTENANCE | 5 | 1 | 0 | 0.0 |
| MEXC request rejected: For risk management reasons, opening positions for this trading pair is unavailable in your country or region. You may only close existing positions. | 5 | 3 | 1 | 3.8 |
| PAPER_STRATEGY_VERSION_MISSING | 3 | 3 | 0 | -1.0 |
| DIRECTION_NOT_ALLOWED | 3 | 0 | 0 | 0.0 |
| STALE_PROCESSING_NO_EXCHANGE_FOOTPRINT | 2 | 0 | 0 | 0.0 |
| UNCLASSIFIED_REJECTION | 2 | 2 | 0 | 0.0 |
| SCORE_BELOW_LIVE_CANARY | 2 | 0 | 0 | 0.0 |
| STOCK_LIVE_BROAD_MARKET_CONFLICT | 2 | 0 | 0 | 0.0 |
| PAPER_EXPERIMENT_SIZE_INVALID | 1 | 0 | 0 | 0.0 |
| STALE_QUEUE_AT_DEQUEUE | 1 | 0 | 0 | 0.0 |
