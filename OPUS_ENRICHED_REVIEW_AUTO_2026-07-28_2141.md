# Opus Enriched Review — late-session risk review — Auto Cycle 21:41 EEST

## 1. Executive Summary
Advisory only / no auto-trade. **Slot: late-session risk review** (US cash session in its final ~1.5h, 21:41 EEST / ~14:41 ET). Crypto and stocks both remain **risk-off**; **zero fresh A/B-tier actionable setups on either desk this cycle** — crypto scalp is kill-switched, crypto intraday/swing produced no B, and every stocks-intraday raw-A/B was gate-demoted to C. The one genuinely live, **OPEN actionable** position on either desk is a pre-existing **B-tier ZEC/USDT short** (waiting_for_entry, entry 469.6–472.6, created 17:35 UTC today, expires tomorrow 17:36 UTC) backed by a real, fresh, internally-verified catalyst: Zcash rushed its Ironwood upgrade live after an Orchard-pool security flaw / counterfeiting scare (Decrypt, CryptoBriefing, both within the last 2h) — this is the best catalyst-backed candidate this cycle. **XLE short-vs-strongest-sector** and **PLTR short-vs-bullish-technical** contradictions (first raised 16:07 and 18:39) remain unresolved into this third-consecutive review, now 5+ hours open. Crypto short candidates (EUL/LA/ESP/SOXLB/KAITO) are almost universally squeeze-capped this cycle — a systemic pattern worth a look, not a reason to force a trade. COTI/USDT remains the best crypto long-watch, still unchased-pullback, now a fourth consecutive review with the same unresolved read.

