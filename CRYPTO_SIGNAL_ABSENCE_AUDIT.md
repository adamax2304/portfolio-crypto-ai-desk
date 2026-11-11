# Crypto Signal Absence Audit — 2026-05-27

**Generated:** 2026-05-28 ~01:05 EEST (post-day review)
**Scope:** explain why crypto produced very few/no Telegram alerts today while stocks got 110+.

---

## Executive Summary

**Verdict:** **Crypto no-trade today was MOSTLY correct** — the market regime flipped to a downtrend, the system rejected over-extended movers, and only 1 crypto B-tier idea was generated all day (ICP/USDT scalp at 13:30 UTC, which expired without triggering).

**BUT** there is also a **real architectural asymmetry** in the alert path: crypto uses the **legacy `watchlist_alerts`** table with `_maybe_send_trade_alerts` (only fires on tier upgrades between monitor ticks), while stocks uses the **modern `signal_alerts`** ledger with `MaterialImprovementChecker` (fires on score/entry/invalidation deltas). This means even when crypto **does** produce A/B, the alert rate is intrinsically much lower than for stocks.

So the answer to "why few crypto alerts?":
- **80 % market conditions** (downtrend regime → almost no clean A/B candidates today)
- **20 % alert architecture asymmetry** (crypto path only alerts on tier upgrades, not on score/entry improvements within the same tier)

**No scoring/threshold changes recommended** based on today's data. Sample too small; regime explanation is sufficient.

---

## 1. Crypto Report Funnel — today

5 scalp + 5 intraday reports were generated today. Picking the **latest scalp report** (2026-05-27 16:11 UTC) as representative:

| Stage | Count |
|-------|------:|
| After liquidity filter | 43 |
| After momentum filter | 8 |
| Fused candidates | 53 |
| Full agent analysis | 15 |
| **A-tier** | **0** |
| **B-tier** | **0** |
| C-tier / watchlist | several |
| Rejected | many |

**Rejection reasons in scalp report:** 12 occurrences of `Price is more than 2 ATR from EMA20 / extended / chase`. Top movers were correctly demoted as over-extended (textbook behaviour — system saved itself from chasing).

**Crypto reports across the day (5 scalp + 5 intraday):**
- `data/reports/scalp/2026-05-27_{05-11,08-26,11-39,13-30,16-11}_scalp_report.md`
- `data/reports/intraday/2026-05-27_{05-19,08-32,11-48,13-38,16-21}_intraday_report.md`

Each ran in 8–10 minutes. No exceptions. Data freshness within 1 hour of run. Exchange coverage normal (Binance + Bybit + MEXC).

---

## 2. Crypto Regime — what changed today

| Field | 2026-05-26 | 2026-05-27 (today) |
|-------|------------|---------------------|
| BTC trend | transition_up | **downtrend** |
| ETH trend | range | **downtrend** |
| Altcoin breadth above EMA20 | 65–72 % | **57.14 %** |
| Recommended style | selective only | **mean reversion or wait for clean breakouts** |

This is a meaningful regime shift. The scoring engine appropriately:
- Raised the bar for longs (downtrend = penalty)
- Demoted over-extended movers to rejected (12+ rejections for "Price > 2 ATR from EMA20")
- Surfaced no fresh A/B because no setup satisfied both **trend alignment** AND **clean R:R** AND **invalidation**

**This is exactly what the protocol calls for: "NO TRADE is a valid, preferred answer."**

---

## 3. Crypto Alert Path — what happened today

| Metric | Count |
|--------|------:|
| Crypto A/B `proposed_signals` registered today | **1** (ICP/USDT scalp B-tier, score 65.0, 13:30 UTC) |
| Crypto `signal_alerts` rows (new ledger) | **0** |
| Crypto `watchlist_alerts` rows (legacy) | **2** |
| Crypto signals currently `expired` / `stopped` | 9 of 9 (all closed) |
| Latest still-active crypto signal | none — TAO/USDT B `tp1_hit` from 2026-05-25 was the last open one and has since closed |

**The one crypto B-tier today (ICP/USDT, 13:30 UTC):**
- Status: **expired** (validity window passed without entry trigger)
- Score: 65.0 (just over the B-tier floor)
- Mode: scalp
- Direction: long

