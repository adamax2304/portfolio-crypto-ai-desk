# Post Crypto-Timeout-Fix Verification

**Date:** 2026-06-07 · Verifies the parallel-fetch optimization
(`CRYPTO_REPORT_PARALLEL_FETCH_FIX_REPORT.md`). No strategy/scoring/threshold/
stop-TP/signal changes. No auto-trade. Timeout NOT raised.

## 1. Tests
- `tests/test_parallel_fetch.py` — **6 passed** (all sources invoked; success
  populates; one failure degrades only that source; concurrency < sequential;
  slow source times out & degrades; per-source timings logged).
- Core regression subset (supervisor smoke/routing, universe collector, RS gate,
  crypto alert registration, parallel fetch) — **49 passed**. No scoring/tier
  regression.

## 2. Before / contended / clean measurement (18 symbols, isolated)
| stage | BEFORE seq | AFTER contended* | **AFTER clean** |
|---|---|---|---|
| rank_candidates | 311.7 s | 296.9 s | 267.9 s |
| OHLCV block | 137 s (seq) | ~65 s | **52 s** (2.6×) |
| derivatives block | 370 s (seq) | ~116 s | **125 s** (2.96×) |
| news | 65 s | 32.5 s | 33.9 s |
| social | ~33 s | 32.8 s | 25.7 s |
| **update_data** | **~572 s** | 245.8 s | **236.8 s (~59% faster)** |
| **fetch (rank+update)** | **~883 s** | 542.8 s | **504.7 s** |

*Contended = overlapped a live old-code scheduler scalp run on the same
exchanges → conservative. Clean = ran only after the scheduler went idle. In
both, the diagnostics log shows all 3 OHLCV starting at the same instant and all
3 derivatives starting at the same instant (parallel confirmed).

**Production projection (~48 sym):** before ~2400–2600 s (the timeout source) →
after ~1500 s, a comfortable ~1150 s margin under the 2700 s wall.

## 3. Integrity / safety checks
| check | result |
|---|---|
| SQLite `PRAGMA integrity_check` | **ok** (1209 rows) |
| Cache corruption | none — BTC/ETH 15m readable, 220 rows, fresh `last_ts` |
| All sources present (`last_update.json`) | OHLCV 72 (binance) / bybit 47 (7 fail = symbols not listed, normal) / mexc 72; derivatives 17/18/17; news 15 sources (2 known non-fatal: Reuters 404, SEC 403); social 0 |
| Missing/degraded source reported | yes — degradation path logs `SOURCE_FAIL …` (validated by the 2 unit-test injected failures `ohlcv_bad`, `deriv_hang`); **0 production source failures** this run |
| SQLite write concurrency | none — news + `db.save_symbols` kept on main thread; only network→file fetches run in worker threads |
| Per-source timings in diagnostics | yes — `logs/diagnostics/crypto_report_timing_2026-06-07.log` |

## 4. Controlled report verification (cached, new code)
| command | exit | elapsed | < 2700 s |
|---|---|---|---|
| `scalp-report --no-update --skip-packet` | 0 | **222.9 s** | ✅ |
| `intraday-report --no-update` | 0 | **205.3 s** | ✅ |

- LLM packet refreshed: `llm_analysis_packet.md` mtime 22:10:56 → **22:31:39** ✅
- Untracked crypto alerts: **0** before and after ✅
- New report files written (scalp 22:28, intraday 22:31) ✅
- No auto-trade ✅
- (`scalp-report --no-update` added for parity with `intraday-report`; cached
  path mirrors the same `daily_report` pipeline.)

## 5. Scheduler deployment (PART 6)
- Old scheduler python **PID 13864** (11:08 boot, old sequential code) was
  between cycles; terminated so the autostart `.bat` loop relaunches with the
  optimized code. **Telegram collector NOT restarted.**
- New scheduler python **PID 20328** (born 22:34) — fresh process → loads the
  optimized `supervisor.py`.
- New process booted clean: `CYCLE 1/12 START — 22:34` → `crypto scalp report`
  running under the optimized parallel-fetch path.
- **First optimized live crypto report result:** ✅ **`CMD END: crypto scalp
  report exit=0 1119.2 s`** (18.7 min) — vs the 2700 s wall = **~1581 s margin**,
  down from the pre-fix ~2270–2700 s (timing-out) range. The live diagnostics
  (42 symbols) confirm the parallel signature: the 3 derivatives collectors ran
  **concurrently** — bybit_history 241 s, multi 281 s, binance 371 s → wall
  **371 s** vs ~893 s sequential; `update_data` 576 s total; `daily_report`
  236 s. The scheduler immediately proceeded to the intraday report on the same
  optimized path. **Production timeout resolved.**

## 6. Remaining risks
- `rank_candidates` (~270 s) still sequential per-exchange — future secondary
  optimization (not in scope).
- Concurrency rate-limit risk mitigated (bounded `max_workers=4`, cross-host,
  per-source degrade). Monitor first live cycles for 429s.

## Verdict
```
READY_AFTER_CRYPTO_TIMEOUT_FIX
```
Parallel fetch verified (clean 18-sym: update_data ~572 s → 237 s), all tests +
regressions green, integrity/cache/sources intact, cached reports complete far
under the wall with packet refresh + untracked=0, and the optimized code is
deployed to the running scheduler (new PID 20328). Final live-cycle timing
confirmation appended in §5 once the first post-restart crypto report closes.
