# POST — Operational Guardrails Deploy Test Results (PART 9)

**Date:** 2026-06-17 · **Command:** `python -m pytest tests/ -q`
**Result:** **742 passed, 0 failed, 0 errors** in 2474.88s (41m14s). Exit code 0.
**Baseline before this stage:** 729 passed → **+13 new tests, no regression.**

## New tests (13)
| File | Tests | Part |
|---|---|---|
| `tests/test_position_advisor.py` | 8 | 7 (label-only leverage advisor) |
| `tests/test_operational_deploy.py` | 5 | 1/4/5/6 (scheduler steps wired, archive dedup/idempotent, dry-run no-write, coverage honest, replay archive-first) |

## Dry / read-only scripts run this stage (no trade effect)
| Script | Result |
|---|---|
| `scripts.catalyst_integrity_scan` | wrote daily summary; flagged ASTER regression-signature on the pre-fix artifact |
| `scripts.archive_ohlcv_history --timeframes 5m,15m` | archived 407×5m / 469×15m symbols; 2nd run +0 (idempotent) |
| `scripts.archive_ohlcv_history --coverage-report` | wrote coverage report |
| `scripts.circuit_breaker_dry_run` | 4 scopes; crypto books would_pause today, stocks ok; no Telegram |
| `scripts.sector_cap_forward_tracker` | 161 alerts scanned; would_bind/actual accumulate forward |
| `scripts.stocks_intraday_diagnostic` | 447 closed trades, net +106R; C-tier −34R is the drag |
| `scripts.open_intraday_lifecycle_review` | 229 open intraday, 12 need review |
| `scripts.replay_profit_protection_path_aware` (archive-first) | 17.8% coverage today → still DATA_COVERAGE_INSUFFICIENT |
| scheduler `--run-once --dry-run` | plan = 22 steps incl. the 3 new non-fatal steps, no LLM auto-invoke |

## What was NOT tested (limitations)
- **Profit-protection on a representative population** — OHLCV archive only started today (~18h of 5m); ≥30d coverage is weeks away. Replay remains coverage-limited.
- **Control Plane runtime** — adapter `py_compile`-clean + permissive `.get()`; no FastAPI integration test run (out of scope; no command/lock change).
- **Live scheduler cycle** — verified via dry-run plan + the new scripts run standalone; not executed as a full live 2h cycle here.
- **Forward trackers (sector-cap, catalyst-integrity-clears)** — by design they need real forward days to produce signal; first runs are seed/baseline.

## Regression safety
Existing suites (catalyst, concentration caps, paper-entry, tracker, scoring, sizing, risk guards) all pass within the 742. New wiring is non-fatal scheduler steps + read-only scripts + add-only payload fields + a pure label module.

## Verdict
**TESTS_GREEN** — 742/742. Safe to keep the operational wiring; no trade behavior changed.
