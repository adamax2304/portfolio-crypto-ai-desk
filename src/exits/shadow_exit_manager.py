"""Shadow exit manager (FAST SAFE ACCELERATION PART 3).

ARCHIVED 2026-06-24 — SUPERSEDED_BY_MODEL_F. The BE/partial/trailing/reentry
variants A..I here arm protection at/after TP1 (~1R away), which the viability +
PnL audits showed is inferior: most favorable excursion dies in the +0.5R→TP1
zone, so arming there leaves the actionable book net-negative. The authoritative
paper risk model is now `src/execution/paper_execution_accounting.py` (Model F:
early MFE-armed protection — BE @ +0.6R, lock +0.5R @ +1R, runner TP3), active in
paper accounting. This module is **kept for research/replay only** (used by
`scripts/shadow_exit_ledger_update.py`, `scripts/tp_stop_replay.py`); it is NOT
wired into the tracker/scheduler and must NOT be promoted to paper/production
without re-clearing the gates. See `config/paper_features.yaml`
(`shadow_exit_manager_variants: state: archived`) and
`reports/SHADOW_FEATURE_ARCHIVE_REPORT.md`.

For a filled trade + its OHLCV path, computes what alternative exit rules WOULD have
produced — candle-by-candle, in order. Shadow measurement ONLY: it does not change
real exits, does not enable partial_exit_model, and does not mutate actual outcomes.

Same-candle rule: if stop and a target are both touched in one candle, the stop is
taken first (conservative; matches the production tracker).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

VARIANTS = [
    "A_current", "B_BE_0.5R", "C_BE_1R", "D_partial50_1R", "E_partial50_1R_BE",
    "F_trail_1R", "G_candle_close_stop", "H_no_reentry", "I_one_reentry",
]

ROOT = Path(__file__).resolve().parent.parent.parent
ARCHIVE_DIR = ROOT / "data" / "archive" / "ohlcv"
CACHE_DIR = ROOT / "data" / "raw" / "ohlcv"
EXCHANGES = ("binance", "bybit", "mexc")
TFS = ("5m", "15m", "1h")


def ohlcv_path(ex: str, tf: str, sym: str):
    """Archive-first, then rolling cache."""
    arch = ARCHIVE_DIR / ex / tf / f"{sym}.csv"
    if arch.exists():
        return arch
    cache = CACHE_DIR / ex / tf / f"{sym}.csv"
    return cache if cache.exists() else None


def load_path(symbol: str):
    """Return (candles_list, exchange, tf) finest-TF available, archive-first."""
    import pandas as pd
    sym = symbol.replace("/", "_").upper()
    for tf in TFS:
        for ex in EXCHANGES:
            p = ohlcv_path(ex, tf, sym)
            if p is None:
                continue
            try:
                df = pd.read_csv(p)
                df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
                return df, ex, tf
            except Exception:
                continue
    return None, None, None


def _r_at(price, entry, r_unit, long):
    return (price - entry) / r_unit if long else (entry - price) / r_unit


def simulate_variant(variant, entry, stop, tps, direction, candles):
    """Return a dict: shadow_R, exit_reason, touched_0_5R, touched_1R,
    moved_to_BE, partial_taken, stopped_after_BE. Pure."""
    long = (direction or "long").lower() != "short"
    r_unit = abs(entry - stop)
    out = {"shadow_R": None, "exit_reason": "no_data", "touched_0_5R": False,
           "touched_1R": False, "moved_to_BE": False, "partial_taken": False,
           "stopped_after_BE": False}
    if r_unit == 0 or not candles:
        return out
    tlist = [t for t in tps if t is not None]
    tlist = sorted(tlist) if long else sorted(tlist, reverse=True)

    active_stop = stop
    peak_r = 0.0
    booked = 0.0
    remaining = 1.0
    moved_be = False
    partial = False
    reentered = False

    def hit_stop(c):
        return (c["low"] <= active_stop) if long else (c["high"] >= active_stop)

    def hit_stop_close(c):
        return (c["close"] <= active_stop) if long else (c["close"] >= active_stop)

    def hit(c, px):
        return (c["high"] >= px) if long else (c["low"] <= px)

    for c in candles:
        cand_r = _r_at(c["high"] if long else c["low"], entry, r_unit, long)
        peak_r = max(peak_r, cand_r)
        if peak_r >= 0.5:
            out["touched_0_5R"] = True
        if peak_r >= 1.0:
            out["touched_1R"] = True

        if variant == "B_BE_0.5R" and peak_r >= 0.5 and not moved_be:
            active_stop = entry; moved_be = True; out["moved_to_BE"] = True
        if variant in ("C_BE_1R", "D_partial50_1R", "E_partial50_1R_BE") and peak_r >= 1.0 and not moved_be:
            if variant != "D_partial50_1R":  # D moves BE only on the partial book below
                active_stop = entry; moved_be = True; out["moved_to_BE"] = True
        if variant == "F_trail_1R" and peak_r >= 1.0:
            trail = entry + (peak_r - 1.0) * r_unit if long else entry - (peak_r - 1.0) * r_unit
            active_stop = max(active_stop, trail) if long else min(active_stop, trail)

        if variant in ("D_partial50_1R", "E_partial50_1R_BE") and remaining == 1.0 and tlist and hit(c, tlist[0]):
            booked += 0.5 * _r_at(tlist[0], entry, r_unit, long)
            remaining = 0.5; partial = True; out["partial_taken"] = True
            active_stop = entry; moved_be = True; out["moved_to_BE"] = True

        stopped = hit_stop_close(c) if variant == "G_candle_close_stop" else hit_stop(c)
        if stopped:
            exit_r = _r_at(active_stop, entry, r_unit, long)
            total = booked + remaining * exit_r
            if variant == "I_one_reentry" and not reentered and exit_r <= -0.99:
                reentered = True
                continue
            out["shadow_R"] = round(total, 3)
            out["exit_reason"] = "be_stop" if moved_be and abs(exit_r) < 0.05 else "stop"
            out["stopped_after_BE"] = bool(moved_be and abs(exit_r) < 0.05)
            return out

        if tlist and hit(c, tlist[-1]):
            total = booked + remaining * _r_at(tlist[-1], entry, r_unit, long)
            out["shadow_R"] = round(total, 3)
            out["exit_reason"] = "target"
            return out

    last = candles[-1]
    total = booked + remaining * _r_at(last["close"], entry, r_unit, long)
    out["shadow_R"] = round(total, 3)
    out["exit_reason"] = "window_end"
    return out


def shadow_rows_for_trade(trade: dict[str, Any], candles, *, exchange=None, tf=None,
                          coverage_status=None):
    """Build one ledger row per variant for a single trade. ``candles`` may be
    None → all rows get coverage_status='missing_data' and shadow_R=None (no fake).
    ``coverage_status`` (covered/partial_data/missing_data) is set by the caller,
    which knows whether the OHLCV window spans the full entry→exit (do not over-
    report coverage — only a full-span window is 'covered')."""
    actual_r = trade.get("actual_R")
    try:
        actual_r = float(actual_r) if actual_r is not None else None
    except (TypeError, ValueError):
        actual_r = None
    entry, stop = trade.get("entry"), trade.get("stop")
    tps = [trade.get("tp1"), trade.get("tp2"), trade.get("tp3")]
    direction = trade.get("direction") or "long"
    rows = []
    coverage = coverage_status or ("covered" if candles else "missing_data")
    for v in VARIANTS:
        base = {
            "signal_id": trade.get("signal_id"), "symbol": trade.get("symbol"),
            "asset_class": trade.get("asset_class"), "mode": trade.get("mode"),
            "tier": trade.get("tier"), "direction": direction,
            "entry_time": trade.get("entry_time"), "exit_time": trade.get("exit_time"),
            "entry": entry, "stop": stop, "tp": tps[0],
            "actual_R": actual_r, "variant": v, "shadow_R": None,
            "exit_reason": "missing_data", "touched_0_5R": "", "touched_1R": "",
            "moved_to_BE": "", "partial_taken_time": "", "stopped_after_BE": "",
            "winner_clipped": "", "loser_saved": "",
            "data_timeframe_used": tf or "", "data_coverage_status": coverage,
        }
        if candles and entry is not None and stop is not None:
            sim = simulate_variant(v, float(entry), float(stop),
                                   [float(x) if x is not None else None for x in tps],
                                   direction, candles)
            sr = sim["shadow_R"]
            base.update({
                "shadow_R": sr, "exit_reason": sim["exit_reason"],
                "touched_0_5R": sim["touched_0_5R"], "touched_1R": sim["touched_1R"],
                "moved_to_BE": sim["moved_to_BE"],
                "stopped_after_BE": sim["stopped_after_BE"],
                "winner_clipped": bool(actual_r is not None and sr is not None
                                       and actual_r > 0 and sr < actual_r),
                "loser_saved": bool(actual_r is not None and sr is not None
                                    and actual_r < 0 and sr > actual_r),
            })
        rows.append(base)
    return rows
