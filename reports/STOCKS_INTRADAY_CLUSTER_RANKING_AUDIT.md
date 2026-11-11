# Stocks Intraday Cluster Ranking (PART 4 — additive only)

**Date:** 2026-06-14 11:11 UTC
**Scope:** stocks intraday A/B last 14d (n=332).
**Behavior:** ranking only — no signal is suppressed.

## Cluster-day summary (last 14d, ≥ 3 same-direction signals only)

| Day | Cluster | Dir | n | best 1 (rank score) | best 3 (top syms) | cluster R | cluster risk |
|---|---|---|---:|---|---|---:|---|
| 2026-05-28 | ai_infra | long | 13 | SMCI (78.0) | SMCI, SMCI, SMCI | +18.0 | MEDIUM |
| 2026-05-28 | mega_tech | long | 21 | AAPL (88.2) | AAPL, AAPL, AAPL | -2.0 | MEDIUM |
| 2026-05-28 | semis | long | 34 | AMD (84.6) | AMD, XLK, XLK | +35.0 | MEDIUM |
| 2026-05-29 | ai_infra | long | 17 | AVGO (82.6) | AVGO, AVGO, SMCI | -2.0 | MEDIUM |
| 2026-05-29 | index_etfs | long | 3 | QQQ (81.8) | QQQ, QQQ, QQQ | +0.0 | LOW |
| 2026-05-29 | mega_tech | long | 38 | AAPL (86.4) | AAPL, AAPL, AAPL | -5.0 | MEDIUM |
| 2026-05-29 | semis | long | 52 | AMD (86.0) | AMD, AMD, AMD | -11.0 | MEDIUM |
| 2026-05-31 | mega_tech | long | 4 | AAPL (86.4) | AAPL, MSFT, AVGO | +3.0 | MEDIUM |
| 2026-05-31 | semis | long | 5 | AMD (88.0) | AMD, XLK, AVGO | +4.0 | LOW |
| 2026-06-01 | ai_infra | long | 21 | NVDA (85.7) | NVDA, NVDA, AVGO | +19.0 | MEDIUM |
| 2026-06-01 | mega_tech | long | 36 | AAPL (86.4) | AAPL, AAPL, AAPL | +19.0 | MEDIUM |
| 2026-06-01 | semis | long | 48 | AMD (88.0) | AMD, AMD, AMD | +35.0 | MEDIUM |
| 2026-06-02 | ai_infra | long | 4 | NVDA (87.7) | NVDA, SMCI, NVDA | -2.0 | LOW |
| 2026-06-02 | mega_tech | long | 6 | NVDA (87.7) | NVDA, AAPL, MSFT | -3.0 | MEDIUM |
| 2026-06-02 | semis | long | 8 | AMD (87.7) | AMD, NVDA, AMD | +0.0 | MEDIUM |
| 2026-06-03 | ai_infra | long | 4 | NVDA (86.0) | NVDA, SMCI, SMCI | -2.0 | LOW |
| 2026-06-03 | mega_tech | long | 5 | AAPL (93.0) | AAPL, NVDA, AAPL | -3.0 | LOW |
| 2026-06-03 | semis | long | 9 | AMD (90.5) | AMD, AMD, NVDA | -5.0 | MEDIUM |
| 2026-06-04 | mega_tech | long | 3 | AVGO (89.7) | AVGO, NVDA, AAPL | +0.0 | LOW |
| 2026-06-04 | semis | long | 6 | AVGO (89.7) | AVGO, AMD, AMD | -1.0 | MEDIUM |
| 2026-06-05 | mega_tech | short | 5 | META (85.5) | META, TSLA, AMZN | +5.0 | LOW |
| 2026-06-05 | semis | short | 4 | AMD (77.9) | AMD, NVDA, SMH | +1.0 | LOW |
| 2026-06-09 | mega_tech | short | 8 | MSFT (79.0) | MSFT, TSLA, AMZN | +5.0 | MEDIUM |
| 2026-06-10 | mega_tech | short | 3 | MSFT (83.2) | MSFT, PLTR, TSLA | +3.0 | LOW |
| 2026-06-11 | mega_tech | short | 4 | MSFT (82.7) | MSFT, GOOGL, META | -3.0 | LOW |

## Current top cluster (most recent day: 2026-06-12)

- **semis / long** — top 3: AMD, AMD

## Behavior

- This audit is **additive only**. No alert is suppressed.
- Dashboards may display `cluster rank #N/M` and `cluster risk: high/medium/low` per signal.
- Operator can use the rank as a manual sizing hint; the system never enforces it.