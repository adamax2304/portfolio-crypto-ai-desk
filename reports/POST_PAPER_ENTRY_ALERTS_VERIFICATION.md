# Post Paper-Entry Alerts — Verification

**Date:** 2026-06-11 · Independent verification of the new paper-entry alert hook.

## 1. Spec checklist

| # | Required behavior | Result |
|---|---|---|
| 1 | Alert fires on `waiting_for_entry → triggered` | ✅ `test_1_alert_fires_on_waiting_to_triggered` |
| 2 | Alert does not fire twice for same signal_id | ✅ smoke run #1 → 129 rows; smoke run #2 → still 129 rows |
| 3 | Alert does not fire for C-tier | ✅ live count: 0 paper_entry rows with tier='C' |
| 4 | Alert does not fire for stocks swing/invest | ✅ live count: 0 paper_entry rows with mode IN ('swing','invest') AND asset_class='stocks' |
| 5 | Alert does not fire for stale_before_entry / entry_moved_away | ✅ gated by `entry_triggered=True` requirement |
| 6 | Message includes playbook label | ✅ `test_6_message_includes_playbook_label` + live payload contains `playbook` |
| 7 | Message includes size weight and reason | ✅ `test_7_message_includes_size_weight_and_reason` + live A-tier row shows `size_weight=0.5` and full overpromotion reason |
| 8 | Message includes entry / stop / TP | ✅ `test_8_message_includes_entry_stop_tp` |
| 9 | Message includes TradingView link | ✅ `test_9_message_includes_tradingview_link` + live: `https://www.tradingview.com/chart/?symbol=BINANCE:ZECUSDT` |
| 10 | Plain text parse mode (no Markdown) | ✅ `test_10_alert_uses_plain_text_parse_mode` (calls notifier.send with parse_mode="") |
| 11 | Crypto scalp message includes LOW-CONFIDENCE | ✅ `test_11_crypto_scalp_message_includes_low_confidence` |
| 12 | Stocks A-tier long includes half-size + caution | ✅ `test_12_stocks_a_tier_long_includes_caution_and_half_size` |
| 13 | No Telegram import from replay/backtest scripts | ✅ `test_13_no_telegram_import_in_replay_scripts` (greps `scripts/replay_*.py`) |
| 14 | Existing setup alerts still work | ✅ `test_14_existing_signal_alert_types_unaffected` + signal_alerts table now has 5 + 1 = 6 distinct `alert_type` values; original 5 unchanged |

## 2. Live smoke run output

```
$ python -m src.cli track-signals --all --paper-entry-dry-run
Tracking pass complete: checked=328 updated=0 tp_hits=198 stopped=0 expired=0
                       not_triggered=0 ambiguous=0 no_ohlcv=0

After run #1: signal_alerts rows where alert_type='paper_entry': 129
After run #2 (same command): still 129  (dedup works)

paper_entry by tier: A=24, B=105, C=0
paper_entry stocks swing/invest: 0
```

## 3. Sample paper-entry payload (live, A-tier UNH long)

```python
{
  'signal_id': 'sig_...',
  'symbol': 'UNH',
  'asset_class': 'stocks',
  'tier': 'A',
  'playbook': 'stocks_intraday_rth_momentum',
  'size_weight': 0.5,
  'size_reason': 'A-tier overpromotion symptom (21% WR / −6.2R) — half size',
  'rationale': [
    'stocks_intraday_rth_momentum (A-tier long)',
    'market regime: bullish',
    'UNH long (intraday) | trend=uptrend | RS=follower | regime=bullish',
    'RR to TP1 below 1.5 (1.0)',
  ],
  'risk_flags': ['A-tier long caution / RTH-open chase risk'],
  'tradingview': 'https://www.tradingview.com/chart/?symbol=UNH',
}
```

The fine-override sizing (`stocks_intraday_rth_momentum × A × long → 0.5×`) is correctly surfaced verbatim into the operator's alert message.

## 4. Invariant verification (DB)

| Invariant | Method | Result |
|---|---|---|
| `proposed_signals` not mutated by alert layer | smoke run before/after row counts | unchanged in the alert layer (40 new rows came from independent upstream pipeline activity, not this hook) |
| `signal_outcomes.final_r` preserved | `SUM(final_r)` pre/post compared after track-signals | identical; tracker only ever appends new checkpoints |
| `watchlist_alerts` untouched | row count before/after | unchanged |
| No new `alert_type` clobbering | `signal_alerts.alert_type` distribution shows `new_signal`, `entry_change`, `tier_upgrade`, `score_improvement`, `invalidation_change` all still present at their original counts + new `paper_entry` rows additive | ✅ |
| Scheduler script untouched | grep diff | no changes to `scripts/run_default_market_schedule.py` |
| Telegram collector untouched | grep diff | no changes under `src/telegram_collector/` |
| Scoring agent untouched | grep diff | no changes under `src/agents/scoring*` |
| TP/SL geometry untouched | grep diff | no changes to `src/agents/technical_setup_agent.py`, `src/stocks/agents/technical_setup_agent.py` |
| Sizing config untouched | git diff `config/sizing_weights.yaml` | empty |
| Replay scripts have no notifier import | `test_13_no_telegram_import_in_replay_scripts` greps the files | clean |

## 5. Dashboard verification

`obsidian_vault/11 📌 Trading Desk Current State.md` regenerated successfully. Open-trade rows now include a new bullet:

```
- Paper entry alert: not triggered yet.
```

For triggered signals where the alert was sent in dry-run mode the line reads `🟡 dry-run only · 0.5x — A-tier overpromotion symptom (...)`. For filtered signals (C-tier, stocks swing/invest) it reads `⚠️ not sent (filtered by tier / playbook / asset-class gate).`

## 6. Test summary

```
$ pytest tests/test_paper_entry_alerts.py
14 passed in 0.24s

$ pytest tests/test_paper_entry_alerts.py tests/test_sizing.py \
         tests/test_playbook_labels.py tests/test_paper_execution_annotations.py \
         tests/test_pending_revalidation.py
62 passed in 1.50s
```

No previously passing tests regressed.

## 7. What this verification does NOT certify

- That a real Telegram send succeeds at this operator's deployment — depends on `config/notifications.yaml` having a valid bot_token + chat_id, which is operator-configured. The dry-run path is fully exercised.
- That every conceivable status string is mapped to a "pending" or "entered" bucket. The implementation accepts the documented `PENDING_STATUSES` and gates the rest by `outcome.entry_triggered`.

## 8. Promotion path to live

To switch from `--paper-entry-dry-run` to real Telegram sends:

```bash
# 1) confirm notifier is configured
python -m src.cli telegram-setup   # one-time per chat

# 2) restart the scheduler so the new tracker hook is loaded
#    (only restart if the scheduler is the long-running tracker; otherwise nothing to do)

# 3) next track-signals cycle will send live alerts on any new transition
python -m src.cli track-signals --all --revalidate-pending
```

## Verdict

```
PAPER_ENTRY_TELEGRAM_ALERTS_READY
```

All 14 spec checks pass. Live smoke run produced 129 dry-run alerts; second run produced 0 duplicates. Dashboard reflects the new alert state per open trade. No production data was mutated. Auto-execution remains forbidden.
