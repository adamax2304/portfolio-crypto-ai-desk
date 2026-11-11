# Opus Enriched Review — US open reaction review — Auto Cycle 18:39 EEST

## 1. Executive Summary

- **Slot: US open reaction review** (18:30 EEST slot, fired ~18:39). Advisory only / no auto-trade.
- Crypto tape: bullish trend, risk-on price action (BTC/ETH uptrend, 55-64% alt breadth), but macro risk score 82.5-100/100 (Iran/Saudi drone strike, China-US AI sanctions threat) — treat as **mixed**: price action risk-on, macro headline risk-off.
- Stocks: **risk_off** (VIX 19.14, SPY/QQQ downtrend, breadth 0% above EMA20). Sector rotation into energy/financials/healthcare, out of semis/tech.
- **Zero A-tier and zero actionable stocks A/B this cycle** — 5 raw-A stocks setups (NVDA, AVGO, QQQ, XLK, AMD) all demoted to C by session/liquidity/catalyst gates. Crypto B-tier remains the only actionable lane.
- Two confirmed **legal/headline-risk stocks** (UNH: DOJ criminal+civil Medicare probe, externally verified; TSLA: internal "going_concern" flag not externally corroborated as a formal auditor opinion — treat as unresolved/manual review, not confirmed).
- Untracked-alert detector shows **2 anomalies** (DIA/USDT intraday + swing watchlist alerts with no backing proposed_signal) — same known bug pattern as the ALLO/BANK case, now recurring on DIA. TODO raised, no code touched.
- Catalyst mapping this run is **weak (68.2% unmapped)** — treat catalyst layer as context, not final decision.

## 2. Data Used

