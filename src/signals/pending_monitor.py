"""Fast pending-only entry monitor (crypto) + leader election (2026-07-05).

A lightweight loop that ONLY runs the existing A/B pending-entry tracker (`track_pending_entries`) at
a 30-60s cadence — it refreshes OHLCV for *pending* symbols and detects entry-touch, then lets the
tracker fire the (idempotent, dedup'd) paper-entry alert. It deliberately does NOT run
`re_evaluate()` / scoring / news / LLM / report generation, so a tick is cheap enough to run every
~45s instead of the 300-600s `monitor-watchlist` cadence.

Safety:
  * paper/shadow only — never places an order, never changes score/tier/actionability/TP/SL/sizing;
  * reuses `track_pending_entries` → same status gates + alert dedup (can't double-fire vs the full
    pass or a concurrent `monitor-watchlist`);
  * LEADER ELECTION: only one pending monitor per asset_class runs; a second process detects a fresh
    leader lock and exits/skips (no destructive kills);
  * fail-open on data-fetch errors / 429 (backoff, never crash the scheduler), with a latency
    warning emitted to telemetry.
"""
from __future__ import annotations

import json
import os
import shutil
import threading
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from src.signals import latency_telemetry as tel

_LEADER_DIRNAME = ".locks"


def _write_runtime_heartbeat(
    root: Path,
    *,
    worker_id: str,
    tick: int,
    stage: str,
) -> None:
    """Persist a tiny operational heartbeat for the dedicated fast worker.

    The leader lease is intentionally released when a worker stops and should
    not be the only liveness signal.  This file lets the independent watchdog
    distinguish a healthy long-running tick from a process that merely exists.
    """
    try:
        path = Path(root) / "data" / "runtime_locks" / "pending_monitor.heartbeat.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "pid": os.getpid(),
            "worker_id": worker_id,
            "tick": int(tick),
            "stage": stage,
            "at": datetime.now(timezone.utc).isoformat(),
        }
        path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
    except Exception:
        # A diagnostic marker must never take down the latency-critical loop.
        return


def disk_space_status(root: Path, *, warning_free_mb: int = 5120,
                      critical_free_mb: int = 1024) -> dict:
    """Return a conservative local-disk status for the pending-data cache.

    Failure to inspect disk space is deliberately ``unknown`` rather than a
    trading block. A confirmed critical threshold blocks this tick so the
    tracker cannot act on a cache that might be stale or partially written.
    """
    try:
        free_bytes = shutil.disk_usage(root).free
        free_mb = round(free_bytes / (1024 * 1024), 1)
        if free_mb < max(0, float(critical_free_mb)):
            state = "critical"
        elif free_mb < max(0, float(warning_free_mb)):
            state = "warning"
        else:
            state = "ok"
        return {"state": state, "free_mb": free_mb,
                "warning_free_mb": int(warning_free_mb),
                "critical_free_mb": int(critical_free_mb)}
    except OSError as exc:
        return {"state": "unknown", "error": type(exc).__name__}


def _leader_path(root: Path, asset_class: str) -> Path:
    d = Path(root) / _LEADER_DIRNAME
    try:
        d.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    return d / f"pending_monitor_leader_{asset_class}.lock"


def leader_status(root: Path, asset_class: str, *, ttl_sec: float, now: float | None = None) -> dict:
    """Report whether a FRESH leader lock (mtime within ttl) exists. Read-only."""
    now = now if now is not None else time.time()
    p = _leader_path(root, asset_class)
    try:
        if not p.exists():
            return {"active": False, "path": str(p)}
        age = now - p.stat().st_mtime
        info = {"age_sec": round(age, 1), "path": str(p)}
        try:
            info["holder"] = p.read_text(encoding="utf-8").strip()[:120]
        except Exception:
            pass
        info["active"] = age <= ttl_sec
        info["stale"] = age > ttl_sec
        return info
    except Exception:
        return {"active": False, "path": str(p)}


