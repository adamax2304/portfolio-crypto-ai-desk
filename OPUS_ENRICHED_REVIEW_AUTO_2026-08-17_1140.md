# Opus Enriched Review — Europe / Pre-US Context — Auto Cycle 11:40 EEST

## 1. Executive Summary

**Europe / pre-US context review, 11:40 EEST.** **Advisory only — no auto-trade.** No A/B-tier actionable setups anywhere this cycle (crypto scalp/intraday/swing, or stocks intraday) — everything on the desk is C-tier watchlist/planning. Crypto regime is unchanged **range/chop**: BTC range, ETH transition_up, altcoin breadth ~56–60% above EMA20. External check corroborates: BTC pinned $62.3K–$64K (repeatedly rejected above $64K), ETH capped under $1,900–$1,922, sentiment "bearish to neutral" — nothing has broken out. Macro risk is elevated and **worse than the 04:40 review (93.7/100 vs 81.5/100)** on continued Ukraine/Russia and EU-sanctions headlines plus fresh Coldcard-exploit follow-through (external check: total theft now >$130M across 5,000+ addresses, ~90% of stolen BTC still unmoved — an overhang, not a resolved story). **Data-integrity carry-forward: the OHLCV-freeze defect first flagged 02:00 EEST is still unresolved 7+ cycles later.** HOLO/USDT, AVNT/USDT, PROM/USDT (×2), LUNA/USDT, MMT/USDT, BABY/USDT — all *currently open* crypto swing positions — are still reading raw 15m candles frozen at **2026-08-15 22:30–23:00 UTC** (now ~37h stale); BMT/MUBARAK didn't get fixed, they just auto-expired to `CLOSED FLAT 0R` via the timeout path, which masks the bug rather than resolving it. Treat these 7 open positions' displayed state as **unverified**. Stocks are pre-market (US cash session closed) — 15 A-raw candidates exist but all are demoted to C for `market_closed_intraday_planning_only`; 5 of those 15 (REGN, DELL, INTU, BLK, SMCI) carry additional active legal/headline risk (class action, indictment, securities fraud) and must not be treated as clean even after the open. Cleanest pre-open long-watch: **COP** (raw A/100, no legal-risk flag). Crypto best long-watch: **PORTAL/USDT** (top C-tier swing idea, but already +67.7% 24h — genuine chase risk, needs a pullback). Best short-watch: **GRVT/USDT** (fresh downtrend, RS negative vs BTC, 2.49x volume confirming). Catalyst mapping is weak this run (57% unmapped, worse than 51.8% prior) — use catalyst layer as context only.

**External web research used this cycle** (BTC/ETH/XRP levels + Coldcard-exploit follow-up) — corroborates internal chop/risk-off read, does not contradict; see §13.

## 2. Data Used

