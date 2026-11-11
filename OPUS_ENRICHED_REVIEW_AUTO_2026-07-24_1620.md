# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:20 EEST

## 1. Executive Summary

Slot: **pre-US-open decision review** (run at 16:27 EEST, 2026-07-24, ~3min before the 16:30 EEST / 09:30 ET cash open). **Advisory only — no auto-trade, no scoring/strategy changes.** Crypto: **0 A/B-tier fresh** across scalp (12:54 gen), intraday (12:55 gen), and swing (13:26 gen) — all three independently conclude "no trade." Regime is **bearish/risk-off** on all three timeframes: BTC and ETH both read `transition_down`, altcoin breadth above EMA20 is **0.00%**, macro/geopolitical risk score **89-91/100** driven by escalating Iran/Strait-of-Hormuz headlines (oil +10% weekly, Trump reportedly weighing a larger strike). 17 crypto B-tier signals remain tracked from prior cycles — only RE/USDT is genuinely WAITING for entry and LA/USDT swing is the one live OPEN position; the other 15 are ENTERED-UNRESOLVED (TP1/TP2 partially banked, validity window since closed) — no fresh action needed on those. **Untracked-alert detector clean** (0 rows). Stocks: market is still **closed** at run time (opens in ~3 minutes) — 15 raw **A-tier** short setups (MSFT, AMZN, TSLA, AAPL, META, COIN, MSTR, SPY, QQQ, PLTR, XLF, GOOGL, DIA, XLY) plus one A-tier long (JPM) are all demoted to C purely for `market_closed_intraday_planning_only` — **this is the pre-open watchlist to confirm at/after the open**, not a rejection of the setups themselves. Two of these carry independently-**externally-confirmed** legal/headline risk that survives the open: **MSFT** (real, ongoing securities-fraud class action re Copilot/Azure misrepresentation, lead-plaintiff deadline Aug 11 2026 — §13) stays **AVOID**; **TSLA** carries a real, externally-confirmed Q2 earnings miss + 14.4% one-day crash (July 23) with negative FCF, but the internal `going_concern` tag itself is **not** corroborated by any external source found (TODO-3, carried) — treat TSLA as a legitimate but **post-earnings, gap-risk, needs-fresh-levels** short-watch, not a going-concern AVOID. **AMZN**'s only symbol-tagged risk item ("Russia's Amazon" Wildberries hub attacks) is a **false symbol match** — a different company — while a separate, real Iran-IRGC claim of an AWS-Bahrain strike (externally confirmed to exist, but **AWS itself has not confirmed any service impact** and Bahrain says the attack was intercepted — §13) makes AMZN's short thesis geopolitically-aligned but **not yet a confirmed fundamental hit**. Stocks C-tier overall quality remains weak (winrate 1.9%, PF 0.56, n=185) — consistent with the known, already-documented systemic issue that stocks C-tier is watchlist/research-only, never actionable. Catalyst mapping is **weak this run** (76.8% unmapped, 2,242/2,920) — use as context only. VIX at 18.84 is notably calm given the 89-91/100 geopolitical risk score — a real divergence worth watching into the open. No clean crop this window is a routed **watch-only + wait-for-RTH-confirmation** call, not a system-wide stop — scanning, tracking, and monitors continue in all moods.

## 2. Data Used

