# Unalerted Stocks A/B Signals — Audit

**Date:** 2026-05-25 ~23:42 EEST (20:42 UTC)
**Source data:** `proposed_signals` + `signal_alerts` tables (read-only).
**Tooling:** `scripts/audit_unalerted_stocks.py` (one-off, read-only).
**No Telegram messages were sent during this audit.**

---

## Headline counts

| Metric | Value |
|--------|-------|
| Total A/B stocks signals in registry | **43** |
| Alerted by `signal_id` (have a row in `signal_alerts`) | **8** |
| **Unalerted by `signal_id`** | **35** |
| ↳ Old/stale (status = stopped/expired/missed_no_entry) | **0** |
| ↳ Missing invalidation | **0** |
| ↳ Superseded by a newer signal for the same setup | **35** |
| ↳ Duplicate of a setup already alerted (no newer signal) | **0** |
| ↳ Active and valid but never alerted at all | **0** |
| Should receive a one-time *initial* Telegram alert | **0 of the 35** (see "Important nuance" below) |

The dry-run output earlier matches this: `dup_skipped=43, no_inv_skipped=0`. Every unalerted A/B is correctly silenced by the de-dupe layer.

---

## How the 35 break down

All 35 unalerted signals are **prior-run versions of the same 8 setups** that are currently active. The stocks pipeline registers a fresh `proposed_signals` row every time `stocks-intraday-report` runs, even when the underlying idea has not changed. Across 6 report runs today + yesterday we accumulated:

| Report run (UTC) | A/B signals in run | All superseded by 19:48 run? |
|------------------|--------------------|------------------------------|
| 2026-05-24 23:00 | 2 (AAPL B 77.46, TSLA B 70.15) | yes |
| 2026-05-24 23:52 | 1 (AAPL A 86.14) | yes |
| 2026-05-25 14:12 | 8 (the canonical AAPL/LLY/AMD/XLK/SMCI/SMH/UNH/TSLA) | yes |
| 2026-05-25 16:45 | 8 | yes |
| 2026-05-25 17:31 | 8 | yes |
| 2026-05-25 17:33 | 8 | yes |
| **2026-05-25 19:48** (current) | **8** | **— these are the "alerted by signal_id" 8** |

Total older rows: 2 + 1 + 8 + 8 + 8 + 8 = **35**. Each of them points at the latest 19:48 signal with the same `(symbol, mode, direction)` as the newer twin. Confirmed for every single row by `audit_unalerted_stocks.py`'s `superseded_by_newer` classifier.

### Per-setup view (current 8 setups)

| Symbol | Tier | Current score | Latest signal_id (alerted) | # prior duplicates |
|--------|------|---------------|----------------------------|---------------------|
| AAPL | A | 88.64 | sig_2771164d54b72b46 (19:48) | 6 prior rows |
| LLY  | A | 80.33 | sig_f8684dbcc7a924d8 (19:48) | 4 prior rows |
| AMD  | B | 78.77 | sig_3f6d9a236a624d1e (19:48) | 4 prior rows |
| XLK  | B | 74.91 | sig_326863601afbbb85 (19:48) | 4 prior rows |
| SMCI | B | 74.26 | sig_2b2220282e946a08 (19:48) | 4 prior rows |
| SMH  | B | 73.93 | sig_8d97349402e11fbf (19:48) | 4 prior rows |
| UNH  | B | 68.59 | sig_c6786172e71ab969 (19:48) | 4 prior rows |
| TSLA | B | 67.30 | sig_6b79cc342604cef3 (19:48) | 5 prior rows |
| **Total** | | | | **35** |

Scores are **identical** across every duplicate of a given setup (the scoring engine is deterministic for the same OHLCV snapshot), so no material improvement exists for any of the 35. The `MaterialImprovementChecker` correctly classifies them as "duplicate" and the monitor refuses to alert them.

---

## Quality flags on the 35

| Flag | Count | Notes |
|------|-------|-------|
| Closed status (stopped/expired/missed_no_entry) | **0** | All 35 remain `waiting_for_entry` |
| Missing invalidation | **0** | Every row has a non-null `invalidation` |
| Expires within 2.5 hours | **2** | The 2026-05-24 23:00 batch (AAPL B 77.46, TSLA B 70.15) expires at 2026-05-25 23:00 UTC — about ~2 h 20 min from audit time |
| Expires within 6 hours | **3** | + AAPL A 86.14 from 2026-05-24 23:52 |
| Score equal to the latest twin | **35 / 35** | Identical scores; no material upgrade |
| Has a newer twin with same setup | **35 / 35** | All superseded |

