# Settings Backtest — full signal history on DEEP OHLCV (read-model, NEVER auto-applied)

- db_path: `C:\Users\adama\Documents\crypto-ai-desk\db\crypto_ai_desk.sqlite`
- generated_at: `2026-07-07T16:59:01.942620+00:00`  ·  **PERSISTED (read-model table written)**
- matches persisted table: **true**
- asset_class: **crypto** · history_days: 60
- signals covered: **990** / 1002 total  (deep history unlocked **566** signals the 9-day cache could not replay; only 424 were within 9 days)
- coverage_status: **OK** (min 100 to draw a conclusion)

> **SETTINGS question only.** Real signals, varied handling, scored on real deep paths. This ranks/prunes settings — it does NOT prove live signal edge, model live fills/latency, or promote anything. Promotion stays forward + post-fee + positive + sign-off.

Covered by mode: intraday=342, scalp=407, swing=241

Covered by entry_mode (lookahead-safe pre-entry classify): BREAKOUT_CONTINUATION=264, LIMIT_THEN_TAKER_TIMEOUT=234, MOMENTUM_TAKER_NOW=37, NO_CHASE_SKIP=11, PULLBACK_LIMIT=439, STRUCTURAL_RETEST=5

## breakout_trigger_offset_atr

| variant | trades | skipped | net USD | net R | winrate | PF |
|---|--:|--:|--:|--:|--:|--:|
| `current` *(best)* | 885 | 105 | 395 | 80.08 | 0.40 | 1.04 |
| `0.05` | 881 | 109 | 93 | 66.87 | 0.39 | 1.01 |
| `0.1` | 880 | 110 | -134 | 57.07 | 0.38 | 0.99 |
| `0.2` | 875 | 115 | -537 | 39.48 | 0.37 | 0.94 |

## limit_then_taker_timeout_bars

| variant | trades | skipped | net USD | net R | winrate | PF |
|---|--:|--:|--:|--:|--:|--:|
| `4` *(best)* | 885 | 105 | 471 | 83.03 | 0.40 | 1.05 |
| `2` | 885 | 105 | 450 | 82.19 | 0.40 | 1.05 |
| `current` | 885 | 105 | 395 | 80.08 | 0.40 | 1.04 |
| `0` | 885 | 105 | 395 | 80.08 | 0.40 | 1.04 |
| `8` | 885 | 105 | 395 | 80.08 | 0.40 | 1.04 |

## maker_trade_through_bps

| variant | trades | skipped | net USD | net R | winrate | PF |
|---|--:|--:|--:|--:|--:|--:|
| `2` *(best)* | 885 | 105 | 461 | 82.67 | 0.40 | 1.05 |
| `current` | 885 | 105 | 395 | 80.08 | 0.40 | 1.04 |
| `5` | 885 | 105 | 395 | 80.08 | 0.40 | 1.04 |
| `10` | 884 | 106 | 159 | 70.68 | 0.39 | 1.02 |

## pullback_zone_depth_atr

| variant | trades | skipped | net USD | net R | winrate | PF |
|---|--:|--:|--:|--:|--:|--:|
| `deeper` *(best)* | 885 | 105 | 665 | 91.95 | 0.40 | 1.07 |
| `current` | 885 | 105 | 395 | 80.08 | 0.40 | 1.04 |
| `shallow` | 885 | 105 | 177 | 70.83 | 0.39 | 1.02 |

## structural_stop_atr_buffer

| variant | trades | skipped | net USD | net R | winrate | PF |
|---|--:|--:|--:|--:|--:|--:|
| `0.5` *(best)* | 892 | 98 | 505 | 65.51 | 0.35 | 1.06 |
| `0.1` | 887 | 103 | 481 | 78.97 | 0.39 | 1.05 |
| `current` | 885 | 105 | 395 | 80.08 | 0.40 | 1.04 |
| `0.2` | 887 | 103 | 361 | 69.75 | 0.37 | 1.04 |
| `0.35` | 888 | 102 | 197 | 57.63 | 0.36 | 1.02 |

## taker_fallback_enabled

| variant | trades | skipped | net USD | net R | winrate | PF |
|---|--:|--:|--:|--:|--:|--:|
| `current` *(best)* | 885 | 105 | 395 | 80.08 | 0.40 | 1.04 |
| `True` | 885 | 105 | 395 | 80.08 | 0.40 | 1.04 |
| `False` | 885 | 105 | 395 | 80.08 | 0.40 | 1.04 |
