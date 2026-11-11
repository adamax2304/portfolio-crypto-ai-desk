"""Conservative, forward-only crypto intraday idea tests.

This is a read-model experiment lane.  It deliberately tests only the small set
of ideas approved for the current review:

* PULLBACK_LIMIT: current zone, shallow/deeper zone, one-bar level hold, one-bar VWAP hold.
* BREAKOUT_CONTINUATION: point-in-time strong confirmation only, HALF_SIZE accounting.
* MOMENTUM_TAKER_NOW: control only, HALF_SIZE until 30 resolved forward trades.
* LIMIT_THEN_TAKER_TIMEOUT: disabled, never simulated.

Crypto samples must be ``preentry_v2`` and ``data_quality=ok``.  Asia/off rows are
excluded by the production session guard, which this module never changes.  No
variant is promoted automatically; fewer than 30 resolved forward trades produce
an explicit insufficient-sample status.
"""
from __future__ import annotations

import json
import hashlib
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from src.config import load_config
from src.execution import profit_protection as pp
from src.execution.crypto_quality_overlay import load_cfg, session_bucket
from src.execution.entry_mode_parameter_sweep import _f, _variant_geometry
from src.execution.shadow_strategy_common import parse_dt, simulate_confirmed_close_entry

VERSION = "crypto_intraday_preentry_v4"
MIN_RESOLVED_FORWARD = 30
HALF_SIZE = 0.5
VARIANTS = {
    "PULLBACK_LIMIT": (
        ("current", "current zone"),
        ("shallow", "shallow zone"),
        ("deeper", "deeper zone"),
        ("level_hold_1bar", "one closed candle holds the pullback level, then a later retest fills"),
        ("level_hold_v2", "mid-zone reclaim with a quality close, then a retest within three bars"),
        ("vwap_hold_1bar", "one closed candle holds session VWAP, then a later retest fills"),
        ("vwap_confirm_close", "enter at the close of the candle confirming session VWAP hold"),
        ("level_hold_mid_zone_retest_2bar", "close through the mid-zone with a strong body; retest within two bars"),
        ("level_hold_far_edge_retest_2bar", "close through the far zone edge with a strong body; retest within two bars"),
        ("vwap_zone_slope_hold_retest_2bar", "hold VWAP and the far zone edge with aligned VWAP slope; retest within two bars"),
        ("level_hold_mid_zone_quality_retest_2bar", "mid-zone hold plus frozen light market/derivatives quality; retest within two bars"),
        ("vwap_zone_slope_quality_retest_2bar", "VWAP/zone/slope hold plus frozen light market/derivatives quality; retest within two bars"),
    ),
    "BREAKOUT_CONTINUATION": (("strong_confirmation_only", "point-in-time strong confirmation"),),
    "MOMENTUM_TAKER_NOW": (("current_half_size", "current entry, HALF_SIZE control"),),
}
# Counterfactual vetoes, not Paper filters.  Each branch keeps the exact
# ``current`` PULLBACK geometry/Model-F execution and changes only whether an
# already-frozen signal enters the research basket.  They can never route or
# promote a trade by themselves.
SHADOW_FILTER_VARIANTS = {
    "PULLBACK_LIMIT": (
        ("risk_off_veto_shadow", "Shadow counterfactual: omit only a frozen explicit BTC risk_off state."),
        ("oi_unknown_veto_shadow", "Shadow counterfactual: omit only fresh derivatives snapshots with OI regime unknown."),
        ("high_atr_veto_shadow", "Shadow counterfactual: omit observed ATR(14) > 2.5%; waits for point-in-time feature coverage."),
        ("low_rvol_veto_shadow", "Shadow counterfactual: omit observed RVOL(20) < 0.5; waits for point-in-time feature coverage."),
    ),
    "BREAKOUT_CONTINUATION": (
        ("breakout_15m_vwap_btc_quality_shadow",
         "Paper counterfactual: strong 15m breakout structure, VWAP-side hold and aligned BTC slope; waits for frozen feature coverage."),
    ),
}


_HOLD_POLICIES: dict[str, dict[str, Any]] = {
    "level_hold": {"level_fraction": 0.0},
    "level_hold_1bar": {"level_fraction": 0.0},
    # Production-Paper V2.  This remains deliberately less restrictive than
    # the old Shadow-only VWAP/two-bar experiments: its purpose is to remove
    # weak pullback bounces, not to starve the Paper lane of observations.
    "level_hold_v2": {
        "level_fraction": 0.5, "max_retest_bars": 3,
        "min_close_location": 0.60, "min_body_fraction": 0.35,
    },
    "vwap_hold_1bar": {"require_vwap": True},
    "vwap_confirm_close": {"require_vwap": True},
    "level_hold_mid_zone_retest_2bar": {
        "level_fraction": 0.5, "max_retest_bars": 2, "min_close_location": 0.60, "min_body_fraction": 0.35,
    },
    "level_hold_far_edge_retest_2bar": {
        "level_fraction": 1.0, "max_retest_bars": 2, "min_close_location": 0.65, "min_body_fraction": 0.40,
    },
    "vwap_zone_slope_hold_retest_2bar": {
        "require_vwap": True, "require_vwap_slope": True, "level_fraction": 1.0,
        "max_retest_bars": 2, "min_close_location": 0.65, "min_body_fraction": 0.40,
    },
    "level_hold_mid_zone_quality_retest_2bar": {
        "level_fraction": 0.5, "max_retest_bars": 2, "min_close_location": 0.60, "min_body_fraction": 0.35,
        "requires_light_quality": True,
    },
    "vwap_zone_slope_quality_retest_2bar": {
        "require_vwap": True, "require_vwap_slope": True, "level_fraction": 1.0,
        "max_retest_bars": 2, "min_close_location": 0.65, "min_body_fraction": 0.40,
        "requires_light_quality": True,
    },
}

_SUMMARY_DDL = """
CREATE TABLE IF NOT EXISTS crypto_intraday_idea_sweep_results (
  generated_at TEXT, version TEXT, entry_mode TEXT, variant TEXT, status TEXT,
  source_signals INTEGER, eligible_signals INTEGER, resolved INTEGER, skipped INTEGER,
  unresolved INTEGER, net_usd REAL, net_r REAL, winrate REAL, profit_factor REAL,
  size_action TEXT, size_weight REAL, notes TEXT, entries_observed INTEGER,
  geometry_changed_signals INTEGER, mean_bars_to_entry REAL,
  filter_excluded INTEGER NOT NULL DEFAULT 0, feature_unavailable INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (version, entry_mode, variant)
)
"""
_TRADE_DDL = """
CREATE TABLE IF NOT EXISTS crypto_intraday_idea_sweep_trades (
  generated_at TEXT, version TEXT, signal_id TEXT, entry_mode TEXT, variant TEXT,
  status TEXT, skip_reason TEXT, session_bucket TEXT, strong_confirmation INTEGER,
  size_action TEXT, size_weight REAL, net_usd REAL, net_r REAL, close_reason TEXT,
  entry_rule TEXT, confirmation_at TEXT, confirmation_price REAL,
  simulation_start_at TEXT, entry_bar_at TEXT, entry_price REAL, bars_to_entry INTEGER,
  entry_order_type TEXT, entry_low_used REAL, entry_high_used REAL,
  entry_trigger_used REAL, suggested_entry_used REAL, stop_used REAL,
  geometry_changed INTEGER,
  PRIMARY KEY (version, signal_id, variant)
)
"""

