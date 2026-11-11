"""Tests for the 2026-06-16 Option B lightweight pending-only entry tracker.

Verifies: A/B-pending scoping, lock yields to the full pass, no-overlap lock,
and that the pass is idempotent/safe to call concurrently with the full pass.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

from src.signals import tracker as tracker_mod
from src.signals.tracker import (
    full_pass_marker,
    select_pending_ab_signal_ids,
    track_pending_entries,
    _pending_lock,
    _full_pass_active,
    _pending_lock_active,
)


def _store(tmp_path):
    from src.storage.sqlite import SQLiteStore
    st = SQLiteStore(tmp_path / "t.sqlite")
    st.init_db()
    return st


def _insert(st, signal_id, tier, status, asset="crypto", mode="intraday"):
    with st.connect() as c:
        c.execute(
            "INSERT INTO proposed_signals(signal_id, created_at, updated_at, symbol, "
            "direction, mode, tier, score, asset_class, status) "
            "VALUES(?,?,?,?,?,?,?,?,?,?)",
            (signal_id, "2026-06-16T10:00:00+00:00", "2026-06-16T10:00:00+00:00",
             "ZEC/USDT", "long", mode, tier, 70.0, asset, status),
        )
        c.commit()


# ---- WAL concurrency ------------------------------------------------------

def test_connect_enables_wal_and_busy_timeout(tmp_path):
    st = _store(tmp_path)
    with st.connect() as c:
        assert c.execute("PRAGMA journal_mode").fetchone()[0].lower() == "wal"
        assert int(c.execute("PRAGMA busy_timeout").fetchone()[0]) >= 1000


# ---- A/B pending scoping --------------------------------------------------

def test_select_only_ab_nonterminal(tmp_path):
    st = _store(tmp_path)
    _insert(st, "ab_wait", "B", "waiting_for_entry")
    _insert(st, "ab_trig", "A", "triggered")
    _insert(st, "c_wait", "C", "waiting_for_entry")          # excluded: C-tier
    _insert(st, "ab_done", "B", "expired")                   # excluded: terminal
    _insert(st, "stk_swing", "B", "waiting_for_entry",
            asset="stocks", mode="swing")                    # excluded: paper-paused
    _insert(st, "stk_invest", "A", "waiting_for_entry",
            asset="stocks", mode="invest")                   # excluded: paper-paused
    _insert(st, "stk_intra", "B", "triggered",
            asset="stocks", mode="intraday")                 # included: actionable
    ids = set(select_pending_ab_signal_ids(st))
    assert ids == {"ab_wait", "ab_trig", "stk_intra"}


def test_track_pending_empty_when_no_ab_pending(tmp_path):
    st = _store(tmp_path)
    _insert(st, "c_only", "C", "waiting_for_entry")
    from src.signals.config import load_signal_tracking_config
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])

    class _Cfg:  # minimal project_config stand-in; root = tmp (lock dir lives here)
        root = tmp_path

    res = track_pending_entries(
        store=st, file_store=MagicMock(), project_config=_Cfg(),
        tracker_config=cfg, paper_entry_notifier=None,
    )
    assert res.checked == 0


# ---- lock yields to the full pass -----------------------------------------

def test_pending_lock_yields_to_full_pass(tmp_path):
    root = tmp_path
    with full_pass_marker(root):
        assert _full_pass_active(root) is True
        with _pending_lock(root) as acquired:
            assert acquired is False     # must yield while full pass runs
    assert _full_pass_active(root) is False
    with _pending_lock(root) as acquired:
        assert acquired is True          # free again


def test_pending_lock_is_exclusive(tmp_path):
    root = tmp_path
    with _pending_lock(root) as a:
        assert a is True
        with _pending_lock(root) as b:
            assert b is False            # no overlapping pending pass


def test_full_pass_waits_for_active_pending_lock(tmp_path, monkeypatch):
    """2026-07-09 fix: the reverse direction of the race the old test suite never
    covered — a pending pass that is ALREADY in flight the instant the full pass
    starts must finish and release its lock BEFORE the full pass claims its
    marker, closing the window where both could touch the same signal_id at once.

    The background thread acquires/releases the lock via the real _pending_lock
    context manager (not a manual unlink from another thread) — on Windows an
    open file handle blocks a cross-thread delete, so releasing must happen on
    the same fd that opened it, exactly like the real pending pass does."""
    monkeypatch.setattr(tracker_mod, "_PENDING_WAIT_TIMEOUT_SEC", 2.0)
    monkeypatch.setattr(tracker_mod, "_PENDING_WAIT_POLL_SEC", 0.05)
    root = tmp_path
    import threading, time as _t

    acquired_evt = threading.Event()
    released: dict = {"at": None}

    def _hold_pending_lock():
        with _pending_lock(root) as acquired:
            assert acquired is True
            acquired_evt.set()
            _t.sleep(0.2)
        released["at"] = _t.time()   # set right after the context actually released the file

    th = threading.Thread(target=_hold_pending_lock, daemon=True)
    th.start()
    assert acquired_evt.wait(timeout=1.0)           # ensure the pending pass holds the lock first
    assert _pending_lock_active(root) is True

    start = _t.time()
    with full_pass_marker(root):
        claimed_at = _t.time()
    th.join(timeout=1.0)
    assert released["at"] is not None
    # the marker must not have been claimed until AFTER the pending lock released
    assert claimed_at >= released["at"]
    assert claimed_at - start < tracker_mod._PENDING_WAIT_TIMEOUT_SEC   # didn't wait the full bound


def test_full_pass_never_hangs_on_stuck_pending_lock(tmp_path, monkeypatch):
    """A pending lock that never clears (stuck/crashed process) must not block the
    full pass beyond the bounded wait — the 2h outcome sweep must always proceed."""
    monkeypatch.setattr(tracker_mod, "_PENDING_WAIT_TIMEOUT_SEC", 0.3)
    monkeypatch.setattr(tracker_mod, "_PENDING_WAIT_POLL_SEC", 0.05)
    root = tmp_path
    with _pending_lock(root) as acquired:
        assert acquired is True
        import time as _t
        start = _t.time()
        with full_pass_marker(root):
            elapsed = _t.time() - start
        assert elapsed >= tracker_mod._PENDING_WAIT_TIMEOUT_SEC
        assert elapsed < tracker_mod._PENDING_WAIT_TIMEOUT_SEC + 1.0        # bounded, not indefinite


def test_track_pending_skips_under_full_pass(tmp_path):
    """When the full pass marker is set, the pending pass is a no-op."""
    st = _store(tmp_path)
    _insert(st, "ab_wait", "B", "waiting_for_entry")
    from src.signals.config import load_signal_tracking_config
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])

    class _Cfg:
        root = tmp_path

    with full_pass_marker(tmp_path):
        res = track_pending_entries(
            store=st, file_store=MagicMock(), project_config=_Cfg(),
            tracker_config=cfg, paper_entry_notifier=None,
        )
    assert res.checked == 0   # yielded to full pass


# ---- 2026-07-09: strict writer_lock — closes the TOCTOU gap the marker-only coordination had -----
# The old full_pass_marker/_pending_lock pair is check-then-act: full checks _pending_lock_active()
# is False, then (before it writes its own marker) a pending pass could still slip in and acquire
# _pending_lock in that gap — both would then be free to call track_active_signals concurrently.
# writer_lock() is atomic (single O_CREAT|O_EXCL syscall, no separate check step) and is now the
# ONLY thing both track_pending_entries and the CLI full pass rely on for actual mutual exclusion.

def test_writer_lock_pending_holds_full_waits(tmp_path, monkeypatch):
    """Pending (nonblocking) already holds the writer lock; the full pass's
    blocking acquire must wait for release before proceeding — no TOCTOU gap."""
    monkeypatch.setattr(tracker_mod, "_WRITER_BLOCK_TIMEOUT_SEC", 2.0)
    monkeypatch.setattr(tracker_mod, "_WRITER_POLL_SEC", 0.05)
    root = tmp_path
    import threading, time as _t

    acquired_evt = threading.Event()
    released = {"at": None}

    def _hold():
        with tracker_mod.writer_lock(root, blocking=False) as got:
            assert got is True
            acquired_evt.set()
            _t.sleep(0.2)
        released["at"] = _t.time()

    th = threading.Thread(target=_hold, daemon=True)
    th.start()
    assert acquired_evt.wait(timeout=1.0)
    assert tracker_mod._try_acquire_writer_lock_once(root) is None  # confirm genuinely held

    start = _t.time()
    with tracker_mod.writer_lock(root, blocking=True) as got:
        claimed_at = _t.time()
        assert got is True
    th.join(timeout=1.0)
    assert released["at"] is not None
    assert claimed_at >= released["at"]
    assert claimed_at - start < tracker_mod._WRITER_BLOCK_TIMEOUT_SEC


def test_writer_lock_full_holds_pending_fails_fast(tmp_path):
    """Full pass (blocking) holds the writer lock; a pending (nonblocking) attempt
    must fail immediately — no retry loop, no waiting."""
    root = tmp_path
    import time as _t
    with tracker_mod.writer_lock(root, blocking=True) as got_full:
        assert got_full is True
        start = _t.time()
        with tracker_mod.writer_lock(root, blocking=False) as got_pending:
            elapsed = _t.time() - start
        assert got_pending is False
        assert elapsed < 0.2   # fail-fast, single atomic attempt only


def test_writer_lock_stuck_lock_bounds_the_full_pass(tmp_path, monkeypatch):
    """A held (fresh, non-stale) writer lock must not block a blocking acquire
    beyond its bounded timeout — and the caller must see False, never barge in
    unlocked."""
    monkeypatch.setattr(tracker_mod, "_WRITER_BLOCK_TIMEOUT_SEC", 0.3)
    monkeypatch.setattr(tracker_mod, "_WRITER_POLL_SEC", 0.05)
    root = tmp_path
    import time as _t
    with tracker_mod.writer_lock(root, blocking=False) as got:
        assert got is True
        start = _t.time()
        with tracker_mod.writer_lock(root, blocking=True) as got2:
            elapsed = _t.time() - start
            assert got2 is False    # must never proceed unlocked
        assert elapsed >= tracker_mod._WRITER_BLOCK_TIMEOUT_SEC
        assert elapsed < tracker_mod._WRITER_BLOCK_TIMEOUT_SEC + 1.0


def test_writer_lock_two_nonblocking_only_one_wins(tmp_path):
    """Two simultaneous nonblocking attempts (e.g. monitor-watchlist's tick racing
    the standalone pending-monitor daemon's tick) — exactly one acquires."""
    root = tmp_path
    results = []
    import threading, time as _t

    def _try():
        with tracker_mod.writer_lock(root, blocking=False) as got:
            results.append(got)
            if got:
                _t.sleep(0.1)   # hold briefly so the race window is real

    threads = [threading.Thread(target=_try) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=2.0)
    assert sorted(results) == [False, True]


def test_writer_lock_reclaims_fresh_lock_from_dead_owner(tmp_path, monkeypatch):
    lock_dir = tmp_path / ".locks"
    lock_dir.mkdir()
    lock = lock_dir / "tracker_writer.lock"
    lock.write_text("999999 2026-08-03T00:00:00+00:00", encoding="utf-8")
    monkeypatch.setattr(tracker_mod, "_pid_is_running", lambda pid: False)

    with tracker_mod.writer_lock(tmp_path, blocking=False) as got:
        assert got is True
    assert not lock.exists()


def test_pending_lock_reclaims_fresh_lock_from_dead_owner(tmp_path, monkeypatch):
    lock_dir = tmp_path / ".locks"
    lock_dir.mkdir()
    lock = lock_dir / "track_pending.lock"
    lock.write_text("999999 2026-08-03T00:00:00+00:00", encoding="utf-8")
    monkeypatch.setattr(tracker_mod, "_pid_is_running", lambda pid: False)

    with tracker_mod._pending_lock(tmp_path) as got:
        assert got is True
    assert not lock.exists()


def test_track_pending_entries_yields_when_writer_lock_held(tmp_path, monkeypatch):
    """End-to-end: while the writer lock is held (simulating an in-flight full
    pass), track_pending_entries must return empty and must NOT call
    track_active_signals at all."""
    st = _store(tmp_path)
    _insert(st, "ab_wait", "B", "waiting_for_entry")
    from src.signals.config import load_signal_tracking_config
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])

    class _Cfg:
        root = tmp_path

    called = {"n": 0}
    monkeypatch.setattr(
        tracker_mod, "track_active_signals",
        lambda **kw: called.__setitem__("n", called["n"] + 1) or tracker_mod.TrackingResult(),
    )

    with tracker_mod.writer_lock(tmp_path, blocking=False) as got:
        assert got is True
        res = track_pending_entries(
            store=st, file_store=MagicMock(), project_config=_Cfg(),
            tracker_config=cfg, paper_entry_notifier=None,
        )
    assert res.checked == 0
    assert called["n"] == 0   # never entered track_active_signals


