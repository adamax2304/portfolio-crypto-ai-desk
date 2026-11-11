# 📌 Performance by Mode / Tier

_Refreshed: **2026-11-11 16:51 EEST** · Source: `proposed_signals` × latest `signal_outcomes` per signal_id._

> **Headline WR excludes** `waiting_for_entry`, `stale_before_entry`, `entry_moved_away`, `not_triggered`, `expired`, C-tier / watchlist, and shadow candidates. **WR = Wins ÷ (Wins + Losses)**.

---

## 🎯 Headline (actionable A/B, closed-only)

_`netR` below is LEGACY TOUCH R (optimistic highest-TP-touched) — **NOT PnL**. Authoritative PnL is
USD net (`paper_portfolio_ledger.net_pnl_usdt`) and realistic R is `paper_execution_r` in the app._

| Cohort | n | Triggered | Wins | Losses | Closed | **WR** | netR (legacy touch) |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Crypto A/B (all modes, closed)** | 2654 | 2437 | 493 | 1201 | 1694 | **29%** | -40R |
| **Stocks intraday A/B (closed)** | 1146 | 704 | 91 | 136 | 227 | **40%** | +49R |

_Old stocks swing & invest are DEPRECATED/REMOVED (not paused-to-return) and **not included** in the stocks headline. The new `stocks_swing_growth_breakout` is a separate shadow-only research lane, also excluded from the headline._

---

## 📊 Actionable A/B — by asset class × mode × tier

| Asset | Mode | Tier | n | Trig | Pend* | W | L | Closed | **WR (closed)** | Avg R | Total R |
|-------|------|------|--:|----:|----:|----:|----:|----:|---:|------:|--------:|
| crypto | intraday | **B** | 1026 | 959 | 131 | 253 | 642 | 895 | 28% | -0.04 | -38.00 |
| crypto | scalp | **A** | 3 | 2 | 2 | 0 | 1 | 1 | 0% | -0.33 | -1.00 |
| crypto | scalp | **B** | 608 | 496 | 496 | 5 | 107 | 112 | 4% | -0.15 | -91.50 |
| crypto | swing | **A** | 1 | 1 | 0 | 1 | 0 | 1 | 100% | +3.00 | +3.00 |
| crypto | swing | **B** | 1016 | 979 | 331 | 234 | 451 | 685 | 34% | +0.09 | +87.00 |
| stocks | intraday | **A** | 126 | 87 | 92 | 13 | 21 | 34 | 38% | +0.06 | +7.08 |
| stocks | intraday | **B** | 1020 | 617 | 827 | 78 | 115 | 193 | 40% | +0.04 | +41.52 |
| stocks | invest | **A** | 2 | 2 | 1 | 0 | 1 | 1 | 0% | -0.50 | -1.00 |
| stocks | invest | **B** | 36 | 36 | 3 | 6 | 27 | 33 | 18% | -0.58 | -21.00 |
| stocks | swing | **A** | 10 | 10 | 3 | 0 | 7 | 7 | 0% | -0.70 | -7.00 |
| stocks | swing | **B** | 58 | 55 | 18 | 5 | 35 | 40 | 12% | -0.50 | -29.00 |

---

## 📊 Actionable A/B — by direction

| Asset | Tier | Direction | n | Pend* | W | L | Closed | **WR (closed)** | Avg R | Total R |
|-------|------|-----------|--:|----:|----:|----:|----:|---:|------:|--------:|
| crypto | **A** | long | 4 | 2 | 1 | 1 | 2 | 50% | +0.50 | +2.00 |
| crypto | **B** | long | 2453 | 883 | 457 | 1113 | 1570 | 29% | -0.01 | -36.50 |
| crypto | **B** | short | 197 | 75 | 35 | 87 | 122 | 29% | -0.03 | -6.00 |
| stocks | **A** | long | 97 | 63 | 6 | 28 | 34 | 18% | -0.13 | -12.92 |
| stocks | **A** | short | 41 | 33 | 7 | 1 | 8 | 88% | +0.29 | +12.00 |
| stocks | **B** | long | 572 | 385 | 38 | 149 | 187 | 20% | -0.12 | -69.48 |
| stocks | **B** | short | 542 | 463 | 51 | 28 | 79 | 65% | +0.11 | +61.00 |

---

## 🔬 Watchlist / Counterfactual (C-tier, paused modes — NOT trading performance)

These rows show what watchlist setups would have done if actionable — they validate the pause decisions for stocks_swing and stocks_invest. **They are not Telegram-actionable** and should not be read as "the system is losing".

| Asset | Mode | Tier | n | Trig | Pend* | W | L | Closed | WR (closed) | Avg R | Total R |
|-------|------|------|--:|----:|----:|----:|----:|----:|---:|------:|--------:|
| stocks | intraday | **C** | 7953 | 1618 | 7156 | 207 | 590 | 797 | 26% | -0.03 | -219.40 |
| stocks | invest | **C** | 201 | 201 | 98 | 48 | 55 | 103 | 47% | -0.01 | -2.00 |
| stocks | swing | **C** | 254 | 253 | 106 | 58 | 90 | 148 | 39% | -0.04 | -11.00 |

### By direction (watchlist)

| Asset | Tier | Direction | n | Pend* | W | L | Closed | WR (closed) | Avg R | Total R |
|-------|------|-----------|--:|----:|----:|----:|----:|---:|------:|--------:|
| stocks | **C** | long | 4152 | 3544 | 185 | 423 | 608 | 30% | -0.03 | -135.40 |
| stocks | **C** | short | 4256 | 3816 | 128 | 312 | 440 | 29% | -0.02 | -97.00 |


