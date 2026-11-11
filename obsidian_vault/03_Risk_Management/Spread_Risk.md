# Spread Risk

## Filter

`config/universe.yaml.max_spread_pct = 0.35`. Symbols whose Binance-quoted bid/ask spread exceeds 0.35% are excluded from the universe.

## Why it matters

- A 0.35% spread means your round-trip cost is at least 0.7% (you pay the spread twice). On a scalp targeting 1 ATR (~1%), this halves your expected R/R.
- Wide spreads correlate with low liquidity, which compounds slippage risk.

## What spread the desk uses

- Best-bid / best-ask snapshot from Binance ticker, available during Stage 2 ranking. Bybit / MEXC spreads are not currently checked symbol-by-symbol in the universe pipeline.

## When spread is unknown

- If the exchange doesn't expose bid/ask in the call, the spread filter is skipped — the symbol passes through. This is acceptable for anchor (Binance) but can let through bad symbols from MEXC.

## Operator rules

- For scalps, mentally raise the spread tolerance to 0.10–0.15% — anything wider eats the R/R.
- For swing, 0.35% is acceptable.

## Common mistakes

- Trading a 0.5% spread symbol because "the chart looks clean" — the cost is in the spread.

## Related

- [[Liquidity_Risk]]
- [[Exchange_Risk]]
- [[Score_Caps]]

## Implemented status

- **Implemented** (Binance spread filter only).
