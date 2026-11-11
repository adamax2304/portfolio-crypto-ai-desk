# Tomorrow Schedule Setup Report — 2026-05-28

**Generated:** 2026-05-27 ~00:45 EEST
**Target run date:** **2026-05-28 (Thursday)**, Asia/Nicosia
**Author of automation:** safe wrapper around existing CLI — no scoring, agents, thresholds, or trading logic touched.

---

## 1. What was created

| File | Purpose |
|------|---------|
| `scripts/run_tomorrow_schedule.py` | Main scheduler. ~470 lines. Pure stdlib (argparse, subprocess, zoneinfo, logging). |
| `scripts/run_tomorrow_schedule.bat` | Windows wrapper that sets PYTHONIOENCODING=utf-8 + PYTHONPATH and launches the Python scheduler. Pauses only when launched interactively. |
| `data/scheduled_runs/2026-05-28/` (will be created at first launch) | Daily folder for logs + per-cycle Markdown + final review. |

The scheduler reuses **only existing CLI commands**:
- `track-signals --all`
- `scalp-report`
- `intraday-report`
- `stocks-intraday-report`
- `active-signals --asset-class crypto/stocks`
- `signal-stats --asset-class crypto/stocks`
- `monitor-watchlist --interval 600 --iterations N`
- `stocks-monitor-session --minutes N --interval-minutes 10 [--market-hours-only] --send-telegram`
- `alert-status --asset-class crypto/stocks`
- `python -m scripts.dedup_signal_stats` (read-only helper)

No new code paths, no new dependencies, no paid APIs.

---

## 2. Schedule (Asia/Nicosia)

| Cycle | Time (Nicosia) | Time (UTC) | Name | Steps | Includes monitor? |
|-------|---------------:|-----------:|------|------:|-------------------|
| `cycle_1` | **09:00** | 06:00 | Morning Crypto Check | 6 | no |
| `cycle_2` | **14:30** | 11:30 | Pre-US Market Check | 9 | no |
| `cycle_3` | **16:20** | 13:20 | US Open Full Monitor | 9 | **yes** (crypto 90 min + stocks 90 min) |
| `cycle_4` | **19:00** | 16:00 | Mid-US Session Refresh | 11 | **yes** (crypto 60 min + stocks 60 min) |
| `cycle_5` | **22:30** | 19:30 | Final Daily Review | 8 | no — final review only |

The full day takes the scheduler from 09:00 to roughly 23:00 EEST (Cycle 5 finishes within minutes). The scheduler sleeps between cycles — no spin loops, no polling.

---

## 3. Exact commands per cycle

Same as the spec; replayed here so the external reviewer doesn't need to open the script.

### Cycle 1 — 09:00
```
python -m src.cli track-signals --all
python -m src.cli scalp-report
python -m src.cli intraday-report
python -m src.cli active-signals --asset-class crypto --limit 20
python -m src.cli signal-stats --asset-class crypto
python -m src.cli track-signals --all
```

### Cycle 2 — 14:30
```
python -m src.cli track-signals --all
python -m src.cli scalp-report
python -m src.cli intraday-report
python -m src.cli stocks-intraday-report
python -m src.cli active-signals --asset-class crypto --limit 20
python -m src.cli active-signals --asset-class stocks --limit 20
python -m src.cli signal-stats --asset-class crypto
python -m src.cli signal-stats --asset-class stocks
python -m src.cli track-signals --all
```

### Cycle 3 — 16:20 (US Open)
```
python -m src.cli track-signals --all
python -m src.cli scalp-report
python -m src.cli intraday-report
python -m src.cli stocks-intraday-report
# crypto monitor (background, 90 min)
python -m src.cli monitor-watchlist --interval 600 --iterations 9
# stocks monitor session (foreground, 90 min, market-hours-only, Telegram on)
python -m src.cli stocks-monitor-session --minutes 90 --interval-minutes 10 --market-hours-only --send-telegram
python -m src.cli track-signals --all
python -m src.cli signal-stats --asset-class crypto
python -m src.cli signal-stats --asset-class stocks
```

