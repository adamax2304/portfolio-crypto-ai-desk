# Opus Enriched Review — late-session risk review — Auto Cycle 21:40 EEST

## 1. Executive Summary

**Late-session risk review, 21:40 EEST (18:40 UTC / ~14:40 ET) — US cash session ~5h10m old, ~1h20m from the 16:00 ET close. Advisory only — no auto-trade.** Crypto mood **upgraded to bullish trend / risk-on** since the 18:45 review: BTC transition_up, ETH uptrend, altcoin breadth 65.9-68.3% above EMA20/50 (up from ~52%), though no A-tier crypto setup exists and macro risk stays elevated (89-100/100 depending on report) on a stacked exploit/geopolitics overhang (Coldcard wallet exploit now ~1,778-2,055 BTC stolen across 3 waves, a second SafePal wallet data-breach headline, plus a new Iran/Strait-of-Hormuz theme). **Stocks got a genuine fresh post-open rescan this cycle (18:32 UTC, ~8 min old at review time)** — and it materially reverses the prior review's top pick: all 15 previously-A-tier stocks longs (GE, INTC, BAC, MU, MRVL, LMT, SMCI, UBER, AMGN, REGN, ASML, PYPL, TSM, NVDA, SMH) were demoted to C-tier / not-actionable this cycle by the rolling drawdown guard and market-context-conflict gates — GE is **no longer a clean actionable long**, contradicting the 18:45 review. The desk's only fresh A/B-tier stocks idea this cycle is **BX short** (B-tier, intraday, aligned with the guard-approved shorts subset, PF 9.00 on the 14d evidence cited in its own playbook note). Two stocks names newly carry **legal/headline risk flags**: SMCI (indictment) and REGN (class action) — both already C-tier/non-actionable, so no protocol downgrade is needed, but both are worth tracking. **Carried-forward critical data-integrity issue, now flagged a 5th consecutive cycle: 6 open crypto swing positions (HOLO, AVNT, PROM, LUNA, MMT, BABY) are confirmed still OPEN_ACTIVE and being monitored for TP/SL off OHLCV frozen at 2026-08-15 22:30 UTC (~44h stale)** — no remediation across ~44h of tracking. Best crypto long-watch: **GPS/USDT** (B-tier swing, on a defined pullback, but tagged `avoid_chase`/`wait_pullback` if extended). Best short-watch (either asset class): **BX** (stocks, B-tier intraday, cleanest actionable setup on the desk this cycle). No clean catalyst-backed actionable exists this window — GE remains the best catalyst-watch pending the market-context-conflict gate clearing. Avoid: **SMCI** (fresh indictment headline) and chasing **GPS/ACE/BTW** at current extension.

## 2. Data Used

