# Opus Enriched Review — Europe / Pre-US Context — Auto Cycle 11:39 EEST

> **Advisory only / no auto-trade. Thursday July 2, 2026. Slot: Europe / pre-US context (11:30). Crypto: LIVE. Stocks: CLOSED — planning only, RTH opens 16:30 EEST / 09:30 ET.**

---

## 1. Executive Summary

**Slot: Europe / pre-US context — advisory only / no auto-trade.**

BTC recovered to **~$60,123** (+2.45%) after touching $57,891 intraday — bouncing on Kevin Warsh / Fed inflation narrative after June's worst monthly drop (−20.48%) since 2022. ETF inflows collapsed. Macro risk score 65/100 (4 risk-off headwinds despite Warsh bounce). Crypto regime: **range/chop neutral** (ETH transition_up on latest intraday report). Altcoin breadth: 54.76% above EMA20 — mixed. Stocks regime: **bullish** (4/4 indices uptrend, VIX 16.85, breadth 100% above EMA20).

**Critical flags this cycle:**
- **⚠️ UNH DOJ CRIMINAL PROBE (3rd consecutive review):** A-tier long signals for UNH are invalid. LEGAL RISK / AVOID — all modes, all horizons.
- **⚠️ TLM BINANCE DELISTING MONITORING (May 22, 2026) + PRICE DISCREPANCY:** TLM swing long is TRIGGERED/ENTERED-UNRESOLVED. Binance price $0.0172 vs CoinGecko $0.000885 — factor ~19x. NEEDS HUMAN REVIEW immediately.
- **DYDX sell-the-news CONFIRMED:** dYdX launched Arcus DEX on Robinhood Chain — −29.85% 24h with 673% volume spike. Strong short continuation candidate on bounce.
- **⚠️ Catalyst mapping weak (69.4% unmapped):** Use catalyst layer as context only, not final decision filter.

System: 21 B-tier crypto signals active (BTC short, ETH short, BERA, AAA swings → ENTERED UNRESOLVED at TP1). Stocks: 50 C-tier + AMD B-tier WAITING for RTH. No A-tier crypto this cycle. JPM A-tier stocks clean for RTH planning.

---

## 2. Data Used

| Source | File / CLI | Age at 11:39 EEST | Status |
|--------|-----------|-------------------|--------|
| Scheduler cycle_04 | `cycle_04_10-55_summary.md` | 24 min | **FRESH** |
| Crypto scalp | `2026-07-02_08-02_scalp_report.md` | 0.62h | **FRESH** |
| Crypto intraday | `2026-07-02_08-07_intraday_report.md` | 0.54h | **FRESH** |
| Crypto swing | `2026-07-02_00-58_swing_report.md` | 7.7h | **CARRY-FORWARD** |
| Stocks intraday | `2026-07-02_08-13_stocks_intraday_report.md` | 0.44h | **FRESH** |
| Stocks swing | `2026-07-02_00-59_stocks_swing_report.md` | 7.67h | **CARRY-FORWARD** |
| Stocks invest | `2026-07-02_01-01_stocks_invest_report.md` | 7.64h | **CARRY-FORWARD (paused)** |
| LLM packet (crypto) | `llm_analysis_packet.md` | 0.54h | **FRESH** |
| LLM packet (stocks) | `llm_stocks_packet.md` | 0.43h | **FRESH** |
| Catalyst cycle | `catalyst_cycle_08-07.md` | 0.53h | **FRESH** |
| Active signals crypto | CLI `active-signals --asset-class crypto` | 11:39 | 21 B-tier |
| Active signals stocks | CLI `active-signals --asset-class stocks` | 11:39 | 50 C-tier + AMD B-tier |
| Signal stats crypto | CLI `signal-stats --asset-class crypto` | 11:39 | n=72, PF=0.70, −8R |
| Signal stats stocks | CLI `signal-stats --asset-class stocks` | 11:39 | A/B n=25, PF=0.375, −5R |
| Untracked legacy alerts | CLI `detect_untracked_legacy_alerts` | 11:39 | **NONE — clean** |
| BTC price / market | WebSearch (CryptoTimes, Finbold) | 11:39 | ~$60,123, +2.45%, low $57,891 |
| UNH DOJ probe | WebSearch (Yahoo Finance, FierceHealthcare, Nasdaq) | 11:39 | Criminal Medicare fraud probe confirmed multi-source |
| TLM delisting / price | WebSearch (CoinMarketCap, Binance, CoinGecko data) | 11:39 | Delisting monitoring confirmed; Binance $0.0172 vs CoinGecko $0.000885 |
| DYDX Arcus launch | WebSearch (BanklessTimes) | 11:39 | Sell-the-news −29.85%, volume 673% spike |
| Previous review | `OPUS_ENRICHED_REVIEW_AUTO_2026-07-02_0439.md` | 7h ago | Loaded |

**External web research:** Operational — 4 searches executed, all returned usable results.
**scheduler.log:** NOT FOUND (persistent issue — non-blocking).

---

## 3. Scheduler / Data Freshness

