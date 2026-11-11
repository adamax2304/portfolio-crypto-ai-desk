"""Fast pending monitor: leader election + tick telemetry (2026-07-05). No network/live."""
from __future__ import annotations

import time
from pathlib import Path
from unittest.mock import MagicMock

from src.signals import pending_monitor as pm
from src.signals import latency_telemetry as tel


class _Cfg:
    def __init__(self, root):
        self.root = root


class _Sup:
    def __init__(self, db, root):
        self.db = db
        self.file_store = MagicMock()
        self.config = _Cfg(root)


def _store(tmp_path):
    from src.storage.sqlite import SQLiteStore
    st = SQLiteStore(Path(tmp_path) / "t.sqlite")
    st.init_db()
    return st


# ---- leader election ------------------------------------------------------

def test_leader_lock_second_acquire_declines(tmp_path):
    with pm.leader_lock(tmp_path, "crypto", worker_id="w1", ttl_sec=180) as hb1:
        assert hb1 is not None                      # first acquires
        assert pm.leader_status(tmp_path, "crypto", ttl_sec=180)["active"] is True
        with pm.leader_lock(tmp_path, "crypto", worker_id="w2", ttl_sec=180) as hb2:
            assert hb2 is None                       # second declines (no parallel run)
    # released after first exits
    assert pm.leader_status(tmp_path, "crypto", ttl_sec=180).get("active") in (False, None)


def test_leader_lock_steals_stale(tmp_path):
    p = pm._leader_path(tmp_path, "crypto")
    p.write_text("999999 old 2020-01-01T00:00:00+00:00", encoding="utf-8")
    old = time.time() - 10_000
    import os
    os.utime(p, (old, old))                          # make it stale
    assert pm.leader_status(tmp_path, "crypto", ttl_sec=180)["active"] is False
    with pm.leader_lock(tmp_path, "crypto", worker_id="w1", ttl_sec=180) as hb:
        assert hb is not None                         # stale lock stolen


def test_run_pending_monitor_skips_when_leader_active(tmp_path, monkeypatch):
    # a fresh leader lock exists → run must skip without ticking
    p = pm._leader_path(tmp_path, "crypto")
    p.write_text("111 other now", encoding="utf-8")   # fresh mtime
    st = _store(tmp_path)
    monkeypatch.setattr("src.signals.config.load_signal_tracking_config",
                        lambda root: type("C", (), {"enabled": True})())
    res = pm.run_pending_monitor(_Sup(st, tmp_path), interval_sec=1, iterations=1,
                                 sleep=lambda s: None)
    assert res["skipped"] is True and res["reason"] == "leader_active"


def test_run_pending_monitor_requests_recycle_only_after_complete_ticks(tmp_path, monkeypatch):
    st = _store(tmp_path)
    sup = _Sup(st, tmp_path)
    monkeypatch.setattr("src.signals.config.load_signal_tracking_config",
                        lambda root: type("C", (), {"enabled": True})())
    calls = []

    def _tick(*_args, tick_index, **_kwargs):
        calls.append(tick_index)
        return {"checked": 1, "tp": 0, "stop": 0, "refreshed": 1, "errors": [],
                "selected_crypto": 1, "skipped_non_crypto": 0,
                "refresh_attempted_symbols": 1, "refresh_succeeded_symbols": 1,
                "refresh_failed_symbols": 0, "refresh_succeeded_pairs": 1,
                "refresh_attempted_pairs": 1, "timeframes": ["15m"], "concurrency": 1,
                "cache_hits": 0, "effective_ttl_sec": 1, "disk_status": "ok",
                "disk_free_mb": 10000, "selection_ms": 1, "fetch_ms": 1,
                "track_ms": 1, "total_ms": 3, "tracker_retries": 0}

    monkeypatch.setattr(pm, "pending_monitor_tick", _tick)
    res = pm.run_pending_monitor(
        sup, interval_sec=1, recycle_after_ticks=2, sleep=lambda _seconds: None)

    assert calls == [1, 2]
    assert res["reason"] == "recycle"
    assert res["totals"]["ticks"] == 2
    events = tel.load_events(st)
    assert any(e["event_type"] == "pending_monitor_recycle" for e in events)


