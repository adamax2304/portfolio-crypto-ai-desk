# Telegram Integration

The single most important page in this folder. There are **two halves** to the Telegram integration and they should not be confused.

## Half 1 — Outbound bot (this project owns it)

- **Library**: `requests` over plain HTTPS — Telegram Bot API. No Telethon, no `python-telegram-bot`.
- **File**: [src/notifiers/telegram.py](../../src/notifiers/telegram.py).
- **Config**: [config/notifications.yaml](../../config/notifications.yaml) — `bot_token`, `chat_id`, `cooldown_minutes`, `enabled`.
- **Setup flow**: `python -m src.cli telegram-setup`. The user `/start`s the bot in Telegram, the CLI calls `getUpdates`, finds the most-recent chat_id, persists it to YAML.
- **Sending**: `notifier.send(text, parse_mode="Markdown" or "")`. Markdown is used by `Supervisor._format_idea_alert`; plain text by `WatchlistMonitor.format_alert` (so symbol names with special characters don't break parsing).
- **Cooldown**: per-symbol 30-minute dedup via `watchlist_alerts` SQLite table. `db.last_alert_for(symbol)` is checked before send.

### What gets sent

1. **From `Supervisor`**: every A/B-tier idea in a freshly generated daily/intraday/scalp/swing report (`_maybe_send_trade_alerts`). Includes entry, invalidation, TP1/TP2/TP3, caps, thesis, report id.
2. **From `WatchlistMonitor`**: every C→B/A or rejected→B/A upgrade detected during a monitor tick. Includes entry, **SL**, TP1, TP2, thesis, caps. (`SL` was added explicitly so alerts never miss the stop.)

### How to test

```
python -m src.cli telegram-test --message "ping"
```

### Failure modes

- `TelegramNotConfigured` — token missing or chat_id missing.
- HTTP 4xx / 5xx from Telegram — usually rate limit or invalid parse_mode. The notifier raises; the calling code catches and logs.
- Markdown parse errors — fall back to `parse_mode=""`.

## Half 2 — Inbound Telegram (lives in `news_trader`, consumed read-only)

- **Library used in `news_trader`**: Telethon (not in this repo).
- **What `news_trader` does**: scrapes 50+ public crypto / macro Telegram channels (lookonchain, whale_alert, BinanceListings, BWEnews, WalterBloomberg, zachxbt, …), classifies and tiers each signal, writes them to `news_trader/news_trader/state/telemetry.jsonl`.
- **How this desk reads them**: [src/data_collectors/news_trader_bridge.py](../../src/data_collectors/news_trader_bridge.py) tails the **last ~5 MB** of `telemetry.jsonl`, parses JSON lines, accepts events `aggregator_emit`, `bus_publish (topic=enriched)`, `executor_signal_received`.

### Bridge fields per signal

- `ts`, `source`, `source_name`, `symbol`, `category`, `tier`, `score`, `direction`, `headline`, `raw_event`.
- `is_telegram` — true when `source = "telegram"` or `source_name` contains `t.me/`.

### Bridge aggregation

`bridge.aggregate(lookback_minutes=240, tickers_of_interest=[...])` returns a `dict[ticker, TickerAttention]`:

- `mention_count`, `telegram_mention_count`, `strong_tier_count`.
- `bullish_count` / `bearish_count` / `riskoff_count` / `riskon_count` — keyword-tagged from headline using `SENTIMENT_KEYWORDS`.
- `sources[]`, `top_headlines[]`, `latest_ts`.
- `attention_score` ∈ 0..100 — composite of mention counts + strong-tier count.
- `net_sentiment` ∈ {bullish, bearish, mixed, neutral}.

### How the bridge feeds the desk

- `Supervisor.daily_report` calls `bridge.aggregate` + `bridge.macro_pulse`, saves a snapshot to `data/processed/news_trader_bridge_latest.json`, and converts attention into `manual_social_notes` shape:
  - `verification = "confirmed"` if any signal in the cluster was `tier=strong`.
  - `verification = "single_source"` otherwise.
  - `confidence = "high"` if strong tier present, else `"medium"`.
  - `sentiment = "bullish" / "bearish" / "neutral"` from net_sentiment.
- These notes are appended to manual social notes and fed to `CrowdAttentionAgent`.
- **They do NOT go into `ScoringAgent.catalyst_news` directly.** The Telegram path only influences attention staging and the catalyst component indirectly through `CatalystAgent` reading SQLite `news_items`, which are populated by `NewsAgent` from RSS — not from the bridge.

### Macro pulse

`bridge.macro_pulse(lookback_minutes=240)` returns:

- `signal_count`, `strong_count`.
- `top_categories[(category, count)]`.
- `top_sources[(source_name, count)]`.

This feeds report context (no scoring impact today).

## CRITICAL CONSTRAINT

`news_trader_bridge` is **strictly read-only**. The module's docstring is explicit: it must never write to the `news_trader` directory or any subdirectory. The bridge:

- Resolves path via `DEFAULT_PATH = Path(r"C:\Users\adama\Documents\zeph ai projects\news_trader\news_trader\state")`.
- Opens `telemetry.jsonl` in `"rb"` and **tails** only the last `DEFAULT_TAIL_BYTES = 5 MB`.
- Never opens any file for writing inside that path.

Any LLM modifying this desk must preserve that invariant.

## Configuration quick reference

| File | Field | Purpose |
|---|---|---|
| `config/notifications.yaml` | `telegram.bot_token` | outbound bot token |
| `config/notifications.yaml` | `telegram.chat_id` | outbound chat |
| `config/notifications.yaml` | `telegram.cooldown_minutes` | per-symbol alert cooldown |
| `news_trader_bridge.DEFAULT_PATH` | (code) | location of inbound feed |
| `news_trader_bridge.DEFAULT_TAIL_BYTES` | (code) | tail window |

## Common debugging steps

- "Why no alerts?" — check `notifier.enabled` (`bot_token` present), `notifier.chat_id` (set), idea actually `tier ∈ {A, B}`, cooldown window.
- "Why no Telegram context in report?" — check `NewsTraderBridge().available`. If `False`, the path is wrong or news_trader hasn't started. The bridge logs a warning and returns empty payload.
- "Why no sentiment tagging?" — headlines may not contain any keyword from `SENTIMENT_KEYWORDS`. Add new keywords if a class of news is being missed.

## Related

- [[Telegram_Sources]]
- [[Telegram_Message_Parsing]]
- [[Telegram_News_Evaluation]]
- [[News_Verification]]
- [[Crowd_Attention]]
- [[Telegram_Commands]]
- [[Telegram_Rumor_Risk]]

## Implemented status

- **Implemented**. The bridge is the only Telegram inbound path. The outbound bot is fully wired.
