# Opus Enriched Review — Late-Session Risk Review — Auto Cycle 21:39 EEST

> **Advisory only / no auto-trade. Thursday July 2, 2026. Slot: Late-Session Risk Review (21:30 EEST). Crypto: LIVE. Stocks: US RTH ~1.5h remaining (~14:39 ET).**

---

## 1. Executive Summary

**Slot: Late-Session Risk Review — advisory only / no auto-trade.**

Late US afternoon (~14:39 ET, ~1.5h before close). BTC holding **~$60,128** (range today $57,891–$60,377) — recovered fully from the NFP-miss dip. Crypto regime remains **bullish trend (risk-on)**; altcoin breadth 81.4% above EMA20. SYN has reached **A-tier scalp at TP** — the only A-tier crypto signal active today. Two crypto swing **shorts** (BTC/ETH direction) also at TP.

Stocks: **healthcare and financials continue to lead** (XLV +11.95% RS, XLF +10.44% RS vs SPY). TSLA buy-rumor-sell-news fully confirmed (B-short triggered, stock −8.8% from intraday peak of ~$438 → ~$399). **CRITICAL: UNH C-tier long is TRIGGERED** despite active DOJ multi-front criminal probe — must NOT be treated as actionable; LEGAL RISK / AVOID.

**Late-session posture:**
- **DO NOT add** new intraday crypto positions — too late in session for scalp/intraday; existing triggered signals only.
- **Hold** LLY A-tier long (catalyst fresh); manage TSLA B-short toward TP or tighten above $410.
- **Avoid** TLM new entries (overcrowded, −0.97% funding, +85.6% 24h, Binance delisting watch).
- **Avoid UNH** in all modes — DOJ criminal probe multi-front active; legal risk overrides C-signal.

Stocks A/B playbook remains structurally weak: **PF=0.24, WR=3%, −5.3R weekly.** Require confirmed catalyst + regime alignment before acting on any stocks A/B idea.

---

## 2. Data Used

| Source | File / CLI | Age at 21:39 EEST | Status |
|--------|-----------|-------------------|--------|
| Scheduler cycle_08 | `cycle_08_20-29_summary.md` | 46 min | **FRESH** |
| Crypto scalp | `2026-07-02_17-37_scalp_report.md` | 62 min | **FRESH** |
| Crypto intraday | `2026-07-02_17-43_intraday_report.md` | 56 min | **FRESH** |
| Crypto swing | `2026-07-02_13-01_swing_report.md` | 5h38m | CARRY-FORWARD |
| Stocks intraday | `2026-07-02_18-30_stocks_intraday_report.md` | 9 min | **VERY FRESH** |
| Stocks swing | `2026-07-02_13-03_stocks_swing_report.md` | 5h36m | CARRY-FORWARD |
| Stocks invest | `2026-07-02_13-05_stocks_invest_report.md` | 5h34m | CARRY-FORWARD |
| Active signals crypto | CLI (live) | fresh | **30 signals** (1 A-tier SYN at TP) |
| Active signals stocks | CLI (live) | fresh | **50 signals** (3 A-tier; UNH C triggered) |
| Signal-stats crypto | CLI (live) | fresh | n=105, PF=1.795, +15.9R |
| Signal-stats stocks | cycle_08 step 26 | 46 min | A/B n=36, PF=0.24, −5.3R |
| Untracked legacy | CLI (live) | fresh | **1: ME/USDT B intraday** |
| Market dashboard | cycle_08 step 15 | 46 min | crypto=trend, stocks=risk_on, VIX=16.74 |
| Paper monitor | cycle_08 step 30 | 46 min | 23 open, 1 waiting, 34 entered-unresolved |
| BTC price | WebSearch (fortune.com, cryptonews.net) | live | ~$60,128 (high $60,377 / low $57,891) |
| TSLA session | WebSearch (cnbc.com, techtimes.com) | live | 480k deliveries; stock −8.8% from peak ~$438→$399 |
| Previous review | `OPUS_ENRICHED_REVIEW_AUTO_2026-07-02_1839.md` | ~3h ago | Loaded |

> **External web research: Operational — 3 WebSearch queries executed.**
> Swing/invest reports are carry-forward (5h+ old) — use for trend context only.

---

## 3. Scheduler / Data Freshness

