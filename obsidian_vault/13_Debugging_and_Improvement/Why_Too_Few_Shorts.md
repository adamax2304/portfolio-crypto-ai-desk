# Why Too Few Shorts

Mirror of [[Why_Too_Many_Longs]]. Shorts are structurally penalized in `bullish trend` (alignment 0.25).

## Diagnostic

- Check regime label. In bullish trend with breadth ≥ 55, shorts should be rare.
- Check setup warnings — "Short setup fights a bullish tape" is the typical warning.

## When too few shorts is wrong

- Regime is `bearish trend` (breadth ≤ 40 + BTC downtrend) but desk produces few shorts.
  - Likely: many candidates extended > 2 ATR (already flushed).
  - Or: most candidates are MEXC-only → capped, become C.
  - Or: derivatives data is missing widely → derivative component flat → setups don't reach 65.

## Pattern recognition

- In the early hours of a downturn, the desk often shows 0–2 shorts because the move is extended and entries lack acceptance.
- After a 24h sideways consolidation in a bear regime, shorts start surfacing on retests.

## What to do

- Wait for retest setups, not first-break entries.
- Watchlist monitor will surface upgrades when retests confirm.

## Don't

- Don't force shorts in `bullish trend`.
- Don't lower thresholds to surface more shorts.

## Related

- [[Market_Regime_Overview]]
- [[Long_Short_Neutral_Bias]]
- [[Why_Too_Many_Longs]]

## Implemented status

- **Diagnostic guide**.
