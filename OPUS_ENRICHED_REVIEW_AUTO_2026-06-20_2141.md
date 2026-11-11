# Opus Enriched Review — Late-Session Risk Review — Auto Cycle 21:41 EEST

_Generated 2026-06-20 21:41 EEST (Saturday, weekend crypto-only mode). Advisory only. No auto-trade. Scanner / collection / tracking continue in all moods._

> **CATALYST MAPPING CRITICALLY LOW: 21.6% (536/2479 events mapped). Use catalyst layer as CONTEXT ONLY, not final decision basis.**
>
> **REGIME: BTC range/chop ~$63.6K. ETH uptrend. Breadth 46.3% EMA20 (compressed). Shorts dominant bucket (WR 28.6%, PF 1.77). Longs systemically losing (WR 8.6%, PF 0.44).**
>
> **KEY FLAG: SYN/USDT — NO CATALYST confirmed externally. Pure speculative pump. Bitget delisted SYN June 18 (bearish). Price 3x above forecast. AVOID.**

---

## 1. Executive Summary

**Sat 2026-06-20, 21:41 EEST — Late-Session Risk Review — advisory only / no auto-trade.**

- Slot type: **late_session** (21:30 EEST). Stocks closed (weekend). Crypto is the live class.
- Scheduler fresh (scheduler.log 21:11, 30 min), cycle_01 completed at 19:41 (2h ago). Data quality: OK with caveats.
- **Catalyst mapping CRITICALLY LOW: 21.6%** — flag emitted; catalyst layer is context only this review.
- BTC confirmed ~$63,676 (external), in range/chop; ETH uptrend; breadth 46.3% — mixed/compressed.
- Active crypto signals: **23** (all B-tier, 0 A-tier). Since 18:40 review: 26 → 20 (cycle tracked 6 closed) → 23 (3 new post-cycle). Untracked alerts: 0.
- Paper monitor (19:41): OPEN actionable 7 · WAITING 2 · ENTERED UNRESOLVED 25 · REVIEW/SHADOW 129 · NO-ENTRY 30 · Closed 271W/15L/0flat · Needs review 0.
- Crypto performance: WR 9.4%, PF 0.53, Total R −40R (reliable, n=258). **Longs PF 0.44 (failing). Shorts PF 1.77 (only working bucket).**
- **SYN/USDT**: external research confirmed NO catalyst — pure technical breakout speculation; Bitget delisted June 18 (bearish); OI declining (short covering only). AVOID.
- **SOL/USDT**: best catalyst-backed long — bitFlyer listing June 24 upcoming + tokenized equity leadership + whale buy ($16.55M, ~15h stale). B-tier 76 WAITING. Price $71.43 > entry zone $70.44–$70.73. Do NOT chase above zone.
- **NEAR short**: B-tier short WAITING — best pure short candidate.
- Head trader verdict: CAUTION / WAIT-FOR-TRIGGER. Prefer shorts + SOL catalyst-backed only. No new longs for extended names (SYN/BICO/ALICE). Late-session risk applies to all.

---

## 2. Data Used

| Source | File / Tool | mtime EEST | Freshness |
|---|---|---|---|
| Scheduler log | `scheduler.log` | 21:11 | 30 min — FRESH |
| Latest cycle | `cycle_01_19-07_summary.md` | 19:41 | 2h — FRESH (< 3h) |
| Scalp report | `2026-06-20_16-24_scalp_report.md` | 19:24 | 2h17m — FRESH (<4h) |
| Intraday report | `2026-06-20_16-39_intraday_report.md` | 19:39 | 2h2m — FRESH (<4h) |
| Swing report | `2026-06-20_13-30_swing_report.md` | 16:30 | 5h11m — CARRY-FORWARD (4–12h) |
| Stocks reports | N/A | — | Weekend (not generated) |
| Catalyst events | `data/catalysts/2026-06-20/catalyst_events.jsonl` | cycle | 2,479 events; 536 mapped (21.6%) |
| LLM packet | `data/processed/llm_analysis_packet.md` | 19:39 | Refreshed end of cycle |
| Active signals | `active-signals --asset-class crypto` | 21:41 live | 23 signals |
| Signal stats | `signal-stats --asset-class crypto` | bg output | 258 sample |
| Untracked alerts | `detect_untracked_legacy_alerts --since 2026-06-20` | 21:41 | 0 untracked |
| Paper monitor | `PAPER_MONITOR_STATUS_LATEST.md` | 19:41 cycle | From cycle step 14 |
| Previous review | `OPUS_ENRICHED_REVIEW_AUTO_2026-06-20_1840.md` | 18:40 | Previous slot |
| External: BTC price | CoinDesk / WebSearch | 2026-06-20 | $63,676 confirmed |
| External: SOL catalysts | Phemex / OpenPR | 2026-06-20 | bitFlyer June 24 listing + tokenized equity |
| External: SYN | CoinMarketCap AI | 2026-06-20 | NO catalyst; Bitget delisted June 18 |

