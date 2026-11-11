from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Any

import requests

from src.config import ProjectConfig
from src.logger import get_logger
from src.storage.file_store import FileStore
from src.utils.symbols import symbol_to_ticker
from src.utils.time import utc_now


AMBIGUOUS_TICKERS = {"LINK", "NEAR", "OP", "SEI", "APT"}


@dataclass
class SocialCollectionSummary:
    fetched_sources: list[str] = field(default_factory=list)
    failed_sources: dict[str, str] = field(default_factory=dict)
    mentions: list[dict[str, Any]] = field(default_factory=list)


class SocialCollector:
    """Fetch lightweight public social attention signals.

    The MVP deliberately uses public/free sources only. X/Telegram/Discord are
    represented by manual notes because reliable live access usually needs paid
    APIs, scraping, or private credentials.
    """

    def __init__(self, config: ProjectConfig, store: FileStore):
        self.config = config
        self.store = store
        self.logger = get_logger(self.__class__.__name__)
        self.tickers = sorted({symbol_to_ticker(symbol) for symbol in config.symbols}, key=len, reverse=True)
        self.narratives = config.watchlist.get("narratives", {})

    def fetch(self) -> SocialCollectionSummary:
        summary = SocialCollectionSummary()
        for source in self.config.sources.get("social_sources", []):
            name = str(source.get("name", "unknown"))
            url = str(source.get("url", ""))
            source_type = str(source.get("type", "reddit_json"))
            if not url:
                continue
            try:
                response = requests.get(
                    url,
                    timeout=20,
                    headers={
                        "User-Agent": "crypto-ai-desk/0.1 local research tool",
                        "Accept": "application/json,text/plain,*/*",
                    },
                )
                response.raise_for_status()
                if source_type == "reddit_json":
                    mentions = self._parse_reddit_json(response.json(), name)
                else:
                    mentions = []
                summary.mentions.extend(mentions)
                summary.fetched_sources.append(name)
                self.logger.info("Fetched %s social mentions from %s", len(mentions), name)
            except Exception as exc:
                summary.failed_sources[name] = str(exc)
                self.logger.warning("Failed social source %s: %s", name, exc)

        summary.mentions.extend(self._load_manual_mentions())
        self.store.save_json(
            Path("data") / "raw" / "social" / "social_latest.json",
            {
                "fetched_at": utc_now().isoformat(),
                "fetched_sources": summary.fetched_sources,
                "failed_sources": summary.failed_sources,
                "mentions": summary.mentions,
            },
        )
        return summary

    def _parse_reddit_json(self, payload: dict[str, Any], source_name: str) -> list[dict[str, Any]]:
        mentions: list[dict[str, Any]] = []
        children = payload.get("data", {}).get("children", [])
        for child in children:
            data = child.get("data", {})
            title = str(data.get("title") or "")
            text = " ".join([title, str(data.get("selftext") or "")])
            symbols = [ticker for ticker in self.tickers if self._mentions_ticker(text, ticker)]
            narratives = self._detect_narratives(text)
            if not symbols and not narratives:
                continue
            mentions.append(
                {
                    "observed_at": utc_now().isoformat(),
                    "source": source_name,
                    "title": " ".join(title.split()),
                    "url": f"https://www.reddit.com{data.get('permalink', '')}",
                    "symbols": symbols,
                    "narratives": narratives,
                    "score": int(data.get("score") or 0),
                    "comments": int(data.get("num_comments") or 0),
                    "type": "reddit_post",
                }
            )
        return mentions

    def _load_manual_mentions(self) -> list[dict[str, Any]]:
        path = self.config.root / "data" / "raw" / "social" / "manual_social_mentions.yaml"
        if not path.exists():
            return []
        try:
            import yaml

            payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except Exception as exc:
            self.logger.warning("Failed manual social mentions: %s", exc)
            return []

        mentions = []
        for item in payload.get("mentions", []) or []:
            if not isinstance(item, dict):
                continue
            symbol = str(item.get("symbol") or "").upper()
            ticker = symbol_to_ticker(symbol) if symbol else ""
            mentions.append(
                {
                    "observed_at": str(item.get("observed_at") or utc_now().isoformat()),
                    "source": str(item.get("source") or "Manual social note"),
                    "title": str(item.get("note") or item.get("topic") or "Manual crowd signal"),
                    "url": str(item.get("url") or ""),
                    "symbols": [ticker] if ticker else [],
                    "narratives": [],
                    "stance": str(item.get("stance") or "unclear"),
                    "confidence": str(item.get("confidence") or "low"),
                    "type": "manual_social_note",
                }
            )
        return mentions

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
        return any(re.search(pattern, text.upper()) for pattern in patterns)
