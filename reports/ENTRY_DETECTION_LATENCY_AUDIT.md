# Entry-Detection Latency Audit (PART 2)

**Date:** 2026-06-16 · Source: `db/crypto_ai_desk.sqlite` (read-only)
**Per-signal data:** [ENTRY_DETECTION_LATENCY.csv](ENTRY_DETECTION_LATENCY.csv) (1,368 entered signals)
**Generator:** `scripts/audit_latency_expired.py latency`

## Definitions

- **entry_touch_at** = `signal_outcomes.entry_triggered_at` (candle timestamp the entry
  zone was first touched — theoretical touch from OHLCV).
- **tracker_detected_at** = first `checked_at` where `entry_triggered=1`.
- **paper_entry_alert_at** = `MIN(signal_alerts.sent_at)` for `alert_type='paper_entry'`.
- **entry_age_sec** = paper_entry_alert_at − entry_touch_at (the operator-facing lag).
- **detection_lag** = tracker_detected_at − entry_touch_at; **emit_lag** = alert_at − detected.
- Classes: fresh ≤2m · acceptable ≤5m · late 5–15m · very_late >15m · already_closed
  (entry + terminal status in the same tracker evaluation).

> **Honest limitation:** `price_at_alert_time` and `current_price` are **not persisted**
> by the tracker, so price-distance-at-send cannot be reconstructed retroactively without
> a heavy OHLCV re-walk. This audit measures **time latency** precisely; the freshness
> label (PART 5) computes the time-based age live at send. R-geometry distance to stop is
> fixed by construction (stop ≈ 1R), not informative per-signal here.

## Results — entry_age distribution

| Window | n entered | fresh | acceptable | late | **very_late** | already_closed | unknown |
|--------|----------:|------:|-----------:|-----:|--------------:|---------------:|--------:|
| 24h    | 83        | 0     | 0          | 0    | **36**        | 16             | 31      |
| 7d     | 401       | 0     | 0          | 0    | **113**       | 51             | 237     |
| 14d    | 755       | 0     | 0          | 0    | **130**       | 126            | 499     |

**entry_age (minutes), excluding already_closed/unknown:**

| Window | n | median | mean | p90 | max |
|--------|--:|-------:|-----:|----:|----:|
| 24h    | 50  | **135.0** | 134.4 | 211.7 | 339.5 |
| 7d     | 145 | 135.9 | 291.4 | 339.5 | 2635.6 |
| 14d    | 167 | 145.6 | 1300.4 | 4735.6 | 12745.6 |

> `unknown` = scalp shadow rows / signals where touch-ts or alert-ts is missing. The very
> large 7d/14d means/maxima come from a few signals whose entry candle far predates the
> first tracker pass (multi-day swing backfill); the **median ~135 min is the stable,
> representative figure**.

## By asset/mode (24h — fresh / acceptable / late / very_late / already_closed)

```
crypto  intraday  0/0/0/7/6
crypto  scalp     0/0/0/5/4   (shadow-only — not pushed)
crypto  swing     0/0/0/11/5
stocks  intraday  0/0/0/13/1
```

## Conclusion

**Zero** entered signals in any window were fresh, acceptable, or even "late" (≤15m).
**Every** measurable paper-entry alert is `very_late` — median **~135 min (2.25h)** behind
the actual entry touch. This is structural, not jitter:

- Root cause (PART 0): paper-entry detection runs **only** inside `track-signals`, which
  fires twice per **2-hour** cycle. The 5-min crypto monitor does not detect entries.
- So `detection_lag` (touch → tracker sees it) dominates and is bounded by the 2h cadence;
  `emit_lag` (detected → Telegram) is sub-second (PART 3).

**Implication:** paper-entry alerts are currently **not actionable for manual entry** in
any fast mode — by the time the alert fires, the trade is ~2h into (or past) its life.
This is the central driver for the latency-reduction plan (PART 4), the freshness label
(PART 5), and the manual-readiness verdict (PART 10).

**PART 2 status: DONE.**
