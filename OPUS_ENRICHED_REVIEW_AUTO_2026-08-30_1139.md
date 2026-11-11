# Opus Enriched Review — Europe / Pre-US Context — Auto Cycle 11:39 EEST

## 1. Executive Summary

Slot: **Europe / pre-US context** (11:30 EEST). **Advisory only — no auto-trade.** Scheduler is fresh (last cycle 10:56 EEST, ~43 min old); no defer needed. Zero fresh crypto A-tier and only one continuing B-tier idea (PROM/USDT swing) across the last three cycles — the book remains almost entirely carry-forward. Market stays **range/chop** on both BTC and ETH with a **risk-off macro overlay** (74–86/100, Iran/Hormuz + a deadly Kyiv drone strike) against modestly improving altcoin breadth (55%/72.5% EMA20/50). The two open-long contradiction cases flagged in the prior three reviews are **worse, not better**: an independent CoinGecko cross-check now confirms **both TUT/USDT and DEXE/USDT trade below their own invalidation levels** while the tracker still shows them `triggered` — DEXE is a **new confirmed breach** this cycle (previously only "weak/bias-contradicted"). A broader sweep of the signals table also surfaced a **previously unscoped, larger version of the known outcome-tracker bug**: 252 signals across both crypto and stocks sit with `expires_at` in the past (some from May 2026) while `status` still reads `triggered`/`tp1_hit`/`tp2_hit`/`waiting_for_entry`, including 3 stocks A-tier and 16 stocks B-tier rows — not just the ~50-row crypto subset tracked so far. Stocks market is closed (Sunday) — stocks content below is planning/watchlist context only, though a legal-risk cluster is building on UNH (DOJ Medicare-fraud probe) worth carrying into Monday. Scanning, tracking, and the scheduler continue uninterrupted regardless of this review's caution stance.

## 2. Data Used

