# POST — Profitability Guardrails Test Results (PART 8)

**Date:** 2026-06-17 · **Command:** `python -m pytest tests/ -q`
**Result:** **729 passed, 0 failed, 0 errors** in 2505.50s (41m45s). Exit code 0.
**Baseline before this stage:** 687 passed → **+42 new tests, no regression.**

## New test groups (42)
| File | Tests | Part |
|---|---|---|
| `tests/test_circuit_breaker.py` | 10 | 1 |
| `tests/test_risk_guard_fields.py` | 6 | 2 (+1 integration) |
| `tests/test_sector_cap_shadow.py` | 6 | 3 |
| `tests/test_intraday_lifecycle.py` | 7 | 5 |
| `tests/test_risk_off_label.py` | 8 | 6 |
| `tests/test_catalyst_integrity.py` | 6 | 7 (catalyst-backed stays watch-pullback) |

## Diagnostic scripts run read-only (dry)
| Script | Result |
|---|---|
| `scripts/replay_profit_protection_path_aware.py` | ran; 28/146 covered (19.2%), all 5m → DATA_COVERAGE_INSUFFICIENT |
| `scripts/catalyst_integrity_scan.py` | ran; wrote `CATALYST_INTEGRITY_DAILY_SUMMARY.md`; flagged ASTER regression-signature on the pre-fix artifact |
| circuit-breaker / sector-cap / lifecycle / risk-off | exercised via unit + integration tests (in-memory + tmp SQLite stores; live DB never written) |

## What was NOT tested (limitations)
- **Path-aware profit protection on a representative population** — OHLCV is rolling-window only (1m≈4h, 5m≈18h, 15m≈2.3d, 1h≈9d), so only 19.2% of 30d trades are path-coverable, biased to the recent loss window. Needs deeper archived 5m/15m history.
- **Control Plane runtime** — the adapter change was compile-checked (`py_compile`) and is a permissive `.get()` pass-through; no FastAPI integration test was run in this stage (out of scope; no command/lock change).
- **Live monitor emission of the circuit-breaker Telegram line** — validated by the paper-entry integration test (send + dedupe), not by a live tick.

## Regression safety
- Existing suites unchanged: catalyst layer, stock concentration caps, paper-entry, tracker, scoring, sizing — all still pass within the 729.
- The 2 new store methods are pure SELECT (no schema change); all new wiring is fail-open and add-only.

## Verdict
**TESTS_GREEN** — 729/729. Safe to keep all PART 1–7 changes; nothing in this stage alters trade behavior.
