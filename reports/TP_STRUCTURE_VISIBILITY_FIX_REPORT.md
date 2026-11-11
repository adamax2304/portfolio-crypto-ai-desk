# TP Structure Visibility Fix (PART 7)

**Date:** 2026-06-24. TP generation NOT changed (still mechanical ATR ladder; structural change requires separate approval).

## What the app/Telegram now show
- **TP Quality: MECHANICAL_ATR_LADDER** — `/api/trades/{id}/chart-events` returns `tp_quality {label, volume_profile_supported, note}`. App shows a `MECHANICAL_ATR` badge on the closed-trade detail; Telegram close alert appends `· MECHANICAL_ATR (not structural)`.
- **TP source** — production TPs are `close ± k·ATR` (ATR extension), explicitly not a swing/SR/volume-profile level. The note states this plainly.
- **Volume profile** — `volume_profile_supported = "unknown"` (no VP module). Shown as `VP unknown`, never "false" or "supported".
- **TP3 warning** — the standalone `tp_structure_validator` (display-only) flags an unjustified TP3 in chop/non-runner; this audit surfaces the mechanical-ladder label everywhere TPs appear.
- **Not misleading:** the app never describes a mechanical TP as a "chart level"; exact R is shown beside each TP (PART 4).

## Verdict
`TP_STRUCTURE_VISIBLE_AND_NOT_MISLEADING`
