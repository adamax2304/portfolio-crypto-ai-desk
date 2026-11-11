# Category Performance Summary (PART 2)

**Date:** 2026-06-11 · **Companion:** [FULL_RESULTS_BY_CATEGORY_AUDIT.md](FULL_RESULTS_BY_CATEGORY_AUDIT.md).

Deduped per-category metrics. Actionable cohorts and watchlist-only / counterfactual cohorts are **separated** — never mixed into the headline number.

---

## 1. ACTIONABLE cohorts (A/B-tier, non-paused playbooks)

### All-time

| Category | n | trig | W | L | Exp | Wait/Stale | WR | PF | raw netR | **sized netR** | avg R | avg MFE | avg MAE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| stocks intraday | 646 | 445 | 140 | 89 | 215 | 201 | 61% | 2.50 | +135.0 | **+133.0** | +0.30 | +0.55 | −0.55 |
| crypto swing | 38 | 35 | 16 | 17 | 2 | 3 | 48% | 2.12 | +19.0 | **+19.0** | +0.54 | +0.80 | −0.55 |
| crypto failed-bounce shorts | 24 | 17 | 7 | 10 | 0 | 7 | 41% | 2.10 | +11.0 | **+11.0** | +0.65 | +0.85 | −0.50 |
| crypto intraday catalyst | 33 | 24 | 3 | 21 | 0 | 9 | 12% | 0.33 | −14.0 | **−14.0** | −0.58 | +0.30 | −0.70 |
| crypto scalp (0.5×) | 85 | 43 | 0 | 9 | 34 | 42 | 0% | 0.00 | −9.0 | **−4.5** | −0.21 | +0.35 | −0.45 |
| **Actionable total** | **826** | **564** | **166** | **146** | **251** | **262** | **53%** | **1.94** | **+142.0** | **+144.5** | — | — | — |

Max drawdown (closed equity curve, raw R, deduped per setup): −12R over 4 consecutive losing days in crypto intraday (2026-06-02 → 2026-06-05).

### 14-day window

| Category | n | trig | W | L | WR | sized netR |
|---|---:|---:|---:|---:|---:|---:|
| stocks intraday | 275 | 206 | 60 | 65 | 48% | +32.5 |
| crypto swing | 38 | 35 | 16 | 17 | 48% | +19.0 |
| crypto intraday + shorts | 47 | 34 | 7 | 25 | 22% | −6.0 |
| crypto scalp | 77 | 37 | 0 | 8 | 0% | −4.0 |
| **14d total** | **437** | **312** | **83** | **115** | **42%** | **+41.5** |

### 7-day window

| Category | sized netR |
|---|---:|
| stocks intraday | +8.5 |
| crypto swing | +10.0 |
| crypto intraday | +2.0 |
| crypto scalp | −0.5 |
| **7d total** | **+20.0** |

### 48-hour window

| Category | raw netR |
|---|---:|
| crypto swing | +1.0 |
| crypto scalp | 0.0 |
| stocks intraday | −1.0 |
| crypto intraday | −6.0 |
| **48h total** | **−6.0** |

48h is a normal noisy window; no decision should be made from it alone.

---

## 2. WATCHLIST-ONLY / PAUSED cohorts (sized weight = 0×)

These do NOT count toward headline performance. Shown only as counterfactual ("if we had taken these at 1×").

| Category | n | trig | W | L | WR | raw netR (counterfactual) |
|---|---:|---:|---:|---:|---:|---:|
| stocks swing watchlist | 54 | 51 | 6 | 39 | 13% | **−32.0** |
| stocks invest watchlist | 39 | 38 | 0 | 26 | 0% | **−26.0** |

Both confirm the pause is right (sized R = 0 = "we lost nothing real").

---

## 3. C-tier / shadow / expansion candidates

| Cohort | n | sized R |
|---|---:|---:|
| C-tier (any asset / mode) | 681 | **+0.0** (weight 0× across the board) |

C-tier never contributes to the portfolio number — by design.

---

## 4. Headline (deduped, all-time)

| Metric | Value |
|---|---:|
| Total A/B sized R | **+144.5 R** |
| Total A/B WR (closed) | 53% |
| Total A/B PF | 1.94 |
| Number of distinct setup-days | 21 |
| Best single setup | STG/USDT swing long ×2 (+6R combined) |
| Worst cohort | crypto_intraday_catalyst_or_momentum (−14R sized) |

The portfolio is **net positive across every window from 7d outward**. The 48h window is negative but small-sample.
