# Opus Enriched Review — post-close final daily review — Auto Cycle 23:29 EEST

## 1. Executive Summary

Slot: **post-close final daily review** (23:29 EEST, 2026-07-23, ~29min after the 23:00 EEST US cash close). **Advisory only — no auto-trade, no scoring/strategy changes.** Daily wrap: US indices closed **red across the board** — Dow −1.0% (−507pts), S&P 500 −1.2%, Nasdaq −2.2% — driven by GOOGL (−7% on raised AI-capex guidance despite a beat) and TSLA (−14% on 2026 "massive capex year" commentary plus a $112M crypto paper loss), compounded by Brent crude crossing $100/bbl on Houthi tanker-attack escalation in the Red Sea (externally confirmed, see §13). Stocks book: **0 A/B-tier actionable** all session (US cash now closed — every raw-A/B name demoted to C for `market_closed_intraday_planning_only`); MSFT/TSLA/GOOGL carry standing AVOID/MANUAL-REVIEW legal-headline flags, all previously externally verified and unchanged tonight. Crypto book: **0 A-tier, 0 B-tier fresh** on scalp or intraday; regime reads bearish-trend/risk-off (scalp) to range/chop (intraday) — mixed but net cautious; best watchlist idea remains ZAMA/USDT (62.4/100, momentum_breakout basket, fresh <1h, no verified catalyst — pure RS/momentum). The crypto scalp report step **failed again this cycle** (exit=1, "database is locked" pattern recurring — 2 of 5 scalp attempts failed today: 19:18 and 22:47 EEST) — see TODO-1, escalated (recurring, not a one-off). **XLE remains absent from both stocks Top-Candidates and Rejected/Not-Ready for a 4th consecutive cycle** despite energy still reading "strong" in sector rotation (RS +10.12% vs SPY) — TODO-4 escalation continues. One **untracked legacy alert** detected (ZAMA/USDT B-tier intraday, sent 18:57 UTC, no matching `proposed_signal`) — consistent with the known watchlist-alert-reuse bug already tracked project-side (TODO-5). Catalyst mapping is **weak** at 79.1% unmapped (2,769/3,500 cumulative today) — use as context only. Overnight-into-Asia: crypto regime is genuinely mixed (BTC/ETH transition_down but altcoin breadth ~40% and RS leaders like BANK/ZAMA/LA still running), no clean short confirmed (all fresh crypto shorts are squeeze-risk-capped), no clean long confirmed (all crypto longs are chase-risk/no-catalyst watchlist only) — routed to **watch-only, both sides**, not a blanket no-trade. Scanning, tracking, and monitors continue regardless of this review's caution stance.

## 2. Data Used

