# Opus Enriched Review — Late-Session Risk Review — Auto Cycle 21:39 EEST

## 1. Executive Summary

**Slot: late-session risk review (21:30 EEST / ~14:39 ET, deep into the US cash session) — advisory only / no auto-trade.** Focus: exposure on the 3 open actionable positions, whether the aging TSLA short is still worth trusting, crypto evening continuation vs reversal, and what stays active overnight.

**Scheduler healthy, data fresh.** `2026-07-13_default_schedule` cycle_03 started 19:42 EEST, last summary 20:08 EEST (~1h31m old, well under the 3h defer threshold). Crypto scalp (19:49 EEST) and intraday (19:54 EEST) are fresh; crypto swing (17:38 EEST, ~4h01m old) is just past the 4h fresh cutoff — treated as **carry-forward**, not stale, still usable. Stocks intraday (21:38 EEST, data 18:38 UTC) is essentially real-time. Stocks swing/invest remain the known-deprecated ~11-day-stale legacy mode, excluded.

**No fresh A/B fired in any of the four current-cycle reports — crypto or stocks.** Scalp/intraday/swing all independently returned "No A-tier / No B-tier setups found." Stocks intraday found 9 raw B-tier candidates and demoted every one to C (0 actionable) — mostly on `liquidity_rvol_below_min` + `catalyst_none_and_not_exceptional_technical`, which is expected behavior deep in a chop session with no fresh catalysts. This is a genuine no-new-signal cycle, not a data gap.

**US session closed down, broad and macro-driven, not a fake move.** Verified via WebSearch: Dow -0.2%, S&P 500 -0.7%, Nasdaq -1.4% on renewed Iran/Strait-of-Hormuz escalation (Trump reinstated a shipping blockade) — oil spiked, semiconductors led the damage (SK Hynix -6%, Micron -5%, SanDisk -12%, Seagate -6%), which lines up exactly with the desk's own weakest-sector read (semiconductors RS -5.46% vs SPY) and the stocks regime label of **chop** (VIX 17.18, breadth 50%/100%). This is a broad, catalyst-confirmed risk-off tape, not noise — treat late-session stock longs with extra caution and don't fight the tape into the close.

**Three open actionable positions to manage into the close/overnight, no new entries recommended.** **AMZN long (A-tier, stocks/intraday)** — entered ~17:23 EEST on AI-chip-bet optimism; regime turned to chop after entry, monitor for late-session fade risk rather than adding. **XOM long (B-tier, stocks/intraday)** — open, energy is the strongest S&P sector today on oil spike (tailwind). **KITE/USDT long (B-tier, crypto/swing)** — open, monitoring TP/SL, crypto tape is chop-to-bearish. **TSLA short (B-tier, stocks/intraday)** is still `waiting_for_entry` after ~4h16m (registered 14:23 UTC / 17:23 EEST) — this is now a stale, unfilled setup; re-verify the entry zone (393.35-396.06) live before trusting it, do not chase if price has moved away.

**Crypto direction stats flag a real risk-manager concern**: despite the desk running short-biased/risk-off all session, the **short** cohort (n=18, weekly) is running PF 0.33 / avgR -0.12 — losing — while **long** (n=181) is PF 1.10 and net positive. The regime call to prefer shorts hasn't been paying off recently; treat new crypto shorts with extra scrutiny (clean breakdown + volume, not just "regime says short").

**Catalyst mapping is weak this run**: 83.8% of today's 3,954 logged catalyst events are unmapped to a symbol (640 mapped). Use the catalyst layer as context only, not as a standalone trade trigger (§5, §14 — this is a known, persistent issue, not new).

**Overall verdict: CAUTION, routed by side — not a blanket no-trade.** Crypto: chop/bearish, no fresh A/B; best long-watch is JTO/USDT (RS-leader, strong swing-mode playbook edge, needs a catalyst or clean pullback-hold); best short-watch is DEXE/USDT but it is explicitly squeeze-flagged (still +48.5% on the week, heavily short-skewed) — wait for a confirmed breakdown, don't chase. Stocks: chop regime, gates correctly blocking new entries into the close; manage the 3 open positions, let TSLA's stale waiting order expire rather than force it. Scanning, tracking, and the paper book continue uninterrupted.

