# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:31 EEST

## 1. Executive Summary

Slot: **pre-US-open decision review** (Monday 2026-07-27, nominal 16:20 EEST, run at 16:31 EEST — ~10 minutes before the 09:30 ET / 16:30 EEST US cash open). **Advisory only — no auto-trade.** The single most important finding this cycle: the internal stocks-intraday report (generated 16:19 EEST, 5 minutes ago — the freshest data available) still labels the regime **risk_off / short bias** (VIX 17.71, 0/4 indices trending up, breadth 0%), but externally-verified pre-market futures show the opposite — **Dow +1.14%, S&P 500 +0.84%, Nasdaq +1.28%**, on the US-Iran ceasefire holding and Brent crude down >7%, with an 88% "up-open" prediction-market read. This is a genuine internal/external contradiction: the desk's short-tier stocks book (SMH, AVGO, XLK, META, QQQ, MSTR, AMD, COIN, AMZN, TSLA, DIA, SPY, MSFT — all C-tier, market-closed-demoted) faces real **gap risk** at the open and must not be shorted blind into a confirmed pre-market gap-up; require RTH confirmation that the gap fades/rejects before treating any of these as a clean short. Crypto remains the only live-actionable class pre-open and stays risk-on (BTC/ETH uptrend, altcoin breadth 64-72% above EMA20), reinforced by fresh institutional-flow news (Bitmine +9,946 ETH this week, ETH testing $2,000). No A-tier setups anywhere (crypto or stocks). Per the authoritative `PAPER_MONITOR_STATUS_LATEST.md` (13:22 EEST): **4 OPEN_ACTIVE** (AERO/USDT-intraday, LA/USDT-intraday, LA/USDT-swing, ZEC/USDT-swing, all long), **2 WAITING_FOR_ENTRY** (NIL/USDT-intraday, AKE/USDT-intraday), 1 UNKNOWN_INCONSISTENT (XOM, carried cosmetic issue). DIA/USDT continues its multi-cycle chase-risk pattern — registered as a waiting/watch idea across scalp, intraday, and swing all day, and confirmed NO_ENTRY (price ran away before fill) in every mode per the lifecycle log; still the highest-scored fresh idea this cycle (66.1, intraday) so it stays the long-watch pick, but with an explicit "has failed to fill repeatedly" caveat. `detect_untracked_legacy_alerts` shows **2 untracked crypto alerts** this cycle (ZAMA/USDT and DIA/USDT intraday, sent 12:44 EEST without a matching `proposed_signal`) — a recurrence of the previously-flagged high-priority TODO (see §14). Catalyst mapping continues to degrade: **67.9% unmapped** this cycle, the 5th consecutive worsening data point. No code touched; TODOs carried and updated.

## 2. Data Used

