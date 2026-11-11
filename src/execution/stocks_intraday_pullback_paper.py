"""Versioned Paper lane for the stock 15m pullback-to-VWAP hold profile."""
from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from src.execution import stocks_intraday_breakout_1bar_paper as shared


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CFG: dict[str, Any] = {
    "enabled": True, "live_enabled": False,
    "profile_id": "stocks_intraday_pullback_vwap_paper_v2",
    "legacy_profile_ids": ["stocks_intraday_pullback_vwap_paper_v1"],
    "source_shadow_profile": "pullback_vwap_hold_15m_v1",
    "strategy_id": "stocks_intraday_pullback_vwap_paper_v2",
    "paper_lane": "paper_stocks_intraday_pullback_vwap",
    "timeframe": "15m", "require_vwap": True, "use_default_universe": True,
    "include_preopen_ab_plans": True, "max_signals_per_symbol_session": 1,
    "max_chase_r": 0.30, "require_directional_body": True,
    "min_full_size_confirmation_rvol": 0.80,
    "max_full_size_atr_extension": 3.50,
    "require_full_size_sector_confirmed": True,
    "weak_size_weight": 0.50, "symbols": [],
}


def load_cfg() -> dict[str, Any]:
    cfg = deepcopy(DEFAULT_CFG)
    path = ROOT / "config" / "paper" / "stocks" / "pullback_limit.yaml"
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        supplied = raw.get("stocks_intraday_pullback_paper") or {}
        if isinstance(supplied, dict):
            cfg.update(supplied)
    except Exception:
        pass
    return cfg


def _raw(signal: dict[str, Any]) -> dict[str, Any]:
    value = signal.get("raw_idea_json")
    if isinstance(value, dict):
        return dict(value)
    try:
        parsed = json.loads(value or "{}")
        return parsed if isinstance(parsed, dict) else {}
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}


def matches_signal(signal: dict[str, Any], cfg: dict[str, Any] | None = None) -> bool:
    cfg = cfg or load_cfg()
    raw = _raw(signal)
    accepted_profiles = {str(cfg.get("profile_id") or "")}
    accepted_profiles.update(str(value) for value in (cfg.get("legacy_profile_ids") or []))
    return bool(
        cfg.get("enabled", True)
        and str(signal.get("asset_class") or "").lower() == "stocks"
        and str(signal.get("mode") or "").lower() == "intraday"
        and str(raw.get("paper_entry_profile") or "") in accepted_profiles
        and raw.get("paper_lane") == cfg.get("paper_lane")
    )


def tag_idea(idea: Any, cfg: dict[str, Any] | None = None) -> Any:
    cfg = cfg or load_cfg()
    raw = deepcopy(getattr(idea, "raw", None) or {})
    raw.update({
        "paper_entry_profile": cfg["profile_id"],
        "paper_lane": cfg["paper_lane"],
        "paper_entry_policy_version": "stocks_pullback_vwap_hold_v2",
        "paper_entry_confirmation": "zone_touch_then_directional_closed_15m_vwap_hold",
        "source_shadow_profile": cfg["source_shadow_profile"],
        "paper_max_chase_r": float(cfg.get("max_chase_r") or 0.30),
    })
    return idea.model_copy(update={"raw": raw})


def select_ideas(ideas: list[Any], cfg: dict[str, Any] | None = None) -> list[Any]:
    cfg = cfg or load_cfg()
    if not cfg.get("new_signals_enabled", True):
        return []
    symbols = set(shared.configured_symbols(cfg))
    selected: list[Any] = []
    for idea in ideas:
        raw = dict(getattr(idea, "raw", None) or {})
        setup = dict(raw.get("setup") or {})
        final_tier = str(getattr(idea, "tier", "")).upper()
        pre_gate = str(raw.get("pre_gate_tier") or final_tier).upper()
        cap_reasons = [str(item) for item in (raw.get("cap_reasons") or [])]
        preopen_ab = bool(
            cfg.get("include_preopen_ab_plans", True)
            and final_tier == "C"
            and pre_gate in {"A", "B"}
            and any(
                "market_closed_intraday_planning_only" in reason
                for reason in cap_reasons
            )
        )
        if str(getattr(idea, "symbol", "")).upper() not in symbols:
            continue
        if str(getattr(idea, "mode", "")).lower() != "intraday":
            continue
        if str(getattr(idea, "direction", "")).lower() not in {"long", "short"}:
            continue
        needed = ("entry_low", "entry_high", "invalidation", "tp1", "tp2", "tp3")
        if any(shared._float(setup.get(key)) is None for key in needed):
            continue
        if final_tier not in {"A", "B"} and not preopen_ab:
            continue
        selected.append(tag_idea(idea, cfg))
    return selected


