# Catalyst Label Backfill (PART 9)

**Date:** 2026-06-15 · Derived table only. Core signal rows NOT mutated.

## Approach

Per the spec's preferred path, labels were backfilled into a **separate derived
table** `signal_catalyst_labels` — NOT by mutating `proposed_signals`.

```
signal_catalyst_labels(signal_id PK, catalyst_freshness, catalyst_strength,
    source_quality, symbol_mapping, derivatives_label, headline_short, computed_at)
```

## Result

- **1,016 rows** backfilled for A/B signals (last 30 days), via `compute_labels`.
- Freshness distribution: `none=970, recent(?)=46`.
- Derivatives distribution: `not-available(stocks)=753, OI-up=190, funding-supportive=43, no-squeeze=23, squeeze-risk=7`.

## Not changed (forbidden mutations avoided)

- score, tier, final_outcome, raw R, sized R, entry/stop/TP — all untouched.
- No historical trading decision rewritten.

The derived table is safe to drop + rebuild at any time from raw payloads.
Going forward, new signals also carry the live `news_supported` flag (PART 1)
and per-signal catalyst_meta, so labels stay current without backfill.
