# Opus Enriched Review — post-close final daily review — Auto Cycle 23:15 EEST

> **Advisory only / no auto-trade. Sunday June 28, 2026. Post-close slot: daily wrap + overnight-into-Asia setup. Stocks: CLOSED (weekend). Crypto: live and active.**

---

## 1. Executive Summary

**Slot: post-close final daily review — advisory only / no auto-trade.**

Today's Sunday crypto session closed with BTC flat at ~$60,251 (F&G=18, Extreme Fear). Both BTC and ETH remain in sustained downtrend. Altcoin breadth weakened through the session: 47.4% above EMA20 in morning → 44.7% by late session. Dominant narrative: broad crypto selloff led by ETH/XRP/DOGE as tech stocks tumble; AI capital rotating away from crypto.

**What worked today:** ACT/USDT +62% 24h (strongest RS-leader); VELVET +270% 7d (MEXC-only speculative). MANTA/S/SYN showed relative strength. Short playbook edge confirmed: shorts PF=2.20 (+12R). Paper shadow B outperforming A forward-only (B +5.55R / A −26.97R, 3d).

**What failed:** PUMP swing long correctly avoided (token unlock risk; stopped cycle 5). BTC intraday short stopped. MEME swing short stopped. Scalp mode: 0W/4L, −4R (persistent failure — no new scalp entries until re-audit).

**Overnight-into-Asia setup:** BTC must defend $59,750–$60K support. If BTC breaks $59K → broad alt selloff; ZEC/BTC/ETH shorts extend. If BTC reclaims $61,500 → ZEC short squeeze risk; reduce short weight. ACT pullback to 0.0116–0.0124 is cleanest long-watch. ZEC bounce to 381–384 is cleanest short-watch. HYPE is catalyst-watch for Monday.

**Head Trader routing:** shorts preferred, catalyst-backed for longs. No scalp entries. No chasing VELVET/MEXC-only names. Weekend mode ends tonight.

ALWAYS-SCAN continues. Scanner, tracking, data collection, paper accounting all uninterrupted.

---

## 2. Data Used

| Source | File/CLI | Generated (EEST) | Age | Status |
|--------|----------|-----------------|-----|--------|
| Scheduler | scheduler.log | 23:14:41 | <1 min | **FRESH** |
| Latest cycle | cycle_05_22-12_summary.md | 23:14:40 | <1 min | **FRESH** |
| Scalp report | 2026-06-28_19-41_scalp_report.md | 22:41 | 34 min | **FRESH** |
| Intraday report | 2026-06-28_20-09_intraday_report.md | 23:09 | 6 min | **FRESH** |
| Swing report | 2026-06-28_14-06_swing_report.md | 17:06 | ~6h | **CARRY-FORWARD** (4–12h) |
| Stocks intraday | 2026-06-26_20-14 | Jun 26 23:14 | ~48h | **STALE** (weekend closed) |
| Stocks swing | 2026-06-26_15-06 | Jun 26 18:06 | ~53h | **STALE** (weekend closed) |
| Stocks invest | 2026-06-26_15-13 | Jun 26 18:13 | ~53h | **STALE** (weekend closed) |
| Catalyst events | data/catalysts/2026-06-28/ | 20:09 cycle | ~3h | **FRESH** (345 events, 4 baskets) |
| LLM crypto packet | llm_analysis_packet.md | 23:09 | 6 min | **FRESH** |
| Active signals | CLI live | 23:15 | live | 9 crypto B-tier active |
| Signal stats | CLI live | 23:15 | live | n=113, PF=1.31, +12R |
| External web | Intellectia.AI / MEXC News / Yahoo | 23:15 | live | BTC $60,035–60,251; F&G=18 |

> Swing report carry-forward (~6h); acceptable for post-close wrap. Stocks stale — weekend closed; Monday planning only. **External web research available and used.**

---

## 3. Scheduler / Data Freshness

