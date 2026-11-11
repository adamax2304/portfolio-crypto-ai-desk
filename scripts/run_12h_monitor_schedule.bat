@echo off
REM ===========================================================================
REM 12-hour monitoring scheduler — Windows wrapper.
REM
REM Usage:
REM   scripts\run_12h_monitor_schedule.bat                       full 12h/2h run
REM   scripts\run_12h_monitor_schedule.bat --dry-run             validate only
REM   scripts\run_12h_monitor_schedule.bat --minutes 10 --interval-minutes 5 --skip-reports --no-send-telegram
REM
REM All args are passed straight through to the Python scheduler.
REM Keep the window open unless launched via Task Scheduler.
REM ===========================================================================

cd /d "%~dp0\.."

set PYTHONIOENCODING=utf-8
set PYTHONPATH=%CD%

REM Default to a 12-hour / 2-hour session with Telegram on when no args given.
if "%~1"=="" (
    python -m scripts.run_12h_monitor_schedule --hours 12 --interval-hours 2 --send-telegram
) else (
    python -m scripts.run_12h_monitor_schedule %*
)
set EXITCODE=%ERRORLEVEL%

echo.
echo ============================================================
echo 12h monitor exit code: %EXITCODE%
echo logs: data\scheduled_runs\^<date^>_12h_monitor\
echo ============================================================

if defined SESSIONNAME (
    if /I not "%SESSIONNAME%"=="Services" pause
)
exit /b %EXITCODE%
