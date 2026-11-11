# Pre-Implementation Baseline — Stocks Concentration Cap (PART 0)

**Date:** 2026-06-16 · Production DB: `db/crypto_ai_desk.sqlite` (read-only)

| Check | Result |
|-------|--------|
| `sector` / `narrative` populated? | **No** — 0/1938 rows. Sector/proxy must be inferred from a symbol map. |
| Main affected mode | **stocks intraday** (the only stocks mode that pushes actionable paper-entry alerts) |
| stocks swing/invest | paused / 0× (playbook weight) — overlay leaves them untouched |
| crypto scalp | 0× / shadow_only — unaffected |
| auto-trade path | none (`create_order/place_order/ccxt..Order` → empty) |

**Row-count + R baseline (latest outcome per signal):**
- `proposed_signals`: **1938** (crypto 339, stocks 1599)
- `signal_outcomes`: 123,583
- SUM final_r: crypto intraday +3 / scalp −12 / swing +20 · stocks intraday +100 / invest −45 / swing −29

These are the invariants verified unchanged in PART 8 (the overlay writes nothing to the DB;
`signal_outcomes` may grow only from the normally-running tracker, not from this change).

**PART 0 status: DONE.**
