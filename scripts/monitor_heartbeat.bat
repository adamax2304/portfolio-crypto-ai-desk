@echo off
REM Env-safe wrapper for the heartbeat watchdog (used by the CryptoAIDeskHeartbeat task).
REM Sets UTF-8 so emoji in Telegram payloads never trip cp1252. Read-only on trade data.
cd /d "%~dp0..\"
set PYTHONIOENCODING=utf-8
python -m scripts.monitor_heartbeat %*
