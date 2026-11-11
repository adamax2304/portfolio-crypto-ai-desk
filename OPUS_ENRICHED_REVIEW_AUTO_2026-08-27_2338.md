# Opus Enriched Review — post-close final daily review — Auto Cycle 23:15 EEST

## 1. Executive Summary

**Slot: post-close final daily review (advisory only / no auto-trade).** Scheduler cycle_02 (started 18:25 EEST) just finished writing its summary at 23:23 — fresh. Underlying scalp/intraday/stocks-intraday reports are unchanged since the 21:48 review (same source files); swing report is a 7.7h carry-forward. Crypto: zero fresh A/B this cycle, but the RS-momentum swing cohort (CHIP/RUNE/S/MOVR/PROM/TAO/…) is open and mostly triggered/managing — book is 100% long, zero shorts triggered all week. Stocks: zero A/B actionable (all 15 raw-A candidates gate-demoted to C by the rolling paper-R drawdown guard, earnings, or a contested legal-risk tag on NVDA). Catalyst mapping weak (74.7% unmapped, mostly macro central-bank noise) — use as context only. The ONG/USDT bias-tag contradiction (open long vs. current short-bias tag) is unresolved for a third consecutive review — still the top integrity item. Scanning, tracking, and the scheduler continue regardless of tonight's verdict.

## 2. Data Used

