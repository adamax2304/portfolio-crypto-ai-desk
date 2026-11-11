# Stocks All-Modes Research Plan

Status: preregistered research protocol. This file does not enable Paper or
live routing and is not read by the scheduler.

## Objective

Test every distinct current stock hypothesis without pooling incompatible
strategies, discard families with no plausible edge early, and optimize only
the survivors. Net PnL in USD after fees and slippage is authoritative. R is a
secondary diagnostic.

## Mode inventory

| Family | Current implementation | Historical test status | Next action |
|---|---|---|---|
| Intraday breakout | `BREAKOUT_CONTINUATION`, one 15m confirmation bar | Current forward and Paper evidence; raw variants negative | Baseline the production rule, then test only a small quality grid |
| Intraday pullback | `PULLBACK_LIMIT`, VWAP hold | Current forward and Paper evidence; raw variant negative | Baseline the production rule; do not reuse the rejected raw rule as evidence |
| Catalyst RS | Fresh trusted non-earnings catalyst plus stock/market/sector RS | Only short forward evidence | Point-in-time event replay and news-ablation study |
| Earnings gap | Earnings-only v2 | v1 evidence contaminated by mixed event types | Fresh earnings-only replay; never reuse v1 as v2 evidence |
| Pre-US MEXC news | Overnight/pre-market event plan revalidated before RTH | Promising but only seven sessions | Reconstruct candidate lifecycle and test by session, symbol and event type |
| Position Swing V2 | Breakout-retest or trend-pullback, multi-session | Almost no clean outcomes | Historical daily/1h adapter, then walk-forward |
| Residual momentum | Monthly cross-sectional rotation | Positive but underpowered and concentrated | Expand universe/time, test concentration controls; no threshold mining |
| PEAD long/short | Post-earnings drift | Independent validation failed | Stop; archive as rejected hypothesis |
| Technical FVG trend reclaim | Same-day H1/M15 technical reclaim | Negative before costs and after costs | Stop; archive as rejected hypothesis |
| Raw intraday variants | 1/2-bar breakout, retest, VWAP-hold | Large negative forward sample | Stop; keep tables only as negative controls |

Deprecated legacy stock swing/invest modes are not current strategies and are
not revived by this study.

## Stage 0 - data and causality gate

1. Price bars must have explicit bar-open, bar-close and `available_at` times.
2. Entry features may use only bars closed by the decision time.
3. News may be used only when `available_at <= decision_at`; publication time
   alone is insufficient.
4. Reconstructed current-universe data is labelled for survivorship bias.
5. Dirty, missing and late rows remain visible but are excluded from edge.
6. Yahoo underlying and MEXC-contract outcomes are reported separately. They
   may not be silently pooled.

## Stage 1 - baseline viability

Run the exact frozen/current rule before changing parameters. Report gross and
net USD PnL, PF, win rate, drawdown, trades, unique sessions/symbols, top-five
profit share, maximum symbol share, fees and slippage.

A family stops here when either condition is true:

- gross PnL is negative with at least 30 clean trades; or
- net PF is below 0.90 with at least 30 clean trades and no positive temporal
  fold.

An underpowered positive result remains `RESEARCH_ONLY`; it is not promoted.

## Stage 2 - news attribution

Technical modes are measured in causal buckets without changing their entry:

- `NO_FRESH_NEWS`: no linked point-in-time event;
- `POSITIVE_CONFIRMED`: linked, trusted event agrees with direction;
- `NEGATIVE_OR_RISK`: linked event conflicts or is a risk event;
- `UNKNOWN_OR_STALE`: news exists but was unavailable, stale or unresolved.

Compare the same candidate in two views:

1. executed-only: identical entries, grouped by the news state;
2. with-skips: counterfactual effect of blocking `NEGATIVE_OR_RISK` or requiring
   `POSITIVE_CONFIRMED`.

For Catalyst RS and Earnings Gap, news is core eligibility, so the ablation is
trusted/corroborated/exploratory/unresolved and age/source tiers, not a fake
technical-only strategy.

Enriched review is not synthesized historically. It is analyzed only where the
review was already available before the decision. This separates actual LLM
incremental value from hindsight commentary.

## Stage 3 - limited parameter screening

Only Stage-1 survivors enter a preregistered compact grid. Change one logical
axis at a time, keep exit/cost assumptions frozen, and require a parameter
plateau rather than one isolated optimum.

- Breakout: one/two confirmation bars, RVOL quality, close location, maximum
  extension and stop ATR.
- Pullback: VWAP/level hold depth, one/two hold bars, maximum extension and
  stop ATR.
- Event modes: event age, source trust, impulse/gap, RVOL and relative strength.
- Position: breakout/pullback setup separately, regime, RS and exit horizon.
- Residual momentum: frozen formation/skip logic; test universe and portfolio
  concentration controls rather than mining thresholds again.

## Stage 4 - selection and validation

Use rolling train/test folds. Select on train only, evaluate the selected
variant on the next untouched fold. Final claims require:

- at least 100 clean historical closes for intraday or 60 for multi-session;
- positive net USD PnL and PF at least 1.25;
- at least three positive test folds and minimum fold PF at least 1.0;
- acceptable drawdown;
- no single symbol above 15% of positive PnL and top five below 40%;
- cluster-bootstrap significance with multiple-testing correction;
- positive neighboring parameter variants, not a single sharp optimum.

If the sample cannot satisfy these gates, verdict is
`UNDERPOWERED_RESEARCH_ONLY`, even when PnL is positive.

## Stage 5 - forward evidence

Historical winners start an isolated Shadow lane. No automatic promotion.
Paper review requires at least 30 clean closed forward trades and 28 forward
days for intraday, or 60 closes and 126 days for multi-session modes, plus
positive net USD PnL, PF at least 1.25 and acceptable drawdown/concentration.

## Deliverables

- immutable run manifest with config/data/code hashes;
- baseline leaderboard and explicit stopped families;
- news-attribution and enriched-review incremental-value tables;
- per-fold selected variants and untouched test results;
- executed-only and with-skips views;
- a final manual recommendation: reject, keep Shadow, or review for Paper.