- Reports: scalp (15:32 EEST, no-trade), intraday (15:44 EEST), swing (17:31 EEST), stocks intraday (18:38 EEST — very fresh).
- Stocks swing/invest reports last generated 2026-07-02 — **stale/deprecated**, excluded (per [[project_crypto_ai_desk_stocks_position_framework]] these legacy modes are deprecated; new stocks_swing_growth_breakout framework is shadow-only and not in these reports).
- Catalyst/narrative: `data/catalysts/2026-07-27/catalyst_events.jsonl` (3000 events), `narrative_baskets.jsonl` (6 baskets).
- CLI: `active-signals` (crypto n=25, stocks n=50), `signal-stats` (crypto + stocks), `detect_untracked_legacy_alerts --since 2026-07-27`.
- DB read queries: `db/crypto_ai_desk.sqlite` → `proposed_signals` (status breakdown, last 24h, both asset classes).
- External: 3 WebSearch queries (UNH DOJ, TSLA going-concern, PUMP catalyst) + 2 WebFetch (1 succeeded — CryptoPotato PUMP article; CNBC UNH fetch blocked 403, search snippet used instead).
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-27_1631.md` (16:44 EEST, pre-US-open slot).

## 3. Scheduler / Data Freshness

- Latest scheduled-run folder: `data/scheduled_runs/2026-07-27_default_schedule/` — `scheduler.log` mtime 18:37 EEST (~2 min old). **Not deferred** (well under 3h threshold).
- Latest `cycle_*_summary.md`: `cycle_09_15-24_summary.md` (mtime 17:44 EEST, ~1h old).
- Report freshness: scalp 3h07m old (borderline), intraday 2h55m old (fresh-ish), swing 1h08m old (fresh), stocks intraday 1 min old (very fresh).
- Monitor logs (crypto/derivatives/fast_news/mexc_canary/stocks/pending) all updated within the last few minutes — monitors appear alive.
- Stocks swing/invest: **stale (>14h, actually 25 days)** — excluded from final verdict per rule, deprecated legacy mode per memory.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-07-27 18:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["stocks swing/invest fresh data (deprecated, last 2026-07-02)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 18:37 EEST", "cycle_09 summary mtime 17:44 EEST", "scalp report 3h07m old"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["mixed", "risk_off", "longs_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH uptrend, 55-64% alt breadth, but macro risk 82.5-100/100", "stocks: risk_off, VIX 19.14, breadth 0% above EMA20, SPY/QQQ downtrend"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["mapping_weak", "stale_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 955/3000 = 31.8% mapped (68.2% unmapped)", "PUMP catalyst externally confirmed but 7 days old (Ansem buy 2026-07-20)", "momentum_breakout basket fresh <1h primary DIA/AKE/NIL but system shows 'no fresh verified catalyst detected' for those symbols — contradiction between basket layer and per-symbol catalyst score"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "data_unavailable"],
      "data_missing": ["OI 24h for most fallback_via_mexc rows"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Nearly all crypto short candidates (DEXE, BANK, EUL, RIF, SYN, ADA, ALLO) capped to C for short-squeeze risk against a bullish tape", "PUMP OI declining even as price rises (spot-driven, not fresh leverage) per external search"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["chase_risk", "entry_late", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PUMP RSI >70 per external source, overbought/correction risk flagged externally", "Most B-tier crypto ideas require pullback entry, current price already above entry zone for several (DIA, NIL, ZAMA)"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.75,
      "reason_codes": ["open_actionable", "waiting_for_entry", "no_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto 24h: triggered=6, waiting_for_entry=3, no-entry/stale/moved-away=16, closed win=5 (tp1/tp3), closed loss=12 (stopped)", "stocks 24h: triggered=1, waiting_for_entry=1, no-entry/stale=50, closed loss=1", "2 untracked legacy alerts (DIA/USDT intraday+swing) — needs_review"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review"],
      "data_missing": ["confirmed external source for TSLA going_concern"],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: DOJ criminal+civil Medicare billing investigation externally confirmed (WSJ/CNBC reports, company acknowledged)", "UNH earnings-adjacent block already active; TSLA legal flag internal-only so far, external search shows accounting-milestone skepticism (Seeking Alpha) but not a formal going-concern opinion — flag as ambiguous, not confirmed"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing mode PF 3.34/+30.4R (n=49, stronger) — best-performing mode", "crypto scalp mode PF 0.10/-9.0R (n=43) — losing, matches known kill-switch/disabled status in scalp report", "stocks C-tier 30d: no_gate_context bucket -406R over 730 trades — dominant loss driver, all gate-demoted/no-context signals"]
    },
    {
      "agent": "head_trader",
      "verdict": "watch_only",
      "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto swing is the strongest live cohort (PF 3.34); stocks intraday has zero actionable A/B this cycle due to gates", "Best long = DIA/USDT (RS-leader, momentum-only, needs real close), Best catalyst-backed = PUMP/USDT (external confirmation, but chase-risk from RSI>70 and 7-day-old catalyst), Best short-watch = NVDA (gated, sector-aligned), Avoid = UNH (confirmed legal risk) and TSLA (ambiguous legal flag, treat as manual review)"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "mixed",
    "best_long_candidate": { "symbol": "DIA/USDT", "trigger": "genuine 1h close inside 0.1610-0.1676 (intraday) or 0.1542-0.1607 (swing) with volume confirmation — has repeatedly failed to fill; demand a real close not proximity", "reason": "Highest RS-vs-BTC momentum leader (91.6 score) across scalp/intraday/swing reports, but no fresh verified catalyst and thin volume (0.14-0.33x)" },
    "best_short_candidate": { "symbol": "NVDA", "trigger": "RVOL rebuild above minimum + any catalyst confirmation + post-lunch session confirmation (SI-gates currently blocking on liquidity_rvol_below_min + lunch_requires_strong_confirmation)", "reason": "Score 92 raw-A, semis sector -16% RS vs SPY (weakest sector), stocks regime risk_off — cleanest short thesis if gates clear" },
    "best_catalyst_candidate": { "symbol": "PUMP/USDT", "trigger": "clean pullback into 0.0020-0.0021 with volume held above 1.5x — do not chase the existing spike; RSI already overbought per external sources", "reason": "Externally-confirmed catalyst (Ansem $1.5M buy, BOOST mode launch) and best-performing playbook this week (crypto_swing_narrative_rs_momentum, 14d PF 5.80)" },
    "avoid_candidate": { "symbol": "UNH", "reason": "Confirmed DOJ criminal + civil Medicare billing investigation (externally verified) plus earnings tomorrow (2026-07-28) — never actionable regardless of score" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.65 | mixed, risk_off, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, stale_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, entry_late, clean_retest | advisory_only |
| execution_lifecycle | ok | 0.75 | open_actionable, waiting_for_entry, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.70 | legal_risk, headline_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | watch_only | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-07-27_1631.md` (16:44 EEST):
- Long-watch DIA/USDT is unchanged — still cited as "highest-scored fresh crypto idea but has failed to fill repeatedly today," still true 2 hours later (now compounded by the untracked-alert bug on the same symbol).
- Previous short-watch was SMH (stocks) on a pre-market-gap-fade thesis; that thesis has now played out (US session is open) — SMH is now C-tier/gated (`sector_confirmation_weak_or_unknown`), no longer the cleanest short. NVDA/AVGO (raw-A, gated to C) are now the stronger short-quality candidates on sector weakness.
- Previous catalyst-watch was HYPE/USDT (perps_dex_narrative, no tradeable levels yet) — still no concrete signal; catalyst-watch reassigned to PUMP/USDT this cycle since it has an externally-verifiable, tradeable structure.
- Previous avoid list (KAITO/USDT crypto, UNH stocks) — KAITO/USDT no longer appears in this cycle's top setups (dropped out of scan); UNH avoid **confirmed and strengthened** by external DOJ verification this cycle.
- New this cycle: TSLA legal_headline_risk flag (going_concern) — did not appear in the 16:44 review; flagged now as unresolved/needs verification.
- New this cycle: untracked-legacy-alert bug recurrence on DIA/USDT (2 instances) — not present in the 16:44 review.

