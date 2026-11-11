# Opus Enriched Review — pre-US-open decision review — Auto Cycle 15:58 EEST

## 1. Executive Summary
Slot: **pre-US-open decision review** (target 08:55 America/New_York / ~16:20 EEST equivalent this DST window; see §3 for actual-fire delta). Advisory only / no auto-trade. Pre-US schedule check: target 08:55 ET, actual fire ≈08:59 ET (Δ+4min, within tolerance — no DST-mismatch flag needed, 2026-08-13 is outside both documented drift windows). Crypto stays risk-off/chop: BTC downtrend (~$63.5K, externally confirmed down on the day, all trend timeframes negative this morning), ETH mixed, macro risk 100/100 on Ukraine-grain-terminal strikes + Strait-of-Hormuz tension + sticky CPI. **Zero A/B-tier crypto setups fired this cycle** (scalp/intraday/swing all clean-empty) — a genuine quiet book, not a broken one. Stocks regime is bullish pre-open (VIX 14.61, 4/4 indices uptrend, breadth 100%) but the US cash session is still closed, so every stock idea sits at C-tier by design (`market_closed_intraday_planning_only`) until RTH confirms it. This slot's new work: the **Stocks Pre-US Review Overlay** scored all 41 eligible session-cap-only candidates — 4 cleared **SUPPORT** (XLE, BX, XOM, COP — energy/AI-infra theme, RS-leader + fresh entity-resolved catalysts), 9 landed **CAUTION** (chase-risk, valuation-stretched, dilution, or negative-headline flags — incl. PANW and BX carrying "above fair value" caveats worth reading even on the SUPPORT side), 3 hit **INSUFFICIENT_DATA** on catalyst **entity-resolution false positives** (ARM matched an "adjustable-rate mortgage" article, not Arm Holdings; AXP matched an unrelated gold-mining company), rest NEUTRAL. The carried-forward **TUT/USDT invalidation-monitor integrity gap is still unresolved** — same DB row, same `updated_at`, now unchanged for 4 straight days — joined this cycle by the same stale-`triggered` signature on HEI/USDT, ZBT/USDT, and ACE/USDT. Catalyst-symbol mapping remains weak (26.7% mapped / 73.3% unmapped) — treat the catalyst layer as context only.

## 2. Data Used
- Reports: scalp (2026-08-13 13:18 EEST, fresh, ~2.7h old), intraday (13:26, fresh), swing (04:37, ~11.4h old — **carry-forward, borderline-stale band 4-12h**, flagged), stocks intraday (13:59, fresh; market still closed — planning only).
- Stocks swing/invest: excluded — deprecated/removed playbooks, last report 2026-07-02 (>6 weeks stale, per standing policy never resurrected).
- Catalyst layer: `data/catalysts/2026-08-13/` (latest `catalyst_cycle_10-31.md`, `catalyst_events.jsonl` — 2,000 cumulative rows today across 4 cycles, 534 mapped / 1,466 unmapped = 26.7% mapped).
- LLM packets: `llm_analysis_packet.md` (10:26 UTC gen), `llm_stocks_packet.md` (10:59 UTC gen).
- Scheduler: `data/scheduled_runs/2026-08-12_default_schedule/scheduler.log` + `cycle_06_13-08_summary.md`, both 14:20 EEST (~1h40min old — fresh, well under 3h defer threshold).
- CLI: `active-signals` ×2 (crypto 50 rows / stocks 50 rows), `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-08-13` (clean — 0 untracked crypto alerts today).
- New for this slot: `stocks-preus-candidates` → 41 eligible / 43 excluded (`reports/STOCKS_PREUS_REVIEW_CANDIDATES.md`); this review's own verdict JSON at `data/raw/enriched_review_sources/preus_review_2026-08-13T13-10-22Z.json`, ingested via `stocks-preus-review-ingest` (see §3 for completion status at time of writing — the ingest ran long; enforced/actual values are used wherever the command had returned by publish time, otherwise the requested values are marked as such).
- `reports/PAPER_MONITOR_STATUS_LATEST.md` (14:17 EEST, fresh) — lifecycle-aware operator counts.
- Direct read-only SQL against `db/crypto_ai_desk.sqlite`: `proposed_signals` status breakdowns (crypto/stocks), TUT/USDT + HEI/USDT + ZBT/USDT + ACE/USDT row history (all still-`triggered`, all `updated_at` unchanged from prior reviews), `news_items` freshness checks for all 41 stocks pre-US candidates + 10 non-promotable eligible names.
- External: WebSearch ×3 (BTC spot price/trend; PANW catalyst; BX AI-infra catalyst) + WebFetch ×1 (stockanalysis.com/PANW) — all corroborate internal data; PANW additionally surfaced a China regulatory-review risk not visible internally.

