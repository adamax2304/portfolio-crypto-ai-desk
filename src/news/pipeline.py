"""Fail-open incremental post-ingest news processing.

Every common SQLite news ingest path calls this after its transaction commits.
Resolution and canonical-event materialization therefore happen in seconds,
while scheduled full-window passes remain a repair/backfill safety net.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _journal(stage: str, error: Exception, urls: list[str]) -> None:
    try:
        root = Path(__file__).resolve().parents[2]
        path = root / "data" / "diagnostics" / "news_pipeline_errors.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "at": datetime.now(timezone.utc).isoformat(), "stage": stage,
            "error_type": type(error).__name__, "error": str(error)[:500],
            "url_count": len(urls), "sample_urls": urls[:5],
        }
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except Exception:
        pass


def process_ingested_urls(db: str, urls: list[str]) -> dict[str, Any]:
    """Resolve and materialize exact newly-upserted URLs. Never raises.

    Ingest remains authoritative: a resolver/policy failure is journaled and the
    raw news row stays committed for the scheduled repair pass.
    """
    clean = list(dict.fromkeys(str(u) for u in urls if str(u or "").strip()))
    result: dict[str, Any] = {"urls": len(clean), "resolver": None, "canonical": None, "errors": []}
    if not clean:
        return result
    try:
        from src.news import entity_resolver
        result["resolver"] = entity_resolver.refresh(db=db, urls=clean, limit=len(clean), write=True)
    except Exception as exc:
        _journal("entity_resolver", exc, clean)
        result["errors"].append(f"entity_resolver:{type(exc).__name__}")
    try:
        from src.news import canonical_events
        result["canonical"] = canonical_events.refresh(db=db, urls=clean)
    except Exception as exc:
        _journal("canonical_events", exc, clean)
        result["errors"].append(f"canonical_events:{type(exc).__name__}")
    return result


__all__ = ["process_ingested_urls"]
