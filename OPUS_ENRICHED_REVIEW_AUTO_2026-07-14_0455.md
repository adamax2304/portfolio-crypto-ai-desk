# Opus Enriched Review — Crypto Overnight / Asia Review — Auto Cycle 04:30 EEST

## 1. Executive Summary

**Slot: crypto overnight / Asia review (04:30 EEST / ~21:40 ET prior day) — advisory only / no auto-trade.** Focus: overnight crypto action, Asia-session BTC/ETH regime, whether alts are bleeding/rotating, and what to watch into the Europe open. Stocks are closed — carried forward as planning-only context.

**Scheduler healthy, data fresh.** `2026-07-14_default_schedule` cycle_01 ran 02:14–02:41 EEST (finished ~2h14m ago, well under the 3h defer threshold, 54/54 steps ok). Crypto scalp (02:21 EEST) and intraday (02:27 EEST) are fresh (~2h18m old, latest available — this is a genuinely quiet Asia-hours cycle, not a data gap). Crypto swing (17:38 EEST prior day, ~11h old) is **carry-forward, borderline-stale** — used for context only. Stocks intraday (02:36 EEST) is fresh but the US cash session is closed, so every stocks idea is capped to planning-only. Today's catalyst folder was missing at run start and was regenerated via the allowed `catalyst-scan` CLI (500 events, 4 baskets).

**Genuinely quiet cycle — no fresh actionable A/B anywhere.** Crypto scalp, intraday, and swing each independently report "No A-tier / No B-tier setups found"; all 10 intraday trade ideas are WATCHLIST ONLY. Stocks intraday found 4 raw A-tier + 10 raw B-tier candidates but demoted every one to C via `market_closed_intraday_planning_only` (expected — US session is shut). This is a real no-new-signal cycle, not a broken pipeline.

**Macro backdrop is a live, escalating risk-off event, not routine chop.** Verified via WebSearch/WebFetch: the US and Iran resumed strikes over the Strait of Hormuz after a brief ceasefire (Iran hit UAE/Qatar/Kuwait/Oman/Bahrain in response); Brent is near $79–83 and WTI near $78 after a 9.4% Monday rally; maritime traffic through the strait has collapsed to ~6 vessels/12h vs. 18–22/day pre-escalation; South Korea's Kospi fell 9% (SK Hynix −15%) and Japan's Nikkei fell ~2%. Bitcoin slipped from ~$64.3k to ~$62.3–62.8k in an Asian-session leverage flush (CoinDesk, modest liquidations, ~1/6 of the worst 30-day print) compounded by the Iran escalation and hawkish Fed signaling (Gov. Waller). This lines up exactly with the desk's own regime read: BTC/ETH trend `transition_down`, only 25% of tracked alts above EMA20/50, recommended style "short bias or no trade; avoid weak altcoin longs."

**22 active crypto signals and 50 active stocks signals are non-terminal (triggered/tp1_hit/tp2_hit) in `active-signals`, but the lifecycle snapshot in `PAPER_MONITOR_STATUS_LATEST.md` (also fresh, 02:39 EEST) shows 0 in every OPEN/WAITING/REVIEW/UNRESOLVED bucket.** This is a genuine reconciliation gap between the two data sources, not something this review can resolve — flagged as a §14 TODO rather than asserted as fact either way.

**Overall verdict: CAUTION, routed by side — not a blanket no-trade.** Best long-watch: **ALLO/USDT** (RS-leader vs. BTC, OI confirms fresh positioning) but price (0.4624) is already through the conditional pullback zone (0.4473–0.4578) — chase risk, wait for a hold-and-retest of that zone. Best short-watch: **LUMIA/USDT**, failed-retest short into 0.0763–0.0795, invalidation above 0.0836. Best catalyst-watch: **HYPE/USDT** (spot-ETF inflow +$10.36M/week, `perps_dex_narrative` basket primary, fresh <1h) — no formal signal yet, wait for pullback per the desk's own `wait_pullback` playbook. Avoid: **XEC/USDT** — top score (91.6) but thin volume (0.23–0.31x) and negative funding flagged "crowding elevated" by the desk's own derivatives cross-check; parabolic, squeeze-prone, no catalyst. AMZN (A-tier, stocks) remains open/carried from the prior US session, unresolved status pending RTH. Scanning, tracking, and the paper book continue uninterrupted regardless.

