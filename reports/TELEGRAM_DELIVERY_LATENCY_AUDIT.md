# Telegram Delivery Latency Audit (PART 3)

**Date:** 2026-06-16 · Source: `db/crypto_ai_desk.sqlite` (read-only), `src/notifiers/telegram.py`

## Pipeline stages and where each is timestamped

| # | Stage | Timestamp available? | Measured delay |
|---|-------|----------------------|----------------|
| 1 | Price touches entry | `entry_triggered_at` (candle ts) | — |
| 2 | **Tracker detects entry** | first `checked_at` w/ entry=1 | **median ~135 min** (cadence-bound, PART 2) |
| 3 | `signal_alerts` row created | `sent_at` | written in the same call as 4/5 |
| 4 | `notifier.send` called | (not separately stamped) | sub-second |
| 5 | Telegram delivered | `telegram_status='sent'` | sub-second |

**Key structural fact:** stages 3–5 happen synchronously inside one `send_*_alert` call —
the row's `sent_at` is written right after the send attempt. There is **no separate
DB-create vs send timestamp**, so stages 3→4→5 collapse into one sub-second "emit" step.
The measurable `emit_lag` (alert_at − tracker_detected_at) is seconds, inside the same
`track-signals` process. **All meaningful latency is in stage 2 (the tracker), not in
Telegram.**

## Delivery reliability (7 days, by alert_type)

| alert_type | sent | shadow_only | dry_run | errors |
|------------|-----:|------------:|--------:|-------:|
| paper_entry | 128 | 6 | 129 | 3 (2× ReadTimeout, 1× ConnectTimeout) |
| close_tp | 166 | 2 | — | 0 |
| close_expired | 71 | 4 | — | 1 (ConnectTimeout) |
| close_stop | 29 | 2 | — | 0 |
| entry_change | 39 | — | — | 0 |
| new_signal / tier_upgrade / score_improvement / invalidation_change | 26 | — | — | 0 |

- **Total 7d: 606 alerts, 4 errors = 0.7% error rate.** All errors are network timeouts
  (`ConnectTimeout` / `ReadTimeout`). **Zero formatting / parse-mode / BadRequest errors**
  — the plain-text (`parse_mode=""`) standardization holds.
- **No retry logic** in `src/notifiers/telegram.py` (grep: no retry/backoff). On a timeout
  the alert is **dropped** (status recorded `error:*`), not delayed-then-retried. So
  Telegram failures cost ~0.7% of alerts as *drops*, not as latency.
- `dry_run` (129 on paper_entry) = scheduler/smoke dry-run passes; not real sends.
- Duplicate suppression (`message_hash`, `has_existing_close_alert`) is synchronous —
  adds no delay.

## Conclusion

Telegram delivery is **fast and reliable** (sub-second, 0.7% timeout-drop, no formatting
failures). It is **not** a latency source. The entire operator-facing lag is the
**tracker detection cadence (~2h)** documented in PART 2.

Two minor, separately-addressable robustness notes (not latency):
1. ~0.7% of alerts are silently dropped on a network timeout — a single bounded retry
   would recover most. (Out of scope for this latency task; flagged only.)
2. Stages 3–5 are not individually instrumented; if finer Telegram timing is ever needed,
   add a `created_at` column distinct from `sent_at`. Not required now.

**PART 3 status: DONE.**
