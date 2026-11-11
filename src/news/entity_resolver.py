"""Production news entity/narrative resolver — the layer that decides WHAT a headline is about,
BEFORE it reaches crypto/stocks scoring context, enriched review, catalyst labels and diagnostics.

READ-MODEL / enrichment only. It NEVER touches live, final_r, signal_outcomes, score, tier, TP/SL, or
routing. It additively enriches `news_items` (union-only on detected_symbols/narratives + new entity
columns). It does NOT auto-promote or auto-trade off a news item.

It reuses the boundary/case-safe `EntityAliasMatcher` (crypto + stocks) and adds:
  * text extraction across title / raw_json summary·description·body·text·content / url slug / structured
    SEC·DefiLlama fields (future-proof: uses whatever text a row actually carries),
  * a crypto exchange-listing parser (`MEXC to list XYZUSDT` → XYZ/USDT tradable, else untracked_entity),
  * macro / geopolitics event tagging (no forced symbol),
  * cross-asset detection (a stock named in a crypto-classified row, and vice-versa),
each carrying a match reason / source / confidence and an asset_impact_scope + tradability_status.
"""

from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

RESOLVER_VERSION = "entity_resolver_v8"
_ROOT = Path(__file__).resolve().parents[2]

# additive nullable columns on news_items (idempotent migration).
_NEW_COLUMNS = (
    ("detected_entities_json", "TEXT"), ("event_tags_json", "TEXT"),
    ("entity_match_confidence", "REAL"), ("entity_match_reason", "TEXT"),
    ("entity_match_source", "TEXT"), ("asset_impact_scope", "TEXT"),
    ("tradability_status", "TEXT"), ("resolved_at", "TEXT"), ("resolver_version", "TEXT"),
    # trust layer (2026-07-08): only symbols with real provenance may drive catalyst/news_supported.
    ("trusted_symbols_json", "TEXT"), ("resolution_status", "TEXT"),
    ("resolution_trigger", "TEXT"), ("resolution_latency_seconds", "REAL"),
)

# real-matcher sources whose hits are trustworthy for catalyst/news_supported linkage.
TRUSTED_SOURCES = frozenset({
    "alias_crypto", "alias_stocks", "issuer_alias", "issuer_cik", "listing_parser", "cross_asset", "cashtag",
    "headline_issuer_alias", "provider_symbol",
})

_TRUSTED_PROVIDER_SYMBOL_SOURCES = frozenset({"finnhub company-news"})

# Short ETF / acronym tickers that collide with everyday words or non-financial acronyms ("DIA Approval"
# = Defense Intelligence Agency, not the Dow ETF). A bare uppercase token is NOT enough — they require a
# cashtag ($DIA) or an explicit ETF/company alias to be a trusted catalyst symbol.
AMBIGUOUS_TICKERS = frozenset({
    "DIA", "SPY", "QQQ", "IWM", "SMH", "XLF", "XLE", "XLK", "XLV", "XLY", "DXY", "SOXX", "VOO", "VTI",
    "ARB", "OP", "ONE", "NEAR", "LINK", "FLOW", "INJ", "ADA", "TON", "SUI", "APT", "SEI", "TIA", "FET",
})

# macro / geopolitics event tags — keyword → tag. NEVER forces a tradable symbol.
_MACRO_TAGS: dict[str, tuple[str, ...]] = {
    "rates": ("interest rate", "rate cut", "rate hike", "rate decision", "basis points", "bps cut"),
    "inflation": ("inflation", "cpi", "pce", "core cpi", "disinflation"),
    "jobs": ("jobs report", "nonfarm", "non-farm", "payrolls", "unemployment", "jobless claims"),
    "fed": ("federal reserve", "the fed", "fomc", "powell", "jerome powell", "rate-setting"),
    "yields": ("treasury yield", "10-year yield", "bond yield", "yields"),
    "dxy": ("dollar index", "dxy", "u.s. dollar", "us dollar strength"),
    "oil": ("crude oil", "oil price", "brent", "wti", "opec"),
    "tariffs": ("tariff", "tariffs", "trade war", "import duties"),
    "geopolitics": ("geopolit", "military strike", "airstrike", "invasion", "ceasefire"),
    "war": ("war", "missile", "drone strike", "conflict escalation"),
    "sanctions": ("sanction", "sanctions", "export control"),
    "middle_east": ("middle east", "israel", "iran", "gaza", "hezbollah", "red sea"),
    "china_taiwan": ("china", "taiwan", "beijing", "pboc", "yuan", "renminbi"),
    "crypto_regulation": ("sec charges", "sec sues", "crypto regulation", "mica", "genius act",
                          "crypto bill", "regulatory clarity", "cftc"),
    "stablecoin_regulation": ("stablecoin bill", "stablecoin regulation", "stablecoin law"),
    "etf": ("spot etf", "etf approval", "etf inflow", "etf outflow", "etf filing"),
}

# exchange / stablecoin narrative tags (event context, not always a trade symbol).
_EXCHANGES = ("binance", "coinbase", "bybit", "mexc", "okx", "kraken", "kucoin", "upbit", "bitget",
              "gate.io", "crypto.com", "gemini")
