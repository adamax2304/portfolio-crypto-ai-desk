# Full System and Trade Audit — 48H

**As of:** 2026-06-05 20:30 EEST · window: last 48h · **READ-ONLY** (no code /
scoring / threshold / strategy / scheduler / data changes; no auto-trade).
Data: deduped unique setups from `proposed_signals` + latest `signal_outcomes`
(NOT inflated raw tracker rows). Full universe → `TRADE_UNIVERSE_48H.csv`
(254 rows). Per-trade A/B diagnosis → `TRADE_BY_TRADE_CHART_REVIEW_48H.md`
(55 crypto charts in `reports/trade_charts/48h/`).

## 1. Executive Summary
- **System: PARTIAL-healthy.** Infra stable (scheduler, monitors, collector,
  gates, Opus all working; 0 untracked alerts; 0 cross-contamination). Two
  non-fatal issues: stocks-monitor Telegram **400 delivery failures (~19%)** and
  one **transient network** cycle failure.
- **Crypto A/B: +6R, PF 1.43, WR 39% — net positive.** Shorts **+6R PF 2.0**
  (squeeze guard working), intraday **+4R**, swing +6R(n3). **Scalp −4R PF 0.33**
  is the crypto laggard. **Catalyst-backed +7R PF 4.5 WR 67%** vs no-news −1R.
- **Stocks A/B: −15R, PF 0.42, WR 23% — losing (last 48h).** Driven by
  **swing −12R (0W/12L)** and **A-tier −6R PF 0.14 WR 12%**. (Over the 7-day
  window stocks are still +15R — the damage is concentrated in the last 2 days,
  i.e. the AVGO-led semi/tech pullback hit the swing book.)
- **Best mode:** crypto intraday/shorts + catalyst-backed crypto. **Worst:**
  **stocks swing** (0 wins / 12 losses) and stocks A-tier.
- **Main loss root cause:** stocks **swing longs into a sector pullback** +
  **A-tier overpromotion**. Not stops, not the new gates.
- **Next action:** **pause/cap stocks SWING to watchlist** + fix A-tier
  promotion; fix the stocks-Telegram 400. Crypto: keep, lean into catalyst-backed
  + shorts, review scalp. **Verdict: NEEDS_MODE_PAUSE.**

## 2. System Health
See `FULL_SYSTEM_HEALTH_AUDIT_48H.md`. Verdict **SYSTEM_PARTIAL**. Scheduler
PID 37572 Running; collector 26656; crypto monitor 37880; stocks monitor 36276.
1 transient network cycle-fail (20:04, self-recovered). Stocks-Telegram 400s.

## 3. Fix Verification (all PART-22-era fixes live)
| Fix | Status (48h live) |
|---|---|
| Crypto funnel / RS-leader longs | ✅ active; RS-leaders trade |
| Crypto short-side | ✅ shorts +6R PF 2.0 |
| Crypto squeeze guard (PART 22) | ✅ caps thin/bounce (IO/CHZ→C); clean shorts pass |
| Stock market-closed gate | ✅ overnight A/B → C |
| Post-earnings stale gate | ✅ AVGO-class blocked |
| SMCI legal gate | ✅ C + flag |
| ETF earnings N/A | ✅ |
| A/B-only headline reporting | ✅ |
| Opus market-aware schedule | ✅ slot labels correct |

## 4. Signal Pipeline Integrity
- Untracked legacy alerts: **0**. Bad asset_class rows: **0**. No test_source
  leak in headline (A/B-only split). C-tier separated (not Telegram-actionable).
- `signal_alerts` 48h: 76 sent / **15 failed:HTTPError** / 3 ReadTimeout / 7
  dry_run → **stocks Telegram delivery degraded (~19% fail)**.
- Tracking writes outcomes every cycle (`checked=324 updated=29 tp_hits=164
  stopped=6`). Headline stats use deduped unique setups.

## 5. Trade Universe (48h)
254 signals total. Crypto 55 (all A/B; 0 C). Stocks 199 (A/B 85, C 114). Full
columns (entry/stop/TP/MFE/MAE/times/regime/caps/telegram) in
`TRADE_UNIVERSE_48H.csv`.

