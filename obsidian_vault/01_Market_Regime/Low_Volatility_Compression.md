# Low-Volatility Compression Regime

## Status

- **Recommended / partially wired.** The label exists in [config/scoring.yaml](../../config/scoring.yaml) under `regime_weights["low-volatility compression"]`, but `MarketRegimeAgent.run` does **not** emit it today. The block of multipliers is therefore dead code unless an LLM modifies the agent.

## Intended behavior

When BTC ATR percentile is very low (≤ 20) and breadth is mid (40–60), the desk should flag compression and prefer:

- Setup × 1.15
- Momentum × 0.90
- Derivatives × 1.05

This is the "spring loaded" regime: low ATR + neutral breadth, often precedes a breakout in either direction.

## Recommended wiring

Inside the decision tree of [How_Regime_Is_Detected](How_Regime_Is_Detected.md), add a check before the `range/chop` branch:

```python
if btc_atr_pct is not None and btc_atr_pct <= 20 and 40 <= breadth_score <= 60:
    label = "low-volatility compression"
    risk_mode = "neutral"
    style = "patience; wait for expansion + confirmation"
```

## How to trade it (if you implement it)

- Watch only. Do not chase early candles of the expansion.
- Demand the first 1h close outside the compression range + volume > SMA20.
- Use the compression range high/low as invalidation.

## Related

- [[Market_Regime_Overview]]
- [[How_Regime_Is_Detected]]
- [[Improvement_Backlog]]

## Implemented status

- **Partially implemented** — config exists, agent emit logic missing.
