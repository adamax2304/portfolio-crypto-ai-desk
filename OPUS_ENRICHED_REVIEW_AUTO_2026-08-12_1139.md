# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:39 EEST

## 1. Executive Summary
Slot: **Europe / pre-US context (11:30 EEST)**. Advisory only — no auto-trade, no scoring/threshold changes. Crypto is range/chop with a macro risk-off geopolitical overlay (Houthi Red Sea attack, N. Korea missile test, Iran/Strait-of-Hormuz rhetoric); stocks regime is bullish/risk-on (VIX 15.3) but the **US CPI print lands today at 08:30 ET / 12:30 UTC / 15:30 EEST — ~4h from now, ~1h before the US cash open** — the single biggest risk event of this session. No A-tier ideas fired in either asset class this cycle; all fresh crypto ideas landed as C-tier watchlist only. Catalyst mapping is weak this run (71.7% unmapped) with a confirmed symbol-misattribution bug (CoreWeave earnings tagged as GOOGL/USDT). Route around CPI: size down / avoid fresh entries into the print, reassess at the 16:20 pre-US-open slot with the number known.

## 2. Data Used
- Reports: `2026-08-12_07-25_intraday_report.md` (crypto, ~1h old), `2026-08-12_07-15_scalp_report.md`, `2026-08-12_04-48_swing_report.md` (~4h, carry-forward), `2026-08-12_08-04_stocks_intraday_report.md` (~35min old)
- `data/processed/llm_analysis_packet.md` (07:25 UTC), `data/processed/llm_stocks_packet.md` (08:12 UTC)
- `data/catalysts/2026-08-12/` — catalyst_events.jsonl (1500 rows across 3 cycles), narrative_baskets.jsonl (4 baskets), catalyst_cycle_07-30.md
- CLI: `active-signals` (crypto n=50, stocks n=50), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-08-12` (clean — 0 untracked)
- 1 WebSearch (CPI release schedule) — internal data otherwise sufficient and fresh; no WebFetch needed.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-12_0448.md` (04:48 EEST, crypto-overnight slot)

