# Catalyst Quality Score — Diagnostic (PART 7)

**Date:** 2026-06-15 · Read-only diagnostic. **No production scoring change.**

This defines a read-only quality rubric for catalyst integration. It is a measurement lens, not a scorer.

## Rubric

| Dimension | Levels | Current data availability |
|---|---|---|
| **catalyst_freshness** | fresh ≤1h / recent ≤6h / old >6h / none | ✅ derivable from `published_at` vs signal `created_at` (freshness_hours exists in catalyst events) |
| **catalyst_strength** | strong / medium / weak / none | ✅ `importance_score` (classifier) → strong ≥7, medium 4-7, weak <4 |
| **source_quality** | official / reputable news / social / unknown | ✅ `classify_source_quality` (exchange announcement=official, CoinDesk/Reuters=reputable, t.me=social) |
| **symbol_mapping_confidence** | exact / inferred / ambiguous / missing | ✅ exact = `detected_symbols_json`; inferred = EntityAliasMatcher fallback; missing = none |
| **derivatives_confirmation** | OI up / funding supportive / squeeze risk / missing | ✅ from `oi_context`/`funding_context` string (100% present for crypto) |

## Current state per dimension (crypto A/B, qualitative)

| Dimension | Observed |
|---|---|
| freshness | mixed — **no gate**, so old (>6h) catalysts still back signals. ~21% of signals have any catalyst flag. |
| strength | importance_score IS used (baseline 0.3 + importance/10), so strong catalysts score higher |
| source_quality | classified but **not surfaced** to the operator or Telegram |
| symbol_mapping | exact for `detected_symbols_json`, inferred via aliases; 17% of news carry a symbol |
| derivatives_confirmation | 100% present (latest-cache), feeds alignment penalty |

## How to operationalize (diagnostic only)

A per-signal catalyst-quality stamp could be computed at report time and shown in dashboard/journal:
```
catalyst: recent(3h) · strength: medium(imp=5) · source: reputable(CoinDesk) · map: exact · deriv: OI-up
```
This is **display-only** — it does not alter tier/score. Proposed as an additive label in the fix plan.

## Conclusion

All five dimensions are **computable from existing data** today. The gaps are **presentation** (source_quality and freshness not shown) and **freshness enforcement** (no gate) — not collection. No scoring change made.
