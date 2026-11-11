# Stock Intraday Mode

Horizon: same session to ~24 hours.
Run: `python -m src.cli stocks-intraday-report`

## Timeframes

- Execution: 15m
- Context: 1h
- Daily for prev-day H/L

## Priorities (scoring multipliers)

- `technical_setup` ×1.10
- `volume_relative_volume` ×1.15 — relative volume is the lifeblood of intraday
- `news_catalyst` ×1.10
- `relative_strength` ×1.05
- `earnings_risk_adjustment` ×0.80 — intraday can trade reactions, less harsh

## Required confirmations for A-tier

1. SPY/QQQ direction agrees with the trade.
2. Sector ETF status agrees.
3. Last close has cleared prev-day high (long) or low (short).
4. Relative volume > 1.0 (Stage 7 addition).
5. ATR/price ≥ 0.5% — enough movement to matter.
6. Clean invalidation level.

## Common rejects

- Range trend (`no_directional_setup` block).
- ATR/price < 0.5% — nothing to trade.
- Price > 2 ATR from planned entry (chasing).
- Missing invalidation.

## Earnings handling

Allowed to trade reactions, but **must** acknowledge in the thesis: "trading earnings reaction post-AMC release." Otherwise the idea is flagged high-risk and demoted.

## Recommended discipline

Intraday is the loudest mode in terms of false signals. The system caps `volume_relative_volume` raw at 0.5 in the MVP because we don't have rolling 20-bar relative volume yet — when Stage 7 wires that, expect tier distributions to shift. Until then, be skeptical of intraday A-tier ideas without a clear catalyst.
