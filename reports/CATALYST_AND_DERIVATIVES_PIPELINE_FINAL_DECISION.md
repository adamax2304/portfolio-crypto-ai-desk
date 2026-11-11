# Catalyst & Derivatives Pipeline — Final Decision (PART 10)

**Date:** 2026-06-15

## Verdict

```
CATALYST_PIPELINE_WORKING_BUT_NEEDS_LABELS
```

The pipeline correctly collects news/catalysts/funding/OI, feeds them to Opus and the scorer, and crypto catalyst-backed signals demonstrably trade far better. The weaknesses are **labelling and archiving** (additive, safe), plus one optional scoring change (freshness gate) that needs separate approval — not a broken pipeline.

## Answers (crypto + general)

1. **Collects news/catalysts correctly?** ✅ Yes — 13,748 items, 1,718/48h, RSS + real-time Telegram + bridge, daily catalyst JSONL.
2. **Does Opus see catalysts?** ✅ Yes — crypto packet includes catalysts, baskets (freshness-labelled), funding/OI, regime. Two minor visibility gaps (individual catalyst age, stocks options absence silent).
3. **Does scorer/tier logic use catalysts?** ✅ Yes — `catalyst_quality` component (baseline 0.3 + importance/10 − risk penalty), rumour cap at 55, derivatives alignment penalty.
4. **Which playbooks depend on catalysts?** crypto swing (most), crypto intraday catalyst, failed-bounce shorts (negative catalyst + squeeze), stocks intraday (news + earnings). Scalp does NOT (by design).
5. **Crypto scalp technical or catalyst-driven?** **Technical** — correctly so. News is not required for scalp.
6. **Checks funding?** ✅ 100% of crypto A/B signals.
7. **Checks OI?** ✅ 100% of crypto A/B signals.
8. **Funding/OI point-in-time or latest-cache?** **Latest-cache** (snapshot at signal creation; no historical archive table).
9. **Catch fast moves quickly?** ⚠️ Partial — collection is real-time but signal generation is on a ~2h cycle, so fast intraday pumps are entered late or (correctly) rejected as chase.
10. **Telegram clear on catalyst vs technical?** ⚠️ Partial — risk cautions present (scalp low-confidence, no-news short), but no positive catalyst/source/freshness label.
11. **Categories trading without enough catalyst/derivatives support?** Stocks (no options/OI; news flag unset). Crypto scalp by-design technical. Everything else is adequately supported.
12. **Fix first?** (1) Set the stocks `news_supported` label; (2) add funding/OI snapshot archive; (3) add catalyst/source/freshness labels to dashboard + Telegram (after approval).
13. **Do NOT change yet?** Scoring (the freshness gate), thresholds, TP/SL, routing, sizing. No unpausing, no promotion, no filter weakening.

## Answers (stocks-specific, the 7 extra questions)

1. **Does the system see stock news?** ✅ Yes — 7,547 stock news items in 14d (Yahoo, Motley Fool, Seeking Alpha, MarketWatch, CNBC, Seeking Alpha Currents).
2. **Sees earnings/legal/analyst/company catalysts?** Earnings ✅ (yfinance), legal ✅ (legal_risk gate), company news ✅. **Analyst actions ❌** (classified but not wired).
3. **Reaches LLM packet?** Company news ✅, earnings ✅, legal ✅. Analyst actions ❌, options/OI ❌ (don't exist).
4. **Reaches Telegram rationale?** ❌ Stocks Telegram does not show catalyst/earnings context explicitly (and `news_supported` flag is unset).
5. **Options/OI data at all?** ❌ None for stocks — only earnings + news.
6. **If options/OI missing, does it say "missing" honestly?** ⚠️ Earnings says "unknown — calendar lookup missing"; options/OI absence is **silent** (never stated).
7. **Stocks with catalyst vs without — trade better?** **Cannot measure** — `news_supported` is 0 on all 533 stocks signals (labelling gap #1). Fixing the label unlocks this analysis. (Crypto equivalent: catalyst +15R vs technical −3R — strong signal.)

## Bottom line

Pipeline is **working, not broken**. The high-value finding: **crypto catalyst-backed signals trade dramatically better (+15R vs −3R)** yet only ~21% of signals carry the flag, and **stocks catalysts are completely unlabelled**. The safe, high-EV next step is **labelling** (so the operator and future analysis can see catalyst quality), plus a derivatives **archive** — no scoring change without separate approval.
