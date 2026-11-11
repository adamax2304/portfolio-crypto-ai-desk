# Stocks Position Framework — Phase 1 (shadow-only) — implementation report

**Date:** 2026-07-02 · **Scope:** shadow/research only. No live, no auto-live, no manual-live, no
Telegram, no actionability, no scoring changes, no change to `signal_outcomes.final_r`. Existing
stocks **intraday** untouched. Paper/PnL contract unchanged (USD net authoritative,
`paper_execution_r` auxiliary, `legacy_touch_r` diagnostic only). Live remains **LOCKED**.

## What was built

New module `src/stocks/position_framework/` (active playbook: **`stocks_swing_growth_breakout`**
only; long-only; weekly/daily). `stocks_swing_earnings_drift` (Phase 2) and
`stocks_invest_stage2_position` (Phase 3) exist only as **disabled placeholders** in config.

- `__init__.py` — constants; `asset_class="stocks"`, `mode="swing"` (reuses existing mode, NOT a
  new mode), `playbook="stocks_swing_growth_breakout"`, `status="shadow_open"`.
- `config.py` — loads `config/stocks/position_framework.yaml`; `is_shadow_only` fails safe True.
- `features.py` — pure indicators (SMA/EMA 10/21/50/200, ATR14, volume_ratio, dollar_volume_30d,
  pct-below-3M/6M/52W-high, RS vs SPY/QQQ/sector). Missing history → `None`, never fabricated.
- `setup_detector.py` — market→sector→stock gates + 4 variants (breakout / pullback_21d_50d /
  reclaim_after_shakeout / consolidation_continuation). Long-only. Score 0–100, data_confidence,
  reasons/warnings/rejection_reasons, thesis/counter-thesis.
- `risk_plan.py` — ATR-buffered structural stop clamped to [min,max]·ATR; rejects too-wide stops;
  **exact R multiples** stored; gap-risk-aware sizing.
- `shadow_store.py` — **separate** tables `stocks_position_candidates` + `stocks_position_outcomes`
  (CREATE TABLE IF NOT EXISTS; additive/migration-safe). Never writes `proposed_signals`.
- `runner.py` — orchestrates existing collectors (StockOHLCV / MarketIndex / SectorETF / Earnings)
  → features → detector → persist. No Telegram, no live.
- `report.py` — Markdown with a mandatory SHADOW-ONLY banner; outcomes render **pending /
  unavailable** (no fake PnL).

Config: `config/stocks/position_framework.yaml` (enabled, shadow_only, write_proposed_signals=false,
universe/market/sector/stock filters, setups, risk, exits, evidence_gate).

CLI (`src/cli.py`): `stocks-position-scan` (`--dry-run`, `--no-update`, `--symbols`, `--limit`),
`stocks-position-report`, `stocks-position-outcome-refresh` (honest skeleton — stamps last price,
leaves PnL NULL/pending, no fake fills). Every command prints the SHADOW-ONLY banner.

## Retired / deprecated old stocks swing/invest (not paused-to-return)

- `config/sizing_weights.yaml` — old `stocks_swing_watchlist_rs_rotation` /
  `stocks_invest_watchlist_30d_thesis` marked DEPRECATED/REMOVED (0×, never sized); new
  `stocks_swing_growth_breakout` listed 0× shadow-only (not sized).
- `config/paper_features.yaml` — reworded to deprecated/removed + replaced by shadow framework;
  actionability stays hard-disabled. Added `stocks_position_framework_shadow` (keep_shadow).
- `src/analysis/packet.py` — sizing + playbook context now show the two old playbooks as
  DEPRECATED/REMOVED; added a new **"Stocks Position Framework — shadow-only research"** Opus
  extended-analysis block (Opus tasks + must-NOT list; review as research candidates only).
- Dashboard/journal text: `write_obsidian_current_state_dashboard.py`,
  `refresh_obsidian_dashboard.py`, `build_live_shadow_journal.py` reworded paused→deprecated/removed
  + new shadow lane shown separately.