### Cycle 4 — 19:00 (Mid US)
```
python -m src.cli track-signals --all
python -m src.cli scalp-report
python -m src.cli intraday-report
python -m src.cli stocks-intraday-report
# crypto monitor (background, 60 min, dedup-checked first)
python -m src.cli monitor-watchlist --interval 600 --iterations 6
python -m src.cli stocks-monitor-session --minutes 60 --interval-minutes 10 --market-hours-only --send-telegram
python -m src.cli track-signals --all
python -m src.cli active-signals --asset-class crypto --limit 20
python -m src.cli active-signals --asset-class stocks --limit 20
python -m src.cli signal-stats --asset-class crypto
python -m src.cli signal-stats --asset-class stocks
```

### Cycle 5 — 22:30 (Final Review)
```
python -m src.cli track-signals --all
python -m src.cli active-signals --asset-class crypto --limit 50
python -m src.cli active-signals --asset-class stocks --limit 50
python -m src.cli signal-stats --asset-class crypto
python -m src.cli signal-stats --asset-class stocks
python -m src.cli alert-status --asset-class stocks
python -m src.cli alert-status --asset-class crypto
python -m scripts.dedup_signal_stats
```

At the end of Cycle 5 the scheduler also writes `DAILY_AUTO_MONITOR_REVIEW_2026-05-28.md`.

---

## 4. Dry-run output (validated)

```
$ python -m scripts.run_tomorrow_schedule --dry-run
scheduler boot — date=2026-05-28 dry_run=True send_telegram=False
=== DRY RUN — no commands will be executed ===
cycle_1 (Morning Crypto Check) @ 2026-05-28T09:00:00+03:00 — 6 step(s)
cycle_2 (Pre-US Market Check) @ 2026-05-28T14:30:00+03:00 — 9 step(s)
cycle_3 (US Open Full Monitor) @ 2026-05-28T16:20:00+03:00 — 9 step(s)
cycle_4 (Mid-US Session Refresh) @ 2026-05-28T19:00:00+03:00 — 11 step(s)
cycle_5 (Final Daily Review) @ 2026-05-28T22:30:00+03:00 — 8 step(s)
--- validating CLI surface ---
validate track-signals              OK
validate scalp-report               OK
validate intraday-report            OK
validate active-signals             OK
validate signal-stats               OK
validate stocks-intraday-report     OK
validate monitor-watchlist          OK
validate stocks-monitor-session     OK
validate alert-status               OK
=== dry run complete ===
```

All 9 CLI commands the scheduler relies on respond to `--help`. No syntax or path errors.

---

## 5. Smoke-test output (real run of cycle_1)

```
$ python -m scripts.run_tomorrow_schedule --run-now cycle_1 --no-send-telegram --date 2026-05-27
scheduler boot — date=2026-05-27 dry_run=False send_telegram=False
CYCLE START: cycle_1 — Morning Crypto Check
CMD END: track-signals (pre)      exit=0  9.8 s
CMD END: crypto scalp report       exit=0  709.0 s
CMD END: crypto intraday report    exit=0  584.4 s
CMD END: active-signals (crypto)   exit=0  2.5 s
CMD END: signal-stats (crypto)     exit=0  2.7 s
CMD END: track-signals (post)      exit=0  10.0 s
CYCLE END: cycle_1 (telegram=skipped)
```

- **0 failed steps.**
- Telegram correctly skipped (--no-send-telegram).
- Daily folder + log + per-cycle Markdown were created:
  - `data/scheduled_runs/2026-05-27/scheduler.log`
  - `data/scheduled_runs/2026-05-27/cycle_1_morning_crypto_check.md`

Cycle 1 takes **~22 minutes wall-clock** mostly because crypto scalp + intraday reports each take ~10 minutes (Bybit derivatives fetch). Plan accordingly: tomorrow's Cycle 3 will run from 16:20 and finish around 18:10 because the 90-minute stocks monitor blocks the cycle (the crypto monitor runs in parallel in the background).

---

## 6. How to start it tomorrow

**Option A — manual launch in PowerShell (you can watch progress):**
```powershell
cd C:\Users\adama\Documents\crypto-ai-desk
.\scripts\run_tomorrow_schedule.bat
```
Leave the window open. The scheduler will sleep until 09:00 EEST and then start firing cycles. Logs stream to the window AND to file.

