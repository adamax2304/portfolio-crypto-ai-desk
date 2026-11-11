# Latency Reduction Options (PART 4)

**Date:** 2026-06-16
**Problem (from PART 2):** paper-entry detection runs only inside `track-signals` (twice
per 2h cycle) → median entry-age **~135 min**. Telegram delivery is sub-second (PART 3),
so the entire fix target is the **detection cadence**.
**Current load context:** ~48 pending/active A/B signals across **~28 distinct symbols**
(15 crypto + 13 stocks) at any time — polling them is cheap.

**Full report cadence is NOT changed by any option here.** These only re-check
entry-touch / terminal-outcome for *existing pending/triggered A/B signals* — no scanner,
no LLM, no news refresh, no scoring rerun.

## Option comparison

| Dim | A: 60s pending-only tracker | B: monitor-tick entry check (5 min) | C: split crypto/stocks cadence | D: event-driven (websocket) |
|-----|------------------------------|--------------------------------------|--------------------------------|------------------------------|
| Latency target | **~60–90s** | **~5 min** | crypto 60–120s / stocks 60s RTH | **sub-second** |
| API calls/min | ~28 sym/min (trivial vs Binance ~1200 wt/min) | ~28 / 5min (negligible) | ~15 crypto/min + 13 stocks/min RTH | persistent ws streams |
| DB lock risk | **Medium** — writes `signal_outcomes`/status concurrently with the 2h full pass → SQLite write contention | **Medium** — same, but monitor already runs alongside | Medium (two writers) | Medium |
| Scheduler overlap risk | **Medium** — must not run while full `track-signals` writes; needs a pidfile/lock | **Low** — reuses the existing monitor process slot | Medium | Medium-High |
| Duplicate alert risk | **Low** — paper_entry deduped by `alert_type`; close deduped by `has_existing_close_alert`; new status-gates prevent same-tick double | Low (same dedup) | Low | Low |
| Latency improvement | ~135min → ~1min (**~99%**) | ~135min → ~5min (**~96%**) | best, session-aware | maximal |
| New dependency | none (reuse `track_active_signals`) | none | none | **ccxt.pro / websockets — FORBIDDEN (no new deps)** |
| Implementation risk | **Medium** (new lightweight CLI + lock + A/B-pending filter) | **Low–Medium** (wire entry-check into existing monitor) | High (most infra) | **High + dep** |

## Shared safety requirement for A / B / C

All three add a **second writer** to `signal_outcomes` / `proposed_signals.status`. SQLite
serializes writes; the existing scheduler already runs the 2h `track-signals` plus the
5-min crypto monitor and 10-min stocks monitor. To add a faster entry-detector safely we
**must**:
1. enable WAL mode (check current journal mode first),
2. guard the fast tracker with a **pidfile lock** so it never overlaps a full
   `track-signals` write pass,
3. restrict it to `tier IN (A,B) AND status IN (waiting_for_entry, triggered)` only
   (no full scan, no revalidation, no scoring),
4. keep `--paper-entry-alerts` dedup intact (already proven race-safe by PART 1 gates).

## Recommendation

**Phase 1 — implement now (zero cadence risk):** the **entry freshness label + late/terminal
shadow routing** (PART 5). This does not touch cadence at all; it makes the *existing*
late alerts honestly self-labelled and stops late/terminal entries from masquerading as
actionable. It is purely additive to the notification layer.

**Phase 2 — propose, do NOT implement in this pass:** **Option B** (entry detection on the
existing 5-min monitor tick) as the lowest-risk cadence win — reuses an existing process
slot, ~96% latency cut, dedup-safe. Promote to **Option A/C** (sub-minute) only if 5 min
is still too slow for intraday after Phase 1.
**Excluded:** Option D (needs a websocket/ccxt.pro dependency — violates the no-new-deps
constraint).

**Why not implement the cadence change now:** it introduces a second concurrent DB writer.
That is *probably* safe with WAL + a lock, but "probably safe" does not meet this task's
"implement only if **clearly** safe" bar without first confirming the journal mode and
adding+testing the lock against the live scheduler. So Phase 2 is specified and left for
explicit approval; Phase 1 (the label) is implemented now.

**PART 4 status: DONE — options analyzed; Phase-1 label implemented in PART 5.**

**UPDATE 2026-06-16: Phase-2 Option B has since been APPROVED and IMPLEMENTED** (WAL +
busy_timeout + full-pass marker + exclusive lock; A/B non-paused pending only; wired into
the 5-min monitor tick). See
[LATENCY_OPTION_B_PENDING_TRACKER_IMPLEMENTATION.md](LATENCY_OPTION_B_PENDING_TRACKER_IMPLEMENTATION.md).
