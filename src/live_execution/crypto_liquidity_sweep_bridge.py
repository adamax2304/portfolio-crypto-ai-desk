"""Bridge fresh, clean liquidity-sweep reversals into the common live outbox.

The sweep detector remains isolated from Paper and order code. This module is
the only handoff point: it validates versioned source provenance, enforces a
short point-in-time window and then relies on the ordinary MEXC/Bybit preflight
for current price, contract, margin, stop and three-TP verification.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml

from src.config import load_config
from src.execution.stop_contract import normalize_stop_contract, stop_contract_label
from src.execution.strategy_governance import runtime_route_gate

from . import store as ls
from .config import LiveCanaryConfig, load_live_canary_config
from .routing_registry import route_enabled


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "crypto_liquidity_sweep_live.yaml"


def load_liquidity_sweep_live_config(path: str | Path | None = None) -> dict[str, Any]:
    selected = Path(path) if path else CONFIG_PATH
    payload = yaml.safe_load(selected.read_text(encoding="utf-8")) or {}
    block = payload.get("crypto_liquidity_sweep_live") or {}
    return block if isinstance(block, dict) else {}


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


def _float(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def _hash(value: Any) -> str:
    return hashlib.sha256(_stable_json(value).encode("utf-8")).hexdigest()


def _json_obj(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if isinstance(value, str) and value.strip():
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return {}
        return parsed if isinstance(parsed, dict) else {}
    return {}


def _normalized_regime(value: Any) -> str:
    text = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "risk_off": "risk_off",
        "riskoff": "risk_off",
        "btc_risk_off": "btc_risk_off",
        "bear": "bearish",
        "bearish": "bearish",
        "bearish_market": "bearish",
        "bearish_trend": "bearish_trend",
        "down": "downtrend",
        "down_trend": "downtrend",
        "downtrend": "downtrend",
        "short": "short",
        "short_bias": "short_bias",
        "risk_on": "risk_on",
        "riskon": "risk_on",
        "bullish": "bullish",
        "bullish_trend": "bullish",
        "uptrend": "uptrend",
        "up_trend": "uptrend",
    }
    return aliases.get(text, text or "unknown")


def _latest_market_context(db: Path) -> dict[str, Any]:
    """Return the newest dashboard regime hints without requiring the table."""
    try:
        conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        try:
            row = conn.execute(
                "SELECT crypto_market_mode,crypto_regime,raw_json "
                "FROM market_dashboard_snapshots ORDER BY id DESC LIMIT 1"
            ).fetchone()
        finally:
            conn.close()
    except sqlite3.Error:
        return {}
    if row is None:
        return {}
    out = {
        "crypto_market_mode": row["crypto_market_mode"],
        "crypto_regime": row["crypto_regime"],
    }
    raw = _json_obj(row["raw_json"])
    for key in ("crypto_market_mode", "crypto_regime", "market_regime", "bias"):
        if raw.get(key) not in (None, ""):
            out[key] = raw.get(key)
    return out


def _regime_labels(row: dict[str, Any], market: dict[str, Any]) -> list[tuple[str, str]]:
    labels: list[tuple[str, str]] = []
    for key in (
        "market_regime", "crypto_market_mode", "crypto_regime",
        "btc_regime_state", "market_bias", "bias",
    ):
        if row.get(key) not in (None, ""):
            labels.append((f"row.{key}", str(row.get(key))))
    for container_name in ("features_json", "notes_json"):
        container = _json_obj(row.get(container_name))
        for key in (
            "market_regime", "crypto_market_mode", "crypto_regime",
            "btc_regime_state", "market_bias", "bias",
        ):
            if container.get(key) not in (None, ""):
                labels.append((f"{container_name}.{key}", str(container.get(key))))
    for key in ("crypto_market_mode", "crypto_regime", "market_regime", "bias"):
        if market.get(key) not in (None, ""):
            labels.append((f"dashboard.{key}", str(market.get(key))))
    return labels


def _market_regime_guard(
    row: dict[str, Any], market: dict[str, Any], cfg: dict[str, Any],
) -> dict[str, Any]:
    block = cfg.get("market_regime_filter") or {}
    if not bool(block.get("enabled", False)):
        return {"ok": True, "source": "disabled", "regime": "unchecked"}
    labels = _regime_labels(row, market)
    blocked = {
        _normalized_regime(value)
        for value in (block.get("blocked_regimes") or [])
        if str(value or "").strip()
    }
    keywords = [
        _normalized_regime(value)
        for value in (block.get("blocked_keywords") or [])
        if str(value or "").strip()
    ]
    checked: list[dict[str, str]] = []
    for source, raw in labels:
        normalized = _normalized_regime(raw)
        checked.append({"source": source, "raw": str(raw), "normalized": normalized})
        if normalized in blocked or any(keyword and keyword in normalized for keyword in keywords):
            return {
                "ok": False,
                "reason": "MARKET_REGIME_BLOCKED",
                "source": source,
                "regime": normalized,
                "raw_regime": str(raw),
                "checked": checked,
            }
    if not labels and bool(block.get("block_unknown", False)):
        return {
            "ok": False,
            "reason": "MARKET_REGIME_UNKNOWN",
            "source": "none",
            "regime": "unknown",
            "checked": checked,
        }
    primary = checked[0] if checked else {"source": "none", "normalized": "unknown", "raw": "unknown"}
    return {
        "ok": True,
        "source": primary["source"],
        "regime": primary["normalized"],
        "raw_regime": primary["raw"],
        "checked": checked,
    }


def _geometry_ok(direction: str, entry: float, stop: float, targets: tuple[float, float, float]) -> bool:
    tp1, tp2, tp3 = targets
    if direction == "long":
        return stop < entry < tp1 < tp2 < tp3
    if direction == "short":
        return tp3 < tp2 < tp1 < entry < stop
    return False


def capture_forward_sweeps(
    rows: Iterable[dict[str, Any]], *, db: str | Path | None = None,
    route_cfg: dict[str, Any] | None = None,
    live_cfg: LiveCanaryConfig | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Queue one immutable live decision for each fresh, clean sweep row.

    This does not place an order. The existing worker later chooses MEXC or
    Bybit, repeats all current-price preflight checks, and submits exactly one
    order only when an eligible venue is armed.
    """
    cfg = route_cfg or load_liquidity_sweep_live_config()
    live = live_cfg or load_live_canary_config()
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    counts = {"seen": 0, "queued": 0, "duplicate": 0, "rejected": 0}
    reasons: dict[str, int] = {}

    def reject(reason: str) -> None:
        counts["rejected"] += 1
        reasons[reason] = reasons.get(reason, 0) + 1

    if not bool(cfg.get("enabled", False)) or (
        route_cfg is None and not route_enabled(
            mode="liquidity_sweep", entry_mode="LIQUIDITY_SWEEP"
        )
    ):
        return {**counts, "status": "DISABLED", "reasons": reasons}
    if abs(float(cfg.get("fixed_risk_usdt", 10.0)) - live.risk_per_trade_usdt) > 1e-9:
        return {**counts, "status": "RISK_CONFIG_MISMATCH", "reasons": reasons}
    # This collector intentionally does not receive exchange credentials. It
    # may freeze a fresh decision only while the route is configured live; the
    # credential-bearing MEXC worker remains the sole component that can submit
    # it and independently verifies the venue arm at preflight.
    if not (live.capture_enabled and live.submission_enabled and live.execution_mode == "live"):
        return {**counts, "status": "LIVE_ROUTE_DISABLED", "reasons": reasons}

    path = Path(db) if db else load_config().db_path
    # Materialize the common live ledger before the read-only governance check.
    # Fresh test/new installations legitimately have zero positions; absence
    # of the tables must not be confused with an unhealthy execution ledger.
    with ls.connect(path) as bootstrap_conn:
        ls.ensure_tables(bootstrap_conn)
    governance = runtime_route_gate(
        "crypto_liquidity_sweep_v1", db=path, now=now,
    )
    if not governance.get("allowed"):
        return {
            **counts,
            "status": str(governance.get("verdict") or "GOVERNANCE_BLOCKED"),
            "reasons": {
                str(reason): 1 for reason in (
                    governance.get("reasons") or ["GOVERNANCE_BLOCKED"]
                )
            },
            "governance": governance,
        }
    expected_strategy = str(cfg.get("source_strategy_id") or "")
    expected_profile = str(cfg.get("source_profile_id") or "")
    expected_lane = str(cfg.get("source_shadow_lane") or "")
    expected_data = str(cfg.get("required_data_status") or "ok").lower()
    allowed_directions = {str(value).lower() for value in (cfg.get("allowed_directions") or [])}
    max_age = float(cfg.get("max_capture_age_seconds", 90.0))
    market_context = _latest_market_context(path)

    for raw in rows:
        row = dict(raw)
        counts["seen"] += 1
        if str(row.get("strategy_id") or "") != expected_strategy:
            reject("STRATEGY_ID_MISMATCH")
            continue
        if expected_profile and str(row.get("profile_id") or "") != expected_profile:
            reject("PROFILE_ID_MISMATCH")
            continue
        if expected_lane and str(row.get("shadow_lane") or "") != expected_lane:
            reject("SOURCE_LANE_MISMATCH")
            continue
        if str(row.get("eligibility_status") or "") != "eligible" or int(row.get("is_clean_for_edge") or 0) != 1:
            reject("NOT_CLEAN_ELIGIBLE")
            continue
        if str(row.get("data_status") or "").lower() != expected_data:
            reject("DATA_STATUS_NOT_CLEAN")
            continue
        direction = str(row.get("direction") or "").lower()
        if direction not in allowed_directions:
            reject("DIRECTION_NOT_ALLOWED")
            continue
        regime_guard = _market_regime_guard(row, market_context, cfg)
        if regime_guard.get("ok") is not True:
            reject(str(regime_guard.get("reason") or "MARKET_REGIME_BLOCKED"))
            continue
        decision_at = _parse(row.get("decision_at"))
        if decision_at is None:
            reject("DECISION_AT_MISSING")
            continue
        age = (now - decision_at).total_seconds()
        if age < 0 or age > max_age:
            reject("CAPTURE_TOO_OLD")
            continue
        symbol = str(row.get("symbol") or "").upper()
        entry, stop = _float(row.get("entry_price")), _float(row.get("stop_price"))
        targets = (_float(row.get("tp1")), _float(row.get("tp2")), _float(row.get("tp3")))
        if not symbol or entry is None or stop is None or any(value is None for value in targets):
            reject("MISSING_GEOMETRY")
            continue
        tp1, tp2, tp3 = (float(value) for value in targets)
        if not _geometry_ok(direction, entry, stop, (tp1, tp2, tp3)):
            reject("INVALID_GEOMETRY")
            continue

        candidate_id = str(row.get("candidate_id") or "")
        if not candidate_id:
            reject("CANDIDATE_ID_MISSING")
            continue
        signal_id = f"crypto_liquidity_sweep:{candidate_id}"
        decision_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"mexc-live:{signal_id}"))
        structure_level = _float(row.get("level") or row.get("sweep_price"))
        stop_contract = normalize_stop_contract(
            {
                "stop_source": "liquidity_sweep_extreme",
                "stop_model": "sweep_extreme_atr_buffer_v1",
                "structure_timeframe": str(row.get("timeframe") or "5m"),
                "structure_level": structure_level,
                "structure_level_kind": "sweep_low" if direction == "long" else "sweep_high",
                "atr": _float(row.get("atr") or row.get("atr14")),
                "buffer_atr": _float(cfg.get("stop_buffer_atr")),
                "raw_stop_price": stop,
                "fallback_used": False,
                "confidence": "medium",
            },
            symbol=symbol,
            asset_class="crypto",
            mode=str(cfg.get("mode") or "liquidity_sweep"),
            direction=direction,
            entry_price=entry,
            stop_price=stop,
        )
        frozen = {
            "signal_id": signal_id,
            "source_candidate_id": candidate_id,
            "decision_context_type": "point_in_time_liquidity_sweep",
            "captured_at": now.isoformat(),
            "signal_created_at": row.get("generated_at"),
            "entry_triggered_at": row.get("decision_at"),
            "entry_bar_open_at": row.get("sweep_at"),
            "entry_detected_at": row.get("decision_at"),
            "entry_time_basis": "point_in_time_current_bar",
            "current_price_revalidated": True,
            "entry_revalidation_reason": "closed_5m_liquidity_sweep_snapshot",
            "symbol": symbol,
            "asset_class": "crypto",
            "mode": str(cfg.get("mode") or "liquidity_sweep"),
            "direction": direction,
            "tier": "OPERATOR_LIVE",
            "entry_mode": str(cfg.get("entry_mode") or "LIQUIDITY_SWEEP").upper(),
            "entry_price": entry,
            "original_stop": stop,
            "stop_contract": stop_contract,
            "stop_label": stop_contract_label(stop_contract),
            "tp1": tp1,
            "tp2": tp2,
            "tp3": tp3,
            "entry_age_seconds": max(0.0, age),
            "market_regime": regime_guard.get("regime"),
            "market_regime_source": regime_guard.get("source"),
            "market_regime_guard": regime_guard,
            "paper_action": "NOT_APPLICABLE_VERSIONED_LIQUIDITY_SWEEP_ROUTE",
            "paper_size_weight": 1.0,
            "live_route_risk_cap": 1.0,
            "live_risk_multiplier": float(cfg.get("risk_multiplier", 1.0)),
            "preentry_source": "observed_liquidation_closed_5m_sweep",
            "preentry_data_quality": "ok",
            "strategy_profile": str(cfg.get("route_id") or ""),
            "strategy_version": str(cfg.get("live_strategy_version") or ""),
            "source_strategy_id": expected_strategy,
            "source_profile_id": expected_profile,
            "source_shadow_lane": expected_lane,
            "risk_bucket": str(cfg.get("risk_bucket") or "crypto_liquidity_sweep"),
            "protection_model": "early_mfe_protection_v1",
            "evidence_cohort": "strategy_governance_v1_post_2026_09_28",
            "paper_exit_parity_required": "live_exit_parity_v3_incremental",
        }
        record = {
            "decision_id": decision_id,
            "signal_id": signal_id,
            "captured_at": now.isoformat(),
            "paper_alert_id": None,
            "symbol": symbol,
            "mode": frozen["mode"],
            "entry_mode": frozen["entry_mode"],
            "eligible": 1,
            "state": "QUEUED",
            "rejection_reasons_json": "[]",
            "decision_json": _stable_json(frozen),
            "decision_hash": _hash(frozen),
            "config_hash": live.config_hash,
            "decision_context_type": "point_in_time_liquidity_sweep",
        }
        with ls.connect(path) as conn:
            result = ls.insert_decision(conn, record, queue=True)
            if result["queued"]:
                ls.event(conn, "LIQUIDITY_SWEEP_LIVE_CAPTURED", decision_id=decision_id, payload={
                    "candidate_id": candidate_id,
                    "source_profile_id": expected_profile,
                    "entry_age_seconds": round(max(0.0, age), 3),
                })
                conn.commit()
        if result["queued"]:
            counts["queued"] += 1
        else:
            counts["duplicate"] += 1
    risk_multiplier = float(cfg.get("risk_multiplier", 1.0))
    return {**counts, "status": "OK", "reasons": reasons, "route_id": cfg.get("route_id"),
            "risk_usdt": live.risk_per_trade_usdt * risk_multiplier,
            "base_risk_usdt": live.risk_per_trade_usdt}


__all__ = ["capture_forward_sweeps", "load_liquidity_sweep_live_config"]
