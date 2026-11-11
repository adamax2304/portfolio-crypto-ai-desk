# Opus Enriched Review — US open reaction review — Auto Cycle 18:39 EEST

## 1. Executive Summary

Slot: **US open reaction review** (Sunday 2026-07-26, run at 18:39 EEST). Advisory only — no auto-trade. Framing note carried from the 16:20 review: **today is Sunday — there is no US cash open at all today**; the "first US-session reaction" focus of this slot does not apply — stocks stay fully closed until Monday 2026-07-27 ~16:30 EEST (confirmed: this cycle ran in `weekend (crypto-only)` mode with stocks disabled). Crypto remains the only live actionable class. No A/B crypto setup cleared the desk again this cycle (scalp mode correctly stayed kill-switched off with zero ideas; intraday produced 2 watchlist names, swing produced 1 B-tier watchlist idea already registered as `waiting_for_entry`). Four swing signals (DIA, PENGU, EPIC, EUL) were freshly registered as `waiting_for_entry` when the swing report regenerated at 17:52 EEST — a change from the 16:20 review's zero. **Biggest change this cycle: ZAMA/USDT fully reversed** — from the 16:20 review's cleanest volume-backed long-watch (+11.46%/24h, RS-leader) to a `weak_rs_short` C-tier name (-3.85%/24h) this cycle; treat the prior long thesis as invalidated, not carried. DIA/USDT's catalyst-tag false positive from 16:20 has resolved on its own (dropped out of `momentum_breakout`, now correctly shows `catalyst_news: no fresh verified catalyst detected`), but a **third instance of the same ticker-substring-collision resolver bug** was found this cycle on ARX/USDT (direct `news_items` query for "ARX" in the last 24h returns only an unrelated "USARx" stock listing). EUL/USDT's Upbit-KRW-listing catalyst remains externally reconfirmed (WebSearch + WebFetch, dated today) but is still mismapped internally — unresolved for a third consecutive cycle. Macro/geopolitical risk ticked back up to 79.9/100 (from 72.3/100 at 16:20) on fresh Iran/Hormuz tanker-attack and blockade-enforcement headlines, externally corroborated. Three TODOs carried/raised, no code touched.

## 2. Data Used

