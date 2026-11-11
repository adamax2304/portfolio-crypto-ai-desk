from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml

from src.config import load_config
from src.data_collectors.crypto_invest_universe import load_selected_symbols
from src.execution.stop_contract import normalize_stop_contract, stop_contract_label

from .config import LiveCanaryConfig, load_live_canary_config
from .routing_registry import route_enabled
from . import store as ls


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "crypto_invest_live.yaml"


def load_crypto_invest_live_config(path: str | Path | None = None) -> dict[str, Any]:
    selected = Path(path) if path else CONFIG_PATH
    payload = yaml.safe_load(selected.read_text(encoding="utf-8")) or {}
    return payload.get("crypto_invest_live") or {}


def _parse(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def _hash(value: Any) -> str:
    return hashlib.sha256(_stable_json(value).encode("utf-8")).hexdigest()


def _float(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _geometry_ok(direction: str, entry: float, stop: float,
                 targets: list[float]) -> bool:
    if len(targets) != 3:
        return False
    if direction == "long":
        return stop < entry < targets[0] < targets[1] < targets[2]
    if direction == "short":
        return targets[2] < targets[1] < targets[0] < entry < stop
    return False


def capture_forward_decisions(
    rows: Iterable[dict[str, Any]], *, db: str | Path | None = None,
    route_cfg: dict[str, Any] | None = None,
    live_cfg: LiveCanaryConfig | None = None,
    universe: Iterable[str] | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Bridge fresh, clean Regime Reclaim decisions into the existing MEXC worker.

    This route deliberately bypasses the ordinary Paper overlay and Paper risk
    guard, but it does not bypass executable-price provenance, MEXC contract and
    spread checks, fixed USD stop risk, three-TP protection, idempotency or the
    account-wide concurrent-risk cap.
    """
    cfg = route_cfg or load_crypto_invest_live_config()
    live = live_cfg or load_live_canary_config()
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    universe_path = Path(str(cfg.get("universe_config") or "config/crypto_invest_universe.yaml"))
    if not universe_path.is_absolute():
        universe_path = ROOT / universe_path
    symbols = {str(value).upper() for value in (
        universe if universe is not None else load_selected_symbols(universe_path)
    )}
    allowed_directions = {str(value).lower() for value in cfg.get("allowed_directions") or []}
    max_age = float(cfg.get("max_capture_age_seconds", 180))
    max_spread = float(cfg.get("max_mexc_spread_bps", 20))
    expected_strategy = str(cfg.get("source_strategy_id") or "")
    expected_profile = str(cfg.get("source_profile_hash") or "")
    counts = {"seen": 0, "queued": 0, "duplicate": 0, "rejected": 0}
    reasons: dict[str, int] = {}

    def rejected(reason: str) -> None:
        counts["rejected"] += 1
        reasons[reason] = reasons.get(reason, 0) + 1

    if not bool(cfg.get("enabled", False)) or (
        route_cfg is None and not route_enabled(mode="invest", entry_mode="REGIME_RECLAIM")
    ):
        return {**counts, "status": "DISABLED", "reasons": reasons}
    if abs(float(cfg.get("fixed_risk_usdt", 10.0)) - live.risk_per_trade_usdt) > 1e-9:
        return {**counts, "status": "RISK_CONFIG_MISMATCH", "reasons": reasons}
    if not live.live_armed():
        return {**counts, "status": "LIVE_NOT_ARMED", "reasons": reasons}

    path = Path(db) if db else load_config().db_path
    for raw in rows:
        row = dict(raw)
        counts["seen"] += 1
        if str(row.get("strategy_id") or "") != expected_strategy:
            rejected("STRATEGY_ID_MISMATCH")
            continue
        if expected_profile and str(row.get("profile_hash") or "") != expected_profile:
            rejected("PROFILE_HASH_MISMATCH")
            continue
        if str(row.get("status") or "") != "ELIGIBLE_FORWARD_ENTRY" or int(row.get("is_clean") or 0) != 1:
            rejected("NOT_CLEAN_ELIGIBLE")
            continue
        symbol = str(row.get("symbol") or "").upper()
        direction = str(row.get("direction") or "").lower()
        if symbol not in symbols:
            rejected("SYMBOL_NOT_IN_REVIEWED_UNIVERSE")
            continue
        if direction not in allowed_directions:
            rejected("DIRECTION_NOT_ALLOWED")
            continue
        observed_at = _parse(row.get("observed_at"))
        if observed_at is None:
            rejected("OBSERVED_AT_MISSING")
            continue
        age = (now - observed_at).total_seconds()
        if age < 0 or age > max_age:
            rejected("CAPTURE_TOO_OLD")
            continue
        entry = _float(row.get("entry_price"))
        stop = _float(row.get("stop_price"))
        try:
            targets = [float(value) for value in json.loads(row.get("targets_json") or "[]")]
            features = json.loads(row.get("features_json") or "{}")
        except (TypeError, ValueError, json.JSONDecodeError):
            rejected("INVALID_JSON")
            continue
        quote = features.get("mexc_quote") or {}
        spread = _float(quote.get("spread_bps"))
        if quote.get("status") != "ok" or spread is None or spread > max_spread:
            rejected("MEXC_QUOTE_NOT_EXECUTABLE")
            continue
        if entry is None or stop is None or not _geometry_ok(direction, entry, stop, targets):
            rejected("INVALID_GEOMETRY")
            continue

        source_decision_id = str(row.get("decision_id") or "")
        signal_id = f"crypto_invest:{source_decision_id}"
        decision_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"mexc-live:{signal_id}"))
        stop_contract = normalize_stop_contract(
            {
                "stop_source": "regime_reclaim_rebased_unit_pct",
                "stop_model": "invest_regime_reclaim_unit_pct_v1",
                "structure_timeframe": str(features.get("timeframe") or features.get("structure_timeframe") or "4h"),
                "structure_level": _float(features.get("reference_level") or features.get("pullback_level")),
                "structure_level_kind": str(features.get("reference_level_kind") or "regime_reclaim"),
                "raw_stop_price": stop,
                "fallback_used": False,
                "confidence": "medium",
                "warnings": ["stop is rebased from invest forward decision; verify with structural candidate in audit"],
            },
            symbol=symbol,
            asset_class="crypto",
            mode=str(cfg.get("mode", "invest")),
            direction=direction,
            entry_price=entry,
            stop_price=stop,
        )
        frozen = {
            "signal_id": signal_id,
            "source_decision_id": source_decision_id,
            "decision_context_type": "point_in_time_crypto_invest",
            "captured_at": now.isoformat(),
            "signal_created_at": row.get("formed_at"),
            "entry_triggered_at": row.get("decision_at"),
            "entry_bar_open_at": row.get("decision_at"),
            "entry_detected_at": row.get("observed_at"),
            "entry_time_basis": "point_in_time_current_bar",
            "current_price_revalidated": True,
            "entry_revalidation_reason": "forward_mexc_quote_snapshot",
            "symbol": symbol,
            "asset_class": "crypto",
            "mode": str(cfg.get("mode", "invest")),
            "direction": direction,
            "tier": "OPERATOR_LIVE",
            "entry_mode": str(cfg.get("entry_mode", "REGIME_RECLAIM")).upper(),
            "entry_price": entry,
            "original_stop": stop,
            "stop_contract": stop_contract,
            "stop_label": stop_contract_label(stop_contract),
            "tp1": targets[0], "tp2": targets[1], "tp3": targets[2],
            "entry_age_seconds": max(0.0, float(row.get("latency_seconds") or 0.0)),
            "paper_action": "NOT_APPLICABLE_INDEPENDENT_ROUTE",
            "paper_size_weight": 1.0,
            "live_route_risk_cap": 1.0,
            "live_risk_multiplier": float(cfg.get("risk_multiplier", 1.0)),
            "preentry_source": "regime_conditioned_forward_point_in_time",
            "preentry_data_quality": "ok",
            "strategy_profile": str(cfg.get("route_id") or ""),
            "strategy_version": str(cfg.get("live_strategy_version") or ""),
            "source_strategy_id": expected_strategy,
            "source_profile_hash": expected_profile,
            "risk_bucket": str(cfg.get("risk_bucket") or "crypto_invest"),
            "evidence_status": str(cfg.get("evidence_status") or ""),
            "protection_model": "early_mfe_protection_v1",
        }
        record = {
            "decision_id": decision_id, "signal_id": signal_id,
            "captured_at": now.isoformat(), "paper_alert_id": None,
            "symbol": symbol, "mode": frozen["mode"],
            "entry_mode": frozen["entry_mode"], "eligible": 1, "state": "QUEUED",
            "rejection_reasons_json": "[]", "decision_json": _stable_json(frozen),
            "decision_hash": _hash(frozen), "config_hash": live.config_hash,
            "decision_context_type": "point_in_time_crypto_invest",
        }
        with ls.connect(path) as conn:
            result = ls.insert_decision(conn, record, queue=True)
        if result["queued"]:
            counts["queued"] += 1
        else:
            counts["duplicate"] += 1
    risk_multiplier = float(cfg.get("risk_multiplier", 1.0))
    return {**counts, "status": "OK", "reasons": reasons,
            "route_id": cfg.get("route_id"),
            "risk_usdt": live.risk_per_trade_usdt * risk_multiplier,
            "base_risk_usdt": live.risk_per_trade_usdt}
