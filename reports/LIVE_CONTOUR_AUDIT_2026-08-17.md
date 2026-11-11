# Live Contour Audit - 2026-08-17

## Scope

Audited the full route from Paper-approved signals through MEXC capture,
preflight, order submission, native stop/three-TP protection, reconciliation,
watchdog, and stock routing. No artificial live order was created for this
audit.

## Fixed

1. Standard stocks Paper breakouts were incorrectly coupled to the separate
   public MEXC stock-futures Paper simulator. A transient simulator quote
   timeout could prevent an otherwise fresh ordinary Paper breakout from being
   captured for live preflight. The routes are now independent in both the
   stocks monitor and the one-shot CLI command.
2. The event journal recorded the same reconciliation failure every monitor
   tick. Events are now rate-limited per position/outage window while the
   monitor still retries and increments the true error counter.
3. Swing policy drift was removed. Live swing and swing-repricing are now
   aligned to PULLBACK_LIMIT and BREAKOUT_CONTINUATION only.
4. MEXC's symbol-filtered position endpoint intermittently timed out. Live
   reconciliation now uses one authoritative account-wide position snapshot
   and filters it exactly in-process; the narrower endpoint is only a fallback.
5. Once MEXC has natively installed the stop and three close-limit TP orders,
   their full remote verification runs every 12 seconds rather than on every
   3-second price/Model-F tick. Price and Model-F monitoring remain frequent.
   This reduces avoidable API load without removing exchange-native protection.
6. Reconciliation error events now include their failed stage for faster
   diagnosis.
7. The long-running monitor now reuses its authenticated MEXC HTTPS session
   across ticks and replaces it only when its configuration or access key
   changes. It no longer creates a fresh network session every three seconds.

## Current Verification Snapshot

- Relevant regression suite: 204 passed.
- MEXC public and private preflight: OK; live armed, kill switch CLEAR.
- Live monitor, crypto pending monitor, stocks monitor, scheduler, and
  watchlist monitor: running with fresh leader leases.
- Queue: empty. Bot-owned active risk is within the configured cap.
- Manual exchange positions remain isolated from bot reconciliation and do not
  count as bot-owned positions.
- A normal live-route GPS_USDT position was observed during the audit, not
  created by the audit. It has a native stop and all three active TP legs.
  Its protection stage reached BREAKEVEN and the latest reconciliation was
  successful with zero current monitor errors.

## Residual External Risk

MEXC can still experience temporary network ReadTimeouts. The system treats
these as preflight retry/reject conditions before an order, retains native
exchange protection after an order, retries reconciliation, and raises a
watchdog alert rather than assuming success. Historical timeout events remain
in the audit journal intentionally; they are not a current unresolved position
error after the final verification snapshot.