- **actionability.py (control-plane): left intact** — the existing hard block for
  `asset=stocks & mode in (swing,invest)` → `mode_paused` already blocks any stray row; the new
  framework never writes `proposed_signals`, so it is doubly guaranteed non-actionable.

## Commands run + results

- `pytest tests/stocks/test_position_framework.py -q` → **10 passed** (config / features / detector
  gates / risk-plan exact-R / shadow-table-storage-never-proposed_signals / CLI smoke).
- `pytest tests/stocks tests/test_stock_intraday_coverage.py tests/test_intraday_lifecycle.py -q`
  → **60 passed** (stocks intraday regression clean).
- `pytest tests/test_sizing.py tests/test_playbook_labels.py tests/test_audit_fixes_engine.py
  tests/test_paper_entry_alerts.py -q` → **62 passed** (sizing/playbook/packet wording intact).
- `pytest tests -q` (full desk) → **958 passed, 2 failed**. The 2 failures are in
  `tests/test_risk_guard_fields.py` (paper-entry freshness), pre-existing and **unrelated** to this
  PR (time-sensitive: fixed `NOW` makes the entry "283m very late" → `late_shadow`; that file
  references none of position_framework/packet/sizing/paper_features).
- Control-plane: `pytest backend/tests/test_control_plane.py test_paper_features.py test_books.py -q`
  → **50 passed** (live_locked=True, actionability hard-block intact). `npm run build` → **exit 0**.
- Live wiring proof: `python -m src.cli stocks-position-scan --symbols … --dry-run` and a real
  persisting scan (10 megacaps) → ran clean end-to-end, market=risk_on, 0 candidates (strict gates:
  below 50/200D, RS negative, sector ETFs breaking, low volume), report written to
  `reports/stocks_position_framework_latest.md`, both shadow tables created (0 rows — honest).

## Skipped (deliberate)

- **Control-plane UI card / endpoints** — skipped for Phase 1. The backend is live-locked and
  redeploys have caused watchdog churn; the directive permits skipping UI if the report file exists
  (it does). Next: add read-only `GET /api/stocks-position/summary` + `/candidates` (query the
  separate `stocks_position_candidates` table via the existing read-only desk connection) and a
  separate "Stocks Position Shadow" card — never mixed into the operator/paper book.
- **Outcome engine (USD-net simulation)** — table + read/report skeleton shipped; PnL intentionally
  left pending (no fake fills). Next: simulate entry-fill → partials(+2R/+3R) → 21D-EMA trail →
  50D-hard-exit → sector-breakdown exit → 40-day cap, in **USD net** (commission-free + ~1bp; no
  perp funding for equities), writing `net_pnl_usd` + `paper_execution_r`.
- **Daily scheduler step** — not added (kept schedule untouched). Next: optional flag-guarded
  after-US-close step in `scripts/run_default_market_schedule.py` that never blocks other lanes.

## Exact next steps (do NOT implement now)

- **Phase 2 — `stocks_swing_earnings_drift`:** enable the placeholder; use
  EarningsCalendarCollector as the *signal* (post-earnings drift), validate earnings-reaction edge
  on forward data; keep shadow-only.
- **Phase 3 — `stocks_invest_stage2_position`:** enable the placeholder; 2–6 month horizon, weekly
  10W/30W structure; separate longer evidence gate.
- **Promotion gate (all phases):** ≥28 forward days, ≥30 forward trades, net-USD positive, better
  than old stocks swing, acceptable drawdown — AND operator sign-off. Backfill is not proof.

---

## Phase 1 tail-close (2026-07-02) — old swing/invest fully retired + hardening

Closed the remaining ways the OLD stocks swing/invest could still run:

1. **Old CLI neutralised** — `stocks-swing-report` / `stocks-invest-report` no longer call
   `_run_stocks_report`; they print "Old stocks swing/invest are DEPRECATED/REMOVED. Use
   stocks-position-scan…" and exit 0 (no pipeline, no trade_ideas, no proposed_signals). Banner
   wording "removed/paused" → "deprecated/removed".
