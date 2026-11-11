# First Cycle Signal Recording Check — 2026-05-29

**Checked at:** ~14:10 EEST, after the 12h-monitor production cycle 1 completed at 14:04.
**Scope:** read-only inspection + tracking/stat commands. No code/scoring/threshold changes. No auto-trade.

---

## 1. Executive Summary

| Question | Answer |
|----------|--------|
| Are signals being recorded correctly? | ✅ **YES** — 23 stocks B-tier + 20 C-tier registered with full entry/invalidation/TP |
| Are alerts linked to signals? | ✅ Stocks: 0 orphan alerts, 0 C-tier alerts. ⚠️ Crypto: 1 legacy alert (XLM swing) has **no** backing proposed_signal |
| Are outcomes being tracked? | ✅ YES — `track-signals` updated outcomes, `no_ohlcv=0`, `errors=0` |
| Is statistics updating? | ✅ YES — crypto + stocks stats refresh; deduped view available |
| Is Obsidian logging working? | ❌ **NO** — dormant (newest log 2026-05-22), not written this cycle |

**Verdict: WORKING — schedule can continue.** Two non-blocking limitations documented (crypto legacy-alert registration gap; Obsidian dormant).

---

## 2. First Cycle Summary

- **Started:** 2026-05-29 13:10:59 EEST
- **Finished:** 2026-05-29 14:04:01 EEST (~53 min)
- **Result:** `ok=12 failed=0 telegram=sent`
- **Reports generated (cycle 1 includes swing/invest once):**
  - crypto scalp `2026-05-29_10-23` (UTC) ✅
  - crypto intraday `2026-05-29_10-33` ✅
  - stocks intraday `2026-05-29_10-40` ✅
  - crypto swing `~10-56` ✅
  - stocks swing `2026-05-29_10-59` ✅
  - stocks invest `2026-05-29_11-03` ✅
- **Errors/warnings:** none (12/12 steps exit 0)
- **Telegram:** the "sent" ping = scheduler cycle summary. Cycle 1 was NOT a US-window cycle, so **no stocks per-signal monitor alerts** fired. One **crypto** swing alert (XLM/USDT) went out via the legacy path.

---

## 3. Signal Registry Check

| Asset | A | B | C | Notes |
|-------|--:|--:|--:|-------|
| Crypto | 0 | 0 | 0 | downtrend regime → correct NO-TRADE |
| Stocks | 0 | **23** | **20** | across intraday + swing + invest modes |

- **0 A-tier** anywhere — regime cooling (stocks max score 77.95, below the A floor of 80).
- **23 stocks B-tier** span the three modes correctly:
  - intraday (10:40): LLY 77.95, AAPL 77.68, AMD 76.62, XLK 74.68, SMCI 73.05, SMH 70.24, TSLA 69.32, GOOGL 66.66, QQQ 65.11
  - swing (10:59): SMCI 76.39, AMD 75.63, AAPL 74.86, LLY 73.71, XLK 71.12, SMH 67.94, TSLA 67.03, QQQ 65.28
  - invest (11:03): AMD 70.94, AAPL 70.27, SMCI 70.0, LLY 68.31, XLK 65.86, SMH 65.68
- **All 23 B-tier** have entry zone + invalidation + TP1/2/3 + `status=waiting_for_entry` + `source_report_path` stamped. ✅
- **C-tier:** 20 registered, **all 20** carry entry + invalidation (actionable trigger). ✅
- **Rejected ideas:** not present as active signals. ✅
- **Swing/invest correctly ran once** (cycle 1 only) — they will NOT repeat every 2h.

---

## 4. Alert Matching Check

**Stocks (`signal_alerts` ledger):**
- Alerts sent during cycle 1 window: **0** (cycle 1 not a US window → no `stocks-monitor-session`).
- Integrity scan: **0 alerts without a matching proposed_signal**; **0 C-tier alerts**. ✅

**Crypto (legacy `watchlist_alerts`):**
| symbol | tier | mode | score | sent_at | backing proposed_signal? |
|--------|------|------|------:|---------|--------------------------|
| XLM/USDT | B | swing | 65.4 | 10:56 UTC | ❌ **NOT found in proposed_signals** |

⚠️ **Finding (medium):** the crypto **swing** report sent a Telegram alert for XLM/USDT B via the legacy `_maybe_send_trade_alerts` path, but the signal was **not** registered in `proposed_signals`. Consequence: this alert **cannot be tracked** (no signal_id → no outcome). This is a gap in the legacy crypto swing alert path, not in the stocks ledger. Per your "do not change code" instruction, flagged only.

**alert-status (cumulative):**
- Stocks: 394 A/B total, 178 alerts sent, 216 not-alerted (duplicates), 0 dup-skip estimate.
- Crypto: 0 in `signal_alerts` (uses legacy table).

