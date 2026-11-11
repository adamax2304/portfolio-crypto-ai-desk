# Current Testing & Waiting State

> Single human-readable status of what is **implemented**, what is **still testing / waiting**, what is **archived**, and what is **locked**. Last updated: 2026-06-24.
> Source-of-truth configs: [`config/paper_features.yaml`](../config/paper_features.yaml) (feature registry) · [`config/cohort_guard.yaml`](../config/cohort_guard.yaml) (cohort label). Companion docs: `PROJECT_STATE.md`, `docs/DECISION_LOG.md`, `docs/SHADOW_MODE_REGISTRY.md`, `docs/WEEKLY_FORWARD_METRICS.md`.

## 1. Current system status

- **Paper PnL is now computed via `paper_execution_r`** (Model F / `early_mfe_protection_v1`), written to the additive `paper_execution_outcomes` table. This is the **authoritative paper PnL**.
- **`signal_outcomes.final_r` is no longer the main PnL.** It is the legacy **touch-based / highest-TP-touched / optimistic signal-quality metric** — kept and labelled, never the headline.
- **Model F is active for PAPER / ACCOUNTING only:** +0.6R MFE → stop to breakeven; +1.0R MFE → lock +0.5R; runner can reach TP3. It never moves a real stop and never places an order.
- **App / dashboard / Telegram show Paper Execution R and Touch R separately** (Touch R labelled "optimistic / signal-quality").
- **`live` / `auto-live` / `exchange execution` are LOCKED** (`/api/health` → `live_locked:true, auto_live_locked:true`).
- **Historical `final_r` is unchanged** — never rewritten; no `paper_execution_*` column was added to `signal_outcomes`; the new data lives only in `paper_execution_outcomes`.
- **Trade detail is CHART-FIRST with TRUE partial-exit markers** (2026-06-24): clicking any trade opens a candlestick chart with entry/stop/moved-stop/TP1-3 price lines + per-fill markers (TP1/TP2/TP3 fills at true prices — the ENA "single exit near TP1/TP2" was a `Chart.tsx` bug; backend was always correct), then a price-ladder outcome table (price·R·net$·status), lifecycle timeline, setup. Active-after-TP1 partial badges. **Market tab VIX** now loads (yfinance ^VIX + SPY/QQQ trend + ETH/BTC), backfilled in the Opus parser/fallback so it's never blank; shows "VIX unavailable" explicitly otherwise. Signals card overflow fixed. (See `reports/TRADE_UI_MARKET_FIX_FINAL_REPORT.md`.)
- **Paper now uses STRUCTURAL TP + MAKER-FIRST execution under a SAFE MAX-2X leverage policy** (paper only). Production TP generation (mechanical ATR ladder) is UNCHANGED. The structural+maker-first paper book is `bybit_structural_maker_first`; the mechanical-taker baseline is `bybit_non_vip_usdt_perp`. Compare via `/api/portfolio/compare`. Bybit $5000/587: **A +3.72%/$1763 fees → B +8.19%/$1585 fees** (Δ +4.47pp, 177 maker entries). Structural swing/VP TP is **forward-only** (live candles); the historical backfill labels ATR-fallback.

## 2. Active paper / accounting / display features