- Scheduler: `data/scheduled_runs/2026-08-17_default_schedule/scheduler.log` (mtime 21:40 EEST — current, fresh). Latest `cycle_01_16-18_summary.md` (mtime 18:54 EEST, ~2h46m old) — jointly clears the 3h defer threshold easily.
- Reports: scalp `2026-08-17_18-39` (UTC filename = 21:39 EEST, ~1min old — very fresh), intraday `2026-08-17_14-05` (UTC = 17:05 EEST, ~4h35m old — stale for an intraday horizon, no fresher crypto-intraday scan exists this cycle, used with caveat), swing `2026-08-17_15-43` (UTC filename = 18:43 EEST header-confirmed, ~2h57m old — **fresh**, first genuinely fresh swing scan in several cycles), stocks intraday `2026-08-17_18-32` (UTC filename = 21:32 EEST, ~8min old — **very fresh, genuine post-open confirmation**, first of the day), stocks swing/invest `2026-07-02` (6+ weeks stale, expected/deprecated per known project state).
- Catalysts: `data/catalysts/2026-08-17/catalyst_events.jsonl` (1,672 events, mtime 17:11 EEST — **unchanged since the 18:45 review, now ~4h29m stale**; see TODO-3), `narrative_baskets.jsonl` (3 baskets, same mtime), `catalyst_cycle_14-11.md` (latest cycle summary — no fresher cycle has landed this run).
- LLM packets: `llm_analysis_packet.md` (generated 2026-08-17T18:39:30 UTC = 21:39:30 EEST — very fresh, matches the scalp report), `llm_stocks_packet.md` (mtime 17:38 EEST, superseded this cycle by the fresher `2026-08-17_18-32` stocks-intraday report read directly).
- `reports/PAPER_MONITOR_STATUS_LATEST.md` (mtime 18:50 EEST, ~50min old — fresh, used as the **authoritative lifecycle source** this cycle, unlike 18:45 when it was stale).
- CLI: `active-signals --asset-class crypto` (n=50), `active-signals --asset-class stocks` (n=50), `signal-stats --asset-class crypto` (A/B headline sample=78, PF 2.79, totalR +25.1), `signal-stats --asset-class stocks` (intraday-only sample=594, PF 0.19, totalR -10.5; C-tier winrate 6%), `detect_untracked_legacy_alerts --since 2026-08-17` → **clean, no untracked alerts**.
- Direct file check: `data/raw/ohlcv/binance/15m/{HOLO,AVNT,PROM,LUNA,MMT,BABY,WLFI,CHIP}_USDT.csv` last-row timestamps — re-confirms the 6-symbol freeze is unchanged and pair-specific (WLFI/CHIP are fresh controls, last rows today).
- Direct catalyst-file count: `catalyst_events.jsonl` parsed for mapped-vs-unmapped symbol ratio (1,672 total / 534 mapped / 1,138 unmapped = 68.1% unmapped).
- Prior review for comparison: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-17_1845.md` (US open reaction review, 18:45 EEST).
- **External web research not attempted this cycle** — internal data (two genuinely fresh reports — swing and stocks-intraday — plus a fresh lifecycle file) was sufficient, internally consistent, and materially informative on its own; no contradiction required external verification per §G. Noted per source-discipline checklist.

## 3. Scheduler / Data Freshness

- Scheduler fresh (current-minute mtime). Cycle-summary 2h46m old. Both clear the 3h joint-defer threshold comfortably.
- Crypto: scalp very fresh (~1min), swing fresh (~2h57m, first non-stale swing scan in several cycles), intraday stale (~4h35m, no fresher source, used with caveat).
- Stocks intraday: **genuinely fresh post-open scan this cycle** (~8min old, "Market session: regular session", data freshness 18:32 UTC vs current 18:40 UTC) — resolves the pre-open-snapshot caveat that applied to the 15:59 and 18:45 reviews.
- **Data-integrity carry-forward, confirmed for the 5th consecutive cycle today (04:40 → 11:40 → 15:59 → 18:45 → now 21:40):** the same 6 crypto symbols (HOLO, AVNT, PROM, LUNA, MMT, BABY) remain frozen on 15m OHLCV at 2026-08-15 22:30:00 UTC (now ~44h stale). `reports/PAPER_MONITOR_STATUS_LATEST.md` (fresh, 18:50 EEST) confirms all 6 are **OPEN_ACTIVE** positions still being monitored for TP/SL off this frozen feed. Control symbols WLFI and CHIP are fresh (last rows today). No progress on remediation in ~44h. See TODO-1.
- `detect_untracked_legacy_alerts --since 2026-08-17`: **clean** — every legacy crypto alert has a backing proposed_signal.
- Signal-duplication anomaly, still present this cycle (was INTC/BAC/GE at 18:45, now shifted to different symbols): the stocks active-signals pull shows BX ×3 identical `waiting_for_entry` rows (same entry/invalidation/expiry) and AMZN ×3 identical `tp1_hit` rows. See TODO-2 (carried forward).
- **New this cycle:** catalyst-scan cadence appears stalled — `catalyst_events.jsonl`/`catalyst_cycle_14-11.md` mtimes are identical to the 18:45 review (17:11 EEST), meaning no catalyst cycle has landed in ~4h29m despite the scheduler completing at least one full cycle (cycle summary at 18:54) in that window. See TODO-3 (new).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-08-17 21:40 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["stocks swing/invest 6wk+ stale (expected/deprecated)", "no fresher crypto-intraday scan than 17:05 EEST"],
      "suggested_effect": "advisory_only",
      "facts_used": ["6 crypto symbols frozen at 2026-08-15 22:30 UTC (~44h stale), confirmed 5th consecutive cycle, all 6 OPEN_ACTIVE per fresh paper-monitor file", "catalyst layer unchanged/stale since 17:11 EEST (~4h29m), no new cycle landed despite scheduler activity", "stocks-intraday and swing reports are both genuinely fresh this cycle (first time in several cycles for both)"] },
    { "agent": "market_regime", "verdict": "risk_on", "confidence": 0.7,
      "reason_codes": ["risk_on", "longs_preferred", "shorts_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC transition_up, ETH uptrend, altcoin breadth 65.85-67.5% above EMA20, up from ~52% at 18:45 — regime label upgraded chop→bullish trend risk-on", "stocks: VIX 14.95, breadth 100% above EMA20/50, 4/4 indices uptrend, regime label bullish — but stocks_intraday_long_guard is actively blocking nearly the entire A-tier long cohort on rolling paper-R drawdown grounds, so risk-on tape does not currently translate into actionable stocks longs"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.45,
      "reason_codes": ["mapping_weak", "stale_catalyst", "narrative_supported", "catalyst_contradicted"],
      "data_missing": ["no catalyst cycle newer than 17:11 EEST this run"],
      "suggested_effect": "advisory_only",
      "facts_used": ["1,672 catalyst events today, 68.1% unmapped (534/1672 mapped) — identical to 18:45, mapping layer itself stale, not just weak", "3 unchanged narrative baskets: delisting_thin_liquidity (ATOM), rwa_narrative (ONDO/XLM), momentum_breakout (GPS/ACE/BTW, avoid_chase)", "GE's catalyst (industrial-AI capex tailwind) is real but the fresh stocks scan gates it out on market_context_conflict + catalyst_none_and_not_exceptional_technical"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.4,
      "reason_codes": ["data_unavailable", "squeeze_risk", "oi_supports"],
      "data_missing": ["OI 24h% n/a for GPS/ACE/BTW/HEMI (MEXC/bybit fallback symbols)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ACE/USDT: negative funding across bybit+mexc, crowding elevated — squeeze-prone if chased", "GPS/USDT: funding neutral/slightly negative, crowding low — cleaner than ACE", "ETH/USDT: price up + OI up, fresh positioning confirms trend"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "overextended", "entry_fresh", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["GPS/USDT: preferred pullback entry 0.0149-0.0155, current price 0.0158 — at/just past the top of the planned zone, borderline chase", "ACE/BTW both still tagged overextended/momentum_breakout basket (avoid_chase/wait_pullback)", "BX short: not yet triggered (waiting_for_entry 141.43-142.15), technical_setup subscore 23.10/highest component, RR to TP1 1.50 — clean, not chasing"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.75,
      "reason_codes": ["open_actionable", "review_shadow", "no_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PAPER_MONITOR_STATUS_LATEST.md (fresh, authoritative this cycle): OPEN_ACTIVE=20, WAITING_FOR_ENTRY=0, REVIEW_ONLY_SHADOW=8, ENTERED_UNRESOLVED_EXPIRED=0, NO_ENTRY_EXPIRED=187, CLOSED_WIN=158, CLOSED_LOSS=7, CLOSED_FLAT=40, UNKNOWN_INCONSISTENT=0", "6 of the 20 OPEN_ACTIVE positions (HOLO/AVNT/PROM/LUNA/MMT/BABY) run on the frozen OHLCV feed — needs_review", "stocks active-signals still lists GE/INTC/BAC as triggered/waiting_for_entry from earlier cycles even though the fresh 18:32 rescan demotes all three to C — stale-vs-fresh classification gap, see TODO-4"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["legal_risk", "headline_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["SMCI: active legal/headline risk flag (indictment), C-tier this cycle — no live A/B exposure but watch if it re-promotes", "REGN: active legal/headline risk flag (class_action), C-tier this cycle — same treatment", "HD and PANW have earnings tomorrow (2026-08-18) — explicit do-not-chase warning from the desk itself", "BTC exploit_hack risk warnings (Coldcard ~2,055 BTC, SafePal breach) continue layering onto an already-elevated macro score"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto A/B headline: sample=78, winrate 18.3%, PF 2.79, totalR +25.1 — edge still driven almost entirely by swing (PF 5.28); intraday and scalp both negative avgR", "crypto direction=short: n=8, PF 0.0, avgR -0.50, totalR -3.0 — still a losing bucket, extra skepticism warranted on any new crypto short idea", "stocks intraday all-tier: PF 0.19, totalR -10.5, winrate 8.8%; A-tier long guard is actively (and per the desk's own evidence, correctly) blocking nearly every A-tier long this cycle", "BX's own playbook note cites stocks-intraday B-tier 14d WR 55% / PF 2.03, shorts subset PF 9.00 — the shorts subset is the one currently-working stocks bucket"] },
    { "agent": "head_trader", "verdict": "advisory_synthesis_only", "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["see section 8 below"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "GPS/USDT", "trigger": "clean pullback confirmation into 0.0149-0.0155 with price accepting the zone rather than chasing; already an existing triggered swing position, not a fresh add at current price 0.0158" },
    "best_short_candidate":    { "symbol": "BX", "trigger": "waiting_for_entry 141.43-142.15, B-tier, aligned with the guard-approved stocks-shorts playbook (14d PF 9.00 subset), invalidation 142.87" },
    "best_catalyst_candidate": { "symbol": "GE", "trigger": "no clean catalyst-backed actionable exists this window — GE's capex-tailwind catalyst is real but gated by market_context_conflict; re-open only if a later cycle clears that gate with fresh confirmation" },
    "avoid_candidate":         { "symbol": "SMCI", "reason": "fresh active legal/headline risk flag (indictment) this cycle; already C-tier/non-actionable but do not treat as a clean idea if it re-promotes without the flag clearing" },
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
| market_regime | risk_on | 0.70 | risk_on, longs_preferred, shorts_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.45 | mapping_weak, stale_catalyst, narrative_supported, catalyst_contradicted | advisory_only |
| derivatives_squeeze | caution | 0.40 | data_unavailable, squeeze_risk, oi_supports | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, overextended, entry_fresh, clean_retest | advisory_only |
| execution_lifecycle | needs_review | 0.75 | open_actionable, review_shadow, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.70 | legal_risk, headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.60 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | advisory_synthesis_only | 0.65 | — | advisory_only |

## 4. What Changed vs Previous Review (vs 18:45 EEST US open reaction review)

- **Reversed:** GE is no longer a clean actionable long. The 18:45 review's top pick was based on an earlier-cycle "triggered" signal; the fresh 18:32 UTC post-open rescan demotes GE (and all 14 other prior A-tier stocks longs) to C-tier via `market_context_conflict` / `catalyst_none_and_not_exceptional_technical` / `stocks_intraday_long_guard`. See TODO-4.
- **New:** SMCI (indictment) and REGN (class_action) now carry active legal/headline risk flags in the fresh stocks scan — neither was flagged at 18:45.
- **New:** the only fresh A/B-tier stocks idea this cycle is BX short — same symbol was already present as a duplicate `waiting_for_entry` row in the 18:45 active-signals pull, but is now confirmed by a genuine post-open scan with full evidence (technical_setup 23.10, RR 1.50).
- **Improved:** crypto mood upgraded from chop to bullish trend/risk-on; altcoin breadth rose from ~52% to 65.9-68.3% above EMA20/50; the swing report is genuinely fresh for the first time in several cycles (~2h57m vs 14h+ previously).
- **Resolved (not reproduced):** the WLFI/USDT bias-tag contradiction flagged at 18:45 (long position vs short-biased tag) does not reappear in this cycle's freshest crypto packet — WLFI no longer appears in the Weakest Symbols list. Treat as resolved pending next-cycle confirmation, not proven fixed.
- **Unchanged / escalating:** OHLCV freeze on the same 6 crypto symbols, now confirmed a 5th consecutive cycle (~44h stale), still no remediation (TODO-1).
- **Unchanged:** duplicate signal_id emission (TODO-2), now on BX/AMZN instead of INTC/BAC/GE — same underlying pattern, not fixed.
- **New:** catalyst-scan cadence appears stalled at 17:11 EEST — the mapped/unmapped catalyst counts are byte-for-byte identical to the 18:45 review (534/1672), meaning no new catalyst cycle has run in ~4h29m (TODO-3, new).
- **Dropped from consideration:** META and AMZN, both deep-dived at 18:45, do not appear anywhere in the fresh 18:32 stocks-intraday scan's Top Candidates or Actionable sections this cycle — treat their prior theses as stale/expired, not invalidated.

## 5. Catalyst Coverage

- Total catalyst_events today: **1,672**. Mapped (non-null symbol): **534** (32%). Unmapped: **1,138** (68.1%).
- Narrative baskets: **3** — `delisting_thin_liquidity` (ATOM, avoid_low_liquidity), `rwa_narrative` (ONDO/XLM, related_beta_rotation), `momentum_breakout` (GPS/ACE/BTW, avoid_chase) — all unchanged since 17:11 EEST.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Additionally, the catalyst layer itself is stale this cycle (~4h29m, no cycle since 17:11 EEST) — treat catalyst-backed conclusions as background context only, not as confirming this cycle's price action.
- Top 3 unmapped headlines (same set as last cycle, no fresher scan available): "SK Hynix's Stock Trades at Around 5 Times Next Year's Earnings Even After Revenue Grew 257%..."; "Navy SEALs criticize Trump over Pacific military base readiness issues"; "US businesses' AI spending surges to $7,400 per employee monthly as corporate divide widens."

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **risk-on / bullish trend** (BTC transition_up, ETH uptrend, altcoin breadth 65.9-68.3% above EMA20/50 — a real improvement from chop at 18:45), but macro risk stays elevated (89.3-100/100 across reports) on a stacked exploit/geopolitics overhang
- Stocks mood: **risk-on tape (VIX 14.95, breadth 100%, 4/4 indices uptrend) that is not currently translating into actionable longs** — the rolling drawdown guard is blocking nearly the entire A-tier long cohort this cycle
- Dominant narrative: crypto — momentum-breakout cluster (GPS/ACE/BTW) plus a growing BTC exploit stack (Coldcard ~2,055 BTC, SafePal breach); stocks — AI capex tailwind real but currently gated out of actionability, shorts subset (BX-style) is the working playbook
- Preferred side now: **mixed — crypto selective longs on confirmed pullbacks only; stocks shorts (guard-approved subset), not longs, until the drawdown guard eases**
- Best long candidate: **GPS/USDT** (crypto, B-tier swing, existing triggered position; new adds only on a genuine pullback into 0.0149-0.0155, not at the current 0.0158)
- Best short candidate: **BX** (stocks, B-tier intraday, waiting_for_entry 141.43-142.15, cleanest single actionable setup on the desk this cycle)
- Best catalyst-backed candidate: **none clean this window** — GE's catalyst is real but gated; treat as catalyst-watch only
- What to avoid: **SMCI** (fresh indictment flag), chasing **GPS/ACE/BTW** at current extension, treating any of the 15 gate-demoted stocks A-tier longs (GE/INTC/BAC/MU/etc.) as actionable off their stale earlier-cycle signal rows, and managing **HOLO/AVNT/PROM/LUNA/MMT/BABY** off the displayed price/TP/SL (frozen feed, unverified)
- What would change the view: OHLCV feed remediation for the 6 frozen crypto symbols; a fresh catalyst-scan cycle; the stocks long-guard easing (would need a positive paper-R stretch to reopen A-tier longs); GPS/ACE pulling back into their tagged entry zones

## 7. Candidate Deep Dives

**1. BX — stocks, B-tier, short, intraday, waiting_for_entry (141.43-142.15, invalidation 142.87)**
- Catalyst: 2 internal news catalysts in the lookback window (not independently re-verified externally this cycle — internal data fresh and sufficient, no contradiction found).
- Price reaction: not yet triggered — has not yet reacted, so chase risk is low; RR to TP1 is 1.50, one of the highest of any candidate scanned this cycle.
- Legal/headline risk: none found for BX in the fresh scan's risk-warning block.
- Aligned with market mood: yes for the *playbook* (guard-approved shorts subset, PF 9.00 on 14d evidence), even though the broader stocks tape is risk-on — this is a stock-specific technical short (RS vs SPY +10.02%, i.e. BX itself has been a relative-strength leader, now showing a downtrend/below-prev-day-low setup), not a tape-level bet.
- Actionable now: only once price prints into the 141.43-142.15 zone; do not chase below it.
- Would invalidate: close beyond 142.87.
- Note: 3 identical duplicate `signal_id` rows for this same setup in the active-signals pull — treat as one setup (TODO-2).

**2. GE — stocks, previously A-tier, long, intraday — now demoted to C ("watchlist / not actionable") in the fresh 18:32 rescan**
- Contradiction vs the 18:45 review: that review named GE "cleanest actionable, already triggered" based on an earlier-cycle signal row (still showing tp1_hit/triggered/waiting_for_entry in the raw active-signals table). The fresh, genuinely post-open rescan explicitly gates GE out: `market_context_conflict`, `catalyst_none_and_not_exceptional_technical`.
- Catalyst: the capex-tailwind / GE-Aerospace-Kratos contract story is still real and still cited by the desk (`GE [geopolitical_risk]: risk_warning` block also references the same Kratos contract), but the gate logic determined the broader market context conflicts with the setup this cycle.
- Legal/headline risk: none found.
- Actionable now: **no** — treat as catalyst-watch only, not a live long, until a future rescan clears the conflict gate.
- Note: the earlier-cycle GE signal rows (tp1_hit ×2, triggered/waiting_for_entry) remain in the active-signals lifecycle table; this is expected system behavior (older signals aren't retroactively deleted when a fresh scan changes tier), but operators reading the raw active-signals CLI output without cross-checking the freshest report could mistake GE for still-actionable. See TODO-4.

**3. SMCI / REGN — stocks, C-tier, both flagged with active legal/headline risk this cycle**
- SMCI: `legal_headline_risk: indictment` — demoted A→C for this reason specifically (not for the drawdown guard like most of the rest of the cohort). No live A/B exposure currently.
- REGN: `legal_headline_risk: class_action` — same treatment, demoted A→C specifically for the legal flag.
- Per source-discipline protocol (§I), if either re-promotes to A/B in a future cycle without this flag clearing, it must be downgraded to MANUAL REVIEW REQUIRED, not treated as a clean actionable, regardless of score.
- Actionable now: no — both are C-tier/watchlist only.
- What would change the view: the underlying legal story resolving/being dismissed, or a corroborating second source firming up the risk (worth a human check next time either symbol scores into A/B).

**4. GPS/USDT — crypto, B-tier, swing, long, existing triggered position (entry 0.014880-0.015538, invalidation 0.014075)**
- Has price already reacted to the catalyst? No fresh verified catalyst is attached to GPS itself — this is a pure momentum/relative-strength setup (24h +49.3%, RS vs BTC +48.2%), not catalyst-driven.
- Is the setup chasing? Borderline — the swing report's own preferred pullback zone is 0.0149-0.0155; current price 0.0158 sits at/just past the top of that zone.
- Retest/pullback structure: yes, defined explicitly by the desk (pullback into 0.0149-0.0155).
- Overextended vs EMA20? Tagged `overextended` in the momentum_breakout basket alongside ACE/BTW — treat fresh adds with caution.
- Aligned with market mood: yes (bullish trend, selective-longs style favors RS leaders on pullback).
- Actionable now: as an **existing position**, yes (already triggered, running); as a **fresh add**, only on confirmed pullback acceptance into the zone, not at the current price.
- Would invalidate: 1h close beyond 0.0141.
- Is this chase-risk: yes if adding now; no if simply holding the existing triggered position.

**5. Frozen-feed crypto swing book — HOLO, AVNT, PROM (×2), LUNA, MMT, BABY — all OPEN_ACTIVE**
- Not a new candidate — an existing-book data-integrity risk, included here because it materially affects "what's actionable" this window.
- All 6 are confirmed OPEN_ACTIVE in the fresh `PAPER_MONITOR_STATUS_LATEST.md` (18:50 EEST), meaning the system is actively monitoring these for TP/SL hits off a feed frozen at 2026-08-15 22:30 UTC — any TP/SL trigger event on these 6 names should be treated as unverified until the feed is confirmed live again.
- Would invalidate/resolve: OHLCV ingest remediation for this specific symbol set (see TODO-1); until then, no new adds to this set and no confidence in displayed price/TP/SL state for the existing 6.

## 8. Best Candidates Ranked

1. **BX (short)** — cleanest actionable on the desk this cycle, clean RR, guard-approved playbook, not yet triggered. Trigger: price into 141.43-142.15.
2. **GPS/USDT (long, existing position)** — best crypto long-watch, but treat a fresh add as chase-risk unless a real pullback into 0.0149-0.0155 prints.
3. **GE (catalyst-watch only)** — real catalyst, currently gated by market_context_conflict; re-open only on a future rescan clearing the gate with fresh confirmation.
4. **SMCI / REGN (avoid / legal-risk watch)** — both C-tier and flagged; watch for the legal story resolving before treating either as clean even if it re-scores into A/B.
5. **Frozen-feed swing book (needs-review, not a fresh add)** — HOLO/AVNT/PROM/LUNA/MMT/BABY, existing positions only, data-integrity caveat on all displayed levels.

**Excess candidates not deep-dived (slot cap):** INTC and BAC — same demotion logic as GE (market_context_conflict / long-guard gates), not separately dived to avoid repeating the GE analysis. ACE/BTW — same momentum_breakout/avoid_chase treatment as GPS, held out for brevity.

## 9. Avoid / No Trade (this decision window only)

- **SMCI** as any kind of long — fresh indictment flag, C-tier, do not treat as clean even at a high score.
- **GE, INTC, BAC** and the other 12 gate-demoted stocks A-tier longs — real scores, but explicitly not actionable this cycle per the fresh rescan; do not act on their stale earlier-cycle "triggered"/"waiting_for_entry" rows.
- **GPS/USDT, ACE/USDT, BTW/USDT** as fresh crypto adds at current extension — wait for the tagged pullback zones.
- **HOLO, AVNT, PROM, LUNA, MMT, BABY** — do not add to or manage these open crypto swing positions off the displayed price/TP/SL; feed frozen ~44h, unverified. Existing positions continue running per system logic; this is a data-quality caution, not a stop-the-system instruction.
- This is a decision-window-only read — scanning, candidate generation, and tracking continue uninterrupted regardless of this section.

## 10. Main Risks

- **Frozen OHLCV on 6 open crypto swing positions**, 5th consecutive cycle unresolved (~44h stale), all 6 confirmed OPEN_ACTIVE — displayed price/TP/SL cannot be trusted until the feed is fixed.
- **Stocks long-guard is currently blocking almost the entire A-tier long cohort** (15 names this cycle) — appropriate given the desk's own 30d evidence (bullish-regime longs net -3.0R, continuation setups net -4.0R, no_news longs net -4.0R), but it means "risk-on tape" and "actionable longs" have decoupled this cycle; do not read index-level bullishness as a green light for individual stock longs right now.
- **Catalyst layer itself is stale** (~4h29m, no cycle since 17:11 EEST) — catalyst-backed conclusions this review should be read as background context from ~4.5h ago, not live confirmation.
- **Legal/headline risk newly active on SMCI (indictment) and REGN (class_action)** — both currently non-actionable, but watch closely if either re-scores into A/B in a future cycle.
- **Duplicate signal emission continues** (BX ×3, AMZN ×3 this cycle) — inflates apparent setup counts; read active-signal counts with that in mind.
- **Crypto short bucket remains a losing playbook** (n=8, PF 0.0, totalR -3.0) — any new crypto short idea needs extra skepticism until sample size improves; no fresh crypto short idea exists in this cycle's reports regardless.
- **Macro/geopolitics risk still elevated** (89.3-100/100) — Coldcard exploit now ~2,055 BTC stolen, a second SafePal wallet breach headline, and a new Iran/Strait-of-Hormuz theme layering onto an otherwise-improving crypto tape.
- **Stale-vs-fresh classification gap** — active-signals CLI still lists gate-demoted names (GE/INTC/BAC) as triggered/waiting_for_entry from earlier cycles; an operator reading only the CLI output (not the freshest report) could mistake them for still-actionable (TODO-4).

## 11. Action Plan — next 4 hours

- Do not add to GE/INTC/BAC/any of the 15 gate-demoted stocks longs unless a future rescan clears their specific demotion reasons.
- Watch BX for entry into 141.43-142.15; do not chase if it gaps through the zone.
- Watch GPS/USDT for a genuine pullback into 0.0149-0.0155 before considering a fresh add; the existing triggered position continues running per system logic.
- Re-check OHLCV feed remediation for the 6 frozen crypto symbols at the next cycle (6th consecutive check).
- Watch for the next catalyst-scan cycle to land; if `catalyst_events.jsonl` mtime is still 17:11 EEST at the next review, escalate TODO-3.
- Into the close (~1h20m away): expect the next review (post-close final daily review) to assess today's outcome by mode/tier and flag anything that should carry overnight vs expire.
- No new crypto swing adds recommended given the frozen-feed exposure already on the book.

## 12. Final Verdict per Mode

- **Crypto scalp:** no clean actionable this window; desk-documented negative-avgR mode this week — continue data collection only.
- **Crypto intraday:** no fresh clean intraday long/short surfaced this cycle; intraday-mode PF is negative on the week (avgR -0.01).
- **Crypto swing:** bullish-trend backdrop, GPS/USDT is the best long-watch (pullback-only for fresh adds); existing book carries data-integrity risk on 6 positions (needs review); no new adds recommended this window.
- **Stocks intraday:** genuine post-open confirmation this cycle — BX short is the only clean actionable; the entire A-tier long cohort is guard-demoted to C, treat as non-actionable regardless of score; HD/PANW earnings tomorrow, do not chase either into the print.
- **Stocks swing/invest:** deprecated framework, no signal (per known project state).

## 13. Sources

- Internal: `data/reports/stocks/intraday/2026-08-17_18-32_stocks_intraday_report.md` — fresh post-open scan, source for the GE/INTC/BAC/etc. demotion, SMCI/REGN legal flags, and the BX idea card.
- Internal: `data/reports/swing/2026-08-17_15-43_swing_report.md` — fresh swing scan, source for the crypto market-regime upgrade and the GPS/USDT trade idea.
- Internal: `data/processed/llm_analysis_packet.md` (generated 2026-08-17T18:39:30 UTC) — source for the crypto macro/geopolitics risk score and headline list (Coldcard exploit, Strait of Hormuz).
- Internal: `reports/PAPER_MONITOR_STATUS_LATEST.md` — source for the authoritative lifecycle counts and confirmation that the 6 frozen-feed symbols are OPEN_ACTIVE.
- Internal: `data/catalysts/2026-08-17/catalyst_cycle_14-11.md` and direct parse of `catalyst_events.jsonl` — source for catalyst mapping ratio and narrative baskets.
- Internal: direct OHLCV CSV timestamps, `data/raw/ohlcv/binance/15m/{HOLO,AVNT,PROM,LUNA,MMT,BABY,WLFI,CHIP}_USDT.csv`, read 2026-08-17 ~21:40 EEST, used for the frozen-feed finding.
- No external web sources this cycle — internal data was fresh, sufficient, and internally consistent for every candidate; see §2.

## 14. Fix Requests / TODO

### TODO-1 (carried forward, escalating — 5th consecutive cycle)
- **issue:** 6 crypto swing positions (HOLO, AVNT, PROM, LUNA, MMT, BABY) are open (OPEN_ACTIVE per paper-monitor) and being monitored for TP/SL off 15m OHLCV frozen at 2026-08-15 22:30:00 UTC.
- **evidence:** `data/raw/ohlcv/binance/15m/{HOLO,AVNT,PROM,LUNA,MMT,BABY}_USDT.csv` all last-row `2026-08-15 22:30:00+00:00`, checked 2026-08-17 ~21:40 EEST (~44h stale). Control symbols WLFI/CHIP fresh (last rows today). `reports/PAPER_MONITOR_STATUS_LATEST.md` (18:50 EEST) confirms all 6 as OPEN_ACTIVE. Also flagged in `_0440.md`, `_1140.md`, `_1559.md`, `_1845.md`.
- **suggested manual fix:** investigate the OHLCV ingest/refresh path for this specific symbol set; verify whether the paper-monitor TP/SL logic for these 6 positions is reading this frozen file or a separate live-price source (if the latter, the risk is smaller than it looks but should be confirmed, not assumed).
- **priority:** high
- **first observed:** 2026-08-17 02:00 EEST (carried through 04:40, 11:40, 15:59, 18:45, now 21:40)

### TODO-2 (carried forward, symbols changed)
- **issue:** Duplicate signal_id emission for the same underlying setup continues — this cycle BX shows 3 identical `waiting_for_entry` rows and AMZN shows 3 identical `tp1_hit` rows (was INTC/BAC/GE at 18:45).
- **evidence:** `python -m src.cli active-signals --asset-class stocks` output, 2026-08-17 ~21:40 EEST.
- **suggested manual fix:** same as previously logged — investigate the stocks signal-generation path for a dedup gate on symbol+tier+mode+entry-zone within a short time window.
- **priority:** medium
- **first observed:** 2026-08-17 18:40 EEST (recurring, not yet fixed)

### TODO-3 (new this cycle)
- **issue:** Catalyst-scan cadence appears stalled — `data/catalysts/2026-08-17/catalyst_events.jsonl` and `catalyst_cycle_14-11.md` mtimes are unchanged since 17:11 EEST, identical byte-for-byte counts to the 18:45 review, despite the scheduler completing at least one full cycle (summary at 18:54 EEST) in the intervening ~4.5h.
- **evidence:** `ls -la data/catalysts/2026-08-17/` shows latest cycle file `catalyst_cycle_14-11.md` (mtime 17:11 EEST); direct parse of `catalyst_events.jsonl` returns identical mapped/unmapped counts (534/1672) as the 18:45 review.
- **suggested manual fix:** check whether the catalyst-scan step is still wired into the scheduler's cycle loop, or is failing/erroring silently; compare against `scheduler.log` for the relevant time window to see if the step was skipped or threw.
- **priority:** medium
- **first observed:** 2026-08-17 21:40 EEST

### TODO-4 (new this cycle)
- **issue:** Active-signals CLI output does not reflect same-day tier demotions from a fresher rescan — GE, INTC, and BAC still show as `triggered`/`waiting_for_entry`/`tp1_hit` in `active-signals --asset-class stocks` even though the fresh 18:32 UTC rescan demotes all three to C-tier/not-actionable (`market_context_conflict`, `stocks_intraday_long_guard`, etc.). An operator reading only the raw active-signals table without cross-referencing the freshest report could treat these as still-actionable.
- **evidence:** compare `python -m src.cli active-signals --asset-class stocks` (GE/INTC/BAC rows, 2026-08-17 ~21:40 EEST) against `data/reports/stocks/intraday/2026-08-17_18-32_stocks_intraday_report.md` §7 (same 3 symbols listed as "watchlist / not actionable").
- **suggested manual fix:** clarify (or add a display flag for) whether active-signals should surface the most recent tier verdict for a still-open signal_id when a fresher scan has since demoted the underlying setup, so the two views can't silently disagree.
- **priority:** medium
- **first observed:** 2026-08-17 21:40 EEST
