# Market Regime Overview

Regime is the **first agent that runs** in every report and every watchlist tick. It frames every subsequent decision: scoring multipliers, allowed direction, no-trade conditions.

## Why it matters

- Wrong regime call → systematic loss across all ideas.
- Regime defines whether the desk wants longs, shorts, or no trades.
- Regime drives the per-component scoring multipliers in [config/scoring.yaml](../../config/scoring.yaml).

## Inputs

`MarketRegimeAgent.run` consumes the raw OHLCV frames already loaded by `Supervisor`. It computes:

- BTC trend (uptrend / downtrend / transition_up / transition_down / range / unknown). Uses EMA20/50 cross on the **regime timeframe** (`config/settings.yaml.execution.regime_timeframe`, default `4h`).
- ETH trend (same logic).
- BTC 24h return on the regime timeframe.
- Breadth across the loaded universe: % above EMA20, % above EMA50, % positive 24h, % outperforming BTC.
- BTC ATR percentile (high if ≥ 80).

## Labels (exact strings used in scoring.yaml)

- `bullish trend`
- `bearish trend`
- `range/chop`
- `transition`
- `high-volatility danger`
- `low-volatility compression` (label key exists in scoring.yaml; not currently emitted by `MarketRegimeAgent` — see Known gap below).

See [[How_Regime_Is_Detected]] for the exact decision tree.

## Output

A `MarketRegime` model:

- `label` — one of the strings above.
- `confidence` — 0–100.
- `risk_mode` — `risk-on / risk-off / neutral / mixed / danger`.
- `recommended_style` — short prose ("selective longs; prefer pullbacks on relative strength", etc.).
- `btc_trend`, `eth_trend`.
- `alt_breadth` — dict of percentages.
- `volatility` — BTC ATR percentile + qualitative state.
- `key_levels` — BTC/ETH local support/resistance.
- `warnings` — when BTC or ETH data is missing.

## How it shapes downstream scoring

- Each regime has its own multiplier block in `scoring.yaml.regime_weights`:
  - `bullish trend` boosts momentum (×1.25) and setup (×1.10), reduces derivatives weight slightly.
  - `bearish trend` boosts momentum + setup, mutes catalyst_news and narrative.
  - `range/chop` mutes momentum hard (×0.75) and boosts execution_quality (×1.20).
  - `transition` mutes momentum mildly, boosts derivatives.
  - `high-volatility danger` boosts derivatives + execution_quality, mutes momentum and narrative.
- Each setup is checked for direction conflict with regime in [[Technical_Setup_Agent]] and [[Risk_Agent]] — penalties applied to score.

## How to use in trade decisions

- In `bullish trend` → prefer longs, treat shorts as countertrend (cap them mentally to B-tier even if scored higher).
- In `bearish trend` → prefer shorts, do not chase altcoin longs.
- In `range/chop` → demand cleaner structure; momentum is muted by design.
- In `transition` → demand confirmation; cap your size mentally.
- In `high-volatility danger` → reduce size or skip; the desk recommends "reduce size or no trade until structure settles".

## Known gap

The `low-volatility compression` label exists in `scoring.yaml.regime_weights` but `MarketRegimeAgent.run` does not currently emit it. The dead branch is harmless (no symbol carries that label, so the multipliers are unused), but it should either be wired up or removed. See [[Low_Volatility_Compression]].

## Related

- [[How_Regime_Is_Detected]]
- [[Bullish_Regime]]
- [[Bearish_Regime]]
- [[Neutral_Chop_Regime]]
- [[Transition_Regime]]
- [[High_Volatility_Regime]]
- [[Low_Volatility_Compression]]
- [[Long_Short_Neutral_Bias]]
- [[How_Regime_Affects_Scoring]]
- [[Regime_Debugging]]

## Used by agents

`ScoringAgent`, `TechnicalSetupAgent`, `RiskAgent`, `TradeIdeaAgent`, `NarrativeAgent`, every report builder.

## Common mistakes

- Trading a regime that the desk has not actually labeled (e.g. assuming "bullish" because BTC rallied 1 hour ago — the agent uses 4h trend and breadth).
- Ignoring breadth — strong BTC + weak breadth = `transition`, not `bullish trend`.

## Future improvements

- Wire `low-volatility compression` properly when BTC ATR percentile ≤ 20.
- Add explicit BTC-dominance and stablecoin-dominance reads.
- Add fast intraday regime (15m) overlay so scalpers don't rely on a 4h call.

## Implemented status

- **Implemented** (with one dead label noted above).
