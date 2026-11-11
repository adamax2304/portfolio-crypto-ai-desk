# Demoted / Loss-Making Regime Repair Audit

- DB: `C:\Users\adama\Documents\crypto-ai-desk\db\crypto_ai_desk.sqlite`
- Window: last 45 days from `2026-07-31T19:27:53.704936+00:00`
- Scope: regimes demoted from live to Paper plus still-live regimes with negative live evidence.

## Executive Table

| regime | status | paper closed | paper R | paper PF | live closed | live net USD | low-MFE live losses | decision |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Crypto Swing BREAKOUT_CONTINUATION | demoted to Paper-only | 109 | 69.52 | 3.67 | 40 | -18.12 | 18 | keep Paper-only; build reclaim/hold v2 |
| Crypto Swing PULLBACK_LIMIT + confirmed pullback branches | live disabled; v2 Paper branches active | 524 | 165.97 | 1.92 | 33 | -21.27 | 18 | disable raw pullback; test confirmed-retest/fib only |
| Crypto Intraday BREAKOUT_CONTINUATION | Paper-only; old live evidence negative | 135 | 72.84 | 2.16 | 22 | -32.01 | 13 | keep Paper-only; require volume+BTC+level hold v2 |
| Crypto Swing LIMIT_THEN_TAKER_TIMEOUT | still live canary; included because live is negative and should not be scaled | 109 | 116.93 | 7.88 | 9 | -5.12 | 3 | keep $5 canary only; add loser-veto before scaling |
| Crypto Intraday LEVEL_HOLD_V2 | live canary route enabled but mostly no fills; candidate route needs readiness check | 48 | 29.30 | 2.72 | 0 | 0.00 | 0 | canary candidate; fix route/fill sample before scaling |
| Stocks Intraday BREAKOUT_CONTINUATION | still live but recently hardened; included as loss-driver | 22 | -2.15 | 0.25 | 46 | -24.94 | 16 | keep only hardened live; compare post-filter sample |
| Stocks Intraday PULLBACK_LIMIT/VWAP | Paper-only | 17 | -1.00 | 0.00 | 0 | 0.00 | 0 | Paper-only; needs stronger candle/sector filter |

## Crypto Swing BREAKOUT_CONTINUATION

- Current state: demoted to Paper-only

### Paper summary

| metric | value |
|---|---:|
| n | 117 |
| closed | 109 |
| wins | 36 |
| losses | 26 |
| sum_r | 69.52 |
| pf | 3.6738 |
| wr | 0.3303 |
| low_mfe_losses | 23 |

### Live summary

| metric | value |
|---|---:|
| n | 116 |
| closed | 40 |
| wins | 18 |
| losses | 22 |
| net_usd | -18.12 |
| pf | 0.7087 |
| wr | 0.4500 |
| low_mfe_losses | 18 |
| avg_live_paper_delta_r | -0.4049 |

### Paper breakdowns

| slice | closed | wins | losses | sum R | PF | low-MFE losses |
|---|---:|---:|---:|---:|---:|---:|
| entry:BREAKOUT_CONTINUATION | 109 | 36 | 26 | 69.52 | 3.67 | 23 |
| direction:long | 105 | 33 | 25 | 65.72 | 3.63 | 22 |
| direction:short | 4 | 3 | 1 | 3.80 | 4.80 | 1 |
| setup:pullback | 98 | 32 | 23 | 63.92 | 3.78 | 20 |
| setup:breakout | 7 | 1 | 2 | 1.80 | 1.90 | 2 |
| setup:breakdown | 4 | 3 | 1 | 3.80 | 4.80 | 1 |
| close:expired_flat | 36 | 0 | 0 | 0.00 | n/a | 0 |
| close:original_stop | 26 | 0 | 26 | -26.00 | 0.00 | 23 |
| close:profit_lock_stop | 22 | 22 | 0 | 11.00 | n/a | 0 |
| close:tp3_runner | 14 | 14 | 0 | 84.52 | n/a | 0 |
| close:breakeven_stop | 11 | 0 | 0 | 0.00 | n/a | 0 |
| close:open | 0 | 0 | 0 | 0.00 | n/a | 0 |
| close:no_entry | 0 | 0 | 0 | 0.00 | n/a | 0 |

### Live breakdowns

