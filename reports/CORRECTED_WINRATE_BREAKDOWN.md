# Corrected Winrate Breakdown (PART 2)

**Date:** 2026-06-10 · Read-only recalculation against the same deduped per-setup CTE that tab 10 uses. All-time window.
**Method:** `Closed = Wins + Losses` (rows with `final_r > 0` or `< 0`). `WR_closed = Wins / Closed × 100`. `WR_all_setups` (the misleading current display) shown for comparison.

## 1. Crypto headline metrics

| Cohort | n | trig | W | L | closed | **WR_closed** (correct) | WR_all_setups (current display) | PF | netR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **All signals (all tiers, all modes)** | 117 | 89 | 19 | 40 | 59 | **32%** | 16% | 1.19 | +8R |
| **Actionable A/B only** | 117 | 89 | 19 | 40 | 59 | **32%** | 16% | 1.19 | +8R |
| Crypto A/B closed-triggered only | 89 | 89 | 19 | 40 | 59 | **32%** | 21% | 1.19 | +8R |

(Note: crypto has no C-tier in this window; "all signals" == "A/B only".)

## 2. Crypto by playbook (A/B closed)

| Playbook | n | trig | W | L | closed | **WR_closed** | PF | netR | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `crypto_swing_narrative_rs_momentum` (long) | 18 | 18 | 9 | 9 | 18 | **50%** | 2.22 | +11R | ✅ actionable (primary) |
| `crypto_intraday_catalyst_or_momentum` (catalyst=1) | 12 | 10 | 4 | 6 | 10 | **40%** | 1.83 | +5R | ✅ actionable |
| `crypto_intraday_catalyst_or_momentum` (no catalyst) | 24 | 18 | 3 | 14 | 17 | 18% | 0.50 | −7R | ⚠ weak (catalyst is the edge) |
| `crypto_failed_bounce_short` | 50 | 30 | 6 | 13 | 19 | **32%** | 1.38 | +5R | ✅ regime-dependent actionable |
| `crypto_scalp_momentum_continuation` | 58 | 38 | 0 | 9 | 9 | **0%** | 0.00 | −8R | ⚠ low-confidence (as documented) |

## 3. Stocks headline metrics

| Cohort | n | trig | W | L | closed | **WR_closed** (correct) | WR_all_setups (current display) | PF | netR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **All signals (all tiers, all modes)** | 643 | 505 | 100 | 223 | 323 | **31%** | 16% | 0.62 | −80R |
| **Actionable stocks intraday A/B only** | 161 | 128 | 47 | 49 | 96 | **49%** | 29% | 1.53 | +19R |
| Actionable A/B closed-triggered only | 128 | 128 | 47 | 49 | 96 | **49%** | 37% | 1.53 | +19R |

## 4. Stocks intraday by direction (A/B only — the playbook lane)

| Cohort | n | W | L | closed | **WR_closed** | PF | netR |
|---|---:|---:|---:|---:|---:|---:|---:|
| stocks_intraday_long (A/B) | 135 | 38 | 45 | 83 | **46%** | 1.34 | +11R |
| stocks_intraday_short (A/B) | 26 | 9 | 4 | 13 | **69%** | 3.00 | +8R |

## 5. Stocks intraday A-tier vs B-tier (A/B only)

| Tier | n | W | L | closed | **WR_closed** | netR | Comment |
|---|---:|---:|---:|---:|---:|---:|---|
| A | 28 | 4 | 15 | 19 | 21% | −6R | A-tier overpromotion symptom (warned in 14d audit) |
| B | 133 | 43 | 34 | 77 | **56%** | +25R | healthy B-tier edge |

## 6. Watchlist / counterfactual (C-tier, paused modes)

These are NOT Telegram-actionable. They appear here to validate the pause decisions.

| Cohort | n | trig | W | L | closed | **WR_closed** | netR | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| stocks_swing C (paused) | 145 | 136 | 14 | 68 | 82 | **17%** | −49R | ✅ pause justified by counterfactual |
| stocks_invest C (paused) | 111 | 103 | 2 | 44 | 46 | **4%** | −42R | ✅ pause STRONGLY justified |
| crypto C (watchlist) | 0 | — | — | — | — | — | — | empty in current window |

## 7. The user's "16% / 17%" — explained side by side

| What the user saw | Where in tab 10 | Why it's misleading | Correct interpretation |
|---|---|---|---|
| "stocks long 17%" | By-direction `stocks long: n=467 W=78 WR=17%` | n=467 mixes ALL tiers (A/B + C/watchlist) + ALL modes (intraday + paused swing + paused invest); denominator includes pending/expired/not_triggered | **stocks intraday A/B long WR = 46% (closed-only)** |
| "stocks intraday C 16%" | By-mode-tier `stocks intraday C n=226 W=37 WR=16%` | C-tier is watchlist; denominator includes pending/expired/not_triggered | **C-tier is NOT a tradable cohort**; this row should be flagged as counterfactual, not a "trading performance" number |
| "crypto WR around 16%" | likely from a crypto-all aggregate | denominator includes pending/expired/not_triggered | **crypto A/B closed WR = 32%** |

## 8. Mapping to playbooks

For an honest headline display, the actionable playbooks (with their corrected WRs) are:

| Status | Playbook | 14d-style WR_closed | netR |
|---|---|---:|---:|
| actionable primary | `crypto_swing_narrative_rs_momentum` | **50%** | +11R |
| actionable | `crypto_intraday_catalyst_or_momentum` (catalyst) | **40%** | +5R |
| actionable | `crypto_failed_bounce_short` | **32%** | +5R |
| low-confidence | `crypto_scalp_momentum_continuation` | 0% | −8R |
| actionable primary | `stocks_intraday_rth_momentum` (long) | **46%** | +11R |
| actionable | `stocks_intraday_rth_momentum` (short) | **69%** | +8R |
| watchlist-only (paused) | `stocks_swing_watchlist_rs_rotation` | 17% | −49R (counterfactual) |
| watchlist-only (paused) | `stocks_invest_watchlist_30d_thesis` | 4% | −42R (counterfactual) |

These match what tab 11 already shows correctly in §8b — confirming the bug is only in tab 10.

```
CORRECTED_WINRATES_COMPUTED
```
