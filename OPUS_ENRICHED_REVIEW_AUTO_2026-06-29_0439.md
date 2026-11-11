# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:39 EEST

> **Advisory only / no auto-trade. Monday June 29, 2026. Slot: crypto overnight / Asia review. Stocks: pre-market planning only (US open 16:30 EEST / 09:30 ET). Crypto: live and active.**

---

## 1. Executive Summary

**Slot: crypto overnight / Asia review — advisory only / no auto-trade.**

BTC held ~$59K overnight (external sources: $58,983–60,064). Cycle 06 (01:14–02:12 EEST) completed cleanly — 32/32 steps ok. Fresh scalp report generated at 04:37 EEST confirms continued **range/chop** regime: BTC downtrend, ETH downtrend, altcoin breadth 48.7% above EMA20 (near 50/50). F&G=18 (Extreme Fear), unchanged from last night.

**Active signals (11 crypto B-tier):** ZEC scalp short OPEN (triggered), SYN scalp long WAITING FOR ENTRY, POWR scalp long TRIGGERED with **anomalous OI +212% flag**, plus 8 swing signals at tp_hit status (BTC short, ETH short, ETH long, SOL long, HOT long, BEL long, AAV long, AXS long). No A-tier signals across all modes.

**Best long-watch:** ACT/USDT — pull back to 0.0114–0.0120 (strongest RS-leader, +44% vs BTC), only if BTC defends $59K.
**Best short-watch:** ZEC/USDT — already OPEN; next fresh entry zone: bounce to 386–388.
**Best catalyst-watch:** HYPE/USDT — perps_dex_narrative basket (Bitwise BHYP ETF), pullback into consolidation.
**Avoid:** POWR (OI anomaly — potential squeeze trap), UNH (DOJ criminal probe active), VELVET (MEXC-only chase after +270% 7d).

Scalp mode continues to underperform (1W/7L 14d, PF 0.14). No new scalp long entries until re-audit. Swing intraday signals (BTC/ETH shorts) remain the preferred directional trade pending crypto mood.

ALWAYS-SCAN continues. Scanner, tracking, data collection, paper accounting all uninterrupted.

**External web research: available (WebSearch used, WebFetch failed — downgraded to single_source).**

---

## 2. Data Used

| Source | File / CLI | Generated (EEST) | Age | Status |
|--------|-----------|-----------------|-----|--------|
| Scheduler | scheduler.log | 04:38 | 0.03h | **FRESH** |
| Latest cycle | cycle_06_01-14_summary.md | 02:12 | 2.46h | **FRESH** |
| Scalp report | 2026-06-29_01-37_scalp_report.md | 04:37 | <15 min | **FRESH** |
| Intraday report | 2026-06-28_23-04_intraday_report.md | 02:05 | ~2.5h | **FRESH** |
| Swing report | 2026-06-28_14-06_swing_report.md | 17:06 Jun 28 | ~11.5h | **BORDERLINE STALE** (12–14h range) |
| Stocks intraday | 2026-06-28_23-11_stocks_intraday_report.md | 02:11 | ~2.5h | **CARRY-FORWARD** (market closed) |
| Stocks swing | 2026-06-26_15-06 | Jun 26 18:06 | >48h | **STALE** (market closed) |
| Catalyst events | data/catalysts/2026-06-28/ | Cycle 06 ~02:09 | 2.5h | **CARRY-FORWARD** (no 06-29 dir yet) |
| LLM crypto packet | llm_analysis_packet.md | 01:37 UTC | ~3h | **FRESH** |
| Active signals | CLI live | 04:38 | live | 11 crypto B-tier |
| Signal stats | CLI live | 04:38 | live | n=113, PF=1.33, +13R (week) |
| External web | WebSearch | 04:38 | live | BTC ~$58,983–60,064; F&G=18 |

> Swing borderline stale (~11.5h) — use for structure only; do not rely on exact price levels. Stocks stale but market was closed (Monday open 16:30 EEST). **WebFetch failed; external data downgraded to single_source confidence. No external web data ingested this slot.**

---

## 3. Scheduler / Data Freshness

