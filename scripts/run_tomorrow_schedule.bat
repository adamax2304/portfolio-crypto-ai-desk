@echo off
REM ===========================================================================
REM crypto-ai-desk — one-day scheduler wrapper for Windows.
REM
REM Usage:
REM   scripts\run_tomorrow_schedule.bat              run full day (tomorrow)
REM   scripts\run_tomorrow_schedule.bat --dry-run    validate only
REM   scripts\run_tomorrow_schedule.bat --run-now cycle_1   run one cycle
REM
REM Designed so it can also be wired to Windows Task Scheduler. Keep the
REM window visible — the Python scheduler logs to file AND to stdout, so
REM you can watch progress in real time if you launch it manually.
REM ===========================================================================

REM Move to the project root regardless of where the .bat was invoked from.
cd /d "%~dp0\.."

REM Force UTF-8 so the Python CLI's Rich tables / Markdown render cleanly.
set PYTHONIOENCODING=utf-8

REM Ensure ``import src.*`` works when run via Task Scheduler.
set PYTHONPATH=%CD%

python -m scripts.run_tomorrow_schedule %*
set EXITCODE=%ERRORLEVEL%

echo.
echo ============================================================
echo scheduler exit code: %EXITCODE%
echo log dir: data\scheduled_runs\
echo ============================================================

REM Pause only when launched interactively (double-click). Task Scheduler runs
REM headless, so it sees no STDIN and skips the pause.
if defined SESSIONNAME (
    if /I not "%SESSIONNAME%"=="Services" pause
)
exit /b %EXITCODE%
