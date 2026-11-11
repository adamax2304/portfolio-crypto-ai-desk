# How LLM Should Read This Vault

Reading order for a fresh LLM session. Optimized for context efficiency.

## Tier 1 — Must-read (every session, always)

1. [[LLM_Operating_Instructions]] — the protocol.
2. [[System_Principles]] — the rules.
3. [[Implemented_vs_Recommended]] — what actually exists vs what's documented as future.
4. [[Current_Context_For_LLM]] — the live desk snapshot.

## Tier 2 — Read on demand by topic

When the user mentions:

| Keyword | Read |
|---|---|
| trade / setup / idea | [[Pre_Trade_Checklist_For_LLM]], [[Score_Caps]], [[Trade_Idea_Template]], mode-specific page |
| review / past trade | [[Post_Trade_Review_Checklist_For_LLM]], [[Review_Template]], [[Review_Agent]] |
| news / Telegram / channel / rumor | [[Telegram_Integration]], [[Telegram_News_Evaluation]], [[News_Verification]], [[News_Evaluation_Checklist_For_LLM]] |
| regime / market / breadth | [[Market_Regime_Overview]], [[How_Regime_Is_Detected]] |
| scoring / cap / threshold | [[Scoring_Overview]], [[Score_Caps]] |
| sector / narrative | [[Sector_Overview]], the matching sector file |
| exchange / Binance / Bybit / MEXC | [[Exchange_Overview]], the matching role file |
| modify / adjust / config | [[System_Modification_Checklist_For_LLM]], [[How_to_Adjust_Filters]], [[How_to_Adjust_Scoring]] |
| debug / no trades / too many longs | [[Why_No_Trades]], [[Why_Too_Many_Longs]], [[Candidate_Debug_Guide]] |

## Tier 3 — Skim only if directly relevant

The agent-by-agent files in `08_Agents/`. Read the single relevant agent file rather than all of them.

## Reading discipline

- **Don't try to read everything.** The vault is ~80+ files. Tier 1 + relevant Tier 2 is enough.
- **Quote file paths when you reference vault content.** It helps the user verify.
- **Distinguish vault claims from code claims.** Vault may be slightly outdated; if conflict, trust the code (`src/agents/`, `config/`).

## Output discipline

- Cite paths: `obsidian_vault/01_Market_Regime/Market_Regime_Overview.md`.
- Cite code paths when the source matters: `src/agents/scoring_agent.py`.
- For trade decisions, follow the exact output shape in [[LLM_Operating_Instructions]] Step 4.

## Related

- [[LLM_Operating_Instructions]]
- [[Pre_Trade_Checklist_For_LLM]]

## Implemented status

- **Operator framework**.
