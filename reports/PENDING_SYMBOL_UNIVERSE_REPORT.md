# Pending-Symbol Universe (PART 2)

**Date:** 2026-06-16 · `src/signals/pending_symbol_universe.py`

`select_pending_tracking_symbols(store, now=None, asset_class="crypto", tiers=("A","B"),
include_scalp=True, limit=None)` → distinct pending/triggered A/B symbols (metadata dicts:
symbol, norm, mode, tier, status, created_at). `pending_symbols(...)` → just the symbol
strings. Read-only; never raises (returns `[]` on store error).

**Scope:**
- asset_class = crypto (parameterized); tier A/B only.
- status ∈ {generated, waiting_for_entry, triggered, tp1_hit, tp2_hit} (non-terminal).
- excludes C-tier, rejected, expired, stopped, closed/terminal.
- includes **discovery alts** with active/pending A/B signals (the coverage-gap symbols).
- scalp included by default (keeps shadow research tracking fresh) but **deprioritized**
  (refreshed last, dropped first under a cap) and `include_scalp=False` drops it; scalp is
  never pushed (routing handles that).
- symbols normalized (upper/trim) and de-duplicated.

**Priority order:** non-scalp before scalp; within that, most-recent `created_at` first —
so a per-tick cap always keeps the freshest actionable candidates.

**Live:** returns 26 distinct pending A/B crypto symbols currently (RIF, HMSTR, GPS, ZEC,
ZRO, WLD, PUMP, SUI, TAO, NEAR, BABY, MEME, …).

Tests: `test_1..6` in `tests/test_option_b_pending_symbol_refresh.py` (includes alt,
excludes C-tier, excludes terminal, distinct+metadata, scalp toggle/deprioritization,
store-error fail-safe). **PART 2 status: DONE.**
