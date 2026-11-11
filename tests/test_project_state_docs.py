"""Project-state doc-layer validation (documentation sprint).

Confirms the doc layer exists and PROJECT_STATE.md carries the key safety phrases.
No trading logic touched.
"""
from __future__ import annotations

from pathlib import Path

import scripts.check_project_state_docs as chk

ROOT = Path(__file__).resolve().parent.parent


def test_required_docs_exist_and_phrases_present():
    assert chk.check() == [], f"doc-layer problems: {chk.check()}"


def test_required_files_individually():
    for rel in chk.REQUIRED_FILES:
        assert (ROOT / rel).exists(), f"missing {rel}"


def test_adrs_present():
    for adr in ("ADR-0001-live-remains-locked.md",
                "ADR-0002-profit-protection-disabled.md",
                "ADR-0003-c-tier-stocks-intraday-shadow.md",
                "ADR-0004-ohlcv-backfill-and-shadow-exits.md",
                "ADR-0005-manual-micro-live-canary-gate.md"):
        assert (ROOT / "docs" / "decisions" / adr).exists(), f"missing {adr}"


def test_project_state_has_locked_rules_and_gate():
    text = (ROOT / "PROJECT_STATE.md").read_text(encoding="utf-8")
    assert "Locked Rules" in text
    assert "Manual Micro-Live Gate" in text
    assert "System is NOT live-ready" in text


def test_validator_returns_clean():
    assert chk.main() == 0