- Reports: `data/reports/scalp/2026-07-26_14-08_scalp_report.md` (mtime 17:08 EEST, ~1.5h old), `data/reports/intraday/2026-07-26_14-16_intraday_report.md` (mtime 17:16 EEST, ~1.4h old), `data/reports/swing/2026-07-26_14-52_swing_report.md` (mtime 17:52 EEST, ~47min old, daily swing regenerated this cycle). All fresh, all from the same 16:59-17:56 EEST scheduled cycle.
- Stocks: `data/reports/stocks/intraday/2026-07-24_20-10_stocks_intraday_report.md` (~46h old, stale by design — weekend, market closed all Sunday), swing/invest from 2026-07-02 (very stale, market closed regardless). Treated as planning-only per slot rules.
- Catalysts: `data/catalysts/2026-07-26/catalyst_events.jsonl` (1904 events today), `narrative_baskets.jsonl` (6 baskets), `catalyst_cycle_14-22.md` (latest cycle, generated 17:22 EEST — already fresh, no CLI regeneration needed).
- LLM packet: `data/processed/llm_analysis_packet.md` (fresh, generated 17:52 EEST, swing mode).
- CLI: `active-signals` (crypto ×19, stocks ×50), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-07-26` (clean — no untracked crypto alerts).
- Direct `news_items` SQLite queries (last 24h) for EUL, ZAMA, KAITO, DIA, ARX, BANK — confirmed EUL's Upbit-KRW-listing news exists but is unmapped/mismapped (`detected_symbols_json` empty or wrong); confirmed DIA's and ARX's 24h "matches" are pure ticker-substring collisions (unrelated wire stories containing the letter sequences "dia"/"arx").
- Scheduler cycle log: `data/scheduled_runs/2026-07-26_default_schedule/cycle_01_16-59_summary.md` — 61/63 steps OK, 2 failed (MEXC parity exits: transient connection errors; crypto swing versioned shadow sweep: timeout, both shadow-only/non-blocking). News source health monitor: 41 OK / 0 error / 0 stale / 0 dead. News entity resolver: 100% resolved, 0 unresolved symbol-tagged rows in 24h/72h windows.
- External web research: 2 WebSearch queries (BTC/Iran-Hormuz macro cross-check; EUL/Upbit-KRW listing corroboration) + 1 WebFetch (TradingView/CoinMarketCal EUL listing article, confirmed dated 2026-07-26) — see §13.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-26_1620.md`.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime 2026-07-26 17:56 EEST, latest cycle (`cycle_01_16-59_summary.md`) finished 17:56:56 EEST — both well under the 3h defer threshold at run time (18:39). **Not deferred.**
- Monitors all writing fresh: `pending_monitor` through 18:39 (active, largest log this cycle — 602KB), `fast_news_monitor` through 18:38, `derivatives_monitor` through 17:04/17:43 (canary), `telegram_dashboard` through 17:02 — all alive.
- Scalp/intraday/swing reports: all regenerated this cycle (17:08-17:52 EEST), all fresh (<1.5h old at run time).
- Stocks: closed by design — Sunday, `weekend (crypto-only)` mode confirmed in cycle summary header (`Stocks enabled: False`). No fresher data possible until Monday pre-market.
- Catalyst folder for 2026-07-26 fresh (latest cycle 17:22 EEST) — no regeneration needed.
- News infra health: source health monitor OK across all 41 sources, entity resolver 100% resolved with 0 unresolved symbol-tagged rows — no ingest-pipeline concerns this cycle.
- Two non-blocking step failures in the latest cycle: "MEXC parity exits (shadow-only)" and "crypto swing versioned shadow sweep (counterfactual)" — both shadow/read-model only, isolated to this cycle (not recurring across the last 3 days checked), likely transient network blips (consistent with other steps this cycle also logging `ConnectionError`/`HTTPError` against Gemini/Deribit). No live/scoring impact.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-07-26 18:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["stocks fresh RTH data (market closed, Sunday)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log / cycle summary ~43min old at run time", "scalp/intraday/swing reports all regenerated this cycle, 17:08-17:52 EEST", "stocks reports stale by design (weekend mode, stocks disabled)", "news source health 41 OK/0 error/0 stale/0 dead", "news entity resolver 100% resolved, 0 unresolved symbol-tagged rows", "2 non-blocking shadow-step failures this cycle, isolated/non-recurring"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chop", "mixed", "risk_off", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC regime range/chop, ETH uptrend (unchanged since 16:20)", "altcoin breadth 56.41% above EMA20 (up from 48.72% at 16:20 — improving, not yet a broad confirmation)", "macro risk 79.9/100 (up from 72.3/100 at 16:20) on fresh Iran/Hormuz tanker-attack and blockade-enforcement headlines", "external WebSearch corroborates real escalation: Bitcoin fell below $63K on tanker attacks, Iran declared the Strait 'closed until further notice'", "stocks fully closed (Sunday, weekend crypto-only mode)"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "catalyst_confirmed", "no_catalyst", "mapping_weak"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["1904 catalyst events today, 1131 unmapped (59.4%) — weak mapping this run", "EUL/USDT Upbit-KRW listing externally reconfirmed via WebSearch+WebFetch (TradingView/CoinMarketCal, livebitcoinnews — dated 2026-07-26), yet both intraday and swing reports still show catalyst_news 6.8/10 'no fresh verified catalyst detected' — mapper miss persists a 3rd consecutive cycle (11:44 -> 16:20 -> 18:39)", "DIA/USDT's 16:20 false-positive catalyst tag has resolved organically — dropped out of momentum_breakout basket this cycle, now correctly shows catalyst_news 6.8 'no fresh verified catalyst'", "NEW: ARX/USDT direct news_items query (24h) returns only an unrelated 'USARx' stock-listing headline — same ticker-substring-collision pattern as the DIA false positive, third confirmed instance of this resolver bug class"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "oi_contradicts", "oi_supports", "data_unavailable"], "data_missing": ["OI history for several MEXC-only names"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ARX/USDT newly capped to C on the intraday timeframe this cycle for thin_liquidity_short_squeeze_risk (not flagged at 16:20) while the swing timeframe still lists it as an actionable watchlist short — a timeframe conflict worth caution", "ARX funding flat (5e-05), OI -5.07% — deleveraging/long-liquidation, consistent with the short thesis", "KAITO/USDT price up + OI up (+5.88%), volume 2.18x — fresh positioning confirms trend, but price already >2 ATR from EMA20 (do not chase)", "ZAMA/USDT flipped from long RS-leader (+11.46%/24h, volume 1.21x at 16:20) to weak_rs_short (-3.85%/24h) this cycle — full reversal, treat prior long thesis as invalidated"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["overextended", "chase_risk", "price_moved_away", "entry_late"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["EUL/USDT price 2.378, still above both the intraday pullback zone (2.224-2.331) and the registered swing signal's entry zone (2.1065-2.2183); volume still 0.27x, below average — unconfirmed pullback persisting a 3rd cycle", "KAITO/USDT +25.61%/24h with genuine 2.18x volume confirmation, flagged extended_from_ema20 / '>2 ATR from EMA20, do not chase' — best RS-leader long structurally, but needs a pullback first, no confirmed entry zone published yet", "ARX/USDT at 0.1690, just below its 0.1697-0.1713 failed-bounce/retest zone — needs the bounce first, then a 1h close back below ~0.1670", "DIA/USDT cooling all day (51.1% -> 37.6% /24h), no longer catalyst-tagged, now just fading momentum, not an attractive long or short"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.6,
      "reason_codes": ["waiting_for_entry", "entered_unresolved", "review_shadow", "needs_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["19 crypto active-signals: 4 now waiting_for_entry (DIA/PENGU/EPIC/EUL, swing, expires 2026-08-02) — newly registered this cycle when the swing report regenerated at 17:52, a change from 16:20's zero waiting-for-entry; 15 entered_unresolved (tp1_hit/tp2_hit with expires_at 4-9 days in the past, unchanged pattern from 04:40/11:44/16:20)", "50 stocks active-signals: 15 genuinely future-dated (invest-mode, 2026-07-31/08-01 expiries, unresolved by design given 30d+ horizon), 35 past-expiry entered_unresolved — unchanged from 16:20", "~13 unique crypto watchlist/C-tier names surfaced across scalp+intraday+swing this cycle (EUL, DIA, ARX, ZAMA, KAITO, EPIC, PENGU, RE, SYN, SHIB, RIF, LTC, DEXE) — none actionable, all review/shadow", "detect_untracked_legacy_alerts: clean, 0 untracked crypto alerts"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["headline_risk", "reduce_risk", "correlation_cluster"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TSLA (Musk SEC-settlement disclosure fine) and UNH (DOJ antitrust/fraud probe into Medicare billing, recurring across 5+ outlets) legal-risk headlines recur again today's catalyst top-importance list, unchanged/carried — stocks closed (Sunday), not re-verifiable live this cycle", "macro geopolitical risk score rose to 79.9/100 (from 72.3 at 16:20) on fresh Hormuz tanker-attack/blockade headlines, externally corroborated — system's own macro note says 'reduce alt long aggression'", "NVDA exploit_hack operator-review advisory carried (Jensen Huang / Hugging Face reference, display-only, does not gate routing)"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto weekly stats: tier=B swing n=37, PF 3.91, avgR +1.00 (working well); intraday n=70, PF 1.44, avgR +0.19 (working); scalp n=42, PF 0.42, avgR -0.18 (losing, correctly kill-switched off — zero scalp ideas surfaced this whole cycle)", "stocks: headline A/B sample=0 this week (by design — C-tier never actionable per position-framework hardening); C-tier watchlist PF 0.56, avgR -0.10 (expected research-grade underperformance, closed all Sunday anyway)"] },
    { "agent": "head_trader", "verdict": "caution",
      "reason_codes": ["wait_for_trigger", "mapping_weak", "chase_risk"],
      "data_missing": [], "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.55,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": { "symbol": "KAITO/USDT", "trigger": "wait for a pullback of at least 1 ATR (~5%) toward EMA20 with volume holding above 1x of the 20-period average before considering long; do not chase the current +25.6%/24h print (>2 ATR extended, scanner-rejected for chase risk)", "reason": "cleanest RS-leader with genuine volume confirmation (2.18x, OI +5.88%) on today's board, but currently too extended to enter" },
    "best_short_candidate": { "symbol": "ARX/USDT", "trigger": "bounce into 0.1697-0.1713 followed by a 1h close back below ~0.1670 support; confirm no active squeeze before entering", "reason": "clean C-tier failed-bounce/deleveraging structure (OI -5.07%, price 0.1690 just below the zone), but this cycle's intraday timeframe newly flags thin_liquidity_short_squeeze_risk on the same name — treat with reduced confidence vs the 16:20 pick" },
    "best_catalyst_candidate": { "symbol": "EUL/USDT", "trigger": "pullback into 2.224-2.331 (intraday) / 2.1065-2.2183 (registered swing waiting_for_entry signal) with volume confirmation (still 0.27x, below average) — do not chase the current 2.378", "reason": "Upbit KRW listing externally reconfirmed today (WebSearch+WebFetch, TradingView-dated 2026-07-26), but internal catalyst mapper still misses it (score 6.8/10, unresolved 3rd cycle running)" },
    "avoid_candidate": { "symbol": "BEAT/USDT", "reason": "MEXC-only listing (exchange confirmation missing), no real catalyst_events match, scanner confirmation only 38-46/100 — unchanged avoid from the 16:20 review" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.55 | chop, mixed, risk_off, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, catalyst_confirmed, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, oi_contradicts, oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | overextended, chase_risk, price_moved_away, entry_late | advisory_only |
| execution_lifecycle | needs_review | 0.60 | waiting_for_entry, entered_unresolved, review_shadow, needs_review | advisory_only |
| risk_manager | caution | 0.55 | headline_risk, reduce_risk, correlation_cluster | advisory_only |
| playbook_performance | caution | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.55 | wait_for_trigger, mapping_weak, chase_risk | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-07-26_1620.md` (pre-US-open decision review, 16:31 EEST):

- **New / reversal:** ZAMA/USDT flipped completely — from 16:20's cleanest volume-backed long-watch (+11.46%/24h, +62.41%/7d, volume 1.21x) to a `weak_rs_short` C-tier name this cycle (-3.85%/24h, RS vs BTC -4.59%). The prior long thesis is invalidated, not carried forward.
- **New:** A third confirmed instance of the ticker-substring-collision resolver bug — ARX/USDT's only 24h `news_items` match is an unrelated "USARx" stock-listing headline, mirroring the DIA false-positive pattern from 16:20. Folded into the existing TODO (§14) rather than raised separately.
- **Resolved (organically):** DIA/USDT's 16:20 catalyst-tag false positive is gone — DIA dropped out of the `momentum_breakout` basket this cycle and now correctly shows `catalyst_news: no fresh verified catalyst detected`. The underlying resolver bug is not fixed (see ARX above), but this specific mischaracterization did not recur.
- **New:** 4 swing signals (DIA, PENGU, EPIC, EUL) moved to `waiting_for_entry` status when the daily swing report regenerated at 17:52 EEST — up from 0 at 16:20. All 4 are the same names that were C-tier/B-tier watchlist ideas in the prior two reviews; no fresh independent thesis, just formal registration on the book.
- **Unchanged/carried:** EUL/USDT's Upbit-KRW-listing catalyst mapper miss, unresolved for a 3rd consecutive cycle (11:44 -> 16:20 -> 18:39); price has drifted slightly higher (2.420 -> 2.378) and remains above its pullback zones without volume confirmation (0.27x). ARX/USDT remains the best short-watch structurally but now carries a fresh intraday-timeframe squeeze-risk caveat not present at 16:20. Macro/geopolitical risk moved from 72.3/100 (16:20) back up to 79.9/100 on fresh Hormuz tanker-attack/blockade headlines — the same fragile, not-durably-de-escalating cycle flagged across the last several reviews. TSLA/UNH legal-risk headlines recur unchanged. Scalp mode remains correctly kill-switched off (zero ideas). Stocks fully closed all day (Sunday).
- **Thesis status:** BANK/USDT long-watch, mentioned as a fallback in earlier reviews, was not present in this cycle's active watchlist output at all (thin volume, dropped off the radar) — not re-raised this cycle.

## 5. Catalyst Coverage

- Total `catalyst_events` today: **1904**. Mapped (non-null symbol): **773** (40.6%). Unmapped: **1131** (59.4%).
- `narrative_baskets`: **6** (rwa_narrative/ONDO+XLM, delisting_thin_liquidity/no primary, ai_narrative/NEAR+RENDER+TAO+FET, perps_dex_narrative/HYPE, binance_ecosystem_teaser/BNB, momentum_breakout/KAITO).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top unmapped headlines by importance score are routine class-action solicitation wire spam (unchanged pattern from 16:20): "VRRM Deadline: VRRM Investors Have Opportunity to Lead Verra Mobility Corporation Securities Fraud Lawsuit" (PR Newswire, 0.73), "GPGI, CMPO Investors Have Opportunity to Lead GPGI Securities Fraud Lawsuit" (PR Newswire, 0.73), "Zillow Deadline: Z, ZG Investors Have Opportunity to Lead Zillow Group Securities Fraud Lawsuit" (PR Newswire, 0.71) — not missed genuine catalysts. The operationally consequential unmapped row this cycle is lower down the importance ranking but far more material: "Upbit Will List EUL" (t.me/AstronomicaNews) — the same EUL listing catalyst that remains unmapped for a 3rd cycle (§4, §14).

## 6. Market Landscape

**Crypto:** BTC trend `range/chop`, ETH trend `uptrend` (unchanged since 16:20). Altcoin breadth improved to 56.41% above EMA20 (from 48.72% at 16:20) but not yet a broad confirmation either way. Macro/geopolitical risk score **79.9/100** (8 risk-off hits, 0 risk-on, 3 calendar/watch), up from 72.3/100 at 16:20 on fresh Iran/Hormuz tanker-attack and US-forces-blockade-enforcement headlines — externally corroborated via WebSearch (Bitcoin fell below $63K on tanker attacks; Iran declared the Strait "closed until further notice" during escalations). Treat the risk uptick as confirmed-fresh, not stale. Strongest names: KAITO (+25.61%/24h, volume 2.18x confirmed, but >2 ATR extended — do not chase), EUL (+50.13%/24h per intraday read, pulling back from its listing spike, still no volume confirmation), DIA (+37.56%/24h, cooling all day from +51%, no longer catalyst-tagged), ESP (+45.86%/24h, volume 50x, extended/overextended flag). Weakest/reversed: ZAMA (-3.85%/24h, full reversal from long to weak-short this cycle), DEXE (-24.93%, still a fade), RE/SYN/RIF (all weak_vs_market, thin). Production risk warnings carried: NVDA (exploit_hack, operator-review advisory, display-only), BTC (geopolitical_risk), ETH (two bridge exploits ~$31.7M combined, staking halted on a third protocol — risk-only).

**Stocks:** Fully closed — **today is Sunday, there is no US cash open at all this slot** despite the slot's default "US open reaction" label; next open is Monday 2026-07-27 ~16:30 EEST. Weekend crypto-only mode confirmed in this cycle's scheduler header (`Stocks enabled: False`). No fresh RTH data possible. Carried, not re-verified this cycle: TSLA (Musk SEC-settlement disclosure fine) and UNH (DOJ antitrust/fraud probe into Medicare billing, recurring across 5+ outlets) both carry legal-risk flags; treat as AVOID/manual-review if either resurfaces as an A/B candidate Monday. No fresh stocks A/B candidates exist or are possible this slot (headline sample=0 this week, per signal-stats; all 50 active stocks signals are C-tier, watchlist/research-grade by design).

### Market Mood / Risk Routing

- Crypto mood: **chop / mixed, risk-off intensifying again (79.9/100, up from 72.3)**
- Stocks mood: **closed** (Sunday — no session today; reopens Monday 2026-07-27, ~16:30 EEST)
- Dominant narrative: EUL/USDT's Upbit-KRW-listing pullback (still unconfirmed by volume, still mismapped internally); KAITO/USDT's clean RS-leadership but chase-risk extension; ZAMA/USDT's full long-to-short reversal; Iran/Hormuz macro risk re-intensifying on fresh tanker-attack/blockade headlines
- Preferred side now: **wait-for-trigger** — no clean chase-free long, short, or catalyst-backed trade; KAITO is the cleanest technical long-watch (needs a pullback first), ARX the cleanest (but now squeeze-flagged) short-watch, EUL the best (imperfect, still-mismapped) catalyst story
- Best long candidate: KAITO/USDT — trigger: ≥1 ATR pullback toward EMA20 holding >1x volume
- Best short candidate: ARX/USDT — trigger: failed bounce into 0.1697-0.1713 then 1h close back below ~0.1670 (confirm no squeeze first)
- Best catalyst-backed candidate: EUL/USDT — trigger: pullback into 2.224-2.331 (intraday) or 2.1065-2.2183 (registered swing signal) with volume confirmation (do not chase 2.378)
- What to avoid: chasing KAITO/USDT at its current extension (>2 ATR from EMA20); ZAMA/USDT on stale long bias (thesis reversed this cycle); BEAT/USDT (thin, MEXC-only, no real catalyst)
- What would change the view: a Hormuz de-escalation confirmation holding >12h, BTC reclaiming its local range-top structure, or KAITO/EUL printing volume-confirmed pullback holds

## 7. Candidate Deep Dives

### KAITO/USDT — RS-leader long-watch, extended (WATCHLIST ONLY)

- Has price already reacted? Yes — +25.61%/24h, +8.58%/4h, trend_score 100.0. The move already happened; this is not a fresh trigger.
- Chasing? Yes if entered now — flagged `extended_from_ema20`, >2 ATR from EMA20 per the scanner's own chase-risk gate.
- Retest/pullback structure? Not yet defined with an exact zone in this cycle's output; 1h change is already -2.19%, an early pullback tick worth watching for continuation.
- Overextended? Yes, explicitly flagged.
- Late now? Yes.
- What makes it actionable? A clean pullback of roughly 1 ATR (~5%, ATR% 5.08) toward EMA20 that holds with volume still above ~1x of the 20-period average (current volume_anomaly 2.18x, well above average — the key confirming signal on this name).
- Mood alignment: consistent with "prefer RS-leader longs" under an improving-breadth, still-choppy regime.
- Long/short/wait: wait-for-trigger long.
- Actionable now or after confirmation: after confirmation (pullback + volume hold).
- Invalidation: a close back below the pre-move base, or BTC/ETH breaking down against the broader thesis.
- Chase-risk setup: yes, explicitly.
- Catalyst confirmation/contradiction: none — pure RS/momentum play, no catalyst tag this cycle.
- Chart: `TradingView / manual chart check unavailable` — no chart MCP loaded; figures above are from local OHLCV/ATR/EMA fields only, no fabricated chart observations.

### EUL/USDT — catalyst-backed long-watch, unconfirmed pullback (WATCHLIST ONLY / registered swing waiting_for_entry)

- Has price already reacted? Yes — 24h return 50.13% (intraday read) / 39-51% range across today's cycles, driven by the confirmed Upbit KRW listing.
- Chasing? Current price 2.378 sits above both the intraday (2.224-2.331) and registered-swing (2.1065-2.2183) entry zones — entering now would be chasing.
- Retest/pullback structure? Defined but not yet touched; volume remains 0.27x of average, well below the confirmation bar.
- Overextended? Less extreme than KAITO but still above every defined entry zone.
- Late now? Yes, at the current price.
- What makes it actionable? A close inside the 2.224-2.331 (or lower, 2.1065-2.2183) zone with volume turning up toward or above 1x.
- Mood alignment: the desk's cleanest catalyst-backed idea this cycle despite the persistent mapping miss (external verification via WebSearch+WebFetch confirms the Upbit KRW listing is genuine and dated today, 2026-07-26).
- Long/short/wait: wait-for-trigger long.
- Actionable now or after confirmation: after confirmation (pullback + volume).
- Invalidation: 1h close beyond 2.093 (intraday) / beyond 1.9699 (registered swing signal).
- Chase-risk setup: yes at current price.
- Catalyst confirmation/contradiction: confirmed externally (Upbit KRW listing, live 2026-07-26 per TradingView/CoinMarketCal, livebitcoinnews); internal mapper still fails to tag it — treat the internal `catalyst_news: 6.8/10` score as an undercount, not evidence of no catalyst.
- Chart: unavailable, same caveat as above.

### ARX/USDT — failed-bounce short-watch, cross-timeframe squeeze caveat (WATCHLIST ONLY)

- Has price already reacted? Partially — -2.93%/24h, downtrend, OI -5.07% (deleveraging).
- Chasing? No — price (0.1690) sits just below the proposed zone, needs the bounce first, not a chase.
- Retest/pullback structure? Yes — failed-bounce/retest zone 0.1697-0.1713 defined by the swing scanner.
- Overextended? No.
- Late now? No, structurally early — the setup requires waiting for the bounce.
- What makes it actionable? A bounce into 0.1697-0.1713 followed by a 1h close back below ~0.1670 support.
- Mood alignment: fits "prefer clean liquid shorts" under the risk-off-leaning mood, though liquidity itself is the caveat here (MEXC-only, high_risk_only, confirmation only 38/100).
- Long/short/wait: wait-for-trigger short.
- Actionable now or after confirmation: after confirmation (bounce + rejection).
- Invalidation: 1h close beyond 0.1733 (swing) / BTC/ETH reclaiming local levels.
- Chase-risk setup: no.
- Catalyst confirmation/contradiction: none genuine — the only 24h `news_items` match for "ARX" is an unrelated "USARx" stock-listing headline (ticker-substring collision, §14 TODO); treat as no-catalyst, pure technical short.
- **New this cycle:** the intraday-timeframe scan separately caps ARX to C for `thin_liquidity_short_squeeze_risk` — a caveat not present at 16:20. Confirm no active squeeze condition before treating the swing-timeframe short structure as clean.
- Chart: unavailable, same caveat as above.

### ZAMA/USDT — reversed from long to weak short (WATCHLIST ONLY, thesis invalidated)

- Has price already reacted? Yes, in the opposite direction from 16:20 — now -3.85%/24h vs +11.46%/24h at 16:20, a full reversal within one cycle.
- Chasing? Not assessed as a fresh short idea — this entry exists to flag the reversal, not to propose a new trade.
- Retest/pullback structure? Not defined this cycle (tagged `weak_rs_short`, shadow/C-tier, low_volume_ratio).
- Overextended? No specific flag.
- Late now? N/A — no active proposal.
- What makes it actionable? Nothing proposed this cycle; needs its own confirmed short structure (bearish HTF structure + derivatives confirmation + clear stop above swing high) before consideration, per the report's own playbook note.
- Mood alignment: the reversal itself is the signal — a reminder that today's RS leaders can flip within a single 2-3h scheduler cycle in this chop/mixed regime.
- Long/short/wait: no directional call this cycle — informational only.
- Actionable now or after confirmation: not actionable.
- Invalidation: N/A (no active thesis).
- Chase-risk setup: N/A.
- Catalyst confirmation/contradiction: none.
- Chart: unavailable, same caveat as above.

## 8. Best Candidates Ranked

1. **Best long-watch: KAITO/USDT** — trigger: ≥1 ATR pullback toward EMA20 holding >1x volume (currently 2.18x, well-confirmed). Do not chase the current +25.6%/24h extension.
2. **Best short-watch: ARX/USDT** — trigger: bounce into 0.1697-0.1713 then 1h close back below ~0.1670. Confirm no active squeeze first (intraday timeframe flags thin-liquidity squeeze risk this cycle).
3. **Best catalyst-watch: EUL/USDT** — trigger: pullback into 2.224-2.331 (or lower, 2.1065-2.2183) with volume turning up toward 1x. Catalyst externally confirmed, internally still mismapped.
4. No clean A/B trade exists this cycle — all three above are wait-for-trigger watchlist ideas, not open-actionable positions.

## 9. Avoid / No Trade

This decision window only — scanning, tracking, and monitors all continue regardless.

- **BEAT/USDT** — MEXC-only listing, confirmation 38-46/100, no genuine catalyst match, unchanged avoid from 16:20.
- **KAITO/USDT at current price** — do not chase the extension; wait for the pullback defined in §7/§8.
- **ZAMA/USDT on the old long thesis** — that thesis reversed this cycle; do not act on stale 16:20 context.
- **DIA/USDT** — cooling momentum (+37.6%/24h, down from +51%), no catalyst, no clean structure either direction; skip.
- No blanket crypto no-trade call — this applies to the specific names above only; the scanner, tracker, and monitors continue running.

## 10. Main Risks

- Ticker-substring-collision resolver bug (DIA, ARX confirmed false-positive matches; EUL confirmed false-negative miss) continues to distort catalyst characterization across at least 3 symbols and 3+ review cycles — treat any catalyst_news score near the "no fresh catalyst" floor with skepticism until a human resolver audit lands (§14).
- Macro/geopolitical risk re-intensified to 79.9/100 on fresh, externally-corroborated Iran/Hormuz tanker-attack and blockade headlines — not a durable de-escalation; alt-long aggression should stay reduced per the system's own macro note.
- ARX/USDT carries a cross-timeframe conflict this cycle (swing: clean actionable watchlist short; intraday: newly squeeze-capped) — a reminder that timeframe-specific caps can diverge and should both be checked before treating a name as clean.
- Stocks fully closed all day; TSLA/UNH legal-risk headlines are carried context only and must be re-verified fresh before any Monday A/B consideration.

## 11. Action Plan — next 4 hours

- Watch KAITO/USDT for a pullback toward EMA20 with volume holding; do not chase the current print.
- Watch ARX/USDT for a bounce-then-rejection into 0.1697-0.1713, but re-check squeeze-risk status before treating it as clean.
- Watch EUL/USDT for a volume-confirmed pullback into its defined zones; treat the Upbit KRW listing as a real, live catalyst despite the internal mapping miss.
- No new stocks activity possible or expected before Monday's pre-market/cash open.
- Re-verify macro/Hormuz headlines next cycle for confirmation vs further escalation before adjusting alt-long risk appetite.

## 12. Final Verdict per Mode

- **Crypto scalp:** No trade — correctly kill-switched off (losing PF 0.42 bucket), zero ideas surfaced.
- **Crypto intraday:** Watchlist only (EUL, DIA) — no A/B, wait for confirmation.
- **Crypto swing:** Watchlist / waiting-for-entry only (DIA, PENGU, EPIC, EUL registered; ARX, KAITO, ZAMA, others C-tier) — no open-actionable trade this cycle.
- **Stocks (all modes):** Market closed (Sunday) — no trade possible, planning/watchlist context only pending Monday's open.

## 13. Sources

- [Bitcoin Retraces As Oil Tanker Attacks in Strait of Hormuz Escalate U.S.-Iran Tensions](https://coingape.com/bitcoin-retraces-as-oil-tanker-attacks-in-strait-of-hormuz-escalate-u-s-iran-tensions/) — CoinGape, corroborates the fresh Hormuz/tanker-attack macro risk uptick.
- [U.S.-Iran War: Iran Claims Tanker Attacks as War Pushes Brent Crude Past $90, Bitcoin Falling](https://coingape.com/iran-claims-tanker-attacks-as-war-pushes-brent-crude-past-90-bitcoin-falling/) — CoinGape, corroborates Bitcoin's risk-off reaction to the tanker attacks.
- [Bitcoin Drops Below $63K as Trump Resumes Iran Strikes While Oil Jumps 4.5%](https://news.bitcoin.com/bitcoin-holds-64k-us-iran-strikes-oil-jumps/) — Bitcoin.com News, corroborates the price impact of the escalation cycle.
- [Upbit Lists Euler (EUL) on KRW Market as Token Jumps Into Spotlight](https://www.livebitcoinnews.com/upbit-lists-euler-eul-on-krw-market-as-token-jumps-into-spotlight/) — LiveBitcoinNews, corroborates the EUL catalyst.
- [Euler: EUL enters Upbit's KRW market — By 26 Jul 2026](https://www.tradingview.com/news/coinmarketcal:8bf54e85e094b:0-euler-eul-enters-upbit-s-krw-market-by-26-jul-2026/) — TradingView/CoinMarketCal, WebFetch-verified, dated 2026-07-26, confirms the listing is genuine but cautions it "does not by itself demonstrate wider adoption or a sustained market effect."
- Internal: `data/reports/scalp/2026-07-26_14-08_scalp_report.md`, `data/reports/intraday/2026-07-26_14-16_intraday_report.md`, `data/reports/swing/2026-07-26_14-52_swing_report.md`, `data/catalysts/2026-07-26/catalyst_cycle_14-22.md`, `data/scheduled_runs/2026-07-26_default_schedule/cycle_01_16-59_summary.md`.

## 14. Fix Requests / TODO

### TODO-catalyst-symbol-substring-collision (carried, evidence upgraded to 3 confirmed instances — priority raised)
- **issue:** The catalyst/news symbol resolver has (at least) two failure modes affecting the same component: (a) **false-positive substring collisions** — short crypto tickers matching unrelated words/tickers embedded in longer headlines or other symbols (DIA/USDT matched generic "...dia..." wire-story substrings at 16:20; ARX/USDT this cycle matched only an unrelated "USARx" stock-listing headline in its 24h `news_items` window); (b) **false-negative mapping misses** — genuine listing-announcement catalysts (e.g., "Upbit Will List EUL") failing to populate `detected_symbols_json`/`symbol` for the actual token, unresolved for EUL across 3 consecutive review cycles (11:44, 16:20, 18:39).
- **evidence:** direct `news_items` SQLite queries (last 24h) for DIA, ARX, EUL run this cycle and at 16:20; `data/catalysts/2026-07-26/catalyst_events.jsonl` unmapped-row scan showing "Upbit Will List EUL" with empty symbol; `data/reports/intraday/2026-07-26_14-16_intraday_report.md` and `data/reports/swing/2026-07-26_14-52_swing_report.md` both showing EUL `catalyst_news: 6.8/10, no fresh verified catalyst detected` despite the externally-confirmed listing.
- **suggested manual fix:** unchanged from 16:20 — a human-driven session should audit the symbol/catalyst resolver for (1) word-boundary-aware ticker matching to prevent substring collisions, and (2) whether listing-announcement title patterns ("X Will List Y") are parsed for the listed symbol specifically. Now 3 confirmed real-symbol instances across 3 cycles — recommend treating this as a single resolver-disambiguation ticket rather than one-off false positives.
- **priority:** high (raised from medium — recurring across 3+ cycles and now 3 distinct symbols; actively distorts catalyst characterization on the desk's own watchlist candidates).
- **first observed:** 2026-07-26 11:44 EEST (EUL miss); 2026-07-26 16:31 EEST (DIA false positive); re-confirmed and expanded (ARX false positive) 2026-07-26 18:39 EEST (this run).

### TODO-stale-active-signals (carried, unchanged)
- **issue:** `active-signals` continues to list crypto and stocks signals with `expires_at` dates in the past while still showing `tp1_hit`/`tp2_hit`/`triggered` status rather than a terminal closed state. As of this run, 15 of 19 crypto actives are past-expiry (the other 4 are the newly-registered swing waiting_for_entry signals, future-dated); 35 of 50 stocks actives are past-expiry, the remaining 15 (invest-mode) are future-dated. Same pattern flagged in the 04:40, 11:44, and 16:20 reviews.
- **evidence:** `python -m src.cli active-signals --asset-class crypto` (19 rows, 15 past-expiry); `python -m src.cli active-signals --asset-class stocks` (50 rows, 35 past-expiry).
- **suggested manual fix:** unchanged from prior reviews — confirm whether `active-signals` should filter on `expires_at`, or add an explicit `past_expiry`/`entered_unresolved` flag column so reviews don't need to eyeball dates.
- **priority:** low (no functional/routing impact observed; readability issue for manual review only).
- **first observed:** carried context from multiple prior reviews; re-raised 2026-07-26 18:39 EEST.

### TODO-mexc-parity-exits-transient-failure (new, low priority)
- **issue:** The "MEXC parity exits (shadow-only, 1m candles)" scheduler step failed this cycle with a connection-level error (urllib3 `ConnectionError`); the "crypto swing versioned shadow sweep (counterfactual)" step also failed (timeout, exit=-1). Both are shadow-only/counterfactual, non-blocking, and not observed in the prior 2 days of cycle logs checked — likely a transient network blip (other steps this cycle also logged isolated `ConnectionError`/`HTTPError` against Gemini and Deribit).
- **evidence:** `data/scheduled_runs/2026-07-26_default_schedule/cycle_01_16-59_summary.md`, steps 9 and 49 (both marked `[FAIL]`).
- **suggested manual fix:** no action needed unless this recurs across multiple cycles — if it does, audit outbound connectivity/rate-limiting for the MEXC parity-exit and swing-shadow-sweep steps specifically.
- **priority:** low (shadow-only, isolated, no live/scoring impact).
- **first observed:** 2026-07-26 17:56 EEST (this cycle).

## Telegram

```
[AUTO-REVIEW US open reaction 18:39 EEST]

Mood:
- Crypto: chop/mixed, risk-off intensifying (79.9, up from 72.3)
- Stocks: closed (Sunday — no session today)
- Prefer: wait-for-trigger

Status:
- Open actionable: 0
- Waiting for entry: 4 (crypto swing: DIA, PENGU, EPIC, EUL — newly registered this cycle)
- Review/Shadow: 13 unique crypto watchlist/C-tier names (EUL, DIA, ARX, ZAMA, KAITO, EPIC, PENGU, RE, SYN, SHIB, RIF, LTC, DEXE)
- Entered unresolved: 15 crypto + 35 stocks (past-expiry tp1/tp2_hit/triggered, see TODO)
- No-entry/stale/moved-away: not distinctly surfaced by current tooling
- Needs review: 3 (catalyst substring-collision resolver [raised to high], stale active-signals readability, MEXC parity-exits transient failure)

Decisions:
- Long-watch:     KAITO/USDT trigger pullback >=1 ATR toward EMA20 holding >1x volume, don't chase +25.6%/24h
- Short-watch:    ARX/USDT trigger bounce into 0.1697-0.1713 then 1h close <0.1670 (confirm no squeeze first)
- Catalyst-watch: EUL/USDT trigger pullback into 2.224-2.331 with volume confirm; Upbit KRW listing externally confirmed, still internally mismapped
- Avoid:          BEAT/USDT MEXC-only, no real catalyst, confirmation 38-46/100

Risk:
- Macro/Hormuz risk re-intensified to 79.9/100 (externally corroborated); ZAMA/USDT fully reversed from long to weak-short this cycle — don't act on stale 16:20 context.

Catalyst coverage: mapped 773/1904 (40.6%), baskets 6
                   weak this run — context only

File: OPUS_ENRICHED_REVIEW_LATEST.md
Advisory only. No auto-trade.
```
