# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:20 EEST

> **Advisory only / no auto-trade. Thursday July 2, 2026. Slot: pre-US-open decision review (16:20 EEST). Crypto: LIVE. Stocks: PRE-MARKET — RTH opens 16:30 EEST / 09:30 ET in ~10 minutes.**

---

## 1. Executive Summary

**Slot: pre-US-open decision review — advisory only / no auto-trade.**

BTC has consolidated to **~$58,620–$59,400** after yesterday's bounce from the 652-day low ($57,950). The bounce to ~$61k has faded; BTC sits below the 20-day EMA (~$62,450) in range/chop. Crypto regime is **neutral/chop at scalp-intraday TF**, **bullish trend at swing TF** (altcoin breadth 78% above EMA20). F&G = 19 (Extreme Fear). VIX = 16.0. Stocks regime: **bullish** (4/4 indices uptrend).

**CRITICAL — 10 MINUTES TO US OPEN:**
- **NFP June 2026 releases at 8:30 AM ET (16:30 EEST)** coinciding with the US cash open — binary gap risk.
- **TSLA Q2 deliveries due today** (consensus 406k, Goldman at 420k) — binary stock event.
- **DO NOT CHASE** any pre-market crypto or equity move without RTH confirmation post-NFP.

**Ongoing flags:**
- **⚠️ UNH DOJ CRIMINAL PROBE EXPANDED (4th review):** DOJ now covers Medicare Advantage billing + Optum Rx + physician reimbursement. Multi-front criminal investigation. UNH and XLV → **LEGAL RISK / AVOID all modes**.
- **⚠️ TLM B-tier scalp: ENTERED-UNRESOLVED + Binance delisting monitoring (May 22):** No new TLM entries. Existing position needs human review for exit planning.
- **Catalyst mapping: estimated ~65-70% unmapped** → use catalyst layer as context only, not final decision filter.

Crypto signal stats: dramatically improved this cycle — PF 1.95, +18.1R weekly (was -8R at 11:39 review). 20 B-tier crypto signals active (all longs). 20 C-tier stocks signals (all WAITING, market-closed demotion). No new crypto A-tier. Stocks B-tier PF=0.27, WR=8% — poor; maintain caution.

**Decision for the open:** WAIT-FOR-TRIGGER. NFP direction determines whether NEAR/BCH longs activate or DYDX short extends. No entries before first 15-30 min post-NFP. Scanning and data collection continue normally.

---

## 2. Data Used

| Source | File / CLI | Age at 16:20 EEST | Status |
|--------|-----------|-------------------|--------|
| Scheduler cycle_06 | `cycle_06_15-37_summary.md` | 12 min | **FRESH** |
| Crypto scalp | `2026-07-02_12-43_scalp_report.md` (UTC=15:43) | 37 min | **FRESH** |
| Crypto intraday | `2026-07-02_12-48_intraday_report.md` (UTC=15:48) | 32 min | **FRESH** |
| Crypto swing | `2026-07-02_13-01_swing_report.md` (UTC=16:01) | 19 min | **FRESH** |
| Stocks intraday | `2026-07-02_12-55_stocks_intraday_report.md` (UTC=15:55) | 25 min | **FRESH** |
| Stocks swing | `2026-07-02_13-03_stocks_swing_report.md` (UTC=16:03) | 17 min | **FRESH** |
| Active signals crypto | CLI active-signals (cycle 06 step 27) | 12 min | 20 B-tier |
| Active signals stocks | CLI active-signals (cycle 06 step 29) | 12 min | 20 C-tier |
| Signal stats crypto | CLI signal-stats (cycle 06 step 28) | 12 min | n=97, PF=1.95 +18.1R |
| Signal stats stocks | CLI signal-stats (cycle 06 step 30) | 12 min | A/B n=25, PF=0.27 −5.8R |
| Untracked legacy alerts | CLI (cycle 06 step 32) | 12 min | **NONE — clean** |
| Market dashboard | cycle 06 step 15 | 12 min | crypto_mode=trend, stocks=risk_on |
| BTC price / market context | WebSearch (CryptoTimes, KuCoin) | live | ~$58,620–$59,400 |
| UNH DOJ probe | WebSearch (Benzinga, PYMNTS, FierceHealthcare) | live | Expanded to Optum Rx + physician reimbursement confirmed |
| NFP June 2026 schedule | WebSearch (BLS, Kiplinger) | live | Due TODAY 8:30 ET, expect +110k |
| TSLA Q2 deliveries | WebSearch (TechTimes, Electrek) | live | Due TODAY, consensus 406k |
| TLM delisting status | WebSearch (CoinMarketCap) | live | Monitoring active, price ~$0.0172 confirmed |
| Previous review | `OPUS_ENRICHED_REVIEW_AUTO_2026-07-02_1139.md` | 4.7h ago | Loaded |

