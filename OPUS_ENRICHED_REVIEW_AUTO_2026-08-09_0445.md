# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:45 EEST

## 1. Executive Summary

- **Slot: crypto overnight / Asia review (04:30 EEST).** Advisory only — no auto-trade, no code/scoring changes made.
- Crypto book: 50 active B-tier signals, **100% long, 0 A-tier, effectively 0 shorts** (system-wide direction=short sample is n=1 all-time). No fresh catalyst backs any of today's top movers (TST, BICO, ACE, DODO) — pure momentum continuation in a desk-labelled "bullish trend (risk-on)" regime.
- Macro overlay is a **genuine, still-live** risk-off headwind: Strait of Hormuz remains effectively closed to shipping (day ~160, independently verified via web search), not a stale recycled headline. Desk macro risk score eased from ~96-97/100 (23:15 review) to ~74-90/100 this cycle but stays elevated.
- **It is Sunday — weekend regime.** Internal stats show weekend signals underperform non-weekend by a wide margin (PF 1.31 vs 2.39, winrate 17% vs stronger on weekdays) — this is a real routing input, not just caution talk.
- Best long: **DODO/USDT** (both intraday and swing legs now triggered + tp1_hit — the swing leg filled since the 23:15 review). Best catalyst-backed: **XLM/ONDO** (rwa_narrative, Circle/USDC-on-Stellar growth, primary-ish source). Best short-watch: none open; nearest candidates are **KAITO/USDT** or **EPIC/USDT** on a confirmed breakdown retest.
- Recurring integrity issue confirmed again this cycle: **HEI/USDT, ZBT/USDT, SKYAI/USDT are simultaneously tagged `bias short` in the money-flow "weakest symbols" list while carrying open LONG B-tier signals** — same contradiction flagged in the last several reviews (TODO already escalated to HIGH per prior session memory; still unresolved).
- Stocks: markets closed (Sunday) — all stocks context is planning/watchlist only; existing stocks paper positions are stale (some open since mid-July, unresolved for 3+ weeks — see §14 TODO).

## 2. Data Used

