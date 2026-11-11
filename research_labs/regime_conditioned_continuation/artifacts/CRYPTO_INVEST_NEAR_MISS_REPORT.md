# Crypto Invest Near-Miss Monitor

This is an isolated diagnostic dataset. It never writes Paper, live, or official PnL tables.
- Database: `C:\Users\adama\Documents\crypto-ai-desk\research_labs\regime_conditioned_continuation\near_miss.sqlite`
- Recorded near-miss snapshots: 5607
- All counterfactual outcomes are diagnostic proxies and excluded from official metrics.

## Rejection Funnel

| Failed stage | Reason | Count |
|---|---|---:|
| RSI_RESET | RSI_RESET_NOT_CONFIRMED | 3079 |
| LOWER_TF_RECLAIM | NO_CLOSED_RECLAIM_CONFIRMATION | 1648 |
| ENTRY_GEOMETRY | ENTRY_CHASE_EXTENSION | 294 |
| RELATIVE_STRENGTH | RELATIVE_STRENGTH_BELOW | 212 |
| BTC_REGIME | BTC_REGIME_NOT_ALIGNED | 143 |
| FVG_QUALITY | FVG_INVALIDATED_ON_FIRST_RETEST | 117 |
| STOP_GEOMETRY | STOP_GEOMETRY_OUT_OF_BOUNDS | 107 |
| SYMBOL_EXPOSURE | SYMBOL_POSITION_ALREADY_OPEN | 4 |
| VOLATILITY | VOLATILITY_COMPRESSED | 2 |
| DATA_QUALITY | FORWARD_EXECUTION_OR_LATENCY_DIRTY | 1 |

## Proxy Outcomes

| Horizon | Status | First event | Count |
|---:|---|---|---:|
| 4h | DATA_UNAVAILABLE | - | 8 |
| 4h | PENDING | - | 139 |
| 4h | RESOLVED | TP1_BEFORE_STOP | 1844 |
| 4h | RESOLVED | STOP_BEFORE_TP1 | 1562 |
| 4h | RESOLVED | NO_1R_EVENT | 1538 |
| 24h | DATA_UNAVAILABLE | - | 8 |
| 24h | PENDING | - | 1023 |
| 24h | RESOLVED | TP1_BEFORE_STOP | 2267 |
| 24h | RESOLVED | STOP_BEFORE_TP1 | 1751 |
| 24h | RESOLVED | NO_1R_EVENT | 42 |
| 72h | DATA_UNAVAILABLE | - | 8 |
| 72h | PENDING | - | 4872 |
| 72h | RESOLVED | TP1_BEFORE_STOP | 114 |
| 72h | RESOLVED | STOP_BEFORE_TP1 | 97 |