2. **Pipeline hard guard** — `StocksPipeline.run_report()` raises `ValueError("old stocks
   swing/invest pipeline deprecated/removed; use stocks-position-scan")` at the very top for
   `mode in (swing, invest)`, BEFORE any fetch/`save_trade_ideas`/`register_ideas`. Intraday
   unaffected.
3. **Control-plane actionability** — reason text now "old stocks swing/invest deprecated/removed;
   new stocks position framework is shadow-only"; `blocked_reason` kept `mode_paused` for
   API/frontend compatibility.
4. **Stricter missing-data gates** (`setup_detector.py`) — missing `rs_spy`, missing sector RS
   (when a sector ETF is mapped), and missing SPY/QQQ regime data now **reject** (were warnings /
   caution). Better to skip than accept a partial-data candidate.
5. **Weekly features** — `weekly_above_10w` / `weekly_above_30w` / `weekly_30w_slope_positive`
   (from 1wk bars the runner now fetches). Absent weekly data → warning, non-blocking (Phase 1).
6. **Universe expanded** — `config/stocks/position_framework.yaml` now carries a curated ~68
   liquid US large/mega-caps + a self-contained `sector_map` (no ETFs as candidates; no new/paid
   providers; does NOT touch the shared `universe.yaml`).
7. **Scheduler** — removed the old `stocks-swing/invest-report` daily steps; added an optional
   fail-open `stocks-position-scan` step guarded by `scheduler_enabled` (default **false** → a
   "disabled" note step). No Telegram/actionability/live.
8. **Control-plane read-only API** — `GET /api/stocks-position/summary` +
   `/api/stocks-position/candidates` (new `backend/app/stocks_position.py`) read the shadow tables
   via the existing read-only desk connection; always `shadow_only=true, actionable=false,
   live_locked=true`; empty payload when no scan/DB. UI card deferred to next iteration.

**Verification:** `test_position_framework.py` **16 passed** (added CLI-deprecation, pipeline-guard,
intraday-not-blocked, stricter-gates tests); consolidated stocks/intraday/pause/sizing/playbook
**120 passed**; control-plane `test_stocks_position.py`+control_plane+books+paper_features
**54 passed**; `npm run build` **exit 0**; manual `stocks-swing-report`/`stocks-invest-report`
print the deprecation + exit 0; `stocks-position-scan --dry-run` runs clean (weekly fetch + stricter
gates). Pre-existing unrelated failures: 2 in `tests/test_risk_guard_fields.py` (freshness time-bomb).
**Live remains LOCKED.**

---

## Phase 1 cleanup (2026-07-02) — monitorable + forward-audit-ready

1. **Schedulers scrubbed** — removed `stocks-swing-report` / `stocks-invest-report` from ALL
   scheduler flows (`run_12h_monitor_schedule.py`, `run_default_market_schedule.py`,
   `run_24h_crypto_only_schedule.py`) — not even as a no-op. The only stocks step is
   `stocks-position-scan`, gated by `scheduler_enabled` (default false). Stale references in
   docstrings / CLI-validation / forbidden lists / `refresh_obsidian_dashboard.py` rewritten to
   "old removed; new shadow-only". Verified: zero `_cli("stocks-swing/invest-report")` calls remain.
2. **Frontend card** — `Stocks Position Shadow` in the Market tab (`screens.tsx` +
   `types.ts`/`api.ts`/`query.ts`): latest scan, open-candidate count, outcomes availability, top
   candidates (entry/stop/TP1), explicit `SHADOW ONLY · no live/Telegram/actionability` label, and
   an honest empty state. Consumes the read-only `/api/stocks-position/*` endpoints.
3. **Outcome engine** — new `outcome_engine.py` (SHADOW/read-model). Realistic daily-bar execution:
   entry only on a real zone-cross (gap → fill at open), OHLC stop/target, +2R/+3R partials booked
   only if reached (no R-rounding), 21D-EMA trail / 50D hard exit / max-hold, US-equity
   fees+slippage (separate from crypto), gap-aware stop fills. Per-trade record (symbol/sector/
   setup/dates/px/qty/notional/gross/fees/slippage/net/net_pct/MAE/MFE/exit_reason) + aggregate
   (total/avg net USD, winrate, PF, expectancy, max-DD, by-sector, by-setup). **USD net, never
   final_r.** No fake fills — insufficient forward bars → `pending`. Wired to
   `stocks-position-outcome-refresh`.
