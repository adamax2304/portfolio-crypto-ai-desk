# Opus Enriched Review — Late-Session Risk Review — Auto Cycle 21:40 EEST

> **Advisory only / no auto-trade. Monday June 29, 2026. Slot: late-session risk review (21:30). Crypto: live. US stocks: active session (~14:40 ET, 1.5h to close).**

---

## 1. Executive Summary

**Slot: late-session risk review — advisory only / no auto-trade.**

Current time 21:40 EEST = 14:40 ET (US market open, ~1.5 hours to close). Crypto is in **range/chop** with BTC holding a range and ETH showing a transition_up structure. No A-tier or new B-tier crypto signals generated this cycle — the desk remains on **watch posture** with 9 active B-tier crypto signals (mostly swing positions, several with TP1 already hit).

Key developments since the 18:39 (US open reaction) review:
- **MiCA July 1 deadline is TOMORROW** — EU crypto platforms may see user disruption; 10M EU users may need to switch platforms.
- **CLARITY Act passage odds now at 50%** — macro headwind for US crypto regulation.
- **BTC ETF outflows $1.8B last week** + Fed rate hike bets mounting — risk-off backdrop for BTC.
- **ORDI +36.6% today** — pure momentum, overextended, >2 ATR, REJECTED for entry. Not actionable.
- **TAO (Bittensor)**: Kraken listing of Bittensor subnet alpha tokens — best fresh catalyst in today's cycle, intraday with-catalyst playbook (PF 2.75). No active signal yet.
- **BTC/ETH swing shorts** from the earlier part of the session remain ENTERED UNRESOLVED with TP1 hit. Late session = watch for covering pressure.
- **Stocks**: AMD (B long) and LLY (B long) active in RTH. Regime is chop, VIX 17.66. Late-session entries risky.
- Signal stats improving: crypto B-tier now +11R PF 1.46 (was +8R at 18:39). Shorts outperforming: PF 2.09 vs longs PF 0.92. Exchange-confirmed signals: PF 3.22 (vs 0.08 without).

**Late-session rule**: No new scalp entries (PF 0.14, losing). Crypto intraday without catalyst: avoid (PF 0.70, net-negative). Prefer managing existing signals and watching TAO catalyst.

---

## 2. Data Used

| Source | File | Age (EEST) | Status |
|--------|------|-----------|--------|
| Scheduler log | scheduler.log | <1 min (21:40:25) | **VERY FRESH** |
| Crypto scalp report | 2026-06-29_18-07_scalp_report.md | 21:07 EEST | **FRESH** |
| Crypto intraday report | 2026-06-29_18-32_intraday_report.md | 21:32 EEST | **VERY FRESH** |
| Stocks intraday report | 2026-06-29_18-39_stocks_intraday_report.md | 21:39 EEST | **VERY FRESH** |
| Crypto swing report | 2026-06-29_02-30_swing_report.md | 05:30 EEST | **STALE ~16h** (structure only) |
| Stocks swing report | 2026-06-29_02-31_stocks_swing_report.md | 05:31 EEST | **STALE ~16h** (structure only) |
| LLM crypto packet | llm_analysis_packet.md | 21:33 EEST | **VERY FRESH** |
| LLM stocks packet | llm_stocks_packet.md | 21:40 EEST | **VERY FRESH** |
| Catalyst cycle | catalyst_cycle_18-33.md | 21:33 EEST | **VERY FRESH** |
| Active signals (crypto) | CLI | live | 9 B-tier |
| Active signals (stocks) | CLI | live | 50 signals (2 B-tier) |
| Signal stats (crypto) | CLI | live | n=72, PF=1.46, +11R |
| Signal stats (stocks) | CLI | live | A/B n=23, PF=1.11, +1R |
| Untracked alerts | CLI | live | NONE |
| Previous review | OPUS_ENRICHED_REVIEW_AUTO_2026-06-29_1839.md | 18:39 EEST | Loaded |
| External web research | — | — | **Not run** (internal sources fresh and consistent) |

---

## 3. Scheduler / Data Freshness

