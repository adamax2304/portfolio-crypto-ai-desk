# Opus Enriched Review — Crypto Overnight / Asia Review — Auto Cycle 04:39 EEST

**Slot:** crypto overnight / Asia review | **Time:** 2026-07-05 04:39 EEST
**Previous review:** 2026-07-04 23:15 EEST (post-close final daily review)
**Advisory only — no auto-trade. Weekend mode active (Sunday). Stocks CLOSED.**

---

## 1. Executive Summary

This is the **crypto overnight / Asia review** for Sunday 2026-07-05 at 04:39 EEST. Crypto-only weekend mode — all stocks logic disabled. Advisory only, no auto-trade.

**Overnight regime:** BTC trending back toward $62,000 after the July 4 recovery to $63,147. Short squeezes visible in ETH and SOL according to the market dashboard. Altcoin breadth extremely strong — 84.6% above EMA20, 87.2% above EMA50. F&G=23 (Extreme Fear) persists as a contrarian bullish backdrop despite the price rally.

**Signal picture:** 20 active B-tier signals (all long, crypto). No A-tier. Swing mode is the strongest performer (14d PF 5.80, WR 72%). Intraday no-catalyst and scalp modes have documented negative edge — do not rely on them without RS-leader or breakout confirmation. Weekend signals historically underperform (WR 20% flag).

**Top opportunity:** **ADA/USDT** — catalyst label flipped news_supported 0→1 this cycle (ADA×3 news flips), B-tier swing actionable, ETF SEC review window opens August 9, whale accumulation confirmed, price recovering from June 30 lows ($0.1453 → $0.194). Wait for pullback into 0.1890–0.1910 (swing entry zone). SL 0.1866.

**Key avoids:** VANRY (+46.85% overnight, OI +140%, negative funding, momentum_breakout "avoid_chase" basket). HMSTR (+85% 7d). Both are post-impulse; no retest structure. APT/TLM/UNH remain operator-review blocked.

**Catalyst mapping:** Weak (12 high-importance symbols unmapped: ARB, AVAX + 8 stocks tickers). Use catalyst layer as context only.

---

## 2. Data Used

| Source | Mtime / Freshness | Status |
|---|---|---|
| scheduler.log (cycle_01_03-59) | 04:25 EEST (14 min ago) | **FRESH** |
| cycle_01_03-59_summary.md | 04:24 EEST (15 min) | **FRESH** |
| scalp report `2026-07-05_01-06` | 04:06 EEST (33 min) | **FRESH** |
| intraday report `2026-07-05_01-11` | 04:11 EEST (28 min) | **FRESH** |
| swing report `2026-07-05_01-22` | 04:22 EEST (17 min) | **FRESH** |
| stocks reports | Weekend mode — disabled | **N/A** |
| catalyst_events.jsonl / baskets | Cycle 04:24 EEST | **FRESH** |
| llm_analysis_packet.md | 04:22 EEST (swing) | **FRESH** |
| active-signals CLI (crypto) | Cycle 04:22 EEST | **LIVE (20 signals)** |
| signal-stats CLI (crypto) | Cycle 04:22 EEST | **LIVE** |
| paper monitor status | Cycle 04:25 EEST | **FRESH** |
| detect_untracked_legacy_alerts | Cycle 04:25 EEST (0 untracked) | **CLEAR** |
| BTC price (dashboard snapshot) | Cycle 04:15 EEST | toward $62K |
| ADA catalyst (WebSearch + WebFetch) | 04:39 EEST | ETF window Aug 9 confirmed |
| ADA HF status (external) | 04:39 EEST | Disputed — see §7 |

**Notes:**
- Stocks: disabled (weekend mode, Sunday).
- Social: Reddit 403 blocked; no live X/Telegram connectors.
- Onchain: `interface_ready_config_missing` (no config/onchain.yaml).
- Weekend mode active: A-tier penalty −2pts, chasing entries demote, MEXC-only capped C.

