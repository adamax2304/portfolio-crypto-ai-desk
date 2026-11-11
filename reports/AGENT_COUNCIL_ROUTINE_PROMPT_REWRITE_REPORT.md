# Agent Council Routine Prompt — Rewrite Report (PART 11)

**Date:** 2026-06-19 · **Type:** prompt/SKILL text rewrite (advisory analytical core). **No trade logic / scoring / routing / permission weakening.**

## What changed
The scheduled Opus/Sonnet enriched-review prompt now runs as an **Agent Council**: a single LLM run that reasons through nine virtual trading-desk roles, then a Head Trader synthesis — no extra agents, processes, or LLM calls.

### Files edited (prompt/doc text only)
1. **`~/.claude/scheduled-tasks/opus-enriched-review-4h/SKILL.md`** (master scheduled prompt — auto-inherited by the `preus` + `postclose` sibling routines):
   - Added **AGENT COUNCIL REVIEW MODE** section: the 9 virtual agents with responsibilities + reason-code sets, the one-LLM-run rule, per-agent output schema (verdict / confidence / reason_codes / data_missing / suggested_effect=`advisory_only` / facts_used).
   - Added the **mandatory machine-readable Agent Council JSON** spec (agents[] + head_trader{} with `do_not_change` list), explicitly advisory-only.
   - Added **STATUS / LIFECYCLE LANGUAGE** rules (no raw `expired`, no bare `+0R`, no "no active trades"; expired split; R wording).
   - Updated render structure (§L) with `## 3A. Agent Council JSON` + `## 3B. Agent Council Table` (decimal labels chosen to preserve every existing `§N`-of-review cross-reference in §D–§Q), and made the Market Mood block "DRIVEN BY the Agent Council".
   - Rewrote the §O Telegram template to the **Status block** format (Open / Waiting / Review-Shadow / Entered-unresolved / No-entry / Needs-review) + Decisions (long/short/catalyst-watch + avoid). Kept ≤3500-char rule + advisory-only.
2. **`prompts/llm_review/enriched_market_review_protocol.md`** — added **§17 Agent Council Review Mode** (contract summary: 9 agents, JSON, status language), pointing to the master SKILL as the operative copy. PART 16 permission contract untouched.
3. **`.claude/skills/enriched-review/SKILL.md`** (manual `/enriched-review`) — Phase 6 now requires the Agent Council + JSON + Table + status language; render structure updated with 3A/3B.
4. **`obsidian_vault/15_LLM_Context/Opus_Enriched_Market_Review_System_Prompt.md`** — added an Agent Council Review Mode section + status-language rule (canonical behavior contract stays aligned).
5. **`scripts/validate_agent_council_prompt.py`** (new) — read-only validator for all required invariants.

## How the council works inside ONE LLM run
The model reads internal data once (§E), then writes the review reasoning sequentially through the nine roles — it is an *internal reasoning structure*, not orchestration. No tool is called per agent; nothing is spawned. The output is a markdown review + one advisory JSON block. `suggested_effect` is always `advisory_only`; the Head Trader is bound by §B FORBIDDEN + ALWAYS-SCAN.

## Why this adds no new agents/processes
- No code, no scheduler change, no new task. The three active routines already existed and already invoke the master SKILL.md; only the prompt text changed.
- "Agent Council" is a prompt-level reasoning pattern, explicitly "no extra physical agents / processes / LLM calls / sub-tasks."

## Slot behavior
Unchanged 6-slot market-aware schedule (04:30/11:30/16:20/18:30/21:30/23:15 EEST); the council is slot-aware — it carries the slot type into the JSON `slot_type`, the title, and the Telegram header, and applies the existing per-slot focus (crypto-overnight → US-prep → pre-open legal/earnings checks → US-open confirm/fail → late-session risk → post-close wrap).

## Safety
Permission contract preserved/stricter (see `ROUTINE_PROMPT_PERMISSION_CONTRACT_CHECK.md`); validator + doc tests pass (`AGENT_COUNCIL_ROUTINE_PROMPT_TEST_RESULTS.md`). No scoring / TP-SL / entry / routing / filters / validity change; no live/scalp/C-tier/BE-partial-trailing enabling.

## Verdicts
`AGENT_COUNCIL_ROUTINE_PROMPT_READY · ONE_LLM_RUN_VIRTUAL_AGENTS · PERMISSION_CONTRACT_PRESERVED · STATUS_LANGUAGE_INTEGRATED · TELEGRAM_REVIEW_SUMMARY_UPDATED · NO_TRADE_LOGIC_CHANGE`
