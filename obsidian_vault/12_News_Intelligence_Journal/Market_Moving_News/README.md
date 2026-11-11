# Market_Moving_News

Items that produced a measurable price reaction — even if you didn't trade them.

## Criteria

- ≥ 2% move on the named symbol within 60 minutes.
- OR ≥ 5% move within 24 hours.
- OR ≥ 1% move on BTC / ETH within 30 minutes for macro headlines.
- Volume_ratio ≥ 1.5 on the corresponding bars.

## Why log even non-traded ones

- Reveals which sources are first / reliable for market-moving news.
- Builds the dataset for the future per-source reliability score.
- Helps you decide which channels / RSS feeds to weight more heavily next time.

## Mandatory fields

- Price reaction at 5m / 15m / 1h / 4h.
- Volume reaction.
- OI / funding reaction (where available).
- Source(s) that first reported.
- Source(s) that re-reported (and how late).

## Related

- [[News_That_Moved_Market]]
- [[News_Item_Template]]