- Reports: `data/reports/scalp/2026-07-27_12-32_scalp_report.md` (mtime 15:32 EEST, ~1h old, data-as-of 12:30 UTC — fresh), `data/reports/intraday/2026-07-27_12-44_intraday_report.md` (mtime 15:44 EEST, ~47min old, data-as-of 12:30 UTC — fresh), `data/reports/swing/2026-07-27_01-58_swing_report.md` (mtime 04:58 EEST, ~11h33m old, data-as-of 01:45 UTC — **carry-forward**, inside the 4-12h band, near its upper edge; used with reduced weight for anything not corroborated by fresher intraday/scalp data).
- Stocks: `data/reports/stocks/intraday/2026-07-27_13-19_stocks_intraday_report.md` (mtime 16:19 EEST, **~12 minutes old — the freshest report of this entire cycle**, ideal timing for the pre-open slot). Stocks swing/invest reports remain from 2026-07-02 (25 days stale) — deprecated framework per prior audits ([[project_crypto_ai_desk_stocks_position_framework]]), not a fresh gap.
- Catalysts: `data/catalysts/2026-07-27/catalyst_events.jsonl` computed directly this cycle — **2,500 cumulative rows, 803 mapped / 1,697 unmapped = 67.9% unmapped**; `narrative_baskets.jsonl` (6 baskets: delisting_thin_liquidity, binance_ecosystem_teaser, ai_narrative, perps_dex_narrative, rwa_narrative, momentum_breakout); `catalyst_cycle_12-51.md` (freshest, generated 15:51 EEST).
- CLI: `active-signals` (crypto ×23, stocks ×50), `signal-stats` (crypto: weekly A/B sample=171, PF 1.81, +34.0R; stocks: weekly A/B sample=0, C-tier only n=203, PF 0.56, -3.5R), `detect_untracked_legacy_alerts --since 2026-07-27` (**2 untracked crypto alerts**: ZAMA/USDT, DIA/USDT — both intraday, sent 12:44 EEST).
- Direct `db/crypto_ai_desk.sqlite` query: `news_items.detected_symbols_json` 24h-freshness check for LA, DIA, AERO, ZEC, NIL, AKE — zero genuine hits for LA/DIA/AERO/NIL/AKE; **ZEC/USDT returns one genuine <24h hit** (Zcash Ironwood upgrade, t.me/wublockchainenglish, 11:10 EEST) not present in the structured catalyst layer for this symbol. BTC/ETH last-6h query: 5 hits each, both consistent with the internal bullish-trend/risk-on regime (Bitmine +9,946 ETH; Strategy holding steady at 843,775 BTC, $3.75B cash reserve).
- `reports/PAPER_MONITOR_STATUS_LATEST.md` (mtime 13:22 EEST, ~3h09m old — authoritative for §3A execution_lifecycle and the Telegram Status block; no fresher snapshot exists this cycle).
- External web research: 2 WebSearch + 1 WebFetch this cycle (US pre-market futures levels/drivers; S&P "up-open" sentiment) — see §13, all loaded successfully.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-27_1139.md` (Europe / pre-US context, 11:39 EEST, same day).

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime 2026-07-27 16:20:16 EEST (~11min old at run time); latest cycle folder `cycle_08_12-36_summary.md` (mtime ~13:24 EEST, ~3h07m old). Both well under the 3h joint-defer threshold (only cycle-summary mtime is aging; scheduler.log itself is essentially live). **Not deferred.**
- Scalp/intraday reports regenerated this cycle (15:32-15:44 EEST) — fresh, ~1h old.
- Swing report unchanged since 04:58 EEST (~11h33m old) — inside the 4-12h carry-forward band but near its upper edge; the desk's swing B-tier book (LA/ESP/DIA/KAITO/ZEC/ORDI/TAO) still originates from this carried report. Flagged, used with reduced weight for anything not corroborated by fresher intraday/scalp data.
- Stocks intraday report is the freshest data point of the entire cycle (16:19 EEST, ~12min old) — ideal timing, captures the pre-open picture directly.
- Catalyst folder fresh (cycle regenerated 15:51 EEST, ~40min old).
- `detect_untracked_legacy_alerts`: **2 untracked crypto alerts** (ZAMA/USDT, DIA/USDT) — not clean this cycle.
- Paper-monitor lifecycle snapshot is ~3h09m old (13:22 EEST) — the freshest available; no newer snapshot exists. Treated as authoritative per routine but flagged as the least-fresh of the core inputs this cycle.
- News infra: only the standing Reddit 403 social-source failures (documented blindspot, unchanged for weeks) — no new ingest-pipeline concerns.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-27 16:31 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["fresher swing report than 11h33m carry-forward", "fresher paper-monitor snapshot than 3h09m"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log ~11min old, well under 3h defer threshold", "scalp/intraday reports regenerated 15:32-15:44 EEST, fresh", "stocks intraday report generated 16:19 EEST — freshest input this cycle, ideal pre-open timing", "swing report unchanged since 04:58 EEST (~11h33m, near the upper edge of the 4-12h carry-forward band)", "paper-monitor lifecycle snapshot 13:22 EEST (~3h09m old) — no fresher snapshot exists, flagged as the least-fresh core input"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["risk_on", "mixed", "longs_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto: BTC uptrend, ETH uptrend, altcoin breadth 64.1%/71.8% above EMA20 across intraday/swing — internal regime label bullish trend (risk-on), unchanged and reinforced by fresh institutional-flow news (Bitmine +9,946 ETH this week; ETH testing $2,000)", "Stocks (internal, 16:19 EEST): risk_off/short bias, VIX 17.71, 0/4 indices trending up, breadth 0% above EMA20/EMA50", "Stocks (external, WebFetch-verified): pre-market futures show Dow +1.14% (+595pt/52,719), S&P 500 +0.84% (+62.25/7,509.75), Nasdaq +1.28% (+362/28,644.25) — driven by Brent crude down >7% and the US-Iran ceasefire holding; 88% 'up-open' prediction-market read (Benzinga, single_source)", "This is a genuine internal/external contradiction: the internal stocks regime label has not caught up to the real-time pre-market gap-up — treat the risk_off/short-bias label as stale-lagging, not as a live signal to short blind at the open", "AAPL premarket +3.53% (external) despite being internally rejected as 'long_in_risk_off_regime' — a note-only observation, not a registered internal setup, so not independently actionable"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "fresh_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["2,500 cumulative catalyst events today, 1,697 unmapped (67.9%) — the 5th consecutive worsening data point (60.1%->60.9%->64.6%->65.3%->67.9%)", "Direct news_items 24h-freshness check: LA/DIA/AERO/NIL/AKE all show zero genuine hits — consistent with each report's own 'no fresh verified catalyst detected' language", "ZEC/USDT (OPEN_ACTIVE swing) has a genuine fresh catalyst — Zcash Ironwood upgrade (shielded pool, supply safeguards), t.me/wublockchainenglish, 11:10 EEST, single_source — not present in the structured catalyst_events.jsonl for this symbol, a missed-mapping example (same defect family as prior LA/USDT and EUL/USDT misses)", "momentum_breakout basket (NIL/PUMP/ZAMA, fresh <1h, no confirmed news) and binance_ecosystem_teaser (BNB primary, fresh <1h) both remain pure-momentum/basket-level with no concrete registered entry", "perps_dex_narrative (HYPE/USDT primary) still has no concrete registered signal, unchanged across multiple cycles today"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["oi_supports", "squeeze_risk", "data_unavailable"],
      "data_missing": ["OI history for several MEXC-only names"],
      "suggested_effect": "advisory_only",
      "facts_used": ["DIA/USDT: fresh OI build with price across scalp/swing (rejected/no-derivatives-confirmation on scalp, +101.45% on swing) — fresh positioning confirms trend on the desk's highest-scored idea, but repeated NO_ENTRY across all three modes means the positioning has not translated into a fill", "NIL/USDT: negative funding across bybit/mexc (-0.0051/-0.0047), crowding elevated per intraday cross-check — shorts paying longs after a strong run, a squeeze-fuel signal but also a late-stage/crowded-move caution for a fresh long entry", "AKE/USDT: OI down -40% on scalp fallback view despite price up — short-covering pattern, weaker continuation quality than the headline momentum score (91.6) implies", "SYN/RE/RIF/ALLO/EUL all capped to C for thin_liquidity_short_squeeze_risk — still no clean crypto short on the board, consistent all day"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chase_risk", "entry_late", "price_moved_away", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["DIA/USDT: registered pullback zone this cycle (intraday) 0.1610-0.1676, current price 0.1705 — just above the zone, not yet a clean fill; lifecycle log shows repeated NO_ENTRY across scalp/intraday/swing today ('price ran away from the entry zone before a fill') — a persistent, confirmed chase-risk pattern for this specific symbol, not a one-off", "AERO/USDT (OPEN_ACTIVE intraday): filled cleanly inside its registered zone earlier; current position is manage-only, not a fresh-entry decision", "LA/USDT (OPEN_ACTIVE both intraday and swing): both filled inside their respective registered zones; manage-only, do not add at current extension", "ZEC/USDT (OPEN_ACTIVE swing): filled inside registered zone 498.83-501.18; current desk notes show price near 502, a clean fill supported by the fresh Ironwood catalyst found externally", "KAITO/USDT: still shows in active-signals (B, swing, weekend flag) with no volume confirmation across today's reports (0.55x on scalp) — same unresolved chase-risk read as prior cycles"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Paper-monitor lifecycle (13:22 EEST, authoritative, no fresher snapshot): OPEN_ACTIVE=4 (AERO-intraday, LA-intraday, LA-swing, ZEC-swing, all long), WAITING_FOR_ENTRY=2 (NIL-intraday, AKE-intraday), REVIEW_ONLY_SHADOW=34, ENTERED_UNRESOLVED_EXPIRED=0, NO_ENTRY_EXPIRED=57, CLOSED_WIN=152/CLOSED_LOSS=9/CLOSED_FLAT=31, UNKNOWN_INCONSISTENT=1 (XOM, carried cosmetic issue, unmapped status field 'tp2_hit')", "ZAMA/USDT closed WIN +1.0R (legacy touch) since the 11:39 review — no longer an open position, consistent with the lifecycle log", "detect_untracked_legacy_alerts: 2 untracked crypto alerts this cycle — ZAMA/USDT and DIA/USDT (both intraday, sent 12:44 EEST) — these were pushed to Telegram but carry no matching proposed_signal, so they will not contribute to PF/winrate/avgR tracking; a recurrence of the previously-flagged high-priority watchlist-alert/signal-reuse defect"] },
    { "agent": "risk_manager", "verdict": "manual_review", "confidence": 0.6,
      "reason_codes": ["headline_risk", "correlation_cluster", "legal_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Gap risk at the US open: internal stocks regime (risk_off/short) is contradicted by externally-verified pre-market futures (Dow/S&P/Nasdaq all +0.8-1.3%) — any short entered pre-open or in the first minutes of RTH risks being caught by the gap; require confirmation the gap fades before acting on the short book", "UNH carries an active DOJ/Medicare-fraud legal-risk flag plus earnings tomorrow (2026-07-28), block_requires_operator_review, do_not_chase_warning — correctly excluded regardless of score or the futures-driven gap-up", "TSLA (going-concern) and MSFT (class-action/securities-fraud) carry the same standing flags, unchanged", "correlated risk: 4 open crypto long positions (AERO, LA x2, ZEC) are all crypto-beta longs — a BTC/ETH reversal would hit all simultaneously; macro backdrop remains risk-on per fresh institutional flow (Bitmine ETH buy)", "Fed decision Wednesday (per external research) is a fresh, dated macro event this cycle not previously carried forward with a specific day attached — worth tracking into the mid-week reviews"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto weekly headline (A/B): sample=171 (165 triggered), winrate 22.4%, PF 1.81, avgR +0.29, total +34.0R — consistent with the 11:39 review's +35.2R/PF1.85, mild rolling-window drift, not a regime change", "by-mode split (from signal-stats): mode2 (likely swing) PF 3.70/avgR+0.85/+32.4R (strongest, unchanged as the desk's best mode), mode1 (likely intraday) PF 1.53/avgR+0.24/+10.6R (working), mode3 (likely scalp) PF 0.10/avgR-0.24/-9.0R (structurally negative, consistent with the scalp report's own low-confidence banner: 1W/7L over 14d, PF 0.14)", "stocks weekly: sample=0 A/B, C-tier n=203, winrate 3.0%, PF 0.56, -3.5R — unchanged structurally poor picture, zero live-capital implication; per-direction split shows both long (n=137, PF 0.53) and short (n=66, PF 0.65) C-tier cohorts underperforming", "signal-stats observations flag: reliable tier=B (n=171) triggered winrate 22% is low; weak-confidence weekend cohort (n=17) underperforms at 31% winrate — both carried, unresolved patterns"] },
    { "agent": "head_trader", "verdict": "manual_review",
      "reason_codes": ["longs_preferred", "wait_for_trigger", "mapping_weak", "headline_risk"],
      "data_missing": [], "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents — crypto stays risk-on/longs-preferred; stocks requires RTH confirmation before acting on the short book given the verified pre-market gap-up contradicts the internal risk_off label"] }
  ],
  "head_trader": {
    "overall_verdict": "manual_review",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate": { "symbol": "DIA/USDT", "trigger": "1h close inside the registered intraday pullback zone 0.1610-0.1676 with volume ticking back above 0.33x; do not market-buy the current ~0.1705 extension — note this exact setup has failed to fill repeatedly today across scalp/intraday/swing (confirmed NO_ENTRY, price ran away each time)", "reason": "highest-scored fresh crypto idea this cycle (66.1, intraday), OI-confirming positioning on the swing view, RS-leader vs BTC across all three timeframes all day — but the repeated failure-to-fill pattern is itself a data point: demand a real 1h close inside the zone, not just proximity" },
    "best_short_candidate": { "symbol": "SMH", "trigger": "WAIT for RTH confirmation after the 16:30 EEST open — specifically, wait to see whether the externally-verified pre-market gap-up (semis-heavy Nasdaq futures +1.28%) fades/rejects in the first 15-30 minutes before acting on the registered short zone; do NOT short into the gap", "reason": "highest raw score (85.15) in the stocks book, no legal/headline-risk flag (unlike UNH/TSLA/MSFT) — but this cycle's externally-verified pre-market strength (AI-capex/chip-sector tailwind per AAPL +3.53%, broad Nasdaq futures +1.28%) is a genuine counter-thesis to a clean semis short; the internal risk_off/short-bias regime label has not caught up to real-time pre-market data and should not be acted on blind" },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "playbook wait_pullback — no concrete entry zone registered yet (basket-level only, unchanged across multiple cycles today); wait for the desk to register specific levels on a subsequent scan before treating as actionable", "reason": "perps_dex_narrative basket remains the freshest genuinely-narrative-driven basket on the board without a concrete signal yet; separately, ZEC/USDT (already OPEN_ACTIVE swing) now has a confirmed genuine fresh catalyst (Zcash Ironwood upgrade) supporting the existing position — a stronger catalyst-confirmation story than HYPE's basket-only status, but ZEC is a manage-only position, not a fresh entry-watch" },
    "avoid_candidate": { "symbol": "UNH", "reason": "active DOJ/Medicare-fraud legal-risk flag plus earnings tomorrow (2026-07-28), block_requires_operator_review — raw score 81.99 (A-tier raw) but never actionable regardless of the market-closed gate clearing or the pre-market gap-up; manual review required if this ever surfaces again" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.60 | risk_on, mixed, longs_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, no_catalyst, fresh_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.50 | oi_supports, squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | chase_risk, entry_late, price_moved_away, clean_retest | advisory_only |
| execution_lifecycle | needs_review | 0.70 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | manual_review | 0.60 | headline_risk, correlation_cluster, legal_risk | advisory_only |
| playbook_performance | ok | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | manual_review | — | longs_preferred, wait_for_trigger, mapping_weak, headline_risk | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-07-27_1139.md` (Europe / pre-US context, 11:39 EEST, same day):

