# Intraday Trade Template

Default mode. Use for 4–24h horizons.

```
# Intraday — {{symbol}} — {{date}}

## Snapshot
- Direction: {{long|short}}
- Mode: intraday
- Timeframes: 15m/1h/4h thesis, 15m execution
- Tier: {{A|B|C|rejected}}
- Score: {{score}} (caps: ...)
- Data confidence: {{high|medium|low}}

## Why intraday
- Regime: {{label}}, breadth {{above_ema20_pct}}%
- Sector / narrative: {{narrative status}}
- 24h return: {{return_24h}}%; 7d return: {{return_7d}}%
- RS vs BTC: {{relative_strength_btc}}%
- Volume ratio: {{volume_ratio}}x
- 1h setup: {{breakout|reclaim|continuation|range_fade}}

## Execution
- Entry zone: {{entry_low}} – {{entry_high}}
- Invalidation (1h close): beyond {{invalidation}}
- TP1 (1 ATR): {{tp1}}
- TP2 (2 ATR): {{tp2}}
- TP3 (optional 3 ATR): {{tp3}}
- RR to TP1: {{rr_to_tp1}}R

## Derivatives
- Funding: {{funding_rate}} ({{crowding_risk}})
- OI change: {{oi_change_pct}}%
- Interpretation: {{interpretation}}
- Cross-venue: anchor + derivatives confirmed?

## Catalyst / News
- Verified catalyst? {{yes/no}}
- Telegram attention stage: {{stage}}
- Macro risk-off / risk-on tags: {{from MacroGeopoliticsAgent}}

## Counter-thesis
- {{critic counter_thesis}}
- {{contradictions}}

## Avoid conditions
- >2 ATR away from entry
- BTC structural break against the trade
- Adverse verified catalyst
- Coverage audit reporting missing major streams

## Notes
- {{free text}}
```

## Related

- [[Intraday_Mode]]
- [[Trade_Idea_Template]]
- [[Pre_Trade_Checklist_For_LLM]]

## Implemented status

- **Template**.
