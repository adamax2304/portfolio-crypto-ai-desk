# Opus Manual Review — Latest System Analysis

**Reviewer:** manual Opus-style trader / risk-manager pass (no LLM API used — this is reasoning written directly into the file).
**Timestamp:** 2026-05-29 ~16:20 EEST. Scheduler still running; this review is read-only.

---

## 1. Executive Summary

- **Market regime:** split tape. **Crypto = risk-off downtrend** (BTC + ETH both downtrend, breadth collapsing to 23–31% above EMA20). **Stocks = bullish but cooling at the top** (VIX 15.87, 100% index breadth, yet 0 A-tier — leaders lost their A-grade momentum, all dropped to B).
- **Crypto scalp:** **NO TRADE.** 0 A/B, short-bias regime, negative track record.
- **Crypto intraday:** **NO TRADE.** 0 A/B, 0 active signals, breadth 23%.
- **Stocks intraday:** **WATCHLIST ONLY / selective.** 9 B-tier longs (LLY/AAPL/AMD lead), no A-tier, R:R thin. Tradeable only on a clean pullback into zone with index confirmation.
- **Should you hunt trades now?** **No.** Crypto is a no-trade. Stocks have no A-tier and weak R:R — watch LLY/AAPL/AMD for retests, don't chase. Sit on hands; the edge is not screaming.

---

## 2. Data Freshness / Inputs Used

**Reports read:**
- Crypto scalp: `data/reports/scalp/2026-05-29_13-16_scalp_report.md` (16:16 EEST) — fresh.
- Crypto intraday: `data/reports/intraday/2026-05-29_10-33_intraday_report.md` (13:33 EEST) — ~3h old; intraday cadence ok.
- Stocks intraday: `data/reports/stocks/intraday/2026-05-29_10-40_stocks_intraday_report.md` (13:40 EEST).

**Commands run (live):** `track-signals --all`, `signal-stats` (crypto+stocks), `active-signals` (crypto+stocks), dedup script.

**Prior audits incorporated:** `AUDIT_NOTE_UNTRACKED_LEGACY_CRYPTO_ALERTS.md`, `CRYPTO_ALERT_REGISTRATION_AUDIT.md`, `FIRST_CYCLE_SIGNAL_RECORDING_CHECK.md`, `LLM_INTEGRATION_AUDIT.md`.

**Missing / caveats:**
- No live OI/funding deep-dive in this read (derivatives summarized in packet only).
- Earnings = UNKNOWN for most stocks (yfinance gap).
- Stocks RSS disabled → thin stock news.
- Crypto PF/winrate **incomplete** — 4 legacy crypto alerts never registered (see §6).
- No LLM was called by the system; this review is the human/Opus layer.

---

## 3. Crypto Review

### Crypto Scalp
- **Regime:** BTC downtrend, ETH downtrend, **only 31% of symbols above EMA20**. Style label: *"short bias or no trade; avoid weak altcoin longs."*
- **Candidates:** 0 A-tier, 0 B-tier. Top C-tier watchlist: **ICP/USDT** (watchlist only).
- **Why no trades:** correct gating. In a downtrend with collapsing breadth, longs are penalized and movers are over-extension-rejected. The system is doing the right thing.
- **What to watch:** BTC reclaiming its EMA structure + breadth back above ~50% before any long is worth considering.

### Crypto Intraday
- **Regime:** same downtrend, breadth even weaker at **23.1% above EMA20**.
- **Active signals:** **0** — every prior crypto signal has closed (stopped/expired).
- **Tracking outcomes:** crypto is **0 wins / 5 losses**, PF 0.0, **−5R** over 12 (dedup 11) signals. The system's crypto track record this week is **net-negative**.
- **Action:** nothing. No long, and the system isn't producing clean shorts either (counter-trend shorts are capped, and no short cleared A/B).

### Is the crypto silence correct, or a filter/alert problem?
**Mostly correct no-trade**, with one real caveat:
- ✅ **Correct:** downtrend + 23–31% breadth + short-bias style → 0 A/B is the textbook outcome. Not a filter bug.
- ⚠️ **Caveat (alert path):** 4 crypto B-tier alerts (UNI, BCH scalp shorts; XLM, INJ swing longs) were **sent to Telegram via the legacy `watchlist_alerts` path but never registered in `proposed_signals`** → they are invisible to PF/winrate. So the crypto −5R is computed on an **incomplete** sample. The crypto stat is *directionally* negative but the count is understated. (Fix deferred until scheduler finishes, per instruction.)

---

## 4. Stocks Review

