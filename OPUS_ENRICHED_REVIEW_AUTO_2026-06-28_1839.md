# Opus Enriched Review — US Open Reaction Review — Auto Cycle 18:39 EEST

> **Advisory only / no auto-trade.** Today is **Sunday June 28, 2026** — US markets are closed. "US open reaction" slot runs as crypto-only weekend review. Stocks analysis is carry-forward planning for Monday June 29 RTH open (16:30 EEST).

---

## 1. Executive Summary

**Slot: US open reaction review (18:30 EEST) — advisory only / no auto-trade.**
Today is Sunday; US markets are closed. This review covers crypto weekend action only; stocks context is Monday planning.

**Crypto mood: risk-off / chop.** BTC ~$60,065 (F&G=13, Extreme Fear — worsened from F&G=18 this morning). Both BTC and ETH in downtrend. Altcoin breadth deteriorated intraday: 47% above EMA20 in swing report vs 59% in scalp — breadth weakening through the day. VIX=18.41, SPY/QQQ both down per dashboard.

**Key development since 16:20 review:** JTO/USDT surged **+31.8% in 24h** on confirmed catalyst — JTX consumer trading terminal launch (Jito Labs, July 2026) and KODA Korean institutional staking partnership. Strongest RS-leader move this weekend cycle. However, B signal entry zone is 0.840–0.850; current price ~$0.877 = **price moved ABOVE entry zone — do NOT chase**. Wait for pullback.

**PUMP token unlock risk identified (new):** July 12 (14 days), releasing 82.5B PUMP tokens ($121M, 9.7% supply) — this significantly undermines the swing long thesis. Avoid.

**What changed since 16:20:** Cycle 3 completed 17:07 EEST (29/29 steps ok); fresh swing report generated; 4–6 new B-tier swing signals issued (JTO long, BTC short, ZEC short, SYN long, ACT long, PUMP swing long). Signal count grew 13 → 17.

**Head Trader routing:** Preferred side = **shorts | catalyst-backed (after pullback)**. Best long-watch: JTO (pull back to $0.840–0.855 zone). Best short-watch: ZEC (B signal active, entry 391–393.5, fresh shorts building). Catalyst-watch: HYPE (Bitwise BHYP carry-forward). Avoid: PUMP (token unlock + below entry + regulatory risk). Weekend mode still active — demand retest, no chasing.

ALWAYS-SCAN continues. Scanner, scheduler, data collection, paper tracking all continue uninterrupted.

---

## 2. Data Used

| Source | File | Generated (EEST) | Age at 18:39 | Status |
|--------|------|-----------------|--------------|--------|
| Scheduler / autostart log | data/autostart/scheduler.log | 17:07 | 1.5h | **FRESH** |
| Latest cycle | cycle_03_15-56_summary.md | 17:07 | 1.5h | **FRESH** |
| Scalp report | 2026-06-28_13-20_scalp_report.md | 16:20 (data 13:00 UTC) | 2.3h | **FRESH** |
| Intraday crypto | 2026-06-28_13-44_intraday_report.md | 16:44 (data 13:30 UTC) | 1.9h | **FRESH** |
| Swing crypto | 2026-06-28_14-06_swing_report.md | 17:06 (data 14:00 UTC) | 1.6h | **FRESH** |
| Stocks intraday | 2026-06-26_20-14_stocks_intraday | 23:14 Jun 26 | ~43h | **STALE** — weekend closed |
| Stocks swing | 2026-06-26_15-06_stocks_swing | 18:06 Jun 26 | ~49h | **STALE** — weekend closed |
| Stocks invest | 2026-06-26_15-13_stocks_invest | 18:13 Jun 26 | ~49h | **STALE** — weekend closed |
| Catalyst events | data/catalysts/2026-06-28/ | 16:44 (cycle_13-44) | 2h | **FRESH** (315 events, 3 baskets) |
| LLM crypto packet | llm_analysis_packet.md | 17:06 | 1.6h | **FRESH** |
| LLM stocks packet | llm_stocks_packet.md | 23:14 Jun 26 | ~43h | **STALE** |
| Active signals (crypto) | CLI live 18:39 | live | live | 17 signals |
| Active signals (stocks) | CLI live 18:39 | live | live | 50 signals (all C-tier) |
| Signal-stats crypto | CLI live 18:39 | live | live | n=130, PF=1.45 |
| Signal-stats stocks | CLI live 18:39 | live | live | A/B n=24, PF=0.77 |
| External web | BTC/ETH/JTO/PUMP/SYN prices | live 18:39 | live | fetched via WebSearch |

