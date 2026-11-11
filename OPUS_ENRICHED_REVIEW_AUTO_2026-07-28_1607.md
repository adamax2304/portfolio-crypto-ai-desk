# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:07 EEST

## 1. Executive Summary
Advisory only / no auto-trade. **Slot: pre-US-open decision review** (final read before 09:30 ET open). Both crypto and stocks remain **risk-off / short-biased**; there are **zero A/B-tier actionable setups** on either desk this cycle — crypto scalp is kill-switched, crypto intraday/swing have no A/B, and every stocks intraday A/B was demoted to C purely by `market_closed_intraday_planning_only` (plus three carrying independent legal-risk caps). BTC ~$63-65K / ETH ~$1.87-1.97K, Fear&Greed 29 (external-confirmed). Overnight's dominant story is a chip-sector selloff (Kospi −10/11%) that should set the tone for SMH/NVDA/AMD/AVGO at the open. GOOGL and UNH carry **confirmed, fresh legal/DOJ risk** — avoid regardless of score. AMZN's internal "going_concern" cap could **not** be corroborated internally or externally — flagged as a data-integrity TODO, not treated as a real risk. `stocks-preus-candidates` returned 0 eligible / 0 excluded this run (see §5 overlay + §14).

## 2. Data Used
- `data/reports/scalp/2026-07-28_11-53_scalp_report.md` (crypto scalp, kill-switched)
- `data/reports/intraday/2026-07-28_12-01_intraday_report.md` (crypto intraday)
- `data/reports/swing/2026-07-28_01-25_swing_report.md` (crypto swing, carry-forward)
- `data/reports/stocks/intraday/2026-07-28_12-46_stocks_intraday_report.md`
- stocks swing/invest reports last dated 2026-07-02 — **deprecated framework, not used** (per prior project decision; new stocks_swing_growth_breakout framework is shadow-only and out of scope for this advisory review)
- `data/catalysts/2026-07-28/catalyst_events.jsonl` + `narrative_baskets.jsonl`
- `active-signals` (crypto: 18 rows, stocks: 50 rows), `signal-stats` (crypto, stocks)
- `scripts.detect_untracked_legacy_alerts --since 2026-07-28` → clean
- `src.cli stocks-preus-candidates` → 0 eligible / 0 excluded
- Internal `news_items` queries (UNH DOJ probe, GOOGL class action, AMZN legal-flag check)
- 2 WebSearch + 1 WebFetch (Amazon going-concern check; BTC/ETH market mood; chip-selloff corroboration)
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-28_1140.md` (11:40 EEST, Europe/pre-US slot)

## 3. Scheduler / Data Freshness
- **Pre-US schedule check:** target 08:55 ET, actual fire ≈08:59 ET (Δ+4min, within tolerance). Current date 2026-07-28 is outside both documented DST-mismatch windows (2026-03-08→03-29, 2026-10-25→11-01) — standard 7h Nicosia/NY offset holds.
- Scheduler folder: `data/scheduled_runs/2026-07-27_default_schedule/` (rolling folder, still active into 07-28) — `scheduler.log` mtime = now (fresh); latest `cycle_07_11-59_summary.md` mtime ≈3h15m old. Rule requires BOTH stale (>3h) to defer — scheduler.log is fresh, so **no defer**.
- Crypto reports: scalp 14:53 EEST (fresh), intraday 15:01 EEST (fresh), swing 04:25 EEST (**carry-forward**, ~11.5h old, borderline the 12h line — still bearish/risk-off, consistent with fresher reports).
- Stocks intraday: 15:46 EEST (fresh). Stocks swing/invest: 2026-07-02 (>14h stale by a wide margin) — **excluded**, deprecated per project decision, no fresher source needed since new framework replaces it.
- Catalyst layer: `data/catalysts/2026-07-28/` present, latest cycle file 15:04 EEST (fresh).
- Untracked-alert detector: **clean** (no untracked crypto legacy alerts).
- Paper/monitor status: `pending_monitor_restarted.log` actively updating (last write ≈now); `stocks_monitor_*.log` cadence ~2h40m (last 14:45 EEST) — both look alive, no restart/kill needed or attempted.

## 3A. Agent Council JSON
```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-28 16:07 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log fresh", "swing report 11.5h old (carry-forward)", "stocks swing/invest deprecated since 2026-07-02"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["risk_off", "shorts_preferred", "chop"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC downtrend, ETH transition_down, altcoin breadth 17.8%", "stocks regime risk_off bias short, VIX 18.66, breadth_ema20 25%", "external BTC $63.1K/ETH $1.87K Fear&Greed 29 confirms"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "no_catalyst"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["861/2500 catalyst events mapped (34.4%) — mapping weak this run", "Kospi chip-selloff confirmed fresh + external", "rwa_narrative / perps_dex_narrative baskets fresh <24h"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.4,
      "reason_codes": ["squeeze_risk", "data_unavailable"], "data_missing": ["OI 24h% for most top movers", "order book depth / CVD"],
      "suggested_effect": "advisory_only",
      "facts_used": ["COTI/VANRY negative funding across bybit+mexc (crowding elevated)", "several short candidates flagged thin_liquidity_short_squeeze_risk"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["entry_late", "chase_risk", "overextended"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["SNXXB/MUB/SNDKB/SOXLB rejected: >2 ATR from EMA20, do not chase", "XLE stocks short (score 93.44) contradicts XLE being the strongest sector (RS +7.01%) — technical contradiction"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.7,
      "reason_codes": ["no_entry", "entered_unresolved", "review_shadow"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["18 crypto B-tier positions all tp1/tp2_hit (entered-unresolved)", "ADA/USDT B intraday short now stale_before_entry (was waiting_for_entry in 11:40 review)", "50 stocks rows, all C-tier, mostly stale beyond original expiry — display/research only"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: DOJ Medicare-fraud probe confirmed internally (8-K 2026-07-16), earnings today", "GOOGL: fresh (2026-07-27) class-action + prior securities-fraud investigation, stale post-earnings levels", "AMZN: going_concern cap could not be corroborated internally or externally — data-integrity flag"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["low_sample", "playbook_failing", "playbook_working"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto B-tier 7d reliable: WR24.2% PF1.93 total+30.6R", "stocks C-tier 7d reliable: WR2.8% PF0.57 total-3.0R (watchlist quality, not actionable)", "stocks A/B forward_postfreeze 14d n5 +1.0R, 30d n11 -2.5R — small sample"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents; no A/B anywhere; chip-selloff is the cleanest catalyst-backed idea; GOOGL/UNH avoid on confirmed legal risk"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "shorts",
    "best_long_candidate":     { "symbol": "COTI/USDT", "trigger": "confirmed pullback/retest with volume into 0.40-0.42 zone before considering long; do not chase the +60% 24h spike", "reason": "strongest RS-vs-BTC symbol in flow, but momentum-only, no catalyst confirmation, crowding elevated on negative funding" },
    "best_short_candidate":    { "symbol": "SMH / NVDA / AMD (stocks, watch)", "trigger": "wait for RTH — short only on a 15m break of the pre-market low with volume; do not chase the pre-market chip-selloff gap", "reason": "Kospi chip-sector selloff (~-10/11%) confirmed fresh + externally corroborated, aligns with stocks risk-off/short regime" },
    "best_catalyst_candidate": { "symbol": "SMH / NVDA / AMD (chip selloff)", "trigger": "same as above — RTH confirmation required, legal/earnings clear for NVDA/AMD/SMH", "reason": "cleanest fresh, externally-verified catalyst this cycle" },
    "avoid_candidate":         { "symbol": "GOOGL / UNH", "reason": "GOOGL: fresh 2026-07-27 class-action + stale post-earnings setup; UNH: confirmed DOJ Medicare-fraud probe + earnings today — both manual-review-only, never actionable regardless of score" },
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
| market_regime | caution | 0.75 | risk_off, shorts_preferred, chop | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, fresh_catalyst, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.40 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.50 | entry_late, chase_risk, overextended | advisory_only |
| execution_lifecycle | ok | 0.70 | no_entry, entered_unresolved, review_shadow | advisory_only |
| risk_manager | caution | 0.65 | legal_risk, headline_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.60 | low_sample, playbook_failing, playbook_working | advisory_only |
| head_trader | caution | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (11:40 EEST)
- **Crypto mood:** unchanged, risk-off. **Stocks mood:** was "pre-market/mixed", now **risk_off/bias-short outright** (VIX 18.66, breadth_ema20 25%) — sharpened, not reversed.
- **ADA/USDT (crypto, B intraday short):** was `waiting_for_entry` in the 11:40 review → now **`stale_before_entry`** — invalidated/expired without a fill. No longer a live short-watch idea.
- **COTI/USDT:** unchanged best-long-watch idea; still no pullback/retest confirmation, still the top "Where Money Is Flowing" symbol (+59.9% 24h).
- **SMH/NVDA/AMD chip-selloff:** carried forward and **strengthened** — Kospi crash now explicitly externally corroborated (Bloomberg/WaPo) in addition to the internal Telegram catalyst; still pre-market only, still needs RTH confirmation.
- **GOOGL/UNH avoid:** unchanged, confirmed legal risk persists.
- **New this cycle:** AMZN "going_concern" legal-headline cap appears in the stocks report for the first time reviewed here — investigated and found **unsupported** (see §14).
- **New this cycle:** `stocks-preus-candidates` (the pre-US overlay tool) returned 0/0 — no session-cap-only stocks C's were eligible for scoring this run (see §5, §14).

## 5. Catalyst Coverage
- Total catalyst events today: **2500**. Mapped (non-null symbol): **861 (34.4%)**. Unmapped: **1639 (65.6%)**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (unmapped 65.6% > 50% threshold)
  - Top unmapped headlines: "DataStrike Expands Snowflake Managed Services..." (PR Newswire (Stocks)); "Beazley Security and Halcyon Launch Cyber Resilience Retainer..." (PR Newswire (Stocks)); Reza Pahlavi commentary (t.me/ClashReport, geopolitical, not ticker-mappable).
- `narrative_baskets` today: **3** rows / 2 active baskets — `rwa_narrative` (primary ONDO/USDT, XLM/USDT, fresh <6h) and `perps_dex_narrative` (primary HYPE/USDT, fresh <24h).

### Pre-US Stocks Review Overlay
- candidates reviewed: **0** (SUPPORT 0 / NEUTRAL 0 / CAUTION 0 / BLOCK 0 / INSUFFICIENT_DATA 0)
- session-cap-only C's now eligible for pre-open Paper lane: **0**
- excluded by hard gate: **0 listed** — `stocks-preus-candidates` returned `eligible=0, excluded=0` outright (no `proposed_signals` rows matched the query's mode='intraday'/status-in/funnel_state criteria), even though the stocks-intraday report shows 15 C-tier names capped only by `market_closed_intraday_planning_only`. This looks like the underlying candidates were never persisted as `proposed_signals` rows in a status the overlay query recognizes, not that they were individually excluded. Flagged as TODO-preus-empty in §14 rather than guessed at further.

## 6. Market Landscape
Crypto: BTC downtrend, ETH transition_down, altcoin breadth above EMA20 only 17.8%. Macro/geopolitics risk score 85.2/100 (Aramco refinery shutdown after Houthi attack, Zelensky/Russia-sanctions lobbying, Fed press conference this week) — risk-off headwind. Stocks: 0/4 major indices trending up, breadth above EMA20 only 25%, VIX 18.66; energy/financials the only strong sectors, semis/tech/discretionary weak; a Kospi chip-sector crash (~-10/11%) overnight is the dominant pre-open story, hitting NVDA/AMD/SMH/AVGO/QQQ pre-market.

### Market Mood / Risk Routing
- Crypto mood: **risk-off**
- Stocks mood: **risk-off / pre-market** (closed, but regime label itself is now risk_off, not just "mixed")
- Dominant narrative: **chip-sector selloff (Kospi crash) bleeding into US semis pre-market**; secondary: energy/financials relative strength vs weak tech/semis
- Preferred side now: **shorts** (both desks), with crypto secondarily open to a confirmed RS-leader long (COTI) only after a clean retest
- Best long candidate: none clean — see best-long-watch (COTI/USDT) in §8
- Best short candidate: none clean pre-open — see best-short-watch (SMH/NVDA/AMD) in §8
- Best catalyst-backed candidate: SMH/NVDA/AMD chip-selloff (externally confirmed)
- What to avoid: GOOGL, UNH (confirmed legal/DOJ risk); chasing COTI/ZAMA/VANRY (crowded, extended); chasing the chip-selloff gap without RTH confirmation
- What would change the view: BTC reclaiming local downtrend structure; chip-selloff stabilizing at the US open (SMH holding pre-market low); a clean COTI pullback with rising volume

## 7. Candidate Deep Dives

### 7.1 XLE (stocks, short, score 93.44 raw-A → C by market-closed gate) — CAUTION / technical contradiction
- Has price already reacted to the catalyst? XLE is the **strongest** sector this cycle (RS vs SPY 20d +7.01%, 20d return +8.40%) — the "top candidate" table nonetheless lists it as a **short**. That is a direct contradiction between §2 (sector rotation: energy strong) and §5 (top candidate: short XLE).
- Is the setup chasing? Unclear without the underlying deep-dive card (this report cycle's format only exposes scores/tiers, not full thesis text for stocks).
- Retest/pullback structure? Not verifiable from available fields.
- Overextended >2 ATR from EMA20? Not stated for this symbol in the available table.
- Aligned with market mood? No — shorting the sector showing the most RS strength while the broader stocks regime is risk_off/short-biased is an internal inconsistency, not a mood-aligned idea.
- Actionable now or later? Neither — market closed (gate), and the contradiction itself demotes this to **manual review**, not just a session-cap wait.
- What would invalidate/confirm: needs the full technical thesis (is this a mean-reversion fade after an extended energy rally, or a scoring/labeling issue) before it can be trusted even after the open.
- Verdict: **CAUTION / needs manual review** — do not treat the raw A-tier score as trustworthy until the sector-vs-direction conflict is resolved by a human.

### 7.2 UNH (stocks, short, score 86.73, capped: legal_headline_risk sec_doj) — AVOID
- Catalyst: DOJ civil/criminal fraud investigation into Medicare billing practices — confirmed via internal `news_items` (QuiverQuant, CBS News, Medical Economics, SEC 8-K filed 2026-07-16). Fresh enough (12 days old, ongoing) to still matter; earnings also **today** (2026-07-28).
- Price reaction: report notes "shares dive 16%" language attached to the original probe headline (older reporting, not this morning's move specifically).
- Legal/headline risk: **confirmed, primary source**. Combined with earnings-today chase risk.
- Verdict: **AVOID** — never actionable regardless of score; this is a textbook legal+earnings stack, not a tradeable short or long today.

### 7.3 GOOGL (stocks, short, score 86.68, capped: legal_headline_risk class_action/securities_fraud + stale_post_earnings_setup) — AVOID / MANUAL REVIEW
- Catalyst: fresh (2026-07-27, 1 day old) "Pending Class Action Lawsuit Involving the Purchase and/or Acquisition of Alphabet Inc." (PR Newswire), plus earlier 2026-07-16/07-21 securities-fraud-investigation announcements (GlobeNewswire/BusinessWire) — **confirmed, primary source, genuinely fresh**.
- Also flagged `stale_post_earnings_setup`: GOOGL reported earnings 2026-07-27T10:45 UTC while the earnings calendar itself shows UNKNOWN — pre-earnings levels are invalid.
- Is this chasing? By definition yes — any short built on pre-earnings levels the day after a print is chasing stale structure.
- Verdict: **AVOID / MANUAL REVIEW REQUIRED** — two independent disqualifiers (fresh legal risk + stale post-earnings levels) stack here; do not treat as actionable even after RTH confirmation until fresh levels are built.

### 7.4 AMZN (stocks, short, score 86.99, capped: legal_headline_risk going_concern) — MANUAL REVIEW (data-integrity flag, not a real risk as far as verified)
- Checked internal `news_items` for AMZN + {SEC, DOJ, fraud, investigation, lawsuit, class action, going concern, auditor} in the last 30h and broader history — found labor-poaching lawsuit (Warner Bros, 2026-07-25), routine SEC EDGAR filings (8-K/424B5/Form 4), AI-strategy news — **nothing resembling a going-concern / auditor doubt**.
- Ran external WebSearch ("Amazon AMZN going concern auditor warning 2026") — no result corroborates a going-concern flag; a mega-cap with $200B 2026 capex plans is not a going-concern profile.
- Verdict: **the `going_concern` cap on AMZN looks like a mislabeled/false-positive legal-risk tag**, not a real risk. Treating as **manual review** rather than a hard avoid — the underlying short idea itself is untested (2 ATR/chase-risk unknown from available fields), but the stated reason for its cap should not be trusted as-is. See §14 TODO.

### 7.5 COTI/USDT (crypto, long, C-tier watchlist, score 91.6, +59.9% 24h) — WATCH ONLY
- Strongest RS-vs-BTC symbol in flow (+62.4%), but momentum-only: no fresh verified catalyst, negative funding across bybit+mexc ("crowding elevated") — a squeeze/positioning risk on further upside, not a clean trend continuation.
- Is this chasing? Yes at current price after a +60% day; would need a genuine pullback/retest with rising volume, not a fresh high.
- Verdict: **WATCH ONLY** — same conclusion as the 04:45 and 11:40 reviews; nothing has changed enough to promote it.

## 8. Best Candidates Ranked
No A/B-tier clean actionable candidate exists on either desk this cycle. Ranked watch-list:
1. **Best short-watch / best catalyst-watch (stocks, pre-open): SMH / NVDA / AMD chip-selloff** — Kospi -10/11% overnight, externally corroborated (Bloomberg/WaPo) in addition to internal Telegram catalyst. Trigger: wait for the 09:30 ET open, then a 15m break of the pre-market low with volume before shorting; do not chase the pre-market gap. Invalidated if SMH/NVDA reclaim their pre-market lows within the first 15-30 minutes.
2. **Best long-watch (crypto): COTI/USDT** — trigger: a confirmed pullback/retest into the 0.40-0.42 zone with rising volume; invalidated by a fresh high without volume confirmation (chase risk) or by funding staying negative/crowded.
3. **Third watch (stocks, avoid-turned-context): energy/financials (XLE/JPM) relative strength** — the one pocket of stocks-side strength; not independently actionable given XLE's contradictory short/strong-sector signal (§7.1) — needs a human look before use either direction.

## 9. Avoid / No Trade
This decision window only — never a command to stop the system, scanning/tracking continues in all cases.
- **UNH** — confirmed DOJ Medicare-fraud probe + earnings today. AVOID.
- **GOOGL** — fresh class-action + stale post-earnings levels. AVOID / MANUAL REVIEW.
- **XLE short** — contradicts the sector's own RS-strength read; do not trust the raw score until reconciled. MANUAL REVIEW.
- Chasing COTI/ZAMA/VANRY/REZ at current extension — crowded, negative funding, counter-tape longs.
- Chasing the pre-market chip-selloff gap in SMH/NVDA/AMD before RTH confirmation.

## 10. Main Risks
- FOMC/Fed decision this week (external + internal macro flag) — expect volatility around the announcement, size down into it.
- Chip-sector selloff (Kospi) could either extend into US cash hours or mean-revert on the open — no RTH confirmation yet.
- Catalyst mapping is weak this run (34.4%) — treat the catalyst layer as context only, not as a standalone trade trigger today.
- `stocks-preus-candidates` overlay returned empty (0/0) — the newer pre-open scoring path is not currently surfacing any of today's session-cap-only names; until a human confirms this is expected, don't assume the overlay is silently vetting things correctly.
- ETH exploit_hack risk flagged (5,280 ETH drained to a single address, Triple-A wallet breach) — operator-review warning, not a trading signal but worth tracking for contagion.

## 11. Action Plan — next 4 hours
- Watch SMH/NVDA/AMD/AVGO at the 09:30 ET open for a clean break of pre-market lows before considering any short; do not act on pre-market prints alone.
- Watch COTI/USDT for a genuine pullback/retest; do not chase the existing spike.
- Do not touch GOOGL or UNH in either direction today.
- Treat XLE (and by extension energy-sector shorts) as needing a human sanity check before use.
- No crypto scalp/intraday/swing A/B exists to act on; continue monitoring, no action required.

## 12. Final Verdict per Mode
- **Crypto scalp:** kill-switched (mode off) — no action.
- **Crypto intraday:** no A/B; watch-only (COTI long-watch, ZEC/NIL/RE short-watch per report, all sub-threshold).
- **Crypto swing:** carry-forward, no A/B, same risk-off read.
- **Stocks intraday:** market closed, 0 actionable A/B; 15 C-tier watchlist names capped only by market-closed gate (session-cap-only), 3 capped additionally by confirmed/flagged legal risk (UNH, GOOGL) or unverified legal risk (AMZN).
- **Stocks swing/invest:** deprecated framework, not evaluated this cycle.
- **Overall desk stance:** WATCH / CAUTION. No new positions recommended pre-open beyond the two watch triggers above.

## 13. Sources
- [UnitedHealth (UNH) Faces DOJ Probe, Shares Dive 16% on Fraud Investigation](internal:news_items) — QuiverQuant/CBS News/Medical Economics, 2026-07-16 (SEC 8-K same date)
- [Pending Class Action Lawsuit Involving the Purchase and/or Acquisition of Alphabet Inc. Class A and/or Class C Shares](internal:news_items) — PR Newswire (Stocks), 2026-07-27
- [Amazon Has Fallen 13% From Its High. Is 2026 the Turning Point?](https://www.tikr.com/blog/amazon-has-fallen-13-from-its-high-is-2026-the-turning-point) — TIKR.com, 2026-07-28 (general AMZN context; no going-concern corroboration found)
- [Crypto News Today 28 July: BTC, ETH, SHIB, KAITO and Top 15 Headlines](https://www.coingabbar.com/en/crypto-currency-news/crypto-news-today-bitcoin-eth-shib-kaito-price-28-july-2026) — CoinGabbar, 2026-07-28
- Internal: `data/reports/stocks/intraday/2026-07-28_12-46_stocks_intraday_report.md` (Kospi chip-selloff internal catalyst notes, t.me/WalterBloomberg)
- Chip-selloff external corroboration found via WebSearch result titles (Bloomberg "Japanese, Korean Stocks Tumble as Chip Selloff Intensifies", Washington Post "Asian shares slip and South Korea's Kospi index sinks nearly 11%...") — same headlines already present verbatim in the internal stocks-intraday report's News/Catalysts section (§4, SMH/QQQ/XLK rows), confirming internal and external agree; not independently re-fetched as they were already internal.

## 14. Fix Requests / TODO

### TODO-amzn-going-concern-unsupported
- **issue:** AMZN's stocks-intraday candidate carries a `legal_headline_risk: going_concern` cap this cycle. Neither internal `news_items` (30h and broader history) nor external WebSearch turns up any auditor/going-concern doubt for Amazon.
- **evidence:** SQL query against `news_items` for AMZN + {SEC, DOJ, fraud, investigation, lawsuit, class action, going concern, auditor} — only unrelated hits (Warner Bros poaching lawsuit, routine SEC filings). WebSearch "Amazon AMZN going concern auditor warning 2026" — no corroborating result.
- **suggested manual fix:** audit the legal_headline_risk detector's source/keyword match that produced the `going_concern` tag for AMZN this cycle — likely a mislabel or a stale/misattributed news_item.
- **priority:** medium
- **first observed:** 2026-07-28 16:07 EEST

### TODO-preus-empty
- **issue:** `python -m src.cli stocks-preus-candidates` returned `eligible=0, excluded=0` this run, even though the stocks-intraday report lists 15 C-tier names capped only by `market_closed_intraday_planning_only` (the exact case this overlay is meant to surface for pre-open scoring).
- **evidence:** CLI stdout `eligible=0 excluded=0 -> reports\STOCKS_PREUS_REVIEW_CANDIDATES.md`; generated JSON shows both lists empty.
- **suggested manual fix:** check whether today's demoted stocks-intraday candidates were ever persisted as `proposed_signals` rows with `mode='intraday'` and `status` in `('generated','waiting_for_entry','triggered')` — if the report renders them without writing a row, the overlay's SQL query will always return empty for market-closed-only demotions, defeating its purpose.
- **priority:** high
- **first observed:** 2026-07-28 16:07 EEST

### TODO-xle-short-vs-sector-strength
- **issue:** Stocks-intraday top-candidates table lists XLE as a short (score 93.44, highest raw score this cycle) while the same report's sector-rotation section (§2) lists energy/XLE as the single strongest sector (RS vs SPY 20d +7.01%, 20d return +8.40%). No thesis text is exposed in this report format to explain whether this is an intentional mean-reversion fade or a scoring inconsistency.
- **evidence:** `data/reports/stocks/intraday/2026-07-28_12-46_stocks_intraday_report.md` §2 (Strongest Sectors: energy XLE) vs §5 (Top Candidates: XLE short, score 93.44).
- **suggested manual fix:** review whether the stocks scoring pipeline exposes (or should expose) a short thesis-text field per candidate the way crypto trade-idea cards do, so contradictions like this are auditable without cross-referencing sections manually.
- **priority:** low
- **first observed:** 2026-07-28 16:07 EEST

### Source-discipline checklist
- Every external claim above has source + title + date + URL. ✓
- No uncited stats, no uncited legal claims. ✓
- No fabricated TradingView/chart observations — TradingView/manual chart check unavailable this run; only local OHLCV/ATR/EMA fields used. ✓
- Missing source → wrote "no result found" rather than guessing (AMZN going-concern check). ✓
- No `test_source`/fixture URLs ingested. ✓
- §13 Sources section present. ✓
- External web research **was** available this run (2 WebSearch, 1 WebFetch succeeded; 1 WebFetch to calebandbrown.com returned HTTP 403 and was abandoned in favor of an alternate source).
