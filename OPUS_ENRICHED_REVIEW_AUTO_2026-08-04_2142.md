# Opus Enriched Review — Late-session risk review — Auto Cycle 21:42 EEST

## 1. Executive Summary

Slot: **late-session risk review** (21:30 EEST target, fired ~21:42; US cash session ~5h in, closes 23:00 EEST). **Advisory only — no auto-trade.** Zero A-tier and zero fresh B-tier setups on either asset class this cycle: crypto scalp/intraday reports both show "No A-tier / No B-tier setups found," and stocks intraday again demoted all 14 raw-A/B candidates to C via the SI-1..5 gates (liquidity RVOL, sector confirmation, catalyst-none). The only "active" positions worth watching are prior-cycle triggers: crypto swing **TUT/USDT long** (still the desk's best-performing playbook this week) and a handful of already-triggered B-tier intraday/swing longs (HFT, PUMP, HOME, COTI, EPIC, AEVO). Cross-asset mood is genuinely split, not a data artifact: crypto's macro overlay reads risk-off (100/100 risk score) on the still-escalating Coldcard hardware-wallet hack (~$100-130M stolen) plus Iran/Hormuz geopolitical headlines, while stocks read cleanly risk-on/bullish (VIX 16.53, breadth 100% above EMA20/50, PLTR +30% on earnings). Catalyst→symbol mapping keeps degrading — **63.5% unmapped**, the fifth consecutive worsening review (53.2%→57.2%→60.2%→62.9%→63.5%). No untracked legacy alerts fired. Earnings risk today: AMD, CAT, SMCI — do not chase into prints.

## 2. Data Used

- Crypto: `data/reports/scalp/2026-08-04_18-19_scalp_report.md` (mtime 21:19 EEST, ~23min old, fresh), `data/reports/intraday/2026-08-04_18-28_intraday_report.md` (mtime 21:28 EEST, ~14min old, fresh), `data/reports/swing/2026-08-04_14-56_swing_report.md` (mtime 17:56 EEST, ~3h46m old — carry-forward, still <4h so treated as fresh per freshness rule)
- Stocks: `data/reports/stocks/intraday/2026-08-04_18-28_stocks_intraday_report.md` (mtime 21:28 EEST, ~14min old, fresh, mid-RTH). Stocks swing/invest last generated 2026-07-01/02 — stale/deprecated (known: old stocks swing/invest frameworks deprecated), excluded.
- `data/processed/llm_analysis_packet.md` (21:29), `data/processed/llm_stocks_packet.md` (20:50)
- `data/catalysts/2026-08-04/catalyst_events.jsonl` (4000 rows today, 2539 null-symbol — computed this run), `narrative_baskets.jsonl` (2 baskets), `catalyst_cycle_18-36.md` (latest cycle file)
- CLI: `active-signals --asset-class crypto` (27 rows), `active-signals --asset-class stocks` (50 rows), `signal-stats` (both asset classes), `detect_untracked_legacy_alerts --since 2026-08-04` (0 untracked)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-04_1830.md` (US open reaction review, 18:30 EEST)
- External: **no WebSearch/WebFetch this cycle** — internal records (production news risk warnings, catalyst events, prior-review-confirmed Coldcard/geopolitical facts) were fresh, present, and internally consistent, so external verification was not required per the internal-first rule. No new legal/earnings claim in this review is unsourced from internal data.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime 21:37 EEST (~5min old at review start) — fresh, not deferred. Cycle 1/12 (boot 21:06 EEST) was still mid-cycle at review time (last step logged: "paper execution accounting refresh" 21:37:54); no `cycle_*_summary.md` exists yet for today's folder, but the scheduler-log freshness alone clears the not-deferred bar.
- Crypto scalp/intraday: <25min old — fresh. Crypto swing: ~3h46m old — carry-forward, within the <4h fresh bucket.
- Stocks intraday: ~14min old — fresh, mid-session. Stocks swing/invest: stale since 2026-07-01/02 (>1 month) — excluded, known-deprecated frameworks per standing project memory.
- No monitor/paper-status file was read this cycle (not in the allowed read list).
- No data-quality anomalies observed this cycle beyond the recurring catalyst-mapping degradation (see §5, §14).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-08-04 21:42 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh"],
      "data_missing": ["no cycle_*_summary.md for today yet (cycle 1/12 still running at review time)", "monitor/paper-status file not read (outside allowed read list)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log 21:37 EEST, ~5min old", "crypto scalp/intraday <25min old", "crypto swing ~3h46m old (carry-forward, still <4h)", "stocks intraday ~14min old", "stocks swing/invest stale since 2026-07-01/02, known-deprecated"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["mixed", "risk_off", "risk_on", "chop"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto macro/geopolitical risk score 100/100, risk-off headwind, driven by 8 risk-off news hits (Coldcard hack, Iran/Hormuz) vs 1 risk-on hit", "crypto price regime itself is 'transition (mixed)': BTC transition_up, ETH range, altcoin breadth 70% above EMA20 — not a clean risk-off tape despite the macro overlay score", "stocks regime cleanly risk_on/bullish: VIX 16.53, breadth 100% above EMA20/50, 4/4 indices uptrend", "this crypto-macro-vs-crypto-price-vs-stocks split is a genuine cross-asset divergence, consistent with the prior review's framing"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "catalyst_confirmed", "catalyst_contradicted"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["63.5% unmapped catalyst events today (2539/4000) — worse than 18:30's 62.9%, fifth consecutive worsening review: 53.2%→57.2%→60.2%→62.9%→63.5%", "2 narrative baskets: binance_ecosystem_teaser (BNB, <6h fresh), momentum_breakout (BTW, <1h fresh)", "Coldcard hack narrative confirmed ongoing/escalating across multiple independent internal sources (CoinDesk, AMBCrypto, CryptoSlate, CryptoBriefing, The Block) — consistent, not single-source noise", "PLTR: catalyst (earnings, +30% commercial-revenue beat) confirmed, but contradicted/capped by an independent legal_headline_risk flag (sec_doj) — catalyst does not clear it for actionability"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "oi_supports", "data_unavailable"],
      "data_missing": ["OI 24h n/a for several intraday movers (SKHYB, SNDKB, KORUB)", "no derivatives coverage for the stocks side"],
      "suggested_effect": "advisory_only",
      "facts_used": ["TUT/USDT swing (open): funding +5e-05, OI +18.55%, crowding normal — clean continuation positioning, not squeeze-flagged", "HFT/USDT: funding +0.00101, 'extreme long crowding' flagged in the scalp report — chase/squeeze risk if approached fresh, though it is already a triggered B-tier position not a new entry", "GIGGLE/USDT, ERA/USDT: weak-RS shorts capped to C specifically for short-squeeze risk (thin liquidity / high upper-wick) — do not treat as clean shorts"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["entry_fresh", "stale_before_entry", "price_moved_away"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TUT/USDT: preferred pullback zone 0.0230-0.0235; last observed price (14:56 report) 0.0237 — essentially inside the zone at last read, not badly extended, but not independently re-verified live this cycle", "HOME/USDT, COTI/USDT, BICO/USDT crypto intraday watchlist: all scored 50-52/100, explicitly watch-only, no fresh entry structure this cycle", "stocks: all 14 raw-A/B candidates demoted to C by liquidity/RVOL/sector/catalyst gates — no clean fresh entry structure confirmed late-session"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["open_actionable", "waiting_for_entry", "no_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TUT/USDT swing: OPEN actionable (status=triggered, expires 2026-08-11) — the desk's one live crypto position of note", "HOME/USDT intraday, PUMP/USDT intraday: WAITING for entry, not yet filled", "XRP/USDT swing short: tp1_hit — partially resolved, remainder tracking toward further TPs, not a fresh idea", "a large block of crypto (16/27) and stocks (45/50) active-signal rows carry expires_at dates weeks in the past while still tagged tp1_hit/tp2_hit/triggered — flagged again as the carried-forward lifecycle-labeling TODO (§14), not treated as fresh or actionable"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["headline_risk", "legal_risk", "manual_review", "reduce_risk"],
      "data_missing": ["no daily paper PnL figure was read this cycle (not in the allowed CLI list)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["PLTR: sec_doj legal/headline risk flag, score 100 but capped to C — do not treat the earnings pop as tradeable without operator review", "MSFT: class_action/securities_fraud legal flag, score 93 but capped to C", "Coldcard hack still escalating (internal sources), a live headline risk for BTC-correlated crypto longs", "AMD, CAT, SMCI report earnings today (2026-08-04) — explicit do_not_chase_warning; LLY, UBER report tomorrow"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto intraday mode (week): PF 3.41, avgR +0.89, 9W/9L — the strongest mode this week", "crypto swing mode (week, all setups pooled): PF 0.97, avgR -0.008 — near-breakeven-negative in aggregate, but the specific crypto_swing_narrative_rs_momentum playbook that produced TUT/USDT self-reports 14d WR 72% / PF 5.80 / +24R inside the swing report — a playbook-specific vs mode-aggregate gap worth noting, not treated as contradictory since they measure different cohorts", "crypto scalp mode (week): PF 0.17, 0W/3L — confirms the scalp report's own 'low confidence, data-collection only' framing", "stocks C-tier (week): PF 0.65, 4W/12L; stocks shorts specifically: PF 0.14, 1W/10L over 30d paper — avoid new stock shorts; stocks A/B headline sample n=7, anecdotal confidence, do not tune on it"] },
    { "agent": "head_trader", "verdict": "watch_only", "confidence": 0.6,
      "reason_codes": ["mixed", "wait_for_trigger", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["no A-tier or fresh B-tier anywhere this cycle; one open crypto swing position (TUT/USDT) to monitor into invalidation/TP; stocks cleanly risk-on but gate-blocked; PLTR/MSFT are earnings-catalyst-confirmed but legal-risk-avoid, not buys"] }
  ],
  "head_trader": {
    "overall_verdict": "watch_only",
    "confidence": 0.6,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "TUT/USDT (open, add-on only)", "trigger": "retest of 0.0230-0.0235 zone holding on 1h close, invalidation 0.0224 unbroken", "reason": "Only currently-open crypto long with a working playbook (RS-leader + narrative-basket swing, 14d PF 5.80 self-reported); not a fresh entry, a hold/monitor idea" },
    "best_short_candidate":    { "symbol": "none clean — GIGGLE/USDT watch", "trigger": "confirmed bearish HTF structure + clear stop above swing high once short-squeeze risk (thin liquidity, high upper-wick) clears", "reason": "Weakest RS symbol (-15.3% vs BTC) but explicitly capped to C for squeeze risk this cycle; stocks shorts are separately in a confirmed 30d losing streak (PF 0.14) — avoid new stock shorts entirely for now" },
    "best_catalyst_candidate": { "symbol": "none actionable — AVGO/chip-sector watch", "trigger": "RVOL clears liquidity gate + sector (SMH/XLK) confirmation returns, keeping the existing chip-rally catalyst (Intel +10%, AMD +8%, AVGO +6% same-day)", "reason": "Real catalyst and real move already happened, but stocks-intraday gates (liquidity_rvol_below_min, sector_confirmation_weak_or_unknown) still block it from actionable status" },
    "avoid_candidate":         { "symbol": "PLTR", "reason": "Score 100, earnings catalyst confirmed (+30% on 'otherworldly' commercial revenue), but carries an active sec_doj legal/headline risk flag — chasing a name already up 30% AND under legal-risk caps is a clean avoid, not a manual-review edge case" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh | advisory_only |
| market_regime | caution | 0.65 | mixed, risk_off, risk_on, chop | advisory_only |
| catalyst_narrative | caution | 0.6 | mapping_weak, fresh_catalyst, catalyst_confirmed, catalyst_contradicted | advisory_only |
| derivatives_squeeze | caution | 0.5 | squeeze_risk, oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | entry_fresh, stale_before_entry, price_moved_away | advisory_only |
| execution_lifecycle | caution | 0.6 | open_actionable, waiting_for_entry, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.6 | headline_risk, legal_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | watch_only | 0.6 | mixed, wait_for_trigger, manual_review | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-04_1830.md` (18:30, US open reaction):

- **New:** none — no new A/B setups fired on either asset class this cycle.
- **Removed:** none of the prior watchlist names carried over as named ideas (18:30 didn't name specific new watch symbols either, beyond the open TUT/USDT position).
- **Upgraded/downgraded:** no tier changes to report; PLTR/MSFT remain capped to C for the same legal/headline reasons as before.
- **New catalysts:** PLTR's Q2 "otherworldly" commercial-revenue beat and the broad chip-sector rally (Intel +10%, AMD +8%, AVGO +6%) are new since 18:30, both gate-blocked from actionability.
- **Thesis changed:** none. TUT/USDT thesis unchanged (still the desk's best-performing crypto swing playbook this week).
- **Confirmed:** stocks risk-on regime persists (VIX drifted 16.23→16.53, still calm); no untracked legacy alerts again this cycle (bug dormant, root cause still unfixed per §14).
- **Invalidated:** none.
- Catalyst mapping continued its now 5-review losing streak: 62.9%→63.5% unmapped.

## 5. Catalyst Coverage

- Total catalyst events today: **4000**; mapped (non-null symbol): **1461**; unmapped: **2539** (**63.5%**).
- Narrative baskets: **2** (`binance_ecosystem_teaser` — BNB, fresh <6h; `momentum_breakout` — BTW, fresh <1h).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Unmapped exceeds 50% for the fifth consecutive review.
- Top unmapped-adjacent headlines this cycle were dominated by generic macro/geopolitical items (Iran/Hormuz, Coldcard hack updates) and broad-market commentary that don't resolve to a single ticker — consistent with the pattern already flagged in §14 across prior reviews.

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **mixed** — macro overlay risk-off (100/100 score, Coldcard hack + geopolitical headlines) but underlying price action is transition/constructive (BTC transition_up, ETH range, 70% of alts above EMA20).
- Stocks mood: **risk-on / bullish** — VIX 16.53, breadth 100% above EMA20/50, 4/4 indices uptrend.
- Dominant narrative: Coldcard hardware-wallet exploit (ongoing, ~$100-130M stolen) dominating crypto headline flow; chip-sector rally + PLTR earnings dominating stocks headline flow.
- Preferred side now: **wait-for-trigger** — no clean directional edge confirmed on either asset class this cycle; existing crypto swing longs (TUT/USDT) can be held/monitored, not added to blindly.
- Best long candidate: none fresh — TUT/USDT (open position) is the closest thing to a working long thesis.
- Best short candidate: none clean — GIGGLE/USDT is the weakest-RS name but squeeze-risk-capped; avoid new stock shorts given the confirmed 30d PF 0.14 losing streak on that side.
- Best catalyst-backed candidate: none actionable — AVGO/chip-sector cluster has a real catalyst but is gate-blocked (liquidity/sector confirmation).
- What to avoid: PLTR (legal/DOJ risk stacked on an already-priced +30% move), new stock shorts generally, chasing AMD/CAT/SMCI into today's earnings prints.
- What would change the view: stocks RVOL/sector-confirmation gates clearing on the chip-rally names; crypto macro risk score coming off 100/100 as the Coldcard hack narrative resolves; a clean pullback-and-hold on HOME/USDT or COTI/USDT with volume confirmation.

## 7. Candidate Deep Dives

### TUT/USDT (crypto swing long, OPEN actionable)
- Status: triggered, expires 2026-08-11. Playbook `crypto_swing_narrative_rs_momentum` (self-reported 14d WR 72% / PF 5.80 / +24R for this specific playbook, vs a near-breakeven -0.008 avgR for the swing mode in aggregate this week — a playbook-vs-mode gap, not a contradiction, since the playbook cohort is narrower).
- Has price already reacted to the catalyst? No fresh verified catalyst was ever cited for this name — it's a pure RS-leader/momentum thesis (24h +15.55%, 7d +71.86%, RS vs BTC +15.39% at last report).
- Chasing? No — last observed price (14:56 report) 0.0237 sits essentially inside the preferred pullback entry zone (0.0230-0.0235), not extended.
- Overextended (>2 ATR from EMA20)? Not per the report at read time.
- Actionable now or confirmation-only? Already triggered/open — this is a hold/monitor, not a new-entry decision.
- Invalidation: 1h close beyond 0.0224. Not independently re-verified with a live price this cycle (no live-price CLI in the allowed tool list) — flagged as a data gap, not a risk event.
- Chase-risk setup? No, given entry proximity at last read.
- Catalyst confirmation/contradiction: none cited either way; thesis is purely technical/RS.
- Mood alignment: crypto's price-level regime (transition, 70% breadth) supports continuation longs even though the macro overlay is risk-off — a case where the macro score and the tradeable regime diverge, and the RS-leader thesis leans on the latter.

### PLTR (stocks, C-tier, AVOID)
- Score 100 (raw A), demoted to C for `legal_headline_risk: sec_doj`.
- Has price already reacted to the catalyst? Yes — already +30% same-day on "otherworldly" Q2 commercial revenue per the report's own news feed; entering now would be chasing a fully-realized move.
- Chase-risk: high — both because of the size of the move already made and because of the active SEC/DOJ flag.
- Actionable now or confirmation-only? Never — legal/headline risk demotions are a hard cap in this pipeline, correctly excluding it from actionable status regardless of the underlying score.
- What would invalidate the avoid call: a resolution or de-escalation of the SEC/DOJ matter, confirmed via a verified external source (not available this cycle, no WebSearch run).
- Mood alignment: aligned with the bullish stocks tape, but the legal overlay overrides mood-alignment for actionability.

### AVGO / chip-sector cluster (stocks, C-tier, catalyst-backed watch)
- AVGO score 97 (raw A), demoted to C for `liquidity_rvol_below_min` + `catalyst_none_and_not_exceptional_technical`; SMCI/NVDA/XLK/JPM/GOOGL similarly demoted mostly on `sector_confirmation_weak_or_unknown` + the same liquidity/catalyst gates.
- Has price already reacted? Yes — "Intel Soars 10%, AMD Jumps 8%, Broadcom Rises 6% as Chip Stocks Ride a Risk-On Rally" per the news feed; the move is same-day and ongoing, not stale.
- Chase risk: moderate — the rally is broad and sector-wide (reduces single-name chase risk) but RVOL confirmation is explicitly missing per the gate.
- Actionable now or confirmation-only? Confirmation-only — needs the liquidity/sector gates to clear, which is a data-driven bar, not a subjective call.
- What would make it actionable: RVOL clearing the minimum threshold and SMH/XLK sector-RS confirmation strengthening from its current "mixed" status.
- Mood alignment: fully aligned with the bullish stocks regime; this is a "wait for confirmation," not a "avoid," idea.

### HOME/USDT, COTI/USDT, BICO/USDT (crypto intraday, C-tier watchlist)
- All three scored 50-52/100, explicitly watch-only per the intraday report ("Score is below active-trade threshold; this is watchlist/no-trade").
- No fresh verified catalyst on any of the three; all are momentum/RS plays in a "transition (mixed)" regime with below-average volume ratios (0.21-0.34x) — the report's own known-failure-mode note for this playbook ("No-catalyst intraday in chop is net-negative") applies directly.
- Actionable now? No — all three need either a verified catalyst or a clean breakout/RS-leader confirmation on 15m-1h structure before promotion.
- Mood alignment: momentum-consistent with the 70%-above-EMA20 breadth reading, but the "chop" framing and lack of catalyst keep them sub-threshold.

## 8. Best Candidates Ranked

1. **TUT/USDT (crypto swing long, OPEN)** — hold/monitor; add-on only on a clean retest of 0.0230-0.0235 with invalidation 0.0224 intact.
2. **AVGO / chip-sector cluster (stocks, catalyst-backed watch)** — wait for RVOL + sector-confirmation gates to clear.
3. **HOME/USDT (crypto intraday, long-watch)** — wait for RS-leader or breakout confirmation on 15m-1h with volume.
4. **GIGGLE/USDT (crypto, short-watch)** — wait for squeeze risk to clear and bearish HTF structure to confirm before treating as a short.
5. **PLTR (stocks, AVOID)** — do not chase; legal/headline risk caps it regardless of score.

No clean new-entry candidate cleared the desk threshold this cycle on either asset class — consistent with the last several reviews.

## 9. Avoid / No Trade

*(This applies to this decision window only — scanning, tracking, and the scheduler continue unchanged.)*

- **PLTR** — already +30% on the day, active SEC/DOJ legal-risk flag; avoid chasing.
- **MSFT** — active class-action/securities-fraud legal-risk flag; avoid despite score 93.
- **AMD, CAT, SMCI** — earnings today (2026-08-04); explicit do_not_chase_warning from the production risk layer.
- **New stock shorts generally** — 30d paper performance on stock shorts is PF 0.14 (1W/10L); no new short ideas on this side until the trend reverses.
- **GIGGLE/USDT, ERA/USDT shorts** — squeeze-risk-capped (thin liquidity / high upper-wick); not clean shorts as-is.
- **Crypto scalp mode generally** — PF 0.17 (0W/3L) this week; the report itself frames scalp as data-collection only, low confidence.

## 10. Main Risks

- Coldcard hardware-wallet hack remains unresolved and escalating per internal sources ($100-130M range, still climbing) — a live headline-risk overhang for BTC-correlated crypto longs.
- Geopolitical (Iran/Hormuz) headlines continue to drive the crypto macro-risk score to 100/100 even as underlying crypto price action stays constructive — a genuine cross-signal divergence that could resolve either direction.
- Catalyst→symbol mapping degradation (63.5% unmapped, 5th consecutive worsening review) reduces confidence in any catalyst-backed framing this cycle; treat catalyst context as directional color, not confirmation.
- A large block of "active" signals (16/27 crypto, 45/50 stocks) carry expired `expires_at` dates while still tagged `triggered`/`tp1_hit`/`tp2_hit` — the lifecycle-labeling ambiguity flagged in prior reviews (§14) makes it hard to distinguish genuinely open risk from stale/closed rows without a manual pass.
- Earnings risk today (AMD, CAT, SMCI) and tomorrow (LLY, UBER) — headline/gap risk into and immediately after prints.

## 11. Action Plan — next 4 hours

- Monitor TUT/USDT into its invalidation (0.0224) / TP1 (0.0248) — no action needed unless price closes through invalidation on the 1h.
- Watch AVGO/chip-sector cluster for RVOL and sector-confirmation gates to clear before treating as actionable.
- Watch HOME/USDT and COTI/USDT for a volume-confirmed breakout or RS-leader confirmation; do not chase the current extended reads.
- Do not initiate any position in PLTR, MSFT, AMD, CAT, or SMCI given active legal/headline/earnings flags.
- Re-check catalyst mapping % at the next cycle to see if the 5-review worsening trend continues or stabilizes.
- Continue scanning/tracking/monitors unchanged — this review recommends caution on new entries only, not a pause of any kind.

## 12. Final Verdict per Mode

- **Crypto scalp:** no trade — data-collection only, PF 0.17 this week, no A/B setups this cycle.
- **Crypto intraday:** no trade — no A/B setups this cycle; HOME/COTI/BICO watch-only.
- **Crypto swing:** hold existing (TUT/USDT); no new entries — mode is near-breakeven-negative in aggregate despite the RS-momentum playbook's strong self-reported stats.
- **Stocks intraday:** no trade — 0/14 raw A/B cleared gates; bullish regime does not override liquidity/sector/legal caps.
- **Stocks swing/invest:** not evaluated — reports stale/deprecated, excluded per standing policy.

## 13. Sources

- Internal only this cycle (no external WebSearch/WebFetch run): `data/reports/scalp/2026-08-04_18-19_scalp_report.md`, `data/reports/intraday/2026-08-04_18-28_intraday_report.md`, `data/reports/swing/2026-08-04_14-56_swing_report.md`, `data/reports/stocks/intraday/2026-08-04_18-28_stocks_intraday_report.md`, `data/catalysts/2026-08-04/catalyst_events.jsonl`, `data/catalysts/2026-08-04/narrative_baskets.jsonl`, `OPUS_ENRICHED_REVIEW_AUTO_2026-08-04_1830.md`.

## 14. Fix Requests / TODO

### TODO-catalyst-mapping-persistently-weak (priority: low, recurring, worsening)
- **issue:** Catalyst→symbol mapping has now been over the 50% unmapped threshold for at least five consecutive reviews and continues to worsen: 53.2% (04:45) → 57.2% (11:39) → 60.2% (16:11) → 62.9% (18:30) → **63.5%** (this run).
- **evidence:** `data/catalysts/2026-08-04/catalyst_events.jsonl` (4000 rows today, 2539 null-symbol, computed this run).
- **suggested manual fix:** revisit the symbol resolver in the catalyst layer; a monotonically worsening trend across five reviews in the same day suggests this isn't a stable share of un-mappable macro noise but a resolver regression or an upstream feed change.
- **priority:** low
- **first observed:** 2026-08-04 04:45 EEST (carried forward, still unresolved, still worsening).

### TODO-legacy-open-position-volume (priority: medium, carried forward, unresolved)
- **issue:** `active-signals` still returns dozens of rows (16/27 crypto, 45/50 stocks) with `expires_at` dates in the past while status reads `tp1_hit`/`tp2_hit`/`triggered` — unclear whether these are correctly "not yet finally closed" by design or a stuck closure job.
- **evidence:** e.g. `sig_b16bb9e54598333a` (NEAR scalp, tp1_hit, expires_at 2026-07-17T15:56:12) still present in this run's `active-signals --asset-class crypto` output, nearly three weeks past expiry.
- **suggested manual fix:** unchanged from prior reviews — a human-driven session should confirm the intended lifecycle semantics and, if needed, add clearer status labeling in the CLI output.
- **priority:** medium
- **first observed:** 2026-08-04 11:39 EEST (carried forward, still unresolved).

### TODO-untracked-alert-bug-not-refired-but-unfixed (priority: high, recurring root cause, dormant this cycle)
- **issue:** The watchlist-alert signal-reuse bug (re-fire reuses a stale/closed `signal_id` instead of minting a fresh `proposed_signal`) produced no untracked alerts this cycle (0) — but the underlying root cause remains unfixed, so recurrence is expected whenever the same watchlist symbol re-fires.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-04` returned 0 this run; prior confirmed instances on ALLO/USDT, BANK/USDT (2026-07-17) and TUT/USDT (2026-08-04 16:11).
- **suggested manual fix:** as already raised (TODO-3, raised to high priority 2026-07-17): fix the watchlist-alert path so a re-fire mints a fresh `proposed_signal` instead of reusing a stale/closed `signal_id`.
- **priority:** high
- **first observed root cause:** 2026-07-17; **last confirmed instance:** 2026-08-04 16:11 EEST (TUT/USDT); **this cycle:** dormant, not fixed.