## 3. Scheduler / Data Freshness
- `scheduler.log` mtime 11:30 EEST (fresh, <10min old at time of writing) — **not deferred**.
- Latest cycle summary `cycle_05_10-01_summary.md` mtime 11:30 EEST — fresh.
- Paper monitor status task ran clean this cycle (exit=0, Telegram sent).
- Stocks swing/invest reports are from 2026-07-02 (stale, >14h) — this is **expected**: the old stocks swing/invest playbooks are deprecated/removed per project design, not a data-freshness fault. Excluded from this review's actionable set.
- Untracked-alert detector: **0** — no signal-reuse integrity issue this run.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-08-12 11:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.9,
      "reason_codes": ["scheduler_fresh"], "data_missing": [], "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log + cycle summary both mtime 11:30 EEST", "stocks intraday report 35min old", "crypto intraday report 74min old", "0 untracked legacy alerts"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["mixed", "chop", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: range/chop, macro risk score 100/100 risk-off (geopolitical)", "stocks: bullish/risk-on, VIX 15.32, breadth 100% above EMA20/50", "CPI print 15:30 EEST today, ~1h before US cash open"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["fresh_catalyst", "mapping_weak", "no_catalyst"], "data_missing": ["accurate symbol resolution for stock-earnings-transcript sources"],
      "suggested_effect": "advisory_only",
      "facts_used": ["71.7% of 1500 catalyst_events today unmapped (symbol=null)", "binance_ecosystem_teaser basket fresh <6h", "momentum_breakout (PROM) fresh <1h, no confirmed news catalyst", "CoreWeave earnings headline mis-tagged as GOOGL/USDT"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["squeeze_risk", "funding_extreme", "oi_supports"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PROM/USDT funding -0.35% (shorts crowded, squeeze-supportive for longs), OI +47.2%", "TUT/USDT funding +0.034%, OI +4.2% while price down (fresh shorts pressing)"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["chase_risk", "price_moved_away", "entry_late"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PROM/USDT +25.5% 24h, price 2.807 above pullback zone 2.639-2.755", "TUT/USDT price 0.0742 below failed-bounce short zone 0.0757-0.0790, -24% 24h after +206% 7d"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["open_actionable", "no_entry", "review_shadow"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["50 open B-tier crypto signals (mostly triggered swing longs)", "0 fresh A/B this cycle — all 5 crypto ideas fell to C-tier watchlist", "0 current/compatible open A/B stocks intraday candidates (market closed)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["headline_risk", "legal_risk", "reduce_risk"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["REGN long demoted A→C: active class_action legal risk", "ISRG flagged block_requires_operator_review (FDA/competitive headline)", "CSCO earnings today, AMAT earnings tomorrow — swing-blocked", "HEI/USDT: 2 open long swing signals vs same-cycle short-bias reclassification (-25% 24h, overextended)", "CPI print in ~4h — reduce fresh-entry risk into the number"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["playbook_working", "low_sample", "playbook_failing"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing: PF 5.13, WR 22%, +45.4R (n=104, reliable) — primary lane healthy", "crypto scalp: PF 1.8 but avgR 0.03 (n=64) — known low-confidence lane", "stocks A/B headline: n=11 weak-confidence, PF 0.0, avgR -0.5 — too small to act on", "stocks C-tier watchlist: PF 0.23 (n=719) — expected for non-actionable research tier"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["mixed", "wait_for_trigger", "reduce_risk"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["no A-tier either asset class", "CPI print ~4h out, ~1h before cash open", "catalyst mapping weak (71.7% unmapped)", "PROM long-watch and TUT short-watch both have clear, un-triggered levels"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.7,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": { "symbol": "PROM/USDT", "trigger": "pullback into 2.639-2.755 on defended volume; invalidate on 1h close below 2.497", "reason": "top RS mover (+25.5% 24h, RS/BTC +26%), negative funding = crowded shorts / squeeze-supportive, but current price 2.807 is above the pullback zone — chasing now is late" },
    "best_short_candidate": { "symbol": "TUT/USDT", "trigger": "failed-bounce retest into 0.0757-0.0790 with rejection; invalidate on 1h close above 0.0830", "reason": "-24% 24h after a +206% 7d pump, fresh shorts pressing (OI+4.2%, funding+0.034%), price 0.0742 currently below the entry zone — wait for the bounce, don't chase the breakdown" },
    "best_catalyst_candidate": { "symbol": "BNB/USDT", "trigger": "wait for a clean pullback/consolidation after the AOS-2/Aster ecosystem teaser cools; do not chase the initial pop", "reason": "binance_ecosystem_teaser basket is fresh (<6h) but flagged single-source and sell-the-news / early-rotation risk" },
    "avoid_candidate": { "symbol": "REGN", "reason": "demoted A→C on active class_action legal risk — never actionable regardless of RR (1.92) or score (100)" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.90 | scheduler_fresh | advisory_only |
| market_regime | caution | 0.75 | mixed, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.60 | fresh_catalyst, mapping_weak, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.60 | squeeze_risk, funding_extreme, oi_supports | advisory_only |
| technical_entry | caution | 0.65 | chase_risk, price_moved_away, entry_late | advisory_only |
| execution_lifecycle | ok | 0.85 | open_actionable, no_entry, review_shadow | advisory_only |
| risk_manager | caution | 0.70 | headline_risk, legal_risk, reduce_risk | advisory_only |
| playbook_performance | ok | 0.75 | playbook_working, low_sample, playbook_failing | advisory_only |
| head_trader | caution | 0.70 | mixed, wait_for_trigger, reduce_risk | advisory_only |

## 4. What Changed vs Previous Review (04:48 EEST)
- Previous best long was GIGGLE/USDT (chase risk above 38.129); GIGGLE has dropped off the fresh-idea list this cycle — no longer surfaced as a top mover, still an open swing long (score 67.5) but not a fresh pick.
- Previous best short was ADA/USDT (open, tight invalidation 0.188434); ADA remains open (2 swing longs actually — one long, one short, from different dates) but is no longer the freshest short thesis. TUT/USDT is now the cleanest fresh short setup.
- New this cycle: TUT/USDT flipped from a pump narrative to a fresh failed-bounce short watchlist idea after -24% in 24h.
- Previous review's overall_verdict was `manual_review` / `wait_for_trigger`; this cycle upgrades slightly to `caution` / `wait_for_trigger` — no A-tier has fired all day, but the crypto swing lane continues to perform (PF 5.13).
- CPI print context is new information this cycle (not mentioned in the 04:48 review) — now the dominant near-term risk driver.

## 5. Catalyst Coverage
- Total catalyst_events today: **1500** | mapped (symbol present): **425 (28.3%)** | unmapped: **1075 (71.7%)**
- Narrative baskets: **4** (binance_ecosystem_teaser, delisting_thin_liquidity, ai_narrative, momentum_breakout)
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped/misattributed headlines observed:
  1. "CoreWeave Second-Quarter Results Top Estimates Amid Cloud Computing Demand" — **mis-tagged as GOOGL/USDT** (wrong symbol entirely; CoreWeave ≠ Google) — see §14 TODO.
  2. "Global Industrial (GIC) Q2 2026 Earnings Call Transcript" — ticker present in headline (GIC) but symbol field left null.
  3. "Tanger (SKT) Q2 2026 Earnings Call Transcript" — ticker present (SKT) but unmapped.

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **range/chop**, risk mode neutral, but macro overlay is risk-off (geopolitical: Houthi Red Sea attack, N. Korea missile test ahead of Aug 17-27 US-ROK drills, Iran/Strait-of-Hormuz rhetoric). Macro risk score 100/100.
- Stocks mood: **bullish / risk-on** pre-market (VIX 15.3, all 4 major indices in uptrend, breadth 100% above EMA20/50) — but this reading predates today's CPI print.
- Dominant narrative: binance_ecosystem_teaser (BNB/ASTER, fresh <6h, sell-the-news risk) and a pure-momentum breakout cluster (PROM/USDT +25.5%, no confirmed catalyst).
- Preferred side now: **wait-for-trigger** — crypto: selective RS-leader longs on pullback (PROM) or failed-bounce shorts on retest (TUT); stocks: planning-only until RTH confirmation, and specifically until the CPI print clears at 15:30 EEST.
- Best long candidate: PROM/USDT (crypto) — wait for 2.639-2.755 pullback; no clean stocks long yet (market closed, CPI pending).
- Best short candidate: TUT/USDT (crypto) — wait for 0.0757-0.0790 retest/rejection.
- Best catalyst-backed candidate: BNB/USDT ecosystem teaser — wait for cooldown, don't chase the pop.
- What to avoid: REGN (legal/class_action), ISRG (FDA/competitive headline, operator-review flagged), SMCI (stale post-earnings levels), chasing PROM at current price, chasing TUT's breakdown without a bounce.
- What would change the view: CPI print at 15:30 EEST (in ~4h) is the explicit trigger — reassess risk routing for both asset classes once the number and initial reaction are known (feeds directly into the 16:20 pre-US-open review).

## 7. Candidate Deep Dives

### 1. PROM/USDT (crypto, long-watch, C-tier/watchlist)
- Score 57.9 (low confidence), playbook `crypto_intraday_catalyst_or_momentum` (no-catalyst variant, 14d WR 23%/PF 0.70 — known weak lane on its own, but RS+funding context adds edge here).
- Has price already reacted to a catalyst? No — this is pure momentum/RS (+25.48% 24h, +40% 7d), no verified news catalyst; classified under the `momentum_breakout` narrative basket.
- Chasing? Yes at current price (2.807, above the 2.639-2.755 planned pullback zone).
- Retest/pullback structure? Yes — the plan explicitly wants the pullback zone before treating it as active.
- Overextended? Not yet >2 ATR from EMA20 per the report, but extended on the 24h/7d move.
- Would entry now be late? Yes.
- Actionable level: 2.639-2.755 with volume acceptance; invalidation 1h close below 2.497.
- Aligned with market mood? Partially — chop regime favors mean-reversion/pullback entries over breakout chases, which fits this plan.
- Direction: long. Actionable only after confirmation (pullback + volume), not now.
- Invalidator: 1h close below 2.497, or BTC/ETH breaking down against thesis.
- Chase-risk setup: yes if bought now.
- Catalyst confirmation/contradiction: no catalyst confirmed; funding is negative (shorts crowded) which is squeeze-supportive but not catalyst-backed.
- Two existing open long swing signals on PROM (entries 2.08-2.20 and 2.49-2.59) are both already in profit at current price 2.807 — the fresh idea is about adding/re-entering on a pullback, not the existing position.
- TradingView/manual chart check unavailable — using local OHLCV/ATR/EMA fields only.

### 2. TUT/USDT (crypto, short-watch, C-tier/watchlist)
- Score 62.1 (medium confidence), playbook `crypto_intraday_catalyst_or_momentum` (no-catalyst, same weak 14d lane — treat with caution).
- Has price already reacted? Yes — already down -24.06% in 24h (after +205.89% in 7d), so the move is underway; the idea explicitly wants a bounce back into resistance before shorting, not chasing the breakdown.
- Chasing? No if executed as planned — price (0.0742) is currently below the 0.0757-0.0790 zone.
- Retest/pullback structure? Yes, that is the entire thesis (failed bounce/retest short).
- Overextended? Downtrend already extended; watch for a further capitulation leg that voids the retest thesis.
- Actionable level: 0.0757-0.0790 with rejection; invalidation 1h close above 0.0830; targets 0.0670 / 0.0597 / 0.0525.
- Aligned with market mood? Yes — chop/risk-off macro overlay favors clean shorts on failed bounces over fresh longs.
- Direction: short, actionable only on the retest, not now.
- Chase-risk: only if shorted at current price without the bounce.
- Catalyst confirmation/contradiction: none — no fresh verified catalyst; derivatives show fresh shorts already pressing (OI +4.2%), so a squeeze back into resistance before further downside is plausible and consistent with the "wait for retest" plan.
- **Risk note**: 2 open long swing signals remain on TUT/USDT from the earlier pump (entries 0.036-0.037 and 0.123-0.143, expiring 08-14 and 08-16) — these are separate, older positions opened during the +206% 7d run and are a different question from this fresh short-watch idea; flagged for awareness, not a contradiction on their own (see §14 TODO for the more concrete HEI/USDT case).

### 3. BNB/USDT (crypto, catalyst-watch)
- Catalyst: binance_ecosystem_teaser basket (Aster AOS-2 launch, BNB/ASTER rotation), fresh <6h, single-source, playbook `related_beta_rotation`.
- Has price reacted already? 24h move only +1.56% per the derivatives snapshot — muted so far relative to the news, external funding neutral to slightly elevated (crowding=elevated per cross-check).
- Chasing? Not yet — no confirmed breakout, so waiting for confirmation is the correct posture.
- Actionable level: none scored this cycle (no A/B signal fired on BNB); treat as catalyst-watch only — confirm with a clean pullback or breakout with volume before considering size.
- Aligned with market mood? Marginal — chop regime plus single-source catalyst reporting raises early-rotation/sell-the-news risk explicitly noted in the basket.
- Catalyst confirmation/contradiction: single-source only — no independent confirmation yet.

### 4. REGN (stocks, avoid)
- Was A-tier by raw score (100, RR to TP1 1.92, structural tp1_source) but demoted A→C for **active class_action legal risk** plus `market_closed_intraday_planning_only` (US cash session not open yet).
- Legal/headline risk verified per demotion caps in the packet itself (internal, consistent, no external check needed).
- Final verdict: **AVOID / never actionable** regardless of technical quality, per the mandatory legal-risk demotion rule.

### 5. ISRG (stocks, manual review required)
- On the demoted near-A/B watch list (score 100, RR 1.5, healthcare, RS·SPY 3.24) with only `market_closed_intraday_planning_only` in the packet's own caps — but the production risk-warnings section separately flags **ISRG [fda_clinical]: block_requires_operator_review** (J&J's Ottava FDA approval as a competitive threat to Intuitive Surgical).
- Chasing/retest: not assessable pre-open; this is planning-only.
- Verdict: **manual review required** before treating as a clean pre-open watch candidate — the FDA/competitive headline needs a human read, not a clean pass-through to "watch."

## 8. Best Candidates Ranked
1. **PROM/USDT long-watch** — wait for 2.639-2.755 pullback, invalidate below 2.497. (crypto, momentum + squeeze-supportive funding, no catalyst)
2. **TUT/USDT short-watch** — wait for 0.0757-0.0790 retest/rejection, invalidate above 0.0830. (crypto, post-pump correction, fresh shorts building)
3. **BNB/USDT catalyst-watch** — wait for confirmation/pullback after the Aster ecosystem teaser cools, avoid chasing the initial pop. (crypto, single-source catalyst)
4. **BX (stocks, long-watch, planning only)** — RS·SPY 15.66, rr_to_tp1 1.5, financials, no legal/earnings flags in this cycle's data; confirm after CPI print and RTH open, not before.
5. No clean stocks catalyst-backed pick fires this cycle pre-open; COIN has a positive fresh Abu Dhabi tokenization-license headline but no scored signal — informational only, not a triggered candidate.

## 9. Avoid / No Trade (this decision window only)
- **REGN** — active class_action legal risk; never actionable this window regardless of score.
- **SMCI** — stale post-earnings levels (verified earnings print 2026-08-11T21:47 UTC, calendar shows UNKNOWN); needs fresh post-earnings levels before any plan is usable.
- **Chasing PROM/USDT at 2.807** — above the planned pullback zone; late entry.
- **Chasing TUT/USDT's breakdown below 0.0742** — the plan requires a bounce/retest, not shorting the move that already happened.
- **Any fresh stocks intraday entry into the CPI print** — market closed anyway pre-open, but this extends into the immediate post-open window too; prefer RTH confirmation after the number is digested.
- This is a decision-window call only — scanning, tracking, and outcome recording all continue uninterrupted.

## 10. Main Risks
1. **CPI print at 15:30 EEST (08:30 ET), ~4h from now, ~1h before the US cash open** — the dominant risk event of the session for both asset classes; can invalidate the current bullish-stocks/chop-crypto read within the hour.
2. **Catalyst mapping weak (71.7% unmapped)** and at least one confirmed misattribution (CoreWeave earnings → GOOGL/USDT) — treat catalyst layer as context only this run, not confirmation.
3. **Macro risk-off geopolitical overlay** (Red Sea, N. Korea, Iran/Hormuz) sitting underneath a chop crypto regime — headline risk can move BTC/majors abruptly.
4. **HEI/USDT**: 2 open long swing signals sit against a same-cycle fresh short-bias reclassification (-25% 24h, "do not chase," `crypto_failed_bounce_short` playbook) — worth a manual check on whether invalidation levels (0.183234 / 0.187505) have been breached (see §14).
5. **Stocks A/B headline sample is tiny and negative** (n=11, PF 0.0, avgR -0.5) — too small to read as a trend, but do not lean on stocks A/B tier for size this week without more data.
6. **CSCO earnings today, AMAT earnings tomorrow** — both swing-blocked; avoid chasing either into/around the print.

## 11. Action Plan — next 4 hours
1. Hold current crypto swing book (PF 5.13 lane, 50 open B-tier positions) — no new entries needed to defend it; playbook is working.
2. Watch PROM/USDT for a 2.639-2.755 pullback with volume acceptance before adding/re-entering long.
3. Watch TUT/USDT for a 0.0757-0.0790 retest/rejection before considering a short; do not chase the current breakdown.
4. Do not initiate any new stocks intraday position before the CPI print (15:30 EEST) — stocks market is closed anyway until 16:30 EEST.
5. Re-run/refresh context at or shortly after the CPI print for the 16:20 pre-US-open decision review; that review should explicitly reconcile the pre-CPI bullish-stocks read against the actual print.
6. Manually spot-check HEI/USDT's two open long invalidation levels against current price given the -25% 24h move (see §14 TODO-2).

## 12. Final Verdict per Mode
- **Crypto scalp**: no trade this cycle — 0 fresh ideas, known weak playbook (PF 1.8, avgR 0.03); hold existing tp1_hit legacy scalps to their process, no new entries.
- **Crypto intraday**: watch-only — PROM (long) and TUT (short) both need confirmation before being actionable; no fresh A/B fired.
- **Crypto swing**: hold — the healthy lane today (PF 5.13, WR 22%, +45.4R reliable sample); no new entries flagged this cycle, let the 50 open positions play out per their own invalidations/expiries.
- **Stocks intraday**: planning-only until RTH — market closed, CPI print pending; BX is the cleanest watch name, REGN is avoid, SMCI/ISRG need fresh levels or manual review before actionability.
- **Stocks swing/invest**: not applicable — playbooks deprecated/removed; `stocks_swing_growth_breakout` remains shadow-only research, not actionable.

## 13. Sources
- [US CPI Report August 2026: Date, Time & What to Expect](https://www.financecalendar.com/event/us-cpi-report-august-2026/) — CPI release confirmed for 2026-08-12, 08:30 AM ET.
- Internal: `data/reports/intraday/2026-08-12_07-25_intraday_report.md` (2026-08-12 07:25 UTC)
- Internal: `data/reports/stocks/intraday/2026-08-12_08-04_stocks_intraday_report.md` (2026-08-12 08:04 UTC)
- Internal: `data/processed/llm_analysis_packet.md`, `data/processed/llm_stocks_packet.md`
- Internal: `data/catalysts/2026-08-12/catalyst_cycle_07-30.md`, `catalyst_events.jsonl`, `narrative_baskets.jsonl`

## 14. Fix Requests / TODO

### TODO-catalyst-symbol-misattribution
- **issue:** Catalyst symbol resolver mis-tags a non-matching headline with a wrong ticker, and separately leaves tickers-in-headline unmapped. Confirmed example: "CoreWeave Second-Quarter Results Top Estimates Amid Cloud Computing Demand" (Finnhub company-news) is tagged as **GOOGL/USDT** — CoreWeave is not Google. Additionally 71.7% of today's 1500 catalyst_events (1075 rows) have symbol=null, including several where the ticker is plainly present in the headline text (e.g. "Global Industrial (GIC) Q2 2026 Earnings Call Transcript", "Tanger (SKT) Q2 2026 Earnings Call Transcript", "GXO (GXO) Q2 2026 Earnings Call Transcript", "Fortune Brands Innovations (FBIN) Q2 2026 Earnings Call Transcript").
- **evidence:** `data/catalysts/2026-08-12/catalyst_cycle_07-30.md` "Top catalysts by importance" section, entries `0.73 GOOGL/USDT [earnings_event] CoreWeave Second-Quarter Results...` and `0.73 GOOGL/USDT [earnings_event] CoreWeave jumps 10%...`; unmapped-sample query over `data/catalysts/2026-08-12/catalyst_events.jsonl`.
- **suggested manual fix:** Audit the symbol resolver for the earnings-call-transcript source path (looks like a fixed/stale symbol is being applied instead of extracting from headline); add a `(TICKER)`-in-headline extraction regex for the Finnhub/PR-Newswire earnings-transcript source pattern; stop appending `/USDT` to plain equity tickers when the source is a stocks feed.
- **priority:** high — this is an active misattribution, not just missing coverage, and it degrades the "Top catalysts by importance" ranking used in this review's own §5/§6 sourcing.
- **first observed:** 2026-08-12 11:39 EEST (this run); catalyst-mapping weakness generally has prior history — see `project_crypto_ai_desk_news_layer_hardening` memory (17% symbol-match audit).

### TODO-hei-open-long-vs-fresh-short-bias
- **issue:** HEI/USDT carries 2 open long swing signals (score 69.9, entry 0.185987-0.194373, invalidation 0.187505, expires 2026-08-15; score 65.2, entry 0.197794-0.209706, invalidation 0.183234, expires 2026-08-14) while this same cycle's fresh scan independently classifies HEI/USDT as a short candidate (score ~32, bias=short, 24h -25.06%, "Price is more than 2 ATR from EMA20; do not chase", routed to `crypto_failed_bounce_short` playbook). This is the same category of issue previously escalated for ZBT/ACE on 2026-08-08 (open longs tagged bias=short with negative 24h, 3 consecutive reviews).
- **evidence:** `data/reports/intraday/2026-08-12_07-25_intraday_report.md` lines 48, 579, 628 (HEI/USDT bias short, -25.06% 24h, score 31.9); `python -m src.cli active-signals --asset-class crypto` output showing 2 open HEI/USDT long swing rows with invalidations 0.187505 / 0.183234.
- **suggested manual fix:** Pull current HEI/USDT price and confirm whether either invalidation (0.187505 or 0.183234) has already been breached given the -25% pullback; if breached, investigate why the position hasn't auto-closed (stalled invalidation-check job vs a genuinely-not-yet-breached price). Separately, re-check whether the earlier ZBT/ACE bias-tag-contradiction fix regressed or was never generalized beyond those two symbols.
- **priority:** high — directly affects whether an open position's stated risk (invalidation level) is still valid.
- **first observed:** 2026-08-12 11:39 EEST (this run); prior occurrences 2026-08-08 (ZBT, ACE) per `project_crypto_ai_desk_bias_tag_contradiction` memory.
