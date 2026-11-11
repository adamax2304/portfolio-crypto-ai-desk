# Telegram Message Parsing

The bridge does light parsing only. Heavy parsing happens upstream in `news_trader`.

## Bridge-level parsing (in this project)

`news_trader_bridge.iter_signals` and `_tickers_from_signal`:

1. Read each JSON line in `telemetry.jsonl` from the tail.
2. Skip lines whose `event` is not in `{aggregator_emit, bus_publish (topic=enriched), executor_signal_received}`.
3. Parse `ts_iso` (UTC). Skip if older than `lookback_minutes`.
4. Build `NewsTraderSignal` with: ts, source, source_name, symbol, category, tier, score, direction, headline.
5. Extract canonical tickers from:
   - The `symbol` field, normalized (`upper().replace("/", "").replace("USDT", "")`). Mapped via `CATEGORY_TICKER_MAP` (GOLD→PAXG, OIL→USOON, XAU→PAXG, WTI→USOON, BRENT→USOON).
   - The headline: regex `[#$]([A-Z]{2,10})\b`. Filters out `USDT`, `USD`, `USDC`, `BTC` if already present. Applies same category mapping.

## Sentiment tagging

`_tag_sentiment` matches lower-cased headline against `SENTIMENT_KEYWORDS`:

- **bullish**: approval, approved, etf inflow, etf launch, listing, list, buy, accumulation, partnership, integration, upgrade, mainnet, rally, surge, soars, all-time high, breakout, moon.
- **bearish**: hack, exploit, rug, drained, lawsuit, ban, delisting, delist, dump, crash, drops, tumble, sec sues, bankruptcy, rugpull, outage, exit scam.
- **macro_riskoff**: war, attack, strike, missile, sanction, escalat, rate hike, fed hawkish, yields surge, tariff, recession.
- **macro_riskon**: rate cut, dovish, ceasefire, agreement signed, easing, stimulus, etf inflow.

A single headline may bump multiple counters. The counters are aggregated per ticker into `TickerAttention`.

## Dedup

`(ticker, raw_event + "|" + headline[:120])` is the dedup key. Re-posts of the same headline by the same event class are skipped per ticker per window.

## Headline truncation

Headlines are stored truncated to 400 chars in `NewsTraderSignal.headline` and to 6 entries per ticker in `TickerAttention.top_headlines`.

## What is NOT parsed

- Inline links / attachments (not in telemetry).
- Reply / forward chains (news_trader strips structure before writing).
- Emoji / formatting (kept as-is; sentiment regex is case-insensitive on lowercase).
- Foreign-language content (works only when headline contains English keywords).

## Recommended improvements

- Add language detection + multi-lingual sentiment keywords.
- Add per-source weight in `_tag_sentiment`.
- Detect explicit tier-strong upgrades and emit a separate "fresh strong" flag.

## Related

- [[Telegram_Integration]]
- [[Telegram_Sources]]
- [[Telegram_News_Evaluation]]
- [[Crowd_Attention]]

## Implemented status

- **Implemented** (light, keyword-based).