# The two legacy tables remain a convenient "latest run" read model for the
# dashboard. Evidence itself is append-only below: a new run can never erase a
# prior forward result or silently rewrite its configuration context.
_RUN_DDL = """
CREATE TABLE IF NOT EXISTS crypto_intraday_idea_sweep_runs (
  run_id TEXT PRIMARY KEY, generated_at TEXT NOT NULL, version TEXT NOT NULL,
  config_hash TEXT NOT NULL, signals_sampled INTEGER NOT NULL,
  source_scope TEXT NOT NULL
)
"""
_HISTORY_SUMMARY_DDL = """
CREATE TABLE IF NOT EXISTS crypto_intraday_idea_sweep_results_history (
  run_id TEXT NOT NULL, generated_at TEXT NOT NULL, version TEXT NOT NULL,
  entry_mode TEXT NOT NULL, variant TEXT NOT NULL, status TEXT NOT NULL,
  source_signals INTEGER NOT NULL, eligible_signals INTEGER NOT NULL,
  resolved INTEGER NOT NULL, skipped INTEGER NOT NULL, unresolved INTEGER NOT NULL,
  expired_entry_skips INTEGER NOT NULL, net_usd REAL NOT NULL, net_r REAL NOT NULL,
  winrate REAL, profit_factor REAL, size_action TEXT NOT NULL, size_weight REAL NOT NULL,
  notes TEXT, entries_observed INTEGER NOT NULL, geometry_changed_signals INTEGER NOT NULL,
  mean_bars_to_entry REAL,
  filter_excluded INTEGER NOT NULL DEFAULT 0, feature_unavailable INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (run_id, entry_mode, variant)
)
"""
_HISTORY_TRADE_DDL = """
CREATE TABLE IF NOT EXISTS crypto_intraday_idea_sweep_trades_history (
  run_id TEXT NOT NULL, generated_at TEXT NOT NULL, version TEXT NOT NULL,
  signal_id TEXT NOT NULL, entry_mode TEXT NOT NULL, variant TEXT NOT NULL,
  status TEXT NOT NULL, skip_reason TEXT, signal_session TEXT, entry_session TEXT,
  signal_created_at TEXT, signal_expires_at TEXT, entry_bar_at TEXT, entry_bar_closed_at TEXT,
  entry_within_validity INTEGER, entry_delay_minutes REAL, strong_confirmation INTEGER,
  size_action TEXT NOT NULL, size_weight REAL NOT NULL, net_usd REAL, net_r REAL,
  close_reason TEXT, entry_rule TEXT, confirmation_at TEXT, confirmation_price REAL,
  simulation_start_at TEXT, entry_price REAL, bars_to_entry INTEGER, entry_order_type TEXT,
  entry_low_used REAL, entry_high_used REAL, entry_trigger_used REAL,
  suggested_entry_used REAL, stop_used REAL, geometry_changed INTEGER,
  PRIMARY KEY (run_id, signal_id, variant)
)
"""


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def _json(v: Any) -> dict:
    try:
        x = json.loads(v or "{}")
        return x if isinstance(x, dict) else {}
    except (TypeError, ValueError):
        return {}


def _row_dict(row: Any) -> dict:
    if hasattr(row, "to_dict"):
        return row.to_dict()
    return dict(row)


def _candle_rows(candles: Any) -> list[dict]:
    if candles is None or getattr(candles, "empty", False):
        return []
    rows = []
    for _, r in candles.iterrows():
        rows.append({
            "open": _f(r.get("open")), "high": _f(r.get("high")),
            "low": _f(r.get("low")), "close": _f(r.get("close")),
            "volume": _f(r.get("volume")), "timestamp": r.get("timestamp"),
        })
    return rows


def _session_vwap(rows: list[dict], idx: int) -> float | None:
    if idx < 0 or idx >= len(rows):
        return None
    ts = pd.to_datetime(rows[idx].get("timestamp"), utc=True, errors="coerce")
    if pd.isna(ts):
        return None
    day = ts.date()
    pv = vol = 0.0
    for row in rows[: idx + 1]:
        rts = pd.to_datetime(row.get("timestamp"), utc=True, errors="coerce")
        volume = row.get("volume")
        if pd.isna(rts) or rts.date() != day or volume is None or volume <= 0:
            continue
        if row.get("high") is None or row.get("low") is None or row.get("close") is None:
            continue
        pv += ((row["high"] + row["low"] + row["close"]) / 3.0) * volume
        vol += volume
    return pv / vol if vol > 0 else None


def _iso(value: Any) -> str | None:
    ts = pd.to_datetime(value, utc=True, errors="coerce")
    return None if pd.isna(ts) else ts.isoformat()


def _as_utc(value: Any):
    ts = pd.to_datetime(value, utc=True, errors="coerce")
    return None if pd.isna(ts) else ts


