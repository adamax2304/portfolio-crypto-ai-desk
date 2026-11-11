# Stock Risk Management

[src/stocks/agents/risk_agent.py](../../src/stocks/agents/risk_agent.py) combines regime / sector / RS / earnings / structure inputs into a per-symbol risk assessment with **flags**, a **penalty**, and **blocks**.

## Penalties (config/stocks/scoring.yaml → risk_penalties)

| Trigger | Penalty |
|---|---|
| earnings_today | -20 |
| earnings_next_session | -12 |
| earnings_within_3_days_for_swing | -10 |
| gap_unfilled_recent | -8 |
| contradicts_index_trend | -8 |
| contradicts_sector_trend | -6 |
| low_relative_volume | -6 |
| weak_relative_strength | -6 |
| no_clean_invalidation | -10 |
| macro_event_imminent | -8 |
| overextended_post_gap | -6 |

Penalties stack. The final score = base_components + sum(applied_penalties).

## Blocks (force rejection)

A symbol is tagged `tier=rejected` regardless of score when **any** block fires:

- `no_invalidation` — no clean stop level produced by the technical agent
- `no_directional_setup` — trend is range
- `earnings_today_blocks_swing` (swing mode only)
- `earnings_blocks_swing_entry` (swing mode, earnings ≤2 days out)

## Liquidity gates (config/stocks/risk.yaml → liquidity)

- `min_avg_dollar_volume_30d: 25_000_000`
- `min_price: 5.0` (avoid penny stocks)
- `reject_if_relative_volume_lt: 0.5`

The MVP doesn't enforce avg dollar volume yet (would require a separate metric collector). The price floor and relative volume floor will be enforced in Stage 7.

## Gap rules

- Symbols that gapped >5% in the last session require pullback/retest before entry — no immediate chasing.
- Symbols with >10% gap = no entry without a clear setup (overextension).

## Macro event awareness

`config/stocks/risk.yaml → macro.events_of_note` lists what triggers macro caution: CPI, PPI, FOMC, NFP, Powell, ECB. If a macro event is within 4 hours, the trade is flagged `high_risk_warning`. Stage 7 adds a `data/manual/stocks/macro_calendar.csv` collector to drive this automatically.

## Why these defaults

These numbers came from common-sense desk policy, not backtest fitting. After ~30 stocks signals are tracked, run `signal-stats --asset-class stocks` and tune the rules that the data tells you to. **Never auto-tune.** The signal-tracking module is observation-only by design.