## 3. Scheduler / Data Freshness
- **Pre-US schedule check: target 08:55 ET, actual fire ≈08:59 ET (Δ+4min, within tolerance).** No DST-mismatch flag — today (2026-08-13) is outside both documented 2026 drift windows (2026-03-08→03-29 and 2026-10-25→11-01).
- Scheduler fresh: `scheduler.log` and `cycle_06_13-08_summary.md` both at 14:20 EEST (~1h40min old at review start). No defer triggered.
- Report freshness: scalp/intraday/stocks-intraday fresh (<3h); swing 04:37 (~11.4h old, 4-12h carry-forward band, near its upper edge — treat swing watchlist reads as directional only this cycle).
- Monitor status: `derivatives_monitor` and `fast_news_monitor` logs both updated within the last few minutes of review start (15:56-15:58 EEST) — active, not stalled. `pending_monitor` completed a fresh tick (checked=74, tp=2, stop=0) but logged `pending-monitor recycle failed: PermissionError: [WinError 5] Access is denied` — a repeating (1×/log, every recent cycle) non-fatal worker-recycle error; flagged in §14, not blocking.
- Paper/monitor: `PAPER_MONITOR_STATUS_LATEST.md` (14:17 EEST) — OPEN_ACTIVE 46, WAITING_FOR_ENTRY 1, REVIEW_ONLY_SHADOW 22, ENTERED_UNRESOLVED_EXPIRED 6, NO_ENTRY_EXPIRED 169, CLOSED 157W/11L/37flat, UNKNOWN_INCONSISTENT 3 (needs review).
- Live/execution: no live trading — system remains paper/read-model only per standing lock.
- **Overlay ingest — CONFIRMED COMPLETE.** `stocks-preus-review-ingest` finished after ≈20 min for 41 items (≈1 item every ~55s — see TODO-preus-ingest-latency in §14). Post-completion verification via direct read-only SQL: **all 41/41** of this review's signal_ids landed in `stocks_preus_review` with **zero discrepancies** between requested and server-enforced verdicts. Spot-checked the 4 SUPPORT candidates specifically: XLE (`sig_e313180c422521ec`, +5 → 86.1/A), BX (`sig_a94a72f9f24796b5`, +5 → 88.48/A), XOM (`sig_78fa7f92a928ae7d`, +5 → 100.0/A), COP (`sig_72cc83f396267541`, +5 → 100.0/A) — all enforced exactly as requested, all confirmed tier A, ready for the pre-open Paper lane pending RTH confirmation. §5/§7/§8 figures below are final, not provisional.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-08-13 15:58 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale", "derivatives_sparse"],
      "data_missing": ["swing report >4h (11.4h)", "on-chain whale flows", "order book depth/CVD"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log/cycle_06 14:20 EEST", "swing report 04:37 (~11.4h)", "PAPER_MONITOR_STATUS_LATEST.md 14:17 EEST"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.8,
      "reason_codes": ["risk_off", "chop", "mixed", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC downtrend, macro risk 100/100 risk-off", "altcoin breadth ~50% above EMA20", "stocks regime bullish, VIX 14.61, but session closed", "WebSearch: BTC ~$63.5K, daily/weekly/monthly trend all negative this morning"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "fresh_catalyst", "narrative_supported"],
      "data_missing": ["symbol resolver coverage for majority of events"],
      "suggested_effect": "advisory_only",
      "facts_used": ["534/2000 catalyst events mapped today (26.7%)", "momentum_breakout basket <1h fresh (ATM/BANK/HOME)", "2 catalyst-entity-resolution false positives found in stocks pre-US review (ARM, AXP)"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "data_unavailable", "oi_contradicts"],
      "data_missing": ["futures data for several C-tier crypto names"],
      "suggested_effect": "advisory_only",
      "facts_used": ["MMT/USDT 2 ATR extended, do-not-chase gate", "BANK/USDT price+OI: short covering, weaker continuation quality"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["entry_late", "chase_risk", "stale_before_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PANW premarket +2.84% already above entry_trigger — chase risk", "DXCM +52.5% in 3mo framing — overextension", "BANK/USDT pullback zone 0.0378-0.0384 not yet reclaimed"] },
    { "agent": "execution_lifecycle", "verdict": "manual_review", "confidence": 0.65,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review", "review_shadow"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PAPER_MONITOR_STATUS_LATEST.md: OPEN_ACTIVE 46 / WAITING 1 / REVIEW_SHADOW 22 / ENTERED_UNRESOLVED_EXPIRED 6 / UNKNOWN_INCONSISTENT 3", "TUT/USDT + HEI/USDT + ZBT/USDT + ACE/USDT all stale-triggered, updated_at unchanged for 4-7 days"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["headline_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["macro risk-off 100/100 (grain-terminal strikes, Hormuz, sticky CPI)", "PANW China regulatory review (external)", "4 stocks excluded LEGAL_RISK: HD, INTU, BLK, REGN", "TUT/USDT integrity gap now 4 days stale"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_working", "low_sample", "fresh_expired_problem"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto B-tier winrate 17.8% / PF 2.46 (touch-based, weekly)", "stocks C-tier winrate 2% / PF 0.27 (n=802) — never actionable by design", "stocks B-tier n=10 winrate 0%/PF 0.00 — low sample, weak confidence"] },
    { "agent": "head_trader", "verdict": "normal", "confidence": 0.6,
      "reason_codes": ["wait_for_trigger", "shorts_preferred", "longs_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["all 9 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "watch_only",
    "confidence": 0.6,
    "preferred_side": "catalyst_backed",
    "best_long_candidate":     { "symbol": "XOM", "trigger": "RTH confirmation above 159.76 entry zone; energy sector RS-leader + Mideast oil catalyst", "reason": "SUPPORT verdict: entity-resolved fresh catalyst, sector tailwind, RS leader, no hard cap" },
    "best_short_candidate":    { "symbol": "MMT/USDT", "trigger": "wait for 1h retest/pullback into structure before shorting — currently >2 ATR from EMA20, do-not-chase gate active", "reason": "weak-vs-market -14.77% 24h, but extended; needs cleaner entry" },
    "best_catalyst_candidate": { "symbol": "BX", "trigger": "RTH confirmation; Nvidia-led $500B AI-infra financing alliance, Blackstone named participant, +3.6% Aug 11", "reason": "entity-resolved, fresh, RS-leader — carries an 'above fair value' valuation caveat, size accordingly" },
    "avoid_candidate":         { "symbol": "TUT/USDT", "reason": "displayed 'triggered' status unreliable — unchanged row for 4 days, invalidation breach confirmed by a prior review and never resolved; do not use it to gauge open book risk" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 7
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.75 | scheduler_fresh, report_stale, derivatives_sparse | advisory_only |
| market_regime | caution | 0.80 | risk_off, chop, mixed, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, no_catalyst, fresh_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, data_unavailable, oi_contradicts | advisory_only |
| technical_entry | caution | 0.55 | entry_late, chase_risk, stale_before_entry | advisory_only |
| execution_lifecycle | manual_review | 0.65 | open_actionable, waiting_for_entry, needs_review, review_shadow | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.60 | playbook_working, low_sample, fresh_expired_problem | advisory_only |
| head_trader | normal | 0.60 | wait_for_trigger, shorts_preferred, longs_preferred | advisory_only |

## 4. What Changed vs Previous Review
Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-13_1139.md` (11:39 EEST, Europe/pre-US context slot).
- **New this cycle:** Stocks Pre-US Review Overlay ran for the first time this slot type — 41 candidates scored, 4 SUPPORT / 9 CAUTION / 3 INSUFFICIENT_DATA / 25 NEUTRAL (see §5, §7). Two catalyst entity-resolution false positives discovered (ARM ↔ mortgage-rate article, AXP ↔ unrelated gold-mining company) — new TODO.
- **Confirmed still-broken, worse:** TUT/USDT's flagged `triggered` row is unchanged for a 3rd consecutive review (same `updated_at`, 4 days stale now vs. the previous review's characterization). **New this cycle:** ZBT/USDT and ACE/USDT show the identical stale-`triggered` signature, `updated_at` unchanged since 2026-08-06/07 (6-7 days) — this broadens the confirmed pattern from 2 rows to 4.
- **Unchanged:** catalyst mapping still weak (26.7% mapped vs. 21.4% at 11:39 — a modest improvement but still far below the 50% flag threshold). Zero A/B crypto setups fired again this cycle (3rd consecutive review with a clean-empty crypto book).
- **Crypto watchlist:** BANK/USDT, MMT/USDT, COTI/USDT remain the same top watch names as the prior review — no material change in thesis.
- Untracked-alert detector: clean again (0 findings).

## 5. Catalyst Coverage
- Total catalyst events today (cumulative, 4 cycles): **2,000**. Mapped (non-null symbol): **534 (26.7%)**. Unmapped: **1,466 (73.3%)**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Narrative baskets today: 5 (`rwa_narrative`, `perps_dex_narrative`, `ai_narrative`, `binance_ecosystem_teaser`, `momentum_breakout`).
- Top 3 unmapped headlines (all noise, not tradeable — RBA commentary via `t.me/marketfeed`):
  1. "RBA'S KENT: TAX CHANGES IN FEDERAL BUDGET LIKELY CURBED DEMAND IN ESTABLISHED HOUSING MARKET..."
  2. "RBA'S KENT: SIGNIFICANT INVESTMENT IN DATA CENTRES AND AI INFRASTRUCTURE SUPPORTS AGGREGATE DEMAND GROWTH..."
  3. "RBA SAYS HOUSING CONDITIONS HAVE SOFTENED NOTICEABLY AS TAX CHANGES AND HIGHER BORROWING COSTS WEIGH ON DEMAND..."

### Pre-US Stocks Review Overlay
- Candidates reviewed: **41** (SUPPORT 4 / NEUTRAL 25 / CAUTION 9 / BLOCK 0 / INSUFFICIENT_DATA 3, across 41 signal-id records covering 38 unique symbol/direction pairs)
- Session-cap-only C's now eligible for pre-open Paper lane (SUPPORT, pending code-enforced clamp confirmation): **XLE (long), BX (long), XOM (long), COP (long)**
- Excluded by hard gate: **43** — 28× `EARNINGS_BLACKOUT` (incl. AAPL, NVDA, META, BAC, GS×2, WMT, LLY, CSCO, DELL, LMT — see §14 for an LMT-specific data-consistency note), 11× `NO_ENTITY_RESOLVED_CATALYST` (mostly sector ETFs: XLC/XLY/XLU/XLI/XLF/IWM/QQQ/XLV/XLK + AFRM×2 + ETN), 4× `LEGAL_RISK` (HD, INTU, BLK, REGN)

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **risk-off / chop** — BTC downtrend (all timeframes negative today, externally confirmed ~$63.5K), ETH transition_up intraday but downtrend on swing, altcoin breadth ~47-50% above EMA20 (neutral, not broad participation). Macro risk 100/100 (Ukraine strikes on Russian grain terminals, Iran/Strait-of-Hormuz standoff, sticky-CPI-vs-weak-BTC divergence).
- Stocks mood: **bullish (pre-market planning) / closed** — VIX 14.61 (low, risk-on), all 4 major indices in uptrend, breadth 100% above EMA20/50. This is a *planning* read only — US cash session has not opened; every stock idea is capped C by design until RTH confirms.
- Dominant narrative: crypto — perps/DEX (HYPE + DYDX/GMX/ASTER), AI-rotation (NEAR/RENDER/TAO/FET), pure-momentum cluster (ATM/BANK/HOME, no confirmed news). Stocks — AI-infrastructure financing (Nvidia's $500B third-party capital mobilization naming Blackstone; energy sector strength on Mideast-driven oil prices).
- Preferred side now: **catalyst-backed longs in stocks-at-open (energy + AI-infra theme) / wait-for-trigger in crypto** — crypto has no clean directional edge this cycle; the risk-off macro backdrop favors caution on fresh alt longs.
- Best long candidate: **XOM** (stocks, RTH-confirmation required) — energy sector RS-leader, fresh entity-resolved Mideast-oil catalyst, no hard cap. Crypto: none clean — BANK/USDT is the best long-watch (see §8).
- Best short candidate: **none clean crypto** — MMT/USDT is the best short-watch, but is currently >2 ATR extended and gated do-not-chase; wait for 1h retest.
- Best catalyst-backed candidate: **BX** (Nvidia-led AI-infra financing alliance, entity-resolved and fresh) — carries an "above fair value" valuation caveat from independent coverage, size and confirm accordingly.
- What to avoid: chasing PANW/DXCM at the open (both already extended/overbought going into the print, see §7); treating TUT/USDT's, HEI/USDT's, ZBT/USDT's, or ACE/USDT's "triggered" status as valid open risk; any stocks entry before RTH confirmation regardless of pre-US overlay verdict.
- What would change the view: a BTC reclaim of local resistance with OI confirmation would flip crypto risk routing toward longs; a clean SPY/QQQ open above pre-market levels with sector confirmation would strengthen the stocks-long thesis; resolution (open/close) of the Strait-of-Hormuz standoff would materially cut the macro risk-off score.

## 7. Candidate Deep Dives (≤5)

### 1. XOM — SUPPORT (stocks, energy, long, RTH-confirmation required)
- Pre-gate tier A (score 100.0), demoted to C solely by `market_closed_intraday_planning_only` (session-cap, not substantive) — eligible for promotion per the pre-US overlay.
- RS component 16.54 (top-decile, "leader" classification); sector (energy/XLE) independently confirmed **strong** in the stocks report (RS vs SPY 20d +5.68%, 20d return +8.02%).
- Catalyst: "ExxonMobil (XOM) Stock Could Be A Bargain On Cash Flow Despite Rich Earnings" + broader sector coverage "The Middle East Crisis Has Rewired The Oil Market" (entity-resolved, fresh, 2026-08-13). Consistent with today's macro risk read (Strait of Hormuz tension driving oil).
- Entry plan (from proposed_signals): entry_trigger 159.76, stop 158.80. **Not actionable pre-open** — wait for RTH confirmation and re-check the level hasn't already gapped away.
- Legal/headline check: none found. Earnings: not in blackout window (excluded list has no XOM entry). What would invalidate: oil reversing / Hormuz de-escalation headline, or a gap-and-fade open below the entry zone.

### 2. COP — SUPPORT (stocks, energy, long, RTH-confirmation required)
- Same theme as XOM: pre-gate A (score 100.0), RS leader (16.54), energy sector strong, fresh entity-resolved catalyst ("ConocoPhillips starts production at Coyote 3SX on Alaska's North Slope" + sector oil-price tailwind).
- Entry: 127.33 / stop 126.54. Not actionable pre-open. Correlated with XOM — treat as one sector bet, not two independent ones, for position sizing purposes (this review makes no sizing recommendation itself).

### 3. BX — SUPPORT (stocks, financials/AI-infra, long, RTH-confirmation required), with a valuation caveat
- Pre-gate A (score 83.48), RS leader (16.54). Catalyst externally verified via WebSearch: Nvidia unveiled a financing effort to mobilize $500B+ third-party capital for AI compute infrastructure; Blackstone named as a participating firm; BX +3.6% on 2026-08-11 on the news. Entity-resolved, fresh, primary-source-adjacent (multiple independent outlets).
- **Caveat — flag, not a block:** internal coverage also carries "Blackstone (BX) Stock Could Be 26% Above Fair Value As AI Data Center Bets Grow" (2026-08-13). Genuine fresh catalyst + RS leadership support the SUPPORT verdict, but the stretched-valuation framing means this is a "confirm strength, don't chase into euphoria" long, not a blank check.
- Entry: 146.45 / stop 144.77. Not actionable pre-open.

### 4. PANW — CAUTION (stocks, cybersecurity, long) — real catalyst, but chase-risk + regulatory flag
- Pre-gate A (score 99.26), RS leader (16.54). Catalyst confirmed via WebSearch + WebFetch (stockanalysis.com): AI-security demand narrative, Black Hat conference tailwind for the sector, stock up 114% YTD.
- **Chase risk:** pre-market quote $398.00 (+2.84%) already well above the proposed entry_trigger of $387.10 — if this holds into the open, the planned entry zone is stale before RTH even starts.
- **Regulatory risk (new, external-only — not visible in internal data):** China initiated a cybersecurity review of PANW's products citing national-security concerns. This is exactly the kind of legal/headline risk the base routine requires flagging on every stock A/B even after a clean internal gate.
- **Valuation:** consensus 12-month PT ($345, per one source) sits *below* the current price — an outlier bull case (Citizens, $415 PT) is doing the heavy lifting. Overall: real catalyst, but three independent reasons to wait for confirmation rather than chase the open.

### 5. TUT/USDT — needs review (crypto, NOT a trade candidate) — carried-forward, now widened
- `proposed_signals` row `sig_e4875989af64bab7` (entry 0.14284, invalidation 0.09882) has `updated_at = 2026-08-09T17:01:44+00:00` — **byte-for-byte unchanged** from the 11:39 EEST review, itself unchanged from the review before that. This is the 3rd consecutive review confirming zero state change on this exact row, and the underlying invalidation breach was independently price-verified two reviews ago and never resolved.
- **New this cycle:** the same signature (stale `triggered` status, `updated_at` frozen for multiple days) now confirmed on three more rows via direct SQL: HEI/USDT (`sig_a4e763ceaf1df917`, unchanged since 2026-08-08T05:43:12), ZBT/USDT (`sig_0be20040e229aec5`, unchanged since 2026-08-07T03:00:17), ACE/USDT (`sig_9d70822c7254b39f`, unchanged since 2026-08-07T03:00:17). None of these four rows were independently re-verified against live price this cycle (no allowed live-price CLI in this slot's tool contract) — flagging the pattern, not re-confirming each breach.
- Do not treat any of TUT/USDT, HEI/USDT, ZBT/USDT, or ACE/USDT's displayed "triggered" status as current open risk. System-integrity item, escalated in §14.

## 8. Best Candidates Ranked
1. **XOM (stocks, long)** — SUPPORT, RTH-confirmation required. Best clean long this cycle.
2. **COP (stocks, long)** — SUPPORT, RTH-confirmation required. Same-sector correlated bet with XOM.
3. **BX (stocks, long)** — SUPPORT with a valuation caveat, RTH-confirmation required. Best catalyst-backed idea.
4. **Long-watch (crypto): BANK/USDT** — trigger: reclaim + hold of the 0.0378-0.0384 pullback zone on 1h close, invalidation 1h close below 0.0371. Currently watchlist-only (score 63.5, no fresh verified catalyst beyond a pure-momentum tag).
5. **Short-watch (crypto): MMT/USDT** — trigger: wait for a 1h retest/pullback into prior structure; currently >2 ATR from EMA20 (do-not-chase gate active). Weak-vs-market -14.77% 24h.
6. **Catalyst-watch (crypto): COTI/USDT** — trigger: derivatives/anchor-exchange confirmation (currently MEXC-adjacent with no derivatives confirmation); +15-25% 24h RS leader, catalyst-tagged.
7. **Avoid-into-open: PANW, DXCM** — both real-momentum names but already extended/chase-risk going into RTH (see §7, §9).

## 9. Avoid / No Trade
This applies to the **current decision window only** — never a system-stop.
- **Chasing PANW or DXCM at/near the open** — both show genuine momentum but are already extended (PANW premarket +2.84% above entry_trigger; DXCM +52.5% in 3 months per internal coverage) — wait for a retest, not a breakout chase.
- **Treating TUT/USDT, HEI/USDT, ZBT/USDT, or ACE/USDT's `triggered` status as valid open risk** — confirmed stale for 4-7 days across all four rows; system-integrity item, not tradeable information.
- **Any stocks entry before RTH confirmation**, regardless of this cycle's pre-US overlay verdict (SUPPORT is a scoring input, not a green light to trade the pre-market print).
- **INTC long** — CEO's personal $12M buy-in to the capital raise is a genuine bullish signal, but it's also confirmation of an active dilution/offering event already flagged internally as a risk warning; treat with caution, not conviction, until the raise terms are digested by the market.
- **New alt longs into the current risk-off macro backdrop** without a specific RS-leader + catalyst combination (per Market Mood routing above).

## 10. Main Risks
- **Invalidation-monitoring integrity gap, now confirmed on 4 rows, unresolved for 3+ consecutive reviews** — undermines confidence in every "N open positions" read this system produces (see §7, §14).
- **Catalyst-symbol entity resolution has confirmed false positives** — ARM (Arm Holdings ticker) matched a completely unrelated "adjustable-rate mortgage" article; AXP (American Express ticker) matched an unrelated gold-mining company press release. If this generalizes beyond the two caught this cycle, some fraction of "catalyst-backed" tags across the whole system may be spurious (see §14).
- **Macro risk-off backdrop (100/100)** on live geopolitical events (Ukraine grain-terminal strikes, Strait of Hormuz standoff) — reduces conviction on any fresh crypto alt long regardless of individual setup quality.
- **PANW China regulatory review** — external-only finding, not visible in internal data; a reminder that internal-first sourcing can miss fresh single-name regulatory catalysts on stocks the system already scores highly.
- **Swing report is 11.4h old**, near the top of the carry-forward band — crypto swing watchlist reads (BANK/MMT/COTI) should be treated as directional, not precise, until the next swing cycle refreshes.
- **Catalyst mapping stuck at ~27% mapped** — the catalyst layer materially undercounts true coverage; do not use "no catalyst found" as proof of absence.

## 11. Action Plan — next 4 hours
1. At/after the US cash open (09:30 ET): re-check XOM, COP, BX entry zones against the actual print — if price has already gapped through the entry zone, treat as stale-before-entry, not a chase target.
2. Watch PANW and DXCM for a retest/pullback rather than an open-print chase; re-evaluate SUPPORT-adjacent names only after the first 15-30 minutes of RTH confirm direction.
3. Crypto: watch BANK/USDT for a reclaim of 0.0378-0.0384 (long-watch) and MMT/USDT for a 1h retest (short-watch); no action until either triggers.
4. No manual code/data intervention this cycle (advisory-only) — all findings routed to §14 for a human-driven follow-up session.
5. Confirm the `stocks-preus-review-ingest` run (started 13:11 UTC, still in progress at review publish time — see §3) completed cleanly and applied the enforced/clamped adjustments; re-run diagnostics if not.

## 12. Final Verdict per Mode
- **Crypto scalp**: disabled by kill-switch (mode off, any hour/day) — no ideas possible regardless of setup quality.
- **Crypto intraday**: zero A/B this cycle. Market regime range/chop, no clean directional edge. Wait for trigger.
- **Crypto swing**: strongest lane by weekly stats (14d WR 72%/PF 5.80, touch-based — known to overstate realized edge, read directionally). Zero A/B this cycle. BANK/MMT/COTI top the watchlist, unchanged thesis from the prior review.
- **Stocks intraday**: market closed — all ideas planning-only by design. Pre-US overlay promotes XOM/COP/BX to a **watch-for-RTH-confirmation** status (not yet actionable); PANW/DXCM/SMH/ISRG/CRWD/SBUX/INTC/ORCL/DDOG carry explicit caution flags; do not treat any as clean until RTH confirms.
- **Stocks swing/invest**: deprecated/removed, not reviewed.
- **System integrity**: **manual review required** — TUT/USDT invalidation-monitoring gap confirmed unchanged for a 3rd consecutive review and now widened to 4 rows (TUT, HEI, ZBT, ACE); catalyst mapping still weak (26.7% mapped); two catalyst entity-resolution false positives newly confirmed this cycle; untracked-alert detector clean (0 findings) today.

## 13. Sources
- [FinancialContent — Palo Alto Networks (PANW) Stock Is Up, What You Need To Know](https://markets.financialcontent.com/stocks/article/stockstory-2026-8-10-palo-alto-networks-panw-stock-is-up-what-you-need-to-know) (2026-08-10)
- [stockanalysis.com — Palo Alto Networks (PANW) Stock Price & Overview](https://stockanalysis.com/stocks/panw/) (fetched 2026-08-13, premarket $398.00 +2.84%)
- [gurufocus.com — Blackstone (BX) Partners with Apollo on $35B AI Platform Initiative](https://www.gurufocus.com/news/8907798/blackstone-bx-partners-with-apollo-on-35b-ai-platform-initiative)
- [Simply Wall St News — Blackstone (BX) Deepens Ties With NVIDIA On AI Infrastructure Financing Platforms](https://simplywall.st/stocks/us/diversified-financials/nyse-bx/blackstone/news/blackstone-bx-deepens-ties-with-nvidia-on-ai-infrastructure)
- [Yahoo Finance — Bitcoin and ethereum prices today, Thursday, August 13, 2026: BTC price trends turn negative](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-thursday-august-13-2026-btc-price-trends-turn-negative-124406250.html)
- Internal: `data/reports/scalp/2026-08-13_10-18_scalp_report.md`, `data/reports/intraday/2026-08-13_10-26_intraday_report.md`, `data/reports/swing/2026-08-13_01-37_swing_report.md`, `data/reports/stocks/intraday/2026-08-13_10-59_stocks_intraday_report.md`, `data/catalysts/2026-08-13/catalyst_cycle_10-31.md`, `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md`, `reports/PAPER_MONITOR_STATUS_LATEST.md`.

## 14. Fix Requests / TODO

### TODO-invalidation-monitor-gap (carried forward, now widened — HIGH)
- **issue:** `proposed_signals` rows can remain `status='triggered'` after price has breached (or simply aged well past) their own invalidation/validity window, with no automatic transition to `stopped`/`expired`. TUT/USDT confirmed unchanged for a 3rd consecutive review (row `sig_e4875989af64bab7`, `updated_at` frozen at 2026-08-09T17:01:44, invalidation breach independently price-verified 2 reviews ago). This cycle additionally confirms the identical stale-`updated_at` signature on HEI/USDT (`sig_a4e763ceaf1df917`, frozen since 2026-08-08T05:43:12), ZBT/USDT (`sig_0be20040e229aec5`, frozen since 2026-08-07T03:00:17), and ACE/USDT (`sig_9d70822c7254b39f`, frozen since 2026-08-07T03:00:17) — none independently price-re-verified this cycle (no live-price CLI in this slot's allowed-tools contract), flagging the pattern only.
- **evidence:** direct SQL against `db/crypto_ai_desk.sqlite` → `proposed_signals` for the four signal_ids above, all `status='triggered'`, all `updated_at` unchanged across 2-3 consecutive automated review cycles.
- **suggested manual fix:** a human-driven session should (1) re-verify current price vs. invalidation for all four rows, (2) audit whether the invalidation-monitor process runs on the expected cadence for `triggered`-status rows specifically (vs. `waiting_for_entry`, which does appear to update), (3) consider whether this is the same root cause as `[[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]]` or a distinct one, (4) given the pattern has now widened from 1→4 rows across 3 reviews, treat as a systemic gap, not four isolated incidents.
- **priority:** high
- **first observed (this pattern, this row set):** 2026-08-13 15:58 EEST (TUT/USDT itself first flagged earlier — see prior reviews)

### TODO-catalyst-mapping-coverage (carried forward — MEDIUM)
- **issue:** catalyst-symbol mapping remains stuck at ~21-27% mapped across the last several review cycles, well below the 50% usability threshold.
- **evidence:** `data/catalysts/2026-08-13/catalyst_events.jsonl` — 534/2000 mapped (26.7%) this cycle; 11:39 EEST review recorded 21.4% mapped.
- **suggested manual fix:** audit the symbol resolver's coverage against the actual `news_items.source` mix (Telegram macro/FX channels like `t.me/marketfeed` appear to dominate the unmapped tail with non-tradeable macro commentary — consider a source-level pre-filter rather than trying to entity-resolve every row).
- **priority:** medium
- **first observed:** carried forward, most recently 2026-08-13 11:39 EEST

### TODO-catalyst-entity-resolution-false-positives (NEW — MEDIUM)
- **issue:** during the Stocks Pre-US Review Overlay, two of 41 candidates had their only "fresh" internal catalyst hit turn out to be an entity-resolution false positive: ARM (ticker for Arm Holdings) matched a Yahoo Finance mortgage-rates article using "ARM" as an acronym for adjustable-rate mortgage; AXP (ticker for American Express) matched a press release headlined "Amex Gold Mining Files Project Notice for the Perron Gold Mine" — an unrelated company whose name happens to contain "Amex."
- **evidence:** `news_items` rows matched via `detected_symbols_json LIKE '%"ARM"%'` and `%"AXP"%'` on 2026-08-13; both top-ranked "fresh" hits are semantically unrelated to the actual ticker's company.
- **suggested manual fix:** tighten the symbol/entity resolver to require a company-name or ticker-context match (not just a bare acronym/substring match) for ambiguous 2-4 letter tickers that collide with common English terms (ARM, AXP-as-"Amex", and likely others e.g. ALL, ARE, FAST, KEY, NOW). Consider a denylist of known-ambiguous acronym collisions as a quick mitigation.
- **priority:** medium
- **first observed:** 2026-08-13 15:58 EEST (pre-US overlay review)

### TODO-news-catalyst-score-saturation (NEW — MEDIUM)
- **issue:** the `news_catalyst` scoring component was exactly `11.0` for all 28 promotable Stocks Pre-US candidates inspected this cycle, regardless of whether the underlying catalyst was genuinely material (e.g., BX's Nvidia-led $500B AI-infra alliance) or a content-free "X vs Y, which stock is the better buy" comparison article (e.g., ADBE, TSM, PEP). This looks like a saturated/capped component rather than one that discriminates on catalyst quality.
- **evidence:** `data/processed/agent_outputs/20260813_105817_stocks_stock_scoring.json` — `components.news_catalyst` = 11.0 for all 28 symbols checked (ASML, ARM, TXN, CMCSA, ADBE, VRT, MS, KLAC, AXP, INTC, TSM, XLE, ISRG, SMH, BX, PEP, BKNG, CRWD, JPM, ANET, DXCM, BIIB, SBUX, PANW, ABNB, XOM, COP, ORCL).
- **suggested manual fix:** a human-driven session should check `src/signals/sizing.py` / the scoring component logic for whether `news_catalyst` has a "has ≥1 catalyst → flat max score" path instead of scaling with catalyst count/recency/materiality, and whether that's intended behavior or a regression.
- **priority:** medium
- **first observed:** 2026-08-13 15:58 EEST

### TODO-pending-monitor-recycle-permission-error (NEW — LOW)
- **issue:** `pending_monitor` logs show a recurring `pending-monitor recycle failed: PermissionError: [WinError 5] Access is denied` on worker-memory rotation, once per recent log file checked.
- **evidence:** `data/scheduled_runs/2026-08-12_default_schedule/pending_monitor_1786615765.log` and `pending_monitor_1786604797.log`, both showing exactly 1 occurrence of the error string.
- **suggested manual fix:** investigate the file/handle the recycle step tries to release on Windows (likely an OS-level file lock held by another thread) — non-fatal today (monitor continues ticking normally after the error) but worth checking it isn't slowly leaking worker memory across long-running sessions.
- **priority:** low
- **first observed:** 2026-08-13 15:58 EEST

### TODO-preus-ingest-latency (NEW — LOW)
- **issue:** `stocks-preus-review-ingest` took ≈55 seconds per candidate (≈20 min total for 41 items) instead of completing near-instantly for what is documented as pure local DB read/write logic. Completed successfully with zero discrepancies (verified 41/41 post-completion), so this is a performance issue, not a correctness one.
- **evidence:** background task `bc4mfzfv4` started 2026-08-13 13:11 UTC, completed 2026-08-13 ~13:31 UTC (41/41 rows landed in `stocks_preus_review`, exact match to this review's `preus_review_2026-08-13T13-10-22Z.json` signal_ids and requested verdicts).
- **suggested manual fix:** profile `record_verdict`'s per-item `refresh_actionability` + `repair_bug_expired_actionable_plans` calls (`src/execution/stocks_preus_review.py`) — likely candidates are a non-indexed full-table scan or redundant recomputation across all signals on every single-item call instead of a batched pass at the end of the ingest loop.
- **priority:** low
- **first observed:** 2026-08-13 15:58 EEST

### TODO-lmt-earnings-blackout-inconsistency (NEW — LOW)
- **issue:** LMT was excluded from the Stocks Pre-US Review Overlay's eligible list via `EARNINGS_BLACKOUT`, but the same day's `stock_trade_idea` agent output for LMT shows `next_earnings_date: 2026-10-20` (`days_ahead: 68`) — 68 days out, well outside any reasonable blackout window.
- **evidence:** `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md` (LMT excluded, reason `EARNINGS_BLACKOUT`) vs. `data/processed/agent_outputs/20260813_105826_stocks_stock_trade_idea.json` (LMT `earnings.next_earnings_date = 2026-10-20`, `days_ahead = 68`).
- **suggested manual fix:** reconcile which earnings-date source the pre-US eligibility gate consults vs. the one the RS/trade-idea agent uses — they may be reading different calendars, or the pre-US gate may be using a stale/different lookup for LMT specifically.
- **priority:** low
- **first observed:** 2026-08-13 15:58 EEST
