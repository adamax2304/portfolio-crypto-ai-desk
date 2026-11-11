# Opus Enriched Review — Europe / Pre-US Context — Auto Cycle 11:30 EEST

## 1. Executive Summary

Slot: **Europe / pre-US context** (11:30 EEST, 2026-07-23). **Advisory only — no auto-trade, no scoring/strategy changes.** Crypto has cooled from the overnight risk-on read: BTC has slipped from uptrend into **range**, ETH still holds an uptrend, and the intraday/scalp regime reads **transition (mixed)** — while the (5.5h-old, carry-forward) swing report still reads **bullish trend (risk-on)**, so treat the swing-timeframe bullishness with a freshness caveat. No new A/B setups fired in scalp or intraday this cycle; the crypto book still carries 5 open/triggered B-tier longs (ERA, RE, EPIC, BANK, TLM) plus 3 waiting-for-entry, with the rest already partially booked (tp1/tp2). The cross-chain exploit-hack cluster from the overnight review has **worsened**, not resolved — Lookonchain is now calling it "Hackers' Day" with three same-day exploits (AFX Trade, a new VerusCoin Ethereum bridge hit, plus the Arbitrum bridge incident) touching ETH/ARB. Stocks remain closed pre-open (chop regime, VIX 16.64); best planning longs are XOM/AVGO/NVDA/AMD, best planning shorts are META/XLV/PLTR — none actionable until RTH confirmation. GOOGL and LMT report earnings today — do not chase. UNH's DOJ Medicare-billing investigation remains open and unchanged (avoid/manual-review, no update in 7+ days). Catalyst mapping is still weak this run (79% unmapped, same resolver bug flagged last cycle — now confirmed persisting). Scanning, tracking, and monitors continue regardless of this review's caution stance.

## 2. Data Used