## 6. Chart Review Summary
`TRADE_BY_TRADE_CHART_REVIEW_48H.md` covers all 140 A/B trades with
OHLCV-derived per-trade diagnosis (entry-reached / wick-vs-close stop / MFE
milestone / overextension). 55 crypto charts rendered; **stocks charts pending**
(the stocks OHLCV cache uses a yfinance path the chart loader didn't resolve →
`TODO-stocks-chart-ohlcv-path`, cosmetic). Pattern: crypto losers cluster in
chop/danger + thin shorts; stocks losers are swing longs stopped in the pullback.

## 7. Crypto Results (deep)
- **RS-leader longs:** functional; long book net 0R PF 1.0 this window (chop).
- **Shorts:** **+6R PF 2.0 WR 46%** — the short fixes + squeeze guard are paying
  off as the tape stayed bearish (ETH −3R… sorry, ETH short **+3R**, NEAR/FET
  swing shorts **+2R** each). Squeeze guard capped thin/bounce shorts (IO, CHZ)
  to C; **no thin/scam short escaped into A/B**.
- **Regime:** bearish-trend **+5R PF 6.0** (shorts shine); danger −2R; chop −1R.
  → danger/chop remain low-quality for fresh entries (already capped).
- **Liquidity:** thin-coin shorts are the historical losers; guard now filters.
- **Catalyst:** **news-backed +7R PF 4.5 WR 67%** vs no-news −1R PF 0.92 — the
  single strongest performance discriminator in crypto.
- **Mode:** intraday +4R, swing +6R(n3, small), **scalp −4R PF 0.33** (weak).

## 8. Stocks Results (deep)
- **A/B −15R PF 0.42 WR 23%.** Gates all firing (market-closed, post-earnings,
  legal, ETF) — **defense works**; the loss is in *selection/timing*, not gates.
- **By mode:** **swing −12R (0W/12L)**, invest −2R(0W), intraday −1R PF 0.92.
- **A vs B:** **A-tier −6R PF 0.14 WR 12%** (overpromotion persists), B −9R PF
  0.53. A-tier remains worse than B — recurring regression.
- **ETF vs single:** single −11R, ETF −4R.
- **Cause:** swing/A-tier longs on semis/tech (NVDA/SMH/XLK/AMD/AAPL/MSFT)
  entered then got stopped in the **AVGO-led semiconductor pullback** + bullish-
  but-narrow tape. Sector-rotation/timing, compounded by A-tier overcrediting
  score/extension.

## 9. Mode Comparison
| asset/mode | n(A/B) | PF | totalR | WR | read |
|---|---|---|---|---|---|
| crypto intraday | 19 | 1.50 | +4 | 38% | **working** |
| crypto swing | 3 | ∞ | +6 | 100% | working (small n) |
| crypto scalp | 33 | 0.33 | −4 | 25% | **weak — review** |
| stocks intraday | 44 | 0.92 | −1 | 40% | ~breakeven |
| stocks invest | 17 | 0.00 | −2 | 0% | flat/neg, small |
| **stocks swing** | 24 | 0.00 | **−12** | 0% | **PAUSE candidate** |
- Working: crypto intraday/swing/shorts. Losing: **stocks swing**, stocks
  A-tier, crypto scalp. Pause first: **stocks swing**. More data: crypto swing
  (n3), stocks invest. Optimize first: stocks A-tier promotion.

## 10. Stop / TP / Entry Findings
- Crypto stops adequate (prior audit: 2.4–4.5× p90 wick); losses = chop/late
  shorts, now squeeze-guarded. **No stop-geometry change warranted.**
- Stocks swing losses: MFE mostly low before stop = entries faded into the
  pullback (timing), not stops-too-tight. Many overnight/market-closed entries
  already demoted by the new gate; the swing book is the residual.
- **Do NOT change stop/TP geometry** — evidence points to mode/selection, not
  stop width.

## 11. Opus Review Quality
Market-aware slots correct (titles: pre-US-open / US-open reaction / etc.);
8–9 cited URLs; compares prior review; advisory-only (no edits/trades).
**Caught** AVGO stale setup + stocks swing/A-tier weakness independently — i.e.
the deterministic system's blind spots. No false overrides of good crypto shorts.

