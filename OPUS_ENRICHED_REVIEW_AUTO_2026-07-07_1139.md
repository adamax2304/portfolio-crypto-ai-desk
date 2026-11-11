---
REVIEW: OPUS ENRICHED REVIEW — ⚠ ADVISORY ONLY — NO EXECUTION
SLOT: Europe / Pre-US Context · 2026-07-07 · 11:30 EEST
WRITTEN: 2026-07-07 11:39 EEST
PREV REVIEW: 2026-07-07 04:40 EEST (crypto overnight / Asia review)
STATUS: AUTOMATED SCHEDULED RUN — NO HUMAN IN SESSION
---

# Opus Enriched Review — Europe / Pre-US Context — Auto Cycle 11:39 EEST

## 1. Executive Summary

**Slot: Europe / pre-US context — advisory only / no auto-trade.**

BTC and ETH remain in uptrend (~$63,182 BTC), altcoin breadth 68.3% above EMA20 — regime is **bullish trend / risk-on**. Asia dead-zone has cleared (was 03:00–09:00 EEST). Cycle 03 completed successfully at 09:55 EEST with 32/32 steps OK; monitors actively running (last: 11:27 EEST). US cash open is ~4.5 hours away (16:30 EEST / 09:30 ET); stocks are in **planning-only** mode until then.

**Key shift vs 04:40 review**: BLUR A-tier swing TP has been hit — price moved from the 0.0187–0.0195 entry zone flagged in the overnight review through TP1 levels. The 41% BLUR surge is confirmed altcoin-season-driven with no specific fundamental catalyst; a token unlock is scheduled **July 14** — this limits new swing entries to retest-only and reduces continuation confidence. XRP MiCA catalyst has **backfired** (price dropped ~3% on the announcement at $1.05); do not open fresh long on that thesis.

**Key risk event**: FOMC minutes release **tomorrow, July 8 at 14:00 ET / 21:00 EEST**. All new swing positions opened today will face this event overnight. Reduce swing sizing and confirm entries only on pullback/retest structures.

**Best ideas for the pre-US window**: PYTH/USDT (cleanest long setup — near entry zone 0.0445–0.0451, fresh OI + RWA narrative); BLUR/USDT for retest-watch (pullback to 0.0187–0.0195 zone only — do not chase current price); BONK short only on failed bounce (confirmed $20M governance hack — but squeeze risk means manual-review-only, not direct entry). US cash open watchlist: AAPL (90), TSLA (89), XLV/XLF/XLY sector ETFs — wait for RTH open confirmation before any action.

---

## 2. Data Used

| Source | File / Timestamp | Age at 11:39 EEST | Quality |
|--------|-----------------|-------------------|---------|
| Scalp report | `data/reports/scalp/2026-07-07_06-38_scalp_report.md` | ~2h (data 06:30 UTC) | **FRESH** ✓ |
| Intraday report | `data/reports/intraday/2026-07-07_06-44_intraday_report.md` | ~1h55m | **FRESH** ✓ |
| Swing report | `data/reports/swing/2026-07-07_02-03_swing_report.md` | ~6h36m | **CARRY-FORWARD** ⚠ (4–12h range) |
| Stocks intraday | `data/reports/stocks/intraday/2026-07-07_06-51_stocks_intraday_report.md` | ~1h48m | **FRESH** ✓ |
| Stocks swing | `data/reports/stocks/swing/2026-07-02_13-03_stocks_swing_report.md` | 5 days | **STALE** ✗ (exclude) |
| Stocks invest | `data/reports/stocks/invest/2026-07-02_13-05_stocks_invest_report.md` | 5 days | **STALE** ✗ (exclude) |
| Previous review | `OPUS_ENRICHED_REVIEW_AUTO_2026-07-07_0440.md` | ~7h | CONTEXT |
| Cycle 03 summary | `data/scheduled_runs/2026-07-07_default_schedule/cycle_03_09-31_summary.md` | 1h44m | FRESH |
| Active signals (crypto) | CLI `active-signals --asset-class crypto` | live | LIVE (~50 signals incl. TP hits) |
| Signal stats (crypto) | CLI `signal-stats --asset-class crypto` | live | LIVE |
| Untracked alerts | CLI `detect_untracked_legacy_alerts --since 2026-07-07` | live | LIVE (0 alerts) |
| Catalyst events | `data/catalysts/2026-07-07/catalyst_events.jsonl` | cycle 03 | 488 events / 4 baskets |
| External sources | WebSearch (BLUR, XRP, BONK, BTC/FOMC) | live | Multiple (see §13) |

**Notes:**
- TradingView / manual chart check unavailable. All technical observations from local OHLCV / ATR / EMA fields only.
- Swing report carry-forward (~6.5h from report generation) — entry zones may have shifted.
- Stocks swing/invest: 5 days stale — excluded from actionable decisions.
- Social attention missing (Reddit 403 errors consistently); no live KOL/X/Telegram data.
- Onchain: `interface_ready_config_missing` (no `config/onchain.yaml`) — whale/exchange flows blind.

---

## 3. Scheduler / Data Freshness

