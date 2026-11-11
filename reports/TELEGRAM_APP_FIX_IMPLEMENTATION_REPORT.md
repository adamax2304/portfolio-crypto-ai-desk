# Telegram App Fix Implementation (PART 10)

**Date:** 2026-06-20. All fixes are **operational/integration only — no trading logic touched.**

## Fix 1 — Persistent self-healing app keeper (the durable root-cause fix)
- **Files added:**
  - `trading-desk-control/scripts/app_keeper.ps1` — infinite loop: every 60s health-checks the stack (`/api/health`==200 AND bot.py alive AND cloudflared alive); if anything is down, runs the idempotent `launch_robust.ps1`. Steady-state healthy → just sleeps (no thrash, no needless URL rotation).
  - `trading-desk-control/scripts/app_keeper.bat` — foreground wrapper (task action / double-click).
- **Why safe:** pure process supervision; reuses the existing, validated `launch_robust.ps1`; reads `.env`; never imports/edits desk trading code; cannot enable live (backend keeps `live_locked:true`).
- **Rollback:** `Unregister-ScheduledTask CryptoAIDeskApp -Confirm:$false`; delete the two files. Trading core unaffected.

## Fix 2 — Register `CryptoAIDeskApp` scheduled task
- Registered non-elevated (`-Once` + `StartWhenAvailable`, `MultipleInstances IgnoreNew`, `RestartCount 3`, `ExecutionTimeLimit 0`), Principal Interactive/Limited — same proven pattern as `CryptoAIDeskMonitor`. Started → **State: Running**. The keeper (task-owned) then brought the stack up, so the processes are **owned by the Task Scheduler service** and survive session-end + reboot.
- **Rollback:** `Unregister-ScheduledTask CryptoAIDeskApp -Confirm:$false`.

## Fix 3 — Tunnel URL + bot menu button refreshed (via launch_robust, invoked by keeper)
- Stale `MINI_APP_URL` replaced with the live tunnel; `setChatMenuButton` re-pointed; one test "Open Control Plane" button sent to operator (msg_id=8).
- **Rollback:** none needed (idempotent config refresh).

## What was NOT changed
No scoring / TP-SL / entry logic / routing / actionability / filters / validity windows / live / auto-live / exchange execution / scalp-or-C-tier actionable / BE-partial-trailing / historical outcomes. No desk Python touched. No frontend/backend app code touched (only added 2 ops scripts + 1 Windows task).

## Verification
backend 200 (local+tunnel), single instances of scheduler/bot/cloudflared, menu button == live URL, tests green (PART 11).

## Verdict
**TELEGRAM_APP_FIXED** (restart + durable persistence keeper). Not merely a restart — the root cause (non-persistence) is now structurally fixed.
