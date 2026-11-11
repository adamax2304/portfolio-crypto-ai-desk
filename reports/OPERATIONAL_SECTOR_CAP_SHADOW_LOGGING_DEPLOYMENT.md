# Operational Sector-Cap Shadow Logging — Deployment (PART 5)

**Date:** 2026-06-17 · **Verdict:** **SECTOR_CAP_WOULD_BIND_FORWARD_TRACKING_READY**

## Logging (live, per stocks-intraday A/B alert)
The paper-entry payload now carries (via the risk-guard assembler → `would_bind_sector_cap(store, signal)`):
`would_bind_sector_cap`, `would_sector_rank`, `would_sector_bucket`, `would_sector_reason`, `actual_concentration_status`, `diagnostic_only=true`.
The **live** concentration behavior is unchanged — the live per-signal cap remains the only thing that can affect an alert; the day-batch cap runs in shadow only. Cap value unchanged; no cap=3; no hard block.

## Forward tracker
`scripts/sector_cap_forward_tracker.py` reads the last 14d of stocks-intraday `paper_entry` payloads and reports: # would_bind vs # actual_bind, the distribution, and the net R of would-bound names (joined to outcomes).

### First run
`stocks-intraday paper_entry alerts (14d): 161 · would_bind=0 · actual_bind=0`.
This is expected: `would_bind_sector_cap` is written **only on new alerts** produced after this deploy, so historical payloads have no would-bind field yet. The tracker **starts accumulating now** and becomes meaningful after ≥10 trading days of new alerts.

## Decision gate (unchanged)
After ≥10 trading days: enable a batch-aware LIVE cap (still paper, with explicit approval) ONLY if would-bound names are net-negative AND the cap does not clip net-positive clusters. Until then: shadow-only.

## Tests
`tests/test_sector_cap_shadow.py` (6): 3 same-bucket → 3rd would-bind; actual routing unchanged; payload has actual-vs-would; cap value unchanged; existing concentration suite unregressed.

## Reports
`SECTOR_CAP_WOULD_BIND_FORWARD_TRACKER.md` (rolling).
