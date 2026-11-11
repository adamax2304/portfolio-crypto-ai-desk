from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from xml.etree import ElementTree

from src.data_collectors.rss_news_collector import RSSNewsCollector
from src.models import NewsItem
from src.news import asset_registry, canonical_events, quality_gate
from src.signals.catalyst_label_refresh import direct_news_for_signal
from src.signals.config import SignalTrackingConfig
from src.signals.registry import register_ideas
from src.storage.sqlite import SQLiteStore


NOW = datetime(2026, 7, 13, 18, 0, tzinfo=timezone.utc)


def _store(tmp_path):
    store = SQLiteStore(tmp_path / "news.sqlite")
    store.init_db()
    return store


def test_common_ingest_resolves_and_materializes_immediately(tmp_path):
    store = _store(tmp_path)
    item = NewsItem(
        title="Hedera partners with a global payments firm",
        source="CoinDesk", url="https://example.test/hbar", published_at=NOW.isoformat(),
        available_at=NOW.isoformat(), content="Hedera announced a signed integration partnership.", importance=2.5,
    )
    assert store.save_news_items([item]) == 1
    with store.connect() as conn:
        news = conn.execute(
            "SELECT trusted_symbols_json,resolution_status,resolver_version FROM news_items"
        ).fetchone()
        event = conn.execute("SELECT * FROM news_canonical_events").fetchone()
    assert "HBAR" in {str(s).split("/")[0] for s in json.loads(news["trusted_symbols_json"])}
    assert news["resolution_status"] in {"resolver_added", "resolver_confirmed"}
    assert news["resolver_version"] == "entity_resolver_v8"
    assert event["event_type"] == "partnership"
    assert event["direction_hint"] == "bullish"
    assert event["linkage_allowed"] == 1
    assert event["content_level"] == "full_body"


def test_ingest_is_fail_open_when_incremental_pipeline_fails(tmp_path, monkeypatch):
    store = _store(tmp_path)
    import src.news.pipeline as pipeline
    monkeypatch.setattr(pipeline, "process_ingested_urls",
                        lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("boom")))
    item = NewsItem(title="Bitcoin market update", source="Reuters", url="https://x.test/fail",
                    published_at=NOW.isoformat())
    assert store.save_news_items([item]) == 1
    with store.connect() as conn:
        assert conn.execute("SELECT COUNT(*) FROM news_items").fetchone()[0] == 1


def test_structured_rows_use_same_incremental_path(tmp_path):
    store = _store(tmp_path)
    store.save_news_rows([{
        "title": "Tesla 8-K filing", "source": "SEC EDGAR", "url": "https://sec.test/tsla",
        "published_at": NOW.isoformat(), "detected_symbols_json": "[]", "importance": 3.0,
        "raw_json": {"ticker": "TSLA", "cik": "0001318605", "event_type": "filing",
                     "source_quality": "regulator"},
    }], asset_class="stocks")
    with store.connect() as conn:
        row = conn.execute("SELECT trusted_symbols_json,entity_match_source FROM news_items").fetchone()
        event = conn.execute("SELECT event_type,source_quality FROM news_canonical_events").fetchone()
    assert "TSLA" in json.loads(row["trusted_symbols_json"])
    assert "issuer_cik" in row["entity_match_source"]
    assert tuple(event) == ("sec_filing", "regulator")


def test_canonical_dedupe_prefers_non_social_and_corroborates(tmp_path):
    store = _store(tmp_path)
    items = [
        NewsItem(title="Hedera partners with Acme payments", source="t.me/crypto_news",
                 url="https://t.me/crypto_news/1", published_at=NOW.isoformat(),
                 content="Hedera announced its Acme partnership."),
        NewsItem(title="Hedera partners with Acme payments", source="Reuters",
                 url="https://reuters.test/hbar", published_at=(NOW + timedelta(minutes=2)).isoformat(),
                 content="Hedera and Acme confirmed a signed integration partnership."),
    ]
    store.save_news_items(items)
    with store.connect() as conn:
        rows = [dict(r) for r in conn.execute(
            "SELECT source,is_cluster_primary,corroboration_count,independent_non_social_count,"
            "linkage_allowed FROM news_canonical_events ORDER BY source")]
    assert len(rows) == 2
    assert {r["corroboration_count"] for r in rows} == {2}
    assert {r["independent_non_social_count"] for r in rows} == {1}
    assert next(r for r in rows if r["source"] == "Reuters")["is_cluster_primary"] == 1
    # The independent primary may drive linkage; the social copy remains
    # confidence-capped even though the cluster records its corroboration.
    assert next(r for r in rows if r["source"] == "Reuters")["linkage_allowed"] == 1
    assert next(r for r in rows if r["source"] == "t.me/crypto_news")["linkage_allowed"] == 0


def test_directional_contract_prevents_opposite_catalyst_boost(tmp_path):
    store = _store(tmp_path)
    store.save_news_items([NewsItem(
        title="Sui network exploit drains funds", source="CoinDesk", url="https://x.test/sui-hack",
        published_at=(NOW - timedelta(hours=1)).isoformat(),
        available_at=(NOW - timedelta(hours=1)).isoformat(),
        content="The Sui security team confirmed an exploit and paused contracts.",
    )])
    with store.connect() as conn:
        assert direct_news_for_signal(conn, "SUI/USDT", NOW.isoformat(), direction="long") is None
        short_hit = direct_news_for_signal(conn, "SUI/USDT", NOW.isoformat(), direction="short")
    assert short_hit and short_hit["direction_hint"] == "bearish"
    assert short_hit["canonical"] is True


