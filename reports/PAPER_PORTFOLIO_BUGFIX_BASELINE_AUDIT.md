# Paper Portfolio Bugfix — Baseline Audit (PART 1)

**Date:** 2026-06-24. Pre-fix state.

| check | state at baseline |
|---|---|
| `paper_execution_r` active | yes |
| `paper_portfolio_ledger` exists | yes (586 rows, single profile) |
| app uses Paper Execution R headline | yes |
| touch_r labelled optimistic | yes |
| live_locked / auto_live_locked | true / true |
| `final_r` unchanged | yes (no paper col on signal_outcomes) |
| current fee profile | bybit_default_futures (taker) |
| `/api/portfolio/trades` has leverage/margin/notional/risk | in ledger yes, NOT shown in frontend rows |
| `/api/trades/{id}/chart-events` exit markers | NO exit/expired marker; `exit_price` NULL for all rows |

**Bugs confirmed:** (1) close fee used ENTRY notional, not exit; (2) `exit_price = None` for every ledger row → no expiry close price / exit marker; (3) TP shown by name "+1R" though exact R differs (e.g. 1.2/2.2/3.2R); (4) leverage not surfaced in app UI; (5) chart overlay TODO; (6) TP structural quality not surfaced; (7) touch vs paper — headline already paper (OK).

## Verdict
`PAPER_PORTFOLIO_BUGFIX_BASELINE_COMPLETE`
