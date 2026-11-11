# Opus / LLM Catalyst Visibility Audit (PART 3)

**Date:** 2026-06-15 · Read-only. Source: `src/analysis/packet.py`, `src/stocks/llm_packet.py`.

## What the crypto packet shows Opus (`_build_catalyst_block`)

| Question | Answer | Detail |
|---|---|---|
| Recent news? | ✅ | reads latest `catalyst_events.jsonl` + news_trader macro pulse |
| Catalyst summaries? | ✅ | high-confidence catalysts section (confidence=="high", non-"other_news") |
| Symbol-specific catalysts? | ✅ | events carry primary_symbol + related_symbols |
| Funding/OI? | ✅ | DerivativesSummary block (funding rate, OI change, crowding/squeeze) |
| BTC/ETH regime? | ✅ | regime block in packet |
| Source timestamps? | ✅ | event.timestamp + freshness label per basket ("<1h"/"<6h"/"<24h"/"stale") |
| Marks stale data? | ⚠️ partial | freshness labels on baskets, BUT no hard "this catalyst is stale" marker on individual high-conf events |
| Separates fresh catalyst from old narrative? | ⚠️ partial | baskets carry freshness; high-conf catalyst list does not sort/flag by age |
| Says when catalyst is MISSING? | ✅ | explicit stub "catalyst scan has not run yet today" + "could not load catalyst JSONL" error |

## What the stocks packet shows Opus (`build_stocks_packet`)

| Question | Answer | Detail |
|---|---|---|
| Company news? | ✅ | CompanyNewsAgent output loaded per symbol |
| Earnings? | ✅ | earnings risk + days-to-earnings per symbol (yfinance) |
| Legal? | ✅ | legal_risk gate carries into packet |
| Analyst actions? | ❌ | classified by RSS classifier but **not surfaced in packet or scoring** |
| Options / OI? | ❌ | **no options or OI data for stocks at all** — only earnings + news |
| Says "missing" honestly? | ⚠️ partial | earnings shows "unknown — calendar lookup missing" when absent; options/OI absence is silent (never mentioned) |

## Verdict

- **Opus DOES see crypto catalysts, funding/OI, and regime** with freshness labels on baskets. Visibility is good.
- **Two visibility gaps:**
  1. **Crypto:** individual high-confidence catalysts are not age-flagged → Opus can treat a 10-hour-old catalyst as equally fresh as a 30-minute-old one.
  2. **Stocks:** no options/OI exists, and its absence is silent (the packet never says "options/OI: not available"). Analyst actions are collected but invisible to Opus.
- **No Opus→Telegram path** — Opus influence is packet-only; the Telegram message is rendered deterministically downstream and (today) does not echo the catalyst context Opus saw.
