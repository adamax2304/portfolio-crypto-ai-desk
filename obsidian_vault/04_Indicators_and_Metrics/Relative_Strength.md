# Relative Strength

## Source

`src/indicators/relative_strength.py`. Computes symbol return − BTC return over a window. Surface metric: `relative_strength_btc` on each `MomentumCandidate`.

## Where it is used

- **Universe ranking** — RS contributes to opportunity score.
- **Regime breadth** — `outperforming_btc_pct`.
- **`TradeIdeaAgent` evidence** — quoted in the report.
- **`ScoringAgent` indirectly** via momentum component (RS feeds candidate.score).

## Reading

- Positive RS → symbol outperforming BTC in the chosen window.
- Negative RS → underperforming.
- The desk does **not** auto-prefer high-RS longs in `bearish trend` (the regime mute on momentum keeps that honest), but it does help separate leaders from laggards in `bullish trend`.

## Useful patterns

- **Leader rotation**: top-RS names in a bull tape, especially in a hot narrative, tend to continue.
- **Laggard short**: bottom-RS names in a bearish tape often produce clean continuation shorts.
- **Mean-reverter**: extreme negative RS combined with `fear_capitulation` crowd stage can be an early-attention long — but the desk caps confidence here.

## Common mistakes

- Buying because "RS is positive" without checking trend / extension.
- Treating RS as static — it shifts hour-by-hour, especially on alts.

## Related

- [[Indicators_Overview]]
- [[Momentum_Scanner_Agent]]
- [[Market_Regime_Overview]]
- [[Sector_Overview]]

## Implemented status

- **Implemented**.