_STABLECOINS = {"USDT": "tether", "USDC": "usd coin", "DAI": "dai", "PYUSD": "paypal usd",
                "RLUSD": "ripple usd", "FDUSD": "first digital usd", "TUSD": "trueusd"}
_LISTING_KEYWORDS = ("to list", "will list", "lists ", "listing", "to add", "adds ", "has listed",
                     "innovation zone", "main board", "perpetual", "spot trading", "delist", "will add",
                     "opens trading")
# tokens that look like tickers but must never be emitted as a symbol from the listing parser.
_TICKER_STOP = frozenset({
    "MEXC", "OKX", "USDT", "USDC", "USD", "CEO", "CFO", "USA", "SEC", "CFTC", "ETF", "IPO", "AI", "API",
    "DAO", "NFT", "DeFi", "DEFI", "GDP", "CPI", "PCE", "FOMC", "FED", "BUY", "SELL", "NEW", "THE", "AND",
    "FOR", "ALL", "NOW", "TOP", "WEB", "APP", "LLC", "INC", "ETH", "BTC",   # majors handled by alias path
    "FUTURES", "FUTURE", "SPOT", "PERPETUAL", "TRADING", "TRADE", "ZONE", "MARGIN", "CROSS",
    "ISOLATED", "PAIR", "PAIRS", "LISTING", "LIST", "TOKEN", "TOKENS", "PRE", "IPO", "MARKET",
    "UTC", "NASDAQ", "NYSE", "NYSEAMERICAN", "TSX", "TSXV", "PREIPO",
})
_SOCIAL_PREFIX = ("t.me/", "twitter", "x.com", "reddit")
_OFFICIAL = ("sec", "edgar", "pr newswire", "globenewswire", "business wire", "businesswire",
             "binance announcements", "federal reserve")
_REPUTABLE = ("coindesk", "cointelegraph", "the block", "reuters", "bloomberg", "yahoo finance", "motley fool",
              "cnbc", "marketwatch", "wall street journal", "financial times", "decrypt", "cryptoslate")

_CASHTAG = re.compile(r"[$#]([A-Za-z]{2,10})\b")
_LISTING_PAIR = re.compile(r"(?<![A-Z0-9])([A-Z0-9]{2,20}?)(?:USDT|USDC|USD)(?![A-Z0-9])")
_LISTING_TOKEN = re.compile(r"(?<![A-Z0-9])[$#]?([A-Z][A-Z0-9]{1,19})(?![A-Z0-9])")


# ---- schema migration -------------------------------------------------------------------------
def ensure_news_entity_columns(conn) -> None:
    """Idempotent additive migration — adds the resolver columns to news_items. Never drops / never
    deletes rows. Safe to call repeatedly and on an old schema."""
    existing = {r[1] for r in conn.execute("PRAGMA table_info(news_items)")}
    for col, typ in _NEW_COLUMNS:
        if col not in existing:
            try:
                conn.execute(f"ALTER TABLE news_items ADD COLUMN {col} {typ}")
            except Exception:
                pass


# ---- text extraction --------------------------------------------------------------------------
def _load_raw(row) -> dict:
    raw = row.get("raw_json")
    if isinstance(raw, dict):
        return raw
    try:
        return json.loads(raw) if raw else {}
    except (TypeError, ValueError):
        return {}


def _url_slug(url: str | None) -> str:
    if not url:
        return ""
    try:
        tail = re.sub(r"[?#].*$", "", str(url)).rstrip("/").rsplit("/", 1)[-1]
        tail = re.sub(r"\.(html?|php|aspx?)$", "", tail)
        return re.sub(r"[-_]+", " ", tail)
    except Exception:
        return ""


def extract_text_fields(row: dict) -> dict[str, str]:
    """All matchable text a row actually carries. Body/summary keys are read defensively so the resolver
    improves automatically if future ingest persists them; today most rows expose title + url slug (+
    structured SEC/DefiLlama fields)."""
    raw = _load_raw(row)
    title = str(row.get("title") or raw.get("title") or "")
    summary = str(raw.get("summary") or "")
    description = str(raw.get("description") or "")
    body = str(row.get("content_text") or raw.get("body") or raw.get("text") or
               raw.get("content") or raw.get("message") or "")
    # structured provider fields (SEC EDGAR / DefiLlama) carry ticker/protocol names as text.
    structured = " ".join(str(raw.get(k) or "") for k in ("ticker", "protocol", "protocol_symbol",
                                                           "symbol", "company", "event_type"))
    slug = _url_slug(row.get("url") or raw.get("url"))
    combined = " ".join(x for x in (title, summary, description, body, structured, slug) if x).strip()
    return {"title": title, "summary": summary, "description": description, "body": body,
            "url_slug": slug, "structured": structured, "combined": combined}


def _source_quality_hint(source: str | None) -> str:
    s = str(source or "").lower()
    if any(s.startswith(p) or p in s for p in _SOCIAL_PREFIX):
        return "social"
    if any(o in s for o in _OFFICIAL):
        return "official"
    if any(r in s for r in _REPUTABLE):
        return "reputable"
    return "unknown"