## 2. Data Used

- Crypto scalp report: **fresh** — `2026-07-13_16-49_scalp_report.md` (generated 19:49 EEST; data 16:45 UTC). No A/B; regime bearish/risk-off; scalp mode kill-switch disabled (known, ongoing).
- Crypto intraday report: **fresh** — `2026-07-13_16-54_intraday_report.md` (generated 19:54 EEST; data 16:45 UTC). No A/B; best C-tier watch EVAA/USDT (score 60.0, no catalyst, known-bad no-catalyst-intraday cohort WR 23%/PF 0.70).
- Crypto swing report: **carry-forward (4h01m old)** — `2026-07-13_14-38_swing_report.md` (generated 17:38 EEST; data 14:30 UTC). No A/B; best C-tier watch JTO/USDT (score 63.3, RS-leader, strong-mode playbook).
- Stocks intraday: **fresh, near-real-time** — `2026-07-13_18-38_stocks_intraday_report.md` (generated 21:38 EEST; data 18:38 UTC, ~1min old). Regime **chop** (VIX 17.18, breadth 50%/100%). 9 raw B-tier candidates, all demoted to C by SI-1..5 gates; 0 actionable A/B.
- Stocks swing/invest: still 2026-07-02, ~11 days stale, known-deprecated legacy mode, not evaluated.
- Catalysts: `data/catalysts/2026-07-13/catalyst_events.jsonl` (3,954 events logged today) + `narrative_baskets.jsonl` (5 active baskets: `perps_dex_narrative`/HYPE, `rwa_narrative`/ONDO+XLM, `ai_narrative`/NEAR+RENDER+TAO+FET, `binance_ecosystem_teaser`/BNB, `delisting_thin_liquidity`/none). Mapped/unmapped computed directly from the JSONL (§5).
- CLI: `active-signals --asset-class crypto` (26 rows, all B-tier, mostly tp1/tp2-hit or triggered — no fresh waiting-for-entry), `active-signals --asset-class stocks` (50 rows; AMZN A / TSLA B / XOM B currently live, rest historical), `signal-stats` crypto (week: n=199, PF 1.06, winrate 13.9%, totalR +3.5; short direction PF 0.33 — flagged in §1/§6), `signal-stats` stocks (week: A/B n=10, PF 1.39, totalR +1.57; C-tier n=197, PF 0.84), `detect_untracked_legacy_alerts --since 2026-07-13` (**0 found**).
- Paper Monitor Status (`reports/PAPER_MONITOR_STATUS_LATEST.md`): lifecycle counts in §3.
- Direct SQLite reads (read-only): `proposed_signals` (AMZN/TSLA signal metadata), `news_items` (AMZN/TSLA last-24h headline check — no legal/headline contradiction found for either).
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-13_1844.md` (18:44 EEST, ~2h55m ago) — primary comparison baseline for §4.
- External: 2 WebSearch queries (US market close + Iran/Hormuz; BTC/ETH price today) + 1 WebFetch (Yahoo Finance BTC quote, verified ~$64.0k) — sources in §13.

## 3. Scheduler / Data Freshness

- `scheduler.log` (`2026-07-13_default_schedule`): `cycle_03` started 19:42 EEST, last activity/summary 20:08 EEST — **fresh, not deferred** (~1h31m old at review time, well under the 3h defer threshold).
- Crypto scalp/intraday: **fresh** (generated 19:49-19:54 EEST).
- Crypto swing: **carry-forward** (generated 17:38 EEST, ~4h01m old — just past the 4h fresh cutoff, used as context per §D, not excluded).
- Stocks intraday: **fresh, near-real-time** (generated 21:38 EEST, data 18:38 UTC, ~1min old).
- Stocks swing/invest: **stale** (2026-07-02, ~11 days) — known-deprecated legacy mode, excluded from final verdict.
- Untracked legacy crypto alerts: **0** (confirmed this cycle).
- Paper Monitor Status: **Open actionable 3 (AMZN long stocks/intraday/A, XOM long stocks/intraday/B, KITE/USDT long crypto/swing/B) · Waiting for entry 1 (TSLA short stocks/intraday/B, ~4h16m stale) · Review/Shadow 114 · Entered unresolved (expired-after-entry) 6 · No-entry/stale/moved-away 45 · Closed 393W / 29L / 0flat · Needs review 0**.
- No legal/headline gate regressions found: UNH's DOJ block and JPM's earnings do-not-chase block are both still correctly active (display/advisory, non-gating). Checked `news_items` directly for AMZN and TSLA (last 24h) — no legal/headline contradiction for either; AMZN's AI-chip-bet coverage supports the long thesis, TSLA news is generic (Rivian comparison, retail-flow chatter, no fresh legal event beyond the standing SEC-Twitter-settlement item already priced in).
- Known non-blocking noise (unchanged, self-documented in every report): Reddit social-attention sources unavailable; Bybit/OKX futures partial coverage; token-unlock/liquidation-heatmap/order-book/on-chain blindspots not automated.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-07-13 21:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["stocks swing/invest (~11 days stale, known deprecated mode)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["cycle_03 started 19:42 EEST, last summary 20:08 EEST", "crypto scalp/intraday fresh (19:49-19:54 EEST); crypto swing carry-forward (17:38 EEST, 4h01m); stocks intraday near-real-time (21:38 EEST)", "0 untracked legacy crypto alerts"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["risk_off", "chop", "shorts_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC transition_down, ETH range, altcoin breadth 27.5% above EMA20, recommended style short-bias-or-no-trade", "stocks: chop regime, VIX 17.18, breadth 50%/100%, SPY -0.7% / QQQ -1.4% / DIA -0.2% on close (WebSearch verified)", "energy sector strongest on oil spike (XOM tailwind); semiconductors weakest (SMH RS -5.46%)"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["83.8% of 3954 catalyst events today unmapped to a symbol", "5 active narrative baskets: ai_narrative (NEAR/RENDER/TAO/FET), rwa_narrative, perps_dex_narrative (HYPE), binance_ecosystem_teaser", "AMZN AI-chip-bet coverage supports open long; no fresh catalyst for JTO/DEXE/EVAA watchlist ideas"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.4,
      "reason_codes": ["squeeze_risk", "data_unavailable"],
      "data_missing": ["Bybit/OKX full OI/liquidation coverage (partial only)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["DEXE/USDT: price down + OI up, fresh shorts pressing, global long/short heavily short-skewed = squeeze risk explicitly flagged by the desk's own counter-thesis", "JTO/USDT: price up + OI up, fresh positioning confirms trend, crowding normal", "KITE/USDT (open swing long): price up + OI up at time of entry, funding neutral"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["stale_before_entry", "chase_risk", "entry_late"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TSLA short waiting_for_entry since 17:23 EEST, ~4h16m unfilled — price has not come to the zone (393.35-396.06), re-verify live before trusting", "EVAA/USDT down -42.6% 24h — already reacted, late to chase a fresh short here without a fresh catalyst", "DEXE/USDT +48.5% 7d, -10.2% 24h — extended on the week, short setup risks squeezing on any BTC/ETH bounce"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Open actionable: 3 (AMZN A long, XOM B long, KITE/USDT B long)", "Waiting for entry: 1 (TSLA B short, stale ~4h16m)", "Review/Shadow: 114 · Entered unresolved: 6 · No-entry/stale: 45 · Closed: 393W/29L/0flat"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["reduce_risk", "repeated_losses", "legal_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto short direction cohort PF 0.33 / avgR -0.12 over 18 signals this week — regime-driven short bias not currently paying off", "UNH long correctly hard-blocked on active DOJ Medicare-fraud criminal probe", "JPM earnings tomorrow (2026-07-14) — do-not-chase block active", "geopolitical (Iran/Hormuz) risk is live and could gap either book overnight"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing mode PF 1.48 / +10.1R (14d) — strongest mode, JTO/DEXE both scored via this playbook", "crypto scalp mode PF 0.32 / -6.8R — kill-switched, consistent with prior audits", "crypto intraday mode PF 1.01 — roughly breakeven", "no-catalyst intraday cohort (EVAA/NEAR playbook) WR 23% / PF 0.70 / -3R over 14d — known-bad, both current intraday watchlist ideas sit in this cohort", "stocks A/B n=10 this week, PF 1.39 — small sample, directional only"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "JTO/USDT", "trigger": "hold/defend pullback zone 0.6459-0.6540 on volume, or fresh catalyst confirming the RS-leader move", "reason": "RS leader (+7.9% 24h, +10.4% vs BTC), swing-mode playbook has 72% WR / PF 5.80 (14d), OI confirming — but bearish overall regime and no catalyst yet, score (63.3) below active threshold" },
    "best_short_candidate":    { "symbol": "DEXE/USDT", "trigger": "confirmed 1h close below 42.70 support with volume AND funding/long-short skew normalizing (currently heavily short-skewed = squeeze risk)", "reason": "down -10.2% 24h but still +48.5% on the week (extended), OI rising into the drop (fresh shorts pressing) — desk's own counter-thesis flags squeeze risk; crypto short cohort is PF 0.33 this week, demand a clean confirmed breakdown, not a chase" },
    "best_catalyst_candidate": { "symbol": "NEAR/USDT", "trigger": "hold pullback zone 1.931-1.945 with volume; catalyst is a MEXC network-upgrade announcement (thin, low-confidence) plus AI-narrative tailwind", "reason": "only crypto watchlist idea with an actual mapped catalyst + RS-leadership (+5.4% vs BTC); confidence still low, score 58.4 below threshold" },
    "avoid_candidate":         { "symbol": "UNH", "reason": "active DOJ criminal investigation into Medicare billing fraud — confirmed legal/headline risk, hard block, not a routine gate demotion" },
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
| market_regime | caution | 0.70 | risk_off, chop, shorts_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.40 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | stale_before_entry, chase_risk, entry_late | advisory_only |
| execution_lifecycle | ok | 0.80 | open_actionable, waiting_for_entry, review_shadow | advisory_only |
| risk_manager | caution | 0.60 | reduce_risk, repeated_losses, legal_risk | advisory_only |
| playbook_performance | caution | 0.55 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-07-13_1844.md` (18:44 EEST US-open-reaction review):

