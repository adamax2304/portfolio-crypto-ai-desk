# Circuit Breaker — Alert-Only Implementation (PART 1)

**Date:** 2026-06-17 · **Verdict:** **CIRCUIT_BREAKER_ALERT_ONLY_READY**
**Mode:** would-pause diagnostic. **No hard block, no size change, no routing change.**

## What was built
- **`src/risk/circuit_breaker.py`**
  - `evaluate_circuit_breaker(rows, scope_asset, scope_mode, scope_direction, scope_regime, now, config)` — pure evaluator over today's terminal outcomes.
  - `circuit_breaker_for_signal(store, signal, now, config)` — store-driven wrapper (fails open to `ok`).
  - `circuit_breaker_warning_line(state)` — compact Telegram line, or `None`.
  - `CircuitBreakerConfig` thresholds (alert-only): daily ≤ −2R (L2), ≤ −3R (L3), ≥3 stops/day, ≥2 crypto-long stops same regime.
- **`src/storage/sqlite.py`** (2 read-only helpers): `load_recent_terminal_outcomes(since_iso)` (latest terminal outcome per signal, joined to metadata, exit ≥ since), `last_alert_by_type(alert_type)` (for dedupe). Pure SELECT — no schema change.
- **Wiring:** `src/notifiers/paper_entry.py` calls `assemble_risk_guard_fields(...)` (which includes the breaker) after the concentration block, merges fields into the payload, and appends a deduped warning line to actionable messages. Fails open to `{}`.

## Fields emitted (payload + report + Control Plane)
`circuit_breaker_state` (ok/watch/would_pause), `circuit_breaker_level` (0/2/3), `circuit_breaker_reason`, `day_realized_r`, `day_realized_r_asset`, `stops_today`, `consecutive_stops`, `crypto_long_streak_count`, `last_stop_time`, `would_pause_new_entries`, `would_throttle_crypto_longs`, `would_reduce_size`, `would_require_fresh_catalyst`, `diagnostic_only=true`.

## Thresholds (what fires the would-pause)
| Trigger | Rule | Level |
|---|---|---|
| Daily realised R | ≤ −2R | L2 |
| Daily realised R | ≤ −3R | L3 |
| Stops today (asset/mode) | ≥ 3 | L2 |
| Crypto long stops, same regime | ≥ 2 | L2 |
| First stop today | ≥ 1 | `would_reduce_size` flag (watch) |
| Consecutive stops | ≥ 3 | `would_require_fresh_catalyst` flag |

The threshold R uses `min(asset_day_R, asset+mode_day_R)` so a clean mode never masks a bleeding asset book.

## Telegram (deduped)
A single compact line — *"⚠ Circuit breaker would pause new entries (−Xr today / N stops) — diagnostic, not blocked"* — is appended to the actionable alert. Dedupe: one per `asset/mode/day/level`, enforced by recording a `cb_diag:<asset>:<mode>:<day>:L<level>` marker row in `signal_alerts` and checking `last_alert_by_type` before re-emitting.

## Control Plane (read-only)
The new fields flow through `payload_json`; `backend/app/desk_adapter.py` now passes them through (`.get()`, additive). No command/lock/routing change.

## Safety
- Never blocks an entry, never changes size or routing (the actionable path still sets `telegram_channel="telegram"`).
- Fails open: a broken store → `circuit_breaker_state="ok"`, `would_pause_new_entries=False`.
- `diagnostic_only=True` on every result.

## Why alert-only (not hard) now
Per the prior would-pause audit, 7d of data is too thin and one outlier day dominates; a hard auto-pause needs a ≥30d threshold sweep + explicit approval. This stage ships observation + the would-pause flag only.