## 5. Catalyst Coverage

- Total catalyst events today: **3000**; mapped (non-null symbol): **955** (31.8%); unmapped: **2045 (68.2%)**.
- Narrative baskets: 6 active (intraday snapshot: rwa_narrative, perps_dex_narrative, binance_ecosystem_teaser, momentum_breakout; swing snapshot adds ai_narrative, delisting_thin_liquidity).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (symbol resolver miss):
  - "MEXC to Convert CXMTUSDT Pre-IPO Futures into Standard Futures #New_Listings"
  - "WEMIX reports contract breach tied to WEMIX$ stablecoin, attacker mints tokens and moves about $724,000"
  - "#Bithumb News — OPEN API 1.0 IP/Key bulk blocking information (@CexAlerts)"

## 6. Market Landscape

Crypto: BTC and ETH both in uptrend, altcoin breadth 55-64% above EMA20 depending on snapshot, volatility normal (ATR percentile 6-10). Desk-recommended style: selective longs, prefer pullbacks on relative strength. Momentum leaders are RS-leader alts (ZAMA, NIL, DIA, AKE, BEAT, BTW) mostly **without a fresh verified catalyst** — pure momentum/RS trades in the `crypto_intraday_catalyst_or_momentum` / `crypto_swing_narrative_rs_momentum` playbooks. Weakest symbols (DEXE, EUL, BANK, SYN, SHIB) are all short-squeeze-risk-capped — shorting is fighting a bullish tape and thin liquidity, not clean right now.

Stocks: regime risk_off, VIX 19.14, 0% of tracked symbols above EMA20, SPY/QQQ downtrend. Sector rotation clearly favors energy/financials/healthcare (RS +5-8% vs SPY) over semis/tech (RS -6% to -16%). Five raw-A setups this cycle (NVDA, AVGO, QQQ, XLK, AMD — all short) were all demoted to C by the SI-1..5 actionability gates (liquidity RVOL below minimum, lunch-session confirmation required, no catalyst). Zero A/B actionable stocks setups this cycle.

