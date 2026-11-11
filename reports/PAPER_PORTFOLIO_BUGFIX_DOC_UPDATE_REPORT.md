# Paper Portfolio Bugfix — Doc Update Report (PART 11)

**Date:** 2026-06-24. Docs only.

## Updated
- `PROJECT_STATE.md` — Last Updated + bugfix callout (fees/expired/TP-R/leverage/chart, verdicts, links).
- `docs/DECISION_LOG.md` — new Active row (bugfix pass; exit-notional fee; expired close; exact TP R; leverage; markers).
- `docs/CURRENT_TESTING_AND_WAITING_STATE.md` — new bugfix section (what's fixed + TODO/watch).
- `docs/WEEKLY_FORWARD_METRICS.md` — existing paper-portfolio watch block remains the forward checklist (fees-as-% of gross, equity vs replay).
- `trading-desk-control/README.md` — paper portfolio note updated (leverage visible, exit/expired markers, exact TP R, MECHANICAL_ATR, exit-notional fees).

## Docs now state
- fees are configurable + account-specific (per-side, exit-notional close fee, source/last_verified, custom_account_override);
- expired policy (close at implied price; `expiry_close_price` + source; never silent 0);
- exact TP R (not "+1R");
- leverage visibility (dashboard + detail + Telegram; leverage ≠ risk);
- chart markers status (markers timeline + endpoint; full overlay = TODO);
- TP mechanical finding remains (MECHANICAL_ATR_LADDER, VP unknown);
- live locked; `final_r` never rewritten.

Docs validator: `PROJECT STATE DOCS: OK`.

## Verdict
`DOCS_UPDATED_FOR_PORTFOLIO_BUGFIX`
