# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:11 EEST

## 1. Executive Summary

Slot: **pre-US-open decision review** (target 08:55 ET / 15:55 EEST; actual fire ~08:58 ET, Δ+3min — within tolerance; review authoring finished ~09:11 ET, still 19 min before the 09:30 ET cash open). **Advisory only — no auto-trade.** Crypto: no fresh A/B-tier idea cleared this cycle (all C-tier/watchlist); BTC trend improved to transition_up (breadth 65% above EMA20) but the Coldcard self-custody hack has **escalated, not receded** — externally confirmed $100M/1,596 BTC now, with a suspected total up to $130M/2,055 BTC across **15 independent attackers** (was $89-116M/3 waves at the 11:39 review). Stocks: the desk's own regime label is **risk_off/short-bias (VIX 15.67, breadth 0%, nan on index returns)** — but this is stale: fresh external premarket data shows S&P/Dow/Nasdaq futures **up** 0.3-0.9%, VIX **down** to 15.59, driven by strong earnings (CAT +9%, PLTR +14% AH) after Monday's +1.48% close. This is a genuine internal-vs-fresh-market contradiction, not a clean signal either way — treat stocks mood as **unresolved until RTH confirms it**. The pre-US stocks overlay reviewed 7 eligible candidates: 0 SUPPORT, 3 NEUTRAL (WMT, BAC, SPY), 2 CAUTION (SMH, NFLX — both explicitly rejected by today's freshest 11:30 pipeline run for `long_in_risk_off_regime`), 2 INSUFFICIENT_DATA (XLK, XLY — no fresh pipeline coverage today). No candidate was promoted; all remain planning-only pending RTH confirmation. Legal/earnings check clear for all 7 (hard gate already excluded META/PLTR/MSFT/AAPL/GOOGL/AMZN/NVDA/AVGO/COIN/SMCI/TSLA/LLY/UNH for legal risk or earnings blackout). 2 untracked legacy Telegram alerts fired today for TUT/USDT (known signal-reuse bug, prior TODO-3).

## 2. Data Used

- Crypto: `data/reports/scalp/2026-08-04_11-06_scalp_report.md`, `data/reports/intraday/2026-08-04_11-12_intraday_report.md`, `data/reports/swing/2026-08-04_03-22_swing_report.md` (carry-forward, ~9h49m old)
- Stocks: `data/reports/stocks/intraday/2026-08-04_11-30_stocks_intraday_report.md`; stocks swing/invest reports are stale (Jul 2, deprecated frameworks — excluded)
- `data/processed/llm_analysis_packet.md`, `data/processed/llm_stocks_packet.md`
- `data/catalysts/2026-08-04/catalyst_cycle_11-15.md`, `catalyst_events.jsonl` (2500 rows today), `narrative_baskets.jsonl` (6 baskets)
- CLI: `active-signals --asset-class crypto` (24 rows), `active-signals --asset-class stocks` (50 rows), `signal-stats` (both), `detect_untracked_legacy_alerts --since 2026-08-04` (2 untracked: TUT/USDT)
- Pre-US stocks overlay: `python -m src.cli stocks-preus-candidates` → 7 eligible / 26 excluded; `stocks-preus-review-ingest` on 7 constructed verdicts (see §5)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-04_1139.md`
- External: 4 WebSearch queries (S&P premarket futures, BAC catalysts, NFLX news, Coldcard hack update) + 1 WebFetch (Yahoo Finance market-today, verified opens) — see §13

## 3. Scheduler / Data Freshness

- Pre-US schedule check: target 08:55 ET, actual fire 08:58 ET (Δ+3min, within tolerance). No DST mismatch window active (2026 windows are 03-08→03-29 and 10-25→11-01).
- `scheduler.log` mtime: 14:42 EEST (~1h29m old at fire time) — **fresh**, not deferred.
- Latest cycle summary: `cycle_07_13-59_summary.md` — same cycle window as the reports used here.
- Crypto scalp/intraday reports: ~11:06-11:12 UTC generation (~1h50m old at fire time) — **fresh**.
- Crypto swing report: 03:22 UTC / ~9h49m old — **carry-forward** (4-12h band), flagged.
- Stocks intraday report: 11:30 UTC / ~1h28m old — **fresh**, but pre-market (US cash opens 09:30 ET / 16:30 EEST).
- Stocks swing/invest: last generated 2026-07-02 — **stale (>14h)**, excluded from verdict (known deprecated frameworks).
- No monitor/paper-status file was read this cycle (not in the allowed read list).
- **Data-quality flag (recurring):** stocks report §1 still shows `Breadth above EMA20/50: 0.0%` and index 5d/20d returns `+nan%` (same gap flagged in the 11:39 review's TODO — unresolved, still present). This nan/zero breadth is a direct input to the `risk_off` label that the freshest 11:30 pipeline run used to reject SPY/NFLX/SMH longs — see §4 and §14.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-08-04 16:11 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["scheduler_fresh", "report_stale", "derivatives_sparse"],
      "data_missing": ["stocks index 5d/20d returns nan; breadth 0.0%", "RS-vs-SPY/sector nan for XLK/SMH in Sector Rotation table — blocks any preus-overlay SUPPORT verdict", "WMT/BAC not in today's 84-symbol tracked coverage set"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log 14:42 EEST fresh", "swing report 9h49m old", "stocks intraday report shows nan RS values"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mixed", "risk_off", "longs_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["internal stocks label: risk_off/short-bias, VIX 15.67, breadth 0%", "external premarket: S&P futures +0.3%, Dow +0.8%, Nasdaq +0.9%, VIX 15.59 (down 1.7%), driven by CAT/PLTR earnings", "crypto: BTC transition_up, ETH range, altcoin breadth 65% above EMA20 — mildly constructive under a heavy macro overlay"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "catalyst_confirmed", "no_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["60.2% unmapped catalyst events today (1504/2500) — worse than 11:39's 57.2%", "6 narrative baskets: delisting_thin_liquidity(XRP), binance_ecosystem_teaser(BNB), ai_narrative(NEAR/RENDER/TAO/FET), rwa_narrative(ONDO/XLM), momentum_breakout(HOME/COTI/SNXXB)", "Coldcard hack catalyst confirmed + escalating externally ($100-130M, 15 attackers)", "WMT/XLK/SMH/XLY/SPY preus candidates lack a material entity-resolved catalyst"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "data_unavailable"],
      "data_missing": ["OI 24h n/a for HOME/TUT/BTW", "no derivatives coverage for stocks side"],
      "suggested_effect": "advisory_only",
      "facts_used": ["HOME/USDT negative funding across bybit/mexc/okx (-0.0071 to -0.0134), crowding elevated — classic squeeze setup on an already +46% 24h move", "TUT/BTW funding neutral, crowding low/normal"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chase_risk", "overextended", "price_moved_away"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["HOME/USDT +46.0% 24h (score 51.7, watchlist-only), pullback zone 0.0086-0.0090 vs current ~0.0091", "NFLX entry_trigger 73.32 sits at the Aug-3 session high on a stock 46% off its 52wk high — classic chase-into-a-downtrend setup", "SPY/NFLX/SMH longs explicitly rejected by the 11:30 pipeline run for rs_not_exceptional_for_risk_off_long"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["waiting_for_entry", "entered_unresolved", "needs_review", "review_shadow"],
      "data_missing": ["closure/expiry logic for weeks-old 'active' crypto/stocks signals still unverifiable from this view (carried TODO)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 24 active — 2 waiting_for_entry (COTI, HFT intraday), 5 entered-unresolved (triggered, expiry still ahead), 17 needs-review (tp1/tp2_hit with expiry already in the past)", "stocks: 50 active — nearly all needs-review (legacy, expiry in the past); ORCL/NOC are the most recent (expiry ~13:54 UTC today)", "pre-US overlay: 7 signals moved to review/shadow (paper-plan tier, market_closed_intraday_planning_only cap) — 0 promoted", "2 untracked legacy Telegram alerts (TUT/USDT) not backed by a proposed_signal"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["headline_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Coldcard hack now $100-130M / 1,596-2,055 BTC across 15 attackers (escalation vs 11:39's $89-116M/3 waves) — still the dominant crypto risk-off driver even as BTC price recovers toward $64k", "AMD/CAT/SMCI report earnings today — gap/chase risk regardless of direction", "hard gate already excludes META/PLTR/MSFT for legal_risk and 9 names for earnings_blackout from the preus overlay — no new legal/headline hits found on WMT/BAC/NFLX/SPY/XLK/SMH/XLY"] },
    { "agent": "playbook_performance", "verdict": "bad", "confidence": 0.7,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto scalp week: PF 0.167, avgR -0.192, 0W-3L — structurally negative", "crypto weekend cohort: PF 0.50, winrate 11% (n=10) — underperforms", "crypto intraday week: PF 3.34, avgR 0.91 — strongest mode", "stocks C-tier week: PF 0.54, winrate 5% (n=203, reliable) — weak", "stocks shorts week: PF 0.14, 1W-10L (n=91) — weak"] },
    { "agent": "head_trader", "verdict": "watch_only", "confidence": 0.55,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["synthesis of all agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.55,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "HOME/USDT", "trigger": "1h close inside 0.0086-0.0090 pullback zone with volume; invalidation below 0.0082", "reason": "top RS/momentum mover (+46% 24h, RS/BTC +44%) but score 51.7 watchlist-only, negative funding = squeeze-prone not a clean trend-continuation long" },
    "best_short_candidate":    { "symbol": "KAITO/USDT", "trigger": "confirmed failed-bounce structure (crypto_failed_bounce_short playbook, 14d WR40%/PF2.0) plus derivatives confirmation before entry", "reason": "genuine relative weakness (-8.66% 24h, RS/BTC -10.52%) but not yet a confirmed structure — do not short on RS score alone" },
    "best_catalyst_candidate": { "symbol": "BTC/USDT", "trigger": "a formal Coinkite/Galaxy resolution statement, or 24-48h with no new theft wave / new attacker joining", "reason": "externally confirmed, escalating ongoing hack ($100-130M, 15 attackers) — the dominant catalyst risk this window, decoupled from BTC's own price recovery toward $64k" },
    "avoid_candidate":         { "symbol": "NFLX (stocks pre-open long)", "reason": "rejected by today's freshest pipeline run as long_in_risk_off_regime/rs_not_exceptional; stock is 46% off its 52wk high and 21% YTD; entry trigger sits at the Aug-3 session high — textbook chase-into-a-downtrend" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 6
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.60 | scheduler_fresh, report_stale, derivatives_sparse | advisory_only |
| market_regime | caution | 0.50 | mixed, risk_off, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, fresh_catalyst, catalyst_confirmed, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | chase_risk, overextended, price_moved_away | advisory_only |
| execution_lifecycle | caution | 0.55 | waiting_for_entry, entered_unresolved, needs_review, review_shadow | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, reduce_risk | advisory_only |
| playbook_performance | bad | 0.70 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | watch_only | 0.55 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (11:39 EEST — Europe/pre-US context)

- **BTC/Coldcard exploit — escalated, not contained**: externally confirmed total now $100M/1,596 BTC (Galaxy Research), with a suspected ceiling of $130M/2,055 BTC and **15 independent attackers** now exploiting the flaw (vs the 11:39 review's $89-116M/3 attack waves). BTC price itself is decoupled — recovering toward $64k per internal risk-warning feed. Still catalyst-watch, not a trade.
- **Crypto regime improved slightly**: BTC trend upgraded from range/chop to **transition_up**; altcoin breadth 65% above EMA20 (vs 57.5% at 11:39). Still no A/B-tier crypto idea clears the desk threshold.
- **HOME/USDT more extended**: 24h +46.0% (vs +32.4% at 11:39) — chase-risk keeps building, not resolving; still watchlist-only per the desk's own scorer.
- **KAITO/USDT**: -8.66% 24h (vs -9.68% at 11:39) — weakness essentially unchanged, still the cleanest short-watch, still lacking a confirmed failed-bounce structure.
- **New this cycle — pre-US stocks overlay run**: 7 candidates reviewed (WMT, XLK, BAC, SMH, NFLX, XLY, SPY); 0 SUPPORT, 3 NEUTRAL, 2 CAUTION, 2 INSUFFICIENT_DATA — none promoted. This is new analysis specific to this slot, not present in the 11:39 review.
- **Internal-vs-external stocks regime contradiction — new finding**: the 11:30 pipeline run explicitly rejected SPY-long, NFLX-long, SMH-long for `long_in_risk_off_regime`, but fresh external premarket data (this run) shows broad risk-on futures. This tension did not exist as clearly at 11:39 (market was still hours from any premarket read).
- **Catalyst mapping**: 60.2% unmapped today vs 57.2% at 11:39 — trending worse for a third consecutive review.
- **Untracked alerts — new since 11:39**: 2 TUT/USDT untracked legacy alerts fired at 09:00 and 12:47 UTC today (0 were reported at 11:39's read, taken slightly earlier).
- Crypto/stocks open-position composition otherwise largely unchanged (same legacy tp1/tp2_hit backlog flagged in the standing TODO).

## 5. Catalyst Coverage

- Total catalyst_events today: **2500**; mapped (non-null symbol): **996** (39.8%); unmapped: **1504** (60.2%).
- Narrative baskets: **6** (delisting_thin_liquidity/XRP, binance_ecosystem_teaser/BNB, ai_narrative/NEAR+RENDER+TAO+FET, rwa_narrative/ONDO+XLM, momentum_breakout/HOME+COTI+SNXXB, +1 additional vs the 11:39 read).
- **Catalyst mapping weak this run (60.2% unmapped) — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines: "ARC Group Securities Acquisition I Announces Pricing of $105,000,000 Initial Public Offering"; "Voters prefer Democrats over Republicans on economy for first time in a decade, Reuters/Ipsos poll finds"; "Southern Company announces upsize and pricing of $725 million in aggregate principal amount of Series 2026A/B Convertible Senior Notes" — general macro/political/corporate-finance noise, not symbol-specific misses.

### Pre-US Stocks Review Overlay
- candidates reviewed: 7 (SUPPORT 0 / NEUTRAL 3 / CAUTION 2 / BLOCK 0 / INSUFFICIENT_DATA 2)
- session-cap-only C's now eligible for pre-open Paper lane: 0 (no candidate met the SUPPORT bar required for promotion; enforced adjustments below are advisory only, not routing changes)
  - WMT (short): NEUTRAL, adjustment 0, pre-gate tier B, base_score 65.77 — no material bearish catalyst, RS unconfirmed (nan)
  - XLK (long): INSUFFICIENT_DATA, adjustment 0, pre-gate tier C, base_score 57.17 — no fresh directional signal today, RS vs SPY nan
  - BAC (long): NEUTRAL, adjustment 0, pre-gate tier A, base_score 83.23 — real catalyst (JPMorgan PT raise $62.50→$68, sector tailwind) but not <24h fresh, RS unconfirmed
  - SMH (long): CAUTION, adjustment -4 → 50.5, pre-gate tier C, base_score 54.5 — explicitly rejected by today's freshest pipeline run for long_in_risk_off_regime
  - NFLX (long): CAUTION, adjustment -5 → 62.81, pre-gate tier B, base_score 67.81 — rejected by freshest pipeline run, 46% off 52wk high, entry sits at recent session high (chase risk)
  - XLY (long): INSUFFICIENT_DATA, adjustment 0, pre-gate tier B, base_score 69.16 — no fresh pipeline coverage today, RS nan
  - SPY (long): NEUTRAL, adjustment 0, pre-gate tier B, base_score 71.25 — internal regime rejected it as long_in_risk_off, but fresh external premarket data (S&P/Dow/Nasdaq futures up, VIX down) directly contradicts that internal label; genuinely unresolved, not a clean either-way call
- excluded by hard gate: 26 — EARNINGS_BLACKOUT (LLY, TSLA, AVGO, AAPL, UNH, COIN, SMCI, NVDA, GOOGL, AMZN — 10 names); LEGAL_RISK (META, PLTR, MSFT — 3 names); NO_ENTITY_RESOLVED_CATALYST (PANW, GE, ORCL, LMT, ADBE, NOW, CRM, DIA, IWM, QQQ, XLV, XLF, CRWD — 13 names)

All 7 enforced adjustments above are ADVISORY-ONLY per the overlay's own permission model — none write to `proposed_signals`, none change tier for live/Telegram routing (all remain capped `market_closed_intraday_planning_only` until RTH confirmation per each candidate's `paper_entry_confirmation` rule: one closed 15m bar beyond trigger + VWAP).

## 6. Market Landscape

- **Crypto**: BTC trend transition_up, ETH range, altcoin breadth 65.0% above EMA20 / 55.0% above EMA50 — mildly constructive tape sitting under a heavy macro risk-off overlay (100/100) driven by the escalating Coldcard hack ($100-130M, 15 attackers) and continued Iran/Strait-of-Hormuz tension (missile-stockpile depletion reporting, Syria-Russia oil-sanctions negotiation). Top RS movers (SNXXB, SNDKB, MUB, HOME, KORUB, TUT, BTW, SOXLB) skew small/mid-cap momentum with thin volume (0.08-0.68x 20-period average) — several already flagged overextended or squeeze-prone (HOME).
- **Stocks**: US cash session not open until 09:30 ET / 16:30 EEST. Internal desk regime label: risk_off/short-bias, VIX 15.67, breadth 0% above EMA20/50 (index 5d/20d returns nan — same unresolved data gap from the standing TODO). **This label is stale relative to fresh external data**: S&P futures +0.3%, Dow futures +0.8%, Nasdaq-100 futures +0.9% premarket, VIX down to 15.59, following Monday's +1.48% close — driven by earnings strength (Caterpillar +9% premarket on record sales, Palantir +14% after-hours on an "otherworldly" quarter) plus a secondary, disputed Iran de-escalation signal. AMD/CAT/SMCI report earnings today; LLY/UBER tomorrow — avoid chasing into any of the three today.

### Market Mood / Risk Routing

- Crypto mood: **risk-off / chop, mildly improving** (breadth/trend better than 11:39, but the Coldcard catalyst is escalating, not resolving)
- Stocks mood: **mixed / unresolved** (internal label says risk_off, fresh premarket data says risk-on-on-earnings; treat as genuinely contested until RTH confirms one side)
- Dominant narrative: escalating BTC self-custody exploit risk (now 15 attackers) competing against altcoin RS leadership (HOME/TUT/BTW) and an earnings-driven stocks premarket rally (CAT/PLTR) that the desk's own regime classifier hasn't caught up to yet
- Preferred side now: **wait-for-trigger** on crypto (mild bearish lean from the macro overlay); **wait for RTH confirmation** on stocks — do not assume either the internal risk_off label or the premarket risk-on tape is the final word
- Best long candidate: HOME/USDT (crypto, chase-risk — wait for the stated pullback) / BAC (stocks, strongest fundamentals of the 7 reviewed but still capped market-closed-planning-only)
- Best short candidate: KAITO/USDT — needs a confirmed failed-bounce structure, not a fresh-weakness chase
- Best catalyst-backed candidate: BTC/USDT — Coldcard exploit escalation watch (now the largest ongoing self-custody theft this cycle, 15 attackers)
- What to avoid: chasing HOME at current extension; NFLX/SMH longs (both explicitly rejected by the freshest pipeline run); new crypto scalp entries (structurally negative); any stocks entry before RTH confirmation, regardless of which regime label turns out to be right
- What would change the view: a Coinkite/Galaxy resolution statement or a clean 24-48h with no new attacker on Coldcard; a genuine volume-backed pullback into the HOME zone; the first 15-30 min of RTH price action resolving the internal-vs-external stocks regime contradiction one way or the other

## 7. Candidate Deep Dives

### BTC/USDT — catalyst-watch (macro risk driver, escalating)
- Has price reacted to the catalyst? Partially — BTC is recovering toward $64k even as the theft total climbs, i.e. the market is treating this as a self-custody/protocol-specific risk rather than a systemic BTC risk.
- Chasing / retest / overextended? N/A — risk-context watch, not a directional entry.
- Actionable level: a formal Coinkite/Galaxy Research resolution/containment statement, or a clean 24-48h window with no new attacker joining and no new theft wave.
- Aligned with mood? Yes — primary source of today's crypto macro risk-off score (100/100).
- Long/short/wait? Wait-for-trigger (macro context, not a directional trade).
- Catalyst confirmation: **confirmed and escalating** — Galaxy Research now puts confirmed losses at $100M/1,596 BTC across 7,300+ addresses, with a suspected ceiling of $130M/2,055 BTC, and reports 15 independent attackers now exploiting the same firmware flaw (root cause: a March 2021 Coldcard firmware change that reduced recovery-seed entropy, making keys reproducible offline without device access).

### HOME/USDT — long-watch (best crypto long candidate), squeeze-risk flagged
- Top RS mover this cycle (24h +46.0%, 7d +58.1%, RS/BTC +44.1%), desk's own trade-idea agent scores it only 51.7/100 (watchlist, low confidence) — "evidence is not strong enough for an active trade."
- No fresh verified catalyst (pure `momentum_breakout` basket).
- Derivatives: negative funding across bybit (-1.34%), mexc (-1.31%), okx (-0.71%); crowding **elevated** — classic short-squeeze setup layered on an already-extended move, which cuts both ways (a squeeze could extend it further, or a funding-flip could trigger a sharp reversal).
- Chase-risk: high at current price (~0.0091, above the stated conditional entry zone 0.0086-0.0090); invalidation if activated: 1h close below 0.0082.
- Separately, an open B-tier swing long (`sig_57d425cf4bc41003`, triggered, entry 0.00604-0.00617) is already running from a prior cycle — no new entry needed there.

### KAITO/USDT — short-watch (best crypto short candidate)
- Weak_vs_market bias persists: 24h -8.66%, RS/BTC -10.52% (essentially unchanged from 11:39's -9.68%/-11.36%).
- Not yet a confirmed failed-bounce structure — do not short purely on the relative-weakness score.
- Actionable level: confirmed failed-bounce (crypto_failed_bounce_short playbook, 14d WR 40%/PF 2.00) plus independent derivatives confirmation before entry.
- Note: an existing open B-tier intraday long on KAITO (`sig_c48e5a1bfac269cb`, tp2_hit, entered ~Jul 21) already banked its wins before this week's weakness emerged — no live conflict.

### BAC — stocks long-watch (strongest of the 7 pre-US candidates, still planning-only)
- Pre-gate tier A, base_score 83.23 — highest of the 7 reviewed, but capped to C (`market_closed_intraday_planning_only`) until RTH confirmation.
- Catalyst present and genuinely bullish-leaning but not <24h fresh: JPMorgan raised its BAC price target to $68 from $62.50 (Overweight); MDSec Consulting acquisition announced Jul 30; dividend increase declared Jul 24; financials broadly outpacing on a steeper yield curve.
- No RS-vs-XLF/sector confirmation available (internal Sector Rotation table returns nan for RS calculations — see §14 TODO); this alone blocks a SUPPORT verdict regardless of how good the catalyst looks.
- Legal/headline check: clear — no indictment, investigation, or restatement risk found.
- Actionable level: `stocks_intraday_breakout_1bar_paper_v1` confirmation — one closed 15m bar beyond the 62.49 entry trigger **and** VWAP — only after the RTH open, plus genuine RS confirmation vs XLF/SPY once real intraday data exists.

### NFLX — stocks avoid-candidate (rejected by fresh pipeline, chase risk)
- Explicitly rejected by today's 11:30 pipeline run for `long_in_risk_off_regime, rs_not_exceptional_for_risk_off_long`.
- Stock is 46% off its 52-week high and down 21% YTD; the pre-US entry_trigger (73.32) sits essentially at the Aug-3 session high (72.18-73.95 range) — a breakout-style long on a name in a severe downtrend is a textbook chase/dead-cat-bounce setup.
- Recent headlines are mixed, not a clean bullish catalyst: "Big Screens Are Beating Streaming... Have Left NFLX Buffering" (bearish-leaning) vs "3 Big Reasons to Love Netflix" (bullish-leaning) — no single confirmed material catalyst either way.
- Company fundamentals (sales +13% YoY, operating profit +11%, guidance met per late-July results) are genuinely fine — the setup risk here is technical/chase, not a fundamental red flag.

### SPY — stocks neutral/contested (internal-vs-external regime contradiction)
- Rejected by the 11:30 pipeline run as `long_in_risk_off_regime`, but fresh external premarket data (S&P futures +0.3%, Dow +0.8%, Nasdaq +0.9%, VIX 15.59 down) directly contradicts that internal risk_off label.
- Index — no single-entity catalyst to resolve, no RS-vs-self applicable; this candidate's fate is entirely a call on which regime read is right, which only RTH price action can answer.
- Not actionable pre-open either way; watch the first 15-30 min of RTH for a clean resolution.

## 8. Best Candidates Ranked

1. **Long-watch (crypto): HOME/USDT** — trigger: 1h close inside 0.0086-0.0090 with volume; invalidate below 0.0082; squeeze-risk cuts both directions, do not chase current price.
2. **Short-watch (crypto): KAITO/USDT** — trigger: confirmed failed-bounce structure + independent derivatives confirmation; do not short on RS-weakness score alone.
3. **Catalyst-watch (crypto): BTC/USDT** — trigger: Coinkite/Galaxy resolution statement, or 24-48h with no new attacker/theft wave.
4. **Long-watch (stocks, pre-open planning only): BAC** — trigger: RTH confirmation (one closed 15m bar beyond 62.49 + VWAP) plus genuine RS vs XLF/SPY once intraday data exists; WMT (short) is the only regime-aligned candidate of the 7 but lacks a material catalyst.
5. **Stocks watchlist, contested regime: SPY** — trigger: first 15-30 min of RTH resolving the internal-risk_off-vs-external-premarket-risk-on contradiction.
6. **Open-position watch (no new entries)**: 24 crypto B-tier positions (2 waiting, 5 entered-unresolved, 17 needs-review/legacy) and 50 stocks positions (nearly all needs-review/legacy) — monitor invalidation levels only.
7. **Avoid: NFLX and SMH stocks longs (both rejected by the freshest pipeline run); HOME/USDT at current extension; crypto scalp mode.**

No A-tier setup cleared the desk threshold in any crypto mode or stocks intraday this cycle, and no pre-US candidate reached SUPPORT.

## 9. Avoid / No Trade (this decision window only)

- **NFLX long (stocks pre-open)** — rejected by fresh pipeline, 46% off highs, chase-risk at the recent session high.
- **SMH long (stocks pre-open)** — rejected by fresh pipeline for the same regime reason.
- **HOME/USDT at current spot** — chase-risk; +46.0% 24h, squeeze-prone but not a clean continuation entry.
- **Crypto scalp mode** — structurally negative this week (PF 0.167, 0W-3L).
- **Crypto weekend cohort** — underperforms (winrate 11%, n=10); avoid new weekend-mode entries.
- **Stocks — all names** — market not yet open; every candidate is planning-only until RTH confirmation, regardless of which regime read (internal risk_off vs external premarket risk-on) turns out correct.
- **AMD, CAT, SMCI** — earnings land today; gap/chase risk regardless of direction.
- This is a decision-window verdict only — **not** a recommendation to pause scanning, tracking, or the scheduler, all of which continue normally.

## 10. Main Risks

- **Coldcard exploit escalating** — confirmed $100M/1,596 BTC, suspected ceiling $130M/2,055 BTC, now 15 independent attackers (up from 3 waves at 11:39) — a genuine worsening trend, not stabilizing; a fresh large wave would deepen crypto's risk-off mood further.
- **Internal stocks regime label may be stale/wrong at the open** — risk_off/short-bias computed from data showing 0% breadth and nan index returns, while fresh premarket data shows broad risk-on (futures up, VIX down, earnings-driven). Trading either side on the internal label alone before RTH confirms is risky.
- **Catalyst mapping weak and worsening** — 60.2% unmapped today (57.2% at 11:39, 53.2% at 04:45) — three consecutive reviews trending the wrong way; treat the catalyst layer as context only.
- **RS-vs-sector data unavailable (nan)** — blocks genuine SUPPORT-level confirmation for every stocks pre-US candidate today, including the strongest one (BAC); this is a structural gap in today's decision quality, not a candidate-specific weakness.
- **Untracked legacy alerts** — 2 TUT/USDT alerts (09:00, 12:47 UTC) sent to Telegram without a backing `proposed_signal`; matches the previously-identified watchlist-alert signal-reuse bug (prior TODO-3).
- **Legacy open-position volume** — 24 crypto + 50 stocks "active" signals include dozens with `expires_at` weeks in the past still showing tp1/tp2_hit/triggered; lifecycle status ambiguous (standing TODO, unresolved since 11:39).
- **Stocks short-side edge weak** — PF 0.14, 1W-10L (n=91) — avoid leaning on short signals without independent confirmation, including WMT (the one regime-aligned pre-US candidate today).

## 11. Action Plan — next 4 hours

- Watch for a Coinkite/Galaxy resolution statement or a new Coldcard attacker/wave before the next review; treat the exploit as ongoing, not contained.
- Watch HOME/USDT for a genuine volume-backed pullback into 0.0086-0.0090 — do not add at current extension; monitor funding for a squeeze vs. reversal resolution.
- Watch KAITO/USDT for a confirmed failed-bounce structure before treating it as a clean short.
- At the 09:30 ET / 16:30 EEST open: watch BAC first 15-30 min for the paper-entry confirmation (closed 15m bar beyond 62.49 + VWAP); watch SPY/broad tape to resolve the internal-vs-external regime contradiction; do NOT treat NFLX or SMH as a clean long even after the open without a fresh reassessment — both were explicitly rejected by the desk's own scorer this morning.
- No new crypto scalp or weekend-mode entries this window.
- Continue scanning, tracking, and monitor processes in all cases — no pause recommended for any mode or asset class.

## 12. Final Verdict per Mode

- **Crypto scalp:** No trade. Structurally negative this week (PF 0.167, 0W-3L).
- **Crypto intraday:** Watch-only. Best name HOME/USDT (score 51.7), chase-risk at current extension; strongest-performing mode by week stats (PF 3.34) but nothing clears the desk threshold this cycle.
- **Crypto swing:** Selective watch. Existing open positions (HFT, HOME, EPIC, AEVO, COTI) continue to be monitored; no new entries this window.
- **Stocks intraday:** Planning-only until 09:30 ET RTH open. BAC is the strongest pre-open candidate (pending RTH confirmation + RS check); WMT is the only regime-aligned short but lacks a material catalyst; NFLX and SMH are avoid, not watch, given the fresh pipeline rejection.
- **Stocks swing/invest:** Stale (>1 month, deprecated frameworks) — excluded from this cycle's verdict, unchanged status.

## 13. Sources

- [Stock Market: Will S&P 500 Open Up or Down Today?](https://www.benzinga.com/markets/prediction-markets/26/08/60896308/sp500-aug-4-open-up-or-down-polymarket-trump-iran-tech-rally-amazon-ai-earnings) — Benzinga, 2026-08-04.
- [Stock market today: Dow, S&P 500, Nasdaq futures rise as earnings roll in](https://finance.yahoo.com/markets/live/stock-market-today-tuesday-august-4-dow-sp-500-nasdaq-100140227.html) — Yahoo Finance, 2026-08-04 (WebFetch-verified: VIX 15.59, futures up 0.3-0.9%, CAT/PLTR earnings driving sentiment).
- [Bank of America (BAC) Stock Forecast / press releases](https://tickeron.com/ticker/BAC/forecasts-predictions/) and [Yahoo Finance BAC press releases](https://finance.yahoo.com/quote/BAC/press-releases/) — JPMorgan PT raise to $68, MDSec acquisition (Jul 30), dividend increase (Jul 24).
- [Netflix Stock Down 46%: Is Now the Time to Buy NFLX in August 2026?](https://intellectia.ai/blog/netflix-stock-analysis-august-2026) — 2026-08, 46% off 52wk high / 21% YTD figures.
- [Coldcard Hack Losses Hit $100M With 1,596 BTC Stolen in Ongoing Attack](https://www.cryptotimes.io/2026/08/04/coldcard-hack-losses-hit-100m-with-1596-btc-stolen/) — CryptoTimes, 2026-08-04.
- [15 Attackers Exploit Ongoing Coldcard Hack as Losses Approach $130M](https://www.cryptotimes.io/2026/08/04/coldcard-exploit-15-attackers-130m-losses-galaxy/) — CryptoTimes, 2026-08-04.
- [Galaxy estimates Coldcard exploit may have stolen up to 2,055 Bitcoin](https://crypto.news/galaxy-estimates-coldcard-exploit-may-have-stolen-up-to-2055-bitcoin/) — crypto.news, 2026-08.
- Internal: `data/reports/scalp/2026-08-04_11-06_scalp_report.md`, `data/reports/intraday/2026-08-04_11-12_intraday_report.md`, `data/reports/swing/2026-08-04_03-22_swing_report.md`, `data/reports/stocks/intraday/2026-08-04_11-30_stocks_intraday_report.md`, `data/catalysts/2026-08-04/catalyst_cycle_11-15.md`, `catalyst_events.jsonl`, `narrative_baskets.jsonl`, `data/processed/llm_analysis_packet.md`, `data/processed/llm_stocks_packet.md`, `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md`, `OPUS_ENRICHED_REVIEW_AUTO_2026-08-04_1139.md`.

## 14. Fix Requests / TODO

### TODO-stocks-rs-nan-blocks-preus-support (priority: high, new)
- **issue:** The stocks intraday report's Sector Rotation table returns `RS vs SPY 20d=+nan%` for every sector (XLK, SMH, etc.), and index 5d/20d returns are also `+nan%`. This means the pre-US stocks overlay's `relative_strength_confirmed` SUPPORT precondition can **never** be honestly satisfied under current data — every eligible candidate this run was capped to NEUTRAL/CAUTION/INSUFFICIENT_DATA at best, purely because RS math is broken, not because the candidates were necessarily weak (BAC in particular had a real catalyst).
- **evidence:** `data/reports/stocks/intraday/2026-08-04_11-30_stocks_intraday_report.md` §2 Sector Rotation ("Benchmark (SPY) 20d return: +nan%"; "technology (XLK): RS vs SPY 20d=+nan%"); same nan pattern present in the 11:39 review's TODO for index returns.
- **suggested manual fix:** trace why 20d RS/return calculations return nan — likely an insufficient historical-bar lookback or a broken join on the OHLCV source for these tickers; this silently defeats the entire purpose of the RS-confirmation requirement in the pre-US overlay spec.
- **priority:** high
- **first observed:** 2026-08-04 16:11 EEST (this run; the underlying nan issue is the same one carried in TODO-stocks-breadth-data-gap below, first observed 11:39).

### TODO-preus-funnel-stale-vs-fresh-pipeline (priority: medium, new)
- **issue:** `stocks-preus-candidates` (funnel snapshot at 13:01 UTC, built from signals created 00:10-06:05 UTC) listed SPY, NFLX, and SMH as eligible/promotable longs. The freshest regular intraday pipeline run (11:30 UTC) explicitly **rejected** long setups on all three of these exact tickers today for `long_in_risk_off_regime, rs_not_exceptional_for_risk_off_long`. The pre-US overlay funnel does not appear to re-check against the latest same-day pipeline rejection before presenting a candidate as "eligible."
- **evidence:** `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md` (SPY base_score 71.25, NFLX 67.81, SMH 54.5, all created before 06:05 UTC) vs `data/reports/stocks/intraday/2026-08-04_11-30_stocks_intraday_report.md` §8 Rejected/Not Ready (SPY 46.65, NFLX 48.18, SMH 45.66, all `long_in_risk_off_regime`).
- **suggested manual fix:** have the preus-candidates funnel cross-check each eligible signal's ticker+direction against the most recent same-day intraday report's Rejected list, and either exclude or flag those that were freshly rejected, rather than relying solely on the earlier snapshot's own tier/cap logic.
- **priority:** medium
- **first observed:** 2026-08-04 16:11 EEST.

### TODO-stocks-breadth-data-gap (priority: medium, carried forward, unresolved)
- **issue:** `llm_stocks_packet.md` / stocks intraday report §1 Stock Market Regime still shows `Breadth above EMA20: 0.0%`, `Breadth above EMA50: 0.0%`, and index 5d/20d returns as `+nan%`, driving the `risk_off` regime label — now directly contradicted by fresh external premarket data (futures up, VIX down) at this pre-US-open slot.
- **evidence:** `data/reports/stocks/intraday/2026-08-04_11-30_stocks_intraday_report.md` §1; same gap reported in the 11:39 review, unresolved three cycles later.
- **suggested manual fix:** as previously suggested — add a pre-market/session-gap guard to the stocks regime classifier so it doesn't emit a confident `risk_off` label off nan/zero breadth inputs, especially right before the cash open when the label most directly drives operator decisions.
- **priority:** medium
- **first observed:** 2026-08-04 11:39 EEST (carried forward, still unresolved).

### TODO-catalyst-mapping-persistently-weak (priority: low, recurring, worsening)
- **issue:** Catalyst→symbol mapping has been over the 50% unmapped threshold for at least three consecutive reviews and is trending worse: 53.2% (04:45) → 57.2% (11:39) → 60.2% (this run).
- **evidence:** `data/catalysts/2026-08-04/catalyst_events.jsonl` (2500 rows today, 1504 null-symbol, computed this run).
- **suggested manual fix:** revisit the symbol resolver in the catalyst layer per the earlier-raised TODO; the trend (getting worse, not better) suggests this isn't just a stable share of un-mappable macro noise.
- **priority:** low
- **first observed:** 2026-08-04 04:45 EEST (carried forward, still unresolved, still worsening).

### TODO-untracked-tut-alert (priority: high, recurring instance of known bug)
- **issue:** 2 TUT/USDT Telegram alerts (B-tier, 65.8 and 75.0, sent 09:00:04 and 12:47:37 UTC today) fired without a backing `proposed_signal` within 6h — they will not contribute to PF/winrate/avgR tracking. This is the same watchlist-alert signal-reuse pattern previously confirmed on ALLO/USDT and BANK/USDT.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-04` output this run: 2 untracked legacy crypto alerts, both TUT/USDT.
- **suggested manual fix:** as already raised in the prior TODO-3 (raised to high priority 2026-07-17): fix the watchlist-alert path so a re-fire mints a fresh `proposed_signal` instead of reusing a stale/closed `signal_id`.
- **priority:** high (matches the existing raised priority; this is a fresh instance, not a new root cause)
- **first observed root cause:** 2026-07-17 (ALLO/USDT, BANK/USDT); **this instance observed:** 2026-08-04 16:11 EEST (TUT/USDT).

### TODO-legacy-open-position-volume (priority: medium, carried forward, unresolved)
- **issue:** `active-signals` still returns dozens of rows (17/24 crypto, ~48/50 stocks) with `expires_at` dates in the past while status reads `tp1_hit`/`tp2_hit`/`triggered` — unclear whether these are correctly "not yet finally closed" by design or a stuck closure job.
- **evidence:** e.g. `sig_233f3bc872fbc9ae` (JPM swing, tp1_hit, expires_at 2026-07-08T03:09:43) still present in this run's `active-signals --asset-class stocks` output.
- **suggested manual fix:** unchanged from the 11:39 review — a human-driven session should confirm the intended lifecycle semantics and, if needed, add clearer status labeling in the CLI output.
- **priority:** medium
- **first observed:** 2026-08-04 11:39 EEST (carried forward, still unresolved).
