# Routine Prompt — Permission Contract Check (PART 2)

**Date:** 2026-06-19 · Confirms the Agent Council rewrite did NOT weaken the scheduled-run permission contract.

## Preserved verbatim in `opus-enriched-review-4h/SKILL.md`
| Contract element | Status |
|---|---|
| Advisory-only / read-mostly header (`# PERMISSION CONTRACT (PART 16 — read this FIRST)`) | **unchanged** |
| §A ALLOWED actions (read; read-only CLI list; WebSearch/WebFetch; write only the 3 artifact patterns; one Telegram) | **unchanged** |
| §B FORBIDDEN actions (no code edits anywhere incl. `prompts/`/`.claude/skills/`; no pytest; no fixes/refactors; no scoring/threshold/agent/strategy/scheduler change; no Windows-task restart; no process kill; no deps/paid APIs; no auto-trade; no `news_trader/` writes) | **unchanged** |
| §C absolute "do NOT request permission → skip + TODO" rule | **unchanged** |
| ALWAYS-SCAN rule (never recommend disabling/pausing/stopping scanner/monitor/scheduler) | **unchanged** |
| §Q TODO-only maintenance escape valve (`Fix Requests / TODO`, "DO NOT attempt to fix") | **unchanged** |

## What the rewrite added (advisory only — does not touch the contract)
- An internal **Agent Council reasoning structure** (9 virtual roles, one LLM run) — explicitly "no extra agents/processes/LLM calls", `suggested_effect` always `advisory_only`.
- A machine-readable **Agent Council JSON** block, explicitly "descriptive only — no code or action may be triggered from it", with a hard-coded `do_not_change` list (scoring, TP/SL, entry logic, routing, live execution).
- **Status/lifecycle language** rules (display wording only).
- Render structure sections `3A/3B` and a reworded §O Telegram **Status** block.

The Head Trader virtual role is explicitly **bound by §B FORBIDDEN and the ALWAYS-SCAN rule** — it can route decisions but cannot change strategy or execute.

## Net effect on permissions
**Stricter-or-equal.** The rewrite adds an explicit `do_not_change` list and repeats "advisory_only / no execution" inside the new council + JSON blocks — it narrows, never widens, what the run may do. No new write target, no new command, no new API, no permission-prompt path introduced. The run still completes autonomously with zero human permission prompts.

## Validator evidence
`python scripts/validate_agent_council_prompt.py` → **OK** (all permission-contract checks PASS: contract present, ALLOWED/FORBIDDEN present, no-permission-prompt rule present, no-pytest, no scheduler restart, no auto-trade, ALWAYS-SCAN, TODO-only).

## Verdict
**PERMISSION_CONTRACT_PRESERVED**
