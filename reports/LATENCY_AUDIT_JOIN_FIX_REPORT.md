# Latency Audit Join Fix (PART 5)

**Date:** 2026-06-16

## Finding
The **canonical** audit (`scripts/audit_latency_expired.py::load_entry_rows`) already joins
paper-entry alerts to outcomes **by `signal_id`**:
```sql
SELECT signal_id, MIN(sent_at) AS sent_at, telegram_status
FROM signal_alerts WHERE alert_type='paper_entry' GROUP BY signal_id
```
So `entry_age_sec` in `ENTRY_DETECTION_LATENCY.csv` is correctly per-signal. **No bug in
the audit script.**

The unreliable join was in the **ad-hoc inline query** used during the live sanity check,
which matched alerts by `symbol+mode` (`WHERE symbol=? AND mode=? LIMIT 1`) and therefore
picked the wrong signal's alert (producing nonsensical negative ages like −7303m). That was
a throwaway query, not the audit tool.

## Action
- Confirmed `signal_alerts.signal_id` exists and is populated → signal_id linkage is the
  correct, available join key.
- Added a guard test `test_12_latency_audit_joins_by_signal_id` asserting the audit script
  contains `alert_type='paper_entry' GROUP BY signal_id` and does **not** contain the
  `symbol=? AND mode=?` linkage — locking in the correct join and preventing regression to
  the buggy pattern.
- Going forward, per-entry alert age must be reported only via the signal_id join; ad-hoc
  symbol+mode joins are banned (documented here + enforced by the test).

`detection_lag` (det − touch) is always reliable (it comes from the outcome rows
themselves, no alert join needed) and is the metric to trust when an alert row is absent.

**PART 5 status: DONE — canonical audit already correct; ad-hoc query was the defect, now
guarded by a test.**
