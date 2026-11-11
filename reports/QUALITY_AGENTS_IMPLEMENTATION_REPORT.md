# Quality Agents Implementation Report

Generated: 2026-09-19

## Delivered

- Added versioned point-in-time contracts for signal context, verdicts and the
  deterministic reducer.
- Added five narrow agents: news/entity quality, event risk, market regime,
  execution sanity and post-trade forensics.
- Added idempotent storage for runs, signal/market verdicts, reducer decisions,
  execution incidents and post-trade diagnostics.
- Integrated synchronous shadow capture at the common live decision boundary,
  covering standard Paper handoff, stocks, Crypto Invest and Liquidity Sweep.
- Integrated stock pre-US candidate evaluation before actionability.
- Mirrored post-ack stop, TP, position-ledger and reconciliation defects from
  the existing live watchdog into the agent evidence ledger without creating a
  second Telegram alert owner.
- Added a scheduled post-trade/effectiveness refresh and the
  `quality-agents-refresh` CLI command.
- Added bounded retention and latest-outcome replacement so recurring refreshes
  cannot duplicate diagnostics or grow the database without limit.

## Safety State

- Global operation mode: `shadow`.
- Existing strategy, Paper and live routing decisions remain authoritative.
- Agent errors, missing context and stale context are fail-open and persisted.
- Recommendations are measured but the applied action remains `ALLOW`.
- Objective execution incidents continue to be alerted by the established live
  watchdog; quality agents do not send duplicate alerts.

## Latency

- News and event agents share one point-in-time news lookup per signal.
- The lookup uses indexed availability windows before symbol expansion.
- Real database benchmark: about 100 ms for the full four-agent pre-dispatch
  evaluation on BTC, including SQLite evidence writes inside a transaction.

## Evidence Baseline

- Post-trade diagnostics materialized: 4,193 unique outcomes.
- Paper outcomes seen: 4,029.
- Live outcomes seen: 164.
- No signal verdicts existed before deployment; matched forward effectiveness
  starts with the next live-routed candidates.

## Verification

- Full test suite: 2,488 passed.
- Runtime processes restarted after deployment: scheduler, crypto signal
  monitor, pending live handoff, derivatives monitor and live reconciliation.
- Runtime heartbeat audit after restart: no problems.

## Promotion Rule

News, event and regime recommendations stay shadow until matched closed outcomes
show positive net benefit after missed winners and stable latency/error rates.
Execution sanity may later enforce only objective invariants, after the same
evidence review and an explicit configuration change.