> **Note:** External web research available and used this run. BTC/ETH current prices confirmed. JTO catalyst confirmed. PUMP unlock risk confirmed.

---

## 3. Scheduler / Data Freshness

- **Scheduler (autostart):** Last write 17:07 EEST (1.5h ago) — **FRESH** (threshold: 3h).
- **Latest cycle summary:** cycle_03_15-56 completed 17:07 EEST (1.5h ago) — **FRESH**.
- **Cycle 3 steps:** 29 ok / 0 failed. Monitor running (background pid=6512, 90-min window).
- **Paper accounting:** 1,796 signals refreshed, 0 errors. Paper structural TP/stop running.
- **Paper shadow A/B (forward only):** B +3.63R / A −19.8R (forward 3d, 90t B / 124t A). NOT_READY for promotion (5/6 criteria; window 3d < 14d minimum). B is outperforming forward.
- **Reddit social:** All 3 subreddits blocked (403). KOL watchlist: placeholder account only.
- **Onchain config:** MISSING (config/onchain.yaml) — onchain risk data unavailable.
- **Telegram notifier:** Paper-shadow digest error — `TelegramNotifier.__init__() missing config_path`. Main notifier operational for this review.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-06-28 18:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.88,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["onchain_config_missing", "reddit_social_blocked", "stocks_stale_weekend"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "scheduler.log mtime 17:07 EEST (1.5h)",
        "cycle_03 completed 17:07 (29 steps ok)",
        "crypto reports all <2.3h old",
        "stocks reports 43-49h old — weekend closed, acceptable",
        "Reddit 403 on all 3 subreddits",
        "onchain.yaml not configured"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.80,
      "reason_codes": ["risk_off", "chop", "shorts_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC downtrend (all reports), ETH downtrend",
        "BTC ~$60,065, F&G=13 (Extreme Fear, worsened from 18 this morning)",
        "Altcoin breadth 47% EMA20 swing (fell from 59% scalp — breadth deteriorating intraday)",
        "VIX=18.41, SPY down, QQQ down (dashboard snapshot cycle 3 step 15)",
        "Market regime: range/chop per all three reports",
        "BTC threatened 200-week MA (per scalp report macro note)",
        "ETH ETF outflows $12.85M; AI capital rotation narrative away from crypto"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["fresh_catalyst", "narrative_supported", "mapping_weak"],
      "data_missing": ["catalyst_mapping_weak"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "JTO: JTX consumer trading terminal launch (Jito Labs, July 2026) — confirmed",
        "JTO: KODA Korean custodian institutional staking partnership — confirmed",
        "JTO: +31.8% 24h surge, mktcap $427M",
        "PUMP: token unlock July 12 — 82.5B tokens, $121M, 9.7% supply",
        "PUMP: GO platform regulatory risk (Gov. Hochul comment)",
        "HYPE: Bitwise BHYP ETF live (NYSE + Deutsche Borse Xetra), 1.775M staked — carry-forward",
        "BTC: sub-$60K bearish headline, ETF outflow narrative",
        "UNH: DOJ criminal probe (stocks) — dual source confirmed",
        "Catalyst mapping: 95/315 mapped (30.2%) — 220 unmapped (69.8%) exceeds 50% threshold"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["oi_contradicts", "squeeze_risk", "data_unavailable"],
      "data_missing": ["derivatives_sparse", "onchain_config_missing"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "ACT: OI +277.9% (extreme), funding -0.02% (extreme negative), l/s 1.158 — very elevated crowding",
        "JTO: OI -1.01% (short covering after surge — squeeze likely exhausted), l/s 1.577",
        "ZEC: OI +4.15%, price down — fresh shorts pressing; squeeze risk if price reclaims",
        "SYN: OI -5.9% (short covering on upside move = weaker continuation quality)",
        "VELVET: elevated long crowding, funding 0.00066",
        "Intelligence: phase_5_post_unwind_chop=40 symbols; squeeze_expansion=3; build_up=11",
        "Funding/OI history noted as sparse in intelligence layer"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["chase_risk", "price_moved_away", "stale_before_entry", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "JTO: signal entry 0.840–0.850, current ~$0.877 — price ABOVE entry zone (moved away)",
        "PUMP: signal entry 0.001445–0.001465, current ~$0.001368 — price BELOW entry zone",
        "BTC short: signal entry 60,122–60,238, current ~$60,065 — price fell below entry",
        "SYN: signal entry 0.356–0.371, current ~$0.3704 — WITHIN zone but OI declining",
        "ZEC: signal entry 391–393.5 — price ~$385 below zone, needs bounce first",
        "Weekend mode active: require retest after impulse, tight stop warning",
        "No A-tier signals in any report this cycle",
        "TradingView chart MCP unavailable — using OHLCV/ATR from report fields only"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.78,
      "reason_codes": ["waiting_for_entry", "entered_unresolved", "no_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "17 active crypto signals (all B-tier, swing/intraday)",
        "WAITING FOR ENTRY (in zone): ZEC short, SYN long, ACT long",
        "NO-ENTRY / MOVED AWAY: JTO (above zone ~$0.877 vs 0.840–0.850), PUMP (below zone), BTC short (below zone)",
        "ENTERED UNRESOLVED (TP hit, remainder open): BEL tp1 (exp Jul4), AAVE tp1 (exp Jul4), SOL tp2 (exp Jul3), ETH short tp1 (exp Jul3), BTC-swing2 tp1 (exp Jun30), HOME tp2 (exp Jun29), ETH swing long tp2 (exp Jun29), MEGA tp1 (exp Jun26 STALE)",
        "STALE/EXPIRED: BTC intraday short (exp Jun27), HEI (exp Jun26), AXS (exp Jun27)",
        "50 stocks signals — all C-tier, closed Sunday, planning only",
        "Untracked legacy alerts: 0 (detector clean)"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["correlation_cluster", "headline_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Weekend mode: historical WR=18%, PF=0.80 on weekend=Y signals",
        "PUMP token unlock July 12: $121M supply release — systematic downside risk",
        "ACT extreme crowding (OI +278%) — do not enter despite trigger",
        "Correlation cluster: JTO + SYN + PUMP + SOL ecosystem (all Solana-adjacent)",
        "BTC <$60K macro: any BTC leg down invalidates all crypto longs simultaneously",
        "UNH DOJ probe — confirmed dual-source; stocks AVOID Monday open",
        "Stocks A/B: PF=0.77, -3R — losing playbook on stocks this cycle",
        "F&G=13 — capitulation risk or extended chop; ATR 39th percentile = low volatility"
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
        "Crypto swing: PF=2.07, +16R (n=42, strongest mode)",
        "Crypto intraday: PF=1.35, +7R (n=42, working)",
        "Crypto scalp: PF=0.00, -5R (n=46, avoid entirely)",
        "Shorts direction: PF=2.63, +13R (best direction)",
        "Cross-exchange signals: PF=2.27 vs Binance-only PF=0.70",
        "Weekend signals (Y): PF=0.80, -2R (underperform vs weekday PF=1.67)",
        "Stocks A/B headline: PF=0.77, winrate 17%, -3R (failing)",
        "Paper shadow B forward: +3.63R vs A -19.8R (3d window, not yet promotion-ready)"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.72,
      "preferred_side": "shorts",
      "best_long_candidate": {
        "symbol": "JTO/USDT",
        "trigger": "Pullback to 0.840–0.855 + 1h candle stability + volume acceptance",
        "reason": "Strongest catalyst this cycle (JTX launch confirmed, KODA partnership), +31.8%, but already above entry zone — wait for retest"
      },
      "best_short_candidate": {
        "symbol": "ZEC/USDT",
        "trigger": "Bounce to 391–393.5 + 1h rejection candle, stop above 396.4",
        "reason": "B signal triggered, fresh shorts building (OI +4.15%), negative catalyst (whale $4.9M short), downtrend alignment"
      },
      "best_catalyst_candidate": {
        "symbol": "HYPE/USDT",
        "trigger": "Pullback to $58–60 zone, basket playbook wait_pullback",
        "reason": "Bitwise BHYP ETF live, 1.775M staked ($114M), institutional demand structural carry-forward"
      },
      "avoid_candidate": {
        "symbol": "PUMP/USDT",
        "reason": "Token unlock July 12 ($121M, 9.7% supply), price below entry zone, GO platform regulatory risk"
      },
      "operator_action": "wait_for_trigger",
      "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
      "todo_count": 3,
      "suggested_effect": "advisory_only"
    }
  ]
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Key Reason Codes | Suggested Effect |
|-------|---------|-----------|-----------------|-----------------|
| data_quality | **ok** | 0.88 | scheduler_fresh, report_stale | advisory_only |
| market_regime | **caution** | 0.80 | risk_off, chop, shorts_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | **caution** | 0.65 | fresh_catalyst, narrative_supported, mapping_weak | advisory_only |
| derivatives_squeeze | **caution** | 0.55 | oi_contradicts, squeeze_risk, data_unavailable | advisory_only |
| technical_entry | **caution** | 0.65 | chase_risk, price_moved_away, clean_retest | advisory_only |
| execution_lifecycle | **ok** | 0.78 | waiting_for_entry, entered_unresolved, no_entry | advisory_only |
| risk_manager | **caution** | 0.72 | correlation_cluster, headline_risk, reduce_risk | advisory_only |
| playbook_performance | **ok** | 0.75 | playbook_working, playbook_failing | advisory_only |
| **head_trader** | **caution** | 0.72 | wait_for_trigger, shorts preferred | advisory_only |

---

## 4. What Changed vs Previous Review (16:20 EEST)

| Item | Previous (16:20) | Now (18:39) | Status |
|------|-----------------|------------|--------|
| Cycle | Cycle 2 (13:56) | Cycle 3 (17:07, 29/29 ok) | **Updated** |
| Signal count (crypto) | 12 | 17 | **+5 new swing signals** |
| F&G | 18 | 13 | **Worsened** |
| Altcoin breadth EMA20 | 59% (scalp) | 47% (swing) | **Deteriorated intraday** |
| New signals generated | — | JTO, BTC short, ZEC short, SYN, ACT, PUMP (swing) | **6 new B-tier** |
| JTO | Not highlighted | **+31.8% 24h confirmed, JTX launch catalyst** | **Major new finding** |
| PUMP | momentum-only watchlist | **Token unlock July 12 ($121M, 9.7%) — AVOID** | **Risk upgraded** |
| HYPE thesis | Catalyst long-watch valid | **Still valid, carry-forward** | Unchanged |
| ZEC | Short-watch (wait retest) | **B signal now live (entry 391–393.5)** | **Upgraded to active signal** |
| BTC price | ~$60,148 | ~$60,065 | Slight decline |
| Paper shadow | Digest error | B +3.63R / A −19.8R forward (3d) | Consistent |

**Confirmed:** ZEC short thesis valid, HYPE catalyst valid. ACT: still do NOT enter (OI extreme). **Invalidated:** None from 16:20 thesis.

---

## 5. Catalyst Coverage

> **⚠ CATALYST MAPPING WEAK THIS RUN — use catalyst layer as context, not final decision.**

- Total catalyst events (JSONL): **315**
- Mapped to specific symbols: **95** (30.2%)
- **Unmapped: 220 (69.8%)** — exceeds 50% warning threshold
- Narrative baskets: **3** (momentum_breakout, ai_narrative, delisting_thin_liquidity)
- High-importance unmapped symbols (integrity scan): ADA, ALGO, AVAX, COIN, DOT, FIL, HBAR, INJ, TON, TSLA (11 symbols with important news not resolved into catalyst_events)

**Top 3 unmapped headlines:**
1. [legal_risk] DOJ criminal probe into UnitedHealth extends to Optum Rx, physician reimbursement (Fierce Healthcare)
2. [legal_risk] UnitedHealth Faces DOJ Probe, Shares Dive 16% (QuiverQuant)
3. [partnership] Salesforce acquisition / "SaaSpocalypse" (Motley Fool)

**Active baskets:**
- `momentum_breakout` (fresh <1h): PUMP/USDT, SYN/USDT — pure momentum, no verified catalyst
- `ai_narrative` (fresh unknown): NEAR, RENDER, TAO, FET — AI sector rotation watch
- `delisting_thin_liquidity` (fresh <6h): no primary — avoid thin-market chasing

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** risk-off / chop (deteriorating — altcoin breadth fell 59% → 47% EMA20 intraday)
- **Stocks mood:** closed (Sunday) — Monday RTH planning only
- **Dominant narrative:** BTC sub-$60K bearish; AI capital rotation away from crypto; ETF outflows (ETH -$12.85M); Iran/Hormuz macro noise (neutral to BTC)
- **Preferred side now:** **shorts** and **catalyst-backed longs** (on pullback only — do not chase)
- **Best long candidate:** JTO/USDT — wait for pullback to $0.840–$0.855 zone; confirmed JTX catalyst
- **Best short candidate:** ZEC/USDT — B signal active, entry 391–393.5; needs bounce first
- **Best catalyst-backed candidate:** HYPE/USDT — Bitwise BHYP ETF carry-forward; pullback $58–60
- **What to avoid:** PUMP (token unlock July 12 + below entry), ACT (OI extreme +278%), scalp mode (PF=0.00)
- **What would change the view:** BTC reclaims $61,000+ on volume + breadth recovers above 60% → route to longs. BTC breaks $59,250 → short-only routing, reduce all long exposure.

---

## 7. Candidate Deep Dives

### Candidate 1: JTO/USDT — Best Catalyst Long-Watch

**Tier:** B swing long | **Lifecycle:** NO-ENTRY / MOVED ABOVE (price above entry zone) | **Score:** 65.7

- **Signal entry zone:** 0.840219–0.850244 | **SL:** 0.827966 | **Current price (web 18:39):** ~$0.877
- **Catalyst (externally confirmed):** JTX consumer trading terminal launch by Jito Labs (spot trading July 2026, perps/prediction markets later). KODA Korean custodian institutional staking partnership (opened regulated staking demand for JitoSOL). SOL Strategies ecosystem reserve with JTO as first token.
- **Price reaction:** YES — +31.8% surge moved price from entry zone to ~$0.877 (3% above top of entry zone). The signal was triggered at the right time; the question is whether price revisits.
- **Is setup chasing?** YES at $0.877. Entry zone is behind. Do not enter above $0.855.
- **Retest structure?** Not yet. Needs pullback to $0.840–0.855 to form one.
- **What level makes it actionable?** Pullback to $0.840–0.855 + 1h candle volume acceptance (not rejected at zone) → entry valid. Stop $0.828.
- **Derivatives note:** OI -1.01% on the surge = short covering (squeeze exhausted). L/S 1.577 (longs heavy after surge). If longs crowded, retracement more likely before next leg. Confirm OI stabilizes or builds before entry.
- **Mood alignment:** Partial — risk-off hurts beta alts, but JTO has institutional-grade catalyst differentiating it. Best single long idea this cycle.
- **Actionable now?** NO — lifecycle = NO-ENTRY / MOVED ABOVE. WAIT FOR TRIGGER.
- **Invalidation:** BTC breaks $59,250; JTX delayed officially; KODA partnership cancelled.

---

### Candidate 2: ZEC/USDT — Best Short-Watch

**Tier:** B swing short | **Lifecycle:** WAITING FOR ENTRY (needs bounce to zone) | **Score:** 67.2

- **Signal entry zone:** 391.007–393.453 | **SL:** 396.442 | **Current price (report 13:30 UTC):** ~$385.76
- **Catalysts (2 internal items):** (1) Coinbase CEO defending betting promotions vs Zcash founder criticism — narrative headwind for ZEC; (2) AMBCrypto whale: "Major whale shorts $4.92M in ZEC — Can Zcash rebound to $520?" — confirms institutional short positioning.
- **Price reaction:** YES — ZEC -6% 24h, -14.85% 7d, clear downtrend. Already moving in the short direction.
- **Chasing?** NO. Short entry requires price to BOUNCE UP to 391–393.5 first, then fail. Current price ~$385 is below zone.
- **Retest structure:** YES — price down + OI +4.15% = fresh shorts pressing. A relief bounce that fails at the entry zone is the trigger.
- **Entry now?** NOT until bounce to zone. WAITING FOR ENTRY.
- **What makes it actionable:** Bounce to 391–393.5 + 1h close rejection below 392 + volume confirmation → short entry. Stop above 396.4.
- **Targets:** TP1 ~$380, TP2 ~$375, TP3 ~$370. RR: ~1.84R to TP1 per report.
- **Squeeze risk:** If BTC surges and alts squeeze, ZEC could spike through 396 — hard stop is critical.
- **Mood alignment:** YES — risk-off, shorts preferred, relative weakness, negative catalyst.

---

### Candidate 3: SYN/USDT — Long Within Zone (Low Conviction)

**Tier:** B swing long | **Lifecycle:** WAITING FOR ENTRY (price within zone) | **Score:** 65.5

- **Signal entry zone:** 0.356402–0.371077 | **SL:** 0.338465 | **Current price (web):** ~$0.3704
- **Price is within the entry zone.** However, significant concerns:
- **Catalyst?** NONE verified. Pure momentum basket (SYN +11.4% 24h, +175.4% 7d). No fresh verified catalyst in internal data.
- **Derivatives:** OI -5.9% on price up = short covering (not fresh longs entering) — weaker continuation quality. Funding -0.00024 (slightly negative).
- **Playbook performance:** No-catalyst intraday in chop = 14d WR=23%, PF=0.70, -3R per playbook notes. This is a known negative expected-value bucket without catalyst.
- **7d +175% move:** Historically extended. A pullback retest would be cleaner but the signal is live at current zone.
- **Actionable?** LOW CONVICTION — within zone but no-catalyst + chop + weak derivatives = avoid absent a confirmed catalyst event.
- **WATCH TRIGGER:** Any confirmed news/listing/protocol event for SYN + price holds above $0.356 + volume expansion = upgrade to active entry.

---

### Candidate 4: HYPE/USDT — Catalyst Carry-Forward (No Active Signal)

**Tier:** C-watch (basket primary) | **Lifecycle:** NO ACTIVE SIGNAL — catalyst-only watch

- **Catalyst (externally confirmed, carry-forward from 16:20):** Bitwise BHYP spot ETF live on NYSE and Deutsche Borse Xetra. Bitwise deposited 1.775M HYPE (~$114M), staked entire amount via Bitwise Onchain Solutions (in-house staking). Not a one-time event — ongoing institutional demand.
- **Basket:** perps_dex_narrative (playbook: `wait_pullback`, primary: HYPE/USDT).
- **Actionable?** NOT until pullback to $58–60 zone. No active signal.
- **What makes it better:** Any price dip to $58–60 + volume acceptance + no broader risk-off cascade.
- **Invalidation:** BTC breaks $59,250 (cascade); BHYP AUM significant outflows; Bitwise unstakes position.
- **Sources (verified 16:20):** Bitwise BHYP ETF newsroom; Bitcoin.com Bitwise staking announcement (June 2026).

---

### Candidate 5: PUMP/USDT — AVOID

**Tier:** B swing long (signal) | **Lifecycle:** NO-ENTRY (price below entry zone) | **Score:** 68.1

- **Signal entry zone:** 0.001445–0.001465 | **Current price (web):** ~$0.001368 — price is BELOW the entry zone.
- **Token unlock (CRITICAL NEW RISK):** July 12, 2026 (14 days from now) — 82.5B PUMP tokens released: $73.47M Team + $47.75M Investor = $121M total (9.7% of total circulating supply). Signal window expires July 5 — any position held would be directly in front of this unlock.
- **Platform risk:** "GO" viral bounty platform facing regulatory scrutiny (Governor Hochul "dystopian model" comment, potential regulatory action).
- **Buyback note:** $254.93M in buybacks (-19.98% supply) = positive but insufficient to offset the $121M scheduled unlock.
- **VERDICT: DO NOT ENTER.** Price below entry zone + $121M unlock in 14 days + regulatory risk = negative asymmetry. Do not re-enter even if price bounces into zone.

---

## 8. Best Candidates Ranked

| Rank | Symbol | Direction | Mode | Lifecycle | Conviction | Action |
|------|--------|-----------|------|-----------|-----------|--------|
| 1 | ZEC/USDT | Short | Swing | WAITING FOR ENTRY | Medium | Watch — needs bounce to 391–393.5, then short rejection |
| 2 | JTO/USDT | Long | Swing | NO-ENTRY/MOVED ABOVE | High (catalyst) | Watch — pullback to $0.840–$0.855 required |
| 3 | HYPE/USDT | Long | Catalyst | NO SIGNAL | Medium | Watch — pullback to $58–60 zone |
| 4 | SYN/USDT | Long | Swing | WAITING FOR ENTRY | Low | Watchlist only — no catalyst, chop = negative bucket |
| 5 | BTC/USDT short | Short | Swing | WAITING/BELOW ZONE | Low-Medium | Watch — needs bounce to 60,122–60,238 |

**No clean immediate entry this window. All top candidates require specific price trigger.**

- **Best long-watch:** JTO/USDT — trigger: pullback to $0.840–$0.855 + 1h candle volume acceptance
- **Best short-watch:** ZEC/USDT — trigger: bounce to 391–393.5 + 1h rejection candle, stop 396.4
- **Best catalyst-watch:** HYPE/USDT — trigger: pullback to $58–60, basket: wait_pullback

---

## 9. Avoid / No Trade (this decision window only)

- **PUMP/USDT:** Token unlock July 12 ($121M, 9.7% supply), below entry, regulatory risk — **AVOID absolutely**
- **ACT/USDT:** Extreme OI crowding (+277.9%), extended +84% move — **AVOID despite triggered signal**
- **Scalp mode:** PF=0.00, -5R — **AVOID entirely**
- **Weekend no-catalyst intraday:** Known -3R bucket (WR=23%, PF=0.70) — demand catalyst or defer
- **Any stock intraday today:** Markets closed (Sunday) — planning only
- **UNH (Monday open):** DOJ criminal probe confirmed dual-source — **AVOID on Monday RTH open**

This is a decision-window routing verdict. Scanner continues. Candidate generation continues. Paper tracking continues. System does not stop.

---

## 10. Main Risks

1. **BTC breakdown below $59,250** — cascade risk for all crypto longs; route to short-only immediately
2. **PUMP token unlock July 12** ($121M, 9.7% supply) — systematic supply overhang; avoid all PUMP longs
3. **ACT OI extreme crowding** (+278%) — if ACT reverses, Solana-adjacent alts (JTO/SYN/PUMP) could face correlation liquidation
4. **Weekend liquidity** — thin markets amplify wicks; weekend signals PF=0.80 historically
5. **Catalyst mapping weak** (69.8% unmapped) — COIN, DOT, TON, TSLA news may be missed; verify manually for relevant symbols
6. **Telegram notifier config error** — paper-shadow digest not delivered (config_path missing)
7. **JTO chase risk** — entering above $0.855 after +31.8% surge carries significant momentum-reversal risk

---

## 11. Action Plan — Next 4 Hours

| Priority | Action | Condition | Symbol |
|----------|--------|-----------|--------|
| 1 | Monitor ZEC bounce | Price reaches 391–393.5 | ZEC short |
| 2 | Monitor JTO pullback | Price returns to 0.840–0.855 | JTO long |
| 3 | Monitor HYPE | Price reaches $58–60 | HYPE catalyst-watch |
| 4 | Watch BTC key level | Break below $59,250 → route to short-only | BTC |
| 5 | Confirm PUMP avoidance | Do not enter regardless of price action | PUMP |
| 6 | Monday stock planning | UNH = avoid; AMD/JPM/UNH swing signals need 15–30 min RTH confirmation before entry | Stocks |

Crypto swing mode best (PF=2.07). Intraday acceptable with confirmation. Scalp avoid. Weekend: demand retest.

---

## 12. Final Verdict per Mode

| Mode | Verdict | Rationale |
|------|---------|-----------|
| Crypto swing | **WATCH_FOR_TRIGGER** | PF=2.07, +16R (best mode). 2 good candidates (ZEC short, JTO long) both need price trigger first |
| Crypto intraday | **CAUTION** | PF=1.35, working but chop + weekend = require catalyst or breakout confirmation |
| Crypto scalp | **AVOID** | PF=0.00, -5R. No A/B scalp setups. Do not trade scalp. |
| Stocks intraday | **CLOSED** | Sunday — planning only; Monday needs 15–30 min RTH wait |
| Stocks swing | **PLANNING** | Stale 48h, weekend. Monday watchlist: avoid UNH; AMD/JPM potential if RTH confirms |
| Stocks invest | **PLANNING** | C-tier only, low confidence, stale data |

---

## 13. Sources

- [Bitcoin/ETH prices today — Yahoo Finance (Jun 25–28 2026)](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-thursday-june-25-2026-bitcoin-hits-its-lowest-levels-in-years-125308371.html) — BTC ~$60,065, ETH ~$1,580
- [Jito JTO news — Bitget](https://www.bitget.com/price/jito/news) — JTX terminal launch, KODA partnership (June 2026)
- [Jito JTO CMC analysis](https://coinmarketcap.com/cmc-ai/jito/latest-updates/) — +31.8% 24h confirmed, mktcap $427M
- [Pump.fun token unlock — CMC](https://coinmarketcap.com/cmc-ai/pump-fun/latest-updates/) — July 12 unlock $121M (9.7% supply)
- [Pump.fun price — CoinGecko](https://www.coingecko.com/en/coins/pump-fun) — current ~$0.001368
- [Synapse SYN price — CMC](https://coinmarketcap.com/currencies/synapse-2/) — $0.3704, +4.51% 24h (Jun 28 2026)
- Internal: `data/reports/swing/2026-06-28_14-06_swing_report.md`
- Internal: `data/reports/intraday/2026-06-28_13-44_intraday_report.md`
- Internal: `data/reports/scalp/2026-06-28_13-20_scalp_report.md`
- Internal: `data/scheduled_runs/2026-06-28_default_schedule/cycle_03_15-56_summary.md`
- Internal: `data/catalysts/2026-06-28/catalyst_cycle_13-44.md`
- Internal: CLI `active-signals`, `signal-stats` (live 18:39 EEST)
- UNH DOJ probe — catalogued in `catalyst_events.jsonl`: Fierce Healthcare + QuiverQuant (Jun 28 2026)

---

## 14. Fix Requests / TODO

### TODO-pump-unlock-signal-risk
- **issue:** PUMP/USDT B swing long signal is active (entry 0.001445–0.001465, expires Jul 5), but a $121M token unlock occurs July 12 (9.7% supply, 14 days). Signal validity window expires just 1 week before the unlock, creating direct exposure risk. Signal scoring does not account for upcoming unlock risk.
- **evidence:** CMC unlock data (Jun 28 2026); `active-signals` output showing PUMP swing long (weekend=Y, exp Jul 5); signal vs unlock timeline overlap.
- **suggested manual fix:** Review whether scoring should integrate tokenomist/unlock calendar as a negative catalyst modifier. Consider rejecting or downgrading signals where >5% supply unlock occurs within 21 days of signal entry.
- **priority:** medium
- **first observed:** 2026-06-28 18:39 EEST

### TODO-catalyst-mapping-weak-recurring
- **issue:** Catalyst mapping at 30.2% (95/315 mapped), 69.8% unmapped — above 50% warning threshold. 11 high-importance symbol-tagged catalysts (ADA, ALGO, AVAX, COIN, DOT, FIL, HBAR, INJ, TON, TSLA) not resolved into catalyst_events. Appears in multiple runs.
- **evidence:** `data/catalysts/2026-06-28/catalyst_cycle_13-44.md` — integrity scan WARNING; direct JSONL count 315 total / 95 with symbol.
- **suggested manual fix:** Audit symbol resolver in catalyst layer; expand ticker-to-symbol mapping table for COIN, DOT, TON, TSLA, ADA. Investigate why high-importance tagged symbols are not being resolved.
- **priority:** medium
- **first observed:** 2026-06-28 18:39 EEST (recurring)

### TODO-telegram-notifier-config-path
- **issue:** Paper-shadow A/B Telegram digest fails with `TelegramNotifier.__init__() missing 1 required positional argument: 'config_path'`. Daily digest not delivered.
- **evidence:** `cycle_03_15-56_summary.md` step 14: "send error: TelegramNotifier.__init__() missing 1 required positional argument: 'config_path'"
- **suggested manual fix:** Inspect paper-shadow telegram digest invocation; pass config_path argument or default it from project config path. Verify scheduler call uses correct signature.
- **priority:** low
- **first observed:** 2026-06-28 18:39 EEST
