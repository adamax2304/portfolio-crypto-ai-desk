"""Crypto swing production-paper policy.

Versioned Paper/Shadow policy for crypto swing. The active Paper profile is
explicitly configured; counterfactual alternatives remain isolated Shadow
profiles. The live canary has an independent, version-pinned allowlist and is
never enabled by this module.

This module never places orders and never writes source trading tables. It is a
policy/read-model helper shared by signal creation, paper actionability, alerts,
and research reports.
"""
from __future__ import annotations

import ast
import json
import sqlite3
from copy import deepcopy
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[2]

FULL_SIZE = "FULL_SIZE"
HALF_SIZE = "HALF_SIZE"
SHADOW_ONLY = "SHADOW_ONLY"
BLOCK = "BLOCK"
NOT_ACTIONABLE = "NOT_ACTIONABLE"

DEFAULT_CFG: dict[str, Any] = {
    "enabled": True,
    "live_enabled": False,
    "canonical_target_override_enabled": True,
    "main_paper_enforcement_enabled": False,
    "production_profile": {
        "name": "production_t130_targets",
        "version": "crypto_swing_paper_t130_v1",
        "target_multipliers": [1.30, 2.30, 3.60],
    },
    "breakout_paper_experiment": {
        "enabled": False,
        "experiment_id": "crypto_swing_breakout_paper_experiment_v1",
        "entry_mode": "BREAKOUT_CONTINUATION",
        "size_weight": 0.5,
        "require_latency_audit": True,
        "reject_latency_causes": ["DATA_GAP_LATE", "DATA_GAP", "DETECTION_LATENCY", "NO_DATA"],
    },
    "shadow_profiles": {
        "target_t140": {
            "version": "crypto_swing_shadow_t140_v2",
            "target_multipliers": [1.40, 2.40, 3.80],
        },
        "target_t130": {
            "version": "crypto_swing_shadow_t130_v2",
            "target_multipliers": [1.30, 2.30, 3.60],
        },
        "allow_half_size": {"version": "crypto_swing_shadow_t140_allow_half_v2"},
        "allow_no_overlay": {"version": "crypto_swing_shadow_t140_no_overlay_v2"},
    },
}


def load_cfg() -> dict[str, Any]:
    path = ROOT / "config" / "crypto_swing_paper_policy.yaml"
    if yaml and path.exists():
        try:
            with open(path, "r", encoding="utf-8") as fh:
                user = (yaml.safe_load(fh) or {}).get("crypto_swing_paper_policy") or {}
            cfg = deepcopy(DEFAULT_CFG)
            for k, v in user.items():
                if isinstance(v, dict) and isinstance(cfg.get(k), dict):
                    cfg[k].update(v)
                else:
                    cfg[k] = v
            return cfg
        except Exception:
            pass
    return deepcopy(DEFAULT_CFG)


def is_crypto_swing(asset_class: Any, mode: Any) -> bool:
    return str(asset_class or "crypto").lower() == "crypto" and str(mode or "").lower() == "swing"


def _f(v: Any) -> float | None:
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return None


def _raw_setup(raw_json: Any) -> dict[str, Any]:
    if isinstance(raw_json, dict):
        obj = raw_json
    else:
        try:
            obj = json.loads(raw_json or "{}")
        except Exception:
            return {}
    setup = obj.get("raw_setup") or obj.get("setup") or {}
    if isinstance(setup, str):
        try:
            setup = ast.literal_eval(setup)
        except Exception:
            setup = {}
    return setup if isinstance(setup, dict) else {}


def _infer_ref_close_atr(signal: dict[str, Any]) -> tuple[float | None, float | None, str]:
    setup = _raw_setup(signal.get("raw_idea_json"))
    atr = _f(setup.get("atr"))
    close = _f(setup.get("current_price"))
    if atr is not None and close is not None and atr > 0:
        return close, atr, "raw_setup"

    direction = str(signal.get("direction") or "long").lower()
    sign = -1.0 if direction == "short" else 1.0
    tp1, tp2 = _f(signal.get("tp1")), _f(signal.get("tp2"))
    if tp1 is not None and tp2 is not None:
        inferred_atr = abs(tp2 - tp1)
        if inferred_atr > 0:
            inferred_close = tp1 - sign * inferred_atr
            return inferred_close, inferred_atr, "inferred_from_existing_targets"
    return None, None, "missing_ref_close_or_atr"


