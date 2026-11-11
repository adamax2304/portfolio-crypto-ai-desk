"""Tests for Crypto Signal Expansion v1 — discovery layer.

Coverage:
- Multi-source discovery (RS-BTC / RS-ETH / momentum / volume / catalyst / narrative / short)
- Shadow / C-tier safety lane via quality gates
- PART 3 invariant: crypto scalp playbook is NEVER produced by expansion
- PART 5 invariants: squeeze guard fires on shorts; playbook labels render
- Read-only: agent does not register signals, does not send Telegram
"""
from __future__ import annotations

from src.agents.discovery_expansion_agent import (
    DiscoveryExpansionAgent,
    MAX_TOTAL_WATCHLIST,
    render_expansion_watchlist_markdown,
)
from src.signals.playbooks import (
    PLAYBOOK_CRYPTO_FAILED_BOUNCE_SHORT,
    PLAYBOOK_CRYPTO_INTRADAY,
    PLAYBOOK_CRYPTO_SCALP,
    PLAYBOOK_CRYPTO_SWING,
)


def _cand(symbol, **kw):
    """Build a candidate dict the agent accepts."""
    base = {
        "symbol": symbol,
        "direction_bias": "long",
        "score": 60,
        "return_24h": 0.0,
        "return_7d": 0.0,
        "relative_strength_btc": 0.0,
        "relative_strength_eth": 0.0,
        "volume_ratio": 1.0,
        "quote_volume_24h_usd": 10_000_000,
        "upper_wick_atr_max": 0.5,
        "reason_tags": [],
    }
    base.update(kw)
    return base


# ---------------------------------------------------------------------------
# Source coverage
# ---------------------------------------------------------------------------


def test_rs_btc_leader_surfaces_with_high_rs():
    cs = [
        _cand("ALPHA/USDT", relative_strength_btc=8.0),
        _cand("BETA/USDT", relative_strength_btc=0.5),
    ]
    res = DiscoveryExpansionAgent().run(candidates=cs)
    syms = {c.symbol for c in res.candidates}
    assert "ALPHA/USDT" in syms
    assert any(c.discovery_source == "rs_btc_leader" for c in res.candidates)


def test_short_breakdown_routes_to_failed_bounce_short():
    cs = [_cand("WEAK/USDT", relative_strength_btc=-5.0, direction_bias="short")]
    res = DiscoveryExpansionAgent().run(candidates=cs)
    flagged = [c for c in res.candidates if c.symbol == "WEAK/USDT"
               and c.discovery_source == "weak_rs_short"]
    assert flagged, "weak RS short candidate should be surfaced"
    assert flagged[0].candidate_playbook == PLAYBOOK_CRYPTO_FAILED_BOUNCE_SHORT
    assert flagged[0].direction_bias == "short"


def test_catalyst_source_routes_to_intraday_catalyst():
    cs = [_cand("CATA/USDT", quote_volume_24h_usd=20_000_000)]
    catalysts = {"CATA/USDT": {"events": [{"title": "news"}], "score": 0.7}}
    res = DiscoveryExpansionAgent().run(candidates=cs, catalysts=catalysts, mode="intraday")
    cata = [c for c in res.candidates if c.symbol == "CATA/USDT"]
    assert cata, "catalyst-backed name should surface"
    assert any(c.discovery_source == "catalyst_backed" for c in cata)
    assert any(c.candidate_playbook == PLAYBOOK_CRYPTO_INTRADAY for c in cata)


def test_narrative_basket_membership_surfaces():
    cs = [_cand("HYPE/USDT", quote_volume_24h_usd=50_000_000)]
    narratives = {"perps_dex_narrative": {"symbols": ["HYPE/USDT"]}}
    res = DiscoveryExpansionAgent().run(candidates=cs, narratives=narratives, mode="swing")
    assert any(c.symbol == "HYPE/USDT"
               and c.discovery_source == "narrative_basket"
               and c.candidate_playbook == PLAYBOOK_CRYPTO_SWING
               for c in res.candidates)


def test_unusual_volume_surfaces():
    cs = [_cand("VOL/USDT", volume_ratio=2.5)]
    res = DiscoveryExpansionAgent().run(candidates=cs)
    assert any(c.discovery_source == "unusual_volume" for c in res.candidates)


# ---------------------------------------------------------------------------
# PART 3 invariant — scalp playbook MUST NEVER be produced by expansion
# ---------------------------------------------------------------------------


def test_scalp_playbook_is_never_produced_by_expansion():
    """No expansion candidate should carry the crypto_scalp_momentum_continuation label.
    The agent skips scalp by mapping all surfaced candidates to intraday/swing/short."""
    cs = [
        _cand("ALPHA/USDT", relative_strength_btc=5.0),
        _cand("BETA/USDT", return_24h=20.0),
        _cand("GAMMA/USDT", direction_bias="short", relative_strength_btc=-5.0),
        _cand("DELTA/USDT", volume_ratio=3.0),
    ]
    res = DiscoveryExpansionAgent().run(candidates=cs, mode="scalp")
    for c in res.candidates:
        assert c.candidate_playbook != PLAYBOOK_CRYPTO_SCALP, (
            f"expansion produced a scalp playbook for {c.symbol}; PART 3 invariant violated"
        )


