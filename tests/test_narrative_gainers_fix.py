"""Tests for PART 5 narrative + new-gainers fix.

Covers:
1. Extended classifier patterns (regulatory, listing, governance,
   infrastructure, partnership).
2. New catalyst categories: `governance_event`, `infrastructure_failure`,
   `momentum_breakout`.
3. `build_momentum_breakout_basket` — pure-momentum cluster from top
   gainers without news catalyst.
4. Expanded sources.yaml RSS list.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from src.catalysts.baskets import build_momentum_breakout_basket
from src.catalysts.classifier import classify_catalyst_type
from src.catalysts.models import CATALYST_TYPES, PLAYBOOKS
from src.agents.narrative_agent import NarrativeAgent


PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Classifier — extended patterns
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("headline,expected_type", [
    # exchange_listing — Binance Futures perpetual
    ("Binance Futures Will Launch USDⓈ-Margined SLXUSDT Perpetual Contract",
     "exchange_listing"),
    ("Binance Lists Aster (ASTER) on Spot Pair",
     "exchange_listing"),

    # regulatory_sector_headline — ETF outflows + Congress + bank rails + Citi
    ("Bitcoin extends slide as spot ETF outflows hit a record",
     "regulatory_sector_headline"),
    ("US Congress returns as GENIUS comments periods close",
     "regulatory_sector_headline"),
    ("Coinbase launches rupee bank rails in India after FIU nod",
     "regulatory_sector_headline"),
    ("Citi predicts the tokenized securities market will grow to 5.5 trillion",
     "regulatory_sector_headline"),

    # partnership — Wintermute liquidity + "major play for X market"
    ("Wintermute to bring liquidity to booming prediction markets sector",
     "partnership"),
    ("Coinbase makes a major play for India crypto market",
     "partnership"),

    # governance_event — Foundation cancels + failed funding vote
    ("Cardano Foundation cancels annual conference after failed funding vote",
     "governance_event"),

    # infrastructure_failure — Sui mainnet halts + outages
    ("Three Sui mainnet halts in 48 hours traced to an upgrade bug",
     "infrastructure_failure"),
    ("Solana network outage stops block production for 30 minutes",
     "infrastructure_failure"),

    # Existing patterns still work
    ("Aave overhauls listing standards after $230M rsETH exploit",
     "exploit_hack"),
    ("SMCI indictment over Nvidia smuggling",
     "legal_risk"),
    ("LayerZero proposes $110M Stargate acquisition",
     "partnership"),
])
def test_extended_classifier_patterns(headline, expected_type):
    assert classify_catalyst_type(headline) == expected_type, (
        f"{headline!r} → {classify_catalyst_type(headline)} expected {expected_type}"
    )


def test_new_catalyst_types_registered():
    """The 3 new categories must be in the public enum."""

    for new_type in ("governance_event", "infrastructure_failure", "momentum_breakout"):
        assert new_type in CATALYST_TYPES, f"missing {new_type} in CATALYST_TYPES"


def test_avoid_chase_playbook_registered():
    """avoid_chase must still be a valid playbook (used by momentum basket)."""

    assert "avoid_chase" in PLAYBOOKS
    assert "wait_pullback" in PLAYBOOKS


# ---------------------------------------------------------------------------
# Momentum breakout basket
# ---------------------------------------------------------------------------


def test_momentum_breakout_returns_none_when_no_qualifiers():
    movers = [
        {"symbol": "BTC/USDT", "score": 50, "return_24h_pct": 1.2, "volume_ratio": 0.3},
    ]
    assert build_momentum_breakout_basket(movers) is None


def test_momentum_breakout_filters_low_movement():
    movers = [
        {"symbol": "BTC/USDT", "score": 50, "return_24h_pct": 5.0, "volume_ratio": 1.5},  # 5% < 10% → reject
    ]
    assert build_momentum_breakout_basket(movers) is None


def test_momentum_breakout_filters_low_volume():
    movers = [
        {"symbol": "BTC/USDT", "score": 80, "return_24h_pct": 20.0, "volume_ratio": 0.3},  # 0.3 < 0.5 → reject
    ]
    assert build_momentum_breakout_basket(movers) is None


def test_momentum_breakout_clusters_qualifying_movers():
    movers = [
        {"symbol": "HOME/USDT", "score": 91, "return_24h_pct": 41.0, "volume_ratio": 0.55},
        {"symbol": "WLD/USDT", "score": 88, "return_24h_pct": 13.2, "volume_ratio": 1.42},
        {"symbol": "TON/USDT", "score": 73, "return_24h_pct": 11.6, "volume_ratio": 6.77},
        # Filter out:
        {"symbol": "BTC/USDT", "score": 50, "return_24h_pct": 1.2, "volume_ratio": 0.3},
    ]
    basket = build_momentum_breakout_basket(movers)
    assert basket is not None
    assert basket.basket_name == "momentum_breakout"
    assert basket.suggested_playbook in {"wait_pullback", "avoid_chase"}
    # 3 qualifying movers; up to 3 land in primary.
    assert {"HOME/USDT", "WLD/USDT", "TON/USDT"} <= set(basket.primary_symbols)
    # BTC should not be in either bucket.
    all_members = set(basket.primary_symbols) | set(basket.related_symbols)
    assert "BTC/USDT" not in all_members


def test_momentum_breakout_overextended_flag_pushes_avoid_chase():
    movers = [
        {"symbol": "PORTAL/USDT", "score": 92, "return_24h_pct": 167.0, "volume_ratio": 0.6, "overextension_risk": True},
        {"symbol": "HOME/USDT", "score": 85, "return_24h_pct": 22.0, "volume_ratio": 0.55},
    ]
    basket = build_momentum_breakout_basket(movers)
    assert basket is not None
    assert basket.suggested_playbook == "avoid_chase"
    assert "PORTAL/USDT" in basket.symbols_overextended


def test_momentum_breakout_caps_at_6_members():
    movers = [
        {"symbol": f"TEST{i}/USDT", "score": 80, "return_24h_pct": 15.0 + i, "volume_ratio": 0.8}
        for i in range(10)
    ]
    basket = build_momentum_breakout_basket(movers)
    assert basket is not None
    total = len(basket.primary_symbols) + len(basket.related_symbols)
    assert total <= 6, f"basket has {total} members, exceeds cap of 6"


def test_momentum_breakout_sorts_by_24h_pct_descending():
    movers = [
        {"symbol": "AAA/USDT", "score": 70, "return_24h_pct": 12.0, "volume_ratio": 0.8},
        {"symbol": "BBB/USDT", "score": 70, "return_24h_pct": 40.0, "volume_ratio": 0.8},
        {"symbol": "CCC/USDT", "score": 70, "return_24h_pct": 25.0, "volume_ratio": 0.8},
    ]
    basket = build_momentum_breakout_basket(movers)
    assert basket is not None
    # Primary = top 3 sorted by 24h desc: BBB (40%), CCC (25%), AAA (12%)
    assert basket.primary_symbols == ["BBB/USDT", "CCC/USDT", "AAA/USDT"]


# ---------------------------------------------------------------------------
# Sources YAML expansion
# ---------------------------------------------------------------------------


def test_sources_yaml_includes_new_rss_feeds():
    """PART 5 added TheBlock, BeInCrypto, AMBCrypto, CryptoSlate, CryptoBriefing."""

    path = PROJECT_ROOT / "config" / "sources.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    feeds = data.get("rss_feeds", [])
    names = {f.get("name") for f in feeds}
    for required in ("The Block", "BeInCrypto", "AMBCrypto",
                     "CryptoSlate", "CryptoBriefing"):
        assert required in names, f"missing source {required!r}"


def test_sources_yaml_existing_feeds_untouched():
    """We must not have broken the existing source list."""

    path = PROJECT_ROOT / "config" / "sources.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    feeds = data.get("rss_feeds", [])
    names = {f.get("name") for f in feeds}
    for required in ("Binance Announcements", "CoinDesk", "Cointelegraph", "Decrypt"):
        assert required in names, f"{required} removed by accident"


def test_broad_narrative_mentions_cannot_heat_theme_without_market_representative(monkeypatch):
    config = type("Config", (), {"watchlist": {
        "narratives": {"ai": {"symbols": ["FET", "TAO"]}}
    }})()
    agent = NarrativeAgent(config, None, None)
    monkeypatch.setattr(agent, "save_output", lambda payload: None)

    result = agent.run(
        [], {"by_narrative": {"ai": [{"title": "AI adoption expands"}] * 12},
             "by_symbol": {}}, {},
    )["ai"]

    assert result.attention_score == 0
    assert result.heat_score == 0
    assert result.status == "quiet"
    assert any("ignored" in warning.lower() for warning in result.warnings)
