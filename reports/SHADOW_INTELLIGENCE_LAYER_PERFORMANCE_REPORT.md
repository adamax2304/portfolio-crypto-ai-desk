# Shadow Intelligence Layer — Performance Report (PART 9)

**Date:** 2026-06-18 · **Verdict:** within budget.

## Cached enrichment latency (alert path)
`assemble_intelligence_fields` over **100 sample signals** using local cached data:

| pctl | runtime |
|---|---|
| p50 | **47 ms** |
| p95 | **63 ms** |
| p99 | **78 ms** |
| max | 78 ms |

Targets: p95 < 100 ms ✅ · p99 / hard cap < 300 ms ✅.

## Performance discipline (verified)
- **No external network / LLM in the alert path** — asserted by a test that monkeypatches `socket.connect` to raise; the aggregator completes normally (`test_aggregator_no_network`).
- **Cache-only reads** — derivatives / squeeze / on-chain are read from `intelligence.sqlite` (single-symbol indexed lookups); the only compute in-path is the deterministic thesis (string templating).
- **Time budget** — the aggregator checks a monotonic budget between submodules and returns `intelligence_layer_status="timeout_partial"` rather than overrun.
- **Heavy compute is background** — timeline bootstrap, derivatives trajectory, squeeze phase, on-chain run in `scripts/intelligence_update.py` / `onchain_risk_update.py` (scheduler, non-fatal), not in the monitor/alert path.
- **Metrics emitted per signal:** `intelligence_runtime_ms`, `intelligence_cache_hit_ratio`, `intelligence_data_freshness_sec`, `intelligence_layer_status`.

## Telegram budget
`intelligence_telegram_lines` returns **≤3** compact lines; the SL/Stop line is never replaced (asserted in tests). Full detail lives in the payload / Control Plane / reports, not Telegram.

## Notes
- The 63ms p95 includes one small RO timeline query + 3 cache reads + the thesis; it does not load OHLCV (that happens in the background updater). Real-world per-signal cost in the live monitor is bounded by the same path.
