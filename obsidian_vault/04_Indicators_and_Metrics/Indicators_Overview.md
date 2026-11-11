# Indicators & Metrics Overview

All indicators live in [src/indicators/](../../src/indicators/) and are **deterministic** (same input → same output). No proprietary signals, no ML, no APIs.

## Implemented indicators

| Indicator | Code | Used by |
|---|---|---|
| EMA20 / EMA50 / EMA200 | `technicals.enrich_ohlcv` | regime trend, setup quality, distance gate |
| ATR14 | `technicals.atr` | invalidation, targets, extension gate |
| RSI14 | `technicals.rsi` | momentum context (mild use) |
| Volume SMA20 | `technicals.enrich_ohlcv` → `volume_sma20` | volume_ratio |
| Return 1-bar | `technicals.enrich_ohlcv` → `return_1` | breadth components |
| pct_return(N) | `technicals.pct_return` | regime + candidate returns |
| recent_range(20) | `technicals.recent_range` | support / resistance |
| trend_label | `technicals.trend_label` | regime + candidate |
| ATR percentile | `volatility.atr_percentile` | high-volatility danger flag |
| relative_strength | `relative_strength.py` | candidate ranking |
| volume_anomaly | `volume_anomaly.py` | universe ranking |
| derivatives_metrics | `derivatives_metrics.py` | crowding, alignment |

## Not implemented (Recommended)

- VWAP — see [[VWAP]].
- MACD — not used.
- Bollinger Bands — not used.
- Volume profile / market profile — not used.
- Order book depth, CVD — not collected.
- Liquidation maps — not collected.

## How indicators feed scoring

```
MomentumScannerAgent
  → trend, RS vs BTC, volume_ratio, return_24h/7d, distance_from_ema20_atr, breakouts

TechnicalSetupAgent
  → entry zone (close ± fraction of ATR), invalidation (support/resistance ± 0.15 ATR or 1.2 ATR),
    targets (close ± 1/2/3 ATR), setup_quality

ScoringAgent
  → multiplies setup_quality / momentum_score by configured weights and regime/mode multipliers

RiskAgent
  → adds penalties for extension, low volume, missing derivatives, regime conflicts
```

## Data confidence

`TradeIdeaAgent._data_confidence` reads four signals: derivatives present, catalyst present, anchor listed, derivatives listed. Returns `high` (≥4 points), `medium` (≥2), or `low`. See [[Data_Confidence]].

## Related

- [[EMA]] · [[ATR]] · [[RSI]] · [[VWAP]] · [[Volume_Anomaly]] · [[Relative_Strength]] · [[Breakout_Reclaim_Structure]] · [[Support_Resistance]] · [[Market_Structure]] · [[Open_Interest]] · [[Funding_Rate]] · [[Liquidations]] · [[Volatility]] · [[Data_Confidence]]

## Implemented status

- **Implemented** for the indicators listed in the first table. **Recommended** for the second.
