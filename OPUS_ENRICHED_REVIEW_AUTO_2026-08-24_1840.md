# Opus Enriched Review — US OPEN REACTION REVIEW — Auto Cycle 18:40 EEST

## 1. Executive Summary

Slot: **US open reaction review** (18:30 EEST fire). Advisory only — no auto-trade, no live execution, no scoring/threshold changes made or recommended for auto-application. Crypto stays technically bullish (BTC/ETH uptrend, 87.5% breadth) but macro-geopolitical risk is pinned at 100/100 (Iran sanctions, Canada-US tariffs, Ukraine) — treat as **mixed**, not clean risk-on. Stocks regime is **chop** (QQQ downtrend 5d, SPY/IWM/DIA range, 25% breadth above EMA20) and the stocks-intraday rolling paper-R drawdown guard is now **fully engaged**, demoting every A/B candidate (ABNB, BKNG, TSLA, MSFT, MRVL, BA, etc.) to C — **zero A/B-tier stocks intraday setups this cycle**. No new crypto A-tier either. Best live idea remains the already-open NEAR/USDT catalyst long. Catalyst mapping is weak this run (75.9% unmapped) — treat the catalyst layer as context, not proof of "no catalyst."

## 2. Data Used

- Reports: `2026-08-24_14-02_scalp_report.md` (17:01 EEST gen), `2026-08-24_14-14_intraday_report.md` (17:12 EEST gen), `2026-08-24_15-35_swing_report.md` (18:34 EEST gen, freshest), `2026-08-24_14-55_stocks_intraday_report.md` (17:55 EEST gen, freshest stocks read)
- `data/catalysts/2026-08-24/catalyst_events.jsonl` (2000 events), `narrative_baskets.jsonl` (2 baskets)
- `python -m src.cli active-signals --asset-class crypto` / `--asset-class stocks` (multiple reads; scheduler was actively writing mid-run, see §14 TODO)
- `python -m src.cli signal-stats --asset-class crypto` / `--asset-class stocks` (week window)
- `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-24`
- `db/crypto_ai_desk.sqlite` direct read-only queries: `news_items` (BLK legal-risk history), `proposed_signals` (signal creation timestamps for ABNB/MA/V/XPL)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-24_1607.md` (16:07 EEST, pre-US-open decision review)
- 1 WebSearch (BlackRock/Rosen Law Firm class action verification) + fetch of search snippets (no separate WebFetch call needed — search results self-verified across 9 independent outlets)

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: 2026-08-24 18:38 EEST (< 2 min old at review start) — **fresh**, not deferred.
- Scheduler was mid-run through a long daily-job chain at review time (crypto swing report daily took 787s ending 18:37 EEST; stocks position-framework shadow scans running 18:38-18:40 EEST) — DB write contention caused two `signal-stats`/`active-signals` CLI calls to time out at 90-120s and retry in background; completed successfully on retry.
- Report file timestamps in filenames are UTC; "Generated at" fields are EEST (UTC+3) — cross-checked, consistent.
- Swing report: 5 min old (freshest). Intraday: ~1.5h old. Scalp: ~1.6h old. Stocks intraday: ~45 min old (post-open, includes RTH reaction). All within carry-forward/fresh bands, no staleness flag needed.
- Stocks swing/invest (old, deprecated) reports are from 2026-07-02 — expected, per [[project_crypto_ai_desk_stocks_position_framework]] these are permanently deprecated/removed, not a freshness issue.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-08-24 18:40 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh"], "data_missing": [], "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 18:38 EEST", "swing report 5min old", "stocks intraday report 45min old"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["mixed", "chop", "shorts_preferred"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH uptrend, 87.5% breadth, macro risk 100/100", "stocks: regime=chop, VIX 15.82, QQQ downtrend 5d -3.27%, breadth_above_ema20=25%"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "stale_catalyst"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["2000 catalyst events, 1518 unmapped (75.9%)", "NEAR/USDT ai_narrative catalyst fresh <6h", "BLK Rosen Law Firm notice recurring since 2026-07-15, republished 2026-08-24"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.5,
      "reason_codes": ["oi_supports", "data_unavailable"], "data_missing": ["bybit ohlcv 18 failed fetches this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["VIRTUAL/PROM/AERO/POL/STORJ: price up + OI up, funding ~5e-05 (neutral, not extreme)", "COTI/PORTAL/ZAMA: price up + OI down = short covering"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["overextended", "clean_retest", "entry_late"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["VIRTUAL/PROM/COTI 24h +10-30%, pullback zones defined not chased", "stocks: all top-scored A candidates gate-demoted, no clean entry this cycle"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 50 triggered + 29 tp1 + 13 tp2 open, 13 waiting", "stocks: 23 triggered + 144 tp1 + 48 tp2 open, 7 waiting", "17 untracked legacy crypto alerts today"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["reduce_risk", "legal_risk", "daily_loss_pressure"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["stocks headline A/B: winrate 6.9%, PF 0.125, totalR -3.5 (week)", "BLK class-action investigation ongoing, republished today", "stocks intraday drawdown guard fully engaged both long+short"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto intraday PF2.51/+53R, swing PF2.21/+25.5R (strong)", "crypto scalp PF0.10/-4.5R (known weak lane)", "stocks A-tier PF4.0/+6R but n=19 (low sample), B/C tiers negative"] },
    { "agent": "head_trader", "verdict": "manual_review", "confidence": 0.65,
      "reason_codes": ["watch_only", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "NEAR/USDT", "trigger": "already open/actionable, catalyst-backed", "reason": "quantum-resistant pilot catalyst, ai_narrative basket, crypto breadth bullish" },
    "best_short_candidate":    { "symbol": "TUT/USDT", "trigger": "1h close below current swing low, confirmation of continued RS weakness", "reason": "weakest symbol today (24h -19.24%, RS vs BTC -22.68%), no existing position to conflict" },
    "best_catalyst_candidate": { "symbol": "NEAR/USDT", "trigger": "already open", "reason": "same as best-long — cleanest catalyst-confirmed name on the desk right now" },
    "avoid_candidate":         { "symbol": "BLK", "reason": "ongoing securities class-action investigation (Rosen Law Firm), recurring since 2026-07-15, republished 2026-08-24; correctly demoted A→C" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh | advisory_only |
| market_regime | caution | 0.75 | mixed, chop, shorts_preferred | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, fresh_catalyst, stale_catalyst | advisory_only |
| derivatives_squeeze | ok | 0.50 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.65 | overextended, clean_retest, entry_late | advisory_only |
| execution_lifecycle | caution | 0.60 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.70 | reduce_risk, legal_risk, daily_loss_pressure | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | manual_review | 0.65 | watch_only, wait_for_trigger | advisory_only |

## 4. What Changed vs Previous Review (16:07 EEST — pre-US-open decision review)

- **Stocks intraday guard now fully active**: at 16:07 the review still listed TSLA/GILD/AMAT/INTC as post-open watch candidates. By 17:55 EEST (post-open, current data), the rolling paper-R drawdown guard (`stocks_intraday_long_guard` + `stocks_intraday_short_guard`) demotes **every** A/B raw candidate to C — including TSLA, ABNB, BKNG, COP, UBER, MSTR, MSFT, DIS, KO, GOOGL, SOFI, MRVL, NOW, BA. Zero A/B actionable stocks intraday setups this cycle.
- **AMAT/INTC short-watch dropped out entirely**: neither symbol appears in the current top-candidates or rejected list — they no longer scored high enough to surface, so the pre-open short-watch trigger from 16:07 is now moot (not confirmed, not failed — just not present).
- **PUMP/USDT bias-tag contradiction appears resolved**: 16:07 review flagged PUMP tagged bias=short with negative 24h while holding an open long. Current news shows PUMP +109.6% today (top-10 altcoin performer list) — no longer in any weakest-symbols list. Removing from active-watch, but keep the underlying detector logic on the TODO list (§14) since the pattern has recurred multiple times historically (see [[project_crypto_ai_desk_bias_tag_contradiction]]).
- **New contradiction surfaced**: XPL/USDT — open B-tier swing long (`waiting_for_entry` since 2026-08-24T04:09 UTC) but tagged bias=short in the current swing report's weakest-symbols list (24h -9.33%, RS vs BTC -12.76%). Same class of issue as the PUMP case; see §7.2.
- **NEAR/USDT unchanged**: still the cleanest catalyst-backed long, still open, thesis intact.
- **MSTR "$1.6B war chest" headline**: not re-verified this cycle (no new catalyst event for MSTR since 16:07); prior stale-headline finding stands.
- **Untracked alert count**: 17 today (vs 9 reported at 16:07) — count has grown through the session, confirming this is an ongoing per-scan leak, not a one-off.

## 5. Catalyst Coverage

- Total `catalyst_events` today: **2000**; mapped (symbol present): **482**; unmapped: **1518** (**75.9% unmapped**).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Narrative baskets: **2** active — `rwa_narrative` (ONDO/XLM, freshness <1h) and `perps_dex_narrative` (HYPE primary, DYDX/GMX/ASTER related, freshness <6h).
- Top 3 unmapped headlines (symbol resolution failed):
  1. "Bybit now supports $GROVE deposits and withdrawals on Mantle Network..."
  2. "NOMURA INTERNATIONAL FUNDING SECURED AN 'A-' CREDIT RATING FROM FITCH..."
  3. "Pulnovo Medical Announces First Two U.S. Patients Enrolled in PULSE-LHD IDE Clinical Trial..."

## 6. Market Landscape

**Crypto:** BTC/ETH both in uptrend, 87.5% of tracked symbols above EMA20/EMA50, desk regime label "bullish trend (risk-on)." Fear & Greed flipped to Extreme Greed (81). But the macro-geopolitical layer is independently pinned at 100/100 risk (Iran secondary-sanctions escalation, Canada-US auto-tariff hike to 50%, Ukraine missile-interceptor headlines) — a genuine two-layer tension: technically bullish, macro-fragile, unchanged in character from the 16:07 review.

**Stocks:** regime flipped from "transition/neutral pre-market" (16:07) to **"chop"** now that RTH has confirmed: 0/4 major indices trending up, QQQ in a 5d downtrend (-3.27%), SPY/IWM/DIA all range-bound, breadth thin (only 25% of symbols above EMA20 despite 75% above EMA50 — a short-term pullback inside a longer uptrend). VIX calm at 15.82 (no stress, just chop). Sector leadership: energy and consumer_discretionary strongest (RS +4.4%/+3.7% vs SPY); utilities and industrials weakest (RS -9.4%/-5.5%). This is consistent with — and likely the direct cause of — the stocks-intraday drawdown guard now blocking every new A/B candidate.

### Market Mood / Risk Routing
- Crypto mood: **mixed** (technically risk-on, macro risk-off — treat as chop/danger for aggressive sizing)
- Stocks mood: **chop** (confirmed post-open; not risk-off in the VIX sense, just directionless/thin — guard-driven caution is appropriate)
- Dominant narrative: crypto — perps_dex (HYPE) and rwa (ONDO/XLM) baskets freshest; momentum names (VIRTUAL/PROM/COTI) extended without fresh catalysts. Stocks — no dominant theme; energy/consumer_discretionary rotation vs weak utilities/industrials.
- Preferred side now: **crypto: selective longs, RS-leader + catalyst-confirmed only (NEAR/USDT); stocks: no new entries either side — guard is correctly blocking both longs and shorts this cycle, wait for the guard to clear or for a genuinely clean RTH breakout**
- Best long candidate: **NEAR/USDT** (crypto, catalyst-backed, already open)
- Best short candidate: **TUT/USDT** watch (crypto, weakest symbol today, no conflicting open position) — trigger: 1h close below current structure/swing low
- Best catalyst-backed candidate: **NEAR/USDT** (same as best long)
- What to avoid: **BLK** (ongoing legal risk, verified); new stocks longs or shorts before the drawdown guard clears (every A/B candidate is currently gated); chasing VIRTUAL/PROM/COTI at spot (10-30% extended, only actionable at stated pullback zones)
- What would change the view: the stocks drawdown guard clearing (would reopen A/B actionability); a clean RTH breakout with rising relative volume in an ungated name; de-escalation on the Iran/Canada headlines (would resolve crypto's mixed-mood tension toward clean risk-on)

## 7. Candidate Deep Dives

### 7.1 NEAR/USDT — LONG, catalyst-backed (crypto, swing + intraday, B-tier, open)
- Catalyst: banks/regulators joining a quantum-resistant crypto transfer pilot on NEAR testnet (CryptoBriefing), part of `ai_narrative` basket, unchanged and still the freshest verified catalyst on the desk.
- Price reaction: already triggered/open (intraday leg hit tp2 earlier today) — not a fresh chase.
- Actionable: yes, already open. Aligned with mood (catalyst-confirmed inside a bullish-breadth market).
- Invalidation: per active-signals row (~1.95-1.97 depending on leg).
- Would invalidate: 1h close below invalidation, or a reversal/contradiction of the quantum-pilot story.

### 7.2 XPL/USDT — CONTRADICTION, needs review (crypto, swing, B-tier, waiting_for_entry since 2026-08-24T04:09 UTC)
- Desk holds an open B-tier swing **long** proposal (entry 0.0957-0.0972, invalidation 0.0938, still `waiting_for_entry`), score 67.0.
- Today's flow data tags XPL/USDT **bias=short** in the weakest-symbols list: 24h -9.33%, RS vs BTC -12.76%.
- This is the same pattern as the PUMP/USDT contradiction resolved earlier this session and the ZBT/ACE contradictions from [[project_crypto_ai_desk_bias_tag_contradiction]] (escalated to HIGH priority 2026-08-08, recurring).
- Actionable: **no** — do not let this waiting long convert to a filled position without a manual bias check; flagged for operator review (§14).

### 7.3 ABNB / MA / V — stocks, guard-vs-open contradiction (A/A/B-tier, all `waiting_for_entry` since 2026-08-24T14:00:02 UTC)
- Registered at the pre-open scan (17:00 EEST) with strong scores (ABNB 95.5, MA 84.3, V 78.7), still sitting unfilled.
- The **current** (post-open, 17:55 EEST) stocks-intraday scan would **not** generate these as A/B today — ABNB itself reappears in this scan at a lower raw score (87.23) and gets demoted C via `stocks_intraday_long_guard`.
- Actionable: **manual review** — these are stale-relative-to-current-guard-state signals; if they fill, treat with the same skepticism the guard is currently applying to fresh candidates, not as pre-cleared setups.
- Would invalidate: guard-driven caution is the market's current read; a genuine RTH breakout with confirming volume would be the only thing that overrides it.

### 7.4 BLK — AVOID (stocks, was A-tier raw, demoted A→C: legal/headline risk)
- **Verified via WebSearch** (9 independent outlets: PRNewswire, GlobeNewswire, Businesswire, Morningstar, Newsfilecorp, local press-release syndication): Rosen Law Firm has an **ongoing securities class-action investigation** into BlackRock, Inc. mutual funds, alleging materially misleading business information. Announcements recur roughly weekly/biweekly since at least 2026-07-15, most recently **republished today (2026-08-24)**.
- This is a real, ongoing legal matter (investor-rights solicitation tied to an active investigation), not a single stale headline — the desk's `legal_headline_risk: class_action` demotion is correctly justified.
- Actionable: **no** — avoid new long exposure regardless of technical score (raw score was 81.55, A-tier before the gate).
- Would invalidate the avoid: investigation formally dropped/settled with no finding, or a sourced statement clarifying immateriality.

### 7.5 TUT/USDT — SHORT-WATCH (crypto, not currently an active signal)
- Weakest symbol across both scalp and swing "Where Money Is Flowing" sections: 24h -19.24% (swing) to -10.53% (scalp snapshot), RS vs BTC -22.68% / -11.83%.
- No existing open position on this symbol (unlike XPL/PUMP), so no bias-tag conflict.
- Not yet a scored/proposed signal — this is a manual watch idea, not a system-generated one.
- Actionable: **only on confirmation** — 1h close below the current swing structure low, ideally with volume, would make this a clean relative-weakness short in a market that is otherwise bullish-breadth (a genuine laggard, not a beta short).
- Would invalidate: a reclaim of the recent range with volume, or a broad BTC/ETH breakdown that makes the whole book risk-off (at which point this becomes a beta short, not a clean RS short).

## 8. Best Candidates Ranked

1. **NEAR/USDT** — LONG, catalyst-backed, already open/actionable. Best overall candidate this cycle (unchanged from 16:07).
2. **TUT/USDT** — SHORT-WATCH, cleanest relative-weakness idea with no conflicting position; trigger: 1h close below structure low.
3. **XPL/USDT** — NEEDS REVIEW (contradiction) — do not let the waiting long fill without checking current bias tag.
4. **ABNB / MA / V** — stocks, NEEDS REVIEW (guard-vs-open contradiction) — stale-relative-to-guard, treat with elevated skepticism if filled.
5. **BLK** — AVOID (legal risk, verified).

## 9. Avoid / No Trade

*(This decision window only — never a command to stop scanning, tracking, or the scheduler.)*

- **BLK** — verified ongoing securities class-action investigation; do not take new long exposure (§7.4).
- **New stocks A/B entries generally** — the drawdown guard is correctly blocking every raw A/B candidate (TSLA, MSTR, MSFT, GOOGL, MRVL, BA, etc.) this cycle; respect the gate rather than treating the raw (pre-gate) score as tradeable.
- **VIRTUAL/PROM/COTI at spot** — 10-30% extended over 24h; only actionable at the stated pullback zones in the reports, not at market price.
- **XPL/USDT long fill** — pending bias-tag review (§7.2); do not treat as clean until resolved.
- **MSTR "$1.6B war chest" headline** — verified stale/inaccurate at the 16:07 review; no new catalyst since, finding still stands.

## 10. Main Risks

- **Crypto stats methodology caveat**: the week's crypto headline performance (PF 2.21, +74R) uses the desk's standard touch-based accounting. Per [[project_crypto_ai_desk_touch_based_pnl]], touch-based `final_r` (highest-TP-touched) has historically overstated realized PnL by roughly +100-143R vs. realistic execution — treat the +74R headline as directionally positive but not literally achievable P&L.
- **Stocks book-wide weakness deepened**: headline actionable A/B winrate is now 6.9% / PF 0.125 / -3.5R this week (worse than the 16:07 review's already-poor read) — consistent with, and likely the direct driver of, the drawdown guard now blocking new entries.
- **Catalyst mapping weak (75.9% unmapped)** — do not treat "no catalyst found" as proof nothing is happening for any symbol not explicitly checked.
- **Untracked alert leakage grew intraday**: 17 crypto Telegram alerts today (up from 9 at 16:07) have no backing `proposed_signal` — those outcomes will never be counted in PF/winrate stats.
- **Bias-tag contradiction recurrence**: XPL/USDT today, PUMP/USDT earlier this session, ZBT/ACE historically — this is now a recurring pattern across multiple review cycles, not a one-off (§14).
- **Active-signals count instability**: two CLI reads minutes apart returned materially different stocks counts while the scheduler was writing — see §14, likely benign (live writes) but not confirmed.

## 11. Action Plan — next 4 hours

1. Hold NEAR/USDT long; no size addition on the catalyst alone.
2. Watch TUT/USDT for a confirmed 1h close below structure before treating it as a short idea — this is a watch-only idea, not yet a system signal.
3. Do not let the XPL/USDT waiting long convert without a manual bias-tag check against current weakest-symbols data.
4. Do not treat ABNB/MA/V waiting signals as pre-cleared if they fill — the live guard state disagrees with their original (17:00 EEST) scores.
5. Avoid BLK entirely pending resolution of the securities investigation.
6. Respect the stocks-intraday drawdown guard — no manual override into any of the currently-demoted A/B-raw names (TSLA, MSTR, MSFT, GOOGL, MRVL, BA, etc.).
7. Continue scanning/tracking as normal in all modes — no pause, no stop, regardless of the caution verdicts above.

## 12. Final Verdict per Mode

- **Crypto scalp:** caution — PF~0.10 this week (matches the report's own low-confidence banner); research-grade only.
- **Crypto intraday:** watch/actionable — PF~2.51, strongest crypto lane this week; prefer catalyst-backed names (NEAR/USDT).
- **Crypto swing:** watch/actionable — PF~2.21; NEAR/USDT is the cleanest open idea; XPL/USDT waiting long needs a bias review before it's trusted.
- **Stocks intraday:** manual_review — drawdown guard fully engaged, zero A/B actionable this cycle; wait for the guard to clear or a genuinely clean RTH breakout.
- **Stocks swing/invest (old):** not applicable — deprecated/removed, never actionable.
- **Stocks swing growth-breakout (new):** shadow-only research; no change to that status this run.

## 13. Sources

- [Rosen Law Firm Encourages BlackRock, Inc. Mutual Fund Investors to Inquire About Securities Class Action Investigation — PR Newswire](https://www.prnewswire.com/news-releases/rosen-law-firm-encourages-blackrock-inc-mutual-fund-investors-to-inquire-about-securities-class-action-investigation-302843055.html) — recurring release, most recent instance 2026-08-24
- [BlackRock Investor News: Rosen Law Firm — GlobeNewswire](https://www.globenewswire.com/news-release/2026/08/24/3349435/673/en/blackrock-investor-news-if-you-have-suffered-losses-in-blackrock-inc-mutual-funds-you-are-encouraged-to-contact-the-rosen-law-firm-about-your-rights.html) — 2026-08-24
- [Rosen Law Firm Encourages BlackRock, Inc. Mutual Fund Investors — Morningstar syndication](https://www.morningstar.com/news/pr-newswire/20260810dc22374/rosen-law-firm-encourages-blackrock-inc-mutual-fund-investors-to-inquire-about-securities-class-action-investigation) — 2026-08-10 (earlier recurrence, confirms pattern)
- Internal: `data/catalysts/2026-08-24/catalyst_events.jsonl`, `narrative_baskets.jsonl`; `db/crypto_ai_desk.sqlite` `news_items` table (source `PR Newswire (Stocks)`, 6 recurrences 2026-07-15 through 2026-08-19 plus today's WebSearch hit); `data/reports/swing/2026-08-24_15-35_swing_report.md`; `data/reports/stocks/intraday/2026-08-24_14-55_stocks_intraday_report.md`; previous review `OPUS_ENRICHED_REVIEW_AUTO_2026-08-24_1607.md`.

## 14. Fix Requests / TODO

### TODO-untracked-alerts-growth
- **issue:** 17 untracked legacy crypto Telegram alerts today (no backing `proposed_signal`), up from 9 at the 16:07 review — the leak is ongoing throughout the session, not a one-off. Matches previously-escalated bug [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]] (confirmed on ALLO/USDT + BANK/USDT, raised to high priority 2026-07-17).
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-24` → 17 rows, all `NO (no proposed_signal)`, spanning 10:11-15:39 UTC today.
- **suggested manual fix:** investigate why watchlist re-fires are still not minting a fresh `proposed_signal`/`signal_id` per the TODO-3 root cause already on file; this is a recurrence, not a new finding.
- **priority:** high
- **first observed (this recurrence):** 2026-08-24 18:40 EEST (originally 2026-07-17)

