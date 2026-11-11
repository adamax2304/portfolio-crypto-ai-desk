"""Authoritative PAPER action/size resolver — the single source of truth for what size a signal enters
the production paper portfolio at. Makes the paper equity ledger agree with the paper-entry alert.

READ-MODEL / accounting only. NEVER touches live, signal generation, tier, score, TP/SL, final_r or
signal_outcomes. It only decides, per signal, the paper `size_weight` ∈ {1.0, 0.5, 0.0}:

  FULL_SIZE → 1.0x · HALF_SIZE → 0.5x · SHADOW_ONLY / BLOCK → 0.0x (excluded from the actionable ledger)

Priority (most authoritative first):
  1. The ACTUAL paper_entry alert payload (what production really did at entry) — `cqo_quality_action`
     / `size_weight` / a non-actionable overlay status. Forward trades.
  2. The LOOKAHEAD-SAFE counterfactual reconstruction (`crypto_quality_counterfactual.overlay_action`)
     — the overlay decision as it WOULD have been at the trade's entry, rebuilt point-in-time. This is the
     honest way to size PRE-overlay historical crypto trades (no real-time alert existed).
  3. A POINT-IN-TIME overlay decision (`crypto_quality_overlay_decisions` with
     `decision_context_type='point_in_time'`). A CURRENT snapshot is NEVER used to size a trade.
  4. Legacy `actionable(asset, mode, tier)` — full-size if actionable, excluded otherwise.

Non-crypto (stocks/etc.) always uses legacy actionable() only — this resolver never resizes stocks.
"""
from __future__ import annotations

import json
from typing import Any

FULL_SIZE, HALF_SIZE, SHADOW_ONLY, BLOCK, NOT_ACTIONABLE = (
    "FULL_SIZE", "HALF_SIZE", "SHADOW_ONLY", "BLOCK", "NOT_ACTIONABLE")
_SIZE = {FULL_SIZE: 1.0, HALF_SIZE: 0.5, SHADOW_ONLY: 0.0, BLOCK: 0.0}
_SEV = {FULL_SIZE: 0, HALF_SIZE: 1, SHADOW_ONLY: 2, BLOCK: 3, NOT_ACTIONABLE: 3}
NON_ACTIONABLE_ALERT_STATUSES = {
    "shadow_only", "shadow_c_tier", "shadow_sector_cap", "shadow_stocks_context", "late_shadow",
    "shadow_llm_review", "shadow_crypto_quality", "blocked_crypto_quality", "shadow_risk_guard", "dry_run",
}
STOCKS_SWING_EVENT_RS_PROFILES = {
    "stocks_swing_event_rs_pullback_quality_paper_v1",
    "stocks_swing_event_rs_pullback_flow_paper_v1",
}


def _clamp01(v) -> float:
    try:
        return max(0.0, min(1.0, float(v)))
    except (TypeError, ValueError):
        return 1.0


def legacy_actionable(asset: str, mode: str, tier: str | None) -> bool:
    """The pre-overlay actionability rule (kept identical so nothing regresses)."""
    if (tier or "").upper() not in ("A", "B"):
        return False
    if asset == "crypto" and mode == "scalp":
        return False
    if asset == "stocks" and mode in ("swing", "invest"):
        return False
    return True


def _raw_signal_payload(signal: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(signal, dict):
        return {}
    raw = signal.get("raw_idea_json")
    if isinstance(raw, dict):
        return dict(raw)
    try:
        parsed = json.loads(raw or "{}")
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def _paper_profile(signal: dict[str, Any] | None) -> str:
    if not isinstance(signal, dict):
        return ""
    direct = str(signal.get("paper_entry_profile") or "").strip()
    if direct:
        return direct
    return str(_raw_signal_payload(signal).get("paper_entry_profile") or "").strip()


def _paper_size_weight(signal: dict[str, Any] | None) -> float:
    if not isinstance(signal, dict):
        return 1.0
    for value in (
        signal.get("paper_size_weight"),
        _raw_signal_payload(signal).get("paper_size_weight"),
        (_raw_signal_payload(signal).get("stock_swing_event_rs_pullback") or {}).get("size_weight")
        if isinstance(_raw_signal_payload(signal).get("stock_swing_event_rs_pullback"), dict) else None,
    ):
        if value is not None:
            return _clamp01(value)
    return 1.0


def _has(conn, t) -> bool:
    return bool(conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (t,)).fetchone())


