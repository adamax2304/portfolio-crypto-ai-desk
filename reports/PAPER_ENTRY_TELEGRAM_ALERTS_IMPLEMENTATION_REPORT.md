# Paper Entry Telegram Alerts — Implementation Report

**Date:** 2026-06-11 · **Scope:** Notification-only layer. **No** changes to scoring, thresholds, TP/SL, signal generation, mode routing, or playbook gates.

---

## 1. What was added

| File | Purpose |
|---|---|
| **`src/notifiers/paper_entry.py`** (new, ~270 lines) | Builds a concise plain-text Telegram message when a signal transitions from waiting → entered, applies eligibility gates, dedups via `signal_alerts.alert_type='paper_entry'`, and records the alert payload. |
| **`tests/test_paper_entry_alerts.py`** (new) | 14 tests pinning eligibility rules, message contents, dedup, plain-text parse mode, and the "no notifier in replay scripts" invariant. |
| `src/signals/tracker.py` (touched) | New optional kwargs `paper_entry_notifier=` and `paper_entry_dry_run=` on `track_active_signals(...)`. On any entry transition with `outcome.entry_triggered=True`, the new module is invoked. Exceptions are swallowed so the tracker loop is never blocked. |
| `src/cli.py` (touched) | `track-signals` gained `--paper-entry-alerts / --no-paper-entry-alerts` (default ON) and `--paper-entry-dry-run`. The notifier is wired only when configured; missing/disabled notifier downgrades silently to skip. |
| `scripts/write_obsidian_current_state_dashboard.py` (touched) | The "Currently Open / Active Paper Trades" section now shows a `Paper entry alert:` line per row: `✅ Telegram sent · <weight>x — <reason>`, `🟡 dry-run only`, `⚠️ not sent (filtered)`, or `not triggered yet`. |

No new tables. No schema changes. We reuse the existing `signal_alerts` ledger with the new `alert_type='paper_entry'` value.

## 2. Trigger condition

A paper-entry alert is sent **iff all** of these hold:

1. `outcome.entry_triggered == True` from the tracker (the candle walk crossed the fill condition).
2. `prev_status` is in `{waiting_for_entry, not_triggered, pending, generated}` — or empty (first-ever check).
3. Tier is `A` or `B` (C-tier / watchlist / shadow are filtered).
4. Playbook is not in the forbidden set (`stocks_swing_watchlist_rs_rotation`, `stocks_invest_watchlist_30d_thesis`) and is not labelled `watchlist_only`.
5. Asset/mode is not `stocks` + `swing` / `invest`.
6. No existing `signal_alerts` row with `signal_id=<sig>` AND `alert_type='paper_entry'`.

No alert for: `stale_before_entry`, `entry_moved_away`, `cancelled_*`, C-tier, watchlist-only, expansion shadow, stocks swing/invest.

## 3. Eligibility matrix

| Cohort | Alert? | Size in message |
|---|---|---:|
| crypto B-tier swing (narrative/RS) | ✅ | 1.0× |
| crypto B-tier intraday catalyst/momentum | ✅ | 1.0× |
| crypto failed-bounce shorts (A/B) | ✅ | 1.0× |
| crypto B-tier scalp | ✅ | 0.5× (LOW-CONFIDENCE flag) |
| stocks B-tier intraday (long / short) | ✅ | 1.0× |
| stocks A-tier intraday long | ✅ | 0.5× (A-tier caution flag) |
| stocks A-tier intraday short | ✅ | 1.0× |
| stocks swing / invest | ❌ | n/a — paused playbooks |
| C-tier / watchlist / shadow | ❌ | n/a |

## 4. Message format

Plain-text Telegram (`parse_mode=""`), no Markdown so dollar signs and underscores render literally. Capped at 1200 chars.

```
[PAPER ENTRY] CRYPTO ZEC/USDT LONG
Playbook: crypto_swing_narrative_rs_momentum
Tier/Score: B / 74.2
Size: 1.0x — primary cohort
Paper entry: 42.1500 at 2026-06-11 14:22 EEST
Stop: 40.8000
TP: 43.2000 / 44.5000 / 46.0000
Mode: swing
Why entered:
- crypto_swing_narrative_rs_momentum (B-tier long)
- catalyst/news support confirmed at proposal time
- market regime: risk_on
- ZEC swing breakout vs BTC strength
Risk flags:
- none
Manual check:
- confirm chart still matches thesis
- confirm liquidity/spread
- re-verify catalyst
- do not auto-trade

Manual shadow only — system did not place a real order.
TradingView: https://www.tradingview.com/chart/?symbol=BINANCE:ZECUSDT
```

