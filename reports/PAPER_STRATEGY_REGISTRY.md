# Paper and Shadow Strategy Registry

This file is navigation only. Referenced configs remain authoritative.

## Paper / Crypto

| strategy | mode | entry mode | status | config |
|---|---|---|---|---|
| crypto_swing_t130 | swing | - | paper | `config/crypto_swing_paper_policy.yaml` |
| crypto_swing_pullback_confirmed_retest | swing | PULLBACK_CONFIRMED_RETEST | paper | `config/crypto_swing_pullback_paper.yaml` |
| crypto_swing_fib_impulse_retest | swing | FIB_IMPULSE_RETEST | paper | `config/crypto_swing_pullback_paper.yaml` |
| crypto_intraday_level_hold_v2 | intraday | - | paper | `config/crypto_intraday_level_hold_paper.yaml` |
| crypto_intraday_breakout | intraday | - | paper | `config/crypto_intraday_breakout_paper.yaml` |
| crypto_liquidity_sweep_reclaim_v2 | liquidity_sweep | LIQUIDITY_SWEEP_RECLAIM | paper | `config/paper/crypto/liquidity_sweep_reclaim_v2.yaml` |

## Paper / Stocks

| strategy | mode | entry mode | status | config |
|---|---|---|---|---|
| stocks_intraday_pullback_vwap_paper_v2 | intraday | PULLBACK_LIMIT | paper | `config/paper/stocks/pullback_limit.yaml` |
| stocks_intraday_breakout_1bar_paper_v1 | intraday | BREAKOUT_CONTINUATION | paper | `config/stocks/intraday_breakout_1bar_paper.yaml` |
| stocks_catalyst_rs_paper_v1 | intraday | CATALYST_RS_CONTINUATION | paper | `config/paper/stocks/catalyst_rs.yaml` |
| stocks_swing_event_rs_pullback_paper_v1 | swing | EVENT_RS_PULLBACK | paper | `config/paper/stocks/event_rs_pullback.yaml` |

## Shadow / Stocks

| strategy | mode | entry mode | status | config |
|---|---|---|---|---|
| stocks_catalyst_rs_v1 | - | - | shadow | `config/shadow_stocks_catalyst_rs.yaml` |
| stocks_earnings_gap_continuation_v2 | - | - | shadow | `config/shadow/stocks/earnings_gap_continuation.yaml` |

Validation: **OK**