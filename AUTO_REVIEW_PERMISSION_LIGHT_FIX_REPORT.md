# Auto-Review Permission-Light Fix Report (PART 16)

**Date:** 2026-06-03
**Scope:** Make the scheduled `opus-enriched-review-4h` Claude routine
permission-light — every cron run completes autonomously without
showing the user a single Claude Desktop permission prompt. Advisory
only. **No edits to `src/`, tests, scoring, agents, scheduler, or any
project code.**

---

## 1. Problem

Recent scheduled runs of the auto-review were triggering Claude Desktop
permission prompts because the routine prompt did not bound the action
space tightly enough. The routine could "feel" justified in:

- editing `src/` to fix a regression it spotted;
- running `pytest`;
- restarting `CryptoAIDesk_Scheduler` if it looked stale;
- killing python processes;
- adding a dependency to satisfy a missing import;
- patching a SKILL / prompt / config file mid-run.

Each of those would surface a permission dialog because the routine
fires without a human present. **The fix is to make the routine
contractually unable to take those actions, and to provide a single,
disciplined escape valve for surfacing maintenance work.**

---

## 2. Files Changed

| # | Path | Change |
|---|------|--------|
| 1 | `C:\Users\adama\.claude\scheduled-tasks\opus-enriched-review-4h\SKILL.md` | **Full rewrite via `mcp__scheduled-tasks__update_scheduled_task`.** New "**PERMISSION CONTRACT**" block at the very top (§A allowed, §B forbidden, §C absolute permission-prompt rule) precedes the workflow body. New `§Q` (Section 14 of every review) defines the `Fix Requests / TODO` escape valve in canonical format. Workflow body trimmed to PART 15 content (13-section review structure preserved). |
| 2 | `.claude/skills/enriched-review/SKILL.md` | Added PART 16 banner at the top describing "two execution modes" (manual vs scheduled). Pointed scheduled-mode reader to the routine SKILL.md permission contract. Added a dedicated subsection at the end making the §14 TODO escape valve mandatory in every review document. |
| 3 | `prompts/llm_review/enriched_market_review_protocol.md` | Inserted a PART 16 block-quote immediately under the `# Enriched Market Review Protocol` heading describing allowed / forbidden / no-permission-prompt rules. |
| 4 | `obsidian_vault/15_LLM_Context/Opus_Enriched_Market_Review_System_Prompt.md` | Added PART 16 paragraph next to the existing PART 15 banner. |
| 5 | `AUTO_REVIEW_PERMISSION_LIGHT_FIX_REPORT.md` (this file) | New. |

No code under `src/`, `tests/`, `scripts/`, or `config/` was touched.

---

## 3. New Hard Rules (verbatim)

These rules now appear in the routine prompt, the project skill, the
protocol doc, and the Obsidian system prompt — so the scheduled run
sees them in every place it reads context:

> **Scheduled review is read-mostly. It may create review artifacts
> only. It must never implement fixes.**

> **If permissions are required for a forbidden action, do not request
> them. Skip the action and write a TODO.**

---

## 4. Allowed Action Surface (routine SKILL.md §A)

1. **Read** anywhere under the project (reports, catalysts, news_items,
   proposed_signals, signal_outcomes, watchlist_alerts, LLM packets,
   prior auto-reviews, scheduler logs).
2. **WebSearch / WebFetch** when loaded (graceful fallback otherwise).
3. **Write ONLY** these three artifact patterns at project root /
   raw-data dir:
   - `OPUS_ENRICHED_REVIEW_LATEST.md` (overwrite)
   - `OPUS_ENRICHED_REVIEW_AUTO_<YYYY-MM-DD_HHMM>.md` (history copy)
   - `data/raw/enriched_review_sources/<ISO>.json` (citations JSON)
4. **Read-only / idempotent CLI commands** (explicit whitelist):
   - `python -m src.cli active-signals --asset-class crypto|stocks`
   - `python -m src.cli signal-stats --asset-class crypto|stocks`
   - `python -m scripts.detect_untracked_legacy_alerts --since <today>`
   - `python -m src.cli catalyst-scan --no-print` *(only when
     `data/catalysts/<today>/` is missing)*
   - `python -m scripts.ingest_enriched_review_sources --json <path>
     --asset-class <crypto|stocks>` *(idempotent UPSERT only; rows the
     routine itself cited)*
5. **One** compact Telegram message via the existing notifier.

Everything else is forbidden.

---

## 5. Forbidden Action Surface (routine SKILL.md §B)

Every item below is forbidden **without exception**, even when the
data clearly seems to ask for it. If observed, write a TODO instead.

- Edit ANY code anywhere (`src/`, `tests/`, `scripts/`, `config/`,
  `.claude/skills/`, `prompts/`, `obsidian_vault/`).
- Run `pytest` or any test runner.
- Implement bug fixes, refactors, or features.
- Modify scoring, thresholds, agents, strategy, or scheduler code.
- Modify or restart `CryptoAIDesk_Scheduler` /
  `CryptoAIDesk_TelegramCollector` Windows tasks.
