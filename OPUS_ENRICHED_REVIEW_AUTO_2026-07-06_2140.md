---
REVIEW: OPUS ENRICHED REVIEW — ⚠ ADVISORY ONLY — NO EXECUTION
SLOT: Late-Session Risk Review · 2026-07-06 · 21:30 EEST
WRITTEN: 2026-07-06 21:40 EEST
PREV REVIEW: 2026-07-06 18:40 EEST (US open reaction)
STATUS: AUTOMATED SCHEDULED RUN — NO HUMAN IN SESSION
---

# §1 — EXECUTIVE SUMMARY

BTC recovered from the 18:40 gap-trap intraday low ($61,677) back to $63,500–$63,650, but now faces structural resistance at $63,999. Crypto regime remains range/chop (neutral) — the recovery was a range-rebound, not a trend initiation. F&G at 24 (Fear) and ETH/BTC flat at 0.0282 confirm the absence of bullish momentum expansion.

Stocks session is closed. All A/B stocks intraday setups remain demoted to C-tier by the global drawdown guard (7d: −3.0R / PF 0.00). No actionable stocks signals tonight.

**⚠ FOMC minutes drop July 8 (tomorrow). Reduce swing sizing tonight.**

Top late-session watching positions:
- **NEAR/USDT**: swing WAITING FOR ENTRY at $2.037–2.054; reactive pullback entry only
- **ETH/USDT**: catalyst-backed (Bitmine accumulation + ETF 7d positive); entry zone $1,775–1,790 on pullback

**Hard avoids**: VANRY (Binance Monitoring Tag July 3, 2026 — delisting risk), TLM (Binance delisting monitoring May 2026), MSFT/UNH (legal/DOJ risk).

⚠ **PART 1 regression worsening**: 18 untracked B-tier legacy alerts today (vs 11 at 18:40 cycle). Telegram push count diverging from proposed_signals.

**Head Trader verdict: WATCH_ONLY** — no clean new entries at current prices; set price alerts only.

---

# §2 — DATA USED

| Source | File / Run | Age at 21:40 EEST | Quality |
|--------|-----------|-------------------|---------|
| Cycle 7 summary | `data/scheduled_runs/2026-07-06_default_schedule/cycle_07_19-24_summary.md` | 1h 50m | FRESH |
| Scalp report | `data/reports/scalp/2026-07-06_16-31_scalp_report.md` | 2.2h | USABLE |
| Intraday report | `data/reports/intraday/2026-07-06_16-37_intraday_report.md` | 2.1h | USABLE |
| Swing report | `data/reports/swing/2026-07-06_14-19_swing_report.md` | 4.4h | CARRY-FORWARD ⚠ |
| Stocks intraday | `data/reports/stocks/intraday/2026-07-06_18-19_stocks_intraday_report.md` | 0.4h | VERY FRESH ✓ |
| Previous review | `OPUS_ENRICHED_REVIEW_AUTO_2026-07-06_1840.md` | 3.0h | CONTEXT |
| Active signals (crypto) | CLI `active-signals --class crypto` | 0m | LIVE |
| Active signals (stocks) | CLI `active-signals --class stocks` | 0m | LIVE |
| Signal stats (crypto) | CLI `signal-stats --class crypto` | 0m | LIVE |
| Signal stats (stocks) | CLI `signal-stats --class stocks` | 0m | LIVE |
| Untracked alerts | CLI `detect_untracked_legacy_alerts` | 0m | LIVE |
| Web research | BEL, VANRY (CoinGabbar), BTC macro context | ~1h | SUPPLEMENTAL |

---

# §3 — SCHEDULER / DATA FRESHNESS

- **Last completed cycle**: Cycle 7 — 19:24–19:50 EEST — ok=32 / failed=0
- **Next scheduled cycle**: ~22:30–23:00 EEST (estimated)
- **Scheduler health**: All 32 steps completed in cycle 7. No failed steps.
- **Staleness flags**:
  - Swing report 4.4h old — carry-forward; use with caution for fresh signal interpretation
  - Onchain: `interface_ready_config_missing` (no `config/onchain.yaml`)
  - Stocks: DATA_GAP_LATE 40% of intraday signals blocked (RTH session ended)
- **Asia dead-zone guard**: Activates 01:00 EEST tonight (23:00 UTC). Crypto scalp/intraday demoted to C for 00:00–06:00 UTC. Swing unaffected.

---

# §3A — AGENT COUNCIL (JSON)