| slice | closed | wins | losses | net USD | PF | low-MFE losses | avg delta R |
|---|---:|---:|---:|---:|---:|---:|---:|
| venue:mexc | 37 | 16 | 21 | -18.42 | 0.69 | 17 | -0.42 |
| venue:bybit | 3 | 2 | 1 | 0.31 | 1.13 | 1 | -0.27 |
| venue:none | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| direction:long | 38 | 16 | 22 | -25.27 | 0.59 | 18 | -0.42 |
| direction:short | 2 | 2 | 0 | 7.15 | n/a | 0 | 0.18 |
| direction:unknown | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| setup:pullback | 37 | 15 | 22 | -26.58 | 0.57 | 18 | -0.44 |
| setup:breakdown | 2 | 2 | 0 | 7.15 | n/a | 0 | 0.18 |
| setup:breakout | 1 | 1 | 0 | 1.31 | n/a | 0 | 0.39 |
| setup:unknown | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:SUBMITTED | 40 | 18 | 22 | -18.12 | 0.71 | 18 | -0.40 |
| state:REJECTED | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED_PREFLIGHT | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED_SUBMISSION | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED_STALE_QUEUE | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED_RISK_LIMIT | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:SUBMISSION_NOT_SENT_WAF_DENIED | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:SUBMISSION_NOT_SENT_INVALID_ENDPOINT | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |

### Worst live examples

| captured | symbol | dir | setup | pnl | MFE R | paper R | venue |
|---|---|---|---|---:|---:|---:|---|
| 2026-09-04T05:29 | ADA/USDT | long | pullback | -4.91 | 0.50 | 0.00 | mexc |
| 2026-09-08T21:00 | XPL/USDT | long | pullback | -4.90 | 0.49 | 0.00 | mexc |
| 2026-09-06T03:00 | UNI/USDT | long | pullback | -4.87 | 0.37 | 0.00 | mexc |
| 2026-09-12T17:39 | ETHFI/USDT | long | pullback | -4.85 | 0.16 | -1.00 | mexc |
| 2026-08-04T15:03 | TUT/USDT | long | pullback | -4.61 | 0.58 | 0.00 | mexc |
| 2026-08-21T19:40 | TUT/USDT | long | pullback | -4.54 | 0.44 | 0.00 | mexc |
| 2026-08-06T03:00 | KITE/USDT | long | pullback | -4.33 | 0.58 | 0.00 | mexc |
| 2026-08-25T07:00 | PROM/USDT | long | pullback | -4.21 | 0.15 | 0.00 | mexc |

### Repair proposal

- Do not re-enable current route. The negative live delta and low-MFE long losses mean live entry quality is worse than Paper.
- Create `crypto_swing_breakout_reclaim_v2`: require 15m/1h level reclaim/hold after trigger, not just breakout touch.
- Make it asymmetric: long side needs BTC 1h/4h not down, OI/funding not crowded, and no first-candle rejection; short side can use separate lower threshold because recent closed shorts were stronger.
- Use venue-native Paper/parity only: MEXC/Bybit quote, spread, stop geometry, and actual executable ladder before counting evidence.

## Crypto Swing PULLBACK_LIMIT + confirmed pullback branches

- Current state: live disabled; v2 Paper branches active

### Paper summary

| metric | value |
|---|---:|
| n | 558 |
| closed | 524 |
| wins | 156 |
| losses | 181 |
| sum_r | 165.97 |
| pf | 1.9170 |
| wr | 0.2977 |
| low_mfe_losses | 170 |

### Live summary

| metric | value |
|---|---:|
| n | 121 |
| closed | 33 |
| wins | 9 |
| losses | 24 |
| net_usd | -21.27 |
| pf | 0.6323 |
| wr | 0.2727 |
| low_mfe_losses | 18 |
| avg_live_paper_delta_r | -0.3128 |

### Paper breakdowns