**Option B — Windows Task Scheduler (headless):**
1. Open Task Scheduler.
2. Create a Basic Task → "Crypto AI Desk daily".
3. Trigger: One time → start at **2026-05-28 08:55 EEST** (5 min before Cycle 1).
4. Action: Start a program.
   - Program/script: `cmd.exe`
   - Add arguments: `/c "C:\Users\adama\Documents\crypto-ai-desk\scripts\run_tomorrow_schedule.bat"`
   - Start in: `C:\Users\adama\Documents\crypto-ai-desk`
5. Run only when user is logged on (so Telegram + Python env work).
6. (Optional) "Run with highest privileges" if you ever bump into permission issues.

Either way it just calls the same Python script. Option A is easier; Option B is more "set and forget".

**Option C — run a single cycle manually:**
```powershell
python -m scripts.run_tomorrow_schedule --run-now cycle_3 --send-telegram
```
Useful if you want to test Telegram by triggering Cycle 3 now.

---

## 7. How to stop it

**While running:**
- `Ctrl+C` in the window. The scheduler catches `KeyboardInterrupt`, cleans up background monitors (kills the crypto-monitor child via `taskkill /F /T`), and exits cleanly. Daily folder + partial logs are preserved.

**If launched via Task Scheduler and you can't see a window:**
- Open Task Manager → find `python.exe` running `run_tomorrow_schedule` → End task.
- Then for safety, kill any leftover monitors: `Get-Process python | Stop-Process -Force` (this also stops *all* Python — use only if nothing else important is running).

**Lock files:**
- `data/scheduled_runs/2026-05-28/crypto_monitor.pid` is the PID of the background crypto monitor. The scheduler auto-cleans it at end of Cycle 3 and Cycle 4. Safe to delete manually if a crash leaves it behind.

---

## 8. Where logs are saved

```
data/scheduled_runs/2026-05-28/
├── scheduler.log                              # consolidated INFO log
├── cycle_1_morning_crypto_check.md            # per-step output + exit codes
├── cycle_2_pre-us_market_check.md
├── cycle_3_us_open_full_monitor.md
├── cycle_4_mid-us_session_refresh.md
├── cycle_5_final_daily_review.md
├── crypto_monitor_<unixtime>.log              # background crypto monitor stdout
├── crypto_monitor.pid                         # transient PID file (auto-cleaned)
└── DAILY_AUTO_MONITOR_REVIEW_2026-05-28.md    # final review (written at end of Cycle 5)
```

Each per-cycle Markdown shows: scheduled time vs actual start/finish, every command's argv + exit code + duration + last 6 KB of stdout. You can audit any cycle after the day completes.

---

## 9. What Telegram messages to expect tomorrow

**Per-cycle scheduler summary** (5 messages, one after each cycle):

```
[SCHEDULER] CYCLE_1 — Morning Crypto Check
started: 2026-05-28T09:00:00+03:00
finished: 2026-05-28T09:22:14+03:00
steps: ok=6 failed=0
see daily folder for full log.
```

**Plus existing alerts from the CLI commands themselves:**
- Crypto: `monitor-watchlist` already sends Telegram on tier promotions (B/A). No spam — built-in cooldown.
- Stocks: `stocks-monitor-session --send-telegram` sends one Telegram per new/materially-improved A/B (existing dedup logic). Per yesterday's 60-min session, this fired 1 new + 56 improvement alerts. Expect a similar burst at Cycle 3 (US open) if scores shift during the morning.
- C-tier and rejected ideas — **never alerted** (existing gate).

**Realistic expectation for tomorrow's Telegram inbox:**
- 5 scheduler summary pings (one per cycle).
- 0 crypto alerts if regime stays "transition mixed" (current state).
- Several stocks alerts at Cycle 3 if AAPL/LLY/AMD/etc. shift scores or entries by ≥5 points / 0.5 % during US open.
- 0–10 more during Cycle 4 (mid-session).
- 0 during Cycle 5 (review only).

If the inbox feels too noisy, you can:
- Run with `--no-send-telegram` to silence everything.
- Or call `python -m src.cli stocks-monitor-session --no-send-telegram …` directly for the next session — the scheduler's pings will still fire.

---

## 10. Known limitations

