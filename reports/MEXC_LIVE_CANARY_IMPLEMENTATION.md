# MEXC Live Canary Implementation

Date: 2026-07-17

## Current state

- Exchange: MEXC USDT perpetual futures (`https://api.mexc.com`).
- Scope: crypto swing long only.
- Allowed Paper entry modes: `PULLBACK_LIMIT`, `BREAKOUT_CONTINUATION`.
- Required Paper action: `FULL_SIZE` with a clean, point-in-time `entry_path` classifier.
- Production swing geometry remains `crypto_swing_legacy_native_v1`; T130/T140 and HALF/SHADOW lanes are excluded.
- Capital allocation: 100 USDT.
- Risk per trade: 2% = 2 USDT including conservative fees/slippage.
- Maximum simultaneous risk: 10% = 10 USDT. Five full-risk reservations fit; a sixth is rejected.
- Margin: isolated. Leverage is dynamic, capped at 50x, and constrained by the structural stop and liquidation buffer.
- Current execution mode: `live`.
- Real submission: enabled and armed through the Windows User environment.

Credentials are not stored in the repository, `.env`, logs, reports, SQLite, or order payloads. Because the current test key was disclosed in chat, it should still be rotated after the canary experiment and replaced with an IP-bound key without withdrawal permission.

## Decision flow

1. Existing Paper logic detects an actual entry and computes all overlays/guards.
2. After final Paper routing, but before Telegram I/O, an immutable point-in-time snapshot is written to `mexc_canary_decisions`.
3. Only an eligible snapshot receives one unique outbox row. Repeated tracker ticks cannot create another decision or order.
4. The dedicated three-second monitor claims an outbox row transactionally.
5. MEXC public metadata and depth are checked again: standard USDT perpetual, API allowed, spread, drift, tick/contract size, stop geometry and current fees.
6. In live mode, account equity, available margin, untracked exchange positions, kill switch, daily loss and local risk-ledger consistency are checked.
7. Risk is reserved in SQLite before submission. The create request uses a deterministic `externalOid`; after a timeout the worker queries that ID instead of blind-retrying.
8. A capped IOC long order is sent with isolated margin, original stop and TP3 attached.
9. Reconciliation verifies the fill, exchange position, liquidation price and TP/SL order.
10. Model F moves the stop to breakeven at +0.6R, then to +0.5R at +1.0R; TP3 remains the runner target. A three-second fair-price poll is supplemented with recent one-minute highs.

## Fail-closed gates

- Paper alert is shadow/review/half/block or generated under Paper `--dry-run`.
- Entry classification is scheduler backfill, unknown, dirty, or not one of the two allowed modes.
- `DATA_GAP_LATE`, excessive data gap, missing latency audit, stale entry, excessive entry drift, wide spread, or invalid stop/TP geometry.
- MEXC contract is disabled, non-standard, pre-market/TradFi, not API-allowed, or below minimum contract size.
- Estimated full loss including costs exceeds 2 USDT after contract rounding.
- Liquidation is less than 3x the stop distance or less than 0.5% beyond the stop.
- Any exchange position is not owned by this canary, or an owned open position lacks an active risk reservation.
- Active risk would exceed 10 USDT, total margin 50 USDT, gross notional 500 USDT, daily loss 3 USDT, or available margin. The effective risk basis is `min(100 USDT allocation, current exchange equity)`.
- Config hash changed after the immutable decision.
- Submission result is unknown. This trips the kill switch instead of retrying blindly.
- Protective stop cannot be verified after fill. The module submits an emergency close and trips the kill switch.

## Storage isolation

The module writes only:

- `mexc_canary_decisions`
- `mexc_canary_outbox`
- `mexc_canary_risk_reservations`
- `mexc_canary_orders`
- `mexc_canary_positions`
- `mexc_canary_events`
- `mexc_canary_control`

It contains no write path to `proposed_signals`, `signal_outcomes`, `final_r`, `signal_alerts`, or `paper_portfolio_ledger`.

## Operator commands

```powershell
python -m src.cli mexc-canary-status
python -m src.cli mexc-canary-preflight --symbol BTC/USDT
python -m src.cli mexc-canary-preflight --private --symbol BTC/USDT
python -m src.cli mexc-canary-order-probe --symbol BTC/USDT
python -m src.cli mexc-canary-order-probe --execute --symbol BTC/USDT
python -m src.cli mexc-canary-worker
python -m src.cli mexc-canary-monitor --interval 3 --duration-hours 3
python -m src.cli mexc-canary-kill --reason "operator stop"
python -m src.cli mexc-canary-kill --flatten --reason "emergency flatten"
```

`--clear` only clears the local kill switch after investigation; it never reopens a position.

## Activated state

1. Futures equity observed at activation: about 100.92 USDT; no open positions.
2. MEXC account position mode: Hedge (`positionMode=1`).
3. `submission_enabled=true`, `execution_mode=live`, arm value and credentials are present outside the repository.
4. Private preflight for both `BTC_USDT` and `ONDO_USDT`: `ready_for_real_orders=true`.
5. A dedicated continuous three-second monitor is running. The next fresh scheduler process also inherits the User environment and retains the normal scheduled monitor step.

Only decisions captured after the final live config is loaded can execute. Existing dry-run decisions are rejected by the immutable config-hash check.

## Verification completed

- Official MEXC public/private preflight: account, contract metadata, depth and positions all available; no untracked position.
- A real minimum BTC post-only order was accepted with isolated margin, Hedge Mode, explicit leverage and attached stop/TP fields, then canceled unfilled. Final exchange state was `4`, `dealVol=0`; open orders and positions both returned zero.
- The first probe exposed a live MEXC contract discrepancy: `cancel_with_external` currently accepts a singular JSON object even though its documentation shows a list example. The client now uses the observed payload shape and falls back to cancellation by authoritative `orderId`; a second real probe passed end to end.
- Real-contract sizing was checked for BTC, ETH, SOL and ONDO at 1%, 2%, 4% and 6% structural stops. Selected leverage was approximately 23x, 13x, 7x and 5x; every plan stayed at or below 2 USDT risk and above the 3x liquidation-distance requirement.
- Fourteen-day replay found 9 clean FULL swing candidates in the selected modes; 2 met the strict live freshness limits. Late Paper touches remain rejected rather than pretending they were live-fillable.
- Focused integration regression: 146 passed. Full project regression: **1636 passed**. Scheduler dry-run: 76 steps and all MEXC CLI surfaces valid.
- Paper/Shadow authority tables are not written by the live module. At final verification the canary had zero decisions, outbox rows, orders, positions and reservations; only operator probe/control audit events existed.

The real create/query/cancel path is verified. A synthetic market fill was deliberately not forced; real fill, attached TP/SL reconciliation and Model F movement will be verified on the first eligible point-in-time Paper swing signal.