## 2. Data Used
- `data/reports/scalp/2026-07-28_18-31_scalp_report.md` (crypto scalp, kill-switched, data freshness 18:30 UTC)
- `data/reports/intraday/2026-07-28_18-40_intraday_report.md` (crypto intraday, data freshness 18:30 UTC)
- `data/reports/swing/2026-07-28_01-25_swing_report.md` (crypto swing, **stale >14h**, not used for verdict)
- `data/reports/stocks/intraday/2026-07-28_18-36_stocks_intraday_report.md` (data freshness 18:35 UTC)
- stocks swing/invest reports last dated 2026-07-02 — deprecated framework, not evaluated
- `data/catalysts/2026-07-28/catalyst_events.jsonl` (3000 events today) + `narrative_baskets.jsonl` (3 baskets)
- `active-signals --asset-class crypto` (19 rows) / `--asset-class stocks` (50 rows)
- `signal-stats --asset-class crypto` / `--asset-class stocks`
- `scripts.detect_untracked_legacy_alerts --since 2026-07-28` → clean, no untracked alerts
- Internal `db/crypto_ai_desk.sqlite` `proposed_signals` (ZEC/USDT history) and `news_items` (ZEC/USDT, last 24h) queries
- No external WebSearch/WebFetch needed this cycle — internal ZEC catalyst records were fresh (<2h), consistent across two independent sources, and directionally unambiguous; see §14 discipline note
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-28_1839.md` (18:39 EEST, US open reaction slot)

## 3. Scheduler / Data Freshness
- Scheduler folder: `data/scheduled_runs/2026-07-28_default_schedule/` — `scheduler.log` mtime 21:32 EEST (7 min old, fresh) → **no defer**.
- Latest `cycle_01_18-12_summary.md` mtime 19:00 EEST (~2.7h old) — older bucket file, but scheduler.log freshness alone clears the defer gate per protocol; the three mode reports (scalp/intraday/stocks-intraday) are all independently fresh (data freshness 18:30–18:36 UTC = effectively this run).
- Crypto swing: 01:25 EEST, ~20h16m old → **stale (>14h)**, excluded from verdict, carried only as background context (still consistent: bearish/risk-off unchanged).
- Stocks swing/invest: 2026-07-02 → deprecated framework, not read for this review.
- Catalyst layer: `data/catalysts/2026-07-28/` present, 3000 unique events / 3 narrative baskets today.
- Untracked-alert detector: **clean** — every legacy crypto alert has a backing proposed_signal.
- Monitor/keeper process health was not independently re-verified this cycle beyond the allowed read-only CLI/file list; scheduler.log recency is used as the freshness proxy per protocol.

## 3A. Agent Council JSON
```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-07-28 21:41 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["monitor process health"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log 7min old", "swing report 20h16m old (stale, excluded)", "scalp/intraday/stocks-intraday all data-freshness 18:30-18:36 UTC (effectively current)"] },
    { "agent": "market_regime", "verdict": "risk_off", "confidence": 0.85,
      "reason_codes": ["risk_off", "shorts_preferred", "chop"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC downtrend, ETH uptrend, altcoin breadth 27.27% above EMA20, macro risk 96.9-97.2/100 (Strait of Hormuz talks, Russia-sanctions Senate vote)", "stocks: risk_off bias short, VIX 18.38, breadth_ema20 25%, only DIA in range/up, semis/tech weakest sectors, energy/financials/healthcare strongest"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["fresh_catalyst", "catalyst_confirmed", "mapping_weak"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZEC/USDT: fresh (<2h), internally cross-confirmed (Decrypt + CryptoBriefing) bearish catalyst (Ironwood upgrade rushed after security flaw) aligned with the open short signal", "catalyst mapping 1052/3000 = 35.1% mapped, 64.9% unmapped — weak-mapping threshold crossed, same persistent pattern as prior reviews", "momentum_breakout basket (COTI/VANRY) explicitly tagged avoid_chase"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "data_unavailable"], "data_missing": ["OI 24h% for most C-tier movers (n/a on MEXC fallback)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["9 of ~13 rejected crypto C-tier shorts this cycle explicitly capped for thin_liquidity_short_squeeze_risk or extreme_negative_funding_against_short (EUL, LA, SOXLB, KORUB, KAITO, ESP, SKHYB, MUB, SHIB, BANK, SNXXB)", "COTI/VANRY negative funding across bybit+mexc, crowding elevated"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chase_risk", "overextended", "entry_fresh"], "data_missing": ["live ZEC/USDT OHLCV — symbol not in this cycle's top-40 deep-analysis universe, so current distance-to-entry cannot be confirmed from report fields"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZEC/USDT entry zone 469.62-472.62, invalidation 476.29, created 4h ago, still waiting_for_entry — fresh setup, not yet triggered", "COTI +53-58% 24h across cycles, no pullback yet — chase risk unchanged", "SNXXB/MUB/BANK rejected: >2 ATR from EMA20, do not chase"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.6,
      "reason_codes": ["waiting_for_entry", "entered_unresolved", "no_entry"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 1 OPEN actionable / WAITING for entry (ZEC/USDT short), 18 ENTERED UNRESOLVED (tp1_hit/tp2_hit riding toward next target/stop, some 6-11 days old on scalp/intraday-mode signals whose expected horizon is hours — worth a lifecycle-closure check, see TODO)", "stocks: 0 A/B open; 50 C-tier rows mostly review/shadow, several tp1/tp2-hit ENTERED UNRESOLVED aged 3+ weeks (invest-mode, deprecated framework)", "0 new A/B triggered this cycle on either desk"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["headline_risk", "manual_review", "correlation_cluster"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PLTR short contradicted by bullish 20/50-day MA reclaim technical headlines (recurring, unresolved since 18:39)", "XLE short contradicts XLE being the single strongest sector (RS +7.66%), unresolved since 16:07", "LRCX/META/MSFT/AAPL/AMZN/COIN/MSTR earnings tomorrow, UNH/V earnings today — do_not_chase_warning active", "ETH/NVDA/SOL exploit_hack operator-review warnings still active"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto B-tier 7d reliable: WR25.7% PF2.18 total+34.1R (swing mode PF3.43 strongest, scalp mode PF0.17/0-6 W-L, actively net-negative)", "stocks C-tier 7d reliable: WR4.7% PF0.43 total-4.0R (watchlist quality, expected, not actionable)", "stocks-intraday A/B guard: 14d n5 +1.0R, 30d n11 -2.5R — small sample, fee-fragile per §9 of the stocks report"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents; ZEC/USDT is the one genuinely open, catalyst-confirmed candidate — treat as the priority watch item into the close; XLE/PLTR contradictions still unresolved after 3 review cycles; crypto shorts broadly squeeze-capped this cycle"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "catalyst_backed",
    "best_long_candidate":     { "symbol": "COTI/USDT", "trigger": "confirmed pullback/retest with rising volume into 0.0113-0.0119; do not chase a fresh high without volume confirmation", "reason": "strongest RS-vs-BTC symbol in flow across all three timeframes for a fourth consecutive review, but momentum-only, no verified catalyst, crowded on negative funding, narrative basket explicitly tags it avoid_chase" },
    "best_short_candidate":    { "symbol": "SMH / XLK (stocks, semis, watch)", "trigger": "wait for a failed relief-bounce/retest with volume into the close rather than chasing the already-extended intraday move; short only on rejection", "reason": "semiconductors remain the weakest sector (RS vs SPY -16.22% 20d) and the chip-selloff narrative from earlier today has not reversed, but no fresh trigger this cycle and entry is still late" },
    "best_catalyst_candidate": { "symbol": "ZEC/USDT", "trigger": "already OPEN / WAITING for entry — short entry zone 469.62-472.62, invalidation above 476.29, expires 2026-07-29T17:36 UTC; internally-confirmed bearish catalyst (Ironwood upgrade rushed live after an Orchard-pool security flaw / counterfeiting scare, Decrypt + CryptoBriefing, both <2h old)", "reason": "the only candidate on either desk this cycle with both an open B-tier signal AND a fresh, cross-confirmed, directionally-aligned catalyst" },
    "avoid_candidate":         { "symbol": "PLTR short / XLE short", "reason": "PLTR: bearish score contradicted by bullish 20/50-day-MA-reclaim technical headlines, unresolved since 18:39. XLE: short candidate directly contradicts XLE being the single strongest sector this cycle (RS +7.66%), unresolved since 16:07 — third consecutive review with the same open contradiction." },
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
| market_regime | risk_off | 0.85 | risk_off, shorts_preferred, chop | advisory_only |
| catalyst_narrative | caution | 0.55 | fresh_catalyst, catalyst_confirmed, mapping_weak | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | chase_risk, overextended, entry_fresh | advisory_only |
| execution_lifecycle | needs_review | 0.60 | waiting_for_entry, entered_unresolved, no_entry | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, manual_review, correlation_cluster | advisory_only |
| playbook_performance | caution | 0.60 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (18:39 EEST, US open reaction)
- **ZEC/USDT is a new finding this cycle** — a B-tier intraday short (score 65.2) went to `waiting_for_entry` at 17:35 UTC (before the 18:39 review's data-freshness cutoff, but not mentioned in that review — it was not in the deep-analysis top-40 that cycle). It remains open into this review, backed by a fresh, internally cross-confirmed bearish catalyst.
- **XLE short-vs-sector-strength contradiction: still open, now 5h20m since first flagged (16:07).** Same symbol, same conflict (XLE short, score 84.51 this cycle vs. 88.2 at 18:39, energy remains the strongest sector RS +7.66%).
- **PLTR short-vs-bullish-headline contradiction: still open.** Score moved 93.54 (18:39) → 82.42 (this cycle); the specific bullish angle shifted from earnings-beat-preview to "just overtook/reclaimed the 20/50-day moving average" — still a bullish technical read contradicting a short score.
- **AMD's gate reasoning normalized**: at 18:39 AMD showed a `sector_confirmation_conflict` label that looked internally inconsistent with the report's own weak-semis read (flagged as TODO); this cycle AMD (score 81.21, down from 87.06) shows only `liquidity_rvol_below_min` + `catalyst_none_and_not_exceptional_technical` — the sector-conflict label itself did not recur, though the "catalyst_none" framing is arguably still mislabeled given the report's own AMD headline ("AMD, Intel and Micron extend losses as chip stocks get clobbered") is a bearish, direction-aligned catalyst, not an absence of one.
- **Catalyst mapping: 35.1% mapped (1052/3000), essentially unchanged from 18:39's 35.1% (1052/3000)** — same weak-mapping read persists, not improving, not worsening this cycle.
- **Crypto active signals: 19 rows (was 18 at 18:39)** — the new row is the ZEC/USDT waiting_for_entry signal; the other 18 remain the same tp1_hit/tp2_hit entered-unresolved positions, unchanged.
- **Crypto scalp mode performance now visible in signal-stats as a distinct negative bucket**: PF 0.17, 0 wins / 6 losses, avgR -0.25 — flagged as a new TODO this cycle.

## 5. Catalyst Coverage
- Total catalyst events (raw, today): **3000**. Mapped (non-null symbol): **1052 (35.1%)**. Unmapped: **1948 (64.9%)**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (unmapped 64.9% > 50% threshold; unchanged from the 18:39 review's identical 35.1%/64.9% split — the persistence itself, not just the level, is notable).
  - Top unmapped: a $250.2M USDC Treasury mint alert (not ticker-mappable); Bitget/Bybit CEX-announcement spam (AEONUSDT futures listing, stock-perp listings, City Edition promo — not tradable catalysts); POSCO International on-chain trade-receivables pilot (South Korea, no mapped symbol).
- `narrative_baskets` today: **3** — `perps_dex_narrative` (playbook `wait_pullback`, primary HYPE/USDT, fresh <1h), `rwa_narrative` (playbook `related_beta_rotation`, primary ONDO/USDT + XLM/USDT, fresh <6h), `momentum_breakout` (playbook `wait_pullback`, primary VANRY/USDT, fresh <1h — COTI/USDT is the same basket's other primary member per the 18:39 review and is explicitly `avoid_chase`-tagged there).

## 6. Market Landscape

Crypto: BTC downtrend, ETH uptrend (mixed regime, net classified bearish trend/risk-off), altcoin breadth above EMA20 only 27.27%, macro/geopolitics risk 96.9-97.2/100 — Senate Russia-sanctions vote, Iran/Oman Strait of Hormuz shipping-control negotiations, crude oil below $80. Stocks: risk_off, bias short, VIX 18.38, only DIA of 4 major indices in an uptrend/range-positive state (QQQ -4.59% 5d / -6.58% 20d is the weakest index), breadth above EMA20 only 25% (though breadth above EMA50 is a healthier 75%, a notable divergence — near-term weakness inside a still-intact medium-term uptrend). Energy/financials/healthcare are the strongest sectors; semiconductors (-16.22% RS vs SPY 20d) and technology (-7.70%) are the weakest — the chip-selloff theme flagged in the 18:39 review has not reversed by the late session, but has also not produced a fresh actionable trigger this cycle (all semis/tech shorts remain gate-demoted to C on liquidity/sector-confirmation/catalyst grounds).

### Market Mood / Risk Routing
- Crypto mood: **risk-off**
- Stocks mood: **risk-off** (late session, ~1.5h from the 16:00 ET close)
- Dominant narrative: **Zcash Ironwood upgrade rushed live after a security flaw** (fresh, catalyst-backed, directionally short-aligned); secondary: semis/tech weakness unresolved since the open, energy/financials/healthcare holding relative strength
- Preferred side now: **catalyst-backed** (ZEC short is open and confirmed); secondarily shorts on stocks semis (watch only, no fresh trigger) and crypto momentum longs only on a genuine COTI pullback
- Best long candidate: none clean and fresh — see COTI long-watch in §8
- Best short candidate: none clean and fresh on either desk — crypto shorts broadly squeeze-capped; stocks semis short (SMH/XLK) needs a retest, not a chase
- Best catalyst-backed candidate: **ZEC/USDT** (open, waiting_for_entry, internally cross-confirmed bearish catalyst)
- What to avoid: PLTR short (bullish-technical conflict, unresolved), XLE short (sector-strength contradiction, unresolved), chasing any crypto C-tier short that is squeeze-capped, chasing SMH/XLK/AMD after the earlier move
- What would change the view: ZEC/USDT price entering 469.62-472.62 with the setup still valid (would promote from watch to live-entry-window); a genuine COTI pullback with rising volume; semis stabilizing/reclaiming VWAP into the close

## 7. Candidate Deep Dives

### 7.1 ZEC/USDT (crypto, B-tier intraday short, score 65.2, status **WAITING for entry**) — TOP PRIORITY WATCH
- Has price already reacted to the catalyst? Partially — the internal headline itself states "ZEC Falls 5%" concurrent with the upgrade going live; the signal's entry zone (469.62-472.62) sits below the current invalidation level (476.29), consistent with a breakdown/retest setup, but this cycle's report does not carry ZEC in its top-40 deep-analysis universe, so live current price / distance-to-entry cannot be independently confirmed from report fields this run (data gap, noted in §3A technical_entry).
- Is the setup chasing? No evidence of that — it is a pre-existing waiting_for_entry order, not a fresh chase.
- Retest/pullback structure? The setup is explicitly a "breakdown/retest" playbook per the signal thesis; momentum score 66.0/100, tag `weak_vs_market`.
- Overextended >2 ATR from EMA20? Not stated; no OHLCV available this cycle to check.
- Aligned with market mood? Yes — crypto mood is risk-off/short-biased, and this is one of the very few crypto shorts this cycle NOT flagged for squeeze risk.
- Actionable now or after confirmation? It is already an open, valid B-tier signal; treat as watch-into-fill, not a new idea to originate.
- What would invalidate: 1h close above 476.29 (per invalidation field), or the setup simply timing out at its 2026-07-29T17:36 UTC expiry without filling.
- Chase-risk: low (this is a limit-style wait, not a market chase).
- Catalyst confirmation/contradiction: **confirmed**, internally, by two independent sources within the last 2h (Decrypt: "Zcash Activates Ironwood Upgrade After Counterfeiting Scare"; CryptoBriefing: "Zcash activates Ironwood upgrade after Orchard security flaw") — both bearish-leaning (a rushed security fix, not a celebratory feature launch), directionally consistent with the short.
- Verdict: **WATCH — the one open, catalyst-confirmed candidate on either desk this cycle.** Monitor for fill; no action needed beyond watching, per the ALWAYS-SCAN rule the system continues tracking this automatically.

### 7.2 XLE (stocks, short, score 84.51 raw-A → C by gate: `sector_confirmation_weak_or_unknown`, `liquidity_rvol_below_min`, `catalyst_none_and_not_exceptional_technical`) — MANUAL REVIEW, unresolved 3 cycles running
- §2 of the current stocks report explicitly lists energy (XLE) as the **strongest** sector this cycle (RS vs SPY 20d +7.66%), while §5's candidate table scores XLE as a **short** at 84.51 — the same raw contradiction flagged at 16:07 and 18:39, now open 5h20m.
- Aligned with market mood? No — directly contradicts the sector's own relative-strength read.
- Actionable now or after confirmation? Neither — do not trade until a human reconciles the score-direction/sector-strength mismatch.
- Verdict: **MANUAL REVIEW REQUIRED**, unchanged conclusion, third consecutive review.

### 7.3 PLTR (stocks, short, score 82.42 raw-A → C by gate: `sector_confirmation_weak_or_unknown`, `liquidity_rvol_below_min`, `catalyst_none_and_not_exceptional_technical`) — MANUAL REVIEW, unresolved
- Current report's own §4 news for PLTR: "Palantir Technologies Inc. (PLTR) Just Overtook the 20-Day Moving Average" and "...Just Reclaimed the 50-Day Moving Average" (both today) — bullish technical reads that sit awkwardly against a short candidate scored as the second-highest raw score this cycle.
- This is the same category of issue as the 18:39 review's PLTR finding (there it was earnings-beat-preview headlines; today it is moving-average-reclaim headlines) — the underlying pattern of "catalyst_none" gate language masking a directionally-opposed news backdrop recurs.
- Verdict: **AVOID / MANUAL REVIEW REQUIRED**, recurring pattern, see TODO (carried).

### 7.4 COTI/USDT (crypto, C-tier watchlist, score 91.6 intraday / 92 scalp, +53-58% 24h across today's reports) — WATCH ONLY, fourth consecutive review
- Strongest RS-vs-BTC symbol in flow across scalp/intraday reports for a fourth consecutive cycle today (04:45, 16:07, 18:39, now); momentum-only, no fresh verified catalyst, negative funding across bybit+mexc, `momentum_breakout` narrative basket explicitly tags it `avoid_chase`.
- Is this chasing? Yes, at current levels after a sustained multi-day spike — needs a genuine pullback/retest with rising volume into 0.0113-0.0119, not a fresh high.
- Verdict: **WATCH ONLY**, unchanged.

### 7.5 SMH / XLK / AMD (stocks, semis, short-watch, all gate-demoted to C this cycle) — WATCH, retest required
- Semiconductors remain the weakest sector this cycle (RS vs SPY 20d -16.22%), consistent with the chip-selloff theme confirmed extending at the 18:39 open-reaction review.
- No fresh trigger this cycle; AMD's gate reasoning normalized to `liquidity_rvol_below_min` + `catalyst_none...` (the earlier `sector_confirmation_conflict` label did not recur, see §4), though the "catalyst_none" framing remains arguably mislabeled given the report's own bearish AMD/Intel/Micron headline this cycle.
- Actionable now or after confirmation? After confirmation only — wait for a relief-bounce/retest into the final ~1.5h of the session; do not chase the already-extended move from earlier today.
- Verdict: **WATCH-ONLY / retest required**, unchanged directional thesis from 18:39, no new entry this cycle.

## 8. Best Candidates Ranked
1. **Best catalyst-backed (crypto): ZEC/USDT short** — already open/waiting_for_entry, entry 469.62-472.62, invalidation 476.29, expires 2026-07-29T17:36 UTC. Internally cross-confirmed bearish catalyst (Ironwood upgrade rushed after security flaw). This is the priority watch item into the close.
2. **Best short-watch (stocks): SMH / XLK / AMD** — semis remain the weakest sector; trigger is a relief-bounce/retest with volume into the final 1.5h, not a chase of the earlier move.
3. **Best long-watch (crypto): COTI/USDT** — trigger: confirmed pullback/retest into 0.0113-0.0119 with rising volume; invalidated by a fresh high without volume confirmation or funding staying negative/crowded.
4. **Manual-review (stocks): XLE short** — unresolved sector-strength contradiction, third consecutive review.
5. **Manual-review (stocks): PLTR short** — unresolved bullish-technical contradiction, recurring pattern (different bullish angle each cycle).

## 9. Avoid / No Trade
This decision window only — never a command to stop the system; scanning/tracking continues in all cases.
- **XLE short** — contradicts the sector's own RS-strength read, unresolved since 16:07 (third consecutive review).
- **PLTR short** — contradicts today's own bullish moving-average-reclaim headlines, unresolved since 18:39.
- Chasing any of EUL/LA/SOXLB/KORUB/KAITO/ESP/SKHYB/MUB/SHIB/BANK/SNXXB short — all explicitly squeeze-capped or extreme-negative-funding-against-short this cycle; the desk's own gates already routed these to C for good reason.
- Chasing COTI/VANRY at current extension — crowded, negative funding, no-catalyst momentum tagged `avoid_chase` by the system's own narrative basket.
- Chasing AMD/SMH/NVDA/XLK at current extended levels — the move already happened earlier today; wait for a retest.
- AAPL, AMZN, COIN, LRCX, MA, META, MSFT, MSTR — earnings tomorrow (2026-07-29); UNH, V — earnings today. Do-not-chase warning active on all.

## 10. Main Risks
- Two live, unresolved contradiction TODOs (XLE sector-strength, PLTR bullish-headline) have now persisted across three review cycles today without self-resolving — worth a human look even though nothing is actionable regardless.
- Catalyst mapping remains weak (35.1% mapped) and flat, not improving across at least three cycles today.
- ZEC/USDT's live price/ATR context could not be independently confirmed this cycle (symbol outside this run's top-40 deep-analysis universe) — treat the signal's own entry/invalidation fields as authoritative until a fresher report includes it.
- Late-session, thin-liquidity window into the 16:00 ET close — squeeze-risk warnings across most crypto C-tier shorts suggest genuinely thin books in several small-cap alts right now, not just an overly strict gate.
- FOMC/Fed rate decision commentary and Strait-of-Hormuz shipping talks remain live macro risks into tomorrow's session (also LRCX/META/MSFT/AAPL/AMZN/COIN/MSTR earnings tomorrow) — size down into the overnight/pre-open gap risk.

## 11. Action Plan — next 4 hours
- Watch ZEC/USDT for a fill into 469.62-472.62; no action needed beyond monitoring — the system tracks this automatically.
- Watch SMH/XLK/AMD for a relief-bounce/retest with volume into the close before considering any fresh short; do not chase the already-extended move.
- Watch COTI/USDT for a genuine pullback/retest; do not chase the existing spike.
- Do not touch PLTR or XLE on the short side without a human resolving the respective contradictions first.
- No crypto scalp/swing A/B exists to act on; continue monitoring, no action required.
- Heading into the close and overnight: expect thin liquidity in the small-cap crypto alts currently squeeze-capped — no fresh shorts there without a clean retest.

## 12. Final Verdict per Mode
- **Crypto scalp:** kill-switched (mode off) — no action; signal-stats shows this mode net-negative this week (PF 0.17, 0W/6L) even setting the kill-switch aside, see TODO.
- **Crypto intraday:** no fresh A/B this cycle; one pre-existing B-tier signal (ZEC/USDT short) remains OPEN/WAITING for entry — priority watch item.
- **Crypto swing:** stale (>14h), excluded from actionable verdict, background-consistent with risk-off read.
- **Stocks intraday:** late session, 0 actionable A/B; 10 raw-A/B demoted to C by SI-1..5 gates this cycle (XLE/PLTR/AMD/SMH/QQQ/SMCI/JPM/META/XLV/XLK among them), 2 with unresolved directional/catalyst contradictions worth a human look (XLE, PLTR).
- **Stocks swing/invest:** deprecated framework, not evaluated this cycle.
- **Overall desk stance:** WATCH / CAUTION. No new positions recommended this cycle beyond monitoring the one open ZEC/USDT signal and the two watch-only triggers (SMH/XLK/AMD retest short-watch, COTI pullback long-watch).

## 13. Sources
- Internal: `db/crypto_ai_desk.sqlite` `news_items` — "Zcash Activates Ironwood Upgrade After Counterfeiting Scare" (Decrypt, 2026-07-28 18:24 UTC) and "Zcash activates Ironwood upgrade after Orchard security flaw" (CryptoBriefing, 2026-07-28 18:05 UTC)
- Internal: `db/crypto_ai_desk.sqlite` `proposed_signals` — ZEC/USDT signal history (sig_1f5c6f251618d32f, created 2026-07-28T17:35:23 UTC)
- Internal: `data/reports/stocks/intraday/2026-07-28_18-36_stocks_intraday_report.md` §2 (sector rotation), §4 (PLTR, AMD news), §5/§7 (candidate scores + gate reasons)
- Internal: `data/reports/intraday/2026-07-28_18-40_intraday_report.md` and `data/reports/scalp/2026-07-28_18-31_scalp_report.md` (crypto regime, C-tier watchlist, rejected/squeeze-capped shorts)
- Internal: `data/catalysts/2026-07-28/catalyst_events.jsonl`, `narrative_baskets.jsonl`
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-28_1839.md`
- No external web sources this cycle — internal records were sufficient (fresh, cross-confirmed, unambiguous); see §14 discipline checklist.

## 14. Fix Requests / TODO

### TODO-xle-pltr-contradictions-persist-3-cycles
- **issue:** The XLE short-vs-strongest-sector contradiction (first flagged 16:07) and the PLTR short-vs-bullish-headline contradiction (first flagged 18:39) are both still open at 21:41 — third and second consecutive review respectively with no resolution. Neither symbol's gate framing ("sector_confirmation_weak_or_unknown", "catalyst_none_and_not_exceptional_technical") captures the actual issue (a directionally-opposed confirmed catalyst/sector-strength read, not an absence of information).
- **evidence:** `data/reports/stocks/intraday/2026-07-28_18-36_stocks_intraday_report.md` §2 (energy=strongest sector, RS+7.66%) vs §5 (XLE short, score 84.51); §4 (PLTR bullish MA-reclaim headlines) vs §5 (PLTR short, score 82.42, gate reason `catalyst_none_and_not_exceptional_technical`).
- **suggested manual fix:** as previously suggested (16:07, 18:39): audit whether the catalyst-linkage/sector-confirmation gates for stocks-intraday distinguish "no catalyst" from "catalyst/sector-strength present but contradicts trade direction" — these need different operator language and different gate codes, since the current framing has now produced the same false signal on two different symbols across three review cycles in one day.
- **priority:** high (escalated from medium — third-cycle persistence with no self-resolution)
- **first observed:** 2026-07-28 16:07 EEST (XLE); 2026-07-28 18:39 EEST (PLTR); this persistence observation 2026-07-28 21:41 EEST

### TODO-crypto-scalp-mode-net-negative
- **issue:** `signal-stats --asset-class crypto` mode breakdown shows scalp mode at PF 0.17, avgR -0.25, 0 wins / 6 losses over the week window — a reproducibly losing bucket, separate from and in addition to the existing kill-switch (mode is already disabled for entry, but the historical/backtest-style signals continue to be scored and tracked at this negative rate).
- **evidence:** `python -m src.cli signal-stats --asset-class crypto` → By-mode table: `mode=scalp | n=28 | trig=23 | wins=0 | losses=6 | PF=0.1667 | avgR=-0.25 | totalR=-5.0`.
- **suggested manual fix:** review whether crypto scalp scoring/entry logic should be tightened before any future re-enable, given the consistent net-negative signal quality even independent of the current kill-switch; alternatively confirm the kill-switch is expected to stay permanent and scalp scoring/tracking could be reduced to save compute.
- **priority:** medium
- **first observed:** 2026-07-28 21:41 EEST

### TODO-scalp-intraday-entered-unresolved-aging
- **issue:** Several crypto scalp/intraday-mode B-tier signals are sitting in `tp1_hit`/`tp2_hit` (ENTERED UNRESOLVED) status 6-11 days past their own mode's typical hours-scale horizon (e.g. NEAR/USDT scalp, expires_at 2026-07-17, 11 days ago; ONDO/OPN/FIL scalp, expires_at 2026-07-22, 6 days ago) without resolving to a final closed state in the `active-signals` view.
- **evidence:** `python -m src.cli active-signals --asset-class crypto` → 11+ of 19 rows are scalp/intraday-mode signals with `expires_at` dates 6-11 days in the past, still shown status=tp1_hit/tp2_hit rather than a terminal closed state.
- **suggested manual fix:** confirm whether this is expected behavior (a partial-TP position intentionally rides open-ended toward final stop/TP with no forced time-based closure) or whether a lifecycle-closure job should be finalizing/archiving these once their mode-appropriate horizon has clearly passed; if expected, consider a distinct display state (e.g. "AGED UNRESOLVED") so the operator can tell a 4-hour-old vs 11-day-old unresolved position apart at a glance.
- **priority:** low
- **first observed:** 2026-07-28 21:41 EEST

### Source-discipline checklist
- Every external claim above has source + title + date + URL, or is explicitly marked internal-only with a file/table path. ✓
- No uncited stats, no uncited legal claims. ✓
- No fabricated TradingView/chart observations — TradingView/manual chart check unavailable this run; only local OHLCV/ATR/EMA/score fields used, and ZEC's missing live-price context was explicitly flagged as a data gap rather than guessed. ✓
- No `test_source`/fixture URLs ingested. ✓
- §13 Sources section present. ✓
- External web research was **not needed** this cycle: internal `news_items` records for ZEC/USDT were fresh (<2h), cross-confirmed by two independent sources, and directionally unambiguous, satisfying the internal-first bar without requiring WebSearch/WebFetch. No new external sources → no ingest step run this cycle (nothing to ingest).