- Scheduler: `data/scheduled_runs/2026-08-16_default_schedule/scheduler.log` — fresh (mtime 11:36 EEST, ~4 min old); latest `cycle_05_09-33_summary.md` (mtime 11:36 EEST, same). Both well under the 3h defer threshold.
- Reports: scalp `2026-08-17_07-13` (generated 10:13 EEST, ~1.5h old, fresh), intraday `2026-08-17_07-50` (generated 10:50 EEST, ~50min old, fresh), swing `2026-08-17_04-22` (generated 07:22 EEST, ~4h20min old — **carry-forward**, no fresher swing scan this cycle), stocks intraday `2026-08-17_08-20` (generated 11:20 EEST, ~20min old, fresh but market pre-open — planning-only), stocks swing/invest `2026-07-02` (six weeks stale — expected/deprecated per prior project context, not investigated further).
- Catalysts: `data/catalysts/2026-08-17/catalyst_events.jsonl` (672 events today, mtime 10:54 EEST), `narrative_baskets.jsonl` (5 baskets, same mtime).
- LLM packets: `llm_analysis_packet.md` fresh (10:51 EEST), `llm_stocks_packet.md` fresh (11:22 EEST).
- CLI: `active-signals` (crypto n=42, stocks n=50), `signal-stats` (crypto: n=67 stronger-confidence, PF 3.17, totalR +28.3, scalp mode weak PF 0.5/-0.5R; stocks: A/B headline sample=8 anecdotal PF 0.0 totalR -1.0, C-tier watchlist n=564 PF 0.18 totalR -9.0 — small-sample, not actionable), `detect_untracked_legacy_alerts --since 2026-08-17` → **clean**, no untracked alerts.
- Direct OHLCV CSV timestamp re-check (`data/raw/ohlcv/binance/15m/*.csv`) for the 12 symbols previously flagged frozen — primary continuity diagnostic this cycle (see §3).
- `reports/PAPER_MONITOR_STATUS_LATEST.md` (mtime 11:33 EEST) — cross-checked against raw OHLCV for HOLO/BMT/MUBARAK.
- Prior review for comparison: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-17_0440.md` (crypto overnight / Asia review, 04:40 EEST).
- **External web research run this cycle** (1 WebSearch + 1 WebFetch: BTC/ETH/XRP levels for Aug 17 2026; 1 WebSearch: Coldcard exploit follow-up) — corroborates internal regime and risk read, does not contradict.

## 3. Scheduler / Data Freshness

- Scheduler: **fresh**, cycle 5 completed 11:36 EEST (~4 min old, well under 3h defer threshold).
- Scalp: **fresh** (~1.5h). Intraday: **fresh** (~50min). Swing: **carry-forward** (~4h20min, still the latest snapshot, within the 4–12h carry-forward band). Stocks intraday: **fresh** (~20min) but market pre-open, planning-only. Stocks swing/invest: **stale** (6 weeks, expected/deprecated).
- Catalyst folder: fresh (672 events today, mtime 10:54 EEST), 5 narrative baskets, mapping **weak** (57% unmapped — see §5, worse than the 51.8% at 04:40).
- **Monitor/price-feed integrity: CONFIRMED STILL DEGRADED, 7th+ consecutive cycle.** Direct re-check of raw OHLCV (binance 15m) for the 13 symbols flagged at 04:40:
  - **Still frozen at 2026-08-15 22:30–23:00 UTC (now ~37h stale):** HOLO, MUBARAK, THE, AVNT, PROM, LUNA, MMT, BABY, PEOPLE, BANANAS31, TST — unchanged from the 04:40 review, no progress on the underlying fetch defect. Control symbols (PORTAL, WLFI, CHIP) all show a fresh 2026-08-17 08:30 UTC candle (~10min old) — confirms this remains pair-specific, not a global outage.
  - `PAPER_MONITOR_STATUS_LATEST.md`: **BMT and MUBARAK have transitioned to `⚪ CLOSED FLAT 0R (expired_flat)`** since 04:40 — but their underlying OHLCV is still frozen at the same stale timestamp, so this looks like the expiry-timeout path closing them out on stale data, not a genuine fresh-price resolution. **HOLO/USDT is still shown `🟢 OPEN — entry filled, monitoring TP/SL`** despite the frozen feed — this display cannot be trusted.
  - Of the 12 still-frozen symbols, **7 (HOLO, AVNT, PROM ×2, LUNA, MMT, BABY) are currently listed as open (`triggered`) positions in `active-signals`** with real capital-equivalent exposure in the paper book — their TP/SL/invalidation state should be treated as **unverified**, not confirmed-open, until the feed is fixed.
  - **TODO-2 (PORTAL scalp `waiting_for_entry` past its own `expires_at`) appears resolved this cycle** — `sig_3d9797eb42e0d678` no longer appears in `active-signals` output at all (42 rows this cycle vs 50 at 04:40). Tentatively closing this thread; will re-flag if it recurs.
  - **New observation this cycle:** a large share of `active-signals` rows carry `expires_at` weeks in the past while still showing `tp1_hit`/`tp2_hit`/`triggered` status — e.g. `sig_b16bb9e54598333a` (NEAR/USDT scalp) expired 2026-07-17, still listed active 31 days later. 25 of 42 crypto rows and effectively all 50 stocks rows are in this state. Distinct from the OHLCV-freeze bug (these have fresh underlying prices, TP was genuinely hit) — this looks like a lifecycle/archival gap, not a live-risk issue, but it degrades the signal of `active-signals` as a "what's actually open" view. See TODO-4.
- `detect_untracked_legacy_alerts --since 2026-08-17`: **clean**.
- See §14 TODO-1 (updated, still critical), TODO-2 (tentatively resolved), TODO-4 (new).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-08-17 11:40 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "bad", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["stocks swing/invest 6wk stale (expected/deprecated)", "on-chain whale flows not connected"],
      "suggested_effect": "advisory_only",
      "facts_used": ["7th+ consecutive cycle with 11-12 symbols on frozen OHLCV (2026-08-15 22:30-23:00 UTC)", "scheduler fresh 4min", "HOLO still shown OPEN on stale feed", "BMT/MUBARAK closed via timeout not genuine resolution"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["chop", "risk_off", "mixed", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC range, ETH transition_up, breadth 56-60%", "external: BTC $62.3-64K rejected repeatedly, ETH capped <$1900-1922, sentiment bearish-to-neutral", "macro risk 93.7/100, up from 81.5/100 at 04:40", "stocks: bullish/risk-on, VIX 14.94, breadth 100%"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"],
      "data_missing": ["PORTAL/GRVT/ONG/most watchlist symbols: zero internal catalyst hits"],
      "suggested_effect": "advisory_only",
      "facts_used": ["672 events today, 57% unmapped (worse than 51.8% at 04:40)", "momentum_breakout/avoid_chase basket: PORTAL, ONG, BTW", "BTC exploit_hack + delisting_risk baskets active", "SOL/BTC/ETH: Bank Leumi x Galaxy institutional-access primary-source item, long-dated (early 2027)"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.4,
      "reason_codes": ["data_unavailable", "oi_supports"],
      "data_missing": ["OI 24h% n/a for several MEXC-fallback symbols", "no live squeeze/crowding feed beyond per-symbol funding snapshot"],
      "suggested_effect": "advisory_only",
      "facts_used": ["PORTAL: price up + OI up, fresh positioning, funding -0.00032", "ONG: price up + OI up, funding -0.00098", "PUMP/TUT: price up + OI down = short covering, weaker continuation"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "overextended", "clean_retest", "entry_late"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PORTAL +67.7% 24h, 0.54x volume vs 20d avg — classic chase-risk profile, avoid_chase basket", "GRVT -1.02% 24h but -12.83% 7d, 2.49x volume — fresher, less extended short setup", "no A/B setups cleared entry-freshness bar anywhere this cycle"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.6,
      "reason_codes": ["open_actionable", "entered_unresolved", "needs_review"],
      "data_missing": ["exact waiting_for_entry / no-entry counts not distinctly exposed by active-signals CLI this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 17/42 active rows have future expires_at (open actionable), 25/42 past-expiry (entered unresolved, TP already hit or triggered)", "stocks: 50/50 active rows past-expiry from prior sessions (market currently closed, nothing fresh today yet)", "7 open crypto positions (HOLO/AVNT/PROM x2/LUNA/MMT/BABY) run on frozen OHLCV — needs_review"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["headline_risk", "legal_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["5 of 15 A-raw stocks (REGN, DELL, INTU, BLK, SMCI) carry active legal/headline risk (class_action/indictment/securities_fraud)", "BTC Coldcard exploit >$130M, ~90% of stolen BTC still unmoved — ongoing overhang not resolved", "macro risk 93.7/100 driven by geopolitical (Ukraine/Russia, EU sanctions) headlines"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["low_sample", "playbook_working", "playbook_failing"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto overall PF 3.17, totalR +28.3R (n=67) — working; scalp mode specifically weak PF 0.5, -0.5R (n=11)", "stocks A/B headline PF 0.0, totalR -1.0 (n=8, anecdotal — too small to act on)", "stocks C-tier watchlist PF 0.18, totalR -9.0 (n=564, reliable but by definition not actionable)"] },
    { "agent": "head_trader", "verdict": "advisory_synthesis_only", "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["see section 8 below"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "PORTAL/USDT", "trigger": "pullback into 0.0170-0.0179 zone with volume pickup (currently 0.0184, +67.7% 24h — do not chase at current price)", "reason": "top-scored C-tier swing idea (61.6), RS-leader with OI/price confirmation, but no catalyst and low relative volume — chase risk flagged by its own avoid_chase basket" },
    "best_short_candidate":    { "symbol": "GRVT/USDT", "trigger": "1h close below the 0.2918-0.2941 failed-bounce/retest zone, confirming rejection toward 0.2857", "reason": "downtrend (-1.02% 24h, -12.83% 7d), negative RS vs BTC, 2.49x volume confirming distribution, no catalyst to fight" },
    "best_catalyst_candidate": { "symbol": "SOL/USDT", "trigger": "fresh A/B signal firing with RS confirmation off the Bank Leumi x Galaxy institutional-access news (primary source, t.me/CoinMarketCapAnnouncements) or the staking-as-dividend narrative", "reason": "genuine primary-source institutional-adoption catalyst, but long-dated (early 2027 rollout) and no live signal yet — watch only" },
    "avoid_candidate":         { "symbol": "INTU", "reason": "A-raw score 100 but active securities-fraud class-action with a named Sept 8 2026 filing deadline (PR Newswire, catalyst_events today) — demoted to C and flagged legal_headline_risk; do not treat as clean even after the cash open" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | bad | 0.85 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | caution | 0.75 | chop, risk_off, mixed, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.4 | data_unavailable, oi_supports | advisory_only |
| technical_entry | caution | 0.6 | chase_risk, overextended, clean_retest, entry_late | advisory_only |
| execution_lifecycle | needs_review | 0.6 | open_actionable, entered_unresolved, needs_review | advisory_only |
| risk_manager | caution | 0.7 | headline_risk, legal_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.5 | low_sample, playbook_working, playbook_failing | advisory_only |
| head_trader | advisory_synthesis_only | 0.65 | — | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-17_0440.md` (04:40 EEST, crypto overnight/Asia):

