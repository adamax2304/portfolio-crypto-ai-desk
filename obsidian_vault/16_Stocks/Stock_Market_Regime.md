# Stock Market Regime

Classification is done by [src/stocks/agents/market_regime_agent.py](../../src/stocks/agents/market_regime_agent.py) from daily OHLCV of SPY, QQQ, IWM, DIA (+ ^VIX if available).

## Labels

- **bullish** — all 4 indices in uptrend, breadth ≥ 0.75 above EMA20. Bias = long.
- **risk_on** — ≥3/4 indices uptrending, breadth ≥ 0.5, VIX not elevated. Bias = long.
- **risk_off** — ≥3/4 indices in downtrend OR breadth ≤ 0.25. Bias = short.
- **high_volatility** — VIX ≥ 25. Bias = neutral; widen stops, halve size.
- **low_volatility** — VIX ≤ 14, and ≥2 indices uptrending. Bias = long.
- **transition** — mixed: at least one up and one down trend.
- **chop** — no clear trend across indices, breadth in the 0.25–0.5 band.
- **unknown** — no index data available; abstain.

## How each label changes scoring

The label maps to multipliers in `config/stocks/scoring.yaml → regime_weights`:

- `risk_off` boosts `relative_strength` (winners stand out) and `earnings_risk_adjustment` (more cautious about events), discounts `technical_setup` (breakdowns common).
- `bullish` slightly boosts both `relative_strength` and `technical_setup`.
- `chop` discounts `technical_setup` (breakouts fail), boosts `volume_relative_volume` (need confirmation).
- `high_volatility` boosts `risk_reward` (need bigger reward) and `earnings_risk_adjustment`.

## Hard rules

- In `risk_off`, a long requires the symbol to be RS-classified as **leader** (top tier). Otherwise the trade gets demoted to watchlist.
- In `bullish`, shorts need an explicit catalyst — don't fight the trend without cause.
- In `high_volatility`, ATR-based stops must be widened (the technical agent already uses ATR; the risk agent flags `require_widened_stops`).

## Bias is not destiny

A `risk_off` label biases short, but if you have a single mega-cap with leader-grade RS and a clean breakout setup, that's a valid long. The bias is a default; per-symbol RS and structure override.
