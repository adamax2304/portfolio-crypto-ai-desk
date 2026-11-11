# POST — Profitability Guardrails Final Decision (PART 9)

**Date:** 2026-06-17 · **Stage:** visibility + alert-only/shadow-only guardrails + catalyst-integrity monitoring + path-aware profit measurement.
**Nothing in this stage changed live trading, scalp enablement, scoring, TP/SL, thresholds, the sector-cap value, force-close, or the Control Plane's safety/commands/locks.**

## Deliverables
| Part | Code | Reports |
|---|---|---|
| 0 | — | `PRE_PROFITABILITY_GUARDRAILS_IMPLEMENTATION_BASELINE.md` |
| 1 | `src/risk/circuit_breaker.py`, 2 store helpers, paper-entry wiring | `CIRCUIT_BREAKER_ALERT_ONLY_IMPLEMENTATION.md` + `_TEST_RESULTS.md` + `POST_CIRCUIT_BREAKER_ALERT_ONLY_VERIFICATION.md` |
| 2 | `src/risk/risk_guards.py`, Control-Plane adapter + TS types | `RISK_GUARD_VISIBILITY_FIELDS_IMPLEMENTATION.md` + `_TEST_RESULTS.md` |
| 3 | `src/signals/sector_cap_shadow.py` | `STOCK_SECTOR_CAP_SHADOW_ONLY_WIRING_IMPLEMENTATION.md` + `_TEST_RESULTS.md` + `_FORWARD_PLAN.md` |
| 4 | `scripts/replay_profit_protection_path_aware.py` | `CRYPTO_PROFIT_PROTECTION_PATH_AWARE_REPLAY.md` + `.csv` |
| 5 | `src/signals/lifecycle.py` | `INTRADAY_LIFECYCLE_LABELS_IMPLEMENTATION.md` + `_TEST_RESULTS.md` |
| 6 | `src/risk/risk_off.py` | `INTRADAY_RISK_OFF_LABEL_IMPLEMENTATION.md` + `_TEST_RESULTS.md` + `_30D_MEASUREMENT.md` |
| 7 | `src/catalysts/integrity.py`, `scripts/catalyst_integrity_scan.py` | `CATALYST_INTEGRITY_MONITORING_IMPLEMENTATION.md` + `CATALYST_INTEGRITY_DAILY_SUMMARY.md` |
| 8 | — | `POST_PROFITABILITY_GUARDRAILS_TEST_RESULTS.md` (729 passed) |
| 9 | — | this report |

---

## The 16 questions

**1. What was implemented?** Six diagnostic modules — alert-only circuit breaker, risk-guard visibility assembler, sector-cap shadow/would-bind, intraday lifecycle labels, risk-off label, catalyst-integrity monitor — plus a path-aware profit-protection replay script, 2 read-only store helpers, add-only paper-entry payload wiring with a deduped Telegram warning line, and a read-only Control-Plane pass-through. 42 new tests.

**2. What is diagnostic-only?** Everything. Every field carries `diagnostic_only=True`; no module blocks a trade, changes size, routing, TP/SL, scoring, or the sector-cap value. All entry points fail open.

**3. Did catalyst monitoring pass?** Yes — and it earned its keep on day one: the live scan flagged the exact regression signature (ASTER in a no-catalyst basket while having a direct high-importance news hit) on the **pre-fix on-disk artifact**. 6 unit tests pass; the ASTER-like case stays catalyst-backed watch-on-pullback. **Verdict: CATALYST_INTEGRITY_MONITORING_READY.**

**4. Is circuit breaker alert-only ready?** Yes. Would-pause fires at ≤−2R / ≤−3R / ≥3 stops / ≥2 crypto-long stops; the paper-entry integration test proves it does NOT block the alert and the warning is deduped per asset/mode/day/level. **Verdict: CIRCUIT_BREAKER_ALERT_ONLY_READY.**

**5. What threshold looks best?** **−2R daily** as the primary trigger (highest leverage, 0 winners missed in the audit window), paired with **≥3 stops/day** for high-frequency bleed. −3R = escalation (L3). These stay alert-only until a ≥30d sweep.

**6. Is the sector-cap live path still inert?** Yes — structurally. The live per-signal check sees no concurrent peers; 0× live vs 18/92 day-batch groups. Unchanged this stage (by design).

**7. Is shadow-only would-bind ready?** Yes. The day-batch cap runs in shadow and emits `would_bind_sector_cap` + the actual-vs-would gap, without touching routing or the cap value. **Verdict: SECTOR_CAP_SHADOW_ONLY_READY.**