- Reports: scalp (2026-08-08 23:25 EEST, gen), intraday (2026-08-08 23:34 EEST), swing (2026-08-08 21:06 EEST). Stocks intraday (2026-08-07 20:57, stale — weekend), stocks swing/invest (2026-07-02, stale/deprecated per prior audit).
- `active-signals --asset-class crypto` (50 rows, all B-tier/long), `active-signals --asset-class stocks` (30 rows, mostly weeks-old unresolved).
- `signal-stats --asset-class crypto` and `--asset-class stocks`.
- `detect_untracked_legacy_alerts --since 2026-08-09` → none found.
- `catalyst-scan` run fresh this cycle (today's folder was missing) → 500 events, 3 baskets.
- `news_items` spot-checks for DODO/ACE/TST/BICO/HYPE/ONDO/XLM/TUT/HEI/ZBT/SKYAI (24h window).
- Latest scheduler cycle summary (`cycle_02_02-16_summary.md`) for lifecycle counts and pipeline health.
- 2 WebSearch queries (BTC/ETH price action, Strait of Hormuz status) + 2 WebFetch (one blocked 451, one succeeded) to verify the macro overlay is live, not stale.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-08_2315.md`.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime 2026-08-09 03:12 EEST — **fresh** (~1.5h old at review time). Not deferred.
- Latest cycle (`cycle_02_02-16_summary.md`) completed 2026-08-09 03:12 EEST.
- Paper Monitor Status (from that cycle): **Open actionable: 36, Waiting for entry: 4, Entered unresolved: 0, Review/Shadow: 28, No-entry/stale/moved-away: 82, Closed today: 158W/16L/31flat, Needs review: 3.**
- Two pipeline steps **FAILED on timeout (300s)** this cycle: `paper structural TP refresh` and `refresh obsidian dashboard` — see §14 TODO.
- Crypto reports fresh (<3.5h at review time). Stocks intraday report is from Friday 2026-08-07 (weekend gap, expected — market closed). Stocks swing/invest are stale (>1 month, deprecated per prior audit — not treated as live).
- Catalyst folder for today was **missing** and was regenerated this run (§A.4 allowed action): 500 events, 3 baskets.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-08-09 04:45 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "catalyst_missing", "derivatives_sparse"],
      "data_missing": ["stocks_swing_fresh_data", "stocks_invest_fresh_data"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 03:12 EEST", "catalyst folder regenerated this run", "2 pipeline steps timed out (TP refresh, obsidian dashboard)"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["risk_off", "longs_preferred", "chop"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/ETH uptrend, breadth 71-83% above EMA20/50 per reports", "desk macro risk-off score 74-90/100", "Strait of Hormuz independently verified still closed (day ~160)", "weekend underperformance in signal-stats"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 181/500 = 36.2% mapped, 63.8% unmapped (>50% threshold)", "3 baskets: rwa_narrative, perps_dex_narrative, momentum_breakout", "no fresh 24h news_items for DODO/ACE/TST/BICO/TUT/HEI/ZBT/SKYAI"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.4,
      "reason_codes": ["oi_supports", "data_unavailable"],
      "data_missing": ["OI 24h for most mexc-fallback symbols shows n/a"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BLUAI elevated long crowding flagged in report", "TST/BICO/PUMP show OI-down + price-up = short covering, weaker continuation per scalp report derivatives section"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["entry_fresh", "overextended", "chase_risk"],
      "data_missing": ["TradingView / manual chart check unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": ["TUT/USDT +168-177% 24h flagged symbols_overextended in momentum_breakout basket, playbook avoid_chase", "TST/BICO/ACE all no-catalyst momentum with known playbook failure mode (WR23%/PF0.70/-3R for no-catalyst intraday in chop)"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Open actionable 36, Waiting for entry 4, Entered unresolved 0, Review/Shadow 28, No-entry/stale/moved-away 82, Needs review 3 (latest cycle paper monitor status)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["headline_risk", "manual_review", "correlation_cluster"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC exploit_hack risk flags active (Coldcard hack, BTCPay vuln) — block_requires_operator_review already set in production risk warnings", "HEI/ZBT/SKYAI bias-tag contradiction persists (open longs tagged bias=short) — prior-session TODO escalated HIGH, still open", "book is 100% long, 0 shorts — correlation/concentration risk if regime flips"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto B-tier overall PF 1.997 reliable (n=204)", "swing PF 4.55 strong (n=74)", "intraday PF 1.40 modest (n=84)", "scalp PF 0.167 negative, avgR -0.076 (n=46) — known low-confidence data-collection-only mode", "stocks intraday PF 0.167, C-tier winrate 1% — confirms C-tier never-actionable stance"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "DODO/USDT", "trigger": "already open — manage intraday leg toward TP2 0.02255/TP3 0.02388, swing leg toward TP2 0.02326/TP3 0.02481; no new entry needed, thesis confirmed since swing leg filled+tp1 since last review" },
    "best_short_candidate":    { "symbol": "KAITO/USDT", "trigger": "none open — needs confirmed 1h close below prior swing low + volume expansion on the breakdown before any short is actionable; currently bias-short-tagged with no signal generated" },
    "best_catalyst_candidate": { "symbol": "XLM/USDT", "trigger": "rwa_narrative basket, Circle/USDC-on-Stellar 35% mcap growth (single_source, <6h) — needs a scored B/A signal to appear before actionable; currently basket-level only" },
    "avoid_candidate":         { "symbol": "TUT/USDT", "reason": "flagged symbols_overextended in momentum_breakout basket (playbook avoid_chase), +168-177% 24h with no catalyst — chase risk, do not add" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.75 | scheduler_fresh, catalyst_missing, derivatives_sparse | advisory_only |
| market_regime | caution | 0.65 | risk_off, longs_preferred, chop | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | ok | 0.40 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | entry_fresh, overextended, chase_risk | advisory_only |
| execution_lifecycle | ok | 0.80 | open_actionable, waiting_for_entry, review_shadow | advisory_only |
| risk_manager | caution | 0.65 | headline_risk, manual_review, correlation_cluster | advisory_only |
| playbook_performance | caution | 0.75 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader (synthesis) | caution | 0.60 | preferred_side=longs, operator_action=watch | advisory_only |

## 4. What Changed vs Previous Review (2026-08-08 23:15 EEST)

- **DODO/USDT swing leg confirmed**: was `waiting_for_entry` at 0.02073-0.02148 (unfilled since 16:02:59 UTC) → now `triggered` + `tp1_hit` at entry 0.021613-0.022255. Thesis playing out as expected.
- **Macro risk-off score eased** from 96.6-96.7/100 (23:15, "active, escalating" per independent ADNOC-tanker-strike confirmation) to 74.3-89.8/100 this cycle, but the underlying Strait of Hormuz situation is confirmed still live via web search (day ~160, effectively closed) — not resolved, just less acute in the headline mix this cycle.
- **TST/USDT emerged as the new top mover** (score 91.6-99.6, +23-25% 24h) — not called out as a top candidate in the 23:15 review.
- **TUT/USDT more extended** — was already flagged avoid in the previous review at a lower % move; now +168-177% 24h and explicitly tagged `symbols_overextended` in the fresh momentum_breakout basket. Same avoid stance carries forward, reinforced.
- **Catalyst-backed candidate unchanged**: ONDO/XLM (rwa_narrative) still basket-level only, no live scored signal — same as 23:15.
- **New this run**: catalyst folder for today (2026-08-09) had not been generated yet at review time; regenerated per the allowed CLI action. Mapping came back weak (63.8% unmapped) — flagged in §5.
- **Bias-tag contradiction (HEI/ZBT/SKYAI) persists unchanged** across both this and the prior review — still an open TODO, not resolved.

## 5. Catalyst Coverage

- Total catalyst_events today (2026-08-09, freshly generated): **500**. Mapped (non-null symbol): **181 (36.2%)**. Unmapped: **319 (63.8%)**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (unmapped > 50%)
- Top 3 unmapped headlines:
  1. "The 16th Worldwide Chinese Life Insurance Congress & 2026 International Dragon Award (IDA) Annual Conference Grandly Held" (PR Newswire, Stocks)
  2. "China July consumer prices fall 0.1% m/m; producer prices..." (t.me/BWEtradfi)
  3. "Former SK Hynix employee jailed for leaking information to a Chinese firm" (t.me/BWEtradfi)
- Narrative baskets (3): `rwa_narrative` (ONDO/XLM, playbook `related_beta_rotation`, single_source, <6h), `perps_dex_narrative` (HYPE, playbook `wait_pullback`, single_source, <6h), `momentum_breakout` (TUT, playbook `avoid_chase`, single_source, <1h, flagged `symbols_overextended`).

## 6. Market Landscape

BTC and ETH both in short-term uptrend per desk technicals (altcoin breadth 72-83% above EMA20/50 across scalp/intraday/swing reports), and the desk classifies the regime as "bullish trend (risk-on)." However, this needs context: broader web-verified macro backdrop shows BTC still ~28% below its 52-week high and total crypto market cap ~46% below the October 2025 peak — the current move reads as a **bounce inside a longer bear/consolidation phase**, not a fresh bull leg. The desk's short-horizon regime call and the medium-term macro backdrop are not contradictory, but the gap matters for sizing/confidence on breakout longs.

The Strait of Hormuz shipping crisis is confirmed independently (via web search) to still be live and largely unresolved (day ~160 of closure per third-party tracker; Iran-Oman framework talks ongoing but Iran's Revolutionary Guard still restricting transit) — this is a real, current risk-off macro input, not a stale recycled headline as it might first appear from repeated mentions across recent cycles.

Crypto derivatives read is unremarkable — no extreme funding, only BLUAI shows "elevated long crowding." Momentum leadership (TST, BICO, ACE, BLUAI, TUT, CASHCAT, DODO) is broad but **entirely uncatalyzed** — none of these symbols have a verified news hit in the last 24h; they are pure price/RS movers. TUT is the most extended (+168-177% 24h) and explicitly flagged as chase risk.

### Market Mood / Risk Routing

- Crypto mood: **risk-on (short-term technical), with a live risk-off macro overlay (Hormuz) and a weekend-underperformance headwind** — net: mixed/cautious.
- Stocks mood: **closed** (Sunday) — planning/watchlist only.
- Dominant narrative: rwa_narrative (ONDO/XLM, Circle/USDC-on-Stellar growth) and perps_dex_narrative (HYPE, but catalyst is a negative token-unlock risk, not a tailwind).
- Preferred side now: **longs, selective, manage existing — no fresh weekend chases.**
- Best long candidate: **DODO/USDT** — already open on both intraday and swing, both confirmed and progressing (tp1_hit on each), no catalyst but consistent RS/trend continuation.
- Best short candidate: **none open** — nearest: KAITO/USDT or EPIC/USDT on a confirmed breakdown retest-fail (currently only bias-tagged, no signal).
- Best catalyst-backed candidate: **XLM/USDT** (rwa_narrative, Circle/USDC-on-Stellar 35% mcap growth in 30 days, single_source <6h) — basket-level only, not yet a scored signal.
- What to avoid: **TUT/USDT** (chase risk, overextended, avoid_chase playbook), and **new no-catalyst intraday longs generally this weekend** (14d no-catalyst cut for this playbook is WR 23%/PF 0.70/-3R, and today's weekend-mode stats show winrate ~17%, PF 1.31 vs 2.39 on weekdays).
- What would change the view: a confirmed Strait of Hormuz reopening (de-escalation) would remove the macro headwind; a scored signal appearing on ONDO/XLM would upgrade the catalyst-backed idea from watch to actionable; Monday's session-open would remove the weekend-underperformance drag.

## 7. Candidate Deep Dives

### 1. DODO/USDT — LONG, already open (best long candidate)
- Two live legs: intraday (`sig_daaddc397aaac7b8`, entry 0.021654-0.022281, tp1_hit, expires 2026-08-09T12:01) and swing (`sig_c0c357f59df5e5b6`, entry 0.021613-0.022255, tp1_hit, expires 2026-08-15T21:06).
- Has price already reacted to a catalyst? No catalyst — pure momentum/RS continuation (11-16% 24h across reports, RS vs BTC +11 to +16%).
- Chasing? No — both legs are already filled and running; this is management, not a new entry.
- Retest/pullback structure? Yes, entries were pullback-style per playbook `crypto_intraday_catalyst_or_momentum`.
- Overextended (>2 ATR from EMA20)? No — current price ~0.0217 sits between support 0.0189 and resistance 0.0260, not stretched.
- Would entry now be late? N/A — already entered.
- Aligned with market mood? Yes — RS-leader long in a risk-on-tagged regime, no chase.
- Actionable now or after confirmation? Already actionable/open; manage toward TP2/TP3.
- Invalidation: intraday 1h close below 0.020887; swing 1h close below 0.020828.
- Catalyst confirmation or contradiction? None either way — pure technical/momentum thesis, known playbook caveat (no-catalyst intraday in chop is net-negative) applies structurally but this leg has already cleared TP1 on both timeframes.
- Chase risk? No.

### 2. TST/USDT — LONG, B-tier actionable (top fresh mover)
- Score 67.5 (intraday), 99.6 momentum score in scalp report; 24h +23-25%, RS vs BTC +23-25%, volume 0.42-0.55x (below average).
- Has price already reacted? Yes, the move (+23%) has already happened; entry plan is a pullback into 0.0160-0.0164 vs current 0.0167 — close to the zone, not yet filled.
- Chasing? Borderline — price is only marginally above the pullback zone, but volume is sub-1x, so breakout confirmation is weak per the report's own counter-thesis.
- Retest structure? Yes, pullback design.
- Overextended? No (ATR 0.0010, current 0.0167 vs entry zone 0.0160-0.0164 — under 1 ATR away).
- Actionable now or wait? Per playbook: needs RS-leader or breakout confirmation since there's no catalyst; low-volume pullback fill would be the trigger.
- Catalyst confirmation? None found in news_items 24h scan — pure momentum, known playbook failure mode (WR 23%/PF 0.70 for no-catalyst intraday in chop) applies directly. Treat as watch-until-fill, not a chase.
- Chase risk? Moderate if bought above the stated zone.

### 3. HEI/USDT & ZBT/USDT & SKYAI/USDT — bias-tag contradiction (needs review)
- All three carry **open LONG B-tier signals** (HEI: swing triggered + scalp tp1_hit; ZBT: 3x swing triggered + scalp tp1_hit; SKYAI: swing triggered + intraday tp1_hit) while simultaneously appearing in the **"Weakest Symbols" / bias=short** list in scalp, intraday, and swing reports this same cycle (HEI -10.8% to -15.0% 24h, ZBT -8.2% to -12.7% 24h, SKYAI -5.8% 24h in swing report specifically).
- This is the same contradiction flagged across multiple prior review cycles (see prior-session TODO, escalated HIGH). It persists unresolved this cycle too — not a new finding, but confirmed still-open.
- Is this actionable? No — this is a data-integrity flag, not a trade idea. Existing open longs on these symbols should get extra scrutiny/manual review given the desk's own weakness tagging contradicts the live position direction.

### 4. HYPE/USDT — catalyst-backed but negative catalyst (watch, not long)
- perps_dex_narrative basket, primary symbol. Catalyst: HyperLabs $23M token unlock (risk_warning, per §5c production risk warnings) — this is a headwind catalyst, not a tailwind.
- Has price reacted? News from 2026-08-08 22:00 UTC notes "Hyperliquid ETFs Turn Green After Bleeding $30M in Three Weeks" — mixed signal (recovering flows, but unlock risk ahead).
- Suggested playbook: `wait_pullback` — not a chase, not a fresh long until the unlock is digested.
- Actionable now? No — no scored signal exists yet; this is basket/watch-level only.
- What would invalidate/activate: a clean pullback with unlock absorbed and no renewed net outflows.

### 5. TUT/USDT — avoid / chase risk
- Momentum_breakout basket, flagged `symbols_overextended`, playbook `avoid_chase`. +168% to +177% 24h across scalp/intraday reports, no catalyst.
- Has price already reacted? Yes, massively — this move is done, not starting.
- Retest structure? None offered; pure vertical extension.
- Would entry now be late? Extremely late — this is the textbook chase-risk case.
- Prior review already flagged this same symbol as "do not add exposure to TUT even after its small pullback" — guidance reinforced, now even more extended.
- Actionable? No — avoid new entries; if a scored signal appears here it should be treated with elevated skepticism given the explicit basket flag.

## 8. Best Candidates Ranked

1. **DODO/USDT (long, already open)** — thesis confirmed since last review, manage toward TP2/TP3 on both legs. No new entry required.
2. **TST/USDT (long-watch)** — trigger: clean fill of pullback zone 0.0160-0.0164 on rising volume (currently sub-1x); avoid if bought above zone without volume confirmation.
3. **XLM/USDT (catalyst-watch)** — trigger: a scored B/A signal appearing on the rwa_narrative basket backed by continued Circle/USDC-on-Stellar flow data; currently context-only.
4. **KAITO/USDT (short-watch)** — trigger: confirmed 1h close below prior swing low with volume expansion; no signal currently exists, this is a pure watch level.
5. **TUT/USDT (avoid)** — no trigger makes this actionable at current extension; would need a multi-day base/retest before reconsideration.

## 9. Avoid / No Trade

- **New no-catalyst intraday longs this weekend window specifically** — playbook's own 14d no-catalyst cut is WR 23%/PF 0.70/-3R, and today's weekend-mode signal-stats confirm underperformance (PF 1.31 vs 2.39 weekday). This is a routing caution for *this decision window*, not a system-wide stop — scanning, tracking, and candidate generation continue as normal.
- **TUT/USDT** — chase risk, explicitly flagged overextended.
- **New shorts** — direction=short sample is effectively zero (n=1 all-time in crypto B-tier stats); no clean short setup currently exists. This does not mean "never short," it means none is confirmed right now.
- **HEI/USDT, ZBT/USDT, SKYAI/USDT longs** — not a stop-loss recommendation, but flagged for manual review given the bias-tag contradiction described in §7.

## 10. Main Risks

- Macro: Strait of Hormuz closure remains live and unresolved — a renewed escalation headline could hit risk sentiment quickly; a resolution headline could remove the current risk-off drag.
- Concentration: 100% of the active crypto book is long (0 shorts), all B-tier, no A-tier — regime-flip risk is unhedged.
- Weekend-mode underperformance is a real, data-backed drag on any new entries taken today.
- BTC exploit_hack headline cluster (Coldcard hack, BTCPay vulnerability) is an ongoing sector-wide security overhang, already correctly gated as `block_requires_operator_review` in production risk warnings — no action needed here beyond awareness.
- Data integrity: the HEI/ZBT/SKYAI bias-tag contradiction, if it reflects a real scoring/tagging bug rather than a display quirk, could mean other open longs are similarly mistagged — worth a human audit (see §14).

## 11. Action Plan — Next 4 Hours

- Manage DODO/USDT legs toward TP2/TP3 on both timeframes; no new action needed unless invalidation levels are hit (intraday <0.020887, swing <0.020828).
- Watch TST/USDT for a volume-confirmed fill of its 0.0160-0.0164 pullback zone before treating as actionable.
- Continue monitoring XLM/ONDO (rwa_narrative) for a scored signal to emerge from the basket.
- No new weekend chases on no-catalyst momentum names; let the scanner keep collecting data as usual.
- Re-check macro/Hormuz headlines at the next slot (11:30 EEST, Europe/pre-US context) for any material change.

## 12. Final Verdict per Mode

- **Scalp**: caution / data-collection-only, consistent with the report's own low-confidence banner (PF 0.167 this cycle, 1W/4L). No new scalp entries recommended beyond what the scanner already generates.
- **Intraday**: caution / selective — manage DODO, watch TST/BICO/ACE for confirmed fills only; no-catalyst chase names avoided.
- **Swing**: watch/manage — DODO swing leg progressing well (PF 4.55 for the mode overall); no new swing adds flagged as high-conviction this cycle.
- **Stocks (all modes)**: closed (Sunday) — planning/watchlist only, no live verdict until Monday's pre-US-open slot.

## 13. Sources

- [Bitcoin and ethereum prices today, Friday, August 7, 2026](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-august-7-2026-crypto-prices-moving-higher-following-july-jobs-report-131451960.html) — verified via WebFetch, price/sentiment confirmed, no Hormuz mention in this specific article.
- [2026 Strait of Hormuz crisis — Wikipedia](https://en.wikipedia.org/wiki/2026_Strait_of_Hormuz_crisis) — background reference (not fetched, title/snippet only).
- [Strait of Hormuz Closed, Day 160 — Live Tracker](https://straits.live/) — third-party day-count tracker cited in search snippet (not fetched directly).
- [CNN Iran-Trump live coverage, Aug 5 2026](https://www.cnn.com/2026/08/05/world/live-news/iran-war-trump) — WebFetch returned HTTP 451 (geo-blocked), used only as a search-snippet source, not independently verified by fetch.
- [Crypto market recap — investingnews.com](https://investingnews.com/cryptocurrency-market-recap/) — macro backdrop (46% below Oct 2025 peak), snippet only, not fetched.
- Internal: `data/reports/scalp/2026-08-08_23-25_scalp_report.md`, `data/reports/intraday/2026-08-08_23-34_intraday_report.md`, `data/reports/swing/2026-08-08_21-06_swing_report.md`, `data/catalysts/2026-08-09/catalyst_events.jsonl` (freshly generated), `news_items` table (SQLite queries), `data/scheduled_runs/2026-08-08_default_schedule/cycle_02_02-16_summary.md`.

## 14. Fix Requests / TODO

### TODO-bias-tag-contradiction-recurrence
- **issue:** HEI/USDT, ZBT/USDT, SKYAI/USDT continue to carry open LONG B-tier signals while the same-cycle "weakest symbols" list tags them `bias short` with negative 24h returns. This is the same pattern previously escalated to HIGH priority and remains unresolved across at least this and the prior review cycle.
- **evidence:** `data/reports/swing/2026-08-08_21-06_swing_report.md` weakest symbols section (ZBT -12.69%, HEI -10.79%, SKYAI -5.83%, all `bias short`) vs `active-signals --asset-class crypto` showing open long signals for all three (e.g. `sig_a4e763ceaf1df917` HEI swing long triggered, `sig_0be20040e229aec5` ZBT swing long triggered, `sig_806d7d2a8890269d` SKYAI swing long triggered).
- **suggested manual fix:** Human audit of whether "bias" in the money-flow weakest-symbols computation and the signal-generation direction logic are reading from different/stale data sources, or whether this is intentional (bias=short is a momentum-only label, unrelated to the signal's actual trade direction) and just confusingly named.
- **priority:** high (carried forward, not new).
- **first observed (this lineage):** 2026-08-08 (per prior-session memory); reconfirmed 2026-08-09 04:45 EEST.

### TODO-pipeline-timeouts-latest-cycle
- **issue:** Two scheduler pipeline steps failed on a 300s timeout in the latest cycle: `paper structural TP refresh` and `refresh obsidian dashboard`.
- **evidence:** `data/scheduled_runs/2026-08-08_default_schedule/cycle_02_02-16_summary.md` lines ~309 (`### 25. [FAIL] paper structural TP refresh (exit=-1, 300.1s, attempts=1)`) and ~1067 (`### 57. [FAIL] refresh obsidian dashboard (exit=-1, 300.0s, attempts=1)`).
- **suggested manual fix:** Investigate whether these are DB lock contention (SQLite WAL) from concurrent scheduler steps, or a genuine dataset-growth performance regression; consider raising the timeout or profiling the query/script.
- **priority:** medium.
- **first observed:** 2026-08-09 03:12 EEST (this cycle).

### TODO-stale-unresolved-stocks-signals
- **issue:** Several stocks signals in `active-signals --asset-class stocks` show status `triggered`/`tp1_hit`/`tp2_hit` with `expires_at` dates 3+ weeks in the past (e.g. entries from 2026-07-09 through 2026-07-21) that are still appearing as non-terminal/open rather than being resolved/closed out.
- **evidence:** `active-signals --asset-class stocks` output — e.g. `sig_e0b02f34d99d8f0f` XLK expires_at 2026-07-16T19:31:01 still status `tp2_hit` (non-terminal display) as of 2026-08-09.
- **suggested manual fix:** Human check of the stocks paper-lifecycle monitor to confirm whether expired-but-unresolved stocks positions are being finalized/closed on schedule, or whether there's a gap in the expiry-closure logic specific to stocks (crypto book shows `Entered unresolved: 0` in the same cycle, so this looks stocks-specific).
- **priority:** medium.
- **first observed:** 2026-08-09 04:45 EEST.

### TODO-catalyst-mapping-weak-recurrence
- **issue:** Catalyst symbol mapping came back at 36.2% mapped / 63.8% unmapped this run, above the 50% weak-mapping threshold. Top unmapped items are mostly non-crypto macro/PR-newswire noise (China CPI, insurance conference, SK Hynix leak case) rather than crypto-specific catalysts that should have mapped.
- **evidence:** `data/catalysts/2026-08-09/catalyst_events.jsonl` — 500 total events, 181 with non-null `symbol`.
- **suggested manual fix:** Consistent with prior "improve symbol resolver in catalyst layer" guidance already on file — this run reconfirms the issue is still present.
- **priority:** low (recurring, already known, use catalyst layer as context only per standing guidance).
- **first observed (this lineage):** prior sessions; reconfirmed 2026-08-09 04:45 EEST.
