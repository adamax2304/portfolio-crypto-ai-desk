# Live Execution Evidence

## Fill parity

| mode | entry | venue | closed | live net USD | comparable | avg live-paper R |
|---|---|---|---:|---:|---:|---:|
| intraday | BREAKOUT_CONTINUATION | bybit | 4 | -16.23 | 4 | -0.093 |
| intraday | BREAKOUT_CONTINUATION | mexc | 5 | -11.24 | 5 | -0.0401 |
| liquidity_sweep | LIQUIDITY_SWEEP | mexc | 1 | -3.97 | 0 | None |
| stock_intraday | BREAKOUT_CONTINUATION | mexc | 37 | -33.48 | 5 | -0.3205 |
| swing | BREAKOUT_CONTINUATION | bybit | 1 | -2.53 | 1 | -1.0299 |
| swing | BREAKOUT_CONTINUATION | mexc | 23 | -14.37 | 20 | -0.5486 |
| swing | LIMIT_THEN_TAKER_TIMEOUT | bybit | 3 | -2.74 | 2 | 0.0973 |
| swing | LIMIT_THEN_TAKER_TIMEOUT | mexc | 6 | -4.04 | 4 | 0.0837 |
| swing | PULLBACK_LIMIT | bybit | 2 | -5.01 | 2 | -0.6183 |
| swing | PULLBACK_LIMIT | mexc | 14 | -10.49 | 14 | -0.1717 |

## Rejected counterfactuals

| mode | entry | stage | rejected | closed | winners | paper R |
|---|---|---|---:|---:|---:|---:|
| swing | LIMIT_THEN_TAKER_TIMEOUT | capture | 32 | 29 | 5 | 14.284 |
| stock_intraday | BREAKOUT_CONTINUATION | capture | 29 | 6 | 2 | -0.243 |
| swing | PULLBACK_CONFIRMED_RETEST | capture | 23 | 21 | 5 | 6.1 |
| swing | BREAKOUT_CONTINUATION | capture | 22 | 21 | 8 | 6.6 |
| stock_intraday | BREAKOUT_CONTINUATION | preflight | 21 | 5 | 0 | 0.0 |
| intraday | BREAKOUT_CONTINUATION | capture | 14 | 14 | 3 | 2.389 |
| stock_intraday | PULLBACK_LIMIT | capture | 13 | 3 | 0 | 0.0 |
| swing | PULLBACK_LIMIT | capture | 10 | 10 | 0 | -2.0 |
| intraday | LEVEL_HOLD_V2 | capture | 7 | 7 | 2 | 0.7 |
| swing | MOMENTUM_TAKER_NOW | capture | 6 | 6 | 3 | 0.5 |
| swing | BREAKOUT_CONTINUATION | preflight | 5 | 5 | 2 | 4.3 |
| intraday | PULLBACK_LIMIT | capture | 4 | 4 | 2 | -1.0 |
| swing | PULLBACK_LIMIT | preflight | 4 | 4 | 0 | 0.0 |
| intraday | BREAKOUT_CONTINUATION | preflight | 3 | 3 | 1 | 2.234 |
| intraday | MOMENTUM_TAKER_NOW | capture | 3 | 3 | 1 | 4.581 |
| intraday | LIMIT_THEN_TAKER_TIMEOUT | capture | 2 | 2 | 0 | -2.0 |
| swing | LIMIT_THEN_TAKER_TIMEOUT | preflight | 2 | 1 | 0 | 0.0 |
| swing | FIB_IMPULSE_RETEST | capture | 1 | 1 | 0 | -1.0 |

## Rejection reasons

| reason | rejected | closed | winners | paper R |
|---|---:|---:|---:|---:|
| ENTRY_MODE_NOT_ALLOWED | 79 | 77 | 16 | 15.208 |
| PAPER_NOT_ACTIONABLE | 75 | 73 | 24 | 27.384 |
| LIVE_ROUTE_DISABLED | 69 | 64 | 12 | 15.127 |
| CURRENT_PRICE_NOT_REVALIDATED | 54 | 52 | 24 | 31.384 |
| ENTRY_NOT_POINT_IN_TIME | 54 | 52 | 24 | 31.384 |
| PAPER_SIZE_INVALID | 54 | 52 | 24 | 31.384 |
| ENTRY_TOO_OLD | 49 | 47 | 20 | 20.684 |
| PAPER_ACTION_NOT_LIVE_ENABLED | 39 | 39 | 6 | -4.7 |
| PAPER_STRATEGY_VERSION_NOT_LIVE_ENABLED | 36 | 34 | 6 | -0.657 |
| SWING_POLICY_ACTION_NOT_LIVE_ENABLED | 34 | 34 | 5 | -3.2 |
| NO_ELIGIBLE_EXECUTION_VENUE | 17 | 9 | 2 | 2.734 |
| SOURCE_PROFILE_NOT_LIVE_ENABLED | 14 | 3 | 0 | 0.0 |
| PAPER_STRATEGY_VERSION_MISSING | 11 | 11 | 4 | 5.528 |
| CAPTURE_TOO_OLD | 10 | 3 | 1 | -0.122 |
| STOCK_LIVE_LOW_CONF_STOP_CONTRA_INTRADAY_BROAD | 7 | 3 | 1 | -0.122 |
| MEXC request rejected: For risk management reasons, opening positions for this trading pair is unavailable in your country or region. You may only close existing positions. | 6 | 4 | 1 | 3.8 |
| STALE_QUEUE_MAINTENANCE | 5 | 1 | 0 | 0.0 |
| STOCK_LIVE_BROAD_MARKET_CONFLICT | 5 | 0 | 0 | 0.0 |
| SCORE_BELOW_LIVE_CANARY | 4 | 0 | 0 | 0.0 |
| DIRECTION_NOT_ALLOWED | 3 | 0 | 0 | 0.0 |
| STOCK_LIVE_LEGACY_STOP_NOT_STRUCTURAL | 3 | 0 | 0 | 0.0 |
| STALE_QUEUE_AT_DEQUEUE | 2 | 1 | 0 | 0.0 |
| STALE_PROCESSING_NO_EXCHANGE_FOOTPRINT | 2 | 0 | 0 | 0.0 |
| UNCLASSIFIED_REJECTION | 2 | 2 | 0 | 0.0 |
| Bybit request rejected: ab not enough for new order | 1 | 1 | 0 | 0.0 |
