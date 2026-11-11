# Opus Enriched Review — Europe / pre-US context (off-schedule catch-up) — Auto Cycle 15:48 EEST

## 1. Executive Summary

**Slot: Europe / pre-US context framing, dispatched off-schedule at ~15:40-15:48 EEST on Saturday 2026-07-18.** This task fires 04:30/11:30/18:30/21:30 EEST; this run landed at neither — it is ~4h10m after the 11:30 slot and ~2h42m before the 18:30 slot, with no `DEFERRED`/`BLOCKED` marker files for any of the six slots since the last successful review (2026-07-17 16:29 EEST). See TODO-11. **Advisory only — no auto-trade, no code/scoring/routing changes.** Pipeline healthy: `scheduler.log` mtime 15:03 EEST, latest `cycle_05_14-30_summary.md` mtime 15:03 EEST (~45min old at review start) — both well under the 3h defer threshold, **not deferred**.

**It is Saturday — US cash markets are closed all day; stocks are planning/watchlist context only, crypto is the sole live actionable class.** Crypto scalp (14:39 EEST) and intraday (14:44 EEST) reports are fresh (~1h old); the swing report (04:47 EEST, ~11h old, carry-forward) produced one B-tier long idea (VIRTUAL/USDT) whose thesis has since **flipped and is now invalidated** by the fresher 11:44 UTC scan (VIRTUAL now shows `bias short`, RS -2.70% vs BTC, tag `weak_vs_market` — see §4/§7). Neither the scalp nor intraday cycle produced any A- or B-tier setup this run ("No A-tier setups found... No B-tier setups found" in both reports) — this is a genuinely quiet/no-fresh-idea cycle, not a data outage.

Two crypto signals remain listed as "active" but are functionally closed: NEAR/USDT (B, scalp, short, `tp1_hit`, expired 2026-07-17T15:56 UTC) and ONDO/USDT (B, intraday, long, `tp2_hit`, expired 2026-07-17T08:36 UTC) — the same non-terminal-status-past-expiry lifecycle gap flagged in the last two reviews (TODO-2/TODO-10, still reproducing). Macro risk is **67.2/100** (down from 96/100 at the 2026-07-17 16:20 EEST review) — the US-Iran/Gulf conflict is ongoing but external verification (WebSearch) suggests the market has grown somewhat desensitized to it, with Fed policy competing as the dominant price driver. **Catalyst mapping is weak this run (82.6% unmapped, 2130/2579)** — consistent with the known catalyst-linkage gap already logged in project memory, use as directional context only.

**Positive changes this run**: the untracked-legacy-alert detector returned clean (0 results) for the first time in 4+ consecutive reviews (TODO-3 not reproducing today, watch for recurrence); `market_dashboard_snapshots.crypto_regime` now reads `transition`, matching the report-level regime classifier (TODO-9 appears resolved, watch for recurrence). `mexc_canary_monitor` is still crash-looping on `database is locked` (TODO-8, unchanged, high priority, live-execution-adjacent). A new, higher-severity earnings-calendar regression was found (TODO-7 upgraded: 0 earnings events tracked, lookup failing for 10 of the tracked stock tickers, actively demoting multiple would-be-A candidates) and a new data-quality bug in `news_items.published_at` formatting was found (TODO-12, read-only finding, affects freshness filtering broadly).

## 2. Data Used

- Reports: `data/reports/scalp/2026-07-18_11-39_scalp_report.md` (mtime 14:39 EEST, ~1h09m old, fresh), `data/reports/intraday/2026-07-18_11-44_intraday_report.md` (mtime 14:44 EEST, ~1h04m old, fresh), `data/reports/swing/2026-07-18_01-47_swing_report.md` (mtime 04:47 EEST, ~11h01m old, **carry-forward**, thesis since invalidated by fresher scan — see §4), `data/reports/stocks/intraday/2026-07-17_21-56_stocks_intraday_report.md` (mtime ~00:56 EEST 2026-07-18, ~14h52m old, **stale/borderline**, market-closed header regardless), `data/reports/stocks/swing/2026-07-02_13-03_stocks_swing_report.md` and `data/reports/stocks/invest/2026-07-02_13-05_stocks_invest_report.md` (both 16 days old, **stale**, excluded from any verdict, mentioned only for continuity).
- Catalyst: `data/catalysts/2026-07-18/catalyst_events.jsonl` (2579-row rolling buffer, 449 mapped / 2130 unmapped), `narrative_baskets.jsonl` (5 baskets), `data/catalysts/2026-07-18/catalyst_cycle_11-47.md` (latest cycle, mtime 14:47 EEST, already present, no re-scan needed).
- LLM packets: `data/processed/llm_analysis_packet.md` (generated 11:44:51 UTC / 14:44 EEST, ~1h04m old, fresh — this is the freshest single source used for the VIRTUAL/DODO/RE symbol-level bias reads in §7), `data/processed/llm_stocks_packet.md` (generated 2026-07-17T11:25 UTC, ~28h old, **stale**, not used for any live decision — market closed anyway).
- Internal CLI: `active-signals` (crypto: 2 rows; stocks: 50 rows, all resolved/expired), `signal-stats` (crypto: week, A/B headline PF 2.49, totalR +28.4, n=93; stocks: week, A/B headline PF 0.75, totalR -0.5, n=11), `detect_untracked_legacy_alerts --since 2026-07-18` (0 results — clean).
- SQLite direct reads (read-only): `news_items` (ONDO/NEAR/VIRTUAL symbol-tagged rows, last 24h), `narrative_baskets.jsonl` parse, `intelligence_source_health`, `news_source_runs` (telegram collector heartbeat vs actual-item runs — see §14 investigation), `market_dashboard_snapshots` (latest row, id=192, 11:53 UTC), `watchlist_alerts` (9 rows last 24h, informational).
- External: WebSearch ×2 (Iran/Gulf-conflict crypto-market impact; ONDO team-wallet-to-Coinbase transfer) — both used because internal single-source items needed corroboration/context per §G. No WebFetch performed (search snippets were sufficient and consistent across multiple independent outlets).