# ---- specialised taggers ----------------------------------------------------------------------
def _keyword_match(text: str, keyword: str) -> bool:
    """Match a word/phrase without substring false positives (Warsh, awards, warns)."""
    value = str(keyword or "").strip().lower()
    if not value:
        return False
    escaped = re.escape(value)
    suffix = r"(?:s)?" if " " not in value else ""
    return bool(re.search(rf"(?<![A-Za-z0-9]){escaped}{suffix}(?![A-Za-z0-9])", text.lower()))


def _macro_event_tags(text: str) -> list[str]:
    low = text.lower()
    tags = {tag for tag, kws in _MACRO_TAGS.items() if any(_keyword_match(text, k) for k in kws)}
    if re.search(r"\bFed\b", text):       # bare capitalized "Fed" = Federal Reserve (not "fed up")
        tags.add("fed")
    if re.search(r"\brates?\b", low) and ("hold" in low or "steady" in low or "cut" in low or "hike" in low):
        tags.add("rates")
    return sorted(tags)


def _exchange_stablecoin_tags(text: str) -> list[str]:
    tags = [f"exchange:{ex}" for ex in _EXCHANGES if _keyword_match(text, ex)]
    tags += [f"stablecoin:{sym}" for sym, name in _STABLECOINS.items()
             if _keyword_match(text, name) or re.search(rf"[$#]?\b{re.escape(sym)}\b", text, re.I)]
    return tags


def _dynamic_crypto_tickers() -> set[str]:
    """Bases present in the latest local multi-exchange universe.

    A freshly-listed asset may be tradable before it earns a curated project-name
    alias.  We may recognise its explicit listing ticker only when it is already
    present in this locally collected exchange universe; unknown tickers remain
    visible as untracked entities and never become fake tradable symbols.
    """
    paths = (
        _ROOT / "data" / "processed" / "symbol_universe.json",
        _ROOT / "data" / "processed" / "universe" / "binance.json",
        _ROOT / "data" / "processed" / "universe" / "bybit.json",
        _ROOT / "data" / "processed" / "universe" / "mexc.json",
    )
    out: set[str] = set()
    for path in paths:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            symbols = payload.get("symbols") if isinstance(payload, dict) else payload
        except Exception:
            continue
        for value in symbols or []:
            symbol = value.get("symbol") if isinstance(value, dict) else value
            base = str(symbol or "").upper().split("/", 1)[0]
            if re.fullmatch(r"[A-Z0-9]{2,20}", base or ""):
                out.add(base)
    return out


def _listing_market(text: str) -> str:
    low = text.lower()
    if "delist" in low or "removal" in low:
        return "delisting"
    if "perpetual" in low or "futures" in low:
        return "perpetual"
    if "spot" in low:
        return "spot"
    return "listing"


def _listing_symbols(text: str, crypto_by_ticker: dict,
                     dynamic_tickers: set[str] | None = None) -> list[dict]:
    """Crypto exchange-listing parser. Extract candidate tickers near a listing keyword; a tracked
    ticker → tradable TICKER/USDT, otherwise an untracked_entity (recorded, never a fake trade symbol)."""
    low = text.lower()
    if not any(k in low for k in _LISTING_KEYWORDS):
        return []
    out: list[dict] = []
    seen: set[str] = set()
    # The local exchange universe proves that a token spelling has been seen by
    # our discovery layer, not that it is safe to make a trusted catalyst link.
    # Only the curated matcher may produce a tradable/trusted listing symbol.
    dynamic = set(dynamic_tickers) if dynamic_tickers is not None else _dynamic_crypto_tickers()
    curated = set(crypto_by_ticker)
    known = curated | dynamic
    tokens: list[str] = [m.group(1).upper() for m in _LISTING_PAIR.finditer(text)]
    tokens.extend(m.group(1).upper() for m in _LISTING_TOKEN.finditer(text))
    market = _listing_market(text)
    for tok in tokens:
        # The pair regex already produced VEXAI from VEXAIUSDT. Avoid recording
        # the full pair again as a second untracked token.
        if tok.endswith(("USDT", "USDC")):
            continue
        if tok in _TICKER_STOP or tok in seen or len(tok) < 2:
            continue
        if tok.isdigit() and tok not in known:
            continue
        seen.add(tok)
        if tok in curated:
            out.append({"symbol": f"{tok}/USDT", "ticker": tok, "tradable": True,
                        "market": market, "dynamic_universe": False})
        else:
            # Keep an explicit exchange-discovered spelling visible for the
            # coverage-gap report, but never turn it into a trusted trade link.
            out.append({"symbol": None, "ticker": tok, "tradable": False, "market": market,
                        "dynamic_universe": tok in dynamic})
    return out


def _issuer_name_key(value: str | None) -> str:
    return re.sub(r"[^a-z0-9]", "", str(value or "").lower())


def _safe_issuer_alias(value: str | None) -> bool:
    """Only use full, specific corporate names outside the curated alias table."""
    words = re.findall(r"[A-Za-z0-9]+", str(value or ""))
    return len(words) >= 2 and len("".join(words)) >= 8


@lru_cache(maxsize=1)
def _cik_to_ticker() -> dict[str, str]:
    try:
        from src.news.edgar import load_cik_map
        return {str(cik).zfill(10): str(ticker).upper() for ticker, cik in load_cik_map().items()}
    except Exception:
        return {}


