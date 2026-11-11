# Profitability Levers Audit — Final Recommendation

**Date:** 2026-06-10 · Read-only synthesis. No code, scoring, threshold, TP/SL, or signal-generation changes proposed for immediate implementation in this PR.

**Companion reports (all in this PR):**
- [STOCKS_A_TIER_OVERPROMOTION_STUDY.md](STOCKS_A_TIER_OVERPROMOTION_STUDY.md) — PART 1
- [CRYPTO_SCALP_EXIT_SIMULATION.md](CRYPTO_SCALP_EXIT_SIMULATION.md) — PART 2
- [CRYPTO_EXPANSION_WATCHLIST_QUALITY_AUDIT.md](CRYPTO_EXPANSION_WATCHLIST_QUALITY_AUDIT.md) — PART 3
- [CATALYST_MAPPING_IMPROVEMENT_CANDIDATES.md](CATALYST_MAPPING_IMPROVEMENT_CANDIDATES.md) — PART 4
- [PLAYBOOK_POSITION_SIZING_SIMULATION.md](PLAYBOOK_POSITION_SIZING_SIMULATION.md) — PART 5

## 1. Executive summary

The system today produces strong signals on its best cohorts (crypto swing 50% WR / PF 2.22, stocks intraday B-tier 56% WR / PF 2.x, catalyst-backed intraday PF 1.83) but is dragged into negative territory by two persistent weak cohorts: **crypto scalp** (0/9 closed, low-confidence by design) and **stocks A-tier intraday longs** (21% WR / −6.2R, RTH-open chase symptom).

**The single highest-impact, lowest-risk lever is `playbook_aware` position sizing** (PART 5): same signals, half-size on low-confidence + A-tier-long, zero on paused modes. Counterfactual on the existing per-setup dataset: **portfolio totalR flips from −31R to +34R, WR rises 32% → 43%, PF doubles 0.78 → 1.51, max drawdown halves**.

## 2. Ranked recommendations

Each lever is scored by:
- **Impact** (S/M/L expected R contribution)
- **Risk** (overfit + breakage)
- **Data sufficiency** (n closures supporting the decision)
- **Code change required** (Yes/No/Config)
- **Signal-flow impact** (does it change alert volume?)

### Lever 1 — **`playbook_aware` position sizing (config only)** ⭐

| Dimension | Rating |
|---|---|
| Impact | **L** (+65R simulated swing on same dataset) |
| Risk | **Very Low** — does not touch signal generation |
| Overfit risk | Low — sizing rules derive from independent cohort audits (14d audit, 48h audit, scalp deep-dive) |
| Data sufficiency | Medium-High (271+ deduped setups; A-tier subset n=19 marginal but consistent) |
| Code change | Config-file only (`sizing_weights.yaml`) + dashboard/report annotation |
| Signal flow | **None** — alerts unchanged |

**Recommendation:** **highest priority** for next implementation cycle. Sizing is the cleanest profitability lever because it converts existing analyses into measurable P&L improvement without touching strategy.

### Lever 2 — **Crypto scalp TP1 → +0.5R** (strategy change, deferred)

| Dimension | Rating |
|---|---|
| Impact | **M** (+6.5R on the 40-trigger scalp set; would also let the low-confidence banner fade) |
| Risk | **Medium-High** — TP geometry change |
| Overfit risk | Medium — based on MFE/MAE only, not bar-level replay |
| Data sufficiency | n=40 triggered scalp signals; need 1m-bar replay before committing |
| Code change | YES — changes `TechnicalSetupAgent` TP placement |
| Signal flow | None directly; could reduce expired-flat count |

**Recommendation:** **research-only.** Before changing geometry, run a 1m-bar reconstruction over the same 40 signals to confirm MFE/MAE order is what the simulation assumes. If confirmed, propose as a separate PR.

### Lever 3 — **Stocks A-tier-long RTH-open gate** (gate logic change, deferred)

| Dimension | Rating |
|---|---|
| Impact | **M** (+4–6R if 11 of 19 A-tier RTH-open longs would have been demoted to B) |
| Risk | **Medium** — adds a gate that could miss A-tier winners (UNH +1, LLY +1) |
| Overfit risk | Medium — based on 19 closures; need 20+ post-deploy to validate |
| Data sufficiency | Medium |
| Code change | YES — gate in `src/stocks/agents/trade_idea_agent.py` |
| Signal flow | Reduces A-tier alert volume during 13:00–14:59 UTC; user might miss rare clean A's |

