from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

from src.models import NewsItem
from src.news import canonical_events, fast_news
from src.news.freshness import (
    AVAILABILITY_UNKNOWN,
    CONTINUATION_EVENT,
    FAST_EVENT,
    THESIS_EVENT,
    classify_observation,
)
from src.signals.catalyst_label_refresh import direct_news_for_signal
from src.storage.sqlite import SQLiteStore


def test_observation_class_uses_when_the_desk_saw_the_news():
    ref = datetime(2026, 7, 26, 12, tzinfo=timezone.utc)
    assert classify_observation((ref - timedelta(minutes=8)).isoformat(), ref.isoformat()).event_latency_class == FAST_EVENT
    assert classify_observation((ref - timedelta(hours=2)).isoformat(), ref.isoformat()).event_latency_class == CONTINUATION_EVENT
    assert classify_observation((ref - timedelta(days=2)).isoformat(), ref.isoformat()).event_latency_class == THESIS_EVENT
    assert classify_observation(None, ref.isoformat()).event_latency_class == AVAILABILITY_UNKNOWN


def test_save_preserves_first_availability_and_canonical_effective_time(tmp_path: Path):
    db = tmp_path / "news.sqlite"
    store = SQLiteStore(db)
    store.init_db()
    early = "2026-07-26T12:00:00+00:00"
    store.save_news_items([
        NewsItem(title="Apple wins a major contract", source="Fast test", url="https://test/1",
                 published_at="2026-07-26T11:58:00+00:00", available_at=early,
                 detected_symbols=["AAPL"]),
    ], asset_class="stocks")
    assert store.save_news_items([
        NewsItem(title="Apple wins a major contract", source="Fast test", url="https://test/1",
                 published_at="2026-07-26T11:58:00+00:00", available_at="2026-07-26T13:00:00+00:00",
                 detected_symbols=["AAPL"]),
    ], asset_class="stocks") == 0
    canonical_events.refresh(db=str(db), urls=["https://test/1"],
                             now=datetime(2026, 7, 26, 12, 5, tzinfo=timezone.utc))
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        item = conn.execute("SELECT available_at,event_latency_class FROM news_items").fetchone()
        event = conn.execute("SELECT available_at,effective_at,event_latency_class FROM news_canonical_events").fetchone()
    assert dict(item) == {"available_at": early, "event_latency_class": FAST_EVENT}
    assert dict(event) == {"available_at": early, "effective_at": early, "event_latency_class": FAST_EVENT}


def test_news_write_retries_a_short_sqlite_lock(monkeypatch, tmp_path: Path):
    db = tmp_path / "news.sqlite"
    store = SQLiteStore(db)
    store.init_db()
    original = store._save_news_items_once
    attempts = {"n": 0}

    def transient_lock(items, *, asset_class):
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise sqlite3.OperationalError("database is locked")
        return original(items, asset_class=asset_class)

    monkeypatch.setattr(store, "_save_news_items_once", transient_lock)
    monkeypatch.setattr("src.storage.sqlite.time.sleep", lambda _seconds: None)
    saved = store.save_news_items([
        NewsItem(title="Retry-safe news", source="test", url="https://test/retry",
                 published_at="2026-07-26T12:00:00+00:00", available_at="2026-07-26T12:01:00+00:00"),
    ])
    assert saved == 1
    assert attempts["n"] == 3


def test_catalyst_requires_point_in_time_visibility_and_horizon_compatibility(tmp_path: Path):
    db = tmp_path / "news.sqlite"
    store = SQLiteStore(db)
    store.init_db()
    visible_at = datetime(2026, 7, 26, 12, tzinfo=timezone.utc)
    store.save_news_items([
        NewsItem(title="Apple Inc unveils a new chip", source="Reuters", url="https://test/aapl",
                 published_at=(visible_at - timedelta(minutes=11)).isoformat(),
                 available_at=visible_at.isoformat(),
                 content="Apple Inc launched a new chip and detailed customer availability."),
    ], asset_class="stocks")
    with store.connect() as conn:
        assert direct_news_for_signal(
            conn, "AAPL", (visible_at - timedelta(seconds=1)).isoformat(), asset_class="stocks",
            direction="long", mode="intraday",
        ) is None
        assert direct_news_for_signal(
            conn, "AAPL", visible_at.isoformat(), asset_class="stocks", direction="long", mode="scalp",
        ) is None
        assert direct_news_for_signal(
            conn, "AAPL", visible_at.isoformat(), asset_class="stocks", direction="long", mode="intraday",
        )["event_latency_class"] == CONTINUATION_EVENT
        assert direct_news_for_signal(
            conn, "AAPL", visible_at.isoformat(), asset_class="stocks", direction="long", mode="swing",
        )["event_latency_class"] == CONTINUATION_EVENT


