"""Tests for audit fix #5: stocks news minimum path.

Covers:
  - save_news_items honors asset_class kwarg (already shipped in Stage 1).
  - CompanyNewsAgent prefers stocks-tagged rows and falls back to cross-asset.
  - CompanyNewsAgent surfaces counters for stocks_tagged vs cross_asset.
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

import pytest

from src import config as _config_mod
from src.config import load_config
from src.models import NewsItem
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore
from src.stocks import load_stocks_config
from src.stocks.agents import CompanyNewsAgent


@pytest.fixture(autouse=True)
def _isolated_db(tmp_path, monkeypatch):
    """Test-isolation fix (2026-06-03): route every ``load_config()`` in this
    module to a fresh per-test temp SQLite DB so ``news_items`` starts EMPTY.

    Previously these tests ran against the live production DB
    (``db/crypto_ai_desk.sqlite``); once it grew past 500 news rows, a freshly
    inserted fixture fell outside ``load_recent_news(limit=500)`` and the
    assertions failed. With an isolated DB the test only ever sees its own
    rows. Pure fixture-level DI — no production code or data is touched.
    """
    db_file = tmp_path / "isolated_news.sqlite"

    def _patched_load_config(*args, **kwargs):
        cfg = _config_mod.load_config(*args, **kwargs)
        cfg.settings.setdefault("data", {})["db_path"] = str(db_file)
        return cfg

    monkeypatch.setattr(sys.modules[__name__], "load_config", _patched_load_config)
    yield


def _kit():
    config = load_config()
    scfg = load_stocks_config()
    fs = FileStore(config)
    db = SQLiteStore(config.db_path)
    db.init_db()
    return config, scfg, fs, db


def _insert_news(
    db: SQLiteStore,
    *,
    title: str,
    url: str,
    detected_symbols: list[str],
    asset_class: str,
    published_at: str | None = None,
) -> None:
    """Insert a single news row directly with the given asset_class. Uses
    save_news_items to exercise the production code path. Defaults to a FRESH published_at so the
    CompanyNewsAgent's 72h time-window loader keeps the row (was a fixed 2026-05-25 date)."""
    from datetime import datetime, timezone
    item = NewsItem(
        title=title,
        source="test_source",
        url=url,
        published_at=published_at or datetime.now(timezone.utc).isoformat(),
        detected_symbols=detected_symbols,
        detected_narratives=[],
        importance=2.0,
    )
    db.save_news_items([item], asset_class=asset_class)


def test_save_news_items_writes_asset_class(tmp_path):
    """Direct DB inspection: save_news_items(asset_class='stocks') persists 'stocks'."""
    config, scfg, fs, db = _kit()
    unique_url = "https://example.com/test-news-stocks-tag-fix"
    # Clean leftovers from any previous run.
    with sqlite3.connect(config.db_path) as conn:
        conn.execute("DELETE FROM news_items WHERE url = ?", (unique_url,))
    _insert_news(
        db,
        title="NVDA beats earnings",
        url=unique_url,
        detected_symbols=["NVDA"],
        asset_class="stocks",
    )
    with sqlite3.connect(config.db_path) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT asset_class, detected_symbols_json FROM news_items WHERE url = ?",
            (unique_url,),
        ).fetchone()
    assert row is not None
    assert row["asset_class"] == "stocks"
    detected = json.loads(row["detected_symbols_json"])
    assert "NVDA" in detected


def test_company_news_agent_prefers_stocks_tagged(monkeypatch):
    """Inserting a stocks-tagged hit should surface in has_catalyst.

    Production filter drops ``source='test_source'`` by default; this test
    flips ``CRYPTO_AI_DESK_INCLUDE_TEST_NEWS=1`` to keep the historical fixture
    visible to the agent.
    """
    monkeypatch.setenv("CRYPTO_AI_DESK_INCLUDE_TEST_NEWS", "1")
    config, scfg, fs, db = _kit()
    url = "https://example.com/news-stocks-tagged-aapl"
    with sqlite3.connect(config.db_path) as conn:
        conn.execute("DELETE FROM news_items WHERE url = ?", (url,))
    _insert_news(
        db,
        title="AAPL announces share buyback",
        url=url,
        detected_symbols=["AAPL"],
        asset_class="stocks",
    )

    agent = CompanyNewsAgent(config, scfg, fs, db)
    payload = agent.run(symbols=["AAPL"], lookback_limit=500)
    assert "AAPL" in payload["has_catalyst"]
    assert payload["counts"]["stocks_tagged"] >= 1


