# Opus Enriched Review — Late-Session Risk Review — Auto Cycle 21:40 EEST

_Generated 2026-06-23 21:40 EEST (Tuesday). Advisory only. No auto-trade. Scanner / collection / tracking continue in all moods._

---

## 1. Executive Summary

**Tue 2026-06-23, 21:40 EEST — Late-Session Risk Review — advisory only / no auto-trade.**

- **SLOT: Late-session risk review.** ~80 minutes to US cash close (23:00 EEST / 16:00 ET).
- **Crypto: RISK-OFF persists.** BTC ~$62,415 (−3.3%), ETH ~$1,657 (−4.7%). Both in confirmed downtrends. Altcoin breadth 20.9% above EMA20 — deteriorating vs prior sessions. Rate-hike expectations cited as structural headwind.
- **Stocks: Semiconductor selloff deepening.** S&P 500 −1.04%, Nasdaq −2.67%, SOX −7.3%, MU −10.6%, AMD −8.7%, INTC −6.2%. KOSPI triggered circuit breaker (−9.99%). Dow essentially flat (+0.02%). Financials (JPM) holding.
- **Open ACTIONABLE signals:** SMH short B (within entry zone $625.62 vs zone $623–628), JPM long B (+0.4%), TSLA short B (triggered), BTC swing short B, ENA swing+intraday short B (x2).
- **Late-session risk flags:** 80 min to US close → DO NOT open fresh intraday positions. Maintain existing triggered signals with stops in place. AMD swing long B is COUNTER-REGIME — DO NOT ENTER.
- **Untracked alert integrity flag:** 2 ETH swing short alerts sent to Telegram without backing proposed_signal (14:35 UTC, 16:05 UTC). ETH swing short is WAITING, not yet triggered.
- **Playbook health (critical):** Crypto intraday 0W/10L PF 0.00, −10R this week. Stocks B-tier intraday 0W/6L PF 0.00, −6R (n=15, weak sample). Crypto swing is the ONLY profitable mode (PF 1.57, +12R). Weight swing; avoid new intraday signals.
- **Avoid (confirmed):** UNH (DOJ Medicare probe confirmed), SMCI (export-control indictment confirmed).
- **Overnight setup:** BTC/ENA/ETH (if triggers) swing shorts can run overnight into Asia. Avoid new scalp/intraday entries after 22:00 EEST.

---

## 2. Data Used

| Source | File / Path | mtime EEST | Freshness |
|---|---|---|---|
| Latest cycle | `data/scheduled_runs/2026-06-23_default_schedule/cycle_06_19-21_summary.md` | 19:38 | **FRESH** (2h2m) |
| scheduler.log | not found at default path | — | **MISSING** (cycle file used as proxy) |
| Crypto scalp report | `data/reports/scalp/2026-06-23_16-28_scalp_report.md` | 19:28 | **FRESH** (2h12m) |
| Crypto intraday report | `data/reports/intraday/2026-06-23_16-33_intraday_report.md` | 19:33 | **FRESH** (2h7m) |
| Crypto swing report | `data/reports/swing/2026-06-23_14-15_swing_report.md` | 17:15 | **CARRY-FORWARD** (4h25m) |
| Stocks intraday | `data/reports/stocks/intraday/2026-06-23_18-17_stocks_intraday_report.md` | 21:17 | **VERY FRESH** (23m) |
| Stocks swing | `data/reports/stocks/swing/2026-06-23_14-18_stocks_swing_report.md` | 17:18 | **CARRY-FORWARD** (4h22m; watchlist-only) |
| Stocks invest | `data/reports/stocks/invest/2026-06-23_14-20_stocks_invest_report.md` | 17:20 | **CARRY-FORWARD** (4h20m) |
| LLM analysis packet | `data/processed/llm_analysis_packet.md` | 16:33 UTC | **CARRY-FORWARD** |
| Catalyst events | `data/catalysts/2026-06-23/catalyst_events.jsonl` | cycle 06 | **FRESH** |
| Narrative baskets | `data/catalysts/2026-06-23/narrative_baskets.jsonl` | cycle 06 | **FRESH** |
| Active-signals CLI | crypto (25) + stocks (50) | 21:40 | **LIVE** |
| Signal-stats CLI | crypto + stocks | 21:40 | **LIVE** |
| Untracked alerts | `detect_untracked_legacy_alerts` | 21:40 | **LIVE — 2 untracked** |
| Prior review | `OPUS_ENRICHED_REVIEW_AUTO_2026-06-23_1839.md` | 18:54 | 2h46m ago |
| BTC/ETH price | WebSearch (Yahoo Finance) | 21:40 | **FRESH** (single_source) |
| Stocks late session | WebSearch + WebFetch (ts2.tech) | 21:40 | **FRESH** (single_source) |

**External web research: partially available.** Yahoo Finance (BTC/ETH confirmed), ts2.tech (stocks late session confirmed). TheStreet and CryptoNews returned 403 on WebFetch — URL confirmed from search results only, treating as single_source unverified fetch.

**Blindspots:** scheduler.log missing from default path (cycle summary used as proxy). Reddit social blocked. Liquidation heatmaps / order book / onchain config missing. ETF flows internal only. TradingView chart MCP unavailable.

