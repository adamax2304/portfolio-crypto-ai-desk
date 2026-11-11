from __future__ import annotations

import json
from typing import Any

from src.agents.base_agent import BaseAgent
from src.models import NewsItem


class NewsAgent(BaseAgent):
    name = "news_agent"

    def run(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        items = [self._row_to_item(row) for row in rows]
        items.sort(key=lambda item: (item.importance, item.published_at or ""), reverse=True)
        trusted_by_url: dict[str, list[str]] = {}
        for row in rows:
            if "trusted_symbols_json" not in row:
                continue
            try:
                trusted_by_url[str(row.get("url") or "")] = list(
                    json.loads(row.get("trusted_symbols_json") or "[]") or []
                )
            except Exception:
                trusted_by_url[str(row.get("url") or "")] = []

        canonical_by_url: dict[str, dict[str, Any]] = {}
        canonical_active = False
        try:
            with self.db.connect() as conn:
                canonical_active = bool(conn.execute(
                    "SELECT 1 FROM sqlite_master WHERE type='table' AND name='news_canonical_events'"
                ).fetchone())
                if canonical_active:
                    for row in conn.execute(
                        "SELECT url,trusted_symbols_json,event_type,direction_hint,source_quality,"
                        "content_level,confidence,linkage_allowed,linkage_reason,risk_action,policy_version "
                        "FROM news_canonical_events"
                    ):
                        canonical_by_url[str(row["url"] or "")] = dict(row)
        except Exception:
            canonical_active = False

        by_symbol: dict[str, list[dict[str, Any]]] = {}
        risk_by_symbol: dict[str, list[dict[str, Any]]] = {}
        by_narrative: dict[str, list[dict[str, Any]]] = {}
        for item in items:
            payload = item.model_dump(mode="json")
            canonical = canonical_by_url.get(str(item.url or "")) if canonical_active else None
            if canonical:
                payload["canonical_event"] = {k: canonical.get(k) for k in (
                    "event_type", "direction_hint", "source_quality", "content_level", "confidence",
                    "linkage_allowed", "linkage_reason", "risk_action", "policy_version")}
                try:
                    subject_symbols = json.loads(canonical.get("trusted_symbols_json") or "[]")
                except Exception:
                    subject_symbols = []
            else:
                if not canonical_active:
                    subject_symbols = trusted_by_url.get(
                        str(item.url or ""), list(item.detected_symbols)
                    )
                else:
                    subject_symbols = []
            positive_symbols = subject_symbols if (
                not canonical_active or bool(canonical and canonical.get("linkage_allowed")
                                             and canonical.get("direction_hint") == "bullish")) else []
            risk_symbols = subject_symbols if (
                canonical and (canonical.get("risk_action") not in (None, "none")
                               or canonical.get("direction_hint") == "bearish")) else []
            for symbol in positive_symbols:
                symbol = str(symbol).split("/")[0].upper()
                by_symbol.setdefault(symbol, []).append(payload)
            for symbol in risk_symbols:
                symbol = str(symbol).split("/")[0].upper()
                risk_by_symbol.setdefault(symbol, []).append(payload)
            for narrative in item.detected_narratives:
                by_narrative.setdefault(narrative, []).append(payload)

        output = {
            "top_news": [item.model_dump(mode="json") for item in items[:15]],
            "by_symbol": {key: value[:8] for key, value in by_symbol.items()},
            "risk_by_symbol": {key: value[:8] for key, value in risk_by_symbol.items()},
            "by_narrative": {key: value[:8] for key, value in by_narrative.items()},
            "canonical_policy_active": canonical_active,
            "warnings": []
            if items
            else ["No RSS news items available; catalyst/news confidence is low."],
        }
        self.save_output(output)
        return output

    @staticmethod
    def _row_to_item(row: dict[str, Any]) -> NewsItem:
        raw = row.get("raw_json")
        item: NewsItem | None = None
        if raw:
            try:
                item = NewsItem.model_validate(json.loads(raw))
            except Exception:
                pass
        try:
            symbols = json.loads(row.get("detected_symbols_json") or "[]")
        except Exception:
            symbols = []
        try:
            narratives = json.loads(row.get("detected_narratives_json") or "[]")
        except Exception:
            narratives = []
        updates = {
            "title": str(row.get("title") or (item.title if item else "")),
            "source": str(row.get("source") or (item.source if item else "")),
            "url": str(row.get("url") or (item.url if item else row.get("title") or "")),
            "published_at": row.get("published_at") or (item.published_at if item else None),
            "detected_symbols": symbols, "detected_narratives": narratives,
            "importance": float(row.get("importance") or (item.importance if item else 1)),
            "content": row.get("content_text") or (item.content if item else None),
        }
        return item.model_copy(update=updates) if item is not None else NewsItem(**updates)