def build_maps(conn) -> dict[str, dict]:
    """Preload the lookup maps once (avoids per-signal queries in the backfill loop)."""
    maps: dict[str, dict] = {"alerts": {}, "counterfactual": {}, "decisions": {}, "snapshots": {}}
    if _has(conn, "signal_alerts"):
        try:
            for sid, ts, pj in conn.execute(
                "SELECT signal_id, telegram_status, payload_json FROM signal_alerts "
                "WHERE alert_type='paper_entry' ORDER BY sent_at ASC"):     # ASC → last write = latest
                try:
                    payload = json.loads(pj) if pj else {}
                except Exception:
                    payload = {}
                maps["alerts"][sid] = (ts, payload)
        except Exception:
            pass
    if _has(conn, "crypto_quality_counterfactual"):
        try:
            for sid, act in conn.execute(
                "SELECT signal_id, overlay_action FROM crypto_quality_counterfactual"):
                maps["counterfactual"][sid] = act
        except Exception:
            pass
    if _has(conn, "crypto_quality_overlay_decisions"):
        try:
            cols = {r[1] for r in conn.execute("PRAGMA table_info(crypto_quality_overlay_decisions)")}
            hash_sql = "overlay_config_hash" if "overlay_config_hash" in cols else "NULL"
            for sid, act, ctx, cfg_hash in conn.execute(
                f"SELECT signal_id, quality_action, decision_context_type, {hash_sql} "
                "FROM crypto_quality_overlay_decisions"):
                maps["decisions"][sid] = (act, ctx, cfg_hash)
        except Exception:
            pass                              # column may be absent on a pre-migration table
    if _has(conn, "crypto_quality_overlay_decision_snapshots"):
        try:
            cols = {r[1] for r in conn.execute(
                "PRAGMA table_info(crypto_quality_overlay_decision_snapshots)")}
            hash_sql = "overlay_config_hash" if "overlay_config_hash" in cols else "NULL"
            for sid, act, cfg_hash in conn.execute(
                f"SELECT signal_id, quality_action, {hash_sql} "
                "FROM crypto_quality_overlay_decision_snapshots "
                "WHERE decision_context_type='point_in_time'"):
                maps["snapshots"][sid] = (act, cfg_hash)
        except Exception:
            pass
    return maps


def _apply_floor(base: dict[str, Any], floor_action: str | None, *, source_suffix: str,
                 reason: str) -> dict[str, Any]:
    if not floor_action:
        return base
    floor = str(floor_action)
    current = str(base.get("paper_action") or FULL_SIZE)
    if _SEV.get(floor, 0) <= _SEV.get(current, 0):
        return base
    out = dict(base)
    out["paper_action"] = floor
    out["size_weight"] = _SIZE.get(floor, 1.0)
    out["source"] = f"{base.get('source') or 'unknown'}+{source_suffix}"
    prev = str(base.get("reason") or "").strip()
    out["reason"] = f"{prev}; {reason}" if prev else reason
    return out


def _apply_crypto_swing_policy(conn, *, signal_id: str, asset_class: str, mode: str, tier: str | None,
                               base: dict[str, Any], signal: dict[str, Any] | None,
                               require_latency: bool | None) -> dict[str, Any]:
    try:
        from src.execution.crypto_swing_paper_policy import apply_main_paper_floor
        return apply_main_paper_floor(
            conn, signal_id=signal_id, asset_class=asset_class, mode=mode, tier=tier,
            base=base, signal=signal, require_latency=require_latency)
    except Exception:
        if str(asset_class or "crypto").lower() == "crypto" and str(mode or "").lower() == "swing":
            out = dict(base)
            out["paper_action"] = SHADOW_ONLY
            out["size_weight"] = 0.0
            out["source"] = f"{base.get('source') or 'unknown'}+crypto_swing_policy_error"
            prev = str(base.get("reason") or "").strip()
            err = "crypto swing main paper blocked: policy error"
            out["reason"] = f"{prev}; {err}" if prev else err
            return out
        return base


