# Paper Operational Audit

Generated: `2026-11-11T21:03:08.940311+00:00` - window: `7d`

## Authoritative net USD

| Asset | Mode | Side | Closed | Net USD | PF | WR | Max DD | Top-3 winner share | Fee profile |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| crypto | intraday | long | 7 | -36.30 | 0.00 | 0% | 36.30 | n/a | bybit_non_vip_usdt_perp |
| crypto | intraday | short | 2 | -3.01 | 0.00 | 0% | 3.01 | n/a | bybit_non_vip_usdt_perp |
| stocks | intraday | long | 1 | -1.59 | 0.00 | 0% | 1.59 | n/a | mexc_default_futures |
| stocks | intraday | short | 8 | -50.60 | 0.52 | 38% | 80.90 | 100% | mexc_default_futures |

## Evidence
- crypto intraday long: forward clean closed 1 - forward dirty closed 0 - historical/unclassified closed 0 - open/unresolved 1
- crypto intraday short: forward clean closed 4 - forward dirty closed 0 - historical/unclassified closed 0 - open/unresolved 3
- stocks intraday long: forward clean closed 14 - forward dirty closed 0 - historical/unclassified closed 0 - open/unresolved 246
- stocks intraday short: forward clean closed 25 - forward dirty closed 0 - historical/unclassified closed 0 - open/unresolved 412

## Routing and overlays
- crypto intraday: unique signals 44 - BLOCK 5, FULL_SIZE 14, HALF_SIZE 6, SHADOW_ONLY 19
- crypto intraday alerts: live_not_queued 4, shadow_crypto_quality 3 - sizes 0.5x 2, 1.0x 5 - overlay UNKNOWN 7 - guard NO_GUARD_ACTION 7
- stocks intraday alerts: late_shadow 8, live_not_queued 18, shadow_sector_cap 7 - sizes 0.0x 12, 0.5x 12, 1.0x 9 - overlay SHADOW_ONLY 10, UNKNOWN 23 - guard NO_GUARD_ACTION 33

## Stocks funnel
- snapshots: `{"PREOPEN_PLAN": 497, "REJECTED_AT_DECISION": 150, "RTH_ELIGIBLE": 50}`
- RTH decisions: `{"PREUS_MEXC_PAPER_FILLED": 4, "READY_FOR_EXISTING_PAPER_TRACKER": 19, "REJECTED_PREUS_ACTIONABILITY": 186, "REJECTED_PREUS_REVIEW_OR_RTH_CANDIDATE_MISSING": 201}`
- awaiting fresh RTH candidate: `0`

## Stocks USD-ledger reconciliation
- clean closed executions: `39`
- actionable closed / ledger present / same-trade deduplicated / missing: `6 / 6 / 0 / 0`
- intentionally non-actionable (Shadow): `33` `[["legacy_actionable_non_crypto", 28], ["alert_status_non_actionable", 5]]`

## MEXC handoff
- decisions: `{"REJECTED": 7}`
- eligibility: `{"ineligible": 7}`
- outbox: `{}`
- venue attempts: `{}`
- venue rejections: `[]`
- positions: `{"CLOSED": 226}` - open risk `$0.00`
- parity mexc_model_f_runner_v1: clean forward closed 26 - net `$-32.60` - PF `0.068`
- parity mexc_partial_tp_33_33_34_v1: clean forward closed 26 - net `$-29.87` - PF `0.136`

## Latency
- crypto acceptance: `INSUFFICIENT_SAMPLE`
- stocks intraday acceptance: `INSUFFICIENT_SAMPLE`
- Plan age signal -> entry (not execution latency): `{"max": 58158.5, "n": 161, "p50": 2220.6, "p90": 47568.4, "p95": 54678.3}`
- Detection -> MEXC capture: `{"max": null, "n": 0, "p50": null, "p90": null, "p95": null}`
- MEXC queue -> preflight: `{"max": null, "n": 0, "p50": null, "p90": null, "p95": null}`
- MEXC preflight -> submit: `{"max": null, "n": 0, "p50": null, "p90": null, "p95": null}`

## News quality
- status: `NOT_READY` - p95 resolution `26.43s` - reasons `["primary_source_error_dead=4"]`

## Warnings
- `INSUFFICIENT_CLEAN_FORWARD_SAMPLE:crypto intraday long:1`
- `WEAK_PROFIT_FACTOR:crypto intraday long:0.0`
- `INSUFFICIENT_CLEAN_FORWARD_SAMPLE:crypto intraday short:4`
- `WEAK_PROFIT_FACTOR:crypto intraday short:0.0`
- `INSUFFICIENT_CLEAN_FORWARD_SAMPLE:stocks intraday long:14`
- `WEAK_PROFIT_FACTOR:stocks intraday long:0.0`
- `INSUFFICIENT_CLEAN_FORWARD_SAMPLE:stocks intraday short:25`
- `PNL_CONCENTRATED_TOP3:stocks intraday short:1.0`
- `WEAK_PROFIT_FACTOR:stocks intraday short:0.521`
- `NEWS_QUALITY_NOT_READY:primary_source_error_dead=4`