- **Macro risk worsened**: 93.7/100 vs 81.5/100 — geopolitical headline flow (Ukraine/Russia strikes, EU sanctions expansion, Japan-auto exposure) intensified overnight into the EU morning.
- **TODO-1 (OHLCV freeze) — unresolved, partially masked, not fixed.** BMT and MUBARAK moved to `CLOSED FLAT 0R` via the expiry-timeout path (not a genuine price-driven resolution — their raw feed is still frozen). HOLO is still openly showing `🟢 OPEN` on stale data. 7 live crypto positions are now confirmed running on unverified pricing (up from an implicit "some subset" at 04:40).
- **TODO-2 (PORTAL scalp expiry bug) — appears resolved.** The affected signal no longer appears in `active-signals`; tentatively closing, will re-confirm next cycle.
- **Catalyst mapping weakened further**: 57% unmapped vs 51.8% at 04:40.
- **Crypto regime unchanged**: still range/chop, BTC range / ETH transition_up, no A/B setups in any crypto mode.
- **Stocks flipped from closed/no-data to a live pre-market picture**: 15 A-raw candidates now visible (COP, REGN, CRM, DELL, INTU, SHOP, PYPL, ADBE, DIS, BLK, XOM, XLE, SMCI, MA, GE), all demoted to C for market-closed; 5 of them additionally carry fresh legal/headline risk (REGN, DELL, INTU, BLK, SMCI) — this is new information not present at 04:40, when stocks intraday had no fresh A-raw list.
- **New top crypto watchlist idea**: PORTAL/USDT swing (61.6) — wasn't the top idea at 04:40; flagged this cycle for genuine chase risk given the +67.7% 24h move.
- Thesis on BTC/ETH range/chop: **confirmed**, not invalidated, by external check.

