# Opus Enriched Review — US open reaction review — Auto Cycle 18:30 EEST

## 1. Executive Summary

Slot: **US open reaction review** (~2h10m into the RTH session; US cash opened 16:30 EEST / 09:30 ET). **Advisory only — no auto-trade.** The internal-vs-external stocks regime contradiction flagged in the 16:11 pre-US review has **resolved cleanly to risk-on**: today's freshest stocks-intraday pipeline run (15:33 UTC / 18:33 EEST) now shows regime **risk_on**, VIX 16.23 (down from 15.67 stale-read), breadth 100% above EMA20/50, 3/4 indices in uptrend — matching the premarket futures signal from two cycles ago. Despite the clean regime, **zero A/B-tier stocks setups are actionable**: 9 raw-A and 5 raw-B candidates (AMZN, MSFT, PLTR, SMCI, AVGO, NVDA, JPM, XLK, XLF, QQQ, SMH, XLY, SPY, DIA) were all demoted to C by the SI-1..5 actionability gates (lunch-session confirmation, RVOL, sector confirmation, catalyst quality) — this is the gates doing their job in a session-transition window, not a data failure. Crypto remains no-A/B across scalp/intraday; the lone active crypto idea is a previously-triggered B-tier swing long, TUT/USDT. The Coldcard hardware-wallet exploit that has driven crypto's macro risk-off score all day is externally confirmed as real and still escalating (Fortune: ~$116M/1,816 BTC as of Aug 3; our internal feed shows $100-130M/1,596-2,055 BTC across 15 attackers — consistent, single-source variance is normal for a live incident). Crypto catalyst mapping continues to worsen for a fourth consecutive review (53.2%→57.2%→60.2%→**62.9%** unmapped). No untracked legacy alerts fired this cycle (crypto detector clean).

## 2. Data Used

