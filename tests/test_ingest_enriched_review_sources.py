"""Tests for scripts/ingest_enriched_review_sources.py — PART 4 §14
source-discipline ingest pipeline used by the enriched-review skill.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.ingest_enriched_review_sources import _to_news_item


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _collect(items: list[dict]) -> tuple[list, list]:
    rejected: list[dict] = []
    valid = []
    for raw in items:
        item = _to_news_item(raw, rejected=rejected)
        if item is not None:
            valid.append(item)
    return valid, rejected


def test_primary_source_accepted():
    valid, rejected = _collect([
        {
            "title": "Binance launches GENIUS HODLer Airdrop",
            "source": "Binance Announcements",
            "url": "https://www.binance.com/example",
            "published_at": "2026-05-30T14:00:00Z",
            "detected_symbols": ["BNB"],
            "verification_status": "primary_source",
        }
    ])
    assert len(valid) == 1
    assert len(rejected) == 0
    assert valid[0].verification_status == "primary_source"
    assert valid[0].detected_symbols == ["BNB"]


def test_test_source_rejected():
    valid, rejected = _collect([
        {
            "title": "fake",
            "source": "test_source",
            "url": "https://example.com/test",
            "verification_status": "single_source",
        }
    ])
    assert valid == []
    assert len(rejected) == 1
    assert "test_source" in rejected[0]["reason"]


def test_unverifiable_rejected():
    """§14: 'If you cannot cite it, you may not state it as fact.'"""

    valid, rejected = _collect([
        {
            "title": "vague rumor",
            "source": "anon",
            "url": "https://example.com/rumor",
            "verification_status": "unverifiable",
        }
    ])
    assert valid == []
    assert len(rejected) == 1
    assert "unverifiable" in rejected[0]["reason"]


def test_missing_url_rejected():
    valid, rejected = _collect([
        {"title": "x", "source": "CoinDesk", "verification_status": "single_source"}
    ])
    assert valid == []
    assert "missing url" in rejected[0]["reason"]


def test_missing_source_rejected():
    valid, rejected = _collect([
        {"title": "x", "url": "https://example.com/x",
         "verification_status": "single_source"}
    ])
    assert valid == []
    assert "missing source" in rejected[0]["reason"]


def test_unknown_verification_rejected():
    valid, rejected = _collect([
        {
            "title": "x",
            "source": "CoinDesk",
            "url": "https://example.com/x",
            "verification_status": "made_up",
        }
    ])
    assert valid == []
    assert "unknown verification_status" in rejected[0]["reason"]


def test_default_verification_is_single_source():
    valid, _ = _collect([
        {"title": "x", "source": "CoinDesk", "url": "https://example.com/x"}
    ])
    assert len(valid) == 1
    assert valid[0].verification_status == "single_source"


def test_importance_clamped_to_unit_interval():
    valid, _ = _collect([
        {
            "title": "x",
            "source": "CoinDesk",
            "url": "https://example.com/clamp1",
            "importance": 5.0,
        },
        {
            "title": "x",
            "source": "CoinDesk",
            "url": "https://example.com/clamp2",
            "importance": -0.5,
        },
        {
            "title": "x",
            "source": "CoinDesk",
            "url": "https://example.com/clamp3",
            "importance": "not a number",
        },
    ])
    assert [v.importance for v in valid] == [1.0, 0.0, 0.5]


def test_dry_run_does_not_write(tmp_path):
    """Smoke: invoke the script with --dry-run and confirm it returns 0
    and prints the rejected counts without touching the DB."""

    payload = [
        {
            "title": "good",
            "source": "CoinDesk",
            "url": "https://example.com/dry-good",
            "verification_status": "single_source",
        },
        {
            "title": "bad",
            "source": "test_source",
            "url": "https://example.com/dry-bad",
            "verification_status": "single_source",
        },
    ]
    fp = tmp_path / "input.json"
    fp.write_text(json.dumps(payload), encoding="utf-8")

    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.ingest_enriched_review_sources",
            "--json",
            str(fp),
            "--dry-run",
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )
    assert proc.returncode == 0, proc.stderr
    out = proc.stdout
    assert "input: 2 | valid: 1 | rejected: 1" in out
    assert "test_source" in out
    assert "--dry-run" in out
