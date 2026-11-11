# Telegram Commands

## Setup (one-time per fresh chat_id)

1. Open Telegram, find your bot, send `/start`.
2. From the desk:
   ```powershell
   python -m src.cli telegram-setup
   ```
   This calls Telegram's `getUpdates`, picks the most-recent chat that sent `/start`, persists `chat_id` into `config/notifications.yaml`, and sends a test message.

## Test

```powershell
python -m src.cli telegram-test --message "Crypto AI Desk test alert."
```

## Configuration

In `config/notifications.yaml`:

```yaml
telegram:
  enabled: true
  bot_token: <YOUR_BOT_TOKEN>
  chat_id: '<YOUR_CHAT_ID>'
  cooldown_minutes: 30
```

## What gets sent

- A/B-tier ideas from a daily/intraday/scalp/swing report (markdown formatted).
- C→B/A or rejected→B/A upgrades from `monitor-watchlist` (plain text, includes `SL:` line).

## Cooldown

Default 30 minutes per symbol. Tracked in SQLite `watchlist_alerts`. Same-tier alerts inside cooldown are skipped.

## How to debug

- "Why no alerts?" — `python -m src.cli doctor`; check `chat_id` is set.
- "Bot not responding to /start" — bot token in `notifications.yaml` may be wrong.
- "Parse error from Telegram" — markdown in alert content; the desk uses `parse_mode=""` for monitor alerts to avoid this.

## Reading inbound Telegram

This desk does **not** read Telegram channels itself. Inbound Telegram comes from the `news_trader` project via [[Telegram_Integration]] (bridge, read-only).

To debug inbound: see [[How_to_Debug_Telegram_News]].

## Related

- [[Telegram_Integration]]
- [[Daily_Commands]]
- [[Watchlist_Monitor_Agent]]

## Implemented status

- **Implemented** for outbound.
- **Read-only via news_trader_bridge** for inbound.