- Crypto: `data/reports/scalp/2026-08-04_13-51_scalp_report.md` (mtime 16:51 EEST), `data/reports/intraday/2026-08-04_13-58_intraday_report.md` (mtime 16:58 EEST), `data/reports/swing/2026-08-04_14-56_swing_report.md` (mtime 17:56 EEST) — all fresh (<2h)
- Stocks: `data/reports/stocks/intraday/2026-08-04_15-33_stocks_intraday_report.md` (mtime 18:33 EEST, ~9min old) — fresh; stocks swing/invest reports last generated 2026-07-02 — stale/deprecated, excluded
- `data/processed/llm_analysis_packet.md` (17:56), `data/processed/llm_stocks_packet.md` (17:25)
- `data/catalysts/2026-08-04/catalyst_cycle_14-03.md`, `catalyst_events.jsonl` (3000 rows today, computed mapped/unmapped this run), `narrative_baskets.jsonl` (4 baskets)
- CLI: `active-signals --asset-class crypto` (26 rows), `active-signals --asset-class stocks` (50 rows), `signal-stats` (both asset classes), `detect_untracked_legacy_alerts --since 2026-08-04` (0 untracked)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-04_1611.md` (pre-US-open decision review)
- External: 3 WebSearch queries (Coldcard exploit total-stolen update, AWS/Iran Gulf strikes, Clarity Act pre-recess status) — see §13

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime 18:03 EEST (~39min old) — fresh, not deferred.
- Latest cycle summary: `cycle_08_16-42_summary.md` (18:03 EEST) — same cycle window as the crypto/stocks reports used here.
- Crypto scalp/intraday/swing reports: 16:51/16:58/17:56 EEST — all fresh (<2h).
- Stocks intraday report: 18:33 EEST, ~9min old — fresh, mid-RTH-session.
- Stocks swing/invest: last generated 2026-07-02 — stale (>14h), excluded (known deprecated frameworks, per standing memory).
- No monitor/paper-status file was read this cycle (not in the allowed read list).
- **Data-quality note (resolved):** the nan-breadth/risk_off-label contradiction flagged in the 16:11 pre-US review is gone — this cycle's stocks report shows clean breadth (100%) and a coherent risk_on label. The underlying RS-vs-sector nan issue for the *pre-US overlay* specifically was not re-checked this cycle (that overlay only runs at the 16:20 slot) — see §14 carried TODO.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-08-04 18:30 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["pre-US overlay RS-vs-sector nan issue not re-checked this slot (only runs at 16:20)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log 18:03 EEST fresh (39min)", "all crypto reports <2h old", "stocks intraday report 9min old", "stocks swing/invest stale since 2026-07-02, deprecated"] },
    { "agent": "market_regime", "verdict": "ok", "confidence": 0.7,
      "reason_codes": ["risk_on", "mixed", "longs_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["stocks regime now cleanly risk_on: VIX 16.23, breadth 100% EMA20/50, 3/4 indices uptrend — resolves the 16:11 review's internal-vs-external contradiction", "crypto: BTC transition_up, ETH range, altcoin breadth 65-72.5% above EMA20 depending on mode, but macro risk score ~99-100/100 from Coldcard hack + geopolitical overlay — mixed, not clean risk-on"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "catalyst_confirmed", "no_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["62.9% unmapped catalyst events today (1888/3000) — worse than 16:11's 60.2%, fourth consecutive worsening review", "4 narrative baskets: perps_dex_narrative(HYPE), ai_narrative(NEAR/RENDER/TAO/FET), binance_ecosystem_teaser(BNB), momentum_breakout(BTW/SNXXB/KORUB)", "Coldcard hack externally confirmed ongoing/escalating (Fortune: $116M/1,816 BTC as of Aug 3)", "Clarity Act externally confirmed likely to miss its Aug 7 pre-recess deadline — relevant to COIN/BTC regulatory catalyst framing"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "data_unavailable"],
      "data_missing": ["OI 24h n/a for most intraday movers (SNDKB, KORUB, SNXXB, MUB, SKHYB)", "no derivatives coverage for stocks side"],
      "suggested_effect": "advisory_only",
      "facts_used": ["TUT/USDT swing: funding +5e-05, OI +18.55%, crowding normal — clean continuation positioning, not squeeze-flagged", "BTW/USDT: funding +0.0006, OI +14.09%, crowding elevated long — squeeze-risk on further chase", "COTI/USDT: negative funding across bybit/mexc, crowding elevated/unknown — short-covering bounce, weaker continuation quality"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["entry_late", "chase_risk", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TUT/USDT swing: preferred entry is the pullback zone 0.0230-0.0235; current price 0.0237, essentially inside the zone — not badly extended", "all 14 raw-A/B stocks candidates demoted to C by lunch-session/RVOL/sector/catalyst gates — none have a clean fresh entry structure at this point in the session", "KAITO/USDT still lacks a confirmed failed-bounce structure, same as 16:11"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["waiting_for_entry", "entered_unresolved", "needs_review", "no_entry"],
      "data_missing": ["closure/expiry semantics for weeks-old tp1/tp2_hit rows still unverifiable from this view (carried TODO)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 26 active — 2 waiting_for_entry, 8 entered-unresolved (7 triggered + 1 tp1_hit with future expiry, XRP), 16 needs-review (tp1/tp2_hit with expiry already in the past)", "stocks: 50 active — 4 waiting_for_entry, 1 entered-unresolved (AMAT), 45 needs-review (legacy, expiry in the past)", "0 untracked legacy crypto alerts this cycle (detector clean, unlike 16:11's 2 TUT/USDT instances)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["headline_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Coldcard hack externally confirmed real and ongoing ($100-130M internal / ~$116M external, both escalating) — root cause is a March 2021 firmware RNG flaw, not fixed by a simple patch", "AWS/Iran Gulf strikes externally confirmed as a real, recurring pattern (March/April/July 2026 strikes on AWS UAE/Bahrain facilities) — legitimate ongoing risk factor for AMZN, not a stale/fabricated headline", "AMD/CAT/SMCI report earnings today — avoid chasing into the print (already past for AMD/CAT/SMCI as of 18:30, but still a fresh-reaction risk)", "no new indictment/SEC/DOJ/class-action hits found for today's top stocks candidates (AMZN, COIN) in external search"] },
    { "agent": "playbook_performance", "verdict": "bad", "confidence": 0.7,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto scalp week: PF 0.167, avgR -0.192, 0W-3L — structurally negative, unchanged from 16:11", "crypto swing week: PF 0.97, avgR -0.009, totalR -0.20 — flat/slightly negative", "crypto intraday week: PF 3.34, avgR 0.86, totalR +16.4 — strongest crypto mode by far", "stocks C-tier week: PF 0.59, winrate 4% (n=214, reliable) — weak", "stocks shorts week: PF 0.14, 1W-10L (n=91-92) — structurally weak, avoid leaning on stocks shorts"] },
    { "agent": "head_trader", "verdict": "watch_only", "confidence": 0.6,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["synthesis of all agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "TUT/USDT", "trigger": "already triggered/active (swing B-tier, entry 0.02297-0.023475); watch for continuation toward TP1 0.0248 with volume confirmation, invalidate below 0.02235", "reason": "only real active B-tier crypto long; RS-leader (+15.4% vs BTC), OI+18.6% confirms fresh positioning, funding neutral — cleanest structure on the desk right now" },
    "best_short_candidate":    { "symbol": "KAITO/USDT", "trigger": "confirmed failed-bounce structure (crypto_failed_bounce_short playbook, 14d WR40%/PF2.0) plus independent derivatives confirmation before entry", "reason": "persistent relative weakness (-8.3% to -10.5% 24h depending on report) unchanged since 16:11 — genuine but still unconfirmed structure, do not short on RS score alone" },
    "best_catalyst_candidate": { "symbol": "BTC/USDT", "trigger": "a formal Coinkite/Galaxy resolution statement, or 24-48h with no new theft wave/attacker; separately watch Aug 7 Clarity Act Senate deadline for a regulatory catalyst", "reason": "externally confirmed, still-escalating self-custody exploit ($100-130M range across both internal and external sources) remains the dominant crypto macro-risk driver; Clarity Act deadline (external: likely to miss Aug 7) is a fresh binary catalyst risk for the whole sector this week" },
    "avoid_candidate":         { "symbol": "stocks intraday shorts (all names)", "reason": "PF 0.14, 1W-10L over 30d — structurally negative edge; today's only C-tier short (COIN, score 63.76) also carries a two-sided regulatory catalyst (Clarity Act) that could resolve either direction, adding event risk on top of an already-weak playbook" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | ok | 0.70 | risk_on, mixed, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, fresh_catalyst, catalyst_confirmed, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | entry_late, chase_risk, clean_retest | advisory_only |
| execution_lifecycle | caution | 0.60 | waiting_for_entry, entered_unresolved, needs_review, no_entry | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, reduce_risk | advisory_only |
| playbook_performance | bad | 0.70 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | watch_only | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (16:11 EEST — pre-US-open decision review)

- **Stocks regime contradiction resolved — cleanly risk-on**: the 16:11 review's internal risk_off/nan-breadth label vs external risk-on premarket data has resolved in favor of risk-on. This cycle's own pipeline shows VIX 16.23 (down), breadth 100% (up from 0%), 3/4 indices uptrend — no longer a "trust which source" problem.
- **Stocks A/B→C demotions are now gate-driven, not data-broken**: 14 raw-A/B candidates (AMZN, MSFT, PLTR, SMCI, AVGO, NVDA, JPM, XLK, XLF, QQQ, SMH, XLY, SPY, DIA) all demoted to C this cycle by SI-1..5 session/liquidity/sector/catalyst gates — a different failure mode than the earlier nan-breadth issue, and one the gates are designed to catch (early-session confirmation still pending).
- **Untracked legacy alerts — cleared**: 0 this cycle vs 2 TUT/USDT instances at 16:11. Same underlying signal-reuse bug (TODO-3) is not fixed, just didn't fire this window.
- **Coldcard exploit — externally corroborated, consistent scale**: external Fortune figure (~$116M/1,816 BTC as of Aug 3) sits inside the internal $100-130M/1,596-2,055 BTC range reported at 16:11 — no material new escalation since the last review, but not resolved either.
- **New catalyst this cycle — Clarity Act deadline**: internal catalyst feed surfaced Coinbase CEO comments + Yahoo Finance coverage on the Aug 7 Senate deadline (importance 0.80); external search confirms the bill is likely to miss that window per Majority Leader Thune — a fresh binary regulatory catalyst for COIN/BTC not present in the 16:11 review.
- **Catalyst mapping — worse again**: 62.9% unmapped this cycle vs 60.2% at 16:11 (53.2%→57.2%→60.2%→62.9%, fourth consecutive worsening review).
- **HOME/USDT** no longer appears as a top mover in this cycle's intraday/swing "strongest symbols" (was +46-53% 24h at 16:11); still an open triggered B-tier swing position from a prior cycle, unchanged status.
- **TUT/USDT** now the desk's only active B-tier setup in crypto swing (score 67.8) — was watchlist-only C-tier scoring lower at 16:11's carry-forward swing report; this is a genuine promotion this cycle, not a stale carry-forward.

## 5. Catalyst Coverage

- Total catalyst_events today: **3000**; mapped (non-null symbol): **1112** (37.1%); unmapped: **1888** (62.9%).
- Narrative baskets: **4** (perps_dex_narrative/HYPE, ai_narrative/NEAR+RENDER+TAO+FET, binance_ecosystem_teaser/BNB, momentum_breakout/BTW+SNXXB+KORUB).
- **Catalyst mapping weak this run (62.9% unmapped) — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines: "ARC Group Securities Acquisition I Announces Pricing of $105,000,000 Initial Public Offering"; "Voters prefer Democrats over Republicans on economy for first time in a decade, Reuters/Ipsos poll finds"; "Southern Company announces upsize and pricing of $725 million in aggregate principal amount of Series 2026A/B Convertible Senior Notes" — general corporate-finance/political noise, not symbol-specific misses.

## 6. Market Landscape

- **Crypto**: BTC trend transition_up, ETH range, altcoin breadth 65-72.5% above EMA20 depending on report mode — a mildly constructive tape sitting under a persistently heavy macro risk-off overlay (~99-100/100) driven by the still-unresolved Coldcard exploit and continued Iran/Strait-of-Hormuz geopolitical tension. Top RS movers (SKYAI, KORUB, HOME, TUT, COTI, SNDKB, BTW, SOXLB) remain small/mid-cap momentum names, several thin-volume or already extended.
- **Stocks**: US cash session ~2h10m in. Regime is now cleanly **risk_on** (VIX 16.23, breadth 100%, SPY/IWM/DIA uptrend, QQQ range). Energy (XLE) is the strongest sector (+6.85% 20d, RS +4.21% vs SPY); utilities/semis/healthcare weakest. Despite the constructive regime, every raw-A/B candidate this cycle failed at least one of the session-timing (lunch-window confirmation), liquidity (RVOL), sector-confirmation, or catalyst-quality gates — a normal outcome for this point in the session, not a data problem. AMD/CAT/SMCI reported earnings today; LLY/UBER report tomorrow.

### Market Mood / Risk Routing

- Crypto mood: **mixed, cautious risk-off tilt** (constructive trend/breadth numbers undercut by a still-unresolved, externally-confirmed exploit and heavy geopolitical overlay)
- Stocks mood: **risk-on, confirmed** (VIX down, breadth 100%, 3/4 indices trending up — the 16:11 review's internal-vs-external contradiction is resolved)
- Dominant narrative: an externally-corroborated, ongoing Bitcoin self-custody exploit (Coldcard) competing against a clean US equities risk-on tape and a fresh Aug 7 Clarity Act deadline risk for crypto-adjacent names (COIN, BTC)
- Preferred side now: **longs** on stocks (regime-aligned, but wait for gates to clear — none actionable yet this cycle) / **wait-for-trigger** on crypto (constructive trend, but macro overlay keeps aggression capped)
- Best long candidate: TUT/USDT (crypto, active B-tier swing, already triggered) / AMZN (stocks, best raw score 94.96 but demoted to C — watch for gates to clear later in the session)
- Best short candidate: KAITO/USDT — still lacks a confirmed failed-bounce structure
- Best catalyst-backed candidate: BTC/USDT — Coldcard exploit resolution watch + Aug 7 Clarity Act deadline
- What to avoid: stocks shorts generally (PF 0.14, 1W-10L/30d); crypto scalp mode (structurally negative); chasing any of the 14 gate-demoted stocks names before their specific gate clears
- What would change the view: a Coinkite/Galaxy resolution statement or clean 24-48h with no new Coldcard attacker; any of the 14 demoted stocks candidates clearing its specific gate (lunch-session confirmation, RVOL, sector, or catalyst) later in the session; a concrete Clarity Act floor-vote outcome

## 7. Candidate Deep Dives

### TUT/USDT — long (best crypto candidate, active B-tier swing)
- Has price already reacted? Yes — already triggered, currently trading essentially inside the preferred entry zone (0.0237 vs 0.0230-0.0235 pullback zone).
- Chasing? No — not extended relative to its own entry plan; 24h +15.6%, 7d +71.9% (most of the move is older, not a fresh vertical spike today).
- Retest/pullback structure? Yes — this is the retest entry itself.
- Overextended (>2 ATR from EMA20)? No flag raised by the desk's own gate.
- Aligned with mood? Yes — RS-leader long in a mildly constructive (if macro-capped) crypto tape.
- Long/short/wait? Long, already active — not a new entry decision, a monitoring one.
- Actionable now or after confirmation? Already active; monitor for TP1 (0.0248) with volume, or invalidation below 0.02235 (1h close).
- Chase-risk? Low at current price.
- Catalyst confirmation/contradiction? No fresh verified catalyst — pure RS/momentum thesis (`crypto_swing_narrative_rs_momentum` playbook, 14d WR 72%/PF 5.80 on this mode's actionable cohort).

### KAITO/USDT — short-watch (best crypto short candidate, unconfirmed)
- Has price reacted to weakness? Yes — persistent underperformance, -8.3% to -10.5% 24h depending on report, RS/BTC -8.5% to -11.2%.
- Chasing? Would be if entered now without structure — the move may already be late relative to EMA20/ATR (flagged in the intraday report's counter-thesis).
- Retest/pullback structure? Not yet confirmed — desk explicitly notes "not active while score is below threshold."
- Aligned with mood? Only partially — crypto mood is mixed/cautious, not a clean risk-off short environment.
- Long/short/wait? Wait-for-trigger short.
- Actionable level: confirmed failed-bounce structure (crypto_failed_bounce_short playbook, 14d WR 40%/PF 2.00) plus independent derivatives confirmation before entry.
- Catalyst: none — pure relative-weakness/RS thesis, no fresh verified catalyst.
- Note: an existing open B-tier intraday long on KAITO (`sig_c48e5a1bfac269cb`, tp2_hit, entered ~Jul 21) already banked wins before this week's weakness emerged — no live conflict with a potential future short.

### BTC/USDT — catalyst-watch (macro risk driver + fresh regulatory catalyst)
- Has price reacted to the catalyst? Partially — BTC continues recovering toward $63-64k even as the Coldcard theft total holds in the $100-130M range, suggesting the market treats this as a protocol/self-custody-specific risk rather than systemic.
- Chasing/retest/overextended? N/A — risk-context watch, not a directional entry.
- Actionable level: a formal Coinkite/Galaxy resolution/containment statement, or a clean 24-48h window with no new attacker/theft wave; separately, the Aug 7 Senate floor-vote deadline for the Clarity Act (externally confirmed likely to be missed, per Majority Leader Thune) is a fresh binary catalyst this week.
- Aligned with mood? Yes — primary driver of today's crypto macro risk-off score.
- Catalyst confirmation: Coldcard exploit **externally confirmed and consistent** with internal figures (Fortune ~$116M/1,816 BTC as of Aug 3 vs internal $100-130M/1,596-2,055 BTC) — root cause is a March 2021 firmware RNG flaw affecting Coldcard Mk3 4.0.1-4.1.9, not a one-time incident. Clarity Act status **externally confirmed**: absent from this week's Senate schedule as of Aug 3, deadline slippage likely.

### AMZN — stocks long-watch (best raw score, gate-demoted, real geopolitical risk flag)
- Has price reacted? Raw score 94.96 (A-tier), highest of today's stocks candidates — but demoted to C by `sector_confirmation_weak_or_unknown`, `lunch_requires_strong_confirmation`, `liquidity_rvol_below_min`, `catalyst_none_and_not_exceptional_technical`.
- Chasing/retest? Cannot assess cleanly — RVOL gate specifically flags insufficient volume confirmation at this point in the session.
- Aligned with mood? Yes — stocks regime is risk_on, AMZN is a regime-aligned long candidate on raw technicals.
- Actionable now or after confirmation? Not yet — needs its specific gates (sector confirmation, RVOL, post-lunch session confirmation) to clear.
- Legal/headline risk check: production feed flags `AMZN [geopolitical_risk]: AI data centers become war targets as Iran strikes AWS facilities in the Gulf` — **externally verified as a real, recurring pattern** (Iranian strikes on AWS UAE/Bahrain data centers in March, April, and July 2026, most recently reported by CNBC/TheConversation/RestOfWorld), not a stale or fabricated headline. This is a genuine ongoing operational-risk overhang on AMZN's cloud infrastructure, though not an indictment/SEC/legal-risk-tier event that would force an AVOID verdict — it's a risk_warning, not a block.
- Verdict: watchlist, not yet actionable; monitor for gate-clearing later in the session, with the AWS/Iran risk as a standing headwind to size around.

### COIN — stocks/crypto-crossover avoid-candidate (weak short edge + two-sided catalyst)
- C-tier only, score 63.76, short direction.
- Catalyst: Coinbase CEO Brian Armstrong commented today that America "needs" the Clarity Act ("economic security is national security") — importance 0.80 in the catalyst feed. Externally confirmed the bill is genuinely at risk of missing its Aug 7 pre-recess deadline.
- Chasing/retest? N/A — not an actionable tier regardless.
- Aligned with mood? Ambiguous — a missed Clarity Act deadline could read bearish (regulatory uncertainty extends) or the "at least get Clarity started" framing from Senate leadership could read as a modest positive; this is a genuine two-sided catalyst, not a clean short thesis.
- Actionable level: N/A this cycle — stocks shorts as a cohort carry a structurally weak playbook (PF 0.14, 1W-10L/30d); layering a two-sided regulatory catalyst on top of an already-weak short edge is a reason to avoid, not trade.

## 8. Best Candidates Ranked

1. **Long (crypto, active): TUT/USDT** — already triggered; monitor for TP1 0.0248 with volume, invalidate below 0.02235.
2. **Long-watch (stocks, gate-pending): AMZN** — trigger: sector confirmation + RVOL pickup + post-lunch session confirmation; monitor the AWS/Iran geopolitical risk as an ongoing headwind, not a hard block.
3. **Short-watch (crypto): KAITO/USDT** — trigger: confirmed failed-bounce structure + independent derivatives confirmation; do not short on RS-weakness score alone.
4. **Catalyst-watch (crypto): BTC/USDT** — trigger: Coldcard resolution statement or clean 24-48h window; separately watch the Aug 7 Clarity Act Senate deadline.
5. **Open-position watch (no new entries)**: 26 crypto positions (2 waiting, 8 entered-unresolved, 16 needs-review/legacy) and 50 stocks positions (4 waiting, 1 entered-unresolved, 45 needs-review/legacy) — monitor invalidation levels only.
6. **Avoid: COIN short and stocks shorts generally (PF 0.14, 1W-10L/30d); crypto scalp mode (structurally negative, 0W-3L this week).**

No A-tier setup cleared the desk threshold in any crypto mode or stocks intraday this cycle.

## 9. Avoid / No Trade (this decision window only)

- **Stocks shorts generally** — PF 0.14, 1W-10L over 30d, structurally weak edge.
- **COIN short specifically** — additionally carries a two-sided Clarity Act catalyst this week; avoid stacking event risk on an already-weak playbook.
- **Crypto scalp mode** — structurally negative this week (PF 0.167, 0W-3L).
- **The 14 gate-demoted stocks A/B candidates at current session point** — AMZN, MSFT, PLTR, SMCI, AVGO, NVDA, JPM, XLK, XLF, QQQ, SMH, XLY, SPY, DIA — each blocked by a specific gate (lunch-session confirmation / RVOL / sector confirmation / catalyst quality); not a blanket "stocks are bad" call, just not yet confirmed.
- This is a decision-window verdict only — **not** a recommendation to pause scanning, tracking, or the scheduler, all of which continue normally.

## 10. Main Risks

- **Coldcard exploit remains unresolved** — externally confirmed ongoing at $100-130M/1,596-2,055 BTC scale (internal) vs ~$116M/1,816 BTC (external, Fortune); no fresh escalation since 16:11, but no resolution statement found either — treat as the standing crypto macro-risk driver.
- **AWS/Iran Gulf strikes are a real, recurring pattern, not a one-off headline** — externally confirmed strikes on AWS UAE/Bahrain facilities in March, April, and July 2026; a genuine ongoing operational-risk overhang for AMZN specifically and cloud/AI infrastructure names generally.
- **Clarity Act deadline risk (new this cycle)** — externally confirmed the bill is likely to miss its Aug 7 pre-recess Senate deadline; a binary event risk for COIN/BTC/crypto-adjacent names this week.
- **Catalyst mapping weak and worsening for a fourth consecutive review** — 62.9% unmapped today (60.2% at 16:11, 57.2% at 11:39, 53.2% at 04:45); treat the catalyst layer as context only, not a decision input.
- **Stocks short-side edge structurally weak** — PF 0.14, 1W-10L (n≈91-92) over 30d; avoid leaning on short signals without independent confirmation.
- **Legacy open-position volume** — 26 crypto + 50 stocks "active" signals include dozens (16 crypto, 45 stocks) with `expires_at` weeks in the past still showing tp1/tp2_hit/triggered status; lifecycle closure semantics remain ambiguous (standing TODO, unresolved since at least the 11:39 review).

## 11. Action Plan — next 4 hours

- Monitor TUT/USDT for TP1 (0.0248) with volume confirmation or invalidation below 0.02235; no action needed unless one of those levels prints.
- Watch AMZN and the other 13 gate-demoted stocks candidates for their specific gates to clear later in the session (post-lunch confirmation, RVOL pickup, sector confirmation) — do not treat the risk_on regime alone as sufficient to trade any of them.
- Watch KAITO/USDT for a confirmed failed-bounce structure before treating it as a clean short.
- Watch for a Coinkite/Galaxy Coldcard resolution statement or a new attacker/wave; watch for any Aug 7 Clarity Act floor-vote development.
- No new crypto scalp entries this window; avoid initiating new stocks shorts given the weak 30d short-side edge.
- Continue scanning, tracking, and monitor processes in all cases — no pause recommended for any mode or asset class.

## 12. Final Verdict per Mode

- **Crypto scalp:** No trade. Structurally negative this week (PF 0.167, 0W-3L).
- **Crypto intraday:** Watch-only. No B-tier setups cleared this cycle; strongest-performing mode by week stats (PF 3.34) but nothing actionable right now.
- **Crypto swing:** Monitor active TUT/USDT (only live B-tier long); existing open positions (HFT, HOME, EPIC, AEVO, COTI, XRP short) continue to be monitored; no new entries this window.
- **Stocks intraday:** Regime confirmed risk_on but zero A/B actionable — all 14 raw candidates gate-demoted to C. AMZN is the strongest watch-item pending gate clearance; avoid stocks shorts (weak 30d edge) including COIN.
- **Stocks swing/invest:** Stale (>1 month, deprecated frameworks) — excluded from this cycle's verdict, unchanged status.

## 13. Sources

- [Bitcoin owners rocked by $116 million hack: What we know about the Coldcard exploit](https://fortune.com/2026/08/03/bitcoin-owners-116-million-hack-coldcard-coinkite-exploit/) — Fortune, 2026-08-03.
- [Bitcoin cold-wallet attack spreads to 4,500 addresses as losses near $89 million](https://www.coindesk.com/tech/2026/08/02/bitcoin-cold-wallet-attack-spreads-to-4-500-addresses-as-losses-near-usd89-million) — CoinDesk, 2026-08-02.
- [Coldcard Hardware Wallet Flaw Linked to $70 Million Bitcoin Theft in 41 Minutes](https://thehackernews.com/2026/08/coldcard-hardware-wallet-flaw-linked-to.html) — The Hacker News, 2026-08.
- [Iran says it attacked Amazon infrastructure in Bahrain](https://www.cnbc.com/2026/07/21/iran-war-update-five-things-to-know-after-resumption-of-hostilities.html) — CNBC, 2026-07-21.
- [Why Iran targeted Amazon data centers and what that does – and doesn't – change about warfare](https://theconversation.com/why-iran-targeted-amazon-data-centers-and-what-that-does-and-doesnt-change-about-warfare-278642) — The Conversation, 2026.
- [Iranian drone strikes at Amazon sites raise alarms over protecting data centers](https://restofworld.org/2026/iran-amazon-data-center-strikes/) — Rest of World, 2026.
- [Clarity Act expected to miss its window before Congress' summer break, leadership says](https://www.coindesk.com/policy/2026/07/23/clarity-act-expected-to-miss-its-window-before-congress-summer-break-leadership-says) — CoinDesk, 2026-07-23.
- [CLARITY Act Countdown: Senate Has Days to Save Landmark Crypto Bill Before Recess](https://bitcoinfoundation.org/news/regulation/clarity-act-countdown-senate-has-days-to-save-landmark-crypto-bill-before-recess/) — Bitcoin Foundation, 2026-08.
- [Crypto bill faces make-or-break moment ahead of August recess](https://thehill.com/policy/technology/5963428-crypto-bill-clarity-act-make-or-break-congress/) — The Hill, 2026.
- Internal: `data/reports/scalp/2026-08-04_13-51_scalp_report.md`, `data/reports/intraday/2026-08-04_13-58_intraday_report.md`, `data/reports/swing/2026-08-04_14-56_swing_report.md`, `data/reports/stocks/intraday/2026-08-04_15-33_stocks_intraday_report.md`, `data/catalysts/2026-08-04/catalyst_cycle_14-03.md`, `catalyst_events.jsonl`, `narrative_baskets.jsonl`, `data/processed/llm_analysis_packet.md`, `data/processed/llm_stocks_packet.md`, `OPUS_ENRICHED_REVIEW_AUTO_2026-08-04_1611.md`.

## 14. Fix Requests / TODO

### TODO-catalyst-mapping-persistently-weak (priority: low, recurring, worsening)
- **issue:** Catalyst→symbol mapping has been over the 50% unmapped threshold for at least four consecutive reviews and is trending worse: 53.2% (04:45) → 57.2% (11:39) → 60.2% (16:11) → **62.9%** (this run).
- **evidence:** `data/catalysts/2026-08-04/catalyst_events.jsonl` (3000 rows today, 1888 null-symbol, computed this run).
- **suggested manual fix:** revisit the symbol resolver in the catalyst layer per the earlier-raised TODO; the trend (consistently getting worse, not stabilizing) suggests this isn't just a stable share of un-mappable macro noise.
- **priority:** low
- **first observed:** 2026-08-04 04:45 EEST (carried forward, still unresolved, still worsening).

### TODO-legacy-open-position-volume (priority: medium, carried forward, unresolved)
- **issue:** `active-signals` still returns dozens of rows (16/26 crypto, 45/50 stocks) with `expires_at` dates in the past while status reads `tp1_hit`/`tp2_hit`/`triggered` — unclear whether these are correctly "not yet finally closed" by design or a stuck closure job.
- **evidence:** e.g. `sig_b16bb9e54598333a` (NEAR scalp, tp1_hit, expires_at 2026-07-17T15:56:12) still present in this run's `active-signals --asset-class crypto` output, three weeks past expiry.
- **suggested manual fix:** unchanged from prior reviews — a human-driven session should confirm the intended lifecycle semantics and, if needed, add clearer status labeling in the CLI output (e.g. distinguish "still open, tracking toward further TPs" from "expired, needs manual close").
- **priority:** medium
- **first observed:** 2026-08-04 11:39 EEST (carried forward, still unresolved).

### TODO-untracked-alert-bug-not-refired-but-unfixed (priority: high, recurring root cause, dormant this cycle)
- **issue:** The watchlist-alert signal-reuse bug (re-fire reuses a stale/closed `signal_id` instead of minting a fresh `proposed_signal`) did not produce any untracked alerts this cycle (0, vs 2 TUT/USDT instances at 16:11) — but the underlying root cause is unfixed, so recurrence is expected whenever the same watchlist symbol re-fires.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-04` returned 0 this run; prior confirmed instances on ALLO/USDT, BANK/USDT (2026-07-17) and TUT/USDT (2026-08-04 16:11).
- **suggested manual fix:** as already raised (TODO-3, raised to high priority 2026-07-17): fix the watchlist-alert path so a re-fire mints a fresh `proposed_signal` instead of reusing a stale/closed `signal_id`.
- **priority:** high
- **first observed root cause:** 2026-07-17; **last confirmed instance:** 2026-08-04 16:11 EEST (TUT/USDT); **this cycle:** dormant, not fixed.

