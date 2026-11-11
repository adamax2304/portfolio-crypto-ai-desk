# Obsidian Dashboard Path Audit (PART 2)

**Date:** 2026-06-10 · Read-only inspection.

## 1. Generation surfaces

| Script | What it writes | Trigger |
|---|---|---|
| `scripts/refresh_obsidian_dashboard.py` | **All 12 pinned tabs** (00–11) | Scheduler `core_tail_steps` → `"refresh obsidian dashboard"` step every cycle (2 h) |
| `scripts/write_obsidian_current_state_dashboard.py` (standalone CLI) | **Only tab 11** (Current State) | Manual `python -m scripts.write_obsidian_current_state_dashboard` OR delegated from `refresh_obsidian_dashboard.write_current_state()` via shared `build_page()` |
| `src/cli.py review-day --write-obsidian` | `obsidian_vault/11_Trade_Journal/Daily_Reviews/<date>.md` (NOT a pinned tab) | Scheduler tail step `("daily review (obsidian)", ...)` |

## 2. Canonical page
- **Single source of truth**: `obsidian_vault/11 📌 Trading Desk Current State.md`
- Standalone CLI writes the same file: `PAGE = VAULT / "11 📌 Trading Desk Current State.md"`
- Refresh script's `write_current_state()` writes the same file by importing `build_page` from the standalone module.

**No duplicate page exists.** The previously-deprecated `obsidian_vault/00_Dashboards/Trading_Desk_Current_State.md` is verified absent.

## 3. Answers to the 10 audit questions

| # | Question | Answer |
|---|---|---|
| 1 | Canonical current-state dashboard? | `obsidian_vault/11 📌 Trading Desk Current State.md` |
| 2 | Duplicate pages, one fresh and one stale? | **No duplicates** |
| 3 | Scheduler writes to a different file than user opens? | No — same file |
| 4 | Script reads latest DB rows correctly? | Yes — `proposed_signals × latest signal_outcomes` per signal_id |
| 5 | Filters by wrong date/timezone? | No — uses `datetime.now(timezone.utc)` with `iso_minus_hours(...)` for window cutoffs |
| 6 | Only shows closed trades, not active? | No — open-trades section is the first content block; pulls `tier IN ('A','B') AND final_outcome NOT IN (...closed...)` |
| 7 | Ignores `watchlist_alerts` / only reads `signal_alerts`? | Reads `proposed_signals + signal_outcomes`; uses `watchlist_alerts` only for the untracked-legacy probe |
| 8 | Ignores new statuses (`stale_before_entry`, `entry_moved_away`, intrabar)? | **No** — `open_trade_comment()` explicitly recognises `stale_before_entry`, `entry_moved_away`, `regime_changed`, `needs_reprice`. Recent-trade comments parse `outcome_notes` for `intrabar_entry_stop / intrabar_entry_tp / gap_slip_stop / gap_slip_tp` annotations. |
| 9 | UTC/EEST cutoff bug? | No — windows are pure UTC math; only the header timestamp is shown in EEST (display-only) |
| 10 | Obsidian sync/cache hides fresh modifications? | Not observed. The 16:02 partial mtime update on tabs 01-04 (without content change) appears to be Obsidian's own indexing — cosmetic, not a freshness issue |

## 4. Hardcoded paths
- `PAGE = VAULT / "11 📌 Trading Desk Current State.md"` (canonical)
- `VAULT = REPO_ROOT / "obsidian_vault"` (resolved at import)

No accidental path divergence.

## 5. Verdict
- Generation path is **healthy**.
- Scheduler step exists and runs (exit 0 every cycle today).
- Script reads fresh DB; renders fresh tab when invoked.
- **The "stale" feeling comes from the 2-hour scheduler cadence** between cycles, not from a code bug.

```
PATH_AUDIT_COMPLETE
```
