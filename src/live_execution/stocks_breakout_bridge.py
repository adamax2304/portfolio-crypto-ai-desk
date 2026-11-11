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
from src.execution.stop_contract import (
    build_initial_stop_contract,
    is_structural_stop_contract,
    stop_contract_label,
)

from .config import LiveCanaryConfig, load_live_canary_config
from .routing_registry import route_enabled
from . import store as ls


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "stocks" / "mexc_stock_futures_live_bridge.yaml"
_LIVE_CAPTURE_DB_TIMEOUT_SECONDS = 15.0
_LIVE_CAPTURE_DB_BUSY_TIMEOUT_MS = 15_000


def load_stocks_live_bridge_config(path: str | Path | None = None) -> dict[str, Any]:
    selected = Path(path) if path else CONFIG_PATH
    payload = yaml.safe_load(selected.read_text(encoding="utf-8")) if selected.exists() else {}
    return (payload or {}).get("mexc_stock_futures_live_bridge") or {}


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


def _truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _context_float(context: dict[str, Any], key: str) -> float | None:
    return _float(context.get(key))


def _geometry_ok(direction: str, entry: float, stop: float,
                 targets: tuple[float, float, float]) -> bool:
    if direction == "long":
        return stop < entry < targets[0] < targets[1] < targets[2]
    if direction == "short":
        return targets[2] < targets[1] < targets[0] < entry < stop
    return False


def _rebase_geometry_to_confirmed_entry(
    *,
    direction: str,
    reference_entry: float | None,
    confirmed_entry: float | None,
    stop: float | None,
    targets: tuple[float | None, float | None, float | None],
) -> tuple[float, tuple[float, float, float]] | None:
    """Carry a valid planned R ladder to the price that Paper actually filled.

    Stock Paper entries are confirmed from a current quote after a completed
    15-minute bar.  A fast continuation can therefore fill above the original
    trigger.  Keeping the old stop/TP prices in that case can put TP1 below the
    confirmed entry.  Rebase only from an originally valid plan, preserving its
    stop percentage and target R-multiples.  This never rewrites Paper data.
    """
    values = (reference_entry, confirmed_entry, stop, *targets)
    if any(value is None for value in values):
        return None
    reference = float(reference_entry)
    entry = float(confirmed_entry)
    initial_stop = float(stop)
    initial_targets = (float(targets[0]), float(targets[1]), float(targets[2]))
    if reference <= 0 or entry <= 0 or not _geometry_ok(direction, reference, initial_stop, initial_targets):
        return None
    risk = abs(reference - initial_stop)
    if risk <= 0:
        return None
    risk_pct = risk / reference
    multipliers = [abs(target - reference) / risk for target in initial_targets]
    rebased_risk = entry * risk_pct
    if direction == "long":
        rebased_stop = entry - rebased_risk
        rebased_targets = tuple(entry + rebased_risk * multiple for multiple in multipliers)
    elif direction == "short":
        rebased_stop = entry + rebased_risk
        rebased_targets = tuple(entry - rebased_risk * multiple for multiple in multipliers)
    else:
        return None
    if not _geometry_ok(direction, entry, rebased_stop, rebased_targets):
        return None
    return rebased_stop, rebased_targets


def _loads(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    try:
        parsed = json.loads(value or "{}")
        return parsed if isinstance(parsed, dict) else {}
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}


def _lower(value: Any) -> str:
    return str(value or "").strip().lower()


def _truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value in (None, ""):
        return False
    if isinstance(value, (int, float)):
        return value != 0
    return str(value).strip().lower() in {"1", "true", "yes", "y", "supported"}


def _first_present(*values: Any) -> Any:
    for value in values:
        if value not in (None, ""):
            return value
    return None


def _as_dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _signal_row(conn: sqlite3.Connection, signal_id: str | None) -> dict[str, Any]:
    if not signal_id or not _table_exists(conn, "proposed_signals"):
        return {}
    row = conn.execute(
        "SELECT * FROM proposed_signals WHERE signal_id=? LIMIT 1",
        (str(signal_id),),
    ).fetchone()
    return dict(row) if row else {}


def _top_level_stock_context(payload: dict[str, Any]) -> dict[str, Any]:
    prefix = "stocks_context_"
    return {
        key[len(prefix):]: value
        for key, value in payload.items()
        if isinstance(key, str) and key.startswith(prefix)
    }


