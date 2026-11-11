# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:39 EEST

## 1. Executive Summary

Slot: **crypto overnight / Asia review** (04:30 EEST target, written 04:39). **Advisory only — no auto-trade.** US cash markets are closed at this hour; crypto is the only live-actionable class, stocks are planning/watchlist only. **Top story**: the Iran–US conflict flagged as a macro risk-off headline all week is **externally confirmed as a genuine, active escalation** — the US struck Iranian missile launchers on Larak Island in the Strait of Hormuz (2026-08-30), and Iran's IRGC retaliated with strikes on two US bases in Jordan (early 2026-08-31); nearly all incoming fire was intercepted, no major damage reported ([Washington Post](https://www.washingtonpost.com/national-security/2026/08/30/us-strikes-iran-missile-sites-larak-island/), [CNN](https://edition.cnn.com/2026/08/30/politics/us-iran-strikes-larak-island)). The desk's own macro score is pinned at its ceiling (100/100 risk-off) — but external context shows crypto has grown **desensitized** to this recurring saga over the past month (BTC "barely moved" on the last comparable Hormuz headline), so this reads as **background risk, not a fresh acute shock**; treat as elevated-but-familiar, not a reason to go flat. Confirming that read, the desk's own swing-timeframe regime is still **uptrend** (BTC/ETH, breadth 47.6%/71.4% above EMA20/50) even as the short-timeframe intraday regime has cooled to **range/chop** (breadth 42.9%/61.9%) — a normal digestion pattern, not a reversal. **No new A/B-tier ideas fired this cycle** in either intraday or swing; all 50 active crypto positions are long, carried from prior cycles. The most consequential **new** finding this cycle: three existing open longs — **ONG/USDT, PUMP/USDT, POL/USDT** — now directly contradict the desk's own fresh momentum/RS scan, which tags all three "weak_vs_market / breakdown" with double-digit negative 24h moves; ONG/USDT is the sharpest case (-17.3% intraday / -12.7% swing, active swing long still open, score 73.9). On the catalyst side, the `ai_narrative` basket (TAO/RENDER/FET/NEAR, fresh <1h) and the catalyst-confirmed `momentum_breakout` basket (UNI/USDT) remain the desk's best catalyst-linked setups. On stocks (planning-only, market closed): **INTU** carries a genuine, externally-confirmed securities-fraud class action (Baldwin v. Intuit, N.D. Cal., filing deadline 2026-09-08) despite a 98.3 raw A-tier score — correctly capped to C/avoid by the desk's own legal-risk gate. Two housekeeping items carried from the last review: the lifecycle-status backlog that spiked to 494 rows at 23:32 has **reverted to 253** (back near its ~252 baseline) after the 03:33 lifecycle-review step ran; the untracked-legacy-alert bug (already HIGH priority per prior sessions) is **confirmed still active**, with three fresh instances (ZKC/AUCTION/ZK, sent 21:24 EEST yesterday) on top of the still-unresolved DEXE case (~40h old).

## 2. Data Used

