# Correlation Risk

## Status

The desk does **not** measure portfolio correlation. It can only compute relative strength vs BTC and breadth. Correlation discipline is **manual**.

## Practical buckets

Treat these as single-position buckets when sizing:

- **BTC + ETH** — high beta, often move together but not always.
- **SOL ecosystem** — SOL, JTO, JUP, BONK, WIF tend to correlate.
- **L2** — ARB, OP, MATIC; loosely correlate.
- **AI** — TAO, FET, RNDR, NEAR; news-driven correlation.
- **Memes** — WIF, PEPE, BONK, DOGE; attention-driven correlation.
- **DePIN / Gaming** — usually each on its own story, less correlation.

If the day's report surfaces 3 ideas across one bucket, treat them as **one** trade for risk-budget purposes.

## How to detect a high-correlation day

- `MarketRegimeAgent.alt_breadth.positive_24h_pct ≥ 80` or `≤ 20` → market is moving together.
- BTC and ETH both at new local high/low same hour → correlation tight.
- A single narrative ([[Narrative_Agent]] heatmap) is `hot` and explains most leaders.

In that environment, holding multiple longs across the same narrative is leverage on one bet.

## Practical rules

- Cap "same narrative" book at 1× your normal single-trade risk.
- Cap "two majors" (e.g. BTC + ETH) at 1.5× single-trade risk.
- In `high-volatility danger` regime, force every open idea into the same bucket regardless of label.

## Recommended (future)

- Compute pairwise rolling correlation for the watchlist universe and surface in the report.
- Auto-tag candidates with a correlation cluster ID.

## Related

- [[Risk_Management_Overview]]
- [[Sector_Overview]]
- [[Narrative_Agent]]

## Implemented status

- **Recommended / not implemented**.
