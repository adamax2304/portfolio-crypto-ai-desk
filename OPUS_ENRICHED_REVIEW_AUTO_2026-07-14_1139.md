# Opus Enriched Review — Europe / Pre-US Context — Auto Cycle 11:30 EEST

## 1. Executive Summary

**Slot: Europe / pre-US context (11:30 EEST / 08:39 UTC) — advisory only / no auto-trade.** Focus: what changed since the overnight review, whether crypto signals are still valid, and building the US-session watchlist. US cash market is still closed (opens ~13:30 UTC / 16:30 EEST) — stocks are pre-market/planning context only, not confirmed intraday entries.

**Scheduler fresh, no defer.** Latest cycle (`cycle_04_09-44`) finished 10:11 EEST, ~1.5h old — well under the 3h defer threshold. Crypto scalp/intraday fresh (~09:51/09:56 EEST). Crypto swing is **carry-forward** (05:15 EEST, ~6.4h old — inside the 4–12h window, used for context, not as a fresh signal source). Stocks intraday fresh (10:06 EEST) but explicitly market-closed-capped by the pipeline itself. Stocks swing/invest are **stale (~12 days, 2026-07-02)** — excluded from live decisions, known-deprecated legacy mode.

**Quiet cycle again — no new A/B anywhere.** Crypto scalp, intraday, and swing each independently report "No A-tier / No B-tier setups found" this cycle; all crypto ideas are watchlist-only. Stocks intraday found 4 raw A-tier + 10 raw B-tier candidates but every one is demoted to C via `market_closed_intraday_planning_only` (expected pre-open behavior). This matches a genuinely quiet pre-US-open cycle, not a pipeline gap.

**Crypto regime unchanged and still risk-off.** BTC `transition_down`, ETH `range`, altcoin breadth 26–36% above EMA20 — desk's own recommended style is "short bias or no trade; avoid weak altcoin longs." Verified externally: Bitcoin has been trading in a war-driven-but-muted band (~$62–64k) after renewed Iran/Strait-of-Hormuz strikes; unlike gold/oil/equities, BTC is "no longer trading the war," taking direction mainly from dollar liquidity and the chip cycle (CoinDesk, 2026-07-13).

**Overall verdict: CAUTION, routed by side — not a blanket no-trade.** Best short-watch: **TAO/USDT** (active B-tier swing short, failed-bounce retest 198.99–200.09, aligned with regime) but the desk's own derivatives cross-check flags squeeze risk (OI up while price down). Best long-watch: **VELVET/USDT** (RS-leader vs. BTC +14–17%, OI+price both up = fresh positioning confirms trend, low funding) — extended, wait for a hold-and-retest, do not chase. Best catalyst-watch: **NVDA** — fresh, multi-outlet-verified China AI-chip screening story, real but currently a risk/uncertainty catalyst, not yet a clean directional score (42.6, no_trade). Avoid: **AVGO** — internal signal is SHORT (score 79.5) but external news is strongly bullish (confirmed $30B multi-year Apple deal, AI revenue +143% YoY) — a genuine catalyst-vs-technical contradiction, on top of being market-closed-demoted to C anyway. Also flagged: **UNH** carries an active, externally-confirmed DOJ Medicare-billing investigation (open since July 2025, no indictment yet) — the desk's own gate already demotes any *new* UNH A/B to C with `legal_headline_risk: sec_doj`; existing UNH B-tier positions in `active-signals` predate that flag and should get a manual look. Scanning, tracking, and the paper book continue uninterrupted.

## 2. Data Used

