# Paper Integrity and Execution Hardening - 2026-07-16

## Scope

Integrity, accounting, observability, and alert delivery only. No score threshold,
entry filter, guard threshold, risk size, stop/target geometry, or live-routing
configuration was tightened or enabled. Live remains locked.

## Implemented

1. Signal lifecycle is monotonic. Re-registration cannot rewind an entered trade
   to waiting/no-entry or rewrite execution geometry after entry.
2. Model F keeps TP1/TP2 as open-position milestones. Realized PnL is recorded only
   at TP3, original/protected stop, expiry, or ambiguity.
3. Paper execution rows freeze entry geometry, entry time/price, terminal time/source,
   decision time, first observable executable price, and adverse entry drift.
4. The first terminal event wins. A later refresh cannot replace stop with TP or
   replace a closed trade with no-entry.
5. The USD ledger reads the immutable paper-execution table, uses exit time for
   realized-PnL day/calendar attribution, and keeps entry time separately.
6. Entry latency is timeframe-aware. Normal next 1h/4h bars are not called data
   gaps, while impossible rolling-cache backfills cannot be labelled FAST.
7. Failed paper entry/close Telegram deliveries enter a durable idempotent outbox.
   The scheduler retries them without touching signal/trade state.
8. Crypto overlay decisions now carry a hash of the effective overlay and cohort
   configuration through point-in-time payloads, actionability, and the ledger.
   Historical rows are not assigned a fabricated hash.

## Real Database Verification

- paper execution refresh: 2,794 scanned, 2,794 written, 2,328 resolved, 0 errors.
- lifecycle after migration: 2,328 CLOSED, 466 OPEN, 358 NO_ENTRY.
- CLOSED rows missing exit_at: 0.
- OPEN rows with realized paper_execution_r: 0.
- active fee-profile ledger: 643 closed actionable rows, all with entry_at and exit_at.
- overlay current decisions carrying the new config hash: 500, one effective hash.
- Telegram outbox is installed and scheduled; no new delivery was pending at verification.

The rebuilt all-history active-profile ledger reports +$6,744 net. This is accounting
output, not proof of forward/live edge: it mixes historical/backfill periods and must
not be used alone to authorize live trading.

## Verification

- Full test suite: 1,601 passed.
- Scheduler dry-run: complete; 70-step weekday plan; no automatic LLM invocation.
- New outbox CLI surface: valid.
- Python compile checks: passed for all changed runtime modules.

## Expected Effect

Trade frequency and eligibility are unchanged. The visible PnL may become lower or
move to a different calendar day because TP1/TP2 are no longer booked as completed
runner wins and realized PnL is assigned to exit time. That is removal of optimistic
accounting, not degradation of the strategy. Future statistics should be materially
more reliable for deciding which Paper mode is ready for a small live pilot.
