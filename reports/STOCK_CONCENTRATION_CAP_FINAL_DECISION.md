# Stocks Concentration Cap — Final Decision (PART 9)

**Date:** 2026-06-16

## Verdict

```
STOCK_CONCENTRATION_CAP_READY_SHADOW_FIRST
```

The overlay is built, wired (live paper-entry + payload), and fully tested, but the
full-history counterfactual is **not a clean P&L win** (it is duplicate-confounded and
regime-dependent). It is a risk-shape / manual-de-noise tool — so enable it in its
shadow/label + alert-de-noising form first and validate forward before treating the
sized-R cap as a P&L-positive production rule.

## Answers
1. **Proxy duplicate stacking fixed?** Yes — Rule A collapses QQQ/XLK, SPY/DIA/IWM, and
   same-symbol duplicates to the single best candidate; the rest route shadow.
2. **Sector concentration capped?** Yes — Rule B caps per risk_bucket+direction at
   1.0×/0.5×/0× (1st/2nd/3rd+), counting existing open exposure, combined conservatively
   with the playbook weight.
3. **Non-stock / non-intraday modes unaffected?** Yes — crypto (incl. scalp shadow 0×),
   stocks swing/invest (paused 0×), and C-tier are all `not_applicable` / unchanged
   (tests 9–12).
4. **Raw signals & raw R preserved?** Yes — overlay writes nothing to the DB, mutates no
   input, preserves score/tier/TP/SL/raw R; labels live in `payload_json`.
5. **Counterfactual R change?** Recent windows positive (7d/14d ≈ +1.5R vs baseline sized;
   cluster bleed −13→−7; worst day −4.5→−2.5; today's −4R softened). Full history negative
   (sized +133 → +15) — but that is a **duplicate-signal + trend-regime artifact** of an
   equal-weight-everything baseline no live operator uses; we explicitly do **not** claim a
   P&L improvement. Rule A alone (proxy collapse) is the more robust component (14d +10.5).
6. **Enable in production or shadow-first?** **Shadow-first.** The live wiring already
   behaves correctly for a manual operator (de-noises correlated alerts, warns on 2nd,
   shadows 3rd+). Keep it in this label/route form; do not retroactively rescore historical
   P&L on it; revisit hard sizing enforcement after forward validation.
7. **Follow-up still needed?**
   - Insert the "Stocks Concentration Guard" section into the Obsidian dashboard (data +
     helper ready; deferred to keep the live surface minimal).
   - Forward-validate over the next weeks of fresh stock entries; if cluster-loss days keep
     dominating, promote from shadow-first to full enforcement.
   - Consider tuning bucket granularity (e.g. split semis vs megacap more finely) once
     `sector` data is populated upstream.

## Change surface
`config/stock_risk_clusters.yaml` (new), `src/stocks/risk_clusters.py` (new),
`src/signals/portfolio_caps.py` (new), `src/notifiers/paper_entry.py` (live wiring),
`tests/test_stock_concentration_caps.py` (new, 20), `scripts/audit_sector_concentration.py`
+ `scripts/counterfactual_stock_concentration.py` (read-only research). No scoring / TP-SL /
threshold / generation / schema change; no auto-trade; raw R and history intact.

---

**FINAL ANSWER: `STOCK_CONCENTRATION_CAP_READY_SHADOW_FIRST`**
