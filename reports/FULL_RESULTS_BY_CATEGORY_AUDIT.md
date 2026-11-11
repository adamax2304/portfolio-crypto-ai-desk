# Full Results By Category — Audit (PART 1)

**Date:** 2026-06-11 · **Scope:** Read-only audit of all proposed_signals × latest signal_outcomes across 4 windows × 2 asset classes × 6 modes × 9 playbooks. Source-of-truth: production DB.

---

## 1. A/B-tier headline (sized R = playbook-aware weights)

### All-time (signal history 2026-05-22 → 2026-06-11)

| Asset | Mode | n | trig | W | L | Exp | WR | raw R | sized R | PF |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| crypto | scalp | 85 | 43 | 0 | 9 | 34 | 0% | −9.0 | **−4.5** | 0.00 |
| crypto | intraday | 52 | 38 | 7 | 29 | 2 | 19% | −10.0 | **−10.0** | 0.66 |
| crypto | swing | 38 | 35 | 16 | 17 | 2 | 48% | +19.0 | **+19.0** | 2.12 |
| stocks | intraday | 646 | 445 | 140 | 89 | 215 | 61% | **+135.0** | **+133.0** | 2.50 |
| stocks | swing (paused) | 54 | 51 | 6 | 39 | 6 | 13% | −32.0 | +0.0 | 0.18 |
| stocks | invest (paused) | 39 | 38 | 0 | 26 | 12 | 0% | −26.0 | +0.0 | 0.00 |
| **A/B total** | — | **914** | **650** | **169** | **209** | **271** | **45%** | **+77.0** | **+137.5** | — |

### 14-day window (2026-05-28 onwards)

| Asset | Mode | n | trig | W | L | Exp | WR | raw R | sized R |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| crypto | scalp | 77 | 37 | 0 | 8 | 29 | 0% | −8.0 | −4.0 |
| crypto | intraday | 47 | 34 | 7 | 25 | 2 | 22% | −6.0 | −6.0 |
| crypto | swing | 38 | 35 | 16 | 17 | 2 | 48% | +19.0 | +19.0 |
| stocks | intraday | 275 | 206 | 60 | 65 | 81 | 48% | +28.0 | +32.5 |
| stocks | swing | 54 | 51 | 6 | 39 | 6 | 13% | −32.0 | +0.0 |
| stocks | invest | 39 | 38 | 0 | 26 | 12 | 0% | −26.0 | +0.0 |

### 7-day window

| Asset | Mode | n | trig | W | L | WR | raw R | sized R |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| crypto | scalp | 46 | 14 | 0 | 1 | 0% | −1.0 | −0.5 |
| crypto | intraday | 31 | 20 | 6 | 14 | 30% | +2.0 | +2.0 |
| crypto | swing | 31 | 28 | 12 | 14 | 46% | +10.0 | +10.0 |
| stocks | intraday | 60 | 55 | 19 | 20 | 49% | +7.0 | +8.5 |
| stocks | swing | 7 | 7 | 0 | 5 | 0% | −5.0 | +0.0 |
| stocks | invest | 7 | 7 | 0 | 2 | 0% | −2.0 | +0.0 |

### 48-hour window (2026-06-10 → 2026-06-11)

| Asset | Mode | n | trig | W | L | raw R |
|---|---|---:|---:|---:|---:|---:|
| crypto | scalp | 23 | 3 | 0 | 0 | 0.0 |
| crypto | intraday | 19 | 12 | 2 | 10 | −6.0 |
| crypto | swing | 19 | 16 | 5 | 9 | +1.0 |
| stocks | intraday | 19 | 17 | 4 | 9 | −1.0 |

48h was rough across the board (BTC chop / range-bound stocks). 14-day window is healthier.

---

## 2. By playbook (all-time A/B)

