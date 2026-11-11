# Exchange Overview

The desk operates across three exchanges (configured in [config/exchanges.yaml](../../config/exchanges.yaml)). Each has a **role**, a **trust weight**, and explicit caps/flags.

## Roles

| Exchange | Role | trust | weight | high_risk | market_types |
|---|---|---|---|---|---|
| binance | anchor | 0.95 | 1.00 | no | spot |
| bybit | derivatives | 0.85 | 0.85 | no | spot + linear |
| mexc | discovery | 0.50 | 0.55 | **yes** | spot |

## Data flows

```
Stage 1 (universe):
  binance → universe/binance.json
  bybit   → universe/bybit.json
  mexc    → universe/mexc.json
  fused   → exchange_symbol_map.json + universe_ranked_candidates.json

Stage 2 (rank):
  per-mode ranked candidates (universe_ranked_candidates_<mode>.json)

OHLCV:
  binance (anchor) → data/raw/ohlcv/binance/<tf>/<SYMBOL>.csv
  bybit            → data/raw/ohlcv/bybit/<tf>/<SYMBOL>.csv
  mexc             → data/raw/ohlcv/mexc/<tf>/<SYMBOL>.csv

Derivatives:
  binance USD-M    → binance_futures_latest.json
  bybit linear     → bybit_derivatives_latest.json (history)
  bybit + okx      → multi_exchange_derivatives_latest.json (snapshot)
```

## Exchange fusion

`ExchangeFusionAgent` builds per-symbol confirmation:

- `anchor_listed` — listed on binance.
- `derivatives_listed` — listed on any non-anchor / non-high_risk venue (currently bybit).
- `discovery_listed` — listed on any high_risk venue (currently mexc).
- `high_risk_only` — listed **only** on high_risk venues.
- `price_consistency` — agreement of 24h price change across listed venues.
- `volume_consistency` — agreement of volume anomaly across venues.
- `confirmation_score` — 0–100 composite.
- `best_exchange_for_data` — anchor if listed, else highest liquidity venue.
- `suggested_exchange_focus` — anchor → derivative venue → any non-high-risk → any.
- `risk_flags` — `mexc_only`, `not_on_anchor`, `no_derivatives_confirmation`, `price_divergence_across_exchanges`.

## How fusion affects scoring

- `high_risk_only` → cap 70 (65 if structure weak).
- Not anchor + not high_risk_only → cap 75.
- Both → cap is the lower; cap_reasons logged.

## Related

- [[Binance_Role]]
- [[Bybit_Role]]
- [[MEXC_Role]]
- [[Cross_Exchange_Confirmation]]
- [[MEXC_Only_Risk]]
- [[Bybit_Derivatives_Confirmation]]
- [[Exchange_Data_Confidence]]
- [[Exchange_Failure_Handling]]
- [[Exchange_Fusion_Agent]]

## Implemented status

- **Implemented**.