def register_result(
    *,
    pipeline: Any,
    result: Any,
    cfg: dict[str, Any] | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    return shared.register_result(
        pipeline=pipeline,
        result=result,
        cfg=cfg or load_cfg(),
        now=now,
        selector=select_ideas,
    )


def refresh(*, project_config: Any | None = None, now: datetime | None = None,
            skip_data_update: bool = False, cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = cfg or load_cfg()
    moment = shared._utc(now)
    if not cfg.get("enabled", True) or not cfg.get("new_signals_enabled", True):
        return {"enabled": False, "registered": 0, "selected": 0, "signal_ids": []}
    from src.config import load_config
    from src.stocks.pipelines.stocks_pipeline import StocksPipeline

    project_config = project_config or load_config()
    pipeline = StocksPipeline(project_config)
    result = pipeline.run_report(
        mode="intraday", symbols=shared.configured_symbols(cfg),
        skip_data_update=skip_data_update, shadow_only=True, now=moment,
        apply_intraday_guards=False,
    )
    return register_result(pipeline=pipeline, result=result, cfg=cfg, now=moment)


def resolve_entry(*, signal: dict[str, Any], candles: pd.DataFrame, now: datetime,
                  timeframe_seconds: int, cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = cfg or load_cfg()
    if not matches_signal(signal, cfg):
        return {"applied": False}
    raw = _raw(signal)
    signal_profile = str(raw.get("paper_entry_profile") or cfg["profile_id"])
    calibrated = signal_profile == str(cfg.get("profile_id") or "")
    if int(timeframe_seconds) != 15 * 60:
        return {"applied": True, "ready": False, "profile_id": signal_profile,
                "reason": "15m_confirmation_frame_unavailable"}
    created = pd.to_datetime(signal.get("created_at"), utc=True, errors="coerce")
    if pd.isna(created):
        return {"applied": True, "ready": False, "profile_id": signal_profile,
                "reason": "signal_timestamp_invalid"}
    setup = {
        "entry_low": signal.get("entry_low"), "entry_high": signal.get("entry_high"),
        "invalidation": signal.get("invalidation"), "tp1": signal.get("tp1"),
        "tp2": signal.get("tp2"), "tp3": signal.get("tp3"),
    }
    from src.execution.stocks_intraday_variants_shadow import _profile_entry
    decision_at = created.to_pydatetime()
    try:
        from src.stocks.market_calendar import stock_intraday_target_session
        target_open, _target_close = stock_intraday_target_session(decision_at)
        # In-session signals keep their exact decision clock. After-hours plans
        # begin at the next RTH open instead of being stranded on yesterday.
        decision_at = max(decision_at, target_open)
    except Exception:
        pass
    visible = candles.copy()
    if "timestamp" in visible:
        visible["timestamp"] = pd.to_datetime(visible["timestamp"], utc=True, errors="coerce")
        visible = visible.loc[
            visible["timestamp"] + pd.Timedelta(minutes=15) <= pd.Timestamp(shared._utc(now))
        ].reset_index(drop=True)
    entry, rejection = _profile_entry(
        profile={
            "rule": "pullback_vwap_hold",
            "require_directional_body": bool(
                calibrated and cfg.get("require_directional_body", True)
            ),
        },
        direction=str(signal.get("direction") or "long").lower(), setup=setup,
        bars=visible, decision_at=decision_at, bar_minutes=15,
    )
    if not entry:
        return {"applied": True, "ready": False, "profile_id": signal_profile,
                "entry_mode": "PULLBACK_LIMIT", "reason": str(rejection or "pullback_confirmation_pending")}
    entry_at = str(entry["entry_ts"])
    size_weight = 1.0
    size_reasons: list[str] = []
    if calibrated:
        quality = dict(entry.get("quality") or {})
        confirmation_rvol = shared._float(quality.get("confirmation_rvol"))
        structured = dict(raw.get("structured") or {})
        actionability = dict(raw.get("intraday_actionability") or {})
        atr_extension = shared._float(structured.get("atr_extension"))
        if (confirmation_rvol is None
                or confirmation_rvol < float(cfg.get("min_full_size_confirmation_rvol") or 0.80)):
            size_reasons.append("confirmation_rvol_weak_or_missing")
        if (atr_extension is None
                or atr_extension > float(cfg.get("max_full_size_atr_extension") or 3.50)):
            size_reasons.append("setup_atr_extension_high_or_missing")
        if (cfg.get("require_full_size_sector_confirmed", True)
                and str(actionability.get("sector_confirmation_status") or "").lower() != "confirmed"):
            size_reasons.append("sector_not_confirmed")
        if size_reasons:
            size_weight = max(0.0, min(1.0, float(cfg.get("weak_size_weight") or 0.50)))
    frame = shared._rth(candles)
    later = frame.loc[frame["timestamp"] >= pd.Timestamp(entry_at)].reset_index(drop=True)
    return {
        "applied": True, "ready": True, "profile_id": signal_profile,
        "entry_mode": "PULLBACK_LIMIT",
        "reason": ("zone_touch_then_directional_closed_15m_vwap_hold" if calibrated
                   else "zone_touch_then_closed_15m_vwap_hold"),
        "confirmation_at": entry_at, "entry_price": float(entry["entry"]),
        "entry_trigger": float(entry["entry"]), "max_chase_r": float(cfg.get("max_chase_r") or 0.30),
        "paper_size_weight": size_weight,
        "paper_size_reason": (
            "pullback_v1_legacy_full_size" if not calibrated
            else ("pullback_v2_full_quality" if not size_reasons
                  else "pullback_v2_half_quality: " + ",".join(size_reasons))
        ),
        "candles": later,
    }


__all__ = [
    "load_cfg", "matches_signal", "tag_idea", "select_ideas",
    "register_result", "refresh", "resolve_entry",
]