```json
{
  "review_slot": "late_session_risk_review",
  "timestamp": "2026-07-06T18:40:00Z",
  "agents": [
    {
      "agent_id": "data_quality",
      "verdict": "DEGRADED",
      "confidence": 55,
      "key_finding": "18 untracked B-tier legacy Telegram alerts today (up from 11 at 18:40 cycle) — PART 1 regression worsening. 11 dead news sources (Business Wire, SEC EDGAR, announcement TG channels). Onchain config missing. Stocks intraday DATA_GAP_LATE 40% blocks. Active crypto signal counts stable.",
      "recommendation": "Treat Telegram B-tier alert volume as unreliable until PART 1 patched. All signals ADVISORY-ONLY. Do not infer closed positions from Telegram push count."
    },
    {
      "agent_id": "market_regime",
      "verdict": "RANGE_CHOP_NEUTRAL",
      "confidence": 72,
      "key_finding": "Crypto range/chop (neutral) confirmed by both scalp and intraday reports. BTC recovered from $61,677 intraday gap-trap low to $63,500–$63,650 but faces structural resistance at $63,999. Breadth 48.72% EMA20 — not bullish expansion. ETH/BTC 0.0282 flat — no altcoin rotation signal. Stocks session closed, regime bullish (VIX 15.83, 4/4 indices up) but untradeable tonight.",
      "recommendation": "Size to chop: no directional momentum bias. Favor reactive pullback entries off proven levels. Reduce swing sizing ahead of FOMC July 8."
    },
    {
      "agent_id": "catalyst_narrative",
      "verdict": "MIXED_CATALYST",
      "confidence": 65,
      "key_finding": "1119 events today, 3 baskets. Dominant basket: momentum_breakout (VANRY/TLM/ANSEM) — all already extended, tagged avoid_chase. Positive: XRP MiCA CASP authorization (30 EEA countries), BTC Clarity Act progress. Negative: Summer.fi $6M exploit (ETH DeFi ecosystem advisory), UNH DOJ probe, MSFT 4,800 layoffs + Xbox restructure. FOMC July 8 not in automated macro calendar.",
      "recommendation": "ETH catalyst-backed but carry Summer.fi DeFi contagion advisory. XRP: wait for pullback entry. VANRY/TLM: fundamental risk overrides TA. FOMC tomorrow reduces swing sizing to minimum."
    },
    {
      "agent_id": "derivatives_squeeze",
      "verdict": "SQUEEZE_MIXED",
      "confidence": 60,
      "key_finding": "BEL: funding -0.375% to -0.783% (crowded short) + OI +32% = classic squeeze setup but no external catalyst confirmed. VANRY short squeeze partially fired ($1.72M liquidations, -$1.15M shorts) — price already +47% extended. SYN: price down + OI up = fresh short accumulation, potential squeeze reversal. Squeeze phase distribution dominated by post_unwind_chop (47 assets) — most recent squeezes already exhausted.",
      "recommendation": "BEL: manual review only — do not add into squeeze without catalyst. VANRY: squeeze exhausted + monitoring tag = hard avoid. SYN: watch for failed-bounce reversal signal before entry."
    },
    {
      "agent_id": "technical_entry",
      "verdict": "MIXED_ENTRY_NO_CHASE",
      "confidence": 58,
      "key_finding": "No clean low-risk entries at 21:40 current prices. NEAR price ~$2.06 slightly above waiting entry zone ($2.037–2.054) — reactive pullback entry valid. ETH $1,793 — cleanest entry on pullback to $1,775–1,790. BTC at structural resistance $63,999 — breakout or pullback bifurcation unresolved. SYN: $0.39–0.40 short zone only on failed-bounce confirmation. BTC ATR 509; ETH near-term support $1,737 (today's intraday low).",
      "recommendation": "Wait for price to come to levels, not chase. Preferred triggers: ETH $1,775–1,790 or NEAR $2.03–2.05. SYN short only on confirmed failed bounce. No BTC entry at resistance."
    },
    {
      "agent_id": "execution_lifecycle",
      "verdict": "NORMAL_LIFECYCLE",
      "confidence": 80,
      "key_finding": "Paper monitor: OPEN=1 | WAITING=5 | ENTERED_UNRESOLVED=33 | REVIEW_SHADOW=155 | NO-ENTRY/STALE=83 | CLOSED=370W/78L/0flat | NEEDS_REVIEW=1. Changes vs 18:40: WAITING grew 3→5 (+2 new entries cycle 7). NO-ENTRY grew 78→83 (+5 expired). BEL scalp+intraday+swing TP hits. TRB swing+intraday TP hits. ALICE swing TP hit. NEEDS_REVIEW=1 uninvestigated.",
      "recommendation": "Check NEEDS_REVIEW=1 signal manually in next cycle. Do not open new entries without operator sign-off in late session. Monitor 33 ENTERED_UNRESOLVED positions for overnight TP/SL levels."
    },
    {
      "agent_id": "risk_manager",
      "verdict": "RISK_ELEVATED",
      "confidence": 75,
      "key_finding": "FOMC minutes July 8 (tomorrow 14:00 ET) not in automated macro calendar — manual advisory only. Asia dead-zone activates 01:00 EEST tonight. Stocks guards correctly firing (global 7d: -3.0R/PF0.00, long guard active). DeFi contagion tail risk (Summer.fi exploit). 18 untracked alerts = position sizing blind spot. Paper portfolio maxDD 13.43% within limits. Shadow NOT_READY (11d window < 14d minimum, 4/6 criteria).",
      "recommendation": "No new swing positions tonight (FOMC tomorrow). Cap intraday exposure 23:00+ UTC. Do not disable stock guards. ETH positions carry reduced size due to DeFi advisory."
    },
    {
      "agent_id": "playbook_performance",
      "verdict": "SWING_DOMINANT",
      "confidence": 77,
      "key_finding": "Swing: WR 72% / PF 5.80 / +24R/14d (strongest mode). Scalp B-tier 7d: WR 18.6% / PF 1.83 / +55.84R. Intraday no-catalyst bucket: WR 23% / PF 0.70 / -3R/14d (NET NEGATIVE). Stocks A/B 7d: -3.0R/PF 0.00. Model F paper: +$1,685 / +33.7% / maxDD 13.43% under Bybit non-VIP fee profile. Conservative fee estimate: -5.65%.",
      "recommendation": "Prioritize swing setups with catalyst or strong RS confirmation. Skip intraday no-catalyst setups entirely. Stocks: wait for guard reset. Scalp B-tier valid only with high-confidence entry — no chasing extended moves."
    },
    {
      "agent_id": "head_trader",
      "verdict": "WATCH_ONLY",
      "confidence": 85,
      "key_finding": "Late session 21:40 EEST — stocks closed, crypto in chop recovery near resistance. F&G 24 (Fear). FOMC July 8 tomorrow. No clean new entries at current prices. Top watch: NEAR/USDT (swing WAITING, reactive pullback entry $2.03–2.05) and ETH/USDT (catalyst-backed Bitmine+ETF, entry $1,775–1,790). Squeeze watch: BEL (manual review, crowded short). Short watch: SYN (fresh short OI, failed-bounce reversal only). Hard avoids: VANRY (Binance monitoring July 3), TLM (delisting monitoring May 2026).",
      "recommendation": "WATCH_ONLY: set price alerts at NEAR $2.03–2.05, ETH $1,775–1,790, SYN $0.39–0.40 short. No new positions tonight without clear pullback trigger. Reduce swing sizing to minimum due to FOMC tomorrow. VANRY and TLM: do not trade until monitoring status cleared."
    }
  ],
  "council_summary": {
    "consensus_verdict": "WATCH_ONLY",
    "consensus_confidence": 70,
    "dominant_concern": "range_chop_near_resistance_plus_fomc_tomorrow",
    "best_opportunity": "near_usdt_swing_waiting_reactive_entry",
    "catalyst_backed": "eth_usdt_bitmine_etf_positive",
    "top_avoid": "vanry_usdt_monitoring_tag_july3_2026"
  }
}
```