def _issuer_alias_matches(text: str, stocks_matcher) -> list[tuple[str, str]]:
    """Exact canonical issuer-name matches not already required in aliases.

    Single-word canonicals such as ``Circle`` are deliberately excluded: broad
    prose must not become a stock catalyst merely because it shares a noun.
    """
    out: list[tuple[str, str]] = []
    for ticker, info in stocks_matcher.by_ticker.items():
        canonical = str((info or {}).get("canonical_name") or "").strip()
        if not _safe_issuer_alias(canonical):
            continue
        variants = {canonical, canonical.rstrip(".")}
        if any(_keyword_match(text, v) for v in variants if v):
            out.append((ticker, canonical))
    return out


def _headline_issuer_alias_matches(title: str, stocks_matcher) -> list[tuple[str, str]]:
    """Resolve narrowly approved one-word issuer names in a trusted stock headline.

    General body-text matching of names such as ``Oracle`` or ``Apple`` is too
    broad.  The curated ``headline_aliases`` list is deliberately opt-in and is
    used only for official/reputable stock headlines; this fixes visible
    mapping gaps without turning ordinary prose or social posts into catalysts.
    """
    out: list[tuple[str, str]] = []
    for ticker, info in stocks_matcher.by_ticker.items():
        context_terms = [str(value) for value in (info or {}).get("headline_context_terms") or []]
        for alias in (info or {}).get("headline_aliases") or []:
            if not _keyword_match(title, str(alias)):
                continue
            if context_terms and not any(_keyword_match(title, term) for term in context_terms):
                continue
            out.append((ticker, str(alias)))
    return out


def _structured_issuer_reference(raw: dict, source: str, stocks_matcher) -> tuple[str, str, bool] | None:
    """Resolve an issuer declared by a structured SEC/provider row.

    Raw tickers from arbitrary articles are useful evidence but not enough to
    drive trusted linkage.  A SEC/filing CIK provenance is trusted; otherwise
    the entity remains visible but untrusted until corroborated by an alias.
    """
    raw_ticker = str(raw.get("ticker") or raw.get("issuer_ticker") or "").upper().split("/", 1)[0]
    cik = str(raw.get("cik") or raw.get("issuer_cik") or "").strip()
    ticker = raw_ticker if raw_ticker in stocks_matcher.by_ticker else ""
    if not ticker and cik:
        ticker = _cik_to_ticker().get(cik.zfill(10), "")
    if not ticker:
        issuer_key = _issuer_name_key(raw.get("company") or raw.get("issuer") or raw.get("issuer_name"))
        for candidate, info in stocks_matcher.by_ticker.items():
            if issuer_key and issuer_key == _issuer_name_key((info or {}).get("canonical_name")):
                ticker = candidate
                break
    if ticker not in stocks_matcher.by_ticker:
        return None
    source_low = str(source or "").lower()
    raw_quality = str(raw.get("source_quality") or "").lower()
    official = bool(cik) and (
        "sec edgar" in source_low or str(raw.get("event_type") or "").lower() == "filing"
        or "regulator" in raw_quality or "primary" in raw_quality
    )
    label = f"CIK {cik.zfill(10)}" if cik else (raw_ticker or ticker)
    return ticker, label, official


def _structured_provider_symbols(row: dict, raw: dict, stocks_matcher) -> list[str]:
    """Resolve symbols proven by a narrowly allow-listed provider route.

    Finnhub company-news is queried for an explicit ticker. New rows persist
    that query context; historical rows can use the symbols saved by the same
    endpoint. No other feed receives this trust shortcut.
    """
    source = str(row.get("source") or "").strip().lower()
    if source not in _TRUSTED_PROVIDER_SYMBOL_SOURCES:
        return []
    values = raw.get("provider_symbols") or []
    if not values:
        try:
            values = json.loads(row.get("detected_symbols_json") or "[]") or []
        except (TypeError, ValueError):
            values = []
    out: list[str] = []
    for value in values:
        ticker = str(value or "").upper().split("/", 1)[0]
        if ticker in stocks_matcher.by_ticker and ticker not in out:
            out.append(ticker)
    return out


# ---- main resolver ----------------------------------------------------------------------------
def _matchers():
    from src.catalysts.entity_aliases import get_matcher, get_stocks_matcher
    return get_matcher(str(_ROOT)), get_stocks_matcher(str(_ROOT))


