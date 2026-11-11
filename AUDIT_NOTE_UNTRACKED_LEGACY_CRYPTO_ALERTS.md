# Audit Note — Untracked Legacy Crypto Alerts

**Status:** non-invasive audit note. Scheduler is RUNNING and was NOT stopped or modified. No code changed. No scoring/threshold changes. No auto-trade.

**Opened:** 2026-05-29 ~14:15 EEST, during the 12h-monitor run (cycle 1 done, cycle 2+ pending).

---

## The gap

Crypto alerts are sent via the **legacy `watchlist_alerts`** path
(`Supervisor._maybe_send_trade_alerts`). Some of these Telegram alerts have
**no matching row in `proposed_signals`**, so:

- they are **not trackable** by `track-signals`;
- they will **never contribute** to crypto PF / winrate / avgR / totalR;
- they appear in Telegram but vanish from the performance record.

This was first noticed for XLM/USDT, but a full scan shows it is broader.

## Detected untracked legacy crypto alerts (today, 2026-05-29)

| symbol | tier | mode | score | direction | sent_at (UTC) | trackable |
|--------|------|------|------:|-----------|---------------|-----------|
| UNI/USDT | B | scalp | 65.5 | short | 08:36:22 | ❌ NO |
| BCH/USDT | B | scalp | 72.1 | short | 08:45:52 | ❌ NO |
| XLM/USDT | B | swing | 65.4 | long | 10:56:53 | ❌ NO |
| INJ/USDT | B | swing | 66.1 | long | 11:36:14 | ❌ NO |

**4 untracked legacy crypto alerts.** Note it affects **both scalp and swing**
(not only swing). The two scalp shorts (UNI, BCH) fired at 08:36/08:45 UTC
(before this 12h run's cycle 1 boot at 10:10 UTC), so the legacy path has been
emitting untracked alerts across processes, not just inside this scheduler.

Detector: `scripts/detect_untracked_legacy_alerts.py` (read-only; matches a
crypto `watchlist_alerts` row to a `proposed_signals` row of the same symbol
within ±6h; lists any with no match).

---

## How this will be surfaced going forward (no code change)

The running scheduler's auto-generated `cycle_N_summary.md` files are produced
by the **already-running** Python process, so a new "Untracked Legacy Crypto
Alerts" section cannot be injected into them without restarting the scheduler
(which you asked me not to do).

Instead, the section is produced **on demand** by the detector and will be:
- included in the **final 12h review** (appended when the run completes);
- runnable any time mid-run via:
  ```
  python -m scripts.detect_untracked_legacy_alerts --since 2026-05-29
  ```

This keeps the running schedule untouched while still giving you the section.

---

## Recommendation (decision deferred to end of 12h run)

Per your instruction, the final recommendation will be made at the end of the
12-hour session. Current lean, to be confirmed against the full-day data:

1. **Migrate legacy crypto alerts into `proposed_signals`** — best long-term:
   makes every crypto alert trackable, unifies crypto with the stocks
   `signal_alerts` model. Larger change; do it as a dedicated patch AFTER the
   schedule ends, not during.
2. **Keep separate but mark as untracked** — lowest effort: keep the detector
   as the audit layer; accept that legacy crypto alerts are "notify-only".
   Safe but leaves a permanent blind spot in crypto PF/winrate.
3. **Disable legacy swing/scalp alerts until trackable** — stops the blind-spot
   alerts entirely; you would lose crypto Telegram alerts until option 1 ships.

**Preliminary preference:** option **1** (migrate), implemented as a separate
patch once the schedule is idle — it preserves alerts AND makes them trackable.
Option 2 is the safe interim if you want zero code change. Option 3 only if the
untracked alerts are causing confusion.

**Do NOT implement now** — the schedule is running and no fix is required for it
to keep working. Revisit when the 12h run finishes.

---

## Safety

- Scheduler NOT stopped, NOT modified.
- No code / scoring / threshold / agent changes.
- Detector is read-only.
- No auto-trade.
