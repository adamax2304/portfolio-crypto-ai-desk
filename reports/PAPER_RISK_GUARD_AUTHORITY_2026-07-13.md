# Paper Risk-Guard Authority Decision

Date: 2026-07-13

## Enabled

Only the explicit circuit-breaker pause is authoritative for new paper entries:

- scope: crypto `intraday` and `swing`;
- condition: `circuit_breaker_state=would_pause` and level `>=2`;
- result: record `shadow_risk_guard`, `SHADOW_ONLY`, and paper size `0.0`;
- existing positions are not closed or resized;
- no signal score, tier, entry, stop, target, `final_r`, or live path is changed.

The rule is monotone: it can only downgrade a paper entry. A malformed or
unavailable registry disables this new authority and preserves diagnostic-only
behaviour.

## Still Diagnostic / Shadow

These fields remain visible but do not independently block paper entries:

- `watch` / one-stop circuit-breaker states;
- BTC risk-off and long-bias hints;
- lifecycle and next-day revalidation labels;
- sector-cap shadow diagnostics (the existing concentration route remains the
  authority for its own stock rule);
- profit-protection hints;
- catalyst-integrity labels;
- position/leverage advisor output.

This avoids duplicate gates and prevents a weak or non-point-in-time diagnostic
from removing otherwise valid opportunities.

## Already Locked

The previously proven-bad lanes remain disabled or non-actionable: crypto
scalp, stocks C-tier, old stocks swing/invest, and the configured disabled
entry modes. New experimental modes remain shadow until their forward evidence
is sufficient.

## Verification

- risk/actionability/config suites: `41 passed`;
- overlay/swing/paper accounting suites: `71 passed`;
- the new alert path test confirms an explicit L3 pause is persisted as
  `shadow_risk_guard` and is excluded by the paper actionability resolver;
- read-only production database inspection showed the current crypto sample at
  `would_pause` L2; future new crypto paper entries will therefore be recorded
  in shadow until the breaker returns to a non-paused state.

Two broader legacy tests still expect `sent` while the current crypto-quality
overlay returns `shadow_crypto_quality`; those failures are unrelated to this
change and do not exercise the new risk-guard floor.
