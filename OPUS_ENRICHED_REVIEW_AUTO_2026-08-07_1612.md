# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:12 EEST

## 1. Executive Summary

Slot: **pre-US-open decision review** (target 08:55 ET / 15:55 Nicosia-cron; actual data-gathering window ~08:59-09:12 ET, Δ+4-17min, within tolerance). **Advisory only — no auto-trade, no scoring/threshold/strategy changes.** Stocks are still **closed** (RTH opens ~09:30 ET / ~16:30 EEST, <20 min away) — every stocks item below is planning-only until the open confirms it. Crypto stays the only live-actionable class this slot; regime remains **bullish** (BTC/ETH uptrend, altcoin breadth 57.1%) under a still-pinned **100/100 macro risk-off headline score**, unchanged all week. Crypto scalp remains **kill-switched** (config, not a bug); crypto intraday's **XAI/USDT B-tier long has now filled cleanly inside its 0.0074-0.0077 pullback zone** (current 0.0078) — this is the desk's cleanest actionable idea today. This cycle ran the **Stocks Pre-US Review Overlay** for the first time this run window: 28 raw candidates (10 unique symbols) cleared the code's `market_closed_intraday_planning_only`-only gate; after catalyst/RS/legal diligence, **zero cleared the bar for SUPPORT** — two carry real event risk worth flagging explicitly (**PYPL**: extended +32%/month into a reported $53B Stripe/Advent takeover rumor at $60.50, entry sits right under that price; **CSCO**: AI-order catalyst is a stale recap of Tue's move with FQ4 earnings only 5 trading days out). EPIC/USDT's OHLCV gap remains unresolved (6th+ consecutive cycle). Catalyst mapping is weak this run (53.8% unmapped) — treat catalysts as context, not final decision.

## 2. Data Used

- `data/reports/scalp/2026-08-07_11-36_scalp_report.md` (mtime 14:36 EEST)
- `data/reports/intraday/2026-08-07_11-44_intraday_report.md` (mtime 14:44 EEST)
- `data/reports/swing/2026-08-07_02-55_swing_report.md` (mtime 05:55 EEST — carry-forward, ~10h17m old)
- `data/reports/stocks/intraday/2026-08-07_12-20_stocks_intraday_report.md` (mtime 15:20 EEST)
- `data/catalysts/2026-08-07/catalyst_events.jsonl`, `narrative_baskets.jsonl` (mtime 14:50 EEST)
- `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md` (generated this cycle, 28 eligible / 80 excluded)
- `db/crypto_ai_desk.sqlite` — `proposed_signals`, `signal_outcomes`, `news_items`, `watchlist_alerts` (read-only queries)
- `python -m src.cli active-signals` ×2 (crypto/stocks), `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-08-07`
- `data/scheduled_runs/2026-08-06_default_schedule/scheduler.log`, `cycle_06_14-25_summary.md`
- WebSearch/WebFetch (market futures, CSCO, PYPL, MA, TSM/GS/MS, NFLX/COST/BKNG/ADBE) — 6 queries, 1 fetch
- `OPUS_ENRICHED_REVIEW_AUTO_2026-08-07_1145.md` (previous review, for §4 comparison)

## 3. Scheduler / Data Freshness