---

# §3B — AGENT COUNCIL TABLE

| Agent | Verdict | Conf | Key Concern | Recommendation |
|-------|---------|------|-------------|----------------|
| data_quality | DEGRADED | 55% | 18 untracked legacy alerts; 11 dead sources; onchain missing | B-tier Telegram unreliable; advisory-only |
| market_regime | RANGE_CHOP_NEUTRAL | 72% | BTC chop recovery, near $64K resistance; breadth 48.72% | Size to chop; reactive entries; reduce swing for FOMC |
| catalyst_narrative | MIXED_CATALYST | 65% | avoid_chase basket dominant; DeFi exploit advisory on ETH | ETH carry DeFi advisory; XRP pullback; skip VANRY/TLM |
| derivatives_squeeze | SQUEEZE_MIXED | 60% | BEL crowded short (no catalyst); VANRY squeeze exhausted | BEL manual review only; SYN watch for reversal |
| technical_entry | MIXED_ENTRY_NO_CHASE | 58% | No clean entries at current prices | Wait for ETH $1,775–90 or NEAR $2.03–05 pullback |
| execution_lifecycle | NORMAL_LIFECYCLE | 80% | WAITING 3→5; NEEDS_REVIEW=1 uninvestigated | Check NEEDS_REVIEW=1; no new entries without sign-off |
| risk_manager | RISK_ELEVATED | 75% | FOMC July 8; Asia dead-zone 01:00 EEST; DeFi tail risk | No new swings tonight; cap intraday 23:00+ UTC |
| playbook_performance | SWING_DOMINANT | 77% | Intraday no-catalyst −3R/14d; stocks guards blocking | Swing + catalyst only; skip no-catalyst intraday |
| head_trader | WATCH_ONLY | 85% | Late session, chop, FOMC tomorrow, no clean entries | Alerts only: NEAR $2.03–05, ETH $1,775–90, SYN $0.39 short |

