# Quality Agents Implementation Plan

## Goal

Add five narrow, auditable quality agents around the existing deterministic
trading system. Agents must improve data quality, event-risk awareness,
regime context, live execution integrity, and post-trade diagnosis without
turning an LLM into an unmeasured mandatory trade gate.

## Safety contract

1. Existing strategy generation, Paper eligibility, and live route flags stay
   authoritative during the evidence phase.
2. Missing, stale, failed, or malformed agent output is fail-open and recorded.
3. `CAUTION` is advisory and may only suggest half size or remove a catalyst
   boost. It never blocks by itself.
4. `BLOCK_HARD` is reserved for objective conditions such as wrong entity,
   invalid symbol/geometry, unavailable venue, missing protection, or a known
   event halt.
5. Every verdict is point-in-time, versioned, expires, and includes evidence,
   reason codes, hashes, latency, and model/prompt provenance.
6. The reducer is deterministic. Agents provide facts and labels; code owns the
   final action.

## Delivery phases

1. **Contracts and storage**
   - Add shared enums/dataclasses and input/output validation.
   - Add idempotent SQLite tables for runs, signal verdicts, market verdicts,
     execution incidents, reducer decisions, and post-trade diagnostics.
   - Add indexes and read APIs for latest point-in-time evidence.

2. **Agent registry and runner**
   - Register versions, scopes, TTLs, dependencies, and execution modes.
   - Isolate failures per agent and persist run health/latency.
   - Support `shadow`, `advisory`, and later `enforced` operation.

3. **Five agents**
   - News/entity: symbol linkage, direction, source quality, and
     FAST/CONTINUATION/THESIS freshness.
   - Event risk: earnings, dilution/offering, legal/regulatory, FDA/court,
     macro, and halt risk.
   - Market regime: deterministic stock/crypto regime and directional quality.
   - Execution sanity: signal-to-live delivery, venue/symbol/geometry,
     fixed-risk sizing, TP/SL, routing, reconciliation, and worker health.
   - Post-trade forensics: classify normal loss versus entry, stop, regime,
     news, execution, or protection defects.

4. **Deterministic reducer**
   - Produce `ALLOW`, `ALLOW_HALF_SIZE`, `ALLOW_NO_CATALYST_BOOST`,
     `BLOCK_HARD`, or `REVIEW_ONLY`.
   - Enforce freshness and precedence rules in one place.
   - Persist both the recommendation and the actually applied action.

5. **Pipeline integration**
   - Stocks: capture pre-US and RTH candidate verdicts before actionability.
   - Crypto: capture regime and execution checks without an LLM dependency.
   - Live: run execution sanity before dispatch and after order/protection
     acknowledgement; feed critical objective defects into the watchdog.
   - Closed trades: enqueue forensic diagnostics without delaying monitors.

6. **Operations**
   - Add configuration with all agents initially `shadow`.
   - Add a CLI/report command and a scheduler-safe refresh script.
   - Add bounded retention and deduplication so the new telemetry cannot bloat
     the project database.

7. **Effectiveness measurement**
   - Join verdicts to Paper/live outcomes.
   - Report saved losers, missed winners, net delta R/USD, false-block rate,
     stale/missing rate, latency, and cost by agent/version/reason code.
   - Do not promote an agent to enforcement without matched evidence.

8. **Verification**
   - Unit tests for schemas, expiry, fail-open behavior, hard-block allowlist,
     reducer precedence, deduplication, and each agent.
   - Integration tests for live capture and watchdog incidents.
   - Compile and run focused regression suites, then inspect database rows.

9. **Promotion criteria**
   - Execution sanity may enforce objective invariants after regression tests.
   - News/event/regime agents remain shadow until the effectiveness report has
     enough matched closed outcomes and positive net delta after missed winners.
   - Post-trade forensics remains diagnostic only.

