# Opus Enriched Review — post-close final daily review — Auto Cycle 23:32 EEST

## 1. Executive Summary

Slot: **post-close final daily review** (20:32 UTC / 23:32 EEST, after US cash close). Advisory only — no auto-trade, no code/scoring changes made. Scheduler is fresh (log mtime 23:11 EEST, ~21 min old); cycle 3/12 is mid-run (crypto scalp report just regenerated at 23:24 EEST, intraday report regenerating now, not yet complete). **Key daily-wrap finding: crypto cooled into the close.** Mid-session reports (swing 17:52, intraday 15:22) read bullish-trend/risk-on (BTC/ETH uptrend, 56–65% of alts above EMA20); the freshest snapshot at the close (scalp report, data as of 20:15 UTC) flips the regime label to **range/chop (neutral)** — alt breadth above EMA20 eased to 52.1%, volatility percentile eased from ~82 to 78. Macro/geopolitical risk stayed pinned at 97.5–100/100 all day (Iran sanctions, Strait of Hormuz tension) — a persistent risk-off overlay under a technically-still-uptrend BTC/ETH. **No A-tier crypto or stocks setups today.** Best crypto B-tier ideas remain PYTH/USDT (long, near entry) and ZRO/USDT (long, catalyst-paired-with-risk); ONG/USDT is now well extended past its entry zone — chase risk. Stocks: **zero A/B actionable setups all day** — every A-scored candidate was demoted to C by the rolling paper-R drawdown guard or by confirmed legal/headline risk (SMCI indictment, BLK class action, both still open). Stocks week-to-date: shorts (PF 1.67) meaningfully outperformed longs (PF 0.79) — a routing note for tomorrow. Crypto scalp mode remains kill-switched for new entries (pre-existing policy, `crypto_scalp_disabled_by_policy`) — not a new issue. The known untracked-Telegram-alert bug recurred with the same 8 instances already logged in the prior cycle (no new occurrences since 21:39 EEST). Route decisions per mood; do not force trades; scanning continues into Asia regardless.

## 2. Data Used

