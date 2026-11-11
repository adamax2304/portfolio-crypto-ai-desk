---
REVIEW: OPUS ENRICHED REVIEW — ⚠ ADVISORY ONLY — NO EXECUTION
SLOT: crypto overnight / Asia review · nominal 04:30 EEST · written 2026-07-10 04:39 EEST
PREV REVIEW: 2026-07-10 03:33 EEST (post-close final daily review)
STATUS: AUTOMATED SCHEDULED RUN — NO HUMAN IN SESSION
---

# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:30 EEST

## 1. Executive Summary

**Slot: crypto overnight / Asia review — advisory only / no auto-trade.** Stocks are closed (Asia hours); crypto is the only live-actionable class this window.

**Headline finding — a status/reality gap on the two open BTC/ETH swing shorts.** The prior 03:33 review described these as "still running toward TP2/TP3, invalidation not touched." A direct check of live mark prices (Binance funding snapshots, ~03:06 EEST) against the desk's own Model-F profit-protection stop plan shows that is no longer accurate: **BTC/USDT swing short has already traded back through its post-TP1 breakeven lock** (breakeven 62096.26 vs mark ~62,950–63,140) and **ETH/USDT swing short is sitting almost exactly on its breakeven lock** (breakeven 1739.20 vs mark ~1738–1742). Under the realistic execution model these are effectively flat-to-round-tripping, not "running" — see §7 dive #1 and §14 TODO-1.

**Crypto regime: chop/mixed, risk-off leaning.** BTC nominally uptrend / ETH range, altcoin breadth only ~44–50% above EMA20, macro risk score 65–79/100 (Iran/Israel tension — externally confirmed still unresolved, ceasefire dissolved per Yahoo Finance, 2026-07-09), Fear&Greed 23 (Fear). Scalp mode remains kill-switched (mode off) for new ideas; two legacy scalp positions (SENT triggered, DEXE waiting) are manage-only leftovers.

**Open crypto book (6 non-legacy positions, all no-catalyst except ZEC):** ZEC/USDT (swing waiting near entry, intraday triggered in shallow drawdown — catalyst-backed), SENT/USDT (swing waiting near entry, scalp triggered near breakeven — no catalyst, RS-leader), DEXE/USDT (scalp waiting, but price has already run past the pullback zone — chase risk), THE/USDT (intraday triggered, small profit), ALLO/USDT (intraday triggered, small drawdown). External search corroborates DEXE (+11–23% 24h) and the broader "altseason building but Bitcoin-Season-dominant" narrative (CMC Altcoin Season Index ~46–52/100, BTC dominance 58%).

