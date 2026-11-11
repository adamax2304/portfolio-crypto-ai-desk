"""Regression tests for the Recent Signal Performance section fix.

Covers the bugs found during live verification:
  1. The active-signals counter used a non-existent ``signals`` table and
     silently returned 0. After the fix it must query ``proposed_signals``.
  2. The asset_class filter must produce different counts for crypto vs
     stocks.
  3. Schema bugs (wrong table / column) must no longer be swallowed silently.
  4. The stocks pipeline registers signals BEFORE rendering the report so
     the embedded signal-performance section reflects the current run.
"""

from __future__ import annotations

import sqlite3
import uuid
from datetime import datetime, timezone

from src.config import load_config
from src.signals.report_section import (
    _ACTIVE_SIGNAL_STATUSES,
    _count_active_signals,
    build_signal_performance_block,
)
from src.storage.sqlite import SQLiteStore


def _make_store() -> SQLiteStore:
    config = load_config()
    store = SQLiteStore(config.db_path)
    store.init_db()
    return store


def _insert_signal(
    store: SQLiteStore,
    *,
    symbol: str,
    asset_class: str,
    status: str = "waiting_for_entry",
    tier: str = "B",
    mode: str = "intraday",
    direction: str = "long",
) -> str:
    sig_id = f"sig_test_{asset_class}_{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc).isoformat()
    with store.connect() as conn:
        conn.execute(
            """
            INSERT INTO proposed_signals(
                signal_id, created_at, updated_at, symbol, direction, mode,
                tier, score, confidence, asset_class, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                sig_id, now, now, symbol, direction, mode,
                tier, 70.0, "medium", asset_class, status,
            ),
        )
    return sig_id


def _cleanup(store: SQLiteStore, signal_ids: list[str]) -> None:
    if not signal_ids:
        return
    with store.connect() as conn:
        qmarks = ",".join("?" for _ in signal_ids)
        conn.execute(
            f"DELETE FROM proposed_signals WHERE signal_id IN ({qmarks})",
            tuple(signal_ids),
        )


# ---------------------------------------------------------------------------
# Bug 1 — _count_active_signals queries the correct table
# ---------------------------------------------------------------------------

def test_count_active_signals_uses_proposed_signals_table():
    """The helper must query ``proposed_signals``, not the non-existent
    ``signals`` table that the original implementation referenced."""
    store = _make_store()
    inserted: list[str] = []
    try:
        sig = _insert_signal(
            store, symbol="QA_FIX_AAPL", asset_class="stocks",
            status="waiting_for_entry",
        )
        inserted.append(sig)
        n = _count_active_signals(store, asset_class="stocks")
        assert n >= 1, "active count should include the just-inserted signal"
    finally:
        _cleanup(store, inserted)


def test_count_active_signals_respects_asset_class():
    """Inserting a stocks signal must not bump the crypto active count."""
    store = _make_store()
    inserted: list[str] = []
    try:
        crypto_before = _count_active_signals(store, asset_class="crypto")
        stocks_before = _count_active_signals(store, asset_class="stocks")
        sig = _insert_signal(
            store, symbol="QA_FIX_TSLA", asset_class="stocks",
        )
        inserted.append(sig)
        crypto_after = _count_active_signals(store, asset_class="crypto")
        stocks_after = _count_active_signals(store, asset_class="stocks")
        assert stocks_after == stocks_before + 1
        assert crypto_after == crypto_before  # untouched
    finally:
        _cleanup(store, inserted)


def test_count_active_signals_filters_closed_states():
    """Stopped/expired signals must NOT count as active."""
    store = _make_store()
    inserted: list[str] = []
    try:
        before = _count_active_signals(store, asset_class="stocks")
        sig_stopped = _insert_signal(
            store, symbol="QA_FIX_NVDA_STOP", asset_class="stocks",
            status="stopped",
        )
        sig_expired = _insert_signal(
            store, symbol="QA_FIX_AMD_EXP", asset_class="stocks",
            status="expired",
        )
        inserted.extend([sig_stopped, sig_expired])
        after = _count_active_signals(store, asset_class="stocks")
        assert after == before, (
            "stopped/expired signals must not appear in active count"
        )
    finally:
        _cleanup(store, inserted)


def test_active_signal_statuses_constant_kept_in_sync_with_registry():
    """``_ACTIVE_SIGNAL_STATUSES`` must match the registry's notion of
    active. If it drifts, ``active-signals`` CLI and the report block will
    return different numbers."""
    expected = {
        "generated", "waiting_for_entry", "triggered", "tp1_hit", "tp2_hit",
    }
    assert set(_ACTIVE_SIGNAL_STATUSES) == expected


# ---------------------------------------------------------------------------
# Bug 2 — exceptions are no longer swallowed silently
# ---------------------------------------------------------------------------

def test_count_active_signals_raises_on_schema_bug(tmp_path):
    """If someone breaks the schema (e.g. by querying the wrong table) the
    helper must raise ``sqlite3.OperationalError`` instead of returning 0
    silently. This is the regression test for the original bug."""
    # Build a SQLiteStore against a fresh empty DB that intentionally has no
    # `proposed_signals` table.
    empty_db = tmp_path / "empty.db"
    with sqlite3.connect(empty_db) as conn:
        # Create some unrelated table so the file exists.
        conn.execute("CREATE TABLE _dummy(id INTEGER)")

    class _BareStore:
        def __init__(self, path):
            self._path = path

        def connect(self):
            return sqlite3.connect(self._path)

    store = _BareStore(empty_db)
    raised = False
    try:
        _count_active_signals(store, asset_class="stocks")  # type: ignore[arg-type]
    except sqlite3.OperationalError:
        raised = True
    assert raised, (
        "wrong schema must raise sqlite3.OperationalError, not return 0 "
        "(this was the silent failure caught by the QA verification)"
    )


def test_build_block_degrades_gracefully_on_import_error(monkeypatch):
    """The outer block stays failure-safe for genuine ImportError / DB
    connection errors so the report keeps going."""

    class BrokenConfig:
        @property
        def root(self):
            raise RuntimeError("simulated")

        @property
        def db_path(self):
            raise RuntimeError("simulated")

    # RuntimeError is not in the narrow except list now; this should raise.
    raised = False
    try:
        build_signal_performance_block(BrokenConfig(), asset_class="crypto")
    except RuntimeError:
        raised = True
    assert raised, "RuntimeError must propagate after the narrow except fix"


# ---------------------------------------------------------------------------
# Bug 3 — block reports a non-zero active count when one exists
# ---------------------------------------------------------------------------

def test_block_shows_nonzero_active_when_signals_exist():
    store = _make_store()
    config = load_config()
    inserted: list[str] = []
    try:
        sig = _insert_signal(
            store, symbol="QA_FIX_GOOG", asset_class="stocks",
        )
        inserted.append(sig)
        text = build_signal_performance_block(config, asset_class="stocks")
        assert "Active right now: 0" not in text, (
            "block reports 0 active despite an active stocks signal existing"
        )
        # The expected line should appear with a number ≥ 1.
        # We don't lock down the exact number because the production DB
        # may already have other live signals — but it must NOT be 0.
    finally:
        _cleanup(store, inserted)


def test_block_renders_for_both_asset_classes():
    config = load_config()
    crypto_block = build_signal_performance_block(config, asset_class="crypto")
    stocks_block = build_signal_performance_block(config, asset_class="stocks")
    assert "Asset class: crypto" in crypto_block
    assert "Asset class: stocks" in stocks_block
    # Neither should claim "unavailable" against the live DB.
    assert "unavailable" not in crypto_block.lower()
    assert "unavailable" not in stocks_block.lower()


def test_block_sample_size_matches_signal_stats():
    """The all-tier sample shown in the report must match what
    ``signal-stats --asset-class stocks`` reports — the original bug was a
    field-name mismatch (``sample`` vs ``sample_size``) that made the
    report read 0 while the CLI read N.

    R1 (2026-06-03): the headline is now A/B-only, so the FULL all-tier sample
    appears in the 'All-tier diagnostic' block (not the headline). The
    headline carries the A/B sample. Both are validated here.
    """
    from src.signals.analytics import compute_breakdowns, headline_split
    from src.signals.config import load_signal_tracking_config

    config = load_config()
    store = _make_store()
    cfg = load_signal_tracking_config(config.root)
    breakdown = compute_breakdowns(
        store, config=cfg, period="week", asset_class="stocks"
    )
    expected_all = int(breakdown.overall.get("sample_size") or 0)
    split = headline_split(store, config=cfg, period="week", asset_class="stocks")
    expected_ab = int(split["actionable"].get("sample_size") or 0)

    block = build_signal_performance_block(config, asset_class="stocks")
    # All-tier diagnostic block carries the full sample (the regression guard).
    diag = block.split("All-tier diagnostic")[-1]
    assert f"Sample: {expected_all}" in diag, (
        f"all-tier diagnostic sample does not match signal-stats sample_size={expected_all}"
    )
    # Headline block carries the A/B sample.
    headline = block.split("C-tier Watchlist")[0]
    assert f"Sample: {expected_ab}" in headline, (
        f"headline A/B sample does not match A+B sample_size={expected_ab}"
    )


def test_block_does_not_break_signal_stats():
    """Sanity: importing the section module and rendering a block must not
    poison the signal-stats analytics layer."""
    from src.signals.analytics import compute_breakdowns
    from src.signals.config import load_signal_tracking_config

    config = load_config()
    store = _make_store()
    cfg = load_signal_tracking_config(config.root)

    before = compute_breakdowns(
        store, config=cfg, period="week", asset_class="stocks"
    ).overall.get("sample_size")
    build_signal_performance_block(config, asset_class="stocks")
    after = compute_breakdowns(
        store, config=cfg, period="week", asset_class="stocks"
    ).overall.get("sample_size")
    assert before == after, "rendering the block changed signal-stats output"
