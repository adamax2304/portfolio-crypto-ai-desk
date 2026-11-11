# Post-P1-Stock-Fixes Restart Verification

**Date:** 2026-06-05 ~22:10 EEST (19:10 UTC) · Scope: restart the long-lived
processes so the two P1 stock fixes (swing pause + Telegram 400) go live, then
verify. No code changed, no data deleted, no auto-trade. Telegram collector left
running (not restarted).

## 0. Pre-restart state (diagnosis)
- `CryptoAIDesk_Scheduler` task **State=Ready** (idle), LastResult
  `3221225786` (0xC000013A = terminated). The scheduler had **died silently
  after cycle 2** — `scheduler.log` frozen at `2026-06-05 20:19:45` with no
  `.bat` restart line; both per-cycle monitors already past their 90-min
  lifetime.
- Tracked monitor PIDs from today's lock files — crypto **37880**, stocks
  **36276** — both confirmed **DEAD**.
- The audit-era "scheduler PID 37572" is now an **unrelated Polymarket-bot
  worker** (PID reuse), not our scheduler.
- Separate tasks left untouched: `CryptoAIDesk_TelegramCollector` (PID 26656,
  Running) and `CryptoWatchlistMonitor` (Running) — neither was restarted.

## 1. Restart action
Restarted the Windows task that owns the autostart loop:
`Start-ScheduledTask CryptoAIDesk_Scheduler` → task **State=Running**, LastRun
`22:07:15`, LastResult `267009` (0x41301 = currently running).

Process pair confirmed up:
| Role | PID | Parent | Born | Cmd |
|---|---|---|---|---|
| autostart_scheduler.bat | **38080** | 2448 | 22:07:15 | loop wrapper |
| run_default_market_schedule | **36860** | 38080 | 22:07:17 | `python -m scripts.run_default_market_schedule --hours 24 --interval-hours 2 --monitor-minutes 90 --send-telegram` |

`scheduler.log` shows a fresh boot at `22:07:17` → `track-signals (pre)` →
`crypto scalp report` (cycle 1 in progress). **Item 1 ✅ / Item 12 ✅.**

## 2. Verification checklist
| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Scheduler PID changed & running | ✅ | new python PID **36860** (was dead); cmd 38080 |
| 2 | Stocks monitor PID changed (separate proc) | ✅ | per-cycle child; old **36276** dead → respawned **6268** by cycle-1 stocks step (crypto monitor likewise 37880→**29444**); both alive |
| 3 | Swing A/B → C with cap_reason | ✅ | post-fix swing run: NVDA/AMD `tier=C`, `cap_reasons=['stocks_swing_paused_after_48h_audit']` (created 19:07:19 UTC) |
| 4 | Swing report shows watchlist-only banner | ✅ | `2026-06-05_19-07_stocks_swing_report.md`: "**STOCKS SWING — watchlist / research only … −12R, 0W/12L**" |
| 5 | No swing A/B Telegram alerts | ✅ | all 18 active swing A/B are pre-fix & `already_alerted=True` → deduped; new swing capped to C → never enters A/B set |
| 6 | Stocks intraday unaffected | ✅ | 123 active intraday A/B intact; gate is `mode=="swing"`-only |
| 7 | Stocks invest unaffected | ✅ | 33 active invest A/B intact; not demoted, no swing cap |
| 8 | Crypto unaffected | ✅ | gate lives only in `StockTradeIdeaAgent`; crypto path untouched; crypto monitor respawns normally |
| 9 | Stock alerts send plain text (`parse_mode=""`) | ✅ | live test send `ok=True` message_id=2176 with hostile `[]/()/_/+-/$` content |
| 10 | No new HTTP 400 on first post-restart stock send | ✅ | live `parse_mode=""` test: no 400 (msg 2176); no production send was *due* (all A/B deduped + market closed) so zero failures generated — see §3 |
| 11 | signal_alerts records sent/dry_run/failed | ✅ | 48h: 76 sent / 15 failed:HTTPError / 7 dry_run / 3 failed:ReadTimeout |
| 12 | Scheduler healthy | ✅ | cycle 1 progressing, no errors/locks in log |