def _apple_idea():
    from src.models import TradeIdea
    return TradeIdea(
        symbol="AAPL", direction="long", score=75, confidence="high", risk_level="medium",
        timeframe="15m/1h", tier="B", mode="intraday", asset_class="stocks",
        exchange_focus="US", exchanges_confirmed=["US"], data_confidence="high",
        thesis="Apple breakout", evidence=["structure"], counterarguments=["market risk"],
        entry_plan="pullback", invalidation="190", targets=["200"], what_to_monitor=["SPY"],
        avoid_conditions=[], data_sources_used=["news"],
        raw={"setup": {"entry_low": 195, "entry_high": 196, "invalidation": 190,
                       "tp1": 200, "tp2": 204, "tp3": 210}, "news_count": 3},
    )


def test_registration_uses_canonical_policy_not_broad_news_count(tmp_path, monkeypatch):
    monkeypatch.setattr("src.signals.registry._iso_now", lambda: NOW.isoformat())
    denied = _store(tmp_path / "denied")
    denied.save_news_items([NewsItem(
        title="Apple Inc unveils a new chip", source="Yahoo Finance",
        url="https://yahoo.test/aapl", published_at=NOW.isoformat(),
        available_at=NOW.isoformat(),
    )], asset_class="stocks")
    result = register_ideas(denied, [_apple_idea()], config=SignalTrackingConfig(),
                            report_id="denied", asset_class="stocks")
    with denied.connect() as conn:
        row = conn.execute("SELECT news_supported,raw_idea_json FROM proposed_signals").fetchone()
    assert result.inserted == 1 and row["news_supported"] == 0
    assert json.loads(row["raw_idea_json"])["news_influence_contract"]["source"] == \
        "no_eligible_canonical_event"

    allowed = _store(tmp_path / "allowed")
    allowed.save_news_items([NewsItem(
        title="Apple Inc unveils a new chip", source="Reuters",
        url="https://reuters.test/aapl", published_at=NOW.isoformat(),
        available_at=NOW.isoformat(),
        content="Apple Inc launched a new chip and detailed customer availability.",
    )], asset_class="stocks")
    result = register_ideas(allowed, [_apple_idea()], config=SignalTrackingConfig(),
                            report_id="allowed", asset_class="stocks")
    with allowed.connect() as conn:
        row = conn.execute("SELECT news_supported,raw_idea_json FROM proposed_signals").fetchone()
    assert result.inserted == 1 and row["news_supported"] == 1
    assert json.loads(row["raw_idea_json"])["news_influence_contract"]["source"] == "canonical_event"


def test_news_agent_uses_db_enrichment_and_splits_positive_from_risk(tmp_path):
    from src.agents.news_agent import NewsAgent
    from src.config import load_config
    from src.storage.file_store import FileStore

    store = _store(tmp_path)
    recent = datetime.now(timezone.utc).isoformat()
    store.save_news_items([
        NewsItem(title="Hedera partners with Acme", source="Reuters", url="https://x.test/hbar-pos",
                 published_at=recent, content="Hedera confirmed an integration partnership."),
        NewsItem(title="Sui network exploit drains funds", source="CoinDesk", url="https://x.test/sui-risk",
                 published_at=recent, content="The Sui security team confirmed the exploit."),
    ])
    rows = store.load_news_window(hours=48, limit=20, include_test_sources=True)
    agent = NewsAgent(load_config(), FileStore(load_config()), store)
    agent.save_output = lambda _payload: None
    output = agent.run(rows)
    assert output["canonical_policy_active"] is True
    assert "HBAR" in output["by_symbol"]
    assert "SUI" not in output["by_symbol"]
    assert "SUI" in output["risk_by_symbol"]
    # raw_json was written before resolver enrichment, so this proves the
    # authoritative DB symbols were not discarded during model restoration.
    assert output["by_symbol"]["HBAR"][0]["canonical_event"]["linkage_allowed"] == 1


def test_asset_registry_never_promotes_discovered_assets(tmp_path):
    db = str(tmp_path / "registry.sqlite")
    result = asset_registry.refresh(db=db, now=NOW)
    conn = sqlite3.connect(db)
    tracked = conn.execute(
        "SELECT status FROM news_asset_registry WHERE asset_key='crypto:BTC'").fetchone()
    bad = conn.execute(
        "SELECT COUNT(*) FROM news_asset_registry WHERE status NOT IN ('TRACKED','DISCOVERED')").fetchone()[0]
    conn.close()
    assert tracked and tracked[0] == "TRACKED"
    assert bad == 0
    assert result["counts"]["TRACKED"] > 0


def test_rss_prefers_content_encoded_over_short_description():
    xml = ElementTree.fromstring(
        "<item xmlns:content='http://purl.org/rss/1.0/modules/content/'>"
        "<description>Short headline</description>"
        "<content:encoded><![CDATA[Long full article body with issuer and catalyst details.]]></content:encoded>"
        "</item>"
    )
    body = RSSNewsCollector._rich_content(xml, ("encoded", "description", "content"))
    assert body == "Long full article body with issuer and catalyst details."


def test_gold_quality_cases_are_all_green():
    result = quality_gate.run_gold_cases()
    assert result["cases"] >= 20
    assert result["failed"] == 0, result["failures"]
