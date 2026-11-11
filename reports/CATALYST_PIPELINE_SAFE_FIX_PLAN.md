# Catalyst Pipeline — Safe Fix Plan (PART 11)

**Date:** 2026-06-15 · Nothing implemented in this pass. Ranked by EV / risk.

## Allowed (safe, additive) — recommended order

| # | Fix | Type | Effort | Risk | Why |
|---|---|---|---|---|---|
| 1 | **Set stocks `news_supported` flag** from the scorer's existing news_payload | label-only (writes a flag already in schema) | ~1h | low | Unlocks catalyst-vs-not measurement for stocks (currently impossible); 0 stocks signals labelled today |
| 2 | **Funding/OI snapshot archive** — new `funding_snapshots` / `oi_snapshots` tables, 1 row/symbol/cycle | archive-only | ~3h | low | Enables historical replay + funding-cost modelling; no read-path change |
| 3 | **Catalyst quality labels in dashboard + journal** — freshness / strength / source / mapping / deriv (PART 7 rubric) | dashboard-only | ~2h | none | Operator sees catalyst quality; all 5 dims already computable |
| 4 | **Catalyst context block in Telegram** (3 lines: Catalyst / Funding-OI / Move type) | label-only (changes message) | ~2h | low | Needs operator approval (message content change). Per PART 8. |
| 5 | **Fast-move latency report** — join top-gainer candles to first-signal time | report-only | ~3h | none | Quantifies detection latency that today's data can't (PART 6) |
| 6 | **Surface analyst actions + source_quality in packet** | packet-only | ~1h | none | Already classified, just unused (failure mode #6, #7) |
| 7 | **Per-catalyst age tag in packet** high-conf list | packet-only | ~1h | none | Stops Opus over-weighting stale catalysts (failure mode #10) |

## NOT allowed without separate approval

| Change | Why blocked |
|---|---|
| Catalyst **freshness gate** in scorer (reject/downgrade >6h catalysts) | scoring change — needs its own study + approval; could suppress valid late-developing catalysts |
| Any threshold / TP/SL / routing / sizing change | out of scope |
| Promoting catalyst-backed signals to A/B automatically | promotion — forbidden |
| Unpausing stocks swing/invest | forbidden |
| Weakening any filter (e.g. relaxing the >2 ATR chase reject) | forbidden; chase-rejection is net-protective |

## Recommended first action

**Fix #1 (stocks `news_supported` label) + Fix #2 (derivatives archive)** — both low-risk, both additive, both unlock measurement that is currently impossible. They require no scoring change and can be done + tested in one safe pass when the operator approves.

## Highest-EV insight to act on (no code needed)

Crypto catalyst-backed signals trade **+15R vs −3R** for technical-only. The operator can already use this **today** in manual shadow: prioritise mirroring crypto signals that carry a catalyst, deprioritise pure-technical longs. No system change required to benefit.
