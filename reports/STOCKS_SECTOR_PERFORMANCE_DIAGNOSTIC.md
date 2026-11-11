# Stocks Sector-Performance Diagnostic (READ-ONLY)

**Date:** 2026-06-03
**Window:** last 14 days · **973 unique stock setups** (deduped by `signal_id`,
latest `signal_outcomes` row — NOT raw repeated tracker rows).
**Nature:** read-only analysis. No scoring / thresholds / live logic / DB
changed. Source: `scripts/_sector_diag.py`.

Metrics: `res` = resolved & triggered outcomes; `totR` = Σ realized R;
`PF` = gross-win-R / gross-loss-R; `stop%`/`tp1%` over resolved.

## Overall
`n=973 · triggered=681 · wins=156 · losses=140 · avgR=+0.145 · totR=+99.0 · PF=1.71`

## By tier
| tier | n | trig | res | W | L | avgR | totR | PF | stop% | tp1% |
|---|---|---|---|---|---|---|---|---|---|---|
| **C** | 332 | 241 | 241 | 37 | 66 | **−0.087** | **−21.0** | **0.68** | 28 | 15 |
| A | 90 | 64 | 64 | 23 | 17 | +0.125 | +8.0 | 1.47 | 27 | 36 |
| **B** | 551 | 376 | 376 | 96 | 57 | +0.298 | **+112.0** | **2.96** | 17 | 26 |

→ **B-tier carries the desk (+112R, PF 2.96). C-tier is the only net-negative tier (−21R, PF 0.68).**

## By mode
| mode | n | res | totR | PF |
|---|---|---|---|---|
| **swing** | 64 | 57 | **−6.0** | 0.45 |
| invest | 52 | 37 | 0.0 | — (none resolved) |
| intraday | 857 | 587 | +105.0 | 1.81 |

## By direction
| dir | n | res | totR | PF |
|---|---|---|---|---|
| long | 969 | 677 | +101.0 | 1.73 |
| short | 4 | 4 | −2.0 | 0.00 (tiny sample) |

## By sector
| sector | n | res | totR | PF | note |
|---|---|---|---|---|---|
| **consumer_discretionary** | 107 | 83 | **−19.0** | 0.30 | AMZN/XLY/TSLA |
| **healthcare** | 106 | 79 | **−10.0** | 0.69 | XLV disaster + LLY winner |
| **technology** | 183 | 103 | **−6.0** | 0.75 | AAPL drag vs XLK/MSFT |
| communications | 24 | 19 | −1.0 | 0.00 | |
| ai_software (PLTR) | 27 | 22 | +2.0 | 1.33 | |
| index_etf | 217 | 143 | +25.0 | 2.56 | SPY/QQQ/DIA |
| **semiconductors** | 224 | 159 | **+48.0** | 2.92 | SMH/AMD/AVGO |
| **ai_hardware (SMCI)** | 82 | 70 | **+62.0** | **9.86** | strongest |

## By symbol — the bleeders vs the winners
| symbol | n | res | W | L | totR | PF | stop% |
|---|---|---|---|---|---|---|---|
| **XLV** | 25 | 25 | 0 | 23 | **−23.0** | 0.00 | **92** |
| **AAPL** | 72 | 44 | 4 | 18 | **−13.0** | 0.28 | 41 |
| **IWM** | 60 | 31 | 0 | 11 | **−11.0** | 0.00 | 35 |
| **AMZN** | 23 | 22 | 0 | 11 | **−11.0** | 0.00 | 50 |
| **XLY** | 23 | 23 | 0 | 10 | **−10.0** | 0.00 | 43 |
| … | | | | | | | |
| LLY | 60 | 51 | 19 | 8 | +13.0 | 2.62 | 16 |
| SPY | 48 | 27 | 14 | 2 | +12.0 | 7.00 | 7 |
| SMH | 79 | 54 | 15 | 8 | +18.0 | 3.25 | 24 |
| AVGO | 49 | 40 | 14 | 4 | +21.0 | 6.25 | 10 |
| QQQ | 82 | 60 | 18 | 1 | +24.0 | 25.0 | 2 |
| **SMCI** | 82 | 70 | 32 | 7 | **+62.0** | 9.86 | 10 |

## Tier split of the bleeders (the decisive cut)
| symbol | A | B | C |
|---|---|---|---|
| XLV | — | — | **−23R / 25n** |
| IWM | — | 0R/3n | **−11R / 28n** |
| AMZN | — | — | **−11R / 22n** |
| XLY | — | — | **−10R / 23n** |
| **AAPL** | **−6R/27n** | **−7R/17n** | — |
| TSLA | +0/2n | +2R/31n | +0/5n |

→ **XLV, IWM, AMZN, XLY losses are ~100 % C-tier (watchlist-only, never
Telegram-alerted).** The single genuine A/B bleeder is **AAPL (−13R)** — a
*leader-sector* (technology) stock that rolled over intraday.

## ETF vs single name
| | n | res | totR | PF |
|---|---|---|---|---|
| ETF | 421 | 286 | +15.0 | 1.25 |
| single name | 552 | 395 | +84.0 | 2.06 |

## Sector leader / laggard bucket — DATA LIMITATION
Sector-ETF **RS-vs-SPY is only stored for the sectors whose ETF produced a
signal with that evidence line** — in this window only **technology (+11.7%)**
and **semiconductors (+13.4%)**. XLY/XLV/IWM/etc. signals did not expose a
parsed `RS vs SPY`, so a reliable leader/neutral/**laggard** classification at
signal-time **cannot be reconstructed from the DB**. (The markdown reports'
"Sector Rotation" section has it, but it is not joinable to signals.) This is
the key constraint the gate simulation runs into — see the simulation report.

## Catalyst / earnings flags
Earnings flags parsed (`safe` / `N/A (ETF)` / `unknown` / `today`) and
`news_supported` are available per signal but did not isolate the drag — the
losers are ordinary trend-follow longs on laggard names, not catalyst trades.
