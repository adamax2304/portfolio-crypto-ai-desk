# Stocks Sector-Cap Counterfactual Audit (PART 6)

**Date:** 2026-06-17 · read-only · CSV: `STOCK_SECTOR_CAP_COUNTERFACTUAL.csv`.

## The cap as built
`src/signals/portfolio_caps.py` (+ `config/stock_risk_clusters.yaml`, `src/stocks/risk_clusters.py`), wired in `paper_entry.py`, **stocks intraday A/B only**:
- **Rule A — proxy collapse:** redundant proxies (QQQ/XLK/XLY → one group; SPY/DIA/IWM; same-symbol dups) → 2nd+ become `shadow_proxy_duplicate` (0×).
- **Rule B — per `risk_bucket`+direction rank:** 1st → 1.0×, 2nd → 0.5×, **3rd+ → 0× `shadow_sector_cap`**. `_RANK_WEIGHT = {1:1.0, 2:0.5}`. So effectively "**max 2 actionable per cluster/day/direction**."

## The decisive measurement
- **`concentration_status` was set on ZERO paper-entries in the last 7 days** (`not_applicable`/`None` only). The cap **shadowed nothing live.**
- Re-grouping the 173 stocks-intraday signals by (day, direction, risk cluster): **18 of 92 cluster groups had >2 signals** (where a hard cap-2 *would* shadow a 3rd), **0 had >3**, max occupancy = 3.
- **0 stock-intraday entries on 06-17** (today) — the day the user noticed "almost no stock trades."

## Reads
1. **The cap is NOT what's choking stock trades.** It bound 0× live; today's emptiness is not cap-driven. Low stock activity today is far more likely **few signals generated / pipeline timing / market**, not concentration shadowing. (Stocks intraday over-generated 20–36 entries/day on 06-11…06-16, then 0 on 06-17 — a generation/scheduling pattern, not a cap.)
2. **Latent gap:** the theoretical cap would bind in 18 cluster-days, but live it bound 0×. This strongly suggests the cap **only evaluates cross-signal context in batch report runs and is effectively inert on the per-signal monitor/paper-entry path** (each signal arrives alone, so "2nd/3rd in bucket" never computes). Worth a code check — but it means the cap is currently *neither helping nor hurting*.
3. Because it's non-binding, **"max 2 too strict?" is moot on this data** — there's nothing to soften yet. The prior `SHADOW_FIRST` decision (label-only, validate forward) stands.

## Variant evaluation (conceptual, since 0 live bindings)
| variant | assessment on this data |
|---|---|
| A. cap=2 hard | non-binding (18 would-bind groups, but never fired live) |
| B. cap=3 hard | binds even less (0 groups >3) — no practical difference |
| C. soft (1.0/0.5/0.25) | **preferred IF/when enforced** — avoids hard-blocking a good 3rd name |
| D. rank-based (keep best 2 by score/catalyst/freshness, 3rd if different sub-theme) | **best design** — but premature to wire while non-binding |
| E. per risk-bucket (semis vs broad vs QQQ) | already the design; fine |
| F. override if catalyst-backed / low-corr / better-RR / existing at BE | sensible future rule |

## Verdict
**Do NOT change the cap now.** It is currently non-binding and is **not** the cause of low stock activity. Two cautious follow-ups (after forward validation, not now): (1) **verify whether the cap actually runs on the live monitor path** (suspected inert) and fix if it's a silent no-op; (2) **if it is ever hard-enforced, make it soft/rank-based (C/D), not a hard block.** Not `SECTOR_CAP_TOO_STRICT` on this evidence — it's `SECTOR_CAP_NON_BINDING_VERIFY_WIRING`.
