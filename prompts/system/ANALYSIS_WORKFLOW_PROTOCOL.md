# Analysis Workflow Protocol

The deterministic workflow every analysis must follow. Linear, numbered, no skipping.

---

## Step 0 — Determine mode

Map the user's request to one of the supported modes:

| User phrasing | Mode |
|---|---|
| "scalp", "5m", "next hour", "now" | `scalp` |
| "intraday", "today", "morning", "still valid" | `intraday` (default) |
| "swing", "multi-day", "few days" | `swing` |
| "invest", "long-term", "weeks", "months" | `invest` (fallback to `swing`; see [[MODE_SELECTION_PROTOCOL]]) |
| "review", "what worked", "ревью" | `review` |
| "news", "Telegram", "channel said" | `news-only` |
| "debug X", "why X" | `candidate-debug` |
| nothing specific | `intraday` |

State the mode explicitly in your first sentence.

## Step 1 — Prepare context (mandatory)

Run (or ask the user to run):

```powershell
python -m src.cli prepare-analysis --mode <mode>
```

This generates `data/processed/llm_analysis_packet.md`. If it already exists and is < 30 minutes old, reuse it. Otherwise, regenerate.

Then read in this order:

1. `data/processed/llm_analysis_packet.md`
2. `data/processed/context_for_llm.md`
3. `obsidian_vault/15_LLM_Context/Current_Context_For_LLM.md`
4. The mode page (Scalp_Mode / Intraday_Mode / Swing_Mode / Long_Term_Mode).
5. `obsidian_vault/03_Risk_Management/No_Trade_Conditions.md`.
6. `obsidian_vault/09_Scoring_System/Scoring_Overview.md` + `Score_Caps.md`.

## Step 2 — Update data if needed

If `last_update.json` is older than:

- 30 minutes for scalp,
- 60 minutes for intraday,
- 2 hours for swing,
- 4 hours for invest fallback,

run:

```powershell
python -m src.cli update-data
```

If candidate data is missing or stale:

```powershell
python -m src.cli update-universe
python -m src.cli scan-universe --mode <mode>
```

If news / Telegram context is stale:

- Confirm `news_trader` is running (read-only consumer can only return what news_trader has written).
- Otherwise RSS is the only fresh source.

## Step 3 — Run mode-specific report

| Mode | Command |
|---|---|
| scalp | `python -m src.cli scalp-report --auto-universe` |
| intraday | `python -m src.cli intraday-report --auto-universe` |
| swing | `python -m src.cli swing-report --auto-universe` |
| invest | `python -m src.cli swing-report --auto-universe` (fallback — flag it) |
| review | `python -m src.cli review` |
| news-only | (no report; consume context_for_llm.md + news_trader_bridge snapshot) |
| candidate-debug | `python -m src.cli candidate-debug --symbol X --mode <mode>` |

## Step 4 — Evaluate every candidate

For each candidate from the latest ranked file, check the following in order — fail-fast:

1. **Invalidation present?** If no → reject; document reason.
2. **Data fresh (< 3h)?** If no → reject with stale-data cap.
3. **Regime alignment?** If long-in-bearish or short-in-bullish → mark conflict and downgrade.
4. **Setup quality** from `TechnicalSetupAgent` (≥ 60 = healthy).
5. **Momentum + RS** (vs BTC; volume_ratio ≥ 1.5).
6. **Derivatives** (funding healthy? OI direction?).
7. **Cross-exchange** (anchor + derivatives confirmed?).
8. **Telegram / news / catalyst** (verified? rumor?).
9. **Narrative / crowd attention** (`hot` / `rising` / `euphoria` / `rumor_driven`).
10. **Risk** (RiskAgent score, warnings).
11. **Critic verdict** (accept / watch / reject).
12. **Caps active?** List them.
13. **R/R to TP1 ≥ 1?** If no → poor_risk_reward penalty.

Anything that fails gates 1, 2 → rejected immediately. Everything else → continue to scoring.

## Step 5 — Classify

Use `ScoreBreakdown` + `tier`. If you are re-classifying manually, apply the exact rules from [[RISK_AND_SCORING_PROTOCOL]]:

- A-tier: score ≥ 80 + no caps + long/short.
- B-tier: score ≥ 65 + valid invalidation.
- C-tier: score ≥ 50 OR conditional setup.
- Rejected: anything else.

## Step 6 — Output trade ideas

Only output trades that pass Step 5 as A or B-tier. For each:

- Use the canonical trade idea card shape (see `obsidian_vault/10_Trade_Idea_Format/Trade_Idea_Template.md`).
- Cite source paths (`data/reports/...`, `data/processed/agent_outputs/...`).
- Explicitly state caps if active.

If there are zero A/B ideas, output an explicit "NO TRADE" with reason, plus the top 3 watchlist names if any.

## Step 7 — Log outputs

Follow [[TRADE_IDEA_LOGGING_PROTOCOL]] and [[NEWS_INTELLIGENCE_PROTOCOL]] for where files go.

Until the `log-idea-to-obsidian` CLI is implemented, this is manual:

1. Copy the matching template from `obsidian_vault/11_Trade_Journal/Templates/` or `obsidian_vault/12_News_Intelligence_Journal/Templates/`.
2. Save as `YYYY-MM-DD_SYMBOL_MODE_DIRECTION_TIER_SCORE.md` in the right folder.
3. Cross-link back to the report path.

## Step 8 — Update memory

- Refresh `obsidian_vault/15_LLM_Context/Current_Context_For_LLM.md` with the new snapshot block (mode, regime, top candidates, active watchlist, news pulse, focus next).
- If lessons emerged → add a bullet to `obsidian_vault/13_Debugging_and_Improvement/Improvement_Backlog.md`.

## Step 9 — Closing summary

End your response with:

1. **Compact trade table** (symbol / tier / score / direction / entry / SL / TP1 / caps).
2. **Risk warnings**.
3. **What to monitor next**.
4. **Data that was weak/missing** (from `CoverageAuditAgent`).
5. **Logging actions taken** (paths created/updated).

If any step in 1–9 had to be skipped, **explicitly say so** at the end.

## Anti-patterns to refuse

- Generating trades without running the report.
- Producing A-tier without consulting cap_reasons.
- Treating a Telegram message as a catalyst without verification.
- Promoting a C-tier to B-tier because "the chart looks good".
- Silently switching modes between sections of the analysis.
- Skipping the memory update step at the end.

## Related

- [[AI_TRADING_DESK_SYSTEM_PROMPT]]
- [[OBSIDIAN_MEMORY_PROTOCOL]]
- [[TRADE_IDEA_LOGGING_PROTOCOL]]
- [[NEWS_INTELLIGENCE_PROTOCOL]]
- [[MODE_SELECTION_PROTOCOL]]
- [[RISK_AND_SCORING_PROTOCOL]]
- [[WATCHLIST_AND_TIER_PROTOCOL]]
- [[REVIEW_AND_LEARNING_PROTOCOL]]
