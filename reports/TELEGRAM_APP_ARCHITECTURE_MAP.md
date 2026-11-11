# Telegram App / Mini App Architecture Map (PART 3)

**Date:** 2026-06-20.

## Components
- **Bot:** `trading-desk-control/bot/bot.py` (aiogram, long-polling). Token + URL from `.env` (`TELEGRAM_BOT_TOKEN`, `MINI_APP_URL`, `ALLOWED_TELEGRAM_USER_IDS`).
- **Backend:** FastAPI `backend/app/main.py` on **127.0.0.1:8000**. Serves `/api/*` AND the **built frontend `frontend/dist` at `/`** (single origin — added in the status-clarity session to avoid Vite-dev fragility).
- **Frontend:** Vite/React build in `frontend/dist` (served by the backend; the dev server is no longer used for the Mini App).
- **Tunnel:** bundled `scripts/bin/cloudflared.exe` quick-tunnel → `http://localhost:8000`. Public HTTPS URL rotates each launch.

## How Telegram opens the app
- **Menu button** (persistent, bottom-left): set via Bot API `setChatMenuButton` (web_app → `MINI_APP_URL`) by `launch_robust.ps1` on every (re)launch.
- **Inline `/start` button:** `bot.py` sends `InlineKeyboardButton(web_app=WebAppInfo(url=MINI_APP_URL))`.
- Both now point at the **current** tunnel URL.

## URL that must open
The **current cloudflared quick-tunnel** (rotates each launch) → backend :8000 (serves the app + API on one origin). Today: `https://domains-exemption-affiliated-cancelled.trycloudflare.com`.

## Frontend ↔ backend
- **API base:** same-origin `/api` (`VITE_API_BASE` empty) → no CORS hop in production (app + API on the one tunnel origin). Backend also has permissive CORS middleware (`allow_origins=["*"]`).
- **Auth:** Telegram `initData` via header `X-Telegram-Init-Data`, verified server-side + user-id whitelist (`ALLOWED_TELEGRAM_USER_IDS=6411752454`). `AUTH_DISABLED` empty (auth ON). `/api/health` is unauthenticated (liveness).
- **DB:** `DESK_DB_PATH` → `crypto-ai-desk/db/crypto_ai_desk.sqlite` (read-only); `CONTROL_DB_PATH` → backend control.sqlite.

## Ports
backend **8000** (serves app + API); tunnel target **localhost:8000**; (frontend dev :5173 not used for the Mini App anymore).

## Docs
`trading-desk-control/README.md`, `docs/TELEGRAM_MINI_APP_LAUNCH_SETUP.md`, `docs/LOCAL_LAUNCH_RUNBOOK.md`; launchers `scripts/launch_robust.ps1` (+ `launch_app.bat`), now `scripts/app_keeper.ps1` (+ `.bat`).

## Verdict
**TELEGRAM_APP_ARCHITECTURE_MAPPED**
