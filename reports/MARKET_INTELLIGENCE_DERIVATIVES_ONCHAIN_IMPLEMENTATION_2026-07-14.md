# Derivatives and On-chain Intelligence Implementation

Date: 2026-07-14

## Scope and safety

Implemented and enabled a free, keyless market-intelligence layer for crypto paper trading.

- Live trading remains locked.
- Missing, stale, ambiguous, or unavailable intelligence fails open.
- Intelligence never increases score or position size.
- Confirmed adverse derivatives context may only reduce a paper candidate to HALF or SHADOW.
- On-chain hard blocks require an unambiguous verified contract and two independent confirmations.
- Unresolved ticker matches are visibility-only and have no paper authority.
- Existing `proposed_signals`, `signal_outcomes`, and `final_r` contracts were not changed by these modules.

## Canonical point-in-time storage

The authoritative intelligence store is the dedicated WAL sidecar
`data/intelligence/market_intelligence.sqlite`. It is intentionally separate
from `db/crypto_ai_desk.sqlite`, so long report/tracker writes cannot delay
pre-entry market context. An idempotent migration copied the existing rows
without deleting the legacy copies. Added additive SQLite tables for:

- derivatives snapshots with provider and receive timestamps;
- funding settlement events;
- forward liquidation events;
- per-source freshness and failure state;
- canonical asset/chain/contract identity;
- on-chain metrics;
- token security snapshots;
- holder concentration;
- future curated wallet-flow events.

Every trading read is point-in-time (`provider_ts <= decision time`). Future rows cannot leak into historical decisions.

## Free derivatives pipeline

Enabled current polling for up to 80 active symbols:

- Binance Futures;
- Bybit linear perpetuals;
- OKX swaps;
- Hyperliquid;
- MEXC futures.

MEXC uses `https://api.mexc.com`. The former `contract.mexc.com` domain was
removed after a production 403 exposed the stale endpoint; health recorded the
failure and Telegram sent the recovery after the endpoint was corrected.

Current cadence is five minutes. A bounded 29-day backfill runs in long-horizon scheduler windows for Binance, Bybit, OKX, and Hyperliquid.

Important correctness rules:

- Funding rates are normalized by their real interval.
- Bybit intervals come from instruments-info instead of assuming eight hours.
- Bybit HTTP-200 responses with non-zero `retCode` are errors.
- Bybit funding history uses both time bounds and bounded backward pagination.
- Open-interest changes compare the same venue through time.
- MEXC `holdVol` remains native contract units; it is never mislabeled as USD OI.
- Network requests complete before short per-source SQLite write transactions.
- A transient SQLite lock cannot terminate the long-running monitor.

## Liquidations

The Binance all-market forced-order WebSocket is running and archives events forward from activation.

- Source health is `ok`, with zero consecutive failures.
- No liquidation occurred during the verification windows, so the production table currently has zero rows.
- The system makes no claim of historical liquidation coverage.

## Free on-chain pipeline

Enabled:

- CoinGecko for canonical IDs and contract discovery;
- CoinMetrics Community metrics when present in the free catalog;
- DefiLlama chain TVL;
- GoPlus contract identity, token security, and holders;
- Honeypot.is as an independent security confirmation;
- Solana public RPC support for verified SPL-token largest-account concentration.

The registry currently contains:

- 8 verified native assets;
- 6 verified token contracts;
- 49 ambiguous candidates with no paper authority.

Verified token coverage includes LINK, UNI, AAVE, ARB, OP, and POL. Contract and burn addresses are excluded from EOA holder-concentration calculations. The latest top-10 concentration values are no longer inflated by token/LP contracts.

## Paper decision integration

The crypto quality overlay now reads a cached point-in-time derivatives and on-chain context.

Derivatives behavior:

- adverse OI/price regimes or material cross-venue disagreement can demote only;
- unknown or stale data does nothing;
- intelligence cannot promote a candidate.

On-chain behavior:

- independently confirmed honeypot, blacklist, or extreme sell tax can BLOCK paper;
- moderate sell tax, mintability, or high holder concentration can reduce to HALF;
- one provider alone cannot create a hard block;
- native assets receive network visibility but no token-contract security action.

The current-snapshot overlay contains 629 recent crypto candidates:

- FULL: 131
- HALF: 158
- SHADOW: 340
- BLOCK: 0

This current-snapshot table is diagnostic/read-model state. Historical ledger
sizing remains point-in-time and is never retroactively rewritten from a newer
snapshot.

## Funding accounting

The paper portfolio now uses actual exchange funding settlements first and a clearly labeled estimate only when events are unavailable.

Active Bybit profile after the production backfill:

