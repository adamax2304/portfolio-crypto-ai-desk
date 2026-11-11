# Stocks Liquidity Shock Reclaim v1

## Objective

Test whether a liquid US stock that makes an abnormal, idiosyncratic RTH
downside move has a short-lived recovery edge after it reclaims a swept local
low.  The implementation deliberately calls the observable event a liquidity
shock.  Historical bars do not reveal the hidden stop inventory or the order
book state, so the system must not label those facts as known.

## Research basis

- SEC market-structure work documents that temporary order-book liquidity
  imbalances can create sharp moves that reverse when liquidity returns.
- Academic liquidity-provision research links temporary price pressure with
  short-run reversal, while also showing that information-driven moves are a
  different and more dangerous population.
- LULD/halts alter execution mechanics. They are excluded from v1 rather than
  simulated without an authoritative point-in-time halt tape.

Primary references:

- https://www.sec.gov/newsroom/speeches-statements/taking-stock-treasury-market-regulation
- https://www.sec.gov/files/dera-luld-white-paper.pdf
- https://faculty.haas.berkeley.edu/hender/liq_provision_ret_predict_JBF.pdf
- https://www.federalreserve.gov/econres/feds/slow-capital-fast-prices-shocks-to-funding-liquidity-and-stock-price-reversals.htm
- https://www.sciencedirect.com/science/article/pii/S0304405X14001366

## Implementation stages

1. Detect a closed 15m RTH shock using prior-only ATR, volume and local-low
   features.
2. Require adequate 30-day dollar liquidity and bar dollar volume.
3. Reject broad SPY/sector cascades and require idiosyncratic underperformance.
4. Reject negative point-in-time company events whose `available_at` is not
   later than the decision.
5. Compare two independent Paper profiles on the same raw event:
   `FAST_1M_RECLAIM` requires one closed reclaim bar; `HELD_1M_RECLAIM`
   requires two consecutive progressing closes.
6. Place a structural stop below the shock low plus an ATR buffer. Use two
   targets, conservative stop-first intrabar ordering, modeled fees/slippage,
   and no overnight carry.
7. Store outcomes in a dedicated table and bars in a separate append-only
   research database. Do not create generic proposed signals and do not add a
   live route.
8. Select thresholds on the first 70% of event time only. Evaluate the final
   30% once, with correlated events capped by symbol/day, sector/15m and market
   episode.

## Initial result

The local archive spans 2026-07-24 through 2026-09-28, with non-uniform 1m
coverage across 91 eligible single names. After costs and independence caps:

- FAST: 41 all-period trades, -$14.71, -1.47R, PF 0.89; holdout 15 trades,
  -$25.72, PF 0.56. It remains a negative Paper control.
- HELD: 33 all-period trades, +$73.93, +7.39R, PF 2.12; holdout 15 trades,
  +$14.48, PF 1.34. It is the primary Paper candidate.

This is preliminary evidence, not a live promotion. The required next evidence
is at least 30 clean forward closes over 30 distinct forward days with positive
net PnL, PF at least 1.20 and controlled drawdown.

