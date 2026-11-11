# Exchange Tokens

## Status

**Not currently configured.** Recommended addition. Includes BNB, OKB, KCS.

## What usually moves the sector

- Exchange-specific news: revenue, user growth, BNB Chain activity.
- Regulatory risk for the parent exchange.
- Launchpad activity (BNB benefits from successful launches).
- Token buybacks / burns.

## What news matters

- Quarterly burn / buyback announcements.
- Regulatory wins / losses (SEC, EU MiCA).
- Major exchange product launches.

## What does NOT matter much

- Generic "BNB Chain transactions up" — usually noise unless it's a structural change.

## Telegram / social signals

- Moderate Telegram presence; aggregators frequently mention exchange tokens.

## Best regime

- `bullish trend` (exchange tokens are leveraged proxies for exchange revenue).
- Worst: regulatory event hitting the exchange.

## Common risk

- Regulatory risk is the #1 tail risk; can produce 20%+ drops on news.
- BNB is on Binance; OKB on OKX only (likely capped `not_on_anchor`); KCS on KuCoin (not configured in the desk's exchanges).

## Common fake signals

- "Binance listing X" — important for X, not for BNB itself.

## Recommended config

```yaml
Exchange tokens:
  symbols: [BNB]
  keywords:
    - binance
    - bnb chain
    - exchange token
```

OKB / KCS would require adding their venues to `config/exchanges.yaml` first.

## Related

- [[Sector_Overview]]
- [[Exchange_Overview]]

## Implemented status

- **Recommended / not implemented**.
