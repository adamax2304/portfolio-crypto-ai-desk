# Opus Routine — Risk-Routing Prompt Update

**Date:** 2026-06-07 · Scope: Opus auto-enriched-review **prompts / SKILL.md
only**. No trading code, scoring, thresholds, stop/TP, strategy, or scheduler
touched. No restart. Advisory-only contract preserved.

## Goal
Make Opus reviews **market decision reviews, not signal summaries** — using
market mood as a **risk-routing layer** (which side/what confirmation), never as
a blanket "NO TRADE" filter, while the deterministic scanner keeps running in all
moods.

## Files changed (3 prompt files; zero code)
| File | Change |
|---|---|
| `~/.claude/scheduled-tasks/opus-enriched-review-4h/SKILL.md` (shared source of truth, 4 slots) | Added per-slot focus detail (PART 6); new **MARKET MOOD / RISK ROUTING + ALWAYS-SCAN** section (PART 2/3/9); required **Market Mood / Risk Routing** subsection in §6 render structure (PART 4); mood-aligned candidate decision logic in §J (PART 5); **Mood** block + watch-candidate fallback in the Telegram template (PART 8). |
| `~/.claude/scheduled-tasks/opus-enriched-review-preus/SKILL.md` (16:20 sibling) | Now also requires the mood/risk-routing block + always-scan rule; reaffirms slot focus. Still points to the shared SKILL.md. |
| `~/.claude/scheduled-tasks/opus-enriched-review-postclose/SKILL.md` (23:15 sibling) | Same sibling update. |

The shared `opus-enriched-review-4h/SKILL.md` remains the single source of truth;
the two siblings "Read and execute EXACTLY" that file at runtime, so the logic is
not duplicated.

## What was added (by PART)
- **PART 1 — permission contract preserved:** the PART 16 ADVISORY-ONLY /
  READ-MOSTLY contract (no code edits, no tests, no patches, no scheduler ops, no
  restarts, no auto-trade, no permission prompts, write only the 3 allowed
  artifacts, one Telegram ≤3500, bugs → §14 TODO only) is **unchanged and not
  weakened**.
- **PART 2 — Market Mood / Risk Routing layer:** risk-off→shorts/relative
  weakness; risk-on→RS-leader/catalyst longs; chop/danger→cleaner entries + still
  name best long & short + triggers; mixed→split crypto/stocks/sectors/narratives,
  no one broad no-trade. Must identify best long / short / catalyst-backed /
  avoid each run; if none clean, give the failing side, missing confirmation,
  exact trigger, and re-check time. "No clean trade" = this window only, never a
  stop command.
- **PART 3 — Always-Scan rule:** scanner / candidate generation / tracking /
  outcomes continue in all moods; Opus may advise caution but must NEVER
  recommend disabling the scanner, data collection, monitors, or scheduler.
- **PART 4 — required §6 subsection:** "Market Mood / Risk Routing" block
  (Crypto mood / Stocks mood / Dominant narrative / Preferred side / Best long /
  Best short / Best catalyst-backed / What to avoid / What would change the view)
  is mandatory every run; advisory only, never modifies scoring/strategy.
- **PART 5 — candidate decision logic:** §J now weighs mood, BTC/ETH regime,
  breadth, funding/OI/crowding, catalyst, chase-risk, overextension, squeeze-prone
  shorts, RS-leader vs weak-bounce longs, stock actionable-vs-planning, and
  legal/earnings risk — plus the 6 per-candidate questions (aligned-with-mood?
  long/short/wait? actionable-now-or-after-confirmation? what invalidates?
  chase-risk? catalyst confirm/contradict?).
- **PART 6 — slot focus detail:** all **6** slots (04:30, 11:30, 16:20, 18:30,
  21:30, 23:15) have explicit focus bullets in the shared SKILL.md.
- **PART 7 — 3 task prompts updated:** each states its slot, reads/executes the
  shared SKILL.md, preserves advisory-only, requires the Market Mood block, and
  keeps the slot name in the Telegram header.
- **PART 8 — Telegram template:** adds a compact 3-line **Mood** block
  (Crypto / Stocks / Prefer); keeps ≤3500; the no-clean-trade fallback now lists
  long-watch / short-watch / catalyst-watch + triggers instead of a bare
  "no-trade"; never emits "stop the system".
- **PART 9 — anti-over-conservatism guardrails:** explicit "do not default to
  no-trade"; route by mood; always list watch candidates + exact triggers when no
  clean trade.

## PART 10 — Validation (all ✅)
| Check | Result |
|---|---|
| Permission contract still present (not weakened) | ✅ `PERMISSION CONTRACT (PART 16` + ADVISORY-ONLY/READ-MOSTLY intact |
| Market Mood / Risk Routing layer exists | ✅ |
| Required §6 Market Mood subsection | ✅ |
| Always-Scan rule exists | ✅ |
| Anti-"NO TRADE" rule exists | ✅ |
| All 6 slot types present | ✅ (04:30 / 11:30 / 16:20 / 18:30 / 21:30 / 23:15) |
| All 3 tasks point to shared SKILL.md | ✅ (siblings reference it; main is the source) |
| Telegram template includes mood/routing line | ✅ (`Prefer: longs/shorts/catalyst-backed/wait-for-trigger`) |
| ≤3500-char reminder retained | ✅ |
| No code / scoring / strategy files changed | ✅ only the 3 `.md` prompt files edited |
| Scheduler restart | ✅ not needed — prompts are file-based, read at each fire; tasks still enabled with paths unchanged (next runs scheduled) |

## Deployment
Live immediately for the next scheduled slot — the runtime reads each task's
SKILL.md at fire time (siblings explicitly read the shared file). No task
re-creation, no scheduler/collector restart. Disabled legacy tasks
(`opus-decision-us-open`, `opus-decision-evening`, `enriched-review-cycle-6`)
left untouched.

## Final
```
OPUS_ROUTINE_PROMPTS_UPDATED
```