def resolve_row(row: dict, *, crypto_matcher=None, stocks_matcher=None) -> dict[str, Any]:
    """Resolve a single news_items row → enriched fields. Cross-asset aware: BOTH matchers run on the
    combined text; the row's own asset_class decides which matches are 'primary' vs 'cross_asset'. The
    resolver puts BOTH crypto (/USDT) and stock (bare) symbols into detected_symbols so the downstream
    catalyst refresh can link a stock signal to a stock story that arrived on a crypto feed."""
    if crypto_matcher is None or stocks_matcher is None:
        crypto_matcher, stocks_matcher = _matchers()
    asset = str(row.get("asset_class") or "crypto").lower()
    tf = extract_text_fields(row)
    text = tf["combined"]
    title = tf["title"]
    raw = _load_raw(row)

    entities: list[dict] = []
    symbols: set[str] = set()
    trusted_symbols: set[str] = set()      # only symbols with real provenance (never a bare ingest tag)
    sources: set[str] = set()
    reasons: list[str] = []
    confidence = 0.0
    cashtags = {m.group(1).upper() for m in _CASHTAG.finditer(text)}

    def _add(sym, ticker, cls, alias, src, conf, kind, *, trusted=True):
        nonlocal confidence
        if sym:
            symbols.add(sym)
            if trusted:
                trusted_symbols.add(sym)
        entities.append({"name": alias, "ticker": ticker, "asset_class": cls, "kind": kind,
                         "symbol": sym, "source": src, "trusted": bool(trusted)})
        sources.add(src)
        if alias and f"{alias}→{ticker}" not in reasons:
            reasons.append(f"{alias}→{ticker}")
        confidence = max(confidence, conf)

    def _conf_for(alias: str, ticker: str) -> float:
        # exact uppercase ticker (or cashtag) in the TITLE is the strongest signal.
        if alias == ticker and re.search(rf"[$#]?\b{re.escape(ticker)}\b", title):
            return 0.9
        if alias == ticker:
            return 0.8
        return 0.75    # a company / project NAME alias

    def _alias_trusted(alias: str, ticker: str) -> bool:
        # ambiguous ETF/acronym tickers need a cashtag or a descriptive (non-bare) alias — a bare
        # uppercase token in prose ("DIA Approval") is NOT a trusted catalyst symbol.
        if ticker in AMBIGUOUS_TICKERS:
            return (ticker in cashtags) or (alias != ticker)
        return True

    # cashtag pass — explicit $TICKER / #TICKER references are always trusted.
    for _tk in cashtags:
        if _tk in stocks_matcher.by_ticker:
            _add(_tk, _tk, "stocks", f"${_tk}", "cashtag", 0.9,
                 "primary" if asset == "stocks" else "cross_asset", trusted=True)
        elif _tk in crypto_matcher.by_ticker:
            _add(f"{_tk}/USDT", _tk, "crypto", f"${_tk}", "cashtag", 0.9,
                 "primary" if asset == "crypto" else "cross_asset", trusted=True)

    # crypto + stock alias matches on the combined text (cross-asset by construction).
    for sym, alias in crypto_matcher.detect(text, return_pairs=True):
        tk = sym.split("/")[0]
        primary = asset == "crypto"
        _add(sym, tk, "crypto", alias, "alias_crypto" if primary else "cross_asset",
             _conf_for(alias, tk) if primary else min(0.65, _conf_for(alias, tk)),
             "primary" if primary else "cross_asset", trusted=_alias_trusted(alias, tk))
    for tk, alias in ((s, a) for s, a in stocks_matcher.detect(text, return_pairs=True)):
        primary = asset == "stocks"
        _add(tk, tk, "stocks", alias, "alias_stocks" if primary else "cross_asset",
             _conf_for(alias, tk) if primary else min(0.65, _conf_for(alias, tk)),
             "primary" if primary else "cross_asset", trusted=_alias_trusted(alias, tk))

    # Structured issuer provenance is particularly useful for SEC rows: a filing may
    # be titled only with a form number, while its raw payload has the CIK/ticker.
    # Arbitrary provider tickers stay visible but cannot become trusted by themselves.
    issuer = _structured_issuer_reference(raw, str(row.get("source") or ""), stocks_matcher)
    if issuer:
        tk, label, official = issuer
        primary = asset == "stocks"
        _add(tk, tk, "stocks", label, "issuer_cik" if official else "issuer_alias",
             0.95 if official else 0.55, "primary" if primary else "cross_asset",
             trusted=official)
    for tk in _structured_provider_symbols(row, raw, stocks_matcher):
        primary = asset == "stocks"
        _add(tk, tk, "stocks", tk, "provider_symbol", 0.9,
             "primary" if primary else "cross_asset", trusted=True)
    for tk, canonical in _issuer_alias_matches(text, stocks_matcher):
        primary = asset == "stocks"
        _add(tk, tk, "stocks", canonical, "issuer_alias" if primary else "cross_asset",
             0.82 if primary else 0.65, "primary" if primary else "cross_asset", trusted=True)

    # A listed company buying crypto for its treasury is primarily a company
    # event. Bitcoin/Ether remains useful cross-asset context, but it is not a
    # direct token catalyst and therefore cannot enter trusted_symbols.
    corporate_crypto_treasury = bool(
        asset == "stocks"
        and re.search(r"\b(?:bitcoin|btc|ether|ethereum|eth)\b", text, re.IGNORECASE)
        and re.search(
            r"\b(?:treasury|reserve|balance\s+sheet|holdings?|purchase[sd]?|"
            r"buys?|bought|acquire[sd]?)\b", text,
            re.IGNORECASE,
        )
    )
    if corporate_crypto_treasury:
        for entity in entities:
            if entity.get("asset_class") == "crypto" and entity.get("symbol"):
                trusted_symbols.discard(str(entity["symbol"]))
                entity["trusted"] = False
                if entity.get("kind") == "cross_asset":
                    entity["kind"] = "contextual_reference"
        reasons.append("corporate_crypto_treasury_is_context_not_direct_token_catalyst")

    # crypto exchange-listing parser (tradable → symbol; untracked → recorded entity only).
    # A generic stock headline containing "NASDAQ listing" must never be
    # parsed as a crypto ticker-listing event merely because it has capital words.
    crypto_listing_context = bool(_LISTING_PAIR.search(text)) or any(
        _keyword_match(text, exchange) for exchange in _EXCHANGES
    )
    listing = _listing_symbols(text, crypto_matcher.by_ticker) if crypto_listing_context else []
    for hit in listing:
        if hit["tradable"]:
            alias = hit["ticker"] + (" (exchange universe)" if hit["dynamic_universe"] else "")
            _add(hit["symbol"], hit["ticker"], "crypto", alias, "listing_parser", 0.8, "primary",
                 trusted=True)
        else:
            entities.append({"name": hit["ticker"], "ticker": hit["ticker"], "asset_class": "crypto",
                             "kind": "untracked_entity", "symbol": None, "source": "listing_parser",
                             "trusted": False})
            sources.add("listing_parser")
            reasons.append(f"listing:{hit['ticker']}(untracked)")
    if asset == "stocks" and _source_quality_hint(row.get("source")) in {"official", "reputable"}:
        for tk, alias in _headline_issuer_alias_matches(title, stocks_matcher):
            _add(tk, tk, "stocks", alias, "headline_issuer_alias", 0.8, "primary", trusted=True)

    macro_tags = _macro_event_tags(text)
    event_tags = macro_tags + _exchange_stablecoin_tags(text)
    if corporate_crypto_treasury:
        event_tags.append("corporate_crypto_treasury")
    if listing:
        event_tags.append("listing")
        event_tags.extend(f"listing:{hit['market']}" for hit in listing)

    # narratives: reuse the aliases' curated tags for matched tickers + macro tags as narratives.
    narratives: set[str] = set(macro_tags)
    for e in entities:
        if e["symbol"] and e["asset_class"] == "crypto":
            for t in crypto_matcher.tags_for(e["ticker"]):
                narratives.add(t)

    # asset_impact_scope + tradability_status.
    primary_symbols = [e["symbol"] for e in entities if e["kind"] == "primary" and e["symbol"]]
    cross_only = [e for e in entities if e["kind"] == "cross_asset"]
    untracked = [e for e in entities if e["kind"] == "untracked_entity"]
    if primary_symbols:
        scope, tradability = "symbol", "tradable_symbol"
    elif cross_only:
        scope, tradability = "sector", "tracked_symbol"    # named a tradable name of the other class
    elif untracked:
        scope, tradability = ("crypto_market" if asset == "crypto" else "sector"), "untracked_entity"
    elif macro_tags:
        geop = {"geopolitics", "war", "sanctions", "middle_east", "china_taiwan"}
        scope = "geopolitics" if (set(macro_tags) & geop) else "macro"
        tradability = "macro_only"
        confidence = max(confidence, 0.4)
    elif event_tags:
        scope, tradability = "crypto_market", "untracked_entity"
    else:
        scope, tradability = "unknown", "ignored"

    # honest source label: only claim a trusted match when there is one; otherwise stay explicit.
    trusted_sources = {s for s in sources if s in TRUSTED_SOURCES}
    if trusted_symbols and trusted_sources:
        src_str = ",".join(sorted(trusted_sources))
    elif macro_tags:
        src_str = "macro_tagger"
    else:
        src_str = "no_match"                # never fake 'none' looking like a clean resolution
    return {
        "detected_symbols": sorted(symbols),
        "trusted_symbols": sorted(trusted_symbols),
        "detected_entities": entities,
        "detected_narratives": sorted(narratives),
        "event_tags": sorted(set(event_tags)),
        "entity_match_confidence": round(confidence if trusted_symbols else min(confidence, 0.4), 3),
        "entity_match_reason": "; ".join(reasons[:8]),
        "entity_match_source": src_str,
        "asset_impact_scope": scope,
        "tradability_status": tradability,
        "source_quality_hint": _source_quality_hint(row.get("source")),
    }


