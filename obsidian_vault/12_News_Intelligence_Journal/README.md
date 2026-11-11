# 12 — News Intelligence Journal

The dataset of how news / Telegram signals actually performed. Build this over weeks to learn which sources matter.

## Folder layout

```
12_News_Intelligence_Journal/
  Useful_News/                  # News that created or confirmed a trade
  Useless_News/                 # News that produced no measurable reaction
  Fake_or_Unverified_News/      # News that turned out false
  Telegram_News/                # Default landing folder for Telegram items
  Market_Moving_News/           # Items that produced ≥ 2% / 60min moves
  News_Reviews/                 # Weekly / monthly source rankings
  Templates/                    # The 5 templates
```

## Filename convention

```
YYYY-MM-DD_HHMM_SOURCE_SYMBOL_SHORT-SLUG.md
```

Examples:

- `2026-05-23_0942_BinanceListings_ABC_listing-announcement.md`
- `2026-05-23_1011_lookonchain_BTC_whale-accumulation.md`
- `2026-05-23_1530_RSS-CoinDesk_ETH_etf-flow.md`

For reviews:

- `2026-05-23_News_Impact_Review.md`
- `2026-W21_Source_Reliability_Review.md`

## Workflow

1. **As news arrives** (Telegram alert or RSS pickup): drop a quick entry into `Telegram_News/` using [[Templates/Telegram_News_Template]] or [[Templates/News_Item_Template]] for non-Telegram items.
2. **After 1h / 4h / 24h**: revisit and fill in price/volume/OI reaction; reclassify.
3. **Move** to:
   - `Useful_News/` if it created or confirmed a trade.
   - `Useless_News/` if it produced no measurable reaction.
   - `Fake_or_Unverified_News/` if proven false later.
   - `Market_Moving_News/` if it produced a ≥ 2% move regardless of trade outcome.
4. **Weekly**: write a `News_Reviews/YYYY-Www_Source_Reliability_Review.md` ranking sources by hit rate.
5. **Monthly**: re-evaluate which Telegram channels deserve more / less weight.

## Why bother

- The desk does **not** yet weight by source reliability.
- Operator-built reliability map is the closest substitute.
- Future improvement (see [[Improvement_Backlog]]): port the manual map into `news_trader_bridge` config.

## Related

- [[News_System_Overview]]
- [[Telegram_Integration]]
- [[Useful_vs_Useless_News]]
- [[Templates/News_Item_Template]]
- [[Templates/Telegram_News_Template]]
- [[Templates/Useful_News_Template]]
- [[Templates/Useless_News_Template]]
- [[Templates/News_Impact_Review_Template]]

## Implemented status

- **Folder + templates implemented**. Manual workflow.
