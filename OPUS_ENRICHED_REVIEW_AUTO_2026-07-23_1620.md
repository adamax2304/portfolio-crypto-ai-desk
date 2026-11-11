# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:20 EEST

## 1. Executive Summary

Slot: **pre-US-open decision review** (16:20 EEST, 2026-07-23, ~10 min before / right at the US cash open). **Advisory only — no auto-trade, no scoring/strategy changes.** This is a **gap-risk day**: internal Telegram-sourced feeds (t.me/BWEtradfi, t.me/ClashReport) report the S&P 500 opening ~1.1% lower and Nasdaq ~1.8% lower at 13:30 UTC, Brent crude topping $100/barrel for the first time since May, and a fresh Israel/US military escalation against Iran (Netanyahu's office statement). External WebSearch corroborates the underlying pattern — this is week 7+ of an ongoing US/Israel-Iran conflict that has repeatedly driven S&P/Nasdaq gap-downs and oil spikes on multiple dates this month (Jul 8/9/13/19/20/21/22) — though same-day (Jul 23) primary-source confirmation of the exact open print was not retrievable via WebSearch (search-index lag); treat the specific -1.1%/-1.8% print as single-source-internal, directionally consistent with the confirmed macro backdrop. Separately, ECB's Lagarde gave a downside-risk-tilted, energy-inflation-heavy speech today — another risk-off macro input. Internal macro risk score is 95.5/100, BTC bias "risk-off headwind." Crypto: BTC/ETH both read **range** (not the swing report's carried-forward "bullish/risk-on" — that divergence, flagged last cycle, persists and should be treated as stale). No new crypto A/B fired this cycle; book still all B-tier. Stocks: pre-gate A-tier ideas (XOM, XLE, NVDA, AMD, GOOGL-short, AVGO, JPM, META-short, XLV-short) are all demoted to C (market-closed-planning) as of the 10:27 UTC report — all need first-15-30min RTH confirmation before being treated as live, and the oil spike materially strengthens the energy-long thesis (XOM/XLE) while the AI-spending-selloff theme (CNBC: "Tesla and Alphabet shares slump as AI spending concerns spook investors," today) strengthens the growth/semis-short thesis. **GOOGL carries a verified fresh legal catalyst — an EU $1B/€890M Digital Markets Act antitrust fine, confirmed today via CNN/Semafor/wire — verdict is AVOID/MANUAL REVIEW, not a clean short**, despite the aligned macro thesis. UNH's DOJ investigation remains open/unchanged (re-verified, no fresh news in the last 48h). Catalyst mapping is weak this run (80.4% unmapped) — use catalyst layer as context only. Scanning, tracking, and monitors continue regardless of this review's caution stance.

## 2. Data Used

- Crypto reports: `2026-07-23_12-48_scalp_report.md` (mtime 15:48, ~0.7h old, fresh), `2026-07-23_12-54_intraday_report.md` (mtime 15:54, ~0.6h old, fresh)
- Swing report: `2026-07-23_03-05_swing_report.md` (mtime 06:05, ~10.3h old — **carry-forward**, 4-12h bucket; regime divergence vs intraday persists, same TODO as last cycle)
- Stocks intraday: `2026-07-23_10-27_stocks_intraday_report.md` (mtime 13:27, ~3.0h old, fresh — generated market-closed, planning-only; needs RTH confirmation at/after today's open)
- Stocks swing/invest: last available `2026-07-02_13-0x` reports (**~21 days stale**, unchanged — TODO-2 carried forward, not used)
- Catalyst layer: `data/catalysts/2026-07-23/catalyst_events.jsonl` (2,500 cumulative rows today), `narrative_baskets.jsonl` (5 baskets), `catalyst_cycle_13-02.md` (fresh, generated 16:02)
- LLM packets: `llm_analysis_packet.md` (crypto, mtime 15:54), `llm_stocks_packet.md` (stocks, mtime 13:29)
- CLI: `active-signals` (crypto ×26, stocks ×50), `signal-stats` (crypto + stocks), `detect_untracked_legacy_alerts --since 2026-07-23` (clean — no untracked alerts)
- Direct SQL against `db/crypto_ai_desk.sqlite` (`news_items`): last-3h feed scan (ECB Lagarde, S&P/Nasdaq open, Brent $100, Iran/Israel), UNH/DOJ re-check (no fresh news, confirms unchanged), catalyst mapped/unmapped ratio computed directly from JSONL (symbol='' = unmapped)
- External: WebSearch ×3 (S&P/Nasdaq open + Iran/oil context; GOOGL EU fine verification), WebFetch ×1 (investing.com Iran-tensions market article, for date/number cross-check)
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-23_1139.md` (11:39 EEST, Europe/pre-US slot) — used for §4 comparison

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: 2026-07-23 16:29 (fresh, ~5min old at read time) — not deferred
- Latest cycle summary in scheduled_runs folder: ~13:39 (well within defer threshold)
- Monitors alive and current: `derivatives_monitor` (16:26), `pending_monitor` (16:33), `stocks_monitor` (16:33), `mexc_canary_monitor` (16:17), `telegram_dashboard` (16:30) — all updated within the last ~15 minutes
- Crypto scalp/intraday fresh (<1h)
- Swing carry-forward (~10.3h) — regime divergence flagged (bullish/risk-on vs current range/mixed) — do not treat swing regime label as current
- Stocks intraday fresh (~3.0h) but generated market-closed — every candidate is `market_closed_intraday_planning_only`, none actionable pre-RTH-confirmation
- Stocks swing/invest ~21 days stale — not used (TODO-2, unchanged)
- Catalyst scan already present for today (latest cycle `catalyst_cycle_13-02.md`, 16:02) — no need to re-run the CLI

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-23 16:35 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "catalyst_missing"],
      "data_missing": ["stocks swing/invest ~21d stale", "same-day (Jul 23) primary-source confirmation of exact S&P/Nasdaq open print"],
      "suggested_effect": "advisory_only", "facts_used": ["scheduler.log 16:29", "monitor logs 16:17-16:33", "catalyst mapping 80.4% unmapped"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["risk_off", "mixed", "chop", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["macro risk score 95.5/100, BTC bias risk-off headwind", "BTC/ETH both range (intraday/scalp)", "swing report still reads bullish — stale divergence", "stocks regime=chop, VIX 17.70, S&P/Nasdaq reported gap-down at open", "Brent >$100/bbl", "ECB Lagarde downside-risk-tilted speech today"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "catalyst_confirmed", "no_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["80.4% unmapped catalyst events this run", "GOOGL EU $1B DMA fine confirmed via CNN/Semafor", "rwa_narrative basket (ONDO/XLM) fresh <6h", "momentum_breakout basket (BANK/AIXDROP/ZAMA) no confirmed catalyst"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.4,
      "reason_codes": ["data_unavailable", "funding_extreme"],
      "data_missing": ["OI change data (n/a across all crypto derivatives rows)"],
      "suggested_effect": "advisory_only", "facts_used": ["ZAMA/DEXE negative funding, crowding=elevated across external venues (bybit/mexc/okx)"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["entry_late", "stale_before_entry", "clean_retest", "chase_risk"],
      "data_missing": ["pre-market tick data for stocks candidates"],
      "suggested_effect": "advisory_only", "facts_used": ["WLFI/KAITO top RS with existing B-tier entries", "stocks pre-gate-A ideas frozen at 10:27 UTC close-of-data levels, need fresh RTH levels"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["waiting_for_entry", "open_actionable", "no_entry", "review_shadow"],
      "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["26 crypto active-signal rows (all B-tier), 50 stocks active-signal rows (all B/C), untracked-alert detector clean"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["headline_risk", "legal_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["GOOGL EU antitrust fine (verified today)", "UNH DOJ probe open/unchanged (re-verified, no update in 48h)", "geopolitical escalation (Iran/Israel) elevating tail risk into the US open", "LLY GLP-1 lawsuit (carried forward)"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["crypto scalp PF 0.67 (losing, n=44)", "crypto short direction PF 0.125 (n=8, anecdotal but consistently bad)", "crypto swing PF 3.00 best mode", "stocks tier=C triggered winrate 6%", "stocks short direction PF 1.10 vs long PF 0.75"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "catalyst_backed",
    "best_long_candidate":     { "symbol": "XOM", "trigger": "RTH open confirms hold above pre-close entry zone 153.98-154.45 with volume; oil spike + energy-sector RS leadership align", "reason": "pre-gate A (score 95.06), RS leader vs SPY/sector, catalyst = Brent >$100/bbl on Iran escalation, earnings-safe (7/31, 8 days out)" },
    "best_short_candidate":    { "symbol": "META", "trigger": "RTH open confirms breakdown continuation below pre-close short zone with volume; no legal/earnings flag today", "reason": "pre-gate A (score 80.96), downtrend + RS-leader-to-the-downside, aligned with today's AI-capex-spending-concern theme (CNBC), clean on legal/earnings axis" },
    "best_catalyst_candidate": { "symbol": "XLE", "trigger": "same RTH confirmation as XOM; sector-wide oil-shock beta", "reason": "pre-gate A (score 86.07), sector already RS-leader (20d RS vs SPY +6.82%) before today's fresh Brent >$100 catalyst" },
    "avoid_candidate":         { "symbol": "GOOGL", "reason": "verified fresh EU $1B/EUR890M DMA antitrust fine (today, confirmed via CNN/Semafor/wire) + earnings-reported AI-spending-selloff reaction stacked on a stale post-earnings setup — manual review required, never a clean actionable despite short-aligned thesis" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, catalyst_missing | advisory_only |
| market_regime | caution | 0.75 | risk_off, mixed, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.6 | mapping_weak, fresh_catalyst, catalyst_confirmed, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.4 | data_unavailable, funding_extreme | advisory_only |
| technical_entry | caution | 0.6 | entry_late, stale_before_entry, clean_retest, chase_risk | advisory_only |
| execution_lifecycle | ok | 0.8 | waiting_for_entry, open_actionable, no_entry, review_shadow | advisory_only |
| risk_manager | caution | 0.75 | headline_risk, legal_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.6 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | caution | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Compared to the 11:39 EEST (Europe/pre-US) review:

- **New, decision-relevant:** Confirmed today's fresh macro escalation — S&P/Nasdaq reported gap-down at the open, Brent crude topping $100/barrel (first time since May), fresh Israel/US-Iran military action headline, ECB Lagarde downside-risk speech. None of this was in the 11:39 review.
- **New, verified:** GOOGL EU $1B/€890M DMA antitrust fine — confirmed today via external search (CNN, Semafor, wire outlets). The 11:39 review already had GOOGL as avoid/manual-review (post-earnings stale setup); this adds a second, independent avoid reason.
- **Unchanged / carried forward:** UNH DOJ investigation (re-verified, no update); Wanchain/AFX/Verus-Ethereum bridge exploit cluster still present in today's top catalysts (ETH/ARB/BNB/ADA caution persists); stocks swing/invest still ~21 days stale; regime divergence between fresh intraday/scalp (range/mixed) and stale swing (bullish/risk-on) persists; catalyst mapping still weak (80.4% vs 79.1% at 11:39 — essentially unchanged, still the TODO-1 resolver defect).
- **Crypto book:** No new A/B fired since 11:39; same B-tier names (WLFI, BANK, RE, EPIC, ERA, TLM, ONDO, OPN, ZAMA, ADA, VIRTUAL, ALLO, PENGU, PUMP, KAITO, KITE, NEAR) at various lifecycle stages — no material tier upgrades/downgrades.
- **Stocks:** Same pre-gate-A candidate list (XOM, XLE, NVDA, AMD, GOOGL-short, AVGO, JPM, META-short, XLV-short) as the source report has not refreshed since 10:27 UTC (pre-open) — today's actual open (now imminent/occurring) has not yet produced a fresh RTH-confirmed report. This review's job is to hand off the pre-open read; the 18:30 US-open-reaction slot will confirm/invalidate.
- **Thesis change:** Previous review's best-long (TLM, momentum-only, no catalyst) is superseded this cycle by the oil-shock-driven XOM/XLE catalyst thesis, which is materially stronger (verified external catalyst vs. unconfirmed momentum-only breakout).

## 5. Catalyst Coverage

- Catalyst events today (cumulative): **2,500** total; mapped (non-null symbol): **490**; unmapped: **2,010** (**80.4% unmapped**).
- Narrative baskets: **5** (rwa_narrative, perps_dex_narrative, ai_narrative, binance_ecosystem_teaser, momentum_breakout).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines by importance: (1) "BSquared hack drains $3.9M — can B2 recover after a 44% crash?" (AMBCrypto, imp 0.748); (2) "Warren Buffett's Berkshire Hathaway Has Barely Touched AI Stocks..." (Motley Fool, imp 0.748); (3) "Why AFX Trade's $24.15M hack is another warning for crypto bridges" (AMBCrypto, imp 0.73). Root cause unchanged from TODO-1 (literal-ticker Binance/MEXC announcement formats resolving to null symbol) — the two highest-importance unmapped items here are narrative/opinion pieces (correctly symbol-less) rather than resolver failures, but the bulk of the 2,010 unmapped rows are still the known funding-rate/listing-notice pattern.

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **mixed, leaning risk-off** (BTC/ETH both range on the freshest data; macro risk score 95.5/100 with explicit "risk-off headwind" bias; swing report's "bullish/risk-on" read is stale — do not use it as current)
- Stocks mood: **risk-off at the open** (chop regime carried from the 10:27 UTC report, VIX 17.70 pre-open; today's reported S&P -1.1%/Nasdaq -1.8% open print plus Brent >$100 and the AI-capex-selloff theme in mega-cap tech/semis all point the same direction)
- Dominant narrative: geopolitical/oil-shock (Iran/Israel escalation, Brent >$100) is the macro overlay of the day; secondarily the AI-capex-spending-concern theme hitting GOOGL/TSLA/META/semis, and the crypto rwa_narrative (ONDO/XLM) as the cleanest catalyst-backed crypto story
- Preferred side now: **catalyst-backed** — energy-sector longs (XOM/XLE) aligned with the oil shock, selective growth/semis shorts aligned with the AI-capex theme, wait-for-trigger on momentum-only crypto names; avoid chasing gap moves in either direction without RTH/1h confirmation
- Best long candidate: **XOM** — RTH confirmation of hold above 153.98-154.45 with volume (see §8)
- Best short candidate: **META** — RTH confirmation of breakdown continuation with volume (see §8)
- Best catalyst-backed candidate: **XLE** — sector-wide oil-shock beta, already RS-leader before today's fresh catalyst (see §8)
- What to avoid: GOOGL (verified fresh legal risk + stale post-earnings setup), UNH (open DOJ investigation, unchanged), ETH/ARB/BNB/ADA (active bridge-exploit cluster), LMT/earnings-day names (do not chase into prints), crypto scalp mode generally (PF 0.67 this week), crypto short direction generally (PF 0.125, n=8)
- What would change the view: a same-day primary-source confirmation (or retraction) of the reported S&P/Nasdaq open print; BTC reclaiming uptrend on the intraday timeframe; the exploit-hack cluster resolving; the first 15-30min of RTH price action confirming or invalidating the XOM/XLE/META pre-open levels

## 7. Candidate Deep Dives

### 1. XOM (stocks, long, pre-gate A / gated to C for market-closed-planning)
- Has price already reacted to the catalyst? Data through 10:27 UTC (pre-open) shows XOM already an RS-leader (20d RS vs SPY +8.65%, vs sector +1.83%) before today's fresh Brent >$100 spike — the catalyst is fresh as of today's session, the RS leadership is not yet a same-day reaction to it.
- Chasing? Not as of pre-open data; needs RTH re-check — energy names can gap hard on oil-shock days.
- Retest/pullback structure? Report shows a defined entry zone 153.98-154.45, invalidation 153.51, TP1/2/3 at 155.85/156.79/158.19 (RR to TP1 = 1.5).
- Overextended? Not flagged pre-open; ATR extension 2.8 noted as a raw-score input, not flagged overextended in the report text.
- Would entry now be late? Only assessable after the open — do not treat the pre-close 153.98-154.45 zone as current without a fresh RTH read.
- Actionable level: RTH confirmation of holding the zone (or a fresh pullback to it) with relative volume expansion.
- Market-mood alignment: strong — long energy into an oil-shock day is the cleanest mood-aligned idea this cycle.
- Long/short/wait: long, but wait for RTH confirmation (not yet actionable pre-open).
- Invalidation: close beyond 153.51 (per report) — recheck against RTH levels once available.
- Chase risk: moderate on a gap day; do not chase if price opens far above the pre-close zone.
- Catalyst confirmation: confirmed and fresh (Brent >$100/bbl today, Iran/Israel escalation) — this is a case where the catalyst arrived after the report was generated, strengthening rather than contradicting the technical read.
- TradingView/manual chart check unavailable — reading only from the report's local OHLCV/ATR/EMA fields.
- Legal/headline check: none found for XOM today.

### 2. XLE (stocks, long, pre-gate A / gated to C for market-closed-planning)
- Same oil-shock catalyst as XOM, sector-wide; 20d RS vs SPY +6.82%, sector status "strong."
- Actionable level: RTH confirmation, same discipline as XOM — do not chase a gap.
- Legal/headline check: none found.
- Catalyst confirmation: confirmed (Brent >$100/bbl).

### 3. META (stocks, short, pre-gate A / gated to C for market-closed-planning)
- Has price already reacted? Pre-open data shows downtrend + RS-leader-to-the-downside; today's news flow (CNBC: "Tesla and Alphabet shares slump as AI spending concerns spook investors") supports continuation of the AI-capex-selloff theme into META, though the cited article names TSLA/GOOGL specifically, not META directly — treat the META linkage as thematic/sector-level, not a confirmed single-name catalyst.
- Chasing? Needs RTH re-check.
- Retest/pullback structure? Not detailed in the packet excerpt read this cycle — use the report's own entry/invalidation levels at RTH confirmation time.
- Actionable level: RTH confirmation of breakdown continuation with volume.
- Market-mood alignment: aligned with risk-off/AI-capex-concern theme.
- Long/short/wait: short, wait for RTH confirmation.
- Chase risk: moderate — semis/mega-cap tech can also snap back sharply on any de-escalation headline.
- Catalyst confirmation: thematic (sector-level AI-capex concern), not a single-name-specific confirmed catalyst — weaker confirmation than XOM/XLE's direct oil-shock link.
- Legal/headline check: none found for META today.

### 4. GOOGL (stocks, avoid/manual-review)
- **LEGAL/HEADLINE RISK — verified**: European Commission fined Google €890M (~$1B) under the Digital Markets Act for self-preferencing in Search/Play, confirmed today (2026-07-23) via CNN, Semafor, and multiple wire outlets (WSB-TV/Action News Jax/Boston 25/WHIO/KIRO7 syndication).
- Stacked with the already-carried-forward post-earnings stale setup (reported earnings 2026-07-22, intraday short setup demoted C for `stale_post_earnings_setup`) and today's AI-capex-selloff reaction (CNBC).
- Per §I: final verdict is **AVOID / MANUAL REVIEW REQUIRED** — never a clean actionable, even though the fundamental thesis (regulatory overhang + earnings-reaction selloff) would otherwise support a short.

### 5. Crypto — WLFI/USDT (long, best-RS scalp/intraday B-tier, already active) and DEXE/USDT (short-watch, unchanged)
- WLFI: top RS leader both scalp (score 100) and intraday, already has an active scalp `triggered` signal (entry 0.060015-0.061181) and an intraday `waiting_for_entry` signal — tracking existing exposure, not a fresh idea. Funding neutral across venues, crowding low — no squeeze warning.
- DEXE: weakest symbol (24h -29.63%, RS vs BTC -28.83-28.89%), negative funding across bybit/mexc (external cross-check also negative), crowding elevated — a failed-bounce short candidate, but no formal level published this cycle; same low-confidence caveat as last review given crypto short-direction PF is 0.125 (n=8) this week.
- Catalyst confirmation: none formal for either — momentum/RS-based, not catalyst-backed.

## 8. Best Candidates Ranked

1. **Long-watch: XOM** — trigger: RTH open/first-30min confirms hold of the 153.98-154.45 zone (or a clean pullback to it) with relative volume expansion; invalidate below 153.51. Catalyst-backed (oil shock) + RS-leader.
2. **Short-watch: META** — trigger: RTH confirmation of breakdown continuation with volume; thematic AI-capex-concern alignment, not single-name-confirmed — treat as watch-only until price confirms.
3. **Catalyst-watch: XLE** — trigger: same RTH discipline as XOM; sector-wide oil-shock beta, RS-leader pre-catalyst.
4. **Avoid: GOOGL** — verified fresh EU antitrust fine + stale post-earnings setup — manual review required, never actionable this window.
5. **Crypto long-watch (secondary): WLFI/USDT** — already active (scalp triggered, intraday waiting_for_entry) — track existing exposure per the report's own entry/invalidation, not a fresh idea.
6. **Crypto short-watch (secondary, low-confidence): DEXE/USDT** — failed-bounce/breakdown continuation with volume; crypto short-direction PF is weak this week (0.125, n=8) — demand unusually strong confirmation.

## 9. Avoid / No Trade

This is a decision-window call only — scanning, data collection, tracking, and the scheduler continue unchanged.

- **GOOGL** — verified fresh EU $1B/€890M DMA antitrust fine (today) stacked on a stale post-earnings setup — manual review required.
- **UNH** — open federal DOJ investigation (Medicare billing/civil fraud), re-verified no update in 48h — avoid new exposure regardless of technical score.
- **ETH, ARB** (and ADA, BNB per the still-open Wanchain flag) — active cross-chain bridge-exploit cluster (Verus-Ethereum second exploit $7.54M, AFX Trade $24.15M) still in today's top catalysts.
- **LMT and any name reporting earnings today** — do not chase into the print.
- **Crypto scalp mode generally** — PF 0.67 this week; treat any scalp idea with extra scrutiny.
- **Crypto short direction generally** — PF 0.125, n=8 this week; any new short needs materially better confirmation than a long for the same risk.
- **Chasing the reported gap-down open itself** — until RTH price action confirms the pre-market/open read, do not treat the -1.1%/-1.8% print as a tradeable level on its own.

## 10. Main Risks

- **Gap risk at the open:** reported S&P -1.1% / Nasdaq -1.8% open on Iran/Israel escalation + Brent >$100/bbl — elevated whipsaw risk in the first 15-30min of RTH; do not treat pre-open technical levels as live without confirmation.
- **Geopolitical tail risk:** ongoing (week 7+) US/Israel-Iran conflict, oil supply-shock dynamics (Strait of Hormuz exposure per external sources) — broad risk-off overlay for both crypto and stocks.
- **Regime divergence (carried forward):** intraday/scalp reads range/mixed while the swing report (10.3h stale) still reads bullish/risk-on — do not use the swing regime label as current.
- **Exploit-hack cluster (carried forward):** ETH/ARB/ADA/BNB bridge-exploit risk unresolved.
- **Legal/headline risk:** GOOGL (new, verified today), UNH (unchanged), LLY (GLP-1 lawsuit, carried forward).
- **Catalyst layer degraded:** 80.4% of catalyst events unmapped — same resolver defect as prior cycles (TODO-1).
- **Data staleness:** stocks swing/invest ~21 days stale (TODO-2); stocks intraday report itself is pre-open (10:27 UTC) — the actual RTH reaction has not yet been captured in a fresh report as of this review.
- **Unverified same-day print:** the specific -1.1%/-1.8% open numbers came from internal Telegram feeds only; WebSearch could not retrieve a same-day (Jul 23) primary-source article confirming the exact print (search-index lag) — directionally consistent with the confirmed multi-week pattern, but treat the precise numbers as single-source until the 18:30 US-open-reaction review can cross-check against a fresh stocks report.

## 11. Action Plan — Next 4 Hours

- Watch XOM/XLE for RTH confirmation of the pre-close long zones; treat as actionable only after the first 15-30min of price action confirms.
- Watch META for RTH confirmation of breakdown continuation before treating as actionable; this is thematic, not single-name-catalyst-confirmed, so demand cleaner technical confirmation than usual.
- Do not touch GOOGL under any framing this window — manual review required regardless of price action.
- Keep ETH/ARB/ADA/BNB on the avoid list through the open unless the exploit cluster news resolves.
- Track existing WLFI exposure (scalp triggered, intraday waiting) per its own entry/invalidation; do not add fresh crypto entries into the gap-risk backdrop without a clean confirmation stack.
- Monitor whether BTC reclaims uptrend and whether the swing/intraday regime divergence resolves.
- Feed the 18:30 US-open-reaction review with a same-day check on the S&P/Nasdaq actual open print (cross-check against a fresh stocks report once generated).
- No changes to scoring, thresholds, or scanning — system continues running as-is.

## 12. Final Verdict per Mode

- **Scalp:** No new A/B. Losing mode this week (PF 0.67) — extra scrutiny on any future scalp idea, especially into a gap-risk day.
- **Intraday:** No new A/B this cycle; book carries WLFI/BANK/OPN/TLM/ONDO/ZAMA/ADA/VIRTUAL/ALLO/KITE/PENGU/PUMP/KAITO watchlist-only for new entries.
- **Swing:** Best-performing mode this week (PF 3.00) but the report is ~10.3h old and reads a regime (bullish/risk-on) that diverges from the fresher intraday/scalp read (range/mixed) — treat open positions (RE, EPIC, BANK, ERA) as tracking-only; do not originate new swing ideas off this read without a same-day refresh.
- **Stocks intraday:** Pre-open data shows the strongest catalyst-aligned setups are XOM/XLE (long, oil shock) and META (short, AI-capex theme); GOOGL is avoid/manual-review despite an aligned short thesis. All require RTH confirmation before being actionable — none are live yet as of this review.
- **Stocks swing/invest:** Data ~21 days stale — do not use for any current decision (TODO-2, unchanged).

## 13. Sources

- Internal: `data/catalysts/2026-07-23/catalyst_cycle_13-02.md` (GOOGL EU fine catalyst, GS/CLARITY Act, INTC earnings, exploit-hack cluster)
- Internal: `data/reports/scalp/2026-07-23_12-48_scalp_report.md`, `data/reports/intraday/2026-07-23_12-54_intraday_report.md`, `data/reports/swing/2026-07-23_03-05_swing_report.md`, `data/reports/stocks/intraday/2026-07-23_10-27_stocks_intraday_report.md`
- Internal: `news_items` direct SQL — last-3h feed scan (ECB Lagarde speech, t.me/BWEtradfi S&P/Nasdaq open print, t.me/ClashReport Brent $100 + Netanyahu statement); UNH/DOJ re-check (no fresh news in 48h, confirms unchanged)
- Internal: CLI `active-signals`, `signal-stats`, `detect_untracked_legacy_alerts` (2026-07-23 16:2x-16:3x runs)
- [EU slaps Google with record $1 billion antitrust fine — Semafor](https://www.semafor.com/article/07/23/2026/eu-slaps-google-with-record-1-billion-antitrust-fine) (2026-07-23)
- [Europe fines Google $1 billion for 'harming' rivals — CNN Business](https://edition.cnn.com/2026/07/23/business/europe-fines-google-1-billion-intl) (2026-07-23)
- [S&P 500 and Nasdaq open lower as Iran tensions jolt sentiment, chip stocks slide — Investing.com/Reuters](https://www.investing.com/news/stock-market-news/sp-500-and-nasdaq-open-lower-as-iran-tensions-jolt-sentiment-chip-stocks-slide-4788785) (2026-07-13, used for pattern/context only — not same-day)
- [U.S. stocks sink as war against Iran intensifies, Brent settles above $100/bbl — Seeking Alpha](https://seekingalpha.com/news/4563766-sp500-nasdaq-composite-dow-jones-stock-news) (date per search index, used for pattern/context)
- [Stock Market Today (July 20, 2026): Iran worries derail Nasdaq, S&P 500 — TheStreet](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-july-20-2026) (2026-07-20, context)
- Source unavailable: same-day (2026-07-23) primary-source article confirming the exact S&P -1.1%/Nasdaq -1.8% open print — internal Telegram feed only (t.me/BWEtradfi), external search index had not yet indexed same-day coverage at review time.

## 14. Fix Requests / TODO

### TODO-1: Catalyst symbol resolver missing tickers spelled out literally in the headline (recurring — 3rd consecutive cycle with evidence)
- **issue:** Funding-rate-adjustment and new-listing notices continue landing with a null symbol despite the ticker being present verbatim in the title.
- **evidence:** `data/catalysts/2026-07-23/catalyst_events.jsonl` — 2,010/2,500 (80.4%) unmapped this cycle (was 79.1% at 11:39 EEST, 78.0% at 04:48 EEST — same pattern, essentially flat, unresolved across three cycles today).
- **suggested manual fix:** Extend the symbol resolver's regex/lookup to catch `#Trading_Updates` / `#New_Listings`-style Binance/MEXC announcement formats where the ticker appears as a single concatenated token (e.g. `RIFUSDT`) rather than the usual `RIF/USDT` form.
- **priority:** high
- **first observed:** 2026-07-23 04:48 EEST; confirmed recurring at 11:39 and again at 16:20 EEST (same specific tickers, unresolved across all three cycles today).

### TODO-2: Stocks swing/invest reports ~21+ days stale (unchanged)
- **issue:** `data/reports/stocks/swing/` and `data/reports/stocks/invest/` have no report newer than 2026-07-02.
- **evidence:** latest files still `2026-07-02_13-0x`.
- **suggested manual fix:** investigate why the stocks swing/invest report generator stopped running or is failing silently; check scheduler config for these two report types.
- **priority:** high
- **first observed:** carried forward from 2026-07-23 04:48 EEST review; unchanged this cycle.

### TODO-7: Same-day market-open print not independently verifiable via external search at review time
- **issue:** This review relied on a single internal Telegram source (t.me/BWEtradfi) for the exact S&P -1.1%/Nasdaq -1.8% open print; WebSearch could not retrieve same-day (2026-07-23) primary-source confirmation, only pattern-consistent context from prior dates this month. Not a bug — a structural limitation (search-index lag on very fresh market-open news) — but worth noting for the 18:30 US-open-reaction review to explicitly cross-check against a freshly-generated stocks report once available.
- **evidence:** WebSearch queries this run returned July 8/9/13/19/20/21/22 coverage of the same Iran/Israel/oil theme, but nothing dated July 23 for the specific open print.
- **suggested manual fix:** none required — flagging for the next slot's awareness only.
- **priority:** low
- **first observed:** 2026-07-23 16:20 EEST (this run).

_Carried-forward TODO-3, TODO-4, TODO-5, TODO-6 from the 11:39 EEST review remain open and unchanged (regime-divergence display question, past-expiry-signal display question, `no_gate_context` stocks-intraday loss bucket, `telegram-test` underscore parse_mode bug) — not re-detailed here to avoid duplication; see `OPUS_ENRICHED_REVIEW_AUTO_2026-07-23_1139.md` §14 for full text._