def test_pending_monitor_writes_runtime_heartbeat_for_a_completed_tick(tmp_path, monkeypatch):
    st = _store(tmp_path)
    sup = _Sup(st, tmp_path)
    monkeypatch.setattr("src.signals.config.load_signal_tracking_config",
                        lambda root: type("C", (), {"enabled": True})())
    monkeypatch.setattr(
        pm,
        "pending_monitor_tick",
        lambda *_args, **_kwargs: {
            "checked": 0, "tp": 0, "stop": 0, "refreshed": 0, "errors": [],
            "selected_crypto": 0, "skipped_non_crypto": 0,
            "refresh_attempted_symbols": 0, "refresh_succeeded_symbols": 0,
            "refresh_failed_symbols": 0, "refresh_succeeded_pairs": 0,
            "refresh_attempted_pairs": 0, "timeframes": [], "concurrency": 0,
            "cache_hits": 0, "effective_ttl_sec": 1, "disk_status": "ok",
            "disk_free_mb": 10000, "selection_ms": 1, "fetch_ms": 1,
            "track_ms": 1, "total_ms": 3, "tracker_retries": 0,
        },
    )

    pm.run_pending_monitor(sup, interval_sec=1, iterations=1, sleep=lambda _seconds: None)

    import json
    heartbeat = json.loads((tmp_path / "data" / "runtime_locks" / "pending_monitor.heartbeat.json").read_text())
    assert heartbeat["tick"] == 1
    assert heartbeat["stage"] == "tick_completed"


# ---- tick telemetry (no A/B pending, no network) --------------------------

def test_pending_monitor_tick_emits_telemetry(tmp_path):
    st = _store(tmp_path)                              # empty → no pending symbols, no fetch
    sup = _Sup(st, tmp_path)
    from src.signals.config import load_signal_tracking_config
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    s = pm.pending_monitor_tick(sup, tracker_config=cfg, tick_index=1, worker_id="w", source="pending-monitor")
    assert s["checked"] == 0                           # nothing pending
    events = tel.load_events(st)
    assert any(e["event_type"] == "pending_tracker_seen" for e in events)


# ---- crypto-only scoping (fix 2) ------------------------------------------

def _insert_signal(st, sid, tier, asset, mode, status="waiting_for_entry"):
    with st.connect() as c:
        c.execute(
            "INSERT INTO proposed_signals(signal_id, created_at, updated_at, symbol, direction, "
            "mode, tier, score, asset_class, status) VALUES(?,?,?,?,?,?,?,?,?,?)",
            (sid, "2026-07-05T10:00:00+00:00", "2026-07-05T10:00:00+00:00", "BTC/USDT", "long",
             mode, tier, 80.0, asset, status))
        c.commit()


def test_select_pending_asset_class_filter(tmp_path):
    from src.signals.tracker import select_pending_ab_signal_ids
    st = _store(tmp_path)
    _insert_signal(st, "c1", "A", "crypto", "intraday")
    _insert_signal(st, "c2", "B", "crypto", "scalp")
    _insert_signal(st, "s1", "A", "stocks", "intraday")   # stocks intraday — must be excluded when crypto-only
    crypto = set(select_pending_ab_signal_ids(st, asset_class="crypto"))
    legacy = set(select_pending_ab_signal_ids(st))         # no filter → old behaviour (both)
    assert crypto == {"c1"}                                # stocks + disabled scalp excluded
    assert legacy == {"c1", "s1"}                          # paused modes stay out globally