def test_company_news_agent_falls_back_to_crypto_tagged_when_symbol_matches(monkeypatch):
    """A crypto-tagged news row that mentions a stocks ticker (e.g. COIN
    in a CoinDesk story) should still surface for the stocks agent because
    the cross-asset gate is on by default."""
    monkeypatch.setenv("CRYPTO_AI_DESK_INCLUDE_TEST_NEWS", "1")
    config, scfg, fs, db = _kit()
    url = "https://example.com/news-crypto-tagged-coin"
    with sqlite3.connect(config.db_path) as conn:
        conn.execute("DELETE FROM news_items WHERE url = ?", (url,))
    _insert_news(
        db,
        title="Coinbase reports record revenue (COIN)",
        url=url,
        detected_symbols=["COIN"],
        asset_class="crypto",   # tagged crypto despite naming COIN
    )

    agent = CompanyNewsAgent(config, scfg, fs, db)
    payload = agent.run(symbols=["COIN"], lookback_limit=500, prefer_stocks_tagged=True)
    assert "COIN" in payload["has_catalyst"]
    assert payload["counts"]["cross_asset"] >= 1


def test_company_news_agent_can_strict_filter_stocks_only(monkeypatch):
    """When prefer_stocks_tagged=False, cross-asset rows are ignored."""
    monkeypatch.setenv("CRYPTO_AI_DESK_INCLUDE_TEST_NEWS", "1")
    config, scfg, fs, db = _kit()
    url = "https://example.com/news-crypto-tagged-strict-test"
    with sqlite3.connect(config.db_path) as conn:
        conn.execute("DELETE FROM news_items WHERE url = ?", (url,))
    _insert_news(
        db,
        title="MicroStrategy buys more (MSTR)",
        url=url,
        detected_symbols=["MSTR"],
        asset_class="crypto",
    )

    agent = CompanyNewsAgent(config, scfg, fs, db)
    payload = agent.run(symbols=["MSTR"], lookback_limit=500, prefer_stocks_tagged=False)
    # Strict mode: a crypto-tagged row alone is not enough.
    # If there happens to be a stocks-tagged MSTR row from a previous test
    # leftover, this test would fail — that's why we clean the URL above.
    # The assertion is "we did not count this cross-asset row," which we
    # verify via counts.
    assert payload["counts"]["cross_asset"] == 0


def test_test_source_filter_drops_by_default(tmp_path):
    """QA Fix #2 regression: the default load_recent_news must drop
    ``source='test_source'`` rows so they never leak into production
    reports."""
    config, scfg, fs, db = _kit()
    url = "https://example.com/qa-fix-2-test-source-filter"
    with sqlite3.connect(config.db_path) as conn:
        conn.execute("DELETE FROM news_items WHERE url = ?", (url,))
    _insert_news(
        db,
        title="QA fix #2 fake AAPL fixture",
        url=url,
        detected_symbols=["AAPL"],
        asset_class="stocks",
    )

    # Default behaviour (no env, no kwarg): test_source row is excluded.
    rows = db.load_recent_news(limit=500)
    assert not any(r.get("url") == url for r in rows), (
        "test_source row leaked into default load_recent_news"
    )

    # Opt-in: the row reappears.
    rows_opt_in = db.load_recent_news(limit=500, include_test_sources=True)
    assert any(r.get("url") == url for r in rows_opt_in)


def test_load_recent_news_asset_class_filter(tmp_path):
    """QA Fix #2 regression: asset_class filter excludes stocks rows from
    crypto-scoped loads and vice versa."""
    config, scfg, fs, db = _kit()
    url = "https://example.com/qa-fix-2-asset-class-filter"
    with sqlite3.connect(config.db_path) as conn:
        conn.execute("DELETE FROM news_items WHERE url = ?", (url,))
    # Insert with asset_class=stocks but with a NON-test source so the
    # test_source filter does not also drop it.
    item = NewsItem(
        title="QA Fix #2 real-looking stocks news",
        source="Reuters",
        url=url,
        published_at="2026-05-25T12:00:00+00:00",
        detected_symbols=["AAPL"],
        detected_narratives=[],
        importance=2.0,
    )
    db.save_news_items([item], asset_class="stocks")

    # Crypto scope must NOT see the stocks row.
    crypto_rows = db.load_recent_news(limit=500, asset_class="crypto")
    assert not any(r.get("url") == url for r in crypto_rows)

    # Stocks scope must see it.
    stocks_rows = db.load_recent_news(limit=500, asset_class="stocks")
    assert any(r.get("url") == url for r in stocks_rows)
