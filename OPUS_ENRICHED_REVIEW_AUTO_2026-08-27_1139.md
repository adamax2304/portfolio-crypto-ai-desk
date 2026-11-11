# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:39 EEST

## 1. Executive Summary
- Slot: **Europe / pre-US context** (04:39 ET / pre-market). Advisory only — no auto-trade, no code/strategy changes made.
- Crypto: no fresh A/B triggers this cycle in scalp or intraday; scalp mode remains disabled by kill-switch. Swing book carries 9 active B-tier longs (top: BICO/USDT 71.2), all momentum/RS-based, **none catalyst-confirmed**.
- Stocks: US cash session closed → all 15 raw-A/B candidates (ORCL, DELL, MSFT, ARM, ANET, MSTR, QCOM, AMD, HOOD, CRCL, BKNG, XOM, XLY, NVDA, REGN) demoted to C-tier "planning only" by the market-closed gate. Zero actionable A/B.
- Two names carry active legal/headline risk and must NOT be chased even after the gate lifts: **NVDA** (short, Taiwan indictment of an NVDA manager for chip smuggling, verified) and **REGN** (short, active securities class action, verified).
- Macro backdrop is risk-off (Hormuz tanker incident, Ukraine strikes, macro risk score 100/100) but crypto price action (BTC/ETH uptrend, 77% of alts above EMA50) is constructive — a genuine **mixed** regime, not a blanket no-trade.
- Catalyst mapping is weak this run (79% unmapped) — treat the catalyst layer as context only, not a decision driver.

