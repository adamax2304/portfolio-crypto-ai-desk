# Crypto AI Desk — Project State

> Single source of truth for current status, locked rules, active verdicts, and next decision gates.
> **Every agent must update this file (and `docs/DECISION_LOG.md`) after doing work.** See `docs/AGENT_HANDOFF.md`.

## Last Updated
2026-06-24 — after TRADE-DETAIL CHART-FIRST + TRUE PARTIAL-EXIT MARKERS + MARKET VIX + MOBILE-OVERFLOW follow-up fix (same day: execution UI + lifecycle + market dashboard + max-5x; structural-TP/maker-first; bugfix; upgrade; shadow→paper; risk upgrade).

> **Trade UI + partial markers + VIX + overflow follow-up (2026-06-24): TRUE_PARTIAL_EXIT_EVENTS_AVAILABLE + FULL_CHART_OVERLAY_SHOWS_PARTIAL_EXITS + TRADE_DETAIL_OPENS_CHART_FIRST + PRICE_LADDER_SHOWS_OUTCOMES_CLEARLY + ACTIVE_POSITIONS_REMAIN_AFTER_PARTIAL_TP + STRUCTURAL_STOP_MOVEMENT_VERIFIED + SIGNALS_CARDS_NO_OVERFLOW + MARKET_TAB_VIX_AND_DATA_LOADED + OPUS_ROUTINE_FEEDS_MARKET_DASHBOARD + NO_LIVE_EXECUTION_ENABLED + HISTORICAL_FINAL_R_UNCHANGED.** PAPER/app/read-model only. ENA/USDT +3R "single exit near TP1/TP2" root cause = the candlestick **`frontend/src/Chart.tsx` drew one `overlays.exit_at` marker and ignored chart-events**; backend was already correct (3 tp_fill). Fixes: (1) chart-events markers enriched to the full execution schema (cumulative R/$, side, source_book, is_partial/final, event_type, marker_id) + `lines`; (2) `Chart.tsx` now renders lifecycle markers + entry/stop/moved-stop/TP1-3 price lines, drops the single generic exit (ENA live: tp_fill=3, genericExit=0, lines=6); (3) **TradeDetail is chart-first** (candlestick → PnL → `PriceLadderTable` → lifecycle → setup); all trade clicks (incl. Closed rows) route there; (4) **price-ladder outcome table** (Stop/Entry/TP1-3 · price·R·net$·status); (5) active-after-TP1 partial badges + next-target; (6) structural-stop manager verified (fallback clearly labelled where backend has no candles); (7) **Signals card overflow fixed** (KV min-w-0+break-words, KVsm, grid-cols-2 + full-width TP row); (8) **Market VIX** via deterministic `fetch_market_extras` (yfinance ^VIX + SPY/QQQ trend + ETH/BTC), backfilled in the Opus parser/fallback/populate so VIX is never blank (live: VIX 19.7); Market tab shows "VIX unavailable" explicitly otherwise. 43 crypto + 72 backend tests pass; frontend build clean (92 modules); stack live (clean `launch_robust`). No live/exec; production TP/scoring/routing unchanged; `final_r` not rewritten. See `reports/TRADE_UI_MARKET_FIX_FINAL_REPORT.md` (+14 part reports).

> **Execution UI + lifecycle + market dashboard + max-5x (2026-06-24): MAX_5X_SAFE_LEVERAGE_POLICY_ACTIVE_FOR_PAPER + PAPER_POSITION_LIFECYCLE_WITH_PARTIAL_EXITS_READY + STRUCTURAL_STOP_MOVEMENT_AFTER_TP_READY + FULL_CHART_OVERLAY_SHOWS_TRUE_EXECUTION_EVENTS + TRADE_DETAIL_UI_EXCHANGE_LIKE + ACTIVE_POSITIONS_SHOW_PARTIALS + REGIME_UNKNOWN_REDUCED + MSTR_LATE_ENTRY_FIXED + MARKET_TAB_REDESIGNED + OPUS_UPDATES_MARKET_TAB + NO_LIVE_EXECUTION_ENABLED + HISTORICAL_FINAL_R_UNCHANGED.** PAPER/read-model/UI only. (1) **Leverage policy 2x→5x safe** (`config/paper_portfolio.yaml`: max_leverage 5, margin ≤25%, notional ≤150%, liq-buffer 3×, skip_if_liquidation_too_close; `position_sizing.py` reduces leverage on wide stops so liq ≥ 3× stop; leverage ≠ risk). (2) **Position lifecycle + partial exits** (`backend/app/lifecycle.py`, `/api/trades/{id}/lifecycle`): TP1 33%/TP2 33%/TP3 34% fills, moved/structural stops, blended R + $ per fill, active-after-TP1; derived LIVE (not batch ledger). (3) **Structural stop after TP** (`src/execution/structural_stop_manager.py`). (4) **Chart fix** (`/chart-events` sources true execution markers from lifecycle): **ETH +3R now shows 3 TP fill markers** at 1636.86/1623.09/1609.32 ($9.51/$27.27/$54.07, blended 2.21R) — no single misleading exit. (5) **Exchange-like trade detail** (`LifecyclePanel`+`ExecChart` price-scaled SVG). (6) **Active partials badge**. (7) **Regime fix** (`backend/app/regime.py`: free-text→enum; unknown only when empty). (8) **MSTR fix**: chase-guard "very late — DO NOT CHASE" no longer leaks onto closed/expired trades (`actionability.py`); MSTR entry was on time, expired flat (MFE 0.36R) — not a miss; + missed-opportunity journal (`/api/missed-opportunities`). (9) **Market dashboard** (`market_dashboard_snapshots` table + `/api/market-dashboard` + redesigned Market tab: fear&greed, risk-now, regime, today/long-term news, extras) written by the **Opus routine final block** (protocol §17, parser `scripts/market_dashboard_from_review.py`, fail-open) **without changing the enriched-review body**. 24 crypto + 70 backend tests pass; frontend build clean (92 modules). No live/auto-live/exchange; production TP/scoring/routing unchanged; `final_r` not rewritten. See `reports/EXECUTION_UI_MARKET_DASHBOARD_FINAL_REPORT.md` (+15 part reports).

