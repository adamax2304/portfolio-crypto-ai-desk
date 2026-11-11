# POST-CATALYST-FIX DATA INTEGRITY + APP RESULTS CORRECTION — Final Report

**Date:** 2026-06-20. **Scope:** make the Telegram Mini App / backend report **honest** numbers (correct Today R, Operator/Paper/Shadow separation, economic dedup, latest/terminal outcome, catalyst/regime/delivery/near-winner visibility). **No trade logic changed.**

## 0. Catalyst linkage refresh baseline verification — `CATALYST_LABEL_REFRESH_BASELINE_OK`
Verified the already-shipped fix is live and not regressed: `src/signals/catalyst_label_refresh.py` exists; CLI `catalyst-label-refresh` registered; scheduler step `catalyst_label_refresh_step` is **`command_nonfatal`, placed right after `catalyst_integrity_step`**; `signal_catalyst_labels.computed_at` fresh (2026-06-20T17:25Z); **78/78** last-2-day signals labelled; **6** `test_catalyst_label_refresh` tests pass. Flags are additive only — ORDI/EDEN correctly remain `0` (substring noise: "Ordinals"/"Sweden"), while ONDO/WLD/XLM/AVAX/SUI genuine hits are flagged. No scoring/routing path touched. **Not reimplemented.**

## 1. Root cause of wrong app Today R — `APP_PNL_ROOT_CAUSE_FOUND`
The app showed ~**−26R**. Source: [frontend/src/screens.tsx](../trading-desk-control/frontend/src/screens.tsx) — `todayR = signals.filter(final_r!=null).reduce(...)` over `/api/signals` = `list_signals(200)`. That number:
- spanned **5 days** (06-16…06-20), not "today" — no date boundary;
- **mixed all books** — shadow (crypto scalp, C-tier, stocks swing/invest) summed with actionable;
- **no economic dedup** — duplicate signal_ids for one setup each added their R;
- treated raw `final_r` uniformly (no terminal-only / expired-unresolved separation).

Exact decomposition (reproduced against the live DB): **−26.0R = Paper d7 (−22R) + Shadow d7 (−4R)**. The raw `signal_outcomes` row-sum is +229,680R (time-series rows) — proof the read model, not the data, was wrong.

## 2. Canonical books — `CANONICAL_BOOKS_DEFINED`
New `trading-desk-control/backend/app/books.py` (read-only): `economic_trade_key`, `derive_trade_book`, `in_book`, `outcome_class`, `realized_r`, `is_closed`, `close_time`, `collapse_economic_trades`, `get_closed_trades`, `get_dashboard_summary`, `near_winner_expired`, `close_reason`, `plain_explanation`. Books: **Operator** (A/B, delivered=`sent`), **Paper** (actionable-by-policy incl. delivery-failed; superset of Operator), **Shadow** (scalp/C-tier/stocks-swing-invest/sector-cap/late-shadow/blocked), **Research** (all).