- **New**: TSLA short's `waiting_for_entry` status persists and is now materially staler (~4h16m vs ~implied-fresher at 18:44) — was not yet flagged as stale at 18:44, now is.
- **New**: HYPE/USDT short — which was the prior review's lead crypto watch item (`waiting_for_entry` since 14:44 EEST, flagged stale at 18:44) — no longer appears in the current active-signals crypto list at all; it has aged out to `NO_ENTRY_EXPIRED` per the Paper Monitor Status (confirmed: "signal aged out waiting for entry (stale)"). Confirmed outcome, not a live idea anymore.
- **New watchlist leads**: JTO/USDT (crypto swing, RS-leader) and NEAR/USDT (crypto intraday, catalyst-backed) have emerged as the cleanest watch candidates this cycle, replacing the 16:28/18:44 reviews' EVAA/HYPE focus (EVAA remains on watch but is a weaker, no-catalyst idea).
- **Confirmed**: Regime stayed `chop` (stocks) / `bearish trend, risk-off` (crypto) across both reviews — no regime flip.
- **Confirmed**: UNH DOJ block, JPM earnings block, and the standing operator-review flags (BTC/ETH/HOOD/JPM/ORCL/TSLA/XRP) are unchanged and still correctly active.
- **Confirmed**: Catalyst mapping weakness persists — 83.8% unmapped now vs 84.2% at 18:44 — flat, still well above the 50% threshold.
- **Escalated**: Geopolitical risk (Iran/Hormuz) got worse through the day and is now confirmed to have driven the actual US close (Dow -0.2%/S&P -0.7%/Nasdaq -1.4%, semis hit hardest) — this was "watch" language at 18:44, now a confirmed closing-print driver.
- **Thesis unchanged**: AMZN long thesis (AI-chip-bet catalyst) still holds; no contradicting news found.

