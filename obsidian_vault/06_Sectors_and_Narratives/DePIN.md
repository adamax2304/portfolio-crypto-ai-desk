# DePIN (Decentralized Physical Infrastructure)

Configured narrative (keywords only, no symbols mapped today). Keywords: depin, decentralized infrastructure.

## What this sector includes (typical)

- Helium (HNT), IoTeX (IOTX), Render (RNDR — also AI), Filecoin, Akash, Hivemapper.

## What usually moves the sector

- Real-world adoption metrics (nodes deployed, coverage).
- AI compute demand (overlap with AI narrative).
- Partnerships with hardware vendors.

## What news matters

- Adoption / coverage milestones with real numbers.
- Major customer wins (a Fortune 500 buying network capacity).
- Token utility increase (fee burn, staking).

## What does not matter

- Generic "DePIN is the future" headlines.

## Telegram / social signals

- Quieter narrative on Telegram than AI / memes.
- When a DePIN coin moves on Telegram chatter, verify with on-chain network stats.

## Best regime

- `bullish trend` with broad altcoin participation.
- Sector is more story-driven than momentum-driven, so narrative heat matters.

## Indicators that matter most

- 7d return vs BTC.
- Volume sustainability over days.

## Common risk

- Low-cap names; liquidity issues.
- Concentrated holdings; insider distribution risk.

## Common fake signals

- "Decentralized X for Y" announcements with no usage data.

## Scoring posture

- Without configured symbols, the narrative will mostly fire on news mentions; the `representative_symbols` block in `NarrativeAgent` falls back to no candidates → narrative contribution muted.

## Recommended config

Add at least RNDR + HNT (if on Binance) + FIL + AKT:

```yaml
DePIN:
  symbols: [RNDR, HNT, FIL, AKT]
  keywords:
    - depin
    - decentralized infrastructure
    - decentralized compute
```

## Related

- [[Sector_Overview]]
- [[AI_Coins]] (overlap)

## Implemented status

- **Partially implemented** — keywords only, no symbol map.
