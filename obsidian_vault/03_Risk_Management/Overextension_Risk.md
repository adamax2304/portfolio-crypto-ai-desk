# Overextension Risk

## Metric

`distance_from_ema20_atr = (close - ema20) / atr14` (signed). Used in `MomentumScannerAgent` and consumed by `RiskAgent` + `TechnicalSetupAgent`.

## Thresholds

| Absolute distance | Effect |
|---|---|
| `> 2` | RiskAgent +12, "Move is extended more than 2 ATR from EMA20" |
| `> 2` | ScoringAgent setup_quality −14, warning "Entry quality is weak because the move is extended" |
| `> 2.5` | TechnicalSetupAgent converts to `watchlist_only`, warning "Converted to watchlist only: wait for pullback" |

So a symbol that ran > 2.5 ATR away from EMA20 cannot produce an A/B trade until it pulls back.

## Why this exists

Chasing extended moves is the #1 way casual traders feed the desk's enemies (squeezes, funding traps). The hard gate is intentional.

## How to use it

- If `distance > 2`, wait for a pullback into EMA20 ± 0.5 ATR.
- If `distance > 2.5`, the desk will only quote you a conditional watchlist plan, not an active idea.
- For shorts, the same logic applies symmetrically (extended down moves).

## Edge case — relief rallies

In a `bearish trend` regime, a sharp counter-trend bounce can briefly push `distance > 2`. Don't read that as "short here" — wait for the bounce to fail and `distance` to recover toward 1.

## Common mistakes

- Trading the breakout candle of an already-extended move because "the catalyst is strong" — the desk still rejects it.
- Sizing larger to "make up" for a worse entry — that compounds the wrong way.

## Related

- [[ATR]]
- [[Momentum_Scanner_Agent]]
- [[Technical_Setup_Agent]]
- [[Risk_Agent]]

## Implemented status

- **Implemented**.
