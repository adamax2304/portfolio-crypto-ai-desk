# Intraday Carryover / Next-Day Revalidation — Would-Expire Audit (PART 5)

**Date:** 2026-06-17 · **Mode:** alert/label only. **No force-close, no flatten, no expiry enforced.**
**CSV:** `INTRADAY_REVALIDATION_WOULD_EXPIRE_AUDIT.csv` (per triggered intraday trade).
**Verdict:** **LABEL_AND_REVALIDATE, DO_NOT_FORCE_CLOSE.**

## What was measured
For each triggered intraday trade: held_hours, overnight_carried, result_R, and two diagnostic flags — `would_expire_crypto_intraday_12h` (crypto intraday open >12h) and `carryover_requires_review`/`next_day_revalidation_required` (carried across a day boundary).

## Findings (7d)
| Metric | Value |
|---|---|
| Crypto intraday trades open >12h | **8** |
| Realized R on those 8 (as-traded) | **+10.0R** (net positive) |
| Stocks intraday carried overnight | **84** |
| (Prior audit context) intraday expired @0R | 155 |

## Key nuance — do NOT blanket-expire
The crypto intraday trades that overran the 12h intraday horizon were **net +10R** as actually traded. A hard "expire at 12h → flatten" rule would have *destroyed* positive R. This mirrors the prior overnight-carryover finding (carry was net +17R). So the correct intervention is **revalidation + relabel**, not force-close:

- Crypto intraday open >12h → **flag for revalidation** (is the thesis still intact on current 1h structure?) and **relabel intraday→carryover/swing with reduced risk**, rather than silently holding *or* dumping.
- Stocks intraday carried overnight (84) → **RTH-aware next-session revalidation**: at next open, re-check the setup; keep/relabel/reduce — never auto-flatten in this stage.

## Recommendation (alert/label only)
1. Ensure `--revalidate-pending` / the revalidator path actually runs on the monitor tick (verify, don't change logic).
2. Add a **diagnostic** `lifecycle_label` ∈ {`fresh`,`aging_intraday`,`carryover_needs_review`,`overnight_relabel_candidate`} to alerts/dashboard. Pure label — no lifecycle action.
3. Surface `held_hours` + `carryover_requires_review` in Telegram/Control Plane (PART 7).
4. **Do NOT** add max-trade-age enforcement, EOD flatten, or any force-close in this stage — the data shows carry is net-positive; enforcement risks cutting winners. Revisit only with a path-aware study + your approval.
