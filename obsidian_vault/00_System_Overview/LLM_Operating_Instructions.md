# LLM Operating Instructions

You are an LLM (Claude / Codex / GPT) being asked to evaluate trades, generate new ideas, review past performance, or modify the desk. Follow this protocol **before producing any output**.

## Step 0 — Frame check

Confirm what kind of request this is:

- **Trade evaluation** — "Is X a buy/short?", "Should I take this idea?"
- **New idea generation** — "Find me intraday longs", "Give me scalp setups"
- **News evaluation** — "Is this Telegram message useful?", "Did this news matter?"
- **Post-trade review** — "Why did this trade fail?", "Review yesterday's ideas."
- **System modification** — "Tweak scoring", "Add an agent", "Change a config."

Each path has its own checklist below.

## Step 1 — Mandatory pre-reading

Before producing **any** output, read the relevant vault pages:

1. [[System_Principles]] — non-negotiable rules.
2. [[Market_Regime_Overview]] — what regime BTC/ETH and breadth imply.
3. The mode-specific page:
   - [[Scalp_Mode]] for 30m–2h horizons.
   - [[Intraday_Mode]] for 4–24h horizons.
   - [[Swing_Mode]] for multi-day horizons.
   - [[Long_Term_Mode]] — flag as **not implemented** if asked about it; do not invent rules.
4. [[Risk_Management_Overview]] + [[No_Trade_Conditions]].
5. [[Scoring_Overview]] + [[Score_Caps]].
6. If Telegram or news is involved: [[Telegram_News_Evaluation]] + [[News_Verification]].
7. [[Data_Confidence]].
8. The matching checklist:
   - [[Pre_Trade_Checklist_For_LLM]]
   - [[Post_Trade_Review_Checklist_For_LLM]]
   - [[News_Evaluation_Checklist_For_LLM]]
   - [[System_Modification_Checklist_For_LLM]]

## Step 2 — Read the live desk context

Always read `data/processed/context_for_llm.md` from the project root. This is the freshest snapshot of the desk: regime, top candidates, ideas, rejected, funnel, news, coverage gaps. If asked about a specific symbol, also load the latest report under `data/reports/`.

If `context_for_llm.md` is older than 3 hours, say so and recommend `python -m src.cli update-data && python -m src.cli intraday-report` before trusting it.

## Step 3 — Hard rules you must never break

1. **Never hallucinate missing data.** If a field is empty in `context_for_llm.md` (e.g. derivatives unavailable, news none), state that, do not fabricate.
2. **Never treat Telegram rumors as confirmed news.** A signal from `news_trader_bridge` is at most `single_source` unless `tier = strong`.
3. **Never output a trade without invalidation.** If invalidation is None, the only valid answer is "no trade" or "watchlist".
4. **Never promote past a score cap.** If a cap pinned the score, the cap is the ceiling. Removing it requires a real data change, not narrative.
5. **Never push A-tier when caps are active.** A-tier requires score ≥ 80 **and** zero active caps.
6. **Never claim long-term mode behavior.** It is recommended, not implemented. See [[Long_Term_Mode]].
7. **Never write to `news_trader/` directory.** That project is read-only from here.
8. **Never auto-execute a trade.** This desk is research-only.
9. **If code and vault conflict, flag the conflict and trust the code.** Do not silently rewrite either.
10. **Be explicit about uncertainty.** Confidence levels in this system are `low / medium / medium-high / high` and tied to data quality, not vibes.

## Step 4 — Path-specific instructions

### Trade evaluation

- Run [[Pre_Trade_Checklist_For_LLM]] line by line.
- Cite the tier, score, score caps, regime alignment, and data confidence.
- Output the verdict in this exact shape:
  ```
  Verdict: take / watchlist / reject
  Tier requested: A / B / C / rejected
  Score: NN.N
  Caps active: [...]
  Top reasons to take: ...
  Top reasons to avoid: ...
  Invalidation: ...
  ```

### New idea generation

- Use only symbols that already appear in the latest ranked-candidates file or report.
- Do not introduce a symbol that the universe scanner has not surfaced.
- Honor regime: prefer longs in `bullish trend`, prefer shorts in `bearish trend`, prefer no-trade / counter-trend with cap in `range/chop` and `transition`.

### News evaluation

- Use [[News_Evaluation_Checklist_For_LLM]].
- Classify as `useful / useless / market-moving / fake or unverified / late or priced in / watch only`.
- Drop the artifact into [[12_News_Intelligence_Journal/README|the news journal]] using the matching template.

### Post-trade review

- Use [[Post_Trade_Review_Checklist_For_LLM]].
- Compare original score / tier / thesis to outcome.
- Identify which agent was right and which was wrong (regime / setup / derivatives / catalyst / risk / critic).
- Write the review into `11_Trade_Journal/Reviews/YYYY-MM-DD_Daily_Review.md`.

### System modification

- Use [[System_Modification_Checklist_For_LLM]].
- Never break the existing CLI surface.
- Never silently change `config/scoring.yaml`. Surface the diff first.
- Never bypass score caps "for one symbol". Caps are global rules.

## Step 5 — Output discipline

- If the data does not support a trade, say "no trade". This is correct behavior, not a failure.
- Keep the answer compact. Cite the file paths you read (e.g. `data/processed/context_for_llm.md`, `data/reports/intraday/...md`).
- If you are asked to log something into Obsidian, use the matching template file from `Templates/` and drop the new note in the correct folder.

## Related

- [[System_Principles]]
- [[Pre_Trade_Checklist_For_LLM]]
- [[Implemented_vs_Recommended]]

## Implemented status

- **Implemented** — every rule above is consistent with current code behavior.