| slice | closed | wins | losses | sum R | PF | low-MFE losses |
|---|---:|---:|---:|---:|---:|---:|
| entry:PULLBACK_LIMIT | 493 | 149 | 173 | 154.39 | 1.89 | 162 |
| entry:PULLBACK_CONFIRMED_RETEST | 29 | 7 | 6 | 13.58 | 3.26 | 6 |
| entry:FIB_IMPULSE_RETEST | 2 | 0 | 2 | -2.00 | 0.00 | 2 |
| direction:long | 489 | 144 | 171 | 148.83 | 1.87 | 160 |
| direction:short | 35 | 12 | 10 | 17.14 | 2.71 | 10 |
| setup:pullback | 475 | 141 | 164 | 154.33 | 1.94 | 155 |
| setup:breakdown | 35 | 12 | 10 | 17.14 | 2.71 | 10 |
| setup:breakout | 14 | 3 | 7 | -5.50 | 0.21 | 5 |
| close:original_stop | 181 | 0 | 181 | -181.00 | 0.00 | 170 |
| close:expired_flat | 100 | 0 | 0 | 0.00 | n/a | 0 |
| close:breakeven_stop | 87 | 0 | 0 | 0.00 | n/a | 0 |
| close:profit_lock_stop | 84 | 84 | 0 | 42.00 | n/a | 0 |
| close:tp3_runner | 72 | 72 | 0 | 304.97 | n/a | 0 |
| close:open | 0 | 0 | 0 | 0.00 | n/a | 0 |
| close:no_entry | 0 | 0 | 0 | 0.00 | n/a | 0 |

### Live breakdowns

| slice | closed | wins | losses | net USD | PF | low-MFE losses | avg delta R |
|---|---:|---:|---:|---:|---:|---:|---:|
| venue:mexc | 30 | 9 | 21 | -12.69 | 0.74 | 16 | -0.28 |
| venue:bybit | 3 | 0 | 3 | -8.59 | 0.00 | 2 | -0.66 |
| venue:none | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| direction:long | 33 | 9 | 24 | -21.27 | 0.63 | 18 | -0.31 |
| direction:short | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| setup:pullback | 33 | 9 | 24 | -21.27 | 0.63 | 18 | -0.31 |
| setup:breakdown | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:SUBMITTED | 33 | 9 | 24 | -21.27 | 0.63 | 18 | -0.31 |
| state:REJECTED_STALE_QUEUE | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED_SUBMISSION | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED_PREFLIGHT | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED_RISK_LIMIT | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED_DAILY_LOSS | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |

### Worst live examples

| captured | symbol | dir | setup | pnl | MFE R | paper R | venue |
|---|---|---|---|---:|---:|---:|---|
| 2026-08-30T23:00 | CAKE/USDT | long | pullback | -4.86 | 0.19 | 0.00 | mexc |
| 2026-08-01T18:02 | EPIC/USDT | long | pullback | -4.84 | 0.56 | 0.00 | mexc |
| 2026-08-26T10:08 | ONG/USDT | long | pullback | -4.62 | 0.04 | 0.00 | mexc |
| 2026-08-21T04:00 | ONT/USDT | long | pullback | -4.17 | 0.24 | 0.00 | bybit |
| 2026-08-22T20:00 | WIF/USDT | long | pullback | -4.15 | 0.14 | -1.00 | mexc |
| 2026-08-27T13:00 | RUNE/USDT | long | pullback | -4.14 | 0.27 | 0.00 | mexc |
| 2026-08-27T15:00 | CATI/USDT | long | pullback | -4.05 | 0.58 | -1.00 | mexc |
| 2026-08-25T03:00 | ZAMA/USDT | long | pullback | -4.02 | 0.42 | 0.00 | bybit |

### Repair proposal

- Keep raw `PULLBACK_LIMIT` out of live. Blind pullback fills have negative live history.
- Continue only confirmed branches: `PULLBACK_CONFIRMED_RETEST` and `FIB_IMPULSE_RETEST`, but split their stats in reports; do not aggregate them with raw pullback.
- Add a rejection candle / reclaim candle requirement and cancel if price slices through 0.618/0.786 without reclaim.
- If testing live later, use half-risk only after at least 30 clean venue-native closes and low-MFE original-stop losses below 35%.

## Crypto Intraday BREAKOUT_CONTINUATION

- Current state: Paper-only; old live evidence negative

### Paper summary

| metric | value |
|---|---:|
| n | 157 |
| closed | 135 |
| wins | 48 |
| losses | 63 |
| sum_r | 72.84 |
| pf | 2.1562 |
| wr | 0.3556 |
| low_mfe_losses | 62 |

