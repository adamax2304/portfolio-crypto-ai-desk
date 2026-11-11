# Option B — DB Concurrency Safety Verification (PART 4)

**Date:** 2026-06-16 ~11:16 UTC

## Findings

| Check | Result |
|-------|--------|
| Alert rows with `database is locked` / `OperationalError` status | **0** (all time) |
| `error:` statuses present | only `error:ConnectTimeout` (2), `error:ReadTimeout` (3) — **Telegram API** timeouts, not DB |
| `database is locked` / `OperationalError` / `disk I/O` / WAL errors in scheduler & monitor logs | **none found** |
| Stale lock files (`track_pending.lock`, `track_signals_full.running`) | **none** (`.locks/` empty) |
| Pending tracker overlap with full pass | **none possible** — lock + marker enforce mutual exclusion (unit-tested) |

## Mechanisms in place (verified)

- **WAL + `busy_timeout=30000` + `synchronous=NORMAL`** — confirmed live on the production
  DB. WAL permits readers during a write; busy_timeout makes a second writer wait up to 30s
  instead of erroring.
- **Full-pass marker** — the 2h `track-signals` writes `track_signals_full.running` while
  it runs; the pending pass checks it and **yields** (returns empty). Unit test:
  `test_pending_lock_yields_to_full_pass`, `test_track_pending_skips_under_full_pass`.
- **Exclusive pending lock** — only one pending pass runs at a time; a second caller gets
  `False` and skips. Unit test: `test_pending_lock_is_exclusive`.
- **Stale-lock auto-steal** — a lock/marker older than 30 min (dead process) is reclaimed.
- **Idempotence** — alert dedup + status gates mean even if both passes touched the same
  signal, no duplicate/again-fired alert results.

## Honest caveat

These mechanisms are **verified by unit tests and by the clean pre-Option-B history**, but
the **live concurrent-writer pattern** (5-min pending pass + 2h full pass writing the same
DB) has **not yet executed in production** — because the running monitor predates the
implementation (PART 1). No live concurrency incident can exist yet, so this is "no errors
+ mechanisms proven correct," not "observed clean under real concurrency." Re-check this
report's log scan after the next monitor cycle has run the new code for a few hours.

## Expectations vs observed

| Expectation | Status |
|-------------|--------|
| 0 DB lock errors | ✅ (0 in history; WAL+busy_timeout in place) |
| 0 overlap incidents | ✅ (lock+marker; unit-tested) |
| no stale locks after completion | ✅ (`.locks/` empty) |
| pending tracker fails safe if full pass running | ✅ (yields; unit-tested) |

**PART 4 status: DONE — no DB-lock/WAL issues; concurrency guards in place and unit-proven;
live-concurrency observation pending the next cycle.**
