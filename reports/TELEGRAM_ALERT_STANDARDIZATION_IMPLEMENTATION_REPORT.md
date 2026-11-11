# Telegram Alert Standardization — Implementation Report

**Date:** 2026-06-14 · **Scope:** Notification formatting only. **No** scoring / threshold / TP-SL / signal-generation / routing / sizing change.

---

## 1. What was added / changed

### New modules
| File | Purpose |
|---|---|
| `src/notifiers/alert_headers.py` | Single source of truth for every visible message header + shared helpers (`tradingview_link`, `fmt_price`, `operator_summary`, `cap`). |
| `src/notifiers/setup_alert.py` | Standardized `[🟡 SETUP — WAITING FOR ENTRY]` template; shared by both crypto supervisor and stocks monitor. Stocks sub-type header per `alert_type`. |
| `src/notifiers/close_alert.py` | NEW close / outcome alert (`[✅ CLOSE — TP HIT]` / `[❌ CLOSE — STOP HIT]` / `[⏳ CLOSE — EXPIRED]` / `[⚠️ CLOSE — AMBIGUOUS]`). Mirrors paper-entry: dedup via `signal_alerts.alert_type` ∈ `{close_tp, close_stop, close_expired, close_flat, close_ambiguous}`. |
| `tests/test_telegram_standardization.py` | 21 tests pinning headers, body content, disclaimers, dedup, parse-mode, surface invariants. |

### Files touched (notification surfaces only)
| File | Change |
|---|---|
| `src/agents/supervisor.py::_format_idea_alert` | Delegates to `setup_alert.render_setup_alert`. Now uses plain text (was Markdown). Carries `signal_id` to the body. |
| `src/agents/supervisor.py::_maybe_send_trade_alerts` | `notifier.send(text, parse_mode="")` — plain text. |
| `src/stocks/monitor.py::format_stocks_alert` | Delegates to `setup_alert.render_setup_alert(stocks_subtype=decision.alert_type)`. |
| `src/notifiers/paper_entry.py` | Header now `[🟢 PAPER ENTRY — TRIGGERED]` / `[🔴 ...]` per direction. Compact body. `signal_id:` visible. New `NO-NEWS / NO-DERIV SHORT` flag for crypto intraday shorts without news+derivatives. |
| `src/signals/tracker.py::track_active_signals` | New `close_alert` hook — fires after the existing paper-entry hook, when `outcome.final_outcome` is terminal. Exception-safe; one row per (signal_id, alert_type). |
| `scripts/write_obsidian_current_state_dashboard.py::render_open_trade` | Per-trade label updated to match new headers: `SETUP — WAITING FOR ENTRY`, `PAPER ENTRY — TRIGGERED`, `CLOSE — TP HIT/STOP HIT/EXPIRED/AMBIGUOUS`. |
| `tests/test_paper_entry_alerts.py` | Test 1 + 8 updated to match new header line / `Entry:` field. |

### Headers locked in (final)
```
[🟡 SETUP — WAITING FOR ENTRY]
[🟡 STOCKS SETUP — NEW SIGNAL] / ENTRY CHANGE / SCORE IMPROVEMENT / TIER UPGRADE
[⚠️ STOCKS SETUP — INVALIDATION CHANGE]
[🟢 PAPER ENTRY — TRIGGERED]            (long)
[🔴 PAPER ENTRY — TRIGGERED]            (short)
[✅ CLOSE — TP HIT]
[❌ CLOSE — STOP HIT]
[⏳ CLOSE — EXPIRED]
[⚪ CLOSE — FLAT]
[⚠️ CLOSE — AMBIGUOUS]
[⚠️ SETUP — CANCELLED]
[👀 WATCHLIST — NOT ACTIONABLE]
[🧾 OPERATOR SUMMARY — NOT A TRADE]
[📊 DAILY SUMMARY]
```

## 2. Dry-run sample sizes (within budget)

| Template | Sample length | Budget | OK? |
|---|---:|---:|---|
| Crypto setup | 473 chars | 900 | ✅ |
| Stocks setup (new_signal A-tier with caution) | 480 chars | 900 | ✅ |
| Paper-entry long | 589 chars | 1100 | ✅ |
| Paper-entry short (no-news caution) | 557 chars | 1100 | ✅ |
| Close TP | 228 chars | 700 | ✅ |
| Close stop | 231 chars | 700 | ✅ |
| Operator summary | 151 chars | 3000 | ✅ |

## 3. Required content present in every actionable alert

