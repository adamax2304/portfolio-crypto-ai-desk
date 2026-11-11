# Opus Enriched Review — late-session risk review — Auto Cycle 21:46 EEST

## 1. Executive Summary

**Slot: late-session risk review (advisory only / no auto-trade).** US cash session has ~1h14m left (close 23:00 EEST). Scheduler is fresh (`scheduler.log` 21:39 EEST, ~7 min old) — no defer. Crypto regime: **range/chop, neutral**, macro/geopolitical risk still pinned at **100/100** (Iran sanctions, Strait of Hormuz oil-tanker economics, Russia mobile-missile drills) — persistent risk-off overlay on a range-bound tape. Zero A-tier crypto signals; the book stays structurally **100% long** (headline PF 1.33, triggered winrate only 11% — touch-based capture, not a clean win rate; scalp bucket confirmed net-negative again, PF 0.09/-10.0R over 14d). **TRUMP/USDT — this cycle's best long candidate at 18:39 — has been demoted by the freshest intraday model run** (score fell 89.2→50.8, now C-tier **watchlist-only**, with a conditional re-entry zone 2.637-2.686 that sits **below** the still-open B-tier swing signal's waiting-entry zone (2.7908-2.8422, invalidation 2.7280) — the two model reads now disagree on where TRUMP is actionable; flagged for operator reconciliation, not a clean pick anymore. **TUT/USDT and ONG/USDT open-long contradictions are unresolved for a third+ consecutive cycle** — TUT's 24h move eased to -20.99%..-24.16% (was -29.5%..-29.6% at 18:39) but remains far beyond its ~2%-below-entry invalidation while status still reads "triggered"; ONG's bias=short tag persists (24h -11.16%..-14.91%) against its open long. With crypto the only asset class trading into the Asia session, resolving TUT before end-of-day carries more urgency than in earlier cycles. Stocks: regime **risk_on** (VIX 14.4, breadth 100% >EMA50) but the underlying report is now ~4h old (17:43 EEST) heading into the close; the rolling paper-R drawdown guard continues to demote every fresh A/B candidate to C (14d net -5.7R PF 0.39) — MU (93.4, genuinely bullish fresh news: Micron-rival IPO surge, Nvidia margin-pressure tailwind) stays **not actionable**, working as designed. Only two stocks positions are genuinely live this window: **COST** (open intraday short, triggered, expires tomorrow) and **MU** (waiting_for_entry, guard-capped C). Untracked legacy alerts unchanged at **4 today** (MOVR, HEMI×2, CHIP) — same recurring bug, no new ones this cycle. Catalyst mapping improved slightly to 70.9% unmapped (was 73.8%) but is **still weak — context only**. Today's scheduler folder now has one `cycle_*_summary.md` (partial improvement on last cycle's gap TODO). Scanning, tracking, and the scheduler continue regardless of this window's verdict.

## 2. Data Used

