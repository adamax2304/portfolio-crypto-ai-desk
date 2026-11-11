# Volatility

## Implementation

`src/indicators/volatility.py` exposes:

- `atr_percentile(frame)` — percentile rank of latest ATR within trailing window.

## Where used

- **`MarketRegimeAgent`** — `high_vol = btc_atr_pct >= 80`. With `|btc_24h_return| > 4%`, triggers `high-volatility danger`.
- **`MarketRegime.volatility`** payload — exposes percentile + qualitative state (`elevated / normal/unknown`).

## ATR % per mode

| Mode | min_atr_percent (universe) | rationale |
|---|---|---|
| scalp | 0.12 | enough motion in 5m bars |
| intraday | 0.35 | enough motion in 1h bars |
| swing | 0.80 | enough motion in 4h bars |

These are floors. Higher ATR % usually = more risk but more opportunity.

## Reading

- ATR% rising + price expanding = volatility regime change. Re-evaluate stop sizes.
- ATR% falling for many bars = compression. Possible spring-loaded setup (see [[Low_Volatility_Compression]] — recommended wiring).

## Common mistakes

- Sizing during high ATR like during normal ATR — you bleed faster.
- Trading scalp during compression — there isn't enough motion.

## Related

- [[ATR]]
- [[High_Volatility_Regime]]
- [[Low_Volatility_Compression]]
- [[Market_Regime_Overview]]

## Implemented status

- **Implemented**.
