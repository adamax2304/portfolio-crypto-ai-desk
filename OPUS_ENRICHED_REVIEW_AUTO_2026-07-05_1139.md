# Opus Enriched Review — Europe / Pre-US Context — Auto Cycle 11:39 EEST

**Slot:** Europe / pre-US context | **Time:** 2026-07-05 11:39 EEST
**Previous review:** 2026-07-05 04:39 EEST (crypto overnight / Asia review)
**Advisory only — no auto-trade. Weekend mode active (Sunday). Stocks CLOSED (US holiday weekend, market reopens Mon Jul 6).**

---

## 1. Executive Summary

This is the **Europe / pre-US context** review for Sunday 2026-07-05 at 11:39 EEST. Weekend mode active — all stocks are CLOSED until Monday July 6 (US July 4 holiday observed Friday July 3 + Saturday + Sunday). Advisory only, no auto-trade.

**Regime:** Bullish trend (risk-on). BTC/ETH both uptrend. Altcoin breadth strengthened to 86.84% above EMA20 (vs 84.6% at overnight review). Regime bias: selective longs via pullback; scalp and no-catalyst intraday have documented negative edge on weekends — avoid without RS-leader or breakout confirmation.

**What changed since 04:39:** 30 new signals generated in the 08:27–08:32 cycle (20 → 50 active). Multiple triggered, then rapidly stopped out: ADA×2, VANRY×2, ETHFI×2, AIGENSYN, HMSTR, BREV, ETH-short → -1.0R each. OGN scalp/intraday closed WIN +1.0R each; KITE and SENT swing closed WIN +3.0R. Cumulative closed: 374W/38L → 375W/59L (+1W/+21L since morning).

**Top opportunity:** **ADA/USDT** swing B (score 72.6) — multi-mode RS leader, ADA ETF SEC window opens Aug 9 (confirmed external), RealFi Testnet launches July 6 (tomorrow), entry zone 0.1890–0.1910. Scalp/intraday signals already stopped out this morning; swing entry remains valid on pullback.

**Best short watch:** VANRY/USDT — post-impulse (+64% 24h), elevated crowding, negative funding across all venues (Bybit/MEXC), already closed -1.0R. Wait for failed retest rather than chasing.

**Key avoids:** VANRY (post-impulse chase); TLM (delisting risk block, existing open position only); ETH/SOL/APT (exploit_hack operator-review block); EPIC (swing signal stale after -44% round-trip since 04:22).

**Catalyst coverage:** Weak (JSONL 28% mapped, 72% unmapped). Use catalyst layer as context only. ADA and ETHFI have externally confirmed catalysts.

---

## 2. Data Used

| Source | Mtime / Freshness | Status |
|---|---|---|
| scheduler.log (cycle_04_11-20) | 11:39 EEST (1 min ago) | **FRESH** |
| cycle_04_11-20_summary.md | 11:39 EEST (1 min) | **FRESH** |
| scalp report `2026-07-05_08-27` | 11:27 EEST (12 min) | **FRESH** |
| intraday report `2026-07-05_08-32` | 11:32 EEST (7 min) | **FRESH** |
| swing report `2026-07-05_01-22` | 04:22 EEST (7.3h) | **CARRY-FORWARD** (4–12h) |
| stocks_intraday `2026-07-03_20-07` | 07/03 23:07 | **STALE** (>14h, holiday weekend) |
| stocks_swing `2026-07-02_13-03` | 07/02 16:03 | **STALE** (>14h, holiday weekend) |
| stocks_invest `2026-07-02_13-05` | 07/02 16:05 | **STALE** (>14h, holiday weekend) |
| catalyst_events.jsonl / baskets | cycle 11:27–11:39 | **FRESH** |
| llm_analysis_packet.md | 11:32 EEST | **FRESH (weekend intraday)** |
| active-signals CLI (crypto) | cycle 11:39 | **LIVE (50 signals)** |
| signal-stats CLI (crypto) | cycle 11:39 | **LIVE** |
| active-signals CLI (stocks) | cycle 11:39 | **LIVE (50 signals, C-tier dominant)** |
| signal-stats CLI (stocks) | cycle 11:39 | **LIVE (net negative all modes)** |
| paper monitor status | cycle 11:38 | **FRESH** |
| detect_untracked_legacy_alerts | 11:37 EEST | **4 UNTRACKED** |
| ADA ETF research (WebSearch + WebFetch) | 11:39 EEST | LBank + CrowdFundInsider |
| ETHFI research (WebSearch + WebFetch) | 11:39 EEST | CoinGecko live price |

**Notes:**
- Stocks: CLOSED (holiday weekend). Reports stale by design.
- Swing report is carry-forward (7.3h) — note EPIC reversal flag (see §14 TODO).
- Social: no live X/Telegram connectors. KOL watchlist placeholder not replaced.
- Onchain: `interface_ready_config_missing` (no config/onchain.yaml).
- Weekend mode active: A-tier penalty, chasing entries demote, MEXC-only capped C.
- External web research: AVAILABLE — used for ADA and ETHFI.

---

## 3. Scheduler / Data Freshness