## 2. Data Used
- Reports: scalp (07:17 EEST), intraday (07:28 EEST), swing (04:47 EEST) — crypto; stocks intraday (08:20 EEST) — all same-day, all fresh (<4.5h).
- Stocks swing/invest reports: none newer than 2026-07-02 — this framework is deprecated/removed per project history; excluded from this review (not "stale", genuinely retired).
- `data/catalysts/2026-08-27/` (catalyst_events.jsonl, narrative_baskets.jsonl, catalyst_cycle_07-35.md) — fresh (10:35 EEST).
- `data/processed/llm_analysis_packet.md` (10:31), `llm_stocks_packet.md` (11:23).
- CLI: `active-signals` (crypto n≈112 open, stocks n≈209 open), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts` (0 found).
- DB read queries: `news_items` (NVDA, ORCL, REGN, BICO, PYTH, HEMI symbol checks), `proposed_signals` status counts.
- External web research unavailable this run (WebSearch/WebFetch not exercised — internal records were sufficient and recent for every candidate reviewed; no candidate required external verification per §G).

## 3. Scheduler / Data Freshness
- `data/scheduled_runs/2026-08-26_default_schedule/scheduler.log` — mtime 11:38 EEST (1 min old). **Fresh.**
- Latest cycle summary `cycle_06_10-02_summary.md` — mtime 11:38 EEST. **Fresh.**
- No defer/blocker triggered.
- Monitor/paper status: not separately queried this run (not in the read-only allowlist); no anomaly signal from `detect_untracked_legacy_alerts` (0 untracked crypto alerts).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-08-27 11:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["stocks_swing_invest_reports (deprecated, not a gap)"],
      "suggested_effect": "advisory_only", "facts_used": ["scheduler.log mtime 11:38", "cycle_06 summary mtime 11:38", "intraday/scalp reports <4.5h old"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["mixed", "risk_off", "longs_preferred"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["BTC/ETH uptrend both crypto reports", "macro risk score 100/100 risk-off", "stocks regime=transition, VIX 14.92, bias neutral"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "no_catalyst", "fresh_catalyst"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["79.2% unmapped catalyst events today", "3 narrative baskets: ai_narrative, perps_dex_narrative, momentum_breakout", "BICO/PROM/PYTH/HEMI: 0 fresh news_items hits in 24h"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "data_unavailable"], "data_missing": ["bybit/OKX depth for PYTH/POL/GPS shorts"],
      "suggested_effect": "advisory_only", "facts_used": ["GPS/POL/ACE short setups capped to C by thin_liquidity_short_squeeze_risk", "PYTH price down + OI down = deleveraging, not squeeze-prone"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["entry_late", "chase_risk", "stale_before_entry"], "data_missing": ["OHLCV/ATR levels for ORCL/DELL/MSFT planning candidates (not published while C-tier)"],
      "suggested_effect": "advisory_only", "facts_used": ["MOVR/PROM/TAO flagged >2 ATR from EMA20 — do not chase", "BICO entry pullback zone 0.0276-0.0287 vs current 0.0291 — close to zone"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "no_entry"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["crypto: 65 entered-unresolved, 36 open-actionable (TP1/TP2 partial), 11 waiting", "stocks: 15 entered-unresolved, 194 open-actionable (TP1/TP2 partial), 0 waiting"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["NVDA: Taiwan indictment of NVDA manager (chip smuggling), verified via Finnhub/Bloomberg/CryptoBriefing 2026-08-24/25", "REGN: active securities class action, verified via 5+ PR Newswire filings since 2026-08-20", "AFRM, MRVL earn today — do-not-chase"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["crypto scalp mode PF 0.11 (net-negative, disabled)", "crypto intraday PF 2.19 (healthy)", "crypto swing PF 1.80", "stocks C-tier PF 0.59 / winrate 8% (weak)", "stocks A-tier n=8 PF=inf but tiny sample"] },
    { "agent": "head_trader", "verdict": "ok", "confidence": 0.65,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["synthesis of all 8 agents"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "BICO/USDT", "trigger": "already triggered — hold/add only on pullback into 0.0276-0.0287, invalidate 1h close below 0.0263", "reason": "RS-leader (+48.6% vs BTC 24h), 14d swing playbook WR 72% / PF 5.80, bullish HTF regime" },
    "best_short_candidate":    { "symbol": "PYTH/USDT", "trigger": "not system-leveled (scalp kill-switch off) — manual watch only: confirm 1h close below recent swing low with RS staying <-10% and no bullish catalyst reversal", "reason": "RS -11.7% vs BTC, 2.46x volume expansion, price down + OI down (deleveraging, not squeeze-prone unlike POL/GPS)" },
    "best_catalyst_candidate": { "symbol": "ORCL", "trigger": "confirm opening range holds above pre-market reference + no fade in first 15-30min of RTH before treating A-tier score (92.47) as live", "reason": "raw A-tier, high confidence, positive analyst/conference coverage 2026-08-26, no legal/earnings flags — cleanest of the market-closed-gated names" },
    "avoid_candidate":         { "symbol": "NVDA", "reason": "Taiwan indictment of an NVDA manager for GPU smuggling (verified, 2026-08-24/25) stacked with a same-day Hugging Face acquisition-talk headline and stale post-earnings levels — legal_headline_risk demotes any short to manual review; REGN carries a parallel active class-action risk on the short side" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---:|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale(n/a) | advisory_only |
| market_regime | caution | 0.70 | mixed, risk_off, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, no_catalyst, fresh_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | entry_late, chase_risk, stale_before_entry | advisory_only |
| execution_lifecycle | ok | 0.80 | open_actionable, waiting_for_entry, entered_unresolved | advisory_only |
| risk_manager | caution | 0.75 | legal_risk, headline_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.70 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | ok (synthesis) | 0.65 | — | advisory_only |

## 4. What Changed vs Previous Review
Previous: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-27_0440.md` (04:40 EEST, crypto overnight/Asia slot).
- Crypto swing book unchanged in composition (same 9 B-tier longs — BICO, PROM, ONG, TUT, S, GIGGLE, SOL, TAO, ONT); scores drifted slightly (e.g. BICO likely similar), still no catalyst confirmation on any.
- Stocks: still zero actionable A/B — the market-closed-planning-only gate persists into the Europe slot as expected pre-open; same top-of-book names (ORCL, DELL, MSFT, ARM, ANET) reappear as A-tier raw.
- NVDA/REGN legal-risk flags carried forward unchanged (Taiwan indictment story is now 2-3 days old, still active; REGN class action deadline unchanged at 2026-09-14).
- Catalyst mapping was already weak in the overnight review; still >50% unmapped this cycle — persistent, not a new regression (see §14 TODO).
- No signals invalidated or newly confirmed since 04:40; no new HIGH-severity news since overnight (NVDA/Hugging Face talk and REGN suits were already flagged then).

