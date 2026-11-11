from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any

from src.execution.stop_contract import build_initial_stop_contract, stop_contract_label
from src.execution.paper_execution_accounting import economic_trade_key

from .config import LiveCanaryConfig
from .routing_registry import route as registered_route


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _canonical_hash(value: dict[str, Any]) -> str:
    body = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def _string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            value = [value]
    if not isinstance(value, (list, tuple, set)):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _allowed_preentry_sources(cfg: LiveCanaryConfig) -> set[str]:
    configured = cfg.get("required_preentry_sources")
    if isinstance(configured, (list, tuple, set)):
        return {str(value).strip().lower() for value in configured if str(value).strip()}
    return {str(cfg.get("required_preentry_source", "entry_path")).strip().lower()}


def _allowed_entry_modes(cfg: LiveCanaryConfig, mode: str) -> set[str]:
    by_mode = cfg.get("allowed_entry_modes_by_mode", {}) or {}
    configured = by_mode.get(str(mode).lower())
    if not isinstance(configured, (list, tuple, set)):
        configured = cfg.get("allowed_entry_modes", []) or []
    return {str(value).strip().upper() for value in configured if str(value).strip()}


def _allows_unprofiled_strategy_version(
    cfg: LiveCanaryConfig, *, mode: str, entry_mode: str,
) -> bool:
    by_mode = cfg.get("allow_unprofiled_strategy_versions_by_mode", {}) or {}
    configured = by_mode.get(str(mode).lower())
    if not isinstance(configured, (list, tuple, set)):
        return False
    wanted = str(entry_mode or "").strip().upper()
    return wanted in {str(value).strip().upper() for value in configured if str(value).strip()}


def _has_fresh_point_in_time_entry(payload: dict[str, Any], *, max_age: float) -> bool:
    age = _f(payload.get("entry_age_seconds"))
    return (
        str(payload.get("entry_time_basis") or "") == "point_in_time_current_bar"
        and payload.get("current_price_revalidated") is True
        and age is not None
        and 0 <= age <= max_age
    )


def _symbol_keys(symbol: str) -> set[str]:
    text = str(symbol or "").strip().upper().replace("-", "/")
    keys = {text}
    if "_" in text:
        base, quote = text.rsplit("_", 1)
        keys.add(f"{base}/{quote}")
    if "/" in text:
        base, quote = text.rsplit("/", 1)
        keys.add(f"{base}_{quote}")
    return {item for item in keys if item}


