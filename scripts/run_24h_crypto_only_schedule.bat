@echo off
REM 24h CRYPTO-ONLY weekend validation run.
REM Crypto only. NO stocks. NO auto-trade. NO scoring/threshold changes.
REM
REM Usage:
REM   .\scripts\run_24h_crypto_only_schedule.bat            (24h, 2h interval, Telegram on)
REM   .\scripts\run_24h_crypto_only_schedule.bat --dry-run  (validate plan only)

cd /d "%~dp0..\"
set PYTHONIOENCODING=utf-8
python -m scripts.run_24h_crypto_only_schedule --hours 24 --interval-hours 2 --monitor-minutes 90 --send-telegram %*
