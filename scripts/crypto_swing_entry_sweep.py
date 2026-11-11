"""Read-only crypto swing entry-geometry sweep.

Replays existing crypto swing paper trades on the same cached OHLCV with the
same Model-F protection/cost model, varying only entry geometry/gates. It writes
only a markdown report under reports/; no DB writes, no live, no final_r.
"""
from __future__ import annotations

import argparse
import ast
import json
import math
import random
import sqlite3
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import load_config
from src.execution import paper_portfolio
from src.execution.crypto_swing_paper_policy import load_cfg as load_swing_policy_cfg
from src.execution import profit_protection as pp
from src.execution.paper_shadow_engine import _load_candles
from src.backtest.settings_replay import load_deep_candles
from src.execution.shadow_strategy_common import normalize_frame, parse_dt, simulate_confirmed_close_entry
from src.storage.file_store import FileStore


REPORT = ROOT / "reports" / "CRYPTO_SWING_ENTRY_SWEEP.md"
BREAKOUT_REPORT = ROOT / "reports" / "CRYPTO_SWING_BREAKOUT_REFINEMENTS.md"
_SWING_POLICY = load_swing_policy_cfg()
_SHADOW_PROFILES = _SWING_POLICY.get("shadow_profiles") or {}


def _profile_meta(name: str, fallback_version: str, fallback_targets: list[float]) -> tuple[str, list[float]]:
    profile = _SHADOW_PROFILES.get(name) or {}
    return str(profile.get("version") or fallback_version), [float(x) for x in (
        profile.get("target_multipliers") or fallback_targets)]


POLICY_VARIANTS = {
    "shadow_legacy_full_clean": ("crypto_swing_shadow_legacy_control_v1", []),
    "shadow_t140_full_clean": _profile_meta("target_t140", "crypto_swing_shadow_t140_v2", [1.40, 2.40, 3.80]),
    "shadow_t130_full_clean": _profile_meta("target_t130", "crypto_swing_shadow_t130_v2", [1.30, 2.30, 3.60]),
    "shadow_t140_allow_half_size": _profile_meta("allow_half_size", "crypto_swing_shadow_t140_allow_half_v2", [1.40, 2.40, 3.80]),
    "shadow_t140_no_overlay_clean": _profile_meta("allow_no_overlay", "crypto_swing_shadow_t140_no_overlay_v2", [1.40, 2.40, 3.80]),
}
_CF_DDL = """
CREATE TABLE IF NOT EXISTS crypto_swing_paper_counterfactual (
  signal_id TEXT,
  variant TEXT,
  profile_version TEXT,
  target_multipliers_json TEXT,
  symbol TEXT,
  direction TEXT,
  created_at TEXT,
  quality_action TEXT,
  latency_cause TEXT,
  data_gap_min REAL,
  entered INTEGER,
  skipped INTEGER,
  close_reason TEXT,
  net_pnl_usd REAL,
  delta_vs_current_usd REAL,
  computed_at TEXT,
  version TEXT,
  snapshot_id TEXT,
  is_current_snapshot INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (signal_id, variant)
);
"""


def _f(v: Any) -> float | None:
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return None


def _dt(v: Any) -> pd.Timestamp | None:
    if not v:
        return None
    try:
        return pd.to_datetime(v, utc=True)
    except Exception:
        return None


def _raw_setup(raw_json: str | None) -> dict[str, Any]:
    try:
        obj = json.loads(raw_json or "{}")
    except Exception:
        return {}
    setup = obj.get("raw_setup") or {}
    if isinstance(setup, str):
        try:
            setup = ast.literal_eval(setup)
        except Exception:
            setup = {}
    return setup if isinstance(setup, dict) else {}


def _quality_reasons(row: dict[str, Any]) -> str:
    return str(row.get("quality_reasons_json") or "")


def _quality_action(row: dict[str, Any]) -> str:
    return str(row.get("quality_action") or "NO_OVERLAY")


def _side(row: dict[str, Any]) -> bool:
    return str(row.get("direction") or "long").lower() != "short"


@dataclass
class Variant:
    name: str
    mutate: Callable[[dict[str, Any]], dict[str, Any] | None]


def _rr_from_fill_edge(g: dict[str, Any]) -> float | None:
    long = _side(g)
    entry = g.get("entry_high") if long else g.get("entry_low")
    stop = g.get("stop")
    tp1 = g.get("tp1")
    if entry is None or stop is None or tp1 is None or abs(entry - stop) <= 0:
        return None
    return abs(tp1 - entry) / abs(entry - stop)


def _set_zone_from_atr(g: dict[str, Any], near: float, far: float) -> dict[str, Any] | None:
    atr, close = g.get("atr"), g.get("ref_close")
    if atr is None or close is None or atr <= 0:
        return None
    out = dict(g)
    if _side(g):
        out["entry_high"] = close - near * atr
        out["entry_low"] = close - far * atr
    else:
        out["entry_low"] = close + near * atr
        out["entry_high"] = close + far * atr
    return out


def _set_stop_from_close(g: dict[str, Any], mult: float) -> dict[str, Any] | None:
    atr, close = g.get("atr"), g.get("ref_close")
    if atr is None or close is None or atr <= 0:
        return None
    out = dict(g)
    out["stop"] = close - mult * atr if _side(g) else close + mult * atr
    return out


def _set_targets_from_close(g: dict[str, Any], tp1: float, tp2: float, tp3: float) -> dict[str, Any] | None:
    atr, close = g.get("atr"), g.get("ref_close")
    if atr is None or close is None or atr <= 0:
        return None
    out = dict(g)
    s = 1 if _side(g) else -1
    out["tp1"] = close + s * tp1 * atr
    out["tp2"] = close + s * tp2 * atr
    out["tp3"] = close + s * tp3 * atr
    return out


def _skip_if(pred: Callable[[dict[str, Any]], bool]) -> Callable[[dict[str, Any]], dict[str, Any] | None]:
    def inner(g: dict[str, Any]) -> dict[str, Any] | None:
        out = dict(g)
        out["force_skip"] = bool(pred(g))
        return out
    return inner


def _clean_latency(g: dict[str, Any]) -> bool:
    cause = str(g.get("latency_cause") or "").upper()
    gap = g.get("data_gap_min")
    if cause in {"DATA_GAP_LATE", "LEGITIMATE_LATE", "NO_DATA", "NO_AUDIT"}:
        return False
    return gap is not None and gap <= 60


def _no_symbol_cooldown(g: dict[str, Any]) -> bool:
    return "symbol_cooldown" not in _quality_reasons(g).lower()


def _production_clean_full(g: dict[str, Any]) -> bool:
    return _quality_action(g) == "FULL_SIZE" and _clean_latency(g) and _no_symbol_cooldown(g)


def _set_weight(g: dict[str, Any], weight: float) -> dict[str, Any]:
    out = dict(g)
    out["size_weight"] = float(weight)
    return out


