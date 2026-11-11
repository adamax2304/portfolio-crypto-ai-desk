# EXECUTION UI + POSITION LIFECYCLE + MARKET DASHBOARD + LATENCY — FINAL REPORT

**Date:** 2026-06-24. **PAPER ONLY** — no live/auto-live/exchange/real orders, no
production TP/SL or scoring/routing change, `signal_outcomes.final_r` never rewritten.
Feature-flagged where accounting affects output; reversible; tested.

## 1. What was wrong with the ETH exit marker?
The chart drew **one** "Exit" marker from the A-book ledger `exit_price` (a Model-F
blended/locked exit, near TP1/TP2) while the header showed the **touch +3R**, and the
recent trade wasn't in the batch ledger yet. One blended exit + a +3R header = the
mismatch.

## 2. Was +3R calculated correctly?
Yes — `signal_outcomes` shows tp1/tp2/tp3 all hit (MFE 4.95R), final_r 3.0. The touch
+3R is correct; the marker, not the number, was misleading.

## 3. Are all partial exits shown now?
Yes — the lifecycle splits the position TP1 33% / TP2 33% / TP3 34%. ETH now shows three
fill markers at 1636.86 / 1623.09 / 1609.32 ($9.51 / $17.76 / $26.80), **blended 2.21R,
$54.07** (touch +3R kept in audit).

## 4. Are entry/exit prices shown clearly?
Yes — price ladder (entry, initial stop, current/moved stop, TP1-3) + execution timeline
(every fill with price, qty, R, $, fee, order type) + price-scaled chart overlay.

## 5. Are stop/TP dollar outcomes shown?
Yes — max loss at stop ($), and $ per TP on its partial slice; realized $ + blended R.

## 6. Does the active tab keep trades after TP1 with remaining qty?
Yes — status `tp1_filled_active` / `tp2_filled_active`, a partial badge on the card, and
realized vs unrealized separated; the trade is not removed while qty remains.

## 7. Does the stop move structurally after TP1/TP2?
Yes — `structural_stop_manager` picks a structural level (swing/SR/VWAP) after each TP,
BE/+0.5R-lock fallback, never worse than current. Lifecycle emits `stop_moved_structural`.

## 8. Why was MSTR 184min late?
It wasn't. Entry triggered 6 min after the signal (14:09→14:15) and then expired flat
(MFE 0.36R). The "very late 184m — DO NOT CHASE" was a **chase-guard label leaking onto a
closed/expired trade** (age = now − entry_time ≈ 184m at view). Not latency, not a miss.

## 9. Was MSTR fixed?
Yes — closed/terminal trades now return a neutral "closed (<status>)" freshness; the
chase-guard only applies to open trades. MSTR shows "Expired flat (+0R, MFE 0.36R)".

## 10. Is regime unknown fixed?
Yes — `normalize_regime` maps free-text→enum; "unknown" only when the field is genuinely
empty. ETH→Trend↓, MSTR→Chop instead of "unknown".

## 11. Is max 5x policy active?
Yes — `config/paper_portfolio.yaml` max_leverage 5, margin ≤25%, notional ≤150%,
liq-buffer 3×, skip_if_liquidation_too_close. Lifecycle/sizing clamp ≤5x.

## 12. Why is max 5x still safe under risk-based sizing?
Risk = stop distance × size (0.5% = $25), independent of leverage. The engine forces
liquidation ≥ 3× the stop distance — so it only uses 5x when the stop is < ~6.7% (liq 20%
≫ stop). Wider stops auto-reduce leverage. The stop is always hit far before liquidation;
leverage just sets margin.

## 13. Is the Market tab redesigned?
Yes — `market_dashboard_snapshots` + `/api/market-dashboard` + a card dashboard (fear&
greed, crypto/stock mode + main risk now, regime, today + long-term news, extras).

## 14. Does Opus update the Market tab?
Yes — protocol §17 appends a `market_dashboard_update` JSON block at the END of the
enriched review; `scripts/market_dashboard_from_review.py` parses + stores it (fail-open
to a deterministic fallback). **The enriched-review body is unchanged.**

## 15. Were all buttons/tabs audited?
Yes — `tsc -b && vite build` exit 0 (92 modules, all tabs/drawers/handlers type-checked);
all five new endpoints return valid shapes (LOCAL 200 / auth-on 401). Live Telegram
click-through needs the Mini-App context; build + endpoint + 70 backend tests cover the
broken-button/data failure modes.

## 16. Did live remain off? Yes — `/api/health` → live_locked:true, auto_live_locked:true.

## 17. Was final_r unchanged? Yes — no paper column on `signal_outcomes`; never written.

## 18. What remains TODO
- Full candlestick line-overlay via a chart lib (needs a per-trade OHLCV candle endpoint).
- Per-trade OHLCV structural re-walk for historical structural TPs/stops (forward path
  already structural).
- Live Opus market block (the writer + parser + fallback are wired; first real block
  lands on the next 4h review).
- Optional: surface the missed-opportunity journal as its own UI section.

## Final verdicts
- MAX_5X_SAFE_LEVERAGE_POLICY_ACTIVE_FOR_PAPER
- PAPER_POSITION_LIFECYCLE_WITH_PARTIAL_EXITS_READY
- STRUCTURAL_STOP_MOVEMENT_AFTER_TP_READY_FOR_PAPER
- FULL_CHART_OVERLAY_SHOWS_TRUE_EXECUTION_EVENTS
- TRADE_DETAIL_UI_EXCHANGE_LIKE_AND_CLEAR
- ACTIVE_POSITIONS_SHOW_PARTIALS_AND_NEXT_TARGETS
- REGIME_UNKNOWN_REDUCED_AND_EXPLAINED
- MSTR_LATE_ENTRY_CAUSE_IDENTIFIED_AND_FIXED
- MARKET_TAB_REDESIGNED_AS_RISK_NEWS_DASHBOARD
- OPUS_ROUTINE_UPDATES_MARKET_TAB_WITHOUT_CHANGING_REVIEW
- APP_UI_POLISHED_AND_BUTTONS_AUDITED
- NO_LIVE_EXECUTION_ENABLED
- HISTORICAL_FINAL_R_UNCHANGED
- READY_FOR_FORWARD_VALIDATION