def _bar_minutes(rows: list[dict]) -> int:
    timestamps = [pd.to_datetime(row.get("timestamp"), utc=True, errors="coerce") for row in rows]
    diffs = [int((b - a).total_seconds() // 60) for a, b in zip(timestamps, timestamps[1:])
             if not pd.isna(a) and not pd.isna(b) and b > a]
    return max(0, int(pd.Series(diffs).median())) if diffs else 0


def _confirmation_at(rows: list[dict], idx: int) -> str | None:
    ts = pd.to_datetime(rows[idx].get("timestamp"), utc=True, errors="coerce")
    if pd.isna(ts):
        return None
    return (ts + timedelta(minutes=_bar_minutes(rows))).isoformat()


def _close_quality(row: dict, *, long: bool, min_close_location: float, min_body_fraction: float) -> bool:
    open_px, high, low, close = (row.get(key) for key in ("open", "high", "low", "close"))
    if None in {open_px, high, low, close} or high <= low:
        return False
    body = abs(close - open_px) / (high - low)
    close_location = ((close - low) / (high - low)) if long else ((high - close) / (high - low))
    direction_ok = close >= open_px if long else close <= open_px
    return bool(direction_ok and body >= min_body_fraction and close_location >= min_close_location)


def _hold_policy(kind: str) -> dict[str, Any] | None:
    return _HOLD_POLICIES.get(kind)


def pullback_confirmation_gate(geom: dict, candles: Any, kind: str, *, entry_expires_at: Any = None) -> dict:
    """Return the first post-touch confirmation window without using future bars in the fill.

    The confirmation candle is fully closed, then simulation starts on the following
    candle.  This avoids crediting an entry before the confirmation was observable.
    """
    rows = _candle_rows(candles)
    if kind == "current":
        return {"eligible": True, "start_index": 0, "reason": "current_control"}
    if not rows:
        return {"eligible": False, "start_index": None, "reason": "no_candles"}
    long = str(geom.get("direction") or "long").lower() != "short"
    low, high = geom.get("entry_low"), geom.get("entry_high")
    if low is None or high is None:
        return {"eligible": False, "start_index": None, "reason": "missing_pullback_zone"}
    policy = _hold_policy(kind)
    if policy is None:
        return {"eligible": False, "start_index": None, "reason": "unknown_confirmation"}
    for idx, row in enumerate(rows):
        fill, _, _ = pp.entry_fill_bar(
            "PULLBACK_LIMIT", row, long=long, entry_low=low, entry_high=high,
            entry_trigger=geom.get("entry_trigger"), suggested=geom.get("entry"),
            is_first=(idx == 0), bps=pp.DEFAULT_MAKER_TRADE_THROUGH_BPS)
        if fill is None:
            continue
        confirm_idx = idx + 1
        if confirm_idx >= len(rows):
            return {"eligible": False, "start_index": None, "reason": "no_closed_confirmation_bar"}
        close = rows[confirm_idx].get("close")
        if close is None:
            return {"eligible": False, "start_index": None, "reason": "confirmation_close_missing"}
        required_level = None
        fraction = policy.get("level_fraction")
        if fraction is not None:
            required_level = low + (high - low) * float(fraction) if long else high - (high - low) * float(fraction)
            if not (close >= required_level if long else close <= required_level):
                return {"eligible": False, "start_index": None, "reason": "confirmation_failed"}
        if policy.get("require_vwap"):
            vwap = _session_vwap(rows, confirm_idx)
            if vwap is None:
                return {"eligible": False, "start_index": None, "reason": "vwap_volume_unavailable"}
            if not (close >= vwap if long else close <= vwap):
                return {"eligible": False, "start_index": None, "reason": "confirmation_failed"}
            if policy.get("require_vwap_slope"):
                prior_vwap = _session_vwap(rows, confirm_idx - 1)
                if prior_vwap is None or not (vwap > prior_vwap if long else vwap < prior_vwap):
                    return {"eligible": False, "start_index": None, "reason": "vwap_slope_not_aligned"}
        if not _close_quality(
            rows[confirm_idx], long=long,
            min_close_location=float(policy.get("min_close_location") or 0.0),
            min_body_fraction=float(policy.get("min_body_fraction") or 0.0),
        ):
            return {"eligible": False, "start_index": None, "reason": "confirmation_candle_too_weak"}
        confirmation_at = _confirmation_at(rows, confirm_idx)
        expires = _as_utc(entry_expires_at)
        if expires is not None and (_as_utc(confirmation_at) is None or _as_utc(confirmation_at) > expires):
            return {"eligible": False, "start_index": None, "reason": "confirmation_after_signal_expiry"}
        return {"eligible": True, "start_index": confirm_idx + 1,
                "confirmation_index": confirm_idx, "confirmation_at": confirmation_at,
                "confirmation_price": float(close), "required_level": required_level,
                "max_retest_bars": policy.get("max_retest_bars"), "reason": "confirmed"}
    return {"eligible": False, "start_index": None, "reason": "no_pullback_touch"}


def _session_guard(created_at: Any, cfg: dict) -> str:
    try:
        dt = pd.to_datetime(created_at, utc=True, errors="coerce")
        if pd.isna(dt):
            return "unknown"
        bucket = session_bucket(dt.to_pydatetime(), cfg)
        return "off" if bucket is False else str(bucket or "off")
    except Exception:
        return "unknown"


def _execution_fields(base_geom: dict, used_geom: dict, *, entry_rule: str,
                      gate: dict | None = None, work: Any = None) -> dict:
    gate = gate or {}
    rows = _candle_rows(work)
    return {
        "entry_rule": entry_rule,
        "confirmation_at": gate.get("confirmation_at"),
        "confirmation_price": gate.get("confirmation_price"),
        "simulation_start_at": _iso(rows[0].get("timestamp")) if rows else None,
        "entry_low_used": used_geom.get("entry_low"),
        "entry_high_used": used_geom.get("entry_high"),
        "entry_trigger_used": used_geom.get("entry_trigger"),
        "suggested_entry_used": used_geom.get("entry"),
        "stop_used": used_geom.get("stop"),
        "geometry_changed": int(any(used_geom.get(k) != base_geom.get(k)
                                    for k in ("entry_low", "entry_high", "entry_trigger", "entry", "stop"))),
    }


def _simulate(geom: dict, candles: Any, variant: str, *, fee_profile: str, size_weight: float,
              entry_expires_at: Any = None) -> dict:
    base_geom = dict(geom)
    used_geom = dict(geom)
    work = candles
    gate: dict | None = None
    entry_rule = "mode_specific_fill"
    expiry = _as_utc(entry_expires_at)
    bar_minutes = _bar_minutes(_candle_rows(candles))
    if variant in _HOLD_POLICIES:
        gate = pullback_confirmation_gate(used_geom, candles, variant, entry_expires_at=expiry)
        entry_rule = ("confirmation_close_taker" if variant == "vwap_confirm_close"
                      else "confirmation_then_limit_retest")
        if not gate["eligible"]:
            out = {"status": "skipped", "skip_reason": gate["reason"]}
            out.update(_execution_fields(base_geom, used_geom, entry_rule=entry_rule, gate=gate, work=work))
            return out
        work = candles.iloc[int(gate["start_index"]):].reset_index(drop=True)
    elif variant == "shallow":
        used_geom, _ = _variant_geometry("pullback_zone_depth_atr", "shallow", used_geom)
        entry_rule = "shallow_pullback_limit"
    elif variant == "deeper":
        used_geom, _ = _variant_geometry("pullback_zone_depth_atr", "deeper", used_geom)
        entry_rule = "deeper_pullback_limit"

    diagnostics = _execution_fields(base_geom, used_geom, entry_rule=entry_rule, gate=gate, work=work)
    diagnostics.update(signal_expires_at=_iso(expiry), bar_minutes=bar_minutes)
    if variant == "vwap_confirm_close":
        required = (gate.get("confirmation_price"), used_geom.get("stop"), used_geom.get("tp1"),
                    used_geom.get("tp2"), used_geom.get("tp3"))
        if any(value is None for value in required):
            diagnostics.update(status="skipped", skip_reason="missing_confirmed_close_geometry")
            return diagnostics
        entry = float(gate["confirmation_price"])
        stop, tp1, tp2, tp3 = (float(used_geom[k]) for k in ("stop", "tp1", "tp2", "tp3"))
        long = str(used_geom.get("direction") or "long").lower() != "short"
        valid_order = (stop < entry < tp1 < tp2 < tp3) if long else (stop > entry > tp1 > tp2 > tp3)
        if not valid_order:
            diagnostics.update(status="skipped", skip_reason="invalid_confirmed_close_geometry")
            return diagnostics
        sim = simulate_confirmed_close_entry(
            direction=used_geom.get("direction") or "long",
            entry=entry, stop=stop, tp1=tp1, tp2=tp2, tp3=tp3,
            future_candles=work, symbol=used_geom.get("symbol") or "", fee_profile=fee_profile,
        entry_at=parse_dt(gate.get("confirmation_at")), bar_minutes=bar_minutes,
            force_close=False,
        ).to_dict()
        diagnostics.update(
            entry_bar_at=gate.get("confirmation_at"), entry_price=sim.get("entry_price"),
            bars_to_entry=0, entry_order_type="taker", close_reason=sim.get("close_reason"),
        )
        if sim.get("status") != "closed" or sim.get("net_pnl_usd") is None or sim.get("net_r") is None:
            diagnostics.update(status="unresolved" if sim.get("status") == "open" else "skipped",
                               skip_reason=sim.get("close_reason") or sim.get("status") or "unresolved")
            return diagnostics
        diagnostics.update(status="resolved", net_usd=round(sim["net_pnl_usd"] * size_weight, 4),
                           net_r=sim["net_r"])
        return diagnostics

    wr = pp.walk(
        direction=used_geom.get("direction") or "long", entry_mode=used_geom.get("entry_mode") or "PULLBACK_LIMIT",
        entry_low=used_geom.get("entry_low"), entry_high=used_geom.get("entry_high"),
        entry_trigger=used_geom.get("entry_trigger"), suggested=used_geom.get("entry"),
        stop=used_geom.get("stop"), tp1=used_geom.get("tp1"), tp2=used_geom.get("tp2"),
        tp3=used_geom.get("tp3"), candles=work,
        entry_expiry_bars=gate.get("max_retest_bars") if gate else None,
        entry_expires_at=expiry.to_pydatetime() if expiry is not None else None,
        bar_minutes=bar_minutes,
    )
    work_rows = _candle_rows(work)
    entry_idx = wr.bars_to_entry if wr.bars_to_entry is not None else None
    diagnostics.update(
        entry_bar_at=(_iso(work_rows[entry_idx].get("timestamp"))
                      if entry_idx is not None and 0 <= entry_idx < len(work_rows) else None),
        entry_price=wr.entry_price, bars_to_entry=wr.bars_to_entry,
        entry_order_type=wr.entry_order_type,
    )
    if not wr.entered:
        diagnostics.update(status="skipped", skip_reason=(
                           "entry_after_signal_expiry" if wr.entry_expired and expiry is not None else
                           "retest_expired" if wr.entry_expired else
                           "pre_entry_invalidation" if wr.pre_entry_invalidation else "no_fill"))
        return diagnostics
    res = pp.protect(
        direction=used_geom.get("direction") or "long", entry=wr.entry_price, stop=used_geom.get("stop"),
        tp1=used_geom.get("tp1"), tp2=used_geom.get("tp2"), tp3=used_geom.get("tp3"),
        walk_result=wr, symbol=used_geom.get("symbol") or "", fee_profile=fee_profile,
        entry_mode=used_geom.get("entry_mode"),
    ).to_dict()
    diagnostics["close_reason"] = res.get("close_reason")
    if res.get("net_usd") is None or res.get("net_r") is None:
        diagnostics.update(status="unresolved", skip_reason=res.get("skip_reason") or "unresolved")
        return diagnostics
    diagnostics.update(status="resolved", net_usd=round(res["net_usd"] * size_weight, 4),
                       net_r=res["net_r"])
    return diagnostics


def _has(conn, table: str) -> bool:
    return bool(conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone())


def ensure_tables(conn) -> None:
    """Create latest-view and append-only evidence tables without deleting prior runs."""
    for ddl in (_SUMMARY_DDL, _TRADE_DDL, _RUN_DDL, _HISTORY_SUMMARY_DDL, _HISTORY_TRADE_DDL):
        conn.execute(ddl)
    # The latest cache can predate the diagnostic counters.  Additive migration
    # keeps every historic run readable and never mutates source trades.
    for table in ("crypto_intraday_idea_sweep_results", "crypto_intraday_idea_sweep_results_history"):
        columns = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
        for column in ("filter_excluded", "feature_unavailable"):
            if column not in columns:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} INTEGER NOT NULL DEFAULT 0")


