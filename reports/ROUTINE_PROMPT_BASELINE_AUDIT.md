# Routine Prompt Baseline Audit (PART 1)

**Date:** 2026-06-19 · Read-only inventory of the scheduled Opus/Sonnet review prompts before the Agent Council rewrite.

## Prompt / SKILL files in play
| File | Role |
|---|---|
| `~/.claude/scheduled-tasks/opus-enriched-review-4h/SKILL.md` (517 lines) | **THE master scheduled prompt** — permission contract (§A/§B/§C), slot awareness, market-mood routing, content workflow (§D–§Q), structure (§L), Telegram (§O), TODO (§Q). This is what cron executes. |
| `~/.claude/scheduled-tasks/opus-enriched-review-preus/SKILL.md` (16 lines) | Thin pointer — 16:20 slot; "runs the same SKILL.md" as 4h. |
| `~/.claude/scheduled-tasks/opus-enriched-review-postclose/SKILL.md` (16 lines) | Thin pointer — 23:15 slot; runs the same SKILL.md. |
| `prompts/llm_review/enriched_market_review_protocol.md` (repo) | Canonical advisory **protocol** (§1–§16) — the contract; permission contract PART 16 lives here too. |
| `.claude/skills/enriched-review/SKILL.md` (repo) | Operational checklist for **manual** `/enriched-review` runs (Phase 1–7). |
| `obsidian_vault/15_LLM_Context/Opus_Enriched_Market_Review_System_Prompt.md` (repo, 305 lines) | Named by the protocol as "the canonical behavior contract for the Opus run". |

## Routine status
| Routine | Slots | Status |
|---|---|---|
| `opus-enriched-review-4h` | 04:30 / 11:30 / 18:30 / 21:30 EEST | **ACTIVE** |
| `opus-enriched-review-preus` | 16:20 EEST (pre-US-open) | **ACTIVE** (sibling) |
| `opus-enriched-review-postclose` | 23:15 EEST (post-close) | **ACTIVE** (sibling) |
| `enriched-review-cycle-6` | one-time 2026-05-31 06:25 | **LEGACY** (one-shot, past) |
| `opus-decision-us-open` | — | **DISABLED 2026-06-01** (superseded by 4h) |
| `opus-decision-evening` | — | **DISABLED 2026-06-01** (superseded by 4h) |

All 6 market-aware slots are covered by the 3 active routines. The 3 inactive ones are legacy and **not required**; do not unpause without operator request (see `ROUTINE_TASK_STATUS_AUDIT.md`).

## Outputs / wiring
- `OPUS_ENRICHED_REVIEW_LATEST.md` (overwrite at project root) — latest review.
- `OPUS_ENRICHED_REVIEW_AUTO_<YYYY-MM-DD_HHMM>.md` (project root) — history copies.
- `data/raw/enriched_review_sources/<ISO>.json` — citations (ingested via `scripts/ingest_enriched_review_sources.py`, idempotent ON CONFLICT(url)).
- Telegram: ONE compact message per run via the existing notifier (§O of the master SKILL).
- Defer/blocked artifacts: `OPUS_ENRICHED_REVIEW_DEFERRED_<ISO>.md`, `OPUS_ENRICHED_REVIEW_BLOCKED_<ISO>.md`.

## Parts that MUST NOT be touched (safety)
- §A ALLOWED / §B FORBIDDEN / §C absolute permission-prompt rule (scheduled run must never ask for human permission).
- Read-mostly + advisory-only contract; no code edits / no pytest / no scheduler restart / no process kill from the scheduled run.
- ALWAYS-SCAN rule (never recommend stopping scanner/monitor/scheduler).
- §Q TODO-only maintenance escape valve.
- The content rules that protect scoring/TP-SL/entry/routing/filters/validity (no strategy change).

## Rewrite plan (single source of truth)
Insert the **Agent Council** analytical core into the master `opus-enriched-review-4h/SKILL.md` (auto-inherited by preus/postclose). Mirror a concise Agent Council section + status-language rules + JSON requirement into the repo protocol, Obsidian system prompt, and the manual `enriched-review` SKILL so manual and scheduled runs stay aligned. **No trading logic, no permission weakening.**
