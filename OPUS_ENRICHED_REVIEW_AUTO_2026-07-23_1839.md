# Opus Enriched Review — US open reaction review — Auto Cycle 18:39 EEST

## 1. Executive Summary

Slot: **US open reaction review** (18:39 EEST, 2026-07-23, ~2h09m into the RTH session that opened 16:30 EEST). **Advisory only — no auto-trade, no scoring/strategy changes.** The RTH open has now confirmed the gap-risk thesis flagged in the 16:20 pre-open review: the fresh stocks-intraday report (15:30 UTC / 18:30 EEST, ~9min old) shows VIX rising from 17.70 pre-open to **19.94**, breadth above EMA20 at **0.0%**, SPY/QQQ both in confirmed downtrend (SPY 5d −1.98%, QQQ 5d −2.51%), and stocks regime label flipping to explicit **risk_off / bias=short**. This resolves last cycle's TODO-7 (same-day open print unverifiable via external search) — the internal RTH data now independently confirms the risk-off direction without needing fresh WebSearch. **META** remains the cleanest short-aligned name (still A-raw score 94.5, thematically tied to today's "AI-spending-concerns" selloff) but is gate-demoted to C on liquidity/sector-confirmation grounds — not yet a clean actionable. **XOM**, last cycle's best-long/catalyst pick, is now explicitly demoted by the **stocks_intraday_long_guard** (rolling paper-R drawdown guard) rather than by market-closed status — the guard is doing its job: stocks-intraday longs are net -1.0R/PF 0.67 this week vs shorts +3.0R/PF 2.0, so blocking a fresh long here is directionally correct even though the oil-shock catalyst is real. **XLE has dropped out of both the Top-Candidates and Rejected lists entirely this cycle** (was a clean A-raw catalyst pick at 16:20) — flagged as a minor data-quality TODO, not acted on. **GOOGL remains AVOID/MANUAL REVIEW** (EU $1B DMA fine, confirmed 16:20, unchanged; stale post-earnings setup). Crypto book is unchanged: BTC/ETH both still read **range**, no new A/B fired this cycle, all 25 active crypto signals remain B-tier at various lifecycle stages. The swing report is now **~12.6h old — crossing into the borderline-stale band (12-14h)** and still reads a divergent bullish/risk-on regime; treat it as carry-forward context only, not current. Catalyst mapping is unchanged and still weak (80.4% unmapped, same cumulative file as last cycle — no new catalyst scan ran). Scanning, tracking, and monitors continue regardless of this review's caution stance.

## 2. Data Used

