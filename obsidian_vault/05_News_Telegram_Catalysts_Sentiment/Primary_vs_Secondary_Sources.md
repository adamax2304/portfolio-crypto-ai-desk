# Primary vs Secondary Sources

## Definition

- **Primary** — the authority that owns the event:
  - Exchange announcement page (Binance, Coinbase, OKX).
  - Project's own blog or governance forum.
  - Regulator filings (SEC, CFTC, ESMA).
  - Tokenomics / unlock schedule maintained by the project.
- **Secondary** — anyone reporting / aggregating:
  - News aggregators (CoinDesk, Cointelegraph, Decrypt).
  - Telegram channels, Twitter accounts.
  - Re-shares, even of primary content.

## How the desk marks it

`config/sources.yaml.rss_feeds[*].primary_source: true|false`:

- Binance Announcements: `true`.
- Coinbase Blog: `true` (currently disabled due to Cloudflare 403).
- CoinDesk: `false`.
- Cointelegraph: `false`.
- Decrypt: `false`.

`NewsAgent` does not currently weight by this flag — it surfaces all items by importance. Recommended improvement: multiply `importance` by 1.5x for primary-source items.

## How to use it

- **Listings**: only trust primary (exchange) page. Secondary "X is being listed" rumors get the rumor cap.
- **Unlocks**: only trust the project's tokenomics page. Aggregator unlock dates can be off by a day.
- **Partnerships**: only trust the projects involved. Press-release wires often pre-leak; treat as single-source.
- **Regulatory**: primary only — filings, court documents. Tweets are NOT primary.

## What "verified" means here

A reasonable verification flow for a trade idea:

1. Primary source confirms event existence.
2. At least one secondary source corroborates within 30 minutes.
3. Price + volume show measurable reaction within 30–60 minutes.

When all three are present, classify as `confirmed`. Anything less is `single_source`.

## Operator behavior

- Before trading on a "listing on Binance" story, open `https://www.binance.com/en/support/announcement` (the actual page) and confirm.
- Before trading on an "unlock today" story, open the project's tokenomics page.
- Save the URL in the journal entry.

## Related

- [[News_Verification]]
- [[Listings]]
- [[Token_Unlocks]]
- [[News_System_Overview]]

## Implemented status

- **Partially implemented** — `primary_source` flag exists but does not multiply score yet.
