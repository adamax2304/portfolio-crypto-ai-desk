# Crypto Liquidity Sweep v1 - Implementation

## Status

- Strategy: `crypto_liquidity_sweep_v1`
- Lane: `shadow_crypto_liquidity_sweep`
- Activation: 2026-08-24
- Scope: isolated Shadow only
- Promotion: manual `REVIEW_ONLY` decision only; never automatic

## Deterministic setup

1. A closed 5-minute candle sweeps the 3-hour range low or high by at least 8 bps.
2. That candle closes back inside the prior range with a rejection wick and RVOL >= 1.25.
3. A matching actual Binance force-order event exists during the preceding 10 minutes:
   - forced sells support a long reversal after a downside sweep;
   - forced buys support a short reversal after an upside sweep.
4. Aggregate matching forced-order notional is at least USD 50,000.
5. The same exchange set shows a 10-minute OI decrease of at least 0.25%.
6. Fresh order-book data and spread <= 20 bps are required.
7. Asia/off sessions are blocked. Missing, stale, mismatched, or ambiguous data rejects the observation.

Entry is the close of the confirmation candle. The stop is beyond the sweep extreme plus 0.12 ATR, capped at 3.5% distance. Targets are 1R, 2R, and 3R. The existing Model F profit-protection simulator prices fees, slippage, and actual funding separately.

## Isolation

The strategy writes only:

- `crypto_liquidity_sweep_v1_shadow_outcomes`
- `crypto_liquidity_sweep_v1_shadow_evaluations`
- `crypto_liquidity_sweep_v1_shadow_meta`

It has no Paper signal, Paper ledger, Telegram trade alert, routing, order, or Live execution path.

## Evidence policy

Only clean forward outcomes count. A manual Paper review requires at least 30 clean closed forward trades, 28 forward days, positive net USD PnL, PF >= 1.25, acceptable drawdown, and a positive paired comparison when a valid control exists.

## Initial data state

The Binance force-order websocket is connected. The retained liquidation-event archive was empty at activation, so no historical result is claimed and no synthetic OI proxy is used. The lane will accumulate evidence only from observed events after activation.
