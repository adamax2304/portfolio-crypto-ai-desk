# Opus Enriched Review — US open reaction review — Auto Cycle 18:39 EEST

## 1. Executive Summary

Advisory only / no auto-trade. **US open reaction review** (~2h10m after the 16:30 EEST / 09:30 ET cash open). Crypto regime is computed as **transition/mixed** (BTC and ETH both uptrend, altcoin breadth 37.5%/42.5% above EMA20/50) but the freshest scalp report's macro/geopolitical score jumped to **83.2/100 risk-off** (vs 45/100 one cycle ago) on a cluster of risk-off headlines — the Iran-US Islamabad ceasefire MoU (signed 17 June) has **frayed, not de-escalated**: Trump declared the initial ceasefire "over" on 8 July after Iranian strikes on a tanker in the Strait of Hormuz, and that tension is still the live backdrop (confirmed via external search, multiple outlets). Stocks regime is **risk_on** (VIX 16.4, breadth 75%/100%) with JPMorgan's Q2 beat driving financials strength — JPM traded **up ~2.8%** post-open (external search confirms this **reverses** the prior review's "sold off pre-market" read) — but **zero A/B-tier stocks setups are actionable this cycle**: every raw A/B candidate (AAPL, AMD, PLTR, META, XLF, JPM, LLY, XLE, COIN, MSTR, XOM) is gate-demoted to C, mainly on `liquidity_rvol_below_min` + `catalyst_none_and_not_exceptional_technical`. A **system-integrity anomaly** was found this cycle: 2 crypto Telegram alerts (HEI/USDT, CRV/USDT) were sent with **no matching proposed_signal** — untracked, will not count toward PF/winrate. AVGO's prior contradiction (internal short vs. Apple's $30B deal) has **resolved** — its score collapsed to 49.6 no-directional, no longer conflicting. UNH's DOJ/Medicare legal-risk flag (confirmed independently via external search: criminal probe now extends to Optum Rx and physician reimbursement) remains **AVOID/MANUAL REVIEW** for existing exposure. Catalyst mapping is weak this run (83.7% unmapped) — use as context only. Scanning, tracking, and the paper book continue uninterrupted in all moods.

## 2. Data Used

- Crypto reports: scalp (15:38 gen / 18:38 mtime, freshness 15:30 UTC), intraday (14:37 gen / 17:37 mtime, freshness 14:30 UTC), swing (02:15 gen / 05:15 mtime, freshness 02:00 UTC — **carry-forward, ~13h24m old at time of this review, borderline stale**)
- Stocks reports: intraday (15:18 gen / 18:18 mtime, regular session, freshness 15:18 UTC)
- Stocks swing/invest reports: last dated **2026-07-02** — **stale (>14h, ~12 days)**, excluded from final verdict; position-framework for stocks swing/invest is deprecated per prior desk decision (see project memory), no fresher source exists, not a new issue
- `data/catalysts/2026-07-14/catalyst_events.jsonl` (3,499 events today), `narrative_baskets.jsonl` (4 baskets)
- `data/processed/llm_analysis_packet.md` (mtime 18:38), `data/processed/llm_stocks_packet.md` (mtime 17:50)
- CLI: `active-signals --asset-class crypto` (22 rows), `active-signals --asset-class stocks` (50 rows), `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`, `detect_untracked_legacy_alerts --since 2026-07-14` (**2 untracked found**)
- Direct read-only SQL against `proposed_signals` / `news_items` for entry zones, statuses, and catalyst-symbol matching (columns truncated in the CLI's fixed-width table)
- External: WebSearch ×5 (HEI/Heima token, Bittensor/TAO news, US market/Iran/JPM open reaction, UNH DOJ probe, Iran ceasefire status) + WebFetch ×1 (Yahoo Finance live markets page) — all resolved successfully

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime 18:38 EEST, latest `cycle_02_17-25_summary.md` mtime 17:54 EEST — both **well under 3h**, no defer needed.
- Latest cycle (started 17:25) completed; pending-monitor and stocks-monitor logs both updated within the last ~10 minutes (18:29–18:30) — paper-tracking pipeline is live and current.
- Swing report is a **carry-forward** (~13h24m old) — borderline-stale band (12–14h); TAO/USDT thesis below is read from it but cross-checked live against `active-signals` and current price context.
- Stocks swing/invest reports are **stale** (~12 days) — excluded, long-horizon context only, deprecated framework (not a fresh issue).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-07-14 18:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale", "derivatives_sparse"],
      "data_missing": ["stocks swing/invest >12d old, excluded", "on-chain flow feeds not live", "OI n/a on many fallback_via_mexc rows"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log/cycle mtime 18:38/17:54", "swing report mtime 05:15 (~13h24m old)", "stocks swing/invest mtime 2026-07-02"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["mixed", "risk_off", "risk_on", "chop"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH both uptrend but macro risk score jumped 45→83.2/100 risk-off intracycle", "stocks: label=risk_on, VIX 16.41, breadth 75%/100%", "Iran ceasefire MoU confirmed frayed since 8 July, not de-escalating"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "no_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["83.7% of today's 3,499 catalyst_events unmapped to a symbol", "HEI/USDT and SYN/USDT are primary in fresh <1h momentum_breakout basket, but neither has a verified news catalyst (checked news_items directly, no matches)", "UNH DOJ/Optum Rx probe independently reconfirmed via WebSearch"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "oi_supports", "data_unavailable"],
      "data_missing": ["OI 24h % n/a for most non-BTC/ETH symbols (fallback_via_mexc)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["TAO/USDT: price down + OI up 8-10% = fresh shorts pressing, squeeze risk on reclaim >201.44 (per original swing entry)", "SXT/USDT: negative funding across venues (bybit -0.0008, mexc -0.002), crowding elevated"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["entry_late", "chase_risk", "price_moved_away", "entry_fresh"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["SXT/USDT still waiting_for_entry but current price 0.0092 already above entry_high 0.008948 — zone was breached without a fill, fresh entries here would be chasing", "SYN/USDT triggered cleanly at 14:46 UTC within its 0.2605-0.2697 zone", "TAO/USDT already tp1_hit, managing not entering"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["open_actionable", "waiting_for_entry", "no_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 22 active signals, all B-tier — 1 waiting_for_entry (SXT), 1 triggered (SYN), 17 tp1_hit, 3 tp2_hit, none expired/stale this cycle", "stocks: 50 active signals, mostly C-tier watchlist/research, 2 B-tier (XOM tp2_hit, NVDA tp2_hit) — none newly actionable this cycle (A/B=0 per stocks report)", "2 crypto Telegram alerts (HEI, CRV) sent with no proposed_signal — needs_review, untracked, excluded from PF/winrate"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["legal_risk", "headline_risk", "reduce_risk", "correlation_cluster"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: DOJ criminal Medicare-billing probe reconfirmed, now extends to Optum Rx and physician reimbursement (external search)", "JPM, NFLX, UNH earnings-window do_not_chase_warning active", "HBAR/LPT/MAGIC/MASK/STG/SUSHI carry delisting/exploit operator-review warnings", "19 of 22 active crypto signals are swing longs in altcoins while macro risk score just jumped to 83.2/100 risk-off — correlation-cluster exposure into a deteriorating macro tape"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto direction=short: PF ~0.5x, n=20 — weak, matches TAO's playbook known-failure-mode note", "crypto scalp mode: PF 0.14, n=37, 0 wins/8 losses — desk's own banner already flags this as low-confidence/data-collection-only", "crypto weekend_mode=Y: PF ~3.2x/n=50 vs weekend=N PF ~0.5x/n=101 (desk's own CLI flags weekend cohort winrate 24% as still underperforming vs. a higher bar)", "stocks: both directions weak this week (long PF~0.7x n=116, short PF~0.9x n=93)", "stocks C-tier tier=C: winrate 11%, PF 0.75 — desk's own CLI observation flags this as below 0.8"] },
    { "agent": "head_trader", "verdict": "manual_review",
      "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "SYN/USDT", "trigger": "already triggered and active (entered 0.2605-0.2697, stop 0.2493); fresh adds only on a hold above the trigger zone with volume, invalidate below 0.2493", "reason": "clean zone-fill this cycle, RS +10.7% vs BTC, but playbook itself flags no-catalyst intraday momentum as historically net-negative (WR 23%/PF 0.70) — treat as a small, managed position, not a chase" },
    "best_short_candidate":    { "symbol": "TAO/USDT", "trigger": "already active (tp1_hit, managing toward TP2 196.05/TP3 191.15); fresh re-entry only on a new 1h failed-bounce retest into 198.99-200.09, invalidate above 201.44", "reason": "external search confirms TAO down -3% 24h / -4% 7d with no bullish reversal catalyst (THORChain integration and Robin τ upgrade are both stale, late-June items) — thesis intact, but crypto short-direction is historically weak (PF ~0.5x) so size any add small" },
    "best_catalyst_candidate": { "symbol": "JPM", "trigger": "not a scored candidate (earnings-day gate blocks new A/B); watch for a clean hold/continuation above today's post-earnings range with volume before treating any JPM-adjacent financials idea (e.g. XLF) as actionable", "reason": "record Q2 profit ($16.9B), stock +2.8% post-open per external search — confirmed catalyst reaction, reverses the prior review's pre-market 'sell-the-news' read, financials (XLF) is the strongest sector (RS +4.4% vs SPY)" },
    "avoid_candidate":         { "symbol": "UNH", "reason": "DOJ criminal Medicare-billing probe independently reconfirmed via external search (now extends to Optum Rx, physician reimbursement); internal signal was raw A (score 80-85) but gate-demoted to C on legal_headline_risk — two open legacy positions (intraday, invest) predate the flag and need a human look" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale, derivatives_sparse | advisory_only |
| market_regime | caution | 0.65 | mixed, risk_off, risk_on, chop | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, fresh_catalyst, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | entry_late, chase_risk, price_moved_away, entry_fresh | advisory_only |
| execution_lifecycle | caution | 0.75 | open_actionable, waiting_for_entry, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.70 | legal_risk, headline_risk, reduce_risk, correlation_cluster | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | manual_review | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-07-14_1628.md` (16:28 EEST, pre-US-open slot):

- **AVGO — contradiction resolved.** No longer a raw B short (was 79.5); today it's `no_trade` at 49.6 with reason `no_directional_setup`. The internal-short-vs-bullish-catalyst conflict flagged last cycle is moot — drop from AVOID list.
- **JPM — "sell-the-news" read reversed.** Prior review flagged JPM trading ~2% lower pre-market despite a beat. External search now confirms JPM **rallied +2.8%** after the open on record $16.9B Q2 profit — the gap-down did not hold. Still not a scored candidate (earnings-day gate).
- **TAO/USDT short — unchanged, still tp1_hit, thesis reconfirmed.** External search (not available/needed last cycle in this depth) shows TAO -3% 24h with no bullish catalyst — supports continuing to manage toward TP2/TP3 rather than closing early.
- **VELVET/USDT — dropped from best-long-watch.** No longer surfaces in the current cycle's top symbols or narrative baskets; SYN/USDT (fresh trigger, 14:46 UTC) and SXT/USDT (waiting-for-entry, zone now breached) take its place as this cycle's live intraday names.
- **NVDA catalyst-watch — no update this cycle;** the China AI-chip-screening story was not independently re-checked this run (external budget prioritized HEI/TAO/JPM/UNH instead); still no_trade technically per stocks report and not scored.
- **New this cycle:** 2 untracked Telegram alerts detected (HEI/USDT, CRV/USDT) — a fresh system-integrity finding not present last cycle's clean `detect_untracked_legacy_alerts` run.
- **New this cycle:** crypto macro/geopolitical risk score jumped from 45/100 to 83.2/100 (risk-off) between the 14:37 and 15:38-generated reports — a fast intracycle deterioration worth watching into the next slot.
- **UNH — unchanged, AVOID/MANUAL REVIEW carries forward;** external search this cycle adds detail (DOJ probe now explicitly named as extending to Optum Rx and physician reimbursement).

## 5. Catalyst Coverage

- Total `catalyst_events` today: **3,499**. Mapped (non-null symbol): **570**. Unmapped: **2,929** (**83.7%**).
- `narrative_baskets`: **4** — delisting_thin_liquidity (primary —), perps_dex_narrative (primary HYPE/USDT, fresh <6h), binance_ecosystem_teaser (primary BNB/USDT, fresh <1h), momentum_breakout (primary HEI/USDT, SYN/USDT, fresh <1h).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (Recurring across multiple recent cycles — see §14 TODO, already tracked, not re-opened as new.)
- Top 3 unmapped headlines (representative sample): "MEHR SAYS SEVERAL AREAS IN SOUTHWESTERN IRAN'S KHUZESTAN'S OMIDIYEH HIT BY U.S. PROJECTILES" (@WalterBloomberg); "EMBC Investors Have Opportunity to Lead Embecta Corp. Securities Fraud Lawsuit" (PR Newswire); "Serve Robotics: A Risky Bet or a Future Winner?" (single-source commentary).

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **mixed, deteriorating toward risk-off intracycle** — BTC/ETH both technically uptrend (altcoin breadth 37.5%/42.5% above EMA20/50), but the macro/geopolitical score jumped from 45→83.2/100 within this cycle on Iran/Strait-of-Hormuz headline flow (ceasefire MoU confirmed frayed since 8 July, not resolved) plus soft-CPI cross-currents. Desk style: "selective only; demand clean invalidation."
- Stocks mood: **risk-on** (VIX 16.41, breadth 75%/100%, financials strongest sector RS +4.4% vs SPY on JPM's earnings beat) but **zero A/B actionable** — every raw A/B candidate demoted to C on liquidity/catalyst gates, not on directional weakness.
- Dominant narrative: crypto — momentum names (SYN, SXT, HEI) pumping without verified catalysts against a worsening macro backdrop; stocks — bank-earnings-driven risk-on tape that the scoring gates aren't yet willing to call actionable.
- Preferred side now: **mixed / wait-for-trigger** — crypto leans "manage existing, don't chase fresh momentum," stocks requires a liquidity/catalyst gate to clear before any new actionable, not just RTH confirmation (already 2h+ past the open).
- Best long candidate: SYN/USDT (already triggered — see §8).
- Best short candidate: TAO/USDT (existing tp1_hit position — see §8).
- Best catalyst-backed candidate: JPM-adjacent financials strength (JPM itself not scoreable — see §8).
- What to avoid: chasing SXT/USDT above its breached entry zone; chasing HEI/USDT or CRV/USDT off the untracked Telegram alerts (no proposed_signal backing them — treat as unverified until the gap is investigated); UNH long exposure without a legal-risk review.
- What would change the view: a fresh Iran/Strait-of-Hormuz headline in either direction, BTC breaking its local range against the mixed-regime thesis, or a genuine verified catalyst emerging for HEI/USDT (currently none found internally or externally).

## 7. Candidate Deep Dives

### SYN/USDT — crypto intraday long (B-tier, 66.0, triggered 14:46 UTC this cycle) — MONITOR, MANAGE EXISTING
- Has price already reacted to the catalyst? No catalyst exists — pure momentum/RS trigger (24h +12.7%, RS vs BTC +10.7%, volume 2.4x).
- Is the setup chasing? Not for the existing fill (entered cleanly inside the 0.2605-0.2697 zone). A brand-new entry now, after the trigger, would be late.
- Retest / pullback structure? Entry was a continuation/pullback fill inside plan; no fresh retest data available post-14:46 UTC (later reports don't re-list SYN's live price).
- Overextended (>2 ATR from EMA20)? Not computable from available fields this cycle.
- Would entry now be late? Yes for fresh size — manage the existing fill only.
- Level that makes an add actionable? A hold above the 0.2605-0.2697 trigger zone with continued volume; invalidate below stop 0.2493.
- Aligned with market mood? Marginal — it's a long in a market whose macro score just deteriorated to 83.2/100 risk-off; reduce conviction accordingly.
- Long, short, or wait? Long (existing), wait for confirmation on any add.
- Actionable now or after confirmation? Existing position is live to manage; adds need confirmation.
- What would invalidate? 1h close below stop 0.2493, or a broader BTC/macro breakdown.
- Chase-risk setup? Yes for any fresh size.
- Catalyst confirmation or contradiction? None found — checked `news_items.detected_symbols_json` directly, no SYN-specific rows in the last 24h. Desk's own playbook note: "no-catalyst intraday in chop is net-negative" (WR 23%/PF 0.70) — treat as small/managed, not conviction.

### SXT/USDT — crypto intraday long (B-tier, 65.3, waiting_for_entry) — DO NOT CHASE, ZONE BREACHED
- Has price already reacted? Yes — 24h +17.1%, 7d +26.7%, RS vs BTC +15.1%, and current price (~0.0092 per the 18:38 scalp report) is already **above** the entry zone high (0.008948) without a documented fill — the zone was breached, not filled.
- Is the setup chasing? Yes, for any entry at current levels.
- Retest / pullback structure? None confirmed since the breach; would need a fresh pullback into (or retest of) the 0.00865-0.00895 zone.
- Overextended? Volume ratio is only 0.07-0.19x of the 20-period average despite the price move — the rally is not backed by strong current volume, a caution flag.
- Would entry now be late? Yes.
- Level that makes it actionable again? A confirmed retest/hold back inside 0.00865-0.00895 with volume pickup; invalidate below stop 0.00829.
- Aligned with market mood? Counter to the deteriorating macro score — a long in a market trending toward risk-off.
- Long, short, or wait? Wait for retest; do not chase.
- Actionable now or after confirmation? After confirmation only.
- What would invalidate? A 1h close below 0.00829, or continued price extension away from the zone without a retest (likely converts to `entry_moved_away`/stale next cycle).
- Chase-risk? Yes, high.
- Catalyst confirmation/contradiction? No fresh verified catalyst detected internally; SXT is negative-funding across venues (bybit -0.0008, mexc -0.002) with "crowding elevated" per the intraday report's cross-check — a mild derivatives caution against the long.

### TAO/USDT — crypto swing short (B-tier, 65.3, tp1_hit) — MANAGE EXISTING, RE-ENTRY ONLY ON FRESH RETEST
- Has price already reacted to a catalyst? No catalyst either way — pure technical/regime trade. External search (Bittensor/TAO) found nothing bullish: price -3% 24h / -4% 7d as of this morning; the two "recent developments" cited by search results (THORChain integration 23 June, Robin τ subnet-capacity upgrade ~22 June) both predate this week and are already priced in.
- Is the setup chasing? Not for the existing position (entered 198.99-200.09, already tp1_hit, managing toward TP2 196.05/TP3 191.15). A brand-new short here needs a fresh retest.
- Retest structure? Original entry was a failed-bounce retest; a new entry requires the pattern to repeat.
- Overextended? Not computable from currently-loaded fields.
- Would entry now be late? For fresh size, likely yes without a new retest.
- Level for a new add? A fresh 1h failed-bounce back into 198.99-200.09; invalidate above 201.44.
- Aligned with market mood? Yes for the existing position — but note crypto short-direction is historically weak overall (PF ~0.5x, n=20) per this cycle's `signal-stats`, so keep any add small.
- Long, short, or wait? Short (existing), wait for confirmation on any add.
- Actionable now or after confirmation? Existing position live to manage; new entries need confirmation.
- What would invalidate? 1h close beyond 201.44, or a verified bullish TAO-specific catalyst (none found this cycle).
- Chase-risk? Yes for any fresh entry at/above current levels.
- Catalyst confirmation/contradiction? No catalyst either way — confirmed via external search as a clean technical/regime trade, no contradicting news found.

### HEI/USDT — crypto intraday, untracked Telegram alert (B-tier score 68.7, sent 14:54 UTC, NO proposed_signal) — SYSTEM-INTEGRITY FLAG, DO NOT TREAT AS A CLEAN SIGNAL
- Has price already reacted to a catalyst? There is a large move (24h +26.2%, RS vs BTC +24.2%, momentum score 86.3) but **no verified catalyst was found** — checked `news_items.detected_symbols_json` directly (no HEI-specific rows in the last 24h) and ran an external search: HEI is "Heima," a Layer-1 settlement-layer token; the only recent structural news found is a governance proposal to burn 16.5M tokens (~18.7% of supply), dated **31 May 2026** — stale, not a fresh driver of today's move.
- Is the setup chasing? Yes if treated as a fresh long — the move is already 24h old and unconfirmed.
- Retest / pullback structure? Not evaluated — no proposed_signal exists to define one; this alert has no tracked entry/stop/TP.
- Overextended? Momentum score 86.3/100 with no narrative-basket catalyst beyond the desk's own `momentum_breakout` basket tag (fresh <1h, single_source, unverified).
- Would entry now be late? Cannot be assessed — no defined entry plan exists for this alert.
- Level that makes it actionable? None currently — this needs an operator to reconcile why a Telegram alert fired without a corresponding `proposed_signal` row before it should be treated as tradeable at all.
- Aligned with market mood? Momentum-only long in a market whose macro score is deteriorating — would be counter-trend risk even if it had a plan.
- Long, short, or wait? Wait — this is a data-integrity issue, not a trade decision.
- Actionable now or after confirmation? Neither — flagged for manual/operator review (see §14 TODO).
- What would invalidate/resolve? Root-causing why `watchlist_alerts` fired for HEI/USDT and CRV/USDT without a matching `proposed_signal` within 6h.
- Chase-risk? Yes, if anyone acts on the raw alert without a tracked plan.
- Catalyst confirmation/contradiction? **No catalyst found**, internal or external — this is a pure momentum move with no supporting news, and the underlying signal itself was never properly tracked.

### UNH (UnitedHealth) — stocks long (raw A, 80.x) → demoted to C (legal_headline_risk) — AVOID / MANUAL REVIEW
- Has price already reacted? Yes — external search reconfirms the DOJ criminal Medicare-billing probe (fraud-related diagnosis inflation allegations) is active and has **now been reported to extend to Optum Rx and physician reimbursement** as well, beyond the original Medicare Advantage scope. Stock has fallen sharply over the past year on this and other pressures (down ~55% from ATH per one source), though analyst consensus remains Buy with meaningful implied upside — a genuinely two-sided, not one-sided, risk picture.
- Is the setup chasing? Not applicable — gated before entry consideration for new signals.
- Retest structure? Not evaluated (chart tools unavailable).
- Overextended? Not computable.
- Would entry now be late? The desk's own gate already blocks this from becoming a fresh A/B; the live question is the **existing legacy UNH exposure** in `active-signals` (multiple C-tier rows, intraday/invest, various directions and statuses) that predate the flag.
- Level that makes it actionable? N/A while the legal flag is active.
- Aligned with market mood? Healthcare is a mixed-to-moderate sector today (not a top-3 mover); company-specific legal risk dominates regardless.
- Long, short, or wait? Wait / manual review of existing exposure.
- Actionable now or after confirmation? Manual review required regardless of confirmation — legal-risk gate, not a technical-confirmation gate.
- What would invalidate (clear) the flag? Resolution or material narrowing of the DOJ probe's scope — not observed this cycle; if anything the scope was reported wider (Optum Rx, physician reimbursement) than before.
- Chase-risk? N/A.
- Catalyst confirmation/contradiction? **Confirmation of an ongoing and widening legal risk** — final verdict stays AVOID/MANUAL REVIEW, never a clean actionable.

## 8. Best Candidates Ranked

1. **TAO/USDT — best short (existing, monitor); best short-watch for a fresh add.** Managing toward TP2 196.05/TP3 191.15. Fresh-entry trigger: new 1h failed-bounce retest into 198.99-200.09, invalidate above 201.44. Thesis reconfirmed clean via external search (no bullish TAO catalyst found).
2. **SYN/USDT — best long (existing, monitor).** Entered cleanly 0.2605-0.2697, stop 0.2493. No catalyst backing (playbook known-failure-mode); manage small, don't add without a hold-above-trigger confirmation.
3. **JPM-adjacent financials strength — best catalyst-watch.** JPM itself not scoreable (earnings-day gate); trigger for any XLF/financials idea: a confirmed hold of today's post-earnings gains with volume, not the headline alone.
4. **UNH — avoid / manual review** for existing exposure; new entries already blocked by the desk's own gate; DOJ scope reported wider this cycle.
5. **HEI/USDT (and CRV/USDT) — system-integrity watch, not a trade candidate.** Do not act on either raw Telegram alert until the untracked-signal gap is resolved (§14). SXT/USDT is a secondary long-watch but **do not chase** — its entry zone (0.00865-0.00895) is already breached; wait for a retest.

## 9. Avoid / No Trade (this decision window only)

- **Chasing SXT/USDT** above its breached entry zone (current ~0.0092 vs. zone top 0.008948) — wait for a retest.
- **Acting on the HEI/USDT or CRV/USDT Telegram alerts** as if they were tracked signals — neither has a `proposed_signal`, entry, stop, or TP; this is a data-integrity gap, not a trade setup.
- **UNH long exposure** without a legal-risk review; DOJ scope reported wider this cycle, not narrower.
- **Chasing any stocks name off the JPM/earnings headline** — every raw A/B stock candidate remains gate-demoted to C this cycle regardless of the risk-on tape; require the gates to clear, not just RTH time elapsed.
- This is a decision-window-only call — scanning, tracking, candidate generation, and outcome recording continue in all cases; nothing here is a command to pause any part of the system.

## 10. Main Risks

- Geopolitical: the Islamabad Iran-US ceasefire MoU (17 June) has frayed since 8 July (Trump declared it "over" after an Iranian tanker strike in the Strait of Hormuz); this is the likely driver behind the intracycle jump in the crypto macro-risk score from 45 to 83.2/100 — not a resolved situation, still live into the next slot.
- Concentration: 19 of 22 active crypto signals are swing longs in altcoins, now sitting against a macro score that just deteriorated sharply within this cycle — a correlation cluster that could unwind together.
- Data-integrity: 2 untracked Telegram alerts this cycle (HEI/USDT, CRV/USDT) — until root-caused, any similar future alert should be treated with the same suspicion (see §14).
- Catalyst-mapping is weak this run (83.7% unmapped) — treat the catalyst layer as context only, not a standalone decision input (recurring, already tracked).
- Legal/headline: UNH's DOJ probe scope was reported wider this cycle (Optum Rx, physician reimbursement) — existing legacy exposure is a live manual-review item, not a resolved flag.
- Historically weak buckets to lean against this week: crypto short-direction signals (PF ~0.5x, n=20), crypto scalp mode (PF 0.14, 0 wins/8 losses — desk already treats scalp as data-collection-only), stocks C-tier overall (winrate 11%, PF 0.75, both below the desk's own 0.8 bar).

## 11. Action Plan — next 4 hours

- Manage TAO/USDT toward TP2 196.05; only add on a fresh 1h failed-bounce retest into 198.99-200.09, invalidate above 201.44.
- Manage SYN/USDT toward its stated TP ladder (TP1 0.2941/TP2 0.3145/TP3 0.3348); do not add fresh size without a confirmed hold above the 0.2605-0.2697 trigger zone.
- Do not enter SXT/USDT at current levels; wait for a retest back into 0.00865-0.00895 with a volume pickup.
- Root-cause (operator task, not this run) why HEI/USDT and CRV/USDT Telegram alerts fired without a matching `proposed_signal` — until resolved, treat both as unverified/untracked, not tradeable signals.
- Keep UNH on manual-review status for existing legacy exposure; DOJ scope was reported wider this cycle.
- Watch for whether stocks A/B candidates (AAPL, AMD, PLTR, META, XLF, JPM, LLY, XLE, COIN, MSTR, XOM) can clear the `liquidity_rvol_below_min` / `catalyst_none_and_not_exceptional_technical` gates later in the session as intraday volume builds — none are actionable as of this review.
- Continue monitoring Iran/Strait-of-Hormuz headline flow as the dominant driver behind the crypto macro-risk-score jump; a further escalation or a genuine de-escalation would meaningfully change the crypto mood call.

## 12. Final Verdict per Mode

- **Crypto scalp**: No A-tier, no B-tier. No trade (desk's own banner: data-collection-only, PF 0.14).
- **Crypto intraday**: No new A-tier. Managing 1 triggered B-tier (SYN/USDT long) + 1 waiting-for-entry B-tier (SXT/USDT, zone breached — do not chase). 2 untracked Telegram alerts (HEI, CRV) flagged, not actionable.
- **Crypto swing**: No A-tier. Managing 1 B-tier (TAO/USDT short, tp1_hit) toward TP2/TP3; fresh adds need retest confirmation.
- **Stocks intraday**: No A/B-tier actionable — every raw A/B candidate gate-demoted to C this cycle despite a risk-on tape. Manual review flagged for UNH (existing legacy exposure).
- **Stocks swing/invest**: Stale data (>12 days) / framework deprecated — no verdict, carry-forward context only.
- **Overall**: CAUTION, routed by side — not a blanket no-trade. Manual review flagged for UNH and for the HEI/CRV untracked-alert integrity gap.

## 13. Sources

- [Heima Price: HEI/USD Live Price Chart, Market Cap & News Today — CoinGecko](https://www.coingecko.com/en/coins/heima) (accessed 2026-07-14)
- [HEIUSDT Charts and Quotes — TradingView](https://www.tradingview.com/symbols/HEIUSDT/) (accessed 2026-07-14)
- [Bittensor price today, TAO to USD live price, marketcap and chart — CoinDesk](https://www.coindesk.com/price/tao) (accessed 2026-07-14)
- [Latest Bittensor News — CoinMarketCap](https://coinmarketcap.com/cmc-ai/bittensor/latest-updates/) (accessed 2026-07-14)
- [Stock market today: S&P 500, Nasdaq, Dow futures slip as Iran tensions ratchet up, bank earnings and Fed report on deck — Yahoo Finance](https://finance.yahoo.com/markets/stocks/live/stock-market-today-tuesday-july-14-231302282.html) (2026-07-14, fetched directly)
- [US Stock Market Today: Dow Jones, Nasdaq & S&P 500 Rises... Bank Stocks Rally — Sunday Guardian Live](https://sundayguardianlive.com/business/us-stock-market-today-dow-jones-nasdaq-sp-500-rises-as-ibm-crashes-24-bank-stocks-rally-bitcoin-oil-surges-2-gold-silver-prices-fall-amid-us-iran-tensions-what-investors-should-watch-236552/) (2026-07-14)
- [2026 Iran war ceasefire — Wikipedia](https://en.wikipedia.org/wiki/2026_Iran_war_ceasefire) (accessed 2026-07-14)
- [How the US-Iran ceasefire and MOU broke down — a timeline — ABC News](https://abcnews.com/Politics/us-iran-ceasefire-mou-broke-timeline/story?id=134622392) (accessed 2026-07-14)
- [Explainer-Why Has the Iran-US Ceasefire Memorandum Frayed? — US News](https://www.usnews.com/news/world/articles/2026-07-13/explainer-why-has-the-iran-us-ceasefire-memorandum-frayed) (2026-07-13)
- [UnitedHealth stock sinks 4.7% after company confirms DOJ investigation into Medicare billing practices — Yahoo Finance](https://finance.yahoo.com/news/unitedhealth-stock-sinks-47-after-company-confirms-doj-investigation-into-medicare-billing-practices-133527260.html) (accessed 2026-07-14)
- [DOJ's criminal probe into UnitedHealth extends to Optum Rx, physician reimbursement — FierceHealthcare](https://www.fiercehealthcare.com/payers/wsj-report-doj-interviewing-former-employees-about-medicare-billing-practices-unitedhealth) (accessed 2026-07-14)
- Internal: `data/reports/scalp/2026-07-14_15-38_scalp_report.md`, `data/reports/intraday/2026-07-14_14-37_intraday_report.md`, `data/reports/swing/2026-07-14_02-15_swing_report.md`, `data/reports/stocks/intraday/2026-07-14_15-18_stocks_intraday_report.md`, `data/catalysts/2026-07-14/catalyst_events.jsonl`, `data/catalysts/2026-07-14/narrative_baskets.jsonl`, `db/crypto_ai_desk.sqlite` (`proposed_signals`, `news_items` direct queries)

## 14. Fix Requests / TODO

### TODO-untracked-telegram-alerts-2026-07-14
- **issue:** `detect_untracked_legacy_alerts` found 2 crypto Telegram alerts sent this cycle with no matching `proposed_signal` within 6h — HEI/USDT (B, intraday, 68.7, long, sent 14:54:37 UTC) and CRV/USDT (B, intraday, 67.4, long, sent 15:02:23 UTC). These alerts will not contribute to PF/winrate/avgR since the tracker has no signal_id to follow, and there is no entry/stop/TP plan for an operator (or this review) to evaluate.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-14` output; cross-checked `db/crypto_ai_desk.sqlite.proposed_signals` — no row for either symbol with `created_at` near the alert `sent_at` timestamps.
- **suggested manual fix:** Investigate the Telegram-alert dispatch path for a race condition or write failure between `watchlist_alerts` insert and `proposed_signals` insert around 14:54-15:02 UTC on 2026-07-14; check for an exception in `scheduler.log` around that window that may have aborted signal creation after the alert was already queued/sent.
- **priority:** medium
- **first observed:** 2026-07-14 18:39 EEST (this cycle — first time this specific detector has returned non-clean output in the reviews inspected this session).

### TODO-catalyst-mapping-weak
- **issue:** Catalyst-event → symbol mapping is at 83.7% unmapped for today's cycle (2,929 of 3,499 events have no `symbol`), well above the 50% weak-mapping threshold, and this has recurred across multiple recent auto-review cycles (84.6% at 16:28, similar figures at 11:39 and earlier today).
- **evidence:** `data/catalysts/2026-07-14/catalyst_events.jsonl` — 570 mapped / 3,499 total; sampled unmapped headlines include clearly symbol-relevant items (e.g. "EMBC Investors Have Opportunity to Lead Embecta Corp. Securities Fraud Lawsuit" — ticker EMBC is present in the title text) that the resolver failed to attach.
- **suggested manual fix:** Revisit the symbol resolver in the catalyst layer (ticker/company-name extraction from title text), especially for the recurring "Investors Have Opportunity to Lead ... Securities Fraud Lawsuit" PR-Newswire template, which reliably contains a ticker but is landing unmapped.
- **priority:** medium (unchanged from prior cycles — carried forward, not re-escalated)
- **first observed:** 2026-07-14 11:39 EEST (prior review cycle); still present 2026-07-14 18:39 EEST.