### Live summary

| metric | value |
|---|---:|
| n | 105 |
| closed | 22 |
| wins | 5 |
| losses | 17 |
| net_usd | -32.01 |
| pf | 0.2511 |
| wr | 0.2273 |
| low_mfe_losses | 13 |
| avg_live_paper_delta_r | -0.2813 |

### Paper breakdowns

| slice | closed | wins | losses | sum R | PF | low-MFE losses |
|---|---:|---:|---:|---:|---:|---:|
| entry:BREAKOUT_CONTINUATION | 135 | 48 | 63 | 72.84 | 2.16 | 62 |
| direction:long | 130 | 46 | 60 | 74.84 | 2.25 | 59 |
| direction:short | 5 | 2 | 3 | -2.00 | 0.33 | 3 |
| setup:pullback | 122 | 43 | 57 | 70.89 | 2.24 | 56 |
| setup:breakout | 8 | 3 | 3 | 3.95 | 2.32 | 3 |
| setup:breakdown | 5 | 2 | 3 | -2.00 | 0.33 | 3 |
| close:original_stop | 63 | 0 | 63 | -63.00 | 0.00 | 62 |
| close:tp3_runner | 28 | 28 | 0 | 125.84 | n/a | 0 |
| close:profit_lock_stop | 20 | 20 | 0 | 10.00 | n/a | 0 |
| close:breakeven_stop | 19 | 0 | 0 | 0.00 | n/a | 0 |
| close:expired_flat | 5 | 0 | 0 | 0.00 | n/a | 0 |
| close:no_entry | 0 | 0 | 0 | 0.00 | n/a | 0 |

### Live breakdowns

| slice | closed | wins | losses | net USD | PF | low-MFE losses | avg delta R |
|---|---:|---:|---:|---:|---:|---:|---:|
| venue:mexc | 14 | 2 | 12 | -16.99 | 0.33 | 8 | -0.25 |
| venue:bybit | 8 | 3 | 5 | -15.02 | 0.14 | 5 | -0.34 |
| venue:none | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| direction:long | 22 | 5 | 17 | -32.01 | 0.25 | 13 | -0.28 |
| direction:short | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| setup:pullback | 20 | 5 | 15 | -22.40 | 0.32 | 11 | -0.30 |
| setup:breakout | 2 | 0 | 2 | -9.61 | 0.00 | 2 | -0.06 |
| setup:breakdown | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:SUBMITTED | 22 | 5 | 17 | -32.01 | 0.25 | 13 | -0.28 |
| state:REJECTED | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED_PREFLIGHT | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED_STALE_QUEUE | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED_RISK_LIMIT | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED_SUBMISSION | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |

### Worst live examples

| captured | symbol | dir | setup | pnl | MFE R | paper R | venue |
|---|---|---|---|---:|---:|---:|---|
| 2026-08-27T00:15 | TRUMP/USDT | long | breakout | -4.97 | 0.21 | -1.00 | bybit |
| 2026-08-28T02:50 | ENA/USDT | long | breakout | -4.64 | 0.15 | -1.00 | bybit |
| 2026-08-22T03:42 | BCH/USDT | long | pullback | -4.50 | 0.34 | -1.00 | mexc |
| 2026-08-27T00:00 | PUMP/USDT | long | pullback | -4.35 | 0.59 | -1.00 | mexc |
| 2026-08-27T00:10 | ZEC/USDT | long | pullback | -4.33 | 0.28 | -1.00 | mexc |
| 2026-08-27T00:51 | ASTER/USDT | long | pullback | -4.20 | 0.59 | 0.00 | mexc |
| 2026-08-23T07:13 | ACE/USDT | long | pullback | -3.99 | 0.00 | -1.00 | mexc |
| 2026-08-28T01:56 | WLD/USDT | long | pullback | -3.10 | 0.13 | -1.00 | bybit |

### Repair proposal

- Keep Paper-only. Intraday breakout live has negative USD despite Paper positives, likely from fees/spread/late chase.
- Require volume expansion, BTC alignment, and one-bar level hold before entry; otherwise convert to no-trade or Level Hold V2 candidate.
- Reduce TP optimism in Paper by modeling taker entry/stop and venue spread; intraday edge is very sensitive to costs.

