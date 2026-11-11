# Paper Portfolio Risk — Doc Update Report (PART 13)

**Date:** 2026-06-24. Docs only.

## Updated
- `PROJECT_STATE.md` — Last Updated + callout (deposit/risk/sizing/leverage/fees, TP mechanical finding, fee-fragility, verdicts, links).
- `docs/DECISION_LOG.md` — new Active row (paper portfolio + sizing + leverage + fees + TP validator; backfill results; no live/exec/rewrite).
- `docs/CURRENT_TESTING_AND_WAITING_STATE.md` — new "Paper portfolio" update section (active features + key finding + watch + blocked).
- `docs/WEEKLY_FORWARD_METRICS.md` — new "Paper portfolio" forward-watch block (equity, fees-as-% of gross, risk-capped count, maxDD, TP quality).
- `trading-desk-control/README.md` — paper portfolio note (deposit/risk/sizing/leverage/fees, endpoints, fee-fragility, locks).

## Docs now state
- paper deposit = **$5000 USDT**; risk per trade = **0.5%** of equity;
- paper PnL = **net USD after fees/slippage** (from `paper_execution_r`);
- Model F active for paper accounting only;
- **TP levels are validated for structural quality (found mechanical ATR ladder)**;
- Touch R is **not** PnL;
- **live/execution still locked**; `final_r` never rewritten;
- what to watch next (forward equity vs +2.9% Bybit replay, fee survival, drawdown, TP quality).

Docs validator: `PROJECT STATE DOCS: OK`.

## Verdict
`DOCS_UPDATED_FOR_PORTFOLIO_RISK`
