@echo off
title Trading Desk (Monitor / Scheduler)
echo ============================================================
echo  Starting the Trading Desk monitor / scheduler...
echo  (Idempotent: if it is already running, no second copy is started.)
echo ============================================================
call "%~dp0start_monitor_scheduler.bat"
echo.
echo ============================================================
echo  Desk monitor launch requested. It runs in the background.
echo  Telegram heartbeat / cycle alerts will arrive as usual.
echo  You can close this window.
echo ============================================================
pause