def test_track_pending_entries_reaches_track_active_signals_when_uncontended(tmp_path, monkeypatch):
    """Regression/dedup-safety counterpart: with no writer lock held, the SAME
    signal_ids/notifier/telemetry_source still flow through to
    track_active_signals unimpeded — the new lock changes nothing about what the
    dedup-relevant call looks like on the normal, uncontended path."""
    st = _store(tmp_path)
    _insert(st, "ab_wait", "B", "waiting_for_entry")
    from src.signals.config import load_signal_tracking_config
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])

    class _Cfg:
        root = tmp_path

    called = {"n": 0, "kwargs": None}

    def _fake(**kw):
        called["n"] += 1
        called["kwargs"] = kw
        return tracker_mod.TrackingResult()

    monkeypatch.setattr(tracker_mod, "track_active_signals", _fake)

    track_pending_entries(
        store=st, file_store=MagicMock(), project_config=_Cfg(),
        tracker_config=cfg, paper_entry_notifier=None, telemetry_source="pending-monitor",
    )
    assert called["n"] == 1
    assert called["kwargs"]["signal_ids"] == ["ab_wait"]
    assert called["kwargs"]["telemetry_source"] == "pending-monitor"


def test_signal_writer_lock_blocks_only_the_same_signal(tmp_path):
    with tracker_mod.signal_writer_lock(tmp_path, "sig-a", blocking=False) as got_a:
        assert got_a is True
        with tracker_mod.signal_writer_lock(tmp_path, "sig-a", blocking=False) as got_same:
            assert got_same is False
        with tracker_mod.signal_writer_lock(tmp_path, "sig-b", blocking=False) as got_other:
            assert got_other is True


def test_cooperative_tracking_skips_locked_signal_but_processes_other(tmp_path, monkeypatch):
    st = _store(tmp_path)
    _insert(st, "sig-a", "B", "waiting_for_entry")
    _insert(st, "sig-b", "B", "waiting_for_entry")
    from src.signals.config import load_signal_tracking_config
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])

    class _Cfg:
        root = tmp_path

    seen = []

    def _fake_track_signal(**kwargs):
        seen.append(kwargs["signal"]["signal_id"])
        return None

    monkeypatch.setattr(tracker_mod, "track_signal", _fake_track_signal)
    with tracker_mod.signal_writer_lock(tmp_path, "sig-a", blocking=False) as got:
        assert got is True
        result = tracker_mod.track_active_signals(
            store=st,
            file_store=MagicMock(),
            project_config=_Cfg(),
            tracker_config=cfg,
            signal_ids=["sig-a", "sig-b"],
            coordinate_signal_writes=True,
            signal_lock_blocking=False,
        )

    assert seen == ["sig-b"]
    assert result.checked == 1
    assert result.skipped_writer_lock == 1