### Market Mood / Risk Routing
- Crypto mood: **mixed** (bullish price action, risk-off macro overhang — Iran/Saudi drone strike, China-US AI-sanctions threat, macro risk score 82.5-100/100)
- Stocks mood: **risk_off** (VIX 19.14, breadth 0%, downtrend indices; sector rotation into defensives)
- Dominant narrative: crypto RS-leader momentum rotation (no fresh catalyst backing most leaders); meme-coin re-heating (PUMP, DOGE) per top news
- Preferred side now: crypto — selective RS-leader longs on pullback only; stocks — no clean actionable side (all gated), watch NVDA/semis for a short if gates clear
- Best long candidate: DIA/USDT (see above)
- Best short candidate: NVDA (gated, watch for confirmation)
- Best catalyst-backed candidate: PUMP/USDT
- What to avoid: UNH (confirmed legal risk + earnings), any crypto short into the current bullish tape (squeeze risk dominant), chasing PUMP above the registered entry zone
- What would change the view: a genuine 1h close through the registered entry zones (crypto), or NVDA/semis clearing the liquidity/lunch gates with sector confirmation improving (stocks)

## 7. Candidate Deep Dives

### 1. UNH (stocks, short, C-tier after gate demotion from B, score 70.08)
- Has price already reacted to the catalyst? Yes — stock already reflects known DOJ-probe overhang; today's demotion reason is legal/headline risk, not a fresh reaction.
- Is the setup chasing? N/A — not actionable.
- Retest/pullback structure? N/A.
- Overextended >2 ATR? Not flagged as the primary reason; legal risk is the blocking reason.
- Would entry now be late? N/A — blocked regardless of timing.
- What level makes it actionable? None — legal/headline risk overrides tier/score per §I; this stays AVOID/MANUAL REVIEW until the DOJ matter is resolved or formally priced/settled.
- Aligned with market mood? Stocks risk_off supports a short bias generally, but this specific setup is blocked on legal grounds, not technicals.
- Long/short/wait? N/A — avoid.
- Actionable now or after confirmation? Never actionable on legal/headline risk per system rule.
- Invalidation? N/A.
- Chase-risk? N/A.
- Catalyst confirmation/contradiction? **Confirmed externally**: UnitedHealth is under DOJ criminal and civil investigation into Medicare Advantage billing practices; company has acknowledged the probe (sources below). Earnings tomorrow (2026-07-28) compounds the risk — do not chase into the print regardless of direction.
- **LEGAL/HEADLINE RISK: confirmed, verdict = AVOID.**

### 2. TSLA (stocks, short, C-tier after gate demotion from B, score 76.21)
- Internal system flags `legal_headline_risk: going_concern` as the demotion reason.
- External research found Tesla's own accounting classifies 11 of 12 CEO-award growth milestones as "not probable" (Seeking Alpha) — a real signal of internal skepticism about growth targets — but this is **not the same thing** as a formal going-concern qualification from Tesla's external auditor. No external source found confirming an actual going-concern opinion in July 2026.
- Q2 2026 earnings (reported 2026-07-22) missed and shares fell ~12-15% on heavy AI/Optimus capex (>$25B planned, 3x prior year) pressuring free cash flow — this is a real fundamental headwind, separate from the internal "going_concern" tag.
- Is this chase risk? Yes if shorting the post-earnings drop now — the move has already happened (stock down 12.68% on Jul 23).
- What would make it actionable? Confirmation that the internal `going_concern` tag reflects a real, sourced filing risk (not just the CEO-award milestone language) — needs a manual read of the actual source before treating as a hard legal block.
- **Verdict: MANUAL REVIEW REQUIRED** — treat the internal legal flag as unresolved/ambiguous pending human verification, not as confirmed as UNH's DOJ probe is. Do not is quietly waved through as clean either.