## 5. Catalyst Coverage

- Total catalyst events logged today (`catalyst_events.jsonl`, cumulative across all cycles): **3,954**.
- Mapped to a symbol: **640** (16.2%). Unmapped: **3,314 (83.8%)**.
- Narrative baskets active: **5** (`ai_narrative`, `rwa_narrative`, `perps_dex_narrative`, `binance_ecosystem_teaser`, `delisting_thin_liquidity`).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Top unmapped headlines (all MEXC futures trading-parameter/leverage-adjustment notices — low-value noise, not missed trading catalysts):
  - "Maximum Leverage Adjusted for BLASTUSDT Futures" (t.me/MEXC_OfficialAnnouncements)
  - "Adjustment to BLASTUSDT Funding Rate Settlement Frequency" (t.me/MEXC_OfficialAnnouncements)
  - "Adjustment to PARTIUSDT Funding Rate Settlement Frequency" (t.me/MEXC_OfficialAnnouncements)
- Note: this matches the persistent, previously-documented catalyst-mapping gap (symbol resolver misses non-canonical tickers / exchange-maintenance notices dominate the unmapped bucket) — not a new regression. See §14.

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **bearish trend / risk-off**, chop-leaning (BTC transition_down, ETH range, altcoin breadth 27.5% above EMA20).
- Stocks mood: **chop** (VIX 17.18, breadth 50% above EMA20 / 100% above EMA50), closed broadly lower and macro-confirmed (Dow -0.2%, S&P -0.7%, Nasdaq -1.4%) on Iran/Hormuz escalation. Semiconductors and other high-beta tech led losses; energy was the standout strong sector (oil spike).
- Dominant narrative: geopolitical risk-off (Iran/Hormuz blockade reinstated) bleeding into both books; secondarily AI-chip narrative (Amazon, Nvidia, Broadcom coverage) still running in the background.
- Preferred side now: **wait-for-trigger** — the desk's own short-direction cohort is underperforming (PF 0.33) despite the risk-off regime, so don't lean into shorts mechanically; longs need RS-leadership + confirmation, not just "regime says short."
- Best long candidate: **JTO/USDT** — none active; trigger: hold/defend 0.6459-0.6540 pullback zone on volume or a fresh catalyst.
- Best short candidate: **DEXE/USDT** — none active; trigger: confirmed 1h close below 42.70 with volume AND long/short skew normalizing (currently squeeze-prone).
- Best catalyst-backed candidate: **NEAR/USDT** — thin catalyst (MEXC network-upgrade note) + AI-narrative tailwind + RS leadership; trigger: hold 1.931-1.945 with volume.
- What to avoid: UNH (confirmed DOJ legal risk — hard avoid); chasing TSLA's stale short entry; chasing EVAA's already-reacted -42.6% move without a fresh catalyst; new crypto shorts without a clean, confirmed breakdown given the weak short-cohort stats.
- What would change the view: a confirmed Hormuz de-escalation headline (risk-on unlock for both books), a BTC/ETH reclaim of local resistance (would flip crypto to more constructive), or a fresh mapped catalyst on any of the three crypto watchlist names.

