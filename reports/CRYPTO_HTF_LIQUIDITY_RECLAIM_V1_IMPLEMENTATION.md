# Crypto HTF Liquidity Reclaim v1 - Implementation

## Scope

`crypto_htf_liquidity_reclaim_v1` is an isolated Shadow experiment. It has its
own lane, OHLCV cache, SQLite outcomes, observations, evaluations, report and
CLI command. It cannot create a Paper signal, modify a Paper ledger, write a
Live route or place an order.

The config is deliberately shipped with `feature_flag: false`. Enable it only
when the desk wants to begin a fresh forward cohort; it must never be promoted
automatically.

## Deterministic sequence

1. Builds support/resistance zones from 4h pivots. A pivot becomes visible only
   after three *subsequent closed* 4h candles, preventing look-ahead leakage.
2. Requires a 1h candle to sweep through one confirmed zone, reject it with a
   wick, close back through it, and show non-weak relative volume.
3. Requires observed Binance/Bybit forced flow in the matching direction,
   same-venue OI deleveraging, fresh usable spread and non-adverse funding.
4. Requires BTC 4h alignment by default. A missing or conflicting alignment is
   a rejection, never a positive assumption.
5. Opens no trade at the sweep. It creates two private pending rows:
   `EARLY_RECLAIM` enters only after one closed 15m reclaim; `HELD_RECLAIM`
   waits for two consecutive closed reclaim candles. Both expire after four
   15m bars and remain separate evidence cohorts.
6. Stop is beyond the sweep extreme with a 1h ATR buffer. The nearest opposing
   confirmed 4h level must leave at least `2.5R` room. TP1/TP2 are 1.0R/1.75R;
   TP3 sits just before that opposing zone. The shared confirmed-close Model F
   simulator supplies costs, funding and profit protection.

## Inputs and cadence

- Private Bybit Linear OHLCV cache for `4h`, `1h`, `15m`.
- Existing market-intelligence snapshots: multi-venue OI/funding/BBO plus
  Binance/Bybit public liquidation streams.
- `scripts/derivatives_monitor.py` refreshes the data before this lane ticks.
  It refreshes each timeframe only at a new candle boundary, so the new
  experiment does not add avoidable two-minute collector latency.

## Evidence policy

Reports distinguish pending, skipped, open and closed outcomes, and summarize
each profile separately. Promotion can only become `REVIEW_ONLY` after at least
30 clean closed forward trades, 28 forward days, positive USD PnL, PF >= 1.25
and acceptable drawdown. There is no auto-promotion path.

## Verification

- New unit coverage: no-look-ahead pivots, side-correct liquidation flow,
  missing liquidation transport, one- versus two-close confirmation, idempotent
  schema migration, dry-run isolation and monitor order.
- Relevant Shadow/market-intelligence/scheduler regression: `121 passed`.

## Known limitations

Public liquidation streams are confirmation signals, not a complete market
liquidation tape; their notional remains a lower-bound observation. The lane
does not use CVD/order-flow, liquidation heatmaps or paid order-book history.
Those are potential v2 additions only after clean forward evidence makes the
basic setup worth extending.
