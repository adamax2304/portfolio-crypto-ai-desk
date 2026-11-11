# News That Moved Market

## Definition

Any news item — Telegram, RSS, primary, secondary — that produced a measurable price reaction on the symbol or sector within a reasonable window.

A working threshold:

- ≥ 2% move within 60 minutes on the named symbol.
- ≥ 5% move within 24 hours.
- ≥ 1% move on BTC / ETH within 30 minutes for macro headlines.

## Why track these separately

Even if you didn't trade them, market-moving items reveal:

- Which sources have predictive value.
- Which categories (listing, hack, regulatory, partnership) actually drive price.
- Which channels timely-report.

## Logging shape

Use [[News_Item_Template]]. Important fields to fill in carefully:

- **Price reaction after 5m / 15m / 1h / 4h** — populate all four to capture decay.
- **Volume reaction** — confirms the move was driven (not coincidence).
- **OI/funding reaction** — separates spot-driven from leverage-driven moves.
- **Did the market care?** — yes/no qualitative gate.
- **Did it create a trade? Support a trade? Invalidate?** — the operator's choice retrospectively.

## Common patterns to recognize

- **Pump-and-dump on small-cap listing rumor** — sharp spike + dump within 30–60 min.
- **Hack / exploit announcement** — fast bearish move, sometimes followed by relief bounce.
- **CPI / FOMC** — initial spike + reversion to direction within 2 hours.
- **War / attack headline** — instant risk-off, often reverses within 4 hours.
- **Exchange listing on Binance / Coinbase** — pre-tweet leak + tweet spike + sell-the-news within 30 min.

## What to do with the dataset

- Weekly: rank sources by hit rate (market-moving rate ÷ total items).
- Monthly: identify reliable channels and add them to a mental whitelist.
- When a new channel keeps appearing → check its `news_trader` reliability; if it earns its place, suggest adding weight in `news_trader_bridge`.

## Related

- [[Useful_vs_Useless_News]]
- [[News_That_Was_Noise]]
- [[Telegram_News_Evaluation]]

## Implemented status

- **Operator framework**; supported by `12_News_Intelligence_Journal/Market_Moving_News/`.
