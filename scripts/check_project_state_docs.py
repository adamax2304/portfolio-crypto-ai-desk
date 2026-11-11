"""Lightweight project-state doc validator (documentation sprint).

Checks that the project-state doc layer exists and that PROJECT_STATE.md still
carries the key safety phrases. Read-only; exits non-zero on failure so it can be
used in CI / pre-flight. No trading logic touched.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "PROJECT_STATE.md",
    "docs/DECISION_LOG.md",
    "docs/AGENT_HANDOFF.md",
    "docs/WEEKLY_FORWARD_METRICS.md",
    "docs/decisions/ADR-TEMPLATE.md",
]

# Accept either casing for the live-readiness phrase.
REQUIRED_PHRASES_ANY = [
    ("SYSTEM IS NOT LIVE-READY", "System is NOT live-ready"),
]
REQUIRED_PHRASES_ALL = [
    "PROFIT_PROTECTION_STILL_DISABLED",
    "MICRO_LIVE_CANARY_REVIEW_IN_7_10_DAYS",
    "NO_PRODUCTION_TRADE_MATH_CHANGE",
]


def check() -> list[str]:
    problems: list[str] = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            problems.append(f"missing file: {rel}")

    ps = ROOT / "PROJECT_STATE.md"
    text = ps.read_text(encoding="utf-8") if ps.exists() else ""
    for variants in REQUIRED_PHRASES_ANY:
        if not any(v in text for v in variants):
            problems.append(f"PROJECT_STATE.md missing any of: {variants}")
    for phrase in REQUIRED_PHRASES_ALL:
        if phrase not in text:
            problems.append(f"PROJECT_STATE.md missing phrase: {phrase}")
    return problems


def main() -> int:
    problems = check()
    if problems:
        print("PROJECT STATE DOCS: FAIL")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("PROJECT STATE DOCS: OK — all required docs present and PROJECT_STATE.md intact.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
