# Opus Enriched Review — Crypto Overnight / Asia Review — Auto Cycle 04:45 EEST

## 1. Executive Summary
Slot: **crypto overnight / Asia review** (04:30 EEST). Advisory only / no auto-trade. BTC/ETH are in downtrend across scalp/intraday/swing scans; macro risk score is 91.6/100 (risk-off) after the Hormuz reopening narrative collapsed on Trump's 50-year-compensation demand from Iran — externally confirmed (Brent >$89, BTC -1.68% 24h). Zero A/B-tier crypto setups fired this cycle across all three modes; the only "action" is one already-open intraday win (BICO/USDT +1.0R) and a batch of swing signals closing flat/unresolved. Stocks are closed (bullish/risk-on regime carried forward, planning only). The most important finding this run is **not a new trade** — it's a confirmed, currently-live instance of the previously-flagged invalidation-monitoring gap: TUT/USDT's open "triggered" long has price trading ~33% below its own invalidation level while still shown as an active position (see §10, §14).

## 2. Data Used
- Reports: scalp (03:24), intraday (03:34), swing (04:37, freshest — fresh), stocks intraday (04:07, fresh; market closed). Stocks swing/invest excluded — deprecated, last data >6 weeks old (2026-07-02).
- Catalyst layer: `data/catalysts/2026-08-13/` (cycle_00-41, generated 03:41 EEST — fresh).
- LLM packets: `llm_analysis_packet.md` (03:35), `llm_stocks_packet.md` (04:09).
- CLI: `active-signals` ×2 (crypto/stocks), `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-08-13`.
- Direct read-only SQL: `proposed_signals` rows for TUT/USDT, HEI/USDT; `signal_outcomes` for overnight batch resolutions; `watchlist_alerts` schema check.
- External: 3 WebSearch queries (BTC/ETH overnight price action, XRP bridge exploit status, Iran/Hormuz macro). No WebFetch needed — search snippets were sufficient and consistent with internal data; no fabricated observations made.

