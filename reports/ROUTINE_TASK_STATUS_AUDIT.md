# Routine / Task Status Audit (PART 9)

**Date:** 2026-06-19 · Read-only inventory of `~/.claude/scheduled-tasks/`. **Nothing unpaused** (no operator request to do so).

## Routines
| Task | Slot(s) EEST | Runs which prompt | Status | Classification |
|---|---|---|---|---|
| `opus-enriched-review-4h` | 04:30 · 11:30 · 18:30 · 21:30 | its own SKILL.md (the master, now Agent Council) | **ACTIVE** | required |
| `opus-enriched-review-preus` | 16:20 (pre-US-open) | the master SKILL.md (sibling pointer) | **ACTIVE** | required |
| `opus-enriched-review-postclose` | 23:15 (post-close) | the master SKILL.md (sibling pointer) | **ACTIVE** | required |
| `enriched-review-cycle-6` | one-time 2026-05-31 06:25 | own (legacy one-shot) | **INACTIVE** | legacy — past one-time run; not required |
| `opus-decision-us-open` | — | own (header: "DISABLED 2026-06-01 — superseded by opus-enriched-review-4h") | **DISABLED** | legacy — superseded |
| `opus-decision-evening` | — | own (header: "DISABLED 2026-06-01 — superseded by opus-enriched-review-4h") | **DISABLED** | legacy — superseded |

## Coverage of the 6 market-aware slots
All six slots (04:30 / 11:30 / 16:20 / 18:30 / 21:30 / 23:15) are covered by the **3 active** routines. The Agent Council rewrite went into the **master** `opus-enriched-review-4h/SKILL.md`; the two sibling pointers run that same file, so all 3 active routines inherit the Agent Council format automatically — no per-sibling edit needed.

## Required vs legacy
- **Required & active:** the 3 enriched-review routines. Fully cover the schedule.
- **Legacy & inactive:** `enriched-review-cycle-6` (one-shot, expired), `opus-decision-us-open`, `opus-decision-evening` (both explicitly DISABLED 2026-06-01, superseded). **None required.**

## Action
- **No unpausing performed.** Per the task rules, paused/disabled routines are left as-is.
- The legacy `opus-decision-*` tasks are NOT needed (the 6×/day enriched-review schedule supersedes them). If the operator ever wants a separate US-open / evening *decision* run on top, it can be re-enabled — but it would also need the Agent Council block ported in. **TODO (operator-gated):** "If a US-open-specific or evening decision routine is desired again, unpause `opus-decision-us-open` / `opus-decision-evening` AND port the AGENT COUNCIL REVIEW MODE block into their SKILL.md — do not run them on the old format."

## Verdict
Active routines fully cover the market-aware schedule; legacy routines remain paused by design.
