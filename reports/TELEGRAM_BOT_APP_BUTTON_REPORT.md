# Telegram Bot / App Button Health (PART 7)

**Date:** 2026-06-20.

- **Bot process:** 1 instance of `bot/bot.py` (single — no TelegramConflictError 409 risk).
- **Token:** loaded from `.env`; `getMe` → **@aitradingdesk1_bot** (token valid, no 401/403).
- **Menu button:** `getChatMenuButton` → type **`web_app`**, url = **`https://domains-exemption-affiliated-cancelled.trycloudflare.com/`** (current tunnel) — always-visible "open app" entry point, now correct.
- **Inline `/start` button:** `bot.py` emits a `web_app` button from the same `MINI_APP_URL`.
- **One safe test performed:** `sendMessage` to operator (chat 6411752454) with health line + an **"Open Control Plane" `web_app` inline button** → **ok=True, message_id=8**. No spam (single message).

## Verdicts
**TELEGRAM_BOT_OK · TELEGRAM_APP_BUTTON_FIXED** (menu button re-pointed to live URL; fresh working button delivered to operator).
