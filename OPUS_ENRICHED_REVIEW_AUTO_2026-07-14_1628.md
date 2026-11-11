# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:28 EEST

## 1. Executive Summary

Advisory only / no auto-trade. **Pre-US-open decision review** (~2 min before/at the 16:30 EEST / 09:30 ET cash open). Crypto stays **risk-off**: BTC transition_down, fresh Iran/Strait-of-Hormuz escalation (4th round of US strikes, Iran hit two tankers), BTC ~$62.6–63k, long-liquidation-heavy ($62.6M longs vs $10.5M shorts, 6:1). Offsetting: June CPI printed soft (0.4% MoM decline, YoY 3.5% vs 3.8% est.) — a genuine bullish cross-current for risk assets into the open. Stocks regime is **chop** (VIX 17.4, breadth 50%/100%), **zero A/B-tier stocks setups actionable** — every raw A/B stock candidate is gate-demoted to C solely for `market_closed_intraday_planning_only`, so re-evaluate all of them fresh at/after 09:30 ET. JPMorgan (JPM) beat Q2 EPS big ($6.14 vs $5.59 est., record profit) but traded ~2% lower pre-market — a "sell-the-news" signal worth tracking at the open, though JPM itself is not a scored candidate today (earnings-day block). Two live contradiction risks carried from the prior cycle: **AVGO** (internal signal short vs. confirmed $30B Apple chip deal, bullish) and **UNH** (internal long vs. active DOJ/Medicare-billing legal flag) — both stay AVOID/MANUAL REVIEW. Catalyst mapping is weak this run (84.6% unmapped) — treat catalyst layer as context only. Scanning, tracking, and the paper book continue uninterrupted in all moods.

## 2. Data Used

