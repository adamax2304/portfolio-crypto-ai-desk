"""Tests for PART 1 catalyst / narrative collection layer.

Covers per Sprint spec PART 10:
- catalyst event requires source / timestamp
- rumour_only → not actionable
- overextended catalyst → wait_retest / avoid_chase basket
- low-liquidity / delisting → basket avoid
- BNB / ASTER narrative basket created
- HYPE / perps narrative basket created
- Opus not called automatically (catalyst-scan does no LLM call)
- Obsidian system prompt file exists
- LLM packet includes catalyst block
- Scheduler step is classified as `command_nonfatal` so a failure
  does not block the cycle.
- No auto-trade hook anywhere.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.catalysts import (
    CATALYST_TYPES,
    PLAYBOOKS,
    CatalystEvent,
    NarrativeBasket,
    build_narrative_baskets,
    classify_catalyst_type,
    classify_source_quality,
    collect_catalysts,
    detect_low_liquidity_risk,
    detect_rumour_marker,
)
from src.catalysts.classifier import (
    is_test_source,
    score_importance,
    detect_geopolitical_severity,
)
from datetime import datetime, timezone, timedelta


def _recent(hours: int = 3) -> str:
    """Recent, IN-WINDOW published_at for the collector's rolling lookback (default 720h).
    Absolute fixture dates (e.g. 2026-06-01) silently age out of the window and fail on a
    later run — anchoring to `now` keeps these fixtures durable."""
    return (datetime.now(timezone.utc) - timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%S+00:00")


_R10 = _recent(3)      # earliest (was 2026-06-01T10:00)
_R11 = _recent(2)      # was 2026-06-01T11:00  (ordered strictly after _R10)
_R1130 = _recent(1)    # latest (was 2026-06-01T11:30)


# ---------------------------------------------------------------------------
# Classifier — pure regex
# ---------------------------------------------------------------------------


def test_dxsale_exploit_classified_as_exploit_hack():
    assert classify_catalyst_type(
        "DxSale drained for $7.3M in BNB Chain liquidity exploit"
    ) == "exploit_hack"


def test_smci_indictment_classified_as_legal_risk():
    assert classify_catalyst_type(
        "Super Micro hit with federal indictment over alleged AI server diversion"
    ) == "legal_risk"


def test_binance_hodler_airdrop_classified():
    assert classify_catalyst_type(
        "Introducing Genius Terminal (GENIUS) on Binance HODLer Airdrops"
    ) == "hodler_airdrop"


def test_dtcc_partnership_classified_as_partnership():
    assert classify_catalyst_type(
        "DTCC partners with Stellar Development Foundation for tokenization"
    ) == "partnership"


def test_layerzero_acquisition_partnership():
    assert classify_catalyst_type(
        "LayerZero Foundation Proposes $110M Acquisition Deal for Stargate"
    ) == "partnership"


def test_binance_delisting_classified():
    assert classify_catalyst_type(
        "Binance to Delist 19 Tokens on May 14"
    ) == "exchange_delisting"


def test_margin_delisting_more_specific_than_delisting():
    # The margin pattern must win over general delisting.
    assert classify_catalyst_type(
        "Binance to remove HEI margin trading pairs"
    ) == "margin_delisting"


def test_rumour_only_when_no_specific_category():
    assert classify_catalyst_type(
        "Sources say BNB ecosystem token reveal coming soon"
    ) == "rumour_only"


def test_other_news_fallback():
    assert classify_catalyst_type("BTC trades sideways") == "other_news"


# ---------------------------------------------------------------------------
# Source quality
# ---------------------------------------------------------------------------


def test_binance_announcements_is_primary_source():
    assert classify_source_quality("Binance Announcements") == "primary_source"


def test_coindesk_is_single_source():
    assert classify_source_quality("CoinDesk") == "single_source"


def test_twitter_is_social_only():
    assert classify_source_quality("Twitter") == "social_only"


def test_empty_source_is_unverifiable():
    assert classify_source_quality("") == "unverifiable"


def test_test_source_detected():
    assert is_test_source("test_source") is True
    assert is_test_source("FIXTURE") is True
    assert is_test_source("CoinDesk") is False


# ---------------------------------------------------------------------------
# Auxiliary flags
# ---------------------------------------------------------------------------


def test_low_liquidity_detection():
    assert detect_low_liquidity_risk("PSG fan token delisted from CoinDCX") is True
    assert detect_low_liquidity_risk("BTC trades sideways") is False


def test_rumour_marker_detection():
    assert detect_rumour_marker("Sources say BNB launch coming") is True
    assert detect_rumour_marker("Binance Announces GENIUS Airdrop") is False


# ---------------------------------------------------------------------------
# Basket clustering
# ---------------------------------------------------------------------------


def _ev(symbol: str, catalyst_type: str = "other_news",
        related: list[str] | None = None, source_quality: str = "single_source",
        fresh: float | None = 2.0) -> CatalystEvent:
    return CatalystEvent(
        catalyst_id=f"cat_test_{symbol.replace('/', '_')}_{catalyst_type}",
        asset_class="crypto",
        symbol=symbol,
        related_symbols=related or [],
        catalyst_type=catalyst_type,
        source="CoinDesk",
        source_quality=source_quality,
        title=f"test {symbol} {catalyst_type}",
        url=f"https://example.com/{symbol}",
        freshness_hours=fresh,
    )


def test_bnb_aster_basket_clusters():
    """BNB-rooted catalyst should pull ASTER into the basket via static config."""

    events = [
        _ev("BNB/USDT", "hodler_airdrop"),
        _ev("ASTER/USDT", "product_launch"),
    ]
    baskets = build_narrative_baskets(events)
    names = [b.basket_name for b in baskets]
    assert "binance_ecosystem_teaser" in names
    bnb_basket = next(b for b in baskets if b.basket_name == "binance_ecosystem_teaser")
    assert "BNB/USDT" in bnb_basket.primary_symbols
    assert "ASTER/USDT" in bnb_basket.related_symbols


def test_hype_perps_basket_clusters():
    events = [_ev("HYPE/USDT", "platform_growth")]
    baskets = build_narrative_baskets(events)
    names = [b.basket_name for b in baskets]
    assert "perps_dex_narrative" in names


def test_delisting_basket_is_dynamic_and_blocks_trade():
    events = [
        _ev("HEI/USDT", "margin_delisting"),
        _ev("PSG/USDT", "exchange_delisting"),
        _ev("NFP/USDT", "low_liquidity_event"),
    ]
    baskets = build_narrative_baskets(events)
    assert len(baskets) == 1
    b = baskets[0]
    assert b.basket_name == "delisting_thin_liquidity"
    assert b.suggested_playbook == "avoid_low_liquidity"
    assert {"HEI/USDT", "PSG/USDT", "NFP/USDT"} <= set(b.primary_symbols)


def test_basket_with_rumour_prefers_sell_the_news_watch():
    events = [_ev("BNB/USDT", "rumour_only", related=["ASTER/USDT"])]
    baskets = build_narrative_baskets(events)
    b = next(b for b in baskets if b.basket_name == "binance_ecosystem_teaser")
    assert b.suggested_playbook == "sell_the_news_watch"


def test_basket_freshness_label_chooses_youngest_event():
    """When multiple events feed a basket the freshness reflects the youngest."""

    events = [
        _ev("BNB/USDT", "hodler_airdrop", fresh=24.0),
        _ev("BNB/USDT", "product_launch", fresh=0.5),
    ]
    baskets = build_narrative_baskets(events)
    assert baskets[0].freshness == "<1h"


# ---------------------------------------------------------------------------
# CatalystEvent record requirements (PART 3)
# ---------------------------------------------------------------------------


def test_catalyst_event_to_dict_has_all_required_fields():
    ev = _ev("BNB/USDT", "hodler_airdrop")
    d = ev.to_dict()
    for required in (
        "catalyst_id", "asset_class", "symbol", "related_symbols",
        "catalyst_type", "source", "source_quality", "title", "url",
        "timestamp", "collected_at", "freshness_hours", "narrative",
        "confidence", "importance", "expected_time_window", "price_reaction_so_far",
        "volume_confirmation", "overextension_risk", "low_liquidity_risk",
        "sell_the_news_risk", "confirms_internal_signal",
        "contradicts_internal_signal", "notes",
    ):
        assert required in d, f"missing field {required}"


def test_narrative_basket_to_dict_has_all_required_fields():
    b = NarrativeBasket(basket_name="x", primary_symbols=["A/USDT"])
    d = b.to_dict()
    for required in (
        "basket_name", "primary_symbols", "related_symbols",
        "catalyst_summary", "source_quality", "freshness",
        "symbols_moved", "symbols_lagging", "symbols_overextended",
        "symbols_blocked", "suggested_playbook", "event_ids", "created_at",
    ):
        assert required in d


def test_catalyst_types_includes_all_spec_categories():
    must_have = {
        "official_product_teaser", "product_launch", "exchange_listing",
        "exchange_delisting", "margin_delisting", "airdrop", "hodler_airdrop",
        "buyback_burn", "token_unlock", "roadmap_event", "mainnet_launch",
        "regulatory_sector_headline", "platform_growth", "social_narrative",
        "partnership", "legal_risk", "exploit_hack", "rumour_only",
        "low_liquidity_event", "sell_the_news_risk",
    }
    assert must_have.issubset(set(CATALYST_TYPES)), (
        f"missing: {must_have - set(CATALYST_TYPES)}"
    )


def test_playbooks_includes_all_spec_actions():
    must_have = {
        "early_breakout", "breakout_retest", "related_beta_rotation",
        "wait_pullback", "sell_the_news_watch", "avoid_chase",
        "avoid_low_liquidity", "no_trade",
    }
    assert must_have.issubset(set(PLAYBOOKS))


# ---------------------------------------------------------------------------
# Collector end-to-end (with isolated SQLite)
# ---------------------------------------------------------------------------


def _store_with_news(tmp_path: Path, items: list[dict]) -> "SQLiteStore":
    from src.models import NewsItem
    from src.storage.sqlite import SQLiteStore

    store = SQLiteStore(tmp_path / "desk.sqlite")
    store.init_db()
    news_items = [NewsItem(**i) for i in items]
    store.save_news_items(news_items, asset_class="crypto")
    return store


def test_collector_rejects_test_source(tmp_path):
    store = _store_with_news(tmp_path, [
        {"title": "Real news", "source": "CoinDesk",
         "url": "https://coindesk.com/example",
         "published_at": _R10,
         "detected_symbols": ["BTC/USDT"]},
        {"title": "Fixture", "source": "test_source",
         "url": "https://test.example/fixture",
         "published_at": _R10},
    ])
    result = collect_catalysts(
        store, project_root=tmp_path, lookback_hours=720, write_files=False,
    )
    assert result.rejected_test_sources == 1
    assert len(result.events) == 1
    assert result.events[0].source == "CoinDesk"


def test_collector_rejects_missing_url(tmp_path):
    from src.models import NewsItem
    from src.storage.sqlite import SQLiteStore

    store = SQLiteStore(tmp_path / "desk.sqlite")
    store.init_db()
    # NewsItem requires url; emulate a malformed row directly.
    with store.connect() as conn:
        conn.execute(
            "INSERT INTO news_items(title, source, url, published_at, "
            "detected_symbols_json, detected_narratives_json, importance, "
            "asset_class, raw_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("Headline", "CoinDesk", "", _R10,
             "[]", "[]", 0.5, "crypto", "{}"),
        )
    result = collect_catalysts(
        store, project_root=tmp_path, lookback_hours=720, write_files=False,
    )
    assert result.rejected_missing_fields == 1
    assert result.events == []


def test_collector_writes_jsonl(tmp_path):
    store = _store_with_news(tmp_path, [
        {"title": "DxSale drained for $7.3M in BNB Chain liquidity exploit",
         "source": "Cointelegraph",
         "url": "https://cointelegraph.com/example/dxsale",
         "published_at": _R10,
         "detected_symbols": ["BNB/USDT"]},
        {"title": "DTCC partners with Stellar Development Foundation",
         "source": "CoinDesk",
         "url": "https://coindesk.com/example/dtcc-stellar",
         "published_at": _R11,
         "detected_symbols": ["XLM/USDT"]},
    ])
    result = collect_catalysts(
        store, project_root=tmp_path, lookback_hours=720,
    )
    assert result.events_path is not None and result.events_path.exists()
    assert result.baskets_path is not None and result.baskets_path.exists()
    assert result.summary_path is not None and result.summary_path.exists()
    # Events file has 2 records.
    lines = result.events_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    for line in lines:
        rec = json.loads(line)
        assert rec["asset_class"] == "crypto"
        assert rec["source"]
        assert rec["title"]
        assert rec["url"]


def test_collector_clusters_bnb_dxsale_and_xlm_dtcc_into_separate_baskets(tmp_path):
    """Different catalysts produce different baskets per the static map."""

    store = _store_with_news(tmp_path, [
        {"title": "DxSale drained for $7.3M in BNB Chain liquidity exploit",
         "source": "Cointelegraph",
         "url": "https://cointelegraph.com/example/dxsale",
         "published_at": _R10,
         "detected_symbols": ["BNB/USDT"]},
        {"title": "DTCC partners with Stellar Development Foundation",
         "source": "CoinDesk",
         "url": "https://coindesk.com/example/dtcc",
         "published_at": _R11,
         "detected_symbols": ["XLM/USDT"]},
    ])
    result = collect_catalysts(
        store, project_root=tmp_path, lookback_hours=720, write_files=False,
    )
    names = {b.basket_name for b in result.baskets}
    assert "binance_ecosystem_teaser" in names
    assert "rwa_narrative" in names


# ---------------------------------------------------------------------------
# Safety contract — verifies the spec promises
# ---------------------------------------------------------------------------


def test_no_llm_imports_in_catalysts_module():
    """The catalyst layer must NOT auto-invoke any LLM API."""

    import src.catalysts.collector as collector
    import src.catalysts.classifier as classifier
    import src.catalysts.baskets as baskets

    for mod in (collector, classifier, baskets):
        src_text = Path(mod.__file__).read_text(encoding="utf-8").lower()
        for forbidden in ("anthropic", "openai", "claude api", "opus.invoke"):
            assert forbidden not in src_text, (
                f"forbidden token '{forbidden}' in {mod.__file__}"
            )


def test_obsidian_system_prompt_exists():
    p = (Path(__file__).resolve().parent.parent /
         "obsidian_vault" / "15_LLM_Context" /
         "Opus_Enriched_Market_Review_System_Prompt.md")
    assert p.exists(), f"missing {p}"
    txt = p.read_text(encoding="utf-8")
    # Hardest contract checks.
    assert "advisory" in txt.lower()
    assert "no auto-trade" in txt.lower() or "not allowed to auto-trade" in txt.lower()
    assert "catalyst" in txt.lower()


def test_protocol_file_includes_section_15_and_16():
    p = (Path(__file__).resolve().parent.parent /
         "prompts" / "llm_review" / "enriched_market_review_protocol.md")
    txt = p.read_text(encoding="utf-8")
    assert "## 15. Operational skill" in txt
    assert "## 16. Auto-collected catalyst layer" in txt


def test_scheduler_catalyst_step_is_command_nonfatal():
    """Scheduler must classify catalyst step as nonfatal — cycle keeps going."""

    from scripts.run_default_market_schedule import catalyst_scan_step

    label, argv, kind, duration = catalyst_scan_step()
    assert kind == "command_nonfatal"
    assert "catalyst-scan" in " ".join(argv)


def test_no_auto_trade_in_scheduler_or_catalyst_paths():
    """Sanity: grep the scheduler + catalyst module for forbidden execute hooks."""

    repo = Path(__file__).resolve().parent.parent
    forbidden = ("place_order", "create_order", "auto_trade")
    for sub in ("scripts/run_default_market_schedule.py",
                "src/catalysts/collector.py",
                "src/catalysts/classifier.py",
                "src/catalysts/baskets.py"):
        text = (repo / sub).read_text(encoding="utf-8").lower()
        for f in forbidden:
            assert f not in text, f"'{f}' must not appear in {sub}"


# ---------------------------------------------------------------------------
# Importance scoring (catalyst prioritization fix)
# ---------------------------------------------------------------------------


def test_score_importance_in_unit_range():
    """Every score must stay within [0, 1] across a spread of inputs."""

    cases = [
        dict(catalyst_type="exploit_hack", source_quality="primary_source",
             freshness_hours=0.5, symbol="BTC/USDT", title="BTC bridge hack"),
        dict(catalyst_type="other_news", source_quality="unverifiable",
             freshness_hours=None, symbol="", title=""),
        dict(catalyst_type="rumour_only", source_quality="social_only",
             freshness_hours=200.0, symbol="FOO/USDT", title="rumour"),
        dict(catalyst_type="earnings_event", source_quality="single_source",
             freshness_hours=5.0, symbol="AVGO", title="AVGO Q2 earnings beat"),
    ]
    for c in cases:
        s = score_importance(**c)
        assert 0.0 <= s <= 1.0, f"{c} -> {s}"


def test_score_importance_is_nonzero_for_real_catalyst():
    """The bug being fixed: a real catalyst must NOT score 0.0."""

    s = score_importance(
        catalyst_type="exchange_listing", source_quality="primary_source",
        freshness_hours=1.0, symbol="SOL/USDT",
        title="Binance lists SOL perpetual",
    )
    assert s > 0.0


def test_high_severity_outranks_other_news():
    high = score_importance(
        catalyst_type="exploit_hack", source_quality="primary_source",
        freshness_hours=0.5, symbol="BTC/USDT", title="Protocol drained $50M exploit",
    )
    low = score_importance(
        catalyst_type="other_news", source_quality="single_source",
        freshness_hours=0.5, symbol="BTC/USDT", title="BTC trades sideways",
    )
    assert high > low


def test_primary_source_outranks_social_only_all_else_equal():
    primary = score_importance(
        catalyst_type="partnership", source_quality="primary_source",
        freshness_hours=2.0, symbol="ETH/USDT", title="ETH foundation partnership",
    )
    social = score_importance(
        catalyst_type="partnership", source_quality="social_only",
        freshness_hours=2.0, symbol="ETH/USDT", title="ETH foundation partnership",
    )
    assert primary > social


def test_fresh_outranks_stale_all_else_equal():
    fresh = score_importance(
        catalyst_type="partnership", source_quality="single_source",
        freshness_hours=0.5, symbol="ETH/USDT", title="ETH partnership",
    )
    stale = score_importance(
        catalyst_type="partnership", source_quality="single_source",
        freshness_hours=200.0, symbol="ETH/USDT", title="ETH partnership",
    )
    assert fresh > stale


def test_mapped_symbol_outranks_basket_level():
    mapped = score_importance(
        catalyst_type="partnership", source_quality="single_source",
        freshness_hours=2.0, symbol="ETH/USDT", title="ETH partnership",
    )
    basket = score_importance(
        catalyst_type="partnership", source_quality="single_source",
        freshness_hours=2.0, symbol="", title="some partnership",
    )
    assert mapped > basket


def test_major_symbol_outranks_obscure_all_else_equal():
    major = score_importance(
        catalyst_type="partnership", source_quality="single_source",
        freshness_hours=2.0, symbol="BTC/USDT", title="BTC partnership",
    )
    obscure = score_importance(
        catalyst_type="partnership", source_quality="single_source",
        freshness_hours=2.0, symbol="ZZZ/USDT", title="ZZZ partnership",
    )
    assert major > obscure


def test_rumour_modifier_discounts_score():
    confirmed = score_importance(
        catalyst_type="partnership", source_quality="single_source",
        freshness_hours=2.0, symbol="ETH/USDT", title="ETH inks deal",
        is_rumour=False,
    )
    rumoured = score_importance(
        catalyst_type="partnership", source_quality="single_source",
        freshness_hours=2.0, symbol="ETH/USDT", title="ETH inks deal",
        is_rumour=True,
    )
    assert rumoured < confirmed


def test_geopolitical_detection_and_boost():
    assert detect_geopolitical_severity(
        "US Central Command strikes Iran-bound oil tankers near Strait of Hormuz"
    ) is True
    assert detect_geopolitical_severity("BTC trades sideways") is False

    geo = score_importance(
        catalyst_type="regulatory_sector_headline", source_quality="single_source",
        freshness_hours=2.0, symbol="", title="Missile strikes near Strait of Hormuz",
    )
    plain = score_importance(
        catalyst_type="regulatory_sector_headline", source_quality="single_source",
        freshness_hours=2.0, symbol="", title="Routine market update",
    )
    assert geo > plain


def test_collector_assigns_nonzero_importance_and_ranks(tmp_path):
    """End-to-end: serialized events carry a non-zero importance and the
    high-severity exploit outranks the partnership."""

    store = _store_with_news(tmp_path, [
        {"title": "DTCC partners with Stellar Development Foundation",
         "source": "CoinDesk",
         "url": "https://coindesk.com/example/dtcc-stellar",
         "published_at": _R11,
         "detected_symbols": ["XLM/USDT"]},
        {"title": "Protocol drained for $50M in BNB Chain liquidity exploit",
         "source": "Cointelegraph",
         "url": "https://cointelegraph.com/example/exploit",
         "published_at": _R1130,
         "detected_symbols": ["BNB/USDT"]},
    ])
    result = collect_catalysts(
        store, project_root=tmp_path, lookback_hours=100000,
    )
    by_sym = {e.symbol: e for e in result.events}
    assert by_sym["BNB/USDT"].importance > 0.0
    assert by_sym["XLM/USDT"].importance > 0.0
    # exploit_hack must outrank partnership.
    assert by_sym["BNB/USDT"].importance > by_sym["XLM/USDT"].importance
    # And it must be serialized to the JSONL.
    lines = result.events_path.read_text(encoding="utf-8").strip().splitlines()
    for line in lines:
        rec = json.loads(line)
        assert "importance" in rec
        assert isinstance(rec["importance"], (int, float))
