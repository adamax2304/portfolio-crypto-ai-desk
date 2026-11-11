# Crypto Short Continuation Retest: Implementation Report

## Status

- Strategy: `crypto_short_retest_v1`
- Shadow lane: `shadow_crypto_short_retest`
- State: enabled in isolated Shadow
- Paper/live/MEXC routing: disabled
- Background cadence: every 120 seconds through `derivatives_monitor`
- Universe: up to 40 liquid symbols with fresh derivatives/OHLCV data

## Implemented setup

The strategy waits for the complete sequence:

1. A fresh support level is broken on a closed candle.
2. The first breakdown is not excessively extended.
3. Price retests the broken level within a bounded number of bars.
4. The retest is rejected without a durable reclaim above the level.
5. The next closed candle confirms continuation below the rejection close.
6. Entry, stop, targets, costs, funding and profit protection are simulated deterministically.

There are two independent profiles:

- `short_retest_intraday_v1`: 15-minute execution, 1-hour context, targets `1R / 2R / 3R`.
- `short_retest_swing_v1`: 1-hour execution, 4-hour context, targets `1.3R / 2.3R / 3.6R`.

Both profiles reuse the realistic Paper execution and Model F profit-protection framework. Net USD PnL is authoritative; fees, slippage and funding are stored separately.

## Filter calibration

The filters are deliberately moderate:

- A single shallow move above the broken level does not invalidate the setup.
- Invalidation requires a hard reclaim or two accepted closes above the level.
- Missing funding, OI, spread, liquidity or catalyst context does not reject the setup.
- Such incomplete-context entries are recorded as `exploratory_v1` and cannot prove edge.
- Only explicit hazards reject: crowded shorts, violent BTC/ETH rebound, positive fresh catalyst, hard on-chain hazard, known excessive spread or known inadequate liquidity.
- Asia/off-session setups are simulated at half size instead of being discarded.

A read-only retrospective frequency check was used only to verify that the rules are not impossible:

| Profile | Breakdowns | Confirmed setups | Approx. conversion |
|---|---:|---:|---:|
| Intraday | 44 | 4 | 9% |
| Swing | 203 | 43 | 21% |

These are frequency diagnostics, not official performance evidence. Official evidence starts after activation and is forward-only.

## Isolation and storage

The strategy owns four private tables:

- `crypto_short_retest_shadow_events`
- `crypto_short_retest_shadow_outcomes`
- `crypto_short_retest_shadow_evaluations`
- `crypto_short_retest_shadow_meta`

It does not write to:

- `proposed_signals`
- `signal_outcomes`
- `final_r`
- the active Paper ledger
- MEXC/live routing

Migrations are idempotent and every insert uses an explicit column list.

## Verification

- Focused and regression tests: `194 passed`.
- Scheduler dry-run: all 82 planned steps validated.
- Source refresh: 40/40 strategy symbols fetched successfully.
- Background monitor restarted on the new code and is running at the 120-second cadence.
- A real forward event was detected for `LDO/USDT` and remains `pending` because the retest/confirmation sequence has not completed. No premature entry was created.

The test suite covers deterministic breakdown/retest/confirmation, reclaim invalidation, late-chase rejection, incomplete auxiliary context, explicit market hazards, native swing timeframes, isolated storage, scheduler ordering and absence of forbidden writes.

## Evidence policy

No profile can be considered ready from retrospective frequency alone. Manual review requires at least:

- 30 clean closed forward trades;
- 28 forward days;
- positive net USD PnL;
- profit factor at least 1.25;
- acceptable drawdown;
- separate review of strict and exploratory evidence.

There is no automatic promotion to Paper or live.
