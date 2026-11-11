# Stocks-Intraday — Safe Restriction Plan (PART 8)

**Date:** 2026-06-17 · **No production change made.** Diagnostic + plan only.
**Verdict:** **STOCKS_INTRADAY_KEEP_WITH_FILTERS** — specifically, move **C-tier** stocks-intraday to shadow/review-only (with your approval); keep A/B actionable.

## Diagnostic (30d closed stocks-intraday, raw R)
`scripts/stocks_intraday_diagnostic.py` → `STOCKS_INTRADAY_REWORK_DIAGNOSTIC.md` + `STOCKS_INTRADAY_FILTER_COUNTERFACTUAL.csv`.

| Cut | n | net R |
|---|---|---|
| **All** | 447 | **+106.0** |
| C-tier | 206 | **−34.0** ← the drag |
| B-tier | 193 | **+132.0** ← carries the book |
| A-tier | 48 | +8.0 |
| catalyst-backed | 8 | −2.0 (too sparse to filter on) |
| no-catalyst | 439 | +108.0 |

### Filter counterfactuals (simulated, not applied)
| Filter | kept | net R |
|---|---|---|
| current (all) | 447 | +106.0 |
| **drop C-tier** | 241 | **+140.0** ✅ best |
| only catalyst-backed | 8 | −2.0 (kills the book) |
| only RTH session | 196 | +18.0 (hurts — premarket-created signals are net-positive here) |
| exclude legal-flag | 440 | +105.0 (legal cut is tiny: 7 trades) |
| A/B + catalyst + RTH | 1 | −1.0 (over-filters) |
| A/B + RTH, no legal | 137 | +24.0 (hurts) |

## Honest reconciliation with the "−12R recent audit"
Over **30d raw R the book is net +106R**, not −12R. The recent-audit −12R was a shorter / sized / deduped window during a choppy stretch. So stocks-intraday is **not broadly broken** — it has a **C-tier leak** (−34R) plus recent-regime weakness. The 30d signal is clear and actionable: **C-tier is the consistent loser; B-tier is the engine.**

## Answers to the PART-8 questions
- **Which tickers/sectors lose?** See the diagnostic's "worst 10 tickers" + by-bucket tables (CSV per-trade). The dominant axis is **tier (C)**, not a single sector.
- **C/B/premarket/no-catalyst/legal/follow-through?** Losses concentrate in **C-tier**. Premarket-created and no-catalyst are *net-positive* here (so not the problem). Legal-flag cut is negligible (7 trades).
- **Do RTH-confirmation filters help?** **No** on this data — RTH-only *reduces* net R (premarket-planned B-tier setups are net-positive). Do not require RTH confirmation.
- **Catalyst-backed + RTH remove losers without missing winners?** No — catalyst tagging is too sparse (8 trades) and over-filters to ~nothing.
- **Downgrade to review-only?** Not the whole mode — only **C-tier**.

## Recommended safe restriction (to apply later, with approval — NOT applied now)
1. **C-tier stocks-intraday → shadow/review-only** (highest-value, data-supported: +106R → +140R by removing the −34R C-tier leak). Keep A/B actionable.
2. **Do NOT** require catalyst-backed (too sparse) or RTH confirmation (counterproductive here).
3. Keep the **legal-overhang gate** as-is (already small).
4. Watch the recent-window weakness via the now-deployed **circuit breaker** (alert-only) + forward tracking; re-run this diagnostic in 2–4 weeks.

## Constraints honored
No production change in this stage. No scoring/TP/SL/threshold change. The C-tier→shadow move is a *recommendation* requiring your explicit approval before any wiring.
