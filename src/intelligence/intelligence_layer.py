"""Intelligence Aggregator (Shadow Intelligence PART 6).

Unifies the 5 shadow modules into one compact field bundle for the alert payload /
Telegram / Control Plane / reports. ALERT-PATH SAFE: reads only pre-computed local
caches + a tiny timeline query + a pure deterministic thesis. NO external API, NO
LLM, NO compute of heavy trajectories here. Fails open per submodule and respects a
time budget (returns partial + `timeout_partial` if exceeded). Never mutates the
signal/routing/score/TP-SL/size; `diagnostic_only=True`.
"""
from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Any

DEFAULT_BUDGET_MS = 300


def assemble_intelligence_fields(
    signal: dict[str, Any], *, store=None, file_store=None,
    now: datetime | None = None, prior_fields: dict[str, Any] | None = None,
    time_budget_ms: int = DEFAULT_BUDGET_MS,
) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    prior = prior_fields or {}
    symbol = signal.get("symbol") or ""
    t0 = time.monotonic()
    fields: dict[str, Any] = {"diagnostic_only": True}
    cache_lookups = 0
    cache_hits = 0
    status = "ok"

    def over_budget() -> bool:
        return (time.monotonic() - t0) * 1000.0 > time_budget_ms

    # 1) timeline (tiny RO query)
    try:
        from src.intelligence.symbol_timeline import compact_timeline_for_payload
        fields.update(compact_timeline_for_payload(symbol, now=now))
    except Exception:
        pass

    deriv_full = {}
    squeeze_full = {}
    onchain_full = {}

    # 2) derivatives (cache read)
    if not over_budget():
        try:
            from src.intelligence.derivatives_trajectory import derivatives_trajectory_for_payload
            from src.intelligence import store as _st
            cache_lookups += 1
            raw = _st.read_cache("deriv_cache", symbol.split("/")[0].upper())
            cache_hits += 1 if raw else 0
            deriv_full = raw or {}
            fields.update(derivatives_trajectory_for_payload(symbol))
        except Exception:
            pass
    else:
        status = "timeout_partial"

    # 3) squeeze phase (cache read)
    if not over_budget():
        try:
            from src.intelligence.squeeze_phase import squeeze_phase_for_payload
            from src.intelligence import store as _st
            cache_lookups += 1
            raw = _st.read_cache("phase_cache", symbol.split("/")[0].upper())
            cache_hits += 1 if raw else 0
            squeeze_full = raw or {}
            fields.update(squeeze_phase_for_payload(symbol))
        except Exception:
            pass
    else:
        status = "timeout_partial"

    # 4) onchain (cache read)
    if not over_budget():
        try:
            from src.intelligence.onchain_risk import onchain_risk_for_payload
            from src.intelligence import store as _st
            cache_lookups += 1
            raw = _st.read_cache("onchain_cache", symbol.split("/")[0].upper())
            cache_hits += 1 if raw else 0
            onchain_full = raw or {}
            fields.update(onchain_risk_for_payload(symbol))
        except Exception:
            pass
    else:
        status = "timeout_partial"

    # 5) thesis (pure / deterministic — always run, it's cheap)
    try:
        from src.intelligence.thesis_formatter import format_thesis
        catalyst = {"catalyst_integrity_status": prior.get("catalyst_integrity_status")}
        advisor = {"position_advisor_status": prior.get("position_advisor_status")}
        fields.update(format_thesis(
            signal, catalyst=catalyst, derivatives=deriv_full or fields,
            squeeze=squeeze_full or fields, onchain=onchain_full or fields,
            timeline={"timeline_confidence": fields.get("timeline_confidence")},
            advisor=advisor))
    except Exception:
        pass

    runtime_ms = round((time.monotonic() - t0) * 1000.0, 1)
    fresh = [fields.get("timeline_data_freshness_sec"),
             fields.get("derivatives_data_freshness_sec")]
    fresh = [f for f in fresh if isinstance(f, (int, float))]
    fields["intelligence_layer_status"] = status if status != "ok" else (
        "ok" if cache_hits else "partial_no_cache")
    fields["intelligence_runtime_ms"] = runtime_ms
    fields["intelligence_cache_hit_ratio"] = (
        round(cache_hits / cache_lookups, 2) if cache_lookups else None)
    fields["intelligence_data_freshness_sec"] = max(fresh) if fresh else None
    fields["diagnostic_only"] = True
    return fields


def intelligence_telegram_lines(fields: dict[str, Any]) -> list[str]:
    """At most 3 compact lines. Diagnostic only; never replaces the SL line."""
    lines: list[str] = []
    phase = fields.get("squeeze_phase")
    conf = fields.get("squeeze_phase_confidence")
    if phase and phase not in ("phase_0_unknown", None) and conf in ("medium", "high"):
        extra = []
        if fields.get("funding_turning_down"):
            extra.append("funding turning down")
        if fields.get("oi_stall_detected"):
            extra.append("OI stalled")
        tail = (" — " + ", ".join(extra)) if extra else ""
        warn = " · DO NOT CHASE" if fields.get("no_chase_warning") else ""
        lines.append(f"🧠 Phase: {phase.replace('phase_', '').replace('_', ' ')}{tail}{warn} — diagnostic only")
    if fields.get("thesis_summary_compact"):
        lines.append(f"🧠 {fields['thesis_summary_compact']}")
    if fields.get("onchain_risk_status") == "high":
        suffix = "paper safety guard" if fields.get("paper_guard_eligible") else "diagnostic only"
        lines.append(f"🧠 On-chain risk HIGH (score {fields.get('onchain_risk_score')}) — {suffix}")
    return lines[:3]
