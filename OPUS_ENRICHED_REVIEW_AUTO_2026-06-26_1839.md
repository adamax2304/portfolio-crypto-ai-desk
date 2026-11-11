# Opus Enriched Review — US open reaction review — Auto Cycle 18:39 EEST

**Slot:** US open reaction review (18:30 EEST slot)
**Time:** 2026-06-26 18:39 EEST (~2h 9min into US regular session)
**Date:** 2026-06-26 (Friday)
**Model:** claude-sonnet-4-6
**Advisory only — no auto-trade, no signal registration**

---

## 1. Executive Summary

**Slot: US open reaction review — advisory only / no auto-trade.**

US session is ~2h in. Stocks chop (VIX 19.28), healthcare/financials leading. **BTC remains below $60K** with large ETF outflows (−$670M 1D, −$1.32B 7D) and an active whale 20x short on $54.55M BTC + $15.65M ETH. Crypto regime: **risk-off** on scalp/intraday, **range/chop** on swing with altcoin breadth recovering to 40.5%.

**Critical legal risk update: UNH B-tier long TRIGGERED — MANDATORY AVOID.** DOJ fraud probe (criminal + civil) confirmed in catalyst events. UNH appeared as B-tier 68.4 intraday long in today's fresh report; ignore entirely due to legal risk.

**Crypto active signals (14):** 3 OPEN ACTIONABLE swing longs (SOL/HEI/APE triggered), 2 WAITING FOR ENTRY (AAVE/JTO), 9 ENTERED UNRESOLVED (TP hit including BTC/ETH shorts + several longs). **ETH contradiction persists: ETH swing short (65, TP hit) AND ETH swing long (66, TP hit) both ENTERED UNRESOLVED — do not add fresh ETH exposure without manual review.**

**Best actionable this window:** AAVE (catalyst-backed B swing, WAITING for entry at pullback); LLY (B stocks intraday, healthcare RS leader, TRIGGERED, no legal flags). SOL OPEN but approaching resistance 70.99 — do not add; manage existing.

**ALWAYS-SCAN continues. Scanner and data collection unchanged.**

---

## 2. Data Used

| Source | File | Generated (EEST) | Age at 18:39 | Status |
|--------|------|-----------------|--------------|--------|
| Scheduler log | scheduler.log | (not found) | — | MISSING (not blocking — cycle mtime used) |
| Cycle 5 summary | cycle_05_16-35_summary.md | 18:15 | 24 min | FRESH |
| Scalp report | 2026-06-26_13-56_scalp_report.md | 16:56 | 1h43m | FRESH |
| Intraday crypto | 2026-06-26_14-10_intraday_report.md | 17:10 | 1h29m | FRESH |
| Swing crypto | 2026-06-26_14-50_swing_report.md | 17:50 | 49 min | FRESH |
| Stocks intraday | 2026-06-26_15-31_stocks_intraday_report.md | 18:31 | 8 min | VERY FRESH |
| Stocks swing | 2026-06-26_15-06_stocks_swing_report.md | 18:06 | 33 min | VERY FRESH |
| Stocks invest | 2026-06-26_15-13_stocks_invest_report.md | 18:13 | 26 min | VERY FRESH |
| Catalyst events | data/catalysts/2026-06-26/ | today | — | FRESH (926 events, 6 baskets) |
| Active signals CLI | src.cli active-signals ×2 | 18:39 | live | LIVE |
| Signal stats CLI | src.cli signal-stats ×2 | 18:39 | live | LIVE |
| Untracked alerts | detect_untracked_legacy_alerts | 18:39 | live | NONE FOUND |
| Previous review | OPUS_ENRICHED_REVIEW_AUTO_2026-06-26_1623.md | 16:23 | 2h16m | READ |
| External web | — | — | — | NOT RUN — internal data sufficient for all candidates |

**Notable vs previous review:** ALL reports now fully fresh (previous: swing/invest/stocks were 11h borderline stale). Scheduler.log not found — using cycle mtime (18:15) as proxy. Not blocking.

---

## 3. Scheduler / Data Freshness

