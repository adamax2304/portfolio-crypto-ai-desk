# Opus Enriched Review — US open reaction review — Auto Cycle 18:30 EEST

## 1. Executive Summary

**Slot: US open reaction review** (nominal 18:30 EEST slot; this run dispatched at **19:14 EEST**, ~44 min jitter — noted in §3, does not change the read). **Advisory only — no auto-trade, no scoring/threshold/strategy changes made or implied.**

**Critical framing correction:** today, **2026-07-19, is a Sunday.** US cash equities are **closed all day** — there was no same-day US open to react to. Per the routine's own weekend rule, all stock signals below are **planning/watchlist context only**; crypto is the sole live-actionable class this window. (Same correction carried by the sibling 16:20-slot review dispatched at 18:03 today.)

**Crypto had a genuinely good day operationally**: 6 CLOSED WIN (TP3 hits: TLM×2, XLM×2, HOME, CASHCAT), 2 CLOSED LOSS (ETH scalp, OPN intraday stopped), 1 OPEN with TP1 hit running (LTC/USDT intraday). But the **current moment has no clean fresh entry**: the two live momentum names (KAITO, VANRY) both fired ENTERED-UNRESOLVED batches in the last cycle, and BANK/USDT (+112.9% today, confirmed via CoinGecko) is a chase-risk, no-catalyst, high-concentration-risk (top-5 wallets hold ~75% of supply) name the system correctly caps to avoid.

**Macro divergence still open (3rd consecutive review flagging it today):** internal reports label the market "bullish trend (risk-on)"; verified external sources show BTC/ETH under sustained pressure from an escalating US-Iran conflict (Strait of Hormuz strikes, $350M+ liquidations this week). Treat the internal regime label as macro-fragile.

**Integrity note (escalating further):** the untracked watchlist-alert bug (Telegram alert fires, no `proposed_signal` minted) now shows **5 instances today across 3 symbols** — ALLO/USDT (×3), HOME/USDT (×1), and **BANK/USDT (×1, new today)**. See §14 TODO-1.

**Stocks:** market closed; no A/B candidate is actionable today. UNH beat Q2 earnings and raised guidance (July 16), but the CFO's cautious tone on medical-cost trend plus an ongoing/widening DOJ probe keeps the open UNH C-tier positions on **manual-review**, not a clean hold.

**Catalyst mapping is weak this run (65.7% unmapped)** — use as context, not as a decision driver.

## 2. Data Used

