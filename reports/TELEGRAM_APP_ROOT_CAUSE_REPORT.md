# Telegram App Root-Cause Report (PART 9)

**Date:** 2026-06-20.

## Symptom
"Приложение в Telegram не работает" — opening the Mini App did nothing / didn't load.

## Evidence
At audit start (2026-06-20 ~15:08):
- backend uvicorn = **0**, port 8000 **not listening**, `http://127.0.0.1:8000/api/health` **unreachable**.
- cloudflared = **0** → no public HTTPS endpoint existed.
- bot.py = **0** → bot offline.
- `.env` `MINI_APP_URL` = **stale dead tunnel** (`certificates-creative-retro-loans...`).
- Meanwhile the trading scheduler (`CryptoAIDeskMonitor`) was **alive, uptime ~23.5h**.
- Date had rolled 06-19 → **06-20**: the failure spanned an overnight session boundary.

## Root cause
**The Control Plane app stack (backend + cloudflared tunnel + bot) was not persistent and was reaped when the previous session/terminal ended.** The trading core survived only because it runs under a **Windows scheduled task** (service-owned). The app stack had only ever been started from an ephemeral agent shell, so its processes died with the session — taking the public URL with them. With no tunnel and no backend, the bot's button pointed at a dead URL and nothing loaded.

This is **not** a code/CORS/auth/build bug — backend, frontend build, CORS, auth, and DB path are all correct (PARTs 4–8). It is a **process-lifecycle / persistence** failure (the same class previously solved for the trading monitor, but never applied to the app stack).

Ruled out: backend down (true, but downstream of non-persistence) · stale URL (true symptom) · CORS/auth (no) · initData (no) · old build (no) · port conflict (no) · duplicate process (no) · machine asleep (cycles were continuous, so the box was up — purely session-reap).

## Fix applied
New **`CryptoAIDeskApp`** Windows scheduled task running a **self-healing keeper** (`scripts/app_keeper.ps1`) that keeps backend+tunnel+bot up, rebuilds via `launch_robust.ps1` if any component dies, and refreshes `.env`+menu button on each restart. Stack is now **task-owned → survives session-end + reboot**, mirroring the trading core. (Details: PART 10.)

## Verification
Post-fix: backend `/api/health` 200 (local + tunnel), single bot (`@aitradingdesk1_bot`), cloudflared up, new URL written to `.env`, menu button re-pointed, test button delivered (msg_id=8). See PARTs 4–8, 11.

## Remaining risk
- cloudflared quick-tunnel URL still rotates on restart (keeper auto-updates menu + `.env`; old inline buttons in old chat messages can be stale → use the menu button). A stable named tunnel/custom domain would remove rotation entirely (future, optional).
- If Windows is fully powered off, the task resumes at next logon (`StartWhenAvailable`).

## Verdict
**TELEGRAM_APP_ROOT_CAUSE_FOUND** — non-persistent app stack reaped at session end; fixed by a persistent keeper task.
