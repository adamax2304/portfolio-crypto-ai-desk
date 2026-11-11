# Opus Enriched Review — Crypto Overnight / Asia Review — Auto Cycle 04:39 EEST

## 1. Executive Summary

Slot: **crypto overnight / Asia review** (04:30 EEST). Advisory only — no auto-trade, no scoring/threshold/routing changes. Stocks market is closed; treat stocks as planning/watchlist context only, crypto is the live actionable class.

Crypto regime reads local "range/chop, uptrend" on the desk's own indicators, but that sits inside a much heavier bearish backdrop confirmed via external search: BTC at a 4-month low (~$61k) on Iran/Hormuz tension and ETF outflows, and >50% down from its Oct 2025 ATH per a BlackRock note picked up overnight. Treat the intraday "uptrend" label as a local bounce, not a trend reversal. Macro/geopolitical risk score is 100/100 (Strait of Hormuz crisis, still active per external confirmation). Catalyst mapping is weak this run (74.6% unmapped) — use catalysts as context, not as the deciding factor. 20 crypto B-tier positions are open/entered-unresolved (0 A-tier active); two (HOLO, PROM) expire within ~1h of this review and need an operator glance. No untracked-alert integrity issues detected.

## 2. Data Used

- Reports: scalp (00:39, fresh), intraday (00:47, fresh), swing (2026-08-18 19:07, ~9.5h old → carry-forward), stocks intraday (01:15, fresh but market closed), stocks swing/invest (deprecated, last real data 2026-07-02 — excluded).
- `data/processed/llm_analysis_packet.md`, `data/processed/context_for_llm.md`, `data/processed/market_summary/last_update.json`.
- `data/catalysts/2026-08-19/catalyst_events.jsonl` (500 events), `narrative_baskets.jsonl` (4 baskets), `catalyst_cycle_00-52.md`.
- SQLite `db/crypto_ai_desk.sqlite`: `proposed_signals` (status/tier distribution, active B-tier detail), `news_items` (per-symbol catalyst verification, Telegram last-4h feed).
- CLI: `active-signals` (crypto 47 rows, stocks 50 rows), `signal-stats` (crypto + stocks), `detect_untracked_legacy_alerts` (0 findings).
- External: WebSearch ×3 (BTC/ETH Asia-session mood, ACE catalyst check, Strait of Hormuz status) + implicit fetch via search snippets — no dedicated WebFetch call was needed since search results were sufficiently sourced and dated.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-18_2325.md` (23:34 EEST cycle).

## 3. Scheduler / Data Freshness

- `data/scheduled_runs/2026-08-18_default_schedule/scheduler.log`: mtime **04:37 EEST** (2 min old) → scheduler actively running, not deferred.
- Latest cycle summary in that folder: `cycle_03_00-23_summary.md`, mtime **01:30 EEST** (~3h09 old) — inside the normal 2h cycle cadence window, not a stale-scheduler condition (defer rule requires BOTH scheduler.log and latest cycle summary >3h old; scheduler.log is fresh).
- A parallel `2026-08-19_default_schedule` folder exists with `scheduler.log` mtime 02:38 and no cycle summaries yet — looks like a same-day rollover artifact, not the active log; the 2026-08-18 folder is the one actively updating.
- Reports: scalp/intraday fresh (<1h), swing carry-forward (~9.5h, still usable per the 4–12h band), stocks intraday fresh but not tradable (market closed).
- Catalyst data fresh: generated 03:52 EEST (47 min old).
- No paper-portfolio/monitor status file was read this run (not in the allowed read set beyond active-signals/signal-stats) — status inferred from `proposed_signals` table directly.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-08-19 04:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh"], "data_missing": ["monitor/paper-portfolio status file"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 04:37", "cycle_03_00-23_summary.md mtime 01:30", "intraday report 00:47", "swing report 2026-08-18 19:07 carry-forward"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["chop", "risk_off", "mixed"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["internal regime label range/chop, BTC/ETH local uptrend", "altcoin breadth 48.7% above EMA20", "external: BTC 4-month low ~$61k, >50% off Oct 2025 ATH", "macro risk score 100/100"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["mapping_weak", "stale_catalyst", "no_catalyst", "fresh_catalyst"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 127/500 mapped (25.4%), unmapped 74.6%", "ACE Bitget PoolX/airdrop catalyst dated 2026-08-13 (6d stale)", "KORUB/GPS/SKHYB/BTW/HOLO/PROM: 0 news_items hits in last 24h", "XRP: primary-source Ripple/Jeonbuk Bank news, fresh"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["squeeze_risk", "funding_extreme", "oi_supports"], "data_missing": ["OI% for MEXC-fallback symbols (GPS, ACE, PUMP, HEMI, XPL, ZEC, PLUME, TUT — OI change n/a)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ACE funding -0.0018 across bybit/mexc, crowding elevated", "GPS funding -0.0001 to -0.0006 across venues, crowding moderate", "ETH price up + OI up = fresh positioning", "BNB price down + OI up = fresh shorts, squeeze risk if reclaimed"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["chase_risk", "entry_late", "overextended"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["KORUB -26.3% 24h, 4.0x volume, breakdown+overextended tags", "ACE +45.4% 24h (up from +29-33% at 23:34 review), still no fresh catalyst", "GPS +10.5% 24h, moderate extension", "EDEN already filled at prior cycle, hold not fresh entry"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["entered_unresolved", "needs_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["20 crypto B-tier ENTERED UNRESOLVED (status=triggered)", "0 crypto/stocks A-tier active", "HOLO expires 04:48 EEST (~9 min out), PROM expires 05:40 EEST (~1h out) — NEEDS REVIEW", "stocks: 0 A/B open, market closed, C-tier watchlist only (never actionable)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["headline_risk", "correlation_cluster", "reduce_risk"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["macro risk 100/100, risk-off headwind per system context", "20 open crypto longs mostly altcoin-beta correlated to BTC/risk mood", "Strait of Hormuz crisis externally confirmed ongoing (UAE/ADNOC vessel attacks)"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto_swing_narrative_rs_momentum 14d WR72%/PF5.80 (primary)", "crypto_intraday_catalyst_or_momentum no-catalyst variant WR23%/PF0.70 (weak)", "week actionable A/B crypto: n=81, WR21.5%, PF2.96, totalR +29.4", "weekend-mode weak signals underperform (WR18%, n=17)"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.7,
    "preferred_side": "mixed",
    "best_long_candidate": { "symbol": "GPS/USDT", "trigger": "hold above entry zone 0.01707-0.01755; only add on a clean retest, not a chase above 0.0180", "reason": "active B-tier swing long already triggered, RS+8-10% vs BTC, moderate (not extreme) extension, playbook crypto_swing_narrative_rs_momentum (14d WR72%/PF5.80); no fresh catalyst so treat as pure RS/momentum" },
    "best_short_candidate": { "symbol": "KORUB/USDT", "trigger": "wait for a failed retest/rejection back below the broken support (do not short the -26% move directly — already extended); invalidate on reclaim + close back above prior support", "reason": "cleanest weak_vs_market breakdown with 4.0x volume confirmation, no catalyst contradiction found (0 news hits), fits crypto_failed_bounce_short playbook (14d WR40%/PF2.00)" },
    "best_catalyst_candidate": { "symbol": "XRP/USDT", "trigger": "watch for RS vs BTC turning positive on continued volume (currently 2.08x average) with the Ripple/Jeonbuk Bank partnership news still fresh; no formal signal yet — confirmation-only", "reason": "only symbol this cycle with a primary-source, unambiguous catalyst (Ripple x Jeonbuk Bank cross-border payments, The Block) and no contradicting risk tag" },
    "avoid_candidate": { "symbol": "ACE/USDT", "reason": "chase risk: +45.4% 24h (up from +29-33% at the 23:34 review), catalyst (Bitget PoolX listing/airdrop) is 6 days stale, funding still deeply negative (-0.0018, elevated crowding) — same avoid call as the prior two reviews, now more extended, not less" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh | advisory_only |
| market_regime | caution | 0.70 | chop, risk_off, mixed | advisory_only |
| catalyst_narrative | caution | 0.75 | mapping_weak, stale_catalyst, no_catalyst, fresh_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.60 | squeeze_risk, funding_extreme, oi_supports | advisory_only |
| technical_entry | caution | 0.70 | chase_risk, entry_late, overextended | advisory_only |
| execution_lifecycle | ok | 0.85 | entered_unresolved, needs_review | advisory_only |
| risk_manager | caution | 0.70 | headline_risk, correlation_cluster, reduce_risk | advisory_only |
| playbook_performance | ok | 0.75 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader (synthesis) | caution | 0.70 | — | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-18_2325.md` (23:34 EEST):

