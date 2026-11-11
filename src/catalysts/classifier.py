"""Catalyst classifier — pure regex/keyword logic, no I/O.

Maps a news_items row (title + source + optional body) into one of the
:data:`src.catalysts.models.CATALYST_TYPES` categories, plus auxiliary
flags: source_quality, low_liquidity_risk, rumour marker.

Stays narrow on patterns to avoid false positives. A single high-
confidence hit is enough to assign a category; multiple hits prefer the
most specific match (order matters in CATEGORY_PATTERNS).
"""

from __future__ import annotations

import re
from typing import Any


# Each entry is (catalyst_type, [regex patterns, case-insensitive]).
# ORDER MATTERS — first match wins. Put most-specific first.
CATEGORY_PATTERNS: list[tuple[str, list[str]]] = [
    # --- Most specific / highest priority -------------------------------
    # PART 6 — stocks-specific catalyst categories (above governance because
    # the patterns are more specific).
    ("earnings_event", [
        r"\b(beats?|misses?|tops?|trails?) (analyst |Wall Street )?(estimates?|consensus|expectations?)\b",
        r"\b(reports?|posts?|delivers?)\b.{0,30}\b(Q[1-4]|quarterly|first[- ]quarter|second[- ]quarter|third[- ]quarter|fourth[- ]quarter) (earnings|results|revenue)\b",
        # Earnings + beat/miss surprise — but REQUIRE EPS or quarterly context to avoid catching crypto "revenue jump"
        r"\b(EPS|earnings) (beat|miss|surprise|surge|jump|tops|trails)\b",
        r"\b(Q[1-4]|quarterly|fiscal[- ]year) (earnings|EPS|revenue|guidance)\b",
        r"\b(raises?|cuts?|lowers?|reduces?|boosts?) (full[- ]year|annual|Q[1-4]|fiscal[- ]year)?\s*(guidance|outlook|forecast)\b",
        r"\bguidance (raised|lowered|cut|reaffirmed|withdrawn)\b",
        r"\bpre[- ]announces?\b.{0,40}\b(earnings|EPS|quarterly revenue)\b",
        r"\bearnings call\b.{0,40}\b(today|tomorrow|tonight|after hours|preview)\b",
    ]),
    ("analyst_action", [
        r"\b(upgrade[ds]?|downgrade[ds]?)\b.{0,40}\b(to |from |stock|shares?|rating)\b",
        r"\b(price target|PT) (raised|cut|lowered|boosted|increased|reduced) (to |from )?\$?\d",
        r"\b(initiates? coverage|reiterate[ds]?|maintain[ds]?)\b.{0,40}\b(buy|sell|hold|outperform|underperform|overweight|underweight)\b",
        r"\b(JPMorgan|Goldman|Morgan Stanley|Bank of America|BofA|Citi|Wells Fargo|Jefferies|Wedbush|Barclays|UBS|Deutsche Bank|Mizuho|Stifel|Piper Sandler|Cowen|Bernstein|Raymond James|RBC|Evercore|HSBC|BMO)\b.{0,30}\b(upgrade|downgrade|raises|cuts|maintains|initiates|reiterates)\b",
        r"\banalysts? (raises?|cuts?|lifts?|lowers?)\b.{0,40}\b(target|estimate|forecast)\b",
        r"\bWall Street (raises?|cuts?|targets?)\b",
    ]),
    ("clinical_milestone", [
        r"\bFDA (approves?|approval|clears?|rejection|priority review|fast track)\b",
        r"\b(Phase [123]|Phase I+|pivotal trial)\b.{0,40}\b(results?|met|missed|success|fail)\b",
        r"\b(EMA|MHRA|PMDA) (approval|clearance|review)\b",
        r"\b(biosimilar|biologics) (approval|clearance|filing|BLA)\b",
        r"\b(NDA|BLA) (submitted|filed|approved)\b",
    ]),
    ("insider_activity", [
        r"\binsider (buys?|bought|purchases?|sells?|sold)\b",
        r"\bForm 4 (filing|disclosure)\b",
        r"\b(CEO|CFO|director)\b.{0,30}\b(buys?|sells?|purchases?|disposes?)\b.{0,40}\bshares?\b",
        r"\b10b5-1 (plan|trading)\b",
    ]),
    ("governance_event", [
        r"\b(foundation|DAO) (cancels|cancelled|cancellation|disbands|dissolves)\b",
        r"\bfailed funding vote\b",
        r"\b(treasury|community) vote\b.{0,30}\b(reject|fail|approve|pass)\b",
        r"\b(DAO|foundation) (votes? |proposal )(reject|fail|pass|approv)",
        r"\b(governance|grant) (proposal )?(rejected|failed)\b",
        r"\b(CEO|CFO|founder|chair) (resigns?|step.down|fires?d|terminated)\b",
    ]),
    ("infrastructure_failure", [
        r"\bmainnet (halts?|outages?|down|stopped|broke|broken)\b",
        r"\bnetwork (halts?|outages?|down|congestion|broken)\b",
        r"\b(chain|node|consensus) (halts?|outages?|failure|stopped)\b",
        r"\b(three|two|multiple|several)\b.{0,40}\b(halts?|outages?)\b",
        r"\bupgrade bug\b.{0,40}\b(outage|halt|crash)\b",
        r"\bnodes? went (down|offline)\b",
    ]),
    ("exploit_hack", [
        r"\bexploit(ed|ing)?\b",
        r"\bhack(ed|ing)?\b",
        r"\bdrained?\b.{0,40}\b(\$|usd|m|million)\b",
        r"\bbackdoor\b",
        r"\bvulnerab(ility|le)\b.{0,40}\b(funds?|loss)\b",
    ]),
    ("legal_risk", [
        r"\bindict(ed|ment|ing)\b",
        r"\bSEC\b.{0,40}\b(charges?|sues|complaint|enforcement|investigation|probe|lawsuit)\b",
        r"\bDOJ\b.{0,40}\b(charges?|sues|investigation|probe|lawsuit)\b",
        r"\b(securities|accounting|wire) fraud\b",
        r"\bauditor (resign|withdrew|step.down|dismissed)\b",
        r"\b(class[- ]action|shareholder) (lawsuit|complaint|filed|sue[ds]?)\b",
        r"\b(going concern|chapter 11|chapter 7)\b",
        r"\b(filed|filing) (a )?lawsuit\b",
        r"\bsubpoena(ed)?\b",
        r"\b(injunction|restraining order)\b.{0,40}\b(crypto|exchange|token)\b",
    ]),
    ("margin_delisting", [
        r"\bmargin\b.{0,30}\b(delist|removal|removed)\b",
        r"\b(delist|remov)\w*\b.{0,40}\bmargin\b",
    ]),
    ("exchange_delisting", [
        r"\bdelist(ed|ing|s)?\b",
        r"\bremoval of (trading|spot) pair",
        r"\btrading halt(ed)?\b",
    ]),
    ("exchange_listing", [
        r"\b(Binance|Coinbase|Bybit|MEXC|OKX|Kraken|Bitget|KuCoin)\b.{0,50}\b(list|listing)\b",
        r"\blist(s|ed|ing)\b.{0,40}\b(spot|perp|futures|pair)\b",
        r"\b(new listing|launches spot trading|launches perpetual)\b",
        r"\b(Binance|Bybit|OKX|MEXC) (Futures|Spot)\b.{0,60}\b(launch|list|add)\b",
        r"\b(USDT?|USDC|US[DⓈ$]?-margined)\b.{0,40}\bperpetual contract\b",
        r"\b(perpetual|spot|futures) (contract|pair)\b.{0,40}\b(launch|live|add)\b",
    ]),
    ("hodler_airdrop", [
        r"\bHODLer airdrop",
        r"\bhodler airdrops\b",
    ]),
    ("airdrop", [
        r"\bairdrop\b",
        r"\bretroactive\b.{0,30}\b(reward|distribution)\b",
    ]),
    ("token_unlock", [
        r"\btoken unlock\b",
        r"\bcliff unlock\b",
        r"\bvesting cliff\b",
        r"\bunlock(ed|s|ing)\b.{0,40}\b(tokens?|supply)\b",
    ]),
    ("buyback_burn", [
        r"\bbuyback\b",
        r"\btoken burn\b",
        r"\bsupply burn\b",
        r"\bdeflation(ary)?\b.{0,30}\b(buyback|burn)\b",
    ]),
    ("partnership", [
        r"\bpartner(s|ship)\b",
        r"\b(integrate|integration) with\b",
        r"\binks (a )?deal\b",
        r"\bteam(s|ed) up with\b",
        r"\bacquisition\b",
        r"\bmerger\b",
        r"\bbuyout\b",
        r"\btakeover\b",
        # Liquidity provisions / market-maker partnerships
        r"\b(Wintermute|Jump Crypto|GSR|DWF Labs|Cumberland)\b.{0,40}\bliquidity\b",
        # "play for X market"
        r"\bmajor (play|push) for\b.{0,40}\bmarket\b",
        # Strategic alliances
        r"\bstrategic (partnership|alliance)\b",
    ]),
    ("mainnet_launch", [
        r"\bmainnet (launch|live|going live|launches)\b",
        r"\bgenesis launch\b",
    ]),
    ("roadmap_event", [
        r"\broadmap\b",
        r"\bupgrade\b.{0,30}\b(scheduled|launches|live)\b",
        r"\bfork\b.{0,30}\b(scheduled|live)\b",
    ]),
    ("regulatory_sector_headline", [
        r"\bregulator(y|s)\b.{0,80}\b(crypto|digital asset|stablecoin|ETF)\b",
        r"\bETF\b.{0,40}\b(approv|launch|filing|inflow|outflow)\b",
        r"\b(approve|approves|approved)\b.{0,30}\bETF\b",
        r"\bstablecoin\b.{0,40}\b(bill|legislation|approval)\b",
        r"\bSEC clarif",
        r"\bCFTC\b.{0,40}\b(crypto|digital|approval|guidance|enforcement)\b",
        r"\bSEC\b.{0,40}\b(approval|guidance|clarif)\b",
        r"\bfederal reserve\b.{0,60}\b(crypto|stablecoin)\b",
        r"\b(MiCA|FATF|FSB)\b.{0,60}\b(crypto|digital|stablecoin)\b",
        # ETF flows context — handle plural "outflows" / "inflows"
        r"\bspot ETF\b.{0,40}\b(outflows?|inflows?)\b.{0,30}\b(record|hit|top|peak)\b",
        r"\bETF\b.{0,30}\b(inflows?|outflows?)\b.{0,30}\b\$?\d",
        r"\bspot ETF\b.{0,40}\b(outflows?|inflows?)\b",
        # US Congress / political
        r"\b(US |U\.S\. )?Congress\b.{0,60}\b(crypto|stablecoin|GENIUS|CLARITY|bill)\b",
        r"\bGENIUS (Act|comments?)\b",
        r"\bCLARITY Act\b",
        # Country-level launches
        r"\b(bank|rupee|fiat) rails?\b",
        r"\b(FIU|RBI|MAS|FCA|BaFin) (nod|approval|registration)\b",
        # Institutional forecasts (handle plural "predicts" + "tokenized")
        r"\b(Citi|Citigroup|JPMorgan|Goldman|Morgan Stanley|BlackRock)\b.{0,40}\b(predicts?|forecasts?|estimates?)\b.{0,60}\btokeniz\w*\b",
        # IRS / treasury
        r"\b(IRS|Treasury) (guidance|rule|crypto)\b",
    ]),
    ("platform_growth", [
        r"\b(record|all[- ]time high)\b.{0,40}\b(volume|TVL|users|TPS|active wallets)\b",
        r"\b\$\d+(\.\d+)?\s*(T|B|M)\b.{0,40}\b(cumulative|total) volume\b",
        r"\bperpetual DEX\b.{0,40}\b(top|second|largest)\b",
        r"\bTVL\b.{0,40}\b(surge|spike|growth|rise|increase|ATH|all[- ]time high)\b",
        r"\b(surge|spike|growth|rise|jump)\b.{0,40}\bTVL\b",
        r"\b(revenue|fees)\b.{0,40}\b(growth|surge|ATH|all[- ]time high)\b",
        r"\b(daily|weekly|monthly) (active )?users\b.{0,40}\b(record|ATH|growth)\b",
    ]),
    ("official_product_teaser", [
        r"\bteased?\b.{0,40}\b(launch|product|reveal)\b",
        r"\bhints? at\b.{0,40}\b(launch|partnership|product)\b",
        r"\bcryptic\b.{0,40}\b(tweet|post|hint)\b",
    ]),
    ("product_launch", [
        r"\bunveil(s|ed|ing)\b",
        r"\b(launch|release)\b.{0,30}\b(today|new|product|app|feature)\b",
        r"\bgoes live\b",
    ]),
    ("social_narrative", [
        r"\bgoes viral\b",
        r"\btrending on\b.{0,30}\b(twitter|X|reddit|telegram)\b",
        r"\bmeme(coin)? rotation\b",
        r"\bnarrative\b.{0,30}\b(rotation|heating)\b",
    ]),
    ("rumour_only", [
        r"\brumor(s|ed)?\b",
        r"\brumour(s|ed)?\b",
        r"\b(unconfirm|alleg)\b",
        r"\bspeculation\b",
        r"\bsources? say\b",
    ]),
    ("low_liquidity_event", [
        r"\bthin (liquidity|orderbook|book)\b",
        r"\billiquid\b",
        r"\blow[- ]float\b",
        r"\bfan token\b",
        # Infrastructure failures = liquidity/reliability risk
        r"\bmainnet (halt|outage|down|stopped)\b",
        r"\bnetwork (halt|outage|down)\b",
        r"\bchain (halt|outage|congestion)\b",
        r"\b(three|two|multiple) (mainnet )?(halt|outage)s?\b",
        r"\bupgrade bug\b",
    ]),
    ("sell_the_news_risk", [
        r"\bsell[- ]the[- ]news\b",
        r"\bpriced in\b",
        r"\bbuy the rumor, sell the news\b",
    ]),
]