def _stock_signal_context(
    *,
    payload: dict[str, Any],
    order: dict[str, Any] | None = None,
    signal_row: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Extract the frozen stock context used by the live-only quality gate."""
    order_snapshot = _loads((order or {}).get("snapshot_json"))
    source_signal = _as_dict(payload.get("source_signal")) or _as_dict(
        order_snapshot.get("source_signal")
    )
    signal = signal_row or {}
    raw_from_signal = _loads(signal.get("raw_idea_json"))
    raw_context = (
        _as_dict(source_signal.get("raw_context"))
        or _as_dict(raw_from_signal.get("raw_context"))
        or raw_from_signal
    )
    actionability = (
        _as_dict(payload.get("intraday_actionability"))
        or _as_dict(raw_context.get("intraday_actionability"))
    )
    structured = _as_dict(raw_context.get("structured")) or _as_dict(raw_from_signal.get("structured"))
    news_contract = (
        _as_dict(payload.get("news_influence_contract"))
        or _as_dict(raw_context.get("news_influence_contract"))
    )
    stock_options = _top_level_stock_context(payload)

    market_regime = _first_present(
        signal.get("market_regime"),
        source_signal.get("market_regime"),
        raw_context.get("market_regime"),
        payload.get("market_regime"),
    )
    setup_type = _first_present(
        signal.get("setup_type"),
        source_signal.get("setup_type"),
        payload.get("thesis_setup_type"),
        payload.get("setup_type"),
    )
    news_supported = _first_present(
        signal.get("news_supported"),
        source_signal.get("news_supported"),
        news_contract.get("supported"),
        payload.get("news_supported"),
    )
    return {
        "market_regime": market_regime,
        "sector": _first_present(signal.get("sector"), structured.get("sector")),
        "setup_type": setup_type,
        "news_supported": _truthy(news_supported),
        "telegram_supported": _truthy(_first_present(
            signal.get("telegram_supported"), payload.get("telegram_supported"),
        )),
        "market_context_status": actionability.get("market_context_status"),
        "market_context_reason": actionability.get("market_context_reason"),
        "market_regime_intraday": actionability.get("market_regime_intraday"),
        "sector_confirmation_status": actionability.get("sector_confirmation_status"),
        "sector_confirmation_reason": actionability.get("sector_confirmation_reason"),
        "sector_etf": _first_present(actionability.get("sector_etf"), structured.get("sector_etf")),
        "sector_rth_return_pct": actionability.get("sector_rth_return_pct"),
        "sector_vs_vwap": actionability.get("sector_vs_vwap"),
        "spy_rth_return_pct": actionability.get("spy_rth_return_pct"),
        "spy_vs_vwap": actionability.get("spy_vs_vwap"),
        "qqq_rth_return_pct": actionability.get("qqq_rth_return_pct"),
        "qqq_vs_vwap": actionability.get("qqq_vs_vwap"),
        "rs_vs_spy": _first_present(actionability.get("rs_vs_spy"), structured.get("rs_vs_spy")),
        "rs_vs_sector": _first_present(actionability.get("rs_vs_sector"), structured.get("rs_vs_sector")),
        "rvol": _first_present(actionability.get("rvol"), structured.get("volume_ratio")),
        "liquidity_status": actionability.get("liquidity_status"),
        "session_phase": actionability.get("session_phase"),
        "catalyst_quality": _first_present(
            actionability.get("catalyst_quality"), payload.get("catalyst_quality"),
        ),
        "stocks_options_context": stock_options,
        "stocks_context_status": stock_options.get("status"),
        "stocks_context_reason": stock_options.get("reason"),
        "stocks_context_underlying": stock_options.get("underlying"),
        "has_intraday_actionability": bool(actionability),
        "source_route": _first_present(order_snapshot.get("source_route"), payload.get("source_route")),
        "raw_context_available": bool(raw_context),
    }


def _dedupe_reasons(reasons: Iterable[str]) -> list[str]:
    out: list[str] = []
    for reason in reasons:
        if reason and reason not in out:
            out.append(reason)
    return out


def _stop_is_low_confidence(stop_contract: dict[str, Any] | None) -> bool:
    if is_structural_stop_contract(stop_contract):
        return False
    contract = stop_contract or {}
    source = _lower(contract.get("stop_source") or contract.get("source"))
    model = _lower(contract.get("stop_model"))
    confidence = _lower(contract.get("confidence"))
    return bool(
        contract.get("fallback_used")
        or confidence == "low"
        or source.startswith("legacy")
        or source == "atr_fallback"
        or model.startswith("atr_distance")
    )


def _structural_stop_matches_execution(
    *,
    stop_contract: dict[str, Any] | None,
    candidate_structural_stop_contract: dict[str, Any] | None,
    tolerance_bps: float = 10.0,
) -> bool:
    """Return true only when the executable stop itself has structural provenance.

    A payload may contain a structural *candidate* while the actual Paper/live
    stop remains an ATR or legacy fallback.  Live must not treat that as a
    structural stop unless the executable stop price matches the candidate.
    """
    if is_structural_stop_contract(stop_contract):
        return True
    actual_stop = _float((stop_contract or {}).get("stop_price"))
    candidate = candidate_structural_stop_contract or {}
    candidate_stop = _float(
        candidate.get("stop_price")
        or candidate.get("raw_stop_price")
        or candidate.get("candidate_stop_price")
    )
    if (
        actual_stop is None
        or candidate_stop is None
        or not is_structural_stop_contract(candidate)
    ):
        return False
    tolerance = max(abs(actual_stop) * (float(tolerance_bps) / 10_000.0), 1e-9)
    return abs(actual_stop - candidate_stop) <= tolerance


def _stock_live_quality(
    *,
    filter_cfg: dict[str, Any] | None,
    context: dict[str, Any],
    direction: str,
    tier: str,
    score: float | None,
    entry_age_seconds: float,
    entry_mode: str,
    stop_contract: dict[str, Any],
    candidate_structural_stop_contract: dict[str, Any] | None,
) -> dict[str, Any]:
    block = filter_cfg or {}
    if not bool(block.get("enabled", False)):
        return {"enabled": False, "passed": True, "reasons": []}

    score_value = float(score or 0.0)
    market_regime = _lower(context.get("market_regime"))
    market_context = _lower(context.get("market_context_status"))
    sector_status = _lower(context.get("sector_confirmation_status"))
    setup_type = _lower(context.get("setup_type"))
    stock_context_status = _lower(context.get("stocks_context_status"))
    news_bypass = bool(block.get("allow_news_supported_bypass", True)) and bool(
        context.get("news_supported")
    )
    structural_stop = _structural_stop_matches_execution(
        stop_contract=stop_contract,
        candidate_structural_stop_contract=candidate_structural_stop_contract,
        tolerance_bps=float(block.get("candidate_structural_stop_tolerance_bps", 10.0)),
    )
    low_conf_stop = _stop_is_low_confidence(stop_contract) and not structural_stop
    reasons: list[str] = []
    intraday_regime = _lower(context.get("market_regime_intraday"))
    spy_vwap = _lower(context.get("spy_vs_vwap"))
    qqq_vwap = _lower(context.get("qqq_vs_vwap"))
    spy_ret = _context_float(context, "spy_rth_return_pct")
    qqq_ret = _context_float(context, "qqq_rth_return_pct")
    broad_threshold = float(block.get("min_broad_move_pct_for_low_conf_contra", 0.10))
    broad_intraday_down = bool(
        intraday_regime in {"trend_down", "downtrend", "bearish"}
        or (spy_vwap == "below" and qqq_vwap == "below")
        or (
            spy_ret is not None and qqq_ret is not None
            and spy_ret <= -broad_threshold and qqq_ret <= -broad_threshold
        )
    )
    broad_intraday_up = bool(
        intraday_regime in {"trend_up", "uptrend", "bullish"}
        or (spy_vwap == "above" and qqq_vwap == "above")
        or (
            spy_ret is not None and qqq_ret is not None
            and spy_ret >= broad_threshold and qqq_ret >= broad_threshold
        )
    )
    broad_bypass_score = float(block.get("min_score_to_bypass_broad_conflict", 90.0))
    strict_news_bypass = bool(
        news_bypass and score_value >= broad_bypass_score and sector_status == "confirmed"
    )

    if bool(block.get("require_structural_stop_for_live", False)) and not structural_stop:
        reasons.append("STOCK_LIVE_STOP_NOT_STRUCTURAL")
    if bool(block.get("require_intraday_actionability", False)) and not context.get(
        "has_intraday_actionability"
    ):
        missing_context_score = float(
            block.get("min_score_to_bypass_missing_intraday_actionability", 95.0)
        )
        if not (news_bypass and score_value >= missing_context_score):
            reasons.append("STOCK_LIVE_INTRADAY_CONTEXT_MISSING")

    if market_context in {"blocked", "conflict", "risk_off_conflict"}:
        reasons.append("STOCK_LIVE_MARKET_CONTEXT_CONFLICT")
    if sector_status in {"blocked", "conflict", "weak"}:
        reasons.append("STOCK_LIVE_SECTOR_CONTEXT_CONFLICT")

    if bool(block.get("require_sector_confirmation_for_live", False)):
        allowed_sector_status = {
            _lower(value)
            for value in block.get("live_allowed_sector_statuses", ["confirmed"])
        }
        unknown_floor = float(block.get("min_score_for_unknown_sector_live", 92.0))
        if sector_status not in allowed_sector_status and not (
            strict_news_bypass or (
                sector_status in {"", "unknown", "provisional"}
                and score_value >= unknown_floor
                and news_bypass
            )
        ):
            reasons.append("STOCK_LIVE_SECTOR_NOT_CONFIRMED")

    transition_short_score = float(block.get("min_transition_short_score", 83.0))
    transition_short_confirmed = sector_status == "confirmed" or (
        bool(context.get("has_intraday_actionability")) and market_context == "ok"
        and score_value >= transition_short_score
    )
    if direction == "long":
        disallowed = {
            _lower(value)
            for value in block.get("long_disallowed_market_regimes", ["risk_off", "bearish", "chop"])
        }
        if market_regime in disallowed and not strict_news_bypass:
            reasons.append("STOCK_LIVE_BROAD_MARKET_CONFLICT")
    elif direction == "short":
        hard_disallowed = {
            _lower(value)
            for value in block.get("short_disallowed_market_regimes", ["bullish", "risk_on"])
        }
        neutral_regimes = {
            _lower(value)
            for value in block.get("short_needs_confirmation_market_regimes", ["transition", "neutral", "range", "chop"])
        }
        if market_regime in hard_disallowed and not strict_news_bypass:
            reasons.append("STOCK_LIVE_SHORT_AGAINST_BROAD_MARKET")
        if market_regime in neutral_regimes and not (news_bypass or transition_short_confirmed):
            reasons.append("STOCK_LIVE_SHORT_CONTEXT_NOT_CONFIRMED")
        if (
            bool(block.get("transition_short_requires_broad_intraday_down", True))
            and market_regime in neutral_regimes
            and not (news_bypass or broad_intraday_down)
        ):
            reasons.append("STOCK_LIVE_SHORT_BROAD_NOT_BEARISH")

    if bool(block.get("block_against_intraday_broad", False)) and not strict_news_bypass:
        if direction == "long" and broad_intraday_down:
            reasons.append("STOCK_LIVE_BROAD_INTRADAY_AGAINST_DIRECTION")
        if direction == "short" and broad_intraday_up:
            reasons.append("STOCK_LIVE_BROAD_INTRADAY_AGAINST_DIRECTION")

    session_phase = _lower(context.get("session_phase"))
    open_keywords = tuple(
        _lower(value)
        for value in block.get("rth_open_session_phase_keywords", ["rth_open", "opening_range"])
    )
    if (
        bool(block.get("block_rth_open_without_confirmation", False))
        and session_phase
        and any(keyword and keyword in session_phase for keyword in open_keywords)
    ):
        open_floor = float(block.get("min_score_for_rth_open_confirmation", 85.0))
        if not (
            score_value >= open_floor
            and market_context == "ok"
            and sector_status == "confirmed"
            and structural_stop
        ):
            reasons.append("STOCK_LIVE_RTH_OPEN_UNCONFIRMED")

    reversal_keywords = tuple(
        _lower(value)
        for value in block.get("reversal_setup_keywords", ["reversal", "fade", "mean_reversion"])
    )
    if any(token and token in setup_type for token in reversal_keywords):
        min_reversal_score = float(block.get("min_reversal_score", 85.0))
        if score_value < min_reversal_score or (
            direction == "short" and market_regime not in {"risk_off", "bearish"}
        ):
            reasons.append("STOCK_LIVE_WEAK_REVERSAL")

    if low_conf_stop:
        legacy_stop_policy = _lower(block.get("legacy_stop_policy") or "block_stale")
        if legacy_stop_policy in {"block", "deny", "reject", "structural_only"}:
            reasons.append("STOCK_LIVE_LEGACY_STOP_NOT_STRUCTURAL")
        elif not news_bypass and legacy_stop_policy not in {"warn", "observe", "none"}:
            stale_limit = float(block.get("max_stale_legacy_stop_age_seconds", 90.0))
            stale_score_floor = float(block.get("min_score_for_stale_legacy_stop", 83.0))
            if stock_context_status == "stale" and (
                entry_age_seconds > stale_limit or score_value < stale_score_floor
            ):
                reasons.append("STOCK_LIVE_STALE_CONTEXT_LEGACY_STOP")
            missing_context_score = float(block.get("min_score_for_missing_context_legacy_stop", 85.0))
            if (
                not context.get("has_intraday_actionability")
                and not stock_context_status
                and market_regime in {"chop", "neutral", "range"}
                and score_value < missing_context_score
            ):
                reasons.append("STOCK_LIVE_LEGACY_STOP_CONTEXT_MISSING")
        if not news_bypass and bool(block.get("block_low_confidence_stop_against_intraday_broad", False)):
            contra_floor = float(block.get("min_score_for_low_conf_contra_broad", 83.0))
            if direction == "long" and broad_intraday_down and score_value < contra_floor:
                reasons.append("STOCK_LIVE_LOW_CONF_STOP_CONTRA_INTRADAY_BROAD")
            if direction == "short" and broad_intraday_up and score_value < contra_floor:
                reasons.append("STOCK_LIVE_LOW_CONF_STOP_CONTRA_INTRADAY_BROAD")

    return {
        "enabled": True,
        "version": str(block.get("version") or "stock_live_no_mfe_guard_v1"),
        "passed": not reasons,
        "reasons": _dedupe_reasons(reasons),
        "context": context,
        "stop_is_structural": structural_stop,
        "low_confidence_stop": low_conf_stop,
        "score": score_value,
        "tier": str(tier or "").upper(),
        "direction": direction,
        "entry_mode": entry_mode,
    }


def _stock_bybit_symbol(
    *,
    ticker: str,
    mexc_symbol: str | None,
    route_cfg: dict[str, Any],
    live_cfg: LiveCanaryConfig,
) -> str | None:
    """Return a Bybit stock-futures symbol only from an explicit curated map."""
    maps: list[dict[str, Any]] = []
    for key in ("bybit_stock_symbol_aliases", "bybit_symbol_aliases", "venue_symbols"):
        value = route_cfg.get(key)
        if isinstance(value, dict):
            maps.append(value)
    bybit_cfg = live_cfg.bybit_config()
    for key in ("stock_symbol_aliases",):
        value = bybit_cfg.get(key)
        if isinstance(value, dict):
            maps.append(value)

    lookup_keys = {
        ticker.upper(),
        f"{ticker.upper()}/USDT",
        f"{ticker.upper()}USDT",
    }
    if mexc_symbol:
        native = str(mexc_symbol).upper().replace("_", "/")
        lookup_keys.add(native)
        lookup_keys.add(native.replace("/", ""))
    for mapping in maps:
        aliases = {
            str(key).strip().upper().replace("_", "/"): str(value).strip().upper()
            for key, value in mapping.items()
            if str(key).strip() and str(value).strip()
        }
        for key in list(lookup_keys):
            normalized = key.replace("_", "/")
            if normalized in aliases:
                return aliases[normalized].replace("/", "").replace("_", "")
            if normalized.replace("/", "") in aliases:
                return aliases[normalized.replace("/", "")].replace("/", "").replace("_", "")
    if bool(route_cfg.get("allow_synthetic_bybit_stock_symbols", False)):
        return f"{ticker.upper()}USDT"
    return None


def _stock_venue_symbols(
    *, ticker: str, mexc_symbol: str | None,
    route_cfg: dict[str, Any], live_cfg: LiveCanaryConfig,
) -> dict[str, str]:
    out: dict[str, str] = {}
    if mexc_symbol:
        out["mexc"] = str(mexc_symbol)
    bybit = _stock_bybit_symbol(
        ticker=ticker, mexc_symbol=mexc_symbol, route_cfg=route_cfg, live_cfg=live_cfg,
    )
    if bybit:
        out["bybit"] = bybit
    return out


def _source_profile(order: dict[str, Any]) -> str:
    snapshot = _loads(order.get("snapshot_json") or order.get("order_snapshot_json"))
    source = snapshot.get("source_signal") or {}
    raw = source.get("raw_context") or {}
    return str(raw.get("paper_entry_profile") or "")


def _position_order(conn: sqlite3.Connection, position: dict[str, Any]) -> dict[str, Any]:
    order = conn.execute(
        "SELECT * FROM mexc_stock_futures_paper_orders WHERE order_id=?",
        (position.get("order_id"),),
    ).fetchone()
    return dict(order) if order else {}


def _candidate_rows(
    conn: sqlite3.Connection,
    *,
    rows: Iterable[dict[str, Any]] | None,
    now: datetime,
    max_age_seconds: float,
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    if rows is not None:
        out = []
        for raw in rows:
            position = dict(raw)
            order = _position_order(conn, position)
            out.append((position, order))
        return out
    cutoff = (now.timestamp() - max_age_seconds)
    query = (
        "SELECT * FROM mexc_stock_futures_paper_positions "
        "WHERE status='OPEN' AND entry_at>=? ORDER BY entry_at DESC LIMIT 50"
    )
    out = []
    for row in conn.execute(
        query,
        (datetime.fromtimestamp(cutoff, tz=timezone.utc).isoformat(),),
    ):
        position = dict(row)
        out.append((position, _position_order(conn, position)))
    return out


def _table_exists(conn: sqlite3.Connection, name: str) -> bool:
    return bool(conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone())


def _columns(conn: sqlite3.Connection, table: str) -> set[str]:
    if not _table_exists(conn, table):
        return set()
    return {str(row[1]) for row in conn.execute(f"PRAGMA table_info({table})")}


def _source_signal_seen(conn: sqlite3.Connection, source_signal_id: str | None) -> bool:
    """Deduplicate the same Paper trade across standard and Pre-US bridges."""
    if not source_signal_id or not _table_exists(conn, "mexc_canary_decisions"):
        return False
    return bool(conn.execute(
        "SELECT 1 FROM mexc_canary_decisions "
        "WHERE json_extract(decision_json,'$.source_signal_id')=? "
        "AND eligible=1 "
        "AND state NOT LIKE 'REJECTED%' "
        "LIMIT 1",
        (str(source_signal_id),),
    ).fetchone())


def _record_rejected_stock_decision(
    conn: sqlite3.Connection,
    *,
    row: dict[str, Any],
    payload: dict[str, Any],
    reasons: list[str],
    cfg: dict[str, Any],
    live: LiveCanaryConfig,
    now: datetime,
    signal_prefix: str,
    decision_context_type: str,
    paper_alert_id: str | None = None,
) -> None:
    source_signal_id = str(row.get("source_signal_id") or "")
    if not source_signal_id or not reasons:
        return
    reason_key = "|".join(sorted({str(reason) for reason in reasons if str(reason)}))
    if not reason_key:
        return
    digest = hashlib.sha256(f"{source_signal_id}|{reason_key}".encode("utf-8")).hexdigest()[:12]
    signal_id = f"{signal_prefix}_rejected:{source_signal_id}:{digest}"
    decision_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"mexc-live-stock-rejected:{signal_id}"))
    ticker = str(row.get("ticker") or payload.get("display_symbol") or "").upper()
    symbol = f"{ticker}/USDT" if ticker and "/" not in ticker else (ticker or "UNKNOWN/USDT")
    entry_mode = str(
        row.get("paper_execution_entry_mode")
        or row.get("entry_mode")
        or payload.get("paper_execution_entry_mode")
        or ""
    ).upper()
    frozen = {
        "signal_id": signal_id,
        "source_signal_id": source_signal_id,
        "source_paper_alert_id": paper_alert_id or row.get("alert_id"),
        "decision_context_type": decision_context_type,
        "captured_at": now.isoformat(),
        "signal_created_at": row.get("signal_created_at") or row.get("created_at"),
        "entry_triggered_at": row.get("entry_at") or payload.get("entry_triggered_at"),
        "symbol": symbol,
        "display_symbol": ticker,
        "asset_class": "stock_futures",
        "mode": str(cfg.get("mode") or "stock_intraday"),
        "direction": str(row.get("direction") or "").lower(),
        "tier": str(row.get("tier") or row.get("source_pre_gate_tier") or "").upper(),
        "score": _float(row.get("score") or row.get("source_score")),
        "entry_mode": entry_mode,
        "entry_price": _float(row.get("entry_price_used") or row.get("entry_price") or payload.get("entry_used")),
        "original_stop": _float(row.get("stop_initial") or payload.get("stop")),
        "paper_action": "FULL_SIZE",
        "paper_size_weight": 1.0,
        "live_route_risk_cap": float(cfg.get("risk_multiplier", 0.5)),
        "live_risk_multiplier": float(cfg.get("risk_multiplier", 0.5)),
        "preentry_source": decision_context_type,
        "preentry_data_quality": "ok",
        "strategy_profile": str(cfg.get("route_id") or ""),
        "strategy_version": str(
            row.get("paper_entry_profile")
            or payload.get("paper_entry_profile")
            or cfg.get("live_strategy_version")
            or ""
        ),
        "risk_bucket": str(cfg.get("risk_bucket") or "stock_intraday_breakout"),
        "rejection_reasons": sorted({str(reason) for reason in reasons}),
    }
    record = {
        "decision_id": decision_id,
        "signal_id": signal_id,
        "captured_at": now.isoformat(),
        "paper_alert_id": paper_alert_id or row.get("alert_id"),
        "symbol": symbol,
        "mode": frozen["mode"],
        "entry_mode": entry_mode,
        "eligible": 0,
        "state": "REJECTED",
        "rejection_reasons_json": json.dumps(frozen["rejection_reasons"], sort_keys=True),
        "decision_json": _stable_json(frozen),
        "decision_hash": _hash(frozen),
        "config_hash": live.config_hash,
        "decision_context_type": decision_context_type,
    }
    ls.insert_decision(conn, record, queue=False)


def _standard_paper_candidates(
    conn: sqlite3.Connection,
    *,
    now: datetime,
    max_age_seconds: float,
    source_signal_id: str | None = None,
    payload_override: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Return fresh, currently-open normal Paper stock entries.

    This is intentionally separate from the MEXC-stock Paper simulator.  The
    ordinary stock Paper tracker is the strategy authority for its own lane;
    this function only freezes an already-confirmed, point-in-time fill for
    the MEXC execution worker.
    """
    required = {
        "proposed_signals", "signal_alerts", "paper_execution_outcomes",
        "mexc_stock_futures_contracts",
    }
    if not all(_table_exists(conn, table) for table in required):
        return []
    execution_cols = _columns(conn, "paper_execution_outcomes")
    live_contract_cols = {"entry_time_basis", "current_price_revalidated"}
    if not live_contract_cols.issubset(execution_cols):
        return []
    cutoff = datetime.fromtimestamp(
        now.timestamp() - max_age_seconds, tz=timezone.utc,
    ).isoformat()
    signal_filter = "AND p.signal_id=?" if source_signal_id else "AND a.alert_id IS NOT NULL"
    params: tuple[Any, ...] = ((cutoff, source_signal_id) if source_signal_id else (cutoff,))
    rows = conn.execute(
        f"""
        WITH latest_execution AS (
          SELECT o.*, ROW_NUMBER() OVER (
            PARTITION BY o.signal_id ORDER BY o.computed_at DESC, o.rowid DESC
          ) AS rn
          FROM paper_execution_outcomes o
        ), latest_contract AS (
          SELECT c.*, ROW_NUMBER() OVER (
            PARTITION BY c.ticker ORDER BY c.snapshot_at DESC, c.rowid DESC
          ) AS rn
          FROM mexc_stock_futures_contracts c
        ), latest_alert AS (
          SELECT a.*, ROW_NUMBER() OVER (
            PARTITION BY a.signal_id ORDER BY a.sent_at DESC, a.rowid DESC
          ) AS rn
          FROM signal_alerts a
          WHERE a.alert_type='paper_entry'
            AND lower(COALESCE(a.asset_class,''))='stocks'
        )
        SELECT
          a.alert_id, a.payload_json, a.sent_at,
          p.signal_id AS source_signal_id, p.symbol AS ticker, p.direction,
          p.tier, p.score, p.created_at AS signal_created_at,
          p.market_regime, p.sector, p.setup_type, p.news_supported,
          p.telegram_supported, p.raw_idea_json,
          NULL AS planned_entry,
          e.entry_at, e.entry_price_used, e.stop_initial,
          e.paper_entry_profile, e.paper_execution_entry_mode,
          e.lifecycle_state, e.execution_validity, e.entry_time_basis,
          e.current_price_revalidated, e.close_reason,
          c.mexc_symbol, c.state AS contract_state, c.api_allowed
        FROM proposed_signals p
        JOIN latest_execution e ON e.signal_id=p.signal_id AND e.rn=1
        LEFT JOIN latest_contract c ON c.ticker=p.symbol AND c.rn=1
        LEFT JOIN latest_alert a ON a.signal_id=p.signal_id AND a.rn=1
        WHERE lower(COALESCE(p.asset_class,''))='stocks'
          AND lower(COALESCE(p.mode,''))='intraday'
          AND e.lifecycle_state='OPEN'
          AND e.execution_validity='valid'
          AND e.entry_at>=?
          {signal_filter}
        ORDER BY e.entry_at DESC
        """,
        params,
    ).fetchall()
    return [dict(row) for row in rows]


def capture_standard_paper_breakouts(
    *,
    db: str | Path | None = None,
    route_cfg: dict[str, Any] | None = None,
    live_cfg: LiveCanaryConfig | None = None,
    now: datetime | None = None,
    source_signal_id: str | None = None,
    payload_override: dict[str, Any] | None = None,
    paper_alert_id: str | None = None,
) -> dict[str, Any]:
    """Queue fresh main-Paper stock breakouts for multi-venue preflight.

    No Paper row is altered here.  A decision is queued only after the main
    Paper tracker has recorded an OPEN point-in-time entry. Venue-specific
    contract availability remains authoritative at the parallel preflight.
    """
    cfg = route_cfg or load_stocks_live_bridge_config()
    standard = dict(cfg.get("standard_paper_breakout") or {})
    live = live_cfg or load_live_canary_config()
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    counts = {"seen": 0, "queued": 0, "duplicate": 0, "rejected": 0}
    reasons: dict[str, int] = {}

    def rejected(reason: str) -> None:
        counts["rejected"] += 1
        reasons[reason] = reasons.get(reason, 0) + 1

    if (not bool(cfg.get("enabled", False)) or not bool(standard.get("enabled", False))
            or (route_cfg is None and not route_enabled(
                mode="stock_intraday", entry_mode="BREAKOUT_CONTINUATION",
                asset_class="stocks",
            ))):
        return {**counts, "status": "DISABLED", "reasons": reasons}
    risk_multiplier = float(cfg.get("risk_multiplier", 0.5))
    expected_risk = float(cfg.get("fixed_risk_usdt", 5.0))
    if abs((live.risk_per_trade_usdt * risk_multiplier) - expected_risk) > 1e-9:
        return {**counts, "status": "RISK_CONFIG_MISMATCH", "reasons": reasons}
    if not live.live_armed():
        return {**counts, "status": "LIVE_NOT_ARMED", "reasons": reasons}

    allowed_profiles = {str(value) for value in (standard.get("allowed_source_profiles") or [])}
    allowed_modes = {str(value).upper() for value in (standard.get("allowed_entry_modes") or [])}
    allowed_directions = {str(value).lower() for value in (standard.get("allowed_directions") or [])}
    min_score = float(standard.get("min_score", 0.0))
    blocked_symbols = {
        str(value).upper().replace("/", "_")
        for value in (cfg.get("blocked_mexc_symbols") or [])
    }
    armed_venues = set(live.enabled_live_venues(asset_class="stock_futures"))
    max_age = float(standard.get("max_capture_age_seconds", cfg.get("max_capture_age_seconds", 300)))
    path = Path(db) if db else load_config().db_path
    rejection_cfg = {
        **cfg,
        **standard,
        "mode": cfg.get("mode") or "stock_intraday",
        "route_id": standard.get("route_id") or cfg.get("route_id"),
        "risk_multiplier": risk_multiplier,
        "risk_bucket": cfg.get("risk_bucket") or "stock_intraday_breakout",
    }

    with ls.connect(
        path,
        timeout_seconds=_LIVE_CAPTURE_DB_TIMEOUT_SECONDS,
        busy_timeout_ms=_LIVE_CAPTURE_DB_BUSY_TIMEOUT_MS,
    ) as conn:
        ls.ensure_tables(conn)
        def reject_row(row: dict[str, Any], payload: dict[str, Any],
                       reason_values: str | list[str]) -> None:
            reason_list = (
                [reason_values] if isinstance(reason_values, str)
                else [str(reason) for reason in reason_values]
            )
            reason_list = [str(reason) for reason in reason_list if str(reason)]
            if reason_list:
                counts["rejected"] += 1
                for reason in reason_list:
                    reasons[reason] = reasons.get(reason, 0) + 1
            _record_rejected_stock_decision(
                conn,
                row=row,
                payload=payload,
                reasons=reason_list,
                cfg=rejection_cfg,
                live=live,
                now=now,
                signal_prefix="stock_paper",
                decision_context_type="point_in_time_stock_paper_entry",
                paper_alert_id=paper_alert_id,
            )

        candidate_rows = _standard_paper_candidates(
            conn, now=now, max_age_seconds=max_age,
            source_signal_id=source_signal_id, payload_override=payload_override,
        )
        if not candidate_rows and source_signal_id and payload_override is not None:
            rejected("PAPER_EXECUTION_OUTCOME_NOT_MATERIALIZED")

        for row in candidate_rows:
            counts["seen"] += 1
            if _source_signal_seen(conn, row.get("source_signal_id")):
                counts["duplicate"] += 1
                continue
            payload = dict(payload_override) if payload_override is not None else _loads(
                row.get("payload_json")
            )
            profile = str(row.get("paper_entry_profile") or payload.get("paper_entry_profile") or "")
            entry_mode = str(row.get("paper_execution_entry_mode") or payload.get("paper_execution_entry_mode") or "").upper()
            direction = str(row.get("direction") or "").lower()
            entry_at = _parse(row.get("entry_at"))
            entry = _float(row.get("entry_price_used") or payload.get("entry_used"))
            stop = _float(row.get("stop_initial") or payload.get("stop"))
            targets = (_float(payload.get("tp1")), _float(payload.get("tp2")), _float(payload.get("tp3")))
            if str(row.get("entry_time_basis") or "") != "point_in_time_current_bar":
                reject_row(row, payload, "PAPER_EXECUTION_NOT_POINT_IN_TIME")
                continue
            if not _truthy(row.get("current_price_revalidated")):
                reject_row(row, payload, "PAPER_EXECUTION_PRICE_NOT_REVALIDATED")
                continue
            if str(row.get("close_reason") or "open") not in {"open", ""}:
                reject_row(row, payload, "PAPER_EXECUTION_NOT_OPEN")
                continue
            if allowed_profiles and profile not in allowed_profiles:
                reject_row(row, payload, "SOURCE_PROFILE_NOT_LIVE_ENABLED")
                continue
            if entry_mode not in allowed_modes:
                reject_row(row, payload, "ENTRY_MODE_NOT_ALLOWED")
                continue
            if direction not in allowed_directions:
                reject_row(row, payload, "DIRECTION_NOT_ALLOWED")
                continue
            score = _float(row.get("score"))
            if score is None or score < min_score:
                reject_row(row, payload, "SCORE_BELOW_LIVE_CANARY")
                continue
            if entry_at is None or (now - entry_at).total_seconds() < 0 or (now - entry_at).total_seconds() > max_age:
                reject_row(row, payload, "CAPTURE_TOO_OLD")
                continue
            contract_state = _float(row.get("contract_state"))
            mexc_symbol = str(row.get("mexc_symbol") or "")
            ticker = str(row.get("ticker") or "").upper()
            venue_symbols = _stock_venue_symbols(
                ticker=ticker, mexc_symbol=mexc_symbol,
                route_cfg=cfg, live_cfg=live,
            )
            mexc_contract_ok = bool(
                mexc_symbol and contract_state == 0 and bool(row.get("api_allowed"))
            )
            mexc_blocked = mexc_symbol.upper().replace("/", "_") in blocked_symbols
            possible_venues = set(armed_venues)
            if not mexc_contract_ok or mexc_blocked:
                possible_venues.discard("mexc")
            if "bybit" not in venue_symbols:
                possible_venues.discard("bybit")
            if not possible_venues:
                reject_row(row, payload, "MEXC_SYMBOL_BLOCKED" if mexc_blocked else "NO_STOCK_LIVE_VENUE")
                continue
            reference_entry = _float(row.get("planned_entry") or payload.get("entry_reference"))
            geometry_rebased = False
            current_geometry_valid = (
                None not in (entry, stop, *targets)
                and _geometry_ok(
                    direction, float(entry), float(stop),
                    (float(targets[0]), float(targets[1]), float(targets[2])),
                )
            )
            if not current_geometry_valid:
                rebased = _rebase_geometry_to_confirmed_entry(
                    direction=direction, reference_entry=reference_entry,
                    confirmed_entry=entry, stop=stop, targets=targets,
                )
                if rebased is not None:
                    stop, targets = rebased
                    geometry_rebased = True
            if None in (entry, stop, *targets) or not _geometry_ok(
                direction, float(entry), float(stop),
                (float(targets[0]), float(targets[1]), float(targets[2])),
            ):
                reject_row(row, payload, "INVALID_GEOMETRY")
                continue

            source_signal_id = str(row["source_signal_id"])
            signal_id = f"stock_paper:{source_signal_id}"
            decision_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"mexc-live-stock-paper:{source_signal_id}"))
            setup_payload = payload.get("raw_setup") or payload.get("setup") or {}
            stop_contract = build_initial_stop_contract(
                symbol=ticker,
                asset_class="stock_futures",
                mode=str(cfg.get("mode") or "stock_intraday"),
                direction=direction,
                entry_price=float(entry),
                stop_price=float(stop),
                setup=setup_payload if isinstance(setup_payload, dict) else {},
                payload=payload,
                source="stocks_breakout_bridge",
            )
            stock_context = _stock_signal_context(
                payload=payload, order=None, signal_row=row,
            )
            candidate_structural_stop = payload.get("candidate_structural_stop_contract") or {}
            quality = _stock_live_quality(
                filter_cfg=standard.get("live_quality_filter") or cfg.get("live_quality_filter"),
                context=stock_context,
                direction=direction,
                tier=str(row.get("tier") or "A").upper(),
                score=score,
                entry_age_seconds=max(0.0, (now - entry_at).total_seconds()),
                entry_mode=entry_mode,
                stop_contract=stop_contract,
                candidate_structural_stop_contract=(
                    candidate_structural_stop
                    if isinstance(candidate_structural_stop, dict) else {}
                ),
            )
            quality_reasons = quality.get("reasons") or []
            if quality_reasons:
                reject_row(row, payload, [str(reason) for reason in quality_reasons])
                continue
            frozen = {
                "signal_id": signal_id,
                "source_signal_id": source_signal_id,
                "source_paper_alert_id": paper_alert_id or row.get("alert_id"),
                "decision_context_type": "point_in_time_stock_paper_entry",
                "captured_at": now.isoformat(),
                "signal_created_at": row.get("signal_created_at"),
                "entry_triggered_at": entry_at.isoformat(),
                "entry_bar_open_at": payload.get("entry_bar_open_at") or entry_at.isoformat(),
                "entry_detected_at": now.isoformat(),
                "entry_time_basis": "point_in_time_current_bar",
                "current_price_revalidated": True,
                "entry_revalidation_reason": "main_stock_paper_entry_snapshot",
                "symbol": f"{ticker}/USDT",
                "display_symbol": ticker,
                "venue_symbols": venue_symbols,
                "bybit_stock_symbol_explicit": "bybit" in venue_symbols,
                "blocked_venues": [
                    venue for venue, blocked in (
                        ("mexc", mexc_blocked or not mexc_contract_ok),
                        ("bybit", "bybit" in armed_venues and "bybit" not in venue_symbols),
                    ) if blocked
                ],
                "asset_class": "stock_futures",
                "mode": str(cfg.get("mode") or "stock_intraday"),
                "direction": direction,
                "tier": str(row.get("tier") or "A").upper(),
                "score": score,
                "entry_mode": entry_mode,
                "entry_price": float(entry),
                "original_stop": float(stop),
                "stop_contract": stop_contract,
                "stop_label": stop_contract_label(stop_contract),
                "source_initial_stop_contract": payload.get("initial_stop_contract") or {},
                "candidate_structural_stop_contract": (
                    candidate_structural_stop if isinstance(candidate_structural_stop, dict) else {}
                ),
                "stock_context": stock_context,
                "stock_live_quality": quality,
                "tp1": float(targets[0]),
                "tp2": float(targets[1]),
                "tp3": float(targets[2]),
                "entry_age_seconds": max(0.0, (now - entry_at).total_seconds()),
                "paper_action": "FULL_SIZE",
                "paper_size_weight": 1.0,
                "live_route_risk_cap": risk_multiplier,
                "live_risk_multiplier": risk_multiplier,
                "preentry_source": "main_stock_paper_entry",
                "preentry_data_quality": "ok",
                "strategy_profile": str(standard.get("route_id") or cfg.get("route_id") or ""),
                "strategy_version": profile,
                "source_paper_profile": profile,
                "risk_bucket": str(cfg.get("risk_bucket") or "stock_intraday_breakout"),
                "protection_model": "early_mfe_protection_v1",
            }
            if geometry_rebased:
                frozen.update({
                    "live_geometry_rebased": True,
                    "geometry_reprice_reason": "confirmed_stock_entry_preserve_original_r_ladder",
                    "geometry_reference_entry": reference_entry,
                })
            record = {
                "decision_id": decision_id,
                "signal_id": signal_id,
                "captured_at": now.isoformat(),
                "paper_alert_id": paper_alert_id or row.get("alert_id"),
                "symbol": frozen["symbol"],
                "mode": frozen["mode"],
                "entry_mode": entry_mode,
                "eligible": 1,
                "state": "QUEUED",
                "rejection_reasons_json": "[]",
                "decision_json": _stable_json(frozen),
                "decision_hash": _hash(frozen),
                "config_hash": live.config_hash,
                "decision_context_type": frozen["decision_context_type"],
            }
            result = ls.insert_decision(conn, record, queue=True)
            if result["queued"]:
                counts["queued"] += 1
            else:
                counts["duplicate"] += 1
    return {
        **counts,
        "status": "OK",
        "reasons": reasons,
        "route_id": standard.get("route_id"),
        "risk_usdt": expected_risk,
    }


