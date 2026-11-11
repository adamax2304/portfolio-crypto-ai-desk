# Opus Enriched Review — US open reaction review — Auto Cycle 18:30 EEST

## 1. Executive Summary

Slot: **US open reaction review** (target 18:30 EEST / 11:30 ET; actual data pull ~18:39-18:47 EEST — within tolerance). **Advisory only — no auto-trade, no scoring/threshold/strategy changes.** External web research was available and used this run (WebSearch succeeded on all 6 queries; no WebFetch needed beyond search-result synthesis).

**Zero A-tier signals actionable anywhere.** Crypto: all-B active positions only (no new A/B in the freshest 12:16-16:34 cycle reports). Stocks: the desk's own algorithm flagged **AMZN as A-tier (score 94.7)** this cycle but demoted it A→C for **"active legal/headline risk (going_concern) — manual review required."** I searched `news_items` (title/content_text, 72h and 7-day windows) and found **zero rows anywhere in the database ever tagged or containing "going concern" language for AMZN** — external research (WebSearch) also found nothing except a blowout Q2 print (AWS +36.7%, EPS $5.75 vs $1.82 expected, stock +13-14% intraday) and 36/37 analysts on Buy. This looks like a **false-positive legal-risk trigger**, not a real going-concern event — flagged as **TODO-1 (high priority)** below. The system's own gate still applies (this review cannot override it), so AMZN stays watch-only pending human verification.

**Real, verified catalysts today:** AMZN (AWS beat, confirmed), COIN (Q2 net loss $359M vs -$0.01 EPS expected, revenue miss, confirmed), AAPL (Services/China miss, -7.2% intraday, plus a Sen. Cotton "blacklisted Chinese chips" headline — confirmed), and BANK/USDT (Lorenzo Protocol, down ~56-60% over the week on insider-float-concentration concerns after a $13.7M token transfer to Aster — confirmed, catalyst-backed, not a random move).

**Market mood:** Stocks are **narrow risk-on** — S&P +0.67%, Nasdaq +1.32%, Russell +1.37% — but 10Y Treasury yield hit **4.737%, highest since Jan 2025**, and the rally is concentrated in single-name earnings reactions (AMZN) rather than broad breadth; AAPL alone is dragging the mega-cap complex. Crypto stays **risk-off/chop**: BTC downtrend, ETH transition_down, macro/geopolitics risk pinned at **100.0/100** (Iran-war headlines, Coldcard hardware-wallet hack draining ~$38-40M). BTC/ETH backed off from an early bounce per external sources, consistent with the internal downtrend read — **no internal/external divergence this cycle** (unlike the 16:05 pre-open review).

**Persisting data-quality issue:** `track-signals (pre)` and `(post)` have now failed (`exit=1`) in **every cycle today since 04:30**, including the two most recent runs at 16:38 and 18:41 — signal-outcome tracking may be silently missing an extended window. Escalated further in §14. Scanning, tracking, and monitors continue regardless — this review never recommends stopping the system.

## 2. Data Used

| File / Source | mtime (local) | Age |
|---|---|---|
| `data/reports/scalp/2026-07-31_12-04_scalp_report.md` | 15:04 EEST | ~3h40m — no A/B/C ideas this cycle (mode is a standing weekly loser) |
| `data/reports/intraday/2026-07-31_12-16_intraday_report.md` | 15:16 EEST | ~3h30m — carry-forward |
| `data/reports/swing/2026-07-31_13-34_swing_report.md` | 16:34 EEST | ~2h10m — fresh (<4h bucket) |
| `data/reports/stocks/intraday/2026-07-31_13-37_stocks_intraday_report.md` | 16:37 EEST | ~2h10m — fresh, market-open data |
| `data/reports/stocks/swing/` / `invest/` (2026-07-02) | ~29 days stale | excluded — deprecated/removed playbooks, see [[project_crypto_ai_desk_stocks_position_framework]] |
| `data/catalysts/2026-07-31/catalyst_events.jsonl` (2500 rows) + `narrative_baskets.jsonl` (2 baskets) | 15:21 EEST | ~3h26m fresh |
| `data/processed/llm_analysis_packet.md` / `llm_stocks_packet.md` | 16:35 / 15:46 EEST | fresh |
| `data/scheduled_runs/2026-07-31_default_schedule/scheduler.log` + `cycle_01_14-55_summary.md` | 16:41 / 16:40 EEST | ~2h06m — well inside the 3h non-defer window |
| `reports/PAPER_MONITOR_STATUS_LATEST.md` | 16:38 EEST | ~2h09m — carry-forward, treated as representative |
| `python -m src.cli active-signals --asset-class crypto` / `stocks` | live query | now |
| `python -m src.cli signal-stats --asset-class crypto` / `stocks` | live query | now |
| `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-31` | live query | now — **0 found** (the recurring GIGGLE untracked-alert bug from earlier cycles did not reproduce this cycle) |
| `news_items` direct SQL (AMZN going_concern verification, SMCI legal check) | live query | now |
| WebSearch ×6: AMZN going-concern, AMZN earnings reaction, US market open, BTC/ETH price, MSTR Bitcoin-sale/dividend, BANK/Lorenzo crash, COIN earnings | live | now |
| Prior review `OPUS_ENRICHED_REVIEW_AUTO_2026-07-31_1605.md` | 16:05 EEST | for §4 diff |

