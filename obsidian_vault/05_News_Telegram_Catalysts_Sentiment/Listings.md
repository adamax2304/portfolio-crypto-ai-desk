# Listings

## What "listing" means here

An exchange adding a symbol to spot or perpetual trading. Subtypes:

- Spot listing on Binance / Coinbase / OKX / Bybit / MEXC.
- Perp listing on Binance USD-M, Bybit linear, etc.
- "Innovation zone" / "launchpool" — pre-listing precursor.

## Why it matters

- A confirmed major-exchange listing can produce a sharp move in the hours before and after the official announcement.
- Pre-listing leaks via Telegram are common.
- After the listing event itself, "sell-the-news" flushes are also common.

## How the desk handles it

- `CatalystAgent` does not have a dedicated "listing" code path; a manual event of `type: listing` adds it to `catalysts` (not `risk_events`).
- `news_trader_bridge` keywords `listing`, `list` are tagged bullish.
- `ScoringAgent` does not give a listing-specific bonus — verification ladder applies.
- The score cap for unverified rumor-only catalysts (55) is the main brake.

## Operational checklist for a listing rumor

1. Source channel? If primary (exchange page) → likely real.
2. Is the listing already announced? Check the exchange's announcement page directly.
3. Is the symbol already traded on Binance? If yes, "listing on Binance" is meaningless (already there).
4. Spot or perp? Perp listings drive different flow patterns.
5. Time of day — listings often go live at scheduled exchange windows.
6. Volume in the hour before the announcement — leaked listings show volume + price drift.

## Trade patterns

- **Pre-announcement leak run-up** → fade after the official tweet, OR ride momentum for a few minutes then exit. High risk.
- **Post-announcement open spike + dump** — common on smaller listings; do not chase.
- **Post-announcement open spike + continuation** — happens when narrative aligns (e.g. AI listing during AI rotation).

## How to log

- Pre-event: log as a Telegram News in [[Telegram_News/README|Telegram_News]] with verification = single_source.
- After the event: move to [[Useful_News]] if it produced a clean tradable move, or [[Useless_News]] if it whipsawed.

## Related

- [[News_Verification]]
- [[Primary_vs_Secondary_Sources]]
- [[Exchange_Announcements]]
- [[Catalyst_Agent]]
- [[Useful_News]]

## Implemented status

- **Implemented** (as a manual event type + bridge keyword).