> **Structural TP + maker-first + safe 2x (2026-06-24): STRUCTURAL_TP_ACTIVE_FOR_PAPER_ONLY + MAKER_FIRST_EXECUTION_ACTIVE_FOR_PAPER + FEE_AWARE_EXECUTION_ACTIVE_FOR_PAPER + MAX_2X_SAFE_LEVERAGE_POLICY_ACTIVE_FOR_PAPER + PAPER_EXECUTION_USES_STRUCTURAL_TP_AND_MAKER_FIRST + APP_SHOWS_ACTIVE_STRUCTURAL_TP_AND_MAKER_FIRST + NO_LIVE_EXECUTION_ENABLED + HISTORICAL_FINAL_R_UNCHANGED + READY_FOR_FORWARD_VALIDATION.** Implemented (PAPER ONLY, feature-flagged, reversible): (1) **safe leverage max 2x** (`config/paper_portfolio.yaml`: max_leverage 2, max_margin 40%, max_notional 80%, liq_buffer 3.0) — leverage ≠ risk; tight stops cap notional + `risk_capped`, never lever up; (2) **structural TP engine** (`src/analysis/{market_structure_levels,volume_profile}.py` + `src/execution/structural_tp_engine.py`) — swing/range/round/VP levels, TP1 ≥ 0.6R after fees, TP3 only for runners/not chop, ATR fallback labelled, **no fake VP**; (3) **fee-aware execution** (`src/execution/fee_aware_execution.py`) — fee_r_cost + survival labels, skip EXTREME/TIGHT drag; (4) **maker-first** (`src/execution/maker_first_execution.py`) — maker entry for pullbacks, maker TP, **stop always taker**, conservative fills (no free maker); (5) config `config/paper_execution_policy.yaml`. Integrated backfill `scripts/structural_maker_backfill.py` persists the **B book** (`bybit_structural_maker_first`). **Result ($5000, 587 trades, Bybit): A mechanical+taker +3.72%/$1763 fees → B structural+maker-first +8.19%/$1585 fees (Δ +4.47pp, fees −$178, 177 maker entries, 0 fee-drag skips).** MEXC +17.12%→+19.98%; conservative −4.91%→−0.73% (still net-neg on punitive taker account). App: `/api/portfolio/compare` + dashboard A/B card + per-trade `paper_execution_b`; Telegram close alert carries maker-first net + structural label + exact R. Note: **structural swing/VP TP is forward-only** (live candles); historical backfill labels ATR-fallback (no per-trade OHLCV slice) — economic win carried by maker-first+fee-aware+2x. Production TP generation (MECHANICAL_ATR_LADDER) unchanged; no live/auto-live/exchange; `final_r` not rewritten. 44 crypto (targeted) + 6 new backend tests pass; frontend build clean. See `reports/STRUCTURAL_TP_MAKER_FIRST_ACTIVE_PAPER_FINAL_REPORT.md` (+11 part reports).

