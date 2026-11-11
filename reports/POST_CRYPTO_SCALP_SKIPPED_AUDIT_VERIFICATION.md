# Post Crypto-Scalp Skipped Audit — Verification (PART 6)

**Date:** 2026-06-15

## 1. Scope of change

| File | Change |
|---|---|
| `src/agents/supervisor.py` | + `should_suppress_setup_telegram()` helper; `_maybe_send_trade_alerts` skips Telegram send for crypto scalp setup (still records watchlist_alert row with `telegram_channel` marker) |
| `tests/test_telegram_standardization.py` | + `test_15b` pinning the predicate |
| `reports/CRYPTO_SCALP_*` (5) | new audit + decision reports |

**No other source file touched.**

## 2. Invariant checklist

| # | Required | Result |
|---|---|---|
| 1 | No scoring changes | ✅ no edits under `src/agents/scoring*` / `src/stocks/agents/scoring*` |
| 2 | No TP/SL changes | ✅ no edits to technical-setup agents or signal levels |
| 3 | No routing changes | ✅ mode routing untouched |
| 4 | No sizing changes | ✅ `config/sizing_weights.yaml` untouched |
| 5 | No historical outcomes modified | ✅ audit is SELECT-only; `signal_outcomes` writes came from the production scheduler, not this task |
| 6 | No C-tier promoted | ✅ no tier mutation |
| 7 | No auto-trade path added | ✅ notification-only |
| 8 | Scheduler restart | ✅ NOT required — report subprocesses (`scalp-report`) load fresh `supervisor.py` on next cycle; no template/parse-mode change needs a manual restart |
| 9 | Only scalp setup Telegram behavior changed | ✅ predicate is `crypto + scalp` only; verified by `test_15b` (intraday/swing/stocks all still send) |

## 3. Tests

```
$ pytest tests/test_telegram_standardization.py tests/test_paper_entry_alerts.py
38 passed
```

`test_15b_scalp_setup_telegram_suppressed_crypto_only` confirms:
- `should_suppress_setup_telegram("crypto","scalp")` → True
- `(crypto,intraday)`, `(crypto,swing)`, `(stocks,scalp)`, `(stocks,intraday)` → False

## 4. What still works after the change

- Crypto scalp signals are still generated, registered, tracked, paper-traded, and recorded to `watchlist_alerts` (now tagged `telegram_channel=digest_only`).
- Crypto scalp PAPER-ENTRY alerts still fire on Telegram with the `⚠️ LOW-CONFIDENCE SCALP` warning.
- Crypto scalp CLOSE alerts still fire.
- All non-scalp setup alerts (crypto intraday/swing, stocks) and all paper-entry/close alerts are unaffected.

## 5. Live verification (next cycle)

The next `scalp-report` subprocess spawned by the running scheduler will import the patched `supervisor.py` and stop emitting the immediate scalp SETUP Telegram message. No manual scheduler restart performed (none required). Operator can confirm on the next scalp cycle: scalp setups appear in Obsidian/journal but no longer ping Telegram, while a scalp paper-entry (if one triggers) still pings.

## Verdict

```
SCALP_ALERT_NOISE_REDUCTION_READY
```
