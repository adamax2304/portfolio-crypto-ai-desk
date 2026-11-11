# Context Filters Status

- as of: `2026-11-11T20:28:40.665742+00:00`
- config: `context_filters_v1`; live: **LOCKED**

| filter | Paper routing | current state | evidence rows |
|---|---:|---|--:|
| stablecoin depeg | yes | UNKNOWN / insufficient_fresh_peg_venues | 78383 |
| cross-exchange consistency | yes | BTC/USDT:unknown/FULL_SIZE, ETH/USDT:unknown/FULL_SIZE | 347641 |
| token unlock | no (shadow) | DefiLlama public calendar fallback | 97677 |
| crypto IV-RV | no (advisory) | Deribit DVOL | 1644 |
| stocks GEX | no (shadow) | provisional yfinance OI/IV gamma proxy | 485 |
| insider cluster | no (shadow confirmation) | Form 4 code P | 343 |
| Catalyst RS overnight | no (counterfactual) | eligible 0, resolved 0 | 0 |

## Source health

- `context:cross_exchange_quotes`: error; failures=7; last_success=2026-11-11T20:12:54.126853+00:00
- `context:deribit_dvol`: ok; failures=0; last_success=2026-11-11T20:14:02.765632+00:00
- `context:sec_form4_bulk`: ok; failures=0; last_success=2026-11-11T18:03:46.016798+00:00
- `context:stablecoin_pegs`: error; failures=7; last_success=2026-11-11T20:12:54.126853+00:00
- `context:stocks_options_import`: disabled_no_current_file; failures=0; last_success=2026-11-11T20:14:02.765632+00:00
- `context:stocks_options_yfinance_proxy`: error; failures=1; last_success=2026-11-11T16:52:20.782411+00:00
- `context:token_unlocks`: ok; failures=0; last_success=2026-11-11T20:14:28.493502+00:00

Only stablecoin depeg and cross-exchange consistency may reduce new Paper entries. 
All other filters are point-in-time Shadow/advisory evidence and cannot promote a trade.