- **Cycle 04:** Started 10:55 EEST, finished 11:15 EEST — **32 steps OK, 0 failed**. Runtime 20 min.
- **Cycle freshness (24 min):** PASSES the 3-hour defer threshold — **NOT DEFERRED**.
- **Pre-cycle tracking pass:** 525 signals checked, 318 TP hits processed, 0 stopped, 0 expired. Revalidation: 29 checked, 4 stale, 0 moved_away, 0 manual_review.
- **Scalp/intraday/stocks reports:** All FRESH (< 1h).
- **Swing reports:** 7.7h → CARRY-FORWARD (4–12h window).
- **Derivatives:** Several symbols on `fallback_via_mexc` (TLM, ZBT, SYN, RIF, MORPHO) — partial OI/L/S data.
- **Social attention:** MISSING (Reddit blocked 403, persistent).
- **Onchain config:** Absent (persistent blind spot).
- **Catalyst mapping:** 69.4% unmapped → **WEAK** — context only.
- **Untracked legacy crypto alerts:** NONE — clean.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-07-02 11:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["scheduler.log (not found — persistent)", "social_attention (Reddit 403)", "onchain_config"],
      "suggested_effect": "advisory_only",
      "facts_used": ["cycle_04 finished 11:15 EEST (24 min ago, 32 OK / 0 failed)", "scalp/intraday/stocks < 1h", "swing 7.7h carry-forward", "catalyst_cycle_08-07 fresh", "LLM packets 0.5h"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["chop", "mixed", "longs_preferred", "wait_for_trigger"],
      "data_missing": ["live BTC/ETH tick beyond 08:00 UTC cutoff", "US pre-market momentum data"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC range/chop (~$60,123, recovering from $57,891 low)", "ETH transition_up (intraday)", "altcoin breadth 54.76% above EMA20", "macro risk 65/100 (4 risk-off hits)", "stocks bullish (4/4 indices, VIX 16.85, breadth 100%)", "June BTC −20.48% worst since 2022", "Kevin Warsh / Fed inflation bounce narrative"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["fresh_catalyst", "stale_catalyst", "mapping_weak", "catalyst_confirmed", "catalyst_contradicted"],
      "data_missing": ["X/Twitter live sentiment", "multi-source ENA/Blackrock confirmation"],
      "suggested_effect": "advisory_only",
      "facts_used": ["DYDX Arcus sell-the-news confirmed (BanklessTimes 2026-07-02, −29.85%, vol 673%)", "UNH DOJ probe confirmed multi-source (Yahoo Finance, FierceHealthcare, Nasdaq)", "TLM Binance delisting monitoring since May 22 2026", "ETH Robinhood Chain AI-L2 launch (Decrypt)", "ETH whale contradiction: Chun Wang sells 16,842 ETH vs 0x2684 buys 15,802 ETH", "SYN: no catalyst for +19.77%", "69.4% unmapped → mapping_weak", "ENA: Ethena/Blackrock partnership (AMBCrypto, importance 0.73, single_source)"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.60,
      "reason_codes": ["data_unavailable", "squeeze_risk", "oi_contradicts", "oi_supports"],
      "data_missing": ["Full OI 24h for most symbols (fallback_via_mexc)", "liquidation heatmap", "aggregated funding feed"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ME/USDT: negative funding bybit/okx/mexc (−0.0042/−0.002/−0.009) → crowding elevated", "DYDX: OI +22.29% as price down → fresh shorts pressing (squeeze risk if reclaims)", "TLM swing: OI +58.5% 24h, L/S 1.82 → crowded longs + delisting risk", "BTC short TP1 HIT → in-profit ~$60,123 vs ~$62k entry", "ETH short TP1 HIT → Robinhood Chain adds catalyst friction"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": ["entry_late", "chase_risk", "overextended", "clean_retest", "stale_before_entry"],
      "data_missing": ["Chart MCP unavailable — TradingView / manual chart check not loaded; using OHLCV fields from reports only"],
      "suggested_effect": "advisory_only",
      "facts_used": ["SYN: +19.77% 24h, +48.63% 7d — extended; entry only pullback 0.5276–0.5435", "TLM: +36–58% 24h — extreme extension, chase risk", "RIF: +45% 24h — extended", "DYDX: −29.85% 24h — potential short but >2 ATR move, wait dead-cat bounce", "JPM stocks: WAITING, RTH 16:30 EEST", "BTC short: TP1 HIT, in-profit; no new entry"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "review_shadow",
      "confidence": 0.80,
      "reason_codes": ["entered_unresolved", "waiting_for_entry", "needs_review", "open_actionable"],
      "data_missing": ["Exact per-signal entry prices (CLI output truncated)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["21 crypto B-tier: ~6 ENTERED UNRESOLVED TP HIT (BTC short, ETH short, JTO swing, BERA swing, AAA swing), ~5 TRIGGERED (SYN scalp, PUMP, HERA, SOL intraday, TLM swing), ~10 WAITING FOR ENTRY", "50 stocks C-tier + AMD B-tier: majority WAITING (market closed), AMD B-tier TP HIT", "TLM swing: TRIGGERED/ENTERED — Binance delisting + price discrepancy → NEEDS HUMAN REVIEW", "Untracked legacy alerts: NONE", "Revalidation: 4 stale signals, 0 moved_away"]
    },
    {
      "agent": "risk_manager",
      "verdict": "manual_review",
      "confidence": 0.88,
      "reason_codes": ["legal_risk", "headline_risk", "correlation_cluster", "reduce_risk", "manual_review"],
      "data_missing": ["Current UNH stock price post-DOJ impact", "TLM exact entry price vs CoinGecko price"],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH DOJ criminal Medicare fraud probe multi-source confirmed, shares −16%, 3rd consecutive review", "TLM delisting monitoring May 22 + price discrepancy ($0.0172 Binance vs $0.000885 CoinGecko = ~19x)", "50 stocks signals all long = correlation cluster", "Crypto shorts (ETH, BTC) in profit at TP1 — manage exits", "DYDX −29.85% + 673% volume → extreme; new short risky without retest", "Weekly crypto stats: −8R, PF 0.70"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample", "old_tail_expired"],
      "data_missing": ["Per-mode breakdown for current week (aggregate only)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto_swing_narrative_rs_momentum: WR 72%, PF 5.80, +24R (14d) — PRIMARY, working", "crypto_failed_bounce_short: PF 2.00, +9R — working", "crypto_intraday_catalyst_or_momentum (no catalyst): WR 23%, PF 0.70, −3R — net negative", "crypto_scalp: WR 12%, PF 0.14, −6R — low confidence", "stocks_intraday_rth_momentum: WR 55%, PF 2.03, +80R (B-tier working)", "stocks A-tier long: WR 21%, −6.2R — overpromotion (0.5× sizing)", "Weekly crypto swing: 8W/14L, PF 1.14, +2R — only positive crypto mode this week"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.72,
    "preferred_side": "mixed",
    "best_long_candidate": {
      "symbol": "JPM",
      "trigger": "RTH open 16:30 EEST + first 15-min bullish candle confirmation; SL below 15-min candle low; do not chase pre-market",
      "reason": "A-tier stocks, financials RS leader (+8.27% vs SPY 20d), no legal/earnings risk, bullish macro regime, VIX 16.85"
    },
    "best_short_candidate": {
      "symbol": "DYDX/USDT",
      "trigger": "Dead-cat bounce to $0.155–$0.165 resistance zone failure OR break below $0.143 on volume; SL above $0.175",
      "reason": "Arcus DEX sell-the-news confirmed (−29.85%, 673% volume spike), fresh shorts in OI (OI +22% as price falls), perps-DEX narrative basket"
    },
    "best_catalyst_candidate": {
      "symbol": "ENA/USDT",
      "trigger": "Ethena/Blackrock partnership confirmed multi-source + pullback entry into support; importance 0.73; no entry until verified",
      "reason": "Highest-importance fresh catalyst this cycle — Blackrock partnership, AI/RWA crossover narrative"
    },
    "avoid_candidate": {
      "symbol": "UNH",
      "reason": "DOJ criminal Medicare fraud probe multi-source confirmed; A-tier long (score 80.11) invalid; 3rd consecutive review LEGAL RISK / AVOID all modes all horizons"
    },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason Codes | Suggested Effect |
|-------|---------|------------|--------------|-----------------|
| data_quality | **ok** | 0.82 | scheduler_fresh, report_stale (swing 7.7h) | advisory_only |
| market_regime | **caution** | 0.72 | chop, mixed, longs_preferred (stocks), wait_for_trigger | advisory_only |
| catalyst_narrative | **caution** | 0.75 | fresh_catalyst, mapping_weak (69.4% unmapped), catalyst_confirmed (DYDX), catalyst_contradicted (ETH whale) | advisory_only |
| derivatives_squeeze | **caution** | 0.60 | data_unavailable (fallback_via_mexc), squeeze_risk (DYDX), oi_contradicts (ME crowded) | advisory_only |
| technical_entry | **caution** | 0.68 | entry_late (SYN/TLM/RIF extended), chase_risk (DYDX −29%), clean_retest (JPM wait RTH) | advisory_only |
| execution_lifecycle | **review_shadow** | 0.80 | entered_unresolved (BTC/ETH/BERA/AAA TP HIT), needs_review (TLM delisting), waiting_for_entry (~10 crypto) | advisory_only |
| risk_manager | **manual_review** | 0.88 | legal_risk (UNH DOJ), headline_risk (TLM delisting+19x price discrepancy), correlation_cluster (50 stocks long) | advisory_only |
| playbook_performance | **caution** | 0.75 | playbook_working (crypto_swing, stocks_intraday_B), playbook_failing (no-catalyst intraday, scalp, stocks_A_long) | advisory_only |
| head_trader | **caution** | 0.72 | wait_for_trigger (stocks RTH), shorts_preferred (DYDX bounce), catalyst_backed (ENA watch) | advisory_only |

---

## 4. What Changed vs Previous Review (04:39 EEST)

| Item | Previous (04:39) | Now (11:39) | Delta |
|------|-----------------|-------------|-------|
| BTC price | ~$58,620 (from $57,950 low) | ~$60,123 (+2.45%) | **+$1,500 bounce — Warsh narrative** |
| ETH trend | range | transition_up (intraday) | **Upgraded** |
| Altcoin breadth (EMA20) | 48.7% (swing, 03:58) | 54.76% (intraday, 08:07) | **+6pp improvement** |
| Crypto active signals | 6 B-tier swing | 21 B-tier (scalp+intraday+swing) | **+15 new cycle signals** |
| BTC short swing | ENTERED UNRESOLVED TP1 | Still ENTERED UNRESOLVED | Progressing; no action needed |
| ETH short swing | ENTERED UNRESOLVED TP1 | Still ENTERED UNRESOLVED | Robinhood Chain friction persists |
| TLM swing long | TRIGGERED ⚠️ delisting flag | TRIGGERED ⚠️ + 19x price discrepancy confirmed | **Escalated — HUMAN REVIEW REQUIRED** |
| DYDX | Early sell-off noted | −29.85% confirmed, 673% vol spike | **Arcus sell-the-news fully confirmed** |
| UNH DOJ probe | AVOID flagged | AVOID confirmed multi-source web | **3rd consecutive — no change** |
| Catalyst mapping | 93.4% other_news (213 events) | 69.4% unmapped (285 events) | Still weak; slightly more classified |
| Stocks regime | Bullish, planning mode | Bullish, VIX 16.85, RTH at 16:30 | No change — building watchlist |
| New catalysts | — | ENA/Blackrock partnership, INJ mainnet, SOL RWA ATH | 3 new catalyst items |

---

## 5. Catalyst Coverage

- **Latest cycle (08:07):** 285 catalyst events scanned; 4 narrative baskets.
- **Accumulated JSONL (all cycles today):** 1,190 entries — Mapped: 364, Unmapped: 826 → **69.4% unmapped**.
- **⚠️ Catalyst mapping weak this run — use catalyst layer as context, not final decision filter.**

Top 3 unmapped headlines (basket-only, symbol null):
1. `[exploit_hack]` — Taiko bridge reopens after $1.7M exploit recovery (CryptoBriefing)
2. `[regulatory_sector_headline]` — Senator Lummis calls to stop "baseless attacks" on the Clarity Act (BeInCrypto)
3. `[legal_risk]` — UNH DOJ criminal probe / Optum Rx extension (QuiverQuant, FierceHealthcare) ← basket unmapped but UNH clearly affected

**Mapped highlights:**

| Symbol | Type | Headline | Importance |
|--------|------|----------|-----------|
| ENA/USDT | partnership | Ethena/Blackrock new partnership (AMBCrypto) | 0.73 |
| BTC/USDT | product_launch | Bitcoin statue unveiled at NYSE (CryptoBriefing) | 0.64 |
| LINK/USDT | product_launch | Solana Prediction Market World Goes Live (BeInCrypto) | 0.62 |
| DYDX/USDT | sell-the-news | dYdX Arcus DEX launch — sell-the-news crash −29.85% (BanklessTimes) | confirmed |
| SOL/USDT | token_unlock | July unlock pressure vs RWA ATH $3.4B TVL (AMBCrypto) | watchlist |
| INJ/USDT | exchange_event | Binance mainnet upgrade support + temp deposit halt (CryptoBriefing) | watch |

**Active baskets (4):**
1. `perps_dex_narrative` — HYPE (primary), DYDX/GMX/ASTER (related); playbook: `wait_pullback`
2. `ai_narrative` — NEAR/RENDER/TAO/FET (primary), WLD/ASTER (related); playbook: `related_beta_rotation`
3. `delisting_thin_liquidity` — no primary symbol; playbook: `avoid_low_liquidity`
4. `momentum_breakout` — NFP/TLM/SYN (primary), ME (related); playbook: `wait_pullback` (**do not chase**)

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** chop / mixed — BTC range-bound recovery on thin Warsh narrative; ETH positive divergence (transition_up); altcoin breadth improving but macro 65/100 risk-off caps conviction
- **Stocks mood:** risk-on / pre-market (planning) — bullish regime (VIX 16.85, 4/4 indices uptrend); healthcare and financials leading; US cash opens 16:30 EEST
- **Dominant narrative:** Kevin Warsh / Fed inflation optimism (BTC thin bounce); DYDX Arcus sell-the-news implosion; Robinhood Chain / ETH L2 ecosystem momentum; UNH legal cloud
- **Preferred side now:** Mixed — crypto: short on dead-cat bounces (DYDX) or wait for RS-leader catalyst confirmation (ENA); stocks: long on RTH open (JPM, XLF) after 15-min confirmation
- **Best long candidate:** JPM — A-tier stocks, financials RS leader, clean; trigger: RTH open + 15-min confirmation; SL below 15-min low
- **Best short candidate:** DYDX/USDT — sell-the-news confirmed; trigger: dead-cat bounce to $0.155–$0.165 or break below $0.143; SL above $0.175
- **Best catalyst-backed candidate:** ENA/USDT — Ethena/Blackrock partnership (importance 0.73, single-source; needs verification before entry)
- **What to avoid:** UNH (DOJ criminal probe, AVOID); TLM (delisting + price discrepancy, HUMAN REVIEW); no-catalyst SYN intraday (−3R lane); scalp mode (PF 0.14, low confidence)
- **What would change the view:** BTC clean break above $62k on volume → uptrend regime; BTC below $57,891 → risk-off re-engages; ENA partnership confirmed multi-source → catalyst entry valid; stocks RTH gap-up held 15 min → JPM actionable

---

## 7. Candidate Deep Dives

### Candidate 1 — UNH (A-tier stocks intraday long) — **LEGAL RISK / AVOID**

**Signal:** A-tier intraday long, score 80.11, WAITING for RTH. Stocks swing B-tier also active (74.95, paused watchlist mode).

**Legal/Headline risk (confirmed multi-source):**
- DOJ criminal probe into Medicare Advantage billing practices (Yahoo Finance, FierceHealthcare, Healthcare Finance News, Nasdaq)
- DOJ healthcare-fraud unit overseeing; FBI interviewing former employees about billing practices
- Probe extended to Optum Rx and physician reimbursement (FierceHealthcare, 2026)
- UNH shares dived ~16% on fraud investigation headline; company acknowledged formal civil and criminal DOJ requests
- 3rd consecutive auto-review cycle flagging this risk

**LEGAL/HEADLINE RISK — FINAL VERDICT: AVOID all modes, all horizons.**
A-tier score (80.11) is invalid. Scoring system does not capture active criminal probes. The 0.5× A-tier long sizing rule is irrelevant here — this is a hard AVOID, not a size adjustment.

**Has price reacted?** Yes — shares already −16% post-headline. Any recovery is potential short-squeeze / dead-cat, not a confirmed long setup.

---

### Candidate 2 — JPM (A-tier stocks intraday long) — **BEST LONG WATCH — RTH trigger**

**Signal:** A-tier intraday long, score 85.71 (highest active stocks signal this cycle), WAITING for RTH. Swing B-tier: 74.0 (paused mode).

**Catalyst check:** No legal or headline risk in catalysts or news. Financials sector (XLF) is 2nd-strongest sector RS leader (+8.27% vs SPY 20d, +6.45% 20d return). No near-term earnings flagged. JPM appears in catalyst data only with general financials coverage — no adverse headlines.

**Market mood alignment:** Stocks bullish regime (VIX 16.85, 4/4 uptrend). Financials leading. JPM is the cleanest A-tier long with no contamination risk.

**Technical entry (from report):** WAITING for RTH. Entry zone ~$320–$322 range (abbreviated from active signals). SL below recent structure (~$305–$308 depending on open).

**Chase check:** US market closed — no chase issue yet. Wait for RTH open at 16:30 EEST, first 15-min candle confirmation. No market buy at open.

**Playbook:** `stocks_intraday_rth_momentum`. A-tier long sub-cohort: WR 21%, −6.2R → size at **0.5×** per overpromotion rule. B-tier sub-cohort (for XLF if confirmed): WR 56%, PF healthy.

**Is it actionable now?** NO — US market closed until 16:30 EEST. Planning mode only.
**SL level:** Below first 15-min RTH candle low; approximate $305–$308.
**Invalidation:** Market gap-down at open; VIX spike above 20; JPM-specific adverse headline in next 4h.

---

### Candidate 3 — DYDX/USDT — **BEST SHORT WATCH — dead-cat bounce trigger**

**Signal:** DYDX appears as weakest symbol across scalp and intraday reports (−29.85% 24h, RS vs BTC −32.02%). Listed in `perps_dex_narrative` basket (related symbol). Crypto intraday and swing reports note fresh attention/catalyst for DYDX.

**External catalyst (confirmed):** dYdX launched Arcus DEX on Robinhood Chain (July 1–2, 2026) — 24/7 trading for 95 stock tokens, equity perpetuals, major crypto. Classic sell-the-news: +21.54% intraday surge on announcement, followed by −29.85% crash. Volume 673% to $125M (above $116M market cap) → aggressive capitulation/liquidation. Token trading ~$0.1448 (BanklessTimes, 2026-07-02).

**Derivatives (internal):** DYDX OI +22.29% as price falls → fresh shorts pressing. Long/short 1.541. Funding: 1.564e-05 (neutral). Fresh short positioning confirmed — NOT a squeeze setup.

**Chase check:** −29.85% 24h is already an extreme move. New short at current level = chasing. Wait for:
1. Dead-cat bounce to $0.155–$0.165 (prior support-now-resistance) + failed retest candle.
2. OR continuation break below $0.143 (current low) on volume re-expansion.

**Playbook:** `crypto_failed_bounce_short` (PF 2.00, +9R, 14d) aligns. `perps_dex_narrative` basket playbook: `wait_pullback`. Both say: wait, do not chase.

**Is it actionable now?** NO — wait for dead-cat structure.
**SL level:** Above $0.175 (invalidates failed-retest structure).
**Squeeze risk:** DYDX OI +22% as price falls = shorts crowded. A surprise buyback or adoption news could cause violent squeeze. Keep size small when entry triggers.
**Invalidation of short thesis:** Price reclaims $0.175 with volume; Arcus TVL showing strong adoption; BTC broad recovery above $62k.

---

### Candidate 4 — TLM/USDT (B-tier swing long, TRIGGERED/ENTERED) — **⚠️ NEEDS HUMAN REVIEW**

**Signal:** B-tier swing long, score 66.1, TRIGGERED (ENTERED UNRESOLVED). Previous review (04:39) already flagged: "Binance delisting monitoring confirmed May 22, 2026. NOT captured in scoring."

**Price discrepancy (CRITICAL — 2nd cycle):**
- Binance/Bybit spot: **$0.017206** (web search, Binance trade page)
- CoinGecko: **$0.0008850**
- Factor: ~19× gap
- Prior review: internal $0.0013–$0.0014 vs CoinMarketCap $0.000878 — now Binance shows $0.0172

**Binance delisting monitoring:** Confirmed since May 22, 2026. TLM placed on delisting monitoring along with 8 other tokens — not yet delisted but at high delistable risk. Exchange can delist with limited notice.

**Derivatives (internal):** OI +58.5% 24h, L/S 1.82 → crowded long positioning into a delisting-risk event. Dangerous combination.

**Chase check:** +36–58% 24h (varies by report) — extreme extension. Position already entered by system; no additional sizing.

**FINAL VERDICT: NEEDS HUMAN REVIEW — DO NOT ADD TO POSITION.**
- Entry price needs verification in DB — $0.0172 vs $0.000885 is a 19× difference in P&L calculation
- Delisting monitoring not reflected in scoring — system cannot self-correct
- Recommend human session: (1) verify actual entry price in signals DB, (2) determine exit plan given delisting risk, (3) investigate price discrepancy (possible token migration or data feed mismatch)

---

### Candidate 5 — SYN/USDT (B-tier scalp TRIGGERED, B-tier intraday WAITING) — **RS LEADER, NO-CATALYST WATCH**

**Signal:** B-tier scalp TRIGGERED (score 66.2, low_confidence overlay). B-tier intraday WAITING (score 64.2). Strongest mover: score 100.0 in movers list, +19.77% 24h, RS vs BTC +17.44–17.60%, volume 1.28x. 7d: +48.63%.

**Catalyst check:** "no fresh verified catalyst detected" — stated explicitly in both scalp and intraday reports. No news mapping to SYN in catalyst cycle. The +19.77% move is pure momentum without catalyst.

**Basket context:** `momentum_breakout` basket lists SYN as primary. Playbook: `wait_pullback` (i.e., do not chase).

**Derivatives (internal):** Price up + OI down (−0.43%) → short covering, **weaker continuation quality**. Intraday: fallback_via_mexc, neutral funding. No OI on fallback.

**Playbook alignment:**
- Scalp (already triggered): `crypto_scalp_momentum_continuation` → LOW CONFIDENCE (WR 12%, PF 0.14, −6R). Size 0.5× by rule.
- Intraday (waiting): `crypto_intraday_catalyst_or_momentum` WITHOUT catalyst → WR 23%, PF 0.70, −3R. **Net-negative lane.**

**Chase check:** +19.77% in 24h, +48.63% in 7d. Already extended. Entry only on pullback to 0.5276–0.5435. BTC in range/chop — breakout failure risk elevated.

**Is it actionable?** Scalp already triggered by system (research-grade, 0.5×). Intraday: **WATCHLIST ONLY** — do not upgrade without verified catalyst or regime breakout. SL: 1h close below $0.5082.

---

**Excess candidates (excluded from §7 due to 5-candidate cap):**
- **ETH short (B-tier swing, ENTERED UNRESOLVED TP1):** Robinhood Chain friction + mixed whale signals. Monitor existing position; no new entry. Partial exit if ETH shows sustained strength.
- **BTC short (B-tier swing, ENTERED UNRESOLVED TP1):** In profit at $60,123 vs ~$62k entry. Warsh bounce = friction. Trail/manage.
- **ME/USDT (B-tier intraday, WAITING):** Negative funding across 3 exchanges (crowding elevated) — contradicts entry signal quality. Watch only.
- **ENA/USDT:** Best catalyst watch (importance 0.73, Blackrock partnership) but single-source only; no active B/A signal in system.
- **RIF/USDT (B-tier intraday/swing, WAITING):** +45.19% 24h — extreme extension, chase risk. `momentum_breakout` basket: wait_pullback.

---

## 8. Best Candidates Ranked

No fully clean NOW-actionable candidate (crypto chop; stocks RTH closed). Routing instead of "no trade":

| Rank | Symbol | Side | Trigger | When |
|------|--------|------|---------|------|
| 1 | JPM | Long | RTH open 16:30 EEST + first 15-min confirmation; SL below 15-min low; 0.5× size (A-tier caution) | Today 16:30 EEST |
| 2 | DYDX/USDT | Short | Dead-cat bounce $0.155–$0.165 fails; OR break below $0.143 on volume; SL $0.175 | When bounce appears |
| 3 | ENA/USDT | Long | Partnership confirmed multi-source + pullback; no entry until verified; SL below support | After verification |
| 4 | BTC short (existing) | Short | ENTERED UNRESOLVED — manage TP trail; no new entry | Ongoing |
| 5 | ETH short (existing) | Short | ENTERED UNRESOLVED — monitor Robinhood Chain friction; no new entry; consider partial | Ongoing |

**Best long-watch:** JPM — trigger: RTH open + 15-min bull candle; SL below 15-min low; 0.5× A-tier sizing.
**Best short-watch:** DYDX/USDT — trigger: $0.155–$0.165 dead-cat bounce failure or $0.143 break; SL $0.175.
**Best catalyst-watch:** ENA/USDT — trigger: Blackrock partnership multi-source confirmed + pullback; importance 0.73.

---

## 9. Avoid / No Trade (this decision window only)

- **UNH:** LEGAL RISK / AVOID. DOJ criminal Medicare fraud probe. A-tier score invalid. No entry any mode.
- **TLM (new entry):** NEEDS HUMAN REVIEW. Binance delisting monitoring + 19× price discrepancy. Existing position needs manual evaluation.
- **SYN intraday (new entry):** Chop market + no catalyst + no-catalyst intraday lane net-negative (−3R playbook). Scalp already triggered by system at research grade.
- **RIF/USDT:** +45% 24h — extreme extension, chase risk. Momentum_breakout basket = `wait_pullback`.
- **Crypto scalp (new entries):** PF 0.14, WR 12%, −6R. Low-confidence class. Size 0.5× on any system-generated scalp signal.
- **Stocks swing/invest:** Paused (swing −12R, 0W/12L; invest −24R, 0W/24L). Watchlist/research only.

*Scanner, tracking, and data collection continue regardless — ALWAYS-SCAN rule in effect.*

---

## 10. Main Risks

1. **UNH DOJ probe in scoring system:** System continues generating A-tier UNH long signals. Legal risk not captured. Each cycle will re-flag until manual intervention. → TODO §14
2. **TLM price discrepancy (19×) unresolved:** System P&L tracking potentially meaningless for TLM. May reflect token version mismatch (Binance vs CoinGecko tracking different contracts). → TODO §14
3. **BTC below $57,891 support:** Would negate Warsh bounce; re-engage June bear trend; stocks likely gap-down at RTH.
4. **Catalyst mapping 69.4% unmapped:** Major events may be missed or misrouted. Context only.
5. **Stocks correlation cluster:** 50 active signals all long. Broad market sell-off would sweep all simultaneously.
6. **DYDX short squeeze risk:** OI +22% fresh shorts pressing. Surprise adoption news / token buyback could cause violent squeeze. Size small.
7. **ETH short catalyst friction:** Robinhood Chain launch is genuine positive catalyst for ETH. Sustained ETH strength could reduce short profit window.

---

## 11. Action Plan — Next 4 Hours (11:39–15:39 EEST)

**Immediate (now):**
- [ ] **HUMAN REVIEW REQUIRED:** TLM swing position — verify entry price, check exit given Binance delisting risk and price discrepancy
- [ ] Monitor DYDX for dead-cat bounce to $0.155–$0.165. Do NOT enter until bounce confirmed and fails
- [ ] Monitor BTC support at $57,891. If revisited, crypto risk-off re-engages

**Pre-RTH planning (13:00–16:00 EEST):**
- [ ] Finalize JPM entry plan; confirm no new JPM-specific adverse headlines; check XLF pre-market momentum
- [ ] AMD B-tier (TP HIT stocks) — assess remaining position
- [ ] Monitor BTC/ETH existing shorts — consider partial exit if BTC sustains above $61k

**RTH open (16:30 EEST):**
- [ ] JPM: First 15-min candle. If bullish and above key level → entry 0.5× size. If red/indecisive → wait
- [ ] XLF B-tier: Confirm sector breadth supports JPM entry

**Ongoing:**
- Scanner, tracking, and catalyst collection continue. No mode changes or system stops.

---

## 12. Final Verdict per Mode

| Mode | Asset | Verdict | Best Setup | Note |
|------|-------|---------|------------|------|
| Crypto scalp | Crypto | **LOW CONFIDENCE** | SYN (already triggered, 0.5× size) | PF 0.14, WR 12%; no new scalps |
| Crypto intraday | Crypto | **WAIT / CATALYST REQUIRED** | DYDX short (dead-cat bounce trigger) | No-catalyst lane = −3R; catalyst required |
| Crypto swing | Crypto | **MONITOR EXISTING** | BTC/ETH shorts (TP1 HIT, manage); TLM → HUMAN REVIEW | Best mode (+2R weekly); TLM open issue |
| Stocks intraday | Stocks | **PLAN / WAIT FOR RTH** | JPM (16:30 EEST trigger, 0.5× size) | A-tier but 0.5× overpromotion rule; AVOID UNH |
| Stocks swing | Stocks | **WATCHLIST ONLY (PAUSED)** | — | −12R, 0W/12L pre-pause |
| Stocks invest | Stocks | **WATCHLIST ONLY (PAUSED)** | — | −24R, 0W/24L |

---

## 13. Sources

- [Bitcoin price today, July 2026 — Finbold](https://finbold.com/bitcoin-price-today-july-2026/) — BTC ~$60,123, low $57,891, June −20.48%
- [Bitcoin Price Prediction July 2026 — CryptoTimes](https://www.cryptotimes.io/2026/07/02/bitcoin-price-prediction-july-2026-will-btc-go-up-or-crash/) — BTC market context
- [UnitedHealth under criminal probe for Medicare fraud — Yahoo Finance](https://finance.yahoo.com/news/unitedhealth-under-criminal-probe-possible-231729520.html) — DOJ criminal probe
- [UNH Faces DOJ Probe, Shares Dive 16% — Nasdaq](https://www.nasdaq.com/articles/unitedhealth-unh-faces-doj-probe-shares-dive-16-fraud-investigation) — shares −16%
- [DOJ criminal probe extends to Optum Rx — FierceHealthcare](https://www.fiercehealthcare.com/payers/wsj-report-doj-interviewing-former-employees-about-medicare-billing-practices-unitedhealth) — expanded probe
- [DYDX Price Crashes After Arcus Debut — BanklessTimes](https://www.banklesstimes.com/articles/2026/07/02/dydx-coin-price-crashes-20-after-arcus-debut-whats-next/) — sell-the-news, vol 673%, price ~$0.1448
- [TLM Binance delisting monitoring — Bitcoin Sistemi](https://en.bitcoinsistemi.com/binance-announces-both-listing-and-delisting-here-are-the-11-altcoins-affected/) — May 22 delisting monitoring
- [TLM price on Binance](https://www.binance.com/en/trade/TLM_USDT) — $0.017206 (Binance spot)
- [TLM price on CoinGecko](https://www.coingecko.com/en/coins/alien-worlds) — $0.0008850 (~19× discrepancy)
- Internal: `data/reports/scalp/2026-07-02_08-02_scalp_report.md`
- Internal: `data/reports/intraday/2026-07-02_08-07_intraday_report.md`
- Internal: `data/reports/swing/2026-07-02_00-58_swing_report.md`
- Internal: `data/reports/stocks/intraday/2026-07-02_08-13_stocks_intraday_report.md`
- Internal: `data/reports/stocks/swing/2026-07-02_00-59_stocks_swing_report.md`
- Internal: `data/catalysts/2026-07-02/catalyst_cycle_08-07.md`
- Internal: `data/processed/llm_analysis_packet.md`
- Internal: `data/processed/llm_stocks_packet.md`
- Internal: CLI `active-signals` × 2, `signal-stats` × 2, `detect_untracked_legacy_alerts`

---

## 14. Fix Requests / TODO

### TODO-unh-legal-scoring
- **issue:** Scoring system generates A-tier UNH long signals despite confirmed active DOJ criminal fraud probe — legal risk not captured in scoring
- **evidence:** UNH score 80.11 (intraday A-tier), 74.95 (swing B-tier); 3rd consecutive review flagging AVOID; catalyst basket `legal_risk` maps to "basket" not UNH symbol directly
- **suggested manual fix:** Add UNH to a manual legal_risk blacklist / score cap in scoring config, or add legal-risk penalty layer in `CatalystRiskAgent`; symbol-level legal risk from catalyst_events should reduce score cap to ≤50 (rejected tier) while probe is active
- **priority:** high
- **first observed:** 2026-07-02 04:39 EEST (3rd cycle flag)

### TODO-tlm-delisting-price-discrepancy
- **issue:** TLM Binance delisting monitoring (May 22, 2026) not reflected in scoring; AND major price discrepancy — Binance $0.0172 vs CoinGecko $0.000885 (~19×). TLM swing long is TRIGGERED/ENTERED.
- **evidence:** Binance spot page $0.017206; CoinGecko $0.0008850; prior review (04:39) noted $0.0013–$0.0014 internal vs $0.000878 CoinMarketCap; 2-cycle-persistent discrepancy
- **suggested manual fix:** (1) Human session: verify TLM entry price in signals DB; (2) Investigate price discrepancy source (possible token migration or different contract addresses); (3) Add delisting_monitoring_list to scoring to cap affected symbols to rejected tier; (4) Determine and execute exit plan if position is real
- **priority:** high
- **first observed:** 2026-07-02 04:39 EEST (escalated this cycle with 19× confirmation)

### TODO-catalyst-mapping-improvement
- **issue:** Catalyst mapping persistently weak — 69.4% unmapped today (826/1190); major events like UNH DOJ probe mapped only to "basket" with null symbol, reducing per-signal utility
- **evidence:** `catalyst_cycle_08-07.md`: 275/285 events as `other_news`; UNH legal_risk basket has null symbol; ENA partnership correctly mapped; stock symbol extraction clearly under-performing
- **suggested manual fix:** Review and improve symbol resolver in catalyst layer; add explicit patterns for major stock tickers (UNH, JPM, LLY, AMD, NVDA, etc.); consider LLM-assisted symbol extraction for "other_news" bucket; target < 40% unmapped
- **priority:** medium
- **first observed:** 2026-07-02 04:39 EEST (93.4% other_news), confirmed persistent at 69.4%
