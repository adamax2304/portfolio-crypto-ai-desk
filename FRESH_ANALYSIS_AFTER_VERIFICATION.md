# Fresh Analysis After Verification — 2026-05-29 (00:0x EEST)

**Verification verdict:** READY (see `SYSTEM_SIGNAL_TRACKING_VERIFICATION.md`).
**Context:** run just after midnight EEST. US market CLOSED. Crypto 24/7.

---

## 1. Verification verdict

**READY.** Signal recording, tracking, stats, report integration, and the stocks alert ledger all verified working. No critical bug → **no code changes made**. Documented limitations: stocks stats inflation (~8×), crypto legacy-alert asymmetry, Obsidian dormant.

---

## 2. Reports generated

| Mode | Path (UTC filename) | EEST |
|------|---------------------|------|
| Crypto scalp | `data/reports/scalp/2026-05-28_21-06_scalp_report.md` | 00:06 |
| Crypto intraday | `data/reports/intraday/2026-05-28_21-05_intraday_report.md` | 00:05 |
| Stocks intraday | `data/reports/stocks/intraday/2026-05-28_21-01_stocks_intraday_report.md` | 00:01 |

Result line (stocks): `Regime=bullish | A/B ideas=9 | C watchlist=8 | rejected=11 | signals registered=17`.

---

## 3. LLM packets refreshed

All three auto-refreshed by their report runs (`LLM packet refreshed:` in each stdout). Crypto packet = crypto only; stocks packet = stocks only. Source report stamped.

---

## 4. Crypto — new A/B/C/rejected

| Tier | Scalp | Intraday |
|------|------:|---------:|
| A | **0** | **0** |
| B | **0** | **0** |
| C / watchlist | BTC/USDT + others | BTC/USDT + others |
| Rejected | many | many |

**Regime:** BTC trend **downtrend**, ETH trend **downtrend**. Style: **"short bias or no trade; avoid weak altcoin longs"** (deepened from yesterday's "mean reversion").

**Verdict:** correct **NO-TRADE**. Crypto has been in a worsening downtrend for 3 days; the scoring engine is right to produce 0 A/B. 1 crypto signal still active (OP/USDT B scalp short, `tp1_hit` — already in profit).

---

## 5. Stocks — new A/B/C/rejected

9 B-tier ideas (NO A-tier this run — a notable softening):

| # | Symbol | Tier | Score |
|---|--------|------|------:|
| 1 | LLY | B | 77.95 |
| 2 | AAPL | B | 77.61 (was A 88.64 earlier this week) |
| 3 | AMD | B | 76.62 |
| 4 | XLK | B | 74.68 |
| 5 | SMCI | B | 73.05 |
| 6 | SMH | B | 70.24 |
| 7 | TSLA | B | 69.32 |
| 8 | **GOOGL** | B | 66.66 (NEW name) |
| 9 | **QQQ** | B | 65.11 (promoted from C) |

- C watchlist: 8 | rejected: 11 | registered: 17
- **No A-tier** — AAPL/LLY both slipped from A to B (scores compressed ~10 pts). The bullish regime is cooling. GOOGL + QQQ newly entered B-tier.

---

## 6. Active signals

| Class | Active | Detail |
|-------|-------:|--------|
| Crypto | 1 | OP/USDT B scalp short — `tp1_hit` (booked TP1) |
| Stocks | ~314+ | the 9 fresh B-tier + duplicates of prior setups; most `waiting`/`triggered` |

---

## 7. Signal-stats (post-analysis)

```
track-signals --all: checked=179 updated=94 tp_hits=98 stopped=21 no_ohlcv=0 errors=0

crypto:  sample=13 (weak)     | triggered=11 | wins=1 losses=5 | PF=0.20 avgR=-0.36 totalR=-4.0R
stocks:  sample=582 (reliable*)| triggered=376| wins=97 losses=62 amb=1 | PF=2.37 avgR=+0.23 totalR=+86.0R
```
\*stocks "reliable" inflated ~8× by duplicate registrations. Deduped stocks A/B ≈ 45 unique setups, PF ~3.5.

**Honest read:**
- Crypto: net negative (PF 0.2, −4R) on weak sample → no edge yet, regime explains it.
- Stocks: strongly positive raw (+86R) but inflated; deduped still positive. Bullish-regime tailwind. Do not over-trust small dedup sample.

---

## 8. Telegram alerts (this run)

- **0 new alerts sent.** Crypto produced 0 A/B → nothing. Stocks reports ran but **no monitor session started** (see §9), so no new stocks alerts.
- 0 duplicates, 0 failures (nothing attempted).

---

## 9. Monitoring decision

| Monitor | Action | Reason |
|---------|--------|--------|
| **Crypto** | ✅ **Started** (`monitor-watchlist --interval 600 --iterations 6`, task `bkzzurb92`, ~60 min) | Crypto trades 24/7; catches any promotion overnight |
| **Stocks** | ⛔ **NOT started** | US market **CLOSED** (00:0x EEST, closed 23:00). A stocks monitor now would run on **stale after-hours data** and re-alert the same 9 B-tier duplicates → violates your own rules ("no stale-data alerts", "no duplicate alerts") |

**Recommendation:** start the stocks monitor at US pre-market / open (≈16:30 EEST) — that's when fresh stock prints arrive. Until then, stocks monitoring has no value.

⚠️ **Crypto monitor is Claude-background** (`bkzzurb92`) — dies if you close Claude. For overnight autonomy, re-arm the Task Scheduler frequent schedule:
```powershell
schtasks /run /tn "CryptoAIDesk_Frequent"
```
(or re-create it for tomorrow). It was the autonomous runner that worked 01:22→~14:12 today before the PC slept.

---

## 10. Missing data warnings

- US market closed → stocks data stale until pre-market.
- yfinance earnings still UNKNOWN for most stocks (risk flag shown per idea).
- Stocks RSS feeds disabled (thin news layer).
- Obsidian dynamic logging dormant (`update-obsidian-context` TODO).
- Autonomous Task Scheduler run today stopped ~14:12 EEST (PC likely slept) — re-arm before next away period.

---

## 11. Final verdict

| Mode | Verdict |
|------|---------|
| **Crypto scalp** | **NO TRADE** — downtrend, short-bias regime, 0 A/B, net-negative sample |
| **Crypto intraday** | **NO TRADE / watchlist** — same downtrend; manage existing OP short (tp1_hit) |
| **Stocks intraday** | **Watchlist only right now** — 9 B-tier (no A-tier; regime cooling), and market is CLOSED. Re-evaluate at US open. LLY/AAPL/AMD remain the lead names if regime holds |

---

## 12. Safety confirmation

- ✅ No auto-trades
- ✅ No scoring changes (no bug found → no code touched)
- ✅ No threshold changes
- ✅ No agent / architecture changes
- ✅ No duplicate monitors (autonomous scheduler already finished; only 1 fresh crypto monitor started)
- ✅ No stale-data alerts (stocks monitor deliberately NOT started post-close)
- ✅ Crypto/stocks isolation preserved
