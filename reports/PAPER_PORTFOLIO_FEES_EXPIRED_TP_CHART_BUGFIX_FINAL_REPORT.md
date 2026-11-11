# Paper Portfolio / Fees / Expired / TP-R / Chart Markers — Bugfix FINAL (PART 12)

**Date:** 2026-06-24. PAPER / ACCOUNTING / APP display only. No live, no production exit/TP-SL/scoring/entry/routing change, `final_r` not rewritten.
Supporting: PAPER_PORTFOLIO_BUGFIX_BASELINE_AUDIT · FEE_MODEL_AUDIT_AND_FIX_REPORT · EXPIRED_TRADE_HANDLING_FIX_REPORT · TP_R_MULTIPLE_DISPLAY_FIX_REPORT · LEVERAGE_AND_POSITION_VISIBILITY_FIX_REPORT · CHART_MARKERS_OVERLAY_FIX_REPORT · TP_STRUCTURE_VISIBILITY_FIX_REPORT · HISTORICAL_PORTFOLIO_REBUILD_AFTER_BUGFIX · APP_TELEGRAM_PORTFOLIO_DISPLAY_AUDIT_FIX_REPORT · PAPER_PORTFOLIO_BUGFIX_TEST_RESULTS.

## The 18 answers
1. **Were commissions wrong?** Yes — the **close fee was charged on the ENTRY notional**, not the exit notional (and there was no per-side rate, no source/estimated metadata).
2. **How are fees calculated now?** open = entry_notional × entry_rate; close = **exit_notional** × exit_rate; slippage per side; net = gross − fees − slippage − funding. Exit price implied from `paper_execution_r` (1R = |entry−stop|); `fee_estimated` only if exit unknown.
3. **Active fee profile?** `bybit_non_vip_usdt_perp` (taker 0.055%); also mexc/conservative/zero/custom_override, each with source + last_verified.
4. **Leverage visible now?** Yes — dashboard avg (1.95x) / max (5x) / risk-capped; per-trade leverage/margin/notional/risk in detail; Telegram Paper $ line.
5. **How are expired trades closed?** At the implied close price from `paper_execution_r` (protected level), `expiry_close_price_source="implied_from_paper_execution_r"`; `paper_execution_available=false` if unresolvable (never silent 0).
6. **Expired chart markers?** Yes — `expired_exit` marker with price + R + net $.
7. **TP R-multiples exact now?** Yes — e.g. TP1 1.2R / TP2 2.2R / TP3 3.2R (not "+1/2/3R"); shorts sign-flipped; in app + Telegram.
8. **TP levels still mechanical ATR ladder?** Yes — `close ± 1/2/3·ATR`, unchanged (generation change needs approval). Now clearly labelled MECHANICAL_ATR_LADDER, VP unknown.
9. **What changed in app?** Portfolio cards (equity/today $/maxDD/fees) + **Leverage + Open/Margin cards**; closed-trade detail gains a sizing/exit block, exact TP R, markers timeline, TP-quality badge.
10. **What changed in Telegram?** Close alert adds Paper $ (risk/leverage/fees/net) + exact TP R + MECHANICAL_ATR.
11. **Historical portfolio after corrected accounting?** $5000 → no-cost +47.45%, **Bybit +2.82% ($5141)**, MEXC +16.15%, conservative −5.76%. Backend headline ≈ $5136 / +2.72%.
12. **`final_r` unchanged?** Yes.
13. **Live/execution off?** Yes — `/api/health` live_locked:true, auto_live_locked:true; 0 live steps.
14. **TODO?** Full candlestick **line-overlay** on `Chart.tsx` (markers timeline + endpoint live now); a **volume-profile module** to make TPs structural (approval-gated); pulling **account-specific fee rates** into `custom_account_override`.
15. **Watch next?** Forward equity vs the +2.82% Bybit replay; fees-as-% of gross (~74%); risk-capped count; whether the edge survives real account fees; expired close-price sanity on live trades.

## Bugs found & fixed
(1) close fee on entry notional → exit notional; (2) `exit_price` NULL on all rows → populated (implied) + expiry close price/source; (3) "+1R" by name → exact R; (4) leverage not surfaced → dashboard + detail + Telegram; (5) no exit/expired chart marker → markers timeline; (6) TP quality not shown → MECHANICAL_ATR_LADDER everywhere; (7, found mid-fix) renamed fee profile orphaned old ledger rows → backend filters one active profile + backfill drops non-canonical; (8) `_to_float` NameError (prior) confirmed fixed.

## Final verdicts
`FEE_MODEL_AUDITED_AND_FIXED` · `EXPIRED_TRADES_CLOSE_WITH_MARK_PRICE_OR_EXPLICIT_UNAVAILABLE` · `TP_R_MULTIPLES_DISPLAY_EXACT` · `LEVERAGE_VISIBLE_IN_APP_AND_TELEGRAM` · `CHART_MARKERS_VISIBLE_FOR_ENTRY_EXIT_STOPS_TPS_EXPIRED` · `TP_STRUCTURE_VISIBLE_AND_NOT_MISLEADING` · `HISTORICAL_PORTFOLIO_REBUILT_WITH_CORRECTED_ACCOUNTING` · `NO_LIVE_EXECUTION_ENABLED` · `HISTORICAL_FINAL_R_UNCHANGED` · `READY_FOR_FORWARD_VALIDATION`
