# Stocks Position Framework — stocks_swing_growth_breakout (shadow research)

> **SHADOW ONLY — research candidates.** No actionability · no live / auto-live / manual-live · no Telegram · not sized in the paper book. The old stocks swing/invest playbooks (`stocks_swing_watchlist_rs_rotation`, `stocks_invest_watchlist_30d_thesis`) are **deprecated/removed** — not paused-to-return. Authoritative profitability = **USD net PnL**; legacy final_r is diagnostic only.

- Scan time (UTC): `2026-09-30T13:26:29.945328+00:00`
- Universe: 68 · scanned: 68 · candidates: **0** · rejected: 68
- Market regime: **risk_on** · SPY>50D=True · SPY>200D=True · QQQ>50D=True · VIX=15.8

### Candidates

_No qualifying candidates in the latest scan._

### Rejected (sample)

- AAPL: sector RS negative vs SPY, volume ratio 0.90 < 1.1
- MSFT: sector RS negative vs SPY, volume ratio 1.00 < 1.1
- ORCL: sector RS negative vs SPY, below 50D SMA, below 200D SMA
- CRM: sector RS negative vs SPY, volume ratio 1.01 < 1.1, 16.0% below nearest 3M/6M/52W high (> 12%)
- ADBE: sector RS negative vs SPY, below 50D SMA, below 200D SMA
- ACN: sector RS negative vs SPY, below 200D SMA
- CSCO: sector RS negative vs SPY, below 50D SMA, RS vs SPY not positive
- IBM: sector RS negative vs SPY, below 50D SMA, below 200D SMA
- NOW: sector RS negative vs SPY, volume ratio 0.73 < 1.1, 13.1% below nearest 3M/6M/52W high (> 12%)
- INTU: sector RS negative vs SPY, below 50D SMA, below 200D SMA
- TXN: sector RS negative vs SPY, RS vs SPY not positive, volume ratio 0.83 < 1.1
- QCOM: sector RS negative vs SPY, RS vs SPY not positive, volume ratio 0.67 < 1.1

### Runbook / status (forward-audit)

- scheduler_enabled: **True**
- latest scan (UTC): `2026-09-30T13:26:29.945328+00:00`
- candidates stored (open): **13**
- outcomes: closed **27** · pending **13** · no-entry **2**
- ⚠️ sample too small: 27 closed < 30 required for any read.

> **No profitability conclusion** until ≥30 forward candidates have resolved through the outcome engine in **USD net**. Backfill is not proof.

### Outcomes

> USD net is authoritative; `paper_execution_r` is auxiliary. Rows with NULL PnL are still open/pending (not zero).

**USD net (closed n=27):** total $-117.96 · avg $-4.37 · winrate 26% · PF 0.324

| Candidate | Status | Net $ | Paper-exec R | MFE R | MAE R | Hold d |
|---|---|---:|---:|---:|---:|---:|
| spf_MSFT_2026-08-05 | pending | — | — | 0.59 | -0.35 | 38 |
| spf_JNJ_2026-08-11 | pending | — | — | 1.37 | -0.41 | 34 |
| spf_XOM_2026-08-11 | pending | — | — | 0.86 | -0.47 | 34 |
| spf_MRK_2026-08-19 | pending | — | — | 1.91 | -0.89 | 28 |
| spf_XOM_2026-08-26 | pending | — | — | 1.91 | -0.44 | 23 |
| spf_TMO_2026-09-08 | pending | — | — | 3.03 | -0.28 | 15 |
| spf_ABBV_2026-09-18 | pending | — | — | 0.46 | -0.16 | 7 |
| spf_MRK_2026-09-18 | pending | — | — | 1.27 | -0.24 | 7 |
| spf_CVX_2026-09-22 | pending | — | — | 1.06 | -0.18 | 5 |
| spf_TMO_2026-09-22 | pending | — | — | 0.81 | -0.15 | 5 |
| spf_DIS_2026-09-25 | pending | — | — | 0.43 | -0.20 | 2 |
| spf_LLY_2026-09-25 | pending | — | — | 0.96 | -0.13 | 3 |
| spf_MSFT_2026-09-25 | pending | — | — | 1.95 | -0.31 | 3 |
| spf_COP_2026-08-11 | closed | 3.11 | — | 2.03 | -0.01 | 29 |
| spf_V_2026-08-17 | closed | 1.22 | — | 1.42 | -0.27 | 25 |
| spf_CVX_2026-09-14 | closed | -12.74 | — | 0.52 | -1.04 | 6 |
| spf_COP_2026-09-17 | closed | -12.12 | — | 0.47 | -1.61 | 3 |
| spf_KO_2026-09-01 | closed | -5.99 | — | 0.49 | -0.45 | 14 |
| spf_MA_2026-08-19 | closed | 0.36 | — | 2.21 | -0.12 | 22 |
| spf_WFC_2026-09-01 | closed | 2.04 | — | 1.77 | -0.13 | 11 |
| spf_BAC_2026-08-21 | closed | -12.99 | — | 1.26 | -1.78 | 16 |
| spf_JPM_2026-09-01 | closed | -12.88 | — | 0.92 | -1.10 | 9 |
| spf_MRK_2026-08-03 | closed | 29.56 | — | 3.44 | -0.18 | 27 |
| spf_BLK_2026-08-21 | closed | -12.75 | — | 0.86 | -1.25 | 13 |
| spf_ABT_2026-09-01 | closed | -12.73 | — | 0.61 | -1.23 | 7 |
| spf_ABBV_2026-09-07 | closed | -2.98 | — | 0.30 | -0.37 | 0 |
| spf_ABBV_2026-08-05 | closed | 19.51 | — | 2.24 | -0.25 | 17 |
| spf_GS_2026-08-26 | closed | -4.17 | — | 0.06 | -0.38 | 0 |
| spf_LLY_2026-08-06 | closed | 0.72 | — | 1.74 | -0.12 | 14 |
| spf_LLY_2026-08-19 | closed | -7.82 | — | 0.61 | -0.97 | 6 |
| spf_JPM_2026-08-24 | no_entry | — | — | — | — | 0 |
| spf_PANW_2026-08-05 | closed | -9.03 | — | 0.83 | -0.73 | 14 |
| spf_RTX_2026-08-20 | closed | -12.76 | — | 0.58 | -1.00 | 2 |
| spf_GE_2026-08-19 | closed | -6.29 | — | 0.63 | -0.80 | 1 |
| spf_CSCO_2026-08-12 | closed | -11.33 | — | 0.19 | -1.29 | 1 |
| spf_CSCO_2026-08-05 | closed | -15.72 | — | 0.07 | -1.17 | 6 |
| spf_AAPL_2026-07-06 | no_entry | — | — | — | — | — |
| spf_GS_2026-08-05 | closed | -3.14 | — | 0.18 | -0.26 | 0 |
| spf_MS_2026-08-05 | closed | -2.75 | — | 0.17 | -0.22 | 0 |
| spf_UNH_2026-07-17 | closed | -6.93 | — | 1.37 | -0.59 | 13 |
| spf_AAPL_2026-07-05 | closed | -3.30 | — | 1.76 | -0.32 | 19 |
| spf_MS_2026-07-17 | closed | -6.06 | — | 0.74 | -0.83 | 7 |


### Promotion / evidence gate (NOT met — shadow only)

- min forward days: 28
- min forward trades: 30
- require net USD positive: True
- require better than old stocks swing: True
- require drawdown acceptable: True

Nothing here becomes actionable/live until this gate passes on FORWARD data **and** the operator signs off. Backfill is not proof.
