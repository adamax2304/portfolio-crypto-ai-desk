# Opus Enriched Review — Late-Session Risk Review — Auto Cycle 21:39 EEST

**Date:** 2026-07-03 | **Slot:** late_session (21:30 EEST) | **Generated:** 21:39 EEST
**Cycle:** 08 (finished 20:47 EEST, ~52 min ago) | **Status:** ADVISORY ONLY — NO AUTO-TRADE

> ℹ️ **MARKET CONTEXT:** US stock market **CLOSED TODAY** (July 3 = Independence Day observed; July 4 falls Saturday). Stocks are in planning-only mode. Crypto is the live actionable class. Next US market open: Monday July 6.

---

## 1. Executive Summary

- **Slot:** Late-session risk review (21:30 EEST) — crypto live; stocks closed (planning only). Advisory only, no auto-trade.
- **Crypto market:** BTC ~$61,500-61,700, +2.7% on the day; ETH uptrend; 82% altcoins above EMA20; regime = bullish trend (risk-on). F&G=21 (Fear) diverges from price action — warrants caution on FOMO.
- **Key macro:** BTC ETF inflow $221M today, snapping 10-day outflow streak (largest since May). Single-session inflow — not yet confirmed as trend reversal. BTC still near 21-month lows before this bounce; bounce quality TBD.
- **Active crypto signals:** 20 (down from 44 at 18:40 — many tp_hit or resolved intraday). All B-tier long.
- **Paper monitor:** OPEN actionable=18 · WAITING=5 · ENTERED UNRESOLVED=54 · REVIEW/SHADOW=177 · NO-ENTRY/STALE/MOVED-AWAY=88 · Needs review=0. Paper closed 356W/54L today.
- **Late-session risk focus:** ZKP/THE/MANA have elevated crowding (OI +110-127%, negative funding across venues) → avoid new longs on these late-session; squeeze risk if BTC reverses. RIF remains cleanest swing setup with normal derivatives. ZEC has confirmed Ironwood catalyst (proceeding July).
- **Untracked alerts rising:** 18 today (vs 13 at 18:40 → +5 in 3h). Persistent systemic issue.
- **Stocks:** All intraday signals demoted to C (market closed). UNH carries active DOJ/SEC legal risk → AVOID. Stocks A/B PF=0.33 (7d) — deeply negative.
- **Advisory only. No auto-trade. No live execution.**

---

## 2. Data Used

| Source | File / Command | Age at 21:39 | Status |
|---|---|---|---|
| Crypto scalp report | 2026-07-03_17-31_scalp_report.md | ~1h 9m | ✅ FRESH |
| Crypto intraday report | 2026-07-03_17-36_intraday_report.md | ~1h 3m | ✅ FRESH |
| Crypto swing report | 2026-07-03_12-59_swing_report.md | ~5.6h | ⚠️ BORDERLINE STALE (flag) |
| Stocks intraday | 2026-07-03_18-35_stocks_intraday_report.md | ~4 min | ✅ VERY FRESH |
| Stocks swing | 2026-07-02_13-03_stocks_swing_report.md | ~29.5h | ❌ STALE — excluded from verdict |
| Stocks invest | 2026-07-02_13-05_stocks_invest_report.md | ~29.5h | ❌ STALE — excluded |
| LLM analysis packet | data/processed/llm_analysis_packet.md | ~1h | ✅ FRESH |
| Catalyst events | data/catalysts/2026-07-03/catalyst_events.jsonl | cycle 08 | ✅ 425 events, 5 baskets |
| Cycle 08 summary | cycle_08_20-24_summary.md | 52 min | ✅ FRESH |
| active-signals crypto | Step 23 of cycle 08 | cycle 08 | ✅ 20 signals |
| active-signals stocks | Step 25 of cycle 08 | cycle 08 | ✅ 20 signals |
| signal-stats crypto | Step 24 of cycle 08 | cycle 08 | ✅ |
| signal-stats stocks | Step 26 of cycle 08 | cycle 08 | ✅ |
| untracked-legacy | Step 28 of cycle 08 | cycle 08 | ✅ 18 alerts |
| Paper monitor status | Step 30 of cycle 08 | cycle 08 | ✅ |
| Previous review | OPUS_ENRICHED_REVIEW_AUTO_2026-07-03_1840.md | 2h 59m | ✅ Used for delta |
| Web search | BTC price, ETF flows, ZEC Ironwood | ~21:35 | ✅ |

**External web research:** Available and used. Sources cited in §13.

---

## 3. Scheduler / Data Freshness

