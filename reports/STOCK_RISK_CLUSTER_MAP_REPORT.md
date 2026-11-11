# Stock Risk-Cluster / Proxy Map (PART 1)

**Date:** 2026-06-16

## Files
- `config/stock_risk_clusters.yaml` — symbol → {risk_bucket, proxy_group} + defaults.
- `src/stocks/risk_clusters.py` — `load_stock_risk_clusters()`, `get_stock_risk_bucket(sym)`,
  `get_stock_proxy_group(sym)`, `normalize_symbol(sym)`. Pure, cached, never raises.

## Buckets / proxy groups
| risk_bucket | symbols | redundant-proxy group |
|-------------|---------|------------------------|
| megacap_tech | AAPL MSFT META AMZN GOOGL NFLX (singles); **QQQ XLK XLY** | `qqq_xlk_proxy` (collapse) |
| semis | AMD NVDA SMCI AVGO (singles); **SMH** | `semis_proxy` |
| broad_index | **SPY DIA IWM** | `broad_index_proxy` (collapse) |
| high_beta_ai | PLTR | — |
| high_beta_consumer | TSLA | — |
| crypto_equity | COIN MSTR | — |
| healthcare | LLY UNH; XLV | `healthcare_proxy` |
| financials | JPM; XLF | `financials_proxy` |
| energy | XOM; XLE | `energy_proxy` |
| **unknown** (default) | anything unmapped | `symbol_itself:<SYM>` (collapses only vs itself) |

## Collapse semantics
- `*_proxy` groups (QQQ/XLK, SPY/DIA/IWM, …) collapse **across symbols** — they are
  redundant baskets of the same exposure.
- All other groups (`*_single`, unknown) collapse **only against the same symbol**
  (duplicate signals), so two distinct names (AAPL vs MSFT) are never merged by Rule A —
  Rule B caps those instead.

## Tests
`tests/test_stock_concentration_caps.py::test_17_helper_known_and_unknown_symbols` +
`test_17b_unknown_symbol_actionable_not_capped` — known symbols map correctly,
`normalize_symbol("aapl.us")=="AAPL"`, unknown → bucket `unknown` + own proxy group, `None`
safe. **PART 1 status: DONE.**
