# POST — Safe Guardrails & Catalyst-Fix Final Decision (PART 9)

**Date:** 2026-06-17 · **Stage:** diagnostics + alert-only/shadow-only guardrails + one catalyst **label** fix.
**Nothing in this stage changed live trading, scalp enablement, scoring, TP/SL, thresholds, the sector-cap value, force-close behavior, historical outcomes, or the Control Plane.**

## Deliverables produced
| Part | Reports / artifacts |
|---|---|
| 0 | `PRE_SAFE_GUARDRAILS_AND_CATALYST_FIX_BASELINE.md` |
| 1 | `CATALYST_NEWS_ITEMS_MAPPING_FIX_REPORT.md`, `CATALYST_NEWS_ITEMS_MAPPING_TEST_RESULTS.md`, `POST_CATALYST_MAPPING_FIX_VERIFICATION.md` + code (`collector.py`, `baskets.py`, `tests/test_catalyst_aster_regression.py`) |
| 2 | `CIRCUIT_BREAKER_WOULD_PAUSE_AUDIT.md` + `.csv` |
| 3 | `STOCK_SECTOR_CAP_LIVE_PATH_WIRING_AUDIT.md`, `STOCK_SECTOR_CAP_WOULD_BIND_REPLAY.csv`, `STOCK_SECTOR_CAP_SHADOW_ONLY_FIX_PLAN.md` |
| 4 | `CRYPTO_PROFIT_PROTECTION_FULL_COUNTERFACTUAL.md` + `.csv` |
| 5 | `INTRADAY_REVALIDATION_WOULD_EXPIRE_AUDIT.md` + `.csv` |
| 6 | `INTRADAY_RISK_OFF_THROTTLE_DIAGNOSTIC.md` + `.csv` |
| 7 | `RISK_GUARD_VISIBILITY_FIELDS_PLAN.md` |
| 8 | `POST_SAFE_GUARDRAILS_AND_CATALYST_FIX_TEST_RESULTS.md` (687 passed) |
| 9 | this report |

---

## The 15 questions

**1. Was the catalyst integrity bug real, and what was it?**
Yes. `build_momentum_breakout_basket()` hard-coded "Top gainers without confirmed news catalyst" **without ever consulting `news_items`**. So genuinely catalyst-backed movers (ASTER buyback) were mislabeled as no-catalyst momentum chases.

**2. Was it a wrong-column bug (`detected_symbols` vs `detected_symbols_json`)?**
No — and that's an important nuance. The live DB exposes only `detected_symbols_json` (no legacy column), and the collector query already reads it correctly. The bug was a **missing lookup**, not a wrong column. The fix still implements the column read **defensively** (schema discovery + legacy fallback) so a future rename can't silently break it.

**3. Is the fix safe / label-only?**
Yes. It changes only the basket *summary* string and `suggested_playbook`. No scoring, entry, tier, threshold, or promotion change. Degrades to `set()` on any error. 687/687 tests pass.

**4. Did ASTER get promoted to actionable?**
No. ASTER is **catalyst-backed but overextended → watch-on-pullback**. The basket never sets an entry/actionable field (enforced by test 7). This is the correct read and the explicit instruction.

**5. Does a circuit breaker have evidence to exist?**
Yes, as **alert-only**. Over 7d: 7 days would trip −2R, 4 days −3R, 10 days ≥3 stops; worst day 06-11 stocks −16R/20 stops. A same-day −2R entry-halt would have avoided ≈25R (optimistic upper bound), missing 0R of winners in this window.

**6. Should the circuit breaker hard-block now?**
No. **`THRESHOLD_NEEDS_MORE_DATA`** — 7 days is too thin and one outlier (06-11) dominates. Ship the would-pause flag + Telegram alert; require ≥30d threshold sweep before any hard auto-pause.

**7. Is the sector cap actually working live?**
No — it is **wired but effectively inert**. It fired 0× live vs 18/92 cluster-day groups that would bind in the day-batch view.