def capture_filled_positions(
    rows: Iterable[dict[str, Any]] | None = None,
    *,
    db: str | Path | None = None,
    route_cfg: dict[str, Any] | None = None,
    live_cfg: LiveCanaryConfig | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Queue filled stock-futures Paper breakouts into the MEXC canary worker.

    The stock Paper lane remains the strategy authority. This bridge only
    mirrors fresh, open, version-pinned BREAKOUT_CONTINUATION fills into the
    existing live executor with a fixed $5 risk budget.
    """
    cfg = route_cfg or load_stocks_live_bridge_config()
    live = live_cfg or load_live_canary_config()
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    counts = {"seen": 0, "queued": 0, "duplicate": 0, "rejected": 0}
    reasons: dict[str, int] = {}
    provided_rows = list(rows) if rows is not None else None

    def rejected(reason: str) -> None:
        counts["rejected"] += 1
        reasons[reason] = reasons.get(reason, 0) + 1

    if not bool(cfg.get("enabled", False)):
        return {**counts, "status": "DISABLED", "reasons": reasons}
    if provided_rows is not None and not provided_rows:
        return {**counts, "status": "OK", "reasons": reasons,
                "route_id": cfg.get("route_id"),
                "risk_usdt": float(cfg.get("fixed_risk_usdt", 5.0))}
    risk_multiplier = float(cfg.get("risk_multiplier", 0.5))
    expected_risk = float(cfg.get("fixed_risk_usdt", 5.0))
    if abs((live.risk_per_trade_usdt * risk_multiplier) - expected_risk) > 1e-9:
        return {**counts, "status": "RISK_CONFIG_MISMATCH", "reasons": reasons}
    if not live.live_armed():
        return {**counts, "status": "LIVE_NOT_ARMED", "reasons": reasons}

    allowed_profiles = {str(value) for value in (cfg.get("allowed_source_profiles") or [])}
    allow_unprofiled_source = bool(cfg.get("allow_unprofiled_source", False))
    allowed_modes = {str(value).upper() for value in (cfg.get("allowed_entry_modes") or [])}
    allowed_directions = {str(value).lower() for value in (cfg.get("allowed_directions") or [])}
    min_score = float(cfg.get("min_score", 0.0))
    blocked_symbols = {
        str(value).upper().replace("/", "_")
        for value in (cfg.get("blocked_mexc_symbols") or [])
    }
    armed_venues = set(live.enabled_live_venues(asset_class="stock_futures"))
    expected_strategy = str(cfg.get("source_strategy_id") or "")
    max_age = float(cfg.get("max_capture_age_seconds", 300))
    path = Path(db) if db else load_config().db_path

    with ls.connect(
        path,
        timeout_seconds=_LIVE_CAPTURE_DB_TIMEOUT_SECONDS,
        busy_timeout_ms=_LIVE_CAPTURE_DB_BUSY_TIMEOUT_MS,
    ) as conn:
        ls.ensure_tables(conn)
        if not conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' "
            "AND name='mexc_stock_futures_paper_positions'"
        ).fetchone():
            return {**counts, "status": "NO_STOCK_PAPER_TABLE", "reasons": reasons}
        def reject_position(position: dict[str, Any], order: dict[str, Any],
                            payload: dict[str, Any],
                            reason_values: str | list[str]) -> None:
            reason_list = (
                [reason_values] if isinstance(reason_values, str)
                else [str(reason) for reason in reason_values]
            )
            reason_list = [str(reason) for reason in reason_list if str(reason)]
            if reason_list:
                counts["rejected"] += 1
                for reason in reason_list:
                    reasons[reason] = reasons.get(reason, 0) + 1
            row = {
                **position,
                "paper_entry_profile": _source_profile(order),
                "score": order.get("source_score"),
                "tier": order.get("source_pre_gate_tier"),
            }
            _record_rejected_stock_decision(
                conn,
                row=row,
                payload=payload,
                reasons=reason_list,
                cfg=cfg,
                live=live,
                now=now,
                signal_prefix="stock_mexc",
                decision_context_type=str(
                    cfg.get("decision_context_type") or "point_in_time_stock_futures_fill"
                ),
            )

        for position, order in _candidate_rows(conn, rows=provided_rows, now=now, max_age_seconds=max_age):
            counts["seen"] += 1
            if _source_signal_seen(conn, position.get("source_signal_id")):
                counts["duplicate"] += 1
                continue
            order_snapshot = _loads(order.get("snapshot_json"))
            if str(position.get("status") or "") != "OPEN":
                reject_position(position, order, order_snapshot, "POSITION_NOT_OPEN")
                continue
            if expected_strategy and str(position.get("strategy_id") or "") != expected_strategy:
                reject_position(position, order, order_snapshot, "STRATEGY_ID_MISMATCH")
                continue
            entry_mode = str(position.get("entry_mode") or "").upper()
            if entry_mode not in allowed_modes:
                reject_position(position, order, order_snapshot, "ENTRY_MODE_NOT_ALLOWED")
                continue
            source_profile = _source_profile(order)
            if allowed_profiles and source_profile not in allowed_profiles and not (
                allow_unprofiled_source and not source_profile
            ):
                reject_position(position, order, order_snapshot, "SOURCE_PROFILE_NOT_LIVE_ENABLED")
                continue
            direction = str(position.get("direction") or "").lower()
            if direction not in allowed_directions:
                reject_position(position, order, order_snapshot, "DIRECTION_NOT_ALLOWED")
                continue
            source_score = _float(order.get("source_score"))
            if source_score is None or source_score < min_score:
                reject_position(position, order, order_snapshot, "SCORE_BELOW_LIVE_CANARY")
                continue
            mexc_symbol = str(position.get("mexc_symbol") or "")
            ticker = str(position.get("ticker") or "").upper()
            venue_symbols = _stock_venue_symbols(
                ticker=ticker, mexc_symbol=mexc_symbol,
                route_cfg=cfg, live_cfg=live,
            )
            mexc_blocked = mexc_symbol.upper().replace("/", "_") in blocked_symbols
            possible_venues = set(armed_venues)
            if mexc_blocked or not mexc_symbol:
                possible_venues.discard("mexc")
            if "bybit" not in venue_symbols:
                possible_venues.discard("bybit")
            if not possible_venues:
                reject_position(
                    position, order, order_snapshot,
                    "MEXC_SYMBOL_BLOCKED" if mexc_blocked else "NO_STOCK_LIVE_VENUE",
                )
                continue
            entry_at = _parse(position.get("entry_at"))
            if entry_at is None:
                reject_position(position, order, order_snapshot, "ENTRY_AT_MISSING")
                continue
            age = (now - entry_at).total_seconds()
            if age < 0 or age > max_age:
                reject_position(position, order, order_snapshot, "CAPTURE_TOO_OLD")
                continue
            entry = _float(position.get("entry_price"))
            stop = _float(position.get("stop_initial"))
            targets = (
                _float(position.get("tp1")),
                _float(position.get("tp2")),
                _float(position.get("tp3")),
            )
            if None in (entry, stop, *targets) or not _geometry_ok(
                direction, float(entry), float(stop),
                (float(targets[0]), float(targets[1]), float(targets[2])),
            ):
                reject_position(position, order, order_snapshot, "INVALID_GEOMETRY")
                continue

            source_position_id = str(position.get("position_id") or "")
            signal_id = f"stock_mexc:{source_position_id}"
            decision_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"mexc-live-stock:{source_position_id}"))
            stop_contract = build_initial_stop_contract(
                symbol=ticker,
                asset_class="stock_futures",
                mode=str(cfg.get("mode") or "stock_intraday"),
                direction=direction,
                entry_price=float(entry),
                stop_price=float(stop),
                setup={},
                payload=order_snapshot,
                source="stocks_breakout_bridge",
            )
            signal_context_row = _signal_row(conn, position.get("source_signal_id"))
            stock_context = _stock_signal_context(
                payload=order_snapshot, order=order, signal_row=signal_context_row,
            )
            candidate_structural_stop = order_snapshot.get("candidate_structural_stop_contract") or {}
            quality = _stock_live_quality(
                filter_cfg=cfg.get("live_quality_filter"),
                context=stock_context,
                direction=direction,
                tier=str(order.get("source_pre_gate_tier") or "A").upper(),
                score=source_score,
                entry_age_seconds=max(0.0, age),
                entry_mode=entry_mode,
                stop_contract=stop_contract,
                candidate_structural_stop_contract=(
                    candidate_structural_stop
                    if isinstance(candidate_structural_stop, dict) else {}
                ),
            )
            quality_reasons = quality.get("reasons") or []
            if quality_reasons:
                reject_position(position, order, order_snapshot, [str(reason) for reason in quality_reasons])
                continue
            frozen = {
                "signal_id": signal_id,
                "source_signal_id": position.get("source_signal_id"),
                "source_position_id": source_position_id,
                "source_order_id": position.get("order_id"),
                "decision_context_type": str(cfg.get("decision_context_type") or "point_in_time_stock_futures_fill"),
                "captured_at": now.isoformat(),
                "signal_created_at": order.get("decision_at") or position.get("created_at"),
                "entry_triggered_at": entry_at.isoformat(),
                "entry_bar_open_at": entry_at.isoformat(),
                "entry_detected_at": now.isoformat(),
                "entry_time_basis": "point_in_time_current_bar",
                "current_price_revalidated": True,
                "entry_revalidation_reason": "mexc_stock_futures_paper_fill_snapshot",
                "symbol": f"{ticker}/USDT",
                "display_symbol": ticker,
                "venue_symbols": venue_symbols,
                "bybit_stock_symbol_explicit": "bybit" in venue_symbols,
                "blocked_venues": [
                    venue for venue, blocked in (
                        ("mexc", mexc_blocked or not mexc_symbol),
                        ("bybit", "bybit" in armed_venues and "bybit" not in venue_symbols),
                    ) if blocked
                ],
                "asset_class": "stock_futures",
                "mode": str(cfg.get("mode") or "stock_intraday"),
                "direction": direction,
                "tier": str(order.get("source_pre_gate_tier") or "A").upper(),
                "score": source_score,
                "entry_mode": entry_mode,
                "entry_price": float(entry),
                "original_stop": float(stop),
                "stop_contract": stop_contract,
                "stop_label": stop_contract_label(stop_contract),
                "source_initial_stop_contract": order_snapshot.get("initial_stop_contract") or {},
                "candidate_structural_stop_contract": (
                    candidate_structural_stop if isinstance(candidate_structural_stop, dict) else {}
                ),
                "stock_context": stock_context,
                "stock_live_quality": quality,
                "tp1": float(targets[0]),
                "tp2": float(targets[1]),
                "tp3": float(targets[2]),
                "entry_age_seconds": max(0.0, age),
                "paper_action": "FULL_SIZE",
                "paper_size_weight": 1.0,
                "live_route_risk_cap": risk_multiplier,
                "live_risk_multiplier": risk_multiplier,
                "preentry_source": "mexc_stock_futures_paper_fill",
                "preentry_data_quality": "ok",
                "strategy_profile": str(cfg.get("route_id") or ""),
                "strategy_version": source_profile or str(cfg.get("live_strategy_version") or ""),
                "source_strategy_id": expected_strategy,
                "source_paper_profile": source_profile,
                "risk_bucket": str(cfg.get("risk_bucket") or "stock_intraday_breakout"),
                "protection_model": "early_mfe_protection_v1",
            }
            record = {
                "decision_id": decision_id,
                "signal_id": signal_id,
                "captured_at": now.isoformat(),
                "paper_alert_id": None,
                "symbol": frozen["symbol"],
                "mode": frozen["mode"],
                "entry_mode": entry_mode,
                "eligible": 1,
                "state": "QUEUED",
                "rejection_reasons_json": "[]",
                "decision_json": _stable_json(frozen),
                "decision_hash": _hash(frozen),
                "config_hash": live.config_hash,
                "decision_context_type": frozen["decision_context_type"],
            }
            result = ls.insert_decision(conn, record, queue=True)
            if result["queued"]:
                counts["queued"] += 1
            else:
                counts["duplicate"] += 1
    return {
        **counts,
        "status": "OK",
        "reasons": reasons,
        "route_id": cfg.get("route_id"),
        "risk_usdt": expected_risk,
    }