- **Market regime:** **bullish.** 4/4 indices (SPY/QQQ/IWM/DIA) trending up, breadth **100%** above EMA20, **VIX 15.87** (low / risk-on).
- **But:** **0 A-tier today.** Top score is LLY at 77.95 — below the 80 A-floor. AAPL/LLY have slipped from A (88) earlier in the week to B (77). **Interpretation: the rally's leaders are losing relative momentum even as the index holds.** Classic late-stage-uptrend breadth-vs-leadership divergence. Risk-on tape, but the best names are cooling.
- **Sectors:** tech/semis still lead (AAPL/AMD/XLK/SMH/SMCI present), pharma (LLY) strongest single name.

### Best B-tier setups (no A-tier exists)

**LLY long — B 77.95**
- Direction: long | Entry: **1120.76–1127.46** | Invalidation: **1107.35** | TP1: **1147.57**
- Thesis: strongest RS leader vs index + sector; bullish regime tailwind.
- Main risk: R:R to TP1 ≈ 1.0 (thin); earnings UNKNOWN (undated event risk).
- What to monitor: hold above 1107.35; SPY not breaking down; volume on the push.

**AAPL long — B 77.68**
- Direction: long | Entry: **311.65–312.50** | Invalidation: **309.95** | TP1: **315.05**
- Thesis: above prior day high, RS leader; mega-cap anchor.
- Main risk: very tight stop (≈2 pts), R:R ~1.0; downgraded from A → momentum fading.
- What to monitor: 309.95 must hold; don't chase above 312.5.

**AMD long — B 76.62**
- Direction: long | Entry: **513.64–518.14** | Invalidation: **504.64** | TP1: **531.64**
- Thesis: best RS vs SPY of the group; semis strong.
- Main risk: wide entry zone, extended; R:R ~1.0–1.3.
- What to monitor: retest into 513–514 rather than chasing 518.

### Ignore / lower-conviction
XLK/SMH/QQQ (ETF B-tiers — basket trades, low edge), GOOGL B 66.66 + QQQ B 65.11 (just over B-floor), and all swing/invest duplicates of the same names (registry noise, not new ideas).

### Earnings / data risk
**Earnings = UNKNOWN** for AAPL/LLY/AMD (yfinance gap). Every one of these B-tiers carries undated event risk — do not hold blindly into an unscheduled print.

---

## 5. Signal Performance Review

| Class | Raw sample | Raw PF | Raw totalR | Dedup unique | Dedup PF | Dedup totalR | Dedup winrate |
|-------|-----------:|-------:|-----------:|-------------:|---------:|-------------:|--------------:|
| Crypto A/B | 13 | 0.0 | −5.0R | 11 | 0.0 | −5.0R | 0% |
| Crypto scalp A/B | 8 | 0.0 | −1.0R | 6 | 0.0 | −1R | 0% |
| Crypto intraday A/B | 5 | 0.0 | −4.0R | 5 | 0.0 | −4R | 0% |
| Stocks A/B | 394 | 2.37 | +86R | **70** | 5.50 | +9R | 80%* |
| Stocks A-only | 68 | — | — | 11 | 1.00 | 0R | 50% |
| Stocks B-only | 326 | — | — | 59 | inf* | +9R | 100%* |

**Reading like a risk manager:**
- **Crypto: avoid.** 0 wins in 11 unique A/B, −5R. Even ignoring the regime, the system's crypto signals have **no demonstrated edge** — they're net-negative. This is **too small to be statistically damning (weak sample)** but it is *zero positive evidence*. Do not take crypto longs on system score alone.
- **Stocks raw stats are UNRELIABLE — inflated ~5.6× by duplicate registrations** (394 raw → 70 unique). The +86R / PF 2.37 raw number is **not trustworthy.**
- **Stocks dedup (70 unique, +9R, PF 5.50)** is more honest and *positive*, BUT: the `B-only PF=inf / winrate=100%` is an **artifact** — most B-tier are still `waiting_for_entry`, and the dedup win-counter lags the live status (`final_outcome` not yet stamped). So the true booked edge is **smaller than +9R suggests**. Verdict: **positive lean, but TOO EARLY to trust as an edge.**
- **A-tier vs B-tier:** stocks A-only dedup is neutral (PF 1.0, 0R, 50%); the apparent edge sits in B-only — which is exactly where the unbooked-waiting bias is largest. Treat with suspicion.

**Bottom line:** crypto = proven-negative-so-far (small sample); stocks = early-positive-but-inflated. Neither justifies aggressive sizing.

---

## 6. Alerts / Tracking Integrity

