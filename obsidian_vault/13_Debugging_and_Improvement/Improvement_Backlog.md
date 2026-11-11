# Improvement Backlog

A running list of recommended improvements. Add to this page when you spot something during a review. Move items to "Done" when implemented.

## Pending

### Modes

- [ ] Add `long_term` mode (config + agent + setup TF) — see [[Long_Term_Mode]].
- [ ] Add per-mode `setup_timeframe` so scalp uses 5m, intraday uses 1h, swing uses 4h.
- [ ] Add a fast intraday (15m) regime overlay for scalpers.

### Regime

- [ ] Wire `low-volatility compression` label properly in `MarketRegimeAgent`.
- [ ] Add BTC dominance + stablecoin dominance reads.
- [ ] Add 15m regime overlay.

### Indicators

- [ ] Add VWAP (anchored + session).
- [ ] Add MACD as a context-only indicator.
- [ ] Add swing-high/swing-low detection (not just window extrema).
- [ ] Add explicit BoS / ChoCH flags.

### Risk

- [ ] Position-sizing recommendation field on TradeIdea (`recommended_risk_pct`).
- [ ] Per-mode stop multiplier (default 1.2 ATR; scalp 0.8–1.0, swing 1.5–1.8).
- [ ] Time-stop: emit a target holding window per mode.
- [ ] Correlation-aware risk: cluster-cap exposure across correlated symbols.

### News / Telegram

- [ ] Per-source reliability score in `news_trader_bridge`.
- [ ] Add Twitter / X collector.
- [ ] Add automated unlock calendar (TokenUnlocks API).
- [ ] Add Bybit / OKX / MEXC native announcement scrapers.
- [ ] Re-enable Coinbase RSS with Cloudflare-aware fetcher.
- [ ] Multi-lingual sentiment keywords.
- [ ] Catalyst sentiment classification beyond event type.
- [ ] Automated `review-news-impact --date YYYY-MM-DD` skeleton generator.

### Sectors

- [ ] Configure Solana ecosystem, Base ecosystem, Perp DEX, Bitcoin ecosystem, Exchange tokens, Privacy, Stablecoin Related narratives.
- [ ] Auto-decay narrative scores over time.
- [ ] Per-narrative cool-down.

### Exchange

- [ ] MEXC derivatives collector.
- [ ] Per-symbol book depth check.
- [ ] Slippage model in `TradeIdea`.

### Scoring

- [ ] Move score cap values from `scoring_agent.py` to `scoring.yaml.thresholds.caps`.
- [ ] Add primary-source bonus to `catalyst_news` component (multiply `importance` by 1.5 for primary).
- [ ] Add RSI-state to MomentumCandidate and use in RiskAgent.

### Telegram bot

- [ ] Add B-tier downgrade alerts (B → C) to surface thesis weakening.
- [ ] Per-mode cooldown.
- [ ] Add a "doctor" alert: when coverage degrades, ping operator.

### Obsidian / journal

- [ ] `python -m src.cli export-knowledge-base --format obsidian`.
- [ ] `python -m src.cli log-trade-to-obsidian --idea-id <id>`.
- [ ] `python -m src.cli log-news-to-obsidian --news-id <id>`.
- [ ] `python -m src.cli review-news-impact --date YYYY-MM-DD`.
- [ ] `python -m src.cli obsidian-daily-context` — refresh [[Current_Context_For_LLM]] from latest report.

### Review / backtest

- [ ] Full backtest engine (`python -m src.cli backtest --start --end --mode`).
- [ ] Backtest report joining SQLite + candle cache.
- [ ] Persistent historical regime + breadth.

### Streamlit / UI

- [ ] Streamlit dashboard (listed in Priority 3 remaining work in README).

## Done

(Move items here as they ship.)

## Related

- [[Implemented_vs_Recommended]]
