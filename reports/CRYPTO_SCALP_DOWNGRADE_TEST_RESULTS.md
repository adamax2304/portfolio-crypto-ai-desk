# Crypto Scalp Downgrade — Guardrail Test Results (PART 4)

**Date:** 2026-06-16
**New test file:** `tests/test_scalp_downgrade.py` (10 guardrails)

## The 10 required guardrails

| # | Guardrail | Test | Result |
|---|-----------|------|--------|
| 1 | crypto scalp size/actionable weight is **0×** | `test_1_scalp_sizing_weight_is_zero` (asserts `weight==0.0`, `sized_r==0.0`) | ✅ PASS |
| 2 | crypto scalp **setup** Telegram remains suppressed | `test_2_scalp_setup_telegram_suppressed` (`should_suppress_setup_telegram("crypto","scalp") is True`) | ✅ PASS |
| 3 | crypto scalp **paper-entry** immediate Telegram is shadow-only | `test_3_scalp_paper_entry_shadow_only` (status `shadow_only`, `notifier.send` not called, `"SHADOW ONLY"` in message, row recorded with `telegram_channel="shadow_only"`) | ✅ PASS |
| 4 | crypto scalp **still appears** in research/journal | `test_4_scalp_still_generated_and_recorded` (signal_alerts row recorded for scalp) | ✅ PASS |
| 5 | crypto **intraday** paper-entry still sends | `test_5_crypto_intraday_still_sends` (`status=="sent"`, `notifier.send` called once) | ✅ PASS |
| 6 | crypto **swing** paper-entry still sends | `test_6_crypto_swing_still_sends` | ✅ PASS |
| 7 | crypto **failed-bounce short** still sends | `test_7_crypto_short_still_sends` | ✅ PASS |
| 8 | **stocks intraday** paper-entry still sends | `test_8_stocks_intraday_still_sends` | ✅ PASS |
| 9 | no TP/SL/scoring/routing change (scalp geometry intact) | `test_9_no_tp_sl_scoring_change` (geometry constants `1.0*atr`, `1.2*atr`, `0.65*atr` present in `technical_setup_agent.py`) | ✅ PASS |
| 10 | no auto-trade path added | `test_10_no_auto_trade_path` (`place_order`/`create_order`/`ccxt` absent from `paper_entry.py` + `close_alert.py`) | ✅ PASS |

```
tests/test_scalp_downgrade.py ..........                    [100%]
10 passed
```

## Reconciling pre-existing tests with the 0× weight

The downgrade changed `crypto_scalp_momentum_continuation` from `0.5` → `0.0`. Four
`tests/test_sizing.py` cases encoded the old `0.5×` and were updated to the new reality
(this is the intended consequence of the approved downgrade, not a regression):

- `test_crypto_scalp_gets_half` → renamed `test_crypto_scalp_gets_zero_shadow_only`
  (`weight == 0.0`).
- `test_sized_r_is_product_of_raw_and_weight` → uses swing (1.0×) for the product check
  plus an explicit scalp 0× check.
- `test_size_signals_does_not_mutate_input` → uses swing; asserts weight 1.0.
- `test_portfolio_totals_skip_zero_weight_from_sized_metrics` → updated:
  `n_sized==2`, `sum_sized_r==0.0`, `sum_raw_r==-3.0`, `wins==1`, `losses==1`
  (scalp no longer contributes sized R).

One unrelated, time-flaky catalyst fixture was also de-flaked: `test_catalyst_safe_fixes.py::_crypto_catalyst_signal()` had a hardcoded `published_at` that aged to "old"
as wall-clock advanced; it now uses `datetime.now(utc) - 2h` so freshness is
deterministically "recent". (Not caused by the scalp change.)

## Focused regression (all green)

```
tests/test_scalp_downgrade.py tests/test_sizing.py tests/test_catalyst_safe_fixes.py
  → 43 passed

tests/test_telegram_standardization.py tests/test_paper_entry_alerts.py
  → 38 passed
```

## Full suite

```
626 passed, 3 failed in 1750.63s
```

### The 3 failures are pre-existing and unrelated to this task

All three are **stocks Telegram alert formatting** tests that assert an **old** alert
header format that the earlier "Standardize/redesign Telegram notifications" task
(already completed and accepted) deliberately replaced:

| Failing test | Asserts (stale) | Current production output |
|--------------|-----------------|---------------------------|
| `test_stocks_monitor_alerts.py::test_format_stocks_alert_contains_required_sections` | `[STOCKS INTRADAY] [A] [AAPL]` | `[🟡 STOCKS SETUP — NEW SIGNAL]\nSTOCKS AAPL LONG` |
| `test_stocks_telegram_safe.py::test_formatter_has_no_markdown_italic_markers` | `"alert_type:"` present | new header has no `alert_type:` line |
| `test_stocks_telegram_safe.py::test_formatter_handles_hostile_symbol_and_values` | symbol upper-cased in body | formatter preserves original symbol case |

These touch only the **stocks setup-alert formatter** (`render_setup_alert` /
`format_stocks_alert`), which this task did **not** modify. They fail identically
whether or not the scalp downgrade is applied. Per the task constraint "do not change
stocks intraday," they are left as-is and flagged for a separate stocks-Telegram test
refresh.

**Conclusion:** all 10 scalp-downgrade guardrails pass; the entire scalp/sizing/
paper-entry/close/Telegram regression is green; the only red tests are pre-existing
stocks-format assertions outside this task's scope.

**PART 4 status: DONE.**
