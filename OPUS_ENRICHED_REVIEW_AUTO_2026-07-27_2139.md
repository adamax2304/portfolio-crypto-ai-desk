# Opus Enriched Review — late-session risk review — Auto Cycle 21:39 EEST

## 1. Executive Summary

- **Slot: late-session risk review** (21:30 EEST slot, fired ~21:39; US cash session still open, ~14:39 ET, closes ~23:00 EEST). Advisory only / no auto-trade.
- Crypto: price action still bullish (BTC/ETH uptrend, ~42.5% alt breadth above EMA20 as of 18:01 EEST snapshot) but macro headline risk remains elevated (94.3–100/100 risk-off score, Iran/Saudi/oil headlines) — same **mixed** picture as prior cycles: bullish tape, risk-off macro overhang.
- Stocks: **risk_off** confirmed (VIX 19.33, breadth 0% above EMA20, SPY/QQQ downtrend). **Zero A/B-tier actionable stocks setups this cycle** (headline sample=0) — every raw-A/B setup (NVDA, AVGO, GOOGL, META, QQQ, XLK, AMD, AMZN, TSLA, SMH, JPM, LLY, UNH, MSTR, PLTR) was gate-demoted to C. This is the 4th consecutive cycle today with zero stocks A/B actionable.
- **New this cycle — externally confirmed:** GOOGL's "legal/headline risk" demotion is a real, active securities-fraud investigation (Glancy Prongay Wolke & Rotter, Pomerantz, Frank R. Cruz) triggered by a Bloomberg report (2026-07-16) that Gemini 3.5 Pro is months behind schedule; GOOGL fell 4.4% same day, then Alphabet guided FY2026 capex up to $195–205B on 2026-07-22. Confirms the internal gate was correct to block this — not a false positive.
- **PUMP/USDT long (active swing, triggered, top idea) needs a chase-risk downgrade:** external research shows Pump.fun's $350–400M buyback program has **repeatedly failed to lift price** (multiple independent sources), and a 41%-of-supply unlock hit on 2026-07-12 — the "buyback" narrative surfacing in tonight's catalyst feed is not fresh bullish fuel, it's a recycled/weak narrative. Treat the open position as manage-only, not a reason to add.
- DEXE/USDT short (active B-tier swing, waiting_for_entry) is now **contradicted by fresh data**: this cycle's own scan downgraded a new DEXE short to C for "extreme negative funding against short" (squeeze risk, funding -0.0125 to -0.0147 across venues, crowding "elevated"). The existing waiting order should be treated with reduced confidence, not blindly held.
- Untracked-alert bug on DIA/USDT (2 alerts, no backing signal) is **unchanged** from the 18:39 review — same two timestamps, still unresolved. No new occurrence.
- Catalyst mapping this run: **67.1% unmapped** (weak) — use catalyst layer as context only.

## 2. Data Used

