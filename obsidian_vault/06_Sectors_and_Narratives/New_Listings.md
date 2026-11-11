# New Listings

## Definition

Symbols recently listed on Binance / Bybit / MEXC. Not a configured narrative but a behavioral pattern.

## What usually moves a new listing

- Initial discovery — listing-day volume.
- Subsequent flushes — sell-the-news.
- Inclusion in the desk's universe — Stage 1 picks them up when they hit volume floor.

## How the desk treats new listings

- If only on MEXC → `mexc_only` flag, cap at 70 (65 if weak).
- If on Binance + MEXC, but not Bybit → reduced derivatives confirmation; lower data confidence.
- Initial listing day: ATR and EMA200 have no history; `MarketRegimeAgent` may emit `unknown` trend.

## Operator rules

- **Listing day**: scalp only, very small size.
- **First week**: distrust momentum signals; volatility is structural, not predictive.
- **After ~3 weeks**: structure starts to form; can begin to trade normally.

## Common patterns

- Listing pump (often pre-announcement leak) → vertical first 30 min → dump.
- Range build for 1–2 weeks, then a clean trend emerges.
- Sometimes long-term winners (e.g. some L2 listings) trend from listing.

## Common fake signals

- Pre-listing pump rumors that don't materialize.
- Coordinated Telegram blasts post-listing.

## Related

- [[Sector_Overview]]
- [[Listings]]
- [[Exchange_Announcements]]
- [[MEXC_Role]]

## Implemented status

- **Implemented** behaviorally — universe picks them up. Listing-aware scoring is **Recommended**.
