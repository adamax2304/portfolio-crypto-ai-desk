@echo off
REM PART 14 — autonomous scheduler launcher for Windows Task Scheduler.
REM
REM This wrapper:
REM   * runs the 2-hour cycle scheduler in an infinite restart loop;
REM   * survives transient Python crashes / network blips / yfinance hangs;
REM   * appends every restart to data\autostart\scheduler.log so we have
REM     a stable place to see crash history without polluting the
REM     per-day scheduled_runs/ folders.
REM
REM Run from Windows Task Scheduler at user logon. Do NOT double-click
REM manually — the task scheduler instance + a manual instance would
REM both try to grab the same SQLite handles.
REM
REM Stop with TaskScheduler ("End task"). Or kill the python.exe child
REM and this .bat will sleep 20s then relaunch — by design.

setlocal
set PROJECT=%~dp0..
set PYTHONIOENCODING=utf-8
REM Refresh user-scoped MEXC canary credentials on every wrapper start. Values
REM remain in the Windows user environment and are never stored in this file.
for /f "usebackq delims=" %%V in (`powershell -NoProfile -Command "[Environment]::GetEnvironmentVariable('MEXC_CANARY_ACCESS_KEY','User')"`) do set "MEXC_CANARY_ACCESS_KEY=%%V"
for /f "usebackq delims=" %%V in (`powershell -NoProfile -Command "[Environment]::GetEnvironmentVariable('MEXC_CANARY_SECRET','User')"`) do set "MEXC_CANARY_SECRET=%%V"
for /f "usebackq delims=" %%V in (`powershell -NoProfile -Command "[Environment]::GetEnvironmentVariable('BYBIT_LIVE_ACCESS_KEY','User')"`) do set "BYBIT_LIVE_ACCESS_KEY=%%V"
for /f "usebackq delims=" %%V in (`powershell -NoProfile -Command "[Environment]::GetEnvironmentVariable('BYBIT_LIVE_SECRET','User')"`) do set "BYBIT_LIVE_SECRET=%%V"
for /f "usebackq delims=" %%V in (`powershell -NoProfile -Command "[Environment]::GetEnvironmentVariable('BYBIT_LIVE_ARMED','User')"`) do set "BYBIT_LIVE_ARMED=%%V"
for /f "usebackq delims=" %%V in (`powershell -NoProfile -Command "[Environment]::GetEnvironmentVariable('MEXC_LIVE_CANARY_ARMED','User')"`) do set "MEXC_LIVE_CANARY_ARMED=%%V"
set LOGDIR=%PROJECT%\data\autostart
if not exist "%LOGDIR%" mkdir "%LOGDIR%"
set LOGFILE=%LOGDIR%\scheduler.log

cd /d "%PROJECT%"

:loop
echo [%date% %time%] starting scheduler >> "%LOGFILE%"
python -m scripts.run_default_market_schedule --hours 24 --interval-hours 2 --monitor-minutes 90 --send-telegram >> "%LOGFILE%" 2>&1
echo [%date% %time%] scheduler exited with code %ERRORLEVEL%, restart in 20s >> "%LOGFILE%"
timeout /t 20 /nobreak > nul
goto loop
