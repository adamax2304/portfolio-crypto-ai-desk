# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:39 EEST

## 1. Executive Summary

**Slot: Europe / pre-US context — advisory only / no auto-trade.** US cash open is ~5h away (13:30 UTC); crypto is the only live-actionable class this window, stocks are planning/watchlist only.

**Crypto tape improved modestly since the 04:39 review, but sentiment is still cautious.** BTC $63,356 (+2.18% 24h), ETH $1,750 (+1.02% 24h), both now clean "uptrend" per the desk's own regime read (was chop/ETH-range at 04:39). Fear & Greed ticked 22→23 — still in Fear territory. The two BTC/ETH swing shorts flagged at 04:39 as "already breached breakeven, at risk of round-tripping to a loss" **resolved the other way — both hit TP1 (final_r +1.0 each)**, confirmed via `signal_outcomes` as of 08:41 UTC. Two unrelated BTC/ETH short signals from 2026-07-09 did stop for -1R each, already closed before this window.

**Fresh this cycle:** BTC/USDT and XRP/USDT intraday longs both upgraded C→B (08:37–08:41 UTC), both still `waiting_for_entry` — no chase needed yet. ZEC/USDT's Ironwood-proof catalyst is externally confirmed (Project Tachyon/Shielded Labs formal-verification progress) and remains the cleanest catalyst-backed watch, though its original swing pullback zone (474–478) is now stale — price has run to the 495–499 area (see new ZEC intraday signal).

**Stocks: pre-open planning only.** All raw A-tier stock setups (META, AAPL, AMD, JPM, TSLA, AVGO, QQQ, SMH, AMZN, XLF) are correctly gate-demoted to C for market-closed; UNH additionally carries an active legal/headline risk (SEC/DOJ) that should keep it avoid-until-cleared even after the open.

**Overall verdict: CAUTION, routed by side.** Crypto: watch BTC/XRP intraday triggers and ZEC-intraday; don't chase DEXE (documented no-catalyst chase-risk, still open across 3 modes) or ZEC's stale swing zone. Stocks: build the pre-US watchlist, do not treat anything as actionable before 09:30 ET confirmation.

