# Risk-Guard Visibility Fields — Test Results (PART 2)

**Date:** 2026-06-17 · **Command:** `python -m pytest tests/test_risk_guard_fields.py -q` → **6 passed**.

| Test | Asserts |
|---|---|
| assembler_returns_expected_fields | bundle contains circuit_breaker_state, day_realized_r, stops_today, regime_context, lifecycle_label, would_bind_sector_cap, profit_protection_hint, catalyst_integrity_status + diagnostic_only |
| profit_protection_hint_mapping | 0R→none, 0.6R→reached_+0.5R, 1.2R→would_move_to_BE, None→unknown |
| paper_entry_not_blocked_and_fields_in_payload | alert sends; payload carries the fields; routing `telegram`; size untouched |
| circuit_breaker_warning_is_deduped_per_day_level | warning shown once/day/level, field always present |
| assembler_fails_open | broken store → diagnostic_only, no crash |
| (profit hint unit) | see mapping test |

## Cross-checks
- **Control Plane safety:** `backend/app/desk_adapter.py` compiles; fields are read via `.get()` (absent → None); `frontend/src/types.ts` fields are optional. No command/lock/routing change.
- **Null-not-fake:** risk-off returns `unknown` without BTC data (PART 6 tests); catalyst integrity returns `unknown` without news_items (PART 7 tests).
- **SL always present:** the diagnostic lines are appended after the freshness line; the existing `Stop:` line in the message body is untouched.

## Verdict
**RISK_GUARD_VISIBILITY_FIELDS_READY** — fields land in payload + Control Plane, render compactly, fail open, and never alter trade behavior.
