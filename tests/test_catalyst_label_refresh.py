"""Tests for the catalyst/news linkage refresh (2026-06-20 regression fix).

Covers:
  * a signal whose symbol has a recent, symbol-tagged news_items hit gets
    news_supported=1 AND a non-"none" signal_catalyst_labels row (fixes both the
    under-firing flag and the frozen label cache);
  * a title-substring-only mention ("Ordinals" / "Sweden") never fabricates a
    catalyst — news_supported stays 0;
  * a telegram-sourced hit sets telegram_supported=1;
  * the flag update is additive-only (never downgrades) and idempotent;
  * --labels-only mode rebuilds the cache without touching the flags.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pytest

from src.storage.sqlite import SQLiteStore
from src.signals.catalyst_label_refresh import refresh_signal_catalyst_labels

NOW = datetime(2026, 6, 20, 18, 0, 0, tzinfo=timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")


def _store(tmp_path) -> SQLiteStore:
    st = SQLiteStore(tmp_path / "linkage.sqlite")
    st.init_db()
    return st


def _add_news(st, *, title, source, url, published_at, detected, importance=2.0):
    with st.connect() as conn:
        conn.execute(
            "INSERT INTO news_items(title, source, url, published_at, "
            "detected_symbols_json, detected_narratives_json, importance, "
            "asset_class, raw_json) VALUES(?,?,?,?,?,?,?,?,?)",
            (title, source, url, published_at, json.dumps(detected),
             json.dumps([]), importance, "crypto", "{}"),
        )


def _add_signal(st, *, signal_id, symbol, created_at, news=0, tg=0,
                status="waiting_for_entry"):
    with st.connect() as conn:
        conn.execute(
            "INSERT INTO proposed_signals(signal_id, created_at, updated_at, "
            "symbol, direction, mode, tier, score, asset_class, "
            "news_supported, telegram_supported, raw_idea_json, status) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (signal_id, created_at, created_at, symbol, "long", "intraday",
             "B", 75.0, "crypto", news, tg, "{}", status),
        )


def _row(st, signal_id):
    with st.connect() as conn:
        r = conn.execute(
            "SELECT news_supported, telegram_supported FROM proposed_signals "
            "WHERE signal_id=?", (signal_id,)).fetchone()
        lab = conn.execute(
            "SELECT * FROM signal_catalyst_labels WHERE signal_id=?",
            (signal_id,)).fetchone()
    return r, (dict(lab) if lab else None)


def test_recent_news_hit_sets_flag_and_label(tmp_path):
    st = _store(tmp_path)
    _add_signal(st, signal_id="sig_ondo", symbol="ONDO/USDT",
                created_at=_iso(NOW - timedelta(hours=1)), news=0)
    _add_news(st, title="ONDO Finance partners with Mirae Asset",
              source="CoinDesk", url="u1",
              published_at=_iso(NOW - timedelta(hours=3)), detected=["ONDO"])

    with st.connect() as conn:
        stats = refresh_signal_catalyst_labels(conn, now=NOW)

    sig, lab = _row(st, "sig_ondo")
    assert sig["news_supported"] == 1, "genuine detected hit must flip 0->1"
    assert stats.news_flips == 1
    assert lab is not None, "a label row must be written (cache no longer frozen)"
    assert lab["catalyst_freshness"] != "none"
    assert lab["source_quality"] in {"reputable", "official", "social", "unknown"}
    assert lab["headline_short"]


def test_title_substring_only_does_not_fabricate(tmp_path):
    """'Ordinals' in a title (no detected ORDI tag) must NOT set news_supported."""
    st = _store(tmp_path)
    _add_signal(st, signal_id="sig_ordi", symbol="ORDI/USDT",
                created_at=_iso(NOW - timedelta(hours=1)), news=0)
    # Title mentions "Ordinals" but the collector never tagged ORDI.
    _add_news(st, title="Bitcoin Ordinals inscriptions hit a record high",
              source="CryptoBriefing", url="u2",
              published_at=_iso(NOW - timedelta(hours=2)), detected=["BTC"])

    with st.connect() as conn:
        stats = refresh_signal_catalyst_labels(conn, now=NOW)

    sig, lab = _row(st, "sig_ordi")
    assert sig["news_supported"] == 0, "must not fabricate a catalyst from substring"
    assert stats.news_flips == 0
    assert lab is not None and lab["catalyst_freshness"] == "none"


def test_telegram_source_sets_telegram_supported(tmp_path):
    st = _store(tmp_path)
    _add_signal(st, signal_id="sig_wld", symbol="WLD/USDT",
                created_at=_iso(NOW - timedelta(hours=1)), news=0, tg=0)
    _add_news(st, title="WLD whale accumulation flagged", source="t.me/lookonchain",
              url="u3", published_at=_iso(NOW - timedelta(hours=4)), detected=["WLD"])

    with st.connect() as conn:
        stats = refresh_signal_catalyst_labels(conn, now=NOW)

    sig, _ = _row(st, "sig_wld")
    assert sig["news_supported"] == 1
    assert sig["telegram_supported"] == 1
    assert stats.telegram_flips == 1


def test_out_of_window_news_is_ignored(tmp_path):
    """A detected hit older than the lookback window must not flip the flag."""
    st = _store(tmp_path)
    _add_signal(st, signal_id="sig_old", symbol="TAO/USDT",
                created_at=_iso(NOW - timedelta(hours=1)), news=0)
    _add_news(st, title="Bittensor TAO proposal", source="Decrypt", url="u4",
              published_at=_iso(NOW - timedelta(hours=200)), detected=["TAO"])

    with st.connect() as conn:
        refresh_signal_catalyst_labels(conn, now=NOW, lookback_hours=48)

    sig, lab = _row(st, "sig_old")
    assert sig["news_supported"] == 0
    assert lab["catalyst_freshness"] == "none"


def test_additive_only_and_idempotent(tmp_path):
    """Already-true flags are never downgraded; re-running flips nothing new."""
    st = _store(tmp_path)
    # Signal already news_supported=1 but with NO matching news row in window.
    _add_signal(st, signal_id="sig_keep", symbol="ZEC/USDT",
                created_at=_iso(NOW - timedelta(hours=1)), news=1)
    with st.connect() as conn:
        refresh_signal_catalyst_labels(conn, now=NOW)
    sig, _ = _row(st, "sig_keep")
    assert sig["news_supported"] == 1, "must never downgrade 1->0"

    # Idempotency on a genuine flip.
    _add_signal(st, signal_id="sig_sui", symbol="SUI/USDT",
                created_at=_iso(NOW - timedelta(hours=1)), news=0)
    _add_news(st, title="SUI ecosystem upgrade", source="The Block", url="u5",
              published_at=_iso(NOW - timedelta(hours=2)), detected=["SUI"])
    with st.connect() as conn:
        s1 = refresh_signal_catalyst_labels(conn, now=NOW)
    with st.connect() as conn:
        s2 = refresh_signal_catalyst_labels(conn, now=NOW)
    assert s1.news_flips == 1
    assert s2.news_flips == 0, "second run must be a no-op for flags"


def test_labels_only_mode_does_not_touch_flags(tmp_path):
    st = _store(tmp_path)
    _add_signal(st, signal_id="sig_lo", symbol="XLM/USDT",
                created_at=_iso(NOW - timedelta(hours=1)), news=0)
    _add_news(st, title="XLM payment rail expansion", source="CoinDesk", url="u6",
              published_at=_iso(NOW - timedelta(hours=2)), detected=["XLM"])

    with st.connect() as conn:
        stats = refresh_signal_catalyst_labels(conn, now=NOW, update_flags=False)

    sig, lab = _row(st, "sig_lo")
    assert sig["news_supported"] == 0, "labels-only must not write the flag"
    assert stats.news_flips == 0
    # But the label cache still reflects the detected catalyst.
    assert lab is not None and lab["catalyst_freshness"] != "none"


def test_refresh_creates_runtime_indexes_for_large_news_tables(tmp_path):
    st = _store(tmp_path)
    _add_signal(st, signal_id="sig_idx", symbol="BTC/USDT",
                created_at=_iso(NOW - timedelta(minutes=5)), news=0)
    with st.connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS news_canonical_events("
            "news_item_id INTEGER PRIMARY KEY,effective_at TEXT,linkage_allowed INTEGER)"
        )
        refresh_signal_catalyst_labels(conn, now=NOW, days=1)
        canonical_indexes = {
            row["name"] for row in conn.execute("PRAGMA index_list(news_canonical_events)")
        }
        item_indexes = {
            row["name"] for row in conn.execute("PRAGMA index_list(news_items)")
        }
    assert "idx_news_canonical_effective_linkage" in canonical_indexes
    assert "idx_news_items_asset_published" in item_indexes


def test_refresh_records_completion_when_there_are_no_signals(tmp_path):
    st = _store(tmp_path)
    with st.connect() as conn:
        stats = refresh_signal_catalyst_labels(conn, now=NOW, days=1)
        row = conn.execute(
            "SELECT completed_at, scanned, labels_written "
            "FROM catalyst_label_refresh_runs ORDER BY id DESC LIMIT 1"
        ).fetchone()

    assert stats.scanned == 0
    assert tuple(row) == (_iso(NOW), 0, 0)
