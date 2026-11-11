# Long-Term Mode (Recommended / Not Implemented)

## Status

This mode does **not exist in code**. It is documented here so LLMs do not invent it.

- `scoring.yaml.mode_weights` defines only `scalp`, `intraday`, `swing`.
- `TradeIdeaAgent._mode_normalised` forces any unknown mode to `intraday`.
- `config/universe.yaml.modes` has no `long_term` block.

If you ask the desk for "long term ideas", it will silently fall back to intraday.

## What it would be

- **Horizon**: weeks to months.
- **Timeframes**: 1d, 1w (1w currently not fetched).
- **Primary TF**: 1d.
- **Universe filter**: much higher liquidity floor; only majors + sector leaders.
- **Setup quality** would be driven by:
  - Higher-timeframe structure (200d EMA, weekly close).
  - Sector / narrative thesis (year-scale, not week-scale).
  - On-chain accumulation (not yet collected).
  - Macro context (rates, dollar, ETF flows — partially in `MacroGeopoliticsAgent`).

## What it should weight differently

- Narrative × 1.40+ — long-term is mostly thesis.
- Catalyst_news × 1.30+.
- Market_regime × 1.20+ — macro regime weighting.
- Momentum × 0.50–0.70 — short-term momentum is noise.
- Execution_quality × 0.80 — entry timing matters less.

## What would need to be built

1. A `long_term` block in `config/universe.yaml.modes` with 1d/1w timeframes and majors-only watchlist.
2. A `long_term` block in `scoring.yaml.mode_weights`.
3. Extend `TradeIdeaAgent._mode_normalised` to accept `long_term`.
4. Extend `MarketRegimeAgent` to read a weekly trend label.
5. Add a `1w` timeframe to `data.ohlcv_limit`.
6. Add a long-term review job (`review --mode long_term`) checking weekly outcomes.

## Why this is not in the MVP

The desk is a research terminal for tactical (intraday / swing) trading. Long-term positioning is closer to a thesis tracker than a trade idea generator, and benefits more from on-chain + macro data than from this desk's strengths (multi-exchange + derivatives + narrative attention).

## How to fake it today

If you must produce a long-term view, run:

```
python -m src.cli swing-report --auto-universe
```

then mentally extend the horizon. The thesis from `narrative_agent` and `catalyst_agent` survives but the targets/invalidation should be widened manually.

## Related

- [[Trading_Modes_Overview]]
- [[Implemented_vs_Recommended]]
- [[Improvement_Backlog]]

## Implemented status

- **Recommended** — not implemented anywhere in code.