- `data/reports/scalp/2026-08-27_15-47_scalp_report.md` (generated 18:42 EEST, ~4.9h old)
- `data/reports/intraday/2026-08-27_16-34_intraday_report.md` (generated 19:32 EEST, ~4.1h old)
- `data/reports/swing/2026-08-27_12-46_swing_report.md` (generated 15:45 EEST, ~7.9h old — **carry-forward**)
- `data/reports/stocks/intraday/2026-08-27_18-31_stocks_intraday_report.md` (data freshness 18:31 UTC = 21:31 EEST, ~2.1h old — fresh)
- `data/reports/stocks/swing/2026-07-02_...` and `data/reports/stocks/invest/2026-07-02_...` — **~8 weeks stale, excluded**
- `data/catalysts/2026-08-27/catalyst_events.jsonl` (2,500 events), `narrative_baskets.jsonl` (5 baskets)
- `active-signals --asset-class crypto` (50 rows), `active-signals --asset-class stocks` (50 rows, all historical/closed)
- `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`
- `detect_untracked_legacy_alerts --since 2026-08-27` (7 hits)
- `news_items` table direct queries (ONG/USDT, CHIP/USDT, TAO/USDT, RUNE/USDT — 24h window)
- `proposed_signals` table direct query (ONG/USDT history, 8 rows)
- 1 WebSearch (ONG/USDT price-move verification) — external web research available this cycle.
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-27_2148.md`

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: 2026-08-27 23:23:25 EEST — **fresh** (<1h old at review time 23:38).
- Latest cycle summary: `cycle_02_18-25_summary.md`, mtime 23:23:20 EEST — **fresh**.
- Both fresh → no defer needed.
- Report-level freshness: scalp/intraday ~4-5h old (same cycle, still within the cycle window); swing 7.9h old → **carry-forward** per the 4-12h rule, flagged accordingly in §7; stocks-intraday fresh (~2.1h); stocks swing/invest excluded (8wk stale).
- No monitor/paper-portfolio status file was read this cycle (out of the allowed read set); not blocking.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "post_close",
  "as_of": "2026-08-27 23:38 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["scheduler_fresh"],
      "data_missing": ["stocks swing/invest reports (last 2026-07-02, ~8wk stale, excluded)", "swing report is a 7.9h carry-forward, not fresh this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 23:23:25 EEST", "cycle_02_18-25_summary.md mtime 23:23:20 EEST", "swing report generated 15:45 EEST"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["mixed", "longs_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/ETH uptrend, altcoin breadth 72-89% above EMA50 (swing report)", "macro/geopolitical risk score 79-100/100 risk-off across all 3 crypto reports today", "stocks regime label=transition, risk_on=False, VIX=14.64, breadth 100% above EMA20/50"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "fresh_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["2500 catalyst_events today, 633 mapped (25.3%), 1867 unmapped (74.7%) — mostly BOJ/BOK macro commentary", "SOL/USDT, ZEC/USDT, ZRO/USDT carry internally-verified fresh catalysts"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.55,
      "reason_codes": ["oi_supports", "data_unavailable"],
      "data_missing": ["MSTRB/USDT futures data unavailable", "GOOGLB/USDT no external futures data"],
      "suggested_effect": "advisory_only",
      "facts_used": ["CHIP/RUNE/S/TAO/VET all show price-up+OI-up fresh positioning, crowding normal", "no funding extremes flagged in scalp/intraday/swing reports"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TRUMP/CHIP explicitly rejected on scalp timeframe: >2 ATR from EMA20, do not chase", "swing B-tier cohort (CHIP/RUNE/S/TAO/SOL) defines pullback-only entry zones below current price, not market-buy"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals: 43 open/managed (triggered+tp1_hit), 7 waiting_for_entry, 1 needs_review (ONG/USDT)", "stocks active-signals: 50 rows, all historical tp1_hit/tp2_hit with expires_at in the past — 0 live open today"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["correlation_cluster", "headline_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto book 100% long, 0 shorts triggered all week (signal-stats direction table)", "crypto_swing_narrative_rs_momentum playbook's own known-failure-mode: BTC dump invalidates the whole correlated cohort", "macro risk score 94-100/100 today (Iran war, Strait of Hormuz, Saudi-Houthi tension)", "HON legal-risk (Honeywell investigation) live operator-review flag"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto mode=scalp PF 0.05 this week (matches report's own low-confidence banner)", "crypto mode=intraday PF 1.98, mode=swing PF 1.78 — both working", "stocks sector=financials PF 2.67 vs technology/healthcare/semiconductors negative PF", "stocks A/B sample n=10, confidence=weak"] },
    { "agent": "head_trader", "verdict": "ok", "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.62,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "CHIP/USDT", "trigger": "pullback fill into 0.0362-0.0368, no market buy if extended", "reason": "tied top swing score 72.4, RS-leader + momentum basket, price-up+OI-up, but no fresh verified catalyst — pullback-only, chase-risk on faster timeframes" },
    "best_short_candidate":    { "symbol": "GOOGLB/USDT", "trigger": "confirm bearish HTF structure + derivatives data + clear stop above swing high", "reason": "weak_rs_short expansion-watchlist candidate, -3.4% RS vs BTC, 3.0x unusual volume, not yet promoted — squeeze risk on upper wick until confirmed" },
    "best_catalyst_candidate": { "symbol": "SOL/USDT", "trigger": "pullback fill into 103.34-104.05, invalidation 1h close beyond 102.48", "reason": "internally-verified fresh catalyst (DeFi Development 'State of Solana' platform launch), canonical_news_event, importance 0.75" },
    "avoid_candidate":         { "symbol": "ONG/USDT", "reason": "active bias-tag contradiction (open swing long since 08-26 vs. current desk snapshot tagging ONG bias=short, 24h -26.09%, RS -29.20%) — needs operator review before any new action either direction; 3rd consecutive review cycle unresolved" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.70 | scheduler_fresh | advisory_only |
| market_regime | caution | 0.65 | mixed, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, fresh_catalyst | advisory_only |
| derivatives_squeeze | ok | 0.55 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, clean_retest | advisory_only |
| execution_lifecycle | ok | 0.75 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.70 | correlation_cluster, headline_risk, reduce_risk | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | ok | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-27_2148.md` (21:48 EEST, same underlying scalp/intraday/stocks-intraday source reports — the scheduler cycle has not produced new reports since).