4. **Universe/sector guard** — `validate_universe()` (every symbol mapped; only fetchable ETFs);
   the runner now SKIPS (with reason) any symbol lacking a sector mapping rather than scanning it
   with the sector gate silently bypassed. Missing SPY/QQQ/sector/RS data → reject, never neutral.
5. **Runbook clarity** — the report now shows `scheduler_enabled`, latest scan, stored candidates,
   outcome counts (closed/pending/no-entry), a small-sample warning, and an explicit **"No
   profitability conclusion until ≥N forward candidates resolve through the outcome engine (USD
   net); backfill is not proof."** USD-net metrics render once closed trades exist.
6. **Freshness time-bomb fixed** — `test_risk_guard_fields.py` now stamps a real-now entry
   timestamp (freshness is computed vs wall-clock inside `send_paper_entry_alert`), so it no longer
   flips to `late_shadow` after 12:15 UTC. Test-only; no live behavior change.

**Verification:** `test_position_framework.py` **23 passed** (+7: universe guard ×2, outcome engine
×5); `test_risk_guard_fields.py` **5 passed**; control-plane `test_stocks_position.py` +
control_plane + books + paper_features **55 passed** (+ serialization/read-only); `npm run build`
**exit 0** (card compiled). Manual `stocks-position-report --limit 10` renders the runbook + USD-net
contract; `stocks-position-outcome-refresh` wired clean. **SQLite sanity:** `proposed_signals`
(2857) and `signal_outcomes` (461091) row counts **unchanged** by the stocks-position commands
(read-only proven). Old stocks swing/invest are **not scheduled anywhere**. stocks-position remains
**shadow-only**. **Live remains LOCKED.**

---

## Phase 1 QA hardening (2026-07-02) — 5 audit findings fixed

1. **Schedule test updated** — `tests/test_default_market_schedule.py` rewritten for the new
   contract: crypto swing daily stays; NO stocks swing/invest steps; `scheduler_enabled=false` →
   "stocks position framework scan (disabled)" note; `=true` → shadow scan; weekend/crypto-only
   exclude the position scan. New guard test asserts no label/argv contains `stocks-swing-report`
   / `stocks-invest-report` across all scenarios × both scheduler states.
2. **Windows cp1252-safe CLI** — `stocks-position-report` no longer dumps the unicode Markdown
   (⚠️ / ≥ / arrows) to stdout. New `report.ascii_summary()` prints a pure-ASCII summary; the full
   Markdown stays in the FILE. Verified `PYTHONIOENCODING=cp1252 … stocks-position-report` → exit 0.
3. **Outcome engine entry realism** — entry is now buy-stop (breakout/continuation) vs buy-limit
   (pullback/reclaim): a **gap-up OPEN above the entry fills at the open**, no longer mis-counted as
   `no_entry`. `entry_low/entry_high` bound the zone / pick direction.
4. **Outcome engine exit realism** — `exit_px` is the **actual closing fill**, never the bar close:
   stop → stop price (or the OPEN on a gap-down through it); EMA-trail / 50D / max-hold → the close.
   Gap fills recompute `actual_risk = fill_px − stop` for the auxiliary MFE/MAE-in-R metrics (R
   values are decimals, never rounded to whole R). USD net stays authoritative.
5. **Open/closed consistency** — a terminal outcome (`closed`/`no_entry`) removes the candidate from
   the open list two ways: the engine flips `stocks_position_candidates.status` to
   `shadow_closed`/`shadow_no_entry`, **and** `shadow_store.latest_candidates` + the control-plane
   `/api/stocks-position/*` queries LEFT JOIN outcomes and exclude terminal statuses. `Open
   candidates` now reflects only genuinely open/pending shadow candidates.

