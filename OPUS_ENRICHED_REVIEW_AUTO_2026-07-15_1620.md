# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:20 EEST

## 1. Executive Summary

Slot: **pre-US-open decision review** (16:20 EEST / 09:20 ET, 2026-07-15 — cash open at 16:30 EEST/09:30 ET, i.e. this read lands right at the bell). **Advisory only — no auto-trade, no code/scoring/routing changes.** Stocks pre-market stays **risk_on** (VIX 16.4, breadth 75%/100%) and external futures confirm it going into the open (SPY premarket +0.25% at $753.68, S&P fut +0.15%, Nasdaq fut +0.40% — cooler June PPI just reduced Fed-hike odds), but the whole session sits under an unresolved Iran/Strait-of-Hormuz overlay (oil >$85, fresh US strikes, blockade threats) that keeps crypto macro risk at 100/100 risk-off and is the single biggest gap-risk factor for stocks too. The same pre-gate-A stocks basket from the 11:30 review (JPM, META, XLF, NVDA, PLTR, GOOGL, AMZN, COIN) is still sitting on `market_closed_intraday_planning_only` — every one of them needs a fresh RTH-confirmed level at/after 16:30 EEST before being actionable; none is actionable right now. GOOGL now carries a genuine fresh catalyst (Buffett/Berkshire disclosed an Alphabet stake, CNBC/Yahoo, today) on top of its RS score. JPM stays a contradiction case (highest raw score, but post-earnings-stale). UNH stays AVOID (confirmed DOJ probe + earnings tomorrow 07-16; NFLX earnings tomorrow too — no chasing either into the print). Crypto is unchanged chop/risk-off-overlay with no A-tier and thin B-tier (KAITO/XEC long-watch, DEXE short-watch, still not retested). Two untracked legacy crypto alerts (FF/USDT carried over, LTC/USDT new) and the catalyst-mapping rate (81.1% unmapped today) are logged as TODOs, not fixed.

## 2. Data Used

- Reports: `2026-07-15_12-13_scalp_report.md`, `2026-07-15_12-19_intraday_report.md`, `2026-07-15_12-54_swing_report.md` (crypto, all <1.5h old); `2026-07-15_12-33_stocks_intraday_report.md` (stocks, ~1h old, generated pre-open — "MARKET CLOSED — planning/watchlist only" banner, as expected for this slot). Stocks `swing`/`invest` reports last `2026-07-02` (>14h, **stale**, deprecated legacy playbooks per project memory — excluded from verdicts).
- Internal `news_items` / `catalyst_events.jsonl` / `narrative_baskets.jsonl` for `2026-07-15` (direct reads, no scoring touched).
- CLI: `active-signals` (crypto ×21, stocks ×50), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-07-15`.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-15_1130.md` (Europe/pre-US context slot, 5h ago) — used for §4 comparison.
- **External web research performed** (internal-first check found the pre-open futures/gap-risk picture — not covered by any internal report, which is inherently pre-open/stale by definition for this slot — so ran WebSearch + one WebFetch per §G):
  - WebSearch: "S&P 500 futures pre-market July 15 2026 Iran Strait of Hormuz" (result: SPY premarket +0.25% at $753.68, cooler June PPI -0.3% vs flat expected, Polymarket pricing a higher open).
  - WebFetch: Benzinga pre-market wrap (result: S&P fut +0.15%, Nasdaq fut +0.40%, Dow fut +0.13%, Russell +0.02%; 10Y yield 4.60%; FedWatch 85.6% odds of a July hold; IBM +1.19% recovering after a 25% Tuesday plunge on weak revenue guidance — corroborates the internal legal/investigation-notice flag on IBM seen in catalyst_events).
  - Both sources are dated 2026-07-15 and consistent with each other and with the internal risk_on/VIX-16.4 read — no contradiction found, external check used to fill the gap-risk/futures gap only.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime 15:59 EEST, latest `cycle_06_15-06_summary.md` mtime 15:59 EEST — both ~30 min old at review time (16:29 EEST). **Not deferred.**
