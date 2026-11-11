"""Move 3 — wide-net shadow A/B lane (READ-MODEL / paper only).

Why the primary forward sample is small: the live shadow only processes signals the tracker marked
`entry_triggered=1` within its 9-day rolling window, and the new logic then SKIPS ~2/3 of those.
So paired (A filled AND B filled) forward trades accrue slowly — a handful per mode.

This lane widens the sample WITHOUT touching live behaviour or the authoritative lane:
  * it evaluates BOTH branches (old_paper vs new_logic_shadow) over EVERY forward proposed_signal —
    not just the trigger-gated subset — using the Move-1 DEEP history store and each signal's real
    validity horizon, so signals the live tracker never processed still get an A/B outcome;
  * results land in a SEPARATE table `paper_shadow_wide_outcomes` (lane='wide_net_deep_history'),
    NEVER in paper_shadow_execution_outcomes, so the primary promotion evidence is unchanged.

It is a PROVISIONAL, faster-accumulating read (feeds the SPRT `--source wide` and Move-4
reconciliation), explicitly NOT the authoritative live rolling-cache forward evidence. Reuses the
exact same simulate_branch engine, so A/B semantics are identical — only the candle source (deep
history) and the signal set (all forward, not trigger-gated) differ. proposed_signals is read-only;
never writes final_r / the live lane; live locked.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.execution.paper_shadow_engine import (
    _asset_is_stock, _f, _overlays, DEFAULT_FEE_PROFILE,
    select_fee_profile, simulate_branch,
)
from src.backtest.settings_replay import load_deep_frame, _horizon_end


def _activation_ro(conn) -> str:
    """Read the forward-lane activation instant STRICTLY read-only. Unlike paper_shadow_engine's
    _activation_iso this NEVER writes paper_shadow_meta — the wide lane must not create activation
    state. If unset, fall back to epoch so every signal counts as forward (safe for this crypto
    read-model lane)."""
    try:
        row = conn.execute("SELECT v FROM paper_shadow_meta WHERE k='activated_at'").fetchone()
        if row and row[0]:
            return row[0]
    except sqlite3.OperationalError:
        pass
    return "1970-01-01T00:00:00+00:00"

LANE = "wide_net_deep_history"

_DDL = """
CREATE TABLE IF NOT EXISTS paper_shadow_wide_outcomes (
  generated_at TEXT, lane TEXT, signal_id TEXT, branch TEXT, symbol TEXT, asset_class TEXT,
  mode TEXT, entry_mode TEXT, window TEXT, entry_fill_status TEXT, entry_fill_time TEXT,
  net_r REAL, net_pnl_usdt REAL, PRIMARY KEY (signal_id, branch)
);
"""


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def _forward_signals(conn, activation: str, limit: int) -> list[dict]:
    """ALL forward crypto proposed_signals (not trigger-gated), shaped for simulate_branch."""
    import pandas as pd  # noqa: F401  (kept for parity with deep loader dtypes)
    rows = conn.execute(
        "SELECT signal_id, symbol, direction, mode, asset_class, setup_type, market_regime, "
        "exchange_focus, created_at, suggested_entry, entry_trigger, entry_low, entry_high, "
        "stop_loss, invalidation, tp1, tp2, tp3, validity_window_hours, expires_at "
        "FROM proposed_signals WHERE asset_class='crypto' AND created_at >= ? "
        "AND suggested_entry IS NOT NULL ORDER BY created_at DESC LIMIT ?",
        (activation, int(limit))).fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM proposed_signals LIMIT 0").description]
    out = []
    for r in rows:
        d = dict(zip(
            ["signal_id", "symbol", "direction", "mode", "asset_class", "setup_type",
             "market_regime", "exchange_focus", "created_at", "suggested_entry", "entry_trigger",
             "entry_low", "entry_high", "stop_loss", "invalidation", "tp1", "tp2", "tp3",
             "validity_window_hours", "expires_at"], r))
        entry = _f(d.get("entry_trigger")) or _f(d.get("suggested_entry")) or _f(d.get("entry_low"))
        stop = _f(d.get("invalidation")) or _f(d.get("stop_loss"))
        out.append({
            "signal_id": d["signal_id"], "symbol": d["symbol"],
            "direction": (d.get("direction") or "long").lower(), "mode": d.get("mode"),
            "asset_class": d.get("asset_class"), "playbook": d.get("setup_type") or "",
            "regime": d.get("market_regime") or "", "exchange_focus": d.get("exchange_focus") or "",
            "created_at": d.get("created_at"), "entry_low": _f(d.get("entry_low")),
            "entry_high": _f(d.get("entry_high")), "entry_trigger": _f(d.get("entry_trigger")),
            "suggested_entry": _f(d.get("suggested_entry")), "tp1": _f(d.get("tp1")),
            "tp2": _f(d.get("tp2")), "tp3": _f(d.get("tp3")), "stop0": stop,
            "validity_window_hours": d.get("validity_window_hours"), "expires_at": d.get("expires_at"),
            "economic_trade_key": "|".join(str(x) for x in (
                d["symbol"], (d.get("direction") or "").lower(), (d.get("mode") or "").lower(),
                round(entry or 0, 8), str(d.get("created_at"))[:10])),
        })
    return out


def refresh(*, db: str | None = None, limit: int = 5000, persist: bool = True,
            now_iso: str | None = None) -> dict[str, Any]:
    """Build the wide-net A/B lane over deep history. Reads proposed_signals + deep store; writes
    ONLY paper_shadow_wide_outcomes. Never the live lane, final_r, or any live path."""
    from src.config import load_config
    import pandas as pd
    cfg = load_config()
    path = db or str(cfg.db_path)
    generated_at = now_iso or datetime.now(timezone.utc).isoformat()

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        activation = _activation_ro(conn)          # STRICTLY read-only; never writes activation state
        sigs = _forward_signals(conn, activation, limit)
        frame_cache: dict[tuple, tuple] = {}
        results: list[dict] = []
        covered = 0
        for sig in sigs:
            ckey = (sig["symbol"], sig["mode"], sig["exchange_focus"])
            if ckey not in frame_cache:
                frame_cache[ckey] = load_deep_frame(cfg, sig["symbol"], sig["mode"], sig["exchange_focus"])
            full, _ex, _tf = frame_cache[ckey]
            if full is None or full.empty:
                continue
            start = pd.to_datetime(sig["created_at"], utc=True)
            end = _horizon_end(sig, sig["created_at"])
            post = full[(full["timestamp"] >= start) & (full["timestamp"] <= end)]
            if post.empty:
                continue
            covered += 1
            ov = _overlays(conn, sig["signal_id"])
            fp = select_fee_profile(sig.get("asset_class"), DEFAULT_FEE_PROFILE)
            for branch in ("old_paper", "new_logic_shadow"):
                rec, _events = simulate_branch(branch, sig, ov, post.reset_index(drop=True), fp)
                results.append({
                    "signal_id": sig["signal_id"], "branch": branch, "symbol": sig["symbol"],
                    "asset_class": sig.get("asset_class"), "mode": sig.get("mode"),
                    "entry_mode": rec.get("entry_mode"), "window": "forward_since_activation",
                    "entry_fill_status": rec.get("entry_fill_status"),
                    "entry_fill_time": rec.get("entry_fill_time"),
                    "net_r": rec.get("net_r"), "net_pnl_usdt": rec.get("net_pnl_usdt"),
                })
    finally:
        conn.close()

    persisted_rows = None
    if persist:
        wconn = sqlite3.connect(path)
        try:
            wconn.execute("DROP TABLE IF EXISTS paper_shadow_wide_outcomes")
            wconn.execute(_DDL)
            for r in results:
                wconn.execute(
                    "INSERT OR REPLACE INTO paper_shadow_wide_outcomes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (generated_at, LANE, r["signal_id"], r["branch"], r["symbol"], r["asset_class"],
                     r["mode"], r["entry_mode"], r["window"], r["entry_fill_status"],
                     r["entry_fill_time"], r["net_r"], r["net_pnl_usdt"]))
            wconn.commit()
            persisted_rows = wconn.execute(
                "SELECT count(*), max(generated_at) FROM paper_shadow_wide_outcomes").fetchone()
        finally:
            wconn.close()

    # widening factor: paired (A filled AND B filled) per mode on the wide lane
    filled = {}
    for r in results:
        if r["entry_fill_status"] == "filled":
            filled.setdefault(r["signal_id"], {})[r["branch"]] = r["mode"]
    wide_pairs: dict[str, int] = {}
    for sid, br in filled.items():
        if "old_paper" in br and "new_logic_shadow" in br:
            wide_pairs[br["old_paper"] or "?"] = wide_pairs.get(br["old_paper"] or "?", 0) + 1

    return {
        "db_path": str(path), "generated_at": generated_at, "persisted": bool(persist),
        "lane": LANE, "signals_considered": len(sigs), "signals_covered": covered,
        "rows_written": len(results), "wide_pairs_by_mode": wide_pairs,
        "matches_persisted_table": bool(persist and persisted_rows and persisted_rows[0] == len(results)
                                        and persisted_rows[1] == generated_at),
    }


__all__ = ["refresh", "LANE"]