# ---- batch refresh (union-only writes) --------------------------------------------------------
def _parse_ts(v):
    from src.news.source_health import _parse_ts as p
    return p(v)


def refresh(*, db: str | None = None, hours: float = 72.0, limit: int = 10000,
            asset_class: str = "all", min_confidence: float = 0.0, write: bool = True,
            now_iso: str | None = None, urls: list[str] | None = None) -> dict[str, Any]:
    """Resolve recent news_items and union-only enrich them. Never touches score/tier/proposed_signals/
    final_r/live. Returns match-rate before/after + newly-tagged + scope/tradability breakdowns."""
    from src.config import load_config
    path = db or str(load_config().db_path)
    now = datetime.fromisoformat(now_iso) if now_iso else datetime.now(timezone.utc)
    cutoff = now.timestamp() - hours * 3600
    crypto_matcher, stocks_matcher = _matchers()
    # This is a scheduled enrichment pass, never an execution gate.  Give a
    # concurrent monitor a bounded chance to finish its transaction instead of
    # failing a whole news-repair batch on a transient SQLite writer lock.
    conn = sqlite3.connect(path, timeout=10.0)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA busy_timeout=10000")
        ensure_news_entity_columns(conn)
        conn.commit()
        news_cols = {r[1] for r in conn.execute("PRAGMA table_info(news_items)")}
        content_col = "content_text" if "content_text" in news_cols else "NULL AS content_text"
        ingested_col = "ingested_at" if "ingested_at" in news_cols else "NULL AS ingested_at"
        where_parts: list[str] = []
        params: list[Any] = []
        if asset_class in ("crypto", "stocks"):
            where_parts.append("asset_class=?")
            params.append(asset_class)
        if urls:
            clean_urls = list(dict.fromkeys(str(u) for u in urls if str(u or "").strip()))
            if not clean_urls:
                return {"rows": 0, "newly_symbol_tagged": 0, "rows_with_entities": 0,
                        "rows_macro_only": 0, "rows_untracked_entity": 0, "by_source": {},
                        "newly_by_source": {}, "before_tagged": 0, "before_symbol_match_rate": 0.0,
                        "after_symbol_match_rate": 0.0, "generated_at": now.isoformat()}
            where_parts.append("url IN (" + ",".join("?" for _ in clean_urls) + ")")
            params.extend(clean_urls)
        where = ("WHERE " + " AND ".join(where_parts)) if where_parts else ""
        rows = [dict(r) for r in conn.execute(
            f"SELECT id, title, source, url, published_at, detected_symbols_json, "
            f"detected_narratives_json, asset_class, raw_json, {content_col}, {ingested_col} "
            f"FROM news_items {where}", params)]
        # Exact post-ingest processing must also resolve SEC/date-only rows and
        # old articles re-seen through a repaired source. Scheduled scans retain
        # the normal rolling-window filter.
        if not urls:
            rows = [r for r in rows if (_parse_ts(r.get("published_at")) or 0) and
                    _parse_ts(r["published_at"]).timestamp() >= cutoff]
        rows.sort(key=lambda r: _parse_ts(r.get("published_at")) or datetime.min.replace(tzinfo=timezone.utc),
                  reverse=True)
        rows = rows[:limit]

        def _had(r):
            try:
                return bool(json.loads(r.get("detected_symbols_json") or "[]"))
            except (TypeError, ValueError):
                return False

        before_tagged = sum(1 for r in rows if _had(r))
        m = {"rows": len(rows), "newly_symbol_tagged": 0, "rows_with_entities": 0, "rows_macro_only": 0,
             "rows_untracked_entity": 0, "by_source": {}, "newly_by_source": {},
             "before_tagged": before_tagged}
        pending_updates: list[tuple[Any, ...]] = []
        update_sql = (
            "UPDATE news_items SET detected_symbols_json=?, detected_narratives_json=?, "
            "detected_entities_json=?, event_tags_json=?, entity_match_confidence=?, "
            "entity_match_reason=?, entity_match_source=?, asset_impact_scope=?, "
            "tradability_status=?, trusted_symbols_json=?, resolution_status=?, "
            "resolved_at=?, resolver_version=?, "
            "resolution_trigger=CASE WHEN resolution_trigger='incremental_post_ingest' "
            "THEN resolution_trigger ELSE ? END, "
            "resolution_latency_seconds=CASE WHEN resolution_trigger='incremental_post_ingest' "
            "THEN resolution_latency_seconds ELSE ? END WHERE id=?"
        )
        for r in rows:
            res = resolve_row(r, crypto_matcher=crypto_matcher, stocks_matcher=stocks_matcher)
            if res["entity_match_confidence"] < min_confidence and not res["event_tags"]:
                continue
            src = r.get("source") or "?"
            m["by_source"].setdefault(src, {"rows": 0, "tagged": 0})
            m["by_source"][src]["rows"] += 1
            if res["detected_entities"]:
                m["rows_with_entities"] += 1
            if res["tradability_status"] == "macro_only":
                m["rows_macro_only"] += 1
            if res["tradability_status"] == "untracked_entity":
                m["rows_untracked_entity"] += 1
            existing = []
            try:
                existing = json.loads(r.get("detected_symbols_json") or "[]") or []
            except (TypeError, ValueError):
                existing = []
            # Union-only, but preserve upstream ordering. Some downstream
            # catalyst records treat the first symbol as the primary entity;
            # enrichment may add related assets without silently replacing it.
            union = list(dict.fromkeys([*existing, *res["detected_symbols"]]))
            trusted = set(res["trusted_symbols"])
            newly = bool(set(res["detected_symbols"]) - set(existing))
            if union:
                m["by_source"][src]["tagged"] += 1
            if newly and not existing:
                m["newly_symbol_tagged"] += 1
                m["newly_by_source"][src] = m["newly_by_source"].get(src, 0) + 1
            # provenance status — never claim a clean resolution when only untrusted preexisting tags exist.
            if trusted:
                status = "resolver_added" if (trusted - set(existing)) else "resolver_confirmed"
            elif existing:
                status = "preexisting_unverified"
                m["rows_preexisting_unverified"] = m.get("rows_preexisting_unverified", 0) + 1
            elif res["tradability_status"] == "macro_only":
                status = "macro_only"
            else:
                status = "no_match"
            src_final = res["entity_match_source"] if trusted else (
                "preexisting_unverified" if existing else res["entity_match_source"])
            if write:
                nar_existing = []
                try:
                    nar_existing = json.loads(r.get("detected_narratives_json") or "[]") or []
                except (TypeError, ValueError):
                    nar_existing = []
                nar_union = sorted(set(nar_existing) | set(res["detected_narratives"]))
                trigger = "incremental_post_ingest" if urls else "scheduled_repair"
                latency_seconds = None
                if urls:
                    ingested = _parse_ts(r.get("ingested_at"))
                    if ingested is not None:
                        latency_seconds = max(0.0, round((now - ingested).total_seconds(), 3))
                pending_updates.append(
                    (json.dumps(union), json.dumps(nar_union), json.dumps(res["detected_entities"]),
                     json.dumps(res["event_tags"]), res["entity_match_confidence"],
                     res["entity_match_reason"], src_final, res["asset_impact_scope"],
                     res["tradability_status"], json.dumps(sorted(trusted)), status,
                     now.isoformat(), RESOLVER_VERSION, trigger, latency_seconds, r["id"])
                )
        if write:
            # Resolution is CPU work. Finish it before taking SQLite's single
            # writer slot, then persist in tiny deterministic batches.
            for start in range(0, len(pending_updates), 25):
                conn.executemany(update_sql, pending_updates[start:start + 25])
                conn.commit()
        after_tagged = before_tagged + m["newly_symbol_tagged"]
        m["before_symbol_match_rate"] = round(before_tagged / len(rows), 4) if rows else 0.0
        m["after_symbol_match_rate"] = round(after_tagged / len(rows), 4) if rows else 0.0
        m["generated_at"] = now.isoformat()
        return m
    finally:
        conn.close()


