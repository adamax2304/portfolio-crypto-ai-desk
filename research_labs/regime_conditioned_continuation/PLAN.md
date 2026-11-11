# Regime-Conditioned Continuation research plan

## Status and separation

This is a new hypothesis after `technical_trend_reclaim` failed its sealed
holdout. The failed holdout is never reused as a tuning target. This package has
its own config, SQLite ledger, reports and forward journal. It imports shared
historical archives and the deterministic cost simulator read-only.

No Paper, production Shadow, scheduler, risk-guard or live table is writable
from this package. Historical success can activate only an isolated forward
shadow lane. It cannot auto-promote itself.

## Hypothesis

A structural FVG reclaim has positive continuation expectancy only when all of
the following point-in-time conditions are true:

1. BTC 4H trend is aligned with the trade direction.
2. BTC directional strength is high enough, measured by causal EMA slope and
   ADX on closed 4H bars.
3. The symbol has directionally aligned 24H relative strength versus BTC.
4. Current symbol volatility is not compressed relative to its own causal
   30-day 4H ATR-percent median, so expected movement can pay MEXC costs.

Funding and OI can veto a crowded trade when fresh. Missing or stale derivative
history is `unknown`, never positive confirmation.

## Fixed entry and risk mechanics

- 4H EMA/structure trend for the symbol; no mandatory symbol ADX.
- FVG 0.10 to 0.75 ATR, first retest within 12 H1 bars.
- Baseline RSI reset confirmation.
- Closed M15 reclaim confirmation; entry at the next M15 open.
- Maximum chase extension 0.35 ATR.
- Structural stop plus 0.20 ATR, with a 0.5% minimum stop width.
- Targets 1.3R / 2.3R / 3.6R, Model F protection, 72-hour maximum hold.
- MEXC conservative fees and 15 bps slippage.

These values are inherited as execution/risk controls, not re-optimized on the
failed 2026 holdout.

## Pre-registered 16-profile grid

The only development dimensions are:

- BTC ADX minimum: 15 or 22;
- BTC absolute EMA-slope minimum: 0.05 or 0.15 ATR;
- absolute symbol-vs-BTC 24H relative-strength minimum: 0% or 2%;
- symbol 4H ATR-percent / 30-day median minimum: 0.80 or 1.10.

No other threshold may be changed during v1. A candidate must sit on a positive
neighbouring plateau; the maximum raw-PnL row is not automatically preferred.

## Historical protocol

- Archive target: 1,095 days for the liquid crypto universe.
- Historical development and chronological validation end before the period
  used as evidence in the previous lab wherever practical.
- The already inspected 2025–2026 region is an `audit_known_period`, never a
  sealed claim and never a source of additional tuning.
- Report pooled and per-fold net USD, PF, win rate, max drawdown, costs,
  long/short, symbols, days, top-trade concentration and monthly stability.
- Stress the frozen historical candidate at 10/15/20/25 bps and with one M15
  bar of extra entry delay. Stress results cannot select a more favourable row.

## Forward evidence

After historical freeze, the isolated forward lane records, at decision time:

- the exact config/code/data hashes;
- bar/event time, available time, observed ingestion time and decision time;
- BTC regime, symbol RS, volatility ratio, funding/OI freshness and every
  rejection reason;
- planned entry/stop/targets and MEXC conservative expected costs;
- later fill/exit events without rewriting the original decision snapshot.

Readiness requires at minimum 60 clean closed forward trades, 42 forward days,
positive net USD, PF >= 1.25, max DD <= 10R, both market directions represented,
no unresolved data-integrity warning, p90 decision-to-order-model latency below
60 seconds and p90 all-in slippage <= 15 bps. Status can become `REVIEW_ONLY`;
promotion remains manual.

## Development iteration log

### v1 result: rejected, validation untouched

- Full universe: 45 symbols, 4 development folds, 16 preregistered profiles.
- Best diagnostic profile: `v03`, 17 trades, +$168.43 net, PF 2.42, 3 positive folds.
- Rejected because the sample was too small and concentrated, one fold fell below the
  PF floor, and absolute-edge FDR did not pass.
- No profile was frozen and no validation or audit period was opened.

### v2 preregistration

This is the only development revision permitted before validation. Entry, stop,
targets, Model F, fees, slippage, holding period, and validation dates remain fixed.
The changes address the measured frequency collapse only:

- warmup reduced from 180 to 90 days; 90 days still exceeds the 30-day volatility
  history and indicator stabilization requirements;
- BTC ADX grid: 10/15;
- BTC slope fixed at 0.05 ATR because the v1 slope dimension was empirically redundant;
- relative-strength grid: 0.5/1.0/1.5/2.0 percent;
- volatility-ratio grid: 0.65/0.80.

The resulting grid is frozen at 16 profiles. Failure of v2 ends this crypto
hypothesis; there will be no third parameter search against the same development data.
