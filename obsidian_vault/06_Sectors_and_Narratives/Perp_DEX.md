# Perp DEX

## Status

**Not currently configured.** Recommended addition.

## What this sector includes (typical)

- HYPE (Hyperliquid), DYDX, GMX, GNS, JUP (Solana perps).

## What usually moves the sector

- DEX vs CEX flow narrative.
- Volume share data (CEX outages or regulatory hits push volume to DEX).
- Funding mechanic news (e.g. Hyperliquid funding model changes).

## What news matters

- Major DEX launches.
- DEX fee shares / governance changes.
- CEX issues (driving rotation to DEX).

## Telegram / social signals

- HYPE has very active Telegram presence; DYDX moderate.

## Best regime

- `bullish trend` with risk-on — speculators chase DEX leverage.
- Lower beta in `bearish trend` but not safe.

## Common risk

- HYPE is not yet on Binance — `not_on_anchor` cap (75) applies if traded.
- Watch for exchange-listing rumors (HYPE on a major CEX = catalyst).

## Common fake signals

- "HYPE listing soon" rumors.

## Recommended config

```yaml
Perp DEX:
  symbols: [DYDX, GMX, JUP]
  keywords:
    - perp dex
    - hyperliquid
    - dydx
    - gmx
```

(HYPE is not on Binance — leave out unless you change `watchlist.yaml.symbols`.)

## Related

- [[Sector_Overview]]

## Implemented status

- **Recommended / not implemented**.
