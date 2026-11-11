# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:40 EEST

## 1. Executive Summary

**Slot: crypto overnight / Asia review (advisory only / no auto-trade).** Saturday overnight — US stocks are closed all day (weekend), so this cycle is crypto-actionable / stocks-planning-only. Scheduler is fresh (`scheduler.log` 04:38 EEST, ~2m old) — no defer. Freshest crypto reads (scalp/intraday, both ~04:16-04:26 EEST) show **market regime: transition (mixed)** — BTC and ETH both trend "range", altcoin breadth only 33.3%/56.3% above EMA20/50. Macro/geopolitics risk holds at **100/100** (Iran war oil-economics, Strait of Hormuz VLCC rates, Russia drone strikes on fuel infrastructure) — a risk-off headwind unchanged from the last several cycles. Despite the mixed/range regime, the **entire active crypto book (53 live B-tier rows) is long-only** — zero shorts, zero A-tier — and most of these signals were originally scored when the desk still classified the market as "bullish trend" (created Aug 22-28); the regime has since drifted to mixed without the book being re-screened, a genuine staleness risk worth flagging. Weekly headline actionable performance: **PF 1.141, winrate 10.6% (42W/133L of 395 triggered), totalR +11.7R** — thin edge, consistent with the desk's known small-winrate/tail-driven structure. **TUT/USDT and ONG/USDT open swing longs remain unresolved bias contradictions for a 5th+ consecutive review cycle** (first flagged 2026-08-28 18:39 EEST, ONG originally 2026-08-08) — both still `status=triggered` against invalidations that the reports' own bias tags say should be breached (TUT -20.47% 24h vs entry, ONG -15.12%); this is now overnight-into-Asia priority for operator/monitor resolution. On the positive side, `detect_untracked_legacy_alerts` shows **zero** new untracked crypto alerts today (2026-08-29) — an improvement vs the recurring 4/day pattern from prior cycles, though the underlying bug is not confirmed fixed, only quiet. Catalyst mapping remains weak: **69.0% unmapped** (345/500 events), flat vs yesterday's ~70.9%. Stocks: fully closed (Saturday); no active A/B stocks positions — Friday's VRT (Pomerantz legal-risk short), CRCL, LLY, COST all resolved `missed_no_entry`/`stale_before_entry`/`expired` without ever triggering, so no open contradicted stocks exposure carries into the weekend. Scanning, tracking, and the scheduler continue overnight into Europe regardless of this window's verdict.

## 2. Data Used