**Consensus**: WATCH_ONLY · Confidence 70% · 9/9 agents aligned on no new entries at current prices

---

# §4 — WHAT CHANGED vs PREVIOUS REVIEW (18:40 EEST)

| Metric | 18:40 EEST | 21:40 EEST | Delta |
|--------|-----------|-----------|-------|
| BTC price | ~$61,677 (intraday gap-trap low) | $63,426–$63,652 | +$1,975 recovered ✓ |
| ETH price | ~$1,737 (intraday low) | ~$1,793 | +$56 recovered ✓ |
| VIX | 16.29 | 15.83–15.91 | Improved ↓ |
| F&G | 24 | 24 | Unchanged |
| WAITING signals | 3 | 5 | +2 new (AIGENSYN swing added) |
| NO-ENTRY/STALE | 78 | 83 | +5 expired this cycle |
| REVIEW_SHADOW | 154 | 155 | +1 |
| Untracked legacy alerts | 11 | 18 | **+7 WORSENED ⚠** |
| BEL lifecycle | B-tier ENTERED | TP HIT (scalp+intraday+swing) | Resolved higher ✓ |
| TRB lifecycle | B-tier ENTERED | TP HIT (swing+intraday) | Resolved higher ✓ |
| ALICE lifecycle | B-tier ENTERED | TP HIT (swing) | Resolved higher ✓ |
| PUMP lifecycle | B-tier ENTERED | TP HIT (intraday) | Resolved higher ✓ |
| Stocks intraday report | Stale | 0.4h (VERY FRESH) | Refreshed ✓ |

**Narrative delta**: The US open gap-trap (BTC $63,590 → $61,677, −2.9%) described in the prior review has fully reversed during the afternoon session. BTC and ETH both recovered to pre-gap-trap levels. This is **range recovery, not trend initiation** — BTC is back at the same level as the opening and faces the same structural resistance at $63,999. The cluster of TP hits on BEL/TRB/ALICE/PUMP confirms the scalp/intraday long thesis from the prior cycle was correct. Seven additional untracked legacy alerts fired in cycle 7, worsening the PART 1 regression.

---

# §5 — CATALYST COVERAGE

- **Total events today**: 1,119 (catalyst_events.jsonl cumulative)
- **Active narrative baskets**: 3

| Basket | Tag | Primary Symbols | Action |
|--------|-----|----------------|--------|
| momentum_breakout | avoid_chase | VANRY, TLM, ANSEM | ❌ AVOID — already extended >2 ATR |
| perps_dex_narrative | wait_pullback | HYPE | ⏳ Wait for pullback (exploit_hack flag active) |
| delisting_thin_liquidity | avoid_low_liquidity | (none primary) | ❌ AVOID — thin liquidity |

**Production risk flags active**:
- APT: `token_unlock` (dilution risk)
- ETH: `exploit_hack` advisory (Summer.fi $6M DeFi exploit, ecosystem-adjacent)
- HYPE: `exploit_hack` (direct risk flag)
- MSFT: `legal_risk` (securities_fraud class action)
- SOL: `exploit_hack` advisory

**Positive catalysts** (partially or fully unmapped to active signals):
- **XRP**: MiCA CASP full authorization for 30 EEA countries — regulatory tailwind; no active B-tier signal yet
- **BTC**: US Clarity Act congressional progress — macro positive
- **NVDA**: disputes supply delay report — AI/tech sector positive sentiment

**Negative catalysts**:
- **UNH**: DOJ probe, stock −16% (large health sector drag)
- **MSFT**: 4,800 job cuts + Xbox restructuring; `legal_headline_risk: securities_fraud`
- **Summer.fi**: $6M DeFi exploit — ETH ecosystem advisory, not direct ETH protocol risk

**⚠ FOMC minutes July 8 NOT in automated macro calendar** — manual advisory only. Scheduled ~14:00 ET tomorrow. Reduces swing sizing tonight and tomorrow pre-event.

