# Stocks Pullback Paper V2 Calibration - 2026-08-19

## Decision

`stocks_intraday_pullback_vwap_paper_v2` is active in Production Paper only.
It is not enabled in Shadow and is not eligible for MEXC or Bybit live routing.
The parameters below are now frozen for forward collection.

This is a conservative calibration, not proof of profitability. The available
sample is small and the unchanged-direction historical evidence is still weak.

## Evidence used

- Corrected forward report: 15 clean closed pullback observations, +$35.15,
  PF 1.24 when all evaluator rows are included. The unchanged production
  direction slice was -$62.57, PF 0.57, so direction-flip experiments were not
  treated as production evidence.
- Current legacy Paper profile: 13 closed trades, -0.5 Paper execution R.
- Deterministic source-direction replay over candidates with sufficient cached
  15-minute data:
  - V1 confirmation: 25 closes, -$82.78, PF 0.52, 36% win rate.
  - Directional-body confirmation: 24 closes, -$55.97, PF 0.61, 38% win rate.

The directional confirmation improved the replay loss by $26.81 while retaining
24/25 (96%) of the closable observations. It did not make the historical sample
profitable. Score, clock, hard RVOL and hard extension filters were rejected
because their apparent benefit was unstable and they removed too many winners.

## Implemented Paper rules

1. Keep the same broad stock-intraday A/B candidate stream and the existing
   pre-open A/B planning path.
2. Price must touch the configured pullback zone.
3. A completed 15-minute candle must then close through the far edge of the zone
   and on the correct side of session VWAP.
4. V2 also requires the confirmation candle body to agree with the trade
   direction. If the first reclaim candle disagrees, the plan remains pending
   and may enter on a later valid candle in the same session.
5. Full Paper size requires all three quality conditions:
   - confirmation-bar RVOL >= 0.80 versus the previous eight session bars;
   - decision-time ATR extension <= 3.50;
   - sector confirmation status is `confirmed`.
6. A weak or missing quality field does not delete the trade. The trade remains
   eligible at 0.5x Paper size so frequency and evidence collection continue.
7. Existing V1 candidates keep their original V1 confirmation and profile id
   until they resolve. They are never silently relabelled as V2.

## Data and accounting fixes

- Versioned stock resolvers now receive the complete originating RTH session.
  Session VWAP and confirmation RVOL therefore include causal pre-signal context,
  while entry eligibility still begins strictly after `decision_at` and uses
  closed bars only.
- V1 and V2 are mapped authoritatively to `PULLBACK_LIMIT` in Paper provenance.
- The V2 quality size is carried from resolver to tracker outcome, Paper alert
  and Paper portfolio payload.
- Live allowlists remain unchanged: both pullback versions fail the stock live
  bridge with `SOURCE_PROFILE_NOT_LIVE_ENABLED`.

## Verification

- Focused Paper/tracker/alert/live regression: 165 passed.
- Full stock test selection: 504 passed.
- Scheduler dry-run: 12 cycles; all CLI surface checks passed.
- Paper strategy registry: valid.
- Cached activation refresh: profile V2 loaded correctly, selected 0 and
  registered 0 in the current after-hours snapshot. No synthetic candidate was
  created to force activity.
- Pending monitor restarted through the project watchdog and is healthy on the
  new code. The stock monitor is outside its required RTH window and will be
  started by the scheduler for the next session.

## Forward review gate

Do not tune these thresholds after individual wins or losses. Review V2 after at
least 30 clean closed forward Paper trades and several independent sessions.
Use net USD PnL after fees/slippage, PF, drawdown, symbol/day concentration and
trade count. A reasonable continuation threshold is positive net USD PnL and
PF >= 1.25 without one symbol or one day explaining most of the result.
