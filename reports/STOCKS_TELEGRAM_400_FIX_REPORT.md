# Stocks Telegram 400 Delivery — P1 Fix Report

**Date:** 2026-06-05 · Source: 48h health audit (`FULL_SYSTEM_HEALTH_AUDIT_48H.md` §2)
**Scope:** stocks-monitor Telegram transport only. No change to alert selection,
cooldown, or dedup logic. No crypto changes.

## 1. Symptom
Over 48h `signal_alerts`: **76 sent / 15 `failed:HTTPError` (400 Bad Request) /
3 `failed:ReadTimeout` / 7 dry_run → ~19% of stock alerts not delivered.**

## 2. Root cause
The stocks alert is rendered by `format_stocks_alert()` and was sent with the
notifier default `parse_mode="Markdown"`. The message text is **not valid
Telegram Markdown**:
- Header `[STOCKS INTRADAY] [A] [SYMBOL]` — Telegram Markdown reads `[...]` as
  the label of a `[text](url)` link. Three consecutive unbalanced brackets with
  no `(url)` ⇒ "Can't parse entities" ⇒ **HTTP 400**.
- The footer emitted `_alert_type_:` — `_..._` is Markdown italic; combined with
  reasons/tickers containing stray `_`, `+`, `-`, `$`, `(`, `)` this compounds
  the parse failure.

This is the same class of failure seen when sending audit summaries with
special chars — confirmed fixed there by sending plain text (`parse_mode=""`).

## 3. Fix (transport + formatter, `src/stocks/monitor.py`)
Two minimal changes, no selection/cooldown/dedup touched:

1. **Send as plain text.** The single send site now passes `parse_mode=""`:
   ```python
   notifier.send(text, parse_mode="")  # plain text — robust vs [..] $ _ +/-
   ```
   Telegram treats an empty `parse_mode` as "no formatting", so brackets,
   tickers and symbols are delivered verbatim and never parsed as entities.

2. **Formatter emits no Markdown control markers.** `format_stocks_alert()`
   footer changed `_alert_type_:` → `alert_type:` (plain). The message now
   contains no `*_`` ``[]()` *formatting* markers, so it is also safe even if a
   future caller renders it through a Markdown parser.

`TelegramNotifier.send(text, parse_mode="Markdown")` already accepts a
`parse_mode` argument; passing `""` requires no notifier change and is already
used by the audit-summary path.

## 4. Failure isolation (already present, now pinned)
The send is wrapped in `try/except Exception` → on failure it logs a warning,
sets `telegram_status="failed:<ExcClass>"`, increments `result.telegram_failed`,
and **records the alert row anyway**. One Telegram error never crashes the
monitor loop or loses the alert record. Pinned by test.

## 5. Tests (`tests/test_stocks_telegram_safe.py`, all green)
| Test | Asserts |
|---|---|
| `test_formatter_has_no_markdown_italic_markers` | `_alert_type_` gone; `alert_type:` present |
| `test_formatter_handles_hostile_symbol_and_values` | ticker `BRK_B+ (test) [x] $US-D` + reasons with `_ + [] () $` don't crash; chars preserved |
| `test_monitor_sends_with_plain_text_parse_mode` | every monitor send uses `parse_mode=""` |
| `test_monitor_telegram_400_does_not_crash` | a 400 on every send → no exception raised; `telegram_failed≥1`; alert row stored `failed:…` |
| `test_dedup_unchanged_after_transport_fix` | duplicate tick still de-dupes (no second send) |

Existing `tests/test_stocks_monitor_alerts.py` (formatter contract, B→A
upgrade, score-improvement, C-tier no-alert, missing-invalidation, watchlist
isolation, dry-run status) and `tests/test_stocks_monitor_cooldown.py` continue
to pass unchanged → selection/cooldown/dedup behavior is intact.

## 6. Verification (safe, no spam)
- Formatter tests render hostile content with no exception.
- Monitor dry-run path unchanged (`telegram_status="dry_run"`).
- Plain-text send is the same transport already verified working twice for
  audit summaries (no 400). No bulk real-Telegram send was triggered by this
  change; only a controlled test message / dry-run was exercised.