def _shadow_legacy_full_clean(g: dict[str, Any]) -> dict[str, Any] | None:
    if not _production_clean_full(g):
        out = dict(g)
        out["force_skip"] = True
        return out
    return dict(g)


def _shadow_t140(g: dict[str, Any]) -> dict[str, Any] | None:
    if not _production_clean_full(g):
        out = dict(g)
        out["force_skip"] = True
        return out
    return _set_targets_from_close(g, 1.40, 2.40, 3.80)


def _shadow_t130(g: dict[str, Any]) -> dict[str, Any] | None:
    if not _production_clean_full(g):
        out = dict(g)
        out["force_skip"] = True
        return out
    return _set_targets_from_close(g, 1.30, 2.30, 3.60)


def _shadow_allow_half(g: dict[str, Any]) -> dict[str, Any] | None:
    action = _quality_action(g)
    if action not in {"FULL_SIZE", "HALF_SIZE"} or not _clean_latency(g) or not _no_symbol_cooldown(g):
        out = dict(g)
        out["force_skip"] = True
        return out
    out = _set_targets_from_close(g, 1.40, 2.40, 3.80)
    if out is not None and action == "HALF_SIZE":
        out = _set_weight(out, 0.5)
    return out


def _shadow_no_overlay(g: dict[str, Any]) -> dict[str, Any] | None:
    # A real no-overlay counterfactual: preserve the clean-data requirement but
    # ignore every overlay action and overlay-derived cooldown.
    if not _clean_latency(g):
        out = dict(g)
        out["force_skip"] = True
        return out
    return _set_targets_from_close(g, 1.40, 2.40, 3.80)


VARIANTS: list[Variant] = [
    Variant("current", lambda g: dict(g)),
    Variant("zone_0.25_0.70atr", lambda g: _set_zone_from_atr(g, 0.25, 0.70)),
    Variant("zone_0.30_0.75atr", lambda g: _set_zone_from_atr(g, 0.30, 0.75)),
    Variant("zone_0.35_0.80atr", lambda g: _set_zone_from_atr(g, 0.35, 0.80)),
    Variant("zone_0.40_0.90atr", lambda g: _set_zone_from_atr(g, 0.40, 0.90)),
    Variant("zone_0.45_0.95atr", lambda g: _set_zone_from_atr(g, 0.45, 0.95)),
    Variant("zone_0.50_1.10atr", lambda g: _set_zone_from_atr(g, 0.50, 1.10)),
    Variant("zone_0.55_1.05atr", lambda g: _set_zone_from_atr(g, 0.55, 1.05)),
    Variant("zone_0.20_0.80atr_wide", lambda g: _set_zone_from_atr(g, 0.20, 0.80)),
    Variant("stop_0.85atr_from_close", lambda g: _set_stop_from_close(g, 0.85)),
    Variant("stop_1.00atr_from_close", lambda g: _set_stop_from_close(g, 1.00)),
    Variant("stop_1.10atr_from_close", lambda g: _set_stop_from_close(g, 1.10)),
    Variant("stop_1.20atr_from_close", lambda g: _set_stop_from_close(g, 1.20)),
    Variant("stop_1.40atr_from_close", lambda g: _set_stop_from_close(g, 1.40)),
    Variant("stop_1.60atr_from_close", lambda g: _set_stop_from_close(g, 1.60)),
    Variant("targets_1.10_2.10_3.25atr", lambda g: _set_targets_from_close(g, 1.10, 2.10, 3.25)),
    Variant("targets_1.20_2.20_3.40atr", lambda g: _set_targets_from_close(g, 1.20, 2.20, 3.40)),
    Variant("targets_1.25_2.25_3.50atr", lambda g: _set_targets_from_close(g, 1.25, 2.25, 3.50)),
    Variant("targets_1.30_2.30_3.60atr", lambda g: _set_targets_from_close(g, 1.30, 2.30, 3.60)),
    Variant("targets_1.40_2.40_3.80atr", lambda g: _set_targets_from_close(g, 1.40, 2.40, 3.80)),
    Variant("targets_1.50_2.50_4.00atr", lambda g: _set_targets_from_close(g, 1.50, 2.50, 4.00)),
    Variant("shadow_legacy_full_clean", _shadow_legacy_full_clean),
    Variant("shadow_t140_full_clean", _shadow_t140),
    Variant("shadow_t130_full_clean", _shadow_t130),
    Variant("shadow_t140_allow_half_size", _shadow_allow_half),
    Variant("shadow_t140_no_overlay_clean", _shadow_no_overlay),
    Variant("gate_rr_edge_ge_1.10", _skip_if(lambda g: (_rr_from_fill_edge(g) or 0) < 1.10)),
    Variant("gate_rr_edge_ge_1.20", _skip_if(lambda g: (_rr_from_fill_edge(g) or 0) < 1.20)),
    Variant("gate_rr_edge_ge_1.30", _skip_if(lambda g: (_rr_from_fill_edge(g) or 0) < 1.30)),
    Variant("gate_overlay_full_only", _skip_if(lambda g: g.get("quality_action") != "FULL_SIZE")),
    Variant("gate_no_symbol_cooldown", _skip_if(lambda g: "symbol_cooldown" in _quality_reasons(g))),
    Variant("gate_clean_latency_no_gap_gt30", _skip_if(lambda g: (g.get("data_gap_min") is not None and g["data_gap_min"] > 30))),
    Variant("gate_clean_latency_no_gap_gt60", _skip_if(lambda g: (g.get("data_gap_min") is not None and g["data_gap_min"] > 60))),
    Variant("gate_clean_latency_no_gap_gt120", _skip_if(lambda g: (g.get("data_gap_min") is not None and g["data_gap_min"] > 120))),
    Variant("gate_score_ge_60", _skip_if(lambda g: (g.get("score") or 0) < 60)),
    Variant("gate_score_ge_65", _skip_if(lambda g: (g.get("score") or 0) < 65)),
    Variant("gate_score_ge_70", _skip_if(lambda g: (g.get("score") or 0) < 70)),
    Variant("gate_score_ge_75", _skip_if(lambda g: (g.get("score") or 0) < 75)),
    Variant("gate_score_ge_80", _skip_if(lambda g: (g.get("score") or 0) < 80)),
    Variant("combo_targets_1.25_no_cooldown", lambda g: (
        None if "symbol_cooldown" in _quality_reasons(g) else _set_targets_from_close(g, 1.25, 2.25, 3.50)
    )),
    Variant("combo_targets_1.25_score65", lambda g: (
        None if (g.get("score") or 0) < 65 else _set_targets_from_close(g, 1.25, 2.25, 3.50)
    )),
    Variant("combo_targets_1.25_clean60", lambda g: (
        None if (g.get("data_gap_min") is not None and g["data_gap_min"] > 60)
        else _set_targets_from_close(g, 1.25, 2.25, 3.50)
    )),
    Variant(
        "combo_full_no_cooldown_rr1.2_clean",
        _skip_if(lambda g: (
            g.get("quality_action") != "FULL_SIZE"
            or "symbol_cooldown" in _quality_reasons(g)
            or (_rr_from_fill_edge(g) or 0) < 1.20
            or (g.get("data_gap_min") is not None and g["data_gap_min"] > 60)
        )),
    ),
    Variant("combo_zone_0.40_0.90_rr1.2", lambda g: (
        None if (_rr_from_fill_edge(_set_zone_from_atr(g, 0.40, 0.90) or {}) or 0) < 1.20
        else _set_zone_from_atr(g, 0.40, 0.90)
    )),
]


