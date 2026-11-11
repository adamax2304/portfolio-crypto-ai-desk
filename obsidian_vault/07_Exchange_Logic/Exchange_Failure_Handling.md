# Exchange Failure Handling

How the desk degrades when an exchange is unhealthy.

## Failure surfaces

- `Supervisor.update_data` returns a `CollectionSummary` with `fetched` + `failed` for the anchor exchange.
- For secondary exchanges (bybit, mexc), failures are captured in `secondary_summaries[exchange].failed`.
- For derivatives, separate `derivatives_failed`, `multi_exchange_derivatives_failed`, `bybit_derivatives_failed`.
- For news / social, `news_failures` and `social_failures`.

All of these are persisted into `data/processed/market_summary/last_update.json`.

## How to inspect

```
python -m src.cli exchange-status
python -m src.cli doctor
```

`exchange-status` shows per-venue role, trust, high-risk flag, universe count, OHLCV fetched count, OHLCV failed dict.

`doctor` returns readiness summary: db_exists, cached_symbols, latest_data freshness, last update failures.

## How `CoverageAuditAgent` surfaces it

The report contains a section like:

```
Coverage audit:
- binance OHLCV: 17 symbols fetched, 0 failed.
- bybit OHLCV: 17/17 fetched.
- mexc OHLCV: 14/17 fetched, 3 failed.
- Binance USD-M futures: 17/17.
- Multi-exchange derivatives: bybit/okx 16/17.
- RSS news: 4/4 sources OK.
- Social: Reddit OK; manual notes loaded.
- Manual events: 0 added this run.
- news_trader bridge: available, 240-min pulse: 14 signals, 3 strong.
```

The exact wording comes from the agent; what matters is **every subsystem reports green / partial / red**.

## Graceful degradation patterns

- Anchor (Binance) fails entirely → daily-report raises "No market data available". You must wait and re-run.
- Bybit fails → `derivatives_listed` becomes False for missing symbols; ideas can still produce, but at lower confidence + possibly cap at 75 (not on anchor doesn't apply, but missing derivatives confirmation does feed into the score).
- MEXC fails → discovery surface shrinks. Existing Binance / Bybit ideas unaffected.
- RSS fails → catalyst component drops; missing_news penalty applies (-3).
- news_trader_bridge unavailable → bridge logs warning, manual_social notes from bridge are empty; the desk falls back to RSS + manual notes only.

## What to do as operator

1. After every report, glance at `coverage_audit` first.
2. If any subsystem is red, do not take new ideas until you understand why.
3. If anchor is red, halt all trading until fixed.
4. If only derivatives are red, reduce position size or skip new entries.

## Related

- [[Exchange_Overview]]
- [[Coverage_Audit_Agent]]
- [[Doctor_and_Status]]

## Implemented status

- **Implemented**.