class _Response:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class _Session:
    def __init__(self, published_unix: int):
        self.published_unix = published_unix
        self.calls = []

    def get(self, url, *, params, headers, timeout):
        self.calls.append((url, params, headers, timeout))
        if url.endswith("/news"):
            return _Response([{
                "id": 1, "headline": "Apple wins a major contract", "summary": "Detailed source text",
                "datetime": self.published_unix, "related": "AAPL", "url": "https://provider/market-1",
            }])
        return _Response([{
            "id": 2, "headline": "Apple product launch", "summary": "Company article",
            "datetime": self.published_unix, "related": "AAPL", "url": "https://provider/company-1",
        }])


def test_finnhub_refresh_writes_point_in_time_rows_only(monkeypatch, tmp_path: Path):
    db = tmp_path / "news.sqlite"
    SQLiteStore(db).init_db()
    ref = datetime(2026, 7, 26, 12, tzinfo=timezone.utc)
    monkeypatch.setenv("FINNHUB_API_KEY", "test-key")
    monkeypatch.setattr(fast_news, "load_config", lambda: SimpleNamespace(db_path=db))
    monkeypatch.setattr(fast_news, "_next_company_symbols", lambda *_args, **_kwargs: ["AAPL"])
    monkeypatch.setattr(fast_news, "_load_settings", lambda: {
        "enabled": True, "request_timeout_seconds": 1,
        "finnhub": {"enabled": True, "key_env": "FINNHUB_API_KEY", "base_url": "https://test/api",
                    "global_category": "general", "global_limit": 10, "company_symbols_per_tick": 1,
                    "company_lookback_days": 1, "max_company_items_per_symbol": 10},
    })
    session = _Session(int((ref - timedelta(minutes=4)).timestamp()))
    result = fast_news.refresh(now=ref, session=session)
    assert result["market"]["saved"] == 1
    assert result["company"]["saved"] == 1
    assert "test-key" not in str(result)
    with sqlite3.connect(db) as conn:
        rows = conn.execute(
            "SELECT source,event_latency_class,available_at,raw_json FROM news_items ORDER BY source"
        ).fetchall()
        assert {row[0] for row in rows} == {fast_news.FINNHUB_MARKET_SOURCE, fast_news.FINNHUB_COMPANY_SOURCE}
        assert {row[1] for row in rows} == {FAST_EVENT}
        assert {row[2] for row in rows} == {ref.isoformat()}
        company_raw = json.loads(next(
            row[3] for row in rows if row[0] == fast_news.FINNHUB_COMPANY_SOURCE
        ))
        assert company_raw["provider_symbols"] == ["AAPL"]
        assert company_raw["provider_symbol_provenance"] == "finnhub_company_query"
        assert conn.execute("SELECT COUNT(*) FROM proposed_signals").fetchone()[0] == 0
        assert conn.execute("SELECT COUNT(*) FROM signal_outcomes").fetchone()[0] == 0


def test_fast_refresh_reports_the_selected_rss_lane(monkeypatch, tmp_path: Path):
    db = tmp_path / "news.sqlite"
    SQLiteStore(db).init_db()
    ref = datetime(2026, 7, 26, 12, tzinfo=timezone.utc)
    monkeypatch.setenv("FINNHUB_API_KEY", "test-key")
    monkeypatch.setattr(fast_news, "load_config", lambda: SimpleNamespace(db_path=db))
    monkeypatch.setattr(fast_news, "_next_company_symbols", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(fast_news, "_refresh_fast_rss", lambda *_args, **_kwargs: {
        "status": "ok", "sources": ["Benzinga Movers"], "seen": 2, "failed": [],
    })
    monkeypatch.setattr(fast_news, "_load_settings", lambda: {
        "enabled": True, "request_timeout_seconds": 1, "fast_rss_sources": ["Benzinga Movers"],
        "finnhub": {"enabled": True, "key_env": "FINNHUB_API_KEY", "base_url": "https://test/api",
                    "global_category": "general", "global_limit": 1, "company_symbols_per_tick": 0,
                    "company_lookback_days": 1, "max_company_items_per_symbol": 1},
    })
    result = fast_news.refresh(now=ref, session=_Session(int(ref.timestamp())))
    assert result["rss"] == {"status": "ok", "sources": ["Benzinga Movers"], "seen": 2, "failed": []}
