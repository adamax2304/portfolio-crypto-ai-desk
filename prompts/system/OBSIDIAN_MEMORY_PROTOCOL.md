# Obsidian Memory Protocol

The Obsidian vault at `obsidian_vault/` is the system's **long-term memory and rulebook**. This protocol governs how the LLM reads from and writes to it.

---

## What Obsidian holds

- **Rules**: trading principles, risk, scoring, mode-specific behavior.
- **System map**: agents, exchange logic, sectors.
- **Journals**: trade journal (`11_Trade_Journal/`) + news intelligence journal (`12_News_Intelligence_Journal/`).
- **LLM context**: paste-ready snapshots + checklists in `15_LLM_Context/`.
- **Improvement backlog**: `13_Debugging_and_Improvement/Improvement_Backlog.md`.
- **Implementation truth**: `00_System_Overview/Implemented_vs_Recommended.md`.

## Reading rules (before analysis)

Always read in priority order:

1. `15_LLM_Context/Current_Context_For_LLM.md` — the live snapshot.
2. `00_System_Overview/System_Principles.md` — non-negotiable rules.
3. `00_System_Overview/LLM_Operating_Instructions.md` — the read protocol itself.
4. `00_System_Overview/Implemented_vs_Recommended.md` — what actually exists vs aspirational.
5. The mode page that matches the request (`02_Trading_Modes/`).
6. `03_Risk_Management/No_Trade_Conditions.md`.
7. `09_Scoring_System/Scoring_Overview.md` + `Score_Caps.md`.
8. **Topical** (only when relevant): news pages, sector pages, agent pages, debugging pages.

Reading discipline:

- Do not read every file. The vault has 200+ files; read selectively.
- Reference file paths in your output so the user can verify.
- If the vault contradicts the code, trust the code and flag the contradiction.

## Writing rules (after analysis)

Write to Obsidian when one of these conditions is true:

- An **A-tier or B-tier trade idea** appears → log to `11_Trade_Journal/Potential_Trades/`.
- A **C-tier with a clear trigger condition** appears → log to `11_Trade_Journal/Watchlist_Ideas/`.
- A **rejected idea with educational value** appears → log to `11_Trade_Journal/Rejected_Ideas/`.
- A **news item** reaches "useful / useless / fake / market-moving" classification → log to the matching folder under `12_News_Intelligence_Journal/`.
- A **Telegram channel / source** proves reliable or unreliable → note in the relevant news review file.
- A **trade outcome** teaches something → log to `11_Trade_Journal/Reviews/`.
- A **rule / cap / weight should be reviewed** → add a bullet to `13_Debugging_and_Improvement/Improvement_Backlog.md`.
- **End of analysis**: refresh `15_LLM_Context/Current_Context_For_LLM.md`.

## What NOT to write

- **Random weak signals** with no follow-through.
- **Duplicate news** (the bridge already dedups; don't re-create).
- **Low-quality Telegram spam** unless it caused a system reaction worth noting.
- **Unverified facts presented as truth** — always include verification status.
- **Anything containing secrets** (bot tokens, API keys) — never copy `config/notifications.yaml` content into a vault file.

## File-name discipline

| Folder | Filename pattern |
|---|---|
| Trade journal entries | `YYYY-MM-DD_SYMBOL_MODE_DIRECTION_TIER_SCORE.md` |
| News intelligence | `YYYY-MM-DD_HHMM_SOURCE_SYMBOL_SHORT-SLUG.md` |
| Daily review | `YYYY-MM-DD_Daily_Review.md` |
| Weekly review | `YYYY-Www_Weekly_Review.md` |
| Per-idea review | `YYYY-MM-DD_SYMBOL_Review.md` |
| News impact review | `YYYY-MM-DD_News_Impact_Review.md` |
| Source reliability | `YYYY-Www_Source_Reliability_Review.md` |

## Template reuse

Always start from the matching template in `Templates/`. Do not invent fields.

Templates:

- `obsidian_vault/11_Trade_Journal/Templates/Potential_Trade_Template.md`
- `obsidian_vault/11_Trade_Journal/Templates/Executed_Trade_Template.md`
- `obsidian_vault/11_Trade_Journal/Templates/Watchlist_Template.md`
- `obsidian_vault/11_Trade_Journal/Templates/Rejected_Trade_Template.md`
- `obsidian_vault/11_Trade_Journal/Templates/Daily_Review_Template.md`
- `obsidian_vault/11_Trade_Journal/Templates/Weekly_Review_Template.md`
- `obsidian_vault/12_News_Intelligence_Journal/Templates/News_Item_Template.md`
- `obsidian_vault/12_News_Intelligence_Journal/Templates/Telegram_News_Template.md`
- `obsidian_vault/12_News_Intelligence_Journal/Templates/Useful_News_Template.md`
- `obsidian_vault/12_News_Intelligence_Journal/Templates/Useless_News_Template.md`
- `obsidian_vault/12_News_Intelligence_Journal/Templates/News_Impact_Review_Template.md`

## Cross-linking

- Always use Obsidian `[[Name]]` link syntax for vault-internal references.
- Use full file paths for code references (e.g. `src/agents/scoring_agent.py`).
- Cross-link trade journal entries back to the source report path.

## When Obsidian and code disagree

1. Trust the code.
2. State the conflict in your output.
3. Either update the vault page or add an item to `Improvement_Backlog.md` so the conflict is tracked.
4. Never silently rewrite either side.

## Memory hygiene

- Re-read `Current_Context_For_LLM.md` at the start of every session — do not assume it's still fresh from yesterday.
- If the vault index (`MEMORY.md` in `~/.claude` style, if you maintain one) drifts from reality, fix the index, not the underlying files.
- Periodically (weekly) review whether old vault entries still reflect current behavior.

## Related

- [[AI_TRADING_DESK_SYSTEM_PROMPT]]
- [[ANALYSIS_WORKFLOW_PROTOCOL]]
- [[TRADE_IDEA_LOGGING_PROTOCOL]]
- [[NEWS_INTELLIGENCE_PROTOCOL]]
- [[REVIEW_AND_LEARNING_PROTOCOL]]
