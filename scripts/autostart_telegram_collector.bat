@echo off
REM PART 14 — autonomous Telegram-collector launcher for Windows Task Scheduler.
REM
REM This wrapper:
REM   * runs the 18-channel Telethon collector in an infinite restart loop;
REM   * survives Telethon TCP drops / Telegram FloodWait / session reauth;
REM   * appends every restart to data\autostart\telegram_collector.log.
REM
REM Run from Windows Task Scheduler at user logon. Auth must already be
REM established — the session lives in data\telegram\crypto_ai_desk_tg.session.
REM If the session expires, run scripts\setup_telegram_auth.py once
REM interactively to re-establish it.

setlocal
set PROJECT=%~dp0..
set PYTHONIOENCODING=utf-8
set LOGDIR=%PROJECT%\data\autostart
if not exist "%LOGDIR%" mkdir "%LOGDIR%"
set LOGFILE=%LOGDIR%\telegram_collector.log

cd /d "%PROJECT%"

:loop
echo [%date% %time%] starting telegram collector >> "%LOGFILE%"
python scripts\run_telegram_collector.py >> "%LOGFILE%" 2>&1
echo [%date% %time%] collector exited with code %ERRORLEVEL%, restart in 20s >> "%LOGFILE%"
timeout /t 20 /nobreak > nul
goto loop
