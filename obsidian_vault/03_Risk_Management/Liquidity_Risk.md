# Liquidity Risk

## Where the desk filters for liquidity

1. **Universe Stage 1**: `min_24h_quote_volume_per_exchange` — binance 10M, bybit 5M, mexc 1.5M (lower in `--discovery`).
2. **Universe Stage 2**: `min_recent_candle_quote_volume` per mode — 20k scalp, 75k intraday, 150k swing.
3. **Universe Stage 2**: `max_spread_pct = 0.35` — wide spreads disqualify.
4. **`RiskAgent`**: tags `low_liquidity` warning when volume_ratio < 0.5.
5. **`ScoringAgent`**: applies cap **60** if `low_liquidity` in warnings.

## How to interpret a "low_liquidity" flag

- The symbol may be illiquid in absolute terms (Stage 1 should catch this, but discovery mode can let it through).
- Or it may be temporarily quiet (volume drying up before a move) — also dangerous, because the next breakout can slip badly.
- Either way the cap puts the ceiling at 60 (mid-C-tier).

## Slippage assumption

The desk has **no slippage model**. The reported entry zone assumes you fill near the close. For illiquid symbols you should mentally widen entry by:

- Half the spread.
- Plus your typical exchange slippage at your size.

## Per-exchange notes

- **Binance**: deepest, most reliable.
- **Bybit**: deep on majors, thinner on small caps.
- **MEXC**: thinner books overall; even more so on listings.
- `ExchangeFusionAgent` picks the best venue based on liquidity score; you should trade on that venue unless you have an explicit reason to switch.

## Common mistakes

- Trading a MEXC-only listing because the score looks fine — the cap is 70 and slippage can erase 50% of expected R/R.
- Sizing market orders into a quiet book — wait for liquidity or use limit orders.
- Trusting a `volume_ratio` spike on a single 1m bar — confirmation requires multi-bar volume above SMA20.

## Related

- [[Volume_Anomaly]]
- [[Spread_Risk]]
- [[Exchange_Risk]]
- [[Score_Caps]]

## Implemented status

- **Implemented** (filters and cap). Slippage modeling **Recommended / not implemented**.