### 3. NVDA (stocks, short, raw-A demoted to C, score 92.08)
- Has price already reacted? Semis sector is already the weakest (RS -16.05% vs SPY 20d) — this is an established trend, not a fresh break.
- Chasing? Possible — NVDA and AVGO both score raw-A on the short side; SI-gates are blocking specifically on `liquidity_rvol_below_min` and `lunch_requires_strong_confirmation`, i.e. the system judges current-session volume/timing as not confirmed yet, not that the thesis is wrong.
- Retest/pullback structure? Not assessable without chart tooling — **TradingView/manual chart check unavailable**, using only local OHLCV/ATR/EMA fields from the report (none surfaced beyond the score table for this candidate).
- Overextended >2 ATR? Not flagged.
- Would entry now be late? Possibly, given this is the "US open reaction" window and the setup was already raw-A pre-open — a chase into current price without RVOL confirmation would violate the gate for good reason.
- What level/condition makes it actionable? RVOL climbing back above the minimum threshold + session moving past the lunch-confirmation requirement + ideally a catalyst appearing (`catalyst_none_and_not_exceptional_technical` is also blocking).
- Aligned with mood? Yes — stocks risk_off + weak semis sector supports a short bias.
- Chase risk? Yes if entered immediately; **wait for gate-clear signal.**
- Catalyst confirmation/contradiction? No fresh NVDA-specific catalyst found internally or externally in this pass beyond general "AI capex skepticism" macro narrative (Michael Burry commentary on QQQ per stocks report §4).
- **Verdict: WATCH — best short-watch candidate, not yet actionable.**

### 4. PUMP/USDT (crypto, long, B-tier swing, score 77.1 — top idea this cycle)
- Has price already reacted to the catalyst? Yes — the Ansem $1.5M buy and BOOST-mode catalyst are from **2026-07-20**, 7 days old; today's report shows "no fresh verified catalyst detected" for PUMP at the per-symbol level, which is consistent (the catalyst is not fresh, just still-supportive).
- Is the setup chasing? Current price 0.0021 is at/above the top of the registered entry zone (0.0020-0.0021) — a market buy here would be chasing.
- Retest/pullback structure? Entry plan explicitly calls for a pullback into 0.0020-0.0021; no confirmation yet that price has pulled back and held.
- Overextended? External source flags RSI already above 70 (overbought) as of July 20 — real chase-risk signal, and OI is declining even as price rises (spot-driven momentum, not fresh leverage, per external search) which is a double-edged signal: less squeeze risk, but also less conviction behind the move.
- Would entry now be late? Yes, if chasing; only a genuine pullback-and-hold is clean.
- What would invalidate the idea? 1h close beyond 0.0020 (below planned entry zone), or BTC breaking regime support.
- Aligned with market mood? Yes — fits the "selective longs on RS-leader/catalyst-backed" mood.
- Actionable now or after confirmation? After confirmation (pullback), not a market chase.
- Chase-risk? Yes, currently high.
- Catalyst confirmation? **Confirmed but stale (7d)** — supportive, not fresh.
- **Verdict: WATCH / catalyst-backed candidate — wait for the pullback, do not chase.**

