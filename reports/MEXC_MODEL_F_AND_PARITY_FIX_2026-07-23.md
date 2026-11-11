# MEXC Model F And Parity Fix

## Scope

- The active Paper strategy, its ledger, `signal_outcomes`, and `final_r` are unchanged.
- No new live entry mode, symbol, leverage, or risk limit was enabled.
- Existing MEXC live orders continue to use the current whole-position runner: native stop + TP3, with Model F moving only the stop.

## Fixed

1. The MEXC monitor now writes an explicit heartbeat and each open position records its last successful reconciliation, last price observation, and monitor errors.
2. A monitor that starts while another leader is active remains as a standby.  It retries leadership after the lease expires instead of exiting permanently.
3. Model F stop moves and reconciliation failures are recorded as dedicated MEXC events.
4. Existing canary plans are imported into an isolated MEXC-parity ledger.  New preflight-valid MEXC plans are recorded there before any possible submission.

## Isolated MEXC Evidence

- `mexc_model_f_runner_v1`: the current live exit design.
- `mexc_partial_tp_33_33_34_v1`: shadow-only comparison; 33% TP1, 33% TP2, 34% TP3.
- Both use public MEXC one-minute candles and conservative handling of intra-minute stop/target ambiguity.
- They write only `mexc_canary_parity_*` tables.  They never create, modify, or close an exchange order.

## VIRTUAL Case

For the historic VIRTUAL MEXC entry, the isolated minute-path replay shows that the current Model F would have moved its stop and closed at a small estimated net profit around $0.70.  TP1 had not yet been reached at the first protective-stop exit, so the partial-TP profile is identical for this one observation.  This is a debugging confirmation, not enough evidence to change live exits.

## Promotion Rule

Keep partial TP shadow-only until there are at least 30 clean closed MEXC-parity observations and the profile improves net USD PnL, profit factor, and drawdown versus the current Model F runner on the same executed plans.