| Check | Value | Status |
|---|---|---|
| scheduler.log mtime | 2026-07-03 20:47:58 EEST | ✅ 52 min fresh |
| Latest cycle summary | cycle_08_20-24_summary.md — 20:47:57 EEST | ✅ 52 min fresh |
| Cycle result | 31/32 steps OK, 1 failed (stocks intraday CLI — DB locked) | ⚠️ Minor failure |
| Crypto monitor | Background pid=16636 (90 min window, started 20:45) | ✅ Running |
| Stocks monitor | Background pid=12516 (90 min window) | ✅ Running |
| Crypto swing report | 5.6h old (borderline stale) | ⚠️ Flag |
| Stocks swing/invest | 29.5h old | ❌ Excluded |
| Reddit social | 403 blocked (all 3 sources — persistent) | ⚠️ Missing |
| Onchain | config missing (interface ready, no config/onchain.yaml) | ⚠️ Not configured |

**Deferral check:** scheduler.log 52 min old AND cycle_08 52 min old — both well under 3h threshold. **No deferral.**

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-07-03 21:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["scheduler_fresh", "report_stale", "derivatives_sparse"],
      "data_missing": [
        "reddit_social_403_blocked",
        "onchain_config_missing",
        "stocks_swing_stale_29h",
        "stocks_intraday_cli_step_failed_db_locked",
        "social_attention_missing",
        "cvd_orderbook_depth_missing"
      ],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "scheduler.log mtime 20:47:58 EEST (52 min fresh)",
        "cycle_08 finished 20:47:57 EEST (31/32 steps OK)",
        "stocks intraday step 20 FAILED: OperationalError: database is locked",
        "crypto scalp/intraday reports 1h fresh",
        "stocks intraday monitor report 4 min fresh",
        "intelligence layer: funding/OI numeric history sparse"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.80,
      "reason_codes": ["risk_on", "longs_preferred", "mixed"],
      "data_missing": ["live_btc_eth_price_tick", "social_attention"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC uptrend (~$61,500-61,700 +2.7% today per web search)",
        "ETH uptrend; ETH/BTC=0.027942 (low — BTC-dominated)",
        "Altcoin breadth above EMA20=82.05%",
        "VIX=15.81 (low, supportive)",
        "F&G=21 (Fear) — diverges from bullish price action",
        "SPY uptrend, QQQ=range (tech sector weak)",
        "crypto_mode=trend, stocks_mode=risk_on per market dashboard"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "ok",
      "confidence": 0.72,
      "reason_codes": ["fresh_catalyst", "stale_catalyst", "catalyst_confirmed", "narrative_supported"],
      "data_missing": ["live_telegram_discord_kol_feeds", "token_unlock_calendar_automated"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC ETF: $221M inflow July 3 — snapped 10-day outflow streak (99bitcoins.com)",
        "BlackRock 10-day streak -35,980 BTC ($2.24B) broken by one session",
        "ZEC Ironwood: proceeding as planned per July 3 Shielded Labs statement (DailyCoin)",
        "Catalyst label refresh cycle 08: 5 news_supported flips: WLD×2, TIA, ZEC, NEAR",
        "ZKP, THE, HMSTR, MANA, RIF: no fresh verified catalyst (technical setups only)",
        "HYPE unlock: $630M Core Contributor unlock July 6 (3 days)",
        "Baskets: delisting_thin_liquidity, perps_dex_narrative, binance_ecosystem_teaser, ai_narrative (NEAR/RENDER/TAO/FET)"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.70,
      "reason_codes": ["squeeze_risk", "oi_supports", "funding_extreme"],
      "data_missing": ["oi_numeric_history_sparse", "liquidation_heatmap_missing", "cvd_missing"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "ZKP OI +110.58%; funding bybit -0.00838, okx -0.00522, mexc -0.00520 → elevated crowding 3 venues",
        "THE OI +127.19%; funding mexc -0.00630 → crowding elevated",
        "MANA OI +52.91%; funding okx -0.00119, mexc -0.000927 → moderate crowding",
        "ARPA OI +265.09% (swing report 5.6h old) — extreme",
        "RIF OI +2.39%; funding neutral → fresh positioning, normal crowding",
        "TIA OI +5.82%; funding neutral → clean",
        "Intelligence layer: 6 symbols phase_2_squeeze_expansion, 37 phase_5_post_unwind_chop",
        "Derivatives numeric history sparse — crowding calls lower confidence"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["entry_late", "chase_risk", "overextended", "stale_before_entry"],
      "data_missing": ["live_price_tick", "tradingview_chart_unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "TradingView / manual chart check unavailable — using OHLCV/ATR/EMA fields from report",
        "THE +41.04% 24h, current 0.0708 above entry zone 0.0665-0.0695",
        "ZKP +28.98% 24h, current 0.0592 above entry zone 0.0559-0.0582",
        "MANA +16.28% 24h, current 0.0743 at/above zone 0.0725-0.0738",
        "ADA: explicit >2ATR from EMA20 overextended flag",
        "RIF +22.14% 24h, current 0.1197 above entry zone 0.1131-0.1177",
        "ZEC current 457-458 above entry zone 451.94-455.87",
        "Scalp playbook: all low_confidence overlay active (TP1/2h horizon mismatch)"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.88,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "no_entry", "review_shadow"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Paper monitor: OPEN actionable=18, WAITING for entry=5, ENTERED UNRESOLVED=54",
        "REVIEW/SHADOW=177, NO-ENTRY/STALE/MOVED-AWAY=88, Needs review=0",
        "Paper closed today: 356 WINS / 54 LOSSES / 0 FLAT",
        "Active crypto signals: 20 (down from 44 at 18:40)",
        "Active stocks signals: 20 (all C-tier — market closed demotion)",
        "Cycle 08 track-signals post: checked=555 updated=6 tp_hits=348 stopped=1 expired=1",
        "Entered-unresolved (no TP/SL before window): 54 | No-entry/stale/moved-away: 88"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.82,
      "reason_codes": ["repeated_losses", "legal_risk", "headline_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Stocks A/B PF=0.33 (7d), WR=3.1%, totalR=-3.33 → repeated_losses",
        "Stocks all-tier: PF=0.452, totalR=-17.00",
        "UNH: DOJ/SEC confirmed (Optum Rx Medicare billing probe + UnitedHealth payment practices)",
        "HYPE $630M Core Contributor unlock July 6 (3 days) → headline_risk",
        "18 untracked legacy alerts (up from 13 at 18:40) → systemic tracking gap",
        "F&G=21 (Fear) vs $61.7K BTC — potential mean-reversion risk",
        "Late session 21:30 → new scalp entries inappropriate",
        "DB locked error stocks intraday step = data integrity concern",
        "ETH/BTC=0.027942 (historically low) → altcoin risk elevated if BTC reverses"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "ok",
      "confidence": 0.78,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample", "fresh_expired_problem"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto B swing (7d): PF=7.10, avgR=0.78, n=51 → strongest mode",
        "Crypto B intraday (7d): PF=3.66, n=68 → working",
        "Crypto scalp (7d): 1W/7L PF=0.14 → low_confidence overlay, playbook_failing",
        "Stocks A/B: PF=0.33, WR=3.1% → playbook_failing",
        "Paper portfolio (bybit_non_vip): +$1461.18 net (+29.22%) across all history",
        "Paper shadow forward (B vs A): B +24.13R / A -39.15R (8d forward, NOT_READY)",
        "ENTERED UNRESOLVED=54 → many signals expired after entry without TP/SL hit"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "ok",
      "confidence": 0.75,
      "reason_codes": ["longs_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto regime risk-on, B swing PF 7.10 supports long bias",
        "Late session 21:30 → no new scalps; swing pullback setups only",
        "ZKP/THE elevated crowding + negative funding → avoid new longs now",
        "RIF: cleanest setup (normal OI/funding, news_supported flip, swing score 79.1)",
        "ZEC: confirmed Ironwood catalyst (late July), active triggered signal",
        "WLFI: -2.24% 24h RS vs BTC, consistent weak — best short watch on BTC breakdown",
        "Stocks: UNH AVOID (DOJ); all planning-only until Monday"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "normal",
    "confidence": 0.75,
    "preferred_side": "longs",
    "best_long_candidate": {
      "symbol": "RIF/USDT",
      "trigger": "pullback into 0.1131-0.1177 with BTC holding above $60K",
      "reason": "cleanest B-swing setup: OI fresh/normal, funding neutral, news_supported flip today, 7d RS +72.7%"
    },
    "best_short_candidate": {
      "symbol": "WLFI/USDT",
      "trigger": "BTC 1h close below $60K; WLFI retest of prior breakdown zone",
      "reason": "consistent relative weakness -2.24% 24h; against bullish tape so wait-for-trigger only"
    },
    "best_catalyst_candidate": {
      "symbol": "ZEC/USDT",
      "trigger": "Ironwood late-July activation confirmed; price holds above 447 invalidation or returns to 451-455 zone",
      "reason": "Shielded Labs confirmed upgrade proceeding July 3; signal already triggered; news_supported flip this cycle"
    },
    "avoid_candidate": {
      "symbol": "UNH",
      "reason": "Active DOJ/SEC legal risk (Optum Rx Medicare billing + UnitedHealth payment practices); stocks market closed until Monday; stocks A/B PF=0.33"
    },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason Codes | Suggested Effect |
|---|---|---|---|---|
| data_quality | ok | 0.82 | scheduler_fresh, report_stale (swing 5.6h), derivatives_sparse | advisory_only |
| market_regime | ok | 0.80 | risk_on, longs_preferred, mixed (F&G=21 divergence) | advisory_only |
| catalyst_narrative | ok | 0.72 | fresh_catalyst (BTC ETF $221M), catalyst_confirmed (ZEC Ironwood), stale_catalyst (ZKP/THE/MANA), narrative_supported (AI basket) | advisory_only |
| derivatives_squeeze | caution | 0.70 | squeeze_risk (ZKP/THE/MANA), oi_supports (RIF/TIA), funding_extreme (ZKP bybit -0.84%) | advisory_only |
| technical_entry | caution | 0.75 | entry_late, chase_risk, overextended (ADA/THE/ZKP) | advisory_only |
| execution_lifecycle | ok | 0.88 | open_actionable=18, waiting=5, entered_unresolved=54, no_entry=88, review_shadow=177 | advisory_only |
| risk_manager | caution | 0.82 | repeated_losses (stocks PF=0.33), legal_risk (UNH DOJ), headline_risk (HYPE unlock July 6), reduce_risk (late session) | advisory_only |
| playbook_performance | ok | 0.78 | playbook_working (crypto swing PF 7.10), playbook_failing (crypto scalp PF 0.14, stocks A/B PF 0.33) | advisory_only |
| head_trader | ok | 0.75 | longs_preferred (crypto swing pullbacks), wait_for_trigger (shorts, new scalps) | advisory_only |

---

## 4. What Changed vs Previous Review

**Previous review:** OPUS_ENRICHED_REVIEW_AUTO_2026-07-03_1840.md (18:40 EEST, US open reaction slot)

| Category | Previous (18:40) | Now (21:39) | Change |
|---|---|---|---|
| Active crypto signals | 44 | 20 | -24 (many tp_hit or expired intraday) |
| Active stocks signals | — | 20 | All C-tier (market closed demotion) |
| Untracked alerts | 13 | 18 | +5 in ~3h (worsening) |
| Stocks intraday step | — | FAILED (DB locked) | New issue this cycle |
| BTC ETF inflows | 10-day outflow streak | $221M inflow — streak snapped | Positive (single session) |
| ZEC Ironwood | Delay possible | Proceeding confirmed (July 3 Shielded Labs) | Positive catalyst confirmed |
| Catalyst label flips | — | WLD×2, TIA, ZEC, NEAR → news_supported | 5 new mappings |
| Paper monitor wins | 350W/54L | 356W/54L | +6W today |
| ZKP crowding | OI +106% | OI +110.58% | Slightly worsened |
| ARPA | In top setups (OI +246%) | Not featured cycle 08 | Faded from top setups |
| HYPE unlock | Flagged July 6 | Still 3 days away | Maintain HYPE avoid |
| RIF best long zone | 0.1210-0.1258 | 0.1131-0.1177 (from cycle 08 report) | Zone updated |

**New this review:** Stocks intraday cycle 8 FAILED (DB locked) → TODO. 18 untracked alerts (daily worst count). ZEC Ironwood confirmed. WLD/TIA news_supported flips.

---

## 5. Catalyst Coverage

- **Cycle 08 scan:** events=425, baskets=5, scanned=425, rejected=0
- **Daily cumulative:** 957 unique events, 4-5 baskets
- **Label refresh (cycle 08):** scanned=845, news_flips=5 (WLD×2, TIA, ZEC, NEAR), telegram_flips=2, labels_written=845
- **Active baskets:** delisting_thin_liquidity (BTC/XRP), perps_dex_narrative (HYPE), binance_ecosystem_teaser (BNB), ai_narrative (NEAR/RENDER/TAO/FET)
- **Notable unmapped events:** Humanity Protocol $36M hack, Binance hints delisting 4 altcoins (unnamed), ESMA MiCA licensing, Fed minutes attention, XRP Holder losses at 12-year deep
- **Coverage assessment: adequate this run** — 845 records labeled, baskets fresh (<1h to <6h). No "catalyst mapping weak" flag required.

**Key catalysts by candidate:**
- **ZEC:** Ironwood upgrade proceeding (late July confirmed) — positive; software migration delay risk persists
- **WLD:** news_supported flip (WLD×2 today) — mildly positive
- **TIA/NEAR:** news_supported flip; NEAR in AI narrative basket
- **BTC:** $221M ETF inflow (single session, largest since May)
- **ZKP/THE/HMSTR/MANA/RIF:** No verified catalyst — technical momentum only

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** risk-on / bullish trend
- **Stocks mood:** closed / risk-on (planning only; next actionable Monday July 6)
- **Dominant narrative:** BTC bounce on weak jobs data + rate-cut narrative; ETF inflow reversal signal (unconfirmed trend). Altcoin breadth expansion broad (82% above EMA20). Healthcare + Financials leading stocks. Tech/Semis lagging (QQQ=range).
- **Preferred side now:** longs (crypto swing pullbacks only); NO new scalp entries; NO stocks intraday until Monday
- **Best long candidate:** RIF/USDT — pullback into 0.1131-0.1177 while BTC holds $60K. Cleanest setup: normal OI/funding, news_supported, swing PF=7.10
- **Best short candidate:** WLFI/USDT — only if BTC 1h close breaks $60K; consistent -RS; wait-for-trigger
- **Best catalyst-backed candidate:** ZEC/USDT — Ironwood upgrade proceeding; signal active (triggered); news_supported flip today
- **What to avoid:** THE/ZKP/MANA (OI +52-127%, negative funding → squeeze risk late session); ADA (overextended); UNH (DOJ active); HYPE (July 6 unlock); new scalps at 21:30+
- **What would change the view:** BTC 1h close below $60K → shift to caution/wait; shorts on WLFI/SYN/RE become viable. BTC sustained above $62K with volume on Monday → alts continuation; ZKP/THE re-entry on pullback viable.

---

## 7. Candidate Deep Dives

### Candidate 1: ZKP/USDT — B Intraday/Swing — CAUTION / AVOID NEW ENTRY

**Status:** OPEN ACTIONABLE (intraday B triggered) | CLOSED WIN partial (swing, TP hit per cycle 07 tracking)
**Lifecycle:** Partially OPEN actionable (intraday), partial CLOSED WIN (swing)

**Setup:** +28.98% 24h, RS vs BTC +28.15%. Score 67.1 intraday, 78 swing. Entry zone 0.0559-0.0582, invalidation 0.0531.

- Price above entry zone at report time (0.0592); likely further extended at 21:39
- OI +110.58%; funding negative across bybit (-0.00838), okx (-0.00522), mexc (-0.00519) = crowded longs, 3-venue confirmation
- No fresh verified catalyst — pure momentum
- Chase risk HIGH at current hour
- Mood-aligned: yes (risk-on long) but late-session timing wrong
- **Verdict: AVOID NEW LONG at 21:39.** Swing TP already hit earlier — don't re-enter extended. If price pulls back to 0.0559-0.0582 in Asia session with BTC stable, reassess. Invalidation 0.0531.

---

### Candidate 2: THE/USDT — B Intraday — ELEVATED RISK / NO NEW ENTRY

**Status:** OPEN ACTIONABLE (intraday B triggered)
**Lifecycle:** OPEN actionable

**Setup:** +41.04% 24h, RS vs BTC +40.21% (top RS leader). Score 67.1 intraday. Entry zone 0.0665-0.0695, invalidation 0.0629.

- Highest 24h mover in the universe. Price 0.0708 at report = above entry zone.
- OI +127.19% — highest OI expansion in universe. Funding: mexc -0.00630 (strongly negative). Crowding: elevated/unknown.
- No verified catalyst. Meme/momentum move.
- Chase risk: EXTREME. 41% move with crowded longs = late-session squeeze trap.
- Positions entered earlier this session: monitor stop at 0.0629 hard. Do NOT add.
- **Verdict: DO NOT OPEN NEW LONG.** Highest squeeze risk in current book. If already in: stop at 0.0629, no averaging up. If not in: PASS.

---

### Candidate 3: RIF/USDT — B Swing — BEST LONG WATCH

**Status:** OPEN ACTIONABLE (intraday B triggered); swing partially closed WIN (earlier TP)
**Lifecycle:** OPEN actionable (intraday)

**Setup (swing):** Score 79.1 swing, 66.1 intraday. +22.14% 24h, RS vs BTC +21.31%, 7d return +72.73%. Entry zone 0.1131-0.1177 (swing), invalidation 0.1075. TP1: 0.1299, TP2: 0.1401, TP3: 0.1502.

- Price at 0.1197 at report time (above entry zone by ~1.7%). Needs pullback.
- OI +2.39% (intraday) / +28.77% (scalp) — fresh positioning, NORMAL crowding
- Funding: neutral (5e-05 MEXC). Clean derivatives — best in universe.
- news_supported flip today (0→1 in label refresh). Momentum breakout basket (swing).
- 7d return +72.73% — multi-day RS leader, not just 24h spike.
- Volume: below average (0.12x) — organic move, not volume-driven frenzy.
- NOT chasing at 0.1197: need pullback to 0.1131-0.1177 zone.
- **Verdict: BEST LONG WATCH.** Wait for pullback into 0.1131-0.1177 zone + BTC stable above $60K. This is the swing setup for Asia session. Do not enter at market above 0.1177. Invalidation: 1h close below 0.1075.

---

### Candidate 4: ZEC/USDT — B Scalp — CATALYST WATCH

**Status:** OPEN ACTIONABLE (scalp B triggered at 451.94-455.87)
**Lifecycle:** OPEN actionable (triggered in prior cycle)

**Setup:** Score 68 (scalp), +3.96% 24h, RS vs BTC +2.99%. Entry zone 451.94-455.87, current ~457-458, resistance 469.10, support 425.28, invalidation 447.13.

- Modest move vs peers (+3.96% vs +20-40% for ZKP/THE). Not extended.
- OI -5.25% (price up + OI down = SHORT COVERING, weaker continuation quality). Funding neutral. Lower-quality derivatives signal.
- Catalyst confirmed: Ironwood upgrade proceeding (Shielded Labs July 3 statement, DailyCoin). Late July target. Delay risk from software migration remains but secondary.
- news_supported flip today. Catalyst is confirmed event (upgrade, not speculation).
- Price slightly above entry zone (457 vs 455.87 upper limit = +0.2% above). Nearly at zone.
- Chase risk: LOW relative to peers. Small price action, near entry zone.
- **Verdict: CATALYST WATCH.** Best catalyst quality in current universe. Price is close to entry zone (451-455). If BTC stable and price returns to zone, this is a low-risk catalyst play with defined invalidation at 447.13. Monitor for overnight/Asia session entry.

---

### Candidate 5: UNH — LEGAL/HEADLINE RISK — MANDATORY AVOID

**Status:** A→C stocks intraday (demoted: DOJ legal risk + market closed)
**Lifecycle:** NO ENTRY / LEGAL RISK / planning only until Monday

**Raw score:** 76.69/100. Final tier: C (market_closed_intraday_planning_only + sec_doj cap).

**LEGAL/HEADLINE RISK CONFIRMED:**
- DOJ Probe Extends to Optum Rx Medicare Billing Practices (WSJ via FierceHealthcare — today's catalyst events)
- DOJ Expands Probe Into UnitedHealth Prescription and Payment Practices (PYMNTS — today's catalyst events)
- Two independent DOJ probe sources confirmed today.

**Final verdict: AVOID.** Do not enter UNH until DOJ probe formally resolved. Score irrelevant — active DOJ investigation overrides all technical signals. Even when stocks market reopens Monday July 6, this signal remains AVOID.

**Note:** JPM A-tier signals (score 84, long) do not carry legal risk. The JPM headline ("Charlie Javice scammed JPMorgan") positions JPM as the VICTIM of fraud — no legal risk to the company. JPM long remains a planning-level candidate for Monday open (financials sector strongest, XLF 94.68 raw score).

---

## 8. Best Candidates Ranked

No clean new entry appropriate at 21:39 EEST (late session, most alts above entry zones).

| Rank | Symbol | Side | Status | Entry Trigger | Confidence |
|---|---|---|---|---|---|
| 1 | RIF/USDT | Long | BEST WATCH | Pullback to 0.1131-0.1177 + BTC >$60K | Medium-high |
| 2 | ZEC/USDT | Long | CATALYST WATCH | Return to 451-455 zone + BTC stable | Medium |
| 3 | TIA/USDT | Long | SECONDARY WATCH | Pullback to 0.3939-0.3976 + BTC stable | Medium |
| 4 | WLD/USDT | Long | SECONDARY WATCH | Pullback to 0.4244-0.4280 + BTC stable | Medium |
| 5 | WLFI/USDT | Short | CONDITIONAL ONLY | BTC 1h close <$60K + failed retest | Low (against current tape) |

**Excess candidates (not top 5):** HMSTR (short covering, weaker), MANA (OI +52.91% elevated), ZKP (too crowded late session), THE (extreme crowding), NEAR (C-tier), ARPA (OI +265%, extreme).

---

## 9. Avoid / No Trade

**This window (21:30 → next cycle ~22:30):**
- No new scalp entries — late session; scalp playbook low confidence (PF 0.14/14d)
- No new THE or ZKP longs — OI expansion +110-127%, negative funding = squeeze risk
- No ADA entries — >2ATR overextended, high risk penalty
- No UNH entries — DOJ/SEC active probe
- No HYPE entries (any mode) — $630M unlock July 6
- No new ARPA entries — OI +265% extreme crowding
- Stocks market closed (planning only until Monday)

**This is a late-session verdict only. Scanning continues, tracking continues, paper tracking continues. The system does not stop.**

---

## 10. Main Risks

1. **BTC bounce quality unconfirmed:** $221M ETF inflow = single session after 10-day outflow streak. BTC touched 21-month lows sub-$58K this week. F&G=21 (Fear) = crowd not convinced. Bounce needs follow-through Monday.
2. **Crowded altcoin longs:** ZKP/THE/MANA/ARPA OI expansion +52-265% with negative funding. Crowded longs unwind fast if BTC reverses. THE is highest risk (OI +127%).
3. **HYPE $630M unlock July 6 (3 days):** Avoid all HYPE. Monitor whether HYPE signals are properly prevented from Telegram alerts.
4. **18 untracked alerts (rising):** 13→18 in 3 hours. Each is a Telegram alert with no tracking ID → PnL blindspot. Count worsening.
5. **Stocks intraday DB locked:** Cycle 08 step 20 failed. Concurrent access between stocks_monitor and intraday CLI. May cascade to future cycles.
6. **ETH/BTC = 0.027942 (historically low):** Market is BTC-dominated. Altcoins lack independent ETH-led narrative strength.
7. **Scalp playbook deteriorating:** PF 0.14 over 14d. Low-confidence overlay active. Scalp signals are data-collection mode only.

---

## 11. Action Plan — Next 4 Hours (21:39 → 01:39 EEST)

1. **Watch RIF/USDT for pullback** into 0.1131-0.1177 (swing entry zone). Best setup if BTC holds $60K. Invalidation: 1h close below 0.1075.
2. **Watch ZEC/USDT** — if price returns to 451-455 zone, consider catalyst play. Invalidation: 1h close below 447.13.
3. **Watch TIA/WLD** (secondary) — both news_supported today; pullbacks to respective entry zones (TIA: 0.3939-0.3976, WLD: 0.4244-0.4280).
4. **Avoid THE/ZKP/MANA new entries** — extreme crowding, late entry.
5. **No scalps** until next cycle (~22:30-23:00 EEST).
6. **Key BTC level: $60,000** — 1h close below = shift to wait/caution.
7. **Stocks Monday planning:** XLF (94.68), JPM (93.06), XLV (91.32), COIN (90.88), AAPL (84.45) — strongest raw scores (all demoted to C today; re-evaluate Monday). UNH → AVOID.
8. **Do not re-enter HYPE** in any mode. July 6 unlock.

---

## 12. Final Verdict per Mode

| Mode | Verdict | Notes |
|---|---|---|
| Crypto Scalp | AVOID NEW ENTRIES (21:39+) | PF 0.14/14d; late session; resume next cycle |
| Crypto Intraday | WAIT-FOR-TRIGGER | RIF/TIA/ZEC pullbacks only; avoid THE/ZKP |
| Crypto Swing | WATCH / PULLBACK ONLY | Best mode (PF 7.10); RIF primary; ZEC catalyst secondary |
| Stocks Intraday | CLOSED / PLANNING ONLY | No entry until Monday July 6; plan JPM/XLF/AAPL/COIN |
| Stocks Swing | STALE DATA — EXCLUDED | 29.5h old; no verdict until Monday cycle |
| Stocks Invest | STALE DATA — EXCLUDED | 29.5h old; excluded |

**Paper-shadow A/B:** B outperforms A (+24.13R forward, 8d). NOT_READY (4/6 gates, forward window <14d, DATA_GAP 41%). No promotion action.

---

## 13. Sources

- [Bitcoin ETF News: Inflows Hit $221M as 10-Day Outflow Streak Ends](https://99bitcoins.com/news/bitcoin-btc/bitcoin-etf-news-inflows-outflow-streak-ends/) — 99bitcoins.com, 2026-07-03
- [Zcash Ironwood Upgrade Targets July Activation After Critical Orchard Fix](https://dailycoin.com/zcash-ironwood-upgrade-targets-july-activation-after-critical-orchard-fix) — DailyCoin, 2026-07-03
- [Zcash Ironwood Timeline Pressured by Software Migration](https://cointelegraph.com/news/zcash-ironwood-upgrade-possible-delay-infrastructure-readiness) — Cointelegraph, 2026-07-03
- [Bitcoin Price Tags $62.3K Nine-Day High](https://cointelegraph.com/) — Cointelegraph, 2026-07-03 (via scalp report)
- [BlackRock BTC Outflows 10 Consecutive Days — 35,980 BTC ($2.24B)](https://arkm.com/explorer/entity/blackrock) — Lookonchain (t.me), 2026-07-03 (via scalp report)
- [DOJ Probe Extends to Optum Rx Medicare Billing Practices — WSJ](https://www.fiercehealthcare.com/) — FierceHealthcare, 2026-07-03 (via catalyst events)
- [DOJ Expands Probe Into UnitedHealth Prescription and Payment Practices](https://www.pymnts.com/) — PYMNTS, 2026-07-03 (via catalyst events)
- Internal: `cycle_08_20-24_summary.md`, `2026-07-03_17-31_scalp_report.md`, `2026-07-03_17-36_intraday_report.md`, `2026-07-03_12-59_swing_report.md`, `2026-07-03_18-35_stocks_intraday_report.md`

---

## 14. Fix Requests / TODO

### TODO-untracked-alerts-rising
- **issue:** Untracked legacy crypto alerts increased from 13 → 18 in ~3 hours (+5 today). Each is a Telegram alert with no proposed_signal match → PnL blindspot.
- **evidence:** `cycle_08 step 28: 18 untracked legacy crypto alert(s). These were sent to Telegram but will NOT contribute to PF / winrate / avgR. Symbols: TLM, ETH, ALLO, THE, PUMP, BTC, NEAR etc.`
- **suggested manual fix:** Investigate whether Telegram alerter fires before `proposed_signals` is written for certain modes (scalp, swing). Cross-check alert timestamps vs proposed_signal insertion timestamps for today's 18 alerts. Check ±6h matching window.
- **priority:** high
- **first observed:** 2026-07-02 (recurring; daily count now at highest: 18)

### TODO-stocks-intraday-db-locked
- **issue:** Stocks intraday CLI (step 20) failed with `OperationalError: database is locked` in cycle 08. The error occurs in `save_events()` during earnings event storage.
- **evidence:** `cycle_08_20-24_summary.md step 20: [FAIL] exit=1, 122.2s → OperationalError: database is locked at src/storage/sqlite.py:525 save_events()`
- **suggested manual fix:** Investigate concurrent DB access between `stocks_monitor` background process (pid=12516) and stocks intraday CLI. Add WAL mode or exponential-backoff retry wrapper for events table write in `src/storage/sqlite.py`.
- **priority:** high
- **first observed:** 2026-07-03 20:43 EEST

### TODO-scalp-playbook-performance
- **issue:** Crypto scalp playbook deteriorating: 1W/7L over 14d, PF 0.14. TP1/2h horizon mismatch caps capture (avg MFE +0.54R vs TP1 ~1.86R).
- **evidence:** `scalp_report: low_confidence_scalp overlay active; known failure mode: TP1 distance ~1.86R vs typical captured MFE 0.54R — mean reverts before TP`
- **suggested manual fix:** At 20 closed A/B scalp signals, re-audit scalp playbook. Consider reducing TP1 to 0.5-0.7R (nearer to avg MFE) or implementing a "partial at MFE" rule. Review `src/playbooks/crypto_scalp.py` TP ladder.
- **priority:** medium
- **first observed:** 2026-06-25 (recurring)

### TODO-stocks-signal-performance-negative
- **issue:** Stocks A/B: PF=0.33, WR=3.1%, totalR=-3.33R (7d). All-tier: PF=0.452, totalR=-17.00R. System flag active. DATA_GAP_LATE cohort 41% of forward signals excluded from edge.
- **evidence:** `cycle_08 step 26 signal-stats stocks: HEADLINE A/B sample=32, wins=1, losses=6, PF=0.333, avgR=-0.133, totalR=-3.3333`
- **suggested manual fix:** Review stocks intraday scoring. Compare stocks shorts (paper 30d: +10.7R/WR=50% in risk_off) vs longs (net negative). Consider whether current long bias in stocks intraday is miscalibrated. Also audit DATA_GAP_LATE 41% exclusion — this is a large blind spot in forward evidence.
- **priority:** medium
- **first observed:** 2026-07-01 (worsening trend)