### 5. DIA/USDT (crypto, long, appears in intraday score 66.1 B-tier and swing score 72.4 B-tier — also flagged by the untracked-legacy-alert detector)
- Has price already reacted? 24h return already +22-28% depending on snapshot — a large move has already happened; RS vs BTC +21-27%.
- Is the setup chasing? Current price (0.1636-0.1705) sits above both registered entry zones (0.1542-0.1676) in every snapshot today — this idea has been "the highest-scored fresh crypto idea but has failed to fill repeatedly" per the previous review, and remains unfilled 2+ hours later.
- Retest/pullback structure? Entry zones are pullback zones by design; price simply hasn't come back to them.
- Overextended >2 ATR? Not explicitly flagged in the report, but the persistent non-fill across three consecutive reports (scalp/intraday/swing) over several hours is itself a signal that this is running away, not consolidating.
- What would invalidate/what level makes it actionable? A genuine 1h close inside 0.1542-0.1676 with the stated invalidation intact (1h close beyond 0.1463-0.1530 depending on mode).
- **System-integrity note:** the untracked-alert detector shows 2 DIA/USDT watchlist alerts (intraday sent 12:44:33 UTC, swing sent 14:30:33 UTC) with **no matching proposed_signal within 6h** — meaning these alerts were pushed to Telegram but will not contribute to PF/winrate tracking. This is the same failure pattern previously confirmed on ALLO/USDT and BANK/USDT (see [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]]), now recurring on a third symbol. Raised as TODO-3 below (do not fix — hand to a manual session).
- Aligned with mood? Yes, momentum/RS-leader long fits current desk style.
- Catalyst confirmation/contradiction? momentum_breakout narrative basket lists DIA/AKE/NIL as primary with "fresh <1h" freshness, but the per-symbol catalyst score still says "no fresh verified catalyst detected" — a genuine contradiction between the basket layer and the per-symbol catalyst score worth noting, not resolving here.
- **Verdict: WATCH — demand a real close, not proximity; treat the repeated non-fill as a signal the entry zone may need to be reassessed, not chased.**

## 8. Best Candidates Ranked

1. **Long-watch: DIA/USDT** — trigger: genuine 1h close inside 0.1542-0.1676 (mode-dependent) with volume confirmation; has failed to fill repeatedly across 3 consecutive reports today.
2. **Catalyst-watch: PUMP/USDT** — trigger: confirmed pullback into 0.0020-0.0021 holding on volume ≥1.5x; do not buy the current overbought spike (RSI>70 externally confirmed).
3. **Short-watch: NVDA** — trigger: RVOL climbs back above the minimum gate threshold + session moves past lunch-confirmation requirement; semis sector RS is the weakest in the stocks universe (-16.05%).
4. **Avoid (stocks, confirmed): UNH** — DOJ criminal+civil Medicare investigation externally verified, plus earnings tomorrow; never actionable regardless of score.
5. **Avoid/manual-review (stocks, unresolved): TSLA** — internal going_concern flag not externally corroborated as a formal auditor opinion; treat as ambiguous pending human verification, not clean.
6. **Monitor-only (already open, do not add): LA/USDT (swing, triggered), NIL/BTW/AKE/USDT (swing, triggered)** — manage existing TP/SL only, no new entries.

## 9. Avoid / No Trade

This applies to the **current decision window only** — scanning, tracking, and monitors continue regardless.
- UNH: confirmed legal/headline risk (DOJ) + earnings tomorrow.
- TSLA: unresolved legal flag, manual review required before treating as either clean or blocked.
- Any fresh crypto short: DEXE, BANK, EUL, RIF, SYN, ADA, ALLO are all short-squeeze-risk-capped to C against the bullish tape — shorting into this regime is fighting the tape with thin liquidity.
- Chasing PUMP/USDT above the registered entry zone (overbought, stale catalyst).
- Chasing DIA/USDT at current price — wait for the actual pullback fill.

## 10. Main Risks

- Macro/geopolitical headline risk is elevated (score 82.5-100/100): Iran-Saudi drone attack, China-US AI-sanctions threat — any escalation could flip the crypto risk-on tape quickly.
- Catalyst mapping is weak this run (68.2% unmapped) — do not over-weight the catalyst layer for new decisions.
- Two legal/headline-risk stocks in the current book (UNH confirmed, TSLA ambiguous) — avoid new exposure to either regardless of score.
- Recurring untracked-alert bug (now 3rd symbol affected: DIA, after ALLO/BANK) means some Telegram-pushed alerts are silently falling outside PF/winrate tracking — a data-quality/monitoring gap, not a live-trading risk, but distorts performance read.
- Stocks C-tier 14d "would-have-been-A/B" diagnostic shows net -11.5R / PF 0.42 across 71 near-A/B setups — the gates are, on net, saving R by blocking these, supporting continued caution on gated stocks setups.

