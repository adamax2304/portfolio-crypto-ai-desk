# 12-Hour Monitor — Setup Report

**Created:** 2026-05-29 ~04:05 EEST
**Scope:** scheduling/automation only. No scoring/threshold/agent/architecture changes. No auto-trade.

---

## 1. What was created

| File | Purpose |
|------|---------|
| `scripts/run_12h_monitor_schedule.py` | 12-hour, 6-cycle, every-2-hour scheduler (~520 lines, pure stdlib) |
| `scripts/run_12h_monitor_schedule.bat` | Windows wrapper (passes args through; defaults to 12h/2h/Telegram-on) |
| `data/scheduled_runs/<date>_12h_monitor/` | Per-session log folder (auto-created) |

---

## 2. Schedule logic

- **6 regular cycles**, one every **2 hours** (12h total).
- **Swing / invest run ONCE** at cycle 1 only (`swing-report`, `stocks-swing-report`, `stocks-invest-report`) — they change slowly, so they are not repeated every 2h (avoids registry pollution + Telegram spam).
- **US-window cycles are high-priority**: if a cycle starts inside US pre-market (15:30–16:30), open (16:30–17:30), mid (18:30–20:00), or close (22:00–23:00) Nicosia → it appends a 60-min stocks monitor + a background crypto monitor.
- Regular cycle steps: `track-signals` → `scalp-report` → `intraday-report` → `stocks-intraday-report` → [US monitors if window] → `active-signals` ×2 → `signal-stats` ×2 → `track-signals` (post).

**Note on US windows:** they only trigger if a cycle's clock time lands inside the window. A session started at 03:52 finishes at 15:52 and therefore hits **0 US windows**. Start the session later in the day (e.g. ~14:00–15:00 EEST) if you want the US-open monitor cycle included.

---

## 3. Exact command to START

```powershell
cd C:\Users\adama\Documents\crypto-ai-desk
.\scripts\run_12h_monitor_schedule.bat --hours 12 --interval-hours 2 --send-telegram
```

Or directly:

```powershell
cd C:\Users\adama\Documents\crypto-ai-desk
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONPATH='.'
python -m scripts.run_12h_monitor_schedule --hours 12 --interval-hours 2 --send-telegram
```

Leave the window open. The scheduler runs cycle 1 immediately, then every 2 hours, writes a final review at the end, and exits.

### Optional: true headless via Task Scheduler (no admin needed for current user)

```powershell
schtasks /create /tn "CryptoAIDesk_12h" ^
    /tr "C:\Users\adama\Documents\crypto-ai-desk\scripts\run_12h_monitor_schedule.bat" ^
    /sc once /sd 29/05/2026 /st 14:00 /f
schtasks /run /tn "CryptoAIDesk_12h"
```
(date format is dd/mm/yyyy on this machine). This survives Claude/terminal closure because Task Scheduler owns the process.

---

## 4. Exact command to STOP

**While running in a window:** `Ctrl+C` — the scheduler catches it, kills any background crypto monitor, removes the lockfile, and exits cleanly.

**If launched via Task Scheduler / window lost:**
```powershell
# find the scheduler process
Get-WmiObject Win32_Process -Filter "Name='python.exe'" |
  Where-Object { $_.CommandLine -like '*run_12h_monitor_schedule*' } |
  Select-Object ProcessId, CommandLine
Stop-Process -Id <PID> -Force
# if a Task Scheduler entry exists:
schtasks /end /tn "CryptoAIDesk_12h"
schtasks /delete /tn "CryptoAIDesk_12h" /f
```

---

## 5. Logs path

```
data/scheduled_runs/2026-05-29_12h_monitor/
├── scheduler.log                # consolidated INFO log
├── cycle_1_summary.md           # per-step output, exit codes, durations
├── cycle_2_summary.md
├── ... cycle_6_summary.md
├── crypto_monitor_<unixtime>.log  # background crypto monitor stdout (US cycles)
├── crypto_monitor.pid           # transient PID file (auto-cleaned)
└── final_12h_review.md          # end-of-session review
```
Plus `FINAL_12H_MONITOR_REVIEW.md` is mirrored to the project root at session end.