- Crypto scalp report: `data/reports/scalp/2026-08-29_01-16_scalp_report.md` (04:16 EEST, ~24m old — **freshest**)
- Crypto intraday report: `data/reports/intraday/2026-08-29_01-26_intraday_report.md` (04:26 EEST, ~14m old — **freshest**)
- Crypto swing report: `data/reports/swing/2026-08-28_19-37_swing_report.md` (22:37 EEST, ~6h old — **carry-forward**, still the source for the TUT/ONG bias-tag evidence since no fresher swing scan has run)
- Stocks intraday report: `data/reports/stocks/intraday/2026-08-28_18-54_stocks_intraday_report.md` (21:54 EEST, ~6h45m old — market closed all weekend, planning-only)
- Stocks swing/invest reports: both dated 2026-07-02 (deprecated pipeline per `project_crypto_ai_desk_stocks_position_framework` memory — excluded)
- `data/processed/llm_analysis_packet.md` (04:29 EEST, fresh), `data/processed/llm_stocks_packet.md` (21:56 EEST Aug 28)
- `data/catalysts/2026-08-29/catalyst_events.jsonl` (500 rows, direct-counted: 155 mapped/345 unmapped), `narrative_baskets.jsonl` (4 baskets), `catalyst_cycle_01-34.md`
- CLI: `active-signals --asset-class crypto` (50 rows), `active-signals --asset-class stocks` (50 rows), `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`, `detect_untracked_legacy_alerts --since 2026-08-29`
- Direct read-only SQL against `db/crypto_ai_desk.sqlite`: `proposed_signals` (full active crypto book, 53 rows; stocks book last 24h), `signal_outcomes` (recent resolutions), `watchlist_alerts` (tier-upgrade history), `news_items` (ONG catalyst check — none found)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-28_2331.md` (post-close final daily review, 23:31 EEST)
- **External web research not used this run** — internal reports, catalyst layer, and news_items were sufficient and internally consistent for every candidate reviewed; no candidate's verdict depended on unverified external claims.
- **TradingView / manual chart check unavailable** — all technical reads taken directly from report-stated OHLCV/ATR/EMA/RS/funding/OI fields.

## 3. Scheduler / Data Freshness

- `scheduler.log`: 2026-08-29 04:38 EEST (~2m old) — **fresh**.
- Latest `cycle_*_summary.md`: `cycle_03_00-57` (written 02:04 EEST) — ~2h36m old; scheduler.log itself is fresh so no defer per the "both stale" rule.
- Crypto scalp: 04:16 EEST (~24m) — **fresh**.
- Crypto intraday: 04:26 EEST (~14m) — **fresh**.
- Crypto swing: 22:37 EEST (~6h) — **carry-forward** (4-12h band); regime/breadth figures reused from scalp/intraday freshest reads instead where available, but TUT/ONG bias-tag detail only exists in this swing report.
- Stocks intraday: 21:54 EEST (~6h45m) — carry-forward; market closed all weekend regardless, planning-only.
- Stocks swing/invest: 2026-07-02 — stale/deprecated, excluded.
- No monitor-process-uptime file was read this run (not in the allowed CLI/read list).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-08-29 04:40 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["swing report ~6h old, only source for TUT/ONG bias-tag evidence"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 04:38 EEST", "scalp/intraday reports both <30m old", "swing report 22:37 EEST is 6h old (carry-forward band)"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["mixed", "chop", "risk_off", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["market regime: transition (mixed); BTC trend range, ETH trend range", "altcoin breadth 33.3%/56.3% above EMA20/50", "macro/geopolitics risk 100/100, risk-off headwind (Iran war, VLCC rates, Russia fuel-infra strikes)", "active book is 100% long despite mixed regime"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported", "fresh_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["69.0% unmapped in catalyst_events.jsonl (345/500), flat vs yesterday's 70.9%", "SOL/USDT has a fresh primary-ish catalyst (DeFi Development 'State of Solana' platform, The Block) but tagged weak_vs_market momentum", "zero active crypto signals carry news_supported=1", "ONG/USDT has no news_items match in the last 4 days — pure momentum signal"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "oi_contradicts", "funding_extreme"],
      "data_missing": ["no fresh OI/funding read newer than the 22:37 EEST swing report for TUT/ONG"],
      "suggested_effect": "advisory_only",
      "facts_used": ["TUT/USDT: price down + OI down (-4.49%), funding -0.00052, deleveraging/long-liquidation pattern", "ONG/USDT: price down + OI down (-8.68%), funding -0.00160, deleveraging pattern", "TUT short capped to C tier on short_bounce_guard / squeeze risk (score 48.1)"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["stale_before_entry", "entry_late", "clean_retest", "price_moved_away"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TRUMP/USDT swing long is waiting_for_entry (not yet chased), zone 2.7908-2.8422", "51 of 53 active rows already status=triggered — most of the book is post-entry, not fresh", "many entries created Aug 22-25, now 4-7 days into a swing validity window"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.65,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["53 live crypto B-tier rows: 51 open_actionable (triggered), 2 waiting_for_entry (TRUMP, RE)", "recent 8h signal_outcomes snapshot shows a large batch resolving final_outcome=expired at final_r=0.0 (0R display / unresolved, no TP/SL before window — not a loss)", "stocks: VRT/CRCL/LLY/COST all resolved missed_no_entry/stale_before_entry/expired without ever triggering over the weekend"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["repeated_losses", "correlation_cluster", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TUT/USDT and ONG/USDT open longs contradicted by the desk's own bias=short tag for 5th+ consecutive cycle, deepening on ONG", "book is 100% long with zero diversification into shorts in a mixed-regime overnight session", "no legal/headline risk on any currently-open crypto or stocks position (VRT never triggered)"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["low_sample", "playbook_working"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["headline actionable (A/B): winrate 10.6%, PF 1.141, avgR 0.0362, totalR +11.7R over sample=418", "stocks headline sample=13 (confidence=weak), winrate 60%, PF inf, totalR +12.0R — too small to trust", "stocks C-tier watchlist PF 0.40, winrate 7% — reliably poor, consistent with prior reviews"] },
    { "agent": "head_trader", "verdict": "watch_only", "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "TRUMP/USDT", "trigger": "confirmed fill in zone 2.7908-2.8422 with volume; invalidate below 2.72803", "reason": "highest-score active B (77.7), still waiting_for_entry so not chasing, unlike the 51 already-triggered rows" },
    "best_short_candidate":    { "symbol": "TUT/USDT", "trigger": "watch only — needs short-squeeze risk to clear (system already caps a TUT short to C on short_bounce_guard); would need a clean break of the recent low on rising volume without an upper-wick rejection", "reason": "the desk's own scanner already flags TUT as short-squeeze-prone even while its open long is contradicted by the same bias=short tag" },
    "best_catalyst_candidate": { "symbol": "SOL/USDT", "trigger": "RS vs BTC turning positive (currently weak_vs_market) before treating the DeFi Development 'State of Solana' catalyst as actionable strength, not just context", "reason": "only active signal with a traceable fresh news catalyst, but momentum tag contradicts it" },
    "avoid_candidate":         { "symbol": "ONG/USDT", "reason": "open swing long directly contradicted by the report's own bias=short tag, deepening losses (-15.12% 24h), negative funding, OI down 8.68%, zero news support, unresolved for 5th+ cycle — manual review required, not a clean hold" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.70 | mixed, chop, risk_off, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, no_catalyst, narrative_supported, fresh_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, oi_contradicts, funding_extreme | advisory_only |
| technical_entry | caution | 0.60 | stale_before_entry, entry_late, clean_retest, price_moved_away | advisory_only |
| execution_lifecycle | needs_review | 0.65 | open_actionable, waiting_for_entry, entered_unresolved, needs_review | advisory_only |
| risk_manager | caution | 0.70 | repeated_losses, correlation_cluster, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.60 | low_sample, playbook_working | advisory_only |
| head_trader | watch_only | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

(vs `OPUS_ENRICHED_REVIEW_AUTO_2026-08-28_2331.md`, 23:31 EEST post-close review)

- **New:** DEXE/USDT tier-upgraded C→B (65.3, swing) at 19:59 EEST Aug 28 — most recent watchlist tier-up, now in the active book.
- **Resolved (naturally):** TRUMP/USDT's swing-vs-intraday model disagreement flagged in the prior review is gone — the intraday TRUMP/USDT long (created 04:45 EEST Aug 28) is now `status=stopped`, leaving only the swing long (`waiting_for_entry`) active. No manual action needed; the market resolved the disagreement itself.
- **Improved:** `detect_untracked_legacy_alerts --since 2026-08-29` returns **zero** untracked alerts today, vs the 4/day (MOVR, HEMI×2, CHIP) pattern flagged in the last several reviews. Root cause (`project_crypto_ai_desk_watchlist_alert_signal_reuse_bug`) is not confirmed fixed — just quiet since midnight.
- **Unchanged / escalating:** TUT/USDT and ONG/USDT open swing longs remain `status=triggered` with unresolved bias=short contradictions — now a 5th+ consecutive cycle (first flagged 18:39 EEST Aug 28 for TUT; 2026-08-08 for ONG). ONG's contradiction deepened again in the last fresh swing read (-15.12% vs -11.16% at 22:37 EEST — no fresher swing scan exists this cycle to confirm further movement).
- **Unchanged:** Catalyst mapping 69.0% unmapped (was 70.9%) — still weak, still context-only.
- **Closed out cleanly (weekend):** VRT (Pomerantz legal-risk short), CRCL, LLY, COST all resolved `missed_no_entry`/`stale_before_entry`/`expired` without ever triggering — no open contradicted stocks exposure carries into the weekend, so the LLY-legacy-gate-integrity TODO from the prior review is now moot for this specific signal (it never armed).
- **Regime:** unchanged at "transition (mixed)" since 22:37 EEST — no material shift overnight so far.

## 5. Catalyst Coverage

- Total catalyst events today (`catalyst_events.jsonl`, direct count): **500**
- Mapped (non-null symbol): **155** (31.0%)
- Unmapped (null symbol): **345** (69.0%)
- `narrative_baskets.jsonl`: **4** baskets
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (no symbol resolved):
  1. "$250,000,000 USDC minted at USDC Treasury" (exchange/stablecoin flow, no single-asset attribution)
  2. "Malicious Chrome and Edge extensions targeted crypto wallets and crypto platform logins" (sector-wide security risk, not asset-specific)
  3. "SBI Holdings plans to buy a 20% stake in Indonesian brokerage Ajaib Group for $270M to expand its yen-pegged JPYSC stablecoin" (macro/corporate, no listed-asset match)

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **mixed / chop** (transition regime, BTC/ETH both range, breadth 33.3%/56.3% >EMA20/50) with a **risk-off macro headwind** (100/100 geopolitical risk score, unchanged for multiple cycles: Iran war oil-economics, Strait of Hormuz VLCC rates, Russia fuel-infrastructure strikes).
- Stocks mood: **closed** (Saturday, weekend) — Friday's close context (from the last stocks report) was risk-on with VIX ~14.6; treat as planning-only, not a live read.
- Dominant narrative: momentum/relative-strength continuation longs (the entire active book), not catalyst- or news-driven — only SOL/USDT carries a traceable fresh catalyst, and even that is tagged weak-vs-market.
- Preferred side now: **wait-for-trigger / selective longs only** — the regime has drifted from "bullish trend" (when most of the current book was scored) to "mixed" without a full re-screen; treat existing longs as carried risk, not fresh conviction, and require confirmation before adding new size.
- Best long candidate: **TRUMP/USDT** (waiting_for_entry, zone 2.7908-2.8422, invalidation 2.72803) — cleanest because it hasn't chased yet.
- Best short candidate: **none armed** — TUT/USDT is the closest short-watch (capped to C on short-squeeze risk); needs a clean low break without upper-wick rejection before it's tradeable.
- Best catalyst-backed candidate: **SOL/USDT** — fresh DeFi Development "State of Solana" platform news (The Block), but momentum currently reads weak-vs-market; wait for RS to turn positive.
- What to avoid: **ONG/USDT** — open long directly contradicted by the system's own bias=short tag, deepening losses, negative funding/OI, zero news support, unresolved 5th+ cycle.
- What would change the view: a fresher swing scan (>22:37 EEST) confirming or refuting the TUT/ONG bias-tag breach; BTC/ETH breaking out of range in either direction; breadth crossing back above ~50%/70% (>EMA20/50) to re-confirm "bullish trend."

## 7. Candidate Deep Dives

### 7.1 ONG/USDT (swing long, B, score 73.9, `triggered`) — AVOID / MANUAL REVIEW REQUIRED
- Entry 0.09561-0.09824, stop/invalidation 0.09240, TP1 0.10700. Created 2026-08-26T02:59 UTC — now ~3 days into a swing validity window that expires 2026-09-02.
- Has price already reacted to a catalyst? No catalyst exists — `news_items` has zero ONG matches in the last 4 days; this is a pure relative-strength/momentum signal (original thesis: "momentum score 91.6/100, relative_strength").
- Is the setup chasing? No — already long since Aug 26; the concern is the opposite (holding through an adverse move).
- Retest/pullback structure? Not observable without a fresher chart read; the swing report (6h old) shows 24h -15.12%, RS vs BTC -12.30%, funding -0.00160 (negative), OI -8.68% (deleveraging/long-liquidation pattern), long/short ratio 1.123.
- Overextended? N/A (adverse, not extended in the entry's favor).
- Would entry now be late? Moot — already triggered.
- Aligned with current market mood? No — the regime has drifted to mixed while the position was scored under "bullish trend."
- Long, short, or wait-for-trigger? The system's own report tags ONG/USDT bias=**short** while the open position is long — a direct contradiction, unresolved for 5th+ cycle.
- Actionable now or after confirmation? Should not be treated as a clean hold; escalate to operator/monitor (see §14 TODO).
- Invalidation: 0.09240 (stop_loss = invalidation). Not confirmed breached from current data, but the deepening adverse move plus contradictory bias tag warrants a direct price check outside this run's permission scope.
- Chase-risk? No.
- Catalyst confirmation or contradiction? No catalyst; technical/derivatives contradiction only.

### 7.2 TUT/USDT (swing long, B, score 69.2, `triggered`) — AVOID / MANUAL REVIEW REQUIRED
- Entry 0.05164-0.05250, stop/invalidation 0.05058, TP1 0.05539. Created 2026-08-27T04:46 UTC — ~2 days into a swing validity window expiring 2026-09-03.
- 24h -20.47%, RS vs BTC -17.65%, funding -0.00052 (negative), OI -4.49% (deleveraging/long-liquidation), volume 0.58x — same deleveraging signature as ONG.
- Report bias tag: **short** (score 80.2) directly contradicting the open long.
- Invalidation buffer from entry to stop is only ~3.7% (0.05250 → 0.05058); a -20.47% 24h move strongly suggests the stop should already be through, but `status` still reads `triggered`, not `stopped`.
- Notably, the system's own scanner separately evaluated a TUT **short** and capped it to C tier on `short_bounce_guard` / `high_upper_wick_short_squeeze_risk` (score 48.1) — meaning even a short here is judged squeeze-prone, not a clean flip.
- Actionable now or after confirmation? Neither direction is clean — long is contradicted, short is squeeze-capped. Escalate to operator (see §14 TODO); do not add to either side.

### 7.3 TRUMP/USDT (swing long, B, score 77.7, `waiting_for_entry`) — WATCH, cleanest active long
- Entry zone 2.7908-2.8422, invalidation 2.72803, TP1 3.0134. Created 2026-08-28T15:28 UTC, expires 2026-09-04.
- Has price reacted to a catalyst? No catalyst tag; pure "relative_strength" momentum thesis (91.0/100).
- Chasing? No — still waiting_for_entry, meaning price hasn't reached the zone yet; this is the one active B-tier idea that isn't already several days deep into an adverse or unconfirmed hold.
- Retest/pullback structure? Entry is framed as a zone (2.7908-2.8422) implying a pullback-into-support design, consistent with the mode's "continuation/pullback" setup type.
- Overextended? Not assessable pre-entry without a fresher chart read.
- Aligned with market mood? Partially — mood is mixed/chop, so any new long should demand clean confirmation; treat entry as conditional on volume confirming the zone, not an automatic fill.
- Long/short/wait? Long-only idea; correctly framed as wait-for-trigger already (system status itself is `waiting_for_entry`).
- Invalidation: 2.72803, a clean, pre-defined level.
- Chase-risk? Low, given it hasn't triggered.
- Catalyst confirmation/contradiction? None found; technical-only setup.

### 7.4 SOL/USDT (swing long, B, score 71.9, `triggered`) — WATCH, catalyst present but momentum contradicts
- Entry 96.017-96.649, stop/invalidation 95.244, TP1 98.757. Created 2026-08-24T15:39 UTC.
- Has price reacted to the catalyst? The swing report's catalyst-narrative section flags SOL/USDT: "fresh catalyst exists but risk events require caution" — catalysts: DeFi Development's "State of Solana" real-time intelligence platform (The Block); risks: a geopolitical/macro WuBlockchain weekly digest plus a separate item "Solana Neobank Avici Hacked for $650,000. Token Crashes 40%" (an ecosystem-adjacent hack, not SOL itself, but a headline risk worth noting).
- Original thesis momentum tag: "weak_vs_market" (score 69.4) — the catalyst exists but price/RS strength has not confirmed it.
- Chasing? Already triggered; not a fresh entry decision this cycle.
- Aligned with market mood? Mixed signal — catalyst-positive, technically weak-vs-market, sitting inside an overall mixed regime.
- Long/short/wait? Existing long; new size would be wait-for-trigger pending RS turning positive.
- Catalyst confirmation or contradiction? Confirms narrative (Solana ecosystem development) but momentum tag contradicts near-term strength — treat as context, not confirmation, per §5's mapping-weak guidance too.

### 7.5 DEXE/USDT (swing long, B, score 65.3 at time of upgrade) — WATCH, most recent tier-up
- Most recent crypto tier-upgrade in `watchlist_alerts` (C→B, 19:59:53 EEST Aug 28), the closest available proxy for "new B-tier triggered this cycle" since no fresher upgrade exists within the last ~2.5h.
- No catalyst support found; standard relative-strength continuation thesis consistent with the rest of the book.
- Aligned with market mood? Same caveat as the rest of the long book — scored under a more bullish read than the current mixed regime.
- Actionable now or after confirmation? Treat as carried risk, not fresh conviction, given the regime drift noted in §6.

## 8. Best Candidates Ranked

1. **Long-watch: TRUMP/USDT** — trigger: filled entry in 2.7908-2.8422 with volume confirmation; invalidate below 2.72803.
2. **Catalyst-watch: SOL/USDT** — trigger: RS vs BTC/market turning positive (currently weak_vs_market) to confirm the DeFi Development catalyst as tradeable strength.
3. **Short-watch: TUT/USDT** — trigger: clean break of the recent low on rising volume with no upper-wick rejection (system currently caps this short to C on squeeze risk).
4. **Needs-review (not a new entry): ONG/USDT, TUT/USDT open longs** — see §14 TODOs; hold status should not be treated as a clean, thesis-confirmed position until a human verifies current price against invalidation.
5. **Secondary watch: DEXE/USDT** — most recent tier-up, no catalyst, treat as book-consistent momentum carry only.

## 9. Avoid / No Trade

- **ONG/USDT** (open long) — direct bias-tag contradiction, deepening losses, negative funding/OI, zero catalyst support, unresolved 5th+ cycle. This verdict applies to *this decision window only* — it is not a command to close the position (execution changes are out of scope for this review) nor to pause the scanner.
- **New crypto shorts in general** — the desk currently has zero shorts armed and the one short setup evaluated this cycle (TUT) is squeeze-capped; avoid manually forcing a short until the scanner itself clears one.
- **New stocks positions** — market closed (weekend); nothing to avoid or take today, purely planning context for Monday.

## 10. Main Risks

- **TUT/ONG unresolved contradiction, now 5th+ cycle / 10h+**: if the invalidations were in fact breached and not recorded, both positions are carrying unrecognized risk in whatever downstream paper/monitor accounting depends on `status`.
- **Regime drift without book re-screen**: 53 active long signals scored under "bullish trend" now sit against a "transition (mixed)" regime read (unchanged since 22:37 EEST) — no single-side wipeout risk since these are paper/advisory, but the aggregate thesis quality of the book is weaker than its original scores suggest.
- **Macro risk-off headwind persists at 100/100** (Iran war economics, Russia fuel-infrastructure strikes) — unchanged for multiple cycles, a standing tailwind for downside volatility.
- **Catalyst mapping weak (69% unmapped)** — reduces confidence that "no catalyst" tags on any given symbol are actually true absence of news vs. an unmapped headline.
- **Swing report staleness (6h)**: the only source for TUT/ONG's detailed bias-tag/derivatives evidence is 6h old; a fresher swing scan could materially change the picture in either direction.

## 11. Action Plan — next 4 hours

- Monitor for a fresher crypto swing report (should refresh within the normal ~2-3h cadence) to confirm/refute TUT/ONG's bias-tag status and check whether invalidations have been breached.
- Watch TRUMP/USDT for a confirmed fill in its entry zone with volume; treat as the cleanest new-long idea if it triggers cleanly.
- Watch SOL/USDT's RS-vs-market reading for a shift from weak to neutral/positive before treating its catalyst as tradeable.
- No new stocks action until Monday pre-market; carry forward VRT (legal risk), CRCL, LLY as watch-only names for the pre-US-open review.
- Continue scanning/tracking as normal into the Europe session — no scanner or scheduler changes recommended.

## 12. Final Verdict per Mode

- **Crypto scalp**: caution / selective only — regime mixed, breakout-failure risk elevated per the report's own scoring notes; several C-tier scalp candidates explicitly disabled by kill-switch.
- **Crypto intraday**: caution / wait-for-trigger — same mixed-regime caveat; only 1 `triggered` row live.
- **Crypto swing**: caution / hold-existing-only — 51 open_actionable + 2 waiting_for_entry rows; do not add new size without a fresher regime confirmation; TUT/ONG need manual review before being treated as clean holds.
- **Stocks (all modes)**: closed — planning-only until Monday pre-market; VRT/CRCL/LLY carry forward as watch names.

## 13. Sources

No external sources were cited this run (internal-only cycle — see §2). Internal sources used, with paths and timestamps, are listed in full in §2 above.

## 14. Fix Requests / TODO

### TODO-tut-ong-invalidation-unresolved (carryover, escalating — 5th+ cycle)
- **issue:** Open swing longs `sig_c7ce9835f38c40a8` (TUT/USDT, invalidation 0.05058) and `sig_8d3a8fd71bf0bf75` (ONG/USDT, invalidation 0.09240) both still show `status=triggered` despite the desk's own bias tags reading "short" with 24h moves of -20.47% and -15.12% respectively (per the 22:37 EEST swing report, the only fresh source for this detail). No fresher swing scan exists this cycle to confirm further movement.
- **evidence:** `proposed_signals` direct query (both signal_ids, status=triggered, invalidation unchanged from Aug 28 23:31 review); `data/reports/swing/2026-08-28_19-37_swing_report.md` lines 48-49, 71-72 (bias short, 24h moves, funding/OI figures).
- **suggested manual fix:** a human-driven session should query current TUT/USDT and ONG/USDT prices directly against their invalidation levels, confirm whether stops were actually hit and simply not yet recorded as a `signal_outcome`, and investigate why the monitor hasn't closed/recorded them if so. Now spanning overnight into Asia — time-sensitive.
- **priority:** high
- **first observed:** 2026-08-28 18:39 EEST (TUT), 2026-08-08 (ONG) — both still open at 2026-08-29 04:40 EEST.

### TODO-catalyst-mapping-weak (carryover, unchanged)
- **issue:** `data/catalysts/2026-08-29/catalyst_events.jsonl` unmapped rate is 69.0% (345/500), essentially flat vs yesterday's 70.9% — the catalyst layer remains context-only, not decision-grade, across multiple consecutive days.
- **evidence:** direct count of `catalyst_events.jsonl` (155 mapped / 345 unmapped); comparable figure in prior reviews (70.9% Aug 28).
- **suggested manual fix:** unchanged from prior reviews — audit the symbol-resolver in the catalyst layer; consider whether stablecoin-flow / sector-wide headlines (like the top-3 unmapped examples in §5) should be a distinct "no-symbol-expected" category rather than counted against the mapping rate at all.
- **priority:** medium
- **first observed:** 2026-08-28 18:39 EEST (recurring, unchanged 2026-08-29 04:40 EEST).

### TODO-book-regime-staleness (new)
- **issue:** All 53 active crypto B-tier signals were originally scored while the desk classified the market as "bullish trend" (thesis text: "...while the desk classifies the market as bullish trend..."), created between Aug 22-28. The freshest regime reads (scalp/intraday, both ~04:20 EEST Aug 29) now classify the market as "transition (mixed)" with BTC/ETH both in "range" trend and breadth at only 33.3%/56.3%. No re-screen or re-scoring mechanism appears to flag existing open positions when the regime classification changes after entry.
- **evidence:** `proposed_signals` thesis text across the 53-row active book (uniform "bullish trend" phrasing); `data/reports/scalp/2026-08-29_01-16_scalp_report.md` line 7 ("Market regime: transition (mixed)"); `data/reports/intraday/2026-08-29_01-26_intraday_report.md` line 7 (same).
- **suggested manual fix:** a human-driven session should decide whether open positions should carry a "regime at entry" vs "regime now" comparison field surfaced in `active-signals` output, so reviewers don't have to manually cross-reference thesis text against the latest report each cycle.
- **priority:** medium
- **first observed:** 2026-08-29 04:40 EEST.

### TODO-untracked-alerts-quiet-not-confirmed-fixed (carryover, improved but unverified)
- **issue:** `detect_untracked_legacy_alerts --since 2026-08-29` returns zero rows today, an improvement over the recurring ~4/day pattern (MOVR, HEMI×2, CHIP) seen in prior reviews — but the underlying root cause (`project_crypto_ai_desk_watchlist_alert_signal_reuse_bug`, escalated HIGH 2026-07-17) has not been confirmed fixed, only quiet for one partial day.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-29` output ("None. Every legacy crypto alert has a backing proposed_signal.").
- **suggested manual fix:** continue monitoring across the next few cycles before downgrading or closing this TODO; if it stays quiet through Monday's active session, consider it a candidate for root-cause verification rather than assuming it self-resolved.
- **priority:** medium (downgraded from high pending continued observation)
- **first observed:** 2026-07-17 (recurring); quiet since 2026-08-29 00:00 EEST.