def resolve_paper_actionability(conn, signal_id: str, asset_class: str, mode: str, tier: str | None,
                                *, maps: dict | None = None, overlay_version: str = "cqo_v1",
                                apply_crypto_swing_policy: bool = True,
                                signal: dict[str, Any] | None = None,
                                require_crypto_swing_latency: bool | None = None) -> dict[str, Any]:
    asset = (asset_class or "crypto").lower()
    mode = (mode or "").lower()
    maps = maps if maps is not None else build_maps(conn)
    a = (maps.get("alerts") or {}).get(signal_id)
    if a and str(a[0] or "").lower() in NON_ACTIONABLE_ALERT_STATUSES:
        return {"paper_action": SHADOW_ONLY, "size_weight": 0.0,
                "source": "alert_status_non_actionable",
                "reason": f"paper alert status {str(a[0]).lower()} is non-actionable",
                "overlay_version": None,
                "overlay_config_hash": (a[1] or {}).get("cqo_overlay_config_hash")}

    if asset == "stocks" and mode == "swing" and _paper_profile(signal) in STOCKS_SWING_EVENT_RS_PROFILES:
        if (tier or "").upper() not in ("A", "B"):
            return {"paper_action": NOT_ACTIONABLE, "size_weight": 0.0,
                    "source": "stocks_swing_event_rs_profile",
                    "reason": "stock swing event-RS Paper profile requires A/B tier",
                    "overlay_version": None, "overlay_config_hash": None}
        sw = _paper_size_weight(signal)
        action = FULL_SIZE if sw >= 0.999 else HALF_SIZE if sw > 0 else NOT_ACTIONABLE
        return {"paper_action": action, "size_weight": sw,
                "source": "stocks_swing_event_rs_profile",
                "reason": "explicit stock swing event-RS Paper profile",
                "overlay_version": None, "overlay_config_hash": None}

    # Non-crypto: legacy only — never resize stocks/etc from the crypto overlay.
    if asset != "crypto" and a and (
        str(a[0] or "").lower() == "sent" or str(a[0] or "").lower().startswith("error:")
    ):
        # This is a point-in-time fact about a trade already accepted by Paper,
        # not a path to promote new signals. A later re-score must not erase it.
        return {"paper_action": FULL_SIZE, "size_weight": 1.0,
                "source": "paper_entry_alert_point_in_time",
                "reason": "paper entry alert recorded at entry time",
                "overlay_version": None, "overlay_config_hash": None}
    if asset != "crypto":
        ok = legacy_actionable(asset, mode, tier)
        return {"paper_action": FULL_SIZE if ok else NOT_ACTIONABLE, "size_weight": 1.0 if ok else 0.0,
                "source": "legacy_actionable_non_crypto", "reason": "non-crypto legacy actionability",
                "overlay_version": None, "overlay_config_hash": None}

    def finish(base: dict[str, Any]) -> dict[str, Any]:
        if apply_crypto_swing_policy and asset == "crypto" and mode == "swing":
            return _apply_crypto_swing_policy(
                conn, signal_id=signal_id, asset_class=asset, mode=mode, tier=tier,
                base=base, signal=signal, require_latency=require_crypto_swing_latency)
        return base

    # 1) actual paper_entry alert payload — what production really did (authoritative for forward trades).
    if a:
        ts, payload = a
        if isinstance(payload, dict) and ("cqo_quality_action" in payload or
                                          ts in {"shadow_crypto_quality", "blocked_crypto_quality"}):
            action = str(payload.get("cqo_quality_action") or "")
            if ts in {"shadow_crypto_quality", "blocked_crypto_quality"} or action in (SHADOW_ONLY, BLOCK):
                return finish({"paper_action": action or SHADOW_ONLY, "size_weight": 0.0, "source": "alert_payload",
                               "reason": (", ".join(payload.get("cqo_reasons") or [])[:200]
                                          or "crypto overlay shadow"),
                               "overlay_version": payload.get("cqo_overlay_version") or overlay_version,
                               "overlay_config_hash": payload.get("cqo_overlay_config_hash")})
            sw = payload.get("size_weight")
            sw = _clamp01(sw) if sw is not None else _SIZE.get(action, 1.0)
            if action == HALF_SIZE:
                sw = min(sw, _SIZE[HALF_SIZE])
            base = {"paper_action": action or FULL_SIZE, "size_weight": sw, "source": "alert_payload",
                    "reason": str(payload.get("size_reason") or action or "overlay full size"),
                    "overlay_version": payload.get("cqo_overlay_version") or overlay_version,
                    "overlay_config_hash": payload.get("cqo_overlay_config_hash")}
            dec = (maps.get("decisions") or {}).get(signal_id)
            if dec and str(dec[1]) == "point_in_time":
                return finish(_apply_floor(base, dec[0], source_suffix="overlay_floor",
                                           reason="point-in-time overlay risk floor"))
            return finish(base)

    snap = (maps.get("snapshots") or {}).get(signal_id)
    if snap:
        action = str(snap[0])
        return finish({"paper_action": action, "size_weight": _SIZE.get(action, 1.0),
                       "source": "overlay_snapshot_point_in_time",
                       "reason": "immutable entry-time overlay snapshot", "overlay_version": overlay_version,
                       "overlay_config_hash": snap[1]})

    # 2) lookahead-safe counterfactual reconstruction — the honest historical overlay decision.
    cf = (maps.get("counterfactual") or {}).get(signal_id)
    if cf:
        action = str(cf)
        return finish({"paper_action": action, "size_weight": _SIZE.get(action, 1.0),
                       "source": "counterfactual_lookahead_safe",
                       "reason": "overlay decision reconstructed lookahead-safe at entry",
                       "overlay_version": overlay_version, "overlay_config_hash": None})

    # 3) POINT-IN-TIME overlay decision only (a current snapshot is never used to size a trade).
    dec = (maps.get("decisions") or {}).get(signal_id)
    if dec and str(dec[1]) == "point_in_time":
        action = str(dec[0])
        return finish({"paper_action": action, "size_weight": _SIZE.get(action, 1.0),
                       "source": "overlay_decision_point_in_time", "reason": "point-in-time overlay decision",
                       "overlay_version": overlay_version, "overlay_config_hash": dec[2]})

    # 4) legacy actionable (no overlay decision available for this crypto signal).
    ok = legacy_actionable(asset, mode, tier)
    return finish({"paper_action": FULL_SIZE if ok else NOT_ACTIONABLE, "size_weight": 1.0 if ok else 0.0,
                   "source": "legacy_actionable", "reason": "no overlay decision; legacy actionability",
                   "overlay_version": None, "overlay_config_hash": None})


__all__ = ["resolve_paper_actionability", "build_maps", "legacy_actionable",
           "FULL_SIZE", "HALF_SIZE", "SHADOW_ONLY", "BLOCK", "NOT_ACTIONABLE",
           "NON_ACTIONABLE_ALERT_STATUSES"]