- Reports: `data/reports/intraday/2026-08-30_23-39_intraday_report.md` (data freshness 2026-08-30 23:30 UTC = 02:30 EEST, **fresh**, ~2h old); `data/reports/swing/2026-08-30_21-16_swing_report.md` (data freshness 2026-08-30 21:00 UTC = 00:00 EEST, **carry-forward** band, ~4h39m old); `data/reports/scalp/2026-08-30_13-18_scalp_report.md` not read in depth — scalp mode's own stats this cycle confirm it remains structurally unprofitable (see §6/§14), consistent with its "disabled by design" status noted in prior reviews.
- Stocks: `data/reports/stocks/intraday/2026-08-31_00-24_stocks_intraday_report.md` (00:23 UTC, ~4h16m old, borderline carry-forward — irrelevant to actionability since **US cash session is closed**; all raw A-tier ideas are gate-demoted to C for `market_closed_intraday_planning_only`). Stocks swing/invest reports are from 2026-07-02 — long-stale, expected: that pipeline is deprecated per `[[project_crypto_ai_desk_stocks_position_framework]]`, informational only.
- Catalysts: today's folder (`data/catalysts/2026-08-31/`) was missing at run start; regenerated via the allowed `catalyst-scan --no-print` CLI (445 events scanned, 4 baskets, `catalyst_cycle_01-43.md`). Cross-referenced against the fresher `data/catalysts/2026-08-30/` cycle embedded in the two reports above (1045 events, 6 baskets) for narrative-basket continuity.
- LLM packet: `data/processed/llm_analysis_packet.md` not separately re-read this cycle (report content already supersedes it for this window).
- CLI: `active-signals --asset-class crypto` (50 rows: 41 triggered, 8 tp1/tp2-hit, 1 waiting_for_entry — **all long, 0 shorts**); `active-signals --asset-class stocks` (50 rows: 31 waiting_for_entry [C-tier, market-closed planning], 15 tp1_hit, 4 tp2_hit); `signal-stats --asset-class crypto` (tier B n=290, PF 1.079; by mode: swing PF 1.40 best, intraday PF 1.10, **scalp PF 0.125 — badly losing**; Binance-only confirmation PF 1.87 vs cross-exchange PF 0.64); `signal-stats --asset-class stocks` (intraday n=607 PF 1.60 lifetime; C-tier winrate 8%/PF 0.40 — expected, C-tier never actionable); `detect_untracked_legacy_alerts --since 2026-08-31` (0 rows — but see §14, the calendar-day cutoff masks same-evening alerts, confirmed by a wider `--since 2026-08-28` check showing 8 rows).
- Direct read-only SQL (`proposed_signals`, allowed table): lifecycle-status sweep (`expires_at < now() AND status IN open-states`) → **253 rows** (crypto B=37, stocks A=3/B=16/C=197) — down from 494 at the 23:32 review, back near the long-running ~252 baseline.
- External: 3 WebSearch (Iran/Hormuz strikes verification; crypto market reaction to the Hormuz saga; INTU securities-fraud class action verification) — see §13. No WebFetch needed; WebSearch results included full corroborating detail from primary/reputable outlets.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-30_2332.md` (post-close final daily review, 23:32 EEST).

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: 2026-08-31 03:45 EEST (~54min old at run start) — fresh, well within the 3h defer threshold.
- Latest cycle summary: `cycle_02_02-28_summary.md` (03:45 EEST) — fresh, cycle completed cleanly: `CYCLE 2 END ok=76 failed=4 telegram=sent`. The 4 failures were non-fatal (one `CMD TIMEOUT: refresh obsidian dashboard`, logged and continued).
- All monitors confirmed still running at end-of-cycle: crypto (pid 28804, ~90min lifetime), pending, mexc-canary, crypto-invest-forward, derivatives, fast-news, stocks monitors — all "still running," no restarts flagged.
- **Lifecycle-status backlog (positive update)**: the 23:32 review flagged a spike to 494 rows (`expires_at < now()` while status still reads open) — up from a long-running ~252 baseline. Re-run now shows **253 rows**, essentially back to baseline. The `open intraday lifecycle review` step (03:33:09–03:34:22, 72.9s) and `track-signals (post)` step (03:34:23–03:35:42, 79.1s) both ran this cycle and appear to have cleared the backlog. Reads as a temporary processing lag, not a permanent regression — but see §14 for a suggested tighter-cadence fix.
- **Untracked-legacy-alert bug — confirmed still active, not resolved.** The mandated `--since 2026-08-31` (today) check returns 0 rows, but this is a **methodology artifact**: it only catches alerts sent after local midnight. Widening to `--since 2026-08-28` surfaces **8** untracked rows, including **3 fresh ones from yesterday evening**: ZKC/USDT (swing, sent 2026-08-30T21:24:42Z), AUCTION/USDT (swing, 21:24:43Z), ZK/USDT (swing, 21:24:47Z) — all ~7.4h old at write time, all past the detector's own 6h window, all still without a backing `proposed_signal`. DEXE/USDT (swing, sent 2026-08-29T14:36:42Z) remains unresolved at ~38h old. This is the same bug flagged HIGH priority in `[[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]]` (raised 2026-07-17) — now with fresh evidence it is still live 6 weeks later. Notably, **AUCTION/USDT and ZK/USDT are both currently open active long positions** — the untracked alert likely means a watchlist re-fire on an already-tracked symbol failed to reconcile against the existing signal_id, not that the position itself is unmanaged. **ZKC/USDT is not currently an open position at all** despite the untracked alert — see §4 (missed-winner note).
- Catalyst scan: regenerated fresh this cycle (`catalyst_cycle_01-43.md`, 445 events / 4 baskets, 2026-08-31). Mapping coverage is **weak this run**: 192/445 mapped (43.1%), 253/445 unmapped (**56.9%**) — driven almost entirely by unmapped geopolitical wire copy (Iran/Hormuz headlines) and unrelated general-news items. **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Top 3 unmapped headlines: "Iran's IRGC says it launched attack on two US bases in Jordan – Reuters"; "Oil jumps more than 1% after US attack on Iran's Larak island – Reuters"; "LG ELECTRONICS UNVEILS THE NEXT EVOLUTION OF AI HOME AT IFA 2026" (correctly unrelated to any tracked symbol).
- Monitor/paper Windows Task Scheduler state not separately queried — outside the allowed read-only CLI list this run.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-08-31 04:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["Windows Task Scheduler live state", "root cause of the swing-report date-rollover cosmetic bug"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log + cycle summary both ~54min old, cycle ok=76 failed=4 (non-fatal) telegram=sent", "intraday report fresh (~2h old), swing report carry-forward (~4h39m old)", "today's catalyst folder was missing and was regenerated via the allowed catalyst-scan CLI", "lifecycle-status backlog reverted from 494 to 253 rows, back near ~252 baseline"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mixed", "risk_off", "longs_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["intraday: BTC/ETH range/chop, breadth 42.9%/61.9% above EMA20/50", "swing: BTC/ETH uptrend, breadth 47.6%/71.4% above EMA20/50 — longer-term trend intact", "macro/geopolitics risk pinned at 100/100 (Iran/Hormuz) both reports", "externally confirmed active US-Iran escalation (Larak Island strikes + Jordan retaliation) but crypto historically desensitized to this recurring headline pattern per external search"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "catalyst_confirmed", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 56.9% unmapped this run, driven by geopolitical wire copy", "ai_narrative basket fresh <1h: TAO/RENDER/FET/NEAR — desk holds active TAO/FET longs, alignment confirmed", "momentum_breakout basket fresh <1h: UNI/USDT explicitly catalyst-confirmed (do not chase, wait_pullback); HEMI/AUCTION in same basket flagged as NOT catalyst-confirmed (pure momentum)", "Coldcard hardware-wallet exploit (~2055 BTC) offset by continued 9-day BTC/ETH ETF net-inflow streak — muted net catalyst", "Cronos $75M hack attempt mapped to BNB/USDT — same mapping pattern flagged in prior reviews"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["oi_supports", "oi_contradicts", "funding_extreme", "data_unavailable"],
      "data_missing": ["derivatives data for POL/USDT and BMT/USDT (not in the top-8 derivatives table this cycle)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNI/AUCTION/TNSR/ERA/ZK: price up + OI up, fresh positioning confirms trend, crowding normal", "ONG/USDT: price down + OI down = deleveraging/long liquidation; funding negative across bybit+mexc, crowding elevated per cross-check", "HEMI/USDT: price up + OI down = short covering, weaker continuation quality"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["overextended", "chase_risk", "price_moved_away", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["No A/B setups cleared the desk threshold this cycle in intraday or swing", "UNI/HEMI/AUCTION/TNSR/ZK all rejected this cycle for being >2 ATR from EMA20 — do not chase", "ZKC/USDT rallied to +65.2% 24h (top strongest symbol) without the tracked watchlist thesis (0.0600-0.0634 pullback zone) ever being hit — the parabolic move skipped the pullback entirely"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.65,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 41 triggered + 8 tp1/tp2-hit = 49 open actionable, 1 waiting_for_entry, 0 shorts, all 50 rows long", "stocks: 31 waiting_for_entry (C-tier, market-closed planning only), 15 tp1_hit + 4 tp2_hit open", "3 active longs (ONG/PUMP/POL) contradict the fresh momentum/RS scan direction — needs_review", "untracked-alert bug confirmed active with 3 fresh instances (ZKC/AUCTION/ZK) — needs_review"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["headline_risk", "legal_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["INTU: externally confirmed active securities-fraud class action (Baldwin v. Intuit, N.D. Cal. 3:26-cv-07086), filing deadline 2026-09-08 — desk's own legal-risk gate already caps it to C/manual-review despite a 98.3 raw A-tier score", "UNH: ongoing DOJ Medicare-billing criminal probe, C-tier score 57.1, correctly not actionable", "ONG/USDT open long directly opposes the desk's own -17.3%/-12.7% weak-symbol read — concrete contradiction risk on a live position"] },
    { "agent": "playbook_performance", "verdict": "bad", "confidence": 0.7,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample", "missed_winner"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto scalp mode: PF 0.125, avgR -0.095, n=96 (85 triggered) — structurally losing, consistent with prior 'disabled by design' notes", "crypto swing mode: PF 1.40 — best-performing mode by a wide margin", "cross-exchange confirmation PF 0.64 (losing) vs Binance-only PF 1.87 (strong) — confirmation-source quality matters", "ZKC/USDT: prior review's best long-watch thesis played out (+65% 24h) but the tracked signal never triggered — a missed winner tied to the untracked-alert bug"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate": { "symbol": "UNI/USDT", "trigger": "Catalyst-confirmed (momentum_breakout basket, fresh <1h), OI+price both up (OI 24h +23.5%, long/short 1.6-1.8x), funding neutral. Currently >2 ATR from EMA20 — wait for a pullback/retest into the rising-EMA20 zone before entry; do not chase the extended print.", "reason": "Best combination of confirmed catalyst + healthy derivatives positioning among this cycle's strongest symbols." },
    "best_short_candidate": { "symbol": "ONG/USDT", "trigger": "Confirmed breakdown-with-volume on a retest of prior support-turned-resistance. Bearish RS (-17.3%/-12.7% 24h), negative funding across bybit+mexc (crowding elevated), OI down + price down = active deleveraging.", "reason": "Cleanest bearish technical + derivatives alignment this cycle — BUT the desk already holds an active LONG on this exact symbol (see §7); do not add a fresh short without first resolving the existing position via manual review." },
    "best_catalyst_candidate": { "symbol": "TAO/USDT", "trigger": "ai_narrative basket (TAO/RENDER/FET/NEAR), fresh <1h, multi-symbol AI-sector rotation. Desk already holds an active TAO/USDT swing long (score 67.5, triggered) — the catalyst confirms the existing thesis; watch for basket-wide crowding as the rotation matures.", "reason": "Only basket in today's scan with both multi-symbol confirmation and an existing aligned position." },
    "avoid_candidate": { "symbol": "INTU", "reason": "Active, externally-confirmed securities-fraud class action (filing deadline 2026-09-08) despite a 98.3 raw A-tier technical score. Correctly capped to C/manual-review by the desk's own legal-risk gate — treat as AVOID regardless of technical strength, and irrespective of the market-closed demotion." },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 6
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.75 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | caution | 0.60 | mixed, risk_off, longs_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, fresh_catalyst, catalyst_confirmed, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.50 | oi_supports, oi_contradicts, funding_extreme, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | overextended, chase_risk, price_moved_away, clean_retest | advisory_only |
| execution_lifecycle | needs_review | 0.65 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, legal_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | bad | 0.70 | playbook_failing, playbook_working, low_sample, missed_winner | advisory_only |
| head_trader | caution | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (23:32 EEST)

- **Lifecycle-status backlog resolved (for now)**: spiked to 494 rows at 23:32, now back to 253 — near the long-running ~252 baseline. Not yet proof the underlying delay pattern is fixed (see §14).
- **Untracked-alert bug: still active, expanding, not shrinking.** DEXE/USDT (~29h at 23:32) is now ~38h unresolved. Three **new** instances appeared overnight: ZKC/USDT, AUCTION/USDT, ZK/USDT (all sent 21:24 EEST yesterday).
- **ZKC/USDT — missed winner.** Was the previous review's best long-watch (pullback zone 0.0600-0.0634). It never pulled back — instead it rallied +65.2% 24h and is now the single strongest symbol in the swing scan. The tracked watchlist thesis never triggered a live signal; ties directly to the untracked-alert bug above.
- **Regime cooled on the short timeframe, held on the longer one.** 23:32 review: bullish/risk-on trend, breadth 71.8%/79.5%. Now: intraday breadth down to 42.9%/61.9% (range/chop), but swing breadth still healthy at 47.6%/71.4% (uptrend intact). Reads as digestion, not reversal.
- **Macro risk unchanged at the ceiling (100/100)** — but this review is the first to externally verify the Iran/Hormuz conflict is a genuine active escalation rather than recycled headline noise, and to find that crypto has historically shrugged off this specific saga.
- **New catalyst, muted net effect**: Coldcard hardware-wallet exploit (~2,055 BTC estimated stolen) landed alongside a continuing 9-day BTC/ETH ETF net-inflow streak ($242M+) — no clear net directional signal.
- **New avoid candidate**: INTU securities-fraud class action, not flagged in the 23:32 review (that review's stocks context was Sunday-closed with no fresh legal flags).
- MANTRA/USDT swing long (flagged elevated-risk at 23:32 after external confirmation it was hit by the Cosmos EVM six-chain exploit) remains open (score 66.3, triggered) — carried-forward risk, unresolved this cycle.

## 5. Catalyst Coverage

- Total catalyst events today (`2026-08-31` cycle): **445**. Mapped: **192** (43.1%). Unmapped: **253 (56.9%)**. Narrative baskets: **4**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Driven by geopolitical wire volume (Iran/Hormuz) and general news, not a symbol-resolution failure per se.
- Top 3 unmapped headlines: "Iran's IRGC says it launched attack on two US bases in Jordan – Reuters"; "Oil jumps more than 1% after US attack on Iran's Larak island – Reuters"; "LG ELECTRONICS UNVEILS THE NEXT EVOLUTION OF AI HOME AT IFA 2026".
- Active narrative baskets (from the fresher `2026-08-30` cycle embedded in the reports, 1045 events / 6 baskets): `ai_narrative` (TAO/RENDER/FET/NEAR, fresh <1h, catalyst_backed); `binance_ecosystem_teaser` (BNB/ASTER, fresh <6h); `momentum_breakout` (HEMI/UNI/AUCTION, fresh <1h — UNI explicitly catalyst-confirmed, HEMI/AUCTION not); `rwa_narrative` (ONDO/XLM, freshness unknown); `perps_dex_narrative` (HYPE, <24h); `delisting_thin_liquidity` (AAVE, <24h, avoid-low-liquidity playbook).
- Top-importance events: Cronos $75M hack attempt (BNB/USDT, 0.79); Coldcard exploit ~2,055 BTC (BTC/USDT, 0.77 ×2, offset by continued ETF inflows); TSLA SEC settlement $1.5M fine (0.77, minor); UNH DOJ Medicare-billing criminal probe (0.73, six separate wire hits — the most heavily-covered single legal story today).

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **mixed** — intraday range/chop, swing uptrend still intact; macro overlay pinned risk-off (100/100) but externally confirmed as a familiar, desensitized headline pattern rather than a fresh shock.
- Stocks mood: **closed** (04:39 EEST overnight) — underlying regime read from the latest report is **risk_on** (VIX 14.43, breadth 75%/100% above EMA20/50, 3/4 indices uptrend) — carry into the US-session watchlist, do not treat as confirmed until after the 09:30 ET open.
- Dominant narrative: AI-sector rotation (TAO/RENDER/FET/NEAR) and momentum/catalyst-confirmed breakout (UNI) are the freshest, most multi-symbol-confirmed threads; geopolitical (Iran/Hormuz) dominates raw headline volume but is muted in price impact per external check.
- Preferred side now: **longs**, selectively — no new setups clear the desk's own threshold; existing longs should be triaged (see §9) before adding exposure.
- Best long candidate: UNI/USDT (wait for pullback — see §8).
- Best short candidate: ONG/USDT (wait for confirmed breakdown retest — see §8; note the desk holds a contradicting open long here).
- Best catalyst-backed candidate: TAO/USDT (ai_narrative basket, already an aligned open position).
- What to avoid: INTU (legal risk, confirmed); ONG/PUMP/POL longs should not be added to or chased further without manual review (see §7).
- What would change the view: a fresh de-escalation or escalation headline out of the Strait of Hormuz with an actual price reaction in BTC/ETH (not just headline volume); a clean pullback print on UNI/HEMI/AUCTION into the rising EMA20; resolution of the ONG/PUMP/POL long-vs-momentum contradiction one way or the other.

## 7. Candidate Deep Dives

_**TradingView / manual chart check unavailable this run** — all technical reads below (EMA distance, ATR extension, breakdown/retest structure) come from the local OHLCV/ATR/EMA fields already computed in the intraday/swing reports, not a live chart inspection._

### 1. ONG/USDT (open long, swing, score 73.9, triggered) — contradiction / needs_review
- Has price already reacted to the catalyst? No specific fresh catalyst; this is a pure momentum/RS breakdown (-17.28% intraday scan, -12.68% swing scan, both tagged `weak_vs_market, breakdown, overextended`).
- Is the setup chasing? N/A for the existing long — it was opened at a materially better level; the concern is the trend has since reversed against it.
- Is there a retest/pullback structure? No — this is a clean breakdown with OI down + price down (deleveraging/long liquidation per the swing derivatives table) and negative funding across bybit+mexc (crowding elevated per cross-check).
- Overextended >2 ATR from EMA20? Rejected-list entries this cycle for ONG (new short attempts) cite exactly this, plus a short-squeeze-risk cap to C — so a fresh short here is itself lower-conviction than the raw bearish read suggests.
- Aligned with current market mood? No — this is the single clearest technical-vs-position contradiction on the desk right now.
- Long, short, or wait? The open position is long; the fresh data says short. Recommend flagging to manual review rather than auto-closing (out of scope for this advisory run).
- Actionable now or after confirmation? N/A — existing position, not a new entry.
- What would invalidate the short thesis? A reclaim of the recent breakdown level with volume, or a positive catalyst (none currently mapped to ONG).
- Chase-risk? N/A.
- Catalyst confirmation or contradiction? No catalyst on either side — this is a pure technical contradiction.

### 2. INTU (stocks, no position — new avoid candidate, score 98.3 raw A-tier → C)
- Has price already reacted? Yes — per external research, INTU fell ~20% on 2026-05-21 after the underlying TurboTax growth-guidance disclosures; the stock has since stabilized but the litigation is ongoing (lead-plaintiff deadline 2026-09-08).
- Is the setup chasing? N/A — technical score is high (98.3) but this is irrelevant given the legal flag.
- Retest/pullback structure? Not evaluated — legal risk overrides technical read per the desk's own gate.
- Overextended? Not evaluated for the same reason.
- Aligned with market mood? Irrelevant — legal risk is symbol-specific, not regime-driven.
- Long, short, or wait? Neither — AVOID / manual review, regardless of direction.
- Actionable now or after confirmation? Never actionable while the class action is open and unresolved; market is also closed at this hour regardless.
- What would invalidate the avoid call? Dismissal or settlement of the Baldwin v. Intuit case with no material findings — would need re-verification, not assumed.
- Chase-risk? N/A.
- Catalyst confirmation? Confirmed via external search (Morningstar, PR Newswire, GlobeNewswire, Bleichmar Fonti & Auld — see §13) — real, active, multi-firm-represented securities-fraud class action, not a single-source rumor.

### 3. UNI/USDT (no position, best long-watch, catalyst-confirmed)
- Has price already reacted to the catalyst? Yes — +9.97%/+13.50% 24h across the two reports, OI confirms (24h OI +23.5%, long/short 1.6-1.8x).
- Is the setup chasing? Yes at the current print — rejected this cycle for "more than 2 ATR from EMA20; do not chase" is not explicitly listed for UNI in §7b but UNI shares the same extended-momentum profile as its basket-mates (HEMI/AUCTION), which were rejected on exactly this basis.
- Retest/pullback structure? Not yet — needs to develop one; the basket's own playbook is explicitly `wait_pullback`.
- Overextended? Likely, given basket-mates were rejected for exactly this.
- Aligned with market mood? Yes — one of the few genuinely catalyst-confirmed setups this cycle (momentum_breakout basket, single_source but fresh <1h).
- Long, short, or wait? Long, wait-for-trigger.
- Actionable now or after confirmation? After a pullback into the rising EMA20 with volume confirmation.
- What would invalidate it? A break of the basket's momentum structure, or funding/OI rolling over (currently funding neutral, OI still rising — healthy).
- Chase-risk? High at the current extended print — this is precisely why it's a watch, not an entry.
- Catalyst confirmation? Confirmed — explicitly labeled catalyst-backed in the `momentum_breakout` basket, distinct from basket-mates HEMI/AUCTION which are flagged as momentum-only.

### 4. TAO/USDT (open long, swing, score ~67.5, triggered) — catalyst-backed, aligned
- Has price already reacted? Yes, moderately — part of the broader AI-sector rotation (NEAR/RENDER/TAO/FET), fresh <1h basket.
- Chasing? The existing position was opened earlier; a fresh short attempt on TAO this cycle was explicitly capped to C for short-squeeze risk — reinforces that the long bias here is the correct side, not a fresh chase.
- Retest/pullback structure? Not required — position already held.
- Overextended? Not flagged specifically for TAO's long side this cycle.
- Aligned with market mood? Yes — the ai_narrative basket is one of only two multi-symbol-confirmed catalyst threads today (with `momentum_breakout`).
- Long, short, or wait? Long, hold — catalyst supports the existing thesis.
- Actionable now or after confirmation? Already actionable/held; monitor for basket-wide crowding as AI-sector rotation matures (narrative heatmap shows AI momentum 70.2-78.7/100, but attention only 18/100 — early-stage, not yet crowded).
- What would invalidate it? A reversal in the basket's shared RS-vs-BTC read, or a rotation into a different narrative.
- Chase-risk? Low for the existing position; would be moderate for a fresh add at current levels.
- Catalyst confirmation? Confirmed — fresh <1h, multi-symbol basket.

### 5. POL/USDT (open long, swing, score 73.0, triggered) — second contradiction case
- Has price already reacted? Yes, negatively — -8.82%/-8.23% 24h, tagged `weak_vs_market, breakdown` in both reports' Weakest Symbols lists.
- Chasing? N/A for the existing long.
- Retest/pullback structure? A fresh short attempt on POL this cycle was explicitly capped to C for **thin-liquidity short-squeeze risk** — meaning the bearish read, while directionally correct, is lower-conviction/less liquid than ONG's case.
- Overextended? Fresh short attempts flagged ">2 ATR from EMA20; do not chase" for POL specifically.
- Aligned with market mood? No — same technical-vs-position contradiction pattern as ONG, but with an added squeeze-risk caveat that argues for patience over urgency.
- Long, short, or wait? Existing position is long; fresh data leans bearish but squeeze-prone — recommend manual review rather than either adding to the long or flipping short.
- Actionable now or after confirmation? N/A — existing position.
- What would invalidate the bearish read? A short-squeeze move back through recent highs, consistent with the system's own squeeze-risk flag.
- Chase-risk? High on either side given the squeeze-risk cap.
- Catalyst confirmation? None mapped either way — pure technical contradiction, lower-conviction than ONG's.

## 8. Best Candidates Ranked

1. **Best long-watch: UNI/USDT** — catalyst-confirmed, OI+price up, wait for pullback into rising EMA20; do not chase the current extended print.
2. **Best catalyst-watch: TAO/USDT** — ai_narrative basket (fresh <1h, TAO/RENDER/FET/NEAR), already an aligned open long; monitor for crowding as the rotation matures.
3. **Best short-watch: ONG/USDT** — confirmed breakdown-with-volume retest needed; bearish RS + negative funding + OI-down/price-down deleveraging all align, but the desk's own open long here means this is a manual-review item before it's a fresh short.
4. **Best avoid: INTU** — externally confirmed active securities-fraud class action; AVOID regardless of the 98.3 raw technical score.

No candidate this cycle cleared the desk's own A/B threshold for a genuinely fresh, clean entry — all four above are watch-and-wait or manage-existing-position items, consistent with the intraday/swing reports' own "No A-tier / No B-tier setups found" this cycle.

## 9. Avoid / No Trade

- This decision window only — scanning, tracking, and the scheduler continue regardless.
- **AVOID new entries**: INTU (legal risk), any fresh short on ONG/POL without first resolving the existing long-side contradiction (squeeze risk on POL specifically), any chase of UNI/HEMI/AUCTION at current extended levels.
- **No fresh crypto shorts anywhere** — the desk currently holds 0 short positions across 50 active crypto signals; today's fresh scan surfaces several short-biased weak symbols (ONG, PUMP, POL, TRUMP, BMT) but none have cleared to an actionable short tier this cycle.
- **Stocks intraday: nothing actionable** — market closed, all raw A-tier ideas gate-demoted to C for `market_closed_intraday_planning_only`; re-evaluate at/after 09:30 ET.

## 10. Main Risks

- **Live technical-vs-position contradiction** on ONG/USDT, PUMP/USDT, and POL/USDT — three open longs directly opposing the desk's own fresh momentum/RS read. Highest-priority manual-review item this cycle.
- **Untracked-alert bug confirmed still active** (ZKC/AUCTION/ZK, plus the 38h-old DEXE case) — degrades confidence in Telegram-alert-to-tracked-signal reconciliation, and appears to have contributed to a missed winner (ZKC +65.2%).
- **Geopolitical overhang**: active US-Iran conflict in the Strait of Hormuz, externally confirmed and ongoing — muted price impact so far per historical pattern, but a genuine tail risk if it escalates beyond the recent pattern (oil-spike-only reactions).
- **Legal risk on two symbols**: INTU (stocks, active class action) and UNH (stocks, DOJ criminal probe) — both correctly gated by the desk's own legal-risk logic, no action needed beyond continued exclusion.
- **Catalyst mapping weak this run** (56.9% unmapped) — treat the catalyst layer as context only, not a final decision input, until mapping coverage recovers.
- **Crypto scalp mode structurally unprofitable** (PF 0.125) — consistent with its known "disabled by design" status; no new action needed, just confirmation the prior decision remains correct.
- Telegram send for this cycle's compact summary (§12) was **not sent** — see §14 (no allowlisted CLI/notifier command available within this run's permission contract).

## 11. Action Plan — Next 4 Hours

1. Manual review of ONG/USDT, PUMP/USDT, POL/USDT open longs against the fresh bearish momentum/RS read — decide hold/trim/exit outside this advisory run.
2. Watch UNI/USDT for a pullback into the rising EMA20 with volume confirmation before considering a fresh long entry.
3. Monitor the ai_narrative basket (TAO/RENDER/FET/NEAR) for crowding as attention (currently 18/100) catches up to momentum (70-79/100).
4. Re-run `detect_untracked_legacy_alerts` with a rolling (not calendar-day) window next cycle to properly catch the ZKC/AUCTION/ZK instances going forward.
5. Track the Iran/Hormuz situation for any actual BTC/ETH price reaction (not just headline volume) — escalation beyond the recent pattern would be the first genuine trigger to re-rate the macro risk-off score as more than background noise.
6. Stocks: carry MSFT, CMCSA, ABNB, NFLX, NOW, UBER, MU, CRM, ADBE, CRWD, XLK, IBM, DXCM, NET as planning-only watchlist names into the 11:30 EEST pre-US review; re-confirm on fresh RTH levels, not these overnight prints. INTU stays excluded regardless of score. AVGO/CRM/CRWD/DELL/PANW/SNOW carry an earnings-in-1-2-days flag — do not chase into the print.

## 12. Final Verdict per Mode

- **Crypto scalp**: NO TRADE (structural, PF 0.125) — not a fresh call, consistent with prior sessions.
- **Crypto intraday**: WATCH — no new A/B setups; range/chop regime favors mean reversion or waiting for a clean breakout, not chasing.
- **Crypto swing**: WATCH / MANAGE EXISTING — uptrend intact, but 3 of 41 open longs (ONG, PUMP, POL) need manual review against contradicting fresh data. New entries require a genuine pullback (UNI) or catalyst-confirmed continuation (TAO/FET), not a chase.
- **Stocks intraday**: PLANNING ONLY — market closed; carry the A-tier-raw watchlist into the US session, re-confirm on RTH levels. INTU excluded on legal risk regardless of tier.
- **Stocks swing/invest**: deprecated pipeline, no verdict issued (informational only per prior sessions).

## 13. Sources

- [U.S. strikes Iran missile sites on Larak Island](https://www.washingtonpost.com/national-security/2026/08/30/us-strikes-iran-missile-sites-larak-island/) — Washington Post, 2026-08-30.
- [US and Iran trade attacks, marking first escalation in a month](https://edition.cnn.com/2026/08/30/politics/us-iran-strikes-larak-island) — CNN, 2026-08-30.
- [Iran Denies Trump's Hormuz Deal, Oil Jumps but Bitcoin Watches](https://finance.yahoo.com/markets/commodities/articles/iran-denies-trump-hormuz-deal-123921314.html) — Yahoo Finance, date unavailable (referenced for the "BTC muted/desensitized to Hormuz headlines" pattern; contextual, late Aug 2026 per search ranking).
- [Intuit Inc. (INTU) Class Action Lawsuit Seeks Recovery for Investors; September 8, 2026, Deadline](https://www.globenewswire.com/news-release/2026/08/23/3349410/0/en/intuit-inc-intu-class-action-lawsuit-seeks-recovery-for-investors-september-8-2026-deadline-contact-kessler-topaz-meltzer-check-llp.html) — GlobeNewswire / Kessler Topaz Meltzer & Check, 2026-08-23.
- [Intuit Inc. Class Action Lawsuit](https://www.bfalaw.com/cases/intuit-class-action-lawsuit) — Bleichmar Fonti & Auld LLP, date unavailable (case detail: Baldwin v. Intuit Inc., N.D. Cal., 3:26-cv-07086).

## 14. Fix Requests / TODO

### TODO-untracked-alert-recurrence
- **issue:** The watchlist-alert-to-proposed_signal reconciliation bug (previously raised HIGH, 2026-07-17) is confirmed still active 6 weeks later, with 3 fresh instances overnight.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-28` → 8 rows including ZKC/USDT (21:24:42Z), AUCTION/USDT (21:24:43Z), ZK/USDT (21:24:47Z), all sent 2026-08-30, all still without a backing `proposed_signal`; DEXE/USDT (2026-08-29T14:36:42Z) now ~38h unresolved.
- **suggested manual fix:** Investigate whether a watchlist re-fire on an already-tracked symbol (AUCTION, ZK) is failing to match the existing signal_id, vs. a genuinely new alert (ZKC, DEXE) never minting one at all — these may be two distinct root causes requiring separate fixes.
- **priority:** high
- **first observed (this recurrence):** 2026-08-31 04:39 EEST (originally 2026-07-17 per prior memory).