## 7. Candidate Deep Dives

### 1. AMZN long (A-tier, stocks/intraday) — OPEN ACTIONABLE, manage into close
- Entered ~17:23 EEST (14:23 UTC) on an AI-chip-bet momentum/catalyst thesis (score 84.5). Entry zone 245.41-246.44, invalidation 244.38.
- Has price already reacted to the catalyst? Partially — the AI-chip coverage (Motley Fool: "Amazon's AI Chip Bet Could Be Bigger Than Investors Realize") is same-day, still fresh.
- Is the setup chasing? No — position was entered earlier in the session before the market rolled over into chop/risk-off.
- Overextended? Not verifiable without a live chart tool (TradingView/manual chart check unavailable — using only local OHLCV/report fields).
- Actionable now or confirmation-only? Already live — this is a manage-not-add decision.
- What would invalidate: a 1h close through 244.38, or a contradicting AMZN-specific headline (none found in last-24h `news_items` check).
- Chase risk: N/A (already filled).
- Catalyst confirmation/contradiction: confirmed, no contradiction found.
- Aligned with mood? Partially — thesis is stock-specific/AI-narrative, not tape-following; broader tape (chop, Nasdaq -1.4% close) is a headwind into the close. Monitor for late-session fade risk rather than adding size.

### 2. TSLA short (B-tier, stocks/intraday) — WAITING FOR ENTRY, stale, do not chase
- Registered 17:23 EEST, still `waiting_for_entry` ~4h16m later. Entry zone 393.35-396.06 (short), invalidation 398.77.
- Has price already reacted? Unclear without live quote — the fact it hasn't triggered in 4h+ suggests price has stayed below the zone or gone range-bound, i.e., the short entry is not confirming.
- Is this chase risk? Not chasing (never filled), but it is now a **stale, aging setup** — the standard lifecycle language applies: WAITING FOR ENTRY, not a fresh idea.
- Legal/headline check: no fresh contradiction found in `news_items` last 24h (generic Rivian-comparison and retail-flow coverage only). One production risk-warning tag exists (`TSLA [exploit_hack]: block_requires_operator_review`) sourced from a headline containing the word "Exploit" in an unrelated Rivian/California-subsidy context — this reads as a probable keyword false-positive, not a real exploit/hack event. Flagged as a data-quality TODO (§14), not treated as a real risk here.
- What would make it actionable: price actually trading into 393.35-396.06 with confirmation; what would kill it: window expiry (2026-07-14T14:23:20) without a fill.
- Recommendation: let it expire naturally rather than manually forcing/chasing; re-verify live before trusting if it does fill this late.