| feature | status | what it does | affects trades? | evidence | where visible | owner file / report |
|---|---|---|---|---|---|---|
| Model F / `paper_execution_r` | active paper accounting | early MFE-armed protection PnL (BE@+0.6R, lock+0.5R@+1R, runner TP3) | no (accounting only) | replay actionable touch +6.2R → +74.1R, PF 1.43 (forward pending) | dashboard headline, close alerts, ledger | `src/execution/paper_execution_accounting.py` · PAPER_RISK_MANAGEMENT_UPGRADE_FINAL_REPORT.md |
| `touch_r` relabel (optimistic) | active display | demote `final_r` to signal-quality metric | no | touch overstated ~+100..+143R vs realistic | "Recorded Touch R" card | `backend/app/books.py` |
| Paper Features panel | active display | lists active/shadow/archived/locked features + evidence | no | n/a (display) | dashboard panel, `GET /api/paper-features` | `backend/app/paper_features.py` · `config/paper_features.yaml` |
| per-trade feature tags | active display | `model_f` / `be_protected` / `giveback→protected` / `weak cohort` badges | no | n/a | closed-trade rows + detail | `backend/app/books.py::paper_exec_flags` |
| status clarity / lifecycle labels | active display | expired split, lifecycle-aware R, honest active/waiting | no | UNKNOWN_INCONSISTENT 87→3 | all status views | `src/status/display_status.py` |
| close-alert Model F line | active display | shows Paper exec R + protection + "closed at protected stop" | no | n/a | Telegram close alerts | `src/notifiers/close_alert.py` |
| safe **max-5x** leverage policy (2026-06-24; was 2x) | active paper sizing | max 5x, margin ≤25%, notional ≤150%, liq-buffer 3× (reduces leverage on wide stops); tight stops → `risk_capped` (never lever up) | no (paper sizing) | leverage ≠ risk; liquidation kept ≥3× stop distance | per-trade leverage/margin/liq in app | `src/execution/position_sizing.py` · MAX_5X_SAFE_LEVERAGE_POLICY_REPORT.md |
| position lifecycle + partial exits | active paper read-model | TP1 33%/TP2 33%/TP3 34% fills, moved/structural stops, blended R+$, active-after-TP1; derived live | no (read-model) | exchange-like execution view | trade detail `LifecyclePanel` · `/api/trades/{id}/lifecycle` | `backend/app/lifecycle.py` · PAPER_POSITION_LIFECYCLE_IMPLEMENTATION_REPORT.md |
| structural stop after TP | active paper | structural protective stop (swing/SR/VWAP) after TP1/TP2, BE/lock fallback | no | tighter, never-worse protection | execution timeline | `src/execution/structural_stop_manager.py` |
| regime normalization | active display | free-text→canonical enum; unknown only when empty | no | ~223 empty + unmapped were shown "unknown" | trade detail regime label | `backend/app/regime.py` · REGIME_UNKNOWN_FIX_REPORT.md |
| market dashboard | active display | fear&greed/risk-now/regime/news tab written by Opus routine final block | no | new Market tab | Market tab · `/api/market-dashboard` | `src/market/market_dashboard.py` · MARKET_TAB_DASHBOARD_REDESIGN_REPORT.md |
| structural TP (paper) | active paper TP | swing/range/round/VP levels, TP1 ≥ 0.6R, TP3 runner-only, ATR fallback, no fake VP | no (paper TP only; prod unchanged) | forward-only structural; backfill ATR-fallback | trade detail `paper_execution_b.tp_set_label` | `src/execution/structural_tp_engine.py` · STRUCTURAL_TP_ACTIVE_PAPER_IMPLEMENTATION_REPORT.md |
| fee-aware execution (paper) | active paper filter | fee_r_cost + survival labels; skip EXTREME/TIGHT drag | yes (paper book inclusion) | 2 conservative-profile skips on backfill | compare counts | `src/execution/fee_aware_execution.py` · FEE_AWARE_PAPER_EXECUTION_IMPLEMENTATION_REPORT.md |
| maker-first execution (paper) | active paper exec | maker entry for pullback, maker TP, stop always taker, conservative fills | no (accounting of fees) | Bybit fees −$178, +4.47pp | `/api/portfolio/compare`, trade detail, close alert | `src/execution/maker_first_execution.py` · MAKER_FIRST_ACTIVE_PAPER_IMPLEMENTATION_REPORT.md |
| catalyst label refresh / integrity | active advisory | re-derive news_supported/telegram_supported; data-quality | no | fixes scan-time ~5h news under-fire | reports, catalyst labels | `src/signals/catalyst_label_refresh.py` |
| funding / OI archive | active data | append-only archival for path replay | no | enables path-aware replay | n/a (data) | scheduler `ohlcv_archive` / `intelligence_update` |
| risk-guard warnings (advisory) | active advisory | circuit-breaker would_pause / sector-cap / correlation / profit-hint as **warning lines**, fail-open, never block | no | advisory only | paper-entry Telegram alert | `src/risk/risk_guards.py` |
| cohort guard `warn` label | active display | label `crypto_intraday_catalyst_or_momentum` as weak (chase-long) | no (label only, no routing) | +0.02R/trade (weakest actionable) | "weak cohort" badge, panel | `config/cohort_guard.yaml` |

## 3. What we are still testing / waiting for

