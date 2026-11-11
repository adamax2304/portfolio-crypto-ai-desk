# Opus Enriched Review — Late-Session Risk Review — Auto Cycle 21:39 EEST

## 1. Executive Summary

Slot: **late-session risk review** (21:39 EEST, 2026-07-23, ~5h into the RTH session that opened 16:30 EEST, ~1h20m before the 23:00 EEST close). **Advisory only — no auto-trade, no scoring/strategy changes.** Nothing new fired this cycle on either book: crypto's Top Trade Ideas section came back empty (no A-tier, no B-tier) and the crypto scalp report step **failed outright this cycle** (`OperationalError: database is locked` during the symbol-save step — see TODO-1), so the scalp view is running on the 12:48 snapshot (~9h stale). Stocks intraday is fresh (18:27 UTC / 21:27 EEST) and confirms the risk-off thesis carried from the pre-open and open-reaction reviews: **0 A/B-tier actionable candidates**, regime **risk_off/bias=short**, VIX 19.65, breadth above EMA20 **0.0%**. External search independently confirms today's driver: a Mag-7-led sell-off (Nasdaq −2.22%, S&P −1.44%, Mag-7 basket −5.27%) on AI-capex disappointment (GOOGL −5% premarket on capex guidance, TSLA capex commentary) plus oil crossing $100/bbl pushing yields up. The stocks book's best short-aligned name remains **AAPL** (raw A, score 90, short) — gated only by `liquidity_rvol_below_min` / `sector_confirmation_weak_or_unknown`, no legal flag, thematically aligned with the confirmed tech selloff. **MSFT**'s `securities_fraud` tag is now externally confirmed as a real, currently-pending class action (W.D. Wash., lead-plaintiff deadline Aug 11 2026) — AVOID stands. **UNH**'s DOJ tag is confirmed and escalating (antitrust + Medicare-billing-fraud probes both active per this week's reporting) — AVOID stands. **TSLA**'s `going_concern` tag could **not** be corroborated externally this cycle (search found capex/accounting-tweak scrutiny but no confirmed auditor going-concern opinion) — flagged as a possible stale/mistagged label, TODO-3, but the system gate is left untouched. All 17 crypto active-signal rows sit at **tp1_hit/tp2_hit** (partial-TP touched under the touch-based paper tracker — this is a known PnL-overstatement risk per prior audits, not a fresh entry signal); none are fresh or actionable tonight. Catalyst mapping remains weak (80.1% unmapped, cumulative today, essentially unchanged from the 80.4% seen at 18:39). **XLE has now been absent from both Top-Candidates and Rejected/Not-Ready for a third consecutive cycle** despite energy still reading "strong" in sector rotation (RS +10.89% vs SPY) — escalated to TODO-4 (high priority, was medium). Scanning, tracking, and monitors continue regardless of this review's caution stance.

## 2. Data Used

