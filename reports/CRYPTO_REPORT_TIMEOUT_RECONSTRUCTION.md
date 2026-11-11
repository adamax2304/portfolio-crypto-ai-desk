# Crypto Report Timeout — Event Reconstruction (PART 1)

**Window:** 2026-06-05 20:00 → 06-07 19:12 (last ~48h of scheduler.log).
Timeout wall: `timeout=2700s` (45 min) per crypto scalp/intraday report.

## Event table (crypto scalp + intraday only)
| date/time (EEST) | command | elapsed | result | note |
|---|---|---|---|---|
| 06-05 20:04 | scalp | 409s | **exit=1** | fast fail — network (during my 22:00 restart window) |
| 06-05 20:04 | intraday | 50s | exit=1 | fast fail — network |
| 06-05 22:18 | scalp | 607s | exit=1 | fast fail — network |
| 06-05 23:03 | intraday | ~2700s | **TIMEOUT** | |
| 06-06 02:07 | scalp | ~2700s | **TIMEOUT** | overnight |
| 06-06 02:52 | intraday | ~2700s | **TIMEOUT** | overnight |
| 06-06 05:39 | scalp | **2368s** | exit=0 | completed (9.5 min under wall) |
| 06-06 06:24 | intraday | ~2700s | **TIMEOUT** | |
| 06-06 10:38 | scalp | ~2700s | **TIMEOUT** | |
| 06-06 11:24 | intraday | ~2700s | **TIMEOUT** | |
| 06-06 16:19 | scalp | ~2700s | **TIMEOUT** | |
| 06-06 17:04 | intraday | ~2700s | **TIMEOUT** | |
| 06-06 20:32 | scalp | ~2700s | **TIMEOUT** | |
| 06-06 21:13 | intraday | **2447s** | exit=0 | completed (4 min under wall) |
| 06-06 23:54 | scalp | **2343s** | exit=0 | completed |
| 06-07 00:38 | intraday | **2622s** | exit=0 | completed (**1.3 min under wall**) |
| 06-07 03:20 | scalp | **2471s** | exit=0 | completed |
| 06-07 04:01 | intraday | **2433s** | exit=0 | completed |
| 06-07 06:47 | scalp | ~2700s | **TIMEOUT** | |
| 06-07 07:32 | intraday | ~2700s | **TIMEOUT** | |
| 06-07 10:19 | scalp | ~2700s | **TIMEOUT** | |
| 06-07 11:04 | intraday | ~2700s | **TIMEOUT** | |
| 06-07 11:54 | scalp | ~2700s | **TIMEOUT** | |
| 06-07 12:36 | intraday | **2501s** | exit=0 | completed |
| 06-07 15:15 | scalp | **2269s** | exit=0 | completed |
| 06-07 15:48 | intraday | **1953s** | exit=0 | completed (fastest) |
| 06-07 18:30 | scalp | **2273s** | exit=0 | completed |
| 06-07 19:12 | intraday | **2488s** | exit=0 | completed |

## The key finding
**Successful runs complete in 1953–2622 s (33–44 min).** The timeout wall is
2700 s (45 min). So the report **legitimately runs for ~40 min** with a margin of
**only ~1–9 minutes** under the wall. Normal run-to-run variance (network
latency, more symbols passing the funnel in active markets) **intermittently
pushes a run past 45 min → TIMEOUT.** This is **not a hang** — it is a workload
that sits a few minutes under its own kill-timeout.

Evidence: 06-07 00:38 intraday completed at **2622 s** — only **78 s** under the
wall. A run that is 2% slower times out. ~50% of recent runs cross it.

## Two distinct failure modes
1. **TIMEOUT (~2700 s)** — dominant. Workload ≈ kill-timeout (see above).
2. **Fast exit=1 (50–607 s)** — only on 06-05 around the manual restart =
   transient **network** errors (urllib3 connection). Not seen since; not the
   recurring issue.

## Daytime vs overnight
Weak-to-moderate correlation: more *completions* cluster overnight/off-peak
(03:20, 04:01, 15:48) and more *timeouts* in active hours — consistent with
"more symbols / slower endpoints under load," but several overnight runs also
timed out (06-06 02:07/02:52) and several daytime runs completed (15:15, 18:30).
→ It is **variance around a mean that sits just under the wall**, not a clean
time-of-day switch.

## Post-timeout behavior
- **Non-fatal:** on timeout the step is logged `CMD TIMEOUT` and the **cycle
  continues** — stocks step, monitors, tracking, dashboard all still run
  (`CYCLE END ok=9–11 failed=1–2`).
- **Recovers next cycle:** every following cycle ran; several were fully clean
  (`failed=0`: 06-07 00:38, 04:01, 15:51, 19:12).
- **No SQLite locks, no DLL errors, no stale/hung cycles** tied to these
  timeouts.

## Why the stage is invisible in scheduler.log
The scheduler captures the report's stdout and only logs a tail on completion;
on timeout it logs `(timeout)`. There is **no per-stage timing** in the existing
logs — which is exactly the gap PART 2 instrumentation fills.

## Hypothesis carried into PART 2/3
The ~40-min cost is dominated by **`update_data`** — which fetches OHLCV
**sequentially** across Binance → Bybit → MEXC, then Binance/multi/Bybit
derivatives, then news + social (see `supervisor.update_data`). The code comment
claims these are "fetched in parallel" but the implementation is a sequential
loop. Confirmed/quantified by the stage timer in
`CRYPTO_REPORT_TIMEOUT_DIAGNOSTIC_REPORT.md`.
