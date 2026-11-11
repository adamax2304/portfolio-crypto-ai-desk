# Opus Enriched Review — Europe / Pre-US Context — Auto Cycle 11:39 EEST

**Slot:** Europe / Pre-US Context (11:30 EEST slot)
**Time:** 2026-06-26 11:39 EEST
**Date:** 2026-06-26 (Friday — weekday, crypto+stocks)
**Model:** claude-sonnet-4-6
**Advisory only — no auto-trade, no signal registration**

---

## 1. Executive Summary

**Slot: Europe / Pre-US Context — advisory only / no auto-trade.**

**Crypto regime improved from overnight "danger" to "range/chop"** — altcoin breadth recovered 19% → 41% above EMA20. BTC remains in confirmed downtrend (~$59–62K range, bounced off June 2026 lows), facing record ETF headwinds ($3.4B outflows in one week per external sources). Europe session showing tentative stabilization — not a reversal signal. Macro: Fed hawkish repricing, Treasury yields 4.82%, rate cuts pushed toward 2027. AI/tech selloff (-10%) driving crypto correlation.

**11 active crypto B-tier signals.** Three OPEN ACTIONABLE (triggered): G/USDT scalp long, BEL/USDT swing long, ETH/USDT swing long. Eight ENTERED UNRESOLVED (tp_hits, partials taken): ETH swing short, WLD scalp short, HEI intraday long, BTC swing short, HOT/AXL swing longs, MEN swing short. **WARNING: ETH/USDT has simultaneous swing short (entered) AND swing long (triggered) — contradictory. Manual review required before adding any ETH position.**

**New from Cycle 3:** G/USDT (B scalp long, RS +41.7%, volume 1.66x, no verified catalyst). BEL/USDT (B swing long, triggered). G/USDT is the session RS leader but scalp playbook is the losing bucket (PF 0.14, WR 12%).

**Catalyst mapping STRONG this cycle** (only 2 unmapped high-importance symbols: IWM, META — major improvement vs 73.9% unmapped overnight). 583 events, 5 baskets.

**MANDATORY AVOID: UNH** (DOJ criminal+civil fraud probe, shares −16%). **AVOID ADA** (Cardano wallet exploit confirmed). **Do not chase G/USDT above 0.0043** (chase risk in chop, no catalyst).

**Stocks: CLOSED (US opens 16:30 EEST, ~5h away).** All 20 stock signals are C-tier, all WAITING. Planning context only — no actionable intraday entries until after RTH open.

**ALWAYS-SCAN continues. Scanner, data collection, monitoring unchanged.**

---

## 2. Data Used

| Source | File | Generated (EEST) | Age at 11:39 | Status |
|--------|------|------------------|--------------|--------|
| Scheduler log | scheduler.log | 11:35 | 4 min | FRESH |
| Cycle 3 summary | cycle_03_10-30_summary.md | 11:35 | 4 min | FRESH (30 OK / 0 failed) |
| Scalp report | 2026-06-26_07-48_scalp_report.md | 07:48 | 3h51m | CARRY-FORWARD |
| Intraday crypto | 2026-06-26_08-06_intraday_report.md | 08:06 | 3h33m | CARRY-FORWARD |
| Swing crypto | 2026-06-26_02-25_swing_report.md | 02:25 | 9h14m | CARRY-FORWARD |
| Stocks intraday | 2026-06-26_08-33_stocks_intraday_report.md | 08:33 | 3h6m | FRESH |
| Stocks swing | 2026-06-26_02-31_stocks_swing_report.md | 02:31 | 9h8m | CARRY-FORWARD |
| Stocks invest | 2026-06-26_02-35_stocks_invest_report.md | 02:35 | 9h4m | CARRY-FORWARD |
| Catalyst integrity | CATALYST_INTEGRITY_DAILY_SUMMARY.md | 08:07 | 3h32m | FRESH |
| LLM packet | llm_analysis_packet.md | 08:07 | 3h32m | FRESH |
| Active signals CLI | src.cli active-signals x2 | 11:39 | live | LIVE |
| Signal stats | cycle 3 step 22/24 | 11:35 | 4 min | CYCLE 3 |
| Untracked legacy | cycle 3 step 26 | 11:35 | 4 min | NONE FOUND |
| External web | WebSearch (BTC price, ETF outflows) + WebFetch | 11:39 | live | LIVE |
| Previous review | OPUS_ENRICHED_REVIEW_AUTO_2026-06-26_0439.md | 04:39 | 7h | READ |