def _load_rows(conn: sqlite3.Connection, fee_profile: str) -> list[dict[str, Any]]:
    sql = """
    WITH latest AS (
      SELECT *, ROW_NUMBER() OVER (PARTITION BY signal_id ORDER BY checked_at DESC, id DESC) rn
      FROM signal_outcomes
    )
    SELECT p.signal_id, p.symbol, p.direction, p.mode, p.asset_class, p.exchange_focus, p.created_at,
           p.expires_at, p.score, p.entry_low, p.entry_high, p.entry_trigger, p.suggested_entry,
           COALESCE(p.invalidation, p.stop_loss) AS stop, p.tp1, p.tp2, p.tp3,
           p.raw_idea_json, l.net_pnl_usdt AS ledger_net_usd, l.close_reason AS ledger_close_reason,
           COALESCE(cf.overlay_action, q.quality_action, 'NO_OVERLAY') AS quality_action,
           COALESCE(cf.quality_reasons_json, q.quality_reasons_json, '') AS quality_reasons_json,
           e.cause AS latency_cause,
           e.recorded_latency_min, e.data_gap_min
    FROM latest o
    JOIN proposed_signals p ON p.signal_id = o.signal_id
    LEFT JOIN paper_portfolio_ledger l
      ON l.signal_id = p.signal_id AND l.fee_profile=? AND l.event_type='exit'
    LEFT JOIN crypto_quality_counterfactual cf ON cf.signal_id = p.signal_id
    LEFT JOIN crypto_quality_overlay_decisions q
      ON q.signal_id = p.signal_id AND q.decision_context_type = 'point_in_time'
    LEFT JOIN entry_latency_audit e ON e.signal_id = p.signal_id
    WHERE o.rn=1 AND o.entry_triggered=1
      AND p.asset_class='crypto' AND p.mode='swing'
    ORDER BY p.created_at
    """
    return [dict(r) for r in conn.execute(sql, (fee_profile,))]


