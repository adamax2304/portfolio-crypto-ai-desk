# Telegram Sources

## Who scrapes what

The crypto-ai-desk project itself **does not** read any Telegram channel directly. All Telegram ingestion lives in the **sister project** `news_trader`.

## news_trader scope (per its docstring referenced in `news_trader_bridge`)

> news_trader runs a Telethon scraper across 50+ public crypto/macro Telegram channels (lookonchain, whale_alert, BinanceListings, BWEnews, WalterBloomberg, zachxbt, ...) and an aggregator that classifies + scores each signal.

The full source list is maintained inside the `news_trader` project — **not here**. From the bridge perspective, every signal carries:

- `source_name` — e.g. `t.me/whale_alert`, `t.me/lookonchain`.
- `source` — usually `"telegram"`.
- `category` — coarse asset / topic tag (BTC, ETH, GOLD, etc.).
- `tier` — `strong / medium / ...` per news_trader's own classifier.

## Source tiers the desk relies on

| news_trader tier | Desk verification |
|---|---|
| strong | `confirmed` |
| medium / unknown / missing | `single_source` |

## Useful source archetypes

- **Listing channels** (e.g. BinanceListings, KuCoin Listings) — high signal on event existence; usually beats the official RSS by minutes.
- **On-chain analytics** (lookonchain, whale_alert) — wallet flows; high signal but slow to materialize on price.
- **Macro / general** (BWEnews, WalterBloomberg) — broader-market headlines; useful for regime context.
- **OSINT / fraud** (zachxbt) — bearish catalysts on rugs / exploits.

## Reliability is NOT yet weighted

The bridge stores `source_name` but does not weight by reliability. Recommended improvement: a config map `{source_name: reliability_score 0..1}` that multiplies the attention contribution.

## How to add a source

You don't add it here. You add it inside the `news_trader` project (Telethon channel list) and the bridge will see new headlines automatically.

## Related

- [[Telegram_Integration]]
- [[News_Verification]]
- [[Telegram_Rumor_Risk]]

## Implemented status

- **Implemented** (sources live in news_trader, bridge reads them). Per-source reliability **Recommended**.
