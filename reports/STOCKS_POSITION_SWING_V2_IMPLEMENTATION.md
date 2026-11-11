# Stocks Position Swing V2 - Implementation Report

Date: 2026-07-30

## Status

- Enabled for scheduled Shadow collection.
- Shadow only. It cannot write to Paper, live, Telegram, `proposed_signals`,
  `signal_outcomes`, `final_r`, or the Paper portfolio ledger.
- Strategy identity: `stocks_position_swing_v2`.
- Shadow lane: `shadow_stocks_position_swing_v2`.
- Profile: `stocks_position_swing_v2@2026-07-30`.
- No automatic promotion.

## Implemented strategy

V2 is a long-only US-stock swing framework with two deterministic setups:

1. `BREAKOUT_RETEST`
   - A 20-session base is broken on at least 1.2x relative volume.
   - The following completed daily bar must retest and hold the breakout.
   - The confirmation bar must close bullish and no more than 0.5 ATR above
     the reclaimed level.
   - Entry becomes valid only on a later US cash session.

2. `TREND_PULLBACK_RECLAIM`
   - The stock must reclaim EMA21 or SMA50 after a controlled pullback.
   - The confirmation bar must be bullish, close near its upper range, and
     have at least 1.0x relative volume.
   - Entry becomes valid only on a later US cash session.

Both setups require positive relative strength versus SPY and the stock's
sector, positive sector context, daily and weekly trend confirmation, adequate
dollar volume, and proximity to a medium/long-term high.

## Regime and event behavior

- `risk_on`: both setups, full model size.
- `neutral`: pullback/reclaim only, half model size.
- `risk_off`: no new long candidates.
- Earnings inside seven future US trading sessions block a candidate.
- Legal, offering/dilution, delisting, margin-delisting, and FDA/clinical risk
  block a candidate.
- Missing earnings/event data, dead primary stock-news feeds, stale market
  bars, and unadjusted split-like price discontinuities fail closed.
- All date comparisons use the New York session calendar and the latest
  completed session. Premarket scans do not incorrectly require today's
  unfinished daily bar.

## Execution and risk

- Entry starts strictly after the scan session and expires after three valid
  sessions.
- Excessive next-session gaps/chasing are rejected.
- Stops are structural plus an ATR buffer. An excessively wide structural stop
  rejects the trade instead of being silently tightened.
- TP1 is 2R on 50%; TP2 is 3R on 25%; the remainder uses the EMA21 trail,
  hard SMA50 exit, or 40-session time exit.
- Gap-through-stop fills use the opening price.
- Ambiguous entry-and-stop bars use stop-first ordering.
- Execution profile is `us_equity_commission_free_7bps_v1`: fees are zero under
  the stated commission-free US-equity assumption, while slippage is charged
  separately at 7 bps per side. Funding is explicitly zero.
- Model risk is 0.25% of $5,000 equity per full-size trade.
- Maximum five open V2 positions, 1.25% aggregate open risk, and 35% model
  equity notional in one sector.

## Evidence and review

- Candidates, outcomes, scans, and enriched reviews use four separate V2
  tables.
- Net PnL in USD is authoritative. Fees, slippage, and funding remain separate.
- Dirty rows are excluded from edge.
- Readiness requires at least 28 forward days, 30 clean closed trades, 10 per
  setup, positive net USD, PF at least 1.25, and maximum drawdown no greater
  than 8% of model equity.
- Passing readiness returns `REVIEW_ONLY`; it never promotes automatically.
- Enriched review can only keep, wait, reject, or request more data. Review
  cannot modify candidate geometry, score, status, execution, Paper, or live.

## Scheduler

The existing daily long-horizon stock cycle now runs:

1. V2 outcome refresh.
2. V2 scan after shared market data refresh.
3. A second outcome refresh.
4. V2 enriched-review packet preparation.

The 12-hour monitor also includes the isolated V2 refresh, scan, and packet.

## Verification

- V2 focused tests: 20 passed.
- Full stock and relevant Paper/news/scheduler regression: 354 passed,
  5 skipped, 0 failed.
- Full scheduler dry-run completed and validated every V2 CLI command.
- Static SQL guard found no forbidden writes from V2 modules.
- Real database scan completed across 68 symbols.

Latest real scan:

- Market regime: `neutral`.
- Scanned: 68.
- Candidates: 0.
- Rejected: 68.
- Most common conditions: weak sector trend/relative strength, weak daily or
  weekly trend, proximity to earnings, and distance from highs.
- Seven symbols reached the final setup check; none had a completed
  V2 retest/reclaim on the latest daily bar.

This zero is not evidence that V2 is unprofitable or broken. It means there was
no eligible setup on this specific scan. Forward evidence begins only when a
new candidate is created.

## Known limits

- This is long-only V2. Stock short swing requires a separate profile and
  evidence because borrow, squeeze, and gap risks are materially different.
- Shared daily prices are raw/unadjusted. V2 currently rejects split-like
  discontinuities instead of trying to reconstruct adjusted history.
- Official V2 metrics are US-underlying Shadow execution, not MEXC contract
  parity. MEXC contract price, spread, fees, funding, and symbol availability
  must be added before any future MEXC Paper/live review.
- No historical backfill is mixed into readiness. The current claim is only
  that the forward test is implemented and operational, not that edge has
  already been proven.
