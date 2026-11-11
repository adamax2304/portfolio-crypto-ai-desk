# Watchlist Template

For C-tier ideas — interesting but not entry-ready.

```
# Watchlist — {{symbol}} — {{date}}

## Snapshot
- Tier: C
- Score: {{score}} (caps: {{cap_reasons or "none"}})
- Direction bias: {{long|short}} (from setup; activated only on upgrade)
- Mode: {{scalp|intraday|swing}}
- Exchange focus: {{exchange}}
- Data confidence: {{high|medium|low}}

## Why watch, not trade
- {{primary reason from cap_reasons or thesis}}
- {{relevant warnings}}

## Conditional setup
- Conditional entry zone: {{entry_low}} – {{entry_high}}
- Potential invalidation: {{invalidation}}
- Conditional TP1 / TP2 / TP3: {{tp1}} / {{tp2}} / {{tp3}}

## Conditions for activation
- BTC / ETH structure that supports the direction
- Volume confirmation (volume_ratio ≥ 1.5)
- Funding normalization if currently extreme
- Verified catalyst if currently rumor-only
- Anchor exchange listing if currently MEXC-only

## Monitor signals
- Watchlist monitor (`monitor-watchlist`) is auto-tracking this name
- Telegram alert will fire on C → B/A upgrade with SL line

## My note
- {{free-text observation about what could turn this into an active idea}}
```

## Related

- [[C_Tier_Watchlist_Setups]]
- [[Watchlist_Monitor_Agent]]
- [[Trade_Idea_Template]]

## Implemented status

- **Template**.
