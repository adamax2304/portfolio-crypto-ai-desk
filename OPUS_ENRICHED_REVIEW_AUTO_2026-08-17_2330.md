# Opus Enriched Review — post-close final daily review — Auto Cycle 23:30 EEST

## 1. Executive Summary

**Post-close final daily review, 23:30 EEST (20:30 UTC / ~16:30 ET) — US cash session just closed. Advisory only — no auto-trade.** Crypto stays in the same **bullish-trend / risk-on** short-term regime flagged at 21:40 (BTC transition_up, ETH uptrend, altcoin breadth 65.85% above EMA20/50), but an external cross-check (Yahoo Finance, 09:17 ET) frames the bigger picture more cautiously: BTC ~$63,413 / ETH ~$1,895, both down on the week, BTC still **down ~46.5% YoY** with analysts undecided on whether the multi-month bear market has bottomed — treat the desk's "bullish trend" label as a short-term structure read, not a green light to size up. No A-tier crypto setup exists tonight; the only fresh B-tier crypto ideas (HEMI, GPS — both from the 22:24 EEST intraday scan) are explicitly flagged low-confidence ("no catalyst" cohort, 14d WR 23%/PF 0.70/−3R). **Stocks closed with only one fresh actionable idea all day: UBER short (B-tier, still `waiting_for_entry` 75.04–75.39, not yet triggered) — not enterable until the next RTH open.** The entire A-tier stocks-long cohort (COP, AMGN, ETN, XOM, LRCX, CRCL, PYPL, MU, MRVL, ASML, INTC, SMH, TSM, GE — 14 names, unchanged in substance since 21:40) remains gated to C by the rolling drawdown guard, which is evidence-based: today's stocks all-tier signal-stats are net negative (PF 0.19, totalR −10.5 on the week; today alone A/B sample=20, wins=7/losses=0 but avgR=0.0 — mostly still-open touches, not closed R). **REGN keeps an active legal/headline risk flag (class_action) for a second consecutive cycle** — treat as avoid/manual-review regardless of its 88.5 score. SMCI's indictment flag from 21:40 did **not reproduce** in tonight's fresh scan (it fell to `no_trade: no_directional_setup`, score 51) — noted as not-reproduced, not resolved. **Catalyst-scan cadence resumed this cycle** (new cycle at 22:30 EEST, 500 fresh events) after appearing stalled at 21:40 — TODO-3 from the last review is resolved. **The 6-symbol crypto OHLCV freeze (HOLO, AVNT, PROM, LUNA, MMT, BABY) is now confirmed for a 6th consecutive cycle, ~50h stale** — escalating, unresolved (TODO-1). Best long-watch overnight: **GPS/USDT** (existing triggered crypto swing position, holding). Best short-watch: **UBER** (stocks, clean B-tier setup, but only actionable at tomorrow's RTH open — market is closed now). No clean catalyst-backed actionable exists; GE remains catalyst-watch pending its market-context-conflict gate clearing. Avoid: **REGN** (active legal flag) and chasing any of the 14 gate-demoted stocks A-tier longs off their stale earlier-cycle signal rows.

## 2. Data Used

- Scheduler: `data/scheduled_runs/2026-08-17_default_schedule/scheduler.log` (mtime 23:22 EEST — current, fresh). Latest `cycle_01_16-18_summary.md` (mtime 18:54 EEST, ~4h36m old) — joint check clears the 3h defer threshold on the scheduler.log freshness alone.
- Reports: scalp `2026-08-17_18-39` (UTC filename = 21:39 EEST, ~1h51m old — fresh, no A/B setups found this cycle, clean no-trade), intraday `2026-08-17_19-24` (UTC = 22:24 EEST, ~1h06m old — fresh, first genuinely new crypto-intraday scan since 21:40), swing `2026-08-17_15-43` (UTC = 18:43 EEST, ~4h47m old — **carry-forward**, same report used at the 21:40 review, now its 3rd consecutive cycle in use; GPS/USDT's entry zone is unchanged from that report), stocks intraday `2026-08-17_19-56` (UTC = 22:56 EEST, ~34min old — **very fresh, the last scan before/at the close**), stocks swing/invest `2026-07-02` (6+ weeks stale, expected — these playbooks are deprecated/removed per known project state, not a live gap).
- Catalysts: `data/catalysts/2026-08-17/catalyst_events.jsonl` (2,172 events today, mtime 22:30 EEST — **fresh, new cycle landed**, resolving the cadence-stall flagged at 21:40), `narrative_baskets.jsonl` (2 baskets, same mtime — `ai_narrative` and `binance_ecosystem_teaser`, both new since 21:40), `catalyst_cycle_19-30.md` (latest cycle summary, 500 events this cycle).
- LLM packets: `llm_analysis_packet.md` (generated 2026-08-17T19:24:24 UTC = 22:24 EEST — fresh, matches the intraday report), `llm_stocks_packet.md` (generated 19:56 UTC = 22:56 EEST — fresh, matches the stocks intraday report).
- `reports/PAPER_MONITOR_STATUS_LATEST.md` (mtime 18:50 EEST, ~4h40m old — **stale this cycle**, used only as background context, not as the authoritative lifecycle source; `active-signals` CLI output used instead as the closer-to-current lifecycle read).
- CLI: `active-signals --asset-class crypto` (n=50, no A-tier), `active-signals --asset-class stocks` (n=50, A-tier present but from earlier-cycle rows), `signal-stats --asset-class crypto --period week` (A/B headline sample=79, PF 2.61, totalR +24.1) and `--period today` (sample=19, wins=0 losses=2, PF 0.25, totalR −1.5), `signal-stats --asset-class stocks --period week` (A/B headline sample=28, PF 0.0, totalR −1.0; all-tier PF 0.19, totalR −10.5) and `--period today` (sample=20, wins=7 losses=0, avgR 0.0 — mostly open/unresolved touches), `detect_untracked_legacy_alerts --since 2026-08-17` → **clean, no untracked alerts**.
- Direct file check: `data/raw/ohlcv/binance/15m/{HOLO,AVNT,PROM,LUNA,MMT,BABY,WLFI,CHIP,ETH}_USDT.csv` last-row timestamps — reconfirms the same 6-symbol freeze at `2026-08-15 22:30:00+00:00` (control symbols WLFI/CHIP/ETH all fresh, last rows today).
- Direct catalyst-file parse: `catalyst_events.jsonl` — 2,172 total / 720 mapped (33.1%) / 1,452 unmapped (66.9%).
- Prior review for comparison: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-17_2140.md` (late-session risk review, 21:40 EEST).
- **External web research**: 1 WebSearch ("Bitcoin BTC price news August 17 2026") + 1 WebFetch verifying the top Yahoo Finance result opens — used to sanity-check the crypto macro backdrop against the desk's short-term regime label; no candidate's verdict critically depended on it, but it materially nuances the mood read (see §1, §6). Ingested into `news_items` via `scripts.ingest_enriched_review_sources` (`data/raw/enriched_review_sources/2026-08-17T20-29-30Z.json`, 1/1 rows written, asset_class=crypto).

## 3. Scheduler / Data Freshness

- Scheduler fresh (current-minute mtime). Both crypto-intraday and stocks-intraday reports refreshed since the 21:40 review; crypto-swing did not (3rd consecutive cycle on the same 18:43 EEST report).
- **Data-integrity carry-forward, confirmed for the 6th consecutive cycle today (04:40 → 11:40 → 15:59 → 18:45 → 21:40 → now 23:30):** the same 6 crypto symbols (HOLO, AVNT, PROM, LUNA, MMT, BABY) remain frozen on 15m OHLCV at `2026-08-15 22:30:00 UTC` (~50h stale). Control symbols WLFI, CHIP, ETH are all fresh (last rows today). See TODO-1 (escalated).
- `detect_untracked_legacy_alerts --since 2026-08-17`: **clean** — every legacy crypto alert has a backing proposed_signal.
- **Resolved this cycle:** catalyst-scan cadence, flagged stalled at 21:40 (TODO-3, unchanged mtime since 17:11 EEST), has resumed — a new cycle landed at 22:30 EEST with 500 fresh events and 2 fresh narrative baskets. TODO-3 closed as resolved.
- Signal-duplication anomaly, still present this cycle (carried from TODO-2): the stocks active-signals pull shows BX with 3 distinct `signal_id` rows for an identical setup (66.4 short, same entry/invalidation, differing only by `expires_at`), INTC with 3 rows (2 identical `triggered`, 1 `waiting_for_entry`), GE with 3 identical `tp1_hit` rows, and AMZN with 3 identical `tp1_hit` rows. Same underlying pattern as 21:40, not yet fixed.
- **Stale-vs-fresh classification gap continues (TODO-4, carried forward):** `active-signals --asset-class stocks` still lists INTC, BAC, and GE as `triggered`/`waiting_for_entry`/`tp1_hit` from earlier-cycle signal rows, even though tonight's fresh 22:56 EEST rescan explicitly demotes all three (and 11 other former A-tier names) to C-tier/`stocks_intraday_long_guard`. An operator reading only the CLI table could mistake these for still-actionable.
- `PAPER_MONITOR_STATUS_LATEST.md` is stale this cycle (18:50 EEST, ~4h40m old) — not used as the authoritative lifecycle source; flagged here rather than silently substituted.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "post_close",
  "as_of": "2026-08-17 23:30 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["stocks swing/invest 6wk+ stale (expected/deprecated)", "crypto swing report unchanged for 3rd consecutive cycle", "PAPER_MONITOR_STATUS_LATEST.md stale (~4h40m)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["6 crypto symbols frozen at 2026-08-15 22:30 UTC (~50h stale), confirmed 6th consecutive cycle", "catalyst cadence resumed this cycle after appearing stalled at 21:40 (TODO-3 resolved)", "crypto-intraday and stocks-intraday both refreshed since 21:40; crypto-swing did not"] },
    { "agent": "market_regime", "verdict": "mixed", "confidence": 0.65,
      "reason_codes": ["risk_on", "longs_preferred", "shorts_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC transition_up, ETH uptrend, altcoin breadth 65.85% above EMA20/50, desk regime label bullish trend/risk-on, unchanged from 21:40", "external cross-check (Yahoo Finance, WebSearch): BTC ~$63,413/ETH ~$1,895, both down on the week, BTC -46.5% YoY, analysts split on bear-market bottom timing — desk's short-term label does not imply a resolved macro trend", "stocks: VIX 15.28, breadth 100% above EMA20/50, 4/4 indices uptrend, regime label bullish — but stocks_intraday_long_guard blocks nearly the entire A-tier long cohort on the week's own negative signal-stats (PF 0.19, totalR -10.5)"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported", "no_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["2,172 catalyst events today, 66.9% unmapped (720/2172 mapped) — still weak mapping, use as context not final decision", "2 fresh narrative baskets this cycle: ai_narrative (NEAR/RENDER/TAO/FET, related WLD/ASTER) and binance_ecosystem_teaser (BNB, related ASTER) — both single_source, <6h fresh, context-only, no B-tier idea currently maps to either", "GE's catalyst (industrial-AI capex tailwind, GE Aerospace/Kratos contract) is real but still gated by market_context_conflict in tonight's fresh rescan", "HEMI/GPS B-tier crypto ideas explicitly flagged no-catalyst, low-confidence cohort"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.4,
      "reason_codes": ["data_unavailable", "oi_supports", "squeeze_risk"],
      "data_missing": ["OI 24h% n/a for HEMI/GPS (bybit/mexc fallback symbols)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ETH/USDT: price up + OI up, fresh positioning confirms trend", "HEMI/USDT: fallback_via_bybit, funding neutral, crowding normal", "GPS/USDT: fallback_via_bybit, funding slightly negative, crowding low"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chase_risk", "entry_fresh", "clean_retest", "stale_before_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["GPS/USDT swing entry zone (0.0149-0.0155) unchanged from the 21:40 review's stale-vs-fresh caveat — same idea, 3rd consecutive cycle, current price ~0.0158 still at/past the top of the zone", "UBER short: not yet triggered (waiting_for_entry 75.04-75.39), technical_setup subscore 23.10 (highest component of its score breakdown), RR to TP1 1.50 — clean, not chasing, but market is closed so entry cannot happen until next RTH open", "HEMI intraday B-tier: preferred pullback 0.0071-0.0072, no market buy if extended — fresh idea but explicitly low-confidence per playbook"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.65,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow", "needs_review"],
      "data_missing": ["PAPER_MONITOR_STATUS_LATEST.md stale (~4h40m), lifecycle counts from that file not used as authoritative this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["active-signals crypto: 0 A-tier, all B-tier, mix of triggered/waiting_for_entry/tp1_hit/tp2_hit spanning back to mid-July (old tp1_hit/tp2_hit rows are closed-partial, not open-actionable)", "active-signals stocks: UBER short waiting_for_entry (2 duplicate rows), duplicate signal_id pattern continues on BX/INTC/GE/AMZN", "6 of the crypto book's open positions run on the frozen OHLCV feed — needs_review"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["legal_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["REGN: active legal/headline risk flag (class_action) for a 2nd consecutive cycle, C-tier, do not treat as clean even at score 88.5", "SMCI: 21:40's indictment flag did not reproduce this cycle (now no_trade/no_directional_setup, score 51) — not-reproduced, not confirmed resolved", "HD earnings next session (2026-08-18, days_ahead=1) and WMT in 3 trading days — explicit do-not-chase warning carries into tomorrow", "BTC exploit_hack risk warnings (Coldcard, SafePal-style breach headlines) continue layering onto an already-elevated macro backdrop"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto A/B week: sample=79, PF 2.61, totalR +24.1, edge concentrated in swing (PF 5.28); intraday (PF 0.86) and scalp (PF 0.50) both net-negative on the week", "crypto A/B today: sample=19 (weak), wins=0 losses=2, PF 0.25, totalR -1.5 — a losing day so far on realized closes, small/mostly-unresolved sample", "stocks A/B week: PF 0.0, totalR -1.0; all-tier week PF 0.19, totalR -10.5 (winrate 8.8%) — the drawdown guard blocking A-tier longs is evidence-based, not overcautious", "stocks A/B today: sample=20, wins=7 losses=0, avgR 0.0 — wins recorded but R not yet finalized (open/touched positions, not closed)"] },
    { "agent": "head_trader", "verdict": "advisory_synthesis_only", "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["see section 8 below"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "GPS/USDT", "trigger": "existing triggered crypto swing position, holding overnight; a fresh add only on a genuine pullback into 0.0149-0.0155, not at current price ~0.0158" },
    "best_short_candidate":    { "symbol": "UBER", "trigger": "waiting_for_entry 75.04-75.39, B-tier stocks intraday, invalidation 75.74 — not actionable until the next RTH open, market is closed now" },
    "best_catalyst_candidate": { "symbol": "GE", "trigger": "no clean catalyst-backed actionable exists this window — GE's capex-tailwind catalyst is real but still gated by market_context_conflict; re-open only if a future rescan clears the gate" },
    "avoid_candidate":         { "symbol": "REGN", "reason": "active legal/headline risk flag (class_action) for a 2nd consecutive cycle; C-tier, do not treat as clean even at a high score" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.70 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | mixed | 0.65 | risk_on, longs_preferred, shorts_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, fresh_catalyst, narrative_supported, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.40 | data_unavailable, oi_supports, squeeze_risk | advisory_only |
| technical_entry | caution | 0.55 | chase_risk, entry_fresh, clean_retest, stale_before_entry | advisory_only |
| execution_lifecycle | needs_review | 0.65 | open_actionable, waiting_for_entry, review_shadow, needs_review | advisory_only |
| risk_manager | caution | 0.65 | legal_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.60 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | advisory_synthesis_only | 0.60 | — | advisory_only |

## 4. What Changed vs Previous Review (vs 21:40 EEST late-session risk review)

- **Resolved:** catalyst-scan cadence, flagged stalled at 21:40 (TODO-3), resumed this cycle with a fresh 22:30 EEST cycle (500 events, 2 new narrative baskets replacing the previous 3). TODO-3 closed.
- **Not reproduced (not confirmed resolved):** SMCI's indictment legal flag from 21:40 does not appear in tonight's fresh stocks rescan — SMCI is now plain `no_trade: no_directional_setup` (score 51, well below its earlier A-tier score). Could mean the flag cleared or the name simply fell out of scoring contention; not enough evidence to call it resolved.
- **Unchanged/confirmed:** REGN's legal/headline flag (class_action) persists for a 2nd consecutive cycle — same treatment, still C-tier/avoid.
- **Unchanged:** the 14-name stocks A-tier long cohort (GE, INTC, BAC, MU, MRVL, LMT, SMCI-was, UBER-was-long, AMGN, REGN, ASML, PYPL, TSM, NVDA, SMH — substantively the same set as 21:40) remains gated by `stocks_intraday_long_guard`; no gate has cleared.
- **Unchanged:** BX short from 21:40 no longer appears as the top stocks idea in tonight's freshest scan — UBER short is now the desk's sole fresh A/B stocks idea (BX may have expired out of the current top-candidates list; not separately re-verified this cycle, treat BX's earlier thesis as stale/expired, not invalidated).
- **Unchanged/escalating:** OHLCV freeze on the same 6 crypto symbols, now confirmed a 6th consecutive cycle (~50h stale), still no remediation (TODO-1).
- **Unchanged:** duplicate signal_id emission continues (TODO-2) — same pattern, different symbols each cycle (BX/INTC/GE/AMZN tonight).
- **New:** two fresh crypto B-tier ideas this cycle from the refreshed intraday scan — HEMI/USDT and GPS/USDT (intraday variant, distinct entry zone from the swing position) — both explicitly flagged low-confidence, no-catalyst.
- **New:** two fresh narrative baskets — `ai_narrative` (NEAR/RENDER/TAO/FET) and `binance_ecosystem_teaser` (BNB) — context-only, no B-tier idea currently maps to either.

## 5. Catalyst Coverage

- Total catalyst_events today: **2,172**. Mapped (non-null symbol): **720** (33.1%). Unmapped: **1,452** (66.9%).
- Narrative baskets: **2** — `ai_narrative` (NEAR/RENDER/TAO/FET, related WLD/ASTER, playbook `related_beta_rotation`) and `binance_ecosystem_teaser` (BNB, related ASTER, playbook `related_beta_rotation`) — both fresh (<6h), single_source.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped/low-signal headline types this cycle (from `catalyst_cycle_19-30.md`, 500 events): a wave of small-cap securities-fraud class-action PR-mill items (AARD, PROCEPT/PRCT, Wix/WIX, Microvast/MVST, Futu/FUTU, EMBC, First Solar/FSLR, Rackspace/RXT, Cogent) — mostly boilerplate law-firm solicitations, not fresh material news; NVDA/regulatory (SEC guidance on data-center financing sponsors); HD/WMT earnings-week items.

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **risk-on / bullish trend (short-term structure)**, unchanged from 21:40 — BTC transition_up, ETH uptrend, altcoin breadth 65.85% above EMA20/50. External cross-check nuances this: BTC ~$63,413 / ETH ~$1,895 (Yahoo Finance, 09:17 ET), both down on the week, BTC −46.5% YoY, "controlled relief bounce near support" rather than a high-conviction rally, analysts split on bear-market bottom timing. Macro/geopolitics risk score stays elevated (91.2/100) on the Coldcard exploit stack and Iran/Strait-of-Hormuz theme.
- Stocks mood: **risk-on tape (VIX 15.28, breadth 100%, 4/4 indices uptrend) that remains decoupled from actionable longs** — the rolling drawdown guard is blocking the entire A-tier long cohort for the 3rd consecutive cycle, and today's/this-week's stocks signal-stats justify the caution (week all-tier PF 0.19, totalR −10.5).
- Dominant narrative: crypto — AI-sector rotation (NEAR/RENDER/TAO/FET) and a Binance-ecosystem teaser (BNB), both fresh but context-only; stocks — AI capex tailwind (GE) real but gated, shorts (UBER) the only clean stocks playbook currently working.
- Preferred side now: **mixed — crypto hold existing longs, no fresh crypto short idea (crypto-short bucket remains a losing playbook, n=8 PF 0.0 on the week); stocks shorts-only (UBER) at tomorrow's open, avoid stocks longs broadly until the drawdown guard eases.**
- Best long candidate: **GPS/USDT** (crypto, existing triggered swing position; fresh adds only on a genuine pullback into 0.0149-0.0155)
- Best short candidate: **UBER** (stocks, B-tier intraday, waiting_for_entry 75.04-75.39; not actionable until the market reopens)
- Best catalyst-backed candidate: **none clean this window** — GE's catalyst is real but gated; the two fresh narrative baskets (AI rotation, Binance ecosystem) are context, not yet actionable ideas.
- What to avoid: **REGN** (active legal flag), chasing any of the 14 gate-demoted stocks A-tier longs off stale earlier-cycle signal rows, adding to **GPS/USDT** at current extension, and managing **HOLO/AVNT/PROM/LUNA/MMT/BABY** off the displayed price/TP/SL (frozen feed, unverified, 6th cycle).
- What would change the view: OHLCV feed remediation for the 6 frozen crypto symbols; the stocks long-guard easing on a positive paper-R stretch; GPS pulling back into its tagged entry zone; UBER printing into its entry zone at tomorrow's open; REGN's legal story resolving or firming up with a second source.

## 7. Candidate Deep Dives

**TradingView / manual chart check unavailable this cycle — all technical reads below use only local OHLCV / ATR / EMA / RS fields from the reports and CLI, no chart-visual claims made.**

**1. UBER — stocks, B-tier, short, intraday, waiting_for_entry (75.04-75.39, invalidation 75.74)**
- Catalyst: 8 internal news catalysts in the lookback window (not independently re-verified externally this cycle — internal data fresh and sufficient).
- Price reaction: not yet triggered — chase risk is low; RR to TP1 is 1.50.
- Legal/headline risk: none found for UBER.
- Aligned with market mood: yes for the *playbook* (stocks-intraday shorts subset, 14d WR 55%/PF 2.03, shorts PF 9.00), even though the broader tape is risk-on — this is a stock-specific relative-weakness setup (below prev-day low, RS vs sector +2.29% but downtrend structure), not a tape-level bet.
- Actionable now: **no — US cash market is closed.** Only actionable once price prints into 75.04-75.39 after tomorrow's RTH open; do not chase below the zone.
- Would invalidate: close beyond 75.74.
- Note: 2 duplicate `signal_id` rows for this setup in active-signals — treat as one setup (TODO-2).

**2. REGN — stocks, C-tier, active legal/headline risk (class_action), 2nd consecutive cycle**
- `legal_headline_risk: class_action` — demoted A→C specifically for this reason (score would otherwise be 88.5, well into A-tier territory).
- Actionable now: no — C-tier/watchlist only, and per source-discipline protocol, must be downgraded to MANUAL REVIEW REQUIRED (not treated as clean) if it ever re-promotes to A/B without the flag clearing.
- What would change the view: the underlying legal story resolving/being dismissed, or a corroborating second source firming up the risk.

**3. GE — stocks, previously A-tier, long, intraday — demoted to C ("watchlist / not actionable") for a 3rd consecutive cycle**
- Same gate as 21:40: `stocks_intraday_long_guard` (rolling paper-R drawdown guard). The Kratos/GE-Aerospace capex-tailwind catalyst is still real and cited, but the guard, not a catalyst contradiction, is now the primary gate reason in tonight's report.
- Legal/headline risk: none found.
- Actionable now: **no** — catalyst-watch only. The earlier-cycle GE signal rows (tp1_hit ×2, triggered) remain visible in the raw active-signals table — same stale-vs-fresh classification gap as 21:40 (TODO-4).

**4. GPS/USDT — crypto, B-tier, swing, long, existing triggered position (entry 0.014880-0.015538, invalidation 0.014075)**
- Has price already reacted? No fresh verified catalyst attached — pure momentum/RS setup (24h +49.3% at last swing-report read, RS vs BTC +48.2%).
- Is the setup chasing? Yes for a fresh add — the preferred pullback zone is 0.0149-0.0155; current price ~0.0158 sits at/past the top of that zone, and this entry-zone data itself is now 3 cycles old (no fresher crypto-swing scan since 18:43 EEST).
- Retest/pullback structure: yes, explicitly defined by the desk.
- Aligned with market mood: yes (bullish-trend, selective-longs style favors RS leaders on pullback).
- Actionable now: as an **existing position**, yes (already triggered, running overnight); as a **fresh add**, only on confirmed pullback acceptance into the zone.
- Would invalidate: 1h close beyond 0.0141.

**5. Frozen-feed crypto swing book — HOLO, AVNT, PROM, LUNA, MMT, BABY**
- Not a new candidate — an existing-book data-integrity risk, included because it materially affects "what's safe to trust" overnight.
- All 6 confirmed frozen on 15m OHLCV at `2026-08-15 22:30:00 UTC` (~50h stale), 6th consecutive cycle, control symbols (WLFI/CHIP/ETH) fresh by contrast.
- Would invalidate/resolve: OHLCV ingest remediation for this specific symbol set (TODO-1); until then, no confidence in displayed price/TP/SL state for these 6 overnight.

## 8. Best Candidates Ranked

1. **GPS/USDT (long, existing position)** — best crypto overnight hold; a fresh add only on a genuine pullback into 0.0149-0.0155, current price above the zone.
2. **UBER (short-watch)** — cleanest stocks setup on the desk today, but next-session-only; watch for entry into 75.04-75.39 after tomorrow's RTH open.
3. **GE (catalyst-watch only)** — real catalyst, gated by the drawdown guard for a 3rd cycle; re-open only on a future rescan clearing the gate.
4. **REGN (avoid / legal-risk watch)** — C-tier, active legal flag for a 2nd cycle; watch for the legal story resolving before treating as clean even at a high score.
5. **Frozen-feed swing book (needs-review, not a fresh add)** — HOLO/AVNT/PROM/LUNA/MMT/BABY, existing positions only, data-integrity caveat on all displayed levels overnight.

**Excess candidates not deep-dived (slot cap):** INTC, BAC, MU, MRVL, ASML, TSM, SMH, COP, AMGN, ETN, XOM, LRCX, CRCL, PYPL — same `stocks_intraday_long_guard` demotion logic as GE, not separately dived to avoid repeating the analysis. HEMI/USDT (fresh crypto intraday B-tier) — held out for brevity, same low-confidence no-catalyst treatment as GPS's intraday variant.

## 9. Avoid / No Trade (this decision window only)

- **REGN** as any kind of long — active legal flag, C-tier, do not treat as clean even at a high score.
- **GE, INTC, BAC** and the other 11 gate-demoted stocks A-tier longs — real scores, but explicitly not actionable this cycle per the fresh rescan; do not act on their stale earlier-cycle "triggered"/"tp1_hit" rows.
- **GPS/USDT** as a fresh crypto add at current extension — wait for the tagged pullback zone.
- **HOLO, AVNT, PROM, LUNA, MMT, BABY** — do not manage these open crypto swing positions off the displayed price/TP/SL; feed frozen ~50h, unverified. Existing positions continue running per system logic; this is a data-quality caution, not a stop-the-system instruction.
- This is a decision-window-only read — scanning, candidate generation, and tracking continue uninterrupted regardless of this section, including overnight and into tomorrow's Asia/EU/US sessions.

## 10. Main Risks

- **Frozen OHLCV on 6 open crypto swing positions**, 6th consecutive cycle unresolved (~50h stale) — displayed price/TP/SL cannot be trusted overnight until the feed is fixed.
- **Stocks long-guard is blocking almost the entire A-tier long cohort** for a 3rd consecutive cycle — appropriate given the week's own signal-stats (all-tier PF 0.19, totalR −10.5), but "risk-on tape" and "actionable longs" remain decoupled; carries into tomorrow.
- **Duplicate signal emission continues** (BX/INTC/GE/AMZN this cycle) — inflates apparent setup counts; read active-signal counts with that in mind.
- **Crypto short bucket remains a losing playbook** (n=8, PF 0.0, totalR −3.0 on the week) — no fresh crypto short idea exists this cycle regardless.
- **Crypto today (realized closes) is net negative**: A/B sample=19 (weak), wins=0/losses=2, PF 0.25, totalR −1.5 — small, mostly-unresolved sample, but worth tracking into tomorrow.
- **Macro/geopolitics risk still elevated** (91.2/100) — Coldcard exploit stack, SafePal-style breach headline, Iran/Strait-of-Hormuz theme layering onto a crypto tape that external sources still frame as an unresolved bear market (BTC −46.5% YoY).
- **HD and PANW have earnings tomorrow (2026-08-18)** — explicit do-not-chase warning carries overnight into the next session.
- **Stale-vs-fresh classification gap** — active-signals CLI still lists gate-demoted names (GE/INTC/BAC) as triggered/tp1_hit from earlier cycles; an operator reading only the CLI output (not the freshest report) could mistake them for still-actionable (TODO-4).

## 11. Action Plan — next session / overnight-into-Asia

- Hold GPS/USDT as an existing crypto swing position; do not add at current price, only on a genuine pullback into 0.0149-0.0155.
- Watch UBER for entry into 75.04-75.39 at tomorrow's RTH open; do not chase if it gaps through the zone.
- Do not add to GE/INTC/BAC/any of the 14 gate-demoted stocks longs unless a future rescan clears their specific demotion reasons.
- Re-check OHLCV feed remediation for the 6 frozen crypto symbols at the next cycle (7th consecutive check).
- Do not chase HD or PANW into tomorrow's earnings prints.
- Watch for a fresh crypto-swing rescan to replace the now-3-cycles-old 18:43 EEST swing report.
- Track REGN's legal story and SMCI's flag status (not reproduced tonight) at the next cycle.
- No new crypto swing adds recommended given the frozen-feed exposure already on the book.

## 12. Final Verdict per Mode

- **Crypto scalp:** no A/B setups found tonight (clean no-trade per the desk's own scalp report); today's realized closes are negative — continue data collection only.
- **Crypto intraday:** two fresh B-tier ideas (HEMI, GPS-intraday-variant), both explicitly low-confidence/no-catalyst; intraday-mode PF is negative on the week (0.86).
- **Crypto swing:** bullish-trend backdrop persists; GPS/USDT is the best long-watch (pullback-only for fresh adds, existing position holding overnight); swing report itself is now 3 cycles stale; 6-symbol frozen-feed book needs review; no new adds recommended.
- **Stocks intraday:** market closed; UBER short is the only clean actionable, next-session-only; the entire A-tier long cohort remains guard-demoted to C; HD/PANW earnings tomorrow, do not chase either into the print.
- **Stocks swing/invest:** deprecated framework, no signal (per known project state).

## 13. Sources

- Internal: `data/reports/stocks/intraday/2026-08-17_19-56_stocks_intraday_report.md` — fresh pre-close scan, source for the GE/INTC/BAC/etc. demotion, REGN legal flag, SMCI not-reproduced finding, and the UBER idea card.
- Internal: `data/reports/intraday/2026-08-17_19-24_intraday_report.md` and `data/processed/llm_analysis_packet.md` — source for the crypto macro/geopolitics risk score, HEMI/GPS-intraday B-tier ideas, and headline list (Coldcard exploit).
- Internal: `data/reports/swing/2026-08-17_15-43_swing_report.md` — carried-forward swing scan, source for the GPS/USDT swing entry zone.
- Internal: `data/catalysts/2026-08-17/catalyst_cycle_19-30.md` and direct parse of `catalyst_events.jsonl` / `narrative_baskets.jsonl` — source for the catalyst mapping ratio and the two fresh narrative baskets.
- Internal: direct OHLCV CSV timestamps, `data/raw/ohlcv/binance/15m/{HOLO,AVNT,PROM,LUNA,MMT,BABY,WLFI,CHIP,ETH}_USDT.csv`, read 2026-08-17 ~23:30 EEST, used for the frozen-feed finding.
- External: [Bitcoin and ethereum prices today, Monday, August 17, 2026: Crypto prices down slightly as analysts question timing of bear market bottom](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-monday-august-17-2026-crypto-prices-down-slightly-as-analysts-question-timing-of-bear-market-bottom-135747407.html) (Yahoo Finance, published ~2026-08-17 13:17 UTC, verification_status single_source) — used for the BTC/ETH price and macro-mood cross-check in §1/§6. Fetched and verified via WebFetch. Ingested into `news_items` (`data/raw/enriched_review_sources/2026-08-17T20-29-30Z.json`).

## 14. Fix Requests / TODO

### TODO-1 (carried forward, escalating — 6th consecutive cycle)
- **issue:** 6 crypto swing positions (HOLO, AVNT, PROM, LUNA, MMT, BABY) remain open and are being monitored for TP/SL off 15m OHLCV frozen at `2026-08-15 22:30:00 UTC`.
- **evidence:** `data/raw/ohlcv/binance/15m/{HOLO,AVNT,PROM,LUNA,MMT,BABY}_USDT.csv` all last-row `2026-08-15 22:30:00+00:00`, checked 2026-08-17 ~23:30 EEST (~50h stale). Control symbols WLFI/CHIP/ETH fresh (last rows today). Also flagged in `_0440.md`, `_1140.md`, `_1559.md`, `_1845.md`, `_2140.md`.
- **suggested manual fix:** investigate the OHLCV ingest/refresh path for this specific symbol set; verify whether the paper-monitor TP/SL logic for these 6 positions is reading this frozen file or a separate live-price source.
- **priority:** high
- **first observed:** 2026-08-17 02:00 EEST (carried through 04:40, 11:40, 15:59, 18:45, 21:40, now 23:30)

### TODO-2 (carried forward, symbols changed)
- **issue:** Duplicate signal_id emission for the same underlying setup continues — this cycle BX shows 3 distinct rows for one setup, INTC shows 3 rows (2 identical triggered + 1 waiting_for_entry), GE shows 3 identical `tp1_hit` rows, AMZN shows 3 identical `tp1_hit` rows.
- **evidence:** `python -m src.cli active-signals --asset-class stocks` output, 2026-08-17 ~23:30 EEST.
- **suggested manual fix:** same as previously logged — investigate the stocks signal-generation path for a dedup gate on symbol+tier+mode+entry-zone within a short time window.
- **priority:** medium
- **first observed:** 2026-08-17 18:40 EEST (recurring, not yet fixed)

### TODO-4 (carried forward)
- **issue:** Active-signals CLI output does not reflect same-day tier demotions from a fresher rescan — GE, INTC, and BAC still show as `triggered`/`waiting_for_entry`/`tp1_hit` in `active-signals --asset-class stocks` even though the fresh 22:56 EEST rescan demotes all three (and 11 other names) to C-tier/not-actionable (`stocks_intraday_long_guard`, etc.).
- **evidence:** compare `python -m src.cli active-signals --asset-class stocks` (GE/INTC/BAC rows, 2026-08-17 ~23:30 EEST) against `data/reports/stocks/intraday/2026-08-17_19-56_stocks_intraday_report.md` §7 (same symbols listed as "watchlist / not actionable").
- **suggested manual fix:** clarify (or add a display flag for) whether active-signals should surface the most recent tier verdict for a still-open signal_id when a fresher scan has since demoted the underlying setup.
- **priority:** medium
- **first observed:** 2026-08-17 21:40 EEST (recurring, not yet fixed)

_TODO-3 (catalyst-scan cadence stall, first observed 21:40 EEST) is RESOLVED this cycle — a fresh catalyst cycle landed at 22:30 EEST. Not carried forward._