**External web research:** Operational — 5 searches executed, all returned usable results.

---

## 3. Scheduler / Data Freshness

- **Cycle 06:** Started 15:37 EEST, finished 16:08 EEST — **36/36 OK, 0 failed**. Runtime 31 min.
- **Freshness:** 12 min since completion — **PASSES 3-hour defer threshold. NOT DEFERRED.**
- **Pre-cycle tracking:** 527 signals checked, 327 TP hits processed, 0 stopped, 0 expired.
- **Post-cycle tracking:** 555 signals checked, 324 TP hits, 0 expired. Revalidation: 53 checked, **14 stale, 3 moved_away**.
- **All reports:** < 40 min old → **FRESH**.
- **Intelligence:** derivatives_sparse (funding/OI numeric history thin); squeeze phases 109 symbols cached.
- **Onchain:** interface_ready_config_missing (persistent blindspot).
- **Social attention:** MISSING — Reddit 403 blocked (persistent).
- **Catalyst mapping:** ~65-70% unmapped (estimated, consistent with prior 69.4%) → **use as context only**.
- **Untracked legacy alerts:** NONE — clean.
- **Paper monitor:** Open actionable=2, Waiting=11, Entered unresolved=31, Review/Shadow=201, No-entry/stale/moved-away=61, Needs review=0. Closed today: 327W / 21L / 0 flat.
- **Paper portfolio (Bybit fees):** $6,026 / +20.5% on $5,000. Paper shadow forward-only: B +17.21R vs A -63.38R (B gate: NOT_READY 4/6, 7d < 14d requirement).

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-02 16:20 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_fresh"],
      "data_missing": ["social_attention", "onchain_config", "live_orderbook", "liquidation_heatmaps"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Cycle 06 finished 16:08 EEST — 12 min ago, 36/36 OK",
        "All reports < 40 min old (FRESH)",
        "Catalyst: 643 events (swing report), 4 baskets",
        "Reddit social blocked 403 — persistent",
        "Onchain: interface_ready_config_missing",
        "Untracked legacy alerts: NONE"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["chop", "mixed", "wait_for_trigger", "longs_preferred"],
      "data_missing": ["nfp_result", "post_open_price_action"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto scalp/intraday: range/chop neutral; BTC transition_up, ETH transition_up",
        "Crypto swing: bullish trend, altcoin breadth 78% above EMA20",
        "BTC ~$58,620-$59,400 web; pulled back from $60,123 at 11:39; below 20d EMA $62,450",
        "F&G=19 (Extreme Fear), VIX=16.0",
        "Stocks: bullish 4/4 indices uptrend, breadth 100% above EMA20",
        "NFP June 2026 in 10 min (8:30 ET = 16:30 EEST) — binary directional risk",
        "TSLA Q2 deliveries today — binary stock event",
        "Macro risk score 51/100 (swing)"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.62,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported"],
      "data_missing": ["unmapped_pct_exact", "post_nfp_catalyst"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "643 unique events (swing), 4 baskets; ~65-70% unmapped estimated",
        "Label refresh: ETH and ZEC gained news_supported (0→1)",
        "ai_narrative: NEAR/RENDER/TAO/FET (fresh <6h)",
        "momentum_breakout: BREV/TLM/SYN (fresh <1h)",
        "SOL: token_unlock risk (July) — bearish overlay",
        "DOJ Optum Rx: legal_risk basket, no crypto symbol mapped",
        "TSLA Q2 deliveries: binary catalyst at open",
        "BTC: bounce from 652-day low + capitulation signals — mixed"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["data_unavailable", "oi_supports", "squeeze_risk"],
      "data_missing": ["full_oi_numeric_history", "liquidation_heatmaps", "exchange_cvd"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "TLM: OI +133.55%, funding -0.00643 (negative), crowding unknown — elevated",
        "BREV: OI +182.16%, funding -0.00894 (negative), crowding unknown — elevated",
        "DYDX: price down + OI up, fresh shorts pressing; funding -0.000270",
        "BCH: price up + OI up; long/short 2.366 — skewed long",
        "INJ: price down + OI up, fresh shorts pressing; +10.47% OI",
        "Phase dist: 35 post-unwind-chop, 19 build-up, 7 squeeze-expansion, 4 unwind"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["clean_retest", "chase_risk", "overextended"],
      "data_missing": ["live_15m_chart", "orderbook_depth"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "NEAR: B-tier swing, entry zone 1.919-1.933, current ~1.936 — within <1 ATR (ATR 0.0328)",
        "BCH: B-tier swing, entry zone 215.91-217.29, current ~217.90 — within 1 ATR (3.064)",
        "TLM: scalp triggered, +79.87% 24h, OI 133% — extended; do not add",
        "SOL/ADA/XRP/ETH/ZEC: >2 ATR from EMA20 — chase filter applied, rejected",
        "BTC ATR-percentile=80 (elevated) — wider intraday swings at NFP open expected"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.80,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "review_shadow"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Paper monitor: OPEN actionable=2, WAITING=11, ENTERED UNRESOLVED=31, REVIEW/SHADOW=201, NO-ENTRY/STALE/MOVED-AWAY=61, NEEDS REVIEW=0",
        "Active crypto: 20 B-tier (all longs); TLM scalp=triggered/entered",
        "Active stocks: 20 C-tier (demoted from market-closed + swing watchlist-only penalty)",
        "TLM scalp ENTERED-UNRESOLVED + Binance delisting monitoring — flag for human review",
        "Closed today (paper): 327W / 21L / 0 flat",
        "Post-cycle revalidation: 14 stale, 3 moved_away identified"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.82,
      "reason_codes": ["headline_risk", "legal_risk", "manual_review", "reduce_risk"],
      "data_missing": ["today_realized_pnl", "live_exposure"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "UNH: DOJ criminal probe expanded to Optum Rx + physician reimbursement (multi-source confirmed)",
        "XLV: healthcare sector exposure to UNH DOJ risk",
        "TLM: delisting monitoring (May 22) + scalp entered — capital at exchange-removal risk",
        "TSLA: Q2 deliveries binary event (consensus 406k) — no new positions before result",
        "NFP at 16:30 EEST: binary event at US open — gap risk in both directions",
        "BTC: F&G=19 Extreme Fear, June -20.48% worst month since 2022",
        "Stocks swing 48h audit: 0W/12L — capped to watchlist-only",
        "Stocks A/B weekly: PF=0.27, WR=8%, -5.8R — entry caution mandatory"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.70,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": ["intraday_12h_breakdown", "regime_conditional_stats"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto A/B weekly: n=97, PF=1.95, +18.1R, WR=23.3% — improvement from -8R at 11:39",
        "Crypto setup=long_breakout: n=78, PF=3.0, +19.9R (strong)",
        "Crypto setup=momentum: n=13, PF=0.58, -3.3R (LOSING bucket)",
        "Stocks A/B: n=25, PF=0.27, WR=8%, -5.8R (alarming)",
        "Stocks B-tier: PF=0.21, WR=5%",
        "Paper shadow B forward 7d: B +17.21R vs A -63.38R; B net fees negative (gate NOT_READY)"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.73,
      "reason_codes": ["wait_for_trigger", "legal_risk", "longs_preferred"],
      "data_missing": ["nfp_result", "post_open_confirmation"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "NFP at 16:30 EEST = binary event; all new entries deferred until post-open confirmation",
        "BTC ~$58.6-59.4k, chop regime; bounce from 652-day low not yet confirmed as sustained trend",
        "Best long: NEAR (B-tier swing, <1 ATR from entry, catalyst-backed, AI narrative)",
        "Best short: DYDX (sell-the-news -26%, fresh short OI, dead-cat bounce watch)",
        "Avoid: UNH/XLV (multi-front DOJ criminal), TLM (delisting monitoring + entered)"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.73,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": {
      "symbol": "NEAR",
      "trigger": "Pullback to 1.919-1.933 after NFP confirms positive; BTC holding ≥$57,950",
      "reason": "B-tier swing, <1 ATR from entry zone, AI narrative basket, upgrade catalyst confirmed"
    },
    "best_short_candidate": {
      "symbol": "DYDX",
      "trigger": "Dead-cat bounce rejection: 1h close below intraday bounce high after failed recovery",
      "reason": "Sell-the-news -26%, fresh short OI building, no recovery catalyst"
    },
    "best_catalyst_candidate": {
      "symbol": "NEAR",
      "trigger": "Protocol upgrade catalyst + AI narrative basket; pullback to 1.919 entry post-NFP",
      "reason": "Freshest confirmed catalyst; news_supported label flipped 0→1 this cycle"
    },
    "avoid_candidate": {
      "symbol": "UNH",
      "reason": "DOJ criminal probe spans Medicare Advantage + Optum Rx + physician reimbursement; multi-front criminal investigation"
    },
    "operator_action": "wait_for_trigger",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|-------|---------|------------|-------------|-----------------|
| data_quality | **ok** | 0.85 | scheduler_fresh, report_fresh | advisory_only |
| market_regime | **caution** | 0.72 | chop, mixed, wait_for_trigger, longs_preferred | advisory_only |
| catalyst_narrative | **caution** | 0.62 | mapping_weak, fresh_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | **caution** | 0.55 | data_unavailable, oi_supports, squeeze_risk | advisory_only |
| technical_entry | **caution** | 0.65 | clean_retest, chase_risk, overextended | advisory_only |
| execution_lifecycle | **ok** | 0.80 | open_actionable, waiting_for_entry, entered_unresolved | advisory_only |
| risk_manager | **caution** | 0.82 | headline_risk, legal_risk, manual_review | advisory_only |
| playbook_performance | **caution** | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | **caution** | 0.73 | wait_for_trigger, legal_risk, longs_preferred | advisory_only |

---

## 4. What Changed vs Previous Review (11:39 EEST)

| Item | Previous (11:39) | Current (16:20) | Change |
|------|-----------------|-----------------|--------|
| BTC price | ~$60,123 (+2.45%) | ~$58,620–$59,400 | **↓ Pulled back ~$1,000–$1,500** |
| Crypto regime | range/chop | range/chop (scalp/int) / bullish trend (swing) | Same chop at execution TF |
| Crypto signal stats | n=72, PF=0.70, −8R | n=97, PF=1.95, +18.1R | **⬆ MAJOR IMPROVEMENT** |
| Active crypto signals | 21 B-tier | 20 B-tier | Largely unchanged |
| Active stocks signals | 50 C-tier + AMD B-tier | 20 C-tier | Reduced (market session) |
| UNH DOJ probe | Medicare fraud probe (3rd review) | **Expanded to Optum Rx + physician reimb** | **⬆ Escalated** |
| Catalyst events | 505 unique (scalp run) | 643 unique (swing run) | +138 events this cycle |
| NFP event | Not surfaced as immediate risk | **NFP at 16:30 EEST — 10 min** | **NEW CRITICAL EVENT** |
| TSLA deliveries | Mentioned as upcoming | **Due TODAY** | **NEW BINARY EVENT** |
| ZEC catalyst | no news_supported | news_supported flipped 0→1 | New catalyst label |
| NEAR catalyst | no news_supported | news_supported flipped 0→1 | New catalyst label |
| TLM price discrepancy | CoinGecko $0.000885 vs Binance $0.0172 | CMC confirms ~$0.0172 (CG data error likely) | Partially resolved |

**Confirmed / unchanged:**
- UNH LEGAL RISK / AVOID (persistent, now stronger)
- DYDX short thesis (sell-the-news holding)
- Catalyst mapping weak (persistent)
- TLM delisting monitoring (unresolved)
- Reddit social blocked (persistent)
- Onchain config missing (persistent)

---

## 5. Catalyst Coverage

- **Total events:** 643 (swing report); 433 (cycle step 4 scan)
- **Baskets:** 4 — `ai_narrative`, `perps_dex_narrative`, `delisting_thin_liquidity`, `momentum_breakout`
- **Estimated unmapped:** ~65-70% (consistent with prior 69.4%)

> **⚠️ Catalyst mapping weak this run — use as context only, not final decision filter.**

**Top unmapped events with market impact:**
1. `[legal_risk]` DOJ criminal probe extends to Optum Rx *(impacts UNH, XLV — NOT mapped to symbol)*
2. `[exchange_listing]` Binance Futures launches TradFi perpetual contracts *(basket only)*
3. `[exploit_hack]` Tokenized Google stock inflated 7,700% in DeFi exploit *(basket only)*

**Symbol-mapped catalyst highlights:**
- **NEAR:** protocol upgrade +5% rally (positive); news_supported flipped 0→1 this cycle
- **ETH:** news_supported flipped 0→1 this cycle
- **ZEC:** news_supported flipped 0→1 this cycle (catalyst source — check news_items)
- **SOL:** governance framework + July token unlock pressure (dual-direction)
- **TLM/SYN/BREV:** momentum_breakout basket (fresh <1h)
- **HYPE:** perps_dex_narrative basket (fresh <6h)

---

## 6. Market Landscape

### Market Mood / Risk Routing

**Crypto mood:** chop/mixed — range/chop at scalp-intraday TF; bullish trend at swing TF. BTC ~$58.6-59.4k, bounced from 652-day low ($57,950) but no sustained trend established. F&G=19 (Extreme Fear). Altcoin breadth bifurcated: 53.85% (scalp/int) vs 78.05% (swing).

**Stocks mood:** bullish pre-market (4/4 indices uptrend, VIX 16, breadth 100%) — **but NFP BINARY IN 10 MINUTES.**

**Dominant narrative:** Post-June-drawdown bounce attempt; AI narrative rising (NEAR/TAO/RENDER leading); sell-the-news in crypto (DYDX −26%); healthcare DOJ legal risk (UNH/XLV); US jobs data coincides with market open.

**Preferred side now:** **WAIT-FOR-TRIGGER** (pre-NFP — no directional bias until 16:30 EEST)
- IF NFP ≥ 110k: risk-on → longs after 15-30min RTH (NEAR pullback to 1.919–1.933; BCH pullback to 215.91–217.29)
- IF NFP < 90k: risk-off → DYDX short on failed bounce; BTC watch $57,950 support; no stock longs

**Best long candidate:** NEAR (B-tier swing, close to entry, catalyst-backed, AI narrative)
**Best short candidate:** DYDX (sell-the-news -26%, fresh short OI, dead-cat bounce setup)
**Avoid:** UNH, XLV (multi-front DOJ criminal); TLM (delisting monitoring + entered); chasing overextended moves (SOL/ADA/XRP/ETH/ZEC all >2 ATR from EMA20)

**What would change the view:**
- BTC holds $58,500+ after NFP → longs activate (NEAR/BCH)
- BTC breaks $57,950 on 1h close → short-side bias only
- NFP ≥ 150k surprise → strong risk-on, more aggressive long stance
- NFP ≤ 75k → risk-off, shift to DYDX short + defensive
- TLM delisting confirmed → urgent exit required

---

## 7. Candidate Deep Dives

### 7.1 TLM/USDT — B-tier Scalp ENTERED-UNRESOLVED — NEEDS HUMAN REVIEW

**Tier/Mode:** B-tier, scalp — status: triggered (entered)
**Direction:** Long (entered, UNRESOLVED)

**Current situation:** TLM scalp was triggered this cycle — entry taken at market price in the scalp zone. Signal now ENTERED-UNRESOLVED.

**Contradiction risks:**
- Binance delisting monitoring active since May 22, 2026 (CoinMarketCap confirmed). Not yet confirmed as full delisting but risk is elevated.
- +79.87% 24h move at time of trigger — highly overextended entry
- OI +133.55%, funding -0.00643 (negative cross-venue: Bybit + MEXC both negative funding) — crowding UNKNOWN
- No fresh verified catalyst — momentum_breakout basket only (thin liquidity + pump dynamics possible)
- Previous review CoinGecko price discrepancy ($0.000885 vs $0.0172): CoinMarketCap now shows ~$0.0172 consistent with Binance — CoinGecko data appears to have been erroneous. Price appears normalized but verifying against second live source recommended.

**Price levels:**
- Entered near scalp zone; TP1: ~$0.0018; SL: 1h close below $0.0014

**VERDICT: No new TLM entries. Monitor TP1 ($0.0018) and SL ($0.0014 1h close). Delisting monitoring = elevated exit urgency. Manual review of exit plan required.**

---

### 7.2 NEAR/USDT — B-tier Swing WAITING — Best Long-Watch

**Tier/Mode:** B-tier, swing (waiting)
**Direction:** Long
**Entry zone:** 1.919–1.933 | **SL:** 1h close <1.897 | **TP1:** 1.973 | **TP2:** 2.006 | **TP3:** 2.034
**ATR:** 0.0328 | **Current price:** ~1.936

**Catalyst:** `news_items.detected_symbols_json` → NEAR has verified catalyst: "NEAR Protocol's latest upgrade could matter beyond its 5% price rally" (AMBCrypto). Label refresh flipped news_supported 0→1 this cycle. Single-source, importance 0.75.

**Narrative:** ai_narrative basket primary (NEAR/RENDER/TAO/FET, fresh <6h). Protocol governance upgrade provides fundamental catalyst beyond pure momentum.

**Derivatives:** price up + OI down (short covering, weaker continuation quality). Funding -0.000385. Not a negative squeeze threat. L/S ratio 0.957 (shorts slightly dominant — short covering accelerates on upward move).

**Distance from entry:** Current ~1.936 vs entry top 1.933 → +0.003 above zone (~0.1 ATR). **Within reach on any minor pullback.**

**Chase check:** NOT extended — 24h +8.46%, RS vs BTC +3.6%, healthy and not overextended. Entry now requires <0.5 ATR pullback. No chase required.

**Mood alignment:** AI narrative + confirmed catalyst + B-tier (close to entry) = well-aligned with longs-preferred routing.

**VERDICT: BEST LONG-WATCH. Entry ONLY after NFP at 16:30 EEST + BTC holds $57,950 + price pulls back into 1.919–1.933. Invalidation: 1h close <1.897.**

---

### 7.3 BCH/USDT — B-tier Swing+Scalp WAITING — Secondary Long-Watch

**Tier/Mode:** B-tier, swing + scalp (waiting)
**Direction:** Long
**Entry zone (swing):** 215.91–217.29 | **SL:** 1h close <214.22 | **TP1:** 220.96 | **TP2:** 224.03 | **TP3:** 227.09
**ATR:** 3.064 | **Current price:** ~217.90

**Catalyst:** No fresh verified catalyst. No news_items entries. Catalyst score 6.8/10 (category default). No basket membership.

**Derivatives:** price up + OI up (fresh positioning confirms trend). Funding 3.2e-5 (neutral). L/S ratio 2.366 (longs dominating — monitor crowding).

**Distance from entry:** ~217.90 vs 217.29 (zone top) → +$0.61 above zone (~0.2 ATR). **Actionable on any pullback.**

**Chase check:** 24h +7.08%, RS vs BTC +2.2% — moderate RS, not leading. Not extended.

**Risk note:** BCH L/S 2.366 skewed long — if BTC drops post-NFP, longs may exit, amplifying BCH decline. No catalyst = momentum-only in chop = known failure mode (WR=23%/PF=0.70 in chop).

**VERDICT: SECONDARY LONG-WATCH. Enter AFTER NFP confirmation + BTC holds, AND after NEAR entry confirms first. Lower conviction than NEAR due to no catalyst.**

---

### 7.4 UNH + XLV — LEGAL RISK / AVOID (all modes)

**Tier:** C-tier stocks (demoted from A-tier 80.11 / B-tier 72.93 due to market-closed demotion)

> ⚠️ **LEGAL/HEADLINE RISK — UNH: DOJ criminal probe (multi-front).**

**DOJ probe scope (confirmed multi-source):**
1. DOJ Criminal Division: Medicare Advantage billing fraud (original, ongoing)
2. DOJ Criminal Division: Optum Rx prescription practices (new expansion) — Source: Benzinga, PYMNTS
3. DOJ Criminal Division: physician reimbursement practices (new expansion) — Source: FierceHealthcare

**This is a multi-front criminal investigation.** Not a civil regulatory inquiry — criminal division involvement elevates legal risk substantially. UNH has cooperated but no settlement announced.

**XLV:** UNH represents ~18% of the Health Care Select Sector ETF. Healthcare is the strongest sector 20d (+8.98% vs SPY -1.82%), but UNH contamination creates headline overhang on the entire ETF.

**Note on report scores:** Stocks intraday lists UNH as "A-tier 80.11" in the table, stocks swing shows "B-tier 75.0". These are nominal scores BEFORE legal risk overlay and before market-closed demotion. **Live system correctly demotes all stocks signals to C-tier.** UNH A-tier table entry does NOT reflect live actionability.

**VERDICT: AVOID / LEGAL RISK. No long position in UNH or XLV any mode any horizon until DOJ criminal probe is resolved or closed.**

---

### 7.5 DYDX/USDT — Short-Watch (C-tier, squeeze guard applied)

**Tier/Mode:** C-tier only (B-tier capped due to `short_bounce_guard + exhaustion`); intraday
**Direction:** Short watch only
**Setup:** Dead-cat bounce rejection after -26% sell-the-news

**Sell-the-news thesis:**
- dYdX launched Arcus DEX on Robinhood Chain — major anticipated event → sell-the-news complete
- 24h: −25.67% to −26.18% (scalp/intraday/swing reports consistent)
- OI: price down + OI up = fresh shorts pressing (bearish structure confirmed)
- Funding: -0.000270 to -0.000291 (slightly negative — shorts paying small premium, not extreme)
- L/S ratio: 1.096 (barely longs-dominant — near neutral; fresh shorts will tip this)

**Entry logic:** NOT a chase-the-dump short. Requires dead-cat bounce FIRST, then rejection.
- Watch for: intraday bounce to resistance level, followed by 1h close below bounce high
- If BTC rips post-NFP → DYDX may bounce significantly; WAIT for bounce to peak and reject before entering short

**Squeeze risk:** System capped DYDX to C due to `short_bounce_guard`. With L/S at 1.096 and NFP risk, short squeeze if risk-on event is real.

**No recovery catalyst:** Arcus launch event completed. No upcoming positive catalyst identified.

**VERDICT: BEST SHORT-WATCH. Do not chase -26% move. Wait for dead-cat bounce and 1h rejection. Risk-off NFP → higher conviction. Risk-on NFP → wait longer for bounce to exhaust before shorting.**

---

### Excess Candidates (noted, not full deep-dive)

- **SYN/USDT** (B-tier scalp+swing, entry zone 0.5459–0.5643 vs current ~0.5724, no catalyst): tertiary long-watch after NEAR/BCH
- **JPM** (C-tier stocks swing score 90.34, highest stocks score this cycle): best stocks candidate for RTH entry after NFP + first 15-30min confirmation. No legal risk detected.
- **TSLA** (C-tier swing, Q2 deliveries today consensus 406k): binary catalyst at open; no pre-positioning.

---

## 8. Best Candidates Ranked

*All entries deferred until after NFP at 16:30 EEST. No pre-NFP positions.*

| Rank | Mode | Symbol | Side | Entry trigger | Levels |
|------|------|---------|------|--------------|--------|
| 1 | Long-watch | NEAR | Long | NFP ≥ 110k + BTC ≥$57,950 + price pulls back into zone | Entry: 1.919–1.933 · SL: 1h close <1.897 · TP1: 1.973 |
| 2 | Short-watch | DYDX | Short | Dead-cat bounce → 1h rejection below bounce high | Watch bounce high; enter on 1h close below |
| 3 | Long-watch | BCH | Long | Same as NEAR + NEAR entry confirmed first | Entry: 215.91–217.29 · SL: 1h close <214.22 · TP1: 220.96 |
| 4 | Catalyst-watch | NEAR | Long | Same as rank 1 — note catalyst layer adds conviction | Same as rank 1 |
| 5 | Catalyst-watch | TSLA | — | Q2 deliveries number: beat >406k = long; miss = short | Wait for delivery report + 15min RTH candle |

---

## 9. Avoid / No Trade

- **ALL assets: no new entries 16:20–16:30 EEST (pre-NFP window)**
- **UNH, XLV:** LEGAL RISK / AVOID — all modes, all horizons
- **TLM:** no new entries; monitor existing; delisting monitoring = elevated urgency
- **Stocks swing:** watchlist-only (48h audit: 0W/12L)
- **SOL, ADA, XRP, ETH, ZEC, ALLO, FIL, LINK:** overextended (>2 ATR from EMA20) — no chase
- **BREV:** OI +182%, funding negative, crowding unknown — WAIT for cleanup
- **Momentum bucket (PF=0.58):** do not add momentum-only positions in chop; long_breakout setup only (PF=3.0)
- Scanning continues normally. No-trade applies to new entries only.

---

## 10. Main Risks

1. **NFP binary gap (16:30 EEST):** June jobs +/- surprise; BTC range $57,950–$61k could expand quickly
2. **BTC $57,950 support:** 652-day low. Break on NFP miss → broad crypto selling; NEAR/BCH longs invalid
3. **TLM delisting confirmation:** If Binance announces confirmed removal of TLM, position needs immediate exit
4. **UNH legal escalation:** Formal charges or indictment at/near open → XLV gap risk
5. **TSLA deliveries miss (<380k):** TSLA gap-down drags QQQ/NASDAQ at open
6. **DYDX squeeze on NFP beat:** L/S 1.096 + fresh shorts → squeeze if BTC rips; wait for bounce to exhaust
7. **Crypto scalp edge low-confidence:** 23.3% WR weekly; TLM entered in low-confidence mode
8. **Stocks A/B underperformance:** PF=0.27, WR=8% — do not add new stock A/B positions in this state
9. **Catalyst mapping weak:** DOJ/Optum Rx not symbol-mapped; may miss healthcare sector risk signals

---

## 11. Action Plan — Next 4 Hours (16:20–20:20 EEST)

**16:20–16:30 EEST — STANDBY:**
- No new entries. Monitor open positions.
- TLM: alert at TP1 ($0.0018) and SL ($0.0014 1h close).
- Prepare NEAR order: limit at 1.919–1.933 (ready to activate post-NFP).

**16:30 EEST — NFP RELEASE:**
- Read NFP number immediately.
- ≥110k: activate NEAR long watch (pull to zone); BCH secondary.
- <90k: cancel all long plans; watch DYDX dead-cat for short; BTC watch $57,950.
- TSLA deliveries (when released): check vs 406k consensus.

**16:30–17:00 EEST — FIRST RTH WINDOW:**
- No entries during first 15-30min — observe structure.
- Confirm BTC direction on 15m closes.

**17:00–18:30 EEST:**
- If NFP positive: NEAR/BCH longs if price in zone + BTC held. Strict SL discipline.
- DYDX: watch for dead-cat bounce to reject; short on 1h rejection.
- TLM: monitor TP/SL; exit if delisting news breaks regardless of PnL.
- JPM (C-tier stocks): if bullish RTH after 17:00, possible entry with tight SL.

**18:30+ EEST:**
- Next auto-review (US-open reaction slot) will assess first-hour structure.
- NEAR/BCH either entered/confirmed or invalidated by then.

---

## 12. Final Verdict per Mode

| Mode | Verdict | Notes |
|------|---------|-------|
| Crypto scalp | **WAIT-FOR-TRIGGER** | Chop regime; scalp edge low-confidence; post-NFP only |
| Crypto intraday | **WAIT-FOR-TRIGGER** | NFP binary; NEAR primary candidate post-NFP; DYDX short-watch |
| Crypto swing | **WAIT-FOR-TRIGGER → NEAR** | NEAR best candidate; catalyst confirmed; BTC direction needed |
| Stocks intraday | **WAIT-FOR-RTH-CONFIRMATION** | NFP + TSLA at open; JPM watch after 15-min confirmation |
| Stocks swing | **WATCHLIST-ONLY** | 48h audit: 0W/12L; no new swing positions |
| Stocks invest | **PLANNING-ONLY** | Long-horizon; no immediate action |

---

## 13. Sources

**External:**
- BTC price context: CryptoTimes July 2, 2026 + KuCoin July 2, 2026
- UNH DOJ probe (multi-source): Benzinga (DOJ probe expands to Optum Rx) + PYMNTS (prescription/payment practices probe) + FierceHealthcare (physician reimbursement)
- TSLA Q2 deliveries: TechTimes (consensus 406,024) June 29, 2026 + Electrek (consensus 406k) June 26, 2026
- NFP schedule: BLS.gov release schedule + Kiplinger "What to Expect From June Jobs Report" July 2, 2026
- TLM price: CoinMarketCap alien-worlds latest updates (~$0.0172 confirmed)

**Internal:**
- `data/scheduled_runs/2026-07-02_default_schedule/cycle_06_15-37_summary.md`
- `data/reports/scalp/2026-07-02_12-43_scalp_report.md`
- `data/reports/intraday/2026-07-02_12-48_intraday_report.md`
- `data/reports/swing/2026-07-02_13-01_swing_report.md`
- `data/reports/stocks/intraday/2026-07-02_12-55_stocks_intraday_report.md`
- `data/reports/stocks/swing/2026-07-02_13-03_stocks_swing_report.md`
- `OPUS_ENRICHED_REVIEW_AUTO_2026-07-02_1139.md` (previous review)

---

## 14. Fix Requests / TODO

### TODO-tlm-price-mapping
- **Issue:** CoinGecko returned $0.000885 for TLM in previous review (vs Binance $0.0172, CoinMarketCap $0.0172 — ~19x discrepancy). CoinGecko likely mapped to wrong token/pair.
- **Suggested fix:** Audit the news_items price source for TLM — check if CoinGecko ticker maps to wrong TLM chain. Switch to CoinMarketCap or Binance API as primary price source for TLM.
- **Priority:** high
- **First observed:** 2026-07-02 11:39 EEST

### TODO-catalyst-healthcare-sector-mapping
- **Issue:** DOJ Optum Rx probe event stored as `[legal_risk]` basket with no symbol — directly impacts UNH and XLV but not mapped. Healthcare company name→ticker resolver missing.
- **Suggested fix:** Add name→ticker resolver: "Optum Rx" → UNH, "UnitedHealth" → UNH, "UNH" → [UNH, XLV]. Improve legal_risk basket for stocks with sector ETF propagation.
- **Priority:** high
- **First observed:** 2026-07-02 16:20 EEST

### TODO-stocks-b-tier-performance-review
- **Issue:** Stocks B-tier weekly: PF=0.21, WR=5%, -6.33R. Stocks swing 48h audit: 0W/12L. Both severely below acceptable thresholds.
- **Suggested fix:** Manual audit of stocks B-tier signal selection criteria; review entry timing (RTH confirmation), sector exclusion (tech/comm weakness), and stocks scoring thresholds. Consider raising minimum score threshold for B-tier stocks.
- **Priority:** high
- **First observed:** Ongoing; severity documented 2026-07-02 16:20 EEST

### TODO-reddit-social-blocked
- **Issue:** Reddit social blocked 403 (persistent). Social attention blindspot.
- **Suggested fix:** Replace Reddit direct API with Reddit JSON fallback (`old.reddit.com`) or add alternative (LunarCrush, Santiment, or X API).
- **Priority:** medium
- **First observed:** Persistent (multiple weeks)

### TODO-onchain-config-missing
- **Issue:** `config/onchain.yaml` missing; onchain risk update returns INTERFACE_READY_CONFIG_MISSING across all cycles.
- **Suggested fix:** Create `config/onchain.yaml` with Glassnode or Nansen API key + ETH/BTC contract addresses.
- **Priority:** medium
- **First observed:** Persistent (multiple weeks)
