# Crypto Intraday Evidence Hardening

Date: 2026-07-23

## Scope

This pass hardens the isolated crypto-intraday research lane. It does not
change Paper routing, live routing, sizing, stops, targets, Model F, or the
current crypto quality overlay policy.

## What Changed

1. The intraday idea sweep now accepts an entry only when the entry candle had
   fully closed before the original signal expiry. A valid entry remains managed
   by the existing Model F framework after expiry; only a late pre-entry fill is
   rejected.
2. Sweep evidence is append-only. The latest dashboard cache can refresh, while
   every run keeps its own run id, configuration hash, signal/entry timing,
   validity flag, and session fields.
3. Public Binance Futures and MEXC Futures order-book snapshots now record BBO,
   spread, and visible depth at the same cadence as the derivatives monitor.
   MEXC USD depth is computed only when contract metadata supplies a multiplier.
4. The overlay freezes diagnostic-only, fully closed 15m features into future
   point-in-time decisions: ATR(14) percent, 1h/4h realized volatility, RVOL20,
   24h dollar volume, VWAP distance, and public book context. These fields do
   not currently alter an action.
5. Four PULLBACK_LIMIT counterfactual branches are isolated in Shadow:
   explicit BTC risk-off, classified OI-regime unknown, ATR(14) above 2.5%, and
   RVOL20 below 0.5. They use the current geometry and execution model; they
   neither route nor promote signals.
6. The derivatives monitor now records a heartbeat for a connected but quiet
   liquidation websocket, and a temporary sidecar failure cannot skip the other
   monitor stages.

## First Clean Baseline

The first v4 sweep used 90 source signals. The current PULLBACK_LIMIT control
had 10 clean, expiry-valid closed outcomes: net +1.2216 R and +$6.96, 50% win
rate, PF 1.0618. This is explicitly insufficient for a decision.

The historical ATR and RVOL branches correctly report
`AWAITING_POINT_IN_TIME_FEATURE_COVERAGE`; those values were not available in
old point-in-time snapshots. They will start producing evidence only for new
signals. The OI-unknown branch is currently worse than the control and must not
be applied. The risk-off branch has too little covered data to interpret.

## Operational Verification

- Public books: Binance and MEXC both returned fresh BTC, ETH, and SOL books.
- The running derivatives monitor recorded 157 new liquidity snapshots during
  the verification window and health reported two fresh venues for each major.
- The idea-sweep and telemetry paths write only their own read-model tables and
  the market-intelligence sidecar. They do not write `proposed_signals`,
  `signal_outcomes`, `final_r`, the Paper ledger, or live routing.

## Decision Rule

No branch may be moved to Paper automatically. Require at least 30 clean,
closed, post-activation outcomes and 28 forward days, positive net USD PnL,
PF at least 1.25, acceptable drawdown, and a positive paired delta against the
current control. Review the branch manually after that gate.
