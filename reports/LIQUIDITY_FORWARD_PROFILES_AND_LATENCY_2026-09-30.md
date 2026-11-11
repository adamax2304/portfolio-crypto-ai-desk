# Liquidity Forward Profiles and Latency - 2026-09-30

## Scope

The liquidity-reversal research suite now contains 11 isolated forward Paper
profiles: 8 crypto profiles and 3 stock profiles. Every profile has a unique
`profile_id`; none of these lanes routes an order to live execution.

## New target-policy twins

1. `crypto_fast_flush_reclaim_fast_1m_atr_targets_paper_v3`
   - Same strict FAST 1m entry cohort and structural stop as the FAST control.
   - TP1 = entry + 1 setup ATR.
   - TP2 = entry + 2 setup ATR.
   - Activated for forward evidence at `2026-09-30T00:00:00Z`.

2. `stocks_liquidity_shock_held_1m_structure_targets_paper_v1`
   - Same HELD 1m entry cohort and structural stop as the stock HELD control.
   - Requires two genuine chart-structure targets.
   - Rejects the row when the structural engine can only provide ATR fallback.
   - Activated for forward evidence at `2026-09-30T00:00:00Z`.

## Latency changes

- Crypto fast-flush evaluation runs in an independent 15-second lane aligned
  to wall-clock boundaries, with a 1.5-second candle-publication settle delay.
- Crypto research archiving runs in a separate five-minute loop and can no
  longer block entry evaluation.
- Candidate 1m and 5m Bybit bars use the public REST endpoint directly and are
  fetched in parallel. A live smoke check reduced the two-timeframe refresh
  from about 16.2 seconds to about 1.47 seconds.
- The stock liquidity-shock lane has an independent 15-second Paper cadence,
  aligned with a five-second publication settle delay, while the full stock
  monitor remains on its normal one-minute cadence.
- Newly closed stock 15m universe bars use the Alpaca multi-symbol endpoint.
  Candidate 1m bars use the same batch path and individually retry only missing
  symbols.
- Separate heartbeat files expose elapsed time, refresh counts, and failures:
  `data/runtime_locks/fast_flush_paper.heartbeat.json` and
  `data/runtime_locks/stocks_liquidity_shock_paper.heartbeat.json`.
- Fast Paper writers use bounded 1.5-2.0 second SQLite waits and retry on the
  next idempotent cadence. Slow research writers are awaited to completion, so
  a timed-out thread cannot remain alive and keep the database locked.

## Provider finding

The configured Alpaca credentials currently return HTTP 401 from both the
paper trading account endpoint and the market-data endpoint. The Paper data
collector therefore falls back to a multi-symbol yfinance batch and labels the
source `yfinance_batch`. This preserves forward research but is not considered
live-grade. An auth circuit breaker stops additional Alpaca chunks after the
first 401/403 and suppresses retries for 15 minutes. The 101-instrument fallback
smoke test fetched every symbol in about 6.45 seconds. Replace or reactivate the
Alpaca credentials before relying on the stock lane for low-latency live execution.

## Validation

- Configuration count: 8 crypto + 3 stock = 11 unique IDs.
- Database evaluation rows: 8 crypto + 3 stock profiles materialized.
- Final combined regression suite: 134 tests passed.
- Restarted derivatives monitor produced healthy fast-lane cycles around
  1.1 seconds without a refresh and 1.5-1.9 seconds with a candidate refresh.

## Interpretation

The 1.5-second and five-second values are post-close scheduling targets, not a
promise to trade before confirmation. The strategies still wait for their
configured closed 1m/5m confirmation bars. Network publication delay, provider
health, and SQLite contention remain measured rather than hidden.