- **New and most important this cycle: internal stocks regime (risk_off/short) is now directly contradicted by verified pre-market futures data.** The 11:39 review had stocks still closed/pre-market with no futures-level check performed. This cycle's WebFetch confirms Dow/S&P/Nasdaq futures all up 0.8-1.3% on the same US-Iran ceasefire/oil-decline driver that pushed crypto risk-on — a genuine gap-risk finding for every stocks short candidate.
- **ZAMA/USDT closed WIN +1.0R** since the 11:39 review (was OPEN_ACTIVE intraday then) — no longer an open position.
- **AERO/USDT graduated from WAITING_FOR_ENTRY (11:39) to OPEN_ACTIVE (this review, intraday)** — filled since the last cycle.
- **ZEC/USDT gained a genuine external catalyst** (Zcash Ironwood upgrade, 11:10 EEST) not present at the 11:39 review and not visible in the internal structured catalyst layer — supports the existing OPEN_ACTIVE swing position.
- **DIA/USDT long-watch persists but the chase-risk read hardened**: still the highest-scored waiting/fresh crypto idea (66.1 this cycle vs. 73.9 at 11:39 on the swing view specifically), but the lifecycle log now shows confirmed repeated NO_ENTRY across all three modes today — the 11:39 review flagged chase-risk as a live concern; this review confirms it actually played out (price ran away before fill, multiple times).
- **Untracked legacy alerts reappeared**: 0 at 11:39, **2 this cycle** (ZAMA/USDT, DIA/USDT, both sent 12:44 EEST) — a recurrence of the high-priority watchlist-alert/signal-reuse defect (see §14).
- **Catalyst mapping degraded further**: 67.9% unmapped this cycle vs. 65.3% at 11:39 — the 5th consecutive worsening data point (60.1%->60.9%->64.6%->65.3%->67.9%).
- **Unchanged**: no A-tier anywhere; KAITO/USDT still avoid-for-new-entries on no volume confirmation; LA/USDT still OPEN_ACTIVE in both intraday and swing, manage-only; UNH/TSLA/MSFT still correctly excluded on legal/headline-risk grounds; HYPE/USDT still basket-only with no concrete signal; XOM's cosmetic UNKNOWN_INCONSISTENT status persists.

