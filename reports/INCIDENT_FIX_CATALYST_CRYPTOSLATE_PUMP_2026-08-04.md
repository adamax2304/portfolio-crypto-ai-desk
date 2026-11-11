# Catalyst, CryptoSlate, and PUMP MEXC Incident Fix

Date: 2026-08-04

## Findings

1. `signal_catalyst_labels` was not stopped. Its refresh is a late derived step in a long
   two-hour scheduler cycle, while the watchdog used the shorter core-tracking SLA. The 2.9h
   warning was a false mid-cycle alarm.
2. CryptoSlate had two consecutive read timeouts and then recovered. It still had fresh rows
   and is a redundant, non-primary editorial source, so declaring the whole source ERROR on
   one short incident was too severe.
3. PUMP reached the MEXC outbox in seconds and was live-policy eligible. Preflight requested
   `PUMP_USDT`, an old closed MEXC contract (`state=3`). The active Pump.fun contract is
   `PUMPFUN_USDT` (`state=0`, `apiAllowed=true`). No queue, risk-guard, credential, margin,
   leverage, or Telegram delay blocked this signal.

## Changes

- Added an explicit canonical-to-MEXC alias: `PUMP/USDT -> PUMPFUN_USDT`.
- Individual preflight now uses the documented `/api/v1/contract/detail` endpoint; the
  regional catalogue remains available for discovery.
- Split contract rejection codes into `CONTRACT_STATE_NOT_OPEN` and
  `CONTRACT_API_DISABLED`, with sanitized contract details in the event/outbox result.
- Added three bounded CryptoSlate attempts (12s timeout, exponential 1s/2s backoff).
- Added `DEGRADED` for a transient failure of this non-primary feed while its own content is
  still fresh; the incident remains journaled and becomes ERROR if freshness is actually lost.
- Changed the derived-table watchdog SLA from 170m to 210m. Core scheduler/tracking alerts
  keep the original tighter SLA.
- Removed the misleading `Manual shadow only` sentence from a real Paper entry message.
  Paper and MEXC confirmation are now described as separate lifecycle events.

## Verification

- Consolidated regression: 323 passed, 0 failed.
- Scheduler dry-run: complete; all CLI commands validated.
- Current CryptoSlate state: OK; recovery alert sent and journaled.
- Current PUMP private preflight: active `PUMPFUN_USDT`, public/private API OK,
  `ready_for_real_orders=true`, kill switch CLEAR.
- MEXC monitor restarted on the new code; heartbeat OK.
- Pending Paper monitor restarted on the new alert code.

The historical PUMP signal was not replayed because its point-in-time entry was already stale.
The next fresh eligible PUMP Paper signal will use `PUMPFUN_USDT` at MEXC preflight.
