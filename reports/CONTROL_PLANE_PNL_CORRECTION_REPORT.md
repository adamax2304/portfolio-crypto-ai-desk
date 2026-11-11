# Control Plane PnL Correction (PART 5)

**Date:** 2026-06-24. Backend read-model + frontend display. READ-ONLY (no DB writes). Health stays `live_locked:true`.

## Backend (`backend/app/books.py`, `desk_adapter.py`)
- New `paper_execution_r(sig)` — Model F (early_mfe_protection_v1), computed from the fields already on each signal (`mfe_r`, `tp3_hit`, `stop_hit`, `final_r`/touch, outcome class). Mirrors the desk-side module; pinned by tests. Returns None for open/waiting (no realized paper PnL yet) and **None (not 0) when `mfe_r` is missing → surfaced as a fallback warning, never silently zeroed**.
- `touch_r(sig)` = the old `final_r` (kept, labelled optimistic).
- `paper_exec_flags(sig)` — per-trade `protection_armed`, `lock_armed`, `stop_moved`, `giveback`, `original_stop_avoided`, `paper_execution_available`, `highest_tp_touched`.
- `_summ` now reports per window/book: `paper_execution_r` (main), `touch_r`, `touch_minus_paper_r`, `giveback_n`, `be_scratch_n`, `protected_n`, `original_stops_avoided_n`, `paper_unavailable_n`.
- Headline: **`today_paper_execution_r` is the main number** (+ `h48`/`d7`); `today_touch_r` secondary; `today_operator_r` back-compat alias now points at the paper number. Label explains Touch R is optimistic/signal-quality.
- `desk_adapter` exposes `tp2_hit`/`tp3_hit`; each trade row enriched with `touch_r`, `paper_execution_r`, `risk_model`, protection flags.

**Live verification (after backend restart):** `/api/dashboard/summary` headline →
`today_paper_execution_r −1.0 · h48 +20.0 · d7 +21.5 · risk_model early_mfe_protection_v1 · h48_touch_r +18.0 · today_paper_unavailable_n 0`. `/api/health` → `live_locked:true, auto_live_locked:true`.

## Frontend (`frontend/src/screens.tsx`, `types.ts`)
- Headline card **"Today R · Paper Exec" (Model F)** = `paper_execution_r`; new **"Recorded Touch R"** card labelled "highest TP touched · optimistic · signal-quality".
- "48h R · Paper Exec" with W/L + BE-scratch count; protection row "48h Protected · N stops→BE/lock · giveback".
- Note line: risk model + paper-vs-touch + ⚠ fallback warning when `paper_unavailable_n > 0`.
- Closed-trade row leads with paper R (touch shown faint when differing) + `giveback→protected` / `lock +0.5R` / `BE armed` badges.
- Closed-trade detail: KVs `Paper Exec R`, `Touch R (opt.)`, `Risk model`; a **"Paper execution (Model F)"** block — *"Old accounting counted the highest TP touched (X); new paper execution applies early MFE-armed protection and closes at the protected stop (Y)"* — plus protection steps in the timeline (BE @ +0.6R, lock @ +1R, reversed → protected stop).
- **Frontend `npm run build` (tsc -b + vite) passes clean.**

## Verdicts
`APP_USES_PAPER_EXECUTION_R` · `TOUCH_R_LABELLED_AS_OPTIMISTIC`