> **Paper portfolio bugfix (2026-06-24): FEE_MODEL_AUDITED_AND_FIXED + EXPIRED_TRADES_CLOSE_WITH_MARK_PRICE + TP_R_MULTIPLES_DISPLAY_EXACT + LEVERAGE_VISIBLE + CHART_MARKERS_VISIBLE + TP_STRUCTURE_VISIBLE + HISTORICAL_FINAL_R_UNCHANGED + NO_LIVE_EXECUTION_ENABLED.** Operator-reported accounting/display bugs fixed (paper/app only): (1) **close fee now on EXIT notional** (was entry) — Bybit replay +2.94%→**+2.82%**; per-side rates + `config/fee_profiles.yaml` with source/last_verified + `fee_estimated`; (2) **expired trades close at the implied price** from `paper_execution_r` (`exit_price` was NULL on all rows) with `expiry_close_price`+source + an `expired_exit` chart marker; (3) **exact TP R** (e.g. 1.2/2.2/3.2R, not "+1R") in app + Telegram; (4) **leverage/margin/notional/risk visible** (dashboard avg 1.95x/max 5x + per-trade detail + Telegram); (5) `/api/trades/{id}/chart-events` enriched markers (entry/exit/expired/stops/TPs + R + $) + detail timeline (full candle line-overlay = TODO); (6) TP labelled **MECHANICAL_ATR_LADDER**, VP unknown. Ledger rebuilt (4 fee profiles × 587; exit_price 0 NULL). Mid-fix bug: renamed profile orphaned old rows → backend filters one active profile. 43 crypto + 58 backend tests pass; frontend build clean. No production exit/TP-SL/scoring/entry/routing change; `final_r` not rewritten; live locked. See `reports/PAPER_PORTFOLIO_FEES_EXPIRED_TP_CHART_BUGFIX_FINAL_REPORT.md` (+11).

> **Paper portfolio upgrade (2026-06-24): PAPER_PORTFOLIO_LEDGER_READY + POSITION_SIZING_ENGINE_READY + FEE_MODEL_READY_CONFIGURABLE + PAPER_EXECUTION_NOW_HAS_USD_POSITION_ACCOUNTING + APP_SHOWS_USD_PNL_AND_CHART_MARKERS + TP_LEVEL_STRUCTURE_AUDIT_COMPLETE + NO_LIVE_EXECUTION_ENABLED + HISTORICAL_FINAL_R_UNCHANGED.** Added a real paper-trading portfolio (PAPER/ACCOUNTING/APP only): **$5000 deposit, 0.5%/equity risk ($25), stop-based position sizing, dynamic leverage** (min for margin cap ≤20%, ≤5x, liquidation-buffer-aware — *leverage ≠ risk*), **configurable fee/slippage profiles** (`config/fee_profiles.yaml`: bybit/mexc/conservative/zero). New modules `src/execution/{position_sizing,fees,paper_portfolio,tp_structure_validator}.py`; table `paper_portfolio_ledger`; backfill `scripts/paper_portfolio_backfill.py` → equity-curve + ledger CSVs. **TP audit:** production TPs are a MECHANICAL ATR ladder (`close ± 1/2/3·ATR`); stops semi-structural; volume-profile unknown → added a display-only `tp_structure_validator`. **Backfill result ($5000, 586 trades):** no-cost **+47.6%**, Bybit **+2.94%**, MEXC +16.3%, conservative **−5.65%** → Model F edge real but **fee-fragile**. App: portfolio cards + `/api/portfolio` + `/api/trades/{id}/chart-events`; Telegram close alert carries Paper $ (risk/leverage/fees/net). No live/exec; no production exit/TP-SL/scoring/entry/routing change; `final_r` never rewritten. 88 crypto + 57 backend tests pass; frontend build clean. See `reports/PAPER_PORTFOLIO_RISK_AND_CHART_MARKERS_FINAL_REPORT.md` (+13 part reports).

> **Shadow→paper promotion audit (2026-06-24): SHADOW_FEATURE_INVENTORY_COMPLETE + SHADOW_PROMOTION_DECISIONS_READY + APPROVED_PAPER_FEATURES_IMPLEMENTED + BAD_SHADOW_FEATURES_ARCHIVED_OR_LEFT_OFF + PAPER_FEATURES_VISIBLE_IN_APP_AND_TELEGRAM + NO_LIVE_EXECUTION_ENABLED + NO_PRODUCTION_TRADE_LOGIC_CHANGE.** Inventoried ~22 shadow/default-off/advisory features (source of truth `docs/SHADOW_MODE_REGISTRY.md` + new `config/paper_features.yaml`). **Promoted to paper (display/accounting/advisory only):** Model F/`paper_execution_r` (already active), touch-relabel, status clarity, risk-guard warnings, catalyst labels — plus NEW: cohort-guard `warn` (weak `crypto_intraday_catalyst_or_momentum` label, NO routing change) + a Control Plane **Paper Features panel** (`GET /api/paper-features`) + per-trade feature tags (`model_f`, `be_protected`, `cohort_warn`…). **Archived:** `src/exits/shadow_exit_manager.py` variants A–I (SUPERSEDED_BY_MODEL_F; kept for research, not wired). **Kept shadow/measuring:** circuit-breaker block, sector/concentration-cap block, position advisor, intelligence layer, adaptive TP3. **Dangerous/locked (unchanged):** crypto scalp / stocks C-tier / stocks swing-invest actionable. Every active paper feature is `affects_trades:false`; live/auto-live still locked; `final_r` never rewritten. 78 crypto + 55 backend tests pass; frontend build clean. See `reports/FULL_SHADOW_TO_PAPER_PROMOTION_FINAL_REPORT.md` (+11 part reports). **Plain-English current state (implemented / testing / waiting / archived / locked): [`docs/CURRENT_TESTING_AND_WAITING_STATE.md`](docs/CURRENT_TESTING_AND_WAITING_STATE.md).**

