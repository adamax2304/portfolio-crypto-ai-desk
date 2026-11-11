# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:39 EEST

## 1. Executive Summary

**Slot type: crypto overnight / Asia review. Advisory only — no auto-trade.** Current time 01:39 UTC / 04:39 EEST — inside the desk's own Asia dead-zone window (00–06 UTC). Crypto stays deep risk-off: BTC `transition_down`, ETH `downtrend`, breadth **0.0%** of tracked symbols above EMA20 in both the 00:38 intraday and 00:33 swing scans, macro risk 84–92/100 on the ongoing Iran/Strait-of-Hormuz escalation. Discovery breadth was minimal tonight — both scans report 0 fused candidates and deep-analyzed only the two hardcoded anchors (BTC, ETH); no fresh A- or B-tier crypto setup was produced this cycle. Stocks are closed (pre-market not even open yet) — carried-forward planning context only; AVGO reported a Q4 guidance miss overnight (-4% AH) confirming its existing short thesis, but it's already capped C-tier for `stale_post_earnings_setup` + market-closed. Six B-tier crypto swing longs (PROM, TUT, S, GIGGLE, TAO, ONT) hit their validity-window end at **04:46 EEST** — signal_outcomes already logged them **entered-unresolved (0R display / unresolved, no TP/SL before window)**, not a loss. The live open crypto position worth watching is **ENA/USDT intraday short** (triggered, no catalyst contradiction found, expires 17:29 EEST today). Best long-watch remains **FF/USDT** (momentum-breakout basket, no catalyst — pullback only). Best catalyst-backed watch is **UNI/USDT** (Uniswap volume-record narrative, still fresh in tonight's cycle, already extended — do not chase). Best short-watch is the desk's own **BTC/USDT** C-tier idea (score 54.1, failed-retest short bias). Catalyst mapping is weak this run (53.6% unmapped) — treat catalyst layer as context only.

## 2. Data Used

- `data/reports/intraday/2026-09-03_00-38_intraday_report.md` (fresh, ~4h old at run time; data freshness stamp 2026-09-03 00:30 UTC)
- `data/reports/swing/2026-09-02_21-33_swing_report.md` (fresh <4h at generation; ~4h06m old at run time — borderline fresh/carry-forward boundary, still today's newest swing scan)
- `data/reports/stocks/intraday/2026-09-03_01-20_stocks_intraday_report.md` (last stocks-intraday scan; market closed, planning-only per its own header)
- `data/catalysts/2026-09-03/catalyst_cycle_00-44.md`, `catalyst_events.jsonl` (500 events), `narrative_baskets.jsonl` (5 baskets) — all ~1h old
- CLI: `active-signals --asset-class crypto` (50 rows), `active-signals --asset-class stocks` (no active — all C-tier/closed), `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`, `detect_untracked_legacy_alerts --since 2026-09-03` (clean — no untracked alerts)
- `db/crypto_ai_desk.sqlite` — read-only: `news_items` (ENA/USDT 24h check — none found), `proposed_signals` (ENA history: long→long→short thesis evolution), `signal_outcomes` (6 expiring swing longs — confirmed entered-unresolved/0R)
- `data/scheduled_runs/2026-09-02_default_schedule/scheduler.log` (freshness + timeout audit)
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-09-02_2336.md` (post-close, ~5h earlier)
- **External web research: not needed this cycle** — internal `news_items`/`proposed_signals`/catalyst records were sufficient, recent, and internally consistent for every candidate reviewed (no WebSearch/WebFetch performed).

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime **04:29 EEST** (~10 min old at run time) → fresh.
- Latest `cycle_*_summary.md` (`cycle_01_22-07_summary.md`) mtime **01:30 EEST** (~3h09m old) → aging but scheduler.log alone is fresh, so **no defer** (§D rule: defer only if both > 3h).
- Intraday report generated 03:37:54 EEST (data freshness stamp 00:30 UTC) → fresh.
- Swing report generated 00:33:36 EEST → **carry-forward** (~4h old at run time, just past the strict <4h "fresh" cutoff but still today's newest swing scan; no fresher one exists).
- Stocks intraday report (01:20 UTC) → expected/appropriate; market is closed until 16:30 EEST, treated as planning-only per its own header.
- Scalp report last dated 2026-08-30 — **expected**: crypto scalp remains correctly disabled (signal-stats: mode=scalp PF 0.167, n=41, avgR -0.076 this week — still net-negative, disable decision still empirically supported).
- Stocks swing/invest reports last dated 2026-07-02 — **expected/known**: deprecated/removed playbooks per project memory, not a regression.
- **Timeout cluster, still elevated:** scheduler.log shows **16 `CMD TIMEOUT` lines** across the last ~2 cycles (22:35 EEST 09-02 → 04:01 EEST 09-03), all logged non-fatal / cycle continues. Notably **`refresh obsidian dashboard` timed out again at 01:30 EEST** — this is the same step that caused a 6h05m scheduler hang on 2026-08-31 (per project memory). This time it recovered on its own; scheduler.log confirms normal progression through 04:40 EEST with no hang. Flagged again in §14 given the specific-step recurrence.
- Discovery funnel: both intraday and swing scans report `Scanned on binance/bybit/mexc: 0`, `After liquidity filter: 0`, `After momentum filter: 0`, `Fused candidates: 0`, with only the 2 hardcoded BTC/ETH anchors reaching deep analysis. Consistent with the Asia dead-zone guard (00–06 UTC demotes crypto scalp/intraday to C) and generally thin overnight liquidity — not treated as an anomaly this cycle, but breadth of candidate discovery was essentially zero beyond BTC/ETH.
- Paper/monitor status: no fatal crashes in the log window reviewed; the timeout cluster above affected paper-shadow/portfolio-ledger-adjacent steps in the prior cycle window, so any paper-shadow numbers for that window may reflect a stale ledger for that cycle only (does not affect tonight's active-signals read, which queries `proposed_signals`/`signal_outcomes` directly).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-09-03 04:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["fresh cross-exchange scan beyond BTC/ETH"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 04:29 EEST, cycle_01_22-07_summary.md mtime 01:30 EEST (~3h09m, still under defer threshold)", "16 CMD TIMEOUT lines 22:35-04:01, incl. recurrence of 'refresh obsidian dashboard' (2026-08-31 hang precedent), non-fatal this time", "fused candidates: 0 in both intraday and swing scans; deep analysis limited to BTC/ETH anchors"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.85,
      "reason_codes": ["risk_off", "shorts_preferred"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: bearish trend / risk-off, BTC transition_down, ETH downtrend, 0.0% breadth above EMA20/EMA50 in both scans", "macro risk 84.4-92.2/100, Iran/Strait-of-Hormuz escalation unchanged from post-close review", "stocks: risk_off/short bias, but market closed (pre-market not open) — carry-forward only"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl: 500 total, 232 mapped (46.4%), 268 unmapped (53.6%) -> weak this run", "momentum_breakout basket (<1h fresh): UNI/USDT catalyst-confirmed, AUCTION/USDT explicitly flagged 'without confirmed catalyst'", "no ENA/USDT news_items in last 24h -> short signal not catalyst-contradicted"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["oi_supports", "data_unavailable"], "data_missing": ["OI/funding coverage beyond BTC/ETH"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/ETH: price down + OI down = deleveraging/long liquidation, funding near-neutral, crowding normal (both Bybit internal and Bybit/OKX/MEXC cross-check)", "no derivatives read available for the night's narrative-basket names (UNI, FF, AUCTION, HYPE, NEAR cluster)"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["entry_late", "chase_risk", "price_moved_away"], "data_missing": ["TradingView / manual chart check unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/USDT C-tier watch score 54.1, conditional failed-retest short zone 77081.14-77267.76, invalidation 77495.84", "ETH/USDT swing C-tier watch score 51.2, conditional failed-retest short zone 2398.51-2407.56, invalidation 2418.61", "AUCTION/USDT already triggered (swing long, score 68.0) riding a no-catalyst-confirmed momentum move per tonight's basket note"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.8,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 2 waiting_for_entry (KITE, ZK swing) + ~20 triggered (this week's cohort) + a long tail of older tp1/tp2_hit runner positions still shown open back to late July", "6 swing longs (PROM, TUT, S, GIGGLE, TAO, ONT) confirmed in signal_outcomes as entered-unresolved / final_r 0.0 as their windows close at 04:46 EEST", "0 untracked legacy alerts today (detect_untracked_legacy_alerts clean)", "stocks: 0 active A/B signals — all C-tier/planning, market closed"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["reduce_risk"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["cross-exchange-confirmation cohort still losing: PF 0.4333 / avgR -0.174 (n=52, wins=3/losses=17) vs Binance-only PF 2.857 / avgR +0.361 (n=103) — same divergence flagged in the 2026-09-02 post-close TODO, confirmed again tonight", "no fresh legal/headline risk detected on any live crypto position (ENA checked clean)"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto tier=B week: PF 1.674, avgR 0.163, n=157 reliable", "by mode: swing PF 2.30 (n=55, strongest), intraday PF 1.55 (n=61), scalp PF 0.167 (n=41, confirmed correctly disabled)", "weekend_mode=Y cohort underperforms (PF 1.057, avgR 0.017, n=35) vs weekend=N (PF 1.89, n=122)"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.7,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.7,
    "preferred_side": "shorts",
    "best_long_candidate":     { "symbol": "FF/USDT", "trigger": "pullback/retest holding above the momentum-breakout support shelf with volume confirmation", "reason": "in tonight's fresh (<1h) momentum_breakout basket, explicitly flagged 'without confirmed catalyst' — do not chase the breakout itself, size small" },
    "best_short_candidate":    { "symbol": "BTC/USDT", "trigger": "1h close below 76264.00 support, or a failed retest/rejection inside 77081.14-77267.76 with volume", "reason": "the desk's own C-tier watch (score 54.1) in a confirmed transition_down regime with 0% breadth above EMA20 — cleanest short structure available tonight, but not yet active (score below threshold)" },
    "best_catalyst_candidate": { "symbol": "UNI/USDT", "trigger": "pullback to the breakout shelf holding with volume, do not chase the existing extension", "reason": "the only symbol in tonight's basket explicitly tagged catalyst-backed (Uniswap trading-volume-record narrative), fresh <1h in tonight's cycle" },
    "avoid_candidate":         { "symbol": "AUCTION/USDT", "reason": "already-triggered B-tier swing long (score 68.0) riding a momentum move tonight's own basket note flags as 'without confirmed catalyst' in a risk-off/short-preferred regime — do not add to it or treat similar no-catalyst names as new entries" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.75 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.85 | risk_off, shorts_preferred | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, fresh_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.50 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | entry_late, chase_risk, price_moved_away | advisory_only |
| execution_lifecycle | caution | 0.80 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.65 | reduce_risk | advisory_only |
| playbook_performance | ok | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.70 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Comparison vs `OPUS_ENRICHED_REVIEW_AUTO_2026-09-02_2336.md` (post-close, ~5h earlier):

- **Confirmed / unchanged:** Crypto regime still bearish/risk-off, macro risk still elevated on the same Iran/Strait-of-Hormuz theme (84-92/100 vs 100/100 at post-close — marginally lower but still dominant). Neither intraday nor swing has produced a fresh A/B for at least 5 consecutive cycles now. Cross-exchange-confirmation cohort still losing (PF 0.43 tonight vs PF 0.35 at post-close — consistent, sample-supported divergence).
- **Resolved since last review:** The prior review's SNOW AVOID call and BIIB/DELL manual-review/wait flags are stocks-side and carry forward unchanged (market still closed) — no new information on them this cycle. AVGO's overnight guidance-miss reaction (-4% AH, confirmed via internal news_items) validates the desk's own short bias on AVGO, already correctly capped C-tier for post-earnings + market-closed.
- **New this cycle:** Six B-tier swing longs (PROM, TUT, S, GIGGLE, TAO, ONT) that were open at post-close have since reached their validity-window end (04:46 EEST) and are confirmed in `signal_outcomes` as entered-unresolved (0R). The post-close review's long-watch/short-watch/catalyst-watch trio (FF/UNI/ONG) is materially unchanged tonight except the short-watch: ONG/USDT is no longer in tonight's top-movers or watchlist output, so the short-watch this cycle is the desk's own fresh BTC/USDT C-tier idea instead.
- **Breadth deteriorated further:** breadth above EMA20 was 31.25% at post-close; both of tonight's scans show 0.0% — confirms the risk-off regime intensified overnight into the Asia session, consistent with the "crypto overnight/Asia" slot focus.
- **Recurring data-quality item:** `refresh obsidian dashboard` timed out again (01:30 EEST) — same step flagged in project memory for the 2026-08-31 6h05m hang. Non-fatal this time (see §3, §14).

## 5. Catalyst Coverage

- Total `catalyst_events` today: **500**
- Mapped (non-null symbol): **232 (46.4%)**
- Unmapped (null symbol): **268 (53.6%)**
- `narrative_baskets` today: **5** (ai_narrative, binance_ecosystem_teaser, perps_dex_narrative, rwa_narrative, momentum_breakout)
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Top 3 unmapped headlines (macro/rates noise, no ticker resolution attempted by design):
  1. "OIL FUTURES FALL ON LIKELY TECHNICAL CORRECTION - WSJ ..."
  2. "Pantera Capital CEO Dan Morehead predicts only 'one or two' digital asset treasuries per coin will survive..."
  3. "JAPAN SERVICES PMI COMES IN AT 52.5, UP FROM PREVIOUS 52.3 ..."
- Freshest (<1h) high-confidence catalyst-linked crypto name: **UNI/USDT** (momentum_breakout basket, catalyst-confirmed per the basket's own cross-check text). AUCTION/USDT sits in the same basket but is explicitly marked "without confirmed catalyst."

## 6. Market Landscape

- **Crypto:** Regime = bearish trend / risk-off. BTC `transition_down`, ETH `downtrend` (intraday) / `transition_down` (swing). Breadth: **0.0%** above EMA20 and EMA50 in both scans — a deterioration from the post-close review's 31.25%. Strongest names (ETH score 59.7-59.9, BTC score 45.4-57.3) are only "strongest" in a relative, thin-volume sense (volume ratio 0.43-0.57x) — not real breadth-driven strength. Derivatives: both BTC and ETH show price-down + OI-down (deleveraging/long liquidation), funding near-neutral, crowding normal — no squeeze setup detected.
- **Stocks:** Market closed (pre-market not yet open; RTH opens 16:30 EEST). Carried-forward planning context only: prior night's regime was risk_off/short bias, VIX ~15.2-15.4 (not a fear spike — a breadth/trend call). AVGO reported Q4 guidance miss overnight (-4% after-hours per internal `t.me/marketfeed` wire), confirming its existing A-tier short thesis, but it (and every other stocks candidate) is capped to C-tier for `market_closed_intraday_planning_only` plus `stale_post_earnings_setup` for AVGO/SNOW specifically. DELL also reports earnings today — do not chase either name pre-open.
- **Macro:** Risk score 84.4-92.2/100, still dominated by the Iran/Strait-of-Hormuz escalation theme (US ambassador/NATO rhetoric, Trump aide reporting on intensifying attacks post-election, US Navy escorting oil tankers through the Strait) — unchanged in substance from the post-close review, marginally lower numeric score.

### Market Mood / Risk Routing

- Crypto mood: **risk-off** (deepened overnight — 0% breadth vs 31% at post-close)
- Stocks mood: **closed** (pre-market; carry-forward risk-off/short bias from yesterday)
- Dominant narrative: Iran/Strait-of-Hormuz geopolitical escalation (macro overlay, unchanged); Uniswap volume-record narrative still fresh in DeFi; AI-sector rotation (NEAR/RENDER/TAO/FET) newly surfaced in tonight's catalyst cycle, unconfirmed by price/RS yet.
- Preferred side now: **shorts (crypto)**, catalyst-backed only for longs, stocks planning-only until RTH.
- Best long candidate: **FF/USDT** (watch-only, no catalyst — see §8)
- Best short candidate: **BTC/USDT** (watch-only, desk's own C-tier idea — see §8)
- Best catalyst-backed candidate: **UNI/USDT** (watch-only, already extended — see §8)
- What to avoid: adding to AUCTION/USDT or chasing any other no-catalyst-confirmed narrative-basket name (NEAR, RENDER, TAO, FET, BNB, HYPE, DYDX, GMX) at current extension without RS/volume confirmation; chasing AVGO/SNOW pre-RTH on last night's after-hours moves.
- What would change the view: BTC/ETH reclaiming `transition_down`/`downtrend` back toward neutral with breadth recovering off 0%; a de-escalation in Iran/Strait-of-Hormuz headline flow; a confirmed pullback entry on UNI or FF holding on volume.

## 7. Candidate Deep Dives

### 7.1 ENA/USDT (crypto, open B-tier intraday short, score 65.5, `triggered`)
- Signal: entry 0.14869-0.15025, invalidation 0.15215 (above), TP1 0.14454/TP2 0.14109/TP3 0.13763, expires 2026-09-03T17:29:17Z.
- Thesis history check (per §I contradiction-risk priority): this is the *third* ENA thesis in 36h — swing long (score 70.3, stopped) → intraday long (score 67.0, stopped) → now intraday short (score 65.5, `weak_vs_market`/`breakdown` tags). This reads as the model correctly flipping direction as ENA's relative strength deteriorated, not a contradiction.
- Catalyst check: no ENA/USDT `news_items` rows in the last 24h, and no ENA entry in tonight's `catalyst_events.jsonl` — the short is **not catalyst-contradicted**.
- Has price already reacted? Yes — two prior long attempts already stopped out on the way down.
- Chase risk? No — this was an intraday breakdown/retest setup, not a chase.
- Aligned with market mood? Yes — matches the "short bias or no trade" regime recommendation.
- Actionable now? Already triggered and open; nothing new to do — monitor into its 17:29 EEST window close.
- **Verdict: OPEN ACTIONABLE — no change, no contradiction found, consistent with regime.**

### 7.2 The six expiring swing longs — PROM, TUT, S, GIGGLE, TAO, ONT (crypto, B-tier swing, `triggered`)
- All created 2026-09-02T04:46:34Z, validity window ends 2026-09-03T04:46:34Z (within minutes of this review).
- `signal_outcomes` confirms all six as `entry_triggered=1`, `stop_hit=0`, `tp1_hit=0`, `final_r=0.0`, `final_outcome='expired'` as of the last check (01:46 EEST).
- Per the mandated lifecycle vocabulary: this is **ENTERED UNRESOLVED — 0R display / unresolved, no TP/SL before window** for all six, **not** a loss and **not** a missed entry.
- **Verdict: NEEDS NO ACTION — routine window closure, correctly logged.**

### 7.3 UNI/USDT (crypto, C-tier/momentum-breakout basket, catalyst-backed, not yet a proposed_signal)
- Fresh (<1h) in tonight's `catalyst_cycle_00-44.md`, explicitly tagged catalyst-backed (Uniswap trading-volume-record narrative) vs. AUCTION/USDT in the same basket which is explicitly "without confirmed catalyst."
- Has price already reacted? Per the prior cycle's data it was already +19.5% before this basket refreshed — likely still extended; no fresh OHLCV pulled for UNI tonight (outside the BTC/ETH deep-analysis scope) to confirm current extension.
- Chase risk: **yes**, treat as pullback-only until a fresh retest holds on volume.
- **Verdict: CATALYST-BACKED WATCH — not actionable at assumed current extension; needs a fresh OHLCV check before any real entry consideration (data gap noted).**

### 7.4 AUCTION/USDT (crypto, open B-tier swing long, score 68.0, `triggered`, expires 09-06)
- Part of tonight's momentum_breakout basket but explicitly flagged "without confirmed catalyst" in the basket's own cross-check text — i.e., the position currently open is riding a momentum move the catalyst layer itself does not confirm.
- Aligned with market mood? No — this is a long in a regime the desk's own model labels "short bias or no trade; avoid weak altcoin longs."
- **Verdict: MONITOR CLOSELY, DO NOT ADD — existing open position, no new-entry action possible or recommended; flagged as this cycle's avoid-candidate for any similar no-catalyst momentum add.**

### 7.5 FF/USDT (crypto, momentum-breakout basket, no catalyst, not yet a proposed_signal)
- Same basket as UNI/AUCTION; funding neutral across Bybit/MEXC per last night's derivatives read, low crowding.
- **Verdict: LONG-WATCH ONLY — pullback/retest entry with volume confirmation only; no catalyst backing, keep size/confidence low.**

### 7.6 BTC/USDT (crypto, C-tier watchlist, score 54.1, not yet a proposed_signal)
- Tonight's own intraday report watch idea: conditional failed-retest short zone 77081.14-77267.76, invalidation above 77495.84, conditional targets 76583.50/76168.80/75754.09.
- Is this a chase-risk setup? No — it is explicitly conditional/watch-only, requiring the retest to fail first.
- Aligned with mood? Yes — matches transition_down regime and 0% breadth.
- **Verdict: SHORT-WATCH ONLY — wait for the failed-retest confirmation or the 1h close below 76264 support; do not pre-position.**

## 8. Best Candidates Ranked

1. **Best short-watch: BTC/USDT** — trigger: 1h close below 76264.00, or a failed rejection inside 77081.14-77267.76 with volume; do not pre-position ahead of confirmation.
2. **Best catalyst-backed watch: UNI/USDT** — trigger: pullback to the breakout shelf holding with volume; treat as likely still extended (data gap — no fresh OHLCV pulled tonight).
3. **Best long-watch: FF/USDT** — trigger: pullback/retest holding above the momentum-breakout support with volume confirmation; no catalyst backing, keep size small.
4. **Open, no action needed: ENA/USDT** intraday short — monitor into its 17:29 EEST window, no contradiction found.
5. **Avoid adding to: AUCTION/USDT** — open swing long riding a no-catalyst-confirmed move in a short-preferred regime.

No new immediately-actionable trade exists this cycle (correct given 0% breadth, 0 fused candidates, and the Asia dead-zone guard window) — the above are the best-available watch candidates with exact triggers, per PART 9, not a blanket no-trade call.

## 9. Avoid / No Trade

*This decision window only — scanning, tracking, and the scheduler continue in all moods.*

- **New adds to AUCTION/USDT** or any other no-catalyst-confirmed narrative-basket name (NEAR, RENDER, TAO, FET, BNB, HYPE, DYDX, GMX) — none carry RS/volume confirmation yet.
- **Chasing UNI/USDT** at its already-extended level — pullback/retest only.
- **New crypto longs generally** — regime explicitly recommends against weak altcoin longs with 0% breadth above EMA20.
- **Stocks: any pre-RTH action on AVGO, SNOW, or DELL** based on last night's after-hours moves — full RTH confirmation required; DELL reports today.

## 10. Main Risks

- **Extreme breadth deterioration**: 0.0% of tracked symbols above EMA20/EMA50 in both scans tonight — a further decline from 31.25% at post-close; a genuine broad-based risk-off condition, not a data artifact (consistent across independent intraday and swing scans).
- **Macro/geopolitical**: Iran/Strait-of-Hormuz risk persists at 84-92/100 for multiple consecutive cycles — a real incident could move BTC/ETH sharply intraday.
- **Cross-exchange-confirmation cohort still losing**: PF 0.43 (n=52) vs Binance-only PF 2.86 (n=103) — same sample-supported divergence flagged at post-close, unresolved (§14).
- **Scheduler timeout cluster recurrence**: `refresh obsidian dashboard` timed out again — same step as the 2026-08-31 6h05m hang precedent. Non-fatal tonight but worth tracking for a third recurrence (§14).
- **AUCTION/USDT open position**: riding a momentum move the catalyst layer itself flags as unconfirmed, in a regime the desk labels short-preferred — elevated reversal risk versus other open swing longs.
- **Thin discovery breadth**: 0 fused candidates in both scans tonight means tonight's watch list leans entirely on carried-forward narrative-basket names and the desk's own BTC/ETH anchor ideas — genuinely new setups may be missed until liquidity picks up into the EU/US session.

## 11. Action Plan — next 4 hours

1. No new crypto entries — watch BTC/USDT for a failed-retest confirmation, UNI/FF for pullback/retest entries only.
2. Do not add to the open AUCTION/USDT swing long; monitor its invalidation level given the no-catalyst basket flag.
3. Monitor the ENA/USDT intraday short into its 17:29 EEST window — no action needed absent a regime or price contradiction.
4. Continue tracking BTC/ETH `transition_down` status and Iran/Strait-of-Hormuz headline flow into the EU session open (~09:00-11:00 EEST) — no routing change unless regime flips.
5. No stocks action possible until RTH open (16:30 EEST); the 11:30 EEST review will re-assess pre-market reaction on AVGO/DELL/SNOW.
6. Operator: watch for a third `refresh obsidian dashboard` timeout occurrence — if it recurs and this time blocks the cycle, escalate against the 2026-08-31 hang precedent immediately (§14).

## 12. Final Verdict per Mode

- **Crypto scalp:** disabled (confirmed correct — PF 0.167, avgR -0.076, n=41 this week). No change recommended.
- **Crypto intraday:** no new A/B this cycle; ENA/USDT short remains the only live intraday position, unconfirmed by any contradiction. Preferred side: shorts / wait-for-trigger.
- **Crypto swing:** no new A/B this cycle; six swing longs closed out entered-unresolved at 04:46 EEST; remaining open swing book (KITE, ZK, CHIP, NEAR, TNSR, CAKE, AUCTION, GIGGLE, PROM, BANK, DEXE, TURBO, MANTRA, ZEC, RUNE) continues per its own invalidation levels — no new adds recommended given 0% breadth.
- **Stocks intraday:** market closed; zero actionable A/B; AVGO/SNOW carry post-earnings caps into the pre-open review; DELL reports today.
- **Stocks swing/invest (old):** deprecated/removed, not in scope.
- **Stocks swing_growth_breakout (new):** shadow-only research lane, not reviewed this cycle (no fresh data surfaced).

## 13. Sources

- Internal only this cycle (no external web research performed — internal records were sufficient, recent, and consistent for every candidate reviewed):
  - `data/reports/intraday/2026-09-03_00-38_intraday_report.md` — crypto regime, BTC/USDT watch idea, derivatives, macro headlines (generated 2026-09-03T03:37:54+03:00, data freshness 2026-09-03T00:30:00Z).
  - `data/reports/swing/2026-09-02_21-33_swing_report.md` — ETH/USDT watch idea, narrative baskets, macro headlines (generated 2026-09-03T00:33:36+03:00).
  - `data/reports/stocks/intraday/2026-09-03_01-20_stocks_intraday_report.md` — AVGO/SNOW/DELL earnings-risk flags, C-tier candidate table (generated 2026-09-03T01:20:00Z).
  - `data/catalysts/2026-09-03/catalyst_cycle_00-44.md`, `catalyst_events.jsonl`, `narrative_baskets.jsonl` — momentum_breakout / UNI catalyst-backed vs AUCTION no-catalyst classification (generated ~2026-09-03T00:44:00+03:00).
  - `db/crypto_ai_desk.sqlite` — `news_items` (ENA/USDT 24h symbol check, zero rows), `proposed_signals` (ENA thesis history sig_9ca62a42/sig_43e67cd1/sig_de0ac144), `signal_outcomes` (6 expiring swing longs, all `final_outcome='expired'`, `final_r=0.0`).
  - `data/scheduled_runs/2026-09-02_default_schedule/scheduler.log` — freshness + CMD TIMEOUT audit.
  - Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-09-02_2336.md`.

## 14. Fix Requests / TODO

### TODO-obsidian-dashboard-timeout-recurrence
- **issue:** `refresh obsidian dashboard` logged a `CMD TIMEOUT` again at 2026-09-03 01:30:06 EEST. This is the exact step already flagged in project memory as the root cause of the 2026-08-31 6h05m scheduler hang. Tonight's occurrence was non-fatal — scheduler.log confirms the cycle continued normally through 04:40 EEST — but the same step timing out for a second time is worth tracking closely.
- **evidence:** `data/scheduled_runs/2026-09-02_default_schedule/scheduler.log:308` — `2026-09-03 01:30:06,629 [ERROR] CMD TIMEOUT: refresh obsidian dashboard`. Prior incident documented in project memory `project_crypto_ai_desk_scheduler_hang.md` (2026-08-31, 11:20-17:26, 6h05m block).
- **suggested manual fix:** A human-driven session should profile the obsidian-dashboard-refresh step for what makes it intermittently slow/hanging (file I/O on the vault, lock contention, or a network call) and consider giving it a tighter timeout + non-blocking retry so a third occurrence cannot again block a whole cycle.
- **priority:** medium (non-fatal twice so far, but recurring on the exact step with a known hang precedent — escalate to high if it recurs a third time or blocks a cycle).
- **first observed:** 2026-08-31 (hang); this occurrence: 2026-09-03 01:30 EEST (non-fatal recurrence).

### TODO-cross-exchange-cohort-still-losing
- **issue:** `signal-stats --asset-class crypto` again shows the `exchange_confirmation=cross-exchange` cohort losing — PF 0.4333 / avgR -0.174 / totalR -6.8 (n=52, wins=3/losses=17) — versus `exchange_confirmation=Binance` (single-exchange) at PF 2.857 / avgR +0.361 / totalR +26.0 (n=103). This is the same large, sample-supported divergence raised as `TODO-cross-exchange-confirmation-cohort-losing` in the 2026-09-02 post-close review (then: PF 0.35 n=61 vs PF 2.88 n=110) — confirmed again tonight with a fresh sample, not resolved.
- **evidence:** `python -m src.cli signal-stats --asset-class crypto` → "By exchange_confirmation" table, run 2026-09-03 04:39 EEST.
- **suggested manual fix:** unchanged from the prior TODO — investigate whether cross-exchange-confirmed candidates are systematically lower-quality (adverse selection from thinner primary-exchange liquidity), and consider down-weighting or revisiting the cap logic for this cohort.
- **priority:** medium (recurring, still unresolved).
- **first observed:** 2026-09-02 (post-close review); confirmed again 2026-09-03 04:39 EEST.

### TODO-catalyst-mapping-weak-recurring
- **issue:** Catalyst symbol-mapping rate is again below 50% (46.4% mapped / 53.6% unmapped tonight, n=500) — the same "weak this run" condition flagged in the 2026-09-02 post-close review (then 42.4% mapped, n=3000). This appears to be a persistent condition rather than a one-off, at least across the last two reviews spanning different sample windows.
- **evidence:** `data/catalysts/2026-09-03/catalyst_events.jsonl` — 500 events, 232 with a non-null `symbol` field, 268 without, computed via direct JSONL scan this run.
- **suggested manual fix:** a human-driven session should sample the unmapped headlines (macro/rates/PMI-style items dominate the top-3 sample both times) to confirm these are correctly left unmapped by design (no ticker to resolve) rather than a resolver regression; if the ratio holds below 50% for several more cycles with headlines that *do* contain resolvable tickers, escalate to a resolver-coverage investigation.
- **priority:** low (plausibly by-design given the unmapped sample is macro/rates noise both times, but flagging the recurrence for a human to confirm intent).
- **first observed:** 2026-09-02 (post-close review); confirmed again 2026-09-03 04:39 EEST.

### TODO-legacy-runner-signals-long-open
- **issue:** `active-signals --asset-class crypto` (limit 50, no status filter) surfaces a long tail of B-tier scalp/intraday signals still shown at `tp1_hit`/`tp2_hit` status with `expires_at` dates back to **2026-07-21/07-22** (e.g. ZAMA/USDT scalp+intraday, FIL/USDT scalp, ONDO/USDT scalp+intraday, KITE/USDT intraday — 40+ days old). It is unclear from this read-only pass whether these are intentional long-running "let the runner ride past TP1" positions that are still genuinely open, or whether they should have been finalized/closed out and are stuck in a non-terminal status.
- **evidence:** `python -m src.cli active-signals --asset-class crypto --limit 50` output, rows with `status=tp1_hit`/`tp2_hit` and `expires_at` in 2026-07-21 through 2026-08-25 range, run 2026-09-03 04:39 EEST.
- **suggested manual fix:** a human-driven session should check whether these tp1_hit/tp2_hit signals have a defined final-close mechanism (e.g., a trailing stop or a hard time-based close) and, if so, why some are still open 40+ days after tp1/tp2, versus confirming this is intended trailing-runner behavior with no bug present.
- **priority:** low (informational — no evidence of harm, just an open question about intended lifecycle).
- **first observed:** 2026-09-03 (this cycle; not previously logged as a TODO in project memory).

_No further issues beyond the four above this cycle._
