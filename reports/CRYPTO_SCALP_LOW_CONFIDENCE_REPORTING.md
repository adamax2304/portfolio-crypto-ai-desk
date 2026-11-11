# Crypto Scalp — Low-Confidence Reporting (Fix Report)

**Date:** 2026-06-09 · **Scope:** Mark crypto scalp output as low-confidence in user-facing surfaces. **No scoring/TP/SL/routing changes.** Crypto scalp A/B remains fully actionable; no demotion, no Telegram suppression.
**Audit reference:** [CRYPTO_SCALP_VIABILITY_AUDIT.md](CRYPTO_SCALP_VIABILITY_AUDIT.md) + [MODE_ROUTING_DECISION_RECOMMENDATION.md](MODE_ROUTING_DECISION_RECOMMENDATION.md).

## 1. What changed (3 reporting surfaces)

### 1.1 Crypto report header banner
File: [src/reports/report_builder.py](src/reports/report_builder.py) — `ReportBuilder.build_daily`

Added a header banner block immediately after the metadata block (Date / Generated / Mode / Data freshness / Market regime), rendered **only** when `mode == "scalp"`:

> **CRYPTO SCALP — low confidence.** Entry edge exists (100% of expired scalps had positive MFE, avg +0.54R) but TP1/2h horizon mismatch caps capture (1W/7L over 14d, PF 0.14). Scalp remains active for data collection; re-audit at 20 closed A/B scalp signals. Treat A/B scalp ideas with lower confidence than intraday/swing.

The banner appears in every scalp report (live + `--no-update` cached), and propagates into the LLM analysis packet through the existing "Latest Scalp Report" excerpt section.

### 1.2 Supervisor Telegram alert (crypto pipeline)
File: [src/agents/supervisor.py](src/agents/supervisor.py) — `_format_idea_alert`

When `mode == "scalp"` and `idea.asset_class == "crypto"`, the supervisor appends a single annotation line right under the score/mode/conf header:
```
low confidence mode audit — entry edge OK, TP1/2h horizon mismatch caps capture; re-audit at 20 closed
```
Entry / SL / TP1-3 / thesis / caps / report-id are all still emitted — **no suppression**. Annotation only.

### 1.3 Watchlist monitor Telegram alert
File: [src/agents/watchlist_monitor.py](src/agents/watchlist_monitor.py) — `WatchlistMonitor.format_alert`

Same annotation pattern as above, scoped to `mode == "scalp"` AND `asset_class == "crypto"`. The `monitor-watchlist` CLI uses `parse_mode=""` (plain text), so the annotation renders verbatim and does not affect alert delivery.

## 2. What this fix does NOT do
- **Does not pause crypto scalp.** A/B scalp ideas are still registered as proposed signals.
- **Does not demote crypto scalp to C.** Tier assignment is untouched.
- **Does not restrict crypto scalp to catalyst-only.** Audit found catalyst-backed scalp is *worse* than no-catalyst (0W/2L vs 1W/5L) in the 14d window — restricting would strip the only win.
- **Does not suppress Telegram alerts.** Per the user spec: "Do not suppress Telegram A/B scalp alerts solely because of this tag."
- **Does not change scoring/TP/SL/horizon.** The TP1 / 2h mismatch identified in PART 2 of the audit is a strategy-layer concern and is **out of scope** for this fix.
- **Does not affect crypto intraday or crypto swing.** Banner / annotation are scoped to `mode == "scalp"`.
- **Does not affect stocks.** The watchlist-monitor annotation is gated on `asset_class == "crypto"` (verified by `test_telegram_stocks_scalp_does_not_get_crypto_note`).

## 3. Tests
File: [tests/test_crypto_scalp_low_confidence.py](tests/test_crypto_scalp_low_confidence.py) — 6 new tests:

| Test | Asserts |
|---|---|
| `test_scalp_report_renders_low_confidence_banner` | Banner present in scalp report; contains "TP1/2h horizon mismatch" and "re-audit at 20 closed" |
| `test_intraday_report_has_no_scalp_banner` | Banner absent from intraday report |
| `test_swing_report_has_no_scalp_banner` | Banner absent from swing report |
| `test_telegram_scalp_alert_includes_low_confidence_line` | Watchlist monitor scalp alert has annotation + entry/SL still rendered |
| `test_telegram_intraday_alert_has_no_low_confidence_line` | Intraday alert has no annotation |
| `test_telegram_stocks_scalp_does_not_get_crypto_note` | Stocks-scalp (hypothetical) does not get the crypto-specific note |

All 6 pass.

## 4. Verification — live scalp report
Ran `python -m src.cli scalp-report --no-update`. Output:
```
Scalp report saved: data/reports/scalp/2026-06-09_13-46_scalp_report.md
LLM packet refreshed: data/processed/llm_analysis_packet.md
```
Header excerpt of the generated report:
```
# Crypto AI Desk Report

Date: 2026-06-09
Generated at: 2026-06-09 16:46:01 EEST
Mode: scalp
Data freshness: 2026-06-09 13:30:00+00:00
Market regime: range/chop (neutral)

> **CRYPTO SCALP — low confidence.** Entry edge exists (100% of expired scalps had positive MFE, avg +0.54R) but TP1/2h horizon mismatch caps capture (1W/7L over 14d, PF 0.14). Scalp remains active for data collection; re-audit at 20 closed A/B scalp signals. Treat A/B scalp ideas with lower confidence than intraday/swing.

## 0. Exchange Coverage & Candidate Funnel
...
```
Banner renders at the top, immediately under the metadata block, before any A/B/C tier output. Verified.

## 5. Re-audit trigger
Per [MODE_ROUTING_DECISION_RECOMMENDATION.md](MODE_ROUTING_DECISION_RECOMMENDATION.md): re-audit crypto scalp **when closed A/B reaches 20 signals** (current: 8 of 55). At the observed rate (≈8 closures / 14 d), that is ≈3 more weeks. If at that point WR/PF improve materially, drop the banner; otherwise consider strategy-layer changes (TP1/horizon).

## Final
```
CRYPTO_SCALP_LOW_CONFIDENCE_REPORTING_DEPLOYED
```
