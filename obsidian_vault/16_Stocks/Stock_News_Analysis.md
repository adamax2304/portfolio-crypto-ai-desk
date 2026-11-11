# Stock News Analysis

[src/stocks/agents/company_news_agent.py](../../src/stocks/agents/company_news_agent.py) filters the shared SQLite `news_items` table for entries that either:

1. Are tagged `asset_class='stocks'`, OR
2. Have detected symbols in the configured stocks universe (handles cross-tagged sources like Bloomberg posts that mention both COIN and BTC).

## Categories (planned, partial in MVP)

The MVP just surfaces title + source + timestamp. Stage 6+ will classify each hit into one of:

- **company-specific** — single ticker, primary impact
- **sector-wide** — affects the whole sector ETF
- **index/macro** — CPI, FOMC, NFP, Powell speech
- **analyst upgrade/downgrade** — rating change
- **earnings/guidance** — pre-announcement or post-event reaction
- **legal/regulatory** — DOJ, FTC, SEC actions
- **product launch** — new SKU, feature, version
- **M&A** — acquisition, merger, divestiture
- **management commentary** — CEO/CFO public statements
- **competitor news** — material moves by direct competitor

## Reliability gates (config/stocks/risk.yaml → news)

- A-tier ideas require a **verified source** for the catalyst.
- Rumor-only catalysts are rejected.
- "Already priced in" catalysts get their weight halved (0.5).

## How to use in the report

Section 4 of the stocks report lists the top 3 news hits per symbol that has them. The scoring agent rewards `news_catalyst` with weight 10 (mode-multiplied). If a stock has news, that contributes; if it doesn't, scoring is unaffected (raw 0.0).

## Source pipeline

News comes from the same RSS collectors as crypto, plus the news_trader bridge if it's running. **The bridge is read-only — do not write to it.** Stock-specific news classification is a future improvement; for now, tagging is done at insert time via the asset_class column on news_items.