**8. Why is the sector cap inert?**
The live path (`concentration_for_live_signal`) ranks each signal only against *concurrently-open* same-bucket+direction A/B stock-intraday peers at alert time. The *binding* logic (day-batch `apply_stock_concentration_caps`) is only used in tests/scripts, never on the live path. Intraday names rarely have ≥2 concurrently-open correlated peers, so rank stays 1 = actionable.

**9. What's the safe sector-cap next step?**
**Shadow-only**: run the day-batch cap in shadow on the monitor, record `would_bind_sector_cap` + surface it (PART 7). No cap-value change, no cap=3, no soft/hard switch, no blocking. Measure ≥10 trading days before considering a batch-aware live path.

**10. Does crypto profit-protection help?**
Estimates are favorable (BE-after-+1R ≈ +10R; partial-50%-at-+1R ≈ +16R; BE-after-+0.5R ≈ +43R but unreliable) vs −2R current. **But these are MFE/MAE upper bounds** — they ignore intra-trade path order and BE-stop whipsaw, and under-count clipped winners (34 winners touched +1R).

**11. Should profit-protection be enabled?**
No. **`DO_NOT_ENABLE`.** Re-run on **1m OHLCV path replay** so triggers respect sequence; only enable (still paper, with approval) if path-aware net R incl. all winners is positive. `partial_exit_model.enabled` stays false.

**12. Should intraday trades be force-expired / flattened?**
No. Crypto intraday open >12h were net **+10R**; overnight carry was net-positive (prior audit +17R). **`LABEL_AND_REVALIDATE, DO_NOT_FORCE_CLOSE`** — add lifecycle labels + next-session revalidation, never auto-flatten in this stage.

**13. Is the long-bias-into-red-BTC problem real, and costly?**
Real as a pattern (the risk-off flag correctly fires on 06-16/17 down days, not on the 06-15 up day), but **small as a cost**: longs on risk-off days netted only −1R combined (26 losers nearly offset by 16 winners).

**14. Should risk-off throttle longs now?**
No. **`SHADOW_LABEL_ONLY`** — ~1R saved at best while skipping 16 winners isn't worth automated sizing. Ship the regime label for visibility; re-measure over ≥30d incl. a sharper downtrend.

**15. What becomes visible in Telegram / Control Plane?**
Add-only fields (PART 7): `circuit_breaker_state`, `day_realized_r`, `would_bind_sector_cap`, `lifecycle_label`/`held_hours`, `btc_intraday_risk_off`/`regime_context`, `profit_protection_hint`. SL level still always on B/A alerts. No routing/channel/engine-status change.

---

## Verdicts (summary)
| Item | Verdict |
|---|---|
| Catalyst mapping fix | **CATALYST_MAPPING_FIX_READY** (landed, 687 tests green) |
| Circuit breaker | **IMPLEMENT_CIRCUIT_BREAKER_ALERT_ONLY**; hard block = `THRESHOLD_NEEDS_MORE_DATA` |
| Sector cap | wired-but-inert → **SHADOW-ONLY wiring next** (no value change) |
| Crypto profit-protection | **DO_NOT_ENABLE** (MFE/MAE only → need 1m path replay) |
| Intraday revalidation | **LABEL_AND_REVALIDATE, DO_NOT_FORCE_CLOSE** |
| Risk-off throttle | **SHADOW_LABEL_ONLY** |
| Visibility fields | add-only, ship `circuit_breaker_state` + `regime_context` first |

## Recommended order of implementation (all still paper / alert-only)
1. **Circuit-breaker would-pause flag + Telegram alert** (highest leverage, zero trade-behavior risk) — ship with a unit test.
2. **Risk-guard visibility fields** (PART 7) — `circuit_breaker_state` + `regime_context` first.
3. **Sector-cap shadow wiring** (`would_bind_sector_cap`) — measure live binding.
4. *(measurement, not enabling)* **1m path-aware profit-protection replay**; **risk-off label** over ≥30d.

## Do-not-touch (reaffirmed)
Live, auto-live, exchange execution, crypto/stocks scalp enablement, C-tier promotion, the sector-cap value, all scoring/TP/SL/thresholds, force-close, historical outcomes, and the Control Plane — **unchanged** until the above counterfactuals/tests pass and you explicitly approve.