**External web research**: Available and performed. All claims cited. No fabricated data.

**Blindspots**: Reddit 403 blocked (crowd sentiment missing), on-chain config missing (`config/onchain.yaml` absent), liquidation heatmaps not connected, live KOL feeds not automated, Bybit OHLCV in swing report: 0 rows / 40+ failed (see TODO-BYBIT).

---

## 3. Scheduler / Data Freshness

- `scheduler.log` last write: **21:11 EEST** (30 min ago) — FRESH
- `cycle_01_19-07_summary.md` last write: **19:41 EEST** (2h ago) — FRESH (< 3h threshold)
- Cycle 1 steps: **ok=16 failed=0** — clean run
- Monitor window: 90 min background (pid=17120)
- Intelligence layer: 105 symbols tracked, 689 events, last event 16:48 UTC; derivatives 76 symbols cached
- Squeeze phases: expansion=3 · build-up=13 · unwind=3 · **post-unwind-chop=24** · unknown=33
- Paper monitor (cycle 19:41): OPEN actionable=7 · WAITING for entry=2 · ENTERED UNRESOLVED=25 · REVIEW/SHADOW=129 · NO-ENTRY/stale/moved-away=30 · Closed today 271W/15L/0flat · Needs review=0
- Current active signals (CLI 21:41): **23** crypto B-tier
- Untracked legacy alerts: **0** (pipeline healthy)
- Weekend mode: **ACTIVE** (Saturday; A-tier margin penalty; weak signals cap at B; chasing entries demote)
- Bybit OHLCV: degraded (40 failures in swing report) — see TODO-BYBIT

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-06-20 21:41 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["onchain_config_missing", "social_attention_missing", "reddit_blocked", "bybit_ohlcv_degraded"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "scheduler.log mtime 21:11 EEST (30 min ago — fresh)",
        "cycle_01_19-07 finished 19:41 EEST (2h ago — fresh < 3h threshold)",
        "scalp 19:24 EEST (2h17m — fresh), intraday 19:39 EEST (2h2m — fresh)",
        "swing 16:30 EEST (5h11m — carry-forward 4-12h band)",
        "catalyst_events.jsonl: 2479 total, 536 mapped (21.6%) — CRITICALLY LOW (<50% threshold)",
        "Reddit 403 blocked; on-chain config missing; Bybit OHLCV 40 failures"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.80,
      "reason_codes": ["chop", "mixed", "wait_for_trigger"],
      "data_missing": ["live_x_twitter_sentiment", "liquidation_heatmaps", "etf_flows", "dxy_yields"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC $63,676 (external confirmed), trend: range (intraday/scalp)",
        "ETH trend: uptrend (intraday/scalp); swing report shows downtrend (stale carry-forward)",
        "Altcoin breadth EMA20 46.3%, EMA50 53.7% — below median, no clear bull",
        "Volatility: btc_atr_percentile 17-18% (low/normal)",
        "Squeeze phases: 24 post-unwind-chop — majority digesting prior moves",
        "Weekend mode active — thinner liquidity, wider wicks expected"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["catalyst_missing", "mapping_weak", "stale_catalyst"],
      "data_missing": ["unmapped_78pct_catalyst_events"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Catalyst mapping: 536/2479 (21.6%) — well below 50% warning threshold; mapping weak this run",
        "SOL: whale buy $16.55M (Lookonchain, ~15h old — stale); bitFlyer listing June 24 (upcoming, confirmed external)",
        "SYN: NO catalyst confirmed (CoinMarketCap AI); Bitget delisted June 18 (bearish signal)",
        "BICO/BEL/ALICE: no verified catalyst; momentum_breakout basket (wait_pullback playbook)",
        "Axelar $4.7M bridge hack (basket-level exploit, no active-signal mapping)",
        "ETH: Tom Lee funding crisis denial (positive sentiment, single source)"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.60,
      "reason_codes": ["squeeze_risk", "post_unwind_chop", "funding_extreme"],
      "data_missing": ["bybit_oi_history_sparse", "liquidation_heatmaps", "order_book_depth"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "ALICE: OI +119.75%, long/short 2.134, funding -0.00375 (shorts paying) — squeeze setup on short side",
        "BICO: OI +106.4%, crowding UNKNOWN — massive positioning on thin volume (0.16-0.27x avg)",
        "BEL: OI +26%, crowding UNKNOWN, funding negative multi-venue",
        "AXS: OI +46%, crowding UNKNOWN",
        "SYN: OI -18% while price up → SHORT COVERING ONLY, not fresh longs; weaker continuation",
        "BTW: extreme long crowding 90% — avoid entirely",
        "24 symbols in post-unwind-chop phase; 3 in expansion; 3 in unwind"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.70,
      "reason_codes": ["entry_late", "chase_risk", "stale_before_entry"],
      "data_missing": ["tradingview_chart_mcp", "order_book_depth", "cvd"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "SOL: price $71.43 (intraday 19:39) vs entry zone $70.44-$70.73 — price ABOVE zone (chase risk)",
        "SYN: price $0.1523-$0.1623 vs swing entry zone $0.1439-$0.1504 — price ABOVE zone (extended)",
        "BICO: price $0.0412-$0.0436 vs entry zone $0.0382-$0.0403 — price ABOVE zone",
        "NEAR short: WAITING for zone $2.78-$2.81 — not yet triggered",
        "BEL/AXS/ALICE: TRIGGERED — tracking, not new entries",
        "Late session 21:41 EEST: intraday entries too late to initiate",
        "TradingView / manual chart check unavailable — using OHLCV/ATR/EMA fields only"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["open_actionable", "entered_unresolved", "review_shadow"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "OPEN actionable: 7 (weekend B-tier crypto)",
        "WAITING for entry: 2 (SOL swing, ME... swing — waiting for entry zones)",
        "ENTERED UNRESOLVED: 25 (entry triggered, no TP/SL before window — not missed entries)",
        "REVIEW/SHADOW: 129 (monitoring only, not Telegram-actionable)",
        "NO-ENTRY/stale/moved-away: 30 (price missed zone or stale)",
        "Closed today: 271W / 15L / 0flat (expired-after-entry count: 25 unresolved; no-entry: 30)",
        "Needs review: 0"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.82,
      "reason_codes": ["repeated_losses", "correlation_cluster", "reduce_risk"],
      "data_missing": ["live_position_sizes", "account_equity"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto A/B PF 0.53, WR 9.4%, Total R -40R — systemically negative (reliable n=258)",
        "Longs PF 0.44 (n=240) — chronic underperformance; shorts PF 1.77 (n=17) only working",
        "Weekend mode: n=33, WR 11% — extra underperformance layer",
        "Scalp mode: 1W/13L — worst performing bucket",
        "Correlation cluster: BEL/ALICE/SYN all in momentum_breakout basket",
        "SYN: headline risk (Bitget delisting, no catalyst, extreme extension)",
        "BTW: MEXC-only, 90% long crowding, +97% 24h — extreme headline risk",
        "Late-session (21:41): new entries face overnight thin-liquidity gap on Saturday"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.85,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "crypto_swing_narrative_rs_momentum (primary): n=224, WR ~7.5%, PF ~0.44 — failing",
        "crypto_scalp_momentum_continuation: n=115, 1W/13L — worst bucket",
        "Shorts (crypto_failed_bounce_short): n=17, WR 28.6%, PF 1.77 — only working segment",
        "Weekend Y (n=33): WR 11% — underperforms weak mean",
        "crypto_intraday: n=60, WR 25% — moderate, better than swing longs"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.78,
      "reason_codes": ["wait_for_trigger", "shorts_preferred", "catalyst_backed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "No A-tier exists; all B-tier; longs systemically losing",
        "SOL only verified catalyst-backed long — price above entry zone (wait for pullback)",
        "NEAR short: WAITING, cleanest short structure available",
        "SYN: AVOID — confirmed no catalyst, exchange delisting, extreme overextension",
        "Shorts PF 1.77 — only working playbook; prefer shorts for new entries",
        "Late session: no new intraday entries at 21:41; only swing monitoring valid"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.78,
    "preferred_side": "shorts",
    "best_long_candidate": {
      "symbol": "SOL/USDT",
      "trigger": "pullback to $70.44–$70.73 entry zone; invalidation 1h close below $70.08",
      "reason": "Only verified catalyst-backed long: bitFlyer Japan listing June 24, tokenized equity 97% share, whale buy; do NOT chase above $71.43"
    },
    "best_short_candidate": {
      "symbol": "NEAR/USDT",
      "trigger": "failed bounce at $2.78–$2.81 resistance zone; invalidation above swing high",
      "reason": "B-tier short WAITING; best short structure; shorts PF 1.77 this week; normal crowding (no squeeze risk)"
    },
    "best_catalyst_candidate": {
      "symbol": "SOL/USDT",
      "trigger": "pullback to $70.44–$70.73 confirmed; bitFlyer listing approaching June 24",
      "reason": "Cleanest upcoming catalyst (Japan FSA-licensed exchange) + multiple institutional narratives"
    },
    "avoid_candidate": {
      "symbol": "SYN/USDT",
      "reason": "Pure speculative pump from ATL; NO catalyst confirmed externally; Bitget delisted June 18; price 3x forecast range ($0.047-$0.058); OI declining (short covering only); late-session reversal risk extremely high"
    },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.75 | `scheduler_fresh, catalyst_missing, report_stale` | advisory_only |
| market_regime | caution | 0.80 | `chop, mixed, wait_for_trigger` | advisory_only |
| catalyst_narrative | caution | 0.55 | `catalyst_missing, mapping_weak, stale_catalyst` | advisory_only |
| derivatives_squeeze | caution | 0.60 | `squeeze_risk, post_unwind_chop, funding_extreme` | advisory_only |
| technical_entry | caution | 0.70 | `entry_late, chase_risk, stale_before_entry` | advisory_only |
| execution_lifecycle | ok | 0.85 | `open_actionable, entered_unresolved, review_shadow` | advisory_only |
| risk_manager | caution | 0.82 | `repeated_losses, correlation_cluster, reduce_risk` | advisory_only |
| playbook_performance | caution | 0.85 | `playbook_failing, playbook_working, low_sample` | advisory_only |
| head_trader | caution | 0.78 | `wait_for_trigger, shorts_preferred, catalyst_backed` | advisory_only |

---

## 4. What Changed vs Previous Review (18:40 EEST)

**Previous review**: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-20_1840.md`

| Change | 18:40 | 21:41 | Assessment |
|---|---|---|---|
| Active signals | 26 | 23 (20 at cycle end + 3 post-cycle) | 6 closed during cycle run; 3 new post-cycle |
| Closed today (losses) | 271W/13L | 271W/15L | 2 new losses in 3h |
| Cycle | Post cycle_01_15-47 | cycle_01_19-07 completed (ok=16, failed=0) | New scalp/intraday reports generated |
| Catalyst mapping | 598 events (context) | 2,479 events, 21.6% mapped | **CRITICAL: mapping ratio collapsed** |
| SYN thesis | Watchlist/caution | **INVALIDATED externally** — Bitget delisted, no catalyst | Downgrade to AVOID |
| SOL status | B-tier 76 WAITING | B-tier 76 WAITING (unchanged) | Price drifted ~$70.8→$71.4; still above entry zone |
| EIGEN | In active signals | Not visible in current 23 signals | Likely expired/tracked-out during cycle |
| BTW | AVOID (extreme crowding) | AVOID (unchanged) | Carries forward |
| BTC price | ~$63.6K confirmed | ~$63.6K (unchanged, still range/chop) | No regime change |

**Thesis changes**: SYN is now INVALIDATED by external research. All other active theses unchanged. SOL remains strongest catalyst-backed but price drifted above entry zone — requires patience.

---

## 5. Catalyst Coverage

**CRITICAL: Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

- Total catalyst events today: **2,479**
- Mapped (non-null symbol): **536** (21.6%)
- Unmapped: **1,943** (78.4%) — well above 50% threshold
- Narrative baskets: **4** (delisting_thin_liquidity, rwa_narrative, ai_narrative, momentum_breakout)
- Unmapped top-3 headlines: Cannot decode (byte encoding error in JSONL — see TODO-CATALYST-JSONL-ENCODING)

**Notable catalysts confirmed this session**:
- **SOL**: Whale buy $16.55M (Lookonchain, ~15h old — stale but confirmed); bitFlyer listing June 24 (upcoming, external confirmed via Phemex)
- **BTC**: Japan BOJ rate hike absorbed (CryptoSlate); BSTR $2B Bitcoin treasury competitor (CryptoBriefing); network activity rising per CryptoQuant
- **ETH**: Tom Lee funding crisis denial (AMBCrypto) — positive sentiment, single source
- **Axelar bridge**: $4.7M exploit on Secret Network (CryptoBriefing/AMBCrypto) — basket-level risk event; no active crypto signal directly mapped
- **SMCI/USDT** `[legal_risk]`: Export-control indictment (SEC EDGAR FY2026) → AVOID any SMCI exposure
- **UNH/USDT** `[legal_risk]`: DOJ fraud investigation → AVOID any UNH exposure
- **Regulatory positive**: WhiteBIT MiCA Austria license; CLARITY Act progress (mixed reception)

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood**: range/chop (neutral) — BTC $63.6K, oscillating post-peak of $71K in early June. No clean trend. Breadth compressed at 46% EMA20 (below 50% midline).
- **Stocks mood**: closed (Saturday weekend)
- **Dominant narrative**: Institutional adoption resilience (SOL tokenized equity leadership, SoFi stablecoin on Solana, Cash App USDC); Bitcoin macro endurance (BOJ absorbed); regulatory progress mixed (CLARITY Act debate)
- **Preferred side now**: **shorts** + catalyst-backed longs only (specifically SOL on pullback to zone)
- **Best long candidate**: SOL/USDT — trigger: pullback to $70.44–$70.73 entry zone
- **Best short candidate**: NEAR/USDT — trigger: failed bounce into $2.78–$2.81 resistance
- **Best catalyst-backed candidate**: SOL/USDT — bitFlyer June 24 Japan listing is the cleanest upcoming catalyst
- **What to avoid**: SYN (no catalyst, exchange delisting, 3x overextension); BTW (MEXC-only, 90% crowding); any new intraday entries at 21:41; chasing BICO/ALICE/SYN above entry zones; new shorts on ALICE/BICO/BEL (negative funding = shorts already crowded, squeeze risk)
- **What would change the view**: BTC closes above $65K (breadth expansion → longs viable) · NEAR bounces and fails at $2.80 (short trigger) · SOL drops to $70.44 (long entry viable) · Fresh verified catalyst appears for any active signal (would strengthen)

---

## 7. Candidate Deep Dives

### 7.1 SOL/USDT — B-tier Swing WAITING (score 76) — Best Catalyst-Backed Long

**Status**: WAITING for entry (not triggered). Advisory only.

**Catalyst check (internal + external)**:
- Internal: Whale DAWHnv bought $16.55M → 234,898 SOL at avg $70.5 (Lookonchain, now ~15h old)
- External confirmed (Phemex June 2026): SOL captured **97% of tokenized equity spot trading volume**; SoFi launched first US bank stablecoin on Solana; Cash App USDC support on Solana; **bitFlyer (Japan, FSA-licensed) listing SOL June 24, 2026** — high-quality upcoming regulatory catalyst
- Contradiction check: No contradictions. All external sources confirm/strengthen thesis.

**Price reaction / chase check** (TradingView unavailable; using OHLCV/ATR):
- Price (19:39 intraday): $71.43
- Entry zone (swing): $70.44–$70.73 | Invalidation: 1h close below $70.08
- Price is **~$0.70 above entry zone top** (~0.85 ATR). Chase risk if entering now.
- Has price already reacted to catalyst? Yes — whale buy June 20 ~06:30 EEST pushed price up; holding above entry zone.
- Is this chasing? **Yes at $71.43.** Do NOT enter at market. Wait for zone touch.
- Overextended? Not on swing timeframe — $68.72 support below. ATR $0.65–$0.82. Within 2 ATR of EMA.
- Entry actionable NOW? **No** — only if pullback to $70.44–$70.73.
- What would invalidate? 1h close below $70.08.
- Late-session context: WAITING status means no fill tonight unless price retreats. Valid to carry overnight.
- SL: $70.08 (1h close) or structural $68.72.

**Verdict**: WAITING for entry · Best catalyst-backed long · Do NOT chase above $71.00 · bitFlyer June 24 upcoming catalyst remains valid

---

### 7.2 SYN/USDT — B-tier Swing WAITING (score 65.6) — **RED FLAG / AVOID**

**Status**: WAITING (no fill). **External research: AVOID — signal is high-contradiction-risk.**

**Catalyst check**:
- Internal: No catalyst detected. Momentum score 91.6 (technical only). Tags: relative_strength.
- External (CoinMarketCap AI, June 2026): SYN pump was **pure technical breakout from ATL $0.027** (reached ~June 13). Volume spike June 19: +787% to $93M — textbook speculative accumulation, no fundamentals.
- **Bitget delisted SYN/USDT effective June 18, 2026** — reduces liquidity/accessibility (bearish).
- Analysts attribute the pump to altcoin rotation cycle, no partnerships or protocol news.
- Price forecast June 2026: $0.047–$0.058. Current price $0.1533–$0.1623 = **~3x above forecast range**.

**Contradiction assessment**: HIGH. Signal (B-tier swing long) vs external reality (no catalyst, exchange delisting, 3x overextension, OI declining). This is the most significant contradiction of this review.

**Derivatives**: OI -18% while price up = SHORT COVERING ONLY (existing shorts buying to close). No new longs entering at scale. This is the WEAKEST continuation pattern — when short covering ends, no fresh demand.

**Price reaction / chase check**:
- Price $0.1533 vs entry zone $0.1439–$0.1504 — price ABOVE zone. Do not enter.
- 7d return +350-382% — massively overextended.
- Late-session: overnight mean reversion risk to $0.10–$0.12 range is plausible given speculation-only nature.

**HEADLINE RISK**: Exchange delisting (Bitget June 18) — negative liquidity event. Source: CoinMarketCap AI (single_source). **Verdict: contradicts signal thesis.**

**Final verdict**: **AVOID** — Downgraded from watchlist to AVOID. Signal tracked for system data purposes only. No action.

---

### 7.3 NEAR/USDT — B-tier Swing SHORT WAITING (score 65) — Best Short Candidate

**Status**: WAITING for entry. Best short candidate this session.

**Catalyst check**: No catalyst triggering short thesis. Technical weak RS (-4.5% to -6% vs BTC) in downtrend.

**Price / chase check**:
- Swing report (16:30): price ~$2.78, entry zone (failed bounce short): $2.78–$2.81, invalidation: 1h close above swing high (~$2.83+)
- OI: price down + OI down = deleveraging/long liquidation. **No squeeze risk on this short** (normal crowding, no upper wick flag, not thin liquidity flagged).
- Is this chasing? No — it's WAITING for a bounce entry. The setup is: short on failed bounce to resistance, not chasing breakdown.
- Actionable NOW? Only if price bounces into $2.78–$2.81 zone overnight. If price gaps straight down without bounce → stale/moved-away.
- Market mood alignment: Shorts PF 1.77; RS-weak short is best-performing playbook. ALIGNED.
- SL: 1h close above swing high (per signal parameters).

**Verdict**: WAITING for entry · Best short candidate · Valid overnight if NEAR bounces to resistance · Monitor on next check

---

### 7.4 BICO/USDT — B-tier Swing WAITING (score 68) — Risk-Elevated

**Status**: WAITING for entry (no fill).

**Catalyst check**: No verified catalyst. Tag: momentum_breakout basket (playbook: `wait_pullback`). +71.67% 24h, +119-129% 7d.

**Derivatives**: OI +106.4% (from swing report, Bybit Perp data); volume 0.16–0.27x average. Price up + OI up = fresh positioning, but crowding UNKNOWN with thin volume. This is a dangerous combination — large OI expansion on thin participation.

**Price / chase check**:
- Price $0.0412–$0.0436 vs entry zone $0.0382–$0.0403 — price ABOVE zone (not actionable now).
- +71% in 24h on below-average volume = suspect move.
- Late-session (21:41): not appropriate for new entry. 
- If price pulls back to zone overnight with volume expansion (>0.5x avg), re-evaluate only on next cycle.

**Verdict**: WAITING (conditional) · Not actionable at current price · Only consider if pull back to $0.0382–$0.0403 WITH volume confirmation · Crowding UNKNOWN keeps this at elevated risk

---

### 7.5 BEL/USDT — B-tier Swing TRIGGERED (score 65) — Active Monitoring

**Status**: TRIGGERED (entry filled). ENTERED UNRESOLVED (no TP/SL hit before window yet).

**Catalyst check**: No verified catalyst. BEL is in momentum_breakout basket (primary alongside ALICE/SYN). All basket members are no-catalyst.

**Derivatives**: OI +26%; funding negative multi-venue (Bybit: -0.00116, OKX: -0.00217, MEXC: -0.000609) — **shorts are crowded across venues** → partial squeeze protection for existing longs.

**Price / chase check**:
- 24h return +34-40%, 7d return +91-99%.
- Price (intraday 19:39): $0.1626; entry zone: $0.1534–$0.1598; support $0.1122; resistance $0.1850.
- Correlation risk: BEL/ALICE/SYN all in momentum_breakout basket. SYN reversal (now flagged as AVOID) could drag BEL sympathetically.
- TP1: $0.1767 (conditional). Invalidation: 1h close below $0.1457.
- Late session: NOT a new entry. This is monitoring only.
- Overnight risk: If SYN reverses hard, watch BEL for sympathetic selling. BEL has better fundamentals (confirmed OI expansion, multi-venue negative funding as protection).

**Verdict**: ENTERED UNRESOLVED · Monitor for TP1 $0.1767 or invalidation $0.1457 · SYN/ALICE cluster correlation risk is the main overnight threat · No new BEL entries at 21:41

---

### Excess Candidates (above max 5, listed for reference)

- **ALICE/USDT** (B-tier swing TRIGGERED): OI +119.75%, long/short 2.134, crowding UNKNOWN — squeeze risk on short side means shorts are dangerous; existing long position monitoring same framework as BEL. ENTERED UNRESOLVED.
- **WL…/USDT (score 75)** (B-tier swing, tp zone): Already in profit zone. Unidentifiable from truncated CLI output (likely WLD?). No new entry needed; monitoring for TP confirmation.
- **ME…/USDT (score 72)** (B-tier swing WAITING): Highest-score WAITING signal; full symbol undecodable from truncated output. Worth manual verification in next session.

---

## 8. Best Candidates Ranked

No A-tier. No clean actionable entry at 21:41 (late session; all WAITING signals above entry zones; intraday too late). Per PART 9 — best watches with exact triggers:

| Rank | Symbol | Side | Status | Trigger | Key Risk |
|---|---|---|---|---|---|
| 1 | SOL/USDT | Long | WAITING | Pullback to $70.44–$70.73 | Chase risk above $71.00; BTC overnight risk |
| 2 | NEAR/USDT | Short | WAITING | Failed bounce at $2.78–$2.81 | Bounce may not materialize overnight |
| 3 | BEL/USDT | Long | ENTERED | Monitor TP1 $0.1767 or invalidation $0.1457 | SYN cluster correlation; reversal drag |
| 4 | BICO/USDT | Long | WAITING (conditional) | Pull to $0.0382–$0.0403 + volume >0.5x avg | OI +106%, crowding unknown, thin volume |
| — | SYN/USDT | — | **AVOID** | No trigger | No catalyst, delisting, 3x overextension |

**Best long-watch**: SOL/USDT · trigger: pullback to $70.44–$70.73 (do not chase)
**Best short-watch**: NEAR/USDT · trigger: failed bounce at $2.78–$2.81
**Best catalyst-watch**: SOL/USDT · bitFlyer June 24 listing (Japan FSA-licensed)

---

## 9. Avoid / No Trade

**This decision window (21:41–next cycle) only.** Scanner / collection / tracking continue regardless.

- **SYN/USDT**: No catalyst, Bitget delisted June 18, price 3x forecast, OI declining. **AVOID.**
- **BTW/USDT**: MEXC-only, 90% long crowding, +97% 24h, no catalyst. **AVOID.**
- **All new intraday entries**: Too late at 21:41 for meaningful 4-24h capture. **PASS.**
- **ALICE/USDT (new entries only)**: OI +119.75% crowding UNKNOWN. Existing triggered position is different — monitor for TP. No new money.
- **Shorts on ALICE/BICO/BEL**: Negative funding = shorts already crowded on these. Short-squeeze risk. **NOT appropriate.**
- **Scalp mode**: PF 0.14 (1W/13L 14d) + late hour + weekend = triple skip.

---

## 10. Main Risks

1. **Catalyst mapping 21.6%** — review cannot rely on catalyst layer for final decisions; most signals are no-catalyst.
2. **Longs systemically losing** (PF 0.44, WR 8.6%) — historical edge is poor; position sizing should reflect this in any live session.
3. **SYN reversal risk** — if SYN reverses hard overnight, BEL/ALICE (momentum cluster) may see sympathetic pressure on existing triggered positions.
4. **Bybit OHLCV degraded** — swing report uses 0 Bybit rows; derivatives on Bybit-primary symbols may be stale or missing.
5. **Weekend thin liquidity** — wider spreads, larger wicks; TP levels may not fill cleanly; stops may get hunted.
6. **Catalyst JSONL encoding issue** — unmapped events contain byte errors (byte 0x90 in cp1252); valid catalysts may be lost in the 78.4% unmapped bucket (see TODO-CATALYST-JSONL-ENCODING).
7. **SOL overnight gap risk** — if BTC breaks below $62K, SOL likely breaks $70.08 invalidation overnight, collapsing the primary long thesis.

---

## 11. Action Plan — Next 4 Hours (21:41–01:30 EEST)

1. **Monitor existing TRIGGERED signals** (BEL/AXS/ALICE): watch for TP1 hits or invalidation levels. No new entries in cluster.
2. **SOL/USDT**: Watch for pullback to $70.44–$70.73. If price touches zone with structure (not gap-down), this is the cleanest long available. **Do NOT enter above $71.00.**
3. **NEAR short**: Watch for failed bounce into $2.78–$2.81 zone overnight. If NEAR bounces without breaking above swing high, short entry is valid per signal parameters.
4. **SYN/USDT**: **Do not act** on this signal regardless of system classification. External research overrides. Note in session journal.
5. **BTW/USDT**: **Do not act.** Avoid.
6. **New intraday entries**: None appropriate at 21:41. Pass until next morning cycle.
7. **Scheduler**: Expected to run next cycle overnight. Review output when cycle_02 or new day cycle appears.

---

## 12. Final Verdict Per Mode

| Mode | Verdict | Notes |
|---|---|---|
| Crypto scalp | NO TRADE — too late; low-confidence mode (PF 0.14); pass | Not actionable |
| Crypto intraday | NO TRADE — too late at 21:41 EEST | Monitoring existing only |
| Crypto swing | WATCH-ONLY for new entries; monitor TRIGGERED signals | SOL/NEAR specific triggers only |
| Stocks | CLOSED (weekend) — carry-forward planning only | JPM A/B-tier context for Monday |
| Overall | **CAUTION / WAIT-FOR-TRIGGER** | Advisory only; no auto-trade |

---

## 13. Sources

- [CoinDesk — Bitcoin Price Live](https://www.coindesk.com/price/bitcoin) — BTC $63,676 as of June 20, 2026; single_source; confirms
- [Phemex — Solana Price Today June 2026 + Alpenglow Upgrade](https://phemex.com/blogs/solana-price-today-june-2026-sol-alpenglow-upgrade-tvl-2030-outlook) — bitFlyer Japan listing June 24, SOL tokenized equity 97% share; single_source; confirms SOL catalyst
- [OpenPR — SOL Price Prediction June 2026 + 624K Token Unlock](https://www.openpr.com/news/4539754/sol-price-prediction-june-2026-solana-faces-624k-token-unlock) — SOL forecast $70.93–$81.27 for June 2026; single_source; context
- [CoinMarketCap AI — SYN Synapse Latest Updates](https://coinmarketcap.com/cmc-ai/synapse-2/latest-updates/) — SYN June pump confirmed no-catalyst (technical breakout from ATL); Bitget delisted SYN/USDT June 18, 2026; price forecast $0.047–$0.058; single_source; **contradicts signal thesis**
- [Lookonchain Telegram](t.me/lookonchain) — Whale DAWHnv $16.55M SOL buy (internal news_items, already logged)
- [CryptoBriefing — BSTR Bitcoin Treasury](https://www.cryptobriefing.com/) — BSTR $2B Bitcoin treasury competitor (internal, already in news_items)
- [AMBCrypto — Tom Lee ETH Funding](https://ambcrypto.com/) — Tom Lee "no funding crisis for ETH" (internal, already in news_items)

_All sources cited with title, source, date context, verification_status, and confirms/weakens/contradicts label. No fabricated TradingView observations. No uncited statistics._

---

## 14. Fix Requests / TODO

### TODO-CATALYST-MAPPING
- **issue:** Catalyst mapping critically low at 21.6% (536/2479 events). Intraday report context shows 723 events, swing shows 598 — but JSONL total is 2,479. Mapping may not run on all accumulated events.
- **evidence:** `data/catalysts/2026-06-20/catalyst_events.jsonl` — Python analysis: 21.6% mapping rate (536/2479)
- **suggested manual fix:** Audit the catalyst symbol resolver step (`catalyst-scan` pipeline); check if new inbound JSONL sources (Telegram, RSS) are bypassing the mapping pipeline. Run `python -m src.cli catalyst-scan --no-print` and inspect mapping counts per source.
- **priority:** high
- **first observed:** 2026-06-20 21:41 EEST

### TODO-CATALYST-JSONL-ENCODING
- **issue:** `catalyst_events.jsonl` has byte encoding errors preventing clean Python parsing (UnicodeDecodeError: byte 0x90 in cp1252 position 5629). Unmapped headlines read as '?' when using errors='replace'.
- **evidence:** `python -c "open('data/catalysts/2026-06-20/catalyst_events.jsonl')..."` → UnicodeDecodeError; confirmed via errors='replace' workaround
- **suggested manual fix:** Ensure the JSONL writer uses `encoding='utf-8'` explicitly. Sanitize Telegram source text before writing (strip or replace non-UTF8 bytes at ingest). Also add UTF-8 declaration in the reader.
- **priority:** medium
- **first observed:** 2026-06-20 21:41 EEST

### TODO-BYBIT-OHLCV
- **issue:** Bybit OHLCV fetching consistently failing (0 rows contributed, 40 failures in swing report). Derivatives layer falls back to MEXC for symbols that should have Bybit data (e.g., BICO, ALICE, BEL intraday report shows fallback_via_mexc).
- **evidence:** `data/reports/swing/2026-06-20_13-30_swing_report.md` §0: bybit ohlcv_fetched=0, failed=40; `data/reports/intraday/2026-06-20_16-39_intraday_report.md` §3: multiple fallback_via_mexc entries
- **suggested manual fix:** Check Bybit API key validity and rate limits in `config/`; verify endpoint paths haven't changed (Bybit API v5 changes); test `python -m src.cli check-exchange bybit` or equivalent; inspect `data/processed/market_summary/last_update.json` for Bybit error codes.
- **priority:** medium
- **first observed:** Prior reviews (carries forward to 2026-06-20 21:41 EEST)