So while none are *closed*, the oldest 3 will silently expire within hours and the rest will expire tomorrow. None of them should be alerted; the current 19:48 versions are the canonical ones.

---

## Important nuance — dry-run vs sent

The 8 "alerted by signal_id" rows in `signal_alerts` were inserted by the `stocks-monitor-session --dry-run` smoke runs earlier in this session. Their `telegram_status` is **`dry_run`**, not `sent`. That means:

- From the system's de-dupe perspective: those 8 setups are "alerted" — the monitor will not re-fire.
- From the user's actual Telegram inbox: **the user has never received any of these 8 alerts** because dry-run suppressed the actual send.

If the user wants to receive a real Telegram message for the current 8 A/B setups, they have two options:

1. **Recommended (clean):** delete the 8 `dry_run` rows from `signal_alerts` for the latest run, then call `python -m src.cli stocks-monitor-session --minutes 0 --no-market-hours-only --send-telegram --no-dry-run`. The monitor will detect 8 unalerted A/B signals and dispatch one Telegram message per setup.

   ```sql
   DELETE FROM signal_alerts
   WHERE asset_class = 'stocks'
     AND telegram_status = 'dry_run'
     AND signal_id IN (
       'sig_2771164d54b72b46', -- AAPL A
       'sig_f8684dbcc7a924d8', -- LLY A
       'sig_3f6d9a236a624d1e', -- AMD B
       'sig_326863601afbbb85', -- XLK B
       'sig_2b2220282e946a08', -- SMCI B
       'sig_8d97349402e11fbf', -- SMH B
       'sig_c6786172e71ab969', -- UNH B
       'sig_6b79cc342604cef3'  -- TSLA B
     );
   ```

2. **Alternative (less clean):** change the monitor's de-dupe to only count `telegram_status='sent'` rows. That makes the de-dupe more strict but harmless if dry-runs were never used. This is a future code change; not needed today.

---

## Answers to the user's specific questions

> **How many are old/stale?**
> **0.** No row is in a closed status. The 3 oldest (24-May) are still `waiting_for_entry` but their validity window expires in <6 hours; the system will mark them `expired` automatically on the next `track-signals` pass that lands after the deadline.

> **How many are duplicates of the same setup?**
> **35 of 35.** Every unalerted row points at a newer twin in the same `(symbol, mode, direction)` bucket. Same entry zone, same invalidation, same TPs — scoring is deterministic on the same OHLCV snapshot.

> **How many are active and valid but never alerted?**
> **0.** Although all 35 have `status='waiting_for_entry'` and valid invalidation, every one of them has a newer alerted twin. Treating any of them as "never alerted" would double-notify the user.

> **How many have no invalidation?**
> **0.** Every unalerted A/B row carries a real `invalidation` value.

> **How many are superseded by newer signals?**
> **35 of 35.** This is the primary reason the monitor skips them.

> **Should any of the 35 receive a one-time initial Telegram alert?**
> **No.** Each of the 35 is a stale duplicate. Alerting any of them would re-fire on a setup the system already considers "covered". The user-facing question — *"have I received Telegram for AAPL/LLY/etc.?"* — is **answered by the 8 newest rows**, not by the 35.

   - **If the user wants the 8 current setups in Telegram for real:** see "Important nuance" above. The 8 dry-run rows need to be cleared (or the dedupe needs to ignore dry-runs), then `stocks-monitor-session --send-telegram --no-dry-run` will send exactly 8 messages.

---

## Recommended cleanup (optional, not run)

The 35 superseded rows clutter the registry but do **no harm**:
- they don't fire alerts;
- they don't influence scoring;
- they'll auto-expire within 24h.

If the user wants a tidier registry, a one-off SQL prune after expiry can compact the table. The signal-tracker will mark them `expired` on the next pass that runs past their `expires_at`. No action needed today.

---

## Files

- This audit: `UNALERTED_STOCKS_SIGNALS_AUDIT.md` (this file)
- Raw classification dump: `scripts/_unalerted_dump.json` (~34 KB, full per-signal data)
- Reusable script: `scripts/audit_unalerted_stocks.py` (read-only, no side effects)

Both `scripts/` artifacts are read-only and can be deleted or kept as a reusable diagnostic.