## 3. Scheduler / Data Freshness

- `scheduler.log`: mtime 2026-07-18 15:03 EEST — fresh (~45min old).
- Latest cycle summary: `cycle_05_14-30_summary.md`, mtime 15:03 EEST — fresh. Cycle log shows `CYCLE 5 END ok=51 failed=0 telegram=sent` — clean run, no step failures.
- Crypto monitor (pid 21064) and derivatives monitor (pid 6172) both confirmed still running at end-of-cycle 15:03 EEST.
- Reports freshness: scalp/intraday fresh (~1h old); swing carry-forward (~11h old, thesis invalidated — see §4); stocks intraday stale/borderline (~15h old) but irrelevant this run since market is closed all weekend; stocks swing/invest stale (16 days) — excluded.
- Paper monitor status (telegram) ran successfully in this cycle per scheduler log (18.6s, exit=0) — paper tracking pipeline appears healthy.
- **Not deferred** — both freshness signals well under the 3h threshold. See §1/§14 (TODO-11) for the separate, unrelated finding about this task's own dispatch timing (6 slots apparently skipped upstream of this run).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-07-18 15:48 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["stocks swing/invest reports (16d stale)", "reliable telegram-collector freshness signal (published_at format bug, see TODO-12)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log/cycle_05 mtime 15:03 EEST", "swing report 04:47 EEST (~11h old) thesis invalidated by 11:44 UTC scan", "catalyst mapping 82.6% unmapped"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["mixed", "chop", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC uptrend / ETH range, breadth 39.5% above EMA20", "macro risk 67.2/100, down from 96/100 prior review", "market_dashboard_snapshots.crypto_regime=transition matches report regime"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["82.6% unmapped catalyst events today (2130/2579)", "rwa_narrative basket fresh <6h, primary ONDO/XLM", "ai_narrative basket freshness unknown, primary NEAR/RENDER/TAO/FET"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.4,
      "reason_codes": ["squeeze_risk", "data_unavailable"],
      "data_missing": ["order book depth/CVD", "liquidation heatmaps"],
      "suggested_effect": "advisory_only",
      "facts_used": ["HOME/USDT and BANK/USDT capped to C for short-squeeze-risk in latest intraday report", "BONK/USDT thin-liquidity short-squeeze-risk flag"]
    },
    {
      "agent": "technical_entry",
      "verdict": "watch",
      "confidence": 0.5,
      "reason_codes": ["overextended", "price_moved_away", "chase_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ALLO/XEC/BTW/TRUMP all >2ATR from EMA20, rejected as chase risk", "DODO/USDT not overextended but weak volume (0.42x) and no catalyst", "VIRTUAL/USDT thesis flip long->short in fresher scan"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "needs_review",
      "confidence": 0.85,
      "reason_codes": ["closed_flat", "needs_review", "no_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["NEAR/USDT tp1_hit past expires_at (2026-07-17T15:56 UTC)", "ONDO/USDT tp2_hit past expires_at (2026-07-17T08:36 UTC)", "no new A/B this cycle in scalp/intraday"]
    },
    {
      "agent": "risk_manager",
      "verdict": "ok",
      "confidence": 0.7,
      "reason_codes": ["reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["no legal/headline-flagged crypto candidate active this cycle", "macro geopolitical risk elevated but de-escalating (67.2/100, down from 96/100)", "direction=short losing bucket this week (PF 0.20, totalR -4.0)"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto mode=scalp: n=22, PF 0.17, totalR -5.0, 0W/7L this week", "crypto mode=intraday: PF 4.64, totalR +18.2, strong", "stocks headline A/B: n=11, PF 0.75, totalR -0.5, weak/anecdotal sample"]
    },
    {
      "agent": "head_trader",
      "verdict": "watch_only",
      "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["no A/B actionable in either asset class this cycle", "VIRTUAL long thesis invalidated by fresher data", "weekend, stocks closed all day"]
    }
  ],
  "head_trader": {
    "overall_verdict": "watch_only",
    "confidence": 0.6,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": { "symbol": "DODO/USDT", "trigger": "volume expansion to >=1x 20-period average + either a fresh verified catalyst or a clean pullback/retest entry structure on 15m-1h; do not chase the current +10.2% move", "reason": "cleanest RS long in today's scan without the >2ATR overextension tag carried by ALLO/XEC/BTW/TRUMP; currently rejected only for weak volume confirmation and no catalyst, not for being extended" },
    "best_short_candidate": { "symbol": "RE/USDT", "trigger": "confirmed failed bounce / retest of breakdown structure with a clear stop above the swing high; do not short the current extended print", "reason": "weak_rs_short discovery-expansion candidate (score 72, RS -9.5% vs BTC) with a defined playbook (crypto_failed_bounce_short), but already >2ATR extended and direction=short is a losing bucket this week (PF 0.20) -- treat as watch-only, not a fresh chase" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT", "trigger": "a fresh setup forming on continued RWA/tokenization narrative strength (DTCC/SBI institutional thesis, rwa_narrative basket fresh <6h) that also survives the corroborated team-wallet-to-Coinbase sell-pressure headline; the existing sig_a914... is already closed (tp2_hit) and not itself re-actionable", "reason": "only symbol with both a fresh <6h catalyst-narrative basket membership and a live, if mixed, news thread; contradiction between bullish institutional thesis and bearish wallet-movement headline means any fresh setup needs the sell-pressure risk explicitly weighed" },
    "avoid_candidate": { "symbol": "HOME/USDT", "reason": "-14.97% 24h, thin-liquidity + short-squeeze-risk capped to C in the report itself, no fresh catalyst -- overextended on the downside and squeeze-prone if shorted late, consistent with the same avoid-note in the 2026-07-17 16:29 EEST review" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 6
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.75 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | caution | 0.70 | mixed, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, fresh_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.40 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | watch | 0.50 | overextended, price_moved_away, chase_risk | advisory_only |
| execution_lifecycle | needs_review | 0.85 | closed_flat, needs_review, no_entry | advisory_only |
| risk_manager | ok | 0.70 | reduce_risk | advisory_only |
| playbook_performance | caution | 0.75 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | watch_only | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-17_1629.md` (2026-07-17 16:29 EEST, pre-US-open decision review). Note the ~23h gap between that review and this one — six scheduled slots in between produced no output file (see TODO-11).

- **VIRTUAL/USDT (crypto swing long) — thesis INVALIDATED.** The 04:47 EEST swing report scored VIRTUAL/USDT 65.8 (B-tier, long, RS +4.3% vs BTC, momentum 80.4). The fresher 11:44 UTC (14:44 EEST) intraday scan now shows VIRTUAL/USDT with `bias short`, score 62.6, 24h -1.55%, RS/BTC -2.70%, tag `weak_vs_market`. This is a genuine regime flip in ~11 hours, not noise — do not treat the swing report's long thesis as live. Not previously covered in the prior review (VIRTUAL was not mentioned there).
- **TAO/USDT swing short** — mentioned as "stopped out (CLOSED LOSS)" in the prior review; not revisited this cycle (not in current active-signals or top movers).
- **ONDO/USDT** — unchanged lifecycle state (still `tp2_hit`, still past `expires_at`, still flagged TODO-2/10), but a *new* headline surfaced since the prior review: a corroborated (multiple independent outlets) team-wallet-to-Coinbase transfer reported ~10:00 UTC today, adding sell-pressure risk context on top of the existing bullish RWA/DTCC/SBI thesis. Net: still not re-actionable off the closed signal, watch for a fresh setup with this risk priced in.
- **Untracked legacy alerts (TODO-3)** — the prior review (and 3 before it) consistently found ALLO/USDT and BANK/USDT as unresolved untracked alerts. This run's detector returned **0 results** — first clean read in 4+ consecutive reviews. Treat as not-currently-reproducing; keep watching, do not close the underlying project-memory-tracked bug pattern yet.
- **market_dashboard_snapshots regime mismatch (TODO-9)** — prior review found `crypto_market_mode=trend` decoupled from the report-level `bearish trend (risk-off)` classifier. This run's latest snapshot (11:53 UTC) shows `crypto_regime=transition`, matching today's report-level `transition (mixed)` classifier. Appears resolved; watch for recurrence.
- **AVGO/XOM stocks pre-open ideas** — moot this run; it is Saturday, not a pre-open slot, no fresh stocks scan to compare against.
- **New finding**: stocks earnings-calendar lookup now failing for 10 tracked tickers (was TSLA/GOOGL only, TODO-7) — see §14.
- **New finding**: `news_items.published_at` stores inconsistent datetime formats (mixed UTC offsets, `Z` suffix, and 18 literal `date_unavailable` rows), which breaks naive lexicographic freshness filtering — see §14 (TODO-12). This review avoided relying on its own raw SQL freshness filters for any go/no-go decision as a result, using the app-computed `freshness` labels embedded in the catalyst/narrative files instead.

## 5. Catalyst Coverage

- Total `catalyst_events` today (rolling buffer): **2579**
- Mapped (non-null symbol): **449** (17.4%)
- Unmapped (null symbol): **2130** (82.6%)
- `narrative_baskets` count: **5** (rwa_narrative, perps_dex_narrative, binance_ecosystem_teaser, ai_narrative, momentum_breakout)

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Top unmapped headlines (excluding routine exchange trading-parameter notices):
- "💵×10 250,000,000 $USDC (250,074,750 USD) minted at USDC Treasury" (t.me feed, stablecoin mint alert, not symbol-mapped)
- "House Financial Services Committee Chair French Hill says Senate ... set a date to bring the CLARITY Act..." (crypto-policy headline, not symbol-mapped)
- "SBI Holdings completed its majority acquisition of Singapore's Coinhako..." (exchange-M&A headline, not symbol-mapped despite relevance to the rwa_narrative basket)

This is consistent with the previously logged catalyst-linkage gap (project memory: scan-time `news_supported` under-fires; symbol audit historically ~17% match rate, essentially unchanged today at 17.4% mapped).

## 6. Market Landscape

- BTC trend: uptrend. ETH trend: range. Altcoin breadth above EMA20: 39.5%; above EMA50: 42.1%.
- Volatility: BTC ATR percentile 31.0 ("normal/unknown" state).
- Macro/geopolitical risk score: **67.2/100** (BTC bias: risk-off headwind), down from 96/100 at the 2026-07-17 16:20 EEST review. Dominant driver remains the US-Iran/Gulf military conflict (missile/drone strikes, Strait of Hormuz tanker incidents, oil-price pressure). External verification via WebSearch confirms the conflict is real and ongoing but that Bitcoin's reaction has become comparatively muted in mid-July compared to the sharper early-July drawdowns (BTC swung $63K-$69K; by mid-month the market reportedly "does not price geopolitical risk the way it once did," with Fed policy competing as the primary driver) — [US-Iran military escalation rocks crypto markets as Bitcoin swings between $63K and $69K](https://cryptobriefing.com/us-iran-strikes-bitcoin-crypto-market-reaction/), [Iran Strikes Push Bitcoin Below $63K: Fed Policy Now Matters More Than War](https://www.techtimes.com/articles/320296/20260713/iran-strikes-push-bitcoin-below-63k-fed-policy-now-matters-more-war.htm).
- Stocks: closed (Saturday). No live session data; treat any stocks reference as planning/watchlist only through Sunday.

### Market Mood / Risk Routing

- Crypto mood: **transition / mixed / chop** — BTC constructive (uptrend) but ETH range-bound and breadth under 40%; no clean directional edge either way this cycle.
- Stocks mood: **closed** (weekend).
- Dominant narrative: RWA/tokenization (ONDO/XLM, DTCC/SBI institutional thesis, fresh <6h) competing against a corroborated ONDO team-wallet sell-pressure headline; secondary momentum-only cluster (XEC/BTW/ALLO, no catalyst, all overextended >2ATR — do not chase).
- Preferred side now: **wait-for-trigger**, mildly catalyst-backed-long-biased if RWA thesis holds and DODO/ONDO-style names pull back into a clean entry.
- Best long candidate: **DODO/USDT** — none clean right now; trigger: volume ≥1x + catalyst or pullback structure (see §3A).
- Best short candidate: **RE/USDT** — none clean right now; trigger: confirmed failed-bounce retest, not the current extended print (see §3A).
- Best catalyst-backed candidate: **ONDO/USDT** (fresh setup only, not the closed `sig_a914...`) — see §3A.
- What to avoid: **HOME/USDT** (thin, squeeze-prone, no catalyst, -15% already); also avoid chasing any name in the `momentum_breakout` basket (XEC/BTW/ALLO/TRUMP) at current extended prices.
- What would change the view: a volume-confirmed pullback entry on DODO, a confirmed failed-bounce on RE, a de-escalation or fresh escalation headline on the Iran/Gulf conflict, or Monday's US cash open bringing stocks back into play.

## 7. Candidate Deep Dives

### 7.1 DODO/USDT (crypto, long, watch-only)

- Has price already reacted to the catalyst? No verified catalyst exists yet — this is a pure RS/momentum read (score 81.6-82 in the funnel, composite score only 46.4 after gating).
- Is the setup chasing? Not currently — DODO is the only top-mover **without** the `overextended` (>2ATR from EMA20) tag, unlike ALLO/XEC/BTW/TRUMP.
- Retest/pullback structure? Not yet established; report explicitly notes "Volume is below average; breakout confirmation is weak."
- Overextended (>2 ATR from EMA20)? No (only rejected name in the top-8 movers without this flag).
- Would entry now be late? No, but entry now would be low-conviction (weak volume, no catalyst, mixed regime).
- What level makes it actionable? Volume expansion to >=1x the 20-period average, plus either a fresh verified catalyst or a clean 15m-1h pullback/retest structure.
- Aligned with current market mood? Partially — mood is wait-for-trigger/mixed, DODO fits the "not yet confirmed" bucket rather than a clean go.
- Long, short, or wait-for-trigger? Wait-for-trigger long.
- Actionable now or after confirmation? After confirmation only.
- What would invalidate it? BTC breakdown against the regime thesis, or RS reverting negative like VIRTUAL did this cycle.
- Chase-risk setup? No (that is precisely what differentiates it from ALLO/XEC/BTW/TRUMP).
- Catalyst confirmation or contradiction? Neither — no fresh verified catalyst detected per the report.
- **TradingView / manual chart check unavailable.** Using only local OHLCV/ATR/EMA fields from the report.

### 7.2 RE/USDT (crypto, short, watch-only)

- Has price already reacted? Yes — already -8.3% to -9.5% 24h, RS -9.5% vs BTC.
- Is the setup chasing? Yes if shorted at current print — tagged `overextended` (>2ATR from EMA20) in the rejected-list.
- Retest/pullback structure? The discovery-expansion playbook (`crypto_failed_bounce_short`) explicitly requires a failed-bounce/retest confirmation before entry, which has not yet formed per this cycle's data.
- Would entry now be late? Yes, entering the current print would be late/chasing.
- What level makes it actionable? A confirmed failed bounce with bearish HTF structure, derivatives confirmation, and a clear stop above the swing high (per the discovery-expansion "promotes when" note).
- Aligned with mood? Partially — mixed/chop mood argues for caution on any short, and direction=short is a losing bucket this week (PF 0.20, totalR -4.0, n=12) per `signal-stats`.
- Long, short, wait-for-trigger? Wait-for-trigger short.
- Actionable now or after confirmation? After confirmation (retest) only.
- What would invalidate it? A reclaim of the breakdown level or broader altcoin-breadth improvement.
- Chase-risk setup? Yes at current price.
- Catalyst confirmation/contradiction? No fresh catalyst identified for RE/USDT specifically.
- **TradingView / manual chart check unavailable.**

### 7.3 ONDO/USDT (crypto, catalyst-watch, existing signal closed)

- Has price already reacted to the catalyst? The existing signal (`sig_a914cdba49291324`, B, intraday, long) already achieved `tp2_hit` before its 2026-07-17T08:36 UTC expiry — largely already played out.
- Is the setup chasing? N/A — no live signal.
- Retest/pullback structure? Not evaluated this cycle (no fresh report-level score for ONDO in today's scans).
- Overextended? Not evaluated this cycle.
- Would a fresh entry now be late? Unknown without a fresh score; flagged for the next cycle's scan to re-evaluate.
- What level makes a fresh setup actionable? A new proposed_signal with the RWA/DTCC/SBI thesis intact and the wallet-sell-pressure risk explicitly weighed in the risk gate.
- Aligned with mood? The RWA basket is fresh (<6h) and catalyst-backed, fitting the "catalyst-backed longs" preference, but the corroborated sell-pressure headline is a live contradiction.
- Long, short, wait-for-trigger? Catalyst-watch / wait-for-trigger — no live entry to take.
- Actionable now? No — the tracked signal is closed; only a fresh signal from a future scan would be actionable.
- What would invalidate a fresh long thesis? Confirmed exchange deposit/sale execution following the team-wallet transfer (would flip this from "watch" to "avoid").
- Chase-risk? N/A.
- Catalyst confirmation or contradiction? **Both** — bullish (DTCC/SBI institutional partnerships, rwa_narrative basket) and bearish (corroborated team-wallet-to-Coinbase transfer pattern, historically preceded exchange sales) are simultaneously live. Sources: [Ondo Finance moves $63.9mln: Is a sell-off looming?](https://ambcrypto.com/ondo-finance-moves-63-9mln-is-a-sell-off-looming/), [Analyst Flags $49.56M ONDO Transfer from Team Wallet as Potential Sell-Off](https://cryptonews.net/news/altcoins/33048535/), internal `news_items`: "Ondo wallet activity surges after DTCC, SBI deals as ONDO eyes $0.38" (AMBCrypto, 2026-07-17T16:30 UTC).
- **TradingView / manual chart check unavailable.**

## 8. Best Candidates Ranked

No clean Telegram-actionable A/B exists in either asset class right now (crypto: no fresh A/B this cycle, one prior swing long thesis invalidated; stocks: fully closed for the weekend). Per PART 9, the best watch-list:

1. **Best long-watch: DODO/USDT** — wait for volume expansion (>=1x 20-period avg) plus catalyst or clean pullback structure; do not chase the current +10.2% print.
2. **Best short-watch: RE/USDT** — wait for a confirmed failed-bounce/retest with a clear stop above the swing high; direction=short is a losing bucket this week, treat with extra caution.
3. **Best catalyst-watch: ONDO/USDT** — RWA/DTCC/SBI thesis fresh <6h vs a corroborated team-wallet-to-Coinbase sell-pressure headline; watch for a fresh signal that explicitly prices the sell risk, the existing closed signal is not re-actionable.
4. **Invalidated (no longer a watch item): VIRTUAL/USDT** — the 04:47 EEST swing long thesis (RS +4.3%) has flipped to `bias short` / RS -2.70% in the 11:44 UTC scan; drop from any active watchlist until it re-confirms one direction.
5. **Secondary avoid-adjacent watch: HOME/USDT / BANK/USDT** — both explicitly capped to C for short-squeeze-risk / thin-liquidity in the report; only relevant as a "what not to chase" reference, not a trade idea.

## 9. Avoid / No Trade

This decision window only — never a system-stop signal, scanning/tracking continues in all cases.

- **HOME/USDT** — already -14.97% 24h, thin liquidity + short-squeeze-risk capped to C, no fresh catalyst. Overextended on the downside; avoid chasing the breakdown further (unchanged conclusion from the 2026-07-17 16:29 EEST review).
- **BANK/USDT** — -10.79% 24h, also short-squeeze-risk capped to C, thin volume (0.22x). Same avoid logic as HOME.
- **Any name in the `momentum_breakout` basket at current price** (XEC/BTW/ALLO/TRUMP) — pure momentum with no verified catalyst, all >2ATR from EMA20; the system prefers missing the move over chasing it, per the report's own no-trade warning.
- **Stocks, broadly** — market closed all weekend; treat every stocks reference in this review as planning-only, not actionable until RTH confirmation Monday.

## 10. Main Risks

- **Geopolitical**: US-Iran/Gulf conflict remains the dominant macro overhang (risk score 67.2/100); a fresh escalation could reverse the recent de-escalation in market reaction and hit BTC/ETH sharply given still-elevated but declining risk-off positioning.
- **ONDO sell-pressure**: corroborated team-wallet-to-Coinbase transfer pattern is a real, multi-outlet-confirmed risk on the RWA narrative's cleanest name; not yet resolved either way.
- **Data-quality**: catalyst mapping at 17.4% and a confirmed `published_at` format inconsistency (TODO-12) mean this review leaned on report-embedded freshness labels rather than raw DB freshness queries where possible — any future session running raw SQL freshness filters against `news_items` should be aware of this.
- **Lifecycle hygiene**: two crypto signals (NEAR, ONDO) are past their `expires_at` while still showing non-terminal `tp1_hit`/`tp2_hit` status (TODO-2/10, recurring) — does not affect trading decisions this run but degrades the clarity of the active-signals view.
- **Live-execution-adjacent**: `mexc_canary_monitor` still crash-looping on `database is locked` (TODO-8) — self-recovering via restart per prior observation, but touches a kill-switch write path and remains unresolved across at least 2 review cycles.

## 11. Action Plan — next 4 hours

1. Monitor DODO/USDT for a volume pickup or fresh catalyst; no entry without one.
2. Monitor RE/USDT for a failed-bounce/retest structure; no entry on the current extended print.
3. Watch for a fresh ONDO/USDT scan-level score in the next scalp/intraday cycle now that the wallet-transfer headline is public; if a fresh signal fires, the risk gate should ideally reflect the sell-pressure context (advisory note only, no scoring change requested).
4. Drop VIRTUAL/USDT from any active watchlist until it re-confirms a single direction — do not act on the stale 04:47 EEST long thesis.
5. No stocks action possible or expected until Monday's RTH open.
6. Continue scanning/tracking/monitors as normal — no pause or stop recommended anywhere in this review.

## 12. Final Verdict per Mode

- **Crypto scalp**: No trade. No A/B this cycle; mode remains a structurally losing bucket this week (PF 0.17, 0W/7L) — treat any future scalp signal with extra skepticism per the report's own low-confidence header.
- **Crypto intraday**: No trade. No A/B this cycle; mode performance strong this week (PF 4.64, totalR +18.2) when signals do fire — worth staying attentive for the next cycle.
- **Crypto swing**: Watch-only, no trade. VIRTUAL/USDT thesis invalidated; no other swing idea this cycle (report is 11h old).
- **Stocks (all modes)**: Closed / no trade. Planning-only until Monday's RTH open.

## 13. Sources

- [US-Iran military escalation rocks crypto markets as Bitcoin swings between $63K and $69K](https://cryptobriefing.com/us-iran-strikes-bitcoin-crypto-market-reaction/) — CryptoBriefing, undated (retrieved 2026-07-18).
- [Iran Strikes Push Bitcoin Below $63K: Fed Policy Now Matters More Than War](https://www.techtimes.com/articles/320296/20260713/iran-strikes-push-bitcoin-below-63k-fed-policy-now-matters-more-war.htm) — Tech Times, 2026-07-13.
- [Ondo Finance moves $63.9mln: Is a sell-off looming?](https://ambcrypto.com/ondo-finance-moves-63-9mln-is-a-sell-off-looming/) — AMBCrypto, undated (retrieved 2026-07-18).
- [Analyst Flags $49.56M ONDO Transfer from Team Wallet as Potential Sell-Off](https://cryptonews.net/news/altcoins/33048535/) — CryptoNews, undated (retrieved 2026-07-18).
- Internal: `news_items` row "ONDO team-linked wallet sends 26M tokens to Coinbase – Sell-off next?" (AMBCrypto via internal collector, 2026-07-18T10:00:12 UTC, single_source at ingest, corroborated externally this review).
- Internal: `data/catalysts/2026-07-18/narrative_baskets.jsonl`, `catalyst_cycle_11-47.md`.

## 14. Fix Requests / TODO

### TODO-1 (carried forward, unchanged, informational)
- **issue:** Stocks intraday A/B guard combination continues to demote technically-qualified candidates via the market-closed gate. Today is Saturday (fully closed, not just pre-open) so this is fully expected/by-design.
- **evidence:** `data/reports/stocks/intraday/2026-07-17_21-56_stocks_intraday_report.md` — `market_closed_intraday_planning_only` caps applied to NVDA/AVGO/NFLX/COIN/UNH.
- **suggested manual fix:** none needed; re-confirm as by-design.
- **priority:** low.
- **first observed:** 2026-07-16 18:39 EEST review; re-confirmed 2026-07-18 15:48 EEST.

### TODO-2 / TODO-10 (carried forward, unchanged — still high)
- **issue:** Crypto and stocks signals continue to show `expires_at` timestamps in the past while still displaying non-terminal statuses (`tp1_hit`, `tp2_hit`, `triggered`).
- **evidence:** `active-signals --asset-class crypto` this cycle: NEAR/USDT (`tp1_hit`, expires 2026-07-17T15:56 UTC, ~1 day past) and ONDO/USDT (`tp2_hit`, expires 2026-07-17T08:36 UTC, ~1.4 days past). Stocks side shows the same pattern across dozens of rows (e.g. JPM expires 2026-07-11, COIN expires 2026-07-03).
- **suggested manual fix:** human check of the lifecycle/track-signals terminalization job for both asset classes.
- **priority:** high (unchanged).
- **first observed:** 2026-07-16 16:20 EEST review (stocks); 2026-07-17 16:29 EEST review (crypto).

### TODO-3 (not reproducing this run — keep watching)
- **issue:** `detect_untracked_legacy_alerts` had returned the same 2 unresolved results (ALLO/USDT, BANK/USDT) across 4+ consecutive reviews.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-18` returned 0 results this run — "Every legacy crypto alert has a backing proposed_signal."
- **suggested manual fix:** none needed if this stays clean; do not close the underlying project-memory-tracked bug pattern until confirmed clean across several more cycles.
- **priority:** medium (downgraded from high pending re-confirmation).
- **first observed:** 2026-07-16 18:39 EEST review; not reproducing as of 2026-07-18 15:48 EEST.

### TODO-6 (carried forward, unchanged)
- **issue:** Crypto scalp mode remains a consistent losing bucket.
- **evidence:** `signal-stats --asset-class crypto` this cycle, "By mode": `mode=scalp | n=22 | conf=weak | trig=20 | wins=0 losses=7 | PF 0.1667 | avgR -0.2941 | totalR -5.0`. Related: `direction=short | n=12 | PF 0.20 | totalR -4.0` — scalp's dominant short-side plays likely overlap with this losing bucket.
- **suggested manual fix:** human review of whether scalp (and/or short-direction plays specifically) should carry an explicit non-actionable label given the consistency of the negative edge.
- **priority:** medium.
- **first observed:** 2026-07-17 11:45 EEST review.

### TODO-7 (carried forward, evidence upgraded — now high)
- **issue:** Stocks earnings-calendar lookup is failing far more broadly than previously scoped — not just TSLA/GOOGL.
- **evidence:** `data/reports/stocks/intraday/2026-07-17_21-56_stocks_intraday_report.md` §0: "Earnings events tracked: 0" / "Earnings lookup failed for: AAPL, MSFT, NVDA, TSLA, META, AMZN, GOOGL, AMD, NFLX, COIN". This is directly demoting multiple would-be-A candidates (NVDA, AVGO, NFLX, COIN, UNH) to C via `stale_post_earnings_setup ... calendar is UNKNOWN`.
- **suggested manual fix:** human audit of the earnings-calendar source/ingestion — appears to be a broad outage, not a per-ticker gap.
- **priority:** high (upgraded from low-medium).
- **first observed:** 2026-07-17 11:45 EEST review (TSLA/GOOGL only); scope widened 2026-07-18 15:48 EEST review (10 tickers, 0 events tracked).

### TODO-8 (carried forward, unchanged — still high)
- **issue:** `mexc_canary_monitor` continues crash-looping on `sqlite3.OperationalError: database is locked` inside `ensure_tables()` while writing the kill-switch control row.
- **evidence:** `data/scheduled_runs/2026-07-18_default_schedule/mexc_canary_monitor_1784374377.log` (latest today) — same traceback at `src/live_execution/store.py:142`/`service.py:355` as prior instances.
- **suggested manual fix:** human investigation of lock contention on `db/crypto_ai_desk.sqlite` around `mexc_canary_control` writes (WAL-mode/timeout/concurrent-writer issue) — touches a kill-switch write path, treat with real urgency despite self-recovering via restart.
- **priority:** high (unchanged).
- **first observed:** 2026-07-17 11:45 EEST review.

### TODO-9 (not reproducing this run — keep watching)
- **issue:** `market_dashboard_snapshots.crypto_market_mode` had looked decoupled from the report-level regime classifier.
- **evidence:** Latest snapshot (id=192, 2026-07-18T11:53:51 UTC): `crypto_regime=transition`, matching today's report-level `transition (mixed)` classifier. `crypto_market_mode` now reads `unknown` rather than a contradicting `trend` label.
- **suggested manual fix:** none needed if this stays consistent; re-confirm over a few more cycles before closing.
- **priority:** low (downgraded from medium pending re-confirmation).
- **first observed:** 2026-07-17 11:45 EEST review; not reproducing as of 2026-07-18 15:48 EEST.

### TODO-11 (new — high)
- **issue:** This task (`opus-enriched-review-4h`, fires 04:30/11:30/18:30/21:30 EEST) and/or its sibling tasks (`opus-enriched-review-preus` at 16:20, `opus-enriched-review-postclose` at 23:15) appear to have skipped six consecutive scheduled dispatches between the last successful review (2026-07-17 16:29 EEST) and this one (2026-07-18 15:48 EEST): the 2026-07-17 18:30, 21:30, and 23:15 slots, and the 2026-07-18 04:30, 11:30, and 16:20 slots. No `OPUS_ENRICHED_REVIEW_DEFERRED_*` or `OPUS_ENRICHED_REVIEW_BLOCKED_*` marker file exists for any of these six windows, meaning the skip happened upstream of this skill's own defer/block logic (which always writes a marker) — i.e. the scheduling/dispatch layer itself, not this routine's freshness check.
- **evidence:** `ls OPUS_ENRICHED_REVIEW*.md` shows the most recent files jumping directly from `..._2026-07-17_1629.md` to this run; no DEFERRED/BLOCKED files exist for the six intervening slots (checked via `ls OPUS_ENRICHED_REVIEW_DEFERRED*2026-07-1[78]*` / `OPUS_ENRICHED_REVIEW_BLOCKED*2026-07-1[78]*`, both empty). This run itself dispatched at ~15:40-15:48 EEST, which matches none of the four slots this task owns.
- **suggested manual fix:** human check of the outer scheduling mechanism for `opus-enriched-review-4h` / `-preus` / `-postclose` (e.g. `CronList`/Windows Task Scheduler registration, whether the host process was asleep/restarted, whether a prior run hung and blocked the next dispatch).
- **priority:** high.
- **first observed:** 2026-07-18 15:48 EEST review.

### TODO-12 (new — medium)
- **issue:** `news_items.published_at` stores inconsistent datetime formats across rows: some `...+00:00`, some `...Z`, some `...-04:00` (non-UTC offset), and 18 rows with the literal string `date_unavailable`. This breaks naive lexicographic string comparisons (e.g. `WHERE published_at > datetime('now','-N hours')`), because a `-04:00`-offset timestamp can sort as "older" than it actually is in absolute time, and `date_unavailable` sorts after all real dates (breaking any `MAX(published_at)` freshness check).
- **evidence:** Direct query this run: `SELECT MAX(published_at) FROM news_items` returned `'date_unavailable'` instead of a real timestamp. Sample mixed-format rows (by `id DESC`): id 274488 `'2026-07-18T04:02:00-04:00'`, id 274439 `'2026-07-17T10:13:50Z'`, id 274384 `'2026-07-18T11:38:12+00:00'`. A naive `published_at > datetime('now','-4 hours')` filter against `source LIKE 't.me/%'` returned stale-looking rows (latest 2026-07-18T01:16 UTC) even though `news_source_runs` confirms telegram collectors were actively producing items within the same window (590 items across 52 `ok` runs in the prior 3h) — i.e. the collector is healthy, the filter is not.
- **suggested manual fix:** human audit of the `published_at` normalization step in the news ingestion pipeline; standardize to a single UTC ISO format (or add a parsed/normalized numeric epoch column) so downstream freshness queries are reliable. Low urgency operationally today (this review worked around it by using report-embedded freshness labels instead of raw SQL), but any future automated freshness-based gating logic reading `published_at` directly is at risk of false "stale" classifications.
- **priority:** medium.
- **first observed:** 2026-07-18 15:48 EEST review.

_All other checks clean this run: no new legal/headline-risk crypto candidates, no new system-integrity anomalies beyond the above._
