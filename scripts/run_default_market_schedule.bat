@echo off
REM Default market scheduler — desk's permanent operating loop.
REM Every 2h: crypto scalp + intraday (always), stocks intraday on weekdays.
REM Daily-once: swing + invest. No auto-trade. No Opus auto-call.
REM
REM Usage:
REM   .\scripts\run_default_market_schedule.bat                     (24h, 2h, telegram on)
REM   .\scripts\run_default_market_schedule.bat --crypto-only       (skip stocks)
REM   .\scripts\run_default_market_schedule.bat --run-once          (one cycle)
REM   .\scripts\run_default_market_schedule.bat --dry-run           (plan validation)

cd /d "%~dp0..\"
set PYTHONIOENCODING=utf-8
python -m scripts.run_default_market_schedule --hours 24 --interval-hours 2 --monitor-minutes 90 --send-telegram %*