## 5. Catalyst Coverage

- Total `catalyst_events` today: **672**. Mapped (non-null symbol): **289** (43%). Unmapped: **383** (57%). `narrative_baskets`: **5**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (most recent): "HUAWEI AppGallery et GameCenter préparent le terrain pour... Gamescom 2026" (PR Newswire, non-English generic PR noise); "Did e.l.f. Beauty, Inc. Insiders Breach their Fiduciary Duties to Shareholders?" (PR Newswire, generic stocks legal-solicitation boilerplate); "HUAWEI AppGallery und GameCenter bereiten die Bühne..." (PR Newswire, duplicate in German) — the unmapped tail this cycle is dominated by generic PR Newswire wire noise (multi-language duplicates, boilerplate legal-solicitation ads) rather than genuinely unmappable trading-relevant news.
- Active narrative baskets: `delisting_thin_liquidity` (BTC/USDT primary), `ai_narrative` (NEAR/RENDER/TAO/FET), `rwa_narrative` (ONDO/XLM), `binance_ecosystem_teaser` (BNB), `momentum_breakout`/`avoid_chase` (PORTAL/ONG/BTW).

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **chop, risk-off leaning** (range regime, macro risk 93.7/100 driven by geopolitics + ongoing Coldcard-exploit overhang; external check corroborates bearish-to-neutral sentiment on BTC/ETH/XRP).
- Stocks mood: **pre-market / risk-on underlying** (regime label bullish, VIX 14.94, breadth 100%, all 4 major indices in uptrend on 5d/20d) — but session is closed, so this is planning context, not live confirmation.
- Dominant narrative: momentum-breakout/chase-risk names (PORTAL/ONG/BTW) in crypto; AI-capex mega-cap story (MSFT/AMZN/GOOGL ~$600B capex) and a fresh "AI is a super bubble" contrarian rotation headline (Chinese hedge funds, per NVDA news) in stocks.
- Preferred side now: **wait-for-trigger / catalyst-backed** — chop regime plus an escalating macro-risk score argues against forcing directional risk; the cleanest available ideas both require confirmation (PORTAL needs a pullback, GRVT needs a breakdown close, COP needs RTH confirmation after the open).
- Best long candidate: PORTAL/USDT (crypto, watch — chase risk) / COP (stocks, watch — pre-market only).
- Best short candidate: GRVT/USDT (crypto, watch — needs breakdown confirmation).
- Best catalyst-backed candidate: SOL/USDT (crypto, watch — no live signal yet).
- What to avoid: INTU, DELL, REGN, BLK, SMCI (stocks — active legal/headline risk, do not treat as clean even post-open); the 7 crypto positions on frozen OHLCV (HOLO, AVNT, PROM ×2, LUNA, MMT, BABY) should not be actively managed off their displayed TP/SL state until the feed is confirmed fresh.
- What would change the view: a clean BTC reclaim/hold above $64K or ETH clearing $1,922 would flip crypto mood toward risk-on; a confirmed fix to the OHLCV feed (fresh candle on HOLO/AVNT/PROM/LUNA/MMT/BABY) would clear the data-integrity caution; RTH confirmation at/after the 09:30 ET open would make the stocks A-raw names (ex-legal-risk ones) genuinely actionable.