- **Scheduler:** Last write 23:14:41 EEST (<1 min) — **FRESH** (threshold 3h)
- **Latest cycle summary:** cycle_05_22-12 completed 23:14:40 EEST — **FRESH**
- **Cycle 5 stats:** ok=27/27 steps, failed=0. Monitor running (background pid=22008, 90-min window)
- **Paper accounting:** scanned=1,803, written=1,803, resolved=1,803, errors=0
- **Paper structural TP:** processed=800 (STRUCTURAL=699, HYBRID=88, ATR_FALLBACK=13)
- **Paper structural stop:** processed=800 (be=405, lock=532, structure_moves=395)
- **Paper entry mode:** processed=800 (non_pullback=618: breakout=193, momentum=10, limit_then_taker=381; pullback=182; no_chase=31)
- **Paper shadow A/B (FORWARD only — valid):** B +5.55R / A −26.97R (3d, 99 B / 130 A trades). NOT_READY for promotion (5/6 criteria; 3d < 14d minimum). Backfill is look-ahead only.
- **Paper portfolio (bybit fee):** $5,057.40 (+$57.40, +1.15%). Zero-fee: +48.5%; MEXC: +15.23%; Conservative: −7.85%.
- **Untracked alerts:** NONE (cycle step 23 — all crypto alerts have backing proposed_signal)
- **Intelligence layer:** post_unwind_chop=42 (dominant), build_up=11, unknown=36, unwind=5, squeeze_expansion=2. Onchain: config/onchain.yaml MISSING.
- **Reddit social:** All 3 subreddits blocked (403)
- **Telegram paper-shadow digest:** Error persists (`TelegramNotifier.__init__()` missing config_path) — digest NOT sent. Paper monitor status: sent successfully.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "post_close",
  "as_of": "2026-06-28 23:15 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.88,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["onchain_config_missing", "stocks_stale_weekend", "reddit_social_blocked"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "scheduler.log mtime 23:14:41 EEST (<1 min)",
        "cycle_05 completed 23:14:40 EEST (27/27 ok)",
        "scalp 22:41 EEST — FRESH; intraday 23:09 EEST — FRESH",
        "swing 17:06 EEST (~6h) — CARRY-FORWARD",
        "stocks 48-53h old — weekend closed acceptable",
        "Reddit 403 all 3 subreddits; onchain.yaml not configured"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.82,
      "reason_codes": ["risk_off", "chop", "shorts_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC downtrend (all 3 reports), ETH downtrend",
        "BTC ~$60,251 flat (external confirmed: $60,035-60,251)",
        "ETH ~$1,571-1,585 (ETH/BTC=0.02632 x 60,251)",
        "F&G=18 Extreme Fear (improved from 13 at 18:39 back to 18)",
        "Altcoin breadth 44.7% EMA20 (weakened from 47.4% morning)",
        "VIX=18.41, SPY down, QQQ down (dashboard cycle 5 step 15)",
        "crypto_mode=chop; post_unwind_chop dominant: 42/96 symbols"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.60,
      "reason_codes": ["fresh_catalyst", "stale_catalyst", "narrative_supported", "mapping_weak"],
      "data_missing": ["catalyst_mapped_percentage_unknown"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "HYPE: Bitwise BHYP ETF live (NYSE + Xetra) — confirmed",
        "HYPE: Hyper Foundation $10M grants (USDH) — single_source",
        "SOL: whales $15M short (AMBCrypto) — bearish",
        "XRP: MiCA partial win — mixed",
        "BTC: US-Iran talks canceled — background risk",
        "STALE ARTICLE: 'Bitcoin dips rebounds past $102K' — BTC confirmed ~$60K; article from prior period",
        "ACT: momentum_breakout basket (<1h fresh) — no verified news catalyst",
        "345 events, 4 baskets; mapping % unknown (JSONL not read)"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["post_unwind_chop", "oi_supports", "funding_extreme"],
      "data_missing": ["oi_24h_mexc_only_unavailable", "liquidation_heatmaps_missing"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "post_unwind_chop dominant: 42/96 symbols",
        "ZEC: price down + OI up +4.34% — fresh shorts pressing; squeeze if reclaims $387",
        "ACT: OI +211% 24h (Bybit), funding -0.00103 (negative longs paying)",
        "VELVET: elevated long crowding, funding +0.000683",
        "squeeze_expansion: only 2 symbols — broad squeeze risk low"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["entry_late", "chase_risk", "clean_retest", "price_moved_away"],
      "data_missing": ["chart_unavailable_tradingview_mcp_not_loaded"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "ZEC: entry zone 381.22-384.00; current 379.98 — BELOW zone; needs bounce",
        "ACT: pullback zone 0.0116-0.0124; current 0.0127 — slightly above; not chasing",
        "VELVET: 270% 7d — extreme chase risk; MEXC-only",
        "MAGIC: 23.8% 24h + 2.83x volume — overextended >2 ATR from EMA20",
        "Weekend mode active: require retest, wider wicks expected",
        "TradingView / manual chart check unavailable (MCP not loaded)"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.80,
      "reason_codes": ["entered_unresolved", "review_shadow", "no_entry"],
      "data_missing": ["full_entry_prices_active_signals_cli_truncated"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "OPEN actionable: 0",
        "WAITING for entry: 0",
        "ENTERED UNRESOLVED: 26 (entered, no TP/SL before window — NOT missed entries)",
        "REVIEW/SHADOW: 183",
        "NO-ENTRY/STALE/MOVED-AWAY: 8",
        "Closed today: 302W / 10L / 0flat",
        "NEEDS REVIEW: 0",
        "Active B crypto: 9 (ZEC short, BTC short, ETH short, ETH long, BEL long, AAVE long, SOL long, HOT long, AXS long)",
        "INTEGRITY FLAG: ETH has BOTH B swing short AND B swing long simultaneously active"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["reduce_risk", "weekend_risk", "correlation_cluster", "headline_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Weekend signals: PF=0.57 (-3R) — underperforming; ends tonight",
        "Scalp: PF=0.00 (-4R) — no edge; avoid",
        "Longs: PF=1.00 (0R) — breakeven only",
        "Shorts: PF=2.20 (+12R) — clear edge",
        "Paper portfolio (bybit fee): +1.15% — marginal after fee drag",
        "US-Iran tensions (talks canceled) — overnight geopolitical risk",
        "SOL: $15M whale short contradicts B long signal",
        "PUMP stopped — avoid was validated"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": ["a_tier_sample_zero", "c_tier_sample_zero"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "swing: n=42, PF=1.65, +13R — WORKING (strongest mode)",
        "intraday: n=32, PF=1.20, +3R — marginally working",
        "scalp: n=39, PF=0.00, -4R — FAILING (0W/4L)",
        "shorts: n=37, PF=2.20, +12R — WORKING best direction",
        "longs: n=76, PF=1.00, 0R — breakeven",
        "weekend: n=15, PF=0.57, -3R — FAILING",
        "non-weekend: n=98, PF=1.46, +15R — WORKING",
        "B shadow forward: B +5.55R / A -26.97R (3d) — B outperforming"
      ]
    },
    {
      "agent": "head_trader",
      "overall_verdict": "caution",
      "confidence": 0.72,
      "preferred_side": "shorts",
      "best_long_candidate": {
        "symbol": "ACT/USDT",
        "trigger": "pullback to 0.0116-0.0124 + BTC stable >$59.5K + volume confirmation",
        "reason": "Strongest RS-leader +62% 24h; OI +211%; no catalyst so require retest structure, not chase"
      },
      "best_short_candidate": {
        "symbol": "ZEC/USDT",
        "trigger": "bounce to 381-384 entry zone (B signal active; current 379.98 below zone)",
        "reason": "Fresh shorts pressing (OI+4.34%, price down+OI up); unusual vol 2.08x; squeeze risk above $387"
      },
      "best_catalyst_candidate": {
        "symbol": "HYPE/USDT",
        "trigger": "pullback to support Monday + Bitwise BHYP ETF volume data",
        "reason": "Bitwise BHYP ETF live (NYSE + Xetra); $10M grants; perps_dex_narrative primary; wait_pullback playbook"
      },
      "avoid_candidate": {
        "symbol": "VELVET/USDT",
        "reason": "MEXC-only (confirmation=38%); +270% 7d pump; elevated long crowding; funding +0.000683; no catalyst"
      },
      "operator_action": "watch",
      "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
      "todo_count": 5
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.72,
    "preferred_side": "shorts",
    "best_long_candidate": { "symbol": "ACT/USDT", "trigger": "pullback 0.0116-0.0124 + BTC >$59.5K", "reason": "Strongest RS-leader +62% 24h; require retest" },
    "best_short_candidate": { "symbol": "ZEC/USDT", "trigger": "bounce to 381-384 entry zone (B active)", "reason": "Fresh shorts pressing, OI+4.34%, vol 2.08x" },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "Monday pullback + Bitwise ETF volume", "reason": "Bitwise BHYP ETF live + $10M grants; perps_dex basket" },
    "avoid_candidate": { "symbol": "VELVET/USDT", "reason": "MEXC-only; +270% 7d pump; elevated crowding; no catalyst" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|-------|---------|------------|--------------|-----------------|
| data_quality | ok | 0.88 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.82 | risk_off, chop, shorts_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.60 | fresh_catalyst, stale_catalyst, narrative_supported, mapping_weak | advisory_only |
| derivatives_squeeze | caution | 0.65 | post_unwind_chop, oi_supports, funding_extreme | advisory_only |
| technical_entry | caution | 0.65 | entry_late, chase_risk, clean_retest, price_moved_away | advisory_only |
| execution_lifecycle | ok | 0.80 | entered_unresolved, review_shadow, no_entry | advisory_only |
| risk_manager | caution | 0.75 | reduce_risk, weekend_risk, correlation_cluster, headline_risk | advisory_only |
| playbook_performance | caution | 0.72 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.72 | synthesis of all eight | advisory_only |

---

## 4. What Changed vs Previous Review

_Previous: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-28_1839.md` (US open reaction, 18:39 EEST)_

| Item | 18:39 EEST | 23:15 EEST | Change |
|------|------------|------------|--------|
| Active crypto B signals | ~13 | 9 | −4 (3 stopped cycle 5) |
| F&G | 13 (Extreme Fear) | 18 (Extreme Fear) | Slight improvement |
| BTC price | ~$60,065 | ~$60,251 | Flat (+0.3%) |
| ETH price | ~$1,580 | ~$1,571–1,585 | Flat |
| PUMP swing long | AVOID (correct) | CLOSED (stopped) | ✓ Avoid validated |
| BTC intraday short | ACTIVE | CLOSED (stopped) | Invalidated |
| MEME swing short | ACTIVE | CLOSED (stopped) | Invalidated |
| ZEC B swing short | SHORT-WATCH | STILL ACTIVE | Thesis unchanged |
| JTO B swing long | NO-ENTRY (price above entry) | Likely NO-ENTRY/MOVED AWAY | Still above entry |
| Signal stats PF | 1.38 / +14R | 1.31 / +12R | Degraded by 3 stops |
| Catalyst events | 315 events, 3 baskets | 345 events, 4 baskets | +30 events, +1 basket |
| B shadow forward | B +3.63R / A −19.8R | B +5.55R / A −26.97R | B continues outperforming |
| ACT 24h return | ~84% (swing) | ~62% (intraday 23:09) | Normalizing; still RS leader |

**New catalysts:** Hyper Foundation $10M USDH grants (CryptoBriefing, fresh); momentum_breakout basket added (ACT/VELVET/SYN, fresh <1h). US-Iran talks cancellation confirmed background context.

**⚠ Stale RSS article detected:** "Bitcoin dips then rebounds past $102K" — BTC confirmed ~$60K, not $102K. Article from prior period (likely Q1 2026). Flagged as TODO.

**Thesis changes:** ZEC short UNCHANGED (cleanest active short). BTC short UNCHANGED. PUMP: correctly avoided. SOL long: new context — whale $15M short adds contradiction risk. ETH: BOTH B swing short AND B swing long simultaneously active → lifecycle conflict.

---

## 5. Catalyst Coverage

- **Total catalyst events today:** 345 (cycle 5, step 4)
- **Narrative baskets:** 4 — `delisting_thin_liquidity`, `perps_dex_narrative` (HYPE primary), `ai_narrative` (NEAR/RENDER/TAO/FET primary), `momentum_breakout` (ACT/VELVET/SYN primary)
- **Mapped symbols visible in reports:** SOL, BTC, XRP, HYPE, ETH, WIF, ZEC, UNH (~10–15 distinct symbols)
- **⚠ Mapping percentage unknown** — cannot compute precisely without reading full JSONL. Based on visible report coverage (~10–15 mapped symbols vs 345 events), mapping quality likely below 50% for tail events. **Use catalyst layer as context, not final decision this run.** (See TODO-CATALYST-MAPPING-STATS)
- **Notable confirmed catalysts:**
  - HYPE: Bitwise BHYP ETF live (NYSE + Deutsche Borse Xetra) — institutional, significant
  - HYPE: Hyper Foundation $10M grants (USDH shutdown mitigation) — single_source
  - BTC: "Samson Mow says bitcoin bottom is in" (CoinDesk) — single_source, sentiment only
  - BTC: US-Iran talks canceled (CryptoBriefing) — geopolitical background risk
  - SOL: Whales bet $15M against SOL (AMBCrypto) — bearish
  - XRP: MiCA partial win / not full license (CryptoSlate) — mixed
  - UNH: DOJ criminal probe + Optum Rx probe (QuiverQuant / Fierce Healthcare) — dual-source → **STOCKS AVOID**
- **⚠ Stale RSS article:** "Iran launches missile and drone strikes... Bitcoin dips then rebounds past $102K" (CryptoBriefing) — BTC confirmed at ~$60K via external search. Article from prior period. RSS date filtering may be allowing re-circulation.

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** chop / risk-off — BTC ~$60,251 flat, both trends down, F&G=18 Extreme Fear, breadth 44.7% EMA20 (weakening through day), VIX=18.41
- **Stocks mood:** CLOSED (weekend). Monday open context: SPY down, QQQ down, VIX=18.41. Open with caution Monday 16:30 EEST.
- **Dominant narrative:** Broad crypto selloff (ETH/XRP/DOGE leading down); AI capital rotation away; US-Iran background tension; HYPE and ACT as isolated alpha pockets
- **Preferred side now:** **shorts** — data confirms (PF=2.20, +12R); longs breakeven (PF=1.00); catalyst-backed or RS-leader longs on pullback only
- **Best long candidate:** ACT/USDT — trigger: pullback to 0.0116–0.0124 + BTC holds $59.5K + volume returns. Strongest RS leader today.
- **Best short candidate:** ZEC/USDT — trigger: bounce to 381–384 entry zone (B signal active; current 379.98 below zone). Fresh shorts building.
- **Best catalyst-backed candidate:** HYPE/USDT — Bitwise BHYP ETF live + $10M grants. Wait-pullback playbook. Do not chase overnight.
- **What to avoid:** VELVET (MEXC-only parabolic); scalp mode entries (PF=0.00); weekend long entries (PF=0.57); all MEXC-only listings with no anchor
- **What would change the view:** BTC reclaims $61,500 → reduce short bias, ZEC squeeze risk. BTC breaks $59,000 → increase short weight, defer all long-watches.

---

## 7. Candidate Deep Dives

### 7.1 ZEC/USDT — B Swing Short (Active, WAITING for entry bounce)

**Status:** B swing short — WAITING FOR ENTRY. Weekend=Y. Current price 379.98 is BELOW entry zone 381.22–384.00 (no trigger yet).

**Setup:** "Price down + OI up" = fresh shorts pressing. Unusual volume 2.08x. Setup quality 67.4/100. RR 1.84R. Targets: 373.80 / 367.63 / 361.45. Invalidation: 1h close above 387.39.

**Catalyst:** No fresh verified catalyst. Prior swing report: whale shorted $4.92M ZEC (AMBCrypto). Bearish catalyst in play.

**Chase risk?** NO — price below entry zone; requires bounce to 381–384 to trigger.

**Squeeze risk?** YES — OI up while price down = shorts loaded. If BTC reverses and ZEC reclaims $387.39 → squeeze. Keep that as hard invalidation.

**Mood aligned?** YES — shorts preferred; fresh derivatives support.

**Verdict:** WAITING FOR ENTRY. Alert at 381.22 bounce. Cleanest short-watch on desk. Stop: 387.39.

---

### 7.2 ACT/USDT — Long-Watch (C-tier)

**Status:** C-tier WATCHLIST only. No B signal. Strongest RS-leader name.

**Setup:** +62% 24h, +63% RS vs BTC, OI +211% (Bybit), funding −0.00103 (negative). Current price 0.0127. Pullback zone: 0.0116–0.0124. Intraday score 62.0/100. Invalidation: 1h close below 0.0106.

**Catalyst:** In momentum_breakout basket (fresh <1h). NO verified news catalyst. No-catalyst intraday in chop = net-negative (PF=0.70, WR=23% per playbook warning).

**Chase risk?** Current 0.0127 slightly above pullback zone 0.0116–0.0124. Do NOT enter at market. +62% day move in chop = elevated mean reversion risk.

**Verdict:** LONG-WATCH. Trigger: pullback to 0.0116–0.0124 + BTC stable + volume returns. Require structure, not momentum. Weekend mode ends tonight — reassess Monday.

---

### 7.3 ETH/USDT — LIFECYCLE CONFLICT (B Swing Short + B Swing Long Both Active)

**Status:** ⚠ INTEGRITY FLAG — Two simultaneous B signals: ETH B swing short AND ETH B swing long. Both active in CLI. ETH at ~$1,571–1,585.

**Mood alignment:** risk-off/chop → ETH short is mood-aligned. However $1,571 could be support for mean-reversion long. Cannot determine which signal is the current thesis without knowing entry/SL/TP details (CLI truncated).

**Verdict:** MANUAL REVIEW REQUIRED. Cannot recommend either direction. If ETH breaks $1,540 → short thesis strengthens. If holds $1,571 → reassess both. Treat as CONFLICTED until resolved in manual session.

---

### 7.4 BTC/USDT — B Swing Short (Active, likely ENTERED)

**Status:** B swing short active. Entry zone from CLI fragments ~$62,000–63,500 range. Current BTC ~$60,251 = below entry zone → signal likely ENTERED and sitting ~$2K below entry (roughly +1–2R depending on ATR).

**Context:** Sustained downtrend. US-Iran talks canceled adds overnight geopolitical volatility risk (spike possible).

**Verdict:** Hold if entered. Do not add. Monitor TP at ~$59K area. If BTC reclaims $61,500 → re-check stop vs entry.

---

### 7.5 HYPE/USDT — Catalyst-Watch (No Active Signal)

**Status:** C-tier / CATALYST-WATCH. perps_dex_narrative basket primary. Wait-pullback playbook.

**Catalysts:** Bitwise BHYP ETF live (NYSE Arca + Deutsche Borse Xetra) — significant institutional catalyst. Hyper Foundation $10M grants to ease USDH stablecoin shutdown — protocol support.

**Setup:** No specific entry zone this cycle (HYPE not in active signals). Playbook explicitly says "wait_pullback" — correct framing.

**Verdict:** CATALYST-WATCH. Best-positioned name for fundamental-backed entry. Do not chase overnight. Revisit Monday with fresh cycle data and Bitwise ETF flow data.

---

## 8. Best Candidates Ranked

| Rank | Symbol | Dir | Mode | Status | Trigger |
|------|--------|-----|------|--------|---------|
| 1 | ZEC/USDT | Short | Swing | B active — WAITING for bounce 381–384 | Bounce to 381–384 |
| 2 | BTC/USDT | Short | Swing | B active — likely ENTERED (~$62K) | Hold; TP ~$59K |
| 3 | ACT/USDT | Long | Intraday | C-tier LONG-WATCH | Pullback 0.0116–0.0124 |
| 4 | HYPE/USDT | Long | Swing | CATALYST-WATCH | Monday pullback + ETF data |
| 5 | ETH/USDT | Conflict | Swing | MANUAL REVIEW (lifecycle conflict) | Resolve long vs short first |

No OPEN actionable positions (paper monitor: 0 open actionable). ZEC is cleanest short-watch; ACT is cleanest long-watch; both require entry triggers before action.

---

## 9. Avoid / No Trade (this window only — scanning continues)

| Symbol / Category | Reason |
|-------------------|--------|
| VELVET/USDT | MEXC-only; +270% 7d parabolic; elevated crowding; funding +0.000683; no catalyst — avoid both sides |
| Scalp mode entries | PF=0.00, −4R, 0W/4L — in re-audit; no new scalp B entries |
| SOL long (active B) | B signal active BUT whale $15M institutional short directly contradicts; caution |
| MEXC-only listings | Weekend thin liquidity + no anchor = avoid (VELVET/AIXDROP/BTW/SLX/BDX/ARX/SKYAI) |
| Weekend long entries | PF=0.57 (−3R); mode ends tonight — defer new longs to Monday unless very clean |

**Not a stop-system command. Scanner continues in all conditions.**

---

## 10. Main Risks

1. **BTC loses $59,750–$60K support** → broad alt selloff; ACT long-watch invalid; short targets extend
2. **Geopolitical escalation (US-Iran):** Talks canceled (current); overnight military events could spike BTC volatility (initial drop + possible safe-haven rebound)
3. **ZEC short squeeze:** Fresh shorts loaded (OI up). ZEC reclaims $387.39 → squeeze. Hard invalidation.
4. **SOL whale short ($15M):** Institutional bear contradicts B swing long; may stop out signal
5. **ETH signal conflict:** Both B long and short active; potential PnL distortion in paper tracking
6. **Stale Iran/$102K article in RSS:** Potential contamination; BTC confirmed ~$60K not $102K
7. **Telegram paper-shadow digest error:** Persisting `TelegramNotifier.__init__()` config_path error
8. **Weekend thin liquidity through midnight:** Wider wicks, larger slippage on stops

---

## 11. Action Plan — next 4 hours (overnight / Asia session)

1. **No new entries overnight** (23:00–06:00 EEST) — thin liquidity, weekend mode, 0 open actionable
2. **ZEC short:** Alert at 381.22 bounce for entry trigger. Stop 387.39.
3. **BTC short:** If entered at ~$62K, position in profit. Hold; TP ~$59K. Do not add.
4. **ACT long-watch:** Alert at 0.0116. Assess Monday if BTC stable + ACT pulls back.
5. **HYPE catalyst-watch:** Review Monday 16:30 EEST with Bitwise ETF flow data.
6. **ETH conflict:** Flag for manual review. Resolve long vs short before Monday session.
7. **SOL long signal:** Monitor with extra caution given whale position.
8. **Weekend mode ends midnight → 04:30 EEST:** Fresh cycle expected. Scalp re-audit needed.
9. **If BTC breaks $59K:** Short signals extend; all long-watches deferred; re-review MANTA/S/JTO.

---

## 12. Final Verdict per Mode

| Mode | Verdict | Confidence | Notes |
|------|---------|------------|-------|
| **Scalp** | DO NOT TRADE | low | PF=0.00, −4R — playbook in re-audit |
| **Intraday** | WATCHLIST / WAIT | medium | 0 active B intraday; ZEC short-watch via bounce only |
| **Swing** | HOLD ACTIVE / WAIT-FOR-ENTRY | medium | 9 B active; ZEC waiting bounce; BTC in profit; ETH conflict pending |
| **Stocks** | NOT APPLICABLE | n/a | Weekend closed; Monday planning only |
| **Crypto overnight** | SHORTS PREFERRED | medium | ZEC/BTC short bias; ACT long only on pullback; avoid VELVET |
| **Asia setup** | WAIT, REASSESS 04:30 EEST | medium | No new entries; monitor BTC $59.5–60K support |

---

## 13. Sources

**Internal:**
- `data/scheduled_runs/2026-06-28_default_schedule/cycle_05_22-12_summary.md`
- `data/reports/scalp/2026-06-28_19-41_scalp_report.md`
- `data/reports/intraday/2026-06-28_20-09_intraday_report.md`
- `data/reports/swing/2026-06-28_14-06_swing_report.md` (carry-forward)
- `data/processed/llm_analysis_packet.md`
- `python -m src.cli active-signals --asset-class crypto` (live 23:15)
- `python -m src.cli signal-stats --asset-class crypto` (live 23:15)
- `OPUS_ENRICHED_REVIEW_AUTO_2026-06-28_1839.md` (previous review)

**External (verified this run):**
- [Cryptocurrency Market Update June 28, 2026](https://intellectia.ai/news/crypto/cryptocurrency-market-update-for-june-28-2026) — BTC $60,035, ETH $1,571
- [Bitcoin analysis over the weekend, June 28 2026](https://investinglive.com/Cryptocurrency/bitcoin-analysis-over-the-weekend-28-june-2026-20260628/) — BTC weekend analysis
- [Crypto Market Today June 28: BTC Flat at $60,251, F&G=18](https://www.mexc.com/news/1179533) — MEXC News (search result; fetch failed)
- [Bitcoin Just Dropped Below $60,000](https://www.fool.com/investing/2026/06/28/bitcoin-below-60000-history-says-this-happens-next/) — Motley Fool, June 28 2026
- [BTC-USD Price History](https://finance.yahoo.com/quote/BTC-USD/history/) — Yahoo Finance

---

## 14. Fix Requests / TODO

### TODO-STALE-IRAN-ARTICLE
- **issue:** RSS feed contains "Iran launches missile and drone strikes on US bases, Bitcoin dips then rebounds past $102K" (CryptoBriefing) but BTC confirmed ~$60K; article from prior period (likely Q1 2026)
- **evidence:** intraday_report §5 news; external WebSearch confirms BTC at $60,035–60,251 on June 28 2026
- **suggested manual fix:** Add date-based filtering to RSS ingestion (exclude articles >48–72h); audit CryptoBriefing RSS for re-circulation behavior
- **priority:** medium
- **first observed:** 2026-06-28 23:15 EEST

### TODO-CATALYST-MAPPING-STATS
- **issue:** Catalyst mapping percentage (mapped/unmapped) not surfaced in cycle summary; cannot determine if >50% unmapped threshold is breached without reading full JSONL
- **evidence:** cycle_05 step 4 output: "events=345, baskets=4" — no mapped/unmapped breakdown
- **suggested manual fix:** Add mapped_count / unmapped_count / unmapped_pct to catalyst scan CLI output and cycle summary step; expose in reports §5b header
- **priority:** medium
- **first observed:** 2026-06-28 23:15 EEST

### TODO-SCALP-PLAYBOOK-REAUDIT
- **issue:** Scalp mode 0W/4L (−4R, PF=0.00) over n=39 sample — consistently failing
- **evidence:** signal-stats CLI: scalp mode PF=0.00, totalR=-4.0; scalp report header: "TP1/2h horizon mismatch caps capture (1W/7L over 14d, PF=0.14)"
- **suggested manual fix:** Full audit of scalp A/B signals; consider pausing scalp signal issuance or requiring catalyst confirmation; re-evaluate TP1 distance vs typical captured MFE (1.86R TP1 vs 0.54R captured MFE); re-audit at ≥20 closed scalp A/B signals
- **priority:** high
- **first observed:** Recurring; confirmed 2026-06-28 23:15 EEST

### TODO-ETH-SIGNAL-CONFLICT
- **issue:** ETH/USDT has BOTH B swing short AND B swing long active simultaneously
- **evidence:** active-signals CLI: 2 ETH rows (mode=swing, dir=sh and dir=lo, both B tier)
- **suggested manual fix:** Investigate issuance order; add conflict guard in signal lifecycle (prevent opposite-direction B signal on same asset+mode while one active); close stale signal in manual review session
- **priority:** high
- **first observed:** 2026-06-28 23:15 EEST

### TODO-TELEGRAM-PAPER-SHADOW-DIGEST
- **issue:** Paper-shadow digest fails: `TelegramNotifier.__init__()` missing config_path; digest never sent
- **evidence:** cycle_05 step 14: "send error: TelegramNotifier.__init__() missing 1 required positional argument: 'config_path'"
- **suggested manual fix:** Fix TelegramNotifier constructor call in paper-shadow digest script to pass config_path; mirror working pattern from paper_monitor_status (step 25 succeeds)
- **priority:** medium
- **first observed:** 2026-06-28 18:39 EEST (recurring)
