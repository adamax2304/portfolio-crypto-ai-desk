# Long Setup Template

Use for long-direction ideas that are A/B-tier active or being evaluated.

```
# Long — {{symbol}} — {{date}}

## Snapshot
- Direction: long
- Tier: {{A|B|C|rejected}}
- Score: {{score}} (caps: {{cap_reasons or "none"}})
- Mode: {{scalp|intraday|swing}}
- Exchange focus: {{exchange}}
- Data confidence: {{high|medium|low}}

## Why long
- Regime: {{label}} ({{risk_mode}}); style {{recommended_style}}
- Setup tag: {{breakout|reclaim|pullback|range_expansion|continuation}}
- Trend: {{uptrend|transition_up|range}}
- Momentum candidate score: {{candidate.score}}/100
- RS vs BTC: {{relative_strength_btc}}%
- Volume ratio: {{volume_ratio}}x
- Distance from EMA20 in ATR: {{distance_from_ema20_atr}}

## Execution
- Entry zone: {{entry_low}} – {{entry_high}}
- Invalidation: 1h close < {{invalidation}}
- TP1 ({{TP1_distance}} ATR): {{tp1}}
- TP2 ({{TP2_distance}} ATR): {{tp2}}
- TP3 (optional): {{tp3}}
- RR to TP1: {{rr_to_tp1}}R

## Derivatives
- Funding: {{funding_rate}} ({{crowding_risk}})
- OI change: {{oi_change_pct}}%
- Interpretation: {{interpretation}}

## Catalyst / News
- Catalyst: {{catalysts list or "none verified"}}
- Verification: {{verification_status}}
- Telegram attention: {{stage}} from CrowdAttentionAgent

## Counter-thesis
- {{critic counter_thesis}}
- {{top contradictions}}
- {{regime conflict if any}}

## What I am watching
- BTC / ETH structure around local S/R
- Acceptance into entry zone (no chase)
- Volume on retest
- Funding / OI for crowding shift

## Avoid conditions
- >2 ATR away from planned entry
- BTC breakdown
- Adverse Telegram catalyst (verified)
- Setup warnings: {{top 3}}
```

## Related

- [[Trade_Idea_Template]]
- [[Short_Setup_Template]]
- [[Stop_Loss_Logic]]
- [[Pre_Trade_Checklist_For_LLM]]

## Implemented status

- **Template**.