**Blindspots:** Live BTC/ETH tick price (using recent internal + external search context), Bybit API failing (54 symbols → MEXC fallback, OI/LS sparse), Reddit social blocked (403), onchain config missing, no live CVD/liquidation heatmaps.

---

## 3. Scheduler / Data Freshness

- **Scheduler log** mtime: 11:35:48 EEST (4 min ago). **NOT DEFERRED.**
- **Cycle 3**: 2026-06-26 10:30–11:35 EEST. Steps: 30 OK / 0 failed. CLEAN.
- **Bybit API**: FAILED (bybit ohlcv_fetched=0, failed=54 in intraday). MEXC fallback active. OI/long-short sparse.
- **Active crypto signals**: 11 (all B-tier). 3 triggered (OPEN ACTIONABLE), 8 tp_hits (ENTERED UNRESOLVED).
- **Active stocks signals**: 20 (all C-tier, all WAITING). US market closed.
- **Paper monitor status** (Cycle 3, step 28):
  - Open actionable: **5**
  - Waiting for entry: **0**
  - Entered unresolved: **4**
  - Review/Shadow: **212**
  - No-entry/stale/moved-away: **36**
  - Closed today: 289W / 29L / 0flat
  - Needs review: **0**
- **Paper-shadow B** (forward valid, 1d window, ~54 signals): A −6.68R vs B +1.88R (delta +8.56R). NOT_READY for promotion (4/6 criteria — need 14d+/60+ forward trades).
- **Untracked legacy crypto alerts**: NONE (clean).
- **Onchain**: interface_ready / config_missing — no data.
- **Squeeze phase distribution** (93 symbols tracked via intelligence layer):
  - Unknown: 44 · Build-up: 12 · **Squeeze expansion: 3** · Unwind: 6 · Post-unwind chop: 28

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-06-26 11:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.88,
      "reason_codes": ["scheduler_fresh", "derivatives_sparse"],
      "data_missing": ["bybit_OI_54_symbols", "onchain_config_missing", "reddit_social_403", "live_btc_tick"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "scheduler.log mtime 11:35 (4 min ago)",
        "cycle 3: 30 steps OK / 0 failed",
        "scalp 07:48 (3h51m) carry-forward",
        "intraday 08:06 (3h33m) carry-forward",
        "stocks intraday 08:33 (3h6m) fresh",
        "catalyst integrity 08:07 (3h32m) fresh",
        "bybit: 54 symbols failed, MEXC fallback (OI/LS sparse)",
        "untracked legacy alerts = 0"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.82,
      "reason_codes": ["risk_off", "chop", "shorts_preferred", "wait_for_trigger"],
      "data_missing": ["live_btc_price", "live_orderbook", "CVD", "liquidation_heatmaps"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC downtrend confirmed (all three reports)",
        "ETH downtrend confirmed (all three reports)",
        "altcoin breadth EMA20: 41.46% (up from 19.15% overnight — improved but still below 50%)",
        "ATR 100th pct = elevated volatility",
        "VIX 19.62 (stocks chop, 2/4 indices in range)",
        "record ETF outflows: $3.4B in one week (external search confirmed)",
        "BTC approx $59-62K range, bounced from below $60K lows",
        "macro: Fed hawkish (removed progress language), 10y Treasury 4.82%",
        "SPY/QQQ 5d -0.85 to -0.90% (range); IWM +3.1% / DIA +0.6% recovering"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["fresh_catalyst", "narrative_supported", "catalyst_contradicted"],
      "data_missing": ["primary_source_verification_hype"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "catalyst integrity: only 2 unmapped high-importance (IWM/META) — STRONG mapping",
        "583 events today, 5 active baskets",
        "HYPE: Multicoin 400% upside call + whale 267K HYPE ($17M from Coinbase Prime)",
        "BTC: ETF outflows $3.4B week + below $60K + $1.48B liquidations (confirmed)",
        "ETH: contradiction — AscendEX delays (bearish) vs SharpLink/Bitmine buying (bullish)",
        "UNH: DOJ criminal+civil fraud probe confirmed (AVOID)",
        "ADA: wallet exploit SecondFi confirmed (AVOID)",
        "MSFT: Italy antitrust probe (AI price hike) — minor/watch",
        "perps_dex basket: HYPE primary (wait_pullback, fresh <6h)",
        "momentum_breakout basket: BEL/JTO (fresh <1h)"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["data_unavailable", "squeeze_risk", "oi_supports"],
      "data_missing": ["bybit_OI_54_symbols", "aggregated_CVD", "liquidation_heatmaps"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Bybit derivatives failed (54 symbols) → MEXC fallback, OI/LS not available for most",
        "phase_2_squeeze_expansion: 3 symbols (names not identified without JSONL query)",
        "phase_4_unwind: 6 symbols",
        "FOGO: price down + OI up (fresh shorts pressing, squeeze risk if price reclaims)",
        "OPG: price down + OI up (fresh shorts pressing, funding -0.000107)",
        "G/USDT: funding 5e-05 (neutral), OI +34% price up (fresh positioning confirmed)",
        "HEI: OI +38% price up (fresh positioning, already entered)"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["chase_risk", "clean_retest", "entry_late"],
      "data_missing": ["live_chart", "tradingview_confirmation"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "G/USDT: 41.7% 24h move → chase risk above 0.0043; pullback zone 0.0040-0.0041 only",
        "HEI/USDT: tp_hits (already entered) — manage, do not add",
        "ETH swing short: tp_hits, retest zone 1530-1543 (swing report); active",
        "ETH swing long (triggered): contradiction vs active swing short — manual review",
        "BTC swing short: tp_hits, managing existing — regime aligned",
        "HYPE: no active signal yet, wait_pullback required before entry",
        "BEL/USDT: triggered swing long, setup quality 72.2/100"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.88,
      "reason_codes": ["open_actionable", "entered_unresolved", "no_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "OPEN ACTIONABLE (triggered): G/USDT scalp long, BEL/USDT swing long, ETH/USDT swing long",
        "ENTERED UNRESOLVED (tp_hits): ETH swing short, WLD scalp short, HEI intraday long, BTC swing short, HOT swing long, ETH swing long #2, AXL swing long, MEN swing short",
        "Paper monitor: 5 open actionable, 0 waiting, 4 entered unresolved, 212 shadow, 36 no-entry, 0 needs review",
        "Closed today: 289W / 29L / 0flat (paper/shadow)",
        "Untracked legacy alerts: 0 (clean)",
        "ETH: contradictory swing short + swing long — flag for manual review"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.80,
      "reason_codes": ["legal_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "UNH: DOJ criminal+civil fraud probe = mandatory AVOID (legal_risk rule)",
        "ADA: wallet exploit confirmed = AVOID",
        "ETH: contradictory long+short signals simultaneously active = manual review",
        "scalp bucket: PF 0.14 (WR 12%) — losing; reduce scalp exposure",
        "stocks C-tier: PF 0.63 — not actionable",
        "Bybit API failure degrades data quality for 54 symbols",
        "macro: Fed hawkish + Treasury 4.82% + record ETF outflows = structural headwinds",
        "US market opens 16:30 EEST (~5h); stocks planning context only"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.80,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": ["A_tier_crypto_sample"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "scalp: n=42 trig, WR 12%, PF 0.14, -6R — FAILING BUCKET",
        "intraday: n=41 trig, WR 37%, PF 2.00, +18R — WORKING",
        "swing: n=51 trig, WR 24%, PF 1.17, +5R — marginal positive",
        "short/breakdown setup: n=36 trig, WR 36%, PF 3.00, +20R — STRONGEST BUCKET",
        "stocks A/B: n=19 trig (weak confidence), PF 1.11, WR 26%, +1R",
        "stocks C-tier: PF 0.63 (losing) — research only",
        "paper-shadow B forward: +1.88R vs A -6.68R — positive, NOT_READY (4/6)"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.78,
      "reason_codes": ["wait_for_trigger", "shorts_preferred", "catalyst_backed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "no clean new entries this window — existing positions managed (tp_hits)",
        "HYPE: catalyst-backed RS leader (Multicoin + whale) — best new setup on pullback",
        "ETH swing short: best short candidate (active, regime aligned)",
        "UNH mandatory AVOID per legal_risk rule",
        "scalp bucket losing — reduce weight on G/USDT scalp alert",
        "stocks planning context only until 16:30 EEST"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.78,
    "preferred_side": "mixed",
    "best_long_candidate": {
      "symbol": "HYPE/USDT",
      "trigger": "price pulls back to structure support after catalyst; next cycle generates active signal at score >=65",
      "reason": "perps_dex basket primary, Multicoin 400% upside, 267K HYPE institutional buy confirmed — catalyst-backed RS leader in chop"
    },
    "best_short_candidate": {
      "symbol": "ETH/USDT",
      "trigger": "failed bounce retest 1530-1543 zone, no 1h close above 1558",
      "reason": "swing short already active (tp_hits), regime aligned, AscendEX withdrawal risk, ETH leads selloff"
    },
    "best_catalyst_candidate": {
      "symbol": "HYPE/USDT",
      "trigger": "catalyst confirmed; wait for price pullback to structure then entry",
      "reason": "Multicoin Capital 400% upside by 2028 + 267K HYPE ($17M) from Coinbase Prime — institutional thesis"
    },
    "avoid_candidate": {
      "symbol": "UNH",
      "reason": "DOJ criminal+civil fraud probe confirmed, shares -16% — mandatory AVOID per legal_risk rule; also ADA wallet exploit"
    },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|-------|---------|------------|--------------|-----------------|
| data_quality | ok | 0.88 | scheduler_fresh, derivatives_sparse | advisory_only |
| market_regime | caution | 0.82 | risk_off, chop, shorts_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | ok | 0.85 | fresh_catalyst, narrative_supported, catalyst_contradicted | advisory_only |
| derivatives_squeeze | caution | 0.55 | data_unavailable, squeeze_risk, oi_supports | advisory_only |
| technical_entry | caution | 0.72 | chase_risk, clean_retest, entry_late | advisory_only |
| execution_lifecycle | ok | 0.88 | open_actionable, entered_unresolved, no_entry | advisory_only |
| risk_manager | caution | 0.80 | legal_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.80 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.78 | wait_for_trigger, shorts_preferred, catalyst_backed | advisory_only |

---

## 4. What Changed vs Previous Review

**Previous:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-26_0439.md` (04:39 EEST, 7h ago)

| Change | Detail |
|--------|--------|
| Regime improved | danger (19.1% EMA20 breadth) → range/chop (41.46%). BTC/ETH still downtrend, alts stabilized. |
| Catalyst mapping STRONG | Was 73.9% unmapped (WEAK flag). Now only 2 unmapped (IWM/META). Major improvement. |
| New signals (Cycle 3) | G/USDT B scalp long (NEW — RS +41.7%, no catalyst). BEL/USDT B swing long (NEW). |
| Signals resolved | NEAR/USDT (was short-watch, no longer active — expired or TP hit). MEGA/USDT similar. |
| HEI status | Was best long-watch (04:39) → now ENTERED UNRESOLVED (tp_hits). Position running. |
| ETH contradiction | NEW: ETH has simultaneous swing short (tp_hits) AND swing long (triggered). |
| AscendEX warning | NEW: ZachXBT alert on AscendEX withdrawal delays. ETH ecosystem risk. |
| ETF outflows confirmed | External: $3.4B in one week (record). Internal: 6-week streak. Sources aligned. |
| UNH AVOID | Maintained from prior review. DOJ probe ongoing. |
| Paper-shadow B | Forward: A -6.68R / B +1.88R (delta +8.56R). NOT_READY maintained (4/6). |

---

## 5. Catalyst Coverage

- **Total events today:** 583 unique events, **5 active narrative baskets**
- **Catalyst integrity (08:07 EEST):** 41 symbols with high-importance news in last 24h; 45 mapped into catalyst_events
- **Unmapped high-importance:** only **2** (IWM, META) — **STRONG mapping (~95%+ coverage)**
- **No-catalyst regression signature:** NONE (ASTER fix confirmed working)
- **Active narrative baskets:**
  - **rwa_narrative** (ONDO/XLM — related_beta_rotation, fresh <6h)
  - **perps_dex_narrative** (HYPE — wait_pullback, fresh <6h)
  - **binance_ecosystem_teaser** (BNB — related_beta_rotation, fresh <6h)
  - **ai_narrative** (NEAR/RENDER/TAO/FET — related_beta_rotation, freshness unknown)
  - **momentum_breakout** (BEL/JTO — wait_pullback, fresh <1h)

**Notable catalyst events:**
- **ADA/USDT** [exploit_hack]: Cardano wallet exploit — SecondFi traces to private key flaw — **AVOID**
- **BTC/USDT** [regulatory]: $3.4B ETF outflows (record week), BTC fell below $60K / $1.48B liquidations
- **ETH/USDT** [contradiction]: AscendEX withdrawal delays (ZachXBT, bearish) vs SharpLink +5K ETH / Bitmine staking 160K ETH (bullish)
- **HYPE/USDT** [bullish]: Multicoin Capital 400% upside call + 267K HYPE whale buy from Coinbase Prime
- **UNH** [legal_risk]: DOJ criminal+civil fraud probe, shares −16% — **MANDATORY AVOID**
- **MSFT** [regulatory]: Italy antitrust probe (AI/365 price hike) — minor, watch only
- **XRP/USDT** [regulatory]: ETF outflows spillover, regulatory pressure noted

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** chop / mild risk-off — BTC/ETH downtrend, breadth 41% EMA20 (improved but <50%). Elevated volatility (ATR 100th pct). Not danger, not risk-on.
- **Stocks mood:** pre-market / closed — VIX 19.62 (chop). SPY/QQQ in range. IWM/DIA improving. **No intraday entries until RTH open 16:30 EEST (~5h).**
- **Dominant narrative:** BTC/crypto macro selloff (Fed hawkish, record ETF outflows, Treasury yields 4.82%, AI/tech -10%). HYPE as relative outperformer (institutional accumulation + Multicoin). RS leaders (G/HEI/BEAT/BEL) defying the tape.
- **Preferred side now:** shorts on confirmed failed retests + catalyst-backed RS-leader longs (no chase, no broad long)
- **Best long candidate:** HYPE/USDT — wait_pullback to structure; catalyst confirmed (Multicoin + whale accumulation); perps_dex basket primary
- **Best short candidate:** ETH/USDT — failed bounce retest 1530–1543 zone; no 1h close above 1558; existing swing short managing (tp_hits)
- **Best catalyst-backed candidate:** HYPE/USDT — institutional thesis (Multicoin 400% + $17M whale buy), not retail noise
- **What to avoid:** UNH (DOJ probe), ADA (wallet exploit), new scalp longs chasing G/USDT above 0.0043, any new ETH long without resolving short contradiction, broad crypto longs without BTC confirmation
- **What would change the view:** BTC closes above 64–65K on volume → regime may shift to risk-on for longs. ETH 1h close above 1558 → swing short invalidated. ETF inflow reversal or Fed pivot signal → structural regime change.

---

## 7. Candidate Deep Dives

### Candidate 1: G/USDT — B scalp long — OPEN ACTIONABLE

**Status:** OPEN ACTIONABLE (triggered). Entry zone: 0.0040–0.0041.
**Score:** 67.8/100 (scalp) / 63.1/100 (intraday watchlist only)
**Playbook:** `crypto_scalp_momentum_continuation` — **low_confidence** (PF 0.14, WR 12%, 14d)

**Evidence:**
- Strongest RS: +41.7% 24h vs BTC, RS vs BTC +43.9%. Volume 1.66x average.
- OI: +34% with price up (fresh positioning, funding neutral 5e-05).
- No verified catalyst — pure momentum/RS. No-catalyst intraday lane historically WR 23%/PF 0.70 (net negative).
- Momentum score 94.9/100 — top ranked symbol.

**Price-reaction / chase check:**
- Price reacted +41.7% in 24h. Any entry above 0.0043 is chasing.
- Likely >2 ATR from EMA20 — overextended.
- Intraday score 63.1 — below active threshold (watchlist only in intraday mode).
- Scalp playbook: **worst-performing bucket** (PF 0.14, -6R 14d evidence).
- Regime: range/chop → breakout failure risk elevated without catalyst.

**Verdict:** OPEN ACTIONABLE as scalp B signal. **LOW CONFIDENCE.** Pullback to 0.0040–0.0041 ONLY; no market buy above 0.0043. Scalp playbook losing — size down. Intraday: watchlist-only. Invalidation: 1h close below 0.0038–0.0039.

---

### Candidate 2: ETH/USDT — B swing short + swing long — CONTRADICTION

**Status:**
- Swing short: ENTERED UNRESOLVED (tp_hits, partial profits taken)
- Swing long (triggered): OPEN ACTIONABLE — **MANUAL REVIEW REQUIRED**
- Swing long (tp_hits): ENTERED UNRESOLVED

**Playbook (short):** `crypto_failed_bounce_short` — actionable (PF 2.0+, WR 40%)

**Contradiction:** ETH has opposing signals from different cycle generations. Swing short is running with partials taken. Swing long was generated later betting on institutional buying catalyst.

**Bearish catalysts (support short):**
- "Ether leads broad crypto selloff" (CoinDesk) — ETH as weakness leader
- AscendEX withdrawal delays (ZachXBT) — ETH ecosystem trust risk
- BTC ETF outflows → broad crypto weakness

**Bullish catalysts (support long):**
- SharpLink: 5,000 ETH ($7.85M) after 8-month pause (lookonchain)
- Bitmine: staked 160,480 ETH ($248.7M) — institutional staking commitment

**Verdict:** Swing short — **MANAGE EXISTING** (tp_hits, trail stop). Do NOT add without retest 1530–1543 confirmation. Swing long (triggered) — **MANUAL REVIEW REQUIRED.** Do not enter blindly into opposing direction. Invalidation for swing short: 1h close above 1558.

---

### Candidate 3: HEI/USDT — B intraday long — ENTERED UNRESOLVED

**Status:** ENTERED UNRESOLVED (tp_hits — partials taken). Was best long-watch at 04:39.
**Score:** ~66/100 (intraday)
**Playbook:** `crypto_intraday_catalyst_or_momentum`

**Evidence:**
- RS vs BTC: +34% now (was +51% overnight — normalized after entry).
- OI: +38% price up (fresh positioning confirmed at entry). Funding: neutral.
- No verified catalyst (pure momentum RS).
- momentum_breakout basket now BEL/JTO (not HEI) — HEI past initial momentum phase.

**Verdict:** ENTERED UNRESOLVED — trail stop to protect captured R. Do not add at elevated levels. Position working; best practice is to protect R, not extend exposure.

---

### Candidate 4: HYPE/USDT — Catalyst watch — BEST CATALYST CANDIDATE

**Status:** NOT in active B/A signals. In perps_dex_narrative basket (HYPE primary, wait_pullback, fresh <6h).

**Catalyst evidence:**
- Multicoin Capital: "400% upside for HYPE by 2028" (BeInCrypto) — VC with direct holdings
- Whale #1: 222,493 HYPE ($14.41M) from Coinbase Prime (wallet 0x66FE) (lookonchain)
- Whale #2: 44,986 HYPE ($2.87M) from FalconX (wallet 0x6437) (lookonchain)
- Two independent institutional-grade buys, confirmed same session
- No bearish headline for HYPE observed

**Chase check:** Price has reacted to catalyst disclosures. wait_pullback playbook = do NOT enter at current levels. Need price to pull back to structure. Not yet at B-tier score threshold — watch for next cycle signal generation.

**Mood alignment:** HYPE is a catalyst-backed RS leader in a chop tape — the ideal setup profile. Perps DEX is a structural narrative, not a pump-and-dump.

**Verdict:** **CATALYST-WATCH.** Trigger: price pullback to structure support + next cycle generates active B-tier signal. Best candidate for next fresh entry. Do not buy the current move.

---

### Candidate 5: BTC/USDT — B swing short — ENTERED UNRESOLVED

**Status:** ENTERED UNRESOLVED (tp_hits — partial profits taken)
**Playbook:** `crypto_failed_bounce_short`

**Macro context (external confirmed):**
- Record ETF outflows: $3.4B in one week — largest since ETF launch (January 2024)
- BlackRock IBIT: $980M outflows (worst week ever)
- BTC fell below $60K with $1.48B liquidations (June 25 event)
- Strategy $13B paper loss headline — negative sentiment
- Fed: removed "progress toward 2% target," rate cuts pushed to 2027
- Treasury 10y: 4.82% (+18bps in 3 days)
- BTC range external: ~$59–62K (June 24-25 confirmed; June 26 around $58-62K)

**Verdict:** ENTERED UNRESOLVED — hold with trailing stop. Do NOT add now (bounced from lows). Watch BTC at 63–65K resistance for failed bounce → confirmation zone. Invalidation: 1h close above 65K.

---

## 8. Best Candidates Ranked

No new clean entries this window. Action: manage existing entered positions, watch for pullbacks.

| Rank | Symbol | Side | Mode | Action |
|------|--------|------|------|--------|
| 1 | HYPE/USDT | Long (catalyst) | Watch | CATALYST-WATCH — wait_pullback to structure; trigger: next cycle active signal >=65 |
| 2 | ETH/USDT | Short | Swing | MANAGING EXISTING — tp_hits, trail stop; add trigger: retest 1530–1543 only |
| 3 | BTC/USDT | Short | Swing | MANAGING EXISTING — tp_hits, trail stop; watch 63K–65K resistance fail |
| 4 | G/USDT | Long | Scalp only | OPEN ACTIONABLE — pullback 0.0040–0.0041 only; no chase above 0.0043; low confidence |
| 5 | BEL/USDT | Long | Swing | OPEN ACTIONABLE (triggered) — wait pullback; momentum_breakout basket |

**Best long-watch:** HYPE/USDT — trigger: pullback to structure, next cycle generates active signal; institutional thesis confirmed (Multicoin + whale).

**Best short-watch:** ETH/USDT — trigger: failed bounce retest 1530–1543; no 1h close above 1558; active swing short managing.

**Best catalyst-watch:** HYPE/USDT — Multicoin 400% call + 267K HYPE institutional buy; perps_dex basket primary; wait_pullback playbook.

---

## 9. Avoid / No Trade (This Decision Window Only)

| Symbol | Reason |
|--------|--------|
| **UNH** | DOJ criminal+civil fraud probe confirmed, shares -16%. MANDATORY AVOID. Legal risk rule — no exception regardless of score. |
| **ADA/USDT** | Cardano wallet exploit (SecondFi, private key flaw). Avoid until exploit fully contained. |
| **G/USDT above 0.0043** | Chase risk in chop. No catalyst. Scalp PF 0.14. Pullback to 0.0040–0.0041 only. |
| **ETH long (triggered)** | Do not enter vs active swing short without manual resolution of contradiction. |
| **Broad crypto long** | BTC still in downtrend. No broad long until BTC closes above 64K structurally. |
| **All stocks (intraday)** | US market closed until 16:30 EEST. C-tier only, all WAITING. No entries before RTH open. |

*These avoids apply to the current decision window only. Scanner, data collection, monitoring, and tracking continue in all regimes.*

---

## 10. Main Risks

1. **Bybit API failures (54 symbols):** OI and funding data degraded. MEXC fallback misses long/short ratio and OI history. Affects scoring quality for derivatives-heavy setups.
2. **ETH contradictory signals:** Swing short + two swing longs simultaneously active. Manual intervention required before adding any ETH position in either direction.
3. **BTC bounce risk:** Bounced from below $60K. If extends to 63–65K, existing swing shorts face invalidation. Monitor closely.
4. **Record ETF outflows structural:** $3.4B/week is institutional de-risking — structural headwind, not short-term noise. Sustained into summer with macro catalyst (Fed hawkish).
5. **Macro: Fed hawkish + Treasury 4.82%:** Rate cuts pushed to 2027. Persistent headwind for crypto/tech risk assets.
6. **AI/tech selloff spillover:** BTC correlation with tech remains high. Any further tech weakness creates downside pressure. US open 16:30 EEST is the key risk event.
7. **Scalp bucket losing (PF 0.14):** G/USDT scalp signal is in the worst-performing playbook. Alert confidence is lower than tier B implies.
8. **Reddit/social blocked (403):** No social attention data every cycle. KOL config uses placeholder. Crowd context fully missing.

---

## 11. Action Plan — Next 4 Hours (Until ~16:00 EEST, then US open review)

1. **G/USDT scalp (OPEN ACTIONABLE):** Do not chase. Pullback to 0.0040–0.0041 only; trail tightly on any scalp entry. Low confidence — 0.5x sizing per playbook weight.
2. **ETH swing short (ENTERED):** Trail stop; manage existing. Add only on retest of 1530–1543 with no 1h close above 1558. Do not add blindly.
3. **ETH swing long (TRIGGERED — MANUAL REVIEW):** Do not enter without human decision to resolve contradiction vs active swing short. Flag for manual session.
4. **HEI/USDT (ENTERED):** Trail stop on existing position. Protect captured R. No new additions at elevated levels.
5. **BTC swing short (ENTERED):** Hold. Trail stop. Monitor BTC behavior at 63K–65K resistance for failed bounce add zone.
6. **HYPE/USDT (WATCH):** Monitor for pullback. Not yet active signal. Confirm via next cycle.
7. **BEL/USDT swing long (TRIGGERED):** Wait for pullback entry; do not buy extended move. momentum_breakout basket (wait_pullback playbook).
8. **Stocks (PLANNING):** US opens 16:30 EEST. Pre-market watchlist: AMD B long, JPM B long, SMH B long, MSFT B short — all C-tier WAITING, all planning. Revisit at 16:20 pre-US-open review slot.

---

## 12. Final Verdict Per Mode

| Mode | Verdict | Action |
|------|---------|--------|
| Crypto scalp | CAUTION / low confidence | G/USDT: pullback 0.0040–0.0041 only; no chase; PF 0.14 = 0.5x size weight |
| Crypto intraday | WATCH | No new A/B intraday setups; HEI managing; HYPE watch for signal |
| Crypto swing | CAUTION / manage existing | ETH short + BTC short: tp_hits, manage. ETH long: manual review required. BEL/HOT/AXL: hold per plan. |
| Stocks intraday | PLANNING ONLY | US opens 16:30 EEST. All C-tier WAITING. No entries until RTH + 15–30 min confirmation. |
| Stocks swing | WATCHLIST ONLY (paused) | WR 11%, PF 0.15. Not Telegram-actionable. |
| Stocks invest | WATCHLIST ONLY (paused) | WR 0%, 0W/24L. Not Telegram-actionable. |

---

## 13. Sources

- [Bitcoin Falls as Record ETF Outflows and Strategy Sale Hit Sentiment](https://www.investing.com/analysis/bitcoin-falls-as-record-etf-outflows-and-strategy-sale-hit-sentiment-200681446) — Investing.com, June 3, 2026 — confirms ETF outflow context, BTC downtrend structural drivers
- [Bitcoin ETFs Record Largest-Ever $3.4B Sell-Off](https://coinfomania.com/bitcoin-etf-outflows-june-2026-record-selloff/) — Coinfomania, date unavailable — confirms record weekly ETF outflows
- [Bitcoin Drops 3% Amid Leverage Flush, ETF Outflows, Liquidity Rotation](https://coinmarketcap.com/top-stories/6a226761f98ad067b44d4ac2/) — CoinMarketCap, date unavailable — macro context: leverage flush, ETF outflows, liquidity rotation
- [Bitcoin (BTC) Daily Market Analysis 24 June 2026](https://coinstats.app/ai/a/latest-news-for-bitcoin) — CoinStats AI, June 24, 2026 — BTC price context ~$62,651 on June 24
- Internal: `data/reports/scalp/2026-06-26_07-48_scalp_report.md`
- Internal: `data/reports/intraday/2026-06-26_08-06_intraday_report.md`
- Internal: `data/reports/stocks/intraday/2026-06-26_08-33_stocks_intraday_report.md`
- Internal: `data/reports/swing/2026-06-26_02-25_swing_report.md`
- Internal: `data/scheduled_runs/2026-06-26_default_schedule/cycle_03_10-30_summary.md`
- Internal: `reports/CATALYST_INTEGRITY_DAILY_SUMMARY.md`
- Internal: `data/processed/llm_analysis_packet.md`
- Internal: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-26_0439.md` (prior review)

---

## 14. Fix Requests / TODO

### TODO-ETH-CONTRADICTION
- **issue:** ETH/USDT simultaneously has an active swing short (tp_hits/ENTERED) AND swing longs (one triggered, one tp_hits) from the same timeframe category. No warning is issued when opposing-direction signals coexist for the same symbol+mode combo.
- **evidence:** active-signals CLI (11:39 EEST): ETH/USDT — swing short (tp_hits) + swing long (triggered) + swing long (tp_hits). Three simultaneous ETH signals, two opposing in direction.
- **suggested manual fix:** Add contradiction detection to the active-signal tracker: when two active signals of opposite direction exist for the same symbol+mode, flag them in paper monitor output and Telegram alerts. Operator can then cancel one or treat as hedge with explicit approval.
- **priority:** medium
- **first observed:** 2026-06-26 11:39 EEST

### TODO-BYBIT-API-FAILURES
- **issue:** Bybit failed to fetch OHLCV for 54 symbols and failed to initialize (instruments-info endpoint) in Cycle 3. Pattern recurring across multiple cycles. When Bybit fails, OI/funding/long-short data degrades significantly — MEXC fallback does not provide OI history or LS ratio.
- **evidence:** `cycle_03_10-30_summary.md`: "bybit: ohlcv_fetched=0, failed=54"; step 3 log: "Could not initialise bybit: bybit GET .../instruments-info?category=linear&limit=1000"; step 2: "bybit fetch_tickers failed (bybit GET .../tickers?category=spot)"
- **suggested manual fix:** Investigate Bybit API connectivity in the scheduled environment (rate limits, network/firewall, API key expiry, endpoint deprecation). Add health-check alerting step when Bybit fails >N symbols. Consider retry logic or API endpoint migration.
- **priority:** high
- **first observed:** 2026-06-26 11:39 EEST (pattern recurring)

### TODO-REDDIT-403
- **issue:** All three Reddit social sources return 403 (Blocked) every cycle — r/CryptoCurrency, r/Bitcoin, r/ethereum. Social crowd attention context fully missing. KOL config also uses a placeholder account.
- **evidence:** `cycle_03_10-30_summary.md` logs: "Failed social source Reddit CryptoCurrency: 403 Client Error: Blocked" (repeated for all three subreddits across steps 2, 3, 18).
- **suggested manual fix:** Reddit blocked unauthenticated scraping since June 2023 policy change. Replace with OAuth2 Reddit API or alternative social data sources (LunarCrush, Santiment social volume API, or X/Twitter API). Simultaneously replace KOL watchlist placeholder with 3–5 trusted crypto analyst accounts.
- **priority:** medium
- **first observed:** 2026-06-26 11:39 EEST (persistent recurring)
