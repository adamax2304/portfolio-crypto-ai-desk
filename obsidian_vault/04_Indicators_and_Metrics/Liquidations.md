# Liquidations

## Status

**Not collected.** The desk does not have a liquidation data feed.

The README is explicit about this: "still does not pretend to have liquidation maps, paid social sentiment, on-chain flows".

## What this means

- The desk cannot see liquidation clusters or recent liquidation spikes.
- Liquidation risk is inferred indirectly via funding + OI + extension. See [[Funding_Risk]] and [[Open_Interest_Risk]].

## Recommended sources (paid)

- CoinGlass (key reserved in `.env.example`).
- Coinalyze.
- Hyblock.

A future collector would pull liquidation totals + clusters per symbol per timeframe, and emit:

- A `liquidation_pressure` field on `DerivativesSummary`.
- A flag when price approaches a large liquidation cluster.

## How to compensate manually

- Treat funding + OI signals more strictly.
- After a sharp move against funding (e.g. price down with positive funding), assume liquidations were heavy and expect a relief bounce.

## Related

- [[Indicators_Overview]]
- [[Funding_Risk]]
- [[Improvement_Backlog]]

## Implemented status

- **Recommended / not implemented**.