- Crypto reports: `2026-07-23_12-48_scalp_report.md` (mtime 15:48, ~5.9h old — **stale for scalp cadence**; this cycle's scalp step failed with a DB-lock error, see §D/§14), `2026-07-23_16-29_intraday_report.md` (mtime 19:29, ~2.2h old, cycle-fresh)
- Swing report: `2026-07-23_03-05_swing_report.md` (mtime 06:05, ~15.6h old — **stale, >14h band**, excluded from the final verdict, carry-forward context only)
- Stocks intraday: `2026-07-23_18-29_stocks_intraday_report.md` (data freshness 18:27 UTC / 21:27 EEST, ~12min old, fresh)
- Stocks swing/invest: last available `2026-07-02_13-0x` reports (~21 days stale, unchanged — TODO-2 carried forward, not used; framework is deprecated per project notes)
- Catalyst layer: `data/catalysts/2026-07-23/catalyst_events.jsonl` (3,000 cumulative rows across today's 6 scan cycles; 597 mapped / 2,403 unmapped = 80.1% unmapped), `narrative_baskets.jsonl` (3 baskets: perps_dex_narrative, rwa_narrative, momentum_breakout), latest scan `catalyst_cycle_16-32.md` (19:32)
- CLI (re-run fresh this cycle): `active-signals` (crypto ×17, stocks ×50), `signal-stats` (crypto n=173 reliable, stocks headline n=0 / C-tier n=183), `detect_untracked_legacy_alerts --since 2026-07-23` (clean — no untracked alerts)
- Cycle 3 scheduler summary (`cycle_03_19-17_summary.md`, finished 20:06): 66 ok / 1 failed step (crypto scalp report, DB lock), latency SLA report, market-intelligence health (0 open issues), paper-shadow A/B refresh, paper portfolio ledger refresh
- Direct SQL against `db/crypto_ai_desk.sqlite` (`news_items`): 48h scan for MSFT/TSLA/UNH — no fresh (<48h) single-name legal-news rows found for any of the three; the legal tags are standing/persistent flags, not fresh breaking news this cycle
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-23_1839.md` (18:39 EEST, US open reaction slot) — used for §4 comparison
- External (WebSearch, 5 queries this cycle): tech/AI-capex sell-off confirmation, UNH DOJ probe status, Verus-Ethereum bridge exploit detail, MSFT securities-fraud lawsuit status, TSLA going-concern status — see §13

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: 2026-07-23 20:06 (~1h33m old at read time) — not deferred (well under the 3h defer threshold)
- Latest cycle summary: `cycle_03_19-17_summary.md` (started 19:17, finished 20:06) — 66/67 steps ok, 1 failure (crypto scalp report — DB lock)
- Monitors: crypto pending monitor (pid 18412), MEXC canary (pid 12516), derivatives monitor (pid 21000), stocks monitor (pid 22796), telegram dashboard callbacks (pid 17420) — all reported "already running" / healthy in this cycle's summary
- Market intelligence health check (16:55 UTC this cycle): status **ok**, 0 new issues, all context sources (cross-exchange quotes, Deribit DVOL, SEC Form4, stablecoin pegs) reporting fresh
- Crypto intraday: ~2.2h old, within normal cadence. Crypto scalp: ~5.9h old (failed this cycle, running on stale snapshot) — flag for tonight's scalp-mode read
- Swing: ~15.6h old — stale (>14h), excluded from final verdict per policy
- Stocks intraday: ~12min old, fresh
- Stocks swing/invest: ~21 days stale — not used (TODO-2, unchanged; framework deprecated)
- Catalyst scan: latest cycle 19:32, fresh (<2h)

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-07-23 21:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["crypto scalp report this cycle (DB-lock failure, running on 12:48 stale snapshot)", "stocks swing/invest ~21d stale", "XLE root-cause absence from stocks top-candidates/rejected for a 3rd consecutive cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log 20:06 (~1.5h old)", "cycle_03 summary: 66 ok / 1 failed (scalp report DB lock)", "swing report mtime 06:05 (~15.6h, stale)", "catalyst file 3,000 rows / 80.1% unmapped"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.8,
      "reason_codes": ["risk_off", "shorts_preferred", "chop"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["stocks regime risk_off/bias=short, VIX 19.65, breadth 0.0% above EMA20, SPY/QQQ both confirmed downtrend", "crypto BTC trend transition_down, ETH range, altcoin breadth 43.6% above EMA20 (mixed), overall market regime range/chop (neutral)", "external: Nasdaq -2.22%, S&P -1.44%, Mag-7 basket -5.27%, oil > $100/bbl, 10y yields at 18-month high"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "catalyst_confirmed", "no_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["80.1% catalyst events unmapped today (597/3,000 mapped), essentially unchanged from 80.4% at 18:39", "GOOGL AI-capex + EU DMA fine externally confirmed today (Bloomberg/Yahoo)", "ONDO/XLM rwa_narrative basket fresh <24h, single_source (MEXC Ondo tokenized-stock listing)", "momentum_breakout basket (BANK/ZAMA/AIXDROP/AKE) is pure momentum, no confirmed catalyst"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.45,
      "reason_codes": ["squeeze_risk", "data_unavailable"],
      "data_missing": ["symbol-level squeeze-phase detail beyond aggregate distribution", "OI 24h change (n/a across crypto derivatives rows this cycle)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["intelligence layer squeeze_phase distribution: phase_2_squeeze_expansion=5, phase_4_unwind=7, phase_5_post_unwind_chop=71 (aggregate only)", "DEXE/USDT -45.3% 24h with funding -0.008135 (heavily negative) — crowded-short / squeeze-prone, not a clean fresh short"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["chase_risk", "entry_late", "stale_before_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto Top Trade Ideas: 0 A-tier, 0 B-tier this cycle — 'No active trade clears the desk threshold'", "stocks: 9 A-raw names all demoted to C on liquidity_rvol_below_min / sector_confirmation_weak_or_unknown — RTH volume/sector confirmation still lagging the technical score", "KAITO/USDT best crypto watchlist idea at 61.1/100, below active threshold, conditional pullback zone only"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["open_actionable", "review_shadow", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["17 crypto active-signal rows: 11 tp1_hit / 6 tp2_hit (all B-tier, OPEN actionable / partial-TP progressing — touch-based tracker, not literal closes)", "50 stocks active-signal rows: 25 triggered / 13 tp1_hit / 12 tp2_hit, 47 of 50 are C-tier (REVIEW/SHADOW, not Telegram-actionable), 3 legacy B-tier already tp2_hit", "untracked-alert detector clean (0 orphaned watchlist alerts)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.8,
      "reason_codes": ["legal_risk", "headline_risk", "reduce_risk", "manual_review"],
      "data_missing": ["fresh <48h news_items rows for MSFT/TSLA/UNH — all three legal tags are standing/persistent, not freshly-triggered this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["MSFT securities_fraud confirmed real via WebSearch (City of St. Clair Shores Police and Fire Retirement System v. Microsoft, W.D. Wash., No. 26-cv-02071, lead-plaintiff deadline Aug 11 2026)", "UNH DOJ probe confirmed real and expanding (antitrust/Claritev + Medicare Advantage billing-fraud, both active per this week's reporting)", "TSLA going_concern NOT corroborated externally this cycle — capex/accounting-tweak scrutiny found, no confirmed auditor going-concern opinion (TODO-3)", "GOOGL AVOID/MANUAL REVIEW carried forward (EU DMA fine + stale post-earnings setup, earnings calendar UNKNOWN)", "stocks_intraday_long_guard still actively blocking XOM/LLY longs — consistent with long-direction PF well below short-direction PF this week"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto headline (A/B): sample=173 reliable, winrate 25.6%, PF 1.771, totalR +37.0 — by mode: scalp PF 0.61 (losing, n=45), intraday PF 1.60 (n=82), swing PF 3.25 (best, n=46)", "stocks headline (A/B): sample=0 this week — zero actionable stocks trades fired, C-tier diagnostic PF 0.643 / winrate 2% (n=183, weak)"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "shorts",
    "best_long_candidate":     { "symbol": "KAITO/USDT", "trigger": "1h close and hold inside conditional pullback zone 1.020-1.034 with volume confirmation; score currently 61.1/100 (below active threshold) — do not enter pre-confirmation", "reason": "top-scored crypto watchlist idea this cycle (uptrend, RS +7.45% vs BTC, RR to TP1 1.84R); no fresh stocks long is available — all stocks longs (XOM/LLY) are actively guard-blocked this week" },
    "best_short_candidate":    { "symbol": "AAPL", "trigger": "RVOL clears liquidity_rvol_below_min gate and XLK/tech sector confirmation turns negative (currently sector_confirmation_weak_or_unknown); once both clear, breakdown-continuation short aligns with the confirmed AI-capex tech selloff", "reason": "raw A-tier, score 89.92, short, no legal/earnings flag (unlike MSFT/TSLA/GOOGL), thematically tied to today's externally-confirmed Mag-7 selloff, stocks short-direction backdrop remains structurally stronger than long-direction this week" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT", "trigger": "confirmed multi-source pickup on the MEXC tokenized-stock listing news (currently single_source, fresh <24h) plus a clean reclaim of the intraday range high with volume", "reason": "rwa_narrative basket primary, catalyst is real and recent (MEXC Ondo Tokenized Stock Trading Pairs launch, Jul 23 2026) but not yet cross-confirmed by a second independent source" },
    "avoid_candidate":         { "symbol": "MSFT", "reason": "externally-confirmed active securities-fraud class action (real, currently pending, lead-plaintiff deadline Aug 11 2026) stacked on top of an already-gated A→C demotion; manual review required, not a tradeable short despite the highest raw score (89.63/90) on the desk tonight" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.75 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | caution | 0.80 | risk_off, shorts_preferred, chop | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, catalyst_confirmed, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.45 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.65 | chase_risk, entry_late, stale_before_entry | advisory_only |
| execution_lifecycle | ok | 0.80 | open_actionable, review_shadow, needs_review | advisory_only |
| risk_manager | caution | 0.80 | legal_risk, headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.65 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | caution | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Comparing against `OPUS_ENRICHED_REVIEW_AUTO_2026-07-23_1839.md` (18:39, US open reaction slot):

- **New this cycle:** the crypto scalp report step failed with a DB-lock error (not seen at 18:39) — scalp view is now running on a ~5.9h-old snapshot instead of the normal ~2-3h cadence.
- **Confirmed/strengthened:** the risk-off / AI-capex-selloff thesis flagged at 18:39 is now externally corroborated with hard numbers (Nasdaq −2.22%, S&P −1.44%, Mag-7 −5.27%, oil >$100/bbl) rather than inferred from internal VIX/breadth data alone.
- **Legal-risk verification:** MSFT `securities_fraud` and UNH DOJ probe are both now externally confirmed as real and active (not done at 18:39, which only cited GOOGL/UNH from carried-forward context). TSLA `going_concern` could **not** be corroborated — new TODO-3.
- **Unchanged:** GOOGL remains AVOID/MANUAL REVIEW (stale post-earnings setup, unchanged). Catalyst mapping still weak (80.1% vs 80.4%, effectively flat). Crypto book still shows 0 fresh A/B setups. Stocks headline sample still 0 for the week.
- **Escalated:** XLE's absence from both Top-Candidates and Rejected/Not-Ready is now a 3rd-consecutive-cycle pattern (16:20 → 18:39 → 21:39) — raised from medium to **high** priority (TODO-4).
- **head_trader best-short pick unchanged** (AAPL/META-class tech names on liquidity/sector gates), best-long pick shifted from "track existing crypto B-tier exposure generically" (18:39) to a named, level-specific KAITO/USDT watch (this cycle's top-scored watchlist idea).

## 5. Catalyst Coverage

- Total catalyst_events today (cumulative, 6 scan cycles): **3,000**
- Mapped (non-null symbol): **597** (19.9%)
- Unmapped (null symbol): **2,403** (**80.1%**)
- Narrative baskets: **3** (perps_dex_narrative, rwa_narrative, momentum_breakout)

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

Top 3 unmapped headlines (sampled from today's cumulative file):
1. "First in Market: MEXC to List WOODUSDT Futures in Innovation Zone on Jul 22, 2026, 14:30 (UTC)"
2. "Adjustment to RIFUSDT Funding Rate Settlement Frequency [Jul 22, 2026, 16:05 (UTC)]"
3. "Adjustment to BNCUSDT Funding Rate Settlement Frequency [Jul 22, 2026, 16:05 (UTC)]"

(Pattern: most unmapped rows are exchange-ops notices — new-listing/funding-adjustment announcements — that the symbol resolver isn't picking up despite the ticker being present in the title. See TODO-2.)

## 6. Market Landscape

Crypto: BTC trend **transition_down**, ETH trend **range**, altcoin breadth 43.6% above EMA20 / 48.7% above EMA50 (mixed), overall regime **range/chop (neutral)**, recommended style "mean reversion or wait for clean breakouts." Strongest 24h movers: AKE/USDT (+26.9%), BANK/USDT (+36.6%), ZAMA/USDT (+33.0%) — all part of the no-catalyst `momentum_breakout` basket. Notable single-name risk: ETH-ecosystem exploit news (Verus-Ethereum bridge drained $7.54M for the second time in two months, externally confirmed) — sentiment-negative for ETH-adjacent DeFi, not a direct trade trigger for any book symbol.

Stocks: regime **risk_off / bias=short**, VIX 19.65 (up from 17.70 pre-open), breadth above EMA20 **0.0%**, SPY/QQQ both confirmed downtrend. Strongest sectors: energy (XLE, RS +10.89%), healthcare (XLV, +4.41%), financials (XLF, +3.15%) — all on the back of the oil spike and defensive rotation. Weakest: semiconductors (SMH, RS −7.31%). Driver externally confirmed: AI-capex disappointment (GOOGL −5% premarket on capex guidance, Mag-7 basket −5.27%) plus oil >$100/bbl pushing the 10y yield to an 18-month high.

### Market Mood / Risk Routing
- Crypto mood: **chop / mixed** (BTC transition_down, ETH range, altcoin breadth mixed — not a clean risk-off or risk-on read)
- Stocks mood: **risk-off** (regime label explicit, VIX rising, breadth 0%, confirmed externally)
- Dominant narrative: AI-capex-spending disappointment driving a Mag-7-led tech selloff, amplified by an oil-price shock (>$100/bbl) lifting yields
- Preferred side now: **shorts** (stocks tech names, once liquidity/sector gates clear) / **wait-for-trigger** (crypto — no clean side, chop regime)
- Best long candidate: KAITO/USDT — watch only, pullback zone 1.020-1.034, not yet active
- Best short candidate: AAPL — watch only, needs RVOL + sector confirmation, not yet active
- Best catalyst-backed candidate: ONDO/USDT — RWA/tokenized-stock listing narrative, single-source, needs cross-confirmation
- What to avoid: MSFT, TSLA, UNH (all legal/headline-risk gated to AVOID/MANUAL REVIEW), GOOGL (stale post-earnings setup), fresh DEXE/USDT shorts (crowded/squeeze-prone, already −45% 24h — chasing, not initiating)
- What would change the view: a second independent source confirming the ONDO listing catalyst; RVOL/sector confirmation clearing on AAPL or any of the other 8 gated tech shorts; BTC reclaiming trend structure to resolve the crypto chop read; TSLA going-concern tag either confirmed by a primary source or corrected

## 7. Candidate Deep Dives

### 1. KAITO/USDT (crypto, watchlist, long) — best long-watch
- Has price already reacted to the catalyst? No confirmed catalyst — pure technical/momentum setup (score 61.1, "no fresh verified catalyst detected").
- Is the setup chasing? Not yet — current price 1.040 sits above the conditional pullback zone (1.020-1.034); waiting for price to come back to the zone, not chasing the recent move.
- Retest / pullback structure? Yes — this is explicitly a wait-for-pullback playbook (`crypto_intraday_catalyst_or_momentum`, known failure mode: "no-catalyst intraday in chop is net-negative — needs RS-leader or breakout confirmation").
- Overextended? No — ATR 0.0308, current price 1.040 vs support 0.9691 / resistance 1.115, not >2 ATR from the entry zone.
- Would entry now be late? Entry now (at 1.040, above the zone) would be premature/chasing; wait for the pullback fill.
- Actionable level: 1h close and hold inside 1.020-1.034.
- Aligned with market mood? Marginally — crypto mood is chop/mixed, not a clean risk-on tailwind; this is a name-specific RS play, not a regime-aligned trade.
- Long, short, or wait-for-trigger? Wait-for-trigger long.
- Actionable now or after confirmation? After confirmation (pullback fill + volume).
- Invalidation: 1h close below 1.003.
- Chase risk? Low if the zone is respected; high if chased at current price.
- Catalyst confirmation/contradiction? None — technical-only, no catalyst present.

### 2. AAPL (stocks, watchlist, short) — best short-watch
- Has price already reacted to the catalyst? Yes at the sector level (Mag-7 basket −5.27% today, tech-wide AI-capex selloff, externally confirmed) but AAPL's own RVOL and sector-confirmation gates have not yet caught up to the technical score.
- Is the setup chasing? Not yet — it's gated out of actionability, not already extended into the move.
- Retest / pullback structure? N/A — this is a breakdown-continuation short thesis, not a pullback-long.
- Overextended? Not assessed vs EMA20 in this report; gate reasons are liquidity/sector, not extension.
- Would entry now be late? Entering now, ungated, would be premature — the system explicitly demoted it for missing confirmation.
- Actionable level: RVOL clears `liquidity_rvol_below_min` and XLK/tech sector confirmation turns negative.
- Aligned with market mood? Yes — directly aligned with the confirmed risk-off/short-preferred stocks mood.
- Long, short, or wait-for-trigger? Wait-for-trigger short.
- Actionable now or after confirmation? After confirmation (RVOL + sector).
- Invalidation: would invalidate if XLK/sector rotation turns positive or RVOL never confirms into the close.
- Chase risk? Moderate — it's one of nine similarly-gated mega-cap tech names; don't chase the first one that trips, wait for volume to actually show up.
- Catalyst confirmation/contradiction? Catalyst (AI-capex selloff) is externally confirmed and sector-wide, not AAPL-specific — no company-specific news found for AAPL itself tonight.

### 3. ONDO/USDT (crypto, catalyst-backed, long) — best catalyst-watch
- Has price already reacted to the catalyst? Basket-level yes (rwa_narrative flagged fresh <24h) but not independently verified at the single-name level this cycle.
- Is the setup chasing? Unclear without a fresh price read this cycle — treat as unconfirmed, not urgent.
- Retest / pullback structure? Not assessed this cycle (report used for catalyst detection only, not re-scored as a fresh trade idea).
- Overextended? Not assessed this cycle — TODO for the next intraday cycle to re-score ONDO given the fresh listing catalyst.
- Would entry now be late? Cannot say without a fresh technical read — flagged watch-only.
- Actionable level: second independent source confirming the MEXC Ondo tokenized-stock listing, plus a fresh technical re-score.
- Aligned with market mood? Independent of the broader risk-off mood — an idiosyncratic single-name catalyst.
- Long, short, or wait-for-trigger? Wait-for-trigger long (catalyst-backed).
- Actionable now or after confirmation? After confirmation.
- Invalidation: catalyst fails to cross-confirm, or basket is contradicted by a subsequent scan.
- Chase risk? Cannot assess without a fresh technical read this cycle.
- Catalyst confirmation/contradiction? Single-source only (t.me feed) — not yet cross-confirmed.

### 4. MSFT (stocks, avoid) — best avoid candidate
- Highest raw score on the desk tonight (89.63, short) but tier-demoted A→C for `active legal/headline risk (securities_fraud)`.
- Externally confirmed: real, currently-pending securities-fraud class action (W.D. Wash., No. 26-cv-02071; underlying allegation: Copilot/Azure monetization claims misled investors, stock dropped ~10% on Jan 29 2026; lead-plaintiff deadline Aug 11 2026).
- Verdict: **AVOID / MANUAL REVIEW REQUIRED** — do not treat as a clean short despite the score. Source + date cited in §13.

### 5. TSLA (stocks, needs review) — flagged for data-integrity follow-up
- Score 93 raw (18:06 report) / demoted A→C for `active legal/headline risk (going_concern)`.
- External search this cycle found capex-scrutiny and accounting-tweak commentary (2026 CapEx guidance ~$20B, "not probable" milestone classifications reported in June 2026 analysis) but **no confirmed auditor going-concern opinion** for Tesla in 2026 — the specific `going_concern` tag could not be corroborated.
- Verdict: system gate left untouched (AVOID stands per current pipeline behavior) but flagged as **possibly stale or mistagged** — see TODO-3. Do not originate a TSLA short on the assumption the going-concern flag is current without a human re-check of the source.

## 8. Best Candidates Ranked

1. **AAPL** (short-watch) — best risk-adjusted short-watch: highest clean (non-legal-flagged) raw score among the nine gated tech shorts, direct alignment with the externally-confirmed AI-capex selloff. Trigger: RVOL + sector confirmation clear.
2. **KAITO/USDT** (long-watch) — best crypto watchlist idea, defined levels, RR to TP1 1.84R once triggered. Trigger: pullback zone 1.020-1.034 fill + hold.
3. **ONDO/USDT** (catalyst-watch) — real, fresh, single-source RWA/tokenized-stock catalyst. Trigger: second-source confirmation + fresh technical re-score.
4. Runner-up short-watch: any of GOOGL/AMZN/META/PLTR/COIN/TSLA(ex-legal-flag)/QQQ/MSTR/AVGO — all raw A/B tech shorts on the same liquidity/sector gates as AAPL; AAPL is simply the cleanest (no legal flag) of the group.

No clean actionable trade exists on either book tonight — every candidate above is a **watch**, not a live entry.

## 9. Avoid / No Trade

This is a decision-window verdict only — scanning, tracking, and the scheduler continue regardless.

- **MSFT** — confirmed active securities-fraud litigation. AVOID.
- **UNH** — confirmed, escalating DOJ antitrust + Medicare-billing-fraud probes. AVOID.
- **GOOGL** — stale post-earnings setup (calendar UNKNOWN vs a confirmed earnings print), carried AVOID/MANUAL REVIEW from prior cycles.
- **TSLA** — going_concern tag unconfirmed externally; treat as MANUAL REVIEW pending human source-check (TODO-3), not a clean tradeable short tonight either way.
- **DEXE/USDT** — already −45.3% 24h, heavily negative funding (crowded short) — any fresh short here is a squeeze-risk chase, not a clean entry.
- **New crypto scalp entries generally** — this cycle's scalp report failed to run; do not treat the 12:48 snapshot as representative of current intraday scalp conditions.

## 10. Main Risks

- Crypto scalp report pipeline failure this cycle (DB lock) — scalp-mode read is stale by ~6h; if this recurs next cycle, scalp-mode should be treated as fully blind, not just stale (TODO-1).
- Touch-based paper PnL: all 17 active crypto signals show tp1_hit/tp2_hit status. Per standing project audit findings, `final_r = highest-TP-touched` overstates realized PnL vs realistic execution — do not read these as confirmed wins without checking the realistic-execution overlay.
- Catalyst mapping stuck at ~80% unmapped for at least three consecutive cycles today — catalyst-backed decision-making is running on a fifth of the available signal.
- Broad-based mega-cap tech short setup (9 names) is entirely gated by the same two conditions (RVOL, sector confirmation) — if those clear simultaneously near the close, expect a cluster of near-identical short triggers rather than one clean signal; avoid over-sizing into correlated tech shorts.
- Macro tail risk: oil >$100/bbl + rising 10y yields is a genuine cross-asset risk driver tonight, not isolated to tech — could pressure crypto risk appetite into the Asia session if it persists.

## 11. Action Plan — next 4 hours

- Watch AAPL (and the other 8 gated tech names) for RVOL/sector-confirmation clearing into the close; do not force an entry before the gate clears.
- Watch KAITO/USDT for a 1h close inside the 1.020-1.034 pullback zone; do not chase current price.
- Watch ONDO/USDT for a second independent source on the MEXC listing catalyst before treating it as tradeable.
- No new crypto scalp entries tonight given the stale/failed scalp report; wait for the next successful scalp cycle.
- Into the 23:15 post-close review: check whether XOM/LLY longs get unblocked by the rolling drawdown guard, whether the Mag-7 tech shorts confirmed or faded into the close, and whether tomorrow's Asia session shows crypto following stocks lower or decoupling.

## 12. Final Verdict per Mode

- **Crypto scalp:** NO TRADE — report failed this cycle, stale by ~6h. Wait for next cycle.
- **Crypto intraday:** WATCH ONLY — 0 A/B setups; KAITO/USDT best watchlist idea, not yet triggered.
- **Crypto swing:** CARRY-FORWARD ONLY — report >14h stale, excluded from live decisions.
- **Stocks intraday:** WATCH ONLY / MANUAL REVIEW for legal-flagged names — 0 A/B actionable; 9 tech shorts gated on liquidity/sector confirmation; MSFT/TSLA/UNH/GOOGL explicitly AVOID or MANUAL REVIEW.
- **Stocks swing/invest:** NOT USED — deprecated framework, data ~21 days stale.

## 13. Sources

- [Stock market today: Dow, S&P 500, Nasdaq sell off as rising oil prices, bond yields, and AI capex weigh — Yahoo Finance](https://finance.yahoo.com/markets/live/stock-market-today-thursday-july-23-dow-sp-500-nasdaq-oil-bonds-earnings-084444369.html) (Jul 23 2026)
- [US Stock Futures Fall as Alphabet, Tesla Lead Tech Losses, Oil Nears $100 — Bloomberg](https://www.bloomberg.com/news/articles/2026-07-23/us-stock-futures-drop-as-traders-focus-on-ai-spending-oil-jumps) (Jul 23 2026)
- [Google's extreme AI capex spending plans trigger a technical warning on the stock price — Yahoo Finance](https://finance.yahoo.com/markets/stocks/article/googles-extreme-ai-capex-spending-plans-trigger-a-technical-warning-on-the-stock-price-120952068.html) (Jul 23 2026)
- [UnitedHealth Group (UNH) Faces Wider DOJ Antitrust Probe As Claritev Review Expands — Yahoo Finance](https://finance.yahoo.com/healthcare/articles/unitedhealth-group-unh-faces-wider-221504204.html) (Jul 2026)
- [DOJ's criminal probe into UnitedHealth extends to Optum Rx, physician reimbursement — Fierce Healthcare](https://www.fiercehealthcare.com/payers/wsj-report-doj-interviewing-former-employees-about-medicare-billing-practices-unitedhealth) (Jul 2026)
- [Verus Ethereum Bridge hacked again for $7.54M after May exploit — crypto.news](https://crypto.news/verus-ethereum-bridge-hacked-again-for-7-54m-after-may-exploit/) (Jul 23 2026)
- [New Verus-Ethereum bridge attack drains $7.5 million through flaw used in May — The Block](https://www.theblock.co/post/409489/new-verus-ethereum-bridge-attack) (Jul 23 2026)
- [MSFT ALERT: Securities Fraud Class Action Launched Against Microsoft Corporation — August 11, 2026 Deadline — AccessNewswire](https://www.accessnewswire.com/newsroom/en/business-and-professional-services/msft-alert-securities-fraud-class-action-launched-against-micros-1187343) (Jul 2026)
- [MSFT Court News: Microsoft Class Action Lawsuit Alleges Securities Fraud on behalf of Investors with Losses — Morningstar/PRNewswire](https://www.morningstar.com/news/pr-newswire/20260714ny03471/msft-court-news-microsoft-class-action-lawsuit-alleges-securities-fraud-on-behalf-of-investors-with-losses) (Jul 14 2026)
- [Tesla's Own Auditors Say The Growth Narrative Is Currently 'Not Probable' — Seeking Alpha](https://seekingalpha.com/article/4908702-teslas-own-auditors-say-the-growth-narrative-is-currently-not-probable) (2026, date within article unverified — see TODO-3; does not itself confirm a going-concern opinion)
- Internal: `data/reports/intraday/2026-07-23_16-29_intraday_report.md`, `data/reports/stocks/intraday/2026-07-23_18-29_stocks_intraday_report.md`, `data/catalysts/2026-07-23/catalyst_events.jsonl`, `cycle_03_19-17_summary.md`, `active-signals`/`signal-stats` CLI output (this cycle)

## 14. Fix Requests / TODO

### TODO-1: crypto scalp report step failing with SQLite "database is locked"
- **issue:** This cycle's "crypto scalp report" scheduler step failed (exit=1, 268s) with `OperationalError: database is locked` inside `src/storage/sqlite.py:415 save_symbols`, mid-way through fetching BANK/USDT and ZAMA/USDT candles. Scalp-mode read is now ~6h stale as a result.
- **evidence:** `data/scheduled_runs/2026-07-23_default_schedule/cycle_03_19-17_summary.md`, step 12 ("[FAIL] crypto scalp report").
- **suggested manual fix:** investigate concurrent writer contention on `db/crypto_ai_desk.sqlite` during the scalp report's `save_symbols` call (likely colliding with the background monitors/derivatives writers running in the same window); consider WAL mode (if not already enabled) or a short retry/backoff around `save_symbols`.
- **priority:** high (this is the second time in recent cycles a report step has hit "database is locked" — see also step 39 in the same cycle summary, "stocks-intraday-post-trade-refresh skipped (non-fatal): database is locked").
- **first observed:** 2026-07-23 19:21 EEST (this cycle); non-fatal DB-lock skip also seen at 19:56 EEST same cycle (step 39).

### TODO-2: catalyst symbol resolver missing exchange-ops-style tickers
- **issue:** Catalyst mapping is stuck at ~80% unmapped across at least 3 consecutive cycles today (16:32, and prior cycles per earlier reviews). Sampled unmapped headlines are exchange-ops notices (new-futures-listing, funding-rate-adjustment announcements) where the ticker (e.g. WOODUSDT, RIFUSDT, BNCUSDT) is present in the title text but not being resolved to a symbol.
- **evidence:** `data/catalysts/2026-07-23/catalyst_events.jsonl` — 2,403/3,000 rows unmapped; sample titles include "First in Market: MEXC to List WOODUSDT Futures...", "Adjustment to RIFUSDT Funding Rate Settlement Frequency...".
- **suggested manual fix:** extend the catalyst symbol resolver's regex/entity-matching to recognize the `<TICKER>USDT` pattern common in exchange-ops announcement titles (currently likely tuned for prose-style news mentions, not exchange-notice formatting).
- **priority:** medium (persistent, degrades catalyst-backed decision quality, but the review already treats catalyst layer as context-only when this weak).
- **first observed:** carried forward from prior reviews (first flagged in memory as of the news_layer_hardening project); still unresolved as of 2026-07-23 21:39 EEST.

### TODO-3: TSLA "going_concern" legal-risk tag could not be externally corroborated
- **issue:** The stocks-intraday pipeline tags TSLA with `active legal/headline risk (going_concern)`, forcing a hard demotion to C-tier/AVOID. External search this cycle found capex-scrutiny and "milestones classified not probable" commentary but no confirmed auditor going-concern opinion for Tesla dated 2026.
- **evidence:** `data/reports/stocks/intraday/2026-07-23_18-29_stocks_intraday_report.md` line ~163 (`TSLA (short) (was A): score 93 · ... tier demoted A→C: active legal/headline risk (going_concern)`); WebSearch this cycle for "Tesla going concern warning auditor 2026" returned no primary-source confirmation.
- **suggested manual fix:** a human session should trace the `going_concern` tag back to its source record (likely in the legal/headline-risk registry table) and confirm the underlying evidence is current and correctly attributed to Tesla, not stale or mis-tagged from an older filing.
- **priority:** medium (does not currently cause a bad trade — the tag is conservative/AVOID-directionally-consistent with the risk_off regime — but an unverifiable legal tag undermines the credibility of the legal-risk gate generally).
- **first observed:** 2026-07-23 21:39 EEST (this cycle, first time this specific tag was independently checked).

### TODO-4: XLE (energy) absent from stocks Top-Candidates and Rejected/Not-Ready for 3 consecutive cycles
- **issue:** XLE was a clean A-raw catalyst pick (score 86.07, long, oil-shock-backed) at 16:20 EEST. Since then (18:39 and now 21:39), XLE does not appear in either §5 Top Candidates or §8 Rejected/Not Ready in the stocks-intraday report, even though §2 Sector Rotation still lists energy/XLE as "strong" (RS vs SPY now +10.89% at 21:39, up from the 18:39 read). This is now a persistent, reproducible pattern across 3 cycles, not a one-off.
- **evidence:** `data/reports/stocks/intraday/2026-07-23_18-29_stocks_intraday_report.md` §5/§8 (no XLE row in either), §2 (XLE listed strong); same absence pattern noted in the 18:39 review's TODO for the 18:06/15:30 reports.
- **suggested manual fix:** trace why XLE is being scored/considered upstream (it shows up in sector-rotation aggregation) but dropped before reaching either the Top-Candidates or Rejected/Not-Ready output stage — likely a filtering or pipeline bug specific to XLE's data path this session, not a scoring judgment (a rejected/gated XLE would still appear in §8).
- **priority:** high (escalated from medium — persistent 3-cycle pattern, and it's masking a real, externally-confirmed catalyst-backed sector move that the desk cannot currently act on or even see rejected).
- **first observed:** 2026-07-23 16:20 EEST (XLE last seen as a candidate); absence confirmed again at 18:39 and 21:39 EEST.
