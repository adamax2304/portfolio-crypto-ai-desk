# Funding Rate

See [[Funding_Risk]] for the full risk treatment. This page is the data-source view.

## Source

Binance USD-M futures `premium_index.lastFundingRate` per symbol.

Bybit / OKX expose funding via `MultiExchangeDerivativesCollector` snapshots; the cap thresholds in `ScoringAgent` reference the Binance number specifically.

## Derived

`DerivativesAgent` maps funding into:

- `funding_rate` (float).
- `crowding_risk` label (`extreme long crowding / elevated long crowding / normal / unknown / short squeeze potential`).
- `squeeze_potential` label.
- Alignment adjustment (−0.35 / −0.15 / +0.15 / 0).

## Thresholds

| funding_rate | Label | Score-cap effect |
|---|---|---|
| > +0.001 | extreme long crowding | cap 78 if direction = long |
| +0.0005 .. +0.001 | elevated long crowding | warning |
| -0.0005 .. +0.0005 | normal | none |
| -0.001 .. -0.0005 | short squeeze potential | warning |
| < -0.001 | strong squeeze potential | cap 78 if direction = short |

## When funding is unavailable

- `funding_rate = None` → `crowding_risk = unknown`, `squeeze_potential = unknown`, alignment unchanged.
- Risk agent +6 warning.

## Practical interpretation

- Funding is the cost of holding a leveraged position. Persistent positive funding = longs are paying.
- A market with positive funding and falling price means longs are getting squeezed out — leveraged liquidations cascade.
- A market with negative funding and rising price means shorts are getting squeezed — high probability of vertical melt-up.

## Related

- [[Funding_Risk]]
- [[Open_Interest]]
- [[Derivatives_Agent]]

## Implemented status

- **Implemented**.