- Crypto scalp report: `data/reports/scalp/2026-08-28_17-52_scalp_report.md` (20:52 EEST, ~54m old — **fresh**)
- Crypto intraday report: `data/reports/intraday/2026-08-28_18-03_intraday_report.md` (21:02 EEST, ~44m old — **fresh**)
- Crypto swing report: `data/reports/swing/2026-08-28_15-23_swing_report.md` (18:23 EEST, ~3h23m old — **fresh** per band, but the oldest of the three crypto reports this cycle; no newer swing cycle has run since)
- Stocks intraday report: `data/reports/stocks/intraday/2026-08-28_14-43_stocks_intraday_report.md` (17:43 EEST, ~4h03m old — **carry-forward**, borderline stale heading into the close; no fresher cycle available)
- Stocks swing/invest reports: both dated 2026-07-02 (~57d stale, deprecated pipeline, excluded)
- `data/processed/llm_analysis_packet.md` (21:10 EEST, fresh), `data/processed/llm_stocks_packet.md` (17:47 EEST, carry-forward, matches stocks-intraday age)
- `data/catalysts/2026-08-28/catalyst_cycle_18-19.md` (21:19 EEST, **fresh**, 500 events scanned), `catalyst_events.jsonl` (2500 rows, span 01:37-15:05 UTC — see §5), `narrative_baskets.jsonl` (5 baskets)
- `reports/CONTEXT_FILTERS_STATUS.md` (17:36 EEST) — paper-routing filter/health status
- CLI: `active-signals --asset-class crypto` (50 rows), `active-signals --asset-class stocks` (50 rows), `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`, `detect_untracked_legacy_alerts --since 2026-08-28`
- Direct read-only SQL against `db/crypto_ai_desk.sqlite` `news_items` table for COST/Micron headline checks (§I legal/headline discipline)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-28_1839.md`
- **External web research not used this run** — internal reports, catalyst layer, and news_items were sufficient and internally consistent for every candidate reviewed; nothing here depended on an unverified external claim.
- **TradingView / manual chart check unavailable** — all technical reads taken directly from report-stated OHLCV/ATR/EMA/RS fields.

## 3. Scheduler / Data Freshness

- `scheduler.log`: 2026-08-28 21:39:29 EEST (~7 min old) — **fresh**.
- Today's scheduler folder (`2026-08-28_default_schedule`) now contains **one** `cycle_01_15-58_summary.md` (mtime 18:40 EEST) — partial resolution of the prior cycle-summary-gap TODO; still only one summary for the day so far, monitor whether more accumulate (see §14).
- Crypto scalp: 20:52 EEST — **fresh** (~54m).
- Crypto intraday: 21:02 EEST — **fresh** (~44m).
- Crypto swing: 18:23 EEST — **fresh** by the <4h band (~3h23m), but no newer swing cycle has produced since; borderline aging.
- Stocks intraday: 17:43 EEST — **carry-forward** (~4h old), the market has moved for 4 hours since this snapshot heading into the 23:00 EEST close.
- Stocks swing/invest: 2026-07-02 — **stale**, deprecated pipeline, excluded per prior audits.
- `reports/CONTEXT_FILTERS_STATUS.md` (17:36 EEST): paper routing config `context_filters_v1` **LOCKED**; stablecoin depeg NORMAL; cross-exchange consistency OK (BTC/ETH FULL_SIZE); all context-source health checks `ok`/`ok_provisional` except `stocks_options_import` (`disabled_no_current_file`, non-blocking). No reduce-only / paper-blocking condition active.
- No monitor-process-uptime file was read this run (not in the allowed CLI/read list).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-08-28 21:46 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["stocks-intraday report ~4h old heading into close", "catalyst_events.jsonl still lags current time by several hours despite fresher cycle_18-19.md"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 21:39", "stocks intraday report mtime 17:43 EEST", "one cycle_*_summary.md now present today vs none at 18:39 review"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["mixed", "chop", "risk_on", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto regime range/chop neutral, macro risk 100/100 unchanged", "stocks regime risk_on (as of 17:43 snapshot), VIX 14.40, breadth 100% >EMA50", "~1h14m left in US cash session"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["stale_catalyst", "mapping_weak", "no_catalyst", "narrative_supported", "fresh_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["70.9% unmapped in catalyst_events.jsonl (improved from 73.8%)", "SOL/USDT fresh primary-source catalyst (Schwab platform listing) reinforces existing open swing long", "momentum_breakout basket (DEXE/EDEN) explicitly no confirmed news catalyst", "no legal/headline risk found for COST or MU in news_items or catalyst_cycle_18-19.md"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["oi_supports", "funding_extreme", "data_unavailable"],
      "data_missing": ["no OI/derivatives read for TUT/USDT this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ONG/USDT negative funding across venues (bybit 1.25e-05, mexc -0.001538), crowding elevated — supports the bias=short tag against the open long", "TRUMP/USDT funding -0.00012905 (bybit fallback), crowding normal — not extreme either direction"] },
    { "agent": "technical_entry", "verdict": "bad", "confidence": 0.7,
      "reason_codes": ["entry_late", "price_moved_away", "stale_before_entry", "overextended"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TRUMP/USDT intraday model score fell 89.2->50.8, now C-tier watchlist with conditional zone 2.637-2.686 BELOW the open B-tier swing waiting-entry zone 2.7908-2.8422 — model disagreement on entry validity", "DEXE/USDT +26-28% 24h, >2 ATR from EMA20, do-not-chase flag persists", "TUT/USDT >2 ATR from EMA20 on both long and short reads, converted to watchlist-only (score 26.6)"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review", "closed_flat"],
      "data_missing": ["exhaustive book count beyond the 50-row CLI sample per asset class"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto 50-row sample: 39 OPEN actionable (triggered/running), 3 WAITING for entry (TRUMP, CHIP, RE), 8 partial-win running (TP1/TP2 hit)", "stocks 50-row sample: 1 OPEN actionable (COST short), 1 WAITING (MU), ~48 rows are past-expiry historical TP1/TP2-hit carryover from Aug13-26, effectively closed/resolved not live this window"] },
    { "agent": "risk_manager", "verdict": "bad", "confidence": 0.8,
      "reason_codes": ["manual_review", "correlation_cluster", "reduce_risk", "daily_loss_pressure"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TUT/USDT open long still 'triggered' after 3+ cycles despite invalidation almost certainly breached (24h -20.99%..-24.16% vs ~2% invalidation buffer)", "ONG/USDT bias-tag contradiction persists (-11.16%..-14.91%)", "crypto book still 100% long, 0 audited shorts", "late-session timing raises the cost of leaving TUT unresolved into the Asia session where crypto is the only live asset class"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["playbook_failing", "low_sample", "playbook_working"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto scalp weekly PF 0.09, avgR -0.0935, totalR -10.0 (worse than 18:39's -9.0R)", "crypto swing PF 1.69/+18.7R, intraday PF 1.43/+18.4R — both positive", "stocks headline A/B sample=10 confidence=weak winrate 75% PF=inf — too small to trust as proof, anecdotal only", "stocks C-tier sample=554 PF 0.40 losing, consistent with guard rationale"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.68,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "manual_review",
    "confidence": 0.68,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "TRUMP/USDT", "trigger": "model disagreement this cycle — do not chase the still-open B-tier waiting-entry zone (2.7908-2.8422) at face value; wait for either a fill confirmation there or a retest of the lower intraday-model zone (2.637-2.686) before adding size" },
    "best_short_candidate":    { "symbol": "TUT/USDT", "trigger": "not an audited short setup, only a bias/failed-bounce tag (score 26.6, watchlist-only, >2 ATR from EMA20) — confirm bearish HTF structure break + volume before promoting; the open LONG contradiction on this same symbol takes priority over any new short" },
    "best_catalyst_candidate": { "symbol": "SOL/USDT", "trigger": "already-open triggered swing long (entry ~96.0-96.6); reinforced this cycle by a fresh primary-source catalyst (Schwab adding SOL to its crypto platform); no contradicting risk tags" },
    "avoid_candidate":         { "symbol": "TUT/USDT", "reason": "open long unresolved for 3+ consecutive cycles against a still-deep 24h collapse; needs operator/monitor resolution, not a new position either direction" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.70 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | caution | 0.75 | mixed, chop, risk_on, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.60 | stale_catalyst, mapping_weak, no_catalyst, narrative_supported, fresh_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.55 | oi_supports, funding_extreme, data_unavailable | advisory_only |
| technical_entry | bad | 0.70 | entry_late, price_moved_away, stale_before_entry, overextended | advisory_only |
| execution_lifecycle | caution | 0.70 | open_actionable, waiting_for_entry, needs_review, closed_flat | advisory_only |
| risk_manager | bad | 0.80 | manual_review, correlation_cluster, reduce_risk, daily_loss_pressure | advisory_only |
| playbook_performance | caution | 0.75 | playbook_failing, low_sample, playbook_working | advisory_only |
| head_trader | caution | 0.68 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-28_1839.md`:
- **New this cycle — TRUMP/USDT demoted:** the 18:39 review's best clean long (RS-leader, score 89.2) now scores only 50.8 in the freshest intraday model run, C-tier watchlist-only, with a re-entry zone (2.637-2.686) sitting *below* the still-open B-tier swing waiting-entry zone (2.7908-2.8422). This is a new model-disagreement finding, not previously flagged.
- **Eased but still unresolved — TUT/USDT:** 24h move improved from -29.5%..-29.6% to -20.99%..-24.16% (partial bounce), but the open long (`sig_c7ce9835f38c40a8`) still shows status "triggered" rather than a resolved outcome; the core risk-manager concern from 18:39 stands unchanged.
- **Unchanged — ONG/USDT:** bias-tag contradiction continues (24h -11.16%..-14.91% across this cycle's reports vs -13.58% at 18:39, same order of magnitude), same open triggered swing long, no new information.
- **Unchanged — untracked alerts:** still 4 today (MOVR, HEMI×2, CHIP) — no new ones fired since the 18:39 review; same known bug (TODO-3).
- **Improved — cycle summary artifact:** today's scheduler folder now has one `cycle_01_15-58_summary.md` (mtime 18:40 EEST), where the 18:39 review found none at all — partial resolution, downgrading urgency on that TODO but not closing it (only 1 summary for a day that should produce several).
- **Improved — catalyst mapping:** 70.9% unmapped (was 73.8%), and this cycle's `catalyst_cycle_18-19.md` (21:19 EEST) is materially fresher than the 13:59 cycle used previously — still flagged weak, but trending better.
- **Reinforced — SOL/USDT:** a new primary-source catalyst (Schwab platform listing) adds to the already-clean catalyst thesis noted at 18:39; no change to the open position.
- **New context, not actionable — MU:** today's fresh news flow (Micron-rival IPO surge, Nvidia margin-pressure tailwind) is genuinely bullish for MU's thesis, but the guard still blocks it from being actionable; noted for completeness only.

## 5. Catalyst Coverage

- `catalyst_events.jsonl` (2026-08-28): **2500 total, 727 mapped (29.1%), 1773 unmapped (70.9%)**. **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (Improved from 73.8% unmapped at the 18:39 review.)
- Top 3 unmapped headlines: "JAPAN SHOULD NOT RAID ITS FOREX RESERVES..." (macro/FX), "JUDGE BLOCKS KEY PARTS OF TRUMP-BACKED RULE THAT WOULD RESTRICT MAIL-IN VOTING..." (US politics, ×2 near-duplicate headlines), "PHILIPPINE PESO FALLS AS MUCH AS 0.6%..." (macro/FX) — macro/political noise, not symbol-mapping regressions.
- `catalyst_events.jsonl` timestamp span: 2026-08-28T01:37-15:05 UTC (last event ~4-5h behind current time despite a 21:19 EEST file mtime) — the freshest content this cycle came from `catalyst_cycle_18-19.md` (500 events, generated 21:19 EEST) instead, used for §6/§7 narrative content.
- `narrative_baskets.jsonl` (5 baskets, all `<1h`-`<6h` fresh): rwa_narrative (ONDO/XLM), binance_ecosystem_teaser (BNB/ASTER), ai_narrative (NEAR/RENDER/TAO/FET), perps_dex_narrative (HYPE/DYDX/GMX/ASTER), momentum_breakout (DEXE/EDEN — explicitly no confirmed news catalyst).
- Legal/regulatory items in `catalyst_cycle_18-19.md` (REGN, PLAB, CCOI, AARD, BABA, HDB, DNOW, PNR, WIX, PRCT securities-fraud class-action notices) — none map to COST, MU, or any open crypto position this cycle; verified via direct `news_items` query, no contradiction found.

## 6. Market Landscape

**Crypto** (intraday report, 21:02 EEST / 18:00 UTC data): regime **range/chop, neutral**, altcoin breadth 47.9% >EMA20 / 72.9% >EMA50 (narrower than the 15:23 swing snapshot's 54.2%/77.1%). Macro/geopolitical risk unchanged at 100.0/100 (8 risk-off hits: Iran sanctions/oil-tanker economics, Russia mobile-nuclear-missile drill, XRP Ledger security audit noted as geopolitical-risk-tagged). Strongest: DEXE (96.1, +26.2% 24h, overextended/chase-risk), EDEN (93.7, +17.2%), CHIP (89.3, +8.1%), TRUMP (86.3, +5.6% — down from the 18:39 snapshot's momentum read), TST (85.1, +8.3%). Weakest/short-tag list: TUT (-20.99%, contradicts an open long), MOVR (-11.56%), ONG (-11.16%, contradicts an open long), ZRO (-9.46%), VET (-9.37%).

**Stocks** (intraday report, 17:43 EEST snapshot — ~4h old heading into the close): regime **risk_on**, bias long, VIX 14.40 (calm), breadth 75% >EMA20 / 100% >EMA50, 3/4 indices trending up. Rolling paper-R drawdown guard remains active (14d net -5.7R PF 0.39, 7d net -0.2R PF 0.49; would-have-been-A/B 14d: n=83, demoted=25, net -13.7R) and continues to demote every fresh A/B candidate to C. 0 actionable A/B this cycle (0 raw, 0 gate-demoted — nothing even reached the gate this run per §10 of the report); 45 A/B→C demotions logged from earlier in the day. Only genuinely live positions: COST (open intraday short) and MU (waiting_for_entry, C-tier).

### Market Mood / Risk Routing

- Crypto mood: **mixed / chop** (range-bound structure, macro risk-off overlay unchanged, RS-leader longs still doing the work but this cycle's best pick just got demoted)
- Stocks mood: **risk-on** per the last available snapshot (17:43 EEST) but data is aging into the close and the guard suppresses actionability regardless
- Dominant narrative: momentum-breakout (DEXE/EDEN, no confirmed catalyst) on crypto; RWA (ONDO/XLM), AI-sector rotation (NEAR/RENDER/TAO/FET), and perps-DEX (HYPE) baskets simmering; on stocks, no fresh actionable narrative this window (guard-capped)
- Preferred side now: **mixed, cautious** — crypto: hold existing RS-leader longs (SOL), do not chase TRUMP at either quoted zone until the model disagreement resolves; stocks: watch-only into the close, no new risk this late regardless of score
- Best long candidate: none newly clean this cycle — TRUMP/USDT is a hold/reconcile situation, not a fresh entry
- Best short candidate: none clean — TUT/USDT is the best short-watch bias tag, subordinate to resolving the open long on the same symbol
- Best catalyst-backed candidate: SOL/USDT (crypto, already-open swing long, reinforced by a fresh primary-source catalyst)
- What to avoid: new entries on TUT/USDT in either direction; chasing DEXE/USDT (+26% 24h, overextended); acting on the open B-tier TRUMP waiting-entry zone as if the intraday model's lower zone didn't exist; any stocks-intraday C-tier signal treated as actionable; any brand-new stocks risk this close to the 23:00 EEST close
- What would change the view: operator resolution of TUT/USDT and ONG/USDT; a fresh stocks-intraday cycle nearer the close; the stocks 7d/14d cohort turning positive to lift the guard; TRUMP/USDT's two model reads converging on one entry zone

## 7. Candidate Deep Dives

### 1. TUT/USDT (crypto, **open long contradiction — priority risk, 3rd+ consecutive cycle unresolved**, swing, B-tier score 69.2)
- Signal: `sig_c7ce9835f38c40a8`, status **triggered** (ENTERED, unresolved final outcome), entry 0.051638-0.052505, invalidation 0.050579, expires 2026-09-03.
- Has price already reacted? Yes, still — 24h -20.99% (18:00 UTC intraday snapshot) to -24.16% (17:45 UTC scalp snapshot); the magnitude eased versus the -29.5%..-29.6% seen at 18:39 (a partial bounce), but the position's invalidation buffer is only ~2% below entry, so price is almost certainly still through it.
- Is the setup chasing? N/A for the open long — the concern is the position itself.
- Retest/pullback structure? None stated on the long side; the intraday model has converted TUT to a watchlist-only short idea (score 26.6, ">2 ATR from EMA20; do not chase").
- Overextended? Yes, still >2 ATR from EMA20 per this cycle's report.
- Aligned with market mood? No — the open long remains unreconciled with the price action against it.
- Long, short, or wait-for-trigger? **Manual review required**, unchanged verdict — this is a monitor/outcome-recording question (was the stop hit and simply not recorded?), not a new-information question.
- What would invalidate it? Already should be invalidated per stated levels.
- Catalyst confirmation or contradiction? No TUT/USDT-specific catalyst found this cycle either; still a pure price/RS move.
- Derivatives: no OI/funding read available for TUT this cycle (`data_unavailable`).

### 2. ONG/USDT (crypto, open swing long, escalated manual-review carryover, unchanged)
- Signal: `sig_8d3a8fd71bf0bf75`, triggered 2026-08-26, invalidation 0.09240 — still ENTERED UNRESOLVED.
- This cycle's reports still tag ONG/USDT **bias=short**, 24h -11.16% (18:00 UTC) to -14.91% (17:45 UTC) — the same order of magnitude as the -13.58% seen at 18:39, contradiction persists, escalated HIGH since 2026-08-08.
- Derivatives support the bearish tag: negative funding across venues (bybit 1.25e-05, mexc -0.001538), crowding elevated — this is now the fourth+ consecutive review to find the open long unreconciled with a derivatives-confirmed bearish read.
- No new information beyond the continuing contradiction — carried forward as open, still-unresolved.

### 3. TRUMP/USDT (crypto, **model-disagreement finding this cycle** — was the 18:39 review's top long)
- Freshest intraday-model read (21:02 EEST): score 50.8/100, C-tier, **watchlist only** — "the evidence is not strong enough for an active trade." Conditional pullback zone 2.637-2.686, invalidation-if-activated 1.578 close beyond 2.578, RR 1.84.
- Still-open B-tier swing signal (`sig_872308a7ea6bb71c`, score 77.7, status waiting_for_entry): entry zone 2.7908-2.8422, invalidation 2.7280, expires 2026-09-04 — a **higher** zone than the fresh intraday model's conditional entry.
- 24h return eased to +5.58% (was +8.02% at 18:39); RS vs BTC +8.73%; funding -0.00012905 (not extreme), crowding normal.
- Would an entry now be late? Ambiguous — the two live model reads (swing vs intraday) do not agree on where "fresh" is, which is itself the finding this cycle.
- Aligned with market mood? Partially — still the least-bad long candidate in a chop regime, but no longer a clean pick.
- What would invalidate it? A 1h/4h close through 2.7280 (swing) or 2.578 (intraday-conditional), or BTC/ETH breaking the current range down.
- Catalyst confirmation or contradiction? None specific; RS/momentum only, unchanged from 18:39.

### 4. SOL/USDT (crypto, catalyst-backed, already-open swing long — reinforced this cycle)
- Signal: triggered swing long, entry ~96.0168-96.6490, invalidation 95.2440, expires 2026-08-31.
- New this cycle: a primary-source catalyst — Charles Schwab plans to add Solana (plus Avalanche, Chainlink) to its crypto platform (t.me/CoinMarketCapAnnouncements, verification=primary_source) — plus the previously-noted State-of-Solana platform launch and ETF-inflow tailwind (with the standing 20%-pullback historical caveat). No contradicting risk tags found.
- No new action required; existing swing long stands, thesis reinforced not weakened.

### 5. MU (stocks, long, intraday, best-scoring but guard-capped — bullish news context added)
- Raw score 93.4, status `waiting_for_entry`, entry 936.4727-943.4700, invalidation 929.4755, tier **C** (guard-capped from what would otherwise likely be A/B).
- Fresh news this cycle (via direct `news_items` query, all 2026-08-28): "Nvidia's margin pressure is Micron's revenue boost" (Motley Fool), "Micron benefits from Nvidia's margin pressure as memory demand reshapes AI supply chain" (CryptoBriefing), "Nvidia Just Validated Micron's Biggest AI Bull Case" (Finnhub) — genuinely constructive sector-level tailwind, no legal/headline risk found for MU.
- Actionable now or after confirmation? **Not actionable** regardless — the stocks-intraday rolling paper-R drawdown guard (14d net -5.7R PF 0.39) demotes every fresh A/B to C this window; C-tier is never Telegram-actionable per standing hardening.
- What would make it actionable? The guard's 7d/14d cohort recovering to a positive read, or an explicit operator override — not a price-level or news trigger.

## 8. Best Candidates Ranked

1. **TUT/USDT** (manual review, urgent, 3rd+ cycle) — open long contradicting a still-deep 24h collapse; resolve before any new action.
2. **ONG/USDT** (manual review, escalated, unchanged) — open long, derivatives-confirmed bias-tag contradiction persists.
3. **TRUMP/USDT** (reconcile, not a fresh entry) — two live model reads disagree on entry zone; do not act on either in isolation.
4. **SOL/USDT** (catalyst-watch, already open, reinforced) — fresh primary-source catalyst adds conviction to the existing swing long.
5. **MU** (stocks, watch-only) — highest raw stocks score this cycle (93.4), genuinely bullish news, but guard-capped to C; not actionable until the cohort clears.

## 9. Avoid / No Trade (this decision window only)

- **TUT/USDT — new entries either direction.** Open long needs operator resolution first.
- **Acting on the open TRUMP/USDT waiting-entry zone (2.7908-2.8422) as if it were still the cleanest read** — the fresher intraday model disagrees; reconcile before treating either zone as live.
- **Chasing DEXE/USDT at market** — +26% 24h, overextended.
- **New crypto scalp entries** — weekly PF 0.09, net-negative and worsening (-10.0R vs -9.0R at 18:39).
- **Any stocks-intraday C-tier signal treated as actionable** — MU and the rest of today's cohort are all guard-capped; none are Telegram-actionable.
- **Any brand-new stocks risk this close to the 23:00 EEST close** — insufficient time for a same-session thesis to play out.
- **ONG/USDT** — no new long or short action pending operator resolution.
- This is a decision-window verdict only — scanning, candidate generation, tracking, and the scheduler continue in all cases; nothing here recommends pausing any part of the system.

## 10. Main Risks

- **TUT/USDT open long, still unresolved for a 3rd+ consecutive review cycle** — invalidation almost certainly breached given the magnitude of the move (still -21%..-24% 24h against a ~2% buffer), status still reads "triggered." Urgency rising as the Asia session approaches and crypto becomes the only live asset class.
- **ONG/USDT bias-tag contradiction, unresolved, now derivatives-confirmed** (negative funding + elevated crowding support the bearish tag against the open long) — escalated HIGH since 2026-08-08.
- **TRUMP/USDT model disagreement** — the two live signals (swing waiting-entry vs fresh intraday watchlist) quote non-overlapping zones; treating either as authoritative without reconciliation risks a bad fill.
- **Crypto book remains 100% long, 0 audited shorts** — concentration risk if BTC/ETH break the current range down.
- **Crypto scalp underperformance deepening** — weekly PF 0.09, totalR -10.0R (was -9.0R at 18:39).
- **Stocks intraday data aging into the close** (~4h stale) — any close-into-the-bell price action is not reflected in this review's stocks read.
- **Catalyst mapping still weak** (70.9% unmapped), though trending better than 18:39's 73.8%.
- **4 untracked legacy crypto alerts today** (unchanged from 18:39) — known recurring bug, TODO-3, escalated HIGH 2026-07-17.

## 11. Action Plan — next 4 hours

- Escalate TUT/USDT for immediate operator/monitor check before the Asia session begins: confirm whether the position was actually stopped out and not recorded, given 3+ cycles of unresolved status against a clearly-breached invalidation level.
- Continue tracking ONG/USDT; no new action on the existing invalidation (0.09240).
- Do not act on TRUMP/USDT in either quoted zone until the swing/intraday model disagreement is reconciled by the next cycle.
- Hold SOL/USDT's existing swing long; catalyst thesis reinforced, no new action needed.
- No new stocks-intraday risk this close to the 23:00 EEST close regardless of score; re-check MU and the guard cohort at the next cycle (post-close final daily review, ~23:15).
- Watch COST's open intraday short into the close; no fresh operator input needed unless a stop/target is hit.
- No new crypto scalp entries this window (weekly PF 0.09, deepening losses).
- Re-check the untracked-alert count and TUT/ONG resolution status at the next cycle.

## 12. Final Verdict per Mode

- **Crypto scalp:** fresh (~54m); weekly PF 0.09 (losing bucket, worsening) — scanner continues, no new entries this window.
- **Crypto intraday:** fresh (~44m); TRUMP/USDT demoted to watchlist-only this cycle; no new A/B setups beyond the existing book.
- **Crypto swing:** fresh by band (~3h23m, oldest of the three crypto reports); TUT/USDT and ONG/USDT need manual review, not new action; SOL/USDT hold, reinforced.
- **Stocks intraday:** carry-forward (~4h old), 0 A/B actionable this cycle — guard-capped across the board; COST short remains the only genuinely open stocks position.
- **Stocks swing:** stale (2026-07-02) — excluded, deprecated pipeline.
- **Stocks invest:** stale (2026-07-02) — excluded, deprecated pipeline.

## 13. Sources

- Internal: `data/reports/intraday/2026-08-28_18-03_intraday_report.md`, `data/reports/scalp/2026-08-28_17-52_scalp_report.md`, `data/reports/swing/2026-08-28_15-23_swing_report.md`, `data/reports/stocks/intraday/2026-08-28_14-43_stocks_intraday_report.md`, `data/processed/llm_analysis_packet.md`, `data/processed/llm_stocks_packet.md`, `data/catalysts/2026-08-28/catalyst_cycle_18-19.md`, `data/catalysts/2026-08-28/catalyst_events.jsonl`, `data/catalysts/2026-08-28/narrative_baskets.jsonl`, `reports/CONTEXT_FILTERS_STATUS.md`, `db/crypto_ai_desk.sqlite` (`news_items` table, direct read query).
- CLI: `active-signals --asset-class crypto`, `active-signals --asset-class stocks`, `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`, `detect_untracked_legacy_alerts --since 2026-08-28`.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-28_1839.md`.
- No external WebSearch/WebFetch performed this run — internal sources were sufficient and consistent; dates present where used (all news_items rows carry `published_at`).

## 14. Fix Requests / TODO

### TODO-tut-invalidation-unresolved (carryover, escalating)
- **issue:** Open swing long `sig_c7ce9835f38c40a8` (TUT/USDT, entry 0.051638-0.052505, invalidation 0.050579) still shows status `triggered` for a 3rd+ consecutive review cycle, despite 24h prints of -20.99% (18:00 UTC), -24.16% (17:45 UTC) — an invalidation buffer of only ~2% below entry means price is almost certainly through it.
- **evidence:** `active-signals --asset-class crypto` row `sig_c7ce9835f38c40a8`; `data/reports/intraday/2026-08-28_18-03_intraday_report.md:48` ("TUT/USDT: bias short, 24h -20.99%"); `data/reports/scalp/2026-08-28_17-52_scalp_report.md:~50` (-24.16%); same pattern flagged at 18:39, 16:15, and earlier cycles.
- **suggested manual fix:** a human-driven session should query the exact current TUT/USDT price and the position monitor's state directly, confirm whether the stop was actually hit and simply not yet recorded as a `signal_outcome`, and if so investigate why the monitor didn't close/record it. Given this is now a multi-cycle-unresolved item heading into the Asia session, treat as time-sensitive.
- **priority:** high
- **first observed:** 2026-08-28 18:39 EEST (escalating; still open at 21:46 EEST)

### TODO-trump-model-disagreement (new)
- **issue:** TRUMP/USDT has two live, disagreeing model reads this cycle: the open B-tier swing signal (`sig_872308a7ea6bb71c`, waiting_for_entry, entry zone 2.7908-2.8422) and the freshest intraday model run (score 50.8, C-tier watchlist, conditional zone 2.637-2.686) — the intraday zone sits below the swing zone, meaning the two pipelines currently disagree on whether/where TRUMP is actionable.
- **evidence:** `active-signals --asset-class crypto` row `sig_872308a7ea6bb71c` vs `data/reports/intraday/2026-08-28_18-03_intraday_report.md` Trade Idea #4 (WATCHLIST ONLY TRUMP/USDT, entry plan "Conditional pullback zone: 2.637-2.686").
- **suggested manual fix:** a human-driven session should check whether the swing signal's entry zone is stale (computed at a higher price before the pullback) and whether swing/intraday pipelines should cross-check entry zones for the same symbol before both remaining live simultaneously.
- **priority:** medium
- **first observed:** 2026-08-28 21:46 EEST

### TODO-catalyst-window-gap (carryover, improving)
- **issue:** `data/catalysts/2026-08-28/catalyst_events.jsonl` events still lag current time by several hours (span 01:37-15:05 UTC vs a 21:19 EEST-ish mtime) despite the pipeline running fresher cycles (`catalyst_cycle_18-19.md`, generated 21:19 EEST). Improved from the 9h gap seen at 18:39, but the underlying rolling-buffer behavior is unchanged.
- **evidence:** direct read of first/last `timestamp` values across all 2500 lines in `catalyst_events.jsonl`; `catalyst_cycle_18-19.md` used instead for fresh narrative content in this review.
- **suggested manual fix:** unchanged from 18:39 — check whether `catalyst_events.jsonl`'s buffer size/rotation logic is capping it below the actual daily event volume, and whether mapped/unmapped % reported to Opus reviews should be computed from the latest `catalyst_cycle_*.md` cycle summary instead of the full-day jsonl.
- **priority:** medium
- **first observed:** 2026-08-28 18:39 EEST (still open, improving)

### TODO-cycle-summary-gap (carryover, partially resolved)
- **issue:** Today's `data/scheduled_runs/2026-08-28_default_schedule/` folder now has one `cycle_01_15-58_summary.md` (mtime 18:40 EEST), where the 18:39 review found none at all. Only one summary exists for the day so far despite the scheduler running multiple cycles (evidenced by scalp/intraday/swing reports at 5+ distinct timestamps today).
- **evidence:** `ls data/scheduled_runs/2026-08-28_default_schedule/*cycle*` — one file only; compare against 5 scalp reports, 5 intraday reports, and multiple swing/stocks reports generated today.
- **suggested manual fix:** a human-driven session should check whether cycle-summary generation is running once per scheduler restart rather than once per cycle, or whether it's silently failing on later cycles today.
- **priority:** low
- **first observed:** 2026-08-28 18:39 EEST (downgraded from "missing" to "partial" this cycle)

### TODO-untracked-alerts-recurring (carryover, still open, unchanged)
- **issue:** 4 untracked legacy crypto alerts today (MOVR/USDT 12:03, HEMI/USDT 14:39 + 15:28, CHIP/USDT 15:28) — same recurring watchlist-alert/signal-reuse bug escalated to HIGH priority 2026-07-17 (project memory: `project_crypto_ai_desk_watchlist_alert_signal_reuse_bug`). No new alerts since the 18:39 review.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-28` output (identical to the 18:39 review's run).
- **suggested manual fix:** see prior TODO-3 — investigate why these alerts reuse a stale/closed `signal_id` instead of minting a new `proposed_signal`.
- **priority:** high
- **first observed:** 2026-07-17 (recurring; observed again 2026-08-28 21:46 EEST)