def _load_forward_breakout_rows(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """Load only the new pre-entry-v2 forward breakout cohort.

    This deliberately does not reuse the broad swing target sweep's historical
    ledger sample: the refinement report is a separate forward-only Shadow
    experiment and treats data gaps as non-evidence.
    """
    sql = """
      SELECT DISTINCT p.signal_id, p.symbol, p.direction, p.mode, p.asset_class, p.exchange_focus,
             p.created_at, p.expires_at, p.score, p.entry_low, p.entry_high, p.entry_trigger,
             p.suggested_entry, COALESCE(p.invalidation, p.stop_loss) AS stop,
             p.tp1, p.tp2, p.tp3, p.raw_idea_json,
             pre.data_quality AS preentry_data_quality, lat.cause AS latency_cause,
             lat.recorded_latency_min, lat.data_gap_min, snap.decision_json
      FROM paper_shadow_execution_outcomes sh
      JOIN proposed_signals p ON p.signal_id=sh.signal_id
      JOIN signal_entry_mode_preentry pre ON pre.signal_id=p.signal_id
      LEFT JOIN entry_latency_audit lat ON lat.signal_id=p.signal_id
      LEFT JOIN crypto_quality_overlay_decision_snapshots snap
        ON snap.signal_id=p.signal_id AND snap.decision_context_type='point_in_time'
      WHERE sh.branch='new_logic_shadow' AND sh.window='forward_since_activation'
        AND sh.entry_mode='BREAKOUT_CONTINUATION' AND sh.entry_mode_version='preentry_v2'
        AND lower(COALESCE(p.asset_class,''))='crypto' AND lower(COALESCE(p.mode,''))='swing'
        AND lower(COALESCE(pre.data_quality,''))='ok'
      ORDER BY p.created_at
    """
    rows = [dict(r) for r in conn.execute(sql).fetchall()]
    for row in rows:
        try:
            row["snapshot"] = json.loads(row.get("decision_json") or "{}")
        except (TypeError, ValueError):
            row["snapshot"] = {}
    return rows


def _geom(row: dict[str, Any]) -> dict[str, Any] | None:
    setup = _raw_setup(row.get("raw_idea_json"))
    atr = _f(setup.get("atr"))
    close = _f(setup.get("current_price"))
    # Conservative fallback to the existing production geometry.
    if atr is None or close is None:
        long = _side(row)
        hi, lo = _f(row.get("entry_high")), _f(row.get("entry_low"))
        if hi is not None and lo is not None:
            atr = abs(hi - lo) / 0.45 if abs(hi - lo) > 0 else None
            close = (hi + 0.20 * atr) if long and atr else (lo - 0.20 * atr if atr else None)
    required = ["entry_low", "entry_high", "stop", "tp1", "tp2", "tp3"]
    g = {
        **row,
        "entry_low": _f(row.get("entry_low")),
        "entry_high": _f(row.get("entry_high")),
        "entry_trigger": _f(row.get("entry_trigger")),
        "suggested_entry": _f(row.get("suggested_entry")),
        "stop": _f(row.get("stop")),
        "tp1": _f(row.get("tp1")),
        "tp2": _f(row.get("tp2")),
        "tp3": _f(row.get("tp3")),
        "atr": atr,
        "ref_close": close,
        "entry_mode": "PULLBACK_LIMIT",
    }
    return None if any(g.get(k) is None for k in required) else g


def _clip_to_expiry(candles: pd.DataFrame, expires_at: str | None) -> pd.DataFrame:
    exp = _dt(expires_at)
    if exp is None or candles is None or candles.empty or "timestamp" not in candles.columns:
        return candles
    out = candles[pd.to_datetime(candles["timestamp"], utc=True) <= exp].copy()
    return out.reset_index(drop=True)


def _simulate(g: dict[str, Any], candles: pd.DataFrame, fee_profile: str) -> dict[str, Any]:
    if g.get("force_skip"):
        return {"entered": False, "skipped": True, "skip_reason": "gate_skip", "net_usd": 0.0,
                "net_r": 0.0, "close_reason": "gate_skip", "tp3_runner": False}
    res = pp.simulate_from_geometry(
        direction=g.get("direction") or "long",
        entry_low=g.get("entry_low"),
        entry_high=g.get("entry_high"),
        entry_trigger=g.get("entry_trigger"),
        suggested=g.get("suggested_entry"),
        stop=g.get("stop"),
        tp1=g.get("tp1"),
        tp2=g.get("tp2"),
        tp3=g.get("tp3"),
        candles=candles,
        entry_mode=g.get("entry_mode") or "PULLBACK_LIMIT",
        symbol=g.get("symbol") or "",
        fee_profile=fee_profile,
    )
    d = res.to_dict()
    if d.get("skipped"):
        d["net_usd"] = 0.0
        d["net_r"] = 0.0
    weight = _f(g.get("size_weight"))
    if weight is not None and weight < 1.0:
        weight = max(0.0, min(1.0, weight))
        d["net_usd"] = round(float(d.get("net_usd") or 0.0) * weight, 4)
        d["net_r"] = round(float(d.get("net_r") or 0.0) * weight, 4)
        d["size_weight"] = weight
    return d


def _frame_bar_minutes(frame: pd.DataFrame) -> int:
    stamps = pd.to_datetime(frame.get("timestamp"), utc=True, errors="coerce").dropna().sort_values()
    values = [int((b - a).total_seconds() // 60) for a, b in zip(stamps, stamps[1:]) if b > a]
    return max(1, int(pd.Series(values).median())) if values else 60


def _point_atr(frame: pd.DataFrame, idx: int, fallback: float | None = None) -> float | None:
    if fallback is not None and fallback > 0:
        return float(fallback)
    part = frame.iloc[max(0, int(idx) - 13):int(idx) + 1].copy()
    if part.empty:
        return None
    high = pd.to_numeric(part["high"], errors="coerce")
    low = pd.to_numeric(part["low"], errors="coerce")
    close = pd.to_numeric(part["close"], errors="coerce")
    prev = close.shift(1)
    tr = pd.concat([(high - low).abs(), (high - prev).abs(), (low - prev).abs()], axis=1).max(axis=1).dropna()
    value = float(tr.mean()) if not tr.empty else 0.0
    return value if value > 0 else None


def _breakout_snapshot_ok(row: dict[str, Any], *, strict_rvol: bool) -> tuple[bool, str | None]:
    snap = row.get("snapshot") or {}
    side = str(row.get("direction") or "long").lower()
    if str(snap.get("quality_action") or "") not in {"FULL_SIZE", "HALF_SIZE"}:
        return False, "overlay_not_actionable"
    slope = str(snap.get("btc_ema_slope_state") or "unknown")
    if (side == "long" and slope != "up") or (side == "short" and slope != "down"):
        return False, "btc_swing_direction_not_confirmed"
    if side == "long" and str(snap.get("funding_state") or "") == "extreme_long":
        return False, "funding_against"
    if side == "short" and str(snap.get("funding_state") or "") == "short_crowded":
        return False, "funding_against"
    if side == "long" and str(snap.get("oi_price_regime") or "") == "fresh_shorts":
        return False, "oi_price_conflict"
    if side == "short" and str(snap.get("oi_price_regime") or "") == "fresh_longs":
        return False, "oi_price_conflict"
    if strict_rvol:
        rvol = _f(snap.get("volume_rvol"))
        if rvol is None or rvol < 1.0:
            return False, "rvol_too_low_or_unavailable"
    return True, None


def _breakout_clean_for_edge(row: dict[str, Any]) -> bool:
    """Use the same latency-quality definition as the wider swing evidence.

    A missing audit or a late-but-not-gap entry is not a trustworthy proxy for
    what the live path could have filled, so it cannot improve a refinement's
    headline statistics.
    """
    gap = _f(row.get("data_gap_min"))
    cause = str(row.get("latency_cause") or "").upper()
    return bool(
        gap is not None
        and gap <= 60
        and cause not in {"DATA_GAP_LATE", "LEGITIMATE_LATE", "NO_DATA", "NO_AUDIT"}
    )


def _closed_bar_quality(row: pd.Series, *, long: bool) -> bool:
    op, high, low, close = (_f(row.get(key)) for key in ("open", "high", "low", "close"))
    if None in {op, high, low, close} or high <= low:
        return False
    body = abs(close - op) / (high - low)
    location = (close - low) / (high - low) if long else (high - close) / (high - low)
    return bool((close >= op if long else close <= op) and body >= 0.35 and location >= 0.60)


def _reclaim_retest_entry(g: dict[str, Any], candles: pd.DataFrame, *, max_retest_bars: int = 2) -> tuple[dict[str, Any] | None, str | None]:
    """Find a closed reclaim/breakdown then a timely, confirmed retest.

    The first close beyond the trigger confirms structure. A later retest must
    happen within ``max_retest_bars`` and close back in the intended direction;
    this prevents a delayed entry from being credited to the original breakout.
    """
    frame = normalize_frame(candles)
    if frame.empty:
        return None, "ohlcv_unavailable"
    long = _side(g)
    trigger = _f(g.get("entry_trigger"))
    if trigger is None:
        trigger = _f(g.get("entry_high" if long else "entry_low"))
    stop = _f(g.get("stop"))
    if trigger is None or stop is None:
        return None, "missing_breakout_geometry"
    break_idx = None
    for idx, row in frame.iterrows():
        close = _f(row.get("close"))
        if close is not None and (close >= trigger if long else close <= trigger):
            break_idx = int(idx)
            break
    if break_idx is None:
        return None, "breakout_close_not_confirmed"
    for idx in range(break_idx + 1, min(len(frame), break_idx + 1 + int(max_retest_bars))):
        row = frame.iloc[idx]
        close, high, low = (_f(row.get(key)) for key in ("close", "high", "low"))
        if None in {close, high, low}:
            continue
        retest = low <= trigger if long else high >= trigger
        held = close >= trigger if long else close <= trigger
        if not retest or not held or not _closed_bar_quality(row, long=long):
            continue
        atr = _point_atr(frame, idx, _f((_raw_setup(g.get("raw_idea_json"))).get("atr")))
        if atr is None:
            return None, "atr_unavailable"
        if abs(close - trigger) / atr > 0.35:
            return None, "entry_too_extended"
        if abs(close - stop) / atr > 1.5:
            return None, "stop_too_wide"
        ts = parse_dt(row.get("timestamp"))
        return {
            "idx": idx, "entry": close, "stop": stop, "trigger": trigger,
            "entry_at": ts + timedelta(minutes=_frame_bar_minutes(frame)) if ts else None,
            "atr": atr,
        }, None
    return None, "retest_not_confirmed_in_window"


def _simulate_reclaim_retest(g: dict[str, Any], candles: pd.DataFrame, fee_profile: str) -> dict[str, Any]:
    entry, reason = _reclaim_retest_entry(g, candles)
    if entry is None:
        return {"entered": False, "skipped": True, "skip_reason": reason, "net_usd": 0.0,
                "net_r": 0.0, "close_reason": reason, "tp3_runner": False}
    long = _side(g)
    tp1, tp2, tp3 = (_f(g.get(key)) for key in ("tp1", "tp2", "tp3"))
    if None in {tp1, tp2, tp3} or not ((entry["stop"] < entry["entry"] < tp1 < tp2 < tp3) if long
                                      else (entry["stop"] > entry["entry"] > tp1 > tp2 > tp3)):
        return {"entered": False, "skipped": True, "skip_reason": "invalid_confirmed_close_geometry",
                "net_usd": 0.0, "net_r": 0.0, "close_reason": "invalid_confirmed_close_geometry", "tp3_runner": False}
    frame = normalize_frame(candles)
    future = frame.iloc[int(entry["idx"]) + 1:].reset_index(drop=True)
    expiry = _dt(g.get("expires_at"))
    result = simulate_confirmed_close_entry(
        direction=g.get("direction") or "long", entry=float(entry["entry"]), stop=float(entry["stop"]),
        tp1=float(tp1), tp2=float(tp2), tp3=float(tp3), future_candles=future,
        symbol=g.get("symbol") or "", fee_profile=fee_profile, entry_at=entry.get("entry_at"),
        bar_minutes=_frame_bar_minutes(frame),
        force_close=bool(expiry is not None and expiry <= pd.Timestamp.now(tz="UTC")),
    ).to_dict()
    if result.get("status") != "closed":
        return {"entered": True, "skipped": False, "skip_reason": result.get("close_reason"),
                "net_usd": 0.0, "net_r": 0.0, "close_reason": result.get("close_reason"),
                "tp3_runner": False, "outcome_status": "open"}
    return {
        "entered": True, "skipped": False, "net_usd": float(result.get("net_pnl_usd") or 0.0),
        "net_r": float(result.get("net_r") or 0.0), "close_reason": result.get("close_reason"),
        "tp3_runner": result.get("close_reason") == "tp3_runner", "entry_at": entry.get("entry_at"),
        "entry_price": entry.get("entry"), "fees_usd": result.get("fees_usd"),
        "slippage_usd": result.get("slippage_usd"), "outcome_status": "closed",
    }


def _max_drawdown(values: list[float]) -> float:
    peak = cur = mdd = 0.0
    for v in values:
        cur += v
        peak = max(peak, cur)
        mdd = min(mdd, cur - peak)
    return mdd


def _median(values: list[float]) -> float:
    vals = sorted(values)
    if not vals:
        return 0.0
    mid = len(vals) // 2
    if len(vals) % 2:
        return vals[mid]
    return (vals[mid - 1] + vals[mid]) / 2


def _bootstrap_ci(deltas: list[float], reps: int = 1000) -> tuple[float, float]:
    if not deltas:
        return 0.0, 0.0
    rng = random.Random(42)
    vals = []
    n = len(deltas)
    for _ in range(reps):
        vals.append(sum(deltas[rng.randrange(n)] for _ in range(n)))
    vals.sort()
    return vals[int(0.05 * (reps - 1))], vals[int(0.95 * (reps - 1))]


def _agg(records: list[dict[str, Any]], subset: Callable[[dict[str, Any]], bool]) -> list[dict[str, Any]]:
    by: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in records:
        if subset(r):
            by[r["variant"]].append(r)
    out = []
    for name, rows in by.items():
        current_rows = [r for r in rows if r["variant"] == "current"]
        entered_rows = [r for r in rows if r["entered"]]
        net = sum(r["net_usd"] for r in rows)
        delta = sum(r["delta_usd"] for r in rows)
        deltas = [r["delta_usd"] for r in rows]
        ci_lo, ci_hi = _bootstrap_ci(deltas, reps=600)
        out.append({
            "variant": name,
            "n": len(rows),
            "entered": sum(1 for r in rows if r["entered"]),
            "skipped": sum(1 for r in rows if r["skipped"]),
            "net": round(net, 2),
            "delta": round(delta, 2),
            "avg_delta": round(delta / len(rows), 2) if rows else 0,
            "ci90": (round(ci_lo, 2), round(ci_hi, 2)),
            "wr": round(sum(1 for r in entered_rows if r["net_usd"] > 0) / len(entered_rows), 3) if entered_rows else 0,
            "stops": sum(1 for r in rows if r["close_reason"] in ("original_stop", "stopped_full")),
            "tp3": sum(1 for r in rows if r["tp3_runner"]),
            "avoided_losers": sum(1 for r in rows if r["skipped"] and r["current_net_usd"] < 0),
            "missed_winners": sum(1 for r in rows if r["skipped"] and r["current_net_usd"] > 0),
            "mdd": round(_max_drawdown([r["net_usd"] for r in rows]), 2),
            "current_n": len(current_rows),
        })
    order = {"current": -10**9}
    return sorted(out, key=lambda r: (order.get(r["variant"], -r["delta"]), r["variant"]))


def _render_table(rows: list[dict[str, Any]], limit: int = 30) -> list[str]:
    lines = [
        "| variant | n | entered | skipped | net $ | Δ vs current $ | avg Δ | CI90 Δ | WR | stops | TP3 | avoided L / missed W | maxDD $ |",
        "|---|--:|--:|--:|--:|--:|--:|---:|--:|--:|--:|---:|--:|",
    ]
    for r in rows[:limit]:
        ci = f"{r['ci90'][0]:.0f}..{r['ci90'][1]:.0f}"
        lines.append(
            f"| `{r['variant']}` | {r['n']} | {r['entered']} | {r['skipped']} | "
            f"{r['net']:.0f} | {r['delta']:.0f} | {r['avg_delta']:.2f} | {ci} | "
            f"{r['wr']:.2f} | {r['stops']} | {r['tp3']} | "
            f"{r['avoided_losers']} / {r['missed_winners']} | {r['mdd']:.0f} |"
        )
    return lines


def _baseline_diagnostics(records: list[dict[str, Any]]) -> dict[str, Any]:
    cur = [r for r in records if r["variant"] == "current" and r.get("ledger_net_usd") is not None]
    diffs = [float(r["net_usd"]) - float(r["ledger_net_usd"]) for r in cur]
    absdiffs = [abs(x) for x in diffs]
    return {
        "n": len(cur),
        "ledger_net": round(sum(float(r["ledger_net_usd"]) for r in cur), 2),
        "sim_net": round(sum(float(r["net_usd"]) for r in cur), 2),
        "drift": round(sum(diffs), 2),
        "median_abs_drift": round(_median(absdiffs), 2),
        "p90_abs_drift": round(sorted(absdiffs)[int(0.90 * (len(absdiffs) - 1))], 2) if absdiffs else 0.0,
    }


def _group_current(records: list[dict[str, Any]], key: str, limit: int = 12) -> list[dict[str, Any]]:
    cur = [r for r in records if r["variant"] == "current"]
    by: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in cur:
        by[str(r.get(key) or "UNKNOWN")].append(r)
    out = []
    for name, rows in by.items():
        out.append({
            "group": name,
            "n": len(rows),
            "net": round(sum(float(r["net_usd"]) for r in rows), 2),
            "wr": round(sum(1 for r in rows if r["net_usd"] > 0) / len(rows), 3) if rows else 0.0,
            "stops": sum(1 for r in rows if r["close_reason"] in ("original_stop", "stopped_full")),
            "tp3": sum(1 for r in rows if r["tp3_runner"]),
        })
    return sorted(out, key=lambda r: r["net"])[:limit]


def _render_group_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| group | n | net $ | WR | stops | TP3 |",
        "|---|--:|--:|--:|--:|--:|",
    ]
    for r in rows:
        lines.append(f"| `{r['group']}` | {r['n']} | {r['net']:.0f} | {r['wr']:.2f} | {r['stops']} | {r['tp3']} |")
    return lines


def _policy_summary(result: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    all_rows = {r["variant"]: r for r in result["tables"]["all"] if r["variant"] in POLICY_VARIANTS}
    late_rows = {r["variant"]: r for r in result["tables"]["late_test"] if r["variant"] in POLICY_VARIANTS}
    recent_rows = {r["variant"]: r for r in result["tables"]["recent_7d"] if r["variant"] in POLICY_VARIANTS}
    for name in POLICY_VARIANTS:
        a = all_rows.get(name) or {}
        l = late_rows.get(name) or {}
        rc = recent_rows.get(name) or {}
        rows.append({
            "variant": name,
            "entered": a.get("entered", 0),
            "net": a.get("net", 0),
            "wr": a.get("wr", 0),
            "late_net": l.get("net", 0),
            "recent_net": rc.get("net", 0),
            "skipped": a.get("skipped", 0),
        })
    return rows


def _render_policy_summary(result: dict[str, Any]) -> list[str]:
    lines = [
        "## Versioned Shadow Swing Summary",
        "",
        "| variant | entered | skipped | net $ | entered WR | late-test net $ | recent-7d net $ |",
        "|---|--:|--:|--:|--:|--:|--:|",
    ]
    for r in _policy_summary(result):
        lines.append(
            f"| `{r['variant']}` | {r['entered']} | {r['skipped']} | {float(r['net']):.0f} | "
            f"{float(r['wr']):.2f} | {float(r['late_net']):.0f} | {float(r['recent_net']):.0f} |"
        )
    lines += [
        "",
        "Production paper keeps the legacy/native swing geometry. Every row in this table is "
        "shadow/counterfactual evidence only; no target profile is promoted by this report.",
        "",
    ]
    return lines


def run(limit: int | None = None) -> dict[str, Any]:
    cfg = load_config()
    fs = FileStore(cfg)
    fee_profile = paper_portfolio.load_cfg().get("fee_profile", "bybit_non_vip_usdt_perp")
    try:
        from src.execution import crypto_overlay_counterfactual as _cf
        _cf.refresh(db=str(cfg.db_path), persist=True)
    except Exception:
        pass
    try:
        from src.signals.entry_latency_audit import refresh as _lat_refresh
        _lat_refresh(limit=1000, asset_class="crypto", db=str(cfg.db_path))
    except Exception:
        pass
    conn = sqlite3.connect(f"file:{Path(cfg.db_path).as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        rows = _load_rows(conn, fee_profile)
    finally:
        conn.close()
    if limit:
        rows = rows[-int(limit):]

    records: list[dict[str, Any]] = []
    skipped = {"bad_geom": 0, "no_candles": 0, "current_no_fill": 0}
    candle_sources = {"rolling": 0, "deep_history": 0}
    for row in rows:
        g0 = _geom(row)
        if g0 is None:
            skipped["bad_geom"] += 1
            continue
        candles, tf = _load_candles(fs, cfg, row["symbol"], row["mode"], row["asset_class"],
                                    row.get("exchange_focus"), row.get("created_at"))
        source = "rolling"
        if candles is None or getattr(candles, "empty", True):
            candles, _ex, tf = load_deep_candles(cfg, row["symbol"], row["mode"],
                                                 row.get("exchange_focus") or "", row.get("created_at"))
            source = "deep_history"
        if candles is None or getattr(candles, "empty", True):
            skipped["no_candles"] += 1
            continue
        candles = _clip_to_expiry(candles, row.get("expires_at"))
        if (candles is None or candles.empty) and source == "rolling":
            candles, _ex, tf = load_deep_candles(cfg, row["symbol"], row["mode"],
                                                 row.get("exchange_focus") or "", row.get("created_at"))
            source = "deep_history"
            if candles is not None and not candles.empty:
                candles = _clip_to_expiry(candles, row.get("expires_at"))
        if candles is None or candles.empty:
            skipped["no_candles"] += 1
            continue
        candle_sources[source] += 1
        current = _simulate(g0, candles, fee_profile)
        if current.get("skipped"):
            skipped["current_no_fill"] += 1
            continue
        current_net = float(current.get("net_usd") or 0.0)
        for v in VARIANTS:
            gv = v.mutate(g0)
            if gv is None:
                rec = {"entered": False, "skipped": True, "skip_reason": "variant_unavailable",
                       "net_usd": 0.0, "net_r": 0.0, "close_reason": "variant_unavailable",
                       "tp3_runner": False}
            else:
                rec = _simulate(gv, candles, fee_profile)
            net = float(rec.get("net_usd") or 0.0)
            records.append({
                "signal_id": row["signal_id"],
                "created_at": row["created_at"],
                "symbol": row.get("symbol"),
                "direction": row.get("direction") or "long",
                "variant": v.name,
                "net_usd": net,
                "delta_usd": net - current_net,
                "current_net_usd": current_net,
                "ledger_net_usd": _f(row.get("ledger_net_usd")),
                "entered": bool(rec.get("entered")) and not bool(rec.get("skipped")),
                "skipped": bool(rec.get("skipped")),
                "close_reason": rec.get("close_reason") or rec.get("skip_reason") or "",
                "tp3_runner": bool(rec.get("tp3_runner")),
                "quality_action": row.get("quality_action") or "NO_OVERLAY",
                "quality_reasons_json": row.get("quality_reasons_json") or "",
                "score": _f(row.get("score")) or 0.0,
                "data_gap_min": _f(row.get("data_gap_min")),
                "latency_cause": row.get("latency_cause") or "NO_AUDIT",
            })

    def all_rows(_: dict[str, Any]) -> bool:
        return True

    def clean(r: dict[str, Any]) -> bool:
        return (
            r.get("data_gap_min") is not None
            and r["data_gap_min"] <= 60
            and str(r.get("latency_cause") or "").upper()
            not in {"DATA_GAP_LATE", "LEGITIMATE_LATE", "NO_DATA", "NO_AUDIT"}
        )

    def recent_7d(r: dict[str, Any]) -> bool:
        ts = _dt(r.get("created_at"))
        if ts is None:
            return False
        cutoff = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=7)
        return ts >= cutoff

    sig_times = sorted({
        (r["signal_id"], _dt(r.get("created_at"))) for r in records if _dt(r.get("created_at")) is not None
    }, key=lambda x: x[1])
    bucket_by_sig: dict[str, str] = {}
    if sig_times:
        n = len(sig_times)
        for idx, (sid, _ts) in enumerate(sig_times):
            bucket_by_sig[sid] = "old_train" if idx < n / 3 else ("mid_validation" if idx < 2 * n / 3 else "late_test")

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "db_path": str(Path(cfg.db_path).resolve()),
        "fee_profile": fee_profile,
        "rows_loaded": len(rows),
        "paired_signals": len({r["signal_id"] for r in records}),
        "records": records,
        "skipped": skipped,
        "candle_sources": candle_sources,
        "diagnostics": {
            "baseline_vs_ledger": _baseline_diagnostics(records),
            "weakest_symbols_current": _group_current(records, "symbol"),
            "by_direction_current": _group_current(records, "direction", limit=10),
        },
        "tables": {
            "all": _agg(records, all_rows),
            "clean_no_gap_gt60": _agg(records, clean),
            "recent_7d": _agg(records, recent_7d),
            "old_train": _agg(records, lambda r: bucket_by_sig.get(r["signal_id"]) == "old_train"),
            "mid_validation": _agg(records, lambda r: bucket_by_sig.get(r["signal_id"]) == "mid_validation"),
            "late_test": _agg(records, lambda r: bucket_by_sig.get(r["signal_id"]) == "late_test"),
        },
    }


def run_breakout_refinements(limit: int | None = None) -> dict[str, Any]:
    """Forward-only, direction-separated Shadow tests for swing breakouts.

    The active Paper swing remains untouched.  The control uses the same native
    breakout geometry; refinement profiles only differ by a closed reclaim or
    failed-breakdown retest and frozen-at-entry quality checks.
    """
    cfg = load_config()
    fs = FileStore(cfg)
    fee_profile = paper_portfolio.load_cfg().get("fee_profile", "bybit_non_vip_usdt_perp")
    conn = sqlite3.connect(f"file:{Path(cfg.db_path).as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        rows = _load_forward_breakout_rows(conn)
    finally:
        conn.close()
    if limit:
        rows = rows[-int(limit):]

    profiles = (
        ("control_clean", None, False),
        ("long_reclaim_retest", "long", False),
        ("long_reclaim_retest_rvol", "long", True),
        ("short_failed_retest", "short", False),
        ("short_failed_retest_rvol", "short", True),
    )
    records: list[dict[str, Any]] = []
    skipped = {"bad_geometry": 0, "ohlcv_unavailable": 0}
    for row in rows:
        g = _geom(row)
        if g is None:
            skipped["bad_geometry"] += 1
            continue
        g["entry_mode"] = "BREAKOUT_CONTINUATION"
        candles, _tf = _load_candles(fs, cfg, row["symbol"], "swing", "crypto",
                                     row.get("exchange_focus"), row.get("created_at"))
        if candles is None or getattr(candles, "empty", True):
            skipped["ohlcv_unavailable"] += 1
            continue
        candles = _clip_to_expiry(candles, row.get("expires_at"))
        if candles is None or candles.empty:
            skipped["ohlcv_unavailable"] += 1
            continue
        clean = _breakout_clean_for_edge(row)
        control = _simulate(g, candles, fee_profile)
        control_net = float(control.get("net_usd") or 0.0)
        for profile, required_side, strict_rvol in profiles:
            side = str(row.get("direction") or "long").lower()
            base = {
                "signal_id": row["signal_id"], "symbol": row.get("symbol"), "direction": side,
                "profile": profile, "clean": int(clean), "created_at": row.get("created_at"),
                "control_net_usd": control_net, "latency_cause": row.get("latency_cause"),
            }
            if not clean:
                rec = {"entered": False, "skipped": True, "skip_reason": "data_gap_late",
                       "net_usd": 0.0, "net_r": 0.0, "close_reason": "data_gap_late", "tp3_runner": False}
            elif required_side is not None and side != required_side:
                rec = {"entered": False, "skipped": True, "skip_reason": "direction_not_profile",
                       "net_usd": 0.0, "net_r": 0.0, "close_reason": "direction_not_profile", "tp3_runner": False}
            else:
                allowed, reason = _breakout_snapshot_ok(row, strict_rvol=strict_rvol)
                if not allowed:
                    rec = {"entered": False, "skipped": True, "skip_reason": reason,
                           "net_usd": 0.0, "net_r": 0.0, "close_reason": reason, "tp3_runner": False}
                elif profile == "control_clean":
                    rec = control
                else:
                    rec = _simulate_reclaim_retest(g, candles, fee_profile)
            records.append({**base, **rec, "delta_usd": float(rec.get("net_usd") or 0.0) - control_net})

    summaries = []
    for profile, _side, _strict in profiles:
        block = [r for r in records if r["profile"] == profile and r["clean"] == 1]
        entered = [r for r in block if r.get("entered") and not r.get("skipped")]
        closed = [r for r in entered if r.get("outcome_status", "closed") == "closed"]
        pnl = [float(r.get("net_usd") or 0.0) for r in closed]
        wins, losses = [x for x in pnl if x > 0], [x for x in pnl if x < 0]
        summaries.append({
            "profile": profile, "signals": len(block), "entered": len(entered), "closed": len(closed),
            "skipped": sum(bool(r.get("skipped")) for r in block), "net_pnl_usd": round(sum(pnl), 4),
            "paired_delta_usd": round(sum(float(r["delta_usd"]) for r in closed), 4),
            "profit_factor": (round(sum(wins) / abs(sum(losses)), 4) if losses else (float("inf") if wins else None)),
            "winrate": round(sum(x > 0 for x in pnl) / len(pnl), 4) if pnl else None,
            "skip_reasons": dict(sorted((reason, sum(1 for r in block if r.get("skip_reason") == reason))
                                          for reason in {r.get("skip_reason") for r in block if r.get("skip_reason")})),
        })
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(), "fee_profile": fee_profile,
        "source_signals": len(rows), "records": records, "summaries": summaries, "skipped": skipped,
    }


def write_breakout_refinement_report(result: dict[str, Any], out: Path = BREAKOUT_REPORT) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Crypto Swing Breakout Refinements (Shadow)", "",
        "- Forward-only `preentry_v2` new-logic breakout cohort; missing, late, and gap-tainted latency evidence is excluded.",
        "- The native breakout control and each refinement use the same Model-F execution and fee profile.",
        "- This report changes neither Paper geometry nor live routing. No profile is auto-promoted.", "",
        f"- generated_at: `{result['generated_at']}`",
        f"- source_signals: `{result['source_signals']}`; load skips: `{json.dumps(result['skipped'])}`", "",
        "| profile | clean signals | entered | closed | skipped | net USD | paired delta USD | PF | win% |", 
        "|---|--:|--:|--:|--:|--:|--:|--:|--:|",
    ]
    for row in result["summaries"]:
        pf = "inf" if row["profit_factor"] == float("inf") else ("-" if row["profit_factor"] is None else f"{row['profit_factor']:.2f}")
        wr = "-" if row["winrate"] is None else f"{row['winrate'] * 100:.0f}%"
        lines.append(f"| `{row['profile']}` | {row['signals']} | {row['entered']} | {row['closed']} | {row['skipped']} | "
                     f"{row['net_pnl_usd']:.2f} | {row['paired_delta_usd']:.2f} | {pf} | {wr} |")
        if row["skip_reasons"]:
            lines.append(f"  - skips: `{json.dumps(row['skip_reasons'], sort_keys=True)}`")
    lines += ["", "A refinement needs at least 30 clean closed forward trades, 28 forward days, positive USD PnL, PF >= 1.25, and positive paired delta before human Paper review.", ""]
    out.write_text("\n".join(lines), encoding="utf-8")


def persist_counterfactual(result: dict[str, Any], *, db_path: str | None = None) -> int:
    path = db_path or result["db_path"]
    rows = [r for r in result["records"] if r.get("variant") in POLICY_VARIANTS]
    now = result["generated_at"]
    conn = sqlite3.connect(path)
    try:
        conn.execute(_CF_DDL)
        existing_columns = {
            row[1] for row in conn.execute(
                "PRAGMA table_info(crypto_swing_paper_counterfactual)"
            )
        }
        if "snapshot_id" not in existing_columns:
            conn.execute(
                "ALTER TABLE crypto_swing_paper_counterfactual "
                "ADD COLUMN snapshot_id TEXT"
            )
        if "is_current_snapshot" not in existing_columns:
            conn.execute(
                "ALTER TABLE crypto_swing_paper_counterfactual "
                "ADD COLUMN is_current_snapshot INTEGER NOT NULL DEFAULT 0"
            )
        placeholders = ",".join("?" for _ in POLICY_VARIANTS)
        conn.execute(
            "UPDATE crypto_swing_paper_counterfactual SET is_current_snapshot=0 "
            f"WHERE variant IN ({placeholders})",
            tuple(POLICY_VARIANTS),
        )
        payload = []
        for r in rows:
            version, mults = POLICY_VARIANTS[str(r["variant"])]
            payload.append((
                r.get("signal_id"),
                r.get("variant"),
                version,
                json.dumps(mults),
                r.get("symbol"),
                r.get("direction"),
                r.get("created_at"),
                r.get("quality_action"),
                r.get("latency_cause"),
                r.get("data_gap_min"),
                int(bool(r.get("entered"))),
                int(bool(r.get("skipped"))),
                r.get("close_reason"),
                round(float(r.get("net_usd") or 0.0), 4),
                round(float(r.get("delta_usd") or 0.0), 4),
                now,
                version,
                now,
                1,
            ))
        conn.executemany(
            "INSERT OR REPLACE INTO crypto_swing_paper_counterfactual "
            "(signal_id, variant, profile_version, target_multipliers_json, symbol, direction, "
            "created_at, quality_action, latency_cause, data_gap_min, entered, skipped, close_reason, "
            "net_pnl_usd, delta_vs_current_usd, computed_at, version, snapshot_id, "
            "is_current_snapshot) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            payload,
        )
        conn.commit()
        return len(payload)
    finally:
        conn.close()


def write_report(result: dict[str, Any], out: Path = REPORT) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Crypto Swing Entry Sweep",
        "",
        "_Versioned simulation. It may refresh additive diagnostic/counterfactual tables, but never "
        "writes proposed_signals, signal_outcomes, final_r, the active paper ledger, or live._",
        "",
        f"- generated_at: `{result['generated_at']}`",
        f"- db_path: `{result['db_path']}`",
        f"- active fee_profile: `{result['fee_profile']}`",
        f"- rows_loaded: **{result['rows_loaded']}**",
        f"- paired_signals_simulated: **{result['paired_signals']}**",
        f"- skipped: `{json.dumps(result['skipped'], ensure_ascii=False)}`",
        f"- candle_sources: `{json.dumps(result['candle_sources'], ensure_ascii=False)}`",
        f"- variants tested: **{len(VARIANTS)}**",
        "",
        "Interpretation: `Δ vs current` compares each variant to the current simulated geometry on the same signal/candles. "
        "A skipped/no-fill variant books 0 PnL, so avoided losers and missed winners are visible.",
        "",
    ]
    lines += [
        "Methodology note: this is a paired parameter test, not a literal equity-curve replay. "
        "The simulated baseline uses the shared profit-protection engine on the same candles; the live ledger may differ "
        "because of portfolio compounding, size weights, and historical accounting context. Use delta-vs-current more than absolute dollars.",
        "",
        "## Sanity Checks",
        "",
        f"- baseline_vs_ledger: `{json.dumps(result['diagnostics']['baseline_vs_ledger'], ensure_ascii=False)}`",
        "",
        "### Weakest Symbols Under Current Simulation",
        "",
    ]
    lines += _render_group_table(result["diagnostics"]["weakest_symbols_current"])
    lines += [
        "",
        "### Current Simulation By Direction",
        "",
    ]
    lines += _render_group_table(result["diagnostics"]["by_direction_current"])
    lines.append("")
    lines += _render_policy_summary(result)

    for title, key in (
        ("All Paired Signals", "all"),
        ("Clean Audited Subset (data_gap <= 60m)", "clean_no_gap_gt60"),
        ("Recent 7d", "recent_7d"),
        ("Chronological Split: Old Train", "old_train"),
        ("Chronological Split: Mid Validation", "mid_validation"),
        ("Chronological Split: Late Test", "late_test"),
    ):
        lines += [f"## {title}", ""]
        lines += _render_table(result["tables"][key])
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--persist-counterfactual", action="store_true",
                    help="persist versioned crypto-swing shadow variants into the additive read-model table")
    ap.add_argument("--breakout-refinements", action="store_true",
                    help="run the separate forward-only breakout reclaim/failed-retest Shadow report")
    args = ap.parse_args()
    if args.breakout_refinements:
        result = run_breakout_refinements(limit=args.limit)
        write_breakout_refinement_report(result)
        print(f"report={BREAKOUT_REPORT}")
        print(f"source_signals={result['source_signals']} skipped={result['skipped']}")
        if args.json:
            print(json.dumps({k: v for k, v in result.items() if k != "records"}, ensure_ascii=False, indent=2))
        return
    result = run(limit=args.limit)
    write_report(result)
    print(f"report={REPORT}")
    print(f"paired_signals={result['paired_signals']} skipped={result['skipped']}")
    if args.persist_counterfactual:
        n = persist_counterfactual(result)
        print(f"persisted_counterfactual_rows={n}")
    if args.json:
        print(json.dumps({k: v for k, v in result.items() if k != "records"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
