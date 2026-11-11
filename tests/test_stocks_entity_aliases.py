"""PART 19 — stocks entity-alias mapping tests.

Catalyst mapping was ~80 % unmapped in the audit. PART 19 adds a
stocks-side counterpart to ``config/crypto_entity_aliases.yaml``:
``config/stocks_entity_aliases.yaml`` plus a parallel
``EntityAliasMatcher.load_stocks(...)`` factory that returns BARE
tickers (no ``/USDT`` suffix).

These tests pin the mappings the audit explicitly asked for AND
guard against the typical false-positive class (the word "apple" in
a sentence that isn't about Apple Inc., etc.).
"""
from __future__ import annotations

from pathlib import Path

import pytest

from src.catalysts.entity_aliases import (
    EntityAliasMatcher,
    get_stocks_matcher,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def stocks_matcher() -> EntityAliasMatcher:
    return EntityAliasMatcher.load_stocks(PROJECT_ROOT)


def _detected(matcher: EntityAliasMatcher, text: str) -> list[str]:
    return matcher.detect(text)


# ---------------------------------------------------------------------------
# Required mappings — pinned by the audit's PART 3 spec
# ---------------------------------------------------------------------------


def test_super_micro_resolves_to_SMCI(stocks_matcher):
    """Both 'Super Micro' and 'Supermicro' must resolve to SMCI."""
    for headline in (
        "Super Micro Computer Inc reports Q3 FY2026 results",
        "Supermicro AI server demand accelerates",
        "Super Micro indicted in $2.5B export-control case",
    ):
        hits = _detected(stocks_matcher, headline)
        assert "SMCI" in hits, f"missed SMCI in {headline!r} → {hits}"


def test_apple_resolves_to_AAPL(stocks_matcher):
    hits = _detected(stocks_matcher, "Apple Inc unveils new AI features at WWDC")
    assert "AAPL" in hits


def test_advanced_micro_devices_resolves_to_AMD(stocks_matcher):
    hits = _detected(
        stocks_matcher,
        "Advanced Micro Devices announces MI400 AI accelerator family",
    )
    assert "AMD" in hits


def test_broadcom_resolves_to_AVGO(stocks_matcher):
    hits = _detected(
        stocks_matcher,
        "Broadcom Inc reports record AI semiconductor revenue",
    )
    assert "AVGO" in hits


def test_nvidia_resolves_to_NVDA(stocks_matcher):
    hits = _detected(
        stocks_matcher,
        "Nvidia announces next-gen Blackwell chips at Computex",
    )
    assert "NVDA" in hits


def test_spdr_sp500_resolves_to_SPY(stocks_matcher):
    hits = _detected(
        stocks_matcher,
        "SPDR S&P 500 ETF Trust sees record inflows after Fed pivot",
    )
    assert "SPY" in hits


def test_invesco_qqq_resolves_to_QQQ(stocks_matcher):
    hits = _detected(stocks_matcher, "Invesco QQQ Trust hits all-time high")
    assert "QQQ" in hits


# ---------------------------------------------------------------------------
# No false positives on common words
# ---------------------------------------------------------------------------


def test_apple_orchard_does_not_trigger_AAPL(stocks_matcher):
    """The word 'apple' alone (lowercase, generic) must not map to AAPL.

    The aliases list uses 'Apple Inc', 'Apple Computer', or 'Cupertino' so
    a plain noun match requires the full corporate form.
    """
    hits = _detected(
        stocks_matcher,
        "Farmers in upstate New York report an early apple harvest this year.",
    )
    assert "AAPL" not in hits, hits


def test_amd_in_random_acronym_text_is_case_sensitive(stocks_matcher):
    """Short tickers are matched case-sensitively to avoid false hits."""
    hits = _detected(
        stocks_matcher,
        "The amdahl model says system speedup is limited by serial code.",
    )
    assert "AMD" not in hits, hits


def test_meta_word_does_not_falsely_map_to_META(stocks_matcher):
    """Plain 'meta' in 'meta-learning' or 'meta-analysis' must NOT map to META."""
    hits = _detected(
        stocks_matcher,
        "A new meta-analysis confirms the prior meta-learning approach.",
    )
    assert "META" not in hits


def test_dia_etf_alias_does_not_trigger_on_generic_word(stocks_matcher):
    """'Dia' in foreign text shouldn't map to DIA."""
    hits = _detected(stocks_matcher, "Buenos dia means good morning in Spanish.")
    assert "DIA" not in hits


# ---------------------------------------------------------------------------
# Returns BARE tickers (no /USDT suffix) — that's the whole point
# ---------------------------------------------------------------------------


def test_stocks_matcher_returns_bare_tickers(stocks_matcher):
    """Crypto matcher appends ``/USDT``; stocks matcher must NOT."""
    hits = _detected(stocks_matcher, "Apple Inc announces AI features")
    for hit in hits:
        assert "/" not in hit, f"stocks matcher must not append suffix, got {hit!r}"


# ---------------------------------------------------------------------------
# Cached factory works
# ---------------------------------------------------------------------------


def test_get_stocks_matcher_returns_loaded_instance():
    matcher = get_stocks_matcher(str(PROJECT_ROOT))
    assert matcher.by_ticker, "stocks matcher must load entries from YAML"
    assert "SMCI" in matcher.by_ticker


# ---------------------------------------------------------------------------
# Sanity — multiple symbols in one headline
# ---------------------------------------------------------------------------


def test_multi_symbol_headline(stocks_matcher):
    hits = _detected(
        stocks_matcher,
        "Nvidia and Broadcom dominate the AI silicon market while "
        "Super Micro racks ship in record volumes.",
    )
    assert "NVDA" in hits
    assert "AVGO" in hits
    assert "SMCI" in hits


# ---------------------------------------------------------------------------
# Crypto matcher unchanged (regression safety)
# ---------------------------------------------------------------------------


def test_crypto_matcher_still_returns_usdt_suffixed():
    from src.catalysts.entity_aliases import get_matcher

    matcher = get_matcher(str(PROJECT_ROOT))
    hits = matcher.detect("Cardano announces new partnership with Stellar")
    # Should produce ADA/USDT and XLM/USDT (depending on aliases).
    for h in hits:
        assert h.endswith("/USDT"), h