# Source quality classification by source name (lowercased substring match).
PRIMARY_SOURCES = (
    "binance announcements",
    "coinbase announcements",
    "bybit announcements",
    "okx announcements",
    "kraken announcements",
    "company ir",
    "sec filing",
    "sec.gov",
    "stellar.org",
    "ethereum.org",
)
SINGLE_SOURCES = (
    "coindesk", "cointelegraph", "decrypt", "the block", "theblock",
    "cnbc", "bloomberg", "reuters", "yahoo finance", "ft.com",
    "crypto briefing", "cryptotimes", "ambcrypto", "blockonomi",
    "mexc news", "coinmarketcap", "coingecko", "cryptorank",
    "bitcoinist", "u.today", "kiplinger", "banklesstimes",
    "ainvest", "investingnews", "thedefiant", "unchained",
)
SOCIAL_SOURCES = (
    "twitter", "x.com", "telegram", "reddit", "discord",
)


def classify_catalyst_type(title: str, body: str = "") -> str:
    """Return the most-specific catalyst category for a news item.

    Falls back to ``"other_news"`` if nothing matches.
    """

    text = f"{title}\n{body}".lower()
    for category, patterns in CATEGORY_PATTERNS:
        for pat in patterns:
            if re.search(pat, text, re.IGNORECASE):
                return category
    return "other_news"


