# Operational Circuit Breaker — Alert-Only Deployment (PART 1)

**Date:** 2026-06-17 · **Verdict:** **CIRCUIT_BREAKER_OPERATIONAL_ALERT_ONLY_READY**

## Is it really in the daily flow?
Yes. The per-signal alert path `src/notifiers/paper_entry.send_paper_entry_alert` calls `assemble_risk_guard_fields(...)`, which calls `circuit_breaker_for_signal(store, signal)`. That path runs on every B/A actionable alert produced by the crypto monitor (`monitor-watchlist`) and stocks monitor (`stocks-monitor-session`) — both launched each scheduler cycle. So the breaker state is computed and attached to the live alert payload, not just in tests.

## Fields in `payload_json` (confirmed present via the assembler)
`circuit_breaker_state`, `circuit_breaker_level`, `circuit_breaker_reason`, `day_realized_r`, `stops_today`, `consecutive_stops`, `crypto_long_streak_count`, `would_pause_new_entries`, `would_throttle_crypto_longs`, `would_reduce_size`, `would_require_fresh_catalyst`, `diagnostic_only=true`.

## Telegram warning
Appended to actionable alerts only when `circuit_breaker_state == would_pause`, deduped **one per asset/mode/day/level** via a `cb_diag:<asset>:<mode>:<day>:L<level>` marker row in `signal_alerts` (checked with `last_alert_by_type`). It never blocks the alert, never changes size or routing.

## Dry-run command (PART 1 deliverable)
`python -m scripts.circuit_breaker_dry_run` → writes `OPERATIONAL_CIRCUIT_BREAKER_DRY_RUN.md`, prints per asset/mode state, sends **no** Telegram, writes nothing except the report.

### Today's dry-run (live read-only)
| asset | mode | state | level | day_R | stops | crypto_long_streak | would_pause |
|---|---|---|---|---|---|---|---|
| crypto | intraday | would_pause | 3 | −3.0 | 10 | 20 | True |
| crypto | scalp | would_pause | 2 | −1.0 | 3 | 20 | True |
| crypto | swing | would_pause | 2 | +3.0 | 7 | 20 | True |
| stocks | intraday | ok | 0 | +6.0 | 0 | 0 | False |

→ The breaker would correctly flag the crypto books as bleeding today (crypto intraday −3R / 10 stops) while leaving stocks intraday (+6R) untouched. (Note: scalp is shadow-only anyway; swing's stop-count trips even at +3R net — expected for a count-based rule.)

## Safety (asserted by tests)
- Alert still sends when `would_pause` (integration test).
- Dedupe marker prevents repeat warnings (integration test).
- Dry-run writes only its report.
- No routing/size/scoring mutation (`telegram_channel=telegram`, size untouched).

## Reports
`OPERATIONAL_CIRCUIT_BREAKER_DRY_RUN.md` (this run), plus the prior-stage `CIRCUIT_BREAKER_ALERT_ONLY_*`.
