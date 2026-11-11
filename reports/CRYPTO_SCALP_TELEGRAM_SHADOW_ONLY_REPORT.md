# Crypto Scalp — Telegram Shadow-Only Routing (PART 2)

**Date:** 2026-06-16

## Starting state

| Alert type            | Crypto scalp (before) |
|-----------------------|-----------------------|
| **Setup** Telegram    | already suppressed (`should_suppress_setup_telegram("crypto","scalp") → True`) |
| **Paper-entry** Telegram | still pushed to the phone, with a LOW-CONFIDENCE warning |
| **Close/outcome** Telegram | still pushed to the phone |

The paper-entry and close alerts still nudged the operator to mirror a structurally
losing setup. PART 2 removes that nudge without deleting the signal record.

## What changed

A single predicate plus a routing branch, applied to **both** notifier entry points.

### `src/notifiers/paper_entry.py`

```python
def is_shadow_only_scalp(signal: dict) -> bool:
    asset = (signal.get("asset_class") or "crypto").lower()
    mode  = (signal.get("mode") or "").lower()
    return asset == "crypto" and mode == "scalp"
```

In `send_paper_entry_alert`, when `shadow_only` is true:

1. The message is prefixed with the mandated banner:
   ```
   [SHADOW ONLY — DO NOT TRADE]
   CRYPTO SCALP
   Not actionable. Research only.

   <original paper-entry body>
   ```
2. `payload["telegram_channel"] = "shadow_only"` (non-scalp → `"telegram"`).
3. `telegram_status = "shadow_only"` — **`notifier.send` is never called**.
4. The `signal_alerts` row is **still recorded** (so journal / research / digest keep
   full visibility), with `telegram_status="shadow_only"` and the shadow channel in the
   payload.
5. Returns `sent=False`, `reason_skipped="shadow_only"`.

### `src/notifiers/close_alert.py`

`send_close_alert` imports the same `is_shadow_only_scalp` predicate and applies the
identical routing: scalp close alerts get the shadow banner, are recorded with
`telegram_status="shadow_only"`, and are **not** pushed.

## Routing outcome

| Destination                  | Crypto scalp paper-entry (after) |
|------------------------------|----------------------------------|
| Phone Telegram (actionable)  | ❌ never sent (`notifier.send` skipped) |
| `signal_alerts` table        | ✅ row recorded (`shadow_only`)  |
| Obsidian dashboard           | ✅ visible, flagged SHADOW ONLY (PART 3) |
| Live shadow journal          | ✅ visible, `actionability="SHADOW ONLY — research, do not mirror"` |
| Digest (if rendered)         | ✅ banner-prefixed, self-labels as non-actionable |

So the alert is **routed to shadow/journal/digest**, exactly as requested, and the
`signal_alerts` row carries `telegram_channel="shadow_only"` as the standing marker.

## Non-scalp modes — untouched

The predicate is `True` **only** for `asset_class=="crypto" and mode=="scalp"`. For
everything else the old path runs verbatim — `notifier.send` is called and
`telegram_status` becomes `"sent"`. Pinned by guardrail tests:

- crypto intraday paper-entry still sends (`test_5`)
- crypto swing paper-entry still sends (`test_6`)
- crypto failed-bounce short still sends (`test_7`)
- stocks intraday paper-entry still sends (`test_8`)

## Setup Telegram

Untouched and still suppressed — the constraint "do not re-enable scalp setup
Telegram" is honored. `test_2_scalp_setup_telegram_suppressed` pins it.

**PART 2 status: DONE.** Telegram no longer nudges the operator to mirror scalp; any
residual scalp Telegram text carries the `[SHADOW ONLY — DO NOT TRADE]` banner.
