# Crypto Swing BREAKOUT_CONTINUATION Loser Audit

- Window: last 21 days since `2026-08-24T18:20:20.697194+00:00`
- Rows inspected: `52` live decisions
- Closed: `24`, wins: `11`, losses: `13`, live net: `-14.65 USDT`, original-stop/low-MFE losses: `12`

## Breakdown
### Direction
| slice | decisions | closed | wins | losses | net USDT | low-MFE losses |
|---|---:|---:|---:|---:|---:|---:|
| long | 48 | 22 | 9 | 13 | -21.80 | 12 |
| short | 4 | 2 | 2 | 0 | 7.15 | 0 |

### Score bucket
| slice | decisions | closed | wins | losses | net USDT | low-MFE losses |
|---|---:|---:|---:|---:|---:|---:|
| 67-72 | 28 | 13 | 7 | 6 | -2.62 | 5 |
| 72-78 | 10 | 2 | 0 | 2 | -5.04 | 2 |
| <67 | 14 | 9 | 4 | 5 | -6.99 | 5 |

### Setup type
| slice | decisions | closed | wins | losses | net USDT | low-MFE losses |
|---|---:|---:|---:|---:|---:|---:|
| breakdown | 4 | 2 | 2 | 0 | 7.15 | 0 |
| breakout | 5 | 0 | 0 | 0 | 0.00 | 0 |
| pullback | 43 | 22 | 9 | 13 | -21.80 | 12 |

### Venue
| slice | decisions | closed | wins | losses | net USDT | low-MFE losses |
|---|---:|---:|---:|---:|---:|---:|
| bybit | 1 | 1 | 0 | 1 | -2.39 | 1 |
| mexc | 23 | 23 | 11 | 12 | -12.26 | 11 |
| none | 28 | 0 | 0 | 0 | 0.00 | 0 |

## Worst Closed Live Trades
| captured | symbol | dir | score | setup | live PnL | MFE R | paper R | paper close |
|---|---|---|---:|---|---:|---:|---:|---|
| 2026-09-04T05:29 | ADA/USDT | long | 68.0 | pullback | -4.91 | 0.50 | 0.00 | expired_flat |
| 2026-09-08T21:00 | XPL/USDT | long | 68.1 | pullback | -4.90 | 0.49 | 0.00 | breakeven_stop |
| 2026-09-06T03:00 | UNI/USDT | long | 73.0 | pullback | -4.87 | 0.37 | 0.00 | expired_flat |
| 2026-09-12T17:39 | ETHFI/USDT | long | 66.3 | pullback | -4.85 | 0.16 | -1.00 | original_stop |
| 2026-08-25T07:00 | PROM/USDT | long | 66.0 | pullback | -4.21 | 0.15 | 0.00 | breakeven_stop |
| 2026-09-07T10:00 | ORCA/USDT | long | 68.5 | pullback | -3.98 | 0.54 | 0.50 | profit_lock_stop |
| 2026-08-28T18:12 | ENSO/USDT | long | 65.0 | pullback | -3.81 | 0.12 | -1.00 | original_stop |
| 2026-08-25T05:00 | LINK/USDT | long | 65.2 | pullback | -3.13 | 0.58 | 0.00 | breakeven_stop |
| 2026-09-12T07:00 | MINA/USDT | long | 66.2 | pullback | -2.45 | 0.57 |  | open |
| 2026-09-03T20:00 | TRUMP/USDT | long | 69.7 | pullback | -2.39 | 0.11 | 0.00 | expired_flat |
| 2026-09-05T21:00 | LTC/USDT | long | 71.3 | pullback | -0.33 | 0.00 | 0.00 | expired_flat |
| 2026-09-03T20:00 | CRV/USDT | long | 68.2 | pullback | -0.33 | 0.63 | 0.00 | expired_flat |

## Diagnosis
- Live losses are concentrated in trades that reached the original stop before producing meaningful MFE; this is exactly the class that generic Paper overstates when venue spread, drift and stop geometry are not native enough.
- Long continuation needs an extra hold/reclaim filter before live: no live long unless the current venue price is still above the trigger/level, BTC is not countertrend, and the first post-entry candle does not immediately reject the level.
- Shorts have recently behaved better than longs in this slice, so a corrected breakout variant should be asymmetric instead of one shared rule for both directions.
- Keep current BREAKOUT_CONTINUATION Paper-only. Candidate repair path: require MEXC/Bybit native parity, level-hold confirmation, low-MFE loser veto, and separate long/short thresholds before re-promoting.

## Next Research Variant
- `crypto_swing_breakout_reclaim_v2`: Paper-only; source is existing swing BREAKOUT_CONTINUATION, but entry is accepted only after a 15m/1h reclaim/hold around the breakout level.
- Live-readiness threshold: at least 30 clean venue-native closed trades, positive net USD, PF >= 1.25, avg live/parity delta not worse than -0.15R, and original-stop low-MFE losses under 35% of closed losses.
