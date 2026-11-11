# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:39 EEST

## 1. Executive Summary
Slot: **Europe / pre-US context** (11:30 EEST). Advisory only / no auto-trade. BTC is in a downtrend (~$63.8K, externally confirmed) with ETH mixed (transition_up intraday, downtrend swing); macro risk score is elevated (91.8–95.4/100, risk-off) on the Strait of Hormuz standoff — externally confirmed as still unresolved (Iran-Oman talks stalled, Brent ~$87-89, up >40% YTD) — plus soft-CPI-vs-weak-BTC divergence headlines. Zero A/B-tier setups fired in crypto (scalp/intraday/swing) or stocks (market still closed pre-open) this cycle; both desks are in a clean no-new-idea state, not a broken one. Catalyst-symbol mapping is weak this run (21.4% mapped, 78.6% unmapped) — treat the catalyst layer as context only. The most load-bearing finding is a **carried-forward, still-unresolved signal-lifecycle integrity gap**: TUT/USDT's "triggered" position (entered 2026-08-09, invalidation 0.09882) is unchanged since the last review that confirmed a live invalidation breach — this is the 7th consecutive cycle flagging the same row (see §10, §14).

## 2. Data Used
- Reports: scalp (2026-08-13 07:16 EEST, fresh), intraday (07:24, fresh), swing (04:37, ~7h old — **carry-forward**, 4-12h band), stocks intraday (07:51, fresh; market closed — planning only). Stocks swing/invest excluded — deprecated, last dated 2026-07-02 (>6 weeks).
- Catalyst layer: `data/catalysts/2026-08-13/` (latest cycle_07-29.md, catalyst_events.jsonl — 1,500 events today).
- LLM packets: `llm_analysis_packet.md` (10:25), `llm_stocks_packet.md` (10:53).
- Scheduler: `data/scheduled_runs/2026-08-12_default_schedule/scheduler.log` + `cycle_05_10-05_summary.md`, both 11:08 EEST (~31 min old — fresh, well under the 3h defer threshold).
- CLI: `active-signals` ×2 (crypto/stocks), `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-08-13` (clean — 0 untracked alerts).
- Direct read-only SQL against `db/crypto_ai_desk.sqlite`: `proposed_signals` status breakdown (crypto/stocks), TUT/USDT and HEI/USDT row history, oldest-`triggered` audit, `validity_window_hours`/`expires_at` for the two flagged rows.
- External: 2 WebSearch queries (BTC spot price; Strait of Hormuz status) — both corroborate internal data, no contradiction found. No WebFetch needed since search snippets were sufficient and consistent with internal reports.