**Verification:** `test_position_framework.py` **27 passed** (+gap-up-fill, +stop-exit-px,
+terminal-consistency, +cp1252-CLI-subprocess); `test_default_market_schedule.py` **all passed**
(+no-old-commands guard); `test_risk_guard_fields.py` **5 passed** — combined crypto run **61
passed**. Control-plane `test_stocks_position.py` + control_plane + books + paper_features **56
passed** (+terminal-excluded-from-open). `npm run build` **exit 0**. Manual
`stocks-position-report --limit 10` under cp1252 stdout → **exit 0**; `stocks-position-outcome-refresh
--no-update` clean. **Live remains LOCKED; stocks-position shadow-only; old swing/invest not
scheduled anywhere; no profitability conclusion until real forward USD-net outcomes exist.**

---

## Phase 1 enriched-review layer (2026-07-02) — Opus shadow review, read-only

Adds a dedicated enriched-analysis packet + review layer for the shadow candidates. **Still SHADOW
ONLY**: never changes candidates, never writes proposed_signals / signal_outcomes / paper_*, never
Telegram, never actionable/live.

- **Packet builder** `src/stocks/position_framework/llm_packet.py` →
  `data/processed/llm_stocks_position_packet.md`. Sections: SHADOW disclaimer, latest scan,
  scheduler state, open count, outcomes summary (USD-net only), evidence gate + explicit
  "no profitability conclusion", top candidates (full fields + per-ticker local news), recent closed
  outcomes, risk notes (correlation/sector/gap/earnings/legal + "do not promote"), and the Opus
  verdict-JSON instructions.
- **Per-ticker context** `news_context.py` — LOCAL cache only (reuses `load_recent_news`,
  `legal_risk.load_active_legal_news`/`detect_legal_risk`, `earnings_freshness`, the events table).
  No network, no paid providers; when nothing exists it prints **"No reliable ticker-specific news
  found in local cache"** (never fabricates).
- **Review storage** — new separate table `stocks_position_reviews` (candidate_id, reviewed_at,
  reviewer/source, verdict, confidence, reasons/key_news/risk_notes JSON, raw_review, markdown_path).
  Distinct from proposed_signals / signal_outcomes / paper_execution_outcomes /
  paper_shadow_execution_outcomes.
- **CLI:** `prepare-analysis --asset-class stocks-position` (+ alias `prepare-stocks-position-analysis`),
  and `ingest-stocks-position-review --file <path>` — validates candidate_id exists, parses raw
  JSON or ```json fences, upserts into `stocks_position_reviews` ONLY; never alters candidate/status,
  never promotes.
- **Routine docs:** `prompts/llm_review/enriched_market_review_protocol.md` — added the packet to §2
  read list and a new **§18 "Stocks Position Framework — shadow-only review"** (verdict schema:
  approve_shadow / wait_pullback / reject_news_risk / reject_earnings_risk / reject_legal_risk /
  needs_more_data; reject on earnings/legal/headline; prefer wait; never actionable/live). Scheduler
  no-LLM guarantee intact (packet is file-based; not auto-called).
- **Control-plane:** the shadow card + `/api/stocks-position/*` now LEFT JOIN reviews and surface the
  latest `review_verdict` / `confidence` / `reviewed_at` per candidate (read-only badge).

**Verification:** `test_position_framework_llm_packet.py` **7 passed** (empty-DB build; shadow-only /
no-actionability / not-live; candidate + outcome summary; missing-news-explicit-not-fabricated;
review parse; ingest rejects unknown id + writes only reviews table + no candidate/status change;
`prepare-analysis --asset-class stocks-position` exit 0). Combined crypto (position_framework +
llm_packet + schedule + risk_guard) **68 passed**. Control-plane (stocks_position + control_plane +
books + paper_features) **57 passed** (+review-verdict surfaced). `npm run build` **exit 0**. Manual
`prepare-analysis --asset-class stocks-position` writes the packet; `stocks-position-report` cp1252
**exit 0**. **stocks-position remains shadow-only; the review layer is read-only; no
live/paper/actionability/Telegram changes; no old stocks swing/invest restored.**
