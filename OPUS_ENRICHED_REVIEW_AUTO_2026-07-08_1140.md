---
REVIEW: OPUS ENRICHED REVIEW — ⚠ ADVISORY ONLY — NO EXECUTION
SLOT: Europe / pre-US context · 2026-07-08 · 11:40 EEST
WRITTEN: 2026-07-08 11:40 EEST
PREV REVIEW: 2026-07-08 04:47 EEST (crypto overnight / Asia review)
STATUS: AUTOMATED SCHEDULED RUN — NO HUMAN IN SESSION
---

# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:40 EEST

## 1. Executive Summary

**Slot: Europe / pre-US context — advisory only / no auto-trade.** It is 11:40 EEST (~04:40 ET) — US cash markets are still closed; all stocks data below is pre-market/planning context only. Crypto is the live actionable class.

**Regime has cooled from risk-on to range/chop since the 04:40 review.** BTC/ETH both flipped from uptrend to range, altcoin breadth above EMA20 fell from 55.8%→38.6-43.2% (above EMA50: 67.4%→52.3%). Internal macro/geopolitics risk score jumped **63→97/100** on an escalating Iran/Strait-of-Hormuz story — externally verified: Iran fired on ships in the Strait ~19h ago, Brent crude +1.64% to $73.17, but Bitcoin's reaction is described externally as "muted"/"subdued" (BTC has not broken its internal range). No panic, but a genuine risk-off headwind.

**No A-tier signals anywhere** (crypto or stocks). The same **3 crypto intraday-B positions remain OPEN** and unchanged since the last review: SPELL/USDT, BANANA/USDT, ZEC/USDT (all long). Zero new triggers this cycle (`track-signals`: updated=0). Crypto scalp remains correctly policy-disabled (`config/crypto_quality_overlay.yaml: disabled: true`) after a confirmed net-negative bucket (PF 0.47, avgR −0.1175, n=159).

**UNH carries a serious, externally-reconfirmed legal/headline risk**: DOJ criminal *and* civil investigation into Medicare Advantage billing (alleged inflated diagnoses), extending to Optum Rx and physician reimbursement, stock down >45% YTD, CEO departure in May, suspended earnings guidance. UNH appears repeatedly (always **long**, always C-tier) across the internal intraday/swing/invest book — treat as a hard **AVOID / manual review** regardless of tier or score. SMCI carries forward as a softer legal-risk caution with no fresh evidence this cycle.

**ZEC's catalyst is externally reconfirmed and strengthened**: Zcash's Ironwood shielded-pool / "Project Tachyon" mathematical-proof effort against hidden counterfeit bugs is corroborated externally (ZEC ~$483, +8% 24h, reclaimed $500 briefly), and current external whale positioning is described as **long-biased net accumulation** — this appears to supersede the older internal "$14.9M whale short bet" story, which should be treated as stale, not a live contradiction.

Catalyst mapping is weak this run (79.2% unmapped, 292/1401 mapped) — use the catalyst layer as context, not as a final-decision input.

---

## 2. Data Used

| Source | File / Timestamp | Age at 11:40 EEST | Quality |
|--------|-------------------|--------------------|---------|
| Scalp report | `2026-07-08_06-53_scalp_report.md` (gen 09:53 EEST; filename in UTC) | ~1h47m | FRESH |
| Intraday report | `2026-07-08_06-59_intraday_report.md` (gen 09:59 EEST) | ~1h41m | FRESH |
| Stocks intraday | `2026-07-08_07-06_stocks_intraday_report.md` | ~1h34m est. | FRESH but pre-market / planning-only (US cash market closed) |
| Crypto swing | `2026-07-07_02-03_swing_report.md` (gen ~05:03 EEST 2026-07-07) | ~33h37m | **STALE ✗** (>14h; 5th+ consecutive review flagging this, worsening) |
| Stocks swing/invest | `2026-07-02_13-0x` | ~6d | **STALE ✗** (excluded) |
| Cycle summary | `cycle_09_09-47_summary.md` (in `2026-07-07_default_schedule/`, day-rollover naming) | ~1h30m | FRESH, 32/32 steps OK, monitor window 90min |
| Paper monitor | `reports/PAPER_MONITOR_STATUS_LATEST.md` (mtime 10:09 EEST) | ~1h31m | FRESH |
| Previous review | `OPUS_ENRICHED_REVIEW_AUTO_2026-07-08_0440.md` (crypto overnight/Asia) | ~7h | CONTEXT — compared in §4 |
| Catalyst events | `data/catalysts/2026-07-08/catalyst_events.jsonl`, latest cycle file `catalyst_cycle_06-59.md` | ~1h41m | FRESH; 1401 events cumulative today, 292 mapped (20.8%), 3 active baskets |
| DB queries | `db/crypto_ai_desk.sqlite` (`news_items`, `proposed_signals`, read-only) | live | ZEC catalyst, UNH legal news, SMCI (no fresh hits) confirmed |
| External: ZEC catalyst | Coinpedia/KuCoin/Coinbase (WebSearch) | live | multi-source, consistent with internal Orchard/Tachyon story; whale-short internal story appears superseded |
| External: BTC/Iran-Hormuz macro | CoinDesk, Al Jazeera, BeInCrypto, OANDA (WebSearch) | live | multi-source; confirms escalation, confirms BTC "muted" reaction |
| External: UNH DOJ probe | Yahoo Finance, The Hill, TipRanks, FierceHealthcare, Medical Economics (WebSearch) | live | multi-source, primary company confirmation via SEC filing — severity confirmed and exceeds internal single-headline read |