def test_pending_monitor_tick_is_crypto_only(tmp_path, monkeypatch):
    st = _store(tmp_path)
    _insert_signal(st, "c1", "A", "crypto", "intraday")
    _insert_signal(st, "s1", "A", "stocks", "intraday")
    _insert_signal(st, "s2", "B", "stocks", "intraday")
    sup = _Sup(st, tmp_path)
    from src.signals.config import load_signal_tracking_config
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    # hermetic: no network refresh, no OHLCV walk — the SELECTION counts are what we assert.
    monkeypatch.setattr("src.signals.pending_symbol_universe.pending_symbols", lambda *a, **k: [])
    monkeypatch.setattr("src.signals.tracker.track_signal", lambda **kw: None)
    # capture what asset_class the pending pass was actually scoped to
    seen = {}
    import src.signals.tracker as tr
    orig = tr.select_pending_ab_signal_ids
    monkeypatch.setattr(tr, "select_pending_ab_signal_ids",
                        lambda store, **kw: seen.update(kw) or orig(store, **kw))
    s = pm.pending_monitor_tick(sup, tracker_config=cfg, tick_index=1, worker_id="w",
                                source="pending-monitor")
    assert s["selected_crypto"] == 1
    assert s["selected_stocks"] == 2 and s["skipped_non_crypto"] == 2
    assert seen.get("asset_class") == "crypto"     # the pending pass was scoped to crypto only


# ---- optimization guardrails (perf without behaviour change) --------------

def test_needed_timeframes_keeps_1m_for_intraday_point_in_time_execution(tmp_path):
    st = _store(tmp_path)
    _insert_signal(st, "c1", "A", "crypto", "intraday")
    cfg_tfs = ["1m", "5m", "15m", "1h"]
    tfs = pm.needed_timeframes(st, cfg_tfs)
    assert "1m" in tfs                                       # required for execution provenance
    assert set(tfs) == {"1m", "15m", "1h"}                  # structural frames + execution probe
    _insert_signal(st, "c2", "B", "crypto", "scalp")
    assert "5m" not in pm.needed_timeframes(st, cfg_tfs)      # disabled scalp costs no refresh


def test_needed_timeframes_keeps_5m_probe_for_swing_latency(tmp_path):
    st = _store(tmp_path)
    _insert_signal(st, "swing", "A", "crypto", "swing")
    tfs = pm.needed_timeframes(st, ["1m", "5m", "15m", "1h", "4h"])
    assert "5m" in tfs
    assert "1h" in tfs


