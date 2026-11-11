# Opus Enriched Review — Late-Session Risk Review — Auto Cycle 21:39 EEST

## 1. Executive Summary

Advisory only / no auto-trade. **Late-session risk review** (~5h10m after the 16:30 EEST / 09:30 ET cash open, US session into its final stretch). Crypto regime remains **transition/mixed** (BTC/ETH both uptrend on trend labels, altcoin breadth only 37.5%/42.5% above EMA20/50) with the macro/geopolitical risk score still elevated (66.7-73.5/100 across today's reports) on the Iran/Strait-of-Hormuz conflict — confirmed live via external search: BTC held **$62,000-63,100** through repeated US airstrikes and an Iranian closure declaration, showing resilience but not strength. Stocks closed the session **green despite the geopolitical overhang**: S&P 500 +0.4%, Nasdaq +1% on cooler-than-expected June CPI, Dow roughly flat (external search confirms) — but the desk's own gates still show **zero actionable A/B stocks setups** this cycle (all raw A/B candidates demoted to C on `liquidity_rvol_below_min` + `catalyst_none_and_not_exceptional_technical`). On crypto, the two open managed positions from prior cycles remain the story: **TAO/USDT short** is close to its TP2 (196.05) — external price check shows TAO at **$197.19**, now flagged inside an "ai_narrative" defensive-rotation basket (AI tokens being sold ahead of the CPI print), reinforcing the short thesis. **SYN/USDT long** remains open, unconfirmed by any catalyst. **SXT/USDT** intraday entry zone (0.008652-0.008948) remains breached — do not chase. The **HEI/USDT untracked Telegram alert** (sent 14:54 UTC) is still unresolved days-old data-integrity gap, unchanged from the last two cycles — flagged again in §14, not a new issue. UNH's DOJ/Medicare legal risk remains **AVOID/MANUAL REVIEW** for existing exposure (confirmed again via internal `news_items`, no new development). Catalyst mapping is weak this run (82.7% unmapped) — use as context only. Scanning, tracking, and the paper book continue uninterrupted in all moods.

## 2. Data Used

- Crypto reports: scalp (19:18 EEST gen, freshness 16:15 UTC), intraday (19:24 EEST gen, freshness 16:15 UTC), swing (02:15 EEST gen, freshness 02:00 UTC — **carry-forward, ~19h24m old at time of this review, stale (>14h) per freshness rule, excluded from fresh swing verdicts, no fresher source exists**)
- Stocks reports: intraday (21:37 EEST gen, regular session, freshness 18:36 UTC — fresh)
- Stocks swing/invest reports: last dated **2026-07-02** — stale (~12 days), excluded; position-framework for stocks swing/invest is deprecated per prior desk decision, no fresher source exists, not a new issue
- `data/catalysts/2026-07-14/catalyst_events.jsonl` (3,999 events today, up from 3,499 last cycle), `narrative_baskets.jsonl` (3 baskets this latest cycle: `perps_dex_narrative`, `ai_narrative`, `delisting_thin_liquidity`)
- `data/catalysts/2026-07-14/catalyst_cycle_16-25.md` (latest catalyst cycle, 19:25 EEST)
- `data/processed/llm_analysis_packet.md` (mtime 19:24), `data/processed/llm_stocks_packet.md` (mtime 19:37)
- CLI: `active-signals --asset-class crypto` (21 rows), `active-signals --asset-class stocks` (50 rows), `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`, `detect_untracked_legacy_alerts --since 2026-07-14` (**1 untracked found: HEI/USDT, same as prior cycle**)
- Direct Python/sqlite3 query against `news_items` for 24h freshness on TAO, SYN, SXT, HEI, UNH, JPM (sqlite3 CLI unavailable in this environment; used Python's `sqlite3` module against `db/crypto_ai_desk.sqlite`)
- Direct Python scan of `catalyst_events.jsonl` for mapped/unmapped symbol coverage (82.7% unmapped, 3,999 events)
- External: WebSearch ×3 (Bitcoin/Iran/Hormuz market reaction, US stock market close today, Bittensor/TAO price news) — all resolved successfully, no WebFetch needed since search summaries were sufficient and internally consistent
- Compared against previous review `OPUS_ENRICHED_REVIEW_AUTO_2026-07-14_1839.md` (US open reaction review, ~2h50m prior)

## 3. Scheduler / Data Freshness

- `data/scheduled_runs/2026-07-14_default_schedule/scheduler.log` mtime 19:41 EEST (~2h ago) — fresh, well under the 3h defer threshold
- Latest cycle summary `cycle_01_19-11_summary.md` mtime 19:41 EEST — fresh
- `pending_monitor_1784047111.log` updated 21:39 EEST (live, currently running)
- `stocks_monitor_1784047112.log` updated 21:39 EEST (live, currently running); `stocks_monitor.pid` refreshed 19:38 EEST
- No deferral triggered — both freshness checks pass comfortably

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-07-14 21:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["stocks swing/invest fresh data (last 2026-07-02, deprecated per prior decision)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 19:41 EEST", "crypto swing report mtime 05:15 EEST (~19h old)", "stocks intraday report mtime 21:37 EEST (fresh)"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["mixed", "chop", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto regime label transition/mixed, altcoin breadth 37.5%/42.5%", "stocks regime risk_on, VIX 16.36, breadth 75%/100%", "BTC held $62,000-63,100 through Iran strikes per external search", "US indices closed green (SPY +0.4%, Nasdaq +1%) per external search"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["mapping_weak", "stale_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["82.7% of 3,999 catalyst_events unmapped this run", "ai_narrative basket now includes TAO/RENDER/FET/NEAR — defensive rotation confirmed via external search", "UNH DOJ legal risk confirmed fresh in news_items (2026-07-14)"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.4,
      "reason_codes": ["data_unavailable", "oi_supports"],
      "data_missing": ["bybit/OKX cross-check missing for TAO/USDT and SYN/USDT specifically"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scalp/intraday reports show OI data only for the top-8 strongest symbols, not TAO/SYN directly", "external search: TAO OI showing traders closing positions rather than opening (RSI ~31)"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["entry_late", "price_moved_away", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["SXT/USDT intraday entry zone 0.008652-0.008948 vs desk-noted current price ~0.0095 (breached, do not chase)", "TAO/USDT short at 197.19 approaching TP2 196.05, EMA stack 206-219 above price, bearish tilt confirmed externally"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.8,
      "reason_codes": ["open_actionable", "waiting_for_entry", "no_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals: 21 total, 19 tp1/tp2_hit (open actionable, managing), 1 triggered (SYN, open actionable), 1 waiting_for_entry (SXT)", "stocks active-signals: 50 total, all C-tier (review/shadow, not actionable) except 2 historical B-tier already resolved (XOM, NVDA tp2_hit)"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["correlation_cluster", "legal_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["18 of 21 active crypto signals are swing longs in altcoins against an elevated macro-risk backdrop", "UNH DOJ probe scope confirmed still open (Optum Rx, physician reimbursement)", "HEI/USDT untracked alert persists 3rd cycle running"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto signal-stats: tier=B triggered winrate 15% low; weekend signals underperform (24% WR, n=50)", "stocks signal-stats: tier=C triggered winrate 12% low, PF 0.73 below 0.8", "scalp mode PF 0.14, 0 wins/8 losses (already data-collection-only by design)"]
    },
    {
      "agent": "head_trader",
      "verdict": "ok",
      "confidence": 0.75,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.7,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": { "symbol": "none new", "trigger": "SXT/USDT retest into 0.008652-0.008948 with volume pickup", "reason": "existing zone already breached; no fresh long clears the desk threshold this cycle" },
    "best_short_candidate": { "symbol": "TAO/USDT", "trigger": "hold below TP2 196.05, invalidate above 201.44", "reason": "existing managed short approaching TP2; ai_narrative defensive-rotation basket and RSI ~31 both externally confirm continuation" },
    "best_catalyst_candidate": { "symbol": "XLF / financials", "trigger": "confirmed hold of post-earnings JPM/GS strength with volume, not headline alone", "reason": "financials sector strongest today (RS +3.85% vs SPY) but JPM/XLF both gate-demoted to C — not yet actionable" },
    "avoid_candidate": { "symbol": "UNH", "reason": "active DOJ/Medicare legal-risk investigation confirmed again in internal news_items; existing exposure needs manual review, no new entries" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 1
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.70 | mixed, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, stale_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.40 | data_unavailable, oi_supports | advisory_only |
| technical_entry | caution | 0.65 | entry_late, price_moved_away, clean_retest | advisory_only |
| execution_lifecycle | ok | 0.80 | open_actionable, waiting_for_entry, no_entry | advisory_only |
| risk_manager | caution | 0.70 | correlation_cluster, legal_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.75 | playbook_failing, low_sample | advisory_only |
| head_trader | ok | 0.75 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

vs `OPUS_ENRICHED_REVIEW_AUTO_2026-07-14_1839.md` (US open reaction, ~2h50m ago):

- **CRV/USDT untracked alert resolved itself** — only HEI/USDT remains untracked this cycle (was 2, now 1). No root-cause action taken by this run (forbidden); noting the partial self-resolution in §14.
- **Macro risk score eased slightly**: 66.7-73.5/100 this run vs 83.2/100 at the peak of the last cycle — still elevated/risk-off but off the intracycle high. Consistent with external confirmation that Trump abandoned the 20% Hormuz transit fee, taking oil off its highs.
- **US stocks closed green** (S&P +0.4%, Nasdaq +1%) despite the geopolitical overhang — the risk-on stocks regime label held through the close.
- **TAO/USDT short thesis strengthened**: newly labeled inside the `ai_narrative` basket this cycle (AI-token defensive rotation), external search independently confirms RSI ~31 and OI unwinding — no reason to change the existing management plan.
- **SYN/USDT and SXT/USDT unchanged** — same open/breached-zone status as last cycle, no new catalyst either way.
- **UNH legal risk unchanged** — still open DOJ probe, no new headline since last cycle's confirmation.
- Previous review's JPM/financials catalyst-watch idea carries forward unresolved: still gate-demoted to C.

## 5. Catalyst Coverage

- Total `catalyst_events` today: **3,999** (up from 3,499 at the 18:39 cycle)
- Mapped (non-null symbol): **692** (17.3%)
- Unmapped (null symbol): **3,307** (82.7%)
- `narrative_baskets`: **3** active this latest cycle (`perps_dex_narrative`, `ai_narrative`, `delisting_thin_liquidity`)
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (unmapped > 50%, consistent with the 83.7% figure from the prior cycle — this is a recurring, already-tracked condition, not a new regression)
- Top 3 unmapped headlines (sample): "MEHR SAYS SEVERAL AREAS IN SOUTHWESTERN IRAN'S KHUZESTAN'S OMIDIYEH HIT BY U.S. PROJECTILES" (@WalterBloomberg); "EMBC Investors Have Opportunity to Lead Embecta Corp. Securities Fraud Lawsuit"; "Serve Robotics: A Risky Bet or a Future Winner?"

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **mixed / chop** — BTC/ETH trend labels both uptrend but altcoin breadth weak (37.5%/42.5% above EMA20/50), macro risk score elevated (66.7-73.5/100) on live Iran/Hormuz tensions
- Stocks mood: **risk-on** (closed session) — VIX 16.36, breadth 75%/100%, S&P +0.4%/Nasdaq +1% on cool CPI; desk's own actionability gates still show 0 A/B stocks setups
- Dominant narrative: AI-token defensive rotation (TAO/RENDER/FET/NEAR basket) ahead of the CPI print; financials strength (JPM/GS earnings beats) unconfirmed for fresh entries; Iran/Strait-of-Hormuz geopolitical overhang still live, not resolved
- Preferred side now: **wait-for-trigger**, with a bias toward managing the existing TAO short and avoiding fresh alt longs into a weak-breadth, macro-risk-off tape
- Best long candidate: none fresh — SXT/USDT only on a retest into 0.008652-0.008948
- Best short candidate: TAO/USDT (existing, managing toward TP2 196.05 / TP3 191.15)
- Best catalyst-backed candidate: XLF/financials on confirmed post-earnings hold (not yet actionable — still gate-demoted)
- What to avoid: chasing SXT/USDT above its breached zone; any new UNH exposure; any AI-token long into the current defensive-rotation basket
- What would change the view: BTC reclaiming and holding above local resistance with breadth expansion above EMA20/50; Iran/Hormuz de-escalation headline; TAO breaking back above its EMA stack (206-219)

## 7. Candidate Deep Dives

### 1. TAO/USDT — existing swing short, managing toward TP2 (highest priority — active position near target)
- Status: **OPEN actionable** — tp1_hit already, entry 198.99-200.09, invalidation 201.44, TP2 196.05, TP3 191.15
- Has price already reacted to the catalyst? Yes — TAO down ~2.3-3.6% over 24h per external search, now at $197.19, just above TP2
- Chasing? No — this is an existing, already-profitable managed position, not a fresh entry
- Retest/pullback structure? N/A for management; a fresh short entry would need a failed-bounce retest into 198.99-200.09
- Overextended? No — RSI ~31 (oversold-adjacent, not extreme), EMA stack 206-219 sits above price, bearish tilt intact
- Late entry risk: N/A (managing, not entering)
- Aligned with market mood? Yes — fits the defensive AI-token rotation and macro risk-off backdrop
- Long, short, or wait-for-trigger? Short (existing)
- Actionable now or after confirmation? Already actionable/open; fresh adds require the retest trigger above
- Invalidation: 1h close/reclaim above 201.44
- Chase-risk setup? No
- Catalyst confirmation/contradiction? Confirmed — `ai_narrative` basket (fresh <6h) plus external OI/RSI data align with continued weakness

### 2. SYN/USDT — existing intraday long, open/unresolved (no catalyst backing)
- Status: **OPEN actionable (unresolved)** — triggered 0.260537-0.269698, stop 0.249341, expires 2026-07-15T14:46
- Has price reacted to a catalyst? No fresh catalyst found in `news_items` (0 rows in 24h) or `catalyst_events.jsonl` for SYN
- Chasing? No — already entered at the stated zone; do not add without a hold-above confirmation
- Retest/pullback structure? N/A, managing existing position only
- Overextended? Cannot confirm without a fresh chart read; treat conservatively given no-catalyst status
- Aligned with market mood? Partially — long in a mixed/chop tape with weak altcoin breadth is higher risk than usual
- Long/short/wait? Long (existing, managed small)
- Invalidation: stop 0.249341
- Chase-risk? No (existing position)
- Catalyst confirmation/contradiction? Neither — genuinely no-catalyst, matches the playbook's own known-failure-mode note ("No-catalyst intraday in chop is net-negative")

### 3. SXT/USDT — intraday B-tier, entry zone breached (no-chase watch)
- Status: **WAITING for entry**, but current desk-noted price (~0.0095) sits above the stated entry zone (0.008652-0.008948) — effectively a **NO-ENTRY / STALE** condition at current price, not a live opportunity
- Has price already reacted? Yes — SXT is up 21%+ over 24h per the intraday report, well past any clean entry
- Chasing? Yes, if entered now — explicitly a no-chase setup
- Retest/pullback structure? Needed: a pullback with volume back into 0.008652-0.008948 (or the report's separate C-tier conditional pullback zone 0.0090-0.0093) before this becomes tradeable
- Overextended? Yes — RS vs BTC +17.5%, but volume ratio only 0.04x (move not backed by strong current volume)
- Actionable now? No — wait for the retest
- What would invalidate: 1h close beyond 0.0087 (per the C-tier conditional read)
- Chase-risk setup? Yes, explicitly
- Catalyst confirmation? None found in `news_items` last 24h

### 4. UNH — stocks, legal/headline risk (avoid / manual review, existing exposure only)
- Status: **NEEDS REVIEW** — C-tier via `legal_headline_risk: sec_doj` gate demotion; no new A/B entries possible while the gate is active
- Legal/headline check: confirmed independently in `news_items` — DOJ criminal probe extends to Optum Rx and physician reimbursement (FierceHealthcare, 2026-07-14); UnitedHealth stock sank 4.7% on DOJ Medicare-billing confirmation (Yahoo Finance, 2026-07-14) — same facts as last cycle, no new development
- Verdict for this candidate: **AVOID / MANUAL REVIEW REQUIRED** for existing exposure — never a clean actionable while this flag is live
- What would change the view: DOJ probe resolution or a company statement materially narrowing scope (neither observed)

### 5. HEI/USDT — untracked Telegram alert (system-integrity watch, not a trade candidate)
- Status: **NEEDS REVIEW** — B-tier intraday alert sent 2026-07-14T14:54:37Z with no matching `proposed_signal`, so it carries no entry/stop/TP and will not contribute to PF/winrate tracking
- This is the same alert flagged in the last two review cycles (unresolved, not worsening — CRV/USDT's matching gap from the 18:39 cycle appears to have self-resolved, HEI/USDT has not)
- Do not act on the raw Telegram alert as if it were a tracked signal — no risk parameters exist for it
- Root cause is an operator-session task, not something this run can or should fix (see §14)

## 8. Best Candidates Ranked

1. **TAO/USDT — best short (existing, managing toward TP2).** Current 197.19 vs TP2 196.05 — very close. Fresh-entry trigger for anyone not already in: a new 1h failed-bounce retest into 198.99-200.09, invalidate above 201.44. Externally reconfirmed via AI-token defensive-rotation narrative and oversold-adjacent RSI.
2. **SYN/USDT — best long (existing, monitor only).** No catalyst backing; manage small per the playbook's own known-failure-mode warning, do not add without a hold-above-trigger confirmation.
3. **XLF / financials — best catalyst-watch (not yet actionable).** Strongest sector today (RS +3.85% vs SPY) on JPM/GS earnings beats, but every related name (JPM, XLF) remains gate-demoted to C. Trigger: a confirmed hold of today's gains with volume tomorrow, not the headline alone.
4. **UNH — avoid / manual review** for existing exposure; DOJ probe scope confirmed still open, unchanged from last cycle.
5. **SXT/USDT — no-chase watch.** Do not enter at current levels (~0.0095, above the 0.008652-0.008948 zone); wait for a retest with volume.
6. **HEI/USDT — system-integrity watch, not a trade candidate.** Do not act on the raw Telegram alert; no tracked entry/stop/TP exists for it.

## 9. Avoid / No Trade (this decision window only)

- **Chasing SXT/USDT** above its breached entry zone — wait for a retest.
- **Acting on the HEI/USDT Telegram alert** as if it were a tracked signal — no `proposed_signal`, entry, stop, or TP exists; this is a data-integrity gap, not a trade setup.
- **New UNH long exposure** without a legal-risk review; DOJ scope remains open and unresolved.
- **Fresh AI-token longs** (TAO, RENDER, FET, NEAR) while the `ai_narrative` basket shows active defensive rotation.
- **Chasing JPM/XLF strength off the headline alone** — every raw A/B stocks candidate remains gate-demoted to C this cycle regardless of the green close; require the gates to clear, not just price momentum.
- This is a decision-window-only call — scanning, tracking, candidate generation, and outcome recording continue in all cases; nothing here is a command to pause any part of the system.

## 10. Main Risks

- Geopolitical: Iran/Strait-of-Hormuz tensions remain live (fourth round of US airstrikes reported 2026-07-13; Iran declared the strait closed "until further notice"); Trump did drop the 20% transit fee demand, which eased oil/macro-risk slightly this cycle, but the underlying conflict is not resolved — still the dominant tail risk into the overnight/Asia session.
- Concentration: crypto active-signals remain heavily weighted toward swing longs in altcoins (majority of the 21 open positions) against a weak-breadth, still-elevated-macro-risk backdrop — an unwind-together correlation cluster if BTC breaks down.
- Data-integrity: HEI/USDT untracked Telegram alert persists into its third consecutive review cycle — treat any future similarly-unmatched alert with the same suspicion (see §14).
- Catalyst-mapping weak this run (82.7% unmapped) — treat the catalyst layer as context only, not a standalone decision input (recurring, already tracked, not worsening materially vs 83.7% last cycle).
- Legal/headline: UNH's DOJ probe (Optum Rx, physician reimbursement) remains a live manual-review item for existing exposure, unchanged this cycle.
- Historically weak buckets to lean against: crypto tier=B triggered winrate 15% (signal-stats observation, manual-approval-required flag); weekend crypto signals underperform (24% WR, n=50); stocks tier=C triggered winrate 12% / PF 0.73 (both below the desk's own 0.8 bar); crypto scalp mode remains data-collection-only (PF 0.14).

## 11. Action Plan — next 4 hours

- Manage TAO/USDT short toward TP2 196.05 / TP3 191.15; only add on a fresh 1h failed-bounce retest into 198.99-200.09, invalidate above 201.44.
- Manage SYN/USDT toward its stated TP ladder; do not add fresh size without a confirmed hold above the 0.260537-0.269698 trigger zone.
- Do not enter SXT/USDT at current levels; wait for a retest back into 0.008652-0.008948 (or the wider 0.0090-0.0093 conditional zone) with a volume pickup.
- Continue treating UNH as manual-review-only for existing exposure; no new entries while the DOJ gate is active.
- Watch for any post-close overnight Asia-session reaction to the Iran/Hormuz situation — this is the dominant swing factor into the next (04:30 EEST) crypto-overnight review.
- Root-cause (operator task, not this run) why HEI/USDT continues to fire Telegram alerts without a matching `proposed_signal` across three consecutive cycles now — see §14.

## 12. Final Verdict per Mode

- **Crypto scalp**: No trade — desk already treats this mode as data-collection-only (PF 0.14, kill-switch active for most raw candidates this cycle).
- **Crypto intraday**: Manage existing (SYN, SXT-watch only); no new actionable A/B this cycle (0 A-tier, 0 B-tier fresh).
- **Crypto swing**: Manage existing book (majority tp1/tp2_hit, healthy); underlying swing report itself is stale (>14h) so no fresh swing verdict issued this cycle — carry-forward only.
- **Stocks intraday**: No trade — 0 A/B actionable after gates despite a green, risk-on close; all raw A/B (META, AMD, NVDA, PLTR, JPM, AMZN, COIN, QQQ, SMH, XLF, AVGO, UNH) demoted to C.
- **Stocks swing/invest**: Deprecated / stale data source (2026-07-02), no verdict issued, consistent with prior desk decision.

## 13. Sources

- [Bitcoin Holds $62,000 Despite US Strikes, Strait of Hormuz Tensions](https://en.bloomingbit.io/feed/news/116214) — BloomingBit, 2026-07-14
- [U.S.-Iran escalation weighs on bitcoin (BTC) price, stocks as oil climbs: Crypto Daily](https://www.coindesk.com/daybook-us/2026/07/14/u-s-iran-escalation-weighs-on-bitcoin-stocks-as-oil-climbs) — CoinDesk, 2026-07-14
- [Stock Market Live July 14, 2026: S&P 500 (SPY) Regaining Lost Ground on Inflation Report](https://247wallst.com/investing/2026/07/14/stock-market-live-july-14-2026-sp-500-spy-regaining-lost-ground-on-inflation-report/) — 24/7 Wall St., 2026-07-14
- [Stock Market Today (July 14, 2026): Nasdaq, S&P 500 rise as inflation cools more than expected](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-july-14-2026) — TheStreet, 2026-07-14
- [Bittensor (TAO) Defends Key Support: Can It Shake Off Selling Pressure?](https://cryptonews.net/news/analytics/33144974/) — cryptonews.net, 2026-07-14
- [DOJ's criminal probe into UnitedHealth extends to Optum Rx, physician reimbursement](https://www.fiercehealthcare.com/payers/wsj-report-doj-interviewing-former-employees-about-medicare-billing-practices-unitedhealth) — FierceHealthcare, 2026-07-14 (internal `news_items`, re-confirmed)
- [UnitedHealth stock sinks 4.7% after company confirms DOJ investigation into Medicare billing practices](https://finance.yahoo.com/news/unitedhealth-stock-sinks-47-after-company-confirms-doj-investigation-into-medicare-billing-practices-133527260.html) — Yahoo Finance, 2026-07-14 (internal `news_items`, re-confirmed)

## 14. Fix Requests / TODO

### TODO-hei-usdt-untracked-alert-recurring
- **issue:** HEI/USDT B-tier intraday Telegram alert (score 68.7, long, sent 2026-07-14T14:54:37Z) has no matching `proposed_signal` — third consecutive review cycle (11:39, 18:39, 21:39) flagging the same untracked alert. It will not contribute to PF/winrate/avgR.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-14` → "1 untracked legacy crypto alert(s)" → HEI/USDT, sent_at 2026-07-14T14:54:37+00:00, trackable=NO (no proposed_signal). Same row across all three cycles today — the gap has not self-resolved the way CRV/USDT's did between the 18:39 and this cycle.
- **suggested manual fix:** Investigate whether the HEI/USDT alert path bypasses `proposed_signal` creation (same root cause as the general untracked-alert class already documented in `AUDIT_NOTE_UNTRACKED_LEGACY_CRYPTO_ALERTS.md`); confirm whether it's a one-off malformed alert or a symptom of a broader pipeline gap given it has now persisted unresolved across 3 cycles (~7 hours) without any newer duplicate alerts, suggesting it's a single orphaned row rather than an ongoing leak.
- **priority:** medium
- **first observed:** 2026-07-14 11:39 EEST (carried forward, not new to this run)

### TODO-catalyst-mapping-weak-recurring
- **issue:** Catalyst→symbol mapping remains weak (82.7% of 3,999 events unmapped this run, 83.7% last cycle) — consistent with the previously-documented ~17% match rate from the news-layer hardening project.
- **evidence:** Python scan of `data/catalysts/2026-07-14/catalyst_events.jsonl`: total=3999, mapped=692, unmapped=3307 (82.7%).
- **suggested manual fix:** No new action needed beyond what's already tracked in `project_crypto_ai_desk_news_layer_hardening` memory / prior audit reports — flagging only to confirm the condition is stable, not worsening.
- **priority:** low
- **first observed:** recurring, already tracked (this run only reconfirms current magnitude)