- Crypto scalp report: `2026-07-14_06-51_scalp_report.md` (gen 09:51 EEST). No A/B.
- Crypto intraday report: `2026-07-14_06-56_intraday_report.md` (gen 09:56 EEST, data 06:45 UTC). No A/B; regime bearish/risk-off; best RS names SXT/USDT (overextended, 6.81x volume) and NEAR/USDT (OI down + price up = short covering).
- Crypto swing report: `2026-07-14_02-15_swing_report.md` (gen 05:15 EEST, ~6.4h old — **carry-forward**). Contains the active TAO/USDT short idea (score 65.3) matching the live `active-signals` row.
- Stocks intraday report: `2026-07-14_07-06_stocks_intraday_report.md` (gen 10:06 EEST, fresh). 4 raw A-tier + 10 raw B-tier, all demoted to C (`market_closed_intraday_planning_only`); UNH additionally gated `legal_headline_risk: sec_doj`.
- Stocks swing/invest: 2026-07-02, ~12 days stale, deprecated legacy mode — excluded.
- Catalysts: `data/catalysts/2026-07-14/catalyst_events.jsonl` (2,000 events today) + `narrative_baskets.jsonl` (4 baskets) — computed directly (§5).
- LLM packets: `llm_analysis_packet.md` (09:56 EEST), `llm_stocks_packet.md` (10:07 EEST).
- CLI: `active-signals --asset-class crypto` (21 rows, all B-tier, triggered/tp1_hit/tp2_hit), `active-signals --asset-class stocks` (50 rows: 1 A-tier AMZN + 1 B-tier XOM + 1 B-tier NVDA non-terminal, rest historical/aged C-tier), `signal-stats` crypto (tier=B n=154 PF 1.14 but triggered winrate only 13.8% per the tool's own observation; scalp mode PF 0.14, losing; short direction PF 0.5, weak), `signal-stats` stocks (tier=C n=204 PF 0.79, winrate 11.2% — below-0.8 PF flagged by the tool itself), `detect_untracked_legacy_alerts --since 2026-07-14` (**0 found**).
- Direct file read: `reports/PAPER_MONITOR_STATUS_LATEST.md` (10:09 EEST) — lifecycle counts (§3) do not reconcile with `active-signals` non-terminal rows; same gap flagged in the prior 04:55 review, carried forward as §14 TODO.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-14_0455.md` (04:55 EEST, ~6.7h ago) — comparison baseline for §4.
- External: 4 WebSearch queries (UNH DOJ status, NVDA China chip screening, BTC/Iran war reaction, AMZN news) + 1 WebSearch (AVGO news) + 2 WebFetch (CoinDesk BTC article confirmed live; CNBC UNH article 403'd, fallback sources used) — sources in §13, ingested into `news_items` (8/8 valid, 0 rejected).

## 3. Scheduler / Data Freshness

- `scheduler.log` (`2026-07-14_default_schedule`): last cycle `cycle_04_09-44` finished 10:11 EEST — **fresh** (~1.5h old at review time, well under 3h defer threshold).
- Crypto scalp/intraday: **fresh** (09:51–09:56 EEST). 0 fresh A/B is consistent, quiet pre-open behavior.
- Crypto swing: **carry-forward** (05:15 EEST, ~6.4h old, within the 4–12h window) — used for the active TAO short context only.
- Stocks intraday: **fresh** (10:06 EEST) but fully session-capped (US cash market closed until ~16:30 EEST).
- Stocks swing/invest: **stale**, ~12 days, deprecated legacy mode — excluded.
- `PAPER_MONITOR_STATUS_LATEST.md`: **fresh** (10:09 EEST) but its lifecycle counts (0/0/0/0 across OPEN/WAITING/REVIEW/UNRESOLVED, 70 NO_ENTRY_EXPIRED) still do not reconcile with the 71 non-terminal rows (21 crypto + 50 stocks minus terminal ones) in `active-signals` — persistent gap, first flagged in the 04:55 review, not something this read-only review can resolve (§14).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-07-14 11:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["stocks swing/invest ~12 days stale, excluded"],
      "suggested_effect": "advisory_only", "facts_used": ["cycle_04_09-44 finished 10:11 EEST", "crypto scalp/intraday 09:51-09:56 EEST", "crypto swing 05:15 EEST ~6.4h old carry-forward", "stocks intraday 10:06 EEST"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.8,
      "reason_codes": ["risk_off", "shorts_preferred", "chop", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["BTC trend transition_down, ETH range", "altcoin breadth 26-36% above EMA20", "recommended style: short bias or no trade", "stocks regime label chop, VIX 17.16, breadth 50%/100%", "BTC muted war reaction, taking direction from dollar liquidity/chip cycle (CoinDesk)"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "catalyst_contradicted"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["277/2000 (13.8%) catalyst events mapped to a symbol this run — well below 50%", "4 narrative baskets: perps_dex_narrative/HYPE, binance_ecosystem_teaser/BNB, delisting_thin_liquidity/STG, momentum_breakout/ZBT", "AVGO internal SHORT signal contradicted by confirmed bullish $30B Apple deal + 143% YoY AI revenue growth"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "oi_supports", "data_unavailable"], "data_missing": ["OI/funding n/a for several weakest-symbol shorts (SYN, DEXE, LUMIA)"],
      "suggested_effect": "advisory_only", "facts_used": ["TAO/USDT: price down + OI up +8.06% = fresh shorts pressing, possible squeeze if price reclaims", "VELVET/USDT, ZBT/USDT: price up + OI up = fresh positioning confirms trend", "NEAR/USDT: price up + OI down = short covering, weaker continuation quality"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["entry_late", "overextended", "clean_retest", "chase_risk"], "data_missing": ["current live price vs. 05:15 EEST swing-report snapshot for TAO"],
      "suggested_effect": "advisory_only", "facts_used": ["TAO/USDT entry zone 198.99-200.09, price was 198.50 at 05:15 EEST — already through/near the zone, desk itself warns 'no late short after a vertical flush'", "SXT/USDT tagged overextended, 6.81x volume", "VELVET/USDT 24h +15.99%, already extended, needs pullback per its own playbook"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.5,
      "reason_codes": ["entered_unresolved", "no_entry", "needs_review"], "data_missing": ["reconciliation between active-signals non-terminal rows and PAPER_MONITOR_STATUS lifecycle buckets"],
      "suggested_effect": "advisory_only", "facts_used": ["active-signals: 21 crypto (all B, triggered/tp1_hit/tp2_hit) + 50 stocks (1 A + 2 B non-terminal, rest aged C)", "PAPER_MONITOR_STATUS_LATEST.md: OPEN_ACTIVE=0, WAITING_FOR_ENTRY=0, REVIEW_ONLY_SHADOW=0, ENTERED_UNRESOLVED_EXPIRED=0, NO_ENTRY_EXPIRED=70"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["headline_risk", "manual_review", "reduce_risk"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["UNH: confirmed active DOJ Medicare-billing investigation (open since July 2025, no indictment) — desk gate legal_headline_risk: sec_doj", "AVGO: internal short vs. confirmed bullish $30B Apple deal news — catalyst contradiction", "crypto direction=short PF 0.50 (weak, n=20)", "JPM earnings today — do_not_chase_warning already active in the pipeline"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_failing", "low_sample", "playbook_working"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["crypto tier=B triggered winrate 13.8% (own tool observation)", "crypto scalp mode PF 0.14, losing (n=38)", "stocks tier=C PF 0.79, winrate 11.2% (own tool observation, below-0.8 flag)", "crypto weekend=Y PF 3.29 vs weekend=N PF 0.54 — same weekend-effect skew as prior review", "stocks headline A/B n=10, weak-confidence sample"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.65,
      "reason_codes": [], "data_missing": [], "suggested_effect": "advisory_only", "facts_used": [] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "shorts_crypto_wait_for_trigger_stocks",
    "best_long_candidate":     { "symbol": "VELVET/USDT", "trigger": "hold-and-retest of a pullback zone after the +15.99% 24h move; wait for volume-confirmed reclaim, OI+funding stay supportive (OI 24h +5.36%, funding 5e-05, low crowding)", "reason": "RS-leader vs BTC (+17.37%), price+OI both up confirms fresh positioning, but already extended — chasing here is the failure mode" },
    "best_short_candidate":    { "symbol": "TAO/USDT", "trigger": "failed bounce/retest into 198.99-200.09, invalidation 1h close beyond 201.44; confirm bearish HTF structure before entry", "reason": "active B-tier swing short aligned with the desk's own short-biased regime read, but derivatives cross-check flags OI up while price down = squeeze risk if BTC/ETH reclaim local levels" },
    "best_catalyst_candidate": { "symbol": "NVDA", "trigger": "wait for a directional technical setup to form around the China-chip-screening story before treating it as tradable (currently no_trade, score 42.6)", "reason": "fresh, multi-outlet-confirmed (FT via Seeking Alpha/Benzinga/Zawya) China AI-chip buyer-list crackdown — real catalyst but currently a risk/uncertainty item, not yet a clean long or short" },
    "avoid_candidate":         { "symbol": "AVGO", "reason": "internal signal is SHORT (score 79.5) but external news is strongly bullish: confirmed $30B multi-year Apple custom-silicon deal, Q2 AI revenue +143% YoY, Strong-Buy analyst consensus — a genuine catalyst-vs-technical contradiction on top of being market-closed-demoted to C" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.80 | risk_off, shorts_preferred, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, fresh_catalyst, catalyst_contradicted | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | entry_late, overextended, clean_retest, chase_risk | advisory_only |
| execution_lifecycle | needs_review | 0.50 | entered_unresolved, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.65 | headline_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.60 | playbook_failing, low_sample, playbook_working | advisory_only |
| head_trader | caution | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (04:55 EEST)

- **Crypto regime unchanged**: still `transition_down` BTC / `range` ETH / short-biased style. No new A/B in scalp, intraday, or swing — same "genuinely quiet" pattern as the overnight cycle.
- **TAO/USDT short**: still the only clean crypto swing idea in the active book; same entry zone (198.99–200.09), same invalidation (201.44). Thesis unchanged, not invalidated, not yet confirmed either.
- **Prior best-long-watch ALLO/USDT and best-short-watch LUMIA/USDT** no longer appear as fresh top-flow names this cycle (deprioritized to weakest-symbols/swing watchlist tail) — **VELVET/USDT** and **TAO/USDT** replace them as the cleanest long/short reads this cycle.
- **Prior best-catalyst-watch HYPE/USDT** (spot-ETF inflow) has rolled off the top narrative-basket list; `perps_dex_narrative`/HYPE basket is still active but no longer the top headline story. **NVDA China-chip screening** is the new dominant fresh catalyst this cycle (verified externally, multi-outlet).
- **New this cycle**: the AVGO catalyst-vs-technical contradiction (internal short vs. confirmed bullish Apple deal) — not present in the 04:55 review, surfaced fresh from today's stocks intraday scoring pass + external verification.
- **UNH legal/headline flag (`sec_doj`) persists** from the overnight review — still active, externally reconfirmed today (DOJ investigation ongoing since July 2025, no lawsuit/indictment filed as of this run).
- **Reconciliation gap** between `active-signals` and `PAPER_MONITOR_STATUS_LATEST.md` (§3) persists unchanged from the 04:55 review — still unresolved, still a §14 TODO, not re-diagnosed here (read-only routine).
- **Catalyst mapping got worse**: 04:55 review reported 437/500 (87.4%) unmapped; this run's larger pool (2,000 events) is 1,723/2,000 (86.2%) unmapped — same order of magnitude, still weak, still advisory-context-only.

## 5. Catalyst Coverage

- Total catalyst events today: **2,000**
- Mapped to a symbol: **277 (13.8%)**
- Unmapped: **1,723 (86.2%)**
- Narrative baskets: **4** — `perps_dex_narrative` (HYPE, playbook `wait_pullback`), `binance_ecosystem_teaser` (BNB, `related_beta_rotation`), `delisting_thin_liquidity` (STG, `avoid_low_liquidity`), `momentum_breakout` (ZBT, `wait_pullback`)

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Top 3 unmapped headlines:
1. "MEHR SAYS SEVERAL AREAS IN SOUTHWESTERN IRAN'S KHUZESTAN'S OMIDIYEH HIT BY U.S. PROJECTILES" (@WalterBloomberg) — macro/geopolitical, not symbol-specific.
2. "EMBC Investors Have Opportunity to Lead Embecta Corp. Securities Fraud Lawsuit" (PR Newswire) — legal-risk basket item, ticker not resolved by the mapper.
3. "US investigates possible Iranian drone storage in Cuba, Trump says" — macro/geopolitical, not symbol-specific.

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **risk-off** (BTC transition_down, ETH range, altcoin breadth 26–36% above EMA20, desk recommends short bias or no trade)
- Stocks mood: **pre-market / chop** (VIX 17.16, breadth 50% above EMA20 / 100% above EMA50, label "chop", market closed until ~16:30 EEST)
- Dominant narrative: AI/semiconductors (NVDA China-chip screening, AVGO Apple deal) and geopolitical/macro overhang (Iran/Strait-of-Hormuz strikes) — BTC increasingly decoupled from the war headline, tracking dollar liquidity/chip cycle instead
- Preferred side now: **shorts for crypto (with squeeze caution)**, **wait-for-trigger for stocks** (no RTH confirmation yet)
- Best long candidate: VELVET/USDT (wait for pullback — see §8)
- Best short candidate: TAO/USDT (failed-bounce retest — see §8)
- Best catalyst-backed candidate: NVDA (China chip screening, not yet a clean directional trade)
- What to avoid: AVGO short (catalyst-vs-technical contradiction); chasing JPM around today's earnings print; chasing any crypto short already through its entry zone without a clean retest
- What would change the view: BTC reclaiming range highs / altcoin breadth expanding above 50% would flip crypto bias toward longs; US cash open price action in the first 15–30 min will determine which of the demoted stocks A/B candidates (AAPL, UNH, META, SMH, AMZN, AVGO, GOOGL) re-qualify

## 7. Candidate Deep Dives

### 1. AMZN (stocks, A-tier in `active-signals`, long, intraday)
- **Signal**: `sig_78fb61c80fd77352`, entry 245.41–246.44, invalidation 244.38, expires 2026-07-14T14:23:20 UTC, status `triggered`.
- **Reconciliation flag**: this A-tier row is non-terminal in `active-signals`, but today's fresh stocks-intraday report (10:06 EEST) independently re-scores AMZN as **raw B-tier (79.7)**, demoted to **C** via `market_closed_intraday_planning_only` — and `PAPER_MONITOR_STATUS_LATEST.md` shows AMZN under `NO_ENTRY_EXPIRED` (C-tier row) with `touched=False`. These are two different AMZN rows (an older A-tier "triggered" signal vs. today's fresh C-tier watchlist re-score) but the discrepancy is confusing without more context — flagged for manual review, not resolved here (see §3 reconciliation gap).
- **External check**: no legal/headline risk found. AMZN priced $247.31, +0.8% 24h, +4.29% weekly; priced a $25B bond offering for ~$200B 2026 AI capex plan; AWS Q1 revenue +28% YoY; next earnings 2026-07-30 (Forbes/TradingKey/Yahoo Finance).
- **Verdict**: entry already triggered from a prior session and technically still valid per its own invalidation (244.38), but **no fresh RTH confirmation exists yet** — treat as carried-forward/needs-review, not a new actionable idea this cycle. Re-check at/after the US open.

### 2. UNH (stocks, active B-tier tp1_hit/tp2_hit swing+intraday rows in `active-signals`; legal/headline risk)
- **Internal flag**: today's stocks-intraday report demotes any *new* UNH A-tier idea (score 83, was A) to C with `legal_headline_risk: sec_doj — manual review required`.
- **External verification**: confirmed. UnitedHealth is under an active DOJ investigation into Medicare Advantage billing/upcoding practices, publicly disclosed July 2025 and ongoing through 2026 — company is cooperating with formal criminal/civil requests; no lawsuit or indictment filed as of this run (Medical Economics, HealthExec).
- **Legal/headline risk**: **AVOID for any new UNH A/B** — confirmed source + date, per §I. Existing UNH rows already in `active-signals` (multiple B-tier tp1_hit/tp2_hit, opened before this cycle's gate) predate this flag; they are not being closed by this read-only review, but a human should confirm whether those entries were opened knowing about the DOJ investigation.
- **Verdict**: MANUAL REVIEW REQUIRED. Also UNH earnings are within the week (2 trading days out) — swing-blocked by earnings per the stocks report.

### 3. AVGO (stocks, C-tier watchlist, short, raw B-tier score 79.5)
- **Internal signal**: short direction, score 79.5, demoted to C only because the market is closed (`market_closed_intraday_planning_only`) — otherwise this would have been a fresh B-tier actionable short.
- **External verification**: strongly bullish news dominates the tape — a confirmed, multi-year $30B+ custom-silicon/wireless deal with Apple (through 2031, ~20% of AVGO revenue), Q2 FY2026 AI semiconductor revenue $10.8B (+143% YoY), CEO guiding to $100B AI-chip revenue by 2027, 48-analyst consensus "Strong Buy" with $523.73 target (+35% from spot). Some countervailing signal: chip stocks broadly under pressure from geopolitical tension/AI-saturation concerns, and two insiders sold $10.2M in shares on 2026-07-08.
- **Has price reacted to the catalyst?** Partially — the Apple-deal pop already happened (+5.2% on confirmation), but the stock's technical/momentum score is still reading short. **Is the setup chasing?** A short here would be fighting a confirmed fundamental catalyst, not confirming one.
- **Verdict**: **AVOID as a short** this cycle — catalyst-vs-technical contradiction. If anything, this is a candidate to flip and watch for a long *if* a retest/pullback structure forms after the market opens; do not chase either side pre-open.

### 4. TAO/USDT (crypto, active B-tier swing short, `active-signals`)
- **Signal**: `sig_ebd0247c0d6803b4`, entry 198.99–200.09, invalidation 201.44, TP1/2/3 196.05/193.60/191.15, status `triggered`, expires 2026-07-21.
- **Setup**: failed-bounce/retest short, playbook `crypto_failed_bounce_short`, aligned with the desk's own bearish/short-biased regime call. No fresh verified catalyst for TAO specifically.
- **Has price already reacted?** At the 05:15 EEST snapshot, spot (198.50) was already inside/through the entry zone — a late entry now risks chasing a move already in progress; wait for a clean retest rather than market-order in.
- **Squeeze/crowding**: derivatives cross-check flags OI +8.06% while price is down — fresh shorts pressing, which the desk's own playbook explicitly warns can squeeze if BTC/ETH reclaim local levels. This is the single biggest risk to the short thesis.
- **Verdict**: best short-watch this cycle, but **wait for a confirmed failed-bounce retest**, not a market entry at current levels — squeeze risk is real per the desk's own data.

### 5. NVDA (stocks, C-tier `no_trade`, score 42.6; fresh catalyst)
- **Internal**: today's stocks-intraday report scores NVDA `no_trade` (42.58, no_directional_setup) despite the fresh catalyst — the technical/momentum layer has not turned this into a directional setup yet.
- **External verification**: confirmed, multi-outlet (Financial Times via Seeking Alpha, Benzinga, Zawya, Yahoo Finance) — Nvidia cut its approved Asian AI-chip buyer list by more than half amid tighter due-diligence/export-control screening in Singapore, Malaysia, and Japan, following concerns Blackwell chips reached China-linked entities. Excluded buyers can reapply after compliance fixes.
- **Has price reacted?** Report itself already carries this as a `risk_warning` (§5c of the intraday report) rather than a scored catalyst boost — appropriately conservative given the mixed (near-term revenue friction vs. long-term compliance de-risking) nature of the news.
- **Verdict**: real catalyst, currently **WATCH only** — no directional technical confluence yet. Re-check after the open for a clean setup; do not force a trade off the headline alone.

## 8. Best Candidates Ranked

1. **Short-watch: TAO/USDT** — trigger: failed bounce/retest into 198.99–200.09, invalidation 1h close beyond 201.44. Caution: squeeze risk (OI up, price down).
2. **Long-watch: VELVET/USDT** — trigger: hold-and-retest of a pullback zone after +15.99% 24h move, OI (+5.36%) and low funding still supportive. Do not chase the extended print.
3. **Catalyst-watch: NVDA** — trigger: wait for a directional technical setup (currently no_trade, score 42.6) to form around the confirmed China chip-screening story.
4. **Manual-review: UNH** — active DOJ Medicare-billing investigation (confirmed, ongoing since July 2025); avoid any new A/B; review existing open UNH rows.
5. **Avoid: AVGO short** — catalyst-vs-technical contradiction (confirmed bullish $30B Apple deal vs. internal short signal).

## 9. Avoid / No Trade (this decision window only)

- **AVGO short** — do not enter; catalyst contradicts the technical short thesis (see §7.3). This applies to the current pre-open window only, not a standing instruction.
- **New UNH A/B** — do not enter; confirmed active legal/headline risk requires manual review before any new position.
- **Any crypto short chasing TAO/ZBT/SYN/DEXE at current market** without waiting for the desk's own retest/pullback structure — all C-tier watchlist ideas are explicitly "not active until regime, volume, or confirmation improves" per their own thesis text.
- Scanning, candidate generation, tracking, and outcome recording continue uninterrupted regardless of this window's caution stance.

## 10. Main Risks

- **Geopolitical**: renewed Iran/Strait-of-Hormuz strikes are an active, evolving macro risk (oil, gold, equities reacting more than BTC) — a fresh escalation headline during the US session could move risk sentiment quickly.
- **Legal/headline**: UNH DOJ investigation (confirmed, ongoing); several unmapped stocks-legal-risk headlines today (FSLR, AVAV, VERI, EMBC securities-fraud PR-Newswire items) — none currently map to active candidates but worth a periodic scan.
- **Data reconciliation**: `active-signals` vs. `PAPER_MONITOR_STATUS_LATEST.md` lifecycle-count mismatch persists unresolved (§3, §14) — reduces confidence in any single "how many positions are open" answer this cycle.
- **Squeeze risk**: TAO/USDT short has OI building against price — a BTC/ETH bounce could squeeze it before the retest confirms.
- **Session-transition risk**: several stocks candidates (AAPL, UNH, META, SMH, AMZN, AVGO, GOOGL, QQQ, AMD, COIN, TSLA) are all sitting at C-tier purely due to market-closed demotion — expect a wave of re-scoring at/after the 16:30 EEST open; today's pre-open scores are not a reliable predictor of RTH entries.
- **Playbook health**: crypto scalp mode remains a losing bucket (PF 0.14, n=38) and crypto tier=B triggered winrate is low (13.8%) — both are recurring, previously-flagged patterns (see §14).

## 11. Action Plan — next 4 hours

- Watch TAO/USDT for a clean failed-bounce retest into 198.99–200.09 before treating the existing short as freshly actionable; do not add at current levels.
- Watch VELVET/USDT for a pullback/hold structure before considering a long; do not chase the extended move.
- Monitor NVDA for any technical setup forming around the China-chip-screening story; re-score after the US open.
- At/after 16:30 EEST US cash open: re-check AAPL, UNH, META, SMH, AMZN, AVGO, GOOGL, QQQ, AMD, COIN, TSLA — all currently C-tier purely from the closed-market demotion and may re-qualify for real A/B status on RTH confirmation.
- Do not treat AMZN's carried-forward A-tier signal as a fresh entry; wait for RTH price action to confirm or invalidate (244.38).
- Flag UNH for a human legal-risk sign-off before any new position is considered, and to review whether existing open UNH rows should be tightened.
- JPM has earnings today — no new entries into the print per the pipeline's own `do_not_chase_warning`.

## 12. Final Verdict per Mode

- **Crypto scalp**: NO TRADE — no A/B, and the mode is a known losing bucket (PF 0.14) independent of this cycle.
- **Crypto intraday**: NO TRADE — no A/B; best watchlist names (SXT, NEAR) lack a clean confirmed entry.
- **Crypto swing**: WATCH ONLY — TAO/USDT short remains the single live idea; wait for retest, squeeze risk flagged.
- **Stocks intraday**: WATCH / PLANNING ONLY — market closed; every A/B candidate demoted to C; re-evaluate after 16:30 EEST open.
- **Stocks swing/invest**: EXCLUDED — data ~12 days stale, deprecated legacy mode.
- **Overall desk stance**: CAUTION, routed by side — crypto short-biased with squeeze caution, stocks wait-for-RTH-confirmation. Not a stop-trading signal; scanning/tracking continue.

## 13. Sources

- [BTC price news: What recent U.S.-Iran strikes mean for bitcoin, ether, solana](https://www.coindesk.com/markets/2026/07/13/bitcoin-holds-near-usd63-800-as-war-driven-selloff-hits-everything-but-crypto) — CoinDesk, 2026-07-13
- [Iran Strikes Push Bitcoin Below $63K: Fed Policy Now Matters More Than War](https://www.techtimes.com/articles/320296/20260713/iran-strikes-push-bitcoin-below-63k-fed-policy-now-matters-more-war.htm) — Tech Times, 2026-07-13
- [Nvidia Reportedly Cuts More Than Half of Its Asian AI Chip Customers Amid Tighter China Screening](https://www.benzinga.com/markets/tech/26/07/60433026/nvidia-reportedly-cuts-more-than-half-of-its-asian-ai-chip-customers-amid-tighter-china-screening) — Benzinga, 2026-07-14
- [Nvidia halves Asian AI chip buyer list amid tighter China screening - report](https://seekingalpha.com/news/4613408-nvidia-halves-asian-ai-chip-buyer-list-amid-tighter-china-screening---report) — Seeking Alpha, 2026-07-14
- [UnitedHealth Group under DOJ investigation over Medicare billing practices](https://www.medicaleconomics.com/view/unitedhealth-group-under-doj-investigation-over-medicare-billing-practices) — Medical Economics, 2025-07-24
- [DOJ investigation of UnitedHealth confirmed in SEC filing](https://healthexec.com/topics/healthcare-management/legal-news/doj-investigation-unitedhealth-confirmed-sec-filing) — HealthExec, 2025-07-25
- [Broadcom (AVGO) Stock Price Forecast: Apple's $30B US Chip Deal Confirmed](https://www.tradingkey.com/analysis/stocks/us-stocks/262020906-broadcom-avgo-stock-forecast-july-2026-apple-30b-deal-colorado-tradingkey) — TradingKey, 2026-07-08
- [Amazon (AMZN) Stock Price Forecast: AWS Hit Its Fastest Growth in 15 Quarters](https://www.tradingkey.com/analysis/stocks/us-stocks/262026432-amazon-amzn-stock-forecast-july-2026-aws-28-percent-capex-q2-earnings-tradingkey) — TradingKey, 2026-07-13

CNBC UNH article (2025-07-24) returned HTTP 403 on WebFetch verification — used Medical Economics/HealthExec as the confirmed sources instead.

## 14. Fix Requests / TODO

### TODO-active-signals-lifecycle-reconciliation (carried forward)
- **issue:** `active-signals` reports 71 non-terminal rows (21 crypto B-tier triggered/tp1_hit/tp2_hit + 50 stocks) while `PAPER_MONITOR_STATUS_LATEST.md` shows 0 across OPEN_ACTIVE/WAITING_FOR_ENTRY/REVIEW_ONLY_SHADOW/ENTERED_UNRESOLVED_EXPIRED and 70 under NO_ENTRY_EXPIRED.
- **evidence:** `python -m src.cli active-signals --asset-class crypto/stocks` output vs. `reports/PAPER_MONITOR_STATUS_LATEST.md` lines 8–12; same gap first flagged in `OPUS_ENRICHED_REVIEW_AUTO_2026-07-14_0455.md` §3/§14, still present ~6.7h later.
- **suggested manual fix:** trace why `active-signals` (reads `proposed_signals`/`signal_outcomes` directly) and the paper-monitor lifecycle snapshot (reads a different execution-tracking table/view) disagree — likely a status-mapping or query-scope difference between the two code paths.
- **priority:** high
- **first observed:** 2026-07-14 04:55 EEST (this run: 2026-07-14 11:39 EEST, unresolved)

### TODO-catalyst-mapping-weak
- **issue:** catalyst→symbol mapping is 13.8% (277/2,000) this run, well below the 50% threshold; same order-of-magnitude weakness as the 04:55 review (87.4% unmapped then vs. 86.2% now).
- **evidence:** computed from `data/catalysts/2026-07-14/catalyst_events.jsonl` (2,000 total, 277 with non-null `symbol`).
- **suggested manual fix:** review the symbol resolver in the catalyst layer — many unmapped headlines are macro/geopolitical (expected to stay unmapped) but a meaningful share are stock-legal-risk PR-Newswire items (FSLR, AVAV, VERI, EMBC) that plausibly should resolve to tickers.
- **priority:** medium
- **first observed:** 2026-06 (recurring; reconfirmed 2026-07-14 04:55 and 11:39 EEST)

### TODO-avgo-catalyst-technical-contradiction
- **issue:** AVGO's internal technical/momentum score produced a SHORT signal (raw B-tier, 79.5) the same day external, multi-source-confirmed news (Apple $30B multi-year deal, +143% YoY AI revenue, Strong-Buy consensus) is strongly bullish — a genuine catalyst-vs-technical contradiction that a human wouldn't catch without cross-checking outside the pipeline.
- **evidence:** `data/reports/stocks/intraday/2026-07-14_07-06_stocks_intraday_report.md` §5 (Top Candidates table, AVGO short 79.53) vs. externally verified Apple-deal confirmation (TradingKey, 2026-07-08) and Q2 AI-revenue growth.
- **suggested manual fix:** consider whether large confirmed M&A/partnership catalysts should feed into the `catalyst_news` score component (or at minimum trigger a review flag) for the affected symbol, similar to the existing `legal_headline_risk` gate.
- **priority:** medium
- **first observed:** 2026-07-14 11:39 EEST

### TODO-crypto-tierB-low-winrate-recurring
- **issue:** crypto tier=B triggered winrate is 13.8% (own tool observation, "Consider reviewing entries") and crypto scalp mode PF is 0.14 (losing, n=38) — both are recurring patterns across multiple review cycles, not a one-off.
- **evidence:** `python -m src.cli signal-stats --asset-class crypto` observations panel; consistent with the same figures in the 04:55 EEST review.
- **suggested manual fix:** a dedicated scoring-calibration session should review whether tier=B entry criteria are too permissive given the low triggered-winrate despite a positive PF (asymmetric R-multiples currently compensating for a low hit rate — worth confirming this is intentional, not accidental).
- **priority:** low
- **first observed:** recurring (pre-existing; reconfirmed 2026-07-14 11:39 EEST)
