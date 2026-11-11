"""Narrative basket clustering.

Takes a list of :class:`CatalystEvent` and groups them into
:class:`NarrativeBasket` instances based on:

1. **Shared narrative tag** (we set this during classification, e.g.
   "bnb_chain_airdrop", "perps_dex", "delisting_thin_liquidity").
2. **Shared catalyst type** for cross-symbol events (exploit on BNB
   Chain → BNB + ASTER both flagged).
3. **Static well-known baskets** (BNB+ASTER on GENIUS airdrop, HYPE on
   Hyperliquid/perps, HEI+PSG+NFP on delisting/thin liq).

The clustering is intentionally simple — it is **enrichment**, not
strategy. A basket only adds context flags; it does not change scoring.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from src.catalysts.models import CatalystEvent, NarrativeBasket


# Static narrative baskets — symbols that we want to keep grouped even
# when news only mentions one of them. Keys are basket_name; values are
# the canonical symbol list. The first symbol is treated as "primary".
STATIC_BASKETS: dict[str, dict[str, list[str]]] = {
    "binance_ecosystem_teaser": {
        "primary": ["BNB/USDT"],
        "related": ["ASTER/USDT"],
    },
    "perps_dex_narrative": {
        "primary": ["HYPE/USDT"],
        "related": ["DYDX/USDT", "GMX/USDT", "ASTER/USDT"],
    },
    "delisting_thin_liquidity": {
        "primary": [],  # populated from events
        "related": [],
    },
    "ai_narrative": {
        "primary": ["NEAR/USDT", "RENDER/USDT", "TAO/USDT", "FET/USDT"],
        "related": ["WLD/USDT", "ASTER/USDT"],
    },
    "rwa_narrative": {
        "primary": ["ONDO/USDT", "XLM/USDT"],
        "related": [],
    },
}


# Narrative tags assigned by basket-builder when an event triggers a
# basket. These are stored on the CatalystEvent.narrative field.
NARRATIVE_TAGS = {
    "binance_ecosystem_teaser": "bnb_ecosystem_teaser",
    "perps_dex_narrative": "perps_dex",
    "delisting_thin_liquidity": "delisting_thin_liq",
    "ai_narrative": "ai_rotation",
    "rwa_narrative": "rwa_institutional",
}


def _normalize_symbol(s: str) -> str:
    s = s.strip().upper()
    if not s:
        return s
    if "/" not in s:
        s = f"{s}/USDT"
    return s


def _basket_for_event(event: CatalystEvent) -> str | None:
    """Match a single event to a static basket name.

    Returns the basket_name or None.
    """

    symbols = {_normalize_symbol(event.symbol), *map(_normalize_symbol, event.related_symbols)}
    symbols.discard("")

    # delisting / thin-liquidity: anything that classified as delisting,
    # margin_delisting, or low_liquidity_event lands here regardless of
    # symbol.
    if event.catalyst_type in {
        "exchange_delisting", "margin_delisting", "low_liquidity_event",
    }:
        return "delisting_thin_liquidity"

    for basket_name, members in STATIC_BASKETS.items():
        if basket_name == "delisting_thin_liquidity":
            continue  # handled above
        all_members = {*members["primary"], *members["related"]}
        if symbols & set(all_members):
            return basket_name

    return None


def build_narrative_baskets(events: Iterable[CatalystEvent]) -> list[NarrativeBasket]:
    """Cluster a list of CatalystEvent into NarrativeBasket records.

    Side-effect-free; events are NOT mutated.
    """

    by_basket: dict[str, list[CatalystEvent]] = defaultdict(list)
    for event in events:
        name = _basket_for_event(event)
        if name is not None:
            by_basket[name].append(event)

    baskets: list[NarrativeBasket] = []
    for name, members in by_basket.items():
        if name == "delisting_thin_liquidity":
            # build dynamic basket from member symbols
            primary = sorted(
                {_normalize_symbol(e.symbol) for e in members if e.symbol}
            )
            related: list[str] = []
        else:
            spec = STATIC_BASKETS[name]
            primary = list(spec["primary"])
            related = list(spec["related"])

        # Worst-case basket source_quality = best of its events; freshness = min hours.
        order = {"primary_source": 3, "single_source": 2, "social_only": 1, "unverifiable": 0}
        sq = max(members, key=lambda e: order.get(e.source_quality, 0)).source_quality
        fresh_values = [e.freshness_hours for e in members if e.freshness_hours is not None]
        if not fresh_values:
            fresh = "unknown"
        elif min(fresh_values) < 1:
            fresh = "<1h"
        elif min(fresh_values) < 6:
            fresh = "<6h"
        elif min(fresh_values) < 24:
            fresh = "<24h"
        else:
            fresh = "stale"

        # Suggested playbook from basket name.
        playbook = _basket_playbook(name, members)

        summary = _basket_summary(name, members)

        basket = NarrativeBasket(
            basket_name=name,
            primary_symbols=primary,
            related_symbols=related,
            catalyst_summary=summary,
            source_quality=sq,
            freshness=fresh,
            event_ids=[e.catalyst_id for e in members],
            suggested_playbook=playbook,
            # symbols_moved / lagging / overextended / blocked are kept
            # empty here — they're populated by the report builder
            # which has access to live price/volume data. The basket
            # itself is news-derived only.
        )
        baskets.append(basket)
    return baskets


def _basket_playbook(name: str, members: list[CatalystEvent]) -> str:
    if name == "delisting_thin_liquidity":
        return "avoid_low_liquidity"
    if name == "binance_ecosystem_teaser":
        if any(e.catalyst_type == "rumour_only" for e in members):
            return "sell_the_news_watch"
        return "related_beta_rotation"
    if name == "perps_dex_narrative":
        return "wait_pullback"
    if name in {"ai_narrative", "rwa_narrative"}:
        return "related_beta_rotation"
    if name == "momentum_breakout":
        # Pure-momentum cluster without confirmed catalyst — default
        # stance is wait for pullback / avoid chase. If any member has a
        # known overextension flag we tighten to avoid_chase.
        if any(e.overextension_risk for e in members):
            return "avoid_chase"
        return "wait_pullback"
    return "wait_pullback"


def _basket_summary(name: str, members: list[CatalystEvent]) -> str:
    titles = [m.title for m in members if m.title][:3]
    sample = "; ".join(titles)[:300]
    label = {
        "binance_ecosystem_teaser":
            "Binance ecosystem catalyst — BNB/ASTER and related; "
            "early rotation / sell-the-news risk.",
        "perps_dex_narrative":
            "Hyperliquid / perps DEX narrative — HYPE + related DEX/derivatives names.",
        "delisting_thin_liquidity":
            "Delisting / thin-liquidity capitulation — avoid chasing low-float dumps.",
        "ai_narrative":
            "AI sector rotation — multi-symbol momentum, watch for crowding.",
        "rwa_narrative":
            "RWA / tokenization institutional — multi-week thesis (DTCC/Stellar etc).",
        "momentum_breakout":
            "Top gainers without confirmed news catalyst — pure momentum cluster. "
            "Watch for volume confirmation; avoid chase if >2 ATR extended.",
    }.get(name, name)
    return f"{label} Sample headlines: {sample}" if sample else label


# ---------------------------------------------------------------------------
# Momentum-breakout basket (PART 5 fix — surface "new gainers")
# ---------------------------------------------------------------------------


def build_momentum_breakout_basket(
    movers: list[dict],
    *,
    min_24h_pct: float = 10.0,
    min_volume_ratio: float = 0.5,
    catalyst_symbols: set[str] | None = None,
) -> NarrativeBasket | None:
    """Build a `momentum_breakout` basket from the latest scalp/intraday
    top-movers list (PART 5 fix — surface "new gainers" even without news).

    ``movers`` is a list of dicts with keys:
        - symbol (str, e.g. "PORTAL/USDT")
        - score (float)
        - return_24h_pct (float)
        - volume_ratio (float)
        - overextension_risk (bool, optional)

    Returns a basket or ``None`` if no qualifying movers.

    Filtering rules:
    * 24h pct >= ``min_24h_pct`` (default 10%)
    * volume ratio >= ``min_volume_ratio`` (default 0.5×)
    * Up to 6 members; sorted by 24h pct descending.
    """

    qualified = [
        m for m in movers
        if (m.get("return_24h_pct") or 0) >= min_24h_pct
        and (m.get("volume_ratio") or 0) >= min_volume_ratio
    ]
    if not qualified:
        return None

    qualified.sort(key=lambda m: -(m.get("return_24h_pct") or 0))
    qualified = qualified[:6]

    primary = [_normalize_symbol(m["symbol"]) for m in qualified[:3]]
    related = [_normalize_symbol(m["symbol"]) for m in qualified[3:]]
    overextended = [
        _normalize_symbol(m["symbol"]) for m in qualified
        if bool(m.get("overextension_risk"))
    ]

    movers_summary = ", ".join(
        f"{m['symbol']} +{m.get('return_24h_pct', 0):.1f}% "
        f"(vol {m.get('volume_ratio', 0):.2f}x)"
        for m in qualified[:5]
    )

    # PART 1 catalyst-integrity fix: never blanket-label these movers "no confirmed
    # news catalyst" without a DIRECT news_items check. `catalyst_symbols` is a set of
    # base tickers (e.g. {"ASTER"}) that have a recent high-importance symbol-tagged
    # news row. Any mover in that set is catalyst-backed (overextended → watch pullback,
    # NOT chase) and must NOT be called no-catalyst. (Label/enrichment only — does not
    # change scoring, entries, or promote anything to actionable.)
    cat = {s.split("/")[0].upper() for s in (catalyst_symbols or set())}
    catalyst_backed = [_normalize_symbol(m["symbol"]) for m in qualified
                       if m["symbol"].split("/")[0].upper() in cat]
    no_catalyst = [_normalize_symbol(m["symbol"]) for m in qualified
                   if m["symbol"].split("/")[0].upper() not in cat]

    if catalyst_backed:
        catalyst_summary = (
            f"Momentum cluster (news_items-checked). "
            f"CATALYST-BACKED: {', '.join(catalyst_backed)} — treat as catalyst-backed, "
            f"watch pullback / do NOT chase; NOT a no-catalyst momentum chase. "
            f"Without confirmed catalyst: {', '.join(no_catalyst) or 'none'}. "
            f"Movers: {movers_summary}. Threshold: 24h >= {min_24h_pct}%, vol >= {min_volume_ratio}x."
        )
    else:
        catalyst_summary = (
            f"Top gainers without confirmed news catalyst — pure momentum cluster. "
            f"Movers: {movers_summary}. "
            f"Threshold: 24h >= {min_24h_pct}%, vol >= {min_volume_ratio}x."
        )

    # Catalyst-backed-but-extended → watch pullback (the correct ASTER read), not a blind
    # avoid_chase; pure no-catalyst overextension stays avoid_chase.
    if catalyst_backed:
        playbook = "wait_pullback"
    else:
        playbook = "avoid_chase" if overextended else "wait_pullback"

    return NarrativeBasket(
        basket_name="momentum_breakout",
        primary_symbols=primary,
        related_symbols=related,
        catalyst_summary=catalyst_summary,
        source_quality="single_source",  # derived from internal report data
        freshness="<1h",  # built from latest report
        symbols_overextended=overextended,
        suggested_playbook=playbook,
        event_ids=[],
    )
