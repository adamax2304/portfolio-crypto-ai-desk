# MEXC three-TP live execution and native parity

Date: 2026-07-23

## Scope

- Live remains limited to crypto swing long `PULLBACK_LIMIT` and
  `BREAKOUT_CONTINUATION` candidates already accepted by Production Paper.
- Risk settings are unchanged: 2% per trade on the configured $100 allocation,
  10% maximum concurrent risk.
- No new live strategy, short lane, intraday lane, or automatic promotion was
  enabled.

## Live exit correction

- Removed the incorrect full-position TP3 from the entry order.
- The entry retains an exchange-side original-stop fallback while its IOC fill
  is being confirmed.
- Immediately after a fill, the fallback is replaced by exactly three MEXC
  partial-position TP/SL legs.
- Default contract allocation is 33% / 33% / 34%, rounded deterministically to
  MEXC `volUnit`; all three volumes must sum exactly to the filled holding.
- Each leg has its own TP1/TP2/TP3 target and the same active protective stop.
- Model F moves the stop monotonically on every still-open leg.
- A position too small for three valid `minVol` legs is rejected before entry.
- Missing, extra, or volume-mismatched legs fail closed: emergency close is
  submitted and the local kill-switch trips.

## MEXC-native pre-submit parity

Every candidate now persists a point-in-time MEXC snapshot before submission:

- exact native contract and tradability state;
- current best bid/ask and spread;
- Paper reference versus executable MEXC entry and drift;
- tick size, contract size, minimum volume, and volume step;
- exact three-leg volume allocation;
- MEXC-native stop and target geometry;
- estimated gross/net USD outcomes with fees, slippage, and funding separated.

Submission is blocked if this snapshot is not clean. New snapshots are labeled
`forward_post_activation`; imported historical plans remain
`historical_backfill` and cannot satisfy the review threshold.

## Evidence gate

- 0-19 clean closed forward observations: `ACCUMULATING_FORWARD_EVIDENCE`.
- 20-29: `EARLY_REVIEW_WINDOW` only.
- 30 or more: `REVIEW_ONLY` only when forward net USD PnL is positive and PF is
  at least 1.25. There is no automatic expansion or promotion.

## Verification

- Focused MEXC tests: 39 passed.
- Wider live/Paper/overlay/scheduler/protection regression: 193 passed.
- Full project regression: 1758 passed.
- Real database migrated in place; no table rebuild or deletion.
- Real MEXC preflight: public/private API OK, contract tradeable, no open
  position, kill-switch clear.
- The existing historical parity example remains backfill and is not counted as
  forward evidence.
- Live monitor restarted on the new code and reports an OK heartbeat.