**Overall verdict: CAUTION, routed by side.** Manage the BTC/ETH shorts actively — do not assume TP2/TP3 will land; treat them as at/near breakeven, not free-roll runners. Do not chase new no-catalyst longs (yesterday's entire bounce-long book was stopped, per the 03:33 review). ZEC/USDT is the cleanest catalyst-backed watch across all three crypto timeframes. HYPE/USDT is the cleanest short-watch (catalyst-backed narrative-basket primary, still below entry threshold).

Sources: [Yahoo Finance — Bitcoin and ethereum prices today, July 9](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-thursday-july-9-prices-continue-sliding-on-geopolitical-tensions-125531170.html), [CoinDesk — Crypto starts week on firmer ground, altcoin gains mask a divided market](https://www.coindesk.com/markets/2026/07/06/crypto-bounces-back-from-the-brink-as-altcoin-optimism-returns-despite-pockets-of-weakness), [CryptoSlate — Cardano's wallet hack exposed the user layer](https://cryptoslate.com/cardanos-wallet-hack-exposed-the-user-layer-holding-its-on-chain-government-together/), [CoinDesk — SecondFi loses $2.4M in Cardano wallet exploit](https://www.coindesk.com/business/2026/06/24/secondfi-loses-usd2-4-million-in-cardano-wallet-exploit-with-up-to-usd20-million-at-risk)

---

## 2. Data Used

External web research this run: **used** — 3 WebSearch queries (BTC/ETH Asia-session price action; overnight altcoin movers; Cardano/ADA wallet-hack verification). No WebFetch needed — search snippets from Yahoo Finance/CoinDesk/CryptoSlate/Coindesk were internally consistent and corroborated the internal feed without a redundant fetch.

| Source | File / Query | Age at 04:39 EEST | Quality |
|---|---|---|---|
| Scalp report | `2026-07-10_00-39_scalp_report.md` | ~1h00min | FRESH |
| Intraday report | `2026-07-10_00-45_intraday_report.md` | ~0h54min | FRESH |
| Swing report | `2026-07-10_01-08_swing_report.md` | ~0h31min | FRESH |
| Stocks intraday report | `2026-07-10_00-55_stocks_intraday_report.md` | ~0h44min | FRESH (market closed — planning only) |
| Stocks swing/invest | `2026-07-02_13-0x` reports | ~8 days | **STALE** — excluded from actionable, no fresher source |
| Catalyst events / baskets | `data/catalysts/2026-07-10/catalyst_events.jsonl` (500 events), `narrative_baskets.jsonl` (5 baskets), `catalyst_cycle_00-47.md` | ~0h52min | FRESH |
| Funding snapshots (mark price) | `funding_snapshots` table, BTC/ETH, latest 2026-07-10T01:06 UTC | ~1h33min | used to cross-check invalidation/breakeven vs live price |
| Signal stop plan | `signal_stop_plan` table (Model F profit-protection, BE-after-TP1) | live | used for §7 dive #1 |
| DB queries | `proposed_signals` (read-only): all open crypto positions by status/mode | live | §7, §8 |
| Signal stats | `signal-stats --asset-class crypto` (week window) | live | swing +8.36R/PF1.3x, scalp −13.x R/PF0.3, intraday −3.1R/PF0.9 — consistent with 03:33 review |
| Untracked legacy alerts | `detect_untracked_legacy_alerts --since 2026-07-10` | live | **0 found** — clean |
| Previous review | `OPUS_ENRICHED_REVIEW_AUTO_2026-07-10_0333.md` | ~1h06min | compared in §4 |
| External: BTC/ETH Asia session | Yahoo Finance, CoinDesk | live search | confirms BTC $62.7–63.3K, ETH ~$1,740–1,760 range, geopolitical drag ongoing |
| External: overnight altcoin movers | CoinDesk, CryptoTicker, CoinDCX | live search | confirms DEXE real rally (+11–23% variously reported), altseason index rising but still Bitcoin-Season |
| External: ADA wallet hack | CryptoSlate, CoinDesk, TradingView | live search | confirms SecondFi wallet exploit (~$2.4M confirmed, up to $20M at risk) is a genuine, dated (2026-06-23/24) incident — not fabricated, though now ~2.5 weeks old |

**Notes**: TradingView / manual chart check unavailable — all technical levels are from local OHLCV/ATR/EMA and DB fields. Onchain, order-book depth, liquidation heatmaps and live social-attention feeds remain missing (longstanding, unchanged).

---

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: 2026-07-10 04:12 EEST (~27min old) — **FRESH**
- Latest cycle summary `cycle_03_03-32_summary.md` mtime: 2026-07-10 03:32 EEST (~1h07min old) — **FRESH** (well under 3h defer threshold)
- Both fresh → review proceeds (no defer).
- Stocks monitor pid/log active (`stocks_monitor_1783645803.log`, mtime 04:10 EEST) — process alive per file activity.
- Paper monitor status file (`reports/PAPER_MONITOR_STATUS_LATEST.md`) mtime 04:11 EEST — fresh, but note: it tracks legacy touch-based outcomes (expired/closed history), not a live breakeven-adjusted P&L view — see §7 dive #1 and TODO-1.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-07-10 04:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["stocks_swing_invest_fresh_source"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log + cycle summary both fresh (<1h10)", "stocks swing/invest 8 days stale, excluded", "swing report just refreshed (04:08 EEST), no longer carry-forward"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["mixed", "chop", "risk_off", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC uptrend / ETH range, altcoin breadth 44-50% above EMA20", "macro risk 65-79/100 risk-off, Fear&Greed 23", "external: Iran/Israel tension still unresolved (ceasefire dissolved per Yahoo Finance 2026-07-09)", "stocks closed; last read risk_on (VIX 15.84, breadth 100%) but not actionable this slot"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported", "no_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["106/500 catalyst events mapped today (21.2% mapped / 78.8% unmapped) — weak", "5 narrative baskets: perps_dex (HYPE), delisting_thin_liquidity, ai_narrative (TAO/NEAR/FET/RENDER), rwa_narrative (ONDO/XLM), momentum_breakout (SENT/DEXE)", "open book is mostly no-catalyst momentum (SENT/DEXE/THE/ALLO); only ZEC has real catalyst backing"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["oi_supports", "funding_extreme", "squeeze_risk", "data_unavailable"],
      "data_missing": ["liquidation heatmaps", "order book depth/CVD"],
      "suggested_effect": "advisory_only",
      "facts_used": ["DEXE/USDT: elevated long crowding flagged on Bybit/OKX cross-check", "SENT/USDT: negative funding across external venues (bybit/okx/mexc), crowding elevated — shorts crowded, bounce/squeeze risk both ways", "THE/USDT: OI +90% 24h with negative funding — large fresh positioning, unresolved crowding label"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["chase_risk", "entry_late", "clean_retest", "overextended"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["DEXE/USDT scalp pullback zone 31.11-31.90 vs current ~32.25 — price already ran past the planned entry, chase risk", "ZEC/USDT swing pullback zone 474.17-477.69 vs current ~479 — right at the edge, closest to a clean fill", "SENT/USDT swing pullback zone 0.0157-0.0162 vs current ~0.0164 — also just above zone"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["waiting_for_entry", "entered_unresolved", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZEC/USDT (swing) + SENT/USDT (swing) + DEXE/USDT (scalp): WAITING for entry", "SENT/USDT (scalp), ZEC/THE/ALLO/USDT (intraday): ENTERED, unresolved (no TP/SL yet)", "BTC/ETH/USDT (swing) + ETH/USDT (intraday): TP1 hit, needs review — see technical_entry/risk_manager for the breakeven-lock nuance"]
    },
    {
      "agent": "risk_manager",
      "verdict": "manual_review",
      "confidence": 0.65,
      "reason_codes": ["reduce_risk", "manual_review", "correlation_cluster"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/USDT swing short: live mark (~62,950-63,140) has traded THROUGH the Model-F post-TP1 breakeven lock (62096.26) — position is effectively flat-to-negative under realistic execution, not a free-roll runner", "ETH/USDT swing short: live mark (~1738-1742) sitting almost exactly on its breakeven lock (1739.20) — razor-thin, could flip either way", "ETH/USDT intraday short: still ~1-5pts below its breakeven lock (1743.37) — thinnest cushion of the three but still nominally favorable", "ADA/ETH exploit_hack operator-review flags persist across reports (see §14 TODO-2 on the ETH one, likely mislabeled)"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["swing: n=92, PF~1.3x, totalR +8.36 (week) — only consistently working crypto mode", "scalp: n=140, PF~0.3, totalR -13.x (week) — weak, and mode is now kill-switched for new ideas", "intraday: n=142, PF~0.9, totalR -3.1 (week) — marginally negative, no-catalyst momentum playbook explicitly documented as net-negative in its own report text"]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": { "symbol": "SENT/USDT", "trigger": "confirmed hold of swing pullback zone 0.0157-0.0162 with volume, invalidation below 0.01516", "reason": "RS-leader across scalp/intraday/swing, but no catalyst — known failure mode for this playbook is net-negative in chop; treat as low-confidence" },
    "best_short_candidate": { "symbol": "HYPE/USDT", "trigger": "failed retest/rejection at 67.21-67.47 zone with volume, or clean breakdown below 66.66 support", "reason": "perps_dex_narrative basket primary, catalyst-backed (importance 5.06), still below active-trade score threshold — watch only" },
    "best_catalyst_candidate": { "symbol": "ZEC/USDT", "trigger": "swing pullback fill into 474.17-477.69 (currently ~479, right at the edge)", "reason": "only open-book symbol with real news backing (Ironwood shielded-pool proof-of-no-bugs + supply-cap commentary), appears across all 3 crypto timeframes" },
    "avoid_candidate": { "symbol": "DEXE/USDT", "reason": "price has already run past its scalp pullback entry zone (31.11-31.90 vs ~32.25 current), elevated long crowding flagged externally, and yesterday's entire chase-long book was stopped out — do not add here" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.60 | mixed, chop, risk_off, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, fresh_catalyst, narrative_supported, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.50 | oi_supports, funding_extreme, squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, entry_late, clean_retest, overextended | advisory_only |
| execution_lifecycle | caution | 0.70 | waiting_for_entry, entered_unresolved, needs_review | advisory_only |
| risk_manager | manual_review | 0.65 | reduce_risk, manual_review, correlation_cluster | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.60 | (synthesis) | advisory_only |

---

## 4. What Changed vs Previous Review (03:33 EEST)

- **New, material finding this run** (not in the 03:33 review): the BTC/USDT swing short has already traded back through its Model-F post-TP1 breakeven lock, and the ETH/USDT swing short is sitting almost exactly on its own breakeven lock. The 03:33 review's framing ("still running toward TP2/TP3, invalidation not touched") checked only the static `invalidation` field, which uses the *original* pre-TP1 stop — it does not reflect the tighter breakeven lock that Model F's profit-protection overlay computes after TP1. Cross-checking live mark price against `signal_stop_plan.stop_after_tp1` shows BTC is already through its (tighter) breakeven level. See §7 dive #1 and TODO-1.
- Swing report refreshed (gen 04:08 EEST) — no longer carry-forward; SENT/USDT and ZEC/USDT swing longs are fresh B-tier ideas as of this cycle (both still waiting_for_entry).
- Catalyst layer rolled over to a new day's file (`data/catalysts/2026-07-10/`, 500 events scanned vs 4,996 in yesterday's file) — mapped % is roughly flat (21.2% today vs 18.2% at 03:33), still weak.
- No new A-tier signals in any crypto mode (unchanged — none since at least the 03:33 review).
- No untracked legacy alerts (unchanged — clean at both checkpoints).
- Thesis on DEXE/USDT: unchanged from implicit prior caution — now externally corroborated as a genuine mover (+11–23% variously reported across sources), but entry has moved further away from the pullback zone, increasing chase risk rather than decreasing it.

---

## 5. Catalyst Coverage

- Catalyst events today: **500** scanned, **106 mapped (21.2%)**, **394 unmapped (78.8%)**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Narrative baskets: **5** — perps_dex_narrative (primary HYPE/USDT), delisting_thin_liquidity (no primary), ai_narrative (primary NEAR/RENDER/TAO/FET), rwa_narrative (primary ONDO/XLM), momentum_breakout (primary SENT/DEXE).
- Top 3 unmapped headlines (all exchange-listing announcements for symbols outside the tracked universe):
  - "MEXC to List SPYUSDT Index Futures on Jul 9 with 0-Fee Trading" (t.me/MEXC_OfficialAnnouncements)
  - "New Stock Futures Listings: QXO, AKAM, FLUT and GRAB USDT-M Futures to Launch on Jul 9" (t.me/MEXC_OfficialAnnouncements)
  - "New Pre-IPO Futures Listings: SKHY USDT-M Futures to Launch on Jul 9" (t.me/MEXC_OfficialAnnouncements)

---

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **chop / mixed, risk-off leaning** (macro risk 65-79/100, Fear&Greed 23, altcoin breadth only ~44-50% above EMA20; BTC dominance externally reported at 58%, altseason index ~46-52/100 — improving but still Bitcoin-Season).
- Stocks mood: **closed** (Asia hours) — last read was risk_on (VIX 15.84, breadth 100% above EMA20/50); planning-only, not actionable this slot.
- Dominant narrative: perps/DEX (HYPE-led), AI-sector rotation (TAO/NEAR/FET/RENDER), momentum-breakout cluster (SENT/DEXE) — all single-source/basket confidence, not confirmed catalysts.
- Preferred side now: **wait-for-trigger / manage existing** — no fresh conviction long or short; manage the BTC/ETH swing shorts actively (see §7 dive #1).
- Best long candidate: SENT/USDT — no clean trigger yet; needs a confirmed hold of 0.0157-0.0162 with volume (see §8).
- Best short candidate: HYPE/USDT — no clean trigger yet; needs a failed retest of 67.21-67.47 or breakdown below 66.66 (see §8).
- Best catalyst-backed candidate: ZEC/USDT — closest to a clean fill (swing pullback zone 474.17-477.69 vs current ~479).
- What to avoid: DEXE/USDT fresh entries (chase risk — price already past its pullback zone); adding new no-catalyst intraday longs in general (documented net-negative playbook in current regime).
- What would change the view: BTC reclaiming and holding above ~63,300 with altcoin breadth pushing through 60% above EMA20 (risk-on confirmation); or a clean breakdown in BTC back toward the 61,500-62,000 area (reinforces the still-open swing shorts and would argue for adding clean failed-bounce shorts, not longs).

---

## 7. Candidate Deep Dives

### #1 — BTC/USDT & ETH/USDT swing shorts — profit-protection risk (NEEDS REVIEW)

**Status:** TP1_HIT (legacy) / **at-or-through breakeven (realistic, Model-F overlay)** — ENTERED, TP1 locked, now NEEDS REVIEW for the runner portion.

- BTC/USDT swing short: entry 62,096.26, original invalidation 62,527.54, TP1 61,578.72 (hit). Model-F `stop_after_tp1` = 62,096.26 (breakeven). **Live mark ~62,950-63,140 (Binance, 01:06 UTC) is already ~$850-1,050 THROUGH the breakeven lock.** Under the realistic execution model this runner would already be flat or worse, not "running toward TP2/TP3."
- ETH/USDT swing short: entry 1,739.20, original invalidation 1,754.11, TP1 1,721.31 (hit). Model-F breakeven lock = 1,739.20. **Live mark ~1,738-1,742 is sitting almost exactly on that line** — could tip either way on the next candle.
- ETH/USDT intraday short: entry 1,743.37, breakeven lock 1,743.37. Live mark ~1,738-1,742 — still ~1-5 points below (favorable), but the thinnest cushion of the three.
- Has price already reacted to the catalyst? N/A (macro/geopolitical thesis, not a discrete catalyst).
- Is this chasing? No — these are the desk's oldest and best-performing open positions.
- Retest/pullback structure? BTC's bounce back through breakeven looks like exactly the kind of reversal the original short thesis would need to survive; no clean re-break lower yet.
- Overextended? Not by ATR terms — this is about the stop level, not distance from EMA.
- Aligned with market mood? Partially — macro is still risk-off/Iran-driven, which supports the short thesis directionally, but price action has not confirmed it in the last several hours.
- Actionable now or after confirmation? Manage-only; no new entry implied either way.
- Invalidates if: BTC holds above ~63,300 on a closing basis (extends the breakeven breach) or ETH closes above 1,754 (the original invalidation).
- Chase risk? N/A (existing position).
- Catalyst confirmation/contradiction? External search confirms the underlying Iran/Israel risk-off thesis is still live, but does not confirm continued BTC downside — the exact opposite (Trump "deal" comments) drove the bounce that is now testing these breakeven levels.

### #2 — ZEC/USDT (best catalyst-backed candidate)

**Status:** WAITING for entry (swing, B-tier, score 66.6) / ENTERED UNRESOLVED (intraday, triggered, small drawdown).

- Catalyst: Zcash co-founder supply-cap commentary + developers nearing proof the upcoming Ironwood shielded pool has no hidden counterfeiting bugs — both dated, verified internally via news_items, news_mention verification (importance 3.89).
- Swing: pullback zone 474.17-477.69, invalidation 469.86, TP1 487.07. Current ~479 — right at the top edge of the zone, closest of the open watchlist to a clean fill.
- Intraday: already triggered at 483.84, stop 476.31, TP1 492.89; current ~479-480 — in a shallow, still-within-stop drawdown.
- Has price already reacted to the catalyst? Partially — the move has been building over days (7d return +9.9%), not a single-day catalyst pop.
- Chasing? No, this is a pullback/continuation setup, not a breakout chase.
- Overextended? No (only 0.02-0.66x volume ratio, in fact volume is thin — a genuine weakness; relative strength isn't backed by strong current volume per the report's own counter-thesis).
- Aligned with mood? Yes for a catalyst-backed idea in a mood that otherwise favors caution over pure momentum.
- Actionable now or after confirmation? After confirmation — wait for the swing pullback fill or a reclaim of the intraday entry.
- Invalidates below 469.86 (swing) / 476.31 (intraday).
- Chase risk: low (pullback structure, not breakout).

### #3 — DEXE/USDT (avoid candidate for fresh entries)

**Status:** WAITING for entry (scalp, B-tier, score 66) — kill-switched mode, manage/expire-only; also a top-scored, non-actionable watchlist idea in intraday/swing.

- Externally confirmed real mover: +11.6% (internal 24h) to +23% (external aggregator, different window) — momentum_breakout basket primary.
- Scalp pullback zone was 31.11-31.90; current price ~32.25 is already above the zone — the desk's own "waiting_for_entry" status means this hasn't triggered a fill on the planned pullback, and price is moving further away, not closer.
- Derivatives: Bybit/OKX cross-check flags "elevated long crowding" — a genuine squeeze-unwind risk if momentum stalls.
- Is this chasing? Yes, if entered here — the planned entry has already been missed.
- What would make it actionable? A genuine retest back into 31.11-31.90 with volume holding, not a continuation buy at current levels.
- Counter-thesis already on file: "funding is elevated; entry must be clean."

### #4 — HYPE/USDT (best short-watch candidate)

**Status:** WATCHLIST ONLY (swing, C-tier, score 62.3) — not actionable, catalyst-backed.

- perps_dex_narrative basket primary; catalyst importance 5.06 (highest catalyst score among C-tier swing ideas this cycle).
- Setup: failed-bounce/retest short. Conditional zone 67.21-67.47, invalidation if activated above 67.795, targets down toward 65.3-66.5.
- Derivatives: price down + OI up — fresh shorts pressing, possible squeeze if price reclaims. This cuts both ways: a clean breakdown validates the short; a reclaim of 67.8 signals a squeeze, not a short entry.
- Is this chasing? No — it is explicitly a failed-bounce structure, the opposite of chasing.
- Actionable now or after confirmation? After confirmation only — score (62.3) is below the active-trade threshold.
- What would invalidate: a reclaim and hold above 67.795.

### #5 — SENT/USDT (best long-watch candidate)

**Status:** WAITING for entry (swing, B-tier, score 65.4) / ENTERED UNRESOLVED (scalp, triggered, near breakeven).

- Top RS-leader across scalp/intraday/swing reports (24h +20-24%, RS vs BTC +18-23%, volume up to 6.2x) — a genuine strength signal.
- No fresh verified catalyst — this is the playbook's own documented weak spot: "no-catalyst intraday in chop is net-negative — needs RS-leader or breakout confirmation" (14d WR 23% / PF 0.70 / -3R for the no-catalyst cohort).
- Derivatives: negative funding across bybit/okx/mexc, crowding flagged "elevated" — shorts are crowded against this move, which supports a continuation but also raises squeeze/unwind risk on both sides.
- Swing pullback zone 0.0157-0.0162, invalidation 0.01516, TP1 0.01738. Current ~0.0164 — just above the zone.
- Actionable now or after confirmation? After a confirmed hold of the pullback zone with volume — do not chase the current price.
- Chase risk: moderate — RS is strong but volume backing for the swing entry is thin.

---

## 8. Best Candidates Ranked

1. **Best long-watch: SENT/USDT** — trigger: confirmed hold of 0.0157-0.0162 with volume; invalidation 0.01516. Low confidence (no catalyst, documented weak playbook).
2. **Best short-watch: HYPE/USDT** — trigger: failed retest/rejection at 67.21-67.47 with volume, or breakdown below 66.66; invalidation above 67.795.
3. **Best catalyst-watch: ZEC/USDT** — trigger: swing pullback fill into 474.17-477.69 (currently sitting right at the edge, ~479); invalidation 469.86.
4. **Manage-only priority: BTC/ETH swing shorts** — no new trigger; active risk review needed given the breakeven-lock breach (see §7 #1).
5. **Avoid: DEXE/USDT** fresh entries — price has already run past its pullback zone; wait for a genuine retest of 31.11-31.90.

---

## 9. Avoid / No Trade

This applies to the **current decision window only** — not a system pause. Scanning, tracking, and outcome recording continue regardless.

- **DEXE/USDT** fresh longs at current levels (~32.25) — chase risk, elevated long crowding, entry zone already missed.
- New no-catalyst intraday longs generally — the playbook's own 14-day track record for this cohort is net-negative (WR 23% / PF 0.70 / -3R), and yesterday's entire bounce-long book (per the 03:33 review) was stopped out.
- New crypto scalp ideas — mode is kill-switched; only manage the two legacy positions (SENT triggered, DEXE waiting) to their existing stops/targets.
- Stocks — market closed; nothing is actionable in this asset class until the US cash open.

---

## 10. Main Risks

- **BTC/ETH swing-short breakeven breach** (see §7 #1) — the single largest live risk this window; a further BTC push above ~63,300 or ETH close above 1,754 would fully invalidate what had been the desk's best-performing crypto cluster.
- **Chase risk on DEXE/USDT** — externally-confirmed real momentum but entry already missed; adding here repeats yesterday's chase-long failure pattern.
- **Catalyst mapping weak (78.8% unmapped)** — treat all catalyst context this cycle as directional color, not confirmation.
- **Thin volume behind several open longs** (ZEC, SENT, ALLO all show volume ratios well below 1x on swing) — relative strength not backed by strong current volume, per the reports' own counter-theses.
- **Persistent operator-review flags on ADA/ETH "exploit_hack"** — ADA's is a real, verified (if now dated) incident (SecondFi, ~$2.4M confirmed); the ETH one looks like a miscategorized headline (see TODO-2).
- **Ongoing Iran/Israel geopolitical overhang** — externally confirmed still unresolved as of 2026-07-09, the primary driver of the macro risk-off score; a de-escalation or escalation headline could move BTC sharply in either direction with limited warning.

---

## 11. Action Plan — next 4 hours

1. Actively monitor BTC/USDT and ETH/USDT swing shorts against the Model-F breakeven levels (62,096.26 / 1,739.20), not just the stale original invalidation fields — treat both as at-risk, not "still running."
2. Do not add fresh DEXE/USDT longs at current levels; wait for a genuine retest of 31.11-31.90.
3. Watch for a ZEC/USDT swing pullback fill into 474.17-477.69 — closest clean setup on the board.
4. Watch HYPE/USDT for a failed retest of 67.21-67.47 or breakdown below 66.66 as the cleanest short-watch idea.
5. No stocks action — market closed; re-evaluate at/after the US pre-market read (next slot, 11:30 EEST Europe/pre-US context).
6. Continue scanning/tracking as normal across all modes — no pause of any kind.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** No new trades (kill-switched). Manage legacy SENT (triggered) and DEXE (waiting) to existing levels only.
- **Crypto intraday:** No new trades. Manage ZEC/THE/ALLO to existing stops/targets; no-catalyst momentum playbook is net-negative in current regime — do not add.
- **Crypto swing:** Watch-only for SENT/ZEC/DEXE(via basket) entries; the two open swing shorts (BTC/ETH) need active risk review, not passive holding.
- **Stocks intraday/swing/invest:** Market closed — planning/watchlist only. AAPL (Broadcom $30B catalyst, per prior review) remains the cleanest catalyst-backed carry into the next US-session review.

---

## 13. Sources

- [Yahoo Finance — Bitcoin and ethereum prices today, Thursday, July 9](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-thursday-july-9-prices-continue-sliding-on-geopolitical-tensions-125531170.html) (2026-07-09)
- [CoinDesk — Crypto bounces back from the brink as altcoin optimism returns](https://www.coindesk.com/markets/2026/07/06/crypto-bounces-back-from-the-brink-as-altcoin-optimism-returns-despite-pockets-of-weakness) (2026-07-06)
- [CryptoSlate — Cardano's wallet hack exposed the user layer](https://cryptoslate.com/cardanos-wallet-hack-exposed-the-user-layer-holding-its-on-chain-government-together/) (date on source page; incident dated 2026-06-23/24)
- [CoinDesk — SecondFi loses $2.4M in Cardano wallet exploit, up to $20M at risk](https://www.coindesk.com/business/2026/06/24/secondfi-loses-usd2-4-million-in-cardano-wallet-exploit-with-up-to-usd20-million-at-risk) (2026-06-24)
- Internal: `data/reports/{scalp,intraday,swing}/2026-07-10_*` reports; `data/catalysts/2026-07-10/*`; `proposed_signals`, `signal_stop_plan`, `funding_snapshots` tables (live DB reads).

---

## 14. Fix Requests / TODO

### TODO-1
- **issue:** The automated review narrative for tp1_hit swing/intraday shorts (and the `PAPER_MONITOR_STATUS_LATEST.md` file it draws from) describes positions as "still running, invalidation not touched" by checking only the static `proposed_signals.invalidation` field — but the desk's own Model-F profit-protection overlay (`signal_stop_plan.stop_after_tp1`) computes a materially tighter breakeven/lock level after TP1. This run found BTC/USDT swing short had already traded back through its breakeven lock while the invalidation field alone would have said "no issue yet." This caused the 03:33 review to describe the position more favorably than the live-price cross-check supports.
- **evidence:** `proposed_signals` BTC/USDT swing short: invalidation=62527.54; `signal_stop_plan` for same signal_id shows stop_after_tp1=62096.26 (basis='be'); `funding_snapshots` latest BTC/USDT mark_price=62953.42 (2026-07-10T01:06:02Z), i.e. above the BE lock but below the original invalidation — the two fields disagree on whether this position is "at risk."
- **suggested manual fix:** Either (a) have the review/monitor pipeline surface `stop_after_tp1`/`stop_after_tp2` alongside the legacy `invalidation` field once a signal is tp1_hit, or (b) make the automated post-TP1 status label reflect the tighter of the two levels so "still running" isn't reported when the realistic breakeven lock has already been breached.
- **priority:** high
- **first observed:** 2026-07-10 04:39 EEST

### TODO-2
- **issue:** ETH is repeatedly flagged `[exploit_hack]: block_requires_operator_review` across multiple reports/reviews, citing the headline "Ethereum Foundation Turns AI Loose on ETH Network to Find Bugs Before Hackers Do" (Decrypt). That headline describes proactive, defensive bug-bounty/security research, not an actual exploit or hack — it appears to be a false-positive catalyst-type classification triggered by "bugs"/"hackers" language in the title.
- **evidence:** Recurs identically in `2026-07-10_00-39_scalp_report.md` §5c, `2026-07-10_00-45_intraday_report.md` §5c, and `2026-07-10_01-08_swing_report.md` §5c, all citing the same Decrypt headline under `exploit_hack`.
- **suggested manual fix:** Review the catalyst-type classifier's keyword/heuristic rules for `exploit_hack` to exclude proactive-security/bug-bounty framing (e.g. require an actual loss/exploit confirmation term, not just "bug"/"hacker" co-occurrence).
- **priority:** medium
- **first observed:** 2026-07-10 04:39 EEST (recurring across at least this and the prior cycle's reports)

### TODO-3
- **issue:** Catalyst mapping remains persistently weak (78.8% unmapped today, 78.8% at the 03:33 review's date-prior file too) — the majority of unmapped events are MEXC exchange-listing announcements for symbols/futures products (e.g. SPYUSDT index futures, pre-IPO futures like SKHY) that fall outside the tracked spot-symbol universe and can never resolve to a `symbol` match under the current resolver.
- **evidence:** `data/catalysts/2026-07-10/catalyst_events.jsonl` — 394/500 events have `symbol=null`; top unmapped titles are all `t.me/MEXC_OfficialAnnouncements` new-futures-listing posts.
- **suggested manual fix:** Either add a catalyst_type-level suppression/low-priority bucket for exchange "new listing" announcement spam (so the unmapped % stat isn't dominated by noise that was never mappable in principle), or extend the symbol resolver to recognize the exotic futures tickers mentioned in these posts.
- **priority:** low
- **first observed:** 2026-07-10 04:39 EEST (same pattern noted at 18.2%/21.2% mapped across the last several cycles — persistent, not a one-off)