- Reports: scalp (`2026-07-19_15-12`, ~1h02m old — fresh), intraday (`2026-07-19_15-20`, ~54m old — fresh), swing (`2026-07-19_01-47`, ~14h27m old — **stale**, referenced only for continuity, excluded from fresh verdicts). Stocks intraday (`2026-07-17_21-56`, ~45h old, market-closed weekend — planning-only). Stocks swing/invest (`2026-07-02`, ~17 days old) — per prior project context this mode is deprecated/shadow-only, not a fresh data-quality fault; not used for any verdict.
- Catalysts: `data/catalysts/2026-07-19/catalyst_events.jsonl` (2,651 events cumulative today), `narrative_baskets.jsonl` (6 baskets), latest `catalyst_cycle_15-23.md`.
- LLM packets: `llm_analysis_packet.md` (18:21, ~53m old, fresh, crypto). `llm_stocks_packet.md` (Jul 17 14:25, stale/weekend, planning-only).
- CLI: `active-signals` ×2 (crypto 12 rows, stocks 50 rows), `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-07-19` (**5 findings** — ALLO×3, HOME×1, BANK×1).
- DB reads: `proposed_signals` + `signal_outcomes` for the 5 most-recent crypto signals (G, KAITO×2, VANRY×2) and the stale NEAR/USDT short; `news_items` 24h freshness checks for BANK, KAITO, XEC, HYPE, UNH.
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-19_1803.md` (pre-US-open decision slot, nominal 16:20, dispatched 18:03).
- External: 3 WebSearch queries (BTC/ETH/Iran macro, UNH CFO/DOJ, BANK/Lorenzo Protocol surge) + 1 WebFetch verification (Yahoo Finance UNH CFO article). 5/5 sources ingested via `scripts.ingest_enriched_review_sources` (3 crypto-tagged, 2 stocks-tagged).

## 3. Scheduler / Data Freshness

- `scheduler.log`: mtime **18:43**, ~31 min old at run time — fresh, **not deferred**.
- Latest cycle summary `cycle_06_18-02_summary.md`: mtime **18:43** — same cycle, fresh.
- Standalone monitors: `derivatives_monitor` log active to **19:13** (78 symbols, 5 venues, all writing normally), `pending_monitor` log active (9/9 pair checks succeeded this pass, 6 TP hits recorded, 0 failures, disk ok), `mexc_canary_monitor` shows "another leader is active" (normal leader-lock behavior, not a failure) — all monitors healthy.
- Dispatch jitter: nominal slot 18:30 EEST, actual dispatch 19:14 EEST (~44 min late). Data freshness checked independently above; content unaffected.
- Scalp/intraday: fresh (~54m–1h02m old). Swing: ~14h27m old — past the 14h stale threshold, excluded from fresh verdicts (used only for continuity/context).
- Stocks: all modes stale/weekend-closed — planning-only, excluded from any actionable verdict.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-07-19 19:14 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["fresh derivatives snapshot beyond 15:20 intraday report", "live OHLCV newer than report generation"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log + latest cycle summary both mtime 18:43, ~31min old", "scalp/intraday fresh (~1h), swing 14h27m old (stale, excluded)", "dispatch jitter 44min vs nominal 18:30 slot"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["mixed", "risk_off", "chop"],
      "data_missing": ["live BTC/ETH price newer than external snapshot"],
      "suggested_effect": "advisory_only",
      "facts_used": ["internal reports label market 'bullish trend (risk-on)', BTC/ETH both uptrend, altcoin breadth 55.3%", "external: BTC/ETH under sustained pressure this week from escalating US-Iran strikes near the Strait of Hormuz, $350M+ liquidations (Yahoo Finance, CryptoBriefing)", "same internal/external divergence flagged in the 11:39 and 18:03 reviews today, still unresolved"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported", "no_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["910/2,651 catalyst_events mapped = 34.3%, unmapped 65.7% (consistent with 67.3% at 18:03 — no improvement)", "momentum_breakout basket (BANK/TLM/KAITO) explicitly has zero confirmed news catalyst per catalyst_cycle_15-23.md", "HYPE fresh<6h perps_dex_narrative basket, externally verified mixed catalyst (TKNZ ETF weighting vs prior unlock/MAS alert)"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "oi_supports", "data_unavailable"],
      "data_missing": ["live funding/OI updates newer than 18:12/18:20 reports", "OI history for XEC/USDT (n/a in intraday report)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["KAITO/USDT: price up + OI up (24h OI +3.17%, crowding normal) — fresh positioning confirms trend, not squeeze-prone", "XEC/USDT capped to C-tier: 'short squeeze risk' + 'high_upper_wick_short_squeeze_risk (+exhaustion)' per rejected list", "internal squeeze-guard caps every scanned short candidate (LAB, SYN, DEXE, XEC, ASSET) to C-tier"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["entry_late", "chase_risk", "stale_before_entry", "price_moved_away"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["KAITO/VANRY intraday+scalp signals from 15:17-15:20 batch already show entered_unresolved/expired outcomes with final_r=0 — no clean fresh trigger remains from that batch", "BANK/USDT +112.9%/24h off an ATH just printed today ($0.27257), current $0.205 already pulled back — chasing here is late by definition", "G/USDT still waiting_for_entry with a defined pullback trigger, the cleanest live setup on the board"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "needs_review",
      "confidence": 0.65,
      "reason_codes": ["closed_flat", "entered_unresolved", "waiting_for_entry", "needs_review", "no_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["today's crypto B-tier signals: 6 CLOSED WIN (tp3_hit), 2 CLOSED LOSS (stopped), 1 OPEN (tp1_hit, LTC/USDT running), 3 ENTERED UNRESOLVED (0R display/unresolved, no TP/SL before window — KAITO intraday+scalp, VANRY intraday), 1 WAITING for entry (G/USDT), 1 NO-ENTRY/STALE (VANRY scalp, window closed 17:17 without trigger)", "NEAR/USDT scalp short: tp1_hit but ~48h+ past expires_at (2026-07-17T15:56), still unresolved — needs_review, growing further from 50h+ at 18:03 (recomputed from current timestamp)", "ALLO/HOME/BANK untracked watchlist alerts (no proposed_signal) — needs_review"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["headline_risk", "reduce_risk", "manual_review", "correlation_cluster"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["US-Iran conflict still the dominant gap-risk driver into Monday's cash open (equities closed all weekend)", "UNH: earnings beat + guidance raise (July 16) but CFO cautious on medical-cost trend + membership attrition (Yahoo Finance, July 19), plus a DOJ probe that has widened to an antitrust angle on the Claritev integration (Simply Wall St) — unresolved legal overhang on open C-tier positions", "watchlist-alert reuse bug now spans 3 symbols (ALLO, HOME, BANK) — data-integrity risk to Telegram-actionable counts continues to widen"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto week: headline A/B PF 1.60, winrate 28.7%, totalR +16.31 (n=112) — modestly positive; strong mode PF 2.10/1.98 (working) vs weak mode PF 0.52 avgR -0.24 (failing)", "stocks week: headline A/B PF 0.75, winrate 36.4%, totalR -0.5 (n=11, weak sample) — negative; C-tier watchlist PF 0.86, totalR -5.5 (n=209) — also negative", "observation flagged by signal-stats: weekend-mode crypto signals underperform (winrate 32%, n=43) vs non-weekend — consistent with today being a weekend session"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.58,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "G/USDT", "trigger": "waiting_for_entry — pullback into 0.00330771-0.00341314 with 1h close acceptance inside the zone; invalidation below 0.00330486. Score 66.7, weekend-mode active, no fresh catalyst — treat as a small, mechanical B-tier watch, not a conviction long.", "reason": "the only crypto B-tier signal still cleanly in a defined, unresolved waiting state tonight — every other live long from the last cycle (KAITO, VANRY) is already entered-unresolved with a 0R/expired outcome" },
    "best_short_candidate":    { "symbol": "XEC/USDT", "trigger": "capped to C-tier by the system's own squeeze-guard (thin-liquidity/short-squeeze + high-upper-wick exhaustion tags); would need a clean break and retest below the intraday swing low on confirmed volume, AND the squeeze-guard to lift, before it is actionable", "reason": "flipped from the strongest swing-report symbol (+21.7%/24h, 14h+ ago) to the weakest intraday/scalp symbol (-14.6%/-14.9%/24h) within the same day — a textbook failed-bounce/exhaustion pattern, but every internal safeguard currently (correctly) blocks it, consistent with historical short-direction PF of 0.20-0.26 this week" },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "wait_pullback playbook — perps_dex_narrative basket primary, fresh<6h; wait for a pullback toward 60.70-60.88 with volume confirmation, invalidation below 60.48. Do not chase current levels (60.96, just above the pullback zone).", "reason": "genuine, externally-verified two-sided catalyst set (T. Rowe Price TKNZ ETF ~6% HYPE weighting = bullish; prior $645M unlock + MAS Investor Alert List addition = bearish) — real news, not a mistagged headline; same call as the 18:03 review, still valid" },
    "avoid_candidate":         { "symbol": "BANK/USDT", "reason": "momentum_breakout basket primary, +112.9%/24h off an ATH printed today with zero confirmed news catalyst (CoinGecko-verified: technical breakout of a descending channel, not fundamentals); top-5 wallets hold ~75% of supply (concentration/manipulation risk); also the newest symbol in today's untracked-alert integrity bug (§14 TODO-1) — do not chase, do not trust the alert count for this symbol either" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.75 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.50 | mixed, risk_off, chop | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, fresh_catalyst, narrative_supported, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | entry_late, chase_risk, stale_before_entry, price_moved_away | advisory_only |
| execution_lifecycle | needs_review | 0.65 | closed_flat, entered_unresolved, waiting_for_entry, needs_review, no_entry | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, reduce_risk, manual_review, correlation_cluster | advisory_only |
| playbook_performance | caution | 0.60 | playbook_working, playbook_failing, low_sample | advisory_only |
| **head_trader** | **caution (watch)** | **0.58** | synthesis of above | advisory_only |

## 4. What Changed vs Previous Review (18:03 EEST, pre-US-open decision slot)

- **New signal batch since 18:03**: G/USDT (B, intraday, waiting_for_entry, created 15:42) was already present at 18:03; no new proposed_signals have been created between 18:03 and this run — the book is unchanged at the signal level.
- **Lifecycle progression**: the KAITO/VANRY intraday+scalp batch (created 15:17-15:20) that was `triggered`/live at 18:03 has since resolved to `expired`/entered-unresolved (final_r=0) per the 16:10 UTC outcome check — no TP/SL hit before the window closed. VANRY/USDT scalp (waiting_for_entry) also timed out without triggering (expires_at 17:17, now past).
- **Untracked-alert bug widened**: 3 findings at 18:03 (ALLO×2, HOME×1) → **5 findings now** (ALLO×3, HOME×1, **BANK×1 — new symbol**). See TODO-1.
- **NEAR/USDT stale short**: was 50h+ past expiry at 18:03; now recomputed at ~48h+ from this run's later timestamp (expiry math is consistent — still unresolved, still needs_review).
- **UNH**: no new legal development since 18:03; the CFO-warning/DOJ-antitrust-widening context in this review's §7 deep dive was already implicitly known but is now externally sourced and cited for the first time this cycle.
- **Catalyst mapping**: 67.3% unmapped at 18:03 → 65.7% now (cumulative daily count growing in both numerator and denominator) — materially unchanged, still weak.
- **Head Trader synthesis**: largely unchanged from 18:03 (ALLO no longer named as "best long" since its lifecycle status could not be re-confirmed as cleanly open this run; G/USDT substituted as the cleanest defined-trigger long-watch). BANK/USDT avoid call reaffirmed and strengthened with fresh external verification (CoinGecko ATH + whale-concentration data).

## 5. Catalyst Coverage

- Catalyst events today (cumulative): **2,651** total; **910 mapped** (34.3%), **1,741 unmapped** (65.7%).
- Narrative baskets active: **6** — `rwa_narrative`, `perps_dex_narrative`, `delisting_thin_liquidity`, `ai_narrative`, `binance_ecosystem_teaser`, `momentum_breakout`.
- **Catalyst mapping weak this run (65.7% unmapped) — use the catalyst layer as context, not a final decision driver.**
- Top 3 unmapped headlines (sampled): "Base memecoin $BRIAN surges after Brian Armstrong changes X avatar, then crashes 86%..."; a generic "Choose the one that represents you the most..." social post; "TODAY: The GENIUS Act marks its one-year anniversary...".
- Legal/regulatory notables (mapped): TSLA (Musk SEC settlement, $1.5M fine), UNH ×5 (DOJ Medicare-fraud probe headlines), INTU (securities fraud lawsuit opportunity notice).

## 6. Market Landscape

Crypto: BTC and ETH both in an internal uptrend read, altcoin breadth 55.3% above EMA20 — but this internal "bullish trend (risk-on)" label conflicts with verified external reporting of a risk-off week driven by escalating US-Iran strikes near the Strait of Hormuz (Yahoo Finance, CryptoBriefing), with $350M+ in liquidations and both BTC and ETH pulling back from local highs ($65K/$1,900 briefly touched, then faded). ETH has shown less resilience than BTC through these episodes per external sourcing. Today's realized signal performance (6 TP3 wins, 2 stops) suggests the momentum/RS-leader playbook worked well intraday despite the macro overhang — but every fresh momentum name from the last cycle is now either entered-unresolved or already-extended, leaving no clean new entry at this exact moment.

Stocks: market closed (Sunday). UNH is the standout story of the week — a strong Q2 beat and raised full-year guidance ($19.50-$20 adjusted EPS) drove the stock up 5.6% to $423.38 on July 17, but CFO Wayne DeVeydt's on-the-record caution about medical-cost trend and forecast membership losses (~500K exchange, ~1.1M Medicare Advantage members in 2026) tempered the market's read, and the DOJ criminal probe has reportedly widened to an antitrust angle on the Claritev integration. Net: fundamentally improving, legally unresolved — a genuine two-sided story, not a one-line "avoid."

### Market Mood / Risk Routing
- Crypto mood: **mixed** (internal bullish-trend label vs verified external risk-off macro pressure — unresolved divergence, 3rd consecutive review flagging it)
- Stocks mood: **closed** (Sunday; last session +5.6% post-earnings reaction in UNH, broader market untested since Friday's Iran-driven Dow futures weakness)
- Dominant narrative: momentum_breakout cluster (BANK/TLM/KAITO, no confirmed catalyst) competing with US-Iran geopolitical risk-off as the two loudest signals today
- Preferred side now: **wait-for-trigger** (mechanical B-tier watches only; no conviction long or short clears every internal safeguard right now)
- Best long candidate: G/USDT — trigger: pullback into 0.00330771-0.00341314, 1h acceptance, invalidation below 0.00330486
- Best short candidate: XEC/USDT — trigger: clean break + retest below intraday swing low on confirmed volume, squeeze-guard must lift first
- Best catalyst-backed candidate: HYPE/USDT — trigger: pullback into 60.70-60.88 with volume confirmation, invalidation below 60.48
- What to avoid: BANK/USDT (chase risk, no catalyst, whale concentration, integrity-bug symbol); new stocks entries (market closed, no fresh confirmation possible)
- What would change the view: a verified de-escalation headline on the US-Iran conflict (would resolve the internal/external regime divergence); a resolved/closed disposition on the 3 entered-unresolved KAITO/VANRY signals; Monday's actual US cash open print for stocks

## 7. Candidate Deep Dives

**TradingView / manual chart check unavailable** — no chart MCP loaded this run; all technical reads below use only the local OHLCV / ATR / EMA / support-resistance fields already present in the scalp/intraday/swing reports, no fabricated chart observations.

### 7.1 BANK/USDT (Lorenzo Protocol) — AVOID / chase risk

- Has price already reacted to the catalyst? There is no catalyst — this is a pure technical breakout (cleared a descending channel capping price since June) confirmed via CoinGecko; price has already run +112.9%/24h to a fresh ATH ($0.27257) and pulled back to ~$0.205.
- Is the setup chasing? Yes, unambiguously — the playbook tag is literally `avoid_chase`.
- Retest/pullback structure? Not yet established; too early post-ATH to call a clean retest.
- Overextended (>2 ATR from EMA20)? Yes, per the scalp/intraday rejection reasons flagged on related names in the same cluster.
- Would entry now be late? Yes.
- What level makes it actionable? A multi-hour base/retest with volume confirmation well below the ATH, plus a verified fundamental catalyst (currently none exists).
- Aligned with market mood? Only in the narrowest technical-momentum sense; fights the "no fresh verified catalyst" system gate.
- Long, short, or wait-for-trigger? Wait-for-trigger at best; effectively avoid.
- Actionable now or after confirmation? Not actionable — no confirmation path defined by the system (kill-switch: `crypto_scalp_disabled` also applies to the scalp variant).
- Invalidation? N/A — not an active trade.
- Chase-risk setup? Yes.
- Catalyst confirmation or contradiction? No catalyst; external data (whale concentration — top 5 wallets ~75% of supply) adds a manipulation/thin-float risk layer the internal reports do not explicitly score.
- **Integrity flag**: a B-tier scalp alert (score 77.9) fired for BANK/USDT via Telegram at 15:17 with no matching `proposed_signal` — this symbol is now part of the untracked-alert bug (§14 TODO-1), so even if someone wanted to track this trade, the system's own PF/winrate metrics would not see it.

### 7.2 KAITO/USDT & VANRY/USDT — momentum cluster, ENTERED UNRESOLVED

- Both fired intraday (15:20) and scalp (15:17) B-tier long signals off strong RS-vs-BTC readings (KAITO +15.0-15.7%, VANRY +14.2-14.9%) with derivatives support (KAITO: price up + OI up, crowding normal).
- Per `signal_outcomes` (checked 16:10 UTC): all four triggered/entered signals (KAITO intraday+scalp, VANRY intraday) show `final_outcome=expired`, `final_r=0.0`, `entry_time_basis=historical_not_currently_executable` — **ENTERED UNRESOLVED: 0R display / unresolved, no TP/SL before window.** This is not a missed entry; the entry was filled, but neither TP nor stop resolved before the tracker's check window closed.
- VANRY/USDT scalp (waiting_for_entry) never triggered before its 17:17 expiry — **NO-ENTRY / STALE** (price moved away or window simply closed).
- Has price already reacted? Yes — both names were already extended when the signals fired (7d returns: KAITO +46%, VANRY -13%).
- Would entry now be late? Yes, for a fresh chase; a retest of the original entry zones (KAITO 0.938-0.953, VANRY 0.0055-0.0056) would be the next legitimate trigger, not a market re-buy at current levels.
- Catalyst confirmation or contradiction? None — both are in the `momentum_breakout` basket explicitly tagged "no confirmed news catalyst."
- Verdict: **NEEDS REVIEW** — monitor for a clean retest into the original zones; not actionable as a fresh entry right now.

### 7.3 XEC/USDT — best short-watch, capped by squeeze-guard

- 04:47 swing report: XEC was the **strongest** symbol on the board (+21.7%/24h, RS +20.4%). By the 18:12/18:20 scalp/intraday reports (fresher, same day), XEC had flipped to the **weakest** symbol (-14.6% to -14.9%/24h) — a full intraday reversal.
- The system tags this "short squeeze risk" and "high_upper_wick_short_squeeze_risk (+exhaustion)" and caps it to C-tier — i.e., a classic failed-bounce/exhaustion pattern the system correctly refuses to short outright given thin liquidity and squeeze risk.
- Has price already reacted? Yes — the reversal has already happened; shorting the reversal itself now is late.
- What level makes it actionable? A clean break of the intraday swing low with a retest-and-reject on confirmed volume, which would need to also clear the internal squeeze-guard.
- Catalyst confirmation or contradiction? No fresh news found for XEC in the last 24h (`news_items` check: 0 rows) — pure technical/derivatives story.
- Verdict: **WATCH-ONLY**, best short-watch on the board precisely because every internal safeguard currently (correctly) blocks it — consistent with this week's weak short-direction performance (PF 0.20-0.26).

### 7.4 HYPE/USDT — catalyst-backed watch

- Externally verified two-sided catalyst (carried from the 18:03 review, still current): T. Rowe Price's TKNZ multi-token ETF launched with HYPE "significantly overweight" (~6% weighting, bullish) against a prior $645M July unlock and MAS Investor Alert List addition (bearish).
- `perps_dex_narrative` basket primary, `wait_pullback` playbook, fresh <6h.
- Current price 60.96, just above the conditional pullback zone (60.70-60.88) — score 56.8, below the active-trade threshold (C-tier watchlist only).
- Has price already reacted? Partially — the ETF-inclusion news is likely already partly priced in; the unlock overhang is still ahead.
- Chase risk? Yes at current levels; the system's own entry plan explicitly says "watch only... do not treat this as active."
- Verdict: **WATCH-ONLY / catalyst-backed**, wait for the defined pullback zone with volume confirmation.

### 7.5 UNH — legal/headline risk, MANUAL REVIEW REQUIRED

- Q2 2026 earnings (July 16): adjusted EPS beat estimates by ~30%; FY2026 guidance raised to $19.50-$20/share (from $18.25+). Stock +5.6% to $423.38 on July 17 (Yahoo Finance, verified via WebFetch).
- CFO Wayne DeVeydt, on the same earnings call, characterized medical-cost improvement as a "multi-year journey," said costs remain "elevated over historical levels," and forecast ~500K ACA exchange member losses and ~1.1M Medicare Advantage member losses in 2026 (Yahoo Finance, published 2026-07-19).
- **LEGAL/HEADLINE RISK**: the pre-existing DOJ criminal probe into Medicare Advantage billing (extended to Optum Rx / physician reimbursement per earlier-cited FierceHealthcare reporting) has reportedly **widened further** to a broader DOJ antitrust probe concerning the Claritev integration (Simply Wall St, cited this run).
- Open positions: two C-tier invest-mode longs (`sig_90b50ceef0d1ebd3`, expires 2026-08-01; `sig_4697b87c9845547f`, tp1_hit, expires 2026-07-31) carry this risk unaddressed by any internal gate (§14 TODO-4, carried forward).
- Per §I discipline: verified legal/headline risk on an open position → final verdict is **AVOID for new adds / MANUAL REVIEW REQUIRED for the existing open C-tier longs** — never a clean actionable hold, despite the strong fundamental print.

## 8. Best Candidates Ranked

1. **HYPE/USDT** — catalyst-backed watch, wait_pullback into 60.70-60.88, invalidation below 60.48. Most defensible risk/reward of the five because the catalyst is genuine and externally verified both ways.
2. **G/USDT** — mechanical long-watch, pullback into 0.00330771-0.00341314, invalidation below 0.00330486. Small size, no catalyst, weekend-mode — treat as a data-collection trade, not conviction.
3. **XEC/USDT** — short-watch only, needs a confirmed breakdown-and-retest plus the squeeze-guard to lift before it is tradeable.
4. **KAITO/USDT & VANRY/USDT** — monitor for retest into original entry zones (KAITO 0.938-0.953 / VANRY 0.0055-0.0056); not fresh entries at current levels.
5. **BANK/USDT** — avoid; **UNH** — manual review required (existing positions only, no new adds).

No clean, fully-confirmed A-tier or high-conviction trade exists this window — this is a routing/watch call, not a stop-trading call.

## 9. Avoid / No Trade

*(This decision window only — never a system-stop command; scanning, tracking, and data collection continue uninterrupted.)*

- **BANK/USDT**: chase risk, no catalyst, whale concentration (~75% top-5), untracked-alert integrity issue.
- **New UNH adds** (and any new stocks entries generally): market closed; UNH specifically carries an unresolved/widening DOJ legal overhang against a strong-but-caveated earnings beat.
- **Fresh chases into KAITO/VANRY at current levels**: both already extended, both already produced 0R/entered-unresolved outcomes from the last cycle.
- **XEC/USDT as an outright short right now**: squeeze-guard and thin liquidity make this correctly blocked until a confirmed breakdown-retest.

## 10. Main Risks

- **Macro/geopolitical**: US-Iran conflict escalation (Strait of Hormuz strikes) is the dominant gap-risk driver into Monday's US cash open; internal "bullish trend" regime label is macro-fragile against this verified external backdrop (unresolved divergence, 3 consecutive reviews today).
- **Data integrity**: untracked watchlist-alert bug now spans 3 symbols (ALLO, HOME, BANK) in one day — Telegram-visible tier-upgrade alerts are firing without a backing `proposed_signal`, degrading PF/winrate/avgR accuracy for those symbols.
- **Stale bookkeeping**: NEAR/USDT scalp short ~48h+ past expiry, still unresolved in the active-signals table.
- **Legal/regulatory**: UNH DOJ probe widening (Medicare billing → Optum Rx/physician reimbursement → antitrust/Claritev) against two open C-tier positions with no internal legal-risk gate at that tier (§14 TODO-4).
- **Catalyst mapping quality**: 65.7% of today's catalyst events are unmapped — treat the catalyst layer as directional context only, not a scoring input to lean on heavily.
- **Weekend-mode performance drag**: signal-stats flags weekend-mode crypto signals underperforming (winrate 32%, n=43) vs the broader sample — relevant since today (Sunday) is entirely weekend-mode.

## 11. Action Plan — next 4 hours

- Monitor G/USDT for a pullback into 0.00330771-0.00341314; do not chase above the zone.
- Monitor KAITO/USDT (0.938-0.953) and VANRY/USDT (0.0055-0.0056) for a clean retest into their original entry zones before considering re-entry; treat the last cycle's fills as closed/unresolved, not still-live.
- Watch XEC/USDT for a confirmed breakdown-and-retest below the intraday swing low with rising volume; do not short into the current wick without that confirmation.
- Watch HYPE/USDT for a pullback into 60.70-60.88 with volume; do not chase 60.96.
- No new stocks action possible before Monday's cash open; carry UNH's manual-review flag forward into the pre-US-open (16:20) and post-close reviews.
- Continue scanning/tracking as normal — no scanner, monitor, or scheduler changes recommended or implied.

## 12. Final Verdict per Mode

- **Crypto scalp**: no fresh actionable idea; today's realized PF is thin (0.14 per the scalp report's own header) — data collection only, per that report's stated posture.
- **Crypto intraday**: no A-tier; existing B-tier momentum names (KAITO/VANRY) are entered-unresolved, not fresh entries. G/USDT is the one clean waiting-for-entry watch.
- **Crypto swing**: report is stale (14h27m); no fresh verdict rendered this cycle — carry forward XEC/ZBT/BANK/AKE context from the 04:47 report with appropriate staleness caveats only.
- **Stocks (all modes)**: market closed; planning/watchlist only. UNH carries a manual-review flag on its existing open C-tier positions; no new stock adds this window.
- **Overall**: **WATCH** — advisory routing only, no auto-trade, no scoring/threshold/strategy changes.

## 13. Sources

- [Bitcoin and ethereum prices today, Friday, July 17, 2026: Prices ease as conflict in Iran escalates](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-july-17-2026-prices-ease-as-conflict-in-iran-escalates-125602208.html) — Yahoo Finance, 2026-07-17
- [US-Iran military escalation sends Bitcoin below $64K as crypto markets feel the heat](https://cryptobriefing.com/us-iran-strikes-bitcoin-crypto-market-drop/) — CryptoBriefing, 2026-07-08
- [UnitedHealth CFO sends stark warning after earnings](https://finance.yahoo.com/healthcare/articles/unitedhealth-cfo-sends-stark-warning-143700508.html) — Yahoo Finance, 2026-07-19 (WebFetch-verified)
- [UnitedHealth (UNH) Faces Broader DOJ Antitrust Probe Into Claritev](https://simplywall.st/stocks/us/healthcare/nyse-unh/unitedhealth-group/news/unitedhealth-unh-faces-broader-doj-antitrust-probe-into-clar) — Simply Wall St News, date unavailable
- [Lorenzo Protocol Price: BANK/USD Live Price Chart, Market Cap & News Today](https://www.coingecko.com/en/coins/lorenzo-protocol) — CoinGecko, 2026-07-19
- Internal: `data/reports/scalp/2026-07-19_15-12_scalp_report.md`, `data/reports/intraday/2026-07-19_15-20_intraday_report.md`, `data/reports/swing/2026-07-19_01-47_swing_report.md`, `data/catalysts/2026-07-19/catalyst_cycle_15-23.md`, `data/catalysts/2026-07-19/catalyst_events.jsonl`

## 14. Fix Requests / TODO

### TODO-1: watchlist-alert → proposed_signal reuse/drop bug, now spanning 3 symbols in one day
- **issue:** Telegram-visible tier-upgrade alerts fire (`previous_tier` → `new_tier=B`) without a matching `proposed_signal` being created, so `detect_untracked_legacy_alerts` cannot track them for PF/winrate/avgR.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-19` → 5 untracked alerts today: ALLO/USDT (09:39 intraday score 67.1, 11:36 scalp score 70.4, 15:36 intraday score 66.7), HOME/USDT (11:57 intraday score 65.2), **BANK/USDT (15:17 scalp score 77.9 — new symbol today)**.
- **suggested manual fix:** investigate why the alert-tier-transition path and the proposed-signal-creation path can diverge; this is a known, recurring issue (raised to high priority 2026-07-17 per prior session context) that continues to spread to new symbols daily.
- **priority:** high (recurring, now 3 symbols)
- **first observed (recurrence dated):** 2026-07-19 19:14 EEST (original issue predates this session)