### TODO-stocks-preus-overlay-rs-nan-not-rechecked (priority: medium, carried forward, needs re-verification)
- **issue:** The 16:11 pre-US review found the stocks pre-US overlay's RS-vs-sector calculations returning nan for every candidate, blocking any SUPPORT verdict. That overlay only runs at the 16:20 pre-US slot, so this cycle's regular intraday report was not checked for the same nan pattern in its own Sector Rotation table — this cycle's report (§2) shows populated RS values (e.g. energy +4.21%, technology +0.88%), suggesting the nan issue may be specific to the pre-US overlay's calculation path rather than the underlying data, but this has not been confirmed.
- **evidence:** `data/reports/stocks/intraday/2026-08-04_15-33_stocks_intraday_report.md` §2 Sector Rotation shows real RS values this cycle (contrast with the 16:11 review's nan finding for the same-day pre-US overlay).
- **suggested manual fix:** confirm whether the nan issue is isolated to the `stocks-preus-candidates` overlay's own RS calculation path (separate from the main intraday pipeline) — if so, the fix is scoped narrower than previously assumed.
- **priority:** medium
- **first observed:** 2026-08-04 11:39 EEST (carried forward); this cycle narrows the scope of the likely root cause.

### TODO-stocks-gate-demotion-visibility (priority: low, observation)
- **issue:** 14 of 14 raw-A/B stocks candidates this cycle were demoted to C by SI-1..5 gates, all in a similar cluster (`lunch_requires_strong_confirmation`, `liquidity_rvol_below_min`, `sector_confirmation_weak_or_unknown`, `catalyst_none_and_not_exceptional_technical`). This is very likely correct/intended gate behavior for this point in the session (lunch-adjacent, RVOL still building) rather than a bug, but the 100% demotion rate on a clean risk_on day is worth a human sanity-check to confirm the gate thresholds aren't overly conservative for the mid-session window specifically.
- **evidence:** `data/reports/stocks/intraday/2026-08-04_15-33_stocks_intraday_report.md` §10 — "actionable A/B (intraday) after gates: 0 · raw-A/B demoted to C by SI-1..5 gates: 12" (14 in §5/§7 table including QQQ/SMH not double-counted in §10's 12).
- **suggested manual fix:** no fix needed unless a human review confirms the gates are miscalibrated; flagged for awareness only, not a defect.
- **priority:** low
- **first observed:** 2026-08-04 18:30 EEST (this run).
