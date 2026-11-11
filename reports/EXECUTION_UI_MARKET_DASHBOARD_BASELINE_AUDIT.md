# EXECUTION UI + MARKET DASHBOARD — BASELINE AUDIT (PART 1)

**Date:** 2026-06-24. Grounded in live desk DB (`db/crypto_ai_desk.sqlite`). PAPER ONLY.

## 1. ETH/USDT SHORT "+3R but exit marker near TP1/TP2"
Example `sig_c6df604c56ba3036` (ETH/USDT short, 2026-06-24 13:38):
entry 1653.38, stop 1667.16 (risk 13.77), tp1 1636.86, tp2 1623.09, **tp3 1609.32**.
`signal_outcomes`: tp1_hit 15:30, tp2_hit 15:45, **tp3_hit 16:45**, MFE **4.95R**,
final_outcome **win**, final_r **3.0**. → **+3R is CORRECT** (genuine TP3 touch).

**Root cause of the misleading marker:**
1. **The trade is NOT in `paper_portfolio_ledger`** (both A and B rows = None) — it
   post-dates the last batch backfill. The ledger is rebuilt by a batch script, not
   live, so recent/active trades have no ledger row.
2. `chart_events` builds **one** "Exit" marker from the A-book ledger `exit_price`.
   When a ledger row exists, that price is the **Model-F blended exit** (e.g. BE/lock
   or a single TP), which sits near TP1/TP2 — while the headline shows the **touch +3R**
   (tp3). One exit marker at a Model-F price + a +3R header = the visual mismatch.
3. There is **no per-TP fill marker** today; TP markers come from `tp*_hit_at` but the
   single exit marker overrides the visual story.

**Fix path:** PART 3 (partial-exit lifecycle: TP1/TP2/TP3 fill markers at their real
prices), PART 5 (chart-events emits every fill, no single misleading exit), and make
the read-model derive lifecycle live (not only from the batch ledger).

## 2. MSTR SHORT "expired +0R · very late 184m — DO NOT CHASE"
Example `sig_f2fc71137a472dfc` (MSTR short, 2026-06-24 14:09):
created 14:09 → **entry triggered 14:15** (6 min later — entry was NOT late),
then **expired +0R**, MFE only **0.36R** (price chopped flat, never approached TP1).

**Root cause of "very late 184m — DO NOT CHASE":** `actionability.freshness()` computes
`age = now − entry_triggered_at`. At view time (~17:19) that age ≈ 184 min. `classify()`
returns `status:"closed"` for the terminal/expired trade **but still attaches the
freshness dict** with the "very late — DO NOT CHASE" label, which the UI renders. The
chase-guard is meant for *open* trades; showing it on an already-closed trade is
**misleading** — this is a display bug, **not** execution latency, **not** a missed
profitable trade (MFE 0.36R).

**Fix path:** PART 9 — suppress the chase-guard/freshness label on terminal trades;
show "expired · entry filled · chopped flat (+0R, MFE 0.36R)" instead. Add a
missed-opportunity journal for genuine missed/late-entry cases (entry never triggered +
favorable move after).

## 3. regime: unknown
`proposed_signals.market_regime` is **free-text** from the detector/LLM:
`bullish` (1235), `chop` (256), **`''` empty (223)**, `risk_off` (222),
`bullish trend` (215), `risk_on` (126), `bearish trend` (42), `range/chop` (33),
`transition` (15), `high-volatility danger` (3). The app shows **"unknown"** on the
empty string and on any value it can't map to its fixed enum. → most "unknown" are the
**223 empty-string rows** + unmapped free-text, not truly-missing data.

**Fix path:** PART 8 — a normalizer mapping free-text → canonical enum
(trend_up/trend_down/range/chop/transition/risk_off/unknown), with source + confidence;
"unknown" only when genuinely empty.

## 4. Execution-logic visibility gaps (confirmed)
- No partial exits / per-TP fills (single blended exit).
- No "active after TP1 / waiting TP2-TP3" state.
- No structural-stop-after-TP movement (Model F only does BE/lock).
- Exit/stop $ per TP not broken out.
- Leverage/margin/liquidation shown but no "why this leverage" / liq-distance.
- Recent trades missing from ledger (batch-only) → exit data absent live.

## 5. Market tab data sources (current)
No `market_dashboard_*` table or `/api/market-dashboard` endpoint exists. The Market
tab today is thin (no fear&greed, no risk-now, no curated news, no regime summary).
→ PART 10/11 build the data model + endpoint + Opus-routine writer.

## Verdict
**BASELINE_UI_EXECUTION_ISSUES_CONFIRMED**
- ETH +3R correct; marker misleading due to single Model-F exit + missing partials + stale ledger.
- MSTR not late/missed; chase-guard label leaked onto a closed/expired trade.
- regime "unknown" = empty/unmapped free-text, fixable by normalization.
- lifecycle/partials/structural-stop/market-dashboard absent → to build.