**Notes**: TradingView/manual chart check unavailable — all technical levels from local OHLCV/ATR/EMA. Onchain config missing, social attention missing (Reddit sources 403-blocked). Root-level `data/crypto_ai.db` / `data/crypto_ai_desk.db` are stubs — live DB is `db/crypto_ai_desk.sqlite`.

---

## 3. Scheduler / Data Freshness

- **Last completed cycle**: `cycle_09_09-47_summary.md` — started 09:47:05, finished 10:11:29 EEST (~1h29m before this review), 32/32 steps OK, 90-min monitor window.
- **Scheduler health**: FRESH — not deferred. Live monitor logs (`crypto_monitor_*.log`, `stocks_monitor_*.log`) show activity as recent as 11:37-11:40 EEST, i.e. essentially real-time. (Note: freshest scheduler.log/cycle files still live under the `2026-07-07_default_schedule/` folder due to the day-rollover naming quirk — carried-forward TODO, see §14.)
- **Paper monitor status** (operator vocabulary, from `PAPER_MONITOR_STATUS_LATEST.md`, ~1h31m old):
  - OPEN actionable: **3** (SPELL/USDT, BANANA/USDT, ZEC/USDT — all crypto intraday B, long, entry filled, monitoring TP/SL)
  - WAITING for entry: **0**
  - REVIEW/SHADOW: **133**
  - ENTERED UNRESOLVED (entry filled, no TP/SL before window — NOT missed entries): **15**
  - NO-ENTRY / STALE / MOVED-AWAY: **45**
  - CLOSED: **379 WIN / 52 LOSS / 0 FLAT**
  - NEEDS REVIEW: **0**