**Coverage gap note**: Estimated 80%+ of 1,119 events are unmapped to active symbols. The 3 baskets cover highest-conviction narratives; individual event-to-symbol linkage unvalidated for full corpus.

---

# §6 — MARKET LANDSCAPE

## Crypto Intelligence Layer (Cycle 7, 19:50 EEST)

| Metric | Value | Signal |
|--------|-------|--------|
| Fear & Greed | 24 (FEAR) | Crowd is fearful — contrarian caution |
| VIX | 15.91 | Low vol regime (improved from 16.29) |
| SPY | Up | Risk-on session |
| QQQ | Up | Risk-on session |
| BTC price | $63,426–$63,652 | Chop recovery, approaching resistance |
| ETH/BTC ratio | 0.028167 | Flat — no altcoin rotation trigger |
| Crypto mode (internal) | trend | Conflicts with range/chop in reports — trust reports |
| Stocks mode | risk_on | Bullish session; after-hours, untradeable |
| BTC support | $61,307 | Today's proven intraday low (gap-trap bottom) |
| BTC resistance | $63,999 | Structural resistance |
| BTC ATR (scalp) | 509.42 | Normal volatility |
| ETH price | $1,792.97 | Recovered; entry zone below current |

## Squeeze Phase Distribution (Cycle 7)

| Phase | Count | Implication |
|-------|-------|-------------|
| post_unwind_chop | **47** | **Dominant** — most squeezes already fired and exhausted |
| unknown | 34 | Not yet classified by system |
| build_up | 33 | Early-stage squeeze potential |
| squeeze_expansion | 9 | Active squeeze in progress |
| unwind | 4 | Squeeze currently unwinding |

Dominant `post_unwind_chop` (47) means most derivative squeezes this cycle have already resolved. New squeeze setups limited to the 33 `build_up` assets.

## §6A — Market Mood / Risk Routing

| Dimension | Assessment |
|-----------|-----------|
| Crypto direction | CHOP — range recovery, not trend initiation |
| Preferred side | Catalyst-backed long (ETH > BTC); reactive pullback entries only |
| Stocks session | CLOSED — guards active, no A/B actionable tonight |
| Macro event | FOMC July 8 — reduce/avoid new swing tonight |
| DeFi tail risk | ADVISORY — Summer.fi exploit, ETH ecosystem adjacent |
| Asia dead-zone | Activates 01:00 EEST — scalp/intraday auto-demoted to C |
| Session overall | WATCH_ONLY — set alerts, no entries at current prices |

---

# §7 — CANDIDATE DEEP DIVES

## 7.1 — BEL/USDT · ENTERED / TP HIT · Manual Review

**Status**: Multiple TP hits confirmed in cycle 7: scalp B-tier TP hit, intraday B-tier TP hit, swing B-tier TP hit. Lifecycle: signals transitioning toward CLOSED WIN or ENTERED_UNRESOLVED partial hit.

**Thesis**: Short squeeze — heavy short crowding (funding −0.375% to −0.783%), OI +32%. No confirmed external catalyst found via WebSearch. Price follow-through from scalp/intraday TP zones to swing TP confirms squeeze dynamic was active throughout the session.

**Derivatives**:
- Funding: −0.375% to −0.783% (very crowded short)
- OI: +32% vs prior session (shorts increasing even as price moved up)
- Squeeze phase: `build_up` → `squeeze_expansion` probable

**Risk**: Pure squeeze play without external catalyst. If BTC/ETH correct, BEL shorts may re-accumulate. Any mean-reversion after TP zones = leveraged unwind risk.

**Lifecycle action**: TP hit signals → mark CLOSED WIN per playbook. Do **not** re-enter above TP zones. If price pulls back to prior resistance (now support), evaluate as fresh setup with fresh funding check.

---

## 7.2 — NEAR/USDT · WAITING FOR ENTRY · Cleanest Setup

**Status**: B-tier swing WAITING FOR ENTRY at $2.037–2.054. B-tier scalp/intraday WAITING adjacent. Current price ~$2.06 (0.3–1.1% above entry zone — within reactive pullback reach).

**Thesis**: AI/L1 narrative sector momentum. Swing report score 59.5 (C/B border). Both swing and scalp have entry zones just below current price — textbook reactive-entry setup in chop regime.

**Catalyst**: No specific catalyst confirmed. Playbook: `crypto_swing_narrative_rs_momentum` (PF 5.80 / WR 72%). Pure momentum + narrative sector correlation.

**Derivatives**: Neutral — no extreme funding, no active squeeze phase flagged.

**Technicals**: Entry zone $2.037–2.054 is 0.3–1.1% below current price. Normal chop volatility would reach this zone.