- Crypto scalp report `2026-08-25_20-25_scalp_report.md` (freshest, data as of 20:15 UTC / ~23:17 EEST — ~15 min old at review time)
- Crypto swing report `2026-08-25_17-52_swing_report.md` (fresh, <4h — data as of 17:45 UTC)
- Crypto intraday report `2026-08-25_15-22_intraday_report.md` (~8h10m old — **stale, carry-forward context only**; a fresh regeneration started at 23:28:47 EEST but had not completed by the time this review was written)
- Stocks intraday report `2026-08-25_17-00_stocks_intraday_report.md` (~6h30m old but this is the **final snapshot of the trading day** — US market closed after this report ran, no fresher data possible until pre-market tomorrow)
- Stocks swing / invest reports: last generated 2026-07-02 — **deprecated/disabled per project decision** (position-framework rework in progress), not a freshness bug
- `data/catalysts/2026-08-25/catalyst_events.jsonl` + `narrative_baskets.jsonl` (full trading day, 5 catalyst-scan cycles, 2,500 events)
- `active-signals --asset-class crypto` / `--asset-class stocks` (CLI, read-only)
- `signal-stats --asset-class crypto` / `--asset-class stocks` (CLI, read-only, week window)
- `detect_untracked_legacy_alerts --since 2026-08-25` (CLI, read-only)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-25_2139.md`
- **External web research not required this cycle** — every candidate carried an internally consistent, same-day record (swing/scalp reports, catalyst layer, production risk-warning pipeline); no candidate decision depended critically on external verification per §G discipline.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: 2026-08-25 23:11 EEST (~21 min old) — **fresh**. Cycle 2 (17:53 start) ended 21:08:46 EEST: `CYCLE 2 END ok=90 failed=10 telegram=sent`. Cycle 3/12 started 23:08:47 EEST and is **still in progress** (crypto scalp report finished 23:28:47 after 1030.7s; crypto intraday report generation started 23:28:47 and had not finished at write time).
- Non-fatal step failures this cycle: `MEXC parity exits (shadow-only, 1m candles)` exited 1 at 23:11:35 EEST — shadow-only, no live/paper execution impact, cycle continued (see §14 TODO). Prior cycle: `refresh obsidian dashboard` timed out at 21:08:35 EEST — cosmetic, telegram dashboard refresh (read-only) succeeded anyway.
- Monitors confirmed healthy/reused at 23:11 EEST: crypto monitor (pid 13276), pending monitor (pid 16224), mexc-canary monitor (pid 12672), crypto-invest-forward monitor (pid 18188), fast-news monitor (pid 9600), stocks monitor (pid 11172); new derivatives-monitor and telegram-dashboard-monitor processes spawned this cycle (pid 5304, pid 4972).
- Report freshness: crypto scalp fresh (~15 min); crypto swing fresh (<4h); crypto intraday **stale carry-forward** (~8h, regeneration in flight); stocks intraday is the day's final snapshot (market closed, treat as current until pre-market tomorrow); stocks swing/invest deprecated (not a bug).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "post_close",
  "as_of": "2026-08-25 23:32 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["fresh intraday report (regenerating, not complete at write time)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 23:11 EEST (~21m old)", "cycle 3 in progress since 23:08:47", "scalp report regenerated 23:24 EEST (fresh)", "intraday report regeneration started 23:28:47, not finished", "stocks intraday 17:00 report is final snapshot of the closed trading day", "stocks swing/invest deprecated since 2026-07-02 (known, not a bug)", "MEXC parity exits (shadow-only) exit=1 this cycle, non-fatal"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mixed", "chop", "risk_off", "longs_preferred"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["mid-session (swing/intraday) reads: bullish trend risk-on, BTC/ETH uptrend, alt breadth 56-65% >EMA20 / 87-90% >EMA50", "freshest close-of-day scalp snapshot (20:15 UTC data): regime flipped to range/chop (neutral), alt breadth >EMA20 eased to 52.1%, ATR percentile eased 82-83 -> 78", "macro/geopolitical risk score 97.5-100/100 all day (Iran sanctions, Strait of Hormuz, US embassy staff returns)", "BTC crossed $81,000 per catalyst feed (Treasury-buyback/ETF-inflow narrative) — bullish headline coexisting with heavy macro tail-risk", "stocks: short direction PF 1.67 vs long direction PF 0.79 this week — underlying stocks tape favored shorts even before today's snapshot"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported", "stale_catalyst"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["full trading day: 2,500 catalyst events, 593 mapped (23.7%), 1,907 unmapped (76.3%) — mapping weak, >50% threshold", "2 active narrative baskets: perps_dex_narrative (primary HYPE/USDT), ai_narrative (primary NEAR/RENDER/TAO/FET) — both fresh <6h, single_source", "ZRO/USDT: LayerZero ATLAS platform catalyst paired with KelpDAO-exploit chain-axing risk event", "BTC: BlackRock $338M ETF inflow (supportive) paired with Coldcard exploit (1,789 BTC drained) and widened Iran sanctions (risk)"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.5,
      "reason_codes": ["oi_supports", "data_unavailable"], "data_missing": ["liquidation heatmaps", "order book depth/CVD — not connected per report blindspots"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ONG/ONT/PYTH/ZRO: price up + OI up, fresh positioning, crowding normal (swing 17:52)", "PROM/FF: price up + OI down, short covering, weaker continuation quality", "HEMI: price down + OI down (deleveraging/long liquidation) consistently across all three timeframe reports today — persistent weakest symbol"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["entry_fresh", "chase_risk", "price_moved_away"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PYTH/USDT: price 0.0526 (17:52 read) vs entry zone 0.0519-0.0523 — near, low chase risk", "ONG/USDT: price 0.1001 (17:52) already through entry zone 0.0951-0.0985; scalp snapshot 3h later (20:15) still shows ONG among the day's strongest movers (24h +16.15%) — likely more extended now, high chase risk", "ZRO/USDT: swing entry zone 1.214-1.240 vs last price 1.252 — marginally extended; the separate earlier scalp position on ZRO has since expired/resolved and dropped off active-signals"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.65,
      "reason_codes": ["waiting_for_entry", "entered_unresolved", "open_actionable", "no_entry"], "data_missing": ["exact total beyond the 50-row CLI display cap"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals (latest 50 shown, all long direction, all B-tier): mix of waiting_for_entry (~10), triggered/entered-unresolved (~30), tp1/tp2-hit open-actionable (~10)", "the ZRO/USDT scalp position flagged in the prior review (expiry ~19:43 UTC) has since resolved and is no longer in the active-signals list", "stocks active-signals list is entirely historical closed/resolved rows (tp1/tp2_hit, dated 08-13 through 08-26); stocks report §6 confirms: 'No A/B-tier actionable setups in this run'"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review", "reduce_risk"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["SMCI demoted A->C: active legal/headline risk (indictment) — manual review required, still open", "BLK demoted A->C: active legal/headline risk (class action) — manual review required, still open", "NVDA/CRM/CRWD earnings tomorrow (2026-08-26) — do-not-chase warnings active", "macro geopolitical risk score 97.5-100/100 all day (Iran sanctions, Strait of Hormuz)", "HYPE: $1.2B token unlock looming — relevant to perps_dex_narrative basket primary"] },
    { "agent": "playbook_performance", "verdict": "bad", "confidence": 0.7,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto scalp (week, n=114, reliable): PF~0.1, avgR negative, totalR ~-6.0 — losing bucket, but mode is kill-switched for new entries (policy), this is a resolving legacy tail not a live risk", "crypto intraday (week, n=150, reliable): PF~2.3, avgR~0.4, totalR ~48.8 — strongest bucket", "crypto swing (week, n=134, reliable): PF~1.6, avgR~0.1, totalR ~18.5 — moderate", "stocks headline A/B (week, n=77, stronger): PF 1.71, avgR 0.135, totalR 5.0, winrate only 6.35% (thin edge, PF carried by win size)", "stocks by tier: A n=10 PF 8.0 totalR 7.0 (too small a sample); B n=67 PF 0.667 totalR -2.0 (losing); C n=586 PF 0.5 totalR -6.5 (expected, watchlist-only)", "stocks by direction: short n=337 PF 1.67 totalR +2.0 outperforming long n=326 PF 0.79 totalR -3.5 this week", "stocks by sector (week): consumer_discretionary and financials positive; technology, communications, consumer_staples, energy, semiconductors negative"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "mixed",
    "best_long_candidate": { "symbol": "PYTH/USDT", "trigger": "1h close/hold inside 0.0519-0.0523 pullback zone; invalidation 0.0513", "reason": "Cleanest B-tier crypto swing idea (75.2/100), strongest historical playbook cohort (crypto_swing_narrative_rs_momentum, 14d WR 72%/PF 5.80), price only ~0.6% above the entry zone as of the last read — not yet chasing" },
    "best_short_candidate": { "symbol": "none scored", "trigger": "crypto: HEMI/USDT is the persistent weakest symbol across all three timeframe reports today (price down + OI down, deleveraging) — would need a B-tier score with a confirmed breakdown on volume to become actionable. Stocks: INTC (short, score 79.74, was B) was demoted to C by the stocks_intraday_short_guard — would need the guard to reset or a fresh B/A confirmation next session", "reason": "No side has a scored, actionable short setup this cycle in either asset class" },
    "best_catalyst_candidate": { "symbol": "ZRO/USDT", "trigger": "swing entry zone 1.214-1.240; catalyst (LayerZero ATLAS platform unveil) is paired with a risk event (KelpDAO-exploit-driven chain axing) — needs the risk event to stay contained, not re-escalate, before treating this as clean", "reason": "Only candidate this cycle with both a fresh internal catalyst and an explicit paired risk flag — genuinely catalyst-driven, not just RS momentum" },
    "avoid_candidate": { "symbol": "SMCI", "reason": "Demoted A->C on active legal/headline risk (indictment) — manual review required, never a clean actionable regardless of score (was 85.9), still open as of this review" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.60 | mixed, chop, risk_off, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, fresh_catalyst, narrative_supported, stale_catalyst | advisory_only |
| derivatives_squeeze | ok | 0.50 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | entry_fresh, chase_risk, price_moved_away | advisory_only |
| execution_lifecycle | ok | 0.65 | waiting_for_entry, entered_unresolved, open_actionable, no_entry | advisory_only |
| risk_manager | caution | 0.60 | legal_risk, headline_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | bad | 0.70 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | caution | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (21:39 EEST)

- **Regime label flipped** for the freshest slice of the data: the 21:39 review carried the swing/intraday "bullish trend risk-on" read; the new scalp snapshot (data as of 20:15 UTC, generated 23:24 EEST) now reads **range/chop (neutral)** — the first chop reading of the day. This is the single most important delta for the daily wrap: crypto cooled into the US close.
- The previously-flagged **ZRO/USDT scalp position (near its ~19:43 UTC expiry) has now resolved** and dropped off active-signals — no longer a monitor item. The **ZRO/USDT swing idea** (72.4, from the 17:52 report) remains a separate, still-open watch-only candidate.
- **ONG/USDT is more extended now** than at 21:39 — still showing among the day's strongest movers in the 20:15 snapshot (+16.15% 24h) while its entry zone (0.0951–0.0985) was already below price at 17:52; treat as higher chase risk than earlier today.
- **PYTH/USDT unchanged as best long-watch** — same trigger zone (0.0519–0.0523), still the cleanest idea.
- Stocks: still 0 A/B actionable, same guard-demotion / legal-risk pattern (SMCI, BLK unchanged). New this cycle: full **stocks signal-stats by direction** shows shorts (PF 1.67) beating longs (PF 0.79) this week — this specific split was not surfaced in the 21:39 review.
- **Untracked-alert count unchanged**: same 8 instances (POL x2, PROM x3, INJ x1, ONG x2) as reported at 21:39 — no new occurrences in the last ~2 hours, the issue is not actively worsening tonight even though it remains open.
- Full-day catalyst mapping (23.7% mapped, 2,500 events across 5 cycles) is now available as a daily aggregate vs the single-cycle read (23.8% of 500) used at 21:39 — consistent, confirms the weak-mapping pattern held all day, not just one cycle.

## 5. Catalyst Coverage

- Total catalyst events **today (full day, 5 catalyst-scan cycles)**: **2,500**; mapped (non-null symbol): **593 (23.7%)**; unmapped: **1,907 (76.3%)**.
- Narrative baskets: **2** (perps_dex_narrative — primary HYPE/USDT; ai_narrative — primary NEAR/RENDER/TAO/FET).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (unmapped 76.3% > 50% threshold, consistent across every cycle checked today)
- Top 3 unmapped headlines (macro/central-bank commentary, not symbol-specific or trading-relevant):
  1. "RBA says cash rate is at top end of neutral rate estimates from models and markets, with uncertainty around estimates…"
  2. "RBA board: current cash rate seen as effective in moving economy toward balance…"
  3. "RBA: board to receive fresh inflation, labour market and GDP data before September meeting…"
- Separately noted (see §14): several catalyst events for US equity tickers (AFRM, AAPL, AMD) are being tagged with a `/USDT` crypto-pair suffix in the top-importance list — a likely symbol-resolver mismap, distinct from the general unmapped-headline noise above.

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **mixed / cooling** — BTC/ETH still technically in an uptrend on the slower (swing/intraday) reads, but the freshest close-of-day snapshot flipped the regime label to range/chop (neutral), with alt breadth above EMA20 easing from 56–65% to 52.1% and volatility percentile easing from ~82 to 78. Macro/geopolitical risk score stayed pinned at 97.5–100/100 all day (Iran sanctions, Strait of Hormuz tension, widened US sanctions targeting tech/aviation/digital assets). Treat as **bullish-structure-but-cooling-into-the-close, headline-fragile** — not clean risk-on, not risk-off either.
- Stocks mood: **closed** for the day (post-close slot); last live read (17:00 EEST) showed 0 A/B actionable setups, everything gated by the rolling paper-R drawdown guard or by legal/headline risk. Week-to-date performance data favors **shorts (PF 1.67, totalR +2.0)** over **longs (PF 0.79, totalR −3.5)** — a routing note to carry into tomorrow's pre-market review, not an action for tonight.
- Dominant narrative: perps/DEX (HYPE-led) and AI-sector rotation (NEAR/RENDER/TAO/FET) — both flagged fresh (<6h) but single-source; also BTC's Treasury-buyback/ETF-inflow bull narrative (BTC > $81,000) coexisting with a live exploit narrative (Coldcard hack, 1,789 BTC drained) and the Iran-sanctions overhang.
- Preferred side now: **crypto — longs, selective, pullback-only** (no chasing extended movers like ONG); **stocks — no new entries tonight** (market closed; shorts were the stronger side this week for tomorrow's planning).
- Best long candidate: **PYTH/USDT** (crypto) — pullback into 0.0519–0.0523.
- Best short candidate: **none scored** — crypto engine is effectively long-only this week (0 scored shorts in the reliable weekly sample); HEMI/USDT is the persistent weakest symbol (watch, not scored); stocks' INTC short was demoted to C by the short-side drawdown guard.
- What to avoid: **SMCI** (indictment) and **BLK** (class action) — both still open, both were A-scored but gated to C; avoid chasing ONG/USDT (already extended); avoid chasing NVDA/CRM/CRWD into tomorrow's (2026-08-26) earnings prints; no new crypto scalp entries (mode kill-switched by policy).
- What would change the view: BTC/ETH losing local uptrend structure overnight would confirm the chop-flip and should prompt reducing long aggression per the system's own no-trade warning; a confirmed B-tier short (crypto or stocks) would open the short side; a rolling-drawdown-guard reset would reopen the stocks A/B pipeline tomorrow.

## 7. Candidate Deep Dives

### PYTH/USDT — LONG (crypto swing, B-tier, score 75.2)
- Has price already reacted to the catalyst? No fresh verified catalyst for PYTH specifically; move is RS/momentum-driven (24h +6.35%, 7d +36.59%, RS vs BTC +5.76% as of the 17:52 read).
- Chasing? Not yet — last read price 0.0526 is only ~0.6% above the top of the planned entry zone (0.0519–0.0523).
- Retest/pullback structure? Entry plan explicitly requires a pullback into the zone; no market-buy-if-extended per playbook rules.
- Overextended (>2 ATR from EMA20)? Not flagged as overextended in the report; ATR 0.0011, price close to the zone.
- Late if entered now? Only slightly — a small pullback confirms it.
- Mood alignment: yes — matches the desk's strongest historical cohort (crypto_swing_narrative_rs_momentum, 14d WR 72%/PF 5.80), though today's fresher scalp snapshot shows the broader regime cooling into chop, so entry discipline matters more than usual tonight.
- Actionable now or after confirmation? After confirmation — wait for 0.0519–0.0523 to hold on a pullback.
- Invalidation: 1h close beyond 0.0513.
- Chase-risk setup? Low, given proximity to entry as of the last read.
- Catalyst confirmation/contradiction? None — "no fresh verified catalyst detected," which the playbook itself flags (catalyst-backed is the cleanest sub-cohort, and this one isn't).
- TradingView / manual chart check unavailable — using only local OHLCV/ATR/EMA fields from the report.

### ONG/USDT — WATCH, chase-risk (crypto swing, B-tier, score 73.9, waiting_for_entry)
- Has price already reacted? Yes, strongly — 24h +33.71% at the 17:52 read, then still among the day's strongest movers (+16.15% fresh 24h read) in the 20:15 scalp snapshot 3 hours later.
- Chasing? Yes — price (0.1001 at 17:52) was already through the top of the entry zone (0.0951–0.0985) hours ago, and the move has continued since.
- Retest/pullback structure? None confirmed yet; the signal remains `waiting_for_entry` in active-signals.
- Overextended? Volume ratio is thin (0.57x–0.09x of average across reads) despite the large price move — relative strength "not backed by strong current volume" per the report's own counter-thesis.
- Actionable now? No — this is a chase-risk setup tonight. What would make it actionable: a genuine pullback back into or near the stated entry zone, ideally with volume confirmation.
- Mood alignment: directionally consistent with a still-uptrend BTC/ETH, but the fresher chop read argues for more entry discipline, not less.
- Catalyst confirmation/contradiction? None — no fresh verified catalyst detected for ONG specifically.

### ZRO/USDT — catalyst-watch (crypto swing, B-tier, score 72.4)
- Has price already reacted to the catalyst? Partially — 24h +14.44%, 7d +61.13%; catalyst (LayerZero ATLAS platform unveil) is fresh but paired with a risk event.
- Chasing? Marginal — last read price 1.252 vs entry zone 1.214–1.240, about 1% above the top of the zone.
- Retest/pullback structure? Entry plan requires a pullback into the zone; no market-buy-if-extended.
- Catalyst confirmation or contradiction? Both present — the ATLAS-platform catalyst is genuinely fresh, but it's paired with "LayerZero to axe 14 low-activity chains after KelpDAO exploit," which the playbook itself flags as a near-window risk event requiring extra entry discipline.
- Actionable now or after confirmation? After confirmation — wait for the pullback zone to hold; treat the exploit-related risk event as a live reason to keep size small if this triggers.
- Note: this is a **different, still-open** position from the earlier ZRO scalp signal flagged in the 21:39 review, which has since expired/resolved and is no longer in active-signals.
- Invalidation: 1h close beyond 1.183.

### SMCI — AVOID (stocks, was A-tier 85.9/score 86, demoted to C)
- Legal/headline risk: **active indictment** — tier demoted A→C, "manual review required," never a clean actionable regardless of score. Still open as of this review (no change since 21:39 EEST).
- Source: internal production risk-warning pipeline (stocks intraday report §7) — no external claim added; no candidate decision depended on further verification.
- Final verdict: **AVOID / MANUAL REVIEW REQUIRED**, unchanged.

### BLK — AVOID (stocks, was A-tier 80.83/score 81, demoted to C)
- Legal/headline risk: **active class-action** — tier demoted A→C, "manual review required." Still open as of this review.
- Final verdict: **AVOID / MANUAL REVIEW REQUIRED**, unchanged.

## 8. Best Candidates Ranked

1. **PYTH/USDT** (long, crypto, watch) — best long-watch, trigger: pullback hold in 0.0519–0.0523, invalidation 0.0513.
2. **ZRO/USDT** (long, crypto, catalyst-watch) — trigger: pullback hold in 1.214–1.240; watch that the paired exploit/chain-axing risk event doesn't re-escalate.
3. **Best short-watch: HEMI/USDT** (crypto) — persistent weakest symbol across all three reports today (price down + OI down, deleveraging); no scored signal yet — trigger: a B-tier score with a confirmed breakdown below recent support on volume. **Stocks short-watch: INTC** — demoted from B (score 79.74) to C by the stocks_intraday_short_guard; trigger: guard reset or fresh B/A confirmation next session.
4. **ONG/USDT** (long, crypto, chase-risk — not actionable tonight) — would need a genuine pullback into or near 0.0951–0.0985 with volume to become clean; currently just a "what to avoid chasing" item, not a new entry.
5. **SMCI / BLK** — AVOID, both legal/headline-gated, unchanged from prior review.

## 9. Avoid / No Trade (this decision window only)

- **SMCI** — active indictment, legal/headline risk, manual review required.
- **BLK** — active class action, legal/headline risk, manual review required.
- **NVDA, CRM, CRWD** — earnings tomorrow (2026-08-26); do-not-chase warnings active, avoid new entries or holding through the print.
- **ONG/USDT** — already extended well past its entry zone on thin volume; chasing here would violate the playbook's own conditions-to-avoid.
- Stocks broadly: 0 A/B actionable all day — protective guard working as designed, not a system failure. This applies to **this decision window (and the rest of tonight) only**; scanning, tracking, and the guard's own rolling-window reset continue normally into tomorrow's pre-market — this is not a command to pause the system.
- Crypto scalp mode broadly: kill-switched for new entries (policy), and the resolving legacy tail remains a losing bucket (PF ~0.1) — no action needed, just don't read it as representative of current desk edge.

## 10. Main Risks

- **Regime divergence into the close**: mid-session reports still read bullish-trend/risk-on while the freshest post-close snapshot reads range/chop — if this chop reading holds or deepens overnight, correlated long setups (PYTH, ZRO) could stall or reverse before hitting their pullback zones. Watch the next fresh intraday/swing regeneration (in progress as of this review) to confirm or reject the chop read.
- Macro/geopolitical risk score sat at 97.5–100/100 all day (Iran sanctions, Strait of Hormuz tensions) underneath a still-technically-bullish crypto tape — a headline escalation overnight (Asia session) could invalidate correlated long setups quickly, per the system's own no-trade warning.
- HYPE/USDT: $1.2B token unlock looming — relevant given HYPE is the primary of the perps_dex_narrative basket.
- Catalyst mapping is weak (76.3% unmapped, full trading day) — treat catalyst layer as context only, not a decision driver, for anything not individually verified.
- Stocks week-to-date: long direction is net negative (totalR −3.5, PF 0.79) while short direction is net positive (totalR +2.0, PF 1.67) — a real edge asymmetry worth carrying into tomorrow's routing, not acted on tonight since the market is closed.
- Known tracking-integrity bug (untracked Telegram alerts without a backing `proposed_signal`) — same 8 instances as the 21:39 review, still open, not actively worsening tonight.

## 11. Action Plan — next 4 hours (overnight into Asia)

- Watch for the fresh intraday report (regenerating as of this review) to confirm whether the chop read from the scalp snapshot holds, or whether the swing/intraday bullish-trend read reasserts — this determines whether PYTH/ZRO pullback entries are still the right playbook going into Asia.
- Watch PYTH/USDT for a pullback hold into 0.0519–0.0523; do not chase the current price.
- Watch ZRO/USDT for a pullback hold into 1.214–1.240; keep size disciplined given the paired exploit-related risk event.
- Do not chase ONG/USDT; wait for a genuine pullback with volume.
- No new crypto scalp entries (policy kill-switch, and the mode's week-to-date edge remains negative on the resolving legacy tail).
- No new stocks entries tonight (market closed); re-check the pre-US-open review (16:20 EEST tomorrow) for a guard reset or a genuine fresh A/B setup, and carry forward the short > long directional edge observed this week.
- No action needed on SMCI/BLK beyond continuing to exclude them from any manual override consideration.

## 12. Final Verdict per Mode

- **Crypto scalp:** NO NEW ENTRIES — mode kill-switched by policy; legacy tail resolving with negative week-to-date PF (~0.1), not representative of current edge.
- **Crypto intraday:** WATCH — strongest mode this week (PF ~2.3) but today's report is regenerating; no fresh actionable idea from the stale (8h) intraday read tonight.
- **Crypto swing:** WATCH / WAIT-FOR-TRIGGER — PYTH is the cleanest idea (pullback-only), ZRO is the catalyst-watch (pullback-only); ONG is chase-risk, not actionable.
- **Stocks intraday:** NO NEW ENTRIES — market closed, 0 A/B actionable all day, guard-gated; scanning/tracking continues normally overnight and into tomorrow's pre-market.
- **Stocks swing/invest:** N/A — deprecated pending position-framework rework (not a freshness bug).

## 13. Sources

- Internal: [scalp report 20:25 (23:24 EEST)](data/reports/scalp/2026-08-25_20-25_scalp_report.md), [swing report 17:52](data/reports/swing/2026-08-25_17-52_swing_report.md), [intraday report 15:22 (stale, carry-forward)](data/reports/intraday/2026-08-25_15-22_intraday_report.md), [stocks intraday report 17:00 (final snapshot of the day)](data/reports/stocks/intraday/2026-08-25_17-00_stocks_intraday_report.md), [catalyst cycle 15:31](data/catalysts/2026-08-25/catalyst_cycle_15-31.md), `data/catalysts/2026-08-25/catalyst_events.jsonl` (full-day aggregate, 2,500 events).
- ZRO catalyst: "LayerZero unveils ATLAS platform for builders, testnet coming soon" — CryptoBriefing (internal, via swing/scalp report §5); risk pair: "LayerZero to axe 14 low-activity chains after KelpDAO exploit" (internal, via swing/scalp report §5).
- BTC catalyst: "BlackRock Adds Over 60% of Bitcoin's $338 Million ETF Inflow While ETH Also Jumps" (BeInCrypto, internal, via §5b structured catalyst); risk: Coldcard exploit "1,789 BTC drained from 8,865 addresses" (Cointelegraph/CoinMarketCap Telegram, internal).
- SMCI legal risk / BLK legal risk: internal production risk-warning pipeline (stocks intraday report §7, §Production risk warnings) — no external source fetched this cycle (internal record already gates the signal; unchanged since 21:39 EEST).
- No external WebSearch/WebFetch performed this cycle — all cited candidates were covered by fresh, internally consistent, same-day records per §G discipline.

## 14. Fix Requests / TODO

### TODO-untracked-alert-recurrence
- **issue:** Untracked Telegram alerts (watchlist_alerts without a matching proposed_signal within ±6h) — same 8 instances as the 21:39 EEST review: POL/USDT (scalp 09:51, swing 12:29), PROM/USDT (swing 12:29, intraday 15:21, swing 17:52), INJ/USDT (swing 12:29), ONG/USDT (scalp 16:31, swing 17:52). No new occurrences in the last ~2 hours.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-25` output, 2026-08-25 23:2x EEST run.
- **suggested manual fix:** Already tracked as an escalated (high-priority, since 2026-07-17) known bug — watchlist re-fire reuses stale/closed signal_id instead of minting a new proposed_signal. Reconfirmed still unresolved; no new action needed beyond the existing priority.
- **priority:** high (pre-existing, confirmed still open, stable count tonight)
- **first observed:** 2026-07-17 (this run: reconfirmed 2026-08-25 23:32 EEST)