def audit(*, db: str | None = None, hours: float = 72.0) -> dict[str, Any]:
    """Read-only audit: current match-rate (overall + by asset_class + by source) + the lift the resolver
    WOULD add (dry-run refresh), + example unresolved high-value headlines. Never writes."""
    from src.config import load_config
    path = db or str(load_config().db_path)
    dry = refresh(db=path, hours=hours, asset_class="all", write=False)
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    now = datetime.now(timezone.utc)
    cutoff = now.timestamp() - hours * 3600
    by_class: dict[str, list[int]] = {"crypto": [0, 0], "stocks": [0, 0]}
    try:
        for r in conn.execute("SELECT asset_class, published_at, detected_symbols_json FROM news_items"):
            pts = _parse_ts(r["published_at"])
            if pts is None or pts.timestamp() < cutoff:
                continue
            ac = (r["asset_class"] or "crypto").lower()
            by_class.setdefault(ac, [0, 0])
            by_class[ac][0] += 1
            try:
                if json.loads(r["detected_symbols_json"] or "[]"):
                    by_class[ac][1] += 1
            except (TypeError, ValueError):
                pass
    except Exception:
        pass
    finally:
        conn.close()
    return {"hours": hours, "dry": dry,
            "by_class_match_rate": {k: (round(v[1] / v[0], 4) if v[0] else 0.0, v[0]) for k, v in by_class.items()},
            "generated_at": now.isoformat()}


