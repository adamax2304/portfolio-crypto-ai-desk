# Telegram Tunnel / Public URL Health (PART 6)

**Date:** 2026-06-20.

- **Before:** cloudflared = 0 processes → **no public URL at all**. `.env` `MINI_APP_URL` was a **stale dead tunnel** (`certificates-creative-retro-loans...`) from the previous session.
- **Action:** keeper → `launch_robust.ps1` starts a fresh cloudflared quick-tunnel → `localhost:8000`, parses the new URL, writes it to `.env` `MINI_APP_URL`, and re-points the bot menu button.
- **After — current URL:** `https://domains-exemption-affiliated-cancelled.trycloudflare.com`
  - `GET <url>/api/health` → **200** `{"ok":true,...,"live_locked":true,"has_desk_db":true}`
  - `GET <url>/` → **200** (production app, `vite_dev=False`)
  - HTTPS valid; no 502/404/timeout.
- **CORS:** same-origin (app + API both on this tunnel) + permissive backend CORS → tunnel origin accepted.
- **Bot configured with same URL:** menu button `web_app.url` == current tunnel (verified). 

**Known operational property:** the cloudflared *quick* tunnel URL **rotates on every (re)launch**. The keeper handles rotation automatically (writes `.env` + re-sets the menu button), so the always-visible menu button + `/start` button stay valid. The only time a user could hit a stale URL is an old chat message with an old inline button — they should use the **menu button** (always current).

## Verdicts
**TUNNEL_FIXED · URL_ROTATION_FIXED** (stale URL replaced; rotation now self-managed by the keeper).