- Reports: `2026-08-30_06-55_scalp_report.md` (09:55 EEST), `2026-08-30_07-05_intraday_report.md` (10:05 EEST), `2026-08-30_04-34_swing_report.md` (07:34 EEST, ~4h old, carry-forward band); stocks intraday `2026-08-28_18-54` (weekend carry-forward, market closed), stocks swing/invest `2026-07-02` (long-stale, informational only).
- Catalysts: `data/catalysts/2026-08-30/catalyst_cycle_07-13.md`, `catalyst_events.jsonl` (1138 cumulative rows today), `narrative_baskets.jsonl` (4 baskets).
- LLM packet: `llm_analysis_packet.md` (10:07 EEST, fresh).
- CLI: `active-signals` (crypto, stocks), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-08-29` and `--since 2026-08-30`.
- Direct SQLite reads (`db/crypto_ai_desk.sqlite`): `proposed_signals` full-table sweep for `expires_at < now AND status IN (waiting_for_entry, triggered, tp1_hit, tp2_hit)`; `news_items` for TUT/DEXE 24h freshness checks (both empty).
- External: 5 WebSearch queries + 2 WebFetch (CoinGecko live pages for TUT and DEXE; ATOM/Cosmos hack context; BTC/ETH late-August context) — see §13.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-30_0439.md` (crypto overnight/Asia slot, 04:39 EEST).

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: 2026-08-30 10:56 EEST (~43 min old) — **fresh**, no defer.
- Latest cycle: `cycle_06_09-46_summary.md` (10:56), 6th cycle of the 2026-08-29 schedule day (day rolled at midnight, folder name unchanged by design).
- Scalp report: 09:55 (fresh, <2h). Intraday report: 10:05 (fresh, <1.5h). Swing report: 07:34 (~4h old — start of the 4–12h **carry-forward** band; used as context, flagged).
- Stocks reports: Aug 28 21:54 (intraday, weekend carry-forward, market closed) / Jul 2 (swing, invest — long-stale, informational only).
- Catalyst scan: 10:13 (fresh, <1.5h). LLM packet: 10:07 (fresh).
- **Untracked-alert detector**: 0 new since 2026-08-30, but `--since 2026-08-29` still returns the identical DEXE/USDT row (sent 2026-08-29T14:36:42 UTC) — unresolved, now **~21h old, 6th+ consecutive review**.
- **Outcome-tracker candle-gap (crypto)**: 44 of 52 currently-unexpired crypto B-tier `proposed_signals` rows show `candles=0` in their latest `signal_outcomes.notes` as of 08:41 UTC this cycle (was 46/52 at 01:47 UTC prior review) — a modest improvement in count, still unreconciled.
- **NEW this cycle — broader lifecycle-status sweep**: a full-table scan for `expires_at < now` while `status` still reads an "open" value found **252 rows**, not the ~50 previously tracked: 36 crypto (all B-tier, overlapping the candle-gap set above) and **216 stocks** (197 C-tier, 16 B-tier, **3 A-tier**), the oldest dating to **2026-05-29**. This is a materially larger and older instance of the same systemic bug family (see §14).
- Monitor/paper Windows Task state not queried this run (Task Scheduler cmdlets are outside the explicit read-only CLI allowlist for this scheduled routine); scheduler-log/cycle-file freshness above is used as the sole liveness proxy this cycle.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-08-30 11:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.68,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["Windows Task Scheduler live state"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler cycle 10:56 fresh", "swing report ~4h old, carry-forward band", "intraday/scalp <2h fresh", "252 total stale open signals past expires_at across both asset classes, incl. 3 stocks A-tier"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["chop", "mixed", "wait_for_trigger"], "data_missing": ["fresh ETF flow print this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/ETH range both intraday and swing cycles", "altcoin breadth 55%/72.5% (EMA20/50) intraday", "macro risk 74.3-85.9/100 risk-off (Iran/Hormuz, Kyiv drone strike)", "9-day BTC/ETH ETF inflow streak as of Aug 27, not reconfirmed this cycle"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported", "catalyst_contradicted"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["1138 catalyst events today, 613/1138 (53.9%) unmapped", "ATOM exploit_hack importance 0.81, hack occurred Aug20-25, disclosure reopened Aug29", "external research surfaces a competing bullish ATOM deflationary-tokenomics narrative not in the internal record", "4 narrative baskets: perps_dex, rwa, ai, momentum_breakout(avoid_chase)"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "data_unavailable"], "data_missing": ["DEXE funding/OI not in either cycle's top-8 derivatives table"],
      "suggested_effect": "advisory_only",
      "facts_used": ["TUT funding -0.0091 (bybit), elevated short crowding despite price breakdown", "PROM funding neutral -8e-06 to -5e-05, low crowding"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.62,
      "reason_codes": ["chase_risk", "entry_late", "price_moved_away"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PROM current price 6.948 vs waiting_for_entry zone top 6.836 — already through it, chase risk at market", "ZKP/GIGGLE watchlist-only, scores below active-trade threshold"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.62,
      "reason_codes": ["waiting_for_entry", "needs_review", "entered_unresolved"], "data_missing": ["true stop/TP state for all 252 stale rows"],
      "suggested_effect": "advisory_only",
      "facts_used": ["1 waiting_for_entry (PROM swing)", "44/52 crypto B-tier rows candle-gap affected", "252 total rows (36 crypto + 216 stocks) with expires_at in the past but status still open, oldest from 2026-05-29"] },
    { "agent": "risk_manager", "verdict": "manual_review", "confidence": 0.78,
      "reason_codes": ["manual_review", "correlation_cluster", "reduce_risk"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TUT/USDT CoinGecko live price $0.03565 (-10.4% 24h) vs invalidation 0.05058 — ~29.5% through stop, still status=triggered", "DEXE/USDT CoinGecko live price $2.28 (-5.4% 24h) vs invalidation 2.38346 — NEW confirmed breach this cycle, still status=triggered", "DEXE untracked alert unresolved ~21h, 6th+ consecutive review", "book is 100% long, no shorts generated in the last 327-signal sample"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.68,
      "reason_codes": ["playbook_failing", "low_sample", "old_tail_expired"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto A/B week: winrate 11.76%, PF 1.255, avgR +0.061, totalR +15.3, n=327", "scalp-mode bucket: 0 wins/9 losses this week, PF ~0.1x — reproducibly losing", "swing-mode bucket stronger, PF ~1.6-1.7", "stocks A/B n=13 (weak confidence), WR 60%, PF inf — small sample, plausibly inflated by the stale-row lifecycle bug never recording a loss"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.63,
      "reason_codes": ["chop", "manual_review", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.63,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": { "symbol": "PROM/USDT", "trigger": "confirmed 1h close-and-retest holding above 6.85 with volume, or a pullback fill back into the existing 6.583-6.836 waiting_for_entry zone — do not buy the current 6.948 print at market", "reason": "top RS/score leader across scalp/intraday/swing all three cycles today, funding neutral, low crowding" },
    "best_short_candidate": { "symbol": "DEXE/USDT", "trigger": "resolve the existing open long manually first (it is now confirmed through its own invalidation per CoinGecko cross-check); only after that, a confirmed 1h close-and-retest below ~2.28 with volume would be the short-watch trigger", "reason": "weak/short-biased in today's reports and now externally confirmed trading below its own invalidation level while the desk holds an open long on it" },
    "best_catalyst_candidate": { "symbol": "ATOM/USDT", "trigger": "confirmed breakdown with volume on renewed negative reaction to the reopened six-chain hack disclosure — tempered by a competing bullish deflationary-tokenomics narrative found in external research, so this is a two-sided catalyst, not a clean short", "reason": "highest-importance fresh catalyst again this cycle (0.81), no existing desk position" },
    "avoid_candidate": { "symbol": "TUT/USDT", "reason": "open long ~29.5% through its own invalidation per independent CoinGecko cross-check ($0.03565 vs 0.05058), unreconciled outcome-tracker gap, documented Aug 9 pump/crash/liquidation history" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.68 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.65 | chop, mixed, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, fresh_catalyst, narrative_supported, catalyst_contradicted | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.62 | chase_risk, entry_late, price_moved_away | advisory_only |
| execution_lifecycle | needs_review | 0.62 | waiting_for_entry, needs_review, entered_unresolved | advisory_only |
| risk_manager | manual_review | 0.78 | manual_review, correlation_cluster, reduce_risk | advisory_only |
| playbook_performance | caution | 0.68 | playbook_failing, low_sample, old_tail_expired | advisory_only |
| head_trader | caution | 0.63 | chop, manual_review, wait_for_trigger | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-30_0439.md` (crypto overnight/Asia slot, 04:39 EEST).

- **Escalated**: DEXE/USDT moves from "weak/bias-contradicted" to a **confirmed invalidation breach** — independent CoinGecko cross-check this cycle puts it at $2.28 vs invalidation 2.38346, joining TUT/USDT in the same open-long-past-stop failure pattern the tracker cannot see.
- **New, broader finding**: the outcome-tracker/lifecycle bug is bigger than previously scoped. Beyond the ~50-row crypto candle-gap set tracked since 2026-07-17, a full-table sweep found 252 rows (36 crypto + 216 stocks, including 3 stocks A-tier and 16 stocks B-tier) sitting with `expires_at` in the past while `status` still reads an open value, some dating to 2026-05-29. This directly questions the reliability of the stocks A/B headline stat (n=13, WR 60%, PF inf) — a sample that small can be skewed heavily if even one or two of these stale rows belong in it as unrecorded losses.
- **Improved slightly**: crypto candle-gap count is 44/52 this cycle vs 46/52 at 04:39 — moving in the right direction but still unreconciled.
- **Unchanged**: DEXE/USDT untracked legacy alert, now ~21h old (was ~14h), 6th+ consecutive review.
- **Unchanged**: PROM/USDT remains the top RS/score leader across all three modes; the same swing signal (`sig_b108351df18809d4`) continues waiting_for_entry, now with price further extended (6.948 vs the 6.583-6.836 zone, versus 6.948 vs 6.85 at the last check) — chase risk is marginally worse, not better.
- **Refined**: ATOM/USDT's catalyst thesis is less one-sided than it appeared at 04:39 — external research surfaces a competing bullish deflationary-tokenomics narrative running alongside the hack-disclosure overhang, making this a two-sided catalyst rather than a clean bearish one.
- Catalyst mapping essentially unchanged: 53.9% unmapped today vs 54.0% at 04:39 — still weak.
- No A-tier or fresh B-tier crypto signals in any of the three most recent cycles (scalp, intraday, swing) — book remains carry-forward.

## 5. Catalyst Coverage

- Total catalyst events today (cumulative, as of 10:13 EEST catalyst cycle): **1138**. Mapped (non-null symbol): **525**. Unmapped: **613** (**53.9%**).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Narrative baskets: **4** (perps_dex_narrative, rwa_narrative, ai_narrative, momentum_breakout/avoid_chase).
- Top 3 unmapped headlines (by cycle sample): "AEVEX Corp. (AVEX) Class Action Lawsuit: Investors Face October 20, 2026, Deadline"; "Here's How Much You Should Have Saved for Retirement by Age 67, According to 1 Popular Rule"; "Here's the Maximum Social Security Increase You Could Get From a 3.6% 2027 COLA" (the latter two are personal-finance filler correctly left unmapped, inflating the denominator, not a resolver failure).
- Latest single-cycle scan (`catalyst_cycle_07-13.md`, 293 rows): other_news 267, legal_risk 14, exploit_hack 4, partnership 3, insider_activity 2, rumour_only 1, buyback_burn 1, token_unlock 1.
- Highest-importance catalyst: ATOM/USDT exploit_hack, importance 0.81 (down slightly from 0.84 at 04:39, still top).
- New legal-risk cluster building: UNH/USDT — 6 distinct headlines this cycle on a DOJ criminal Medicare-fraud probe deepening (Brach Eichler, Simply Wall St, Yahoo Finance, healthexec.com, QuiverQuant, TipRanks); TSLA/USDT — Musk SEC settlement, $1.5M fine (Union Leader). Both stocks names, relevant for Monday's pre-open review, not actionable today (market closed).

## 6. Market Landscape

BTC and ETH both read **range** across the scalp (09:55), intraday (10:05), and swing (07:34) cycles today. Altcoin breadth above EMA20 sits at 55.0% intraday / 52.5% swing, above EMA50 at 72.5% both — a modest, not decisive, broadening similar to the prior review. Macro/geopolitics risk score is elevated across all three cycles today (74.3–85.9/100), driven by Iran/Hormuz headlines and a fresh, deadlier Kyiv drone-strike headline — a genuine risk-off overlay. The 9-day BTC/ETH spot-ETF inflow streak cited as of Aug 27 was not reconfirmed with a fresher print this cycle; treat it as still-standing but aging context, not a live signal. AI and Memes narrative heat remain "mixed" (25-37/100); RWA, L2, Gaming, DePIN are quiet.

### Market Mood / Risk Routing
- Crypto mood:           chop, with a real risk-off macro overlay (74-86/100) but an unconfirmed-this-cycle bullish ETF-flow undercurrent — genuinely mixed, not a clean call either way.
- Stocks mood:           closed (Sunday) — planning/watchlist context only; a legal-risk cluster is building on UNH into Monday.
- Dominant narrative:    perps_dex (HYPE, wait_pullback), rwa (ONDO/XLM), ai (NEAR/RENDER/TAO/FET) — all single-source and unconfirmed; momentum_breakout basket (4/USDT, CASHCAT/USDT) explicitly flagged avoid_chase by the desk's own playbook.
- Preferred side now:    wait-for-trigger, mild long-lean only on RS leadership (the desk's own signal generator has produced zero shorts across the last 327-signal sample — a structural gap, not a market call).
- Best long candidate:   PROM/USDT — wait for a retest holding above 6.85 or a pullback fill into 6.583-6.836; do not chase the current 6.948 print.
- Best short candidate:  none clean live; DEXE/USDT is the short-watch, but only after its own open-long contradiction (now a confirmed invalidation breach) is manually resolved.
- Best catalyst-backed candidate: ATOM/USDT — two-sided catalyst (bearish hack-disclosure overhang vs bullish deflationary-tokenomics narrative), watch for a confirmed breakdown with volume before treating it as bearish.
- What to avoid:         TUT/USDT (deepest, longest-unresolved breach) and DEXE/USDT (newly confirmed breach) — do not add to either.
- What would change the view: a BTC/ETH close outside the current range with volume confirmation, a fresh ETF-flow print either extending or breaking the streak, or a human reconciling the outcome-tracker's true open-book state.

## 7. Candidate Deep Dives

### TUT/USDT — AVOID / manual review (existing long, confirmed breach)
- Active signal: `sig_c7ce9835f38c40a8`, B-tier swing long, entry 0.05164-0.05250, invalidation 0.05058, TP1/2/3 0.0554/0.0573/0.0598, status `triggered`, expires 2026-09-03.
- Today's reports still tag TUT/USDT bias=short, 24h -7.75% to -9.58% across scalp/intraday/swing.
- External cross-check (CoinGecko, live): **$0.03565, -10.4% 24h** — roughly **29.5% through** the 0.05058 invalidation. This is a slight recovery from the ~30%-through reading independently checked at the 04:39 review (~$0.03523) but the position remains clearly breached while `status` still reads `triggered`.
- No fresh internal `news_items` catalyst found for TUT in the last 72h — the move continues to be pure price action, not news-driven.
- TUT carries a documented history of extreme leverage-driven volatility (>200% surge then -44% in one hour on Aug 9, 2026, $34M liquidations — [KuCoin News](https://www.kucoin.com/news/flash/bsc-project-tut-surges-200-in-24h-then-drops-44-in-1-hour-with-34m-in-liquidations)). Current negative funding (-0.0091 bybit) shows shorts remain crowded, so a fresh short here also carries squeeze risk.
- Not applicable to a fresh entry — the open long needs manual review, not a new trade decision.
- Would invalidate the "avoid new" call: a confirmed reclaim back above the original entry zone (0.0516+) with volume — none observed.

### DEXE/USDT — short-watch / manual review (existing long, NEW confirmed breach)
- Active signal: `sig_5b59fe4d0138325c`, B-tier swing long, entry 2.4777-2.5547, invalidation 2.38346, status `triggered`, expires 2026-09-05.
- Today's scalp report lists DEXE/USDT bias=short, 24h -5.15%.
- External cross-check (CoinGecko, live): **$2.28, -5.4% 24h** — this is **below** the 2.38346 invalidation, a confirmed breach not present in the same clear form at the 04:39 review (previously described only as "weak, no funding data sampled").
- `detect_untracked_legacy_alerts --since 2026-08-29` still returns the identical DEXE/USDT swing-long alert (score 65.0, sent 2026-08-29T14:36:42 UTC) with no backing `proposed_signal` — untracked, now **~21h unresolved, 6th+ consecutive review**.
- No funding/OI data was sampled for DEXE in either of today's top-8 derivatives tables — squeeze risk on a short here remains genuinely unknown.
- Chase/entry check for a fresh short: DEXE has already moved through its own invalidation; a fresh short now would be chasing a move that has already happened at the desk's own timescale. Actionable trigger would be a confirmed retest failure below ~2.28 after consolidation, not a market order now.
- Listed as short-watch, not short-now: the desk holds an open long here and its own tracker has not resolved the breach — manual review of the existing position takes priority over any new position on the same symbol.

### PROM/USDT — long-watch (existing waiting_for_entry, top RS leader)
- Active signal: `sig_b108351df18809d4`, B-tier swing long, `waiting_for_entry`, entry 6.5825-6.8355, invalidation 6.27326, expires 2026-09-06.
- Strongest symbol across all three cycles today (score 91.6 scalp/intraday, 69.0 swing headline score with the same underlying strength read), 24h +34-52% depending on cycle window, RS vs BTC +33-50%.
- Current price per the swing report's own desk note: **6.948** — already above the 6.836 top of the planned entry zone, and above the 6.85 breakout-retest level the prior review flagged as the alternate trigger.
- Derivatives: funding neutral (-8e-06 to -5e-05 across cycles), low-to-normal crowding, no squeeze setup either way.
- Chase/entry check: price has run well past the original entry plan. Treat 6.948 as inside "already through 6.85" territory — the correct participation path now is a confirmed retest holding above 6.85, not a market buy at the current print.
- Catalyst: appears repeatedly in the "Weekly Top Gainers" Telegram digest (+98.03% on a longer window) but no dedicated symbol-specific catalyst verified — momentum/RS-leadership thesis, not catalyst-backed.
- Would invalidate: a close back below 6.27326, or a broader BTC/ETH breakdown dragging RS leaders down with it.

### ATOM/USDT — catalyst-watch (no existing position, two-sided catalyst)
- Top-importance catalyst again this cycle: exploit_hack, importance 0.81 — "Cosmos Labs says it wrongly cleared the bug behind a $5.7 million six-chain hack" ([The Block](https://www.theblock.co/news/defi/2026-08-29-cosmos-labs-says-it-wrongly-cleared-the-bug-behind-a-5-7-million-six-chain-hack-413061), single_source).
- External verification: the exploit itself ran Aug 20-25, 2026 across six Cosmos-EVM chains (~$5.7M stolen); Cosmos Labs silently patched in May after wrongly clearing the bug, then released the real fix Aug 19, with the first attack beginning ~20 hours later ([The Hacker News](https://thehackernews.com/2026/08/cosmos-evm-flaw-exploited-after-cosmos.html), [CryptoSlate](https://cryptoslate.com/cosmos-misjudged-a-critical-bug-for-4-months-before-hackers-stole-nearly-6-million-across-6-chains/)). The Aug 29 story is the disclosure of Cosmos Labs' own process failure, not a new exploit.
- Counter-thesis, newly surfaced this cycle: ATOM is separately running a bullish deflationary-tokenomics narrative (transition to fee-driven buyback/burn) that lifted price earlier in August — this is a genuinely two-sided catalyst, not a clean bearish one.
- No active desk position on ATOM/USDT — clean catalyst-watch, no contradiction risk.
- Not yet reflected in any of today's three "Top Trade Ideas" sections — no technical setup has formed on ATOM yet.
- Actionable trigger: a confirmed breakdown with volume on continued negative reaction to the disclosure; the current level should be treated as still digesting a mixed narrative, not yet a clean short.

### UNH/USDT (stocks, watch-only) — building legal-risk cluster
- Six distinct headlines this cycle on a DOJ criminal Medicare-fraud probe deepening into UnitedHealth/Optum Rx, across Brach Eichler, Simply Wall St, Yahoo Finance, healthexec.com, QuiverQuant, and TipRanks — a corroborated multi-source cluster, not single-source noise.
- Active desk signals on UNH are both C-tier (one long, one short — contradictory bias, but C-tier is never actionable by design, so this is not a live conflict).
- Stocks market is closed today (Sunday); this is planning context for the pre-US-open (16:20) and US-open-reaction (18:30) slots tomorrow, not an actionable item now.
- Per §I discipline: any UNH A/B signal that might form ahead of the open should be treated as `MANUAL REVIEW REQUIRED`, not a clean actionable, given the corroborated DOJ-probe legal risk.

## 8. Best Candidates Ranked

1. **PROM/USDT** (long-watch) — wait for a retest holding above 6.85 or a pullback fill into 6.583-6.836; do not chase 6.948.
2. **ATOM/USDT** (catalyst-watch, two-sided) — wait for a confirmed breakdown with volume; do not treat the hack disclosure alone as bearish confirmation.
3. **DEXE/USDT** (short-watch, blocked by open contradiction) — manual review of the existing long takes priority; now a confirmed invalidation breach, not just "weak."
4. **TUT/USDT** (avoid / manual review) — do not add; existing long remains ~29.5% through its own invalidation.
5. **UNH/USDT** (stocks watch-only) — carry the DOJ-probe legal-risk cluster into Monday's pre-open review; C-tier only today, not actionable.

No clean, unconditional "trade now" candidate exists this cycle — every entry above is trigger-gated, per PART 9.

## 9. Avoid / No Trade

This decision window only — scanning, tracking, and the scheduler continue regardless.

- **TUT/USDT**: existing long confirmed ~29.5% through invalidation via independent cross-check; avoid adding, flag for manual review.
- **DEXE/USDT (new positions)**: existing long now confirmed through its own invalidation; do not add a fresh short while the position and the untracked-alert duplicate are both unresolved.
- **4/USDT, CASHCAT/USDT (momentum_breakout basket)**: desk's own `avoid_chase` playbook applies — top gainers with no confirmed news catalyst.

## 10. Main Risks

- **Outcome-tracker / lifecycle bug is larger than previously scoped**: beyond the known 44-52-row crypto candle-gap set, a full-table sweep found 252 rows across both asset classes (36 crypto, 216 stocks — including 3 stocks A-tier and 16 stocks B-tier) sitting with `expires_at` in the past while `status` still reads an open value, some dating to 2026-05-29. This undermines confidence in every "triggered"/"tp1_hit"/"tp2_hit" label used throughout this review, the live Telegram book, and the stocks A/B headline stat (n=13 — small enough that even a couple of misclassified stale rows would move the reported 60% winrate materially).
- **Two open longs are now confirmed breached simultaneously** (TUT/USDT ~29.5% through, DEXE/USDT newly confirmed through) — the desk's own book cannot currently express a risk-off view even though the market carries a genuine risk-off macro overlay, because it is structurally 100% long with zero shorts generated across the last 327-signal sample.
- **DEXE/USDT untracked alert** unresolved for a 6th+ consecutive review (~21h), matching the escalated watchlist-alert-reuse pattern.
- **Catalyst mapping remains weak this run** (53.9% unmapped) — treat the catalyst layer as context, not a gating input.
- **UNH DOJ-probe cluster** is corroborated across six independent sources this cycle — a real legal-risk item to carry into Monday's stocks pre-open review, not yet actionable today.

## 11. Action Plan — next 4 hours

- Continue watching PROM/USDT for either a retest holding above 6.85 or a pullback fill into the existing waiting_for_entry zone; no new action needed, the signal is already tracked.
- Continue watching ATOM/USDT for a technical setup to form around the two-sided catalyst; nothing tracked yet.
- No new crypto entries recommended into the EU/pre-US window beyond the existing tracked book.
- Human/manual: review TUT/USDT and DEXE/USDT open longs against current price action — both are now independently confirmed past their own invalidation levels while the tracker still shows them open.
- Human/manual: the broadened lifecycle-bug finding (252 stale rows, 3 stocks A-tier) warrants a dedicated audit session, separate from routine candle-gap monitoring — see §14.
- Stocks: no action, market closed; carry DXCM/MRVL/COST/CRCL/GE/UNH names forward as planning context into the pre-US-open (16:20) and US-open-reaction (18:30) slots, with UNH flagged for legal-risk review specifically.

## 12. Final Verdict per Mode

- **Crypto scalp**: avoid — reproducibly losing bucket this week (0 wins/9 losses per the by-mode stats table); no new scalp entries regardless of setup quality until a human reviews this bucket.
- **Crypto intraday**: wait-for-trigger — 0 fresh A/B this cycle.
- **Crypto swing**: wait-for-trigger on PROM/USDT and ATOM/USDT; manual review priority on TUT/USDT and DEXE/USDT open longs (both now confirmed breached).
- **Stocks intraday/swing/invest**: closed/planning-only — no verdict until RTH context refreshes; UNH carries a legal-risk flag into Monday.

## 13. Sources

- [BSC Project TUT Surges 200% in 24 Hours, Then Drops 44% in One Hour with $34 Million in Liquidations](https://www.kucoin.com/news/flash/bsc-project-tut-surges-200-in-24h-then-drops-44-in-1-hour-with-34m-in-liquidations) — KuCoin News, Aug 9, 2026.
- [DeXe (DEXE) live price](https://www.coingecko.com/en/coins/dexe) — CoinGecko, fetched 2026-08-30 ~11:xx EEST, $2.28, -5.4% 24h.
- [Tutorial (TUT) live price](https://www.coingecko.com/en/coins/tutorial) — CoinGecko, fetched 2026-08-30 ~11:xx EEST, $0.03565, -10.4% 24h.
- [Cosmos Labs says it wrongly cleared the bug behind a $5.7 million six-chain hack](https://www.theblock.co/news/defi/2026-08-29-cosmos-labs-says-it-wrongly-cleared-the-bug-behind-a-5-7-million-six-chain-hack-413061) — The Block, Aug 29, 2026.
- [Cosmos EVM Flaw Exploited After Cosmos Labs Knew Every Blockchain Running It Was Vulnerable](https://thehackernews.com/2026/08/cosmos-evm-flaw-exploited-after-cosmos.html) — The Hacker News.
- [Cosmos misjudged a critical bug for 4 months before hackers stole nearly $6 million across 6 chains](https://cryptoslate.com/cosmos-misjudged-a-critical-bug-for-4-months-before-hackers-stole-nearly-6-million-across-6-chains/) — CryptoSlate.
- Internal: `data/catalysts/2026-08-30/catalyst_cycle_07-13.md`, `catalyst_events.jsonl`.
- Internal: `db/crypto_ai_desk.sqlite` `proposed_signals` full-table sweep, run 2026-08-30 ~11:20 EEST.
- Internal: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-30_0439.md` (previous review, for continuity/diff).

## 14. Fix Requests / TODO

### TODO-lifecycle-status-gap-broadened-2026-08-30 (NEW — supersedes/broadens outcome-tracker-candle-gap TODO)
- **issue:** The known crypto candle-gap tracking issue (previously scoped to ~50 open crypto B-tier rows) is one symptom of a **larger, previously-unquantified lifecycle-status bug**: a full-table sweep of `proposed_signals` for `expires_at < now() AND status IN (waiting_for_entry, triggered, tp1_hit, tp2_hit)` returns **252 rows**, not ~52. Breakdown: 36 crypto (all B-tier, overlaps the known candle-gap set), 216 stocks (197 C-tier, 16 B-tier, **3 A-tier**). The oldest row (`DIA`, stocks C-tier) has `expires_at=2026-05-30`, i.e. **three months** past expiry and still shown as an open `tp1_hit` position. Three stocks **A-tier** rows (`GE`, `sig_bc88416f6f2890b0` / `sig_e9b2f0ea552005e7` / `sig_6abeb2c7022a152a`) expired 2026-08-18/19 and still read `tp1_hit`. This means the stocks A/B headline stat (`signal-stats --asset-class stocks`, n=13, WR 60%, PF inf) is being computed over a sample that may not correctly exclude these stale-but-technically-open rows, or may be excluding them entirely and understating the true closed sample — either way the 60%/PF-inf headline should not be trusted at face value until this is resolved.
- **evidence:** Python/SQLite query against `db/crypto_ai_desk.sqlite`, run 2026-08-30 ~11:20 EEST: `SELECT ... WHERE status IN (...) ` then filtering client-side for `expires_at < utcnow()` → 252 rows. Sample stale rows: `sig_21e828beafd7c2eb` (DIA, C, expires 2026-05-30), `sig_1bc6d2076b02bd2b`/`sig_44c859b478a7057e` (SMH, B, expires 2026-06-05/07), `sig_bc88416f6f2890b0`/`sig_e9b2f0ea552005e7`/`sig_6abeb2c7022a152a` (GE, **A-tier**, expires 2026-08-18/19).
- **suggested manual fix:** (1) confirm whether the outcome-checker job covers stocks symbols at all, or only crypto (the 216:36 stocks:crypto skew suggests stocks may not be checked at all); (2) add an automated sweep/alert for `expires_at < now() AND status NOT IN (closed_states)` across both asset classes, not just the crypid candle=0 heuristic; (3) once the root cause is fixed, backfill/reconcile all 252 rows' true final status; (4) re-run `signal-stats --asset-class stocks` after the backfill and treat the current n=13 headline as unreliable until then; (5) this is now the 5th consecutive review carrying an unresolved instance of this bug family — recommend explicit human sign-off that a dedicated maintenance session is scheduled, not just another scheduled-review mention.
- **priority:** high (larger scope than previously known, includes stocks A-tier, unresolved across 5+ reviews)
- **first observed:** 2026-07-17 (crypto candle-gap form, per `project_crypto_ai_desk_bias_tag_contradiction`/candle-gap memory); broadened scope (stocks + 3-month-old rows + A-tier) newly quantified 2026-08-30 11:39 EEST.

### TODO-untracked-alert-dexe-recurrence-2026-08-30 (unresolved, 6th+ consecutive review)
- **issue:** `detect_untracked_legacy_alerts --since 2026-08-29` again returns the identical `DEXE/USDT` swing long alert (score 65.0, direction long, sent 2026-08-29T14:36:42 UTC) with `trackable=NO` — now **~21h unresolved**, the same instance logged at 18:40, 21:45, 23:33 EEST on 2026-08-29 and 04:39 EEST on 2026-08-30. Compounded this cycle by the same DEXE/USDT symbol's tracked position independently confirming a breached invalidation (see §7) — two distinct integrity issues on the same symbol simultaneously.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-29` output at 11:2x EEST 2026-08-30: identical row — DEXE/USDT, tier B, swing, score 65.0, long, sent_at 2026-08-29T14:36:42+00:00, trackable=NO.
- **suggested manual fix:** unchanged — trace the watchlist-alert path for stale/closed `signal_id` reuse on symbol+mode combinations; this DEXE/USDT instance (now ~21h unresolved) remains a durable reproduction case, and its concurrent invalidation-breach makes it a higher-value case to debug against than TUT/USDT alone.
- **priority:** high (unresolved recurrence, now 6th+ consecutive review)
- **first observed:** 2026-07-17 (per memory); this specific instance 2026-08-29 14:36:42 UTC, confirmed still unresolved as of 2026-08-30 11:39 EEST.
