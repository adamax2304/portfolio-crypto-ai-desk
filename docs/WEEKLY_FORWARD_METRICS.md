# Weekly Forward Metrics

Fill one column per weekly review (start ~7–10 days after 2026-06-18). Feeds the micro-live canary decision.
All metrics are observation-only; recording them changes no trading behavior.

> Plain-English current state (what's implemented / testing / waiting / archived / locked): [`CURRENT_TESTING_AND_WAITING_STATE.md`](CURRENT_TESTING_AND_WAITING_STATE.md). The §"Paper feature promotion" + "Paper execution accounting" blocks below are the active forward-validation checklist.

| Metric | Week of ____ | Week of ____ | Week of ____ |
|---|---|---|---|
| max leverage used (≤5x policy) / risk-capped / liq-buffer-reduced count | | | |
| partial-exit blended R vs touch R (avg gap) | | | |
| regime "unknown" rate (target ↓; empty-only) | | | |
| missed-opportunity count (entry never triggered) / would-have-been-profitable | | | |
| market dashboard freshness (Opus block present / stale >4-6h) | | | |
| **B paper equity (structural+maker-first, Bybit)** vs replay baseline $5409 / +8.19% | | | |
| **A paper equity (mechanical+taker, Bybit)** vs replay baseline $5186 / +3.72% | | | |
| fees as % of gross (watch ~74%) | | | |
| maker fill rate (forward vs conservative-model 100%) | | | |
| missed maker entries (forward; backfill assumed 0) | | | |
| fee-drag skips (backfill: 2 conservative / 0 Bybit) | | | |
| structural TP usage (forward, full swing/VP) | | | |
| dates covered | | | |
| full test status (passed/failed) | | | |
| scheduler status (clean / errors) | | | |
| Telegram status (clean / issues) | | | |
| Control Plane status (safe / issues) | | | |
| catalyst integrity status (ok / warning) | | | |
| ASTER flag cleared? (yes/no) | | | |
| circuit breaker would_pause count | | | |
| est. R saved by circuit breaker | | | |
| open intraday lifecycle review count | | | |
| stale / carryover count | | | |
| shadow exit coverage % | | | |
| BE-after-1R forward delta (R) | | | |
| partial-TP1 forward delta (R) | | | |
| winners clipped | | | |
| losers saved | | | |
| stocks intraday A/B performance (R) | | | |
| C-tier blocked / shadow count | | | |
| scalp status (must stay shadow/off) | | | |
| risk-off label usefulness (notes) | | | |
| canary review verdict | | | |

## How to populate
- Tests: `python -m pytest tests/ -q`
- Circuit breaker: `python -m scripts.circuit_breaker_dry_run` → `reports/OPERATIONAL_CIRCUIT_BREAKER_DRY_RUN.md`
- Lifecycle: `python -m scripts.open_intraday_lifecycle_review` → `reports/OPEN_INTRADAY_LIFECYCLE_REVIEW.md`
- Shadow exits: `python -m scripts.shadow_exit_ledger_update && python -m scripts.shadow_exit_summary` → `reports/SHADOW_EXIT_LEDGER_SUMMARY.md`
- Sector cap: `python -m scripts.sector_cap_forward_tracker` → `reports/SECTOR_CAP_WOULD_BIND_FORWARD_TRACKER.md`
- Catalyst: `python -m scripts.catalyst_integrity_scan` → `reports/CATALYST_INTEGRITY_DAILY_SUMMARY.md`
- Stocks intraday: `python -m scripts.stocks_intraday_diagnostic` → `reports/STOCKS_INTRADAY_REWORK_DIAGNOSTIC.md`

> Canary review verdict must remain **MICRO_LIVE_NOT_YET** unless every Manual Micro-Live Gate item in `../PROJECT_STATE.md` is satisfied AND the operator explicitly approves.

## Friday Review Checklist (added 2026-06-18 from daily diagnostic)

Observation-only. Source context: `../reports/DAILY_EXPIRED_LOSS_REVIEW_2026-06-18.md`. Work through each before proposing any rule change:

- [ ] **Expired old-tail vs fresh expired** — split today's/this-week's expired into old-tail (created on earlier days, window simply elapsed) vs genuinely fresh expired; only fresh expired indicates a today-failure.
- [ ] **Missed-winner count** — how many expired/stale signals had MFE ≥ ~1R in-direction after expiry (genuine missed opportunities).
- [ ] **ZRO/USDT follow-up** — track the 2026-06-18 ZRO long (MFE ≈ +3.28R after expiry); single case, do NOT loosen rules from it alone.
- [ ] **Crypto rejection distribution** — share of no-chase / mixed-regime / squeeze-risk-cap / insufficient-data; is the funnel thin for healthy (filter) or unhealthy (data/scanner) reasons?
- [ ] **Pullback-long losses in weak/mixed tape** — did pullback-long playbook concentrate the losses again? Quantify R by playbook × regime.
- [ ] **Stocks B-tier open outcomes** — resolve the 6 B-tier stocks open from 06-18; judge stocks by B-tier outcomes, not raw count.
- [ ] **Intelligence fields availability after restart** — confirm post-restart alerts carry intel labels; only then compare labels vs outcomes.
- [ ] **Circuit breaker state during losses** — was `would_pause` ever true around the loss windows? Est. R it would have saved.
- [ ] **Shadow exit result for loss trades** — re-run shadow exit ledger; did any BE/partial/trailing variant reduce the −R on the pullback-long losers?
- [ ] **Would any new rule have saved R without killing winners** — counterfactually check that a candidate rule (e.g. pullback-long confidence cut in mixed tape) nets positive vs the winners it would also suppress.
- [ ] **Separate entered-unresolved expired from no-entry expired** — when reviewing "expired", split by `entry_triggered` (use `scripts/backfill_display_status.py` / `scripts/paper_monitor_status.py`): entered-unresolved (`ENTERED_UNRESOLVED_EXPIRED`) = a trade was filled but no TP/SL before the window; no-entry (`NO_ENTRY_EXPIRED`) = never touched. Never treat them as one bucket; track `expired_after_entry_count` vs `no_entry_expired_count` and review `unknown_inconsistent_count`.
- [ ] **R display sign consistency** — confirm no `+-` / win-with-negative-R / loss-with-positive-R in Telegram or reports (sign-aware classification in `src/status/display_status.py`).
- [ ] **UNKNOWN_INCONSISTENT provenance** — should stay ~3 (genuine `ambiguous` rows); if it climbs, check for a forward writer regression (no-entry status + `entry_triggered=1`) — currently a read-model artifact only, fixed via latest-outcome-row.
- [ ] **Operator clarity in Telegram** — the per-cycle Paper Monitor Status reads cleanly: open/waiting/entered-unresolved/review-shadow/no-entry + expired split + needs-review; no bare "no active trades" / "+0R".
- [ ] **Monitor uptime** — `CryptoAIDeskMonitor` State=Running, single instance, heartbeat `problems:[]`, cycles every ~2h (`data/autostart/scheduler.log`).
- [ ] **Telegram app / Control Plane uptime** (added 2026-06-20) — `CryptoAIDeskApp` task State=Running; backend `http://127.0.0.1:8000/api/health` → 200 (`live_locked:true`); single bot/cloudflared instance; current tunnel URL in `trading-desk-control/.env` `MINI_APP_URL` opens (200) and the bot **menu button** points at that same URL. If the app "не открывается": it self-heals within ~60s (keeper), else re-run `trading-desk-control/scripts/launch_robust.ps1`. Note the quick-tunnel URL rotates per restart → always open via the **menu button**, not an old inline button.
- [ ] **Operator vs Paper vs Shadow reconciliation** (added 2026-06-20) — read `/api/dashboard/summary`. The headline **Today R = Operator Book** (deduped, terminal-realized, shadow excluded). Confirm Operator ≤ Paper (delivery gap = difference) and Shadow is reported separately and NOT in the headline. If app R looks wildly negative again, it's a read-model regression — check `backend/app/books.py` dedup + book filters, NOT trade logic. (History: a raw sum-over-200-signals once showed −26R = Paper d7 −22 + Shadow d7 −4.)
- [ ] **Catalyst label freshness** (added 2026-06-20) — `signal_catalyst_labels.computed_at` should be < a few hours (refreshed each cycle by `catalyst-label-refresh`). If stale, the app shows catalyst "unknown/stale" (honest) — investigate the refresh step, do NOT mark trades "no catalyst".
- [ ] **market_regime coverage** (added 2026-06-20) — share of entered signals with a non-blank `market_regime`. Still sparse (~30%); the app shows "unknown" when missing. Persisting regime at signal creation is a TODO (data-only).
- [ ] **Telegram delivery errors** (added 2026-06-20) — `signal_alerts.telegram_status` counts of `error:*` / `late_shadow` in the window; the app surfaces a delivery-gap badge. One safe ReadTimeout retry now exists; recurring errors mean a real connectivity issue.
- [ ] **Near-winner expired panel** (added 2026-06-20) — `/api/near-winners` (expired-after-entry with MFE ≥ 0.8R). Diagnostic only (does not change exits); track whether a specific mode/playbook keeps leaving R on the table at expiry.
- [ ] **First full paper-monitor Telegram cycle** — confirm the in-cycle `paper monitor status (telegram)` step fired at least once after `track-signals (post)` (grep `data/autostart/scheduler.log`) and respected the 90-min cooldown (no double-send).
- [ ] **Needs Review stays low** — `unknown_inconsistent_count` should remain ~3 (genuine `ambiguous`); a climb signals a forward writer regression.
- [ ] **Operator clarity** — Telegram/app read cleanly (no `+-`, no raw `expired`, no bare `+0R`); close alerts show lifecycle-aware R.
- [ ] **No-entry vs entered-unresolved** — review these two expired sub-buckets separately, never as one "expired".
- [ ] **Agent Council reason_codes vs outcomes** — for the latest enriched reviews, did the council `reason_codes` line up with what actually happened (e.g. `chase_risk`/`overextended` preceding stopped longs; `squeeze_risk` preceding short squeezes)?
- [ ] **Risk Manager agent predictiveness** — did `risk_manager` warnings (`daily_loss_pressure`, `repeated_losses`, `correlation_cluster`, `legal_risk`) precede actual losers?
- [ ] **Execution/Lifecycle agent clarity** — did the `execution_lifecycle` agent + Status block reduce confusion vs the old raw `expired`/`+0R` wording?
- [ ] **Head Trader candidate usefulness** — were the best long-watch / short-watch / catalyst-watch candidates (and their triggers) actually useful / would-have-worked? Did avoiding "NO TRADE" overuse help or hurt?
- [ ] **Shadow-mode re-evaluation (per `docs/SHADOW_MODE_REGISTRY.md`)** — once the closed-actionable-decision count reaches **≥15 (paper gate) / ≥30 (production gate)**, re-run the shadow-promotion dataset (`data/research/shadow_promotion_dataset_*.csv`) and re-evaluate: squeeze-phase / no-chase predictiveness, circuit-breaker `would_pause` fires (need ≥10), sector/concentration cap binds, playbook-by-bucket R. Promote only what clears the gates with a proof report; keep everything else shadow.

### Paper execution accounting (Model F) — added 2026-06-24
> Authoritative paper PnL is now `paper_execution_r` (Model F: BE @ +0.6R, lock +0.5R @ +1R, runner TP3). Touch-based `final_r` is kept only as an optimistic signal-quality metric; `final_r` is NEVER rewritten; live/exec stay locked.
- [ ] **Paper Execution R (Operator book), FORWARD only** — does `paper_execution_r` stay net-positive on trades entered *after* 2026-06-24? The replay's +74.1R is hindsight / 30d single-epoch, NOT yet forward-validated. Track today / 48h / 7d from the dashboard headline.
- [ ] **Paper vs Touch divergence** — `touch_minus_paper_r` + `giveback_n` per window: confirms early protection is actually firing (BE-scratch + lock events).
- [ ] **Protected / stops-avoided** — `protected_n`, `original_stops_avoided_n`: how often protection turns a would-be −1R into 0R/+0.5R.
- [ ] **`paper_unavailable_n` stays 0** — any entered+resolved trade missing MFE → paper R unavailable (warning, never silently zeroed); a climb = tracker/MFE regression.
- [ ] **Cost/slippage haircut (pre-paper-flag gate)** — Model F is BE-heavy (~42% scratch); apply a fee/spread haircut before trusting absolute R.
- [ ] **`crypto_intraday_catalyst_or_momentum` cohort** — weakest actionable (chase-longs); `config/cohort_guard.yaml` now **`warn`** (dashboard label only, no routing). Watch forward paper R; escalate to `paper_review_only` (paper routing) only with sign-off + the default-off flag.

### Paper feature promotion (Model F audit) — added 2026-06-24
> Source of truth: `config/paper_features.yaml`. Active paper features are display/accounting/advisory only. Watch:
- [ ] **Paper Features panel accuracy** — `/api/paper-features` active list matches reality; no feature silently flips to trade-affecting. `affects_trades` must stay false for all active.
- [ ] **Archived shadow-exit manager stays off** — `shadow_exit_manager` remains research-only (not wired); do not re-promote without re-clearing gates.
- [ ] **Kept-shadow features (circuit-breaker block, sector/concentration caps, intelligence layer, position advisor)** — re-evaluate for promotion only once ≥30 closed actionable + ≥+2R counterfactual (or ≥10 would_pause fires for the breaker).

### Paper portfolio (deposit/risk/fees) — added 2026-06-24
> $5000 paper deposit, 0.5%/equity risk, dynamic leverage, net USD after fees/slippage. Source: `/api/portfolio` + `paper_portfolio_ledger`. Watch:
- [ ] **Forward paper equity** vs the replay baseline (Bybit +2.94% / no-cost +47.6%) on trades entered after 2026-06-24.
- [ ] **Fees as % of gross** — replay = ~74% (Bybit). If forward fees stay this high, the edge does not survive; needs maker fills / wider stops / fee-aware sizing (approval).
- [ ] **Risk-capped trade count** — trades with stop < 0.5% hit the notional cap (actual risk < $25); track how often.
- [ ] **Max drawdown** — replay 9.2% (no-cost) → 18.3% (Bybit); watch live.
- [ ] **TP quality** — production TPs are mechanical (ATR ladder); track `tp_structure_validator` warnings; consider a volume-profile module.

## Paper-shadow A/B — weekly forward (added 2026-06-26, observability only)

Forward A/B monitoring **continues** (gate NOT_READY; decide on the forward window in ~2–4 weeks). Each week record from the **By-mode breakdown** (`/api/paper-shadow/breakdown`) + the daily Telegram digest:

- [ ] **Forward B vs A net R / $** (overall + per mode) — only the `forward_since_activation` window counts; backfill is look-ahead, never proof.
- [ ] **Best / worst B mode** — e.g. baseline 2026-06-26: stocks swing ΔR +2.61 (best), stocks invest ΔR −0.40 (worst).
- [ ] **Maker fill rate + missed + taker-fallback** — watch for the edge depending on optimistic fills.
- [ ] **Promotion-gate criteria met** (n/6) + forward trade count toward the 60-trade / 14-day thresholds.
- [ ] **DB size / `signal_outcomes` rows** — run `signal-outcomes-retention --dry-run` to track bloat (≈1994 MB / 371k rows at baseline).
