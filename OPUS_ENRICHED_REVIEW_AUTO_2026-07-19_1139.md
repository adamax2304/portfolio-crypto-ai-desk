# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:39 EEST

## 1. Executive Summary

**Slot: Europe / pre-US context (11:30 window).** Advisory only — no auto-trade, no scoring/threshold/routing changes made or implied. Crypto desk carried 11 active B-tier signals into this slot; 8 are open-actionable and running well (TRUMP, LTC, ETH-intraday, ETHFI, HOME, CASHCAT, XLM, ALLO all at tp1/tp2/triggered), 2 waiting for entry (ETH-swing, ZEC), and 1 (NEAR scalp short) is a stale bookkeeping item now **44h+ past expiry unresolved** — needs review, not a live risk. The correlation cluster flagged in the prior review (ALLO×4, BANK×3 concurrent signals) has **self-resolved**: BANK has zero active signals now and ALLO is down to one. External verification confirms the macro overhang is real and escalating — US struck ~90 Iranian targets July 13–14, Iran hit US positions in Syria, Strait of Hormuz still closed, Brent near $79, and **BTC has fallen into the low-$60Ks**, which sits awkwardly against the internal swing engine's "bullish trend / risk-on" regime read from stale 01:45 UTC data — treat that regime label as macro-fragile. BANK/USDT's fresh swing candidacy (score 65.7) is externally confirmed to be a **no-catalyst speculative pump that already round-tripped -29%/24h, -35.7%/7d** — stays AVOID. ETH remains the cleanest catalyst-backed long (Bitmine at 4.8% of ETH supply, still buying). Catalyst mapping is weak this cycle (30.2% mapped) — use catalyst layer as context only.

## 2. Data Used