### TODO-2: NEAR/USDT scalp-short signal unresolved ~48h+ past expiry
- **issue:** `sig_b16bb9e54598333a` (NEAR/USDT, scalp, short, tp1_hit) has `expires_at` 2026-07-17T15:56 but remains in the active-signals table ~48h+ later, never formally closed.
- **evidence:** direct `proposed_signals` query this run confirms status still `tp1_hit`, `expires_at` unchanged since the 18:03 review (which read it as 50h+ — expiry math is consistent, only the reference clock differs).
- **suggested manual fix:** add an automated closure/expiry-sweep job for signals whose `expires_at` has passed but status hasn't been finalized, so "active signals" counts stay accurate.
- **priority:** medium-high
- **first observed:** 2026-07-19 04:40 EEST (growing since)

### TODO-3: catalyst mapping persistently weak (>65% unmapped, multiple cycles running)
- **issue:** unmapped catalyst_events share was 69.8% at 11:39, 67.3% at 18:03, and 65.7% now — essentially flat all day.
- **evidence:** `catalyst_events.jsonl` symbol-null count, this run: 1,741/2,651 (65.7%) unmapped; sample unmapped titles skew toward social/meme chatter and generic macro-policy commentary (GENIUS Act anniversary, CLARITY Act status).
- **suggested manual fix:** improve the symbol resolver's recall for macro/legal/sector commentary that currently maps to nothing.
- **priority:** medium
- **first observed:** prior to 2026-07-19 (recurring across multiple reviews)