## 11. Action Plan — next 4 hours

- Watch DIA/USDT for a genuine 1h close into its entry zone; do not chase current price.
- Watch PUMP/USDT for a real pullback + volume hold before considering long entry; treat current level as overbought.
- Watch NVDA/semis for RVOL and session-confirmation gates to clear before treating the short as actionable.
- No new stocks entries this window — zero A/B actionable, all raw-A/B demoted to C.
- Continue monitoring existing open crypto swing positions (LA, NIL, BTW, AKE — all triggered) for TP/SL management only.
- Manual session should verify the TSLA `going_concern` internal tag against its actual source before the next earnings-adjacent review.

## 12. Final Verdict per Mode

- **Crypto scalp:** No trade (kill-switch disabled per report; PF 0.10/-9.0R last 14d, matches known bad mode).
- **Crypto intraday:** Watchlist only — DIA/USDT/NIL/ZAMA/AERO/AKE all momentum-only, no fresh catalyst, wait for real pullback fills.
- **Crypto swing:** Best current lane (PF 3.34/+30.4R, n=49) — PUMP/USDT is the top idea but only on a confirmed pullback; several positions already triggered (LA, NIL, BTW, AKE) and should be managed, not added to.
- **Stocks intraday:** No trade — zero A/B actionable, all raw-A/B gated to C this cycle. Watch NVDA/semis for gate-clear.
- **Stocks swing/invest:** Deprecated/stale (last report 2026-07-02) — not evaluated this cycle.

## 13. Sources