| Playbook | n | W | L | WR | raw R | sized R | PF |
|---|---:|---:|---:|---:|---:|---:|---:|
| `stocks_intraday_rth_momentum` | 646 | 140 | 89 | 61% | +135.0 | **+133.0** | 2.50 |
| `crypto_swing_narrative_rs_momentum` | 33 | 13 | 15 | 46% | +12.0 | **+12.0** | 1.80 |
| `crypto_failed_bounce_short` | 24 | 7 | 10 | 41% | +11.0 | **+11.0** | 2.10 |
| `stocks_swing_watchlist_rs_rotation` | 54 | 6 | 39 | 13% | −32.0 | +0.0 (paused) | 0.18 |
| `stocks_invest_watchlist_30d_thesis` | 39 | 0 | 26 | 0% | −26.0 | +0.0 (paused) | 0.00 |
| `crypto_scalp_momentum_continuation` | 85 | 0 | 9 | 0% | −9.0 | **−4.5** (0.5×) | 0.00 |
| `crypto_intraday_catalyst_or_momentum` | 33 | 3 | 21 | 12% | −14.0 | **−14.0** | 0.33 |

`crypto_catalyst_backed_setup` and `crypto_rs_leader_long`: no signals in current window — labels exist in the playbook registry but no signal hit those branches.

---

## 3. Long vs short (A/B all-time triggered)

| Direction | n trig | W | L | WR | raw R |
|---|---:|---:|---:|---:|---:|
| long | 480 | 145 | 153 | 49% | +101 |
| short | 170 | 24 | 56 | 30% | −24 |

Longs are positive; shorts are net negative. Shorts that work (`crypto_failed_bounce_short` PF 2.10) are isolated; bulk shorts in `crypto_intraday_catalyst_or_momentum` lose.

---

## 4. Catalyst-supported vs not (A/B all-time triggered)

| Catalyst | n trig | W | L | WR | raw R |
|---|---:|---:|---:|---:|---:|
| `news_supported=1` | 218 | 70 | 73 | 49% | +44 |
| `news_supported=0` | 432 | 99 | 136 | 42% | +33 |

Catalyst presence gives WR uplift of ~7pp. Not huge but real. The big winners (stocks intraday B-tier momentum) often don't require explicit catalyst tag.

---

## 5. A-tier vs B-tier (triggered, all-time)

| Tier | n trig | W | L | WR | raw R | sized R |
|---|---:|---:|---:|---:|---:|---:|
| A | 100 | 28 | 36 | 44% | +5 | **+2.5** (half-size on A-long mitigates) |
| B | 550 | 141 | 173 | 45% | +72 | +135 |

A-tier doesn't actually beat B-tier OOS — the sizing layer is correctly half-sizing A-tier long stocks.

---

## 6. Execution-quality flags (from `signal_outcomes.notes`)

| Flag | Count | Notes |
|---|---:|---|
| `intrabar_entry_stop` | 3 | very rare; flagged honestly |
| `ambiguous_intrabar` | 26 | mostly stocks intraday; sized R impact +19 |
| `gap_slip_stop` / `gap_slip_tp` | 90 | mostly stocks; net positive (+71.5R sized) — gaps tend to favor us |
| `pre_entry_invalidation` | 60+ | working as designed (no fill) |

Execution flags are well-distributed; no systemic bias toward losing fills.

---

## 7. What this audit shows

- **Stocks intraday** is the engine: 60%+ WR, PF 2.50, +133R sized. Whatever the playbook does, it works. Don't touch.
- **Crypto swing** is the second engine: 48% WR, PF 2.12, +19R sized. Working.
- **Crypto failed-bounce shorts** are clean: PF 2.10, +11R sized. Working.
- **Crypto intraday catalyst** is the worst non-paused cohort: 12% WR, PF 0.33, −14R sized. Mostly losing shorts.
- **Crypto scalp** is a flat 0% WR on 9 closed trades; the 34 expired carry zero R. Sizing 0.5× mitigates; need 1m data to study exits properly.
- **Stocks swing/invest** are correctly paused (sizing 0×); raw R confirms the pause is right.
