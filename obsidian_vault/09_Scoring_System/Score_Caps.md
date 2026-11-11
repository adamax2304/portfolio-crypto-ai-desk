# Score Caps

The most important page on this topic.

## Definition

A score cap is a **hard ceiling** applied after weights + penalties. If the total exceeds the cap, the score is set to the cap and `cap_reasons` records why.

When multiple caps fire, the **lowest cap value wins**, and `cap_reasons` lists every reason that matches that minimum value.

## Cap table (in evaluation order in `ScoringAgent`)

| Condition | Cap value | Side-effects |
|---|---|---|
| No clean invalidation AND direction ∈ {long, short} | 50 | Tier forced to `rejected` |
| Direction not in {long, short, watchlist_only, no_trade} | 50 | unsupported direction tag |
| MEXC-only listing | 70 | (lowered to 65 if technical_setup component < 14) |
| Not on anchor exchange (AND not MEXC-only) | 75 | reduced data confidence |
| Low liquidity (RiskAgent warns) | 60 | |
| Stale data (>180 min freshness) | 50 | Tier forced to `rejected` |
| Catalyst contains "rumor" AND verification ∈ {none, rumor, single_source} AND no risk_events | 55 | |
| Funding > +0.001 AND direction == long | 78 | |
| Funding < -0.001 AND direction == short | 78 | |

## Implications

- A cap at 50 forces rejected tier. Two caps trigger that: no-invalidation and stale data.
- A cap at 55 means it cannot reach B (65) and definitely cannot reach A (80).
- A cap at 60/65/70 limits how high a setup can go. Often pins the score at the cap exactly.
- A cap at 75 still allows B (65) but blocks A.
- A cap at 78 also blocks A.

## How caps interact with risk_penalty

Caps apply **after** `total = sum(components) - risk_penalty`. If total < cap, the cap doesn't fire.

Example:

```
components total = 76
risk_penalty = 6
total = 70
MEXC-only cap = 70
→ score remains 70 (cap_reasons reports the cap; line "Score capped at 70 (...)" added to reasons)
```

## Tier interaction (in `ScoringAgent`)

```python
invalidation_missing = any("invalidation" in r.lower() for r in cap_reasons)
stale_cap = any("stale" in r.lower() for r in cap_reasons)
if invalidation_missing or stale_cap:
    tier = "rejected"
elif direction in {long, short} and total >= 80 and not caps:
    tier = "A"
elif direction in {long, short} and total >= 65:
    tier = "B"
elif total >= 50:
    tier = "C"
else:
    tier = "rejected"
```

Note: even a 90 score is **NOT** A-tier if any cap is active. The `and not caps` clause enforces this.

## Operator rules

- **Never override a cap.** Caps are global. If you think a cap should be removed, change the config or the agent, do not mentally cheat.
- **A cap is information, not a barrier.** It tells you what specifically is missing.
- **The cap is the new score ceiling.** Targets / sizing should respect the lower number.

## Configuring caps

There's no per-cap config switch in `scoring.yaml` today. Cap values are hard-coded constants in `ScoringAgent`. Changing them requires editing the agent.

Recommended improvement: move cap values to `scoring.yaml.thresholds` so they're configurable.

## Related

- [[Scoring_Overview]]
- [[No_Trade_Conditions]]
- [[Rejected_Setups]]
- [[MEXC_Only_Risk]]
- [[Funding_Risk]]

## Implemented status

- **Implemented**.
