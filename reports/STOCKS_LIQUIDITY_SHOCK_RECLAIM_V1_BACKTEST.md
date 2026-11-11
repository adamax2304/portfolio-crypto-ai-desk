# Stocks Liquidity Shock Reclaim v1 - Historical Replay

- generated: `2026-10-06T00:25:01.384738+00:00`
- event period: `2026-07-24T13:45:00+00:00` to `2026-10-05T19:15:00+00:00`
- chronological split: `2026-09-22T15:00:00+00:00` (70% train / 30% untouched holdout)
- symbols inspected: `91`
- archive additions: `{"15m": 0, "1m": 0}`

All results include modeled fees/slippage. Same-minute stop/target ambiguity is stop-first. The replay caps correlated events so one broad selloff cannot inflate the sample.

## FAST_1M_RECLAIM

- selected on train only: `{"max_flush_atr": 3.5, "max_market_drop_pct": 0.6, "max_sector_drop_pct": 1.1, "min_flush_atr": 1.5, "min_flush_pct": 0.8, "min_idiosyncratic_drop_pct": 0.3, "min_level_breach_atr": 0.15, "min_rvol": 1.7}`
- train: n=36, net=$-5.54 (-0.55R), PF=0.948, win=55.6%, DD=$27.18, cost=$44.91
- holdout: n=21, net=$0.55 (+0.06R), PF=1.007, win=57.1%, DD=$33.03, cost=$26.90
- all independent events: n=57, net=$-4.99 (-0.50R), PF=0.973, win=56.1%, DD=$33.03, cost=$71.81
- raw diagnostic: n=64, net=$-31.66 (-3.17R), PF=0.857, win=53.1%, DD=$48.48, cost=$76.87

## HELD_1M_RECLAIM

- selected on train only: `{"max_flush_atr": 3.5, "max_market_drop_pct": 0.6, "max_sector_drop_pct": 1.1, "min_flush_atr": 1.1, "min_flush_pct": 0.8, "min_idiosyncratic_drop_pct": 0.2, "min_level_breach_atr": 0.05, "min_rvol": 1.7}`
- train: n=24, net=$78.38 (+7.84R), PF=3.238, win=75.0%, DD=$11.86, cost=$23.78
- holdout: n=18, net=$-8.14 (-0.81R), PF=0.876, win=55.6%, DD=$40.93, cost=$17.55
- all independent events: n=42, net=$70.24 (+7.02R), PF=1.698, win=66.7%, DD=$40.93, cost=$41.32
- raw diagnostic: n=46, net=$31.70 (+3.17R), PF=1.228, win=60.9%, DD=$61.08, cost=$44.03

## HELD_1M_STRUCTURE_TARGETS

- selected on train only: `{"max_flush_atr": 3.5, "max_market_drop_pct": 0.6, "max_sector_drop_pct": 1.1, "min_flush_atr": 1.1, "min_flush_pct": 0.8, "min_idiosyncratic_drop_pct": 0.2, "min_level_breach_atr": 0.05, "min_rvol": 1.7}`
- train: n=21, net=$89.59 (+8.96R), PF=4.81, win=81.0%, DD=$11.00, cost=$21.25
- holdout: n=18, net=$9.78 (+0.98R), PF=1.161, win=61.1%, DD=$41.04, cost=$17.73
- all independent events: n=39, net=$99.38 (+9.94R), PF=2.179, win=71.8%, DD=$41.04, cost=$38.99
- raw diagnostic: n=41, net=$82.23 (+8.22R), PF=1.811, win=68.3%, DD=$45.93, cost=$40.30

## HELD_1M_WIDER_STOP_015

- selected on train only: `{"max_flush_atr": 3.5, "max_market_drop_pct": 0.6, "max_sector_drop_pct": 1.1, "min_flush_atr": 1.1, "min_flush_pct": 0.8, "min_idiosyncratic_drop_pct": 0.2, "min_level_breach_atr": 0.05, "min_rvol": 1.7}`
- train: n=24, net=$78.53 (+7.85R), PF=3.26, win=75.0%, DD=$11.79, cost=$23.14
- holdout: n=18, net=$-9.85 (-0.98R), PF=0.847, win=55.6%, DD=$40.18, cost=$17.07
- all independent events: n=42, net=$68.69 (+6.87R), PF=1.692, win=66.7%, DD=$40.18, cost=$40.21
- raw diagnostic: n=46, net=$33.15 (+3.31R), PF=1.246, win=60.9%, DD=$59.88, cost=$42.87

## Verdict

Preliminary holdout edge: `FAST_1M_RECLAIM`, `HELD_1M_STRUCTURE_TARGETS`

The local minute archive has non-uniform symbol coverage. This replay is an initial screen, not a Live promotion decision; the forward Paper cohort remains authoritative.