## 5. Catalyst Coverage
- Catalyst events today (`catalyst_events.jsonl`, cumulative across cycles): 1,500 rows logged; **312 mapped to a symbol (20.8%), 1,188 unmapped (79.2%)**.
- Narrative baskets: 3 (`ai_narrative`, `perps_dex_narrative`, `momentum_breakout`).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top unmapped headlines (macro/central-bank noise, not symbol-specific):
  1. "BOJ'S HIMINO: FINANCIAL CONDITIONS STAY ACCOMMODATIVE, BELIEVE WE SHOULD EASE OFF ACCELERATOR TIMELY AND CONTINUE RAISING POLICY RATE"
  2. "BOJ'S HIMINO: THE BIGGEST CHALLENGE IN OUR COMMUNICATION IS THE ISSUE OF TIME HORIZONS"
  3. "BOK: FUTURE INFLATION PATH HIGHLY UNCERTAIN AMID OIL PRICES, FX RATES AND DOMESTIC DEMAND RECOVERY"

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **mixed** — HTF regime bullish (BTC/ETH uptrend, swing report calls it "bullish trend / risk-on"), but short-timeframe intraday/scalp regime is "range/chop (neutral)" and macro geopolitical risk score is 100/100 risk-off (Hormuz tanker attack, Ukraine strikes). Treat as risk-on structurally, risk-off tactically.
- Stocks mood: **transition / pre-market — planning only.** VIX 14.92 (low), breadth mixed (50% >EMA20, 100% >EMA50), SPY uptrend but QQQ/IWM range. Technology and semiconductors are the strongest sectors on 20d RS; utilities/real estate/staples weakest.
- Dominant narrative: AI-adjacent momentum (ai_narrative basket: NEAR, RENDER, TAO, FET) and a fresh momentum_breakout basket around TUT; on stocks, AI-hardware names (ORCL/DELL/MSFT/ARM/ANET) dominate the raw A-tier list pre-open.
- Preferred side now: **longs** on crypto (RS-leader/swing continuation, no fresh shorts confirmed clean), **catalyst-backed watch** on stocks (wait for RTH confirmation before either side).
- Best long candidate: BICO/USDT (already triggered, respect entry/invalidation).
- Best short candidate: none clean and system-leveled — PYTH/USDT is the best directional short-watch (manual, no formal levels).
- Best catalyst-backed candidate: ORCL (stocks, pending RTH confirmation).
- What to avoid: NVDA and REGN shorts (legal/headline risk, manual review required); any crypto entry >2 ATR from EMA20 (MOVR, PROM, TAO all flagged extended).
- What would change the view: RTH open confirming (or fading) the ORCL/DELL/MSFT/ARM/ANET cohort; BTC losing local support would flip crypto long-preference to defensive.

## 7. Candidate Deep Dives

### 7.1 BICO/USDT — LONG (crypto swing, B-tier, already triggered) — best long
- Status: **OPEN actionable** (entered-unresolved / running; entry zone 0.0276-0.0287, current price 0.0291 at report time).
- Score 71.2/100, playbook `crypto_swing_narrative_rs_momentum` (14d WR 72% / PF 5.80 / +24R for this playbook).
- 24h return +48.5%, RS vs BTC +48.6%, volume 1.33x. Trend uptrend, setup quality 72.7/100.
- No fresh verified catalyst — pure RS/momentum thesis. Chase risk noted explicitly by the system ("move may be late relative to EMA20/ATR").
- Invalidation: 1h close beyond 0.0263. Targets TP1 0.0315 / TP2 0.0338 / TP3 0.0362.
- Is it chasing? Borderline — price (0.0291) sits just above the stated pullback entry zone, not deeply extended, but the 24h move (+48%) is large. Treat as "respect existing entry, do not add on further extension."
- Aligned with mood: yes (risk-on HTF regime, RS leadership). Actionable now (already live) — not a new-entry recommendation.