- Pre-US schedule check: target 08:55 ET, actual fire ~08:59 ET (Δ+4min, within tolerance). No DST-mismatch window active (2026 windows are 03-08→03-29 and 10-25→11-01; today 08-07 is outside both).
- Scheduler: `scheduler.log` mtime 15:41 EEST (~31min old at report time) — **fresh**.
- Latest cycle summary: `cycle_06_14-25_summary.md` mtime 15:41 EEST — **fresh**. All steps `[OK]` except **step 39 `intelligence layer update` — `[FAIL]` (timeout after 300s)**, non-critical background enrichment (§14 TODO).
- Report freshness: scalp/intraday **fresh** (~95/88min old); stocks intraday **fresh** (~52min old); swing **carry-forward** (~10h17m, 4-12h band — used, flagged).
- Monitor status: crypto watchlist monitor (5m), crypto pending monitor (30s), MEXC canary (3s), derivatives monitor (2m), stocks monitor (1m) — all reported `[OK]`/background-running in the latest cycle.
- Paper status: paper execution/structural-TP/structural-stop refresh all `[OK]` this cycle (accounting-only, no live).
- Non-terminal signal backlog (still-open TODO from last review): crypto 57, stocks 166 — stocks backlog grew from the 159 flagged 2026-08-07 11:45 (§14 continuation).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-08-07 16:12 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["swing report >10h old (carry-forward band)", "catalyst mapping only 46.2% mapped this cycle", "no live premarket/RVOL feed for stocks candidates"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 15:41 EEST", "cycle_06 all-OK except intelligence-layer-update timeout"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["mixed", "risk_on", "longs_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/ETH uptrend, alt breadth 57.1%", "macro risk 100/100 risk-off 8th+ consecutive cycle", "stocks regime bullish, VIX 15.18, breadth 100%"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "stale_catalyst", "no_catalyst"],
      "data_missing": ["premarket reaction to CSCO catalyst"],
      "suggested_effect": "advisory_only",
      "facts_used": ["1156/2500 catalyst_events mapped today (53.8% unmapped)", "5 narrative baskets", "CSCO AI-order raise is a Tue recap not a fresh trigger", "PYPL $53B takeover rumor at $60.50"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.55,
      "reason_codes": ["oi_supports", "data_unavailable"],
      "data_missing": ["crowding % for ACE/BICO/XAI (unknown)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ACE/BICO/XAI: price up + OI up, fresh positioning confirms trend"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["chase_risk", "overextended", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["XAI filled cleanly in 0.0074-0.0077 zone, now 0.0078 (near top)", "ACE/BICO both trading above their pullback zones on both intraday and swing reports"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.7,
      "reason_codes": ["open_actionable", "needs_review", "no_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 17 triggered / 2 tp1-tp2_hit / 8 expired in last 24h", "stocks: 119 stale_before_entry+missed_no_entry in last 24h (market mostly closed)", "2 untracked legacy alerts today (ALLO, ADA)", "EPIC/USDT candles=0 gap persists as of 13:13 UTC"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["headline_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["macro risk-off headline score pinned 100/100", "PYPL entry (59.76) sits directly under a rumored $60.50 takeover price — binary confirm/deny risk", "CSCO FQ4 earnings 2026-08-12, 5 trading days out"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing PF 6.22 (n=53)", "crypto intraday PF 2.01 but WR only ~20% (n=62)", "crypto scalp PF 0.125, correctly kill-switched", "stocks intraday resolved sample n=6, 0 wins, PF 0.17"] },
    { "agent": "head_trader", "verdict": "advisory_only", "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "XAI/USDT", "trigger": "already filled 0.0074-0.0077, now 0.0078 — manage risk, do not add on further extension", "reason": "cleanest fill of the cycle, RS-leader, OI confirms trend, invalidation at 0.0071 well-defined" },
    "best_short_candidate":    { "symbol": "HEI/USDT", "trigger": "confirmed failed bounce on 1h/4h before any entry (no formal signal yet)", "reason": "weakest RS in the tape again today (24h -29.1%, RS vs BTC -29.8%), still unconfirmed as a clean short" },
    "best_catalyst_candidate": { "symbol": "CSCO", "trigger": "wait for RTH open + volume confirmation; do not chase pre-market off the recap headline; re-check proximity to 2026-08-12 earnings before any entry", "reason": "only pre-US stocks candidate with a genuinely entity-resolved, material catalyst (AI order target raised to $9B), but it is several days stale and earnings-proximity risk is real" },
    "avoid_candidate":         { "symbol": "PYPL", "reason": "entry (59.76) sits directly beneath a reported $53B Stripe/Advent takeover rumor at $60.50/share after a +32% one-month move — binary confirm/deny event risk, not a clean momentum long" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.75 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.70 | mixed, risk_on, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, stale_catalyst, no_catalyst | advisory_only |
| derivatives_squeeze | ok | 0.55 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.65 | chase_risk, overextended, clean_retest | advisory_only |
| execution_lifecycle | needs_review | 0.70 | open_actionable, needs_review, no_entry | advisory_only |
| risk_manager | caution | 0.65 | headline_risk, reduce_risk | advisory_only |
| playbook_performance | caution | 0.60 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution (synthesis) | 0.65 | — | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-07_1145.md` (Europe/pre-US context, 11:30 EEST slot, ~4h27m ago).

- **XAI/USDT**: was `waiting_for_entry` in the pullback zone — **now filled/triggered** cleanly inside 0.0074-0.0077, current 0.0078. Thesis confirmed, unchanged direction; upgraded from "watch" to "manage open position."
- **STG/USDT**: was the #2 long-watch last cycle (pullback zone 0.1480-0.1537) — dropped out of this cycle's B-tier intraday list entirely; not carried forward as a fresh idea this run (§7b of the intraday report shows it rejected on no-fresh-catalyst grounds this cycle).
- **ONDO/USDT**: was the catalyst-watch pick last cycle (beta-rotation-if-XLM-stabilizes) — no longer appears as an active idea in today's reports; superseded this cycle by the new **Stocks Pre-US Review Overlay** catalyst pick (CSCO).
- **HEI/USDT**: unchanged — still the best short-watch, still unconfirmed, still the weakest-RS symbol on the tape.
- **New this cycle**: first run of the Stocks Pre-US Review Overlay — 10 unique stocks candidates reviewed, 0 SUPPORT, 6 CAUTION, 4 INSUFFICIENT_DATA (§5).
- **DOGE/USDT avoid** and **MSFT/REGN/BLK legal-gated** carry forward unchanged.
- **EPIC/USDT** data gap: unresolved, now confirmed again at 13:13 UTC — 6th+ consecutive cycle.
- **Stale non-terminal backlog**: stocks grew 159→166, crypto 16→57 (crypto count uses a slightly different window here — see §14, needs reconciliation, not a new regression).

## 5. Catalyst Coverage

- Total `catalyst_events` today: 2500. Mapped (non-null symbol): 1156 (46.2%). Unmapped: 1344 (53.8%).
- `narrative_baskets` today: 5 (`rwa_narrative`, `binance_ecosystem_teaser`, `ai_narrative`, `delisting_thin_liquidity`, `momentum_breakout`).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Top 3 unmapped headlines: (1) "Pomerantz Law Firm Announces the Filing of a Class Action Against Microvast Holdings" (2) "Pomerantz Law Firm... Insulet Corporation" (3) "INVESTOR ALERT: Pomerantz... ZoomInfo Technologies" — legal-firm press-release spam, mostly unrelated to today's candidates.

### Pre-US Stocks Review Overlay
- candidates reviewed: 10 unique (SUPPORT 0 / NEUTRAL 1 / CAUTION 6 / BLOCK 0 / INSUFFICIENT_DATA 3, over 28 raw signal_ids)
- session-cap-only C's now eligible for pre-open Paper lane: 10 (all `market_closed_intraday_planning_only`-only, no substantive gate)
- excluded by hard gate: 80 signal_ids across ~40 unique symbols — mostly `EARNINGS_BLACKOUT` (NVDA, META, TSLA, AVGO, MCD, DIS, PLTR, HD, XOM, UNH, LLY, etc.) and `LEGAL_RISK` (MSFT, BLK, REGN, COIN); a handful `NO_ENTITY_RESOLVED_CATALYST` (SNOW, AMGN, NOW, PANW, ORCL, SMCI, XLU/XLK/XLY/XLC, AXP, QCOM, NOC)
- Verdicts: MA (NEUTRAL, stale catalyst); CSCO/PYPL/TSM/MS/GS (CAUTION — see §7); NFLX/COST/BKNG/ADBE (INSUFFICIENT_DATA — no material catalyst found internally or via WebSearch this cycle)
- Ingested via `stocks-preus-review-ingest`; adjusted scores confirmed (no clamps triggered — all requested adjustments accepted as-is, e.g. CSCO 85.35→80.35, PYPL 100.0→94.0). These remain **C-tier / not actionable** pending RTH confirmation regardless of the adjustment.

## 6. Market Landscape

- **Crypto**: BTC/ETH both uptrend; altcoin breadth 57.1% above EMA20/50; recommended style "selective longs, prefer pullbacks on RS." Derivatives on the strongest names (ALLO/BICO/XAI/ACE) show fresh long positioning (price up + OI up) except ALLO/EPIC/TUT (price up + OI down — short-covering, weaker continuation quality). Macro/geopolitical risk score pinned at **100/100** for the 8th+ consecutive review (Iran/Strait-of-Hormuz, Poland/Russia headline, weak jobs data) sitting under a fully long crypto book with zero fresh short exposure — unresolved tension flagged every cycle this week.
- **Stocks**: regime **bullish** — VIX 15.18, all 4 major indices in uptrend, breadth 100% above EMA20/50. Strongest sectors: energy (RS +3.85%), financials (RS +1.85%), materials (RS +1.56%). Weakest: semiconductors (RS **-8.21%**), utilities (-6.12%), technology (-2.25%). Weak US jobs data (July: -23k vs +83k expected, unemployment flat at 4.1%) is pushing futures higher pre-open on rate-cut hopes — a "bad news is good news" setup, worth remembering if the print gets revisited intraday.
- RIOT reports earnings today — avoid holding through/chasing. CSCO/SMCI/CSCO earnings within the week (CSCO 2026-08-12).

### Market Mood / Risk Routing
- Crypto mood: **mixed** (technically risk-on tape, but macro headline layer stuck risk-off 100/100)
- Stocks mood: **pre-market / closed, bullish bias** (VIX 15.18, 100% breadth, futures up on weak-jobs rate-cut hopes)
- Dominant narrative: momentum/RS-leader continuation in low-cap alts (ALLO/BICO/XAI/ACE), no single dominant catalyst theme
- Preferred side now: **longs (crypto, existing book)** / **wait-for-RTH-confirmation (stocks)**
- Best long candidate: **XAI/USDT** — filled cleanly, manage existing position
- Best short candidate: **none confirmed — HEI/USDT on a failed-bounce trigger**
- Best catalyst-backed candidate: **CSCO** — real catalyst but stale + earnings-proximity risk; treat as watch, not a chase
- What to avoid: **PYPL** (M&A-rumor binary risk), **DOGE/USDT** (delisting/thin-liquidity), any pre-market stock entry without RTH confirmation
- What would change the view: a clean 15m breakout+VWAP-hold confirmation on any of today's stocks candidates after the open; BTC losing local support (flip crypto routing defensive); a confirm/deny headline on the PYPL takeover rumor

## 7. Candidate Deep Dives

### 1. XAI/USDT — LONG (crypto intraday, B-tier, score 72.9) — best long-watch, now OPEN

- Has price reacted to a catalyst? No fresh verified catalyst — pure RS/momentum (24h +22.3%, 7d +30.2%, RS vs BTC +21.6%).
- Chasing? No — filled inside the planned 0.0074-0.0077 zone; current 0.0078 is right at the top edge, so **do not add here**.
- Retest/pullback structure? Yes, that's exactly how it filled.
- Overextended (>2 ATR from EMA20)? Not per the report; execution quality flagged only a minor risk penalty (-4.5).
- Aligned with market mood? Yes — RS-leader long in a risk-on (technically) tape.
- Actionable now or wait? Already actionable/filled — this is a **manage, not enter** item.
- Invalidates at: 1h close beyond 0.0071.
- Chase risk: low for the existing fill, high for any fresh add above 0.0078.
- Catalyst confirmation/contradiction: none either way — known failure mode is "no-catalyst intraday in chop is net-negative (WR23%/PF0.70/-3R)," so this trade leans on RS/derivatives confirmation, not catalyst.

### 2. ACE/USDT — LONG (crypto, swing 79.3 + intraday 67.1, already in book) — hold, not a fresh entry

- Multiple ACE signals already active across intraday and swing (`triggered`); this is the strongest RS name on the tape (24h +77-87%, RS vs BTC +77-87%) with the best-performing playbook this week (swing PF 6.22).
- Current price (~0.1355 as of the 14:44 report) sits **above both** the intraday (0.1236-0.1318) and swing (0.1204-0.1284) pullback zones — a fresh entry here would be chasing.
- Derivatives: price up + OI up (+36.5-109%) = fresh positioning confirms trend, but funding negative (shorts crowded) and crowding unknown.
- Verdict: hold the existing position, do not add; wait for a fresh pullback into either zone before considering more size.

### 3. CSCO — LONG (stocks C-tier, base_score 85.3, pre-gate A) — best catalyst-backed, CAUTION

- Catalyst: Cisco raised its FY26 AI infrastructure order target to $9B (from $5B), YTD orders $5.3B, entity-resolved and confirmed via WebFetch (Motley Fool, published 2026-08-07). **But** the underlying stock reaction (+5% to $121.74) happened Tuesday 2026-08-04 — today's articles are recap/analysis, not the original trigger. Internal entry_trigger (120.89) sits just below that Tuesday close.
- **FQ4 earnings land 2026-08-12 — 5 trading days out.** Outside the code's literal `EARNINGS_BLACKOUT` window but a real proximity risk the code's hard gate could not weigh — do not chase into it.
- Sector context: technology RS is mixed (-2.25% vs SPY 20d) — no sector tailwind.
- Verdict: **CAUTION**, adjustment -5 (85.35→80.35, still C-tier/not actionable pending RTH). Actionable only with a clean 15m breakout+VWAP-hold after the open, and only with earnings-proximity risk explicitly acknowledged.

### 4. PYPL — LONG (stocks C-tier, base_score 100.0, pre-gate A) — avoid candidate

- Catalyst: best month ever in July (+32%+), driven by a Q2 beat **and** a reported $53B Stripe/Advent International takeover bid at $60.50/share (WebSearch-confirmed, multiple sources).
- Internal entry_trigger 59.76 / stop 59.31 sit **directly beneath** the rumored deal price — this is binary confirm/deny event risk, not a clean momentum long. If the rumor is confirmed the stock could gap through the trigger without a fillable retest; if denied, expect a sharp reversal.
- Analyst sentiment is itself described as mixed/cautious on execution risk despite the headline strength.
- Verdict: **CAUTION**, adjustment -6 (100.0→94.0, still C-tier/not actionable). Treat as **avoid for a fresh momentum entry**; only relevant if the desk later wants explicit M&A-event exposure, which is out of scope for this framework.

### 5. HEI/USDT — SHORT (crypto, unconfirmed watch, carried forward) — best short-watch

- Weakest symbol on the tape again today: 24h -29.1%, RS vs BTC -29.8%, bias short per the scalp report's "Where Money Is Flowing — Weakest Symbols" list.
- No formal scored signal yet — this is pre-signal watchlist context, not a tracked `proposed_signal`.
- Actionable only after a **confirmed failed bounce** on 1h/4h with a defined stop above the swing high — do not pre-empt or short into the current bleed.
- Counter-thesis: short squeeze risk is real in this tape (multiple other short setups this week were capped to C for exactly this reason); wait for confirmation, not just weakness.

## 8. Best Candidates Ranked

1. **XAI/USDT** — filled cleanly, manage the open position, invalidation 0.0071.
2. **ACE/USDT** — hold existing book (intraday + swing), no new entries, wait for a fresh pullback.
3. **CSCO** — best catalyst-backed stocks watch, wait for RTH open + 15m breakout/VWAP-hold confirmation; earnings-proximity risk noted.
4. **HEI/USDT** — best short-watch, wait for confirmed failed bounce.
5. **BICO/USDT** — same shape as ACE: strong RS (24h +72.8%), already above its 0.0474-0.0495 pullback zone at 0.0505 — hold/watch for pullback, not a fresh entry.

No candidate this cycle clears the bar for an outright fresh actionable A/B call in either asset class before the open.

## 9. Avoid / No Trade

This applies to the current decision window only — scanning, tracking, and the scheduler continue unaffected.

- **PYPL** — M&A-rumor binary risk directly under the entry trigger (§7.4); avoid a fresh momentum long here.
- **DOGE/USDT** — fresh `delisting_thin_liquidity` basket following the Bonk/Upbit delisting story; thin-liquidity capitulation risk, not a trade setup (unchanged from last review).
- **MSFT / REGN / BLK (stocks)** — permanently legal/delisting-gated regardless of score; do not treat as promotable even after the open (unchanged).
- **All fresh stocks entries pre-open** — market closed, planning-only; do not chase pre-market moves without RTH + volume confirmation.
- **EPIC/USDT** — do not treat displayed `triggered` status as a fresh signal; the OHLCV gap (candles=0) is confirmed again as of 13:13 UTC this cycle; existing holders should know live-price tracking is unreliable.

## 10. Main Risks

- **Macro/crypto divergence, 8th+ consecutive cycle**: risk-off geopolitical headline score pinned 100/100 under a fully long, zero-fresh-short crypto book — unresolved and un-de-risked all week.
- **PYPL M&A-rumor gap risk**: entry sits directly under a rumored takeover price; any confirm/deny headline could produce a large, un-fillable gap in either direction — flagged explicitly this cycle, not previously reviewed under this framework.
- **CSCO earnings-proximity chase risk**: catalyst is stale, earnings are 5 trading days out; the code's blackout gate did not catch this but the risk is real.
- **EPIC/USDT data-integrity gap**: unresolved for a 6th+ consecutive cycle (candles=0 on binance/1h) — needs a human session, not another monitoring cycle.
- **Growing stale non-terminal backlog**: stocks 166 / crypto 57 signals sitting non-terminal — the crypto figure needs reconciliation against the 16 cited in the last review (different window/query, not necessarily a new regression — see §14).
- **Untracked legacy alerts recurring**: 2 today (ALLO/USDT, ADA/USDT, both ~12:05-12:37 UTC) — continuation of the known high-priority watchlist-alert/signal-reuse bug (tracked externally as TODO-3 since 2026-07-17).
- **Intelligence-layer-update timeout**: this cycle's step 39 timed out after 300s — non-critical background enrichment, but worth a look if it recurs next cycle.

## 11. Action Plan — next few hours (through and past the US cash open)

- Manage the open XAI/USDT long (invalidation 0.0071); do not add above 0.0078.
- Hold the existing ACE/BICO/ALLO and broader ~57-position crypto book; no new crypto entries this cycle.
- Watch HEI/USDT for a confirmed failed bounce before any short entry.
- At/after the RTH open (~16:30 EEST): re-check CSCO for a clean 15m breakout+VWAP-hold before any paper entry; re-check PYPL's takeover-rumor headline status before touching it at all; treat both re-checks as mandatory, not optional, since the pre-open gate only cleared the market-closed cap, not these two risks.
- Avoid PYPL and DOGE/USDT for the remainder of this decision window.
- Monitor the Iran/Hormuz and jobs-data headline flow for any escalation or reversal that would flip crypto/stocks routing.
- Escalate EPIC/USDT's OHLCV gap and the untracked-alert recurrence to a human maintenance session (§14) — both are now multi-cycle-confirmed, not one-off.

## 12. Final Verdict per Mode

- **Crypto scalp**: kill-switched off (config, not a bug) — no trade, data collection only.
- **Crypto intraday**: XAI/USDT filled cleanly and is the cycle's best actionable idea — manage, don't add. No A-tier.
- **Crypto swing**: report carry-forward (~10h) but regime confirmed bullish by fresher streams; ACE/BICO the strongest lane this week — hold, no new entries.
- **Stocks (all modes)**: market closed — planning/watchlist only. Pre-US overlay reviewed 10 unique candidates; 0 SUPPORT, best catalyst watch is CSCO (caution), clearest avoid is PYPL. Re-evaluate every candidate individually at/after the ~16:30 EEST open with fresh RTH confirmation — the pre-open gate does not substitute for that.

## 13. Sources

- [Cisco Raised Its AI Order Target to $9 Billion. Here's What Investors Need to Know. (The Motley Fool, 2026-08-07)](https://www.fool.com/investing/2026/08/07/cisco-raised-its-ai-order-target-to-9-billion-here/) — WebFetch-verified; confirms $9B AI order target, FQ4 earnings 2026-08-12.
- [Stock Market Today (Aug. 7, 2026): S&P 500 futures rise after July jobs report shows unexpected losses (TheStreet)](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-aug-7-2026) — weak July jobs data (-23k vs +83k expected), rate-cut-hope futures rally.
- WebSearch results (titles/sources cited inline, no single canonical URL): PayPal/Stripe-Advent $53B takeover-bid reporting and July +32% move (multiple outlets incl. CNBC/Yahoo Finance PYPL quote pages); Mastercard Aug 1 earnings beat + BVNK acquisition (Simply Wall St, Traders Union, GuruFocus); Taiwan Semiconductor sector commentary incl. a Goldman Sachs "turns its back" headline (MSN/TheStreet/Bloomberg aggregation); Netflix flat price action + minor co-CEO share transaction (Robinhood/ts2.tech/Yahoo Finance NFLX pages) — dates as cited in §7, exact URLs not individually reproduced where the search returned aggregated snippets rather than a single article.
- Internal: `news_items` table (SQLite, read-only) for MS/TSM/NFLX/COST/BKNG/CSCO/ADBE/MA/PYPL/GS, last-24h window.
- `data/catalysts/2026-08-07/catalyst_events.jsonl`, `narrative_baskets.jsonl`.
- `OPUS_ENRICHED_REVIEW_AUTO_2026-08-07_1145.md` (previous review, §4 comparison).

## 14. Fix Requests / TODO

### TODO-untracked-legacy-alerts-recurring (priority: high, continuation of tracked issue)
- **issue:** `detect_untracked_legacy_alerts` shows 2 untracked crypto alerts again today (ALLO/USDT 12:05:28 UTC, ADA/USDT 12:37:00 UTC) — both sent to Telegram but with no backing `proposed_signal`, so they won't contribute to PF/winrate/avgR tracking.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-07` output, this cycle.
- **suggested manual fix:** this is a continuation of the watchlist-alert/signal-reuse bug already tracked externally as high-priority (raised 2026-07-17, confirmed on ALLO/USDT and BANK/USDT previously) — today's ALLO/ADA occurrence is fresh evidence the root cause is still unresolved, not a new bug.
- **priority:** high
- **first observed (this recurrence):** 2026-08-07 16:12 EEST (root issue first observed 2026-07-17)

### TODO-epic-usdt-ohlcv-gap-still-unresolved (priority: high, 6th+ consecutive cycle)
- **issue:** EPIC/USDT swing signal `sig_f6259f2dfc6f2f63` remains `status=triggered` while `signal_outcomes` logs `candles=0` on `binance/1h` — confirmed again as of 2026-08-07T13:13:32Z, the most recent check.
- **evidence:** `SELECT checked_at, entry_triggered, notes FROM signal_outcomes WHERE signal_id='sig_f6259f2dfc6f2f63' ORDER BY checked_at DESC LIMIT 3` → all rows `candles=0`, `entry_triggered=1`.
- **suggested manual fix:** investigate the OHLCV fetch path for EPIC/USDT on `binance/1h` directly — likely a delisting/symbol-rename/thin-liquidity edge case; this needs a human session, monitoring alone won't resolve it.
- **priority:** high
- **first observed:** 2026-08-06 18:48 EEST (now confirmed unresolved for a 6th+ consecutive review)

### TODO-intelligence-layer-update-timeout (priority: low, new observation this cycle)
- **issue:** Cycle 6 (14:25 EEST) step 39 `intelligence layer update` failed with a 300s timeout (`scripts.intelligence_update --limit 80`), the only non-OK step in an otherwise clean cycle.
- **evidence:** `data/scheduled_runs/2026-08-06_default_schedule/cycle_06_14-25_summary.md`, step 39, `exit=-1, 300.3s`.
- **suggested manual fix:** check whether this is a one-off (transient load/network) or recurring across recent cycles; if recurring, consider raising the timeout or profiling `scripts.intelligence_update` for a slow step.
- **priority:** low
- **first observed:** 2026-08-07 16:12 EEST (single occurrence so far, not yet confirmed recurring)

### TODO-stale-backlog-crypto-figure-reconciliation (priority: medium, carried forward from 2026-08-07 11:45)
- **issue:** This review's §3 cites crypto non-terminal backlog as 57 (via `status IN ('generated','waiting_for_entry','triggered','tp1_hit','tp2_hit')` with no age filter), while the 2026-08-07 11:45 review's corrected query (same status set, but filtered to `>7 days past expires_at`) found only 16. These are different queries (all-non-terminal vs. >7d-stale-non-terminal) and are not directly comparable — worth standardizing which figure future reviews should cite so the trend is trackable.
- **evidence:** this review's ad-hoc `COUNT(*) WHERE asset_class='crypto' AND status IN (...)` (no age filter) = 57; prior review's `>7 days past expires_at` variant = 16.
- **suggested manual fix:** decide a single canonical query (age-filtered vs. not) for this metric and document it in the routine so future reviews don't silently switch definitions.
- **priority:** medium
- **first observed:** 2026-08-07 16:12 EEST