- Reports: scalp (17:51 EEST, no A/B, scalp kill-switched), intraday (18:01 EEST), swing (14:31 EEST — 7h old, carry-forward), stocks intraday (18:38 EEST — 3h old, still today's freshest stocks read).
- Stocks swing/invest: last generated 2026-07-02 — stale/deprecated per [[project_crypto_ai_desk_stocks_position_framework]], excluded.
- Catalyst/narrative: `data/catalysts/2026-07-27/catalyst_events.jsonl` (3500 events today), `narrative_baskets.jsonl`, latest cycle file `catalyst_cycle_18-05.md` (generated ~21:05 EEST, freshest data point this run).
- CLI: `active-signals` (crypto n=21, stocks n=50), `signal-stats` (crypto + stocks), `detect_untracked_legacy_alerts --since 2026-07-27`.
- DB reads: `db/crypto_ai_desk.sqlite` → `proposed_signals` (current levels for PUMP/DEXE/KAITO/ZAMA, 24h status-change counts by asset class).
- External: 2 WebSearch queries (GOOGL securities-fraud investigation, PUMP.fun buyback) + 1 WebFetch (GlobeNewswire GOOGL release, opened successfully).
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-27_1839.md` (18:39 EEST, US open reaction slot).

## 3. Scheduler / Data Freshness

- Latest scheduled-run folder: `data/scheduled_runs/2026-07-27_default_schedule/` — `scheduler.log` mtime 21:38 EEST (~1 min old). **Not deferred.**
- Latest `cycle_*_summary.md`: `cycle_01_17-46_summary.md` (mtime 18:40 EEST, ~3h old — the newer per-mode reports read directly above are fresher than this rolled-up cycle summary).
- Report freshness: scalp 3h48m old, intraday 3h38m old, swing 7h08m old (carry-forward per rule), stocks intraday 3h01m old.
- Monitor logs (crypto/derivatives/fast_news/mexc_canary/stocks/pending) all updated within the last few minutes — monitors alive, `pending_monitor` restarted at 20:41 (new PID file), consistent with normal fast-pending-monitor cycling per [[project_crypto_ai_desk_latency_layer]], not an outage.
- Stocks swing/invest: stale (25 days) — excluded, deprecated legacy mode.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-07-27 21:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["stocks swing/invest fresh data (deprecated, last 2026-07-02)", "live BTC/ETH price newer than 18:01 EEST snapshot"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 21:38 EEST", "swing report 7h08m old (carry-forward)", "catalyst cycle file 21:05 EEST is the freshest data point this run"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["mixed", "risk_off", "longs_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH uptrend, 42.5% alt breadth above EMA20, macro risk 94.3-100/100", "stocks: risk_off, VIX 19.33, breadth 0% above EMA20, SPY/QQQ downtrend"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["mapping_weak", "stale_catalyst", "catalyst_contradicted"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 1151/3500 = 32.9% mapped (67.1% unmapped)", "PUMP buyback narrative externally shown to be a repeated/stale, price-ineffective story, not a fresh bullish catalyst", "GOOGL legal risk externally confirmed and fresh (2026-07-16 to 2026-07-23 filings)"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["squeeze_risk", "oi_contradicts", "funding_extreme"],
      "data_missing": ["OI 24h for most fallback_via_mexc rows"],
      "suggested_effect": "advisory_only",
      "facts_used": ["DEXE/USDT funding -0.00125 (bybit) / -0.00147 (mexc), crowding 'elevated' — this cycle's own scan capped a fresh DEXE short to C for squeeze risk against the still-open waiting_for_entry short signal", "EUL/USDT similarly funding-negative/crowded"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["chase_risk", "overextended", "stale_before_entry"],
      "data_missing": ["TradingView/manual chart check unavailable — local OHLCV/ATR/EMA fields only"],
      "suggested_effect": "advisory_only",
      "facts_used": ["PUMP/USDT triggered at 0.00205-0.00207, current desk snapshot price ~0.0021 sits at/above entry, TP1 0.00214/TP2 0.00219/TP3 0.00226, stop 0.00202 — position is live and modestly in favor, not yet near TP1", "LA/USDT >2 ATR from EMA20 across all today's reports — do-not-chase repeatedly flagged"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "no_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto book now: 19 OPEN actionable (3 triggered + 11 tp1_hit + 5 tp2_hit), 2 WAITING for entry (DEXE short, ZAMA long)", "crypto 24h flow: 6 CLOSED WIN (tp3_hit), 17 CLOSED LOSS (stopped), 15 NO-ENTRY/STALE/MOVED-AWAY, 3 NEEDS REVIEW (expired, TP/SL status unclear from status field alone)", "stocks book now: 3 OPEN actionable B-tier legacy positions (AAPL/GOOGL/XOM, all tp2_hit, managing to close) — but 0 fresh A/B this cycle; 167 C-tier watchlist/research (not actionable)", "2 DIA/USDT untracked legacy alerts unchanged, still NEEDS REVIEW"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["GOOGL: securities-fraud investigation externally confirmed (Gemini 3.5 Pro delay, -4.4% on 2026-07-16, capex guidance raised to $195-205B on 2026-07-22) — AVOID confirmed", "UNH/TSLA legal flags carried forward unresolved from prior cycles, unchanged", "DEXE short-squeeze risk applies risk-manager caution to the existing waiting_for_entry short"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing PF 3.67/+34.7R (n=48, stronger) — best live cohort", "crypto scalp PF 0.10/-9.0R (n=43, 0 wins/11 losses) — confirmed losing, matches kill-switch/disabled status", "stocks C-tier week: PF 0.57, winrate 2.6% (n=189, triggered=76) — gates continue to look correctly protective"]
    },
    {
      "agent": "head_trader",
      "verdict": "watch_only",
      "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto swing remains the only strong live lane; manage existing book (PUMP, KAITO, AKE, and 11 tp1_hit positions), do not add new size into a stale-catalyst long or a squeeze-risk short", "Stocks: 4th straight cycle with zero A/B actionable — best short-watch stays NVDA/semis pending gate-clear; GOOGL now a confirmed avoid, not just gated", "Best long-watch = none clean fresh (existing PUMP position stands but should not be added to); best short-watch = NVDA; catalyst-watch = none fresh and clean this cycle (PUMP catalyst downgraded); avoid = GOOGL (confirmed) + UNH (confirmed) + DEXE new-entry chasing (squeeze risk)"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "mixed",
    "best_long_candidate": { "symbol": "none new — manage PUMP/USDT only", "trigger": "no new crypto long entries this window; PUMP already open, let it run to TP1 0.00214 or stop 0.00202, do not add", "reason": "No fresh clean long setup this cycle; all momentum leaders (LA, DIA, ZAMA, NIL) are either overextended (>2 ATR) or awaiting an unfilled pullback" },
    "best_short_candidate": { "symbol": "NVDA", "trigger": "RVOL clears the liquidity_rvol_below_min gate + any catalyst confirmation appears — still gated as of this cycle", "reason": "Raw-A score 92, semis sector remains the weakest (RS -15.4% vs SPY 20d), stocks regime risk_off" },
    "best_catalyst_candidate": { "symbol": "none clean", "trigger": "would need a genuinely fresh (not recycled) catalyst; PUMP's buyback story is stale and price-ineffective per external sources", "reason": "No candidate this cycle has both a fresh catalyst and clean technical entry" },
    "avoid_candidate": { "symbol": "GOOGL", "reason": "Externally confirmed active securities-fraud investigation (Gemini 3.5 Pro delay, -4.4% single-day move, capex guidance shock) — never actionable regardless of score until resolved" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.75 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.60 | mixed, risk_off, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, stale_catalyst, catalyst_contradicted | advisory_only |
| derivatives_squeeze | caution | 0.65 | squeeze_risk, oi_contradicts, funding_extreme | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, overextended, stale_before_entry | advisory_only |
| execution_lifecycle | ok | 0.70 | open_actionable, waiting_for_entry, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.75 | legal_risk, headline_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | watch_only | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-07-27_1839.md` (18:39 EEST):
- PUMP/USDT moved from "watch, wait for pullback" to **triggered/open** (entered 18:34 UTC, within the same hour as the last review) — now a manage-only position, not an entry decision. New external research downgrades confidence: the "buyback" catalyst surfacing in tonight's feed is the same recycled $350-400M story that has repeatedly failed to move price, plus a 41% supply unlock already occurred 2026-07-12.
- DEXE/USDT is newly relevant: unchanged as an open waiting_for_entry B-tier short, but this cycle's fresh scan explicitly downgraded a new DEXE short to C for extreme negative funding / squeeze risk — a genuine contradiction between the still-open older signal and the freshest read on the same symbol.
- GOOGL: was mentioned only implicitly before; now confirmed externally as a real, active securities-fraud investigation (not just an internal gate flag) — upgraded from "gated" to "confirmed avoid."
- NVDA best-short-watch thesis is unchanged (still gated on liquidity_rvol_below_min).
- DIA/USDT untracked-alert bug: unchanged, same 2 alerts (12:44:33 / 14:30:33 UTC), still unresolved — no new occurrence this cycle.
- UNH/TSLA avoid/manual-review status carried forward unchanged.
- Catalyst mapping improved slightly in relative terms but is still weak: 67.1% unmapped this run vs 68.2% at 18:39.

## 5. Catalyst Coverage

- Total catalyst events today: **3500**; mapped (non-null symbol): **1151** (32.9%); unmapped: **2349 (67.1%)**.
- Narrative baskets active (per `catalyst_cycle_18-05.md`, ~21:05 EEST): delisting_thin_liquidity, rwa_narrative (ONDO, XLM), perps_dex_narrative (HYPE + DYDX/GMX/ASTER), momentum_breakout (LA, ZAMA, PUMP, related NIL).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top unmapped headlines (geopolitical/macro, no ticker to attach): Israel-Iran ceasefire talks (N12/Barak Ravid), Qatar/Pakistan-mediated US-Iran negotiations, Romania drone-shootdown cost report — these are macro-only items with no natural symbol, not resolver failures in the traditional sense.

## 6. Market Landscape

Crypto: BTC/ETH both in uptrend as of the 18:01 EEST intraday snapshot (freshest technical read this cycle), altcoin breadth 42.5% above EMA20, volatility normal (ATR percentile 19). Desk style: mean reversion / wait for clean breakouts. Momentum leaders (LA, ZAMA, PUMP, BANK short, EUL short, DEXE short, NIL, AERO) are almost entirely **without a fresh verified catalyst** — pure RS/momentum trades. Crypto scalp mode remains kill-switched (0 wins / 11 losses, PF 0.10 over 14d) and produced zero A/B ideas again this cycle.

Stocks: regime risk_off, VIX 19.33, 0% of tracked symbols above EMA20, SPY/QQQ downtrend. Sector rotation into energy/financials/healthcare, out of semis/tech (SMH RS -15.4% vs SPY 20d). Fifteen raw-A/B setups this cycle (NVDA, AVGO, GOOGL, META, QQQ, XLK, AMD, AMZN, TSLA, SMH, JPM, LLY, UNH, MSTR, PLTR) were **all** demoted to C by liquidity/sector/catalyst/legal gates — zero A/B actionable, 4th straight cycle today.

### Market Mood / Risk Routing
- Crypto mood: **mixed** (bullish price action, risk-off macro overhang — Iran/Saudi/oil headlines, macro risk score 94-100/100)
- Stocks mood: **risk_off** (VIX 19.33, breadth 0%, downtrend indices, sector rotation into defensives)
- Dominant narrative: crypto RS-leader momentum rotation without fresh catalyst backing; PUMP's buyback narrative is stale/ineffective, not fresh fuel
- Preferred side now: crypto — manage existing swing book only, no new adds; stocks — no clean actionable side, watch NVDA/semis for gate-clear
- Best long candidate: none new — manage open PUMP/USDT position only
- Best short candidate: NVDA (gated, watch for liquidity/catalyst confirmation)
- Best catalyst-backed candidate: none clean this cycle
- What to avoid: GOOGL (confirmed securities-fraud investigation), UNH (confirmed DOJ risk + earnings tomorrow), new DEXE short entries (squeeze risk against negative funding), chasing PUMP above current level
- What would change the view: a genuine 1h close confirming a fresh crypto pullback entry with volume, or NVDA/semis clearing liquidity+catalyst gates with a real confirmation, or the DEXE funding profile normalizing before the waiting order fills

## 7. Candidate Deep Dives

### 1. GOOGL (stocks, short, raw-A demoted to C, score 87.06)
- Has price already reacted to the catalyst? Yes — the triggering Gemini 3.5 Pro delay news broke 2026-07-16 (stock -4.4% same day); today's news flow (Alphabet/YouTube Peacock deal, CAPEX commentary) is secondary chatter, not the primary catalyst.
- Is the setup chasing? N/A — not actionable; internal gate already blocks it (`legal_headline_risk: class_action`, plus `stale_post_earnings_setup` since the 2026-07-27T10:45 earnings print invalidates pre-earnings technical levels).
- Retest/pullback structure? N/A — blocked regardless of technicals.
- Overextended >2 ATR? Not the blocking reason; legal risk overrides.
- Would entry now be late? N/A — never actionable while the investigation is open.
- What level makes it actionable? None on legal grounds; would need the investigation to resolve/settle AND fresh post-earnings technical levels to be established.
- Aligned with market mood? Stocks risk_off would support a short bias generically, but this specific setup is blocked on legal grounds, not technicals — do not use technicals to justify entry here.
- Long/short/wait? N/A — avoid.
- Chase-risk? N/A.
- Catalyst confirmation/contradiction? **Confirmed externally**: multiple law firms (Glancy Prongay Wolke & Rotter, The Law Offices of Frank R. Cruz, Pomerantz LLP) are actively investigating securities-fraud claims tied to the Gemini delay disclosure and the subsequent capex guidance expansion to $195-205B (2026-07-22).
- **LEGAL/HEADLINE RISK: confirmed, verdict = AVOID / MANUAL REVIEW REQUIRED.**

### 2. NVDA (stocks, short, raw-A demoted to C, score 92.08)
- Has price already reacted? Semis sector is already the weakest (RS -15.4% vs SPY 20d) — an established trend, not a fresh break.
- Chasing? Possible if entered now without confirmation — SI-gates are blocking on `liquidity_rvol_below_min` and `catalyst_none_and_not_exceptional_technical`, i.e., volume/catalyst confirmation is judged insufficient, not that the thesis is wrong.
- Retest/pullback structure? **TradingView/manual chart check unavailable** — using only local OHLCV/ATR/EMA fields from the report (none surfaced beyond the score table for this candidate this cycle).
- Overextended >2 ATR? Not flagged.
- Would entry now be late? Late session (US close in ~1.3h) — a fresh short entry now with no catalyst confirmation is low-quality regardless of gate status; better suited to tomorrow's session open.
- What makes it actionable? RVOL clearing the minimum threshold + a genuine catalyst appearing.
- Aligned with mood? Yes — risk_off stocks regime + weakest sector supports a short bias.
- Chase-risk? Yes if forced late-session without confirmation.
- Catalyst confirmation/contradiction? No fresh NVDA-specific catalyst found internally or externally this pass.
- **Verdict: WATCH — best short-watch candidate, not actionable this cycle; low urgency this late in the session.**

### 3. PUMP/USDT (crypto, long, B-tier swing, triggered 18:34 UTC — currently the only fresh crypto long this cycle)
- Has price already reacted to the catalyst? The "buyback" narrative appearing in tonight's catalyst feed ("Pump.fun reclaims $0.0020 – Can $414M in buybacks sustain PUMP's rally?") refers to the same $350-400M buyback program that multiple independent sources confirm has **repeatedly failed to lift the token's price** — this is not fresh bullish fuel, it is a recycled, already-priced-in story. A 41%-of-supply unlock also hit on 2026-07-12, adding structural selling pressure the "buyback" framing does not offset.
- Is the setup chasing? Entry filled at 0.00205-0.00207; current desk snapshot (18:01 EEST) shows price ~0.0021, i.e., at or slightly above entry — the position is live, modestly in favor, not yet extended into TP territory.
- Retest/pullback structure? Already filled; no retest needed now — position is open and being managed toward TP1 0.00214 / TP2 0.00219 / TP3 0.00226, stop 0.00202.
- Overextended >2 ATR? Not flagged for the swing entry itself; LA/USDT (a related momentum name) is the one flagged as overextended, not PUMP.
- Would entry now be late? Yes for a **new** entry — do not add to this position; it is already filled.
- What would invalidate the idea? 1h close beyond stop 0.00202 (below invalidation) or BTC breaking regime support.
- Aligned with market mood? Marginally — fits "selective longs" style, but the catalyst backing is now known to be weaker than the report's "no fresh verified catalyst detected" framing suggested (it's not just absent, it's actively been shown ineffective).
- Actionable now or after confirmation? Already active — manage-only, not an entry decision.
- Chase-risk? Not for the existing position; high for anyone considering adding at current levels.
- Catalyst confirmation? **Contradicted** — external sources show the buyback narrative has not driven sustained price gains; treat this as a technical/RS trade, not catalyst-backed.
- **Verdict: MANAGE ONLY — hold to TP1/stop as planned, do not add size, do not treat the buyback headline as a reason for conviction.**

### 4. DEXE/USDT (crypto, short, B-tier swing, waiting_for_entry — entry 2.7646-2.8741, invalidation 3.0079)
- Has price already reacted? Yes — 24h move -24.4% as of the 18:01 EEST snapshot, a large move already in progress; the swing order (proposed earlier today, updated 15:21 UTC) is waiting for price to retrace up into the 2.7646-2.8741 entry zone before triggering.
- Is the setup chasing? No — it is a limit-style waiting order into a bounce/retest zone, not a market chase.
- Retest/pullback structure? Yes by design — waiting for a bounce into the entry zone on a failed-bounce-short thesis.
- Overextended >2 ATR? Not the current concern; the concern is derivatives-based.
- Would entry now be late? N/A — order has not filled.
- What would invalidate the idea? 1h close beyond invalidation 3.0079, or the negative-funding squeeze thesis worsening further.
- **Aligned with market mood? Increasingly no.** This cycle's fresh intraday scan explicitly capped a *new* DEXE short at score 46.3 for "extreme negative funding against short" — funding is -0.00125 (bybit) to -0.00147 (mexc), crowding flagged "elevated" on external venues. Shorts are already crowded and paying heavily to stay short; a squeeze (sharp bounce that stops out latecomer shorts) is a real, currently-flagged risk on this exact symbol.
- Chase-risk? Not chase-risk in the traditional sense, but **squeeze-risk on the short side** if the waiting order fills into the bounce zone right as short crowding is already extreme.
- Catalyst confirmation/contradiction? No fresh news/catalyst found internally (0 news_items hits in the last 24h) — this is a pure technical/derivatives trade, and the derivatives read has turned against the thesis since the order was placed.
- **Verdict: CAUTION / DOWNGRADE CONFIDENCE — the still-open waiting order is not automatically wrong, but the system's own fresh read on the same symbol now argues against a new short here; if it fills, size down or tighten management given confirmed squeeze risk.**

### 5. KAITO/USDT (crypto, long, B-tier swing, tp1_hit — weekend_mode flag Y, expires 2026-08-02)
- Has price already reacted? Yes — TP1 (1.2157) was already hit (updated 06:17 UTC today); position is now managing the TP1-to-TP3 leg (TP2 1.2562, TP3 1.3088) with stop typically moved to protect gains per the desk's profit-protection model (see [[project_crypto_ai_desk_viable_core]] Model F: BE@+0.6R, lock+0.5R@+1R).
- Is the setup chasing? N/A — already in profit-management phase.
- Retest/pullback structure? N/A at this stage.
- Overextended? Not flagged.
- Would entry now be late? N/A — position already open.
- What would invalidate/what's the risk into the weekend? This position carries the `weekend_mode=Y` flag; per prior signal-stats, weekend-flagged signals underperform (31% winrate, n=17) relative to weekday (reliable cohort). With the position already at TP1 and stop presumably protected, weekend-hold risk is lower than a fresh weekend entry would be, but it is still a name to monitor into the Asia session given the weekend-underperformance pattern.
- Aligned with mood? Yes — momentum long fits the current crypto style; already validated by TP1.
- Chase-risk? None — managing an existing winner.
- Catalyst confirmation/contradiction? No specific catalyst tracked for KAITO this cycle; this is a momentum/RS trade already de-risked by the TP1 hit.
- **Verdict: MANAGE — let the trailing TP2/TP3 structure play out; no new action needed, but flag for the weekend-underperformance pattern if held into Saturday.**

## 8. Best Candidates Ranked

1. **Manage-only (long): PUMP/USDT** — already triggered; hold to TP1 0.00214/stop 0.00202, do not add, buyback catalyst is stale/ineffective per external check.
2. **Short-watch: NVDA** — trigger: RVOL clears liquidity gate + catalyst confirmation; low urgency this late in the session, more relevant for tomorrow's open.
3. **Manage-only (short, reduced confidence): DEXE/USDT** — waiting order 2.7646-2.8741; fresh derivatives read argues against new shorts here (squeeze risk) — if it fills, manage tighter than plan.
4. **Manage-only (long, de-risked): KAITO/USDT** — TP1 already hit, let TP2/TP3 structure run; watch weekend-hold pattern.
5. **Avoid (confirmed): GOOGL** — active securities-fraud investigation, externally verified.
6. **Avoid (confirmed, carried forward): UNH** — DOJ Medicare investigation, earnings tomorrow (2026-07-28).
7. **Monitor-only (already open, do not add): 11 tp1_hit + 5 tp2_hit crypto positions** (ONDO, OPN, FIL, KITE, ZAMA×3, ADA, VIRTUAL, PENGU, ALLO, PUMP-intraday, KAITO-intraday) — manage TP/SL only, no new entries.

## 9. Avoid / No Trade

This applies to the **current decision window only** — scanning, tracking, and monitors continue regardless.
- GOOGL: confirmed active securities-fraud investigation (Gemini delay, capex guidance shock).
- UNH: confirmed DOJ Medicare billing investigation + earnings tomorrow.
- TSLA: unresolved internal `going_concern` legal flag, carried forward as manual-review, not confirmed clean or blocked.
- New DEXE/USDT shorts beyond the already-placed waiting order: extreme negative funding / squeeze risk flagged by this cycle's own fresh scan.
- Adding to the open PUMP/USDT long: entry has filled, catalyst backing is weaker than initially framed.
- Any late-session (< 1.5h to US close) fresh stocks entry: nothing is A/B actionable, and even gate-clearing candidates like NVDA are lower-quality this close to the bell.

## 10. Main Risks

- Macro/geopolitical headline risk remains elevated (94-100/100): Iran/Saudi/oil headlines, unresolved ceasefire negotiations reported this cycle — any escalation could flip the crypto risk-on tape quickly against the open PUMP long.
- Catalyst mapping is weak this run (67.1% unmapped) — do not over-weight the catalyst layer for new decisions.
- Two confirmed/flagged legal-risk stocks in view (GOOGL now confirmed, UNH confirmed, TSLA ambiguous) — avoid new exposure to all three regardless of score.
- DEXE/USDT squeeze risk: the existing waiting_for_entry short could fill directly into a crowded-short bounce; this is a genuine internal contradiction (old signal vs. fresh scan) worth operator attention, not a system bug.
- Stocks C-tier week performance remains weak (PF 0.57, winrate 2.6%, n=189) — the demotion gates are, on net, correctly protective; no reason to second-guess them this cycle.
- Untracked-alert bug on DIA/USDT is unresolved (unchanged from 18:39 review) — a data-quality gap in PF/winrate tracking, not a live-trading risk.

## 11. Action Plan — next 4 hours

- Manage PUMP/USDT to TP1 0.00214 or stop 0.00202; do not add size on the recycled buyback narrative.
- Manage KAITO/USDT toward TP2/TP3; monitor for weekend-hold risk if still open into Saturday.
- Hold the DEXE/USDT waiting order as-is (do not cancel unilaterally — that is a strategy change outside this review's scope) but treat any fill with reduced confidence given the fresh squeeze-risk read; flag for manual reduction if desired.
- No new stocks entries into the close — zero A/B actionable, and even NVDA/semis is low-priority this late in the session; re-evaluate at tomorrow's pre-US-open slot.
- Continue monitoring the 11 tp1_hit / 5 tp2_hit crypto positions for TP/SL management only.
- Manual session should verify the DEXE funding/squeeze read against the still-open waiting order and decide whether to reduce planned size before it fills.

## 12. Final Verdict per Mode

- **Crypto scalp:** No trade (kill-switch disabled; PF 0.10/-9.0R last 14d, 0 wins/11 losses — confirmed losing mode).
- **Crypto intraday:** Watchlist only — no A/B this cycle; momentum leaders lack fresh catalyst or are overextended.
- **Crypto swing:** Best live lane (PF 3.67/+34.7R, n=48) — manage the open book (PUMP, KAITO, AKE×2, DEXE waiting) only; no new adds this window.
- **Stocks intraday:** No trade — zero A/B actionable, 4th straight cycle; GOOGL now confirmed-avoid (not just gated); watch NVDA/semis for tomorrow.
- **Stocks swing/invest:** Deprecated/stale (last report 2026-07-02) — not evaluated this cycle.

## 13. Sources

- [Securities Fraud Investigation Into Alphabet Inc. (GOOG) Continues (GlobeNewswire, 2026-07-21)](https://www.globenewswire.com/news-release/2026/07/21/3330169/34548/en/Securities-Fraud-Investigation-Into-Alphabet-Inc-GOOG-Continues-Shareholders-Who-Lost-Money-Urged-To-Contact-Glancy-Prongay-Wolke-Rotter-LLP-a-Leading-Securities-Fraud-Law-Firm.html)
- [Securities Fraud Investigation Into Alphabet Inc. (GOOG) Announced (BusinessWire, 2026-07-16 origin)](https://www.businesswire.com/news/home/20260716231796/en/Securities-Fraud-Investigation-Into-Alphabet-Inc.-GOOG-Announced-Shareholders-Who-Lost-Money-Urged-To-Contact-The-Law-Offices-of-Frank-R.-Cruz)
- [INVESTOR ALERT: Pomerantz Law Firm Investigates Claims On Behalf of Investors of Alphabet Inc. - GOOG (PR Newswire)](https://www.prnewswire.com/news-releases/investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-alphabet-inc---goog-302831970.html)
- [Pump.fun $350 Million PUMP Buybacks Fail To Lift Token Price (ainvest.com)](https://www.ainvest.com/news/pump-fun-350-million-pump-buybacks-fail-lift-token-price-2604/)
- [Pump.fun's $400M Token Buyback Fails To Ignite PUMP Price Rally (bitcoinworld.co.in)](https://bitcoinworld.co.in/pump-fun-400m-buyback-limited-price-gains/)
- [Pump.fun spends $350M on buybacks but token still 81% below peak (Dealroom.co)](https://app.dealroom.co/news/feed/pump-fun-spends-350m-on-buybacks-but-token-still-81-below-peak)

## 14. Fix Requests / TODO

### TODO-untracked-dia-alert (status check, unchanged)
- **issue:** Untracked-legacy-alert detector still shows the same 2 DIA/USDT watchlist alerts (intraday 12:44:33 UTC, swing 14:30:33 UTC) with no matching proposed_signal within 6h — no new occurrence this cycle, same instance as reported at 18:39 EEST.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-27` output identical to prior cycle; see [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]] (TODO-3, high priority, first raised 2026-07-17).
- **suggested manual fix:** No change from prior recommendation — confirm root cause (stale/closed signal_id reuse on watchlist re-fire) and check whether it recurs on a 4th symbol in coming cycles.
- **priority:** high
- **first observed:** 2026-07-17 (this instance unchanged since 2026-07-27 18:39 EEST)

### TODO-dexe-signal-derivatives-contradiction
- **issue:** The open DEXE/USDT B-tier swing short (waiting_for_entry, entry 2.7646-2.8741, placed ~15:21 UTC today) is now contradicted by the same day's later scans, which cap a *new* DEXE short to C-tier for "extreme negative funding against short" (squeeze risk). There is no automated mechanism to re-flag or auto-adjust an already-placed waiting order when the derivatives picture for the same symbol deteriorates intraday.
- **evidence:** `proposed_signals` row `sig_d952be91201d7a27` (waiting_for_entry, updated 2026-07-27T15:21:27Z) vs. `data/reports/intraday/2026-07-27_18-01_intraday_report.md` §7b rejected-not-ready row: "DEXE/USDT: score 46.3 (short) — extreme negative funding against short."
- **suggested manual fix:** Consider whether waiting_for_entry orders should be re-scored (or at minimum flagged) against the latest derivatives read each cycle, rather than only checked against price for fill/expiry — a policy/product decision, not a quick code fix.
- **priority:** medium
- **first observed:** 2026-07-27 21:39 EEST

## Telegram

```
[AUTO-REVIEW late-session risk review 21:39 EEST]

Mood:
- Crypto: mixed (bullish price action, risk-off macro overhang)
- Stocks: risk_off
- Prefer: manage existing crypto swing book / stocks wait-for-trigger

Status:
- Open actionable: 19 (crypto: 3 triggered + 11 tp1_hit + 5 tp2_hit) + 3 (stocks legacy B, tp2_hit)
- Waiting for entry: 2 (crypto: DEXE short, ZAMA long)
- Review/Shadow: 167 (stocks C-tier watchlist, not actionable)
- Entered unresolved: included in open actionable above
- No-entry/stale/moved-away: 15 (crypto, 24h) + 51 (stocks, 24h)
- Needs review: 2 (DIA/USDT untracked legacy alerts, unchanged) + 3 (crypto expired, TP/SL status unclear)

Decisions:
- Long-watch:     none new — manage PUMP/USDT (triggered) to TP1 0.00214 / stop 0.00202
- Short-watch:    NVDA trigger RVOL clears liquidity gate + catalyst confirmation (low urgency, US close ~1.3h away)
- Catalyst-watch: none clean — PUMP buyback narrative confirmed stale/ineffective externally
- Avoid:          GOOGL (confirmed securities-fraud investigation); UNH (confirmed DOJ + earnings tomorrow)

Risk:
- DEXE/USDT waiting short (2.7646-2.8741) now contradicted by fresh extreme-negative-funding squeeze risk on the same symbol

Catalyst coverage: mapped 1151/3500 (32.9%), baskets 4
                   weak this run — context only

File: OPUS_ENRICHED_REVIEW_LATEST.md
Advisory only. No auto-trade.
```
