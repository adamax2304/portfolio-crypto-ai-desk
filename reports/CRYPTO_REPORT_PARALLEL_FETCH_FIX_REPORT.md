# Crypto Report Parallel-Fetch Fix Report (P1)

**Date:** 2026-06-07 · Approved runtime optimization for the crypto
scalp/intraday report timeout. **No trading strategy / scoring / thresholds /
stop-TP / signal logic / A/B tier logic changed. No auto-trade. Timeout NOT
raised.**

## 1. Root cause recap
Crypto reports were not hanging — they legitimately ran ~2270–2622 s against a
2700 s wall, so normal network/API variance pushed daytime cycles over. The
fetch path in `Supervisor.update_data` ran **sequentially**: Binance→Bybit→MEXC
OHLCV, then Binance→multi→Bybit-history derivatives, then news→social. Measured
(18 symbols): OHLCV 137 s sequential, derivatives 370 s sequential. (Full
diagnostic: `CRYPTO_REPORT_TIMEOUT_DIAGNOSTIC_REPORT.md`.)

## 2. Files changed
| File | Change |
|---|---|
| `src/agents/supervisor.py` | Parallelized the independent OHLCV + derivatives fetches in `update_data` (two bounded-concurrency waves); added `_parallel_fetch` helper; added `concurrent.futures.ThreadPoolExecutor` import. Stage-timing wraps retained. |
| `src/diagnostics/stage_timer.py` | (prior diagnostic) per-stage timing logger — unchanged. |
| `tests/test_parallel_fetch.py` | New — 6 tests for the concurrency primitive. |
| `scripts/_measure_report_fetch.py` | (diagnostic) isolated before/after measurement. |

No agent/scoring/report-content files touched.

## 3. Concurrency design
- **Two bounded waves** (`max_workers=4`), preserving the OHLCV→`fetched_symbols`
  dependency:
  - **Wave 1 — OHLCV:** Binance (anchor) + enabled secondaries (Bybit, MEXC) run
    concurrently. Wall ≈ slowest exchange instead of the sum.
  - **Wave 2 — derivatives:** Binance + multi-exchange + Bybit-history run
    concurrently.
- **News (writes SQLite) + social stay on the MAIN thread**, sequentially after
  the waves. `db.save_symbols` stays on the main thread (between waves).
- Identical symbol set, identical collectors, identical cache paths, identical
  downstream agents/scoring. **Only fetch *scheduling* changed.**

## 4. Safety measures
- **Bounded concurrency** (`max_workers=4`); at most 2 concurrent calls per host
  (e.g. Binance OHLCV + Binance derivatives are in different waves, so never
  simultaneous) → no rate-limit hammering.
- **Distinct cache files per collector** → concurrent writes never collide.
- **No SQLite writes inside worker threads** (news + save_symbols on main thread).
- **Per-source budget** `report_setting('fetch_source_timeout_s', 600)`: a source
  exceeding it (or raising) degrades to `None`, is logged
  (`SOURCE_FAIL …` + `_log_secondary_failure`), and **does not block the other
  sources or the report**. Collectors are also internally bounded by their
  ccxt/HTTP request timeouts. **No fabricated data**; degraded summaries carry an
  explicit `failed={"__exchange__": …}` marker that flows to `last_update.json`.
- **Graceful anchor degradation:** if Binance OHLCV fails, the report continues
  on secondary-exchange OHLCV via the existing `_load_market_data` fallback.
- **Diagnostics preserved** + per-source timings still logged.

## 5. Before / after (18 symbols, isolated `scripts/_measure_report_fetch.py`)
| stage | BEFORE (sequential) | AFTER — contended* | **AFTER — clean** |
|---|---|---|---|
| rank_candidates | 311.7 s | 296.9 s | 267.9 s |
| OHLCV block | **137 s** (53+39+45 seq) | ~65 s (parallel) | **52 s** (parallel; max 52/46/42) |
| derivatives block | **370 s** (141+140+89 seq) | ~116 s (parallel) | **125 s** (parallel; max 125/124/81) |
| news | 65 s | 32.5 s | 33.9 s |
| social | ~33 s | 32.8 s | 25.7 s |
| **update_data total** | **~572 s** | 245.8 s | **236.8 s** |
| **fetch total (rank+update)** | **~883 s** | 542.8 s | **504.7 s** |

Clean run = no live scheduler crypto report active (waited for idle). OHLCV
**137 s → 52 s (2.6×)**, derivatives **370 s → 125 s (2.96×)**, update_data
**~572 s → 237 s (~59% faster)**. All 6 sources logged OK, **no degradation**.

*Contended = overlapped a live scheduler scalp run (old sequential code) hitting
the same exchanges, so it is a **conservative** (worse-than-real) "after". The
parallel waves are still clearly visible (all 3 OHLCV start at the same instant;
all 3 derivatives start at the same instant).

**`update_data` dropped ~572 s → ~246 s even contended** (~57% faster). The
symbol-scaling blocks (OHLCV + derivatives) — which are what push the report over
the wall at the ~48-symbol production size — shrink from ~507 s to ~181 s for 18
symbols, i.e. from sum-of-sources to max-of-sources.

## 6. Production projection (~48 symbols)
- Before: rank 312 + OHLCV ~365 + deriv ~985 + news/social ~125 + analysis ~700
  ≈ **2400–2600 s** (against 2700 s wall — the timeout source).
- After: rank ~300 + OHLCV ~**150** + deriv ~**260** + news/social ~125 +
  analysis ~700 ≈ **~1550 s** → **comfortable ~1150 s margin** under the wall.

## 7. Tests run
- `tests/test_parallel_fetch.py` — **6 passed** (all sources invoked; success
  populates; one failure degrades only that source; concurrency faster than
  sequential; slow source times out & degrades; per-source timings logged).
- Core regression subset (`test_supervisor_smoke`, `test_supervisor_routing`,
  `test_universe_collector`, `test_relative_strength_gate`,
  `test_crypto_alert_registration`, `test_parallel_fetch`) — **49 passed**.

## 8. No strategy/scoring change — confirmation
The change is confined to fetch scheduling in `update_data` + a helper. Scoring,
tiering, thresholds, stop/TP, signal logic, and report content are untouched
(unchanged files). Verified by the registration/routing/scoring regression
subset passing unchanged.

## 9. Remaining risks
- `rank_candidates` (~300 s fixed) is still sequential per-exchange — secondary
  optimization opportunity (not done; would need its own review).
- ThreadPoolExecutor `shutdown(wait=True)` waits for in-flight threads; safe
  because collectors are internally HTTP-timeout-bounded (no infinite hang
  observed in diagnostics).
- Concurrency rate-limit risk mitigated (bounded, cross-host); monitor first
  live cycles for 429s.

## 10. Scheduler deployment status
**Not deployed yet.** The running scheduler (PID from 11:08 boot) still executes
the old sequential code. Deployment (restart) is pending clean verification —
see `POST_CRYPTO_TIMEOUT_FIX_VERIFICATION.md`.