def target_profile(signal: dict[str, Any], *, profile: str = "production",
                   cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = cfg or load_cfg()
    if profile == "production":
        pcfg = cfg.get("production_profile") or {}
    else:
        pcfg = ((cfg.get("shadow_profiles") or {}).get(profile) or {})
    multipliers = [float(x) for x in (pcfg.get("target_multipliers") or [])]
    if len(multipliers) != 3:
        return {"available": False, "status": "missing_target_multipliers", "profile": profile}
    close, atr, source = _infer_ref_close_atr(signal)
    if close is None or atr is None or atr <= 0:
        return {"available": False, "status": source, "profile": profile,
                "version": pcfg.get("version"), "target_multipliers": multipliers}
    sign = -1.0 if str(signal.get("direction") or "long").lower() == "short" else 1.0
    targets = [round(close + sign * m * atr, 8) for m in multipliers]
    return {
        "available": True,
        "status": "ok",
        "profile": profile,
        "version": pcfg.get("version"),
        "target_multipliers": multipliers,
        "ref_close": close,
        "atr": atr,
        "source": source,
        "tp1": targets[0],
        "tp2": targets[1],
        "tp3": targets[2],
    }


def targets_match_profile(signal: dict[str, Any], profile: dict[str, Any], *, rel_tol: float = 1e-6) -> bool:
    if not profile.get("available"):
        return False
    for key in ("tp1", "tp2", "tp3"):
        have = _f(signal.get(key))
        want = _f(profile.get(key))
        if have is None or want is None:
            return False
        tol = max(abs(want) * rel_tol, 1e-8)
        if abs(have - want) > tol:
            return False
    return True


def apply_target_profile_to_setup(setup: dict[str, Any], *, direction: str,
                                  profile: str = "production",
                                  cfg: dict[str, Any] | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return a setup copy with the configured Paper profile when enabled."""
    cfg = cfg or load_cfg()
    sig = {"raw_idea_json": {"raw_setup": setup}, "direction": direction,
           "tp1": setup.get("tp1"), "tp2": setup.get("tp2"), "tp3": setup.get("tp3")}
    prof = target_profile(sig, profile=profile, cfg=cfg)
    out = dict(setup)
    if (cfg.get("enabled", True) and cfg.get("canonical_target_override_enabled", False)
            and prof.get("available")):
        out["tp1"], out["tp2"], out["tp3"] = prof["tp1"], prof["tp2"], prof["tp3"]
        out["paper_target_profile_version"] = prof.get("version")
        out["paper_target_multipliers"] = prof.get("target_multipliers")
    return out, prof


def fetch_signal(conn: sqlite3.Connection, signal_id: str) -> dict[str, Any] | None:
    try:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM proposed_signals WHERE signal_id=?", (signal_id,)).fetchone()
        return dict(row) if row else None
    except Exception:
        return None


def latency_gate(conn: sqlite3.Connection | None, signal_id: str, *,
                 cfg: dict[str, Any] | None = None, require_row: bool | None = None,
                 gate_cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = cfg or load_cfg()
    pcfg = gate_cfg or cfg.get("production_profile") or {}
    max_gap = _f(pcfg.get("max_data_gap_min"))
    reject_causes = {str(x).upper() for x in (pcfg.get("reject_latency_causes") or [])}
    if require_row is None:
        require_row = bool(pcfg.get("require_latency_audit", True))
    if conn is None:
        return {"clean": not require_row, "cause": "NO_LATENCY_CONNECTION",
                "reason": "latency audit unavailable"}
    try:
        has_table = bool(conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='entry_latency_audit'"
        ).fetchone())
        if not has_table:
            return {"clean": not require_row, "cause": "NO_LATENCY_TABLE",
                    "reason": "entry_latency_audit table missing"}
        row = conn.execute("SELECT * FROM entry_latency_audit WHERE signal_id=?", (signal_id,)).fetchone()
    except Exception as exc:
        return {"clean": not require_row, "cause": "LATENCY_AUDIT_ERROR",
                "reason": f"latency audit error: {type(exc).__name__}"}
    if not row:
        return {"clean": not require_row, "cause": "NO_LATENCY_ROW",
                "reason": "entry_latency_audit row missing"}
    d = dict(row)
    cause = str(d.get("cause") or "").upper()
    gap = _f(d.get("data_gap_min"))
    if cause in reject_causes:
        return {"clean": False, "cause": cause, "data_gap_min": gap,
                "reason": f"latency cause rejected: {cause}"}
    if max_gap is not None and gap is not None and gap > max_gap:
        return {"clean": False, "cause": cause or "DATA_GAP_TOO_LARGE", "data_gap_min": gap,
                "reason": f"data_gap_min {gap} > {max_gap}"}
    return {"clean": True, "cause": cause or "OK", "data_gap_min": gap, "reason": "clean latency audit"}


def _entry_mode(conn: sqlite3.Connection | None, signal_id: str, signal: dict[str, Any] | None) -> str:
    """Use the stored entry-time classifier; never infer membership from later candles."""
    if conn is not None:
        try:
            row = conn.execute(
                "SELECT entry_mode FROM signal_entry_mode WHERE signal_id=?", (signal_id,)
            ).fetchone()
            if row and row[0]:
                return str(row[0]).upper()
        except Exception:
            pass
    return str((signal or {}).get("paper_execution_entry_mode") or "").upper()


def apply_breakout_paper_experiment(conn: sqlite3.Connection | None, *, signal_id: str,
                                    asset_class: Any, mode: Any, base: dict[str, Any],
                                    signal: dict[str, Any] | None = None,
                                    cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    """Cap one clean swing-breakout cohort without expanding the Paper entry universe."""
    cfg = cfg or load_cfg()
    exp = cfg.get("breakout_paper_experiment") or {}
    out = dict(base)
    if (not exp.get("enabled", False) or not is_crypto_swing(asset_class, mode)
            or _entry_mode(conn, signal_id, signal) != str(exp.get("entry_mode") or "").upper()):
        out["crypto_swing_breakout_experiment_applied"] = False
        return out

    action = str(out.get("paper_action") or "").upper()
    size = _f(out.get("size_weight"))
    if action not in (FULL_SIZE, HALF_SIZE) or size is None or size <= 0:
        out["crypto_swing_breakout_experiment_applied"] = False
        return out

    lat = latency_gate(
        conn, signal_id, cfg=cfg, gate_cfg=exp,
        require_row=bool(exp.get("require_latency_audit", True)),
    )
    exp_id = str(exp.get("experiment_id") or "crypto_swing_breakout_paper_experiment_v1")
    out["crypto_swing_breakout_experiment_id"] = exp_id
    out["crypto_swing_breakout_latency_cause"] = lat.get("cause")
    out["crypto_swing_breakout_experiment_applied"] = True
    if not lat.get("clean"):
        out["paper_action"] = SHADOW_ONLY
        out["size_weight"] = 0.0
        out["source"] = f"{out.get('source') or 'unknown'}+crypto_swing_breakout_experiment"
        previous = str(out.get("reason") or "").strip()
        add = f"breakout Paper experiment blocked: {lat.get('reason') or 'latency not clean'}"
        out["reason"] = f"{previous}; {add}" if previous else add
        return out

    weight = _f(exp.get("size_weight"))
    weight = 0.5 if weight is None else max(0.0, min(1.0, weight))
    out["paper_action"] = HALF_SIZE
    out["size_weight"] = min(size, weight)
    out["source"] = f"{out.get('source') or 'unknown'}+crypto_swing_breakout_experiment"
    previous = str(out.get("reason") or "").strip()
    add = f"breakout Paper experiment {exp_id}: clean latency, capped at {out['size_weight']:g}x"
    out["reason"] = f"{previous}; {add}" if previous else add
    return out


def _reason_has_rejected_substring(text: str, cfg: dict[str, Any]) -> str | None:
    low = (text or "").lower()
    for frag in ((cfg.get("production_profile") or {}).get("reject_reason_substrings") or []):
        frag_s = str(frag).lower()
        if frag_s and frag_s in low:
            return frag_s
    return None


def apply_main_paper_floor(conn: sqlite3.Connection | None, *, signal_id: str,
                           asset_class: Any, mode: Any, tier: Any,
                           base: dict[str, Any], signal: dict[str, Any] | None = None,
                           cfg: dict[str, Any] | None = None,
                           require_latency: bool | None = None,
                           extra_reasons: list[str] | None = None) -> dict[str, Any]:
    """Downgrade crypto swing to shadow unless it matches the strict main lane."""
    cfg = cfg or load_cfg()
    out = dict(base)
    if (not cfg.get("enabled", True) or not cfg.get("main_paper_enforcement_enabled", False)
            or not is_crypto_swing(asset_class, mode)):
        out["crypto_swing_main_policy_applied"] = False
        return apply_breakout_paper_experiment(
            conn, signal_id=signal_id, asset_class=asset_class, mode=mode,
            base=out, signal=signal, cfg=cfg,
        )
    out["crypto_swing_main_policy_applied"] = True
    rejects: list[str] = []
    pcfg = cfg.get("production_profile") or {}
    required_action = str(pcfg.get("require_overlay_action") or FULL_SIZE)
    action = str(out.get("paper_action") or "")
    size = _f(out.get("size_weight"))
    source = str(out.get("source") or "")
    reason_text = " ".join([str(out.get("reason") or ""), " ".join(extra_reasons or [])])

    if source.startswith("legacy_actionable") or source == "legacy_actionable":
        rejects.append("NO_OVERLAY is not allowed for crypto swing production-paper")
    if action != required_action or (size is not None and size < 1.0):
        rejects.append(f"overlay action {action or 'UNKNOWN'} is not {required_action}")
    bad_reason = _reason_has_rejected_substring(reason_text, cfg)
    if bad_reason:
        rejects.append(f"overlay reason contains rejected marker: {bad_reason}")

    sig = signal or (fetch_signal(conn, signal_id) if conn is not None else None)
    prof = target_profile(sig or {}, profile="production", cfg=cfg)
    if not prof.get("available"):
        rejects.append(f"production target profile unavailable: {prof.get('status')}")
    elif sig is not None and not targets_match_profile(sig, prof):
        rejects.append("signal targets do not match production target profile")

    lat = latency_gate(conn, signal_id, cfg=cfg, require_row=require_latency)
    if not lat.get("clean"):
        rejects.append(lat.get("reason") or "latency not clean")

    out["crypto_swing_policy_profile"] = pcfg.get("name")
    out["crypto_swing_policy_version"] = pcfg.get("version")
    out["crypto_swing_target_multipliers"] = json.dumps(pcfg.get("target_multipliers") or [])
    out["crypto_swing_latency_cause"] = lat.get("cause")
    out["crypto_swing_clean_for_main_paper"] = int(not rejects)

    if not rejects:
        out["source"] = f"{source or 'unknown'}+crypto_swing_main_policy"
        prev = str(out.get("reason") or "").strip()
        add = f"crypto swing main paper: {pcfg.get('name')} clean FULL_SIZE"
        out["reason"] = f"{prev}; {add}" if prev else add
        return apply_breakout_paper_experiment(
            conn, signal_id=signal_id, asset_class=asset_class, mode=mode,
            base=out, signal=signal, cfg=cfg,
        )

    out["paper_action"] = SHADOW_ONLY
    out["size_weight"] = 0.0
    out["source"] = f"{source or 'unknown'}+crypto_swing_main_policy"
    prev = str(out.get("reason") or "").strip()
    add = "crypto swing main paper blocked: " + "; ".join(rejects)
    out["reason"] = f"{prev}; {add}" if prev else add
    return apply_breakout_paper_experiment(
        conn, signal_id=signal_id, asset_class=asset_class, mode=mode,
        base=out, signal=signal, cfg=cfg,
    )


__all__ = [
    "FULL_SIZE", "HALF_SIZE", "SHADOW_ONLY", "BLOCK", "NOT_ACTIONABLE",
    "load_cfg", "is_crypto_swing", "target_profile", "apply_target_profile_to_setup",
    "targets_match_profile", "latency_gate", "apply_breakout_paper_experiment",
    "apply_main_paper_floor", "fetch_signal",
]
