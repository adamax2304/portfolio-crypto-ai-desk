"""Lightweight validator for the Agent Council routine prompt rewrite.

Read-only. Checks that the scheduled-task prompt
(~/.claude/scheduled-tasks/opus-enriched-review-4h/SKILL.md) and the repo
protocol (prompts/llm_review/enriched_market_review_protocol.md) keep the
permission contract intact AND carry the new Agent Council structure +
status-language rules. Exits non-zero on any failure. Touches no trading logic.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCHED = Path(os.path.expanduser("~")) / ".claude" / "scheduled-tasks" / "opus-enriched-review-4h" / "SKILL.md"
PROTOCOL = REPO / "prompts" / "llm_review" / "enriched_market_review_protocol.md"

AGENTS = [
    "data_quality", "market_regime", "catalyst_narrative", "derivatives_squeeze",
    "technical_entry", "execution_lifecycle", "risk_manager",
    "playbook_performance", "head_trader",
]


def _check(name: str, cond: bool, problems: list[str]) -> None:
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        problems.append(name)


def validate_scheduled(text: str, problems: list[str]) -> None:
    print("== scheduled-task SKILL.md ==")
    # Permission contract preserved
    _check("permission contract present", "# PERMISSION CONTRACT" in text, problems)
    _check("ALLOWED actions section", "## A. ALLOWED actions" in text, problems)
    _check("FORBIDDEN actions section", "## B. FORBIDDEN actions" in text, problems)
    _check("no-permission-prompt absolute rule",
           "PERMISSION PROMPTS" in text and "do not request" in text.lower(), problems)
    _check("no code edits (forbidden)", "Edit ANY code" in text, problems)
    _check("no pytest from scheduled run", "Run `pytest`" in text or "run `pytest`" in text.lower(), problems)
    _check("no scheduler restart", "restart" in text.lower() and "CryptoAIDesk" in text, problems)
    _check("no auto-trade (forbidden)", "Auto-trade" in text, problems)
    _check("ALWAYS-SCAN — never stop scanner/monitor/system",
           "never" in text.lower() and "disabling, pausing, or stopping" in text.lower(), problems)
    _check("TODO-only maintenance section", "Fix Requests / TODO" in text and "DO NOT attempt to fix" in text, problems)
    # Agent Council
    _check("Agent Council mode section", "AGENT COUNCIL REVIEW MODE" in text, problems)
    _check("one LLM run, not physical agents",
           "single Opus/Sonnet run" in text and "NO extra" in text, problems)
    for a in AGENTS:
        _check(f"agent listed: {a}", a in text, problems)
    _check("Agent Council JSON block", "```json" in text and '"head_trader"' in text
           and '"overall_verdict"' in text and '"suggested_effect"' in text, problems)
    _check("JSON advisory-only", '"advisory_only"' in text, problems)
    _check("render structure has Agent Council JSON + Table",
           "3A. Agent Council JSON" in text and "3B. Agent Council Table" in text, problems)
    # Slot awareness preserved
    _check("slot awareness present", "SLOT AWARENESS" in text, problems)
    for slot in ("04:30", "11:30", "16:20", "18:30", "21:30", "23:15"):
        _check(f"slot {slot}", slot in text, problems)
    # Status / lifecycle language
    _check("status language section", "STATUS / LIFECYCLE LANGUAGE" in text, problems)
    _check("no raw expired / split instruction",
           "entered-unresolved" in text and "no-entry" in text, problems)
    _check("no bare +0R instruction", "+0R" in text and "CLOSED FLAT 0R" in text, problems)
    for term in ("OPEN actionable", "WAITING for entry", "REVIEW/SHADOW",
                 "ENTERED UNRESOLVED", "NEEDS REVIEW"):
        _check(f"lifecycle term: {term}", term in text, problems)
    # Telegram
    _check("telegram <= 3500 chars rule", "3500" in text, problems)
    _check("telegram Status block", "Status:" in text and "Open actionable:" in text, problems)
    _check("telegram advisory only / no auto-trade", "Advisory only. No auto-trade." in text, problems)


def validate_protocol(text: str, problems: list[str]) -> None:
    print("== repo protocol §17 ==")
    _check("Agent Council Review Mode section", "Agent Council Review Mode" in text, problems)
    _check("permission contract PART 16 still present", "permission contract for SCHEDULED runs" in text, problems)
    for a in AGENTS:
        _check(f"protocol lists agent: {a}", a in text, problems)
    _check("protocol status-language rule",
           "entered-unresolved" in text and "CLOSED FLAT 0R" in text, problems)
    _check("protocol advisory-only", "advisory only" in text.lower(), problems)


def main() -> int:
    problems: list[str] = []
    if not SCHED.exists():
        print(f"WARN: scheduled SKILL not found at {SCHED} — skipping (run on the host where the routine lives).")
    else:
        validate_scheduled(SCHED.read_text(encoding="utf-8"), problems)
    if not PROTOCOL.exists():
        problems.append("protocol file missing")
    else:
        validate_protocol(PROTOCOL.read_text(encoding="utf-8"), problems)
    print()
    if problems:
        print(f"AGENT COUNCIL PROMPT: FAIL ({len(problems)} problems): {problems}")
        return 1
    print("AGENT COUNCIL PROMPT: OK — permission contract preserved + Agent Council structure present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