## 3. Scheduler / Data Freshness
- Scheduler fresh: `scheduler.log` and `cycle_05_10-05_summary.md` both at 11:08 EEST (31 min old). No defer triggered.
- Report freshness: scalp/intraday/stocks-intraday fresh (<3.5h); swing 4-12h band (carry-forward, still usable, flagged).
- Monitor status: `pending_monitor` and `derivatives_monitor` logs both updated within the last cycle (10:12–11:39). No stalled-process signature observed.
- Paper/live: no live execution — system remains paper/read-model only per standing lock.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-08-13 11:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale", "derivatives_sparse", "onchain_config_missing"],
      "data_missing": ["swing report >4h", "on-chain whale flows", "order book depth/CVD"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log 11:08", "swing report 04:37 (~7h)", "blindspots section §9 of scalp/intraday reports"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.8,
      "reason_codes": ["risk_off", "chop", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC downtrend, macro risk 91.8-95.4/100", "altcoin breadth 42.5-45.5% above EMA20", "WebSearch: BTC ~$63.8K, Hormuz still closed"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "no_catalyst", "fresh_catalyst"],
      "data_missing": ["symbol resolver coverage for majority of events"],
      "suggested_effect": "advisory_only",
      "facts_used": ["321/1500 catalyst events mapped (21.4%)", "momentum_breakout basket <1h fresh (KORUB/USDT)"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["oi_supports", "squeeze_risk", "data_unavailable"],
      "data_missing": ["futures data for SPCXB/NBISB/KORUB/SKHYB"],
      "suggested_effect": "advisory_only",
      "facts_used": ["VIRTUAL/USDT price+OI up (fresh positioning)", "MMT/USDT negative funding + OI up (squeeze setup)"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["entry_late", "clean_retest", "stale_before_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["MMT/USDT price 0.1836 vs retest zone 0.1846-0.1869", "BANK/USDT price 0.0387 vs pullback zone 0.0378-0.0384"] },
    { "agent": "execution_lifecycle", "verdict": "manual_review", "confidence": 0.65,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"],
      "data_missing": ["live price re-check for all 45 triggered crypto rows"],
      "suggested_effect": "advisory_only",
      "facts_used": ["45 crypto triggered / 4 waiting_for_entry", "17 stocks triggered (all >72h, market closed)", "TUT/USDT + HEI/USDT unresolved triggered rows, 127-156h old, validity_window_hours=168"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["headline_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["macro risk-off 91.8-95.4/100 (Hormuz + CPI divergence)", "REGN/BLK class-action legal risk (C-tier, contained, not actionable)", "TUT/USDT integrity gap"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto A/B weekly: n=239, WR 17.4%, PF 2.46, +56.9R (touch-based, known to overstate — see memory)", "weekend-mode crypto underperforms: WR 22%, n=110, reliable", "stocks A/B 7d: n=11 weak, WR 0%, PF 0.0, -3.0R", "stocks C-tier watchlist: PF 0.27, WR 2.4%, n=802"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.55,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.55,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "BANK/USDT", "trigger": "1h close holding 0.0378-0.0384 pullback zone with volume ≥0.83x avg; invalidated below 0.0371", "reason": "Best RS leader (+9.9-12.7% 24h) with swing playbook's strongest historical stats (14d WR 72%/PF 5.80), but currently a watch-only C-tier score (63.5) — not yet confirmed" },
    "best_short_candidate":    { "symbol": "MMT/USDT", "trigger": "Rejection candle at 0.1846-0.1869 failed-bounce zone, confirm below on volume; invalidated on 1h close beyond 0.1897", "reason": "Consistent bearish read across scalp/intraday/swing, negative funding + OI building (squeeze-aware), price already inside the retest zone" },
    "best_catalyst_candidate": { "symbol": "KORUB/USDT", "trigger": "Hold above 20.336-20.526 pullback zone with confirming volume + basket still fresh (<6h)", "reason": "Only symbol tied to a <1h-fresh narrative basket (momentum_breakout) with an active swing watchlist entry; derivatives unavailable so confirmation is incomplete" },
    "avoid_candidate":         { "symbol": "TUT/USDT", "reason": "Displayed 'triggered' status is not reliable — unchanged row since 2026-08-09, invalidation breach confirmed by a prior review and never resolved; do not use it to gauge open book risk" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.75 | scheduler_fresh, report_stale, derivatives_sparse, onchain_config_missing | advisory_only |
| market_regime | caution | 0.80 | risk_off, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, no_catalyst, fresh_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.50 | oi_supports, squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | entry_late, clean_retest, stale_before_entry | advisory_only |
| execution_lifecycle | manual_review | 0.65 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.60 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.55 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review
Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-13_0445.md` (crypto overnight / Asia, 04:45 EEST).
- **New:** KORUB/USDT enters the watchlist as a fresh (<1h) momentum_breakout basket primary — wasn't mentioned last cycle.
- **Removed:** BICO/USDT's prior CLOSED WIN (+1.0R) is no longer the headline story; no new resolved positions surfaced this cycle in the reports read.
- **Unchanged / carried:** MMT/USDT short-watch and BANK/USDT long-watch remain the two cleanest crypto watchlist names, same zones, same invalidators — neither has triggered yet across two cycles.
- **Confirmed still-broken:** TUT/USDT's flagged "triggered" row is the *exact same row* (`updated_at` 2026-08-09T17:01:44) as the previous review — zero change in 7h, meaning whatever produced the confirmed invalidation breach last cycle has not been corrected. This is now the 7th consecutive review citing this pattern per memory (`[[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]]` is a related but distinct bug).
- **Stocks:** regime unchanged (bullish/risk-on carried forward, VIX ~14.6-14.7, still pre-open).
- **Catalyst mapping:** 21.4% mapped this run vs the last-reported downward trend (73→76% unmapped in recent reviews); today's 78.6% unmapped continues that trend — worsening, not improving.

## 5. Catalyst Coverage
- Total `catalyst_events` today: **1,500**. Mapped (non-null symbol): **321 (21.4%)**. Unmapped: **1,179 (78.6%)**.
- Narrative baskets: **5** (rwa_narrative, perps_dex_narrative, ai_narrative, binance_ecosystem_teaser, momentum_breakout).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (78.6% > 50% unmapped threshold.)
- Top unmapped-adjacent headlines still worth noting despite no symbol tag: Iran/Hormuz geopolitical stream (multiple sources), CPI/Fed-hold macro narrative, several PR Newswire stock securities-fraud class-action notices (REGN, INTU, PODD, PNR, WSE, GNS, CAPR, BZAI — legal-risk stream is heavy today but mostly unrelated to actionable tickers).

## 6. Market Landscape

BTC is in a confirmed downtrend across scalp/intraday/swing scans; ETH is mixed (transition_up on the freshest intraday read, downtrend on the ~7h-old swing read — treat ETH as genuinely undecided, not a clean signal). Altcoin breadth is 42.5-45.5% above EMA20 — a chop tape, not a directional trend. Macro risk score is 91.8-95.4/100 (risk-off), driven by the Strait of Hormuz standoff remaining unresolved — externally confirmed via WebSearch: Iran-Oman talks stalled, US naval blockade still cited by Iran as the blocker, Brent ~$87-89 (up >40% YTD) — plus a "soft CPI meets weak BTC" divergence headline suggesting crypto isn't getting the same macro-relief bid as risk assets broadly. BTC spot externally confirmed at ~$63,800 (WebSearch), consistent with internal reports' $63.5-64K read.

Stocks: still pre-open (11:39 EEST, cash open is ~16:30 EEST). Regime carried forward from the 07:51 stocks intraday report: **bullish, risk-on**, VIX 14.67 (low), breadth 100% above EMA20/50, all 4 major indices in uptrend (SPY/QQQ/IWM/DIA). Strongest sectors: energy (XLE, RS +5.68%), healthcare (XLV, RS +4.07%). Weakest: utilities, communications, semiconductors. AMAT reports earnings today — avoid chasing into the print. This is planning/watchlist context for the 16:20 pre-open and 18:30 open-reaction slots, not actionable now.

### Market Mood / Risk Routing
- Crypto mood: **risk-off / chop** (BTC downtrend + elevated macro risk, but not a panic — ATR percentile is normal at 26-28%)
- Stocks mood: **pre-market / bullish carried-forward** (cash session closed until ~16:30 EEST)
- Dominant narrative: Strait of Hormuz / oil-driven macro risk-off overhanging a chop crypto tape; AI/RWA/perps-dex narrative baskets active but thin
- Preferred side now: **wait-for-trigger**, with a short-lean bias in crypto given the macro backdrop and a long-lean bias in stocks (bullish regime, but pre-open — no confirmation yet)
- Best long candidate: BANK/USDT (watch — needs 0.0378-0.0384 to hold with volume)
- Best short candidate: MMT/USDT (watch — needs rejection confirmation at 0.1846-0.1869)
- Best catalyst-backed candidate: KORUB/USDT (watch — momentum_breakout basket, <1h fresh, needs volume confirmation)
- What to avoid: chasing any fresh long into the BTC/ETH downtrend without a confirmed pullback hold; treating TUT/USDT's "triggered" status as valid open risk; any stocks entry before RTH confirmation
- What would change the view: BTC reclaiming local resistance and Hormuz de-escalation would flip crypto mood to risk-on; a clean US cash open with breadth confirmation would activate the stocks bullish thesis

## 7. Candidate Deep Dives

### 1. MMT/USDT — short-watch (crypto, C-tier watchlist)
- **Price reaction:** Already inside the failed-bounce/retest zone (current 0.1836-0.1861 vs zone 0.1846-0.1897 depending on report timestamp) — not a fresh breakdown, a retest-in-progress.
- **Chasing?** No — this is the retest itself, not a chase of the initial move.
- **Retest/pullback structure:** Yes, textbook failed-bounce setup per the playbook.
- **Overextended?** No (RR to TP1 ~1.84R, not stretched beyond 2 ATR).
- **Late if entered now?** Borderline — needs confirmation candle, not a market entry.
- **Actionable level:** 1h close below the zone low with volume, OR fade at zone high on rejection.
- **Aligned with mood?** Yes — risk-off/chop favors clean shorts over longs per the routing table.
- **Long/short/wait:** Short, wait-for-trigger.
- **Actionable now or after confirmation?** After confirmation (rejection candle + volume).
- **Invalidates:** 1h close beyond 0.1897 (intraday) / 0.1928 (swing).
- **Chase risk:** Low.
- **Catalyst:** None verified — this is a pure technical/derivatives setup (negative funding, OI building = squeeze-aware).
- **TradingView/manual chart check unavailable** — read is from local OHLCV/ATR/EMA fields only.

### 2. BANK/USDT — long-watch (crypto, C-tier watchlist, swing playbook)
- **Price reaction:** RS leader (+9.9% to +12.7% 24h depending on report); price 0.0387 is just above the 0.0378-0.0384 conditional pullback zone.
- **Chasing?** Mild risk — the move is already up double-digits on 24h; the playbook explicitly warns "chase risk after a vertical 24h move."
- **Retest/pullback structure:** Conditional — needs the pullback zone to actually get tagged and hold.
- **Overextended?** Not yet by the 2-ATR rule, but close given the 24h move.
- **Actionable level:** Pullback into 0.0378-0.0384 holding with volume ≥0.83x avg.
- **Aligned with mood?** Contrarian to the risk-off crypto mood — this is the single best counter-trend RS name, which is exactly why it needs the cleanest confirmation before acting.
- **Long/short/wait:** Long, wait-for-trigger.
- **Invalidates:** 1h close beyond 0.0371, or a fresh BTC downtrend low.
- **Chase risk:** Medium — do not buy the current price, wait for the pullback.
- **Catalyst:** None verified this cycle despite RS leadership — playbook flags catalyst-backed as the "cleanest sub-cohort," and this name doesn't have one yet.
- **Playbook stats:** 14d WR 72% / PF 5.80 / +24R — strongest crypto lane by the numbers, but this is the swing playbook's touch-based R metric (known to overstate realized edge per prior audits — read as directional signal, not literal expectancy).

### 3. VIRTUAL/USDT — long-watch (crypto, appears in all three timeframes)
- **Price reaction:** Uptrend, +9.6-9.7% 24h, derivatives confirm (price up + OI up +27-30%, "fresh positioning confirms trend").
- **Chasing?** Volume is the weak link — 0.1-0.23x of 20-period average across all three reports, well below confirmation threshold.
- **Retest/pullback structure:** Conditional pullback zone 0.5811-0.5897 (swing) / 0.5853-0.5897 (intraday) — current price 0.59-0.5916 is essentially at the zone already.
- **Overextended?** Risk penalty is the largest of the watchlist names (-16.7), specifically for weak volume confirmation.
- **Actionable level:** Needs volume expansion on any pullback hold — the setup quality (69%) is good but confidence stays "low" until volume shows up.
- **Aligned with mood?** No — long in a risk-off crypto tape without volume confirmation is the profile the "no-trade warnings" section explicitly discourages.
- **Long/short/wait:** Long, wait-for-trigger (volume-gated).
- **Invalidates:** 1h close beyond 0.5727 (swing) / 0.5799 (intraday).
- **Catalyst:** None verified.

### 4. KORUB/USDT — catalyst-watch (crypto, fresh basket)
- **Price reaction:** +10.99-11.0% 24h, RS +11.6% vs BTC; primary member of the `momentum_breakout` basket, freshness **<1h** (the freshest basket tag in today's catalyst layer).
- **Chasing?** Some — 7d return is already +22.3%, so this is a continuation, not a fresh base.
- **Retest/pullback structure:** Conditional pullback zone 20.336-20.526 vs current 20.610 — just above the zone.
- **Overextended?** Setup quality 71.9% is solid, but derivatives are unavailable for this symbol (confidence reduced, "no usable derivatives read, so leverage confirmation is missing").
- **Actionable level:** Hold above the pullback zone with volume while the basket stays fresh (<6h window).
- **Aligned with mood?** Catalyst-backed longs are one of the few things the risk routing table green-lights even in a risk-off tape — but only with confirmation.
- **Long/short/wait:** Long, wait-for-trigger.
- **Invalidates:** 1h close beyond 20.103.
- **Catalyst confirmation/contradiction:** Confirms (basket-fresh, no contradicting news found in `catalyst_events.jsonl` for this symbol).

### 5. TUT/USDT — needs review (crypto, NOT a trade candidate)
- **Status:** `triggered`, long, entry 0.14283714, invalidation 0.09882286, `updated_at` = 2026-08-09T17:01:44+00:00 (unchanged since the prior review), `validity_window_hours`=168 (expires 2026-08-16T15:38:12+00:00 — still technically inside its window, so this is not a simple "should have expired" case).
- **Why flagged:** The immediately preceding review (04:45 EEST) confirmed via live price that this position was trading roughly one-third of the way through its own invalidation level while still displaying `triggered`. This review's SQL pull shows the identical row, byte-for-byte unchanged in the 7 hours since — the underlying invalidation-monitoring gap that produced that state has not self-corrected.
- **Broader pattern observed this cycle (lower confidence, not independently price-verified today):** an oldest-`triggered`-first audit of all 45 currently-`triggered` crypto rows shows several others (HEI/USDT 131h old, CTSI/USDT 149-156h, ZBT/USDT 149-156h, ACE/USDT 149-154h, ADA/USDT 148-154h, ZEC/USDT 136h, STG/USDT 134h, BICO/USDT 131h, NIL/USDT 124h) sitting `triggered` for 120-156h. Swing signals have a 168h validity window by design, so age alone is **not** proof of a bug — but it means the book cannot currently distinguish "legitimately still open, price never reached invalidation" from "functionally dead like TUT/USDT, monitor just hasn't closed it." That distinction matters for anyone reading "45 open crypto positions" as current risk exposure.
- **Do not use this position (or the raw `triggered` count) to gauge current book risk** until the underlying gap is investigated.

## 8. Best Candidates Ranked
1. **BANK/USDT long-watch** — best RS + best historical playbook stats, but not yet confirmed; wait for 0.0378-0.0384 to hold with volume.
2. **MMT/USDT short-watch** — cleanest mood-aligned setup (risk-off tape favors shorts); wait for rejection at the retest zone.
3. **KORUB/USDT catalyst-watch** — only fresh (<1h) basket-backed name on the board; wait for pullback hold + volume, derivatives unconfirmed.
4. **VIRTUAL/USDT long-watch** — good trend/derivatives read but volume-starved; lowest-priority long until volume confirms.
5. **TUT/USDT — avoid / needs review** — do not treat as valid open risk; system-integrity item, not a trade idea.

No A/B-tier setups exist in either asset class this cycle — this is a genuine no-clean-trade window, not a system failure. Stocks: best long-watch into the US open is the "was A, demoted to C for market-closed-only" cohort (LMT, ORCL, DELL, COP, XOM, AMGN, ABNB, PANW, LLY, WMT, MCD) — clean of legal/earnings caps; re-evaluate at/after 16:20 pre-open slot. Avoid CSCO (stale post-earnings levels) and REGN/BLK (active legal risk) from that list even after the open.

## 9. Avoid / No Trade
This applies to the current decision window only — never a command to stop scanning, tracking, or the scheduler.
- **Any fresh long chase in the current BTC/ETH downtrend/chop** without a confirmed pullback hold — macro risk-off (91.8-95.4/100) argues against it.
- **VIRTUAL/USDT at current price** — volume (0.1-0.23x avg) does not confirm the move; wait for expansion.
- **Treating TUT/USDT's `triggered` status as valid open risk** — confirmed stale/likely-invalidated, unresolved for 7 consecutive reviews.
- **All stocks C-tier ideas** (LMT, ORCL, DELL, CSCO, etc.) — market closed, entries demoted to C by design, not actionable until RTH confirmation.
- **CSCO, REGN, BLK specifically** even after the open — stale post-earnings levels (CSCO) or active class-action legal risk (REGN, BLK).
- **AMAT** — earnings today; do not chase into or hold through the print.

## 10. Main Risks
- **Invalidation-monitoring integrity gap, still unresolved (7th consecutive review, TUT/USDT)**: the same `triggered` row, unchanged `updated_at`, with a confirmed live invalidation breach from the prior cycle. This undermines confidence in every "active signals" / open-risk read this system produces. HEI/USDT carries the same stale-`updated_at` signature (131h) but was not independently price-verified this cycle.
- **Catalyst mapping degrading further**: 78.6% unmapped this run, continuing a worsening trend flagged in recent prior reviews (73→76%→78.6%).
- **Geopolitical/macro risk-off persists**: Strait of Hormuz standoff externally confirmed still unresolved; this is a grinding overhang, not a one-off headline, and has been the dominant macro driver for multiple consecutive reviews.
- **Swing report is the oldest data source this cycle (~7h)** — used as carry-forward per policy, but BANK/MMT/VIRTUAL zones from it should be sanity-checked against the fresher intraday numbers before acting (done above; zones are consistent across reports).
- **Stocks A/B and C-tier performance both structurally negative** (A/B 7d: -3.0R/PF0.00/n=11 weak; C-tier: PF 0.27/WR 2.4%/n=802) — the stocks desk has not shown a working edge recently; treat any stocks idea today with elevated skepticism regardless of tier.

## 11. Action Plan — next 4 hours
- Watch BANK/USDT for a pullback hold at 0.0378-0.0384 with volume confirmation before any escalation.
- Watch MMT/USDT for a rejection candle at 0.1846-0.1869; do not anticipate the breakdown.
- Watch KORUB/USDT for basket freshness decay (currently <1h, re-check before the 16:20 slot — will be aging toward the 6h fresh-basket cutoff).
- Build the stocks pre-open watchlist from the legal/earnings-clean cohort (LMT, ORCL, DELL, COP, XOM, AMGN, ABNB, PANW, LLY, WMT, MCD) for the 16:20 decision review; do not treat any of it as confirmed before RTH.
- No action required on TUT/USDT or HEI/USDT from this review (advisory-only, no code/data changes) — flagged again in §14 for manual follow-up.
- Re-check catalyst mapping % at the next cycle; if still >70% unmapped, the resolver-coverage TODO should be escalated in priority.

## 12. Final Verdict per Mode
- **Crypto scalp**: no trade; nothing worth stalking this cycle ("Nothing worth stalking yet" per report). Report fresh (07:16).
- **Crypto intraday**: no new A/B. Watchlist: MMT (60.4), BICO (60.0), TST (58.8), HOLO (58.8), HOME (57.9), KAITO (55.1), VIRTUAL (54.0) — none above active-trade threshold.
- **Crypto swing**: strongest lane by weekly stats (14d WR 72%/PF 5.80, touch-based — known to overstate realized edge, read directionally). Zero A/B this cycle. BANK/MMT/BMT/COTI/VIRTUAL top the watchlist; KORUB is the freshest catalyst tie-in. TUT/USDT integrity issue remains open and unresolved.
- **Stocks intraday**: market **CLOSED** (pre-open, cash opens ~16:30 EEST). All candidates including 15 raw A-tier scores (LMT, ORCL, DELL, CSCO, COP, XOM, AMGN, REGN, ABNB, PANW, LLY, SMCI, WMT, BLK, MCD) demoted to C by the market-closed gate; CSCO and REGN/BLK carry additional caps (stale post-earnings, legal risk) that persist past the open. Regime bullish/risk-on carried forward for planning.
- **Stocks swing/invest**: excluded — deprecated data source, last dated 2026-07-02.
- **System integrity**: **manual review required** — TUT/USDT invalidation-monitoring gap confirmed unchanged for a 2nd consecutive review (7th overall); catalyst mapping at a new low (78.6% unmapped); untracked-alert detector clean (0 findings) today.

## 13. Sources
- [Bitcoin price today, BTC to USD live price, marketcap and chart | CoinDesk](https://www.coindesk.com/price/bitcoin) — BTC ~$63,798.81 as of Aug 13, 2026 03:49 EDT, corroborates internal reports' $63.5-64K read.
- [Oil prices today: Uncertainty over U.S.-Iran Strait of Hormuz deal (CNBC)](https://www.cnbc.com/2026/08/10/oil-prices-today-brent-wti-hormuz-trump-iran.html) — confirms Hormuz standoff unresolved, Brent volatility, corroborates internal risk-off macro read.
- [Iran war tensions over Hormuz fail to lift oil prices (AGBI)](https://www.agbi.com/oil-and-gas/2026/08/iran-war-tensions-over-hormuz-fail-to-lift-oil-prices/) — Iran-Oman talks stalled, US blockade cited as blocker, Brent up >40% YTD.
- Internal: `data/reports/scalp/2026-08-13_07-16_scalp_report.md`, `data/reports/intraday/2026-08-13_07-24_intraday_report.md`, `data/reports/swing/2026-08-13_01-37_swing_report.md`, `data/reports/stocks/intraday/2026-08-13_07-51_stocks_intraday_report.md`, `data/catalysts/2026-08-13/catalyst_events.jsonl`.

## 14. Fix Requests / TODO

### TODO-invalidation-monitor-gap
- **issue:** `proposed_signals` rows can remain `status='triggered'` after price has breached their own `invalidation` level, with no automatic transition to `stopped`/`expired`. Confirmed for TUT/USDT by live price in the 2026-08-13 04:45 EEST review; this review confirms the same row is still completely unchanged 7 hours later (`updated_at` identical). HEI/USDT shows the same stale-`updated_at` signature (131h) but was not independently price-re-verified this cycle.
- **evidence:** `db/crypto_ai_desk.sqlite` → `proposed_signals` WHERE `symbol='TUT/USDT' AND status='triggered'` → row with `entry=0.14283714`, `invalidation=0.09882286`, `updated_at='2026-08-09T17:01:44+00:00'`, `validity_window_hours=168`, `expires_at='2026-08-16T15:38:12+00:00'`; oldest-`triggered` audit shows 43/45 currently-`triggered` crypto rows are >24h old (35/45 >72h old), and all 17 currently-`triggered` stocks rows are >72h old — age alone isn't proof of breach given the 168h swing validity window, but it means the book currently cannot distinguish legitimately-still-open positions from functionally-dead ones without a manual price check per symbol.
- **suggested manual fix:** a human-driven session should (1) re-verify TUT/USDT and HEI/USDT current price vs invalidation directly, (2) audit whether the invalidation-monitor process is running on the expected cadence for `triggered`-status rows specifically (as opposed to `waiting_for_entry` rows, which do appear to be monitored), (3) consider whether this is the same root cause as the `[[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]]`-flagged issue or a distinct one.
- **priority:** high
- **first observed (this exact row):** 2026-08-09 (per `updated_at`); first flagged in an Opus review 2026-08-13 04:45 EEST; this is the 2nd consecutive scheduled review confirming zero change.

### TODO-catalyst-mapping-coverage
- **issue:** catalyst-to-symbol mapping has been trending down across recent reviews (73% → 76% → 78.6% unmapped) and is now well past the 50% weak-mapping threshold used by this review's own gating logic.
- **evidence:** `data/catalysts/2026-08-13/catalyst_events.jsonl` — 1,500 events today, 321 mapped (21.4%), 1,179 unmapped (78.6%).
- **suggested manual fix:** audit the symbol resolver in the catalyst ingestion layer (`src/news/` per prior hardening work) for why an increasing share of events aren't getting a symbol tag — could be a source-mix shift (more macro/general-market headlines with no single ticker) rather than a resolver regression; worth a human read of a sample of unmapped events to distinguish the two before any code change.
- **priority:** medium
- **first observed:** trend noted across the last 2-3 scheduled reviews; this run's exact figure first observed 2026-08-13 11:39 EEST.