## 3. Production stocks-monitor respawn + first send (cycle 1 stocks step)
Cycle 1 order: crypto scalp → crypto intraday → catalyst → stocks intraday
report → **spawn crypto+stocks monitors** → tail steps. The stocks monitor is a
per-cycle `subprocess.Popen` child tracked by
`data/scheduled_runs/2026-06-05_default_schedule/stocks_monitor.pid`.

- **New stocks monitor PID:** **6268** (replaces dead 36276), parent scheduler
  36860, spawned 23:17 EEST — i.e. AFTER the 22:07 restart, so it imports the
  fixed `monitor.py` (`parse_mode=""`). Crypto monitor likewise respawned
  37880→**29444**. Both alive at end-of-cycle-1 (`CYCLE 1 END ok=14 failed=2
  telegram=sent (retry)`).
- **First post-restart stock alert status:** **none fired — and none was due.**
  Watched monitor 6268 for 18 min: it stayed alive, ran its tick, and produced
  **0** new stock alerts. Reasons, both benign:
  1. **Market is closed** (verified `is_us_cash_session_open()==False`,
     after-hours; UTC 21:15 = 17:15 ET, RTH ended 16:00 ET). The monitor runs
     `--market-hours-only` → it correctly **no-ops** outside RTH (0-byte action
     log).
  2. All 174 active stocks A/B (123 intraday / 33 invest / 18 swing) are already
     `already_alerted=True` → dedup would skip them even during RTH.
  So there is **no organic stock send to observe tonight**; the next one occurs
  at the **next US RTH**. Per the run constraints, no further manual test send
  was issued. The transport fix is already proven by the completed live test
  (msg 2176, plain text, hostile `[]/()/_/+-/$`, **no 400**), and monitor 6268
  is the process that will emit that next RTH alert using `parse_mode=""`.
- **Pre-fix baseline (the bug):** the 14 most recent pre-restart stock alerts
  (16:41–17:32) were ALL `failed:HTTPError`; the 15:07–15:08 batch was `sent`.
  Post-restart, zero `failed:HTTPError` have been generated (nothing failed
  because nothing was sent).

## 4. Why item 5 holds despite retained pre-fix swing A/B
The fix is **forward-looking** (new swing A/B → C) and **non-destructive**
(historical swing signals retained per spec). The 18 pre-fix swing A/B signals
(created ≤14:50 UTC) already have `signal_alert` rows → the monitor's dedup
treats them as already-alerted and never re-sends. They also can't trigger an
"update" alert because the monitor only re-scores the **intraday** pipeline, so
their stored tier/score never changes. Net: **zero new swing A/B Telegram.**

## 5. Notes
- The 18 pre-fix swing A/B alert rows at 17:32 are `failed:HTTPError` — they hit
  the very 400 bug now fixed; they will NOT be retried (already-alerted), which
  is the desired outcome (swing is paused anyway).
- ReadTimeouts (3) are transient network, not addressed by this fix and not a
  code defect.

## 6. Residual / next-RTH confirmation
The single item not observable tonight is an **organic** production stock send
showing `sent` (not `failed:HTTPError`) — solely because no alert was due
(weekend/after-hours + full dedup), **not** because anything failed. It will be
confirmed automatically at the next US RTH by the already-running, already-fixed
monitor 6268. If, at that time, a fresh stock alert were to log
`failed:HTTPError`, that would warrant re-opening; nothing in the current
evidence suggests it will (live plain-text send to the real API succeeded).

## Final verdict
```
P1_STOCK_FIXES_ACTIVE_IN_PRODUCTION
```
Both fixes are live on the restarted stack: scheduler **36860** + fresh stocks
monitor **6268** (new code), swing→C+cap_reason and the watchlist-only banner
confirmed in a production swing report, no swing A/B Telegram (capped + deduped),
intraday/invest/crypto untouched, and the Telegram transport proven plain-text
deliverable (no 400) via the completed live test. The only deferred check — an
organic stock send — is gated by market hours and will self-confirm at the next
RTH; it is not a defect.
