# Trade Idea Template (canonical)

Generic structure. Mode-specific variants exist for scalp / intraday / swing / (recommended) long-term, plus long / short / watchlist / rejected / review variants under [[11_Trade_Journal/README|11_Trade_Journal]].

## Fields (canonical TradeIdea shape from the desk)

```
Symbol:                 {SYMBOL/USDT}
Direction:              {long | short | watchlist only | no trade}
Tier:                   {A | B | C | rejected}
Score:                  {0..100}
Confidence:             {high | medium-high | medium | low}
Risk level:             {low | medium-low | medium | high}
Mode:                   {scalp | intraday | swing}
Timeframe label:        {e.g. "1h thesis / 15m execution (intraday 4-24h)"}
Exchange focus:         {binance | bybit | mexc}
Exchanges confirmed:    [binance, bybit, ...]
Data confidence:        {high | medium | low}

Thesis:                 {one short paragraph}
Evidence:
  - market regime: ...
  - returns: 24h ... / 7d ...
  - RS vs BTC: ...
  - volume ratio: ...
  - trend / setup_quality / RR-to-TP1
  - components dict
  - derivatives interpretation
  - catalyst interpretation
  - narrative status

Counterarguments:
  - critic counter-thesis
  - contradictions
  - regime risk
  - setup warnings
  - score is below active threshold (if C/rejected)

Entry plan:             {preferred entry zone language}
Invalidation:           {timeframe close beyond X}
Targets:
  - TP1
  - TP2
  - TP3

What to monitor:
  - BTC/ETH structure around local S/R
  - volume on retest
  - acceptance inside entry
  - funding/OI/crowding

Avoid conditions:
  - >2 ATR away from entry
  - BTC breakdown
  - unverified or contradicting catalysts
  - setup warnings (top 3)
  - risk-agent reasons_to_avoid (top 4)

Data sources used:
  - multi-exchange ccxt OHLCV (Binance/Bybit/MEXC)
  - Binance USD-M futures endpoints
  - Bybit/OKX public derivatives endpoints
  - RSS/news cache
  - manual events + manual narrative/social notes + news_trader_bridge
  - deterministic technical indicators
  - scoring.yaml weights + tier caps

Caps active:            {list of cap_reasons or none}
Status:                 {open | watchlist | no_trade}
```

## When you log this in Obsidian

Use the appropriate folder under `11_Trade_Journal/`:

- A/B-tier active → `Potential_Trades/` or `Executed_Trades/` after entry.
- C-tier → `Watchlist_Ideas/`.
- Rejected → `Rejected_Ideas/`.

## Filename convention

```
YYYY-MM-DD_SYMBOL_MODE_DIRECTION_SCORE.md
```

Example: `2026-05-23_SOL_intraday_LONG_78.md`.

## Related

- [[Long_Setup_Template]] · [[Short_Setup_Template]] · [[Watchlist_Template]]
- [[Scalp_Trade_Template]] · [[Intraday_Trade_Template]] · [[Swing_Trade_Template]] · [[Long_Term_Trade_Template]]
- [[Review_Template]] · [[Rejected_Idea_Template]]
- [[Potential_Trade_Template]] · [[Executed_Trade_Template]]

## Implemented status

- **Implemented** as a template; backed by the actual `TradeIdea` model.