## 7. Candidate Deep Dives

### PORTAL/USDT (crypto swing, C-tier watchlist, score 61.6) — best long-watch
- Has price already reacted to the catalyst? No verified catalyst exists; the move (+67.7% 24h, +59.1% 7d) is unexplained by any mapped news — it's a `momentum_breakout` basket member with the `avoid_chase` playbook attached.
- Is the setup chasing? **Yes** — this is the textbook chase-risk case: price is far above any reasonable pullback entry and volume (0.54x 20d avg) does not confirm the move.
- Retest/pullback structure? Conditional pullback zone is defined at 0.0170-0.0179 (current price 0.0184); no retest has occurred yet.
- Overextended (>2 ATR from EMA20)? Not explicitly computed, but 67.7%/24h on 0.54x volume is a strong overextension signal by proxy.
- Would entry now be late? Yes.
- What level makes it actionable? A defended pullback into 0.0170-0.0179 on rising volume, or a clean base above 0.0184 that holds for several hours.
- Aligned with market mood? Partially — chop/wait-for-trigger mood argues for waiting on the pullback rather than chasing.
- Long, short, or wait-for-trigger? Wait-for-trigger (long bias if the pullback holds).
- Actionable now or after confirmation? After confirmation only.
- Invalidation: 1h close below 0.0159.
- Chase-risk setup? Yes, explicitly.
- Catalyst confirmation/contradiction? No catalyst either way — this is a pure momentum/derivatives read (funding -0.00032, OI up, confirms fresh positioning).

### GRVT/USDT (crypto swing, C-tier watchlist, score 58.0) — best short-watch
- Has price already reacted? Yes — already down -1.02%/24h, -12.83%/7d; this is a continuation/retest short, not a fresh breakdown chase.
- Chasing? No — this is comparatively fresh versus PORTAL; volume is elevated (2.49x) confirming distribution rather than a low-volume drift.
- Retest structure? Yes — conditional failed-bounce/retest zone 0.2918-0.2941 defined, current price 0.2908 (just below the zone, i.e. a bounce into resistance would be the short trigger).
- Overextended? No — moderate 7d decline, not a vertical move.
- Late entry risk? Low if triggered on the retest zone; chasing the breakdown further would be late.
- Actionable level: 1h close beyond 0.2969 invalidates; the short thesis wants rejection at/below 0.2918-0.2941 toward TP1 0.2857.
- Aligned with mood? Yes — chop/risk-off macro backdrop favors clean shorts on RS-negative names over fresh longs.
- Long/short/wait? Short, wait-for-trigger (retest confirmation).
- Chase risk? No.
- Catalyst confirmation/contradiction? None either way — pure technical/derivatives setup (fallback derivatives via Bybit, funding neutral).

