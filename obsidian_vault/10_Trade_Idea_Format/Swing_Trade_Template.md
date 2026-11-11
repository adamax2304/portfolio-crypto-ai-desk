# Swing Trade Template

Use for 2–7 day horizons.

```
# Swing — {{symbol}} — {{date}}

## Snapshot
- Direction: {{long|short}}
- Mode: swing
- Timeframes: 1h/4h/1d thesis, 4h execution
- Tier: {{A|B|C|rejected}}
- Score: {{score}} (caps: ...)
- Data confidence: {{high|medium|low}}

## Why swing
- Regime: {{label}} — alignment is structurally weighted ×1.15
- Narrative: {{narrative status}} (×1.30 in swing)
- Catalyst pipeline: {{listings|mainnet|partnership|unlock}}
- 7d return: {{return_7d}}%
- 4h structure: {{higher_highs|lower_lows|consolidation}}

## Execution
- Entry zone: {{entry_low}} – {{entry_high}}
- Invalidation (4h close): beyond {{invalidation}}
- Time-risk: re-evaluate at every 4h close
- TP1 (1 ATR on 1h... revise to 4h): {{tp1}}
- TP2: {{tp2}}
- TP3: {{tp3}}
- Suggested R/R: ≥ 2.5 to TP2

## Derivatives (swing-relevant)
- Funding: {{funding_rate}} (less critical than intraday/scalp)
- OI multi-day trend: {{from Bybit history}}
- Cross-venue agreement: anchor + Bybit confirm?

## Catalyst / News
- Verified pipeline in next 7 days? {{listing|mainnet|partnership}}
- Risk events (unlock/delisting/migration) in next 7 days?
- News importance score: {{number}}

## Counter-thesis
- Late narrative entry risk
- Macro shift could invalidate
- {{critic counter_thesis}}

## Avoid conditions
- Within 48h of confirmed token unlock
- Within 24h of major macro event (CPI, FOMC)
- Narrative cooling (heat_score down ≥ 20)
- BTC regime flips against the trade

## Notes
- {{free text}}
```

## Related

- [[Swing_Mode]]
- [[Trade_Idea_Template]]
- [[Token_Unlocks]]
- [[Narrative_Heatmap]]

## Implemented status

- **Template**.
