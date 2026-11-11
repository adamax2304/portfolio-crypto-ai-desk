# Telegram Alert Taxonomy Audit (PART 1)

**Date:** 2026-06-14 · **Method:** static grep of all `TelegramNotifier.send()` call sites + DB schema cross-check. Read-only.

## 1. Complete taxonomy (all alert sources in the codebase)

| # | Alert family | Source file:fn | Trigger | DB target | alert_type | parse_mode | Actionable? |
|---|---|---|---|---|---|---|---|
| 1 | **Crypto setup alert** | `src/agents/supervisor.py::_maybe_send_trade_alerts` → `_format_idea_alert` | After report cycle: A/B idea exists in `proposed_signals` | `watchlist_alerts` | n/a (column doesn't exist on that table) | **Markdown** (legacy) | Idea / setup waiting for entry |
| 2 | **Stocks setup alert** | `src/stocks/monitor.py::StocksIntradayMonitor.process_signals` → `format_stocks_alert` | After stocks monitor cycle: new/changed A/B signal passes dedup + legal-risk gate | `signal_alerts` | `new_signal` / `entry_change` / `tier_upgrade` / `score_improvement` / `invalidation_change` | **plain text** | Idea / setup waiting for entry |
| 3 | **Paper-entry alert** | `src/notifiers/paper_entry.py::send_paper_entry_alert` (called from `src/signals/tracker.py::track_active_signals`) | Signal transitions from waiting/not_triggered → entry_triggered=1 | `signal_alerts` | `paper_entry` | **plain text** | Actual paper entry — Telegram fires after the system paper-fills |
| 4 | **Operator audit summary** | manual `notifier.send()` in interactive sessions | One-off audit/digest message | none (no DB row) | n/a | varies (usually plain text) | Informational / commentary |
| 5 | **Opus / LLM Telegram sender** | **DOES NOT EXIST** | n/a | n/a | n/a | n/a | n/a |
| 6 | **Legacy untracked alerts** | n/a — alert_type=NULL or signal_id missing | n/a | `signal_alerts` historically; **0 such rows in last 4d** | NULL or `''` | varies | n/a |

### Key clarification: there is no Opus/LLM Telegram path

Opus and the trade-idea LLM agents read packets and write JSON / Markdown reports to disk. They do NOT call `TelegramNotifier.send()` anywhere. The Markdown-rich crypto setup alerts the user perceives as "Opus-style" are actually template (1) — `_format_idea_alert` — produced deterministically by the supervisor after the LLM has already written the idea to `proposed_signals`.

When the operator (or an audit script) sends a one-line summary like `[TP/STOP CATEGORY AUDIT]` or `[CURRENT STATE / MANUAL SHADOW]`, that uses template (4) — direct `notifier.send()` with no DB row. The user may have perceived these as "Opus alerts" because they look like commentary, but they are operator-triggered, not LLM-generated.

## 2. Per-template detail

### (1) Crypto setup alert (`supervisor._format_idea_alert`)
- **Trigger:** the supervisor finishes a scalp/intraday/swing report and finds A/B-tier ideas with valid entry/invalidation.
- **Cooldown:** `notifier.cooldown_minutes` (default 30 min) per symbol, bypassed only on tier upgrade.
- **Format:** Markdown (uses `*bold*` and backticks). Lines: `tier/direction/symbol → score/mode/conf → focus/data → setup` + entry/stop/TP block + thesis.
- **DB write:** `watchlist_alerts(symbol, previous_tier, new_tier, score, direction, mode, payload_json)` — payload includes `signal_id`.
- **Includes signal_id?** Yes (in payload JSON, not as column).
- **Includes playbook?** No (legacy; pre-dates playbook layer).
- **Duplicate risk:** cooldown protects per-symbol; possible cross-template overlap with paper-entry alert when entry triggers within minutes of setup alert.
- **Last 4d:** **50 alerts** (19 intraday / 18 scalp / 13 swing).

### (2) Stocks setup alert (`stocks_monitor.format_stocks_alert`)
- **Trigger:** the stocks intraday monitor cycle finds an A/B signal that passes dedup (cooldown / legal-risk / no-invalidation gates).
- **Decision types:** `new_signal` (first alert) / `entry_change` (entry zone moved) / `tier_upgrade` / `score_improvement` / `invalidation_change`.
- **Format:** **plain text** with `[..]` brackets (fix: 2026-05 brackets switched from Markdown to plain text after `$`-character Markdown parse errors).
- **DB write:** `signal_alerts(alert_id, signal_id, asset_class='stocks', mode, symbol, tier, score, direction, sent_at, alert_type, telegram_status, message_hash, payload_json)`.
- **Includes signal_id?** Yes (column).
- **Includes playbook?** Indirectly via setup_type; no explicit playbook field.
- **Duplicate risk:** dedup via `last_signal_alert_for_setup(asset_class, symbol, mode, direction)`. Last 4d shows **2 same-signal+entry_change duplicate pairs** which is the dedup intentionally allowing repeated entry-change updates when zone keeps moving.
- **Last 4d:** **17 alerts** (1 new_signal, 10 entry_change, 3 score_improvement, 2 tier_upgrade, 1 invalidation_change).

### (3) Paper-entry alert (`paper_entry.send_paper_entry_alert`)
- **Trigger:** `tracker.track_active_signals` detects `outcome.entry_triggered=True` AND `prev_status` was a pending status. Gated by tier ∈ {A, B}, asset/mode (no stocks swing/invest), playbook not in paused set.
- **Format:** plain text (`parse_mode=""`).
- **DB write:** `signal_alerts(alert_type='paper_entry', payload=full dict with rationale + risk flags + size_weight)`.
- **Includes signal_id?** Yes.
- **Includes playbook?** Yes (`payload.playbook`).
- **Includes LLM rationale?** No, but it pulls `rationale_summary` from existing `raw_idea_json` evidence (which originally came from the LLM at proposal time).
- **Duplicate risk:** strict dedup via `has_existing_paper_entry_alert(signal_id)` — one paper_entry row per signal_id ever.
- **Last 4d:** **168 alerts** — 27 crypto, 141 stocks. `telegram_status`: 129 `dry_run`, 56 `sent`. **`dry_run` means the row was recorded but the message was NOT actually delivered to the user's Telegram** (this happens when the audit was run with `--paper-entry-dry-run`).

### (4) Operator audit summary
- Direct `notifier.send(text)` call. Examples this week: TP/STOP CATEGORY AUDIT, CURRENT STATE / MANUAL SHADOW.
- **DB write:** none.
- Not tracked, not deduped, not actionable in the trading sense. Pure commentary.

### (5) Opus / LLM Telegram sender
- **Does not exist.** Verified by grep across `src/` — no LLM agent or Opus-handling code path calls `TelegramNotifier.send()`.

## 3. Cross-template duplicate risk

- 3 cases in the last 4 days where the same symbol appears in `watchlist_alerts` (crypto setup) AND `signal_alerts` (paper_entry) within 1 hour. This is **expected lifecycle behavior**: setup fires when the idea is proposed; paper-entry fires when the price actually touches the entry zone. **Not a bug.**
- Within `signal_alerts.alert_type='entry_change'`: 2 signals with multiple entry_change rows (3 and 2). Also expected — operator wants to know when entry zone keeps moving.

## 4. Coverage gaps

- **No "close / outcome" Telegram alert exists.** The user has no notification when a paper trade hits TP/stop. They must read the dashboard or check the journal.
- **No "stale_before_entry" or "entry_moved_away" notification.** The signal silently transitions; the operator only sees it if they look.
- **No daily summary alert.** Only the operator-triggered manual summaries (template 4) exist.

## 5. Bottom line

Three template families produce *trackable* Telegram messages: crypto setup (Markdown), stocks setup (plain text, 5 sub-types), paper-entry (plain text, dedup-strict). One template is operator-triggered and untracked. There is **no Opus or LLM Telegram sender** in the system; any "Opus-style" alert the operator perceives is either the crypto-setup Markdown template or a manual operator audit summary.