### 7.2 PYTH/USDT — SHORT-WATCH (crypto, not system-leveled) — best short candidate
- Score 60.2 (short) in scalp evaluation, disabled by the scalp kill-switch (mode off) rather than by setup quality — this is a data point, not a live signal.
- 24h -11.8%, RS vs BTC -11.7%, volume 2.46x average (unusual volume flag: `weak_vs_market`, `volume_expansion`).
- Derivatives: price down + OI down = deleveraging / long liquidation — a cleaner short structure than POL/GPS/ACE, which are capped to C for thin-liquidity squeeze risk.
- No fresh catalyst on either side; RWA narrative basket status is "rising" but PYTH itself carries the weak tag within it (contradiction: narrative heat rising while PYTH RS is negative — worth noting, not resolving).
- Trigger to make this actionable: confirmed 1h close below the recent swing low with RS staying weaker than -10% vs BTC and volume staying elevated; no formal entry/invalidation levels are published by the system while scalp mode is off, so this stays a manual-watch idea, not an operator-actionable one.
- Chase risk: low (has already moved down significantly) — better suited to a failed-bounce-short structure than a fresh breakdown chase.

### 7.3 ORCL — LONG-WATCH (stocks, raw A-tier, gated) — best catalyst-backed candidate
- Score 92.47, confidence high, raw tier A, demoted to C solely by `market_closed_intraday_planning_only` (US cash session closed at review time) — not a quality problem.
- Recent news (24h, internal `news_items`, 7 items): "Oracle Stock Is Rising Today," Citi bull case commentary, Deutsche Bank Technology Conference presentation — supportive but not a hard catalyst (no earnings/contract announcement in the window).
- No legal/earnings/headline flags on ORCL.
- No OHLCV/ATR/entry levels are published by the system for demoted planning-only C-tier names — do not fabricate a level. TradingView/manual chart check unavailable this run.
- Actionable only after RTH open confirmation (first 15-30 min), consistent with the pre-US-open slot rule: do not treat pre-market strength as confirmed.
- Would invalidate: a weak/fading open relative to pre-market strength, or broad tech-sector reversal (semiconductors/technology are currently the strongest 20d RS sectors — a reversal there would undercut the thesis).

### 7.4 NVDA — AVOID / MANUAL REVIEW (stocks, short C-tier, gated) — avoid candidate
- Raw B-tier short (score 77.74), demoted to C by both `market_closed_intraday_planning_only` and `legal_headline_risk: indictment`, plus `stale_post_earnings_setup` (earnings verified 2026-08-27T05:11:40Z, pre-earnings levels invalid).
- **Verified**: Taiwan indicted an NVDA manager (not the company) for alleged B300 GPU smuggling to China, alongside 8 others in a broader probe that also touched SMCI. Sources: Finnhub company-news (2026-08-25), CryptoBriefing (2026-08-24), Bloomberg via Finnhub (2026-08-24). Dates confirmed via internal `news_items`.
- Same-day noise: unverified "NVDA in talks to acquire Hugging Face for $13B" chatter (Telegram sources WatcherGuru/marketfeed, `exploit_hack` tag applied by the pipeline — likely a tagging artifact, not an actual exploit; treat the acquisition claim itself as single-source/unverified).
- Also carries fresh 10-Q filing (2026-08-26) and heavy AWS GPU deployment news — genuinely newsy name right now, but the combination of stale post-earnings levels + active legal risk means neither long nor short is clean.
- Verdict: **manual review required**, not a clean short OR long until levels are rebuilt post-earnings and the legal story matures.