## Crypto Swing LIMIT_THEN_TAKER_TIMEOUT

- Current state: still live canary; included because live is negative and should not be scaled

### Paper summary

| metric | value |
|---|---:|
| n | 118 |
| closed | 109 |
| wins | 18 |
| losses | 17 |
| sum_r | 116.93 |
| pf | 7.8784 |
| wr | 0.1651 |
| low_mfe_losses | 16 |

### Live summary

| metric | value |
|---|---:|
| n | 99 |
| closed | 9 |
| wins | 4 |
| losses | 5 |
| net_usd | -5.12 |
| pf | 0.5467 |
| wr | 0.4444 |
| low_mfe_losses | 3 |
| avg_live_paper_delta_r | 0.1557 |

### Paper breakdowns

| slice | closed | wins | losses | sum R | PF | low-MFE losses |
|---|---:|---:|---:|---:|---:|---:|
| entry:LIMIT_THEN_TAKER_TIMEOUT | 109 | 18 | 17 | 116.93 | 7.88 | 16 |
| direction:long | 109 | 18 | 17 | 116.93 | 7.88 | 16 |
| setup:pullback | 107 | 18 | 17 | 116.93 | 7.88 | 16 |
| setup:breakout | 2 | 0 | 0 | 0.00 | n/a | 0 |
| close:expired_flat | 72 | 0 | 0 | 0.00 | n/a | 0 |
| close:original_stop | 17 | 0 | 17 | -17.00 | 0.00 | 16 |
| close:profit_lock_stop | 9 | 9 | 0 | 4.50 | n/a | 0 |
| close:tp3_runner | 9 | 9 | 0 | 129.43 | n/a | 0 |
| close:breakeven_stop | 2 | 0 | 0 | 0.00 | n/a | 0 |
| close:open | 0 | 0 | 0 | 0.00 | n/a | 0 |
| close:no_entry | 0 | 0 | 0 | 0.00 | n/a | 0 |

### Live breakdowns

| slice | closed | wins | losses | net USD | PF | low-MFE losses | avg delta R |
|---|---:|---:|---:|---:|---:|---:|---:|
| venue:mexc | 6 | 2 | 4 | -2.96 | 0.59 | 2 | 0.15 |
| venue:bybit | 3 | 2 | 1 | -2.15 | 0.47 | 1 | 0.16 |
| venue:none | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| direction:long | 9 | 4 | 5 | -5.12 | 0.55 | 3 | 0.16 |
| direction:short | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| setup:pullback | 9 | 4 | 5 | -5.12 | 0.55 | 3 | 0.16 |
| setup:breakout | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| setup:breakdown | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:SUBMITTED | 9 | 4 | 5 | -5.12 | 0.55 | 3 | 0.16 |
| state:REJECTED_PREFLIGHT | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED_STALE_QUEUE | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |

### Worst live examples

| captured | symbol | dir | setup | pnl | MFE R | paper R | venue |
|---|---|---|---|---:|---:|---:|---|
| 2026-08-25T03:00 | VIRTUAL/USDT | long | pullback | -4.04 | 0.41 | -1.00 | bybit |
| 2026-08-26T18:00 | PUMP/USDT | long | pullback | -3.80 | 0.49 | 0.00 | mexc |
| 2026-09-14T11:01 | POLYX/USDT | long | pullback | -2.26 | 0.17 | n/a | mexc |
| 2026-08-25T20:00 | HOLO/USDT | long | pullback | -0.85 | 0.62 | -1.00 | mexc |
| 2026-08-25T04:00 | INJ/USDT | long | pullback | -0.33 | 0.90 | 0.00 | mexc |
| 2026-09-13T23:00 | FIL/USDT | long | pullback | 0.67 | 2.35 | n/a | bybit |
| 2026-09-13T17:00 | CVC/USDT | long | pullback | 1.08 | 1.17 | n/a | mexc |
| 2026-08-27T05:00 | S/USDT | long | pullback | 1.22 | 1.54 | 0.00 | bybit |

### Repair proposal

- Keep canary but do not scale. Paper is strong, live is not yet positive enough.
- Add post-entry low-MFE loser analysis by symbol/session; if losses cluster by session or weak BTC, make those Paper-only.
- Track maker fill quality separately from taker timeout fills; if timeout entries are the losers, shorten timeout or require skip instead of taker chase.

