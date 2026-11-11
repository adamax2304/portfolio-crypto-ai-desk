# Risk Management Overview

The desk has **two layers** of risk handling:

1. **In-code, enforced** — score caps, no-invalidation rejection, stale-data rejection, MEXC cap, freshness cap, RiskAgent / CriticAgent penalties.
2. **Off-code, manual** — position sizing, time stops, portfolio-level correlation, capital allocation.

This vault treats the in-code layer as facts and the manual layer as **rules of practice** the operator must follow.

## Layer 1 — enforced by code

| Mechanism | Where | Effect |
|---|---|---|
| No invalidation cap | `ScoringAgent` | score ≤ 50, tier = rejected |
| Stale data cap | `ScoringAgent` | score ≤ 50, tier = rejected if freshness > 180 min |
| MEXC-only cap | `ScoringAgent` | score ≤ 70 (65 if weak structure) |
| Not on anchor exchange | `ScoringAgent` | score ≤ 75 |
| Low liquidity | `ScoringAgent` | score ≤ 60 |
| Unverified rumor cap | `ScoringAgent` | score ≤ 55 |
| Extreme adverse funding | `ScoringAgent` | score ≤ 78 |
| Regime conflict penalty | `ScoringAgent` | −8 |
| Overextended penalty | `ScoringAgent` | −8 |
| Poor R/R penalty | `ScoringAgent` | −10 |
| No-invalidation penalty | `ScoringAgent` | −15 (in addition to cap) |
| Missing derivatives | `ScoringAgent` | −2 |
| Missing news | `ScoringAgent` | −2 |
| Too many warnings (≥3) | `ScoringAgent` | −5 |
| RiskAgent risk-level lift | `TradeIdeaAgent` | `risk_level = high` in `high-volatility danger` |
| Watchlist convert | `TechnicalSetupAgent` | If extension > 2.5 ATR, force `watchlist_only` |
| Direction conflict warning | `TechnicalSetupAgent` | Long-in-bearish / short-in-bullish |

See [[Score_Caps]] for the full cap table and order of operations.

## Layer 2 — operator rules

These are not in code. Follow them as written here.

1. **Per-trade risk**: never risk more than 1% of account on a single trade. Smaller on scalps, smaller in `high-volatility danger`.
2. **Per-day risk**: cap total open risk at 3% of account. Stop adding ideas after 3 losers.
3. **Per-mode book**: keep scalp / intraday / swing as separate notional buckets. Don't let a "stretched scalp" eat your swing risk.
4. **Correlation**: SOL + SOL-ecosystem alts move together. Treat 3 SOL-ecosystem ideas as 1 idea for risk.
5. **Time stop**: if no progress in the planned holding window, exit. The desk does not force this.
6. **Hard exchange-down stop**: if the exchange your position is on degrades (depth, deposit, withdrawals), close. `coverage_audit` will warn about data; you must act on positions.
7. **News stop**: if a verified bearish catalyst hits against you, close before re-evaluating.
8. **Funding stop**: if funding turns adversarial mid-trade beyond `±0.001`, treat it as a warning to reduce.

## Net effect

The system biases toward **fewer good trades**. By design, on most days the report will show 0–2 A/B-tier ideas and a longer rejected list. That is the correct shape.

## Related

- [[Score_Caps]]
- [[No_Trade_Conditions]]
- [[Risk_Agent]]
- [[Position_Sizing]]
- [[Stop_Loss_Logic]]

## Implemented status

- **Implemented** (layer 1) / **Partially implemented** (layer 2 = manual).