| Field | Setup | Paper-entry | Close |
|---|---|---|---|
| Type header | ✅ | ✅ | ✅ |
| Asset / Symbol / Direction | ✅ | ✅ | ✅ |
| Playbook | ✅ | ✅ | ✅ |
| Tier / Score | ✅ | ✅ | — (irrelevant post-close) |
| Size weight | ✅ "if entered" | ✅ | — |
| Entry / Stop / TP | ✅ | ✅ (entry+stop+TP) | exit only |
| Status line | ✅ "Waiting for ..." | ✅ "Why now: ..." | ✅ "Result: ±xR" |
| Risk flags | ✅ if present | ✅ if present | — |
| Manual shadow disclaimer | ✅ | ✅ | ✅ |
| `signal_id:` (visible) | ✅ | ✅ | ✅ |
| TradingView link | ✅ | ✅ | — |
| Plain text only | ✅ `parse_mode=""` | ✅ `parse_mode=""` | ✅ `parse_mode=""` |

## 4. Cohort-specific cautions (verified by tests)

| Cohort | Caution surfaced where |
|---|---|
| Crypto scalp | "⚠️ LOW-CONFIDENCE SCALP" in setup + paper-entry |
| Stocks A-tier long intraday | "⚠️ A-tier long caution — 0.5x only" in setup + paper-entry |
| Crypto intraday no-news short | "⚠️ NO-NEWS / NO-DERIV SHORT" in setup + paper-entry (added 2026-06-14) |

## 5. NEW alert types stored in `signal_alerts.alert_type`

| Value | When |
|---|---|
| `close_tp` | first TP hit transition |
| `close_stop` | stop transition |
| `close_expired` | validity window expired without TP/stop |
| `close_flat` | reserved (not currently emitted) |
| `close_ambiguous` | same-bar TP+stop adjudicated conservatively |

Dedup is strict: one row per (signal_id, alert_type) ever. The hook in `tracker.track_active_signals` is wrapped in try/except so a Telegram or DB hiccup never blocks the tracker loop.

## 6. What is NOT changed

| Surface | State |
|---|---|
| Scoring agents | unchanged |
| Threshold values | unchanged |
| TP / SL geometry (`tp1, tp2, tp3, stop_loss, invalidation`) | unchanged |
| Signal generation (`trade_idea_agent`) | unchanged |
| Mode routing | unchanged |
| `config/sizing_weights.yaml` | unchanged |
| Stocks swing / invest pause | unchanged (0× kept) |
| C-tier / shadow / expansion | unchanged (no promotion) |
| Historical `final_r` rows | unchanged |
| Scheduler script | unchanged — restart only after this report is reviewed |
| Telegram collector | unchanged |
| Tracker outcome logic (`_evaluate_signal_walk` / `_classify`) | unchanged |

## 7. Tests

`tests/test_telegram_standardization.py` — **21 passed**:
- 1-4: crypto setup header + "No paper entry yet." + signal_id + no long thesis
- 5-5b: stocks setup sub-type headers + A-tier caution
- 6-6b: paper-entry header for long/short
- 7-8: "System did NOT place a real order." + visible signal_id
- 9: crypto scalp caution flag
- 10: no-news short caution
- 11: stocks A-tier long caution
- 12-15: close alert decide / dedup / never-entered / C-tier paused
- 16: operator summary header + disclaimer
- 17-17b: plain-text parse mode discipline
- 18: surface invariant — no UPDATE / no TP/SL assignment in notifier modules

Full focused regression: **91 / 91 passing** (paper-entry + sizing + playbook + paper-execution + pending revalidation + low-risk + standardization).

## 8. How to deploy

```bash
# (optional, paranoid) run the focused regression
python -m pytest tests/test_telegram_standardization.py \
                 tests/test_paper_entry_alerts.py \
                 tests/test_sizing.py -q

# regenerate the dashboard to pick up new labels
python -m scripts.write_obsidian_current_state_dashboard

# restart only the scheduler/monitor PROCESS to pick up new template renderers.
# (Telegram collector does not need restart.)
```

Next real setup message will display `[🟡 SETUP — WAITING FOR ENTRY]`. Next paper-entry will display `[🟢 PAPER ENTRY — TRIGGERED]` (or `🔴` for shorts). When a trade closes, exactly one `[✅/❌/⏳] CLOSE — ...` message will fire.

## Verdict

```
TELEGRAM_ALERT_STANDARDIZATION_DEPLOYED
```