- Crypto reports: scalp (09:18 gen / 12:18 mtime), intraday (09:23 gen / 12:23 mtime), swing (02:15 gen / 05:15 mtime — **carry-forward**, ~11h old at time of this review)
- Stocks reports: intraday (12:20 gen, "after-hours (UTC overnight)" session flag — market-closed demotion active)
- Stocks swing/invest reports: **2026-07-02** — **stale (>14h, actually ~12 days)**, excluded from final verdict; position-framework for stocks swing/invest is deprecated per prior desk decision, no fresher source exists
- `data/catalysts/2026-07-14/catalyst_events.jsonl` (2,999 events today), `narrative_baskets.jsonl` (4 baskets)
- `data/processed/llm_analysis_packet.md` (mtime 13:03), `data/processed/llm_stocks_packet.md` (mtime 15:21)
- CLI: `active-signals --asset-class crypto` (21 rows), `active-signals --asset-class stocks` (29 rows), `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`, `detect_untracked_legacy_alerts --since 2026-07-14` (clean)
- External: WebSearch ×4 (AVGO/Apple deal, NVDA China chip screening, JPM earnings, BTC/Iran macro) + WebFetch ×1 (CoinDesk live-updates page) — all resolved successfully

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime 15:25 EEST, latest `cycle_01_13-37_summary.md` mtime 15:25 EEST — both **well under 3h**, no defer needed.
- Latest cycle (13:37 start / 15:25 finish) shows all paper-only pipeline steps green: paper execution accounting refresh (2,493/2,493, 0 errors), paper structural TP/stop refresh, paper entry-mode classify, paper stock-direction, paper-shadow A/B execution — all exit=0, no live-path touched.
- Swing report is a **carry-forward** (~11h old) — flagged; TAO/USDT thesis below is read from it but cross-checked against live `active-signals`.
- Stocks swing/invest reports are **stale** (~12 days) — excluded, used only as long-horizon context.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-14 16:28 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale", "derivatives_sparse"],
      "data_missing": ["stocks swing/invest >12d old, excluded", "on-chain flow feeds not live"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log/cycle mtime 15:25", "stocks swing/invest mtime 2026-07-02", "OI n/a on many fallback_via_mexc rows"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["risk_off", "mixed", "chop", "shorts_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC trend transition_down, ETH uptrend divergence, altcoin breadth 27-29% above EMA20", "stocks regime label=chop, VIX 17.42, breadth 50%/100%", "soft June CPI vs Iran/oil escalation cross-current"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "catalyst_contradicted", "fresh_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["84.6% of today's 2,999 catalyst_events unmapped to a symbol", "AVGO: internal short vs confirmed $30B Apple deal (bullish)", "NVDA: fresh multi-outlet China chip-screening story", "VELVET in fresh <1h momentum_breakout basket"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "oi_supports", "data_unavailable"],
      "data_missing": ["OI 24h % n/a for most non-BTC/ETH/NEAR/TRX symbols (fallback_via_mexc)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["TAO/USDT: price down + OI up 8.06% = fresh shorts pressing, squeeze risk on reclaim >201.44", "VELVET/USDT: price up + OI up 5.36% = fresh positioning confirms trend"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["entry_late", "chase_risk", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TAO/USDT already tp1_hit, not a fresh entry", "VELVET/USDT current 0.6160 vs conditional pullback zone 0.5968-0.6101 — sitting above the entry zone, not yet a clean retest"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["open_actionable", "review_shadow"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["21 crypto B-tier active signals, all progressing (18 tp1_hit / 3 tp2_hit), none waiting/expired", "29 stocks C-tier active signals (tp1/tp2_hit/triggered), watchlist/research only, none actionable"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["legal_risk", "headline_risk", "reduce_risk", "correlation_cluster"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: active DOJ/Medicare-billing investigation, gate gives legal_headline_risk: sec_doj", "GOOGL: Swiss antitrust probe over Android search defaults (headline risk, moderate)", "JPM earnings today — do_not_chase_warning already active", "geopolitical: Iran strikes/Strait of Hormuz feeding BTC and macro risk", "20 active crypto swing longs concentrated in altcoins against a risk-off BTC tape = correlation cluster"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto direction=short: PF 0.50, avgR -0.083, n=20 — weak", "crypto setup=pullback: PF 1.39, n=122 — reliable/working", "stocks tier=C: winrate 10%, PF 0.79, n=204 — weak", "stocks sector=semiconductors: PF 0.51, n=28 — weak (supports short bias narrowly)"] },
    { "agent": "head_trader", "verdict": "manual_review",
      "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "VELVET/USDT", "trigger": "hold-and-retest of 0.5968-0.6101 pullback zone, do not chase current 0.6160", "reason": "RS-leader +17.4% vs BTC, fresh OI+price confirmation, primary in fresh <1h momentum_breakout basket" },
    "best_short_candidate":    { "symbol": "TAO/USDT", "trigger": "already active (tp1_hit); fresh re-entry only on a new failed-bounce retest into 198.99-200.09, invalidate above 201.44", "reason": "aligned with risk-off regime and failed-bounce playbook, but OI rising into a falling price = squeeze risk on reclaim; short direction historically weak (PF 0.50)" },
    "best_catalyst_candidate": { "symbol": "NVDA", "trigger": "clean directional score (currently no_trade 42.6) plus a defined technical level with volume confirmation after the open", "reason": "fresh, multi-outlet-confirmed China AI-chip export-screening story (Nvidia halved its Asian buyer whitelist) — real but not yet a scoreable directional edge" },
    "avoid_candidate":         { "symbol": "AVGO", "reason": "internal signal is SHORT (raw B, score 79.5) but external news is strongly bullish and confirmed (Apple's >$30B multi-year chip deal through 2031, stock +4% on the news) — genuine catalyst-vs-technical contradiction" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.75 | scheduler_fresh, report_stale, derivatives_sparse | advisory_only |
| market_regime | caution | 0.70 | risk_off, mixed, chop, shorts_preferred | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, catalyst_contradicted, fresh_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | entry_late, chase_risk, clean_retest | advisory_only |
| execution_lifecycle | ok | 0.80 | open_actionable, review_shadow | advisory_only |
| risk_manager | caution | 0.70 | legal_risk, headline_risk, reduce_risk, correlation_cluster | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | manual_review | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-07-14_1139.md` (11:39 EEST, Europe/pre-US slot):

- **TAO/USDT short** — unchanged as best short idea, but has since **tp1_hit** (was flagged at entry zone 198.99-200.09 in that review; now already partially resolved, running toward TP2 196.05/TP3 191.15). Squeeze-risk caveat (OI up, price down) persists.
- **VELVET/USDT long** — unchanged as best long idea. Still RS-leader (+17.4% vs BTC, was +14-17% before), still extended above its conditional pullback zone; thesis stands, still "wait for hold-and-retest, do not chase."
- **NVDA catalyst-watch** — unchanged; the China AI-chip-screening story is the same story, now further confirmed by additional outlets (Benzinga, Seeking Alpha, GuruFocus) publishing the same "halved Asian buyer list" figure. Still no_trade technically (42.6).
- **AVGO avoid** — unchanged and now independently re-verified via WebSearch: Apple's $30B Broadcom chip deal (through 2031) is confirmed, not speculative. Contradiction still live.
- **UNH** — unchanged: DOJ/Medicare legal flag still active; existing UNH C-tier positions (intraday tp2_hit score 71.6, invest triggered score 70.1) still predate the gate and still warrant a manual look.
- **New this cycle**: JPM reported Q2 earnings (record profit, EPS beat) but traded ~2% lower pre-market — a fresh "sell-the-news" data point not present in the 11:39 review (JPM earnings were still pending then).
- **New this cycle**: fresh Iran/Strait-of-Hormuz escalation (4th round of US strikes, Iranian strikes on tankers) plus a surprisingly soft June CPI print — both post-date the 11:39 review and create the mixed macro backdrop for the open.

## 5. Catalyst Coverage

- Total `catalyst_events` today: **2,999**. Mapped (non-null symbol): **461**. Unmapped: **2,538** (**84.6%**).
- `narrative_baskets`: **4** — perps_dex_narrative (primary HYPE/USDT), binance_ecosystem_teaser (primary BNB/USDT), delisting_thin_liquidity (primary —), momentum_breakout (primary ZBT/USDT, SXT/USDT, VELVET/USDT, fresh <1h).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (representative sample): "MEHR SAYS SEVERAL AREAS IN SOUTHWESTERN IRAN'S KHUZESTAN'S OMIDIYEH HIT BY U.S. PROJECTILES" (@WalterBloomberg); "EMBC Investors Have Opportunity to Lead Embecta Corp. Securities Fraud Lawsuit"; "US investigates possible Iranian drone storage in Cuba, Trump says."

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **risk-off** (BTC transition_down, altcoin breadth 27-29% above EMA20/EMA50, desk style = "short bias or no trade; avoid weak altcoin longs"). Fresh geopolitical escalation (Iran/Strait of Hormuz, 4th round of US strikes) is the dominant near-term driver; BTC long-liquidations outweigh shorts 6:1 in the last 24h.
- Stocks mood: **chop / market-closed-pending-open** (VIX 17.42, breadth 50% above EMA20 / 100% above EMA50; label "chop"; every raw A/B candidate demoted to C purely for `market_closed_intraday_planning_only` — re-evaluate all at 09:30 ET). Sector rotation: financials and healthcare strongest (RS +5.0%/+3.2% vs SPY), semiconductors and consumer discretionary weakest (RS -5.5%/-2.8%).
- Dominant narrative: crypto — geopolitical risk-off vs. a surprisingly soft CPI print (cross-currents, not a clean trend); stocks — big-bank earnings day (JPM beat but sold off pre-market) plus an AI-chip supply-chain story cutting both ways (NVDA negative export-screening headline vs. AVGO positive $30B Apple deal).
- Preferred side now: **mixed / wait-for-trigger** — crypto leans short-only-with-confirmation, stocks require RTH confirmation before treating anything as actionable.
- Best long candidate: VELVET/USDT (wait for pullback hold — see §8).
- Best short candidate: TAO/USDT (existing tp1_hit position; fresh re-entry only on a new failed-bounce retest — see §8).
- Best catalyst-backed candidate: NVDA (China chip-screening story, not yet a clean directional trade).
- What to avoid: AVGO short (catalyst-vs-technical contradiction); UNH long exposure without a legal-risk review; chasing JPM either direction around the earnings "sell-the-news" reaction; chasing SMH/semis broadly off the NVDA headline without a confirmed retest.
- What would change the view: a clean break/hold of BTC's local range post-CPI, a de-escalation or re-escalation headline out of the Strait of Hormuz, or the first 15-30 min of RTH price action confirming (or invalidating) the stocks Top-Candidates list above.

## 7. Candidate Deep Dives

### AVGO (Broadcom) — short (raw B, 79.53) → demoted to C (market-closed) — AVOID / MANUAL REVIEW
- Has price already reacted to the catalyst? Yes — Broadcom rose >4% on July 8 when the $30B Apple multi-year chip deal (through 2031) was announced; the move is not fresh but the underlying support (~20% of AVGO revenue tied to Apple, deal removes in-house-chip-defection risk) is durable, not a one-day pop.
- Is the setup chasing? A short here would be fighting a confirmed, structurally bullish catalyst — high risk of chasing into strength.
- Retest / pullback structure? Not evaluated — TradingView / manual chart check unavailable; only local OHLCV/ATR/EMA fields used, none fabricated.
- Overextended (>2 ATR from EMA20)? Not computable from available fields.
- Would entry now be late? Yes, for the short thesis specifically, given the bullish catalyst.
- Level that makes it actionable? None while the internal short and the external bullish catalyst remain in direct conflict — needs a scoring/thesis reconciliation, not a price trigger.
- Aligned with market mood? No — semis sector is weak overall (RS -5.5%), but AVGO's company-specific catalyst overrides the sector-level short bias.
- Long, short, or wait? Wait / avoid.
- Actionable now or after confirmation? Neither — flagged for manual review, not a trigger-based setup.
- What would invalidate the idea? A reconciled desk view (either the short thesis is dropped, or a confirmed negative company-specific catalyst emerges to justify it).
- Chase-risk setup? Yes.
- Catalyst confirmation or contradiction? **Contradiction** — internal technical short vs. externally confirmed bullish fundamental catalyst.

### UNH (UnitedHealth) — long (raw A, 82.84) → demoted to C (legal_headline_risk: sec_doj) — AVOID / MANUAL REVIEW
- Has price already reacted? Not verified without a fresh external check this cycle; internal gate already applied the legal flag from a prior cycle's verified DOJ/Medicare-billing investigation (open, no indictment).
- Is the setup chasing? Not applicable — gated before entry consideration.
- Retest structure? Not evaluated (chart tools unavailable).
- Overextended? Not computable.
- Would entry now be late? The desk's own new-signal gate already blocks this from becoming a fresh A/B; the open question is the two **existing** UNH positions in `active-signals` (intraday C tp2_hit score 71.6; invest C triggered score 70.1) that predate the flag.
- Level that makes it actionable? N/A while the legal flag is active.
- Aligned with market mood? Healthcare is the second-strongest sector (RS +3.2%), but company-specific legal risk overrides sector strength.
- Long, short, or wait? Wait / manual review of existing exposure.
- Actionable now or after confirmation? Manual review required regardless of confirmation — this is a legal-risk gate, not a technical-confirmation gate.
- What would invalidate the idea (i.e., clear the flag)? Resolution or dismissal of the DOJ investigation, or an official statement materially reducing its scope.
- Chase-risk? N/A.
- Catalyst confirmation/contradiction? Confirmation of an ongoing legal risk (per §I discipline) — final verdict stays AVOID/MANUAL REVIEW, never a clean actionable.

### TAO/USDT — swing short (B-tier, 65.3, already tp1_hit) — MONITOR / re-entry only on fresh retest
- Has price already reacted to the catalyst? No fresh verified catalyst for TAO; this is a pure technical failed-bounce/regime trade, already progressed to TP1.
- Is the setup chasing? Not for the existing position (already entered at 198.99-200.09, now managing toward TP2 196.05/TP3 191.15). A brand-new short here would need a fresh retest — do not chase the move already made.
- Retest / pullback structure? Original entry was a failed-bounce retest; a new entry requires the same pattern to repeat, not a market order at current levels.
- Overextended? Not computable from available fields; ATR 2.45 vs current-at-report price 198.50.
- Would entry now be late? For a fresh position, likely yes unless a new retest forms.
- Level that makes a new entry actionable? A fresh 1h failed-bounce back into the 198.99-200.09 zone; invalidation above 201.44.
- Aligned with market mood? Yes — risk-off crypto, short-bias regime.
- Long, short, or wait? Short (existing), wait for fresh confirmation on any add.
- Actionable now or after confirmation? The existing position is live/actionable to manage; a new entry needs confirmation.
- What would invalidate? 1h close beyond 201.44, or BTC/ETH reclaiming local structure against the regime thesis.
- Chase-risk? Yes, for any fresh entry at current levels.
- Catalyst confirmation/contradiction? No catalyst either way — pure technical/regime trade. Caution: derivatives show OI +8.06% while price is down (fresh shorts pressing) — squeeze risk if BTC/ETH reclaim; historically, crypto short-direction signals are weak overall (PF 0.50, n=20) — treat any add with reduced size.

### VELVET/USDT — swing long (watchlist, 57.3, actionable-as-watch) — WAIT FOR PULLBACK, DO NOT CHASE
- Has price already reacted to the catalyst? No fresh verified catalyst; this is a pure RS/momentum trade (24h +16%, 7d +29.6%, RS vs BTC +17.4%).
- Is the setup chasing? At current price (0.6160, per the 02:15 carry-forward report) it is above the conditional pullback entry zone (0.5968-0.6101) — chasing here would be late.
- Retest / pullback structure? Entry plan explicitly requires a hold-and-retest into 0.5968-0.6101; not yet confirmed.
- Overextended? Volume ratio is only 0.09x of the 20-period average despite the price move — the rally is not backed by strong current volume, a caution flag on chase risk.
- Would entry now be late? Yes at current levels.
- Level that makes it actionable? A confirmed hold of the 0.5968-0.6101 zone with volume pickup; invalidate below 0.5806.
- Aligned with market mood? It is a counter-tape long (RS-leader against a bearish BTC regime) — the desk's own counter-thesis explicitly flags "reduce size" for this reason.
- Long, short, or wait? Long, but wait for the retest.
- Actionable now or after confirmation? After confirmation only.
- What would invalidate? A 1h close below 0.5806, or a broader BTC breakdown dragging the whole complex down regardless of RS.
- Chase-risk? Yes at current price.
- Catalyst confirmation/contradiction? No catalyst; supported only by the `momentum_breakout` narrative basket (fresh <1h, source single_source — not yet independently verified).

### NVDA — no_trade (score 42.6) — CATALYST-WATCH ONLY
- Has price already reacted to the catalyst? Partially — the "halved Asian AI-chip buyer list" story has been building for several days (whitelist introduced amid tightening China-related export screening); today's coverage (Benzinga, Seeking Alpha, GuruFocus, Asia Business Daily) confirms and extends it, all citing the same figure (more than half of prior Asian customers excluded in Singapore/Malaysia/Japan).
- Is the setup chasing? No directional setup exists yet — nothing to chase.
- Retest / pullback structure? Not evaluated; chart tools unavailable.
- Overextended? Not computable.
- Would entry now be late? N/A, no trigger yet.
- Level that makes it actionable? A technical score upgrade to B/A plus a defined level with volume confirmation once RTH opens and the market has a chance to price the headline.
- Aligned with market mood? It reinforces the semis-sector weakness already visible in the sector-rotation data (RS -5.5%), but as company-specific revenue-impact uncertainty, not yet a scored edge.
- Long, short, or wait? Wait-for-trigger.
- Actionable now or after confirmation? After confirmation only.
- What would invalidate the catalyst thesis? Clarification that the buyer-list tightening is a compliance formality with negligible revenue impact, or a stronger-than-expected guidance offsetting the headline.
- Chase-risk? Not applicable (no entry yet).
- Catalyst confirmation/contradiction? **Confirmed and reinforced** — multiple independent outlets, consistent figures, no contradicting reports found.

## 8. Best Candidates Ranked

1. **VELVET/USDT — best long-watch.** Trigger: hold-and-retest confirmed inside 0.5968-0.6101 with a volume pickup; invalidate below 0.5806.
2. **TAO/USDT — best short (existing, monitor); best short-watch for a fresh add.** Existing position managing toward TP2 196.05/TP3 191.15. Fresh-entry trigger: a new 1h failed-bounce retest into 198.99-200.09; invalidate above 201.44.
3. **NVDA — best catalyst-watch.** Trigger: technical score upgrade to B/A with a defined level and volume confirmation once RTH opens.
4. **AVGO — avoid / manual review.** No actionable trigger while internal short and external bullish catalyst conflict.
5. **UNH — avoid / manual review** for existing exposure; new entries already blocked by the desk's own gate.

## 9. Avoid / No Trade (this decision window only)

- **AVGO short** — catalyst-vs-technical contradiction (see §7). Not a system-wide stop; re-evaluate once the thesis conflict is reconciled or a fresh confirming/contradicting data point appears.
- **UNH long** — active legal/headline risk; existing exposure needs a human look, new entries already gated.
- **Chasing JPM** either direction around today's earnings "sell-the-news" reaction — record profit beat, ~2% pre-market decline, classic expectations-priced-in pattern; wait for the open to see if the gap holds or fills.
- **Chasing VELVET/TAO at current levels** without the specific retest/confirmation described above.
- This is a decision-window-only call — scanning, tracking, candidate generation, and outcome recording continue in all cases; nothing here is a command to pause any part of the system.

## 10. Main Risks

- Geopolitical: 4th round of US strikes on Iran in six days; Iran struck two tankers in the Strait of Hormuz; Brent crude ~$85 (2nd straight up day) — feeding both crypto risk-off and a broad equity-macro risk premium into the open.
- Offsetting macro: June CPI printed soft (0.4% MoM decline, YoY 3.5% vs 3.8% expected) — a bullish cross-current that could support a relief bid in risk assets if the geopolitical news doesn't worsen further.
- Earnings-day gap risk: JPM (and other big banks per CNBC's live coverage) reporting today; financials is the strongest sector (RS +5.0%) but JPM itself traded down pre-market despite a beat — a reminder that "beat + sell-off" gaps can whipsaw early RTH price action.
- Catalyst-mapping is weak this run (84.6% unmapped) — treat the catalyst layer as context only, not as a standalone decision input, until mapping recovers.
- Concentration: 20 of 21 active crypto signals are swing longs in altcoins while the BTC regime itself is risk-off/transition_down — a correlation cluster that could unwind together on a BTC leg down.
- Historically weak buckets to lean against: crypto short-direction signals (PF 0.50, n=20), stocks C-tier overall (winrate 10%, PF 0.79, n=204), stocks semiconductors/consumer-discretionary sectors (PF ~0.5).

## 11. Action Plan — next 4 hours

- At the 09:30 ET / 16:30 EEST open: re-run the stocks intraday scan and re-check the Top-Candidates table (AAPL, UNH, META, SMH, AMZN, AVGO, GOOGL, XLF, QQQ, AMD, XOM, COIN, TSLA, XLE, SMCI) for which survive the market-closed demotion once real RTH data replaces after-hours data — require the first 15-30 min for confirmation before treating any as actionable, per slot guidance.
- Watch VELVET/USDT for a hold-and-retest into 0.5968-0.6101; do not chase current levels.
- Monitor TAO/USDT toward TP2 196.05; only add on a fresh 1h failed-bounce retest into 198.99-200.09, invalidate above 201.44.
- Track NVDA for any technical-score upgrade following continued China-chip-screening coverage; do not treat the headline alone as a trigger.
- Keep AVGO and UNH on manual-review status; re-check both once RTH price action gives fresh confirming/contradicting signal.
- Watch JPM's open for whether the pre-market ~2% gap-down holds, fills, or extends — informative for financials-sector positioning generally, even though JPM itself is not a scored candidate today.
- Continue monitoring the Iran/Strait-of-Hormuz headline flow and BTC's reaction to it as the dominant crypto-mood driver into the US session.

## 12. Final Verdict per Mode

- **Crypto scalp**: No A-tier, no B-tier. No trade.
- **Crypto intraday**: No A-tier, no B-tier. C-tier watchlist only (SYN, DEXE, TRUMP, XLM, XEC, TRX, GRAM, ZBT) — none actionable.
- **Crypto swing**: No A-tier. One B-tier (TAO/USDT short, already tp1_hit) — monitor/manage existing, fresh adds need retest confirmation. C-tier watchlist includes VELVET/USDT (best long-watch).
- **Stocks intraday**: No A/B-tier actionable — market-closed demotion in effect on every raw A/B candidate. Re-evaluate all at/after the 09:30 ET open with RTH confirmation.
- **Stocks swing/invest**: Stale data (>12 days) / framework deprecated — no verdict, carry-forward context only.
- **Overall**: CAUTION, routed by side — not a blanket no-trade. Manual review flagged for AVGO and UNH.

## 13. Sources

- [Apple Announces $30 billion Multi-year Chip Deal With Broadcom (AVGO) — Yahoo Finance](https://finance.yahoo.com/technology/articles/apple-announces-30-billion-multi-065814718.html) (2026-07-08/09)
- [Broadcom (AVGO) Secures $30 Billion Chip Supply Deal with Apple — GuruFocus](https://www.gurufocus.com/news/8950100/broadcom-avgo-secures-30-billion-chip-supply-deal-with-apple) (2026-07-08/09)
- [Apple (AAPL) Chip Deal With Broadcom (AVGO) Expected to Exceed $30 Billion — Bloomberg](https://www.bloomberg.com/news/articles/2026-07-08/apple-aapl-chip-deal-with-broadcom-avgo-expected-to-exceed-30-billion) (2026-07-08)
- [Nvidia Reportedly Cuts More Than Half of Its Asian AI Chip Customers Amid Tighter China Screening — Benzinga](https://www.benzinga.com/markets/tech/26/07/60433026/nvidia-reportedly-cuts-more-than-half-of-its-asian-ai-chip-customers-amid-tighter-china-screening) (2026-07-14)
- [Nvidia halves Asian AI chip buyer list amid tighter China screening — Seeking Alpha](https://seekingalpha.com/news/4613408-nvidia-halves-asian-ai-chip-buyer-list-amid-tighter-china-screening---report) (2026-07-14)
- [Nvidia (NVDA) Tightens AI Chip Sales with New Customer Restrictions — GuruFocus](https://www.gurufocus.com/news/8956976/nvidia-nvda-tightens-ai-chip-sales-with-new-customer-restrictions) (2026-07-14)
- [Bank earnings live updates: JPMorgan and Bank of America calls are underway — CNBC](https://www.cnbc.com/2026/07/14/jpm-bank-of-america-citi-bank-earnings-live-updates.html) (2026-07-14)
- [JPMorgan Earnings: Record Profit on $6 Billion Stock-Trading Haul — Bloomberg](https://www.bloomberg.com/news/articles/2026-07-14/jpmorgan-notches-record-profit-on-6-billion-stock-trading-haul) (2026-07-14)
- [Live updates: Bitcoin holds $62,600 as the Iran conflict reignites and CPI looms — CoinDesk](https://www.coindesk.com/business/2026/07/14/live-updates-bitcoin-holds-usd62-600-as-the-iran-conflict-reignites-and-cpi-looms) (2026-07-14, fetched directly)
- [U.S.-Iran escalation weighs on bitcoin (BTC) price, stocks as oil climbs: Crypto Daily — CoinDesk](https://www.coindesk.com/daybook-us/2026/07/14/u-s-iran-escalation-weighs-on-bitcoin-stocks-as-oil-climbs) (2026-07-14)
- Internal: `data/reports/scalp/2026-07-14_09-18_scalp_report.md`, `data/reports/intraday/2026-07-14_09-23_intraday_report.md`, `data/reports/swing/2026-07-14_02-15_swing_report.md`, `data/reports/stocks/intraday/2026-07-14_12-20_stocks_intraday_report.md`, `data/catalysts/2026-07-14/catalyst_events.jsonl`, `data/catalysts/2026-07-14/narrative_baskets.jsonl`

## 14. Fix Requests / TODO

### TODO-catalyst-mapping-weak
- **issue:** Catalyst-event → symbol mapping is at 84.6% unmapped for today's cycle (2,538 of 2,999 events have no `symbol`), well above the 50% weak-mapping threshold, and this has recurred across multiple recent auto-review cycles.
- **evidence:** `data/catalysts/2026-07-14/catalyst_events.jsonl` — 461 mapped / 2,999 total; sampled unmapped headlines include clearly symbol-relevant items (e.g. securities-fraud-lawsuit press releases naming specific tickers in the title text) that the resolver failed to attach.
- **suggested manual fix:** Revisit the symbol resolver in the catalyst layer (ticker/company-name extraction from title text, especially for the recurring "Investors Have Opportunity to Lead ... Securities Fraud Lawsuit" PR-Newswire template, which reliably contains a ticker but is landing unmapped).
- **priority:** medium
- **first observed:** 2026-07-14 11:39 EEST (prior review cycle); still present 2026-07-14 16:28 EEST.

### TODO-unh-legacy-signal-gate
- **issue:** The `legal_headline_risk: sec_doj` gate correctly blocks *new* UNH A/B signals, but two existing UNH entries in `active-signals` (intraday C, score 71.6, tp2_hit; invest C, score 70.1, triggered) predate the flag and are not retroactively tagged for manual review inside the active-signals output itself — an operator has to cross-reference the reports to know they carry legal risk.
- **evidence:** `python -m src.cli active-signals --asset-class stocks` rows `sig_ac77abec6ae23236` (UNH intraday) and `sig_90b50ceef0d1ebd3` (UNH invest); legal flag documented in `data/reports/stocks/intraday/2026-07-14_12-20_stocks_intraday_report.md` line 171.
- **suggested manual fix:** Consider surfacing an active legal/headline-risk badge directly in `active-signals` output for any open position whose symbol currently carries a gate flag, regardless of when the position was opened.
- **priority:** low
- **first observed:** 2026-07-14 11:39 EEST (prior review cycle); still present 2026-07-14 16:28 EEST.