def render_markdown(res: dict) -> str:
    d = res.get("dry") or res
    L = [f"# News Entity Resolution Audit ({res.get('generated_at','')})", "",
         "> READ-MODEL / enrichment. Never touches live / final_r / signal_outcomes / score / tier.", "",
         f"## Symbol match-rate (last {res.get('hours', 72)}h)",
         f"- rows: {d.get('rows', 0)}",
         f"- before → after (resolver would add): **{d.get('before_symbol_match_rate', 0)*100:.1f}% → "
         f"{d.get('after_symbol_match_rate', 0)*100:.1f}%**",
         f"- newly symbol-tagged: **{d.get('newly_symbol_tagged', 0)}** · rows_with_entities: "
         f"{d.get('rows_with_entities', 0)} · macro_only: {d.get('rows_macro_only', 0)} · "
         f"untracked_entity: {d.get('rows_untracked_entity', 0)}"]
    bc = res.get("by_class_match_rate") or {}
    L.append("")
    L.append("## Current match-rate by asset_class")
    L += [f"- {k}: {v[0]*100:.1f}% (n={v[1]})" for k, v in bc.items()] or ["- _none_"]
    nb = d.get("newly_by_source") or {}
    if nb:
        L.append("")
        L.append("## Top newly-tagged sources")
        L += [f"- {s}: +{n}" for s, n in sorted(nb.items(), key=lambda kv: -kv[1])[:12]]
    return "\n".join(L)


def write_report(res: dict) -> str:
    out = _ROOT / "reports" / "NEWS_ENTITY_RESOLUTION_AUDIT.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_markdown(res), encoding="utf-8")
    return str(out)


__all__ = ["resolve_row", "extract_text_fields", "ensure_news_entity_columns", "refresh", "audit",
           "render_markdown", "write_report", "RESOLVER_VERSION"]
