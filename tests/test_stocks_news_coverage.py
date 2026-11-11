"""Tests for PART 6 stocks news coverage fix.

Validates:
1. New stocks-specific catalyst categories registered.
2. Classifier patterns for earnings_event, analyst_action,
   clinical_milestone, insider_activity all work + handle plurals.
3. config/sources.yaml has the 8 stocks feeds enabled (3 pre-existing
   + 5 new).
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from src.catalysts.classifier import classify_catalyst_type
from src.catalysts.models import CATALYST_TYPES


PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# New stocks-specific categories
# ---------------------------------------------------------------------------


def test_new_stocks_categories_registered():
    for new_type in ("earnings_event", "analyst_action",
                     "clinical_milestone", "insider_activity"):
        assert new_type in CATALYST_TYPES, f"missing {new_type}"


# ---------------------------------------------------------------------------
# Classifier — earnings_event
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("headline", [
    "NVIDIA beats Q3 earnings estimates, revenue tops $25B",
    "Apple reports first-quarter earnings: EPS beats, revenue tops expectations",
    "Microsoft raises full-year guidance after strong Q2 results",
    "Tesla misses Q4 earnings, lowers fiscal-year outlook",
    "Earnings call tonight: NVDA preview",
    "Lilly delivers Q2 quarterly revenue surge",
    "META pre-announces earnings revenue softness",
])
def test_earnings_event_pattern(headline):
    assert classify_catalyst_type(headline) == "earnings_event", (
        f"{headline!r} → {classify_catalyst_type(headline)}"
    )


# ---------------------------------------------------------------------------
# Classifier — analyst_action
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("headline", [
    "JPMorgan upgrades AAPL to Overweight, raises price target to $310",
    "Wedbush downgrades TSLA shares, cuts price target",
    "Goldman initiates coverage of PLTR with Buy rating",
    "Morgan Stanley reiterates Outperform on MSFT, lifts target",
    "Analyst raises price target for SMCI",
    "Wall Street raises target on NVDA after blowout Q3",
    "Bank of America maintains Buy on AVGO",
])
def test_analyst_action_pattern(headline):
    assert classify_catalyst_type(headline) == "analyst_action", (
        f"{headline!r} → {classify_catalyst_type(headline)}"
    )


# ---------------------------------------------------------------------------
# Classifier — clinical_milestone
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("headline", [
    "FDA approves LLY Mounjaro for new indication",
    "Pfizer Phase 3 trial results met primary endpoint",
    "EMA approval expected for novel cancer therapy",
    "BLA submitted by AbbVie for biologic XYZ",
    "FDA clears medical device after fast track review",
])
def test_clinical_milestone_pattern(headline):
    assert classify_catalyst_type(headline) == "clinical_milestone"


# ---------------------------------------------------------------------------
# Classifier — insider_activity
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("headline", [
    "Insider sells: AAPL CEO disposes shares under 10b5-1 plan",
    "Form 4 filing: TSLA director bought 50000 shares",
    "MSFT CFO sells shares worth $5M",
    "Insider buys NVDA shares ahead of earnings",
])
def test_insider_activity_pattern(headline):
    assert classify_catalyst_type(headline) == "insider_activity"


# ---------------------------------------------------------------------------
# Order priority — stocks patterns must NOT cannibalize crypto patterns
# ---------------------------------------------------------------------------


def test_crypto_patterns_still_match():
    """Ensure adding stocks patterns at the top didn't break crypto classification."""

    cases = [
        ("Aave overhauls listing standards after $230M rsETH exploit", "exploit_hack"),
        ("SMCI indictment federal charges Nvidia smuggling", "legal_risk"),
        ("Binance Lists Aster (ASTER) on Spot Pair", "exchange_listing"),
        ("Cardano Foundation cancels annual conference after failed funding vote", "governance_event"),
        ("Three Sui mainnet halts in 48 hours traced to upgrade bug", "infrastructure_failure"),
        ("LayerZero proposes $110M Stargate acquisition", "partnership"),
        ("Bitcoin whales accumulating despite price drop", "other_news"),
    ]
    for headline, expected in cases:
        actual = classify_catalyst_type(headline)
        assert actual == expected, f"{headline!r} → {actual} (expected {expected})"


# ---------------------------------------------------------------------------
# Sources YAML — stocks feeds enabled
# ---------------------------------------------------------------------------


def test_stocks_rss_feeds_enabled():
    """Stocks RSS coverage. NOTE (2026-07-04): the generic `SEC EDGAR Filings` Atom feed is now
    intentionally DISABLED (it returned 0 rows) — SEC filings are ingested reliably via the
    CIK-mapped API source `SEC EDGAR` (src/news/edgar.py), which is NOT an rss_feeds entry. The
    other stocks RSS feeds (incl. the new press-release wires) stay enabled."""

    path = PROJECT_ROOT / "config" / "sources.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    feeds = data.get("rss_feeds", [])
    stocks = [f for f in feeds if (f.get("asset_class") or "crypto") == "stocks"]
    enabled = [f for f in stocks if f.get("enabled") is True]
    names = {f.get("name") for f in enabled}

    must_have = {
        "MarketWatch Top Stories",
        "Yahoo Finance Top Stories",
            "Seeking Alpha Market Currents",
            "CNBC Markets",
            "Benzinga Movers",
        "The Motley Fool Investing",
    }
    missing = must_have - names
    assert not missing, f"missing enabled stocks feeds: {missing}"
    assert len(enabled) >= 8, f"expected ≥8 enabled stocks feeds, got {len(enabled)}"
    # the old generic SEC EDGAR RSS must remain DISABLED with a reason (0-row generic Atom)
    assert "SEC EDGAR Filings" not in names


def test_sec_edgar_old_rss_disabled_new_api_primary():
    """New contract (2026-07-04): old `SEC EDGAR Filings` RSS disabled+reason; the reliable
    CIK-mapped `SEC EDGAR` api-source is registered as a PRIMARY stocks source in source-health."""

    path = PROJECT_ROOT / "config" / "sources.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    feeds = data.get("rss_feeds", [])
    old = next((f for f in feeds if f.get("name") == "SEC EDGAR Filings"), None)
    assert old is not None
    assert old.get("enabled") is False                        # generic RSS returned 0 rows
    assert old.get("disabled_reason")                         # must explain WHY

    # the new API-ingest source is registered as a primary api source in the health read-model
    from src.news.source_health import _configured_sources, _load_sources
    srcs = {s["name"]: s for s in _configured_sources(_load_sources())}
    assert "SEC EDGAR" in srcs
    sec = srcs["SEC EDGAR"]
    assert sec["source_type"] == "api" and sec["primary"] is True and sec["asset_class"] == "stocks"


# ---------------------------------------------------------------------------
# Safety contract
# ---------------------------------------------------------------------------


def test_no_breaking_changes_in_classifier_module():
    """Classifier module must still be pure-regex, no LLM imports."""

    src = (PROJECT_ROOT / "src" / "catalysts" / "classifier.py").read_text(encoding="utf-8").lower()
    for forbidden in ("anthropic", "openai", "claude api", "opus.invoke"):
        assert forbidden not in src
