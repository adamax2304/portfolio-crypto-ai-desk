# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:46 EEST

## 1. Executive Summary

Slot: **crypto overnight / Asia review** (Monday 2026-07-27, run at 04:46 EEST, ~16min after the nominal 04:30 slot — dispatch jitter). **Advisory only — no auto-trade.** Stocks are fully closed (pre-market, US cash opens ~16:30 EEST) — all 50 stocks active-signals are tier=C, planning/watchlist only, not actionable until RTH confirmation. Crypto is the only live actionable class this slot. No fresh A/B setup appeared in this cycle's scalp or intraday reports (both "No A-tier setups found" / "No B-tier setups found" for new ideas) — the book's B-tier signals are all carried from the 22:48-01:36 scan wave. Per the paper-monitor lifecycle view (authoritative, `reports/PAPER_MONITOR_STATUS_LATEST.md`, generated 01:59 EEST): **6 crypto positions OPEN_ACTIVE** (BANK/USDT-intraday, EPIC/USDT-intraday, EPIC/USDT-swing, EUL/USDT-swing, PENGU/USDT-swing, ORDI/USDT-swing — all long), **6 WAITING_FOR_ENTRY** (EUL/DIA/KAITO-intraday, KAITO/LTC/DIA-swing), **2 NO_ENTRY_EXPIRED** (LA/USDT-intraday, PENGU/USDT-scalp aged out), 1 status-field inconsistency (XOM stocks/intraday tp2_hit unmapped — needs_review, cosmetic). Market regime is bullish-trend/risk-on by price structure (BTC transition_up, ETH uptrend, altcoin breadth 61.5% above EMA20) but macro/geopolitical risk reads 100/100 (Iran/Israel/Red-Sea-Houthi/oil-price headline stream) — external WebSearch this cycle finds the oil spike (Brent ~$97.66) has **not** broken BTC's structure (BTC still holding ~$65k per external sources), consistent with the internal "transition_up" read; this is a genuine price/headline divergence, not resolved either way. Catalyst mapping is weak this cycle (64.6% unmapped, 177/500 mapped) — treat the catalyst layer as context, not decision input. No fresh verified catalyst backs any of today's top RS-momentum longs (ESP, KAITO, LA, DIA, EUL, EPIC, ORDI, PENGU all show "no fresh verified catalyst detected"; a `LA` substring match in `news_items` today is a false positive on unrelated SpaceX/Tesla headlines, reconfirming the long-running symbol-resolver TODO). External research flags a real caution on KAITO/USDT specifically: daily RSI ~77 (compressed R:R for new longs) and a reported ~1.8% supply token-unlock (single-source, not independently re-verified) — both weigh against chasing KAITO despite it being a registered waiting_for_entry B-tier signal in two modes. Two TODOs carried from prior cycles, no code touched.

## 2. Data Used

