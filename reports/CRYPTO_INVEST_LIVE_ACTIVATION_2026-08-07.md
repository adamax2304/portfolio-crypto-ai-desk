# Crypto Invest Live activation

Date: 2026-08-07

## Operator decision

`crypto_regime_conditioned_continuation_v2` was connected to MEXC Live as the
independent route `crypto_invest_regime_conditioned_live_v1`. This is an explicit
operator override before the forward evidence gate has passed. The evidence report
continues to say `ACCUMULATING_FORWARD_EVIDENCE` and does not claim the strategy is
validated or automatically promotable.

## Universe

The reviewed universe contains 60 assets. Ranking combines CoinGecko market cap and
global 24h volume with Binance, Bybit and MEXC perpetual turnover. Eligibility also
requires an active MEXC API contract, an active Binance USDT perpetual, at least 365
days of Binance contract history and 180 days of MEXC contract history. Stablecoins,
wrapped/staked representations and tokenized reserve assets are excluded.

The checked-in list is in `config/crypto_invest_universe.yaml`; the complete source
snapshot and scores are in `reports/crypto_invest_universe_latest.json`. Membership
changes only when the operator runs:

```
python scripts/update_crypto_invest_universe.py --apply
```

Running without `--apply` only produces a proposal/snapshot. The intended review
cadence is weekly or biweekly.

## Live route

- source strategy: `crypto_regime_conditioned_continuation_v2`;
- frozen profile hash: `cf89424a...0413c1cf`;
- MEXC mode: `invest`;
- entry mode: `REGIME_RECLAIM`;
- directions: long and short;
- full-size target risk: $10 at the original stop;
- aggregate bot-owned open risk cap: $50;
- targets: 1.3R / 2.3R / 3.6R;
- exits: three partial TP legs plus Model F protective stop;
- ordinary crypto quality overlay and ordinary Paper risk guard: bypassed;
- losses in other modes do not trigger this route's daily-loss rejection.

The route still requires a fresh point-in-time decision, reviewed-universe membership,
the exact frozen profile, a currently tradable MEXC API contract, a current MEXC quote,
valid directional geometry, acceptable executable spread, available exchange margin,
verified three-leg exit allocation and a safe liquidation buffer. These are execution
invariants, not alpha filters, and were not removed.

## Activation verification

- public market ranking: 60 selected, membership unchanged on repeat refresh;
- live scanner: 60/60 symbols evaluated, zero transport errors;
- MEXC private preflight: credentials/account/public contract API OK;
- kill switch: CLEAR after removing the cross-mode daily-loss trip behavior;
- MEXC monitor: alive, 3-second cadence, heartbeat OK;
- Crypto Invest scanner: alive, 15-minute closed-bar cadence;
- first production cycle: one rejected diagnostic candidate, zero eligible entries,
  therefore no order was manufactured during deployment;
- stderr logs for both processes: empty;
- targeted regression: 128 passed;
- default scheduler dry-run: complete, new background step present.

## Material risk

Historical results were positive overall but forward clean closed trades are still
zero. The known-audit long slice was negative while the short slice generated most of
the historical profit. Both directions remain enabled only because the operator asked
for the frozen strategy unchanged; this is not a claim that long edge is proven.

Current MEXC equity at activation was about $82 with roughly $32 available to open new
positions because three non-bot positions were visible. A tight-stop setup may be
rejected if the exchange cannot supply enough isolated margin for a true $10 stop-risk
position. The system will not silently exceed $10 risk or weaken the liquidation
buffer to force a fill.
