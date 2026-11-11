"""Tests for the curated entity-alias matcher + integrated catalyst flow.

Covers PART 6 from the spec:
- Cardano → ADA, Sui → SUI, Aave → AAVE, etc.
- "Binance Coin" / "BNB Chain" → BNB
- false-positive safety: "near"/"one"/"link"/"flow" lowercase don't trigger
- extended classifier patterns (ETF approval, CFTC, lawsuit, TVL surge)
- narrative basket formed when related symbols match
- scheduler/safety contract unchanged
- no auto-trade
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from datetime import datetime, timezone, timedelta

from src.catalysts.classifier import classify_catalyst_type
from src.catalysts.entity_aliases import (
    EntityAliasMatcher,
    _is_strict_ticker,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Recent, IN-WINDOW published_at for the collector's rolling lookback — absolute fixture dates
# (2026-06-01) age out of the window and fail on a later run; anchor to now for durability.
_R10 = (datetime.now(timezone.utc) - timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S+00:00")


@pytest.fixture(scope="module")
def matcher() -> EntityAliasMatcher:
    return EntityAliasMatcher.load(PROJECT_ROOT)


# ---------------------------------------------------------------------------
# Required PART 6 mappings
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("headline,expected", [
    ("Cardano Foundation cancels annual conference", "ADA/USDT"),
    ("Sui Foundation says major upgrade fixed bugs", "SUI/USDT"),
    ("Aave overhauls listing standards after exploit", "AAVE/USDT"),
    ("DxSale drained for $7.3M in BNB Chain liquidity exploit", "BNB/USDT"),
    ("Binance Coin holders earn from HODLer airdrop", "BNB/USDT"),
    ("Hyperliquid launches new perpetual contract", "HYPE/USDT"),
    ("Ripple SEC settlement reached", "XRP/USDT"),
    ("Solana hits new TPS record", "SOL/USDT"),
    ("Ethereum core devs ship Pectra upgrade", "ETH/USDT"),
    ("Bitcoin ETF inflows top $1B for the week", "BTC/USDT"),
    ("Stellar Development Foundation closes DTCC deal", "XLM/USDT"),
    ("Toncoin holders accumulate after Telegram validator switch", "TON/USDT"),
    ("Worldcoin rolls out Oku Trade DeFi integration", "WLD/USDT"),
])
def test_canonical_name_maps_to_ticker(matcher, headline, expected):
    assert expected in matcher.detect(headline), (
        f"{headline!r} → {matcher.detect(headline)}, expected {expected}"
    )


# ---------------------------------------------------------------------------
# False-positive safety
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("headline", [
    "Stay near the entry zone if pullback holds",
    "If price holds the level it could break out",
    "Coin holders unlocked one new feature",
    "The link between volume and price is clear",
    "Free flow of capital across the bridge",
])
def test_lowercase_common_words_do_not_false_positive(matcher, headline):
    assert matcher.detect(headline) == [], (
        f"{headline!r} should not trigger but got {matcher.detect(headline)}"
    )


def test_uppercase_near_does_trigger(matcher):
    assert "NEAR/USDT" in matcher.detect("NEAR pumps 26% on AI rotation")


def test_lowercase_near_does_not_trigger_without_protocol_alias(matcher):
    """Plain lowercase "near" never hits the NEAR ticker — only the
    multi-word "NEAR Protocol" alias or the uppercase strict ticker."""

    assert "NEAR/USDT" not in matcher.detect("Stay near the breakout zone")


def test_chainlink_multi_word_alias(matcher):
    assert "LINK/USDT" in matcher.detect("Chainlink unveils CCIP v2.0")


def test_optimism_only_matches_multi_word(matcher):
    """OP alone is too risky — only the multi-word 'Optimism' triggers."""

    assert "OP/USDT" in matcher.detect("Optimism Bedrock upgrade live")


def test_bnb_chain_alias_matches(matcher):
    assert "BNB/USDT" in matcher.detect("New L2 launches on BNB Chain")


def test_bsc_short_alias_matches(matcher):
    """BSC = Binance Smart Chain, must map to BNB."""

    assert "BNB/USDT" in matcher.detect("New protocol deploys on BSC")


# ---------------------------------------------------------------------------
# Matcher internals
# ---------------------------------------------------------------------------


def test_strict_ticker_classifier():
    assert _is_strict_ticker("BTC") is True       # short single-word → strict
    assert _is_strict_ticker("ETH") is True
    assert _is_strict_ticker("Cardano") is False  # 5+ chars → case-insensitive
    assert _is_strict_ticker("BNB Chain") is False  # multi-word → case-insensitive


def test_yaml_loaded_with_expected_tickers(matcher):
    expected = {
        "BTC", "ETH", "BNB", "SOL", "XRP", "ADA",
        "AAVE", "SUI", "HYPE", "ASTER", "TON", "WLD",
        "XLM", "STG",
    }
    assert expected.issubset(set(matcher.by_ticker.keys()))


def test_tags_for_returns_tags(matcher):
    assert "majors" in matcher.tags_for("BTC")
    assert "perps" in matcher.tags_for("HYPE")
    assert "rwa" in matcher.tags_for("ONDO")


# ---------------------------------------------------------------------------
# Extended classifier patterns
# ---------------------------------------------------------------------------


def test_etf_approval_is_regulatory_headline():
    assert classify_catalyst_type(
        "SEC approves Bitcoin spot ETF for trading"
    ) == "regulatory_sector_headline"


def test_cftc_enforcement_is_regulatory_headline():
    assert classify_catalyst_type(
        "CFTC enforcement targets crypto derivatives platform"
    ) == "regulatory_sector_headline"


def test_lawsuit_filed_is_legal_risk():
    assert classify_catalyst_type(
        "Activist filed a lawsuit against the exchange"
    ) == "legal_risk"


def test_wire_fraud_is_legal_risk():
    assert classify_catalyst_type(
        "DOJ probes wire fraud at crypto firm"
    ) == "legal_risk"


def test_tvl_surge_is_platform_growth():
    assert classify_catalyst_type(
        "Hyperliquid TVL surge sets new yearly high"
    ) == "platform_growth"


def test_revenue_ath_is_platform_growth():
    assert classify_catalyst_type(
        "Revenue ATH for DEX as fees jump 50%"
    ) == "platform_growth"


# ---------------------------------------------------------------------------
# Catalyst collector end-to-end with alias backfill
# ---------------------------------------------------------------------------


def test_collector_backfills_symbol_via_alias(tmp_path):
    """A news_items row with EMPTY detected_symbols should still get a
    mapped ticker via the entity alias matcher."""

    from src.models import NewsItem
    from src.storage.sqlite import SQLiteStore
    from src.catalysts import collect_catalysts

    # Build a tmp DB with one row that has detected_symbols=[].
    db = SQLiteStore(tmp_path / "desk.sqlite")
    db.init_db()
    db.save_news_items([NewsItem(
        title="Cardano Foundation cancels annual conference after failed funding vote",
        source="Cointelegraph",
        url="https://cointelegraph.com/example/cardano-foundation",
        published_at=_R10,
        detected_symbols=[],  # ← upstream missed it
        importance=0.5,
    )], asset_class="crypto")

    # Use the PRODUCTION YAML (project_root=PROJECT_ROOT).
    result = collect_catalysts(
        db, project_root=PROJECT_ROOT,
        lookback_hours=720, write_files=False,
    )
    assert len(result.events) == 1
    ev = result.events[0]
    assert ev.symbol == "ADA/USDT", (
        f"alias backfill failed: symbol={ev.symbol!r}"
    )


def test_collector_does_not_overwrite_existing_symbols(tmp_path):
    """If detected_symbols was populated, do NOT override it."""

    from src.models import NewsItem
    from src.storage.sqlite import SQLiteStore
    from src.catalysts import collect_catalysts

    db = SQLiteStore(tmp_path / "desk.sqlite")
    db.init_db()
    db.save_news_items([NewsItem(
        title="Cardano Foundation cancels annual conference (also mentions Bitcoin)",
        source="Cointelegraph",
        url="https://cointelegraph.com/example/x",
        published_at=_R10,
        detected_symbols=["BTC/USDT"],  # ← upstream caught BTC
        importance=0.5,
    )], asset_class="crypto")

    result = collect_catalysts(
        db, project_root=PROJECT_ROOT,
        lookback_hours=720, write_files=False,
    )
    ev = result.events[0]
    assert ev.symbol == "BTC/USDT"  # preserves upstream choice


def test_basket_forms_when_alias_backfill_provides_bnb(tmp_path):
    """End-to-end: a "BNB Chain exploit" headline (no upstream symbol)
    should now form the binance_ecosystem_teaser basket."""

    from src.models import NewsItem
    from src.storage.sqlite import SQLiteStore
    from src.catalysts import collect_catalysts

    db = SQLiteStore(tmp_path / "desk.sqlite")
    db.init_db()
    db.save_news_items([NewsItem(
        title="DxSale drained for $7.3M in BNB Chain liquidity exploit",
        source="Cointelegraph",
        url="https://cointelegraph.com/example/dxsale",
        published_at=_R10,
        detected_symbols=[],
        importance=0.5,
    )], asset_class="crypto")

    result = collect_catalysts(
        db, project_root=PROJECT_ROOT,
        lookback_hours=720, write_files=False,
    )
    basket_names = {b.basket_name for b in result.baskets}
    assert "binance_ecosystem_teaser" in basket_names


# ---------------------------------------------------------------------------
# Safety contract
# ---------------------------------------------------------------------------


def test_entity_aliases_module_has_no_llm_imports():
    src = (PROJECT_ROOT / "src" / "catalysts" / "entity_aliases.py").read_text(
        encoding="utf-8"
    ).lower()
    for forbidden in ("anthropic", "openai", "claude api", "opus.invoke"):
        assert forbidden not in src


def test_yaml_file_exists_with_required_tickers():
    p = PROJECT_ROOT / "config" / "crypto_entity_aliases.yaml"
    assert p.exists()
    txt = p.read_text(encoding="utf-8")
    for must in ("Cardano", "Aave", "Hyperliquid", "Ripple", "BNB Chain",
                 "Solana", "Ethereum", "Bitcoin", "Toncoin"):
        assert must in txt, f"missing alias {must!r} in YAML"


def test_no_auto_trade_in_alias_module():
    src = (PROJECT_ROOT / "src" / "catalysts" / "entity_aliases.py").read_text(
        encoding="utf-8"
    ).lower()
    for forbidden in ("place_order", "create_order", "auto_trade"):
        assert forbidden not in src
