# Opus Enriched Review — late-session risk review — Auto Cycle 21:30 EEST

## 1. Executive Summary

**Slot: late-session risk review** (nominal 21:30 EEST; dispatched ~21:42, ~12 min jitter — see §3). **Advisory only — no auto-trade, no scoring/threshold/strategy changes made or implied.**

Today (2026-07-19) is a **Sunday** — US cash equities are closed all day; stocks below are planning/watchlist context only. Crypto is the sole live-actionable class this window.

**Regime cooled off during this window.** Between the 15:20 EEST intraday scan and the fresh 21:51 EEST one, the internal market-regime label flipped from "bullish trend (risk-on)" to **"range/chop (neutral)"** (altcoin breadth 55.3%→52.9%, momentum-filter candidates 9→1). Both the freshest scalp (18:45 data, generated 21:45) and intraday (18:45 data, generated 21:51) reports show **zero A-tier and zero B-tier setups** — every previously-B-tier momentum name (BANK, KAITO, VANRY, TLM) has been demoted to watchlist-only or rejected outright. There is no fresh actionable entry this window; this is a manage-existing-exposure window, not a new-entry window.

**10 active crypto positions**, all B-tier, all long except one short. 2 are `triggered` (not yet TP), 6 are running with TP1 or TP2 already booked, and **2 are stale/past their own `expires_at` while still shown `tp1_hit`** (ALLO/USDT — expired 15:21 today; NEAR/USDT short — expired 2026-07-17, ~2 days stale) — flag both **NEEDS REVIEW**, not fresh.

**Macro divergence persists** (verified externally, not resolved this window): the US-Iran conflict is live and escalating — CENTCOM has struck Iranian positions nightly since a ceasefire broke down July 15, Iran has hit >85 US installations across Bahrain/Kuwait/Jordan, and Bitcoin has been trading a volatile $63K–$69K range this week on the back of it. Internal technical trend reads (BTC/ETH "uptrend") sit awkwardly against this verified risk-off macro backdrop.

**Integrity issue unchanged, still open**: the untracked watchlist-alert bug (Telegram alert fires, no `proposed_signal` minted) still shows exactly **5 instances today** across ALLO/USDT (×3), HOME/USDT (×1), BANK/USDT (×1) — unchanged since the 19:14 review, same underlying root cause, not yet fixed (expected — this run cannot fix code). See §14 TODO-1.

**Catalyst mapping weak this run (65.7% unmapped)** — use catalyst layer as directional context only.

**Stocks:** market closed. Carrying forward the UNH DOJ-probe legal-risk flag on the two open C-tier invest longs into Monday — no new information this window.

## 2. Data Used

