# MEXC Stock Futures Paper Implementation

## Scope

- Paper only.
- Public MEXC contract, quote, depth, funding/OI and one-minute candle data.
- No private MEXC endpoint, real order submission, live routing, or mutation of
  `proposed_signals`, `signal_outcomes`, or `final_r`.
- Existing stocks intraday scoring remains the source of direction, setup and
  stop geometry.

## Timing

- 09:05 New York: warm the ordinary stocks intraday report.
- 09:10 New York: force one fresh report pass, then evaluate candidates. This
  is 20 minutes before the US cash open.
- Every five minutes: refresh source ideas for late news.
- Every minute: evaluate staged orders and open Paper positions against public
  MEXC one-minute candles.
- 15:30 New York: stop accepting new events.
- 15:55 New York: force-flat at the open of the 15:55 one-minute candle.
- 16:05 New York: end the monitoring grace period.

## Eligibility

- Source idea must be stocks/intraday with pre-gate A or B, score at least 70,
  and no cap other than the closed-session planning cap.
- A trusted, entity-resolved, directional canonical event must support the
  source idea and predate its latest recomputation.
- Earnings, legal risk, dilution/offering and management-change events are
  blocked in v1.
- The MEXC contract is discovered dynamically. The ticker is rejected if a
  current, API-enabled contract cannot be mapped exactly.
- Spread, fair/index divergence, top-five depth, hold volume and cash-to-MEXC
  source-price drift are checked point in time.

## Execution And Risk

- `PULLBACK_LIMIT` and `BREAKOUT_CONTINUATION` are selected from the existing
  setup type.
- Risk is 0.5% of current Paper equity per trade.
- Maximum three open positions and 2.5% concurrent risk.
- Maximum leverage is 5x; contract volume is quantized to MEXC units.
- Three partial targets use 33% / 33% / 34%.
- Model F protection uses 0.6R breakeven arm, 1.0R profit-lock arm and 0.5R
  locked stop.
- Entry and stop touched in the same minute are counted as a filled -1R loss,
  never removed as a no-entry.

## Accounting And Visibility

- Closed positions are appended to the common Paper trade stream.
- Contract-quantized quantity, risk, notional, margin and leverage are
  preserved in the USD ledger.
- MEXC futures fees, stock-futures slippage and entry funding-rate estimates
  are separated.
- Open positions appear in the Telegram dashboard.
- The operational report is `reports/MEXC_STOCK_FUTURES_PAPER_LATEST.md`.

## Verification

- New focused tests: 11 passed.
- Stocks suite: 143 passed.
- Full project suite: 1793 passed.
- Scheduler dry-run and CLI validation: passed.
- Public MEXC catalogue: 288 usable stock/tradfi USDT/USDC contracts stored.
- Recent stocks-intraday universe: 24 of 28 tickers mapped exactly. `DIA`,
  `XLF`, `XLV`, and `XLY` currently have no exact MEXC contract and fail
  closed.
- Working stocks monitor restarted on a one-minute tick and five-minute source
  refresh cadence.
