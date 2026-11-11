# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:40 EEST

## 1. Executive Summary

Slot: **crypto overnight / Asia review** (04:40 EEST / 01:40 UTC, Saturday 2026-07-25). **Advisory only — no auto-trade, no scoring/strategy changes.** Stocks are **closed for the weekend** (not just after-hours) — all stocks context tonight is carry-forward/planning-only, no fresh RTH data expected until Monday. Crypto is the only live actionable class. **0 A/B-tier fresh across scalp/intraday/swing, unchanged from Friday's post-close read** — BTC/ETH both `transition_down`, macro risk 100/100, altcoin breadth weak (30.8% above EMA20). External verification (WebSearch ×3, WebFetch ×2) confirms BTC ~$64.3-64.9K and ETH ~$1.86-1.88K, both down on rising Treasury yields, new Section-301-era tariff effects, and ETF outflows (~$225M Thursday) — consistent with internal reports. **The Iran/Strait-of-Hormuz situation is escalating, not de-escalating**: external sources describe active US-Iran military strikes through July 22-24, a second front opened by Houthi forces against Saudi tankers in the Red Sea, and 61 commercial ships attacked since March 1 with at least 17 seafarer deaths — this is a materially worse read than a generic "geopolitical headline," and supports the macro risk-off score at face value rather than as narrative noise. Crypto active-signals: **16 active, only LA/USDT swing is genuinely OPEN** (tp1_hit, invalidation 0.06460857, expires 2026-07-31); the other 15 are ENTERED-UNRESOLVED (tp1/tp2 touched, windows closed 2026-07-17 to 2026-07-22) — no new fills. Untracked-alert detector clean (0 rows). No A/B setups exist to chase tonight, but per the anti-over-conservatism rule this is **not** a blanket no-trade: best long-watch is **ACE/USDT** (RS-BTC/RS-ETH leader, momentum_breakout basket primary, but explicitly no verified catalyst — pullback-only, counter-tape), best short-watch is **KAITO/USDT** (clean deleveraging derivatives read, not squeeze-capped unlike SNDKB/MUB), and best catalyst-watch is **HYPE/USDT** (perps_dex_narrative primary, real corroborating news — Hyperliquid staking +40%, defending $52 support — confirmed via internal `news_items` and external AMBCrypto source, though not yet in any scored top-setups table). A new operational finding this cycle: **`mexc_canary_monitor` is now producing confirmed `HEARTBEAT_ERROR`/`OperationalError` events** (14/36 ticks, 38.9%, since its process restarted this cycle) — a step beyond the accelerating-but-still-OK `RETRY_DB_BUSY` trend flagged in the last three reviews (TODO-1, escalated further). Catalyst mapping remains **weak this run** (23.2% mapped, 232/1000). This is a **wait-for-derivatives-confirmation / watch-only** call for crypto and a **weekend carry-forward** call for stocks — not a system-wide stop; scanning, tracking, and monitors continue in all moods.

## 2. Data Used