### TODO-catalyst-symbol-resolver-stock-usdt-mistag
- **issue:** Several catalyst events for US equity tickers are being tagged with a crypto `/USDT` pair suffix in the catalyst layer's top-importance list, e.g. "AFRM/USDT" (Affirm earnings headline), "AAPL/USDT" (Apple analyst-target headline), "AMD/USDT" (AMD analyst-upgrade headline) in `catalyst_cycle_15-31.md`. These are equities, not crypto trading pairs — looks like a symbol-resolver mismap rather than intentional dual-tagging.
- **evidence:** `data/catalysts/2026-08-25/catalyst_cycle_15-31.md`, "Top catalysts by importance" section — rows for AFRM/USDT, AAPL/USDT (x2), AMD/USDT (x2).
- **suggested manual fix:** A human-driven session should audit the catalyst symbol-resolver's stock-ticker handling — confirm whether `/USDT` is being appended to bare stock tickers by a shared crypto-pair-formatting code path, and whether this affects any scoring/catalyst-linkage logic for stocks (display-only impact suspected, but not yet confirmed as isolated to display).
- **priority:** medium
- **first observed:** 2026-08-25 23:32 EEST (this run)

### TODO-catalyst-mapping-persistently-weak
- **issue:** Catalyst symbol-mapping rate was 23.7% (593/2,500 mapped) for the full trading day today — consistently below the 50% threshold across every cycle checked (single-cycle reads throughout the day were all in the 20–25% range).
- **evidence:** full-day count from `data/catalysts/2026-08-25/catalyst_events.jsonl` (2,500 events, 593 with non-null symbol); per-cycle read in `catalyst_cycle_15-31.md` (119/500 = 23.8%).
- **suggested manual fix:** Consistent with the already-known symbol-audit finding (prior session: ~17% match rate) — a human-driven session should continue the planned widening of the symbol resolver / alias table for the news layer, per the existing catalyst-linkage project track. Not a new finding, but the persistence across an entire trading day is worth reconfirming as still-open.
- **priority:** medium (pre-existing pattern, reconfirmed)
- **first observed:** prior session (symbol audit); reconfirmed 2026-08-25 23:32 EEST

### TODO-mexc-parity-exits-nonfatal-failure
- **issue:** The `MEXC parity exits (shadow-only, 1m candles)` scheduler step exited with code 1 at 23:11:35 EEST this cycle (non-fatal, cycle continued). This is a shadow-only step (no live/paper execution impact), but a repeated failure pattern would be worth tracking.
- **evidence:** `data/scheduled_runs/2026-08-25_default_schedule/scheduler.log`, line at 2026-08-25 23:11:35,855 — `CMD END: MEXC parity exits (shadow-only, 1m candles) exit=1 4.3s (attempt 1)`.
- **suggested manual fix:** A human-driven session should check whether this is a one-off transient failure (e.g. MEXC API hiccup) or a recurring issue by reviewing recent scheduler logs for the same step across multiple cycles/days; no action needed if it's isolated and shadow-only.
- **priority:** low
- **first observed:** 2026-08-25 23:32 EEST (this run) — single occurrence, not yet confirmed as a pattern

---
_Advisory only. No auto-trade, no code/scoring changes made during this run._