## 5. Catalyst Coverage

- Total catalyst events today (`data/catalysts/2026-07-27/catalyst_events.jsonl`, cumulative, computed directly): **2,500**
- Mapped (has symbol): **803** (32.1%)
- Unmapped (no symbol): **1,697** (67.9%)
- Narrative baskets: **6** — delisting_thin_liquidity, binance_ecosystem_teaser (BNB primary, fresh <1h), ai_narrative (NEAR/RENDER/TAO/FET primary, fresh <6h), perps_dex_narrative (HYPE primary, fresh <24h), rwa_narrative (ONDO/XLM primary, fresh <1h), momentum_breakout (NIL/PUMP/ZAMA primary, fresh <1h)
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (67.9% > 50% threshold; 5th consecutive worsening cycle)
- Top 3 unmapped headlines: "MEXC to Convert CXMTUSDT Pre-IPO Futures into Standard Futures #New_Listings"; "WEMIX reports contract breach tied to WEMIX$ stablecoin, attacker mints tokens and moves about $724,000"; "#Bithumb News OPEN API 1.0 Allowed IP Unregistered Key Bulk Blocking Information" — same pattern as prior cycles today (routine exchange/ops notices and macro-official-quote chatter, not missed single-symbol trading catalysts for today's top candidates).
- ZEC/USDT's genuine external catalyst (Zcash Ironwood upgrade, 11:10 EEST) is **not present** in the internal structured catalyst layer for this symbol — a missed-mapping example distinct from the routine unmapped noise, same defect family as the LA/USDT and EUL/USDT misses tracked in prior cycles.

## 6. Market Landscape

Crypto: BTC uptrend, ETH uptrend across scalp/intraday; altcoin breadth 64.1% (intraday) / 71.8% (swing, carried) above EMA20. Internal regime label: bullish trend (risk-on), recommended style "selective longs; prefer pullbacks on relative strength." Internal macro/geopolitical risk score reads 100/100 (headline-lagged, same pattern as prior cycles); the actual macro backdrop continues to improve (US-Iran ceasefire holding, oil down sharply) and fresh institutional-flow news reinforces risk-on (Bitmine +9,946 ETH this week, ETH testing $2,000; Strategy holding steady at 843,775 BTC with $3.75B cash reserve). Stocks: internal regime label is risk_off/short-biased (VIX 17.71, 0/4 indices trending up, breadth 0%) generated at 16:19 EEST — but externally-verified pre-market futures directly contradict this: Dow +1.14%, S&P 500 +0.84%, Nasdaq +1.28%, driven by the same ceasefire/oil de-escalation lifting crypto, plus a Fed decision Wednesday and this week's Big Tech earnings (MSFT/META Wednesday-ish, AAPL/AMZN/COIN/MSTR/XOM within days) as the near-term event calendar. This is a live pre-open contradiction, not a resolved one — treat the internal risk_off/short label as stale-lagging real-time price action, and require RTH confirmation before acting on either side.

### Market Mood / Risk Routing
- Crypto mood: **risk-on** (unchanged all day; reinforced by fresh institutional ETH accumulation news this cycle)
- Stocks mood: **mixed / contradiction** — internal label risk_off/short-bias vs. externally-verified pre-market futures gap-up (+0.8-1.3% across Dow/S&P/Nasdaq); resolve only after RTH confirmation
- Dominant narrative: crypto RS-momentum names (DIA, LA, KAITO, ESP, ZEC) still dominate the top-symbols list; ZEC now has genuine catalyst backing (Ironwood upgrade); stocks narrative is AI-capex/Big-Tech-earnings-week vs. semis-sector-weakness tension, unresolved until the open
- Preferred side now: **longs (crypto)**; **wait-for-trigger (stocks)** — do not short into a confirmed pre-market gap-up without RTH confirmation
- Best long candidate: **DIA/USDT** (registered intraday zone 0.1610-0.1676; note repeated failure-to-fill today — demand an actual close inside the zone)
- Best short candidate: **SMH** (stocks, highest raw score with no legal flag — but wait for the gap-up to fade/reject before acting; do not short pre-open or in the first minutes of RTH)
- Best catalyst-backed candidate: **HYPE/USDT** (perps_dex_narrative, still basket-only, no concrete levels); note ZEC/USDT's fresh Ironwood catalyst supports its existing OPEN_ACTIVE swing position
- What to avoid: **KAITO/USDT** (no volume confirmation, unresolved chase-risk); **UNH/TSLA/MSFT** (stocks, standing legal/headline-risk flags, unaffected by the gap-up debate); shorting the stocks book blind into the verified pre-market gap-up
- What would change the view: RTH confirmation in the first 15-30 minutes post-open showing the gap-up either holding (favors longs/AI-capex names, invalidates the semis-short thesis for now) or fading/reversing (re-opens the internal risk_off/short-bias case); a 1h close for DIA/USDT actually inside 0.1610-0.1676; a BTC 1h close below local support (would reopen risk-off for the 4 open crypto longs)

## 7. Candidate Deep Dives

### 1. DIA/USDT (long, best long-watch — repeated fill failure)
- Has price already reacted to the catalyst? No verified catalyst exists; pure RS-momentum (+21.5-22.8% vs BTC across scalp/intraday today).
- Is the setup chasing? Yes at the current price (~0.1705); registered intraday pullback zone (0.1610-0.1676) sits just below.
- Retest/pullback structure? Nominally yes — a defined zone exists — but the lifecycle log shows this exact pattern has failed to fill repeatedly today across scalp, intraday, and swing modes ("price ran away from the entry zone before a fill" logged multiple times).
- Overextended (>2 ATR from EMA20)? Not explicitly flagged, but the persistent no-fill pattern functions as a practical overextension signal regardless of the raw ATR math.
- Would entry now be late? Yes at market; the desk's own repeated no-fills argue for real patience here, not just nominal patience.
- What level makes it actionable? An actual 1h close inside 0.1610-0.1676 with volume ticking above ~0.33x — not just price touching the zone intraday.
- Aligned with market mood? Yes directionally (longs preferred, RS-leader) but the fill-failure pattern is itself a market-mood signal: buyers are not willing to pay down into the zone, which argues the "pullback" thesis may keep getting invalidated by shallow dips.
- Long, short, or wait-for-trigger? Wait-for-trigger, with elevated skepticism this cycle given the repeated no-fill history.
- Actionable now or after confirmation? After confirmation only — and demand a real close, not proximity.
- What would invalidate it? 1h close beyond 0.1530 (registered intraday) / 0.1314 (registered swing).
- Chase risk? High at market; still meaningful even at the registered zone given today's fill-failure pattern.
- Catalyst confirmation or contradiction? None — pure momentum/derivatives-confirmed, no catalyst either way.

### 2. ZEC/USDT (long, OPEN_ACTIVE swing — genuine catalyst confirmed, manage only)
- Has price already reacted? Position filled earlier inside its registered swing zone (498.83-501.18); current desk notes show price ~502.
- Chasing? No — existing filled position, not a fresh-entry decision.
- Retest structure? N/A — manage TP/SL only (TP1 507.46 / TP2 512.69 / TP3 517.93, invalidation 495.95 per the registering swing report).
- External catalyst check: genuine <24h hit found via direct `news_items` query — Zcash "Ironwood" upgrade (new shielded pool, supply safeguards), t.me/wublockchainenglish, 11:10 EEST, single_source. Not independently WebFetch-verified beyond the internal ingest, but the source (a dedicated blockchain-news channel) and specificity (named upgrade, technical detail) argue against it being noise.
- Internal catalyst layer check: this genuine catalyst is **not present** in `catalyst_events.jsonl` for ZEC/USDT — a missed-mapping example (see §5, §14).
- Actionable now or after confirmation? Already filled — decision is manage, not enter/add.
- What would invalidate it? 1h close beyond 495.95 (registered).
- Chase risk? N/A for the existing fill; would be moderate for a fresh add given the 24h return is still modest (+3.15%) relative to other RS-leaders.
- Catalyst confirmation or contradiction? Confirmation (Ironwood upgrade), not visible internally — strengthens the case for holding the existing position through its registered TP ladder rather than tightening early.

### 3. AERO/USDT (long, OPEN_ACTIVE intraday — manage only)
- Has price already reacted? Filled earlier since the 11:39 review (was WAITING_FOR_ENTRY then); now OPEN_ACTIVE.
- Chasing? No — existing filled position.
- Retest structure? N/A — manage TP/SL (TP1 0.4485 / TP2 0.4559 / TP3 0.4633, invalidation 0.4322 per the registering intraday report).
- Catalyst/news: no fresh verified catalyst detected for AERO in any report or the direct news_items check.
- Actionable now or after confirmation? Already filled — manage only, do not add at the current 24h return of +6.55%/RS +5.86% (moderate, not extended, but no fresh reason to increase size either).
- What would invalidate it? 1h close beyond 0.4322 (registered).
- Chase risk? N/A for the existing fill.
- Catalyst confirmation or contradiction? None either way — pure RS/momentum thesis, unresolved.

### 4. LA/USDT (long, OPEN_ACTIVE both intraday and swing — manage only, do not add)
- Has price already reacted? Filled in both modes; carried context from the 11:39 review already flagged LA/USDT (Lagrange Protocol) with an external Foundation buyback catalyst (2026-07-14) not visible internally — unchanged this cycle, no new external check performed given no material change in the position.
- Chasing? No — two existing filled positions (intraday + swing), not a fresh-entry decision; having both modes open on the same symbol concentrates single-name risk somewhat, worth noting for position-sizing awareness even though this routine makes no sizing changes.
- Retest structure? N/A — manage TP/SL per each mode's registered levels (swing: TP1 0.0782/TP2 0.0823/TP3 0.0865, invalidation 0.0690; intraday levels not independently re-pulled this cycle).
- Internal news_items check: not re-run this cycle for LA specifically (no material change since 11:39); the carried substring-collision defect for this ticker remains an open TODO (see §14).
- Actionable now or after confirmation? Already filled in both modes — manage only.
- What would invalidate it? 1h close beyond the registered invalidation levels per mode.
- Chase risk? N/A for the existing fills; would be high for any fresh add given the accumulated 24h/7d gains already captured.
- Catalyst confirmation or contradiction? Mild external confirmation carried from the 11:39 review (buyback), not visible internally — no contradiction.

### 5. SMH (short, stocks — best short-watch, gap-risk caveat is the headline finding this cycle)
- Has price already reacted? Internal report reflects the last RTH close structure (raw score 85.15, unchanged all day); externally, semis-heavy Nasdaq futures are up ~1.28% pre-market on the ceasefire/oil driver plus a genuine AI-capex tailwind narrative (AAPL +3.53% premarket, Samsung/Broadcom AI-memory MOU headline in today's stocks report).
- Is the setup chasing? Cannot assess pre-market in the traditional sense — the relevant question this cycle is whether the internal short thesis survives contact with a verified gap-up, not whether the entry itself is late.
- Retest/pullback structure? Not yet establishable — wait for the first 15-30 minutes of RTH to see if the gap holds or fades.
- Overextended? N/A pre-open.
- Would entry now be late/wrong? Entering the short pre-open or immediately at the open would be entering directly against a verified, dated (this morning) gap-up — high risk of being caught in a squeeze regardless of the underlying weekly/monthly technical picture.
- What level makes it actionable? Confirmation that the gap-up fades or reverses within the first 15-30 minutes of RTH, with a 1h close breaking the registered short zone — not simply "market open."
- Aligned with market mood? This is exactly the open question this cycle: the internal risk_off/short label says yes, the verified external pre-market data says no (for now) — hence "mixed/contradiction" rather than a clean directional read.
- Long, short, or wait-for-trigger? Wait-for-trigger, explicitly.
- Actionable now or after confirmation? Not actionable now; requires RTH confirmation.
- What would invalidate the short idea entirely (for today)? The gap-up holding through the first 30-60 minutes with sector-wide (SMH/AVGO/XLK) participation — would argue the AI-capex/chip-tailwind narrative is winning today, not the risk_off regime.
- Chase risk? High if entered pre-open or at the open; the whole point of this deep dive is to wait.
- Catalyst confirmation or contradiction? Contradiction — the internal short-bias thesis is being challenged by real-time pre-market strength; no fresh single-symbol SMH-specific catalyst either way.
- Legal/headline risk? None flagged (unlike UNH/TSLA/MSFT) — the only demotion reason on record is `market_closed_intraday_planning_only`, which is about to clear naturally at the open.

## 8. Best Candidates Ranked

1. **Long-watch: DIA/USDT** — trigger: actual 1h close inside 0.1610-0.1676 with volume >0.33x; highest-scored fresh crypto idea (66.1) but has failed to fill repeatedly today — demand a real close, not proximity.
2. **Short-watch: SMH** — trigger: RTH confirmation that the verified pre-market gap-up (Dow/S&P/Nasdaq +0.8-1.3%) fades/rejects within the first 15-30 minutes, then a 1h close breaking the registered short zone; do NOT short into the gap.
3. **Catalyst-watch: HYPE/USDT** — trigger: wait for the desk to register a concrete signal off the perps_dex_narrative basket; no tradeable levels exist yet.
4. **Avoid (crypto): KAITO/USDT** — no volume confirmation, unresolved chase-risk for any new entry.
5. **Avoid (stocks): UNH** — active DOJ/Medicare-fraud legal-risk flag + earnings tomorrow; never actionable regardless of score or the gap-up debate.
6. **Monitor-only (already open, do not add): AERO/USDT (intraday), LA/USDT (intraday + swing), ZEC/USDT (swing, genuine catalyst confirmed)** — all OPEN_ACTIVE per the paper-monitor lifecycle; manage existing TP/SL only.

## 9. Avoid / No Trade

This applies to the current decision window only — scanning, tracking, and the scheduler continue unchanged regardless.

- **Shorting the stocks book (SMH, AVGO, XLK, META, QQQ, MSTR, AMD, COIN, AMZN, TSLA, DIA, SPY, MSFT) pre-open or in the first minutes of RTH** — verified pre-market futures show a strong gap-up directly contradicting the internal risk_off/short-bias regime label; wait for confirmation the gap fades before acting.
- **KAITO/USDT** (any mode) — no volume confirmation, unresolved chase-risk; wait for a rebuild above ~0.5x.
- **All crypto shorts today** (SYN, RE, RIF, ALLO, EUL) — every one is squeeze-capped (thin liquidity) fighting a bullish-trend regime.
- **DIA/USDT at market** (~0.1705) — chasing above the registered zone; the repeated no-fill pattern today argues for real patience, not just nominal patience.
- **UNH, TSLA, MSFT** (stocks) — active legal/headline-risk flags (DOJ probe, going-concern, class-action/securities-fraud respectively); manual review required regardless of score or the futures-driven gap-up.
- **Adding to LA/USDT** at current extension in either mode (intraday or swing) — manage the existing fills for TP/SL only.

## 10. Main Risks

- **Gap risk at the US open**: the internal stocks regime label (risk_off/short) is stale relative to a verified, dated (this morning) pre-market futures gap-up (Dow/S&P/Nasdaq +0.8-1.3%) — the single biggest actionable risk this cycle for anyone tempted to short the C-tier stocks book blind.
- Correlation cluster: 4 open crypto long positions (AERO, LA x2, ZEC) are all crypto-beta longs — a BTC/ETH reversal would hit all simultaneously; macro backdrop remains risk-on per fresh institutional flow, but this is a standing structural risk regardless of today's specific mood.
- Recurrence of the untracked-legacy-alert defect: 2 crypto alerts (ZAMA/USDT, DIA/USDT) sent to Telegram without a matching `proposed_signal` this cycle — these will silently not contribute to PF/winrate tracking, understating true alert volume in the performance stats.
- Catalyst mapping at 67.9% unmapped this cycle — the 5th consecutive worsening data point; genuine catalysts (ZEC's Ironwood upgrade this cycle, LA's buyback previously) continue to be missed by the internal layer entirely.
- Stale-active-signals / lifecycle-field inconsistency persists (1 stocks row, XOM, unmapped status field on the authoritative lifecycle view) — readability risk for manual review only, not a live-trading risk.
- Paper-monitor lifecycle snapshot is the least-fresh core input this cycle (~3h09m old) — the 4 OPEN_ACTIVE / 2 WAITING_FOR_ENTRY counts should be treated as directionally correct but not to-the-minute.
- Fed decision scheduled for Wednesday (per this cycle's external research) — a fresh, dated macro event to track into the mid-week reviews; not previously carried with a specific day attached.
- Source-ingest step (§M) failed twice this cycle with `sqlite3.OperationalError: database is locked` (the scheduler is actively writing to `db/crypto_ai_desk.sqlite` mid-cycle) — the 2 cited external sources were not written to `news_items`. Non-fatal per routine; the citations remain valid in §13 of this document, just not mirrored into the DB this cycle.

## 11. Action Plan — next 4 hours

- **At the open (~16:30 EEST / 09:30 ET): do NOT short SMH/AVGO/XLK/META/QQQ/MSTR/AMD/COIN/AMZN/TSLA/DIA/SPY/MSFT blind.** Watch the first 15-30 minutes of RTH to see whether the verified pre-market gap-up holds (favors AI-capex/chip-tailwind names, invalidates the short thesis for now) or fades (re-opens the internal risk_off/short-bias case) before acting on any registered short zone.
- Monitor the 4 OPEN_ACTIVE crypto positions (AERO-intraday, LA-intraday, LA-swing, ZEC-swing) for TP/SL — no new entries against these theses, no adds.
- Watch DIA/USDT for an actual 1h close inside 0.1610-0.1676 with volume pickup — do not treat mere proximity as a signal given today's repeated no-fill pattern.
- Watch NIL/USDT and AKE/USDT (both registered WAITING_FOR_ENTRY, intraday) for their own entry triggers; no fresh evidence reviewed this cycle beyond registered levels.
- Do not chase KAITO/USDT at current extended, volume-unconfirmed levels.
- Watch for the desk to register a concrete HYPE/USDT (or DYDX/GMX/ASTER) signal off the perps_dex_narrative basket.
- Re-confirm BTC/ETH structure has held the risk-on move through the US session into the 18:30 EEST US-open-reaction review — that review should specifically resolve whether the stocks gap-up held or faded.

## 12. Final Verdict per Mode

- **Scalp (crypto):** No trade. Structurally negative this week (PF 0.10 by mode-split, consistent with the report's own 14d PF 0.14 banner); no A/B ideas this cycle.
- **Intraday (crypto):** Monitor AERO (OPEN_ACTIVE); watch NIL/AKE (WAITING_FOR_ENTRY); watch DIA (repeated no-fill, demand a real close); avoid KAITO for new entries.
- **Swing (crypto):** Hold/monitor. Strongest playbook this week (PF ~3.7 by mode-split); ZEC (OPEN_ACTIVE, catalyst-confirmed) and LA (OPEN_ACTIVE) — manage TP/SL, do not add.
- **Intraday (stocks):** No trade yet — wait for RTH confirmation on the gap-up/gap-down question before acting on any registered short (SMH cleanest, no legal flag) or reconsidering any long (AAPL notable premarket strength, but no internal setup registered). UNH/TSLA/MSFT excluded regardless of outcome.
- **Swing/Invest (stocks):** No trade — framework deprecated per prior audits, data 25 days stale, not a fresh gap.

## 13. Sources

- [Stock market today: Dow, S&P 500, Nasdaq futures rise as oil tumbles, investors brace for busy week](https://finance.yahoo.com/markets/live/stock-market-today-monday-july-27-dow-sp-500-nasdaq-080412540.html) — WebFetch-verified 2026-07-27; pre-market futures levels (Dow +1.14%/52,719, S&P 500 +0.84%/7,509.75, Nasdaq +1.28%/28,644.25), Brent crude down >7%, Fed decision Wednesday, AAPL +3.53% premarket.
- [Stock Market: Will S&P 500 Open Up or Down Today?](https://www.benzinga.com/markets/prediction-markets/26/07/60687326/stock-market-will-sp-500-open-up-or-down-today-11) — background context (88% "up-open" prediction-market read), not independently WebFetch-verified.
- Internal `news_items` (direct SQL query): Ethereum rises to test $2,000 (t.me/whale_alert_io, 2026-07-27T12:36 UTC); Bitmine adds 9,946 ETH (t.me/lookonchain, CoinMarketCapAnnouncements, wublockchainenglish, marketfeed — cross-posted, 2026-07-27T12:36-12:45 UTC); Zcash Ironwood upgrade (t.me/wublockchainenglish, 2026-07-27T11:10 UTC).
- Internal: `data/reports/scalp/2026-07-27_12-32_scalp_report.md`, `data/reports/intraday/2026-07-27_12-44_intraday_report.md`, `data/reports/swing/2026-07-27_01-58_swing_report.md`, `data/reports/stocks/intraday/2026-07-27_13-19_stocks_intraday_report.md`, `data/catalysts/2026-07-27/catalyst_cycle_12-51.md`, `reports/PAPER_MONITOR_STATUS_LATEST.md`.

## 14. Fix Requests / TODO

### TODO-untracked-legacy-alert-recurrence (carried, new same-day evidence)
- **issue:** `detect_untracked_legacy_alerts` shows 2 crypto alerts sent to Telegram this cycle without a matching `proposed_signal` — ZAMA/USDT and DIA/USDT, both intraday, sent 12:44 EEST. This is a recurrence of a previously-flagged high-priority defect (untracked-alert re-fire reusing a stale/closed signal_id instead of minting a new `proposed_signal`, confirmed previously on ALLO/USDT and BANK/USDT).
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-27` output this cycle: "2 untracked legacy crypto alert(s)... will NOT contribute to PF / winrate / avgR."
- **suggested manual fix:** unchanged from the prior TODO — investigate the watchlist-alert re-fire path for stale/closed signal_id reuse instead of minting a fresh `proposed_signal`; this was already raised to high priority 2026-07-17 and continues to recur.
- **priority:** high (unchanged/reconfirmed — recurring defect with fresh same-day evidence).
- **first observed:** 2026-07-17 (ALLO/USDT, BANK/USDT); reconfirmed 2026-07-27 16:31 EEST (ZAMA/USDT, DIA/USDT).

### TODO-catalyst-mapping-coverage (carried, new data point — now 5 consecutive worsening cycles)
- **issue:** Catalyst-event symbol-mapping coverage has been below the 50% weak-mapping threshold for at least 5 consecutive reviews today and continues trending worse: 60.1%->60.9%->64.6%->65.3%->**67.9%** (this run).
- **evidence:** direct tally of `data/catalysts/2026-07-27/catalyst_events.jsonl` this cycle (2,500 cumulative rows, 803 mapped, 1,697 unmapped = 67.9%); prior-review figures cited in `OPUS_ENRICHED_REVIEW_AUTO_2026-07-27_1139.md` §5. This cycle adds a new concrete missed-catalyst example: ZEC/USDT's Zcash Ironwood upgrade (genuine, <24h, found via direct news_items query) is entirely absent from the structured catalyst layer for that symbol.
- **suggested manual fix:** unchanged — a human-driven session should sample the unmapped set for genuine missed single-symbol catalysts (ZEC/USDT's Ironwood-upgrade miss is now the third concrete example this week, after LA/USDT's buyback and the standing EUL/USDT case) and assess whether the resolver's symbol dictionary/source coverage needs expansion, particularly for dedicated crypto-news Telegram channels.
- **priority:** high (raised from medium — three independent concrete missed-catalyst examples now identified across recent cycles, not just routine unmapped noise, plus a continuously-worsening trend line).
- **first observed:** trend noted 2026-07-26 (60.1%->60.9%); this run adds a 5th data point (67.9%) and a 3rd concrete missed-catalyst example (ZEC/USDT).

### TODO-stocks-regime-label-gap-risk-lag (new this cycle)
- **issue:** The internal stocks-intraday regime label (risk_off/short bias, VIX 17.71, breadth 0%) is computed from the last RTH close and does not incorporate real-time pre-market futures data. This cycle, the label was directly contradicted by verified pre-market futures showing a strong gap-up (Dow +1.14%, S&P 500 +0.84%, Nasdaq +1.28%) roughly 10 minutes before the report's own generation timestamp (16:19 EEST) — meaning the regime label was already stale relative to observable market data at the moment it was written, purely because it has no pre-market futures input.
- **evidence:** `data/reports/stocks/intraday/2026-07-27_13-19_stocks_intraday_report.md` §1 (risk_off, VIX 17.71, breadth 0%) vs. WebFetch-verified Yahoo Finance pre-market futures data at the same point in time (Dow/S&P/Nasdaq futures all +0.8-1.3%, driven by the US-Iran ceasefire and falling oil).
- **suggested manual fix:** consider adding a pre-market futures/index-future snapshot (Dow/S&P/Nasdaq futures % change) as a lightweight additional input or at minimum a displayed caveat line in the stocks-intraday report specifically for the pre-US-open window, so the regime label doesn't silently lag known, observable pre-market direction during the ~30-60 minutes before the cash open.
- **priority:** medium (no live-trading impact — this routine is advisory-only and catches the discrepancy manually each pre-US-open cycle — but a recurring blind spot specifically in the highest-stakes decision window of the day).
- **first observed:** 2026-07-27 16:31 EEST (this run).

### TODO-stale-active-signals (carried, unchanged)
- **issue:** The authoritative `PAPER_MONITOR_STATUS_LATEST.md` lifecycle view continues to show 1 `UNKNOWN_INCONSISTENT` row: XOM (stocks/intraday/B) with an unmapped status field `'tp2_hit'`.
- **evidence:** `reports/PAPER_MONITOR_STATUS_LATEST.md` (13:22 EEST), same as the 11:39 and 04:46 reviews.
- **suggested manual fix:** unchanged — extend the paper-monitor status-mapping table to recognize `'tp2_hit'` as a valid intermediate status for stocks signals.
- **priority:** low (no functional/routing impact observed; readability issue for manual review only).
- **first observed:** carried context from multiple prior reviews; still present this cycle (2026-07-27 16:31 EEST).

## Telegram

```
[AUTO-REVIEW pre-US-open 16:31 EEST]

Mood:
- Crypto: risk-on (BTC/ETH uptrend, fresh Bitmine ETH buy)
- Stocks: mixed — internal risk_off/short vs verified pre-market gap-up (Dow/S&P/NDX +0.8-1.3%)
- Prefer: longs (crypto) / wait-for-trigger (stocks, pending RTH)

Status:
- Open actionable: 4 (AERO-intraday, LA-intraday, LA-swing, ZEC-swing)
- Waiting for entry: 2 (NIL-intraday, AKE-intraday)
- Review/Shadow: 34
- Entered unresolved: 0
- No-entry/stale/moved-away: 57
- Needs review: 1 (XOM unmapped status, cosmetic) + 2 untracked legacy alerts (ZAMA, DIA)

Decisions:
- Long-watch:     DIA/USDT trigger 1h close 0.1610-0.1676 vol>0.33x (has failed to fill repeatedly today)
- Short-watch:    SMH trigger RTH gap-fade confirmation post-open — do NOT short into the verified gap-up
- Catalyst-watch: HYPE/USDT perps_dex_narrative, no concrete levels yet
- Avoid:          KAITO/USDT (no volume) / UNH (DOJ + earnings tomorrow)

Risk:
- Verified pre-market futures gap-up (Dow/S&P/NDX +0.8-1.3%) contradicts the internal stocks risk_off/short regime label — gap risk for the entire C-tier short book at the open.

Catalyst coverage: mapped 803/2500 (32.1%), baskets 6
                   weak this run — context only

File: OPUS_ENRICHED_REVIEW_LATEST.md
Advisory only. No auto-trade.
```
