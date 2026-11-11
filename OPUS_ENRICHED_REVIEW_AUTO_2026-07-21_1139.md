# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:30 EEST

## 1. Executive Summary

Slot: **Europe / pre-US context (11:30 EEST)**. Advisory only — no auto-trade, no scoring/threshold changes.
Scheduler + latest cycle (`cycle_05_09-15`) are ~1h40m old — fresh, no defer. Crypto tape stays **bullish trend / risk-on** (BTC & ETH uptrend, 76% breadth > EMA20) but a **risk-off macro overlay** (Iran-Bahrain strike on Amazon infra, Strait of Hormuz disruption, macro risk score 100/100) sits on top — treat as **mixed, not clean risk-on**. Stocks regime is explicitly **risk_off** (VIX 18.65, 0% breadth > EMA20, QQQ downtrend) but the US cash session is still closed — all stock C-tier signals are planning/watchlist only until RTH confirms. No A-tier anywhere. Best long: **VIRTUAL/USDT** (managed, not chasing). Best catalyst: **ADA/USDT** (Cardano hard-fork, genuinely fresh ~17h, multi-source) — **INJ/USDT's "fresh catalyst" framing is stale** (same 2026-07-19T18:25 UTC news item as the prior review flagged, now ~38h old; verified directly against `news_items`, not taken at face value). Best stock short-watch: **NVDA** (semis weak, needs RTH confirmation). Avoid: **BONK/USDT** (live exploit drainer). Catalyst mapping is weak this run (82.7% unmapped) — use as context only. Recurrence of the known untracked-alert bug (INJ, ADA) confirmed today — logged to §14, not fixed here.

## 2. Data Used

- Reports: intraday (06:30, fresh), scalp (06:24, fresh), swing (01:30, **carry-forward ~7h**), stocks intraday (06:47, fresh, market closed)
- Stocks swing/invest reports: last dated 2026-07-02 (19 days old) — **excluded**, superseded by the deprecated old stocks-swing/invest framework per project history; not used in this review
- Catalyst layer: `data/catalysts/2026-07-21/` (catalyst_cycle_06-32.md, catalyst_events.jsonl, narrative_baskets.jsonl)
- LLM packets: `llm_analysis_packet.md` (09:30), `llm_stocks_packet.md` (09:49)
- CLI: `active-signals` (crypto ×27, stocks ×50), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-07-21`
- Direct `news_items` query (per §G discipline) to verify INJ and ADA catalyst freshness before trusting the report's own "fresh catalyst" label
- Heartbeat: `data/autostart/heartbeat_state.json` — last OK 2026-07-21T07:37:35Z (~1h ago)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-21_0440.md` (04:40 slot)
- **External web research unavailable this run** (not invoked — internal `news_items` data was sufficient, fresh, and internally consistent for every candidate; no thesis depended on unverified external claims)

## 3. Scheduler / Data Freshness