1. **No re-tier-upgrade rate-limit.** The stocks monitor sends a Telegram every time a setup's score crosses the ≥5 delta threshold. If the score oscillates, the same symbol could trigger 3–4 alerts in a 90-minute monitor session. Acceptable but worth knowing.
2. **`scalp-report` and `intraday-report` are slow** (~10 min each due to Bybit derivatives history fetch). Cycle 1 takes ~22 min; Cycle 2 takes ~30 min; Cycle 3 takes ~110 min (mostly because of the 90-min stocks monitor block); Cycle 4 takes ~80 min. Cycle 5 is fast (~30 sec). The scheduler accounts for this with generous timeouts.
3. **Market-hours gate is best-effort.** `stocks-monitor-session --market-hours-only` skips ticks outside US 13:30–20:00 UTC, Mon–Fri. It does not account for US holidays. 2026-05-28 is a regular Thursday — no issue.
4. **yfinance earnings 404s** still happen for SPY/QQQ/IWM/DIA/SMH/XLK/XLF/XLE/XLY/XLV. That's expected — ETFs have no earnings. Stocks ideas continue to surface "earnings: UNKNOWN" risk flag.
5. **No paid feeds.** Stocks RSS (MarketWatch / Yahoo / Seeking Alpha) remains disabled, so the news layer for stocks is still thin. Crypto RSS (Cointelegraph, CoinDesk, Decrypt, Binance Announcements) works normally.
6. **Scheduler is single-day.** Re-launching it after 2026-05-28 ends will write into the next day's folder automatically (default `--date` = today + 1).
7. **Crypto monitor mode follows last report.** If Cycle 3's intraday-report runs after the scalp-report (it does — see cycle definition), the crypto monitor will tick in **intraday** mode. If you specifically need scalp-mode monitoring, run scalp-report last by hand before launching Cycle 3.
8. **No auto-strategy modification.** This is a hard guarantee — the scheduler is read-only with respect to scoring, weights, thresholds, agent code, and risk caps.

---

## 11. Final answers (the 7 questions)

1. **Is tomorrow schedule ready?** Yes — dry-run passes, smoke-test passed (cycle_1 ran clean on today's date with 6/6 OK steps).

2. **What time each cycle will run?**
   - Cycle 1: 09:00 Nicosia
   - Cycle 2: 14:30 Nicosia
   - Cycle 3: 16:20 Nicosia (most important — US open)
   - Cycle 4: 19:00 Nicosia
   - Cycle 5: 22:30 Nicosia

3. **How do I start it?**
   - Easiest: double-click `scripts\run_tomorrow_schedule.bat` (or run it from PowerShell). Leave the window open until tomorrow.
   - Headless: Windows Task Scheduler with the .bat as Action, trigger at 08:55 EEST tomorrow.

4. **How do I stop it?** `Ctrl+C` in the window. It cleans up the background crypto monitor automatically. If launched via Task Scheduler, kill the parent `python.exe` from Task Manager.

5. **Where are logs?** `data/scheduled_runs/2026-05-28/`. Five per-cycle Markdowns + one consolidated `scheduler.log` + `DAILY_AUTO_MONITOR_REVIEW_2026-05-28.md` at the end.

6. **What Telegram messages should I expect?** 5 scheduler summary pings + monitor alerts (mostly stocks A/B improvements during Cycles 3 and 4). Estimate: 10–60 messages total tomorrow depending on US market activity.

7. **What risks/limitations remain?**
   - Possible alert bursts on score oscillation (see limitation 1).
   - Slow crypto reports (~10 min each — limitation 2).
   - No paid news feeds (limitation 5).
   - No earnings dates for many stocks (limitation 4).
   - **No auto-trading anywhere — guaranteed.**

---

## 12. Safety checklist (verified)

- ✅ No scoring changes
- ✅ No threshold changes
- ✅ No agent code touched
- ✅ No architecture refactor
- ✅ No paid APIs added
- ✅ No auto-trading possible (no order-placement code path exists in the project)
- ✅ Telegram only A/B (existing gates enforce this — scheduler does not bypass)
- ✅ De-dup honoured (stocks-monitor-session has built-in MaterialImprovementChecker)
- ✅ Failure-safe (each step wrapped, exceptions logged not raised)
- ✅ Stop-clean (Ctrl+C kills background monitor + clears lockfile)
- ✅ Dry-run validated
- ✅ Smoke-test passed (cycle_1, 6/6 OK steps)