**Risk**: FOMC tomorrow limits overnight swing sizing. No catalyst = pure momentum. If BTC fails $63,999, NEAR likely revisits lower.

**Lifecycle action**: Set price alert at $2.03–2.05. Do NOT enter at $2.06 — reactive entry only. Price must come to the level.

---

## 7.3 — ETH/USDT · WAITING FOR ENTRY · Best Risk-Adjusted Watch

**Status**: B-tier scalp active/triggered (partial TP hit this session). ETH C-tier in intraday/swing by score threshold. External catalyst confirmed and double-stacked.

**Dual catalyst**:
1. **Bitmine Holding** purchasing ETH (>$13.4M disclosed) — institutional accumulation
2. **ETH ETF 7-day cumulative inflows** positive

**DeFi advisory**: Summer.fi $6M exploit in ETH DeFi ecosystem. Not direct ETH protocol risk, but adversarial sentiment signal. Production risk flag: `exploit_hack` (advisory level).

**Technicals**: Price $1,793. Today's intraday low: $1,737 (proved support during gap-trap reversal). Clean pullback entry: $1,775–$1,790 (mid-range of recovery). ETH/BTC 0.0282 flat — catalyst-driven buying could decouple ratio.

**Risk**: DeFi exploit contagion (advisory, low probability fat tail). ETH underperforming BTC in rotation metrics. FOMC tomorrow macro overhead.

**Lifecycle action**: Set price alert at $1,775–1,790. Entry on reactive pullback with catalyst active. Reduce size ~20% vs standard: DeFi advisory + FOMC combined overhead.

---

## 7.4 — SYN/USDT · Short-Watch · Conditional Only

**Status**: C-tier swing (score ~50.8). No active B-tier signal. Category: downtrend, short candidate.

**Thesis**: −9.52% relative performance vs BTC (relative weakness leader). Price down + OI up = fresh short accumulation (bears adding, not covering). Potential: failed-bounce retest short entry at $0.39–0.40 if price rallies then rejects.

**Derivatives**: OI building into lower prices = bears in control, not a squeeze — opposite dynamic. Short side confirms relative weakness thesis.

**Risk**: Low volume (`low_confidence` playbook flag). No derivatives squeeze confirmation. If BTC breaks $64K, SYN could rally — wrong side risk. Intraday no-catalyst bucket NET NEGATIVE (−3R/14d).

**Lifecycle action**: SHORT WATCH ONLY. Entry requires all three simultaneously: (a) BTC fails $63K AND (b) SYN failed bounce confirmed at $0.39–0.40 AND (c) volume present. Low conviction — minimum size if all three triggered.

---

## 7.5 — VANRY/USDT · HARD AVOID · Critical External Risk

**Status**: Top RS leader in scalp report (+47.64%), score 63.9 (correctly C-tier due to overextension). Basket: `momentum_breakout / avoid_chase`.

**⚠ Critical external risk NOT captured in production system**:
- **Binance Monitoring Tag added July 3, 2026** — potential delisting warning
- Internal production risk layer does NOT flag this
- Confirmed via external research + prior review (18:40 EEST)

**Additional overextension risk**:
- +47.64% single session — price >2 ATR extended
- Short squeeze partially fired: $1.72M total liquidations, $1.15M shorts squeezed — move already happened
- Any entry at current price is chasing an exhausted move

**TLM parallel**: TLM confirmed Binance delisting monitoring (May 2026) in prior review. Same avoid logic applies — tournament catalyst (Alien Worlds) does not override delisting risk.

**Lifecycle verdict**: HARD AVOID. Fundamental delisting risk overrides all technical signals. Both VANRY and TLM require manual exclusion until Binance monitoring status officially cleared.

---

# §8 — BEST CANDIDATES RANKED

| Rank | Symbol | Mode | Lifecycle | Entry Trigger | Conf | Sizing |
|------|--------|------|-----------|--------------|------|--------|
| 1 | NEAR/USDT | Swing | WAITING FOR ENTRY | Reactive pullback to $2.03–2.05 | 62% | Standard −20% (FOMC) |
| 2 | ETH/USDT | Scalp/Swing | WAITING FOR ENTRY | Reactive pullback to $1,775–1,790 | 68% | Reduced −20% (DeFi+FOMC) |
| 3 | BEL/USDT | Swing | ENTERED / TP HIT | Monitor only — no new entry above TP | 55% | Monitor only |
| 4 | SYN/USDT | Swing Short | WATCHING | Failed bounce $0.39–0.40 + BTC fails $63K | 38% | Min size if triggered |
| — | XRP/USDT | Swing | NO ACTIVE SIGNAL | MiCA catalyst; wait for next cycle signal | — | Wait for signal |

