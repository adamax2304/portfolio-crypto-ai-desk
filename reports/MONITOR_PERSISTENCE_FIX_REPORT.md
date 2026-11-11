# Monitor / Scheduler Persistence — Fix Report (PART 2/3/5)

**Date:** 2026-06-18 ~15:40 UTC · **Type:** operational fix. **No trading logic / scoring / TP-SL / routing / live changed.**

## What was built

### 1. Idempotent, dup-guarded launcher — `scripts/start_monitor_scheduler.ps1` (+ `.bat`)
- **Duplicate protection:** queries `Win32_Process` for any live `python … run_default_market_schedule`; if found, **exits without starting a second** (verified — see §Tests).
- Two modes:
  - **default (detached):** `Start-Process` (hidden) → not parented to the calling shell, so it survives terminal/session close. Used for manual start.
  - **`-Foreground`:** runs the loop inline so **Task Scheduler owns the long-lived process** and its restart-on-failure applies. Used by the task.
- Wraps the existing proven `scripts/autostart_scheduler.bat` (infinite-restart loop, 20s back-off, self-redirect to `data/autostart/scheduler.log`).
- Records pid to `data/autostart/scheduler_runner.pid`; logs to `logs/monitor_scheduler_stdout.log` / `…_stderr.log`; sends a **"Monitor started"** Telegram heartbeat on launch (best-effort, never fails the launch).

### 2. Heartbeat watchdog — `scripts/monitor_heartbeat.py` (+ `.bat`)
- **Checks:** scheduler process liveness **+ uptime**; last `CYCLE END` (`scheduler.log`); last alert / outcome / signal (trading DB, **read-only**); intelligence cache freshness (`intelligence.sqlite`).
- **Telegram events (plain-text, emoji-safe):**
  - `--event start` → "🟢 Monitor started".
  - `--event cycle` → compact per-cycle "🟢 Monitor cycle OK".
  - `--event check` (watchdog) → "🟢 Monitor OK …" when healthy, or **deduped ⚠ warning** when the process is gone or **stuck** (alive but no tracking update beyond one full cycle window).
- **Dedupe/cooldown:** per-key (`warn`/`ok`) state in `data/autostart/heartbeat_state.json`, **60-min cooldown** — no spam, ≤1 heartbeat per cycle.
- **`--auto-restart`:** restarts **only when the process is actually gone/unknown** (never kills a live, possibly-slow scheduler mid-cycle) via `Start-ScheduledTask CryptoAIDeskMonitor` (clean task-owned launch; falls back to the launcher).
- **False-alarm guard:** staleness is gated on **process uptime** so a freshly-started scheduler (old outcomes until its first cycle completes) is not flagged.

### 3. Scheduled tasks (Variant B — Task-Scheduler-service owned, survives session/terminal/reboot-while-logged-in)
| Task | Trigger | Settings | Purpose |
|---|---|---|---|
| **`CryptoAIDeskMonitor`** (new) | `-Once @ now-1min` + **StartWhenAvailable** | `-Foreground`, **RestartCount=3 / 5 min**, `ExecutionTimeLimit=∞`, **MultipleInstances=IgnoreNew** | Primary persistent runner. Auto-starts now; **re-runs ASAP after reboot** (missed `-Once` + StartWhenAvailable); task-owned restart-on-failure. |
| **`CryptoAIDeskHeartbeat`** (new) | `-Once @ now` + **repeat every 20 min** + StartWhenAvailable | `ExecutionTimeLimit=5 min`, MultipleInstances=IgnoreNew | Independent watchdog: warns + auto-restarts; also recovers after reboot. |
| **`CryptoAIDesk_Scheduler`** (old) | — | **DISABLED** | Was dormant since 6/15, **no dup-guard, no restart-on-failure** → disabled to remove duplicate risk. |

**Why not the old task / not `-AtLogon`:** re-registering `CryptoAIDesk_Scheduler` and any `-AtLogon` trigger returned **Access denied** (the old task is elevated/protected; logon-trigger registration needs elevation in this environment). The chosen `-Once + StartWhenAvailable` design needs **no elevation** and still gives reboot recovery.

## Persistence coverage (honest scope)
| Failure | Recovered by | Covered |
|---|---|---|
| Agent session / turn ends | task is service-owned, not session-child | ✅ |
| Terminal / console closed | detached + service-owned | ✅ |
| Scheduler python crash | `autostart_scheduler.bat` 20s restart loop **+** task RestartCount=3 **+** 20-min heartbeat auto-restart | ✅ (triple) |
| Whole runner tree killed | 20-min heartbeat `Start-ScheduledTask CryptoAIDeskMonitor` | ✅ (≤20 min gap) |
| Reboot **while user stays logged in** | `StartWhenAvailable` re-runs missed `-Once` ASAP | ✅ |
| Full **log-off** (not just lock/reboot) | tasks are `LogonType Interactive` (no stored password) → pause until next logon | ⚠ **not covered** (see below) |

**Residual manual note:** tasks run interactively (no password stored — credential entry is out of scope). They run while the user is logged in and resume after reboot+login, but a deliberate **log-off** pauses them. For a desktop that stays logged in over the 2-day forward test this is fine. To add log-off/AtLogon resilience, run **once in an elevated PowerShell**:
```powershell
$me=\"$env:USERDOMAIN\$env:USERNAME\"
$a=New-ScheduledTaskAction -Execute 'C:\Users\adama\Documents\crypto-ai-desk\scripts\start_monitor_scheduler.bat' -Argument '-Foreground'
$t=New-ScheduledTaskTrigger -AtLogOn
$s=New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 5) -ExecutionTimeLimit ([TimeSpan]::Zero) -StartWhenAvailable
Register-ScheduledTask -TaskName 'CryptoAIDeskMonitor' -Action $a -Trigger $t -Settings $s -Principal (New-ScheduledTaskPrincipal -UserId $me -LogonType Interactive) -Force
```

## Tests / verification (PART 5)
- **Focused suite: 86 passed** — `test_shadow_intelligence_layer` + `test_paper_entry_alerts` (intel block + SL line + ≤3 intel lines + no markdown crash) + `test_default_market_schedule` (plan) + `test_telegram_standardization`.
- **Heartbeat:** dry check before start correctly reported `scheduler_alive=false` + stale; after start `scheduler_alive=true`, uptime 1.4 min, `problems: []`, `last_outcome` already refreshed to 15:39 UTC. Sent clean "Monitor OK".
- **Duplicate-lock:** invoking the launcher again while alive → "scheduler already running — not starting a duplicate"; instance count stayed **1 → 1**. ✅
- **Scheduler dry-run plan:** cycle 1 = 24 steps (weekday, stocks on), others 20; **"LLM-auto-invoke check OK — no Opus/Claude tokens in plan"**; no live/execution steps.
- **Project-state docs:** `check_project_state_docs` → OK.

## Trade-math locks (all unchanged ✅)
live off · auto-live off · exchange execution off · crypto scalp actionable off · stocks scalp production off · TP/SL unchanged · scoring unchanged · thresholds unchanged · routing/actionability unchanged · BE/partial/trailing disabled · sector-cap value unchanged. The fix only (re)starts and watches the existing scheduler.

## Verdicts
**MONITOR_PERSISTENCE_READY · MONITOR_HEARTBEAT_READY** (no NEEDS_MANUAL_START, no NEEDS_FIX).