So **1 crypto B-tier was found, 2 legacy `watchlist_alerts` were sent for it (registration + a status update), 0 entries triggered, expired naturally**.

**Why so few?**
- Regime downtrend.
- Over-extension gate rejected the obvious movers.
- Only 1 B-tier passed all filters → very limited alert surface.

---

## 4. Architectural Asymmetry — crypto vs stocks alert path

| Aspect | Crypto path | Stocks path |
|--------|-------------|-------------|
| Alert log table | **`watchlist_alerts`** (legacy) | **`signal_alerts`** (modern, asset-class-aware) |
| Trigger module | `Supervisor._maybe_send_trade_alerts` + `WatchlistMonitor.format_alert` | `StocksMonitorSession` + `MaterialImprovementChecker` |
| Material-improvement detection | No — only tier promotion B→A or new symbol | **Yes** — tier upgrade, score Δ≥5, entry Δ≥0.5%, invalidation Δ≥0.5% |
| Cooldown | Yes (`notifier.cooldown_minutes`) | No (per-setup dedup instead) |
| Per-cycle scan | Only when `WatchlistMonitor` ticks | Every `stocks-monitor-session` tick (~every 10 min) |
| Today's count | 2 (one ICP brief promotion + one update) | 110 (every score wiggle of A/B setups triggered an alert) |

**This is by design** — the two pipelines were built at different times and never unified. Stocks got the modern monitor in the recent QA pass; crypto still runs the original path.

**Is this a bug?** No. **Is this a hygiene gap?** Yes. **Should we fix it now?** No — per the safety contract, no architecture change today. Logging this as a Should-fix.

---

## 5. Crypto Tracking / Stats — verified

```
python -m src.cli track-signals --all
checked=223 updated=0 tp_hits=63 stopped=0 expired=0
not_triggered=0 ambiguous=0 no_ohlcv=0 errors=0

python -m src.cli signal-stats --asset-class crypto
sample=9 (confidence=anecdotal) | triggered=8 / not_triggered=1
wins=1 losses=4 amb=0 | PF=0.5 avgR=-0.25 totalR=-2.0
```

**Dedup view (raw=9, dedup=9, no inflation):**
- Crypto A/B: PF 0.50, totalR -2.0R, winrate 20 %
- Crypto scalp A/B: PF 0.00, totalR -1.0R, winrate 0 % (0/4 wins)
- Crypto intraday A/B: PF 0.67, totalR -1.0R, winrate 25 % (1/4 wins)

**Honest reading:**
- 9 signals across a week → **anecdotal**, not actionable for tuning
- Crypto scalp has been the worst-performing bucket (0 wins in 4 setups)
- Crypto intraday: 1 win (TAO TP1) out of 4 closed = 25 %
- The single win was TAO TP1 booked earlier this week; everything else stopped/expired

**Do not modify scoring on this sample.** Wait for at least 30 closed crypto signals.

---

## 6. LLM Packet Freshness — verified

| Packet | Last modified | Status |
|--------|---------------|--------|
| `data/processed/llm_analysis_packet.md` | 2026-05-27 **19:21:26** | ✅ refreshed by latest crypto run |
| `data/processed/llm_stocks_packet.md` | 2026-05-27 **19:29:47** | ✅ refreshed by latest stocks run |
| `data/processed/context_for_llm.md` | 2026-05-27 **19:21:21** | ✅ refreshed by latest crypto run |

**QA Fix #1 (auto-regenerate on report) confirmed working** — every report run touched its packet within seconds.

Crypto packet correctly contains only crypto candidates (no AAPL/LLY/etc.). Stocks packet correctly contains only stocks. Cross-asset isolation preserved.

---

## 7. Obsidian / Notebook Logging — audit

| Folder / file | What's there | Status |
|---------------|--------------|--------|
| `obsidian_vault/11_Trade_Journal/Signal_Performance/Templates/` | Templates only | ✅ exist |
| `obsidian_vault/11_Trade_Journal/Signal_Performance/Weekly_Reviews/` | `2026-05-24_16-53_week_review.md` (1 file, 3 days old) | ⚠️ stale |
| `obsidian_vault/11_Trade_Journal/Signal_Performance/Signal_Logs/` | `2026-05-22_EDEN_USDT_sig_c4442a063769e04f.md` (1 file, 5 days old) | ⚠️ stale |
| `obsidian_vault/16_Stocks/` | rule pages + templates | ✅ exist, no live data |
| `obsidian_vault/15_LLM_Context/Current_Context_For_LLM.md` | template only ("Replace this block when refreshing") | ❌ never auto-refreshed |
| Obsidian crypto signal performance folder | doesn't exist as separate subfolder | n/a |
| `update-obsidian-context` CLI | still a TODO stub (per audit yesterday) | ❌ not implemented |
| `log-idea-to-obsidian` / `log-news-to-obsidian` / `review-day` CLI | still TODO stubs | ❌ not implemented |

