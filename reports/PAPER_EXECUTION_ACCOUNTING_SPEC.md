# Paper Execution Accounting — Spec (PART 2)

**Date:** 2026-06-24. Module: `src/execution/paper_execution_accounting.py`. PAPER/ACCOUNTING ONLY.

## New quantities (legacy `final_r` kept, no longer the headline PnL)
| field | meaning |
|---|---|
| `touch_r` | = old `signal_outcomes.final_r` (highest TP touched). Label: **"touch-based / signal-quality, optimistic — not real PnL."** |
| `paper_execution_r` | **authoritative paper PnL** for future + recalculated trades. Default model `early_mfe_protection_v1`. |
| `realistic_r` | derived comparison models (`first_tp_close`, `hold_tp3`) for historical context; never overwrites `final_r`. |
| `risk_model` | `legacy_touch` \| `first_tp_close` \| `early_mfe_protection_v1` (default). |

## Model `early_mfe_protection_v1` (Model F) — exact rules
Inputs from the recorded path: TP/stop touches, `mfe_r` (peak favorable R), R-ladder (R of each TP via `r_multiple`). Thresholds: arm BE at **+0.6R** favorable, lock **+0.5R** at **+1.0R** favorable, runner to TP3.

```
R1,R2,R3 = r_multiple(entry,stop,TPk,direction)          # long: (TP-entry)/|entry-stop|; short sign-flipped
m0 (touch) = R3 if tp3 else R2 if tp2 else R1 if tp1 else (-1 if stop else 0)
if not entered or not resolved:        paper_execution_r = None      # open/waiting
elif tp3 reached:                      = R3                 reason=tp3_runner
elif mfe >= 1.0:  stop→+0.5R lock      = +0.5 if (stop or expired) else m0   reason=profit_lock_stop / tp_win
elif mfe >= 0.6:  stop→breakeven       = 0.0  if (stop or expired) else m0   reason=breakeven_stop / tp_win
else:                                  = -1.0 if stop else 0.0  reason=original_stop / expired_flat
```
- **Long/short:** handled by `r_multiple` sign-flip; thresholds are in R so identical for both.
- **Candle-path assumption:** a stopped trade whose `mfe_r ≥ 0.6R` must have traded back through entry, so the BE exit at 0R is path-valid; only same-candle bars are optimistic.
- **Same-candle ambiguity:** conservative stop-first (inherited from tracker). If MFE never cleared +0.6R, a stop is the full −1R. Flagged via `same_candle_ambiguous`.
- **Expired-after-entry:** resolved at the protected level (0R, or +0.5R if lock armed) — never left "unresolved win".

## Output fields (per trade → `paper_execution_outcomes`)
`risk_model, touch_r, paper_execution_r, paper_execution_outcome` (win/loss/breakeven/expired/open/no_entry), `close_reason, stop_initial, stop_current_r, protection_armed, protection_level_r, lock_armed, lock_level_r, highest_tp_touched, first_event, close_event, giveback, same_candle_ambiguous, computed_at, version`.

## Verdict
`PAPER_EXECUTION_ACCOUNTING_DEFINED`