### TODO-bias-tag-contradiction-xpl
- **issue:** Open B-tier swing LONG on XPL/USDT (`waiting_for_entry` since 2026-08-24T04:09 UTC) while today's weakest-symbols data tags it bias=short (24h -9.33%, RS vs BTC -12.76%). Same recurring pattern as [[project_crypto_ai_desk_bias_tag_contradiction]] (PUMP/USDT earlier today, ZBT/ACE 2026-08-08).
- **evidence:** `active-signals --asset-class crypto` row `sig_b4dd748b2c4a5cd0 XPL/USDT B swing long waiting_for_entry`; swing report §2 Weakest Symbols row "XPL/USDT: bias short, 24h -9.33%, RS vs BTC -12.76%".
- **suggested manual fix:** add a pre-fill bias-tag cross-check gate for `waiting_for_entry` signals so a symbol newly tagged bias=short blocks conversion to `triggered` until manually cleared.
- **priority:** medium (recurring pattern, not yet causing a live loss since XPL is still unfilled)
- **first observed (this instance):** 2026-08-24 18:40 EEST

### TODO-active-signals-count-instability
- **issue:** `active-signals --asset-class stocks --limit 500` returned materially different status counts across two calls ~10 minutes apart while the scheduler was mid-run: waiting_for_entry 31→7, triggered 15→23, tp1_hit 141→144. Plausibly explained by live scheduler writes (stocks position-framework scans were running concurrently), but not confirmed as benign.
- **evidence:** first read via combined background command ~18:40 EEST; second isolated read ~18:52 EEST; scheduler.log shows "stocks position framework scan (shadow, daily)" and related jobs running in that window.
- **suggested manual fix:** a human session should re-run `active-signals --asset-class stocks` after the scheduler's daily job chain fully completes and confirm the counts stabilize; if they don't, investigate for a query/index issue rather than assuming live-write noise.
- **priority:** low
- **first observed:** 2026-08-24 18:40 EEST
