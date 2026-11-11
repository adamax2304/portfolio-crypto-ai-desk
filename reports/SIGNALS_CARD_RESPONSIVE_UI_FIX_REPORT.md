# SIGNALS CARD RESPONSIVE UI FIX (PART 8)

**Date:** 2026-06-24. Frontend `components.tsx`. PAPER/UI.

## Root cause
`KV` rendered its value in a `<div>` with no overflow handling, inside a `grid-cols-3`
whose cells default to `min-width:auto` → long low-price strings
(`0.0846·0.083·0.0814`, entry ranges) overflowed the card on narrow widths.

## Fix
- **`KV`**: root `min-w-0` (lets the grid cell shrink) + value `break-words` + label
  `truncate` → generic overflow fix everywhere KV is used.
- New **`KVsm`**: compact 12px mono variant, `break-words leading-tight`, optional
  `col-span-2` for the full-width TP row.
- **SignalCard price row**: `grid-cols-3` → **`grid-cols-2`** (Entry, Stop on row 1; **TP1
  / TP2 / TP3 spanning the full width** on row 2 with " / " separators that give wrap
  points). Entry collapses to a single value when low==high. Badge row gets
  `overflow-hidden`.

Result: ENTRY range, STOP, TP1/2/3, and the Chart / Manual Entry buttons all stay inside
the card at desktop-narrow and mobile-ish widths; long symbols/decimals wrap instead of
overflowing. Frontend build clean (92 modules).

## Verdict
**SIGNALS_CARDS_NO_OVERFLOW**
