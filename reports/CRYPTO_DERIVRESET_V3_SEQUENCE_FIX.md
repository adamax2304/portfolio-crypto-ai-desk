# Derivatives Reset v3: Sequence-Funnel Repair

## Why the prior implementation produced zero entries

The retired implementation was operationally healthy: its 40-symbol Bybit
universe, five-minute cache, and point-in-time snapshots were fresh. The zero
was caused by an incompatible entry sequence rather than a missing data feed.

| prior gate | observations rejected |
|---|---:|
| Flush wick below 0.35% | 25,692 |
| Flush not local extreme | 3,923 |
| Reclaim not held on the immediate next two bars | 1,199 |
| All remaining structural/volume gates | 114 |
| Fully structured candidates reaching OI | 4 |
| OI reset >= 3% | 0 |

The strict implementation only allowed the reclaim ten minutes after the
flush. It then demanded a 3% OI decline and funding normalization in that same
ten-minute interval. Real leverage resets normally mature later. A design-only
replay of the current 40-symbol, 18.25-hour fresh cache found 31 non-overlapping
price-reclaim sequences inside 60 minutes, but only one met the former 3% OI
rule. This replay is a funnel check, not evidence or a backtest result.

## Current design

`crypto_derivreset_v3` / `shadow_derivreset_v3` is a new, isolated Shadow lane.
It never writes Paper, Live, `proposed_signals`, `signal_outcomes`, `final_r`,
or an active ledger. Earlier Derivatives Reset variants were retired and their
private data has been removed; this is the sole active experiment.

1. Observe a fresh, local liquidation wick at the actual bar-close availability
   time, within the existing seven-minute detection limit.
2. Save it as a private pending reset event for at most 60 minutes.
3. Require two later, closed reclaim candles rather than requiring them in the
   first ten minutes.
4. Require OI to decline at least 0.5% from the event peak, a directionally
   extreme funding reading of at least 0.01%, and funding normalization to 70%
   or less of that extreme.
5. Reject a rebuild in OI when price is still stalled at the reclaim level.
6. Preserve all independent safety checks: fresh derivatives and price data,
   1-hour spread-cascade gate, static liquidity, BTC/ETH alignment, Asia/off
   session block, on-chain hard risk, portfolio overlay, symbol cooldown, and
   Model F/cost accounting after entry.

The lower 0.15% wick floor is not a blanket relaxation: every such event still
has to satisfy local-extreme, delayed two-close reclaim, OI, funding, spread,
liquidity, market-alignment, and overlay checks. V3 intentionally has no upper
RVOL cap; a high RVOL after a liquidation reset is not itself a risk condition,
while chasing is limited by the maximum post-reclaim progress rule.

## First live-forward state

The derivatives monitor has been restarted with V3. Its first cycle refreshed
40/40 Bybit Linear series and created a pending WLD/USDT short reset event.
Other observed wicks were correctly rejected for stale snapshots or funding
against the proposed direction. No V3 position has been entered yet; therefore
there is no PnL claim and no promotion evidence.

## Review rule

V3 remains `SHADOW_ONLY` until it has at least 30 clean, closed forward trades
across 28 forward days, positive net USD PnL, PF >= 1.25, acceptable drawdown,
and a positive paired comparison where a valid identical control exists. There
is no automatic route to Paper or Live.