def classify_source_quality(source: str) -> str:
    """Return one of: ``primary_source`` / ``single_source`` /
    ``social_only`` / ``unverifiable``.
    """

    if not source:
        return "unverifiable"
    s = source.lower()
    if any(p in s for p in PRIMARY_SOURCES):
        return "primary_source"
    if any(p in s for p in SOCIAL_SOURCES):
        return "social_only"
    if any(p in s for p in SINGLE_SOURCES):
        return "single_source"
    return "single_source"  # default safe bucket


def detect_low_liquidity_risk(title: str, body: str = "") -> bool:
    """True for tokens / events flagged as thin-liquidity / fan-token /
    delisting consequences. Used as an avoid-chase hint."""

    text = f"{title}\n{body}".lower()
    patterns = (
        r"\bdelist(ed|ing|s)?\b",
        r"\bmargin (delist|remov)",
        r"\bthin (liquidity|orderbook|book)\b",
        r"\billiquid\b",
        r"\bfan token\b",
        r"\blow[- ]float\b",
    )
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def detect_rumour_marker(title: str, body: str = "") -> bool:
    """True iff the headline reads as rumour / unconfirmed."""

    text = f"{title}\n{body}".lower()
    patterns = (
        r"\brumor(s|ed)?\b", r"\brumour(s|ed)?\b",
        r"\b(unconfirm|alleg)\b",
        r"\bspeculation\b",
        r"\bsources? say\b",
    )
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def is_test_source(source: str) -> bool:
    """Match SQLiteStore.TEST_NEWS_SOURCES — reject test_source / fixture."""

    if not source:
        return False
    s = source.strip().lower()
    return s in {"test_source", "test-source", "test", "fixture"}


