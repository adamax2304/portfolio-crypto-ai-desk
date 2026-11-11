# Stocks-Intraday Rework Diagnostic (PART 8)

**Window:** last 30d · closed stocks-intraday trades: **447** · net **106.0R**
**Read-only. No production change — filters are simulated only.**

### By tier
| tier | n | net_R |
|---|---|---|
| C | 206 | -34.0 |
| A | 48 | 8.0 |
| B | 193 | 132.0 |

### By catalyst
| catalyst | n | net_R |
|---|---|---|
| catalyst | 8 | -2.0 |
| no_catalyst | 439 | 108.0 |

### By session (at creation)
| session | n | net_R |
|---|---|---|
| after-hours | 79 | -12.0 |
| regular session | 196 | 18.0 |
| holiday | 36 | 21.0 |
| weekend | 43 | 29.0 |
| premarket | 93 | 50.0 |

### By regime
| regime | n | net_R |
|---|---|---|
| risk_off | 59 | -4.0 |
| risk_on | 35 | -3.0 |
| chop | 43 | 2.0 |
| bullish | 310 | 111.0 |

### By legal flag
| legal | n | net_R |
|---|---|---|
| legal_flag | 7 | 1.0 |
| clean | 440 | 105.0 |

### By risk bucket
| bucket | n | net_R |
|---|---|---|
| megacap_tech | 130 | -16.0 |
| energy | 12 | -10.0 |
| crypto_equity | 8 | -4.0 |
| broad_index | 47 | -4.0 |
| high_beta_consumer | 16 | 0.0 |
| healthcare | 69 | 3.0 |
| high_beta_ai | 19 | 7.0 |
| financials | 20 | 21.0 |
| semis | 126 | 109.0 |

### Worst 10 tickers by net R
| ticker | n | net_R |
|---|---|---|
| XLV | 30 | -16.0 |
| AAPL | 29 | -16.0 |
| IWM | 17 | -15.0 |
| XLY | 15 | -13.0 |
| AMZN | 13 | -8.0 |
| XOM | 7 | -7.0 |
| MSTR | 3 | -3.0 |
| META | 6 | -3.0 |
| XLE | 5 | -3.0 |
| NFLX | 6 | -3.0 |

## Safe-filter counterfactuals (simulated, not applied)
| filter | kept | dropped | net_R |
|---|---|---|---|
| current_all | 447 | 0 | 106.0 |
| drop_C_tier | 241 | 206 | 140.0 |
| only_catalyst_backed | 8 | 439 | -2.0 |
| only_RTH_session | 196 | 251 | 18.0 |
| exclude_legal | 440 | 7 | 105.0 |
| AB_and_catalyst_and_RTH | 1 | 446 | -1.0 |
| AB_and_RTH_no_legal | 137 | 310 | 24.0 |

See `STOCKS_INTRADAY_FILTER_COUNTERFACTUAL.csv` (per-trade) and `STOCKS_INTRADAY_SAFE_RESTRICTION_PLAN.md` for the recommendation.