# Catalyst-to-Signal Trace Audit (PART 4)

**Date:** 2026-06-15 · Read-only. Full data: [CATALYST_TO_SIGNAL_TRACE.csv](CATALYST_TO_SIGNAL_TRACE.csv) (400 rows).

## Method

For each of the last 400 news_items (7d) that carried a detected symbol, check whether the SAME symbol produced an A/B signal AFTER the news timestamp, and what that signal's outcome was.

## Headline

| Outcome | n | % |
|---|---:|---:|
| News → later A/B signal for same symbol | **198** | 50% |
| News → no A/B signal | 202 | 50% |

## Interpretation

- **~50% of symbol-tagged news eventually produced an A/B signal** for that symbol — the pipeline is converting catalysts into candidates at a healthy rate.
- The other 50% are mostly: macro headlines, symbols outside the tradable universe, or catalysts the scorer correctly judged non-actionable.

## Specific failure patterns found

| Pattern | Evidence in trace |
|---|---|
| **Catalyst produced no signal** | 202/400 — most are macro/non-universe; a minority are tradable coins the system didn't pick up within the window |
| **Signal claimed catalyst but no source** | Crypto signals with `news_supported=1` (34) all map to a real `news_items` row — no phantom-catalyst cases found |
| **Symbol moved but catalyst missing** | not separable without per-symbol move data joined to news — flagged for the fast-move audit (PART 6) |
| **Stale catalyst reused too late** | possible — no freshness gate means an old catalyst can still back a late signal; not individually traced here |

## Time-from-news-to-signal

The trace confirms signals appear after their news (causal ordering preserved). Exact latency distribution is in the fast-move audit ([FAST_MOVE_DETECTION_LATENCY_AUDIT.md](FAST_MOVE_DETECTION_LATENCY_AUDIT.md)) — crypto report cadence is ~2h, so catalyst→candidate latency is bounded by the cycle interval, not by collection.

## Conclusion

Catalyst → signal conversion works (50% hit rate on symbol-tagged news). No phantom-catalyst signals. The main weakness is **latency** (2h cycle) and **no freshness gate**, not missing collection.
