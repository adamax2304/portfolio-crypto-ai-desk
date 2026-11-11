# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:39 EEST

## 1. Executive Summary

Slot: **11:30 Europe / pre-US context** (fired at 11:39 EEST due to normal dispatch jitter). **Advisory only — no auto-trade.** Crypto regime is technically range/chop but macro overlay is risk-off (100/100), driven by the ongoing Coldcard hardware-wallet exploit (externally confirmed ~$89–116M stolen since Jul 30, still unresolved) and Iran/Strait-of-Hormuz tension. No fresh A/B-tier crypto idea cleared this cycle's trade-idea agent — everything is C-tier watchlist or rejected. 23 crypto B-tier positions remain open (triggered/tp1/tp2), none waiting-for-entry. Stocks: US cash session not yet open (opens 13:30 EEST); regime flagged risk_off/short-bias by the desk but VIX is calm (15.99) and breadth reads look data-quality-suspect (nan values). No current/compatible open stocks A/B; five near-A/B candidates (CRM, MA, BAC, MSFT, NOW) were demoted only for "market closed" — build the watchlist from these, confirm at the open. MSFT carries an active legal/headline flag (class_action, securities_fraud) — do not treat as a clean long even at the open. Catalyst mapping is weak this run (57.2% unmapped) — use catalyst layer as context only.

## 2. Data Used