def test_tracker_db_lock_gets_one_bounded_retry(tmp_path, monkeypatch):
    st = _store(tmp_path)
    _insert_signal(st, "c1", "A", "crypto", "intraday")
    sup = _Sup(st, tmp_path)
    from src.signals.config import load_signal_tracking_config
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    monkeypatch.setattr("src.signals.pending_symbol_universe.pending_symbols", lambda *a, **k: [])
    calls = {"n": 0}

    def _flaky(**_kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("database is locked")
        return type("R", (), {"checked": 1, "tp_hits": 0, "stopped": 0, "expired": 0})()

    monkeypatch.setattr("src.signals.tracker.track_pending_entries", _flaky)
    s = pm.pending_monitor_tick(sup, tracker_config=cfg, refresh_fn=lambda *a, **k: {"refreshed": 0}, tick_index=1)
    assert calls["n"] == 2
    assert s["tracker_retries"] == 1 and s["checked"] == 1
    assert any(e["event_type"] == "pending_tracker_db_retry" for e in tel.load_events(st))


def test_pending_tick_temporarily_uses_short_sqlite_busy_timeout(tmp_path, monkeypatch):
    st = _store(tmp_path)
    original = st.busy_timeout_ms
    sup = _Sup(st, tmp_path)
    from src.signals.config import load_signal_tracking_config
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    monkeypatch.setattr("src.signals.pending_symbol_universe.pending_symbols", lambda *a, **k: [])
    seen = []

    def _track(**_kwargs):
        seen.append(st.busy_timeout_ms)
        return type("R", (), {"checked": 0, "tp_hits": 0, "stopped": 0, "expired": 0,
                               "skip_reason": None})()

    monkeypatch.setattr("src.signals.tracker.track_pending_entries", _track)
    pm.pending_monitor_tick(
        sup, tracker_config=cfg, tick_index=1, tracker_db_busy_timeout_ms=750)

    assert seen == [750]
    assert st.busy_timeout_ms == original


def test_tracker_lock_contention_gets_one_bounded_retry(tmp_path, monkeypatch):
    st = _store(tmp_path)
    _insert_signal(st, "c1", "A", "crypto", "intraday")
    sup = _Sup(st, tmp_path)
    from src.signals.config import load_signal_tracking_config
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    monkeypatch.setattr("src.signals.pending_symbol_universe.pending_symbols", lambda *a, **k: [])
    calls = {"n": 0}

    def _contended_then_ok(**_kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            return type("R", (), {"checked": 0, "tp_hits": 0, "stopped": 0, "expired": 0,
                                    "skip_reason": "writer_lock_contended"})()
        return type("R", (), {"checked": 1, "tp_hits": 0, "stopped": 0, "expired": 0,
                                "skip_reason": None})()

    monkeypatch.setattr("src.signals.tracker.track_pending_entries", _contended_then_ok)
    s = pm.pending_monitor_tick(sup, tracker_config=cfg, refresh_fn=lambda *a, **k: {"refreshed": 0}, tick_index=1)
    assert calls["n"] == 2
    assert s["tracker_retries"] == 1 and s["checked"] == 1
    assert any(e["event_type"] == "pending_tracker_lock_retry" for e in tel.load_events(st))


def test_default_refresh_cache_reduces_fetch_calls(tmp_path, monkeypatch):
    import time as _t

    class _FakeCollector:
        calls = []

        def __init__(self, config, file_store):
            pass

        def fetch(self, symbols=None, timeframes=None):
            _FakeCollector.calls.append(list(symbols or []))
            return type("S", (), {"fetched": [f"{s} {tf}" for s in symbols for tf in timeframes],
                                  "failed": {}})()

    monkeypatch.setattr("src.data_collectors.binance_collector.BinanceOHLCVCollector", _FakeCollector)
    cache: dict = {}
    mono = _t.monotonic()
    r1 = pm._default_refresh(None, None, ["A/USDT", "B/USDT"], ["5m", "1h"],
                             concurrency=2, cache=cache, ttl_sec=60, mono=mono)
    assert r1["refreshed"] == 2 and r1["cache_hits"] == 0 and r1["failed"] == 0
    r2 = pm._default_refresh(None, None, ["A/USDT", "B/USDT"], ["5m", "1h"],
                             concurrency=2, cache=cache, ttl_sec=60, mono=mono + 1)
    assert r2["refreshed"] == 0 and r2["cache_hits"] == 2           # within TTL → NO refetch
    assert sum(len(c) for c in _FakeCollector.calls) == 2          # collector hit only once


def test_default_refresh_symbol_failure_does_not_kill(tmp_path, monkeypatch):
    class _PartialCollector:
        def __init__(self, config, file_store):
            pass

        def fetch(self, symbols=None, timeframes=None):
            # one symbol "fails", the rest succeed (mirrors collector's per-symbol fail-open)
            failed = {f"{s} {tf}": "boom" for s in symbols if "BAD" in s for tf in timeframes}
            ok = [f"{s} {tf}" for s in symbols if "BAD" not in s for tf in timeframes]
            return type("S", (), {"fetched": ok, "failed": failed})()

    monkeypatch.setattr("src.data_collectors.binance_collector.BinanceOHLCVCollector", _PartialCollector)
    r = pm._default_refresh(None, None, ["GOOD/USDT", "BAD/USDT"], ["5m"],
                            concurrency=1, cache={}, ttl_sec=60, mono=0.0)
    assert r["refreshed"] == 2 and r["failed"] >= 1                # bad symbol counted, run continued


def test_default_refresh_recovers_binance_miss_from_bybit(monkeypatch):
    class _BinanceMiss:
        def __init__(self, config, file_store):
            pass

        def fetch(self, symbols=None, timeframes=None):
            return type("S", (), {"fetched": [],
                                  "failed": {s: "not listed" for s in symbols}})()

    class _BybitHit:
        def __init__(self, config, file_store):
            pass

        def fetch(self, symbols=None, timeframes=None):
            return type("S", (), {"fetched": [f"{s} {tf}" for s in symbols for tf in timeframes],
                                  "failed": {}})()

    class _MexcUnused:
        def __init__(self, config, file_store):
            raise AssertionError("MEXC should not run after full Bybit recovery")

    monkeypatch.setattr("src.data_collectors.binance_collector.BinanceOHLCVCollector", _BinanceMiss)
    monkeypatch.setattr("src.data_collectors.bybit_collector.BybitOHLCVCollector", _BybitHit)
    monkeypatch.setattr("src.data_collectors.mexc_collector.MEXCOHLCVCollector", _MexcUnused)
    result = pm._default_refresh(object(), object(), ["ONLYBYBIT/USDT"], ["5m"],
                                 concurrency=1, cache={}, ttl_sec=0, mono=0.0)
    assert result["refresh_succeeded_pairs"] == 1
    assert result["fallback_fetched_pairs"] == 1
    assert result["refresh_failed_pairs"] == 0


def test_tick_refresh_exception_is_fail_open(tmp_path, monkeypatch):
    st = _store(tmp_path)
    _insert_signal(st, "c1", "A", "crypto", "intraday")
    sup = _Sup(st, tmp_path)
    from src.signals.config import load_signal_tracking_config
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    monkeypatch.setattr("src.signals.pending_symbol_universe.pending_symbols",
                        lambda *a, **k: ["BTC/USDT"])
    monkeypatch.setattr("src.signals.tracker.track_signal", lambda **kw: None)

    def _boom(*a, **k):
        raise RuntimeError("429 rate limited")
    s = pm.pending_monitor_tick(sup, tracker_config=cfg, refresh_fn=_boom, tick_index=1)
    assert any("ohlcv:" in e for e in s["errors"])                 # refresh failure recorded
    assert "track_ms" in s and "total_ms" in s                     # tracker still ran (tick continued)


def test_concurrency_does_not_change_checked_set(tmp_path, monkeypatch):
    st = _store(tmp_path)
    for i in range(4):
        _insert_signal(st, f"c{i}", "A", "crypto", "intraday")
    sup = _Sup(st, tmp_path)
    from src.signals.config import load_signal_tracking_config
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    monkeypatch.setattr("src.signals.pending_symbol_universe.pending_symbols", lambda *a, **k: [])
    checked: dict[int, set] = {}

    def _make_recorder(bucket):
        def _rec(**kw):
            bucket.add(kw["signal"]["signal_id"])
            return None
        return _rec

    for conc in (1, 8):
        checked[conc] = set()
        monkeypatch.setattr("src.signals.tracker.track_signal", _make_recorder(checked[conc]))
        pm.pending_monitor_tick(sup, tracker_config=cfg, concurrency=conc,
                                refresh_fn=lambda *a, **k: {"refreshed": 0, "failed": 0,
                                                            "cache_hits": 0, "cache_misses": 0,
                                                            "concurrency": conc}, tick_index=1)
    assert checked[1] == checked[8] == {"c0", "c1", "c2", "c3"}     # identical checked set


def test_emit_once_holds_across_concurrent_fetch_ticks(tmp_path, monkeypatch):
    from src.storage.sqlite import SQLiteStore
    from src.signals.models import SignalOutcome, STATUS_TRIGGERED
    from src.signals.config import load_signal_tracking_config
    st = SQLiteStore(Path(tmp_path) / "t.sqlite"); st.init_db()
    _insert_signal(st, "sig1", "A", "crypto", "intraday")
    sup = _Sup(st, tmp_path)
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    monkeypatch.setattr("src.signals.pending_symbol_universe.pending_symbols", lambda *a, **k: [])
    monkeypatch.setattr("src.notifiers.paper_entry.send_paper_entry_alert",
                        lambda **kw: {"sent": True, "reason_skipped": None})

    def _fake_ts(**kw):
        s = kw["signal"]
        oc = SignalOutcome(signal_id=s["signal_id"], checked_at="2026-07-06T10:05:00+00:00",
                           status=STATUS_TRIGGERED, entry_triggered=True,
                           entry_triggered_at="2026-07-06T10:05:00+00:00", entry_price_used=100.0)
        return (oc, STATUS_TRIGGERED)
    monkeypatch.setattr("src.signals.tracker.track_signal", _fake_ts)

    class _Not:
        enabled = True
        chat_id = "1"
    for _ in range(3):
        pm.pending_monitor_tick(sup, notifier=_Not(), tracker_config=cfg, concurrency=6,
                                refresh_fn=lambda *a, **k: {"refreshed": 0}, tick_index=1)
    ev = tel.load_events(st)
    assert sum(1 for e in ev if e["event_type"] == "entry_condition_detected") == 1
    assert sum(1 for e in ev if e["event_type"] == "paper_entry_alert_sent") == 1


# ---- review fixes: TTL clamp / failed-not-cached / metrics / observe-only / wording -----

def test_ttl_is_clamped_below_interval(tmp_path):
    st = _store(tmp_path)
    _insert_signal(st, "c1", "A", "crypto", "intraday")
    sup = _Sup(st, tmp_path)
    from src.signals.config import load_signal_tracking_config
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    seen = {}

    def _rec_refresh(config, fs, syms, tfs, *, concurrency, cache, ttl_sec, mono):
        seen["ttl"] = ttl_sec
        return {"refresh_attempted_symbols": 0}
    s = pm.pending_monitor_tick(sup, tracker_config=cfg, tick_index=1, interval_sec=45,
                                fetch_ttl_sec=60.0, refresh_fn=_rec_refresh)
    # effective TTL clamped to interval/2 (22.5) so a 45s-later tick can never reuse stale candles
    assert seen["ttl"] == 22.5 and s["effective_ttl_sec"] == 22.5
    assert s["effective_ttl_sec"] < 45


def test_failed_pair_not_cached_and_retried(tmp_path, monkeypatch):
    calls: list[list[str]] = []

    class _FlakyCollector:
        def __init__(self, config, file_store):
            pass

        def fetch(self, symbols=None, timeframes=None):
            calls.append(sorted(symbols or []))
            ok = [f"{s} {tf}" for s in symbols if "BAD" not in s for tf in timeframes]
            bad = {f"{s} {tf}": "boom" for s in symbols if "BAD" in s for tf in timeframes}
            return type("S", (), {"fetched": ok, "failed": bad})()

    monkeypatch.setattr("src.data_collectors.binance_collector.BinanceOHLCVCollector", _FlakyCollector)
    cache: dict = {}
    r1 = pm._default_refresh(None, None, ["GOOD/USDT", "BAD/USDT"], ["5m"],
                             concurrency=1, cache=cache, ttl_sec=60, mono=100.0)
    assert r1["refresh_succeeded_symbols"] == 1 and r1["refresh_failed_symbols"] == 1
    assert ("GOOD/USDT", "5m") in cache and ("BAD/USDT", "5m") not in cache   # only success cached
    # next tick within TTL: GOOD is fresh (skipped), BAD is retried
    r2 = pm._default_refresh(None, None, ["GOOD/USDT", "BAD/USDT"], ["5m"],
                             concurrency=1, cache=cache, ttl_sec=60, mono=101.0)
    assert r2["cache_hits"] == 1 and r2["refresh_attempted_symbols"] == 1
    assert calls[-1] == ["BAD/USDT"]                                          # only the failed one retried


def test_attempted_succeeded_failed_metrics(tmp_path, monkeypatch):
    class _PartCollector:
        def __init__(self, config, file_store):
            pass

        def fetch(self, symbols=None, timeframes=None):
            # A fully ok; B one tf fails; C symbol-level fail (no tf token)
            fetched, failed = [], {}
            for s in symbols:
                for tf in timeframes:
                    if s == "A/USDT":
                        fetched.append(f"{s} {tf}")
                    elif s == "B/USDT" and tf == "5m":
                        failed[f"{s} {tf}"] = "empty"
                    elif s == "B/USDT":
                        fetched.append(f"{s} {tf}")
                if s == "C/USDT":
                    failed[s] = "not listed"          # symbol-level → all tfs fail
            return type("S", (), {"fetched": fetched, "failed": failed})()

    monkeypatch.setattr("src.data_collectors.binance_collector.BinanceOHLCVCollector", _PartCollector)
    r = pm._default_refresh(None, None, ["A/USDT", "B/USDT", "C/USDT"], ["5m", "1h"],
                            concurrency=1, cache={}, ttl_sec=60, mono=0.0)
    assert r["refresh_attempted_symbols"] == 3
    assert r["refresh_succeeded_symbols"] == 1          # only A fully ok
    assert r["refresh_failed_symbols"] == 2             # B (partial) + C (symbol-level)
    assert r["refresh_attempted_pairs"] == 6
    assert r["refresh_succeeded_pairs"] == 3            # A(2) + B 1h(1)
    assert r["refresh_failed_pairs"] == 3               # B 5m + C 5m + C 1h
    assert r["failed"] == 3                             # back-compat alias = failed pairs (not "succeeded")


def test_tick_never_tracks_symbol_with_incomplete_fresh_ohlcv(tmp_path, monkeypatch):
    """A failed required timeframe must block only that symbol for this tick.

    This prevents the tracker from replaying an old cache as a freshly
    executable entry after a collector outage.
    """
    st = _store(tmp_path)
    _insert_signal(st, "fresh", "A", "crypto", "swing")
    _insert_signal(st, "stale", "A", "crypto", "swing")
    with st.connect() as conn:
        conn.execute("UPDATE proposed_signals SET symbol='ETH/USDT' WHERE signal_id='stale'")
        conn.commit()
    sup = _Sup(st, tmp_path)
    from src.signals.config import load_signal_tracking_config
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    monkeypatch.setattr("src.signals.pending_symbol_universe.pending_symbols",
                        lambda *args, **kwargs: ["BTC/USDT", "ETH/USDT"])
    captured = {}
    def _track(**kwargs):
        captured["ids"] = kwargs["signal_ids"]
        return type("R", (), {"checked": 1, "tp_hits": 0, "stopped": 0, "expired": 0})()
    monkeypatch.setattr("src.signals.tracker.track_pending_entries", _track)
    summary = pm.pending_monitor_tick(
        sup, tracker_config=cfg, tick_index=1,
        refresh_fn=lambda *args, **kwargs: {
            "refresh_attempted_symbols": 2,
            "refresh_succeeded_symbols": 1,
            "refresh_failed_symbols": 1,
            "refresh_attempted_pairs": 4,
            "refresh_succeeded_pairs": 3,
            "refresh_failed_pairs": 1,
            "ready_symbols": ["BTC/USDT"],
        },
    )
    assert captured["ids"] == ["fresh"]
    assert summary["tracking_eligible_symbols"] == 1
    assert summary["tracking_skipped_stale_symbols"] == 1
    assert any(event["event_type"] == "pending_tracker_stale_data_blocked"
               for event in tel.load_events(st))


def test_observe_only_does_not_call_tracker(tmp_path, monkeypatch):
    st = _store(tmp_path)
    _insert_signal(st, "c1", "A", "crypto", "intraday")
    sup = _Sup(st, tmp_path)
    from src.signals.config import load_signal_tracking_config
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    called = {"track": False}
    monkeypatch.setattr("src.signals.tracker.track_pending_entries",
                        lambda **kw: called.__setitem__("track", True))
    s = pm.pending_monitor_tick(sup, tracker_config=cfg, tick_index=1, observe_only=True,
                                refresh_fn=lambda *a, **k: {"refresh_attempted_symbols": 0})
    assert called["track"] is False                    # tracker NOT invoked → no outcome/status writes
    assert s["observe_only"] is True and s["checked"] == 0
    assert s["selected_crypto"] == 1                    # selection + metrics still computed


def test_dry_run_help_does_not_promise_read_only():
    from src.cli import pending_monitor_cmd
    doc = (pending_monitor_cmd.__doc__ or "").lower()
    assert "not fully read-only" in doc                 # docstring is explicit for --dry-run
    assert "observe-only" in doc                        # points to the tracker-skipping mode
    # observe-only must NOT be described as fully non-writing / fully read-only
    assert "fully non-writing" not in doc
    assert "may still record latency telemetry" in doc  # honest about telemetry writes


def test_pending_monitor_tick_attributes_source(tmp_path, monkeypatch):
    from src.storage.sqlite import SQLiteStore
    from src.signals.models import SignalOutcome, STATUS_TRIGGERED
    from src.signals.config import load_signal_tracking_config
    st = SQLiteStore(Path(tmp_path) / "t.sqlite"); st.init_db()
    _insert_signal(st, "sig1", "A", "crypto", "intraday")
    sup = _Sup(st, tmp_path)
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    monkeypatch.setattr("src.signals.pending_symbol_universe.pending_symbols", lambda *a, **k: [])
    monkeypatch.setattr("src.notifiers.paper_entry.send_paper_entry_alert",
                        lambda **kw: {"sent": True, "reason_skipped": None})

    def _fake_ts(**kw):
        s = kw["signal"]
        oc = SignalOutcome(signal_id=s["signal_id"], checked_at="2026-07-06T10:05:00+00:00",
                           status=STATUS_TRIGGERED, entry_triggered=True,
                           entry_triggered_at="2026-07-06T10:05:00+00:00", entry_price_used=100.0)
        return (oc, STATUS_TRIGGERED)
    monkeypatch.setattr("src.signals.tracker.track_signal", _fake_ts)

    class _Not:
        enabled = True
        chat_id = "1"
    # source defaults to "pending-monitor" in pending_monitor_tick
    pm.pending_monitor_tick(sup, notifier=_Not(), tracker_config=cfg, tick_index=1,
                            refresh_fn=lambda *a, **k: {"refresh_attempted_symbols": 0})
    ev = {e["event_type"]: e for e in tel.load_events(st)}
    assert ev["entry_condition_detected"]["source"] == "pending-monitor"
    assert ev["paper_entry_alert_sent"]["source"] == "pending-monitor"


def test_selection_snapshot_matches_checked(tmp_path, monkeypatch):
    st = _store(tmp_path)
    for i in range(4):
        _insert_signal(st, f"c{i}", "A", "crypto", "intraday")
    _insert_signal(st, "s1", "A", "stocks", "intraday")     # excluded from crypto snapshot
    sup = _Sup(st, tmp_path)
    from src.signals.config import load_signal_tracking_config
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    monkeypatch.setattr("src.signals.pending_symbol_universe.pending_symbols", lambda *a, **k: [])
    monkeypatch.setattr("src.signals.tracker.track_signal", lambda **kw: None)  # no OHLCV → skipped
    s = pm.pending_monitor_tick(sup, tracker_config=cfg, tick_index=1,
                                refresh_fn=lambda *a, **k: {"refresh_attempted_symbols": 0})
    # `checked` comes from the SAME snapshot as `selected_crypto` → they match (no re-select drift)
    assert s["selected_crypto"] == 4 and s["checked"] == 4


def test_run_pending_monitor_iterations_and_leader_release(tmp_path, monkeypatch):
    st = _store(tmp_path)
    monkeypatch.setattr("src.signals.config.load_signal_tracking_config",
                        lambda root: type("C", (), {"enabled": True})())
    # avoid any real fetch: no pending symbols in an empty store
    res = pm.run_pending_monitor(_Sup(st, tmp_path), interval_sec=0, iterations=2,
                                 sleep=lambda s: None)
    assert res["skipped"] is False and res["totals"]["ticks"] == 2
    # leader lock released after the run
    assert pm.leader_status(tmp_path, "crypto", ttl_sec=180).get("active") in (False, None)
