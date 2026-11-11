# System Modification Checklist For LLM

Use when the user asks you to change the desk's code or configuration.

## Pre-flight

- [ ] Snapshot the current state. `git status / git diff` if the repo has git history. If not, copy `config/` + the file you're about to edit.
- [ ] Re-read [[Implemented_vs_Recommended]] to confirm whether the request is adding to implemented behavior or building something new.
- [ ] Re-read the relevant vault page(s) to confirm what the page claims about the system.
- [ ] Confirm with the user the scope and reversibility.

## Hard "do not" rules

- **Do not write to `news_trader/` directory or any subdirectory.** Read-only invariant.
- **Do not remove or weaken score caps.** Caps are constitutional.
- **Do not lower `no_clear_invalidation` penalty.**
- **Do not push A-tier threshold below 78.**
- **Do not skip pre-commit / lint hooks.**
- **Do not commit secrets** (the bot_token is in `config/notifications.yaml` — keep it out of any new file you generate).
- **Do not delete `agent_outputs/` or `data/processed/`** during a change.
- **Do not silently switch between modes (`mode="long_term"` → `intraday`)** — explicitly handle unknown modes by raising or warning.

## What to change vs leave alone

| Layer | OK to edit | Use caution | Hands off |
|---|---|---|---|
| YAML in `config/` | Filters, multipliers (within 0.7–1.3) | Thresholds | Bot secrets |
| `src/indicators/` | Add new indicators | Modify existing math (test first) | (none) |
| `src/agents/` | Add new agents | Modify scoring / risk caps | Caps in `scoring_agent.py` without explicit user OK |
| `src/cli.py` | Add commands | Modify existing commands' interfaces | Default modes |
| `src/notifiers/telegram.py` | Add new methods | Modify send behavior | Bot token handling |
| `src/data_collectors/news_trader_bridge.py` | Read-only consumers | (none) | Anything that writes to news_trader path |

## Workflow

1. **State the change** in one sentence + why.
2. **Locate every file affected**.
3. **Snapshot or git-status** before edit.
4. **Apply minimal edit**.
5. **Run smoke**: `python -m src.cli doctor && python -m src.cli intraday-report` and inspect the next report.
6. **If broken** → revert from snapshot, do not "patch over".
7. **Update vault**: if the system semantics changed, update the relevant page (especially [[Implemented_vs_Recommended]] and [[Score_Caps]]).

## Output template

```
Proposed change:
Files affected:
  - <path 1>
  - <path 2>
Risk:
  - <what could break>
Rollback plan:
  - <how to revert>
Vault pages to update:
  - <page>
Smoke test plan:
  - <commands + expected outcome>
```

## When user wants to add a feature recommended in this vault

- Check [[Improvement_Backlog]] for the recommended approach.
- If the user accepts the approach → implement minimally.
- After landing → update [[Implemented_vs_Recommended]] and remove from Improvement_Backlog.

## When user wants to add a feature NOT in this vault

- Ask: does it fit the system philosophy? (See [[System_Principles]].)
- If yes → add to [[Improvement_Backlog]] first, then implement.
- If no → push back politely and explain why.

## Related

- [[LLM_Operating_Instructions]]
- [[System_Principles]]
- [[Implemented_vs_Recommended]]
- [[How_to_Adjust_Filters]]
- [[How_to_Adjust_Scoring]]

## Implemented status

- **Operator framework / checklist**.