### 3. XOM long (B-tier, stocks/intraday) — OPEN ACTIONABLE, tailwind
- Open position, energy sector is today's standout strength (oil spike on Hormuz escalation) — a genuine tailwind, not a contradiction.
- No legal/headline risk found for XOM in recent checks (only older SEC-quarterly-reporting coverage from 2026-07-10, not adverse).
- Aligned with mood: yes — energy long into an oil-spike/geopolitical-risk tape is thesis-supportive.

### 4. JTO/USDT (crypto swing C-tier, score 63.3) — best long-watch, not yet actionable
- RS leader (+7.89% 24h, +10.4% vs BTC), volume 4.43x average, OI rising with price (fresh positioning, not deleveraging).
- Playbook (`crypto_swing_narrative_rs_momentum`) has the desk's strongest historical edge (14d WR 72% / PF 5.80 / +24R).
- Counter-thesis (desk's own): fails if this is just a beta bounce inside a bearish-regime tape and buyers don't defend the pullback zone; no fresh catalyst is verified yet.
- Not actionable: score (63.3) below the active-trade threshold, primarily on regime and risk-penalty drag (-11.7).
- Trigger to promote: defended pullback zone 0.6459-0.6540 on volume, or a fresh mapped catalyst.

### 5. DEXE/USDT (crypto swing C-tier, score 60.0) — best short-watch, squeeze-flagged
- Down -10.2% 24h but still +48.5% on the 7d — an extended move, not a fresh breakdown.
- Derivatives: price down + OI up = fresh shorts pressing; global long/short ratio heavily short-skewed — the desk's own counter-thesis explicitly calls out squeeze risk if BTC/ETH reclaim local levels.
- No fresh catalyst verified.
- Given the crypto short-direction cohort is running PF 0.33 this week, this is a "wait for confirmed breakdown, not a chase" setup, not a clean go-short signal.

## 8. Best Candidates Ranked

_No fresh A/B cleared the desk threshold this cycle in either asset class. Per PART 9, ranking the best watch-only candidates by side:_

1. **Best long-watch: JTO/USDT** — trigger: defend pullback 0.6459-0.6540 on volume, or fresh catalyst.
2. **Best catalyst-watch: NEAR/USDT** — trigger: hold 1.931-1.945 with volume; catalyst is thin (MEXC network-upgrade note), treat as secondary confirmation only.
3. **Best short-watch: DEXE/USDT** — trigger: confirmed 1h close below 42.70 with volume AND long/short skew normalizing (currently squeeze-prone — do not chase the current move).
4. Existing open book (not new candidates, manage only): AMZN long (A), XOM long (B), KITE/USDT long (B).
5. Aging/expiring: TSLA short (B) — let expire, re-verify if it fills late.

## 9. Avoid / No Trade

_This applies to the current decision window only — scanning, tracking, and the paper book continue uninterrupted._

- **UNH long** — hard avoid, confirmed active DOJ criminal investigation into Medicare billing fraud.
- **JPM** — do not chase into tomorrow's (2026-07-14) earnings print, either direction.
- **EVAA/USDT short** — already reacted (-42.6% 24h), no fresh catalyst, sits in the desk's known-bad no-catalyst-intraday cohort (WR 23%/PF 0.70/-3R, 14d). Late to chase.
- **New crypto shorts generally, absent a clean confirmed breakdown** — the short-direction cohort is PF 0.33 this week; the regime call to prefer shorts has not been paying off in execution.
- **TSLA short, as a chase** — do not manually force the stale waiting order; let it expire or re-verify live.

## 10. Main Risks

- **Geopolitical (Iran/Hormuz)**: live, escalating, already drove today's close and could gap either book overnight or into the Asia open — highest-priority risk into the overnight window.
- **JPM earnings tomorrow** (2026-07-14) — bank-sector volatility risk into and after the print; do not add exposure around it.
- **Crypto short-cohort underperformance**: risk of continuing to route into a losing side mechanically because the regime label says "risk-off" — needs disciplined confirmation, not regime-following alone.
- **TSLA stale waiting order**: risk of a late, low-quality fill if price suddenly gaps into the zone without fresh confirmation.
- **Catalyst-mapping gap (83.8% unmapped)**: risk of missing a real catalyst buried in the unmapped bucket, or of over-trusting the catalyst layer where it's actually silent.

## 11. Action Plan — next 4 hours

1. Hold AMZN long and XOM long; no new adds. Monitor AMZN for late-session/into-close fade given the broader chop tape; XOM has a live tailwind (oil spike) — reassess if oil gives back the day's gains.
2. Hold KITE/USDT long swing; monitor TP/SL, no action needed.
3. Let TSLA short's waiting order run its course; do not manually force it. If it fills, immediately re-verify the entry zone against live price before trusting it.
4. Watch JTO/USDT and NEAR/USDT for a defended pullback / volume confirmation overnight into the Asia session — do not enter pre-confirmation.
5. Do not initiate new DEXE/USDT shorts without a confirmed breakdown close below 42.70; squeeze risk is real given the OI/short-skew picture.
6. Track Iran/Hormuz headlines through the Asia session — this is the dominant swing factor for both books overnight.
7. No action on UNH, JPM (earnings), or any other flagged legal/headline names.

## 12. Final Verdict per Mode

- **Crypto scalp**: kill-switch disabled (ongoing), no action.
- **Crypto intraday**: no A/B; watch NEAR/USDT (catalyst-backed) and EVAA/USDT (avoid — already reacted, no catalyst) only; no new entries.
- **Crypto swing**: no A/B; watch JTO/USDT (long) and DEXE/USDT (short, squeeze-flagged) only; manage open KITE/USDT long.
- **Stocks intraday**: no A/B this cycle; manage open AMZN (A) and XOM (B) longs; let TSLA (B) short expire or re-verify if it fills late; hard avoid UNH; do not chase JPM into earnings.
- **Stocks swing/invest**: legacy/deprecated, not evaluated.

## 13. Sources

- [S&P 500 drops after Trump reimposes Strait of Hormuz blockade, SK Hynix leads chip stocks lower: Live updates](https://www.cnbc.com/2026/07/12/stock-market-today-live-updates.html) — CNBC, 2026-07-13
- [Stock market today: Dow, S&P 500, Nasdaq fall as US-Iran tensions escalate, oil jumps](https://finance.yahoo.com/markets/live/stock-market-today-monday-july-13-dow-sp-nasdaq-113249278.html) — Yahoo Finance, 2026-07-13
- [US Stock Futures Fall as Mideast Tensions Flare Anew, Oil Climbs](https://www.bloomberg.com/news/articles/2026-07-13/us-stock-futures-fall-as-mideast-tensions-flare-anew-oil-climbs) — Bloomberg, 2026-07-13
- [Bitcoin and ethereum prices today, Monday, July 13, 2026](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-monday-july-13-2026-strong-price-openings-backtracking-this-morning-133042462.html) — Yahoo Finance, 2026-07-13
- Yahoo Finance BTC-USD quote (WebFetch, live check): ~$63,995.74, +0.32% — date unavailable on page (delayed data notice)

## 14. Fix Requests / TODO

### TODO-catalyst-mapping-weak
- **issue:** 83.8% of today's 3,954 catalyst events are unmapped to a symbol; top unmapped items are MEXC futures leverage/funding-parameter notices, not missed trading catalysts, but the overall mapping rate has been persistently weak across recent review cycles (84.2% at 18:44, 85.0% at 16:28).
- **evidence:** `data/catalysts/2026-07-13/catalyst_events.jsonl` — direct count: 640 mapped / 3314 unmapped.
- **suggested manual fix:** review the symbol resolver's handling of exchange-maintenance/trading-parameter announcements (MEXC/Binance leverage & funding notices dominate the unmapped bucket) — either exclude this event subtype from the mapped/unmapped denominator (it's not a real catalyst-coverage gap) or extend the resolver to tag them as `exchange_operational` so they stop diluting the coverage metric.
- **priority:** low
- **first observed:** 2026-07-13 11:46 EEST (recurring across all reviews today; not new this cycle)

### TODO-tsla-false-positive-exploit-tag
- **issue:** TSLA carries a production risk-warning tag `[exploit_hack]: block_requires_operator_review` sourced from a Yahoo Finance headline ("Rivian Vs. Tesla: Buy Rivian to Exploit California's Protectionist Subsidy That Snubbed Tesla") that has nothing to do with an actual exploit/hack event — reads as a keyword false-positive on the word "Exploit."
- **evidence:** `data/reports/stocks/intraday/2026-07-13_18-38_stocks_intraday_report.md`, "Production risk warnings" section: `TSLA [exploit_hack]: block_requires_operator_review — Rivian Vs. Tesla: Buy Rivian to Exploit California's Protectionist Subsidy That Snubbed Tesla (Yahoo Finance Top Stories)`.
- **suggested manual fix:** tighten the `exploit_hack` event-tagger's keyword/NLP matching to require exploit/hack context (e.g. smart-contract, wallet-drain, credential-theft language) rather than a bare substring match on "exploit."
- **priority:** medium
- **first observed:** 2026-07-13 21:39 EEST

### TODO-crypto-short-cohort-underperforming
- **issue:** Crypto `direction=short` signals are running PF 0.33 / avgR -0.12 over 18 signals this week (vs `direction=long` PF 1.10 over 181), despite the desk running a short-biased/risk-off regime recommendation all session. The regime-driven short bias is not currently translating into a positive edge in execution.
- **evidence:** `python -m src.cli signal-stats --asset-class crypto` — "By direction" table, this run.
- **suggested manual fix:** a human-driven review of recent short-signal entries (symbol selection, entry timing, whether shorts are being taken on already-extended down-moves vs fresh breakdowns) to determine if this is regime-timing noise (small n=18) or a systematic issue with how short setups are being scored/selected.
- **priority:** medium
- **first observed:** 2026-07-13 21:39 EEST