| feature / test | current mode | what we wait for | promotion gate | current blocker | next review |
|---|---|---|---|---|---|
| **Model F forward validation** | active paper accounting (replay-proven) | post-2026-06-24 forward `paper_execution_r` | net-positive forward after costs, n≥30 fresh, stable ≥2 regimes | only ~hours of forward data | 7–14 days (≥2026-07-01) |
| **Cost/slippage haircut** | not yet applied | realistic fee/spread/slippage model | +74R edge survives haircut (BE-heavy ~42% scratch) | haircut model not built | before any paper-flag |
| **crypto_intraday_catalyst cohort** | `warn` (label only) | forward `paper_execution_r` for the cohort | operator approval before any routing/actionability change | weak cohort, thin sample | with Model F forward review |
| **Circuit breaker as block** | advisory / warning only | ≥10 meaningful `would_pause` fires, ≥30 affected closed trades, proof DD↓ without killing winners | gate above + sign-off | not enough fires | when fires accumulate |
| **Sector/concentration/correlation caps as block** | advisory / warning only | proof of drawdown reduction, no Model F winner kill, enough affected trades | counterfactual net-positive + sign-off | insufficient binds | when binds accumulate |
| **Intelligence layer** (timeline/derivatives/squeeze/funding-OI) | measuring / shadow | ≥30 closed affected trades, +2R or clear decision-quality gain under `paper_execution_r`, reliable labels | gate above | <30 closed actionable | rolling |
| **Position/leverage advisor** | label / measuring only | evidence it improves sizing/risk without ↑ drawdown, no live/exec | forward sizing evidence | no evidence yet | rolling |
| **Adaptive TP3** | research / advisory | forward evidence under `paper_execution_r` | display/advisory only unless hard evidence | Model F already handles give-back earlier → TP-count change not needed | rolling |

## 4. Archived / killed / superseded

| feature | status | why |
|---|---|---|
| `shadow_exit_manager` variants A–I (BE / partial / trailing / reentry) | **ARCHIVED — SUPERSEDED_BY_MODEL_F** | They arm protection at/after TP1 (~1R), which is too late — the actionable book stays −96..−137R. Model F arms at +0.6R favorable → +74.1R. **Kept for research/replay only** (`scripts/shadow_exit_ledger_update.py`, `scripts/tp_stop_replay.py`); **NOT wired** to the tracker/scheduler; not promoted. See `config/paper_features.yaml` (`state: archived`) + `reports/SHADOW_FEATURE_ARCHIVE_REPORT.md`. |

## 5. Dangerous / locked / do not enable

| item | status | why locked | evidence required to revisit |
|---|---|---|---|
| crypto scalp actionable | LOCKED-POLICY shadow | net-negative under every model | operator-only, on materially stronger evidence |
| stocks C-tier actionable | LOCKED-POLICY shadow | 30d C-tier = −34R drag | operator-only |
| stocks swing / invest actionable | LOCKED-POLICY paused | paused by policy | operator-only |
| live / auto-live / exchange execution | HARD-LOCKED | no forward-validated profitable edge; not live-ready | sustained forward paper edge + manual review + explicit sign-off |
| any production exit change (BE/partial/trailing in the real tracker) | LOCKED | Model F is paper-accounting only; production exits unproven live | forward paper success + gates + sign-off |
| any routing / actionability change | LOCKED without approval | safety contract | explicit operator approval per change |

Current status of all the above remains **shadow / review / paused** — none are enabled.

## 6. Operator approval boundaries

These require explicit operator approval before proceeding:

- Model F: **paper/accounting → paper execution flag** (moving real paper stops).
- cohort guard: **`warn` → `paper_review_only`** (paper routing change; gated behind `paper_cohort_guard.enabled`, default false).
- circuit breaker: **warning → block**.
- sector / concentration / correlation: **warning → block**.
- any scoring / routing / actionability change.
- any production / live / exchange execution.
- any C-tier / scalp / swing-invest actionability.

## 7. Next 7-day watchlist

- forward `paper_execution_r` (Operator book, trades entered after 2026-06-24);
- touch vs paper divergence (`touch_minus_paper_r`);
- `protected_n`;
- BE-scratch count (`be_scratch_n`);
- `original_stops_avoided_n`;
- `giveback_n`;
- weak-cohort (`crypto_intraday_catalyst_or_momentum`) forward R;
- `paper_unavailable_n` stays 0 (missing-MFE → warning, never silently zeroed);
- Model F result **after cost/slippage haircut**;
- app Paper-Features panel consistency (no active feature silently flips to trade-affecting);
- archived features remain off (`shadow_exit_manager` not wired).