> **Active paper-risk upgrade (2026-06-24): PAPER_EXECUTION_ACCOUNTING_DEFINED + MODEL_F_ACTIVE_FOR_PAPER_ACCOUNTING + APP_USES_PAPER_EXECUTION_R + TOUCH_R_LABELLED_AS_OPTIMISTIC + HISTORICAL_FINAL_R_UNCHANGED + NO_LIVE_EXECUTION_ENABLED + NO_PRODUCTION_TRADE_LOGIC_CHANGE.** Legacy `signal_outcomes.final_r` is **touch-based** (highest TP touched) and overstated PnL (actionable touch +6.2R vs −104.8R with no risk management). New **authoritative paper PnL = `paper_execution_r`** via Model F `early_mfe_protection_v1` (stop→BE @ +0.6R favorable excursion, lock +0.5R @ +1R, runner to TP3) — recovers the actionable replay to **+74.1R**. PAPER/ACCOUNTING ONLY: new module `src/execution/paper_execution_accounting.py`, additive table **`paper_execution_outcomes`** (never touches `signal_outcomes`), fail-open tracker hook, scheduler non-fatal step + CLI `paper-execution-refresh` (backfill 1607 rows, errors=0), close-alert paper-exec line, recalc CSV `data/research/paper_execution_recalc_2026-06-23.csv`. Control Plane `books.py`/`desk_adapter`/frontend now lead with **Paper Execution R**; **Touch R** secondary "optimistic/signal-quality"; protection stats + missing-MFE fallback warning (never silently zeroed). `final_r` **never rewritten**; live/auto-live still locked (`/api/health` live_locked:true). Forward paper validation pending. 74 crypto + 53 backend tests pass; frontend build clean. See `reports/PAPER_RISK_MANAGEMENT_UPGRADE_FINAL_REPORT.md` (+10 part reports).

> **App "Today R" correction + canonical books (2026-06-20): APP_TODAY_R_FIXED + CANONICAL_BOOKS_DEFINED + NO_TRADE_LOGIC_CHANGE.** The Mini App showed ~**−26R** because the frontend summed raw `final_r` over the last 200 signals (no day boundary → 5 days; no economic dedup; shadow + scalp + C-tier mixed in; expired confused with flat). Root cause: [frontend/src/screens.tsx](../trading-desk-control/frontend/src/screens.tsx) `todayR` reduce + the adapter returning all signals with no book separation. Decomposition: −26R = **Paper d7 (−22R) + Shadow d7 (−4R)**. **Fix (read-model / UI only):** new canonical books module `trading-desk-control/backend/app/books.py` (`economic_trade_key`, `derive_trade_book`, `collapse_economic_trades`, latest/terminal outcome, `get_dashboard_summary`, `get_closed_trades`, `near_winner_expired`) + endpoints `/api/dashboard/summary`, `/api/closed/{book}`, `/api/near-winners`; adapter now surfaces delivery status + catalyst labels + regime; frontend dashboard + Closed-trades tab rebuilt (Operator/Paper/Shadow separation, economic dedup with `duplicates_collapsed_count`, honest close reasons, delivery badges, catalyst tri-state incl. "unknown/stale", regime-or-unknown, near-winner-expired diagnostic panel). **Correct numbers:** Operator Book **today +2.0R**, **48h −1.0R (W4/L9)**; Paper 48h −3R; Shadow 48h −1R (25 expired). Headline now: "Today R = Operator Book, deduped, terminal realized only, shadow excluded (UTC day)." Also: catalyst-label-refresh baseline verified live; one safe Telegram ReadTimeout retry added in `src/notifiers/telegram.py` (delivery only, idempotent at the alert-row layer). **No scoring/TP-SL/entry/routing/filters/validity/live changed; historical outcomes not rewritten.** See `reports/POST_DATA_INTEGRITY_APP_FIX_FINAL_REPORT.md`.

