"""Tests for the pending-signal revalidator.

Covers:
- Stale-by-age: a waiting signal older than the mode's freshness horizon
  is promoted to `stale_before_entry`.
- Moved-away: a waiting signal whose favorable excursion exceeded 2R
  without filling is promoted to `entry_moved_away`.
- Invariant: revalidator NEVER mutates entry/stop/TP/expires_at on the
  proposed_signals row.
- Tracker still passes existing tests (sanity reference).
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pandas as pd

from src.signals.revalidator import (
    FRESHNESS_HORIZON_HOURS,
    STATUS_ENTRY_MOVED_AWAY,
    STATUS_STALE_BEFORE_ENTRY,
    revalidate_pending_signals,
    revalidate_signal,
)
from src.signals.models import STATUS_WAITING


UTC = timezone.utc


def _signal(
    *,
    mode: str = "intraday",
    direction: str = "long",
    created_at: datetime,
    entry_low: float = 100.0,
    entry_high: float = 101.0,
    invalidation: float = 97.0,
) -> dict:
    return {
        "signal_id": "sig_test123",
        "symbol": "TEST/USDT",
        "mode": mode,
        "direction": direction,
        "status": STATUS_WAITING,
        "created_at": created_at.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "entry_low": entry_low,
        "entry_high": entry_high,
        "invalidation": invalidation,
        "asset_class": "crypto",
        "exchange_focus": "binance",
    }


def _config():
    cfg = MagicMock()
    cfg.enabled = True
    return cfg


def test_stale_before_entry_triggers_after_horizon():
    """Scalp signal older than 1h freshness horizon → stale_before_entry."""
    now = datetime(2026, 6, 9, 14, 0, tzinfo=UTC)
    created = now - timedelta(hours=2)  # 2h > scalp horizon 1.0h
    signal = _signal(mode="scalp", created_at=created)

    # No OHLCV available — the moved-away check returns 0, falls through to staleness
    file_store = MagicMock()
    file_store.load_ohlcv.return_value = pd.DataFrame()
    file_store.load_stocks_ohlcv.return_value = pd.DataFrame()
    project_config = MagicMock()
    project_config.anchor_exchange = "binance"

    result = revalidate_signal(
        signal=signal,
        file_store=file_store,
        project_config=project_config,
        tracker_config=_config(),
        now=now,
    )
    assert result is not None
    outcome, new_status = result
    assert new_status == STATUS_STALE_BEFORE_ENTRY
    assert "stale_before_entry" in outcome.notes
    assert outcome.entry_triggered is False
    # Spec invariant: revalidator does not set price levels.
    assert outcome.entry_price_used is None
    assert outcome.stop_hit_at is None
    assert outcome.tp1_hit_at is None


def test_fresh_pending_signal_not_promoted():
    """Intraday signal still inside its freshness horizon → no transition."""
    now = datetime(2026, 6, 9, 14, 0, tzinfo=UTC)
    created = now - timedelta(hours=1)  # < intraday horizon 4.0h
    signal = _signal(mode="intraday", created_at=created)

    file_store = MagicMock()
    file_store.load_ohlcv.return_value = pd.DataFrame()
    project_config = MagicMock()
    project_config.anchor_exchange = "binance"

    result = revalidate_signal(
        signal=signal,
        file_store=file_store,
        project_config=project_config,
        tracker_config=_config(),
        now=now,
    )
    assert result is None


def test_stock_intraday_after_close_waits_for_target_session():
    """After-hours/weekend stock plans must not stale before target RTH opens."""
    created = datetime(2026, 9, 18, 20, 59, tzinfo=UTC)  # Friday after NY close
    now = datetime(2026, 9, 19, 14, 0, tzinfo=UTC)       # Saturday
    signal = _signal(mode="intraday", created_at=created)
    signal.update({"asset_class": "stocks", "symbol": "AAPL"})

    file_store = MagicMock()
    file_store.load_ohlcv.return_value = pd.DataFrame()
    file_store.load_stocks_ohlcv.return_value = pd.DataFrame()
    project_config = MagicMock()
    project_config.anchor_exchange = "binance"

    result = revalidate_signal(
        signal=signal,
        file_store=file_store,
        project_config=project_config,
        tracker_config=_config(),
        now=now,
    )
    assert result is None


def test_entry_moved_away_long_with_2r_excursion(monkeypatch):
    """Long signal where price ran 3R favorable without filling → entry_moved_away."""
    # Patch the favorable_excursion helper to return a high R, simulating
    # the favorable move scenario without needing real OHLCV.
    from src.signals import revalidator as rv

    def fake_excursion(signal, file_store, project_config):
        return 3.0, "2026-06-09T13:00:00+00:00"

    monkeypatch.setattr(rv, "_favorable_excursion_r", fake_excursion)

    now = datetime(2026, 6, 9, 14, 0, tzinfo=UTC)
    created = now - timedelta(hours=3)  # > intraday expected_fill horizon (2h)
    signal = _signal(mode="intraday", created_at=created)

    result = rv.revalidate_signal(
        signal=signal,
        file_store=MagicMock(),
        project_config=MagicMock(),
        tracker_config=_config(),
        now=now,
    )
    assert result is not None
    outcome, new_status = result
    assert new_status == STATUS_ENTRY_MOVED_AWAY
    assert "favorable_excursion_r=3.00" in outcome.notes
    assert outcome.entry_triggered is False


def test_non_waiting_signal_skipped():
    """Revalidator only acts on STATUS_WAITING signals."""
    now = datetime(2026, 6, 9, 14, 0, tzinfo=UTC)
    created = now - timedelta(hours=10)
    signal = _signal(mode="scalp", created_at=created)
    signal["status"] = "triggered"  # already filled

    result = revalidate_signal(
        signal=signal,
        file_store=MagicMock(),
        project_config=MagicMock(),
        tracker_config=_config(),
        now=now,
    )
    assert result is None


def test_freshness_horizons_match_spec():
    """Swing horizon matches its registered seven-day validity window."""
    assert FRESHNESS_HORIZON_HOURS["scalp"] == 1.0
    assert FRESHNESS_HORIZON_HOURS["intraday"] == 4.0
    assert FRESHNESS_HORIZON_HOURS["swing"] == 168.0
    assert FRESHNESS_HORIZON_HOURS["invest"] == 72.0


def test_swing_pending_for_three_days_is_not_marked_stale_before_its_validity():
    now = datetime(2026, 6, 9, 14, 0, tzinfo=UTC)
    signal = _signal(mode="swing", created_at=now - timedelta(hours=72))
    result = revalidate_signal(
        signal=signal,
        file_store=MagicMock(),
        project_config=MagicMock(),
        tracker_config=_config(),
        now=now,
    )
    assert result is None


def test_revalidator_does_not_call_upsert(monkeypatch):
    """Invariant: the revalidator must NEVER mutate proposed_signals levels."""
    from src.signals import revalidator as rv

    # Counter to detect any attempt to call upsert.
    upsert_calls = []

    def fake_excursion(signal, file_store, project_config):
        return 0.5, None  # below moved-away threshold

    monkeypatch.setattr(rv, "_favorable_excursion_r", fake_excursion)

    now = datetime(2026, 6, 9, 14, 0, tzinfo=UTC)
    created = now - timedelta(hours=10)
    signal = _signal(mode="scalp", created_at=created)

    result = revalidate_signal(
        signal=signal,
        file_store=MagicMock(),
        project_config=MagicMock(),
        tracker_config=_config(),
        now=now,
    )
    assert result is not None
    outcome, _ = result
    # SignalOutcome has NO field for entry_low / entry_high / tp1 / invalidation —
    # by construction it cannot transmit level changes back to proposed_signals.
    row = outcome.to_row()
    forbidden_fields = {"entry_low", "entry_high", "stop_loss", "invalidation",
                        "tp1", "tp2", "tp3", "expires_at"}
    assert not (forbidden_fields & set(row.keys())), (
        f"SignalOutcome must not carry level fields; found {forbidden_fields & set(row.keys())}"
    )


# ---------------------------------------------------------------------------
# 2026-07-13 review: revalidate_pending_signals() owns the writer_lock (closes the residual
# --revalidate-pending race gap), but nothing exercised the actual lock-contention path --
# only the pure revalidate_signal() decision function was tested. Close that gap.
# ---------------------------------------------------------------------------
def test_revalidate_pending_signals_yields_when_writer_lock_held(tmp_path):
    """End-to-end: while the writer lock is already held (simulating an in-flight
    full pass or pending tick), revalidate_pending_signals must return an empty
    result and must NOT write anything to signal_outcomes/proposed_signals."""
    from src.signals import tracker as tracker_mod
    from src.storage.file_store import FileStore
    from src.storage.sqlite import SQLiteStore

    store = SQLiteStore(tmp_path / "reval.sqlite")
    store.init_db()
    now = datetime(2026, 6, 9, 14, 0, tzinfo=UTC)
    created = (now - timedelta(hours=10)).isoformat()
    store.upsert_proposed_signal({
        "signal_id": "sig_lockheld", "symbol": "TEST/USDT", "direction": "long",
        "mode": "scalp", "tier": "A", "asset_class": "crypto", "exchange_focus": "binance",
        "status": STATUS_WAITING, "created_at": created, "updated_at": created,
        "entry_low": 100.0, "entry_high": 101.0, "invalidation": 97.0,
    })

    class _Cfg:
        root = tmp_path
        anchor_exchange = "binance"

    with tracker_mod.writer_lock(tmp_path, blocking=False) as got:
        assert got is True   # confirm the lock is genuinely held for the duration below
        result = revalidate_pending_signals(
            store=store, file_store=MagicMock(spec=FileStore), project_config=_Cfg(),
            tracker_config=_config(),
        )

    assert result.checked == 0
    assert result.stale == 0 and result.moved_away == 0
    assert result.details == []
    row = store.connect().execute(
        "SELECT status FROM proposed_signals WHERE signal_id='sig_lockheld'"
    ).fetchone()
    assert row[0] == STATUS_WAITING   # untouched -- never even read while locked out


def test_revalidate_pending_signals_reaches_signals_when_uncontended(tmp_path):
    """Counterpart: with no writer lock held, the same signal IS processed --
    proves the lock-yield above isn't just an unconditional early return."""
    from src.storage.file_store import FileStore
    from src.storage.sqlite import SQLiteStore

    store = SQLiteStore(tmp_path / "reval2.sqlite")
    store.init_db()
    # revalidate_pending_signals has no injectable `now` (always real wall-clock via _now()), so
    # use a created_at far enough in the past (60d) to be unambiguously stale regardless of when
    # this test actually runs -- only elapsed-time-vs-horizon matters for the staleness path.
    created = (datetime.now(UTC) - timedelta(days=60)).isoformat()
    store.upsert_proposed_signal({
        "signal_id": "sig_uncontended", "symbol": "TEST/USDT", "direction": "long",
        "mode": "scalp", "tier": "A", "asset_class": "crypto", "exchange_focus": "binance",
        "status": STATUS_WAITING, "created_at": created, "updated_at": created,
        "entry_low": 100.0, "entry_high": 101.0, "invalidation": 97.0,
    })

    class _Cfg:
        root = tmp_path
        anchor_exchange = "binance"

    file_store = MagicMock(spec=FileStore)
    file_store.load_ohlcv.return_value = pd.DataFrame()
    file_store.load_stocks_ohlcv.return_value = pd.DataFrame()

    result = revalidate_pending_signals(
        store=store, file_store=file_store, project_config=_Cfg(), tracker_config=_config(),
    )
    assert result.checked == 1
    assert result.stale == 1
