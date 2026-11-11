# Sector-Cap Would-Bind — Forward Tracker (PART 5)

**Window:** last 14d (since 2026-06-03) · stocks-intraday paper_entry alerts: 161
**Min forward window before any decision:** 10 trading days.

## Would-bind (shadow day-batch cap) vs actual (live per-signal cap)
- **Would bind** (half/shadow): **0**
- **Actually bound live**: **0**
- Gap (would − actual): **0** ← the inert-live discrepancy

### would_bind_sector_cap distribution
- (no would_bind data yet — accumulates as new stocks-intraday alerts fire)

### actual concentration_status distribution
- (none yet)

## Net R of would-bound names (outcome so far)
- would-bound names with a closed outcome: **0**
- net realized R of those names: **0.0R**
  - if strongly negative → the shadow cap is targeting the losers (would help).
  - if positive → the cap would clip winners (do NOT enable).

## Decision gate
Collect ≥10 trading days. Enable a batch-aware LIVE cap (still paper, with explicit approval) ONLY if would-bound names are net-negative AND the cap does not clip net-positive clusters. Until then: shadow-only, cap value unchanged.

_Read-only forward measurement. No routing/size/cap-value change._