# ---------------------------------------------------------------------------
# Importance scoring (PART — catalyst prioritization fix)
#
# Produces a normalized [0,1] prioritization score for a single catalyst.
# This is a *ranking aid only* — it does NOT feed trading logic, scoring
# thresholds, or any auto-trade path. It exists so the enriched-review and
# report layers can surface the most consequential catalysts first instead
# of falling back to insertion order (every row previously serialized with
# no importance field → all 0.0).
#
# Pure function, deterministic, no I/O.
# ---------------------------------------------------------------------------


# Per-catalyst-type base severity in [0,1]. Higher = more market-moving /
# more decision-relevant. Covers every entry in models.CATALYST_TYPES.
TYPE_SEVERITY: dict[str, float] = {
    "exploit_hack": 0.95,
    "legal_risk": 0.95,
    "infrastructure_failure": 0.90,
    "exchange_delisting": 0.85,
    "earnings_event": 0.85,
    "clinical_milestone": 0.85,
    "margin_delisting": 0.80,
    "token_unlock": 0.80,
    "regulatory_sector_headline": 0.80,
    "mainnet_launch": 0.78,
    "exchange_listing": 0.78,
    "hodler_airdrop": 0.70,
    "governance_event": 0.70,
    "buyback_burn": 0.65,
    "analyst_action": 0.60,
    "partnership": 0.60,
    "product_launch": 0.55,
    "airdrop": 0.55,
    "official_product_teaser": 0.50,
    "platform_growth": 0.50,
    "insider_activity": 0.50,
    "sell_the_news_risk": 0.45,
    "low_liquidity_event": 0.45,
    "roadmap_event": 0.45,
    "social_narrative": 0.40,
    "momentum_breakout": 0.40,
    "rumour_only": 0.30,
    "other_news": 0.15,
}
_DEFAULT_TYPE_SEVERITY = 0.30

