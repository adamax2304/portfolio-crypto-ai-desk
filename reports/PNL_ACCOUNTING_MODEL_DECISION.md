# PnL Accounting Model — Decision (PART 7)

**Date:** 2026-06-23. Which model should the desk *report* with.

## The practical reality (answers the philosophical questions)
1. **What did the system intend?** To track signal *quality* via the best TP reached — a research metric, not an executed-PnL metric.
2. **What does the operator think a trade means?** Likely "I'd act on the alert and exit somewhere" — i.e. a *single position*, which the touch model does not represent.
3. **If a Telegram alert says TP1, is the trade closed?** Undefined today. There is **no close instruction and no partial** — the alert just notes TP1 touched; the trade keeps being tracked to its best TP.
4. **Is there manual execution?** Not systematically — the desk is paper. There are **no real fills**.
5. **If there is no order execution, what should paper accounting represent?** The **most honest, reproducible proxy for what a disciplined operator would actually realize** — which is *not* "best TP touched without give-back."

## Options
| Option | Pros | Cons |
|---|---|---|
| **A — Keep legacy touch accounting** | consistent, simple, already there | optimistic; only valid if "touch TP = filled & closed at that TP"; must be labelled |
| **B — Switch paper to first-TP full close** | conservative, simple, no give-back illusion | discards TP2/TP3 information; caps winners (−105R here); throws away the multi-target design |
| **C — Switch paper to partial/runner model** | most realistic; supports dynamic stop | needs explicit split rules; is a *trade-logic* change (forbidden without approval); still relative-only on this data |
| **D — Keep legacy `final_r`, ADD `realistic_r` beside it** | no historical rewrite; both numbers visible; lets operator judge; reversible; display-only | two numbers to explain |

## Recommendation — **Option D**
Keep `signal_outcomes.final_r` exactly as-is (do **not** rewrite history, do **not** change the tracker), and **add a derived `realistic_r`** (default = first-TP-close or +0.5R-lock, configurable) **beside** it in the read-model / reports, with the label **"recorded = highest-TP-touched (optimistic); realistic = simulated single-position exit."**

Rationale: the touch number is a fine *signal-quality* metric and is already embedded everywhere; the problem is it being **silently presented as PnL**. Option D fixes the honesty gap without any trade-logic change, without destroying the TP2/TP3 research signal, and without committing to a partial model that this granularity can't yet validate. B/C are deferred until real execution is on the table; A alone is unacceptable because it's currently unlabelled.

## Verdict
`PNL_ACCOUNTING_MODEL_DECISION_READY` — **Option D: keep legacy `final_r` + add labelled `realistic_r` (display/read-model only).** No production trade-logic change.