### 7.5 REGN — AVOID / MANUAL REVIEW (stocks, short C-tier, gated) — secondary avoid
- Raw A-tier short (score 82.06), demoted to C by `legal_headline_risk: class_action` plus market-closed gate.
- **Verified**: active securities class-action solicitation campaign, at least 5 separate PR Newswire filings from different plaintiff firms since 2026-08-20, common lead-plaintiff deadline September 14, 2026. This pattern (multiple firm solicitations) confirms active litigation exists but does not by itself confirm the underlying fraud allegation — treat as elevated headline risk, not proof of wrongdoing.
- No further internal record contradicting or confirming the short thesis technically; system correctly routes this to manual review rather than a clean actionable.

## 8. Best Candidates Ranked
1. **BICO/USDT** — long, already open, respect stated invalidation (0.0263) and targets — clearest, most system-confirmed idea this cycle.
2. **ORCL** — long-watch, best catalyst-backed pre-US-open name, actionable only after RTH confirmation.
3. **PYTH/USDT** — short-watch, cleanest short structure available but manual/unleveled — needs a confirmed breakdown close before treating as live.
4. PROM/USDT, ONG/USDT — secondary crypto swing longs, same caveats as BICO (no catalyst, momentum-only), already triggered/registered.

If none of the above satisfy: the best long-watch is BICO (already live), the best short-watch is PYTH/USDT (trigger: 1h close below recent swing low, RS < -10%), and the best catalyst-watch is ORCL (trigger: RTH open holds pre-market strength).

## 9. Avoid / No Trade
- This decision window only — scanning, tracking, and the scheduler continue uninterrupted.
- **NVDA** (either direction) — legal/headline risk (verified Taiwan indictment) + stale post-earnings levels — manual review required.
- **REGN** (short) — active securities class action — manual review required.
- Any crypto entry >2 ATR from EMA20 (MOVR, PROM/scalp-context, TAO flagged explicitly by the system as "do not chase").
- POL/USDT, GPS/USDT, ACE/USDT shorts — thin-liquidity squeeze risk, capped to C by the system; do not manually override.

## 10. Main Risks
- Macro/geopolitical risk-off headlines (Hormuz tanker attack, Ukraine strikes) could pressure risk assets broadly into the US open — watch BTC for loss of local support as the tell.
- Catalyst mapping is weak this run (79% unmapped) — any catalyst-backed thesis should be treated as directional color, not confirmation.
- Stocks book still gated by market-closed-planning-only; every "top candidate" here is a pre-open plan, not a live entry.
- AFRM and MRVL report earnings today — explicit do-not-chase warning from the system.
- Crypto scalp mode remains structurally net-negative (PF 0.11) and is correctly disabled — do not manually re-enable.

## 11. Action Plan — next 4 hours
- Hold BICO/PROM/ONG/other active swing longs per their stated invalidation levels; no new crypto entries without a fresh RS or catalyst confirmation.
- Watch ORCL/DELL/MSFT/ARM/ANET into the US cash open; require first-15-30min RTH confirmation before treating any as actionable, per the pre-US-open slot rule.
- Watch PYTH/USDT for a confirmed breakdown close if a manual short is desired; do not manufacture entry levels the system hasn't published.
- Do not touch NVDA or REGN in either direction until legal/headline risk clears or an operator explicitly manually reviews and clears them.
- Re-check catalyst mapping health at the next cycle; if still >50% unmapped, this becomes a pattern worth the TODO in §14 escalating in priority.

## 12. Final Verdict per Mode
- **Scalp (crypto):** No trade — mode disabled by kill-switch (PF 0.11, structurally negative). Data collection only.
- **Intraday (crypto):** No trade — no A/B setups this cycle; HEMI/USDT is best watchlist name (60.4/100), not actionable.
- **Swing (crypto):** Hold existing B-tier longs (BICO best of the 9); no new entries without catalyst or cleaner RS confirmation.
- **Stocks intraday:** No trade — market-closed-planning-only gate. Watch ORCL/DELL/MSFT/ARM/ANET cohort into RTH; avoid NVDA/REGN entirely pending manual review.
- **Stocks swing/invest:** Deprecated frameworks, not evaluated (see project history — new shadow-only stocks_swing_growth_breakout framework is separate and not yet live-facing).