- **Scheduler.log mtime:** 21:40:25 EEST — **VERY FRESH**. Last cycle completed just seconds ago.
- **Cycle sequence:** paper-shadow A/B → ledger refresh → OHLCV archive → intelligence layer → stocks intraday (179s) → active-signals x2 → signal-stats x2 → lifecycle review → untracked-legacy. All exit=0.
- **Both freshness checks PASSED — NOT DEFERRED**
- **Catalysts:** catalyst_cycle_18-33.md at 21:33 EEST — VERY FRESH
- **Swing/invest reports:** 05:30 EEST — stale (16h). Carried for structure context only.
- **Onchain config:** config/onchain.yaml still missing — persistent carry-forward blind spot.
- **Reddit social:** 3 subreddits returning 403 — social attention blind.
- **Funding data:** data/raw/funding/binance_futures_latest.json mtime 21:42 EEST — VERY FRESH.
- **Untracked legacy alerts:** NONE — system integrity clean.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-06-29 21:40 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.88,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["onchain_config_missing", "reddit_social_blocked", "swing_report_stale_16h"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 21:40:25 EEST", "intraday crypto report 21:32 EEST", "stocks intraday 21:39 EEST", "catalyst_cycle 21:33 EEST", "swing report 05:30 (16h stale)", "funding 21:42 EEST"]
    },
    {
      "agent": "market_regime",
      "verdict": "mixed",
      "confidence": 0.72,
      "reason_codes": ["chop", "mixed", "shorts_preferred", "wait_for_trigger"],
      "data_missing": ["live_btc_price", "live_eth_price", "macro_calendar"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC trend=range", "ETH trend=transition_up", "altcoin_breadth_ema20=58.14%", "VIX=17.66", "stocks_regime=chop", "BTC ETF outflows $1.8B", "Fed rate hike bets", "CLARITY Act 50%", "crypto shorts PF 2.09 vs longs 0.92"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["fresh_catalyst", "narrative_supported", "catalyst_contradicted", "mapping_weak"],
      "data_missing": ["multi_source_verification", "onchain_flows", "social_sentiment"],
      "suggested_effect": "advisory_only",
      "facts_used": ["TAO: Kraken Bittensor subnet listing (single_source fresh)", "BTC: ETF outflows $1.8B + CLARITY Act 50%", "ETH: whale dump 550K ETH", "Strategy $1B buyback", "MiCA July 1 TOMORROW", "AI narrative basket fresh <1h heat=70.2", "ORDI momentum_breakout basket no confirmed catalyst", "AAPL China chip senator warning"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "ok",
      "confidence": 0.60,
      "reason_codes": ["oi_supports", "data_unavailable"],
      "data_missing": ["oi_data_many_fallback_mexc", "liquidation_heatmap", "order_book_depth"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ORDI funding -3.5e-5 to -4e-5 (not long-crowded despite +36.6%)", "AVAX OI +1.19% long/short 2.271", "NEAR OI -4.63% short covering", "SOL OI -0.31% covering", "MANTA deleveraging", "JTO deleveraging", "BTC/ETH swing shorts from ~62K already 3R+"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["entry_late", "chase_risk", "overextended", "price_moved_away"],
      "data_missing": ["live_price_charts", "order_book", "cvd"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ORDI >2 ATR from EMA20 REJECTED", "AVAX price 6.755 vs entry zone 6.685-6.734 (above zone)", "SYN 27% extended no catalyst", "NEAR 1.900 above entry zone 1.880-1.894", "BTC/ETH shorts 3R+ late for adding", "TAO no signal, pullback entry potential"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.78,
      "reason_codes": ["open_actionable", "entered_unresolved", "no_entry"],
      "data_missing": ["exact_fill_prices", "current_live_prices"],
      "suggested_effect": "advisory_only",
      "facts_used": ["9 active crypto B-tier: AVAX scalp TRIGGERED; ETH/BTC swing shorts TP1-hit ENTERED UNRESOLVED; swing longs (ETH/HOP/BEAM/AAVE/AXL) TP1-hit ENTERED UNRESOLVED some weekend_mode", "50 stocks: AMD/LLY B-tier TRIGGERED; untracked legacy NONE"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.78,
      "reason_codes": ["late_session", "headline_risk", "manual_review"],
      "data_missing": ["daily_pnl_total", "position_size_current"],
      "suggested_effect": "advisory_only",
      "facts_used": ["late US session 14:40 ET (1.5h to close)", "scalp PF=0.14 low_confidence", "AVAX above entry zone borderline", "BTC/ETH shorts 3R+ late-session covering risk", "MiCA July 1 tomorrow", "AAPL soft political warning not enforcement", "weekend approaching (Monday late session)"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "ok",
      "confidence": 0.75,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": ["longer_horizon_data"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto_scalp PF 0.14 (failing)", "crypto_intraday no-catalyst PF 0.70 (-3R)", "crypto_intraday with-catalyst PF 2.75", "crypto_swing PF 5.80 WR 72%", "crypto_failed_bounce_short PF 2.00", "stocks_intraday PF 2.03 WR 55%", "crypto shorts PF 2.09 vs longs 0.92", "exchange_confirmed PF 3.22 vs unconfirmed 0.08"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.72,
    "preferred_side": "catalyst_backed",
    "best_long_candidate": {
      "symbol": "TAO/USDT",
      "trigger": "15m consolidation after Kraken listing spike; RS vs BTC positive; volume >1.5x average; intraday entry per crypto_intraday_catalyst_or_momentum (with-catalyst PF 2.75)",
      "reason": "Kraken listing Bittensor subnet alpha tokens — freshest verified catalyst today; AI narrative basket primary (heat 70.2); no active signal yet"
    },
    "best_short_candidate": {
      "symbol": "MANTA/USDT",
      "trigger": "Post-bounce retest to -15% RS zone, volume thin (<0.5x), stop above swing high; squeeze guard active — do not enter without confirmation",
      "reason": "Largest RS loser -22.7% vs BTC; deleveraging profile; but thin liquidity squeeze risk gate active today"
    },
    "best_catalyst_candidate": {
      "symbol": "TAO/USDT",
      "trigger": "Same as best_long; Kraken listing catalyst + AI narrative fresh <1h; pullback entry on 15m confirmation",
      "reason": "Only name today with specific verifiable exchange listing catalyst; best-performing intraday playbook sub-cohort"
    },
    "avoid_candidate": {
      "symbol": "ORDI/USDT",
      "reason": "Up 36.6% today, >2 ATR from EMA20, pure momentum_breakout basket, no confirmed catalyst, elevated crowding — system correctly rejected, extreme chase risk"
    },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 1
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|-------|---------|-----------|-------------|-----------------|
| data_quality | **ok** | 0.88 | scheduler_fresh, report_stale | advisory_only |
| market_regime | **mixed** | 0.72 | chop, mixed, shorts_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | **caution** | 0.75 | fresh_catalyst, narrative_supported, catalyst_contradicted, mapping_weak | advisory_only |
| derivatives_squeeze | **ok** | 0.60 | oi_supports, data_unavailable | advisory_only |
| technical_entry | **caution** | 0.72 | entry_late, chase_risk, overextended, price_moved_away | advisory_only |
| execution_lifecycle | **ok** | 0.78 | open_actionable, entered_unresolved, no_entry | advisory_only |
| risk_manager | **caution** | 0.78 | late_session, headline_risk, manual_review | advisory_only |
| playbook_performance | **ok** | 0.75 | playbook_working, playbook_failing, low_sample | advisory_only |
| **head_trader** | **caution** | **0.72** | catalyst_backed, watch posture, no new scalp/no-catalyst intraday | advisory_only |

---

## 4. What Changed vs Previous Review

Previous: **OPUS_ENRICHED_REVIEW_AUTO_2026-06-29_1839.md** (US open reaction, 18:39 EEST)

| Item | Previous (18:39) | Now (21:40) | Change |
|------|-----------------|-------------|--------|
| Active crypto signals | 10 B-tier | 9 B-tier | **1 closed/resolved** |
| Crypto stats | +8R, PF 1.33 | +11R, PF 1.46 | **Improved** |
| BTC/ETH swing shorts | 3R+ mentioned | ENTERED UNRESOLVED at TP1 | **Holding, late session** |
| ORDI | +36.6% rejected | Still +36.6% rejected | No change — avoid |
| GOOGL | INVALIDATED (DJIA) | Stays invalidated | No change |
| LLY | Partially confirmed ATH | B-tier fresh, pullback zone | **Updated** |
| AMD | Not in previous | B-tier new this cycle | **New** |
| MiCA July 1 | Mentioned | **TOMORROW** | **Urgency increased** |
| TAO catalyst | AI basket only | Kraken listing confirmed | **NEW specific catalyst** |
| CLARITY Act | Mentioned | Cut to 50% specifically | **New data point** |
| Stocks active signals | ~38 C-tier | 50 (2 B AMD/LLY) | **Expanded** |
| AVAX scalp | Watchlist | B scalp triggered | **Entered** |

---

## 5. Catalyst Coverage

- **Unique events today:** 846 (from scalp report reference) / 500 scanned in latest cycle
- **Narrative baskets active:** 4 (ai_narrative, binance_ecosystem_teaser, perps_dex_narrative, momentum_breakout)
- **Unmapped ratio:** Dominant "other_news" classification (456/500) limits precision mapping. **Use catalyst layer as context, not final decision.**

### Top catalysts ranked (importance):
1. **BTC [regulatory_sector_headline]** — ETF outflows $1.8B + Fed rate hike bets (The Block) — BEARISH BTC
2. **BTC [buyback_burn]** — Strategy $1B buyback + capital framework (Cointelegraph) — MIXED
3. **TAO (via AI basket)** — Kraken lists Bittensor subnet alpha tokens (CryptoBriefing) — BULLISH TAO
4. **(basket) [legal_risk]** — DOJ grand jury investigation, Singham network (CryptoBriefing) — BASKET RISK
5. **(basket) [regulatory]** — MiCA July 1 deadline, 10M EU users (CoinDesk) — MACRO RISK
6. **(basket) [regulatory]** — CLARITY Act 50% odds (CryptoSlate/Decrypt) — HEADWIND
7. **NVDA [product_launch]** — Claude/Anthropic on GB300 Blackwell Ultra Azure — POSITIVE NVDA
8. **TSLA** — +5.2% recovery (WalterBloomberg/Yahoo Finance) — POSITIVE TSLA
9. **AAPL** — Sen. Cotton China chip warning — SOFT RISK AAPL

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** mixed/chop — BTC in range with risk-off macro headwinds (ETF outflows, Fed bets, CLARITY Act 50%); ETH transition_up; 58% alts above EMA20 (neutral-positive breadth)
- **Stocks mood:** chop — VIX 17.66, SPY/QQQ ranging, IWM/DIA uptrend; late US session (14:40 ET)
- **Dominant narrative:** Regulatory uncertainty (MiCA tomorrow, CLARITY Act) + AI strength (TAO Kraken listing, NVDA Blackwell) + BTC macro risk-off backdrop
- **Preferred side now:** catalyst-backed longs (TAO/AI) + shorts on RS losers after squeeze confirmation; no new scalp; no no-catalyst intraday
- **Best long candidate:** TAO/USDT — trigger: 15m consolidation post-Kraken listing, RS vs BTC positive, vol >1.5x
- **Best short candidate:** MANTA/USDT — trigger: failed bounce to -15% RS zone, thin volume, stop above swing high (squeeze gate active)
- **Best catalyst-backed candidate:** TAO/USDT (Kraken listing Bittensor subnet tokens)
- **What to avoid:** ORDI (>2 ATR chase), SYN/HEI (pure momentum no catalyst), new crypto scalp, new stocks intraday <1.5h before close
- **What would change the view:** BTC breaks range support → confirm risk-off, adds momentum to existing shorts; TAO volume confirms on pullback → actionable long; ETH closes above transition_up key level → reduce swing short exposure

---

## 7. Candidate Deep Dives

### Candidate 1 — TAO/USDT (LONG watch, catalyst-backed)

**Why included:** Kraken listing Bittensor subnet alpha tokens (fresh, single_source CryptoBriefing). AI narrative basket primary (heat 70.2/100, fresh <1h). Best intraday playbook sub-cohort when catalyst present: PF 2.75. No current active signal — monitoring.

**Catalyst quality:** Specific exchange listing = high-quality catalyst type (verifiable, actionable). Single_source verification only — no second confirmation from CoinDesk/Decrypt yet. Treat as confirmed-pending.

**Price context:** TAO not in current active signals. AI narrative basket primary. No current OHLCV signal level available. TradingView/manual chart check unavailable.

**Chase/entry check:**
- Exchange listings often spike immediately then retrace. Entering immediately after announcement = high chase risk.
- Wait for: 15m consolidation candle, pullback into support, volume >1.5x confirming buying sustained.
- Is it late to enter now? Unknown without live price. If Kraken listing was announced hours ago, spike may be spent.
- Actionable NOW or after confirmation? **After confirmation** — pullback + volume + RS check.
- Invalidation: 1h close below pre-listing base.
- Catalyst alignment: STRONG (specific exchange listing + AI narrative basket).
- **Verdict: WAIT FOR TRIGGER (pullback + volume). Most actionable idea for Asia session follow-through.**

---

### Candidate 2 — BTC/ETH Swing Shorts (ENTERED UNRESOLVED at TP1)

**Status:** ENTERED UNRESOLVED. Entered ~$62K BTC (from previous review context). TP1 hit per CLI status. Now in late US session.

**Late-session risk:**
- 14:40 ET = 1.5h to US close. Short covering into close is common behavior.
- BTC at range (~range regime). ETH showing transition_up = technical conflict with short.
- At TP1 (3R+ from entry): already a significant gain. The question is whether TP2 is reachable vs a squeeze into close.
- Do NOT add to shorts now. Manage existing position: tighten mental stop, watch for intraday squeeze signals.
- If BTC shows strong bid / volume surge into close → consider partial profit at current level.
- MiCA tomorrow: could cause overnight volatility in either direction.

**Verdict: ENTERED UNRESOLVED — HOLD with active monitoring. No additions.**

---

### Candidate 3 — AVAX/USDT (B Scalp — TRIGGERED, above entry zone)

**Status:** TRIGGERED per CLI. Score 68.5/100 (scalp), mode=scalp, low_confidence.

**Price issue:** Report price 6.755, entry zone 6.685–6.734, resistance 6.714. Current price is ABOVE the entry zone and above resistance. The scalp was triggered (touched entry zone) but price has since moved up to resistance level.

**Scalp PF context:** PF 0.14 (losing playbook, low_confidence). Known failure: TP1 1.84R vs avg captured MFE 0.54R. Mean-reverts before TP.

**Action:** If already in position (triggered): hold with stop at 6.627. TP1 is 6.862. Monitor whether price holds above resistance 6.714.
If NOT yet in position: DO NOT ENTER above the entry zone (6.734). Stale-entry risk.

**Verdict: MONITOR EXISTING TRIGGERED SIGNAL. No new entry above zone.**

---

### Candidate 4 — AMD / LLY (Stocks B-tier, late session)

**AMD (B long, 65.09, triggered):**
- RS vs SPY +6.53% (20d), semiconductor sector leader (+7.50% RS 20d).
- NVDA Blackwell Ultra/Azure news provides sector tailwind (AI chips).
- Entry zone 532.37–538.94. Triggered per CLI.
- RR to TP1: 1.0 (below 1.5, penalized). Late-session: 1.5h to close.
- **Action: Hold triggered position with stop at 519.24. No fresh size.**

**LLY (B long, 65.09, triggered):**
- RS vs SPY +12.95% (20d), healthcare sector strongest (+9.44% RS 20d).
- From 18:39 review: LLY hit ATH $1,238, pulled back to ~$1,205. Entry zone now 1215.48–1224.89 = clean retest zone from ATH pullback.
- This is actually the most technically clean setup: ATH hit → pullback → retest zone → potential continuation.
- RR to TP1: 1.0 (penalized but structure is clean).
- **Action: Hold triggered position with stop at 1196.67. LLY retest is the best stocks setup tonight.**

**Verdict: HOLD TRIGGERED POSITIONS. LLY technically cleanest. No fresh stocks entries <1.5h before close.**

---

### Candidate 5 — MANTA/USDT (Short watch — squeeze-gated)

**Why included:** Weakest RS vs BTC at -22.7% over 24h. Crypto shorts PF 2.09 outperforming. Deleveraging profile.

**Profile:**
- MANTA: price down + OI down = deleveraging. Funding -0.00060065 (crowding unknown). Long/short 0.962 (balanced, slightly short-heavy).
- Scalp report: "short squeeze risk → capped to C: thin_liquidity_short_squeeze_risk (+exhaustion)"
- After -21.34% today: chasing a short here is EXTREMELY DANGEROUS. Need a bounce first.

**Trigger:** Post-bounce (dead-cat or technical bounce) to the -15% RS zone. Volume must stay thin (confirming no real buyers). Clear stop above swing high. Verify no crowding flip.

**NOT actionable today** after -21% move. Gate: post-bounce retest only.

**Verdict: SHORT WATCH ONLY. Not today. Gate: bounce-to-retest + squeeze check.**

---

## 8. Best Candidates Ranked

| Rank | Symbol | Direction | Status | Trigger |
|------|--------|-----------|--------|---------|
| 1 | TAO/USDT | Long (catalyst) | WAITING FOR ENTRY | 15m consolidation post-Kraken listing, vol >1.5x, RS vs BTC positive |
| 2 | BTC/ETH shorts | Short (existing) | ENTERED UNRESOLVED (TP1) | Monitor TP2, watch late-session covering; no additions |
| 3 | LLY | Long (stocks) | TRIGGERED (ENTERED UNRESOLVED) | Hold, retest zone $1,215-1,225 after ATH pullback; stop 1196.67 |
| 4 | AMD | Long (stocks) | TRIGGERED (ENTERED UNRESOLVED) | Hold, semiconductor sector play; stop 519.24 |
| 5 | MANTA/USDT | Short (watch) | WAITING (squeeze-gated) | Post-bounce retest to -15% RS zone, thin volume, squeeze check |

**Best long-watch for Asia session:** TAO/USDT (Kraken listing + AI narrative carry-through)
**Best short-watch trigger:** BTC break below range support → momentum on existing swing short
**Best catalyst-watch:** TAO/USDT, then NEAR/USDT (AI basket secondary)

---

## 9. Avoid / No Trade — This Window Only

1. **ORDI/USDT** — up 36.6%, >2 ATR, no catalyst, crowding elevated. System correctly rejected. Do not enter at any level until significant pullback and digest.
2. **SYN/USDT, HEI/USDT** — up 27% and 14%, pure momentum_breakout basket, no verified catalysts. No-catalyst intraday PF 0.70 (negative). Avoid.
3. **New crypto scalp entries** — scalp PF 0.14. AVAX scalp already active; no additional scalp entries.
4. **New stocks intraday entries (fresh)** — <1.5h to US close, chop regime. Existing triggered = manage; new = time-risk.
5. **AVAX scalp if not yet entered** — price above entry zone (6.755 vs 6.685-6.734). Do not chase.
6. **BTC/ETH short additions** — already 3R+ from entry. Late session covering risk. No new size.
7. **AAPL short** — senator warning is political statement, not enforcement. Single_source soft risk only. C-tier; skip.

_ALWAYS-SCAN continues. This verdict is for this late-session window only. Scanning, data collection, and tracking continue normally._

---

## 10. Main Risks

1. **MiCA July 1 deadline (TOMORROW)** — EU platform disruption, 10M users potentially switching. Overnight/Asia volatility risk.
2. **BTC ETF outflows + Fed rate hike bets** — macro risk-off. Range break below support → swing shorts accelerate.
3. **Late-session squeeze on BTC/ETH shorts** — positions 3R+ in profit. Covering into US close can cause sharp short-term spikes.
4. **CLARITY Act at 50%** — if news breaks on passage or failure, sharp macro catalyst reaction.
5. **ORDI momentum trap** — a dump from current extension could drag broader market temporarily.
6. **Scalp PF 0.14** — AVAX scalp active, low-confidence. If TP1 not hit in 2h window → treat as NO-ENTRY/STALE.
7. **Data blind spots** — no live social attention, onchain missing, Reddit blocked, liquidation heatmaps absent.
8. **AMD/LLY RR below 1.5** — stock entries have mathematical RR disadvantage. Edge is RS leadership + sector alignment. Size conservatively.
9. **Source-discipline note:** external web research not run this slot; all claims sourced from internal pipeline only. TAO/Kraken catalyst = single_source (CryptoBriefing), not multi-verified.

---

## 11. Action Plan — Next 4 Hours

| Window | Action |
|--------|--------|
| 21:40–22:00 EEST | Monitor BTC/ETH shorts: TP1 hit, watch for TP2 move or late-session covering. Monitor AVAX scalp: TP1=6.862, stop=6.627. |
| ~22:00 (US close, 15:00 ET) | Stocks session closes. Note AMD/LLY status. Intraday results. |
| 22:00–00:00 EEST | Post-close crypto. Watch BTC range. Monitor TAO for Kraken listing impact and pullback entry zone. |
| 00:00+ (Asia open) | MiCA July 1 risk window begins. Watch EU-listed exchange tokens for disruption. AI basket (TAO, NEAR) follow-through potential. |
| All windows | ALWAYS-SCAN continues. No new scalp entries. No no-catalyst intraday. Catalyst-backed (TAO) if trigger met. |

---

## 12. Final Verdict per Mode

| Mode | Verdict | Notes |
|------|---------|-------|
| **Crypto scalp** | WATCH ONLY / LOW CONFIDENCE | AVAX B scalp active; monitor existing; no new entries; PF 0.14 |
| **Crypto intraday (no catalyst)** | AVOID | PF 0.70, net -3R; chop regime compounds this |
| **Crypto intraday (with catalyst)** | WAIT FOR TRIGGER | TAO/USDT: Kraken listing catalyst, wait for pullback + volume; PF 2.75 |
| **Crypto swing** | MANAGE EXISTING | BTC/ETH shorts ENTERED UNRESOLVED at TP1; swing longs also active; no new swing entries tonight |
| **Crypto short** | HOLD / NO NEW SIZE LATE SESSION | Shorts PF 2.09; existing 3R+; late-session covering risk; no additions |
| **Stocks intraday** | MANAGE TRIGGERED / NO NEW ENTRIES | AMD/LLY triggered; <1.5h to US close; hold with stops |
| **Stocks swing/invest** | WATCHLIST ONLY (PAUSED) | Swing PF 0.15, invest WR 0%; paused per playbook audit |

---

## 13. Sources

- Scheduler / Internal CLI — data/autostart/scheduler.log mtime 21:40:25 EEST
- Crypto reports (internal) — data/reports/scalp/2026-06-29_18-07_scalp_report.md, data/reports/intraday/2026-06-29_18-32_intraday_report.md
- Stocks intraday (internal) — data/reports/stocks/intraday/2026-06-29_18-39_stocks_intraday_report.md
- Catalyst cycle (internal) — data/catalysts/2026-06-29/catalyst_cycle_18-33.md at 21:33 EEST
- Active signals / signal stats — CLI live at 21:40 EEST
- Previous review — OPUS_ENRICHED_REVIEW_AUTO_2026-06-29_1839.md
- TAO catalyst — internal news_items via CryptoBriefing (single_source, not multi-verified)
- BTC ETF outflows — internal news_items via The Block (single_source)
- MiCA deadline — internal news_items via CoinDesk (single_source)
- CLARITY Act — internal news_items via CryptoSlate/Decrypt (single_source)

**External web research: Not run this slot.** All data from internal pipeline. Candidates dependent on external verification have been marked single_source or kept at watch/manual status.

---

## 14. Fix Requests / TODO

### TODO-scalp-avax-price-vs-entry-zone
- **issue:** AVAX scalp shows "triggered" but current price (6.755) is above entry zone (6.685–6.734) and above resistance (6.714). Report data freshness is 17:45+00:00 (UTC); price may have moved significantly since entry zone was set. Need to verify whether "triggered" correctly reflects a historical touch of the entry zone or a live-price stale comparison.
- **evidence:** scalp report entry_low=6.685, entry_high=6.734, current_price=6.755, resistance=6.714; data freshness 2026-06-29 17:45:00+00:00
- **suggested manual fix:** In a manual session, check the AVAX 5m/15m chart around 17:45-21:07 UTC to confirm the signal entry zone was actually touched. If it was: standard behavior (price moved from entry to above resistance = working). If not: audit trigger logic vs OHLCV freshness.
- **priority:** low
- **first observed:** 2026-06-29 21:40 EEST

_No other issues this run._