- **Last completed cycle**: `cycle_03_09-31_summary.md` — finished 09:55 EEST (1h44m ago). 32/32 steps OK, 0 failed.
- **Scheduler health**: FRESH. Monitors actively running: crypto_monitor last log 11:27 EEST (12m ago), stocks_monitor last log 11:23 EEST (16m ago).
- **Data freshness**:
  - Scalp / Intraday OHLCV: fresh (cycle 03 ran reports at 09:34–09:44 EEST)
  - Swing: carry-forward (generated 05:03 EEST, data 02:00 UTC)
  - Stocks: after-hours context; US session opens at 16:30 EEST
- **Staleness flags**:
  - Stocks swing/invest: 5 days old — excluded entirely
  - Derivatives OI numeric history: sparse (intelligence layer)
  - Social attention: missing (Reddit 403)
  - Onchain: `interface_ready_config_missing`
  - Dead news sources: 11 (incl. SEC EDGAR, Business Wire, t.me/ announcement channels)
  - **FOMC minutes: July 8 at 14:00 ET / 21:00 EEST** — confirmed via CoinDesk (July 6)
- **Asia dead-zone**: CLEARED at 09:00 EEST / 06:00 UTC — EU session active
- **Paper portfolio** (bybit_non_vip): net +$1,887 / +37.75% / maxDD 13.62% (842 deduped trades; paper only)
- **Paper shadow B vs A**: B net +163.12R forward (12d, NOT_READY 4/6, DATA_GAP_LATE 38%)
- **Untracked alerts**: 0 (clean — was 24 at 23:15 July 6; clean since 04:40 review)

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-07-07 11:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.87,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["onchain_config_missing", "social_attention_missing", "derivatives_sparse"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Cycle 03 completed 09:55 EEST (1h44m ago), 32/32 OK",
        "Monitors running: crypto 11:27, stocks 11:23 EEST",
        "Scalp/intraday/stocks intraday: FRESH (<2h)",
        "Swing: carry-forward (~6.5h from report generation)",
        "Stocks swing/invest: 5 days STALE — excluded",
        "11 dead news sources including SEC EDGAR, Business Wire",
        "OI numeric history sparse per intelligence layer",
        "No onchain.yaml config — whale flows blind"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.83,
      "reason_codes": ["risk_on", "longs_preferred"],
      "data_missing": ["social_attention_missing"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC trend: uptrend (~$63,182)",
        "ETH trend: uptrend",
        "Altcoin breadth above EMA20: 68.3%",
        "Altcoin breadth above EMA50: 75.61%",
        "F&G=27 (fear) — sentiment divergence vs bullish regime",
        "VIX=15.57 (low vol — supports risk-on)",
        "Stocks: all 4 indices uptrend, 100% breadth above EMA20",
        "crypto_mode=trend; stocks_mode=risk_on (dashboard snapshot)",
        "Multiple signals in tp status — market moved up strongly through Asia/EU morning"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.62,
      "reason_codes": ["stale_catalyst", "catalyst_contradicted", "fresh_catalyst", "mapping_weak"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BLUR: no specific catalyst for 41% surge — altcoin-season-driven; Binance monitoring tag (June 18); token unlock July 14",
        "XRP: MiCA license announced July 6 but price DROPPED ~3% to $1.05 — catalyst_contradicted",
        "BONK: $20M governance treasury attack confirmed July 7 (CoinDesk) — fresh bearish catalyst",
        "SOL: Bonk DAO attack = SOL ecosystem exploit_hack risk; operator-review warning active",
        "ETH: UXLINK hacker (14,336 ETH transfers) — operator-review warning",
        "Active narrative baskets: delisting_thin_liquidity, binance_ecosystem_teaser (BNB), rwa_narrative (ONDO/XLM), ai_narrative (NEAR/RENDER/TAO/FET)",
        "catalyst_events today: 488 (cycle 03) / 668 (intraday report) — partial mapping ~40-45% unmapped"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["funding_extreme", "data_unavailable"],
      "data_missing": ["oi_numeric_history_sparse"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BLUR: funding negative Bybit(-0.00123), OKX(-0.00324), MEXC(-0.00601) — crowding elevated (short crowding = longs safe; but reversal squeeze risk for longs)",
        "VANRY: funding negative Bybit(-0.00143), MEXC(-0.00112) — crowding elevated",
        "OPG: funding very negative Bybit(-0.00990), OKX(-0.00946) — extreme; do not short",
        "PYTH: funding neutral (5e-05), OI+2.18% — fresh positioning, low crowding — cleanest derivatives picture",
        "BTC: funding reportedly 9% (news: 'funding rates hit 9%') — elevated long crowding",
        "BONK: squeeze_risk flagged in production gating — thin liquidity, high upper wick",
        "Phase distribution: 45 symbols post_unwind_chop, 34 build_up, 7 squeeze_expansion — moderate squeeze risk across universe"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.67,
      "reason_codes": ["chase_risk", "clean_retest", "overextended", "entry_late"],
      "data_missing": ["tradingview_charts_unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "PYTH: current 0.0454 vs entry zone 0.0445–0.0451 — near-zone, not a chase; ATR=0.0014",
        "BLUR: current ~0.0204 vs swing entry zone 0.0187–0.0195 — A-tier TP already hit; stale_before_entry for new long at current price",
        "VANRY: current ~0.0078-0.0081 vs entry zone 0.0076-0.0080 — +45% 24h / +175% 7d — overextended",
        "EPIC: current ~0.4620 vs entry zone 0.4489-0.4621 — near zone; transition_up; no catalyst",
        "BTC swing: B-tier WAITING at ~63K — cleanest macro proxy if US macro cooperates",
        "All technical observations from local OHLCV / ATR fields only — no TradingView charts available"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.83,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "OPEN ACTIONABLE: 9",
        "WAITING FOR ENTRY: 2",
        "ENTERED UNRESOLVED: 19 (entered, no TP/SL before window — not missed entries)",
        "REVIEW/SHADOW: 151",
        "NO-ENTRY/STALE/MOVED-AWAY: 94",
        "CLOSED WIN/LOSS/FLAT today: 362W / 70L / 0flat",
        "NEEDS REVIEW: 1",
        "BLUR A-tier swing: TP HIT (tp status in active-signals) — CLOSED WIN",
        "Multiple signals (VANRY, HMSTR, BONK, BCH, ZK, ARB, SOL, HEX, JTO) showing tp status in live CLI — bullish session",
        "Scalp kill-switch active — no new scalp proposals actionable",
        "Telegram paper_monitor_status: sent OK; paper-shadow digest: config_path error (not sent)"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.73,
      "reason_codes": ["headline_risk", "legal_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "FOMC minutes: July 8 14:00 ET / 21:00 EEST TOMORROW — new swings today carry overnight event risk; reduce size 30-50%",
        "SOL: Bonk treasury drained $20M governance attack (block_requires_operator_review)",
        "ETH: UXLINK hacker 14,336 ETH transfers (block_requires_operator_review)",
        "HYPE: Fake HyperSwap airdrop drained $12,300 (block_requires_operator_review)",
        "MSFT: securities fraud class action (block_requires_operator_review)",
        "SMCI: federal securities lawsuit export-control violations — AVOID stock long",
        "UNH: DOJ fraud probe, -16% drop — AVOID stock long",
        "BLUR: token unlock July 14 (7 days) — swing duration must be limited",
        "BLUR: Binance monitoring tag (June 18) — persistent elevated risk",
        "APT: token unlock this week",
        "BTC funding 9%: elevated long crowding; de-leveraging risk on sentiment shift",
        "Stocks A/B 7d: 0% WR (weak sample n=28) — extra confirmation required"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "ok",
      "confidence": 0.72,
      "reason_codes": ["playbook_working", "low_sample", "fresh_expired_problem"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto A/B: sample=418 (reliable), PF=1.52, WR=15%, totalR=+40.2R — playbook working",
        "Crypto swing mode: PF=1.8, WR=21% (n=150) — strongest mode",
        "Crypto scalp mode: PF=0.6, WR=2% (n=136) — playbook_failing (kill-switch confirmed correct)",
        "Crypto intraday no-catalyst 14d: WR=23%, PF=0.70, −3R — borderline; use with caution",
        "Paper portfolio: bybit net +$1887/+37.75% (842 deduped trades)",
        "Shadow B forward: +163.12R (12d); NOT_READY for promotion (4/6 gates); DATA_GAP_LATE 38%",
        "Stocks A/B: sample=28 (weak), PF=0.0, WR=0%, totalR=-3.0R — all losses",
        "Stocks C-tier: PF=0.538, WR=3.2% (n=208 reliable) — underperforming"
      ]
    },
    {
      "agent": "head_trader",
      "overall_verdict": "caution",
      "confidence": 0.71,
      "preferred_side": "longs",
      "best_long_candidate": {
        "symbol": "PYTH/USDT",
        "trigger": "Pullback into 0.0445–0.0451 zone on 15m structure with volume confirmation; BTC holds local support; reduce size 30-50% for FOMC tomorrow",
        "reason": "Cleanest entry zone — near-zone, fresh OI (+2.18% price+OI up), neutral funding, RWA narrative basket, less extended than BLUR/VANRY"
      },
      "best_short_candidate": {
        "symbol": "BONK/USDT",
        "trigger": "Failed bounce above local swing low with derivatives confirmation and stop above swing high; MANUAL REVIEW REQUIRED — do not enter on momentum",
        "reason": "Confirmed $20M governance attack July 7; -10% already; but thin liquidity squeeze risk — manual review only"
      },
      "best_catalyst_candidate": {
        "symbol": "BLUR/USDT",
        "trigger": "Retest of swing zone 0.0187–0.0195 holding as support; do NOT chase at current price; limit swing duration to <7 days (before July 14 unlock)",
        "reason": "A-tier TP hit this session; altcoin season momentum confirmed; bounded by token unlock July 14 and Binance monitoring tag"
      },
      "avoid_candidate": {
        "symbol": "VANRY/USDT",
        "reason": "+175% in 7 days, +45% in 24h — extreme extension, no catalyst, momentum_breakout wait_pullback basket; short squeeze risk; extreme chase risk on long side; keep off desk until multi-day consolidation"
      },
      "operator_action": "watch",
      "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
      "todo_count": 3
    }
  ]
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason Codes | Suggested Effect |
|---|---|---|---|---|
| data_quality | **ok** | 0.87 | scheduler_fresh, report_stale | advisory_only |
| market_regime | **ok** | 0.83 | risk_on, longs_preferred | advisory_only |
| catalyst_narrative | **caution** | 0.62 | stale_catalyst, catalyst_contradicted, fresh_catalyst, mapping_weak | advisory_only |
| derivatives_squeeze | **caution** | 0.55 | funding_extreme, data_unavailable | advisory_only |
| technical_entry | **caution** | 0.67 | chase_risk, clean_retest, overextended, entry_late | advisory_only |
| execution_lifecycle | **ok** | 0.83 | open_actionable, waiting_for_entry, entered_unresolved | advisory_only |
| risk_manager | **caution** | 0.73 | headline_risk, legal_risk, reduce_risk | advisory_only |
| playbook_performance | **ok** | 0.72 | playbook_working, low_sample, fresh_expired_problem | advisory_only |
| **head_trader** | **caution** | 0.71 | — | advisory_only |

---

## 4. What Changed vs Previous Review (04:40 EEST)

| Category | 04:40 Review | 11:39 Review (Now) |
|---|---|---|
| Asia dead-zone | ACTIVE (cleared at 09:00) | **CLEARED** |
| BLUR A-tier swing | Actionable — entry 0.0187–0.0195 | **TP HIT** — CLOSED WIN; watch for retest only |
| BLUR risk | Binance monitoring tag only | + **Token unlock July 14** (NEW, from external research) |
| XRP/MiCA | Catalyst-backed — positive framing | **Backfired** — price -3% on announcement; avoid new long |
| BONK attack | Initial news ($20M) | **Fully confirmed** — mechanics detailed (CoinDesk July 7); -10% on token |
| PYTH | Best long candidate | **Remains best long** — near zone at 0.0445–0.0451 |
| FOMC | "July 8, reduce sizing" | **Confirmed July 8 14:00 ET** (CoinDesk source) — 33h away |
| Market activity | Asia dead-zone limiting signals | Multiple signals hitting TP across board — very bullish tape |
| Untracked alerts | 0 | **0** (still clean) |

**Upgraded**: PYTH (confirmed best long), BONK (bearish thesis now fully confirmed)
**Downgraded**: XRP (catalyst failed); BLUR swing (TP hit, now retest-watch with unlock risk)
**New risk**: BLUR token unlock July 14 (7 days)
**New info**: FOMC minutes July 8 confirmed (was estimate, now CoinDesk-sourced)

---

## 5. Catalyst Coverage

- **Total catalyst events today**: 488 (cycle 03 scan) / 668 (intraday report — additional data)
- **Active narrative baskets (4)**: `delisting_thin_liquidity`, `binance_ecosystem_teaser` (BNB), `rwa_narrative` (ONDO, XLM), `ai_narrative` (NEAR, RENDER, TAO, FET)
- **Mapped symbols clearly identified**: BTC, ETH, SOL, XRP, INJ, ZEC, BONK, ADA, LINK, AAVE, HYPE, MSFT, SMCI, UNH, LLY, JPM, APT + basket items
- **Estimated unmapped (basket-only, no direct symbol)**: ~40–45% — GeneDx/WGS, TPI Composites, AVAV, PODD/Insulet, etc.
- **Unmapped % is below 50%** — catalyst layer usable normally (no "context-only" warning triggered)
- **Notable events**:
  - **SOL** [exploit_hack]: Bonk DAO treasury drained $20M governance attack (Decrypt/CoinDesk July 7) — confirmed bearish for SOL ecosystem
  - **XRP** [regulatory]: Ripple MiCA CASP license — confirmed but price reaction negative (-3%)
  - **BTC** [regulatory]: Bitmine $74M ETH buys; Clarity Act improving odds; US BTC reserve federal debate
  - **BONK** [exploit_hack]: Direct governance attack — fresh bearish catalyst; attacker cashing out
  - **UNH** [legal_risk]: DOJ fraud probe — AVOID stock long
  - **MSFT** [legal_risk]: Securities fraud class action — AVOID stock long
  - **SMCI** [legal_risk]: Federal securities lawsuit export-control — AVOID stock long
- **Catalyst mapping quality**: moderate. Top RS leaders (BLUR, VANRY) lack verified catalyst linkage. This limits intraday confidence on those setups.

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood**: risk-on / trend
- **Stocks mood**: risk-on / pre-market (closed; US opens 16:30 EEST)
- **Dominant narrative**: Altcoin season breakout (multiple 30–45% 24h moves, TP hits across board); regulatory clarity improving (Clarity Act, MiCA milestones); FOMC uncertainty caps tail
- **Preferred side now**: longs — pullback/retest entries only; do not chase extended moves
- **Best long candidate**: PYTH/USDT — trigger: pullback into 0.0445–0.0451 zone with 15m structure hold
- **Best short candidate**: BONK/USDT — trigger: failed bounce; MANUAL REVIEW REQUIRED first (squeeze risk)
- **Best catalyst-backed candidate**: BLUR/USDT — trigger: retest of 0.0187–0.0195 zone; NOT at current price; bounded by July 14 token unlock
- **What to avoid**: VANRY (+175% 7d; extreme extension; no catalyst); XRP (catalyst disappointed); stocks intraday before 16:30 EEST RTH open; leveraged chasing of extended moves
- **What would change the view**: BTC losing ~62K support → reduce longs; FOMC minutes hawkish tomorrow → reduce swing exposure; exploit spreading to major protocols → risk-off; BTC funding normalizing → more room for alts

### Macro Context
- VIX: 15.57 (low) — supportive for risk-on
- F&G: 27 (Fear) — contrarian-positive; sentiment diverges from bullish price regime
- SPY: uptrend +3.06% 5d / QQQ +2.31% 5d / DIA +2.38% 5d
- Financials (XLF) strongest sector 20d: +7.57% RS vs SPY; Energy (XLE) weakest: -9.57%
- **FOMC minutes: July 8 14:00 ET / 21:00 EEST** — confirmed risk event for tomorrow
- US 2yr breakeven inflation below 2% (first time since 2024) — dovish Fed expectation, positive for crypto

---

## 7. Candidate Deep Dives

### Candidate 1: PYTH/USDT — LONG — WAITING FOR ENTRY (Best Long-Watch)

**Status**: B-tier swing (score 69.8), WAITING FOR ENTRY
**SL**: 1h close below 0.0438

**Has price already reacted?** PYTH +8.7–11.3% in 24h, +27% in 7d — moderate move, the least extended of the major RS leaders. Price ~0.0454, entry zone 0.0445–0.0451. A 0.5–1% dip gets in.

**Is the setup chasing?** No — if price enters zone, that is a retest entry, not a chase. Current price is 0.5% above zone top.

**Is there a retest/pullback structure?** Entry zone is ATR-grounded (ATR=0.0014). Zone top = 0.0451 = ~one ATR below current. Support 0.0407, Resistance 0.0477 — entry is mid-range.

**Is the move overextended?** Moderate — notably less extended than BLUR (38-41%) or VANRY (45%). This is the key differentiator.

**Entry triggers**: 0.0445–0.0451 pullback with 15m structure holding. TP1: 0.0468, TP2: 0.0481, TP3: 0.0495. RR to TP1: ~1.84R.

**Aligned with mood?** Yes — risk-on, RWA narrative basket active, fresh OI (price up + OI up = fresh positioning), funding neutral (5e-05 = negligible crowding). Derivatives picture is the cleanest of all candidates.

**Catalyst?** No fresh verified catalyst. RWA narrative basket (heat 30.1, risk 55.0 = mixed). No catalyst means pure momentum RS-leader play — acceptable in bullish regime but not catalyst-confirmed.

**FOMC risk**: Reduce size 30–50% for new swing started today; FOMC minutes July 8 21:00 EEST.

**Conclusion**: BEST LONG-WATCH. Actionable on pullback to 0.0445–0.0451. Do not market-buy at 0.0454.

---

### Candidate 2: BLUR/USDT — LONG (RETEST WATCH ONLY)

**Status**: A-tier swing (score 81.2) — **TP ALREADY HIT this session**
**External**: InteractiveCrypto July 2026 — 41.3% surge confirmed; no specific catalyst; Binance monitoring tag (June 18); token unlock **July 14** (next week)

**Has price already reacted?** Massively — +38-41% in 24h. A-tier TP hit. New entry only on retest.

**Retest zone**: 0.0187–0.0195 (swing) / 0.0193–0.0201 (intraday). That's a ~7–8% pullback from ~0.0204 (last print in report) — likely more from current price (probably 0.021+).

**Key risks for NEW entry**:
1. **Token unlock July 14** — 7 days away — material supply headwind; limit swing to <7 days
2. **Binance monitoring tag** (June 18) — elevated platform risk
3. **No fundamental catalyst** — pure altcoin-season beta
4. **FOMC tomorrow** — swing started today carries overnight event risk
5. **Negative funding across venues** — shorts crowded (bullish near-term, but reversal is violent when it comes)
6. OI +206% in swing data — potentially crowded setup

**What makes it actionable (new entry)?** Pullback to 0.0187–0.0195; confirm absorption (volume drying on pullback not spiking); BTC regime intact; plan for exit before July 14. If these conditions met, a short-duration intraday or early-swing entry could work.

**LEGAL/HEADLINE RISK**: BLUR itself has no active legal flags. Binance monitoring tag is a platform risk, not a securities law issue.

**Conclusion**: CATALYST-WATCH (retest trigger only). NOT actionable at current price. Token unlock July 14 caps swing duration hard. If no retest materializes, this is a no-trade for new positions.

---

### Candidate 3: BONK/USDT — SHORT (MANUAL REVIEW REQUIRED)

**Status**: B-tier swing signal (score 68) showing "tp" status in live active-signals — however, this signal is from BEFORE the governance attack (a previously-generated LONG BONK signal that happened to TP). The governance attack creates a new independent SHORT thesis.

**External research**: CoinDesk (July 7) — confirmed $20M treasury drain. Attacker spent $4.4M to buy 1% of BONK supply, passed malicious governance proposal with 99.9% yes vote (no quorum opposition), automatically drained treasury July 6. ~$188K already sent to exchange for cash-out; $19M remains in attacker multisig. Law enforcement notified. CEXs cooperating.

**LEGAL/HEADLINE RISK**: This is a governance exploit, not a security breach. BonkDAO working with law enforcement and exchanges. Possible CEX freeze of attacker funds could cause a short squeeze if the market reads it as asset recovery.

**Has price already reacted?** BONK -8–10% already. The initial sell-off is in. Short momentum continuation requires further selling by attacker (the remaining $19M).

**Is there a short entry?** The setup is:
- Production system: squeeze_risk → CAPPED TO C (thin_liquidity_short_squeeze_risk)
- Directional bias: down — governance attack is materially bearish for trust/sentiment
- But: CEX freeze could reverse this violently; thin liquidity means even small buy pressure creates outsized upswings

**Failed bounce trigger**: Watch for BONK to bounce 3–5% from current levels (~$0.0000108 support area), then show 15m rejection with volume. Short trigger = break below post-bounce low. Stop must be above swing high. Derivatives confirmation required.

**Conclusion**: SHORT — MANUAL REVIEW REQUIRED. Do not enter on momentum. Squeeze risk is non-trivial. Best kept as a watch item with specific entry trigger and tight stop.

---

### Candidate 4: VANRY/USDT — AVOID (EXTREME EXTENSION)

**Status**: B-tier signals (swing 70.7, intraday 68.6, scalp 78 wait); signals showing "tp" in live CLI

**Extension metrics**: +45.43% in 24h, +175.62% in 7d. This is among the most extreme moves in the tracked universe for this session.

**Is there a catalyst?** None identified. The swing report explicitly placed VANRY in `momentum_breakout` basket with playbook `wait_pullback` — meaning even the system recommends NOT entering immediately.

**Derivatives**: Funding negative Bybit(-0.00143), MEXC(-0.00112) — shorts crowded. Volume below average (0.53–0.73x). A massive move on thin volume with no catalyst is a classic pump profile.

**Long side**: Extreme chase risk. The momentum_breakout / wait_pullback basket explicitly says to wait. Entry zone for swing was 0.0076–0.0080 when report was generated; price may now be above this zone. Even if zone was intact, entering a +175% 7d asset with no catalyst after it already TP'd is high-risk.

**Short side**: Squeeze risk active. Shorts are crowded (negative funding). Thin liquidity. Fighting the bullish tape. Production system caps any VANRY short to C.

**Token risk**: Binance monitoring tag from prior session (noted in 04:40 review). This adds platform risk to any VANRY position.

**Conclusion**: AVOID both long (chase) and short (squeeze). Best kept off desk until: (a) 2+ day consolidation, (b) 20–30% pullback from highs, (c) volume-confirmed retest. Do not re-evaluate this for at least 48 hours.

---

### Candidate 5: XRP/USDT — CATALYST WATCH WITH CAUTION (No Fresh Entry)

**Status**: No active A/B XRP signals this cycle. Previous catalyst-backed idea from 04:40 review.

**External**: Multiple sources (July 6–7) — Ripple confirmed CSSF Luxembourg CASP license; full MiCA compliance across 30 EEA countries. XRP price reaction: **-3% to ~$1.05**. CaptainAltcoin: "The 'Ripple MiCA Approval' Hype Is a Myth, XRP Price Doesn't React."

**Why the muted/negative reaction**: MiCA license is company-level (Ripple Labs services), not token-level. XRP the asset did not get "approved" — Ripple got permission to offer payment services. No automatic demand increase for XRP from the license alone.

**From scalp report**: XRP catalyst note — "XRP stalls near $1.14 as breakout attempt struggles for volume" — this was the pre-announcement level. Post-announcement at ~$1.05, the trade has reversed.

**Is there a fresh entry here?** No. The catalyst has been absorbed negatively. Any new XRP long now is betting on a reversal of the sell-the-news pattern.

**What level makes it actionable?** XRP reclaims $1.14–$1.16 with volume on 1h timeframe, holding for 2+ candles = potential breakout retry. This is NOT happening currently.

**Conclusion**: DOWNGRADED from catalyst-watch to no-trade this window. Monitor for potential recovery setup above $1.14 in coming days.

---

## 8. Best Candidates Ranked

| Rank | Symbol | Side | Lifecycle | Trigger | Confidence |
|---|---|---|---|---|---|
| 1 | **PYTH/USDT** | Long-watch | WAITING FOR ENTRY | Pullback into 0.0445–0.0451; 15m structure hold; reduce size 30-50% for FOMC | Medium |
| 2 | **BLUR/USDT** | Long-watch (retest) | TP HIT (prior signal) | Pullback to 0.0187–0.0195; absorption confirmed; limit swing <7d (before July 14 unlock) | Medium-Low |
| 3 | **BTC/USDT** | Long-watch | WAITING FOR ENTRY | B-tier swing at ~63K; cleanest macro proxy; 50% size for FOMC tomorrow | Medium |
| 4 | **BONK/USDT** | Short-watch (manual review) | NO-ENTRY (squeeze risk) | Failed bounce + derivatives confirm; manual review required; do not chase | Low |
| 5 | **AAPL/TSLA/XLF/XLV** | Long-planning | PLANNING ONLY (US closed) | Wait for RTH open 16:30 EEST; confirm no gap-fade; 15–30 min after open | Low (pre-open) |

No clean candidates for immediate execution. Best long-watch (PYTH) requires pullback. Best short-watch (BONK) requires manual review. All stocks require RTH open. This is a watchlist / wait-for-trigger window — scanning and tracking continue as normal.

---

## 9. Avoid / No Trade (This Decision Window Only)

Not actionable in this 11:30 window:

- **VANRY/USDT**: +175% 7d, extreme extension, no catalyst, squeeze risk — AVOID both sides
- **XRP/USDT**: Catalyst backfired (-3%); no fresh thesis — avoid new long until $1.14 reclaim
- **SOL/USDT**: Bonk treasury governance attack on SOL ecosystem — operator-review warning; no SOL A/B signal; avoid aggressive SOL-ecosystem bets
- **ETH/USDT**: UXLINK hacker concern (operator-review) — carry existing signals only; no new ETH intraday entry
- **OPG/USDT**: +20.5% 24h, funding extreme negative (Bybit -0.009, OKX -0.009) — extreme short crowding + scalp kill-switch = do not enter any direction
- **Stock intraday A/B before 16:30 EEST**: Market closed; all demoted to C
- **MSFT, UNH, SMCI**: Legal/headline risk flags — AVOID on any new stock entry
- **All scalp ideas**: Kill-switch active; no scalp entries

This "no clean trade" is specific to this window only. The system continues scanning and tracking. Multiple signals remain OPEN ACTIONABLE and signals are hitting TP levels across the board. The regime is bullish. Patience and pullback discipline is the correct posture.

---

## 10. Main Risks

| Risk | Severity | Timing | Action |
|---|---|---|---|
| **FOMC minutes (July 8, 21:00 EEST)** | High | Tomorrow | Reduce all new swing sizes 30–50%; prefer short-duration setups |
| **BLUR token unlock (July 14)** | Medium | 7 days | Limit BLUR swing to <7d; plan exit before unlock |
| **BONK governance attack continuation** | Medium | Active | Attacker begun cashing out; CEX freeze tail-risk; monitor BONK/SOL |
| **SOL ecosystem reputation risk** | Medium | Active | Operator-review; World Cup meme volatility + Bonk attack = complex SOL tape |
| **BTC funding at 9%** | Medium | Active | Elevated long crowding; de-leveraging risk on sentiment shift |
| **ETH UXLINK hacker** | Medium-Low | Active | 14,336 ETH in motion; no direct trading impact confirmed yet |
| **Altcoin extension risk** | Medium-Low | Active | Multiple 30–45% 24h moves — late entrants vulnerable to mean reversion |
| **VANRY Binance monitoring tag** | Low | Active | No active signal, but monitor if next cycle generates VANRY proposal |
| **Stocks A/B poor performance** | Low | Ongoing | 0% WR 7d (weak n=28); extra RTH confirmation required before stock entry |
| **11 dead news sources** | Low | Ongoing | SEC EDGAR, Business Wire, Telegram channels DEAD; coverage gaps persist |

---

## 11. Action Plan — Next 4 Hours (11:39 → ~15:39 EEST)

1. **PYTH/USDT** — Alert on pullback into 0.0445–0.0451. If zone entered: check 15m structure, volume absorption (not distribution). Size: 30–50% of normal for FOMC. SL: 1h close below 0.0438. TPs: 0.0468 / 0.0481 / 0.0495.

2. **BLUR/USDT** — Watch for pullback toward 0.0187–0.0195 zone. No action at current price. If retest: check volume on pullback (drying = absorption; spiking = distribution). Limit swing to <7 days. Size: reduced for FOMC + token unlock.

3. **BTC/USDT** — B-tier swing WAITING at ~63K entry zone. If BTC consolidates and holds at local support, this is the cleanest macro proxy for the US session. Size: 40–50% for FOMC.

4. **Stocks watchlist prep (for 16:30 EEST RTH open)**:
   - Watch: AAPL (90), TSLA (89), XLV (88), XLF (86), XLY (83), GOOGL (82), JPM (82), AMD (82)
   - Wait 15–30 min after open for gap direction and volume confirmation
   - AVOID: UNH (DOJ fraud probe), MSFT (securities fraud), SMCI (export-control lawsuit)
   - Do not chase pre-market gap-ups without RTH confirmation

5. **BONK** — Watch for failed-bounce setup (~+3–5% bounce then rejection on 15m). If forming, conduct manual review before considering short. Do not short on momentum.

6. **Do NOT**: Chase VANRY, short OPG (extreme negative funding + scalp kill-switch), open stock intraday before 16:30 EEST, open scalps (kill-switch active).

---

## 12. Final Verdict per Mode

| Mode | Verdict | Notes |
|---|---|---|
| Crypto scalp | **DISABLED** | Kill-switch active; do not override |
| Crypto intraday | **WATCH / wait-for-trigger** | Prefer pullback entries; no catalyst-confirmed setups; intraday no-catalyst 14d PF=0.70 applies |
| Crypto swing | **CAUTION** | Longs on pullbacks preferred; FOMC tomorrow limits new sizing; PYTH (cleanest), BLUR (retest only), BTC (macro proxy); reduce size 30–50% |
| Stocks intraday | **PLANNING ONLY** | US closed until 16:30 EEST; wait for RTH + 15–30m confirmation; avoid legal-risk names |
| Stocks swing | **EXCLUDED** | Stocks swing 5d stale; A/B 7d 0% WR |
| Stocks invest | **EXCLUDED** | Stocks invest 5d stale |

---

## 13. Sources

- [BLUR Rockets 41% in 24 Hours Amid Altcoin Season Surge, But Uncertainty Looms](https://www.interactivecrypto.com/blur-rockets-41-in-24-hours-amid-altcoin-season-surge-but-uncertainty-looms-jul-2026) — InteractiveCrypto, July 2026. Confirms: no specific catalyst, Binance monitoring tag June 18, token unlock July 14. Verification: single_source. Confirms / Weakens BLUR swing thesis.

- [BONK Faces $20M Treasury Drain After Attacker Spends $4M to Pass Malicious Proposal](https://www.coindesk.com/markets/2026/07/07/bonk-faces-usd20-million-treasury-drain-after-attacker-spends-usd4-million-to-pass-malicious-proposal) — CoinDesk, July 7 2026. Primary detailed account of governance attack. Verification: primary_source. Confirms BONK short thesis.

- [BONK DAO Loses $20 Million in Governance Attack, Token Falls 10%](https://finance.yahoo.com/markets/crypto/articles/bonk-dao-loses-20-million-180738851.html) — Yahoo Finance, July 7 2026. Price impact -10% confirmed. Verification: single_source. Confirms BONK short thesis.

- [Will XRP Price Recover After Ripple's MiCA License?](https://www.cryptotimes.io/2026/07/06/will-xrp-price-recover-after-ripples-mica-license-on-chain-data-signals-hope/) — CryptoTimes, July 6 2026. XRP price context post-MiCA. Verification: single_source. Weakens XRP long thesis.

- [The 'Ripple MiCA Approval' Hype Is a Myth, XRP Price Doesn't React](https://captainaltcoin.com/the-ripple-mica-approval-hype-is-a-myth-xrp-price-doesnt-react/) — CaptainAltcoin, July 2026. XRP dropped 3% on announcement. Verification: single_source. Weakens XRP long thesis.

- [Ripple Wins MiCA License, Unlocks Crypto Services Across 30 EEA Markets](https://www.banklesstimes.com/articles/2026/07/06/ripple-secures-luxembourg-casp-license-achieves-full-mica-compliance-across-eea/) — BanklessTimes, July 6 2026. MiCA CSSF license detail. Verification: primary_source. Provides context.

- [FOMC Minutes, SpaceX Joins Nasdaq 100: Crypto Week Ahead](https://www.coindesk.com/markets/2026/07/06/fomc-minutes-spacex-joins-nasdaq-100-crypto-week-ahead) — CoinDesk, July 6 2026. Confirms FOMC minutes July 8 14:00 ET. Verification: primary_source. Confirms FOMC risk timing.

- [Bitcoin Gets Bullish Signals from Inflation Breakevens](https://www.coindesk.com/daybook-us/2026/07/06/u-s-inflation-outlook-underpins-bitcoin-bulls-after-best-week-since-march) — CoinDesk, July 6 2026. US 2yr breakeven <2% — dovish Fed context. Verification: single_source.

- Internal: `data/reports/scalp/2026-07-07_06-38_scalp_report.md`, `data/reports/intraday/2026-07-07_06-44_intraday_report.md`, `data/reports/swing/2026-07-07_02-03_swing_report.md`, `data/reports/stocks/intraday/2026-07-07_06-51_stocks_intraday_report.md`, `data/scheduled_runs/2026-07-07_default_schedule/cycle_03_09-31_summary.md`

---

## 14. Fix Requests / TODO

### TODO-blur-token-unlock-risk-layer
- **issue:** Token unlock on July 14 for BLUR is not captured in the production risk-warnings layer or signal scoring. The A-tier BLUR swing signal was generated and acted-upon (TP hit) without any unlock warning in the signal metadata.
- **evidence:** External research (InteractiveCrypto July 2026): "a token unlock scheduled next week" (July 14). Internal reports: no unlock_risk flag for BLUR in news_items or production warnings. APT unlock IS captured (BeInCrypto source), so the mechanism exists — BLUR is missing.
- **suggested manual fix:** Manual session: verify if a token unlock calendar source exists that covers BLUR. If BeInCrypto is configured, check BLUR coverage. If not, manually flag BLUR in token unlock watchlist. Consider adding a pre-unlock risk warning 7–10 days before major unlocks for all tracked assets.
- **priority:** medium
- **first observed:** 2026-07-07 11:39 EEST

### TODO-telegram-notifier-paper-shadow-config-path
- **issue:** Paper-shadow A/B Telegram digest failing with `TelegramNotifier.__init__() missing 1 required positional argument: 'config_path'` — daily paper-shadow digest not being sent.
- **evidence:** `data/scheduled_runs/2026-07-07_default_schedule/cycle_03_09-31_summary.md` step 14: "send error: TelegramNotifier.__init__() missing 1 required positional argument: 'config_path'"
- **suggested manual fix:** Manual session: find the paper-shadow digest script's TelegramNotifier call; add `config_path` argument or update the constructor to use a default path from config.
- **priority:** medium
- **first observed:** 2026-07-07 11:39 EEST

### TODO-dead-news-sources-audit
- **issue:** 11 configured news sources are DEAD (enabled but not writing) per stocks intraday report. Includes SEC EDGAR, Business Wire (Stocks), and multiple Telegram announcement channels (Binance, Bybit, OKX, coin_listing). Ongoing coverage gap.
- **evidence:** `data/reports/stocks/intraday/2026-07-07_06-51_stocks_intraday_report.md`: "SOURCE HEALTH: DEAD primary news sources: Business Wire (Stocks), t.me/binance_announcements, t.me/Bybit_Announcements, t.me/coin_listing, t.me/OKXAnnouncements, SEC EDGAR" and "11 configured sources are DEAD."
- **suggested manual fix:** Manual session: audit each dead source. Check for API key expiry, endpoint changes, or intentional disabling. Prioritize SEC EDGAR (high-value legal/regulatory) and Business Wire (Stocks) for repair. Confirm Telegram channels are still active on the respective platforms.
- **priority:** medium
- **first observed:** 2026-07-07 11:39 EEST (likely ongoing from prior sessions)
