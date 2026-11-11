# How to use the desk with Claude or Codex

The desk is built to be **paired with an LLM**, not used standalone. The reports and `context_for_llm.md` are deliberately structured so a fresh chat session can pick up the desk state with one paste.

## Quick-start prompts

### "Cold start" prompt (paste into a new chat)

```
You are working on the crypto-ai-desk project at C:\Users\adama\Documents\crypto-ai-desk.
Read these files first, in this order:
  1. obsidian_vault/00_System_Overview/LLM_Operating_Instructions.md
  2. obsidian_vault/00_System_Overview/System_Principles.md
  3. obsidian_vault/15_LLM_Context/Current_Context_For_LLM.md
  4. data/processed/context_for_llm.md
Then answer the question below. If the desk data is older than 3 hours, say so first.

Question: <YOUR QUESTION>
```

### "Evaluate an idea" prompt

```
Read obsidian_vault/15_LLM_Context/Pre_Trade_Checklist_For_LLM.md and
data/processed/context_for_llm.md. Then evaluate the idea for <SYMBOL>
in <MODE> mode. Output verdict, tier, score, caps, top reasons, invalidation.
```

### "Evaluate a Telegram message" prompt

```
Read obsidian_vault/05_News_Telegram_Catalysts_Sentiment/Telegram_News_Evaluation.md.
Then classify this Telegram message: <PASTE MESSAGE>.
Output: usefulness, sentiment, verification level, suggested filing folder.
```

## Do / Don't

**Do:**

- Paste `context_for_llm.md` for any market question. It is more compact than a full report.
- Reference specific vault pages with full paths so the LLM doesn't guess.
- Ask the LLM to write into `Trade_Journal/` or `News_Intelligence_Journal/` using the matching template file.
- Treat the LLM as a critic. Ask "what would cancel this trade?" before "should I take this trade?".

**Don't:**

- Don't ask the LLM to "find any trade you can". The desk's job is to find the few that survive filters; the LLM's job is to verify, not generate from scratch.
- Don't let the LLM invent invalidation levels or numbers that are not in the report.
- Don't trust LLM-generated trade thresholds over `config/scoring.yaml`.

## Pair-programming with Codex / Claude Code for system changes

- Always check `git status` / `git diff` first. The desk has no git? Then snapshot before changes.
- Modifications to `src/agents/scoring_agent.py` or `config/scoring.yaml` must be reviewed against [[Score_Caps]] and [[Scoring_Overview]].
- Adding a new agent: follow the pattern in `BaseAgent`, register it in `Supervisor.daily_report`, and create a corresponding `08_Agents/<NewAgent>.md`.

## Related

- [[LLM_Operating_Instructions]]
- [[Pre_Trade_Checklist_For_LLM]]
- [[System_Modification_Checklist_For_LLM]]
- [[Current_Context_For_LLM]]

## Implemented status

- **Implemented** — pairing pattern; export of the daily context to Obsidian via CLI is **Recommended**, see [[Obsidian_Export_Commands]].