## 3. Economic dedup + outcome read-model — `ECONOMIC_TRADE_DEDUP_ENABLED` · `APP_TODAY_R_FIXED`
- Latest outcome per signal; **terminal preferred** over a later stale "open" row.
- Dedup by `economic_trade_key` (symbol·class·mode·dir·tier·playbook·rounded-entry·day); representative = most-resolved; exposes `duplicates_collapsed_count` + `duplicate_signal_ids`.
- **Realized R only from terminal win/loss/flat.** Expired-after-entry = **unresolved (not PnL)**; no-entry/waiting excluded.
- Default Today R = **Operator Book, deduped, terminal-realized, shadow-excluded, explicit UTC day.**
- 11 `test_books.py` tests lock these (10-dup→1, raw rows don't inflate, shadow excluded from Operator R, terminal-over-stale, expired≠PnL, win-with-neg-R→needs-review, books differ).

## 4. Catalyst display — `CATALYST_LABELS_VISIBLE_IN_APP` · `NO_FALSE_NO_CATALYST_LABELS`
Adapter now returns `news_supported`, `telegram_supported`, `catalyst_supported` (tri-state), `catalyst_freshness`, `catalyst_headline`, `catalyst_label_computed_at`. UI shows **"catalyst / technical-only / catalyst unknown"** — **unknown** (not false "no catalyst") when no label row / linkage stale. ORDI/EDEN not marked supported.

## 5. Market regime — `MARKET_REGIME_VISIBLE_OR_UNKNOWN_SAFE`
Adapter returns `market_regime`; UI shows it or **"unknown"** when blank (still sparse ~30%; not faked). TODO (data-only): persist regime at signal creation — added to Friday checklist.

## 6. Closed Trades UX — `CLOSED_TRADES_TAB_HUMAN_READABLE` · `DASHBOARD_R_BOOKS_SEPARATED`
New `ClosedBook` view: Book (Operator/Paper/Shadow) + Date (Today/48h/7d) + Outcome filters; per-book R header ("realized from terminal closes only · W/L/Flat · expired-unresolved · dupes collapsed"); rich rows (symbol/dir/asset/mode/tier, outcome badge, R, MFE/MAE, delivery badge, catalyst tri-state, regime, dup count) + detail drawer (timeline: created→entry→entry-alert→close, plain-English close reason, levels, collapsed-dup note). Home dashboard now shows **Today R · Operator**, **48h R · Operator (W/L)**, Open risk, **Shadow 48h R**, + a note line with Paper/Shadow/delivery-gap/dupes and the headline definition.

## 7. Telegram delivery — `TELEGRAM_DELIVERY_STATUS_VISIBLE` · `READTIMEOUT_RETRY_SAFE`
Adapter surfaces `entry_alert_status`/`close_alert_status`; UI shows per-trade delivery badges + a dashboard delivery-gap count. `src/notifiers/telegram.py` `send()` now does **one retry on transient `ReadTimeout`/`ConnectTimeout`** (1.5s backoff); non-timeout errors are not retried; alert-row idempotency preserved by the caller's (signal_id, alert_type) dedup. 3 `test_telegram_retry` tests (retry-success / give-up / no-retry-on-HTTPError).

## 8. Near-winner expired diagnostics — `NEAR_WINNER_EXPIRED_DIAGNOSTIC_ADDED`
`/api/near-winners` + `near_winner_expired()` (expired-after-entry, MFE ≥ 0.8R). UI panel labelled **"Diagnostic only — does not change exits."**

## 9. Corrected recent results — `RECENT_RESULTS_RECONCILED`
Deduped, terminal-realized, against the live DB:
| Book | Today R | 48h R | 7d R |
|---|---|---|---|
| **Operator** | **+2.0** | **−1.0** (W4/L9) | −13.0 |
| Paper | 0.0 | −3.0 | −22.0 |
| Shadow | +1.0 | −1.0 (25 expired) | −4.0 |

App **−26R explained** = Paper d7 (−22) + Shadow d7 (−4), summed with no dedup / no day boundary. Operator (what the operator should judge as "my book") is **−1R over 48h** — the same noise-level result as the loss analysis, NOT −26R.

## 10. Tests — `APP_AND_DATA_TESTS_PASS`
Control Plane backend **49 passed** (incl. 11 books); crypto focused **89 passed** (display/status, telegram standardization, **telegram retry**, catalyst_label_refresh, default_market_schedule, project_state_docs); frontend `tsc -b` exit 0 + `vite build` ok; scheduler dry-run LLM-guard OK ("no Opus/Claude tokens in plan"); docs validator OK. Endpoints wired (live tunnel: `/api/health` 200; `/api/dashboard/summary`, `/api/closed/operator`, `/api/near-winners` → 401 auth-required vs 404 for bogus route → routes exist).

## 11. Final system sanity — `FULL_SYSTEM_SANITY_OK` · `NO_TRADE_LOGIC_CHANGE`
Trading core intact (`CryptoAIDeskMonitor` scheduler single instance, heartbeat healthy). Control Plane app stack restarted on the new code under the `CryptoAIDeskApp` keeper; one operational fix to the launcher: **backend health-wait widened 20→60s** in `launch_robust.ps1` (cold uvicorn start on a loaded box exceeded 20s, which had made the launcher abort before starting cloudflared/bot — root cause of restart flakiness). Unchanged: scoring · TP/SL · entry logic · routing/actionability · filters · validity windows · risk limits · live/auto-live (locked) · scalp/C-tier/stocks-swing-invest (still shadow) · historical `final_r`/`final_outcome`/`status`/`entry_triggered`. `load_recent_news(limit=100)` scan-time path untouched.

## 12. Docs — `DOCS_UPDATED`
`PROJECT_STATE.md` (app R correction block), `docs/DECISION_LOG.md` (row), `docs/WEEKLY_FORWARD_METRICS.md` (Operator/Paper/Shadow reconciliation, catalyst freshness, regime coverage, delivery errors, near-winner panel), `docs/SHADOW_MODE_REGISTRY.md` (note: data/UI correctness ≠ shadow promotion).

## 13. Answers
1. **Already fixed before this run:** app-stack persistence (`CryptoAIDeskApp` keeper), status/lifecycle display, Agent Council prompt, shadow-promotion audit, catalyst linkage refresh.
2. **catalyst_label_refresh verified?** Yes — live, in scheduler (non-fatal, post-integrity), idempotent, fresh, tests pass; not reimplemented.
3. **Why ~−26R?** Frontend summed raw `final_r` over 200 signals / 5 days / all books / no dedup = Paper d7 (−22) + Shadow d7 (−4).
4. **Operator Book R:** today **+2.0R**, 48h **−1.0R**.
5. **Paper Book R:** today 0.0R, 48h −3.0R.
6. **Shadow Book R:** today +1.0R, 48h −1.0R (25 expired).
7. **Dedup:** `economic_trade_key` collapses duplicate signal_ids → one trade; count + ids surfaced.
8. **Backend read-model:** new `books.py`; adapter adds delivery + catalyst-label + regime fields; endpoints `/api/dashboard/summary`, `/api/closed/{book}`, `/api/near-winners`.
9. **Closed tab:** book/date/outcome filters, rich rows, detail-drawer timeline + plain close reasons, delivery + catalyst + regime + dup badges, near-winner panel.
10. **Dashboard Today R:** Operator Book, deduped, terminal-realized, shadow-excluded, UTC day (labelled).
11. **Catalyst fields shown:** supported/technical-only/**unknown** + freshness + headline + computed_at (no false "no catalyst").
12. **Regime fields shown:** `market_regime` or **unknown** (never faked).
13. **Telegram delivery:** per-trade status + dashboard gap count; one safe ReadTimeout retry.
14. **Near-winner diagnostics:** expired-after-entry with MFE ≥ 0.8R, diagnostic-only.
15. **Tests passed:** 49 backend + 89 crypto + tsc/build + docs + dry-run guard.
16. **NOT changed:** scoring/TP-SL/entry/routing/filters/validity/risk/live/scalp/C-tier/stocks-swing-invest/historical outcomes; scan-time news window.
17. **Operator manual check:** open @aitradingdesk1_bot → **menu button** → Dashboard shows "Today R · Operator" (≈ small, not −26R); Trades → **closed** → toggle Operator/Paper/Shadow + date; confirm rows show outcome + close reason + delivery + catalyst + regime; near-winner panel diagnostic-only.
18. **Friday review:** Operator/Paper/Shadow reconciliation; catalyst-label freshness; regime coverage (persist-at-creation TODO); delivery-error counts; near-winner-by-mode; re-evaluate any promotion only at ≥15 closed actionable.

## Verdicts
`CATALYST_LABEL_REFRESH_BASELINE_OK · APP_TODAY_R_FIXED · CANONICAL_BOOKS_DEFINED · ECONOMIC_TRADE_DEDUP_ENABLED · CATALYST_LABELS_VISIBLE_IN_APP · MARKET_REGIME_VISIBLE_OR_UNKNOWN_SAFE · CLOSED_TRADES_TAB_HUMAN_READABLE · DASHBOARD_R_BOOKS_SEPARATED · TELEGRAM_DELIVERY_STATUS_VISIBLE · READTIMEOUT_RETRY_SAFE · NEAR_WINNER_EXPIRED_DIAGNOSTIC_ADDED · RECENT_RESULTS_RECONCILED · FULL_SYSTEM_SANITY_OK · NO_TRADE_LOGIC_CHANGE · READY_FOR_FORWARD_MONITORING`