- Crypto scalp: `data/reports/scalp/2026-07-24_12-54_scalp_report.md` (data freshness 2026-07-24 12:30 UTC, ~3h57m old at run time — within intraday-relevance band, no fresher scalp cycle available)
- Crypto intraday: `data/reports/intraday/2026-07-24_12-55_intraday_report.md` (same data freshness 12:30 UTC)
- Crypto swing: `data/reports/swing/2026-07-24_13-26_swing_report.md` (generated 16:26:28 EEST, ~1min old — fresh; data freshness still 12:30 UTC underlying)
- Stocks intraday: `data/reports/stocks/intraday/2026-07-24_13-25_stocks_intraday_report.md` (data freshness 13:24 UTC / ~16:24 EEST, ~3min old — fresh; report's own banner: market closed, planning-only, re-evaluate at/after the 09:30 ET open)
- Stocks swing/invest: last available `2026-07-02_13-0x` reports (~22 days stale, deprecated framework per project history — not used)
- Catalyst layer: `data/catalysts/2026-07-24/catalyst_events.jsonl` (2,920 cumulative rows today), `narrative_baskets.jsonl` (4 baskets), latest cycle file `catalyst_cycle_12-58.md` (mtime 15:58 EEST)
- LLM packets: `data/processed/llm_analysis_packet.md` (mtime 15:56, fresh), `data/processed/llm_stocks_packet.md` (mtime 16:14, fresh)
- CLI (re-run this cycle): `active-signals` crypto (17 active, 1 waiting_for_entry, 1 open/triggered, 15 entered-unresolved) / stocks (50 active — 15 within-window "invest"-tier OPEN, 35 past-expiry entered-unresolved, 0 waiting_for_entry), `signal-stats` crypto (n=176 reliable, PF 1.92; scalp mode PF 0.67 losing, short direction 0/4 wins PF 0.00, breakdown setup 0/5 wins) / stocks (headline n/a this week — 0 A/B triggered; C-tier n=185, PF 0.562, winrate 1.9%), `detect_untracked_legacy_alerts --since 2026-07-24` → **0 rows, clean**
- Scheduler log: `data/scheduled_runs/2026-07-23_default_schedule/scheduler.log` (latest activity 16:26 EEST, ~1min old — actively mid-cycle, well under the 3h defer threshold)
- Monitor/paper processes: `crypto_monitor` last cycle 16:23 EEST (all names watchlist/rejected, no new A/B promotions), `mexc_canary_monitor` heartbeat OK/reconcile OK but worker `RETRY_DB_BUSY` recurring (132 occurrences in the current log segment — related to carried TODO-1 DB-contention pattern, different subsystem than the scheduler's own lock errors)
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-24_1140.md` (11:39 EEST, Europe/pre-US slot) — used for §4 comparison
- External (WebSearch ×3 + WebFetch not needed, search snippets sufficiently corroborated/refuted each claim — see §13): (1) "Amazon AWS Bahrain server damage Iran claim July 2026", (2) "Tesla TSLA going concern warning July 2026", (3) "Microsoft MSFT securities fraud class action lawsuit July 2026", (4) "Bitcoin ETF record outflows $3.4 billion sell-off July 2026"

## 3. Scheduler / Data Freshness

- `scheduler.log`: latest activity 16:26 EEST (~1min old), mid-cycle (stock coverage gate, crypto quality overlay, crypto swing versioned shadow sweep all completed in the last 10 minutes) — **not deferred**, nowhere near the 3h threshold.
- Crypto scalp/intraday: data freshness 12:30 UTC (~3h57m old at run time) — no fresher scalp/intraday cycle has completed since; used as the freshest available, flagged as carry-forward-band for intraday purposes.
- Crypto swing: generated 16:26 EEST (~1min old) — fresh.
- Stocks intraday: data freshness 13:24 UTC (~3min old) — fresh; market itself is closed until the 09:30 ET open (~3min from run time), so content is planning-only per the report's own gate, exactly as expected for this slot.
- Stocks swing/invest: ~22 days stale — not used (deprecated framework, unchanged from all prior reviews).
- Catalyst scan: today's directory present, actively growing (2,920 cumulative rows, latest cycle file 15:58 EEST, ~29min old).
- Monitors: `crypto_monitor` 16:23 EEST (fresh, all watchlist/rejected — KAITO/USDT upgraded rejected→C this cycle, still watchlist not actionable); `mexc_canary_monitor` heartbeat OK but repeated `RETRY_DB_BUSY` on the worker claim stage (132 occurrences in-window) — related to the carried TODO-1 SQLite-contention pattern (different log/subsystem than the scheduler's own "database is locked" errors, which remain at 0 today).
- Paper/execution: no stall indicators; `stocks_monitor_session` and related steps completed normally per scheduler.log tail.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-24 16:27 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["crypto scalp/intraday data ~4h old, no fresher cycle available", "stocks swing/invest ~22d stale, deprecated framework"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log latest activity 16:26 EEST, mid-cycle, well under 3h defer threshold", "stocks intraday report data freshness 13:24 UTC (~3min old)", "crypto swing report generated 16:26 EEST (~1min old)"] },
    { "agent": "market_regime", "verdict": "risk_off", "confidence": 0.75,
      "reason_codes": ["risk_off", "shorts_preferred", "danger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: all 3 reports agree BTC=transition_down, ETH=transition_down, altcoin breadth above EMA20=0.00%, recommended style='short bias or no trade'", "stocks: regime label risk_off/bias=short, VIX 18.84, breadth above EMA20 0.0%, 0/4 indices in uptrend, SPY/QQQ both downtrending 5d", "macro/geopolitical risk 89-91/100 across crypto reports driven by Iran/Strait-of-Hormuz escalation"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.4,
      "reason_codes": ["mapping_weak", "no_catalyst", "fresh_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["76.8% of today's cumulative catalyst_events.jsonl unmapped (2242/2920 empty-symbol rows)", "4 active baskets: delisting_thin_liquidity (STX), perps_dex_narrative (HYPE), rwa_narrative (ONDO/XLM), ai_narrative (NEAR/RENDER/TAO/FET) — none scored into a top-setups table this cycle", "AMZN's only symbol-tagged risk headline is a false match (Wildberries, 'Russia's Amazon', unrelated company) — TODO candidate for the news entity resolver"] },
    { "agent": "derivatives_squeeze", "verdict": "data_unavailable", "confidence": 0.3,
      "reason_codes": ["data_unavailable"],
      "data_missing": ["Binance futures funding/OI (54 symbols failed)", "Bybit/OKX cross-check unavailable for BTC/ETH"],
      "suggested_effect": "advisory_only",
      "facts_used": ["all 3 crypto reports: 'futures data unavailable' for BTC/ETH; both BTC/ETH short setups explicitly capped to C for 'short squeeze risk → no_derivatives_thin_short'"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["stale_before_entry", "entry_late", "chase_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 0 A/B setups on all 3 timeframes, 'no trade' explicit in each report's final summary", "stocks: 15 raw-A setups demoted to C solely for market-closed gate — technical levels themselves are pre-open, need RTH confirmation before any entry; TSLA + GOOGL additionally carry stale_post_earnings_setup (fresh earnings prints July 22-23 invalidate pre-earnings levels)"] },
    { "agent": "execution_lifecycle", "verdict": "entered_unresolved", "confidence": 0.75,
      "reason_codes": ["entered_unresolved", "waiting_for_entry", "open_actionable", "review_shadow"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 17 active — RE/USDT WAITING for entry; LA/USDT swing OPEN (triggered, live, expires 2026-07-31); remaining 15 ENTERED-UNRESOLVED (tp1/tp2_hit, validity window since closed, e.g. LA/USDT scalp sig_b23fd157d1c64325 confirmed status=expired at 2026-07-24T09:27 UTC — TP1/partial banked, no further resolution before window shut)", "stocks: 50 active — 15 'invest'-tier signals still within validity window (OPEN/tracking toward further TP, expiry 07-31/08-01), 35 past-expiry intraday/swing signals ENTERED-UNRESOLVED, 0 waiting_for_entry", "24 today's stocks C-tier candidates are REVIEW/SHADOW (planning-only, not yet actionable pending RTH confirmation)", "detect_untracked_legacy_alerts → 0 rows, clean"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["headline_risk", "legal_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["MSFT: securities-fraud class action externally CONFIRMED real and ongoing (lead-plaintiff deadline Aug 11 2026, re Copilot/Azure misrepresentation, stock drop Jan 28 2026) — AVOID stands independent of market open", "TSLA: Q2 earnings miss + 14.4% crash (July 23) externally CONFIRMED real; internal 'going_concern' tag NOT externally corroborated by any auditor opinion found — treat as post-earnings gap-risk, not going-concern AVOID (TODO-3 carried)", "AMZN: AWS-Bahrain strike claim externally CONFIRMED to exist (Iran IRGC claim, multiple outlets) but AWS itself has not confirmed service impact and Bahrain says intercepted — geopolitical noise, not a confirmed fundamental hit; separately, the internally-tagged 'Wildberries=Russia's Amazon' risk item is a false symbol match, unrelated to AMZN", "macro/geopolitical risk 89-91/100 (Iran/Strait of Hormuz, oil +10% weekly) vs VIX only 18.84 — a real divergence, treat index-level complacency with caution into the open"] },
    { "agent": "playbook_performance", "verdict": "playbook_failing", "confidence": 0.6,
      "reason_codes": ["playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: scalp mode PF 0.67 (avgR -0.10, losing), short direction 0/4 wins (PF 0.00, n=6), breakdown setup 0/5 wins (n=7) — three known-weak buckets, none active this cycle", "crypto overall B-tier: PF 1.92, winrate 23.4%, totalR +44.01 (n=176) — headline number remains solid despite the weak sub-buckets", "stocks: C-tier n=185, winrate 1.9%, PF 0.562 — consistent with the already-documented systemic finding that stocks C-tier is watchlist-only, never actionable (project history)"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "shorts",
    "best_long_candidate":     { "symbol": "JPM", "trigger": "wait for RTH open + first 15-30min confirmation of the long thesis (financials sector RS +3.25% vs SPY); demoted to C purely for market-closed gate, no legal/headline flag", "reason": "only clean A-tier long on either desk this cycle, backed by a genuinely strong sector (financials)" },
    "best_short_candidate":    { "symbol": "AMZN", "trigger": "wait for RTH open + confirmation the 94/93.8-score short setup holds; demoted to C purely for market-closed gate, no legal/headline flag surviving verification (AWS-Bahrain claim is real but AWS-unconfirmed/intercepted, not a fundamental hit)", "reason": "highest-score clean short (no legal caveat) aligned with risk_off/bias=short regime and weak tech/discretionary sector RS" },
    "best_catalyst_candidate": { "symbol": "TSLA", "trigger": "wait for RTH open + fresh post-earnings levels (pre-earnings levels explicitly invalid per stale_post_earnings_setup); real Q2 miss + 14.4% crash July 23 is the clearest externally-confirmed catalyst on the desk, but going_concern tag is unconfirmed — treat as earnings-driven short-watch, not legal AVOID", "reason": "only stocks candidate with a fully externally-verified, fresh (within 48h) fundamental catalyst" },
    "avoid_candidate":         { "symbol": "MSFT", "reason": "highest raw score on the stocks desk (94.26) but carries an externally-confirmed, active securities-fraud class action (lead-plaintiff deadline Aug 11 2026) — not tradeable even post-open without a manual legal-risk sign-off" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | risk_off | 0.75 | risk_off, shorts_preferred, danger | advisory_only |
| catalyst_narrative | caution | 0.40 | mapping_weak, no_catalyst, fresh_catalyst | advisory_only |
| derivatives_squeeze | data_unavailable | 0.30 | data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | stale_before_entry, entry_late, chase_risk | advisory_only |
| execution_lifecycle | entered_unresolved | 0.75 | entered_unresolved, waiting_for_entry, open_actionable, review_shadow | advisory_only |
| risk_manager | caution | 0.70 | headline_risk, legal_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | playbook_failing | 0.60 | playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Comparing against `OPUS_ENRICHED_REVIEW_AUTO_2026-07-24_1140.md` (11:39 EEST, Europe/pre-US slot):

- **Regime flipped bearish:** the 11:39 review read crypto as mixed-to-mildly-bullish (BTC/ETH trend flipped to uptrend that cycle, altcoin breadth 46.2% above EMA20). This cycle, all three crypto timeframes now agree BTC/ETH are back to `transition_down` and altcoin breadth has collapsed to **0.00%** above EMA20 — a clean deterioration, not a disagreement between timeframes this time.
- **LA/USDT scalp resolved:** the 11:39 review's flagged live position (LA/USDT scalp, expiring ~12:26 EEST) has since resolved to `status=expired` (confirmed via direct DB check) — no TP/SL hit before the window closed. ENTERED-UNRESOLVED, not a loss or a win; the LA/USDT swing leg remains open (unaffected, invalidation 0.0646, expires 07-31).
- **BANK/USDT still watch-only:** carried from 11:39, still C-tier/watchlist, no promotion.
- **Macro risk re-elevated:** geopolitical risk score moved from 88.6-88.8/100 (11:39) back up to 89-91/100 this cycle, with a new/refreshed macro headline set (oil +10% weekly, "bigger than ever" Iran strike framing) — consistent direction, mild re-escalation.
- **Stocks desk unchanged in composition, now imminent:** the same 15 raw-A short setups + JPM long remain demoted to C for market-closed — but the open is now ~3 minutes away rather than ~5 hours away. This cycle is the last chance to finalize the pre-open watchlist before RTH confirmation is possible.
- **New this cycle:** external verification of three carried/flagged items — (1) TSLA's post-earnings crash is now externally confirmed (was previously flagged only internally); (2) MSFT's securities-fraud class action is externally confirmed as real, ongoing, with a specific Aug 11 2026 deadline; (3) AMZN's AWS-Bahrain risk claim is confirmed to exist but confirmed **not** to have caused verified service impact — narrows the AMZN risk read from "unknown headline" to "geopolitical noise, unconfirmed material impact."
- **Unchanged/carried:** MSFT AVOID stands (now externally reinforced). TSLA `going_concern` tag re-fires again this cycle and remains externally uncorroborated (TODO-3). Catalyst mapping remains weak (76.8% unmapped vs ~78.3% at 11:39 — consistent in kind). `detect_untracked_legacy_alerts` clean again (0 rows). Crypto scalp mode / short direction / breakdown setup remain the three known-weak sub-buckets in signal-stats, unchanged.

## 5. Catalyst Coverage

- Cumulative logged rows across today's scan cycles (`catalyst_events.jsonl`): **2,920** total; mapped (non-empty symbol): **678** (23.2%); unmapped: **2,242** (**76.8%**).
- Narrative baskets (4, current as of the 15:58 catalyst cycle / 13:26 swing report): `delisting_thin_liquidity` (primary STX/USDT, fresh <24h), `perps_dex_narrative` (primary HYPE/USDT, fresh <24h), `rwa_narrative` (primary ONDO/USDT, XLM/USDT, freshness unknown), `ai_narrative` (primary NEAR/USDT, RENDER/USDT, TAO/USDT, FET/USDT, freshness unknown).

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

Top unmapped-style headlines (sampled, out-of-universe issuers or generic listicles — not resolver gaps):
1. "Artificial Intelligence Stocks Under $10" (Benzinga Movers) — generic listicle, no single tracked symbol.
2. "Top Performing High Short Interest Stocks" (Benzinga Movers) — generic listicle.
3. "Bitcoin Falls as Record ETF Outflows and Strategy Sale Hit Sentiment" (Investing.com) — genuinely BTC-relevant but resolver did not tag the symbol; externally, the "record" framing traces to June's $4B monthly outflow record (Bloomberg, §13) rather than a fresh July 24 event — treat the headline's "record" claim with caution, underlying risk-off ETF-flow trend is real but not new today.

## 6. Market Landscape

**Crypto:** All three timeframes (scalp 12:30 UTC data, intraday 12:30 UTC data, swing generated 16:26 EEST) agree: BTC trend `transition_down`, ETH trend `transition_down`, altcoin breadth above EMA20 **0.00%**, recommended style "short bias or no trade; avoid weak altcoin longs." Strongest nominal names (ETH score 60.1, BTC score 57.4) are both still down on the day (-1.37%, -0.33%) — "strongest" here just means least-weak, not a long setup. Macro/geopolitical risk 89-91/100: Iran/Strait-of-Hormuz escalation (oil +10% weekly, Gulf states seeking debt financing for transit alternatives), externally corroborated pattern of BTC ETF outflows (record $4B June, brief early-July inflow recovery — Bloomberg, CoinDesk, §13). Single-name risk: Verus-Ethereum bridge exploited a second time in two months ($7.54M drained, carried); Robinhood CEO's X account hacked to promote a fake token (HOOD/USDT tagged, operator-review warning); Poolin (bitcoin mining pool) filed Chapter 11 bankruptcy. Both BTC/USDT and ETH/USDT short setups this cycle are explicitly capped to C for "short squeeze risk → no_derivatives_thin_short" — no clean short entry even in a risk-off tape, because Binance futures/derivatives data is unavailable for verification (54 symbol fetch failures).

**Stocks:** Market closes out its **closed** window in the next ~3 minutes (09:30 ET open). Regime: **risk_off / bias=short**, VIX 18.84 (calm relative to the 89-91/100 crypto-side geopolitical score — a real cross-asset divergence to watch at the open), breadth above EMA20 0.0%, all 4 major indices non-uptrend (SPY -1.67% 5d, QQQ -1.98% 5d). Strongest sectors: energy (XLE, RS +10.17% vs SPY), healthcare (XLV, +4.60%), financials (XLF, +3.25%). Weakest: semiconductors (SMH, -6.93%), consumer discretionary (XLY, -6.16%), technology (XLK, -3.19%). 15 raw-A setups (14 short + JPM long) all demoted to C purely for `market_closed_intraday_planning_only` — this is the operative pre-open watchlist. Two names carry additional, externally-verified caveats: MSFT (securities-fraud class action, real/ongoing, AVOID) and TSLA/GOOGL (`stale_post_earnings_setup` — both reported earnings within the last 48h, pre-earnings levels are explicitly invalid, fresh RTH levels required). Earnings context: GOOGL and LMT reported within the last 24h (Alphabet -7% on 2026 capex guidance of ~$200B per the report's own news feed); MSFT and META both have earnings in the coming days per the prior cycle's tracking.

### Market Mood / Risk Routing
- Crypto mood: **risk-off** (clean agreement across scalp/intraday/swing this cycle — BTC/ETH transition_down, 0% altcoin breadth, macro risk 89-91/100)
- Stocks mood: **pre-market / closed-into-open** (risk_off/bias=short regime read, VIX calm at 18.84 — a notable complacency-vs-crypto-risk divergence)
- Dominant narrative: Iran/Strait-of-Hormuz escalation (oil, Gulf debt financing, satellite images of a new Chinese sub) driving risk-off across both crypto and equities into the US open
- Preferred side now: **shorts (crypto: squeeze-capped, no clean entry; stocks: wait for RTH confirmation on the demoted-C short book)** — no chase, no forced trade
- Best long candidate: none clean in crypto this cycle; stocks — **JPM**, wait for RTH confirmation (financials RS strength, no legal flag, demoted only for market-closed)
- Best short candidate: none clean in crypto (BTC/ETH both squeeze-capped, no derivatives confirmation); stocks — **AMZN**, wait for RTH confirmation (highest clean score, no surviving legal/headline flag after verification)
- Best catalyst-backed candidate: **TSLA** — real, externally-confirmed Q2 earnings miss/crash, but requires fresh post-earnings levels before it's tradeable, not the stale pre-earnings ones in today's report
- What to avoid: **MSFT** (externally-confirmed active securities-fraud class action); chasing any crypto short into thin/unconfirmed derivatives data; treating pre-earnings TSLA/GOOGL levels as current
- What would change the view: a clean RTH confirmation (first 15-30min) on any of the demoted-C stocks setups; a de-escalation headline on Iran/Strait-of-Hormuz that eases the 89-91/100 macro score; Binance futures/derivatives data coming back online for BTC/ETH (would unlock a clean crypto short read)

## 7. Candidate Deep Dives

### 1. AMZN — short-watch (stocks, was A-tier 93.8, demoted to C for market-closed only)
- Has price already reacted to the catalyst? Unclear pre-open; no RTH confirmation yet.
- Is the setup chasing? Not assessable pre-open; today's levels are the pre-close/overnight read.
- Retest/pullback structure? Not evaluable until RTH prints.
- Overextended (>2 ATR from EMA20)? Not flagged in the report.
- Would entry now be late? N/A — market not yet open at run time.
- What level makes it actionable? First 15-30min RTH confirmation of the short thesis (price rejecting under yesterday's close with volume), consistent with the desk's own "prefer retest over chase" guidance for the open-reaction slot.
- Aligned with market mood? Yes — risk_off/bias=short regime, weak consumer-discretionary/tech RS.
- Long, short, or wait-for-trigger? Short, wait-for-RTH-confirmation.
- Actionable now or after confirmation? After confirmation only (market-closed gate).
- What would invalidate? A strong RTH open above yesterday's close, or the AWS-Bahrain situation escalating into a confirmed, material service disruption (would be a fresh, not-yet-existing catalyst).
- Chase-risk setup? Not yet assessable.
- Catalyst confirmation/contradiction? Two AMZN-tagged headlines this cycle: (1) "Wildberries — Russia's Amazon — Four Major Hubs Attacked" — **false symbol match**, this is a different company (Wildberries), not AMZN, confirmed by reading the headline text itself; (2) Iran-IRGC claimed cruise-missile strike on an AWS data center in Bahrain — externally confirmed to be a real claim (IBTimes, The Register, Tom's Hardware, Gizmodo, §13), but **AWS has not confirmed any damage/service impact** and Bahraini officials say the attack was intercepted; AWS dashboards show no change in service levels. Treat as geopolitical noise reinforcing the macro risk-off backdrop, not a confirmed AMZN-specific fundamental hit.
- **Legal/headline risk check (required for every stocks A/B):** no verified indictment, SEC/DOJ investigation, class action, or accounting issue found for AMZN specifically this cycle. Clean of legal flags.

### 2. MSFT — AVOID (stocks, was A-tier 94.26, highest raw score on the desk)
- Legal/headline risk check: **externally confirmed** — an active securities-fraud class action (City of St. Clair Shores Police and Fire Retirement System v. Microsoft, U.S. District Court, W.D. Washington, case no. 26-cv-02071) alleging misrepresentation of Azure/Copilot performance, tied to a January 28 2026 stock drop; lead-plaintiff deadline **August 11, 2026** (GlobeNewswire, PR Newswire, AccessWire — §13, multiple independent law-firm notices corroborate the same case).
- Final verdict: **AVOID / MANUAL REVIEW REQUIRED** — not a clean actionable even once the market opens, independent of the market-closed gate. Highest score on the desk but not tradeable without a human legal-risk sign-off.
- Would entry now be late? Moot — not tradeable regardless of timing.
- Catalyst confirmation/contradiction? The underlying stock-drop event (Jan 28 2026) is ~6 months old; the litigation itself is live and ongoing (fresh deadline in ~2.5 weeks) — the legal risk is current even though the originating event is not.

### 3. TSLA — catalyst-watch, post-earnings gap risk (stocks, was A-tier 92.71)
- Legal/headline risk check: internal tag is `going_concern` (which would normally force AVOID). **External search found no auditor going-concern opinion or formal warning for Tesla** — instead, multiple independent sources (Bloomberg, The Motley Fool, TradingKey — §13) confirm a real, fresh Q2 2026 earnings miss: non-GAAP EPS $0.33 vs ~$0.47 consensus, auto margins down to 16%, free cash flow **-$1.09B**, stock **-14.4% to -14.5%** on July 23. This is a genuine, externally-confirmed negative catalyst — just not a "going concern" one. TODO-3 (carried) flags the internal tag itself as likely mislabeled/overstated language from earnings-miss commentary, not an audit opinion.
- Has price already reacted? Yes, sharply — the 14.4% crash already happened July 23, one day before this review.
- Is the setup chasing? A short entered now would be chasing an already-realized move; the internal `stale_post_earnings_setup` cap correctly flags that pre-earnings levels (entry/stop/TP in today's report) are invalid — fresh RTH levels are required.
- Retest/pullback structure? Not yet assessable — needs the RTH open to establish a fresh reference level.
- What level makes it actionable? A confirmed RTH open + first 15-30min move establishing a fresh post-earnings range, not the stale pre-earnings levels.
- Aligned with market mood? Yes — risk_off, weak tech/consumer-discretionary RS, real negative catalyst.
- Long, short, or wait-for-trigger? Short-side bias if a fresh bearish continuation structure prints at the open; otherwise wait-for-trigger. Do not short the stale pre-earnings level.
- Chase-risk? High if using today's report's pre-earnings levels; moderate-to-low if waiting for genuinely fresh post-earnings structure.
- **Verdict: catalyst-watch, not AVOID** — downgrade the internal `going_concern` framing to "unconfirmed" per TODO-3, but treat the earnings-miss catalyst itself as real and material.

### 4. GOOGL — catalyst-watch, post-earnings (stocks, was A-tier 83.32)
- Legal/headline risk check: no indictment/DOJ/SEC/class-action found for GOOGL specifically this cycle (distinct from MSFT).
- Catalyst confirmation: internal report flags `stale_post_earnings_setup` — Alphabet reported earnings and guided 2026 capex to ~$200B, stock fell ~7% on July 23 per the report's own news feed ("Stock Market Today, July 23: Alphabet Slides 7% After Announcing 2026 Capex of Roughly $200 Billion"). Consistent, internally-sourced, not independently re-verified externally this cycle (WebSearch budget spent on TSLA/MSFT/AMZN/BTC-ETF items instead — acceptable per §G, internal record is recent/consistent/single-topic).
- Would entry now be late? Yes for the stale pre-earnings level; fresh RTH levels required, same logic as TSLA.
- Aligned with mood? Yes — capex-guidance-driven selloff fits the broader risk-off/tech-weakness picture.
- Long/short/wait? Short-bias watch, wait for fresh post-earnings RTH structure.
- Chase-risk? High on the stale level, moderate on a genuinely fresh retest.

### 5. JPM — long-watch (stocks, was A-tier 81.82, only clean long on the desk)
- Legal/headline risk check: clean, no flags found.
- Catalyst confirmation/contradiction? None specific to JPM beyond sector strength (financials RS +3.25% vs SPY, one of only 3 strong sectors) and an SEC 424B2 filing (routine, not a risk event).
- Has price already reacted? Not assessable pre-open.
- Is the setup chasing? Not yet assessable; report demotes it only for market-closed, no chase flag.
- What level makes it actionable? First 15-30min RTH confirmation of the long thesis with sector-relative strength intact.
- Aligned with market mood? Only long-side idea aligned with the regime's "bias=short" label is a sector-relative-strength exception (financials outperforming); treat as the desk's single counter-trend-but-RS-confirmed long candidate.
- Chase-risk? Not yet assessable.

## 8. Best Candidates Ranked

1. **JPM — long-watch** — trigger: RTH open + first 15-30min confirmation of financials-sector RS strength; no legal flag.
2. **AMZN — short-watch** — trigger: RTH open + first 15-30min confirmation of the short thesis under yesterday's close; no legal flag, AWS-Bahrain claim unconfirmed for material impact.
3. **TSLA — catalyst-watch (post-earnings)** — trigger: fresh RTH post-earnings range established, do not use today's stale pre-earnings levels; `going_concern` tag downgraded to unconfirmed (TODO-3).
4. **GOOGL — catalyst-watch (post-earnings)** — trigger: fresh RTH post-earnings range, same stale-level caveat as TSLA.
5. **MSFT — AVOID** — externally-confirmed active securities-fraud litigation; not tradeable at any point today without manual sign-off.

_Crypto: no candidate qualifies for this list this cycle — all three timeframes independently concluded "no trade," and both BTC/ETH short setups are squeeze-capped for missing derivatives confirmation. Best crypto watch remains: long-watch none clean (0% altcoin breadth); short-watch BTC/USDT or ETH/USDT only after Binance futures/derivatives data returns online (currently 54 symbol fetch failures) and a confirmed non-squeeze read; catalyst-watch HYPE/USDT (perps_dex_narrative basket) only once it re-enters a scored top-setups table._

## 9. Avoid / No Trade

This decision window only — never a command to stop the system.

- **Avoid MSFT** — externally-confirmed active securities-fraud class action, independent of the market-closed gate.
- **Avoid trading today's stale pre-earnings levels on TSLA and GOOGL** — both need fresh RTH-confirmed post-earnings structure first.
- **Avoid chasing any crypto short on BTC/USDT or ETH/USDT right now** — both are squeeze-capped due to missing derivatives/futures data (54 Binance symbol failures), not a clean technical short.
- **No new crypto scalp/intraday/swing A/B fires this window** — all three reports independently concluded "no trade."
- **Avoid treating the AWS-Bahrain headline as a confirmed AMZN fundamental hit** — the claim exists but AWS has not confirmed service impact; treat as geopolitical noise until independently verified.

## 10. Main Risks

- US cash open is ~3 minutes away at run time — every stocks level in this review is pre-open and requires RTH confirmation before being treated as current; do not act on today's stocks report levels without the first 15-30min confirmation.
- Macro/geopolitical risk (89-91/100) vs VIX (18.84) shows a real divergence — equity vol markets are not yet pricing the same risk-off intensity crypto/macro headlines suggest; a sudden VIX repricing at the open is a live risk.
- Crypto has zero clean directional setups on either side this cycle — both BTC/ETH shorts are squeeze-capped for missing derivatives data (54 Binance futures fetch failures); do not manufacture a short thesis from macro headlines alone without technical/derivatives confirmation.
- TSLA's `going_concern` tag remains internally re-fired but externally uncorroborated for multiple consecutive cycles (TODO-3) — a human session should trace the tag to its source record; in the meantime, do not treat TSLA as a going-concern AVOID, only as a real post-earnings catalyst-watch.
- Catalyst mapping remains weak (76.8% unmapped) — the catalyst/narrative layer is context, not confirmation, for any candidate above.
- LA/USDT swing remains the sole open crypto position (invalidation 0.0646, expires 07-31) — no fresh catalyst or contradiction this cycle, continue managing as-is.
- MEXC canary monitor shows repeated `RETRY_DB_BUSY` on its worker claim stage (132 occurrences) — heartbeat/reconcile both report OK, but this is a related symptom to the carried TODO-1 SQLite-contention pattern in a different subsystem; worth a root-cause check even though it hasn't caused an outright failure.

## 11. Action Plan — next 4 hours

- At/after the 09:30 ET open: check the first 15-30min RTH reaction on JPM (long), AMZN (short), TSLA and GOOGL (post-earnings shorts) before treating any as actionable — this is exactly the focus of the 18:30 EEST "US open reaction review" slot.
- Do not use today's stocks-intraday report's entry/stop/TP levels directly for TSLA or GOOGL — wait for a fresh post-earnings range to form.
- Continue treating MSFT as AVOID regardless of open-session price action.
- Manage the LA/USDT swing position (invalidation 0.0646, TP1 0.0722) — no action needed unless price breaks the invalidation level.
- Watch for Binance futures/derivatives data to come back online (currently 54 symbol fetch failures) — this is the blocker preventing any clean BTC/ETH short read despite the risk-off regime.
- Monitor for further Iran/Strait-of-Hormuz escalation or de-escalation headlines — this is the dominant driver of both the crypto and stocks risk-off read today.
- Continue scanning/tracking/monitors as normal — this review's caution stance does not pause any system component.

## 12. Final Verdict per Mode

- **Crypto scalp/intraday/swing:** NO NEW TRADE. All three reports independently conclude "no trade." One live position (LA/USDT swing) continues unmanaged-changed; one signal (RE/USDT) remains WAITING for entry.
- **Stocks intraday:** MARKET CLOSED at run time (opens in ~3min). 15 raw-A setups (14 short + JPM long) demoted to C for market-closed only — this is the pre-open watchlist for the 18:30 EEST open-reaction review. MSFT AVOID (legal). TSLA/GOOGL need fresh post-earnings levels.
- **Stocks swing/invest:** Deprecated/stale framework (~22 days), not used.
- **Overall desk posture:** WATCH-ONLY for new crypto ideas, WAIT-FOR-RTH-CONFIRMATION on the stocks pre-open watchlist. Not a system-wide no-trade — scanning and tracking continue.

## 13. Sources

- [Iran Claims Cruise Missile Strike On Amazon Data Infrastructure In Bahrain](https://www.ibtimes.com/iran-claims-amazon-data-center-attack-bahrain-3805541) (IBTimes, 2026-07-21 context)
- [Iran says it's struck offline AWS facility in Bahrain ... again](https://www.theregister.com/off-prem/2026/07/21/iran-says-its-struck-offline-aws-facility-in-bahrain-again/5275762) (The Register, 2026-07-21 — confirms AWS has not verified damage, Bahrain says intercepted)
- [Stock Market Today, July 23: Tesla Stock Crashes on Earnings Miss and Rising AI Spending](https://www.fool.com/coverage/stock-market-today/2026/07/23/stock-market-today-july-23-tesla-stock-crashes-on-earnings-miss-and-rising-ai-spending/) (The Motley Fool, 2026-07-23)
- [Tesla (TSLA) Fell 14% After Q2 - Margins Dropped, FCF Negative, Cybercab Under $30K](https://www.tradingkey.com/analysis/stocks/us-stocks/262052141-tesla-tsla-fell-14-percent-q2-2026-earnings-margin-cybercab-july-24-tradingkey) (TradingKey, 2026-07-24)
- [MSFT Court Alert: Microsoft Investors ... Securities Fraud Class Action ... Aug 11 Deadline](https://www.globenewswire.com/news-release/2026/07/22/3331195/0/en/msft-court-alert-microsoft-investors-seeking-to-recover-losses-in-securities-fraud-class-action-are-notified-to-contact-bfa-law-before-august-11-deadline.html) (GlobeNewswire, 2026-07-22)
- [Bitcoin (BTC) ETFs Face Record $4 Billion in June Outflows, Worst Since Launch](https://www.bloomberg.com/news/articles/2026-06-29/bitcoin-btc-etfs-face-record-4-billion-in-june-outflows-worst-since-launch) (Bloomberg, 2026-06-29)
- [Bitcoin ETFs draw in $221 million alongside renewed buying from long-term investors](https://www.coindesk.com/markets/2026/07/03/finally-usd221-million-flow-into-bitcoin-etfs-ending-a-painful-10-day-outflow-streak) (CoinDesk, 2026-07-03)
- Internal: `data/reports/scalp/2026-07-24_12-54_scalp_report.md`, `data/reports/intraday/2026-07-24_12-55_intraday_report.md`, `data/reports/swing/2026-07-24_13-26_swing_report.md`, `data/reports/stocks/intraday/2026-07-24_13-25_stocks_intraday_report.md`, `data/catalysts/2026-07-24/catalyst_cycle_12-58.md`, `data/catalysts/2026-07-24/catalyst_events.jsonl`
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-24_1140.md`

## 14. Fix Requests / TODO

### TODO-1 (carried): crypto/paper DB contention — new evidence in a different subsystem
- **issue:** Prior reviews tracked a `database is locked` pattern in `scheduler.log` (0 occurrences today, quiet). This cycle's `mexc_canary_monitor` log shows a related but distinct symptom: 132 occurrences of `RETRY_DB_BUSY` on the worker's `claim` stage, while heartbeat/reconcile both report OK.
- **evidence:** `data/scheduled_runs/2026-07-23_default_schedule/mexc_canary_monitor_1784823519.log` (grep count 132 for `RETRY_DB_BUSY`).
- **suggested manual fix:** confirm whether the mexc-canary worker's claim-stage retries are self-resolving (as they appear to be, given OK heartbeats) or masking a growing contention problem; check if WAL mode / retry-backoff tuning from the original TODO-1 investigation covers this subsystem too.
- **priority:** low-medium (no confirmed functional impact yet, but same root-cause family as the carried TODO-1).
- **first observed:** 2026-07-24 16:27 EEST (this review, new subsystem for an existing issue).

### TODO-2 (carried, unchanged): catalyst symbol resolver mapping weak
- **issue:** 76.8% of today's cumulative catalyst_events rows are unmapped (2242/2920 empty-symbol). Consistent with 76-79% across recent reviews.
- **evidence:** `data/catalysts/2026-07-24/catalyst_events.jsonl` — sample unmapped titles in §5.
- **suggested manual fix:** unchanged — extend resolver entity-matching; separately filter generic listicle headlines (Benzinga Movers "Top Performing X Stocks" style) so they don't inflate the weak-mapping percentage without representing a real resolver gap.
- **priority:** medium (persistent, degrades catalyst-backed decision quality; review already treats the layer as context-only).
- **first observed:** carried forward from prior reviews (news_layer_hardening project); still unresolved.

### TODO-3 (carried, re-fired): TSLA `going_concern` tag still not externally corroborated
- **issue:** Today's 13:25 EEST stocks-intraday report again gates TSLA to a legal/headline-risk cap of `going_concern`. External search this cycle (3 queries) found extensive, well-corroborated coverage of a real Q2 2026 earnings miss and 14.4% crash, but **no** formal auditor going-concern opinion or warning for Tesla anywhere in the results.
- **evidence:** `data/reports/stocks/intraday/2026-07-24_13-25_stocks_intraday_report.md` §5/§7 (TSLA, score 92.71, tier A→C, `legal_headline_risk: going_concern`); WebSearch "Tesla TSLA going concern warning July 2026" this cycle.
- **suggested manual fix:** a human session should trace the tag to its source record in the news/legal-risk pipeline and confirm whether it's a mislabeled classification of ordinary earnings-miss / negative-FCF commentary language, or a genuine but hard-to-find external opinion.
- **priority:** medium (now recurring across 3+ consecutive review cycles with no external corroboration each time).
- **first observed:** 2026-07-23 21:39 EEST; still open, re-confirmed firing today, third consecutive external-search miss.

### TODO-4 (new): news entity resolver produced a false symbol match on AMZN
- **issue:** A catalyst/risk headline about "Wildberries — Russia's Amazon — Four Major Hubs Attacked" was tagged to the AMZN symbol in this cycle's production risk warnings (§5c of the stocks-intraday and crypto reports). Wildberries is a distinct Russian e-commerce company, not Amazon.com (AMZN) — this is a false positive from matching the colloquial nickname "Russia's Amazon" rather than the actual company.
- **evidence:** `data/reports/stocks/intraday/2026-07-24_13-25_stocks_intraday_report.md` and `data/reports/intraday/2026-07-24_12-55_intraday_report.md`, §5c: "AMZN [geopolitical_risk]: risk_warning — Wildberries - Russia's Amazon - Has Seen Four Major Hubs Attacked...".
- **suggested manual fix:** a human session should add a nickname/alias exclusion rule (or tighten entity matching) so colloquial comparisons ("X's Amazon", "Y's Google") don't get tagged to the real company's symbol.
- **priority:** low-medium (risk-only/advisory effect today, but could falsely suppress a genuinely clean AMZN setup in a future cycle if the false flag were ever treated as a real legal/headline risk).
- **first observed:** 2026-07-24 16:27 EEST (this review).

### TODO-5 (carried, informational): XLE absent from stocks Top-Candidates/Rejected despite being the strongest sector
- **issue:** XLE (energy) remains the strongest sector by RS vs SPY (+10.17%) for multiple consecutive cycles, but still does not appear in either the Top-Candidates or Rejected/Not-Ready tables of the stocks-intraday report.
- **evidence:** `data/reports/stocks/intraday/2026-07-24_13-25_stocks_intraday_report.md` line 36 (sector strength) vs absence from §5/§8 tables.
- **suggested manual fix:** a human session should check whether XLE is excluded from the symbol universe or silently filtered by a gate — now directly relevant since the market is about to open.
- **priority:** low-medium (bumped from low — now actionable-relevant since the open is imminent, not purely informational).
- **first observed:** carried from prior reviews; unchanged in substance, priority bumped due to slot timing.