# ---------------------------------------------------------------------------
# Quality gates (PART 4 shadow lane)
# ---------------------------------------------------------------------------


def test_thin_liquidity_blocks_promotion():
    cs = [_cand("THIN/USDT", relative_strength_btc=5.0, quote_volume_24h_usd=500_000)]
    res = DiscoveryExpansionAgent().run(candidates=cs)
    thin = [c for c in res.candidates if c.symbol == "THIN/USDT"]
    assert thin and any("thin_liquidity" in b for b in thin[0].promotion_blockers)


def test_short_squeeze_guard_flags_upper_wick():
    cs = [_cand("WICK/USDT", direction_bias="short",
                relative_strength_btc=-5.0, upper_wick_atr_max=3.5)]
    res = DiscoveryExpansionAgent().run(candidates=cs)
    matches = [c for c in res.candidates if c.symbol == "WICK/USDT"]
    assert matches, "WICK should still appear (informational)"
    assert any("squeeze_risk_upper_wick" in b for b in matches[0].promotion_blockers), (
        "squeeze guard must flag high upper-wick shorts as a promotion blocker"
    )


def test_short_extreme_negative_funding_flags_blocker():
    cs = [_cand("FUND/USDT", direction_bias="short",
                relative_strength_btc=-5.0, upper_wick_atr_max=0.5)]
    derivatives = {"FUND/USDT": {"funding_rate": -0.08}}
    res = DiscoveryExpansionAgent().run(candidates=cs, derivatives=derivatives)
    matches = [c for c in res.candidates if c.symbol == "FUND/USDT"]
    assert matches
    assert any("extreme_negative_funding" in b for b in matches[0].promotion_blockers)


def test_short_missing_derivatives_blocks_promotion():
    cs = [_cand("NODERIV/USDT", direction_bias="short", relative_strength_btc=-5.0)]
    res = DiscoveryExpansionAgent().run(candidates=cs, derivatives={})
    matches = [c for c in res.candidates if c.symbol == "NODERIV/USDT"]
    assert matches
    assert any("derivatives_missing_for_short" in b for b in matches[0].promotion_blockers)


# ---------------------------------------------------------------------------
# In-top-setups handling
# ---------------------------------------------------------------------------


def test_in_top_setups_marked_but_not_dropped():
    cs = [_cand("HOT/USDT", relative_strength_btc=5.0)]
    res = DiscoveryExpansionAgent().run(
        candidates=cs, top_setup_symbols=["HOT/USDT"],
    )
    matches = [c for c in res.candidates if c.symbol == "HOT/USDT"]
    assert matches and matches[0].in_top_setups is True
    assert res.skipped_in_top_setups >= 1


# ---------------------------------------------------------------------------
# Capping
# ---------------------------------------------------------------------------


def test_total_watchlist_capped():
    """If many sources fire, agent caps total to MAX_TOTAL_WATCHLIST."""
    cs = []
    for i in range(40):
        cs.append(_cand(f"SYM{i:02d}/USDT",
                        relative_strength_btc=5.0 + i,
                        return_24h=10.0 + i,
                        volume_ratio=2.0))
    res = DiscoveryExpansionAgent().run(candidates=cs)
    assert len(res.candidates) <= MAX_TOTAL_WATCHLIST


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------


def test_render_markdown_contains_expected_columns():
    cs = [_cand("REND/USDT", relative_strength_btc=5.0)]
    res = DiscoveryExpansionAgent().run(candidates=cs)
    md = render_expansion_watchlist_markdown(res)
    assert "## 7e. Crypto Expansion Watchlist" in md
    assert "Symbol" in md and "Playbook" in md and "Why not A/B" in md
    assert "Informational" in md or "informational" in md
    assert "REND/USDT" in md


def test_empty_result_renders_safely():
    res = DiscoveryExpansionAgent().run(candidates=[])
    md = render_expansion_watchlist_markdown(res)
    assert "## 7e. Crypto Expansion Watchlist" in md
    assert "No expansion candidates" in md


# ---------------------------------------------------------------------------
# Read-only invariant — no DB / signal writes
# ---------------------------------------------------------------------------


def test_agent_does_not_import_sqlite_writes_directly():
    """Spec invariant: the agent must not touch SQLite or send Telegram."""
    import inspect
    from src.agents import discovery_expansion_agent as mod
    src = inspect.getsource(mod)
    # Must not import the notifier, the SQLite store, or the signal registry.
    assert "TelegramNotifier" not in src
    assert "SQLiteStore" not in src
    assert "register_ideas" not in src
    assert "upsert_proposed_signal" not in src
