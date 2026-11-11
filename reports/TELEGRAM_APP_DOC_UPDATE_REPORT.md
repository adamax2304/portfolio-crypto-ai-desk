# Telegram App Doc Update (PART 12)

**Date:** 2026-06-20.

- **`PROJECT_STATE.md`** — `Last Updated` → 2026-06-20; new blockquote documenting the Mini App root cause (non-persistent app stack), the `CryptoAIDeskApp` keeper fix, post-fix health (200 local+tunnel, single bot, menu button re-pointed, msg_id=8), current tunnel URL, the URL-rotation note ("use the menu button"), and **No trade-logic change**.
- **`docs/DECISION_LOG.md`** — appended one row (2026-06-20): Control Plane app stack made persistent via `CryptoAIDeskApp` keeper (operational only; no trade logic).
- **`docs/WEEKLY_FORWARD_METRICS.md`** — added a **"Telegram app / Control Plane uptime"** item to the Friday Review Checklist (task Running, `/api/health` 200, single bot/cloudflared, `.env` URL == menu-button URL == opens 200, self-heal/relaunch instructions, rotation note).

All edits are documentation only. Docs validator (`scripts/check_project_state_docs.py` + `tests/test_project_state_docs.py`) re-run green after the edits (PART 11 / PART 13).
