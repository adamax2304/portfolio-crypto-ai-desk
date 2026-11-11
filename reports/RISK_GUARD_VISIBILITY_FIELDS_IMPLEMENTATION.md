# Risk-Guard Visibility Fields — Implementation (PART 2)

**Date:** 2026-06-17 · **Mode:** add-only / read-only / diagnostic. **No routing, TP/SL, size, or execution change.**

## What was built
- **`src/risk/risk_guards.py`** — `assemble_risk_guard_fields(store, signal, *, file_store, now, mfe_r, regime_now, entry_triggered_at)`: composes all guard blocks into one field bundle; each block is independently fail-open. `risk_guard_warning_lines(fields)` returns the compact operator lines. `profit_protection_hint(mfe_r)` maps live MFE→hint.
- **Wiring:** `src/notifiers/paper_entry.py` merges the bundle into `payload` (via `setdefault`, never overwriting existing keys) and appends warning lines to the actionable message.
- **Control Plane:** `backend/app/desk_adapter.py` passes the fields through read-only; `frontend/src/types.ts` `Signal` gains them as optional fields.

## Fields (all add-only; null/unknown when data is unavailable — never faked)
| Group | Fields |
|---|---|
| Circuit breaker (PART 1) | circuit_breaker_state, circuit_breaker_level, day_realized_r, stops_today, consecutive_stops, crypto_long_streak_count, would_pause_new_entries, would_throttle_crypto_longs, would_reduce_size, would_require_fresh_catalyst |
| Risk-off (PART 6) | btc_intraday_risk_off, btc_day_change_pct, btc_1h_trend, btc_4h_trend, regime_context, would_throttle_long, risk_off_diagnostic |
| Lifecycle (PART 5) | lifecycle_label, held_hours, next_day_revalidation_required, carryover_warning, rth_close_approaching, rth_overnight_hold, catalyst_stale, regime_changed_since_entry |
| Sector cap (PART 3) | would_bind_sector_cap, would_sector_rank, would_sector_bucket, would_sector_reason, actual_concentration_status |
| Profit protection (PART 4) | profit_protection_hint, would_move_to_BE, would_partial_TP1 |
| Catalyst integrity (PART 7) | catalyst_integrity_status, direct_news_items_checked, catalyst_mapping_confidence |
| Marker | diagnostic_only=true |

## Telegram / report rendering
B/A actionable alerts already show **SL** (unchanged), **freshness**, and now (when present) compact diagnostic lines: circuit-breaker would-pause (deduped), risk-off context, carryover/revalidation, sector-cap would-bind, catalyst-backed confirmation. Lines are appended after the freshness line — the SL line is never replaced.

## Null-not-fake rule
Each sub-computation returns `None`/`"unknown"` when its data is missing (e.g. BTC OHLCV unavailable → `regime_context="unknown"`, `btc_intraday_risk_off=None`; news_items unavailable → `catalyst_integrity_status="unknown"`). No placeholder values masquerade as real signals.

## Safety
- `payload.setdefault` only adds keys — never overwrites the existing 23 payload keys.
- The whole block is wrapped in try/except → on failure the alert is unchanged.
- No change to size_weight, telegram routing/channel, TP/SL, or scoring.