- 50 trades use 156 actual Bybit settlements;
- actual funding total: -11.1218 USDT (signed cost/credit);
- 302 older or uncovered crypto trades use `mode_interval_fallback`;
- 289 equity trades are `not_applicable_equity`.

The active paper result changed from 897.40 USDT to 940.65 USDT net when real Bybit funding replaced estimates for covered trades. This is an accounting correction, not new trading profit.

## Enriched review and health

The enriched LLM packet includes derivatives, on-chain identity/risk, coverage, and source-health sections. Alert assembly reads the cache and does not wait on external providers.

The health monitor records source transitions in `logs/market_intelligence_errors.jsonl` and sends Telegram alerts after repeated failures. It reports per-venue freshness, major-asset venue coverage, null rates, p95 polling gaps, and table counts.

Current production state:

- all five derivatives sources: `ok`, zero consecutive failures;
- liquidation WebSocket: `ok`, zero consecutive failures;
- all configured on-chain providers: `ok`;
- BTC/ETH/SOL: five fresh venues each;
- scheduler, crypto monitor, pending monitor, stocks monitor, and derivatives monitor are running.

Health remains temporarily `degraded` because its 24-hour p95 still includes a real 20.3-minute maintenance/restart gap from this deployment. Current major-asset coverage itself is `ok`; the warning should age out as uninterrupted five-minute polls accumulate. It is intentionally not suppressed.

## Production data at verification

- `derivative_snapshots`: 32,582
- `funding_rate_events`: 12,114
- `asset_contract_registry`: 63
- `onchain_metric_snapshots`: 44
- `token_security_snapshots`: 32
- `holder_concentration_snapshots`: 24
- `liquidation_events`: 0 (forward stream, no observed event yet)
- `wallet_flow_events`: 0 (disabled intentionally)

## Verification

- Full repository regression: 1,531 passed across isolated batches. A single
  all-in-one pytest process timed out because of an environment/inter-suite
  hang; every collected test file passed when split.
- End-to-end intelligence/overlay/alert/actionability/enriched tests: 105 passed.
- Focused market-intelligence tests: 15 passed.
- Python compile sweep: passed.
- Scheduler dry-run: completed.
- Real derivatives monitor smoke: 349 rows per poll across five venues.
- Real 29-day backfill: completed without source errors.
- Real on-chain refresh: completed without provider errors.
- Real paper overlay and ledger refresh: persisted successfully.

## End-to-end production acceptance

The collector and consumers were verified separately and together:

- three consecutive five-minute polls wrote 349 rows each across Binance (80),
  Bybit (75), Hyperliquid (55), OKX (60), and MEXC (79), with no SQLite locks;
- after the MEXC domain correction, a fresh poll again wrote all 349 rows and
  source health returned to `ok`;
- a no-write production canary changed SXT and THE intraday from FULL to HALF,
  and SKL swing from FULL to HALF, solely because the fresh cross-venue funding
  disagreement reason was present;
- production current snapshots persist canonical derivatives reasons, including
  `derivatives_cross_venue_disagreement` and
  `derivatives_no_squeeze_no_full_without_confirmation`;
- a funding canary read the real 08:00 UTC Bybit settlement from the sidecar and
  produced `actual_bybit_funding_events`, `estimated=0`, `events=1`;
- POL, OP, and LINK resolve to verified, paper-eligible low on-chain risk. BTC is
  a verified native asset and correctly has visibility without token-contract
  authority;
- enriched review contains the derivatives/on-chain intelligence block.

There has not yet been a natural paper-entry alert after activation (the latest
paper-entry alert is 2026-07-14 03:00 UTC). No fake production signal was
inserted. The future-alert path is covered by tests and calls the same
point-in-time overlay before persisting/sending the alert, but the first natural
post-activation alert remains the final forward audit sample.

## Honest limitations

1. Free APIs do not provide a complete, trustworthy labeled exchange-wallet universe. Wallet-flow ingestion is implemented but disabled until addresses are curated or a reliable provider is added.
2. Liquidation history is forward-only from this deployment. It must accumulate before liquidation-derived edge can be evaluated.
3. MEXC USD OI is deliberately unknown because the public value is contract units without a safe contract-size conversion in this collector.
4. Only verified configured contracts can affect paper. New assets require a canonical ID, preferred chain, and secondary verification before promotion from candidate.
5. On-chain and derivatives data are risk inputs, not proof of profitable edge. Their incremental effect must be evaluated on resolved forward paper outcomes.

## Adding a new asset

For a native asset, add its canonical CoinGecko ID and optional CoinMetrics/DefiLlama mapping to `config/onchain.yaml`.

For a token, add its canonical CoinGecko ID and preferred chain. Do not add a ticker-only contract. Run `python -m scripts.onchain_risk_update`, confirm one unambiguous verified registry row and fresh independent security data, then inspect the enriched packet and overlay reasons.
