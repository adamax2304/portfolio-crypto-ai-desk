# Default Schedule — Windows Task Scheduler instructions

How to run `run_default_market_schedule.py` from a Windows session, by
hand or via Task Scheduler.

---

## Option A — Run manually in PowerShell (simplest)

```powershell
cd C:\Users\adama\Documents\crypto-ai-desk
.\scripts\run_default_market_schedule.bat --hours 24 --interval-hours 2 --send-telegram
```

Other useful invocations:

```powershell
# Crypto-only (e.g. weekend or stocks-off override)
.\scripts\run_default_market_schedule.bat --crypto-only

# Run just one cycle and exit (for spot-checks)
.\scripts\run_default_market_schedule.bat --run-once

# Dry-run (validate plan + CLI surface, no subprocess calls)
.\scripts\run_default_market_schedule.bat --dry-run

# Short smoke test (no Telegram)
python -m scripts.run_default_market_schedule --minutes 6 --interval-minutes 3 --monitor-minutes 1 --skip-reports --no-send-telegram
```

The script runs in the foreground. **Keep the PowerShell window open**;
closing it terminates the scheduler.

---

## Option B — Register with Windows Task Scheduler (no admin needed)

Use the GUI (`Task Scheduler` → `Create Basic Task`) OR run this in
PowerShell (no elevation required; runs as your user):

```powershell
$action  = New-ScheduledTaskAction `
    -Execute "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" `
    -Argument "-m scripts.run_default_market_schedule --hours 24 --interval-hours 2 --send-telegram" `
    -WorkingDirectory "C:\Users\adama\Documents\crypto-ai-desk"

# Daily at 08:00 local time
$trigger = New-ScheduledTaskTrigger -Daily -At 8am

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable

Register-ScheduledTask `
    -TaskName "CryptoAIDesk_Default_24h" `
    -Action $action -Trigger $trigger -Settings $settings `
    -Description "crypto-ai-desk default schedule (24h, every 2h, crypto + stocks weekdays)" `
    -RunLevel Limited
```

Adjust the Python path (`python.exe`) to match `where python` output on
your machine.

### Verify the task

```powershell
schtasks /Query /TN "CryptoAIDesk_Default_24h"
Get-ScheduledTaskInfo -TaskName "CryptoAIDesk_Default_24h"
```

### Stop the task

```powershell
schtasks /End /TN "CryptoAIDesk_Default_24h"          # stop a running instance
schtasks /Delete /TN "CryptoAIDesk_Default_24h" /F   # remove the entry
```

### Where the logs are

```
data\scheduled_runs\<YYYY-MM-DD>_default_schedule\
    scheduler.log                       # full event log
    cycle_NN_HH-MM_summary.md           # per-cycle dump
    crypto_monitor_*.log                # background crypto monitor stdout
    daily_<date>.done                   # marker, set after first long-horizon pass
    final_daily_default_schedule_review.md
```

A copy of the final review is also written to project root as
`FINAL_DAILY_DEFAULT_SCHEDULE_REVIEW.md`.

### Where Telegram summaries go

To the chat configured in `config/notifications.yaml`. The scheduler
sends a per-cycle summary (mode, ok/failed steps, swing/invest gate
status). Long-horizon ideas come from the **deterministic pipeline**
(via `_maybe_send_trade_alerts` in the supervisor, gated by PART 1 + 2
+ 3 fixes) — not from the scheduler wrapper.

---

## What happens if the PC sleeps?

Windows **does not** wake the machine for this task by default. Practical
options:

1. **Prevent sleep while the task runs** — change Power Settings to
   "Never sleep" while the task is active. Simplest, recommended for
   24h runs.
2. **`-WakeToRun`** flag on `New-ScheduledTaskSettingsSet` will wake
   the machine to start, but does not keep it awake mid-cycle. Mid-cycle
   sleeps will lose ticks. **Not** recommended for the 2h cadence.
3. **Use the foreground PowerShell window** (Option A) and disable
   sleep via:
   ```powershell
   powercfg /change standby-timeout-ac 0
   powercfg /change standby-timeout-dc 0
   ```
   Restore via your usual values afterwards.

---

## Known limitations

* No admin rights → can't run as SYSTEM; the task runs only when your
  user is logged in (unless you store the password, which is
  discouraged).
* The script is single-process. If it crashes (Windows DLL init
  failure is now handled internally; other crashes are not), the task
  does not restart automatically — Windows Task Scheduler triggers the
  task once per day, so a mid-cycle crash means lost cycles until the
  next trigger.
* The crypto monitor inside each cycle is bounded to `--monitor-minutes`
  (default 90). At end of cycle the parent kills it via the PID lock
  file, so there is no duplicate-monitor leak between cycles.
* Stocks scalp report **does not exist** in this CLI. The scheduler
  records it as a `note` step ("stocks scalp unavailable") to keep the
  per-cycle summary honest, and continues with stocks intraday.

---

## Stopping the scheduler

* **Foreground**: `Ctrl+C` in the PowerShell window. The `finally`
  block kills the background crypto monitor and removes its lock file.
* **Task Scheduler**: `schtasks /End /TN "CryptoAIDesk_Default_24h"`.
* **Hard kill**: `taskkill /F /PID <python pid>` — leaves a stale lock
  file at `data/scheduled_runs/<date>_default_schedule/crypto_monitor.pid`;
  the next run cleans it up automatically.
