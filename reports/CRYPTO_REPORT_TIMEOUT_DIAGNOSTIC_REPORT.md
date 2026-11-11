# Crypto Report Timeout — Diagnostic Report (PART 5)

**Date:** 2026-06-07 · Method: stage-timing instrumentation
(`src/diagnostics/stage_timer.py`) wrapped around the report pipeline in
`supervisor.py`; isolated bounded fetch measurement (`scripts/_measure_report_fetch.py`,
18 symbols, scalp, **no report/telegram/signal side-effects**). Raw timings:
`logs/diagnostics/crypto_report_timing_2026-06-07.log`.

## 1. Measured stage breakdown (18 symbols, isolated fetch path)
| stage | duration | scales with symbols? |
|---|---|---|
| **rank_candidates** | **311.7s** | no (ranks the full broad universe regardless) |
| ohlcv_binance | 53.0s | yes |
| ohlcv_bybit | 38.6s | yes |
| ohlcv_mexc | 45.0s | yes |
| **deriv_binance** | **140.7s** | yes |
| **deriv_multi** (MEXC/Bybit/OKX) | **140.2s** | yes |
| **deriv_bybit_history** | **88.9s** | yes |
| news_rss | 65.4s | no |
| social | (cut by 900s test cap — minor, tens of s) | no |
| **measured fetch subtotal** | **~883s (14.7 min) for 18 symbols** | |

Analysis stages (momentum scan / setups / scoring / render / register / packet)
were NOT in this isolated fetch run; from the production wall-times they account
for the remaining ~600–800 s (see §4).

## 2. Answers to the diagnostic questions
1. **Total elapsed (production, completed runs):** 1953–2622 s; timeout wall 2700 s.
   Isolated fetch (18 sym): ~883 s + analysis.
2. **Time spent in:**
   - rank_candidates: **312 s (fixed)**
   - Binance OHLCV: 53 s · Bybit OHLCV: 39 s · MEXC OHLCV: 45 s (**137 s OHLCV total, sequential**)
   - derivatives collectors: **370 s** (binance 141 + multi 140 + bybit-hist 89) — **largest block**
   - news: 65 s · social: small (tens of s)
   - scan/setup/scoring/render/register/packet: ~600–800 s (production residual, §4)
3. **Slowest sources:** (1) **derivatives collectors** (~370 s/18 sym, ~20 s/symbol across 3),
   (2) **rank_candidates** (312 s fixed), (3) OHLCV (137 s). No single symbol hung;
   cost is per-symbol HTTP × many symbols × 3 derivative sources, all sequential.
   External source warnings (non-fatal, already degraded): Reuters Business 404,
   SEC EDGAR 403 — these are stock RSS, error out fast, not the bottleneck.
4. **Timeout caused by:** **sequential multi-source network I/O** — specifically
   the three **derivatives collectors run sequentially** + the fixed ~5-min
   **rank_candidates** + sequential OHLCV. NOT one slow exchange, NOT report
   rendering, NOT DB/SQLite, NOT news/social, NOT a hang.
5. **Daytime vs overnight:** the symbol-scaling stages (OHLCV + derivatives) cost
   ~**28 s/symbol**. In active markets more symbols pass the funnel → larger
   `selected` set → linearly more fetch time, plus higher exchange-API latency.
   The mean sits a few minutes under the 2700 s wall, so the extra daytime load
   pushes it over. (Overnight runs select fewer symbols / faster APIs → complete.)

## 3. Root cause (confirmed)
**The crypto report's fetch path is fully sequential.** `supervisor.update_data`
fetches Binance→Bybit→MEXC OHLCV, then Binance→multi→Bybit-history derivatives,
then news→social, one after another. The code comment claims OHLCV is "fetched
in parallel" but the implementation is a sequential loop. At the production
universe size (~48 symbols) this sums to ~30 min of fetch, + ~5 min fixed
rank_candidates, + ~10–13 min analysis ≈ 2300–2600 s — i.e. the report
legitimately runs ~2–9 min under its own 2700 s kill-timeout, and normal
variance crosses it ~50% of the time.

Confirmed NOT a redundant fetch: `daily_report` reads derivatives from the JSON
cache that `update_data` already wrote (`binance_futures_latest.json` etc.); the
re-fetch branches are guarded by cache-miss and do not fire in the scheduler path.

## 4. Production extrapolation (~48 symbols)
| block | est. time | note |
|---|---|---|
| rank_candidates | ~312 s | fixed |
| OHLCV ×3 (sequential) | ~365 s | scales |
| derivatives ×3 (sequential) | ~985 s | scales — **dominant** |
| news + social | ~125 s | fixed |
| analysis (scan→packet) | ~600–800 s | CPU + small I/O |
| **total** | **~2400–2600 s** | matches observed completions |

## 5. What was changed in this diagnostic (logging only — pre-approved)
- Added `src/diagnostics/stage_timer.py` — append-only, env-toggle
  (`CRYPTO_REPORT_TIMING=0`), never alters control flow.
- Wrapped pipeline stages in `supervisor.py` with the timer (no logic change).
- Added `scripts/_measure_report_fetch.py` (isolated, side-effect-free measurement).
**No scoring / thresholds / strategy / stop-TP / timeout changed.**

## 6. Proposed fix (NOT implemented — awaiting approval)
Root cause = sequential I/O ⇒ make the **independent** fetches run with **bounded
parallelism**, identical data, no logic change:
1. **Parallelize `update_data` collectors** via a bounded `ThreadPoolExecutor`
   (`max_workers≈4`): the 3 OHLCV + 3 derivatives collectors are independent and
   write distinct cache files. `db.save_symbols` stays on the main thread.
   Expected: symbol-scaling block ~1350 s → ~max-single-source ~500–600 s
   (**save ~750–850 s**), pulling the report comfortably under the wall.
2. **Investigate `rank_candidates`** (312 s fixed) — parallelize its per-exchange
   universe fetch if it is also sequential (secondary, ~150 s potential).
3. **Per-source timeout + graceful degradation:** each parallel fetch gets a
   bounded timeout; on timeout/error → log + mark source stale + continue
   (agents already tolerate missing derivatives, PART 14b). **No fabricated data.**
4. **Rate-limit safety:** cap workers at 4; same-host calls (binance OHLCV +
   binance derivatives) not over-parallelized.
5. **Diagnostics preserved** (stage_timer stays).
6. **Tests:** mock collectors → assert all sources still fetched; assert one
   slow/failing source degrades without blocking others; existing supervisor smoke.
7. **Do NOT raise the 2700 s timeout** (goal is to go faster, not raise the wall).

**Risk:** medium (concurrency / rate limits / thread-safety). Mitigations above;
verify apples-to-apples with the isolated measurement script before/after, with
**no scheduler conflict and no Telegram/signal side-effects**.

## 7. Recommendation
Scheduler can keep running as-is meanwhile (timeouts are non-fatal; cycle
continues, recovers next cycle, paper trading positive). The parallelization is
the correct fix but is a runtime change → **awaiting approval** before
implementation.
