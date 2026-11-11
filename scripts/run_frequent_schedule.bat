@echo off
REM ===========================================================================
REM Frequent scheduler — headless wrapper for Windows Task Scheduler.
REM
REM This .bat is intended to be triggered by Task Scheduler so the Python
REM process survives Claude / terminal closures. It MUST NOT pause at the end
REM (no human in the loop). It logs everything to file.
REM
REM Args (positional, optional):
REM   %1  number of hours to run (default 22)
REM ===========================================================================

cd /d "%~dp0\.."

set PYTHONIOENCODING=utf-8
set PYTHONPATH=%CD%

set HOURS=%~1
if "%HOURS%"=="" set HOURS=22

REM Use today's Nicosia date for the consolidated stdout log. Python scheduler
REM writes the structured log to data/scheduled_runs/<today>/frequent_scheduler.log
REM This file just captures everything written to stdout/stderr in case Python crashes early.
if not exist "data\scheduled_runs" mkdir "data\scheduled_runs"

python -m scripts.run_frequent_schedule --hours %HOURS% --send-telegram >> "data\scheduled_runs\frequent_scheduler.stdout.log" 2>&1
exit /b %ERRORLEVEL%
