# Sector Overview

Sectors are configured in `config/watchlist.yaml.narratives`. The desk's `NarrativeAgent` produces a heatmap per configured narrative; this folder documents how to interpret each one.

## Currently configured (in code)

- AI — symbols: TAO, FET, RNDR, NEAR.
- RWA — symbols: ONDO, LINK.
- L2 — symbols: ARB, OP.
- Memes — symbols: DOGE, PEPE, WIF.
- DePIN — symbols: (empty list; keyword-driven only).
- Gaming — symbols: (empty list; keyword-driven only).

## Documented in this vault but **not configured** (recommended additions)

- Solana ecosystem.
- Base ecosystem.
- Perp DEX (HYPE, GMX, DYDX style).
- Bitcoin ecosystem (Ordinals / Runes / BRC-20).
- Exchange tokens (BNB, OKB, KCS).
- Stablecoin-related.
- Privacy coins.
- New listings (procedural; pulled directly from listing announcements).

To add a sector, edit `config/watchlist.yaml.narratives` with `symbols` and `keywords` and re-run a report.

## How sectors flow into scoring

- `NarrativeAgent.run` builds a `NarrativeSummary` per configured narrative.
- `ScoringAgent._symbol_narrative_quality(symbol, narratives)` picks the highest-heat narrative the symbol belongs to and contributes to the `narrative` component (weighted 10 base, 1.30× in swing).

## How sectors should be read

- Track which narrative is `hot` / `rising` per day.
- Swing biased toward `hot` narratives; intraday neutral; scalp ignores narrative.
- Bear regime mutes narrative weight (×0.85) — narratives matter less in risk-off.

## Recommended additions to config

```yaml
narratives:
  Solana ecosystem:
    symbols: [SOL, JTO, JUP, BONK, WIF, PYTH]
    keywords:
      - solana
      - sol ecosystem
      - jito
      - jupiter
  Base ecosystem:
    symbols: [AERO, DEGEN, BRETT]
    keywords:
      - base
      - coinbase base
      - aerodrome
  Perp DEX:
    symbols: [GMX, DYDX, HYPE]
    keywords:
      - perp dex
      - hyperliquid
      - dydx
  Bitcoin ecosystem:
    symbols: [STX, ORDI]
    keywords:
      - bitcoin l2
      - stacks
      - ordinals
      - runes
  Exchange tokens:
    symbols: [BNB, OKB, KCS]
    keywords:
      - binance
      - okx
      - kucoin
  Privacy:
    symbols: [XMR, ZEC, DASH]
    keywords:
      - privacy
      - monero
      - zcash
```

## Related

- [[Narrative_Agent]]
- [[Narrative_Heatmap]]
- [[Sector_Overview]]
- [[AI_Coins]] · [[RWA]] · [[L2]] · [[Solana_Ecosystem]] · [[Base_Ecosystem]] · [[Meme_Coins]] · [[DePIN]] · [[Gaming]] · [[Perp_DEX]] · [[Bitcoin_Ecosystem]] · [[Exchange_Tokens]] · [[Stablecoin_Related]] · [[Privacy_Coins]] · [[New_Listings]] · [[How_Sectors_Behave_By_Regime]]

## Implemented status

- **Implemented** for configured narratives. **Recommended** for the rest.
