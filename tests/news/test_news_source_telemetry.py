"""News ingest metadata, macro boundaries, and alert-transition tests."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import requests

from src.data_collectors.rss_news_collector import RSSNewsCollector
from src.config import load_config
from src.models import NewsItem
from src.news import entity_resolver, source_health, source_telemetry
from src.storage.sqlite import SQLiteStore


def test_rss_body_is_persisted_for_future_entity_resolution(tmp_path):
    db_path = Path(tmp_path) / "news.sqlite"
    store = SQLiteStore(db_path)
    store.init_db()
    collector = RSSNewsCollector(load_config(), None, store)  # FileStore is not used by _build_item
    item = collector._build_item(
        "Company update",
        "https://example.test/company-update",
        "2026-07-13T10:00:00+00:00",
        "Test RSS",
        False,
        "Apple Inc. (AAPL) reported stronger revenue and guidance.",
        "stocks",
    )
    store.save_news_items([item], asset_class="stocks")
    conn = sqlite3.connect(db_path)
    row = conn.execute("SELECT content_text, raw_json, content_hash FROM news_items").fetchone()
    conn.close()
    assert row and "Apple Inc." in row[0] and row[2]
    assert "Apple Inc." in json.loads(row[1])["content"]
    fields = entity_resolver.extract_text_fields({"title": item.title, "raw_json": row[1]})
    assert "Apple Inc." in fields["combined"]


def test_macro_tags_use_boundaries_not_substrings():
    assert "war" not in entity_resolver._macro_event_tags("Warsh says the Fed may hold rates")
    assert "war" not in entity_resolver._macro_event_tags("Awards and rewards rise")
    assert "war" in entity_resolver._macro_event_tags("War escalates after a missile strike")
    assert "exchange:coinbase" in entity_resolver._exchange_stablecoin_tags("Coinbase lists USDC")
    assert "stablecoin:USDC" in entity_resolver._exchange_stablecoin_tags("Coinbase lists USDC")


def test_source_telemetry_is_persisted_and_alerts_are_transition_deduped(monkeypatch, tmp_path):
    db = Path(tmp_path) / "telemetry.sqlite"
    source_telemetry.record_source_run(
        source_name="CNBC Markets", source_type="rss", status="ok", item_count=4,
        db=db, write_journal=False,
    )
    assert source_telemetry.latest_runs(db)["rss:CNBC Markets"]["item_count"] == 4

    state = {"status": "ERROR"}
    calls: list[str] = []

    def health(_db, now=None):
        return {
            "summary": {"ok": 0, "error": 1, "stale": 0, "dead": 0},
            "sources": [{
                "source": "CNBC Markets", "source_type": "rss", "enabled": True,
                "stale_status": state["status"], "rows_24h": 0, "rows_72h": 0,
                "warnings": ["latest transport timeout"],
            }],
        }

    class FakeNotifier:
        enabled = True
        chat_id = "123"

        def send(self, message, parse_mode="Markdown"):
            calls.append(message)
            return {"ok": True}

    monkeypatch.setattr(source_health, "compute_source_health", health)
    monkeypatch.setattr(source_telemetry, "_notifier_for", lambda _root: FakeNotifier())
    first = source_telemetry.monitor(db=db, root=Path(tmp_path), send_telegram=True)
    second = source_telemetry.monitor(db=db, root=Path(tmp_path), send_telegram=True)
    assert first["alerts_sent"] == ["rss:CNBC Markets"]
    assert second["alerts_sent"] == []
    assert len(calls) == 1

    state["status"] = "OK"
    recovered = source_telemetry.monitor(db=db, root=Path(tmp_path), send_telegram=True)
    assert recovered["alerts_sent"] == ["rss:CNBC Markets"]
    assert "RECOVERED" in calls[-1]
    journal = Path(tmp_path) / "data" / "diagnostics" / "news_source_errors.jsonl"
    records = [json.loads(line) for line in journal.read_text(encoding="utf-8").splitlines()]
    assert [r["status"] for r in records] == ["ERROR", "recovered"]


def test_source_health_distinguishes_transport_error_from_quiet_feed(tmp_path):
    db = Path(tmp_path) / "health.sqlite"
    SQLiteStore(db).init_db()
    source_telemetry.record_source_run(
        source_name="CNBC Markets", source_type="rss", status="timeout",
        error_code="ReadTimeout", error_message="timed out", db=db, write_journal=False,
    )
    health = source_health.compute_source_health(str(db))
    cnbc = next(row for row in health["sources"] if row["source"] == "CNBC Markets")
    assert cnbc["stale_status"] == "ERROR"
    assert cnbc["last_fetch_status"] == "timeout"


def test_redundant_cryptoslate_timeout_is_degraded_while_its_publications_are_fresh(tmp_path):
    db = Path(tmp_path) / "cryptoslate-health.sqlite"
    store = SQLiteStore(db)
    store.init_db()
    item = NewsItem(
        title="Fresh crypto market update",
        url="https://cryptoslate.com/example",
        source="CryptoSlate",
        published_at=datetime.now(timezone.utc).isoformat(),
        detected_symbols=["BTC"],
    )
    store.save_news_items([item], asset_class="crypto")
    source_telemetry.record_source_run(
        source_name="CryptoSlate", source_type="rss", status="timeout",
        error_code="ReadTimeout", error_message="timed out", db=db, write_journal=False,
    )
    health = source_health.compute_source_health(str(db))
    row = next(value for value in health["sources"] if value["source"] == "CryptoSlate")
    assert row["stale_status"] == "DEGRADED"
    assert health["summary"]["degraded"] >= 1
    assert health["summary"]["error"] == 0


def test_configured_primary_grace_keeps_fresh_pr_wire_failure_degraded(tmp_path):
    db = Path(tmp_path) / "pr-wire-health.sqlite"
    store = SQLiteStore(db)
    store.init_db()
    store.save_news_items([NewsItem(
        title="Issuer publishes quarterly results",
        url="https://www.prnewswire.com/example",
        source="PR Newswire (Stocks)",
        published_at=datetime.now(timezone.utc).isoformat(),
        detected_symbols=["IBM"],
    )], asset_class="stocks")
    source_telemetry.record_source_run(
        source_name="PR Newswire (Stocks)", source_type="rss", status="error",
        error_code="ParseError", error_message="malformed XML", db=db, write_journal=False,
    )
    health = source_health.compute_source_health(str(db))
    row = next(value for value in health["sources"] if value["source"] == "PR Newswire (Stocks)")
    assert row["stale_status"] == "DEGRADED"
    assert "PR Newswire (Stocks)" not in health["summary"]["error_primary"]


def test_cryptoslate_uses_source_specific_retry_budget_and_backoff(monkeypatch):
    cfg = SimpleNamespace(
        symbols=[], watchlist={"narratives": {}}, root=Path("."),
        sources={"rss_feeds": [{
            "name": "CryptoSlate", "url": "https://cryptoslate.com/feed/",
            "asset_class": "crypto", "retry_attempts": 3,
            "request_timeout_seconds": 12, "retry_backoff_seconds": 1,
        }]},
    )

    class Db:
        def save_news_items(self, items, asset_class="crypto"):
            self.items = list(items)

    class Response:
        apparent_encoding = "utf-8"
        status_code = 200
        text = (
            "<rss><channel><item><title>Bitcoin update</title>"
            "<link>https://cryptoslate.com/retry-ok</link>"
            "<pubDate>Tue, 04 Aug 2026 18:00:00 GMT</pubDate>"
            "</item></channel></rss>"
        )

        def raise_for_status(self):
            return None

    calls = []
    sleeps = []
    telemetry = []

    def get(_url, *, timeout, headers):
        calls.append((timeout, headers["User-Agent"]))
        if len(calls) < 3:
            raise requests.exceptions.ReadTimeout("temporary")
        return Response()

    monkeypatch.setattr(RSSNewsCollector, "_load_stocks_tickers", lambda _self: [])
    monkeypatch.setattr("src.data_collectors.rss_news_collector.requests.get", get)
    monkeypatch.setattr("src.data_collectors.rss_news_collector.time.sleep", sleeps.append)
    monkeypatch.setattr(
        "src.data_collectors.rss_news_collector.record_source_run",
        lambda **kwargs: telemetry.append(kwargs),
    )
    db = Db()
    result = RSSNewsCollector(cfg, None, db).fetch(write_snapshot=False)
    assert result.failed_sources == {}
    assert len(calls) == 3
    assert [value[0] for value in calls] == [12.0, 12.0, 12.0]
    assert sleeps == [1.0, 2.0]
    assert telemetry[-1]["status"] == "ok"
    assert telemetry[-1]["metadata"]["attempts"] == 3