## Crypto Intraday LEVEL_HOLD_V2

- Current state: live canary route enabled but mostly no fills; candidate route needs readiness check

### Paper summary

| metric | value |
|---|---:|
| n | 115 |
| closed | 48 |
| wins | 20 |
| losses | 17 |
| sum_r | 29.30 |
| pf | 2.7237 |
| wr | 0.4167 |
| low_mfe_losses | 17 |

### Live summary

| metric | value |
|---|---:|
| n | 7 |
| closed | 0 |
| wins | 0 |
| losses | 0 |
| net_usd | 0 |
| pf | n/a |
| wr | n/a |
| low_mfe_losses | 0 |
| avg_live_paper_delta_r | n/a |

### Paper breakdowns

| slice | closed | wins | losses | sum R | PF | low-MFE losses |
|---|---:|---:|---:|---:|---:|---:|
| entry:LEVEL_HOLD_V2 | 48 | 20 | 17 | 29.30 | 2.72 | 17 |
| direction:long | 44 | 18 | 15 | 27.60 | 2.84 | 15 |
| direction:short | 4 | 2 | 2 | 1.70 | 1.85 | 2 |
| setup:pullback | 40 | 17 | 13 | 26.37 | 3.03 | 13 |
| setup:breakout | 4 | 1 | 2 | 1.23 | 1.62 | 2 |
| setup:breakdown | 4 | 2 | 2 | 1.70 | 1.85 | 2 |
| close:original_stop | 17 | 0 | 17 | -17.00 | 0.00 | 17 |
| close:profit_lock_stop | 13 | 13 | 0 | 6.50 | n/a | 0 |
| close:breakeven_stop | 11 | 0 | 0 | 0.00 | n/a | 0 |
| close:tp3_runner | 7 | 7 | 0 | 39.80 | n/a | 0 |
| close:no_entry | 0 | 0 | 0 | 0.00 | n/a | 0 |

### Live breakdowns

| slice | closed | wins | losses | net USD | PF | low-MFE losses | avg delta R |
|---|---:|---:|---:|---:|---:|---:|---:|
| venue:none | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| direction:long | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| direction:short | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| setup:pullback | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| setup:breakdown | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |

### Repair proposal

- Good candidate conceptually, but live sample is mostly not filled/routed. First fix route/fill observability, not strategy.
- Require a dedicated report: candidates -> paper fills -> live capture -> venue preflight -> submit. Promote only if this funnel is clean.
- If Paper remains positive with clean funnel, keep as primary replacement for raw intraday/pullback entries.

## Stocks Intraday BREAKOUT_CONTINUATION

- Current state: still live but recently hardened; included as loss-driver

### Paper summary

| metric | value |
|---|---:|
| n | 193 |
| closed | 22 |
| wins | 4 |
| losses | 4 |
| sum_r | -2.15 |
| pf | 0.2549 |
| wr | 0.1818 |
| low_mfe_losses | 4 |

### Live summary

| metric | value |
|---|---:|
| n | 118 |
| closed | 46 |
| wins | 24 |
| losses | 22 |
| net_usd | -24.94 |
| pf | 0.6071 |
| wr | 0.5217 |
| low_mfe_losses | 16 |
| avg_live_paper_delta_r | n/a |

### Paper breakdowns

| slice | closed | wins | losses | sum R | PF | low-MFE losses |
|---|---:|---:|---:|---:|---:|---:|
| entry:BREAKOUT_CONTINUATION | 22 | 4 | 4 | -2.15 | 0.25 | 4 |
| direction:long | 13 | 3 | 3 | -1.45 | 0.33 | 3 |
| direction:short | 9 | 1 | 1 | -0.70 | 0.01 | 1 |
| setup:continuation | 22 | 4 | 4 | -2.15 | 0.25 | 4 |
| close:expired_flat | 11 | 0 | 0 | 0.00 | n/a | 0 |
| close:tp3_runner | 5 | 3 | 2 | -0.65 | 0.27 | 2 |
| close:breakeven_stop | 3 | 0 | 0 | 0.00 | n/a | 0 |
| close:original_stop | 2 | 0 | 2 | -2.00 | 0.00 | 2 |
| close:profit_lock_stop | 1 | 1 | 0 | 0.50 | n/a | 0 |
| close:no_entry | 0 | 0 | 0 | 0.00 | n/a | 0 |
| close:open | 0 | 0 | 0 | 0.00 | n/a | 0 |
| close:invalid_stock_intraday_entry_not_point_in_time | 0 | 0 | 0 | 0.00 | n/a | 0 |

