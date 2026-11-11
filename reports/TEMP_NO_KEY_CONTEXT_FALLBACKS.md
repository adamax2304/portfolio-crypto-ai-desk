# Temporary No-Key Context Fallbacks

Implemented: 2026-07-17. Review after: 2026-08-17.

## Scope

- Token unlocks: public DefiLlama calendar HTML is parsed once in the long-horizon scheduler window.
- The normalized future cliff calendar is archived locally and reused for at most 48 hours if the network fails.
- Stock options: SPY and QQQ chains are read through the existing yfinance dependency.
- Net GEX, gamma flip, call wall, put wall, 0DTE OI share, IV30, RV30, and VRP are calculated deterministically.
- Both contexts refresh before `track-signals (pre)` so the observation predates any new entry alert.

## Trust Boundary

- Token rows are labelled `provisional_public_calendar`.
- GEX rows are labelled `provisional_point_in_time` and use the conventional inferred dealer-sign model.
- yfinance is unofficial/delayed; open interest can reflect the previous session.
- Missing, stale, malformed, or unavailable data is neutral. It never upgrades a trade.
- Token unlock and GEX Paper routing remain disabled. Both collect Shadow/counterfactual evidence only.
- Live, paper geometry, risk sizing, ledger accounting, and signal/outcome tables are unchanged.

## Verification

- Real token refresh: 185 normalized future cliff events, no provider key.
- Real options refresh: SPY and QQQ proxy snapshots, no errors.
- Scheduler log: market risk, options context, then tracker; all completed with exit code 0.
- Full regression: 1615 passed before the final cache-only test was added.
- Persisted refresh invariant: proposed signals, outcomes, final R sum, and paper ledger unchanged.

The temporary sources are sufficient for one month of Shadow evidence collection. They are not a substitute for a licensed dealer-positioning feed or a contractual token-unlock API if either filter is later considered for Paper routing.
