"""Ingest external sources collected during an enriched review into ``news_items``.

Companion to ``.claude/skills/enriched-review/SKILL.md`` (PART 4 §14
source-discipline workflow). When the LLM running an enriched review
collects URLs via WebSearch + WebFetch, this script writes them into the
SQLite ``news_items`` table so:

* the next pipeline cycle (CompanyNewsAgent / NewsAgent / CatalystAgent)
  sees those sources automatically;
* the OPUS_ENRICHED_REVIEW_*.md "Sources" section maps 1:1 to a row in
  the database for audit purposes;
* ``test_source`` / fixture data is rejected at ingest time, never
  contaminating production runs.

Input format
------------

A JSON file with a list of items::

    [
      {
        "title": "Bitcoin Whales Are Pulling Back as Activity Mirrors 2022 Bear Market",
        "source": "Decrypt",
        "url": "https://decrypt.co/example",
        "published_at": "2026-05-30T12:00:00Z",
        "detected_symbols": ["BTC/USDT"],
        "detected_narratives": ["macro"],
        "importance": 0.7,
        "verification_status": "single_source"
      },
      ...
    ]

Validation rules (per §14):

* ``source`` must NOT be in ``SQLiteStore.TEST_NEWS_SOURCES``
  (``test_source``, ``fixture`` etc).
* ``url`` must be non-empty (UNIQUE constraint upserts on it).
* ``verification_status`` must be one of:
  ``primary_source / single_source / social_only / unverifiable``.
  ``unverifiable`` items are **rejected** (per §14: "If you cannot cite
  it, you may not state it as fact" — and we don't want unverifiables
  polluting future cycles).
* ``published_at`` may be ``null`` (the script tags it
  ``"date unavailable"`` inside ``raw_json`` but still ingests, since
  the source name + URL are enough for an audit).

Idempotent
----------

``SQLiteStore.save_news_items`` upserts ``ON CONFLICT(url)`` — running
the same JSON twice is safe.

Usage
-----

::

    python -m scripts.ingest_enriched_review_sources \\
        --json data/raw/enriched_review_sources/2026-05-30_2100.json

    python -m scripts.ingest_enriched_review_sources \\
        --json - < sources.json   # stdin
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from src.config import load_config
from src.models import NewsItem
from src.storage.sqlite import SQLiteStore


VALID_VERIFICATION = {
    "primary_source",
    "single_source",
    "social_only",
    "unverifiable",  # parsed but rejected — see below
}

# Items with these verification levels are NOT ingested. Per §14 they
# may not be stated as fact, and we don't want them leaking into the
# CompanyNewsAgent / CatalystAgent inputs.
REJECT_VERIFICATION = {"unverifiable"}


def _load_input(path: str) -> list[dict[str, Any]]:
    if path == "-":
        return json.loads(sys.stdin.read())
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("input JSON must be a list of items")
    return data


def _to_news_item(raw: dict[str, Any], *, rejected: list[dict[str, Any]]) -> NewsItem | None:
    src = str(raw.get("source") or "").strip()
    url = str(raw.get("url") or "").strip()
    title = str(raw.get("title") or "").strip()
    if not url:
        rejected.append({"reason": "missing url", "item": raw})
        return None
    if not title:
        rejected.append({"reason": "missing title", "item": raw})
        return None
    if not src:
        rejected.append({"reason": "missing source", "item": raw})
        return None

    if src.lower() in SQLiteStore.TEST_NEWS_SOURCES:
        rejected.append({"reason": "test_source rejected (§14)", "item": raw})
        return None

    verification = str(raw.get("verification_status") or "single_source").strip().lower()
    if verification not in VALID_VERIFICATION:
        rejected.append(
            {"reason": f"unknown verification_status={verification!r}", "item": raw}
        )
        return None
    if verification in REJECT_VERIFICATION:
        rejected.append(
            {"reason": f"verification={verification} not citable (§14)", "item": raw}
        )
        return None

    detected_symbols = list(raw.get("detected_symbols") or [])
    detected_narratives = list(raw.get("detected_narratives") or [])
    importance_raw = raw.get("importance", 0.5)
    try:
        importance = float(importance_raw)
    except (TypeError, ValueError):
        importance = 0.5
    importance = max(0.0, min(1.0, importance))

    published = raw.get("published_at")
    published_str: str | None = None
    if published:
        published_str = str(published)

    return NewsItem(
        title=title[:480],
        source=src[:120],
        url=url[:512],
        published_at=published_str,
        detected_symbols=[str(s) for s in detected_symbols][:30],
        detected_narratives=[str(n) for n in detected_narratives][:10],
        importance=importance,
        verification_status=verification,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--json",
        required=True,
        help="Path to a JSON file with the list of items, or '-' for stdin.",
    )
    ap.add_argument(
        "--asset-class",
        default="crypto",
        choices=("crypto", "stocks"),
        help="Asset class tag for the inserted rows (default crypto).",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate + report without writing to SQLite.",
    )
    args = ap.parse_args()

    raw_items = _load_input(args.json)
    rejected: list[dict[str, Any]] = []
    items: list[NewsItem] = []
    for raw in raw_items:
        item = _to_news_item(raw, rejected=rejected)
        if item is not None:
            items.append(item)

    print(f"input: {len(raw_items)} | valid: {len(items)} | rejected: {len(rejected)}")
    for r in rejected:
        print(f"  REJECTED [{r['reason']}] url={r['item'].get('url')!r}")

    if args.dry_run:
        print("--dry-run — no DB writes")
        return 0

    if not items:
        print("nothing to write")
        return 0

    config = load_config()
    db = SQLiteStore(config.db_path)
    db.init_db()
    saved = db.save_news_items(items, asset_class=args.asset_class)
    print(f"wrote {saved} row(s) to news_items (asset_class={args.asset_class})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