- **track-signals:** checked=148, updated=0, tp_hits=87 (cumulative), stopped=0, expired=0, **no_ohlcv=0, errors=0.** Healthy this pass (nothing new transitioned).
- **Stocks `signal_alerts`:** registration-first, 0 orphan alerts, 0 C-tier alerts (verified earlier). Clean.
- **Crypto legacy `watchlist_alerts`:** **4 untracked alerts** (UNI, BCH, XLM, INJ) with no `proposed_signal` → not in PF/winrate. **Crypto stats are incomplete by construction.**
- **Crypto active signals: 0** — everything closed.
- **What's missing from stats:** the 4 untracked crypto alerts; any watchlist-monitor tier-flip alerts that bypass registration.

---

## 7. Best Current Candidates

There is **no A-tier anywhere** and crypto is no-trade. The only candidates worth a chart check (all **WATCHLIST / selective, not slam-dunks**):

1. **LLY long** — why it matters: strongest RS leader in a bullish tape. Invalidates below 1107.35. Manually verify: real pharma catalyst, earnings date, SPY trend at entry.
2. **AAPL long** — why it matters: mega-cap anchor above prior-day high. Invalidates below 309.95. Verify: tight stop is realistic for AAPL's ATR, earnings date.
3. **AMD long** — why it matters: best RS vs SPY. Invalidates below 504.64. Verify: wait for 513–514 retest, don't chase.

All three have **R:R ≈ 1.0 to TP1** and **UNKNOWN earnings** — so they are *opportunistic pullback longs*, not high-conviction entries.

---

## 8. Avoid / Watchlist

- **All crypto** — downtrend, 0 A/B, negative track record. AVOID longs; no clean shorts either.
- **Overextended / chase** — don't buy AAPL >312.5, AMD >518.
- **Weak R:R** — every stocks B-tier is ~1.0 to TP1; size down or skip.
- **ETF B-tiers** (XLK/SMH/QQQ) — basket trades, low edge, treat as regime confirmation not setups.
- **Swing/invest duplicates** — same names re-registered; ignore as noise.
- **Missing-invalidation / stale** — none seen today; tracking clean.

---

## 9. Main Risks

- **Market risk:** stocks leaders cooling (A→B drift) inside a still-bullish index — divergence that often precedes a pause/pullback. Crypto in active downtrend.
- **Data risk:** earnings UNKNOWN (all stocks); stocks RSS disabled (thin news); crypto OI/funding not deep-checked here.
- **System risk — crypto legacy tracking gap:** crypto PF/winrate understated because 4 alerts never registered. Don't trust crypto stats as complete.
- **Stocks duplicate inflation:** raw stats 5.6× inflated; only dedup is meaningful, and even dedup is optimistic (unbooked waiting + final_outcome lag).
- **Missing news/earnings/OI/funding** — explicitly flagged, not fabricated.

---

## 10. Action Plan

- **Continue the scheduler** — it's collecting data correctly (tracking clean, no_ohlcv=0). No reason to stop.
- **Next useful analysis:** at the **US-open / mid-US cycles** (the high-priority monitor windows) — that's when stocks B-tiers either trigger on a pullback or fail. Crypto: re-check only if BTC reclaims trend.
- **What to monitor:** LLY 1107.35 / AAPL 309.95 / AMD 504.64 invalidations; SPY/QQQ not breaking down; VIX staying <17; BTC breadth recovering above 50%.
- **Do NOT change** scoring, thresholds, agents, or the legacy crypto path *while the scheduler runs*.
- **Fixes to do AFTER scheduler finishes:** (1) crypto legacy alert → registration unification (per `CRYPTO_ALERT_REGISTRATION_AUDIT.md`); (2) optional — dedup the stocks registry to deflate stats.

---

## 11. Final Verdict

| Mode | Verdict |
|------|---------|
| **Crypto scalp** | **NO TRADE** (downtrend, 0 A/B, negative track record) |
| **Crypto intraday** | **NO TRADE** (downtrend, 0 active, breadth 23%) |
| **Stocks intraday** | **WATCHLIST ONLY** (bullish tape but 0 A-tier, thin R:R, earnings unknown — LLY/AAPL/AMD only on clean pullback) |

**Overall system verdict: WORKS, PARTIALLY TRUSTWORTHY.**
- Pipeline + tracking + reports are functioning correctly.
- **Crypto stats are incomplete** (legacy alert gap) → don't trust crypto PF/winrate yet.
- **Stocks raw stats are inflated** → trust only the deduped view, and even that is early.
- The desk's biggest current value is **discipline**: it correctly refuses crypto trades in a downtrend and refuses to label cooling stock leaders as A-tier. That is exactly what a good risk engine should do.

**Net trader call: sit out crypto entirely; treat stocks as watch-only pullback longs (LLY/AAPL/AMD) with small size and hard invalidations; do not chase; wait for either an A-tier stock setup or a crypto regime flip.**
