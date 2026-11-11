# Opus Enriched Review — Crypto Overnight / Asia Review — Auto Cycle 04:43 EEST

## 1. Executive Summary

- **Slot: crypto overnight / Asia review**, 2026-08-04 04:43 EEST. **Advisory only — no auto-trade.**
- Crypto regime: range/chop, ETH downtrend, BTC risk-off headwind. External check confirms BTC ~$62.8k (below 20MA, descending channel) and ETH ~$1,865 (range-bound) — consistent with internal reports.
- **No A/B setup cleared the desk threshold** in scalp, intraday, or swing this cycle (fourth+ consecutive no-trade cycle per prior review's own count).
- One active B-tier swing order, **VIC/USDT**, is still `waiting_for_entry` at 0.040–0.042 while spot has run to ~0.053 (+55% since order was set) — the entry zone is now stale/chase-risk, not a live trigger.
- Four open B-tier crypto positions (**HOME, EPIC, AEVO, COTI**) are `triggered`/running; **XRP/USDT** short already booked TP1. **COTI/EPIC/AEVO still do not appear in any of tonight's fresh reports** (price/technical sections) — blind spot carried forward unchanged from the prior three reviews.
- Catalyst mapping is **weak this run**: 266/500 events (53.2%) unmapped — treat the catalyst layer as context, not a decision input.
- Stocks: US cash session closed (Asia hours) — all candidates demoted to C-tier/planning-only. No overnight surprises beyond the already-known AMD/CAT/SMCI earnings later today (2026-08-04 RTH).
- Routed decision: **watch-only**. Best long-watch VIC/USDT (pullback only), best short-watch BANK/USDT (needs confirmation), best catalyst-watch BTC/USDT (Coldcard exploit resolution). Scanning, tracking, and monitors continue unchanged — this is a decision-window verdict, not a system pause.

## 2. Data Used

- `data/reports/scalp/2026-08-03_23-47_scalp_report.md` (gen 02:47:53 EEST)
- `data/reports/intraday/2026-08-03_23-53_intraday_report.md` (gen 02:53:57 EEST)
- `data/reports/swing/2026-08-03_21-31_swing_report.md` (gen 00:31 EEST — carry-forward, ~4h12m old)
- `data/reports/stocks/intraday/2026-08-04_00-11_stocks_intraday_report.md` (gen ~03:11 EEST; market closed anyway)
- Stocks swing/invest: excluded — deprecated framework, last artifact 2026-07-02 (>1 month stale)
- `data/catalysts/2026-08-04/catalyst_events.jsonl`, `narrative_baskets.jsonl`, `catalyst_cycle_01-40.md` (regenerated this run via `catalyst-scan`, folder was missing at run start)
- `data/processed/llm_analysis_packet.md` (02:54 EEST), `data/processed/llm_stocks_packet.md` (03:13 EEST)
- CLI: `active-signals --asset-class crypto` (22 rows), `active-signals --asset-class stocks` (50 rows), `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`, `detect_untracked_legacy_alerts --since 2026-08-04`
- `db/crypto_ai_desk.sqlite` — direct read-only `news_items` freshness queries (last 4h/6h windows) for BTC/Coldcard/VIC/HOME/BANK/XRP
- External: WebSearch (Coldcard exploit update, BTC/ETH Aug-4 price context) + implicit fetch of search snippets — see §13
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-03_2315.md` (23:15 post-close cycle)

## 3. Scheduler / Data Freshness

- `scheduler.log` and latest `cycle_03_02-39_summary.md` in `data/scheduled_runs/2026-08-03_default_schedule/` both mtime **2026-08-04 03:23 EEST** (~80 min old) — **fresh**, no defer needed.
- Scalp/intraday reports: ~110–116 min old — **fresh**.
- Swing report: ~4h12m old — **carry-forward** (just past the 4h fresh cutoff; used as-is, flagged).
- Stocks intraday: ~92 min old — **fresh** (moot; market closed).
- Catalyst folder for 2026-08-04 was **missing at run start**; regenerated via the allowed `catalyst-scan --no-print` CLI (events=500, baskets=4, no rejections).
- Monitor processes with logs updated within the last ~5 minutes of run start: `derivatives_monitor`, `fast_news_monitor`, `mexc_canary_monitor`, `pending_monitor`, `stocks_monitor` — all appear alive.
- `detect_untracked_legacy_alerts --since 2026-08-04`: **0 anomalies** — every legacy crypto alert has a backing `proposed_signal`.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-08-04 04:43 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "derivatives_sparse"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 03:23 EEST", "cycle_03_02-39_summary.md mtime 03:23 EEST", "catalyst-scan rerun: events=500 baskets=4"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["chop", "risk_off", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC trend=range, ETH trend=downtrend (internal)", "altcoin breadth 60% >EMA20", "macro risk 100/100", "external: BTC ~$62.8k below 20MA, ETH ~$1,865 range-bound"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "no_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["234/500 mapped (46.8%), 266/500 unmapped (53.2%)", "4 narrative baskets", "BTC Coldcard fresh_catalyst(risk); VIC/HOME/BANK no_catalyst confirmed via direct news_items query"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "data_unavailable"],
      "data_missing": ["OI/funding for several C-tier symbols (SNXXB, SNDKB, SPCXB, KORUB)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["KAITO/GIGGLE/BANK capped to C via short_bounce_guard / thin_liquidity_short_squeeze_risk"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["entry_late", "chase_risk", "price_moved_away", "overextended"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["VIC/USDT waiting_for_entry 0.040-0.042 vs current 0.0530 (order zone now ~2.2 ATR below spot)", "VIC/TUT/BTW all >20% 24h move, chase-risk flagged in reports"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.75,
      "reason_codes": ["waiting_for_entry", "open_actionable", "no_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active B-tier: 1 waiting_for_entry (VIC), 4 triggered (HOME/EPIC/AEVO/COTI), 11 tp1_hit, 6 tp2_hit (all OPEN actionable, trailing)", "stocks: all C-tier, market-closed planning-only, 0 A/B actionable"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["headline_risk", "correlation_cluster"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC exploit_hack risk_warning + block_requires_operator_review active", "MSFT/AMZN/GOOGL legal-risk demotions carried from prior cycle (stocks, moot while closed)", "AMD/CAT/SMCI earnings today (2026-08-04) — do_not_chase_warning"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto B-tier headline: n=61, winrate 18.2%, PF 1.66, totalR +10.50", "scalp mode 14d PF 0.14 (structurally negative, data-collection only)", "stocks C-tier: n=200, winrate 6%, PF 0.54 (below 0.8)"]
    },
    {
      "agent": "head_trader",
      "verdict": "watch_only",
      "confidence": 0.65,
      "reason_codes": ["wait_for_trigger", "shorts_preferred_secondary"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above; no A/B clears threshold; routed to watch/avoid-chase this window"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": { "symbol": "VIC/USDT", "trigger": "clean pullback/retest into 0.0436-0.0458 (swing) or 0.0490-0.0518 (intraday) with volume; do not chase current extension", "reason": "RS-BTC leader (+55%), narrative-basket member, but order zone has moved far below spot — needs fresh confirmation, not the stale pending order" },
    "best_short_candidate": { "symbol": "BANK/USDT", "trigger": "confirmed bearish HTF break + derivatives confirmation + clear stop above swing high; squeeze-guard first", "reason": "weakest-symbols list, catalyst-backed watchlist entry, but currently capped to C for thin-liquidity squeeze risk" },
    "best_catalyst_candidate": { "symbol": "BTC/USDT", "trigger": "a clean 24h with no new Coldcard theft wave, or Coinkite/Galaxy issuing a formal resolution/insurance statement", "reason": "ongoing exploit now verified at ~$116M/1,816 BTC (external), actively suppressing risk appetite market-wide" },
    "avoid_candidate": { "symbol": "Crypto scalp mode (all symbols)", "reason": "structurally negative 14d edge (PF 0.14); kill-switched for new entries, active for data collection only" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, derivatives_sparse | advisory_only |
| market_regime | caution | 0.70 | chop, risk_off, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, fresh_catalyst, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.65 | entry_late, chase_risk, price_moved_away, overextended | advisory_only |
| execution_lifecycle | ok | 0.75 | waiting_for_entry, open_actionable, no_entry | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, correlation_cluster | advisory_only |
| playbook_performance | caution | 0.60 | playbook_failing, low_sample | advisory_only |
| head_trader | watch_only | 0.65 | wait_for_trigger, shorts_preferred_secondary | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-03_2315.md` (23:15 EEST post-close cycle).

- **Coldcard exploit escalated externally**: internal reports still cite ~$114M/"fourth wave, 462 new victims"; external check (WebSearch) confirms the figure has grown to **~$116M / 1,816 BTC** across a third wave now targeting smaller balances with harder-to-trace patterns. Coinkite shipped patched firmware back on Aug 1 — mitigation exists, but theft from unmigrated wallets continues.
- **No new A/B signal** appeared in crypto or stocks since the last cycle — this is now the fifth+ consecutive no-trade cycle.
- **VIC/USDT** swing order remains unfilled and is now further extended from its pending zone (price kept climbing since the order was set).
- **Catalyst mapping improved but still weak**: prior review cited 71.5% unmapped for two consecutive cycles; this run's fresh scan shows 53.2% unmapped — better, but still over the 50% weak-mapping threshold.
- **04:30 slot TODO resolved for today**: the prior review's high-priority TODO (`OPUS_ENRICHED_REVIEW_AUTO_2026-08-03_0430.md` / `_1130.md` missing, flagged across four checks) — **this cycle is the 04:30 slot for 2026-08-04 and completed successfully**, breaking the streak for today. Whether the underlying cause (silent failure vs. task misconfiguration) is fixed or this is a one-off remains unconfirmed — see §14.
- **Open-position blind spot unchanged**: COTI/USDT, EPIC/USDT, AEVO/USDT still absent from all of tonight's fresh reports' price/technical sections (confirmed again by direct grep) — same four consecutive-cycle gap as previously flagged.

## 5. Catalyst Coverage

- Total catalyst events today: **500** (regenerated this run)
- Mapped (non-null symbol): **234 (46.8%)**
- Unmapped (null symbol): **266 (53.2%)**
- Narrative baskets: **4** (scan output); report enrichment additionally names a 5th (`momentum_breakout`, fresh <1h) from the prior cycle's snapshot — minor basket-count discrepancy between the raw scan and report-layer enrichment, not investigated further this cycle.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines:
  1. "ARC Group Securities Acquisition I Announces Pricing of $105,000,000 Initial Public Offering"
  2. "Voters prefer Democrats over Republicans on economy for first time in a decade, Reuters/Ipsos poll finds" (Reuters)
  3. "Southern Company announces upsize and pricing of $725 million in aggregate principal amount of Series 2026A/B Convertible Senior Notes"

## 6. Market Landscape

- Crypto: BTC trend range (internal) / ~$62.8k, below 20MA, inside a descending channel, RSI ~44 (external, WebSearch-verified). ETH downtrend / ~$1,865, RSI ~51, range-bound $1,800–$1,900 expected today (external). Altcoin breadth: 60% above EMA20, 52.5% above EMA50. Volatility: BTC ATR percentile 58 (normal).
- Macro/geopolitical risk score: 100/100 — driven by the Coldcard exploit (risk-off for BTC) plus Exxon/Chevron political headlines; no risk-on hits registered.
- Stocks: after-hours/overnight, US cash session closed — planning/watchlist only. VIX 15.86 (calm), regime "chop", breadth 100% above EMA20/50 (thin overnight sample). Energy strongest sector (RS +9.8% vs SPY 20d), semiconductors weakest (RS -10.6%).

### Market Mood / Risk Routing

- Crypto mood: **risk-off / chop** (BTC range + ETH downtrend + Coldcard-driven macro risk-off headwind)
- Stocks mood: **closed** (Asia hours; VIX calm, chop bias into tomorrow's RTH)
- Dominant narrative: BTC self-custody/exploit risk overshadowing altcoin RS leadership (VIC/TUT/BTW momentum) and the AI/RWA/perps-dex narrative baskets
- Preferred side now: **wait-for-trigger**, with a bearish lean if BTC breaks range support
- Best long candidate: VIC/USDT — none clean at current extension; watch pullback zone
- Best short candidate: BANK/USDT — none clean yet; squeeze-guard capped, needs bearish HTF confirmation
- Best catalyst-backed candidate: BTC/USDT — Coldcard exploit resolution/containment watch
- What to avoid: chasing any of the vertical 24h movers (VIC +55%, TUT +15%, BTW +26%) at current extension; new crypto scalp entries (mode kill-switched, structurally negative); new stocks entries before RTH re-evaluation
- What would change the view: a confirmed Coldcard resolution/insurance statement (risk-on unlock for BTC), or a clean volume-backed pullback into the stated VIC/BICO/TUT zones

## 7. Candidate Deep Dives

### BTC/USDT — catalyst-watch (macro risk driver)

- Has price reacted to the catalyst? Yes — BTC slipped intraday on hack fears per internal news, and external sources confirm continued downward pressure with RSI ~44, below 20MA.
- Chasing? N/A — this is a risk-context watch, not a directional entry.
- Retest/pullback structure? BTC sits inside a descending channel with support ~$61.4k/$59.1k and resistance ~$64.6k (external).
- Overextended? No — mid-range, not stretched.
- Late entry risk? N/A (no active trade proposed).
- Actionable level: a confirmed resolution/insurance statement from Coinkite/Galaxy Research, or price reclaiming $64.6k resistance, would materially change the risk read.
- Aligned with mood? Yes — this catalyst is the primary source of tonight's risk-off mood.
- Long/short/wait? Wait-for-trigger (macro context, not a symbol trade).
- Invalidation of the "still risky" thesis: a clean 24–48h with no new theft wave.
- Chase-risk: N/A.
- Catalyst confirmation: **confirmed and escalating** — external WebSearch corroborates internal risk_warning (now ~$116M/1,816 BTC vs. internal report's $114M figure), third wave ongoing, patch shipped Aug 1.

### VIC/USDT — long-watch (best long candidate)

- Has price reacted to the catalyst? No fresh verified catalyst — this is pure RS/momentum (score 92–94 across scalp/intraday/swing "strongest symbols").
- Chasing? **Yes if entered now** — the open B-tier swing order (`sig_34d1801f499a8b3a`, waiting_for_entry 0.040035–0.042019) sits ~2.2 ATR below the current spot of ~0.0530; price has run +55% since the order was set.
- Retest/pullback structure? Watchlist zones from tonight's reports: intraday 0.0490–0.0518, swing 0.0436–0.0458 — both below spot, requiring a genuine pullback, not a fresh high chase.
- Overextended? Yes, on a 24h basis (+55%); 7d return also +52–55% depending on report.
- Would entry now be late? Yes.
- Actionable level: 1h close back inside the stated pullback zones with volume confirmation.
- Aligned with mood? Partially — RS leadership cuts against the broader risk-off mood; treat as an idiosyncratic name, not a beta play.
- Long/short/wait? Long-watch, wait-for-pullback.
- Invalidation: 1h close beyond 0.0408 (swing) / 0.0457 (intraday).
- Chase-risk: high at current price.
- Catalyst confirmation: none — pure momentum/RS thesis (14d no-catalyst intraday cohort is net-negative per report's own playbook note: WR 23%/PF 0.70/−3R), so demand the pullback, not the breakout.

### HOME/USDT — open position context (no fresh catalyst)

- Open B-tier swing long (`sig_57d425cf4bc41003`, triggered, entry 0.006040–0.006171, invalidation 0.005879) is running well — spot ~0.0075 per tonight's intraday desk notes, comfortably above invalidation.
- No fresh verified catalyst in any of tonight's reports or a direct 6h `news_items` check (the only 6h "HOME" text matches were unrelated bank-name headlines, e.g. "Home BancShares").
- Weekend flag shows "Y" on this signal despite today being a Tuesday — likely reflects the original entry timestamp falling on a weekend, not a live labeling bug; not verified further this cycle (see §14 low-priority note).
- Actionable level: N/A — position is open and running; no new entry proposed.
- What would invalidate: 1h close beyond 0.005879 (original invalidation level).

### XRP/USDT — open position + catalyst risk

- Open B-tier swing short (`sig_c1e2871dd5fcaf1a`), TP1 already hit, invalidation 1.0626.
- Catalyst/risk: Ripple's ~$1.06B token unlock is the standing risk flagged in tonight's reports ("Can XRP stay above KEY support after Ripple's unlock?"); no fresh escalation found in a direct 6h `news_items` check beyond general ETF-flow commentary already captured in the report.
- Aligned with mood? Yes — a short thesis fits the risk-off/chop mood, and TP1 is already banked.
- What would invalidate: price reclaiming above 1.0626 (short invalidation).
- Chase-risk: N/A (already in position, trailing).

### BANK/USDT — short-watch (best short candidate)

- Weakest-symbols list in both scalp and intraday reports (24h −3.4% to −3.6%, RS vs BTC negative).
- Currently capped to C-tier: `thin_liquidity_short_squeeze_risk` — squeeze-guard active, meaning a short here right now risks a violent reclaim.
- Has price reacted to a catalyst? Catalyst-backed watchlist entry exists (`crypto_intraday_catalyst_or_momentum`) but no fresh verified catalyst confirmed via direct DB check.
- Actionable level: confirmed bearish HTF structure + derivatives confirmation (funding/OI data currently unavailable for this symbol) + a clear stop above the swing high.
- Chase-risk: moderate — a short into an already-squeeze-flagged thin-liquidity name is exactly the setup the guard exists to block.
- Invalidation of the short thesis: a reclaim of local resistance / squeeze move against the position.

## 8. Best Candidates Ranked

1. **Long-watch: VIC/USDT** — trigger: 1h close back inside 0.0436–0.0458 (swing) or 0.0490–0.0518 (intraday) with volume; do not add at current +55% extension. Existing pending swing order is stale relative to spot.
2. **Short-watch: BANK/USDT** — trigger: confirmed bearish HTF structure + derivatives confirmation + clear stop above swing high; squeeze-guard must clear first.
3. **Catalyst-watch: BTC/USDT** — trigger: a clean 24–48h with no new Coldcard theft wave, or a formal Coinkite/Galaxy resolution statement; track for market-wide risk de-escalation, not a single-symbol trade.
4. **Open-position watch: HOME/USDT (long, running) and XRP/USDT (short, TP1 booked)** — no new entries; monitor invalidation levels only.
5. **Avoid: Crypto scalp mode (all symbols)** — structurally negative 14d edge; kill-switched, data-collection only.

No A/B-tier setup cleared the desk threshold in any crypto mode or stocks intraday this cycle — consistent with the prior cycle's read.

## 9. Avoid / No Trade (this decision window only)

- **VIC/USDT at current spot** — chase-risk; the only reason to act is the stated pullback zone, not the current price.
- **BANK/USDT (and thin-liquidity shorts generally: KAITO, GIGGLE)** — squeeze-guard active; do not short into a reclaim.
- **Crypto scalp mode** — structurally negative 14d (PF 0.14); active for data collection only.
- **Stocks — all names** — market closed; every candidate is C-tier/planning-only; re-evaluate fresh at the 09:30 ET open.
- **AMD, CAT, SMCI** — earnings land later today (2026-08-04 RTH); `do_not_chase_warning` active.
- This is a decision-window verdict only — **not** a recommendation to pause scanning, tracking, or the scheduler, all of which continue normally.

## 10. Main Risks

- **BTC Coldcard exploit** — externally confirmed to have grown to ~$116M/1,816 BTC across a third wave now targeting smaller balances; patched firmware exists since Aug 1, but unmigrated wallets remain exposed. A further escalation would deepen the current risk-off mood market-wide.
- **Catalyst mapping still weak** — 53.2% unmapped this run (improved from 71.5% in the prior two-cycle read, but still over the 50% weak-mapping threshold); keep the catalyst layer as context only.
- **Open-position blind spot (COTI/EPIC/AEVO)** — three of four open non-HOME crypto B-tier positions cannot be cross-referenced against any of tonight's fresh reports; if one breaches invalidation unnoticed, the desk has no fresh-report-based way to catch it this cycle.
- **VIC/USDT chase-risk** — the single active crypto swing order is now materially stale relative to spot; treat any "VIC is the strongest symbol" framing with the pullback caveat front and center.
- **Stocks paper edge still net-negative** — C-tier 30d/week PF 0.54, winrate 6% (n=200); A/B sample remains anecdotal (n=6) and should not be read as evidence either way.
- **Weekend-mode / labeling quirk** — HOME and XRP active signals show `weekend=Y` despite the current date being a Tuesday; likely reflects original-entry timing, not a live bug, but not independently verified this cycle (see §14).

## 11. Action Plan — Next 4 Hours (overnight into Europe morning)

- Monitor BTC/Coldcard for a new theft wave or a formal Coinkite/Galaxy resolution statement; either would materially change the crypto risk-off read heading into the 11:30 EEST Europe/pre-US review.
- Watch VIC/USDT (and secondarily TUT/BICO) for a genuine pullback/retest into the stated conditional zones before considering any addition — do not chase current extension.
- Watch BANK/USDT (and DEXE/VANRY as secondary weak-RS names) for a confirmed bearish HTF break with derivatives confirmation before treating as a clean short.
- No new stocks entries until the RTH open re-evaluates gates fresh; today's earnings (AMD/CAT/SMCI) are a chase-risk zone regardless.
- Continue scanning, tracking, and monitor processes in all cases — no pause recommended for any mode or asset class.

## 12. Final Verdict per Mode

- **Crypto scalp:** No trade. Structurally negative 14d edge (PF 0.14); active for data collection only.
- **Crypto intraday:** Watch-only. Best name VIC/USDT (62.8/100), chase-risk capped at current extension.
- **Crypto swing:** Selective watch. VIC/BICO/TUT conditional long-watch, BANK conditional short-watch; nothing clears the actionable threshold this cycle. One open pending order (VIC) is stale relative to spot.
- **Stocks intraday:** Closed for the session. 0 A/B actionable after gates; re-evaluate fresh at the 09:30 ET open.
- **Stocks swing/invest:** Stale (>1 month, deprecated framework) — excluded from this cycle's verdict, unchanged status.

## 13. Sources

- [Bitcoin owners rocked by $116 million hack: What we know about the Coldcard exploit](https://fortune.com/2026/08/03/bitcoin-owners-116-million-hack-coldcard-coinkite-exploit/) — Fortune, 2026-08-03.
- [Bitcoin cold-wallet attack spreads to 4,500 addresses as losses near $89 million](https://www.coindesk.com/tech/2026/08/02/bitcoin-cold-wallet-attack-spreads-to-4-500-addresses-as-losses-near-usd89-million) — CoinDesk, 2026-08-02.
- [Coldcard Bitcoin Wallets Compromised as Hackers Exploit Software Flaw](https://www.bloomberg.com/news/articles/2026-08-03/hackers-target-bitcoin-s-safest-hiding-place-in-ongoing-attack) — Bloomberg, 2026-08-03.
- [Bitcoin, Ethereum & XRP Price Prediction (August 04): Analysts Eye Key Support Levels](https://sundayguardianlive.com/business/bitcoin-ethereum-xrp-price-prediction-august-04-will-btc-eth-and-xrp-recover-analysts-eye-key-support-levels-as-crypto-market-awaits-fresh-catalysts-252804/) — Sunday Guardian Live, 2026-08-04 (BTC/ETH level context; date unavailable for exact intraday quote, treated as single_source).
- Internal: `data/reports/scalp/2026-08-03_23-47_scalp_report.md`, `data/reports/intraday/2026-08-03_23-53_intraday_report.md`, `data/reports/swing/2026-08-03_21-31_swing_report.md`, `data/reports/stocks/intraday/2026-08-04_00-11_stocks_intraday_report.md`, `data/catalysts/2026-08-04/catalyst_events.jsonl`, `data/catalysts/2026-08-04/narrative_baskets.jsonl`, `OPUS_ENRICHED_REVIEW_AUTO_2026-08-03_2315.md`, `db/crypto_ai_desk.sqlite` (news_items direct query).

## 14. Fix Requests / TODO

### TODO-crypto-open-position-blindspot-generalized (priority: high, unchanged — confirmed persisting)
- **issue:** COTI/USDT, EPIC/USDT, and AEVO/USDT remain absent from all three of tonight's fresh crypto reports' price/technical sections, despite each having an open B-tier position per `active-signals`. XRP/USDT appears only via news-feed mentions (catalyst risk), not price/technical data.
- **evidence:** `active-signals --asset-class crypto` shows `sig_06b6c2801005f29d` (COTI), `sig_f6259f2dfc6f2f63` (EPIC), `sig_bd5eb3cef514b1bf` (AEVO) all still open (`triggered`); grep for "COTI|EPIC|AEVO" across tonight's scalp/intraday/swing reports returns no matches.
- **suggested manual fix:** add a read-only CLI command (or extend `active-signals`) that surfaces last-known current price / invalidation-distance for any symbol with an open signal, independent of whether that symbol appears in the latest scan-cycle's top-N deep-analysis report.
- **priority:** high
- **first observed:** 2026-08-03 21:40 EEST (confirmed persisting 23:15 and again this 04:43 cycle — fourth consecutive confirmation)

### TODO-catalyst-mapping-weak (priority: medium, improved but still open)
- **issue:** Catalyst symbol-mapping coverage is 46.8% mapped / 53.2% unmapped this run — still above the 50% weak-mapping threshold, though improved from the 71.5% unmapped figure cited in the prior two-cycle read.
- **evidence:** direct read of `data/catalysts/2026-08-04/catalyst_events.jsonl` — 234/500 events have a non-null symbol field, 266/500 do not (top unmapped: IPO pricing announcements, a Reuters/Ipsos political poll, a corporate notes offering — none crypto-relevant).
- **suggested manual fix:** continue tracking the symbol-resolver improvement work already in progress per prior-cycle TODOs; re-check trend over the next several cycles before deciding whether it's stabilizing above or below the 50% line.
- **priority:** medium
- **first observed:** carried forward, originally flagged in earlier cycles at 71.5%

### TODO-weekend-flag-labeling-check (priority: low, new this cycle)
- **issue:** Active signals HOME/USDT and XRP/USDT show `weekend=Y` in `active-signals --asset-class crypto` output despite the current date (2026-08-04) being a Tuesday.
- **evidence:** CLI table column `weekend` = `Y` for `sig_57d425cf4bc41003` (HOME) and `sig_10088a4c71cae845` (ALLO) among others; likely reflects the original signal-entry timestamp falling on a weekend rather than a live bug, but this was not independently verified this cycle.
- **suggested manual fix:** confirm the `weekend_mode` field is computed from entry-time rather than current-time (expected behavior) — if so, no fix needed, just a naming/documentation clarification; if it's computed from current time, this is a live bug affecting the weekend-mode performance cohort in `signal-stats`.
- **priority:** low
- **first observed:** 2026-08-04 04:43 EEST (this cycle)
