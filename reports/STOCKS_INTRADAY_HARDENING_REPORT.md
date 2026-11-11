# Stocks Intraday — paper/actionable hardening (2026-07-02)

**Scope:** stocks INTRADAY paper/actionability only. No live / auto-live / manual-live changes. Old
stocks swing/invest NOT restored (still deprecated/removed + hard-blocked). The new
stocks-position framework stays shadow-only. All performance uses `paper_execution_r` (Model F),
never legacy `final_r`.

## Root cause found
The technical agent's ATR geometry set the stop **1.5·ATR** from the entry anchor while TP1 sat
**1.5·ATR** away → `rr_to_tp1` was mechanically **≈1.0 for every setup**, so the existing
`require_rr_to_tp1_gte: 1.5` gate could never pass. That is why 100% of 30-day A/B were sub-1.5R.

## Changes

1. **TP/stop math** (`technical_agent.py`) — stop tightened to a **1.0·ATR structural** stop and TP1
   is now the **structural prior-day extreme** (`prev_h`/`prev_l`) when it is a real level beyond
   entry, else a measured 1.5·ATR objective. `rr_to_tp1` is computed from those real levels (no
   artificial TP stretch); TP2/TP3 kept monotonic.
2. **Hard RR gate** (`trade_idea_agent.py`) — an A/B idea with `rr_to_tp1 < require_rr_to_tp1_gte`
   (or missing) can **never** be A/B → demoted to C with cap_reason `rr_below_min_required`. C/rejected
   are never actionable.
3. **Rolling drawdown guards** (new `src/stocks/intraday_guards.py`, wired into the idea agent) —
   READ-ONLY over `paper_execution_r`. Global 7-day circuit breaker (`stocks_intraday_7d_drawdown_guard`)
   + per-direction guard (`stocks_intraday_long_guard` / `stocks_intraday_short_guard`, 7d+14d). A weak
   long-cohort long survives only with extra confirmation (RS>0, sector not weak, not extended,
   volume). Demotes NEW A/B to C; never live, never crypto (query filters `asset_class='stocks' AND
   mode='intraday'`).
4. **Sector/RS/volume/RR persistence** — idea now carries `raw.candidate.sector` (→ the
   `proposed_signals.sector` column) and `raw.structured` (sector_etf, rs_vs_spy, rs_vs_sector,
   volume_ratio, rr_to_tp1) into `raw_idea_json`.
5. **Report wording + sections** (`stocks_report_builder.py`) — `## 6. A/B Actionable Candidates`
   now prints explicit **Levels** (entry_low/high · stop · TP1 · **rr_to_tp1**) + Context (sector/RS/
   vol). `## 7. C-tier Watchlist — NOT actionable` is built from the IDEAS payload (so DEMOTED A/B
   appear here with their demote reason instead of vanishing) and every line is marked
   **watchlist / not actionable**. `## 8. Rejected / Not Ready` unchanged.
6. **Quality analytics** (`## 9. Intraday A/B Quality`) — A/B `paper_execution_r` by direction
   (7/14/30d), and 30d breakdowns by RR bucket (<1.5R / 1.5-2R / >2R), regime, setup_type, catalyst,
   and sector. Explicitly "NOT legacy final_r".
7. **Circuit breaker** — see (3): global + long + short, config-driven (`risk.yaml:intraday_guards`),
   read-only over `paper_execution_outcomes`.
8. **Enriched review hook** (`llm_packet.py`) — the stocks intraday LLM packet now lists current
   open A/B candidates (RR/sector/RS/regime/catalyst) + recent cohort stats and asks Opus to
   **approve / wait / reject**. No auto-LLM from the scheduler; ingestion stays read-only.

## Config (`config/stocks/risk.yaml`)
`structure.require_rr_to_tp1_gte: 1.5` (now a hard invariant) + new `intraday_guards` block
(enforce_rr_hard_gate, circuit_breaker 7d PF<0.8/netR<-3, direction_guard 7/14d, long_extra_confirmation).

## Before / after (report)
- **Before:** `## 6. Trade Ideas (A/B-tier)` listed intraday A/B with Entry/Invalidation/Targets but
  **no RR shown** (and rr was mechanically ~1.0); C-tier watchlist rendered a playbook `status`
  that could read as actionable; no quality analytics; `proposed_signals.sector` empty.
- **After (live run, `stocks-intraday-report --no-update`):** `Regime=risk_on | **A/B ideas=0** |
  C watchlist=10 | rejected=5`. During the current 7-day drawdown the RR gate + guards correctly
  demote all A/B to a **watchlist / not actionable** section (each with its demote reason), the A/B
  section prints explicit `Levels … rr_to_tp1`, and the `Intraday A/B Quality` block shows the
  `paper_execution_r` cohort tables. The guard reproduces the audit exactly (7d −5.33R/PF0.24, 14d
  −6.83R/PF0.60; longs negative, shorts positive).

## Verification
- `pytest tests/test_stocks_intraday_hardening.py` → **8 passed** (RR gate can't be A/B; C-tier never
  actionable wording; sector/RS persist; rolling guard demotes weak long cohort; guard is
  stocks-intraday-only not crypto; analytics uses paper_execution_r; old swing/invest blocked).
- `pytest test_default_market_schedule + test_stocks_swing_pause + test_stocks_invest_pause +
  stocks/test_position_framework` → passed (batch **83 passed**).
- Consolidated stocks regression (tests/stocks + intraday coverage/lifecycle + pause + sizing +
  playbook + hardening) → **146 passed**.
- `stocks-intraday-report --no-update` → report written (A/B 0 / C 10 / 5 rejected), packet refreshed.
- `prepare-analysis --asset-class stocks --mode intraday` → exit 0 (packet has the A/B enriched-review
  section).

## Explicit confirmation
- No live / auto-live / manual-live changes.
- Old stocks swing/invest NOT restored (CLI no-op + `run_report` hard-blocked).
- stocks-position framework remains shadow-only.
- stocks intraday remains **paper / actionability only**; guards are read-only and never affect crypto.