- Kill / restart / `Stop-Process` any Python process.
- Edit this routine's own SKILL.md or any other skill / prompt / doc.
- Add new dependencies, paid APIs, or external services.
- Auto-trade, place orders, move funds, modify position state.
- Write under `C:\Users\adama\Documents\zeph ai projects\news_trader\`
  (READ-ONLY).
- Write outside the three artifact patterns in §A.3.
- Request elevated tool permissions for any forbidden action.

---

## 6. Permission-Prompt Rule (routine SKILL.md §C)

The absolute rule, present at the very top of the routine prompt:

> If executing an intended next step would require Claude Desktop to
> ask the human for permission, **DO NOT** request the permission.
> **DO** skip the step and write a TODO under §Q of the review.
>
> The review must finish autonomously every 4 hours without human
> interaction.

This is what stops the prompt cascade: when the routine considers an
action that would trigger a Claude Desktop modal, the contract says
**fall through to the TODO writer**, not to ask the user.

---

## 7. The TODO Escape Valve (routine §Q / skill §14 in every review)

Every review document now ends with a mandatory section:

```
## 14. Fix Requests / TODO

### TODO-<short-tag>
- **issue:**            <one-line description>
- **evidence:**         <file path / log line / SQL query result>
- **suggested manual fix:** <what a human-driven session should do>
- **priority:**         high | medium | low
- **first observed:**   <YYYY-MM-DD HH:MM EEST>
```

Examples of issues that belong in §14 (not code edits):

- Catalyst mapping below 50 % for several runs → "improve symbol
  resolver in catalyst layer" TODO.
- A reproducibly losing bucket in `signal-stats` → "tighten <bucket>
  scoring" TODO.
- Untracked-alert detector showing > 0 → "investigate PART 1
  regression" TODO.
- Stocks `earnings: UNKNOWN` reappearing → "earnings calendar
  regression" TODO.
- Stale RSS source consistently failing → "audit RSS source <name>"
  TODO.

If there are no issues to surface, §14 reads `_None._`. The section
must always exist so the diff-vs-prior-review can track new / closed
TODOs across runs. A separate, manually-driven Claude / Codex session
(with explicit elevated permissions) works the TODO list later.

---

## 8. Task Confirmation

```
taskId:        opus-enriched-review-4h
enabled:       true
cron:          30 0,4,8,12,16,20 * * *   (6 ×/day; 4-hour cadence)
description:   "Auto enriched-review every 4h … PART 15 (content) + PART 16
                (permission-light): read-mostly advisory, no code edits /
                tests / patches / scheduler ops / permission prompts. Fix
                Requests escape valve in review."
nextRunAt:     2026-06-03 04:38 EEST (next fire under PART 16 prompt)
lastRunAt:     2026-06-03 02:12 EEST (under PART 15 prompt, before this fix)
```

---

## 9. Dry Validation

Manual operational checks performed on the live project state:

| Check | Result |
|---|---|
| Routine prompt updated via MCP and persisted | ✓ confirmed via `list_scheduled_tasks` |
| `.claude/skills/enriched-review/SKILL.md` carries PART 16 banner + §14 TODO contract | ✓ |
| `prompts/llm_review/enriched_market_review_protocol.md` carries PART 16 block quote | ✓ |
| `obsidian_vault/15_LLM_Context/Opus_Enriched_Market_Review_System_Prompt.md` carries PART 16 paragraph | ✓ |
| No code modifications under `src/`, `tests/`, `scripts/`, `config/` | ✓ (grep audit) |
| `AUTO_REVIEW_PERMISSION_LIGHT_FIX_REPORT.md` present | ✓ |
| Scheduled task `enabled=true` and `nextRunAt` in the future | ✓ |

No production process was restarted. `CryptoAIDesk_Scheduler` and
`CryptoAIDesk_TelegramCollector` continue running undisturbed via
Windows Task Scheduler (PART 14 autostart loop).

---

## 10. Effect on the next scheduled run (≈ 04:38 EEST)

The next auto-review will:

1. See the PART 16 PERMISSION CONTRACT at the top of its own prompt.
2. Refuse to attempt any forbidden action even if the data invites it.
3. Continue to read scheduler / reports / catalysts / news_items /
   signal stats just like before.
4. Continue to write the three allowed artifacts + send one Telegram
   message.
5. Append a `Fix Requests / TODO` section (§14) — `_None._` if there
   are no issues, otherwise structured TODO entries.

The user should observe **zero Claude Desktop permission prompts** for
this and subsequent scheduled fires.

---

## 11. Limitations / Caveats

- Manual `/enriched-review` invocations still let the operator confirm
  tool prompts interactively. The PART 16 spirit (no code edits inside
  the review skill) is documented but enforcement of code-modification
  forbiddens during a manual operator session is *operator discretion*,
  not contractually blocked by the skill — by design, because the
  manual mode exists precisely for the operator to choose to do more.
- Claude Desktop must still be open for the cron task to fire. If
  closed, the task runs on next launch (single catch-up shot).
- The TODO list is the only way for the routine to escalate maintenance
  work. The user is expected to scan §14 in each review and decide
  which TODOs warrant a separate manual session.

---

## 12. Verdict

`READY_FOR_PERMISSION_LIGHT_AUTO_REVIEW`
