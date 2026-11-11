# Crypto Liquidity Sweep v1 - Logic Audit

Date: 2026-08-24

## Verdict

The implementation is a valid **Shadow-only liquidation-sweep reversal
experiment**, not yet a proven strategy. Its direction, timestamp handling,
and execution simulation are internally consistent. Promotion is correctly
blocked until the configured forward sample and quality requirements are met.

## What Is Correct

- The strategy makes a decision only after the 5-minute sweep candle has
  closed. No intrabar price is used as if it had been known at entry time.
- A downside sweep accepts only observed forced SELL flow before considering a
  long; an upside sweep accepts only forced BUY flow before considering a
  short.
- A swept range is rejected unless the close is back inside it, the rejection
  wick is material, and relative volume is above baseline.
- Cross-venue OI must fall over a comparable ten-minute window. A widening BBO
  spread, stale data, weak session, or invalid stop geometry rejects the row.
- Stop is beyond the sweep extreme plus ATR buffer; targets and Model F use the
  existing realistic cost/profit-protection simulator.
- The lane owns only its outcomes, observations, evaluation, and metadata
  tables. It cannot create Paper signals, ledger rows, Telegram trade alerts,
  or Live orders.

## Corrections Applied During Audit

1. Switched Binance to its current documented all-market force-order stream.
2. Added Bybit's public all-liquidation stream. Bybit reports the *liquidated
   position* side, so the collector explicitly converts it to the actual forced
   order direction before any rule sees it.
3. Configured liquidation sources are now enforced in SQL and health checks.
4. Added a separate observation funnel for structurally swept candles rejected
   before entry. It records enumerable rejection reasons without mixing skipped
   rows with executable outcomes.
5. Split `LIQUIDATION_NOT_OBSERVED` from `LIQUIDATION_DATA_MISSING`: a healthy
   quiet feed is no longer mislabelled as a data failure.

## Parameter Review

| Parameter | Current value | Rationale | Status |
| --- | ---: | --- | --- |
| Candle timeframe | 5 minutes | Fast enough for a post-sweep reversal, but only closed candles are actionable. | Keep |
| Range lookback | 36 bars / 3 hours | Defines a local liquidity boundary without turning this into a multi-day swing trade. | Keep as baseline |
| Level-touch tolerance | 12 bps | Logs whether the range extreme was repeatedly tested; it does not yet block a one-touch level. | Calibration feature |
| Minimum sweep | 8 bps | Rejects a one-tick breach while retaining small, liquid-asset sweeps. | Needs forward calibration |
| Rejection wick | 45% | Requires a material rejection rather than a close at the extreme. | Keep as baseline |
| Close location | 60% | Requires recovery inside the candle, but does not require a near-perfect close. | Keep as baseline |
| RVOL | 1.25x | Confirmation, deliberately not a severe volume gate. | Keep as baseline |
| Forced-flow window | 10 minutes | Covers the sweep candle and immediate confirmation. | Keep |
| Forced-flow minimum | $50k | A conservative *observed-flow* floor, not an estimate of all liquidations. | Do not tune before observations accumulate |
| OI decline | 0.25% | A weak confirmation threshold to avoid rejecting every small unwind. | Needs forward calibration |
| Spread ceiling | 20 bps | Prevents entering while the book remains visibly dislocated. | Keep |
| Stop buffer | 0.12 ATR | Baseline protective margin beyond the sweep wick. | Compare 0.12/0.25/0.35 only as labelled counterfactuals |
| Holding cap | 6 hours | Keeps this a reversal trade rather than a swing thesis. | Keep |

## Important Limits

- Public liquidation feeds are not a complete liquidation tape. Binance sends
  only the latest liquidation for a symbol per second. The strategy treats the
  reported notional as confirmation/lower-bound evidence, never a market-wide
  total.
- No public data proves a universal dollar threshold, wick percentage, or OI
  threshold across BTC and small altcoins. This is why values above are frozen
  priors, not claims of an already optimized edge.
- The current range extreme is a practical proxy for a liquidity level. A true
  stop-density map needs L2/order-flow or liquidation-level data that is not in
  the current free pipeline.

## Evidence Plan

For the next 28 forward days, keep the trading rules frozen. Evaluate only
clean closed rows; separately inspect the observation funnel by symbol, side,
session, rejection reason, observed-flow bucket, OI change, and spread bucket.
Only after 30 clean closed trades compare pre-registered settings such as stop
buffer or a two-touch level requirement. The baseline stays `REVIEW_ONLY`; no
automatic Paper or Live promotion is permitted.