- Crypto scalp/intraday/swing all regenerated within the last ~1.5h — fresh this cycle.
- Stocks intraday report (12:33 EEST server time, ~1h old) is, by construction, still showing the pre-open "market closed" gate — expected for this exact slot (the report literally can't reflect post-open reality yet); RTH-confirmed levels won't exist until the next stocks-intraday cycle after 16:30 EEST.
- Stocks swing/invest: last full run 2026-07-02 (~13 days) — stale, deprecated legacy playbooks (per project memory), not used for verdicts.
- 2 untracked legacy crypto alerts flagged this run (FF/USDT, LTC/USDT) — see §14 TODO-1.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-15 16:29 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log/cycle_06 mtime ~30min old", "crypto scalp/intraday/swing all <1.5h old", "stocks intraday report inherently pre-open, will refresh post-16:30 EEST"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["mixed", "risk_on", "risk_off", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["stocks: risk_on, VIX 16.4, breadth 75%/100%, external futures confirm (SPY premkt +0.25%, S&P fut +0.15%, Nasdaq fut +0.40%) on cooler June PPI", "crypto: bullish-trend label but macro risk 100/100 risk-off overlay (Iran/Hormuz), altcoin breadth 55-70% mixed across modes"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl today: 566/2993 mapped (18.9%), 81.1% unmapped", "GOOGL fresh confirmed catalyst: Buffett/Berkshire Alphabet stake (CNBC, Yahoo, 2026-07-15)", "5 active narrative baskets incl. momentum_breakout (KAITO primary)"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.45,
      "reason_codes": ["oi_supports", "data_unavailable"], "data_missing": ["OI 24h% n/a for several MEXC-only movers (XEC, DODO, PUMP)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["KAITO: price up + OI up, fresh positioning, crowding normal", "DEXE: weak-vs-market with real 0.68x-1.45x volume confirming the move (not thin/illiquid)"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["stale_before_entry", "chase_risk", "price_moved_away"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["stocks pre-gate-A basket (JPM/META/XLF/NVDA/PLTR/GOOGL/AMZN/COIN) entirely planning-only until RTH confirmation, ~1min from the bell", "DEXE already made most of its -7.7 to -9.9% move over the last 5h — a fresh short now would be chasing", "JPM levels (326-334 invest zone) computed pre-earnings-refresh, stale"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "needs_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 21 active signals (mostly tp1_hit/tp2_hit/triggered, 2 waiting_for_entry: DOT, DODO swing + XEC intraday)", "stocks: 50 active rows shown (CLI cap), several C-tier triggered pre-open (NVDA 91.4, AMD 89.6, COIN 80.5, GOOGL 81.7) that are watchlist-only under the market-closed gate, not live entries"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review", "reduce_risk"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: confirmed DOJ criminal probe (news_items, 2026-07-14) + earnings tomorrow 07-16 — AVOID unchanged", "NFLX: earnings tomorrow 07-16, do-not-chase warning active", "IBM: 25% single-day plunge (Tuesday) + shareholder fraud investigation notice — external-confirmed, not a current candidate but sector-adjacent to GOOGL/tech theme", "Iran/Strait-of-Hormuz: fresh US strikes + blockade threats, oil >$85 — dominant gap-risk driver for both asset classes"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto scalp: PF 0.17, 0W/7L over 14d — low-confidence, data-collection only", "crypto swing PF 1.36/+6.2R best crypto bucket; crypto short direction PF 0.50 (weak)", "stocks A/B headline PF 1.64 but n=10 (weak confidence); stocks C-tier PF 0.62, winrate 9% (expected, watchlist-only, not actionable)"] },
    { "agent": "head_trader", "verdict": "manual_review", "confidence": 0.6,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of the eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "NVDA", "trigger": "RTH confirmation holding above the pre-gate 210.72 zone through the first 15-30min after 16:30 EEST open, with SPY/QQQ holding their premarket uptrend" },
    "best_short_candidate":    { "symbol": "DEXE/USDT", "trigger": "clean retest/rejection of the broken support level; do not chase the -7.7 to -9.9% move already made" },
    "best_catalyst_candidate": { "symbol": "GOOGL", "trigger": "RTH confirmation above the pre-gate 358.26-359.55 zone; catalyst is Buffett/Berkshire's disclosed Alphabet stake (CNBC/Yahoo, today) plus RS/technical score 81.7" },
    "avoid_candidate":         { "symbol": "UNH", "reason": "confirmed DOJ criminal probe (Medicare billing) + earnings tomorrow 2026-07-16 — legal + event risk stacked, no new exposure either direction" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.65 | mixed, risk_on, risk_off, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, fresh_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | ok | 0.45 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | stale_before_entry, chase_risk, price_moved_away | advisory_only |
| execution_lifecycle | caution | 0.75 | open_actionable, waiting_for_entry, entered_unresolved, needs_review | advisory_only |
| risk_manager | caution | 0.75 | legal_risk, headline_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.75 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | manual_review | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (11:30 EEST, Europe/pre-US context)

- **Pre-gate-A stocks basket unchanged in composition** (JPM, META, XLF, NVDA, PLTR, GOOGL, AMZN, COIN still the raw-A/B breadth), but scores drifted marginally (NVDA 91.43→91.4, COIN 80.54→80.5, GOOGL 81.74 held) — essentially the same setup, now 5h closer to the open with no fresh confirmation yet possible.
- **GOOGL upgraded from "RS-only" to genuinely catalyst-backed**: Warren Buffett/Berkshire Hathaway disclosed initiating an Alphabet stake today (CNBC, Yahoo Finance) — this is new since 11:30 and is now this review's best catalyst candidate (JPM held that slot last time but remains earnings-stale).
- **External futures/PPI context added this cycle** (not present at 11:30, which found internal data sufficient): cooler June PPI (-0.3% vs flat expected) pulled Fed-hike odds down, S&P/Nasdaq/Dow futures all modestly green heading into the 16:30 EEST open — reinforces the internal risk_on stocks read rather than contradicting it.
- **DEXE/USDT**: still the best crypto short-watch, still not retested — 24h move has drifted slightly (-9.29% at 11:30 → -7.68% to -8.75% across today's scalp/intraday reports), a marginal bounce, not a clean retest structure yet.
- **UNH**: unchanged — still avoid (DOJ probe + earnings now 1 session closer).
- **New untracked alert**: LTC/USDT joins FF/USDT in `detect_untracked_legacy_alerts` (FF/USDT is a carryover, still unresolved from 11:30 — see §14 TODO-1, now escalated).
- Iran/Strait-of-Hormuz overlay persists and, per external check, has intensified overnight (fresh US strikes, blockade reinstated) — still the dominant crypto risk-off driver and now confirmed as a live futures/oil driver for stocks too (oil >$85).

## 5. Catalyst Coverage

- Total `catalyst_events` today (cumulative across cycles): **2,993**; mapped (symbol present): **566 (18.9%)**; unmapped: **2,427 (81.1%)**.
- Narrative baskets: **5** active — `rwa_narrative` (primary ONDO, XLM), `perps_dex_narrative` (primary HYPE), `binance_ecosystem_teaser` (primary BNB), `delisting_thin_liquidity` (no primary), `momentum_breakout` (primary KAITO).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top unmapped headlines (sample, bot-noise filtered): "Guidewire's CEO Sold $166,000 in Stock…", "Oil Climbs to a 1-Month High as the U.S. and Iran Trade Attacks in the Strait of Hormuz…", "SoundHound AI Stock Is Down 37% in 2026…".

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **mixed / risk-off overlay on a nominal uptrend** — BTC/ETH trend-labeled uptrend, altcoin breadth 55-70.7% depending on mode (intraday weaker, swing stronger), but macro risk 100/100 risk-off (Iran/Strait-of-Hormuz strikes) caps conviction; no A-tier anywhere.
- Stocks mood: **risk-on (pre-market → confirmed by external futures)** — VIX 16.4, breadth 75%/100%, SPY premarket +0.25%, S&P/Nasdaq/Dow futures all green on cooler PPI; financials (XLF) and healthcare/utilities are the strongest sectors, semiconductors/materials/consumer-staples weakest.
- Dominant narrative: stocks — mega-cap/tech + financials breadth (JPM/META/NVDA/XLF) plus one fresh single-name catalyst (GOOGL/Buffett); crypto — no dominant breakout theme, KAITO/momentum_breakout basket is the closest thing to a live narrative.
- Preferred side now: **longs, RTH-confirmation required** on stocks (risk-on breadth is real and now futures-confirmed, but nothing is actionable until the market-closed gate lifts at 16:30 EEST); **wait-for-trigger** on crypto (macro risk-off overlay argues against chasing either side without a cleaner catalyst or retest).
- Best long candidate: NVDA (stocks, pre-gate A, watch — needs RTH confirmation).
- Best short candidate: DEXE/USDT (crypto, real volume confirms the move, but chasing risk since most of the move already happened — wait for retest).
- Best catalyst-backed candidate: GOOGL (stocks, Buffett/Berkshire Alphabet stake disclosed today + RS score 81.7).
- What to avoid: UNH (DOJ + earnings tomorrow); NFLX (earnings tomorrow, do-not-chase); using JPM's current pre-gate levels as-is (earnings-stale, needs a fresh post-open recompute); chasing DEXE/ZBT/HEI crypto shorts that already made most of their move.
- What would change the view: a clean RTH open that holds SPY/QQQ's premarket uptrend through the first 15-30 minutes (confirms the risk-on breadth is real, not a pre-market gap trap that fades); any Iran/Strait-of-Hormuz de-escalation headline (would unlock more aggressive crypto alt longs and remove the macro risk-off overlay); a further escalation would be the opposite — a fast risk-off gap that invalidates the pre-gate-A stocks basket entirely regardless of individual technical setup.

## 7. Candidate Deep Dives

### 1. NVDA — stocks, long, best long-watch
- Score 91.43 (pre-gate A), demoted to C **only** by `market_closed_intraday_planning_only` — no stale-data or legal flag.
- Has price already reacted to a catalyst? No single dominant catalyst — mixed news (Jensen Huang Japan trip to shore up partnerships after "Japan passing" backlash; NVIDIA reportedly dropping 50% of Asian AI chip clients amid China crackdown — a real risk note, not support) against a genuinely strong RS/technical score. This is an RS/technical setup, not catalyst-driven.
- Chasing? Not yet — nothing has traded since this remains a planning-only zone (210.72-211.80) until 16:30 EEST.
- Retest/pullback structure? To be confirmed at RTH open.
- Overextended? Semiconductors (SMH) remain the *weakest* sector in the report (RS vs SPY 20d -4.53%) even as NVDA individually scores 91 — a stock-specific divergence from its own sector worth confirming isn't a single-name anomaly once trading starts.
- Actionable now? **No** — planning/watchlist only until the cash open; requires first-15-30min RTH confirmation.
- Legal/headline check: none found (no DOJ/SEC/class-action/delisting flags for NVDA in today's data).
- Mood alignment: aligned with stocks risk-on mood and external futures (Nasdaq fut +0.40%), but sector divergence (semis weak) argues for confirmation over an automatic chase.
- **Verdict: WATCH. Best stocks long-watch for the open — require first-15-30min RTH confirmation before treating as live.**

### 2. JPM — stocks, long, contradiction risk (manual review)
- Score 100.0 (pre-gate A), demoted to C via two independent gates: post-earnings-stale zone (earnings reported 2026-07-14, per prior review's news_items check) and `market_closed_intraday_planning_only`. An `invest`-mode C-tier JPM signal (score 81.8) is separately `triggered` in the tracker — that's a different mode/timeframe and does not make the intraday zone fresh.
- Has price already reacted? Yes — the earnings print already happened; today's pre-gate levels were computed on pre-earnings structure and are stale by definition.
- Chasing? Would be, if traded on the current stale zone as-is.
- Actionable now? **No.** Needs fresh levels recomputed after RTH open before it can be treated as a real intraday signal.
- Legal/headline check: none found for JPM specifically today (external check found broader bank-earnings context — Morgan Stanley posted a record quarter — sector-supportive, not a JPM-specific flag).
- Mood alignment: aligned with risk-on stocks mood; financials (XLF) is the single strongest sector in the report (RS vs SPY 20d +3.97%).
- **Verdict: MANUAL REVIEW REQUIRED. Not actionable on current (stale) levels — this is exactly the "A/B with contradiction risk" case this routine prioritizes.**

### 3. GOOGL — stocks, long, best catalyst-backed candidate
- Score 81.74 (pre-gate A), demoted to C only by `market_closed_intraday_planning_only`.
- Has price already reacted to the catalyst? Partially — the Buffett/Berkshire Alphabet stake was reported today (CNBC "Warren Buffett tells CNBC he initiated Berkshire Hathaway's investment in Alphabet"; Yahoo Finance corroborates) via internal `news_items`, both same-day and consistent — no external research needed for this claim (internal-first check satisfied, §G).
- Chasing? Not yet — nothing has traded on this zone (358.26-359.55) pre-open.
- Retest/pullback structure? To be confirmed at RTH open; watch whether the Buffett-stake reaction is already priced into futures or triggers a fresh gap.
- Overextended? Cannot assess pre-open; check vs 2×ATR once trading starts.
- Legal/headline check: none found for GOOGL (the DOJ/legal flags in today's data belong to UNH and IBM, not GOOGL).
- Mood alignment: aligned with risk-on mood; this is the cleanest catalyst-backed name in the basket (single confirmed, dated, dual-sourced news item vs. the rest of the basket's pure-RS setups).
- **Verdict: WATCH — best catalyst-backed candidate. Require RTH confirmation; the Buffett-stake catalyst is real but do not assume it's still unpriced at the open.**

### 4. UNH — stocks, avoid / manual review (existing exposure only)
- Confirmed via internal `news_items` (2026-07-14, carried forward, unchanged): "DOJ's criminal probe into UnitedHealth extends to Optum Rx, physician reimbursement" (FierceHealthcare) and "UnitedHealth stock sinks 4.7% after company confirms DOJ investigation into Medicare billing practices" (Yahoo Finance). Also present today in `catalyst_events.jsonl` (QuiverQuant, Phemex).
- Earnings confirmed next session (2026-07-16, days_ahead=1) — do-not-chase warning active in the stocks report.
- Active tracker exposure: UNH intraday short C-tier (score 73.2, triggered) and UNH intraday long C-tier (score 80.0, tp1_hit) both still open — pre-existing, not new.
- **LEGAL/HEADLINE RISK — DOJ criminal probe, confirmed 2026-07-14, still active.**
- **Verdict: AVOID / MANUAL REVIEW. No new UNH exposure in either direction; existing tracker positions need human review given the DOJ + earnings stack.**

### 5. DEXE/USDT — crypto, short, best short-watch
- Bias short, 24h move -7.68% to -8.75% across today's scalp/intraday reports (was -9.29% at 11:30 — a slight bounce, not a retest), RS vs BTC -8.90% to -9.91%, volume 0.68x (scalp) confirming the move has real participation, not pure illiquidity noise.
- Has price already reacted? Yes — most of the down-move already happened over the last several hours.
- Chasing? A fresh short at current price would be chasing a move that's already 70-90% complete relative to its 24h range.
- Retest/pullback structure? Needed — wait for a bounce/retest of the broken support level rather than shorting the low directly.
- Actionable now? **Not as a fresh chase.** Best treated as a short-watch pending a clean retest/rejection.
- Legal/headline/catalyst check: no internal news found for DEXE in the last 24h — pure technical/RS weakness, no catalyst either way.
- Mood alignment: aligned with crypto's macro risk-off overlay (Iran/Hormuz), matching the pattern this desk labels `crypto_failed_bounce_short` rather than a raw breakdown chase.
- **Verdict: SHORT-WATCH. Wait for retest/rejection, not a chase of the move already made.**

## 8. Best Candidates Ranked

1. **NVDA — long-watch (stocks)** — best long, RTH confirmation required at/after 16:30 EEST.
2. **GOOGL — catalyst-watch (stocks)** — best catalyst-backed, Buffett/Berkshire stake confirmed today, needs RTH confirmation.
3. **JPM — manual review / catalyst-watch (stocks)** — highest raw score but post-earnings-stale; needs fresh post-open levels.
4. **DEXE/USDT — short-watch (crypto)** — best clean short, wait for retest not a chase.
5. **UNH — avoid / manual review (stocks)** — DOJ + earnings risk stack, existing exposure needs human review.

No clean immediately-actionable trade exists in either asset class at 16:20-16:29 EEST (crypto: risk-off macro overlay; stocks: market not yet open — this review lands at the bell). This is a **decision-window** read, not a system pause — scanning, tracking, and monitors continue unchanged.

## 9. Avoid / No Trade (this decision window only)

- UNH — confirmed legal risk + earnings tomorrow.
- NFLX — earnings tomorrow, do-not-chase warning active.
- Any use of JPM's current pre-gate levels — stale, earnings-invalidated.
- Any fresh DEXE/USDT short at current price without a retest — chasing an already-made move.
- This is a no-new-entries read for the listed names only; the scanner, monitors, and scheduler continue running unchanged.

## 10. Main Risks

- **Gap risk / Iran-Hormuz**: fresh US strikes and a reinstated blockade are live overnight; oil >$85. Futures are green into the open (external check) but this is the single biggest headline-risk factor that could flip the tape intraday regardless of any individual technical setup — treat all of §7/§8 as conditional on no fresh escalation headline at/after the open.
- Catalyst mapping running at 81.1% unmapped today — treat the catalyst layer as context only (see TODO-2, recurring theme per project memory).
- Crypto scalp mode remains structurally negative (PF 0.17, 0W/7L over 14d) — any scalp alert this cycle is data-collection only, not a trade signal.
- Two untracked legacy alerts this run (FF/USDT carryover + new LTC/USDT) — neither contributes to PF/winrate tracking (see TODO-1).
- Sector divergence on NVDA (individually strong vs. weak semiconductors sector) — a flag to watch at the open, not yet a red flag.

## 11. Action Plan — next 4 hours

- Watch NVDA, GOOGL, JPM, META, PLTR, XLF, AMZN, COIN at/after the 16:30 EEST (09:30 ET) cash open for RTH confirmation of the pre-gate-A breadth; do not treat any of them as live before then.
- On GOOGL specifically: confirm whether the Buffett-stake reaction is already priced into the pre-open futures move or produces a fresh gap at the open.
- Watch DEXE/USDT for a retest/rejection structure before considering a short.
- No new UNH or NFLX exposure; flag existing UNH tracker rows for human review given the DOJ + earnings stack.
- Monitor the Iran/Strait-of-Hormuz headline flow through the session — a fresh escalation is the main risk to every long idea above, in both asset classes.
- Continue scanning/tracking as normal — no system changes.

## 12. Final Verdict per Mode

- Crypto scalp: no fresh ideas this cycle; scalp playbook remains structurally negative (PF 0.17) — treat any new scalp alert as data-collection only.
- Crypto intraday: no fresh A/B; KAITO/XEC (B-tier, no catalyst) are watch-only, DEXE is the short-watch.
- Crypto swing: fresh this cycle (12:54 EEST); KAITO (78.0) is the top B-tier actionable long per the playbook's own gating; no A-tier. Existing tracked swing positions (BTC, ETH, TAO, KAT, JST, APE, SENT, ALLO, PYTH, BCH) continue to be managed per their existing TP/SL — no new swing ideas beyond KAITO/XEC/DOT/PUMP/DODO already in the tracker.
- Stocks intraday: **planning/watchlist only until 16:30 EEST** — pre-gate-A breadth (JPM/META/NVDA/PLTR/XLF/GOOGL/AMZN/COIN) is the watchlist for the open; this review lands at the bell, so the very next stocks-intraday cycle is what will confirm or invalidate these levels.
- Stocks swing/invest (legacy): deprecated, not used. `stocks_swing_growth_breakout` (new framework): shadow-only research, not actionable, not queried this run (out of scope for this slot's focus).

## 13. Sources

- [Stock Market Today: Dow Jones, S&P 500 Futures Gain as Trump Vows 'Very Hard' Strikes on Iran](https://www.benzinga.com/markets/equities/26/07/60461692/stock-market-today-dow-jones-sp-500-futures-gain-as-trump-vows-very-hard-strikes-on-iran-pentair-asml-holding-intel-in-focus) — Benzinga, 2026-07-15 (WebFetch-verified: S&P fut +0.15%, Nasdaq fut +0.40%, Dow fut +0.13%, 10Y 4.60%, FedWatch 85.6% hold odds, IBM +1.19% recovering post-25%-plunge).
- [US Equity Futures Drop Pre-Bell as Iran Says Strait of Hormuz Closed Once Again, Oil Prices Jump](https://www.marketscreener.com/news/us-equity-futures-drop-pre-bell-as-iran-says-strait-of-hormuz-closed-once-again-oil-prices-jump-ce7f5edcd988f624) — MarketScreener, 2026-07-15 (WebSearch result).
- Warren Buffett tells CNBC he initiated Berkshire Hathaway's investment in Alphabet — CNBC Markets, 2026-07-15 (internal `news_items`, corroborated by Yahoo Finance same date).
- DOJ's criminal probe into UnitedHealth extends to Optum Rx, physician reimbursement — FierceHealthcare, 2026-07-14 (internal `news_items`, carried forward).
- UnitedHealth stock sinks 4.7% after company confirms DOJ investigation into Medicare billing practices — Yahoo Finance, 2026-07-14 (internal `news_items`, carried forward).
- Internal: `data/reports/stocks/intraday/2026-07-15_12-33_stocks_intraday_report.md`, `data/reports/swing/2026-07-15_12-54_swing_report.md`, `data/reports/intraday/2026-07-15_12-19_intraday_report.md`, `data/reports/scalp/2026-07-15_12-13_scalp_report.md`.
- Internal: `data/catalysts/2026-07-15/catalyst_events.jsonl`, `narrative_baskets.jsonl`.

## 14. Fix Requests / TODO

### TODO-1: Untracked legacy crypto alerts (2 this run — FF/USDT carryover + new LTC/USDT)
- **issue:** `detect_untracked_legacy_alerts` shows 2 Telegram alerts sent without a matching `proposed_signal` within 6h: FF/USDT (B, intraday, score 68.5, sent 2026-07-15T07:36:38Z — flagged in the 11:30 review as a likely timing/registration lag, since FF/USDT does now appear correctly in `active-signals`... but it still shows as untracked in this run's detector output, so the underlying detector-vs-tracker mismatch has not resolved on its own) and LTC/USDT (B, intraday, score 68.2, sent 2026-07-15T10:59:45Z, new this cycle).
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-15` → 2 results (FF/USDT, LTC/USDT), both marked `trackable: NO (no proposed_signal)`.
- **suggested manual fix:** investigate why FF/USDT still shows untracked in this detector run despite appearing in `active-signals` — either the detector's matching window/logic has a gap, or the alert genuinely never got a `proposed_signal` row and the `active-signals` FF/USDT entry is an unrelated/later signal for the same symbol. Confirm which, then check LTC/USDT for the same root cause.
- **priority:** medium (escalated from low in the 11:30 review — now a 2-item recurring pattern, not a one-off).
- **first observed:** 2026-07-15 11:39 EEST (FF/USDT); 2026-07-15 16:29 EEST (LTC/USDT, and FF/USDT's persistence confirmed).

### TODO-2: Catalyst mapping weak (81.1% unmapped today)
- **issue:** `catalyst_events.jsonl` for today shows 566/2,993 (18.9%) events mapped to a symbol; 81.1% unmapped — consistent with the recurring theme flagged in project memory (catalyst-linkage under-fires) and slightly worse than the 11:30 review's same-day reading (16.7% mapped at that point, on a smaller cumulative sample of 2,000).
- **evidence:** direct count of `data/catalysts/2026-07-15/catalyst_events.jsonl` — mapped=566, unmapped=2427, total=2993.
- **suggested manual fix:** revisit the symbol resolver in the catalyst layer; the unmapped sample is dominated by generic multi-ticker "Motley Fool"-style analysis pieces and bot-noise ("welcome to Lookonchain" messages) that arguably shouldn't count against the mapping rate at all — consider a pre-ingest filter for these classes before recomputing the mapping-rate KPI.
- **priority:** medium.
- **first observed:** 2026-07-15 11:39 EEST (recurring, unresolved).