def _load_samples(conn, limit: int) -> list[dict]:
    required = ("paper_shadow_execution_outcomes", "proposed_signals", "signal_entry_mode_preentry")
    if not all(_has(conn, t) for t in required):
        return []
    cols = {r[1] for r in conn.execute("PRAGMA table_info(paper_shadow_execution_outcomes)")}
    if "entry_mode_version" not in cols:
        return []
    signal_cols = {r[1] for r in conn.execute("PRAGMA table_info(proposed_signals)")}
    expires_sql = "p.expires_at AS expires_at" if "expires_at" in signal_cols else "NULL AS expires_at"
    sql = """
      SELECT DISTINCT s.signal_id, s.entry_mode, s.entry_mode_version, s.skipped_shadow_reason,
             p.symbol, p.direction, p.mode, p.asset_class, p.exchange_focus, p.created_at,
             p.entry_low, p.entry_high, p.entry_trigger, p.suggested_entry,
             COALESCE(p.invalidation, p.stop_loss) AS stop_used, p.tp1, p.tp2, p.tp3,
             """ + expires_sql + """, pm.data_quality AS preentry_data_quality, q.decision_json
      FROM paper_shadow_execution_outcomes s
      JOIN proposed_signals p ON p.signal_id=s.signal_id
      JOIN signal_entry_mode_preentry pm ON pm.signal_id=s.signal_id
      LEFT JOIN crypto_quality_overlay_decision_snapshots q
        ON q.signal_id=s.signal_id AND q.decision_context_type='point_in_time'
      WHERE s.branch='new_logic_shadow' AND s.window='forward_since_activation'
        AND s.entry_mode_version='preentry_v2'
        AND lower(COALESCE(p.asset_class,''))='crypto' AND lower(COALESCE(p.mode,''))='intraday'
        AND lower(COALESCE(pm.data_quality,''))='ok'
      ORDER BY p.created_at DESC LIMIT ?
    """
    try:
        rows = conn.execute(sql, (int(limit),)).fetchall()
    except sqlite3.OperationalError:
        return []
    names = [d[0] for d in conn.execute(sql, (int(limit),)).description]
    out = []
    for row in rows:
        d = dict(zip(names, row))
        snap = _json(d.pop("decision_json", None))
        d["strong_confirmation"] = int(bool(snap.get("strong_confirmation")))
        d["quality_action"] = str(snap.get("quality_action") or "UNKNOWN")
        d["btc_regime_state"] = str(snap.get("btc_regime_state") or "unknown")
        d["btc_ema_slope_state"] = str(snap.get("btc_ema_slope_state") or "unknown")
        d["funding_state"] = str(snap.get("funding_state") or "unknown")
        d["oi_price_regime"] = str(snap.get("oi_price_regime") or "unknown")
        d["derivatives_status"] = str(snap.get("derivatives_status") or "unknown")
        d["spread_bps"] = _f(snap.get("spread_bps"))
        d["volume_rvol"] = _f(snap.get("volume_rvol"))
        d["observed_price_feature_status"] = str(snap.get("observed_price_feature_status") or "unknown")
        d["observed_atr14_pct"] = _f(snap.get("observed_atr14_pct"))
        d["observed_rvol20"] = _f(snap.get("observed_rvol20"))
        d["observed_vwap20_distance_pct"] = _f(snap.get("observed_vwap20_distance_pct"))
        out.append(d)
    return out


