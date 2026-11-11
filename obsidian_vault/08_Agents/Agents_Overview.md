# Agents Overview

All agents live in [src/agents/](../../src/agents/). They follow a common pattern via `BaseAgent`: each has a `name`, a `run(...)` method that returns a typed model, and a `save_output()` that dumps to `data/processed/agent_outputs/<run_id>_<name>.json`.

## Agent execution order in `Supervisor.daily_report`

1. **MarketRegimeAgent** — regime label, breadth, key levels.
2. **MomentumScannerAgent** — per-symbol candidates (direction_bias, score, reason_tags).
3. **DerivativesAgent** — funding, OI, long/short, crowding.
4. **MultiExchangeDerivativesAgent** — Bybit + OKX cross-check.
5. **NewsAgent** — RSS news by symbol + narrative + macro keywords.
6. **CatalystAgent** — manual events + news joined per symbol.
7. **NarrativeAgent** — per-narrative heatmap.
8. **MacroGeopoliticsAgent** — risk-on / risk-off keyword pulse.
9. **SocialAttentionAgent** — Reddit + manual social mentions.
10. **CrowdLeaderAgent** — manual KOL watch.
11. **ExchangeFusionAgent** — cross-venue confirmation.
12. **CrowdAttentionAgent** — staging (silent / euphoria / etc).
13. **TechnicalSetupAgent** — entry, invalidation, targets, setup_quality.
14. **RiskAgent** — risk_score, warnings, valid_if.
15. **CriticAgent** — counter-thesis, weak_signal_dependency, late_or_crowded.
16. **ScoringAgent** — final_score, tier, caps, cap_reasons.
17. **TradeIdeaAgent** — assembles the trade idea + rejected list.
18. **CoverageAuditAgent** — names which data streams are missing/partial.

## Specialty / on-demand agents

- **ReviewAgent** — `python -m src.cli review`. Loads saved ideas, checks post-creation candles, MFE/MAE, entry-trigger detection.
- **WatchlistMonitor** — `python -m src.cli monitor-watchlist`. Re-evaluates C/rejected names on a cadence; alerts on tier upgrades.

## Per-agent files

- [[Supervisor_Agent]]
- [[Market_Regime_Agent]]
- [[Momentum_Scanner_Agent]]
- [[Derivatives_Agent]]
- [[Multi_Exchange_Derivatives_Agent]]
- [[News_Agent]]
- [[Telegram_News_Agent]] — **not implemented**, see file
- [[Catalyst_Agent]]
- [[Narrative_Agent]]
- [[Crowd_Attention_Agent]]
- [[Crowd_Leader_Agent]]
- [[Social_Attention_Agent]]
- [[Macro_Geopolitics_Agent]]
- [[Technical_Setup_Agent]]
- [[Risk_Agent]]
- [[Critic_Agent]]
- [[Scoring_Agent]]
- [[Trade_Idea_Agent]]
- [[Review_Agent]]
- [[Exchange_Fusion_Agent]]
- [[Coverage_Audit_Agent]]
- [[Watchlist_Monitor_Agent]]

## Agents folder vs. checklist categories

Some categories in the user's template don't map 1:1 to a file in `src/agents/`. Where there's no real agent, the corresponding page is marked Recommended:

- "Telegram News Agent" — no such file; Telegram is consumed via `news_trader_bridge` + `CrowdAttentionAgent`. See [[Telegram_News_Agent]].
- "Scoring Agent" — exists, that's [[Scoring_Agent]].
- "Candidate Ranking Agent" — actually `MomentumScannerAgent` + `MultiExchangeUniverseCollector.rank_candidates`. See [[Candidate_Ranking_Agent]].

## Implemented status

- **Implemented** — 22 agents listed.
- **Recommended** — Telegram News Agent (dedicated module rather than bridge consumer).