---

## 3. Scheduler / Data Freshness

- `scheduler.log`: **NOT FOUND** at `data/logs/scheduler.log`. Using cycle summary as proxy.
- Latest cycle `cycle_06_19-21_summary.md` mtime: **19:38 EEST** (2h2m ago) — within 3h threshold.
- Cycle 06 (19:21–19:38): ok=22 steps, failed=0. Track-signals pass: checked=453, updated=31, tp_hits=279, stopped=2, expired=0.
- **NOT DEFERRED** — cycle freshness within 3h threshold.
- Monitor status: not directly confirmed this slot (log file missing); presumed running from prior review confirmation at 18:39.

> **TODO:** scheduler.log not at `data/logs/scheduler.log`. Prior review found it; may have been a path lookup issue. See §14.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-06-23 21:40 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.73,
      "reason_codes": ["scheduler_fresh", "report_stale", "packet_missing"],
      "data_missing": ["scheduler_log_missing", "social_attention_absent", "onchain_config_missing", "liquidation_heatmap_unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "cycle_06 mtime 19:38 EEST = 2h2m ago, within 3h threshold",
        "stocks intraday report very fresh: 21:17 EEST (23m ago)",
        "scalp/intraday crypto fresh: 19:28/19:33 EEST (~2h)",
        "swing carry-forward: 17:15 EEST (4h25m)",
        "scheduler.log not found at data/logs/scheduler.log",
        "Reddit social 403 blocked all cycle",
        "no config/onchain.yaml (onchain features disabled)"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.84,
      "reason_codes": ["risk_off", "shorts_preferred", "mixed"],
      "data_missing": ["live_vix_feed", "social_sentiment_absent"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC downtrend: $62,415 -3.3% (Yahoo Finance confirmed)",
        "ETH downtrend: $1,657 -4.7%",
        "altcoin breadth 20.9% above EMA20 (very weak)",
        "S&P 500 -1.04%, Nasdaq -2.67%, SOX -7.3%",
        "KOSPI -9.99% circuit breaker (semiconductor panic)",
        "VIX 18.79 (elevated but not extreme)",
        "IWM/DIA uptrend (small-caps/Dow resilient)",
        "Financials XLF/JPM holding vs tech selloff",
        "Crypto macro bias: rate-hike expectations = structural headwind"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.76,
      "reason_codes": ["fresh_catalyst", "catalyst_confirmed", "narrative_supported", "mapping_weak"],
      "data_missing": ["social_attention_absent", "unmapped_ratio_unquantified"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "559 catalyst events today, 6 narrative baskets",
        "KOSPI -9.99% chip rout confirmed (primary driver of tech selloff)",
        "$2.5B ETF outflows BTC/ETH (CryptoSlate, single_source)",
        "ETH Foundation 20% staff cuts (CryptoBriefing)",
        "UNH DOJ probe confirmed (QuiverQuant)",
        "SMCI export-control indictment confirmed (SEC EDGAR)",
        "LINK Project Pangea (EUR-KRW FX settlement) = positive but no price breakout",
        "XRP Ripple MiCA preliminary approval = positive",
        "Digital Asset Clarity Act: Senate path uncertain",
        "Majority of 559 events estimated basket/unmapped — mapping likely weak"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "ok",
      "confidence": 0.67,
      "reason_codes": ["unwind", "post_unwind_chop", "data_unavailable"],
      "data_missing": ["liquidation_heatmap_unavailable", "onchain_flow_unavailable", "oi_partial_bybit"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "ENA: price down + OI down = deleveraging, no squeeze risk for shorts",
        "WLD: price down + OI down = deleveraging",
        "BTC: price down + OI tracked by cycle (swing B triggered = positioning confirmed)",
        "DOT/INJ/NEAR: price down + OI UP (fresh shorts pressing) — squeeze possible if BTC reclaims; watch closely",
        "DEXE: price UP + OI UP, elevated long crowding (flush risk on reversal)",
        "XLM swing short: OI +1.73% with price down — fresh shorts pressing",
        "No liquidation heatmap data available"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.74,
      "reason_codes": ["entry_late", "chase_risk", "stale_before_entry"],
      "data_missing": ["chart_mcp_unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "21:40 EEST = 14:40 ET — 80 min to US close: too late for new intraday entries",
        "SMH $625.62 within entry zone $623-628 (already triggered — MAINTAIN, not new entry)",
        "JPM +0.4% — triggered at $333-334, TP1=$337.69, SL=$330.80; if above $335 do not add",
        "ENA already down -9.3% 24h before crypto entry triggers (overextended?)",
        "BTC swing short: swing horizon = entry timing less critical, can maintain overnight",
        "ETH swing short: WAITING, entry not yet triggered, cleaner entry available vs chasing",
        "TradingView / manual chart check unavailable"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.81,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "OPEN ACTIONABLE crypto: BTC swing short B (triggered), ENA swing short B (triggered), ENA intraday short B (triggered)",
        "OPEN ACTIONABLE stocks: JPM B intraday long (triggered), SMH B intraday short (triggered), TSLA B intraday short (triggered)",
        "WAITING for entry crypto: ZEC swing short B, WLD swing short B, NEAR swing short B, XLM intraday short B, ETH swing short B",
        "CLOSED WIN (TP hit) crypto: 15+ signals showing tp1_hit (HOV, ETH swing long, TNS, AXS, MEZ, FIL, WLD swing long, SOL, NIX, NEAR swing long, BAND, MEZ, TAO, BAND2, ATO)",
        "CLOSED WIN stocks C-tier: QQQ short C, AVGO short C, GOOGL short C, LLY short C all TP hit",
        "NEEDS REVIEW: ETH/USDT B swing short — 2 Telegram alerts (14:35 UTC, 16:05 UTC) without backing proposed_signal",
        "UNH WAITING signals: AVOID due to confirmed DOJ legal risk"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.83,
      "reason_codes": ["legal_risk", "headline_risk", "correlation_cluster", "late_session_risk"],
      "data_missing": ["daily_loss_tracking_unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "SMCI: export-control indictment (SDNY) confirmed — AVOID all directions",
        "UNH: DOJ Medicare fraud investigation confirmed, -16% dive — AVOID all directions",
        "AMD swing B long: counter-regime with SOX -7.3% on same session — DO NOT ENTER",
        "SMH swing B long (carry-forward): same — DO NOT ENTER (also watchlist-only per audit)",
        "Crypto: 3 simultaneous open shorts (BTC/ENA x2) = correlation cluster (if BTC squeezes, all break)",
        "DOT/INJ/NEAR OI rising with price down = latent short squeeze exposure in watchlist",
        "Stocks B-tier intraday: 0W/6L PF 0.00 this week (n=15, weak but signal) — reduce aggression",
        "80 min to US close: new intraday positions inadvisable",
        "Crypto intraday PF 0.00, -10R this week — weight swing signals only"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.77,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample", "missed_winner"],
      "data_missing": ["daily_granularity_unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto swing: n=43, PF 1.57, +12R — ONLY profitable crypto mode this week",
        "Crypto intraday: n=72, 0W/10L, PF 0.00, -10R — catastrophically losing",
        "Crypto scalp: n=63, 10W/39L, PF 0.56, -17R — losing",
        "Crypto shorts direction: n=146, PF 0.73, -16R — structurally losing at scale",
        "Crypto longs direction: n=32, PF 1.17, +1R — slightly positive",
        "Stocks B-tier intraday: n=15, 0W/6L, PF 0.00, -6R — weak sample, early-week losses",
        "Stocks C-tier: n=178, PF 0.647, -8R — also losing",
        "Stocks SHORTS direction: n=56, 7W/5L, PF 1.80, +4R — PROFITABLE bucket",
        "Stocks LONGS direction: n=137, 2W/20L, PF 0.10, -18R — catastrophically bad",
        "C-tier stocks shorts today: QQQ/AVGO/GOOGL/LLY all TP hit — validates short bias"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.78,
      "reason_codes": ["shorts_preferred", "wait_for_trigger", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Chip selloff persistent into late US session — SMH short B holding in entry zone",
        "Financials divergence: JPM +0.4% = clean relative strength long",
        "Crypto swing shorts profitable mode; ENA/BTC open tracking",
        "ETH swing short waiting; 2 untracked alerts = pipeline integrity issue",
        "Late session: 80 min to close — no new intraday entries; maintain open signals",
        "Stocks longs structurally losing (-18R, n=137); JPM exception via RS+catalyst",
        "AMD swing long B: counter-regime AVOID regardless of score",
        "Overnight: BTC/ETH/ENA swing shorts can continue; check Asia open at 04:30 slot"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.78,
    "preferred_side": "shorts",
    "best_long_candidate": {
      "symbol": "JPM",
      "trigger": "Already triggered; hold if above $332 with SL $330.80; TP1 $337.69 requires 80-min window",
      "reason": "Financials RS leader vs chip rout; uptrend; B-tier triggered; exceptions justify the long despite structurally-losing stocks-long bucket"
    },
    "best_short_candidate": {
      "symbol": "SMH",
      "trigger": "Already triggered at $625.62 (within $623-628 zone); maintain short with SL $636.89; TP1 $609.88",
      "reason": "Catalyst-backed chip selloff (KOSPI -10%, SOX -7.3%); B-tier score 73.07; within entry zone; stocks shorts bucket profitable (PF 1.80)"
    },
    "best_catalyst_candidate": {
      "symbol": "SMH",
      "trigger": "Semiconductor selloff primary catalyst (KOSPI circuit breaker, NVIDIA/AMD/MU multi-session declines)",
      "reason": "Clearest single-stock/ETF narrative with confirmed external catalyst and technical alignment"
    },
    "avoid_candidate": {
      "symbol": "AMD",
      "reason": "B-tier swing long counter-regime (SOX -7.3% session); swing watchlist-only per -12R audit; structurally dangerous entry during chip rout"
    },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.73 | scheduler_fresh, report_stale, packet_missing | advisory_only |
| market_regime | caution | 0.84 | risk_off, shorts_preferred, mixed | advisory_only |
| catalyst_narrative | caution | 0.76 | fresh_catalyst, catalyst_confirmed, mapping_weak | advisory_only |
| derivatives_squeeze | ok | 0.67 | unwind, post_unwind_chop, data_unavailable | advisory_only |
| technical_entry | caution | 0.74 | entry_late, chase_risk, stale_before_entry | advisory_only |
| execution_lifecycle | ok | 0.81 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.83 | legal_risk, headline_risk, correlation_cluster, late_session_risk | advisory_only |
| playbook_performance | caution | 0.77 | playbook_working (swing), playbook_failing (intraday/scalp), low_sample | advisory_only |
| head_trader | caution | 0.78 | shorts_preferred, wait_for_trigger, manual_review | advisory_only |

---

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-23_1839.md` (18:39 EEST, ~3h ago).

| Category | 18:39 State | 21:40 State |
|---|---|---|
| BTC price | ~$62,249 | ~$62,415 (+0.3% — minor bounce/consolidation) |
| ETH price | ~$1,654 | ~$1,657 (+0.2% — consolidating) |
| SMH session move | −6.5% (early) | −6.5% (persistent, late) — within entry zone |
| JPM | +0.4% (confirmed trigger) | +0.4% (holding) |
| Untracked ETH alerts | 1 alert | **2 alerts** (+1 at 16:05 UTC) |
| Active crypto signals | 29 | **25** (some expired/TP'd) |
| Active stocks signals | 50 | 50 |
| Crypto swing stats | PF 1.50, +11R | PF 1.57, +12R (improved) |
| Cycle | 05 (16:53–17:21) | **06** (19:21–19:38) completed |
| Stocks intraday report | 15:37 UTC | **18:17 UTC** (new, very fresh) |
| New B-tier crypto signals | ENA/NEAR/ZEC/XLM shorts | **No new A/B crypto** in cycle 06 |
| Stocks C-tier TP hits | Not reported | QQQ/AVGO/GOOGL/LLY shorts all TP hit |
| ETH swing short | WAITING | **Still WAITING** (no trigger, 2 untracked alerts) |

**Key delta:** BTC/ETH stabilizing slightly above session lows; no reversal. New stocks intraday report (21:17 EEST) confirms JPM B long and SMH B short remain intact. Cycle 06 added no new crypto A/B signals. Semiconductor selloff is persistent and confirmed into late session. Stocks shorts bucket validated (4 C-tier shorts TP'd today).

---

## 5. Catalyst Coverage

- Total events today: **559**
- Narrative baskets: **6** (delisting_thin_liquidity, perps_dex_narrative, rwa_narrative, ai_narrative, binance_ecosystem_teaser, and 1 unresolved)
- Symbol-mapped events visible in reports: ~12–15 (SMCI, UNH, ETH, BTC, SOL, ADA, LINK, XRP, ENA, HYPE, WLD, BNB)
- Unmapped (basket) events: estimated majority of 559 (precise ratio requires JSONL query — not run this slot)

> **⚠️ Catalyst mapping likely weak this run — use catalyst layer as context, not final decision.** Unmapped ratio estimated >50% based on visible symbol-mapped count vs 559 total. Precise count unavailable without JSONL query.

**Top 3 unmapped/basket headlines:**
1. `[exploit_hack]` THORChain resumes trading 5 weeks after $10.7M exploit (The Block / Cointelegraph)
2. `[regulatory_sector_headline]` Digital Asset Market Clarity Act faces tight Senate negotiations before August recess (CryptoBriefing)
3. `[exchange_listing]` Binance Futures to launch USDⓈ-margined TradFi perpetual contracts 2026-06-29

**Key symbol-mapped notable events:**
- **SMCI**: legal_risk — export-control conspiracy indictment (SEC EDGAR filing) → **AVOID**
- **UNH**: legal_risk — DOJ Medicare fraud probe, stock −16% (QuiverQuant) → **AVOID**
- **LINK**: positive — Project Pangea EUR-KRW FX settlement (Cointelegraph, CryptoBriefing)
- **ETH**: negative — Foundation 20% staff cuts, leadership exodus (CryptoBriefing)
- **BTC/ETH**: negative — $2.5B ETF outflows (CryptoSlate, single_source)

---

## 6. Market Landscape

### Market Mood / Risk Routing

**DRIVEN BY: Agent Council `market_regime` (verdict: caution / risk_off) + `risk_manager` (caution)**

- **Crypto mood:** `risk-off` — BTC and ETH both in confirmed downtrends; altcoin breadth 20.9% above EMA20 (very weak); rate-hike expectations; $2.5B ETF outflows; ETH Foundation staff cuts are structural negatives.
- **Stocks mood:** `risk-off (tech) / mixed` — Nasdaq −2.67%, SOX −7.3%; S&P −1.04%. Financials (XLF/JPM) diverging positively. Dow +0.02%. Small-caps (IWM) uptrend. Regime label: **chop trending risk-off**.
- **Dominant narrative:** Global semiconductor selloff triggered by KOSPI crash (−9.99% circuit breaker). AI sustainability concerns. Rate-hike expectations weighing on growth assets.
- **Preferred side now:** `shorts` (tech/semis/crypto) + selective financials long (JPM only, with active signal)
- **Best long candidate:** JPM — already OPEN ACTIONABLE, triggered at $333–334, holding +0.4%. Financials RS leader vs tech. 80 min window; maintain, do not chase above $335.
- **Best short candidate:** SMH — OPEN ACTIONABLE, triggered, $625.62 within zone $623–628. Catalyst-backed chip rout. TP1 $609.88. Stocks shorts bucket PF 1.80 (+4R) this week.
- **Best catalyst-backed candidate:** SMH (chip selloff) or ENA crypto swing short (B-tier triggered, deleveraging confirmed).
- **What to avoid:** AMD swing long B (counter-regime chip rout); UNH any direction (DOJ legal); SMCI any direction (indictment); new intraday entries with 80 min to close.
- **What would change the view:** BTC reclaim above $64,500; SOX reversal >+3%; VIX collapse <16; ETH reclaim above $1,750. None of these are present — maintain caution/short bias.

---

## 7. Candidate Deep Dives (≤5)

### Candidate 1 — SMH Short (B-tier, stocks intraday) — OPEN ACTIONABLE

**Status:** OPEN ACTIONABLE (triggered, within entry zone)
**Score:** 73.07/100 | Confidence: medium | Mode: intraday | Direction: short

**Price reaction / chase check:**
- SMH ~$625.62 at late session (−6.5% for the day from ~$668 open area).
- Entry zone: $623.39–$627.89. Price is squarely inside this zone.
- This is NOT a new entry situation — signal was triggered earlier in the session. If already in: maintain.
- **Is this chasing?** No — signal was triggered within the entry zone. The move is large for the session but driven by a confirmed catalyst (KOSPI -10%, semiconductor selloff). The entry zone accounts for ATR.
- **Retest/pullback structure:** Below previous day low (confirmed in report). Breakdown move, not a bounce-short.
- **Overextended?** Day move is large (~-6.5%). However, sector cascade dynamics (KOSPI → European chip stocks → US semis) suggest the move is structural, not a one-day overextension that immediately reverts. Late session with 80 min to close: TP1 $609.88 is ~$16 below current ~$625.62 = ~2.5% more downside needed.
- **Would entry NOW be late?** For new entries: YES — 80 min to close is late for a fresh intraday short. For maintaining existing: monitor through close.
- **Actionable now?** MAINTAIN existing position. Do NOT add new entries at 14:40 ET.
- **Invalidation:** Close beyond $636.89. Not at risk currently.
- **Catalyst confirmation:** Confirmed (KOSPI -9.99%, SOX -7.3%, NVDA -3%, AMD -8.7%, MU -10.6%).
- **Aligned with market mood?** YES — risk-off tech, stocks shorts profitable bucket.
- **Legal/headline risk:** None identified for SMH (ETF, no individual company legal exposure).
- **Late-session risk:** TP1 within reach (~2.5% more). If market stabilizes or bounces into close, consider tightening stop to $632.

---

### Candidate 2 — JPM Long (B-tier, stocks intraday) — OPEN ACTIONABLE

**Status:** OPEN ACTIONABLE (triggered)
**Score:** 76.09/100 | Confidence: high | Mode: intraday | Direction: long

**Price reaction / chase check:**
- JPM +0.4% at late session. Entry zone was $333.09–$334.24. Current approximate price: ~$334–335 (holding near entry zone top).
- TP1 $337.69 — requires ~$3 more upside (~1%) in 80 min. Challenging but achievable in a financials-led close.
- **Is this chasing?** Price is still within/near the entry zone if you haven't entered. At $335, entering is marginally late but within ATR.
- **Aligned with market mood?** PARTIALLY — stocks longs are structurally losing (PF 0.10, -18R direction stats). However, JPM has specific RS vs sector (financials outperforming tech), catalyst support (news mention, sector rotation), and uptrend. This is an EXCEPTION play.
- **Playbook contradiction:** Stocks longs directional bucket is catastrophically bad this week (-18R). JPM is the one name with genuine RS + catalyst. Weight it accordingly — smaller size, respect the SL.
- **Invalidation:** $330.80. Not at risk currently at $334.
- **Legal/headline risk:** None in current data for JPM.
- **Late-session risk:** With 80 min to close, target $337.69 requires sustained buy pressure. If market disappoints into close (Nasdaq sells off harder), JPM may retrace toward entry. **Tighten mental stop if market weakens.**
- **Chase risk:** LOW for holding existing position. HIGH for new entries above $335.
- **What would invalidate:** SPY/Dow rolling over into final hour; financials sector rotation reversal.

---

### Candidate 3 — BTC Swing Short (B-tier, crypto swing) — OPEN ACTIONABLE

**Status:** OPEN ACTIONABLE (triggered)
**Score:** 65.X/100 | Confidence: medium | Mode: swing | Direction: short

**Price reaction / chase check:**
- BTC ~$62,415, −3.3% for the session. Swing entry triggered (confirmed in active signals: `BTC swing short B, triggered`).
- Swing horizon: this is NOT constrained by the 80-min US close window. Can run overnight into Asia and US open tomorrow.
- **Regime alignment:** BTC downtrend confirmed. Altcoin breadth 20.9% above EMA20 (structural weakness). $2.5B ETF outflows. Rate-hike expectations cited by Yahoo Finance.
- **Catalyst support:** BTC-specific bearish catalysts: indicator signaling possible further -15% decline (CoinDesk, single_source). Ethereum Foundation cuts (negative sentiment for altcoins). Large whale withdrawal from Binance (1,683 BTC, $104.87M) — could indicate continued distribution.
- **Derivatives:** No OI data for BTC swing direction directly from reports. Intraday suggests overall deleveraging mood.
- **Overnight setup:** US late session → Asia open at ~04:30 EEST. If BTC holds below $63,500, short continuation into Asia is the base case. Risk: any macro catalyst (Fed speak, geopolitical) could spike BTC.
- **Invalidation from reports:** ~$63,X area (exact SL in signal — 1h close beyond invalidation level). Not at risk at $62,415.
- **Chase risk:** NOT applicable — already triggered, swing horizon.
- **Correlation cluster risk:** BTC + ENA (x2) + potentially ETH if triggered = 3–4 correlated crypto short positions. If BTC squeezes, all break simultaneously. Acknowledge cluster exposure.
- **Aligned with mood?** YES — crypto risk-off, swing is the profitable mode (PF 1.57, +12R).

---

### Candidate 4 — ENA Scalp + Intraday + Swing Shorts (B-tier, multi-mode) — OPEN ACTIONABLE

**Status:** OPEN ACTIONABLE — scalp (triggered), intraday (triggered), swing (triggered)
**Score range:** 60.8–68.X/100 | Mode: scalp + intraday + swing | Direction: short

**Lifecycle assessment:**
- Three simultaneous ENA short signals across all three crypto modes — all triggered.
- ENA at ~$0.0865–0.0866. Down -9.2% to -9.3% 24h. Weak RS vs BTC: −5.96%.
- Derivatives: price down + OI down = deleveraging (clean for short continuation). Funding -2.272e-05 (slightly negative, shorts paying slightly — not yet extreme).

**Late-session / overnight routing by mode:**
- **Scalp** (30m–2h horizon): STALE for new entries at 21:40 EEST. Scalp horizon is already expired if this was opened earlier. Per playbook PF 0.14 for scalp, AND week stats: 0.56 PF on scalp overall → **do not add new scalp entries, let run to SL or TP if already in.**
- **Intraday** (4–24h horizon): Crypto intraday PF 0.00, -10R this week. Approach with caution. If triggered earlier, monitor. Do not add.
- **Swing** (multi-day): HOLD. Swing mode profitable (PF 1.57, +12R). Overnight continuation is the base case in risk-off regime.

**Chase check:** ENA -9.3% in 24h before any entry — the move has already happened. New entries at $0.0865 risk chasing exhausted sellers. Existing triggered positions: maintain with stops.

**Invalidation (swing):** 1h close beyond $0.0885. Not at risk.
**Targets (swing):** TP1 $0.0849, TP2 $0.0833, TP3 $0.0817.
**Aligned with mood?** YES (risk-off, deleveraging confirmed). Weight the SWING leg only going forward.

---

### Candidate 5 — ETH Swing Short (B-tier, WAITING) — NEEDS REVIEW + Pipeline Flag

**Status:** WAITING for entry — NOT yet triggered
**Score:** 66.1–67.5/100 (from untracked alerts) | Mode: swing | Direction: short

**Critical flags:**
1. **2 Telegram alerts sent without backing proposed_signal** (14:35 UTC, 16:05 UTC). These signals are UNTRACKED — they will NOT contribute to PF/winrate/avgR. This is a pipeline integrity regression: Telegram alert fired without a corresponding `proposed_signal` row to anchor tracking.
2. Entry still WAITING — ETH swing short has NOT triggered. ETH current ~$1,657.
3. ETH bearish catalysts confirmed: Foundation 20% staff cuts, $2.5B ETF outflows, persistent ETH downtrend.

**Price reaction:**
- ETH at $1,657, −4.71% session. Strong bearish catalyst support.
- Entry zone for swing short (from intraday report analog): ~$0.0868–0.0875 range (ENA reference), but ETH entry would be in the $1,655–$1,680 area based on prior review context.
- If ETH breaks below current level and fills the entry zone → swing short becomes actionable with full tracking (once properly proposed_signal backed).
- **Until the pipeline issue is resolved:** treat this as WATCHLIST / MANUAL REVIEW rather than actionable automated signal.

**What makes it actionable:**
- ETH 1h close confirms entry zone fill with volume
- BTC holding below $63,500 (risk-off regime intact)
- Pipeline issue resolved (proposed_signal backing confirmed)

**Legal/headline risk:** ETH Foundation cuts = negative fundamental catalyst. No legal risk per se.
**Invalidation:** 1h close beyond ~$1,710 (ETH swing high area).

---

## 8. Best Candidates Ranked

No new clean intraday setups are actionable at 21:40 EEST (80 min to close). Existing open signals ranked by quality:

| Rank | Symbol | Mode | Dir | Status | Key trigger/rationale |
|---|---|---|---|---|---|
| 1 | **SMH** | intraday | short | OPEN ACTIONABLE | Catalyst-backed chip rout, within entry zone, profitable shorts bucket, 80-min TP1 window |
| 2 | **BTC** | swing | short | OPEN ACTIONABLE | Regime aligned, swing profitable mode, overnight continuation base case |
| 3 | **JPM** | intraday | long | OPEN ACTIONABLE | Financials RS leader, exception long in structurally-losing longs bucket; 80-min window tight |
| 4 | **ENA (swing leg)** | swing | short | OPEN ACTIONABLE | Multi-mode triggered, deleveraging confirmed, swing horizon valid overnight; scale back scalp/intraday legs |
| 5 | **ETH** | swing | short | WAITING | Strong catalyst support, cleaner entry pending; NEEDS REVIEW re: untracked alerts |

**Best long-watch (no new setups needed; if regime shifts):** JPM — trigger: already in zone, hold with SL $330.80.
**Best short-watch:** SMH — trigger: already triggered, maintain; if new session: re-enter only on retest of breakdown if market gaps up tomorrow.
**Best catalyst-watch:** LINK/USDT — Project Pangea is a genuine institutional adoption catalyst; score too low for B-tier but watch for volume breakout confirmation above resistance $18.50.

---

## 9. Avoid / No Trade

**This decision window only (21:40–00:00 EEST / ~80 min to close + overnight). Scanner continues.**

- **AMD swing long B:** COUNTER-REGIME. SOX −7.3% session. Score 71.76 means nothing when the entire sector is imploding. Stocks swing is watchlist-only per -12R audit anyway. **DO NOT ENTER.**
- **SMH swing long B (carry-forward):** Same. Swing report is from 14:18 UTC when regime looked different. INVALIDATED by session developments. **DO NOT ENTER.**
- **UNH (any):** DOJ Medicare fraud probe confirmed, stock -16%. **AVOID ALL DIRECTIONS.**
- **SMCI (any):** US Attorney SDNY export-control indictment. **AVOID ALL DIRECTIONS.**
- **New crypto scalp entries:** Scalp PF 0.14–0.56, all losing buckets. With 80 min to US close and Asia session handoff approaching, new scalp entries are inadvisable.
- **New crypto intraday entries:** Intraday PF 0.00, -10R this week. Do not add new intraday crypto positions.

---

## 10. Main Risks

1. **BTC squeeze risk:** If BTC reclaims $64,000+, all open crypto shorts (BTC/ENA/XLM/ZEC/WLD waiting) reverse simultaneously. Monitor correlation cluster.
2. **Late-session reversal (stocks):** 80 min to close — sentiment can swing. If S&P rallies into close, SMH short and TSLA short could face last-hour squeeze. Tighten stops.
3. **ETH untracked alert pipeline regression:** 2 ETH swing B alerts untracked. If ETH triggers and trades, the outcome will NOT be in PF stats. This is an ongoing integrity issue requiring manual fix.
4. **Stocks longs structural losing bucket:** JPM is the exception, but the -18R background on stocks longs means size discipline matters. Do not over-size the JPM position.
5. **Catalyst mapping weak:** ~50%+ of 559 catalyst events estimated unmapped. Catalyst layer is context, not decision-making input.
6. **scheduler.log missing:** Path issue needs investigation; affects automated freshness monitoring.
7. **OI-long crowding on DEXE:** DEXE elevated long crowding (OI +23.45%) — not an active signal but a flush risk if it reverses.
8. **Rate-hike expectations:** Macro headwind noted by Yahoo Finance for BTC/ETH. If Fed commentary materializes, could accelerate risk-off beyond current levels.

---

## 11. Action Plan — Next 4 Hours (21:40–01:40 EEST)

**21:40–23:00 EEST (US session final 80 min):**
- Maintain SMH short B (SL $636.89, TP1 $609.88). Tighten to $632 if market stabilizes.
- Maintain JPM long B (SL $330.80, TP1 $337.69). Do NOT add above $335.
- Maintain TSLA short B (referenced in active signals, triggered).
- Do NOT open new intraday stocks positions.
- Do NOT open new crypto scalp or intraday positions.

**23:00–00:00 EEST (US close):**
- Stocks intraday signals (SMH/JPM/TSLA) reach end of cycle. If TP1 not hit by close, assess per playbook (some may expire / entered-unresolved if no resolution).
- Crypto swing positions (BTC short, ENA short) continue overnight. No action needed unless invalidation levels approach.

**00:00–01:40 EEST (Asia session start):**
- BTC swing short: key watch level ~$63,500 (invalidation proxy). If BTC holds below and Asia opens soft → continuation short thesis intact.
- ETH: if price fills entry zone while trigger is properly backed → swing short becomes active.
- No new scalp entries into Asia open (per session timing feedback: wait 1-2h into Asia session before acting).

---

## 12. Final Verdict per Mode

| Mode | Asset | Verdict | Rationale |
|---|---|---|---|
| Scalp (crypto) | crypto | **NO NEW ENTRIES** | PF 0.14–0.56, losing; late in cycle; scalp horizon expired |
| Intraday (crypto) | crypto | **NO NEW ENTRIES** | PF 0.00, -10R week; structural losing bucket |
| Swing (crypto) | crypto | **HOLD OPEN POSITIONS** | PF 1.57, +12R; regime aligned; BTC/ENA shorts continue overnight |
| Intraday (stocks) | stocks | **MAINTAIN OPEN ONLY** | SMH/JPM/TSLA triggered; no new entries 80 min to close |
| Swing (stocks) | stocks | **WATCHLIST ONLY** | −12R audit cap; AMD/SMH swing longs counter-regime; no action |
| Invest (stocks) | stocks | **PLANNING ONLY** | Carry-forward 4h+ data; not actionable intraday |

---

## 13. Sources

- [Bitcoin and ethereum prices today, Tuesday June 23, 2026](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-tuesday-june-23-2026-values-slipping-as-possible-rate-hikes-weigh-on-prices-135817007.html) — Yahoo Finance, 2026-06-23 (BTC $62,415, ETH $1,657)
- [Stock Market Today June 23, 2026: Nasdaq, S&P 500 fall — semiconductor selloff](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-23-2026) — TheStreet, 2026-06-23 (403 on fetch; confirmed via search)
- [US Stock Market Today: Live Updates 23.06.2026](https://ts2.tech/en/stock-market-today-23-06-2026/) — ts2.tech, 2026-06-23 (S&P -1.04%, Nasdaq -2.67%, SOX -7.3%, AMD -8.7%, MU -10.6%)
- [Bitcoin price prediction 2026 — US-Iran Deal, ETF Outflows](https://capital.com/en-int/market-updates/bitcoin-price-forecast-23-06-2026) — capital.com, 2026-06-23 (prior-day BTC $64,035; ETF outflows $90.66M on June 18)
- Internal: `data/reports/scalp/2026-06-23_16-28_scalp_report.md` — mtime 19:28 EEST
- Internal: `data/reports/intraday/2026-06-23_16-33_intraday_report.md` — mtime 19:33 EEST
- Internal: `data/reports/stocks/intraday/2026-06-23_18-17_stocks_intraday_report.md` — mtime 21:17 EEST
- Internal: `data/reports/swing/2026-06-23_14-15_swing_report.md` — mtime 17:15 EEST (carry-forward)
- Internal: `python -m src.cli active-signals` (25 crypto, 50 stocks) — 21:40 EEST
- Internal: `python -m src.cli signal-stats` (crypto + stocks) — 21:40 EEST
- Internal: `python -m scripts.detect_untracked_legacy_alerts --since 2026-06-23` — 2 untracked

---

## 14. Fix Requests / TODO

### TODO-scheduler-log-path
- **issue:** `scheduler.log` not found at `data/logs/scheduler.log`; prior reviews found it at this path
- **evidence:** `Test-Path "C:\Users\adama\Documents\crypto-ai-desk\data\logs\scheduler.log"` returned false; cycle summary used as proxy
- **suggested manual fix:** Verify scheduler config for log output path; update review logic to find the correct path or add a fallback glob
- **priority:** medium
- **first observed:** 2026-06-23 21:40 EEST

### TODO-eth-untracked-alerts
- **issue:** 2 ETH/USDT B swing short Telegram alerts (14:35 UTC, 16:05 UTC) sent without backing `proposed_signal` row — untracked forever
- **evidence:** `detect_untracked_legacy_alerts --since 2026-06-23` output: "2 untracked legacy crypto alert(s)"
- **suggested manual fix:** Investigate why ETH swing B alerts fired without proposed_signal creation; check if `watchlist_alerts` table insert is bypassing the signal pipeline; add pre-send assertion that proposed_signal exists
- **priority:** high
- **first observed:** 2026-06-23 18:39 EEST (1st alert); 2026-06-23 21:40 EEST (2nd alert)

### TODO-catalyst-unmapped-ratio
- **issue:** Unmapped catalyst ratio cannot be auto-computed in scheduled reviews; 559 events with only ~12–15 visible symbol-mapped entries suggests >50% basket/unmapped, triggering "weak mapping" flag but without precise confirmation
- **evidence:** Reports show 559 events, 6 baskets; JSONL query not in allowed CLI commands for this skill
- **suggested manual fix:** Add a `catalyst-coverage-stats` CLI command that outputs mapped vs total count, callable from this scheduled review; or add ratio to the cycle summary md
- **priority:** medium
- **first observed:** 2026-06-23 21:40 EEST

### TODO-crypto-intraday-failing-bucket
- **issue:** Crypto intraday PF 0.00, 0W/10L this week (n=72 signals, 57 triggered). Systematically losing bucket consuming signal quota
- **evidence:** signal-stats output: `mod_ 72 str_ 57 0 10 0.00_ -0._-10._` (intraday row)
- **suggested manual fix:** Conduct manual audit of the 10 intraday losses; check if entry timing, regime filter, or TP1 RR is the failure mode; consider raising intraday entry bar or pausing intraday signals pending review
- **priority:** high
- **first observed:** Recurring over multiple reviews; confirmed 2026-06-23 21:40 EEST

### TODO-kol-watchlist-placeholder
- **issue:** KOL watchlist still contains placeholder account; social attention missing in all runs
- **evidence:** All reports: "KOL watchlist still contains the placeholder account; replace it with trusted sources."
- **suggested manual fix:** Replace placeholder with 3–5 verified crypto KOL accounts in the config; test social attention agent with real accounts
- **priority:** low
- **first observed:** Multiple prior reviews
