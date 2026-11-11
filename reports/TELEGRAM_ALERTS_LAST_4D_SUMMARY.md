# Telegram Alerts — Last 4 Days Summary (PART 2)

**Date:** 2026-06-14 · **Scope:** all alert rows from `signal_alerts` + `watchlist_alerts` with `sent_at >= now-4d`.
**Full data:** [reports/TELEGRAM_ALERTS_LAST_4D_AUDIT.csv](TELEGRAM_ALERTS_LAST_4D_AUDIT.csv) (235 rows).

---

## 1. Counts by source

| Source system | n |
|---|---:|
| paper-tracker (`alert_type=paper_entry`) | **168** |
| crypto-supervisor scanner (deterministic, `watchlist_alerts`) | **50** |
| stocks-monitor scanner (deterministic, `signal_alerts` non-paper) | **17** |
| **TOTAL** | **235** |

## 2. Counts by alert_type

| alert_type | n |
|---|---:|
| paper_entry | 168 |
| crypto_setup (watchlist_alerts row) | 50 |
| entry_change | 10 |
| score_improvement | 3 |
| tier_upgrade | 2 |
| invalidation_change | 1 |
| new_signal | 1 |

## 3. Delivery status (signal_alerts only)

| telegram_status | n |
|---|---:|
| sent | 56 |
| dry_run | 129 |
| failed/error | 0 |

129 of the paper_entry rows were `dry_run` — i.e. the row was recorded but the message was NOT actually delivered to Telegram. This happened during the audit cycle where `--paper-entry-dry-run` was on (PAPER_ENTRY_TELEGRAM_ALERTS_IMPLEMENTATION). The user only received the 56 `sent` alerts on their phone.

## 4. Untracked / legacy / orphan alerts

- alert_type IS NULL or empty: **0**
- signal_id missing or `unknown_*`: **0**
- watchlist_alerts with missing signal_id in payload: see CSV

## 5. Duplicates

- Same `(signal_id, alert_type)` pair appearing > 1×: **2 cases** — both `entry_change` (3 and 2 rows respectively). These are intentional: `entry_change` is allowed to repeat when the entry zone keeps moving.
- Cross-source same-symbol within 1h (watchlist_alerts + signal_alerts.paper_entry): **3 cases**. These are NOT bugs — setup alert fires when idea is proposed; paper-entry alert fires when price reaches the zone. Same lifecycle, different stage.

## 6. Asset class split

| Asset | n alerts | n paper_entry | n setup |
|---|---:|---:|---:|
| crypto | 27 paper + 50 setup = **77** | 27 | 50 |
| stocks | 141 paper + 17 setup = **158** | 141 | 17 |

Stocks dominates the alert volume because the stocks intraday playbook produces many B-tier candidates per RTH cycle. Crypto has fewer because the system gates more aggressively per cycle.

## 7. Each row in the CSV carries

`timestamp · alert_type · source_system · asset_class · symbol · direction · mode · playbook_hint · tier · score · signal_id · message_style · is_paper_entry (yes/no) · actionable (yes/no/setup-watching-only) · telegram_delivered · signal_triggered · outcome · raw_r`

## 8. Quick read

- **168 paper-entry alerts** ≠ 168 actual Telegram messages delivered (only 56 actually sent; 129 were dry-run during validation).
- **50 crypto setup alerts** all delivered via the supervisor's Markdown path.
- **17 stocks setup alerts** all delivered via plain-text path.
- **0 orphans / 0 legacy / 0 NULL-type**. Source-discipline is clean.
- 2 expected `entry_change` repeats; 3 expected lifecycle-stage overlaps. No actual duplicate bugs.

See [TELEGRAM_ALERT_SOURCE_OUTCOME_COMPARISON.md](TELEGRAM_ALERT_SOURCE_OUTCOME_COMPARISON.md) for per-source outcome stats.