## 3. Scheduler / Data Freshness
- Scheduler: **fresh** — `scheduler.log` last write 04:45:22 EEST (mid-cycle, actively running: "track-signals (post)" in progress at write time).
- Latest cycle summary: `cycle_02_23-40_summary.md` (01:14 EEST) — cycle 3 running now, not yet summarized.
- Swing report: 04:37 EEST — **fresh** (<4h, in fact ~8 min old).
- Intraday: 03:34 EEST — fresh. Scalp: 03:24 EEST — fresh.
- Stocks intraday: 04:07 EEST — fresh, but market-closed flag active (`MARKET CLOSED — planning / watchlist only`), all entries demoted to C.
- Catalyst JSONL: 03:41 EEST — fresh (~1h old).
- No monitor/paper-status file found beyond scheduler.log; not blocking.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-08-13 04:45 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["scheduler_fresh", "report_stale", "onchain_config_missing"],
      "data_missing": ["HEI/USDT current price not present in this cycle's scan universe"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mid-cycle 04:45", "swing report 04:37 fresh", "stocks swing/invest last dated 2026-07-02"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.8,
      "reason_codes": ["risk_off", "chop", "shorts_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/ETH downtrend all 3 crypto modes", "macro risk 91.6/100 risk-off", "altcoin breadth 45.5% above EMA20", "external: Hormuz deal collapse, BTC -1.68% 24h, Brent $89"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "no_catalyst", "stale_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 120/500 mapped = 76.0% unmapped", "5 narrative baskets, ai_narrative + momentum_breakout freshest (<1h)", "XRP bridge exploit is 4 days old, external search confirms price held $1, contained third-party bridge issue"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.4,
      "reason_codes": ["data_unavailable", "oi_supports"],
      "data_missing": ["cross-exchange OI/funding for most watchlist names (futures data unavailable for SPCXB, KORUB, NIL, SKHYB, NBISB)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["NIL/USDT: price up + OI down = short covering", "COTI/USDT: price up + OI up = fresh positioning", "BANK/USDT: price up + OI down = short covering"] },
    { "agent": "technical_entry", "verdict": "watch", "confidence": 0.6,
      "reason_codes": ["stale_before_entry", "clean_retest", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["all C-tier ideas below active-trade score threshold", "NIL/USDT pullback zone unconfirmed carried 2+ cycles", "MMT/USDT short-watch retest zone 0.1872-0.1897 vs current 0.1861 (already inside/through zone)"] },
    { "agent": "execution_lifecycle", "verdict": "manual_review", "confidence": 0.75,
      "reason_codes": ["needs_review", "entered_unresolved", "closed_flat"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["active-signals crypto: 0 A-tier, ~48 B-tier mostly status=triggered/tp1_hit/waiting_for_entry", "signal_outcomes 01:44 UTC batch: 1 win (BICO intraday +1.0R), ~18 expired/not_triggered at 0.0R (entered-unresolved/no-entry mix)", "untracked-legacy detector: none found today"] },
    { "agent": "risk_manager", "verdict": "bad", "confidence": 0.85,
      "reason_codes": ["manual_review", "correlation_cluster"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TUT/USDT proposed_signals row sig_e4875989af64bab7: status=triggered, invalidation=0.09883, updated_at 2026-08-09 (4d stale); this cycle's fresh scan shows TUT/USDT current price 0.0665 — ~33% below its own invalidation level", "HEI/USDT sig_a4e763ceaf1df917: status=triggered, invalidation=0.18750, updated_at 2026-08-08 (5d stale), symbol absent from current scan universe so live price could not be cross-checked this run"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.6,
      "reason_codes": ["playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing mode: 14d PF 5.84, avgR 0.50, sample=100 reliable", "crypto scalp mode: PF 1.85 but only 1 win / 3 losses, weak edge", "stocks A/B headline: sample=11 weak confidence, PF 0.0, avgR -0.5 (n too small to act on)"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "shorts",
    "best_long_candidate": { "symbol": "BANK/USDT", "trigger": "1h close and hold above 0.0403 pullback zone (0.0378-0.0384) with volume confirmation and BTC not making a new downtrend low", "reason": "cleanest RS-leader in the swing scan (score 63.5, RS +10.52% vs BTC) despite broad risk-off tape; still below active threshold" },
    "best_short_candidate": { "symbol": "MMT/USDT", "trigger": "failed bounce/rejection inside 0.1872-0.1897 retest zone, invalidated only above 0.1928", "reason": "downtrend, negative RS -10.51%, price already trading inside the conditional retest zone (0.1861); note an older triggered short on this same symbol is already open and working — this is a watch for continuation/confirmation, not a fresh add" },
    "best_catalyst_candidate": { "symbol": "none", "trigger": "a fresh (<6h), symbol-mapped catalyst on an RS-leader — none of today's C-tier ideas (BANK, MMT, BMT, COTI, VIRTUAL, NIL, BICO, KORUB, HOLO, TUT) carry a verified fresh catalyst this cycle", "reason": "catalyst mapping is 76% unmapped this run; XRP's exploit is real but 4 days old, contained to a third-party bridge, and price already absorbed it ($1 floor held per external confirmation) — not a fresh trigger" },
    "avoid_candidate": { "symbol": "TUT/USDT (existing open position)", "reason": "status=triggered in DB but current scanned price (0.0665) is ~33% through its own recorded invalidation (0.0988) with no stop/expire event recorded in 4 days — data integrity issue, not a trade signal; treat the position as needs-review, do not rely on its displayed status" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.70 | scheduler_fresh, report_stale, onchain_config_missing | advisory_only |
| market_regime | caution | 0.80 | risk_off, chop, shorts_preferred | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, no_catalyst, stale_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.40 | data_unavailable, oi_supports | advisory_only |
| technical_entry | watch | 0.60 | stale_before_entry, clean_retest, wait_for_trigger | advisory_only |
| execution_lifecycle | manual_review | 0.75 | needs_review, entered_unresolved, closed_flat | advisory_only |
| risk_manager | bad | 0.85 | manual_review, correlation_cluster | advisory_only |
| playbook_performance | ok | 0.60 | playbook_working, low_sample | advisory_only |
| head_trader (synthesis) | caution | 0.65 | — | advisory_only |

## 4. What Changed vs Previous Review
Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-12_2329.md` (23:32 EEST, post-close final daily review).
- **NIL/USDT long-watch: carried forward, still unconfirmed.** Same pullback zone logic (now 0.0412-0.0420 / invalidation 0.0403 vs prior 0.0410-0.0418 / ~0.0401-0.0411) — price has not triggered across two full cycles.
- **KAITO/USDT short-watch from the prior review is gone** — not present in this cycle's C-tier lists (dropped out of the scan or promoted/demoted elsewhere); no longer trackable as a live idea.
- **PROM/USDT open swing long (flagged as "monitor, don't add" last review) has now resolved** — `signal_outcomes` shows it `expired` at 0.0R in the 01:44 UTC batch check (entered-unresolved, no TP/SL before window, not a missed entry).
- **MMT/USDT (short, triggered) persists** from last review, still unresolved, now sitting well in-the-money on current price relative to its invalidation (0.1861 vs 0.2069) — genuinely working, not degrading.
- **TUT/HEI invalidation-status integrity gap is now confirmed with a live price check** (6th consecutive review to flag it, but the first with hard numeric confirmation of a breach — TUT/USDT price 0.0665 vs invalidation 0.0988). This is materially worse than "unresolved," it's now "confirmed wrong."
- **Untracked-alert detector is clean today** (prior review noted a recurring PROM/USDT instance; not reproduced this run — may be transient, keep watching).
- **Catalyst mapping weakened further**: 76.0% unmapped this cycle vs 73.1% in the prior review.
- **CSCO after-hours thesis from prior review** is now moot — no CSCO entries in current stocks C-tier list; market is closed and pre-US-open slot (16:20) will re-evaluate.

## 5. Catalyst Coverage
- Total catalyst_events today: **500**. Mapped (symbol present): **120**. Unmapped: **380** (**76.0%**).
- Narrative baskets: **5** (ai_narrative <1h, binance_ecosystem_teaser <6h, perps_dex_narrative <6h, rwa_narrative <24h, momentum_breakout <1h).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines:
  1. "LATEST: Kalshi says it has become the first prediction market to distribute real-time order book data over a dedicated..." (t.me feed, no symbol tag)
  2. "LATEST: Wintermute plans to invest up to $1B in AI data center infrastructure and high-frequency trading over the next..." (t.me feed, no symbol tag)
  3. "UPDATE: FlightAware dropped its lawsuit against Kalshi just one day after filing it over alleged misuse of its flight..." (t.me feed, no symbol tag)
- By type: other_news 471, earnings_event 8, legal_risk 8, partnership 4, exploit_hack 3, product_launch 2, insider_activity 2, buyback_burn 1, analyst_action 1. The legal_risk cluster is almost entirely generic PR-Newswire class-action-lawyer solicitations (Capricor, Genius Group, Wise, Pentair, Wix, Alarum, Jefferies, Blaize) — routine ambulance-chasing ads, not fresh company-specific developments; treated as noise, not a headline-risk trigger for any current candidate.

## 6. Market Landscape

BTC and ETH are in downtrend across scalp, intraday, and swing scans (consistent read all three modes). Altcoin breadth: 44-45% above EMA20, 48-53% above EMA50 — a chop/mixed tape, not a clean trend down. Macro risk score 91.6/100, risk-off, driven by the Strait of Hormuz negotiation collapsing overnight (Trump's 50-year compensation demand from Iran killed deal talk) — externally confirmed: Brent crude jumped to $89.08 (+12% w/w), BTC -1.68% 24h. Volatility is normal (ATR percentile 23-26%), not a panic regime — this is grinding risk-off, not a crash.

XRP carries a real but contained catalyst: a third-party bridge (tx/Coreum on XRPL) was exploited Aug 9 for ~198,700 XRP (~$200K), bridge halted, vulnerability identified and patched, FBI IC3 complaint filed, XRP Ledger itself unaffected. Externally confirmed XRP held its $1 floor through the event — this is a 4-day-old, already-priced-in story, not a fresh trigger; no XRP signal exists in the active book.

Stocks are closed (04:45 EEST is well outside RTH). Carried-forward regime from the latest stocks intraday report: **bullish, risk-on**, VIX 14.55 (low), breadth 100% above EMA20/50, all 4 major indices in uptrend. Strongest sectors: energy (XLE, RS +5.68%), healthcare (XLV, RS +4.07%). Weakest: utilities, communications, semiconductors (mixed-to-weak). This is planning/watchlist context only for the upcoming Europe (11:30) and pre-US-open (16:20) slots — not actionable now.

### Market Mood / Risk Routing
- Crypto mood: **risk-off / chop**
- Stocks mood: **closed** (carried-forward bullish/risk-on)
- Dominant narrative: AI sector rotation (NEAR/RENDER/TAO/FET, <1h fresh) and a pure-momentum cluster (KORUB/SKHYB) with no confirmed catalyst
- Preferred side now: **shorts / wait-for-trigger** (longs only if RS-leader + confirmed hold, per PART 2 chop routing)
- Best long candidate: BANK/USDT — none active, trigger: 1h close above 0.0403 with volume
- Best short candidate: MMT/USDT — watch for failed-bounce rejection in 0.1872-0.1897 (existing open short already working, this is confirmation not a fresh add)
- Best catalyst-backed candidate: none clean — trigger: a fresh (<6h) symbol-mapped catalyst on an RS-leader
- What to avoid: chasing any C-tier idea below active-trade threshold into a downtrending BTC/ETH tape; treating TUT/USDT's "triggered" status at face value
- What would change the view: BTC/ETH reclaiming the recent range highs, a Hormuz de-escalation headline, or altcoin breadth pushing back above 55-60% on EMA20

## 7. Candidate Deep Dives

### BANK/USDT (crypto swing, C-tier watchlist, long)
- Has price already reacted to the catalyst? No fresh verified catalyst exists for this symbol — the move is pure RS/momentum (24h +9.94%, RS +10.52% vs BTC).
- Chasing? Not yet — price (0.0387) is above the conditional pullback zone (0.0378-0.0384), so a fresh long here would be buying above the planned entry, i.e. mild chase risk.
- Retest/pullback structure? Yes, a defined pullback zone exists; unconfirmed this cycle.
- Overextended (>2 ATR from EMA20)? ATR 0.0013, current price 0.0387 vs support 0.0341/resistance 0.0403 — inside range, not extended.
- Would entry now be late? Only if buying the current price outright rather than waiting for the pullback.
- Actionable level: 1h close/hold in 0.0378-0.0384 with volume.
- Aligned with market mood? Partially — it's a long against a risk-off/downtrend BTC backdrop, which is the higher-risk side of PART 2's routing; only justified by genuine RS leadership, so treat as a counter-trend long-watch, not a mood-aligned trade.
- Long/short/wait: wait-for-trigger.
- Actionable now or after confirmation? After confirmation (pullback hold + BTC stabilizing).
- Invalidator: 1h close beyond 0.0371 if activated, or a fresh BTC downtrend leg.
- Chase-risk setup? Yes, mild, at current price.
- Catalyst confirmation/contradiction? Neither — no catalyst attached.

### MMT/USDT (crypto swing, existing open short + new C-tier watchlist idea, short)
- Two live artifacts on this symbol: an older B-tier swing short (`triggered`, entry ~0.202-0.204, invalidation 0.2069, currently well in-the-money at 0.1861) and this cycle's fresh C-tier watchlist short idea (retest zone 0.1872-0.1897, invalidation 0.1928, TP1 0.1805).
- Has price reacted to the catalyst? No catalyst — pure technical downtrend (24h -11.08%, RS -10.51% vs BTC).
- Chasing? No — price is already inside the proposed retest zone, this is the textbook setup, not a chase.
- Retest structure? Yes, explicitly a failed-bounce/retest thesis.
- Overextended? ATR 0.0056, current 0.1861 vs support 0.1784/resistance 0.2053 — not extended.
- Actionable level: rejection inside 0.1872-0.1897.
- Aligned with mood? Yes — clean risk-off-aligned short in a downtrend symbol.
- Long/short/wait: short, watch for rejection confirmation (existing open short is not a fresh entry signal).
- Invalidator: reclaim/close above 0.1928 (watchlist idea) or 0.2069 (existing open short's own invalidation).
- Chase-risk: no.
- Catalyst: none — pure RS/momentum thesis, funding slightly negative (-0.00022) suggesting shorts not yet crowded.

### TUT/USDT (crypto — DATA INTEGRITY FLAG, not a trade idea)
- DB row `sig_e4875989af64bab7`: symbol=TUT/USDT, status=**triggered**, direction=long, entry 0.12303-0.14284, invalidation=**0.09883**, updated_at=2026-08-09T17:01:44 (stale, 4 days).
- This cycle's fresh swing scan (independently generated, unrelated to the stale DB row) shows TUT/USDT current price = **0.0665**, ATR 0.0053, support 0.0613.
- 0.0665 is roughly **33% below** the recorded invalidation level of 0.0988. A long triggered at 0.123-0.143 with a hard invalidation at 0.0988 should have been stopped out days ago; it is still displayed as an open `triggered` position.
- Not a trade idea — a monitoring-pipeline defect. Do not treat this position as a valid open risk exposure in any downstream read. See §10/§14.

### HEI/USDT (crypto — same integrity pattern, unconfirmed this cycle)
- DB row `sig_a4e763ceaf1df917`: status=triggered, invalidation=0.18750, updated_at=2026-08-08T05:43:12 (5 days stale).
- Symbol did not appear in this cycle's swing/intraday scan universe, so the current price could not be cross-checked this run — flagged as the same suspected pattern as TUT/USDT but unconfirmed by a live price this time.

### BICO/USDT (crypto intraday — resolved, informational only)
- Closed **win, +1.0R** in the 01:44 UTC batch outcome check (intraday mode). No further action; genuine confirmed win, not touch-based inflation concern since intraday R realizations here are smaller/cleaner than swing.

## 8. Best Candidates Ranked
1. **MMT/USDT short-watch** (crypto) — cleanest mood-aligned setup: downtrend, negative RS, price already inside the failed-bounce retest zone (0.1872-0.1897). Not a fresh add given an existing open short on the same name; watch for rejection confirmation only. Invalidator: close above 0.1928.
2. **BANK/USDT long-watch** (crypto) — counter-trend RS leader, needs the 0.0378-0.0384 pullback to hold with volume before it's anything but a chase. Invalidator: 1h close beyond 0.0371, or BTC making a fresh downtrend low.
3. **NIL/USDT long-watch** (crypto) — carried forward two cycles unconfirmed, pullback zone 0.0412-0.0420, invalidation 0.0403. Lowest priority of the three watchlist names since it still hasn't triggered.
4. **TUT/USDT — needs review, not a trade candidate** — existing "open" position with a confirmed invalidation breach in the monitoring data; surfaced here because ignoring it would misstate current book risk.
5. Catalyst-watch: **none clean** — trigger would be a fresh (<6h), symbol-mapped catalyst on an RS-leader; nothing in today's 120 mapped events qualifies for a live candidate.

## 9. Avoid / No Trade
This applies to the current decision window only — never a command to stop scanning, tracking, or the scheduler.
- **Any fresh long chase in the current BTC/ETH downtrend** without a confirmed pullback hold — regime and macro risk (91.6/100 risk-off) argue against it.
- **XRP/USDT in either direction** — catalyst is real but stale (4 days) and already absorbed by price; no edge in trading the old news.
- **All stocks C-tier ideas** (LMT, ORCL, DELL, CSCO, etc.) — market closed, entries demoted to C by design, not actionable until RTH confirmation.
- **Treating TUT/USDT's displayed `triggered` status as valid risk** — the position is functionally invalidated per current price but not marked as such in the system; do not use it to gauge open exposure.
- **Chasing MMT/USDT below the retest zone** — wait for the rejection, not the initial move already in progress.

## 10. Main Risks
- **Invalidation-monitoring integrity gap — now confirmed with a live price breach (TUT/USDT, 6th consecutive review flagging this pattern)**: a `triggered` long position sits ~33% through its own invalidation level with no stop/expire event recorded in 4 days. This directly undermines the reliability of every "active signals" and "open risk" read produced by this system. HEI/USDT carries the same stale-`updated_at` signature but could not be price-confirmed this cycle.
- **Catalyst mapping degrading**: 76.0% unmapped this run vs 73.1% in the prior review — a two-review trend in the wrong direction, not a one-off.
- **Macro risk-off backdrop (91.6/100)** driven by a live, fast-moving geopolitical story (Hormuz/Iran) — externally corroborated but subject to rapid reversal (the narrative already flipped from optimistic to risk-off within the same week per search results); treat any regime read as provisional until the next cycle.
- **Stocks A/B headline sample is too small to trust** (n=11, weak confidence, PF 0.0) — not a live risk today since market is closed, but a reminder the stocks-intraday edge claim needs more data before the next RTH session.
- **HEI/USDT price unconfirmable this cycle** — the symbol has dropped out of the scan universe entirely, which is itself a minor data-completeness concern for anything still open on it.

## 11. Action Plan — next 4 hours
- Watch MMT/USDT for a rejection print inside 0.1872-0.1897 (short continuation) — no action needed if it doesn't materialize, this is confirmation-only.
- Watch BANK/USDT for a pullback hold in 0.0378-0.0384 with volume before considering it anything but chase risk.
- No new stocks action until RTH — the 11:30 Europe/pre-US slot will re-baseline the watchlist.
- Flag TUT/USDT (and check HEI/USDT again once it reappears in the scan universe) for manual review — not an automated fix, a human should verify actual current price against the recorded invalidation and correct the DB row if the breach is confirmed.
- Re-check catalyst mapping trend at the next cycle; two consecutive reviews above 70% unmapped is worth a maintenance look (see §14).

## 12. Final Verdict per Mode
- **Crypto scalp**: no trade for new ideas; nothing worth watching this cycle ("Nothing worth stalking yet" per report). Report is fresh (03:24).
- **Crypto intraday**: no new A/B; one resolved position closed **CLOSED WIN +1.0R** (BICO/USDT). Watchlist carries BMT/COTI/BANK/VIRTUAL/NIL/PROM, none scoring above threshold.
- **Crypto swing**: strongest lane by weekly stats (14d WR 72%/PF 5.84, though touch-based R likely overstates realized edge — known caveat). Zero A/B this cycle. MMT/USDT short and BANK/USDT long are the cleanest watchlist names. TUT/USDT integrity issue needs resolution before its "open" status can be trusted.
- **Stocks intraday**: market **CLOSED** — all 50 active signals are C-tier `waiting_for_entry`, non-actionable by design. Regime carried forward as bullish/risk-on (VIX 14.55) for planning into the 11:30/16:20 slots.
- **Stocks swing/invest**: excluded — deprecated data source, last dated 2026-07-02.
- **Overnight paper-trading outcome (01:44 UTC batch check)**: crypto — 1 win (+1.0R, BICO intraday), remainder of the batch resolved as **entered-unresolved / no-entry** at 0R display (not losses), consistent with an overnight session with no fresh triggers rather than a losing session.
- **System integrity**: **manual review required** — TUT/USDT invalidation breach now confirmed by live price this cycle; catalyst mapping trending weaker (76.0% unmapped, up from 73.1%); untracked-alert detector is clean today (no PROM/USDT recurrence this run).

## 13. Sources
- [Bitcoin and ethereum prices today, Wednesday, August 12, 2026 — Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-wednesday-august-12-2026-crypto-prices-rise-with-cpi-report-on-deck-121022039.html)
- [XRP bridge exploit update: tx identifies flaw, alerts FBI — crypto.news](https://crypto.news/xrp-bridge-exploit-update/)
- [Ripple news: XRP bridge drained after software mistook fake deposits for real ones — CoinDesk](https://www.coindesk.com/tech/2026/08/12/xrp-bridge-drained-for-usd200-000-after-software-mistook-fake-deposits-for-real-ones)
- [XRP Defends $1 Floor as Record $2.7B Derivatives Bets Collide With Bridge Hack — Tech Times](https://www.techtimes.com/articles/324207/20260812/xrp-defends-1-floor-record-27b-derivatives-bets-collide-bridge-hack.htm)
- [Bitcoin (BTC) price stuck below $65,000 as Iran stalemate, Strategy sale squeeze market — CoinDesk](https://www.coindesk.com/markets/2026/08/11/bitcoin-stuck-below-usd65-000-as-the-strait-of-hormuz-stalemate-and-strategy-s-selling-squeeze-the-market)
- [Bitcoin Steadies Above $65,000 as Iran-Oman Deal Talk Eases Hormuz Concerns — PrimeXBT](https://primexbt.com/news/bitcoin-steadies-above-65000-as-iran-oman-deal-talk-eases-hormuz-concerns/)

## 14. Fix Requests / TODO

### TODO-tut-hei-invalidation-breach
- **issue:** `proposed_signals` rows for TUT/USDT (`sig_e4875989af64bab7`) and HEI/USDT (`sig_a4e763ceaf1df917`) remain `status=triggered` despite `updated_at` being 4-5 days stale; this cycle's live swing scan confirms TUT/USDT's current price (0.0665) is ~33% through its recorded invalidation (0.0988) with no stop/expire event logged. This is the 6th consecutive scheduled review to flag this pattern (first suspected 2026-08-12 11:39 EEST), now confirmed with hard numbers.
- **evidence:** DB query `SELECT signal_id, symbol, status, invalidation, updated_at FROM proposed_signals WHERE symbol IN ('TUT/USDT','HEI/USDT')` on `db/crypto_ai_desk.sqlite`; cross-checked against `data/reports/swing/2026-08-13_01-37_swing_report.md` Trade Idea #10 (TUT/USDT desk notes, current price 0.0665).
- **suggested manual fix:** Audit the invalidation-monitoring / signal-tracking job for why `status=triggered` rows aren't transitioning to `stopped`/`invalidated` when price crosses the recorded invalidation level; specifically check if the tracker is silently failing for these two signal_ids (or their symbol) rather than a systemic bug across all rows, since most other `triggered` rows in `active-signals` do show recent `updated_at`/status churn.
- **priority:** high
- **first observed:** 2026-08-12 11:39 EEST (suspected); 2026-08-13 04:45 EEST (confirmed with live price)

### TODO-catalyst-mapping-trend
- **issue:** Catalyst→symbol mapping coverage has degraded across two consecutive reviews: 73.1% unmapped (2026-08-12 23:29) → 76.0% unmapped (2026-08-13 04:45). If this continues, the catalyst layer becomes context-only noise rather than a usable signal input.
- **evidence:** `data/catalysts/2026-08-13/catalyst_events.jsonl` — 500 total events, 120 mapped (symbol field populated), 380 unmapped; dominated by `other_news` (471/500) which appears to be the category least likely to carry a resolvable symbol.
- **suggested manual fix:** Review the symbol-resolver logic for the `other_news` catalyst type specifically — sample unmapped headlines suggest many DO reference tickers/companies in free text (e.g. "$AAPL", "Kalshi", "Wintermute") that a stronger resolver could catch.
- **priority:** medium
- **first observed:** 2026-08-12 23:29 EEST (73.1%), confirmed worsening 2026-08-13 04:45 EEST (76.0%)

### TODO-hei-scan-universe-gap
- **issue:** HEI/USDT dropped out of the swing/intraday scan universe this cycle, preventing a live price cross-check against its stale `triggered` DB status (see TODO-tut-hei-invalidation-breach). Not necessarily a bug — could be a liquidity/volume filter — but worth confirming it isn't masking the same invalidation-breach pattern as TUT/USDT.
- **evidence:** `grep -n "HEI/USDT" data/reports/swing/2026-08-13_01-37_swing_report.md` returns no matches; `grep -n "HEI/USDT" data/reports/intraday/...` also empty this cycle.
- **suggested manual fix:** Check why HEI/USDT fell out of the binance/bybit/mexc scan universe (liquidity filter threshold, delisting, or a fetch failure) and confirm its actual current price against invalidation 0.18750 via a manual price check.
- **priority:** medium
- **first observed:** 2026-08-13 04:45 EEST