def _geom(s: dict) -> dict:
    return {"direction": s.get("direction"), "entry_low": _f(s.get("entry_low")),
            "entry_high": _f(s.get("entry_high")), "entry_trigger": _f(s.get("entry_trigger")),
            "entry": _f(s.get("suggested_entry")), "stop": _f(s.get("stop_used")),
            "tp1": _f(s.get("tp1")), "tp2": _f(s.get("tp2")), "tp3": _f(s.get("tp3")),
            "entry_mode": s.get("entry_mode"), "symbol": s.get("symbol")}


def _light_hold_quality(sample: dict) -> tuple[bool, str | None]:
    """A narrow, frozen-at-entry quality gate for research variants only.

    It deliberately does not demand ``strong_confirmation``: that would make
    PULLBACK research empty.  Unknown inputs fail this *strict test profile*
    rather than being treated as bullish.
    """
    side = str(sample.get("direction") or "long").lower()
    if str(sample.get("quality_action") or "") not in {"FULL_SIZE", "HALF_SIZE"}:
        return False, "overlay_action_not_actionable"
    if str(sample.get("btc_ema_slope_state") or "unknown") in {"unknown", "flat"}:
        return False, "btc_slope_not_aligned"
    if side == "long" and str(sample.get("btc_ema_slope_state")) != "up":
        return False, "btc_slope_not_aligned"
    if side == "short" and str(sample.get("btc_ema_slope_state")) != "down":
        return False, "btc_slope_not_aligned"
    if side == "long" and str(sample.get("funding_state")) == "extreme_long":
        return False, "funding_against"
    if side == "short" and str(sample.get("funding_state")) == "short_crowded":
        return False, "funding_against"
    if side == "long" and str(sample.get("oi_price_regime")) == "fresh_shorts":
        return False, "oi_price_conflict"
    if side == "short" and str(sample.get("oi_price_regime")) == "fresh_longs":
        return False, "oi_price_conflict"
    if sample.get("spread_bps") is None or float(sample["spread_bps"]) > 20.0:
        return False, "spread_unavailable_or_wide"
    if sample.get("volume_rvol") is None or float(sample["volume_rvol"]) < 1.0:
        return False, "rvol_too_low_or_unavailable"
    return True, None


def _shadow_filter_state(sample: dict, variant: str) -> tuple[str, str | None]:
    """Return pass/exclude/unavailable for an isolated, frozen-feature test.

    Unknown data never becomes a negative market finding.  It is reported as
    unavailable so the report shows that a branch lacks evidence rather than
    silently improving its metrics by discarding old rows.
    """
    if variant == "risk_off_veto_shadow":
        state = str(sample.get("btc_regime_state") or "unknown").lower()
        if state == "unknown":
            return "unavailable", "btc_regime_feature_unavailable"
        return ("exclude", "shadow_btc_risk_off") if state == "risk_off" else ("pass", None)
    if variant == "oi_unknown_veto_shadow":
        status = str(sample.get("derivatives_status") or "unknown").lower()
        regime = str(sample.get("oi_price_regime") or "unknown").lower()
        if status != "ok":
            return "unavailable", "derivatives_feature_unavailable"
        return ("exclude", "shadow_oi_regime_unclassified") if regime == "unknown" else ("pass", None)
    if variant == "high_atr_veto_shadow":
        atr14 = _f(sample.get("observed_atr14_pct"))
        if str(sample.get("observed_price_feature_status") or "unknown") != "ok" or atr14 is None:
            return "unavailable", "observed_atr_feature_unavailable"
        return ("exclude", "shadow_atr14_over_2_5pct") if atr14 > 2.5 else ("pass", None)
    if variant == "low_rvol_veto_shadow":
        rvol = _f(sample.get("observed_rvol20"))
        if str(sample.get("observed_price_feature_status") or "unknown") != "ok" or rvol is None:
            return "unavailable", "observed_rvol_feature_unavailable"
        return ("exclude", "shadow_rvol20_below_0_5") if rvol < 0.5 else ("pass", None)
    if variant == "breakout_15m_vwap_btc_quality_shadow":
        # ``strong_confirmation`` is the frozen 15m breakout-structure fact
        # already used by the current breakout profile.  The other two checks
        # are intentionally a small counterfactual, not a fresh indicator
        # reconstruction from future candles.
        if not bool(sample.get("strong_confirmation")):
            return "exclude", "strong_confirmation_not_available_at_entry"
        side = str(sample.get("direction") or "long").lower()
        slope = str(sample.get("btc_ema_slope_state") or "unknown").lower()
        vwap_distance = _f(sample.get("observed_vwap20_distance_pct"))
        if slope in {"unknown", "flat"}:
            return "unavailable", "btc_slope_feature_unavailable"
        if vwap_distance is None:
            return "unavailable", "observed_vwap_feature_unavailable"
        if side == "long" and slope != "up":
            return "exclude", "btc_slope_against_long"
        if side == "short" and slope != "down":
            return "exclude", "btc_slope_against_short"
        # A continuation can retest VWAP, but a confirmed breakout already
        # materially below/above it is no longer the same continuation setup.
        if side == "long" and vwap_distance < -0.15:
            return "exclude", "breakout_lost_vwap_support"
        if side == "short" and vwap_distance > 0.15:
            return "exclude", "breakout_lost_vwap_resistance"
        return "pass", None
    return "pass", None