Sources: [Crypto Market News July 10 — CoinGabbar](https://www.coingabbar.com/en/crypto-currency-news/crypto-market-news-july-10-bitcoin-price-defi-market-up-today), [Zcash native surges as Zooko Wilcox announces proof progress — CryptoBriefing](https://cryptobriefing.com/zcash-zec-surges-ironwood-proof-progress/), [Will Zcash's formal verification of Ironwood clear counterfeiting fears — AMBCrypto](https://ambcrypto.com/will-zcashs-formal-verification-of-ironwood-clear-counterfeiting-fears-and-boost-zec/)

## 2. Data Used

- Crypto: `2026-07-10_08-22_scalp_report.md`, `2026-07-10_08-27_intraday_report.md`, `2026-07-10_01-08_swing_report.md` (carry-forward, ~10.5h old)
- Stocks: `2026-07-10_08-36_stocks_intraday_report.md`; swing/invest reports last generated 2026-07-02 (see §3)
- Catalysts: `data/catalysts/2026-07-10/catalyst_cycle_08-28.md`, `catalyst_events.jsonl` (cumulative day file), `narrative_baskets.jsonl`
- LLM packets: `llm_analysis_packet.md` (11:28), `llm_stocks_packet.md` (11:37)
- CLI: `active-signals` (crypto, stocks), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts`
- DB (read-only): `proposed_signals`, `signal_outcomes`, `watchlist_alerts` for BTC/ETH/ZEC/SENT/DEXE/XRP/HYPE
- External: 2 WebSearch queries (BTC/ETH price + mood; ZEC Ironwood catalyst verification) — no WebFetch needed, search snippets were sufficient and consistent across sources
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-10_0439.md`

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime 11:38 EEST; Cycle 6 completed 11:41:11 EEST, `ok=40 failed=0 telegram=sent` — **fresh, not deferred.**
- Crypto scalp/intraday reports generated 11:22–11:27 EEST this run — fresh (minutes old).
- Crypto swing report generated 01:08 EEST (~10.5h ago) — **carry-forward** (4–12h bucket); ZEC/SENT swing ideas below are read from it but cross-checked against live signal status in the DB.
- Stocks intraday report generated 11:36 EEST — fresh.
- Stocks swing/invest reports last generated **2026-07-02** (>1 week stale). This is consistent with the known deprecation of the legacy stocks swing/invest mode in favor of the shadow-only `stocks_swing_growth_breakout` framework — **not a fresh regression**, no action needed; flagged only for completeness.
- Crypto monitor (pid 12944) and stocks monitor (pid 1668) both confirmed still running at end-of-cycle. Paper monitor Telegram status ran successfully (exit=0).
- Catalyst files for today present (4 cycles: 00:47, 03:47, 06:32, 08:28) — no re-scan needed.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-07-10 11:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.9,
      "reason_codes": ["scheduler_fresh"], "data_missing": [], "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 11:38 EEST", "cycle 6 ok=40 failed=0 telegram=sent", "swing report 10.5h old (carry-forward)", "stocks swing/invest stale since 2026-07-02, expected due to mode deprecation"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["mixed", "longs_preferred", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC $63,356 +2.18%, ETH $1,750 +1.02% (external)", "Fear&Greed 23, up from 22 (external)", "internal macro risk score 79/100 risk-off headwind", "altcoin breadth 51.35% above EMA20", "stocks regime risk_on, VIX 16.06, but market closed"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["fresh_catalyst", "catalyst_confirmed", "mapping_weak", "no_catalyst"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZEC Ironwood shielded-pool proof externally confirmed (Project Tachyon/Shielded Labs)", "catalyst mapping 1606/2000 unmapped today (80.3%)", "DEXE/KAT momentum_breakout basket explicitly no-catalyst pure momentum"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.45,
      "reason_codes": ["squeeze_risk", "data_unavailable"], "data_missing": ["OI 24h% for KAT/DEXE/EVAA/SYN/ZEC/RE (n/a via mexc fallback)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["KAT/SKL/VANRY negative funding + elevated external crowding (short-squeeze risk upside)", "Alphractal CEO warning: BTC/ETH/XRP/SOL crowded longs face liquidation risk"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["entry_fresh", "stale_before_entry", "price_moved_away", "chase_risk"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/XRP intraday fresh C->B this cycle, both waiting_for_entry", "ZEC swing zone 474-478 vs new ZEC intraday zone 495-499 (~3 ATR away, stale)", "DEXE documented chase-risk carried forward from 04:39 review, still open 3 modes"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["waiting_for_entry", "open_actionable", "needs_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/XRP/ZEC-intraday/ZEC-swing/DEXE-swing = waiting_for_entry (5)", "DEXE-intraday/DEXE-scalp/SENT-swing = triggered/entered-unresolved (3)", "1 untracked legacy alert (SENT/USDT scalp, no proposed_signal)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: active sec_doj legal/headline risk, A-raw demoted to C for this reason (not just market-closed)", "TSLA: Musk SEC Twitter settlement approved (resolved, lower incremental risk) but still flagged", "JPM earnings 2026-07-14 (4 trading days out)"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["scalp mode n=137 reliable, PF 0.56, totalR -9.70, WR~10.5% — persistently net-negative", "swing mode n=103 reliable, PF 1.34, totalR +9.97, WR~42% — best-performing mode", "intraday mode n=144, PF 1.04, totalR +1.49 — roughly breakeven-positive", "Binance+Bybit cross-confirmed setups PF 2.23 vs Binance-only PF 0.86 vs MEXC-only PF 0.25"] },
    { "agent": "head_trader", "verdict": "caution",
      "reason_codes": [], "data_missing": [], "confidence": 0.6, "suggested_effect": "advisory_only", "facts_used": [] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "BTC/USDT", "trigger": "clean push + close through 63971-64118 with volume (fresh C->B intraday, still waiting_for_entry, spot ~63,356)", "reason": "uptrend regime, fresh upgrade this cycle, cross-asset confirmation (ETH also up)" },
    "best_short_candidate":    { "symbol": "HYPE/USDT", "trigger": "failed retest/rejection 67.21-67.47 with volume, or breakdown below 66.66; invalidation above 67.795 (carried forward from 04:39 review, NOT re-verified this cycle)", "reason": "perps_dex_narrative basket primary, still below entry threshold, no fresh level data this run" },
    "best_catalyst_candidate": { "symbol": "ZEC/USDT", "trigger": "intraday pullback fill into 495.21-498.68, invalidation 490.97 (swing zone 474-478 is stale, do not chase there)", "reason": "Ironwood shielded-pool proof externally confirmed (Project Tachyon/Shielded Labs), RS-leader vs BTC" },
    "avoid_candidate":         { "symbol": "DEXE/USDT", "reason": "no-catalyst momentum_breakout basket, documented chase-risk since 04:39 review, already open across scalp+intraday(triggered)+swing(waiting) — adding more exposure compounds a known-bad cohort (14d no-catalyst intraday WR23%/PF0.70)" },
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
| market_regime | caution | 0.65 | mixed, longs_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | fresh_catalyst, catalyst_confirmed, mapping_weak, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.45 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | entry_fresh, stale_before_entry, price_moved_away, chase_risk | advisory_only |
| execution_lifecycle | ok | 0.80 | waiting_for_entry, open_actionable, needs_review | advisory_only |
| risk_manager | caution | 0.60 | legal_risk, headline_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.70 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader (synthesis) | caution | 0.60 | — | advisory_only |

## 4. What Changed vs Previous Review (04:39)

- **Resolved positively:** BTC/USDT and ETH/USDT swing shorts (entries 62096.26 / 1739.20) flagged at 04:39 as "already breached breakeven, at risk of round-tripping to a loss" instead **hit TP1** — `signal_outcomes` shows `tp1_hit`, `final_r=+1.0` for both, checked 2026-07-10 08:41:02 UTC. The 04:39 concern did not materialize into a loss.
- **Unrelated, already closed:** a separate pair of BTC/ETH swing shorts (entries created 2026-07-09 01:45–01:53) did stop for -1R each — resolved before this window, not part of the 04:39 headline concern.
- **New this cycle:** BTC/USDT intraday long upgraded C→B (08:41 UTC, score 68.8) and XRP/USDT intraday long upgraded C→B (08:37 UTC, score 65.8) — both fresh, both `waiting_for_entry`.
- **New ZEC intraday signal** (08:36 UTC, entry 495.21–498.68) reflects price having moved up since the 01:08 swing report; the older ZEC swing pullback zone (474.17–477.69) is now roughly 3 ATR below current levels — carried forward but should be treated as stale/low-probability, not a fresh idea.
- **DEXE/USDT** — unchanged story: still open across scalp (triggered), intraday (triggered), and swing (waiting_for_entry). Same avoid-chase guidance as 04:39 carries forward.
- **New integrity anomaly:** 1 untracked legacy alert this window (SENT/USDT scalp B, 08:27 UTC) with no matching `proposed_signal` — did not exist as an open item at 04:39.
- **HYPE/USDT short-watch** — unchanged, still no signal ever proposed, still below entry threshold. Level carried forward, not re-verified this cycle (no fresh HYPE data surfaced in today's reports).
- **Regime characterization improved slightly:** 04:39 called it "chop/mixed, risk-off leaning" (BTC nominal-uptrend/ETH-range, breadth ~44–50%, Fear&Greed 23→ actually was 23 at 04:39 too); this cycle both BTC and ETH show clean uptrend, breadth ticked to 51.35%, Fear&Greed 22→23. Net: modest, not decisive, improvement.

## 5. Catalyst Coverage

- Total catalyst events today (cumulative, `catalyst_events.jsonl`): **2,000**
- Mapped (non-null symbol): **394** (19.7%)
- Unmapped: **1,606 (80.3%)**
- Narrative baskets: **5** (ai_narrative, delisting_thin_liquidity, perps_dex_narrative, rwa_narrative, momentum_breakout)

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

Top unmapped headlines (sampled): MEXC SPY-index futures listing (0-fee promo), MEXC pre-IPO futures listings (QXO/AKAM/FLUT/GRAB), MEXC pre-IPO SKHY futures listing, LABUSDT funding-rate settlement-frequency adjustment. These are mostly generic exchange administrative/listing announcements rather than substantive trading catalysts — the practical information loss from the mapping gap looks lower than the raw 80.3% suggests, but this is a qualitative read, not a re-audit.

## 6. Market Landscape

- **Crypto:** BTC $63,356 (+2.18% 24h), ETH $1,750 (+1.02% 24h) (external, CoinGabbar); both uptrend per internal regime read; altcoin breadth 51.35% above EMA20 / 48.65% above EMA50; ATR percentile 31 (normal vol). Fear & Greed 23 (Fear, up from 22). Internal macro-risk classifier still reads 79/100 risk-off (driven by generic risk-off headline hits, not a specific fresh shock). Global crypto market cap $2.25T, +1.9% 24h.
- **Stocks:** risk_on label, VIX 16.06, breadth 100% above EMA20/50, financials (XLF) and healthcare (XLV) strongest sectors, energy (XLE) weakest. Market closed until 13:30 UTC (09:30 ET) — nothing here is actionable yet.

### Market Mood / Risk Routing

- Crypto mood: **mixed — cautiously improving** (price/trend up, sentiment gauge still Fear, macro-risk classifier still risk-off-leaning)
- Stocks mood: **risk-on, but closed** (pre-market planning only)
- Dominant narrative: AI-sector rotation (NEAR/RENDER/TAO/FET) and perps/DEX (HYPE) baskets remain the two live narrative threads; RWA (ONDO/XLM) is slower-moving multi-week thesis
- Preferred side now: **longs, RS-leader + catalyst-backed, sized cautiously** (crypto); **wait-for-trigger** (stocks, until 09:30 ET)
- Best long candidate: BTC/USDT (fresh intraday B, waiting_for_entry — see §8)
- Best short candidate: HYPE/USDT (carried forward, unverified this cycle — see §8)
- Best catalyst-backed candidate: ZEC/USDT (Ironwood proof, externally confirmed)
- What to avoid: DEXE/USDT fresh entries (chase-risk, no catalyst); UNH (active legal/headline risk regardless of market open); new crypto scalp entries generally (persistently net-negative mode, see §7 dive #5 note in playbook_performance)
- What would change the view: a confirmed BTC close above 64,118 with volume (bullish continuation) or a break of 63,793 (bearish reassertion); Fear&Greed dropping back under 20 would argue for tighter risk overall

## 7. Candidate Deep Dives

### #1 — ZEC/USDT (catalyst-backed watch)

- Has price already reacted to the catalyst? Partially — ZEC jumped ~12% on July 7 on the initial Ironwood proof-progress news; today's 24h move is a more modest +7.36%, so some but not all of the catalyst is priced in.
- Chasing? Not at the intraday level (495.21–498.68 reflects current price, not a stretch); yes at the stale swing level (474–478 is now far below spot).
- Retest/pullback structure? The intraday signal is itself a pullback-style entry; the swing zone would require a much deeper retracement to fill.
- Overextended? Not flagged as >2 ATR from EMA20 in the intraday report; ATR was 7.82 as of the 01:08 swing snapshot.
- Would entry now be late? At the stale swing zone, yes. At the fresh intraday zone, no.
- Actionable level: intraday pullback into 495.21–498.68, invalidation 490.97.
- Mood alignment: yes — RS-leader, uptrend regime, catalyst-confirmed.
- Long/short/wait: long, wait for the pullback fill (not a market long at current spot).
- Invalidation: 490.97 (intraday); 469.86 (stale swing reference only).
- Chase-risk: low at the intraday zone, high at the swing zone.
- Catalyst confirmation/contradiction: **confirmed externally** — Project Tachyon/Shielded Labs formal-verification progress on the Ironwood shielded pool, reported by CryptoBriefing, AMBCrypto, CoinMarketCap (July 7–10).

### #2 — BTC/USDT (best long-watch)

- Has price reacted? Yes, +2.18% 24h, clean uptrend.
- Chasing? No — entry zone (63,971–64,118) is still ~1% above current spot (~63,356); this is a breakout-confirmation entry, not a chase.
- Retest/pullback structure? N/A — this is a continuation-breakout setup, not a pullback play.
- Overextended? No signal of that in the report.
- Would entry now be late? No — signal is still `waiting_for_entry`.
- Actionable level: close through 63,971–64,118 with volume; invalidation 63,793.034.
- Mood alignment: yes, matches the "longs, cautiously" routing.
- Long/short/wait: long, wait for trigger.
- Chase-risk: low (level is above spot, not chasing a move already made).
- Catalyst confirmation: no specific BTC catalyst this cycle beyond broad regulatory/ETF-adjacent news flow (Bitwise index rebalance, Binance derivatives-listing news) — this is a technical/momentum setup, not catalyst-driven.

### #3 — XRP/USDT (secondary long-watch)

- Has price reacted? Fresh C→B upgrade this cycle (08:37 UTC, score 65.8); underlying "catalyst" cited internally is a Bybit promotional post ("$XRP or $SOL? Stake and earn up to 555% APR") — this is exchange marketing, not a fundamental catalyst, plus a bearish Alphractal crowded-longs liquidation warning naming XRP explicitly.
- Chasing? Entry zone 1.1097–1.1125; current spot not independently re-verified this cycle (no live XRP price pulled) — treat distance-to-entry as unconfirmed.
- Actionable level: 1.1097–1.1125, invalidation 1.10635.
- Mood alignment: partial — technical upgrade supports it, but the "catalyst" backing is weak/promotional and there's an explicit external crowded-long warning on this exact symbol.
- Long/short/wait: long, wait for trigger, treat as lower-confidence than BTC given the weak catalyst quality and the crowding warning.
- Catalyst confirmation/contradiction: **contradicted/weak** — cited catalyst is a promotional exchange post, not news; external Alphractal warning flags crowded-long liquidation risk on XRP specifically.

### #4 — UNH (stocks, avoid / legal-headline risk)

- Raw score 93.11/100, tier A, but demoted to C for two independent reasons: (1) market-closed planning-only gate, and (2) an active `sec_doj` legal/headline-risk flag.
- Is this candidate aligned with market mood? Irrelevant while the legal flag is live — legal/headline risk overrides technical alignment per the desk's own gating.
- Actionable now or after confirmation? Neither — this stays avoid/manual-review until the legal flag clears, independent of the 09:30 ET open.
- What would invalidate the avoid call: resolution or dismissal of the underlying SEC/DOJ matter (not sourced with a specific date this cycle — internal risk-warning flag only, no external legal-status article pulled this run).
- Chase-risk: N/A (not actionable).
- Legal/headline risk: **yes, active** — per internal production risk warning (`block_requires_operator_review`, sec_doj tag). Verdict: **AVOID / MANUAL REVIEW REQUIRED**, not a clean actionable even after the open.

### #5 — DEXE/USDT (avoid / chase-risk, carried forward)

- Has price already reacted? Yes — +23–24% 24h, this is a move already made, not a fresh setup.
- Is the setup chasing? Yes, for any new entry — this has been flagged as chase-risk since the 04:39 review and price has not meaningfully pulled back.
- Retest/pullback structure? The desk's own C-tier watchlist entry (score 62.7, `crypto_intraday_catalyst_or_momentum`) explicitly says "not strong enough for an active trade... demand a better entry."
- Overextended? Consistent with a vertical 24h move; the playbook's own known-failure-mode note: "no-catalyst intraday in chop is net-negative — needs RS-leader or breakout confirmation," which this setup has not shown.
- Would entry now be late? Yes.
- Actionable level for a genuine re-entry: a real retest of the 31–32 area (per the 04:39 review's language), not current levels (~33–35 across the three open legs).
- Mood alignment: no — this is exactly the no-catalyst chase cohort the mood routing says to avoid.
- Chase-risk: **high**.
- Catalyst confirmation/contradiction: **no catalyst** — explicitly labeled "momentum_breakout... without confirmed news catalyst" in the narrative-basket data.

## 8. Best Candidates Ranked

1. **Best catalyst-watch: ZEC/USDT** — intraday pullback fill into 495.21–498.68, invalidation 490.97. Ironwood-proof catalyst externally confirmed. Ignore the stale swing zone (474–478).
2. **Best long-watch: BTC/USDT** — breakout-confirmation trigger through 63,971–64,118, invalidation 63,793.034. Fresh C→B this cycle, clean uptrend regime.
3. **Secondary long-watch: XRP/USDT** — trigger 1.1097–1.1125, invalidation 1.10635. Lower confidence: catalyst is promotional, not fundamental, and there's an external crowded-long warning naming XRP.
4. **Best short-watch: HYPE/USDT** — failed retest/rejection 67.21–67.47 or breakdown below 66.66, invalidation above 67.795. Carried forward unchanged from 04:39; **not re-verified this cycle**, re-check the level before acting.
5. **Avoid: DEXE/USDT** fresh entries, and **avoid/manual-review: UNH** (legal risk, independent of market open).

## 9. Avoid / No Trade

This applies to the current decision window only — scanning, tracking, and the scheduler continue regardless.

- **DEXE/USDT** fresh longs — chase-risk, no catalyst, already extended across 3 open legs.
- **New crypto scalp entries** generally — mode is empirically net-negative at scale this week (n=137, PF 0.56, totalR -9.70, WR~10.5%) despite the report banner calling it "active for data collection"; manage existing legacy scalp positions (DEXE triggered) to their stops/targets, don't add new scalp exposure.
- **UNH** — avoid/manual-review regardless of the US open, active legal/headline risk (sec_doj).
- **ZEC/USDT swing entries at the old 474–478 zone** — stale, price has moved ~3 ATR away; use the fresh intraday zone (495.21–498.68) instead if trading ZEC.
- **Stocks generally** — market closed, nothing actionable before 09:30 ET confirmation.

## 10. Main Risks

- Sentiment/price divergence: BTC/ETH price action is improving but Fear&Greed (23) and the internal macro-risk classifier (79/100 risk-off) haven't confirmed a regime shift — a fresh risk-off headline could reverse the modest improvement quickly.
- Crowded-long liquidation risk flagged externally (Alphractal) on BTC/ETH/XRP/SOL simultaneously — relevant to sizing any new long, including BTC/XRP watch items above.
- Scalp-mode drag: continuing to fire new B-tier scalp alerts (7 this cycle alone) into a mode with a documented -9.7R track record this week.
- Catalyst mapping at 80.3% unmapped this run — treat any catalyst-backed thesis as context, verify independently before treating as confirmation.
- JPM earnings 2026-07-14 — 4 trading days out; relevant to any JPM-adjacent position sizing/duration.
- UNH legal/headline risk (sec_doj) is a real, undated internal flag — no external confirmation of case status was pulled this run; treat as an open unknown, not a resolved one.

## 11. Action Plan — next 4 hours

1. Watch for BTC/USDT close through 63,971–64,118 with volume; watch ZEC/USDT pullback fill into 495.21–498.68. Neither is actionable yet.
2. Do not add new DEXE/USDT exposure or chase XRP without re-verifying the crowded-long warning.
3. Do not add new crypto scalp positions; manage existing legacy scalp/intraday/swing legs (DEXE, SENT) to their stops/targets only.
4. Build the pre-US stock watchlist from the C-tier list (META, AAPL, AMD, JPM, TSLA, AVGO, QQQ, SMH, AMZN, XLF) but treat none as actionable until 09:30 ET confirmation; carry UNH as avoid regardless.
5. Re-check HYPE/USDT levels at the next cycle before treating the short-watch trigger as live — this run did not re-verify it.

## 12. Final Verdict per Mode

- **Crypto scalp:** CAUTION / manage-only. Mode is net-negative at scale (PF 0.56, -9.7R, n=137) despite still being nominally active; do not add new exposure.
- **Crypto intraday:** WATCH. Mildly positive edge (PF 1.04, +1.49R). BTC and XRP freshly upgraded to B, both waiting_for_entry; ZEC intraday also fresh and catalyst-backed.
- **Crypto swing:** WATCH, cautiously constructive. Best-performing mode this week (PF 1.34, +9.97R, WR~42%). ZEC/SENT swing already in book; do not chase ZEC's stale swing zone.
- **Stocks intraday:** PLANNING ONLY. Market closed, all A/B demoted to C. Re-evaluate at/after 09:30 ET. UNH stays avoid regardless of the open (legal risk).
- **Stocks swing/invest:** NO FRESH DATA (last generated 2026-07-02) — consistent with known deprecation of this legacy mode in favor of the shadow-only stocks_swing_growth_breakout framework. Not actionable, no verdict change.

## 13. Sources

- [Crypto Market News July 10: Polymarket, Bybit, Binance Lead Headlines — CoinGabbar](https://www.coingabbar.com/en/crypto-currency-news/crypto-market-news-july-10-bitcoin-price-defi-market-up-today) (2026-07-10) — BTC/ETH price + Fear&Greed
- [Zcash native surges as Zooko Wilcox announces proof progress on Ironwood upgrade — CryptoBriefing](https://cryptobriefing.com/zcash-zec-surges-ironwood-proof-progress/) (2026-07) — ZEC catalyst
- [Will Zcash's "formal verification" of Ironwood clear counterfeiting fears and boost ZEC? — AMBCrypto](https://ambcrypto.com/will-zcashs-formal-verification-of-ironwood-clear-counterfeiting-fears-and-boost-zec/) (2026-07) — ZEC catalyst detail
- [ZEC Jumps 12% as Zcash Nears Proof Against Counterfeit Bugs — CoinMarketCap](https://coinmarketcap.com/academy/article/zec-jumps-12-percent-zcash-ironwood-counterfeit-proof) (2026-07) — ZEC price reaction
- [Bitcoin and ethereum prices today, Thursday, July 9 — Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-thursday-july-9-prices-continue-sliding-on-geopolitical-tensions-125531170.html) (2026-07-09) — carried-forward macro context from prior review
- Internal: `data/catalysts/2026-07-10/catalyst_cycle_08-28.md`, `catalyst_events.jsonl`, `data/reports/intraday/2026-07-10_08-27_intraday_report.md`, `data/reports/scalp/2026-07-10_08-22_scalp_report.md`, `data/reports/stocks/intraday/2026-07-10_08-36_stocks_intraday_report.md`, `data/reports/swing/2026-07-10_01-08_swing_report.md`, `db/crypto_ai_desk.sqlite` (proposed_signals, signal_outcomes, watchlist_alerts)

## 14. Fix Requests / TODO

### TODO-scalp-negative-edge
- **issue:** Crypto scalp mode remains persistently net-negative at meaningful sample size (n=137 reliable this week, PF=0.56, avgR=-0.10, totalR=-9.70, ~10.5% win rate on triggered), yet the scalp report banner still labels it "active for data collection" and continues firing new B-tier alerts (7 new scalp upgrades at 08:27 this cycle alone: ZEC, EPIC, SENT, GRAM, DEXE, THE, XLM).
- **evidence:** `python -m src.cli signal-stats --asset-class crypto` → By-mode table, `mode=scalp` row (n=137, PF 0.5591, totalR -9.70).
- **suggested manual fix:** Human-driven session should decide whether to (a) re-run the desk's own stated "re-audit at 20 closed A/B scalp signals" checkpoint — the sample (131 triggered) is now ~6.5x past that threshold without a documented re-audit — or (b) re-kill-switch scalp mode for new entries pending a scoring change.
- **priority:** medium
- **first observed:** 2026-07-10 11:39 EEST (not a new regression; sample has simply grown well past the desk's own re-audit trigger point)

### TODO-untracked-scalp-alert
- **issue:** `detect_untracked_legacy_alerts` flags 1 untracked legacy crypto alert this window — SENT/USDT scalp B (score 66.2, long, sent 2026-07-10T08:27:07 UTC) — sent to Telegram but has no matching `proposed_signal` row, so it will not contribute to PF/winrate/avgR tracking.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-10` output.
- **suggested manual fix:** Investigate why this specific scalp alert didn't get a corresponding `proposed_signal` created (possible timing race between the `watchlist_alerts` write and the `track-signals` step, or a post-alert rejection specific to this symbol).
- **priority:** low
- **first observed:** 2026-07-10 11:39 EEST