- Crypto reports: `2026-07-23_05-29_scalp_report.md` (mtime 08:29, ~3.2h old, fresh), `2026-07-23_05-37_intraday_report.md` (mtime 08:37, ~3.0h old, fresh)
- Swing report: `2026-07-23_03-05_swing_report.md` (mtime 06:05, ~5.5h old — **carry-forward**, 4-12h bucket, used with caution flag; regime divergence noted vs intraday)
- Stocks intraday: `2026-07-23_06-05_stocks_intraday_report.md` (mtime 09:05, ~2.5h old, fresh — market closed, planning-only)
- Stocks swing/invest: last available `2026-07-02_13-0x` reports (**~21 days stale**, unchanged from last review — see §14 TODO-2, not used for any decision)
- Catalyst layer: `data/catalysts/2026-07-23/catalyst_events.jsonl` (1000 cumulative rows today), `narrative_baskets.jsonl` (4 baskets), `catalyst_cycle_05-41.md`
- LLM packets: `llm_analysis_packet.md` (crypto, mtime 08:38), `llm_stocks_packet.md` (stocks, mtime 09:09)
- CLI: `active-signals` (crypto ×26, stocks ×50), `signal-stats` (crypto + stocks), `detect_untracked_legacy_alerts --since 2026-07-23` (clean — no untracked alerts)
- Direct read-only SQL against `db/crypto_ai_desk.sqlite` (`news_items`) — computed catalyst mapped/unmapped ratio directly from the JSONL, and checked for fresh UNH DOJ-investigation news in the last 48h (none found — confirms stale/unchanged)

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: 2026-07-23 11:22 (fresh, ~17min old at read time)
- Latest cycle summary: `cycle_04_08-21_summary.md` (~3.3h old) — within the 3h defer threshold at the margin; review proceeds (not deferred)
- `derivatives_monitor`, `pending_monitor` logs updating within the last hour — monitors alive
- Crypto scalp/intraday reports fresh (~3h)
- Swing report carry-forward (~5.5h) — used for context but flagged, given its regime read (bullish) diverges from the fresher intraday/scalp read (mixed/transition)
- Stocks intraday fresh (~2.5h), market closed (pre-open) — all candidates planning-only per the report's own header
- Stocks swing/invest ~21 days stale — **not used** for any candidate this run (TODO-2, unchanged)
- Catalyst scan already present for today (`catalyst_cycle_05-41.md`, generated 08:41) — no need to re-run the CLI

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-07-23 11:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["scheduler_fresh", "report_stale", "derivatives_sparse"],
      "data_missing": ["stocks swing/invest reports ~21d stale", "exact triggered_at timestamps for open crypto signals"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 11:22 (~17min)", "cycle_04 summary mtime ~3.3h old (borderline vs 3h defer threshold, proceeded)", "swing report mtime ~5.5h (carry-forward)"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mixed", "chop", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC trend now range (was uptrend at 04:30), ETH still uptrend, altcoin breadth 60.5% above EMA20 (down from 73.7% at 04:30)", "swing report (stale-ish) still reads bullish trend/risk-on — regime divergence across timeframes", "stocks regime = chop, neutral, VIX 16.64, market closed"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.35,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"],
      "data_missing": ["accurate symbol resolution for funding-rate/listing notices — same defect as last cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["1000 cumulative catalyst events today, 209 mapped (20.9%) / 791 unmapped (79.1%) — confirmed via direct JSONL read", "rwa_narrative basket (ONDO, XLM) fresh <1h with a real primary-source-adjacent headline (tokenized stocks as collateral)", "ai_narrative basket still headline-mismatched (top sample is an Iran-strike geopolitical item, not AI-sector news)"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.4,
      "reason_codes": ["data_unavailable", "oi_supports"],
      "data_missing": ["long/short ratio for most watchlist names", "OI history beyond 24h"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BANK/USDT funding ~flat, OI +10-30% depending on mode read, price up + OI up (fresh positioning)", "ZAMA/USDT funding negative (-0.00016), OI +29.7%, crowding normal", "ERA/USDT price up + OI down (short covering, weaker continuation quality) across both intraday and swing reads"] },
    { "agent": "technical_entry", "verdict": "watch", "confidence": 0.5,
      "reason_codes": ["chase_risk", "stale_before_entry", "overextended"],
      "data_missing": ["structured chart/TradingView confirmation — not available this run"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BANK/USDT swing thesis explicitly flags 'chase risk after a vertical 24h move' as its known failure mode, and 7d return is +346.65% — parabolic", "TLM/USDT and ZAMA/USDT top today's intraday C-tier watchlist and are also the momentum_breakout basket primaries, but both explicitly no-catalyst", "prior cycle's AKE/USDT and WLFI/USDT long/short watch ideas have both dropped out of today's strongest/weakest lists — faded, do not carry forward"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.6,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 5/26 open_actionable (triggered, within window: ERA-intraday, RE-swing, EPIC-swing, BANK-swing, TLM-intraday), 3/26 waiting_for_entry (ZAMA-intraday, BANK-intraday, ERA-swing), 18/26 entered_unresolved (tp1/tp2_hit, past expiry, no final resolution shown)", "stocks: 13/50 open_actionable (invest-mode, expiry 2026-07-31/08-01), 21 C-tier planning-only (market closed), ~37 entered_unresolved/past-expiry (mostly historical intraday tp1/tp2_hit)", "GOOGL and MSFT specifically flagged needs_review (post-earnings stale setup / active legal flag)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["legal_risk", "headline_risk", "correlation_cluster", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: DOJ Medicare-billing investigation confirmed 2026-07-16/17, no update in the last 48h (checked directly via SQL) — 8th consecutive cycle unchanged", "MSFT: active securities_fraud legal flag (system-tagged, no specific headline cited in the report), tier demoted B->C", "LLY: legal_risk flag — Novo Nordisk GLP-1 lawsuit headline (Motley Fool, 2026-07-22)", "GOOGL: verified earnings print 2026-07-22T20:35:42 UTC while calendar is UNKNOWN — pre-earnings levels invalid, stale_post_earnings_setup, manual review required; LMT also reports earnings today", "exploit-hack cluster worsened: AFX Trade ($24.15M), new VerusCoin Ethereum bridge exploit (~$7.55M), Arbitrum bridge incident — Lookonchain labels it 'Hackers Day', 3 exploits same window, touching ETH/ARB"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto week: A/B headline sample=173, winrate 25.3%, PF 1.67, totalR +30.21 — swing mode drives it (PF 2.91, totalR +21.01, n=48) while scalp mode is reproducibly losing (PF 0.72, avgR -0.09, totalR -3.10, n=44)", "crypto short direction: PF 0.125, 0W/6L (n=8, anecdotal but consistently bad)", "stocks week: A/B headline sample=0 (no A/B actionable this week), C-tier watchlist PF 0.958, avgR -0.0094, totalR -0.50 (n=206) — flat/slightly negative", "stocks-intraday paper diagnostics: 'no_gate_context' failure bucket alone accounts for -405.00R over 726 rows in the last 14d — the single largest avoidable-loss bucket in the system"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.55,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.55,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": { "symbol": "TLM/USDT", "trigger": "1h close and hold above 0.0020 (top of conditional pullback zone) on confirming volume (currently 1.21x, needs >1.5x); invalidate on 1h close below 0.0018", "reason": "top-scored (56.0) crypto watchlist idea this cycle, also the highest-ranked primary of the fresh (<1h) momentum_breakout basket, but explicitly a no-catalyst play — known failure mode is no-catalyst intraday momentum in chop (14d: WR 23%/PF 0.70/-3R), needs breakout/RS confirmation before treating as live" },
    "best_short_candidate": { "symbol": "DEXE/USDT", "trigger": "wait for a failed bounce / breakdown continuation with volume confirmation — no formal entry/ATR structure published this cycle; do not short the already-realized -20.21% move without a retest", "reason": "weakest symbol in today's intraday scan (24h -20.21%, RS -19.91% vs BTC) but crypto short-direction has a consistently poor edge this week (PF 0.125, 0W/6L, n=8) — treat any short here with extra scrutiny, this is a watch-only routed pick, not a confirmed setup" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT", "trigger": "confirm the rwa_narrative basket thesis (tokenized-stocks-as-collateral headline, fresh <1h) with RS/technical follow-through before treating as active; currently watchlist/basket-primary only, no formal Trade Idea published this cycle", "reason": "cleanest catalyst-backed name this window — real, dated headline (network use of tokenized stocks as collateral) rather than a pure momentum/no-news play, though verification_status is single_source, not primary_source" },
    "avoid_candidate": { "symbol": "UNH", "reason": "live DOJ criminal+civil Medicare-billing investigation (confirmed 2026-07-16/17, no update since, re-checked via direct SQL this run) overrides technical/invest-mode score; manual review required, unchanged for 8+ consecutive cycles" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 6
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.60 | scheduler_fresh, report_stale, derivatives_sparse | advisory_only |
| market_regime | caution | 0.50 | mixed, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.35 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.40 | data_unavailable, oi_supports | advisory_only |
| technical_entry | watch | 0.50 | chase_risk, stale_before_entry, overextended | advisory_only |
| execution_lifecycle | needs_review | 0.60 | open_actionable, waiting_for_entry, entered_unresolved, needs_review | advisory_only |
| risk_manager | caution | 0.65 | legal_risk, headline_risk, correlation_cluster, reduce_risk | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.55 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

(vs `OPUS_ENRICHED_REVIEW_AUTO_2026-07-23_0448.md`, 04:48 EEST cycle)

- **Faded:** AKE/USDT (previous best-long-watch) and WLFI/USDT (previous best-short-watch) — neither appears in today's strongest/weakest-symbols lists or watchlist ideas. Both theses are stale; do not carry forward.
- **Regime cooled:** BTC shifted from **uptrend** (04:30) to **range** (11:30); altcoin breadth above EMA20 dropped from 73.7% to 60.5%. The intraday/scalp regime label moved from an implicit risk-on lean to explicit **transition (mixed)**. The swing report still reads bullish/risk-on, but it is now the more-stale of the two reads — a genuine timeframe divergence, not just a caveat repeated from last time.
- **Worsened:** the cross-chain exploit-hack cluster grew. The 04:48 review listed three incidents (Arbitrum $24M, AFX Trade $24.15M, Wanchain Cardano-BNB $9M). This cycle's catalyst scan adds a **new** VerusCoin Ethereum bridge exploit (~$7.55M) and Lookonchain is now framing the day as "Hackers' Day" (three exploits, $35.55M combined per that source) — the risk has not resolved, it has compounded.
- **Unchanged:** UNH avoid/manual-review stance — DOJ investigation still open, re-verified via direct SQL query, no news in the last 48h. Now flagged across 8+ consecutive cycles.
- **Unchanged/confirmed:** RE/USDT, EPIC/USDT, BANK/USDT, ERA/USDT all remain open (triggered) in swing/intraday — no new information, tracking only.
- **Unresolved (recurring):** catalyst symbol-resolver defect (TODO-1 from last review) — unmapped rate is 79.1% this cycle vs 78.0% last cycle, essentially unchanged. This is now the **second consecutive run** with specific evidence (`RIFUSDT`, `BNCUSDT`, `WOODUSDT`, `FWDIUSDT`, `BOTUSDT` tickers spelled out literally but resolved to null) — see §14 TODO-1, escalating supporting evidence.
- **New this cycle:** GOOGL reported earnings after yesterday's close (2026-07-22T20:35:42 UTC) — its stocks-intraday A-tier setup (score 84) is now correctly demoted to C for `stale_post_earnings_setup`, requiring fresh post-earnings levels before any re-entry consideration.

## 5. Catalyst Coverage

- Total catalyst events today (cumulative JSONL): **1000**
- Mapped (non-null symbol): **209 (20.9%)**
- Unmapped: **791 (79.1%)**
- Narrative baskets: **4** (rwa_narrative, perps_dex_narrative, ai_narrative, momentum_breakout)

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

Top 3 unmapped headlines (ticker spelled out literally in the title, symbol field still null):
1. "First in Market: MEXC to List WOODUSDT Futures in Innovation Zone..." (#New_Listings)
2. "Adjustment to RIFUSDT Funding Rate Settlement Frequency..." (#Trading_Updates)
3. "Adjustment to BNCUSDT Funding Rate Settlement Frequency..." (#Trading_Updates)

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **mixed** (BTC range, ETH uptrend, breadth cooling from overnight — 60.5% above EMA20; the older swing report's "bullish trend" read should be treated as stale-leaning, not current consensus)
- Stocks mood: **closed / pre-market** (underlying regime = chop, neutral bias, VIX 16.64, breadth mixed — planning context only, no RTH confirmation yet)
- Dominant narrative: momentum_breakout cluster (TLM/ZAMA, no confirmed catalyst) alongside a fresh (<1h) rwa_narrative basket (ONDO/XLM, tokenized-stocks-as-collateral headline) — the cleaner catalyst story this cycle
- Preferred side now: **wait-for-trigger, selective longs on RS-leader + breakout confirmation**; shorts only on confirmed breakdown with volume (crypto short-direction PF is currently 0.125 this week — treat shorts as low-confidence by default)
- Best long candidate: TLM/USDT — needs a confirmed breakout/volume hold above 0.0020 (see §8)
- Best short candidate: DEXE/USDT — needs a defined failed-bounce entry structure, not published this cycle (see §8)
- Best catalyst-backed candidate: ONDO/USDT — rwa_narrative basket, fresh <1h (see §8)
- What to avoid: UNH (open DOJ investigation), fresh directional bets on ETH/ARB while the exploit-hack cluster is active and growing, chasing GOOGL/LMT into today's earnings, MSFT (active securities_fraud flag)
- What would change the view: BTC reclaiming uptrend would resolve the intraday/swing regime divergence toward risk-on; a primary-source verification on the rwa_narrative catalyst would upgrade ONDO toward a formal B-tier idea; US cash open (16:30 EEST) will determine whether the stocks planning longs (XOM/AVGO/NVDA) get RTH confirmation

## 7. Candidate Deep Dives

### 1. TLM/USDT (long, watchlist, score 56.0)
- Has price already reacted to a catalyst? No — this is the momentum_breakout basket (pure price/volume, no verified news).
- Chasing? Not yet — current price 0.0019 sits inside the conditional pullback zone (0.0019-0.0019 per the report, i.e. right at the zone).
- Retest/pullback structure? Yes, that is the entire watch thesis.
- Overextended (>2 ATR from EMA20)? Not flagged; ATR ~0.0001.
- Would entry now be late? No — but score (56.0) is below the active-trade threshold; this is watchlist, not live.
- Actionable level: 1h close and hold above the zone top (~0.0020) with volume confirmation (currently only 1.21x — needs to expand).
- Market-mood alignment: consistent with "selective longs, demand breakout confirmation."
- Long/short/wait: wait-for-trigger long.
- Invalidation: 1h close below 0.0018.
- Chase risk: low right now, would rise sharply if price runs before volume confirms.
- Catalyst confirmation/contradiction: none — explicitly the playbook's known weak spot (no-catalyst intraday momentum in chop, 14d WR 23%/PF 0.70/-3R).
- TradingView/manual chart check unavailable — reading only from the report's local OHLCV/ATR/EMA fields.

### 2. BANK/USDT (long, already OPEN in swing — status/risk check, not a new idea)
- Confirmed triggered in swing mode (entry 0.2283-0.2366 zone per the report, score 72.4, playbook `crypto_swing_narrative_rs_momentum`, 14d WR 72%/PF 5.80/+24R for this playbook).
- 7d return is **+346.65%** — this is a parabolic move, and the report's own known-failure-mode note explicitly reads "chase risk after a vertical 24h move; BTC dump invalidating correlated swing longs."
- Also appears as waiting_for_entry in intraday mode and as a C-tier watchlist idea (score 50.5) — cross-mode consensus on direction, but the magnitude of the move argues for tight risk management on the existing position rather than adding exposure.
- No fresh catalyst — no-catalyst momentum name riding a strong playbook base rate, but the base-rate stats were built before names ran +346% in a week; treat the historical WR/PF as directionally useful, not as a guarantee at these extended levels.
- Actionable takeaway: tracking only for the open swing position; do not add a fresh intraday entry into an already-vertical move.

### 3. Cross-chain exploit-hack cluster (ETH/ARB) — risk note, not a trade idea
- "Hackers' Day" per Lookonchain: three exploits reported same-day, including a new **VerusCoin Ethereum bridge exploit (~$7.55M)** in addition to the carried-forward AFX Trade ($24.15M) and Arbitrum bridge ($24M, oracle manipulation via Ostium DEX) incidents from the overnight review.
- Not a specific trade call — a reason to avoid fresh directional bets on ETH/ARB (and BNB/ADA, per the Wanchain Cardano-BNB bridge incident still in the system's production risk-warning list) until the cluster resolves.
- Flagged in production risk warnings as `block_requires_operator_review` for ETH, ARB (and ADA, BNB from the Wanchain incident).

### 4. GOOGL (stocks, avoid/manual-review — new development this cycle)
- Reported earnings 2026-07-22T20:35:42 UTC (after yesterday's close). Its intraday setup (short, was A-tier score 84) is correctly demoted to C for `stale_post_earnings_setup` — pre-earnings levels are invalid.
- Also earnings-flagged for "do not chase into the print" alongside LMT (both report today, 2026-07-23).
- Verdict: **manual review required** — needs fresh post-earnings technical levels before any new consideration; do not use the pre-earnings score/levels.

### 5. Stocks planning watchlist — XOM / AVGO / NVDA (longs) vs META / XLV (shorts)
- Market is closed (pre-open); all of these are `market_closed_intraday_planning_only` demotions from A/B down to C.
- XOM (was A, score 95), AVGO (was A, score 83), NVDA (was A, score 86) are the strongest planning longs; META (was A, score 81), XLV (was A, score 80) the strongest planning shorts — none actionable until RTH confirmation at/after the 16:30 EEST open.
- Has price already reacted? Unknown pre-market — no pre-market tick data in this report.
- Actionable level: wait for the first 15-30min of RTH price action to confirm or invalidate these pre-close levels; do not treat pre-close scores as live entries.
- Legal/headline check: none of these five carry an active legal/earnings flag today (GOOGL/LMT do; MSFT does separately). XOM/AVGO/NVDA/META/XLV are clean on that axis.

## 8. Best Candidates Ranked

Even with no clean A/B trade this window, per the anti-over-conservatism rule the routed picks are:

1. **Long-watch: TLM/USDT** — trigger: 1h close/hold above ~0.0020 with volume expansion >1.5x; invalidate below 0.0018.
2. **Short-watch: DEXE/USDT** — trigger: failed bounce / breakdown continuation with volume confirmation; no formal level published this cycle, and crypto shorts are a weak-edge cohort this week (PF 0.125) — treat as low-confidence watch only.
3. **Catalyst-watch: ONDO/USDT** — trigger: rwa_narrative basket (tokenized-stocks-as-collateral headline, <1h fresh) confirmed by RS/technical follow-through; currently basket-primary only, not yet a formal Trade Idea.
4. **Avoid: UNH** — open DOJ investigation, unchanged 8+ cycles, technical/invest-mode score irrelevant while unresolved.
5. **Stocks pre-open watchlist (context, not yet actionable):** best long XOM, best short META — both require RTH confirmation before treating as live.

## 9. Avoid / No Trade

This is a decision-window call only — scanning, data collection, tracking, and the scheduler continue unchanged.

- **UNH** — open federal DOJ investigation (Medicare billing), manual review required, avoid new exposure regardless of technical/invest-mode score.
- **ETH, ARB** (and ADA, BNB per the still-open Wanchain flag) — active and worsening cross-chain exploit-hack cluster; avoid fresh directional bets until it resolves.
- **GOOGL** — post-earnings stale setup, manual review required before any new consideration; do not chase.
- **LMT** — earnings today, do not chase into the print.
- **MSFT** — active securities_fraud legal flag, demoted B→C; manual review required if it resurfaces as A/B.
- **Crypto scalp mode generally** — reproducibly losing this week (PF 0.72, totalR -3.10); no scalp idea should be treated as high-conviction without an unusually strong confirmation stack.
- **Crypto short direction generally** — PF 0.125, 0W/6L this week (n=8, anecdotal but consistently bad) — any new short needs materially better confirmation than a long to be worth the same risk.

## 10. Main Risks

- **Regime divergence:** intraday/scalp reads mixed/transition (BTC range) while the swing report (5.5h stale) still reads bullish/risk-on — do not assume the swing read is still current without a fresher confirmation.
- **Exploit-hack cluster, worsening:** three same-day exploits ("Hackers' Day" per Lookonchain) now touching ETH/ARB, on top of the still-open Wanchain Cardano-BNB incident (ADA/BNB) — elevated tail risk for anything on those chains.
- **Earnings risk:** GOOGL (reported) and LMT (reports today) — do not chase pre/post-earnings moves without fresh confirmed levels.
- **Legal/headline risk:** UNH (DOJ, unchanged), MSFT (securities_fraud), LLY (GLP-1 lawsuit) — all carry standing manual-review flags independent of technical score.
- **Catalyst layer degraded:** 79.1% of catalyst events unmapped — this is the second consecutive cycle with the same specific resolver defect (literal tickers like RIFUSDT/BNCUSDT resolving to null symbol); treat catalyst-driven calls with extra skepticism until fixed.
- **Data staleness:** stocks swing/invest reports are ~21 days old — no swing/invest-mode stocks decision should be made off that data.
- **Systemic (not a trade risk, a data-quality risk):** `no_gate_context` is the largest avoidable-loss bucket in the stocks-intraday paper diagnostics (-405.00R over 726 rows, 14d) — see §14 TODO-5.

## 11. Action Plan — Next 4 Hours

- Watch TLM/USDT for a confirmed breakout/volume hold above ~0.0020 before treating as actionable.
- No new intraday entries into BANK/USDT given the +346.65% 7d run — track the existing open swing position only, respect its stop.
- Keep ETH/ARB/ADA/BNB on the avoid list through the US pre-open cycle unless the exploit cluster news resolves.
- Build the US-session watchlist from XOM/AVGO/NVDA (longs) and META/XLV (shorts), but require the first 15-30min of RTH price action before treating any as live (16:30 EEST open).
- Do not touch GOOGL or LMT until fresh post-earnings levels are published; avoid MSFT while the securities_fraud flag is active.
- Monitor whether BTC reclaims uptrend before the next cycle — that would resolve the current intraday/swing regime divergence.
- No changes to scoring, thresholds, or scanning — system continues running as-is.

## 12. Final Verdict per Mode

- **Scalp:** No A/B setups. Mode itself is a known loser this week (PF 0.72) — treat any future scalp idea with extra scrutiny.
- **Intraday:** No new A/B setups this cycle; book carries open/triggered ERA and TLM plus several partially-booked B-tier longs. Watchlist-only for new entries (TLM/ZAMA/KITE/ERA/RE/MIRA/RIF/BANK).
- **Swing:** Best-performing mode this week (PF 2.91) but the report is ~5.5h old and reads a more bullish regime than the fresher intraday data — treat existing open positions (RE, EPIC, BANK, ERA) as tracking-only; do not originate new swing ideas off this read without a same-day refresh.
- **Stocks intraday:** Market closed — all candidates planning-only (best longs: XOM, AVGO, NVDA, AMD, JPM; best shorts: META, XLV, PLTR). GOOGL/LMT earnings-today caveat applies at the open; MSFT legal flag stands separately.
- **Stocks swing/invest:** Data ~21 days stale — do not use for any current decision (TODO-2, unchanged).

## 13. Sources

- Internal: `data/catalysts/2026-07-23/catalyst_cycle_05-41.md` (VerusCoin Ethereum bridge exploit, AFX Trade exploit, Arbitrum bridge incident — cross-referenced across t.me/lookonchain, CoinDesk, BeInCrypto, The Block, t.me/wublockchainenglish, t.me/peckshield)
- Internal: `data/reports/scalp/2026-07-23_05-29_scalp_report.md`, `data/reports/intraday/2026-07-23_05-37_intraday_report.md`, `data/reports/swing/2026-07-23_03-05_swing_report.md`, `data/reports/stocks/intraday/2026-07-23_06-05_stocks_intraday_report.md`
- Internal: `news_items` direct SQL query for UNH (no fresh DOJ update in last 48h, most recent row 2026-07-21 unrelated "Is It Headed for $500?" piece)
- Internal: CLI `active-signals`, `signal-stats`, `detect_untracked_legacy_alerts` (2026-07-23 11:3x runs)
- LLY legal-risk source (carried in report): The Motley Fool Investing, "Deceptive Advertising! Claims Novo Nordisk in Explosive New GLP-1 Lawsuit Against Eli Lilly", 2026-07-22

External web research (WebSearch/WebFetch) was not invoked this run — internal `news_items`/report data was sufficiently fresh and consistent for every candidate touched (per §G: only escalate to external search when internal records are missing/stale/contradictory). No candidate here depended critically on external verification beyond what direct SQL/report reads already confirmed.

## 14. Fix Requests / TODO

### TODO-1: Catalyst symbol resolver missing tickers spelled out literally in the headline (recurring — 2nd consecutive cycle with evidence)
- **issue:** Funding-rate-adjustment and new-listing notices (e.g. "Adjustment to RIFUSDT Funding Rate Settlement Frequency", "MEXC to List WOODUSDT Futures", "Adjustment to BNCUSDT/FWDIUSDT/BOTUSDT Funding Rate Settlement Frequency") are landing in `catalyst_events.jsonl` with a null symbol despite the ticker being present verbatim in the title.
- **evidence:** `data/catalysts/2026-07-23/catalyst_events.jsonl` — 791/1000 (79.1%) unmapped this cycle (was 390/500, 78.0%, at 04:48 — same pattern, same specific tickers recurring: RIFUSDT/BNCUSDT seen again).
- **suggested manual fix:** Extend the symbol resolver's regex/lookup to catch `#Trading_Updates` / `#New_Listings`-style Binance/MEXC announcement formats where the ticker appears as a single concatenated token (e.g. `RIFUSDT`) rather than the usual `RIF/USDT` form.
- **priority:** high
- **first observed:** 2026-07-23 04:48 EEST; **confirmed recurring:** 2026-07-23 11:39 EEST (same specific tickers, unresolved across two cycles)

### TODO-2: Stocks swing/invest reports ~21 days stale (unchanged)
- **issue:** `data/reports/stocks/swing/` and `data/reports/stocks/invest/` have no report newer than 2026-07-02 — now over 3 weeks stale, while crypto and stocks-intraday reports generate normally on schedule.
- **evidence:** `ls -t data/reports/stocks/swing/*.md` and `data/reports/stocks/invest/*.md` both show `2026-07-02_13-0x` as the latest file.
- **suggested manual fix:** Investigate why the stocks swing/invest report generator stopped running or is failing silently; check the scheduler config for these two report types specifically.
- **priority:** high
- **first observed:** carried forward from 2026-07-23 04:48 EEST review (and earlier); unchanged this cycle.

### TODO-3: Regime divergence between intraday/scalp and swing timeframe reads
- **issue:** This cycle's intraday/scalp market regime reads "transition (mixed)" (BTC range, breadth 60.5% above EMA20) while the swing report — generated ~5.5h earlier — still reads "bullish trend (risk-on)". Both feed into the same candidate universe (BANK, RE, EPIC, ERA all appear in both), creating a risk that an operator reads the swing report's regime label as still-current when the faster-moving data has already shifted.
- **evidence:** `data/reports/intraday/2026-07-23_05-37_intraday_report.md` §1 vs `data/reports/swing/2026-07-23_03-05_swing_report.md` §1 — same day, ~2.5h generation gap, materially different regime labels.
- **suggested manual fix:** Consider whether the swing report's regime label should be recomputed at read-time (or the report annotated with "regime as of generation time") rather than persisting a label that may go stale faster than the report's own 4-12h freshness bucket assumes.
- **priority:** medium
- **first observed:** 2026-07-23 11:39 EEST (this run).

### TODO-4: Large volume of past-expiry signals still shown as "active" (carried forward)
- **issue:** A large share of `active-signals` rows (18/26 crypto, ~37/50 stocks) show `tp1_hit`/`tp2_hit`/`triggered` status with an `expires_at` timestamp already in the past, without a clear final resolution (win/loss/flat) surfaced in this CLI view.
- **evidence:** `python -m src.cli active-signals --asset-class crypto` and `--asset-class stocks`, 2026-07-23 11:3x run — e.g. crypto ALLO/USDT (intraday) shows `tp1_hit`, `expires_at` 2026-07-19T15:21:04, still listed as "active" 4 days later.
- **suggested manual fix:** Confirm whether this is a display-only artifact of the CLI (i.e. these are correctly resolved in `signal_outcomes` and the CLI just doesn't filter by expiry) or a genuine resolution-job backlog. Not confirmed as a bug this run — diagnostic only.
- **priority:** medium
- **first observed:** carried forward from 2026-07-23 04:48 EEST review; not yet independently reconfirmed as bug vs display artifact.

### TODO-5: stocks-intraday `no_gate_context` failure bucket is the largest avoidable-loss bucket in the system
- **issue:** In the 14d stocks-intraday paper diagnostics, the `no_gate_context` failure reason accounts for -405.00R across 726 rows — by a wide margin the single largest avoidable-loss bucket reported anywhere in this review (next largest is `spread_slippage_cost` at -11.00R over 11 rows).
- **evidence:** `data/reports/stocks/intraday/2026-07-23_06-05_stocks_intraday_report.md` §10, "By failure reason" table.
- **suggested manual fix:** Investigate why such a large row count (726) lacks gate context at all — this may indicate a large historical backfill population predating the SI-1..5 gating logic rather than a live/ongoing defect; worth a manual session to confirm the population's date range and whether it's already excluded from live guard calculations.
- **priority:** medium
- **first observed:** 2026-07-23 11:39 EEST (this run; not previously called out by tag in the 04:48 review, though the underlying data existed).

### TODO-6: `telegram-test` CLI (and likely other notifier call-sites) silently 400s on odd-underscore-count messages
- **issue:** `notifier.send()` defaults to `parse_mode="Markdown"` (legacy Telegram Markdown) unless a call-site explicitly overrides it to `""` (as `src/agents/supervisor.py:1004`, `src/cli.py:733`, and two spots in `src/news/` already do, per a comment noting this exact failure mode). `telegram-test` (`src/cli.py:505-517`) does **not** override it, so any `-m` message containing an odd number of underscores (e.g. a bare filename like `OPUS_ENRICHED_REVIEW_LATEST.md`) is parsed as an unterminated italics span and the Telegram API rejects it with `400 Bad Request`.
- **evidence:** Reproduced live this run — `python -m src.cli telegram-test -m "File: OPUS_ENRICHED_REVIEW_LATEST.md"` fails with `400 Client Error: Bad Request`; the identical message with underscores replaced by spaces sends successfully. Root cause confirmed by bisecting the compact review message in isolation.
- **suggested manual fix:** Have `telegram_test()` in `src/cli.py` pass `parse_mode=""` the same way the other call-sites already do (per the comment at `src/agents/supervisor.py:1002`), or add a `--parse-mode` option. Low-risk, one-line change, but out of scope for this advisory-only run.
- **priority:** low
- **first observed:** 2026-07-23 11:50 EEST (this run, while sending the §O Telegram summary — worked around by avoiding underscores in the message text, no code touched).