- **Scheduler:** cycle_05_16-35_summary.md mtime 18:15 EEST (24 min ago). **NOT DEFERRED.**
- **Active crypto signals:** 14 total — 3 OPEN ACTIONABLE, 2 WAITING, 9 ENTERED UNRESOLVED (TP hit).
- **Active stocks signals:** 50 total — mix of B-tier triggered/waiting and C-tier.
- **Untracked legacy alerts:** NONE (clean).
- **Crypto signal stats (week):** A/B n=153, PF=1.24, WR=20.1%, +13R. By mode: **swing +18R PF 2.00 ✓**; intraday +1R PF 1.03 marginal; scalp −6R PF 0.14 ✗. By direction: **shorts +13R PF 2.34 ✓**; longs 0R PF 1.0 flat (inverted vs previous review — significant shift confirmed).
- **Stocks signal stats (week):** A/B n=24 (weak), PF=0.909, −1R. Stocks swing 48h audit (−12R). Stocks invest capped (0W/7L).
- **Data gaps:** Scheduler.log missing; social attention missing; liquidation heatmaps not connected; on-chain config missing; CVD not connected.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-06-26 18:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.88,
      "reason_codes": ["scheduler_fresh", "all_reports_fresh"],
      "data_missing": ["scheduler_log_file", "social_attention", "onchain_config", "liquidation_heatmaps"],
      "suggested_effect": "advisory_only",
      "facts_used": ["cycle_05_mtime_18:15", "all_reports_fresh_<2h", "926_catalyst_events", "6_narrative_baskets"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["risk_off", "chop", "mixed", "shorts_preferred"],
      "data_missing": ["live_BTC_price", "live_ETH_price"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC_downtrend", "ETH_downtrend", "altcoin_breadth_40.5%_swing", "scalp_breadth_23.9%", "stocks_chop_VIX_19.28", "ETF_outflows_670M_1D", "whale_20x_short_BTC_ETH"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.78,
      "reason_codes": ["fresh_catalyst", "catalyst_confirmed", "narrative_supported", "legal_risk"],
      "data_missing": ["mapped_vs_unmapped_exact_count"],
      "suggested_effect": "advisory_only",
      "facts_used": ["kraken_aave_15pct_stake", "ETF_outflows_bearish", "whale_20x_short_bearish", "solana_summer_narrative", "UNH_DOJ_probe_confirmed", "ADA_wallet_exploit", "perps_dex_HYPE_basket_fresh"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.52,
      "reason_codes": ["data_unavailable", "squeeze_risk", "oi_contradicts"],
      "data_missing": ["full_bybit_OI_data", "liquidation_heatmaps", "CVD"],
      "suggested_effect": "advisory_only",
      "facts_used": ["SOL_OI_up+price_up_fresh", "APE_OI_up+price_up", "JTO_OI_down_short_covering", "NEAR_OI_up+price_down_squeeze_risk", "TNSR_neg_funding_crowded_shorts"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.70,
      "reason_codes": ["chase_risk", "price_moved_away", "wait_for_trigger"],
      "data_missing": ["live_tick_prices", "chart_MCP"],
      "suggested_effect": "advisory_only",
      "facts_used": ["SOL_70.81_at_resistance_70.99", "AAVE_87.79_at_entry_zone_top", "HEI_0.1718_above_entry_0.169", "APE_0.1534_above_entry_0.1524", "JTO_0.7793_at_resistance_0.7795", "NEAR_1.780_below_short_entry_1.787"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto_14_active:_3_OPEN_2_WAITING_9_TP_HIT", "ETH_swing_contradiction_long_AND_short_both_TP_hit", "stocks_50_active_LLY_triggered", "UNH_triggered_but_legal_risk", "untracked_alerts_none"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.80,
      "reason_codes": ["legal_risk", "headline_risk", "correlation_cluster", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH_DOJ_probe_criminal_civil", "ADA_wallet_exploit_avoid", "ETH_contradiction_needs_manual", "whale_20x_short_BTC_ETH_SOL", "ETF_outflows_670M_1D_bearish", "stocks_swing_48h_audit_minus12R", "scalp_minus6R_PF_0.14"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["playbook_working", "playbook_failing"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["swing_PF_2.00_+18R_WORKING", "shorts_PF_2.34_+13R_OUTPERFORMING", "intraday_PF_1.03_marginal", "scalp_PF_0.14_FAILING", "stocks_swing_capped_audit", "stocks_invest_capped_0W7L"]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.78,
      "reason_codes": ["wait_for_trigger", "catalyst_backed", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["AAVE_catalyst_backed_WAITING_entry_zone", "UNH_AVOID_legal_risk", "SOL_OPEN_near_resistance", "LLY_healthcare_leader_TRIGGERED", "NEAR_short_watch_below_entry_zone", "shorts_outperforming_longs_week"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.72,
    "preferred_side": "catalyst_backed",
    "best_long_candidate": {
      "symbol": "AAVE/USDT",
      "trigger": "pullback into 86.87–87.50 on decreasing volume; 1h hold above 86.87",
      "reason": "Kraken 15% stake catalyst confirmed, RS leader +8.6% vs BTC, B-tier swing WAITING, best catalyst-backed long this window"
    },
    "best_short_candidate": {
      "symbol": "NEAR/USDT",
      "trigger": "failed bounce into 1.787–1.804 zone with 1h rejection candle, BTC not recovering",
      "reason": "Weak RS −5% vs BTC, price down + OI up (fresh shorts pressing), AI narrative mixed, no catalyst support"
    },
    "best_catalyst_candidate": {
      "symbol": "AAVE/USDT",
      "trigger": "pullback into 86.87–87.50 + Kraken catalyst holding news cycle",
      "reason": "Kraken eyeing 15% stake at $385M valuation — institutional buying thesis; clearest confirmed catalyst this cycle"
    },
    "avoid_candidate": {
      "symbol": "UNH",
      "reason": "DOJ fraud probe (criminal + civil) confirmed; B-tier triggered but MANDATORY AVOID regardless of score"
    },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry_logic", "routing", "live_execution"],
    "todo_count": 3
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|-------|---------|------------|--------------|-----------------|
| data_quality | ok | 0.88 | scheduler_fresh, all_reports_fresh | advisory_only |
| market_regime | caution | 0.75 | risk_off, chop, mixed, shorts_preferred | advisory_only |
| catalyst_narrative | caution | 0.78 | fresh_catalyst, catalyst_confirmed, legal_risk | advisory_only |
| derivatives_squeeze | caution | 0.52 | data_unavailable, squeeze_risk, oi_contradicts | advisory_only |
| technical_entry | caution | 0.70 | chase_risk, price_moved_away, wait_for_trigger | advisory_only |
| execution_lifecycle | ok | 0.82 | open_actionable, waiting_for_entry, entered_unresolved, needs_review | advisory_only |
| risk_manager | caution | 0.80 | legal_risk, headline_risk, correlation_cluster, manual_review | advisory_only |
| playbook_performance | caution | 0.75 | playbook_working, playbook_failing | advisory_only |
| head_trader | caution | 0.78 | wait_for_trigger, catalyst_backed, manual_review | advisory_only |

---

## 4. What Changed vs Previous Review (16:23 pre-US-open)

| Item | Previous (16:23) | Now (18:39) |
|------|-----------------|-------------|
| Scheduler | Cycle 4 (14:35) | Cycle 5 (18:15) — fresh |
| Swing/invest reports | Carry-forward (11h) | Fully fresh (<1h) |
| Active crypto signals | 10 (all ENTERED UNRESOLVED) | 14 (+4 new: SOL/HEI/APE TRIGGERED, AAVE/JTO WAITING) |
| Altcoin breadth | ~27.7% (scalp) | 23.9% scalp / 40.5% swing — partial recovery in swing TF |
| ETH contradiction | Flagged | Persists — both swing short + long TP hit |
| SOL/AAVE/JTO/HEI/APE | Not in signals | Now triggered (SOL/HEI/APE) or waiting (AAVE/JTO) |
| Crypto short performance | Shorts −2R PF 0.93 | Shorts +13R PF 2.34 ✓ (major reversal) |
| UNH legal risk | MANDATORY AVOID flagged | Still B-tier triggered, still AVOID |
| G/USDT | Not prominent | +40.68% 24h RS leader (swing C, no catalyst) |
| Stocks reports | Stale (11h) | Very fresh (8–33 min) |
| Whale short | Not noted | New 20x short BTC $54.55M + ETH $15.65M — bearish |
| ETF outflows | ~noted | BTC −$670M 1D / −$1.32B 7D; ETH −$72M 1D / −$232M 7D |

---

## 5. Catalyst Coverage

- **Total catalyst events today:** 926 (updated from 764 at scalp cycle)
- **Narrative baskets:** 6 active
  - **ai_narrative** (fresh <6h) — NEAR/RENDER/TAO/FET: mixed 45.4/100
  - **perps_dex_narrative** (fresh <1h) — HYPE: wait_pullback playbook
  - **rwa_narrative** (fresh <6h) — ONDO/XLM: related_beta_rotation
  - **delisting_thin_liquidity** (fresh <6h) — no primary
  - **binance_ecosystem_teaser** (fresh <24h) — BNB
- **Key catalyst events:**
  - **AAVE:** Kraken eyeing 15% stake at $385M valuation (Decrypt) — bullish, institutional
  - **BTC/ETH:** Whale 20x shorts re-entered (BTC $54.55M + ETH $15.65M) — bearish
  - **BTC:** ETF outflows −$670M 1D, −$1.32B 7D (t.me/lookonchain) — bearish
  - **UNH:** DOJ fraud probe confirmed (QuiverQuant) — LEGAL RISK → AVOID
  - **ADA:** Cardano wallet exploit (AMBCrypto) — AVOID ADA
  - **HYPE:** Singapore MAS warning list (BeInCrypto) — headline risk, basket
  - **MiCA:** Binance winding down EU services (BeInCrypto) — systemic headwind

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** risk-off / chop — BTC and ETH in downtrend, altcoin breadth 23.9% (scalp TF) / 40.5% (swing TF); BTC <$60K; ETF outflows; whale 20x shorts active
- **Stocks mood:** chop / mixed — VIX 19.28, breadth 50%, 2/4 indices uptrend; healthcare/financials leading; tech/comms weak
- **Preferred side now:** catalyst-backed on crypto swing (AAVE); shorts on weak RS crypto; stocks healthcare longs only
- **Best long candidate:** AAVE — pullback into 86.87–87.50 + Kraken catalyst
- **Best short candidate:** NEAR — failed bounce into 1.787–1.804, BTC weak
- **Best catalyst-backed candidate:** AAVE (Kraken 15% stake, institutional)
- **What to avoid:** UNH (DOJ probe), ADA (exploit), new altcoin longs without catalyst, scalp longs
- **What would change the view:** BTC reclaim above $60K with ETF inflow reversal → regime shifts toward longs

---

## 7. Candidate Deep Dives

### #1 — AAVE/USDT — B swing long — WAITING FOR ENTRY

**Score:** 70.9/100 | **Tier:** B | **Mode:** Swing | **Status:** WAITING FOR ENTRY

**Catalyst:** Kraken eyeing 15% stake at $385M valuation (Decrypt, 2026-06-26). CoinDesk: AAVE +8.9% leading CoinDesk 20. Fresh confirmed institutional catalyst.

**Price/chase check:**
- Price ~87.79–88.27 at TOP of entry zone 86.87–87.84 or marginally above; resistance 88.67 (~0.5% away)
- AAVE +9.23% today on Kraken news — catalyst partially priced in
- Actionable NOW? No — wait for pullback into 86.87–87.50 on declining volume
- Derivatives: price up + OI down (short covering) — weaker continuation quality; funding neutral
- Invalidation: 1h close below 85.68

**VERDICT: BEST CATALYST CANDIDATE. WAITING — entry on pullback to 86.87–87.50 only.**

---

### #2 — UNH — B stocks intraday long — LEGAL RISK / MANDATORY AVOID

**Score:** 68.4/100 | **Tier:** B | **Status:** TRIGGERED → AVOID

**Legal risk:** DOJ fraud probe (criminal + civil) confirmed via QuiverQuant catalyst event. Stock reportedly −16% on news. B-tier score based on technical data; legal risk overrides all scoring.

**VERDICT: MANDATORY AVOID. All timeframes and modes.**

---

### #3 — SOL/USDT — B swing long — OPEN ACTIONABLE (already entered)

**Score:** 74.5/100 | **Tier:** B | **Mode:** Swing | **Status:** TRIGGERED (entered)

**Catalyst:** "Solana Summer" narrative (CryptoSlate). "AI Agents Expand Into Tokenized Stocks" (BeInCrypto).

**Price/chase check:**
- Price ~70.81; above entry zone 69.96–70.55; resistance 70.99 (0.3% away)
- New entries: DO NOT ADD above 70.55 (chase risk confirmed)
- Existing position: monitor 70.99 — rejection → partial take; clean break → hold
- Funding +0.000052 neutral; OI +0.95% fresh positioning; long/short 2.78 (mild crowding)
- Invalidation: 1h close below 69.25

**VERDICT: OPEN ACTIONABLE for existing position. No adds. Manage stop at 69.25.**

---

### #4 — LLY — B stocks intraday long — TRIGGERED

**Score:** 77.17/100 | **Tier:** B | **Mode:** Stocks intraday | **Status:** TRIGGERED

**Legal/earnings:** No earnings in near window. No legal flags. Clean.

**Sector:** Healthcare (XLV) #1 sector RS +8.81% vs SPY 20d. LLY RS +7.92% — sector leader.

**Price:** Entry zone 1177.54–1185.55; above prev day high. TP1 1209.60, stop 1161.51. RR to TP1 ~1.45R (slightly below 1.5).

**Stocks regime:** Chop (VIX 19.28). SPY/QQQ range; IWM/DIA uptrend. Monitor SPY for breakdown.

**VERDICT: TRIGGERED. Best stocks candidate — healthcare RS in chop regime. Monitor SPY. VIX >20 = reduce.**

---

### #5 — NEAR/USDT — C swing short — SHORT WATCH

**Score:** 62.9/100 | **Tier:** C | **Mode:** Swing | **Status:** WATCHLIST

**Check:**
- No fresh catalyst for NEAR. AI narrative basket mixed (45.4/100).
- Price 1.780 BELOW entry zone 1.787–1.804 — not yet actionable
- Derivatives: price down + OI up (fresh shorts); 7d return −17.25% (extended); squeeze risk
- Wait for bounce to 1.787–1.804 then rejection; BTC must remain weak

**VERDICT: SHORT WATCH. Not actionable now. Wait for bounce to entry zone.**

---

## 8. Best Candidates Ranked

| Rank | Symbol | Side | Mode | Status | Trigger |
|------|--------|------|------|--------|---------|
| 1 | AAVE/USDT | Long | Swing | WAITING | Pullback to 86.87–87.50; don't chase above 87.84 |
| 2 | LLY | Long | Stocks intraday | TRIGGERED | SPY not breaking down; VIX stays below 20 |
| 3 | SOL/USDT | Long | Swing | OPEN (manage only) | Monitor 70.99 resistance; stop 69.25; no adds |
| 4 | NEAR/USDT | Short | Swing | WATCH | Bounce to 1.787–1.804 + rejection; BTC weak |
| 5 | HYPE/USDT | Catalyst watch | — | WATCH | Perps_dex_narrative fresh; wait_pullback playbook; MAS warning = headline risk |

---

## 9. Avoid / No Trade

- **UNH** — DOJ fraud probe. MANDATORY AVOID. All timeframes.
- **ADA** — wallet exploit. AVOID.
- **New scalp longs** — PF 0.14 −6R.
- **Adding to SOL/HEI/APE** — chase risk above resistance.
- **TNSR short** — crowded shorts, squeeze risk (−0.00403 funding, OI +5.47%).
- **FOGO/OPG shorts** — thin_liquidity_short_squeeze_risk.
- **Stocks swing/invest new entries** — capped to C (48h audit / 0W7L).

---

## 10. Main Risks

1. **BTC/ETH whale 20x shorts** ($54.55M BTC + $15.65M ETH) — bearish signal; cascade risk
2. **ETF outflows** — BTC −$670M 1D / −$1.32B 7D; ETH −$72M / −$232M 7D — sustained selling
3. **UNH legal risk** — DOJ probe B-tier in system; operator must manually ignore
4. **ETH contradiction** — swing short + swing long both TP hit; double exposure; manual review required
5. **AAVE chase risk** — +9.23% today; entry zone must be respected
6. **AXE/HOD weekend_mode flag** — review if carrying into weekend
7. **MiCA headwind** — Binance EU wind-down; systemic risk for smaller caps
8. **Stocks regime weak** — PF 0.909 net negative; swing audit ongoing

---

## 11. Action Plan — Next 4 Hours

1. **AAVE/USDT:** Wait for pullback 86.87–87.50. Entry: TP1 90.43, TP2 92.59, stop 85.68. Don't chase above 87.84.
2. **SOL/USDT:** Manage existing. Monitor 70.99 resistance. Rejection → partial TP1 (72.11). Break → hold. Stop: 69.25.
3. **LLY stocks:** Monitor SPY/XLV. VIX >20 = reduce. TP1 1209.60. Stop 1161.51.
4. **NEAR short:** Set alert at 1.790. No action until bounce to 1.787–1.804 confirmed.
5. **UNH:** Do not touch.
6. **ETH:** No new exposure until contradiction resolved manually.
7. **Crypto shorts:** Monitor for new failed-bounce short setups on weak-RS names (+13R PF 2.34 week).
8. **Scalp:** Avoid new longs (PF 0.14 −6R week).

---

## 12. Final Verdict per Mode

| Mode | Verdict | Notes |
|------|---------|-------|
| Crypto Swing | **CAUTION / SELECTIVE** | AAVE WAITING (wait pullback); SOL open (manage); HEI/APE open (manage) |
| Crypto Intraday | **CAUTION** | No A/B; shorts outperforming longs; no clean new entries |
| Crypto Scalp | **AVOID NEW LONGS** | PF 0.14 −6R; C-tier only |
| Stocks Intraday | **SELECTIVE** | LLY B-tier legitimate; UNH B-tier MANDATORY AVOID; XLV waiting |
| Stocks Swing | **RESEARCH ONLY** | 48h audit (−12R); no A/B |
| Stocks Invest | **RESEARCH ONLY** | 0W/7L audit; no A/B |

---

## 13. Sources

Internal data only (no external web this cycle):
- `data/reports/scalp/2026-06-26_13-56_scalp_report.md` — 16:56 EEST
- `data/reports/intraday/2026-06-26_14-10_intraday_report.md` — 17:10 EEST
- `data/reports/swing/2026-06-26_14-50_swing_report.md` — 17:50 EEST
- `data/reports/stocks/intraday/2026-06-26_15-31_stocks_intraday_report.md` — 18:31 EEST
- `data/reports/stocks/swing/2026-06-26_15-06_stocks_swing_report.md` — 18:06 EEST
- `data/reports/stocks/invest/2026-06-26_15-13_stocks_invest_report.md` — 18:13 EEST
- `data/catalysts/2026-06-26/catalyst_events.jsonl` — 926 events, 6 baskets
- `data/scheduled_runs/2026-06-26_default_schedule/cycle_05_16-35_summary.md` — 18:15 EEST
- `src.cli active-signals` ×2 — live 18:39 EEST
- `src.cli signal-stats` ×2 — live 18:39 EEST
- `scripts.detect_untracked_legacy_alerts` — 18:39 EEST, clean
- `OPUS_ENRICHED_REVIEW_AUTO_2026-06-26_1623.md` — previous review 16:23 EEST

Key catalyst citations (catalyst_events.jsonl):
- UNH DOJ probe: QuiverQuant 2026-06-26
- AAVE Kraken stake: Decrypt 2026-06-26
- BTC ETF outflows: t.me/lookonchain 2026-06-26
- ADA exploit: AMBCrypto 2026-06-26
- HYPE MAS warning: BeInCrypto 2026-06-26

---

## 14. Fix Requests / TODO

### TODO-UNH-RESCORING
- **issue:** UNH scoring B-tier 68.4 intraday long despite active DOJ fraud probe (stock −16%). Legal risk not captured in scoring.
- **evidence:** `data/reports/stocks/intraday/2026-06-26_15-31_stocks_intraday_report.md` §5; catalyst_events.jsonl UNH [legal_risk]
- **suggested fix:** Add legal_risk flag check in stocks scoring; symbols with confirmed legal_risk catalyst cap to AVOID or C-tier with manual_review overlay
- **priority:** high | **first observed:** 2026-06-26 16:23 EEST; confirmed again 18:39 EEST

### TODO-ETH-CONTRADICTION
- **issue:** ETH swing short (65) and ETH swing long (66) both ENTERED UNRESOLVED with TP hit — persists across cycles (16:23 and 18:39).
- **evidence:** `src.cli active-signals --asset-class crypto` 18:39 EEST
- **suggested fix:** Manual operator review; close/cancel conflicting leg; add contradiction detection alert to execution_lifecycle
- **priority:** high | **first observed:** 2026-06-26 16:23 EEST

### TODO-SCHEDULER-LOG-MISSING
- **issue:** `scheduler.log` not found at project root. Freshness check falls back to cycle mtime. Silent crash may not be detected.
- **evidence:** File path check 18:39 EEST — not found
- **suggested fix:** Confirm log location or restore logging. Update SKILL.md §D if intentionally removed.
- **priority:** medium | **first observed:** 2026-06-26 18:39 EEST