**All rankings under WATCH_ONLY posture.** No entries at current prices. All triggers require price to come to the level.

---

# §9 — AVOID / NO TRADE

| Symbol | Reason | Source |
|--------|--------|--------|
| VANRY/USDT | **Binance Monitoring Tag July 3, 2026** — delisting risk; +47% overextended; `avoid_chase` basket | External confirmed + prior review |
| TLM/USDT | **Binance delisting monitoring May 2026** — not cleared; tournament catalyst does not override | External confirmed + prior review |
| MSFT | `legal_headline_risk: securities_fraud`; 4,800 layoffs + Xbox restructure | Stocks report + news |
| UNH | DOJ probe (−16% session); system rejected short (`both_index_and_sector_contradict`) | Stocks intraday report |
| ETH intraday (no-catalyst) | No-catalyst bucket −3R/14d NET NEGATIVE + DeFi exploit advisory | Playbook stats + catalyst events |
| HYPE/USDT | Direct `exploit_hack` production risk flag active | Catalyst events |
| APT/USDT | `token_unlock` dilution risk active | Catalyst events |
| Any stocks intraday A/B | Guards active: global −3.0R/7d, long −3.0R/7d — do not override | Stocks intraday report |
| New swing positions tonight | FOMC minutes July 8 tomorrow — macro event risk | Manual advisory |

---

# §10 — MAIN RISKS

**1. FOMC minutes July 8 (tomorrow, ~14:00 ET)**
Not in automated macro calendar. Manual advisory only. Any swing position opened tonight carries FOMC volatility exposure. Hard rule: no new swing entries tonight.

