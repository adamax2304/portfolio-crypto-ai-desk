# STRUCTURAL TP + MAKER-FIRST + FEE-AWARE + SAFE 2X — FINAL REPORT

**Date:** 2026-06-24. **Scope: PAPER ONLY** — no live, no auto-live, no exchange
execution, no real orders, no production TP/SL or exit change, `signal_outcomes.final_r`
never rewritten. All features feature-flagged + reversible.

## 1. What changed?
Implemented four paper engines + integration + app/Telegram + A/B backfill:
- **Safe max-2x leverage** (`config/paper_portfolio.yaml`, `position_sizing.py`).
- **Structural TP** (`market_structure_levels.py`, `volume_profile.py`,
  `structural_tp_engine.py`).
- **Fee-aware execution** (`fee_aware_execution.py`).
- **Maker-first** (`maker_first_execution.py`).
- Policy `config/paper_execution_policy.yaml`; integrated backfill
  `scripts/structural_maker_backfill.py` → B book `bybit_structural_maker_first`.
- App: `/api/portfolio/compare`, dashboard A/B card, per-trade `paper_execution_b`.
- Telegram: close alert shows maker-first net (+ saved vs taker), order-type plan,
  structural label, exact TP R.

## 2. Is structural TP active for paper? **Yes** — `STRUCTURAL_TP_ACTIVE_FOR_PAPER_ONLY`.
Forward paper trades (live candles) get swing/range/round/VP levels; the historical
backfill labels `STRUCTURAL_FALLBACK_ATR` (no per-trade OHLCV slice — no fake structure).

## 3. Is maker-first active for paper? **Yes** — `MAKER_FIRST_EXECUTION_ACTIVE_FOR_PAPER`.
177 maker entries + 299 maker TP exits on the backfill; stops always taker; conservative
fills (no free maker).

## 4. Is max 2x active? **Yes** — `MAX_2X_SAFE_LEVERAGE_POLICY_ACTIVE_FOR_PAPER`.
Ledger max leverage = 2 for both books; tight stops cap notional + `risk_capped`.

## 5. Why max 2x does NOT mean "stop at 50%"
Leverage ≠ risk. Risk = `stop_distance × position_size`; a 2% stop risks the same $25
at 1x or 2x. 2x liquidation is ~50% away — but the **technical stop (0.5–8%) is hit
first by 6–100×**, so liquidation is never the exit. Max 2x only caps margin/notional
and removes a fake leverage edge.

## 6. What happened to the old mechanical TP?
Retained as the comparison baseline: book A = `bybit_non_vip_usdt_perp`
(`portfolio_result_mechanical_taker`); book B =
`portfolio_result_structural_maker_first`. Production still generates mechanical ATR TPs
unchanged.

## 7. Did production TP generation change? **No.** Mechanical ATR ladder in
`technical_setup_agent.py` is untouched; structural TPs are paper-only proposals.

## 8. Did live/execution remain off? **Yes** — `/api/health` → `live_locked:true,
auto_live_locked:true`. `NO_LIVE_EXECUTION_ENABLED`.

## 9. Did final_r remain unchanged? **Yes** — `signal_outcomes` has `final_r`, no paper
column added; never written. `HISTORICAL_FINAL_R_UNCHANGED`.

## 10. How much did fees improve?
Bybit fees **$1763 → $1585 (−$177.7, −10.1%)** via maker-first; MEXC $1240 → $1125;
conservative $2098 → $1892.

## 11. How much did equity improve? ($5000, 587 trades)
| profile | A ret% | B ret% | Δpp |
|---|---|---|---|
| Bybit non-VIP | +3.72% | **+8.19%** | +4.47 |
| MEXC default | +17.12% | +19.98% | +2.86 |
| conservative taker | −4.91% | −0.73% | +4.18 |
| zero (no-cost) | +48.59% | +48.59% | 0 |

## 12. How many maker orders missed? **0** in the backfill (conservative fill model
assumes the limit was touched again; forward path will record real misses).

## 13. How many trades skipped due to fee drag? **2** (conservative profile,
EXTREME_FEE_DRAG); **0** on Bybit/MEXC.

## 14. Which playbooks benefit?
Pullback/retest/bounce/swing cohorts gain maker-entry fees (177 fills). All cohorts gain
maker-TP fees on winners. Trend-runner/failed-bounce/catalyst keep TP3; chop loses TP3.

## 15. What does the app show now?
Dashboard A/B card (return/equity/fees per book + Δpp, fees saved, maker entries/exits,
structural vs ATR-fallback). Trade detail: `paper_execution_b` (TP-set label,
entry/exit/stop order types, leverage, B net vs A net), plus exact TP R,
MECHANICAL_ATR_LADDER label, leverage/margin/notional/risk, chart markers. Banner:
"production TP unchanged · paper TP = structural/maker-first · leverage max_2x_safe".

## 16. What does Telegram show now?
Close alert: `Paper $: net … (risk $/0.5%, Nx≤2x, fees $, saved $ vs taker)` ·
`Paper exec: <e>E/<x>X (stop taker) · TP <LABEL>` · `TPs (exact R): … · prod
MECHANICAL_ATR · paper TP=structural/maker-first`. Entry-alert + daily-report blocks are
the documented next wiring (same live engines).

## 17. Bugs found/fixed
(1) A-rebuild drop-list deleted the B book → preserve it; (2) B ledger UNIQUE collision
(wrong profile label) → relabel before insert; (3) maker entry never fired (no
`playbook` in loader) → added; (4) coarse round-number TPs → gate on candles + cap at
15R; (5) `reason` NameError in close_alert → `new_outcome`; (6) broken trade-detail JSX
→ simplified.

## 18. What is still blocked / TODO
- **Live / auto-live / exchange execution** — locked (unchanged).
- **Production structural TP** — would need a separate approval (paper proves it first).
- **Per-trade OHLCV structural re-walk** for the historical backfill (forward path
  already structural).
- **Full candlestick line-overlay** on the chart (markers + structural labels live).
- **`custom_account_override`** real fee rate — fill from the operator's account.
- **Conservative-profile economics still negative** — only Bybit/MEXC maker-first clear
  costs.

## Final verdicts
- STRUCTURAL_TP_ACTIVE_FOR_PAPER_ONLY
- MAKER_FIRST_EXECUTION_ACTIVE_FOR_PAPER
- FEE_AWARE_EXECUTION_ACTIVE_FOR_PAPER
- MAX_2X_SAFE_LEVERAGE_POLICY_ACTIVE_FOR_PAPER
- PAPER_EXECUTION_USES_STRUCTURAL_TP_AND_MAKER_FIRST
- APP_SHOWS_ACTIVE_STRUCTURAL_TP_AND_MAKER_FIRST
- NO_LIVE_EXECUTION_ENABLED
- HISTORICAL_FINAL_R_UNCHANGED
- READY_FOR_FORWARD_VALIDATION