- **Untracked legacy alerts**: **0** today (stable — matches last review).
- **Crypto week signal-stats** (A/B, unexpired+all): sample 427, triggered 407, WR ~15%, PF 1.4327, avgR 0.1247, totalR 35.91. By mode: **scalp PF 0.474/avgR −0.1175 (n=159, net-negative, correctly policy-disabled)**, intraday PF 1.668/avgR +0.194 (n=162, working), swing PF 1.852/avgR +0.304 (n=106, working).
- **Stocks week signal-stats**: intraday PF 0.813/avgR −0.047 (n=177, net-negative). tier=C triggered winrate **6-7%** (n=180, reliable) — confirms C-tier should never be treated as actionable. tier=B n=14 (weak sample) winrate 0%, PF 0.00 — small-sample but worth a TODO watch.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-07-08 11:40 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["onchain_config_missing", "tradingview_unavailable", "social_attention_missing"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Cycle 09 (09:47) finished 10:11:29 EEST, 32/32 OK, ~1h29m before this review",
        "Scalp/intraday/stocks-intraday reports FRESH (~1h34m-1h47m)",
        "Crypto swing STALE ~33h37m (last gen 2026-07-07 ~05:03 EEST) - 5th+ consecutive review flagging, worsening",
        "0 untracked legacy alerts today (stable vs last review)"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["risk_off", "chop", "wait_for_trigger", "mixed"],
      "data_missing": ["etf_flows", "dxy_yields", "onchain_whale_flows"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC trend: range, ETH trend: range (internal intraday report); altcoin breadth 38.64-43.18% above EMA20 (down from 55.81% at 04:40), 52.27% above EMA50 (down from 67.44%)",
        "Macro risk score 97/100 (6 risk-off hits, 0 risk-on, 3 calendar/watch) - up sharply from 63/100 at 04:40",
        "External (CoinDesk/BeInCrypto/OANDA, WebSearch): Iran fired on ships in Strait of Hormuz ~19h ago, Brent crude +1.64% to $73.17, BTC reaction described as muted/subdued - no breakdown",
        "Stocks market closed at this hour (~04:40 ET) - no fresh regime read, pre-market/planning only"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["fresh_catalyst", "catalyst_confirmed", "mapping_weak", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "ZEC Orchard/Ironwood 'Project Tachyon' bug-proof catalyst reconfirmed externally (Coinpedia/KuCoin, multi-source), ZEC ~$483 +8% 24h",
        "External whale positioning for ZEC now described as long-biased net accumulation - internal '$14.9M whale short' story (2026-07-07) appears stale/superseded, not a live contradiction",
        "Catalyst mapping weak this run: 1401 events today, 292 mapped (20.8%), 1109 unmapped (79.2%) - above the 50% weak threshold",
        "3 active narrative baskets: delisting_thin_liquidity (avoid_low_liquidity, no primary), perps_dex_narrative (HYPE primary, wait_pullback, HYPE also carries an operator-review flag for an unrelated phishing/scam-drain headline), ai_narrative (NEAR/RENDER/TAO/FET, related_beta_rotation)"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "oi_supports", "funding_extreme", "data_unavailable"],
      "data_missing": ["oi_24h_change (non-SPELL symbols)", "liquidation_heatmap", "order_book_depth"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "SPELL/USDT: funding -0.0157 (mexc), OI 24h +90.74%, long/short 1.65, crowding elevated/unknown - fresh aggressive long positioning confirms the trend but is stretched",
        "HMSTR/USDT: price down -38.9% 24h + OI up = fresh shorts pressing, possible squeeze if price reclaims; already >2 ATR from EMA20, do-not-chase per system",
        "ZEC/BANANA: funding modest, no extreme readings this cycle",
        "OI 24h change largely n/a for most tracked symbols this cycle - standing blindspot"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["entry_late", "chase_risk", "overextended", "stale_before_entry"],
      "data_missing": ["tradingview_manual_check"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "SPELL/USDT +18.7% 24h, RS vs BTC/ETH leader (score 92), entry plan explicitly flags chase risk - already OPEN (entered), now monitor-only, not a fresh entry decision",
        "ZEC/USDT +6.7% 24h (score 74), same chase-risk flag, already OPEN",
        "HMSTR/USDT short setup (score 85 raw / 35.5 after entry-quality penalty) explicitly rejected by the system: >2 ATR from EMA20, 'do not chase', converted to watchlist-only pending pullback",
        "No fresh B-tier triggers this cycle (track-signals: updated=0)"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["open_actionable", "review_shadow", "entered_unresolved", "no_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Paper monitor (10:09 EEST): OPEN_ACTIVE=3 (SPELL, BANANA, ZEC), WAITING=0, REVIEW/SHADOW=133, ENTERED_UNRESOLVED_EXPIRED=15, NO_ENTRY_EXPIRED=45, CLOSED=379W/52L/0flat, NEEDS_REVIEW=0",
        "0 untracked legacy alerts",
        "track-signals pass: checked=536, updated=0, tp_hits=378 (cumulative), stopped=0, expired=0 this cycle - no state changes since last review"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.8,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "UNH: DOJ criminal AND civil investigation into Medicare Advantage billing (alleged inflated diagnoses), extending to Optum Rx/physician reimbursement, company confirmed via SEC filing, stock down >45% YTD, CEO departed May, earnings guidance suspended (external, multi-source: Yahoo Finance, The Hill, TipRanks, FierceHealthcare)",
        "UNH appears repeatedly across internal C-tier book (intraday/swing/invest), always long direction - must be treated as AVOID regardless of tier/score",
        "SMCI: prior-review legal-risk carry-forward, no fresh matching news_items in last 72h this cycle - softer caution, not fresh evidence"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto scalp mode PF 0.474/avgR -0.1175 (n=159) - net negative, correctly policy-disabled (config/crypto_quality_overlay.yaml disabled:true confirmed this cycle)",
        "Crypto intraday PF 1.668/avgR +0.194 (n=162) and swing PF 1.852/avgR +0.304 (n=106) - both working",
        "Stocks intraday PF 0.813/avgR -0.047 (n=177) - net negative; tier=C triggered winrate 6-7% (n=180) confirms never-actionable status; tier=B n=14 (weak) winrate 0% PF 0.00 - small sample, needs watching",
        "tier=A crypto n=4 - too small a sample for confidence"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": null,
      "confidence": 0.72,
      "reason_codes": ["risk_off", "chop", "wait_for_trigger", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Synthesis of all 8 agents above - see §6/§7/§8/§9 for full routing and candidates",
        "No new actionable signals this cycle; existing 3 open crypto positions being monitored, not chased",
        "UNH is the clearest hard-avoid; ZEC is the clearest catalyst-backed hold; SPELL is the clearest RS-leader (already open); HMSTR is the clearest short-watch (not yet actionable)"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.72,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "SPELL/USDT", "trigger": "already OPEN (intraday B); a *fresh* add/long only on a pullback into the entry zone with RS still intact - do not chase the current extension", "reason": "RS leader vs BTC/ETH (score 92, +18.7% 24h), fresh OI +90.7% confirms trend, but funding/crowding signal it's already stretched" },
    "best_short_candidate":    { "symbol": "HMSTR/USDT", "trigger": "wait for pullback toward EMA20 + confirmed bearish HTF structure + derivatives confirmation + stop above swing high (squeeze risk flagged - do not chase the -38.9% extension)", "reason": "weakest symbol this cycle, price down + OI up = fresh shorts pressing, but system explicitly rejected immediate entry as >2 ATR from EMA20" },
    "best_catalyst_candidate": { "symbol": "ZEC/USDT", "trigger": "already OPEN (intraday B); catalyst intact - Ironwood/Tachyon proof-of-no-counterfeit-bugs reconfirmed externally, whale flow now long-biased", "reason": "clearest verified fundamental catalyst in the current active book, internal whale-short contradiction appears stale/superseded" },
    "avoid_candidate":         { "symbol": "UNH", "reason": "DOJ criminal+civil Medicare Advantage fraud probe, stock -45% YTD, CEO departure, suspended guidance - appears repeatedly long in the C-tier book; avoid regardless of tier/score, manual review only" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale (swing) | advisory_only |
| market_regime | caution | 0.72 | risk_off, chop, wait_for_trigger, mixed | advisory_only |
| catalyst_narrative | caution | 0.60 | fresh_catalyst, catalyst_confirmed, mapping_weak, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, oi_supports, funding_extreme, data_unavailable | advisory_only |
| technical_entry | caution | 0.65 | entry_late, chase_risk, overextended, stale_before_entry | advisory_only |
| execution_lifecycle | ok | 0.85 | open_actionable, review_shadow, entered_unresolved, no_entry | advisory_only |
| risk_manager | caution | 0.80 | legal_risk, headline_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution (synthesis) | 0.72 | risk_off, chop, wait_for_trigger, manual_review | advisory_only |

---

## 4. What Changed vs Previous Review (04:47 EEST, crypto overnight/Asia)

- **Regime flip**: BTC/ETH uptrend → range/chop. Altcoin breadth above EMA20 55.81%→38.64-43.18%, above EMA50 67.44%→52.27%. Macro risk score 63→97/100 on the same escalating Iran/Hormuz story (fresh missile strikes on ships ~19h old per external check).
- **Open positions unchanged**: SPELL/USDT, BANANA/USDT, ZEC/USDT remain OPEN (long, intraday B) — no new triggers this cycle, no closes either.
- **ZEC catalyst strengthened, not weakened**: prior review flagged ZEC as "best-verified catalyst"; this run's external check reconfirms the Ironwood/Tachyon bug-proof story and finds whale flow is now long-biased, which supersedes the earlier internal "$14.9M whale short" headline (still present in `news_items` but appears stale).
- **UNH risk deepened materially**: prior review carried UNH forward as a "hard legal-risk avoid" from a single-headline read; this run's external verification found the DOJ probe is both criminal *and* civil, extends to Optum Rx, and the stock is down >45% YTD with a CEO departure and suspended guidance — the risk is confirmed and larger than the internal single-source headline suggested.
- **Crypto swing report staleness worsened**: ~23h44m at 04:40 → ~33h37m now, 5th+ consecutive review flagging this with no refresh.
- **Untracked legacy alerts**: still 0, stable.
- **Catalyst mapping**: still weak (17.8% mapped at 04:40 → 20.8% mapped now — marginal improvement, still well under the 50% threshold).
- **Notifier bug**: prior review found a Telegram HTTP-400 on the literal filename `OPUS_ENRICHED_REVIEW_LATEST.md` (unbalanced-underscore Markdown parsing); this run uses the same backtick workaround, carried-forward TODO not yet fixed at the code level.

---

## 5. Catalyst Coverage

- Total `catalyst_events` today: **1401**
- Mapped (symbol present): **292 (20.8%)**
- Unmapped: **1109 (79.2%)**
- `narrative_baskets`: **3** — `delisting_thin_liquidity` (avoid_low_liquidity, no primary), `perps_dex_narrative` (primary HYPE/USDT; related DYDX/GMX/ASTER; wait_pullback), `ai_narrative` (primary NEAR/RENDER/TAO/FET; related WLD/ASTER; related_beta_rotation)

**⚠ catalyst mapping weak this run — use catalyst layer as context, not final decision.** (79.2% unmapped, above the 50% threshold.)

Top 3 unmapped headlines this cycle:
1. "Switzerland advances to World Cup quarterfinals after penalty win over Colombia" — no symbol
2. "Russia advances crypto regulation bill, allowing foreign trade use" — sector-level, no symbol
3. "GeneDx Holdings (WGS) Hit with Securities Class Action Following 49% Stock Collapse -- HBSS" — symbol present in text but not resolved by mapper

---

## 6. Market Landscape

Crypto: BTC/ETH both range-bound after an overnight/morning cool-off from uptrend. Altcoin breadth is weak-to-mixed (38.6-43.2% above EMA20). Macro backdrop is risk-off (score 97/100) on the Iran/Strait-of-Hormuz oil-supply story — externally confirmed as an active, escalating (but not yet market-breaking) tail risk; Brent +1.64%, BTC's reaction described externally as muted. No fresh crypto A-tier or new B-tier this cycle. Strongest RS names (SPELL, HMSTR, JTO, SENT, EPIC, TLM, OPG) are a mix of genuine RS-leaders (SPELL) and heavily-shorted, overextended breakdown candidates (HMSTR, EPIC, TLM, OPG) — the system's own entry-quality gate is rejecting immediate chases on all of the latter.

Stocks: pre-market / closed (~04:40 ET). All active stocks signals are C-tier (never actionable per the position-framework hardening). UNH carries a serious, externally-confirmed legal/headline risk that overrides any technical read. Top internal catalyst list is dominated by law-firm "investors have opportunity to lead" securities-class-action solicitations (GRAL, BTU, ERAS, GNS, PLAB, WGS, BMI, GEHC, PODD) — low individual signal quality, treated as noise unless a name also shows technical/price confirmation.

### Market Mood / Risk Routing

- Crypto mood: **chop / risk-off headwind** (regime range/range, macro 97/100, breadth <50% on EMA20)
- Stocks mood: **pre-market / closed** (US cash open still ~5h away)
- Dominant narrative: **AI sector rotation (NEAR/RENDER/TAO/FET)** and **perps/DEX (HYPE)**, plus a live geopolitical/oil tail-risk (Iran/Hormuz) not captured by symbol-level catalysts
- Preferred side now: **wait-for-trigger**; crypto longs only on confirmed RS-leaders with pullback structure, shorts only after failed-bounce confirmation (no chasing extended moves either direction)
- Best long candidate: **SPELL/USDT** (already open; monitor, do not chase the extension)
- Best short candidate: **HMSTR/USDT** (watch only — wait for pullback/failed-bounce confirmation; currently too extended to chase, squeeze risk noted)
- Best catalyst-backed candidate: **ZEC/USDT** (already open; Ironwood/Tachyon catalyst reconfirmed externally)
- What to avoid: **UNH** (DOJ criminal+civil fraud probe, confirmed and worse than initially flagged); low-liquidity/delisting-basket names generally
- What would change the view: BTC/ETH reclaiming their prior uptrend structure with breadth back above 50-55% on EMA20; a de-escalation or further escalation headline out of the Strait of Hormuz; any of SPELL/BANANA/ZEC hitting TP or SL (frees up attention for a fresh entry read); US cash-open reaction for stocks

---

## 7. Candidate Deep Dives

### SPELL/USDT (crypto, intraday B, long, OPEN)
- Score 92 (momentum/RS composite), +18.7% 24h, RS vs BTC/ETH leader, volume 0.5x (not confirmed by volume).
- Derivatives: funding -0.0157 (mexc), OI 24h +90.7%, long/short 1.65, crowding elevated/unknown — fresh, aggressive long positioning; confirms trend but is stretched.
- Has price already reacted? Yes, strongly (+18.7% 24h) — already priced in.
- Chasing? Yes if entering fresh now; the existing position was entered on this leg and the system's own note flags "chase risk."
- Retest/pullback structure? Not yet visible in the report; entry plan calls for pullback into a zone before adding.
- Overextended? Likely (>2 ATR is the standing house rule for HMSTR-style names; SPELL's funding/OI profile suggests similar stretch even without a printed ATR distance).
- Actionable now? Position is already open and being monitored for TP/SL — no fresh entry decision required. A *new* add is not actionable without a pullback.
- Aligned with market mood? Partially — it's a genuine RS-leader in an otherwise chop/risk-off tape, which is exactly the kind of idea PART 2 favors even in mixed conditions.
- Invalidation: loss of RS leadership vs BTC/ETH, or a reversal back through the entry/invalidation band already tracked by the live signal.
- No catalyst found in `news_items` (checked, 24h window) — this is a pure technical/derivatives momentum name, not catalyst-backed.

### ZEC/USDT (crypto, intraday B, long, OPEN)
- Score 74, +6.7% 24h, RS leader vs BTC/ETH.
- Internal catalyst: "ZEC jumps 12% as Zcash nears mathematical proof against hidden counterfeit bugs" (The Block, 2026-07-07 18:12) — Orchard/Ironwood shielded-pool verification effort ("Project Tachyon").
- Internal contradiction flagged: a same-day AMBCrypto piece cited a whale expanding a $14.9M short bet targeting $410.
- **External verification (WebSearch, this run)**: ZEC trading ~$483.72 (+8% 24h, +23% 7d), reclaimed $500 briefly, and current whale activity is described as **long-biased net accumulation** with a long-skewed long/short ratio — this is more recent than the AMBCrypto short-bet story and appears to supersede it. Treat the whale-short headline as stale, not a live contradiction.
- Has price reacted? Yes, partially — the catalyst is >24h old now and priced in to a degree, but momentum/whale flow both still point the same direction externally.
- Chasing? Position already open; no fresh chase decision needed.
- Actionable now? Already OPEN, monitor for TP/SL. Catalyst intact and reconfirmed.
- Invalidation: a genuine fresh whale-short buildup (not the stale one) or Ironwood/Tachyon verification setback.

### BANANA/USDT (crypto, intraday B, long, OPEN)
- Live signal: tier B, score 71.8, triggered 2026-07-07 16:36, expires 2026-07-08 23:49.
- No matching `news_items` catalyst found in the last 24h despite an internal shadow-lane table tagging it "catalyst_backed" at a lower confidence (score 58, shadow/C-tier in that separate evaluation) — the catalyst behind this idea, if any, is not corroborated in the live news feed this cycle. Treat as technical/momentum, not catalyst-confirmed.
- Actionable now? Already OPEN, monitor for TP/SL only.

### HMSTR/USDT (crypto, watch only, short candidate — NOT open, NOT actionable now)
- Score 85.1 raw momentum, but entry-quality penalty drops it to 35.5 for a short: "Price is more than 2 ATR from EMA20; do not chase." System converted this to watchlist-only, wait for pullback.
- 24h -38.9%, RS vs BTC -37.9%, volume 1.71x (real volume confirmation), tags: weak_vs_market, volume_expansion, breakdown, overextended.
- Derivatives: price down + OI up = fresh shorts pressing — squeeze risk flagged if price reclaims; funding neutral across venues (bybit/mexc/okx all ~5e-5), crowding "normal"/"low" (not yet crowded).
- Is this a chase-risk setup? Yes, right now — explicitly rejected by the system's own gate.
- What would make it actionable: a pullback/failed-bounce toward EMA20 with confirmed bearish HTF structure, derivatives data still supporting (no fresh squeeze buildup), and a stop placed above the swing high.
- Invalidation: a reclaim of the recent breakdown structure (which would itself be the squeeze scenario flagged above).

### UNH (stocks, C-tier, long, multiple entries in book — AVOID / LEGAL RISK)
- Internal: 0.73-importance legal_risk catalyst — "UnitedHealth (UNH) Faces DOJ Probe, Shares Dive 16% on Fraud Investigation" (QuiverQuant/Globe and Mail, Yahoo Finance, Healthcare Dive — 3 independent sources, 2026-07-06/07, "UnitedHealth confirms it's under investigation by DOJ").
- **External verification (WebSearch, this run)**: confirms and substantially deepens the picture — the DOJ investigation is **both criminal and civil**, targets Medicare Advantage billing (alleged inflated diagnoses without physician confirmation), extends to **Optum Rx** and physician-reimbursement practices, the company confirmed cooperation via SEC filing, the stock is down **>45% YTD**, the CEO departed in May, and 2025 earnings guidance was suspended.
- UNH appears repeatedly in the current active book — always **long** direction, always C-tier (intraday/swing/invest) — meaning the technical/scoring layer has no visibility into this legal risk.
- Legal/headline risk confirmed per §I discipline (multi-source, dated, primary company confirmation). Final verdict: **AVOID / MANUAL REVIEW REQUIRED** for any UNH long — this is not a clean actionable regardless of score, and C-tier means it isn't actionable anyway, but this should also gate any future tier upgrade for UNH until the investigation outcome is clearer.
- SMCI: carried-forward legal-risk designation from prior reviews; no fresh matching `news_items` in the last 72h this cycle — kept as a softer caution pending fresh evidence, not re-verified this run.

---

## 8. Best Candidates Ranked

1. **ZEC/USDT** — best catalyst-backed idea; already open, catalyst reconfirmed and strengthened externally, whale flow now long-biased. Action: hold/monitor, no fresh entry needed.
2. **SPELL/USDT** — best RS-leader long; already open, technical/derivatives momentum intact but stretched. Action: hold/monitor; a fresh add only on a clean pullback, not the current extension.
3. **BANANA/USDT** — open, technical momentum, catalyst unconfirmed in live feed. Action: hold/monitor for TP/SL.
4. **HMSTR/USDT** — best short-watch; not yet actionable, needs a pullback/failed-bounce confirmation. Exact trigger: reclaim/retrace toward EMA20 + bearish HTF structure + derivatives still supportive + stop above swing high.
5. No clean new long or short entry exists this window beyond the above. Best long-watch beyond the open book: none scoring above the entry-quality bar today (BANANA/ALLO/CHIP catalyst-backed ideas remain shadow/C-tier, below promotion threshold).

---

## 9. Avoid / No Trade

*(This decision window only — scanning, tracking, and monitoring continue regardless.)*

- **UNH** (stocks) — hard avoid, DOJ criminal+civil fraud probe, confirmed severity exceeds the internal single-headline read. Any existing/future UNH long idea needs manual legal-risk review before promotion, independent of score.
- **SMCI** (stocks) — softer carry-forward caution, no fresh evidence this cycle; do not treat as cleared, but do not escalate without a fresh headline either.
- **HYPE/USDT** (crypto) — carries an operator-review flag this cycle for an unrelated phishing/scam-drain headline ("Fake HyperSwap Airdrop Drained $12,300"); not a protocol hack, but avoid chasing HYPE-basket names (DYDX/GMX/ASTER) without manual confirmation this cycle.
- **Delisting/thin-liquidity basket names** — no primary symbol identified, avoid_low_liquidity playbook stands; avoid chasing any low-float dump/pump in this bucket.
- **HMSTR/USDT and similar >2-ATR-extended breakdown names (EPIC, TLM, OPG)** — not a "no trade forever," just not actionable *now*; see §8 for the exact trigger that would flip this to a watch-to-active short.

---

## 10. Main Risks

- Macro/geopolitical tail risk (Iran/Strait of Hormuz) is live and escalating; BTC has absorbed it so far but a further escalation (e.g. an actual Hormuz closure attempt) could shift crypto risk sentiment quickly.
- UNH-style legal/headline risk is invisible to the technical scoring layer — the C-tier gate protects against acting on it today, but any future tier upgrade needs a manual legal check first.
- Crypto swing report is now >33h stale with no refresh in 5+ consecutive review cycles — a real blind spot for swing-mode decisions today.
- Catalyst mapping remains weak (79.2% unmapped) — do not over-trust "no catalyst found" reads; absence of a mapped catalyst is a data gap, not proof of absence.
- Stocks tier=B sample is tiny (n=14) with 0% win rate and PF 0.00 — too small to act on, but worth monitoring for a real pattern.

---

## 11. Action Plan — next 4 hours

- Continue monitoring the 3 open crypto positions (SPELL, BANANA, ZEC) for TP/SL; no manual intervention needed.
- Watch HMSTR/USDT for a pullback/failed-bounce setup into the pre-US-open window; do not chase the current extension.
- Watch for US pre-market stocks data as the 16:20 pre-US-open review approaches; re-run legal/headline checks on any stocks A/B/C candidate that surfaces fresh pre-market volume, especially anything adjacent to UNH's Medicare-billing/DOJ-probe theme (peer names in managed care).
- Re-check the Iran/Hormuz macro story before the 16:20 and 18:30 slots — this is the single most likely source of a regime change today.
- No scoring, threshold, or code changes — advisory only.

---

## 12. Final Verdict per Mode

- **Crypto scalp**: correctly disabled by policy (net-negative, PF 0.47). No change recommended.
- **Crypto intraday**: working (PF 1.67); 3 positions open and healthy, no new entries this cycle; stay selective, avoid chasing extended names.
- **Crypto swing**: data STALE (>33h) — treat any swing-mode read today as carried-forward context only, not a fresh decision input.
- **Stocks intraday/swing/invest**: pre-market/closed; C-tier only, never actionable; UNH flagged AVOID regardless of future tier upgrades pending legal-risk clearance.

---

## 13. Sources

- [UnitedHealth (UNH) Faces DOJ Probe, Shares Dive 16% on Fraud Investigation — The Globe and Mail](https://www.theglobeandmail.com/investing/markets/stocks/UNH-N/pressreleases/32431512/unitedhealth-unh-faces-doj-probe-shares-dive-16-on-fraud-investigation/) (2026-07-07, internal)
- [UnitedHealth stock sinks 4.7% after company confirms DOJ investigation into Medicare billing practices — Yahoo Finance](https://finance.yahoo.com/news/unitedhealth-stock-sinks-47-after-company-confirms-doj-investigation-into-medicare-billing-practices-133527260.html)
- [UnitedHealth acknowledges DOJ investigation into Medicare billing — The Hill](https://thehill.com/policy/healthcare/5418393-unitedhealth-doj-investigation-medicare-billing/)
- [UnitedHealth Stock (UNH) Sinks as DOJ Criminal Probe into Medicare Fraud Deepens — TipRanks](https://www.tipranks.com/news/unitedhealth-stock-unh-sinks-as-doj-criminal-probe-into-medicare-fraud-deepens)
- [DOJ's criminal probe into UnitedHealth extends to Optum Rx, physician reimbursement — FierceHealthcare](https://www.fiercehealthcare.com/payers/wsj-report-doj-interviewing-former-employees-about-medicare-billing-practices-unitedhealth)
- [ZEC jumps 12% as Zcash nears mathematical proof against hidden counterfeit bugs — The Block] (internal `news_items`, 2026-07-07)
- [Zcash Price, Chart, Market Cap — CoinLore](https://www.coinlore.com/coin/zcash)
- [Zcash (ZEC) Price Explodes 10% as Social Activity Spikes — Coinpedia](https://coinpedia.org/price-analysis/zcash-zec-price-explodes-10-as-social-activity-spikes-will-the-rally-continue/)
- [Iran Reportedly Hits Ships in Strait of Hormuz: Oil Price Jumps Again — BeInCrypto](https://beincrypto.com/oil-prices-iran-strait-hormuz-attack/)
- [Live updates: Bitcoin traders don't expect BTC to cross $75,000 as U.S.-Iran threats remain — CoinDesk](https://www.coindesk.com/tech/2026/06/15/live-markets-bitcoin-not-fully-out-of-danger-as-trump-warns-of-further-iran-strikes)
- [2026 Iran conflict: Impact on oil, gold, bitcoin, and forex markets — OANDA](https://www.oanda.com/us-en/skills-and-insights/education/market-commentary/market-moves/2026-iran-conflict-oil-gold-bitcoin-forex-impact/)

---

## 14. Fix Requests / TODO

### TODO-day-rollover-scheduler-folder
- **issue:** Live scheduler.log / cycle summaries for "today" (2026-07-08) continue to be written under the `2026-07-07_default_schedule/` folder rather than a `2026-07-08_default_schedule/` folder; the actual `2026-07-08_default_schedule/` folder only contains a stale dry-run log. Freshness checks had to fall back to mtime-scanning across folders rather than trusting the newest-named folder.
- **evidence:** `data/scheduled_runs/2026-07-08_default_schedule/scheduler.log` last entry is a `=== DRY RUN ===` block at 02:05:58 EEST; the real cycle_09 activity (finished 10:11:29 EEST) is filed under `data/scheduled_runs/2026-07-07_default_schedule/cycle_09_09-47_summary.md`.
- **suggested manual fix:** Align the scheduler's day-folder rollover boundary with the actual cycle start time, or stop creating a same-day dry-run folder that shadows the real one.
- **priority:** low (cosmetic/organizational, not blocking; this is the 2nd+ review to note it)
- **first observed:** 2026-07-08 04:47 EEST (prior review); still present 2026-07-08 11:40 EEST

### TODO-crypto-swing-report-stale
- **issue:** Crypto swing report has not refreshed in >33 hours (last gen ~2026-07-07 05:03 EEST), despite the scheduler otherwise running on schedule. 5th+ consecutive review flagging this.
- **evidence:** `data/reports/swing/2026-07-07_02-03_swing_report.md` is the newest file in `data/reports/swing/`; cycle summaries show swing-mode steps are not part of every 2h05m cycle (only "Daily long-horizon swing/invest included: False" on most cycles per `cycle_09_09-47_summary.md`).
- **suggested manual fix:** Confirm the intended cadence for crypto swing-report regeneration (daily vs every cycle) and verify it is actually firing; if daily-only by design, note that explicitly in the scheduler docs so future reviews stop mis-flagging it as broken.
- **priority:** medium (recurring, worsening, but the swing DB signals themselves are still tracked live)
- **first observed:** prior reviews (4th+ before this one); still present 2026-07-08 11:40 EEST

### TODO-catalyst-mapping-still-weak
- **issue:** Catalyst symbol-mapping coverage remains well under the 50% target (20.8% mapped this cycle, up marginally from 17.8% at the last review) — the catalyst layer is still mostly unusable as a primary decision input.
- **evidence:** `data/catalysts/2026-07-08/catalyst_events.jsonl`: 1401 total, 292 mapped, 1109 unmapped this cycle.
- **suggested manual fix:** Improve the symbol resolver in the catalyst layer (ticker/company-name matching against a broader universe, handle stock-tickers-in-title cases like the GeneDx/WGS example in §5).
- **priority:** medium (recurring across many reviews)
- **first observed:** prior reviews; still present 2026-07-08 11:40 EEST

### TODO-notifier-underscore-workaround-not-yet-fixed
- **issue:** The Telegram notifier's default `parse_mode="Markdown"` rejects (HTTP 400) any message containing the literal filename `OPUS_ENRICHED_REVIEW_LATEST.md` because the underscores are parsed as unbalanced italics markers. A backtick-wrapping workaround was applied manually in the 04:40 review and again this run, but the underlying code has not been fixed.
- **evidence:** Observed HTTP 400 in the 04:47 EEST review run when sending the plain filename; backtick-wrapping (`` `OPUS_ENRICHED_REVIEW_LATEST.md` ``) resolved it both times.
- **suggested manual fix:** Escape underscores (or switch to `parse_mode="MarkdownV2"` with proper escaping, or `parse_mode=None`) in the notifier's message-building code path used by this routine.
- **priority:** low (workaround is reliable, but this is now the 2nd occurrence)
- **first observed:** 2026-07-08 04:47 EEST; still unresolved 2026-07-08 11:40 EEST