- Crypto reports: `2026-07-23_12-48_scalp_report.md` (mtime 15:48, ~2.9h old), `2026-07-23_12-54_intraday_report.md` (mtime 15:54, ~2.8h old) — both cycle-fresh for the 2h scheduler cadence
- Swing report: `2026-07-23_03-05_swing_report.md` (mtime 06:05, ~12.6h old — **borderline stale, 12-14h band**; regime divergence vs intraday/stocks persists, now nearing the 14h hard-stale cutoff)
- Stocks intraday: `2026-07-23_15-30_stocks_intraday_report.md` (mtime 18:30, ~9min old, fresh — first RTH-generated report since the open, supersedes the 10:27 UTC pre-open report used last cycle)
- Stocks swing/invest: last available `2026-07-02_13-0x` reports (~21 days stale, unchanged — TODO-2 carried forward, not used)
- Catalyst layer: `data/catalysts/2026-07-23/catalyst_events.jsonl` (2,500 cumulative rows, unchanged count from last cycle — no new catalyst-scan cycle ran since `catalyst_cycle_13-02.md` at 16:02), `narrative_baskets.jsonl` (3 baskets this read)
- CLI: `active-signals` (crypto ×25, stocks ×50), `signal-stats` (crypto + stocks), `detect_untracked_legacy_alerts --since 2026-07-23` (clean — no untracked alerts)
- Direct SQL against `db/crypto_ai_desk.sqlite` (`news_items`): last-3h and last-8h feed scans for GOOGL/XOM/XLE/META/UNH — no fresh single-name catalyst beyond what the 16:20 review already verified externally; UNH still has zero news in the last 8h (DOJ probe status unchanged)
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-23_1620.md` (16:20 EEST, pre-US-open slot) — used for §4 comparison
- External: none fetched fresh this cycle — internal RTH data (VIX, breadth, index trends) independently confirms the risk-off/gap-down thesis the 16:20 review sourced from a single Telegram feed; the 16:20 review's external verification (GOOGL EU fine via CNN/Semafor, AI-capex theme via CNBC) is same-day and still valid, carried forward rather than re-fetched

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: 2026-07-23 18:07 (~32min old at read time) — not deferred
- Latest cycle summary: `cycle_02_15-39_summary.md` (~1h22m old) — well within defer threshold
- Monitors alive and current: `crypto_monitor` (18:36), `derivatives_monitor` (18:37/18:43), `pending_monitor` (18:39/18:44), `stocks_monitor` (18:39/18:41) — all updated within the last ~5-10 minutes
- Crypto scalp/intraday: ~2.8-2.9h old, within normal 2h-cycle cadence
- Swing: ~12.6h old — borderline stale (12-14h band); regime divergence (bullish/risk-on vs current range/mixed/risk-off) persists — do not treat swing regime label as current
- Stocks intraday: ~9min old, fresh, first RTH-generated read since today's 16:30 EEST open
- Stocks swing/invest: ~21 days stale — not used (TODO-2, unchanged)
- Catalyst scan: same cumulative file as last cycle (`catalyst_cycle_13-02.md`, 16:02) — no new scan needed/run this cycle

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-07-23 18:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["stocks swing/invest ~21d stale", "root cause for XLE disappearing from both top-candidates and rejected lists this cycle"],
      "suggested_effect": "advisory_only", "facts_used": ["scheduler.log 18:07", "monitor logs 18:36-18:44", "swing report mtime 06:05 (~12.6h)", "catalyst file unchanged at 2,500 rows / 80.4% unmapped"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.8,
      "reason_codes": ["risk_off", "shorts_preferred", "mixed", "chop"],
      "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["stocks regime flipped explicit risk_off/bias=short, VIX 17.70->19.94, breadth 0.0% above EMA20, SPY/QQQ confirmed downtrend", "crypto BTC/ETH both still range", "swing report (stale) still reads bullish/risk-on — divergence unresolved"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "catalyst_confirmed", "no_catalyst", "stale_catalyst"],
      "data_missing": ["fresh catalyst cycle since 16:02 (none run)"],
      "suggested_effect": "advisory_only", "facts_used": ["80.4% catalyst events unmapped, unchanged from last cycle", "GOOGL EU $1B fine still the cleanest confirmed single-name catalyst (carried from 16:20)", "META short thesis is thematic/sector-level only, not single-name-confirmed", "rwa_narrative (ONDO/XLM) and momentum_breakout (ZAMA/WLFI) baskets both single-source"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.4,
      "reason_codes": ["funding_extreme", "data_unavailable"],
      "data_missing": ["OI 24h change (n/a across all crypto derivatives rows this cycle)"],
      "suggested_effect": "advisory_only", "facts_used": ["ZAMA/DEXE negative funding + elevated crowding across bybit/mexc/okx cross-check — short-squeeze risk on any DEXE-style failed-bounce short"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "entry_late", "stale_before_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["META/GOOGL/AMZN/etc. all demoted for liquidity_rvol_below_min / sector_confirmation_weak_or_unknown this cycle — RTH volume confirmation has not yet caught up to the technical score", "crypto B-tier book unchanged, no fresh breakout confirmation"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["waiting_for_entry", "open_actionable", "no_entry", "review_shadow"],
      "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["25 crypto active-signal rows (all B-tier: waiting_for_entry / triggered / tp1_hit / tp2_hit mix)", "50 stocks active-signal rows (mostly C-tier, a few legacy B-tier tp2_hit)", "untracked-alert detector clean"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["legal_risk", "headline_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["GOOGL EU antitrust fine (unchanged since 16:20)", "UNH DOJ probe open/unchanged, zero news in 8h", "stocks_intraday_long_guard actively blocking XOM/LLY longs this cycle — consistent with long-direction PF 0.67 (n=36) vs short PF 2.0 (n=84)", "geopolitical Iran/Israel/oil-shock overlay unchanged"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["crypto scalp PF 0.67 (n=45, losing)", "crypto intraday PF 1.60 (n=82)", "crypto swing PF 2.96 (n=46, best mode)", "stocks short-direction PF 2.0 (n=119, reliable) vs long-direction PF 0.67 (n=66, stronger, negative avgR)", "stocks C-tier triggered winrate 4%"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "shorts",
    "best_long_candidate":     { "symbol": "WLFI/USDT", "trigger": "already-active B-tier crypto exposure (scalp waiting_for_entry 1.0519-1.0645 zone via KAITO/scalp and 0.0615-0.0625 intraday zone); track existing levels — RS-leader vs BTC/ETH, funding neutral, low crowding; do not originate a fresh stocks long into a risk_off/guard-blocked backdrop", "reason": "stocks longs are net-negative this week (PF 0.67, n=66) and the intraday long guard is actively blocking XOM/LLY; crypto RS-leader is the cleanest long-side exposure available" },
    "best_short_candidate":    { "symbol": "META", "trigger": "RTH relative-volume pickup (currently gated liquidity_rvol_below_min) plus sector confirmation on XLK/tech; once both clear, breakdown-continuation short aligns with the AI-capex-selloff theme and the strong stocks short-direction backdrop (PF 2.0, n=84)", "reason": "still A-raw score 94.5, downtrend confirmed at RTH, thematically tied to today's CNBC AI-spending-concern coverage, no legal/earnings flag" },
    "best_catalyst_candidate": { "symbol": "XOM", "trigger": "stocks_intraday_long_guard clearing (rolling paper-R drawdown improving) or manual-review override; oil-shock catalyst (Brent >$100/bbl, Iran/Israel escalation) remains fully intact and undiminished", "reason": "cleanest single-name-catalyst link this cycle (energy sector still RS-leader, 20d RS vs SPY now +11.93%, even stronger than pre-open's +6.82%) but systematically blocked by the risk guard — a routed watch, not a rejection of the thesis" },
    "avoid_candidate":         { "symbol": "GOOGL", "reason": "verified fresh EU $1B/EUR890M DMA antitrust fine (confirmed 16:20, unchanged) stacked on a stale post-earnings setup and an earnings-calendar labeling inconsistency (see TODO-8) — manual review required, never a clean actionable regardless of the aligned AI-capex-selloff short thesis" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.8 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | caution | 0.8 | risk_off, shorts_preferred, mixed, chop | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, catalyst_confirmed, no_catalyst, stale_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.4 | funding_extreme, data_unavailable | advisory_only |
| technical_entry | caution | 0.6 | chase_risk, entry_late, stale_before_entry | advisory_only |
| execution_lifecycle | ok | 0.8 | waiting_for_entry, open_actionable, no_entry, review_shadow | advisory_only |
| risk_manager | caution | 0.75 | legal_risk, headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.6 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | caution | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Compared to the 16:20 EEST (pre-US-open) review:

- **New, decision-relevant:** First RTH-generated stocks-intraday report of the day (15:30 UTC / 18:30 EEST) replaces the 10:27 UTC pre-open snapshot used last cycle. It confirms the gap-down/risk-off thesis internally: VIX 17.70→19.94, breadth-above-EMA20 0.0%, SPY/QQQ downtrend confirmed on 5d returns. This resolves TODO-7 (same-day print unverifiable via external search) without needing a fresh WebSearch this cycle.
- **Changed:** XOM's demotion reason shifted from "market-closed-planning" (pre-open) to the explicit **stocks_intraday_long_guard** (rolling paper-R drawdown guard) — a systematic, data-driven block, not a data-availability artifact. The guard is consistent with this week's stocks long-direction PF of 0.67 (negative avgR) vs short PF 2.0.
- **Changed:** XLE disappeared entirely from both the Top-Candidates and Rejected/Not-Ready tables this cycle — it was a clean pre-open A-raw pick (score 86, RS vs SPY +6.82%) at 16:20. Sector data shows XLE/energy is still "strong" and RS is now even stronger (+11.93% vs SPY 20d), so this looks like a scoring/candidate-generation gap rather than a thesis reversal — flagged as TODO-9 below, not acted on.
- **Unchanged:** GOOGL still avoid/manual-review (EU fine + stale post-earnings); UNH still open/unchanged DOJ probe (zero fresh news in 8h); META still A-raw but gate-demoted (now for liquidity/sector-confirmation reasons specifically, same substance as last cycle's "needs RTH confirmation"); crypto book unchanged (still 25 active B-tier signals, same names — WLFI, KAITO, OPN, EPIC, RE, ERA, BANK, TLM, ONDO, FIL, KITE, ZAMA, ALLO, ADA, VIRTUAL, PENGU, PUMP, NEAR — no new triggers this cycle); catalyst mapping still weak and numerically unchanged (80.4% unmapped, same cumulative file — TODO-1 unresolved); stocks swing/invest still ~21 days stale (TODO-2 unchanged); crypto BTC/ETH still range; swing report divergence persists and has moved from "carry-forward" (~10.3h at 16:20) into the "borderline stale" 12-14h band (~12.6h now) — approaching the hard-stale cutoff at the next (21:30) slot.
- **Thesis change:** None material — this cycle is a confirmation/refinement cycle rather than a new-thesis cycle. The 16:20 review's XOM/XLE/META/GOOGL calls all held directionally; only the actionability mechanics (why each is gated) sharpened.

## 5. Catalyst Coverage

- Catalyst events today (cumulative, unchanged from 16:20): **2,500** total; mapped: **490**; unmapped: **2,010** (**80.4% unmapped**).
- Narrative baskets: **3** in this read (rwa_narrative, perps_dex_narrative, momentum_breakout) — fewer than the 5 seen at 16:20 (ai_narrative, binance_ecosystem_teaser not present in this pull); no new catalyst-scan cycle ran, so this is a read-time variance in the aggregation view, not new data.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top unmapped headlines by importance (same set as last cycle, unresolved): (1) "BSquared hack drains $3.9M — can B2 recover after a 44% crash?" (imp 0.748); (2) "Warren Buffett's Berkshire Hathaway Has Barely Touched AI Stocks..." (imp 0.748); (3) "Why AFX Trade's $24.15M hack is another warning for crypto bridges" (imp 0.73). Root cause unchanged from TODO-1.

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **mixed** (BTC/ETH both range; macro risk score ~95/100 risk-off headwind carried from last cycle; no fresh scalp/intraday catalyst regime data this cycle beyond the unchanged macro read)
- Stocks mood: **risk-off, confirmed at the open** (VIX 19.94, breadth 0.0% above EMA20, SPY/QQQ downtrend on 5d, explicit regime label risk_off/bias=short)
- Dominant narrative: the Iran/Israel oil-shock overlay (Brent >$100/bbl) continues to drive both the energy-long thesis (XOM/XLE, still catalyst-intact but guard-blocked) and the broader risk-off tone; secondarily the AI-capex-spending-concern theme pressuring GOOGL/TSLA/META/semis
- Preferred side now: **shorts** (stocks short-direction PF 2.0 this week vs long PF 0.67 negative; stocks regime explicit risk_off/bias=short) with **catalyst-backed watch** on the energy longs specifically once the drawdown guard clears
- Best long candidate: **WLFI/USDT** (crypto, already-active B-tier exposure — see §8)
- Best short candidate: **META** (stocks, gate-blocked on liquidity/sector confirmation — see §8)
- Best catalyst-backed candidate: **XOM** (stocks, guard-blocked despite intact catalyst — see §8)
- What to avoid: GOOGL (legal + stale-earnings), UNH (open DOJ probe), fresh stocks longs generally (guard + weak PF), crypto scalp mode (PF 0.67), ETH/ARB/ADA/BNB (carried bridge-exploit cluster, unchanged from last cycle's read — re-verify before next cycle if not already resolved)
- What would change the view: RTH relative-volume confirmation on META/GOOGL/COIN clearing the liquidity gate; the stocks_intraday_long_guard resetting/clearing so the XOM/XLE oil-shock thesis becomes actionable; BTC/ETH reclaiming an uptrend; the swing/intraday regime divergence resolving one way or the other before it goes fully stale next cycle

## 7. Candidate Deep Dives

### 1. META (stocks, short, A-raw / gated to C)
- Has price already reacted to the catalyst? Yes at the theme level — CNBC's "Tesla and Alphabet shares slump as AI spending concerns spook investors" (today) is the cited driver, but it names TSLA/GOOGL specifically, not META — the META link is sector/theme-level, not single-name-confirmed. Same caveat as last cycle.
- Chasing? RTH data shows the setup still A-raw at score 94.5 with `sector_confirmation_weak_or_unknown` and `liquidity_rvol_below_min` — i.e. the technical score is strong but volume/sector confirmation genuinely has not caught up yet; not a chase, a genuine "not confirmed yet."
- Retest/pullback structure? Not detailed in this cycle's report excerpt; use the report's own levels once gates clear.
- Overextended? Not flagged.
- Actionable level: RTH relative-volume pickup + XLK/tech sector confirmation.
- Market-mood alignment: strong — short is the mood-preferred side this cycle (stocks short PF 2.0 vs long PF 0.67).
- Long/short/wait: short, wait for gate clearance.
- Invalidation: use report's own level once actionable (not detailed in this excerpt).
- Chase risk: moderate — mega-cap tech can snap back sharply on any de-escalation headline.
- Catalyst confirmation: thematic only, not single-name-specific — weaker than XOM/XLE's direct oil-shock link.
- Legal/headline check: none found for META today.

### 2. XOM (stocks, long, B-raw / gated to C via stocks_intraday_long_guard)
- Has price already reacted to the catalyst? Sector (XLE) RS vs SPY is now +11.93% (20d), stronger than the +6.82% seen pre-open — the oil-shock thesis is, if anything, strengthening, not fading.
- Chasing? Cannot assess — this candidate is blocked by a portfolio-level risk guard (rolling paper-R drawdown on stocks-intraday longs), not by a technical/chase concern.
- Actionable level: guard clears (drawdown metric recovers) or a human manually reviews and overrides given the catalyst strength.
- Market-mood alignment: the catalyst is aligned (energy long into an oil shock) but the mood-routing signal (short-preferred, long PF weak) argues the guard is directionally correct to be cautious here even so.
- Long/short/wait: long thesis intact, wait for guard clearance — do not treat as actionable regardless of catalyst strength.
- Invalidation: n/a while gated.
- Chase risk: n/a while gated.
- Catalyst confirmation: confirmed and intact (Brent >$100/bbl, Iran/Israel escalation).
- Legal/headline check: none found for XOM today.

### 3. XLE (stocks, sector ETF — data anomaly, not a trade call)
- No longer appears in either the Top-Candidates or Rejected/Not-Ready tables this cycle, despite sector data showing XLE "strong" and RS strengthening (+11.93% vs SPY 20d, up from +6.82% pre-open). This is a data-quality observation (TODO-9), not a thesis change — the underlying oil-shock/energy-strength thesis is captured via XOM instead.

### 4. GOOGL (stocks, avoid/manual-review — unchanged)
- **LEGAL/HEADLINE RISK — carried forward, verified 16:20, unchanged**: EU €890M (~$1B) DMA antitrust fine, confirmed via CNN/Semafor/wire.
- Stacked with the stale post-earnings setup (earnings printed 2026-07-22T20:35 UTC after-hours) and today's AI-capex-selloff reaction (CNBC).
- **Data inconsistency observed this cycle (TODO-8):** the report's earnings-risk advisory block lists GOOGL under "earnings risk ... today" alongside the do-not-chase warning, while the candidate-demotion note separately confirms the earnings print already happened yesterday (2026-07-22 20:35 UTC) and demotes for `stale_post_earnings_setup`. Both readings agree on the practical conclusion (avoid/do-not-chase), but the calendar-date labeling is internally inconsistent — flagged for manual review, not fixed here.
- Per §I discipline: final verdict remains **AVOID / MANUAL REVIEW REQUIRED**.

### 5. Crypto — WLFI/USDT (long, best-available long exposure, already active) and DEXE/USDT (short-watch, unchanged, low-confidence)
- WLFI: unchanged from last cycle — top RS leader (scalp score 100, intraday ~67), active `waiting_for_entry` scalp signal (1.0519-1.0645... actually zone per active-signals: scalp entry 0.0601-0.0613-equivalent tier; see active-signals table for exact current zone) and an intraday `waiting_for_entry` signal. Funding neutral, crowding low across venues — no squeeze warning. Tracking existing exposure, not a fresh idea.
- DEXE: still the weakest symbol (24h ~-29.6%, RS vs BTC ~-28.8%), negative funding + elevated crowding across bybit/mexc/okx cross-check (unchanged from last cycle) — a failed-bounce short candidate, but no formal level published, and crypto short-direction performance remains weak this week (anecdotal, n=8, PF 0.13 last read) — demand unusually strong confirmation before treating as actionable.

## 8. Best Candidates Ranked

1. **Long-watch: WLFI/USDT** (crypto) — already-active B-tier exposure; track per its own entry/invalidation levels; RS-leader, funding neutral, low crowding. Do not originate a fresh stocks long this window (guard-blocked, weak PF).
2. **Short-watch: META** (stocks) — trigger: RTH relative-volume pickup + XLK sector confirmation; thematic-only catalyst link, demand the technical confirmation given no single-name news.
3. **Catalyst-watch: XOM** (stocks) — trigger: stocks_intraday_long_guard clears, or manual-review override given the intact/strengthening oil-shock catalyst; not actionable this window regardless of catalyst strength.
4. **Avoid: GOOGL** (stocks) — verified fresh EU antitrust fine + stale post-earnings setup + earnings-calendar labeling inconsistency (TODO-8) — never actionable this window.
5. **Secondary short-watch (low-confidence): DEXE/USDT** (crypto) — failed-bounce/breakdown continuation; crypto short-direction PF weak this week — demand unusually strong confirmation.

## 9. Avoid / No Trade

This is a decision-window call only — scanning, data collection, tracking, and the scheduler continue unchanged.

- **GOOGL** — verified fresh EU antitrust fine stacked on a stale post-earnings setup and an internal earnings-date labeling inconsistency — manual review required.
- **UNH** — open federal DOJ investigation, re-verified zero fresh news in 8h — avoid new exposure regardless of technical score.
- **Fresh stocks longs generally** — this week's long-direction PF is 0.67 with negative avgR (n=66); the intraday long guard is actively blocking XOM/LLY for exactly this reason.
- **ETH/ARB/ADA/BNB** — carried bridge-exploit-cluster flag from last cycle; no fresh news checked this cycle to confirm resolution — treat as still-open until re-verified.
- **Crypto scalp mode generally** — PF 0.67 this week; extra scrutiny on any future scalp idea.
- **Chasing META/GOOGL/COIN/etc. shorts before the liquidity/sector gates clear** — the technical scores are strong (A-raw) but the gates exist precisely because RTH volume/sector confirmation hasn't caught up yet.

## 10. Main Risks

- **Regime divergence nearing hard-stale:** swing report (~12.6h old) still reads bullish/risk-on while intraday/scalp/stocks all read range-to-risk-off; this divergence will cross into the fully-stale >14h band by the next (21:30) slot if the swing job doesn't refresh — worth a status check.
- **Systematic long-side risk this week:** stocks-intraday long-direction PF 0.67 (negative avgR) vs short PF 2.0 — any fresh long idea (even catalyst-backed, like XOM) needs to clear the guard, not just look good on paper.
- **Catalyst layer degraded:** 80.4% of catalyst events unmapped, unchanged across cycles today — same resolver defect (TODO-1).
- **Data-generation gap:** XLE, a clean pre-open A-raw candidate, vanished from both candidate tables this cycle without a corresponding rejection reason — worth checking whether this is a display gap or a genuine scoring drop (TODO-9).
- **Legal/headline risk:** GOOGL (EU fine, unchanged), UNH (DOJ, unchanged), LLY (GLP-1 lawsuit, carried forward).
- **Data staleness:** stocks swing/invest ~21 days stale (TODO-2, unchanged); catalyst events file itself is a same-cycle cumulative read (no fresh scan since 16:02).
- **Unresolved bridge-exploit cluster:** ETH/ARB/ADA/BNB flagged last cycle, not re-verified this cycle (no fresh 3-8h news scan targeted these specifically beyond the general macro pull) — treat as still-open.

## 11. Action Plan — Next 4 Hours

- Watch META for RTH relative-volume pickup and XLK sector confirmation before treating the short as actionable.
- Watch XOM/XLE for the stocks_intraday_long_guard to clear (or flag for manual override) — the oil-shock catalyst remains intact and strengthening; this is a guard/timing question, not a thesis rejection.
- Do not touch GOOGL under any framing this window — manual review required regardless of price action; separately, flag the earnings-date labeling inconsistency (TODO-8) for a human to check the earnings-calendar source.
- Continue tracking existing WLFI exposure (scalp/intraday waiting) per its own entry/invalidation; do not add fresh crypto entries without a clean confirmation stack.
- Re-verify the ETH/ARB/ADA/BNB bridge-exploit cluster status before the next cycle (carried forward without a fresh check this cycle).
- Monitor whether the swing report refreshes before the 21:30 slot — if it's still ~03:05-generated by then, it will have crossed into the fully-stale >14h band and the regime-divergence question should be escalated more formally.
- Check whether XLE's disappearance from the candidate tables (TODO-9) recurs at the next cycle — if so, this becomes a higher-priority investigate item.
- No changes to scoring, thresholds, or scanning — system continues running as-is.

## 12. Final Verdict per Mode

- **Scalp:** No new A/B. Losing mode this week (PF 0.67) — extra scrutiny on any future scalp idea.
- **Intraday:** No new A/B this cycle; book unchanged (WLFI/BANK/OPN/TLM/ONDO/ZAMA/ADA/VIRTUAL/ALLO/KITE/PENGU/PUMP/KAITO watchlist/active-tracking only).
- **Swing:** Best-performing mode this week (PF 2.96) but the report is ~12.6h old (borderline stale) and still reads a regime (bullish/risk-on) diverging from the fresher intraday/stocks reads (range/risk-off); treat open positions (RE, EPIC, BANK, ERA) as tracking-only; do not originate new swing ideas off this read.
- **Stocks intraday:** First RTH-confirmed read of the day; regime is explicit risk_off/bias=short. META (short) and XOM/XLE (long, catalyst-backed) are the sharpest candidates but both are gate-blocked (liquidity/sector confirmation for META, rolling drawdown guard for XOM). GOOGL remains avoid/manual-review. No A/B actionable this window.
- **Stocks swing/invest:** Data ~21 days stale — do not use for any current decision (TODO-2, unchanged).

## 13. Sources

- Internal: `data/catalysts/2026-07-23/catalyst_cycle_13-02.md` (unchanged, 16:02 cycle)
- Internal: `data/reports/scalp/2026-07-23_12-48_scalp_report.md`, `data/reports/intraday/2026-07-23_12-54_intraday_report.md`, `data/reports/swing/2026-07-23_03-05_swing_report.md`, `data/reports/stocks/intraday/2026-07-23_15-30_stocks_intraday_report.md`
- Internal: `news_items` direct SQL — last-3h and last-8h scans for GOOGL/XOM/XLE/META/UNH (no fresh single-name catalyst beyond what was already verified at 16:20; UNH zero news in 8h confirms unchanged)
- Internal: CLI `active-signals`, `signal-stats`, `detect_untracked_legacy_alerts` (2026-07-23 18:3x-18:4x runs)
- Carried forward from prior review (same-day, still valid — not re-fetched this cycle): [EU slaps Google with record $1 billion antitrust fine — Semafor](https://www.semafor.com/article/07/23/2026/eu-slaps-google-with-record-1-billion-antitrust-fine) (2026-07-23); [Europe fines Google $1 billion for 'harming' rivals — CNN Business](https://edition.cnn.com/2026/07/23/business/europe-fines-google-1-billion-intl) (2026-07-23)
- Source unavailable: no fresh external WebSearch/WebFetch run this cycle — internal RTH data (VIX, breadth, index trends) was sufficient to confirm the risk-off thesis without needing external re-verification; see §4/§2 for reasoning.

## 14. Fix Requests / TODO

### TODO-1: Catalyst symbol resolver missing tickers spelled out literally in the headline (recurring — 4th consecutive cycle with evidence)
- **issue:** Funding-rate-adjustment and new-listing notices continue landing with a null symbol despite the ticker being present verbatim in the title.
- **evidence:** `data/catalysts/2026-07-23/catalyst_events.jsonl` — 2,010/2,500 (80.4%) unmapped, numerically identical to the 16:20 cycle (same cumulative file, no new scan run).
- **suggested manual fix:** Extend the symbol resolver's regex/lookup to catch `#Trading_Updates` / `#New_Listings`-style Binance/MEXC announcement formats where the ticker appears as a single concatenated token (e.g. `RIFUSDT`) rather than the usual `RIF/USDT` form.
- **priority:** high
- **first observed:** 2026-07-23 04:48 EEST; confirmed recurring at 11:39, 16:20, and again at 18:39 EEST.