## 2. Data Used

- Crypto scalp report: `2026-07-13_23-21_scalp_report.md` (generated 02:21 EEST, data 23:15 UTC). No A/B; regime bearish/risk-off; scalp remains low-confidence (known, ongoing — PF 0.14 on 14d expired scalps).
- Crypto intraday report: `2026-07-13_23-27_intraday_report.md` (generated 02:27 EEST, data 23:15 UTC). No A/B; 10/10 trade ideas watchlist-only; best RS-leader ALLO/USDT (score 54.1, no catalyst).
- Crypto swing report: `2026-07-13_14-38_swing_report.md` (generated 17:38 EEST prior day, ~11h old — **carry-forward, borderline stale**, used for narrative/HYPE ETF-flow context only, not as a fresh signal source). No A/B.
- Stocks intraday report: `2026-07-13_23-36_stocks_intraday_report.md` (generated 02:36 EEST, fresh). 4 A-tier + 10 B-tier raw candidates, all demoted to C via `market_closed_intraday_planning_only`; UNH additionally flagged `legal_headline_risk: sec_doj` by the desk's own gate.
- Stocks swing/invest: still 2026-07-02, ~12 days stale, known-deprecated legacy mode (per prior project context), excluded.
- Catalysts: `data/catalysts/2026-07-14/catalyst_events.jsonl` — regenerated this run via `catalyst-scan --no-print` (500 events, 4 baskets: `perps_dex_narrative`/HYPE, `rwa_narrative`/ONDO+XLM, `binance_ecosystem_teaser`/BNB, `delisting_thin_liquidity`/none). Mapped/unmapped computed directly from the JSONL (§5).
- CLI: `active-signals --asset-class crypto` (22 rows, all B-tier, tp1_hit/tp2_hit — no fresh triggers), `active-signals --asset-class stocks` (50 rows; 1 A-tier AMZN + 1 B-tier XOM + 1 B-tier NVDA currently non-terminal, rest historical/aged), `signal-stats` crypto (week: tier=B n=182 PF 1.04 / tier=A n=2 anecdotal; scalp mode PF 0.36 losing; short direction PF 0.33 weak; weekend=Y PF 3.29 vs weekend=N PF 0.64 — see §14 for an observation-logic anomaly), `signal-stats` stocks (headline A/B n=10 PF 1.39 totalR +1.57, weak confidence; C-tier n=179 PF 0.79 negative), `detect_untracked_legacy_alerts --since 2026-07-14` (**0 found**).
- Paper Monitor Status (`reports/PAPER_MONITOR_STATUS_LATEST.md`, 02:39 EEST): lifecycle counts in §3/§14 — flagged reconciliation gap vs. `active-signals`.
- Direct SQLite reads (read-only, `news_items`): HYPE (ETF inflow $10.36M/week, Hyperliquid fundamentals, HIP-3 volume share), ONDO/XLM/BNB (basket context), AMZN/BTC/ETH (last 24h headline check — no legal/headline contradiction found for AMZN; no crypto-specific legal risk found).
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-13_2139.md` (21:39 EEST prior day, ~7h ago) — primary comparison baseline for §4.
- External: 2 WebSearch queries (BTC/ETH overnight Asia price action; Iran/Strait-of-Hormuz oil market) + 2 WebFetch (Al Jazeera Iran/oil summary; CoinDesk Asian-session leverage-flush detail) — sources in §13, ingested into `news_items` via the allowed ingest CLI (3/3 valid, 0 rejected).

## 3. Scheduler / Data Freshness

- `scheduler.log` (`2026-07-14_default_schedule`): cycle_01 started 02:14 EEST, finished 02:41 EEST, 54/54 steps ok — **fresh, not deferred** (~2h14m old at review time).
- Crypto scalp/intraday: **fresh** (generated 02:21–02:27 EEST; this is a genuinely quiet Asia-hours cycle — 0 fresh A/B is expected behavior, not a gap).
- Crypto swing: **carry-forward, borderline stale** (17:38 EEST prior day, ~11h old — near the 12h borderline-stale cutoff; used for narrative context only).
- Stocks intraday: **fresh** (02:36 EEST) but session-capped (market closed).
- Stocks swing/invest: **stale, ~12 days**, known-deprecated legacy mode — excluded from live decisions.
- Paper Monitor Status: **fresh** (02:39 EEST) but its lifecycle counts (0/0/0/0 across OPEN/WAITING/REVIEW/UNRESOLVED, 52 NO_ENTRY_EXPIRED today) do not reconcile with the 72 non-terminal rows (22 crypto + 50 stocks) in `active-signals` — see §14 TODO. Treat both as directionally informative but not fully cross-validated this run.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-07-14 04:55 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "catalyst_missing"], "data_missing": ["initial catalyst folder had to be regenerated this run"],
      "suggested_effect": "advisory_only", "facts_used": ["cycle_01 finished 02:41 EEST, 54/54 ok", "scalp/intraday 02:21-02:27 EEST", "swing 17:38 EEST prior day ~11h old"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.85,
      "reason_codes": ["risk_off", "shorts_preferred", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["BTC/ETH trend transition_down", "altcoin breadth 25% above EMA20/50", "recommended style: short bias or no trade", "Iran/Strait-of-Hormuz escalation, oil ~$78-83", "Kospi -9%, Nikkei -2%", "BTC Asian-session leverage flush ~$64.3k->$62.3-62.8k"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["437/500 (87.4%) catalyst events unmapped to a symbol", "HYPE ETF inflow +$10.36M/week, perps_dex_narrative fresh <1h", "9 legal_risk stock class-action headlines, mostly unmapped to tradable symbols"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "data_unavailable"], "data_missing": ["no funding/OI for most weakest-symbol shorts"],
      "suggested_effect": "advisory_only", "facts_used": ["XEC/USDT funding -0.0037, cross-check flags crowding elevated", "ALLO/USDT OI +20.26% with price up: fresh positioning, monitor crowding"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["chase_risk", "overextended", "clean_retest"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["ALLO current 0.4624 vs conditional pullback zone 0.4473-0.4578 (already through it)", "LUMIA current 0.0748 vs failed-retest short zone 0.0763-0.0795 (needs bounce to trigger)", "all 10 crypto intraday ideas watchlist-only, below active-trade threshold"] },
    { "agent": "execution_lifecycle", "verdict": "manual_review", "confidence": 0.45,
      "reason_codes": ["needs_review", "open_actionable", "no_entry"], "data_missing": ["reconciliation between active-signals non-terminal rows and PAPER_MONITOR_STATUS_LATEST zero counts"],
      "suggested_effect": "advisory_only", "facts_used": ["active-signals: 22 crypto + 50 stocks non-terminal rows (triggered/tp1_hit/tp2_hit)", "PAPER_MONITOR_STATUS_LATEST: OPEN_ACTIVE=0, WAITING=0, REVIEW=0, UNRESOLVED=0, NO_ENTRY_EXPIRED=52 today"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["headline_risk", "reduce_risk"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["live Iran/Strait-of-Hormuz conflict, oil spiking, may continue 'several more days' per Bloomberg", "UNH stocks gate already flags active legal/headline risk (sec_doj)", "AMZN no legal/headline contradiction found in last-24h news"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["crypto scalp mode PF 0.36 / totalR -5.8 (n=49, losing bucket)", "crypto short direction PF 0.33 weak (n=19)", "crypto setup=breakout PF 0.125, 0 wins / 7 losses (n=8)", "stocks A/B headline PF 1.39 but weak confidence (n=10)"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.65,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["synthesis of all 8 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "shorts",
    "best_long_candidate":     { "symbol": "ALLO/USDT", "trigger": "hold-and-retest of 0.4473-0.4578 pullback zone with volume confirmation; invalidation below 0.4346", "reason": "RS-leader vs BTC (+26.3%), OI+price confirm fresh positioning, but current price 0.4624 already through the pullback zone — chasing now is not advised" },
    "best_short_candidate":    { "symbol": "LUMIA/USDT", "trigger": "failed bounce/retest into 0.0763-0.0795 zone, then breakdown; invalidation on 1h close above 0.0836", "reason": "downtrend, -37.9% 24h, -44.1% 7d, regime supports short bias, but needs the retest to confirm rather than chasing the existing drop" },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "pullback into support with narrative + ETF-inflow still intact, per the desk's own wait_pullback playbook; no formal signal yet", "reason": "perps_dex_narrative basket primary (fresh <1h), spot-ETF net inflow +$10.36M this week alongside BTC/ETH/SOL inflows" },
    "avoid_candidate":         { "symbol": "XEC/USDT", "reason": "top momentum score (91.6) but thin volume (0.23-0.31x) and negative funding; the desk's own cross-check flags 'crowding elevated' — squeeze-prone, no catalyst, still watchlist-only despite the high score" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, catalyst_missing | advisory_only |
| market_regime | caution | 0.85 | risk_off, shorts_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, fresh_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.70 | chase_risk, overextended, clean_retest | advisory_only |
| execution_lifecycle | manual_review | 0.45 | needs_review, open_actionable, no_entry | advisory_only |
| risk_manager | caution | 0.70 | headline_risk, reduce_risk | advisory_only |
| playbook_performance | caution | 0.60 | playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-07-13_2139.md` (21:39 EEST, late-session risk review):

