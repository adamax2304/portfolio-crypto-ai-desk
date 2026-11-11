# Full System Component Audit (PART 1)

**Date:** 2026-06-20 ~15:08 UTC.

## Windows tasks
| Task | State | Note |
|---|---|---|
| CryptoAIDeskMonitor | **Running** | trading scheduler — survived (it is a Windows task) |
| CryptoAIDeskHeartbeat | Ready | 20-min watchdog (fires on interval) |
| **CryptoAIDeskApp** (NEW this session) | **Running** | persistent keeper for the Control Plane app stack — the fix |

## Processes — BEFORE fix (the failure)
| Component | Count | Status |
|---|---|---|
| run_default_market_schedule (trading) | 1 | ALIVE |
| backend uvicorn (:8000) | **0** | **DOWN** |
| bot.py | **0** | **DOWN** |
| cloudflared tunnel | **0** | **DOWN** |
| frontend/vite | 0 | n/a (backend serves built dist) |
| port 8000 listening | **False** | **DOWN** |

## Processes — AFTER fix
| Component | Count |
|---|---|
| trading scheduler | 1 |
| backend uvicorn | 1 |
| bot.py | 1 |
| cloudflared | 1 |
| port 8000 listening | True |

## Logs
- `data/autostart/scheduler.log` — trading cycles continuous (ok=N/0); no gap.
- Control Plane: no live backend/bot/cloudflared logs existed before the fix (processes were not running). After the fix, backend on :8000 + bot polling + cloudflared tunnel active.

## Finding
The **trading core was healthy**; the **Control Plane app stack (backend + tunnel + bot) was entirely down** — the single root cause of "приложение в Telegram не работает" (see `TELEGRAM_APP_ROOT_CAUSE_REPORT.md`). Because only the trading core runs under a Windows task, it survived the overnight session-end while the app stack (previously started only from an ephemeral shell) was reaped.

## Verdict
**SYSTEM_COMPONENTS_HAVE_FAILURES** (pre-fix: app stack down) → resolved this session; post-fix **SYSTEM_COMPONENTS_HEALTHY**.