- **Cycle 08:** Started 20:29 EEST, finished 20:54 EEST — **32/32 OK, 0 failed**.
- **Freshness:** 46 min — **PASSES 3-hour defer threshold. NOT DEFERRED.**
- **Pre-tracking pass:** 559 checked, 17 updated, 333 TP hits, 5 stopped, 0 expired.
- **Post-tracking pass:** 561 checked, 9 updated, 334 TP hits, 1 stopped, 0 expired.
- **Revalidation:** 3 stale + 3 moved-away (pre); 6 stale + 4 moved-away (post).
- **Paper portfolio (bybit_non_vip, active):** $523.49 net / +10.47% / W=185 L=499 / fee-drag $1,561.
- **Paper shadow B (forward 7d):** B +44.52R vs A −99.81R. NOT READY (4/6 gates). DATA_GAP_LATE 49% of forward.
- **Monitor:** Crypto (pid 4016) + Stocks (pid 22120) running — stocks monitor generated new report at 21:30 EEST.
- **Untracked legacy:** **1 — ME/USDT B intraday (17:26 UTC). No signal_id. Will NOT count toward PF/winrate.**

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-07-02 21:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "onchain_config_missing", "derivatives_sparse"],
      "data_missing": ["onchain_config", "derivatives_numeric_oi_history"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "cycle_08 completed 20:54 EEST, 32/32 OK — 46 min ago",
        "scalp 62 min, intraday 56 min, stocks/intraday 9 min old",
        "catalyst_events=806, baskets=5 (label refresh at 20:43)",
        "intelligence layer: derivatives numeric history sparse (price metrics primary)",
        "onchain: interface_ready_config_missing",
        "1 untracked legacy alert: ME/USDT B intraday"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.78,
      "reason_codes": ["risk_on", "longs_preferred", "mixed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "crypto: BTC transition_up, ETH uptrend, altcoin breadth 81.4% above EMA20, 76.7% above EMA50",
        "stocks: VIX 16.82, SPY uptrend +1.14% 5d, QQQ range -0.71% 5d",
        "sector: XLV +11.95% RS, XLF +10.44% RS vs SPY (STRONG); XLK -6.71%, SMH -6.12% (WEAK)",
        "F&G = 19 (extreme fear despite price recovery)",
        "market_dashboard: crypto_mode=trend, stocks_mode=risk_on"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "ok",
      "confidence": 0.72,
      "reason_codes": ["fresh_catalyst", "catalyst_confirmed", "mapping_weak", "narrative_supported"],
      "data_missing": ["catalyst_mapped_count_precise"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "NFP June 2026: +57k vs +110k expected — major dovish miss, Fed hike odds collapsed",
        "LLY: GLP-1 Medicare Bridge $50/mo July 1 launch + Leerink upgrade $1,232 — confirmed fresh",
        "TSLA: Q2 deliveries 480k vs 406k (strong beat); buy-rumor-sell-news, -8.8% from peak",
        "BTC ETF: 1D -$379M, 7D -$2.02B net outflows — sustained macro headwind",
        "ETH ETF: today +$36.6M inflow (positive divergence)",
        "SOL: token unlock July pressure (AMBCrypto)",
        "UNH: DOJ criminal probe multi-front active (carried forward)",
        "806 catalyst events; many unmapped basket events (legal/exploit)"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "oi_supports", "funding_extreme", "data_unavailable"],
      "data_missing": ["oi_numeric_history", "liquidation_data", "stocks_derivatives"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "TLM: +85.6% 24h, OI +200.36%, bybit funding -0.97% / mexc -0.48% — elevated crowding",
        "BREV: negative funding 3 venues (bybit -0.42%, okx -0.11%, mexc -0.55%)",
        "ME: negative funding 3 venues, OI +33.15%",
        "squeeze_phase: 3 expansion, 35 post_unwind_chop, 21 build_up, 46 unknown",
        "2 crypto B swing shorts at TP (BTC/ETH direction)"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["entry_late", "chase_risk", "open_actionable", "stale_before_entry"],
      "data_missing": ["live_chart_data"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "TLM 0.0018 up +85.6% — extreme overextension; do not enter",
        "SOL: stale_intraday 14.26h held, WAITING, regime_changed=True — revalidate required",
        "TSLA: ~$399 range; B short triggered and working; watch $410 resistance",
        "SYN A scalp at TP — manage only, do not add",
        "Most crypto scalp/intraday: triggered or tp_hit — late session, no new entries",
        "JPM A: changed from triggered to waiting (price retrace)",
        "BTC ATR at 86th percentile (elevated vol)"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.80,
      "reason_codes": ["open_actionable", "entered_unresolved", "review_shadow", "no_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "paper monitor: 23 OPEN ACTIONABLE, 1 WAITING FOR ENTRY, 34 ENTERED UNRESOLVED, 192 REVIEW/SHADOW, 64 NO-ENTRY/STALE/MOVED-AWAY",
        "live crypto: 30 signals — 1 A-tier SYN at TP; 2 B swing shorts at TP; majority long",
        "live stocks: 50 signals — AAPL A triggered, LLY A triggered, JPM A waiting",
        "UNH C intraday TRIGGERED + swing TRIGGERED — LEGAL RISK, not paper-actionable",
        "34 entered-unresolved: 0R display / unresolved, no TP/SL before window — NOT missed entries"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["repeated_losses", "legal_risk", "reduce_risk", "headline_risk", "correlation_cluster"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "stocks A/B: PF=0.24, WR=3%, totalR=-5.3R — structurally losing, repeated losses",
        "UNH: DOJ criminal probe multi-front — AVOID all modes",
        "TSLA: late session EOD short-cover squeeze risk",
        "BTC ETF 7d net -$2.02B: macro headwind",
        "SOL token unlock July pressure",
        "TLM: crowded, negative funding, Binance delisting monitoring",
        "Correlation cluster: LLY/XLV/XLF/JPM all in same healthcare/financials rotation"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.70,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample", "fresh_expired_problem"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "crypto A/B: n=105, PF=1.795, avgR=+0.21, totalR=+15.9R — WORKING",
        "stocks A/B: n=36, PF=0.24, avgR=-0.18, totalR=-5.3R — FAILING",
        "stocks B: WR=4%, PF=0.28 — below minimum threshold",
        "stocks A: n=6 anecdotal — too small",
        "no-catalyst crypto intraday: WR 23%, PF 0.70, -3R — avoid",
        "paper shadow B forward: +44.52R vs A -99.81R (7d); promotion NOT READY"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "normal",
      "confidence": 0.72,
      "reason_codes": ["longs_preferred", "shorts_preferred", "catalyst_backed", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "crypto risk-on: hold existing RS-leader longs to TP; no new intraday late session",
        "stocks bifurcated: LLY/JPM hold; TSLA short active; avoid UNH/tech",
        "UNH triggered C signals: operator must override — legal risk",
        "do not add TLM: crowded, -0.97% funding, +85.6% — extreme chase"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "normal",
    "confidence": 0.72,
    "preferred_side": "mixed",
    "best_long_candidate": {
      "symbol": "LLY",
      "trigger": "Hold if triggered (zone 1203-1211); retest zone if not entered; GLP-1 catalyst confirmed",
      "reason": "Healthcare #1 sector RS leader; multi-catalyst fresh (GLP-1 + Leerink upgrade); A-tier triggered; ~1.5h to US close"
    },
    "best_short_candidate": {
      "symbol": "TSLA",
      "trigger": "B short triggered; hold below $410 resistance; tighten/close if EOD bounce above $410",
      "reason": "Buy-rumor-sell-news confirmed (480k deliveries, -8.8% from peak $438 to $399); B-short in play"
    },
    "best_catalyst_candidate": {
      "symbol": "LLY",
      "trigger": "GLP-1 Medicare Bridge $50/mo July 1 confirmed + Leerink $1,232; hold through close",
      "reason": "Freshest confirmed catalyst of the session; healthcare outperforming all sectors"
    },
    "avoid_candidate": {
      "symbol": "UNH",
      "reason": "DOJ criminal probe multi-front active (Medicare Advantage + Optum Rx + physician); C-tier TRIGGERED but LEGAL RISK overrides — AVOID all modes"
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
|-------|---------|-----------|-------------|-----------------|
| data_quality | **ok** | 0.85 | scheduler_fresh, onchain_config_missing, derivatives_sparse | advisory_only |
| market_regime | **ok** | 0.78 | risk_on, longs_preferred, mixed | advisory_only |
| catalyst_narrative | **ok** | 0.72 | fresh_catalyst, catalyst_confirmed, mapping_weak | advisory_only |
| derivatives_squeeze | **caution** | 0.55 | squeeze_risk, oi_supports, funding_extreme, data_unavailable | advisory_only |
| technical_entry | **caution** | 0.65 | entry_late, chase_risk, open_actionable, stale_before_entry | advisory_only |
| execution_lifecycle | **ok** | 0.80 | open_actionable, entered_unresolved, review_shadow, no_entry | advisory_only |
| risk_manager | **caution** | 0.75 | repeated_losses, legal_risk, reduce_risk, headline_risk | advisory_only |
| playbook_performance | **caution** | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | **normal** | 0.72 | longs_preferred, shorts_preferred, catalyst_backed, reduce_risk | advisory_only |

---

## 4. What Changed vs Previous Review

Previous: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-02_1839.md` — US open reaction review ~3h ago.

| Item | Before (18:39) | Now (21:39) | Change |
|------|---------------|-------------|--------|
| BTC price | ~$60,117 | ~$60,128 | Flat — consolidating |
| Crypto signals | 20 active | **30 active** | +10: new scalp/swing triggers + 2 swing shorts |
| Stocks signals | ~20 active | **50 active** | +30: stocks monitor ran at 21:30 |
| SYN A scalp | At TP | At TP (still) | Holding |
| TSLA B short | WAITING → bearish confirmed | **TRIGGERED, working** | In play |
| LLY A-tier | TRIGGERED | **TRIGGERED** | Continuing; catalyst fresh |
| JPM A-tier | TRIGGERED | **WAITING** | Price retrace — B still triggered |
| AAPL A-tier | TRIGGERED | **TRIGGERED** | Active; tech sector still weak |
| UNH C intraday | Flagged legal risk | **TRIGGERED** (C) | Escalation — legal risk + triggered |
| UNH C swing | — | **TRIGGERED** | Same legal risk |
| Crypto swing shorts | Not visible | **2 at TP** | BTC/ETH direction hedge working |
| Untracked legacy | NONE (clean) | **1 (ME/USDT)** | New gap |
| Stocks A/B PF | 0.21, −6.3R | 0.24, −5.3R | Slight recovery (+1R) |
| Crypto PF | 1.97, +19.4R | 1.795, +15.9R | Slight dip (some losses closed) |

---

## 5. Catalyst Coverage

- **Total catalyst events today:** 806 (after label refresh at 20:43 EEST)
- **Baskets active:** 5 (ai_narrative, delisting_thin_liquidity, rwa_narrative, binance_ecosystem_teaser, perps_dex_narrative)
- **Explicitly symbol-mapped:** BTC, ETH, SOL, XRP, LINK, ASTER, ONDO (7 crypto); LLY, TSLA, AAPL, MSFT, NVDA, JPM (stocks via news)
- **Catalyst mapping estimate: >50% unmapped (basket-level events dominate). Use catalyst layer as context, not final filter.**

Top unmapped/basket headlines:
1. `[legal_risk]` DOJ Charges 19-Year-Old Tied to $100M Scattered Spider Crew (BeInCrypto) — basket
2. `[exploit_hack]` Taiko bridge $1.7M exploit, now restored (Cointelegraph/CoinDesk) — basket
3. `[exploit_hack]` Tokenized Google stock inflated 7,700% in rare DeFi lending exploit (CoinDesk) — basket

Catalyst label refresh: 1 news flip (ENA: news_supported 0→1) + 3 telegram flips.

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** risk-on / bullish trend
- **Stocks mood:** risk-on but bifurcated (healthcare/financials = risk-on; tech/semis = risk-off)
- **Dominant narrative:** Healthcare rotation post-NFP miss; crypto recovering from $57.9k dip
- **Preferred side now:** Longs (healthcare/financials); short TSLA (active); crypto RS-leader swing longs
- **Best long candidate:** LLY — trigger: hold at 1203–1211 zone; catalyst confirmed
- **Best short candidate:** TSLA — trigger: hold below $410; tighten above $410
- **Best catalyst-backed candidate:** LLY (GLP-1 Medicare Bridge, Leerink upgrade, fresh)
- **What to avoid:** UNH (legal), TLM new entry (chase/crowded), AAPL (tech weak), no-catalyst crypto intraday
- **What would change the view:** TSLA above $415 (short invalidated); BTC below $58k (crypto sentiment flip); ETF outflows widening into $3B+ weekly

---

## 7. Candidate Deep Dives

### Candidate 1 — SYN / A-tier scalp — OPEN AT TP

**Status:** OPEN actionable · Crypto A-tier scalp · tp_hit · Only A-tier crypto signal today

SYN scalp was A-tier from the previous (US open) review. Now still showing `tp_hit` status — the A-tier position has reached its target. Perps DEX narrative (`perps_dex_narrative` basket, `wait_pullback` playbook) is active for HYPE/SYN.

- Late-session: **manage at TP. Partial take-profit; move stop to breakeven. Do NOT add.**
- Derivatives: funding not explicitly available for SYN; general perps narrative basket active.
- Chart: no live chart MCP; use ATR fields from intraday report only.
- **Decision: OPEN AT TP. Manage. No new entry.**

---

### Candidate 2 — LLY / A-tier intraday long — TRIGGERED (stocks)

**Status:** OPEN actionable · Stocks A-tier · TRIGGERED · No earnings risk

**Evidence:** GLP-1 Medicare Bridge $50/mo launch (July 1) + Leerink upgrade to $1,232. Healthcare XLV: strongest sector vs SPY (+11.95% RS 20d). LLY RS vs SPY 20d: +13.80%. Score: 82.

**Late-session management:**
- Entry zone: $1,203.99–$1,211.18. TP1: $1,232.77. Invalidation: close < $1,189.60.
- ~1.5h from US close. Healthcare defensives hold well into close on rotation days.
- Catalyst still fresh. No legal/headline risk.
- **Aligned with regime** (risk-on → defensives rotation post-NFP miss).
- **Decision: HOLD if triggered. If WAITING: retest entry zone only — no chase above $1,215.**

**Chase check:** Do not market-buy at extended price. Only retest entry zone.

---

### Candidate 3 — TSLA / B-tier intraday short — TRIGGERED (stocks)

**Status:** OPEN actionable · Stocks B-tier short · TRIGGERED

**Evidence:** Q2 deliveries 480k (vs 406k expected — 18% beat). Stock traded $394.25–$437.96 range, price ~$399 late session (−8.8% from peak). Classic buy-the-rumor-sell-the-news confirmed. Truist raised PT to $430 but kept HOLD.

**Late-session risk assessment:**
- Short in play at ~$394–$400.
- **End-of-day short-cover risk:** Closing shorts before 16:00 ET close is common, especially after a large move. Watch for reversal bounce toward $410 in the final hour.
- $410 resistance = key level. If price bounces above $410 cleanly: tighten stops or close.
- Below $394: consider partial take-profit.
- **Do NOT add new short at this stage** — too late; only manage existing.
- **Decision: HOLD. Watch $410. Tighten or close if EOD bounce above $410.**

---

### Candidate 4 — UNH / C-tier — TRIGGERED ⚠️ LEGAL RISK / AVOID

**Status:** C-tier intraday long TRIGGERED + C-tier swing long TRIGGERED · **LEGAL RISK / AVOID ALL MODES**

DOJ criminal probe multi-front active (Medicare Advantage + Optum Rx + physician). Source: fiercehealthcare.com (2026-07-02, confirmed in prior reviews). This is an active **criminal** investigation — not civil, not resolved.

C-tier signals are watchlist/research only (not Telegram-actionable), but paper tracking may have entered UNH longs. Operator must NOT act on any UNH signal. Mark all UNH paper entries as excluded.

**LEGAL/HEADLINE RISK:** AVOID all modes. C-tier triggered = paper artifact only.

---

### Candidate 5 — TLM / B-tier scalp — WAITING ⚠️ CHASE RISK / DO NOT ENTER

**Status:** WAITING for entry · Crypto B-tier scalp · +85.6% 24h · EXTREME CROWDING

- OI +200.36%; funding bybit −0.97% / mexc −0.48%; volume 0.35x (thin despite massive move)
- Binance delisting monitoring active
- Current price: 0.0018; entry zone: 0.0016–0.0017 (far below current price)

Price is already far above the entry zone at 0.0016–0.0017. This is a chase setup:
- Has price already reacted? YES — +85.6% in 24h
- Is the setup chasing? YES — entry zone was 0.0016, current price 0.0018 = 12.5% above zone
- Is move overextended? YES — OI +200%, thin volume, negative funding
- Would entry NOW be late? YES — extreme late entry, not in zone
- **Decision: DO NOT ENTER. Mark as STALE-CHASE-RISK. Let expire or wait for deep pullback.**

---

## 8. Best Candidates Ranked

| Rank | Symbol | Type | Status | Rec | Trigger |
|------|--------|------|--------|-----|---------|
| 1 | LLY | Stocks A long | TRIGGERED | HOLD | Manage → TP1 $1,232; tighten if XLV breaks down |
| 2 | TSLA | Stocks B short | TRIGGERED | HOLD, tighten | Close/tighten if EOD bounce above $410 |
| 3 | SYN | Crypto A scalp | OPEN AT TP | MANAGE | Partial TP; move stop to BE |
| 4 | JPM | Stocks A long | WAITING | WATCH | Retest zone $331.85–$333.12 only; no new chase |
| 5 | COIN | Stocks B long | WAITING | WATCH | Retest $163–$165 entry; crypto bridge stock, regime aligned |

**Best long-watch:** LLY — retest $1,203–$1,211 zone; catalyst still active.
**Best short-watch:** TSLA — hold active position; new entries not recommended late session.
**Best catalyst-watch:** LLY (GLP-1 Medicare Bridge, confirmed fresh, multi-source).

---

## 9. Avoid / No Trade (this decision window only)

| Symbol | Reason |
|--------|--------|
| UNH | LEGAL RISK / AVOID — DOJ criminal probe multi-front active |
| TLM | CHASE RISK — +85.6% 24h, OI +200%, thin volume, Binance delisting watch |
| Any new crypto intraday | TOO LATE — 14:39 ET, ~1.5h to close; no new intraday entries |
| AAPL | CAUTION — A-tier triggered but tech sector weak (QQQ range, -4.42% 20d) |
| No-catalyst crypto intraday | AVOID — 14d WR=23%, PF=0.70, -3R |

Scanning, tracking, and data collection continue normally in all moods.

---

## 10. Main Risks

1. **Stocks A/B structural underperformance:** PF=0.24, WR=3%, −5.3R weekly. Every new stocks A/B entry carries elevated risk.
2. **TSLA EOD short-cover squeeze:** ~1.5h from close. Watch $410 resistance for reversal signal.
3. **TLM crowding unwind risk:** +85.6% 24h + OI +200% + thin vol + Binance delisting = sharp reversal candidate.
4. **BTC ETF 7d outflows −$2.02B:** Sustained selling is a medium-term headwind above $60k.
5. **UNH legal exposure in system:** C-tier signals keep generating despite known DOJ probe. Paper may be tracking UNH longs.
6. **Catalyst mapping weak:** >50% unmapped. Use catalyst layer as context only.
7. **Reddit social blocked (403):** All 3 Reddit sources failed. Social signal coverage degraded. KOL placeholder still in config.
8. **SOL stale_intraday:** 14.26h held WAITING, regime_changed=True. Requires revalidation.
9. **ME/USDT untracked legacy alert:** B intraday sent 17:26 UTC, no signal_id. Will NOT count toward PF/winrate.

---

## 11. Action Plan — next 4 hours

| Time (EEST) | Action |
|-------------|--------|
| 21:39–22:30 | TSLA: watch $410; tighten/close on bounce. LLY: let run toward TP1 $1,232. SYN: manage at TP. |
| ~22:30–23:00 | Pre-close crypto: BTC holding $58k+? ETH uptrend intact? If yes, swing longs overnight valid. |
| 23:00 | US close. Stocks signals expire. Crypto overnight setup review. |
| 23:15 | Post-close final daily review (sibling task). Assess all today's outcomes. |

---

## 12. Final Verdict per Mode

| Mode | Verdict | Notes |
|------|---------|-------|
| Crypto scalp | NO NEW ENTRY | SYN A at TP: manage only; TLM: do not enter |
| Crypto intraday | NO NEW ENTRY | Existing triggered signals only; SOL: stale, revalidate |
| Crypto swing | HOLD | Overnight valid for non-stale B-tier longs; avoid TLM/BREV/ME (crowded) |
| Stocks intraday | MANAGE ONLY | LLY hold, TSLA short hold, AAPL watch; JPM wait for retest |
| Stocks swing | CARRY-FORWARD | Report 5h36m old; no new swing entries from stale data |
| Stocks invest | N/A | Not implemented |

---

## 13. Sources

- [Bitcoin price today, July 2 2026 — cryptonews.net](https://cryptonews.net/news/bitcoin/33081919/)
- [Current price of Bitcoin for July 2 2026 — Fortune](https://fortune.com/article/price-of-bitcoin-07-02-2026/)
- [Bitcoin Price Prediction July 2026 — cryptotimes.io](https://www.cryptotimes.io/2026/07/02/bitcoin-price-prediction-july-2026-will-btc-go-up-or-crash/)
- [Tesla stock sinks 7% despite strong deliveries — CNBC](https://www.cnbc.com/quotes/TSLA)
- [Tesla Q2 2026 Deliveries: 406k bar — TechTimes](https://www.techtimes.com/articles/319305/20260629/tesla-q2-2026-deliveries-wall-street-sets-406024-bar-july-2-report.htm)
- [Dear Tesla Stock Fans, Mark Your Calendars for July 2 — Barchart](https://www.barchart.com/story/news/3062249/dear-tesla-stock-fans-mark-your-calendars-for-july-2)
- [BTC/ETH ETF flows July 2 — Lookonchain](https://x.com/lookonchain/status/2072322805279134208) (single_source)
- [DOJ criminal probe extends to Optum Rx — fiercehealthcare.com](https://www.fiercehealthcare.com) (single_source, 2026-07-02)
- Internal: cycle_08_20-29_summary.md, scalp/intraday/stocks-intraday reports, CLI outputs

---

## 14. Fix Requests / TODO

### TODO-UNH-LEGAL-SUPPRESSION
- **issue:** UNH C-tier intraday (x2 triggered) and swing (triggered) signals active despite 5+ consecutive reviews flagging DOJ criminal probe. System generates signals without legal risk suppression.
- **evidence:** Live stocks CLI: `UNH C intraday long TRIGGERED` + `UNH C swing long TRIGGERED` + `UNH C intraday long WAITING`. Prior reviews flagged "UNH LEGAL RISK / AVOID ALL MODES" since ≥ 18:39 EEST review.
- **suggested manual fix:** Add `legal_risk_override` field to proposed_signals or manual exclusion list in `config/risk_overrides.yaml`. Block UNH from paper entry and Telegram alerts while probe is active. Manual session required.
- **priority:** high
- **first observed:** 2026-07-02 18:39 EEST; recurring each cycle.

### TODO-ME-USDT-UNTRACKED-ALERT
- **issue:** ME/USDT B intraday alert was sent to Telegram at 17:26 UTC without a matching proposed_signal (±6h). Tracking gap: alert exists but will never contribute to PF/winrate/avgR.
- **evidence:** `scripts.detect_untracked_legacy_alerts --since 2026-07-02`: `ME/USDT | B | intraday | 69.6 | long | 2026-07-02T17:26:49+00:00 | NO (no proposed_signal)`.
- **suggested manual fix:** Check `watchlist_alerts` vs `proposed_signals` for ME/USDT timing mismatch. Likely monitor-vs-scheduler race condition. Investigate signal generation order. Manual session required.
- **priority:** medium
- **first observed:** 2026-07-02 21:39 EEST.

### TODO-REDDIT-403-SOCIAL-COVERAGE
- **issue:** All 3 Reddit social sources (r/CryptoCurrency, r/Bitcoin, r/ethereum) returning HTTP 403 consistently. Social signal coverage degraded. KOL watchlist still contains placeholder.
- **evidence:** cycle_08 scalp + intraday steps: repeated `WARNING Failed social source Reddit *: 403 Client Error: Blocked`. Multiple cycles affected.
- **suggested manual fix:** Remove Reddit sources from `config/social_sources.yaml` or migrate to Reddit API with auth. Update KOL watchlist with real accounts. Manual session required.
- **priority:** medium
- **first observed:** Recurring pre-2026-07-02.

## 1. Executive Summary

**Slot: US open reaction review — advisory only / no auto-trade.**

NFP June 2026 came in at **+57k vs +110k expected** — a major dovish miss. This was the dominant catalyst for the open: Fed hike odds collapsed, SPY initially rallied while QQQ lagged (rotation to value/defensives from tech). BTC recovered from the $57.9k low to **~$60,100** (+2.7% vs 24h). Crypto regime: **bullish trend (risk-on)**, altcoin breadth 71.4% above EMA20. Stocks regime: **risk_on** (VIX 16.44, SPY uptrend), but QQQ in range — tech under pressure.

**Key reactions this slot:**
- **TSLA**: Q2 deliveries 480k (vs 406k consensus) — massive beat — but stock **down 5–6%** (buy-rumor-sell-news). B short signal WAITING → bearish divergence now confirmed.
- **LLY A-tier**: TRIGGERED. Multi-catalyst (GLP-1 Medicare Bridge $50/mo launch July 1 + Leerink upgrade to $1,232 + 52-wk high). Healthcare (XLV) is the strongest sector vs SPY (+11.98%).
- **JPM A-tier**: TRIGGERED. Financials (#2 sector vs SPY +10.09%).
- **UNH**: DOJ criminal probe multi-front confirmed active (Medicare Advantage + Optum Rx + physician). **AVOID ALL MODES** (C-tier signal triggered but LEGAL RISK overrides).
- **Crypto**: SYN now A-tier scalp (at TP). 27 crypto signals active (all longs + 2 new B-shorts at TP).

**⚠️ Ongoing flags:**
- UNH **LEGAL RISK / AVOID ALL MODES** (5th review; criminal probe multi-front active).
- TLM B-scalp **ENTERED-UNRESOLVED** (at TP but Binance delisting monitoring active; no new TLM longs — +119% 24h chase risk).
- Catalyst mapping **~65–70% unmapped** (estimate, carried from previous review) — use catalyst layer as context only, not final filter.
- Stocks A/B performance: **PF=0.21, WR=3.1%, −6.3R weekly** — treat stocks intraday A/B with elevated caution.

**Decision now:** LLY long confirmed-actionable with catalyst; JPM long actionable with regime; TSLA short — wait for breakdown trigger below key level. Crypto: HEMI pullback watch (RS leader, no catalyst yet). Avoid UNH, avoid chasing TLM.

---

## 2. Data Used

| Source | File / CLI | Age at 18:39 EEST | Status |
|--------|-----------|-------------------|--------|
| Scheduler cycle_07 | `cycle_07_18-08_summary.md` | 10 min | **FRESH** |
| Crypto scalp | `2026-07-02_15-15_scalp_report.md` | 24 min | **FRESH** |
| Crypto intraday | `2026-07-02_15-20_intraday_report.md` | 19 min | **FRESH** |
| Crypto swing | `2026-07-02_13-01_swing_report.md` | 2h38m | **FRESH** (<4h) |
| Stocks intraday | `2026-07-02_15-29_stocks_intraday_report.md` | 10 min | **FRESH** |
| Stocks swing | `2026-07-02_13-03_stocks_swing_report.md` | 2h36m | **FRESH** (<4h) |
| Stocks invest | `2026-07-02_13-05_stocks_invest_report.md` | 2h34m | **FRESH** (<4h) |
| Active signals crypto | CLI (fresh) | 5 min | 27 signals |
| Active signals stocks | CLI (fresh) | 5 min | 50 signals |
| Signal-stats crypto | cycle 07 step 24 | 10 min | n=102, PF=1.97 +19.4R |
| Signal-stats stocks | cycle 07 step 26 | 10 min | A/B n=38, PF=0.21 −6.3R |
| Untracked legacy alerts | cycle 07 step 28 | 10 min | **NONE — clean** |
| Market dashboard | cycle 07 step 15 | 10 min | crypto=trend, stocks=risk_on, VIX=16.68 |
| Intelligence / squeeze | cycle 07 step 18 | 10 min | squeeze_phase cached 109 symbols |
| Paper monitor status | cycle 07 step 30 | 10 min | 21 open, 7 waiting, 36 entered-unresolved |
| BTC price | WebSearch (fortune.com, cryptotimes.io) | live | ~$60,117 (high $60,377 / low $57,891) |
| NFP June 2026 | WebSearch (fxstreet.com, investing.com) | live | +57k vs +110k expected — dovish MISS |
| TSLA Q2 deliveries | WebSearch (cnbc.com, techtimes.com) | live | 480k delivered, stock −5.6% to −8.8% |
| UNH DOJ probe | WebSearch (fiercehealthcare.com, Yahoo Finance) | live | Criminal probe multi-front active, no resolution |
| LLY catalyst | WebSearch (tradingview.com, investor.lilly.com) | live | GLP-1 Medicare Bridge + Leerink $1,232 target |
| Previous review | `OPUS_ENRICHED_REVIEW_AUTO_2026-07-02_1620.md` | 2h14m ago | Loaded |

**External web research: Operational — 5 searches executed, all returned usable results.**

---

## 3. Scheduler / Data Freshness

- **Cycle 07:** Started 18:08 EEST, finished 18:29 EEST — **32/32 OK, 0 failed**. Runtime 21 min.
- **Freshness:** 10 min since completion — **PASSES 3-hour defer threshold. NOT DEFERRED.**
- **Pre-tracking pass:** 561 signals checked, 41 updated, 331 TP hits, 8 stopped, 4 expired, 0 not-triggered.
- **Post-tracking pass:** 558 checked, 16 updated, 333 TP hits, 6 stopped, 0 expired.
- **Revalidation:** 2 stale + 2 moved-away flags (pre), 0 stale + 2 moved-away (post).
- **Paper portfolio (bybit_non_vip, active):** $696.12 net / +13.92% / 185W-492L / fee-drag $1,539.
- **Paper shadow:** B (forward valid, 7d): +26.79R vs A: −83.36R. NOT READY for promotion (4/6 gates).
- **Monitor:** Crypto (pid 20140) + Stocks (pid 9088) running 90-min background windows.
- **Untracked legacy alerts:** NONE. Integrity clean.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-07-02 18:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "catalyst_missing", "derivatives_sparse"],
      "data_missing": ["onchain_config_missing", "derivatives_numeric_oi_history"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "cycle_07 completed 18:29 EEST 32/32 OK",
        "all reports fresh <3h",
        "catalyst_events=643, baskets=4",
        "intelligence_layer: derivatives numeric history sparse (price metrics primary)",
        "onchain: interface_ready_config_missing"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.75,
      "reason_codes": ["mixed", "longs_preferred", "risk_on"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC transition_up, ETH transition_up",
        "altcoin breadth 71.43% above EMA20 (down from 78% at swing report 16:01)",
        "F&G=19 Extreme Fear despite $60k BTC",
        "VIX=16.44-16.68 (stable, low)",
        "SPY=up, QQQ=down (rotation to value/defensives post-NFP miss)",
        "stocks regime risk_on (3/4 indices uptrend, breadth 75%)",
        "NFP June 2026: +57k vs +110k expected — dovish miss",
        "healthcare+financials+industrials sector RS leaders vs SPY",
        "tech+energy sector laggards",
        "crypto_mode=trend, stocks_mode=risk_on per dashboard"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.70,
      "reason_codes": ["fresh_catalyst", "catalyst_confirmed", "catalyst_contradicted", "mapping_weak", "narrative_supported"],
      "data_missing": ["catalyst_mapped_count_exact"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "LLY: Medicare GLP-1 Bridge $50/mo (July 1), Leerink $1,232 target, 52wk high $1,200.55 — multi-catalyst CONFIRMED",
        "TSLA: 480k deliveries (vs 406k) = massive beat BUT stock -5.6% = CATALYST_CONTRADICTED (buy-rumor-sell-news)",
        "BTC ETF 7D net flow -32,807 BTC ($2.02B) = institutional selling overhang",
        "SOL: July token unlock pressure (AMBCrypto) = headwind for swing longs",
        "momentum_breakout basket (TLM/SYN/ZEC) fresh <1h",
        "ai_narrative basket (NEAR/RENDER/TAO/FET) fresh <6h",
        "UNH: DOJ criminal probe multi-front (Medicare Advantage + Optum Rx + physician) = AVOID",
        "catalyst mapping estimated ~65-70% unmapped (carry-forward from 16:20 review)"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "data_unavailable"],
      "data_missing": ["oi_numeric_history", "liquidation_data"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "TLM: OI +133% with price +119%, funding -0.006 Bybit -0.012 MEXC = short crowding, squeeze alert",
        "ME: negative funding all venues (Bybit -0.00053, OKX -0.00065, MEXC -0.00122) = crowded shorts",
        "BREV: OI +182% with price +39%, funding -0.0089 = crowded shorts",
        "squeeze_phase: phase_2_squeeze_expansion=4 coins, phase_1_build_up=21, phase_5_post_unwind_chop=36",
        "DYDX: OI +2.37% with price -27% = fresh shorts pressing (not yet squeeze)",
        "intelligence_layer note: numeric OI/funding history sparse, price metrics primary"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["chase_risk", "entry_fresh", "overextended", "stale_before_entry"],
      "data_missing": ["chart_not_loaded"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "TLM: +119% 24h = extreme chase risk; don't enter new long; existing signal at TP",
        "HEMI: swing entry zone 0.0048-0.0049, current ~0.0050 (marginal, barely above zone)",
        "LLY: entry zone $1,211-1,218 from stocks intraday report; A-tier triggered = in zone",
        "JPM: entry zone $332-334; A-tier triggered = open-actionable",
        "SYN: A scalp at TP = closed or entered-unresolved; no fresh entry opportunity",
        "TSLA B short: waiting = trigger not yet breached; watch $415 area breakdown",
        "TradingView / manual chart check unavailable — using local OHLCV/ATR fields only"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["open_actionable", "entered_unresolved", "waiting_for_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "paper monitor step 30: Open actionable=21, Waiting for entry=7, Entered unresolved=36, Review/Shadow=189, No-entry/stale/moved-away=58, Needs review=0",
        "Closed today: 337W / 37L / 0 flat",
        "Crypto active: 27 signals (all longs + 2 B-swing shorts at TP)",
        "Stocks active: 50 signals — LLY A triggered, JPM A triggered, AAPL A waiting, TSLA B short waiting",
        "New signals added since 16:20: SYN A scalp, JTO B swing, RIF B swing, BEAM B swing, AAVE B swing, ETH B swing short (TP), BTC B swing short (TP)"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["correlation_cluster", "legal_risk", "manual_review", "headline_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "All 27 crypto signals are LONGS = high BTC-correlation cluster risk",
        "Stocks A/B: PF=0.21, WR=3.1%, -6.3R weekly — poor recent performance, size down",
        "UNH: DOJ criminal probe multi-front active → LEGAL RISK, AVOID ALL MODES",
        "TLM: Binance delisting monitoring active + Bybit OI +133% + extreme chase (+119%)",
        "SOL: July token unlock = structural headwind for swing longs",
        "TSLA: delivery beat + stock -5-6% = headline execution risk for any longs",
        "BTC ETF 7D outflows -$2.02B = institutional selling signal",
        "Weekend signals underperform (WR 21%, n=15, signal-stats flag)",
        "BEAM B swing and AAVE B swing flagged with weekend=Y marker in active signals"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "ok",
      "confidence": 0.75,
      "reason_codes": ["playbook_working", "playbook_failing", "fresh_expired_problem"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "crypto swing: 14d WR 72% / PF 5.80 / +24R = STRONG (primary playbook)",
        "crypto intraday: 14d PF 2.76 (n=28, confidence=weak)",
        "crypto scalp: 14d 1W/7L PF 0.14 = LOW CONFIDENCE despite A-tier SYN",
        "stocks intraday playbook hint: 14d WR 55% PF 2.03 +80R — but live 7d stats: PF=0.21 WR=3.1% (regression!)",
        "stocks swing: WATCHLIST-ONLY (audit, -12R 0W/12L 48h)",
        "setup trend_continuation (n=83): PF 2.75 = STRONG",
        "setup momentum_breakout (n=6): PF 4.40 = STRONG",
        "setup reversal (n=13): PF 0.58 = FAILING",
        "B-tier crypto WR=19% (stats flag: 'low, consider reviewing entries')",
        "paper shadow B forward-valid: +26.79R vs A -83.36R (NOT READY, 4/6 gates)"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.70,
    "preferred_side": "catalyst_backed",
    "best_long_candidate": {
      "symbol": "LLY",
      "trigger": "price holding $1,211–$1,218 entry zone, SPY not reversing, no >2 ATR chase from zone",
      "reason": "A-tier triggered; RS-leader healthcare (+11.98% vs SPY); multi-catalyst (GLP-1 Medicare Bridge + analyst upgrade $1,232); earnings safe until Aug 5; regime risk_on"
    },
    "best_short_candidate": {
      "symbol": "TSLA",
      "trigger": "breakdown + hold below $415 area (approx short-signal level) with volume confirmation; failed delivery pop = bearish divergence confirmed",
      "reason": "B-tier short waiting; deliveries 480k beat 406k consensus yet stock -5.6%; buy-rumor-sell-news pattern confirmed; short signal pre-positioned"
    },
    "best_catalyst_candidate": {
      "symbol": "LLY",
      "trigger": "Same as long: $1,211 entry zone with regime alignment",
      "reason": "Medicare GLP-1 Bridge access expansion (July 1, $50/mo, 20M eligible patients), Leerink upgrade to $1,232, 52-wk high print — best multi-catalyst setup in this session"
    },
    "avoid_candidate": {
      "symbol": "UNH",
      "reason": "DOJ criminal probe multi-front (Medicare Advantage + Optum Rx + physician reimbursement); criminal + civil simultaneous; no resolution timeline; C-tier signal triggered but LEGAL RISK overrides all modes"
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
| data_quality | **ok** | 0.85 | scheduler_fresh, catalyst_missing, derivatives_sparse | advisory_only |
| market_regime | **ok** | 0.75 | mixed, longs_preferred, risk_on | advisory_only |
| catalyst_narrative | **caution** | 0.70 | fresh_catalyst, catalyst_confirmed, catalyst_contradicted, mapping_weak | advisory_only |
| derivatives_squeeze | **caution** | 0.55 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | **caution** | 0.65 | chase_risk, entry_fresh, overextended | advisory_only |
| execution_lifecycle | **ok** | 0.82 | open_actionable, entered_unresolved, waiting_for_entry | advisory_only |
| risk_manager | **caution** | 0.75 | correlation_cluster, legal_risk, manual_review, headline_risk | advisory_only |
| playbook_performance | **ok** | 0.75 | playbook_working (swing/trend_cont), playbook_failing (reversal, stocks all) | advisory_only |
| head_trader | **caution** | 0.70 | catalyst_backed preferred; LLY long; TSLA short; UNH avoid | advisory_only |

**Council consensus: CAUTION** — 3 ok / 4 caution / 2 ok (data + lifecycle). No bad/avoid verdicts from the council itself. Caution is driven by: stocks A/B poor performance, all-long correlation cluster in crypto, catalyst-vs-technical contradiction (TSLA), and mapping weakness.

---

## 4. What Changed vs Previous Review (16:20 EEST)

**Previous review:** `OPUS_ENRICHED_REVIEW_AUTO_2026-07-02_1620.md`

| Dimension | At 16:20 | Now 18:39 | Change |
|-----------|----------|-----------|--------|
| BTC price | ~$58,620–$59,400 | ~$60,117 (high $60,377) | ↑ +$1,500 (NFP dovish relief) |
| Crypto regime | bullish trend | bullish trend | → unchanged |
| Stocks regime | bullish (pre-open) | risk_on (RTH active) | ↑ confirmed open |
| VIX | 16.00 | 16.44–16.68 | → slight uptick (stable) |
| SPY | pre-open | uptrend confirmed | ✓ open bullish |
| QQQ | pre-open | range (tech weak) | ⚠ QQQ lagging |
| F&G | 19 | 19 | → unchanged |
| Active crypto signals | 20 B-tier | 27 (A-tier SYN added + 6 new) | ↑ +7 signals |
| Stocks A-tier | 0 | 2 (LLY A + JPM A triggered) | ↑ new A-tier triggered |
| NFP | PENDING (decision key) | +57k vs +110k (dovish MISS) | ✓ resolved |
| TSLA deliveries | PENDING | 480k (beat) but stock −5.6% | ✓ resolved, bearish |
| UNH DOJ | AVOID flag | AVOID flag — probe multi-front | → persists |
| TLM B scalp | ENTERED-UNRESOLVED | At TP (tp_hit status) | ↑ improved |
| Crypto stats | PF=1.95, +18.1R | PF=1.97, +19.4R | ↑ marginally better |
| Stocks A/B stats | PF=0.27, −5.8R | PF=0.21, −6.3R | ↓ worse |

**New signals added this cycle:** SYN A scalp (at TP), JTO/RIF/BEAM/AAVE B swing (all at TP), ETH B swing short (TP), BTC B swing short (TP).

**Thesis confirmed:** WAIT-FOR-TRIGGER at 16:20 was correct — NFP was the trigger event. Decision now shifts from "wait" to "observe first RTH reaction + confirm triggers."

**Thesis changed:** TSLA was a binary event. Delivery beat but stock selling off = prior planning scenario "buy-the-rumor" confirmed. Short setup strengthened.

---

## 5. Catalyst Coverage

- **Total catalyst_events today (cumulative):** 643 (JSONL `data/catalysts/2026-07-02/`)
- **Active baskets:** 4 (`ai_narrative`, `perps_dex_narrative`, `delisting_thin_liquidity`, `momentum_breakout`)
- **Mapped / unmapped breakdown:** exact query not run (requires SQLite access); **estimated ~65–70% unmapped** (carry-forward from 16:20 review based on pattern observation).

> ⚠️ **CATALYST MAPPING WEAK THIS RUN — use catalyst layer as context, not final decision.**

**Top 3 notable unmapped category events (basket-level, no symbol tag):**
1. `[exploit_hack]` Taiko bridge $1.7M hack recovery (3 articles) — no symbol mapped; TAIKO not in universe.
2. `[exchange_listing]` Binance Futures TradFi perpetual contracts July 2 — not mapped to specific symbols.
3. `[regulatory_sector_headline]` MiCA three-year review (CoinDesk) — macro, no symbol.

**Mapped catalyst highlights:**
- **LLY**: Medicare GLP-1 Bridge (external, confirmed) + analyst upgrade → FRESH, multi-source, CONFIRMS signal.
- **TSLA**: Q2 deliveries 480k → CONTRADICTS price action (bearish divergence).
- **SOL**: Token unlock (AMBCrypto, July) → RISK flag for swing longs.
- **UNH**: DOJ criminal probe (FierceHealthcare, Yahoo Finance) → LEGAL RISK.
- **momentum_breakout basket** (TLM/SYN/ZEC): fresh <1h, `wait_pullback` playbook.
- **ai_narrative** (NEAR/RENDER/TAO/FET): fresh <6h, `related_beta_rotation` playbook.

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** `risk-on / bullish trend` — BTC transition_up, ETH transition_up, breadth 71.4% above EMA20. Dovish NFP lifted BTC $57.9k → $60.1k. F&G 19 (Extreme Fear) = sentiment lagging price, possible contrarian upside. ATR percentile 85% = elevated volatility.
- **Stocks mood:** `risk-on / rotation` — SPY uptrend, QQQ range (tech weak). Healthcare + Financials + Industrials leading. Tech + Energy lagging. VIX 16.44–16.68 = low fear. NFP miss = dovish → supports cyclical/defensive rotation.
- **Dominant narrative:** Dovish NFP miss suppresses rate-hike expectations; GLP-1 healthcare expansion (LLY); TSLA delivery beat + bearish price reaction; BTC recovering post-$57.9k lows.
- **Preferred side now:** `catalyst-backed longs` (LLY healthcare), `value/defensive longs` (JPM financials, XLF), `TSLA short` (failed catalyst); crypto `RS-leader longs on pullback` (HEMI); **avoid tech momentum (NVDA, QQQ short C-tier)**.
- **Best long candidate:** LLY — multi-catalyst, A-tier triggered, healthcare RS-leader, entry $1,211–$1,218.
- **Best short candidate:** TSLA — B-tier short waiting, delivery beat + stock −5.6%, bearish divergence; trigger below ~$415 key level.
- **Best catalyst-backed candidate:** LLY (same as long) — Medicare GLP-1 Bridge + Leerink upgrade.
- **What to avoid:** UNH (DOJ criminal probe), TLM new longs (chase +119%), NVDA/SMH/XLK longs (tech lagging), reversal setups (PF 0.58), weekend-tagged signals (BEAM/AAVE — underperform).
- **What would change the view:** BTC closing below $57.9k (prior low) → risk-off; QQQ recovering above range → broaden to tech longs; UNH probe resolution → XLV may release; NFP revision higher → re-hike risk returns.

---

## 7. Candidate Deep Dives

### Candidate 1: LLY — A-tier Stocks Intraday Long [OPEN-ACTIONABLE]

**Lifecycle:** TRIGGERED (A-tier, intraday, direction=long, score=82.85, confidence=high)
**Mode:** `stocks_intraday_rth_momentum`
**Tier:** A

**Has price already reacted to catalyst?** Yes — GLP-1 Medicare Bridge launched July 1 ($50/month for 20M eligible patients). Leerink upgraded to $1,232. Price hit 52-week high ~$1,200.55 and is likely in the $1,211–$1,218 entry zone (A-tier triggered status confirms entry touched).

**Is the setup chasing?** Moderate risk — stock is at all-time high territory after a catalyst-driven 4%+ surge. However, with A-tier triggered and confirmed entry zone, this is NOT a new chase; the signal pre-positioned at the zone.

**Retest/pullback structure?** Entry zone $1,211–$1,218 represents a pullback from any intraday high. The zone defines the acceptable entry range.

**Is the move overextended?** Elevated risk — stock at 52-week high, multiple catalysts stacked. But regime is risk_on, sector is RS-leader, and earnings are safe until Aug 5. Fundamental catalyst is genuine (not just sentiment).

**Would entry NOW be late?** If price is already in or above the $1,218 top of the zone, any new entry requires checking vs 2-ATR rule. The A-tier triggered status means entry criteria were met; watch for TP1 $1,238 approach.

**Aligned with market mood?** YES — Healthcare RS-leader, risk_on regime, catalyst-backed, sector EMA above all. QQQ lagging makes healthcare relatively even stronger.

**Long/short/wait-for-trigger?** LONG. Triggered. OPEN-ACTIONABLE.

**What invalidates?** 1h close below $1,197.36 (per signal). Or SPY breakdown below key intraday support. Or fresh UNH-style legal news extending to LLY.

**Chase risk?** Moderate (stock at 52-week high). Mitigated by: A-tier pre-positioned trigger, regime support, fundamental catalyst, and earnings distance (Aug 5).

**Catalyst confirmation?** CONFIRMED — Medicare GLP-1 Bridge (July 1), Leerink upgrade, price confirmation at high. Multiple source types, above single_source threshold.

**Legal/Headline check:** No legal/headline risk found. Earnings Aug 5 (safe). Regulatory focus on GLP-1 access is POSITIVE (Medicare expanding coverage). ✓ CLEAN.

**VERDICT: OPEN-ACTIONABLE — best long setup this slot.**

---

### Candidate 2: JPM — A-tier Stocks Intraday Long [OPEN-ACTIONABLE]

**Lifecycle:** TRIGGERED (A-tier, intraday, direction=long, score=82.85, confidence=high)
**Mode:** `stocks_intraday_rth_momentum`
**Tier:** A

**Has price already reacted to catalyst?** No explicit catalyst for JPM today. RS-leader in financials (XLF) — sector play driven by dovish NFP (lower rates environment, but complex for banks: lower NIM vs. better credit outlook).

**Is the setup chasing?** Lower risk than LLY — entry zone $332–$334 with A-tier triggered. JPM has been in uptrend (20d RS vs SPY +12.23%), not at all-time high.

**Retest/pullback structure?** Clean — entry zone $332–$334 is within range. TP1 $337.98, TP2 $340.54, TP3 $344.38. Invalidation $330.29.

**Is the move overextended?** Not significantly — RS +12.23% vs SPY is leadership but not vertical.

**Would entry NOW be late?** A-tier triggered = entry in progress. If already through $334+, check for >2 ATR rule.

**Aligned with market mood?** YES — Financials #2 sector. Dovish NFP complex for banks (lower NIM risk) but sector is RS-leader and the market is treating it risk-on. SPY uptrend supports.

**Long/short/wait-for-trigger?** LONG. OPEN-ACTIONABLE.

**What invalidates?** 1h close below $330.29. Or bank-specific news. Or NFP revision causing rate expectations to swing back hawkish.

**Chase risk?** Low — stock in controlled uptrend, not extended.

**Catalyst confirmation?** Context only — no specific JPM catalyst today. Pure RS + regime play. The news from the swing report ("JPM: AI CHIP RALLY MAY BE HARD TO SUSTAIN" Telegram) is about JPM's research output, not about JPM stock itself.

**Legal/Headline check:** No legal/headline risk found for JPM today. No earnings near term. ✓ CLEAN.

**⚠️ CAUTION NOTE:** Stocks A/B live stats (7d) show PF=0.21, WR=3.1%. Even A-tier JPM faces a poor recent performance environment. Reduce position size vs historical norms. This is an intraday setup — manage to daily risk budget.

**VERDICT: OPEN-ACTIONABLE — second-best long; treat as smaller size given poor stocks stats.**

---

### Candidate 3: TSLA — B-tier Stocks Intraday Short [WAITING]

**Lifecycle:** WAITING FOR ENTRY (B-tier, intraday, direction=short, score=69.11, confidence=medium)
**Mode:** `stocks_intraday_rth_momentum`
**Tier:** B

**Catalyst situation:** Q2 2026 deliveries 480,126 vs 406,024 consensus (+18.2% beat, vs Goldman's 420k also beaten). Yet stock is down **5.6–6%** on the session. Classic buy-the-rumor-sell-the-news. The catalyst was priced in over the prior rally (stock was up 24% from April lows going into the print).

**Is the setup chasing?** NO — the short thesis is validated by the bearish price divergence. Short entry is at a level where price already broke down from the catalyst-pop high. The WAITING status means the trigger price hasn't been officially breached yet — but price action is moving toward it.

**Retest/pullback structure?** The failed delivery pop (initial rally then selloff) IS the retest structure for shorts. Entry on the broken-down retest confirms.

**Is the move overextended (short-side)?** The stock dropped 8.8% from session high. Short entry should not chase the first leg down; wait for the signal trigger level.

**Would entry NOW be late?** Needs the short trigger to confirm. The signal status is WAITING — entry not triggered yet. If price stabilizes and re-bounces from -5.6%, the short may become even better entry. Don't chase the first leg down.

**Aligned with market mood?** YES — TSLA has a catalyst-contradiction (fundamental beat, price breakdown). Short aligns with: (a) failed catalyst pattern, (b) tech/QQQ sector weakness post-NFP, (c) stock had run 24% above April lows = mean-reversion setup.

**Long/short/wait-for-trigger?** SHORT — but WAITING. Confirm trigger level breach before entry.

**What invalidates?** Price recovering above $425–$430 (session open level) would invalidate the bearish divergence. A broad QQQ recovery pulling TSLA back = invalidation.

**Chase risk?** Moderate. Don't short at -8.8% from high without trigger confirmation. Wait for signal to activate.

**Catalyst confirmation?** Yes but inverted — delivery beat CONTRADICTS long signal; CONFIRMS short thesis via price reaction.

**Legal/Headline risk:** None identified. Financial report Jul 22. ✓ CLEAN for legal. But headline risk = any Musk announcement or delivery revision could squeeze.

**VERDICT: WAITING FOR ENTRY — best short candidate this slot. Wait for trigger confirmation; don't chase first leg down.**

---

### Candidate 4: SYN — A-tier Crypto Scalp [AT TP / ENTERED-UNRESOLVED]

**Lifecycle:** AT TP (A-tier, scalp, direction=long, score=80.x, status=tp_hit)
**Mode:** `scalp`
**Tier:** A

**Context:** SYN was the only A-tier crypto signal added in this cycle. The scalp signal has reached TP (tp_hit status). This means either:
- The paper position is ENTERED-UNRESOLVED (entry filled, TP touched, but no clean exit recorded before the window)
- OR the signal is CLOSED WIN at TP1

**Price context:** SYN +9.35–9.69% in 24h. RS vs BTC +6.88–7.32%. Funding -2.5e-05 (near neutral, crowding normal). OI +3.77–5.63% with price up = fresh positioning. L/S ratio 0.656 (slight short majority = potential for squeeze).

**Is entry still valid?** NO — the signal is at TP, not at entry. This is for monitoring/closure, not for new entry consideration. Scalp mode has inherent limitations (1W/7L 14d PF 0.14) and A-tier in scalp has higher edge uncertainty.

**What to monitor:** Whether SYN holds above its resistance or rejects; could set up intraday long for the next cycle if it retests.

**VERDICT: ENTERED-UNRESOLVED / AT TP — monitoring only. No new scalp entry. Note: A-tier crypto scalp exists in the system; it's reaching TP which is a positive signal for the scalp module even if statistically challenged.**

---

### Candidate 5: UNH — Legal/Headline Flag [AVOID ALL MODES]

**Lifecycle:** TRIGGERED (C-tier, intraday + swing longs, multiple signals active)
**Tier:** C (intraday long ~70, swing long ~75)

**⚠️ LEGAL/HEADLINE RISK — AVOID ALL MODES ⚠️**

**DOJ criminal probe details (confirmed via FierceHealthcare, Yahoo Finance, Medical Economics):**
- **Active criminal AND civil DOJ investigations** into Medicare Advantage billing practices.
- **Expanded to:** Optum Rx (pharmacy benefits) + physician reimbursement practices + Medicare Advantage diagnoses inflation.
- **Multi-front criminal investigation** — DOJ interviewing former employees.
- **No resolution timeline.** Outcomes range from settlement to forced divestiture of Optum.
- UNH is cooperating (third-party review in progress) but this does NOT reduce near-term binary risk.
- Medicare Advantage = UNH's single largest revenue segment.

**Price context:** UNH C-tier intraday long (score ~70) triggered, C-tier swing (score ~75) triggered. These are watchlist/research — NOT Telegram-actionable. But the legal flag overrides any manual consideration.

**Signal verdict for all UNH signals:** **AVOID ALL MODES.** Legal risk is active, multi-front, criminal, with no resolution timeline. Any UNH long — regardless of technical score — is a legal-risk setup that should be avoided until the probe resolves or settles.

**XLV note:** XLV (healthcare ETF) is B-tier intraday long (score 79.21, triggered). XLV is a cleaner play on healthcare sector RS than UNH directly. XLV diversifies away from single-stock DOJ risk. XLV is the preferred healthcare exposure vehicle, NOT UNH directly.

**VERDICT: AVOID — active DOJ criminal probe multi-front. Use XLV for healthcare sector exposure instead of UNH.**

---

## 8. Best Candidates Ranked

| Rank | Symbol | Mode | Direction | Tier | Action | Why |
|------|--------|------|-----------|------|--------|-----|
| 1 | **LLY** | stocks intraday | LONG | A | OPEN-ACTIONABLE | Multi-catalyst, RS-leader healthcare, A-tier triggered, earnings safe Aug 5 |
| 2 | **JPM** | stocks intraday | LONG | A | OPEN-ACTIONABLE | RS-leader financials, A-tier triggered, dovish NFP rotation beneficiary |
| 3 | **TSLA** | stocks intraday | SHORT | B | WAITING FOR ENTRY | Failed catalyst (beat + down 6%), bearish divergence, pre-positioned signal |
| 4 | **XLV** | stocks intraday | LONG | B | TRIGGERED | Healthcare ETF RS-leader, cleaner UNH exposure without legal risk |
| 5 | **HEMI** | crypto swing | LONG | B | WAITING (pullback) | RS-leader crypto (+14.81% 24h, +10.1% vs BTC), entry zone 0.0048-0.0049 |

**Best long-watch (no-trade yet):** HEMI — pullback to 0.0048–0.0049, trigger: price accepts in zone with stable BTC above $58k.

**Best short-watch:** TSLA — trigger: confirmation breakdown below signal entry level (~$415 area) with volume; don't chase the first -8.8% leg.

**Best catalyst-watch:** LLY — already triggered; catalyst-watch now focuses on monitoring vs TP1 ($1,238) and managing if price extends into TP2/TP3 zone ($1,252 / $1,273).

**Excess candidates not fitting top 5 (§F rule):**
- COIN B intraday long (triggered, score 79.88) — crypto-sector stock, active catalyst (Robinhood Chain news), valid but behind LLY/JPM in quality.
- NEAR B swing crypto long (triggered) — RS leader in AI narrative basket, pullback entry preferred.
- ZEC B swing long (triggered) — momentum_breakout basket, no catalyst.
- GOOGL B intraday long (triggered, score 65) — tech/QQQ weak post-NFP, regime less supportive.

---

## 9. Avoid / No Trade (this decision window only)

**This window only — scanning continues, system always-on:**

1. **UNH (all modes):** Active DOJ criminal probe, multi-front, no timeline. AVOID.
2. **TLM (new longs):** Chase risk (+119% 24h), Binance delisting monitoring, scalp already at TP. Do NOT enter new long.
3. **NVDA / SMH / XLK longs:** Tech sector lagging post-NFP (QQQ in range). Known failure mode in current regime (A-tier overpromotion on losing names).
4. **Reversal setups (crypto):** PF 0.58 historically. DYDX short-side not triggered, but avoid playing DYDX as a long reversal — fresh shorts pressing.
5. **BEAM / AAVE B-swing crypto (weekend-tagged):** Both have `weekend=Y` flag in active signals. Weekend signals underperform (WR 21%, stats observation). Do not enter late in the week on weekend-tagged signals.
6. **TSLA long:** Despite delivery beat, price action is bearish. The B-long signal waiting is overshadowed by the stronger short signal and bearish price reaction. Avoid TSLA long this window.

**System never stops.** This avoid list applies only to this decision window (18:30–22:30 EEST). Scanning, data collection, and tracking continue at all times.

---

## 10. Main Risks

1. **BTC correlation cluster:** All 27 crypto signals are LONGS. If BTC breaks below $57.9k (recent low), the entire crypto book is simultaneously at risk. Current BTC ~$60.1k offers ~$2.2k buffer.

2. **Stocks A/B poor performance (7d):** PF=0.21, WR=3.1%, -6.3R. Even A-tier stocks intraday signals (LLY, JPM) face a degraded recent-performance environment. Position sizing should reflect this.

3. **Catalyst mapping weak (~65-70% unmapped):** Many events in the 643-item JSONL are unmapped to symbols. Catalyst conviction is limited to the symbols explicitly matched (LLY, TSLA, SOL, UNH, BTC ETF flows).

4. **NFP miss = weak economy signal:** While the dovish miss is short-term risk-on, a sustained weak job market may eventually hurt stocks more broadly. Watch for follow-through weakness in coming sessions.

5. **QQQ in range (tech weak):** If QQQ breaks down further, stocks risk_on mood could flip to mixed/risk-off. SPY-QQQ divergence is unusual and may resolve in either direction.

6. **TSLA short squeeze risk:** If broader market rallies, TSLA short could face squeeze. Always maintain defined risk (invalidation above $425 area).

7. **Reddit social sources 403 error (recurring):** Reddit blocked in all 6 social fetch attempts this cycle. Social sentiment blind spot continues. This is a data gap for crowd sentiment.

8. **TLM delisting monitoring active:** Existing TLM scalp position is at TP but carries Binance delisting risk. No new TLM longs.

---

## 11. Action Plan — next 4 hours (18:39–22:39 EEST)

**Immediate (now — 19:00):**
- ✅ LLY A-tier: Monitor open position near $1,211–$1,218; watch for TP1 approach at $1,238. Invalidation $1,197.
- ✅ JPM A-tier: Monitor open position near $332–$334; TP1 $337.98. Invalidation $330.29.
- 👀 TSLA B short: Watch for trigger confirmation below ~$415 area. Do not chase first leg down.
- ❌ UNH: Zero exposure regardless of C-tier trigger status.

**Near-term (19:00–21:00):**
- 👀 HEMI crypto swing: If BTC holds $59k+, watch HEMI for pullback to 0.0048–0.0049 entry zone. 7d return +1.45% = early in the swing thesis.
- 📊 Cycle 08 expected ~20:00–20:30 EEST: Fresh reports will update signal count and any new A-tier generation.
- 📊 Paper shadow B/A digest NOT sent today (Telegram send error in cycle 7 — note for §14 TODO).

**Late session (21:00–22:39):**
- 🔄 This review hands off to the 21:30 late-session risk review slot.
- Risk check: are LLY/JPM longs near TP or stop? Is TSLA short active?
- Monitor: 21:30 slot should assess late-session risk for any crypto long correlation squeeze.

---

## 12. Final Verdict per Mode

| Mode | Asset | Verdict | Notes |
|------|-------|---------|-------|
| **Scalp (crypto)** | crypto | CAUTION | SYN A at TP (entered-unresolved); scalp historically low PF (0.14, 14d). No new scalp signals from this cycle. |
| **Intraday (crypto)** | crypto | WAIT-FOR-TRIGGER | B-tier intraday longs (HEMI, NEAR, ME, ZBT, SYN, etc.) active. No A-tier crypto intraday. Prefer pullback entries, RS leaders. |
| **Swing (crypto)** | crypto | WATCHLIST — best mode | 14d PF 5.80, WR 72%. Multiple B-tier swings at TP (JTO/RIF/BEAM/AAVE/HEMI). New entries: HEMI pullback 0.0048–0.0049. TLM/BREV avoid new entry (chase/crowded). |
| **Intraday (stocks)** | stocks | CAUTION — A-tier only | LLY A (OPEN-ACTIONABLE, catalyst-backed), JPM A (OPEN-ACTIONABLE, regime-aligned). TSLA B short (WAITING). XLV B (TRIGGERED). Avoid: UNH (legal), TLM, tech (NVDA/SMH). Position-size down due to 7d PF=0.21. |
| **Swing (stocks)** | stocks | WATCHLIST ONLY | Swing is capped to C-tier (audit: -12R, 0W/12L 48h). JPM swing C at TP; LLY swing C active. Research context only. |
| **Invest (stocks)** | stocks | NOT IMPLEMENTED | Desk uses swing proxy for invest context. Watchlist research only. |

---

## 13. Sources

- [Current price of Bitcoin for July 2, 2026 — Fortune](https://fortune.com/article/price-of-bitcoin-07-02-2026/)
- [Bitcoin Price Prediction July 2026 — CryptoTimes](https://www.cryptotimes.io/2026/07/02/bitcoin-price-prediction-july-2026-will-btc-go-up-or-crash/)
- [NFP June 2026 — FXStreet](https://www.fxstreet.com/news/nonfarm-payrolls-set-to-grow-by-over-100k-in-june-reinforcing-bets-of-upcoming-fed-rate-hikes-202607020500)
- [United States Nonfarm Payrolls — Investing.com](https://www.investing.com/economic-calendar/nonfarm-payrolls-227)
- [DOJ criminal probe extends to Optum Rx — FierceHealthcare](https://www.fiercehealthcare.com/payers/wsj-report-doj-interviewing-former-employees-about-medicare-billing-practices-unitedhealth)
- [UnitedHealth DOJ investigation — Yahoo Finance](https://finance.yahoo.com/news/unitedhealth-under-doj-investigation-buy-110002685.html)
- [LLY gains 4% to all-time high — TradingView/Zacks](https://www.tradingview.com/news/zacks:1a985938a094b:0-lly-stock-gains-4-to-all-time-high-is-obesity-access-the-catalyst/)
- [Lilly Q1 2026 results + GLP-1 guidance — investor.lilly.com](https://investor.lilly.com/news-releases/news-release-details/lilly-reports-first-quarter-2026-financial-results-raises-full)
- [Tesla Q2 deliveries 406k bar — TechTimes](https://www.techtimes.com/articles/319305/20260629/tesla-q2-2026-deliveries-wall-street-sets-406024-bar-july-2-report.htm)
- [Tesla stock sinks 6% despite strong deliveries — CNBC](https://www.cnbc.com/quotes/TSLA)

---

## 14. Fix Requests / TODO

### TODO-paper-shadow-telegram-send-error
- **issue:** Paper-shadow A/B Telegram digest failed to send: `TelegramNotifier.__init__() missing 1 required positional argument: 'config_path'` (cycle 07 step 14)
- **evidence:** `cycle_07_18-08_summary.md` step 14: "send error: TelegramNotifier.__init__() missing 1 required positional argument: 'config_path'"`
- **suggested manual fix:** Inspect `scripts/paper_shadow_telegram_digest.py` (or equivalent); verify TelegramNotifier instantiation passes config_path. May need to pass the config path explicitly or use a default path constant.
- **priority:** medium
- **first observed:** 2026-07-02 18:29 EEST

### TODO-stocks-ab-performance-regression
- **issue:** Stocks A/B live 7d performance (PF=0.21, WR=3.1%, -6.3R) is severely below the 14d playbook hint (PF=2.03, WR=55%). This suggests either a recent regime change hurting stocks intraday or a structural issue in recent stock signal generation.
- **evidence:** signal-stats stocks A/B: `PF=0.2083, avgR=-0.2184, totalR=-6.3333`; playbook note: "14d WR 55%, PF 2.03, +80R"
- **suggested manual fix:** Run a cohort breakdown on stocks intraday A/B signals for the last 7 days — check if losses are concentrated in specific symbols (NVDA/SMCI/SMH), directions (short vs long), or entry modes (breakout vs pullback). May require score recalibration or a short-stocks freeze in this regime.
- **priority:** high
- **first observed:** 2026-07-02 18:39 EEST (confirmed regression vs playbook claim)

### TODO-reddit-social-403-persistent
- **issue:** All 6 Reddit social source fetches fail with 403 error every cycle. Reddit blocking automated access.
- **evidence:** cycle 07 steps 2+3: "Failed social source Reddit CryptoCurrency/Bitcoin/Ethereum: 403 Client Error: Blocked"
- **suggested manual fix:** Either remove Reddit from social sources config (it's consistently unavailable) or implement a Pushshift/scraping alternative. Consider replacing with a different social sentiment API (e.g., Santiment free tier, LunarCrush). Without Reddit, social sentiment is blind-spotted.
- **priority:** low (workaround: use Telegram channel sources instead)
- **first observed:** carried-forward; confirmed this cycle