### SOL/USDT (crypto, catalyst-watch, no live signal)
- Catalyst: Bank Leumi (Israel's largest bank) partnering with Galaxy to offer BTC/ETH/SOL trading via Leumi Trade, "starting early 2027" — primary source (t.me/CoinMarketCapAnnouncements). Also a same-cycle CryptoSlate piece on staking-as-dividend plans for ETH/SOL shrinking staked supply.
- Has price reacted? No live SOL signal exists in today's book to check against; treat as pure catalyst-watch.
- Chase risk? N/A, no active setup.
- What makes it actionable: a fresh A/B signal on SOL with RS-leader confirmation would be the trigger to escalate this from catalyst-watch to a real candidate.
- Caveat: the news is real (primary source) but long-dated (2027 rollout) — near-term price impact is speculative, not confirmed.

### COP (stocks intraday, C-tier watchlist — pre-market planning only) — best stocks long-watch
- Raw tier A, score 100, confidence high, risk penalty 0.0 — the cleanest of the 15 A-raw names (no legal/headline flag, unlike REGN/DELL/INTU/BLK/SMCI).
- Demoted to C purely for `market_closed_intraday_planning_only` — a session-state gate, not a quality problem with the setup itself.
- Actionable now or after confirmation? Only after 09:30 ET RTH confirmation — do not treat the pre-market planning level as an entry.
- Legal/headline risk: none found in today's catalyst events for COP.
- Sector context: energy (XLE) is one of the strongest sectors today (+7.33% 20d, RS +2.89% vs SPY) — supportive backdrop for a COP long thesis.

### INTU (stocks intraday, C-tier watchlist) — avoid candidate
- Raw tier A, score 100, but flagged `legal_headline_risk: class_action,securities_fraud` — internal catalyst event today: "APPROACHING DEADLINE ALERT: Intuit Inc. (INTU) Investors: September 8, 2026, Filing Deadline in Securities Fraud Class Action" (PR Newswire, collected today).
- Per §I discipline, this internal record is recent (today), sourced (PR Newswire, named deadline), and consistent with the block flag applied by the pipeline — no external verification needed this cycle; treated as sufficient to sustain AVOID/MANUAL REVIEW.
- Final verdict: **AVOID / MANUAL REVIEW REQUIRED**, never a clean actionable, even after the cash open, until the legal situation is resolved or the flag is manually cleared by a human review.

## 8. Best Candidates Ranked

1. **PORTAL/USDT** — long-watch (crypto), wait for pullback 0.0170-0.0179, chase risk if bought now.
2. **GRVT/USDT** — short-watch (crypto), wait for 1h close below 0.2918-0.2941.
3. **COP** — long-watch (stocks), wait for RTH confirmation at/after 09:30 ET, cleanest of the 15 A-raw pre-market names.
4. **SOL/USDT** — catalyst-watch (crypto), no live signal, watch for a fresh A/B fire on the institutional-adoption/staking narrative.

No clean actionable trade exists in this decision window for any mode — this applies only to the 11:30 EEST window, not a system-wide stop.

## 9. Avoid / No Trade

- **INTU, DELL, REGN, BLK, SMCI** (stocks) — active legal/headline risk (securities fraud, indictment, class action); avoid even if they later trigger a clean technical setup post-open.
- **HOLO, AVNT, PROM (×2), LUNA, MMT, BABY** (crypto, currently "open" positions) — running on a frozen OHLCV feed (~37h stale); do not treat their displayed TP/SL/invalidation state as reliable until the feed is confirmed fixed. This is a data-integrity caution, not an instruction to close them manually (no execution action is authorized by this review).
- This is a decision-window caution only. Scanning, tracking, and candidate generation continue uninterrupted across all modes.

## 10. Main Risks

- **OHLCV-freeze defect, now 37h+ old and 7+ review cycles unresolved** — directly contaminates the displayed state of 7 live crypto positions; the closest thing to a live-risk issue this review has surfaced (see TODO-1).
- Elevated macro risk (93.7/100) driven by Ukraine/Russia geopolitical headlines and EU sanctions expansion — a broad risk-off headwind for crypto beta.
- Coldcard exploit overhang: >$130M stolen, ~90% of stolen BTC still unmoved per external check — a standing liquidation/dump risk if the attacker(s) start moving funds.
- Weak catalyst mapping (57% unmapped) reduces confidence in any catalyst-backed read this cycle.
- 5 of 15 A-raw stocks pre-market candidates carry active legal/headline risk — a naive score-only read would misclassify these as clean.

## 11. Action Plan — next 4 hours

- Watch PORTAL/USDT for a pullback into 0.0170-0.0179 with volume pickup before considering a long.
- Watch GRVT/USDT for a 1h close below 0.2918-0.2941 confirming short continuation.
- Watch COP (and the other 9 non-legal-risk A-raw names: CRM, SHOP, PYPL, ADBE, DIS, XOM, XLE, MA, GE) for RTH confirmation at/after the 09:30 ET US cash open; treat pre-market levels as planning only.
- Do not act on REGN/DELL/INTU/BLK/SMCI regardless of score until legal flags clear.
- Re-check HOLO/AVNT/PROM/LUNA/MMT/BABY OHLCV freshness next cycle; if still frozen, this becomes an 8th consecutive cycle and should be escalated further (see TODO-1).
- No action needed on TODO-2 (PORTAL scalp expiry) unless it recurs.

## 12. Final Verdict per Mode

- **Crypto scalp**: No trade — no A/B setups, weak mode-level stats this window (PF 0.5, -0.5R).
- **Crypto intraday**: No trade — no A/B setups; watch TUT/USDT only as low-confidence watchlist.
- **Crypto swing**: Wait-for-trigger — PORTAL (long, pullback) and GRVT (short, breakdown) are the two watch candidates; do not chase PORTAL at current price.
- **Stocks intraday**: Planning only — market closed; watch COP + 9 clean A-raw names for RTH confirmation; hard-avoid the 5 legal-risk names.
- **Stocks swing/invest**: N/A — deprecated/stale, not evaluated.

## 13. Sources

- [Crypto Price Prediction August 17, 2026: Bitcoin, Ethereum and XRP Face Key Support Levels as Traders Await Breakout Signals](https://sundayguardianlive.com/business/crypto-price-prediction-august-17-2026-bitcoin-ethereum-and-xrp-face-key-support-levels-as-traders-await-breakout-signals-262800/) — Sunday Guardian Live, 2026-08-17
- [Coldcard wallet exploit leads to theft of over 1,778 Bitcoin worth $112M](https://cryptobriefing.com/coldcard-wallet-exploit-bitcoin-theft-112m/) — CryptoBriefing, date unavailable (recent, referenced in today's catalyst events)
- [Hackers steal over $130M by exploiting bug in offline hardware wallets](https://techcrunch.com/2026/08/04/hackers-steal-over-130-million-by-exploiting-bug-in-offline-hardware-wallets/) — TechCrunch, 2026-08-04
- Internal: `data/catalysts/2026-08-17/catalyst_events.jsonl` (672 events), `narrative_baskets.jsonl` (5 baskets)
- Internal: `data/reports/scalp/2026-08-17_07-13_scalp_report.md`, `data/reports/intraday/2026-08-17_07-50_intraday_report.md`, `data/reports/swing/2026-08-17_04-22_swing_report.md`, `data/reports/stocks/intraday/2026-08-17_08-20_stocks_intraday_report.md`
- Internal: `reports/PAPER_MONITOR_STATUS_LATEST.md` (mtime 11:33 EEST)

## 14. Fix Requests / TODO

### TODO-1: Stale OHLCV / false-"OPEN" defect — still unresolved, 7th+ consecutive cycle, partially masked by timeout-close
- **issue:** binance 15m OHLCV fetch remains frozen at 2026-08-15 22:30–23:00 UTC (now ~37h stale) for at least 11 symbols (HOLO, MUBARAK, THE, AVNT, PROM, LUNA, MMT, BABY, PEOPLE, BANANAS31, TST). Of these, 7 (HOLO, AVNT, PROM ×2, LUNA, MMT, BABY) are currently live `triggered` positions in `active-signals` — their TP/SL/invalidation display cannot be trusted. BMT and MUBARAK have since transitioned to `CLOSED FLAT 0R (expired_flat)` in `PAPER_MONITOR_STATUS_LATEST.md`, but this is the expiry-timeout path closing them on stale data, not evidence the underlying fetch is fixed — HOLO is still shown `🟢 OPEN` on the same frozen feed. First flagged 02:00 EEST 2026-08-17 (3 symbols); confirmed present and widened at 18:49, 21:39, 23:29, 04:40, and now 11:40 (same 2026-08-16 date cycle) — no remediation in over 12 hours of tracking.
- **evidence:** `data/raw/ohlcv/binance/15m/{HOLO,MUBARAK,THE,AVNT,PROM,LUNA,MMT,BABY,PEOPLE,BANANAS31,TST}_USDT.csv` last row still dated 2026-08-15 22:30:00+00:00 or 23:00:00+00:00 (re-checked 2026-08-17 11:40 EEST); control symbols (PORTAL, WLFI, CHIP) last row 2026-08-17 08:30:00+00:00. `reports/PAPER_MONITOR_STATUS_LATEST.md` line ~199 shows HOLO/USDT `🟢 OPEN`; lines ~119-120 show BMT/MUBARAK `⚪ CLOSED FLAT 0R (expired_flat)`.
- **suggested manual fix:** identify why the OHLCV ingest job has not recovered for these specific symbols in over 12 hours of tracking despite unaffected pairs in the same batch refreshing normally; add an automated staleness alarm (any active-signal symbol whose latest candle is >2h behind the batch's freshest candle should page/flag, not silently display as OPEN); separately, audit whether the expiry-timeout close path should be allowed to resolve a signal to `CLOSED FLAT` when its underlying OHLCV is itself known-stale — right now that path is quietly hiding the defect for BMT/MUBARAK rather than surfacing it.
- **priority:** critical (unchanged from 04:40 — unresolved 7+ cycles, still directly affecting 7 live position displays).
- **first observed:** 2026-08-17 02:00 EEST (3 symbols); confirmed unresolved 2026-08-17 11:40 EEST (11 symbols still frozen, 7 of them live positions).

### TODO-2: Signal status not transitioning past expires_at (PORTAL/USDT scalp) — tentatively resolved
- **issue:** `sig_3d9797eb42e0d678` (PORTAL/USDT scalp) previously showed `waiting_for_entry` ~2h past its own `expires_at` (flagged 04:40). This cycle it no longer appears in `active-signals` output at all.
- **evidence:** `python -m src.cli active-signals --asset-class crypto` returned 42 rows this cycle vs 50 at 04:40; `sig_3d9797eb42e0d678` is absent from the current output.
- **suggested manual fix:** none needed if this holds; re-confirm next 1-2 cycles that no other scalp signal exhibits the same past-expiry `waiting_for_entry` pattern before fully closing this thread.
- **priority:** low (tentatively resolved, downgraded from medium).
- **first observed:** 2026-08-17 04:40 EEST; resolution observed 2026-08-17 11:40 EEST.

### TODO-3 (carried forward, unrelated): untracked-alert / signal-reuse bug
- **issue:** per prior project memory, watchlist re-fires have previously reused a stale/closed `signal_id` instead of minting a new `proposed_signal` (confirmed on ALLO/USDT and BANK/USDT in an earlier session).
- **evidence:** this cycle's `detect_untracked_legacy_alerts --since 2026-08-17` came back clean again — no new instance observed this run, carrying forward as a watch item.
- **suggested manual fix:** no action needed this cycle; keep running the detector each review.
- **priority:** high (per prior escalation; unchanged, not re-verified this cycle beyond the clean detector run).
- **first observed:** 2026-07-17 (prior session).

### TODO-4 (new): long-tail `active-signals` rows lingering weeks past expires_at without final lifecycle resolution
- **issue:** a large share of `active-signals` rows carry `status` in `{triggered, tp1_hit, tp2_hit}` with `expires_at` weeks in the past, unrelated to the OHLCV-freeze bug (their underlying price data is fresh; TP was genuinely hit). Example: `sig_b16bb9e54598333a` (NEAR/USDT scalp, tp1_hit) has `expires_at=2026-07-17T15:56:12`, still listed active 31 days later on 2026-08-17. 25 of 42 crypto rows and effectively all 50 stocks rows (all from prior sessions, dated 2026-07-10 to 2026-08-15, well past their intraday-scale windows) are in this state.
- **evidence:** `python -m src.cli active-signals --asset-class crypto` and `--asset-class stocks`, comparing each row's `expires_at` to the current run timestamp (2026-08-17 11:40 EEST / 08:40 UTC).
- **suggested manual fix:** clarify whether `active-signals` is intended to show "ever opened, not yet archived" (in which case this is expected and just needs a status/age filter added to the CLI for readability) or "currently open" (in which case a job should be moving fully-resolved past-expiry rows into an archived/closed state). Either way, a human session should confirm intended behavior before treating this as a defect.
- **priority:** medium (data-hygiene / CLI-usefulness issue, not a live-risk issue — TPs were genuinely hit on fresh data in the cases checked).
- **first observed:** 2026-08-17 11:40 EEST.
