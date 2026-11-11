# 16_Stocks

Stock and index analysis. **Asset class: stocks** — distinct from crypto.

This folder is loaded into the stocks LLM packet (`data/processed/llm_stocks_packet.md`) when you run `python -m src.cli prepare-analysis --asset-class stocks --mode <mode>`. Crypto notes in folders 00-15 are not relevant here unless explicitly cross-referenced.

## Contents

- [[Stock_Market_Overview]] — what the stocks module is, how it differs from crypto.
- [[Stock_Market_Regime]] — SPY/QQQ/IWM/DIA + VIX classification.
- [[Sector_Rotation]] — sector ETFs, strongest/weakest mapping.
- [[Earnings_Risk]] — how earnings windows affect each mode.
- [[Stock_News_Analysis]] — company / sector / index / macro news classification.
- [[Stock_Technical_Setups]] — mode-aware entry / invalidation / target conventions.
- [[Stock_Scoring]] — weight breakdown, mode/regime multipliers, tier thresholds.
- [[Stock_Risk_Management]] — hard rejects, caps, gap rules.
- [[Stock_Trade_Idea_Template]] — required fields for stock A/B-tier ideas.
- [[Stock_Intraday_Mode]] / [[Stock_Swing_Mode]] / [[Stock_Invest_Mode]] — per-mode playbooks.

## Run flow

```
python -m src.cli stocks-update-data --mode intraday
python -m src.cli stocks-intraday-report
python -m src.cli prepare-analysis --asset-class stocks --mode intraday
```

Reports land under `data/reports/stocks/{mode}/`. Signal performance is filtered with `python -m src.cli signal-stats --asset-class stocks`.