### TODO-untracked-alert-detector-window
- **issue:** The mandated `--since <today>` invocation of `detect_untracked_legacy_alerts` uses a calendar-day cutoff, not a rolling window — it silently misses alerts sent the previous evening that are still within or just past the detector's own 6h reconciliation window at review time.
- **evidence:** `--since 2026-08-31` returned 0 rows at 04:39 EEST; `--since 2026-08-28` surfaced 3 fresh same-window rows (ZKC/AUCTION/ZK, sent 21:24 the prior evening).
- **suggested manual fix:** Change the review routine's mandated invocation to a rolling lookback (e.g. `--since <36h ago>`) instead of a calendar-day string, or have the detector script itself default to a rolling window.
- **priority:** medium
- **first observed:** 2026-08-31 04:39 EEST.

### TODO-swing-report-date-rollover
- **issue:** The swing report's human-readable "Generated at" header shows a date that does not roll over past UTC midnight when converted to EEST, while the intraday report's equivalent field rolls over correctly.
- **evidence:** `data/reports/swing/2026-08-30_21-16_swing_report.md` header reads "Generated at: 2026-08-30 00:16:05 EEST" — filename implies 2026-08-30 21:16 UTC, which is 2026-08-31 00:16 EEST (date should read 08-31, not 08-30). The intraday report's equivalent conversion (`2026-08-30_23-39` UTC → "2026-08-31 02:39:00 EEST") rolls over correctly.
- **suggested manual fix:** Compare the swing-report generator's EEST-formatting code path against the intraday report's for the date-rollover logic.
- **priority:** low
- **first observed:** 2026-08-31 04:39 EEST.

