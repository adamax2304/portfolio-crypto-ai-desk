"""Human-readable registry for isolated Paper and Shadow strategy lanes.

The registry is navigation and validation only. Existing config files remain
the sole sources of trading parameters, so reorganising the project cannot
silently fork a strategy configuration.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
INDEXES = (
    ROOT / "config" / "paper" / "crypto" / "index.yaml",
    ROOT / "config" / "paper" / "stocks" / "index.yaml",
    ROOT / "config" / "shadow" / "stocks" / "index.yaml",
)


def load_registry() -> dict[str, Any]:
    groups: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    errors: list[str] = []
    for path in INDEXES:
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        scope = "shadow" if "shadow" in path.parts else "paper"
        strategies = payload.get("strategies") or []
        for item in strategies:
            strategy_id = str(item.get("strategy_id") or "").strip()
            key = (scope, strategy_id)
            if not strategy_id:
                errors.append(f"{path.relative_to(ROOT)}: empty strategy_id")
            elif key in seen:
                errors.append(f"duplicate {scope} strategy_id: {strategy_id}")
            seen.add(key)
            config = item.get("config")
            if config and not (ROOT / str(config)).exists():
                errors.append(f"missing config for {strategy_id}: {config}")
        groups.append({"scope": scope, "path": str(path.relative_to(ROOT)), **payload})
    return {"groups": groups, "errors": errors, "valid": not errors}


def render_markdown(registry: dict[str, Any]) -> str:
    lines = ["# Paper and Shadow Strategy Registry", "",
             "This file is navigation only. Referenced configs remain authoritative.", ""]
    for group in registry["groups"]:
        lines += [f"## {group['scope'].title()} / {group.get('asset_class', 'unknown').title()}", "",
                  "| strategy | mode | entry mode | status | config |", "|---|---|---|---|---|"]
        for item in group.get("strategies") or []:
            lines.append(
                f"| {item.get('strategy_id')} | {item.get('mode', '-')} | "
                f"{item.get('entry_mode', '-')} | {item.get('status', group['scope'])} | "
                f"`{item.get('config', '-')}` |"
            )
        lines.append("")
    lines.append(f"Validation: **{'OK' if registry['valid'] else 'FAILED'}**")
    lines.extend(f"- {error}" for error in registry["errors"])
    return "\n".join(lines)


def write_report() -> Path:
    registry = load_registry()
    path = ROOT / "reports" / "PAPER_STRATEGY_REGISTRY.md"
    path.write_text(render_markdown(registry), encoding="utf-8")
    if not registry["valid"]:
        raise ValueError("; ".join(registry["errors"]))
    return path


__all__ = ["load_registry", "render_markdown", "write_report"]
