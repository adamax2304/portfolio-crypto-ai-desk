# News System Overview

The desk has **four** distinct news inputs:

1. **RSS news** — `src/data_collectors/rss_news_collector.py`, configured in `config/sources.yaml.rss_feeds`. Currently: Binance Announcements (primary), CoinDesk, Cointelegraph, Decrypt. Coinbase Blog is disabled (Cloudflare 403).
2. **Manual events** — `data/raw/events/manual_events.yaml`, loaded by `manual_events_loader.py`, persisted to SQLite `events` table.
3. **Manual social notes** — `data/manual/social_notes.yaml` and `data/manual/narrative_notes.yaml`, loaded by `manual_notes_loader.py`. Free-text observations from KOL / Telegram / Discord.
4. **`news_trader_bridge`** — read-only ingestion of pre-classified Telegram + news_trader signals from `news_trader/news_trader/state/telemetry.jsonl`. **The only path Telegram messages enter the desk.**

## Agents that consume news

- **`NewsAgent`** — buckets RSS items by symbol + narrative; top-15 by importance.
- **`CatalystAgent`** — joins manual events + news_agent output per symbol, distinguishes catalysts from risk_events (unlock / delisting / migration).
- **`MacroGeopoliticsAgent`** — keyword scan over news headlines using `sources.yaml.macro_keywords` (risk_off, risk_on, neutral_watch).
- **`SocialAttentionAgent`** — Reddit + manual notes; counts mentions per symbol.
- **`CrowdLeaderAgent`** — manual KOL watch.
- **`CrowdAttentionAgent`** — combines social_attention + manual notes + news_trader_bridge notes + derivatives crowding into a stage (silent → euphoria / rumor_driven / exhaustion / fear_capitulation).
- **`NarrativeAgent`** — heatmap per narrative from news + catalysts + momentum + volume.

## How news affects scoring

- `ScoringAgent.catalyst_news` component reads `catalyst.importance_score` and `risk_events`.
- A risk event (unlock / delisting / migration) reduces catalyst quality by 0.25.
- A fresh verified catalyst increases catalyst quality.
- An unverified rumor caps the entire score at 55 (see [[Score_Caps]]).
- News does NOT directly feed `derivatives` or `setup`. It feeds attention + catalyst + risk components only.

## What this system explicitly does NOT have

- No native Telegram scraper (Telethon lives in `news_trader`).
- No Twitter / X scraper.
- No primary-source verification beyond a per-feed `primary_source: true` flag.
- No source-level reliability scoring.
- No automated post-trade news impact review.

## Related

- [[Telegram_Integration]] — the most important page in this folder.
- [[Telegram_Sources]] · [[Telegram_Message_Parsing]] · [[Telegram_News_Evaluation]]
- [[How_to_Evaluate_News]] · [[News_Verification]] · [[Primary_vs_Secondary_Sources]] · [[Rumors_and_Unverified_News]]
- [[Listings]] · [[Token_Unlocks]] · [[Partnerships]] · [[Airdrops]] · [[Mainnet_Testnet]] · [[Exchange_Announcements]]
- [[Crowd_Attention]] · [[Narrative_Heatmap]]
- [[Useful_vs_Useless_News]] · [[News_That_Moved_Market]] · [[News_That_Was_Noise]]

## Implemented status

- **Implemented** for ingestion + categorization.
- **Partially implemented** for sentiment classification (keyword-based).
- **Recommended**: per-source reliability scoring, primary-source verification per ticker, automated news impact review.