### TODO-4: no legal-risk gate on open C-tier stocks positions
- **issue:** the routine's legal/headline-risk check (§I) is scoped to A/B-tier stock candidates only; the open UNH C-tier invest longs (DOJ probe, now reportedly widening to antitrust/Claritev) have no internal flag despite carrying real, evolving legal risk through early August.
- **evidence:** `active-signals --asset-class stocks` — `sig_90b50ceef0d1ebd3` (UNH, C, invest, long, expires 2026-08-01) and `sig_4697b87c9845547f` (UNH, C, invest, long, tp1_hit, expires 2026-07-31); this run's external sourcing (Simply Wall St) confirms the probe has broadened since it was last checked.
- **suggested manual fix:** extend the legal-risk check to any open C-tier position with a multi-week holding window (invest/swing), not just A/B.
- **priority:** low-medium
- **first observed:** 2026-07-19 18:03 EEST (recurring)

### TODO-5: entry_time_basis="historical_not_currently_executable" / expired outcomes on same-day intraday-window signals
- **issue:** the KAITO/VANRY intraday+scalp signals created 15:17-15:20 today resolved to `final_outcome=expired`/`final_r=0.0` with note `entry_time_basis=historical_not_currently_executable` at a 16:10 UTC check — well before their `expires_at` (2026-07-20, next day). This suggests the outcome tracker is applying a shorter internal execution/check window than the signal's own `expires_at`, producing "expired" labels that read confusingly against the still-open `expires_at` field.
- **evidence:** `signal_outcomes` rows for `sig_d1ede52b83aa2493`, `sig_ee300c0093962175`, `sig_7652cf8dfb00935d` — all `status=triggered`, `final_outcome=expired`, `final_r=0.0`, `entry_time_basis=historical_not_currently_executable`, `current_price_revalidated=0`, checked well ahead of the signal's own `expires_at`.
- **suggested manual fix:** clarify (and if needed, align) the relationship between `proposed_signals.expires_at` and the outcome tracker's own resolution window, and consider surfacing `entry_time_basis` in the operator-facing active-signals CLI output so this ambiguity is visible without a raw DB query.
- **priority:** medium (affects lifecycle-language clarity, not scoring)
- **first observed:** 2026-07-19 19:14 EEST