## 12. Catalyst / Narrative Quality
~1,400 events/day, importance non-zero, top narratives sensible; **mapping ~24%**
(weak, context-only). Crypto **catalyst-backed signals materially outperform**
(+7R vs −1R) → the layer is genuinely predictive when a symbol maps.

## 13. Paper Trading Profitability
**Crypto A/B: +6R PF 1.43** (profitable; shorts + catalyst the engine; scalp the
drag). **Stocks A/B: −15R PF 0.42** over 48h (profitable +15R over 7d → the last
2 days reversed it via swing/A-tier). C-tier (both) negative, correctly excluded
from headline.

## 14. Root Causes of Losses (ranked by R lost)
| rank | bucket | R lost | n | root cause | fixability | overfit risk |
|---|---|---|---|---|---|---|
| 1 | stocks **swing** longs | −12R | 12 | sector pullback (AVGO/semis) into narrow-bull tape | high | low |
| 2 | stocks **A-tier** | −6R | 7 | A-tier overpromotion (score/extension over-credited) | medium | medium |
| 3 | crypto **scalp** | −4R | ~6 | chop whipsaw / low edge in scalp tf | medium | medium |
| 4 | crypto no-catalyst longs | ~−1R | 12 | no catalyst → low edge vs +7R catalyst-backed | medium | low |
| 5 | stocks Telegram 400 | (operational) | 15 | alert message 400 (delivery) | high | none |

## 15. What Works
Crypto shorts (+6R) + squeeze guard; crypto intraday; **catalyst-backed crypto
(+7R)**; crypto swing (small). All stock safety gates (defensive). A/B-only
reporting. Opus market-aware reviews. Infra stability.

## 16. What Does Not Work
**Stocks swing (−12R, 0 wins).** Stocks **A-tier promotion** (PF 0.14). Crypto
**scalp** (−4R PF 0.33). Stocks **Telegram delivery** (400s).

## 17. What NOT To Change Yet
- Crypto short / RS-leader / squeeze-guard logic (working, +6R).
- Stop/TP geometry (stops adequate).
- Global A/B thresholds; crypto long logic; Telegram cooldown/dedup.
- Crypto swing & stocks invest conclusions (n too small — collect more).

## 18. Priority Fix Roadmap (TODOs — evidence attached, NOT implemented)
- **P0:** none (no crash/data-loss/auto-trade risk).
- **P1 `TODO-stocks-swing-pause`** — pause/cap **stocks swing** A/B to
  watchlist (no Telegram) until reviewed. Evidence: −12R, 0W/12L. Benefit:
  removes the single biggest loss bucket. Risk: low (0 winners to lose).
  Implement: **soon**, but confirm it's not a one-off pullback (1 more day data).
- **P1 `TODO-stocks-atier-promotion`** — A-tier PF 0.14 vs B 0.53; investigate
  what overcredits A (score/extension/RS). Benefit: stops promoting losers to
  the top tier. Risk: medium (touches scoring → validate). Implement: after
  scoped study.
- **P1 `TODO-stocks-telegram-400`** — fix stocks-monitor alert 400s (likely
  `parse_mode`/Markdown escaping). Operational; benefit: alerts actually
  deliver. Risk: low. Implement: soon.
- **P2 `TODO-crypto-scalp-review`** — scalp −4R PF 0.33; consider tightening
  scalp entry/quality or weighting catalyst. Benefit: removes the crypto drag.
  Risk: medium. **Need more data** before changing scalp logic.
- **P2 `TODO-crypto-weight-catalyst`** — catalyst-backed +7R vs no-news −1R;
  consider favoring catalyst-backed in selection. Risk: medium (scoring). Wait.
- **P3 `TODO-catalyst-symbol-mapping`** (~24%) + `TODO-stocks-chart-ohlcv-path`.

## Final verdict
```
NEEDS_MODE_PAUSE
```
Infra is healthy; the path to consistently-positive paper trading is to **pause/
cap the stocks swing mode** (the −12R sink) and **fix A-tier overpromotion**,
while **leaning into the crypto book that already works** (shorts + intraday +
catalyst-backed). No stop/TP or threshold change is warranted by the evidence.
All recommendations are TODOs — nothing implemented in this read-only audit.