- Crypto reports: `2026-07-23_19-20_scalp_report.md` (Generated 22:20 EEST, data freshness 19:15 UTC / 22:15 EEST, ~1.3h old — cycle-fresh, this is the last *successful* scalp run before tonight's second failure), `2026-07-23_19-59_intraday_report.md` (Generated 22:59 EEST, data freshness 19:45 UTC / 22:45 EEST, ~0.7h old, fresh)
- Swing report: `2026-07-23_03-05_swing_report.md` (mtime 06:05 EEST, ~17.4h old — **stale, >14h band**, excluded from final verdict, carry-forward context only)
- Stocks intraday: `2026-07-23_20-01_stocks_intraday_report.md` (data freshness 20:00 UTC / 23:00 EEST, ~0.5h old, fresh — right at the cash close)
- Stocks swing/invest: last available `2026-07-02_13-0x` reports (~21 days stale, unchanged — TODO-2 carried forward, not used; framework deprecated per project notes)
- Catalyst layer: `data/catalysts/2026-07-23/catalyst_events.jsonl` (3,500 cumulative rows across today's 7 scan cycles; 731 mapped / 2,769 unmapped = 79.1% unmapped), `narrative_baskets.jsonl` (3 baskets: perps_dex_narrative, rwa_narrative, momentum_breakout)
- CLI (re-run fresh this cycle): `active-signals` (crypto ×17, stocks ×50), `signal-stats` (crypto n=173 reliable, PF 1.771; stocks headline n=0 / C-tier n=181, PF 0.5625), `detect_untracked_legacy_alerts --since 2026-07-23` → **1 untracked alert** (ZAMA/USDT)
- Scheduler log direct read (`scheduler.log`, latest activity 23:26 EEST): crypto scalp report exit=1 at 22:51 (2nd failure today; also failed 19:23), crypto intraday report exit=0 at 23:01, stocks intraday report in progress at time of read
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-23_2139.md` (21:39 EEST, late-session risk review) — used for §4 comparison
- External (WebSearch, 1 query this cycle — internal news_items already had fresh GOOGL/TSLA/oil coverage within 6h, so only the closing-bell recap needed external confirmation): "stock market close July 23 2026 Dow S&P Nasdaq AI capex oil" — see §13

## 3. Scheduler / Data Freshness

- `scheduler.log`: latest activity 23:26 EEST (~3min old at read time) — not deferred, well under the 3h defer threshold
- No finished cycle-summary file yet for the in-progress cycle (last completed: `cycle_03_19-17_summary.md`, finished 20:06); current cycle's steps are visible directly in `scheduler.log` through 23:26
- Monitors: pending monitor (pid 18412), MEXC canary (pid 12516), derivatives monitor (pid 21000), stocks monitor (pid 21800, restarted this cycle), telegram dashboard (pid 17420) — all healthy/reused per scheduler.log
- Crypto scalp: last **successful** run 22:09→22:25 EEST (~1.3h old, cycle-fresh); a **second** attempt at 22:47→22:51 EEST failed (exit=1, "database is locked" pattern) — do not expect a fresher scalp read until the next cycle clears the lock
- Crypto intraday: 22:51→23:01 EEST, exit=0, ~0.5h old, fresh
- Swing: ~17.4h old — stale (>14h), excluded from final verdict per policy
- Stocks intraday: data freshness 23:00 EEST, ~0.5h old, fresh (right at today's cash close)
- Stocks swing/invest: ~21 days stale — not used (TODO-2, unchanged; framework deprecated)
- Catalyst scan: latest integrated cycle ~23:05 EEST, fresh

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "post_close",
  "as_of": "2026-07-23 23:29 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["crypto scalp report failed a 2nd time today (22:47-22:51, DB-lock pattern) — running on the 22:09-22:25 successful snapshot instead", "stocks swing/invest ~21d stale", "XLE absent from stocks Top-Candidates/Rejected for a 4th consecutive cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log latest activity 23:26 EEST (~3min old)", "scalp report CMD END exit=1 at 22:51:58 (277.9s), 2nd failure today after 19:23", "swing report mtime 06:05 (~17.4h, stale)", "catalyst file 3,500 rows / 79.1% unmapped"] },
    { "agent": "market_regime", "verdict": "mixed", "confidence": 0.75,
      "reason_codes": ["mixed", "risk_off", "chop", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto scalp regime: bearish trend (risk-off), BTC/ETH both transition_down, altcoin breadth 38.5% above EMA20", "crypto intraday regime: range/chop (neutral), altcoin breadth 41.0% above EMA20 — slightly less bearish than the scalp read 45min earlier", "stocks regime risk_off/bias=short, VIX 19.41, breadth above EMA20 0.0%, all 4 indices non-uptrend", "external: Dow -1.0%, S&P -1.2%, Nasdaq -2.2% at the close, GOOGL -7%, TSLA -14%, Brent >$100/bbl on Red Sea tanker attacks"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "catalyst_confirmed", "no_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["79.1% catalyst events unmapped today (731/3,500 mapped)", "GOOGL earnings/capex-guidance selloff externally confirmed and matches internal news_items (18:00-18:58 UTC rows)", "momentum_breakout basket (BANK/ZAMA/AIXDROP) fresh <1h, single_source, no verified catalyst per intraday report itself — pure momentum", "rwa_narrative (ONDO/XLM) and perps_dex_narrative (HYPE) baskets unchanged, still single_source"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.45,
      "reason_codes": ["squeeze_risk", "data_unavailable"],
      "data_missing": ["OI 24h change n/a for most fallback_via_mexc symbols", "symbol-level crowding beyond 'normal/unknown' labels for several names"],
      "suggested_effect": "advisory_only",
      "facts_used": ["all fresh crypto C-tier short candidates (SYN, DEXE, CRCLB, TSLAB, KITE, GOOGLB) are explicitly capped by the scoring layer for 'short squeeze risk' (thin_liquidity or high_upper_wick) — none is a clean fresh short tonight", "LA/USDT external funding negative across bybit/mexc/okx (crowding elevated) despite +29% 24h — a long here would be fighting negative funding"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["entry_late", "chase_risk", "stale_before_entry", "price_moved_away"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto Top Trade Ideas: 0 A-tier, 0 B-tier on both scalp and intraday — 'No trade. Data does not justify a fresh idea right now.'", "ZAMA/USDT best crypto watchlist idea at 62.4/100, current price 0.0544 already above the 0.0528-0.0539 conditional pullback zone — would be chasing at current price", "stocks: 13 A/B-raw names all demoted to C purely on market_closed_intraday_planning_only (session over) — nothing tradeable until 09:30 ET tomorrow"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.75,
      "reason_codes": ["open_actionable", "review_shadow", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["17 crypto active-signal rows: all tp1_hit/tp2_hit (OPEN actionable / partial-TP progressing under the touch-based tracker, not literal closes) — no fresh entries tonight", "50 stocks active-signal rows: mostly C-tier triggered/tp1_hit/tp2_hit shadow, 3 legacy B-tier already tp2_hit (AAPL, GOOGL, XOM)", "1 untracked legacy alert this cycle: ZAMA/USDT B-tier intraday sent 18:57 UTC with no matching proposed_signal — needs review, known bug pattern (TODO-5)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["legal_risk", "headline_risk", "reduce_risk", "manual_review"],
      "data_missing": ["fresh <48h single-name legal news for TSLA's going_concern tag specifically — remains unconfirmed per prior-cycle research (TODO-3, unchanged)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["MSFT securities_fraud class action externally confirmed (carried from 21:39 cycle, unchanged) — AVOID stands", "TSLA legal/headline tag (going_concern) still gates to AVOID; today's actual TSLA news is capex-guidance-driven selloff (-14%) plus a $112M crypto paper loss disclosure, not a fresh going-concern development — tag provenance still unverified (TODO-3)", "GOOGL now additionally carries a fresh, externally-confirmed earnings-day selloff (-7%) and a stale_post_earnings_setup gate (earnings printed 2026-07-22T20:35:42 UTC, calendar UNKNOWN) — do_not_chase_warning active", "UNH DOJ probe confirmed and escalating (carried, unchanged)"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto headline (A/B): sample=173 reliable, winrate 24.9%, PF 1.771, totalR +37.01 — by mode: scalp PF 0.617 (losing, n=45, totalR -4.60), intraday PF 1.604 (n=82, +14.50), swing PF 3.259 (best, n=46, +27.11)", "crypto direction split: long PF 1.921 (n=165, reliable) vs short PF 0.125 (n=8, anecdotal, -3.50R) — shorts are a small, weak sample, reinforcing tonight's squeeze-capped short read", "stocks headline (A/B): sample=0 this week — zero actionable stocks trades fired; C-tier diagnostic PF 0.5625 / winrate 1.7% (n=181, weak, worse than the 2% read at 21:39)"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "ZAMA/USDT", "trigger": "1h close back inside the 0.0528-0.0539 pullback zone with volume confirmation; current price 0.0544 is already above the zone — do not chase", "reason": "top-scored crypto watchlist idea (62.4/100), primary of the fresh <1h momentum_breakout basket, RS +26.5% vs BTC, but explicitly no verified catalyst — momentum/RS-only thesis" },
    "best_short_candidate":    { "symbol": "AAPL", "trigger": "09:30 ET open + first 15-30min RTH confirmation (RVOL/sector) before treating the score-89 raw-A short as live; market is closed now, planning-level only", "reason": "cleanest (no legal/headline flag, unlike MSFT/TSLA/GOOGL) of the 13 raw-A/B stocks names demoted purely on market_closed_intraday_planning_only; directionally aligned with the confirmed AI-capex/tech selloff that closed the session" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT", "trigger": "second independent source confirming the MEXC tokenized-stock listing catalyst, plus a fresh technical re-score (not re-scored as a trade idea since prior cycles)", "reason": "rwa_narrative basket primary alongside XLM, fresh <24h, but still single-source and technically unassessed this cycle" },
    "avoid_candidate":         { "symbol": "MSFT", "reason": "externally-confirmed active securities-fraud class action (lead-plaintiff deadline Aug 11 2026) stacked on an A→C demotion; highest raw score on the desk (92.13) but not a tradeable short despite the close-day tech selloff" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.70 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | mixed | 0.75 | mixed, risk_off, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, catalyst_confirmed, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.45 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | entry_late, chase_risk, stale_before_entry, price_moved_away | advisory_only |
| execution_lifecycle | needs_review | 0.75 | open_actionable, review_shadow, needs_review | advisory_only |
| risk_manager | caution | 0.75 | legal_risk, headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.65 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | caution | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Comparing against `OPUS_ENRICHED_REVIEW_AUTO_2026-07-23_2139.md` (21:39, late-session risk review):

- **New this cycle:** the crypto scalp report failed a **second** time today (22:47-22:51, same DB-lock signature as the 19:18 failure) — this is now a recurring pattern (2 of 5 attempts today), not a one-off; TODO-1 escalated from "investigate" to "recurring, needs a real fix."
- **New this cycle:** US cash session actually **closed** — Dow -1.0%, S&P -1.2%, Nasdaq -2.2%, confirming and finalizing the AI-capex/oil-shock thesis flagged pre-close. GOOGL closed -7%, TSLA -14% (both worse than the pre-close reads cited at 21:39).
- **New this cycle:** 1 untracked legacy crypto alert detected (ZAMA/USDT, 18:57 UTC) — the 21:39 review's detector ran clean; this is a fresh occurrence of the known watchlist-alert-reuse pattern (TODO-5).
- **Confirmed/unchanged:** MSFT securities-fraud AVOID stands (unchanged). UNH DOJ AVOID stands (unchanged). TSLA going_concern tag remains externally unverifiable (TODO-3, unchanged, not re-checked this cycle to avoid redundant external calls on an unchanged fact). GOOGL now carries both the earnings-day selloff AND the stale_post_earnings_setup gate — consistent, reinforced.
- **Escalated:** XLE's absence from stocks Top-Candidates/Rejected is now a **4th consecutive cycle** (16:20 → 18:39 → 21:39 → 23:29), still reading "strong" in sector rotation (RS +10.12% vs SPY, essentially flat from +10.89% at 21:39) — TODO-4 remains high priority.
- **head_trader best-long pick shifted** from KAITO/USDT (21:39, pullback zone 1.020-1.034) to ZAMA/USDT (23:29, pullback zone 0.0528-0.0539) — both are the top-scored watchlist idea of their respective cycle, reflecting the intraday report's refreshed "Where Money Is Flowing" ranking, not a thesis reversal. Best-short pick (AAPL) and avoid pick (MSFT) are unchanged for continuity across cycles.

## 5. Catalyst Coverage

- Total catalyst_events today (cumulative, 7 scan cycles): **3,500**
- Mapped (non-null symbol): **731** (20.9%)
- Unmapped (null symbol): **2,769** (**79.1%**)
- Narrative baskets: **3** (perps_dex_narrative, rwa_narrative, momentum_breakout)

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

Top 3 unmapped headlines (sampled from today's cumulative file):
1. "First in Market: MEXC to List WOODUSDT Futures in Innovation Zone on Jul 22, 2026, 14:30 (UTC)"
2. "Adjustment to RIFUSDT Funding Rate Settlement Frequency [Jul 22, 2026, 16:05 (UTC)]"
3. "Adjustment to BNCUSDT Funding Rate Settlement Frequency [Jul 22, 2026, 16:05 (UTC)]"

(Same pattern flagged at 21:39: exchange-ops notices where the ticker is present in the title but not resolved — see TODO-2, unchanged.)

## 6. Market Landscape

**Crypto:** Scalp-report regime (22:15 UTC data) reads **bearish trend (risk-off)**: BTC/ETH both transition_down, altcoin breadth 38.5% above EMA20. The intraday report 45min later (19:45 UTC data) reads slightly less bearish — **range/chop (neutral)**, breadth 41.0% — a small improvement but not a regime flip. Strongest 24h movers both reads: LA/USDT (+29-31%, 3.4x volume, momentum/RS leader), ZAMA/USDT (+25%), BANK/USDT (+13-16%) — the `momentum_breakout` narrative basket (fresh <1h). Weakest: DEXE/USDT (-49% to -52% 24h, catalyst-backed short thesis but already crowded/squeeze-prone). Macro/geopolitical risk score is pinned at **100/100** both reads — Iran/Red Sea war-powers headlines, oil >$100/bbl externally confirmed. Notable single-name risk: Verus-Ethereum bridge exploited for a **second time in two months** ($7.54M drained) — sentiment-negative for ETH-adjacent DeFi.

**Stocks:** Regime **risk_off / bias=short**, VIX 19.41, breadth above EMA20 **0.0%**, all 4 major indices non-uptrend. Confirmed at the close: Dow -1.0% (-507pts), S&P -1.2%, Nasdaq -2.2%. Strongest sectors: energy (XLE, RS +10.12% vs SPY — but absent from the tradeable-candidate list, see TODO-4), healthcare (XLV, +4.56%), financials (XLF, +3.24%) — all defensive/oil-linked rotation. Weakest: semiconductors (SMH, -6.94%), consumer discretionary (XLY, -6.18%), technology (XLK, -3.20%). Driver: GOOGL -7% (raised AI-capex guidance despite an earnings beat) and TSLA -14% (2026 "massive capex year" commentary, Optimus/robotaxi/data-center focus, plus a $112M crypto paper-loss disclosure) dragged the Mag-7-heavy indices down; oil crossing $100/bbl on Houthi tanker-attack escalation in the Red Sea added a second, independent risk-off driver.

### Market Mood / Risk Routing
- Crypto mood: **mixed / chop-leaning-risk-off** (scalp read bearish, intraday read range/chop 45min later — genuinely inconsistent between reads, not a clean regime either way)
- Stocks mood: **risk-off, session closed** (confirmed at the bell: Dow/S&P/Nasdaq all red, VIX elevated, breadth 0%)
- Dominant narrative: AI-capex-spending disappointment (GOOGL, TSLA) compounding an oil-price shock (Red Sea escalation, Brent >$100/bbl) — a genuine two-driver risk-off day, now closed and confirmed rather than developing
- Preferred side now: **wait-for-trigger** (crypto — no clean side, mixed regime) / **shorts, planning-only** (stocks — aligned with the confirmed selloff but market is closed until 09:30 ET)
- Best long candidate: ZAMA/USDT — watch only, pullback zone 0.0528-0.0539, currently trading above it (0.0544) — do not chase
- Best short candidate: AAPL — planning-level only (market closed), needs RTH RVOL/sector confirmation at tomorrow's open
- Best catalyst-backed candidate: ONDO/USDT — RWA/tokenized-stock listing narrative (rwa_narrative basket), single-source, still not cross-confirmed after 2+ cycles
- What to avoid: MSFT, TSLA, UNH (all legal/headline-risk gated to AVOID/MANUAL REVIEW), GOOGL (stale post-earnings setup + do-not-chase-into-earnings warning still technically active for the next session), fresh DEXE/SYN/CRCLB/TSLAB/KITE/GOOGLB crypto shorts (all explicitly squeeze-risk-capped by the scoring layer tonight — chasing an already-crowded short is the main crypto risk)
- What would change the view: a second independent source confirming the ONDO listing catalyst; BTC/ETH reclaiming trend structure to resolve the crypto chop/bearish inconsistency between tonight's two reads; RTH RVOL/sector confirmation clearing on AAPL or peers at tomorrow's open; the crypto scalp-report DB-lock issue getting fixed so scalp-mode isn't running on a stale/failed cadence

## 7. Candidate Deep Dives

### 1. ZAMA/USDT (crypto, watchlist, long) — best long-watch
- Has price already reacted to the catalyst? No verified catalyst exists — the intraday report explicitly states "no fresh verified catalyst detected"; this is a pure RS/momentum play (part of the `momentum_breakout` basket, fresh <1h, single_source).
- Is the setup chasing? Yes at current price (0.0544) — the conditional pullback zone is 0.0528-0.0539, below current price.
- Retest / pullback structure? Explicitly a wait-for-pullback playbook (`crypto_intraday_catalyst_or_momentum`); known failure mode: "no-catalyst intraday in chop is net-negative — needs RS-leader or breakout confirmation."
- Overextended? Not >2 ATR (ATR 0.0024, price 0.0544 vs support 0.0468/resistance 0.0597) but sitting above the entry zone.
- Would entry now be late? Yes — entering at 0.0544 without waiting for the pullback fill would be chasing.
- Actionable level: 1h close and hold inside 0.0528-0.0539.
- Aligned with market mood? Marginally — tonight's crypto mood is mixed/chop-leaning-risk-off, not a clean risk-on tailwind; this is a name-specific momentum play, not a regime-aligned trade.
- Long, short, or wait-for-trigger? Wait-for-trigger long.
- Actionable now or after confirmation? After confirmation (pullback fill + volume).
- Invalidation: 1h close below 0.0515.
- Chase risk? High at current price; low if the pullback zone is respected.
- Catalyst confirmation/contradiction? None — technical/RS-only, explicitly no catalyst.

### 2. AAPL (stocks, watchlist, short) — best short-watch
- Has price already reacted to the catalyst? At the sector/index level yes (Nasdaq -2.2%, tech-wide AI-capex-linked selloff, externally confirmed) but AAPL carries no single-name legal/earnings flag tonight.
- Is the setup chasing? Not assessable — market is closed; this is a planning-level pick, not a live entry.
- Retest / pullback structure? N/A — breakdown-continuation short thesis, not a pullback-long.
- Overextended? Not assessed vs EMA20 in tonight's report; the only gate applied is `market_closed_intraday_planning_only`.
- Would entry now be late? Market is closed — there is no "now" to enter; re-evaluate at the 09:30 ET open.
- Actionable level: RTH open + RVOL/sector confirmation in the first 15-30min.
- Aligned with market mood? Yes — directly aligned with the confirmed risk-off close.
- Long, short, or wait-for-trigger? Wait-for-trigger short (post-open).
- Actionable now or after confirmation? After confirmation (tomorrow's RTH open).
- Invalidation: would invalidate if futures/premarket reverse sharply positive overnight or sector rotation flips.
- Chase risk? Moderate — one of 13 similarly-gated names; don't force the first one that trips at the open.
- Catalyst confirmation/contradiction? Catalyst (AI-capex selloff) is externally confirmed and index-wide, not AAPL-specific — no company-specific AAPL news tonight beyond general Motley Fool commentary.

### 3. ONDO/USDT (crypto, catalyst-backed, long) — best catalyst-watch
- Has price already reacted to the catalyst? Basket-level yes (rwa_narrative flagged fresh <24h) but not independently re-verified at the single-name level this cycle (no fresh news_items row for ONDO in the last 6h internally).
- Is the setup chasing? Unclear — not re-scored as a fresh trade idea this cycle (catalyst-detection only).
- Retest / pullback structure? Not assessed this cycle.
- Overextended? Not assessed this cycle — carried-forward TODO to re-score with a fresh technical read.
- Would entry now be late? Cannot say without a fresh technical read.
- Actionable level: second independent source confirming the MEXC Ondo tokenized-stock listing, plus a fresh technical re-score.
- Aligned with market mood? Independent of the broader risk-off mood — idiosyncratic single-name catalyst.
- Long, short, or wait-for-trigger? Wait-for-trigger long (catalyst-backed).
- Actionable now or after confirmation? After confirmation.
- Invalidation: catalyst fails to cross-confirm across two additional cycles, or basket is contradicted by a subsequent scan.
- Chase risk? Cannot assess without a fresh technical read.
- Catalyst confirmation/contradiction? Still single-source only — unchanged for at least 2 consecutive cycles now (worth flagging if it stays single-source through tomorrow, see TODO-2/§14 note).

### 4. MSFT (stocks, avoid) — best avoid candidate
- Highest raw score on the desk tonight (92.13, short) but tier-demoted A→C for `active legal/headline risk (securities_fraud)`.
- Externally confirmed in the 21:39 cycle (unchanged tonight): real, currently-pending securities-fraud class action (W.D. Wash., No. 26-cv-02071; lead-plaintiff deadline Aug 11 2026).
- Verdict: **AVOID / MANUAL REVIEW REQUIRED** — do not treat as a clean short despite the score, and despite today's broad tech selloff giving it directional tailwind.

### 5. TSLA (stocks, needs review) — flagged for data-integrity follow-up, and today's real news
- Score 90.06 raw (this cycle) / demoted A→C for `active legal/headline risk (going_concern)`.
- Today's **actual** TSLA news is a confirmed, externally-verified capex-guidance selloff (-14% at the close) plus a $112M crypto paper-loss disclosure — neither is a going-concern event.
- The `going_concern` tag itself remains externally unverified as of the 21:39 cycle's research (capex-scrutiny/accounting-tweak commentary found, no confirmed auditor going-concern opinion) — not re-checked this cycle to avoid redundant external calls on an unchanged fact; TODO-3 stands.
- Verdict: system gate left untouched (AVOID stands per current pipeline behavior) but flagged as **possibly stale or mistagged** — a human re-check of the tag's source record is still owed (TODO-3).

## 8. Best Candidates Ranked

1. **AAPL** (short-watch, planning-only) — cleanest (no legal flag) of the 13 raw-A/B tech names, directly aligned with today's confirmed close-day selloff. Trigger: RTH open + RVOL/sector confirmation tomorrow.
2. **ZAMA/USDT** (long-watch) — top-scored crypto watchlist idea, defined levels, RR to TP1 1.84R once triggered. Trigger: pullback zone 0.0528-0.0539 fill + hold.
3. **ONDO/USDT** (catalyst-watch) — real but still single-source RWA/tokenized-stock catalyst, now unconfirmed for 2+ consecutive cycles. Trigger: second-source confirmation + fresh technical re-score.
4. Runner-up short-watch (planning-only, all market-closed-gated): GOOGL, AMZN, TSLA (ex-legal-flag), COIN, QQQ, MSTR, SPY, XLF, PLTR, XLY — same gate as AAPL; AAPL remains the cleanest of the group.
5. Runner-up crypto watch: RIF/USDT (59.4/100, +54% 24h, low confidence, no catalyst), BANK/USDT (58.4/100, no catalyst) — both weaker/lower-confidence versions of the same no-catalyst-momentum thesis as ZAMA.

No clean actionable trade exists on either book tonight — every candidate above is a **watch**, not a live entry. Stocks are additionally planning-only until the next RTH session.

## 9. Avoid / No Trade

This is a decision-window verdict only — scanning, tracking, and the scheduler continue regardless.

- **MSFT** — confirmed active securities-fraud litigation. AVOID.
- **UNH** — confirmed, escalating DOJ antitrust + Medicare-billing-fraud probes. AVOID.
- **GOOGL** — stale post-earnings setup (earnings printed 2026-07-22, calendar UNKNOWN) plus today's confirmed do-not-chase-into-earnings warning; carried AVOID/MANUAL REVIEW.
- **TSLA** — going_concern tag unconfirmed externally (TODO-3); treat as MANUAL REVIEW pending human source-check, separate from today's real (and unrelated) capex-selloff news.
- **DEXE/USDT, SYN/USDT, CRCLB/USDT, TSLAB/USDT, KITE/USDT, GOOGLB/USDT** — all explicitly squeeze-risk-capped by the scoring layer tonight; any fresh short here is a crowded-short chase, not a clean entry.
- **New crypto scalp entries generally** — this cycle's second scalp-report attempt failed (DB-lock); do not treat the current scalp snapshot (22:20 EEST) as more current than ~1.3h old, and expect it may not refresh again until the lock issue is fixed (TODO-1).

## 10. Main Risks

- Crypto scalp report pipeline failure recurred a **second time today** (22:47-22:51, same DB-lock signature as 19:18-19:23) — if this keeps recurring, scalp-mode should be treated as structurally unreliable, not just occasionally stale (TODO-1, escalated).
- Touch-based paper PnL: all 17 active crypto signals show tp1_hit/tp2_hit status. Per standing project audit findings, `final_r = highest-TP-touched` overstates realized PnL vs realistic execution — do not read these as confirmed wins without the realistic-execution overlay.
- Catalyst mapping stuck near 79-80% unmapped across the full session today — catalyst-backed decision-making is running on roughly a fifth of the available signal.
- 1 untracked legacy alert (ZAMA/USDT) sent to Telegram tonight with no backing `proposed_signal` — will not contribute to PF/winrate tracking; matches a known, previously-flagged bug pattern (TODO-5).
- Two independent risk-off drivers converged today (AI-capex disappointment + oil >$100/bbl on Red Sea escalation) rather than one — if either intensifies overnight (further Middle East escalation, or a broader AI-capex re-rating spreading beyond GOOGL/TSLA to the rest of the Mag-7), crypto could follow stocks lower into the Asia session rather than decouple.
- Crypto regime read was internally inconsistent tonight (scalp: bearish trend/risk-off at 22:15 UTC data vs intraday: range/chop/neutral at 19:45 UTC data, ~1.5h apart) — treat the "mixed" mood label as a genuine straddle, not a resolved read, until tomorrow's Asia-session data clarifies it.

## 11. Action Plan — next 4 hours

- Watch ZAMA/USDT for a 1h close back inside 0.0528-0.0539; do not chase the current 0.0544 price.
- Watch ONDO/USDT for a second independent source on the MEXC listing catalyst before treating it as tradeable; flag for a fresh technical re-score once/if confirmed.
- No new crypto scalp entries until the next scalp cycle actually succeeds (2 failures today); check whether the DB-lock issue clears on its own or needs the TODO-1 fix.
- Do not originate fresh shorts on DEXE/SYN/CRCLB/TSLAB/KITE/GOOGLB tonight — all squeeze-risk-capped, crowded already.
- Into the 04:30 overnight/Asia review: check whether BTC/ETH resolve the scalp-vs-intraday regime inconsistency one way or the other, whether Asia-session altcoin breadth holds ~40% or breaks down, and whether the Red Sea/oil situation escalates further overnight (would reinforce risk-off into tomorrow's US pre-market).
- Into tomorrow's pre-US-open review: re-check AAPL/GOOGL/peers for gap risk against tonight's close, and confirm whether XLE resurfaces in the stocks candidate pipeline (TODO-4, now 4 cycles absent).

## 12. Final Verdict per Mode

- **Crypto scalp:** NO TRADE — running on a ~1.3h-old snapshot after tonight's 2nd DB-lock failure; do not expect a fresher read until the lock clears.
- **Crypto intraday:** WATCH ONLY — 0 A/B setups; ZAMA/USDT best watchlist idea, currently above its entry zone (chase risk), not yet triggered.
- **Crypto swing:** CARRY-FORWARD ONLY — report >14h stale, excluded from live decisions.
- **Stocks intraday:** PLANNING ONLY — US cash session closed; 0 A/B actionable; 13 raw-A/B names gated purely on market-closed; MSFT/TSLA/UNH/GOOGL explicitly AVOID or MANUAL REVIEW; re-evaluate all levels fresh at the 09:30 ET open.
- **Stocks swing/invest:** NOT USED — deprecated framework, data ~21 days stale.

## 13. Sources

- [Stock market today: Dow, S&P 500, Nasdaq sell off as rising oil prices, bond yields, and AI capex weigh — Yahoo Finance](https://finance.yahoo.com/markets/live/stock-market-today-thursday-july-23-dow-sp-500-nasdaq-oil-bonds-earnings-084444369.html) (Jul 23 2026)
- [Stock Market News for July 23, 2026 — Yahoo Finance (SG)](https://sg.finance.yahoo.com/news/stock-market-news-july-23-132100785.html) (Jul 23 2026) — closing-bell recap: Dow -507pts/-1.0%, S&P -1.2%, Nasdaq -2.2%, GOOGL -7%, TSLA -14%, Brent crossing $100/bbl on Houthi tanker-attack claims
- [MSFT ALERT: Securities Fraud Class Action Launched Against Microsoft Corporation — August 11, 2026 Deadline — AccessNewswire](https://www.accessnewswire.com/newsroom/en/business-and-professional-services/msft-alert-securities-fraud-class-action-launched-against-micros-1187343) (Jul 2026) — carried from 21:39 cycle, unchanged
- [UnitedHealth Group (UNH) Faces Wider DOJ Antitrust Probe As Claritev Review Expands — Yahoo Finance](https://finance.yahoo.com/healthcare/articles/unitedhealth-group-unh-faces-wider-221504204.html) (Jul 2026) — carried from 21:39 cycle, unchanged
- Internal: `data/reports/scalp/2026-07-23_19-20_scalp_report.md`, `data/reports/intraday/2026-07-23_19-59_intraday_report.md`, `data/reports/stocks/intraday/2026-07-23_20-01_stocks_intraday_report.md`, `data/catalysts/2026-07-23/catalyst_events.jsonl`, `data/scheduled_runs/2026-07-23_default_schedule/scheduler.log`, `active-signals`/`signal-stats` CLI output (this cycle), `scripts.detect_untracked_legacy_alerts` output (this cycle)

## 14. Fix Requests / TODO

### TODO-1: crypto scalp report step recurring "database is locked" failures
- **issue:** The "crypto scalp report" scheduler step failed for the **second time today** (22:47:20-22:51:58 EEST, exit=1, 277.9s), matching the same `OperationalError: database is locked` signature first flagged at 19:18-19:23 EEST. 2 of 5 scalp attempts today have failed (12:47 ok, 15:40 ok, 19:18 FAIL, 22:09 ok, 22:47 FAIL).
- **evidence:** `data/scheduled_runs/2026-07-23_default_schedule/scheduler.log` lines ~350-351 (19:18 failure) and ~529-530 (22:47 failure); prior review's TODO-1 for the same signature.
- **suggested manual fix:** investigate concurrent writer contention on `db/crypto_ai_desk.sqlite` during the scalp report's `save_symbols` call (likely colliding with background monitors/derivatives writers); confirm WAL mode is enabled and add a short retry/backoff around `save_symbols` if not already present.
- **priority:** high (escalated — this is now a recurring, not isolated, failure pattern across the session).
- **first observed:** 2026-07-23 19:21 EEST; recurred 2026-07-23 22:51 EEST (this cycle).

### TODO-2: catalyst symbol resolver missing exchange-ops-style tickers
- **issue:** Catalyst mapping remains stuck near 79-80% unmapped across the full session today (7 consecutive scan cycles). Sampled unmapped headlines are exchange-ops notices (new-futures-listing, funding-rate-adjustment announcements) where the ticker (e.g. WOODUSDT, RIFUSDT, BNCUSDT) is present in the title text but not resolved to a symbol.
- **evidence:** `data/catalysts/2026-07-23/catalyst_events.jsonl` — 2,769/3,500 rows unmapped; sample titles unchanged from prior cycles.
- **suggested manual fix:** extend the catalyst symbol resolver's regex/entity-matching to recognize the `<TICKER>USDT` pattern common in exchange-ops announcement titles.
- **priority:** medium (persistent, degrades catalyst-backed decision quality; review already treats catalyst layer as context-only when this weak).
- **first observed:** carried forward from prior reviews (news_layer_hardening project); still unresolved as of 2026-07-23 23:29 EEST.

### TODO-3: TSLA "going_concern" legal-risk tag could not be externally corroborated
- **issue:** The stocks-intraday pipeline tags TSLA with `active legal/headline risk (going_concern)`, forcing a hard demotion to C-tier/AVOID. External search at the 21:39 cycle found capex-scrutiny/"milestones not probable" commentary but no confirmed auditor going-concern opinion for Tesla dated 2026. Not re-checked this cycle (fact unchanged; avoiding redundant external calls).
- **evidence:** `data/reports/stocks/intraday/2026-07-23_20-01_stocks_intraday_report.md` §8 (`TSLA (short) (was A): score 90 · ... tier demoted A→C: active legal/headline risk (going_concern)`); prior WebSearch (21:39 cycle) found no primary-source confirmation.
- **suggested manual fix:** a human session should trace the `going_concern` tag back to its source record and confirm the underlying evidence is current and correctly attributed to Tesla, not stale or mis-tagged.
- **priority:** medium (conservative-direction-consistent with risk_off regime, but an unverifiable legal tag undermines the legal-risk gate's general credibility).
- **first observed:** 2026-07-23 21:39 EEST; unchanged as of 23:29 EEST.

### TODO-4: XLE (energy) absent from stocks Top-Candidates and Rejected/Not-Ready for a 4th consecutive cycle
- **issue:** XLE was a clean A-raw catalyst pick (score 86.07, long, oil-shock-backed) at 16:20 EEST. It has not appeared in either §5 Top Candidates or the Rejected/Not-Ready section at 18:39, 21:39, or now 23:29 EEST, even though Sector Rotation still lists energy/XLE as "strong" (RS vs SPY now +10.12%, essentially flat from +10.89% at 21:39). This is now a persistent, reproducible 4-cycle pattern.
- **evidence:** `data/reports/stocks/intraday/2026-07-23_20-01_stocks_intraday_report.md` §2 (XLE listed strong) vs §5/§8 (no XLE row in either); same absence noted in the 18:39 and 21:39 reviews' TODOs.
- **suggested manual fix:** trace why XLE is scored/considered upstream (sector-rotation aggregation) but dropped before reaching either the Top-Candidates or Rejected/Not-Ready output stage — likely a filtering or pipeline bug specific to XLE's data path this session (a rejected/gated XLE would still appear in §8, so this looks like a real data-path drop, not a scoring judgment).
- **priority:** high (unchanged — persistent 4-cycle pattern masking a real, externally-confirmed catalyst-backed sector move the desk cannot currently act on or even see rejected).
- **first observed:** 2026-07-23 16:20 EEST; absence confirmed again at 18:39, 21:39, and 23:29 EEST.

### TODO-5: untracked legacy alert — ZAMA/USDT watchlist alert with no backing proposed_signal
- **issue:** `detect_untracked_legacy_alerts` found 1 untracked crypto alert this cycle: ZAMA/USDT B-tier intraday, score 66.3, long, sent to Telegram at 18:57 UTC, with no matching `proposed_signal` within the ±6h window. This alert will not contribute to PF/winrate/avgR tracking. This matches a previously-identified project-side bug pattern (watchlist re-fire reusing a stale/closed signal_id instead of minting a new `proposed_signal`, confirmed earlier on ALLO/USDT and BANK/USDT).
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-23` output this cycle — 1 row, ZAMA/USDT, 2026-07-23T18:57:19+00:00, trackable=NO.
- **suggested manual fix:** a human session should investigate the watchlist-alert-firing code path for ZAMA/USDT specifically around 18:57 UTC and confirm whether it's the same signal_id-reuse root cause already raised for ALLO/USDT and BANK/USDT.
- **priority:** high (matches an already-escalated project-level bug; each occurrence silently degrades tracked PF/winrate completeness).
- **first observed (this specific ZAMA occurrence):** 2026-07-23 18:57 UTC / detected this review cycle 23:29 EEST. (Underlying bug class first observed on ALLO/USDT and BANK/USDT per project history.)