- Reports: scalp (`2026-07-19_18-45`, generated 21:45 EEST, **fresh, ~8 min old** — regime just flipped to range/chop, zero A/B ideas), intraday (`2026-07-19_18-51` filename i.e. 18:45 data, generated 21:51 EEST, **fresh, ~2 min old** — same regime flip, zero A/B ideas, 8 watchlist-only C-tier cards). Swing (`2026-07-19_01-47`, ~17h old — **stale**, past the 14h threshold, referenced only for continuity). Stocks intraday (`2026-07-17_21-56`) / swing / invest (`2026-07-02`) — all weekend-closed, planning-only.
- Catalysts: `data/catalysts/2026-07-19/catalyst_events.jsonl` (2,651 cumulative events today), `narrative_baskets.jsonl` (6 baskets), latest `catalyst_cycle_15-23.md` (18:23 EEST — no newer cycle needed per §D since today's folder already existed).
- LLM packet: `llm_analysis_packet.md` (18:21 EEST, superseded in this review by the fresher 21:45/21:51 reports for regime/candidates, still used for narrative/macro cross-check).
- CLI: `active-signals` ×2 (crypto 10 rows, stocks 50 rows — all stocks rows are pre-weekend carryover), `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-07-19` (5 findings, unchanged from 19:14).
- DB reads: `news_items` 24h freshness checks for BANK/USDT, ALLO/USDT, KAITO/USDT, VANRY/USDT (BANK: 1 generic CoinGecko price-page row, no real catalyst; ALLO/KAITO/VANRY: 0 rows).
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-19_1914.md` (US open reaction slot, nominal 18:30, dispatched 19:14).
- External: 2 WebSearch queries (US-Iran/Bitcoin macro; Lorenzo Protocol/BANK catalyst check) — both corroborate internal reads, no contradiction. No WebFetch needed this run (search-result snippets were sufficient and internally consistent). 3 sources ingested via `scripts.ingest_enriched_review_sources` (crypto-tagged).

## 3. Scheduler / Data Freshness

- `scheduler.log`: mtime **21:39–21:52** (actively writing during this review) — a **new scheduler cycle started at 21:38 EEST** (`CYCLE 1/12 START — Sun 2026-07-19 21:38, weekend, crypto-only`) and was still mid-flight while this review ran (scalp report completed 21:46, intraday completed 21:51; SEC EDGAR / catalyst refresh / other steps still pending as of write time). Not deferred — fresh by a wide margin.
- Latest **completed** cycle summary on disk: `cycle_06_18-02_summary.md` (18:43) — the 21:38 cycle's own summary file had not yet been written at review time; its live log output was used directly instead (same discipline as reading the report files it produced).
- Monitors: `derivatives_monitor` active (76 symbols, 5 venues, all writing normally), `pending_monitor` actively fetching candles as of 21:52 EEST, `mexc_canary_monitor` running (leader-lock normal). All monitors healthy.
- Dispatch jitter: nominal 21:30 EEST, actual ~21:42 EEST (~12 min) — immaterial to content freshness.
- Swing: ~17h old, past the 14h stale threshold — excluded from fresh verdicts, used only for continuity.
- Stocks: all modes stale/weekend-closed — planning-only.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-07-19 21:53 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["cycle_07 summary file (cycle still mid-flight at write time)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scalp report generated 21:45 EEST (~8min old)", "intraday report generated 21:51 EEST (~2min old)", "swing report 17h old, excluded", "stocks all weekend-stale, planning-only", "scheduler cycle actively running since 21:38 EEST"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["chop", "mixed", "risk_off", "wait_for_trigger"],
      "data_missing": ["live BTC/ETH tick price beyond report snapshot"],
      "suggested_effect": "advisory_only",
      "facts_used": ["internal regime label flipped bullish-trend->range/chop between 15:20 and 18:51 reports", "altcoin breadth 55.3%->52.9%, momentum-filter candidates 9->1", "external verification: BTC $63-69K range this week on US-Iran conflict"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["no_catalyst", "mapping_weak", "stale_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 65.7% unmapped today (910/2651 mapped)", "BANK/USDT momentum_breakout basket explicitly tagged no-confirmed-catalyst, externally corroborated", "KAITO/VANRY/ALLO: 0 news_items rows in last 24h"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["oi_contradicts", "funding_extreme", "post_unwind_chop"],
      "data_missing": ["external cross-venue funding refreshed beyond 15:20 snapshot"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BANK/USDT price up + OI down = short covering, weaker continuation quality (21:45 scalp report)", "KAITO/USDT price up + OI up = fresh positioning, crowding normal (cleanest of the active momentum names)", "VANRY external funding negative/elevated crowding cross-venue (15:20 packet)"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["chase_risk", "overextended", "entry_late", "price_moved_away"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BANK/USDT >2 ATR from EMA20, rejection reason literally 'do not chase' (21:45 scalp report)", "0 A-tier / 0 B-tier in both fresh scalp and intraday reports", "8 C-tier watchlist-only cards, all explicitly 'not active until regime/volume/confirmation improves'"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "caution",
      "confidence": 0.8,
      "reason_codes": ["open_actionable", "needs_review", "no_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["10 active crypto signals: 2 triggered, 4 tp1_hit running, 2 tp2_hit running, 2 stale-past-expiry (ALLO, NEAR) needing review", "stocks: 50 rows, all pre-weekend carryover, market closed"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["headline_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["active US-Iran conflict is an open gap-risk driver into Monday's cash open", "UNH DOJ probe unresolved against 2 open C-tier invest longs (carried forward, no new info this window)", "NEAR/USDT short ~2 days past expiry still shown active — bookkeeping risk, not a live risk position"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto direction=short: n=12, PF 0.20, avgR -0.44 (weak)", "crypto scalp: n=27, PF 0.59, avgR -0.15 (weak, matches report's own low-confidence header)", "crypto intraday/swing: PF ~2.0 each (stronger) but no fresh trigger exists right now", "no-catalyst intraday cut: WR 23% / PF 0.70 / -3R (14d)"]
    }
  ],
  "head_trader": {
    "overall_verdict": "watch_only",
    "confidence": 0.65,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": { "symbol": "VANRY/USDT", "trigger": "conditional pullback into 0.0055-0.0056 with 1h acceptance; invalidation below 0.0053", "reason": "cleanest structured watchlist card this cycle; RS +16% vs BTC but no catalyst, C-tier score 61.3 — data-collection-grade, not conviction" },
    "best_short_candidate": { "symbol": "SYN/USDT", "trigger": "failed-bounce/retest short into 0.2152-0.2186 only, invalidation above 0.2228, TP1 0.2061", "reason": "downtrend, RS -9.5% vs BTC, matches crypto_failed_bounce_short playbook (WR40/PF2.00 14d) - must wait for the retest, not the current wick" },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "pullback into narrative-confirmed wait_pullback zone with volume; do not chase current level", "reason": "perps_dex_narrative basket primary, TKNZ multi-token ETF launched significantly overweight HYPE (~6% weighting) - genuine two-sided catalyst, still below active-trade score threshold" },
    "avoid_candidate": { "symbol": "BANK/USDT", "reason": "no confirmed catalyst (internal + external agree), >2 ATR from EMA20 with explicit 'do not chase' rejection, OI now falling on the bounce (short-covering, weakening), and it is the live untracked-alert-bug symbol (§14 TODO-1)" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---:|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.60 | chop, mixed, risk_off, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | no_catalyst, mapping_weak, stale_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.55 | oi_contradicts, funding_extreme, post_unwind_chop | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, overextended, entry_late, price_moved_away | advisory_only |
| execution_lifecycle | caution | 0.80 | open_actionable, needs_review, no_entry | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.70 | playbook_failing, low_sample | advisory_only |

## 4. What Changed vs Previous Review (19:14 EEST, US open reaction slot)

- **Regime downgraded**: "bullish trend (risk-on)" → **"range/chop (neutral)"** between the 15:20 and 18:51 intraday scans. Breadth and momentum-filter counts both fell.
- **All B-tier ideas demoted**: BANK, KAITO, VANRY, TLM were B-tier or top-movers at 19:14; as of the 21:45/21:51 fresh reports, **zero A-tier and zero B-tier setups exist** — everything is now C-tier watchlist-only or outright rejected.
- **Active-signal count and statuses unchanged** (10 crypto rows, same statuses) — no new fills, no new stops between 19:14 and now.
- **Untracked-alert count unchanged** (5, same 3 symbols: ALLO×3, HOME×1, BANK×1) — bug still open, not newly worsened this window.
- **New info this window**: none on UNH legal risk (carried forward verbatim); no new macro de-escalation headline found.
- Confirmed, not invalidated: BANK/USDT avoid-thesis (now further reinforced — OI is now falling on the bounce, i.e. short-covering, weaker continuation than at 19:14).

## 5. Catalyst Coverage

- Total catalyst events today: **2,651**. Mapped (non-null symbol): **910**. Unmapped: **1,741** (**65.7%**).
- Narrative baskets: **6** (rwa_narrative, perps_dex_narrative, delisting_thin_liquidity, ai_narrative, binance_ecosystem_teaser, momentum_breakout).
- **Catalyst mapping weak this run (65.7% unmapped) — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (sample): "Base memecoin $BRIAN surges after Brian Armstrong changes X avatar, then crashes 86%..."; a GENIUS Act one-year-anniversary explainer thread; a CLARITY Act legislative-status thread. None symbol-mappable as posted.

## 6. Market Landscape

Crypto: BTC and ETH both still read "uptrend" at the trend-detector level, but the composite regime label flipped to range/chop as breadth narrowed (52.9% above EMA20, down from 55.3% three hours ago) and the momentum filter collapsed from 9 candidates to 1. Verified external sourcing confirms an active, escalating US-Iran conflict — CENTCOM striking Iranian positions nightly since a July 15 ceasefire collapse, Iran hitting 85+ US installations across Bahrain/Kuwait/Jordan, Bitcoin trading a volatile $63K-$69K band this week. The internal technical read and the verified macro backdrop are not fully reconciled — treat the internal "uptrend" labels as macro-fragile. Every previously-promising momentum name (BANK, KAITO, VANRY, TLM) lost its B-tier status this window without a single stop being hit — this looks like a cooling/consolidation phase, not a reversal, but there is no fresh confirmation either way.

Stocks: market closed (Sunday). No new information since the 19:14 review. UNH's DOJ-probe/earnings-beat two-sided story carries forward unchanged into Monday.

### Market Mood / Risk Routing
- Crypto mood: **mixed, leaning chop** (technical uptrend labels vs. narrowing breadth vs. verified active geopolitical risk-off)
- Stocks mood: **closed** (Sunday)
- Dominant narrative: momentum_breakout cluster losing steam (BANK/TLM/KAITO all demoted this window) vs. the still-unresolved US-Iran macro overhang
- Preferred side now: **wait-for-trigger** — no long or short currently clears every internal safeguard
- Best long candidate: VANRY/USDT — trigger: pullback into 0.0055-0.0056, 1h acceptance, invalidation below 0.0053
- Best short candidate: SYN/USDT — trigger: failed-bounce/retest into 0.2152-0.2186 only, invalidation above 0.2228
- Best catalyst-backed candidate: HYPE/USDT — trigger: pullback into the wait_pullback zone with volume, do not chase current level
- What to avoid: BANK/USDT (chase risk, no catalyst, OI now falling on the bounce, untracked-alert-bug symbol); fresh chases into KAITO/VANRY at current levels (both already extended, both now demoted off B-tier); any new stocks entries (market closed)
- What would change the view: a verified US-Iran de-escalation headline; the regime label reclaiming "bullish trend" on the next cycle; a clean retest fill on VANRY or SYN; Monday's actual US cash open for stocks

## 7. Candidate Deep Dives

**TradingView / manual chart check unavailable** — no chart MCP loaded this run; reads below use only local OHLCV/ATR/EMA/support-resistance fields already present in the fresh scalp/intraday reports, no fabricated chart observations.

### 7.1 BANK/USDT (Lorenzo Protocol) — AVOID / chase risk, thesis reinforced this window

- Has price already reacted? Yes — +84% to +112% over 24h depending on snapshot; already made a fresh local high and is now digesting (4h change flipped to roughly flat/slightly negative in the freshest scan).
- Chasing? Yes — explicit rejection reason in the 21:45 scalp report: "Price is more than 2 ATR from EMA20; do not chase."
- Retest/pullback structure? Not yet established at a level that would qualify as clean.
- Overextended? Yes.
- Would entry now be late? Yes.
- What level makes it actionable? A multi-hour base well below the recent high with volume confirmation, plus a verified fundamental catalyst — none exists (external WebSearch: "no major announcement, new partnership, or protocol update directly explaining the Lorenzo Protocol rally" — capital rotation into AI-tagged names, technical channel-breakout only).
- Aligned with market mood? No — fights the "no fresh verified catalyst" system gate in a chop regime.
- Long/short/wait? Avoid.
- Actionable now or after confirmation? Not actionable.
- Chase-risk? Yes.
- Catalyst confirmation/contradiction? No catalyst — confirmed both internally (`news_items`: 1 generic CoinGecko price-page row only) and externally (WebSearch).
- **New this window**: derivatives flipped from "price up + OI up" (19:14 review) to **"price up + OI down: short covering, weaker continuation quality"** (21:45 scalp report) — the rally's positioning quality is deteriorating, reinforcing avoid.
- **Integrity flag (unchanged)**: a B-tier scalp alert (score 77.9) fired via Telegram at 15:17 with no matching `proposed_signal` — untracked (§14 TODO-1).

### 7.2 Active position review — KAITO/USDT, VANRY/USDT, G/USDT (triggered / running)

- **KAITO/USDT** (`sig_d1ede52b83aa2493`, B, intraday, long, score 71.5, status `triggered`, entry 0.937905-0.953201, invalidation 0.919209): derivatives read is the cleanest of the active book — "price up + OI up: fresh positioning confirms trend, crowding normal." Demoted to watchlist-only in the fresh 21:51 intraday scan (regime chop), but the open position itself has not been stopped. **Verdict: hold per existing plan, do not add — the fresh-entry thesis has weakened even though the open trade has not been invalidated.**
- **VANRY/USDT** (`sig_ee300c0093962175`, B, intraday, long, score 69.2, status `tp1_hit`, running for TP2/TP3): external cross-venue funding negative with "elevated crowding" flagged in the 15:20 snapshot — some short-covering support behind the move. TP1 already banked; treat the remainder as a runner, not a fresh add. A fresh conditional watchlist card also exists at 0.0055-0.0056 (see §6) — that is for a **new** entry, not this position.
- **G/USDT** (`sig_98692d24b7570735`, B, intraday, long, score 66.7, status `triggered`): small, no catalyst, weekend-mode — data-collection-grade position, hold per plan.
- **NEEDS REVIEW — stale bookkeeping**: **ALLO/USDT** (`sig_10088a4c71cae845`) shows `tp1_hit` but `expires_at` was **2026-07-19T15:21:04**, already ~6.5h in the past — this signal should have resolved (win/loss/flat) by now and is instead sitting in `active-signals` past its own window. Compounded by 3 separate untracked watchlist re-alerts on ALLO today (§14 TODO-1) — do not treat any fresh ALLO alert as a new tradeable signal until the underlying bug is fixed.
- **NEEDS REVIEW — stale bookkeeping**: **NEAR/USDT** short (`sig_b16bb9e54598333a`) shows `tp1_hit` with `expires_at` **2026-07-17T15:56:12**, ~2 days past expiry — same pattern, flag for manual cleanup, not a live risk position to react to tonight.

### 7.3 SYN/USDT — best short-watch (failed-bounce structure)

- Downtrend, -9.7%/24h, RS -9.5% vs BTC, no fresh catalyst (0 `news_items` rows in 24h).
- Structured C-tier card (21:51 intraday report): conditional failed-bounce/retest entry 0.2152-0.2186, invalidation above 0.2228, TP1 0.2061 / TP2 0.1984 / TP3 0.1908. Current price 0.2137, ATR 0.0076, support 0.2033, resistance 0.2349.
- Has price already reacted? Yes, the breakdown already happened; shorting the current wick would be chasing.
- What makes it actionable? A bounce *into* the 0.2152-0.2186 zone that fails, on confirmed volume — not the current level.
- Squeeze risk? Score sits at 53.7/100, below active-trade threshold — treat as data-collection-grade even if the retest triggers.
- Verdict: **WATCH-ONLY**, cleanest short structure on the board, consistent with the `crypto_failed_bounce_short` playbook's better 14d numbers (WR 40% / PF 2.00) versus blind RS-weak shorting (overall short PF 0.20 this week).

### 7.4 HYPE/USDT — catalyst-backed watch (carried forward)

- `perps_dex_narrative` basket primary, `wait_pullback` playbook, fresh <6h. TKNZ (T. Rowe Price's actively-managed multi-token spot crypto ETF) launched with HYPE "significantly overweight" — a genuine, real catalyst, not manufactured.
- Below active-trade score threshold this window (not in the 8 structured watchlist cards) — treat as narrative-context, not a live setup.
- Verdict: **WATCH-ONLY / catalyst-backed** — wait for a defined pullback with volume confirmation; do not chase the narrative alone.

### 7.5 UNH — legal/headline risk, MANUAL REVIEW REQUIRED (carried forward, no new information)

- Q2 2026 earnings beat + raised guidance (July 16) against an unresolved/reportedly-widening DOJ probe (Medicare billing → Optum Rx/physician reimbursement → antitrust angle per prior-cited reporting). No new developments found this window.
- Two open C-tier invest longs (`sig_90b50ceef0d1ebd3`, `sig_4697b87c9845547f`) carry this risk with no internal legal-risk gate at that tier (§14 TODO-4, carried forward).
- Verdict unchanged: **AVOID for new adds / MANUAL REVIEW REQUIRED for the existing open positions.**

## 8. Best Candidates Ranked

1. **SYN/USDT** — best short-watch, failed-bounce retest into 0.2152-0.2186 only, invalidation above 0.2228. Cleanest structured setup on the board this window (any direction).
2. **VANRY/USDT** — best long-watch (new entry), pullback into 0.0055-0.0056, invalidation below 0.0053. No catalyst, C-tier, data-collection-grade.
3. **HYPE/USDT** — catalyst-backed watch, wait for pullback with volume; genuine narrative but below threshold.
4. **KAITO/USDT (existing position)** — hold per plan; cleanest derivatives read of the open book but fresh-entry thesis has weakened with the regime flip.
5. **BANK/USDT** — avoid; **UNH** — manual review required (existing positions only).

No clean, fully-confirmed A-tier or high-conviction trade exists this window — this is a routing/watch call, not a stop-trading call.

## 9. Avoid / No Trade

*(This decision window only — never a system-stop command; scanning, tracking, and data collection continue uninterrupted.)*

- **BANK/USDT**: chase risk, no catalyst (internal + external agree), OI now falling on the bounce (weakening short-covering), untracked-alert integrity issue.
- **New UNH adds** (and any new stocks entries generally): market closed; UNH carries an unresolved DOJ legal overhang.
- **Fresh chases into KAITO/VANRY/TLM at current levels**: all three demoted off B-tier this window; the open KAITO/VANRY positions should be held per existing plan, not added to.
- **SYN/USDT as an outright short at the current wick**: must wait for the failed-bounce retest, not the current level.

## 10. Main Risks

- **Macro/geopolitical**: active, escalating US-Iran conflict (nightly CENTCOM strikes since the July 15 ceasefire collapse) is the dominant gap-risk driver into Monday's US cash open; internal "uptrend" technical labels sit against this verified risk-off backdrop.
- **Regime cooling**: momentum-filter candidates collapsed from 9 to 1 and every B-tier idea was demoted to watchlist-only within a single scheduler cycle — a fast-moving regime shift worth monitoring on the next cycle, not yet a confirmed reversal.
- **Data integrity**: untracked watchlist-alert bug still open (5 instances today, 3 symbols) — Telegram-visible alerts firing without a backing `proposed_signal`, degrading PF/winrate/avgR accuracy for ALLO/HOME/BANK.
- **Stale bookkeeping**: two active-signals rows (ALLO/USDT, NEAR/USDT) sit past their own `expires_at` while still shown `tp1_hit` — needs manual resolution, not a live risk tonight but a data-quality gap.
- **Legal/regulatory**: UNH DOJ probe unresolved against two open C-tier positions with no internal legal-risk gate at that tier (§14 TODO-4).
- **Catalyst mapping quality**: 65.7% of today's catalyst events unmapped — directional context only.

## 11. Action Plan — next 4 hours

- No new crypto entries recommended — regime just flipped to chop and every B-tier idea was demoted this cycle.
- Watch SYN/USDT for a failed-bounce retest into 0.2152-0.2186 with rising volume before considering a short; do not short the current wick.
- Watch VANRY/USDT for a fresh pullback into 0.0055-0.0056 before considering a new long add; the existing open VANRY position should simply run its plan.
- Hold KAITO/USDT and G/USDT per existing plan; do not add at current levels.
- Flag ALLO/USDT and NEAR/USDT signals for manual resolution — both are past their own expiry while still shown active.
- No new stocks action possible before Monday's cash open; carry UNH's manual-review flag forward.
- Continue scanning/tracking as normal — no scanner, monitor, or scheduler changes recommended or implied.

## 12. Final Verdict per Mode

- **Crypto scalp**: zero A/B setups this cycle (all rejected, several explicitly via the `crypto_scalp_disabled` kill-switch) — data collection only, consistent with the report's own low-confidence posture (PF 0.14, 14d).
- **Crypto intraday**: zero A/B setups; 8 C-tier watchlist-only cards. Best watch-only long = VANRY/USDT, best watch-only short = SYN/USDT. Existing KAITO/VANRY/G positions held per plan.
- **Crypto swing**: report stale (~17h); no fresh verdict rendered — existing swing positions (LTC, ETHFI, TRUMP, all tp1/tp2_hit and running) carried forward without a fresh read.
- **Stocks (all modes)**: market closed; planning/watchlist only. UNH manual-review flag carried forward; no new stock adds this window.
- **Overall**: **WATCH** — advisory routing only, no auto-trade, no scoring/threshold/strategy changes.

## 13. Sources

- [US-Iran military escalation sends Bitcoin below $64K as crypto markets feel the heat](https://cryptobriefing.com/us-iran-strikes-bitcoin-crypto-market-drop/) — CryptoBriefing
- [Bitcoin retreats from monthly high as Iran attacks U.S. bases and profit-taking sets in](https://www.coindesk.com/markets/2026/07/16/bitcoin-pulls-back-to-usd64-000-after-hitting-monthly-high-as-bears-take-control) — CoinDesk, 2026-07-16
- [Latest Lorenzo Protocol News (BANK) — Future Outlook, Trends & Market Insights](https://coinmarketcap.com/cmc-ai/lorenzo-protocol/latest-updates/) — CoinMarketCap
- Internal: `data/reports/scalp/2026-07-19_18-45_scalp_report.md`, `data/reports/intraday/2026-07-19_18-51_intraday_report.md`, `data/catalysts/2026-07-19/catalyst_cycle_15-23.md`, `data/catalysts/2026-07-19/catalyst_events.jsonl`, `OPUS_ENRICHED_REVIEW_AUTO_2026-07-19_1914.md`

## 14. Fix Requests / TODO

### TODO-1: watchlist-alert → proposed_signal reuse/drop bug (carried forward, still open)
- **issue:** Telegram watchlist alerts fire for a symbol without minting a corresponding `proposed_signal`, so the tracker never sees them — PF/winrate/avgR undercounts affected symbols.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-19` → 5 instances today: ALLO/USDT (09:39, 11:36, 15:36), HOME/USDT (11:57), BANK/USDT (15:17). Identical count/symbols as the 19:14 review — unresolved, not worsening.
- **suggested manual fix:** investigate the watchlist-alert code path for the mint-on-alert step; likely re-fires on an existing/closed signal_id instead of minting a new one when the underlying candidate re-scores above the alert threshold within the same day.
- **priority:** high
- **first observed (this session's evidence chain):** 2026-07-17 (per prior project memory), reconfirmed 2026-07-19 21:53 EEST.

### TODO-2: ALLO/USDT and NEAR/USDT active-signals rows past their own expires_at
- **issue:** two rows in `active-signals` show `tp1_hit` while their `expires_at` timestamp is already in the past — ALLO/USDT by ~6.5h, NEAR/USDT (short) by ~2 days. Neither has been resolved to a terminal state (win/loss/flat/expired).
- **evidence:** `python -m src.cli active-signals --asset-class crypto` — ALLO/USDT `sig_10088a4c71cae845` expires_at 2026-07-19T15:21:04 (now 21:53); NEAR/USDT `sig_b16bb9e54598333a` expires_at 2026-07-17T15:56:12.
- **suggested manual fix:** check why the tracker's post-expiry resolution step is not closing these two rows — likely edge case in the tracker's expiry-sweep logic for signals that already hit TP1 before expiry.
- **priority:** medium
- **first observed:** 2026-07-19 21:53 EEST.

### TODO-3: weekend-mode observation text appears to contradict its own numbers
- **issue:** `signal-stats --asset-class crypto` prints the auto-observation "weekend=Y: weekend signals underperform (winrate 35%, n=38)" — but the same table shows weekend winrate 34.2% (13/38) is actually *higher* than weekday 26.1% (18/69), and weekend PF (1.98) is also higher than weekday PF (1.33). The "underperform" framing looks backwards relative to the printed numbers.
- **evidence:** `python -m src.cli signal-stats --asset-class crypto` → By weekend_mode table + observations block, this run.
- **suggested manual fix:** review the observation-generation logic's comparison baseline (may be comparing against a different reference window than the printed table, or the wording is simply mislabeled).
- **priority:** low
- **first observed:** 2026-07-19 21:53 EEST.

### TODO-4: UNH open C-tier positions have no internal legal-risk gate (carried forward)
- **issue:** two open C-tier invest-mode UNH longs carry an unresolved/widening DOJ legal-risk overhang that no internal scoring/tier gate currently reflects.
- **evidence:** active-signals stocks rows `sig_90b50ceef0d1ebd3`, `sig_4697b87c9845547f`; catalyst_events.jsonl UNH legal_risk entries (DOJ Medicare billing probe, multiple sources).
- **suggested manual fix:** consider a legal-risk overlay/flag at the tier level for symbols with an active `legal_risk` catalyst tag, surfaced in the report itself rather than relying on manual review discovery.
- **priority:** medium
- **first observed:** carried forward from prior reviews (2026-07-19 19:14 EEST session and earlier).
