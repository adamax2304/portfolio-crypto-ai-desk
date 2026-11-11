# Open Interest Risk

## Source

Binance USD-M futures `openInterest` + `openInterestHist` (hourly), Bybit + OKX public snapshots.

## How `DerivativesAgent` reads it

`_oi_change(hist)` returns the % change between first and last bar of the available history window. Combined with 1h price change to produce a label:

| price_24h | oi_change_24h | Label | alignment |
|---|---|---|---|
| > 0 | > 0 | "price up + OI up: fresh positioning confirms trend, monitor crowding" | +0.65 |
| > 0 | < 0 | "price up + OI down: short covering, weaker continuation quality" | +0.20 |
| < 0 | > 0 | "price down + OI up: fresh shorts pressing, possible squeeze if price reclaims" | −0.45 |
| < 0 | < 0 | "price down + OI down: deleveraging or long liquidation" | −0.25 |

For a long setup, alignment is added directly. For a short, alignment is **negated** in `ScoringAgent._market_alignment`-style derivative quality math (so "price down + OI up" becomes +0.45 for shorts).

## What this means in practice

- Long entry with "price up + OI up" → derivative quality high; component scores well.
- Long entry with "price up + OI down" (short covering) → weaker continuation; lower derivative score.
- Short entry with "price down + OI up" (fresh shorts) → potential squeeze risk; the desk warns.
- Either direction with "deleveraging" → derivative noise; mild negative.

## Practical reading

- **Healthy trend confirmation**: price + OI both moving the trade's way.
- **Liquidation rip warning**: price up + OI down can be a short squeeze cleanout; the next pullback may be quick.
- **Bear continuation confirmation**: price down + OI up + funding positive = fresh shorts; tradable for continuation but watch for sudden squeeze if levels reclaim.

## Common mistakes

- Treating rising OI as always bullish — it depends on price direction.
- Ignoring "OI down + price up" — this is often the end of a short-covering rally.

## When OI history is unavailable

- `oi_change_pct = None` → label "data partially unavailable", alignment 0.
- Falls back to baseline derivative quality.

## Related

- [[Funding_Risk]]
- [[Derivatives_Agent]]
- [[Multi_Exchange_Derivatives_Agent]]

## Implemented status

- **Implemented** for Binance + Bybit/OKX where endpoints return data.
