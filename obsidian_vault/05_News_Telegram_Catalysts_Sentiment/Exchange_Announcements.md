# Exchange Announcements

## What this covers

- Binance Announcements (RSS, marked `primary_source: true`).
- Coinbase Blog (currently disabled in `sources.yaml` due to Cloudflare 403 — recommended fix path).
- Bybit / OKX / MEXC announcements (no native RSS in the desk; reach via news_trader bridge channels like `BinanceListings`).

## Why these are weighted higher

- Highest-quality verification class.
- Move price faster than aggregator news.
- Cover the events most relevant to multi-exchange trading: listings, delistings, perp launches, maintenance windows, futures parameter changes.

## How the desk reads them

- `RSSNewsCollector` fetches `binance_announcements` and writes to `news_items` table with the source flag.
- `NewsAgent` surfaces them in `top_news` ordered by `importance`. Recommended improvement: multiply importance by 1.5 if `primary_source = true`.
- `CatalystAgent` does **not** auto-extract event type from announcements — it relies on whether a matching ticker is found via the existing `by_symbol` index.

## Operator workflow

1. Check the report's Top News block first.
2. For each high-importance item, click through to the announcement URL.
3. If the announcement is a listing / delisting / perp launch, add a manual event to `manual_events.yaml` so it's tagged correctly.
4. Re-run `update-data` to load it.

## Trade implications by announcement type

- **Spot listing on Binance / Coinbase** — most impactful. See [[Listings]].
- **Delisting** — sharp drops; the desk's `delisting` event type is risk-event (cap-active).
- **Perp launch** — can attract speculative volume; watch first 24h.
- **Margin / leverage parameter changes** — informational, rarely trade-relevant.
- **Maintenance / withdrawal pauses** — close positions if you're on that venue.

## Recommended improvements

- Re-enable Coinbase Blog with a Cloudflare-friendly fetcher (requests with browser User-Agent + cookie jar).
- Add native announcement scrapers for Bybit / OKX / MEXC.
- Auto-extract event type from announcement title using keyword regex (`will list`, `delist`, `pre-market`, `migration`, etc.) and pre-populate manual_events.

## Related

- [[News_Verification]]
- [[Primary_vs_Secondary_Sources]]
- [[Listings]]
- [[News_System_Overview]]

## Implemented status

- **Implemented** for Binance Announcements RSS only. Other venues require bridge or manual entry.