@contextmanager
def leader_lock(root: Path, asset_class: str, *, worker_id: str, ttl_sec: float):
    """Acquire per-asset_class leadership. Yields a `heartbeat()` callable on success, or None if a
    fresh leader already holds it (caller must exit). Steals only a STALE (ttl-expired) lock. No
    destructive process kills — a second process simply declines."""
    p = _leader_path(root, asset_class)
    st = leader_status(root, asset_class, ttl_sec=ttl_sec)
    if st.get("active"):
        yield None
        return
    # Atomically create/steal the lease. The former check-then-write sequence
    # let two processes both observe a missing file and become leaders.
    if p.exists():
        current = leader_status(root, asset_class, ttl_sec=ttl_sec)
        if current.get("active"):
            yield None
            return
        try:
            p.unlink()  # re-check above proved this lease stale
        except Exception:
            yield None
            return
    try:
        fd = os.open(str(p), os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        try:
            os.write(fd, f"{os.getpid()} {worker_id} {datetime.now(timezone.utc).isoformat()}".encode("utf-8"))
        finally:
            os.close(fd)
    except FileExistsError:
        yield None
        return
    except Exception:
        # if we cannot even write the lock, run without leadership (single-process case)
        yield lambda: None
        return

    def _heartbeat() -> None:
        try:
            p.write_text(f"{os.getpid()} {worker_id} {datetime.now(timezone.utc).isoformat()}",
                         encoding="utf-8")
        except Exception:
            pass

    try:
        yield _heartbeat
    finally:
        try:
            # only remove if it's still ours
            cur = p.read_text(encoding="utf-8")
            if str(os.getpid()) in cur.split()[:1]:
                p.unlink()
        except Exception:
            pass


def needed_timeframes(db: Any, configured: list[str]) -> list[str]:
    """The minimal timeframe set the tracker will ACTUALLY consult for the crypto A/B pending modes
    present — the union of ``TIMEFRAME_PREFERENCE[mode]`` intersected with the configured set. This
    provably does not change detection: every timeframe a present mode could pick is still fetched;
    only timeframes NO present mode uses (e.g. 1m — absent from every crypto preference) are dropped.
    """
    try:
        from src.signals.tracker import TIMEFRAME_PREFERENCE
        modes: set[str] = set()
        for r in db.load_active_signals():
            if (str(r.get("tier") or "").upper() in ("A", "B")
                    and str(r.get("asset_class") or "crypto").lower() == "crypto"):
                mode = str(r.get("mode") or "").lower()
                if mode != "scalp":
                    modes.add(mode)
        want: set[str] = set()
        for m in modes:
            want.update(TIMEFRAME_PREFERENCE.get(m, TIMEFRAME_PREFERENCE["intraday"]))
        # 15m remains the canonical structural timeframe.  A fresh 1m frame is
        # additionally required to prove a crypto-intraday Paper entry was
        # executable at the decision time rather than only visible in history.
        if "intraday" in modes and "1m" in configured:
            want.add("1m")
        # Swing still executes on its canonical higher timeframe.  Keep a
        # 5m probe only to resolve the first touch inside the active 1h bar
        # for latency evidence; it does not change entry/exit logic.
        if "swing" in modes and "5m" in configured:
            want.add("5m")
        out = [tf for tf in configured if tf in want]
        return out or list(configured)
    except Exception:
        return list(configured)


def pending_refresh_requirements(db: Any, configured: list[str]) -> dict[str, tuple[str, ...]]:
    """Minimal fresh-data contract for every active crypto symbol."""
    allowed = set(configured)
    requirements: dict[str, set[str]] = {}
    try:
        for row in db.load_active_signals():
            if str(row.get("asset_class") or "crypto").lower() != "crypto":
                continue
            if str(row.get("tier") or "").upper() not in {"A", "B"}:
                continue
            symbol = str(row.get("symbol") or "").strip().upper()
            if not symbol:
                continue
            mode = str(row.get("mode") or "intraday").lower()
            if mode == "scalp":
                continue
            status = str(row.get("status") or "").lower()
            if mode == "intraday":
                wanted = {"1m"} if status in {"triggered", "tp1_hit", "tp2_hit"} else {"1m", "15m"}
            elif mode == "swing":
                wanted = {"5m", "1h"}
            elif mode == "scalp":
                wanted = {"5m"}
            else:
                from src.signals.tracker import TIMEFRAME_PREFERENCE
                wanted = {TIMEFRAME_PREFERENCE.get(mode, TIMEFRAME_PREFERENCE["intraday"])[0]}
            requirements.setdefault(symbol, set()).update(wanted & allowed)
    except Exception:
        return {}
    return {
        symbol: tuple(tf for tf in configured if tf in wanted)
        for symbol, wanted in requirements.items()
    }


def pending_closed_bar_pairs(db: Any, configured: list[str]) -> set[tuple[str, str]]:
    """Pairs whose intra-bar updates cannot change the pending-entry decision.

    Swing uses 5m only to locate a touch inside its authoritative 1h structure,
    so one refresh per closed 5m bucket is sufficient. Disabled scalp signals
    are not part of this latency-critical refresh contract.
    """
    allowed = set(configured)
    swing_symbols: set[str] = set()
    try:
        for row in db.load_active_signals():
            if str(row.get("asset_class") or "crypto").lower() != "crypto":
                continue
            if str(row.get("tier") or "").upper() not in {"A", "B"}:
                continue
            symbol = str(row.get("symbol") or "").strip().upper()
            mode = str(row.get("mode") or "").lower()
            if not symbol:
                continue
            if mode == "scalp":
                continue
            if mode == "swing":
                swing_symbols.add(symbol)
    except Exception:
        return set()
    if "5m" not in allowed:
        return set()
    return {(symbol, "5m") for symbol in swing_symbols}


def _collector_pairs(summary: Any, tfs: list[str]) -> tuple[set, set]:
    """Parse a CollectionSummary into (fetched_pairs, failed_pairs) as (symbol, timeframe) sets.
    The collector keys pairs as ``"{symbol} {timeframe}"`` (symbols never contain a space); a
    symbol-LEVEL failure key (no trailing timeframe, e.g. "BTW/USDT" not listed) marks all requested
    timeframes for that symbol as failed."""
    tfset = set(tfs)
    fetched: set = set()
    for k in (getattr(summary, "fetched", []) or []):
        sym, _, tf = str(k).rpartition(" ")
        if sym and tf in tfset:
            fetched.add((sym, tf))
    failed: set = set()
    for k in (getattr(summary, "failed", {}) or {}):
        sym, _, tf = str(k).rpartition(" ")
        if sym and tf in tfset:
            failed.add((sym, tf))                       # pair-level failure ("empty response", error)
        else:
            for tf2 in tfs:                             # symbol-level failure → every tf failed
                failed.add((str(k), tf2))
    return fetched, failed


def _default_refresh(config: Any, file_store: Any, symbols: list[str], tfs: list[str], *,
                     concurrency: int, cache: dict, ttl_sec: float, mono: float,
                     requirements: dict[str, tuple[str, ...]] | None = None,
                     closed_bar_pairs: set[tuple[str, str]] | None = None) -> dict:
    """Bounded-concurrency OHLCV refresh reusing the TESTED BinanceOHLCVCollector per chunk (one
    ccxt exchange + one load_markets per chunk → thread-isolated; distinct per-symbol file writes).

    Per-(symbol,tf) TTL cache skips ONLY pairs that were SUCCESSFULLY fetched within the TTL — a
    failed pair is never cached, so it is retried on the next tick. Per-chunk fail-open (a raising
    chunk marks all its pairs failed and the tick continues). Returns attempted/succeeded/failed
    counts at both symbol and pair granularity — it never changes candle data or which symbols the
    tracker later reads from cache."""
    from concurrent.futures import ThreadPoolExecutor
    req = {
        str(s).strip().upper(): tuple((requirements or {}).get(str(s).strip().upper()) or tfs)
        for s in symbols
    }
    bar_seconds = {"5m": 5 * 60, "15m": 15 * 60, "1h": 60 * 60}
    closed_only = closed_bar_pairs or set()

    def _pair_is_fresh(symbol: str, timeframe: str) -> bool:
        structural = timeframe in {"15m", "1h"} or (symbol, timeframe) in closed_only
        if structural and timeframe in bar_seconds:
            bucket = int(time.time() // bar_seconds[timeframe])
            if cache.get(("_closed_bar_bucket", symbol, timeframe)) == bucket:
                return True
        return ((symbol, timeframe) in cache
                and (mono - cache[(symbol, timeframe)]) < ttl_sec)

    fresh, stale = [], []
    fetch_req: dict[str, tuple[str, ...]] = {}
    for s in symbols:
        needed = req[str(s).strip().upper()]
        missing = tuple(tf for tf in needed if not _pair_is_fresh(s, tf))
        if needed and not missing:
            fresh.append(s)
        else:
            stale.append(s)
            fetch_req[s] = missing or needed

    fetched_pairs: set = set()
    failed_pairs: set = set()
    fallback_fetched_pairs: set = set()
    conc = max(1, min(int(concurrency), len(stale))) if stale else 0
    if stale:
        grouped: dict[tuple[str, ...], list[str]] = {}
        for symbol in stale:
            grouped.setdefault(fetch_req[symbol], []).append(symbol)

        def _do(item):
            chunk, chunk_tfs = item
            if not chunk:
                return (set(), set())
            try:
                from src.data_collectors.binance_collector import BinanceOHLCVCollector
                res = BinanceOHLCVCollector(config, file_store).fetch(
                    symbols=chunk, timeframes=list(chunk_tfs))
                return _collector_pairs(res, list(chunk_tfs))
            except Exception:
                # per-chunk fail-open — every pair in the chunk is a failure (NOT cached → retried)
                return (set(), {(s, tf) for s in chunk for tf in chunk_tfs})

        jobs: list[tuple[list[str], tuple[str, ...]]] = []
        for group_tfs, group_symbols in grouped.items():
            workers = max(1, min(conc, len(group_symbols)))
            jobs.extend((group_symbols[i::workers], group_tfs) for i in range(workers))

        with ThreadPoolExecutor(max_workers=max(1, min(conc, len(jobs)))) as ex:
            for fp, ep in ex.map(_do, jobs):
                fetched_pairs |= fp
                failed_pairs |= ep
        # Binance is the anchor, not the whole universe. Retry unresolved
        # symbol/timeframe pairs on Bybit and MEXC so a discovery from either
        # venue cannot be monitored from an old fallback CSV. Tests pass
        # config=None and intentionally remain network-free.
        unresolved = {
            (s, tf) for s in stale for tf in fetch_req[s]
        } - fetched_pairs
        if config is not None and unresolved:
            from src.data_collectors.bybit_collector import BybitOHLCVCollector
            from src.data_collectors.mexc_collector import MEXCOHLCVCollector
            for collector_cls in (BybitOHLCVCollector, MEXCOHLCVCollector):
                if not unresolved:
                    break
                fallback_symbols = sorted({s for s, _ in unresolved})
                fallback_tfs = sorted({tf for _, tf in unresolved})
                try:
                    result = collector_cls(config, file_store).fetch(
                        symbols=fallback_symbols, timeframes=fallback_tfs)
                    fp, _ = _collector_pairs(result, fallback_tfs)
                    recovered = fp & unresolved
                    fetched_pairs |= recovered
                    fallback_fetched_pairs |= recovered
                    unresolved -= recovered
                except Exception:
                    continue
            failed_pairs = unresolved
        # CACHE ONLY SUCCESSFUL PAIRS — failed pairs stay uncached so they retry next tick.
        for (s, tf) in fetched_pairs:
            cache[(s, tf)] = mono
            structural = tf in {"15m", "1h"} or (s, tf) in closed_only
            if structural and tf in bar_seconds:
                cache[("_closed_bar_bucket", s, tf)] = int(time.time() // bar_seconds[tf])

    attempted_pairs = sum(len(fetch_req[s]) for s in stale)
    succeeded_syms = {
        s for s in stale
        if all((s, tf) in fetched_pairs for tf in fetch_req[s])
    }
    failed_syms = set(stale) - succeeded_syms           # any missing/failed pair ⇒ symbol not fully OK
    # ``ready_symbols`` is deliberately stricter than "attempted".  The
    # tracker must never inspect an old local CSV after one of the required
    # timeframes failed to refresh; that can turn a historical touch into a
    # late, apparently current entry.  Cached pairs count only while inside
    # the per-tick TTL established from a successful fetch.
    ready_symbols = sorted(set(fresh) | succeeded_syms)
    return {
        # attempted/succeeded/failed at symbol + pair granularity
        "refresh_attempted_symbols": len(stale),
        "refresh_succeeded_symbols": len(succeeded_syms),
        "refresh_failed_symbols": len(failed_syms),
        "refresh_attempted_pairs": attempted_pairs,
        "refresh_succeeded_pairs": len(fetched_pairs),
        "refresh_failed_pairs": attempted_pairs - len(fetched_pairs),
        # back-compat aliases (attempted count; failed = failed pairs)
        "refreshed": len(stale), "failed": attempted_pairs - len(fetched_pairs),
        "cache_hits": len(fresh), "cache_misses": len(stale), "concurrency": conc,
        "fallback_fetched_pairs": len(fallback_fetched_pairs),
        "ready_symbols": ready_symbols,
        "requirements": {s: list(req[str(s).strip().upper()]) for s in symbols},
    }


def pending_monitor_tick(
    supervisor: Any,
    *,
    notifier: Any = None,
    tracker_config: Any,
    tick_index: int = 1,
    dry_run: bool = False,
    worker_id: str = "pending-monitor",
    source: str = "pending-monitor",
    max_symbols: int = 60,
    timeframes: list[str] | None = None,
    concurrency: int = 6,
    tracker_db_busy_timeout_ms: int = 1000,
    fetch_ttl_sec: float = 60.0,
    interval_sec: float | None = None,
    warning_free_mb: int = 5120,
    critical_free_mb: int = 1024,
    observe_only: bool = False,
    run_cache: dict | None = None,
    refresh_fn: Callable[..., dict] | None = None,
    log: Callable[[str], None] | None = None,
) -> dict:
    """One fast tick: bounded, CONCURRENT OHLCV refresh of pending crypto symbols → pending-entry
    tracker. Emits latency telemetry with stage timings. Fail-open. Returns a summary dict.

    Optimisations (none change A/B selection, entry/TP/SL/status semantics, or alert gates):
      * fetches the structural tracker timeframes plus 1m while crypto intraday
        candidates are pending, so Paper entries have current-price provenance;
      * per-(symbol,tf) TTL cache dedups WITHIN a tick but is CLAMPED so it can never skip the next
        tick's refresh at the normal interval (freshness first); only successfully-fetched pairs
        are cached, so a failed pair retries next tick;
      * bounded concurrency (`concurrency` workers) over the tested collector, per-chunk fail-open.

    ``observe_only=True`` runs selection + OHLCV refresh + timing metrics ONLY — it does NOT call
    ``track_pending_entries``, so it writes NO outcomes/status and fires NO alerts. (It may still
    record the add-only ``market_data_refreshed`` latency telemetry — it is not fully read-only.)
    """
    import time as _time
    log = log or (lambda m: None)
    timeframes = timeframes or ["1m", "5m", "15m", "1h"]
    cache = run_cache if run_cache is not None else {}
    # Clamp the cache TTL so it never spans a full interval — otherwise the next latency-critical
    # tick could reuse stale candles instead of refreshing. Cache stays useful as intra-tick /
    # rapid-iteration dedup; at the normal cadence every tick refetches.
    effective_ttl = float(fetch_ttl_sec)
    if interval_sec and interval_sec > 0:
        effective_ttl = min(effective_ttl, float(interval_sec) / 2.0)
    db = supervisor.db
    t0 = _time.perf_counter()
    summary = {"tick": tick_index, "refreshed": 0, "checked": 0, "tp": 0, "stop": 0, "expired": 0,
               "selected_crypto": 0, "selected_stocks": 0, "skipped_non_crypto": 0,
               "symbols_refreshed": 0, "fetch_errors": 0, "cache_hits": 0, "cache_misses": 0,
               "concurrency": 0, "timeframes": [], "observe_only": observe_only,
               "refresh_attempted_symbols": 0, "refresh_succeeded_symbols": 0,
               "refresh_failed_symbols": 0, "refresh_attempted_pairs": 0,
               "refresh_succeeded_pairs": 0, "refresh_failed_pairs": 0,
               "fallback_fetched_pairs": 0, "effective_ttl_sec": effective_ttl,
               "selection_ms": 0, "fetch_ms": 0, "track_ms": 0, "total_ms": 0, "errors": [],
               "tracker_retries": 0,
               "disk_status": "unknown", "disk_free_mb": None, "data_integrity_blocked": False,
               "tracking_eligible_symbols": 0, "tracking_skipped_stale_symbols": 0}

    # --- selection (crypto-only; counts crypto vs skipped non-crypto) ---
    # The selected crypto ids are SNAPSHOTTED here and handed to the tracker so `selected_crypto`
    # and `checked` come from the same set (no re-select drift inside the tracker).
    ts = _time.perf_counter()
    crypto_ids: list[str] = []
    try:
        from src.signals.tracker import select_pending_ab_signal_ids
        all_ids = select_pending_ab_signal_ids(db)
        crypto_ids = select_pending_ab_signal_ids(db, asset_class="crypto")
        summary["selected_crypto"] = len(crypto_ids)
        summary["selected_stocks"] = summary["skipped_non_crypto"] = len(all_ids) - len(crypto_ids)
        rows_by_id = {
            str(row.get("signal_id") or ""): row for row in db.load_active_signals()
        }
        for signal_id in crypto_ids:
            row = rows_by_id.get(str(signal_id))
            if row:
                tel.emit_discovered(db, row, source=source, worker_id=worker_id)
    except Exception as exc:
        summary["errors"].append(f"select:{type(exc).__name__}")
    summary["selection_ms"] = round((_time.perf_counter() - ts) * 1000, 1)

    # --- bounded OHLCV refresh (crypto-only; mode-specific timeframes) ---
    requirements = pending_refresh_requirements(db, timeframes)
    closed_bar_pairs = pending_closed_bar_pairs(db, timeframes)
    tfs = [tf for tf in timeframes if any(tf in values for values in requirements.values())]
    if not tfs:
        tfs = needed_timeframes(db, timeframes)
    summary["timeframes"] = tfs
    refresh_syms: list[str] = []
    try:
        from src.signals.pending_symbol_universe import pending_symbols
        pend = pending_symbols(db, asset_class="crypto", include_scalp=False)
        if len(pend) > max_symbols:
            # Fresh candidates must never disappear behind an old round-robin
            # backlog. Reserve a sticky head, then rotate the remainder.
            sticky_n = min(20, max(1, max_symbols // 3))
            sticky, tail = pend[:sticky_n], pend[sticky_n:]
            tail_cap = max(0, max_symbols - len(sticky))
            if tail and tail_cap:
                off = ((tick_index - 1) * tail_cap) % len(tail)
                tail = (tail[off:] + tail[:off])[:tail_cap]
            pend = sticky + tail[:tail_cap]
        refresh_syms = pend
    except Exception as exc:
        summary["errors"].append(f"pending_symbols:{type(exc).__name__}")

    tf = _time.perf_counter()
    disk = disk_space_status(Path(supervisor.config.root), warning_free_mb=warning_free_mb,
                             critical_free_mb=critical_free_mb)
    summary["disk_status"] = disk.get("state", "unknown")
    summary["disk_free_mb"] = disk.get("free_mb")
    if disk.get("state") == "warning" and not cache.get("_disk_warning_logged"):
        log("  [pending-monitor] low disk space warning: "
            f"{disk.get('free_mb')}MB free (critical below {disk.get('critical_free_mb')}MB)")
        cache["_disk_warning_logged"] = True
    if disk.get("state") == "critical":
        # A confirmed disk-full condition can produce partial/stale cache data.
        # Skip both refresh and tracking rather than act on that uncertainty.
        summary["data_integrity_blocked"] = True
        summary["errors"].append(f"disk_critical:{disk.get('free_mb')}MB")
        summary["fetch_ms"] = round((_time.perf_counter() - tf) * 1000, 1)
        summary["track_ms"] = 0.0
        summary["total_ms"] = round((_time.perf_counter() - t0) * 1000, 1)
        tel.emit(db, event_type="market_data_refresh_skipped", asset_class="crypto", source=source,
                 worker_id=worker_id,
                 note=(f"disk-critical free_mb={disk.get('free_mb')} "
                       f"threshold_mb={disk.get('critical_free_mb')}; tracker skipped"))
        log("  [pending-monitor] disk critical; refresh/tracker skipped to preserve data integrity")
        return summary
    if refresh_syms and tfs:
        fn = refresh_fn or _default_refresh
        try:
            refresh_kwargs = dict(
                concurrency=concurrency, cache=cache,
                ttl_sec=effective_ttl, mono=tf,
            )
            if refresh_fn is None:
                refresh_kwargs["requirements"] = requirements
                refresh_kwargs["closed_bar_pairs"] = closed_bar_pairs
            r = fn(supervisor.config, supervisor.file_store, refresh_syms, tfs,
                   **refresh_kwargs)
            att = int(r.get("refresh_attempted_symbols", r.get("refreshed", 0)))
            suc = int(r.get("refresh_succeeded_symbols", 0))
            fpairs = int(r.get("refresh_failed_pairs", r.get("failed", 0)))
            summary["refresh_attempted_symbols"] = att
            summary["refresh_succeeded_symbols"] = suc
            summary["refresh_failed_symbols"] = int(r.get("refresh_failed_symbols", att - suc))
            summary["refresh_attempted_pairs"] = int(r.get("refresh_attempted_pairs", att * len(tfs)))
            summary["refresh_succeeded_pairs"] = int(r.get("refresh_succeeded_pairs", 0))
            summary["refresh_failed_pairs"] = fpairs
            summary["fallback_fetched_pairs"] = int(r.get("fallback_fetched_pairs", 0))
            summary["refreshed"] = summary["symbols_refreshed"] = att   # back-compat alias = attempted
            summary["fetch_errors"] = fpairs
            summary["cache_hits"] = int(r.get("cache_hits", 0))
            summary["cache_misses"] = int(r.get("cache_misses", 0))
            summary["concurrency"] = int(r.get("concurrency", 0))
            if summary["refresh_failed_pairs"]:
                summary["errors"].append(f"ohlcv_failed_pairs:{summary['refresh_failed_pairs']}")
        except Exception as exc:   # whole-refresh fail-open (never blocks the tick)
            summary["errors"].append(f"ohlcv:{type(exc).__name__}")
            log(f"  [pending-monitor] ohlcv refresh failed (fail-open): {type(exc).__name__}")
    summary["fetch_ms"] = round((_time.perf_counter() - tf) * 1000, 1)
    tel.emit(db, event_type="market_data_refreshed", asset_class="crypto", source=source,
             worker_id=worker_id, market_data_age_sec=None,
             note=(f"refresh attempted={summary['refresh_attempted_symbols']} "
                   f"succeeded={summary['refresh_succeeded_symbols']} "
                   f"failed={summary['refresh_failed_symbols']} "
                   f"pairs={summary['refresh_succeeded_pairs']}/{summary['refresh_attempted_pairs']} "
                   f"fallback_pairs={summary['fallback_fetched_pairs']} "
                   f"tfs={','.join(tfs)} conc={summary['concurrency']} fetch_ms={summary['fetch_ms']} "
                   f"cache_hits={summary['cache_hits']}"))

    # --- lightweight pending-entry tracker (crypto-ONLY; idempotent alerts; unchanged semantics) ---
    # observe_only skips it entirely: no track_pending_entries → no outcome/status writes, no alerts.
    tk = _time.perf_counter()
    if observe_only:
        summary["track_ms"] = round((_time.perf_counter() - tk) * 1000, 1)
        summary["total_ms"] = round((_time.perf_counter() - t0) * 1000, 1)
        return summary
    original_busy_timeout = getattr(db, "busy_timeout_ms", None)
    pe_notifier = notifier if (notifier is not None and getattr(notifier, "enabled", False)
                               and getattr(notifier, "chat_id", None)) else None
    if original_busy_timeout is not None:
        # The latency-critical monitor uses a short SQLite timeout and retries
        # next tick instead of sitting behind an unrelated analytics writer.
        db.busy_timeout_ms = max(0, int(tracker_db_busy_timeout_ms))
    try:
        from src.signals.tracker import track_pending_entries
        # Only data confirmed fresh in this tick (or in its bounded successful
        # cache) may create an entry/exit transition.  A custom refresh helper
        # without the new field remains compatible only when it reports no
        # failed pairs; otherwise we fail closed for this one tick.
        ready_symbols_raw = r.get("ready_symbols") if "r" in locals() else None
        if ready_symbols_raw is None:
            ready_symbols = (set(refresh_syms)
                             if int(summary.get("refresh_failed_pairs") or 0) == 0 else set())
        else:
            ready_symbols = {str(symbol).strip().upper() for symbol in ready_symbols_raw}
        if not refresh_syms:
            # No symbol refresh was requested (for example an empty pending
            # universe in a test).  Preserve the caller's selected snapshot.
            ready_symbols = None
        selected_rows = {str(row.get("signal_id") or ""): str(row.get("symbol") or "").strip().upper()
                         for row in db.load_active_signals()}
        tracking_ids = (
            crypto_ids if ready_symbols is None else
            [sid for sid in crypto_ids if selected_rows.get(str(sid)) in ready_symbols]
        )
        summary["tracking_eligible_symbols"] = len({selected_rows.get(str(sid)) for sid in tracking_ids})
        summary["tracking_skipped_stale_symbols"] = max(
            0, len({selected_rows.get(str(sid)) for sid in crypto_ids}) - summary["tracking_eligible_symbols"])
        if summary["tracking_skipped_stale_symbols"]:
            tel.emit(db, event_type="pending_tracker_stale_data_blocked", asset_class="crypto",
                     source=source, worker_id=worker_id,
                     note=(f"symbols={summary['tracking_skipped_stale_symbols']}; "
                           f"fresh={summary['tracking_eligible_symbols']}; required_tfs={','.join(tfs)}"))
        def _track_once():
            return track_pending_entries(
                store=db, file_store=supervisor.file_store, project_config=supervisor.config,
                tracker_config=tracker_config, paper_entry_notifier=pe_notifier,
                paper_entry_dry_run=dry_run, asset_class="crypto",
                signal_ids=tracking_ids, telemetry_source=source)

        try:
            res = _track_once()
            if str(getattr(res, "skip_reason", "")) in {
                    "pending_or_full_pass_lock_contended", "writer_lock_contended"}:
                summary["tracker_retries"] = 1
                tel.emit(db, event_type="pending_tracker_lock_retry", asset_class="crypto", source=source,
                         worker_id=worker_id, note=str(res.skip_reason))
                _time.sleep(0.35)
                res = _track_once()
        except Exception as exc:
            if "locked" not in str(exc).lower():
                raise
            # One bounded retry is enough to bridge a short SQLite writer;
            # never let this fast path wait indefinitely behind a scheduler.
            summary["tracker_retries"] = 1
            tel.emit(db, event_type="pending_tracker_db_retry", asset_class="crypto", source=source,
                     worker_id=worker_id, note=f"{type(exc).__name__}: database locked")
            _time.sleep(0.35)
            res = _track_once()
        summary.update({"checked": res.checked, "tp": res.tp_hits, "stop": res.stopped,
                        "expired": res.expired})
        tel.emit(db, event_type="pending_tracker_seen", asset_class="crypto", mode=None,
                 source=source, worker_id=worker_id, note=f"checked {res.checked}")
    except Exception as exc:
        summary["errors"].append(f"tracker:{type(exc).__name__}")
        if "locked" in str(exc).lower():
            tel.emit(db, event_type="pending_tracker_db_locked", asset_class="crypto", source=source,
                     worker_id=worker_id, note=f"{type(exc).__name__}: {exc}")
        log(f"  [pending-monitor] tracker skipped (fail-open): {type(exc).__name__}: {exc}")
    finally:
        if original_busy_timeout is not None:
            db.busy_timeout_ms = original_busy_timeout
    if pe_notifier is not None and not dry_run:
        try:
            from src.notifiers.telegram_outbox import retry_pending
            summary["telegram_outbox"] = retry_pending(db, pe_notifier, limit=10)
        except Exception as exc:
            summary["errors"].append(f"telegram_outbox:{type(exc).__name__}")
    summary["track_ms"] = round((_time.perf_counter() - tk) * 1000, 1)
    summary["total_ms"] = round((_time.perf_counter() - t0) * 1000, 1)
    return summary


def run_pending_monitor(
    supervisor: Any,
    *,
    notifier: Any = None,
    interval_sec: int = 45,
    iterations: int = 0,
    duration_hours: float = 0.0,
    dry_run: bool = False,
    worker_id: str | None = None,
    asset_class: str = "crypto",
    leader_ttl_sec: float = 180.0,
    max_symbols: int = 60,
    timeframes: list[str] | None = None,
    concurrency: int = 6,
    tracker_db_busy_timeout_ms: int = 1000,
    fetch_ttl_sec: float = 60.0,
    warning_free_mb: int = 5120,
    critical_free_mb: int = 1024,
    observe_only: bool = False,
    backoff_sec: int = 30,
    max_consecutive_failures: int = 5,
    max_tick_seconds: float = 240.0,
    recycle_after_ticks: int = 0,
    log: Callable[[str], None] | None = None,
    sleep: Callable[[float], None] | None = None,
) -> dict:
    """Run the fast pending loop under a per-asset_class leader lock. If another fresh leader holds
    it, return immediately with skipped=True (the second process does NOT run in parallel)."""
    log = log or (lambda m: None)
    sleep = sleep or time.sleep
    worker_id = worker_id or f"pending-{os.getpid()}"
    try:
        from src.signals.config import load_signal_tracking_config
        tracker_config = load_signal_tracking_config(supervisor.config.root)
    except Exception as exc:
        return {"skipped": True, "reason": f"tracker config load failed: {exc}"}
    if not getattr(tracker_config, "enabled", True):
        return {"skipped": True, "reason": "signal tracking disabled in config"}

    root = supervisor.config.root
    with leader_lock(root, asset_class, worker_id=worker_id, ttl_sec=leader_ttl_sec) as heartbeat:
        if heartbeat is None:
            st = leader_status(root, asset_class, ttl_sec=leader_ttl_sec)
            log(f"[pending-monitor] another leader active ({st.get('holder')}); exiting (no parallel run).")
            return {"skipped": True, "reason": "leader_active", "leader": st}
        start = time.time()
        last_tick_started: float | None = None
        ticks = 0
        consecutive_fail = 0
        totals = {"ticks": 0, "checked": 0, "tp": 0, "stop": 0, "refreshed": 0}
        run_cache: dict = {}   # per-run (symbol,tf) TTL cache shared across ticks
        while True:
            ticks += 1
            tick_started = time.time()
            if last_tick_started is not None:
                gap = tick_started - last_tick_started
                if gap > max(float(interval_sec) * 4.0, 120.0):
                    tel.emit(supervisor.db, event_type="pending_monitor_tick_gap",
                             asset_class="crypto", source="pending-monitor", worker_id=worker_id,
                             note=f"tick_gap_sec={gap:.1f}; interval_sec={interval_sec}")
                    log(f"[pending-monitor] SLA warning: tick gap {gap:.1f}s")
            last_tick_started = tick_started
            heartbeat()  # refresh leadership TTL each tick
            _write_runtime_heartbeat(
                root, worker_id=worker_id, tick=ticks, stage="tick_started",
            )
            def abort_stuck_tick() -> None:
                _write_runtime_heartbeat(
                    root, worker_id=worker_id, tick=ticks, stage="tick_timeout",
                )
                log(
                    f"[pending-monitor] tick {ticks} exceeded "
                    f"{max_tick_seconds:.0f}s; terminating for watchdog replacement"
                )
                # Network/ccxt calls cannot be cancelled safely from another
                # Python thread. Exit only this isolated monitor process; the
                # independent heartbeat task replaces it under the leader lock.
                os._exit(4)

            tick_timer = threading.Timer(max(1.0, float(max_tick_seconds)), abort_stuck_tick)
            tick_timer.daemon = True
            tick_timer.start()
            try:
                s = pending_monitor_tick(
                    supervisor, notifier=notifier, tracker_config=tracker_config, tick_index=ticks,
                    dry_run=dry_run, worker_id=worker_id, source="pending-monitor",
                    max_symbols=max_symbols, timeframes=timeframes, concurrency=concurrency,
                    tracker_db_busy_timeout_ms=tracker_db_busy_timeout_ms,
                    fetch_ttl_sec=fetch_ttl_sec, interval_sec=interval_sec,
                    warning_free_mb=warning_free_mb, critical_free_mb=critical_free_mb,
                    observe_only=observe_only,
                    run_cache=run_cache, log=log)
            finally:
                tick_timer.cancel()
            totals["ticks"] += 1
            for k in ("checked", "tp", "stop", "refreshed"):
                totals[k] += s.get(k, 0)
            _write_runtime_heartbeat(
                root, worker_id=worker_id, tick=ticks, stage="tick_completed",
            )
            # ccxt/pandas collectors create sizeable cyclic object graphs. A
            # long-lived daemon otherwise keeps their arenas resident for days;
            # periodic collection bounds memory without touching data or logic.
            try:
                import gc
                gc.collect()
            except Exception:
                pass
            log(f"[pending-monitor] tick {ticks}: "
                f"{'observe-only · ' if observe_only else ''}crypto-only · "
                f"selected_crypto={s['selected_crypto']} skipped_non_crypto={s['skipped_non_crypto']} · "
                f"refresh attempted={s['refresh_attempted_symbols']} "
                f"succeeded={s['refresh_succeeded_symbols']} failed={s['refresh_failed_symbols']} "
                f"(pairs {s['refresh_succeeded_pairs']}/{s['refresh_attempted_pairs']}) · "
                f"checked={s['checked']} tp={s['tp']} stop={s['stop']} · tfs={','.join(s['timeframes'])} "
                f"conc={s['concurrency']} cache_hits={s['cache_hits']} ttl={s['effective_ttl_sec']}s · "
                f"disk={s['disk_status']}({s['disk_free_mb']}MB) "
                f"selection_ms={s['selection_ms']} fetch_ms={s['fetch_ms']} track_ms={s['track_ms']} "
                f"total_ms={s['total_ms']} retries={s['tracker_retries']}"
                + (f" errors={s['errors']}" if s["errors"] else ""))
            # backoff if the data path is failing (fail-open; never crash the loop)
            extra = 0
            # A writer-lock collision is expected while the periodic full pass
            # commits. It already had one bounded retry and should be retried
            # at the next normal tick, not delayed by the network-error backoff.
            backoff_errors = [
                error for error in s["errors"]
                if not str(error).startswith("tracker:OperationalError")
            ]
            if backoff_errors:
                consecutive_fail += 1
                extra = backoff_sec if consecutive_fail < max_consecutive_failures else backoff_sec * 3
            else:
                consecutive_fail = 0
            if iterations and ticks >= iterations:
                return {"skipped": False, "totals": totals, "reason": "iterations"}
            if duration_hours and (time.time() - start) >= duration_hours * 3600:
                return {"skipped": False, "totals": totals, "reason": "duration"}
            # Recreating several ccxt market clients on Windows leaves large
            # allocator arenas resident even after every HTTP session and
            # object has been closed.  A bounded worker lifetime releases
            # those arenas at the process boundary.  The CLI replaces this
            # process only after this tick and the leader-lock context have
            # completed, so there is no partially executed tracker pass.
            if (recycle_after_ticks and not iterations and not duration_hours
                    and not dry_run and not observe_only
                    and ticks >= int(recycle_after_ticks)):
                tel.emit(supervisor.db, event_type="pending_monitor_recycle",
                         asset_class=asset_class, source="pending-monitor", worker_id=worker_id,
                         note=f"completed_ticks={ticks}; reason=bounded_worker_memory")
                return {"skipped": False, "totals": totals, "reason": "recycle"}
            try:
                # Fixed-rate cadence: fetch/track work consumes the interval
                # budget instead of being added on top of it.
                work_sec = float(s.get("total_ms") or 0.0) / 1000.0
                sleep(max(0.0, float(interval_sec) - work_sec) + extra)
            except KeyboardInterrupt:
                return {"skipped": False, "totals": totals, "reason": "interrupt"}
