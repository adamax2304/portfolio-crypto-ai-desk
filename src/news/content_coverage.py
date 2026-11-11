"""Read-only visibility into how much usable text each news source preserves.

Entity recognition from a headline alone is inherently weaker than recognition from
the original message/article body.  This module makes that distinction measurable;
it never fetches, modifies ``news_items``, scores, or trading state.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.config import load_config
from src.news.entity_resolver import extract_text_fields
from src.news.source_health import window_news_rows


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def _norm(value: str | None) -> str:
    return " ".join(str(value or "").lower().split())


def content_level(row: dict[str, Any]) -> str:
    """Classify retained content without mistaking a duplicated title for a body."""
    fields = extract_text_fields(row)
    title = _norm(fields["title"])
    body = _norm(fields["body"])
    summary = _norm(" ".join((fields["summary"], fields["description"])))
    if body:
        return "full_body" if body != title else "body_equals_title"
    if summary and summary != title:
        return "summary_only"
    return "title_only"


def _blank() -> dict[str, int]:
    return {"rows": 0, "full_body": 0, "body_equals_title": 0, "summary_only": 0, "title_only": 0}


def _finish(bucket: dict[str, int]) -> dict[str, Any]:
    total = bucket["rows"]
    return {
        **bucket,
        "full_body_rate": round(bucket["full_body"] / total, 3) if total else None,
        "retained_body_rate": round((bucket["full_body"] + bucket["body_equals_title"]) / total, 3) if total else None,
        "title_only_rate": round(bucket["title_only"] / total, 3) if total else None,
    }


def compute_content_coverage(db: str | None = None, *, hours: int = 72,
                             now: datetime | None = None, examples: int = 12) -> dict[str, Any]:
    """Summarise title-only versus retained body/summary by source and asset class."""
    path = db or str(load_config().db_path)
    now = now or datetime.now(timezone.utc)
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        rows = window_news_rows(
            conn, hours=int(hours), now=now,
            columns="title, source, url, published_at, asset_class, raw_json, content_text",
        ) or []
    except sqlite3.OperationalError:
        rows = []
    finally:
        conn.close()

    total = _blank()
    by_asset: dict[str, dict[str, int]] = {}
    by_source: dict[str, dict[str, int]] = {}
    title_only_examples: list[dict[str, Any]] = []
    for row in rows:
        level = content_level(row)
        asset = str(row.get("asset_class") or "unknown").lower()
        source = str(row.get("source") or "unknown")
        for bucket in (total, by_asset.setdefault(asset, _blank()), by_source.setdefault(source, _blank())):
            bucket["rows"] += 1
            bucket[level] += 1
        if level == "title_only" and len(title_only_examples) < examples:
            title_only_examples.append({
                "source": source, "asset_class": asset, "published_at": row["_ts"].isoformat(),
                "title": str(row.get("title") or "")[:180], "url": row.get("url"),
            })

    source_rows = [
        {"source": source, **_finish(bucket)} for source, bucket in by_source.items()
    ]
    source_rows.sort(key=lambda item: (-item["rows"], item["source"]))
    return {
        "generated_at": now.isoformat(), "hours": int(hours), "summary": _finish(total),
        "by_asset_class": {asset: _finish(bucket) for asset, bucket in sorted(by_asset.items())},
        "by_source": source_rows, "title_only_examples": title_only_examples,
        "note": "READ-ONLY content-retention diagnostic. title_only means no body or summary was retained; "
                "body_equals_title is a complete short retained message, not a missing body.",
    }


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# News Content Coverage", "",
        f"_Generated: {report['generated_at'][:19]}Z · last {report['hours']}h · read-only._", "",
        f"**{summary['rows']} rows** · full body **{summary['full_body']}** "
        f"({int((summary['full_body_rate'] or 0) * 100)}%) · body=same-as-title **{summary['body_equals_title']}** · "
        f"summary-only **{summary['summary_only']}** · "
        f"title-only **{summary['title_only']}** ({int((summary['title_only_rate'] or 0) * 100)}%)", "",
        "| asset | rows | full body | body=same title | summary only | title only |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for asset, item in report["by_asset_class"].items():
        lines.append(f"| {asset} | {item['rows']} | {item['full_body']} | {item['body_equals_title']} | "
                     f"{item['summary_only']} | {item['title_only']} |")
    lines += ["", "## Sources", "", "| source | rows | full body | same title | title-only |", "|---|---:|---:|---:|---:|"]
    for item in report["by_source"]:
        lines.append(f"| {item['source']} | {item['rows']} | {item['full_body']} | "
                     f"{item['body_equals_title']} | {item['title_only']} |")
    examples = report.get("title_only_examples") or []
    if examples:
        lines += ["", "## Recent title-only examples", ""]
        for item in examples:
            lines.append(f"- [{item['asset_class']}] {item['source']} · {item['title']}")
    lines += ["", f"_{report['note']}_"]
    return "\n".join(lines)


def refresh(db: str | None = None, *, hours: int = 72, now: datetime | None = None,
            write: bool = True) -> dict[str, Any]:
    report = compute_content_coverage(db, hours=hours, now=now)
    if write:
        root = _root()
        (root / "reports").mkdir(parents=True, exist_ok=True)
        (root / "data" / "diagnostics").mkdir(parents=True, exist_ok=True)
        (root / "reports" / "NEWS_CONTENT_COVERAGE.md").write_text(render_markdown(report), encoding="utf-8")
        (root / "data" / "diagnostics" / "news_content_coverage.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


__all__ = ["content_level", "compute_content_coverage", "render_markdown", "refresh"]
