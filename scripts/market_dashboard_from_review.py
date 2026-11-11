"""PART 11 — populate the Market tab from the Opus enriched review (fail-open).

Runs at the END of the ~4h enriched-review routine. Reads the latest enriched-review
markdown (or a path/stdin), extracts the trailing `market_dashboard_update` JSON block,
and stores a `market_dashboard_snapshots` row. If no valid block is found, writes a
deterministic fallback so the Market tab never goes empty. **Does not change the
enriched-review body/logic** — it only consumes the trailing block.

Usage:
  python -m scripts.market_dashboard_from_review [--file PATH] [--fallback-only]
"""
from __future__ import annotations

import argparse
import glob
import os
import sys

from src.market.market_dashboard import parse_and_store, deterministic_fallback, DB

_GLOBS = [
    "*ENRICHED_REVIEW*.md", "reports/*ENRICHED_REVIEW*.md",
    "data/raw/enriched_review_sources/*ENRICHED_REVIEW*.md",
    "obsidian_vault/**/*Enriched*Review*.md",
]


def _latest_review() -> str | None:
    cands: list[str] = []
    for g in _GLOBS:
        cands += glob.glob(g, recursive=True)
    if not cands:
        return None
    return max(cands, key=lambda p: os.path.getmtime(p))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", help="enriched-review markdown path (default: latest found)")
    ap.add_argument("--fallback-only", action="store_true", help="write deterministic fallback only")
    ap.add_argument("--db", default=DB)
    args = ap.parse_args()

    if args.fallback_only:
        print("fallback:", deterministic_fallback(args.db))
        return 0

    path = args.file or _latest_review()
    text = ""
    if path and os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        print(f"reading review: {path}")
    elif not sys.stdin.isatty():
        text = sys.stdin.read()

    res = parse_and_store(text, args.db) if text else {"stored": False, "reason": "no review text"}
    if not res.get("stored"):
        print(f"no market block ({res.get('reason')}) → deterministic fallback")
        print("fallback:", deterministic_fallback(args.db))
        return 0
    print("stored market snapshot:", res)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
