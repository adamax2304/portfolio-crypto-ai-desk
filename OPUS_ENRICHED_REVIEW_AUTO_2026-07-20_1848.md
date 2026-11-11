# Opus Enriched Review — US open reaction review — Auto Cycle 18:30 EEST

## 1. Executive Summary

**Slot: US open reaction review** (nominal 18:30 EEST; dispatched ~18:39, ~9 min jitter). **Advisory only — no auto-trade, no scoring/threshold/strategy changes made or implied.**

**Crypto:** range/chop, neutral regime (BTC range, ETH range/uptrend split across cycles), zero A-tier and zero B-tier *fresh* setups in the newest scalp/intraday/swing reports. 14 active B-tier positions are all carryover from earlier cycles (13 long, 1 short); 2 of them (ALLO/USDT, NEAR/USDT-short) are **past their own `expires_at`** and still shown running — flag both **NEEDS REVIEW**. Macro backdrop is geopolitical risk-off: active US–Iran hostilities (ceasefire collapsed July 8, nightly strikes continuing) and multiple regional escalation headlines (Houthi maritime embargo, Ukraine drone strikes on Moscow).

**Stocks:** internal regime label is **risk_off / short bias** (VIX 18, breadth-above-EMA20 0%), and the scan produced a wall of high-score short candidates across mega-cap tech and semis (NVDA, AVGO, XLK, QQQ, META, TSLA, COIN, SMH). **Externally verified this run: today is actually a chipmaker-led rebound session** — S&P +0.6%, Nasdaq 100 +1.3%, SOX +3.1% recovering from Friday's bear-market close, NVDA +2% intraday, Broadcom also up — directly contradicting the short thesis on two names. **NVDA and AVGO's own short signals were re-scanned by the system itself ~75–80 minutes later and demoted to `no_directional_setup` (score 38)** — the setups are already self-invalidated by fresher data but the DB still shows them `waiting_for_entry`/`triggered`. Every other stocks idea this cycle (0 A/B actionable, 22 C-tier) is correctly gated non-actionable by the SI-1..5 confirmation gates, so there is **no live execution risk** — the finding is about signal hygiene, not routing.

**Legal/headline risk:** UNH's DOJ/Claritev antitrust probe is **externally confirmed and expanding** (new civil investigative demands, earnings call July 29) — correctly gated to manual-review-only. TSLA's `going_concern` tag could **not** be corroborated by external search (no such warning found) — flagged as a possible stale/mislabeled system flag, TSLA's real near-term risk is the July 22 earnings blackout (also true for GOOGL).

**Data hygiene:** stocks active-signals list carries **28 of 50 rows past their own expiry** (oldest from 2026-07-08, 12 days stale) still shown `tp1_hit`/`tp2_hit` — same pattern as the crypto ALLO/NEAR staleness, much larger scale on the stocks side. Catalyst mapping is weak this run (**71.0% unmapped**, 615/2,121 mapped) — use the catalyst layer as directional context only.

## 2. Data Used

