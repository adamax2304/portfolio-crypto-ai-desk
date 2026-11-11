# RSI

## Implementation

`technicals.rsi(series, period=14)`. Standard RSI: rolling-mean gain over rolling-mean loss.

## How the desk uses it

- Stored on each enriched frame as `rsi14`.
- Currently **not heavily relied on**. The desk does not gate setups by RSI thresholds.
- LLMs reading the report can use it as context but should not override the trend / extension / R/R checks.

## Reading

- Above 70 — overbought-ish; combine with overextension check.
- Below 30 — oversold-ish; in `bearish trend`, do not rush to long.
- Divergence detection is **not** automated.

## Common mistakes

- Treating RSI > 70 as automatic short — in a strong trend, RSI stays > 70 for days.
- Treating RSI < 30 as automatic long — same in reverse.

## Recommended improvements

- Add a `rsi_state` field to `MomentumCandidate` (`overbought / neutral / oversold`) so risk-agent can warn on chasing into stretched RSI.

## Related

- [[Indicators_Overview]]
- [[Momentum_Scanner_Agent]]

## Implemented status

- **Implemented** (computed) / **Partially implemented** (not gating anything yet).
