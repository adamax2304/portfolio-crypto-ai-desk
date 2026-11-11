from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
import re
import time
from typing import Any
from xml.etree import ElementTree

import requests

from src.config import ProjectConfig
from src.logger import get_logger
from src.models import NewsItem
from src.news.content import clean_text, content_hash
from src.news.source_telemetry import now_iso, record_source_run
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore
from src.utils.symbols import symbol_to_ticker
from src.utils.time import utc_now


AMBIGUOUS_TICKERS = {"LINK", "NEAR", "OP", "SEI", "APT"}


@dataclass
class NewsCollectionSummary:
    fetched_sources: list[str] = field(default_factory=list)
    failed_sources: dict[str, str] = field(default_factory=dict)
    items: list[NewsItem] = field(default_factory=list)


class RSSNewsCollector:
    def __init__(self, config: ProjectConfig, store: FileStore, db: SQLiteStore):
        self.config = config
        self.store = store
        self.db = db
        self.logger = get_logger(self.__class__.__name__)
        self.tickers = sorted({symbol_to_ticker(symbol) for symbol in config.symbols}, key=len, reverse=True)
        self.narratives = config.watchlist.get("narratives", {})
        # Stocks universe tickers — used when a source is tagged
        # asset_class='stocks' so we can detect $NVDA / $AAPL / etc. Loaded
        # lazily and tolerantly so a missing stocks config never breaks crypto
        # news collection.
        self._stocks_tickers = self._load_stocks_tickers()

    def _load_stocks_tickers(self) -> list[str]:
        try:
            from src.stocks import load_stocks_config

            scfg = load_stocks_config(self.config.root)
            return sorted({s.upper() for s in scfg.default_symbols}, key=len, reverse=True)
        except Exception as exc:  # noqa: BLE001 — stocks module is optional at runtime
            self.logger.debug("stocks tickers unavailable for news matching: %s", exc)
            return []

    def fetch(
        self,
        limit_per_source: int = 25,
        *,
        source_names: set[str] | None = None,
        request_timeout: float = 20.0,
        write_snapshot: bool = True,
    ) -> NewsCollectionSummary:
        """Fetch all feeds or an explicit low-latency subset.

        The fast-news monitor uses ``source_names`` so a handful of operational
        RSS feeds can run every few minutes without re-polling the whole
        editorial feed list or overwriting the full-cycle raw snapshot.
        """
        summary = NewsCollectionSummary()
        selected = {str(name) for name in source_names} if source_names is not None else None
        seen_urls: set[str] = set()
        seen_content: set[tuple[str, str]] = set()
        # Track which items belong to which asset_class so we can save them
        # with the correct tag. Default is 'crypto' (backward-compatible).
        items_by_asset_class: dict[str, list[NewsItem]] = {"crypto": [], "stocks": []}

        for source in self.config.sources.get("rss_feeds", []):
            name = str(source.get("name", "unknown"))
            if selected is not None and name not in selected:
                continue
            url = str(source.get("url", ""))
            source_type = str(source.get("type", "rss"))
            source_asset_class = str(source.get("asset_class") or "crypto").lower()
            if source_asset_class not in ("crypto", "stocks"):
                source_asset_class = "crypto"
            if source.get("enabled") is False:
                self.logger.info("Skipping disabled RSS source %s", name)
                record_source_run(source_name=name, source_type=source_type, asset_class=source_asset_class,
                                  status="disabled", item_count=0, metadata={"reason": source.get("disabled_reason")})
                continue
            if not url:
                record_source_run(source_name=name, source_type=source_type, asset_class=source_asset_class,
                                  status="error", error_code="missing_url", error_message="source URL is empty")
                continue
            started_at = now_iso()
            try:
                response = None
                last_exc: Exception | None = None
                attempt_count = 0
                attempts = max(1, int(source.get("retry_attempts", 2)))
                timeout_seconds = float(source.get("request_timeout_seconds", request_timeout))
                backoff_seconds = max(0.0, float(source.get("retry_backoff_seconds", 0.0)))
                for attempt in range(attempts):
                    attempt_count = attempt + 1
                    try:
                        response = requests.get(
                            url, timeout=timeout_seconds,
                            headers={"User-Agent": "crypto-ai-desk/0.1 (+news-health)"},
                        )
                        response.raise_for_status()
                        break
                    except requests.exceptions.Timeout as exc:
                        last_exc = exc
                        if attempt + 1 < attempts:
                            if backoff_seconds:
                                time.sleep(backoff_seconds * (2 ** attempt))
                            continue
                    except requests.exceptions.RequestException as exc:
                        last_exc = exc
                        if attempt + 1 < attempts:
                            if backoff_seconds:
                                time.sleep(backoff_seconds * (2 ** attempt))
                            continue
                if response is None:
                    raise last_exc or RuntimeError("RSS request returned no response")
                if source_type == "binance_announcements":
                    parsed = self._parse_binance_announcements(
                        response.json(),
                        source_name=name,
                        primary=bool(source.get("primary_source")),
                        limit=limit_per_source,
                        asset_class=source_asset_class,
                    )
                elif response.apparent_encoding:
                    response.encoding = response.apparent_encoding
                    parsed = self._parse_feed(
                        response.text,
                        source_name=name,
                        primary=bool(source.get("primary_source")),
                        limit=limit_per_source,
                        asset_class=source_asset_class,
                    )
                else:
                    parsed = self._parse_feed(
                        response.text,
                        source_name=name,
                        primary=bool(source.get("primary_source")),
                        limit=limit_per_source,
                        asset_class=source_asset_class,
                    )
                for item in parsed:
                    if item.url in seen_urls:
                        continue
                    content_key = (name, item.content_hash or "")
                    if content_key[1] and content_key in seen_content:
                        # Same publisher repeated the exact same payload under
                        # multiple feed links; keep one row, while identical
                        # content from a different publisher remains useful
                        # corroboration.
                        continue
                    seen_urls.add(item.url)
                    if content_key[1]:
                        seen_content.add(content_key)
                    summary.items.append(item)
                    items_by_asset_class.setdefault(source_asset_class, []).append(item)
                summary.fetched_sources.append(name)
                record_source_run(
                    source_name=name, source_type="rss",
                    asset_class=source_asset_class, status="ok" if parsed else "ok_empty",
                    started_at=started_at, item_count=len(parsed),
                    metadata={"url": url, "http_status": getattr(response, "status_code", None),
                              "attempts": attempt_count},
                )
                self.logger.info(
                    "Fetched %s news items from %s (asset_class=%s)",
                    len(parsed), name, source_asset_class,
                )
            except Exception as exc:
                summary.failed_sources[name] = str(exc)
                status = "timeout" if isinstance(exc, requests.exceptions.Timeout) else "error"
                record_source_run(
                    source_name=name, source_type="rss",
                    asset_class=source_asset_class, status=status, started_at=started_at,
                    error_code=type(exc).__name__, error_message=str(exc),
                    metadata={"url": url, "attempts": locals().get("attempt_count", 0)},
                )
                self.logger.warning("Failed RSS source %s: %s", name, exc)

        summary.items.sort(key=lambda item: item.published_at or "", reverse=True)
        # Save per asset_class so the database column reflects the source tag.
        # Empty buckets are no-ops in save_news_items.
        for ac, items in items_by_asset_class.items():
            if items:
                self.db.save_news_items(items, asset_class=ac)
        if write_snapshot:
            self.store.save_json(
                Path("data") / "raw" / "news" / "rss_latest.json",
                {
                    "fetched_at": utc_now().isoformat(),
                    "fetched_sources": summary.fetched_sources,
                    "failed_sources": summary.failed_sources,
                    "items": [item.model_dump(mode="json") for item in summary.items],
                },
            )
        return summary

    def _parse_feed(
        self, text: str, source_name: str, primary: bool, limit: int,
        asset_class: str = "crypto",
    ) -> list[NewsItem]:
        root = ElementTree.fromstring(text)
        items = root.findall(".//item")
        if items:
            return [
                self._parse_rss_item(item, source_name, primary, asset_class)
                for item in items[:limit]
            ]

        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = root.findall(".//atom:entry", ns)
        return [
            self._parse_atom_entry(entry, source_name, primary, ns, asset_class)
            for entry in entries[:limit]
        ]

    def _parse_binance_announcements(
        self, payload: dict[str, Any], source_name: str, primary: bool, limit: int,
        asset_class: str = "crypto",
    ) -> list[NewsItem]:
        articles: list[dict[str, Any]] = []
        for catalog in payload.get("data", {}).get("catalogs", []) or []:
            articles.extend(catalog.get("articles", []) or [])
        items: list[NewsItem] = []
        for article in articles[:limit]:
            title = str(article.get("title") or "Untitled")
            code = str(article.get("code") or article.get("id") or title)
            link = f"https://www.binance.com/en/support/announcement/{code}"
            release_date = self._parse_timestamp_ms(article.get("releaseDate"))
            items.append(
                self._build_item(title, link, release_date, source_name, primary, "", asset_class)
            )
        return items

    def _parse_rss_item(
        self, item: ElementTree.Element, source_name: str, primary: bool,
        asset_class: str = "crypto",
    ) -> NewsItem:
        title = self._child_text(item, "title") or "Untitled"
        link = self._child_text(item, "link") or title
        published = self._parse_date(self._child_text(item, "pubDate") or self._child_text(item, "published"))
        # Prefer the richest payload. Many feeds expose the useful body in
        # content:encoded while description is only a duplicated headline.
        description = self._rich_content(item, ("encoded", "description", "summary", "content"))
        return self._build_item(title, link, published, source_name, primary, description, asset_class)

    def _parse_atom_entry(
        self, entry: ElementTree.Element, source_name: str, primary: bool, ns: dict[str, str],
        asset_class: str = "crypto",
    ) -> NewsItem:
        title = self._child_text(entry, "atom:title", ns) or "Untitled"
        link = ""
        link_el = entry.find("atom:link", ns)
        if link_el is not None:
            link = link_el.attrib.get("href", "")
        if not link:
            link = self._child_text(entry, "atom:id", ns) or title
        published = self._parse_date(
            self._child_text(entry, "atom:updated", ns) or self._child_text(entry, "atom:published", ns)
        )
        summary = self._rich_content(entry, ("content", "summary"))
        return self._build_item(title, link, published, source_name, primary, summary, asset_class)

    def _build_item(
        self,
        title: str,
        link: str,
        published: str | None,
        source_name: str,
        primary: bool,
        description: str,
        asset_class: str = "crypto",
    ) -> NewsItem:
        body = clean_text(description)
        text = f"{title} {body}"
        # For stocks sources, prefer the stocks universe for ticker matching;
        # also keep crypto matches in case the headline is cross-asset
        # (e.g. "MicroStrategy adds BTC"). For crypto sources, use crypto only.
        if asset_class == "stocks":
            ticker_universe = self._stocks_tickers + self.tickers
        else:
            ticker_universe = self.tickers
        detected_symbols = [ticker for ticker in ticker_universe if self._mentions_ticker(text, ticker)]

        # PART 2 enrichment — also run the curated entity-alias matcher.
        # PART 19 (2026-06-03) — now ALSO runs for stocks news using the
        # parallel ``stocks_entity_aliases.yaml`` (Apple→AAPL, Super Micro
        # → SMCI, Broadcom → AVGO, etc.). Crypto path unchanged.
        try:
            from src.catalysts.entity_aliases import get_matcher, get_stocks_matcher

            if asset_class == "stocks":
                alias_hits = get_stocks_matcher(str(self.config.root)).detect(text)
            else:
                alias_hits = get_matcher(str(self.config.root)).detect(text)
            for sym in alias_hits:
                base = sym.split("/")[0]
                if base and base not in detected_symbols:
                    detected_symbols.append(base)
        except Exception:
            # Read-only enrichment must NEVER break news ingest.
            pass
        detected_narratives = self._detect_narratives(text)
        importance = 1.0 + min(len(detected_symbols), 4) * 0.5 + min(len(detected_narratives), 3) * 0.4
        if primary:
            importance += 0.8
        return NewsItem(
            title=" ".join(title.split()),
            source=source_name,
            url=link,
            published_at=published,
            detected_symbols=detected_symbols,
            detected_narratives=detected_narratives,
            importance=round(importance, 2),
            verification_status="primary_source" if primary else "single_source",
            content=body or None,
            summary=body or None,
            ingested_at=now_iso(),
            first_seen_at=now_iso(),
            content_hash=content_hash(title, body),
        )

    def _detect_narratives(self, text: str) -> list[str]:
        upper_text = text.upper()
        detected: list[str] = []
        for name, payload in self.narratives.items():
            keywords = [str(item).upper() for item in payload.get("keywords", [])]
            symbols = [str(item).upper() for item in payload.get("symbols", [])]
            if any(keyword in upper_text for keyword in keywords) or any(
                self._mentions_ticker(text, symbol) for symbol in symbols
            ):
                detected.append(str(name))
        return detected

    @staticmethod
    def _mentions_ticker(text: str, ticker: str) -> bool:
        token = ticker.upper()
        patterns = [rf"\${re.escape(token)}(?![A-Za-z0-9])", rf"#{re.escape(token)}(?![A-Za-z0-9])"]
        if token not in AMBIGUOUS_TICKERS:
            patterns.append(rf"(?<![A-Za-z0-9]){re.escape(token)}(?![A-Za-z0-9])")
        patterns.append(rf"(?<![A-Za-z0-9]){re.escape(token)}/USDT(?![A-Za-z0-9])")
        return any(re.search(pattern, text) for pattern in patterns)

    @staticmethod
    def _child_text(
        item: ElementTree.Element, tag: str, ns: dict[str, str] | None = None
    ) -> str | None:
        child = item.find(tag, ns or {})
        if child is None or child.text is None:
            return None
        return child.text.strip()

    @staticmethod
    def _rich_content(item: ElementTree.Element, local_names: tuple[str, ...]) -> str:
        """Return the longest non-empty body across RSS/Atom namespaces."""
        values: list[str] = []
        wanted = {str(name).lower() for name in local_names}
        for child in item.iter():
            local = str(child.tag).rsplit("}", 1)[-1].split(":")[-1].lower()
            if local not in wanted:
                continue
            text = "".join(child.itertext()).strip()
            if text:
                values.append(text)
        return max(values, key=len) if values else ""

    @staticmethod
    def _parse_date(value: str | None) -> str | None:
        if not value:
            return None
        try:
            return parsedate_to_datetime(value).isoformat()
        except Exception:
            return value

    @staticmethod
    def _parse_timestamp_ms(value: Any) -> str | None:
        try:
            if value in (None, ""):
                return None
            return datetime.fromtimestamp(float(value) / 1000, timezone.utc).isoformat()
        except (TypeError, ValueError, OSError):
            return None