- **Scheduler:** Last write 04:38 EEST (0.03h) — **FRESH** (threshold 3h)
- **Latest cycle summary:** cycle_06_01-14 completed 02:12 EEST — **FRESH** (2.46h)
- **Cycle 06 stats:** ok=32/32 steps, failed=0. Monitor running (background pids, 90-min window)
- **Paper accounting:** scanned=1,803, written=1,803, resolved=1,803, errors=0
- **Paper structural TP:** processed=800 (STRUCTURAL=698, HYBRID=89, ATR_FALLBACK=13)
- **Paper structural stop:** processed=800 (be=407, lock=532, structure_moves=393)
- **Paper shadow A/B (FORWARD only — valid):** B +3.02R / A −20.79R (A_filled=130, B_filled=96). NOT_READY for promotion. Backfill is look-ahead only.
- **Paper portfolio (bybit fee):** $5,107.76 (net +$107.76, +2.16%). Zero-fee: +49.97%; MEXC: +16.38%; Conservative: −6.93%.
- **Untracked alerts:** NONE — all crypto alerts have backing proposed_signal
- **Intelligence layer:** post_unwind_chop=40 (dominant), build_up=12, unknown=38, unwind=4, squeeze_expansion=2. Onchain: config/onchain.yaml MISSING.
- **Reddit social:** All 3 subreddits blocked (403) — social attention layer blind
- **Telegram paper-shadow digest:** skipped (before_send_time)
- **No 2026-06-29 catalyst directory** yet; last catalyst data from 2026-06-28 cycle 06

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-06-29 04:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["onchain_config_missing", "reddit_social_blocked", "catalyst_dir_2026-06-29_missing", "webfetch_failed"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "scheduler.log mtime 04:38 EEST (0.03h)",
        "cycle_06 completed 02:12 EEST (2.46h, 32/32 ok)",
        "scalp 04:37 EEST — FRESH (<15 min)",
        "intraday 02:05 EEST — FRESH (2.5h)",
        "swing 17:06 Jun 28 — BORDERLINE STALE (11.5h)",
        "stocks intraday fresh but market closed; stocks swing STALE",
        "no 2026-06-29 catalyst dir; using 2026-06-28 data",
        "Reddit 403; onchain.yaml not configured; WebFetch failed"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.85,
      "reason_codes": ["risk_off", "chop", "shorts_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC downtrend all reports; ETH downtrend",
        "BTC ~$58,983–60,064 (external WebSearch, multiple sources)",
        "ETH ~$1,550 (intraday report)",
        "F&G=18 Extreme Fear (dashboard cycle 06 step 15)",
        "Altcoin breadth 48.7% EMA20 (scalp) / 50% (intraday) — near 50/50",
        "VIX=18.41, SPY down, QQQ down; IWM/DIA up 5d (bifurcated markets)",
        "crypto_mode=chop; post_unwind_chop dominant: 40/96 symbols",
        "squeeze_expansion: only 2 symbols — broad squeeze risk low",
        "ETH/BTC ratio 0.026344 — ETH lagging"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["no_catalyst", "stale_catalyst", "mapping_weak", "narrative_supported"],
      "data_missing": ["catalyst_dir_2026-06-29_missing", "mapping_percentage_uncounted"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "No 2026-06-29 catalyst directory; using 2026-06-28 data (355 events, 4 baskets)",
        "No fresh verified catalyst for ZEC, SYN, POWR, ACT (all main candidates)",
        "UNH: DOJ criminal probe confirmed (QuiverQuant + Fierce Healthcare — legal_risk)",
        "HYPE: perps_dex_narrative basket active (intraday report)",
        "Iran missile/drone article: BTC '$102K rebound' contradicts current $59K — STALE from prior period",
        "XRP: MiCA partial win — mixed signal",
        "ACT: momentum_breakout basket (<1h fresh at intraday scan time)"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.60,
      "reason_codes": ["post_unwind_chop", "oi_supports", "data_unavailable"],
      "data_missing": ["oi_24h_mexc_only_unavailable_many_symbols", "liquidation_heatmaps_missing"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "post_unwind_chop dominant: 40/96 symbols",
        "squeeze_expansion: only 2 symbols",
        "ZEC: price down + OI up — fresh shorts pressing; squeeze risk if reclaims $387+",
        "POWR: OI +212% 24h (Bybit); funding -0.0162 (deeply negative) — ANOMALOUS",
        "ACT: OI +130% 24h; funding -0.00135 — crowding unknown",
        "Derivatives numeric history sparse per intelligence_update"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.62,
      "reason_codes": ["entry_late", "chase_risk", "clean_retest", "stale_before_entry"],
      "data_missing": ["chart_unavailable_tradingview_mcp_not_loaded"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "ZEC scalp short: TRIGGERED; current ~$385; stop $391.44",
        "SYN long: WAITING at 0.4077–0.4213; current 0.4274 — ABOVE zone; do not chase",
        "POWR long: TRIGGERED; OI anomaly +212% flags squeeze risk",
        "ACT: current 0.0123; watch zone 0.0114–0.0120; slightly above",
        "Chop regime; mean reversion style preferred",
        "VELVET: 7d +286%; extreme chase risk; MEXC-only"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.78,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "review_shadow"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "CLI 04:38: 11 active crypto B-tier signals",
        "ZEC B scalp short: OPEN ACTIONABLE (triggered)",
        "SYN B scalp long: WAITING FOR ENTRY",
        "POWR B scalp long: OPEN ACTIONABLE (triggered, OI concern)",
        "8 swing signals at tp_hit: BEL/AAV(weekend Y), SOL, ETH short, BTC short, HOT, ETH long, AXS(weekend Y)",
        "Paper monitor (02:12): OPEN=0, WAITING=0, ENTERED_UNRESOLVED=26, REVIEW/SHADOW=205, NO-ENTRY/STALE/MOVED-AWAY=8, CLOSED=302W/10L/0flat, NEEDS_REVIEW=0",
        "Untracked alerts: NONE"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["manual_review", "headline_risk", "correlation_cluster"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Scalp mode failing: 1W/7L 14d, PF 0.14 (low_confidence overlay active)",
        "Stocks B-tier: PF 0.69 (below 0.80 alert threshold); WR 17%",
        "Crypto B-tier weekly: WR 20.4%, PF 1.33, +13R — adequate but low WR",
        "POWR OI +212% anomaly: potential squeeze trap for open long",
        "UNH legal risk: DOJ criminal probe confirmed; AVOID all longs",
        "BTC $59K key support; break triggers correlated alt selloff"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Scalp: 0W/4L by mode in signal-stats; -4R; PF 0.00 — FAILING",
        "Intraday: 15W/20L; +14R; PF 1.70 — WORKING",
        "Swing: 6W/15L; +3R; PF 1.20 — marginal positive",
        "Paper shadow B outperforming A (forward): B +3.02R / A -20.79R",
        "14d swing playbook: 72% WR / PF 5.80 / +24R",
        "No-catalyst intraday 14d: WR 23% / PF 0.70 / -3R (net-negative)"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.78,
      "reason_codes": ["shorts_preferred", "wait_for_trigger", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "ZEC short OPEN — monitor; do not add without clean bounce 386-388",
        "ACT best long-watch — requires pullback to 0.0114-0.0120 + BTC $59K hold",
        "HYPE catalyst-watch — perps_dex_narrative; pullback into consolidation",
        "POWR AVOID until OI anomaly resolved",
        "UNH AVOID — DOJ probe; healthcare sector at risk",
        "No A-tier signals across all modes",
        "Scalp playbook failing — no new scalp long entries"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.78,
    "preferred_side": "shorts",
    "best_long_candidate": { "symbol": "ACT/USDT", "trigger": "pullback to 0.0114-0.0120 + BTC holds $59K", "reason": "strongest RS-leader +44% vs BTC; C-tier long-watch" },
    "best_short_candidate": { "symbol": "ZEC/USDT", "trigger": "already OPEN; fresh entry at bounce 386-388 + bearish rejection", "reason": "B scalp short triggered; fresh shorts pressing (price down + OI up)" },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "pullback into consolidation after perps_dex_narrative basket confirmation", "reason": "perps_dex_narrative; Bitwise BHYP ETF catalyst" },
    "avoid_candidate": { "symbol": "POWR/USDT", "reason": "OI +212% anomaly + funding -0.016; potential squeeze trap; manual review required" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|-------|---------|-----------|-------------|-----------------|
| data_quality | ok | 0.82 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.85 | risk_off, chop, shorts_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | no_catalyst, stale_catalyst, mapping_weak, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.60 | post_unwind_chop, oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.62 | entry_late, chase_risk, clean_retest, stale_before_entry | advisory_only |
| execution_lifecycle | ok | 0.78 | open_actionable, waiting_for_entry, entered_unresolved, review_shadow | advisory_only |
| risk_manager | caution | 0.72 | manual_review, headline_risk, correlation_cluster | advisory_only |
| playbook_performance | caution | 0.75 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | caution | 0.78 | shorts_preferred; ACT long-watch; ZEC short open; HYPE catalyst | advisory_only |

---

## 4. What Changed vs Previous Review

*Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-28_2315.md` (post-close 23:15 EEST)*

| Item | Previous (23:15) | Now (04:39) |
|------|-----------------|-------------|
| Active crypto signals | 9 (8 swing + 1 unspecified) | 11 (3 scalp + 8 swing) |
| Scalp signals | None | ZEC short (triggered), SYN long (waiting), POWR long (triggered, OI anomaly) |
| BTC price | ~$60,035–60,251 | ~$58,983–60,064 (slight drift lower) |
| F&G | 18 Extreme Fear | 18 (unchanged) |
| Altcoin breadth EMA20 | 44.7% (weakened) | 48.7% (recovered slightly overnight) |
| Scalp report | 19:41 Jun 28 | **NEW: 04:37 Jun 29** (fresh cycle) |
| Intraday report | 20:09 Jun 28 | 23:04 Jun 28 (cycle 06) |
| PUMP swing long | STOPPED in cycle 5 | Absent from active signals (confirmed stopped) |
| BTC/ETH swing shorts | Active | Still tp_hit (extended into early morning) |
| ACT long-watch | Zone 0.0116–0.0124 | Still watching; current 0.0123 (within upper edge) |
| UNH legal risk | Flagged (DOJ probe) | Still active; unchanged |
| Weekend mode | OFF (ended Sunday) | OFF confirmed (Monday weekday mode) |

**New thesis change:** None. BTC/ETH short thesis unchanged. ACT RS-leader thesis unchanged but pullback not yet triggered.

---

## 5. Catalyst Coverage

- **Total catalyst events (2026-06-28 data, cycle 06):** 355 events, 4 baskets
- **Active narrative baskets:** perps_dex_narrative (HYPE primary), delisting_thin_liquidity (no primary), ai_narrative (NEAR/RENDER/TAO/FET), momentum_breakout (ACT/MAGIC/MANTA)
- **Mapped (non-null symbol):** estimated ≤30 of 355 based on visible report data; majority unmapped (basket/general news)
- **Unmapped:** estimated >90% — mapping % not directly computed (JSONL not parsed this slot)
- **2026-06-29 catalyst dir:** NOT YET CREATED (first cycle of the day will populate)

> **⚠ Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
> Top unmapped/basket headlines: (1) CLARITY Act regulatory update (AMBCrypto); (2) DOJ probe basket entry (no crypto symbol); (3) Iran missile strike article — STALE, BTC price in article ($102K) contradicts current data ($59K).

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** chop / risk-off (BTC downtrend, ETH downtrend, F&G=18, altcoin breadth ~49%)
- **Stocks mood:** pre-market / planning (US open 16:30 EEST / 09:30 ET; first session of the week)
- **Dominant narrative:** broad crypto selloff led by ETH/XRP/DOGE; tech stocks drag; AI capital rotation away from crypto; BTC struggling to hold $60K; no clear overnight catalyst to reverse
- **Preferred side now:** shorts + catalyst-backed longs (no naked long exposure without RS + catalyst confirmation)
- **Best long candidate:** ACT/USDT — trigger: pullback to 0.0114–0.0120, BTC holding $59K
- **Best short candidate:** ZEC/USDT — already OPEN; next fresh entry zone: bounce 386–388 + bearish rejection
- **Best catalyst-backed candidate:** HYPE/USDT — perps_dex_narrative; trigger: pullback into consolidation after verifying Bitwise BHYP ETF still active
- **What to avoid:** POWR (OI anomaly), VELVET (MEXC-only +270% 7d chase), UNH (DOJ probe), new scalp longs (playbook failing), stocks entries before RTH open + 15–30 min
- **What would change the view:** BTC reclaims $61.5K → reduce short weight, add RS-leader longs; BTC breaks $58K → extend shorts, cancel ACT long-watch; fresh confirmed catalyst for ACT/CELO → upgrade to intraday actionable

---

## 7. Candidate Deep Dives

### Candidate 1 — ZEC/USDT | B scalp short | OPEN ACTIONABLE (triggered)

**Lifecycle:** OPEN ACTIONABLE — entry triggered in prior cycle; currently being monitored.

- 24h: −6.42%; RS vs BTC: −4.96% (scalp) / −5% (intraday)
- Scalp entry zone: 386.46–388.70; stop: 391.44; TP1: 380.50 / TP2: 375.52 / TP3: 370.55
- ATR: ~$4.97; current at last scalp scan: $385.47
- **Derivatives:** Intraday: price down + OI up → fresh shorts pressing; squeeze risk if price reclaims $387+. Scalp: OI change near flat (data partial).
- **Catalyst:** ZEC mentioned in swing report with 2 items (whale $4.92M short / Coinbase CEO article — single_source each). Short thesis aligned with whale positioning.
- **Chase check:** Entry was triggered — monitoring existing open position. Price slightly below the 386–388 zone (entered correctly). Not chasing.
- **Squeeze risk:** OI building with price down = more shorts entering, not yet a squeeze. Becomes squeeze risk if BTC rallies sharply past $61.5K.
- **Market mood alignment:** ✓ aligned (shorts-preferred regime)
- **Trigger for adding:** Clean bounce to 386–388 with bearish rejection; do NOT chase below 383
- **Invalidation:** 1h close above $391.44 (stop)
- **Verdict:** OPEN ACTIONABLE — maintain; monitor stop; do not add without confirmed bounce entry

---

### Candidate 2 — SYN/USDT | B scalp long | WAITING FOR ENTRY

**Lifecycle:** WAITING FOR ENTRY — price not yet in zone.

- 24h: +36.95% (scalp) / +23.31% (intraday); 7d: +102%
- RS vs BTC: +38.4% (scalp) / +25.4% (intraday) — confirmed RS leader
- Entry zone: 0.4077–0.4213 (scalp); current price: 0.4274 (scalp) — ABOVE zone
- ATR: ~0.0303; stop below 0.3910
- **Derivatives:** OI down −4.22% (short covering — weaker continuation signal); funding −0.000326 (normal)
- **Catalyst:** No fresh verified catalyst
- **Chase check:** 0.4274 is above the 0.4213 upper edge — DO NOT ENTER at current level. Requires pullback of ~1.4–4.8% to reach zone.
- **Regime fit:** Long bias partially conflicts with shorts-preferred regime; SYN RS leadership partially offsets but no catalyst strengthens the case
- **Scalp mode caveat:** Scalp 1W/7L 14d — treat this signal with elevated skepticism; if no catalyst appears, this is a marginal setup
- **Actionable trigger:** Price retraces naturally to 0.4077–0.4213
- **Invalidation:** 1h close below 0.3910
- **Verdict:** WAITING FOR ENTRY — valid only if price retraces; discipline required; do not chase

---

### Candidate 3 — POWR/USDT | B scalp long | OPEN ACTIONABLE — NEEDS REVIEW

**Lifecycle:** OPEN ACTIONABLE (triggered) — flagged for manual review due to OI anomaly.

- 24h: +22.88%; RS vs BTC: +25.0%; 7d: +15.01%
- Entry zone: 0.0495–0.0513; current: 0.0521 (through zone); stop: 0.0456
- **Derivatives RED FLAG:** OI +212.13% in 24h (Bybit) — extremely anomalous; funding −0.01624 (deeply negative); long/short 1.818 (more longs despite negative funding — unusual)
- This combination suggests: either massive new long crowding at a discount, OR data anomaly (possible new listing event on Bybit perps), OR a short squeeze setup where shorts were overwhelmed
- **No fresh catalyst** for POWR
- **Chase check:** Price is above entry zone (0.0521 > 0.0513); entered but now slightly extended
- **Risk assessment:** Multiple yellow flags — anomalous OI, deeply negative funding, no catalyst, price through zone, scalp mode failing. Cannot fully assess without knowing the source of the OI surge.
- **Verdict:** NEEDS REVIEW / MANUAL REVIEW REQUIRED — do not add; monitor stop at 0.0456; manual session should investigate POWR Bybit perp OI surge source before next decision

---

### Candidate 4 — ACT/USDT | C scalp + intraday | RS-LEADER LONG-WATCH (overnight)

**Lifecycle:** NO-ENTRY / WAITING — best overnight long-watch; no entry triggered.

- Scalp: 24h +42.92%, RS vs BTC +44.39%, current 0.0123; entry zone: 0.0114–0.0120
- Intraday: 24h +38.98%, RS vs BTC +41.10%, expansion watchlist score 92
- Confirmed across all 4 discovery sources: rs_btc_leader, rs_eth_leader, momentum_24h_leader, catalyst_backed
- OI +130% 24h (Bybit); funding −0.001355 (negative, crowding unknown)
- **Catalyst:** momentum_breakout basket primary (from intraday report) — but no standalone verified news catalyst; basket freshness was <1h at intraday scan time (~6h ago now — potentially stale)
- **Chase check:** Current 0.0123 is at upper edge of the 0.0114–0.0120 watch zone (0.25% above top of zone) — do not chase; requires pullback or confirmation the zone holds
- **What makes this actionable:** Price pulls to 0.0114–0.0120 naturally + BTC holds $59K + volume confirms pullback (not a panic dump)
- **Invalidation:** 1h close below 0.0106
- **Verdict:** BEST LONG-WATCH overnight; requires pullback + BTC stability; do not chase above 0.0123

---

### Candidate 5 — UNH (stocks) | LEGAL/HEADLINE RISK | AVOID

**Lifecycle:** NO-ENTRY / AVOID — legal risk confirmed; stocks closed until 16:30 EEST.

- Stocks intraday: B-tier long at 77.97 (planning only — market closed)
- **LEGAL RISK CONFIRMED:** DOJ criminal probe into UnitedHealth Group
- Two independent internal catalyst entries: QuiverQuant (primary source) + Fierce Healthcare (additional)
- Probe extends to Optum Rx AND physician reimbursement — broadening in scope
- Stock reportedly dropped 16% on the news (QuiverQuant headline)
- **Healthcare sector impact:** XLV (healthcare ETF) watchlist — reduce conviction; check if XLV C-tier short setup improves; LLY may be insulated (different therapeutic area) but headline risk spreads to the sector
- **Verdict:** AVOID — do not enter UNH long; legal/headline risk confirmed from multiple internal sources. Reassess after DOJ news resolution.

---

## 8. Best Candidates Ranked

*No clean A/B actionable candidates without caveats this window. Per PART 9: named candidates with exact triggers.*

| Rank | Symbol | Side | Lifecycle | Trigger | Status |
|------|--------|------|-----------|---------|--------|
| 1 | ZEC/USDT | short | OPEN ACTIONABLE | Already in; next add: bounce 386–388 + rejection | Monitor |
| 2 | ACT/USDT | long-watch | NO-ENTRY / WAITING | Pullback to 0.0114–0.0120 + BTC holds $59K | Long-watch |
| 3 | HYPE/USDT | long (catalyst) | CATALYST-WATCH | Perps_dex basket confirm + pullback into consolidation | Catalyst-watch |
| 4 | SYN/USDT | long | WAITING FOR ENTRY | Retraces to 0.4077–0.4213 naturally | Wait |

**Avoid this window:** POWR (OI anomaly → manual review), UNH (legal), VELVET/MEXC-only names (chase), new scalp longs (playbook failing).

**Best long-watch:** ACT/USDT — trigger: 0.0114–0.0120 + BTC $59K hold
**Best short-watch:** ZEC/USDT — already open; fresh entry only at bounce 386–388
**Best catalyst-watch:** HYPE/USDT — perps_dex_narrative; pullback entry pending basket verification

---

## 9. Avoid / No Trade

*This decision window only — NOT a command to stop the system. ALWAYS-SCAN continues.*

- **POWR/USDT:** OI +212% anomaly + deeply negative funding = manual review required; do not add
- **UNH:** DOJ criminal probe — AVOID all long exposure until resolved
- **VELVET/USDT:** 270% 7d, MEXC-only (confirmation=38%), elevated long crowding — chase trap
- **AIXDROP/USDT:** MEXC-only, no derivatives, chase risk
- **New scalp long entries (general):** Scalp mode 1W/7L 14d, PF 0.14 — no new scalp longs; SYN waiting is the only exception if price retraces naturally
- **Stocks entries before RTH open:** US markets open 16:30 EEST; wait for open + 15–30 min confirmation
- **Any move >2 ATR from EMA20:** regime is chop; mean reversion preferred; do not chase breakouts

---

## 10. Main Risks

1. **BTC breaks $59K support** → broad alt selloff; cancel ACT long-watch; extend ZEC/ETH/BTC shorts
2. **POWR squeeze trap:** open long position into OI anomaly; if large short gets squeezed, position works; if OI unwinds sharply, could stop out
3. **ZEC short squeeze:** if BTC rallies past $61.5K, fresh ZEC shorts face squeeze pressure; monitor stop $391.44
4. **Stale swing report (~11.5h):** swing-level entry/exit levels have reduced precision; use for structure only
5. **Catalyst blind spot:** no 2026-06-29 catalyst scan yet; first-of-day news (01:00–04:39 EEST) not captured; HYPE catalyst freshness unknown
6. **Stale Iran/BTC article recirculating:** appearing as active catalyst despite being from prior period; creates false geopolitical risk signal
7. **Healthcare sector gap risk (UNH DOJ):** Monday morning gap down possible; affects XLV, LLY adjacent names
8. **Reddit blocked + WebFetch failed:** social attention layer blind; crowd data unreliable this slot

---

## 11. Action Plan — Next 4 Hours

1. **ZEC scalp short (OPEN):** Monitor stop at $391.44; watch for extension toward TP1 $380.50. If BTC rallies past $61.5K, reduce/close to avoid squeeze.
2. **SYN long (WAITING):** Do NOT chase 0.4274. Enter ONLY if price retraces naturally to 0.4077–0.4213.
3. **POWR (OPEN, NEEDS REVIEW):** Manual session should check Bybit POWR perp OI surge source. Do not add. Monitor stop at 0.0456.
4. **ACT long-watch:** Monitor for pullback to 0.0114–0.0120. If BTC holds $59K and ACT retraces, this is the best intraday long entry for Asia/EU session.
5. **HYPE catalyst-watch:** Check if perps_dex_narrative basket still active in next cycle (cycle 01 of Jun 29). If HYPE pulls back after EU session opens, catalyst-backed intraday long opportunity.
6. **US stocks (16:30 EEST / 09:30 ET open):** UNH = AVOID. LLY A-tier (87.6 score) requires post-RTH confirmation + re-verify no DOJ spillover. Wait 15–30 min after open before any stocks intraday entries.
7. **Next scheduler cycle:** Should create 2026-06-29 catalyst directory and potentially produce fresh intraday/swing reports. Watch for this in cycle 07/01 summary.

---

## 12. Final Verdict per Mode

| Mode | Verdict | Notes |
|------|---------|-------|
| **Scalp** | CAUTION | ZEC short OPEN (monitor); SYN long WAITING (do not chase); POWR NEEDS REVIEW; no new scalp longs (1W/7L 14d, PF 0.14) |
| **Intraday** | WATCH | No new actionable; CELO pullback 0.0640–0.0664 is best intraday long-watch (61.8 C-tier); ETH short at 1553–1559 zone is short-watch (C-tier); no entry until pullback confirmed |
| **Swing** | CARRY-FORWARD | BTC/ETH swing shorts at tp_hit; swing report borderline stale (~11.5h); ACT becomes intraday/swing candidate on pullback; no new swing entries until fresher report |
| **Stocks** | PLANNING ONLY | US markets closed until 16:30 EEST; UNH = AVOID (DOJ probe); LLY A-tier needs post-open confirmation; healthcare sector contaminated; short side tech (XLF, XLY, GOOGL C-tier) needs RTH confirmation |

---

## 13. Sources

**Internal (primary):**
- `data/scheduled_runs/2026-06-28_default_schedule/cycle_06_01-14_summary.md` — cycle 06 stats, 02:12 EEST
- `data/reports/scalp/2026-06-29_01-37_scalp_report.md` — 04:37 EEST (fresh)
- `data/reports/intraday/2026-06-28_23-04_intraday_report.md` — 02:05 EEST (fresh)
- `data/reports/swing/2026-06-28_14-06_swing_report.md` — 17:06 EEST Jun 28 (borderline stale)
- `data/reports/stocks/intraday/2026-06-28_23-11_stocks_intraday_report.md` — 02:11 EEST (carry-forward, market closed)
- `data/catalysts/2026-06-28/` — 355 events, 4 baskets
- `data/processed/llm_analysis_packet.md` — 01:37 UTC
- `OPUS_ENRICHED_REVIEW_AUTO_2026-06-28_2315.md` — previous review (23:15 EEST)

**External (WebSearch — single_source; WebFetch failed):**
- CoinDesk — Bitcoin price — Jun 29 2026; BTC ~$60,064
- MetaMask — BTC $58,983 — Jun 28–29 2026
- Robinhood Prediction Market — BTC Jun 29 target $59,558
- CryptoTicker — crypto market crash June 2026
- BitDegree — Fear & Greed Jun 27 2026 — F&G=13 Jun 27 (internal shows 18 Jun 29 — improvement from 13 to 18)
- CryptoBriefing — Iran missile/BTC article — **FLAGGED STALE** (BTC $102K in article vs $59K current; from prior period)

---

## 14. Fix Requests / TODO

### TODO-POWR-OI-ANOMALY
- **issue:** POWR/USDT OI +212% in 24h (Bybit) + funding −0.016 deeply negative; anomalous combination; possible data error or unusual listing/positioning event
- **evidence:** `data/reports/intraday/2026-06-28_23-04_intraday_report.md` §3: "price up + OI up: fresh positioning confirms trend; funding -0.01624109; OI 24h 212.13%; long/short 1.818; crowding unknown"
- **suggested manual fix:** Manual session should check Bybit POWR/USDT perp listing date + recent contract changes; cross-reference OI data vs Bybit API directly; flag as data anomaly if listing event explains OI surge
- **priority:** high
- **first observed:** 2026-06-29 04:39 EEST

### TODO-IRAN-ARTICLE-STALE
- **issue:** "Iran launches missile and drone strikes on US bases in Kuwait and Bahrain, Bitcoin dips then rebounds past $102K" (CryptoBriefing) is surfacing in the internal news feed; BTC is currently ~$59K, not $102K — article is from a prior period but is being treated as fresh
- **evidence:** `data/reports/intraday/2026-06-28_23-04_intraday_report.md` §5 News; cross-confirmed via WebSearch (BTC $59K Jun 29 2026)
- **suggested manual fix:** Add published_at age validation to RSS ingestion pipeline; articles older than 7 days should not surface as current news; alternatively add a BTC-price sanity check to flag catalysts with implausible price claims (>2x from current)
- **priority:** medium
- **first observed:** 2026-06-29 04:39 EEST

### TODO-CATALYST-SCAN-TODAY
- **issue:** No `data/catalysts/2026-06-29/` directory at 04:39 EEST; first-of-day catalyst scan not yet run; early morning news (01:00–04:39 EEST) not captured in catalyst layer
- **evidence:** Directory listing empty at review time
- **suggested manual fix:** Confirm next cycle (cycle 07 / first 06-29 cycle) includes catalyst scan step; if still empty by 11:30 EEST slot, trigger manually via `python -m src.cli catalyst-scan --no-print`
- **priority:** low (expected at this hour; first cycle will fix automatically)
- **first observed:** 2026-06-29 04:39 EEST

### TODO-SWING-REPORT-FRESHNESS-ASIA-SLOT
- **issue:** Swing report is ~11.5h old at the 04:30 slot (borderline stale); reaches full stale status by the 11:30 EU slot if no new swing scan runs
- **evidence:** `data/reports/swing/2026-06-28_14-06_swing_report.md` — mtime 17:06 Jun 28; observed at 04:39 Jun 29 (11.5h age)
- **suggested manual fix:** Verify next cycle includes swing report regeneration; if swing report is still from Jun 28 at the 11:30 EU slot, mark as stale and exclude swing-level calls from that review's final verdict
- **priority:** low
- **first observed:** 2026-06-29 04:39 EEST
