# Crypto Scalp — Alert Noise Reduction (PART 4, IMPLEMENTED)

**Date:** 2026-06-15 · Notification-only change. **No** scoring / threshold / TP-SL / signal-generation / routing / sizing change.

## Trigger condition (met)

The PART 3 audit confirmed scalp SETUP alerts are noisy: **152 setup alerts / 14d → 7 wins**, 7× the paper-entry volume, repeated per cycle. The conditional change in the spec is therefore activated.

## What changed (1 surgical edit)

**`src/agents/supervisor.py`**
- New module-level helper `should_suppress_setup_telegram(asset_class, mode)` → returns True **only** for crypto scalp.
- In `_maybe_send_trade_alerts`, the `notifier.send()` for a setup alert is skipped when that predicate is True. The `watchlist_alert` row is **still recorded** (with `payload.telegram_channel = "digest_only"`), so Obsidian / journal / any digest keep full visibility.

## Behavior matrix after the change

| Alert | Telegram now? | Where it still appears |
|---|---|---|
| **crypto scalp SETUP** | ❌ suppressed | watchlist_alerts row → Obsidian / journal / digest |
| crypto intraday/swing SETUP | ✅ sent | unchanged |
| stocks SETUP (all sub-types) | ✅ sent | unchanged |
| crypto scalp **PAPER ENTRY** | ✅ sent | with `⚠️ LOW-CONFIDENCE SCALP — paper only unless manually approved` |
| crypto scalp **CLOSE** (tp/stop/expired) | ✅ sent | unchanged |
| any **paper-entry / close** (non-scalp) | ✅ sent | unchanged |

## Explicitly NOT touched

- Signal generation, scoring, thresholds, TP/SL, routing, sizing weights — all unchanged.
- `proposed_signals` / `signal_outcomes` / historical outcomes — untouched.
- The scalp signal is still generated, registered, tracked, and paper-traded exactly as before. **Only the immediate Telegram SETUP message for crypto scalp is silenced.**
- Paper-entry for scalp still fires (already carries the LOW-CONFIDENCE warning via `_risk_flags`).

## Tests

- New `test_15b_scalp_setup_telegram_suppressed_crypto_only` pins the predicate (crypto scalp → suppress; intraday/swing/stocks → send).
- 38/38 focused Telegram-standardization + paper-entry tests pass.

## Reversibility

To re-enable scalp setup Telegram, change `should_suppress_setup_telegram` to `return False`. One-line revert, no data impact.
