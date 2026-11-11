"""Materialized canonical news events and the fixed news influence contract.

Raw articles remain immutable in ``news_items``.  This table records the
point-in-time entity trust, event taxonomy, content confidence, cross-source
dedupe cluster and whether an item may positively support a paper signal.
Risk visibility is preserved even when positive linkage is denied.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

from src.config import load_config
from src.news.content_coverage import content_level
from src.news.entity_resolver import extract_text_fields
from src.news.source_health import _parse_ts, window_news_rows


POLICY_VERSION = "news_influence_v1"
_ROOT = Path(__file__).resolve().parents[2]
_DDL = """
CREATE TABLE IF NOT EXISTS news_canonical_events (
    news_item_id INTEGER PRIMARY KEY,
    event_id TEXT NOT NULL UNIQUE,
    cluster_key TEXT NOT NULL,
    title TEXT,
    source TEXT,
    url TEXT,
    published_at TEXT,
    available_at TEXT,
    event_latency_class TEXT,
    source_observation_delay_seconds REAL,
    asset_class TEXT,
    trusted_symbols_json TEXT NOT NULL DEFAULT '[]',
    mentioned_symbols_json TEXT NOT NULL DEFAULT '[]',
    event_type TEXT NOT NULL,
    event_subtype TEXT,
    direction_hint TEXT NOT NULL,
    source_quality TEXT NOT NULL,
    content_level TEXT NOT NULL,
    confidence REAL NOT NULL,
    linkage_allowed INTEGER NOT NULL DEFAULT 0,
    linkage_reason TEXT NOT NULL,
    risk_action TEXT NOT NULL DEFAULT 'none',
    effective_at TEXT,
    expires_at TEXT,
    is_cluster_primary INTEGER NOT NULL DEFAULT 1,
    corroboration_count INTEGER NOT NULL DEFAULT 1,
    independent_non_social_count INTEGER NOT NULL DEFAULT 0,
    resolver_version TEXT,
    policy_version TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(news_item_id) REFERENCES news_items(id)
)
"""

_STOCK_TAXO = [
    (("8-k", "10-q", "10-k", "424b", "s-1", "s-3", "form 4"), "sec_filing"),
    (("earnings", "eps", "quarterly results", "reports q"), "earnings"),
    (("guidance", "outlook", "forecast"), "guidance"),
    (("upgrade", "downgrade", "price target", "initiates coverage"), "analyst_action"),
    (("lawsuit", "sec charges", "doj", "investigation", "fraud", "subpoena"), "legal_risk"),
    (("offering", "dilution", "shelf registration", "convertible notes"), "offering_dilution"),
    (("acquire", "acquisition", "merger", "buyout", "takeover"), "mna"),
    (("fda", "phase 3", "clinical", "trial results"), "fda_clinical"),
    (("ceo", "cfo", "resign", "steps down"), "management_change"),
    (("launches", "unveils", "new product"), "product_launch"),
    (("partnership", "partners with", "collaborat"), "partnership"),
]
_CRYPTO_TAXO = [
    (("perpetual", "futures listing", "usdt-margined"), "futures_listing"),
    (("delist", "removal of", "will be removed"), "delisting"),
    (("will list", "to list", "lists ", "listing", "spot trading"), "listing"),
    (("unlock", "vesting", "cliff"), "token_unlock"),
    (("hack", "exploit", "breach", "drained", "stolen", "theft"), "exploit_hack"),
    (("whale", "transferred", "deposited to"), "whale_transfer"),
    (("tvl", "total value locked"), "tvl_change"),
    (("governance", "proposal", "vote"), "governance"),
    (("airdrop",), "airdrop"),
    (("launchpool", "launchpad"), "launchpad"),
    (("maintenance", "suspend deposits", "halt withdrawals"), "maintenance"),
    (("partnership", "partners with", "collaborat", "integration with"), "partnership"),
    (("launches", "unveils", "new product", "goes live"), "product_launch"),
]
_MACRO_TAXO = [
    (("fomc", "federal reserve", "powell", "rate cut", "rate hike"), "fed"),
    (("cpi", "inflation"), "cpi"), (("pce",), "pce"),
    (("jobs report", "nonfarm", "payroll", "unemployment"), "jobs"),
    (("war", "attack", "sanctions", "geopolit", "airstrike", "missile", "blockade",
      "strait of hormuz", "military strike", "retaliation"), "geopolitical_risk"),
]
_BULL = ("beats", "beat estimates", "approval", "upgrade", "record high", "buyback", "soars",
         "surges", "raises guidance", "wins contract")
_BEAR = ("misses", "missed estimates", "downgrade", "probe", "lawsuit", "recall",
         "cuts guidance", "plunge", "halts", "delist", "exploit", "hack", "dilution")
_BULL_TYPES = {"listing", "futures_listing", "buyback_burn", "partnership", "mna", "product_launch"}
_BEAR_TYPES = {"delisting", "exploit_hack", "legal_risk", "offering_dilution", "maintenance"}
_RISK_REVIEW = {"exploit_hack", "legal_risk", "delisting", "fda_clinical"}
_RISK_WARN = {"offering_dilution", "token_unlock", "maintenance", "geopolitical_risk"}
_STRUCTURED_TITLE_OK = {"listing", "futures_listing", "delisting", "sec_filing", "exploit_hack"}
_POSITIVE_TYPES = {
    "listing", "futures_listing", "earnings", "guidance", "analyst_action", "mna",
    "fda_clinical", "product_launch", "partnership", "tvl_change", "launchpad",
    "legal_risk", "delisting", "exploit_hack", "offering_dilution", "management_change",
}
_TTL_HOURS = {
    "sec_filing": 72, "earnings": 48, "guidance": 48, "analyst_action": 24,
    "listing": 24, "futures_listing": 24, "delisting": 24, "exploit_hack": 24,
    "legal_risk": 48, "offering_dilution": 48, "token_unlock": 48,
    "fed": 12, "cpi": 12, "pce": 12, "jobs": 12, "geopolitical_risk": 12,
}
_QUALITY_RANK = {"regulator": 5, "exchange": 5, "primary": 5, "company_pr": 4,
                 "reputable": 3, "secondary": 2, "social": 1}
_CONTENT_RANK = {"full_body": 4, "summary_only": 3, "body_equals_title": 2, "title_only": 1}
_ANALYST_FIRMS = {"WFC", "JPM", "GS", "MS", "BAC", "C", "UBS", "BCS", "DB", "HSBC"}


def ensure_table(conn: sqlite3.Connection) -> None:
    # Canonical refresh is also invoked directly by repair commands/tests, not
    # only via SQLiteStore.save_news_items(). Keep the input-side migration
    # available on that path as well.
    from src.storage.sqlite import SQLiteStore
    SQLiteStore._migrate_news_items(conn)
    conn.execute(_DDL)
    columns = {r[1] for r in conn.execute("PRAGMA table_info(news_canonical_events)")}
    if "mentioned_symbols_json" not in columns:
        conn.execute("ALTER TABLE news_canonical_events ADD COLUMN mentioned_symbols_json TEXT "
                     "NOT NULL DEFAULT '[]'")
    for column, ddl in (
        ("available_at", "TEXT"),
        ("event_latency_class", "TEXT"),
        ("source_observation_delay_seconds", "REAL"),
    ):
        if column not in columns:
            conn.execute(f"ALTER TABLE news_canonical_events ADD COLUMN {column} {ddl}")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_news_canonical_cluster ON news_canonical_events(cluster_key)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_news_canonical_symbol_time "
                 "ON news_canonical_events(published_at, linkage_allowed)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_news_canonical_effective_linkage "
                 "ON news_canonical_events(effective_at, linkage_allowed)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_news_canonical_available "
                 "ON news_canonical_events(available_at)")


def source_quality(source: str | None) -> str:
    value = str(source or "").lower()
    if value.startswith("t.me/") or any(x in value for x in ("telegram", "twitter", "reddit")):
        return "social"
    if any(x in value for x in ("sec edgar", "sec.gov", "federal reserve")):
        return "regulator"
    if any(x in value for x in ("binance announcement", "coinbase announcement", "bybit announcement",
                                "okx announcement", "mexc announcement", "kraken announcement")):
        return "exchange"
    if any(x in value for x in ("globenewswire", "pr newswire", "business wire", "company ir")):
        return "company_pr"
    if any(x in value for x in ("reuters", "bloomberg", "cnbc", "coindesk", "cointelegraph",
                                "the block", "decrypt", "yahoo finance", "marketwatch", "ft.com")):
        return "reputable"
    return "secondary"


def _keyword_present(text: str, keyword: str) -> bool:
    """Boundary-safe taxonomy matching.

    The previous raw substring check treated ``war`` inside ``software`` as a
    geopolitical event and ``fraud`` in cybersecurity marketing as a legal
    action. Only the few explicitly stemmed taxonomy entries may prefix-match.
    """
    value = str(keyword or "").strip().lower()
    if not value:
        return False
    if value in {"collaborat"}:
        return bool(re.search(r"(?<![a-z0-9])collaborat[a-z]*(?![a-z0-9])", text))
    escaped = re.escape(value).replace(r"\ ", r"\s+")
    # Common inflections for standalone action words.
    suffix = r"(?:s|ed|ing)?" if value in {"list", "delist", "hack", "exploit", "attack",
                                                "launch", "acquire", "upgrade", "downgrade"} else ""
    return bool(re.search(rf"(?<![a-z0-9]){escaped}{suffix}(?![a-z0-9])", text))


def classify_event(text: str, asset_class: str) -> tuple[str, str | None]:
    low = str(text or "").lower()
    taxonomy = _STOCK_TAXO if str(asset_class).lower().startswith("stock") else _CRYPTO_TAXO
    for keys, event_type in taxonomy:
        if any(_keyword_present(low, key) for key in keys):
            if event_type == "product_launch" and not any(
                _keyword_present(low, term) for term in (
                    "product", "platform", "network", "mainnet", "update", "service", "chip",
                    "app", "index", "protocol", "fund", "etf", "token", "feature", "accelerator")):
                continue
            if event_type in {"listing", "delisting", "futures_listing"} \
                    and not str(asset_class).lower().startswith("stock") \
                    and any(term in low for term in ("nasdaq", "nyse", "reverse split", "stock exchange")):
                continue
            return event_type, None
    for keys, event_type in _MACRO_TAXO:
        if any(_keyword_present(low, key) for key in keys):
            return event_type, None
    return ("macro_headline" if str(asset_class).lower().startswith("stock") else "other_news"), None


def direction_hint(text: str, event_type: str) -> str:
    low = str(text or "").lower()
    bull = any(_keyword_present(low, k) for k in _BULL) or event_type in _BULL_TYPES
    bear = any(_keyword_present(low, k) for k in _BEAR) or event_type in _BEAR_TYPES
    return "mixed" if bull and bear else "bullish" if bull else "bearish" if bear else "neutral"


def _base_symbols(raw: Any) -> list[str]:
    try:
        values = json.loads(raw) if isinstance(raw, str) else (raw or [])
    except (TypeError, ValueError):
        values = []
    return sorted({str(v).split("/")[0].strip().upper() for v in values if str(v).strip()})


def _load_entities(raw: Any) -> list[dict[str, Any]]:
    try:
        values = json.loads(raw) if isinstance(raw, str) else (raw or [])
        return [v for v in values if isinstance(v, dict)]
    except (TypeError, ValueError):
        return []


@lru_cache(maxsize=512)
def _configured_aliases(asset_class: str, symbol: str) -> tuple[str, ...]:
    try:
        from src.news.entity_resolver import _matchers
        crypto, stocks = _matchers()
        matcher = stocks if str(asset_class).startswith("stock") else crypto
        info = matcher.by_ticker.get(str(symbol).upper()) or {}
        values = [info.get("canonical_name"), *(info.get("aliases") or [])]
        return tuple(str(v).strip() for v in values if str(v or "").strip())
    except Exception:
        return ()


def _alias_position(title: str, alias: str) -> int | None:
    alias = str(alias or "").strip()
    if not alias:
        return None
    match = re.search(rf"(?<![A-Za-z0-9]){re.escape(alias)}(?![A-Za-z0-9])", title)
    return match.start() if match else None


def _event_anchor(title: str, event_type: str) -> int | None:
    patterns = {
        "product_launch": ("launch", "unveil", "release", "goes live"),
        "partnership": ("partner", "collaborat", "integration"),
        "mna": ("acquire", "acquisition", "merger", "buyout", "takeover"),
        "earnings": ("earnings", "reports", "results", "eps"),
        "guidance": ("guidance", "outlook", "forecast"),
        "management_change": ("resign", "steps down", "appoint"),
        "offering_dilution": ("offering", "dilution", "convertible", "shelf"),
        "fda_clinical": ("fda", "phase 3", "clinical", "trial"),
        "exploit_hack": ("exploit", "hack", "breach", "drained"),
        "token_unlock": ("unlock", "vesting", "cliff"),
        "maintenance": ("maintenance", "suspend", "halt"),
    }.get(event_type, ())
    positions = [title.lower().find(p) for p in patterns if title.lower().find(p) >= 0]
    return min(positions) if positions else None


def _legal_target(title: str, alias: str) -> bool:
    a = re.escape(alias)
    patterns = (
        rf"\b(?:charges?|sues?|charged|sued)\s+(?:[^,;:]{{0,30}}\s)?{a}\b",
        rf"\b(?:against|into)\s+(?:[^,;:]{{0,30}}\s)?{a}\b",
        rf"\b{a}\b.{{0,35}}\b(?:faces|charged|sued|under investigation|settles|subpoenaed)\b",
    )
    return any(re.search(pattern, title, re.I) for pattern in patterns)


def _subject_symbols(row: dict[str, Any], title: str, event_type: str,
                     mentioned: list[str]) -> list[str]:
    """Keep entities that are the event subject, not merely context.

    The broad resolver intentionally finds every mention. Positive/risk trading
    influence is narrower: a former Google employee does not make a third-party
    product launch a GOOGL catalyst, and a lowercase DeFi ``oracle`` is not ORCL.
    """
    if not mentioned:
        return []
    raw = row.get("raw_json")
    try:
        raw_obj = json.loads(raw) if isinstance(raw, str) else (raw or {})
    except (TypeError, ValueError):
        raw_obj = {}
    structured = str(raw_obj.get("ticker") or raw_obj.get("issuer_ticker") or "").upper()
    subjects: set[str] = {structured} & set(mentioned) if structured else set()
    anchor = _event_anchor(title, event_type)
    entities = _load_entities(row.get("detected_entities_json"))
    aliases_by_symbol: dict[str, set[str]] = {s: set() for s in mentioned}
    classes_by_symbol: dict[str, set[str]] = {s: set() for s in mentioned}
    for entity in entities:
        base = str(entity.get("symbol") or entity.get("ticker") or "").split("/")[0].upper()
        if base in aliases_by_symbol:
            aliases_by_symbol[base].add(str(entity.get("name") or entity.get("ticker") or base))
            classes_by_symbol[base].add(str(entity.get("asset_class") or ""))
    for symbol in mentioned:
        aliases_by_symbol.setdefault(symbol, set()).update(
            _configured_aliases(str(row.get("asset_class") or ""), symbol))
    for symbol in mentioned:
        # Explicit market notation is always a subject-level reference.
        if re.search(rf"(?:[$#]\s*{re.escape(symbol)}\b|\b{re.escape(symbol)}(?:USDT|USDC)\b|"
                     rf"\b(?:NASDAQ|NYSE)\s*:\s*{re.escape(symbol)}\b)", title):
            subjects.add(symbol)
            continue
        if str(row.get("asset_class") or "").startswith("stock") \
                and "crypto" in classes_by_symbol.get(symbol, set()) \
                and not any(term in title.lower() for term in (
                    " crypto", " token", " blockchain", " bitcoin", " ethereum", " protocol",
                    " mainnet", " defi", " stablecoin")):
            continue
        for alias in aliases_by_symbol.get(symbol) or {symbol}:
            pos = _alias_position(title, alias)
            if pos is None:
                continue
            # Two-word aliases with no overlap to the canonical ticker are
            # commonly executives/founders. They provide context, not issuer
            # subject proof, for stock events.
            words = re.findall(r"[A-Za-z]+", alias)
            if str(row.get("asset_class") or "").startswith("stock") and len(words) == 2 \
                    and symbol not in alias.upper() and not any(
                        token in alias.lower() for token in (
                            "corp", "company", "bank", "group", "holdings", " inc", "ltd", "plc")):
                continue
            if event_type == "legal_risk":
                if _legal_target(title, alias):
                    subjects.add(symbol)
                continue
            if event_type == "analyst_action":
                # Rating firms are context in "Wells Fargo upgrades X" and
                # "X downgraded by Wells Fargo", not the rated security.
                if symbol in _ANALYST_FIRMS:
                    continue
                action_positions = [title.lower().find(k) for k in ("upgrade", "downgrade", "price target")
                                    if title.lower().find(k) >= 0]
                if action_positions:
                    action = min(action_positions)
                    prefix = title[max(0, pos - 4):pos].lower()
                    if not (pos > action and prefix.rstrip().endswith("by")):
                        subjects.add(symbol)
                continue
            if event_type in {"listing", "futures_listing", "delisting"}:
                # Listing parser entities are explicit tokens/pairs; aliases in
                # an exchange name or surrounding prose are not enough.
                if re.search(rf"\b{re.escape(symbol)}(?:USDT|USDC)?\b", title):
                    subjects.add(symbol)
                continue
            if anchor is None or pos <= anchor:
                subjects.add(symbol)
    return sorted(subjects)


def _cluster_key(asset: str, symbols: list[str], event_type: str, published: datetime | None,
                 title: str) -> str:
    if published:
        bucket = f"{published.date().isoformat()}:{published.hour // 6}"
    else:
        bucket = "unknown"
    entity = ",".join(symbols)
    if not entity:
        norm = re.sub(r"[^a-z0-9 ]", " ", str(title or "").lower())
        tokens = [t for t in norm.split() if len(t) > 3][:10]
        entity = hashlib.sha1(" ".join(tokens).encode()).hexdigest()[:12]
    raw = f"{asset}|{entity}|{event_type}|{bucket}"
    return hashlib.sha1(raw.encode()).hexdigest()[:20]


def _confidence(quality: str, level: str, event_type: str, symbols: list[str]) -> float:
    source = {"regulator": .98, "exchange": .98, "primary": .95, "company_pr": .88,
              "reputable": .82, "secondary": .68, "social": .42}.get(quality, .6)
    content = {"full_body": 1.0, "summary_only": .9, "body_equals_title": .72,
               "title_only": .55}.get(level, .5)
    structured = 1.05 if event_type in _STRUCTURED_TITLE_OK else 1.0
    entity = 1.0 if symbols else .65
    return round(min(1.0, source * content * structured * entity), 3)


def _source_family(source: str | None) -> str:
    s = re.sub(r"[^a-z0-9]", "", str(source or "").lower())
    return s[:32] or "unknown"


def _policy(event: dict[str, Any], *, corroboration: int, non_social: int) -> tuple[bool, str, str]:
    et = event["event_type"]
    quality = event["source_quality"]
    level = event["content_level"]
    direction = event["direction_hint"]
    confidence = float(event["confidence"])
    if et in _RISK_REVIEW:
        risk_action = "operator_review"
    elif et in _RISK_WARN:
        risk_action = "risk_warning"
    else:
        risk_action = "none"
    if not event["symbols"]:
        return False, "no_trusted_symbol", risk_action
    if et not in _POSITIVE_TYPES:
        return False, "event_type_not_directional", risk_action
    if direction in {"neutral", "mixed"}:
        return False, f"direction_{direction}", risk_action
    if quality == "social" and (corroboration < 2 or non_social < 1):
        return False, "social_requires_independent_corroboration", risk_action
    if level == "title_only" and not (quality in {"regulator", "exchange"} and et in _STRUCTURED_TITLE_OK):
        return False, "title_only_confidence_cap", risk_action
    if confidence < .55:
        return False, "confidence_below_0.55", risk_action
    return True, "trusted_directional_event", risk_action


def _select_rows(conn: sqlite3.Connection, *, hours: int, now: datetime,
                 urls: list[str] | None) -> list[dict[str, Any]]:
    columns = ("id, title, source, url, published_at, available_at, event_latency_class, "
               "source_observation_delay_seconds, asset_class, raw_json, content_text, importance, "
               "trusted_symbols_json, detected_entities_json, resolver_version")
    if urls:
        placeholders = ",".join("?" for _ in urls)
        return [dict(r) for r in conn.execute(
            f"SELECT {columns} FROM news_items WHERE url IN ({placeholders})", tuple(urls)).fetchall()]
    return window_news_rows(conn, hours=hours, now=now, limit=20000, columns=columns) or []


def refresh(db: str | None = None, *, hours: int = 168, now: datetime | None = None,
            urls: list[str] | None = None) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    stamp = now.isoformat()
    path = db or str(load_config().db_path)
    conn = sqlite3.connect(path, timeout=30)
    conn.row_factory = sqlite3.Row
    affected: set[str] = set()
    try:
        ensure_table(conn)
        conn.commit()
        rows = _select_rows(conn, hours=hours, now=now, urls=urls)
        insert_sql = """
            INSERT INTO news_canonical_events(
                news_item_id,event_id,cluster_key,title,source,url,published_at,available_at,
                event_latency_class,source_observation_delay_seconds,asset_class,
                trusted_symbols_json,mentioned_symbols_json,event_type,event_subtype,direction_hint,source_quality,
                content_level,confidence,linkage_allowed,linkage_reason,risk_action,effective_at,
                expires_at,is_cluster_primary,corroboration_count,independent_non_social_count,
                resolver_version,policy_version,created_at,updated_at
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,1,1,?,?,?,?,?)
            ON CONFLICT(news_item_id) DO UPDATE SET
                cluster_key=excluded.cluster_key,title=excluded.title,source=excluded.source,
                url=excluded.url,published_at=excluded.published_at,available_at=excluded.available_at,
                event_latency_class=excluded.event_latency_class,
                source_observation_delay_seconds=excluded.source_observation_delay_seconds,
                asset_class=excluded.asset_class,
                trusted_symbols_json=excluded.trusted_symbols_json,
                mentioned_symbols_json=excluded.mentioned_symbols_json,event_type=excluded.event_type,
                event_subtype=excluded.event_subtype,direction_hint=excluded.direction_hint,
                source_quality=excluded.source_quality,content_level=excluded.content_level,
                confidence=excluded.confidence,linkage_allowed=excluded.linkage_allowed,
                linkage_reason=excluded.linkage_reason,risk_action=excluded.risk_action,
                effective_at=excluded.effective_at,expires_at=excluded.expires_at,
                resolver_version=excluded.resolver_version,policy_version=excluded.policy_version,
                updated_at=excluded.updated_at
        """
        insert_values: list[tuple[Any, ...]] = []
        for row in rows:
            fields = extract_text_fields(row)
            # Taxonomy and direction use the headline only. Full body remains
            # available to Opus/entity resolution, but generic prose words
            # (e.g. cybersecurity "fraud") must not invent an event type.
            text = fields["title"]
            asset = str(row.get("asset_class") or "crypto").lower()
            mentioned = _base_symbols(row.get("trusted_symbols_json"))
            event_type, subtype = classify_event(text, asset)
            direction = direction_hint(text, event_type)
            symbols = _subject_symbols(row, fields["title"], event_type, mentioned)
            quality = source_quality(row.get("source"))
            level = content_level(row)
            confidence = _confidence(quality, level, event_type, symbols)
            published = _parse_ts(row.get("published_at"))
            cluster = _cluster_key(asset, symbols or mentioned, event_type, published, fields["title"])
            affected.add(cluster)
            ttl = _TTL_HOURS.get(event_type, 18)
            expires = (published + timedelta(hours=ttl)).isoformat() if published else None
            # New rows only become actionable after they arrived here. Legacy
            # rows have no trustworthy observation time, so preserve their
            # historic effective_at rather than pretending they were fast.
            available_at = row.get("available_at") or row.get("published_at")
            provisional = {
                "event_type": event_type, "source_quality": quality, "content_level": level,
                "direction_hint": direction, "confidence": confidence, "symbols": symbols,
            }
            allowed, reason, risk = _policy(provisional, corroboration=1,
                                             non_social=int(quality != "social"))
            insert_values.append(
                (row["id"], f"nev_{row['id']}", cluster, fields["title"], row.get("source"),
                 row.get("url"), row.get("published_at"), available_at,
                 row.get("event_latency_class"), row.get("source_observation_delay_seconds"), asset,
                 json.dumps(symbols), json.dumps(mentioned), event_type,
                 subtype, direction, quality, level, confidence, int(allowed), reason, risk,
                 available_at, expires, int(quality != "social"),
                 row.get("resolver_version"), POLICY_VERSION, stamp, stamp)
            )
        for start in range(0, len(insert_values), 25):
            conn.executemany(insert_sql, insert_values[start:start + 25])
            conn.commit()

        # Recompute cluster trust and choose one canonical primary.  The primary
        # is the richest, highest-quality representation of the same event.
        cluster_updates: list[tuple[Any, ...]] = []
        for cluster in affected:
            members = [dict(r) for r in conn.execute(
                "SELECT * FROM news_canonical_events WHERE cluster_key=?", (cluster,)).fetchall()]
            families = {_source_family(m.get("source")) for m in members}
            non_social = {_source_family(m.get("source")) for m in members
                          if m.get("source_quality") != "social"}
            primary = max(members, key=lambda m: (
                _QUALITY_RANK.get(m.get("source_quality"), 0),
                _CONTENT_RANK.get(m.get("content_level"), 0),
                float(m.get("confidence") or 0), float(m.get("importance") or 0),
                -(int(m.get("news_item_id") or 0)),
            )) if members else None
            for member in members:
                policy_input = {**member, "symbols": _base_symbols(member.get("trusted_symbols_json"))}
                allowed, reason, risk = _policy(policy_input, corroboration=len(families),
                                                 non_social=len(non_social))
                cluster_updates.append(
                    (int(primary is not None and member["news_item_id"] == primary["news_item_id"]),
                     len(families), len(non_social), int(allowed), reason, risk, stamp,
                     member["news_item_id"])
                )
        cluster_sql = (
            "UPDATE news_canonical_events SET is_cluster_primary=?, corroboration_count=?, "
            "independent_non_social_count=?, linkage_allowed=?, linkage_reason=?, risk_action=?, "
            "updated_at=? WHERE news_item_id=?"
        )
        for start in range(0, len(cluster_updates), 25):
            conn.executemany(cluster_sql, cluster_updates[start:start + 25])
            conn.commit()
        counts = dict(conn.execute(
            "SELECT linkage_reason, COUNT(*) FROM news_canonical_events GROUP BY linkage_reason").fetchall())
        allowed_count = conn.execute(
            "SELECT COUNT(*) FROM news_canonical_events WHERE linkage_allowed=1").fetchone()[0]
    finally:
        conn.close()
    return {"generated_at": stamp, "rows_processed": len(rows), "clusters_updated": len(affected),
            "linkage_allowed_total": allowed_count, "by_linkage_reason": counts,
            "policy_version": POLICY_VERSION}


__all__ = ["POLICY_VERSION", "ensure_table", "source_quality", "classify_event",
           "direction_hint", "refresh"]