**External web research was available and used this run.**

## 3. Scheduler / Data Freshness

- Both scheduler.log (16:41) and the latest cycle summary (16:40) are ~2h old — well inside the 3h non-defer threshold. Review proceeds.
- Cycle 1 (14:55-16:41) ran ok=86/failed=3. Cycle 2 started 18:41 (still running at review time; `track-signals (pre)` for cycle 2 already logged `exit=1` at 18:41:32).
- `track-signals` failures: `exit=1` at 14:55 (pre), 16:38 (post), and 18:41 (pre) — **3 consecutive failures today**, same signature as the standing TODO from prior reviews. See §14.
- `stocks/swing` and `stocks/invest` reports are dated 2026-07-02 (~29 days old) — excluded from this review's verdicts per the position-framework deprecation, not treated as a fresh-data failure.
- Paper Monitor Status (16:38 EEST, ~2h09m carry-forward): OPEN_ACTIVE 2, WAITING_FOR_ENTRY 5, REVIEW_ONLY_SHADOW 44, ENTERED_UNRESOLVED_EXPIRED 6, NO_ENTRY_EXPIRED 50, CLOSED_WIN 148 / CLOSED_LOSS 17 / CLOSED_FLAT 21, UNKNOWN_INCONSISTENT 3.
- Untracked-alert detector: **0 found this run** — improvement vs the 16:05 review (1 found, GIGGLE/USDT); the underlying bug (TODO-2gb, watchlist-alert/signal_id reuse) is not confirmed fixed, just not reproduced this specific cycle.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-07-31 18:47 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["stocks swing/invest reports ~29 days stale, excluded"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log/cycle summary ~2h old, within 3h non-defer window", "track-signals pre+post failed exit=1 at 14:55, 16:38, and again 18:41 — 3rd consecutive failure today", "catalyst mapping unmapped % continuing an all-day worsening trend (63.7% at 16:05)"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mixed", "risk_off", "chop", "wait_for_trigger"],
      "data_missing": [],
      "facts_used": ["stocks: S&P +0.67%, Dow +0.38%, Nasdaq +1.32%, Russell +1.37%, but 10Y yield 4.737% (highest since Jan 2025) and rally concentrated in AMZN single-name reaction, not broad breadth", "AAPL -7.2% intraday dragging mega-cap complex", "crypto: BTC downtrend, ETH transition_down, range/chop, macro/geopolitics risk pinned 100.0/100 (Iran war, Coldcard $38-40M hack)", "BTC ~$63.6-64.7k and ETH ~$1877-1917 both backed off an early bounce per external sources — consistent with internal downtrend read, no divergence this cycle"], "suggested_effect": "advisory_only" },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["catalyst_confirmed", "catalyst_contradicted", "mapping_weak", "narrative_supported"],
      "data_missing": [],
      "facts_used": ["AMZN: AWS +36.7%, EPS $5.75 vs $1.82 expected — real, externally confirmed catalyst", "AMZN going_concern flag: zero supporting news_items rows found (title/content_text search, 72h and 7-day windows), zero going_concern-tagged rows in the entire DB ever — contradicted by external fundamentals and 36/37-analyst Buy consensus; likely false positive", "COIN: Q2 net loss $359M, EPS -$1.36 vs -$0.01 expected, revenue $1.2B vs $1.35B expected — real, confirmed catalyst", "AAPL: Services/China miss (-7.2%) plus a Sen. Cotton chip-sourcing headline — real, confirmed catalyst", "BANK/USDT: Lorenzo Protocol down ~56-60% over the week on insider-float-concentration concern after a $13.7M token transfer to Aster — real, confirmed catalyst, not a random/unexplained move", "catalyst mapping still >60% unmapped (continuing trend from earlier cycles today)"], "suggested_effect": "advisory_only" },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "data_unavailable"],
      "data_missing": ["no fresh funding/OI pull beyond the 13:34 swing report snapshot"],
      "facts_used": ["BANK/USDT: funding negative (-0.00186 in the 12:16 snapshot), shorts already crowded — squeeze risk on chasing the short after a 56-60% weekly decline", "GIGGLE/ROBO: price up + OI up, fresh (not yet extreme) positioning, crowding normal"], "suggested_effect": "advisory_only" },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["entry_late", "chase_risk", "overextended", "clean_retest"],
      "data_missing": [],
      "facts_used": ["AMZN already up 13-14% intraday — chasing now is late regardless of the legal-gate question", "AAPL/COIN both already reacted to their catalysts pre-open/at-open; stocks-intraday actionability gates correctly require first-15m ORB/opening-drive confirmation before either becomes actionable", "BANK/USDT already down 56-60% for the week — shorting the initial move now would be very late; only a failed-bounce retest is clean", "ROBO/USDT (crypto swing B, RS-leader, playbook 14d WR 72%/PF 5.80) has a defined, not-yet-reached pullback zone 0.0140-0.0143 — a genuinely clean setup if it fills there"], "suggested_effect": "advisory_only" },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow", "no_entry", "entered_unresolved", "needs_review"],
      "data_missing": ["fresh Paper Monitor regeneration this cycle (using 16:38 carry-forward, ~2h09m old)"],
      "facts_used": ["Paper Monitor 16:38 EEST (carry-forward): OPEN_ACTIVE 2, WAITING_FOR_ENTRY 5, REVIEW_ONLY_SHADOW 44, ENTERED_UNRESOLVED_EXPIRED 6, NO_ENTRY_EXPIRED 50, CLOSED_WIN 148 / CLOSED_LOSS 17 / CLOSED_FLAT 21, UNKNOWN_INCONSISTENT 3", "crypto active-signals: 25 rows, 5 waiting_for_entry, 2 triggered/open, 18 partial-TP still running", "stocks active-signals: 50 rows, nearly all C-tier (never actionable per position-framework hardening); only 2 A-tier and 4 A/B total this week (anecdotal sample)"], "suggested_effect": "advisory_only" },
    { "agent": "risk_manager", "verdict": "manual_review", "confidence": 0.6,
      "reason_codes": ["headline_risk", "manual_review", "legal_risk", "reduce_risk"],
      "data_missing": [],
      "facts_used": ["AMZN going_concern gate: cannot be independently corroborated, likely false positive, but this review cannot override the code's own gate — recommend a human-driven session audit the legal_risk classifier's AMZN trigger specifically", "macro/geopolitics risk pinned 100.0/100 all day (Iran war, sanctions, Coldcard hack)", "10Y yield at highest since Jan 2025 — a broad equity-headwind risk factor not specific to any single candidate", "MSTR: real, ongoing story of using BTC treasury sales to fund preferred dividends (3,588 BTC / ~$216M sold, ~17% of a $1.25B authorization consumed in under a week) — a genuine financial-stress-adjacent caution for the active MSTR long signal, not a clean setup"], "suggested_effect": "advisory_only" },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "facts_used": ["crypto A/B week: winrate 25%, PF 2.34, +29.4R (n=101, reliable) — intraday strongest (PF 4.86), swing modest (PF 1.64), scalp still a standing loser (PF 0.2, avgR -0.21, n=24, 0 wins of 20 triggered) — no scalp candidates surfaced this cycle anyway", "stocks A/B week: winrate 0%, PF 0.0, -1.0R (n=4, anecdotal — too small to act on)", "stocks C-tier week: winrate ~5%, PF 0.22, -7.0R (n=189, reliable) — consistent with the standing C-tier-never-actionable policy"], "suggested_effect": "advisory_only" },
    { "agent": "head_trader", "verdict": "see head_trader block below", "confidence": 0.0, "reason_codes": [], "data_missing": [], "suggested_effect": "advisory_only", "facts_used": [] }
  ],
  "head_trader": {
    "overall_verdict": "manual_review",
    "confidence": 0.55,
    "preferred_side": "catalyst_backed",
    "best_long_candidate":     { "symbol": "AMZN", "trigger": "human verification that the going_concern legal-risk flag is a false positive (no supporting news_items evidence found anywhere, contradicted by fundamentals) — pending that, this stays gated at C-tier/not-actionable regardless of how clean the underlying catalyst is; do not chase the +13-14% move even if unblocked", "reason": "score 94.7, real AWS-beat catalyst, but currently the single most consequential false-gate candidate of the day" },
    "best_short_candidate":    { "symbol": "AAPL", "trigger": "first-15m opening-range confirmation of continued weakness below the session low, per the code's own ORB gate — do not chase the existing -7.2% move without it", "reason": "real, confirmed catalyst (Services/China miss + Sen. Cotton chip-sourcing headline), demoted B→C purely on actionability-gate technicalities (market context, ORB confirmation), not legal risk" },
    "best_catalyst_candidate": { "symbol": "COIN", "trigger": "RTH breakdown confirmation below the session's post-earnings low", "reason": "Q2 net loss $359M vs -$0.01 EPS expected, revenue miss — cleanest, least ambiguous confirmed catalyst of the day" },
    "avoid_candidate":         { "symbol": "BANK/USDT", "reason": "already down 56-60% for the week on a real insider-float-dump catalyst — shorting the initial move now is chasing a squeeze-prone, already-crowded short; only a confirmed failed-bounce retest is clean" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 6
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---:|---|---|
| data_quality | caution | 0.70 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.60 | mixed, risk_off, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | catalyst_confirmed, catalyst_contradicted, mapping_weak, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | entry_late, chase_risk, overextended, clean_retest | advisory_only |
| execution_lifecycle | ok | 0.75 | open_actionable, waiting_for_entry, review_shadow, no_entry, entered_unresolved, needs_review | advisory_only |
| risk_manager | manual_review | 0.60 | headline_risk, manual_review, legal_risk, reduce_risk | advisory_only |
| playbook_performance | caution | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| **head_trader** | **manual_review** | **0.55** | synthesis — see §3A | advisory_only |

## 4. What Changed vs Previous Review (16:05 EEST — pre-US-open)

- **New:** US cash market is now open (regular session). AMZN confirmed +13-14% on the earnings beat; AAPL confirmed -7.2% on the Services/China miss — both were premarket-only reads in the 16:05 review, now RTH-confirmed.
- **New:** AMZN's `going_concern` legal-risk gate identified and investigated this cycle — no supporting evidence found anywhere internally or externally; flagged as a likely false positive (TODO-1, high priority, new finding).
- **New:** COIN earnings result now known — Q2 net loss $359M, wider than expected, stock falling; this was not yet reported at 16:05.
- **Resolved:** The 16:05 review's central open question ("does the premarket risk-on chip/tech tape hold through the open?") is now answered: partially — the index-level numbers are positive (S&P/Nasdaq/Russell all green) but breadth is narrow (AAPL alone is a major drag) and 10Y yields spiking to a 18-month+ high is a genuine headwind not present in the premarket read.
- **Improved:** The GIGGLE/USDT untracked-alert bug (TODO-2gb) did not reproduce this cycle (0 found vs 1 at 16:05) — not confirmed fixed, just not observed this run.
- **Unchanged:** `track-signals` crash continues (now confirmed through the 18:41 cycle-2 kickoff) — see TODO escalation.
- **Unchanged:** BANK/USDT avoid-both-directions verdict carries forward, now with an externally-confirmed fundamental driver (insider float dump) rather than "no cited driver" as in the 16:05 review — upgrade from "avoid, unexplained" to "avoid, catalyst-backed but overextended."
- **Unchanged (not re-verified this cycle):** ESP/USDT swing-long-vs-weakest-symbols-table contradiction (TODO-NEW-4 from 16:05) — still present in both the 16:34 swing report and the 12:16 intraday report's weakest-symbols tables; treated as a monitor-only carry, not re-litigated in a full deep dive this cycle given the 5-candidate cap.
- **Unchanged (carried, not re-verified):** PLTR/META legal-risk flags (TODO-1/TODO-2 from prior reviews, renumbered below) — not re-searched this cycle; time was prioritized toward the new AMZN going_concern finding, which is materially larger (A-tier score vs two already-excluded names).
- **Worsened → JPM's book position:** the 16:05 pre-us JPM long idea is not present in this cycle's active-signals or reports at all — appears to have expired/rotated out; not re-verified as a still-live idea this cycle.

## 5. Catalyst Coverage

- Total catalyst events today (cumulative): **2500**; mapped: **908**; unmapped: **1592** (**63.7%**, same reading as the 16:05 review — no new catalyst cycle completed between 15:21 and this review's data pull).
- Narrative baskets: 2 — `perps_dex_narrative` (playbook `wait_pullback`, primary HYPE/USDT), `binance_ecosystem_teaser` (playbook `related_beta_rotation`, primary BNB/USDT).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (63.7% unmapped, above the 50% threshold.)
- Top unmapped headlines (sampled): USDC Treasury mint notices (250M USDC, ×2, no ticker resolvable), a Korean-language Bithumb exchange UI notice, institutional-OTC-flow and South-Korea-retail-rotation macro notes with no single-symbol attribution.

## 6. Market Landscape

US cash markets are in their first couple of hours of the regular session. Headline index moves are positive (S&P +0.67%, Dow +0.38%, Nasdaq +1.32%, Russell +1.37%) and driven almost entirely by Amazon's blowout Q2 print (AWS +36.7% to $42.2B, EPS $5.75 vs $1.82 expected, 2026 capex guidance raised from $200B to ~$220B) — a single-name earnings reaction, not broad-based buying. Apple is the counterweight, down 7.2% on a Services/China revenue miss plus a fresh political headline (a senator publicly warning Apple against sourcing blacklisted Chinese chips). The 10-year Treasury yield spiking to 4.737% — its highest level since January 2025 — is a genuine cross-asset headwind that the premarket read at 16:05 did not fully capture; the 30-year is near 5.22%, a level not seen since 2007. Coinbase's Q2 miss ($359M net loss) adds a third real, confirmed single-name catalyst to the session.

Crypto stays the more internally-consistent, weaker picture: BTC downtrend, ETH transition_down, altcoin breadth ~45-53% above EMA20 depending on report, and macro/geopolitics risk pinned at the scale ceiling (100.0/100) all day on Iran-war headlines and sanctions news, compounded by a fresh Coldcard hardware-wallet exploit draining an estimated $38-40M. External sources confirm BTC and ETH both backed off an earlier bounce this morning — no internal/external divergence this cycle, unlike the stocks side at 16:05. BANK/USDT (Lorenzo Protocol) remains the standout mover, but this cycle's research finally surfaces a real, confirmed driver: concerns over insider-held float concentration after the protocol's foundation sent $13.7M in tokens to Aster, following a pattern that has burned other recently-rallied small-caps (a comparable token, LAB, collapsed 99% under similar float-concentration revelations).

### Market Mood / Risk Routing
- Crypto mood: **risk-off / chop** (macro risk 100/100 all day, BTC downtrend, ETH transition_down; internal and external reads agree this cycle)
- Stocks mood: **mixed / narrow risk-on** — index-level green but breadth is thin (AAPL a major single-name drag) and rising yields (10Y 4.737%, highest since Jan 2025) are a genuine offsetting headwind
- Dominant narrative: single-name earnings reactions (AMZN/AAPL/COIN) dominate over any broad sector or crypto narrative theme today; perps_dex_narrative (HYPE) and binance_ecosystem_teaser (BNB) remain the only active crypto baskets, both low-conviction
- Preferred side now: **catalyst-backed, RTH-confirmation-gated** — the day's edge is in the three confirmed single-name catalysts (AMZN/AAPL/COIN), not in chasing the index-level tape or in crypto (which stays wait-for-trigger)
- Best long candidate: AMZN — real catalyst, currently gated on an apparent false-positive legal flag; do not chase the existing +13-14% move even if the flag clears
- Best short candidate: AAPL (real catalyst, needs ORB confirmation) or COIN (real catalyst, needs RTH breakdown confirmation) — both watch-only, neither actionable pre-confirmation
- Best catalyst-backed candidate: COIN — the least ambiguous of the three (a clean earnings miss with a clean number, vs AMZN's gate question and AAPL's mix of earnings + political headline)
- What to avoid: BANK/USDT (already down 56-60% for the week, squeeze-prone if shorted now), chasing AMZN's existing move, new crypto scalp ideas (standing weekly loser), adding to the ESP/USDT swing long while its thesis remains contradicted by the weakest-symbols tables
- What would change the view: human resolution of the AMZN going_concern flag (would make AMZN the clear best long of the day if cleared); an ORB/RTH confirmation on AAPL or COIN; a `track-signals` fix restoring confidence in signal-outcome tracking

## 7. Candidate Deep Dives

### AMZN — long, MANUAL REVIEW REQUIRED (apparent false-positive legal gate)
- Has price already reacted to the catalyst? Yes — +13-14% intraday on the AWS-beat/EPS-beat print; this is not a fresh-entry setup on the catalyst alone.
- Is the setup chasing? Yes, if entered now, regardless of the gate question — the move has already happened.
- Retest/pullback structure? None established yet this session; would need to watch for one on this data pull.
- Overextended? Not ATR-quantified in this review (no chart-tool access this cycle — "TradingView / manual chart check unavailable"), but a same-day 13-14% move is large by any measure.
- Legal/headline risk check (mandatory, §I): the code's own `legal_risk.py` classifier tagged **going_concern** (a `BLOCKING_CATEGORIES` entry that auto-blocks A/B Telegram dispatch) and demoted the signal A→C. I searched `news_items` for AMZN + ("going concern" / "bankruptcy" / "chapter 11") across 72h and 7-day windows: **0 rows**. I searched the entire `news_items` table for any row ever tagged `going_concern` in `event_tags_json`: **0 rows, for any symbol, ever**. External WebSearch for `AMZN "going concern" 2026` returned no matching story; instead it returned strongly bullish analyst coverage (36/37 Buy ratings) and the confirmed earnings beat. **This is very likely a false-positive trigger** — possibly a stale cached flag, a misattributed basket-level `legal_risk` event (the swing report's §5b shows several unrelated `legal_risk`-tagged securities-fraud-solicitation headlines for other tickers — MSFT, RXT, Photronics, Alarum, FUTU — in the same catalyst cycle, raising the possibility of a symbol-attribution bug), or a keyword false-match somewhere in the pipeline I could not directly trace without reading the legal_risk source further than a read-only diagnostic pass allows in this review. See TODO-1.
- Per §I's letter, a verified legal/headline risk forces AVOID/MANUAL REVIEW — but here the risk itself could **not** be verified, only the demotion's *existence* was confirmed. This review is not authorized to override the system's own gate, so the practical verdict stays **MANUAL REVIEW REQUIRED**, not a clean actionable, until a human confirms or refutes the flag.
- **Verdict:** watch-only pending human review of the going_concern flag; do not chase the existing move regardless of outcome.

### AAPL — short-watch, ORB-gated
- Has price already reacted? Yes, -7.2% intraday on the Services/China miss.
- Is the setup chasing? The initial move yes; a continuation short after ORB confirmation would not be.
- Retest/pullback structure? Gate requires first-15m opening-range-breakdown or opening-drive confirmation before actionable — not yet satisfied per the report's own demotion reasoning.
- Legal/headline risk check: a Sen. Cotton headline warning Apple against using blacklisted Chinese chips (`t.me/WalterBloomberg`, per §4 of the stocks intraday report) — political/geopolitical, not a securities-fraud/going-concern category; does not auto-block, but is a real headline-risk data point supporting the short thesis, not contradicting it.
- Aligned with market mood? Yes — the one clear single-name weak spot in an otherwise green index tape.
- **Verdict:** short-watch; wait for RTH ORB/opening-drive confirmation below the session low before treating as actionable.

### COIN — short-watch, RTH-gated, cleanest catalyst of the day
- Q2 net loss $359M (EPS -$1.36 vs -$0.01 expected), revenue $1.2B vs $1.35B expected, spot trading volumes down >20% industry-wide — a clean, unambiguous earnings miss.
- Legal/headline risk check: a Coinbase-vice-chair "we won the war on crypto" headline in the swing report's risk-warnings section (`t.me/CoinMarketCapAnnouncements`) is geopolitical/sentiment framing, not a legal/fraud flag — noted, does not gate.
- Is the setup chasing? The initial post-earnings drop already happened (after-hours -6.5% reported externally); an intraday short would need the same ORB/RTH confirmation the report's actionability gate already requires.
- **Verdict:** short-watch; wait for RTH breakdown confirmation below the post-earnings session low.

### BANK/USDT (Lorenzo Protocol) — avoid now, short-watch only on failed-bounce retest
- Confirmed catalyst this cycle (unlike the 16:05 review's "no cited driver"): insider-float-concentration concern after a $13.7M token transfer from the protocol's foundation to Aster, echoing a prior small-cap (LAB) that collapsed 99% on a similar pattern.
- Already down ~56-60% over the week per external sources (internal report showed -29.34% in the most recent 24h snapshot — the weekly move is much larger than the daily one, i.e. the crash front-loaded earlier in the week and has decelerated somewhat).
- Derivatives: funding negative, shorts already crowded per the internal report — squeeze risk if shorted into an already-crowded position.
- Is this chasing? Yes, for a fresh short on the initial move. A confirmed failed-bounce retest (system's own conditional zone: 0.0633-0.0665 in the most recent report) would not be chasing.
- **Verdict:** avoid entering fresh in either direction now; short-watch only on a confirmed failed-bounce retest with funding/OI stabilization.

### ROBO/USDT — long-watch, cleanest technical setup, no catalyst
- Active B-tier swing signal, RS-leader (score 69.0, 24h +11.83%, RS vs BTC +13.87%), playbook `crypto_swing_narrative_rs_momentum` carries a 14d 72% WR / PF 5.80 / +24R track record.
- No fresh verified catalyst — this is a pure momentum/RS setup in a market the desk itself classifies as range/chop.
- Entry not yet triggered: defined pullback zone 0.0140-0.0143, invalidation 0.0136.
- Is this chasing? No — price has not reached the entry zone; this is a genuinely clean, not-yet-actionable watch.
- **Verdict:** long-watch; fill only on a pullback into 0.0140-0.0143, not a market chase at the current 0.0145.

## 8. Best Candidates Ranked

1. **COIN** — short-watch; cleanest, least ambiguous confirmed catalyst (earnings miss); trigger: RTH breakdown below the post-earnings session low.
2. **AAPL** — short-watch; real catalyst (earnings + political headline); trigger: ORB/opening-drive confirmation below the session low.
3. **AMZN** — long-watch, MANUAL REVIEW REQUIRED; real catalyst but gated by an apparent false-positive going_concern flag; trigger: human confirmation the flag is erroneous, and even then, wait for a pullback rather than chasing +13-14%.
4. **ROBO/USDT** — long-watch; cleanest crypto technical setup, no catalyst; trigger: fill on pullback into 0.0140-0.0143.
5. **BANK/USDT** — avoid now; short-watch only on a confirmed failed-bounce retest into 0.0633-0.0665.

## 9. Avoid / No Trade

This applies to the current decision window only — scanning, tracking, and monitors continue regardless.

- **BANK/USDT initial-move shorting** — already down 56-60% for the week, squeeze-prone, already-crowded shorts.
- **Chasing AMZN's existing +13-14% move** — regardless of how the legal-gate question resolves.
- **New crypto scalp ideas** — mode remains a standing weekly loser (PF 0.2, avgR -0.21, n=24); no candidates surfaced this cycle anyway.
- **Adding to the ESP/USDT swing long** — thesis remains contradicted by both the 12:16 intraday and 16:34 swing reports' weakest-symbols tables; carried, not re-litigated in full this cycle.
- **Pre-ORB entries on AAPL or COIN** — both real catalysts, neither RTH-confirmed yet.

## 10. Main Risks

- **AMZN going_concern flag appears to be a false positive blocking the day's single largest, most fundamentally-clean long candidate** — the highest-impact finding of this review; needs human audit of `src/stocks/legal_risk.py`'s AMZN trigger. See TODO-1.
- **`track-signals` pipeline crash, now confirmed through a 3rd consecutive failure at 18:41** — signal-outcome tracking may be silently missing data across an extended window today. See TODO-2 (escalated).
- **10-year Treasury yield at its highest level since January 2025 (4.737%)** — a genuine cross-asset equity headwind not fully priced into the narrow AMZN-led index rally; watch for this to broaden the AAPL-style weakness into other rate-sensitive names.
- **BANK/USDT squeeze risk** — funding already negative/crowded; a short entered now (rather than on a confirmed retest) risks a violent reclaim.
- **ESP/USDT live-position contradiction persists** (swing long vs. weakest-symbols tables in two consecutive fresher reports) — monitor-only, not re-verified in full this cycle given the 5-candidate cap.
- **Catalyst mapping still >60% unmapped** — treat the catalyst layer as context only, not a final-decision input, for any candidate not independently verified via `news_items` or external search (as done for AMZN/AAPL/COIN/BANK this cycle).

## 11. Action Plan — next 4 hours

1. Do not chase AMZN's existing move; flag the going_concern gate for human audit (TODO-1) — if cleared, watch for a pullback rather than an immediate entry.
2. Watch AAPL for an ORB/opening-drive confirmation below the session low before treating the short as actionable.
3. Watch COIN for an RTH breakdown confirmation below its post-earnings session low.
4. Watch ROBO/USDT for a fill into its 0.0140-0.0143 pullback zone; do not chase at the current 0.0145.
5. Leave BANK/USDT alone in both directions unless a confirmed failed-bounce retest into 0.0633-0.0665 appears.
6. Do not add to the ESP/USDT swing long; monitor its existing 0.066305 invalidation only.
7. No action on the `track-signals` crash or the AMZN legal-risk classifier from this review (both are code-level issues, out of scope) — both flagged in §14 for a human-driven session.
8. Re-check at the 21:30 EEST late-session risk review whether the AAPL/COIN shorts confirmed or failed, and whether AMZN's gate has been human-reviewed.

## 12. Final Verdict per Mode

- **Crypto scalp:** No trade — mode is a standing weekly loser (PF 0.2, n=24); no candidates surfaced this cycle. Data collection only.
- **Crypto intraday:** No new A/B this cycle. Existing B-tier positions (GIGGLE, PUMP, FIL, BCH) continue per their own entry/invalidation levels.
- **Crypto swing:** ROBO/USDT is the cleanest long-watch (pullback zone, not yet filled). ESP/USDT triggered and live but thesis-contradicted — monitor only, do not add. No new entries recommended beyond ROBO's defined zone.
- **Stocks intraday:** No trade actionable pre-confirmation. AAPL (short) and COIN (short) are RTH/ORB-gated watch-only ideas; AMZN (long) is gated on an apparent false-positive legal flag requiring human review — do not treat as SUPPORT until resolved.
- **Stocks swing/invest:** Deprecated/removed playbooks, not evaluated (see [[project_crypto_ai_desk_stocks_position_framework]]).

## 13. Sources

- [Stock Market Today (July 31, 2026): S&P 500 slips as bond yields surge, Apple slides — TheStreet](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-july-31-2026) (WebSearch, 2026-07-31)
- [Stock market today: Dow, S&P 500, Nasdaq seesaw as 10-year yield surges — Yahoo Finance](https://finance.yahoo.com/markets/live/stock-market-today-friday-july-31-dow-sp-500-nasdaq-081227738.html) (WebSearch, 2026-07-31)
- [Amazon Stock Jumps 9% as AWS Growth Hits 37% and Revenue Tops $200 Billion — FX Leaders](https://www.fxleaders.com/news/2026/07/31/amazon-stock-jumps-9-as-aws-growth-hits-37-and-revenue-tops-200-billion/) (WebSearch, 2026-07-31)
- [Amazon (AMZN) Q2 earnings report 2026 — CNBC](https://www.cnbc.com/2026/07/30/amazon-amzn-q2-earnings-report-2026.html) (WebSearch, 2026-07-31)
- [Coinbase Q2 2026 earnings miss: $359 million net loss — Yahoo Finance](https://finance.yahoo.com/markets/crypto/articles/coinbase-q2-2026-earnings-miss-144916215.html) (WebSearch, 2026-07-31)
- [Coinbase (COIN) sinks 5% after missing Q2 revenue estimates — CoinDesk](https://www.coindesk.com/markets/2026/07/30/coinbase-sinks-5-after-missing-q2-revenue-estimates) (WebSearch, 2026-07-31)
- [Bitcoin and ethereum prices today, Friday, July 31, 2026 — Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-july-31-2026-crypto-prices-back-off-this-morning-130657761.html) (WebSearch, 2026-07-31)
- [Crypto News On July 31: Bitcoin Rises, GRVT Gains 62%, BANK Drops 57% — CoinGabbar](https://www.coingabbar.com/en/crypto-currency-news/crypto-news-today-31-july-bitcoin-eth-grvt-defi-uniswap-gains) (WebSearch, 2026-07-31)
- [Lorenzo Protocol (BANK) Rallies on BTCfi and Yield Trends — Tapbit](https://www.tapbit.com/en/learn/article/lorenzo-protocol-bank-token-price-rally-july-2026-20260721) (WebSearch, 2026-07-31)
- [Michael Saylor's New MSTR Playbook Is Already Costing Investors: 17% of Bitcoin Sale Capacity Gone — 24/7 Wall St.](https://247wallst.com/investing/2026/07/06/michael-saylors-new-mstr-playbook-is-already-costing-investors-17-of-bitcoin-sale-capacity-gone/) (WebSearch, 2026-07-31)
- Internal: `data/reports/stocks/intraday/2026-07-31_13-37_stocks_intraday_report.md` §7 (AMZN/AAPL/COIN demotion reasons); `news_items` direct SQL query (AMZN going_concern verification — 0 rows found, all windows); `src/stocks/legal_risk.py` (read-only, for the `going_concern` regex/blocking-category definition)

## 14. Fix Requests / TODO

### TODO-1 (new, high priority): AMZN `going_concern` legal-risk flag appears to be a false positive
- **issue:** AMZN (score 94.7, A-tier pre-gate) was demoted A→C this cycle for "active legal/headline risk (going_concern) — manual review required," which auto-blocks Telegram A/B dispatch per `src/stocks/legal_risk.py`'s `BLOCKING_CATEGORIES`. No supporting evidence was found: `news_items` has zero rows for AMZN matching "going concern"/"bankruptcy"/"chapter 11" language in 72h or 7-day windows, and zero rows in the entire table were ever tagged `going_concern` in `event_tags_json` for any symbol. External WebSearch found no going-concern story for AMZN in 2026 at all — instead a blowout Q2 beat and 36/37-analyst Buy consensus.
- **evidence:** `data/reports/stocks/intraday/2026-07-31_13-37_stocks_intraday_report.md` line 178 ("AMZN (long) (was A): score 95 · watchlist / not actionable — tier demoted A→C: active legal/headline risk (going_concern) — manual review required"); `news_items` SQL query this run (0 rows, both narrow and broad searches); WebSearch `Amazon AMZN "going concern" 2026` (no matching result).
- **suggested manual fix:** Trace the specific input that set the `going_concern` flag for AMZN this cycle (likely a stale cached legal-risk record, a symbol-attribution bug pulling in an unrelated basket-level `legal_risk` headline — several unrelated tickers, e.g. MSFT/RXT/Photronics/Alarum/FUTU, show `legal_risk`-tagged securities-fraud-solicitation headlines in the same catalyst cycle — or a regex false-match somewhere in `src/stocks/legal_risk.py`'s scanning path). Given AMZN was the day's single largest fundamentally-clean catalyst candidate, this is a high-value fix.
- **priority:** high
- **first observed:** 2026-07-31 18:47 EEST (this review).

### TODO-2 (escalated, high priority): `track-signals` crash now confirmed through a 3rd consecutive cycle today
- **issue:** `track-signals (pre)` and `(post)` failed with `exit=1` at 14:55, 16:38, and again 18:41 — the same recurring failure documented in the 16:05 and earlier reviews, now spanning the entire day (04:30 through 18:41+).
- **evidence:** `data/scheduled_runs/2026-07-31_default_schedule/scheduler.log` lines showing `CMD END: track-signals (pre) exit=1` at 14:55:45 and 18:41:32, and `CMD END: track-signals (post) exit=1` at 16:38:24.
- **suggested manual fix:** Same as prior reviews — guard the `level_hold_plan.get("applied")` call for `None` in `src/signals/tracker.py`, or fix the upstream step that should populate `level_hold_plan`. Given the now-confirmed all-day recurrence, verify no signal outcomes were silently missed across today's full window once fixed.
- **priority:** high
- **first observed:** 2026-07-31 04:30 EEST; still open as of 18:41 EEST (3rd+ confirmed consecutive failure today).

### TODO-3 (carried, not re-verified this cycle): PLTR `legal_headline_risk: sec_doj` flag still looks like a false positive
- **issue:** Carried from prior reviews (2026-07-30 11:45 EEST onward). Not re-searched this cycle — time was prioritized toward the new, larger AMZN finding above.
- **evidence:** Prior reviews' WebSearch found no official 2026 SEC/DOJ action for PLTR, only 2025-dated shareholder-law-firm solicitation boilerplate.
- **suggested manual fix:** Unchanged — audit the `legal_headline_risk`/`sec_doj` classifier's source data for PLTR; down-weight generic shareholder-solicitation boilerplate. Given the AMZN finding above, this specific classifier family (`src/stocks/legal_risk.py` and its upstream news-tagging) may benefit from a single combined audit pass.
- **priority:** high
- **first observed:** 2026-07-30 11:45 EEST; not re-verified 2026-07-31 18:47 EEST.

### TODO-4 (carried, not re-verified this cycle): META `legal_headline_risk` mislabeled as "indictment"
- **issue:** Carried from prior reviews, not re-searched this cycle.
- **evidence:** Prior reviews' `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md` output (`sig_192e0beccf98e2a3` META — LEGAL_RISK, tagged "indictment").
- **suggested manual fix:** Unchanged — correct the legal-risk taxonomy/label for META from "indictment" to "civil_litigation" or similar.
- **priority:** medium
- **first observed:** 2026-07-30 11:45 EEST; not re-verified 2026-07-31 18:47 EEST.

### TODO-5 (carried, unchanged reading): catalyst mapping still >60% unmapped
- **issue:** 1592 of 2500 catalyst events today have no resolved symbol (63.7% unmapped) — same reading as the 16:05 review (no new catalyst cycle completed between then and this review).
- **evidence:** live count of `data/catalysts/2026-07-31/catalyst_events.jsonl` this run: 908 mapped / 1592 unmapped.
- **suggested manual fix:** Unchanged — continue widening/improving the symbol resolver per [[project_crypto_ai_desk_catalyst_linkage]].
- **priority:** medium-high
- **first observed:** recurring; unchanged reading since 16:05 EEST today.

### TODO-6 (carried, not re-verified): ESP/USDT swing long vs weakest-symbols contradiction persists into a 3rd report
- **issue:** The active ESP/USDT swing long (triggered, score 73.2) continues to appear in the "Weakest Symbols" table of both the 12:16 intraday report and now the fresher 16:34 swing report (bias short, 24h -10.89%, RS vs BTC -8.86%) — the same contradiction first flagged at 16:05, now confirmed in a second, even-fresher report.
- **evidence:** `python -m src.cli active-signals --asset-class crypto` (ESP/USDT swing, triggered, score 73.2) vs `data/reports/swing/2026-07-31_13-34_swing_report.md` line 49 ("ESP/USDT: bias short, 24h -10.89%, RS vs BTC -8.86%").
- **suggested manual fix:** Unchanged from 16:05 — consider a lightweight cross-timeframe consistency check that flags when an active position's symbol appears in the opposite-bias top-movers/weakest-symbols table of a fresher same-day report.
- **priority:** low-medium
- **first observed:** 2026-07-31 16:05 EEST; reconfirmed 2026-07-31 18:47 EEST (now in a 2nd fresher report).
