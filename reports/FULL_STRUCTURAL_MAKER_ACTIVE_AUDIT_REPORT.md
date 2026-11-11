# FULL STRUCTURAL + MAKER-FIRST ACTIVE — AUDIT (PART 10)

**Date:** 2026-06-24. PAPER ONLY. All checks executed against the live desk DB.

## Audit checklist
| # | check | result |
|---|---|---|
| 1 | App values match backend | `/api/portfolio/compare` → A +3.72%/$1763, B +8.19%/$1585, Δ +4.47pp, fees saved $177.73, maker entries 177, maker exits 299 — matches backfill print. ✅ |
| 2 | Backend matches ledger | `portfolio_summary` / `portfolio_compare` read `paper_portfolio_ledger` rows directly per fee_profile. ✅ |
| 3 | Ledger matches formulas | net = R×actual_risk − (entry fee + exit-notional close fee + slippage); equity compounds. ✅ |
| 4 | Telegram matches ledger | close_alert recomputes the same maker-first cost + structural label + exact R (fail-open). ✅ |
| 5 | Maker fill assumptions conservative | maker entry only for pullback; maker TP only if rested; no free maker (gap-through). stop always taker. ✅ |
| 6 | Structural TP lines correct | forward path uses swing/range/VP; historical labelled STRUCTURAL_FALLBACK_ATR (no fake VP). ✅ |
| 7 | No fake VP | `volume_profile.supported=False` when no volume; not injected. ✅ |
| 8 | Max 2x applied | ledger max leverage = 2 for **both** A and B; sizing clamps ≤ 2. ✅ |
| 9 | No double counting | A=`bybit_non_vip_usdt_perp`, B=`bybit_structural_maker_first`; backend filters ONE profile; UNIQUE(key,event_type,fee_profile). ✅ |
| 10 | Old ledger not mixed with new profile | 5 profiles × 587 each; backend never sums across profiles. ✅ |
| 11 | final_r unchanged | `signal_outcomes` has `final_r`, no paper column; never written. ✅ |
| 12 | Live locked | `/api/health` → live_locked:true, auto_live_locked:true. ✅ |

## Bugs found & fixed during implementation
1. **`paper_portfolio_backfill` drop-list deleted the B book.** Re-running the A
   backfill DELETEd `bybit_structural_maker_first` (non-canonical). → drop-list now
   preserves it (`keep = profiles + ["bybit_structural_maker_first"]`); B re-persisted.
2. **B ledger UNIQUE collision.** B rows carried the active profile name in their dict
   so `replace_ledger` inserted under the wrong profile, colliding with A. → relabel
   deduped rows to the persist key before insert.
3. **Maker entry never fired** in the backfill — `load_trades` didn't carry
   `playbook`. → added `playbook`(setup_type)+`regime`; entry maker now fires for
   pullback/bounce cohorts (177 fills).
4. **Round-number TPs too coarse** (produced absurd far "structural" TP1). → gated
   round numbers on having chart candles + capped candidate distance at `max_tp_r`
   (15R); candle-less path degrades cleanly to ATR-fallback.
5. **`reason` NameError risk** in close_alert new block. → use `new_outcome`.
6. Broken JSX in trade-detail fees line. → simplified.

## Verdict
**FULL_STRUCTURAL_MAKER_ACTIVE_AUDIT_COMPLETE**
