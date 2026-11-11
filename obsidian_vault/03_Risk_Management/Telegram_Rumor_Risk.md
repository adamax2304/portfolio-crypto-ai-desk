# Telegram Rumor Risk

## Status

This is the single most common source of bad trades for crypto traders. The desk treats Telegram messages with explicit skepticism.

## How rumors enter the desk

1. **`news_trader`** scrapes Telegram via Telethon.
2. **`news_trader_bridge`** consumes `telemetry.jsonl` read-only.
3. Each signal carries a `tier` (`strong`, `medium`, etc.) and a source. The bridge converts top headlines into "manual social notes" with:
   - `verification = "confirmed"` if any signal in the cluster was `tier=strong`.
   - `verification = "single_source"` otherwise.
4. These notes feed `CrowdAttentionAgent`. They never feed `ScoringAgent` directly.

## How the desk treats them

- A `single_source` Telegram message → attention only; `CrowdAttentionAgent` may move the symbol toward `early_attention` or `growing_hype`. Score is not raised.
- A `confirmed` (i.e. `tier=strong`) Telegram message → still attention only, but verification is upgraded; if a manual note was `verification = rumor`, it stays rumor.
- A `rumor`-flagged note (in `data/manual/social_notes.yaml`) → `CrowdAttentionAgent` forces `stage = rumor_driven` when attention ≥ 15.
- A symbol with a rumor-only catalyst and verification in {`none`, `rumor`, `single_source`} → `ScoringAgent` caps at **55**.

## Why this is conservative

- Telegram is downstream of more reliable sources. By the time a coin is shilled in a channel, the alpha is often gone.
- Telegram channels routinely post fake / unverified rumors.
- "Source" attribution in Telegram is weak (re-shares, fake screenshots, edited messages).

## Operator rules

1. Never increase position size because "Telegram is screaming about it."
2. Never enter a trade purely on a Telegram message. If price + structure + derivatives confirm, the message is **extra** evidence, not the trade.
3. Treat a fresh `tier=strong` signal with no price confirmation as **attention only**.
4. If a channel posts a rumor that the desk later marks `confirmed` from a different source, log it in [[Useful_News]] only after confirmation, not before.
5. If a rumor turns out to be fake or never moved price, log it in [[Useless_News]] or [[Fake_or_Unverified_News]].

## Telegram-driven flush patterns

- Channel posts "X just listed" → price spikes → posts repost → eventual exchange announcement → sell-the-news flush. Often a fade setup, not a buy setup.
- Channel posts insider rumor → small pump → silent → flat. The trade was an illusion.

## Useful Telegram channels (per `news_trader` config — not maintained here)

The list lives in news_trader. Some examples: `lookonchain`, `whale_alert`, `BinanceListings`, `BWEnews`, `WalterBloomberg`, `zachxbt`. The bridge does not weight channels per reliability — recommended improvement.

## Related

- [[News_Verification]]
- [[Telegram_Integration]]
- [[Telegram_News_Evaluation]]
- [[Crowd_Attention_Agent]]
- [[Rumors_and_Unverified_News]]

## Implemented status

- **Implemented** (caps + attention staging). Per-channel reliability scoring **Recommended**.