### TODO-2: Stocks swing/invest reports ~21+ days stale (unchanged)
- **issue:** `data/reports/stocks/swing/` and `data/reports/stocks/invest/` have no report newer than 2026-07-02.
- **evidence:** latest files still `2026-07-02_13-0x`.
- **suggested manual fix:** investigate why the stocks swing/invest report generator stopped running or is failing silently; check scheduler config for these two report types.
- **priority:** high
- **first observed:** carried forward from 2026-07-23 04:48 EEST review; unchanged this cycle.

### TODO-8: GOOGL earnings-calendar date labeling inconsistency (new this cycle)
- **issue:** The stocks-intraday report's earnings-risk advisory lists GOOGL under "earnings risk ... today (2026-07-23)" with a do-not-chase warning, while the same report's candidate-demotion note for GOOGL separately states the earnings print already happened 2026-07-22T20:35:42 UTC (after-hours) and demotes the candidate for `stale_post_earnings_setup`. Both conclusions point the same direction (avoid/do-not-chase) so no bad trade resulted, but the two calendar reads disagree on whether earnings are upcoming or already-printed.
- **evidence:** `data/reports/stocks/intraday/2026-07-23_15-30_stocks_intraday_report.md` §16 ("Earnings risk (as of 2026-07-23): today [GOOGL, LMT]") vs §7 candidate note ("stale_post_earnings_setup: verified earnings print (2026-07-22T20:35:42+00:00) while calendar is UNKNOWN").
- **suggested manual fix:** Check the earnings-calendar source feed for GOOGL — it appears the calendar itself is marked UNKNOWN (per the demotion note) while a separate feed is defaulting to "today," producing the conflicting labels. Likely related to the same earnings-calendar-regression class of issue noted in past sessions.
- **priority:** medium
- **first observed:** 2026-07-23 18:39 EEST (this run).