**8. Did path-aware profit protection confirm BE/partial?** Not conclusively. On the covered slice every variant beats current (BE+0.5R −19.8R→−3.0R; partial-TP1 −10.2R/PF 0.40), but **coverage is only 19.2%** and biased to the recent loss window — winners-clipping is invisible there. **Directionally supportive, not confirmatory.**

**9. Should profit protection stay disabled?** **Yes.** `partial_exit_model.enabled` stays `false`. **Verdict: DATA_COVERAGE_INSUFFICIENT → PROFIT_PROTECTION_STAYS_DISABLED.** Re-run on archived deeper 5m/15m history across both regimes before any enable.

**10. Are intraday lifecycle labels ready?** Yes — labels + revalidation flags, no force-close (overnight carry is net-positive). **Verdict: INTRADAY_REVALIDATION_ALERT_ONLY_READY.**

**11. Is the risk-off label useful?** As **visibility** yes (validated: 06-15 up no-trigger, 06-16/17 down trigger). As an **action**, no: 30d base rate 36.7% and only −1R of throttle-able loss in the 7d sample. **Verdict: RISK_OFF_LABEL_READY (visibility) / NEEDS_MORE_DATA (to throttle).**

**12. What is now visible in Telegram / Control Plane?** Telegram B/A alerts append (when present) deduped lines: circuit-breaker would-pause, risk-off context, carryover/revalidation, sector-cap would-bind, catalyst-backed confirmation — SL line always preserved. Control Plane surfaces the same fields read-only via `desk_adapter.py` + optional `Signal` TS fields. No routing/lock/command change.

**13. What tests passed?** `pytest tests/ -q` → **729 passed, 0 failed** (687 baseline + 42 new), 41m45s, exit 0.

**14. What remains locked?** Live, auto-live, exchange execution, crypto scalp actionable, stocks scalp production, scoring, TP/SL, thresholds, sector-cap value, force-close, hard production block, historical outcomes, Control Plane safety/commands/locks.

**15. Is the system ready for manual micro-live?** **No — not yet.** This stage adds protection-visibility, not validated profitable behavior. Crypto intraday/swing is ~breakeven (PF≈1.0); the drag is stocks-intraday (≈−12R) and crypto-scalp (≈−7R, already shadow). Micro-live should wait for **forward validation** of the alert-only guardrails + a path-aware profit-protection result on representative data. **Verdict: SYSTEM_NOT_READY_FOR_LIVE / MANUAL_MICRO_LIVE_ONLY_AFTER_FORWARD_VALIDATION.**

**16. Next 3 actions?**
1. **Run the alert-only guardrails forward for 2–4 weeks** and collect: how often the circuit breaker would-pause fires + the R it would have saved; how often the sector cap would-bind; risk-off label hit/miss vs outcomes.
2. **Archive deeper 5m/15m OHLCV** and re-run the path-aware profit-protection replay across up+down regimes; only then discuss shadow-enabling partial-TP1 / BE-after-1R.
3. **Wire the daily catalyst-integrity scan + circuit-breaker would-pause into the scheduler/Telegram** (after a fresh catalyst-scan clears the stale ASTER artifact), so regressions and bleed-days surface automatically.

---

## Verdict roll-up
| Item | Verdict |
|---|---|
| Overall | **PROFITABILITY_GUARDRAILS_ALERT_ONLY_READY** · **NO_PRODUCTION_STRATEGY_CHANGE** |
| Circuit breaker | CIRCUIT_BREAKER_ALERT_ONLY_READY |
| Risk-guard visibility | READY (add-only, Control Plane read-only) |
| Sector cap | SECTOR_CAP_SHADOW_ONLY_READY (still inert live, by design) |
| Profit protection | DATA_COVERAGE_INSUFFICIENT → PROFIT_PROTECTION_STAYS_DISABLED |
| Intraday lifecycle | INTRADAY_LIFECYCLE_LABELS_READY |
| Risk-off | RISK_OFF_LABEL_READY (throttle NEEDS_MORE_DATA) |
| Catalyst integrity | CATALYST_INTEGRITY_MONITORING_READY |
| Live readiness | SYSTEM_NOT_READY_FOR_LIVE · MANUAL_MICRO_LIVE_ONLY_AFTER_FORWARD_VALIDATION |

## Principle honored
This stage makes the system **safer and more transparent** — it stops catastrophic-day blindness (circuit breaker), prevents catalyst misclassification (integrity monitor), makes risk visible (guard fields), and measures profit protection **correctly** (path-aware, with honest coverage limits). It does **not** pretend a profitable switch was found. Optimized for fewer stupid losses and clearer explanations, not more trades.