### TODO-telegram-notifier-not-allowlisted
- **issue:** §O of this scheduled task's SKILL.md requires sending a compact Telegram summary "via the existing notifier," but no such command is in the task's own allowed-CLI list (§A.4), and inventing a new invocation (e.g. `telegram-test`) would be an out-of-contract write action requiring a permission prompt this autonomous run cannot request.
- **evidence:** `python -m src.cli --help` lists `telegram-test` ("Send a one-off test message") and `telegram-dashboard-refresh`, neither of which appears in this SKILL.md's §A.4 allowlist.
- **suggested manual fix:** A human session should add the specific, correct notifier invocation (with its exact arguments) to the SKILL.md's §A.4 allowlist so future scheduled runs can comply with §O without ambiguity.
- **priority:** medium
- **first observed:** 2026-08-31 04:39 EEST.

### TODO-lifecycle-status-backlog-cadence
- **issue:** The lifecycle-status gap (`expires_at < now()` while status still open) spiked from a ~252 baseline to 494 rows at 23:32 EEST, then reverted to 253 by 04:39 after the next lifecycle-review step ran. The backlog appears to build up between lifecycle-review runs and clear in a batch rather than staying near-zero continuously.
- **evidence:** Direct SQL sweep on `proposed_signals`: 494 rows at 23:32 review vs. 253 rows at 04:39 review, after the 03:33-03:35 `open intraday lifecycle review` + `track-signals (post)` steps ran.
- **suggested manual fix:** Consider a tighter/more frequent lifecycle-reconciliation cadence, or confirm the ~250-row "resting" backlog itself is expected/benign and only the spike to 494 was anomalous.
- **priority:** low
- **first observed:** 2026-08-30 23:32 EEST (this review confirms it self-resolved by 04:39).

### TODO-mantra-exploit-risk-unresolved
- **issue:** MANTRA/USDT open swing long (score 66.3, triggered) was flagged at the 23:32 review as carrying elevated risk after external confirmation MANTRA was one of the chains hit in the Aug 20-25 Cosmos EVM six-chain exploit. Position remains open, unresolved, not re-verified this cycle.
- **evidence:** `active-signals --asset-class crypto` shows `sig_7645e0e74b394b42 MANTRA/USDT swing long triggered`, expires 2026-09-04.
- **suggested manual fix:** A human/manual session should re-verify current MANTRA/exploit-fallout status and decide whether the open long needs risk-management action.
- **priority:** medium
- **first observed:** 2026-08-30 23:32 EEST (carried forward, still open at 04:39).