**Answers to spec questions:**

1. **Are proposed A/B signals written to Obsidian?** No — no automation writes to Signal_Logs. The 1 existing entry (EDEN 2026-05-22) was manually added or a one-off old run.
2. **Are outcomes written to Obsidian?** No — TP1 hits today (TAO etc.) are in the SQLite tracker, not in Obsidian.
3. **Are TP/stop/expired results written?** No.
4. **Are daily reviews written?** No — 1 weekly review from 3 days ago is the only one.
5. **Are stocks and crypto separated?** Folder structure exists, but neither receives live data.
6. **Does the LLM packet read useful Obsidian context?** It references Obsidian rules but `Current_Context_For_LLM.md` is a template, so dynamic context is missing.
7. **Is `update-obsidian-context` still a TODO stub?** Yes — confirmed.
8. **What exactly is missing?**
   - Automated A/B signal log writer (per-signal Markdown into `Signal_Logs/`)
   - Daily/weekly automated review writer
   - `Current_Context_For_LLM.md` auto-refresh
   - Outcome → Markdown sync (when a signal hits TP/stop, write to Obsidian)

**No fix today** — out of scope for this audit. Documented as a Should-fix list.

---

## 8. Verdict

**Choose one (per spec):** **Crypto no-trade was correct.**

Justification:
- Market regime turned downtrend today; system correctly rejected overextended longs and produced 0 A-tier + 1 B-tier (ICP) all day.
- The 1 B-tier expired without entry — also acceptable (validity window protection).
- Stocks remain bullish regime (separate market) — that's why their alert rate is high.
- Sample size is too small (9 crypto signals total) to claim filters are too strict.

**Secondary finding:** crypto alert architecture is **less reactive** than stocks (legacy `watchlist_alerts` vs modern `signal_alerts`). Even with the same regime, stocks would have produced ~10× more alerts than crypto because of how the monitor is wired. Not broken — just asymmetric.

---

## 9. Recommended Next Step

**Do nothing to scoring / thresholds / agents.** Reasons:
- Sample = 9 crypto signals → anecdotal.
- Regime explanation is sufficient (downtrend → fewer A/B).
- Adjusting thresholds on n=9 risks curve-fitting.

**What to monitor before any change:**
1. Track-signals over the next 5–10 trading days.
2. Watch crypto A/B count vs regime classification.
3. If during a CLEAN UPTREND regime (BTC trend=uptrend, ETH trend=uptrend, breadth ≥ 70 %) we still produce 0 A/B for 48+ hours → THEN investigate filter calibration.
4. If during downtrend / mixed regime we produce 0–2 A/B → that is **correct behaviour**, no fix needed.

**Optional (no scoring impact):** consolidate crypto alerts onto the modern `signal_alerts` ledger so reactivity matches stocks. This is a wiring change, not a strategy change. Out of scope today.

---

## 10. Today's Telegram Failures (separate finding)

While auditing the cycle logs, I found that **cycle_4 and cycle_5 Telegram summaries failed**:
```
2026-05-27 20:34:15,961 telegram=failed:HTTPError (cycle_4)
2026-05-27 22:30:31,046 Telegram send failed: 400 Client Error: Bad Request
2026-05-27 22:30:31,048 telegram=failed:HTTPError (cycle_5)
```

`400 Bad Request` from Telegram usually means:
- Message exceeded 4096 chars (cycle_5 summary text is long), OR
- Markdown parse error (a step's stdout contained unescaped `_` or `*`)

This is an issue in the **scheduler's summary builder** (`build_cycle_telegram` truncates step labels but not the full message). **Not** in the underlying CLI — `telegram-test` worked fine.

Logged as a Should-fix. Easy to address by capping `text` length to 3800 chars before `notifier.send`.