- Crypto: `data/reports/scalp/2026-08-04_08-22_scalp_report.md`, `data/reports/intraday/2026-08-04_08-29_intraday_report.md`, `data/reports/swing/2026-08-04_03-22_swing_report.md` (carry-forward)
- Stocks: `data/reports/stocks/intraday/2026-08-04_06-02_stocks_intraday_report.md`; stocks swing/invest reports are stale (>1 month, deprecated frameworks — excluded)
- `data/processed/llm_analysis_packet.md` (generated 2026-08-04T08:29:12Z), `data/processed/llm_stocks_packet.md` (generated ~06:04Z)
- `data/processed/agent_outputs/20260804_082907_trade_idea_agent.json` (15 crypto ideas, all C-tier/rejected)
- `data/catalysts/2026-08-04/catalyst_cycle_08-31.md`, `catalyst_events.jsonl` (2000 rows today), `narrative_baskets.jsonl` (5 baskets)
- CLI: `active-signals --asset-class crypto` (23 rows), `active-signals --asset-class stocks` (50 rows), `signal-stats` (both), `detect_untracked_legacy_alerts --since 2026-08-04` (0 untracked)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-04_0445.md`
- External: 2 WebSearch queries (Coldcard hack status, Iran/Hormuz status) — see §13

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: 11:39 EEST (current) — **fresh**, not deferred.
- Latest cycle summary: `cycle_05_08-29_summary.md` — fresh, same cycle as the intraday report used here.
- Crypto scalp/intraday reports: ~10–20 min old — **fresh**.
- Crypto swing report: 03:22 UTC / ~5h17m old — **carry-forward** (4–12h band), flagged.
- Stocks intraday report: 06:02 UTC / ~2h37m old — fresh but pre-market (US cash closed until 13:30 EEST).
- Stocks swing/invest: last generated 2026-07-02 — **stale (>14h)**, excluded from verdict.
- No monitor/paper-status file was read this cycle (not in the allowed read list); not included.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-08-04 11:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["stocks breadth EMA20/50 returned 0.0%/nan — likely pre-market data gap"],
      "suggested_effect": "advisory_only", "facts_used": ["scheduler.log 11:39", "swing report 5h17m old", "stocks index trends show 5d/20d=+nan%"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["chop", "risk_off", "mixed"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["crypto regime label range/chop, macro risk 100/100 risk-off", "stocks regime risk_off/short bias, VIX 15.99 calm", "breadth crypto 57.5% above EMA20"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "no_catalyst"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["57.2% unmapped catalyst events today (1144/2000)", "5 narrative baskets: delisting_thin_liquidity(XRP), binance_ecosystem_teaser(BNB/ASTER), ai_narrative(NEAR/RENDER/TAO/FET), rwa_narrative(ONDO/XLM), momentum_breakout(HOME/COTI/SNXXB)"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "funding_extreme", "data_unavailable"], "data_missing": ["OI change n/a for most fallback_via_mexc symbols"],
      "suggested_effect": "advisory_only", "facts_used": ["BICO/COTI/BANK/MIRA/VANRY show negative funding + elevated external crowding = short-squeeze setups", "ETH price up + OI down = short covering, weaker continuation quality"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "overextended", "stale_before_entry"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["VIC/USDT +68.4% 24h, now more extended than the 04:45 review's +55%", "HOME/USDT +32.4% 24h but trade-idea agent still says watch-only, conditional pullback 0.00833-0.00867", "COTI/TUT tagged overextended"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.6,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"], "data_missing": ["closure/expiry logic for weeks-old 'active' stock signals not verifiable from this view"],
      "suggested_effect": "advisory_only", "facts_used": ["23 crypto positions all open (5 triggered, 11 tp1_hit, 7 tp2_hit), 0 waiting", "50 stocks positions: 1 waiting_for_entry (WMT), 49 open running", "0 untracked legacy alerts"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["headline_risk", "legal_risk", "reduce_risk"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["MSFT demoted A→C partly for active legal/headline risk (class_action, securities_fraud)", "GOOGL/USDT catalyst: Teads Holding lawsuit vs Google/Alphabet", "AMD/CAT/SMCI earnings today = gap/chase risk"] },
    { "agent": "playbook_performance", "verdict": "bad", "confidence": 0.75,
      "reason_codes": ["playbook_failing", "low_sample", "playbook_working"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["crypto swing PF 0.83/avgR -0.057 (n=25) negative", "crypto scalp PF 0.167/avgR -0.192, 0W-3L", "crypto intraday PF 3.34/avgR 0.91 strong", "stocks intraday overall PF 0.50, shorts PF 0.14 (1W-10L)", "weekend=Y cohort winrate 11%"] },
    { "agent": "head_trader", "verdict": "watch_only", "confidence": 0.6,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["synthesis of all agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "HOME/USDT", "trigger": "1h close inside 0.00833-0.00867 pullback zone with volume, not the current chase price", "reason": "top RS/momentum mover this cycle, but trade-idea agent explicitly caps it watchlist-only pending a real pullback" },
    "best_short_candidate":    { "symbol": "KAITO/USDT", "trigger": "confirmed failed-bounce structure (crypto_failed_bounce_short playbook, WR40%/PF2 14d) + derivatives confirmation before entry", "reason": "weak_vs_market, -9.68% 24h, RS/BTC -11.36%, but currently rejected by the scorer on low data confidence" },
    "best_catalyst_candidate": { "symbol": "BTC/USDT", "trigger": "24-48h with no new Coldcard theft wave, or a formal Coinkite/Galaxy resolution statement", "reason": "externally confirmed ongoing hack ($89-116M across sources), the dominant driver of today's risk-off macro score" },
    "avoid_candidate":         { "symbol": "VIC/USDT (chase) / crypto scalp mode", "reason": "VIC now +68.4% 24h, more extended than last cycle's +55%; crypto scalp structurally negative (PF 0.167, 0W-3L today)" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.70 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.65 | chop, risk_off, mixed | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, fresh_catalyst, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, funding_extreme, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, overextended, stale_before_entry | advisory_only |
| execution_lifecycle | ok | 0.60 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.65 | headline_risk, legal_risk, reduce_risk | advisory_only |
| playbook_performance | bad | 0.75 | playbook_failing, low_sample, playbook_working | advisory_only |
| head_trader | watch_only | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (04:45)

- **BTC/Coldcard**: unchanged as the dominant catalyst-watch; external figures now cluster $89–116M across sources (vs. the 04:45 review's $116M/1,816 BTC figure) — no evidence of a fresh escalation wave since, but exposure is not fully closed. Still catalyst-watch, not a trade.
- **VIC/USDT**: more extended (+68.4% 24h vs +55% at 04:45) — chase-risk has gotten worse, not better; still no pullback confirmed.
- **BANK/USDT**: dropped out of the top-movers/weakest lists this cycle (24h move only -2.33%); demoted from short-watch to background-watch — no longer the cleanest short idea.
- **New this cycle**: HOME/USDT climbed to the #2 RS mover (was previously only tracked as an open position, not a fresh idea); COTI/BICO surged with elevated negative-funding crowding (squeeze setups); a fresh `ai_narrative` basket formed (NEAR/RENDER/TAO/FET, <6h); ONDO's `rwa_narrative` context now carries a bearish undertow (team dumped 20M tokens, lost key support).
- **Catalyst mapping**: 57.2% unmapped today vs 53.2% at 04:45 — slightly worse, still over the weak-mapping threshold.
- **Stocks**: MA (score 89) and CRM (score 92) remain the top demoted-A/B names into the open, same as the overnight read; MSFT's legal/headline flag (class_action, securities_fraud) is new information surfaced in this cycle's packet.
- Crypto open positions (23) and stocks open positions (50) are unchanged in composition from the last read; no new triggers, no new closes visible in this data view.

## 5. Catalyst Coverage

- Total catalyst_events today: **2000**; mapped (non-null symbol): **856** (42.8%); unmapped: **1144** (57.2%).
- Narrative baskets: **5** (delisting_thin_liquidity/XRP, binance_ecosystem_teaser/BNB+ASTER, ai_narrative/NEAR+RENDER+TAO+FET, rwa_narrative/ONDO+XLM, momentum_breakout/HOME+COTI+SNXXB+TUT).
- **Catalyst mapping weak this run (57.2% unmapped) — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines: "ARC Group Securities Acquisition I Announces Pricing of $105,000,000 Initial Public Offering"; "S.Korea July consumer price index posts first monthly decline since Nov. 2025"; "Ibotta Non-GAAP EPS of $0.46 beats by $0.09, revenue of $88.9M beats by $3.93M" — general macro/earnings noise, not symbol-specific misses.

## 6. Market Landscape

- **Crypto**: regime label range/chop, risk mode neutral (100/100 confidence per the desk's own classifier), breadth 57.5% above EMA20 / 40% above EMA50 / 62.5% positive 24h — a technically constructive breadth read sitting under a heavy macro risk-off overlay (score 100/100) driven by the Coldcard exploit and Iran/Hormuz tension. Top RS movers (HOME, BICO, COTI, SNXXB, TUT, HFT, VIC) skew toward small/mid-cap alt momentum, several already tagged overextended.
- **Stocks**: US cash session not open until 13:30 EEST. Desk labels regime risk_off/short-bias, VIX 15.99 (calm — not confirming the "risk_off" label strongly), breadth reading 0% above EMA20/50 (nan on 5d/20d index returns — likely a pre-market data gap, treat with caution). AMD/CAT/SMCI report earnings today; LLY/UBER report tomorrow. PLTR up ~15% after-hours on an earnings beat (not yet confirmed at RTH).

### Market Mood / Risk Routing

- Crypto mood: **risk-off / chop** (technical breadth is fine, macro overlay is not)
- Stocks mood: **pre-market / mixed** (regime says risk_off, VIX says calm — treat as unresolved until the open)
- Dominant narrative: BTC self-custody exploit risk + Iran/Hormuz geopolitical overhang, competing against altcoin RS leadership (HOME/VIC/COTI/BICO) and AI-sector rotation (NEAR/RENDER/TAO/FET)
- Preferred side now: **wait-for-trigger**, mild bearish lean on crypto beta given the macro overlay
- Best long candidate: HOME/USDT — none clean at current price; watch the stated pullback zone
- Best short candidate: KAITO/USDT — none clean yet; needs a confirmed failed-bounce structure, not a fresh-high chase
- Best catalyst-backed candidate: BTC/USDT — Coldcard exploit containment watch
- What to avoid: chasing HOME/VIC/COTI/BICO at current extension; new crypto scalp entries (structurally negative); new stocks entries before RTH confirmation; MSFT longs without resolving the legal/headline flag
- What would change the view: a Coinkite/Galaxy Research resolution statement on Coldcard, a genuine volume-backed pullback into the stated HOME/VIC zones, or a clean US cash open that confirms (not contradicts) the demoted-A/B stocks list

## 7. Candidate Deep Dives

### BTC/USDT — catalyst-watch (macro risk driver)
- Has price reacted to the catalyst? Yes — internal risk_warning flags an "extreme day" for BTC with on-chain metrics well above 2-year median; external sources confirm an ongoing, multi-wave hack.
- Chasing / retest / overextended? N/A — risk-context watch, not a directional entry.
- Actionable level: a Coinkite/Galaxy Research resolution/containment statement, or 24-48h with no new theft wave.
- Aligned with mood? Yes — primary source of today's risk-off overlay.
- Long/short/wait? Wait-for-trigger (macro context).
- Catalyst confirmation: **confirmed, ongoing but not obviously escalating further** — external figures ($89-116M across Fortune/CoinDesk/Fox Business/TheHackerNews) are consistent with, not larger than, the 04:45 read; patch shipped Aug 1, but unmigrated wallets remain exposed.

### HOME/USDT — long-watch (best long candidate) + open position
- Top RS mover this cycle (24h +32.4%, 7d +54.7%, RS/BTC +30.8%), but the desk's own trade-idea agent caps it C-tier/watchlist (score 64) — "evidence is not strong enough for an active trade."
- No fresh verified catalyst (this is the `momentum_breakout` basket — pure momentum, no news).
- Derivatives: negative funding (-1.41%) via MEXC fallback = short-squeeze potential, but crowding is "unknown" (thin data).
- Separately, an open B-tier swing long (`sig_57d425cf4bc41003`, triggered, entry 0.00604-0.00617, invalidation 0.00588) is already running from a prior cycle — no new entry needed there.
- Actionable level for a **fresh** entry: 1h close inside the conditional pullback zone 0.00833-0.00867 with volume, invalidation 0.00792 if activated.
- Chase-risk: high at current price (~0.00882, above the stated entry zone).

### VIC/USDT — avoid-chase (was best long-watch at 04:45)
- 24h +68.4% (up from +55% at 04:45) — more extended, not less. Trade-idea agent rejects it outright (score 47.3).
- No fresh verified catalyst — pure RS/momentum, and the desk's own no-catalyst-intraday cohort is net negative (WR 23%/PF 0.70/-3R per the playbook table).
- Actionable level: only a genuine multi-ATR pullback with volume; current extension is a clean avoid.

### KAITO/USDT — short-watch (best short candidate)
- weak_vs_market bias, score 79.8 in the RS table but **rejected** by the trade-idea agent (score 47.3, low data confidence).
- 24h -9.68%, RS/BTC -11.36% — genuine relative weakness, not yet a confirmed failed-bounce structure.
- Separately, an existing open B-tier intraday **long** on KAITO (`sig_c48e5a1bfac269cb`, tp2_hit, entered ~Jul 21) already banked its wins before this week's weakness emerged — no live conflict, just a reminder the desk had a long thesis on this name three weeks ago that has since reversed.
- Actionable level: confirmed failed-bounce structure (crypto_failed_bounce_short playbook, 14d WR 40%/PF 2.00) plus derivatives confirmation before entry — do not short purely on the RS/weakness score.

### Stocks — MA / CRM / MSFT (demoted near-A/B, pre-open watchlist)
- MA long (score 89, financials, RR 1.66 structural, RS·SPY 5.95) and CRM long (score 92, technology, RR 1.5, RS·SPY 11.4) are the strongest demoted candidates — demoted **only** for `market_closed_intraday_planning_only`, not a quality flag. Reasonable candidates for RTH confirmation once the cash session opens at 13:30 EEST.
- MSFT long (score 83) carries `legal_headline_risk: class_action,securities_fraud` on top of the market-closed cap — **manual review required**, not a clean approve even after the open.
- BAC and NOW longs (scores 83/82) are lower-conviction versions of the same "wait for RTH confirmation" thesis.
- Legal/headline note (separate from the above): GOOGL/USDT catalyst layer flags a Teads Holding lawsuit against Google/Alphabet (importance 0.82) — no current GOOGL position is open, so this is context, not an active-position risk.

## 8. Best Candidates Ranked

1. **Long-watch: HOME/USDT** — trigger: 1h close inside 0.00833-0.00867 with volume; do not chase current price.
2. **Short-watch: KAITO/USDT** — trigger: confirmed failed-bounce structure + derivatives confirmation; do not short on RS-weakness score alone.
3. **Catalyst-watch: BTC/USDT** — trigger: Coinkite/Galaxy resolution statement or a clean 24-48h with no new theft wave.
4. **Stocks pre-open watchlist: MA, CRM** — trigger: RTH confirmation in the first 15-30 min after the 13:30 EEST open; reject if gap-and-fade.
5. **Open-position watch (no new entries)**: 23 crypto B-tier positions (5 triggered/entered, 11 tp1_hit, 7 tp2_hit) and 49 stocks positions (1 waiting_for_entry: WMT short) — monitor invalidation levels only.
6. **Avoid: VIC/USDT at current extension; crypto scalp mode; MSFT long (legal/headline flag)**.

No A-tier setup cleared the desk threshold in any crypto mode or stocks intraday this cycle — consistent with the 04:45 read.

## 9. Avoid / No Trade (this decision window only)

- **VIC/USDT at current spot** — chase-risk; +68.4% 24h with no catalyst.
- **Crypto scalp mode** — structurally negative today (PF 0.167, 0W-3L) and over 14d (PF 0.14).
- **Crypto swing mode entries (new)** — 14d/today cohort is net negative (PF 0.83, avgR -0.057, n=25); existing open swing positions are fine to hold, new entries need a materially cleaner setup than the average.
- **Stocks — all names** — market not yet open; every candidate is still planning-only until 13:30 EEST RTH confirmation.
- **MSFT long** — active legal/headline risk (class_action, securities_fraud); manual review required even after the open.
- **AMD, CAT, SMCI** — earnings land today; gap/chase risk regardless of direction.
- This is a decision-window verdict only — **not** a recommendation to pause scanning, tracking, or the scheduler, all of which continue normally.

## 10. Main Risks

- **BTC Coldcard exploit** — externally confirmed ongoing since Jul 30, $89-116M across sources, patch shipped Aug 1 but unmigrated wallets remain exposed; a fresh wave would deepen the risk-off mood market-wide.
- **Iran / Strait of Hormuz** — active tension continues (Trump-Iran talks tense per Aug 2-3 reporting); some signals of a possible Hormuz-specific de-escalation deal, but not confirmed enough to lower the macro risk score.
- **Catalyst mapping weak** — 57.2% unmapped today (worse than 53.2% at 04:45); treat the catalyst layer as context only.
- **Crypto swing mode negative edge** — 14d/today PF 0.83, avgR -0.057 (n=25) — the mode carrying the most open positions (COTI, EPIC, AEVO, HFT, HOME, ERA all swing) is the weakest-performing mode right now.
- **Stocks short-side edge weak** — PF 0.14, 1W-10L (91 short signals sampled) — avoid leaning on short signals without independent confirmation.
- **Data-quality gap on stocks breadth** — index 5d/20d returns show `nan`, breadth above EMA20/50 reads 0.0% despite VIX being calm; treat the stocks regime label with caution until the RTH open refreshes clean data.
- **Legacy open-position volume** — 50 "active" stocks signals span back to 2026-07-08, many already tp1/tp2_hit; whether these should still show as "active" vs formally closed is unclear from this read (see §14).

## 11. Action Plan — next 4 hours

- Monitor BTC/Coldcard for a resolution statement or a new theft wave before the 16:20 pre-US-open review.
- Watch HOME/USDT (and secondarily BICO/COTI, both squeeze-flagged) for a genuine pullback into the stated conditional zone — do not add at current extension.
- Watch KAITO/USDT for a confirmed failed-bounce structure before treating it as a clean short.
- Build the RTH watchlist from MA and CRM (demoted-A/B, financials/technology) for confirmation at the 13:30 EEST cash open; treat MSFT as manual-review-only regardless of confirmation.
- No new crypto scalp or swing entries this window; existing open positions continue to be monitored, not added to.
- Continue scanning, tracking, and monitor processes in all cases — no pause recommended for any mode or asset class.

## 12. Final Verdict per Mode

- **Crypto scalp:** No trade. Structurally negative today and 14d (PF 0.167 / 0.14).
- **Crypto intraday:** Watch-only. Best name HOME/USDT (score 64), chase-risk at current extension; strongest-performing mode by 14d stats (PF 3.34) but nothing clears the desk threshold this cycle.
- **Crypto swing:** Selective watch, downgraded caution. Mode is net-negative 14d (PF 0.83); HOME/VIC/KAITO conditional watch only, nothing actionable now.
- **Stocks intraday:** Planning-only until 13:30 EEST RTH open. MA/CRM top pre-open candidates; MSFT flagged for manual review.
- **Stocks swing/invest:** Stale (>1 month, deprecated frameworks) — excluded from this cycle's verdict, unchanged status.

## 13. Sources

- [Bitcoin owners rocked by $116 million hack: What we know about the Coldcard exploit](https://fortune.com/2026/08/03/bitcoin-owners-116-million-hack-coldcard-coinkite-exploit/) — Fortune, 2026-08-03.
- [Bitcoin cold-wallet attack spreads to 4,500 addresses as losses near $89 million](https://www.coindesk.com/tech/2026/08/02/bitcoin-cold-wallet-attack-spreads-to-4-500-addresses-as-losses-near-usd89-million) — CoinDesk, 2026-08-02.
- [Coldcard Hardware Wallet Flaw Linked to $70 Million Bitcoin Theft in 41 Minutes](https://thehackernews.com/2026/08/coldcard-hardware-wallet-flaw-linked-to.html) — The Hacker News, 2026-08 (date within article unavailable, treated as single_source).
- [Coldcard bitcoin hardware wallet flaw linked to $89M bitcoin theft](https://www.foxbusiness.com/fox-news-tech/coldcard-wallet-attack-drains-up-89m-bitcoin-from-1200-addresses) — Fox Business, 2026-08.
- [Aug 2-3, 2026 — Trump calls Iranian leadership 'unbelievably duplicitous' after Tehran denies talks resumed](https://www.cnn.com/2026/08/02/world/live-news/iran-war-trump) — CNN, 2026-08-02/03.
- Internal: `data/reports/scalp/2026-08-04_08-22_scalp_report.md`, `data/reports/intraday/2026-08-04_08-29_intraday_report.md`, `data/reports/swing/2026-08-04_03-22_swing_report.md`, `data/reports/stocks/intraday/2026-08-04_06-02_stocks_intraday_report.md`, `data/catalysts/2026-08-04/catalyst_cycle_08-31.md`, `data/catalysts/2026-08-04/catalyst_events.jsonl`, `data/catalysts/2026-08-04/narrative_baskets.jsonl`, `data/processed/llm_analysis_packet.md`, `data/processed/llm_stocks_packet.md`, `OPUS_ENRICHED_REVIEW_AUTO_2026-08-04_0445.md`.

## 14. Fix Requests / TODO

### TODO-legacy-open-position-volume (priority: medium)
- **issue:** `active-signals --asset-class stocks` returns 50 rows spanning back to 2026-07-08, most already `tp1_hit`/`tp2_hit`, several dozen with `expires_at` dates weeks in the past. It's unclear from CLI output alone whether these are genuinely still "open" (awaiting final close) or should have rolled to a closed state by now.
- **evidence:** `python -m src.cli active-signals --asset-class stocks` (2026-08-04 11:xx EEST run) — e.g. `sig_233f3bc872fbc9ae` (JPM swing, tp1_hit, expires_at 2026-07-08T03:09:43).
- **suggested manual fix:** a human-driven session should confirm whether "active" = "not yet finally closed" by design (in which case this is expected and just needs clearer lifecycle labeling in the CLI output) or whether a closure job is stuck/missing.
- **priority:** medium
- **first observed:** 2026-08-04 11:39 EEST (this run; likely present in prior runs too but not previously called out explicitly).

### TODO-stocks-breadth-data-gap (priority: medium)
- **issue:** `llm_stocks_packet.md` §1 Stock Market Regime shows `Breadth above EMA20: 0.0%`, `Breadth above EMA50: 0.0%`, and index 5d/20d returns as `+nan%` for SPY/QQQ/IWM/DIA — likely a pre-market data availability gap, but it drives the `risk_off` regime label the desk is currently using, which conflicts with a calm VIX (15.99).
- **evidence:** `data/processed/llm_stocks_packet.md` lines 97-123 (2026-08-04 06:xx UTC generation).
- **suggested manual fix:** check whether the stocks regime classifier has a pre-market/session-gap guard (similar to the crypto weekend-mode overlay) that should suppress or caveat the regime label when index returns are nan.
- **priority:** medium
- **first observed:** 2026-08-04 11:39 EEST.

### TODO-catalyst-mapping-persistently-weak (priority: low, recurring)
- **issue:** Catalyst→symbol mapping has been over the 50% unmapped threshold for at least two consecutive reviews (53.2% at 04:45, 57.2% now) — trending worse, not better.
- **evidence:** computed from `data/catalysts/2026-08-04/catalyst_events.jsonl` (2000 rows, 1144 null-symbol) this run; 04:45 review reported 53.2%.
- **suggested manual fix:** revisit the symbol resolver in the catalyst layer per the earlier-raised TODO; consider whether the unmapped rate is a genuine regression or reflects an increasing share of generic macro/earnings headlines the resolver was never meant to map.
- **priority:** low
- **first observed:** 2026-08-04 04:45 EEST (carried forward, still unresolved).