## 8. Current verdict

`CURRENT_SYSTEM_STATUS`:
- `PAPER_EXECUTION_ACCOUNTING_ACTIVE`
- `MODEL_F_ACTIVE_FOR_PAPER_ACCOUNTING`
- `TOUCH_R_LABELLED_OPTIMISTIC`
- `PAPER_FEATURE_REGISTRY_ACTIVE`
- `TRADE_AFFECTING_SHADOW_FEATURES_NOT_PROMOTED`
- `OLD_SHADOW_EXIT_MANAGER_ARCHIVED`
- `LIVE_LOCKED`
- `READY_FOR_FORWARD_PAPER_VALIDATION`

---
## Update 2026-06-24 — Paper portfolio + sizing + dynamic leverage + fees

**Now active (paper/accounting/app only):**
- **Paper deposit $5000**, **risk 0.5%/equity** ($25/trade, compounding) — `config/paper_portfolio.yaml`.
- **Position sizing** (`src/execution/position_sizing.py`): notional = risk / stop-distance; loss-at-stop ≈ risk. **Leverage ≠ risk.**
- **Dynamic leverage**: minimum integer to keep margin ≤20% equity, clamped ≤5x, liquidation-buffer-aware.
- **Fees/slippage** (`config/fee_profiles.yaml`, `src/execution/fees.py`): bybit/mexc/conservative/zero; net = gross − fees − slippage − funding. **Paper PnL uses net USD after fees/slippage** (from `paper_execution_r`, never touch_r).
- **`paper_portfolio_ledger`** table + backfill (`scripts/paper_portfolio_backfill.py`) → equity-curve + ledger CSVs.
- **App**: Paper Equity / Today Net $ + R / Max DD / Fees cards; `/api/portfolio`; `/api/trades/{id}/chart-events` (entry/stop/TP/moved-stop markers). Telegram close alert carries a Paper $ line.
- **TP structural validator** (`src/execution/tp_structure_validator.py`) — display-only.

**Key finding:** production **TP levels are MECHANICAL (ATR ladder `close ± 1/2/3·ATR`)**, not structural; stops are semi-structural; volume-profile module does not exist (unknown). Backfill: $5000 → **+47.6% no-cost, +2.94% Bybit, +16.3% MEXC, −5.65% conservative** → Model F edge is real but **fee-fragile**.

**Still waiting / watch:** forward paper equity vs the +2.9% Bybit replay; fees-as-% of gross; risk-capped (tight-stop) trade count; whether a fee-aware/wider-stop variant survives costs (strategy change → approval).

**Blocked until approval:** live/auto-live/exchange/real-orders; production exits/TP-SL; making TP generation structural; fee-survival strategy changes; routing/actionability/scoring changes. `final_r` never rewritten; live locked.

---
## Update 2026-06-24 (b) — Paper portfolio bugfix (fees / expired / TP-R / leverage / chart)

**Fixed (paper/app only, no live, no final_r rewrite):**
- **Fees:** close fee now on EXIT notional (was entry); per-side rates; `config/fee_profiles.yaml` with source/last_verified + `fee_estimated`; profiles bybit_non_vip_usdt_perp / mexc_default_futures / mexc_conservative_api / conservative_taker / custom_account_override / zero.
- **Expired:** close at implied price from `paper_execution_r` + `expiry_close_price`(+source) + `expired_exit` chart marker (exit_price was NULL on all rows; now 0 NULL).
- **TP R exact:** app + Telegram show 1.2/2.2/3.2R etc., not "+1R". TPs labelled MECHANICAL_ATR_LADDER (VP unknown).
- **Leverage visible:** dashboard avg/max + risk-capped; per-trade leverage/margin/notional/risk; Telegram Paper $ line. leverage != risk.
- **Chart markers:** `/api/trades/{id}/chart-events` markers (entry/exit/expired/stops/TPs + R + $) + detail timeline.

**Rebuilt ledger ($5000, 586 trades):** no-cost +47.45%, Bybit +2.82%, MEXC +16.15%, conservative -5.76%.

**Still TODO / watch:** full candlestick line-overlay on Chart.tsx (markers timeline live now); volume-profile module to make TPs structural (approval-gated); pull account-specific fee rate into custom_account_override; forward equity vs +2.82% Bybit replay; fees-as-% of gross (~74%).
