# Mode Routing — Decision Recommendation (PART 6)

**Date:** 2026-06-09 · **Scope:** Read-only recommendation. No code/routing changes implemented; this document is the input for the next routing decision.
**Inputs:** PART 1 (`MODE_VIABILITY_STATS_AUDIT.md`), PART 2 (`CRYPTO_SCALP_VIABILITY_AUDIT.md`), PART 3 (`STOCKS_INVEST_VIABILITY_AUDIT.md`), PART 4 (`STOCKS_INTRADAY_SWING_SANITY_AUDIT.md`), PART 5 (`MODE_ROUTING_SIMULATION_REPORT.md`).

## 1. Recommendations

### Crypto scalp → **Option 2 (recommended): Keep active but mark low confidence**
Concrete posture:
- Do **not** pause scalp.
- Do **not** restrict scalp to catalyst-only — PART 2 §5.1 shows catalyst-backed scalp is *worse* (0W/2L) than no-catalyst (1W/5L) over 14d. PART 5 confirms every restrictive variant strips the only win.
- Do **not** cap to C-tier — same overfitting risk, and the entry edge (100% positive MFE on expired) is real diagnostic signal.
- **Surface scalp results with a "low-confidence" tag** in user-facing summaries (Telegram, dashboards, Opus reviews) so the reader weighs them appropriately.
- Continue collecting closed-trade data. Re-audit at **20 closed scalp A/B signals** (currently at 8; needs another ~12). At the current pace (≈8 closures / 14 d) that is ~3 more weeks.

Rationale: PART 2 identified the failure mode as **TP1 distance vs 2h horizon mismatch, not entry-edge failure**. The fix lives in TP/SL/strategy — out of audit scope. Pausing now would freeze the diagnostic data needed for that fix later. Marking low-confidence preserves the diagnostic stream while signaling caution to users.

**Backup option:** Option 1 (keep unchanged for 2–3 more days) is acceptable if "low-confidence tag" is operationally awkward — both have the same data-collection benefit.

### Stocks invest → **Option 2 (recommended): Watchlist-only**
Concrete posture:
- Demote invest A/B to **C-tier (watchlist-only)** via the same gate pattern used for stocks-swing pause (`cap_reasons` marker, no Telegram A/B alert).
- Use the marker `stocks_invest_paused_after_mode_viability_audit` (cap_reason text: "0W/7L over 14d, identical failure mode to paused stocks-swing — pipeline overlap").
- **Continue collecting C-tier outcomes** to validate or invalidate.
- Re-audit after **1 full US trading week of C-tier accumulation** AND when post-pause stocks-swing C-tier hits 20+ closures (currently 1 closed of 25 post-pause).

Rationale: PART 3 §6 found stocks-invest **duplicates the swing pipeline** with a longer leash (720 h vs 168 h). The 13/13 LONG losses match the same tickers, dates, and directions that triggered the swing pause. PART 5 confirmed no read-only filter rescues invest. The horizon argument ("invest just needs more time") is **structurally rebutted by the loss anatomy** (stops fire in 1–6 days, median 2 days — the 30-d window is never the binding constraint).

**Why not Option 4 (full pause):** sample is 7 A/B closures; numerically thin for a hard pause. Watchlist-only matches the soft-pause precedent set for stocks-swing.

**Why not Option 1 (keep 2-3 sessions):** the 7 closed losses are concentrated in the late-May → 06-03 tech-long batch, which is precisely the failure mode the stocks-swing pause was designed to stop. Letting actionable invest signals from the same pipeline continue to fire (and trigger Telegram A/B alerts) re-opens the leak that the swing pause closed.

### Stocks swing → **Option 3 (recommended): Keep watchlist-only until 1 full week of C-tier outcomes**
Concrete posture:
- **Hold the existing pause.** 0 A/B leaks in 25 post-pause swings (PART 4 §2.1) — gate is working.
- Continue C-tier accumulation. Currently 1 closed of 25 (1W/0L flat); 11 still pending.
- Re-audit when post-pause C-tier reaches **≥20 closures** (≈1–2 more US trading weeks at current pace).
- If the C-tier counterfactual shows WR ≥ 35% and PF ≥ 1.0, partial re-enable can be considered (high-score, B-tier-only, news-supported subset). Otherwise extend the pause.

Rationale: PART 4 §2.3 — without code changes the same pipeline cannot produce different outcomes. The 14d pre-pause record (5W/36L, −30R) is the structural baseline; the post-pause 1W on 1 closure is consistent with the pre-pause 12% WR. No evidence yet to invalidate the pause.

## 2. Implementation guardrails (NOT applied — this is the spec)

If the user approves implementing the invest watchlist-only routing, the implementation **must**:
- Mirror the exact pattern of the existing stocks-swing pause gate (`src/stocks/agents/trade_idea_agent.py`, the Gate-C pattern):
  - Apply only to `asset_class=stocks AND mode=invest`.
  - Demote A/B → C; do not hard-reject.
  - Append `stocks_invest_paused_after_mode_viability_audit` to `cap_reasons`.
  - Append a human-readable explanation to `avoid_conditions`.
- Add a watchlist-only banner to `src/stocks/reports/stocks_report_builder.py` for `mode=invest` (same pattern as the swing banner).
- Add focused tests under `tests/test_stocks_invest_pause.py` modelled on `tests/test_stocks_swing_pause.py`.
- Do **not** change scoring/thresholds, do **not** touch crypto, do **not** touch stocks-intraday, do **not** restart the scheduler before tests pass and a verification report is written.

**Nothing in this audit changed code.** All implementation is gated on a separate, explicit user approval.

## 3. Re-audit triggers

| Condition | Re-audit |
|---|---|
| Crypto scalp closed A/B reaches 20 (currently 8) | Yes — rebuild PART 2 |
| Crypto scalp catalyst-only closed reaches 8 (currently 2) | Yes — re-test the catalyst gate hypothesis |
| Stocks invest watchlist C-tier closed reaches 20 | Yes — confirm or revoke watchlist-only |
| Stocks swing watchlist C-tier closed reaches 20 (currently 1 of 25 post-pause) | Yes — re-test swing pause |
| Crypto A-tier scalp signal fires (currently 0 in 14d) | Yes — A-tier behavior unknown |
| Any code change to scalp TP1/SL/horizon | Mandatory — invalidates current MFE-based assessment |
| Any code change to invest stop/horizon | Mandatory — invalidates current loss-anatomy assessment |

## 4. What this audit does NOT recommend

- No catalyst-only gate for crypto scalp (data does not support).
- No regime gate for crypto scalp (no regime shows positive PF; gating would just shrink sample).
- No A-tier suppression (stocks A-tier mostly lives inside the already-paused swing batch; intraday A-tier sample is too thin).
- No code/scoring/threshold/TP/SL change in any mode.
- No scheduler restart.
- No auto-trade enablement.

## Final answer
```
MODE_VIABILITY_AUDIT_COMPLETE
```

Caveat: the verdict `MODE_VIABILITY_AUDIT_COMPLETE` reflects audit completeness, not statistical certainty. The crypto scalp (8 closures) and stocks invest (7 A/B closures) samples are **below the 20-closure noise floor for either mode** — the recommendations above are calibrated to that uncertainty (keep + mark low-confidence; soft-pause / watchlist-only) rather than to a confident pass/fail.
