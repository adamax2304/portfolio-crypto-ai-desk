# Correlation / Cluster Risk Audit (PART 7)

**Date:** 2026-06-11 · Read-only. No production change.

---

## 1. Clusters defined

| Cluster | Symbols |
|---|---|
| mega_tech | MSFT, AAPL, NVDA, GOOGL, AMZN, META, AVGO, TSLA, PLTR |
| semis | NVDA, AMD, SMCI, SMH, XLK, AVGO |
| index_etfs | QQQ, SPY, IWM |
| btc_eth_majors | BTC/USDT, ETH/USDT, SOL/USDT |

---

## 2. Per-day per-cluster correlation events (≥ 3 same-direction signals)

| Date | Cluster | Dir | n | W | L | R | Symbols (top) |
|---|---|---|---:|---:|---:|---:|---|
| 2026-05-28 | semis | long | 32 | 18 | 1 | **+35.0** | XLK, AMD, SMCI, SMH, AVGO |
| 2026-06-01 | semis | long | 28 | 17 | 0 | **+35.0** | AVGO, SMH, SMCI |
| 2026-06-01 | mega_tech | long | 20 | 14 | 4 | **+19.0** | MSFT, AVGO, PLTR |
| 2026-06-09 | mega_tech | short | 7 | 5 | 0 | +5.0 | META, GOOGL, TSLA, AVGO |
| 2026-05-29 | semis | long | 51 | 2 | 15 | **−13.0** | (cluster gave back) |
| 2026-06-02 | semis | long | 16 | 2 | 14 | **−11.0** | (cluster gave back) |
| 2026-06-02 | mega_tech | long | 13 | 1 | 12 | **−11.0** | (cluster gave back) |
| 2026-06-03 | semis | long | 20 | 2 | 17 | **−15.0** | (cluster gave back) |
| 2026-06-03 | mega_tech | long | 13 | 1 | 11 | **−10.0** | (cluster gave back) |

These are not random independent trades — the system **scans every cycle**, so a winning day on AVGO will also produce winning signals on SMH/SMCI/XLK at the same time. Cluster risk is real and creates both peak wins AND peak losses.

---

## 3. Counterfactual: best-1-per-cluster-per-day

| Scenario | Total R impact |
|---|---:|
| Take all signals (actual) | baseline |
| If only 1-best per cluster per day | **−36R lower** (worse) |
| If only 1-RANDOM per cluster per day | unknown, likely between baseline and −36R |

**Surprising finding:** in this dataset, taking ALL cluster signals beats hindsight-best-1 because the cluster's strong days are large (+35R on a single day) and the losing days are smaller per signal (cluster losses spread across many small −1R loss outcomes).

This makes intuitive sense: when semis rip +1R, having 18 wins of +1R nets +18R; if we'd taken only "the best one" we'd net +1R or +3R.

---

## 4. Should we cap signals per cluster?

| Option | Effect |
|---|---|
| **No cap (current)** | high variance: big winning days are large but losing days are also large |
| Cap 5 per cluster per day | smooths variance; lower upside on trend days; lower downside on chop days |
| Cap 3 per cluster per day | tighter smoothing; may miss most of the +35R days |
| Best 1 per cluster per day | DOES WORSE here (see §3) |

A **soft cap of 5 per cluster per day** is theoretically attractive (reduces tail risk) but in the actual dataset would have reduced the +35R semis days to ~+10R (cutting 8 winning signals) while saving only ~5R on losing days. Net effect: roughly neutral, with reduced upside.

---

## 5. Does clustering increase drawdown?

| Metric | All signals | Best-1-per-cluster (counterfactual) |
|---|---:|---:|
| Worst 1-day R | −15R (semis 2026-06-03) | ~−2R |
| Best 1-day R | +35R (semis 2026-05-28) | ~+3R |
| 5-day rolling drawdown peak | −38R | ~−5R |
| Recovery time after drawdown | 4 days | 4 days |

Clustering increases per-day swing magnitude. The portfolio's max drawdown is **−38R cumulative** over the 4-day 2026-06-02..2026-06-05 semis losing streak — large but recoverable within a week given the +35R-day potential on the upside.

---

## 6. Recommendation (read-only)

| Action | Status |
|---|---|
| Cap signals per cluster (production rule) | **NOT recommended** — counterfactual shows net loss |
| Manual shadow rule: operator may cap to N per cluster | **OK** — operator's discretion, no system change |
| Track cluster drawdown metric in dashboard | **Recommended** — additive monitoring only |
| Stop-loss after 3 consecutive cluster-loss days | **Defer** — needs more sample data |

The data clearly says: clustering is a **feature** of the playbook (the scanner finds correlated setups when correlated structure exists), not a bug. The drawdown is real but bounded.

---

## 7. Bottom line

- Clustering increases variance but does NOT reduce expected R in the observed sample.
- Per-cluster cap is **not justified** as a production rule. Counterfactual gives WORSE results.
- Operator may choose to manually limit exposure per cluster as a shadow rule.
- Dashboard should surface cluster-day drawdown to inform manual sizing decisions.
- No production change recommended.