## 13. Sources
- [Nvidia Manager Named "Key Figure" in Alleged B300 GPU Smuggling to China, 8 Others Indicted in Taiwan Probe](internal: news_items, Finnhub company-news, 2026-08-25)
- [Nvidia manager indicted in Taiwan for smuggling AI chips to China](internal: news_items, CryptoBriefing, 2026-08-24)
- ['Taiwan Indicts Nvidia Manager Following Chip Smuggling Probe' - Bloomberg](internal: news_items, via Finnhub, 2026-08-24)
- [Regeneron Pharmaceuticals, Inc. (REGN) Investors: September 14, 2026 Lead Plaintiff Deadline in Class Action Lawsuit](internal: news_items, PR Newswire (Stocks), 2026-08-26)
- [Regeneron Pharmaceuticals, Inc. Investors with Substantial Losses Have Opportunity to Lead Regeneron Class Action Lawsuit](internal: news_items, PR Newswire (Stocks), 2026-08-24)
- [Oracle Stock Is Rising Today: What's Going On?](internal: news_items, Finnhub company-news, 2026-08-26)
- Internal reports: scalp/intraday/swing (crypto), stocks intraday — `data/reports/**` 2026-08-27
- Internal: `data/catalysts/2026-08-27/catalyst_events.jsonl`, `narrative_baskets.jsonl`
- External web research unavailable this run (not exercised — internal records sufficed for every candidate reviewed).

## 14. Fix Requests / TODO

### TODO-catalyst-mapping-weak
- **issue:** Catalyst→symbol mapping is 79.2% unmapped this cycle (312/1500 mapped), continuing a pattern already documented in project history (17% match rate observed previously).
- **evidence:** `data/catalysts/2026-08-27/catalyst_events.jsonl` — direct count via read query: 312 mapped, 1188 unmapped of 1500 rows.
- **suggested manual fix:** Revisit the symbol resolver in the catalyst layer (macro/central-bank headlines like BOJ/BOK commentary dominate the unmapped tail and may be acceptably unmapped by design — worth confirming whether the 50% threshold should exclude a macro/no-symbol-expected category before treating this as a true regression).
- **priority:** low (known, persistent, not new)
- **first observed (this thread):** 2026-08-27 11:39 EEST — consistent with prior reviews.

### TODO-stale-open-signals-not-expiring
- **issue:** A large number of `proposed_signals` rows remain in `triggered`/`tp1_hit`/`tp2_hit` status with `expires_at` timestamps weeks in the past (e.g. stocks signals from 2026-08-08, 2026-08-04 still show as "triggered" rather than being resolved to a closed/expired state). This inflates the "active" signal count and may reflect a gap in the resolution/expiry pipeline for partially-booked positions.
- **evidence:** `active-signals --asset-class stocks` output — e.g. `sig_57bd3d1e35d6952f` (BX, triggered, expires_at 2026-08-08T15:41:58) and `sig_838e06bbde9dc1c2` (COP, triggered, expires_at 2026-08-08T15:41:58) still appear as open/active as of 2026-08-27. DB query: stocks `proposed_signals` shows 209 total rows in {triggered, tp1_hit, tp2_hit} status, many with old `expires_at`.
- **suggested manual fix:** A human-driven session should check whether the paper-execution / outcome resolver is correctly closing out signals whose entry triggered but never reached a final TP/SL/expiry resolution, and whether `expires_at` should force a resolution pass for partially-booked (tp1_hit/tp2_hit) signals that have gone stale.
- **priority:** medium
- **first observed (this thread):** 2026-08-27 11:39 EEST.
