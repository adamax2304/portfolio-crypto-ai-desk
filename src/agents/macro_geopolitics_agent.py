from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

from src.agents.base_agent import BaseAgent
from src.models import MacroGeopoliticsSummary
from src.utils.validation import clamp, model_to_dict


class MacroGeopoliticsAgent(BaseAgent):
    name = "macro_geopolitics_agent"

    _CANONICAL_MACRO_TYPES = {"fed", "cpi", "pce", "jobs", "geopolitical_risk"}
    _QUALITY_WEIGHT = {
        "regulator": 1.25, "exchange": 1.15, "primary": 1.15, "company_pr": 0.9,
        "reputable": 1.0, "secondary": 0.7, "social": 0.45,
    }

    def run(self, news_output: dict[str, Any], *, now: datetime | None = None) -> MacroGeopoliticsSummary:
        now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
        keywords = self.config.sources.get("macro_keywords", {})
        risk_off = [str(item).lower() for item in keywords.get("risk_off", [])]
        risk_on = [str(item).lower() for item in keywords.get("risk_on", [])]
        neutral_watch = [str(item).lower() for item in keywords.get("neutral_watch", [])]

        canonical = self._canonical_macro_candidates(now)
        candidates = canonical + [self._top_news_candidate(x) for x in news_output.get("top_news", [])[:50]]
        evidence: list[dict[str, Any]] = []
        for item in candidates:
            title = str(item.get("title") or "").strip()
            if not title:
                continue
            text = title.lower()
            event_type = str(item.get("event_type") or "")
            if (event_type == "geopolitical_risk" and "war" in text
                    and any(x in text for x in (
                        "stock buyback", "dividend restriction", "price war", "talent war",
                        "war on costs", "war on prices", "declares war on fees"))):
                continue
            # Canonical company/token events are not macro merely because the headline contains a
            # metaphor such as "declares war". Generic top-news rows and canonical macro_headline
            # remain eligible for keyword detection.
            if (item.get("canonical") and event_type
                    and event_type not in self._CANONICAL_MACRO_TYPES | {"macro_headline"}
                    and item.get("risk_action") != "risk_warning"):
                continue
            off_matches = self._keyword_matches(text, risk_off)
            on_matches = self._keyword_matches(text, risk_on)
            watch_matches = self._keyword_matches(text, neutral_watch)
            if self._is_corporate_macro_false_positive(
                    item, text, off_matches, on_matches, watch_matches):
                continue
            # Direction-aware handling for the most common macro false positive: "inflation cools"
            # is not the same risk signal as "inflation accelerates". Keep the headline visible as
            # macro evidence, but score the former as disinflation/risk-on.
            disinflation = self._is_disinflation(text)
            if disinflation:
                off_matches = [x for x in off_matches if x not in {"inflation", "rate hike"}]
                on_matches = sorted(set(on_matches + ["disinflation"]))
            is_geo = event_type == "geopolitical_risk" or item.get("risk_action") == "risk_warning"
            is_canonical_macro = event_type in self._CANONICAL_MACRO_TYPES
            if not (off_matches or on_matches or watch_matches or is_canonical_macro):
                continue
            age_h = self._age_hours(item.get("published_at"), now)
            if age_h is None or age_h < -0.1 or age_h > 12.0:
                continue
            row = {**item, "title": title, "off_matches": off_matches, "on_matches": on_matches,
                   "watch_matches": watch_matches, "is_geo": is_geo, "age_h": age_h}
            row["priority"] = self._priority(row)
            evidence.append(row)

        # Canonical clustering is deliberately entity/event strict and can leave differently-worded
        # relays of the same macro release as separate rows. Collapse those here by event family and
        # hour, retaining the highest-quality representation rather than whichever relay arrived last.
        deduped: dict[str, dict[str, Any]] = {}
        for row in evidence:
            key = self._semantic_key(row)
            if key not in deduped or float(row["priority"]) > float(deduped[key]["priority"]):
                deduped[key] = row
        evidence = list(deduped.values())
        evidence.sort(key=lambda x: (float(x["priority"]), str(x.get("published_at") or "")),
                      reverse=True)
        selected = evidence[:20]
        headlines = [str(x["title"]) for x in selected[:8]]
        risk_off_hits = sorted({m for x in selected for m in x["off_matches"]})
        risk_on_hits = sorted({m for x in selected for m in x["on_matches"]})
        watch_hits = sorted({m for x in selected for m in x["watch_matches"]})

        off_points = self._evidence_points(selected, side="off")
        on_points = self._evidence_points(selected, side="on")
        watch_points = min(16.0, sum(2.0 * self._quality_weight(x) for x in selected
                                    if x["watch_matches"]))
        risk_score = clamp(25 + min(75.0, off_points) + watch_points - min(32.0, on_points))
        if risk_score >= 65:
            btc_bias = "risk-off headwind"
        elif risk_score <= 30 and risk_on_hits:
            btc_bias = "risk-on tailwind"
        else:
            btc_bias = "neutral / data-watch"

        themes = sorted(set(risk_off_hits + risk_on_hits + watch_hits +
                            [str(x.get("event_type")) for x in selected if x.get("event_type")]))[:12]
        warnings = []
        if risk_score >= 65:
            warnings.append("Macro/geopolitical headlines are risk-off; reduce alt long aggression.")
        if not headlines:
            warnings.append("No macro/geopolitical news feed signal detected; check external macro calendar manually.")

        summary = MacroGeopoliticsSummary(
            risk_score=round(risk_score, 1),
            btc_bias=btc_bias,
            themes=themes,
            headlines=headlines[:8],
            warnings=warnings,
            explanation=self._explain(risk_score, risk_off_hits, risk_on_hits, watch_hits,
                                      canonical_selected=sum(1 for x in selected if x.get("canonical"))),
        )
        self.save_output(model_to_dict(summary))
        return summary

    @staticmethod
    def _parse_ts(value: Any) -> datetime | None:
        if not value:
            return None
        try:
            dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except Exception:
            return None

    @classmethod
    def _age_hours(cls, value: Any, now: datetime) -> float | None:
        dt = cls._parse_ts(value)
        return (now - dt).total_seconds() / 3600.0 if dt else None

    @staticmethod
    def _normalise_title(title: str) -> str:
        text = re.sub(r"https?://\S+", " ", str(title).lower())
        text = re.sub(r"\([^)]*@[^)]*\)", " ", text)
        text = re.sub(r"[^a-z0-9]+", " ", text)
        return " ".join(text.split())[:240]

    @staticmethod
    def _keyword_present(text: str, keyword: str) -> bool:
        value = str(keyword or "").strip().lower()
        if not value:
            return False
        escaped = re.escape(value).replace(r"\ ", r"\s+")
        suffix = {
            "attack": r"(?:s|ed|ing)?", "sanctions": "", "escalation": r"(?:s)?",
            "airstrike": r"(?:s)?", "missile": r"(?:s)?", "blockade": r"(?:s|d)?",
            "retaliation": r"(?:s)?", "war": r"(?:s)?",
        }.get(value, "")
        return bool(re.search(rf"(?<![a-z0-9]){escaped}{suffix}(?![a-z0-9])", text))

    @classmethod
    def _keyword_matches(cls, text: str, keywords: list[str]) -> list[str]:
        return sorted({word for word in keywords if cls._keyword_present(text, word)})

    @classmethod
    def _is_disinflation(cls, text: str) -> bool:
        if not ("inflation" in text or cls._keyword_present(text, "cpi")):
            return False
        phrases = (
            "inflation cool", "inflation slow", "inflation fell", "inflation fall",
            "inflation ease", "inflation drop", "soft inflation", "cpi cool", "cpi slow",
            "cpi fell", "cpi fall", "cpi ease", "cpi drop", "prices fall", "prices fell",
            "price pressures ease", "below expectation", "lower than expected",
            "inflation will be a thing of the past",
        )
        return any(x in text for x in phrases) or bool(re.search(
            r"(?:lowest.{0,24}\bcpi\b|\bcpi\b.{0,24}lowest)", text,
        ))

    @staticmethod
    def _is_corporate_macro_false_positive(
        item: dict[str, Any], text: str, off_matches: list[str], on_matches: list[str],
        watch_matches: list[str],
    ) -> bool:
        # Institution and promotion names are not evidence of war or the oil market.
        if "war college" in text:
            return True
        # Ambiguous English words need actual conflict context. Product names
        # (for example a gaming keyboard's "attack" mode), marketing copy and
        # corporate price wars are not geopolitical evidence.
        ambiguous = set(off_matches) & {"attack", "war"}
        conflict_context = any(phrase in text for phrase in (
            "military", "missile", "airstrike", "drone strike", "troops",
            "armed forces", "invasion", "border", "ceasefire", "retaliation",
            "iran", "israel", "gaza", "ukraine", "russia", "taiwan",
            "north korea", "south china sea", "strait of hormuz",
        ))
        commercial_context = any(phrase in text for phrase in (
            "gaming", "keyboard", "mouse", "headset", "product launch",
            "marketing campaign", "price war", "talent war", "war on fees",
            "war on costs", "declares war on prices",
        ))
        event_type = str(item.get("event_type") or "")
        canonical_geo = event_type == "geopolitical_risk" or \
            item.get("risk_action") == "risk_warning"
        if ambiguous and not canonical_geo and (commercial_context or not conflict_context):
            return True
        quality = str(item.get("source_quality") or "").lower()
        if (quality == "company_pr" and event_type == "macro_headline"
                and not off_matches and not on_matches
                and set(watch_matches).issubset({"oil"})):
            return True
        return False

    @classmethod
    def _semantic_key(cls, item: dict[str, Any]) -> str:
        event_type = str(item.get("event_type") or "")
        dt = cls._parse_ts(item.get("published_at"))
        bucket = dt.strftime("%Y-%m-%dT%H") if dt else "unknown"
        title = str(item.get("title") or "").lower()
        if event_type == "geopolitical_risk" or item.get("is_geo"):
            if "blockade" in title or "strait of hormuz" in title:
                family = "shipping_conflict"
            elif any(x in title for x in ("missile", "airstrike", "military strike", "retaliat", "attack")):
                family = "military_conflict"
            elif "sanction" in title:
                family = "sanctions"
            else:
                family = "geopolitical"
            return f"geo:{family}:{bucket}"
        if event_type in {"fed", "cpi", "pce", "jobs"}:
            return f"macro:{event_type}:{bucket}"
        return f"title:{cls._normalise_title(title)}"

    @staticmethod
    def _source_family(source: Any) -> str:
        value = str(source or "unknown").lower().strip()
        if value.startswith("t.me/"):
            return value.split("/", 1)[1]
        return re.sub(r"[^a-z0-9]+", "", value)[:40] or "unknown"

    @classmethod
    def _quality_weight(cls, item: dict[str, Any]) -> float:
        return cls._QUALITY_WEIGHT.get(str(item.get("source_quality") or "secondary"), 0.7)

    @classmethod
    def _priority(cls, item: dict[str, Any]) -> float:
        recency = max(0.0, 12.0 - float(item.get("age_h") or 0.0)) * 3.0
        event = 28.0 if item.get("is_geo") else (
            18.0 if item.get("event_type") in cls._CANONICAL_MACRO_TYPES else 0.0)
        quality = cls._quality_weight(item) * 15.0
        corroboration = min(4, int(item.get("corroboration_count") or 1)) * 3.0
        return recency + event + quality + corroboration + float(item.get("confidence") or 0.0) * 10.0

    @classmethod
    def _evidence_points(cls, evidence: list[dict[str, Any]], *, side: str) -> float:
        """Source/event bounded points; a relay flood from one social source cannot dominate."""
        best_by_source_event: dict[tuple[str, str], float] = {}
        social_total = 0.0
        for item in evidence:
            matches = item["off_matches"] if side == "off" else item["on_matches"]
            if not matches and not (side == "off" and item.get("is_geo")):
                continue
            quality = str(item.get("source_quality") or "secondary")
            base = 10.0 * cls._quality_weight(item)
            if side == "off" and item.get("is_geo"):
                base += 15.0 * cls._quality_weight(item)
                if (int(item.get("corroboration_count") or 1) >= 2
                        and int(item.get("independent_non_social_count") or 0) >= 1):
                    base += 16.0 * cls._quality_weight(item)
            recency = max(0.35, 1.0 - float(item.get("age_h") or 0.0) / 16.0)
            value = base * recency
            if quality == "social":
                remaining = max(0.0, 12.0 - social_total)
                value = min(value, remaining)
                social_total += value
            key = (cls._source_family(item.get("source")), str(item.get("event_type") or matches[0]))
            best_by_source_event[key] = max(best_by_source_event.get(key, 0.0), value)
        return sum(best_by_source_event.values())

    def _canonical_macro_candidates(self, now: datetime) -> list[dict[str, Any]]:
        """Fresh canonical primaries, independent of the generic top-news ranking. Fail-open."""
        try:
            with self.db.connect() as conn:
                exists = conn.execute(
                    "SELECT 1 FROM sqlite_master WHERE type='table' AND name='news_canonical_events'"
                ).fetchone()
                if not exists:
                    return []
                rows = conn.execute(
                    "SELECT title,source,published_at,event_type,source_quality,confidence,"
                    "risk_action,corroboration_count,independent_non_social_count,expires_at "
                    "FROM news_canonical_events WHERE is_cluster_primary=1 "
                    "ORDER BY published_at DESC LIMIT 750"
                ).fetchall()
            out = []
            for raw in rows:
                row = dict(raw)
                age = self._age_hours(row.get("published_at"), now)
                expires = self._parse_ts(row.get("expires_at"))
                if age is None or age < -0.1 or age > 12.0 or (expires and expires < now):
                    continue
                row["canonical"] = True
                out.append(row)
            return out
        except Exception:
            return []

    @staticmethod
    def _top_news_candidate(item: dict[str, Any]) -> dict[str, Any]:
        canonical = item.get("canonical_event") if isinstance(item.get("canonical_event"), dict) else {}
        return {
            "title": item.get("title"), "source": item.get("source"),
            "published_at": item.get("published_at"), "event_type": canonical.get("event_type"),
            "source_quality": canonical.get("source_quality") or "secondary",
            "confidence": canonical.get("confidence") or 0.0,
            "risk_action": canonical.get("risk_action") or "none",
            "corroboration_count": 1, "canonical": False,
        }

    @staticmethod
    def _explain(
        risk_score: float, risk_off_hits: list[str], risk_on_hits: list[str], watch_hits: list[str],
        *, canonical_selected: int = 0,
    ) -> str:
        if not risk_off_hits and not risk_on_hits and not watch_hits:
            return "RSS did not surface clear macro/geopolitical drivers."
        return (
            f"Macro risk score {round(risk_score, 1)}/100 from "
            f"{len(risk_off_hits)} risk-off hit(s), {len(risk_on_hits)} risk-on hit(s), "
            f"and {len(watch_hits)} calendar/watch hit(s); "
            f"{canonical_selected} fresh canonical event(s) selected."
        )