---

## 5. Tracking Results

```
python -m src.cli track-signals --all
checked=154 updated=6 tp_hits=87 stopped=0 expired=5
not_triggered=1 ambiguous=0 no_ohlcv=0 errors=0
```

- ✅ Crypto + stocks both tracked.
- ✅ `no_ohlcv=0`, `errors=0`.
- ✅ Outcomes written back: 6 updates this pass (5 expired, 1 not-triggered; tp_hits=87 cumulative).

---

## 6. Active Signals

- **Crypto:** ~1 active (legacy signals mostly closed; downtrend regime produced no new actives). Net-negative bucket.
- **Stocks:** the 23 fresh B-tier from cycle 1 are `waiting_for_entry` (US market opens 16:30 EEST; entries not yet tested). Plus prior duplicates.
- **Important A/B active:** all stocks B-tier are `waiting_for_entry` — none triggered/stopped yet because cycle 1 ran pre-market (~13:10 EEST). They become live at US open (cycle 3, 17:11).

---

## 7. Signal Stats

| Class | Sample | Confidence | Triggered | Wins | Losses | PF | avgR | totalR |
|-------|-------:|-----------|-----------|-----:|-------:|---:|-----:|-------:|
| Crypto | 12 | **weak** | 10 | 0 | 5 | 0.0 | −0.50R | **−5.0R** |
| Stocks | 625 | "reliable"* | 376 | 97 | 62 | 2.37 | +0.23R | **+86.0R** |

\*inflated ~8× by repeated registrations.

**Deduped (one canonical per unique setup):**
| Bucket | Raw | Dedup | PF | totalR | winrate |
|--------|----:|------:|---:|-------:|--------:|
| stocks A/B | 362 | ~45 | 3.50 | +5R | 75% |
| crypto A/B | 12 | ~11 | 0.0 | −5R | 0% |

**Honest read:** crypto is net-negative on a weak/anecdotal sample (regime-driven, no edge yet). Stocks positive but inflated; deduped still positive but small. **Do not tune scoring on this.**

---

## 8. LLM Packets / Reports

| Packet | Last modified (EEST) | Status |
|--------|----------------------|--------|
| llm_analysis_packet.md (crypto) | 13:53 | ✅ fresh (cycle 1) |
| llm_stocks_packet.md | 14:03 | ✅ fresh (stocks invest report) |
| context_for_llm.md | 13:53 | ✅ fresh |

- ✅ **Recent Signal Performance section present** in the stocks report: `Sample size: 599 ... A-tier 68 | B-tier 312 | C-tier 219 | Triggered 376 | Wins 97 | Losses 62 | PF 2.07` — internally consistent with signal-stats at report time (now 625 after the swing/invest registrations that followed; drift is expected and correct).
- ✅ source_report path stamped; no stale packet.
- ✅ crypto packet = crypto only; stocks packet = stocks only.

---

## 9. Obsidian / Notebook

| Item | Status |
|------|--------|
| New proposed signals → Obsidian | ❌ not written |
| Outcomes / TP / stop / expired → Obsidian | ❌ not written |
| Daily review written | ❌ newest is `2026-05-24_16-53_week_review.md` (stale) |
| Signal_Logs newest | `2026-05-22_EDEN_USDT...md` (7 days old) |

**Status: NOT live for this path.** `update-obsidian-context` / `log-idea-to-obsidian` / `review-day` remain TODO stubs. The SQLite registry + signal-stats + the in-report Recent Signal Performance section carry the same information, so the LLM is not data-starved — it just does not read from Obsidian. Documented limitation, no fix today.

---

## 10. Final Verdict

**WORKING — continue the 12-hour schedule.**

Core pipeline is healthy:
- ✅ Signals recorded with full fields.
- ✅ Stocks alerts linked 1:1 to signals (0 orphans, 0 C-tier).
- ✅ Tracking writes outcomes (no_ohlcv=0, errors=0).
- ✅ Stats + Recent Signal Performance update correctly.
- ✅ LLM packets fresh + asset-class isolated.
- ✅ Swing/invest ran once (no spam).

**Non-blocking limitations (do NOT stop the schedule):**
1. **Crypto legacy swing alert not registered** (XLM/USDT alerted but no proposed_signal → untrackable). Legacy crypto path gap; flagged, not fixed.
2. **Stocks stats inflated ~8×** — use the deduped view.
3. **Obsidian dormant** — registry/stats cover the same data.

The schedule can keep running. The next cycle (cycle 2, regular) is at ~15:11 EEST; the high-priority US-open cycle (cycle 3) at ~17:11 will run the stocks monitor and should generate the first per-signal stocks Telegram alerts of the session.