def _decorate_timing(row: dict, cfg: dict) -> None:
    """Persist signal-time and entry-time facts separately, then enforce expiry once more."""
    created = _as_utc(row.get("signal_created_at"))
    expires = _as_utc(row.get("signal_expires_at"))
    entry = _as_utc(row.get("entry_bar_at"))
    row["entry_session"] = _session_guard(entry, cfg) if entry is not None else None
    row["entry_bar_closed_at"] = None
    row["entry_delay_minutes"] = None
    row["entry_within_validity"] = None
    if entry is None:
        return
    close_at = entry + timedelta(minutes=max(0, int(row.get("bar_minutes") or 0)))
    row["entry_bar_closed_at"] = _iso(close_at)
    if created is not None:
        row["entry_delay_minutes"] = round((entry - created).total_seconds() / 60.0, 3)
    row["entry_within_validity"] = int(expires is not None and close_at <= expires)
    if row["entry_within_validity"]:
        return
    # Defence in depth: a future simulator change cannot accidentally credit a
    # stale intraday entry merely because it bypassed the normal walk deadline.
    row.update(status="skipped", skip_reason="entry_after_signal_expiry", net_usd=None,
               net_r=None, close_reason=None, entry_price=None, bars_to_entry=None,
               entry_order_type="none")


def _summary(rows: list[dict], *, source_count: int, entry_mode: str, variant: str,
             size_action: str, size_weight: float, notes: str) -> dict:
    resolved = [r for r in rows if r.get("status") == "resolved"]
    net_usd = sum(float(r.get("net_usd") or 0) for r in resolved)
    net_r = sum(float(r.get("net_r") or 0) for r in resolved)
    wins = [r for r in resolved if float(r.get("net_usd") or 0) > 0]
    gp = sum(float(r.get("net_usd") or 0) for r in wins)
    gl = -sum(float(r.get("net_usd") or 0) for r in resolved if float(r.get("net_usd") or 0) < 0)
    eligible = sum(1 for r in rows if r.get("status") not in (
        "guard_excluded", "disabled", "shadow_excluded", "feature_unavailable"))
    skipped = sum(1 for r in rows if r.get("status") == "skipped")
    unresolved = sum(1 for r in rows if r.get("status") == "unresolved")
    entries = [r for r in rows if r.get("entry_price") is not None]
    entry_bars = [int(r["bars_to_entry"]) for r in entries if r.get("bars_to_entry") is not None]
    feature_unavailable = sum(r.get("status") == "feature_unavailable" for r in rows)
    filter_excluded = sum(r.get("status") == "shadow_excluded" for r in rows)
    status = "FORWARD_REVIEW_ELIGIBLE" if len(resolved) >= MIN_RESOLVED_FORWARD else "INSUFFICIENT_FORWARD_SAMPLE"
    if variant in {name for values in SHADOW_FILTER_VARIANTS.values() for name, _ in values} and feature_unavailable:
        status = "AWAITING_POINT_IN_TIME_FEATURE_COVERAGE"
    if entry_mode == "BREAKOUT_CONTINUATION" and not any(r.get("strong_confirmation") for r in rows):
        status = "BLOCKED_STRONG_CONFIRMATION_EVIDENCE"
    return {"entry_mode": entry_mode, "variant": variant, "status": status,
            "source_signals": source_count, "eligible_signals": eligible, "resolved": len(resolved),
            "skipped": skipped, "unresolved": unresolved, "net_usd": round(net_usd, 2),
            "net_r": round(net_r, 4), "winrate": round(len(wins) / len(resolved), 4) if resolved else None,
            "profit_factor": round(gp / gl, 4) if gl else None, "size_action": size_action,
            "size_weight": size_weight, "notes": notes, "entries_observed": len(entries),
            "geometry_changed_signals": sum(int(r.get("geometry_changed") or 0) for r in rows),
            "mean_bars_to_entry": (round(sum(entry_bars) / len(entry_bars), 2) if entry_bars else None),
            "expired_entry_skips": sum(r.get("skip_reason") == "entry_after_signal_expiry" for r in rows),
            "filter_excluded": filter_excluded, "feature_unavailable": feature_unavailable}


