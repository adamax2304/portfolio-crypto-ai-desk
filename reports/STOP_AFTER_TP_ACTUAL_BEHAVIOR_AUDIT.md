# Current TP/SL & Stop-Management — Actual Behavior Audit (PART 1 + 3)

**Date:** 2026-06-23. Read-only code+DB audit. **Nothing changed.**

## How TP/SL actually works (from `src/signals/tracker.py`)
- TP1/TP2/TP3 + invalidation(stop) are produced by the trade-idea agent and stored on `proposed_signals`. The tracker walks OHLCV candles (`_evaluate_signal_walk`) after entry and records `tp1_hit/tp2_hit/tp3_hit/stop_hit` + their timestamps + MFE/MAE.
- **`final_r` = R of the HIGHEST TP level the price ever touched** (`_classify`): tp3→r_tp3, else tp2→r_tp2, else tp1→r_tp1, else stop→−1R, else expired→0R. The stop only decides the outcome when **no** TP was touched.
- **The stop is the fixed `invalidation` for the entire walk — it is NEVER moved.** No break-even, no profit-lock, no trailing anywhere in the production tracker.
- **No partial close.** One `final_r` per trade. `tp1_hit=1` means "price touched the TP1 level," NOT "a partial was taken." There is no "remaining position" concept.
- Same-candle stop+TP → **conservative**: stop taken first, flagged `ambiguous` → −1R (`config/signal_tracking.yaml: ambiguous_same_candle: conservative`).
- `src/exits/shadow_exit_manager.py` (BE/partial/trailing variants A_current..I_one_reentry) is **shadow/measurement only** — not imported by the tracker or `run_default_market_schedule.py`. Confirmed via grep: zero production wiring.

## Plain-language answers
- **Does the stop move after TP1/TP2 today?** → **NO.** The stop is fixed at the original invalidation for the whole trade. No BE, no profit-lock, no trailing in production.
- **Does TP1 close the whole paper trade or part?** → Neither a partial nor a hard close. The model is **"book the R of the best TP the price touched."** A trade that touches TP1 and later reverses to the original stop is recorded as a **+TP1 WIN** (not a loss) — the model is **optimistic**.
- **Are TP2/TP3 actually used, or theoretical?** → They are **real levels the walker checks**; whichever is the highest one touched sets `final_r`. But because the model banks the best-touched TP, "holding for TP3" is **not** actually simulated — the recorded outcome already assumes you captured the best level reached.
- **BE/partial/trailing — production or shadow?** → **Shadow only.** Default-off, not wired.
- **Adaptive TP count by regime/mode?** → **No.** The number of TP levels is whatever the idea agent emits (≈3); the tracker is uniform across crypto/stocks/intraday/swing/scalp. Mode only changes the OHLCV timeframe (5m crypto-intraday/scalp, 15m stocks, etc.).

## Critical consequence for this audit
Because production accounting is **best-TP-touched (optimistic)**, the recorded `final_r` already gives full credit for TP3 on trades that reached it, and full TP1/TP2 credit even on trades that later reversed. Therefore:
- "Removing TP3 / 2-TP default" can only **clip** recorded winners — it never converts a recorded winner into a loss.
- The operator's "give-back" worry (winner → stop) is only realized under a **stricter hold-to-target** model, which the production tracker does **not** use. The counterfactual (PART 5/6) computes both views so the difference is explicit.

## Verdicts
`CURRENT_TP_BEHAVIOR_MAPPED` · `STOP_MOVE_AFTER_TP_VERIFIED = FALSE (stop never moves; no BE/trailing/partial in production; shadow-only)` · `STOP_MANAGEMENT_ACTUAL_BEHAVIOR_CONFIRMED`
