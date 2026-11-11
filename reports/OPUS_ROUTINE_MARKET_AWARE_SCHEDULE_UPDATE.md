# Opus Auto-Review — Market-Aware Schedule Update

**Date:** 2026-06-04 · Advisory-only routine reschedule. No trading-logic /
scoring / threshold / strategy change; the review remains read-mostly advisory.

## What changed
Old: `opus-enriched-review-4h` fired evenly every 4h — `30 0,4,8,12,16,20 * * *`
(00:30 / 04:30 / 08:30 / 12:30 / 16:30 / 20:30 EEST).

New: a **market-aware** 6×/day schedule (EEST/UTC+3):
| EEST | slot type | task |
|---|---|---|
| 04:30 | crypto overnight / Asia review | opus-enriched-review-4h |
| 11:30 | Europe / pre-US context | opus-enriched-review-4h |
| 16:20 | pre-US-open decision review (~10 min before open) | opus-enriched-review-**preus** |
| 18:30 | US open reaction review | opus-enriched-review-4h |
| 21:30 | late-session risk review | opus-enriched-review-4h |
| 23:15 | post-close final daily review | opus-enriched-review-**postclose** |

### Why three tasks instead of one
The 6 requested times use **three different minutes** (:30, :20, :15). A single
5-field cron expression cannot vary the minute per hour, so the schedule is
realised across:
- `opus-enriched-review-4h` — the four **:30** slots: `30 4,11,18,21 * * *`
- `opus-enriched-review-preus` — `20 16 * * *`
- `opus-enriched-review-postclose` — `15 23 * * *`

The two siblings **execute the same SKILL.md** (single source of truth) with
their slot label, so behaviour / permission contract / outputs are identical.

## Slot awareness (added to SKILL.md)
A new **SLOT AWARENESS** section maps the local hour → slot type + focus; the
review now states its slot in the title (`# Opus Enriched Review — <SLOT> —
Auto Cycle <HH:MM EEST>`) and the Telegram header (`[AUTO-REVIEW <SLOT> HH:MM
EEST]`). The "every 4 hours" wording was replaced with market-aware-slot wording.

## Verification (PART 3)
| # | Check | Result |
|---|---|---|
| 1 | Task name preserved / documented | ✅ `opus-enriched-review-4h` kept; 2 siblings documented |
| 2 | Tasks enabled | ✅ all three `enabled: true` |
| 3 | New times correct (EEST) | ✅ 04:30/11:30/18:30/21:30 + 16:20 + 23:15 |
| 4 | nextRunAt correct | ✅ 4h→`2026-06-04T15:38:50Z` (18:38 EEST) · preus→`13:23:07Z` (16:23 EEST) · postclose→`20:23:22Z` (23:23 EEST) |
| 5 | Advisory-only preserved | ✅ PART 16 permission contract intact (no edits/tests/scheduler-ops/auto-trade) |
| 6 | WebSearch/WebFetch fallback | ✅ §G/§N retained ("External web research unavailable" fallback) |
| 7 | Source discipline | ✅ §N final checklist + §13 Sources retained |
| 8 | Catalyst coverage check | ✅ §H retained (mapped/unmapped, >50% warning) |
| 9 | Compares with previous review | ✅ §K retained (§4 diff) |
| 10 | Telegram compact (≤3500) | ✅ §O retained, now slot-tagged header |

Note: dispatch jitter shifts fire times a few minutes (e.g. preus nextRun 16:23
= 16:20 + ~3 min jitter); still before the 16:30 US open. Jitter is inherent to
the scheduler and not configurable per task.

## Old tasks
`opus-decision-us-open` / `opus-decision-evening` remain **disabled** (superseded);
`enriched-review-cycle-6` one-time, disabled. Left as-is.

## Final
```
OPUS ROUTINE UPDATED — market-aware 6×/day, advisory-only
```
