# Short Setup Template

```
# Short — {{symbol}} — {{date}}

## Snapshot
- Direction: short
- Tier: {{A|B|C|rejected}}
- Score: {{score}} (caps: {{cap_reasons or "none"}})
- Mode: {{scalp|intraday|swing}}
- Exchange focus: {{exchange}}
- Data confidence: {{high|medium|low}}

## Why short
- Regime: {{label}} ({{risk_mode}}); style {{recommended_style}}
- Setup tag: {{failed_breakout|reclaim_failure|breakdown|range_top}}
- Trend: {{downtrend|transition_down|range}}
- Momentum candidate score: {{candidate.score}}/100
- RS vs BTC: {{relative_strength_btc}}%
- Volume ratio: {{volume_ratio}}x
- Distance from EMA20 in ATR: {{distance_from_ema20_atr}}

## Execution
- Entry zone: {{entry_low}} – {{entry_high}} (failed bounce / retest)
- Invalidation: 1h close > {{invalidation}}
- TP1: {{tp1}}
- TP2: {{tp2}}
- TP3 (optional): {{tp3}}
- RR to TP1: {{rr_to_tp1}}R

## Derivatives
- Funding: {{funding_rate}} ({{crowding_risk}})
- OI change: {{oi_change_pct}}%
- Interpretation: {{interpretation}}
- Squeeze risk: {{squeeze_potential}}

## Catalyst / News
- Catalyst: {{catalysts list or "none verified"}}
- Verification: {{verification_status}}
- Telegram attention: {{stage}}

## Counter-thesis
- {{critic counter_thesis}}
- {{contradictions}}
- {{regime conflict if any}}

## What I am watching
- BTC / ETH structure
- Acceptance into entry zone (no chase after vertical flush)
- Volume confirming break
- Funding becoming very negative (squeeze fuel)

## Avoid conditions
- Late short after vertical flush
- Funding < -0.001 against the short (squeeze cap at 78)
- BTC reclaiming local resistance
- Setup warnings: {{top 3}}
```

## Related

- [[Trade_Idea_Template]]
- [[Long_Setup_Template]]
- [[Funding_Risk]]
- [[Pre_Trade_Checklist_For_LLM]]

## Implemented status

- **Template**.
