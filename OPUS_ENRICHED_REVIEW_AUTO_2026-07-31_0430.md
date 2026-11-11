# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:30 EEST

## 1. Executive Summary

Slot: **crypto overnight / Asia review** (target 04:30 EEST, actual data pull ~04:39-04:50 EEST — within tolerance). **Advisory only — no auto-trade, no scoring/threshold/strategy changes.** External web research was available and used this run. Stocks are closed at this hour (US cash session); stock signals below are planning/watchlist context only. **Zero A-tier signals anywhere** (crypto or stocks) and zero freshly-triggered B-tier crypto ideas this cycle — the desk is in a genuine no-fresh-idea window, not a system failure. Crypto scalp remains kill-switched (mode disabled); scalp's trailing stats are badly negative (PF 0.25, 0W/4L, n=25 weak-confidence) but that's a stale/expected artifact of the kill-switch, not a live risk. Macro backdrop is a real risk-off headline overhang, externally confirmed: Russia launched its **largest aerial attack of the war** overnight (reported ~40-41 missiles aimed at Kyiv), driving the internal macro risk score to 99-100/100 — this is a genuine, current event, not stale data. Crypto regime itself still reads bullish-trend/risk-on internally (BTC transition_up, ETH uptrend, altcoin breadth 64% above EMA20), so the desk faces a **mixed** setup: bullish tape, risk-off headlines. **Best long/catalyst-watch is ONDO/USDT** (swing B, waiting_for_entry, score 79.2, externally-confirmed RWA catalyst cluster: Ondo Network launch, FINRA broker-dealer approval, DTCC tokenized-equity testing) — but the last known price (0.4127, ~9h-old swing snapshot) sits only ~0.4% above the entry zone top, so this needs a fresh price check before treating as imminent. **Best avoid/short-squeeze-risk name is BANK/USDT** (Lorenzo Protocol) — internal data shows a -60% to -63% 24h collapse with extreme negative funding and rising OI (fresh shorts pressing into an exhausted long squeeze setup); external search only surfaced the mid-July rally to ATH, not today's crash, so the collapse itself is **internally-sourced only this cycle** — do not chase either direction. **GIGGLE/USDT** (best catalyst-watch candidate on score) carries a real contradiction: internal scoring shows "no fresh verified catalyst," but CZ was publicly responding to Giggle Academy meme-coin donation-selling criticism as of yesterday/today — a live social-controversy catalyst the internal pipeline is not yet capturing. A genuine **new data-quality bug** surfaced this cycle: the post-cycle `track-signals` step crashed with `AttributeError: 'NoneType' object has no attribute 'get'` in `tracker.py:1081`, meaning this cycle's signal-outcome tracking pass did not complete — flagged as a high-priority TODO, not fixed. Stocks remain closed; **NVDA** is carried forward as the cleanest stocks short-watch (Michael Burry's NVDA/semiconductor short thesis is externally verified across multiple independent outlets), though the internal scanner this cycle actually reads NVDA as `no_directional_setup` (score 46.13) — a contradiction to resolve at the 16:20 pre-open review. AMZN's Q2 beat (+~10% after-hours) is now externally confirmed (partially resolves TODO-12); MSTR's after-hours price move is still not confirmed, but the fundamental facts are (an $8.22B GAAP loss on BTC marks vs a $10.02B profit a year ago, revenue miss). Catalyst mapping is weak this run (51.6% unmapped, just over the 50% threshold) — use catalyst layer as context only. Scanning, tracking, and monitors continue in every mood; this review recommends selective caution overnight into Europe, never a stop.

**Status headline (Paper Monitor, 01:55 EEST, ~2h50m old — carried, no fresher pull this cycle):** Open actionable: 5 · Waiting for entry: 4 · Entered unresolved: 7 · Review/Shadow: 42 · No-entry/stale/moved-away: 62 · Needs review: 5. Note: this cycle's `track-signals (post)` step crashed before it could refresh these counts (see §3, §14 TODO-NEW-1) — treat as the last-known-good snapshot, not a live count.

## 2. Data Used

| File / Source | mtime (local) | Age |
|---|---|---|
| `data/reports/scalp/2026-07-31_01-09_scalp_report.md` | 04:09:54 EEST | ~35min — fresh |
| `data/reports/intraday/2026-07-31_01-17_intraday_report.md` | 04:17:12 EEST | ~28min — fresh |
| `data/reports/swing/2026-07-30_16-50_swing_report.md` | 19:50 EEST (prior day) | ~9h — carry-forward (4-12h bucket), no fresher swing regen this cycle |
| `data/reports/stocks/intraday/2026-07-31_01-39_stocks_intraday_report.md` | 04:39 EEST | fresh (market closed, planning only) |
| `data/reports/stocks/swing/…` / `invest/…` (2026-07-02) | stale (~4 weeks) | deprecated/removed playbooks, see [[project_crypto_ai_desk_stocks_position_framework]] — excluded, not a freshness failure |
| `data/catalysts/2026-07-31/catalyst_events.jsonl` (500 rows) + `narrative_baskets.jsonl` (4 baskets) + `catalyst_cycle_01-21.md` | 04:21 EEST | ~24min — fresh |
| `data/scheduled_runs/2026-07-30_default_schedule/scheduler.log` + `cycle_04_00-54_summary.md` | 01:42 / 02:01 EEST | ~3h / ~2h44m — inside 3h non-defer window |
| `reports/PAPER_MONITOR_STATUS_LATEST.md` | 01:55 EEST | ~2h50m — carried (see status caveat above) |
| `python -m src.cli active-signals --asset-class crypto` / `stocks` | live query | now |
| `python -m src.cli signal-stats --asset-class crypto` / `stocks` | live query | now |
| `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-31` | live query | now — none found |
| Prior review `OPUS_ENRICHED_REVIEW_AUTO_2026-07-30_2330.md` (post-close final daily review) | 23:30 EEST prior day | for §4 diff |
| WebSearch: BTC/ETH price Jul 31, AMZN/MSTR earnings reaction, Russia-Ukraine crypto reaction, GIGGLE Academy news, BANK/Lorenzo Protocol news, ONDO RWA news, Michael Burry NVDA short | live | now |

**External web research was available and used this run.**

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime 01:42 EEST (~3h old at cutoff, but latest cycle summary is fresher); `cycle_04_00-54_summary.md` mtime 02:01 EEST (~2h44m old) — well within the 3h non-defer window. No defer needed.
- Cycle 4 (00:54-02:01 EEST) ran 71 steps, **5 FAIL**:
  - **`track-signals (post)` — NEW, high-priority.** `AttributeError: 'NoneType' object has no attribute 'get'` at `src/signals/tracker.py:1081` (`level_hold_plan.get("applied")` — `level_hold_plan` is `None`). This cycle's signal-outcome tracking pass did not complete. See §14 TODO-NEW-1.
  - `stocks intraday report` (exit=1, 127.4s) — logged mid-fetch at 01:38 EEST; a fresh, complete stocks-intraday report file exists at 01:39 EEST mtime, so this looks like a transient failure superseded by a successful retry/rerun in the same cycle window, not a current data gap. Low priority, noted for awareness only.
  - `intelligence layer update` (300.0s timeout), `latency acceptance report` (300.0s timeout), `refresh obsidian dashboard` (300.1s timeout) — same 300s-timeout pattern flagged in the prior review's TODO-13 (DB lock contention). TODO-13 itself did NOT recur this cycle (`paper stock direction (multi-factor)` succeeded in 78.1s, `entry-mode-calibration-refresh` succeeded without a lock error) — but three *different* steps hit the same symptom tonight. Bundled into §14 TODO-NEW-2 (recurring pattern, not the same step each time).
- Crypto scalp (04:09 EEST) and intraday (04:17 EEST) reports both regenerated fresh this cycle.
- Crypto swing report (19:50 EEST prior day, ~9h old) is carry-forward — inside the 4-12h bucket, flagged per policy; ONDO/USDT's price context below uses this carried snapshot and should be re-verified for a live price before acting.
- Stocks-intraday report (04:39 EEST) fresh; market closed, `market_closed_intraday_planning_only` gate correctly active.
- Catalyst JSONL refreshed at 04:21 EEST: **500** events, **242 mapped (48.4%)**, **258 unmapped (51.6%)** — weak-mapping threshold breached (just over 50%). See §5.
- `detect_untracked_legacy_alerts --since 2026-07-31`: **None** — every legacy crypto alert has a backing proposed_signal. Integrity clean.
- Paper Monitor Status (01:55 EEST, ~2h50m old, no fresher pull possible this cycle since `track-signals (post)` crashed before it could refresh the underlying counts): Open actionable 5, Waiting for entry 4, Entered unresolved 7, Review/Shadow 42, No-entry/stale/moved-away 62, Closed today 148W/17L/13flat, Needs review 5.
- `PAPER_MONITOR_STATUS_LATEST.md` and `active-signals` both still show the recurring `UNKNOWN_INCONSISTENT` lifecycle-mapping issue (count=5, unchanged) — TODO-3 carried forward, re-confirmed fresh this cycle (cheap read, not re-derived from stale prior-review text).
- Zero A/B-tier newly-triggered ideas this cycle across scalp (kill-switched, correctly), intraday, and swing beyond signals already carried from earlier cycles (GIGGLE, ROBO, PUMP, MMT, FIL, BCH, ADA — all `waiting_for_entry` or `triggered`, none new tonight).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-07-31 04:45 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["scheduler_fresh", "catalyst_missing", "report_stale"],
      "data_missing": ["fresh Paper Monitor status counts (track-signals post crashed before refresh)", "live ONDO/USDT price (swing snapshot is ~9h old)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log ~3h old, cycle_04 summary ~2h44m old, both inside 3h non-defer window", "scalp/intraday/stocks-intraday all regenerated fresh this cycle", "swing report ~9h old, carry-forward bucket", "catalyst JSONL: 500 rows, 242 mapped (48.4%) / 258 unmapped (51.6%)", "detect_untracked_legacy_alerts: none", "track-signals (post) crashed with AttributeError, tracker.py:1081", "3 unrelated steps hit 300s timeouts this cycle (intelligence layer update, latency acceptance report, obsidian dashboard)"] },
    { "agent": "market_regime", "verdict": "mixed", "confidence": 0.68,
      "reason_codes": ["mixed", "risk_on", "risk_off", "chop"],
      "data_missing": ["confirmed Asia-session BTC/ETH price action for Jul 31 specifically"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Internal crypto regime: bullish trend, BTC transition_up, ETH uptrend, altcoin breadth 64.1% above EMA20 (04:17 EEST intraday snapshot)", "Internal stocks regime (context only, market closed): risk_off/short bias, breadth 25% above EMA20, VIX 17.09", "Macro/geopolitics risk score 99-100/100 — Russia's largest aerial attack of the war overnight, externally confirmed (~40-41 missiles at Kyiv), a genuine current event not stale data", "External: BTC/ETH prices as of Jul 30 close (~$63.9-64.8K BTC, ~$1908-1923 ETH per Yahoo Finance); no confirmed Jul 31 Asia-session move found via WebSearch this cycle"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "catalyst_contradicted", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl: 500 rows, 242 mapped (48.4%), 258 unmapped (51.6%) — weak-mapping threshold breached", "ONDO/USDT: canonical catalyst importance 0.95 ('Ondo launches private execution network'), rwa_narrative basket hot (heat 74.4/100) — externally corroborated (Ondo Network launch, FINRA approval, DTCC tokenized-equity testing, all July 2026)", "GIGGLE/USDT: internal pipeline shows 'no fresh verified catalyst detected' but external search finds a live CZ-vs-critics controversy over Giggle Academy donated-token selling, published Jul 30-31 — genuine catalyst_contradicted case", "BANK/USDT: internal -60% to -63% 24h collapse not corroborated externally this cycle (search only surfaced the mid-July rally to ATH); treat the crash narrative as internal-only until externally confirmed"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["squeeze_risk", "funding_extreme", "oi_supports", "data_unavailable"],
      "data_missing": ["OI change 'n/a' for several intraday symbols this cycle (ROBO, MMT, GIGGLE, BANK, RE via mexc fallback)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BANK/USDT: funding -0.003511 (mexc) to -0.01435855 (bybit external), 24h move -61% to -63%, crowding 'unknown'/'elevated' — fresh shorts pressing an already-capitulating token, classic squeeze-risk-both-ways setup", "ONDO/USDT (19:50 EEST swing snapshot): price up + OI up +10.1%, funding near-zero, crowding normal — fresh positioning confirms trend, no red flag", "DEXE/USDT, RE/USDT, ALLO/USDT: all short-squeeze-risk-capped to C-tier per internal rules (thin liquidity / high upper wick / extreme negative funding against the short) — correctly filtered, not actionable"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["stale_before_entry", "entry_fresh", "clean_retest", "price_moved_away"],
      "data_missing": ["TradingView / manual chart check unavailable this run", "live ONDO/USDT price (last known 0.4127 is ~9h old)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ONDO/USDT: last known price 0.4127 (19:50 EEST) vs entry zone 0.4078-0.4112 — ~0.4% above zone top at last check, the closest-to-actionable name on the desk, but the snapshot itself is 9h stale so this must be re-verified before acting", "GIGGLE/USDT: current price 30.15, C-tier/watchlist only, score 65.7, pullback zone 29.522-29.957 — not yet in zone, 'do not chase' language applies", "No B-tier crypto setup newly triggered this cycle; all live signals are carried from earlier cycles"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["waiting_for_entry", "review_shadow", "no_entry", "needs_review"],
      "data_missing": ["fresh lifecycle counts — track-signals (post) crashed this cycle before refreshing them"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Last-known Paper Monitor snapshot (01:55 EEST, carried): Open actionable 5, Waiting for entry 4, Entered unresolved 7, Review/Shadow 42, No-entry/stale/moved-away 62, Needs review 5, Closed today 148W/17L/13flat", "35 live crypto signals in active-signals, mostly B-tier waiting_for_entry/triggered/tp-ladder rows; several with already-passed expires_at timestamps (recurring display artifact, TODO-3, unchanged n=5 UNKNOWN_INCONSISTENT)", "Stocks: 50 non-terminal legacy rows, all C-tier or legacy; zero A/B actionable (market closed, correctly gated)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.72,
      "reason_codes": ["headline_risk", "reduce_risk", "manual_review", "legal_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Macro risk score 99-100/100, externally confirmed largest Russia aerial attack of the war overnight — real, current headline risk", "PLTR (sec_doj) and META (indictment) legal-flag demotions still active in tonight's stocks report (§7 of stocks-intraday), unresolved for a 5th+ consecutive cycle — TODO-1/TODO-2 carried, not re-verified externally this cycle (no new evidence either way)", "XOM: earnings today (2026-07-31), do_not_chase_warning active in crypto reports' production risk-warnings section (cross-asset carry-through, correctly surfaced)", "BANK/USDT squeeze-both-ways risk (see derivatives_squeeze) — recommend no new position either direction"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto A/B headline (week, n=99, stronger confidence): winrate 25.0%, PF 2.24, avgR 0.33, totalR +22.3 — net-positive, consistent with prior reviews", "By mode: intraday n=39 PF 4.68 avgR 0.97 (strong); swing n=35 PF 1.77 avgR 0.24 (solid); scalp n=25 PF 0.25 avgR -0.16, 0 wins / 4 losses (weak confidence) — scalp remains correctly kill-switched, this is a stale/expected artifact not a live risk", "Stocks A/B headline: n=4 anecdotal, winrate 0%, PF 0.0 — too small a sample to act on, but directionally consistent with stocks C-tier being badly negative (PF 0.11, n=200) — reinforces the existing 'stocks C-tier never actionable' policy"] },
    { "agent": "head_trader", "verdict": "watch_only", "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "ONDO/USDT", "trigger": "confirm live price re-enters 0.4078-0.4112 pullback zone on fresh data (last known 0.4127 is 9h stale); RWA catalyst externally confirmed (Ondo Network, FINRA, DTCC)", "reason": "highest-score live B-tier (79.2), narrative basket hot, no contradiction found" },
    "best_short_candidate":    { "symbol": "BANK/USDT", "trigger": "wait for external confirmation of the -60%+ collapse cause and for funding/crowding to stabilize before entering either direction; do not short into a possible squeeze, do not buy the capitulation blind", "reason": "extreme negative funding + rising OI = classic squeeze-risk-both-ways, internally-sourced crash not yet externally corroborated" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT", "trigger": "same as best_long_candidate — catalyst is the strongest, externally-verified leg of this idea", "reason": "canonical catalyst importance 0.95, RWA basket heat 74.4/100, 3 independent external corroborations this cycle" },
    "avoid_candidate":         { "symbol": "BANK/USDT", "reason": "squeeze-risk-both-ways, unconfirmed externally, extreme funding — avoid new positions until data stabilizes" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 8
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.70 | scheduler_fresh, catalyst_missing, report_stale | advisory_only |
| market_regime | mixed | 0.68 | mixed, risk_on, risk_off, chop | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, fresh_catalyst, catalyst_contradicted, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.65 | squeeze_risk, funding_extreme, oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | stale_before_entry, entry_fresh, clean_retest, price_moved_away | advisory_only |
| execution_lifecycle | caution | 0.65 | waiting_for_entry, review_shadow, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.72 | headline_risk, reduce_risk, manual_review, legal_risk | advisory_only |
| playbook_performance | caution | 0.75 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | watch_only | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-07-30_2330.md` (post-close final daily review, 23:30 EEST):

- **New**: track-signals (post) crash (TODO-NEW-1) and a bundled 3-step timeout pattern (TODO-NEW-2) — neither was present in the prior cycle's step log.
- **Resolved**: TODO-13 (paper stock direction timeout) did NOT recur this cycle — step succeeded in 78.1s.
- **Partially resolved**: TODO-12 (AMZN/MSTR after-hours reaction unconfirmed) — AMZN now confirmed (+~10% AH on the beat); MSTR's exact after-hours % move is still not found via WebSearch, but the underlying fundamentals (an $8.22B loss vs $10.02B prior-year profit, revenue miss) are confirmed and internally reflected via the `stale_post_earnings_setup` demotion.
- **Improved but still open**: TODO-5 (catalyst mapping weak) — 51.6% unmapped tonight vs 68.3% at 23:30 EEST, a meaningful improvement, but still above the 50% threshold.
- **Unchanged / still open**: TODO-1 (PLTR sec_doj false-positive suspected), TODO-2 (META indictment mislabel suspected), TODO-3 (UNKNOWN_INCONSISTENT=5, unchanged count), TODO-9 (binance_ecosystem_teaser basket still present, not re-verified).
- **Thesis carried, not invalidated**: ONDO/USDT remains the best long/catalyst-watch (same symbol as the 23:30 review), BANK/USDT remains the top avoid/squeeze-risk name (same symbol, same direction of concern). No crypto A/B position closed or newly opened between the two reviews beyond the normal tp-ladder rows already tracked.
- **New this cycle**: GIGGLE/USDT catalyst-contradiction flagged (CZ-vs-critics controversy) — not present in the 23:30 review's discussion of GIGGLE.

## 5. Catalyst Coverage

- Total `catalyst_events` today: **500**
- Mapped (non-null symbol): **242 (48.4%)**
- Unmapped (null symbol): **258 (51.6%)**
- `narrative_baskets`: **4** (perps_dex_narrative, binance_ecosystem_teaser, ai_narrative, rwa_narrative)
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (51.6% unmapped, just over the 50% threshold; a real improvement vs 68.3% at the last review, but not yet resolved.)
- Top 3 unmapped headlines: (1) "💵 250,000,000 $USDC minted at USDC Treasury" (Whale Alert-style mint notice, no ticker resolvable to a tradeable symbol); (2) "#Bithumb News 자산 화면 개편 안내 / Asset screen reorganization information" (Korean-language exchange UI notice); (3) "LATEST: 📊 Institutions accounted for a record 72% of spot OTC flow in H1 2026... per Wintermute" (macro/industry stat, no single symbol).

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **mixed** — internal regime bullish-trend/risk-on (BTC transition_up, ETH uptrend, 64.1% of alts above EMA20) vs a genuinely risk-off macro overlay (Russia's largest aerial attack of the war overnight, externally confirmed, macro risk score 99-100/100).
- Stocks mood: **closed** (planning/watchlist only; internal regime reads risk_off/short-biased, VIX 17.09, breadth 25% above EMA20 — narrow, not broad-based, consistent with the prior review's "narrow mega-cap rally" thesis; AMZN's strong beat overnight is a fresh bullish data point for the AI/cloud trade specifically, not yet reflected in breadth).
- Dominant narrative: **RWA/tokenization** (ONDO primary, heat 74.4/100, hot status) is the cleanest, externally-corroborated crypto narrative right now. `perps_dex_narrative` (HYPE) and `ai_narrative` (NEAR/RENDER/TAO/FET) are live but not corroborated externally this cycle.
- Preferred side now: **wait-for-trigger** — no fresh A/B setup exists; the desk's job right now is watching ONDO re-enter its zone and watching whether BANK's collapse gets external confirmation, not forcing a new trade.
- Best long candidate: **ONDO/USDT** — trigger: live price back inside 0.4078-0.4112 with volume, RWA catalyst intact.
- Best short candidate: **none clean** — BANK/USDT is the most extended short-side name but is squeeze-risk-both-ways, not a clean short; trigger to make it actionable: external confirmation of the crash driver + funding/OI stabilizing (not still accelerating negative).
- Best catalyst-backed candidate: **ONDO/USDT** (see above).
- What to avoid: **BANK/USDT** (either direction), any no-catalyst crypto intraday chase (internal playbook note: "no-catalyst intraday in chop is net-negative, 14d WR 23%/PF 0.70/-3R" — applies to GIGGLE/PUMP/ROBO/MMT/ESP/FIL, all currently C-tier watchlist-only for exactly this reason), PLTR/META stock shorts pending legal-flag review (TODO-1/2), NVDA stocks entries before the internal no_directional_setup vs external Burry-short contradiction is resolved.
- What would change the view: a fresh, externally-confirmed BTC/ETH Asia-session price read (not found this cycle); ONDO price re-entering its zone on live data; external confirmation (or refutation) of BANK's collapse driver; NVDA's internal score reconverging with the externally-verified Burry short thesis.

## 7. Candidate Deep Dives

### 7.1 ONDO/USDT — best long / catalyst-watch (swing, B-tier, score 79.2, waiting_for_entry)

- Has price already reacted to the catalyst? Partially — 24h return was +4.83% as of the 19:50 EEST swing snapshot, RS vs BTC +3.28%, volume 2.84x average (unusual-volume flagged). The catalyst (Ondo Network launch, "near-CEX speed" private execution) is externally corroborated by three independent sources this cycle (CoinDesk, plus FINRA/DTCC context).
- Is the setup chasing? No — price (0.4127 last known) sits just ~0.4% above the pullback entry zone (0.4078-0.4112), the tightest gap of any live crypto idea on the desk.
- Is there a retest/pullback structure? Yes, that's exactly the current setup — waiting for price to accept back inside the zone rather than extend.
- Overextended (>2 ATR from EMA20)? No indication in the data; ATR 0.0075, current price only ~0.2 ATR above the zone top at last check.
- Would entry now be late? Marginally, if the 9h-old snapshot is still accurate — but this must be re-verified with live data before acting; do not treat the 19:50 EEST price as current.
- What level makes it actionable? A confirmed 1h/4h close inside 0.4078-0.4112 with volume, per the swing playbook.
- Aligned with market mood? Yes — RWA is the one narrative with a hot basket and no external contradiction this cycle.
- Long, short, or wait-for-trigger? Long, wait-for-trigger (price confirmation).
- Actionable now or after confirmation? After confirmation (fresh price + zone re-entry).
- What would invalidate it? 1h close beyond 0.4037 (stated invalidation level) or BTC breaking down against the regime thesis.
- Chase-risk setup? Low, given the tight gap — but do not market-buy if price has since extended further away.
- Catalyst confirmation or contradiction? Confirmation — externally corroborated, no contradicting signal found.

### 7.2 BANK/USDT (Lorenzo Protocol) — best avoid / squeeze-risk-both-ways

- Has price already reacted? Yes, dramatically — internal data shows 24h move deteriorating from -55.9% (23:30 EEST review) to -60.6% to -63.1% (tonight's scalp/intraday snapshots). This is a genuine, ongoing capitulation by the internal data, following a documented mid-July parabolic rally to an ATH of ~$0.27 (externally confirmed, but only the rally phase — not tonight's crash).
- Is the setup chasing? A fresh short here would be chasing an already-extreme move into negative funding (-0.0035 mexc, -0.0144 bybit external) with rising OI — classic short-squeeze setup risk (internal system already caps BANK to C-tier for exactly this reason: "high_upper_wick_short_squeeze_risk").
- Retest/pullback structure? Not established; still in free-fall per internal data.
- Overextended? Yes, extremely, on the downside.
- Would entry now be late? For a short, yes and dangerous (squeeze risk). For a long/dip-buy, no external catalyst supports a reversal thesis yet.
- What level makes it actionable? Neither direction is actionable until (a) the crash driver is externally confirmed/explained and (b) funding/OI stop still-accelerating negative.
- Aligned with market mood? No clean alignment — this is an idiosyncratic single-name collapse, not a market-wide move.
- Long, short, or wait-for-trigger? Wait-for-trigger / avoid.
- Actionable now? No.
- What would invalidate the avoid call? External confirmation the collapse is a one-off wallet/liquidity event (not a structural break) plus funding normalizing, would make a controlled long-side dip-buy discussable; a confirmed hack/exploit/rug would harden the avoid into a permanent blacklist candidate.
- Chase-risk? Extreme, both directions.
- Catalyst confirmation/contradiction? Neither — internal-only data this cycle, external search did not surface a matching same-day story.

### 7.3 GIGGLE/USDT — catalyst-contradiction, C-tier watchlist (score 65.7, scalp B triggered/intraday B waiting elsewhere in the active-signals table)

- Internal pipeline: "no fresh verified catalyst detected," score 65.7-71.5 depending on mode, watchlist-only, `crypto_intraday_catalyst_or_momentum` playbook explicitly notes "no-catalyst intraday in chop is net-negative (14d WR 23%/PF 0.70/-3R)."
- External: CZ was publicly responding (as of Jul 30-31) to criticism that Giggle Academy donated tokens are being routinely sold/converted to BNB near month-end — a live, negative-optics social-media controversy, not captured by the internal catalyst pipeline (which only tracks canonical/RSS sources, not this kind of X/Telegram-driven drama).
- This is a genuine `catalyst_contradicted` case for the Agent Council: the internal "no catalyst" read is technically true (no canonical event) but incomplete — there is live social risk the system cannot see.
- Actionable now? No — remains C-tier/watchlist by internal score regardless; the external context adds a reason to be *more* cautious about a long, not less.
- What would invalidate/confirm? If the token-selling controversy escalates into a broader confidence crisis, treat as a fresh risk flag; if it fades without price impact, no change needed.

### 7.4 NVDA — carried stocks short-watch, contradiction between internal score and external thesis

- Internal (tonight's stocks-intraday scan): score dropped to 46.13, `no_directional_setup` — no longer even a raw A-tier candidate (it was A-tier ~89.78 in the prior review, purely gated to C by the market-closed rule).
- External: Michael Burry's NVDA/semiconductor short thesis is well-documented and current — verified across CryptoBriefing, Benzinga, GuruFocus, Motley Fool, and 24/7 Wall St., describing an actively growing short position (NVDA add at $210.28, moved SOXX puts further out and higher-strike). This is a real, ongoing bearish narrative, not a one-off headline.
- Stocks are closed — this is planning-only context. The internal/external contradiction (system says no setup, external narrative says bearish) should be specifically re-checked at the 16:20 EEST pre-US-open review once fresh pre-market data exists.
- Legal/headline risk: none beyond the standard "prominent investor is short" narrative risk; not a legal flag.

### 7.5 MSTR — earnings-driven caution, correctly demoted internally

- Internal: B-tier long (score 65) demoted to C via `stale_post_earnings_setup` — the system correctly detected a verified earnings print (2026-07-30T23:18:19 UTC) invalidating pre-earnings levels, while the earnings calendar itself still reads UNKNOWN (a separate, lower-priority data gap, not re-flagged as a new TODO since it's the same root cause as previously known calendar gaps).
- External: confirmed an $8.22B GAAP net loss (vs a $10.02B profit the year prior — driven by mark-to-market on the BTC treasury) and a Q2 revenue miss ($122.4M vs $124.5M consensus). The exact after-hours price reaction was not found via WebSearch this cycle (TODO-12 partially still open, MSTR leg only).
- Actionable now? No — correctly gated by the system; needs fresh levels once market data resumes.

## 8. Best Candidates Ranked

1. **ONDO/USDT** — long-watch, trigger: live re-entry into 0.4078-0.4112 (verify fresh price first).
2. **GIGGLE/USDT** — catalyst-watch (with caution), trigger: pullback into 29.522-29.957 AND resolution of the CZ-controversy overhang.
3. **BANK/USDT** — avoid (both directions), trigger to revisit: external confirmation of crash driver + funding stabilization.
4. **NVDA** — stocks short-watch (planning only), trigger: internal score reconverging bearish at/after the pre-open review, informed by the externally-verified Burry short thesis.
5. **MSTR** — stocks watch (planning only), trigger: fresh post-earnings levels once the system regenerates them; do not use pre-earnings levels.

## 9. Avoid / No Trade

This applies to the current decision window only — scanning, tracking, and monitors all continue regardless.

- **BANK/USDT**: squeeze-risk-both-ways, internally-sourced crash unconfirmed externally, extreme negative funding.
- **No-catalyst crypto intraday chases** (GIGGLE, PUMP, ROBO, MMT, ESP, FIL — all currently C-tier watchlist-only): internal playbook explicitly flags this cohort as net-negative in chop (14d WR 23%/PF 0.70/-3R).
- **PLTR / META stocks shorts**: legal-flag demotions (sec_doj / indictment) still active and unresolved (TODO-1/TODO-2) — treat as manual-review-required, not a clean short, until the flags are audited.
- **Crypto scalp mode generally**: correctly kill-switched; trailing stats (PF 0.25, 0W/4L) confirm the switch is warranted, not evidence of a live problem.

## 10. Main Risks

- **Geopolitical**: Russia's largest aerial attack of the war overnight is a real, externally-confirmed escalation — BTC/broader risk assets could gap on any further escalation into the European session. Macro risk score 99-100/100 reflects this correctly.
- **Data-quality**: `track-signals (post)` crashed this cycle (TODO-NEW-1) — signal-outcome tracking is one cycle behind; the Paper Monitor status numbers quoted in this review are a carried snapshot, not live.
- **BANK/USDT squeeze**: extreme funding + rising OI into an already-collapsed price is a classic setup for a violent short squeeze; equally, shorting into it or catching the falling knife are both live risks.
- **Catalyst mapping still weak** (51.6% unmapped): improving but not resolved — treat the catalyst layer as directional context, not a final signal source, especially for symbols not explicitly named in this review.
- **NVDA internal/external score contradiction**: acting on either the internal "no setup" read or the external Burry-bearish narrative alone, without reconciling them at the next stocks-open review, risks a wrong-footed pre-open decision.

## 11. Action Plan — next 4 hours

1. Re-pull a live ONDO/USDT price before the 11:30 EEST review; if it has re-entered 0.4078-0.4112 with volume, this becomes the desk's cleanest actionable long candidate for that cycle.
2. Watch for any external news explaining BANK/USDT's collapse; do not initiate a new position in either direction until either a cause is confirmed or funding/OI stabilize.
3. Watch for GIGGLE/USDT controversy developments (token-selling criticism) — if it escalates, treat as a fresh risk flag on the whole GIGGLE cohort, not just noise.
4. No action needed on NVDA/MSTR until the US pre-open reviews (16:20 EEST) — market is closed.
5. Confirm at the 11:30 EEST review whether `track-signals (post)` succeeded in the next cycle (resolves or reconfirms TODO-NEW-1) and whether the Paper Monitor status counts have refreshed.

## 12. Final Verdict per Mode

- **Crypto scalp**: kill-switched, no action, stats confirm the switch is correct.
- **Crypto intraday**: watch-only; no fresh A/B, several C-tier no-catalyst names correctly filtered; watch ONDO's sibling swing leg for the cleanest re-entry.
- **Crypto swing**: watch ONDO/USDT specifically for zone re-entry on fresh data; all other active swing legs (ADA, AERO, ACH, ESP) are carried, no new information this cycle.
- **Stocks intraday/swing/invest**: closed, planning-only; carry NVDA (contradiction to resolve) and MSTR (needs fresh post-earnings levels) into the pre-open review.
- **Overall**: caution / watch_only, never a stop — scanning and tracking continue.

## 13. Sources

- [Bitcoin and ethereum prices today, Thursday, July 30, 2026: Prices rise after Fed leaves rates unchanged](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-thursday-july-30-2026-prices-rise-after-fed-leaves-rates-unchanged-132340233.html) — Yahoo Finance, 2026-07-30
- [Crypto Price Prediction Today (July 31): Will Bitcoin, Ethereum and XRP Hold Key Support Levels?](https://sundayguardianlive.com/business/crypto-price-prediction-today-july-31-will-bitcoin-ethereum-and-xrp-hold-key-support-levels-check-btc-eth-xrp-forecast-key-resistance-zones-market-outlook-and-major-catalysts-249862/) — Sunday Guardian Live, 2026-07-31
- [Russia launches largest aerial attacks of the war as crypto markets watch geopolitical risk signals](https://cryptobriefing.com/russia-largest-aerial-attacks-ukraine-crypto-risk/) — CryptoBriefing, 2026-07-31
- [Binance's CZ Responds to Giggle Academy Meme Coin Criticism](https://www.cryptotimes.io/2026/07/31/binances-cz-responds-to-giggle-academy-meme-coin-criticism/) — CryptoTimes, 2026-07-31
- [Lorenzo Protocol's BANK Token Rockets 517% After a Mysterious Wallet Move](https://startupfortune.com/lorenzo-protocols-bank-token-rockets-517-after-a-mysterious-wallet-move/) — Startup Fortune, 2026-07-23 (rally phase only, does not cover tonight's collapse)
- [RWA tokenization news: Ondo drops blockchain plans for private, high-speed trading network](https://www.coindesk.com/business/2026/07/28/ondo-drops-tokenized-asset-blockchain-plans-for-private-high-speed-trading-network) — CoinDesk, 2026-07-28
- [Stock Market Today, July 30: Amazon Soars Over 8% After Hours on Earnings Beat](https://www.fool.com/coverage/stock-market-today/2026/07/30/stock-market-today-july-30-amazon-soars-over-8-after-hours-on-earnings-beat/) — The Motley Fool, 2026-07-30
- [Amazon shares jump after hours on strong earnings and a revenue beat](https://investinglive.com/stocks/amazon-shares-jump-after-hours-on-strong-earnings-and-a-revenue-beat/) — InvestingLive, 2026-07-30
- [Dear MicroStrategy Stock Fans, Mark Your Calendars for July 30](https://www.barchart.com/story/news/3505908/dear-microstrategy-stock-fans-mark-your-calendars-for-july-30) — Barchart, 2026-07-29
- [Michael Burry increases short position against Nvidia, expanding bearish bets across semiconductor sector](https://cryptobriefing.com/michael-burry-short-nvidia-semiconductor/) — CryptoBriefing, 2026-07-30
- ['Big Short' Investor Michael Burry Reveals Tesla, Nvidia Shorts, Says Chip Boom Is 'Beginning of the End'](https://www.benzinga.com/markets/tech/26/07/60207524/big-short-investor-michael-burry-reveals-tesla-nvidia-shorts-says-chip-boom-is-beginning-of-the-end) — Benzinga, 2026-07-01

## 14. Fix Requests / TODO

### TODO-NEW-1 (new, high priority): `track-signals (post)` crashed — `AttributeError: 'NoneType' object has no attribute 'get'`
- **issue:** This cycle's post-cycle signal-tracking pass crashed and did not complete. Root cause: `level_hold_plan` is `None` when `track_signal()` calls `level_hold_plan.get("applied")`.
- **evidence:** `data/scheduled_runs/2026-07-30_default_schedule/cycle_04_00-54_summary.md`, step 67: `[FAIL] track-signals (post) (exit=1, 5.9s, attempts=1)`. Traceback: `src/cli.py:3245` → `src/signals/tracker.py:1462` (`track_signal(**track_kwargs)`) → `src/signals/tracker.py:1081` (`if level_hold_plan.get("applied"):`) → `AttributeError: 'NoneType' object has no attribute 'get'`.
- **suggested manual fix:** Trace what upstream function is expected to populate `level_hold_plan` before line 1081 and guard against `None` (e.g. `if level_hold_plan and level_hold_plan.get("applied"):`) or fix the caller that's supposed to construct it. Since this step didn't complete, verify no signal outcomes were silently missed for this cycle's window once fixed.
- **priority:** high
- **first observed:** 2026-07-31 04:30 EEST (this cycle).

### TODO-NEW-2 (new, medium priority, recurring pattern): three unrelated steps hit 300s timeouts in the same cycle
- **issue:** `intelligence layer update`, `latency acceptance report (per asset, read-only)`, and `refresh obsidian dashboard` all timed out at exactly 300.0-300.1s in cycle 4 (00:54-02:01 EEST). This echoes the prior review's TODO-13 (DB lock contention hypothesis), but TODO-13's original step (`paper stock direction`) succeeded fine this cycle — the timeout symptom has moved to different steps, suggesting a possible shared-resource contention window rather than one broken step.
- **evidence:** `data/scheduled_runs/2026-07-30_default_schedule/cycle_04_00-54_summary.md`, steps 39, 54, 70 — all `[FAIL] ... (exit=-1, ~300s, attempts=1)`, `timed out after 300 seconds`.
- **suggested manual fix:** Investigate whether these three steps (and TODO-13's original step) run in overlapping time windows and contend for the same SQLite writer lock or external API rate limit; consider staggering them further apart in the cycle schedule or raising the timeout with backoff.
- **priority:** medium
- **first observed:** 2026-07-31 04:30 EEST (this cycle); related to TODO-13 (2026-07-30 23:30 EEST, not recurred itself).

### TODO-1 (carried forward): PLTR `legal_headline_risk: sec_doj` flag still looks like a false positive
- **issue:** Still open. PLTR demoted A→C tonight citing "active legal/headline risk (sec_doj)" again (`data/reports/stocks/intraday/2026-07-31_01-39_stocks_intraday_report.md` §7).
- **evidence:** Prior WebSearch verification (multiple reviews through 2026-07-30) found only ~9-month-old shareholder-solicitation boilerplate; not re-verified externally this cycle.
- **suggested manual fix:** Audit the `legal_headline_risk`/`sec_doj` classifier's source data for PLTR; down-weight generic shareholder-solicitation press-release boilerplate.
- **priority:** high
- **first observed:** 2026-07-30 11:45 EEST; still open 2026-07-31 04:30 EEST.

### TODO-2 (carried forward): META `legal_headline_risk` mislabeled as "indictment"
- **issue:** Still open. META demoted A→C tonight citing "active legal/headline risk (indictment)" again. Prior review confirmed the actual exposure is civil litigation (child-safety verdicts/trial), not a criminal indictment.
- **evidence:** Prior WebSearch verification (2026-07-30 11:45 EEST review); not re-verified externally this cycle.
- **suggested manual fix:** Correct the legal-risk taxonomy/label for META from "indictment" to "civil_litigation" or similar.
- **priority:** medium
- **first observed:** 2026-07-30 11:45 EEST; still open 2026-07-31 04:30 EEST.

### TODO-3 (carried forward): Recurring `UNKNOWN_INCONSISTENT` lifecycle mapping — unmapped status `'tp2_hit'`
- **issue:** AAPL, GOOGL, XOM (stocks/intraday/B) pattern, persistent across many consecutive review cycles now. Re-confirmed fresh this cycle (not just carried from stale prior text): `reports/PAPER_MONITOR_STATUS_LATEST.md` (01:55 EEST, ~2h50m old at review time) still shows `UNKNOWN_INCONSISTENT | 5`.
- **evidence:** `reports/PAPER_MONITOR_STATUS_LATEST.md`, line "UNKNOWN_INCONSISTENT | 5".
- **suggested manual fix:** Fix the lifecycle-state mapping for legacy-touch signals with raw status `tp2_hit` in the stocks/intraday/B path so it resolves to a proper CLOSED_WIN/OPEN state.
- **priority:** high
- **first observed:** 2026-07-29; reappeared every reviewed cycle since, count unchanged at 5.

### TODO-5 (carried forward, improving): Catalyst mapping still weak (51.6% unmapped, improved from 68.3%)
- **issue:** 258 of 500 catalyst events today have no resolved symbol — above the 50% weak-mapping threshold, but a real improvement from 68.3% at the last review (23:30 EEST).
- **evidence:** live count of `data/catalysts/2026-07-31/catalyst_events.jsonl` this run: 242 mapped / 258 unmapped.
- **suggested manual fix:** Continue widening/improving the symbol resolver in the catalyst layer per [[project_crypto_ai_desk_catalyst_linkage]].
- **priority:** low (known, deferred, improving)
- **first observed:** recurring; re-confirmed 2026-07-31 04:30 EEST.

### TODO-9 (carried forward, not re-verified): `binance_ecosystem_teaser` narrative basket remains present, previously flagged as possibly mislabeled
- **issue:** The basket (primary BNB/USDT, related ASTER/USDT) is present again in tonight's `narrative_baskets.jsonl`; original concern (2026-07-30 18:38 EEST review) was that it conflates an unrelated small-cap treasury-shell governance story with a genuine Binance-protocol event. Not re-verified externally this cycle.
- **evidence:** `data/catalysts/2026-07-31/catalyst_cycle_01-21.md`, "binance_ecosystem_teaser" basket entry.
- **suggested manual fix:** Correct or suppress the `binance_ecosystem_teaser` basket label until the narrative-basket classifier can distinguish a genuine Binance-protocol event from an unrelated story sharing the "Binance" keyword.
- **priority:** medium
- **first observed:** 2026-07-30 18:38 EEST; still open 2026-07-31 04:30 EEST.

### TODO-12 (carried forward, partially resolved): MSTR after-hours price reaction still not confirmed
- **issue:** AMZN's after-hours reaction is now confirmed (+~10% on the beat). MSTR's exact after-hours % price move is still not found via WebSearch this cycle, though the underlying earnings facts ($8.22B loss, revenue miss) are confirmed.
- **evidence:** WebSearch this cycle found Motley Fool/InvestingLive AMZN coverage but no MSTR after-hours price-reaction article; Barchart's MSTR piece predates the earnings release.
- **suggested manual fix:** No code fix needed — re-query specifically for "Strategy MSTR stock after hours July 30 2026 earnings reaction" at the next review; search-index freshness for MSTR specifically appears to lag AMZN's.
- **priority:** low (self-resolving with time)
- **first observed:** 2026-07-30 23:30 EEST; MSTR leg still open 2026-07-31 04:30 EEST.