### Live breakdowns

| slice | closed | wins | losses | net USD | PF | low-MFE losses | avg delta R |
|---|---:|---:|---:|---:|---:|---:|---:|
| venue:mexc | 46 | 24 | 22 | -24.94 | 0.61 | 16 | n/a |
| venue:none | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| direction:long | 30 | 14 | 16 | -27.90 | 0.46 | 14 | n/a |
| direction:short | 16 | 10 | 6 | 2.97 | 1.25 | 2 | n/a |
| direction:unknown | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| setup:unknown | 46 | 24 | 22 | -24.94 | 0.61 | 16 | n/a |
| state:SUBMITTED | 46 | 24 | 22 | -24.94 | 0.61 | 16 | n/a |
| state:REJECTED | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED_STALE_QUEUE | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED_SUBMISSION | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED_PREFLIGHT | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED_RISK_LIMIT | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |

### Worst live examples

| captured | symbol | dir | setup | pnl | MFE R | paper R | venue |
|---|---|---|---|---:|---:|---:|---|
| 2026-09-03T18:47 | SOFI/USDT | long |  | -5.36 | 0.02 | n/a | mexc |
| 2026-09-02T19:02 | CRWD/USDT | short |  | -5.01 | 0.05 | n/a | mexc |
| 2026-09-11T19:26 | SMCI/USDT | long |  | -4.99 | 0.24 | n/a | mexc |
| 2026-09-03T18:46 | CRM/USDT | long |  | -4.86 | 0.07 | n/a | mexc |
| 2026-09-01T16:29 | TXN/USDT | short |  | -4.81 | 0.30 | n/a | mexc |
| 2026-09-09T14:35 | AMD/USDT | long |  | -4.78 | 0.30 | n/a | mexc |
| 2026-09-11T17:57 | APP/USDT | long |  | -4.65 | 0.00 | n/a | mexc |
| 2026-09-02T18:15 | QCOM/USDT | long |  | -3.71 | 0.28 | n/a | mexc |

### Repair proposal

- Do not judge old live sample after today’s hardening as the same strategy. Start a post-filter cohort from the structural-stop v2 config.
- Keep live small only for structural stop + sector/broad aligned entries; everything else remains Paper/rejected.
- Add opening-range guard: no first-volatility impulse unless it closes and holds above VWAP/level with sector confirmation.

## Stocks Intraday PULLBACK_LIMIT/VWAP

- Current state: Paper-only

### Paper summary

| metric | value |
|---|---:|
| n | 223 |
| closed | 17 |
| wins | 0 |
| losses | 1 |
| sum_r | -1.00 |
| pf | 0.0000 |
| wr | 0.0000 |
| low_mfe_losses | 1 |

### Live summary

| metric | value |
|---|---:|
| n | 15 |
| closed | 0 |
| wins | 0 |
| losses | 0 |
| net_usd | 0 |
| pf | n/a |
| wr | n/a |
| low_mfe_losses | 0 |
| avg_live_paper_delta_r | n/a |

### Paper breakdowns

| slice | closed | wins | losses | sum R | PF | low-MFE losses |
|---|---:|---:|---:|---:|---:|---:|
| entry:PULLBACK_LIMIT | 17 | 0 | 1 | -1.00 | 0.00 | 1 |
| direction:long | 10 | 0 | 0 | 0.00 | n/a | 0 |
| direction:short | 7 | 0 | 1 | -1.00 | 0.00 | 1 |
| setup:continuation | 17 | 0 | 1 | -1.00 | 0.00 | 1 |
| close:expired_flat | 15 | 0 | 0 | 0.00 | n/a | 0 |
| close:original_stop | 1 | 0 | 1 | -1.00 | 0.00 | 1 |
| close:breakeven_stop | 1 | 0 | 0 | 0.00 | n/a | 0 |
| close:no_entry | 0 | 0 | 0 | 0.00 | n/a | 0 |
| close:open | 0 | 0 | 0 | 0.00 | n/a | 0 |
| close:invalid_paper_profile_entry_mode_mismatch | 0 | 0 | 0 | 0.00 | n/a | 0 |
| close:invalid_stock_intraday_entry_after_rth | 0 | 0 | 0 | 0.00 | n/a | 0 |
| close:invalid_stock_intraday_overnight_event | 0 | 0 | 0 | 0.00 | n/a | 0 |