### TODO-9: XLE disappeared from both Top-Candidates and Rejected/Not-Ready tables this cycle (new this cycle)
- **issue:** At 16:20 (pre-open data), XLE was a clean A-raw candidate (score 86.07, long, catalyst-backed by the oil shock). In this cycle's fresh RTH report, XLE does not appear in either §5 (Top Candidates) or §8 (Rejected/Not Ready) — it is simply absent, even though the sector-rotation section still shows energy/XLE as "strong" with RS vs SPY strengthening to +11.93% (20d).
- **evidence:** `data/reports/stocks/intraday/2026-07-23_15-30_stocks_intraday_report.md` §2 (sector strength) vs §5/§8 (candidate tables) — XLE present in the former, absent from both of the latter.
- **suggested manual fix:** Check the candidate-generation pipeline for why an ETF/sector symbol that scored cleanly pre-open dropped out entirely post-open rather than being carried through to either an actionable or a rejected state with a reason.
- **priority:** medium
- **first observed:** 2026-07-23 18:39 EEST (this run).

_Carried-forward TODO-3, TODO-4, TODO-5, TODO-6 from the 11:39 EEST review remain open and unchanged (regime-divergence display question, past-expiry-signal display question, `no_gate_context` stocks-intraday loss bucket, `telegram-test` underscore parse_mode bug) — not re-detailed here to avoid duplication; see `OPUS_ENRICHED_REVIEW_AUTO_2026-07-23_1139.md` §14 for full text. TODO-7 (same-day open print unverifiable via external search) is resolved as of this cycle — see §4._
