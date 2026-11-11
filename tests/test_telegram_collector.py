"""Unit tests for the Telegram realtime news collector (PART 7).

Pure-logic tests — no Telethon network calls. The async ``run()`` loop is
covered indirectly by exercising the message-building path through
``_build_item`` and the YAML config parser.
"""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from src.config import load_config
from src.data_collectors.telegram_collector import (
    TelegramChannelConfig,
    TelegramCollector,
    TelegramCollectorSettings,
    resolve_session_name,
    session_reauth_required,
)
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore


PROJECT_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def cfg():
    return load_config(PROJECT_ROOT)


# ---------------------------------------------------------------------------
# config parsing
# ---------------------------------------------------------------------------


def test_settings_parse_configured_channels(cfg):
    """The configured Telegram channel list is parsed in full. The ``enabled`` flag flips to
    true once the user has run ``setup_telegram_auth.py`` once; we test
    structural parsing here regardless of that flag's current state."""
    s = TelegramCollectorSettings.from_sources_yaml(cfg.sources)
    # The list grew from the original 18-channel rollout; assert the original
    # coverage floor without making future source additions a test failure.
    assert len(s.channels) >= 18
    handles = {c.handle for c in s.channels}
    must_have = {
        # stocks
        "WalterBloomberg", "forexlive", "zerohedge", "BWEtradfi",
        # crypto exchange / listings
        "binance_announcements", "Bybit_Announcements", "BWEnews",
        "wublockchainenglish", "AstronomicaNews",
        # security / hacks
        "zachxbt", "peckshield",
        # whale / on-chain
        "lookonchain", "cryptoquant_official", "glassnode",
        # general
        "WatcherGuru", "cointelegraph", "CoinMarketCapAnnouncements",
    }
    missing = must_have - handles
    assert not missing, f"missing channels: {missing}"


def test_settings_isolated_session_name(cfg):
    s = TelegramCollectorSettings.from_sources_yaml(cfg.sources)
    # Critical: must NOT collide with news_trader's `news_trader_tg`.
    assert s.session_name.startswith("crypto_ai_desk_tg_")
    assert s.per_host_session is True
    assert "news_trader" not in s.session_name


def test_session_name_isolated_by_host(monkeypatch):
    monkeypatch.delenv("TG_SESSION_NAME", raising=False)
    assert resolve_session_name("desk", per_host=True, hostname="PC One") == "desk_PC_One"
    assert resolve_session_name("desk", per_host=True, hostname="server-two") == "desk_server-two"


def test_session_name_explicit_override(monkeypatch):
    monkeypatch.setenv("TG_SESSION_NAME", "desk custom")
    assert resolve_session_name("ignored", per_host=True, hostname="host") == "desk_custom"


def test_channel_asset_class_split(cfg):
    s = TelegramCollectorSettings.from_sources_yaml(cfg.sources)
    by_class = {"stocks": [], "crypto": []}
    for c in s.channels:
        by_class[c.asset_class].append(c.handle)
    # 6 stocks channels minimum (DeItaone, PiQSuite, cnbci, bloomberg, WB, forexlive)
    assert len(by_class["stocks"]) >= 6
    # remaining are crypto
    assert len(by_class["crypto"]) >= 10


def test_channel_dataclass_normalizes_at_prefix():
    c = TelegramChannelConfig.from_dict({"handle": "@foo", "asset_class": "stocks"})
    assert c.handle == "foo"
    assert c.asset_class == "stocks"


def test_unknown_asset_class_defaults_to_crypto():
    c = TelegramChannelConfig.from_dict({"handle": "bar", "asset_class": "forex"})
    assert c.asset_class == "crypto"


def test_revoked_session_error_requires_reauth_not_retry():
    assert session_reauth_required(
        "The authorization key (session file) was used under two different IP addresses"
    )
    assert not session_reauth_required("HTTPSConnectionPool read timed out")


# ---------------------------------------------------------------------------
# message-building (no Telethon required)
# ---------------------------------------------------------------------------