- Reports: scalp (`2026-07-20_13-06`, generated 16:06 EEST), intraday (`2026-07-20_13-12`, generated 16:12 EEST, ~2.5h old — normal cadence gap, next cycle due ~19:1x), swing (`2026-07-20_14-30`, generated 17:30 EEST, ~1.3h old, freshest). Stocks intraday (`2026-07-20_15-36` / data 15:35 UTC = 18:35 EEST, ~13 min old — freshest possible). Stocks swing/invest: `2026-07-02` — **stale** (18 days), excluded from verdicts, no swing/invest scan has run since; not used.
- Catalysts: `data/catalysts/2026-07-20/catalyst_events.jsonl` (2,121 cumulative events today), `narrative_baskets.jsonl` (5 baskets), latest `catalyst_cycle_13-17.md` (16:17 EEST).
- LLM packets: `llm_analysis_packet.md` (17:30 EEST, fresh), `llm_stocks_packet.md` (00:41 EEST, stale — superseded by fresher stocks intraday report for this review).
- CLI: `active-signals` ×2 (crypto 14 rows, stocks 50 rows), `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-07-20` (0 findings — clean).
- DB reads: `proposed_signals` created_at/score history for NVDA, AVGO, XLK, QQQ, META (confirmed NVDA/AVGO thesis reversal timing); `news_items` 72h symbol search for TSLA and UNH (UNH: no direct DOJ headline in local news_items in the window; TSLA: earnings-focused coverage only, no going-concern language).
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-19_2153.md` (late-session slot) — used for §4 comparison.
- External: 5 WebSearch queries (US stock market/semis today, TSLA going-concern check, UNH DOJ check, NVDA/AVGO intraday price action, Iran/Bitcoin macro update). No WebFetch needed — search snippets from Bloomberg, CNBC, Yahoo Finance, Healthcare Dive, PYMNTS, SEC EDGAR were sufficient and mutually consistent. Sources ingested via `scripts.ingest_enriched_review_sources` (crypto + stocks tagged).

## 3. Scheduler / Data Freshness

- `scheduler.log`: mtime ~17:34 EEST, ~74 min old at review start — well under the 3h defer threshold. Not deferred.
- Latest completed cycle summary: `cycle_07_15-58_summary.md` (mtime 17:34 EEST).
- Crypto reports: scalp/intraday ~2.5h old (normal ~3h10m cadence, not stale); swing ~1.3h old (freshest). All three fresh reports independently show **0 A-tier / 0 B-tier new ideas** this run — consistent across modes.
- Stocks intraday: 13 minutes old — as fresh as this pipeline gets. Stocks swing/invest: 18 days old (2026-07-02) — stale, excluded, planning-only if referenced at all (not referenced this review; no new swing/invest signal touched today).
- Monitor/paper status: not directly queried this run (outside the allowed CLI list); no anomaly signal from `detect_untracked_legacy_alerts` (clean) or from scheduler.log recency.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-07-20 18:48 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["monitor/paper-portfolio live status (outside allowed read-only CLI set)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log ~74min old", "stocks intraday report 13min old", "crypto scalp/intraday ~2.5h old on normal ~3h10m cadence", "stocks swing/invest 18 days stale, unused"]
    },
    {
      "agent": "market_regime",
      "verdict": "mixed",
      "confidence": 0.6,
      "reason_codes": ["mixed", "chop", "risk_off"],
      "data_missing": ["live intraday BTC/ETH tick beyond report snapshot"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC range, ETH range/uptrend split, altcoin breadth 47-49%, 0 A/B ideas across scalp/intraday/swing", "stocks: internal label risk_off/short-bias (VIX 18.01, breadth-above-EMA20 0%) but externally-verified today is a chipmaker-led rebound (SOX +3.1%, NDX100 +1.3%, NVDA +2% intraday)", "multi-day (5d/20d) tech trend still negative even as today's session bounces"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "fresh_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 71.0% unmapped today (615/2121 mapped)", "5 active narrative baskets: delisting_thin_liquidity, rwa_narrative(ONDO/XLM), ai_narrative(NEAR/RENDER/TAO/FET), perps_dex_narrative(HYPE), momentum_breakout(PROM)", "UNH DOJ/Claritev probe externally confirmed and expanding", "TSLA going_concern flag not externally corroborated"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.4,
      "reason_codes": ["data_unavailable", "funding_extreme"],
      "data_missing": ["OI 24h% for most crypto active names (n/a in report)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ACE/USDT and ALICE/USDT show negative funding across external venues (bybit/mexc) = elevated crowding on the long side", "VANRY/USDT negative funding + elevated crowding, already rejected from top setups", "most active B-tier names show funding ~neutral, OI n/a"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["chase_risk", "stale_before_entry", "entry_late", "price_moved_away"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["NVDA short (score 87.5, created 14:21 UTC) and AVGO short (score 90.7, created 14:16 UTC) both re-scanned ~75-80min later at score 38 no_directional_setup — thesis already invalidated by fresher data, DB status not yet updated", "PROM/USDT rejected explicitly for being >2 ATR from EMA20 — 'do not chase'", "all 4 crypto C-tier watchlist cards (ALICE, BANK, PUMP, KAITO) explicitly 'not active until regime/volume/confirmation improves'"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "caution",
      "confidence": 0.8,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow", "needs_review", "no_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 14 active B-tier — 7 open/triggered running, 2 waiting_for_entry, 3 tp1_hit running, 2 past-expiry needs-review (ALLO expired 2026-07-19T15:21, NEAR-short expired 2026-07-17T15:56)", "stocks: 22 signals from today's cohort, all C-tier review/shadow (0 A/B actionable after gates), 28 legacy rows past expiry (oldest 2026-07-08, 12 days stale) still shown active"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: DOJ/Claritev antitrust probe expanding, externally confirmed (Healthcare Dive, PYMNTS, SEC 10-Q) — correctly gated legal_headline_risk:sec_doj", "TSLA: gated legal_headline_risk:going_concern but no external corroboration found; TSLA/GOOGL both have earnings in 2 trading days (July 22) — earnings-blackout risk is real regardless of the going_concern tag", "NEAR/USDT short direction has weak historical stats: n=10, PF 0.25, avgR -0.43R"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto B-tier overall: n=119, PF 2.13, but triggered winrate only 30% (observation flag: 'consider reviewing entries')", "crypto direction=short: n=10, PF 0.25, avgR -0.43 — weak, applies directly to the active NEAR/USDT short", "stocks C-tier: n=194, PF 0.74, winrate 20.4% — watchlist-only, consistent with why gates keep it non-actionable", "stocks A/B headline: n=7 anecdotal, PF 1.0, too small to read"]
    },
    {
      "agent": "head_trader",
      "verdict": "ok",
      "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "BANK/USDT", "trigger": "1h close back inside 0.2650-0.2764 pullback zone on rising volume (currently 0.02x avg) — do not chase the extended 48% 24h move", "reason": "highest-score momentum name (91.6) with clean uptrend but volume/confirmation still missing per its own playbook" },
    "best_short_candidate":    { "symbol": "XLK/META (stocks)", "trigger": "post-lunch (13:30-15:00 ET) confirmation with RVOL back above gate minimum + failed retest of today's rebound high, only after SI-1..5 gates clear organically", "reason": "highest-conviction raw scores (85/84) that survived the freshest 15:35 UTC re-scan (unlike NVDA/AVGO which did not) — but currently chasing an active rebound, so wait for confirmation not chase" },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "playbook is explicitly wait_pullback — need a clean pullback entry into the perps_dex_narrative basket, not a breakout chase", "reason": "primary of the freshest (<1h) narrative basket with an actual news-driven thesis (HIP-4 Outcome Markets), unlike PROM/USDT which is pure momentum with no catalyst" },
    "avoid_candidate":         { "symbol": "UNH", "reason": "externally-confirmed expanding DOJ/Claritev antitrust probe; correctly gated to manual-review, do not treat as a clean long or short regardless of technical score" },
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
| market_regime | mixed | 0.60 | mixed, chop, risk_off | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, no_catalyst, fresh_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.40 | data_unavailable, funding_extreme | advisory_only |
| technical_entry | caution | 0.65 | chase_risk, stale_before_entry, entry_late, price_moved_away | advisory_only |
| execution_lifecycle | caution | 0.80 | open_actionable, waiting_for_entry, review_shadow, needs_review, no_entry | advisory_only |
| risk_manager | caution | 0.60 | legal_risk, headline_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.70 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | ok (synthesis) | 0.60 | — | advisory_only |

## 4. What Changed vs Previous Review

vs `OPUS_ENRICHED_REVIEW_AUTO_2026-07-19_2153.md` (late-session, Sunday):

- **New:** stocks are now open and live (Sunday review was weekend-closed/planning-only) — this is the first review this window with real stocks intraday data. Entire stocks candidate set (22 today's-cohort C-tier names) is new to the review.
- **Persisted, unresolved:** NEAR/USDT short still stale-past-expiry (now 3 days past its 2026-07-17 expiry, was already flagged Sunday). ALLO/USDT still stale-past-expiry (now ~1.3 days past its 2026-07-19 expiry, was flagged Sunday as "expired 15:21 today"). Neither has auto-closed across two review cycles — worth escalating (see §14).
- **Resolved:** the untracked-alert integrity issue (5 instances flagged Sunday for ALLO/HOME/BANK) shows **0 findings** today — clean for the current date window. Catalyst mapping is still weak (71.0% today vs 65.7% Sunday) — trending worse, not better.
- **Regime:** crypto stayed in the same range/chop, zero-A/B state across both reviews — no new crypto entries have cleared the desk threshold in over 24h of reviews now.
- **Thesis changed intra-cycle:** NVDA and AVGO stocks shorts (new this run) were created and self-invalidated by the system's own next scan within ~80 minutes — a fast thesis flip driven by today's chipmaker rebound, not present in any prior review.

## 5. Catalyst Coverage

- Total `catalyst_events` today: **2,121** | mapped (non-null symbol): **615** (29.0%) | unmapped: **1,506** (71.0%)
- `narrative_baskets` today: **5** (delisting_thin_liquidity, rwa_narrative, ai_narrative, perps_dex_narrative, momentum_breakout)
- **Catalyst mapping weak this run (71.0% unmapped) — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines this cycle: "Tradfin: *SEOUL STOCK MARKET'S KOSPI FALLS 4%..."; "FSTA vs. XLP: How These Popular Consumer Staples ETFs Compare for Investors"; "Oil Pulls the Market Lower Again" (appeared twice).

## 6. Market Landscape

Crypto: range/chop, neutral. BTC range-bound both cycles; ETH split range/uptrend depending on snapshot. Altcoin breadth 47–49% above EMA20 — genuinely mixed, not broadly risk-on or risk-off. Strongest movers (BANK +48%, ACE +116%, PROM +40%, PUMP +17%) are all momentum-without-confirmed-catalyst per their own playbooks. Macro overlay is geopolitical risk-off: US–Iran ceasefire collapsed July 8, active nightly strikes continuing as of this week, Houthi maritime embargo on Saudi Arabia, Ukraine drone strikes on Moscow — internal macro-risk score 97.8/100. Externally, Bitcoin has been trading a volatile mid-$60Ks–low-$70Ks range through this conflict rather than breaking down sharply — the geopolitical overhang has not translated into a clean directional crypto move either way.

Stocks: internal regime label is risk_off/short-bias (0% breadth above EMA20, QQQ downtrend on 5d/20d), but **today's actual session is a rebound** — S&P +0.6%, Nasdaq 100 +1.3%, SOX +3.1% (recovering from Friday's bear-market close), NVDA +2% intraday, Broadcom also higher, driven by a "deluge of earnings reports" this week (GOOGL/TSLA report Wednesday July 22). Sector rotation: energy/healthcare/financials strongest (RS +8.3%/+7.4%/+5.1% vs SPY 20d), semiconductors/technology weakest on the 20d lookback (-14.2%/-7.4%) even as today bounces — this is a multi-day-downtrend-meets-single-day-bounce setup, not a clean regime.

### Market Mood / Risk Routing

- Crypto mood: **chop** (range-bound, mixed breadth, no confirmed catalyst on the leaders)
- Stocks mood: **mixed** (multi-day downtrend in tech/semis vs today's rebound session; VIX only 18 — not panic-level)
- Dominant narrative: crypto — momentum-without-catalyst rotation (BANK/ACE/PROM); stocks — "Magnificent Seven" earnings week, chip-stock whipsaw
- Preferred side now: **wait-for-trigger** on both books; if forced, crypto favors watching longs (direction=short historically weak, PF 0.25 last week), stocks favors watching shorts on names that survived the freshest re-scan (XLK/QQQ/META/TSLA/COIN/SMH) but only after confirmation, not chasing today's bounce
- Best long candidate: BANK/USDT (crypto) — watch, not yet triggered by volume
- Best short candidate: none actionable — XLK/META/QQQ are the cleanest short-watch names but require post-lunch confirmation the gates haven't given yet
- Best catalyst-backed candidate: HYPE/USDT (perps_dex_narrative, fresh <1h, playbook wait_pullback)
- What to avoid: UNH (confirmed DOJ probe), chasing NVDA/AVGO shorts (already invalidated by the system's own fresher scan), chasing TSLA/GOOGL ahead of Wednesday earnings
- What would change the view: crypto — a fresh catalyst-backed breakout with volume confirmation on any of BANK/ACE/PROM; stocks — a clean post-lunch failed-retest on the tech complex would validate the short thesis, while a held bounce above today's highs into the close would invalidate it further

## 7. Candidate Deep Dives

### 1. NVDA / AVGO (stocks, short) — stale, self-invalidated thesis

- Has price already reacted to the catalyst? Yes — both were scored as strong shorts (NVDA 87.5, AVGO 90.7) at 14:16-14:21 UTC (~10:16-10:21am ET), right around the open, likely capturing an early-session dip.
- Is the setup chasing? By the time of the 15:35 UTC re-scan, both were re-priced by the system itself to `no_directional_setup` (score 38) — the setup is now chasing a move that has already reversed.
- Retest/pullback structure? None documented; the reversal is external (Bloomberg-confirmed NVDA +2% intraday, SOX +3.1%), not a technical pullback.
- Overextended? Not applicable in the classic sense — the *direction* is now wrong, not just late.
- Would entry now be late? Yes — entering either short now would be shorting into a confirmed same-day rebound.
- Aligned with market mood? No — market mood for chips today is recovery, not weakness.
- Long, short, or wait? Neither — treat both as **NO-ENTRY / MOVED AWAY**, not fresh.
- Actionable now or after confirmation? Not actionable; both are C-tier and were never Telegram-pushed, so no live exposure exists. This is a data-hygiene finding, not a risk event.
- Invalidation: already invalidated per the system's own next scan.
- Chase-risk: yes, maximal — this is the textbook chase-a-fake-move case this slot exists to catch.
- Catalyst confirmation/contradiction: contradicted — no fresh catalyst supports either short, and price action contradicts it.

### 2. UNH (stocks) — confirmed legal risk, avoid

- Gated by the system as `legal_headline_risk: sec_doj`, C-tier, not actionable.
- Externally confirmed this run: UNH faces an **expanding** DOJ antitrust probe into its Claritev health-tech unit, including new civil investigative demands alleging collusion with major insurers; executives are expected to address it on the July 29 earnings call (Healthcare Dive, PYMNTS, Simply Wall St, corroborated by UNH's own 10-Q).
- This is real, current, and worsening — not a stale flag. Verdict stays **AVOID / MANUAL REVIEW REQUIRED**, independent of the raw technical score (75.5, short).
- What would change the view: a confirmed DOJ settlement or probe-narrowing announcement; absent that, keep excluding UNH from any actionable consideration.

### 3. TSLA (stocks) — flag mismatch + earnings blackout

- System gates TSLA to C-tier with `legal_headline_risk: going_concern`. External search (multiple queries) found **no** going-concern warning, filing, or auditor language for Tesla in 2026 — only analyst commentary on negative free-cash-flow projections for 2026-2028, which is not the same thing as a going-concern disclosure.
- This looks like a possible mislabeled or stale system flag (see §14 TODO) — but it doesn't change the operator conclusion, because TSLA has a **separate, undisputed** reason to stay off the actionable list: earnings on July 22 (2 trading days out), explicitly flagged by the report as "AVOID holding through / chasing into earnings."
- Actionable now or after confirmation? No — wait for the print. What would invalidate: nothing changes this before Wednesday; post-earnings, reassess fresh.

### 4. HYPE/USDT (crypto) — best catalyst-backed watch

- Primary of the `perps_dex_narrative` basket, freshness <1h, playbook explicitly `wait_pullback`.
- Catalyst: Hyperliquid's HIP-4 Outcome Markets launch (permissionless deployment, 500k HYPE stake) — a genuine news-driven thesis, distinct from the pure-momentum PROM/USDT cluster (no confirmed catalyst).
- Not currently an active signal or scored candidate in either fresh report — this is a narrative-layer watch item, not yet a scored trade idea.
- Actionable now? No — the playbook itself says wait for a pullback, not chase the news. Trigger: clean pullback entry into HYPE/USDT structure with the basket still fresh (<24h) and no contradicting price action.
- Related names in the same basket if HYPE doesn't offer a clean level: DYDX/USDT, GMX/USDT, ASTER/USDT.

### 5. NEAR/USDT (crypto, short) — stale, needs review

- Status `tp1_hit`, but `expires_at` was 2026-07-17T15:56:12 — **3 days past expiry**, still shown as an active running position across two consecutive reviews (flagged Sunday 21:53, still open now).
- Direction=short has weak crypto-wide historical stats this week: n=10, PF 0.25, avgR -0.43R — this specific position sits in the system's worst-performing bucket.
- It also carries the `ai_narrative` basket association (NEAR is a basket primary, freshness <24h) — but that basket context doesn't rescue a 3-day-stale short.
- Recommendation: **NEEDS REVIEW** — this is a lifecycle/monitoring gap, not a live decision; a human should confirm whether the position was actually closed off-system or is genuinely still open and unmanaged.

## 8. Best Candidates Ranked

1. **Long-watch: BANK/USDT** — trigger: 1h close back inside 0.2650–0.2764 with volume rising above the current 0.02x average; do not chase the existing 48% 24h move.
2. **Short-watch: XLK / QQQ / META (stocks)** — trigger: post-lunch RVOL clears the gate minimum + a failed retest of today's rebound high; do not enter into the current bounce.
3. **Catalyst-watch: HYPE/USDT** — trigger: clean pullback into structure while the perps_dex_narrative basket stays fresh (<24h); playbook explicitly says wait, not chase.
4. No clean actionable trade exists on either book this window — both crypto and stocks failed their own confirmation gates, which is functioning as designed given a chop/mixed tape.

## 9. Avoid / No Trade

This window only — never a command to stop the system:

- **UNH** — confirmed, expanding DOJ/Claritev antitrust probe. Avoid until resolved.
- **NVDA / AVGO shorts** — already self-invalidated by the system's fresher re-scan; do not treat the DB's `waiting_for_entry`/`triggered` status as live.
- **TSLA / GOOGL** — earnings July 22, avoid chasing or holding through regardless of the going_concern flag's accuracy.
- **NEAR/USDT short** — stale 3 days past expiry, weak historical short performance; not a fresh idea, needs manual review not a new entry.
- Scanning, candidate generation, tracking, and the scheduler continue uninterrupted — none of the above is a stop-the-system finding.

## 10. Main Risks

- Stocks-side signal staleness at scale: 28 of 50 "active" stocks signals are past expiry by up to 12 days, still shown `tp1_hit`/`tp2_hit` — risks an operator misreading system state if they don't cross-check `expires_at` manually.
- Two crypto signals (ALLO, NEAR) share the same staleness pattern, unresolved across two review cycles now.
- Catalyst mapping is trending worse (71.0% today vs 65.7% Sunday) — reduces confidence in catalyst-backed framing generally this week.
- Geopolitical macro (active US-Iran conflict) remains a live tail risk for crypto that internal technical trend labels (range/uptrend) don't fully price in.
- Mixed-signal regime on stocks (multi-day downtrend label vs single-day rebound) increases chase risk on both sides if an operator only reads the tier/score table without the underlying price action.
- Source ingest for this run failed (`sqlite3.OperationalError: database is locked` — scheduler actively writing at review time); the 7 cited external sources were written to `data/raw/enriched_review_sources/2026-07-20T1848.json` but not yet upserted into `news_items`. Not retried further per the read-mostly contract; a later cycle's own news collection will independently pick up matching headlines.

## 11. Action Plan — next 4 hours

- Do not chase NVDA/AVGO shorts; treat as closed/invalid regardless of DB status.
- Watch for post-lunch (US) confirmation on the tech-short basket (XLK/QQQ/META/TSLA/COIN/SMH) — only actionable if RVOL and sector-confirmation gates clear organically.
- Watch BANK/USDT and HYPE/USDT for volume/pullback confirmation per their own playbooks; no forced entries.
- Manually confirm the true status of NEAR/USDT (short) and ALLO/USDT — both display as active but are well past expiry.
- No new stocks swing/invest scan exists (18 days stale) — do not reference stocks swing/invest data until a fresh scan runs.
- Re-check ahead of the July 22 GOOGL/TSLA earnings prints; avoid new positioning into that window on those two names.

## 12. Final Verdict per Mode

- **Crypto scalp/intraday/swing:** no new trade this window. Manage existing 14 positions; escalate ALLO/NEAR staleness.
- **Stocks intraday:** no A/B actionable. 22 C-tier watchlist names correctly gated; treat NVDA/AVGO as stale/invalid, not merely low-conviction.
- **Stocks swing/invest:** no fresh data (18 days stale) — do not use for decisions this window.
- **Overall:** watch-only / wait-for-trigger across both books. Advisory only, no auto-trade.

## 13. Sources

- [US Stocks Rebound From Selloff as Nvidia, Other Chipmakers Rise — Bloomberg](https://www.bloomberg.com/news/articles/2026-07-20/us-stocks-rebound-from-selloff-as-nvidia-other-chipmakers-rise) (2026-07-20)
- [Chip Stocks Rally as AMD, Nvidia (NVDA), and Micron (MU) Surge Despite Recent Selloff — Blockonomi](https://blockonomi.com/chip-stocks-rally-as-amd-nvidia-nvda-and-micron-mu-surge-despite-recent-selloff/) (2026-07-20)
- [UnitedHealth (UNH) Faces Broader DOJ Antitrust Probe Into Claritev — Simply Wall St News](https://simplywall.st/stocks/us/healthcare/nyse-unh/unitedhealth-group/news/unitedhealth-unh-faces-broader-doj-antitrust-probe-into-clar/amp) (2026-07)
- [DOJ Expands Probe Into UnitedHealth's Prescription and Payment Practices — PYMNTS](https://www.pymnts.com/cpi-posts/doj-expands-probe-into-unitedhealths-prescription-and-payment-practices/) (2026-07)
- [UnitedHealth Group under DOJ investigation over Medicare billing practices — Medical Economics](https://www.medicaleconomics.com/view/unitedhealth-group-under-doj-investigation-over-medicare-billing-practices) (2026-07)
- [Trump declares US-Iran ceasefire over as Bitcoin slides toward $60K — CryptoBriefing](https://cryptobriefing.com/trump-iran-ceasefire-over-bitcoin-slides/) (2026-07-08)
- [The Iran Ceasefire Is Over. Which Cryptocurrencies Could See the Biggest Impact in 2026? — Yahoo Finance](https://finance.yahoo.com/markets/crypto/articles/iran-ceasefire-over-cryptocurrencies-could-092000263.html) (2026-07-11)
- Internal: `data/reports/intraday/2026-07-20_13-12_intraday_report.md`, `data/reports/swing/2026-07-20_14-30_swing_report.md`, `data/reports/stocks/intraday/2026-07-20_15-36_stocks_intraday_report.md`, `data/catalysts/2026-07-20/catalyst_cycle_13-17.md`, `proposed_signals` DB table.

## 14. Fix Requests / TODO

### TODO-stale-stocks-signals
- **issue:** 28 of 50 rows returned by `active-signals --asset-class stocks` are past their own `expires_at` (oldest 2026-07-08, 12 days stale) and still shown `tp1_hit`/`tp2_hit` as if running.
- **evidence:** `python -m src.cli active-signals --asset-class stocks` output this run — e.g. `sig_846c7bc6b3f1aab9` QQQ expires_at 2026-07-08T23:57:27, `sig_8dd73aed38f6c73f` MSFT expires_at 2026-07-09T22:31:41, still listed as active.
- **suggested manual fix:** audit the stocks-intraday expiry-sweep/close job (equivalent of whatever closes crypto signals at `expires_at`) — it appears not to run, or not to run for stocks.
- **priority:** high
- **first observed:** 2026-07-20 18:48 EEST (this run; likely pre-existing, not previously surfaced in an auto-review since stocks weren't open Sunday)

### TODO-nvda-avgo-stale-short-not-flagged
- **issue:** NVDA and AVGO stocks-short signals (created 14:16-14:21 UTC today) were re-scored by the system's own next scan ~75-80 minutes later to `no_directional_setup` (score 38), but the original signals remain `waiting_for_entry`/`triggered` in the DB with no cross-reference or auto-invalidation flag linking the two.
- **evidence:** `proposed_signals` rows `sig_e0fceb60a6327886` (NVDA, created 2026-07-20T14:21:02Z, score 87.47) and `sig_48899bb488411af9` (AVGO, created 2026-07-20T14:16:29Z, score 90.7) vs `data/reports/stocks/intraday/2026-07-20_15-36_stocks_intraday_report.md` §8 Rejected list showing NVDA/AVGO both at score 38.39, `no_directional_setup`.
- **suggested manual fix:** when a later same-day scan materially reverses a symbol's directional score for an already-active signal, either auto-close/invalidate the older signal or surface a explicit contradiction flag on it.
- **priority:** medium (no live risk — both were C-tier, never Telegram-pushed — but this is exactly the kind of thing an operator glancing at `active-signals` could misread)
- **first observed:** 2026-07-20 18:48 EEST

### TODO-tsla-going-concern-flag-audit
- **issue:** TSLA is gated with `legal_headline_risk: going_concern`, but external search this run found no going-concern warning, filing, or auditor disclosure for Tesla in 2026 — only unrelated analyst FCF-projection commentary.
- **evidence:** `data/reports/stocks/intraday/2026-07-20_15-36_stocks_intraday_report.md` line "TSLA (short) (was A): score 82 ... active legal/headline risk (going_concern)"; WebSearch "Tesla going concern warning July 2026" returned no corroborating result.
- **suggested manual fix:** trace where the `going_concern` tag for TSLA originates (likely a static/config-driven legal-risk flag list rather than a fresh news detection) and confirm it's not a stale or mislabeled entry.
- **priority:** low (doesn't change the operator conclusion — TSLA is separately blocked by the July 22 earnings blackout — but worth cleaning up since it's a credibility issue for the legal-risk gate)
- **first observed:** 2026-07-20 18:48 EEST

### TODO-near-allo-persisted-staleness (carried forward)
- **issue:** NEAR/USDT (short) and ALLO/USDT (long) remain past-expiry and shown active across at least two consecutive review cycles (Sunday 21:53 and this run) with no resolution.
- **evidence:** `sig_b16bb9e54598333a` NEAR/USDT expires_at 2026-07-17T15:56:12 (3 days stale); `sig_10088a4c71cae845` ALLO/USDT expires_at 2026-07-19T15:21:04 (~1.3 days stale). First flagged in `OPUS_ENRICHED_REVIEW_AUTO_2026-07-19_2153.md`.
- **suggested manual fix:** same root cause as TODO-stale-stocks-signals but on the crypto side — confirm whether an expiry-sweep job exists at all, or only closes on TP/SL hit and never on time-based expiry.
- **priority:** high (now confirmed persisting across multiple review windows without remediation)
- **first observed:** 2026-07-19 21:53 EEST (this run: still unresolved as of 2026-07-20 18:48 EEST)
