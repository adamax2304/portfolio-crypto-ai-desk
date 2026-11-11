# Entry-Mode Parameter Sweep (read-model — NEVER auto-applied)

- db_path: `C:\Users\adama\Documents\crypto-ai-desk\db\crypto_ai_desk.sqlite`
- generated_at: `2026-07-07T11:46:18.141096+00:00`  ·  **PERSISTED (read-model table written)**
- matches persisted table: **true**
- signals_swept: **80** / signals_sampled: 80 (forward evidence only; backfill excluded by default)
- coverage_status: **OK** (min 30 to draw a conclusion)
- source tables READ-ONLY: paper_shadow_execution_outcomes (branch=new_logic_shadow, window=forward_since_activation) joined proposed_signals; filters asset=None mode=None entry_mode=None since=None
- Each parameter varied one-at-a-time; others at `current`. Mode-specific fills + Model-F protection. maker_trade_through_bps affects the FILL condition, not a cost hack.

## breakout_trigger_offset_atr

| variant | trades | skipped | net USD | net R | winrate | PF |
|---|--:|--:|--:|--:|--:|--:|
| `0.1` *(best)* | 75 | 5 | -599 | -18.09 | 0.27 | 0.45 |
| `0.05` | 76 | 4 | -603 | -18.09 | 0.26 | 0.45 |
| `current` | 77 | 3 | -622 | -18.59 | 0.27 | 0.44 |
| `0.2` | 75 | 5 | -633 | -19.59 | 0.25 | 0.43 |

## limit_then_taker_timeout_bars

| variant | trades | skipped | net USD | net R | winrate | PF |
|---|--:|--:|--:|--:|--:|--:|
| `4` *(best)* | 77 | 3 | -622 | -18.59 | 0.27 | 0.44 |
| `2` | 77 | 3 | -622 | -18.59 | 0.27 | 0.44 |
| `current` | 77 | 3 | -622 | -18.59 | 0.27 | 0.44 |
| `0` | 77 | 3 | -622 | -18.59 | 0.27 | 0.44 |
| `8` | 77 | 3 | -622 | -18.59 | 0.27 | 0.44 |

## maker_trade_through_bps

| variant | trades | skipped | net USD | net R | winrate | PF |
|---|--:|--:|--:|--:|--:|--:|
| `current` *(best)* | 77 | 3 | -622 | -18.59 | 0.27 | 0.44 |
| `2` | 77 | 3 | -622 | -18.59 | 0.27 | 0.44 |
| `5` | 77 | 3 | -622 | -18.59 | 0.27 | 0.44 |
| `10` | 77 | 3 | -634 | -19.09 | 0.26 | 0.43 |

## pullback_zone_depth_atr

| variant | trades | skipped | net USD | net R | winrate | PF |
|---|--:|--:|--:|--:|--:|--:|
| `deeper` *(best)* | 77 | 3 | -495 | -12.81 | 0.29 | 0.55 |
| `current` | 77 | 3 | -622 | -18.59 | 0.27 | 0.44 |
| `shallow` | 77 | 3 | -646 | -19.59 | 0.27 | 0.43 |

## structural_stop_atr_buffer

| variant | trades | skipped | net USD | net R | winrate | PF |
|---|--:|--:|--:|--:|--:|--:|
| `0.5` *(best)* | 77 | 3 | -512 | -16.15 | 0.23 | 0.45 |
| `0.35` | 77 | 3 | -521 | -16.04 | 0.23 | 0.46 |
| `0.2` | 77 | 3 | -619 | -19.45 | 0.25 | 0.41 |
| `current` | 77 | 3 | -622 | -18.59 | 0.27 | 0.44 |
| `0.1` | 77 | 3 | -647 | -20.09 | 0.26 | 0.42 |

## taker_fallback_enabled

| variant | trades | skipped | net USD | net R | winrate | PF |
|---|--:|--:|--:|--:|--:|--:|
| `current` *(best)* | 77 | 3 | -622 | -18.59 | 0.27 | 0.44 |
| `True` | 77 | 3 | -622 | -18.59 | 0.27 | 0.44 |
| `False` | 77 | 3 | -622 | -18.59 | 0.27 | 0.44 |