def _run_identity(generated_at: str, cfg: dict, sample_count: int) -> tuple[str, str]:
    source = {"version": VERSION, "variants": VARIANTS, "shadow_filter_variants": SHADOW_FILTER_VARIANTS, "overlay": cfg,
              "sample_count": int(sample_count)}
    config_hash = hashlib.sha256(json.dumps(source, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:16]
    run_stamp = generated_at.replace("-", "").replace(":", "").replace("+00:00", "Z").replace(".", "")
    return f"{VERSION}:{run_stamp}:{config_hash}", config_hash


def refresh(*, db: str | None = None, limit: int = 400, persist: bool = True,
            write_report_file: bool | None = None, report_dir: str | None = None) -> dict:
    cfg_project = load_config()
    path = db or str(cfg_project.db_path)
    conn = sqlite3.connect(path)
    try:
        samples = _load_samples(conn, limit)
        cfg = load_cfg()
        from src.storage.file_store import FileStore
        from src.execution.paper_shadow_engine import _load_candles, select_fee_profile
        fs = FileStore(cfg_project)
        all_rows: list[dict] = []
        candles_by_id: dict[str, Any] = {}
        for s in samples:
            s["signal_session"] = _session_guard(s.get("created_at"), cfg)
            s["guard_excluded"] = s["signal_session"] in ("asia", "off")
            if not s["guard_excluded"]:
                candles_by_id[s["signal_id"]], _ = _load_candles(
                    fs, cfg_project, s.get("symbol"), s.get("mode"), s.get("asset_class"),
                    s.get("exchange_focus"), s.get("created_at"))
        summaries = []
        shadow_names = {name for values in SHADOW_FILTER_VARIANTS.values() for name, _ in values}
        for em, variants in VARIANTS.items():
            size_action = "HALF_SIZE" if em in ("BREAKOUT_CONTINUATION", "MOMENTUM_TAKER_NOW") else "FULL_SIZE_CONTROL"
            weight = HALF_SIZE if em in ("BREAKOUT_CONTINUATION", "MOMENTUM_TAKER_NOW") else 1.0
            for variant, note in (*variants, *SHADOW_FILTER_VARIANTS.get(em, ())):
                is_filter_variant = variant in shadow_names
                variant_action = (
                    "PAPER_COUNTERFACTUAL_ONLY"
                    if is_filter_variant and em == "BREAKOUT_CONTINUATION"
                    else "SHADOW_ONLY_COUNTERFACTUAL" if is_filter_variant else size_action
                )
                rows = []
                for s in samples:
                    if str(s.get("entry_mode") or "").upper() != em:
                        continue
                    base = {"signal_id": s["signal_id"], "entry_mode": em, "variant": variant,
                            # session_bucket is retained for the latest-view schema and means
                            # signal-time session. Entry-time session is recorded separately.
                            "session_bucket": s["signal_session"], "signal_session": s["signal_session"],
                            "signal_created_at": s.get("created_at"), "signal_expires_at": s.get("expires_at"),
                            "strong_confirmation": s["strong_confirmation"],
                            "size_action": variant_action, "size_weight": weight}
                    if s["guard_excluded"]:
                        base.update(status="guard_excluded", skip_reason="production_asia_off_guard")
                    elif _as_utc(s.get("expires_at")) is None:
                        base.update(status="skipped", skip_reason="missing_signal_expiry")
                    elif is_filter_variant:
                        filter_state, filter_reason = _shadow_filter_state(s, variant)
                        if filter_state == "unavailable":
                            base.update(status="feature_unavailable", skip_reason=filter_reason)
                        elif filter_state == "exclude":
                            base.update(status="shadow_excluded", skip_reason=filter_reason)
                        elif candles_by_id.get(s["signal_id"]) is None:
                            base.update(status="unresolved", skip_reason="ohlcv_unavailable")
                        else:
                            # The filter branch must be paired with the current
                            # production geometry, not a similarly named variant.
                            base.update(_simulate(_geom(s), candles_by_id[s["signal_id"]], "current",
                                                  fee_profile=select_fee_profile(s.get("asset_class")),
                                                  size_weight=weight, entry_expires_at=s.get("expires_at")))
                    elif _hold_policy(variant) and _hold_policy(variant).get("requires_light_quality"):
                        allowed, reason = _light_hold_quality(s)
                        if not allowed:
                            base.update(status="skipped", skip_reason=reason)
                        elif candles_by_id.get(s["signal_id"]) is None:
                            base.update(status="unresolved", skip_reason="ohlcv_unavailable")
                        else:
                            base.update(_simulate(_geom(s), candles_by_id[s["signal_id"]], variant,
                                                  fee_profile=select_fee_profile(s.get("asset_class")),
                                                  size_weight=weight, entry_expires_at=s.get("expires_at")))
                    elif em == "BREAKOUT_CONTINUATION" and not s["strong_confirmation"]:
                        base.update(status="skipped", skip_reason="strong_confirmation_not_available_at_entry")
                    elif variant == "strong_confirmation_only" and not s["strong_confirmation"]:
                        base.update(status="skipped", skip_reason="strong_confirmation_not_available_at_entry")
                    elif candles_by_id.get(s["signal_id"]) is None:
                        base.update(status="unresolved", skip_reason="ohlcv_unavailable")
                    else:
                        base.update(_simulate(_geom(s), candles_by_id[s["signal_id"]], variant,
                                              fee_profile=select_fee_profile(s.get("asset_class")),
                                              size_weight=weight, entry_expires_at=s.get("expires_at")))
                    _decorate_timing(base, cfg)
                    rows.append(base)
                summaries.append(_summary(rows, source_count=sum(1 for s in samples if str(s.get("entry_mode") or "").upper() == em),
                                          entry_mode=em, variant=variant, size_action=variant_action,
                                          size_weight=weight, notes=note))
                all_rows.extend(rows)
        # Explicit disabled lane is reported, never simulated.
        summaries.append({"entry_mode": "LIMIT_THEN_TAKER_TIMEOUT", "variant": "disabled",
                          "status": "DISABLED_BY_TEST_PLAN", "source_signals": 0,
                          "eligible_signals": 0, "resolved": 0, "skipped": 0, "unresolved": 0,
                          "net_usd": 0.0, "net_r": 0.0, "winrate": None, "profit_factor": None,
                          "size_action": "SHADOW_ONLY", "size_weight": 0.0,
                          "notes": "excluded from all parameter tests; production policy unchanged",
                          "entries_observed": 0, "geometry_changed_signals": 0,
                          "mean_bars_to_entry": None, "expired_entry_skips": 0,
                          "filter_excluded": 0, "feature_unavailable": 0})
        generated = datetime.now(timezone.utc).isoformat()
        run_id, config_hash = _run_identity(generated, cfg, len(samples))
        result = {"db_path": path, "generated_at": generated, "version": VERSION,
                  "run_id": run_id, "config_hash": config_hash, "persisted": bool(persist), "signals_sampled": len(samples),
                  "min_resolved_forward": MIN_RESOLVED_FORWARD, "variants": summaries,
                  "guardrail": "Asia/off excluded; overlay config and paper logic unchanged"}
        if persist:
            ensure_tables(conn)
            # Latest-view rows are replaceable; append-only history retains every run.
            conn.execute("DELETE FROM crypto_intraday_idea_sweep_results WHERE version=?", (VERSION,))
            conn.execute("DELETE FROM crypto_intraday_idea_sweep_trades WHERE version=?", (VERSION,))
            for x in summaries:
                conn.execute("""INSERT INTO crypto_intraday_idea_sweep_results
                    (generated_at,version,entry_mode,variant,status,source_signals,eligible_signals,
                     resolved,skipped,unresolved,net_usd,net_r,winrate,profit_factor,size_action,
                     size_weight,notes,entries_observed,geometry_changed_signals,mean_bars_to_entry,
                     filter_excluded,feature_unavailable)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                             (generated, VERSION, x["entry_mode"], x["variant"], x["status"], x["source_signals"],
                              x["eligible_signals"], x["resolved"], x["skipped"], x["unresolved"], x["net_usd"],
                              x["net_r"], x["winrate"], x["profit_factor"], x["size_action"], x["size_weight"],
                              x["notes"], x["entries_observed"], x["geometry_changed_signals"],
                              x["mean_bars_to_entry"], x["filter_excluded"], x["feature_unavailable"]))
            conn.commit()
            for row_index, x in enumerate(all_rows, start=1):
                conn.execute("""INSERT OR REPLACE INTO crypto_intraday_idea_sweep_trades
                    (generated_at,version,signal_id,entry_mode,variant,status,skip_reason,session_bucket,
                     strong_confirmation,size_action,size_weight,net_usd,net_r,close_reason,entry_rule,
                     confirmation_at,confirmation_price,simulation_start_at,entry_bar_at,entry_price,
                     bars_to_entry,entry_order_type,entry_low_used,entry_high_used,entry_trigger_used,
                     suggested_entry_used,stop_used,geometry_changed)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                             (generated, VERSION, x["signal_id"], x["entry_mode"], x["variant"], x.get("status"),
                              x.get("skip_reason"), x.get("session_bucket"), x.get("strong_confirmation"),
                              x.get("size_action"), x.get("size_weight"), x.get("net_usd"), x.get("net_r"),
                              x.get("close_reason"), x.get("entry_rule"), x.get("confirmation_at"),
                              x.get("confirmation_price"), x.get("simulation_start_at"), x.get("entry_bar_at"),
                              x.get("entry_price"), x.get("bars_to_entry"), x.get("entry_order_type"),
                              x.get("entry_low_used"), x.get("entry_high_used"), x.get("entry_trigger_used"),
                              x.get("suggested_entry_used"), x.get("stop_used"), x.get("geometry_changed")))
                if row_index % 100 == 0:
                    conn.commit()
            conn.commit()
            conn.execute("""INSERT INTO crypto_intraday_idea_sweep_runs
                         (run_id,generated_at,version,config_hash,signals_sampled,source_scope)
                         VALUES (?,?,?,?,?,?)""",
                         (run_id, generated, VERSION, config_hash, len(samples),
                          "crypto/intraday/new_logic_shadow/forward_since_activation/preentry_v2/data_quality=ok"))
            for x in summaries:
                conn.execute("""INSERT INTO crypto_intraday_idea_sweep_results_history
                             (run_id,generated_at,version,entry_mode,variant,status,source_signals,eligible_signals,
                              resolved,skipped,unresolved,expired_entry_skips,net_usd,net_r,winrate,profit_factor,
                              size_action,size_weight,notes,entries_observed,geometry_changed_signals,mean_bars_to_entry,
                              filter_excluded,feature_unavailable)
                             VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                             (run_id, generated, VERSION, x["entry_mode"], x["variant"], x["status"],
                              x["source_signals"], x["eligible_signals"], x["resolved"], x["skipped"],
                              x["unresolved"], x["expired_entry_skips"], x["net_usd"], x["net_r"],
                              x["winrate"], x["profit_factor"], x["size_action"], x["size_weight"],
                              x["notes"], x["entries_observed"], x["geometry_changed_signals"],
                              x["mean_bars_to_entry"], x["filter_excluded"], x["feature_unavailable"]))
            for row_index, x in enumerate(all_rows, start=1):
                conn.execute("""INSERT INTO crypto_intraday_idea_sweep_trades_history
                             (run_id,generated_at,version,signal_id,entry_mode,variant,status,skip_reason,
                              signal_session,entry_session,signal_created_at,signal_expires_at,entry_bar_at,
                              entry_bar_closed_at,entry_within_validity,entry_delay_minutes,strong_confirmation,
                              size_action,size_weight,net_usd,net_r,close_reason,entry_rule,confirmation_at,
                              confirmation_price,simulation_start_at,entry_price,bars_to_entry,entry_order_type,
                              entry_low_used,entry_high_used,entry_trigger_used,suggested_entry_used,stop_used,
                              geometry_changed)
                             VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                             (run_id, generated, VERSION, x["signal_id"], x["entry_mode"], x["variant"],
                              x.get("status"), x.get("skip_reason"), x.get("signal_session"), x.get("entry_session"),
                              x.get("signal_created_at"), x.get("signal_expires_at"), x.get("entry_bar_at"),
                              x.get("entry_bar_closed_at"), x.get("entry_within_validity"), x.get("entry_delay_minutes"),
                              x.get("strong_confirmation"), x.get("size_action"), x.get("size_weight"),
                              x.get("net_usd"), x.get("net_r"), x.get("close_reason"), x.get("entry_rule"),
                              x.get("confirmation_at"), x.get("confirmation_price"), x.get("simulation_start_at"),
                              x.get("entry_price"), x.get("bars_to_entry"), x.get("entry_order_type"),
                              x.get("entry_low_used"), x.get("entry_high_used"), x.get("entry_trigger_used"),
                              x.get("suggested_entry_used"), x.get("stop_used"), x.get("geometry_changed")))
                if row_index % 100 == 0:
                    conn.commit()
            conn.commit()
        result["matches_persisted_table"] = bool(persist and conn.execute(
            "SELECT count(*) FROM crypto_intraday_idea_sweep_results WHERE version=?", (VERSION,)).fetchone()[0] == len(summaries))
    finally:
        conn.close()
    do_report = (db is None) if write_report_file is None else bool(write_report_file)
    if do_report:
        write_report(result, report_dir)
    return result


def render_markdown(result: dict) -> str:
    lines = ["# Crypto Intraday Idea Sweep (read-model only)", "",
             f"- version: `{result.get('version')}`",
             f"- run_id: `{result.get('run_id')}`",
             f"- config_hash: `{result.get('config_hash')}`",
             f"- generated_at: `{result.get('generated_at')}`",
             f"- signals_sampled: **{result.get('signals_sampled', 0)}**",
             f"- minimum resolved forward trades: **{MIN_RESOLVED_FORWARD}**",
             "- Source: crypto / intraday / new_logic_shadow / forward_since_activation / preentry_v2 / data_quality=ok.",
             "- Asia/off rows are excluded by the existing production guard. No config, routing, live, final_r, or actionability writes.", ""]
    for x in result.get("variants", []):
        lines.append(f"## {x['entry_mode']} / {x['variant']}")
        lines.append("")
        lines.append(f"Status: **{x['status']}**; resolved={x['resolved']}; skipped={x['skipped']}; "
                     f"unresolved={x['unresolved']}; net=${x['net_usd']:.2f}; net R={x['net_r']:.4f}; "
                     f"winrate={x['winrate'] if x['winrate'] is not None else 'n/a'}; "
                     f"PF={x['profit_factor'] if x['profit_factor'] is not None else 'n/a'}; "
                     f"size={x['size_action']}")
        lines.append(f"Execution diagnostics: entries={x.get('entries_observed', 0)}; "
                     f"geometry changed={x.get('geometry_changed_signals', 0)}; "
                     f"mean bars to entry={x.get('mean_bars_to_entry') if x.get('mean_bars_to_entry') is not None else 'n/a'}; "
                     f"expired-entry skips={x.get('expired_entry_skips', 0)}; "
                     f"filter-excluded={x.get('filter_excluded', 0)}; "
                     f"feature-unavailable={x.get('feature_unavailable', 0)}")
        lines.append(f"Note: {x['notes']}")
        lines.append("")
    lines.append("No variant is auto-promoted. A result becomes reviewable only after the resolved forward gate; operator sign-off remains required.")
    return "\n".join(lines)


def write_report(result: dict, out_dir: str | None = None) -> str:
    base = Path(out_dir) if out_dir else _root() / "reports"
    base.mkdir(parents=True, exist_ok=True)
    out = base / "CRYPTO_INTRADAY_IDEA_SWEEP.md"
    out.write_text(render_markdown(result), encoding="utf-8")
    return str(out)


__all__ = ["refresh", "render_markdown", "write_report", "pullback_confirmation_gate",
           "MIN_RESOLVED_FORWARD", "VERSION"]
