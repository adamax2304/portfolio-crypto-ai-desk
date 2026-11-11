# R / Sign Display Fix Report (PART 1)

**Date:** 2026-06-19 · **Type:** display formatting fix. **No trade logic / scoring / TP-SL / outcomes changed.**

## Bug
`reports/PAPER_MONITOR_STATUS_LATEST.md` showed `✅ CLOSED WIN +-1.0R`.

## Root cause (two faults)
1. **Classification not sign-aware:** `derive_display_status` routed to `CLOSED_WIN` whenever `final_outcome=="win"` (or `status=="tp3_hit"`) *regardless of the sign of `final_r`*. A row labelled `win` but carrying `final_r=-1.0` (a tracking artifact) became `CLOSED_WIN` with a negative R.
2. **Manual sign prefix:** the label used `f" +{final_r:.1f}R"`, so a negative R rendered as `+-1.0R`.

## Fix (`src/status/display_status.py` + Control-Plane mirror `backend/app/display_status.py`)
- Terminal close is now classified by the **sign of `final_r`** when present:
  - `final_r > 0` → `CLOSED_WIN`; `final_r < 0` → `CLOSED_LOSS`; `final_r == 0` → `CLOSED_FLAT`.
  - if the win/loss **label contradicts the sign** (`win`+`final_r<0`, or `loss`+`final_r>0`) → **`UNKNOWN_INCONSISTENT`** (surfaced, never mislabeled).
  - `final_r` absent → fall back to outcome/status (`tp3_hit`/`win`→win, `stopped`/`loss`→loss).
- Sign-correct formatting via `:+.1f` (`+1.0R` / `-1.0R`), so **`+-` can never appear**.

## New display formats
| state | display |
|---|---|
| win | `✅ CLOSED WIN +1.0R` |
| loss | `🔴 CLOSED LOSS -1.0R` |
| flat | `⚪ CLOSED FLAT 0R` |
| unresolved expiry | `0R display / no TP-SL before expiry (unresolved, not a flat trade)` |
| no-entry / waiting / review | `N/A …` |

## Tests added (`tests/test_display_status.py`)
- `final_outcome=win + final_r=-1` → not `CLOSED_WIN` (→ `UNKNOWN_INCONSISTENT`).
- `final_outcome=loss + final_r=+1` → not `CLOSED_LOSS`.
- label exactness: `✅ CLOSED WIN +1.0R`, `🔴 CLOSED LOSS -1.0R`.
- no `+-` substring in `format_paper_monitor_status` output.
- **19 display tests pass.**

## Verification on live data
Regenerated `PAPER_MONITOR_STATUS_LATEST.md` — **no `+-` anywhere**; closed losses render as `🔴 CLOSED LOSS -1.0R`.

## Verdict
**R_DISPLAY_SIGN_FIXED**