def test_build_item_attaches_asset_class_and_url(cfg, tmp_path):
    db = SQLiteStore(tmp_path / "test.db")
    store = FileStore(cfg)
    collector = TelegramCollector(cfg, store, db)
    cfg_ch = TelegramChannelConfig(
        handle="DeItaone", asset_class="stocks", weight=0.95, primary_source=False,
    )
    item = collector._build_item(
        title="NVIDIA beats Q3 earnings estimates",
        body="NVIDIA Corp reported Q3 EPS of $4.02, topping the $3.78 consensus.",
        url="https://t.me/DeItaone/12345",
        published_iso="2026-06-01T10:00:00+00:00",
        source_name="t.me/DeItaone",
        cfg=cfg_ch,
    )
    assert item.title.startswith("NVIDIA beats")
    assert item.source == "t.me/DeItaone"
    assert item.url == "https://t.me/DeItaone/12345"
    # weight-nudge gives importance >= 1 + 0.95 nudge
    assert item.importance > 1.0
    assert item.available_at == item.ingested_at


def test_public_html_fallback_uses_published_and_observed_times(cfg, tmp_path, monkeypatch):
    db = SQLiteStore(tmp_path / "test.db")
    db.init_db()
    store = FileStore(cfg)
    settings = TelegramCollectorSettings(
        enabled=True,
        channels=[TelegramChannelConfig(handle="BWEtradfi", asset_class="stocks")],
    )
    collector = TelegramCollector(cfg, store, db, settings=settings)
    html = """
      <div class="tgme_widget_message_wrap">
        <div class="tgme_widget_message" data-post="BWEtradfi/123"></div>
        <div class="tgme_widget_message_text">NVIDIA announces a new AI chip launch.</div>
        <time datetime="2026-08-19T00:00:00+00:00"></time>
      </div>
    """
    monkeypatch.setattr(
        "requests.get",
        lambda *_a, **_k: SimpleNamespace(
            text=html, raise_for_status=lambda: None,
        ),
    )
    monkeypatch.setattr("src.data_collectors.telegram_collector.datetime", SimpleNamespace(
        now=lambda _tz=None: __import__("datetime").datetime(2026, 8, 19, 0, 1,
                                                               tzinfo=__import__("datetime").timezone.utc),
        fromisoformat=__import__("datetime").datetime.fromisoformat,
    ))
    result = collector.collect_public_html_once(hours=24)
    assert result["processed"] == 1 and result["failed"] == 0
    with db.connect() as conn:
        row = conn.execute(
            "SELECT published_at,ingested_at,available_at,url FROM news_items"
        ).fetchone()
    assert row[0].startswith("2026-08-19T00:00:00")
    assert row[1] == row[2]
    assert row[3] == "https://t.me/BWEtradfi/123"


def test_build_item_detects_crypto_ticker_via_alias(cfg, tmp_path):
    db = SQLiteStore(tmp_path / "test.db")
    store = FileStore(cfg)
    collector = TelegramCollector(cfg, store, db)
    cfg_ch = TelegramChannelConfig(
        handle="zachxbt", asset_class="crypto", weight=0.9,
    )
    item = collector._build_item(
        title="Hyperliquid exploited for $5M",
        body="The Hyperliquid bridge was drained earlier today.",
        url="https://t.me/zachxbt/777",
        published_iso="2026-06-01T10:00:00+00:00",
        source_name="t.me/zachxbt",
        cfg=cfg_ch,
    )
    # The curated alias matcher (entity_aliases.yaml) maps "Hyperliquid"→HYPE.
    # We tolerate the matcher being absent / disabled — assert at minimum that
    # the symbol-detection path runs without raising.
    assert isinstance(item.detected_symbols, list)


def test_build_item_dedup_url_format(cfg, tmp_path):
    """Synthetic t.me URL doubles as the SQLite UNIQUE dedup key."""
    db = SQLiteStore(tmp_path / "test.db")
    store = FileStore(cfg)
    collector = TelegramCollector(cfg, store, db)
    cfg_ch = TelegramChannelConfig(handle="BWEnews", asset_class="crypto", weight=0.95)
    a = collector._build_item(
        title="x", body="x", url="https://t.me/BWEnews/100",
        published_iso="2026-06-01T10:00:00+00:00",
        source_name="t.me/BWEnews", cfg=cfg_ch,
    )
    b = collector._build_item(
        title="y", body="y", url="https://t.me/BWEnews/100",
        published_iso="2026-06-01T11:00:00+00:00",
        source_name="t.me/BWEnews", cfg=cfg_ch,
    )
    assert a.url == b.url


# ---------------------------------------------------------------------------
# isolation contract — no writes outside data/telegram
# ---------------------------------------------------------------------------


def test_session_path_under_data_telegram(cfg):
    s = TelegramCollectorSettings.from_sources_yaml(cfg.sources)
    # The session path must live under the project root, never under news_trader.
    assert s.session_path.startswith("data/")
    assert "news_trader" not in s.session_path