- Reports: `data/reports/scalp/2026-07-27_01-09_scalp_report.md` (mtime 04:08 EEST, ~38min old, data-as-of 01:00 UTC), `data/reports/intraday/2026-07-27_01-15_intraday_report.md` (mtime 04:15 EEST, ~31min old, data-as-of 01:00 UTC) — both fresh, latest of the day. `data/reports/swing/2026-07-26_14-52_swing_report.md` (mtime 17:52 EEST previous day, ~10h50m old, data-as-of 14:45 UTC) — **carry-forward** (4-12h band, near its upper edge), no fresher swing cycle since; used with a flag per §E.
- Stocks: `data/reports/stocks/intraday/2026-07-27_01-36_stocks_intraday_report.md` (mtime 04:36 EEST, ~10min old, fresh) — market closed (pre-market), report itself demotes all A/B to C by policy (`market_closed_intraday_planning_only`). Stocks swing/invest reports are from 2026-07-02 (25 days stale) — this framework is deprecated per prior audits ([[project_crypto_ai_desk_stocks_position_framework]]), not treated as a data gap, market closed regardless.
- Catalysts: `data/catalysts/2026-07-27/catalyst_events.jsonl` (500 events, computed directly — 177 mapped / 323 unmapped = 64.6% unmapped), `narrative_baskets.jsonl` (2 baskets: perps_dex_narrative primary HYPE/USDT, delisting_thin_liquidity), `catalyst_cycle_01-20.md` (fresh, generated 04:20 EEST — regenerated after the scalp/intraday reports, so the reports' own "catalyst scan has not run yet today" note is now stale by ~5-15min; the cycle file itself is the freshest catalyst source and was used directly).
- LLM packets: `data/processed/llm_analysis_packet.md` (fresh, 04:16 EEST), `data/processed/llm_stocks_packet.md` (fresh, 04:38 EEST).
- CLI: `active-signals` (crypto ×29, stocks ×50), `signal-stats` (crypto: weekly A/B sample=158, PF 1.92, +36R; stocks: weekly A/B sample=0, C-tier only, PF 0.56, -3.5R), `detect_untracked_legacy_alerts --since 2026-07-27` (clean — 0 untracked crypto alerts).
- Direct `db/crypto_ai_desk.sqlite` queries: `news_items.detected_symbols_json` 24h-freshness check for all 8 top crypto candidates (ESP, KAITO, LA, DIA, EUL, EPIC, ORDI, PENGU) — zero genuine hits, one false-positive substring match (LA → SpaceX/Tesla stories); `events`/catalyst mapped-vs-unmapped tally direct from JSONL (500/177/323); EUL Upbit-KRW-listing rows re-checked (still present, still mismapped to `["ETH","ETH/USDT"]` or `[]`, now ~28h old — aging out of freshness window but the resolver defect itself persists).
- `reports/PAPER_MONITOR_STATUS_LATEST.md` (mtime 01:59 EEST, ~2h47m old — generated by the prior scheduler cycle, still the latest lifecycle snapshot available; authoritative source for §3A execution_lifecycle and the Telegram Status block).
- External web research: 2 WebSearch + 1 WebFetch this cycle (KAITO catalyst/RSI/unlock check; BTC/ETH price vs. Iran/oil headline check) — see §13, both loaded successfully.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-26_2327.md` (post-close final daily review, 23:27 EEST, prior day).

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime 2026-07-27 04:39 EEST; latest cycle folder `cycle_04_01-16_summary.md` also stamped ~02:01 EEST for its own content but the folder's scheduler.log entry is live-updating — both well under the 3h defer threshold. **Not deferred.**
- Scalp/intraday reports regenerated this cycle (04:08-04:15 EEST, ~30-38min old at run time) — the freshest crypto data of the cycle.
- Swing report unchanged since 17:52 EEST the prior day (~10h50m old) — inside the 4-12h carry-forward band but near its upper edge; the desk's only B-tier crypto candidate this window (EUL/USDT LONG, score 65.1) originates from this carried report. Flagged, used with reduced weight.
- Stocks intraday report is fresh (04:36 EEST) but structurally non-actionable — US cash session closed until ~16:30 EEST; all candidates demoted A/B→C by `market_closed_intraday_planning_only`.
- Catalyst folder fresh (cycle regenerated 04:20 EEST, after the scalp/intraday reports were written — the reports' own in-body note "catalyst scan has not run yet today" is now outdated; this review used the fresher `catalyst_cycle_01-20.md` directly).
- `detect_untracked_legacy_alerts`: clean, 0 untracked crypto alerts.
- Paper-monitor lifecycle snapshot (`PAPER_MONITOR_STATUS_LATEST.md`) is ~2h47m old (last regenerated 01:59 EEST by the prior scheduler cycle) — still the best available lifecycle source, no fresher one exists at run time; used as-is with its age noted.
- News infra: only the standing Reddit 403 social-source failures (documented blindspot, unchanged for weeks) — no new ingest-pipeline concerns.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-07-27 04:46 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["fresher swing report than 10h50m carry-forward", "fresher paper-monitor lifecycle snapshot than 2h47m old"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log ~7min old at run time", "scalp/intraday reports regenerated 04:08-04:15 EEST, freshest of the cycle", "swing report unchanged since 17:52 EEST prior day (~10h50m, inside 4-12h carry-forward band, near upper edge)", "catalyst cycle regenerated 04:20 EEST, fresher than the scalp/intraday reports which pre-date it"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mixed", "longs_preferred", "risk_off", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC trend transition_up, ETH uptrend, altcoin breadth 61.5% above EMA20 — bullish-trend/risk-on price structure per internal regime label", "macro/geopolitical risk 100/100 (8 risk-off hits, 1 risk-on, 2 calendar) driven by Iran/Israel/Red-Sea/oil headlines", "external WebSearch this cycle: BTC holding near $65k, ETH ~$1,874 testing resistance ~$1,950, despite Brent crude near $97.66 — price/headline divergence persists, not yet resolved either way", "stocks regime is risk_off/short-biased but market closed, planning-only"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "no_catalyst", "mapping_weak"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["500 catalyst events today, 323 unmapped (64.6%) — weak mapping, worse than yesterday post-close's 60.9%", "all 8 top crypto RS-momentum names (ESP, KAITO, LA, DIA, EUL, EPIC, ORDI, PENGU) show zero genuine <24h news_items hits; LA/USDT's apparent match is a false-positive substring collision on unrelated SpaceX/Tesla headlines", "EUL/USDT Upbit-KRW-listing rows still present in news_items and still mismapped to ETH/empty, now ~28h old — same resolver defect as the carried TODO, aging out of freshness relevance but structurally unresolved", "perps_dex_narrative basket (HYPE/USDT primary, <1h fresh, playbook wait_pullback) is the one genuinely fresh narrative catalyst on the board, but not yet a registered proposed_signal with concrete levels" ] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "funding_extreme", "oi_supports", "data_unavailable"],
      "data_missing": ["OI history for several MEXC-only names"],
      "suggested_effect": "advisory_only",
      "facts_used": ["DEXE/USDT: extreme negative funding across bybit/mexc (-0.0044/-0.0033) — shorts are crowded and squeeze-prone, reduces confidence in the DEXE short-watch idea", "ESP/USDT: negative funding across bybit/okx/mexc, cross-exchange crowding flagged 'elevated' — shorts are paying longs after a 45%+ run, a genuine squeeze-fuel signal but also a sign the move may already be crowded/late", "RE/RIF/ARX/SYN/INJ all capped to C for thin_liquidity_short_squeeze_risk — no clean short structure on the board tonight", "KAITO/USDT and DIA/USDT show fresh OI build with price (fresh positioning confirms trend) — the cleanest derivatives-supported longs on the board, tempered by KAITO's RSI/unlock caution below" ] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["overextended", "chase_risk", "clean_retest", "entry_fresh"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["DIA/USDT: RS +14-15% vs BTC across scalp/intraday/swing, volume ratio improving toward the swing entry, OI up 101-242% — the highest-scored B-tier crypto signal in the active book (72.4, swing, waiting_for_entry) and the cleanest structural long-watch tonight", "KAITO/USDT: external RSI ~77 on the daily per cryptonomist.ch (2026-07-24, price then $1.05; internal price now $1.183-1.234, further extended) — compressed R:R for a fresh long; internal volume ratio only 0.17-0.2x, no confirmation rebuild", "ESP/USDT: +45-46%/24h, 50x volume spike on the swing report, now cooling to 0.19-0.26x on scalp/intraday — classic blow-off pattern, chasing here is late; C-tier watchlist correctly, not promoted", "EUL/USDT: price (2.268 on the carried swing report) sits above every defined entry zone on the intraday conditional (2.107-2.218 registered, 2.267-2.368 conditional) — still a chase-risk name, matches the carried catalyst-watch framing" ] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.65,
      "reason_codes": ["open_actionable", "waiting_for_entry", "no_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Paper-monitor lifecycle (01:59 EEST, authoritative): OPEN_ACTIVE=6 (BANK-intraday, EPIC-intraday, EPIC-swing, EUL-swing, PENGU-swing, ORDI-swing, all long), WAITING_FOR_ENTRY=6 (EUL/DIA/KAITO-intraday, KAITO/LTC/DIA-swing), REVIEW_ONLY_SHADOW=55 (mostly stocks C-tier), ENTERED_UNRESOLVED_EXPIRED=0, NO_ENTRY_EXPIRED=2 (LA-intraday, PENGU-scalp), UNKNOWN_INCONSISTENT=1 (XOM stocks/intraday, unmapped status 'tp2_hit')", "raw active-signals CLI (less authoritative, legacy-touch based) additionally shows KAITO/LA-scalp as 'triggered' with expires_at already past (03:16 EEST) — same stale-active-signals pattern as the carried TODO, now also affecting scalp-mode rows specifically", "detect_untracked_legacy_alerts: clean, 0 untracked crypto alerts" ] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["headline_risk", "reduce_risk", "correlation_cluster"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["macro/geopolitical risk 100/100 this cycle (up from recent-cycle norms) — Iran/Israel/Red-Sea/Houthi/oil headline stream, externally corroborated (Brent ~$97.66, near two-month high)", "UNH carries an active DOJ-probe/Medicare-fraud legal-risk flag (recurring across many cycles) — stocks A-tier raw score 82 demoted to C for both market-closed and legal-risk reasons; TSLA carries a going-concern flag; MSFT carries class-action/securities-fraud — all three correctly excluded from any actionable framing", "Fed decision scheduled 2026-07-28/29 (per external search) — a major macro catalyst landing within the next ~36-60h, worth flagging into the action plan even though outside this immediate 4h window", "correlated risk: BTC/ETH have not broken down yet despite the macro spike — a break would compound with the existing risk-off headline backdrop rather than being independent" ] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto weekly headline (A/B): sample=158 (148 triggered), winrate 21.0%, PF 1.92, avgR +0.32, total +36.0R", "by-mode split: swing PF 4.34/avgR+0.98/+33.4R (by far the strongest and the mode carrying tonight's only fresh idea, EUL), intraday PF 1.37/avgR+0.16/+7.4R (working, thin), scalp PF 0.47/avgR-0.15/-4.8R (structurally negative — scalp remains correctly low-confidence per the report's own header banner)", "stocks weekly: sample=0 A/B (all C-tier), C-tier sample=203, winrate 3.7%, PF 0.56, -3.5R — structurally poor but zero live-capital implication (never Telegram-actionable)", "signal-stats observation: weekend=Y crypto B-tier underperforms (winrate 21%, n=17) — today is Monday, this caution does not directly apply to today's fresh ideas but does still apply to the still-open weekend-registered positions (EPIC-swing, ORDI-swing, PENGU-swing, KAITO-swing, EUL-swing all tagged weekend=Y)" ] },
    { "agent": "head_trader", "verdict": "caution",
      "reason_codes": ["wait_for_trigger", "mapping_weak", "headline_risk"],
      "data_missing": [], "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.55,
    "preferred_side": "longs",
    "best_long_candidate": { "symbol": "DIA/USDT", "trigger": "1h close inside the registered swing pullback zone 0.123003-0.128747, ideally with volume ticking back above 0.3x (currently 0.19x on intraday, thin); do not market-buy the current +15%/24h extension", "reason": "highest-scored B-tier crypto signal in the active book (72.4, swing, waiting_for_entry), OI up 101-242% confirming fresh positioning, RS +14-15% vs BTC consistently across scalp/intraday/swing — the cleanest structurally-confirmed long on the board tonight, still no catalyst backing so treat as momentum-only" },
    "best_short_candidate": { "symbol": "SMH", "trigger": "RTH confirmation after the ~16:30 EEST US open, break below the registered short zone 561.125-565.06 (entry_low/high) with 1h close confirmation — do not act pre-market", "reason": "highest raw score (85.2) in the stocks book, no legal/headline-risk flag (unlike UNH/TSLA/MSFT), demoted to C purely for market-closed reasons — becomes the cleanest short-planning candidate once the cash session opens; crypto side has no clean short (RE/DEXE/RIF/ARX/SYN all squeeze-capped fighting a bullish tape)" },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "playbook wait_pullback — no concrete entry zone registered yet (basket-level only, not yet a proposed_signal); wait for the desk to register specific levels on the next scan before treating as actionable", "reason": "perps_dex_narrative basket (HYPE primary, DYDX/GMX/ASTER related) is <1h fresh per the 04:20 EEST catalyst cycle, the only genuinely fresh narrative catalyst on the board tonight — informational only until a concrete signal is registered" },
    "avoid_candidate": { "symbol": "KAITO/USDT", "reason": "registered waiting_for_entry B-tier in both intraday and swing modes, but external research flags daily RSI ~77 (compressed R:R, cryptonomist.ch 2026-07-24) plus a reported ~1.8% supply token-unlock (single-source, not independently re-verified) — combined with internal volume confirmation stuck at 0.17-0.2x, there is no fresh evidence supporting a chase here" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | caution | 0.60 | mixed, longs_preferred, risk_off, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, funding_extreme, oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | overextended, chase_risk, clean_retest, entry_fresh | advisory_only |
| execution_lifecycle | needs_review | 0.65 | open_actionable, waiting_for_entry, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, reduce_risk, correlation_cluster | advisory_only |
| playbook_performance | ok | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.55 | wait_for_trigger, mapping_weak, headline_risk | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-07-26_2327.md` (post-close final daily review, 23:27 EEST, prior day):

- **BANK/USDT graduated from long-watch to OPEN_ACTIVE**: the 23:27 review named BANK/USDT as the cleanest long-watch (pullback into 0.3885-0.3961). It has since triggered and is now an open intraday position per the paper-monitor lifecycle snapshot — the thesis played out as flagged, no new information changes it; simply monitor TP/SL now, not re-enter.
- **KAITO/USDT avoid-candidate reconfirmed with new external evidence**: the 23:27 review already flagged KAITO as avoid for lack of volume confirmation (0.2x, evaporated from 2.18x). This review adds external corroboration — daily RSI ~77 and a reported (single-source) ~1.8% unlock — strengthening rather than reversing the avoid call.
- **Macro risk read 100/100 tonight**, up from the already-elevated 91.6/100 at 23:27 — external WebSearch this cycle still finds BTC holding ~$65k despite Brent near $97.66, so the price/macro divergence flagged at 23:27 persists unresolved, not worsening structurally.
- **Catalyst mapping degraded further**: 64.6% unmapped this cycle vs. 60.9% at 23:27 — the downward mapping-quality trend continues (see TODO-catalyst-mapping-coverage, new this cycle).
- **LA/USDT substring-collision reconfirmed** with a fresh example today (SpaceX/Tesla headlines matching "LA") — same defect family as the carried EUL mismap TODO, now with same-day evidence.
- **ARX/USDT and the short side unchanged**: still squeeze-capped, no clean crypto short on the board; SMH now surfaces as the cleanest short-planning idea for the coming US open (new framing this cycle, since stocks data is now same-day/fresh rather than the weekend-stale data used previously).
- **Unchanged**: scalp correctly structurally negative and thin (no fresh scalp ideas this cycle); EUL/USDT still the desk's lone fresh(-ish) B-tier idea, still above every entry zone, still uncaptured by the catalyst mapper for its (aging) Upbit listing.

## 5. Catalyst Coverage

- Total catalyst events today (`data/catalysts/2026-07-27/catalyst_events.jsonl`): **500**
- Mapped (has symbol): **177** (35.4%)
- Unmapped (no symbol): **323** (64.6%)
- Narrative baskets: **2** — `perps_dex_narrative` (HYPE/USDT primary, DYDX/GMX/ASTER related, <1h fresh, playbook `wait_pullback`), `delisting_thin_liquidity` (no primary, <24h fresh, playbook `avoid_low_liquidity`)
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (64.6% > 50% threshold)
- Top 3 unmapped headlines: "MEXC to Convert CXMTUSDT Pre-IPO Futures into Standard Futures #New_Listings"; "WEMIX reports contract breach tied to WEMIX$ stablecoin, attacker mints tokens and moves about $724,000"; "#Bithumb News OPEN API 1.0 Allowed IP Unregistered Key Bulk Blocking Information" — none of these are missed genuine trading catalysts for tonight's top candidates, consistent with the pattern noted in the prior review (unmapped items skew toward routine exchange/ops notices, not missed signal).
- By type: other_news 467, regulatory_sector_headline 11, legal_risk 7, partnership 5, buyback_burn 2, rumour_only 2, earnings_event 2, low_liquidity_event 1, exploit_hack 1, token_unlock 1, analyst_action 1.
- Top-importance items are mostly BTC-level regulatory (CLARITY Act coverage) and the STORJ Chapter 11 legal-risk basket — neither maps to a tradeable single-symbol crypto idea tonight.

## 6. Market Landscape

BTC: transition_up. ETH: uptrend. Altcoin breadth: 61.5% above EMA20/EMA50. Internal regime label: bullish trend (risk-on), recommended style "selective longs; prefer pullbacks on relative strength." Macro/geopolitical risk score: 100/100 (8 risk-off hits, 1 risk-on, 2 calendar/watch) — Iran/Israel conflict, Red Sea/Houthi shipping disruption, oil price spike (Brent ~$97.66 per external search, near a two-month high). External research this cycle (WebSearch, not independently chart-verified) finds BTC still holding near $65,000 and ETH near $1,874 testing resistance ~$1,950 despite the oil spike — spot ETF inflows cited as a stabilizing factor. This is a genuine **price/headline divergence**: the macro score says risk-off, the price structure says still-intact uptrend. Neither has resolved the other yet. Stocks: risk_off/short-biased regime label, but the US cash session is closed (pre-market) — not actionable until RTH confirmation after ~16:30 EEST.

### Market Mood / Risk Routing
- Crypto mood: **mixed** (bullish price structure vs. risk-off macro headline stream — genuine divergence, not chop)
- Stocks mood: **closed** (pre-market; risk_off/short bias once open, per the fresh 04:36 EEST intraday report)
- Dominant narrative: perps_dex_narrative (HYPE/USDT + DYDX/GMX/ASTER, <1h fresh) is the freshest; RS-momentum names (ESP, KAITO, LA, DIA) dominate the top-symbols list but lack catalyst backing
- Preferred side now: **longs** (RS-leader momentum, no catalyst confirmation required for the swing playbook's strongest cohort this week), with reduced size given the macro-price divergence
- Best long candidate: **DIA/USDT** (registered swing B-tier, score 72.4, waiting_for_entry; see §3A for exact trigger)
- Best short candidate: **SMH** (stocks, planning-only until RTH; no clean crypto short tonight — all thin/squeeze-capped)
- Best catalyst-backed candidate: **HYPE/USDT** (perps_dex_narrative, <1h fresh, not yet a concrete registered signal)
- What to avoid: **KAITO/USDT** (RSI ~77 + reported unlock risk + no volume confirmation — do not chase); also avoid all crypto shorts tonight (RE/DEXE/RIF/ARX/SYN all squeeze-capped against a bullish tape)
- What would change the view: a BTC 1h close back below local support (would resolve the macro/price divergence bearishly and justify de-risking the open longs); a volume rebuild (>0.5x) on KAITO or ESP (would re-open the momentum-long case there); RTH confirmation on SMH/AVGO/XLK after the US open (would activate the stocks short-planning idea)

## 7. Candidate Deep Dives

### 1. DIA/USDT (long, best long-watch)
- Has price already reacted to the catalyst? No verified catalyst exists; this is pure RS-momentum (+14-15% vs BTC across scalp/intraday/swing).
- Is the setup chasing? Moderately — price is above the registered swing entry zone (0.123-0.129) at the intraday report's snapshot (0.135); the swing zone itself is not yet extended.
- Retest/pullback structure? Yes — a defined pullback zone exists in the registered swing signal (0.123003-0.128747, invalidation 0.115983).
- Overextended (>2 ATR from EMA20)? Not flagged as such in the reports; OI up 101-242% supports the move as fresh positioning, not exhaustion.
- Would entry now be late? At current intraday price (~0.135) yes, relative to the swing zone; wait for the pullback.
- What level makes it actionable? 1h close inside 0.123003-0.128747 (swing) with volume ticking up.
- Aligned with market mood? Yes — longs preferred, RS-leader, no catalyst needed for the swing cohort.
- Long, short, or wait-for-trigger? Wait-for-trigger (already registered waiting_for_entry).
- Actionable now or after confirmation? After the pullback fills; already a live B-tier registered signal, so "actionable" in the sense the desk already treats it as such — just not yet triggered.
- What would invalidate it? 1h close beyond 0.115983 (registered invalidation).
- Chase risk? Moderate at current price; low at the registered pullback zone.
- Catalyst confirmation or contradiction? None — pure momentum/derivatives-confirmed.

### 2. KAITO/USDT (long, avoid candidate)
- Has price already reacted? Yes — up 16-27% over 24h depending on report snapshot, extended from the RSI~77 read on 2026-07-24 at $1.05 (now $1.18-1.23).
- Chasing? Yes.
- Retest structure? A pullback zone is registered (intraday: 1.162-1.176; swing: 1.1368-1.1550) but volume has not rebuilt (0.17-0.2x vs. 2.18x earlier in the week per the prior review's history).
- Overextended? RSI evidence (external, single-source, from 3 days prior) suggests compressed R:R even before this week's further extension.
- Would entry now be late? Yes, both at market and at the registered pullback zone given the lack of volume confirmation.
- Actionable now or after confirmation? Only after volume rebuilds meaningfully above ~0.5x — no such confirmation exists tonight.
- Invalidation? 1h close beyond 1.145 (intraday) / 1.1145 (swing).
- Chase risk? High.
- Catalyst confirmation or contradiction? A reported ~1.8% supply unlock (single-source, not independently re-verified via WebFetch) would be a mild dilution headwind if confirmed — treat as an open question, not a settled fact.

### 3. EUL/USDT (long, catalyst-adjacent but currently uncaptured)
- Has price already reacted? Yes — the Upbit-KRW-listing catalyst (confirmed genuine in prior reviews, still mismapped by the internal resolver, now ~28h old) likely already drove part of the 43-139% multi-day move; too aged to treat as a fresh catalyst trigger tonight.
- Chasing? Yes — price (2.268 on the carried swing report) sits above every defined entry zone (swing 2.107-2.218; intraday conditional 2.267-2.368).
- Retest structure? A pullback zone is defined but not yet reached.
- Actionable now or after confirmation? Only on a pullback into the defined zones with volume confirmation; the current OPEN_ACTIVE swing position (already filled) should simply be monitored for TP/SL, not added to.
- Invalidation? 1h close beyond 1.9699 (swing) / 2.0337 (intraday, registered).
- Catalyst confirmation or contradiction? Confirmed-but-aged and confirmed-but-mismapped — a genuine catalyst the internal system still cannot see (see TODO).

### 4. HYPE/USDT (catalyst-backed watch, not yet a concrete signal)
- Has price already reacted? Unclear — basket-level data only, no OHLCV/score in this review's data pull.
- Chasing? Unknown — no registered entry/invalidation levels exist yet.
- Actionable now or after confirmation? Not actionable — no proposed_signal has been registered for HYPE/USDT; this is purely a narrative-basket flag (perps_dex_narrative, <1h fresh, playbook `wait_pullback`).
- What would make it actionable? The desk registering a concrete scored signal with entry/invalidation/TP levels on a subsequent scan cycle.

### 5. SMH (short, planning-only, best short-watch for the coming US open)
- Has price already reacted? Unknown pre-market; raw score 85.2 (A-tier raw) reflects the last RTH close structure.
- Chasing? Cannot assess pre-market — no chase-risk read is meaningful until price action resumes.
- Actionable now or after confirmation? Not actionable now (market closed); actionable after RTH confirmation post ~16:30 EEST if the registered short zone (561.125-565.061) breaks with a confirming 1h close.
- Invalidation? 568.998 (registered).
- Legal/headline risk? None flagged (unlike UNH/TSLA/MSFT) — the only demotion reason is `market_closed_intraday_planning_only`.
- Catalyst confirmation or contradiction? None directly; semiconductor-sector weakness is the underlying thesis, no fresh single-symbol catalyst.

## 8. Best Candidates Ranked

1. **Long-watch: DIA/USDT** — trigger 1h close inside 0.123003-0.128747 with volume >0.3x; already registered swing B-tier waiting_for_entry, score 72.4 (highest in the active crypto book).
2. **Short-watch: SMH** — trigger RTH break of 561.125-565.061 after the ~16:30 EEST US open; highest raw score (85.2) with no legal-risk flag among stocks candidates.
3. **Catalyst-watch: HYPE/USDT** — trigger: wait for the desk to register a concrete signal off the perps_dex_narrative basket (<1h fresh); no tradeable levels exist yet.
4. **Avoid: KAITO/USDT** — RSI~77 + reported unlock risk + no volume confirmation; do not chase despite being a registered waiting_for_entry signal in two modes.
5. **Monitor-only (already open, do not add): BANK/USDT, EPIC/USDT (×2), EUL/USDT (swing), PENGU/USDT (swing), ORDI/USDT (swing)** — all OPEN_ACTIVE per the paper-monitor lifecycle; manage existing TP/SL, no new entries against these theses tonight.

## 9. Avoid / No Trade

This applies to the current decision window only — scanning, tracking, and the scheduler continue unchanged regardless.

- **KAITO/USDT** (both modes) — no volume confirmation, overbought RSI evidence, reported unlock risk; wait for a rebuild.
- **All crypto shorts tonight** (RE, DEXE, RIF, ARX, SYN, INJ) — every one is squeeze-capped (thin liquidity) fighting a bullish-trend regime; DEXE additionally shows extreme negative funding against the short.
- **Any stocks A/B entry before RTH confirmation** — market is closed; all 15 raw-A/B candidates are correctly demoted to C by policy.
- **UNH, TSLA, MSFT** (stocks) — active legal/headline-risk flags (DOJ probe, going-concern, class-action/securities-fraud respectively); manual review required if these ever clear the market-closed gate, never a clean actionable regardless of score.
- **EUL/USDT — do not add to the open position** at current extended price; the existing OPEN_ACTIVE swing entry should be monitored for TP/SL, not pyramided.

## 10. Main Risks

- Macro/geopolitical risk at 100/100 (Iran/Israel/Red-Sea/oil) with BTC/ETH price structure not yet reflecting it — a delayed catch-down remains possible and would hit all open long positions (BANK, EPIC×2, EUL, PENGU, ORDI) simultaneously (correlation-cluster risk).
- Fed decision scheduled 2026-07-28/29 (per external search) — a major macro catalyst landing within ~36-60h, outside this immediate window but worth pre-positioning risk awareness for.
- Catalyst mapping at 64.6% unmapped this cycle — genuine catalysts could be missed; treat the catalyst layer as context only, not a decision gate.
- Stale-active-signals / lifecycle-field inconsistencies persist (17 crypto rows past-expiry never reaching a terminal state on the raw CLI view; 1 stocks row with an unmapped status field on the authoritative lifecycle view) — readability risk for manual review, not a live-trading risk.
- KAITO/USDT unlock claim is single-source and not independently re-verified — if false, removes one risk factor; if true, adds sell-pressure to an already-registered waiting_for_entry signal in two modes.

## 11. Action Plan — next 4 hours

- Monitor the 6 OPEN_ACTIVE crypto positions (BANK-intraday, EPIC-intraday, EPIC-swing, EUL-swing, PENGU-swing, ORDI-swing) for TP/SL — no new entries against these theses.
- Watch DIA/USDT for a 1h close into 0.123003-0.128747 with volume pickup — the cleanest waiting_for_entry candidate.
- Do not chase KAITO/USDT, ESP/USDT, or EUL/USDT at current extended prices.
- Watch for the desk to register a concrete HYPE/USDT (or DYDX/GMX/ASTER) signal off the perps_dex_narrative basket on the next scan cycle.
- Re-check BTC/ETH structure against the macro risk-off backdrop through the Asia session into the 11:30 EEST Europe/pre-US review — the price/headline divergence is the single most important thing to resolve before the US open.
- No pre-market stocks action; wait for RTH confirmation on SMH/AVGO/XLK (clean, no legal flag) after ~16:30 EEST; continue to exclude UNH/TSLA/MSFT regardless of score.

## 12. Final Verdict per Mode

- **Scalp (crypto):** No trade. Structurally negative this week (PF 0.47, -4.8R); correctly quiet this cycle (no A/B ideas). Kill-switch context noted in the report banner.
- **Intraday (crypto):** No fresh trade. Existing OPEN_ACTIVE positions (BANK, EPIC) monitored only; DIA/KAITO/EUL waiting_for_entry, watch DIA for the pullback trigger, avoid KAITO.
- **Swing (crypto):** Hold/monitor. Strongest playbook this week (PF 4.34, +33.4R); 4 OPEN_ACTIVE positions (EPIC, EUL, PENGU, ORDI) to manage; KAITO/LTC/DIA waiting_for_entry.
- **Intraday (stocks):** No trade — market closed, planning-only. SMH/AVGO/XLK are the cleanest post-open short-planning candidates (no legal flag); UNH/TSLA/MSFT excluded regardless of score.
- **Swing/Invest (stocks):** No trade — framework deprecated per prior audits, data 25 days stale, not a fresh gap.

## 13. Sources

- [KAITO crypto Analysis: July 2026 Insights and Key Levels](https://en.cryptonomist.ch/2026/07/24/kaito-crypto-analysis-july2026/) — RSI~77, technical levels, WebFetch-verified 2026-07-27.
- [Kaito Price, KAITO to USD, Research, News & Fundraising | Messari](https://messari.io/project/kaito) — background context, not independently WebFetch-verified.
- [Bitcoin holds near $65,000 as the Iran conflict sends oil to a two-month high: Crypto Markets Today](https://www.coindesk.com/markets/2026/07/24/bitcoin-settles-near-usd65-000-as-oil-s-march-toward-usd100-fails-to-spook-the-market) — BTC/ETH price vs. oil/Iran divergence.
- [Crypto Prices Today: Bitcoin Holds Near $65,200 as ETF Inflows Offset US-Iran Tensions](https://www.analyticsinsight.net/price-analysis/crypto-prices-today-bitcoin-holds-near-65200-as-etf-inflows-offset-us-iran-tensions-2) — ETF-inflow stabilization narrative.
- Internal: `data/reports/scalp/2026-07-27_01-09_scalp_report.md`, `data/reports/intraday/2026-07-27_01-15_intraday_report.md`, `data/reports/swing/2026-07-26_14-52_swing_report.md`, `data/reports/stocks/intraday/2026-07-27_01-36_stocks_intraday_report.md`, `data/catalysts/2026-07-27/catalyst_cycle_01-20.md`, `reports/PAPER_MONITOR_STATUS_LATEST.md`.

## 14. Fix Requests / TODO

### TODO-catalyst-symbol-substring-collision (carried, new same-day evidence)
- **issue:** The catalyst/news symbol resolver has two failure modes: (a) false-positive substring collisions — short crypto tickers matching unrelated words in longer headlines; (b) false-negative mapping misses — genuine listing-announcement catalysts failing to populate `detected_symbols_json` for the actual token.
- **evidence:** Today's `news_items` 24h-freshness check for LA/USDT returned 2 rows, both unrelated (SpaceX HSBC-coverage story, Tesla Optimus story) — a fresh same-day example of failure mode (a). EUL/USDT's Upbit-KRW-listing rows (from 2026-07-26, ~28h old) remain mismapped to `["ETH","ETH/USDT"]` or `[]` despite explicit "Market Support for Euler(EUL)" titles — the same failure mode (b) reconfirmed for the 7th+ consecutive review cycle (11:44, 16:20, 18:39, 21:39, 23:27 prior day, 04:46 this run).
- **suggested manual fix:** unchanged from prior cycles — audit the symbol/catalyst resolver for (1) word-boundary-aware ticker matching, and (2) whether listing-announcement title patterns ("X Will List Y" / "Upbit to List Y" / "Market Support for Y") are parsed for the specifically-listed symbol, not just substrings appearing elsewhere in the title.
- **priority:** high (unchanged — recurring across 7+ cycles, actively distorts catalyst characterization on the desk's own watchlist candidates).
- **first observed:** 2026-07-26 11:44 EEST (EUL miss); re-confirmed every cycle since, including this run (LA false-positive is new evidence, same defect family).

### TODO-stale-active-signals (carried, unchanged)
- **issue:** `active-signals` (raw CLI) continues to list crypto signals with `expires_at` dates in the past while showing `triggered`/`tp1_hit`/`tp2_hit` status rather than a terminal closed state. This run: KAITO/USDT and LA/USDT scalp rows show `triggered` with `expires_at` 2026-07-27T03:16:41 — already ~1h23m in the past at run time (04:46) — plus 15 older past-expiry tp1/tp2_hit rows (Jul 17-22). Separately, the authoritative `PAPER_MONITOR_STATUS_LATEST.md` lifecycle view shows 1 `UNKNOWN_INCONSISTENT` row this cycle: XOM (stocks/intraday/B) with an unmapped status field `'tp2_hit'`.
- **evidence:** direct `active-signals --asset-class crypto` output this cycle; `PAPER_MONITOR_STATUS_LATEST.md` line 147 (`XOM long (stocks/intraday/B) — STATUS NEEDS REVIEW — unmapped status 'tp2_hit'`).
- **suggested manual fix:** unchanged — confirm whether `active-signals` should filter on `expires_at`, or add an explicit `past_expiry`/`entered_unresolved` flag; separately, extend the paper-monitor status-mapping table to recognize `'tp2_hit'` as a valid intermediate status for stocks signals (currently only unmapped for at least this one asset/mode/tier combination).
- **priority:** low (no functional/routing impact observed; readability issue for manual review only).
- **first observed:** carried context from multiple prior reviews; re-raised 2026-07-27 04:46 EEST with a new stocks-side example (XOM).

### TODO-catalyst-mapping-coverage (new — trend tracking)
- **issue:** Catalyst-event symbol-mapping coverage has been below the 50% weak-mapping threshold for at least the last 3 consecutive reviews and is trending worse: 60.1% unmapped → 60.9% unmapped (23:27 prior day) → 64.6% unmapped (this run).
- **evidence:** direct tally of `data/catalysts/2026-07-27/catalyst_events.jsonl` this cycle (500 total, 177 mapped, 323 unmapped = 64.6%); prior-review figures cited in `OPUS_ENRICHED_REVIEW_AUTO_2026-07-26_2327.md` §2 and §4.
- **suggested manual fix:** a human-driven session should sample the unmapped set specifically for any genuine missed single-symbol catalysts (not just the routine exchange/ops-notice items sampled in this and prior reviews) and assess whether the resolver's symbol dictionary needs expansion, separately from the substring-collision defect tracked above.
- **priority:** medium (no confirmed missed trade yet across sampled unmapped headlines, but the trend is worsening and warrants a dedicated audit rather than continued cycle-by-cycle spot-checking).
- **first observed:** trend noted 2026-07-26 (60.1%→60.9%); this run adds a third data point (64.6%) confirming the direction.

## Telegram

```
[AUTO-REVIEW crypto overnight 04:46 EEST]

Mood:
- Crypto: mixed (bullish price structure vs. macro risk-off headline stream, 100/100)
- Stocks: closed (pre-market; risk_off/short bias once open ~16:30 EEST)
- Prefer: longs (reduced size given macro/price divergence)

Status:
- Open actionable: 6 (BANK-intraday, EPIC-intraday, EPIC-swing, EUL-swing, PENGU-swing, ORDI-swing)
- Waiting for entry: 6 (EUL/DIA/KAITO-intraday, KAITO/LTC/DIA-swing)
- Review/Shadow: 55 (mostly stocks C-tier, market closed)
- Entered unresolved: 0 expired-after-entry (clean); 17 legacy-view past-expiry rows never reaching terminal state (readability TODO, not live)
- No-entry/stale/moved-away: 2 (LA-intraday, PENGU-scalp aged out)
- Needs review: 1 (XOM stocks unmapped status field, cosmetic)

Decisions:
- Long-watch:     DIA/USDT trigger 1h close 0.123003-0.128747, volume >0.3x
- Short-watch:    SMH trigger RTH break <561.125 post ~16:30 EEST open (no legal flag)
- Catalyst-watch: HYPE/USDT perps_dex_narrative basket <1h fresh, no concrete levels yet
- Avoid:          KAITO/USDT — RSI~77 + reported unlock risk + no volume confirmation

Risk:
- Macro risk 100/100 (Iran/oil/Red Sea) while BTC/ETH price hasn't broken down yet — genuine divergence, size fresh longs conservatively.

Catalyst coverage: mapped 177/500 (35.4%), baskets 2
                   weak this run — context only

File: OPUS_ENRICHED_REVIEW_LATEST.md
Advisory only. No auto-trade.
```