### Live breakdowns

| slice | closed | wins | losses | net USD | PF | low-MFE losses | avg delta R |
|---|---:|---:|---:|---:|---:|---:|---:|
| venue:none | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| direction:unknown | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| setup:unknown | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |
| state:REJECTED | 0 | 0 | 0 | 0.00 | n/a | 0 | n/a |

### Repair proposal

- Paper-only. Pullback VWAP needs stricter confirmation than “touch VWAP”.
- Require reclaim/hold candle, broad/sector alignment, and structural stop under/over 15m structure.
- For shorts, require broad market down; no isolated short against bullish SPY/QQQ.

## Liquidity Sweep Special Tables

### Liquidity Sweep Reclaim V2 Paper

- rows `296`, clean closed `10`, wins `6`, losses `4`, net `$-15.72`, PF `0.83`

| direction | closed | wins | net USD | avg R |
|---|---:|---:|---:|---:|
| long | 10 | 6 | -15.72 | 0.15 |

| session_bucket | closed | wins | net USD | avg R |
|---|---:|---:|---:|---:|
| us | 8 | 5 | 9.21 | 0.23 |
| europe | 1 | 1 | 6.90 | 0.67 |
| asia | 1 | 0 | -31.83 | -1.00 |

| entry_profile | closed | wins | net USD | avg R |
|---|---:|---:|---:|---:|
| RECLAIM_HOLD_5M_2BAR | 10 | 6 | -15.72 | 0.15 |

| confirmation_timeframe | closed | wins | net USD | avg R |
|---|---:|---:|---:|---:|
| 5m | 10 | 6 | -15.72 | 0.15 |

| close_reason | closed | wins | net USD | avg R |
|---|---:|---:|---:|---:|
| profit_lock_stop | 6 | 6 | 78.36 | 0.75 |
| original_stop | 3 | 0 | -90.45 | -1.00 |
| breakeven_stop | 1 | 0 | -3.63 | 0.00 |

### Liquidity Sweep V1 Shadow

- rows `286`, clean closed `79`, wins `31`, losses `48`, net `$-255.18`, PF `0.70`

| direction | closed | wins | net USD | avg R |
|---|---:|---:|---:|---:|
| long | 78 | 31 | -229.01 | 0.17 |
| short | 1 | 0 | -26.16 | -1.00 |

| session_bucket | closed | wins | net USD | avg R |
|---|---:|---:|---:|---:|
| europe | 44 | 16 | -114.52 | 0.22 |
| us | 35 | 15 | -140.66 | 0.07 |

| entry_profile | closed | wins | net USD | avg R |
|---|---:|---:|---:|---:|
| unknown | 79 | 31 | -255.18 | 0.15 |

| confirmation_timeframe | closed | wins | net USD | avg R |
|---|---:|---:|---:|---:|
| unknown | 79 | 31 | -255.18 | 0.15 |

| close_reason | closed | wins | net USD | avg R |
|---|---:|---:|---:|---:|
| profit_lock_stop | 28 | 23 | 286.41 | 0.74 |
| original_stop | 23 | 0 | -689.26 | -1.00 |
| breakeven_stop | 19 | 0 | -136.22 | 0.00 |
| tp3_runner | 6 | 6 | 243.48 | 2.01 |
| time_exit | 3 | 2 | 40.42 | 0.81 |

### HTF Liquidity Reclaim Shadow

- rows `2`, clean closed `0`, wins `0`, losses `0`, net `$0.00`, PF `n/a`

### Liquidity Sweep Decision

- V1 stays retired from live.
- V2 remains Paper-only; if sample is too small or negative, tune sweep/reclaim confirmation first, not live routing.
- Best next change: split 5m reclaim and 15m reclaim, keep only the profile/session/direction slice with positive clean closed net and acceptable low-MFE loss rate.
