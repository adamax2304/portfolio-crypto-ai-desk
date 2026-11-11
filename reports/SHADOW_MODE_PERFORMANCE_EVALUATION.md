# Shadow Mode Performance Evaluation (PART 4)

**Date:** 2026-06-19 · Window ~26.5h · **actionable closed sample = 5 (1W/4L, −3R)**.

> Overarching finding: with **5** closed actionable decisions, no per-feature win-rate / PF / counterfactual is statistically meaningful. Coverage and operational safety can still be assessed; **predictive value cannot**. Per the brief, small sample ⇒ `NEED_MORE_DATA` regardless of how good a feature looks.

## A. Shadow Intelligence Layer
- **Coverage:** good — 69 squeeze/deriv cached, 661 timeline events; labels available pre-decision (cached). Derivatives mostly "unknown" (no funding/OI history) → sparse.
- **Predictive value:** **uncomputable** — only 5 outcomes; e.g. only ~3 crypto intraday closes carry a squeeze phase. Win-rate-by-phase = noise.
- **Counterfactual (as a gate):** not evaluable. **Stability:** crypto-only meaningfully (derivatives sparse for stocks). **Op safety:** alert path is cache-only, p95 ~63–78ms, fail-open, no network. → **predictive NEED_MORE_DATA; operationally healthy as display.**

## B. Risk / guard layers
- **Circuit breaker:** fired ~0 times (calm window, `would_pause=False`). Counterfactual: 0 losers avoided / 0 winners killed → **no evidence either way**. **Sector/concentration caps:** sparse "would-bind" fires → not evaluable. **Risk-guard fields / lifecycle labels:** display/advisory, no decision effect. → **NEED_MORE_DATA as blocks; safe as display.**

## C. Execution / lifecycle
- **expired/no-entry split, entered-unresolved, close-alert lifecycle R, paper-monitor Status:** these are **mechanical display/UX** correctness fixes (validated by `test_display_status` + `test_telegram_standardization`, 0 `+-`, expired split present). Coverage 100% (every row gets a display group). **Predictive value:** N/A — they describe, they don't predict. **Op safety:** display-only, dedup-safe (close alert dedup is by signal_id+alert_type). → **already PROMOTE_NOW (LIVE).**
- **pending-entry revalidation:** tracking correctness; already in the tracker; not a promotable decision-gate.

## D. Profit protection / exits
- **shadow exits / BE / partial / trailing / path-aware replay:** evidence is the prior **146-trade hindsight replay** — pessimistic vs the real book and **net-losing across the tested window**; all signals are **post_factum** (computed after close). Cannot be promoted to anything that touches trades. → **KEEP_SHADOW (HIGH risk if enabled).**

## E. Playbook / sizing
- **Playbook performance labels / sizing weight:** report/label-only; the window's 5 closes are too few (and 3/5 were "pullback"/"breakout"/"breakdown" singletons). Earlier dedup stats exist but are not forward evidence. → display/report fine; **sizing-as-real = NEED_MORE_DATA.**
- **crypto scalp / C-tier / stocks swing-invest:** locked paper-policy (already shadow/paused on prior multi-week evidence) — not part of this promotion.

## F. Catalyst / narrative
- **catalyst integrity:** `ok`, regression signature none — working as an alert-only monitor. **Mapping/analyst/no-catalyst labels:** advisory/display, coverage good, no decision effect. → safe as display/advisory (already live); not a trade gate.

## G. Agent Council reason_codes
- **Just shipped (advisory).** **0 reviews produced on the new format yet** → no reason_code-vs-outcome data. Coverage will be 100% once reviews run. → advisory LIVE; predictive evaluation deferred to Friday.

## Cross-cutting
- **Stability:** nothing has a stable, repeated, multi-symbol, before-decision edge in this window. The one win (AVAX short) and four losses (mostly long breakouts/pullbacks) echo the earlier "pullback/long-in-weak-tape" note — but n=5 proves nothing.
- **Operational safety:** all shadow modules are fail-open, cache/label-only, no external paid API, covered by tests.
