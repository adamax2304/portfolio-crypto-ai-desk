# Latency Option B — Pending-Only Entry Tracker (Implementation)

**Date:** 2026-06-16 · Implements PART 4 Option B from
[LATENCY_REDUCTION_OPTIONS.md](LATENCY_REDUCTION_OPTIONS.md).

## Goal

Cut entry-detection latency from the ~2h `track-signals` cadence (PART 2: median ~135 min)
to ~5 min by detecting entry-touch / terminal outcomes for **tier A/B, non-terminal,
non-paused** signals on each existing **5-min crypto monitor tick** — with no full scan, no
scoring, no LLM, no news refresh.

## What changed

### 1. DB concurrency — `src/storage/sqlite.py`
`connect()` now sets `PRAGMA journal_mode=WAL`, `busy_timeout=30000`,
`synchronous=NORMAL`. Verified live on the production DB (`journal_mode=wal`,
`busy_timeout=30000`). This lets the 2h full writer and the 5-min lightweight writer
serialize safely instead of throwing "database is locked".

### 2. Lightweight pass + locks — `src/signals/tracker.py`
- `select_pending_ab_signal_ids(store)` — tier A/B, non-terminal, **excludes paper-paused
  stocks swing/invest** (they never alert). Production currently selects **181** signals
  (crypto intraday/scalp/swing + stocks intraday).
- `track_pending_entries(...)` — runs `track_active_signals` on exactly those signal_ids
  with the paper-entry notifier. Reuses the **same status gates + alert dedup**, so it is
  idempotent and can never double-fire vs the full pass.
- **Locks:** `full_pass_marker(root)` (the full `track-signals` writes a marker while it
  runs) + `_pending_lock(root)` (exclusive; the pending pass *yields* — returns an empty
  result — if the full pass is active or another pending tick holds the lock). Stale locks
  (>30 min, dead process) are auto-stolen.

### 3. Full pass marks itself — `src/cli.py` (`track-signals`)
The full `track_active_signals` call is wrapped in `full_pass_marker(root)` so the
lightweight pass yields to it.

### 4. Wired into the monitor — `src/cli.py` (`monitor-watchlist`)
New flag `--track-pending/--no-track-pending` (**default on**). Each tick, **after**
`re_evaluate` refreshes the OHLCV cache, the monitor runs `track_pending_entries`
(notifier passed only when Telegram is enabled; respects `--dry-run`). The scheduler's
crypto monitor (`monitor-watchlist --interval 300`) picks this up automatically.

## Expected latency after this change

- Crypto monitor runs the pending pass every **5 min** during its ~90-min/2h window →
  typical entry-detection latency **≤ ~5–10 min** (down from ~135 min), worst case ~35 min
  in the ~30-min/cycle monitor gap. **~96% reduction** in typical latency.
- Combined with the PART 5 freshness label: entries detected within 5 min now classify
  `fresh`/`acceptable` and **push as actionable** (instead of `late_shadow`). No further
  change needed — the label auto-adapts.

## Safety

- **Idempotent:** alert dedup (`has_existing_paper_entry_alert`, `has_existing_close_alert`)
  + status gates → no duplicate or simultaneous alerts even if both passes touch a signal.
- **No overlap:** pending pass yields to the full pass via the marker, and is exclusive
  with itself via the lock.
- **WAL + busy_timeout:** concurrent writes serialize, no lock errors.
- **Scoped:** A/B non-terminal only; paper-paused stocks swing/invest excluded; no scan,
  scoring, news, or LLM; no TP/SL/threshold change; no auto-trade.
- **Fails safe:** wrapped in try/except in the monitor — never blocks a tick.

## Tests — `tests/test_pending_tracker_option_b.py` (6, all pass)

WAL/busy_timeout enabled; A/B-pending scoping (excludes C-tier, terminal, paused stocks);
lock yields to full pass; lock is exclusive; pending pass is a no-op under the full-pass
marker. Plus the full focused regression (alert/scalp/telegram/sizing) stays green (100
passed) and DB/tracker suites green (97 passed).

## Rollout

No scheduler edit required — the crypto monitor already runs `monitor-watchlist
--interval 300`, and `--track-pending` defaults on, so the next monitor process picks it
up. Disable with `--no-track-pending` if ever needed.

**Status: IMPLEMENTED + TESTED.** Re-run the PART 2 latency audit after a few live monitor
cycles to confirm the measured drop, then re-evaluate intraday manual readiness (PART 10).