> **Telegram Mini App root-cause fix (2026-06-20): TELEGRAM_APP_FIXED + CONTROL_PLANE_OK + NO_TRADE_LOGIC_CHANGE.** "Приложение в Telegram не работает" recurred because the **Control Plane app stack (FastAPI backend :8000 + cloudflared tunnel + bot) was not persistent** and got reaped at the previous session's end (the trading core survived only because it is a Windows task). At audit start: backend/bot/cloudflared = 0, port 8000 closed, `.env` `MINI_APP_URL` was a stale dead tunnel; trading scheduler healthy (uptime ~23.5h, `problems:[]`). **Fix (operational only):** new self-healing keeper `trading-desk-control/scripts/app_keeper.ps1`/`.bat` (60s health loop → idempotent `launch_robust.ps1` on any component down) registered as Windows task **`CryptoAIDeskApp`** (`-Once`+`StartWhenAvailable`, RestartCount=3, IgnoreNew) → the app stack is now **task-owned, surviving session-end + reboot**, mirroring the trading monitor. Post-fix: backend `/api/health` 200 (local+tunnel, `live_locked:true`), single bot `@aitradingdesk1_bot`, menu button re-pointed to the live tunnel, test "Open Control Plane" button delivered (msg_id=8), 118 tests pass, tsc exit 0. New tunnel `https://domains-exemption-affiliated-cancelled.trycloudflare.com` (quick-tunnel URL still rotates per launch; keeper auto-updates `.env`+menu button — use the **menu button**, which is always current). **No scoring/TP-SL/entry/routing/filters/live changed.** See `reports/FULL_SYSTEM_AND_TELEGRAM_APP_FINAL_AUDIT.md` + `reports/TELEGRAM_APP_ROOT_CAUSE_REPORT.md`.

> **6h sanity check (2026-06-18 15:13 UTC): MONITORING_6H_MINOR_ISSUES.** All layers wired/healthy, enrichment p95 78ms, no network in alert path, ASTER cleared, all locks intact. Two operational nuances (not code/trade-math): the scheduler loop is **not currently running** (ran 2 clean cycles ok=19/0 then the session-launched loop ended) and live alerts won't show intel fields until monitors restart with the new code. **Action: restart the scheduler via the permanent autostart.** See `reports/MONITORING_6H_SHADOW_SANITY_CHECK.md`.

> **Monitor persistence fix (2026-06-18 15:39 UTC): MONITOR_PERSISTENCE_READY + MONITOR_HEARTBEAT_READY + FORWARD_TEST_RESUMED.** Root cause of the stop = the running loop was *session-launched* and reaped on session end (not a crash); the permanent task had been dormant since 6/15 with no restart-on-failure. Fix: new **`CryptoAIDeskMonitor`** scheduled task (service-owned, `-Once`+`StartWhenAvailable` reboot recovery, RestartCount=3, MultipleInstances=IgnoreNew, `-Foreground`) + dup-guarded launcher `scripts/start_monitor_scheduler.ps1`/`.bat` + watchdog `scripts/monitor_heartbeat.py`/`.bat` (Telegram start/cycle/warn, 60-min cooldown, auto-restart) registered as **`CryptoAIDeskHeartbeat`** (every 20 min). Old dormant `CryptoAIDesk_Scheduler` **disabled** (no dup-guard). Scheduler **PID-running, CYCLE 1/12 in progress, `last_outcome` refreshed 15:39 UTC**; duplicate-lock + 86 focused tests pass. **No trade-math/scoring/TP-SL/routing/live changed.** Residual: tasks are interactive → a full *log-off* pauses them (optional elevated AtLogon command in the fix report). The ~3.1h gap (12:29→15:39 UTC) means the 2-day forward test clock **restarts 15:39 UTC**. See `reports/MONITOR_PERSISTENCE_DIAGNOSTIC.md`, `reports/MONITOR_PERSISTENCE_FIX_REPORT.md`, `reports/POST_MONITOR_RESTART_VERIFICATION.md`.

## Latest Intraday Notes — 2026-06-18

> Read-only diagnostic over the live DB. **No trade logic / scoring / TP-SL / routing / filters changed.** Saved so tomorrow's and Friday's analysis have context. Full detail: `reports/DAILY_EXPIRED_LOSS_REVIEW_2026-06-18.md`.