---

## 💰 Raw R vs Sized R (playbook-aware reporting layer)

> Reporting/paper-PnL annotation only — does **not** influence signal generation, scoring, TP/SL, alerts, or `signal_outcomes`. Weights: `config/sizing_weights.yaml`. Logic: `src/signals/sizing.py`. Audit: [reports/PROFITABILITY_LEVERS_AUDIT.md].

### Portfolio totals (deduped per-setup, all-time)

| Metric | equal 1× (raw) | playbook-aware (sized) |
|---|---:|---:|
| Total R | **-282.3R** | **+103.1R** |
| n setups | 12314 | 3189 (sized > 0) |
| Wins (sized > 0) | — | 579 |
| Losses (sized < 0) | — | 1229 |
| WR (sized closed) | — | 32.0% |
| PF (sized) | — | 1.09 |

### By-playbook contribution

| Playbook | weight(s) | n | n_sized | W | L | rawR | **sizedR** |
|---|---:|---:|---:|---:|---:|---:|---:|
| `crypto_swing_narrative_rs_momentum` | 1.0× | 966 | 966 | 221 | 423 | +86.0 | **+86.0** |
| `stocks_intraday_rth_momentum` | 0.0×, 0.5×, 1.0× | 9099 | 1146 | 91 | 136 | -170.8 | **+51.1** |
| `crypto_failed_bounce_short` | 1.0× | 130 | 130 | 35 | 72 | +9.0 | **+9.0** |
| `crypto_scalp_momentum_continuation` | 0.0× | 611 | 0 | 0 | 0 | -92.5 | **+0.0** |
| `stocks_invest_watchlist_30d_thesis` | 0.0× | 239 | 0 | 0 | 0 | -24.0 | **+0.0** |
| `stocks_swing_watchlist_rs_rotation` | 0.0× | 322 | 0 | 0 | 0 | -47.0 | **+0.0** |
| `crypto_intraday_catalyst_or_momentum` | 1.0× | 947 | 947 | 232 | 598 | -43.0 | **-43.0** |

### Top positive contributors (sized)

- `crypto_swing_narrative_rs_momentum` — sizedR **+86.0R** (weights 1.0×, n_sized=966)
- `stocks_intraday_rth_momentum` — sizedR **+51.1R** (weights 0.0×, 0.5×, 1.0×, n_sized=1146)
- `crypto_failed_bounce_short` — sizedR **+9.0R** (weights 1.0×, n_sized=130)

### Top negative contributors (sized)

- `crypto_intraday_catalyst_or_momentum` — sizedR **-43.0R** (weights 1.0×, n_sized=947)

### Sizing notes

- `crypto_scalp_momentum_continuation`: 0.5× (low-confidence; TP/horizon mismatch).
- `stocks_intraday_rth_momentum` A-tier long: 0.5× (A-tier overpromotion symptom).
- `stocks_swing_watchlist_rs_rotation` + `stocks_invest_watchlist_30d_thesis`: **0×** (DEPRECATED/REMOVED; never sized; not paused-to-return).
- `stocks_swing_growth_breakout`: **0×** (NEW shadow-only research framework; separate; not actionable/sized).
- C-tier / watchlist / shadow: **0×** (informational only).
- All other playbooks at 1.0×.
- Raw R is **never modified**; this section only shows what the portfolio R would be under sizing discipline.

---

## Column meanings

- **n** — unique setups (`(asset, mode, tier, direction, symbol, day)` tuple). Duplicate signal_ids collapse to one row.
- **Trig / Triggered** — setups where price reached the entry zone (`entry_triggered=1` on at least one duplicate signal_id).
- **Pend*** — setups still pending / expired / not_triggered (= `n − Closed`). Excluded from WR by design.
- **W** (Wins) — closed setups with positive average R across duplicate signal_ids.
- **L** (Losses) — closed setups with negative average R.
- **Closed** — `W + L`. The denominator for WR.
- **WR** — `Wins ÷ Closed × 100`. **Closed-only**, never depressed by pending/expired/not_triggered.
- **Avg R / Total R** — these are the **LEGACY TOUCH R** (old `final_r` = highest-TP-touched,
  OPTIMISTIC) per setup / cumulative. **NOT PnL.** Kept for signal-quality only.
- **Authoritative profitability = USD net** (gross − exchange fees − slippage − funding) from
  `paper_portfolio_ledger.net_pnl_usdt`; realistic R = `paper_execution_r` — both in the
  control-plane app. The R columns on this page are the legacy touch metric, never PnL.

A bucket with **Avg R ≥ +0.5** and **Closed ≥ 30** is usually a stronger signal-quality read (still
legacy-touch, not PnL). Anything below 30 closures is "weak confidence" — don't lean on it yet.

### Why the 2026-06-10 fix changed the numbers
Prior to today this dashboard computed `WR = Wins ÷ n` where `n` included pending/expired/not_triggered. That depressed every WR by a factor of (Closed/n) and produced misleading "16-17%" headlines. The corrected formula uses `Closed` in the denominator so a 0/9 scalp now reads `0%` while a 9/18 swing reads `50%` — matching tab 11's `## 8b. Playbook Performance Snapshot`.

⚠️ **Note vs CLI `signal-stats`**: that tool counts raw signal_ids (inflated). This dashboard counts unique setups (deflated, honest). Numbers will differ — trust this dashboard for edge-checking, use the CLI for raw signal-row inspection.

_File generated automatically by `scripts/refresh_obsidian_dashboard.py`._