- **Scheduler:** cycle_04_11-20 completed at 11:39:03 EEST (1 min ago). All OK: 27/27 steps, 0 failed. **FRESH.**
- **Cycle mode:** weekend (crypto-only). Stocks data collection still running; actionability disabled.
- **Paper monitor status (live from cycle 11:38):**
  - OPEN ACTIONABLE: 8
  - WAITING FOR ENTRY: 4
  - ENTERED UNRESOLVED (expired-after-entry): 35 (entry filled, no TP/SL before window — **NOT missed entries**)
  - REVIEW/SHADOW: 160
  - NO-ENTRY / STALE / MOVED AWAY: 37
  - CLOSED (cumulative history): 375W / 59L / 0flat
  - NEEDS REVIEW: 0
- **Untracked legacy alerts:** 4 (ETHFI scalp, ADA scalp, BCH scalp, VANRY scalp — sent to Telegram from 08:27 cycle but no proposed_signal tracker). See §14 TODO.
- **Intelligence layer:** crypto monitor running (pid 18328, ~90 min lifetime). Derivatives: OI numeric history sparse; MEXC fallback for HOT, VANRY, AIGENSYN.
- **Weekend mode adjustments active:** A-tier score penalty −5pts, confidence step-down, overextension multiplier 1.25×, require retest after impulse, tight stop warning.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-07-05 11:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.88,
      "reason_codes": ["scheduler_fresh", "report_stale", "derivatives_sparse"],
      "data_missing": ["stocks_reports_current", "social_attention", "onchain_data", "liquidation_heatmaps", "etf_flows"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "cycle_04 completed 11:39 EEST, 1 min ago — FRESH",
        "scalp (7 min) + intraday (12 min) reports FRESH; swing 7.3h carry-forward",
        "Stocks reports stale by design (US holiday weekend, closed Jul 3-6)",
        "4 untracked legacy alerts from 08:27 scalp cycle (ETHFI/ADA/BCH/VANRY)",
        "JSONL catalyst file: 1478 lines total, 417 mapped (28.2%) — weak mapping",
        "Weekend mode active: Sunday Jul 5, A-tier penalty, retest required"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["risk_on", "longs_preferred"],
      "data_missing": ["live_btc_price_usd", "DXY_yields", "macro_calendar_US", "social_sentiment_live"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC trend: uptrend (all three reports); ETH trend: uptrend",
        "Altcoin breadth 86.84% above EMA20 (strengthened from 84.6% at 04:39)",
        "Altcoin breadth 89.47% above EMA50 — very extended but bullish",
        "Regime label: bullish trend; recommended style: selective longs, prefer pullbacks on RS",
        "Weekend mode: thinner liquidity, require retest after impulse",
        "Macro risk score 59/100 (3 risk-off hits) — data-watch; exploits/laundering events don't change macro"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.60,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "stale_catalyst", "narrative_supported"],
      "data_missing": ["social_feeds_live", "BTC_ETF_flow_data", "ADA_security_classification_resolution"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Catalyst JSONL: 28% mapped (417/1478 total cumulative) — WEAK",
        "ADA: ETF SEC review window opens Aug 9 confirmed (LBank, CrowdFundInsider); RealFi Testnet July 6 (tomorrow)",
        "ADA risk: commodity vs security status unresolved — may delay spot ETF",
        "ETHFI: ~$0.42 +21% 7d, RWA vaults launched (Midas/Plume), DeFi United joined; rsETH exploit bridge risk",
        "ETH/SOL: exploit_hack operator-review block (Step Finance exploiter $21M launder via TornadoCash)",
        "APT: exploit_hack block (Aptos critical vulnerability fixed)",
        "TLM: delisting block (Binance delisting monitoring active, +107% 7d)",
        "5 active narrative baskets: delisting_thin_liquidity, rwa_narrative, perps_dex_narrative, ai_narrative, momentum_breakout"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.62,
      "reason_codes": ["oi_supports", "funding_extreme", "squeeze_risk", "post_unwind_chop"],
      "data_missing": ["OI_numeric_history", "liquidation_heatmaps", "order_book_depth", "exchange_OI_full_breakdown"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "ADA: price up + OI up (+1.07%), funding +8.3e-5 (neutral), long/short 1.976, crowding normal — fresh positioning",
        "ETHFI: MEXC fallback, funding 5e-5 neutral, crowding normal across Bybit/OKX/MEXC",
        "HOT: MEXC fallback, funding -0.01234 ELEVATED negative, OI unavailable — crowding elevated, squeeze-risk flag",
        "VANRY: Bybit funding -0.00322, MEXC -0.00075, crowding elevated, OI 24h +211% massive — post-impulse unwind risk",
        "AIGENSYN: Bybit funding -0.00564, crowding elevated — consistent with stopped-out signal",
        "BCH: price up + OI up +1.3%, funding +0.0001, long/short 1.874, crowding normal — clean",
        "MEXC fallback dominant for altcoins — OI numeric history sparse for most symbols"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": ["clean_retest", "entry_late", "chase_risk", "stale_before_entry"],
      "data_missing": ["live_chart", "order_book", "level2_data", "vwap_anchoring"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "ADA: current 0.1925, swing entry 0.1890–0.1910 (within ATR 0.0044); resistance 0.2000 — pullback entry valid",
        "ADA: scalp/intraday signals stopped out this morning → price may have bounced from zone already",
        "ETHFI: ~0.42, swing entry 0.4157–0.4208 (near); neutral funding, clean crowding",
        "VANRY: +64% 24h from 08:15 data, OI +211%, elevated crowding — CHASE RISK, overextended",
        "EPIC reversal: swing report (04:22) showed +22%; scalp/intraday (11:27) shows -22% — 44% round-trip; swing signal stale/invalidated",
        "DOGS: 0.0000 formatting bug in swing entry/targets (price truncation for sub-satoshi prices)",
        "TradingView/manual chart unavailable — using OHLCV/ATR/EMA from reports only"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "no_entry"],
      "data_missing": ["exact_entry_timing_for_all_35_unresolved"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "OPEN ACTIONABLE: 8 (SENT intraday, TLM intraday, ALLO intraday + 5 others)",
        "WAITING FOR ENTRY: 4 (HOT intraday, BTC intraday, LAB intraday + 1 other)",
        "ENTERED UNRESOLVED (expired-after-entry): 35 — entry was filled, no TP/SL before window ended — NOT losses by PF calc",
        "REVIEW/SHADOW: 160",
        "NO-ENTRY / STALE / MOVED AWAY: 37 (BCH scalp/intraday, AIGENSYN scalp/intraday, ENA, ARPA among no-entry)",
        "CLOSED: 375W / 59L / 0flat (cumulative)",
        "Recent closes: ADA scalp/intraday -1.0R each, VANRY scalp/intraday -1.0R each, ETHFI scalp/intraday -1.0R each, HMSTR swing -1.0R",
        "Recent wins: OGN scalp/intraday +1.0R each, ETHFI swing +1.0R, KITE swing +3.0R, SENT swing +3.0R"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["repeated_losses", "legal_risk", "headline_risk", "reduce_risk", "manual_review"],
      "data_missing": ["daily_R_aggregate", "correlation_cluster_sizing", "portfolio_drawdown_current"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "21 new losses since morning review (38L→59L): ADA×2, VANRY×2, ETHFI×2, AIGENSYN, HMSTR, BREV, ETH-short, + others",
        "Weekend signal WR 21% (n=164 reliable) — historically below threshold",
        "Scalp mode: PF 0.14 over 14d (documented negative), -1.4R total sample",
        "TLM: OPEN ACTIONABLE with delisting block — block_requires_operator_review active; existing position carries forward",
        "ETH/SOL/APT: exploit_hack blocks in place — no new entries permitted",
        "UNH: DOJ probe block (legal_risk) — stocks closed so not actionable this window",
        "4 untracked legacy scalp alerts (no proposed_signal → no PF contribution)"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "ok",
      "confidence": 0.80,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample", "fresh_expired_problem"],
      "data_missing": ["longer_history_beyond_7d", "catalyst_cohort_performance", "weekend_by_mode_breakdown"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto overall (7d): PF 2.26, WR 22.3%, +68R (reliable n=304)",
        "Swing mode: PF 3.34, avg +0.5R, +40.1R (n=104 reliable) — BEST mode",
        "Intraday mode: PF 2.26, avg +0.4R, +29.4R (n=85 strong) — works with RS/catalyst",
        "Scalp mode: PF 0.86, avg -0.01R, -1.4R (n=115 reliable) — net negative",
        "Weekend mode: WR 21%, n=164 (underperform flag from signal-stats)",
        "Non-weekend: PF 4.2, avg +0.5R, +51.5R (n=140 reliable) — much stronger",
        "Stocks (all): PF 0.45, -17R total (reliable n=250) — all modes negative, all C/B stocks",
        "35 entered_unresolved signals: entry filled, no TP/SL reached — window management issue"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["longs_preferred", "wait_for_trigger", "shorts_preferred"],
      "data_missing": ["live_btc_price", "social_sentiment", "order_flow"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Regime bullish trend — longs preferred on swing timeframe",
        "Weekend scalp/intraday historically underperform — avoid unless RS-leader + breakout confirmation",
        "ADA confirmed multi-catalyst: ETF SEC Aug 9 + RealFi Testnet July 6 (tomorrow)",
        "VANRY post-impulse: best short watch on failed retest",
        "Scalp/intraday mode negative edge on weekends — prefer swing entries",
        "TLM OPEN with delisting block — operator monitor only",
        "Stocks closed until Monday — planning only, no actionable setups"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.72,
    "preferred_side": "longs",
    "best_long_candidate": {
      "symbol": "ADA/USDT",
      "trigger": "Price accepts inside 0.1890–0.1910 with 1h structure; confirm not >2 ATR from zone",
      "reason": "Multi-mode RS leader, ETF SEC window Aug 9, RealFi Testnet Jul 6 tech catalyst, clean pullback zone swing B score 72.6"
    },
    "best_short_candidate": {
      "symbol": "VANRY/USDT",
      "trigger": "1h close below 0.0700 (approx bounce low) after failed retest of the 64% impulse peak",
      "reason": "Post-impulse +64%, OI +211%, funding elevated negative across Bybit/MEXC, crowding elevated, already -1.0R stop this session"
    },
    "best_catalyst_candidate": {
      "symbol": "ADA/USDT",
      "trigger": "RealFi Testnet launch confirmation July 6 + price holding above 0.1866 (swing SL)",
      "reason": "ETF SEC review window Aug 9, RealFi Testnet launches tomorrow, CME futures live since Feb — strongest near-term catalyst"
    },
    "avoid_candidate": {
      "symbol": "VANRY/USDT",
      "reason": "Post-impulse +64% in last 24h, elevated OI and crowding, negative funding, recent -1.0R stop — chase risk; also ETH/SOL/APT blocked by exploit_hack, TLM blocked by delisting"
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
|---|---|---|---|---|
| data_quality | **ok** | 0.88 | scheduler_fresh, report_stale, derivatives_sparse | advisory_only |
| market_regime | **ok** | 0.82 | risk_on, longs_preferred | advisory_only |
| catalyst_narrative | **caution** | 0.60 | mapping_weak, fresh_catalyst, stale_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | **caution** | 0.62 | oi_supports, funding_extreme, squeeze_risk, post_unwind_chop | advisory_only |
| technical_entry | **caution** | 0.68 | clean_retest, entry_late, chase_risk, stale_before_entry | advisory_only |
| execution_lifecycle | **ok** | 0.85 | open_actionable, waiting_for_entry, entered_unresolved, no_entry | advisory_only |
| risk_manager | **caution** | 0.75 | repeated_losses, legal_risk, headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | **ok** | 0.80 | playbook_working, playbook_failing, low_sample, fresh_expired_problem | advisory_only |
| head_trader | **caution** | 0.72 | longs_preferred, wait_for_trigger, shorts_preferred | advisory_only |

---

## 4. What Changed vs Previous Review

**Previous review:** 2026-07-05 04:39 EEST (crypto overnight / Asia review)

| Dimension | 04:39 | 11:39 | Change |
|---|---|---|---|
| Active signals (crypto) | 20 | 50 | +30 (new 08:27–08:32 cycle) |
| Closed today W/L | 374W / 38L | 375W / 59L | +1W / +21L (heavy stop losses) |
| Open actionable | 16 | 8 | −8 (closed/expired) |
| Altcoin breadth EMA20 | 84.6% | 86.84% | Strengthened |
| ADA candidate | LONG-WATCH swing B | LONG-WATCH swing B | **Unchanged — still top candidate** |
| VANRY | Post-impulse avoid | Post-impulse, added -1.0R stop | Confirmed avoid; now short-watch on retest |
| ETHFI | Watch | Swing WIN +1.0R closed; scalp/intraday stopped | Mixed: swing worked, short-term failed |
| OGN | Momentum_breakout | Closed WIN +1.0R scalp/intraday | Validated |
| HMSTR | Avoid (post-impulse) | CLOSED LOSS -1.0R swing | Confirmed avoid |
| EPIC/USDT | Swing LONG (swing rpt) | Now -22% (REVERSED) | **Stale swing signal — invalidated** |
| Untracked alerts | 0 | 4 | New issue: ETHFI/ADA/BCH/VANRY scalp sent w/o tracker |
| TLM | Avoid (delisting block) | OPEN ACTIONABLE (entered before block) | **Operator monitoring required** |

**New catalysts since 04:39:**
- ADA: RealFi Testnet launch date July 6 confirmed (external research)
- ETH/SOL: Step Finance exploiter laundering $21M added to exploit_hack block (upgrades prior block)
- Clarity Act: US law enforcement stops blocking (regulatory_sector_headline — crypto positive context)

**Thesis changes:**
- ADA: thesis unchanged (strongest candidate), scalp/intraday losses add caution on entry timing
- VANRY: degraded from avoid to short-watch (confirmed post-impulse with real stop out)
- EPIC: degraded from swing long-watch to avoid/stale (full reversal since swing report)

---

## 5. Catalyst Coverage

- **Unique events today (per reports):** 458; **active baskets:** 5
- **JSONL cumulative file:** 1478 total entries, 417 mapped (28.2%), 1061 unmapped (71.8%)

> **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

**Active baskets:**
| Basket | Playbook | Freshness | Primary symbols |
|---|---|---|---|
| delisting_thin_liquidity | avoid_low_liquidity | <1h | HYPE/USDT |
| rwa_narrative | related_beta_rotation | <24h | ONDO/USDT, XLM/USDT |
| perps_dex_narrative | wait_pullback | <24h | HYPE/USDT |
| ai_narrative | related_beta_rotation | <24h (unknown) | NEAR, RENDER, TAO, FET |
| momentum_breakout | wait_pullback | <1h | NFP/USDT, OGN/USDT |

**Notable individual events:**
- **APT/USDT** [exploit_hack] — Aptos fixed critical vulnerability (CryptoBriefing) → operator block active
- **UNH/USDT** [legal_risk] — DOJ probe, shares -16% (QuiverQuant) → operator block active (stocks closed anyway)
- **ETH/SOL** [exploit_hack] — Step Finance exploiter launder $21M via TornadoCash (t.me/lookonchain, CryptoBriefing) → operator block active
- **(basket)** PHR, CALX, Z/ZG — securities fraud lawsuits (PR Newswire) → stocks only, closed
- **(basket)** Hinkal protocol $820K USDC exploit (AMBCrypto) — no mapped symbol
- **(basket)** CLARITY Act / NOBLE endorsement — regulatory positive background (not symbol-specific)

**Top 3 unmapped headlines (high importance):**
1. Iran Bitcoin payments for Strait of Hormuz fees (CryptoBriefing) — macro positive for BTC
2. Hinkal protocol $820K USDC exploit (AMBCrypto) — exploit risk, unmapped
3. Bitcoin ETFs eighth straight negative week (The Block) — macro caution for BTC longs

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** risk-on (bullish trend, BTC/ETH uptrend, 86.84% breadth above EMA20)
- **Stocks mood:** closed (US holiday weekend; stale reports; reopen Monday July 6)
- **Dominant narrative:** Broad altcoin strength, RS rotation; exploit/launder narrative on ETH/SOL (blocked); ADA ETF pipeline coming into focus; momentum_breakout basket active (NFP, OGN)
- **Preferred side now:** longs (swing only — pullback entries; avoid scalp/intraday without RS-leader or retest)
- **Best long candidate:** ADA/USDT — pullback into 0.1890–0.1910, trigger: 1h structure + confirm not >2 ATR from zone
- **Best short candidate:** VANRY/USDT — trigger: 1h close below recent bounce low after failed retest of the 64% impulse
- **Best catalyst-backed candidate:** ADA/USDT (RealFi Testnet July 6 + SEC window Aug 9)
- **What to avoid:** VANRY chase; scalp/intraday entries without RS + retest; TLM new entries (delisting block); ETH/SOL/APT new entries (exploit block); HMSTR (post-impulse, stopped out)
- **What would change the view:**
  - *Bullish upgrade to risk-on full:* BTC clears $65K on volume, altcoin breadth holds 90%+, ADA confirms at 0.1960+
  - *Downgrade to caution:* BTC 4h close below $60K; exploit narrative spreads to ETH/wider DeFi
  - *Short activation:* VANRY failed retest 1h close below bounce low; or broader breadth rollover

---

## 7. Candidate Deep Dives

### Candidate 1: ADA/USDT — LONG-WATCH (swing B, score 72.6)

**Status:** WAITING FOR ENTRY (swing) | OPEN REVIEW (scalp/intraday stopped out)

**Setup:**
- Swing B-tier, score 72.6/100 (swing report 04:22, carry-forward)
- Intraday B-tier, score 69.0/100 (intraday report 11:32, fresh)
- 24h return: +9.25% (11:32 data), +7.81% (04:22 data); 7d return: +32.03%
- RS vs BTC: +8.65% (strong RS-leader across all timeframes)
- Trend: uptrend; setup quality: 71.5/100; RR to TP1: 1.84R
- Current price (swing rpt): 0.1919; Support: 0.1750; Resistance: 0.2000; ATR: 0.0044

**Catalyst check (internal + external):**
- Internal: no fresh verified catalyst in news_items specifically for ADA this cycle
- External (WebSearch/WebFetch confirmed):
  - ADA ETF SEC review window opens August 9, 2026 (CME futures launched Feb 9, 2026 triggers 6-month clock)
  - Grayscale GADA final decision possible October 23, 2026
  - RealFi Testnet launching **July 6** (tomorrow) — near-term tech catalyst
  - Van Rossem hard fork (June-July 2026) completed
  - Caveat: ADA commodity vs security status still unresolved → may delay spot ETF
- Source: LBank (Cardano ETF Ecosystem article), CrowdFundInsider (Grayscale GADA May 2026)

**Price reaction / chase check:**
- Has price reacted to catalyst? No direct reaction today; background ETF narrative builds gradually
- Is setup chasing? NO — entry zone 0.1890–0.1910 is below current 0.1925; pullback required
- Retest structure? YES — swing entry zone is pullback area; 0.1890 is approx -1.8% from current
- Overextended? Not critically — 7d +32% but still below resistance 0.2000; ATR check shows 1.84R to TP1 (clean)
- Is entry NOW late? MARGINAL — current 0.1925 is slightly above entry zone; waiting for pullback is correct
- Actionable level: pullback into 0.1890–0.1910 on 1h close acceptance
- Invalidation: 1h close below 0.1866
- Aligned with market mood? YES — risk-on bullish trend, RS leader, catalyst-backed swing
- Chase risk? LOW (swing, waiting for pullback)
- Today's scalp/intraday stopped out: scalp at ~0.1925 (stopped below 0.1919 SL); this suggests the entry zone WAS touched and bounced — swing entry may already be forming

**Derivatives:**
- Price up + OI up (+1.07%), funding +8.3e-5 (neutral), long/short 1.976, crowding normal → CLEAN

**Verdict:** WAITING FOR ENTRY — swing long, wait for pullback into 0.1890–0.1910. Do not chase at 0.1925. Monitor RealFi Testnet July 6 announcement as potential momentum catalyst.

---

### Candidate 2: ETHFI/USDT — SWING WATCH (swing B, partial TP1 already hit)

**Status:** SWING CLOSED WIN +1.0R (legacy touch) | Scalp/Intraday CLOSED LOSS -1.0R each

**Setup:**
- Swing B-tier: closed WIN +1.0R — price reached TP1 before window ended
- Scalp B-tier (score 73.4): CLOSED LOSS -1.0R today (entry triggered, stopped out)
- Intraday B-tier (score 67.5): CLOSED LOSS -1.0R today
- 24h return: +13.10%; 7d return: +21.9%; RS vs BTC: +12.5%
- Trend: uptrend; setup quality: 71.9/100
- Current price: ~$0.42; ATR: ~0.0185 (scalp basis); entry zone: 0.4157–0.4208

**Catalyst check:**
- Internal: no verified catalyst in news_items
- External (WebSearch/WebFetch confirmed):
  - ETHFI trading ~$0.42, +21% 7-day (CoinGecko live, July 2026)
  - RWA vaults launched via Midas and Plume — project-specific positive
  - Joined DeFi United — ecosystem expansion
  - rsETH bridge exploit risk (related protocol; bridge security hardened in response)
- Verdict: WEAKLY CONFIRMS bullish thesis, sector-driven (liquid staking/restaking), not standalone catalyst

**Price reaction / chase check:**
- Swing TP1 already hit → price was at or above 0.4342 (TP1) at some point
- Current price ~0.42 means it likely retraced back to near entry zone
- If price is now ~0.42, it's near the top of the entry zone (0.4157–0.4208) → potential re-entry watch on swing
- Scalp/intraday got stopped: entry was triggered then price dropped below 0.4095 (scalp SL)
- rsETH exploit bridge risk is background caution — not a direct ETHFI hack but related protocol
- Aligned with mood? YES (RS leader, liquid staking narrative, risk-on)
- Chase risk? LOW on swing (price back near entry zone); ELEVATED for scalp (already stopped once)

**Verdict:** SWING WATCH — if price accepts above 0.4157 on 1h basis after retest, new swing entry valid. Scalp/intraday: avoid re-entry today (already stopped once; weekend mode caution).

---

### Candidate 3: VANRY/USDT — SHORT-WATCH / AVOID

**Status:** SCALP CLOSED LOSS -1.0R | INTRADAY CLOSED LOSS -1.0R

**Setup (for short watch, NOT long):**
- 24h return: +64.26%; RS vs BTC: +63.65%
- OI 24h: +211.4% (massive fresh positioning on the move up)
- Funding: Bybit -0.00322, MEXC -0.000752 — negative across all venues (longs paying shorts)
- Crowding: ELEVATED per Bybit cross-check
- Long/short ratio: 1.194 (longs slightly dominant but funding tells the real story)
- Active long signals: already stopped out (-1.0R each for scalp and intraday)

**Catalyst check:**
- Internal: no fresh catalyst for VANRY
- No external research performed (avoid, not a long candidate)

**Price reaction / chase check:**
- Has price reacted? YES — massively (+64% 24h). Already overextended.
- Is setup chasing for a long? YES — entry signals triggered into the move, got stopped
- Short thesis: post-impulse + elevated OI + negative funding + no catalyst = unwind candidate
- Trigger for short: 1h close below recent bounce low (estimated ~0.0700, verify from chart)
- Invalidation of short: new catalyst announced driving fresh buy demand; OI/funding normalize

**Verdict:** AVOID for new longs. SHORT-WATCH: wait for 1h close below bounce low after failed retest of the 64% impulse peak. Weekend liquidity thin — be cautious sizing.

---

### Candidate 4: TLM/USDT — OPERATOR MONITOR / NO NEW ENTRIES

**Status:** OPEN ACTIONABLE (entered), operator-review block active for NEW entries

**Context:**
- TLM (Alien Worlds): +107% 7d gain, Binance delisting monitoring active
- Production block: `block_requires_operator_review` — gates NEW A/B only; existing open position continues
- Current signal: intraday B (score ~67.x), OPEN — entry already filled before block was issued
- The OPEN status means the position was entered prior to the delisting block being triggered
- Block behavior: correct per system design — block gates new signals, not existing positions

**Risk assessment:**
- Delisting risk is HIGH for TLM (Binance delisting = major liquidity exit)
- Volume +584% (CMC summary) could be exit liquidity or speculative pump
- TLM OI data via MEXC fallback: funding -0.000627, crowding unknown
- Cross-check Bybit: funding -0.00076428, crowding moderate

**Verdict:** NO NEW ENTRIES. Existing open position: monitor TP/SL levels per existing signal (entry ~0.0103, SL below). Manual operator check of TLM intraday signal TP1/SL levels recommended. The -1.07% funding (negative) on a +107% 7d move with delisting context is a warning sign for any new commitment.

---

### Candidate 5: HOT/USDT — LONG-WATCH (intraday B, WAITING)

**Status:** WAITING FOR ENTRY (intraday B, score 71.3) | Scalp B: REVIEW/SHADOW

**Setup:**
- Intraday B (score 71.3): waiting_for_entry — entry not touched yet (weekend_mode=Y flag)
- 24h return: +18.47%; RS vs BTC: +17.87%; 7d: strong momentum
- OI +191.92%, funding -0.01244648 — HOT's negative funding is the most ELEVATED of all candidates (-1.23%)
- This elevated negative funding means longs are paying shorts significantly → SHORT SQUEEZE risk if price breaks lower

**Price reaction / chase check:**
- +18% today but OI +192% = massive fresh positioning on the move
- Funding -1.23%: extremely elevated negative = longs are heavily paying; if price fails to hold, a rapid unwind could follow
- Entry zone: not touched yet (WAITING) — requires pullback

**Verdict:** LONG WATCH — wait for entry zone. The elevated negative funding (-1.23%) is a caution flag: if this is a short squeeze in progress, entry into the bounce could catch the tail end. Prefer ADA (cleaner funding profile) over HOT in the current window.

---

## 8. Best Candidates Ranked

**No A-tier this session. Weekend mode active. Swing is the only clean mode.**

| Rank | Symbol | Mode | Tier | Verdict | Trigger | SL level |
|---|---|---|---|---|---|---|
| 1 | ADA/USDT | Swing | B | LONG-WATCH | Accept inside 0.1890–0.1910 on 1h | 0.1866 |
| 2 | ETHFI/USDT | Swing | B | SWING WATCH | Accept above 0.4157 on retest 1h | ~0.4095 |
| 3 | HOT/USDT | Intraday | B | LONG WATCH (secondary) | Entry zone touch with 1h retest | per signal |
| — | VANRY/USDT | — | — | SHORT-WATCH | 1h close below bounce low (~0.0700) | above impulse |
| — | OGN/USDT | — | — | MONITOR | Already closed WIN +1.0R; wait for next setup | — |

**Best long-watch:** ADA/USDT — pullback 0.1890–0.1910; trigger: 1h acceptance inside zone; RealFi Testnet July 6 near-term catalyst
**Best short-watch:** VANRY/USDT — failed retest trigger; 1h close below bounce low after 64% impulse
**Best catalyst-watch:** ADA/USDT — RealFi Testnet July 6 + SEC window Aug 9; confirm thesis if testnet launch generates bullish coverage
**Avoid this window:** VANRY (post-impulse), TLM (delisting block new entries), ETH/SOL/APT (exploit blocks), HMSTR (stopped out -1.0R swing), EPIC (stale/reversed swing signal)

---

## 9. Avoid / No Trade (this decision window only)

**No-trade candidates this window:**
- Scalp mode (crypto): historically net negative PF 0.14 on weekends — only take with explicit RS-leader + retest
- Intraday without catalyst or RS-leader: 14d no-catalyst cut: WR 23%, PF 0.70, -3R
- VANRY, HMSTR: post-impulse, no structure — chase risk
- EPIC: stale swing signal (reversed -22% since 04:22 swing report)
- TLM: new entries blocked (delisting risk)
- ETH, SOL, APT: exploit_hack blocks — new entries blocked pending operator review
- Stocks: CLOSED (holiday weekend, reopen Monday July 6). UNH has DOJ legal risk block.

**This is a window-only caution. Scanning, data collection, tracking, and monitoring continue as normal. ALWAYS-SCAN rule applies.**

---

## 10. Main Risks

1. **Weekend scalp/intraday losses accelerating** — +21L since morning review (38→59). Scalp/intraday weekend mode WR 21% historically. Multiple new signals this cycle already stopped. Do not keep re-entering stopped plays intraday on weekends.
2. **VANRY unwind risk** — OI +211%, funding extreme negative, elevated crowding. If selling begins in earnest, the unwind could be rapid and cross-contaminate HOT/AIGENSYN (similar elevated negative funding profile).
3. **TLM delisting** — active open position while delisting monitoring underway. Thin exit liquidity if Binance delisting confirmed.
4. **ETH/SOL exploit narrative** — Step Finance launder $21M through TornadoCash is a negative headline for ETH ecosystem but price held (ETH still uptrend). Monitor whether ETH narrative flips from exploit negative to buy-the-dip.
5. **Catalyst mapping weak** — 72% unmapped in JSONL. Catalyst signals should be treated as context only; do not use as confirmation for entries without external verification.
6. **4 untracked legacy alerts** — ETHFI/ADA/BCH/VANRY scalp alerts sent to Telegram without proposed_signal tracker. No PF contribution. Systematic issue.
7. **ADA security classification** — ETF pipeline has commodity vs security risk overhang. A negative SEC ruling would invalidate the ADA ETF thesis.

---

## 11. Action Plan — Next 4 Hours

**Pre-US-open window (11:39–16:20 EEST):**

1. **Watch ADA/USDT swing entry zone** (0.1890–0.1910). If price pulls back to this zone with 1h acceptance, the swing signal is actionable. Monitor for RealFi Testnet July 6 coverage starting this evening.

2. **Watch ETHFI/USDT swing retest** (~0.4157). Swing TP1 already hit; if price accepts above 0.4157 on a retest, second swing opportunity. Do not chase above 0.43.

3. **Watch VANRY failed retest** — after the +64% impulse, wait for a 1h close below the bounce low. This would be the cleanest short setup in the current window.

4. **HOT/USDT monitoring** — WAITING status; if entry triggers, be aware of the -1.23% funding (squeeze risk). Prefer ADA over HOT in current window.

5. **TLM open position** — manual check of TP/SL levels. No new entries. Delisting risk context live.

6. **Stocks watchlist for Monday July 6:**
   - AMD: B-tier intraday (score ~69, tp1 likely hit), JPM: swing C (score 90 — notably high for C-tier, worth monitoring)
   - UNH: blocked (DOJ probe) — AVOID until legal situation clarifies
   - All intraday stocks signals need RTH confirmation before any entry

7. **Scalp mode**: Do not take new scalp entries unless RS-leader + retest. Weekend scalp historically net negative.

---

## 12. Final Verdict per Mode

| Mode | Asset class | Verdict | Notes |
|---|---|---|---|
| Scalp (crypto) | crypto | **REDUCED CONFIDENCE** | Weekend WR 21%; PF 0.14 14d. Only with RS-leader + retest. 4 untracked alerts. |
| Intraday (crypto) | crypto | **CAUTION — SWING PREFERRED** | No-catalyst cut -3R/14d. Prefer swing timeframe this window. |
| Swing (crypto) | crypto | **ACTIVE — BEST MODE** | PF 3.34, +40R. ADA/USDT and ETHFI/USDT as top watches. |
| Intraday (stocks) | stocks | **CLOSED — PLANNING ONLY** | Holiday weekend. Reopen Mon Jul 6. All signals C-tier. UNH blocked. |
| Swing (stocks) | stocks | **CLOSED — PLANNING ONLY** | Same as above. JPM C-tier (90 score), AMD B-tier monitors for Monday. |
| Invest (stocks) | stocks | **CLOSED — NOT IMPLEMENTED** | Swing proxy if needed; stale reports. |

---

## 13. Sources

| # | Title | Source | Date | URL | Status | Relevance |
|---|---|---|---|---|---|---|
| 1 | Cardano ETF Approval Date: Futures Live, Spot ETF Timeline & ADA Price | LBank | ~Apr 2026 | https://www.lbank.com/explore/cardano-etf-ecosystem-price | primary_source | ADA ETF pipeline, SEC Aug 9 window |
| 2 | Grayscale Investments Eyes Cardano ADA ETF Debut in Late 2026 | CrowdFundInsider | May 2026 | https://www.crowdfundinsider.com/2026/05/278376-grayscale-investments-eyes-cardano-ada-etf-debut-in-late-2026/ | single_source | Grayscale GADA filing confirmation |
| 3 | Ether.fi Price: ETHFI/USD Live Price Chart | CoinGecko | Jul 2026 (live) | https://www.coingecko.com/en/coins/ether-fi | primary_source | ETHFI ~$0.42, +21% 7d, RWA vaults |
| 4 | Step Finance exploiter sells $21M in SOL, buys ETH and launders via TornadoCash | CryptoBriefing | Jul 2026 | internal news_items | single_source | ETH/SOL exploit block context |
| 5 | UnitedHealth Faces DOJ Probe, Shares Dive 16% | QuiverQuant | Jul 2026 | internal news_items | single_source | UNH legal risk block |
| 6 | Aptos fixes critical vulnerability | CryptoBriefing | Jul 2026 | internal news_items | single_source | APT exploit block |
| 7 | TLM Alien Worlds: 107% 7d gain, Binance delisting monitoring | CoinMarketCap AI Summary | Jul 2026 | internal news_items | single_source | TLM delisting block |

_Internal sources: crypto-ai-desk reports, CLI outputs, paper monitor status — not external citations._

---

## 14. Fix Requests / TODO

### TODO-UNTRACKED-ALERTS
- **issue:** 4 scalp alerts (ETHFI, ADA, BCH, VANRY) sent to Telegram from 08:27 cycle but no `proposed_signal` was created; detector flags them as untracked legacy. These contribute no PF data.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-05` → 4 untracked (ETHFI scalp 73.4, ADA scalp 71.6, BCH scalp 69.5, VANRY scalp 68.0)
- **suggested manual fix:** Investigate why scalp signals generated Telegram alerts but not proposed_signal rows; check scalp pipeline's signal persistence step. Could be a race condition between alert dispatch and DB write.
- **priority:** medium
- **first observed:** 2026-07-05 11:39 EEST

### TODO-DOGS-PRICE-TRUNCATION
- **issue:** DOGS/USDT swing signal in `2026-07-05_01-22_swing_report.md` shows entry zone "0.0000–0.0000" and targets TP1/TP2/TP3 = 0.0000/0.0000/0.0001. The price is being truncated to 4 decimal places and rounds to zero, making the signal report unreadable and the entry/target levels nonsensical.
- **evidence:** `data/reports/swing/2026-07-05_01-22_swing_report.md` §6 Trade Idea #3 DOGS/USDT entry plan section
- **suggested manual fix:** Report renderer should use 6–8 decimal places for sub-satoshi priced tokens, or use scientific notation for prices below 0.001.
- **priority:** medium
- **first observed:** 2026-07-05 11:39 EEST

### TODO-EPIC-SWING-STALE
- **issue:** EPIC/USDT appeared as swing LONG (Idea #2, score 72.4) in the 04:22 swing report when it was +22.54% 24h. By 11:27 the same day, EPIC is -22.17% (full reversal ~44pp intraday). The swing report (carry-forward, 7.3h) still shows it as a top idea, but the signal is invalidated. No auto-invalidation occurred for the stale swing signal.
- **evidence:** `swing report 04:22` shows EPIC long (entry 0.6727–0.6888, current 0.6960); `scalp report 11:27` shows EPIC bias=short, 24h -22.17%; `active-signals` does not show EPIC swing in the 50 active signals.
- **suggested manual fix:** Swing signals should have a price-move-based invalidation check during each cycle — if the underlying is >15% adverse from the entry direction since signal generation, flag as stale/invalidated regardless of time window.
- **priority:** medium
- **first observed:** 2026-07-05 11:39 EEST
