# Status Semantics Clarity Report (PART 6)

**Date:** 2026-06-19 · **Type:** display/semantics fix. **No trade logic / scoring / TP-SL / routing / outcomes changed.**

## Canonical display groups (new)
`OPEN_ACTIVE · WAITING_FOR_ENTRY · REVIEW_ONLY_SHADOW · ENTERED_UNRESOLVED_EXPIRED · NO_ENTRY_EXPIRED · CLOSED_WIN · CLOSED_LOSS · CLOSED_FLAT · UNKNOWN_INCONSISTENT`
Single source: `src/status/display_status.py` (`derive_display_status`). Mirror for the Control Plane: `trading-desk-control/backend/app/display_status.py`.

## Counts by display group (full history, 2077 signals)
| display_group | count | new report counter |
|---|---|---|
| NO_ENTRY_EXPIRED | 545 | `no_entry_expired_count` |
| ENTERED_UNRESOLVED_EXPIRED | 467 | `expired_after_entry_count` |
| CLOSED_LOSS | 484 | `closed_loss_count` |
| CLOSED_FLAT | 204 | `closed_flat_count` |
| CLOSED_WIN | 148 | `closed_win_count` |
| REVIEW_ONLY_SHADOW | 137 | `review_shadow_count` |
| OPEN_ACTIVE | 5 | `open_actionable_count` |
| WAITING_FOR_ENTRY | 0* | `waiting_for_entry_count` |
| UNKNOWN_INCONSISTENT | 87 | `unknown_inconsistent_count` |

\* waiting count is point-in-time; 0 in the full-history snapshot because waiting rows have since resolved. Source: `reports/DISPLAY_STATUS_BACKFILL_REPORT.md`.

**The headline fix:** the old single `expired` bucket (≈1012 rows) is now split into **467 entered-unresolved** (a trade was filled, no TP/SL before the window) vs **545 no-entry** (price never reached entry). These mean opposite things and were previously indistinguishable.

## Before / after examples
| Case | Before (confusing) | After (clear) |
|---|---|---|
| `expired`, entry_triggered=1, final_r=0 (ETH/USDT) | `expired` · `+0R` | `⌛ EXPIRED AFTER ENTRY — entered, no TP/SL within window (not a missed entry)` · R: `0R display / no TP-SL before expiry (unresolved, not a flat trade)` |
| `stale_before_entry`, entry_triggered=0 (SUI/USDT) | `expired` | `❌ NO ENTRY — price never reached the entry` · reason: `signal aged out waiting for entry (stale)` |
| `entry_moved_away`, entry_triggered=0 | `expired` | `❌ NO ENTRY` · reason: `price ran away from the entry zone before a fill` |
| C-tier stocks waiting | counted as a signal / "active?" | `👁 REVIEW/SHADOW — not actionable by policy` · NOT counted as open actionable |
| `stopped`, final_r=-1 | `stopped` `-1R` | `🔴 CLOSED LOSS -1.0R` |
| terminal close, final_r=0 | `+0R` (reads like profit/flat ambiguity) | `⚪ CLOSED FLAT 0R` |

## Top confusing cases fixed
1. **`expired` overloaded** → split entered-unresolved vs no-entry (the operator's #1 confusion).
2. **`+0R` ambiguity** → `format_r_with_lifecycle`: unresolved-expiry ≠ flat ≠ N/A.
3. **"no active trades"** → now "no open actionable, but X waiting / Y review/shadow / Z entered-unresolved".
4. **Review/shadow miscounted** → REVIEW_ONLY_SHADOW is a separate bucket, never "active actionable".

## Inconsistent rows
**87** rows map to `UNKNOWN_INCONSISTENT` (a no-entry status carrying `entry_triggered=1`, or `ambiguous`). Surfaced in `reports/DISPLAY_STATUS_BACKFILL_REPORT.md` for review — **the underlying rows are left exactly as-is** (no rewrite).

## How Telegram looks now (live sample, `scripts/paper_monitor_status.py`)
```
📊 Paper Monitor Status
Open actionable: 5
Waiting for entry: 0
Entered unresolved: 30
Review/Shadow: 137
No-entry/stale/moved-away: 41
Closed: 118W / 42L / 173flat
⚠️ Needs review (inconsistent): 4

Expired split:
  Expired after entry (entered, no TP/SL): 30
  No-entry / stale / moved-away: 41
```
Per-item lines now carry: symbol · direction · display label · entry touched (yes/no) · paper alerted (yes/no) · reason · lifecycle-aware R. Top-5 per bucket, "full details in report / Control Plane".

## New report counters available
`expired_after_entry_count · no_entry_expired_count · stale_before_entry_count (within no-entry) · entry_moved_away_count (within no-entry) · review_shadow_count · open_actionable_count · waiting_for_entry_count · closed_flat_count · unknown_inconsistent_count` — via `summarize_display_states()`.