**Monitor / data caveat (interpret today's numbers with care):**
- The scheduler had a **gap**: it ran 2 clean cycles then the (session-launched) process stopped; later it was restarted under the new persistence task (`CryptoAIDeskMonitor`).
- So **part of the day may have had stale caches / no fresh cycles** (no cycles 12:29→15:39 UTC). 
- **The forward-test counts as valid only after the stable persistent monitor** (clock effectively restarts ~15:39 UTC).

**Expired family today = 21** (`expired` 11, `stale_before_entry` 8, `entry_moved_away` 2):
- **Most are old-tail** signals created 06-11…06-17 whose validity window simply elapsed — **only 4 were created today**. Do not read this as a fresh-failure spike.
- **Only one clear missed winner: `ZRO/USDT` long, MFE ≈ +3.28R after expiry.** Everything else was noisy/partial (would likely have stopped first).

**Stocks scanner is NOT broken:**
- Today stocks signals = **22** (B-tier = 6, all triggered/open; C-tier = 16, mostly shadow/review-only).
- "Нет stocks в actionable" ≠ "stocks scanner не работает" — it's visibility/actionability (C-tier is shadow), not a scanner/data failure.

**The thin side today is crypto:**
- Only **3 crypto signals created today**; **70 crypto rejected ideas**.
- Main rejection reasons: **no-chase (26)** ("price >2 ATR from EMA20") / **mixed regime (18)** / **short-squeeze-risk cap to C (24)** / derivatives unavailable (1) / counter-trend (1). Expected filter behavior on a stretched/mixed tape.

**Losses today:**
- **Actionable paper-book crypto non-scalp B = 7 losses / −7R**, all **longs**, mostly **pullback-long** playbook.
- Symbols: BCH, ZEC, SUI, GPS, HOME (intraday); BANK, ALLO (swing). (HOME = breakout; rest = pullback.)
- Shadow losses (NOT in paper book): MITO/USDT scalp + all C-tier stocks.
- **Hypothesis (for Friday, not a change):** pullback-long playbook may underperform in weak/mixed/stretched tape, especially when universe rejects are dominated by no-chase / mixed-regime / squeeze-cap.

**Intelligence labels:**
- Intel fields are **missing on today's closed losses** because those alerts were emitted **before the intelligence block was loaded** (stale in-memory module). Forward alerts (post-restart) should include them; evaluate intel labels only on post-restart alerts.

**Current decision:** `NO_TRADE_LOGIC_CHANGE_TODAY` — saved as Friday-review hypothesis only. See also the Friday Review Checklist in `docs/WEEKLY_FORWARD_METRICS.md`.

> **Status display semantics clarified (2026-06-19):** Telegram/Control Plane/reports now distinguish lifecycle states instead of one word. `expired` is split into **entered-unresolved** (`entry_triggered=1`, no TP/SL before window) vs **no-entry/stale/moved-away** (`entry_triggered=0`); `+0R` is now **lifecycle-aware** (unresolved-expiry ≠ flat ≠ N/A); "no active trades" only means no OPEN actionable (waiting/review/entered-unresolved are shown separately). Canonical module `src/status/display_status.py` (+ Control-Plane mirror `backend/app/display_status.py`); honest summary via `scripts/paper_monitor_status.py`. **No trade logic / scoring / TP-SL / routing / outcomes changed.** See `reports/STATUS_SEMANTICS_CLARITY_REPORT.md`, `reports/POST_STATUS_CLARITY_FIX_REPORT.md`.

> **Status display LIVE-Telegram ready + monitor restarted (2026-06-19 15:37 UTC):** Fixed the `✅ CLOSED WIN +-1.0R` sign bug (sign-aware classification + `:+.1f`); reduced `UNKNOWN_INCONSISTENT` **87→3** via a latest-outcome-row read model (the 84 were a `MAX()` aggregation artifact, the 3 are genuine `ambiguous` rows, none rewritten). `scripts/paper_monitor_status.py` is now `--compact`/cooldown Telegram-ready and wired as a **non-fatal** scheduler step after `track-signals (post)`. Monitor cleanly **restarted** under `CryptoAIDeskMonitor` (PID 17040), heartbeat `problems: []`, Telegram online. **No trade logic change.** See `reports/POST_STATUS_LIVE_POLISH_AND_MONITOR_RESTART_REPORT.md`, `reports/R_DISPLAY_SIGN_FIX_REPORT.md`, `reports/UNKNOWN_INCONSISTENT_PROVENANCE_REPORT.md`, `reports/MONITOR_RESTART_AND_HEARTBEAT_VERIFICATION.md`.

> **Full shadow-modes promotion audit + health check (2026-06-19): SAFE_PROMOTIONS_ONLY · NO_LIVE_EXECUTION_ENABLED.** System healthy (1 scheduler, heartbeat `problems:[]`, Control Plane up, 114+38 tests pass). Evaluation window since the stable monitor restart is ~26.5h with only **5 closed actionable paper decisions (1W/4L, −3R)** → far below promotion gates. **No trade-affecting shadow feature promoted** (intelligence gates, circuit-breaker block, sector/concentration caps, profit protection/exits, real sizing all → NEED_MORE_DATA / KEEP_SHADOW). Display/advisory features (status taxonomy, lifecycle R, paper-monitor Telegram, catalyst context, Agent Council reason_codes) are the only PROMOTE_NOW set and were **already live**. New: `docs/SHADOW_MODE_REGISTRY.md`. **No production trade math / scoring / TP-SL / routing / live change.** See `reports/FULL_SHADOW_PROMOTION_FINAL_REPORT.md`.

> **Routine Opus/Sonnet reviews now use the Agent Council structured prompt (2026-06-19).** Each scheduled enriched-review run (`opus-enriched-review-4h` + siblings preus/postclose) is ONE LLM run that reasons through nine virtual roles (data_quality, market_regime, catalyst_narrative, derivatives_squeeze, technical_entry, execution_lifecycle, risk_manager, playbook_performance, head_trader) and emits a mandatory advisory-only Agent Council JSON block + table, lifecycle-aware status language, and a Status-block Telegram summary. **No new agents/processes/LLM calls, no permission-contract weakening, no trade logic change.** Files: `~/.claude/scheduled-tasks/opus-enriched-review-4h/SKILL.md`, `prompts/llm_review/enriched_market_review_protocol.md` §17, manual `.claude/skills/enriched-review/SKILL.md`, Obsidian system prompt. Validator: `scripts/validate_agent_council_prompt.py`. See `reports/POST_AGENT_COUNCIL_ROUTINE_PROMPT_REWRITE_REPORT.md`.

> **Final status/Telegram/app E2E verification (2026-06-19): READY_FOR_FORWARD_MONITORING.** Monitor running on new code (PID 17040, single instance, heartbeat `problems:[]`); paper-monitor Telegram summary verified sent (no `+-`, expired split, human-readable buckets). **Close alerts** now lifecycle-aware (`close_alert.py`): expired-after-entry → "0R — unresolved", genuine flat → "CLOSED FLAT 0R", win/-R contradiction flagged — **dedup is by (signal_id, alert_type), not text, so no resend**. Source grep: no old status language in live output. Intelligence/catalyst healthy post-restart (catalyst `ok`, no ASTER regression). **165 tests pass; no trade logic change.** See `reports/FINAL_STATUS_TELEGRAM_APP_E2E_VERIFICATION.md`.

## Current Status
- **System is NOT live-ready.**
- Operational guardrails deployed (alert-only / shadow-only / read-only).
- Fast safe acceleration completed (C-tier policy, OHLCV backfill, shadow exits).
- **Latest full test result: 766 passed, 0 failed.**
- No production trade-math change.
- Profit protection disabled.
- Micro-live not approved.

## Current Verdicts
- FAST_SAFE_ACCELERATION_COMPLETE
- STOCKS_C_TIER_SHADOW_APPLIED
- OHLCV_BACKFILL_READY
- SHADOW_EXIT_MANAGER_READY
- SYSTEM_STABLE
- PROFIT_PROTECTION_STILL_DISABLED
- NO_PRODUCTION_TRADE_MATH_CHANGE
- MICRO_LIVE_NOT_YET
- MICRO_LIVE_CANARY_REVIEW_IN_7_10_DAYS

## What Is Operational (alert-only / read-only — no trade behavior)
- circuit breaker alert-only (`src/risk/circuit_breaker.py`)
- catalyst integrity scan (`scripts/catalyst_integrity_scan.py`, scheduler step)
- OHLCV archive / historical backfill (`scripts/archive_ohlcv_history.py`, `scripts/backfill_ohlcv_history.py`)
- open intraday lifecycle review (`scripts/open_intraday_lifecycle_review.py`)
- sector-cap would-bind tracker (`scripts/sector_cap_forward_tracker.py`)
- position/leverage advisor label-only (`src/risk/position_advisor.py`)
- Telegram / Control Plane risk fields (`src/risk/risk_guards.py`, `backend/app/desk_adapter.py`)

## What Is Shadow-Only (measurement, never affects trades)
- shadow exit manager (`src/exits/shadow_exit_manager.py`)
- BE after +0.5R / BE after +1R / partial TP1 / trailing stop
- sector-cap would-bind
- risk-off throttle
- profit-protection variants
- **Shadow Intelligence Layer (`src/intelligence/`)** — symbol timeline memory,
  derivatives trajectory, squeeze phase classifier, thesis/invalidation formatter,
  on-chain risk (interface; config missing). Cached + read-only in alert path
  (p95 63ms); background compute via `scripts/intelligence_update.py`.

## Locked Rules (do NOT change without explicit operator approval)
- live / auto-live / exchange execution
- crypto scalp actionable
- stocks scalp production
- TP/SL
- scoring
- thresholds
- sector cap value
- BE / partial / trailing in real trade logic
- hard circuit breaker
- hard risk-off throttle
- hard sector-cap block
- leverage execution
- force-close logic
- historical outcomes
- Control Plane commands / locks / safety

## Current Key Findings
- C-tier stocks intraday was **already** non-actionable (`decide_paper_entry` blocks all C-tier); the explicit policy (`config/signal_tracking.yaml` → `tier_policy.stocks_intraday_c_tier`) now documents/labels it. The 30d −34R C-tier figure was a tracking artifact, not live exposure.
- OHLCV backfill achieved **100% path-aware replay coverage** on the recent 146 crypto intraday/swing closed trades (60d 5m/15m, 70 symbols, 0% gaps).
- Shadow exit manager works, but **shadow A_current (−39R) is pessimistic vs the actual recorded book (+6R)** for the same 146 trades — artifact of 5m + conservative stop-first same-candle. Only RELATIVE variant deltas are trustworthy.
- Profit protection remains **disabled**. BE-after-0.5R / partial-TP1 / BE-after-1R are **shadow candidates only**; the tested 30d window was net-losing so none is profitable, only less-bleeding.
- ASTER catalyst flag must clear after the next fresh catalyst scan; if it persists post-scan, that's a real regression.
- Manual micro-live is **not approved**; only a canary review after 7–10 days of forward data.

## Near-Term Goal: Next 7–10 Days
Answer:
- Are operational guardrails stable?
- Does catalyst integrity clear ASTER after a fresh scan?
- Are Telegram / Control Plane stable?
- Does the circuit breaker produce useful would-pause signals?
- Do lifecycle reviews catch real stale/carryover issues?
- Do shadow exits behave consistently forward?
- Can we even consider a manual micro-live canary review?

## 30-Day / Longer Goal
Answer:
- Is profit protection useful across up/down regimes?
- Can partial TP1 or BE-after-1R become a paper-rule candidate?
- Can a risk-off throttle be justified?
- Can we safely move paper → manual micro-live → small controlled live?

## Manual Micro-Live Gate
Manual micro-live may be **reviewed** only if ALL hold:
- tests green
- scheduler stable
- Telegram clean
- Control Plane safe
- catalyst ASTER flag cleared
- circuit breaker dry-run reasonable
- no scalp
- no C-tier
- no live automation
- strict manual-only execution
- risk per trade tiny
- operator manually confirms every trade

## Current Next Actions
1. Let the scheduler run 7–10 days.
2. Confirm the ASTER flag clears after a fresh catalyst scan. (✅ cleared on 06-18 fresh scan)
3. Investigate the 5m-shadow vs actual-tracker timeframe discrepancy.
4. Re-run the shadow exit ledger weekly.
5. Review manual micro-live canary readiness only after forward data.
6. **Friday: shadow-intelligence forward comparison** (`reports/SHADOW_INTELLIGENCE_FORWARD_COMPARISON_TEMPLATE.md` + `docs/SHADOW_INTELLIGENCE_FORWARD_METRICS.md`) — does squeeze_phase / no_chase / thesis-invalidation predict outcomes? Default keep_shadow.

## Important Reports
- `reports/POST_FAST_SAFE_ACCELERATION_FINAL_DECISION.md` — latest stage decision (15 Qs).
- `reports/POST_BACKFILL_PROFIT_PROTECTION_REPLAY.md` — 100%-coverage exit replay + caveats.
- `reports/SHADOW_EXIT_LEDGER_SUMMARY.md` — variant net R / PF / clipped / saved.
- `reports/OHLCV_HISTORICAL_BACKFILL_COVERAGE_REPORT.md` — data depth.
- `reports/POST_OPERATIONAL_GUARDRAILS_DEPLOY_FINAL_DECISION.md` — operational deploy.
- `reports/POST_PROFITABILITY_GUARDRAILS_FINAL_DECISION.md` — guardrail design.
- `reports/STOCKS_INTRADAY_SAFE_RESTRICTION_PLAN.md` — C-tier rationale.
- `reports/FAST_ACCELERATION_STABILITY_CHECK.md` — stability sanity.

## Safe observability + DB hygiene pass (2026-06-26)

Observability + hygiene only — **no scoring / actionability / threshold / final_r change; live + auto-live locked; paper-shadow B not promoted; forward A/B monitoring continues** (gate NOT_READY).

- **Per-mode A/B breakdown active** — `/api/paper-shadow/breakdown` + Mini App "By mode" section (forward-emphasized; backfill labelled look-ahead).
- **Daily Telegram A/B digest active** — `config/paper_shadow_digest.yaml` + `paper-shadow-digest-send` CLI + scheduler step (idempotent once-daily).
- **DB retention policy added (ready, not yet run on live)** — `signal-outcomes-retention` (per-bar archive→delete; latest-row-per-signal + final outcomes + recent N days always kept; dry-run default). Baseline ≈1994 MB / 371k rows / 151.8 per signal.
- **Catalyst linkage = diagnostic only** — `catalyst-linkage-shadow-audit` (shadow table; coverage 26.3%→48h 55.1%; **not fed to scoring**).
- **A-tier = diagnostic only** — correctly rare ~3.78%/30d (caps gate it, not the bar); **threshold unchanged**.
- **Stocks scalp/swing/invest remain non-actionable** unless separately approved — `stocks_mode_readiness` (swing best paper-shadow candidate; scalp/invest research-only).
- See `trading-desk-control/reports/SAFE_OBSERVABILITY_DB_HYGIENE_FINAL_REPORT.md`.
