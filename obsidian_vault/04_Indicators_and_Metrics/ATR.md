# ATR (Average True Range)

## Implementation

`technicals.atr(frame, period=14)` — true range rolling-mean.

True range = `max(high-low, |high - prev_close|, |low - prev_close|)`.

## Where the desk uses it

- **Invalidation** — 1.2 ATR fallback, support/resistance ± 0.15 ATR preferred.
- **Targets** — TP1 = ±1 ATR, TP2 = ±2 ATR, TP3 = ±3 ATR.
- **Entry zone** — `close ± 0.2..0.65 ATR`.
- **Extension gate** — `distance_from_ema20_atr` uses ATR as denominator.
- **Universe filter** — `min_atr_percent` per mode (0.12 scalp / 0.35 intraday / 0.80 swing).
- **Regime danger** — `atr_percentile ≥ 80` is the high-vol gate.

## ATR percentile

`volatility.atr_percentile(frame)` ranks the latest ATR vs its trailing window. `≥ 80` = elevated; flags `high-volatility danger` when combined with > 4% BTC move.

## Reading

- ATR % = (ATR / close) × 100. Higher % means choppier; tight stops are harder.
- Sudden ATR expansion = volatility regime shift. Past stop sizes may no longer be relevant.

## Common mistakes

- Using a fixed dollar stop instead of ATR-based — the same dollar amount is too tight on a high-ATR asset and too wide on a low-ATR one.
- Trading scalp on a symbol with ATR % < 0.12 — universe filter already prevents this, but if you bypass it, you'll bleed fees and spread.

## Related

- [[Indicators_Overview]]
- [[Invalidation]]
- [[Risk_Reward]]
- [[Overextension_Risk]]
- [[Volatility]]

## Implemented status

- **Implemented**.
