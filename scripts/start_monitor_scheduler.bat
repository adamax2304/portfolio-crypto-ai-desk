@echo off
REM Thin wrapper so the persistent launcher can be double-clicked or run by Task
REM Scheduler. Delegates to start_monitor_scheduler.ps1 (idempotent + dup-guarded +
REM detached + Telegram heartbeat). Never changes trading logic.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start_monitor_scheduler.ps1" %*