- Reports: scalp (09:29), intraday (09:36), swing (04:47) — all crypto, fresh-to-carry-forward.
- Stocks: intraday (Jul 18 00:56, market-closed/all-fetch-failed run), swing (Jul 2, 17d stale/deprecated), invest (Jul 2, 17d stale/deprecated) — planning-only, weekend, US cash market closed.
- Catalysts: `data/catalysts/2026-07-19/catalyst_events.jsonl` (1750 events today), `narrative_baskets.jsonl` (5 baskets), latest `catalyst_cycle_06-38.md`.
- LLM packets: `llm_analysis_packet.md` (09:36, fresh), `llm_stocks_packet.md` (Jul 17 14:25, stale).
- CLI: `active-signals` ×2, `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-07-19` (clean, no findings).
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-19_0440.md` (crypto overnight/Asia slot).
- External: 6 WebSearch queries (BANK/Lorenzo, ETH/Bitmine, Iran/Hormuz macro, CLARITY Act, BTC spot price, NEAR catalysts), sources ingested via `scripts.ingest_enriched_review_sources` (7/7 valid, written to `news_items`).

## 3. Scheduler / Data Freshness

- `scheduler.log` + `cycle_03_09-21_summary.md`: mtime **09:52**, ~1h47m old at run time (11:39) — well under the 3h defer threshold. **Not deferred.**
- Standalone monitors active past the scheduler cycle: `crypto_monitor` log active to 11:26, `derivatives_monitor` log active to 11:40 — confirms the watchdog/monitor loop is alive independent of the cycle scheduler.
- `pending_monitor`: leader-election lock held by a separate process (PID 4184); this instance exited cleanly (no double-run) — healthy.
- Scalp/intraday reports: fresh (~2h old at generation, ~2.1-2.2h old now). Swing report: ~7h old at run time — inside the 4-12h carry-forward band, used with that flag.
- Stocks intraday: >24h stale, all-fetch-failed run, planning-only. Stocks swing/invest: 17 days stale and **deprecated playbooks** (0× sizing weight) — included only as inert watchlist context, excluded from any actionable verdict.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-07-19 11:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["stocks intraday fetch (0/84 symbols ok on last run)", "unmapped-headline sample for §5"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log/cycle_03 mtime 09:52", "swing report 7h old (carry-forward band)", "stocks intraday all-fetch-failed Jul 17"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["mixed", "chop", "wait_for_trigger"],
      "data_missing": ["live BTC/ETH OHLCV newer than 06:30 UTC internal snapshot"],
      "suggested_effect": "advisory_only",
      "facts_used": ["internal swing regime says bullish/risk-on from 01:45 UTC data", "external: BTC fallen to low-$60Ks amid Iran escalation as of Jul 17-19", "scalp/intraday regime reads range/chop"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.45,
      "reason_codes": ["mapping_weak", "stale_catalyst", "catalyst_contradicted", "narrative_supported"],
      "data_missing": ["unmapped headline titles not sampled this run"],
      "suggested_effect": "advisory_only",
      "facts_used": ["529/1750 catalyst_events mapped = 30.2%, unmapped 69.8%", "CLARITY Act basket importance 0.66 'nearing finalization' vs external: stalled, ~43% odds, no floor vote scheduled", "NEAR has genuine external catalysts (v2.13.0 upgrade, fixed-supply proposal) distinct from the known substring-match bug"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.3,
      "reason_codes": ["data_unavailable"],
      "data_missing": ["funding/OI/liquidation data not surfaced in read internal files this run"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BANK external source: $723K liquidations 24h, $504K short-side, but not tied to our specific position"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["entry_fresh", "clean_retest", "overextended", "chase_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ETH swing waiting_for_entry 1854.44-1857.65, current ~1859 (essentially at entry, not chased)", "BANK swing entry 0.1080-0.1124 sits mid a parabolic move that already reversed externally", "XLM triggered, ZEC waiting_for_entry"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["8 open-actionable (TRUMP tp2, LTC triggered, ETH-intraday tp2, ETHFI tp1, HOME tp2, CASHCAT triggered, XLM triggered, ALLO tp1)", "2 waiting_for_entry (ETH-swing, ZEC)", "1 needs_review: NEAR scalp short tp1_hit but 44h+ past expiry, unresolved bookkeeping (was 36h in prior review — growing)"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["headline_risk", "reduce_risk", "correlation_cluster"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Iran/Hormuz conflict live and escalating, BTC in low-$60Ks, risk-off headwind score 81-100/100 in internal reports", "BANK/ALLO correlation cluster from prior review has self-resolved (BANK 0 active, ALLO 1 active)", "detect_untracked_legacy_alerts clean today"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto_swing_narrative_rs_momentum 14d WR72%/PF5.80/+24R — driving TRUMP/LTC/ETH wins", "crypto_scalp low_confidence WR12%/PF0.14 — scalp correctly returning 0 A/B today", "live signal-stats week: crypto B-tier winrate 24.0%/PF1.08/totalR+2.20 (positive but thin); stocks B-tier winrate 36.4%/PF0.75/totalR-0.50 (negative, weekend/no-live-market)"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "catalyst_backed",
    "best_long_candidate":     { "symbol": "ETH/USDT", "trigger": "waiting_for_entry 1854.44-1857.65, invalidation <1850.53 — Bitmine still accumulating toward 5% of supply", "reason": "only candidate with an externally verified, ongoing institutional catalyst; not chased, entry essentially at market" },
    "best_short_candidate":    { "symbol": "DATA/USDT", "trigger": "no live signal — would need a clean break/retest below 0.0009-0.0010 on rising volume; currently capped by internal short-squeeze guard at score 56-59", "reason": "highest-scoring internal short idea in a risk-off tape, but capped below B by the desk's own squeeze filter — treat as watch-only until the cap lifts or price confirms" },
    "best_catalyst_candidate": { "symbol": "ETH/USDT", "trigger": "same as best-long — Bitmine accumulation is the cleanest verified catalyst on the board", "reason": "see above" },
    "avoid_candidate":         { "symbol": "BANK/USDT", "reason": "swing B-tier candidate (65.7) sits inside a confirmed no-catalyst speculative pump that already reversed -29%/24h and -35.7%/7d per external sources; internal volume ratio 0.19-0.33x confirms thin/low-conviction participation" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.65 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | caution | 0.50 | mixed, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.45 | mapping_weak, stale_catalyst, catalyst_contradicted, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.30 | data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | entry_fresh, clean_retest, overextended, chase_risk | advisory_only |
| execution_lifecycle | caution | 0.70 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, reduce_risk, correlation_cluster | advisory_only |
| playbook_performance | caution | 0.55 | playbook_working, playbook_failing, low_sample | advisory_only |
| **head_trader** | **caution (watch)** | **0.60** | synthesis of above | advisory_only |

## 4. What Changed vs Previous Review (04:40 crypto overnight/Asia)

- **Correlation cluster resolved**: BANK/USDT went from 3 concurrent signals to **0 active**; ALLO/USDT went from 4 concurrent to **1 active**. Prior review's TODO-4 (per-symbol concurrent-signal cap) is less urgent right now, though the underlying gap (no hard cap) is still unaddressed — kept as a TODO.
- **New signals since 04:40**: HOME/USDT (intraday B, already tp2_hit), XLM/USDT (swing B, triggered — rwa_narrative basket primary), ZEC/USDT (swing B, waiting_for_entry), CASHCAT/USDT (swing B, triggered).
- **XEC/USDT** — was the swing report's #1 strongest symbol (92.4) and best-long-watch candidate as of 04:47, but does not appear in the current active-signals table; likely resolved/expired between cycles or never promoted (entry/target prices in the swing report were themselves display-truncated to 0.0000 due to price-precision issues — a minor rendering bug worth a TODO).
- **Thesis confirmations**: TRUMP/USDT (04:40's #1 long-watch) advanced from triggered to **tp2_hit** — working as expected. LTC/USDT progressed from newly-added to **triggered**. ETH/USDT intraday leg also reached **tp2_hit**, reinforcing the ETH catalyst thesis carried from the prior review.
- **NEAR/USDT bookkeeping gap widened**: was ~36h past expiry unresolved at 04:40, now **44h+** past expiry (still tp1_hit, never formally closed) — TODO-2 escalated to high priority below.
- **BANK/USDT reclassification**: prior review flagged BANK as AVOID on pump-with-no-catalyst grounds without external verification; this run's external search **confirms** that call directly (see §7 deep dive) — the AVOID stands on stronger evidence now.
- **Macro**: prior review described "US-Iran conflict day 6"; external verification this cycle shows the conflict has escalated further (US struck ~90 Iranian sites Jul 13-14, Iran retaliated directly against US positions in Syria) — the risk-off overhang is not resolving, it is intensifying.

## 5. Catalyst Coverage

- Total `catalyst_events` today: **1750**. Mapped (non-null symbol): **529 (30.2%)**. Unmapped: **1221 (69.8%)**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (unmapped 69.8% > 50% threshold)
- Unmapped-headline sampling was not performed this pass (time-boxed to keep the review inside cycle) — logged as TODO-3 below rather than fabricated.
- `narrative_baskets.jsonl`: 5 baskets — ai_narrative (NEAR/RENDER/TAO/FET primary; contains the known NEAR substring-match contamination, see §7), perps_dex_narrative (HYPE primary), delisting_thin_liquidity (no symbols), rwa_narrative (ONDO/XLM primary — see §7 XLM deep dive on CLARITY Act overstatement), momentum_breakout (TLM/ALLO/HOME primary).
- Latest cycle (`catalyst_cycle_06-38.md`, 335 news_items scanned): top legal/regulatory items were TSLA Musk SEC settlement (0.77), 5× UNH DOJ Medicare-fraud-probe headlines (0.73 each), AVAV securities-fraud lawsuit (0.68) — all stocks-side, not crypto-actionable this weekend.

## 6. Market Landscape

Internal regime reads are split and stale: scalp/intraday call range/chop (06:15-06:30 UTC data), swing calls bullish/risk-on (01:45 UTC data, now ~10h old), and both scalp and swing internal macro-risk scores are elevated (81.3-100/100, risk-off headwind) citing the Iran conflict. External verification confirms the Iran/Hormuz escalation is real, ongoing, and has pushed BTC into the low-$60Ks — meaningfully below where the swing engine's "bullish trend" label would suggest. Treat the swing regime label as **macro-fragile carry-forward**, not a fresh confirmation.

### Market Mood / Risk Routing
- Crypto mood: **mixed / risk-off leaning** (internal breadth readings 50-56% EMA20 neutral-to-soft; external macro is unambiguously risk-off)
- Stocks mood: **closed** (weekend, no live RTH data; last live read Jul 17 was risk_off/VIX 19.16)
- Dominant narrative: momentum_breakout (TLM/ALLO/HOME, <1h fresh) and institutional ETH accumulation (externally verified) compete with a stale ai_narrative basket (NEAR, contaminated by a known substring-match bug) and an overstated rwa_narrative (XLM/ONDO, CLARITY Act framed as "nearing finalization" when it is actually stalled)
- Preferred side now: **catalyst-backed longs only; avoid chasing pumps**
- Best long candidate: **ETH/USDT** (waiting_for_entry, Bitmine accumulation verified)
- Best short candidate: **none clean** — DATA/USDT is the best short-watch but capped below B by the desk's own squeeze guard; needs a confirmed breakdown under 0.0009 on volume to re-qualify
- Best catalyst-backed candidate: **ETH/USDT**
- What to avoid: **BANK/USDT** (confirmed no-catalyst pump already reversed), fresh NEAR longs riding the ai_narrative basket (catalyst tagging contaminated), chasing anything already >2 ATR extended (BANK, TLM)
- What would change the view: a confirmed Hormuz reopening / de-escalation headline (risk-on unlock), or CLARITY Act reaching an actual floor vote (currently ~43% odds, no vote scheduled) would materially improve the RWA/XLM/ONDO thesis

## 7. Candidate Deep Dives

### 7.1 ETH/USDT — LONG, catalyst-backed (best candidate)
- Signal: swing B-tier, score 69.3, status **waiting_for_entry**, entry 1854.44-1857.65, invalidation <1850.53, TP1/2/3 1866.19/1873.31/1880.43. A second intraday leg (score 65.4) already hit tp2. Current price ~1859.07 (from swing report snapshot), i.e. essentially at the entry zone — not chasing.
- Has price reacted to the catalyst? Partially — Bitmine's accumulation has been running for weeks (steady buying since at least early July), it's a slow-burn institutional catalyst, not a one-day pop.
- Chase risk: low — entry zone is at-market, not extended.
- Retest/pullback structure: yes, ATR 7.12, entry sits within one ATR of current price.
- Overextended (>2 ATR from EMA20)? No indication of that in the report.
- Would entry now be late? No — this is a fresh, in-range entry.
- What would invalidate: 1h close below 1850.53, or confirmed news that Bitmine accumulation has paused/reversed.
- Aligned with market mood? Yes — this is the one long idea that doesn't depend on risk-on breadth; it rides a company-specific accumulation flow that has continued through the Iran-driven BTC selloff.
- Actionable now or after confirmation? Actionable now on a fill inside the stated entry band; no RTH/retest gate applies (crypto, always-on).
- Chase-risk setup? No.
- Catalyst confirmation or contradiction? **Confirmed** externally — Bitmine held 5.77M ETH (4.8% of supply) as of mid-July and continues buying weekly, per Bitmine's own July Chairman's Message and multiple independent outlets (FX Leaders, The Coin Republic).
- Legal/headline risk: none identified.

### 7.2 BANK/USDT — AVOID (confirmed no-catalyst pump)
- Swing report shows a fresh B-tier candidate, score 65.7, entry 0.1080-0.1124, current 0.1143, but scalp/intraday reports reject BANK outright (scalp: rejected 57.5 under kill-switch; intraday: C-tier only 52.2) and prior review already flagged AVOID.
- External verification (CoinGabbar, CoinMarketCap): BANK spiked +29.4% intraday to ~$0.0557 driven by speculative AI/Big-Data sector rotation, "no major announcements, new partnerships, or protocol updates directly explained the rally," volume +303% (speculative, not fundamental), and the coin has since **reversed -29.1% in 24h and -35.7% over 7 days**. Internal volume-ratio readings (0.19-0.33x average volume across reports) corroborate thin, low-conviction participation rather than a durable breakout.
- Has price already reacted to the catalyst? There is no real catalyst — the "reaction" is a leverage/momentum-chase cycle that already round-tripped.
- Chase risk: **high** — any long here would be buying into a confirmed reversal.
- Verdict: stays **AVOID**. Do not treat the swing report's fresh 65.7 score as new information; it is the tail of the same pump the prior review already flagged.

### 7.3 XLM/USDT — swing B, triggered — catalyst overstated
- Signal: swing B-tier, triggered, part of the rwa_narrative basket (primary symbol alongside ONDO). Basket freshness listed as "unknown."
- Catalyst read in `catalyst_cycle_06-38.md` scores CLARITY Act at 0.66 importance framed as "nearing finalization."
- External verification directly **contradicts** that framing: as of mid-July 2026 the CLARITY Act is **stalled in the Senate** — prediction-market odds have fallen from the low-70s to roughly 43%, no floor vote is scheduled, and outstanding disputes (ethics, federal preemption, SEC/CFTC seat-filling) remain unresolved. Advocates hope for a floor vote "as soon as the week of July 20," but that is aspirational, not confirmed.
- Aligned with market mood? Mixed — RWA is a legitimate multi-week narrative, but the specific catalyst cited to justify urgency is weaker than the internal importance score implies.
- What would invalidate: no specific technical invalidation level was captured in the gathered report excerpt for this signal; treat any adverse CLARITY Act news (further delay past August recess) as a thesis-weakening event.
- Verdict: **manual review** — the position can stay open on its own technical/RS merits, but do not add size on the CLARITY Act narrative until an actual floor vote is scheduled.

### 7.4 LTC/USDT — swing B, triggered — long-watch continuation
- Signal: swing B-tier, score 67.5, triggered, entry 46.618-46.848, invalidation <46.337. Part of `crypto_swing_narrative_rs_momentum` (14d WR72%/PF5.80/+24R) — the desk's best-performing active playbook.
- Correlated with TRUMP/USDT (same playbook, both currently working — TRUMP already at tp2_hit).
- Chase risk: low — already triggered at a defined entry, not chasing an extended move per available data.
- Legal/headline risk: none identified.
- Verdict: hold as long-watch continuation; the playbook backing it is statistically the strongest on the desk, but correlation with TRUMP means these two shouldn't be double-sized as if independent.

### 7.5 NEAR/USDT — scalp short, tp1_hit, 44h+ past expiry — needs review
- Signal expired 2026-07-17T15:56, tp1_hit recorded, never formally closed — now **44+ hours** past its expiry window (up from ~36h at the 04:40 review). This is a bookkeeping/lifecycle issue, not a live trading decision.
- Separately, the prior review's TODO-1 (a "near" substring-match bug tagging Iran-conflict headlines about "AREA NEAR HAJIABAD" into the ai_narrative basket) is unresolved and still contaminates NEAR's catalyst attribution.
- However, external research finds NEAR **does** have genuine, unrelated catalysts this month: the v2.13.0 network upgrade (post-quantum signatures, auto-resharding) went live July 13, and a fixed-supply governance proposal is circulating — both are real, verifiable, and distinct from the substring-match bug.
- Verdict: **needs review** on the stale signal itself (lifecycle hygiene); the substring-match bug should not be used to dismiss NEAR broadly, since it has legitimate catalysts running in parallel — but any *new* NEAR signal that cites the "ai_narrative" basket as its catalyst source should be manually checked against the real news, not trusted at face value.

## 8. Best Candidates Ranked

1. **ETH/USDT long** (waiting_for_entry 1854.44-1857.65, invalidation <1850.53) — best catalyst-backed idea on the desk.
2. **LTC/USDT long** (triggered 46.618-46.848, invalidation <46.337) — best playbook (WR72%/PF5.80), correlated with TRUMP.
3. **TRUMP/USDT** — already tp2_hit, thesis confirmed, let it run rather than treat as a fresh entry.
4. **XLM/USDT** — hold on technical merits only; do not add on the overstated CLARITY Act catalyst.
5. **Short-watch only, not yet actionable: DATA/USDT** — needs a confirmed breakdown under 0.0009-0.0010 on rising volume to clear the internal short-squeeze cap.

## 9. Avoid / No Trade

- **BANK/USDT** — confirmed no-catalyst pump already reversed -29%/24h, -35.7%/7d externally. This decision window only; scanning, tracking, and future re-evaluation continue as normal.
- Fresh long entries chasing the ai_narrative basket on NEAR's basket membership alone (contaminated catalyst source) — not a symbol-level avoid, a source-level caution.
- Any stocks intraday/swing/invest action — market closed, swing/invest playbooks deprecated (0× weight), stocks intraday last live run was an all-fetch-failed run 2 days ago.

## 10. Main Risks

- **Macro**: Iran/Hormuz conflict live and escalating (US strikes on ~90 targets Jul 13-14, Iranian retaliation against US positions in Syria, Hormuz still closed, Brent ~$79). BTC has fallen into the low-$60Ks — a real risk-off drag the internal swing regime label ("bullish trend") does not yet reflect.
- **Data-freshness mismatch**: swing report regime read is ~10h old and pre-dates the worst of this week's Iran escalation reaction; treat all swing-report "bullish/risk-on" framing as stale until the next fresh cycle.
- **Catalyst mapping degraded**: 69.8% of today's catalyst_events are unmapped to a symbol — the catalyst layer is context, not a decision input, this cycle.
- **NEAR catalyst-source contamination**: the ai_narrative basket still carries the unresolved substring-match bug from the prior review; don't trust NEAR catalyst claims sourced from that basket without independent check.
- **Telegram notifier not in the allowed CLI list for this scheduled routine** — could not send the compact Telegram summary this cycle (see §14 TODO); the summary text is included below for manual relay if desired.

## 11. Action Plan — Next 4 Hours

- Let ETH long run at/near its stated entry; no chase needed.
- Hold LTC and TRUMP as-is; do not add correlated size across both without accounting for the shared playbook exposure.
- Do not open new BANK/USDT exposure regardless of any fresh scalp/intraday score bump — treat any such score as a lagging artifact of the same reversed pump.
- Watch DATA/USDT for a confirmed breakdown below 0.0009-0.0010 on volume as the best short setup to re-qualify past the internal squeeze cap.
- Re-check BTC/ETH regime freshness once the next scalp/intraday cycle (post-11:30) lands, given the gap between internal "bullish" swing read and external risk-off reality.
- No action needed on stocks — market closed, next live data arrives at/after US pre-market.

## 12. Final Verdict per Mode

| Mode | Verdict |
|---|---|
| Crypto scalp | No trade — internal engine agrees (0 A/B), consistent with chop regime and PF0.14 playbook |
| Crypto intraday | Watch — ALLO tp1_hit running, momentum_breakout basket (TLM/ALLO/HOME) fresh but do not chase |
| Crypto swing | Selective longs only — ETH (catalyst-backed) and LTC/TRUMP (strong playbook) are the clean holds; XLM hold-only (catalyst overstated); BANK avoid |
| Stocks intraday | Closed — planning only, last live data 2 days stale |
| Stocks swing/invest | Deprecated, inert — no action, weight 0× |

## 13. Sources

- [Lorenzo Protocol Price Prediction: Will BANK Extend Its Rally?](https://www.coingabbar.com/en/price-prediction/lorenzo-protocol-price-prediction-bank-price-breakout) — CoinGabbar, 2026-07-16
- [BMNR Stock Attempts Bullish Reversal as Bitmine Moves Closer to Controlling 5% of ETH Supply](https://www.fxleaders.com/news/2026/07/14/bmnr-stock-attempts-bullish-reversal-as-bitmine-moves-closer-to-controlling-5-of-eth-supply/) — FX Leaders, 2026-07-14
- [Bitmine Buys 42,197 ETH, Now Holds 4.8% of Ethereum Supply](https://www.thecoinrepublic.com/2026/07/08/bitmine-buys-42197-eth-now-holds-4-8-of-ethereum-supply/) — The Coin Republic, 2026-07-08
- [Iran vows to keep Strait of Hormuz closed after US strikes, and crypto markets barely flinch](https://cryptobriefing.com/iran-strait-hormuz-closed-crypto-markets/) — CryptoBriefing, 2026-07-14
- [U.S.-Iran escalation weighs on bitcoin (BTC) price, stocks as oil climbs: Crypto Daily](https://www.coindesk.com/daybook-us/2026/07/14/u-s-iran-escalation-weighs-on-bitcoin-stocks-as-oil-climbs) — CoinDesk, 2026-07-14
- [CLARITY Act Stalls in Senate as Three Disputes Block Crypto Regulation 2026](https://finance.yahoo.com/markets/crypto/articles/clarity-act-stalls-senate-three-100403007.html) — Yahoo Finance, 2026-07-15
- [Near Protocol News Today: Ecosystem Update as of July 2026](https://www.coingabbar.com/en/crypto-currency-news/near-protocol-news-today-ecosystem-update-as-of-july-2026) — CoinGabbar, 2026-07-13

## 14. Fix Requests / TODO

### TODO-near-substring-bug (carried forward from 04:40 review, still unresolved)
- **issue:** News/symbol detector false-tags NEAR/USDT via literal substring match on "near" (e.g. "AREA NEAR HAJIABAD" in Iran-conflict headlines), contaminating the `ai_narrative` basket.
- **evidence:** `data/catalysts/2026-07-19/narrative_baskets.jsonl` — `ai_narrative` basket, primary NEAR/USDT.
- **suggested manual fix:** Add word-boundary/case-sensitive matching (or a symbol-alias allowlist) to the catalyst symbol detector.
- **priority:** high
- **first observed:** 2026-07-19 04:40 EEST (still present at 11:39)

### TODO-near-stale-signal (escalated from medium in prior review — growing)
- **issue:** NEAR/USDT scalp short (`sig_b16bb9e54598333a`) is tp1_hit but was never formally closed; now 44h+ past its 2026-07-17T15:56 expiry, up from ~36h at the 04:40 review.
- **evidence:** `active-signals --asset-class crypto` output, row for sig_b16bb9e54598333a.
- **suggested manual fix:** Investigate why expired-but-tp1-hit signals aren't auto-closing; add a lifecycle sweep for signals past expiry with a partial-TP status.
- **priority:** high (escalated — the gap has grown across two consecutive review cycles instead of resolving)
- **first observed:** 2026-07-19 04:40 EEST

### TODO-unmapped-headline-sampling
- **issue:** §5 catalyst coverage diagnostic requires listing top-3 unmapped headlines when unmapped >50%, but this run did not sample them (time-boxed pass) — reported the aggregate stat only, no titles.
- **evidence:** This review, §5 — 1221/1750 unmapped, no sample text included.
- **suggested manual fix:** No code fix needed; future review passes should budget one extra read of a handful of null-symbol rows from `catalyst_events.jsonl` to populate this diagnostic.
- **priority:** low
- **first observed:** 2026-07-19 11:39 EEST

### TODO-telegram-notifier-not-allowlisted
- **issue:** §O of this routine requires sending one compact Telegram summary "via the existing notifier," but no notifier CLI command is listed in this SKILL's §A.4 allowed-command set, and reading `src/` to discover the notifier script/module is outside the §A.1 read-allowlist for this strict scheduled routine. To avoid any risk of triggering an unlisted-action permission prompt (forbidden per the PERMISSION CONTRACT §C), the Telegram send was skipped this cycle.
- **evidence:** SKILL.md §A (allowed actions) vs §O (requires "existing notifier") — the notifier command itself is never named/whitelisted anywhere in the skill file.
- **suggested manual fix:** Add the exact notifier CLI invocation (module path + args) to §A.4's allowed-command list so future automated runs can send it without ambiguity, or confirm it's a fire-and-forget script safe to whitelist.
- **priority:** medium
- **first observed:** 2026-07-19 11:39 EEST (likely present in all prior runs too, worth checking whether Telegram summaries have actually been arriving)

### TODO-xec-price-precision-render-bug
- **issue:** Swing report's #1 strongest/best-long-watch candidate (XEC/USDT, score 92.4) displayed entry/invalidation/TP fields as `0.0000` — the underlying price is too small for the report's fixed decimal formatting.
- **evidence:** `data/reports/swing/2026-07-19_01-47_swing_report.md`, XEC/USDT B-tier row.
- **suggested manual fix:** Use scientific notation or dynamic decimal precision for sub-$0.001 symbols in the swing report renderer.
- **priority:** low
- **first observed:** 2026-07-19 11:39 EEST