- **Unchanged:** No fresh A/B in crypto or stocks this cycle (same as 21:48 and 18:39). Catalyst mapping still weak (74.7% unmapped, same order of magnitude). Macro risk-off headwind persists (94-100/100). ONG/USDT bias-tag contradiction still open — **now confirmed unresolved across 3 consecutive cycles** (18:39 → 21:48 → 23:15).
- **New/confirmed this cycle:** Untracked legacy alert count is 7 today (same count as previously reported, confirms the recurrence is a same-day pattern, not a one-off). NVDA's stocks demotion reason ("legal/headline risk: indictment") was cross-checked against its underlying news item — the actual story is a bullish M&A headline (Nvidia agreeing to buy Hugging Face for $12.9B) with a tangential "previously hacked" mention about Hugging Face itself, not Nvidia — this looks like a legal-risk classifier false-positive, not a real indictment. Flagged as new TODO (§14).
- **Resolved/expired:** The 18:39/21:48 review's "NVDA/INTC/CRM stocks watch, ~1h15m to session close" item has now resolved — the RTH session is fully closed; those stocks-intraday B-tier ideas are gone from the current report (0 A/B, only C-tier watchlist remains).
- **No change in thesis** for the crypto swing RS-momentum cohort (CHIP/RUNE/S/MOVR/PROM/TAO/etc.) — still open, still chase-risk-flagged for fresh entries, manage existing positions to their stated invalidation only.

## 5. Catalyst Coverage

- Total `catalyst_events` today: **2,500**. Mapped (non-null symbol): **633 (25.3%)**. Unmapped: **1,867 (74.7%)**.
- `narrative_baskets` today: **5** (binance_ecosystem_teaser, perps_dex_narrative, ai_narrative, momentum_breakout, plus 1 additional not detailed in the report excerpts).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (sampled): central-bank commentary, not symbol-specific — "BOJ'S HIMINO: FINANCIAL CONDITIONS STAY ACCOMMODATIVE…", "BOJ'S HIMINO: THE BIGGEST CHALLENGE IN OUR COMMUNICATION…", "BOK: FUTURE INFLATION PATH HIGHLY UNCERTAIN…". These are legitimate macro-context items that don't map to a single symbol by design — the weak-mapping % is expected to run high on macro-heavy news days and is not itself a pipeline bug.

## 6. Market Landscape

Crypto: BTC/ETH both in uptrend, altcoin breadth strong (72.92% above EMA20, 89.58% above EMA50 per the swing snapshot), regime label swung from "range/chop" (scalp/intraday, earlier in the cycle) to "bullish trend (risk-on)" (swing, mid-afternoon read) — the desk's own regime label has been inconsistent intraday, which is itself worth noting rather than picking one read as final. Underneath the constructive price action, the macro/geopolitical risk score has been elevated all day (94-100/100), driven by Iran-war-adjacent headlines (Strait of Hormuz, Saudi-Houthi escalation risk, US Iran sanctions) — a real source of gap/reversal risk a pure price read would miss.

Stocks: regime label **transition**, bias neutral, VIX low (14.64), breadth 100% above EMA20/50 — technically strong but the desk's own risk_on flag reads False, and 15 of 15 raw-A candidates were gate-demoted to C tonight (mostly the rolling paper-R drawdown guard on stocks-intraday longs, plus 2 legal/earnings-driven demotions). Financials sector is the standout performer this week (PF 2.67); technology/healthcare/semiconductors are net-negative in the weekly stats despite today's raw-A tilt being almost entirely large-cap tech/growth names (CRM, ADBE, MSFT, NVDA, TSLA, PLTR, CRWD…) — a real disconnect between today's raw scores and the sector's recent realized edge.