# Per-source-quality weight in [0,1] (official vs social-only axis).
SOURCE_QUALITY_WEIGHT: dict[str, float] = {
    "primary_source": 1.00,
    "single_source": 0.60,
    "social_only": 0.30,
    "unverifiable": 0.10,
}

# Tier-1 names that carry market-wide read-through regardless of the
# specific headline. Base ticker (no "/USDT" suffix, upper-cased).
MAJOR_SYMBOLS: frozenset[str] = frozenset({
    # Crypto majors
    "BTC", "ETH", "SOL", "XRP", "BNB", "DOGE", "ADA", "AVAX", "LINK",
    "TRX", "TON", "DOT", "MATIC", "POL", "LTC", "BCH", "SHIB", "XLM",
    "HYPE", "SUI", "NEAR", "APT", "ATOM", "UNI", "AAVE", "ONDO", "ENA",
    # Stock / equity majors most relevant to this desk's universe
    "NVDA", "AMD", "AVGO", "AAPL", "MSFT", "GOOGL", "GOOG", "META",
    "AMZN", "TSLA", "SMCI", "MSTR", "COIN", "QQQ", "SPY", "SMH", "XLK",
})

# Catalyst types that are market-relevant even with no mapped symbol
# (they move the whole tape / sector, not a single ticker).
_MARKET_WIDE_TYPES: frozenset[str] = frozenset({
    "regulatory_sector_headline",
})

# Geopolitical / macro-shock keywords. A hit lifts severity because these
# events drive broad risk-off regardless of which symbol they tag (e.g. the
# Strait-of-Hormuz / Iran cluster the enriched-review surfaced).
_GEOPOLITICAL_RE = re.compile(
    r"\b("
    r"war|warfare|missile|drone|airstrike|air strike|strike[ds]?|"
    r"sanction(s|ed)?|embargo|blockade|tariff(s)?|"
    r"iran|israel|gaza|hormuz|kuwait|ukraine|russia|taiwan|"
    r"military|conflict|invasion|ceasefire|nuclear|"
    r"central command|centcom|geopolit"
    r")\b",
    re.IGNORECASE,
)


def detect_geopolitical_severity(title: str, body: str = "") -> bool:
    """True iff the headline reads as a geopolitical / macro-shock event."""

    return bool(_GEOPOLITICAL_RE.search(f"{title}\n{body}"))


