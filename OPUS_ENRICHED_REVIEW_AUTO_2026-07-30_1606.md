# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:06 EEST

## 1. Executive Summary

Slot: **pre-US-open decision review** (target 08:55 America/New_York, actual fire 08:59 ET / 16:06 EEST, Δ+4min — within tolerance; see DST note in §3). **Advisory only — no auto-trade, no scoring/threshold/strategy changes.** External web research was available and used this run. The single most decision-relevant finding: two of the six pre-US-eligible stocks candidates carry a **raw score contradicted by real premarket price action** — **AMD** (pre-gate A, score 86, short) is trading **+3.2% premarket** on fresh bullish sell-side price-target raises (UBS $730 on 7/24, Mizuho/Wedbush 7/27) ahead of its Aug-4 print, and **AVGO** (pre-gate A, score 95.6, short) is up a mild +0.6% on a fresh Buy rating (7/28) and its $200B Samsung AI deal — both are the opposite of what their internal short scores imply. The Pre-US Stocks Review Overlay (§5) ran on all 6 eligible candidates and issued a short-TTL **BLOCK** veto on AMD (expires ~20:05 EEST) and **CAUTION** on AVGO and XOM (XOM long is also contradicted: Brent crude fell sharply this weekend on US-Iran de-escalation, pulling XOM down ~3% premarket, and XOM reports Q2 earnings tomorrow 7/31). **No candidate cleared the SUPPORT bar this cycle** — nothing is promoted out of the `market_closed_intraday_planning_only` cap. Crypto: only **DEXE/USDT** intraday short (B-tier) is genuinely open (TP1 hit, funding deeply negative on both Bybit/MEXC — a squeeze-risk caveat, manage don't add). Macro backdrop is genuinely mixed, not clean risk-off: the internal geopolitical feed still surfaces "active strike" headlines dated today, but externally-verified reporting shows US-Iran strikes have been **paused since ~7/24-27** with diplomacy ongoing — though the Strait of Hormuz **remains closed** to normal traffic, so the macro risk is real but not escalating as the raw internal headline implies (flagged as TODO-6). Catalyst mapping is weak again (71.6% unmapped). Earnings-blackout names today: AAPL, AMZN, COIN, MA, MSTR — do not chase. Scanning, tracking, and monitors continue in every mood; this review recommends selective caution and RTH confirmation, never a stop.

## 2. Data Used

| File / Source | mtime (local) | Age |
|---|---|---|
| `data/reports/scalp/2026-07-30_12-01_scalp_report.md` | 15:01:57 EEST | ~1h04m |
| `data/reports/intraday/2026-07-30_12-08_intraday_report.md` | 15:08:49 EEST | ~0h57m |
| `data/reports/swing/2026-07-30_01-36_swing_report.md` | 04:36:13 EEST | ~11h23m — **carry-forward** (4-12h bucket) |
| `data/reports/stocks/intraday/2026-07-30_12-31_stocks_intraday_report.md` | 15:31:35 EEST | ~0h28m |
| `data/reports/stocks/swing/…` / `invest/…` (2026-07-02) | deprecated/removed playbooks — see [[project_crypto_ai_desk_stocks_position_framework]], not a freshness failure |
| `data/catalysts/2026-07-30/catalyst_events.jsonl` (2500 rows, re-counted live) + `narrative_baskets.jsonl` | 15:13 EEST | ~0h46m |
| `reports/PAPER_MONITOR_STATUS_LATEST.md` | 12:50:28 EEST | ~3h09m — used with a freshness caveat, cross-checked against live `active-signals` |
| `python -m src.cli active-signals --asset-class crypto` / `stocks` | live query | now |
| `python -m src.cli signal-stats --asset-class crypto` / `stocks` | live query | now |
| `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-30` | live query | now — none found |
| `python -m src.cli stocks-preus-candidates` → `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md` | live | now — 6 eligible, 18 excluded |
| `python -m src.cli stocks-preus-review-ingest --json data/raw/enriched_review_sources/preus_review_2026-07-30T1304Z.json` | live | now — 6 candidates scored |
| Prior review `OPUS_ENRICHED_REVIEW_AUTO_2026-07-30_1145.md` | 11:45 EEST | for §4 diff |
| WebSearch: NFLX/XOM/JPM/AMD/AVGO/IWM premarket + catalysts, US-Iran ceasefire/Strait of Hormuz status, Jamie Dimon market warnings | live | now |

**External web research was available and used this run.**

## 3. Scheduler / Data Freshness

- **Pre-US schedule check: target 08:55 ET, actual fire 08:59 ET (Δ+4min, within tolerance).**
- `data/scheduled_runs/2026-07-30_default_schedule/scheduler.log` mtime 15:57:13 EEST (~2min old) — fresh. Latest `cycle_08_12-10_summary.md` mtime 12:52:30 EEST (~3h07m old) — not deferred since scheduler.log alone is fresh (defer rule requires BOTH stale).
- Crypto scalp/intraday reports fresh (~1h). Crypto swing report ~11h23m old — carry-forward bucket, used with a freshness flag.
- Stocks-intraday report fresh (~28min). US cash session is **closed** pre-open; every stocks candidate this cycle is correctly gated `market_closed_intraday_planning_only`.
- Catalyst JSONL re-counted live this run: **2500** unique events today, **709 mapped (28.4%)**, **1791 unmapped (71.6%)** — weak-mapping threshold breached again (see §5, TODO-5 recurring).
- `detect_untracked_legacy_alerts --since 2026-07-30`: **None** — every legacy crypto alert has a backing proposed_signal.
- `reports/PAPER_MONITOR_STATUS_LATEST.md` (12:50 EEST, ~3h09m old): OPEN_ACTIVE=1, WAITING_FOR_ENTRY=0, ENTERED_UNRESOLVED_EXPIRED=1, REVIEW_ONLY_SHADOW=39, NO_ENTRY_EXPIRED=53, CLOSED_WIN=145, CLOSED_LOSS=13, CLOSED_FLAT=12, UNKNOWN_INCONSISTENT=5. Cross-checked against the live `active-signals` query — consistent (DEXE/USDT is the one open crypto position, now showing `tp1_hit`, i.e. TP1 touched, still tracking toward TP2/TP3 or stop).
- **Recurring lifecycle-mapping anomaly, still present, unchanged from the 11:45 EEST review**: UNKNOWN_INCONSISTENT bucket (5 items) — **AAPL, GOOGL, XOM** (stocks/intraday/B) with unmapped status `'tp2_hit'`, and **MSTR, PLTR** (stocks/intraday/C) with "labelled loss but final_r>0 — inconsistent". Same symbols, same pattern as the last review — not yet fixed (see §14 TODO-3/TODO-4).
- **New this cycle**: ran the Pre-US Stocks Review Overlay (§A of the DST-note task spec) — `stocks-preus-candidates` found 6 eligible / 18 excluded; all 6 were reviewed and ingested via `stocks-preus-review-ingest` (see §5 for the compact block, full detail in §7).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-30 16:06 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.82,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["stocks swing/invest reports deprecated, ~28d stale, not used as fresh"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log 15:57 EEST (~2min)", "cycle_08_12-10_summary.md 12:52 EEST (~3h07m, not both-stale)", "scalp/intraday ~1h fresh, swing ~11h23m carry-forward", "stocks-intraday ~28min fresh, market closed", "catalyst JSONL live-recounted: 2500 rows, 709 mapped/1791 unmapped", "detect_untracked_legacy_alerts: none"] },
    { "agent": "market_regime", "verdict": "mixed", "confidence": 0.55,
      "reason_codes": ["mixed", "chop", "wait_for_trigger"],
      "data_missing": ["no fresh RTH stock price action yet — cash session closed"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Internal crypto regime: 'transition (mixed)', BTC transition_up, ETH uptrend, altcoin breadth only 27.5% above EMA20", "Internal stocks regime: risk_off, bias short, VIX 18.97, breadth 0% above EMA20, SPY/QQQ/IWM downtrending 5d/20d", "External: US-Iran strikes paused since ~7/24-27, oil crashed >8-11% on de-escalation (bullish-for-risk), but Strait of Hormuz remains closed to normal traffic (bearish/uncertain) — a genuinely mixed macro signal, not clean risk-off", "Internal geopolitical headline feed still shows 'active strike today' language that appears stale/contradicted by external verification (TODO-6)"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "catalyst_contradicted", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl: 2500 rows, 709 mapped (28.4%), 1791 unmapped (71.6%) — weak-mapping threshold breached", "AMD short candidate contradicted by fresh bullish analyst price-target raises (UBS 7/24, Mizuho/Wedbush 7/27)", "AVGO short candidate contradicted by fresh Buy rating (7/28) + known $200B Samsung AI deal", "XOM long candidate contradicted by today's oil-crash premarket move on Iran de-escalation", "binance_ecosystem_teaser narrative basket fresh <1h, primary BNB/USDT — only fresh catalyst-backed crypto idea this cycle, but score (32.3) too low to be actionable"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["squeeze_risk", "funding_extreme"],
      "data_missing": ["OI change unavailable ('n/a') for most symbols this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["DEXE/USDT (open short): funding -0.001484 (MEXC fallback), -0.00742598 (Bybit cross-check) — deeply negative on both external venues, crowding 'elevated' — real squeeze-risk caveat against the open position, manage don't add"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "entry_late", "price_moved_away", "overextended"],
      "data_missing": ["TradingView / manual chart check unavailable this run"],
      "suggested_effect": "advisory_only",
      "facts_used": ["AMD/AVGO: shorting into premarket strength would be chase risk against the tape", "NFLX: earnings reaction is 14 days old (stale), stock already recovered +3.61% on 7/28 with no new driver — late entry either direction", "JPM: already down -3.25% on 7/29 plus further premarket weakness — a fresh short entry here is chasing an existing move, not a new signal", "IWM: Russell 2000 futures seen modestly up in one reference point, contradicting the short-biased internal score"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.8,
      "reason_codes": ["open_actionable", "no_entry", "review_shadow", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Open actionable = 1: DEXE/USDT intraday short, TP1 hit, tracking TP2/TP3 or stop", "Waiting for entry = 0", "Entered unresolved (expired-after-entry) = 1", "Review/Shadow = 39, No-entry/stale/moved-away = 53", "Closed = 145 win / 13 loss / 12 flat", "Needs review (inconsistent) = 5: AAPL/GOOGL/XOM unmapped 'tp2_hit', MSTR/PLTR 'labelled loss but final_r>0' — unchanged from prior review, still open (TODO-3/TODO-4)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.68,
      "reason_codes": ["headline_risk", "reduce_risk", "manual_review"],
      "data_missing": ["cannot re-confirm the PLTR sec_doj / META indictment flags beyond the prior review's research pass"],
      "suggested_effect": "advisory_only",
      "facts_used": ["AAPL, AMZN, COIN, MA, MSTR report earnings today (2026-07-30) — do_not_chase_warning active on all five", "XOM reports Q2 earnings tomorrow (2026-07-31) — block_requires_operator_review, additional reason to demote the XOM long idea beyond the oil-crash contradiction", "META still shows legal_headline_risk 'indictment' (C-tier) — prior review found this is actually civil litigation, mislabeled (TODO-2, still open)", "PLTR still shows legal_headline_risk 'sec_doj' (C-tier) — prior review found no corroborating 2026 DOJ/SEC investigation, likely law-firm-solicitation boilerplate (TODO-1, still open)", "AMD short candidate BLOCKED this cycle via the Pre-US Stocks Review Overlay — fresh premarket strength + analyst upgrades directly contradict the short thesis"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto B-tier weekly headline: n=79, winrate 26.3%, PF 1.99, avgR +0.319, totalR +16.9 — healthy despite low winrate", "Stocks A/B headline: n=2 anecdotal, PF 0.0 — not enough sample to trust", "Stocks C-tier watchlist: n=185, winrate 5.7%, PF 0.20 — badly losing, consistent with C-tier being correctly non-actionable by design", "Stocks intraday post-trade diagnostics (14d): forward_postfreeze n=252, ΣR=-55.20 — the only bucket usable as evidence, and it's negative; top avoidable loss bucket is 'no_gate_context' (-410R over 736, but mostly backfill_pretrained, hypothesis-only)"] },
    { "agent": "head_trader", "verdict": "advisory_only",
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of the eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "watch_only",
    "confidence": 0.6,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "none clean — watch NFLX", "trigger": "RTH open + reclaim/hold above premarket VWAP ~73.9-74.5 with volume; no fresh catalyst, earnings 14 days stale, low conviction", "reason": "only long-side candidate with a stable (not falling) premarket tape, but nothing fresh backs it" },
    "best_short_candidate":    { "symbol": "JPM", "trigger": "wait for RTH open + a clean retest/break of the premarket low with volume — do not chase the already-realized -3.25% (7/29) + further premarket weakness", "reason": "macro-aligned (Dimon's market-risk caution, stocks risk_off regime) but no entity-specific fresh catalyst; chase risk if entered now" },
    "best_catalyst_candidate": { "symbol": "BNB/USDT", "trigger": "confirm fresh catalyst + RS not contradicting + entry structure on 15m-1h; current score 32.3 well below actionable threshold, needs real breakout confirmation first", "reason": "binance_ecosystem_teaser narrative basket, fresh <1h, BNB is the stated primary — the only fresh catalyst-backed idea surfaced this cycle" },
    "avoid_candidate":         { "symbol": "AMD (short)", "reason": "Pre-US Stocks Review Overlay issued a short-TTL BLOCK (expires ~20:05 EEST): fresh bullish analyst price-target raises + +3.2% premarket strength directly contradict the raw A-tier short score; also avoid chasing AAPL/AMZN/COIN/MA/MSTR into today's earnings prints" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 7
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.82 | scheduler_fresh, report_stale | advisory_only |
| market_regime | mixed | 0.55 | mixed, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, catalyst_contradicted, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.60 | squeeze_risk, funding_extreme | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, entry_late, price_moved_away, overextended | advisory_only |
| execution_lifecycle | needs_review | 0.80 | open_actionable, no_entry, review_shadow, needs_review | advisory_only |
| risk_manager | caution | 0.68 | headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader (synthesis) | watch_only | 0.60 | — | advisory_only |

## 4. What Changed vs Previous Review (11:45 EEST)

- **Resolved / unchanged**: The UNKNOWN_INCONSISTENT lifecycle bug (AAPL/GOOGL/XOM unmapped `tp2_hit`, MSTR/PLTR "loss but final_r>0") is **still present, unchanged** — same 5 symbols as the 11:45 review. Not yet fixed (TODO-3/TODO-4 remain open).
- **New this cycle**: Ran the Pre-US Stocks Review Overlay for the first time this slot — 6 eligible candidates reviewed and ingested (NFLX, XOM, JPM, AMD, AVGO, IWM). Result: 0 SUPPORT, 3 NEUTRAL, 2 CAUTION (XOM, AVGO), 1 BLOCK (AMD), 1 INSUFFICIENT_DATA (IWM) — **nothing promoted out of the market-closed cap**.
- **New finding**: AMD and AVGO short candidates (both pre-gate A-tier, scores 86/95.6) are directly contradicted by fresh premarket price action and analyst upgrades — this was not visible in the 11:45 review, which only flagged the broad short cluster as "pending RTH confirmation," not specifically contradicted.
- **New finding**: XOM long candidate is contradicted by a fresh oil-crash premarket move tied to US-Iran de-escalation, plus proximity to tomorrow's (7/31) earnings.
- **Thesis unchanged**: DEXE/USDT remains the sole genuinely open crypto position (now TP1 hit, was touch_r=0.0 at 11:45). META and PLTR legal-flag TODOs (TODO-1, TODO-2) remain open, unresolved since the 11:45 review.
- **Catalyst mapping**: weak in both reviews (67.3% unmapped at 11:45, 71.6% now) — persistent, worsening slightly (TODO-5).
- **Macro**: the internal geopolitical headline feed still surfaces "active strike today" language; external verification this cycle confirms strikes have been paused since ~7/24-27 (new finding this cycle, not covered at 11:45) — flagged as a new TODO-6.

## 5. Catalyst Coverage

- Total `catalyst_events` today: **2500**. Mapped (non-null symbol): **709 (28.4%)**. Unmapped: **1791 (71.6%)**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Narrative baskets today: `binance_ecosystem_teaser` (playbook `related_beta_rotation`, fresh <1h, primary BNB/USDT, related ASTER/USDT), plus `perps_dex_narrative` (HYPE), `rwa_narrative` (ONDO/XLM), `ai_narrative` (NEAR/RENDER/TAO/FET) from the freshest intraday report.
- Top 3 unmapped headlines (illustrative, not tradable as-is):
  1. "California Water Service Group Reports Strong Second Quarter 2026 Financial Results"
  2. "$250,000,000 USDC minted at USDC Treasury Details" (Telegram whale-alert style post, no resolvable symbol)
  3. "Grayscale parent Digital Currency Group wrote to Senate leaders urging a CLARITY Act floor vote before the August recess"

### Pre-US Stocks Review Overlay
- candidates reviewed: 6 (SUPPORT 0 / NEUTRAL 3 / CAUTION 2 / BLOCK 1 / INSUFFICIENT_DATA 1)
- session-cap-only C's now eligible for pre-open Paper lane: 0
- excluded by hard gate: 18 — LEGAL_RISK (GOOGL×2, COIN, AMZN, PLTR, META), EARNINGS_BLACKOUT (COIN, UNH, MSTR, TSLA, SPY, NVDA), NO_ENTITY_RESOLVED_CATALYST (XLE, XLV, SMH, SMCI, XLK, DIA, QQQ)
- Enforced results (ingest output, not requested): NFLX NEUTRAL adj 0.0 (tier B, score 65.25 unchanged) · XOM CAUTION adj -6.0 (score 67.96→61.96, tier B→C) · JPM NEUTRAL adj 0.0 (tier A, score 85.6 unchanged) · AMD **BLOCK** (short-TTL veto, expires 2026-07-30T17:05:39Z / ~20:06 EEST, score 85.99 unchanged) · AVGO CAUTION adj -4.0 (score 95.58→91.58, still tier A) · IWM INSUFFICIENT_DATA adj 0.0 (tier A, score 95.76 unchanged)

## 6. Market Landscape

The picture this cycle is genuinely mixed, not clean risk-off, and the pre-US stocks overlay surfaced a real gap between the desk's internal scoring and the live tape: two high-scored short candidates (AMD, AVGO) are moving the *wrong way* premarket on fresh bullish news, and the one long candidate premised on an oil tailwind (XOM) is being undercut by a real oil-price crash tied to US-Iran de-escalation. Crypto stays selective — BTC in a `transition_up` state, ETH uptrend, but altcoin breadth still weak (27.5% above EMA20), no A-tier setups, and the one open position (DEXE short) carries a funding-driven squeeze-risk caveat. The macro narrative itself needs a caveat: the internal geopolitics feed is still surfacing "active strike" headlines dated today, but externally-verified reporting shows the shooting stopped ~5-6 days ago while diplomacy continues — the Strait of Hormuz remains closed, so the risk is real but the internal feed may be over-stating the acute/escalating nature of it (TODO-6).

### Market Mood / Risk Routing
- Crypto mood: **mixed / transition** (BTC transition_up, ETH uptrend, but altcoin breadth only 27.5% above EMA20; macro geopolitical risk elevated but de-escalating per external verification)
- Stocks mood: **pre-market, mixed** (internal regime label risk_off/short-biased, but real premarket price action on two of the six reviewed candidates contradicts the short bias; cash session closed)
- Dominant narrative: US-Iran strikes paused (~7/24-27) but Strait of Hormuz still closed — oil crashed on the de-escalation headline, undercutting the "sustained oil tailwind" thesis behind XOM long; separately, fresh sell-side analyst upgrades on AMD/AVGO ahead of upcoming earnings are contradicting the desk's short bias on both names
- Preferred side now: **wait-for-trigger / RTH-confirmation** — no side is clean pre-open; crypto stays selective (manage DEXE short, don't add)
- Best long candidate: none clean — watch NFLX for a hold above the premarket VWAP zone (~73.9-74.5) at the open, no fresh catalyst though
- Best short candidate: JPM watch — wait for a retest/break of the premarket low with volume, do not chase the already-realized drop
- Best catalyst-backed candidate: BNB/USDT (binance_ecosystem_teaser basket, fresh <1h) — needs real breakout confirmation, current score (32.3) far below actionable
- What to avoid: **AMD short** (BLOCKED this cycle — premarket strength + analyst upgrades contradict the setup); do not chase AAPL/AMZN/COIN/MA/MSTR into today's earnings; do not treat AVGO short or XOM long as clean given the CAUTION findings
- What would change the view: a clean RTH open/retest confirming either side in stocks; a genuine re-escalation or full resolution of the Iran/Hormuz situation; a fresh, symbol-specific bearish catalyst restoring the AMD/AVGO short theses; human confirmation or clearing of the META/PLTR legal flags (TODO-1/TODO-2, still open)

## 7. Candidate Deep Dives

### 1. AMD — stocks intraday, pre-gate A (score 85.99), short — **BLOCKED this cycle**
- Internal setup: short, score 86, `market_closed_intraday_planning_only` demote to C (correct, cash session closed).
- External verification: AMD trading **+3.2% premarket** today; UBS raised its price target to $730 (7/24), Mizuho and Wedbush both raised targets (7/27), ahead of the Aug-4 earnings print. This is a fresh (≤6 days), material, entity-resolved catalyst the code's candidate-selection gate could not see.
- Has price already reacted? Yes — premarket strength already visible.
- Chasing? A short here would be chasing against fresh bullish flow.
- Is this aligned with mood? No — contradicts the stocks-wide short bias for this specific name.
- Actionable now or pending confirmation? **Neither** — vetoed (BLOCK, short-TTL, expires ~20:06 EEST). Needs a fresh re-check before any consideration.
- Catalyst confirmation/contradiction? **Contradicted.**
- Verdict fed to `stocks-preus-review-ingest`: BLOCK, adjustment 0 (veto, not a score change), enforced.

### 2. XOM — stocks intraday, pre-gate B (score 67.96), long — **CAUTION**
- Internal setup: long, `market_closed_intraday_planning_only` demote to C.
- External verification: XOM slid ~3% premarket today as Brent crude fell sharply on the confirmed US-Iran de-escalation over the weekend — this directly undercuts an oil-tailwind long thesis. XOM also reports Q2 2026 earnings **tomorrow (2026-07-31)** — already flagged internally as `block_requires_operator_review` / `do_not_chase_warning`.
- Has price already reacted? Yes, negatively, to the de-escalation.
- Would entry now be late/wrong-sided? A long here would be entering against the fresh catalyst.
- Catalyst confirmation/contradiction? **Contradicted**, plus earnings-proximity risk.
- Verdict fed to ingest: CAUTION, requested -6 → enforced adjustment -6.0 (score 67.96→61.96, tier demoted B→C on the underlying score, on top of the existing market-closed cap).

### 3. AVGO — stocks intraday, pre-gate A (score 95.58), short — **CAUTION**
- Internal setup: short, `market_closed_intraday_planning_only` demote to C.
- External verification: AVGO up a mild +0.6% premarket; fresh Buy rating issued 7/28, reinforced by the widely-reported $200B AI agreement with Samsung. Move is modest (not a full BLOCK), but the qualitative catalyst backdrop is bullish, contradicting the short.
- Catalyst confirmation/contradiction? **Contradicted** (mild).
- Verdict fed to ingest: CAUTION, requested -4 → enforced adjustment -4.0 (score 95.58→91.58, still tier A on the underlying score, market-closed cap still applies).

### 4. DEXE/USDT — crypto intraday, B-tier short — **OPEN, TP1 hit** (manage, not a new entry)
- Entry filled 2.629 zone (opened 04:48 UTC per prior reviews); TP1 has since been touched (`tp1_hit` per live active-signals query, up from `touch_r=0.0` at 11:45 EEST). Stop/invalidation 2.72951.
- Funding deeply negative on both Bybit (-0.00742598) and MEXC (-0.001484 fallback), crowding "elevated" — real squeeze-risk caveat against this exact position.
- Aligned with mood? Yes, directionally (crypto stays selective-bearish), but manage the existing position, don't add.
- Catalyst confirmation/contradiction? None either way — pure technical breakdown, `crypto_intraday_catalyst_or_momentum` playbook.

### 5. BNB/USDT — crypto, C-tier watchlist, catalyst-backed — best catalyst-watch, not actionable yet
- Score 32.3 (long), well below the actionable threshold — "Converted to watchlist only: wait for pullback" per the scalp report; also carries a `delisting`-type risk event (unrelated spot-pair removal notice, not BNB itself) requiring caution.
- Narrative: `binance_ecosystem_teaser` basket, fresh **<1h**, BNB/USDT stated as primary; related ASTER/USDT.
- Has price already reacted? Yes — BNB already +3.16-2.7% 24h with 3.6x unusual volume, "overextended" tag present.
- Chasing? Yes at current levels; "Price is more than 2 ATR from EMA20; do not chase" per the source report.
- Actionable now or pending confirmation? Pending — needs a pullback/consolidation entry with fresh catalyst confirmation, not a chase at current extension.

## 8. Best Candidates Ranked

1. **DEXE/USDT short** — already open, TP1 hit, manage risk, do not add (squeeze-risk caveat).
2. **JPM short-watch** — best short-watch in stocks, wait for RTH retest/break of premarket low, do not chase the already-realized move.
3. **NFLX long-watch** — best long-watch (weakly), needs a hold above premarket VWAP at the open, no fresh catalyst backing it.
4. **BNB/USDT catalyst-watch** — fresh <1h narrative basket, needs a non-chase pullback entry before it's tradable.
5. **AMD short — BLOCKED, explicitly not ranked as tradable this cycle.**

## 9. Avoid / No Trade (this decision window only)

- **AMD short**: BLOCKED via the Pre-US Stocks Review Overlay — fresh premarket strength + analyst upgrades contradict the setup. Short-TTL veto expires ~20:06 EEST; re-check before considering.
- **AVGO short, XOM long**: CAUTION — both contradicted by fresh external evidence (see §7); do not treat as clean even once RTH confirms unless the contradiction resolves.
- **AAPL, AMZN, COIN, MA, MSTR**: earnings today — `do_not_chase_warning` active on all five.
- **META, PLTR**: still carrying unresolved internal legal-risk flags (TODO-1/TODO-2 from the prior review, still open) — treat as manual-review, not confirmed avoid, but also not a clean actionable.
- **Crypto scalp mode**: correctly disabled desk-wide (kill-switch), not a per-symbol avoid.
- This is a decision-window call only — scanning, tracking, and monitors continue in every mood; nothing here is a stop-the-system instruction.

## 10. Main Risks

- **Internal-vs-external macro contradiction**: the geopolitics headline feed is still surfacing "active strike today" language while externally-verified reporting shows the exchange of strikes paused ~5-6 days ago — treat the internal macro risk score (100/100) as somewhat stale/overstated pending a refresh (TODO-6). The Strait of Hormuz genuinely remains closed, so this is not a clean all-clear either.
- **Score-vs-tape contradiction risk on stocks shorts**: AMD and AVGO both show high internal short scores contradicted by real premarket strength — a reminder that pre-open technical scores can lag same-week analyst/catalyst developments; this is exactly what the Pre-US Stocks Review Overlay exists to catch, and it did catch it this cycle, but only for the 6 candidates the code surfaced as eligible.
- Squeeze risk on the one open crypto position (DEXE short) given deeply negative funding on both external venues.
- Data-quality risk: the recurring `UNKNOWN_INCONSISTENT` lifecycle-mapping bug (unmapped `tp2_hit`, "labelled loss but final_r>0") persists unchanged across at least 3 consecutive reviews now (TODO-3/TODO-4) — always cross-check against live `active-signals` / `paper_execution_outcomes` directly.
- Legal-flag reliability risk: META and PLTR legal_headline_risk flags remain unresolved/unverified since the 11:45 EEST review (TODO-1/TODO-2).
- Earnings-proximity risk stacks with the XOM oil-contradiction finding — avoid treating XOM long as clean at any point before its 7/31 print.

## 11. Action Plan — next 4 hours

- Hold DEXE/USDT short as-is (TP1 hit); do not add given the funding-driven squeeze-risk caveat; manage to stop 2.72951 or the remaining TP ladder.
- Do not treat AMD as a short candidate this cycle — BLOCKED, re-check after ~20:06 EEST or once RTH price action is available.
- Do not enter AVGO short or XOM long even after RTH open without first re-verifying the contradicting catalysts have resolved.
- Watch JPM for a clean retest/break of its premarket low at the open before considering a short; watch NFLX for a hold above premarket VWAP before considering a long — neither is a chase-now idea.
- Watch BNB/USDT for a non-extended pullback entry if the `binance_ecosystem_teaser` narrative stays fresh.
- Do not chase AAPL, AMZN, COIN, MA, MSTR into today's earnings prints.
- Continue monitoring the Iran/Strait-of-Hormuz situation for either a genuine re-escalation or a full reopening — both would materially change the stocks/crypto macro read.

## 12. Final Verdict per Mode

- **Crypto scalp**: disabled (kill-switch), no change.
- **Crypto intraday**: 1 open position (DEXE short, TP1 hit), manage only; no new entries scored high enough this cycle.
- **Crypto swing**: no fresh actionable ideas this cycle; BNB/USDT catalyst-watch only, not yet tradable.
- **Stocks intraday**: planning-only until RTH confirms; of the 6 pre-US-reviewed candidates, 0 cleared to SUPPORT — AMD blocked, XOM/AVGO cautioned, NFLX/JPM/IWM neutral-to-insufficient.
- **Stocks swing/invest**: deprecated/removed frameworks, no active signals this run (see [[project_crypto_ai_desk_stocks_position_framework]]).

## 13. Sources

- [NFLX Premarket VWAP Netflix (MarketChameleon)](https://marketchameleon.com/Overview/NFLX/Stock-Price-Action/Premarket-VWAP)
- [Netflix, Inc. (NFLX) Is Sinking After Earnings — Should You Buy the Dip? (Yahoo Finance)](https://finance.yahoo.com/markets/stocks/articles/netflix-inc-nflx-sinking-earnings-213227168.html)
- [Why Is Exxon Mobil Stock Gaining/Sliding — pre-open oil-crash coverage (Benzinga)](https://www.benzinga.com/markets/large-cap/26/07/60603102/why-is-exxon-mobil-stock-gaining-wednesday)
- [Exxon Mobil Corp Stock (XOM) Moved Up by 3.24% on Jul 29 — context (TradingKey)](https://www.tradingkey.com/news/market-movers/262061774-market-movers-xom-20260729)
- [JPMorgan Chase & Co Stock (JPM) Closed Down by 3.25% on Jul 29 (TradingKey)](https://www.tradingkey.com/news/market-movers/262062324-market-movers-jpm-20260729)
- [In 12 Words, JPMorgan CEO Jamie Dimon Just Issued a Stark Warning to Investors (The Motley Fool, 7/30)](https://www.fool.com/investing/2026/07/30/in-12-words-jpmorgan-ceo-jamie-dimon-just-issued-a/)
- [What's Going on With AMD Stock — premarket + analyst target raises (Benzinga)](https://www.benzinga.com/markets/tech/26/07/60692400/whats-going-on-with-amd-stock-monday-8)
- [AMD Stock Is Gaining Wednesday: What's Going On? (Benzinga)](https://www.benzinga.com/markets/tech/26/07/60752479/amd-stock-is-gaining-wednesday-whats-going-on)
- [Broadcom (AVGO) Stock Forecast: Analyst Ratings, Predictions & Price Target (public.com)](https://public.com/stocks/avgo/forecast-price-target)
- [IWM Premarket VWAP iShares Russell 2000 ETF (MarketChameleon)](https://marketchameleon.com/Overview/IWM/Stock-Price-Action/Premarket-VWAP)
- [July 27, 2026 — US pauses new strikes, Iran says no current negotiations with the US (CNN)](https://www.cnn.com/2026/07/27/world/live-news/iran-war-trump)
- [Why has the US halted its bombing of Iran? (Al Jazeera)](https://www.aljazeera.com/news/2026/7/27/why-has-the-us-halted-its-bombing-of-iran)
- [U.S. pauses attacks on Iran for a second straight day and Tehran does too (NPR)](https://www.npr.org/2026/07/26/g-s1-135593/us-pauses-attacks-iran-second-day-tehran)
- [U.S. and Iran pause fighting, Trump dismisses concerns of dwindling stockpiles (CNBC)](https://www.cnbc.com/2026/07/27/us-iran-war-trump-hormuz.html)
- Internal: `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md` (generated 2026-07-30T13:01:54Z) — 6 eligible / 18 excluded, cap_reasons per candidate.
- Internal: `data/raw/enriched_review_sources/preus_review_2026-07-30T1304Z.json` — the 6 verdict objects ingested this run.

## 14. Fix Requests / TODO

### TODO-1: PLTR `legal_headline_risk: sec_doj` flag looks like a false positive from law-firm solicitation boilerplate
- **issue:** Still open, unresolved since the 11:45 EEST review. PLTR remains demoted A→C citing "active legal/headline risk (sec_doj)" this cycle too (visible in the current `data/reports/stocks/intraday/2026-07-30_12-31_stocks_intraday_report.md` §7 C-tier table).
- **evidence:** Prior WebSearch found only ~9-month-old (Oct 2025) shareholder-solicitation boilerplate, structurally identical to boilerplate seen for other volatile stocks; not re-verified this cycle (no new evidence either way).
- **suggested manual fix:** Audit the `legal_headline_risk` / `sec_doj` classifier's source data for PLTR; consider down-weighting generic shareholder-solicitation press-release boilerplate.
- **priority:** high
- **first observed:** 2026-07-30 11:45 EEST; still open 2026-07-30 16:06 EEST.

### TODO-2: META `legal_headline_risk` mislabeled as "indictment"
- **issue:** Still open, unresolved. META remains demoted A→C citing "active legal/headline risk (indictment)" this cycle too. Prior review confirmed the actual exposure is civil litigation (child-safety verdicts / trial), not a criminal indictment.
- **evidence:** Prior WebSearch (see 11:45 EEST review §13); not re-verified this cycle.
- **suggested manual fix:** Correct the legal-risk taxonomy/label for META from "indictment" to "civil_litigation" or similar.
- **priority:** medium
- **first observed:** 2026-07-30 11:45 EEST; still open 2026-07-30 16:06 EEST.

### TODO-3: Recurring `UNKNOWN_INCONSISTENT` lifecycle mapping — unmapped status `'tp2_hit'`
- **issue:** AAPL, GOOGL, XOM (stocks/intraday/B) still show "unmapped status 'tp2_hit'" in `PAPER_MONITOR_STATUS_LATEST.md` this cycle — same symbols as the 11:45 EEST review, no change. This is now confirmed persistent across at least 3 consecutive review cycles (04:47, 11:45, this one).
- **evidence:** `reports/PAPER_MONITOR_STATUS_LATEST.md` (12:50 EEST), AAPL/GOOGL/XOM lines under UNKNOWN_INCONSISTENT.
- **suggested manual fix:** Fix the lifecycle-state mapping for legacy-touch signals with raw status `tp2_hit` in the stocks/intraday/B path so it resolves to a proper CLOSED_WIN/OPEN state.
- **priority:** high
- **first observed:** 2026-07-29 (per 04:47 review); reappeared 11:45 and again 16:06 EEST 2026-07-30 on the same symbols — escalating priority given persistence.

### TODO-4: Separate lifecycle inconsistency — "labelled loss but final_r>0"
- **issue:** MSTR and PLTR (stocks/intraday/C) still show "labelled loss but final_r>0 — inconsistent" this cycle — unchanged from 11:45 EEST.
- **evidence:** `reports/PAPER_MONITOR_STATUS_LATEST.md` (12:50 EEST), MSTR and PLTR lines.
- **suggested manual fix:** Audit the loss-labelling logic for legacy-touch signals where `final_r` is computed as positive but the status field still says "loss".
- **priority:** medium
- **first observed:** 2026-07-30 11:45 EEST; still open.

### TODO-5: Catalyst mapping weak again this run (71.6% unmapped, worse than last cycle's 67.3%)
- **issue:** 1791 of 2500 catalyst events today have no resolved symbol — above the 50% weak-mapping threshold and slightly worse than the 11:45 EEST review (67.3%).
- **evidence:** live count of `data/catalysts/2026-07-30/catalyst_events.jsonl` this run: 709 mapped / 1791 unmapped.
- **suggested manual fix:** Continue widening/improving the symbol resolver in the catalyst layer per [[project_crypto_ai_desk_catalyst_linkage]].
- **priority:** low (known, deferred, not a new regression, but trend is worsening not improving — consider raising if it doesn't stabilize)
- **first observed:** recurring; re-confirmed 2026-07-30 16:06 EEST.

### TODO-6: Internal geopolitical headline feed appears to lag/contradict the actual US-Iran conflict status
- **issue:** The crypto scalp/intraday reports' "Macro, Geopolitics, Crowd" section surfaces headlines phrased as an active, ongoing strike today ("U.S. military strike on Ahvaz today damaged two student housing complexes", "Iran Relies on speedboats to keep Strait of Hormuz closed") that read as escalatory. External WebSearch this cycle confirms the exchange of strikes has actually been **paused since ~2026-07-24 to 07-27**, with diplomatic talks ongoing — though the Strait of Hormuz genuinely remains closed to normal shipping traffic, so the headline about Hormuz specifically is not wrong, but the "strike today" framing may be stale or miscategorized, and it is feeding a macro-risk score of 100/100 that may be overstating acute escalation risk right now.
- **evidence:** `data/reports/scalp/2026-07-30_12-01_scalp_report.md` §4 "Macro headline: Al jazeera quoted the governor of iran's khuzestan province saying a U.S. military strike on ahvaz today damaged two student housing complexes"; WebSearch "US Iran ceasefire strikes pause Strait of Hormuz July 30 2026" (see §13) confirming a pause since ~7/24-27 with continued diplomacy.
- **suggested manual fix:** Audit whether the macro/geopolitics headline ingestion is picking up date-stamped-as-today articles that are actually republished/aggregator copies of older strike coverage, or whether there has been a genuine flare-up not yet reflected in mainstream Western reporting; either way, the macro risk score computation may benefit from a recency/de-duplication check on this specific event stream.
- **priority:** medium
- **first observed:** 2026-07-30 16:06 EEST.

### TODO-7: Consider a lightweight premarket-price-check gate for A-tier stocks candidates that get demoted to `market_closed_intraday_planning_only`
- **issue:** This cycle's Pre-US Stocks Review Overlay manually caught two pre-gate A-tier short candidates (AMD, AVGO) whose fresh premarket price action and analyst-upgrade catalysts directly contradicted their internal short scores. This is exactly the overlay's job and it worked as designed, but it depends on an LLM review catching it each cycle rather than a deterministic check.
- **evidence:** §7 deep dives #1 (AMD) and #3 (AVGO) this review; both raw-A short scores, both moving against the score premarket on fresh, findable news.
- **suggested manual fix:** Consider whether a cheap, deterministic premarket-quote-vs-score-direction sanity check (not a new scoring input, just a display/advisory flag) could pre-flag this class of contradiction for every `market_closed_intraday_planning_only` candidate, not just the 6 the current eligibility filter surfaces, reducing reliance on the LLM overlay catching it manually every time.
- **priority:** low (the overlay already catches this; this is an efficiency/coverage suggestion, not a bug)
- **first observed:** 2026-07-30 16:06 EEST.
