# Crypto Expansion Watchlist — Follow-through Backtest (PART 7)

**Date:** 2026-06-10 23:32 UTC
**Scope:** All crypto proposed_signals (n=130).

## Cohort sizes

- C-tier (watchlist / expansion): **0**
- A/B-tier: **130**

## C-tier follow-through

- C-tier signals whose symbol later got A/B-promoted: **0** / 0 (0%)
- Of those, later A/B winners: **0**

## C-tier outcomes (paper PnL contribution)

- C-tier closed: 0
- C-tier sum R: **+0.00**
- C-tier wins / losses: 0 / 0
- C-tier WR closed: 0%

## Were direction calls correct? (paper PnL > 0 proxy)

- C-tier with final_r > 0 (direction correct + filled): **0** / 0

## Did blockers correctly prevent bad promotions?

- C-tier winners with NO later A/B promotion (missed): **0**

## Would cap 25 or 30 have helped?

- The full-agent cap is enforced upstream in the supervisor, not at signal-write time, so we cannot strictly answer this without re-running scanning.
- **Proxy:** if C-tier winners that did NOT later get A/B promotion are few (above), then the current cap is not leaving large alpha on the table.

## Decision (read-only)

- **No expansion-candidate promotion implemented.** Read-only check only.
- **No full-agent cap change implemented.**
- The current YAML weight for C-tier is **0.0×**, so even if expansion is noisy, it contributes zero to sized R. The audit is informational.