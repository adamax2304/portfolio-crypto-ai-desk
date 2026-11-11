# Telegram_News

Default landing folder for any Telegram-sourced item before classification.

## Criteria for filing here first

- Source originates from a Telegram channel (per `news_trader_bridge.source_name`).
- Not yet evaluated against price / volume.

## Migration rules

After the price reaction window passes:

- → `Useful_News/` if it created / confirmed a setup.
- → `Useless_News/` if no reaction.
- → `Fake_or_Unverified_News/` if proven false.
- → `Market_Moving_News/` if it produced a ≥ 2% move (regardless of trade outcome).
- **Stay here** if still pending verification.

## What to capture

Use [[Telegram_News_Template]]. Important to record:

- Channel name (source_name).
- News_trader tier (strong / medium).
- Message timestamp.
- Related symbol(s).
- Sentiment via keyword tag.

## Related

- [[Telegram_Integration]]
- [[Telegram_News_Evaluation]]
- [[Telegram_News_Template]]