**2. BTC structural resistance $63,999**
BTC recovered from the gap-trap but faces the same structural resistance. Failure to break → potential retest of $61,307 (today's intraday low / proved support). All long positions depend on BTC clearing or holding this zone.

**3. DeFi contagion — Summer.fi $6M exploit**
ETH ecosystem adjacent. Low probability but fat-tail risk. ETH positions carry advisory at reduced sizing.

**4. Asia dead-zone activation (01:00 EEST / 23:00 UTC)**
Crypto scalp/intraday auto-demoted to C. Scalp/intraday positions entered tonight operate in lower liquidity. Config-driven, cannot be overridden.

**5. PART 1 regression — 18 untracked alerts**
Unknown gap between Telegram-pushed and tracked proposed_signals. Paper PnL tracking compromised for affected signals. Position sizing accountability blind spot.

**6. Stocks drawdown guard recovery timing**
Global guard at −3.0R/7d. 7-day rolling window takes time to reset even if tomorrow's session is bullish. Do not anticipate or trade in advance of guard reset.

**7. VANRY/TLM production risk gap**
Internal system does not flag Binance monitoring tags. Automated signals could be pushed to Telegram without override. Manual exclusion required until TODO-2 patched.

---

# §11 — ACTION PLAN (Next 4 Hours: 21:40–01:40 EEST)

| Time | Action | Priority |
|------|--------|----------|
| 21:40–22:00 | Set price alerts: NEAR $2.03–2.05, ETH $1,775–1,790, SYN $0.39 short | HIGH |
| 21:40–22:00 | Manually review NEEDS_REVIEW=1 paper monitor signal | HIGH |
| 22:00–23:00 | Monitor BTC vs $63,999: clean break → re-evaluate NEAR/ETH; rejection → chop confirmed | MEDIUM |
| 23:00 EEST | Asia dead-zone activates — no new scalp/intraday entries | HARD RULE |
| 23:00–01:00 | Swing entries only if price alerts hit AND BTC not in failure mode | CONDITIONAL |
| 01:00–05:00 | Asia dead-zone active — swing entries only (if alerts triggered, price came to zone) | RULE |
| Tomorrow pre-FOMC | No new swing positions; reduce/hedge existing before ~14:00 ET FOMC minutes | HARD RULE |

**No-do list**:
- Do NOT enter VANRY or TLM until monitoring status cleared
- Do NOT disable stocks drawdown guards
- Do NOT increase swing sizing ahead of FOMC
- Do NOT enter HYPE (direct `exploit_hack` active)
- Do NOT enter ETH intraday without catalyst context (no-catalyst bucket NET NEGATIVE)

---

# §12 — FINAL VERDICT PER MODE

| Mode | Verdict | Conf | Rationale |
|------|---------|------|-----------|
| Crypto Scalp | WATCH_ONLY → C (01:00 EEST) | 60% | Asia dead-zone activates soon; chop regime; no A/B signals at current prices |
| Crypto Intraday | WATCH_ONLY | 58% | Range/chop; no-catalyst bucket NET NEGATIVE; no A/B setups in current cycle |
| Crypto Swing | REDUCED SIZING — WATCH | 65% | Strongest mode (PF 5.80) but FOMC tomorrow caps new entries; NEAR/ETH reactive only |
| Stocks Intraday | BLOCKED BY GUARDS | — | All A/B demoted to C; 7d: −3.0R/PF 0.00; session closed; do not override guards |
| Stocks Swing/Growth | SHADOW ONLY | — | `stocks_swing_growth_breakout` shadow-only phase; not in proposed_signals |
| Paper Shadow B | NOT_READY | — | 11d window < 14d minimum; DATA_GAP_LATE 40%; 4/6 criteria; do not promote |

**Overall session verdict: WATCH_ONLY** — set alerts, no new positions at current prices; FOMC tomorrow

---

# §13 — SOURCES

**Internal data (cycle 7, 19:24–19:50 EEST)**:
- `data/scheduled_runs/2026-07-06_default_schedule/cycle_07_19-24_summary.md`
- `data/reports/scalp/2026-07-06_16-31_scalp_report.md` (2.2h old)
- `data/reports/intraday/2026-07-06_16-37_intraday_report.md` (2.1h old)
- `data/reports/swing/2026-07-06_14-19_swing_report.md` (4.4h old — carry-forward)
- `data/reports/stocks/intraday/2026-07-06_18-19_stocks_intraday_report.md` (0.4h — very fresh)
- `OPUS_ENRICHED_REVIEW_AUTO_2026-07-06_1840.md` (prior review — context)
- CLI `python -m src.cli active-signals --class crypto` (21:40 EEST)
- CLI `python -m src.cli active-signals --class stocks` (21:40 EEST)
- CLI `python -m src.cli signal-stats --class crypto` (21:40 EEST)
- CLI `python -m src.cli signal-stats --class stocks` (21:40 EEST)
- CLI `python -m src.cli detect_untracked_legacy_alerts` (21:40 EEST)

**External research** (supplemental):
- CoinGabbar: VANRY article (Neutron AI, channel breakout, $430.98M Binance vol) — monitoring tag context via prior review
- BTC macro context: June $4.5B ETF outflows, Citi target $82K, July 1 crash $58–60K, recovery to $63.4K
- BEL: WebSearch — no fundamental catalyst found; momentum/squeeze play only

---

# §14 — FIX REQUESTS / TODO

### TODO-1 · UNTRACKED-ALERTS · PART 1 REGRESSION · **P0 CRITICAL**
18 B-tier legacy alerts sent to Telegram today without matching proposed_signal entries (up from 11 at 18:40 — 7 more in cycle 7 alone). The proposed_signals table is diverging from Telegram push count cycle over cycle. Paper portfolio PnL tracking cannot be trusted for these 18 positions. Requires investigation of the `watchlist_alerts → proposed_signals` linkage in the cycle loop. Until fixed: all B-tier Telegram alert counts are unreliable.

### TODO-2 · MONITORING-TAG-FLAG · VANRY + TLM · **P1 HIGH**
- VANRY: Binance Monitoring Tag added July 3, 2026 — NOT captured in production risk layer
- TLM: Binance delisting monitoring active since May 2026 — NOT captured in production risk layer

Both are generating B/C tier signals without the monitoring override. Need a symbol-level flag in the risk layer that marks signals as AVOID when Binance monitoring status is active. Until patched: manual exclusion required for VANRY and TLM in all contexts.

### TODO-3 · ONCHAIN-CONFIG · MISSING · **P2 MEDIUM**
`config/onchain.yaml` is missing. System reports `interface_ready_config_missing`. Ingestion pipeline is built and ready, but no config exists — onchain data (wallet flows, exchange reserves, contract events) not flowing. Affects signal quality for onchain-sensitive assets (ETH, BTC, stablecoins).

### TODO-4 · DEAD-SOURCES · PERSISTENT · **P2 MEDIUM**
11 dead news sources confirmed in stocks intraday report: Business Wire, SEC EDGAR (CIK map partial fix but still DEAD), announcement TG channels. Tagged DEAD/DISABLED; absence reduces catalyst coverage. SEC EDGAR symbol audit: 17% match rate. Persistent across multiple cycles.

### TODO-5 · FOMC-MACRO-CALENDAR · NOT AUTOMATED · **P3 LOW**
FOMC minutes July 8 is NOT in the automated macro calendar. Significant market-moving event handled via manual advisory only. Requires automated macro event calendar with configurable signal suppression rules (e.g., no new swing entries within 6h of FOMC/NFP/CPI releases).
