"""Thesis / Invalidation Formatter (Shadow Intelligence PART 4).

Deterministic, template-based explanation block from already-computed fields.
NO LLM / network in the alert path. Diagnostic only — never changes the signal,
SL line, routing, score, or size. Fail-open.
"""
from __future__ import annotations

from typing import Any

_MAX_COMPACT = 240


def _fmt(v):
    return "?" if v is None else (f"{v:g}" if isinstance(v, (int, float)) else str(v))


def format_thesis(signal: dict[str, Any], *, catalyst: dict[str, Any] | None = None,
                  derivatives: dict[str, Any] | None = None,
                  squeeze: dict[str, Any] | None = None,
                  onchain: dict[str, Any] | None = None,
                  timeline: dict[str, Any] | None = None,
                  advisor: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build the thesis fields. Pure + deterministic. Fail-open to unknowns."""
    try:
        catalyst = catalyst or {}
        derivatives = derivatives or {}
        squeeze = squeeze or {}
        onchain = onchain or {}
        timeline = timeline or {}
        advisor = advisor or {}

        direction = str(signal.get("direction") or "long")
        setup = signal.get("setup_type") or signal.get("playbook") or "momentum/structure"
        entry_low, entry_high = signal.get("entry_low"), signal.get("entry_high")
        stop = signal.get("stop_loss") or signal.get("invalidation")
        tps = [signal.get("tp1"), signal.get("tp2"), signal.get("tp3")]

        # why-now reasons (max 2)
        reasons = []
        if catalyst.get("catalyst_integrity_status") == "catalyst_backed_confirmed":
            reasons.append("catalyst-backed (direct news hit)")
        p24 = derivatives.get("price_24h_change_pct")
        if p24 is not None and abs(p24) >= 5:
            reasons.append(f"{'+' if p24 >= 0 else ''}{p24:g}% 24h move")
        if squeeze.get("squeeze_phase") and squeeze["squeeze_phase"] != "phase_0_unknown":
            reasons.append(squeeze["squeeze_phase"].replace("phase_", "").replace("_", " "))
        if not reasons:
            reasons.append(f"{setup} setup")

        # risks against (top)
        risks = []
        if squeeze.get("no_chase_warning"):
            risks.append("distribution near high — do not chase")
        if derivatives.get("derivatives_warning"):
            risks.append(derivatives["derivatives_warning"])
        if onchain.get("onchain_risk_status") in ("high", "elevated"):
            risks.append("on-chain risk elevated")
        if catalyst.get("catalyst_integrity_status") == "no_direct_news_catalyst":
            risks.append("no confirmed catalyst")
        top_risk = risks[0] if risks else "standard market/execution risk"

        invalidation = (f"close beyond {_fmt(stop)}" if stop is not None
                        else "structure break (no stop level)")
        entry_zone = (f"{_fmt(entry_low)}–{_fmt(entry_high)}" if entry_low is not None
                      else _fmt(signal.get("entry_trigger") or signal.get("suggested_entry")))
        targets = " / ".join(_fmt(t) for t in tps if t is not None) or "see report"

        no_chase_zone = None
        if squeeze.get("no_chase_warning"):
            no_chase_zone = "near local high — wait for pullback"

        # data confidence
        confs = [c for c in (derivatives.get("derivatives_data_confidence"),
                             squeeze.get("squeeze_phase_confidence"),
                             timeline.get("timeline_confidence")) if c and c != "unknown"]
        data_conf = ("high" if "high" in confs else "medium" if confs else "low")
        missing = [k for k, v in (("derivatives", derivatives.get("derivatives_data_confidence")),
                                   ("onchain", onchain.get("onchain_risk_status")))
                   if v in (None, "unknown", "unavailable")]

        compact = (f"Thesis: {setup} {direction} because {', '.join(reasons[:2])}. "
                   f"Invalid if {invalidation}. Risk: {top_risk}.")
        if len(compact) > _MAX_COMPACT:
            compact = compact[:_MAX_COMPACT - 1] + "…"

        return {
            "thesis_setup_type": setup,
            "thesis_why_now": "; ".join(reasons[:2]),
            "thesis_entry_zone": entry_zone,
            "thesis_invalidation": invalidation,
            "thesis_targets": targets,
            "thesis_risks_against": "; ".join(risks[:3]) or top_risk,
            "thesis_do_not_chase_zone": no_chase_zone,
            "thesis_data_confidence": data_conf,
            "thesis_missing_data": missing,
            "thesis_summary_compact": compact,
            "diagnostic_only": True,
        }
    except Exception:
        return {
            "thesis_setup_type": signal.get("setup_type"),
            "thesis_summary_compact": None, "thesis_invalidation": None,
            "thesis_data_confidence": "unknown", "thesis_missing_data": ["formatter_error"],
            "diagnostic_only": True,
        }


def thesis_report_block(fields: dict[str, Any]) -> str:
    """Full multi-line report block (for reports / Control Plane, not Telegram)."""
    return "\n".join([
        f"WHY NOW: {fields.get('thesis_why_now') or '?'}",
        f"INVALIDATION: {fields.get('thesis_invalidation') or '?'}",
        f"ENTRY: {fields.get('thesis_entry_zone') or '?'}",
        f"TARGETS: {fields.get('thesis_targets') or '?'}",
        f"RISKS AGAINST: {fields.get('thesis_risks_against') or '?'}",
        f"DATA CONFIDENCE: {fields.get('thesis_data_confidence') or '?'}",
        f"MISSING DATA: {', '.join(fields.get('thesis_missing_data') or []) or 'none'}",
    ])