Each cycle summary contains: start/end time, US window, ok/failed step counts, swing-included flag, and the last 5 KB of each command's stdout.

---

## 6. Dry-run result

`python -m scripts.run_12h_monitor_schedule --dry-run` → **PASS**.

- Plan preview printed 6 cycles (+swing/invest on cycle 1).
- All **12 CLI commands validated OK**: track-signals, scalp-report, intraday-report, stocks-intraday-report, swing-report, stocks-swing-report, stocks-invest-report, active-signals, signal-stats, monitor-watchlist, stocks-monitor-session, alert-status.

---

## 7. Smoke-test result

`python -m scripts.run_12h_monitor_schedule --minutes 10 --interval-minutes 5 --skip-reports --no-send-telegram` → **PASS**.

```
CYCLE 1 END ok=6 failed=0 telegram=skipped   (03:54)
CYCLE 2 END ok=6 failed=0 telegram=skipped   (04:00)
Final review written: ...final_12h_review.md (and root FINAL_12H_MONITOR_REVIEW.md)
12h monitor session complete — 2 cycle(s)
```

Verified:
- ✅ Loop fires cycles on the interval.
- ✅ `track-signals`, `active-signals`, `signal-stats` execute (exit 0).
- ✅ Per-cycle summaries written (`cycle_1_summary.md` 21 KB, `cycle_2_summary.md` 21 KB).
- ✅ Final review written to both the day folder and project root.
- ✅ `scheduler.log` written.
- ✅ `--no-send-telegram` honoured (`telegram=skipped`).
- ✅ `--skip-reports` skipped the slow report steps so the smoke completed in 10 min.

(The smoke used `--skip-reports` so it would finish inside 10 minutes. A full cycle including `scalp-report` + `intraday-report` takes ~22 min — that is exercised in production, not in the smoke.)

---

## 8. Telegram behaviour

- Per-cycle summary ping: `[12H MONITOR] cycle N/6 (priority) / steps: ok=X failed=Y`.
- A/B alerts only, via the existing CLI gates (stocks-monitor-session + watchlist monitor). C-tier / rejected / no-invalidation / stale / duplicate are all blocked in code.
- Plain-text send (`parse_mode=""`) + 3800-char cap → avoids the HTTP-400 Markdown bug seen in the earlier scheduler.

---

## 9. Remaining risks / limitations

1. **PC must stay awake.** `time.sleep()` is suspended on sleep/hibernate → cycles run late or skip. Disable sleep, keep on power.
2. **Window/Claude dependency.** If launched from a terminal or Claude background, closing it kills the process. Use the Task Scheduler option (§3) for true autonomy.
3. **US windows depend on start time.** A pre-15:30 start that ends before 15:30 hits no US window (no monitor cycle). Start ~14:00 EEST to capture US open.
4. **Crypto alerts are low-frequency** (legacy `watchlist_alerts` path) vs stocks (`signal_alerts`). Known asymmetry; not changed.
5. **Stocks stats inflated** by repeat registrations — final review includes a deduped view; trust that.
6. **Obsidian logging dormant** — not written by this scheduler (SQLite registry + signal-stats cover the same info).
7. **Swing/invest reports** run once at cycle 1; if cycle 1 fails, they won't retry this session.

---

## 10. Physical requirements before you leave

- ✅ Plug in to power.
- ✅ Settings → Power → Screen & sleep → both timers **Never** (today).
- ✅ Win+L (lock) is fine — session stays alive.
- ❌ Do NOT sleep / hibernate / shut down / sign out.
- ✅ Keep the PowerShell window open (unless using Task Scheduler).

---

## Safety confirmation

- No auto-trades. No scoring / threshold / agent / architecture changes. Only existing CLI commands invoked. Telegram A/B-only via existing gates. Failure-safe (each step wrapped). Dedup view in final review. Crypto/stocks isolated.
