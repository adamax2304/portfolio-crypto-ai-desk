# RiskAgent

## File

[src/agents/risk_agent.py](../../src/agents/risk_agent.py).

## Role

Per-symbol risk gate. Adds explicit risk_score, risk_level, warnings, avoid lines, valid_if lines.

## Inputs

- `setups`, `candidates`, `regime`, `derivatives`, `catalysts`.

## Outputs

`dict[symbol, RiskAssessment]`:

- `risk_score` (0–100).
- `risk_level` ∈ {low, medium, high}.
- `warnings[]`, `reasons_to_avoid[]`, `valid_if[]`.

## Lift rules (verbatim)

- +10 in `transition` or `range/chop` ("breakout failure risk elevated").
- +25 in `high-volatility danger` (no fresh entries).
- +25 long in `bearish trend`.
- +20 short in `bullish trend`.
- +8 if `volume_ratio < 0.5`.
- +12 if extension > 2 ATR from EMA20.
- +14 if RR to TP1 < 1.
- +25 if no invalidation and direction in {long, short}.
- +6 if derivatives data unavailable.
- +18 if `extreme` crowding; +8 if `elevated`.
- +15 if catalyst risk_events present.

## Used by agents

- `ScoringAgent.risk_penalty += min(risk.risk_score * 0.18, 18)`.
- `TradeIdeaAgent.risk_level` inherits / overrides.
- Report renders risk block.

## Common mistakes

- Reading `risk_level = high` as "do not trade" without checking why — sometimes the lift is a single penalty that goes away after data refresh.
- Ignoring `valid_if[]` — these are the conditions to wait for.

## Future improvements

- Sector-specific risk lifts (e.g. higher for memes, lower for majors).
- Time-of-day risk lift around macro events.
- Correlation-aware risk (multiple correlated open ideas).

## Related

- [[Risk_Management_Overview]]
- [[Score_Caps]]
- [[Critic_Agent]]

## Implemented status

- **Implemented**.