- **Same macro thread, escalated.** The prior review flagged the Iran/Strait-of-Hormuz tape as the driver of a US close down 0.2–1.4% across indices; overnight it escalated further (renewed strikes after a brief ceasefire, Iran hitting four Gulf states, oil pushing to $78–83 from the prior day's spike). Not a new event — a continuation and intensification of the same one.
- **No new crypto A/B, same as prior cycle** — the "genuine no-new-signal cycle" call from 7h ago still holds; this is now two consecutive cycles with 0 fresh crypto A/B.
- **JTO/USDT (prior review's best long-watch)** has since become an active B-tier swing signal at `tp1_hit` (score 69.7) — it graduated from watchlist to a live position; no longer the long-watch pick this cycle.
- **DEXE/USDT (prior review's best short-watch, squeeze-flagged)** is now in the weakest-symbols list again (-11.15% 24h) but did not surface a formal trade idea in this cycle's intraday report — dropped in favor of LUMIA/USDT, which has an explicit failed-retest short setup with levels.
- **AMZN A-tier long**: prior review had it as an open position entered ~17:23 EEST prior day. `active-signals` still shows it non-terminal (`triggered`), but `PAPER_MONITOR_STATUS_LATEST` history log shows an AMZN A-tier row closed `+0.5R (profit_lock_stop)` — unclear if this is the same position resolved since the last review or a data-consistency artifact. See §14 TODO; treated as unresolved/carry-forward pending confirmation, not asserted either way.
- **Crypto short-direction weekly stats** (PF 0.33, flagged as a risk-manager concern 7h ago) are unchanged this cycle — still a losing cohort at the weekly level despite the regime call favoring shorts. Continue treating new crypto shorts with extra scrutiny (clean breakdown + volume, not just "regime says short").
- **Catalyst mapping weak in both reviews** (83.8% unmapped 7h ago, 87.4% unmapped now) — persistent, not new.

## 5. Catalyst Coverage

- Total catalyst events today (`data/catalysts/2026-07-14/catalyst_events.jsonl`, regenerated this run): **500**
- Mapped to a symbol: **63** (12.6%)
- Unmapped: **437** (87.4%)
- Narrative baskets: **4** (`perps_dex_narrative`/HYPE, `rwa_narrative`/ONDO+XLM, `binance_ecosystem_teaser`/BNB, `delisting_thin_liquidity`/none)

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Top 3 unmapped headlines:
1. "MEHR SAYS SEVERAL AREAS IN SOUTHWESTERN IRAN'S KHUZESTAN'S OMIDIYEH HIT BY U.S. PROJECTILES" (t.me/WalterBloomberg) — macro/geopolitical, not symbol-specific.
2. "EMBC Investors Have Opportunity to Lead Embecta Corp. Securities Fraud Lawsuit" (PR Newswire (Stocks)) — legal-risk boilerplate, ticker not auto-extracted.
3. "Serve Robotics: A Risky Bet or a Future Winner?" (The Motley Fool Investing) — generic commentary, not catalyst-grade.

Legal/regulatory risk cluster this run: 9 `legal_risk` events, mostly securities-fraud class-action solicitation notices (EMBC, VERI, AVAV, FSLR, BTU, BMI, VRRM, GRAL, FUTU) — boilerplate law-firm notices, not fresh news of wrongdoing; low actionability, noted for completeness only.

## 6. Market Landscape

**Crypto**: BTC/ETH trend `transition_down`, altcoin breadth only 25% above EMA20/50 (weak). Strongest movers (XEC +35.8%, ALLO +23.8%) are largely thin-volume/no-catalyst pops; weakest movers (LAB -43.9%, LUMIA -37.9%, SYN -23.9%) are already extended down. Overnight BTC leverage flush (~$64.3k → ~$62.3-62.8k) compounded by the Iran/Hormuz escalation and hawkish Fed signaling (Waller). No fresh crypto A/B for a second consecutive cycle.

**Stocks**: Closed (US cash session). 4 A-tier + 10 B-tier raw candidates this cycle, all capped to planning-only by the market-closed gate: longs AAPL/UNH/META/XLF/XLE, shorts SMH/AVGO/GOOGL/QQQ/AMD/COIN/TSLA/SMCI/XLK. UNH additionally carries a system-flagged `legal_headline_risk: sec_doj` (manual review required) — carry this into the pre-US-open review, do not treat UNH as a clean long candidate even after RTH confirmation without a fresh manual check. XLE (long) and semiconductor shorts (SMH/AVGO/AMD) line up with the oil-spike/Kospi-crash macro thread.

### Market Mood / Risk Routing
- Crypto mood: **risk-off** (transition_down trend, weak breadth, live geopolitical escalation)
- Stocks mood: **closed** (planning-only; last known regime chop-to-risk-off per prior cycle, Iran/Hormuz-driven)
- Dominant narrative: **Iran/Strait-of-Hormuz escalation → oil spike → broad risk-off**, secondary: perps-DEX (HYPE) ETF-inflow strength as a local bright spot
- Preferred side now: **shorts** (regime-aligned), with catalyst-backed longs (HYPE on confirmation) as the exception
- Best long candidate: **ALLO/USDT** — trigger: hold-and-retest of 0.4473-0.4578, not chase current 0.4624
- Best short candidate: **LUMIA/USDT** — trigger: failed retest into 0.0763-0.0795 then breakdown
- Best catalyst-backed candidate: **HYPE/USDT** — trigger: pullback + narrative/ETF-inflow still intact (no formal signal yet)
- What to avoid: **XEC/USDT** (thin-volume, crowding-elevated pump); new intraday crypto longs generally, given the desk's own "avoid weak altcoin longs" regime call
- What would change the view: a de-escalation headline out of the Strait of Hormuz conflict, BTC reclaiming and holding above ~$64k, or altcoin breadth pushing back above ~40-50% of EMA20

## 7. Candidate Deep Dives

### 1. AMZN (stocks/intraday, A-tier, carry-forward)
- Status: `active-signals` shows `triggered`, entry 245.41-246.44, expires 2026-07-14T14:23:20 EEST (~07:23 ET, pre-market). Entered during the prior US session (~17:23 EEST prior day per last review).
- Has price already reacted to a catalyst? No fresh AMZN-specific catalyst found in the last 24h beyond generic "Meta and Amazon lead $725B Big Tech spending spree" coverage — this is a momentum/technical entry, not catalyst-driven.
- Legal/headline check: no legal or headline risk found for AMZN in the last 24h.
- Is this chasing? N/A — carried position, not a fresh entry decision this cycle.
- Actionable now? No — market closed; nothing to do until RTH. Reconfirm status live at market open given the §14 monitor/active-signals reconciliation gap below.
- What would invalidate: a break of 244.38 (invalidation level) once the session reopens.

### 2. HYPE/USDT (crypto, catalyst-backed watch, no formal signal)
- Catalyst: spot-ETF net inflow +$10.36M this week (alongside BTC +$197.4M, ETH +$84.4M, SOL +$0.93M; XRP the lone outflow at -$7.18M) — verified via internal `news_items` (t.me/cointelegraph, t.me/wublockchainenglish), consistent across scalp and swing report catalyst sections. `perps_dex_narrative` basket primary, fresh <1h in the latest cycle.
- Has price already reacted? Unclear — no price/ATR levels available in either report (HYPE did not surface as a formal trade idea in scalp/intraday/swing this cycle).
- Chase risk? Cannot assess without price data — treat as watch-only until a formal signal appears.
- Actionable now? No — desk's own playbook for this basket is `wait_pullback`; no entry until the pipeline promotes it to a scored trade idea.
- What would invalidate: the perps-DEX narrative losing steam (e.g., ETF outflow reversal) or the basket downgrading from fresh (<6h) to stale.

### 3. LUMIA/USDT (crypto, best short-watch)
- Setup: intraday Trade Idea #1, score 60.0, low confidence, `crypto_intraday_catalyst_or_momentum` playbook, **watchlist only** (below active-trade threshold, score 33.0 on the risk gate).
- Failed bounce/retest short zone: 0.0763-0.0795. Invalidation: 1h close beyond 0.0836. Conditional targets: TP1 0.0675 / TP2 0.0602 / TP3 0.0529.
- Current price 0.0748 — below the retest zone; needs a bounce back up into 0.0763-0.0795 to trigger, not a chase of the existing -37.9% move.
- No fresh verified catalyst — pure technical/momentum short in a bearish-regime tape.
- Counter-thesis (from the report itself): fails if this is a late breakdown into exhausted sellers and BTC/ETH reclaim local levels; volume is below average (0.09x), so breakout/breakdown confirmation is weak.
- Is this aligned with market mood? Yes — risk-off regime explicitly favors shorts over longs.
- Actionable now? No — watchlist only; wait for the retest + volume confirmation.

### 4. ALLO/USDT (crypto, best long-watch, chase-risk flagged)
- Setup: intraday Trade Idea #6, score 54.1, low confidence, same playbook, **watchlist only**.
- Conditional pullback zone: 0.4473-0.4578. Invalidation: 1h close beyond 0.4346. Conditional targets: TP1 0.4856 / TP2 0.5088 / TP3 0.5320.
- Current price 0.4624 — **already through** the conditional pullback zone; a fresh entry here is chasing.
- Also has a live, separate B-tier swing position already open (entries at 0.4063-0.4136, `tp1_hit`) — the existing runner is fine to hold/monitor; this is a distinct, later-cycle idea, not a size-up on the same position.
- Counter-thesis (from the report): this is a relative-strength long against a bearish tape — reduce size, demand confirmation; no fresh catalyst verified; volume below average (0.15x).
- Is this a chase-risk setup? Yes, at current price. Actionable only on a hold-and-retest of the pullback zone.

## 8. Best Candidates Ranked

1. **HYPE/USDT** — catalyst-watch (ETF inflow + narrative), wait for pullback per desk playbook, no formal signal yet.
2. **LUMIA/USDT** — short-watch, wait for failed retest into 0.0763-0.0795.
3. **ALLO/USDT** — long-watch, wait for hold-and-retest of 0.4473-0.4578; do not chase current price.
4. **AMZN** — carry-forward open A-tier stocks position, reconfirm live at RTH given the §14 reconciliation gap.

No clean immediately-actionable trade exists this cycle across crypto or stocks — this is a decision-window read only, not a system pause; scanning/tracking continue.

## 9. Avoid / No Trade

- **XEC/USDT** — top momentum score (91.6, +35.8% 24h) but thin volume (0.23-0.31x) and negative funding; the desk's own Bybit/OKX cross-check flags "crowding elevated." Squeeze-prone, no catalyst. Avoid chasing.
- **New crypto intraday longs generally** — regime explicitly says "short bias or no trade; avoid weak altcoin longs" with only 25% breadth above EMA20/50.
- **UNH (stocks, once RTH reopens)** — system-flagged `legal_headline_risk: sec_doj`, manual review required; do not treat as a clean long even if it re-scores A-tier at the open.
- This is a **decision-window** call only — never a command to pause scanning, data collection, tracking, or the scheduler.

## 10. Main Risks

- **Live geopolitical escalation**: Iran/Strait-of-Hormuz conflict is ongoing and, per Bloomberg, US strikes "may last several more days" — headline risk cuts both ways (de-escalation could snap back a risk-off tape fast; further escalation could extend the leverage-flush move).
- **Catalyst mapping at 87.4% unmapped** — treat any catalyst-driven thesis as context, not a standalone trigger.
- **Active-signals vs. paper-monitor reconciliation gap** (§14) — do not fully trust either source in isolation for "what's actually open right now" until reconciled.
- **Crypto short-direction weekly PF (0.33) remains negative** despite the regime call favoring shorts — a real, persistent risk-manager concern, not a one-off.
- **Scalp mode remains a losing bucket** (PF 0.36, totalR -5.8 over 49 signals) — treat any scalp-mode idea with extra skepticism regardless of score.

## 11. Action Plan — next 4 hours

- Watch HYPE/USDT for a pullback entry with the ETF-inflow narrative still intact.
- Watch LUMIA/USDT for a failed retest into 0.0763-0.0795 before shorting.
- Do not chase ALLO/USDT above 0.4578; wait for a hold-and-retest.
- Avoid fresh XEC/USDT longs; avoid new crypto intraday longs generally given weak breadth.
- Reconfirm AMZN's actual live status (open vs. closed) once RTH data is available, given the §14 gap.
- Monitor for any de-escalation or further-escalation headline out of the Strait of Hormuz — this is the single biggest swing factor into the Europe open.
- No action needed on scanning/tracking/scheduler — continue as-is.

## 12. Final Verdict per Mode

- **Crypto scalp**: No trade. Known losing bucket (PF 0.36); regime bearish/risk-off; no A/B.
- **Crypto intraday**: No trade. All 10 ideas watchlist-only; wait for LUMIA retest or ALLO pullback-hold.
- **Crypto swing**: No new entries (carry-forward report, ~11h old); manage existing runners (ALLO, KAT, BCH, BTC, TRB, etc. — all already `tp1_hit`/`tp2_hit`, let them run/trail per existing TP/SL).
- **Stocks intraday/swing/invest**: Closed — planning-only. Candidate watchlist for RTH: longs AAPL/META/XLF/XLE (UNH excluded — legal flag); shorts SMH/AVGO/GOOGL/QQQ/AMD/COIN/TSLA/SMCI/XLK, but require RTH confirmation before treating any as actionable, especially given overnight gap risk from the Iran/Hormuz headlines.

## 13. Sources

- [Bitcoin slips below $63,000 in an Asian-session leverage flush](https://www.coindesk.com/markets/2026/07/13/bitcoin-slips-below-usd63-000-in-an-asian-session-leverage-flush) — CoinDesk, 2026-07-13
- [Oil prices jump as US and Iran trade attacks over Strait of Hormuz](https://www.aljazeera.com/economy/2026/7/13/oil-prices-jump-as-us-and-iran-trade-attacks-over-strait-of-hormuz) — Al Jazeera, 2026-07-13
- [Bitcoin and ethereum prices today, Monday, July 13, 2026: Strong price openings backtracking this morning](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-monday-july-13-2026-strong-price-openings-backtracking-this-morning-133042462.html) — Yahoo Finance, 2026-07-13
- [Latest Oil Market News and Analysis for July 14](https://www.bloomberg.com/news/articles/2026-07-13/latest-oil-market-news-and-analysis-for-july-14) — Bloomberg, 2026-07-13 (referenced for "strikes may last several more days," not fetched in full)
- Internal: `data/catalysts/2026-07-14/catalyst_events.jsonl`, `catalyst_cycle_01-40.md`, `news_items` (HYPE ETF-flow rows, t.me/cointelegraph & t.me/wublockchainenglish)

## 14. Fix Requests / TODO

### TODO-active-signals-monitor-reconciliation
- **issue:** `active-signals` CLI shows 22 crypto + 50 stocks rows in non-terminal states (`triggered`/`tp1_hit`/`tp2_hit`), but `reports/PAPER_MONITOR_STATUS_LATEST.md` (same-cycle-fresh, 02:39 EEST) shows 0 in every one of OPEN_ACTIVE/WAITING_FOR_ENTRY/REVIEW_ONLY_SHADOW/ENTERED_UNRESOLVED_EXPIRED, with 52 NO_ENTRY_EXPIRED today instead. Specifically, `active-signals` shows AMZN A-tier `triggered` (entry 245.41-246.44) as still open, while the monitor-status history log contains a separate AMZN A-tier row `CLOSED WIN +0.5R (profit_lock_stop)` — unclear if these are the same position (already resolved, `proposed_signals.status` stale) or genuinely two different signal instances.
- **evidence:** `python -m src.cli active-signals --asset-class stocks` row `sig_78fb61c80fd77352` (AMZN, triggered) vs. `reports/PAPER_MONITOR_STATUS_LATEST.md` line 69 ("AMZN long (stocks/intraday/A) — CLOSED WIN +0.5R").
- **suggested manual fix:** trace whether `PAPER_MONITOR_STATUS_LATEST.md`'s display-group counts are computed from a different/lagging snapshot than `active-signals`, and whether `proposed_signals.status` is being updated when a position closes via paper execution. If they're genuinely the same position, this is a status-sync bug; if genuinely different signal_ids, the monitor's OPEN_ACTIVE=0 count for a cycle where `active-signals` shows 72 non-terminal rows needs an explanation.
- **priority:** high
- **first observed:** 2026-07-14 04:55 EEST

### TODO-signal-stats-weekend-observation-heuristic
- **issue:** `signal-stats --asset-class crypto` auto-generated observation says "(stronger, n=50) weekend=Y: weekend signals underperform (winrate 24%, n=50)" but the same table shows weekend=Y with PF 3.29, avgR +0.606, totalR +20.6 (strongly profitable) vs. weekend=N at PF 0.64, totalR -16.1 (losing). The observation heuristic appears to key off raw winrate only and ignores the R-asymmetry (weekend=Y wins are large, losses are small), producing a directionally misleading auto-observation.
- **evidence:** `python -m src.cli signal-stats --asset-class crypto` → "By weekend_mode" table + "observations (manual approval required)" block, this run (2026-07-14 ~04:45 EEST).
- **suggested manual fix:** review the observation-generation logic (likely a winrate-threshold rule) and have it weight PF/totalR alongside winrate, or at minimum not label a PF-3.29/totalR-+20.6 cohort as "underperform."
- **priority:** medium
- **first observed:** 2026-07-14 04:55 EEST

### TODO-catalyst-mapping-persistently-weak
- **issue:** Catalyst→symbol mapping has been below 20% mapped for at least two consecutive reviews (12.6% today, 16.2% ~7h ago per the prior review). Most unmapped headlines are macro/geopolitical or generic law-firm class-action boilerplate that may never be symbol-mappable, but the persistently low rate limits the catalyst layer's usefulness as a standalone signal input.
- **evidence:** this run: 63/500 mapped (12.6%); prior review (`OPUS_ENRICHED_REVIEW_AUTO_2026-07-13_2139.md`): 640/3954 mapped (16.2%).
- **suggested manual fix:** sample the unmapped set to determine what fraction is genuinely unmappable (macro/legal boilerplate) vs. symbol-specific news the resolver is missing; if the latter is non-trivial, improve the symbol resolver per the existing news-layer-hardening context (17% match rate was already known as an issue).
- **priority:** low
- **first observed:** 2026-07-14 04:55 EEST (persistent — not new)