def _freshness_subscore(freshness_hours: float | None) -> float:
    """Map age-in-hours to a [0,1] recency weight (newer = higher)."""

    if freshness_hours is None:
        return 0.30  # unknown publish time — neutral-low, not zero
    h = max(0.0, float(freshness_hours))
    if h <= 1:
        return 1.00
    if h <= 3:
        return 0.90
    if h <= 6:
        return 0.80
    if h <= 12:
        return 0.60
    if h <= 24:
        return 0.45
    if h <= 48:
        return 0.30
    if h <= 72:
        return 0.20
    return 0.10


def _mapping_subscore(symbol: str, related_symbols: list[str] | None) -> float:
    """Reward a confidently-mapped single symbol; penalize basket-level
    (unmapped) rows and very diffuse multi-symbol mentions."""

    n_related = len(related_symbols or [])
    if not (symbol or "").strip():
        return 0.30  # basket-level / unmapped — least actionable
    if n_related == 0:
        return 1.00  # one clean symbol — most specific
    if n_related <= 2:
        return 0.85
    return 0.70  # mentions many symbols — diffuse


def _market_relevance_subscore(
    symbol: str, related_symbols: list[str] | None, catalyst_type: str
) -> float:
    """Boost tier-1 names and market-wide catalyst types."""

    def _base(sym: str) -> str:
        return (sym or "").strip().upper().split("/")[0]

    syms = {_base(symbol), *(_base(s) for s in (related_symbols or []))}
    syms.discard("")
    if syms & MAJOR_SYMBOLS:
        return 1.00
    if catalyst_type in _MARKET_WIDE_TYPES:
        return 0.60
    if syms:
        return 0.55  # a real, mapped but non-major symbol
    return 0.35  # nothing mapped, not market-wide


def _severity_subscore(catalyst_type: str, title: str) -> float:
    """Legal / security / geopolitical severity component."""

    if catalyst_type in {"legal_risk", "exploit_hack", "infrastructure_failure"}:
        return 1.00
    if detect_geopolitical_severity(title):
        return 0.90
    if catalyst_type in {"regulatory_sector_headline", "exchange_delisting", "margin_delisting"}:
        return 0.60
    return 0.20  # baseline so the (small-weight) component is never zero


# Component weights — sum to 1.0 so the weighted average stays in [0,1].
_WEIGHTS: dict[str, float] = {
    "type": 0.30,
    "source": 0.22,
    "freshness": 0.18,
    "mapping": 0.12,
    "relevance": 0.10,
    "severity": 0.08,
}


def score_importance(
    *,
    catalyst_type: str,
    source_quality: str,
    freshness_hours: float | None,
    symbol: str = "",
    related_symbols: list[str] | None = None,
    title: str = "",
    is_rumour: bool = False,
) -> float:
    """Return a normalized [0,1] importance score for one catalyst.

    Blends seven signals the operator asked for:
      * catalyst type severity      (TYPE_SEVERITY)
      * source quality              (SOURCE_QUALITY_WEIGHT)
      * freshness                   (newer = higher)
      * symbol mapping confidence   (mapped single symbol > basket-level)
      * official vs social-only     (folded into source quality + rumour modifier)
      * market relevance            (tier-1 names / market-wide types)
      * legal/security/geopolitical severity

    A rumour / unverifiable modifier discounts the final value. Ranking aid
    only — no effect on trading logic or thresholds.
    """

    type_s = TYPE_SEVERITY.get(catalyst_type, _DEFAULT_TYPE_SEVERITY)
    source_s = SOURCE_QUALITY_WEIGHT.get(source_quality, 0.40)
    fresh_s = _freshness_subscore(freshness_hours)
    map_s = _mapping_subscore(symbol, related_symbols)
    rel_s = _market_relevance_subscore(symbol, related_symbols, catalyst_type)
    sev_s = _severity_subscore(catalyst_type, title)

    base = (
        _WEIGHTS["type"] * type_s
        + _WEIGHTS["source"] * source_s
        + _WEIGHTS["freshness"] * fresh_s
        + _WEIGHTS["mapping"] * map_s
        + _WEIGHTS["relevance"] * rel_s
        + _WEIGHTS["severity"] * sev_s
    )

    # Confidence modifier (official vs social-only / rumour axis).
    modifier = 1.0
    if is_rumour or catalyst_type == "rumour_only":
        modifier *= 0.70
    if source_quality == "unverifiable":
        modifier *= 0.70
    elif source_quality == "social_only":
        modifier *= 0.90

    return round(max(0.0, min(1.0, base * modifier)), 3)