- `scheduler.log` (2026-07-20_default_schedule folder): mtime 2026-07-21 09:57 → **fresh** (~1h40m old)
- Latest `cycle_05_09-15_summary.md`: mtime 2026-07-21 09:57 → **fresh**
- Heartbeat: OK at 07:37 UTC (10:37 EEST), warn last seen 2026-07-20 12:57 UTC — no recent warn, monitor alive
- Swing report (01:30 generation, 04:30 mtime): **carry-forward** (~7h old, within 4–12h band) — used, flagged
- Stocks swing/invest: **stale (19 days)** — excluded per §D rule (no fresher source exists, but the framework itself is deprecated per project history, so exclusion is correct rather than a gap)
- No deferral triggered (both freshness checks pass)

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-07-21 11:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["stocks swing/invest fresh data (deprecated framework, 19d stale, excluded)", "TradingView/chart MCP not loaded"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 09:57", "cycle_05_09-15_summary.md mtime 09:57", "heartbeat OK 07:37 UTC"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["risk_on", "risk_off", "mixed", "longs_preferred", "shorts_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH uptrend, 76.2% breadth>EMA20, macro risk 100/100 risk-off (Iran/Bahrain, Hormuz)", "stocks: label risk_off, VIX 18.65, breadth 0% >EMA20, QQQ downtrend -6.02% 20d"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "stale_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl today: 1500 rows, 260 mapped / 1240 unmapped = 82.7% unmapped", "ADA/USDT: news_items row 2026-07-20T18:50 UTC 'Cardano Triggers Hard Fork', corroborated by CoinDesk+Cointelegraph — genuinely fresh (~17h)", "INJ/USDT: report labels it canonical_news_event importance 0.95, but the underlying news_items row is 2026-07-19T18:25 UTC — same item flagged stale in the 04:40 review, now ~38h old, not fresh"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["squeeze_risk", "oi_supports", "funding_extreme"],
      "data_missing": ["OI% n/a for LA/ERA/HEMI/PROM/NIGHT/TLM (mexc fallback venues)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["LA/USDT: -0.0138 to -0.02 funding across bybit/okx/mexc while +34.9% 24h — crowded shorts, squeeze fuel", "VIRTUAL/INJ/HEMI: price up + OI up, funding near-neutral, crowding normal"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["clean_retest", "entry_late", "overextended", "chase_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["VIRTUAL: system waiting/managed band, not extended", "HEMI: +30-44% over 24h depending on report window, momentum_breakout basket rotated away from it today (now LA) suggesting cooling but still 2ATR+ extended per scalp rejection notes", "LA/USDT: scalp report explicitly rejects it '>2 ATR from EMA20; do not chase'"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "review_shadow"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals n=27: tp1_hit=14, tp2_hit=5 (open_actionable managing remaining targets), triggered=6 (entered_unresolved/running), waiting_for_entry=2", "stocks active-signals n=50: nearly all C-tier (review/shadow, not actionable per stocks-intraday hardening); only 3 historical B-tier rows already resolved weeks ago, 1 A-tier anecdotal in stats not in live table"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["headline_risk", "repeated_losses", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BONK: block_requires_operator_review, exploit drainer still selling (t.me/lookonchain)", "AMZN/BTC: geopolitical_risk warnings (Iran strike on Bahrain infra, quantum-recovery headline)", "GOOGL/TSLA: earnings 2026-07-22, do_not_chase_warning active", "crypto direction=short: n=8, winrate 0%, PF 0.125, avgR -0.58 (anecdotal but consistently bad)"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing PF 2.40 avgR 0.35 (n=47, stronger) — working", "crypto scalp PF 0.99 avgR -0.003 (n=37) — losing but already kill-switched (mode off)", "stocks C-tier headline winrate 15% (n=187, reliable) — flagged low by the system's own observation", "stocks sector=semiconductors PF 0.20 avgR -0.40 (n=24, weak) — clearly losing bucket"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "VIRTUAL/USDT", "trigger": "already in managed band 0.6532-0.6564; add only on fresh pullback into that zone, invalidation 1h close < 0.6492", "reason": "RS-leader (score 86.3), OI+price up, not overextended, crypto tape bullish" },
    "best_short_candidate":    { "symbol": "NVDA", "trigger": "RTH open, first 15-30min candle confirming below ~205, no gap-fill reclaim", "reason": "C-tier score 87.8 short, semiconductors sector RS -14.7% vs SPY 20d (weakest sector), stocks regime risk_off; planning-only until RTH confirms" },
    "best_catalyst_candidate": { "symbol": "ADA/USDT", "trigger": "manage existing tp2_hit position toward remaining target; fresh add only on retest of 0.1693-0.1704, invalidation 1h close < 0.1680", "reason": "Cardano 'van Rossem' hard fork activated, corroborated by CoinDesk + Cointelegraph + Decrypt within ~17h — genuinely fresh, unlike INJ's stale reused headline" },
    "avoid_candidate":         { "symbol": "BONK/USDT", "reason": "active exploit drainer still distributing stolen BONK to Coinbase, operator-review flag live, -40% since incident" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.60 | risk_on, risk_off, mixed, longs_preferred, shorts_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, fresh_catalyst, stale_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.60 | squeeze_risk, oi_supports, funding_extreme | advisory_only |
| technical_entry | caution | 0.65 | clean_retest, entry_late, overextended, chase_risk | advisory_only |
| execution_lifecycle | ok | 0.70 | open_actionable, waiting_for_entry, entered_unresolved, review_shadow | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, repeated_losses, reduce_risk | advisory_only |
| playbook_performance | caution | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution (synthesis) | 0.60 | see JSON | advisory_only |

## 4. What Changed vs Previous Review (04:40 slot)

- **VIRTUAL/USDT** — long-watch confirmed and progressed: still tp1_hit, thesis intact, unchanged as best long.
- **INJ/USDT** — the 04:40 review already flagged its "fresh catalyst" framing as ~31h stale (same 2026-07-19T18:25 UTC news item). Re-verified directly against `news_items` this cycle: it is the *same* item, now ~38h old. Demoted from any catalyst-watch role; still holds as a plain RS-leader long (no catalyst edge) across scalp/intraday/swing.
- **ADA/USDT** — promoted to best catalyst candidate this cycle after direct `news_items` verification confirmed a genuinely fresh (~17h), multi-source-corroborated Cardano hard-fork catalyst. Position has progressed from tp1_hit (04:40) to tp2_hit now.
- **HEMI/USDT** — was flagged "chase risk, do not enter fresh" after a +62.5% 24h move at 04:40; now rotated OUT of the `momentum_breakout` narrative basket (LA/USDT took the primary slot this cycle), suggesting cooling, but scalp report still rejects it as >2ATR extended. Still avoid fresh entry.
- **LA/USDT** — new this cycle: today's `momentum_breakout` basket primary, +34.9% 24h, crowded negative funding across venues (squeeze fuel). Added as a technical/derivatives watch item, not a clean entry.
- **NVDA** — short-watch thesis carries forward unchanged: still C-tier short (87.8), still planning-only pre-RTH, semis sector still the weakest.
- **BONK/USDT** — avoid carries forward unchanged; exploit drainer still active.
- **New this cycle:** untracked-alert bug (INJ, ADA) confirmed reproducing again today — see §14, ties to existing TODO-3 (raised 2026-07-17).

## 5. Catalyst Coverage

- Total catalyst events in today's file: **1,500** (cumulative across today's cycles) | mapped (non-null symbol): **260** | unmapped: **1,240** → **82.7% unmapped**
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Narrative baskets active: 5 (perps_dex_narrative/HYPE, ai_narrative/NEAR+RENDER+TAO+FET, rwa_narrative/ONDO+XLM, delisting_thin_liquidity, momentum_breakout/LA)
- Top 3 unmapped headlines (symbol resolver missed these):
  1. "MEXC to Delist STM and WULF USDT-M Stock Futures"
  2. "Delisting of UTYAUSDT Perpetual Futures Pair [Jul 23, 2026]"
  3. "IREN raises AI cloud revenue target above $4B on $2.8B in new multi-year contracts"

## 6. Market Landscape

**Crypto**: BTC & ETH both in uptrend, 76.2% of tracked symbols above EMA20, volatility normal (ATR percentile 59). Desk-recommended style: selective longs, prefer pullbacks on relative strength. Strongest symbols today: CRCLB (+12.1%), VIRTUAL (+9.5%), LA (+34.9%), ERA (+68.6%), HEMI (+30.2%), PROM (+13.5%). Weakest/short candidates are thin and mostly capped to C-tier by short-squeeze guards (NIGHT, TLM, ACE, HOME, ALICE) — the system itself is refusing most shorts against the bullish tape.

**Stocks**: Regime explicitly risk_off. VIX 18.65 (elevated-normal), 0% of names above EMA20, QQQ in a -6.0% 20d downtrend. Sector rotation is defensive: energy/healthcare/financials strong, semiconductors/technology weak (SMH -15.3% 20d RS vs SPY). Market is still closed (pre-market EU-morning slot) — every stock signal on the board is C-tier and demoted to planning/watchlist only; do not treat as confirmed until RTH.

**Macro overlay (relevant to both)**: Iran attacked Amazon's Bahrain data infrastructure and renewed fighting is straining the Strait of Hormuz — macro risk score 100/100, risk-off headwind flagged directly against BTC. This sits in tension with the bullish crypto technical regime; treat crypto "risk-on" as conditional, not clean, until the geopolitical thread cools or is priced in.

### Market Mood / Risk Routing
- Crypto mood: **mixed** (technical risk-on, macro risk-off overlay)
- Stocks mood: **risk-off, pre-market** (session closed — planning only)
- Dominant narrative: perps/DEX (HYPE) and AI rotation (NEAR/RENDER/TAO/FET) fresh <6h; RWA (ONDO/XLM) multi-week; Cardano hard-fork (ADA) genuinely fresh ~17h
- Preferred side now: **crypto longs on RS-leaders/catalyst-backed only; stocks wait-for-trigger (shorts favored post-RTH-confirmation)**
- Best long candidate: VIRTUAL/USDT (managed band, not chasing)
- Best short candidate: NVDA (planning-only, needs RTH confirmation)
- Best catalyst-backed candidate: ADA/USDT (verified fresh, multi-source; INJ's catalyst framing is stale — verified, not fresh)
- What to avoid: BONK/USDT (live exploit), fresh entries into HEMI/LA (both overextended, chase risk)
- What would change the view: Iran/Hormuz de-escalation (removes macro headwind) or further escalation (would flip crypto mood fully risk-off); US cash open reaction (confirms or kills the semis-weak short thesis)

## 7. Candidate Deep Dives

### 1. VIRTUAL/USDT (crypto, B-tier, intraday + swing, long) — Best Long
- Score 68.2 (intraday) / active tp1_hit both intraday and swing legs. RS vs BTC +6.5%, volume 0.75x (not confirmed by volume expansion).
- Has price already reacted? Partially — tp1 already hit; this is management, not a fresh chase.
- Chasing? No — system band is 0.6532-0.6564, current structure intact.
- Retest/pullback structure? Yes, the desk's own preferred entry is "pullback into 0.6532-0.6564."
- Overextended >2 ATR from EMA20? No.
- Would entry now be late? Only if buying above the pullback zone.
- Actionable now or after confirmation? Actionable within the defined band; no market-buy if extended.
- Aligned with market mood? Yes — RS-leader long fits the "selective longs, prefer pullbacks on RS" mood.
- Catalyst confirmation or contradiction? None — explicitly "no fresh verified catalyst," which is the system's own known-weak sub-cohort (no-catalyst intraday: 14d WR 23%/PF 0.70/-3R) — flagged as a caveat even though this specific setup is RS-led rather than pure momentum.
- Invalidation: 1h close beyond 0.6492 (intraday) / 0.6359 (swing, separate leg).
- TradingView/manual chart check unavailable — using local OHLCV/ATR/EMA fields only.

### 2. ADA/USDT (crypto, B-tier, intraday, long) — Best Catalyst (verified)
- Score 65.2, active tp2_hit. Entry band 0.169317-0.170413, invalidation 0.167977.
- Verified directly against `news_items` (not just the report's own label): "Cardano Triggers Hard Fork With First Community-Voted Upgrade" (Decrypt, 2026-07-20T18:50 UTC), corroborated by CoinDesk ("Van Rossum hard fork") and Cointelegraph — genuinely fresh (~17h), multi-source, not a repeat of an older item.
- Has price already reacted? Yes, partially — tp1 then tp2 already hit; this is management of a working thesis, not a fresh chase.
- Retest structure? Position is already deep into targets; a fresh add would need a retest of the original 0.1693-0.1704 band.
- Overextended? Not flagged in current reports.
- Actionable now? Managing existing position toward remaining target; fresh sizing only on retest.
- Aligned with mood? Yes — catalyst-backed long in a risk-on-leaning crypto tape.
- Invalidation: 1h close beyond 0.1680 (i.e., below original invalidation 0.167977).
- Contrast: **INJ/USDT's** "canonical_news_event importance 0.95" catalyst label was checked against the same `news_items` table and traces to a single 2026-07-19T18:25 UTC item — the identical headline the 04:40 review already flagged as stale. It is not fresh; INJ holds only as a plain RS-leader long, not a catalyst play, this cycle.

### 3. HEMI/USDT (crypto, B-tier swing per stale-but-carried 01:30 report, long) — Downgrade / Chase-Risk Watch
- Swing score 73.9 (best swing idea in the carried-forward report), but 24h return ranged 30-44% depending on report window — a large move already happened.
- Has price already reacted? Yes, strongly — this is the definition of a move that's "already priced."
- Chasing? Very likely if entering above the stale 0.0061-0.0064 zone; scalp report explicitly rejects HEMI-adjacent extended setups for "Price is more than 2 ATR from EMA20; do not chase."
- Retest structure? Not yet confirmed this cycle — HEMI dropped out of the `momentum_breakout` narrative basket (LA took the slot), suggesting cooling but no clean retest signal yet.
- Would entry now be late? Yes, for any fresh position at pre-cooldown levels.
- Actionable now? No — watch only. What would make it actionable: a genuine pullback into a newly-defined entry zone after the move cools, not the stale 7h-old band.
- Catalyst: none fresh verified.
- Invalidation for the stale idea: 1h close beyond 0.0057 (do not use to size a fresh entry).

### 4. LA/USDT (crypto, momentum only, no tier/no active signal) — Squeeze-Prone Watch
- +34.9% 24h, volume 1.64x, tagged relative_strength/volume_expansion/overextended in the "Unusual Volume" section; today's fresh (<1h) `momentum_breakout` narrative primary.
- Derivatives: funding -0.0138 (mexc) to -0.02 (bybit) to -0.01 (okx) — negative funding across all three venues while price is up sharply = crowded short positioning, squeeze fuel for further upside, but also a classic "this move could reverse hard" setup if longs get trapped chasing the same squeeze.
- Both scalp report (score 53.0, rejected — "2 ATR from EMA20, do not chase") and the catalyst basket itself (`wait_pullback` playbook) agree: not a fresh entry.
- Actionable now? No — watch-only. Trigger for actionability: a confirmed pullback with funding normalizing, not a continuation chase.
- Legal/headline risk: none identified for LA specifically.

### 5. NVDA (stocks, C-tier, intraday, short) — Best Stock Short-Watch (planning only)
- Score 87.8, but market is closed — **not actionable pre-RTH** per the stocks-intraday hardening rule (C-tier is never actionable) and per the report's own explicit banner ("MARKET CLOSED — planning/watchlist only").
- Sector context: semiconductors is the weakest sector (RS -14.7% vs SPY 20d, -15.3% 20d absolute), directly supporting a short thesis.
- Has price already reacted? Partially — Nebius/Nvidia stake news and cheap-Chinese-AI-model headlines are already circulating pre-market; a gap reaction is possible.
- Chasing? Cannot assess pre-open; do not chase a pre-market gap without RTH confirmation.
- Would entry now be late? N/A — market not open yet.
- Actionable trigger: first 15-30min RTH candle confirming below ~205 without a gap-fill reclaim.
- Legal/headline risk: none specific to NVDA beyond normal sector-rotation chatter; no fraud/investigation flags found.
- TradingView/manual chart check unavailable — using local OHLCV/sector fields only.

_No excess candidates beyond these 5 — GOOGL and TSLA (both C-tier, earnings 2026-07-22, `do_not_chase_warning` active) were considered but excluded from deep-dive since they are pure "wait for earnings to clear" holds with no current entry thesis; BONK is covered as an avoid item in §9 rather than repeated here._

## 8. Best Candidates Ranked

1. **Long-watch: VIRTUAL/USDT** — trigger: hold/manage the existing tp1_hit position; add only on a fresh pullback into 0.6532-0.6564, invalidation 0.6492, aligned with risk-on RS-leader thesis, not overextended.
2. **Catalyst-watch: ADA/USDT** — trigger: manage existing tp2_hit position toward remaining target; fresh add only on retest of 0.1693-0.1704, invalidation 0.1680; catalyst verified genuinely fresh (~17h, multi-source) against `news_items`.
3. **Short-watch: NVDA (+ correlated SMH/XLK basket)** — trigger: RTH open, first 15-30min candle confirming below ~205 without a gap-fill reclaim; planning-only until then.
4. **Watch, not entry: LA/USDT** — trigger: funding normalizes and a genuine pullback/retest structure forms; currently overextended and short-squeeze-fueled, do not chase either direction.
5. **Avoid fresh entry: HEMI/USDT** — trigger to reconsider: a clean pullback into a newly-defined zone after the move cools (current 0.0061-0.0064 band is stale and already extended).

## 9. Avoid / No Trade

_(this decision window only — never a command to stop the system)_

- **BONK/USDT** — active exploit drainer still distributing stolen funds to Coinbase; operator-review flag live; avoid until distribution pressure clears.
- **HEMI/USDT, LA/USDT (fresh entries)** — both overextended, chase-risk; system's own playbooks agree (wait_pullback/avoid_chase).
- **INJ/USDT (as a catalyst play)** — its "fresh catalyst" label is stale (~38h old, same item flagged in the prior review); still holds only as a plain RS-leader long, not a catalyst-backed entry.
- **GOOGL, TSLA (stocks)** — earnings 2026-07-22, `do_not_chase_warning` active on both; no new positions into the print.
- **Crypto shorts generally** — direction=short stats are anecdotal but consistently bad (n=8, 0% winrate, PF 0.125, avgR -0.58); bullish tape caps most short setups to C-tier via squeeze guards anyway.
- **Stocks C-tier intraday broadly** — headline winrate 15% (n=187, reliable) per the system's own observation; treat as research/watchlist, never actionable regardless of score.

## 10. Main Risks

- **Geopolitical**: Iran-Bahrain strike on Amazon infra + Strait of Hormuz disruption — macro risk 100/100, risk-off headwind against BTC despite bullish technical regime. Could reverse the crypto risk-on read quickly.
- **Earnings gap risk**: GOOGL and TSLA report 2026-07-22 — elevated volatility risk for correlated tech/semis names into and after the print.
- **Squeeze/reversal risk**: LA/USDT's crowded-negative-funding pump is exactly the setup that can violently reverse once the squeeze exhausts.
- **Catalyst mapping weak (82.7% unmapped)** — reduces confidence in catalyst-driven scoring this cycle; treat catalyst tags as directional color, not confirmation. Compounded by the INJ stale-catalyst mislabel — the "fresh attention/catalyst detected" language in reports does not self-check article age.
- **Known system bug recurring**: untracked watchlist alerts (INJ, ADA) fired today without a backing proposed_signal — those specific alerts won't contribute to PF/winrate tracking (doesn't affect the live signals analyzed above, which do have proper signal_ids).
- **Stale reference data**: stocks swing/invest reports are 19 days old (deprecated framework) — no swing/invest stock context available this cycle.

## 11. Action Plan — Next 4 Hours

- Continue managing VIRTUAL/USDT and ADA/USDT toward remaining targets; do not add size above the defined pullback/retest bands.
- Do not chase HEMI/USDT or LA/USDT at current extended levels; wait for genuine pullback/retest with normalizing funding.
- Watch NVDA and the semis/tech basket (SMH/XLK) into the US cash open for RTH confirmation of the short thesis; do not act on pre-market levels alone.
- Monitor Iran/Hormuz headlines — any material escalation should be treated as a fresh risk-off trigger for crypto, any de-escalation restores the cleaner risk-on read.
- No action needed on GOOGL/TSLA until after their 2026-07-22 earnings clear.
- Scanning, tracking, and monitors continue running unchanged — this review changes nothing in the pipeline.

## 12. Final Verdict per Mode

- **Crypto scalp**: kill-switched (mode off) — consistent with its own negative stats (PF 0.99, avgR -0.003, n=37). No action needed, system already reflects this.
- **Crypto intraday**: selective longs on RS-leaders/catalyst-backed only (PF 1.95, avgR 0.32, n=76 — working). Manage VIRTUAL, ADA; treat INJ as RS-leader-only, not catalyst-backed.
- **Crypto swing**: working well (PF 2.40, avgR 0.35, n=47) but this cycle's report is 7h carry-forward — treat HEMI idea as stale/chase-risk rather than fresh.
- **Stocks intraday**: planning/watchlist only — market closed, all C-tier. Re-evaluate at/after 09:30 ET RTH open.
- **Stocks swing/invest**: no fresh data (framework deprecated, last report 19 days old) — no verdict this cycle.

## 13. Sources

_No new external WebSearch/WebFetch was performed this cycle (per §G, internal records were fresh/consistent/sufficient) — no source-ingest JSON was written and no new `news_items` rows were created. The citations below are existing internal `news_items` rows (source + title + published_at only; the DB query used did not select the stored article URL, so none is fabricated here):_

- "Cardano Triggers Hard Fork With First Community-Voted Upgrade" — Decrypt, 2026-07-20T18:50 UTC (internal `news_items`, used to verify ADA catalyst freshness)
- "Inside Cardano's 'Van Rossum' hard fork, and what it means for users" — CoinDesk, 2026-07-20T14:31 UTC (corroborating source)
- "Cardano activates van Rossem hard fork" — Cointelegraph, 2026-07-20T04:26 UTC (corroborating source)
- "Injective highlights SEC registration, Robinhood listing for INJ at Summit" — CryptoBriefing, 2026-07-19T18:25 UTC (internal `news_items`, used to verify INJ catalyst is stale, not fresh)
- All other candidate context sourced from internal reports/CLI listed in §2.

## 14. Fix Requests / TODO

### TODO-untracked-alert-recurrence-0721
- **issue:** `detect_untracked_legacy_alerts` found 2 more untracked crypto watchlist alerts today (INJ/USDT 07:55:44 UTC, ADA/USDT 08:29:15 UTC) — same signal_id-reuse pattern previously logged.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-21` output: "2 untracked legacy crypto alert(s)... will NOT contribute to PF / winrate / avgR."
- **suggested manual fix:** continue work on the existing signal_id-reuse bug (raised 2026-07-17, high priority in project memory) — this run's INJ/ADA instances are new evidence, not a new bug.
- **priority:** high (already tracked, adding evidence)
- **first observed (this recurrence):** 2026-07-21 11:39 EEST

### TODO-catalyst-freshness-mislabel-0721
- **issue:** report-layer "fresh attention/catalyst detected" / `canonical_news_event` labels do not check underlying article age. INJ/USDT was labeled a fresh, high-importance (0.95) catalyst in both this cycle's swing report and the 04:40 review's data, but the underlying `news_items` row is the same 2026-07-19T18:25 UTC item both times (~38h old by this run) — a recurring false-fresh signal, not a one-off.
- **evidence:** `SELECT published_at, source, title FROM news_items WHERE detected_symbols_json LIKE '%INJ%' AND published_at > now-48h` returns exactly one row, unchanged across at least two review cycles (04:40 and 11:30 today).
- **suggested manual fix:** a human-driven session should add an explicit "hours since publish" field to the catalyst_news score component (or a decay/expiry window) so a 38h-old single-source item stops presenting as "fresh."
- **priority:** medium (does not affect trade correctness since the reviewer manually verifies, but affects trust in the automated label)
- **first observed (this recurrence):** 2026-07-21 11:39 EEST (previously implicitly noted 2026-07-21 04:40 EEST)

### TODO-stocks-semiconductors-sector-loss-0721
- **issue:** `sector=semiconductors` is a clearly losing bucket in stocks signal-stats: PF 0.20, avgR -0.40, n=24 (weak confidence but consistent direction), while stocks C-tier headline winrate overall is 15% (n=187, reliable).
- **evidence:** `python -m src.cli signal-stats --asset-class stocks` — By-sector table, semiconductors row.
- **suggested manual fix:** a human-driven session should review whether semiconductor-sector stock signals need a tighter entry/RR gate similar to the crypto scalp kill-switch, given the sector is also flagged structurally weak (RS -14.7% vs SPY) this cycle.
- **priority:** low (small sample, but directionally consistent with the broader stocks C-tier low-winrate observation)
- **first observed:** 2026-07-21 11:39 EEST