### Market Mood / Risk Routing
- Crypto mood: **mixed** (risk-on price action, risk-off macro overlay)
- Stocks mood: **transition / neutral** (post-close; RTH closed, low VIX, gate-heavy)
- Dominant narrative: crypto RS-momentum / narrative-basket rotation (AI, momentum-breakout, binance-ecosystem); stocks — large-cap tech raw scores vs. financials realized edge
- Preferred side now: **longs (crypto, pullback-only)** / **wait-for-trigger (stocks, session closed)**
- Best long candidate: CHIP/USDT — pullback fill into 0.0362-0.0368, invalidation 1h close beyond 0.0355
- Best short candidate: none clean — best short-watch is GOOGLB/USDT, trigger: confirm bearish HTF structure + derivatives + stop above swing high
- Best catalyst-backed candidate: SOL/USDT — pullback fill into 103.34-104.05, invalidation 102.48
- What to avoid: ONG/USDT (active bias-tag contradiction, needs operator review); fresh entries on TRUMP/CHIP at current extended scalp-timeframe prices; AFRM/MRVL (earnings today, already past close but avoid any pre-market chase tomorrow); NVDA (contested legal-flag, manual review pending, see §14)
- What would change the view: BTC losing local support (invalidates the long-only correlated swing cohort per the playbook's own known-failure-mode); a resolved/verified ONG bias check; catalyst mapping recovering toward symbol-specific (not macro) coverage; a fresh A/B clearing stocks-intraday gates after tomorrow's open

## 7. Candidate Deep Dives

### 1. CHIP/USDT — LONG (best long candidate)
- Score 72.4/100 (swing, tied top), confidence medium. Also appears in scalp (top mover, score 100 on 24h momentum) and intraday (rejected/watchlist, chase risk).
- Has price already reacted? Yes — 24h +11.52%, 7d +21.01%, well above the planned pullback zone.
- Chasing? On the scalp/intraday timeframe, yes — explicitly rejected in the scalp report for being >2 ATR from EMA20. On the swing timeframe, no — the B-tier idea is a defined pullback-only plan (0.0362-0.0368), not a market buy at the current 0.0371 print.
- Retest/pullback structure? Yes, that is the entire swing thesis.
- Overextended >2 ATR from EMA20? Yes on fast timeframes; the swing plan is designed around waiting for that extension to unwind.
- Would entry now be late? Yes if bought at market; no if the pullback zone fills.
- Actionable level: 0.0362-0.0368 fill, invalidation 1h close beyond 0.0355.
- Mood alignment: aligned with the risk-on price leg, but the macro overlay argues for smaller size / faster invalidation respect.
- Catalyst: none internally verified (checked `news_items`, 0 matches in the last 24h for CHIP).
- Chase-risk setup: yes on fast timeframes — this is a manage/pullback-only idea, not a breakout chase.
- Counter-thesis (from report): RS not backed by strong current volume (0.3x), no fresh catalyst, beta-bounce risk if BTC breaks down.

### 2. SOL/USDT — LONG, catalyst-backed
- Score 66.8/100 (swing), 68.0 (intraday watchlist, per untracked-alert log). Fresh catalyst: "DeFi Development launches real-time 'State of Solana' intelligence platform" (The Block), canonical_news_event, importance 0.75.
- Price reaction: 24h +7.57% — already moved, not chasing further at current print (104.36).
- Retest structure: yes, pullback zone 103.34-104.05, invalidation 102.48.
- Overextended: moderate, not flagged as >2 ATR.
- Catalyst confirmation: internally verified, single named source (The Block) — treat as confirmed but not overwhelming (importance 0.75/low-moderate).
- **Data-integrity note:** SOL/USDT also appears 3× in today's `detect_untracked_legacy_alerts` output (scalp, intraday, swing legacy Telegram alerts with no matching `proposed_signal`) — the same symbol firing repeated untracked alerts is a live instance of the known TODO-3 bug (see §14). Treat SOL's Telegram alert history with reduced confidence until that's fixed; the swing-report B-tier idea itself is properly tracked (`sig_4a29d733a07930ab`).

### 3. GOOGLB/USDT — SHORT-WATCH
- Discovery-expansion candidate, `crypto_failed_bounce_short` playbook, score 70, RS vs BTC -3.4%, 3.0x unusual volume (tags: weak_vs_market, volume_expansion).
- Status: in-top but not yet promoted to B-tier; "squeeze_risk_upper_wick (avg upper-wick 2.7× ATR)" flagged in the expansion table — a real caution on shorting into an upper-wick-heavy name.
- Trigger to promote: confirm bearish HTF structure + derivatives data + clear stop above swing high.
- Not actionable tonight — surfaced as the cleanest short-side idea in an otherwise 100%-long book, for balance and to keep short-side muscle memory active.

### 4. ONG/USDT — NEEDS REVIEW / AVOID
- Open swing long, `sig_8d3a8fd71bf0bf75`, triggered 2026-08-26T02:59:24, entry 0.09561-0.09824, invalidation 0.09240, score 73.9. Also `waiting_for_entry` swing sig_5fc650550d967342 (score 69.7) and a closed `tp1_hit` scalp signal from 08-25.
- Current desk snapshot (scalp report, 18:47 EEST) tags ONG/USDT as one of the **weakest** symbols: bias=short, 24h -26.09%, RS vs BTC -29.20%.
- `news_items` check: **0 matches** for ONG/USDT in the last 24h — no internal catalyst explains the move either direction.
- External WebSearch (Forbes Digital Assets snapshot) returned a conflicting read: ONG priced $0.1571, **+61.2%** 24h as of "August 27" — directly contradicts the internal -26% figure. Source has no clear intraday timestamp; treat as **unverifiable / conflicting**, not a resolution. [Ontology Gas (ONG) Price Today, News & Live Chart](https://www.forbes.com/digital-assets/assets/ontology-gas-ong/)
- This is the same bias-tag-contradiction pattern flagged in the prior 2 reviews (18:39, 21:48) and matches the broader recurring pattern in project memory (ZBT/ACE, 2026-08-08). **Third consecutive cycle unresolved.**
- Verdict: **AVOID / MANUAL REVIEW REQUIRED** — do not add to the open long, do not open a fresh short, until an operator confirms current live price against the 0.09240 invalidation.

### 5. NVDA (stocks) — WATCH, contested legal-risk tag
- Raw A-tier score 83.15, demoted A→C citing "active legal/headline risk (indictment) — manual review required."
- Underlying news items (checked in-report): "Nvidia has agreed to buy Hugging Face for $12.9B" (bullish M&A) and a Telegram repost calling Hugging Face "the AI platform that an OpenAI agent previously hacked" — a reference to a past third-party incident at Hugging Face, not an indictment of Nvidia.
- No SEC/DOJ/class-action item naming NVDA specifically was found in the report's legal/SEC feed for this date.
- Assessment: this reads as a legal-risk **classifier false-positive** (exploit_hack tag on a related company misrouted into an "indictment" cap on NVDA), not a verified legal risk. Per the source-discipline rule, this is **not** asserted as a confirmed legal risk — flagged as a TODO for a human to check the classifier (§14), and NVDA stays non-actionable regardless (gate already demoted it; no live A/B stocks setups exist tonight either way).

## 8. Best Candidates Ranked

1. **ONG/USDT** — NEEDS REVIEW (top priority — unresolved bias-tag contradiction, 3rd consecutive cycle).
2. **CHIP/USDT** (long-watch, crypto) — best fresh swing idea, wait for pullback fill into 0.0362-0.0368.
3. **SOL/USDT** (catalyst-watch, crypto) — pullback fill into 103.34-104.05, internally-verified catalyst.
4. **GOOGLB/USDT** (short-watch, crypto) — needs bearish HTF + derivatives confirmation before promotion; best available short-side idea in a long-only book.
5. **RUNE/USDT/S/USDT cohort** (crypto, manage-only) — open at the same top swing score as CHIP, same pullback-only discipline, no fresh catalyst.

## 9. Avoid / No Trade (this decision window only)

- **ONG/USDT** — any new long or short action pending operator review of the bias contradiction and current live price vs. 0.09240 invalidation.
- **TRUMP/CHIP** — fresh entries rejected on the scalp/fast timeframe for chase risk (>2 ATR from EMA20); the swing pullback plan is the only valid entry path.
- **NVDA** — manual review required (contested legal-tag, see §7.5 and §14); no live A/B stocks setups exist tonight regardless.
- **HON, ATOM** — live `block_requires_operator_review` flags (Honeywell investigation, Cosmos Labs exploit-hack warning).
- Stocks broadly — 0 A/B actionable tonight, RTH closed; nothing to chase pre-market off tonight's data.
- This is a decision-window verdict only — scanning, candidate generation, tracking, and the scheduler continue in all cases; nothing here recommends pausing any part of the system.

## 10. Main Risks

- **ONG/USDT bias-tag contradiction**, unresolved 3 consecutive cycles — the most concrete risk-integrity issue tonight, compounded by conflicting external price data (see §7.4).
- **Crypto book is 100% long, 0 shorts triggered all week** (signal-stats direction table) — no short-side capacity is currently being exercised; if the risk-on regime reverses, the desk has no recent short track record to lean on. GOOGLB/USDT is the only short-side candidate anywhere near promotion.
- **Correlated swing cohort risk** — CHIP/RUNE/S/MOVR/PROM/TAO/etc. all share the same `crypto_swing_narrative_rs_momentum` playbook; its own documented failure mode is a BTC dump invalidating the whole basket at once.
- **Macro risk-off headwind (79-100/100) under a bullish crypto tape** — Iran-war-adjacent geopolitical risk (Strait of Hormuz, Saudi-Houthi tension, widened Iran sanctions) sitting underneath BTC/ETH uptrend and strong altcoin breadth.
- **Catalyst mapping weak (74.7% unmapped)** — mostly legitimate macro noise (BOJ/BOK) tonight, not a symbol-mapping regression, but still means the catalyst layer should not carry single-name decisions.
- **7 untracked legacy crypto alerts today** (EDEN, SOL×3, S, BICO, ONT) — confirmed same-day recurrence of the known watchlist-alert/signal-reuse bug (TODO-3, already HIGH priority in project memory).
- **NVDA legal-risk tag likely a classifier false-positive** — worth a human check so a real future indictment/legal story isn't lost in the noise of misfired tags (see §14).
- **Stocks swing/invest pipeline** still has zero fresh reports since 2026-07-02 (~8 weeks) — persists unchanged, cross-referenced not re-raised as a new item.

## 11. Action Plan — next 4 hours (overnight-into-Asia)

- Flag ONG/USDT for operator review before Asia open — verify the live triggered swing signal's current price against its 0.09240 invalidation; the -26%/+61% internal-vs-external conflict needs a human with a live quote, not another automated read.
- Watch CHIP/USDT and the tied-score RUNE/USDT, S/USDT for pullback fills into their stated zones (0.0362-0.0368 / 0.5502-0.5632 / 0.0311-0.0314); do not chase at current extended prints.
- Watch SOL/USDT for a fill into 103.34-104.05; catalyst is confirmed but low-moderate importance, size accordingly.
- Track GOOGLB/USDT for a possible short promotion if bearish HTF structure + derivatives confirm overnight — currently the only non-ONG short-side idea in the book.
- Manage the existing triggered swing cohort (36 open + 7 tp1_hit) against their stated invalidations only; no new correlated adds given the playbook's own BTC-dump failure mode and tonight's elevated macro risk score.
- Re-check REGN/HON/ATOM flags and the NVDA legal-tag at the next cycle (04:30 crypto-overnight/Asia review) before considering any of them for stocks re-open tomorrow.

## 12. Final Verdict per Mode

- **Crypto scalp:** no A/B setups this cycle; weekly mode-level PF 0.05 (matches the report's own low-confidence banner, PF 0.14 over 14d) — scanner continues, no new entries recommended, re-audit at 20 closed A/B scalp signals per the report's own threshold.
- **Crypto intraday:** no A/B setups this cycle; strongest weekly performer by mode-level stats (PF 1.98) but nothing fresh to act on tonight — manage existing triggered/waiting orders only.
- **Crypto swing:** RS-momentum cohort (CHIP/RUNE/S/MOVR/PROM/TAO/etc., PF 1.78 weekly) open and running; no fresh entries — pullback-only discipline, chase risk flagged for anything bought at market.
- **Stocks intraday:** zero A/B this cycle (all 15 raw-A candidates gate-demoted to C — rolling drawdown guard, 2 legal/earnings-driven, 1 sector/liquidity/catalyst gate on V); RTH closed, nothing pending into tomorrow's open from tonight's data.
- **Stocks swing:** stale (2026-07-02) — excluded, cross-referenced not re-raised.
- **Stocks invest:** stale (2026-07-02) — excluded, cross-referenced not re-raised.

## 13. Sources

- Internal: [scalp report](data/reports/scalp/2026-08-27_15-47_scalp_report.md), [intraday report](data/reports/intraday/2026-08-27_16-34_intraday_report.md), [swing report](data/reports/swing/2026-08-27_12-46_swing_report.md), [stocks intraday report](data/reports/stocks/intraday/2026-08-27_18-31_stocks_intraday_report.md)
- Internal: `data/catalysts/2026-08-27/catalyst_events.jsonl`, `narrative_baskets.jsonl`, `catalyst_cycle_16-50.md`
- Internal: `active-signals`/`signal-stats` CLI output (2026-08-27 23:2x-23:3x EEST), `detect_untracked_legacy_alerts --since 2026-08-27`
- Internal: `db/crypto_ai_desk.sqlite` direct queries — `proposed_signals` (ONG/USDT history), `news_items` (ONG/CHIP/TAO/RUNE, 24h window)
- External: [Ontology Gas (ONG) Price Today, News & Live Chart | Forbes Crypto Market Data](https://www.forbes.com/digital-assets/assets/ontology-gas-ong/) — conflicting/unverifiable price snapshot, see §7.4
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-27_2148.md`

## 14. Fix Requests / TODO

### TODO-ong-bias-contradiction (escalated — 3rd consecutive cycle)
- **issue:** ONG/USDT carries an open swing long (`sig_8d3a8fd71bf0bf75`, triggered 08-26, invalidation 0.09240) while the current desk snapshot tags ONG bias=short with 24h -26.09%. Unresolved across 18:39, 21:48, and this 23:15 review.
- **evidence:** `proposed_signals` query (see §7.4); scalp report §2 "Weakest Symbols" list; matches recurring pattern in project memory (ZBT/ACE, 2026-08-08).
- **suggested manual fix:** a human session with a live price feed should check ONG/USDT's actual current price against 0.09240 and either confirm the long is still valid or force-close/flag it; separately, the bias-tagging logic that produces this contradiction (open long + fresh short-bias tag on the same symbol, same cycle) should be traced — this is the 4th+ documented occurrence project-wide.
- **priority:** high
- **first observed (this symbol):** 2026-08-27 18:39 EEST (this cycle: 2026-08-27 23:38 EEST)

### TODO-untracked-alerts-recurrence
- **issue:** 7 untracked legacy crypto alerts today (EDEN, SOL×3, S, BICO, ONT) — Telegram alerts with no matching `proposed_signal`, so they don't contribute to PF/winrate/avgR tracking. Same-day recurrence of the known TODO-3 bug (watchlist-alert/signal-reuse).
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-27` output, 7 rows.
- **suggested manual fix:** already tracked as high-priority TODO-3 in project memory; this confirms it is still live and firing on SOL/USDT 3× in one day.
- **priority:** high
- **first observed:** prior to this cycle (recurring); reconfirmed 2026-08-27 23:38 EEST.

### TODO-nvda-legal-tag-false-positive
- **issue:** NVDA (stocks intraday) demoted A→C citing "active legal/headline risk (indictment)," but the underlying news item is a bullish M&A story (Nvidia agreeing to buy Hugging Face for $12.9B) with only a tangential "previously hacked" mention about Hugging Face itself, not an indictment of Nvidia. No SEC/DOJ/class-action item naming NVDA was found in today's feed.
- **evidence:** `data/reports/stocks/intraday/2026-08-27_18-31_stocks_intraday_report.md` §4 (NVDA news block) vs. §7 demotion reason line for NVDA.
- **suggested manual fix:** a human session should check the legal-risk classifier's keyword/tag mapping for exploit_hack-tagged items referencing a third company — it appears to be misrouting an "indictment" cap onto NVDA based on the word "hacked" appearing in an unrelated company's backstory.
- **priority:** medium
- **first observed:** 2026-08-27 23:38 EEST

### TODO-swing-regime-label-inconsistency
- **issue:** Today's crypto regime label flipped between "range/chop (neutral)" (scalp 18:42, intraday 19:32) and "bullish trend (risk-on)" (swing 15:45) within the same trading day, on largely overlapping BTC/ETH trend inputs (both uptrend in all three reports).
- **evidence:** header line `Market regime:` in each of the three reports.
- **suggested manual fix:** worth a human check on whether the regime classifier's timeframe/window differs enough between scalp/intraday vs. swing to justify the flip, or whether it's noise near a classification boundary.
- **priority:** low
- **first observed:** 2026-08-27 23:38 EEST
