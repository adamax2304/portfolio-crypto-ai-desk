# Operational Risk-Guard Visibility — Verification (PART 3)

**Date:** 2026-06-17 · **Verdict:** **RISK_GUARD_VISIBILITY_OPERATIONAL_READY**

## Telegram B/A alert format (verified against `paper_entry.py`)
- **SL line always present** — the `Stop:` line is built in the message body and is never replaced; diagnostic lines are *appended* after the freshness line.
- **Freshness line present** — `entry_freshness(...)` line is appended on the actionable path.
- **Diagnostic lines appended compactly** — circuit-breaker would-pause (deduped), risk-off context, carryover/revalidation, sector-cap would-bind, catalyst-backed, and the new position-advisor line. Each is a single short line; non-applicable ones are omitted (no spam).
- **No markdown/cp1252 crash** — the notifier sends with `parse_mode=""` (plain text), and messages are emoji-prefixed (⚠/ℹ) which Telegram renders as UTF-8. (The cp1252 issue only ever affected local console `print`, not the Telegram payload.)

## Fields present in `payload_json` (via `assemble_risk_guard_fields`)
`circuit_breaker_state`, `day_realized_r`, `stops_today`, `consecutive_stops`, `crypto_long_streak_count`, `regime_context`, `btc_intraday_risk_off`, `lifecycle_label`, `held_hours`, `next_day_revalidation_required`, `carryover_warning`, `would_bind_sector_cap`, `profit_protection_hint`, `catalyst_integrity_status`, `direct_news_items_checked`, `catalyst_mapping_confidence`, `position_advisor_status`/`suggested_notional`/`max_safe_leverage_estimate`, `diagnostic_only`.

## Control Plane
- `backend/app/desk_adapter.py` passes the fields through read-only (`.get()`); compiles clean.
- `frontend/src/types.ts` `Signal` has them as **optional** fields → TS compiles; absent fields are `undefined`, never a crash.
- No command/lock/routing change.

## Tests
- `tests/test_risk_guard_fields.py` — payload has the fields; SL/Stop still present; assembler fails open.
- Control Plane adapter `py_compile` clean.
- Absent fields → `None`/`undefined`, no crash (permissive `.get()` / optional TS).

See `CONTROL_PLANE_RISK_FIELDS_DISPLAY_PLAN.md` for the (non-breaking) UI display plan.