**Recommendation:** **deferred.** Lever 1 (sizing) captures most of this risk reduction without the false-negative cost.

### Lever 4 — **Crypto expansion lane: study 20→25 cap** (research)

| Dimension | Rating |
|---|---|
| Impact | **S–M** (unknown; possibly +5R from currently-missed names) |
| Risk | Medium — runtime + scoring noise |
| Overfit risk | Low |
| Data sufficiency | Insufficient (need a multi-cycle staging run) |
| Code change | YES — config bump in report settings |
| Signal flow | More A/B candidates per cycle (~20% more) |

**Recommendation:** **deferred to a SANDBOX staging schedule.** Measure runtime delta + PF impact over 5 cycles before any production change.

### Lever 5 — **Non-crypto noise filter on news collector** (config, low impact)

| Dimension | Rating |
|---|---|
| Impact | **S** (cleaner catalyst pipeline, sharper Opus context) |
| Risk | Very Low |
| Overfit risk | Very Low |
| Data sufficiency | Sufficient (top tokens are clearly non-crypto) |
| Code change | Config-only (`news_sources.yaml` or filter list) |
| Signal flow | None |

**Recommendation:** **queue for a small reporting-cleanup PR.**

### Lever 6 — **Macro_release catalyst classification** (small classifier change)

| Dimension | Rating |
|---|---|
| Impact | **S** (CPI/Fed/FOMC days surface as macro overlay, not as missed catalyst) |
| Risk | Low |
| Code change | Small classifier extension |
| Signal flow | None |

**Recommendation:** queue alongside Lever 5.

### Lever 7 — **Expansion lane stays shadow-only** (no change needed)

Already operational. Confirmed by 44% promotion-to-A/B rate of expansion candidates via the standard scoring path. Keep.

## 3. Final ranking

| Rank | Lever | Priority | Type | Touches code? |
|---|---|---|---|---|
| **1** | **`playbook_aware` sizing config** | **NOW** (next PR) | Config + reporting | Config only |
| 2 | Non-crypto news-source filter + macro_release classifier | Soon | Small classifier + config | Yes (small) |
| 3 | Crypto scalp TP1 → +0.5R | Research | Strategy change | Yes (geometry) — needs approval |
| 4 | Expansion cap study 20→25 | Research | Staging experiment | Config in sandbox |
| 5 | Stocks A-tier-long RTH-open gate | Deferred | Gate logic | Yes — only if sizing doesn't catch it |

## 4. What this audit explicitly does NOT recommend
- No changes to scoring weights.
- No changes to thresholds (A/B score cutoffs unchanged).
- No changes to TP/SL geometry in this PR.
- No re-enabling of stocks swing or stocks invest (counterfactual data still −7R / −18R per 48h audit).
- No changes to crypto expansion v1 behavior (shadow-only stays).
- No data deletion or rewrite.

## 5. Data sufficiency check

| Question | Answer |
|---|---|
| Is sizing-scheme sample large enough? | Yes — 371 deduped setups, 271+ closures |
| Is A-tier sample large enough? | Borderline — n=19; consistently weak across 3 weeks |
| Is scalp simulation sample large enough? | Yes for the direction — n=40 triggered, 9 closed, MFE distribution stable |
| Is expansion-quality data large enough? | No — only 18h of v1 data. Re-audit at 7 days. |
| Is catalyst-mapping audit conclusive? | Yes — top tokens are clearly non-crypto noise |

**The only "need more data" cohort is expansion quality.** Sizing has enough data to act on.

## 6. Final answer

```
PROFITABILITY_LEVERS_AUDIT_COMPLETE
```

The next high-impact, low-risk improvement is **`playbook_aware` position sizing** (Lever 1). It changes how we measure outcomes, not how we generate signals — same alerts, same gates, same data. Expected impact on the existing dataset: +65R swing in totalR, PF doubling, drawdown halving. Implementation is a config file + a sizing column in the reports/dashboard.

All other levers are queued: small reporting cleanups (Lever 5–6), research-only items pending more data (Lever 2–4), or already-deployed and validated (expansion shadow-only — Lever 7).