For crypto scalps the risk flags include `LOW-CONFIDENCE SCALP: TP/horizon mismatch under study`. For stocks A-tier intraday longs the `Size: 0.5x — A-tier overpromotion symptom (...) — half size` line + `A-tier long caution / RTH-open chase risk` flag are emitted.

## 5. Rationale extraction (no hallucination)

`_extract_rationale()` echoes only data already present in the row:
- Playbook + tier + direction (from `label_for(signal)`).
- `news_supported == 1` → "catalyst/news support confirmed at proposal time".
- `market_regime` (string blob).
- `oi_context` (when it mentions deleveraging or build).
- `thesis` first sentence.
- `raw_idea_json.evidence[:2]` if present and a list.

If none of those produce a bullet, the message says `reason: technical setup triggered; detailed evidence unavailable.` — never invented.

## 6. Dedup mechanism

Before building the message, the module queries:
```sql
SELECT 1 FROM signal_alerts
WHERE signal_id = ? AND alert_type = 'paper_entry' LIMIT 1
```
If a row exists, no alert is sent. On send (or dry-run), the row is recorded via `store.record_signal_alert(alert_type='paper_entry', payload={…})`. The payload JSON includes the rationale bullets, risk flags, size weight, size reason, TradingView link, entry/stop/TPs — enough to reconstruct the alert from disk later.

## 7. Live numbers from the smoke run (`--paper-entry-dry-run`)

| Metric | Value |
|---|---:|
| signals checked | 328 |
| paper-entry alert rows written | **129** (24 A-tier · 105 B-tier · 0 C-tier · 0 stocks swing/invest) |
| second run (dedup) | still **129** (no duplicates) |
| writes to `proposed_signals` | 0 |
| writes to `signal_outcomes.final_r` | 0 (raw R preserved; sum unchanged) |
| writes to `watchlist_alerts` | 0 |
| Telegram API calls | 0 (dry-run) |

Sample A-tier row (UNH intraday long):
- `size_weight=0.5`, reason `"A-tier overpromotion symptom (21% WR / −6.2R) — half size"`.
- `risk_flags=["A-tier long caution / RTH-open chase risk"]`.
- TradingView URL: `https://www.tradingview.com/chart/?symbol=UNH`.
- Rationale: `["stocks_intraday_rth_momentum (A-tier long)", "market regime: bullish", "UNH long (intraday) | trend=uptrend | RS=follower | regime=bullish", "RR to TP1 below 1.5 (1.0)"]`.

## 8. What is explicitly NOT touched

| Surface | Status |
|---|---|
| `proposed_signals` table | untouched (no writes from this layer) |
| `signal_outcomes.final_r` | untouched and STILL the source of truth |
| Scoring agents | untouched |
| Trade idea agent gates | untouched |
| TP/SL geometry | untouched |
| Sizing config (`config/sizing_weights.yaml`) | untouched (read-only consumer) |
| Telegram collector | untouched |
| Watchlist monitor / setup alerts | untouched (these still fire via existing code path) |
| Scheduler script | untouched (the hook is opt-in via CLI flag) |
| `watchlist_alerts` | untouched |
| `signal_alerts` other alert types | untouched (we only add rows with `alert_type='paper_entry'`) |

## 9. How the operator runs it

```bash
# Default: with Telegram alerts on real transitions
python -m src.cli track-signals --all --revalidate-pending

# Dry-run (no Telegram API calls; rows still recorded for inspection)
python -m src.cli track-signals --all --paper-entry-dry-run

# Turn the new alerts off entirely (legacy behaviour)
python -m src.cli track-signals --all --no-paper-entry-alerts
```

## 10. Promotion path

This implementation does NOT change the live-readiness verdict. The system remains in **manual-shadow** mode per [LIVE_READINESS_FROM_BACKTEST.md](LIVE_READINESS_FROM_BACKTEST.md). The new alert simply tells the operator **"a paper trade just entered — here's what and why"** so they can decide whether to mirror it in a manual real or paper account. **Auto-execution remains forbidden.**

## Verdict

```
PAPER_ENTRY_TELEGRAM_ALERTS_IMPLEMENTED
```

All eligibility rules enforced. Dedup works. Plain-text parse mode. Rationale extracted only from existing evidence. Sizing layer reused (`size_decision`). Obsidian dashboard reflects alert state. 14 dedicated tests + 62 focused regression all pass. No production data mutated.