---

## 3. Scheduler / Data Freshness

- **Scheduler:** cycle_01 completed at 04:24:49 EEST (14 min ago). All OK: 29/29 steps, 0 failed. **FRESH.**
- **Cycle mode:** weekend (crypto-only). Stocks disabled.
- **Paper monitor status (live from cycle 04:25):**
  - OPEN ACTIONABLE: 16
  - WAITING FOR ENTRY: 8
  - ENTERED UNRESOLVED: 31 (filled signals, no TP/SL closed before window — not losses)
  - REVIEW/SHADOW: 164
  - NO-ENTRY / STALE / MOVED AWAY: 31
  - Closed (cumulative history): 374W / 38L / 0flat
  - NEEDS REVIEW: 0
- **Untracked legacy alerts:** 0 (clean — vs 16 in previous July 4 23:15 review)
- **Intelligence layer:** timeline ok (150 symbols, 1978 events). Derivatives: funding/OI numeric history sparse, price metrics primary.
- **Squeeze phase distribution:** 43 unknown, 26 build_up, 2 squeeze_expansion, 4 unwind, **46 post_unwind_chop** (dominant — most of the universe is digesting prior moves).

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-07-05 04:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["social_attention", "onchain_data", "liquidation_heatmaps", "order_book_depth", "etf_flows"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "cycle_01 completed 04:24 EEST, 14 min ago — FRESH",
        "All 3 crypto reports within 33 min — FRESH",
        "Weekend mode active: stocks disabled, A-tier penalty in effect",
        "Catalyst integrity: 12 high-importance unmapped (ARB, AVAX, 8 stock tickers)",
        "Reddit 403 / social: blocked; onchain: config missing",
        "0 untracked legacy alerts — clean vs 16 in prior review"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.80,
      "reason_codes": ["risk_on", "longs_preferred"],
      "data_missing": ["live_btc_price_confirmed", "DXY_yields", "macro_calendar", "social_sentiment"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC uptrend; ETH uptrend (swing/scalp/intraday regime: bullish trend)",
        "Altcoin breadth: 84.6% above EMA20, 87.2% above EMA50 (very strong)",
        "Dashboard: crypto_mode=trend, BTC toward $62K (overnight softening from $63,147 Jul 4)",
        "Short squeeze narrative: ETH and SOL extending gains overnight",
        "F&G=23 (Extreme Fear) — contrarian bullish backdrop",
        "VIX=16.15 (low risk), SPY=up, QQQ=down (mixed stocks, irrelevant weekend)",
        "ETH/BTC=0.028129 (alt-favorable ratio)"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.60,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "stale_catalyst"],
      "data_missing": ["symbol_resolver_coverage", "social_feeds", "btc_etf_flow_data"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "ADA catalyst label: news_supported 0->1 (ADA×3 news flips this cycle)",
        "ADA: Van Rossem HF status uncertain (prev review said June 18 live, external says still July upcoming)",
        "ADA: SEC ETF review window August 9 confirmed (Grayscale/VanEck/21Shares/Canary filings pending)",
        "ADA: Whale accumulation confirmed (38.13% of supply in large wallets end June)",
        "BTC: ETF 8th negative week BUT Independence Day context; Strategy removed never-sell policy",
        "Catalyst integrity: 12 high-importance unmapped — stocks tickers + ARB/AVAX crypto",
        "Hinkal $820K exploit (minor DeFi, no top-20 impact)",
        "Clarity Act advancing (NOBLE endorsement) but Senate vote delayed"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["squeeze_risk", "oi_supports", "funding_extreme"],
      "data_missing": ["bybit_cross_oi_full", "liquidation_heatmap", "stablecoin_flows"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "VANRY: OI +140.54%, funding -0.001 to -0.00106 across Bybit/MEXC — crowded, unknown phase",
        "OGN: OI +122.89%, funding -0.0022 Bybit/MEXC — crowded, negative funding",
        "HMSTR: OI +64.32%, funding neutral — build_up phase, monitor crowding",
        "ADA: OI +2.57%, funding +0.0001, L/S 1.961 — normal, fresh positioning",
        "ETHFI: OI +6.31%, funding neutral, L/S 1.413 — normal",
        "EPIC: OI +15.72%, funding neutral — normal",
        "Phase dist: 26 build_up, 2 squeeze_expansion, 4 unwind, 46 post_unwind_chop"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["chase_risk", "clean_retest", "entry_late"],
      "data_missing": ["live_chart_confirmation", "order_book_depth", "CVD"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "ADA: 0.1940 vs entry 0.1890-0.1910 — ~0.7 ATR above entry zone; pullback required",
        "ETHFI: 0.4180 vs entry 0.4097-0.4155 — at top of zone; can wait for minor dip",
        "VANRY: 0.0044 vs entry 0.0039-0.0043 — ABOVE entry zone — chase risk",
        "EPIC: 0.7170 vs entry 0.6951-0.7103 — just above zone; pullback required",
        "HMSTR: 0.0003 precision too low to assess; 7d +85% likely overextended",
        "Weekend mode: require retest after impulse flag active",
        "TradingView / manual chart check unavailable — OHLCV/ATR/EMA from report only"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.90,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "review_shadow"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "OPEN ACTIONABLE: 16 (triggered, within validity window)",
        "WAITING FOR ENTRY: 8 (entry price not yet touched)",
        "ENTERED UNRESOLVED: 31 (entry filled, no TP/SL before window: 0R display / unresolved, not losses)",
        "REVIEW/SHADOW: 164",
        "NO-ENTRY/STALE/MOVED AWAY: 31",
        "Closed today: 374W / 38L / 0flat (cumulative paper history)",
        "NEEDS REVIEW: 0",
        "0 untracked legacy alerts (clean)"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["correlation_cluster", "reduce_risk", "manual_review"],
      "data_missing": ["daily_pnl_breakdown", "leverage_cluster_data"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "All 20 active signals are long crypto — correlation cluster",
        "Weekend thin liquidity: wider wicks, harder fills",
        "VANRY + OGN: crowded derivatives (OI 122-140%, negative funding) — manual_review",
        "APT/TLM/UNH operator blocks active (exploit/delisting/legal)",
        "No A-tier signals — lower individual conviction",
        "31 entered-unresolved: need monitoring, not new entries on same symbols"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.80,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": ["mode_specific_weekend_breakdown"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Swing: 14d WR 72% / PF 5.80 / +24R — STRONGEST mode",
        "Intraday no-catalyst (14d): WR 23% / PF 0.70 / -3R — net-negative without RS/breakout",
        "Scalp: 1W/7L over 14d, PF 0.14 — low confidence, data-collection phase",
        "Weekly B-tier: WR 23.4% / PF 3.11 / avgR 0.43R",
        "Weekend signals: WR 20% (underperform observation)",
        "Paper portfolio (bybit): +$2541.50 net (+50.83%) on 774 trades",
        "Paper shadow B forward +44.08R vs A -110.78R — gate NOT_READY, no promotion"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "ok",
      "confidence": 0.75,
      "reason_codes": ["risk_on", "longs_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Regime: bullish trend, breadth strong, BTC uptrend holding",
        "Best long: ADA — catalyst flip, ETF Aug 9, whale accumulation, cleanest structure",
        "Best short watch: SYN — -14% 24h, capped C weekend due to squeeze risk",
        "Avoid: VANRY — +46.85% with OI 140%, neg funding, avoid_chase basket",
        "Swing is the only positive-edge playbook for weekend use",
        "Intraday/scalp: only if RS-leader confirmed"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "normal",
    "confidence": 0.75,
    "preferred_side": "longs",
    "best_long_candidate": {
      "symbol": "ADA/USDT",
      "trigger": "pullback into 0.1890-0.1910, 1h hold above 0.1866",
      "reason": "catalyst label flip (news_supported), ETF SEC Aug 9, whale accumulation, swing score 72.6, cleanest structure"
    },
    "best_short_candidate": {
      "symbol": "SYN/USDT",
      "trigger": "wait Monday open + 1h close below ~0.034 + volume expansion",
      "reason": "-14% 24h, RS -13.8% vs BTC, failed bounce; capped C now — weekend thin liquidity squeeze risk"
    },
    "best_catalyst_candidate": {
      "symbol": "ADA/USDT",
      "trigger": "Van Rossem HF date confirmation + pullback into entry zone",
      "reason": "HF potentially still upcoming (external July sources); ETF SEC window Aug 9; whale 38.13%"
    },
    "avoid_candidate": {
      "symbol": "VANRY/USDT",
      "reason": "+46.85% overnight, OI 140%, negative funding, avoid_chase basket; MEXC-only some venues; no retest"
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
| data_quality | **ok** | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | **ok** | 0.80 | risk_on, longs_preferred | advisory_only |
| catalyst_narrative | **caution** | 0.60 | mapping_weak, fresh_catalyst, stale_catalyst | advisory_only |
| derivatives_squeeze | **caution** | 0.72 | squeeze_risk, oi_supports, funding_extreme | advisory_only |
| technical_entry | **caution** | 0.72 | chase_risk, clean_retest, entry_late | advisory_only |
| execution_lifecycle | **ok** | 0.90 | open_actionable, waiting_for_entry, entered_unresolved, review_shadow | advisory_only |
| risk_manager | **caution** | 0.75 | correlation_cluster, reduce_risk, manual_review | advisory_only |
| playbook_performance | **caution** | 0.80 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | **ok** | 0.75 | risk_on, longs_preferred, wait_for_trigger | advisory_only |

**Council synthesis:** 3 ok / 5 caution / 0 bad. Regime genuinely risk-on; weekend overnight context demands patience. Quality over quantity.

---

## 4. What Changed vs Previous Review (2026-07-04 23:15)

| Item | Previous (23:15 Jul 4) | Current (04:39 Jul 5) |
|---|---|---|
| Cycle freshness | 11 min | 14 min |
| Active signals | ~50 | 20 (drop: expiries/resolutions overnight) |
| OGN swing score | In top candidates | 74 (HIGHEST, OPEN ACTIONABLE) |
| ADA catalyst | No label flip | **news_supported 0→1 (ADA×3 flips)** |
| Untracked legacy alerts | 16 | **0 (clean)** |
| BTC level | $63,147 | Toward $62K (overnight softening) |
| ETH/SOL | Strong close | Short squeeze extension overnight |
| Swing report | 7h carry-forward | **FRESH (17 min)** |
| NFP/USDT | Not visible | New in swing strongest (score 81.6) |
| Signal stats | PF 3.6 / totalR 93.7R | PF 3.11 / totalR 84.3R (rolling window) |
| Paper shadow forward | A -81.98R / B +59.62R | A -110.78R / B +44.08R — NOT_READY |
| VANRY | Extended | OI 140% + neg funding — avoid_chase basket |

**Confirmed from previous:** BTC held above $62K. Alt breadth still dominant (84.6%). OGN remains strongest signal.

---

## 5. Catalyst Coverage

- Total catalyst events today: **382–416** (varies by report)
- Narrative baskets active: **5** (scalp/intraday) / **4** (swing)
- Operator blocks: **3** — APT (exploit), TLM (delisting), UNH (legal)
- High-importance unmapped: **12** (ARB, AVAX, AVGO, BLK, COST, MA, MS, QQQ, SMH, STG)
- Catalyst label refresh: **ADA×3** news_supported flips (0→1)

**Active baskets:**
- **rwa_narrative** (`related_beta_rotation`, <6h) → ONDO, XLM
- **perps_dex_narrative** (`wait_pullback`, <1h) → HYPE
- **delisting_thin_liquidity** (`avoid_low_liquidity`, <6h) → no primary
- **ai_narrative** (`related_beta_rotation`, <24h) → NEAR, RENDER, TAO, FET
- **momentum_breakout** (`avoid_chase`, <1h) → **VANRY, EPIC, OGN** ← explicit avoid_chase

**⚠️ Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

Top 3 unmapped headlines (no symbol):
1. CLARITY Act endorsement by NOBLE (broadly crypto-positive)
2. Hinkal $820K USDC exploit (minor DeFi)
3. PHR/CALX securities fraud deadlines (stocks, irrelevant to crypto)

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** `risk-on` (BTC uptrend, breadth 84.6%, ETH short squeeze, F&G=23 contrarian)
- **Stocks mood:** `closed` (weekend, Sunday)
- **Dominant narrative:** Overnight short squeezes in ETH/SOL; BTC digesting $62–63K; ADA ETF catalyst building
- **Preferred side now:** `longs` — RS-leader + catalyst-backed; pullback entries only
- **Best long candidate:** ADA/USDT — trigger: pullback 0.1890–0.1910, SL 0.1866
- **Best short candidate:** SYN/USDT — trigger: wait Monday open + volume + 1h close <0.034
- **Best catalyst-backed candidate:** ADA/USDT (ETF pipeline, HF potentially upcoming, news_supported flip)
- **What to avoid:** VANRY (post-impulse +46.85%), HMSTR (+85% 7d), scalp/intraday without RS-leader
- **What would change the view:** BTC 1h close <$61K → caution/shorts; BTC 1h close >$64.5K → aggressive longs

---

## 7. Candidate Deep Dives

### Candidate 1 — ADA/USDT (Best Long Watch / Best Catalyst)

**Setup:** B-tier swing 72.6 | intraday 68.8 | scalp 71.6
**Status:** WAITING FOR ENTRY (swing) / OPEN ACTIONABLE (intraday triggered)
**Price:** ~0.194 | ATR: 0.0043 | Entry (swing): 0.1890–0.1910 | SL: 0.1866
**TP1:** 0.1963 / **TP2:** 0.2007 / **TP3:** 0.2051

**Has price reacted?** Partially — ADA was $0.1453 on June 30 (−40% monthly decline), recovered to ~$0.194 = +33%. 7d return +31–33%. 24h return +7.8–9.3% (not a violent spike).

**Chase risk:** Moderate. Price is ~0.7 ATR above the swing entry zone. Retest required, not a direct entry.

**Catalyst evidence:**
- **Internal:** ADA×3 news_supported label flip in this cycle (catalyst_label_refresh step)
- **External (confirmed):** Van Rossem Hard Fork — **status disputed**: previous review stated June 18 live, but external sources (MEXC, openpr.com, CoinCodex as of July 2026) suggest still upcoming through July 23. If HF not yet deployed, this is a pre-catalyst setup.
- **External (confirmed):** ADA Spot ETF — Grayscale/VanEck/21Shares/Canary Capital filings pending; **SEC review window opens August 9, 2026** (CME ADA futures since Feb 2026, streamlined SEC review). Strongest medium-term catalyst.
- **External (confirmed):** Whale accumulation — wallets holding 10M–100M ADA grew 37.66% → 38.13% of supply (end of June).
- **External:** SEC safe harbor (Atkins proposal March 2026) — ADA not classified as security.

**Legal/headline risk:** None. SEC safe harbor confirmed.

**Derivatives:** OI +2.57%, funding +0.0001, L/S 1.961 — clean, fresh positioning, no crowding.

**Mood alignment:** YES — risk-on, longs preferred, RS-leader, catalyst-backed.

**Actionable verdict:** YES — WAITING FOR ENTRY on swing. Place limit buy at 0.1890–0.1910. SL: 1h close below 0.1866. Do not chase above 0.194 on swing mode.

**Invalidation:** 1h close below 0.1866 or BTC dumps below $61K.

---

### Candidate 2 — VANRY/USDT (Contradiction / Avoid)

**Setup:** B intraday 67.1 / B swing 68.0 / B scalp 68.0
**Status:** OPEN ACTIONABLE (intraday) / WAITING (swing)
**Price:** ~0.0044 | Entry zone: 0.0039–0.0043 | ABOVE entry zone → chase risk HIGH

**Overnight move:** +46.85% 24h, +45.64% 7d. Price breached entry zone top.

**Derivatives contradiction:** OI +140% (massive build), funding −0.001 to −0.00106 (Bybit + MEXC). Unknown crowding phase. High uncertainty.

**Basket signal:** momentum_breakout → `avoid_chase` playbook.

**Actionable verdict:** NO ENTRY. WAIT FOR RETEST — if price returns to 0.0035–0.0039 and OI/funding normalises, reassess. Currently: NO-ENTRY / WAIT FOR RETEST.

---

### Candidate 3 — ETHFI/USDT (B-tier, Near Entry Zone)

**Setup:** B scalp 71.9 / B intraday 66.1
**Status:** WAITING FOR ENTRY
**Price:** 0.4180 | Entry: 0.4097–0.4155 | SL: 0.4027
**TP1:** 0.4307 / **TP2:** 0.4434 / **TP3:** 0.4561

**Catalyst:** AMBCrypto "eyes $0.40" article — price already above $0.40 target; catalyst lagging/priced. ETH ecosystem benefit from short squeeze.

**Entry proximity:** Price at top of entry zone (0.4180 vs 0.4155 zone top — 0.25 ATR gap). A minor pullback puts price inside zone.

**Playbook caveat:** Scalp low-confidence; intraday no-catalyst net-negative. Swing mode is positive-edge playbook here.

**Actionable verdict:** WAITING FOR ENTRY (swing). If pullback to 0.4097–0.4155 holds on 15m–1h, B-tier entry. Do not enter scalp/intraday without catalyst confirmation.

---

### Candidate 4 — OGN/USDT (Active, Monitor Crowded Derivatives)

**Setup:** B swing 74 (HIGHEST active score)
**Status:** OPEN ACTIONABLE (swing triggered)
**Price:** ~0.0186 | Support: 0.0157 | Resistance: 0.0244

**Already entered** — focus is on management, not entry.

**Derivatives risk:** OI +122.89%, funding −0.0022 to −0.0028 (Bybit/MEXC). Same crowded profile as VANRY. This is an active position with elevated derivative risk.

**No fresh catalyst verified** in production. momentum_breakout basket includes OGN with `avoid_chase` playbook — but signal was already entered at a prior price.

**Action:** Monitor for OI compression and funding normalisation. If funding goes more negative (−0.003+), consider tightening stop to structure (around 0.0157 support).

---

### Candidate 5 — HMSTR/USDT (Watchlist Only / Overextended)

**Setup:** B swing 69 (waiting) / C intraday / C scalp
**Status:** WAITING FOR ENTRY (swing)
**Price:** ~0.0003 (sub-satoshi precision issue) | 7d: +85.37% | OI: +64.32%

**Not actionable:** 7d +85% is extreme. Weekend mode "require retest after impulse" flag applies. ATR/price precision too low to evaluate entry quality. Watchlist only — monitor for structure reset.

---

## 8. Best Candidates Ranked

| Rank | Symbol | Mode | Status | Trigger | Notes |
|---|---|---|---|---|---|
| 1 | **ADA/USDT** | Swing B | WAITING FOR ENTRY | Pullback to 0.1890–0.1910, SL 0.1866 | Best catalyst, ETF Aug 9, clean structure |
| 2 | **ETHFI/USDT** | Swing B | WAITING FOR ENTRY | Pullback to 0.4097–0.4155, SL 0.4027 | Near entry; catalyst lagging |
| 3 | **OGN/USDT** | Swing B | OPEN ACTIONABLE | Already entered — monitor OI/funding | OI 122%, neg funding = watch |
| 4 | **EPIC/USDT** | Swing B | WAITING FOR ENTRY | Pullback to 0.6951–0.7103, SL 0.6766 | 7d +57%; weekend retest required |
| — | SYN/USDT | Short-watch | WAIT | Monday open + 1h close <0.034 + volume | Capped C now; weekend squeeze risk |

**Best long-watch:** ADA/USDT — trigger: pullback into 0.1890–0.1910
**Best short-watch:** SYN/USDT — trigger: Monday open + 1h close below ~0.034 + volume
**Best catalyst-watch:** ADA/USDT — Van Rossem HF confirmation + ETF August 9 pipeline

---

## 9. Avoid / No Trade

- **VANRY/USDT:** +46.85% overnight, OI 140%, negative funding, avoid_chase basket. Do not chase.
- **HMSTR/USDT:** +85% 7d, precision display issue, no retest. Watchlist only.
- **Scalp/intraday (no catalyst, no RS-leader):** Net-negative edge documented (14d). Do not size as primary.
- **BCH/USDT:** >2 ATR from EMA20 — explicitly rejected in the report.
- **APT/TLM/UNH:** Operator block active.
- **This window only** — scanning continues, data collection continues, system keeps running.

---

## 10. Main Risks

1. **BTC breakdown below $61K** — would flip all 20 correlated long signals simultaneously.
2. **VANRY/OGN derivative unwind** — OI 120–140% with negative funding; OGN is entered.
3. **Weekend thin liquidity** — wider wicks, stop-hunting at entry zones.
4. **Catalyst mapping weak** — ~80% unmapped; any catalyst urgency needs independent verification.
5. **ADA HF date uncertainty** — if van Rossem already live (prev review claim), pre-catalyst thesis reduced; ETF Aug 9 remains regardless.
6. **Social/KOL feeds offline** — no live crowd context.

---

## 11. Action Plan — Next 4 Hours (04:39 → 08:39 EEST)

1. **Watch ADA/USDT** — if pullback to 0.1890–0.1910, primary entry trigger. SL 0.1866. Swing mode.
2. **Monitor OGN** — OPEN. Watch OI/funding for unwind. Tighten stop to 0.0157 structure if funding worsens.
3. **Do not chase VANRY** — if retreats to below 0.0040 + OI compresses, reassess at Europe open.
4. **BTC $61K** — if 1h close below, shift to caution.
5. **ETHFI** — watch for pullback to 0.4097–0.4155.
6. **No scalp/intraday without RS-leader** — documented net-negative.
7. **At Europe open ~09:00:** Re-evaluate SYN short with improved liquidity.

---

## 12. Final Verdict per Mode

| Mode | Verdict | Rationale |
|---|---|---|
| **Swing** | WATCH / WAIT FOR ENTRY | ADA + ETHFI: pullback-to-entry. OGN: open, monitor. Strongest edge (PF 5.80). |
| **Intraday** | CONDITIONAL — RS-leader only | ADA triggered; others only with RS + catalyst confirmation. No-catalyst = negative 14d edge. |
| **Scalp** | LOW CONFIDENCE / Data collection | PF 0.14 over 14d. Do not size as primary. |
| **Shorts** | WAIT FOR MONDAY | SYN best short-watch; weekend thin liquidity prohibits clean entry now. |

---

## 13. Sources

- [Cardano Price Prediction July 2026 — CryptoRank](https://cryptorank.io/news/feed/df503-cardano-price-prediction-july-2026-is-history-about-to-repeat-for-ada-this-july) — ADA $0.1453 June 30; date unavailable (article July 2026)
- [ADA Price Prediction: Eyes July Hard Fork Catalyst — openpr.com](https://www.openpr.com/news/4568558/ada-price-prediction-pepeto-presale-gains-ground-as-cardano) — van Rossem HF context; date unavailable
- [Cardano Price Prediction July 2026 — MEXC](https://www.mexc.co/learn/article/cardano-price-prediction-july-2026-will-ada-hold-0-24-before-its-next-hard-fork-/) — HF timing reference; date unavailable
- [Cardano Price Prediction: Whale Accumulation — KuCoin](https://www.kucoin.com/news/flash/cardano-price-prediction-july-2026-whale-accumulation-and-stolen-ada-recovery-in-focus) — whale accumulation 38.13%; date unavailable
- Internal: `data/reports/scalp/2026-07-05_01-06_scalp_report.md` — 2026-07-05 04:06 EEST
- Internal: `data/reports/intraday/2026-07-05_01-11_intraday_report.md` — 2026-07-05 04:11 EEST
- Internal: `data/reports/swing/2026-07-05_01-22_swing_report.md` — 2026-07-05 04:22 EEST
- Internal: `data/scheduled_runs/2026-07-05_default_schedule/cycle_01_03-59_summary.md` — 2026-07-05 04:24 EEST
- Internal: Market dashboard snapshot id=65 — crypto_mode=trend, F&G=23 — 2026-07-05 04:15 EEST
- Internal: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-04_2315.md` — previous review baseline

---

## 14. Fix Requests / TODO

### TODO-ada-hf-date-clarify
- **issue:** ADA van Rossem HF date uncertain — previous review stated "June 18 live" but external sources (MEXC, openpr.com July 2026) use "upcoming HF" language. If HF not deployed, pre-catalyst thesis is stronger than current scoring reflects.
- **evidence:** Internal: OPUS_ENRICHED_REVIEW_AUTO_2026-07-04_2315.md ("June 18 already live"). External: MEXC "Will ADA Hold $0.24 Before Its Next Hard Fork?" (upcoming language)
- **suggested manual fix:** Verify Cardano mainnet epoch status to confirm van Rossem deployment; if not live, update catalyst_events with correct date and ensure ADA catalyst_news component reflects pre-HF premium.
- **priority:** medium
- **first observed:** 2026-07-05 04:39 EEST

### TODO-dogs-bonk-hmstr-precision
- **issue:** DOGS/USDT, BONK/USDT, HMSTR/USDT display as 0.0000 for current price, ATR, support, resistance, and TP values in scalp/intraday reports. Cannot assess entry quality for these tokens from text reports.
- **evidence:** `data/reports/scalp/2026-07-05_01-06_scalp_report.md` Trade Ideas #3 (DOGS), #5 (HMSTR); intraday report Trade Idea #5 (DOGS)
- **suggested manual fix:** Increase decimal precision to 8–10 significant figures or scientific notation for sub-satoshi priced tokens. Alternatively display relative ATR percentage.
- **priority:** medium
- **first observed:** 2026-07-05 04:39 EEST

### TODO-ogn-derivative-crowding-flag
- **issue:** OGN/USDT has B-tier swing signal OPEN ACTIONABLE with OI +122.89% and funding −0.0022 — same crowded profile as VANRY. The system does not surface this derivative crowding contradiction explicitly at the signal confidence level; only visible in the derivatives section and `crowding unknown` notation.
- **evidence:** `data/reports/swing/2026-07-05_01-22_swing_report.md` OGN derivatives; active-signals CLI OGN sw score 74 triggered; VANRY also has same pattern but receives avoid_chase basket
- **suggested manual fix:** Add derivative crowding check (OI >100% AND funding < −0.001) as a signal risk flag or confidence reduction in the swing scoring agent. Bubble the crowding caution into Telegram advisory for entered signals.
- **priority:** medium
- **first observed:** 2026-07-05 04:39 EEST
