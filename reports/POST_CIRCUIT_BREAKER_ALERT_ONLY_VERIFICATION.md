# POST — Circuit Breaker Alert-Only Verification (PART 1)

**Date:** 2026-06-17 · **Verdict:** **CIRCUIT_BREAKER_ALERT_ONLY_READY**

## Verification checklist
- [x] `evaluate_circuit_breaker` fires would_pause at ≤ −2R, level 3 at ≤ −3R, and on ≥3 stops/day (unit tests).
- [x] Crypto-long-streak + consecutive-stop + size-stepdown flags computed (unit tests).
- [x] Store wrapper loads only **today's** terminal outcomes for the signal's asset/mode scope; excludes other assets/days (unit test).
- [x] Integration: with a seeded −3R day, the paper-entry alert **still sends** (`telegram_status=sent`), routing stays `telegram`, size untouched — the breaker does NOT block (integration test).
- [x] Telegram warning is **deduped** one-per asset/mode/day/level via a `cb_diag:*` marker (integration test).
- [x] Fails open on any store error → `ok` / no pause.
- [x] All edited modules compile; 16/16 PART-1 tests pass; full suite re-run at PART 8.

## Recommended threshold (from the would-pause audit, 7d)
- **−2R daily** is the most useful single trigger (fired 7 days, avoided ≈25R of same-day continuation, 0 winners missed in that window).
- Pair with **≥3 stops/day** to catch high-frequency bleed days that don't yet show −2R net.
- **Do NOT** convert to a hard auto-pause until a ≥30d sweep confirms; ship alert-only now.

## Rollback
Remove the `assemble_risk_guard_fields` call block in `paper_entry.py` and delete `src/risk/circuit_breaker.py` + the 2 store helpers. Zero data migration; the `cb_diag:*` marker rows are inert diagnostic alerts.