- **EDEN/USDT** — still open/triggered (was the prior review's #1 long candidate). No status change since; still holding inside its plan, no fresh action needed.
- **ACE/USDT** — extension continued: was +29-33% 24h at 23:34, now **+45.4%**. Avoid-chase call from the prior review stands and is reinforced, not resolved. Funding remains deeply negative (crowded shorts) rather than normalizing.
- **MMT/USDT** — the prior review flagged this as a stale 6-day short to let expire without extending. It is still open (`status=triggered`, created 2026-08-12); no new information changes that call — still let it run to its existing invalidation/expiry, do not add to it.
- **New this cycle:** HOLO/USDT (expires 04:48, ~9 min from this review) and PROM/USDT (expires 05:40, ~1h out) — both were not called out in the 23:34 review and are now imminent expirations; flagged under NEEDS REVIEW below.
- **New this cycle:** KORUB/USDT breakdown (-26.3%, 4.0x volume) is a fresh top-mover not present in the prior review's landscape — added as this cycle's best short-watch.
- **Regime-label lag** (flagged as a risk in the prior review's §10) persists in a related form: the intraday report's "BTC trend: uptrend" label is technically correct for the very short term but is silent on the much larger context (BTC 4-month low, >50% off ATH) that only surfaced via external search this run. See §14 TODO.
- No new A-tier signals appeared in either crypto or stocks since the last review.

## 5. Catalyst Coverage

- Total catalyst_events today: **500**
- Mapped (symbol present): **127** (25.4%)
- Unmapped (null symbol): **373** (74.6%)
- Narrative baskets: **4**

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

Top 3 unmapped headlines:
1. "Ping An Good Doctor Announces 2026 Interim Results"
2. "South Korea's stock market opens sharply lower amid heavy selling in US tech shares"
3. "Gold gains on easing Fed rate hike hopes, physical demand" (WSJ)

None of these are crypto-relevant misses — the unmapped set this run skews toward macro/equities headlines the symbol resolver isn't expected to tag, which is a lower-severity version of the mapping gap than a missed crypto-specific catalyst would be. Still logged per the >50% rule.

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **chop, risk-off-leaning underneath a local bounce.** Internal regime label is "range/chop" with BTC/ETH "uptrend" and altcoin breadth ~48.7% (neutral). External search confirms a much heavier bearish context sitting underneath that local read: BTC at a 4-month low (~$61k) on Iran/Hormuz tension and ETF outflows, and >50% off its October 2025 all-time high per a BlackRock note. Macro/geopolitical risk score is 100/100, and the Strait of Hormuz crisis is externally confirmed still active (UAE accused Iran of new ADNOC-vessel attacks this week).
- Stocks mood: **closed** (04:39 EEST = ~21:39 ET prior day). No fresh RTH data this slot; C-tier watchlist only, never actionable per the standing stocks-intraday hardening rule.
- Dominant narrative: no single crypto narrative is running hot — AI (heat 40/100) and Memes (heat 30/100) are "mixed," RWA/L2/Gaming are quiet. Most of the session's real movers (KORUB, BTW, GPS, ACE, ALPINE, SKHYB) are catalyst-free technical/momentum moves, confirmed via direct `news_items` lookup (0 hits each in the last 24h).
- Preferred side now: **mixed / wait-for-trigger**, leaning toward the swing RS+momentum playbook (14d WR72%/PF5.80, the desk's one clearly edge-positive crypto cohort) over fresh intraday chases. No-catalyst intraday momentum is a weak cohort (WR23%/PF0.70) — don't over-weight it just because a coin is moving.
- Best long candidate: **GPS/USDT** (see §8) — trigger: hold/retest of entry zone, no chase.
- Best short candidate: **KORUB/USDT** (see §8) — trigger: failed retest, not the raw breakdown print.
- Best catalyst-backed candidate: **XRP/USDT** — real, primary-sourced news (Ripple × Jeonbuk Bank), not yet a formal signal; watch-only.
- What to avoid: **ACE/USDT** chase (see §9), and adding to the already-stale **MMT/USDT** short.
- What would change the view: a confirmed BTC reclaim of a higher local level with OI expansion (would upgrade crypto mood toward risk-on); a fresh, verified Strait of Hormuz de-escalation headline (would lower the macro risk score materially); catalyst mapping recovering above 50% would restore confidence in the catalyst layer as a primary decision input.

## 7. Candidate Deep Dives

### 7.1 GPS/USDT (crypto, B-tier swing, score 72.2, ENTERED UNRESOLVED / open)
- Filled zone 0.01707-0.01755, invalidation/stop 0.01649, TP1 0.01913, TP2 0.02019.
- 24h +10.5%, RS vs BTC +10.15%, volume 0.65x (not a volume-confirmed breakout — moderate conviction).
- Derivatives: negative funding across bybit/mexc/okx (-0.0001 to -0.0006), external cross-check shows "moderate" crowding — some short pressure already present, which is a mild tailwind if it continues to squeeze, but not extreme.
- No catalyst: direct `news_items` query returned 0 hits in 24h — pure RS/momentum, playbook `crypto_swing_narrative_rs_momentum`.
- Has price already reacted? Yes, position is filled; this is a hold/monitor, not a fresh-entry decision for the existing position. For *new* size, only on a clean retest of the zone, not a chase above 0.0180.
- Overextension check: +10.5% 24h against a 0.65x volume read is a moderate, not extreme, extension — lower chase-risk than KORUB or ACE.
- Aligned with market mood: partially — crypto mood is chop/risk-off-leaning, so this is a "small, RS-backed, not a market-wide risk-on bet" idea, not a green light to add size broadly.
- Invalidation: 0.01649 (stop), or a broad BTC breakdown that drags correlated alt-longs.

### 7.2 KORUB/USDT (crypto, top-mover, no formal signal — short-watch)
- 24h -26.3%, RS vs BTC -26.6%, volume 4.0x average — the most volume-confirmed move in the whole scan.
- Tags: weak_vs_market, volume_expansion, breakdown, overextended.
- Derivatives: "futures data unavailable" — no funding/OI cross-check possible; **data_missing** for the derivatives_squeeze agent on this name specifically.
- No catalyst: 0 `news_items` hits in 24h — pure technical breakdown.
- Has price already reacted? Yes — a -26% move has already happened; shorting the print now is chasing an extended move, not a fresh entry.
- Chase risk: **high** if entered at market; the actionable version of this idea is a failed-retest short (bounce into resistance that fails), not adding to the breakdown directly.
- What would invalidate: a reclaim and close back above the broken support level, or unusual volume reversing to the upside.
- Fits `crypto_failed_bounce_short` (14d WR40%/PF2.00) *if* entered on the retest, not the raw print.

### 7.3 ACE/USDT (crypto, B-tier swing, score 65.6, ENTERED UNRESOLVED / open — AVOID adding)
- Existing position: filled zone 0.2230-0.2306, stop 0.2138, TP1 0.2559, TP2 0.2728 — that existing plan is unaffected and not being second-guessed here.
- But the live top-mover print shows ACE now +45.4% 24h (was +29-33% at the 23:34 review) — the catalyst driving this (Bitget PoolX listing + 110,000 ACE airdrop, confirmed via external search) is dated **2026-08-13**, i.e. 6 days stale. Internal `news_items` has **zero** hits for ACE in the last 24h, confirming there is no fresh catalyst behind the latest leg up.
- Derivatives: funding -0.0018 across bybit/mexc — deeply negative, "crowding elevated" on the external cross-check. This is short-squeeze fuel, not a clean trend-continuation signal, and the desk's own prior two reviews already flagged this exact chase-risk pattern.
- Verdict: **do not add new size or chase this print.** The existing open position rides on its own plan; this is a note against treating the +45% headline as a fresh long trigger.

### 7.4 HOLO/USDT & PROM/USDT — imminent expirations (NEEDS REVIEW)
- **HOLO/USDT**: B-tier swing, score 70.6, entered zone 0.0822-0.0857, expires **2026-08-19T04:48:47+00:00** — roughly 9 minutes from this review's timestamp.
- **PROM/USDT**: B-tier swing, score 65.1, entered zone 2.489-2.591, expires **2026-08-19T05:40:03+00:00** — roughly 1 hour out.
- Both are already ENTERED (status=triggered), so an expiry here is a validity-window close, not a missed entry — display as **0R display / unresolved, no TP/SL before window** if it lapses without hitting stop/TP, never a bare "+0R" or "expired."
- No action item beyond operator awareness; the scanner/scheduler will continue to process these normally. Flagged here only so the next monitoring pass doesn't mistake a window-close for a bug.

## 8. Best Candidates Ranked

1. **GPS/USDT** — long-watch, hold existing entered position; add only on a clean retest of 0.0171-0.0175, not above 0.0180.
2. **KORUB/USDT** — short-watch, wait for a failed retest/rejection, not the raw -26% print.
3. **XRP/USDT** — catalyst-watch, real primary-source news (Ripple × Jeonbuk Bank), watch for RS vs BTC to turn positive before treating as actionable; no formal signal yet.
4. **EDEN/USDT** — carried-forward hold from the prior review, still open, no new decision needed (hold to TP1 0.0559 / invalidate <0.0460).
5. **ACE/USDT** — explicitly the avoid-chase candidate this cycle (see §7.3 and §9), included here only because it is the most-discussed name in the scan, not because it's a fresh trade idea.

## 9. Avoid / No Trade (this decision window only)

- **Chasing ACE/USDT** at +45.4% 24h — stale (6-day-old) catalyst, deeply crowded negative funding, same failure pattern the desk flagged in the last two reviews, now more extended.
- **Adding to MMT/USDT** — stale 6-day short (opened 2026-08-12), prior review already called this out to let expire without extension; nothing here changes that.
- **Shorting KORUB/USDT at market** — the -26% breakdown has already happened; only the failed-retest variant is actionable, not the raw print.
- This is a decision-window call only — scanning, candidate generation, tracking, and outcome recording all continue uninterrupted. Nothing here is a command to pause any part of the system.

## 10. Main Risks

- **Regime-label vs macro-context gap:** the intraday report's local "BTC trend: uptrend" read is technically accurate short-term but says nothing about the much larger bearish backdrop (4-month low, >50% off ATH, active Iran/Hormuz crisis) that only surfaced via external search this run. A review or operator consuming only the internal snapshot could misread the regime as more constructive than it is. This is a continuation of a pattern flagged in the prior review's risk section — see §14 TODO.
- **Correlation cluster:** 20 open crypto B-tier longs are mostly altcoin-beta positions; a broad BTC breakdown (plausible given the macro backdrop) would pressure most of them simultaneously, not just the weakest names.
- **Catalyst mapping weak (74.6% unmapped):** reduces confidence in using the catalyst layer as a primary filter this run; the news/catalyst read here leans more on direct `news_items` per-symbol queries than on the aggregate catalyst_events feed.
- **Derivatives data gaps:** several of tonight's biggest movers (KORUB, SKHYB, MUB) have "futures data unavailable," meaning the derivatives_squeeze agent could not evaluate crowding/funding on the names with the largest moves.
- **Weekend-mode underperformance pattern** (from `signal-stats`): weak-confidence weekend signals show WR 18% (n=17) — not directly relevant tonight (Wednesday) but worth keeping in view heading into the weekend.

## 11. Action Plan — next 4 hours

- Monitor the 20 open crypto B-tier positions for stop/TP proximity; no new entries recommended beyond the retest-only setups on GPS (long) and KORUB (short).
- Watch HOLO/USDT (expires ~04:48) and PROM/USDT (expires ~05:40) close out their validity windows; log outcome using the standard lifecycle vocabulary, not a bare "expired."
- Track XRP/USDT for RS-vs-BTC confirmation on the Ripple/Jeonbuk Bank catalyst before treating it as more than a watch item.
- Do not add to ACE/USDT or MMT/USDT.
- Re-check BTC regime as Europe opens (11:30 EEST slot) — if BTC reclaims a meaningful level with OI expansion, the "chop/risk-off-leaning" mood call should be revisited.

## 12. Final Verdict per Mode

- **Crypto scalp:** no open signals this cycle (all recent scalp entries already resolved); playbook remains low_confidence (14d WR12%/PF0.14) — no change to that standing caution.
- **Crypto intraday:** no-catalyst momentum names (KORUB, GPS, SKHYB, BTW, ALPINE) are watch-only per the weak no-catalyst intraday cohort (WR23%/PF0.70); treat any intraday-style entry on these as research-grade, not fully sized.
- **Crypto swing:** the desk's one clearly edge-positive crypto cohort (14d WR72%/PF5.80); GPS and EDEN both sit here and remain the highest-confidence holds/watches tonight.
- **Stocks (all modes):** market closed — C-tier watchlist only, never actionable. No forward-testable signal this slot.
- **Stocks position framework (shadow):** unchanged from the 19:09 shadow scan (5 open candidates: V, XOM, JNJ, COP, LLY) — shadow-only research, not reviewed further this cycle since stocks are closed and this is a crypto-focused overnight slot.

## 13. Sources

- [Crypto Price Prediction August 19, 2026: Bitcoin Eyes $64K, Ethereum Tests $1,900 and XRP Defends $1 Ahead of Fed Minutes](https://sundayguardianlive.com/business/crypto-price-prediction-august-19-2026-bitcoin-eyes-64k-ethereum-tests-1900-and-xrp-defends-1-ahead-of-fed-minutes-263681/) — Sunday Guardian, accessed 2026-08-19.
- [Bitcoin and ethereum prices today, Tuesday, August 18, 2026: Crypto prices mixed as Iran stalemate continues](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-tuesday-august-18-2026-crypto-prices-mixed-as-iran-stalemate-continues-155702632.html) — Yahoo Finance, 2026-08-18.
- [Fusionist (ACE) Explodes 86% as Bitget Catalyst Hits](https://www.openpr.com/news/4604931/fusionist-ace-explodes-86-as-bitget-catalyst-hits-alphapepe) — OpenPR, references Bitget PoolX listing dated 2026-08-13.
- [UAE accuses Iran of attacks on two ADNOC vessels in Strait of Hormuz](https://www.aljazeera.com/news/2026/8/14/uae-accuses-iran-of-attacks-on-two-adnoc-vessels-in-strait-of-hormuz) — Al Jazeera, 2026-08-14.
- [August 15, 2026 — Shipping faces more disruptions in the Middle East](https://www.cnn.com/2026/08/15/world/live-news/iran-war-trump) — CNN, 2026-08-15.
- Internal: `data/reports/intraday/2026-08-19_00-47_intraday_report.md`, `data/catalysts/2026-08-19/catalyst_events.jsonl`, `db/crypto_ai_desk.sqlite` (`proposed_signals`, `news_items`), `OPUS_ENRICHED_REVIEW_AUTO_2026-08-18_2325.md`.

## 14. Fix Requests / TODO

### TODO-catalyst-mapping-weak
- **issue:** Catalyst symbol-mapping coverage is weak again this run (127/500 mapped, 74.6% unmapped) — consistent with the recurring mapping-gap pattern already tracked in memory (`project_crypto_ai_desk_news_layer_hardening`, ~17% match rate observed previously).
- **evidence:** `data/catalysts/2026-08-19/catalyst_events.jsonl` — 373/500 events have no `symbol` field; top unmapped headlines are macro/equities items (Ping An Good Doctor, South Korea market open, gold/Fed) that the current resolver doesn't attempt to tag.
- **suggested manual fix:** revisit symbol resolver coverage for macro/equities-adjacent headlines, or explicitly scope the mapping-rate metric to crypto-relevant sources only so a genuinely irrelevant macro headline doesn't count against the same 50% threshold as a missed crypto catalyst.
- **priority:** medium
- **first observed (this thread):** 2026-08-19 04:39 EEST (recurring — see linked memory for earlier instances).

### TODO-regime-label-context-gap
- **issue:** The desk's internal regime label ("BTC trend: uptrend", regime "range/chop") does not surface the larger macro drawdown context (BTC 4-month low, >50% off Oct 2025 ATH, active Strait of Hormuz crisis) that is only visible via external search. A reviewer or operator relying solely on the internal snapshot could misjudge how bearish the backdrop actually is. The prior review (`OPUS_ENRICHED_REVIEW_AUTO_2026-08-18_2325.md`, §10) flagged a related regime-label-lag instance for stocks; this is the crypto-side analogue.
- **evidence:** `data/processed/context_for_llm.md` "BTC trend: uptrend" vs. external search results ("Bitcoin slides to 4-month low at $61k as Iran tensions weigh, ETF outflows continue" — Investing.com, in `news_items`) and BlackRock's "50%+ pullback" note (t.me/wublockchainenglish, 2026-08-19T01:37 UTC).
- **suggested manual fix:** consider adding a longer-horizon (e.g., 90-day) drawdown-from-ATH context line to the market-regime section of the intraday/swing reports so local trend labels are read alongside the larger drawdown context without requiring external search each review cycle.
- **priority:** low
- **first observed (this thread):** 2026-08-19 04:39 EEST.