- [UnitedHealth Acknowledges DOJ Investigation into Medicare Billing Practices](https://www.bracheichler.com/insights/unitedhealth-acknowledges-doj-investigation-into-medicare-billing-practices/)
- [UnitedHealth facing DOJ investigation over Medicare billing (CNBC, 2025-07-24 origin, ongoing into 2026)](https://www.cnbc.com/2025/07/24/unitedhealthcare-doj-investigation-medicare-billing.html)
- [DOJ's criminal probe into UnitedHealth extends to Optum Rx, physician reimbursement (FierceHealthcare)](https://www.fiercehealthcare.com/payers/wsj-report-doj-interviewing-former-employees-about-medicare-billing-practices-unitedhealth)
- [Tesla's Own Auditors Say The Growth Narrative Is Currently 'Not Probable' (Seeking Alpha)](https://seekingalpha.com/article/4908702-teslas-own-auditors-say-the-growth-narrative-is-currently-not-probable)
- [Tesla Earnings: Shares Fall After Profit Tumbles as AI Spending Jumps (Bloomberg, 2026-07-22)](https://www.bloomberg.com/news/articles/2026-07-22/tesla-second-quarter-earnings-miss-wall-street-s-expectations)
- [Tesla Inc Stock (TSLA) Moved Down by 12.68% on Jul 23 (TradingKey)](https://www.tradingkey.com/news/market-movers/262050242-market-movers-tsla-20260723)
- [PUMP Climbs to a 2-Month High: Key Catalysts and What's Next (CryptoPotato, 2026-07-20)](https://cryptopotato.com/pump-climbs-to-a-2-month-high-key-catalysts-and-whats-next/)
- [PUMP Token Surges Amid Influencer Led X Hype And July Insider Unlock (CryptoTimes)](https://www.cryptotimes.io/2026/07/20/pump-token-surges-amid-influencer-led-x-hype-and-july-insider-unlock/)
- [Pump.fun Surges 11.60% Amidst Altcoin Gains — Daily Movers July 27](https://thecurrencyanalytics.com/breaking-news/pump-fun-surges-11-60-amidst-altcoin-gains-daily-movers-july-27)

## 14. Fix Requests / TODO

### TODO-untracked-dia-alert
- **issue:** Untracked-legacy-alert detector shows 2 DIA/USDT watchlist alerts (intraday 12:44:33 UTC, swing 14:30:33 UTC) with no matching proposed_signal within 6h — same bug pattern previously confirmed on ALLO/USDT and BANK/USDT.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-27` output; also see [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]] memory (raised as TODO-3, high priority, 2026-07-17).
- **suggested manual fix:** Confirm whether this is the same root cause (stale/closed signal_id reuse on watchlist re-fire) now affecting a 3rd symbol; escalate priority if pattern keeps recurring across new symbols.
- **priority:** high
- **first observed (this recurrence):** 2026-07-27 18:39 EEST (bug itself first observed 2026-07-17 per memory)

### TODO-tsla-going-concern-verification
- **issue:** Internal stocks-intraday gate demoted TSLA (B→C) citing `legal_headline_risk: going_concern`, but external web research this cycle did not find a formal going-concern auditor opinion — only unrelated accounting skepticism about CEO-award growth milestones (Seeking Alpha) and a post-earnings price drop.
- **evidence:** `data/reports/stocks/intraday/2026-07-27_15-38_stocks_intraday_report.md` §7 TSLA demotion row; WebSearch "Tesla TSLA going concern auditor warning July 2026" (no formal opinion found).
- **suggested manual fix:** Trace the actual source event that set the internal `going_concern` tag for TSLA and confirm whether it's a real filing-based flag or a possible false positive / mislabeled event category.
- **priority:** medium
- **first observed:** 2026-07-27 18:39 EEST

### TODO-catalyst-mapping-coverage
- **issue:** Catalyst symbol-mapping coverage is 31.8% (68.2% unmapped) this run, well below the 50% threshold, consistent with a recurring pattern noted in prior memory ([[project_crypto_ai_desk_news_layer_hardening]] symbol audit ~17% match).
- **evidence:** `data/catalysts/2026-07-27/catalyst_events.jsonl` — 3000 total events, 955 mapped.
- **suggested manual fix:** Revisit the symbol resolver in the catalyst ingestion layer; sample the top unmapped headline patterns (exchange-ops notices, non-English regional exchange announcements) to see if a targeted allowlist/blocklist would recover mapping rate cheaply.
- **priority:** low
- **first observed:** recurring, this instance 2026-07-27 18:39 EEST

## Telegram

```
[AUTO-REVIEW US open reaction review 18:39 EEST]

Mood:
- Crypto: mixed (bullish price action, risk-off macro overhang)
- Stocks: risk_off
- Prefer: crypto selective longs (pullback only) / stocks wait-for-trigger

Status:
- Open actionable: 6 (crypto triggered) + 1 (stocks triggered, legacy B)
- Waiting for entry: 3 (crypto) + 1 (stocks)
- Review/Shadow: 0
- Entered unresolved: included in open actionable above (no TP/SL yet)
- No-entry/stale/moved-away: 16 (crypto) + 50 (stocks, 24h)
- Needs review: 2 (DIA/USDT untracked legacy alerts)

Decisions:
- Long-watch:     DIA/USDT trigger 1h close inside 0.1542-0.1676 w/ volume, has failed to fill repeatedly
- Short-watch:    NVDA trigger RVOL clears gate + session confirmation (semis weakest sector, RS -16%)
- Catalyst-watch: PUMP/USDT trigger confirmed pullback into 0.0020-0.0021, do not chase (RSI>70 externally confirmed)
- Avoid:          UNH (confirmed DOJ Medicare probe + earnings tomorrow); TSLA legal flag unresolved, manual review

Risk:
- Macro risk-off headline score 82.5-100/100 (Iran/Saudi, China-AI sanctions) — crypto risk-on tape could flip fast

Catalyst coverage: mapped 955/3000 (31.8%), baskets 6
                   weak this run — context only

File: OPUS_ENRICHED_REVIEW_LATEST.md
Advisory only. No auto-trade.
```