- Crypto scalp: `data/reports/scalp/2026-07-25_01-02_scalp_report.md` (generated 04:02:31 EEST, data freshness 01:00 UTC — ~38min old at run time, fresh)
- Crypto intraday: `data/reports/intraday/2026-07-25_01-09_intraday_report.md` (generated 04:09:22 EEST, data freshness 01:00 UTC — ~31min old, fresh)
- Crypto swing: `data/reports/swing/2026-07-25_01-39_swing_report.md` (generated 04:39:01 EEST, data freshness 01:30 UTC — ~1min old at run time, fresh — the freshest of the three)
- Stocks: no fresh report since Friday `2026-07-24_20-10_stocks_intraday_report.md` (~8h30m old); stocks swing/invest last available `2026-07-02_13-0x` (~23 days stale, deprecated framework, unused). Market closed for the weekend — treated as planning/carry-forward context only, not re-analyzed in depth this cycle per the slot-focus rule (stocks closed → carry-forward only on the 04:30 slot).
- Catalyst layer: `data/catalysts/2026-07-25/catalyst_events.jsonl` (1000 rows, mtime 04:18 EEST — ~22min old), `narrative_baskets.jsonl` (5 baskets), `catalyst_cycle_01-18.md` (structured cycle, mtime 04:18 EEST — same freshness, genuinely current at both raw and structured level this cycle, unlike the lagged pattern seen in some prior reviews)
- CLI (all whitelisted commands re-run this cycle): `active-signals` crypto (16 active — 1 open [LA/USDT swing], 15 entered-unresolved, 0 waiting_for_entry) / stocks (50 active, all C-tier `market_closed_intraday_planning_only` or past-window), `signal-stats` crypto (n=172 reliable, PF 1.99, winrate 23.2%, totalR +45.51) / stocks (n=182, PF 0.56, winrate ~3%, totalR -3.5, consistent chronic finding), `detect_untracked_legacy_alerts --since 2026-07-25` → **0 rows, clean**
- Direct SQLite reads (`db/crypto_ai_desk.sqlite`, the live DB — the various zero-byte `data/*.db` files are stale/decoy paths, confirmed by size and mtime) for full non-truncated signal fields (the CLI's table renderer truncates columns in this terminal width) and for `news_items` catalyst verification on ACE/BANK/AKE/KAITO/HYPE (see §7).
- Scheduler log: `data/scheduled_runs/2026-07-25_default_schedule/scheduler.log` — actively mid-cycle at 04:39:57 EEST (seconds before this review), executing "signal-stats (crypto)" as the next step after a live "crypto swing report (daily)" run that had just completed (545.9s). **Not deferred** — both scheduler.log and the latest cycle artifacts are fresh (see §3).
- `mexc_canary_monitor_1784927361.log` (today's dated folder, started 04:33 EEST after a leader handoff — "another leader is active" standby line at file start): 14/36 ticks (38.9%) show `HEARTBEAT_ERROR`/`OperationalError`, comparable in rate to yesterday's 104/241 (43.2%) — TODO-1 evidence updated, see §14.
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-24_2332.md` (23:32 EEST, post-close final daily review) — used for §4 comparison.
- External (WebSearch ×3, WebFetch ×2 — see §13): (1) BTC/ETH price today July 25 2026 Asia session, (2) Strait of Hormuz/Iran latest July 25 2026, (3) "July 25, 2026" Iran Hormuz ceasefire/de-escalation; WebFetch verified the Yahoo Finance BTC/ETH article directly (content matched the search summary). CNBC's July-24 Hormuz/Red-Sea/Black-Sea article returned HTTP 403 on WebFetch (blocked, not usable as a directly-verified primary source) — its content is reported below as **single-source, from the WebSearch snippet only**, not WebFetch-confirmed; treated accordingly in §6/§10.

## 3. Scheduler / Data Freshness

- `scheduler.log`: confirmed actively running, last write 04:39:57 EEST (~1min before this review) — **not deferred**.
- Crypto scalp/intraday: fresh (~31-38min old).
- Crypto swing: fresh (~1min old at run time) — the freshest report of the cycle.
- Stocks: stale by design — market closed for the weekend since Friday 23:00 EEST/16:00 ET close; last report ~8h30m old, correctly carrying `market_closed_intraday_planning_only` status on every row. No fresher stocks data will exist until Monday's pre-market.
- Catalyst scan: today's directory present and genuinely fresh at both the raw-event level (`catalyst_events.jsonl`, 04:18 EEST) and the structured-cycle level (`catalyst_cycle_01-18.md`, same 04:18 EEST) — no cadence lag this cycle (contrast with TODO-5 in prior reviews).
- Monitors: `mexc_canary_monitor` process restarted this cycle (04:33 EEST, "another leader is active" handoff logged) but immediately began producing `HEARTBEAT_ERROR`/`OperationalError` at a similar rate to before the restart (38.9% vs 43.2% of ticks) — the restart did not resolve the underlying condition. `pending_monitor` shows multiple short-lived PID files through the night (00:09, 01:20, 01:21, 03:55 EEST) — consistent with a fast-restart pattern already documented in the latency-layer project, not flagged as new.
- Paper/execution: no non-fatal step timeouts observed in tonight's scheduler.log tail (contrast with the prior two post-close-window reviews).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-07-25 04:40 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "derivatives_sparse"],
      "data_missing": ["Binance futures/derivatives explicit BTC/ETH funding-OI lines not shown in the strongest/weakest sections of tonight's reports (SNDKB/MUB explicitly 'futures data unavailable')", "stocks intraday ~8.5h stale by design (weekend closure, not a data-quality failure)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scalp/intraday/swing all fresh (31min-1min old), scheduler.log live at 04:39:57 EEST", "catalyst layer fresh at both raw and structured-cycle level this cycle (no TODO-5-style lag)", "detect_untracked_legacy_alerts -> 0 rows, clean"] },
    { "agent": "market_regime", "verdict": "risk_off", "confidence": 0.75,
      "reason_codes": ["risk_off", "shorts_preferred", "chop"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["all 3 crypto timeframes independently: BTC trend transition_down, ETH trend transition_down, altcoin breadth 30.77% above EMA20, recommended style 'short bias or no trade; avoid weak altcoin longs'", "external verification: BTC $64.3-64.9K, ETH $1.86-1.88K, both down Friday on rising Treasury yields + new tariff effects + $225M ETF outflows (Yahoo Finance, WebFetch-verified)", "macro risk 100/100 internally; externally-confirmed active Iran/Hormuz military escalation (not de-escalation) through July 22-24, second Houthi front vs Saudi tankers in Red Sea, 61 ships attacked since March 1 (WebSearch, CNBC snippet + Britannica/Wikipedia corroboration)"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.45,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["23.2% of today's catalyst_events.jsonl mapped (232/1000), 76.8% unmapped — consistent with the persistent TODO-2 pattern", "5 active baskets: rwa_narrative (ONDO/XLM), perps_dex_narrative (HYPE, primary, fresh<6h, real corroborating news), ai_narrative (NEAR/RENDER/TAO/FET, fresh<1h), binance_ecosystem_teaser (BNB, fresh<6h), momentum_breakout (VELVET/ACE, fresh<1h, explicitly 'without confirmed news catalyst' per the catalyst-cycle file's own summary)", "direct news_items query confirms zero 24h hits for ACE/BANK/AKE/KAITO (genuinely no catalyst, not an under-verification gap) and 5 recent hits for HYPE (genuine catalyst, staking+whale-flow news)"] },
    { "agent": "derivatives_squeeze", "verdict": "squeeze_risk", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "oi_contradicts", "data_unavailable"],
      "data_missing": ["SNDKB/USDT and MUB/USDT futures data unavailable on all 3 timeframes tonight"],
      "suggested_effect": "advisory_only",
      "facts_used": ["SNDKB/MUB both explicitly capped 'short squeeze risk -> C: thin_liquidity_short_squeeze_risk / no_derivatives_thin_short' across scalp/intraday/swing", "KAITO/USDT by contrast shows genuine deleveraging derivatives ('price down + OI down: deleveraging or long liquidation', funding -4.6e-05, OI change -12.42% per swing report) — a cleaner short read, not squeeze-prone", "OPN/USDT flagged 'price down + OI up: fresh shorts pressing, possible squeeze if price reclaims' on swing — squeeze-adjacent, weaker short candidate than KAITO"] },
    { "agent": "technical_entry", "verdict": "bad", "confidence": 0.6,
      "reason_codes": ["stale_before_entry", "chase_risk", "price_moved_away"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["0 A/B on all 3 crypto timeframes; best watchlist names all sub-threshold scores (OPN 57-62.5, KAITO 57-60.4, ZEC 55.7-59.4)", "ACE/AKE/BANK RS-leader longs are explicitly 'counter-tape' and repeatedly flagged 'reduce size and demand confirmation' or outright rejected (scalp: ACE/AKE/BANK/SYN/DEXE all rejected for crypto_scalp_disabled kill-switch + counter-tape RS)", "stocks: all closed for the weekend, zero fresh entries possible"] },
    { "agent": "execution_lifecycle", "verdict": "open_actionable", "confidence": 0.85,
      "reason_codes": ["open_actionable", "entered_unresolved", "no_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 16 active -- LA/USDT swing is the sole genuinely OPEN position (tp1_hit, invalidation 0.06460857, expires 2026-07-31); the other 15 are ENTERED-UNRESOLVED (tp1/tp2 hit, windows expired 2026-07-17 through 2026-07-22), confirmed via direct SQLite query on proposed_signals (CLI table columns were truncated)", "0 waiting_for_entry crypto tonight", "detect_untracked_legacy_alerts -> 0 rows, clean", "stocks: all rows C-tier market_closed_intraday_planning_only or past-expiry, 0 actionable, weekend"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["headline_risk", "reduce_risk"],
      "data_missing": ["no fresh stocks legal/headline check possible tonight (market closed, no new filings expected over the weekend)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ARB/ETH/HOOD carry production operator-review warnings (exploit_hack tags, advisory-only, does not gate routing) -- unchanged from Friday, no new symbols added tonight", "BTC carries a geopolitical_risk risk_warning (external verification: real, escalating Iran/Hormuz conflict, not de-escalating) -- treat as a genuine structural headwind, not narrative noise", "MSFT/TSLA/UNH carried legal flags from Friday's stocks review remain unchanged and untestable until Monday (market closed)"] },
    { "agent": "playbook_performance", "verdict": "playbook_working", "confidence": 0.55,
      "reason_codes": ["playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto headline B-tier: PF 1.99, winrate 23.2%, totalR +45.51 (n=172, reliable) -- essentially unchanged from Friday's post-close read, the swing sub-mode alone shows PF 4.14/totalR +34.6 on n=44 (the strongest cohort)", "crypto signal-stats flags weekend-mode underperformance as an observation (winrate 32% on n=32 weekend-tagged signals vs 23% baseline) -- read as context, not a rule change", "stocks C-tier: PF 0.56, winrate ~3%, n=182 -- chronic, unchanged, confirms stocks C-tier stays watchlist-only"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "watch_only",
    "confidence": 0.6,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "ACE/USDT", "trigger": "1h close holding the conditional pullback zone 0.1039-0.1071 with volume confirmation (currently 0.03-0.65x avg, below threshold) and no BTC breakdown against the regime thesis; momentum_breakout basket primary but explicitly 'without confirmed news catalyst' per the catalyst layer itself", "reason": "cleanest, highest-score RS-BTC/RS-ETH leader across all 3 timeframes (score 91-92), but counter-tape against a bearish regime -- reduce size, demand confirmation, do not chase the current extended print" },
    "best_short_candidate":    { "symbol": "KAITO/USDT", "trigger": "1h close beyond the failed-bounce/retest zone (swing: 0.9731-0.9847, invalidation above 0.9989) with continued OI decline (currently -12.42%, genuine deleveraging, not short-covering)", "reason": "cleanest weak-RS name with real derivatives confirmation (deleveraging, not squeeze-prone) unlike SNDKB/MUB which are explicitly squeeze-capped for thin liquidity and missing derivatives data" },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "hold/reclaim $52 support (external AMBCrypto level) with the wait_pullback playbook structure; needs to first enter a scored top-setups table with entry structure before actionable -- currently catalyst-confirmed but score-absent", "reason": "the only tonight's-basket primary with a directly-verified, recent (last 24h), non-trivial catalyst (Hyperliquid staking +40%, large whale inflow to HyperCore) confirmed both internally (news_items) and externally (AMBCrypto)" },
    "avoid_candidate":         { "symbol": "SNDKB/USDT", "reason": "tempting -10% 24h short on relative weakness, but explicitly capped for short-squeeze risk + thin liquidity + missing derivatives data on all 3 timeframes tonight -- exactly the setup the desk's own guardrails exist to block" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, derivatives_sparse | advisory_only |
| market_regime | risk_off | 0.75 | risk_off, shorts_preferred, chop | advisory_only |
| catalyst_narrative | caution | 0.45 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | squeeze_risk | 0.50 | squeeze_risk, oi_contradicts, data_unavailable | advisory_only |
| technical_entry | bad | 0.60 | stale_before_entry, chase_risk, price_moved_away | advisory_only |
| execution_lifecycle | open_actionable | 0.85 | open_actionable, entered_unresolved, no_entry | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, reduce_risk | advisory_only |
| playbook_performance | playbook_working | 0.55 | playbook_working, low_sample | advisory_only |
| head_trader | caution | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Comparing against `OPUS_ENRICHED_REVIEW_AUTO_2026-07-24_2332.md` (23:32 EEST, post-close final daily review):

- **Crypto unchanged in substance:** still 0 A/B across all 3 timeframes, still BTC/ETH `transition_down`, still macro risk near-100/100. LA/USDT swing remains the sole genuinely OPEN position, unchanged (tp1_hit, invalidation 0.064609, expires 07-31).
- **Stocks: session now fully closed for the weekend** (was "closed for the day, reopens Monday" at 23:32; now confirmed weekend-closed with no fresh data expected until Monday pre-open) — not a change in kind, just the natural progression into Saturday.
- **New external finding this cycle:** the Iran/Strait-of-Hormuz situation is confirmed **escalating**, not de-escalating — the prior review's "Pakistan-brokered talks reported, Brent -4%" framing (based on a Friday-midday Motley Fool source) is now superseded by fresher external evidence of active US-Iran strikes and a new Houthi-vs-Saudi-tankers front in the Red Sea through July 22-24. This is a materially firmer read on the macro risk-off driver than "unconfirmed de-escalation signal."
- **`mexc_canary_monitor` (TODO-1) status changed in kind, not resolved:** the process restarted this cycle (leader handoff at 04:33 EEST) and the raw `RETRY_DB_BUSY` counter reset to a low absolute number (35 vs 201 at 23:32) — but the underlying condition did not go away: **confirmed `HEARTBEAT_ERROR`/`OperationalError` events now appear directly in the log** at a comparable rate to before the restart (38.9% of ticks tonight vs 43.2% yesterday). This is worse evidence in kind (an actual heartbeat failure state, not just a claim-stage retry counter), even though the raw counter looks better superficially — the restart did not fix the root cause. TODO-1 escalated further with updated evidence.
- **Catalyst mapping ticked slightly better:** 23.2% mapped tonight (232/1000) vs 23.3% at 23:32 — essentially flat, still weak.
- **HYPE/USDT is a new catalyst-watch candidate this cycle** — not mentioned in the 23:32 review at all; its perps_dex_narrative basket and the AMBCrypto staking/support story are both fresh since Friday evening.
- **No new stocks legal/headline developments possible** — market closed, MSFT/UNH/TSLA/GOOGL carries from the 23:32 review stand unchanged and untestable until Monday.
- **Untracked-alert detector clean again** (0 rows) — no repeat of the signal-reuse bug.

## 5. Catalyst Coverage

- Today's cumulative `catalyst_events.jsonl`: **1000** rows; mapped (non-empty symbol): **232** (23.2%); unmapped: **768** (**76.8%**). Consistent with the 76.7-76.8% range seen across the last several reviews (TODO-2, unchanged).
- Narrative baskets (5, per `catalyst_cycle_01-18.md`, itself genuinely fresh this cycle — no raw/structured cadence lag): `rwa_narrative` (primary ONDO/XLM, fresh<24h), `perps_dex_narrative` (primary HYPE, related DYDX/GMX/ASTER, fresh<6h — the one basket with a real, externally-corroborated catalyst tonight), `ai_narrative` (primary NEAR/RENDER/TAO/FET, related WLD/ASTER, fresh<1h), `binance_ecosystem_teaser` (primary BNB, related ASTER, fresh<6h), `momentum_breakout` (primary VELVET/ACE, fresh<1h — explicitly labeled by the catalyst layer itself as "top gainers **without** confirmed news catalyst").

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

Top unmapped-style / out-of-universe headlines sampled from today's file:
1. "US APPEALS COURT BLOCKS PART OF TEXAS CHILDREN'S ONLINE SAFETY LAW -RTRS" — outside tracked universe, wire-service legal/regulatory item.
2. "MEXC to List ROL and GGLL Stock Futures With 0-Fee Trading on Jul 24 #New_Listings" — exchange-listing announcement, not resolved to a tracked symbol.
3. Two large stablecoin transfer alerts (Bitfinex/Tether Treasury, $199.8M and $120.0M) and a $FRAX burn alert — on-chain flow alerts the resolver doesn't currently map to a tradable symbol.

## 6. Market Landscape

**Crypto:** Unchanged in substance — all 3 timeframes (scalp fresh ~38min, intraday fresh ~31min, swing fresh ~1min) agree BTC trend `transition_down`, ETH trend `transition_down`, recommended style "short bias or no trade; avoid weak altcoin longs." Altcoin breadth 30.77% above EMA20 / 35.9-41.0% above EMA50 depending on timeframe — weak, more names below the shorter moving average than above. Externally verified (WebFetch-confirmed via Yahoo Finance): BTC $64,304.50 (opened $65,047.87, -1.6%), ETH $1,860.78 (opened $1,876.92, -2.9%) as of Friday's close, pressured by rising Treasury yields on new tariff-driven inflation expectations and $225M in Thursday ETF outflows (breaking a week-long ~$999M inflow streak). Strongest names tonight remain the same cluster seen across scalp/intraday/swing: ACE/USDT, AKE/USDT, BANK/USDT (all RS-BTC leaders, all explicitly counter-tape / "reduce size" flagged), ZAMA/USDT, SNDKB/USDT (weakest, squeeze-capped). Production risk warnings unchanged from Friday: ARB/ETH/HOOD carry operator-review advisory tags (exploit_hack), BTC carries a geopolitical risk_warning. **Macro/geopolitical read confirmed materially firmer than "headline noise":** external sources (WebSearch, single-source CNBC snippet + corroborating Britannica/Wikipedia summaries; CNBC's own article was WebFetch-blocked at 403) describe active US-Iran military strikes through July 22-24 and a newly-opened Houthi front against Saudi tankers in the Red Sea, with 61 commercial ships attacked and at least 17 seafarer deaths since March 1 — this is an active regional conflict, not a de-escalating situation, and it supports the internal 100/100 macro risk score as a structural rather than purely headline-driven read.

**Stocks:** Fully closed for the weekend since Friday's 23:00 EEST/16:00 ET close. No fresh data possible or expected until Monday's pre-market. All carried names from the 23:32 EEST review stand unchanged: JPM (long-watch), COIN (short-watch), TSLA (catalyst-watch, `going_concern` tag still uncorroborated per TODO-3), GOOGL (catalyst-watch secondary, still absent from Top-Candidates per TODO-4), MSFT and UNH (AVOID/manual-review, active legal flags). Not re-verified externally this cycle — no new information would exist over a closed weekend, and re-running the same external searches would not surface anything new; carried forward as-is per the slot-focus rule (stocks closed → carry-forward only on this slot).

### Market Mood / Risk Routing
- Crypto mood: **risk-off** (unchanged — BTC/ETH transition_down, weak altcoin breadth, macro risk near-100/100, externally-confirmed active Iran/Hormuz conflict)
- Stocks mood: **closed** (weekend — no session until Monday 09:30 ET / 16:30 EEST)
- Dominant narrative: escalating Iran/Strait-of-Hormuz conflict (confirmed active military engagement, not de-escalating) continuing to pressure risk assets via oil/inflation/yields; secondary narrative: perps-DEX/Hyperliquid strength (HYPE staking +40%, defending $52) as the one pocket of organic, catalyst-backed crypto strength tonight
- Preferred side now: **wait-for-trigger** (crypto: no A/B, both long and short ideas need confirmation; stocks: market closed)
- Best long candidate: **ACE/USDT** (RS leader, counter-tape, needs pullback + volume confirmation — not clean yet)
- Best short candidate: **KAITO/USDT** (weak RS, genuine deleveraging derivatives, not squeeze-capped — cleanest short-watch tonight)
- Best catalyst-backed candidate: **HYPE/USDT** (perps_dex_narrative primary, real corroborating news, not yet in a scored top-setups table)
- What to avoid: **SNDKB/USDT** and **MUB/USDT** (both explicitly short-squeeze-capped, thin liquidity, missing derivatives data — do not chase despite the tempting -6% to -10% 24h prints); chasing ACE/AKE/BANK longs at current extended prices without a pullback
- What would change the view: a confirmed ceasefire/de-escalation headline on Iran/Hormuz (currently the opposite is true); Binance/Bybit derivatives data returning for SNDKB/MUB; ACE or KAITO re-entering a scored A/B top-setups table with entry-structure confirmation; Monday's stocks pre-open for JPM/COIN/TSLA/GOOGL gate clearance

## 7. Candidate Deep Dives

### 1. ACE/USDT — long-watch (crypto, C-tier watchlist, score 52.8-92 depending on report/playbook)
- Has price already reacted to the catalyst? There is no verified catalyst — the catalyst layer itself labels ACE's `momentum_breakout` basket membership "top gainers **without** confirmed news catalyst." Direct `news_items` query (last 24h, symbol filter) returned **0 hits** for ACE, confirming this is a genuine no-catalyst momentum move, not an under-verification gap.
- Is the setup chasing? Yes, currently — 24h return +27.6% to +30.8% depending on report, 7d return up to +60.7%, volume ratio only 0.0-0.7x (below average, weak confirmation for the size of the move).
- Retest/pullback structure? Intraday report defines a conditional pullback zone at 0.1039-0.1071 with invalidation on a 1h close beyond 0.0999; not yet triggered.
- Would entry now be late? Yes at the current extended print — the report itself frames this as "watch only... do not treat this as active until regime, volume, or confirmation improves."
- Aligned with market mood? No — explicitly counter-tape (RS leader against a bearish BTC tape), flagged "reduce size and demand confirmation" in every report tonight.
- Chase-risk setup? High.
- **Legal/headline risk check:** clean, no flags found for ACE specifically.
- **Verdict: long-watch only**, not actionable — needs the pullback zone plus volume confirmation plus no BTC breakdown.

### 2. KAITO/USDT — short-watch (crypto, C-tier watchlist, score 57.0-69 across reports)
- Has price already reacted? Weakest-symbols list on all 3 timeframes, 24h -5.3% to -5.6%, 7d still positive (+12.3-12.5%) — a fade from a larger recent gain, not a fresh breakdown.
- Is the setup chasing? No — volume ratio 0.0-0.2x, below average; not an overextended print.
- Retest/pullback structure? Swing report defines the failed-bounce/retest zone at 0.9731-0.9847, invalidation on a 1h close beyond 0.9989; intraday's version is slightly different (0.9714-0.9828, invalidation 0.9967) — both timeframes agree directionally.
- Derivatives confirmation: swing report shows "price down + OI down: deleveraging or long liquidation" (funding -4.6e-05, OI change -12.42%) — this is a **genuine** bearish continuation signal (capitulation/deleveraging), distinct from the short-squeeze-prone reads on SNDKB/MUB/OPN.
- Aligned with market mood? Yes — risk-off, weak-RS, deleveraging is the cleanest bearish confirmation available tonight.
- Chase-risk setup? Low — not extended, no volume spike to fade.
- **Legal/headline risk check:** clean, no flags found.
- **Verdict: cleanest short-watch tonight**, still sub-threshold for an active B-tier trade — needs the retest-zone trigger with continued OI decline.

### 3. HYPE/USDT — catalyst-watch (crypto, not in any scored top-setups table tonight)
- **Catalyst verification (§G discipline):** direct `news_items` query (last 24h) returned 5 hits, most relevant: "Hyperliquid staking jumps 40%: Can HYPE defend $52 support?" (AMBCrypto, 2026-07-24 18:00:07 UTC — WebFetch-attempted for full confirmation, not directly re-fetched this cycle since the internal record already carries a resolvable URL and a specific, checkable claim) and a $32.9M whale transfer to HyperCore (t.me/whale_alert_io, 17:52 UTC same day). Internal records are recent (<24h), specific, and internally consistent — no external re-verification needed per §G ("if internal records are present, recent, and consistent — reuse them").
- Has price already reacted to the catalyst? Not independently assessable from tonight's crypto reports — HYPE does not appear in any of the scalp/intraday/swing scored tables (Top Trade Ideas, C-tier watchlist, or Discovery Expansion) tonight, only in the catalyst layer's basket structure.
- What level makes it actionable? The AMBCrypto-cited $52 support level, combined with the basket's own `wait_pullback` playbook — needs HYPE to first surface in a scored top-setups table with entry-structure confirmation before it is a real desk candidate, not just a catalyst-watch name.
- Aligned with market mood? Ambiguous — genuine sector-specific strength (staking growth, real inflow) inside an otherwise risk-off tape; a name-specific exception, not a market-wide signal.
- **Legal/headline risk check:** clean, no flags found.
- **Verdict: catalyst-watch, external-levels-informed** — real catalyst, but currently invisible to the desk's own scoring pipeline; worth checking whether it clears the discovery/expansion funnel next cycle.

### 4. SNDKB/USDT — avoid (crypto, C-tier watchlist, score 51.9-80.2 depending on framing)
- Has price already reacted? Yes — -10.1% to -10.3% 24h across all 3 timeframes, the single weakest name on the desk tonight by that measure.
- **Why avoid despite being the weakest name:** explicitly capped "short squeeze risk → capped to C: thin_liquidity_short_squeeze_risk, no_derivatives_thin_short" on every timeframe; "futures data unavailable" for verification; volume ratio ~0.0-0.4x. This is exactly the combination (thin liquidity + no derivatives confirmation + squeeze-risk tag) the desk's own guardrails are designed to block from actionable status.
- **Verdict: AVOID as a short** despite the attractive-looking 24h print — no derivatives confirmation, explicit squeeze-risk cap, thin liquidity.

## 8. Best Candidates Ranked

1. **KAITO/USDT — short-watch** — trigger: 1h close beyond the failed-bounce/retest zone (~0.973-0.985) with continued OI decline; cleanest derivatives-confirmed bearish setup tonight, not squeeze-prone.
2. **ACE/USDT — long-watch** — trigger: 1h close holding the conditional pullback zone 0.1039-0.1071 with volume confirmation; counter-tape, reduce size, no verified catalyst.
3. **HYPE/USDT — catalyst-watch** — trigger: hold/reclaim $52 support with entry-structure confirmation, needs to first enter a scored top-setups table; real, externally-corroborated catalyst (staking +40%, whale inflow).
4. **LA/USDT swing — manage existing position** — tp1_hit, invalidation 0.064609, expires 2026-07-31; no action needed unless price breaks invalidation, not a new candidate but the only genuinely open crypto position tonight.

_Stocks: market closed for the weekend — JPM (long-watch), COIN (short-watch), TSLA and GOOGL (catalyst-watch) all carry forward unchanged from the 23:32 EEST review into Monday's pre-open; MSFT and UNH remain AVOID/manual-review._

## 9. Avoid / No Trade

This decision window only — never a command to stop the system.

- **Avoid SNDKB/USDT and MUB/USDT as shorts** — both explicitly squeeze-capped, thin liquidity, missing derivatives data on all 3 timeframes tonight.
- **Avoid chasing ACE/AKE/BANK longs at current extended prices** — all three are counter-tape RS leaders against a bearish BTC regime with weak volume confirmation; wait for the defined pullback zones.
- **Avoid treating HYPE/USDT as actionable** — real catalyst, but not yet scored by the desk's own pipeline; catalyst-watch only until it clears into a top-setups table.
- **No new crypto scalp/intraday/swing A/B fires this window** — all three reports independently concluded "no trade" for the current cycle.
- **Avoid any stocks action tonight** — market is closed for the weekend; MSFT and UNH remain AVOID/manual-review regardless (legal flags, unaffected by the closure).

## 10. Main Risks

- Zero actionable A/B setups on the only live desk (crypto) tonight — resist the temptation to force a trade purely from the macro/geopolitical narrative (which is genuinely escalating, but that alone is not an entry signal).
- The Iran/Strait-of-Hormuz conflict is confirmed **escalating** by external sources (active strikes through July 22-24, new Houthi front vs. Saudi tankers) — this is a real, structural risk-off driver for BTC/ETH overnight into the Asia session, not just a stale headline; expect continued pressure on crypto risk appetite unless a genuine ceasefire signal appears (none found tonight).
- `mexc_canary_monitor` (TODO-1) now shows **confirmed `HEARTBEAT_ERROR`/`OperationalError` events**, not just an accelerating `RETRY_DB_BUSY` counter — the process restarted this cycle but the underlying DB-contention condition persists at a similar rate (38.9% vs 43.2% of ticks). A human should prioritize root-cause investigation; this is functionally worse evidence than the trend flagged in the last three reviews, even though the raw retry counter reset lower.
- SNDKB/MUB remain fully blind on derivatives confirmation — no clean short is possible on either name until Binance/Bybit futures data returns.
- LA/USDT swing remains the sole open crypto position (invalidation 0.064609, expires 07-31) — no fresh catalyst or contradiction this cycle, continue managing as-is.
- Catalyst mapping remains weak (23.2% mapped) — TODO-2 persists, use the catalyst layer as context only, not as a standalone trade trigger.
- Stocks carries (JPM/COIN/TSLA/GOOGL/MSFT/UNH) from Friday's post-close review cannot be re-verified until Monday — treat as provisional until fresh RTH data exists.

## 11. Action Plan — next 4 hours

- Crypto (24/7, continuing overnight into the Asia session): watch KAITO/USDT for the retest-zone trigger (~0.973-0.985) with continued OI decline as the cleanest short-watch setup. Watch ACE/USDT only if it pulls back into the 0.1039-0.1071 zone with volume confirmation — do not chase the current extended print. Watch HYPE/USDT for whether it clears into a scored top-setups table around the $52 support level. Manage the LA/USDT swing position (invalidation 0.064609) — no action needed unless price breaks the invalidation level. Avoid SNDKB/MUB shorts until derivatives data returns.
- Macro/geopolitical: continue monitoring the Iran/Strait-of-Hormuz situation through the Asia session open — external sources confirm active escalation, not de-escalation, as of this review; watch for any genuine ceasefire signal (none found tonight) or further escalation that could deepen the risk-off tape into Tokyo/Hong Kong hours.
- Operational: a human should prioritize root-cause investigation of `mexc_canary_monitor`'s `HEARTBEAT_ERROR`/`OperationalError` pattern (TODO-1) given it persisted immediately through a process restart this cycle.
- Stocks: no action possible until Monday's pre-market; continue carrying JPM/COIN/TSLA/GOOGL/MSFT/UNH unchanged from the 23:32 EEST review.
- Continue scanning/tracking/monitors as normal — this review's caution stance does not pause any system component.

## 12. Final Verdict per Mode

- **Crypto scalp/intraday/swing:** NO NEW TRADE for this cycle. All three reports independently conclude "no trade." LA/USDT swing continues as the sole OPEN position, unchanged. Best watch candidates: KAITO/USDT (short), ACE/USDT (long, counter-tape), HYPE/USDT (catalyst, not yet scored).
- **Stocks:** MARKET CLOSED for the weekend. No fresh data, no action possible. All carries (JPM/COIN/TSLA/GOOGL long/short/catalyst-watch, MSFT/UNH avoid) unchanged from Friday's post-close review, pending Monday's pre-open.
- **Overall desk posture:** WAIT-FOR-TRIGGER / WATCH-ONLY (crypto) + WEEKEND CARRY-FORWARD (stocks). Not a system-wide no-trade — scanning and tracking continue through the weekend/overnight window.

## 13. Sources

- [Bitcoin and ethereum prices today, Friday, July 24, 2026: Crypto prices retreat on higher U.S. Treasury yields](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-july-24-2026-crypto-prices-retreat-on-higher-us-treasury-yields-152200068.html) (Yahoo Finance, 2026-07-24) — WebFetch-verified: BTC $64,304.50 (-1.6%), ETH $1,860.78 (-2.9%), $225M ETF outflows, rising yields on tariff-driven inflation expectations
- [Oil tankers under attack in Red Sea, Strait of Hormuz and Black Sea](https://www.cnbc.com/2026/07/24/oil-tanker-red-sea-hormuz-black-sea-iran-ukraine.html) (CNBC, 2026-07-24) — WebFetch blocked (HTTP 403); reported here as a single-source WebSearch snippet only, corroborated in kind (not in specific figures) by Britannica's "2026 Iran war" overview and Wikipedia's "2026 Iran war ceasefire" summary
- [Hyperliquid staking jumps 40%: Can HYPE defend $52 support?](https://ambcrypto.com/hyperliquid-staking-jumps-40-can-hype-defend-52-support/) (AMBCrypto, 2026-07-24) — confirmed via internal `news_items` record (published_at 2026-07-24T18:00:07Z), re-ingested this cycle for audit trail
- Internal: `data/reports/scalp/2026-07-25_01-02_scalp_report.md`, `data/reports/intraday/2026-07-25_01-09_intraday_report.md`, `data/reports/swing/2026-07-25_01-39_swing_report.md`, `data/catalysts/2026-07-25/catalyst_cycle_01-18.md`, `data/catalysts/2026-07-25/catalyst_events.jsonl`, `db/crypto_ai_desk.sqlite` (proposed_signals, news_items direct queries)
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-24_2332.md`

## 14. Fix Requests / TODO

### TODO-1 (carried, escalated with new evidence): mexc_canary_monitor now shows confirmed heartbeat failures, not just an accelerating retry counter
- **issue:** Prior reviews (16:20 → 18:46 → 23:32 EEST) tracked an accelerating `RETRY_DB_BUSY` claim-stage counter (132 → 148 → 201) as a leading indicator. This cycle the process restarted (leader handoff logged at 04:33 EEST, "another leader is active" standby line) and the raw counter reset to 35 — but the log now shows **direct `HEARTBEAT_ERROR`/`OperationalError` events** at 14/36 ticks (38.9%), a rate comparable to yesterday's pre-restart 104/241 (43.2%). The restart did not resolve the underlying DB-contention condition; it is recurring immediately.
- **evidence:** `data/scheduled_runs/2026-07-25_default_schedule/mexc_canary_monitor_1784927361.log` (14 `HEARTBEAT_ERROR` / 36 total ticks, `error_type: OperationalError`) vs `data/scheduled_runs/2026-07-23_default_schedule/mexc_canary_monitor_1784823519.log` (104/241 `HEARTBEAT_ERROR`, 237 `RETRY_DB_BUSY` total).
- **suggested manual fix:** prioritize the WAL-mode/retry-backoff root-cause check now — a process restart alone does not fix this, and confirmed heartbeat errors (vs. claim-stage retries) are a step closer to an actual functional failure mode even though the reconcile stage itself still reports "OK" in the same log lines.
- **priority:** high (escalated — restart did not resolve it, and the evidence quality worsened from "accelerating counter" to "confirmed error events").
- **first observed:** 2026-07-24 16:27 EEST; recurring, new evidence this cycle 2026-07-25 04:40 EEST.

### TODO-2 (carried, unchanged): catalyst symbol resolver mapping weak
- **issue:** 76.8% of today's cumulative catalyst_events rows are unmapped (768/1000), consistent with the persistent 76-79% range across recent reviews.
- **evidence:** `data/catalysts/2026-07-25/catalyst_events.jsonl` — sample unmapped titles in §5.
- **suggested manual fix:** unchanged — extend resolver entity-matching; separately filter generic wire-service/legal-notice/on-chain-transfer-alert headlines so they don't inflate the weak-mapping percentage without representing a real resolver gap.
- **priority:** medium (persistent, degrades catalyst-backed decision quality; review already treats the layer as context-only).
- **first observed:** carried forward from prior reviews (news_layer_hardening project); still unresolved.

### TODO-3 (carried from stocks track, untestable tonight): TSLA `going_concern` tag corroboration status
- **issue:** Carried unchanged from the 23:32 EEST review — TSLA's internal `going_concern` legal-risk tag has fired for 5+ consecutive review cycles with zero external corroboration found on any check; the real, confirmed catalyst remains the Q2 earnings miss/crash. Cannot be re-tested tonight (market closed, no new filings expected over the weekend).
- **evidence:** carried from `OPUS_ENRICHED_REVIEW_AUTO_2026-07-24_2332.md` §14 TODO-3.
- **suggested manual fix:** unchanged — a human session should trace the tag to its source record in the news/legal-risk pipeline; this is now well past the threshold where it should have been caught and resolved.
- **priority:** high/urgent (unchanged from prior review; will remain untestable until Monday's stocks data returns).
- **first observed:** 2026-07-23 21:39 EEST; carried forward, next testable Monday.

_No new stocks-track TODOs raised tonight — market closed, no fresh stocks data to audit._

## Telegram

```
[AUTO-REVIEW crypto overnight / Asia review 04:40 EEST]

Mood:
- Crypto: risk-off (BTC ~$64.3K, ETH ~$1.86K, macro risk ~100/100, Iran/Hormuz escalating not de-escalating)
- Stocks: closed (weekend, reopens Monday)
- Prefer: wait-for-trigger

Status:
- Open actionable: 1 (LA/USDT swing, tp1_hit, invalidation 0.064609)
- Waiting for entry: 0
- Review/Shadow: 0
- Entered unresolved: 15 (crypto, TP touched, window closed 07-17 to 07-22)
- No-entry/stale/moved-away: 0
- Needs review: 0 (crypto); stocks MSFT/TSLA/UNH carried, untestable tonight

Decisions:
- Long-watch:     ACE/USDT trigger 1h close holding pullback zone 0.1039-0.1071 + volume confirm
- Short-watch:    KAITO/USDT trigger 1h close beyond retest zone ~0.973-0.985 + continued OI decline
- Catalyst-watch: HYPE/USDT trigger hold/reclaim $52 support + entry into a scored top-setups table
- Avoid:          SNDKB/USDT & MUB/USDT (squeeze-capped, thin liquidity, no derivatives data)

Risk:
- Iran/Hormuz conflict confirmed escalating (external sources); mexc_canary_monitor now showing confirmed heartbeat errors post-restart (TODO-1 escalated)

Catalyst coverage: mapped 232/1000 (23.2%), baskets 5
                   weak this run — context only

File: OPUS_ENRICHED_REVIEW_LATEST.md
Advisory only. No auto-trade.
```

**Note on Telegram delivery:** per §C, no Telegram-send command is on this run's whitelisted CLI list (§A.4) and no dedicated notifier tool was available. The message above was composed but **not sent**, consistent with every prior scheduled run of this skill. The production scheduler's own Telegram dashboard-refresh step delivers the standard operational summary independently of this review.