def evaluate_paper_candidate(*, signal: dict[str, Any], payload: dict[str, Any],
                             cfg: LiveCanaryConfig, store: Any,
                             paper_alert_id: str | None = None,
                             now: datetime | None = None) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    asset = str(signal.get("asset_class") or "crypto").lower()
    mode = str(signal.get("mode") or "").lower()
    direction = str(signal.get("direction") or "").lower()
    tier = str(signal.get("tier") or "").upper()
    # The versioned Paper execution profile is the authority at the live
    # boundary. ``cqo_entry_mode`` is a pre-entry hint and may describe the
    # original setup rather than the mode that actually triggered in Paper.
    entry_mode = str(
        payload.get("paper_execution_entry_mode")
        or signal.get("paper_execution_entry_mode")
        or payload.get("cqo_entry_mode")
        or ""
    ).upper()
    symbol = str(signal.get("symbol") or "")
    configured_directions = cfg.get("allowed_directions")
    if not isinstance(configured_directions, (list, tuple, set)):
        configured_directions = [cfg.get("allowed_direction", "long")]
    allowed_directions = {str(value).lower() for value in configured_directions}
    in_scope = (
        asset == str(cfg.get("allowed_asset_class", "crypto")).lower()
        and mode in cfg.allowed_modes()
        and direction in allowed_directions
    )

    reasons: list[str] = []
    if not in_scope:
        # This evaluator is also called for stocks before their dedicated
        # bridge is attempted. Do not run crypto-only live policy checks (and
        # their DB reads) for a candidate that can never be queued here.
        return {"in_scope": False, "reasons": ["OUT_OF_SCOPE"]}
    blocked_symbols = {
        str(value).strip().upper().replace("-", "/")
        for value in (cfg.get("blocked_symbols", []) or [])
        if str(value).strip()
    }
    if _symbol_keys(symbol) & blocked_symbols:
        reasons.append("MEXC_SYMBOL_NOT_TRADABLE")
    if tier not in {str(x).upper() for x in (cfg.get("allowed_tiers", ["A", "B"]) or [])}:
        reasons.append("TIER_NOT_ALLOWED")
    if entry_mode not in _allowed_entry_modes(cfg, mode):
        reasons.append("ENTRY_MODE_NOT_ALLOWED")
    route = registered_route(
        mode=mode,
        entry_mode=entry_mode,
        asset_class=asset,
        path=cfg.get("live_route_registry_path") or None,
    )
    if route is None or route.get("enabled") is not True:
        reasons.append("LIVE_ROUTE_DISABLED")
    paper_action = str(payload.get("cqo_quality_action") or "").upper()
    allowed_paper_actions = {str(value).upper() for value in
                             (cfg.get("allowed_paper_actions", ["FULL_SIZE"]) or [])}
    main_policy_action = str(payload.get("crypto_swing_main_paper_action") or paper_action).upper()
    paper_size_weight = _f(payload.get("size_weight"))
    if paper_action not in allowed_paper_actions:
        reasons.append("PAPER_ACTION_NOT_LIVE_ENABLED")
    # ``crypto_swing_main_paper_action`` is meaningful only for the swing
    # policy. Applying its diagnostic label to intraday/invest candidates made
    # the live funnel report claim a non-existent swing-policy block.
    if mode == "swing" and main_policy_action not in allowed_paper_actions:
        reasons.append("SWING_POLICY_ACTION_NOT_LIVE_ENABLED")
    if paper_size_weight is None or paper_size_weight <= 0:
        reasons.append("PAPER_SIZE_INVALID")
    # Paper is the strategy authority. A route cap can only reduce its size;
    # it cannot make a Paper trade larger in live execution.
    paper_profile = str(
        payload.get("paper_entry_profile")
        or signal.get("paper_entry_profile")
        or ""
    ).strip()
    route_risk_cap = cfg.route_risk_cap(
        mode=mode, entry_mode=entry_mode, paper_profile=paper_profile)
    live_risk_multiplier = min(1.0, paper_size_weight or 0.0, route_risk_cap)
    if str(payload.get("telegram_channel") or "") != "telegram":
        reasons.append("PAPER_NOT_ACTIONABLE")
    if payload.get("paper_entry_dry_run") is True:
        reasons.append("PAPER_DRY_RUN")
    if payload.get("cqo_error") or payload.get("crypto_swing_policy_error"):
        reasons.append("PAPER_OVERLAY_ERROR")
    experiment_id = str(payload.get("crypto_swing_breakout_experiment_id") or "").strip()
    if experiment_id:
        allowed_experiments = {str(value).strip() for value in
                               (cfg.get("allowed_paper_experiments", []) or [])}
        if experiment_id not in allowed_experiments:
            reasons.append("PAPER_EXPERIMENT_NOT_LIVE_ENABLED")
        elif paper_size_weight is None or paper_size_weight > 0.5:
            reasons.append("PAPER_EXPERIMENT_SIZE_INVALID")
    allowed_profiles = cfg.allowed_profiles(mode)
    # Live is version-pinned to a mode-specific Paper profile. A missing or
    # mismatched version is not evidence of compatibility.
    if allowed_profiles:
        if not paper_profile:
            if not _allows_unprofiled_strategy_version(
                cfg, mode=mode, entry_mode=entry_mode,
            ):
                reasons.append("PAPER_STRATEGY_VERSION_MISSING")
        elif paper_profile not in allowed_profiles:
            reasons.append("PAPER_STRATEGY_VERSION_NOT_LIVE_ENABLED")
    if str(payload.get("cqo_preentry_data_quality") or "").lower() != str(
            cfg.get("required_preentry_data_quality", "ok")).lower():
        reasons.append("PREENTRY_DATA_NOT_CLEAN")
    if str(payload.get("cqo_entry_mode_source") or "").lower() not in _allowed_preentry_sources(cfg):
        reasons.append("PREENTRY_NOT_POINT_IN_TIME")
    if payload.get("cqo_snapshot_persisted") is not True:
        reasons.append("OVERLAY_SNAPSHOT_NOT_PERSISTED")

    # Candle high/low only proves that an entry happened somewhere inside a
    # bar. It cannot authorize a real order. Live fan-out requires a price that
    # was revalidated when the tracker made its point-in-time decision.
    if str(payload.get("entry_time_basis") or "") != "point_in_time_current_bar":
        reasons.append("ENTRY_NOT_POINT_IN_TIME")
    if payload.get("current_price_revalidated") is not True:
        reasons.append("CURRENT_PRICE_NOT_REVALIDATED")

    age = _f(payload.get("entry_age_seconds"))
    max_age = cfg.entry_limit("max_entry_age_seconds", entry_mode, 60.0, mode=mode)
    if age is None or age < 0 or age > max_age:
        reasons.append("ENTRY_TOO_OLD")

    entry = _f(payload.get("entry_used"))
    stop = _f(payload.get("stop"))
    tp1, tp2, tp3 = (_f(payload.get("tp1")), _f(payload.get("tp2")), _f(payload.get("tp3")))
    if any(value is None for value in (entry, stop, tp1, tp2, tp3)):
        reasons.append("MISSING_GEOMETRY")
    elif not (
        stop < entry < tp1 < tp2 < tp3 if direction == "long"
        else tp3 < tp2 < tp1 < entry < stop
    ):
        reasons.append("INVALID_DIRECTIONAL_GEOMETRY")

    latency: dict[str, Any]
    try:
        from src.execution.crypto_swing_paper_policy import latency_gate
        with store.connect() as conn:
            latency = latency_gate(conn, str(signal.get("signal_id") or ""), require_row=True)
    except Exception as exc:
        latency = {"clean": False, "cause": "LATENCY_GATE_ERROR", "reason": type(exc).__name__}
    latency_cause = str(latency.get("cause") or "").upper()
    rejected_causes = {str(x).upper() for x in (cfg.get("rejected_latency_causes", []) or [])}
    gap_minutes = _f(latency.get("data_gap_min"))
    # A swing entry can wait for its planned level. LEGITIMATE_LATE is
    # continuous data plus a later price touch, not a data-quality failure.
    # Entry-time price revalidation above remains mandatory for real orders.
    expected_wait = latency_cause in {"LEGITIMATE_LATE", "SESSION_GAP"}
    # The tracker can freeze a current-price entry before the rolling OHLCV
    # cache has a reconstructable bar for the signal. In that narrow case the
    # point-in-time payload is stronger evidence than the diagnostic NO_DATA
    # row. A ``DETECTION_LATENCY`` marker may still be clean: it measures the
    # time the tracker needed to detect a setup, not a missing market-data bar.
    # The live entry is safe only when it is also point-in-time revalidated and
    # inside its short entry-age window, both checked above.
    point_in_time_overrides_missing_latency = (
        latency_cause in {"NO_DATA", "NO_LATENCY_ROW"}
        and _has_fresh_point_in_time_entry(payload, max_age=max_age)
    )
    latency_rejected = (
        not point_in_time_overrides_missing_latency
        and (not latency.get("clean")
        or latency_cause in rejected_causes
        or latency_cause.startswith("DATA_GAP")
        or (not expected_wait and gap_minutes is not None
            and gap_minutes > float(cfg.get("max_data_gap_minutes", 60)))
        )
    )
    if latency_rejected:
        reasons.append("LATENCY_NOT_CLEAN")

    raw_idea = {}
    try:
        raw_idea = json.loads(signal.get("raw_idea_json") or "{}")
        if not isinstance(raw_idea, dict):
            raw_idea = {}
    except Exception:
        raw_idea = {}
    setup = raw_idea.get("raw_setup") or raw_idea.get("setup") or {}
    stop_contract = build_initial_stop_contract(
        symbol=symbol,
        asset_class=asset,
        mode=mode,
        direction=direction,
        entry_price=entry,
        stop_price=stop,
        setup=setup if isinstance(setup, dict) else {},
        payload={**raw_idea, **payload},
        source="live_policy",
    )

    frozen = {
        "signal_id": str(signal.get("signal_id") or ""),
        "paper_alert_id": paper_alert_id,
        "decision_context_type": "point_in_time",
        "captured_at": now.isoformat(),
        "signal_created_at": signal.get("created_at"),
        "entry_triggered_at": payload.get("entry_triggered_at"),
        "entry_bar_open_at": payload.get("entry_bar_open_at"),
        "entry_detected_at": payload.get("entry_detected_at"),
        "entry_time_basis": payload.get("entry_time_basis"),
        "current_price_revalidated": payload.get("current_price_revalidated"),
        "entry_revalidation_reason": payload.get("entry_revalidation_reason"),
        "symbol": symbol,
        "asset_class": asset,
        "mode": mode,
        "direction": direction,
        "tier": tier,
        "score": _f(signal.get("score")),
        "entry_mode": entry_mode,
        "entry_price": entry,
        "original_stop": stop,
        "stop_contract": stop_contract,
        "stop_label": stop_contract_label(stop_contract),
        "tp1": tp1,
        "tp2": tp2,
        "tp3": tp3,
        "entry_age_seconds": age,
        "max_entry_age_seconds": max_age,
        "paper_action": paper_action,
        "paper_size_weight": paper_size_weight,
        "paper_entry_profile": paper_profile,
        "live_route_risk_cap": route_risk_cap,
        "paper_overlay_reasons": _string_list(payload.get("cqo_reasons")),
        "live_risk_multiplier": live_risk_multiplier,
        "preentry_source": payload.get("cqo_entry_mode_source"),
        "preentry_data_quality": payload.get("cqo_preentry_data_quality"),
        "overlay_version": payload.get("cqo_overlay_version"),
        "overlay_config_hash": payload.get("cqo_overlay_config_hash"),
        "latency": latency,
        "latency_missing_override": point_in_time_overrides_missing_latency,
        "strategy_profile": cfg.get("strategy_profile"),
        "strategy_version": paper_profile,
        "protection_model": "early_mfe_protection_v1",
        "live_route_key": (route or {}).get("route_key"),
        "live_route_registry_version": "live_routes_v1",
        "mexc_live_repriced": payload.get("mexc_live_repriced"),
        "mexc_live_reprice_reference_entry": payload.get("mexc_live_reprice_reference_entry"),
        "mexc_live_reprice_current_entry": payload.get("mexc_live_reprice_current_entry"),
        "mexc_live_reprice_adverse_bps": payload.get("mexc_live_reprice_adverse_bps"),
        "mexc_live_reprice_exchange_symbol": payload.get("mexc_live_reprice_exchange_symbol"),
    }
    entry_day = str(
        payload.get("entry_triggered_at") or signal.get("created_at") or now.isoformat()
    )[:10]
    frozen["economic_trade_key"] = str(
        payload.get("economic_trade_key")
        or signal.get("economic_trade_key")
        or economic_trade_key(signal, entry_day)
    )
    eligible = in_scope and not reasons
    decision_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"mexc-canary:{frozen['signal_id']}"))
    return {
        "decision_id": decision_id,
        "signal_id": frozen["signal_id"],
        "captured_at": now.isoformat(),
        "paper_alert_id": paper_alert_id,
        "symbol": frozen["symbol"],
        "mode": mode,
        "entry_mode": entry_mode or None,
        "eligible": 1 if eligible else 0,
        "state": "QUEUED" if eligible else "REJECTED",
        "rejection_reasons_json": json.dumps(reasons),
        "decision_json": json.dumps(frozen, sort_keys=True),
        "decision_hash": _canonical_hash(frozen),
        "config_hash": cfg.config_hash,
        "decision_context_type": "point_in_time",
        "economic_trade_key": frozen["economic_trade_key"],
        "parent_decision_id": None,
        "recovery_sequence": 0,
        "in_scope": in_scope,
        "reasons": reasons,
    }
