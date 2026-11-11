# Pre-Analysis Checklist

Run this checklist **before** generating any trade ideas or making any analytical claim. If any line is unknown, say so — do not guess.

---

## A — Mode

- [ ] User's requested mode identified (scalp / intraday / swing / invest / review / news-only / candidate-debug).
- [ ] If `invest` → fallback to swing announced.
- [ ] Mode stated explicitly in first sentence of output.

## A0 — Weekend Mode

- [ ] If today is Saturday or Sunday in the project timezone, run [[Weekend_Mode_Checklist]] **on top of** this checklist.
- [ ] Read the Weekend Mode block in `data/processed/llm_analysis_packet.md` (or run `python -m src.cli weekend-status`).
- [ ] Adjust expectations: A-tier penalty active, weak signals capped at B, weak MEXC-only capped at C, chasing entries demoted.

## B — Context loaded

- [ ] `data/processed/llm_analysis_packet.md` read (or regenerated via `prepare-analysis`).
- [ ] `data/processed/context_for_llm.md` read.
- [ ] [[Current_Context_For_LLM]] read.
- [ ] Matching mode page read ([[Scalp_Mode]] / [[Intraday_Mode]] / [[Swing_Mode]] / [[Long_Term_Mode]]).
- [ ] [[System_Principles]] + [[LLM_Operating_Instructions]] re-confirmed.
- [ ] [[Score_Caps]] re-confirmed.

## C — Data freshness

- [ ] `data/processed/market_summary/last_update.json` read.
- [ ] `last_update.run_at` age vs mode:
  - scalp: < 30 min.
  - intraday: < 60 min.
  - swing: < 2 h.
  - invest fallback: < 4 h.
- [ ] If stale → recommend `update-data` first.

## D — Coverage

- [ ] `CoverageAuditAgent` block read (in the latest report or `agent_outputs`).
- [ ] Any subsystem flagged red / partial?
- [ ] Telegram bridge available? (`news_trader_bridge_latest.json` present and recent?)
- [ ] If coverage is degraded → state which streams are missing, downgrade confidence.

## E — Regime

- [ ] Regime label noted (`bullish trend` / `bearish trend` / `range/chop` / `transition` / `high-volatility danger`).
- [ ] `risk_mode` noted.
- [ ] Breadth above EMA20 % noted.
- [ ] BTC ATR percentile noted.
- [ ] If `high-volatility danger` → flag it; consider no-trade.

## F — Candidates

- [ ] Latest ranked candidates file present:
  `data/processed/candidates/universe_ranked_candidates_<mode>.json`?
- [ ] Top candidates per `MomentumScannerAgent` reviewed.
- [ ] For each candidate: invalidation present, data fresh, regime alignment.
- [ ] Caps active per candidate noted.

## G — News / Telegram

- [ ] `news_trader_bridge_latest.json` checked for `pulse.signal_count` + `strong_count`.
- [ ] Top Telegram sources in the lookback window noted.
- [ ] Macro keyword pulse (`MacroGeopoliticsAgent`) checked.
- [ ] Verification status per relevant symbol noted.
- [ ] No promoting rumor-only catalysts past cap 55.

## H — Risk

- [ ] `RiskAgent` warnings reviewed per candidate.
- [ ] `CriticAgent` verdicts reviewed per candidate.
- [ ] No-invalidation / stale / MEXC-only / rumor / extreme-funding caps respected.
- [ ] Operator-layer rules respected (per-trade ≤ 1%, per-day ≤ 3%, correlation buckets).

## I — Output preparation

- [ ] Mode stated in first sentence.
- [ ] Each candidate evaluated → tier classification.
- [ ] Trade ideas have mandatory fields: direction, entry, invalidation, risk, counter-thesis, tier, data_confidence, caps.
- [ ] NO TRADE prepared if zero A/B candidates pass.
- [ ] Watchlist (C-tier with trigger) prepared.
- [ ] Source paths (data/reports/..., data/processed/agent_outputs/...) cited.

## J — Logging plan

- [ ] List of files to create in `obsidian_vault/11_Trade_Journal/Potential_Trades/`.
- [ ] List of files to create in `Watchlist_Ideas/` (C-tier with trigger).
- [ ] List of news items to file under `obsidian_vault/12_News_Intelligence_Journal/`.
- [ ] [[Current_Context_For_LLM]] refresh plan ready.

If any box is unchecked, **stop**, fix that line, then proceed.

## Related

- [[System_Prompt_For_Analysis]]
- [[Post_Analysis_Checklist]]
- [[Pre_Trade_Checklist_For_LLM]] (per-trade)
- `prompts/system/ANALYSIS_WORKFLOW_PROTOCOL.md`

## Implemented status

- **Operator framework / checklist**.
