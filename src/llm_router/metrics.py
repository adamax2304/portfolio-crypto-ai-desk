from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .config import LLMRouterConfig, load_llm_router_config
from .store import LLMRouterStore


def routing_metrics(
    *, db_path: str | Path, hours: float = 24.0,
    cfg: LLMRouterConfig | None = None,
    include_provider_usage: bool = False,
) -> dict[str, Any]:
    config = cfg or load_llm_router_config()
    store = LLMRouterStore(db_path)
    now = datetime.now(timezone.utc)
    window = timedelta(hours=max(0.1, hours))
    cutoff = (now - window).isoformat()
    baseline_cutoff = (now - max(timedelta(days=7), window * 8)).isoformat()
    with store.connect() as conn:
        rows = [dict(row) for row in conn.execute(
            "SELECT * FROM llm_router_requests WHERE timestamp>=? ORDER BY timestamp",
            (cutoff,),
        ).fetchall()]
        baseline_rows = [dict(row) for row in conn.execute(
            "SELECT selected_tier FROM llm_router_requests "
            "WHERE timestamp>=? AND timestamp<? AND evaluation_only=0",
            (baseline_cutoff, cutoff),
        ).fetchall()]
        attempt_rows = [dict(row) for row in conn.execute(
            "SELECT a.* FROM llm_router_attempts a "
            "LEFT JOIN llm_router_requests r ON r.request_id=a.request_id "
            "WHERE a.timestamp>=? AND COALESCE(r.evaluation_only,0)=0 ORDER BY a.timestamp",
            (cutoff,),
        ).fetchall()]
    production = [row for row in rows if not bool(row.get("evaluation_only"))]
    attempted_request_ids = {str(row.get("request_id") or "") for row in attempt_rows}
    # Requests written before the attempt ledger migration remain visible,
    # but a migrated request is never counted twice.
    billed = list(attempt_rows)
    for row in production:
        if str(row.get("request_id") or "") in attempted_request_ids:
            continue
        if str(row.get("error_type") or "").startswith("llm_daily_budget_exhausted:"):
            continue
        billed.append({
            **row,
            "purpose": "legacy_request_summary",
            "attempt_number": 1,
        })
    total = len(production)
    tiers: dict[str, dict[str, Any]] = {}
    for tier in ("routine", "analyst", "review"):
        selected = [row for row in production if row["selected_tier"] == tier]
        tier_attempts = [row for row in billed if row["selected_tier"] == tier]
        tiers[tier] = {
            "calls": len(selected),
            "share": round(len(selected) / total, 4) if total else 0.0,
            "provider_attempts": len(tier_attempts),
            "cost_usd": round(sum(float(row["cost_usd"] or 0) for row in tier_attempts), 8),
            "avg_latency_ms": round(
                sum(float(row["latency_ms"] or 0) for row in tier_attempts) / len(tier_attempts), 2
            ) if tier_attempts else 0.0,
        }
    grouped: dict[str, dict[str, Any]] = {}
    for field in ("agent", "task_type", "selected_model"):
        bucket: dict[str, dict[str, Any]] = {}
        logical_counts: dict[str, int] = {}
        for row in production:
            key = str(row.get(field) or "unknown")
            logical_counts[key] = logical_counts.get(key, 0) + 1
        for row in billed:
            key = str(row.get(field) or "unknown")
            item = bucket.setdefault(key, {"calls": logical_counts.get(key, 0),
                                           "provider_attempts": 0, "cost_usd": 0.0})
            item["provider_attempts"] += 1
            item["cost_usd"] += float(row.get("cost_usd") or 0.0)
        grouped[field] = {
            key: {**value, "cost_usd": round(value["cost_usd"], 8)}
            for key, value in sorted(bucket.items())
        }
    warnings: list[str] = []
    policy = config.block("policy")
    min_calls = int(policy.get("distribution_warning_min_calls") or 20)
    max_muse = float(policy.get("muse_max_share") or 0.05)
    if total >= min_calls and tiers["review"]["share"] > max_muse:
        warnings.append(
            f"MUSE_SHARE_ABNORMAL:{tiers['review']['share']:.1%}>{max_muse:.1%}"
        )
    shift_pp = float(policy.get("distribution_shift_percentage_points") or 20) / 100.0
    if total >= min_calls and len(baseline_rows) >= min_calls:
        for tier in ("routine", "analyst", "review"):
            baseline_share = sum(row["selected_tier"] == tier for row in baseline_rows) / len(baseline_rows)
            if abs(tiers[tier]["share"] - baseline_share) > shift_pp:
                warnings.append(
                    f"TIER_DISTRIBUTION_SHIFT:{tier}:"
                    f"{baseline_share:.1%}->{tiers[tier]['share']:.1%}"
                )
    total_cost = sum(float(row.get("cost_usd") or 0) for row in billed)
    budget = config.block("budget")
    soft_limit = float(budget.get("total_soft_daily_usd") or 0.0)
    hard_limit = float(budget.get("total_hard_daily_usd") or 0.0)
    local_daily = store.daily_spend(now=now)
    provider_daily: float | None = None
    if include_provider_usage and config.enabled:
        key_name = str(config.raw.get("api_key_env") or "OPENROUTER_API_KEY")
        key = os.getenv(key_name, "").strip()
        if key:
            try:
                from .provider import OpenRouterProvider

                provider_daily = OpenRouterProvider(
                    cfg=config, api_key=key,
                ).daily_usage_usd(cache_seconds=1)
            except Exception:
                provider_daily = None
    effective_daily = max(
        float(local_daily.get("total") or 0.0),
        float(provider_daily) if provider_daily is not None else 0.0,
    )
    if soft_limit > 0 and effective_daily >= soft_limit:
        warnings.append(f"DAILY_LLM_SOFT_BUDGET:{effective_daily:.4f}>={soft_limit:.4f}")
    if hard_limit > 0 and effective_daily >= hard_limit:
        warnings.append(f"DAILY_LLM_HARD_BUDGET:{effective_daily:.4f}>={hard_limit:.4f}")
    return {
        "window_hours": hours,
        "calls": total,
        "calls_by_tier": tiers,
        "cost_by_agent": grouped["agent"],
        "cost_by_task_type": grouped["task_type"],
        "calls_and_cost_by_model": grouped["selected_model"],
        "provider_attempts": len(billed),
        "input_tokens": sum(int(row.get("input_tokens") or 0) for row in billed),
        "output_tokens": sum(int(row.get("output_tokens") or 0) for row in billed),
        "total_cost_usd": round(total_cost, 8),
        "local_utc_day_cost_usd": float(local_daily.get("total") or 0.0),
        "provider_utc_day_cost_usd": (
            round(float(provider_daily), 8) if provider_daily is not None else None
        ),
        "unattributed_utc_day_cost_usd": (
            round(max(0.0, float(provider_daily) - float(local_daily.get("total") or 0.0)), 8)
            if provider_daily is not None else None
        ),
        "average_cost_usd": round(
            total_cost / total, 8
        ) if total else 0.0,
        "average_latency_ms": round(
            sum(float(row.get("latency_ms") or 0) for row in billed) / len(billed), 2
        ) if billed else 0.0,
        "escalation_rate": round(
            sum(bool(row.get("escalation_reason")) for row in production) / total, 4
        ) if total else 0.0,
        "muse_invocation_rate": tiers["review"]["share"],
        "warnings": warnings,
    }


__all__ = ["routing_metrics"]
