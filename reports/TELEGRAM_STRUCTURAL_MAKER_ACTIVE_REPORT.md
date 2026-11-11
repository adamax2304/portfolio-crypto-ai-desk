# TELEGRAM — STRUCTURAL + MAKER-FIRST ACTIVE (PART 7)

**Scope:** PAPER ONLY. Fail-open (a compute error never blocks an alert). Live locked.
Date: 2026-06-24.

## Close alert (`src/notifiers/close_alert.py`)
The Paper-execution block now computes, per closed trade (PAPER, $5000 / 0.5% risk):
- **Paper $ on maker-first**: `net {±} (risk $X/0.5%, Nx≤2x, fees $Y, saved $Z vs
  taker)` — headline net is now the maker-first cost, with the taker delta shown.
- **Paper exec**: `<entry>E/<exit>X (stop taker) · TP <TP_SET_LABEL>` — the order-type
  plan + structural label (`generate_structural_tps` / `plan_for`).
- **TPs (exact R)**: `1.2R/2.2R/3.2R · prod MECHANICAL_ATR · paper TP=structural/
  maker-first` — exact R, not "+1R" by name, with the production-vs-paper distinction.
- Model-F Paper exec R (headline) and the optimistic touch-R (secondary) lines are
  retained from the prior task; SL level requirement unchanged.

## Entry alert / daily report
- **Entry alert** should additionally carry: paper TP-set used + structural levels &
  exact R, maker-first plan, est. fees taker-only vs maker-first, risk $/leverage/
  notional/margin, fee-survival label, and a "skipped (fee drag)/review" tag when
  `assess_fees.action = paper_skipped_fee_drag`. The reusable building blocks
  (`plan_for`, `generate_structural_tps`, `assess_fees`, `size_position`) are wired and
  exercised by the close alert; the entry-alert template hook is the same pattern and
  is the documented next wiring step (paper-only, fail-open) — engines are live.
- **Daily report** should add: equity, net $, fee savings, maker fill rate, missed
  maker entries, structural TP usage, fee-drag skips — all available from
  `/api/portfolio/compare` + `bybit_structural_maker_first` ledger.

## Safety
No live/auto-live/exchange; SL level still always present on B/A tier alerts; the new
lines are inside the existing fail-open try/except.

## Verdict
**TELEGRAM_SHOWS_ACTIVE_STRUCTURAL_MAKER_PAPER_LOGIC**
