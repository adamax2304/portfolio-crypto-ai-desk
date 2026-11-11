# Shadow modes audit - 2026-07-13

## Scope and conclusion

This audit covers the paper-shadow execution lane, entry-mode calibration, sequential gate,
stocks-intraday candidate lane, stocks position framework, coverage/latency labeling, and the
default scheduler wiring. Live, auto-live, manual-live, `proposed_signals`, `signal_outcomes`, and
`final_r` were not changed by the fixes in this pass.

The shadow machinery is now structurally safe for continued collection. It is **not** yet a basis
for promoting a new mode: the eligible forward calibration report currently has zero eligible B
slices and the sequential gate has zero valid paired forward modes.

## Current mode map

| Lane | Current state | Evidence interpretation |
|---|---|---|
| Crypto scalp | Disabled by policy for all entry modes | Historical losses remain diagnostic; no new promotion evidence is collected. |
| Crypto intraday | New pullback and limit-then-taker disabled; breakout exists only in historical backfill | No valid current forward conclusion. The old paper historical cohort is negative and is not proof for B. |
| Crypto swing | Old paper has one current forward fill at -$27.43; B has no current forward fill | B pullback is disabled by the shared policy; historical breakout is negative and hypothesis-only. T140-style conclusions cannot be made from this lane yet. |
| Stocks intraday | Separate B-only `stocks_intraday_forward` lane, only `PULLBACK_LIMIT` and `BREAKOUT_CONTINUATION` | 26 historical rows: 16 filled, 4 missed, 6 skipped, net -$48.09. All are currently dirty because the US session is closed and no clean forward sample exists. |
| Stocks swing/invest legacy | Kept as an audit appendix only | Explicitly `UNSUPPORTED_LEGACY`; excluded from active promotion and from the primary A/B readiness report. |
| Stocks Position Framework | Shadow-only `stocks_swing_growth_breakout`, scheduler enabled | The 13 Jul scan ran: 68 symbols scanned, 0 candidates, 68 rejected, `risk_on`. There are 2 old AAPL candidates, 1 pending outcome, 0 closed outcomes, 0 reviews. No profitability conclusion is allowed. |

## Fixes applied

1. Candidate stock-intraday B-only results no longer enter the general A/B counters, per-asset A/B
   books, or paired deltas. They now have independent `candidate_net_*` and `candidate_by_mode`
   diagnostics.
2. `paper_shadow_events` is now pruned together with outcomes. The live database had 2,547 orphan
   event rows; after the read-model refresh, orphan count is **0**.
3. Generic forward quality, per-mode readiness, calibration, and sequential-gate readers exclude the
   independent stock-intraday lane from A/B evidence.
4. Deprecated stocks swing/invest rows are excluded from the active promotion/readiness book. They
   remain available in the calibration appendix for auditability.
5. Position scans now write a separate `stocks_position_scan_runs` telemetry row even when zero
   candidates pass. This fixed the misleading stale `latest_scan` display: the report now shows the
   13 Jul zero-candidate scan instead of the last day that happened to produce AAPL.
6. Compatibility filters preserve support for old SQLite fixtures that predate `shadow_lane`.
7. The stale `_entry_fill` test was aligned with the current three-value API contract.

## Data quality and latency

The current stock intraday coverage snapshot has 28/28 series marked `SESSION_CLOSED`, therefore
0/28 clean before the US regular session opens. This is expected at the current pre-open time and is
not evidence that the strategy loses. It does mean stock PnL must be re-labeled after a fresh RTH
coverage pass.

The latency audit still shows a material data problem in stocks intraday: 304 `DATA_GAP_LATE` rows,
280 `FAST` rows, 72 `LEGITIMATE_LATE`, and 4 `DETECTION_LATENCY`. Dirty rows remain excluded from
edge metrics. The active stock provider is still yfinance (`live_grade=false`), so stock shadow
execution evidence is not yet equivalent to a live-grade feed.

## Verification

- Targeted shadow/position/coverage/calibration/sequential suites: **160 passed**.
- Scheduler dry-run: CLI validation OK, LLM auto-invoke check OK, dry run complete.
- `py_compile` for changed modules: OK.
- Current database snapshot: `proposed_signals=3616`, `paper_shadow_execution_outcomes=2279`,
  `paper_shadow_events=2198`, orphan events `0`.
- The background bot/scheduler continues to update authoritative `signal_outcomes`; therefore a
  before/after count of that source cannot be used as an invariant while the service is running.
  The changed modules have no writes to `signal_outcomes` or `final_r`.
- Full repository `pytest -q` exceeded the 300-second command timeout. The changed-scope suite is
  green; the full-suite timeout is recorded rather than represented as a pass.

## Operational decision

Continue shadow collection. Do not promote any new mode from this snapshot. The next useful
measurement is a weekday RTH refresh with fresh stock bars, followed by clean forward outcomes;
for crypto, first accumulate valid post-`preentry_v2` forward fills before judging B.
