"""Entry-mode parameter sweep (READ-MODEL / EXPERIMENTAL / NEVER AUTO-APPLIED).

Re-simulates real FORWARD signals under VARIED entry/exit geometry, using the shared
MODE-SPECIFIC fill + Model-F protection simulator (src/execution/profit_protection.py),
to see which parameter settings would have produced more edge — WITHOUT changing any
production behaviour. One-factor-at-a-time (each parameter varied while the others stay
at 'current'), so each knob's effect is isolated.

SOURCE (default): eligible `new_logic_shadow` rows in `paper_shadow_execution_outcomes`
with window = 'forward_since_activation' (NOT just the latest proposed_signals). Backfill
is excluded by default. CLI filters: asset_class / mode / entry_mode / branch / window / since.

Swept parameters (config/entry_mode_calibration.yaml -> parameter_sweep):
  structural_stop_atr_buffer, breakout_trigger_offset_atr, pullback_zone_depth_atr,
  maker_trade_through_bps (affects the fill CONDITION, not a cost subtraction),
  limit_then_taker_timeout_bars, taker_fallback_enabled.

Source tables are READ-ONLY. Read-model writes: `entry_mode_parameter_sweep_results` +
reports/ENTRY_MODE_PARAMETER_SWEEP.md. NEVER writes proposed_signals / signal_outcomes /
final_r; no live; nothing is applied.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.execution import profit_protection as pp
from src.execution.entry_mode_calibration import load_calibration_config, RISK_USD, FORWARD, BRANCH_NEW


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def _f(v):
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return None


def _atr_proxy(entry, stop):
    if entry is None or stop is None:
        return None
    d = abs(entry - stop)
    return (d / 1.2) if d > 0 else None


def _variant_geometry(param: str, value, geom: dict) -> tuple[dict, dict]:
    """Return (modified_geometry, extra_kwargs) for a variant. `extra_kwargs` are passed to
    simulate_from_geometry (timeout_bars / taker_fallback / maker_trade_through_bps)."""
    g = dict(geom)
    kw: dict = {}
    if value == "current":
        return g, kw
    entry, stop = g.get("entry"), g.get("stop")
    atr = _atr_proxy(entry, stop) or (abs((entry or 0) - (stop or 0)) or 1.0)
    long = str(g.get("direction") or "long").lower() != "short"
    if param == "structural_stop_atr_buffer":
        buf = float(value) * atr
        g["stop"] = (stop - buf) if long else (stop + buf)          # wider structural stop
    elif param == "breakout_trigger_offset_atr":
        off = float(value) * atr
        if g.get("entry_trigger") is not None:
            g["entry_trigger"] = g["entry_trigger"] + (off if long else -off)
    elif param == "pullback_zone_depth_atr":
        depth = {"shallow": 0.25, "deeper": 0.75}.get(value)
        if depth is not None and g.get("entry_low") is not None and g.get("entry_high") is not None:
            band = abs(g["entry_high"] - g["entry_low"]) or atr
            adj = (depth - 0.5) * band
            if long:
                g["entry_low"] = g["entry_low"] - adj
            else:
                g["entry_high"] = g["entry_high"] + adj
    elif param == "maker_trade_through_bps":
        # affects the FILL CONDITION (how far price must trade through the limit), not a cost hack
        kw["maker_trade_through_bps"] = float(value) / 10000.0
    elif param == "limit_then_taker_timeout_bars":
        kw["timeout_bars"] = None if int(value) == 0 else int(value)
    elif param == "taker_fallback_enabled":
        # taker fallback only meaningful for LIMIT_THEN_TAKER_TIMEOUT; off -> disable timeout fallback
        if not bool(value):
            kw["timeout_bars"] = None
    return g, kw


def sweep_signal(geom: dict, candles: Any, cfg: dict, *, fee_profile: str = "bybit_non_vip_usdt_perp") -> dict:
    """Run all parameter variants for ONE signal on its real candles (pure; candles supplied).
    Returns {param: {variant_label: ProtectedResult.to_dict()}}."""
    grids = (cfg.get("parameter_sweep") or {})
    out: dict[str, dict] = {}
    for param, values in grids.items():
        if param in ("enabled", "max_signals") or not isinstance(values, list):
            continue
        out[param] = {}
        vals = ["current"] + [v for v in values if str(v) != "current"]
        for val in vals:
            g, kw = _variant_geometry(param, val, geom)
            res = pp.simulate_from_geometry(
                direction=g.get("direction") or "long", entry_low=g.get("entry_low"),
                entry_high=g.get("entry_high"), entry_trigger=g.get("entry_trigger"),
                suggested=g.get("entry"), stop=g.get("stop"), tp1=g.get("tp1"), tp2=g.get("tp2"),
                tp3=g.get("tp3"), candles=candles, entry_mode=g.get("entry_mode"),
                symbol=g.get("symbol") or "", fee_profile=fee_profile, **kw)
            out[param][str(val)] = res.to_dict()
    return out


# --------------------------------------------------------------------------- DB driver
def _has(conn, t):
    return bool(conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (t,)).fetchone())


def _load_forward_sample(conn, *, limit: int, asset_class=None, mode=None, entry_mode=None,
                         branch=BRANCH_NEW, window=FORWARD, since=None) -> list[dict]:
    """Default source = eligible shadow rows (forward_since_activation, new_logic_shadow) joined to
    proposed_signals for geometry. Uses COALESCE(invalidation, stop_loss) as the stop."""
    if not (_has(conn, "paper_shadow_execution_outcomes") and _has(conn, "proposed_signals")):
        return []
    where = ["s.branch = ?", "s.window = ?"]
    args: list = [branch, window]
    # Crypto forward evidence is valid only after the lookahead-safe pre-entry
    # classifier was activated. Older rows remain useful for historical study,
    # but must never leak into a forward parameter ranking.
    outcome_cols = {r[1] for r in conn.execute("PRAGMA table_info(paper_shadow_execution_outcomes)")}
    if "entry_mode_version" in outcome_cols:
        where.append("(lower(COALESCE(s.asset_class,'')) <> 'crypto' OR s.entry_mode_version = 'preentry_v2')")
    if asset_class:
        where.append("lower(s.asset_class) = ?"); args.append(str(asset_class).lower())
    if mode:
        where.append("lower(p.mode) = ?"); args.append(str(mode).lower())
    if entry_mode:
        where.append("upper(s.entry_mode) = ?"); args.append(str(entry_mode).upper())
    if since:
        where.append("p.created_at >= ?"); args.append(str(since))
    sql = f"""
      SELECT DISTINCT s.signal_id, p.symbol, p.direction, p.mode, p.asset_class, p.exchange_focus,
             p.created_at, p.entry_low, p.entry_high, p.entry_trigger, p.suggested_entry,
             COALESCE(p.invalidation, p.stop_loss) AS stop_used,
             p.tp1, p.tp2, p.tp3, s.entry_mode
      FROM paper_shadow_execution_outcomes s
      JOIN proposed_signals p ON p.signal_id = s.signal_id
      WHERE {' AND '.join(where)}
      ORDER BY p.created_at DESC LIMIT ?
    """
    args.append(int(limit))
    cols = [d[0] for d in conn.execute(sql, args).description]
    return [dict(zip(cols, r)) for r in conn.execute(sql, args).fetchall()]


def _agg(results: list[dict]) -> dict:
    acc: dict[tuple, dict] = {}
    for per_sig in results:
        for param, variants in per_sig.items():
            for val, d in variants.items():
                if d.get("skipped") or d.get("net_usd") is None:
                    acc.setdefault((param, val), {"n": 0, "usd": 0.0, "r": 0.0, "w": 0, "gp": 0.0, "gl": 0.0, "skip": 0})
                    acc[(param, val)]["skip"] += 1
                    continue
                a = acc.setdefault((param, val), {"n": 0, "usd": 0.0, "r": 0.0, "w": 0, "gp": 0.0, "gl": 0.0, "skip": 0})
                a["n"] += 1
                a["usd"] += d["net_usd"]
                a["r"] += d.get("net_r") or 0.0
                if d["net_usd"] > 0:
                    a["w"] += 1; a["gp"] += d["net_usd"]
                elif d["net_usd"] < 0:
                    a["gl"] += -d["net_usd"]
    out = []
    for (param, val), a in acc.items():
        out.append({"param": param, "variant": val, "trades": a["n"], "skipped": a["skip"],
                    "net_usd": round(a["usd"], 2), "net_r": round(a["r"], 3),
                    "winrate": round(a["w"] / a["n"], 4) if a["n"] else None,
                    "profit_factor": round(a["gp"] / a["gl"], 4) if a["gl"] > 0 else None})
    return {"variants": out}


_DDL = """
CREATE TABLE IF NOT EXISTS entry_mode_parameter_sweep_results (
  generated_at TEXT, param TEXT, variant TEXT, trades INTEGER, skipped INTEGER, net_usd REAL,
  net_r REAL, winrate REAL, profit_factor REAL, PRIMARY KEY (param, variant)
);
"""


MIN_SWEPT_FOR_CONCLUSION = 30   # below this the sweep 'best' is a ranking diagnostic, not a signal


def refresh(*, db: str | None = None, limit: int | None = None, persist: bool = True,
            asset_class=None, mode=None, entry_mode=None, branch: str = BRANCH_NEW,
            window: str = FORWARD, since=None, write_report_file: bool | None = None,
            report_dir: str | None = None) -> dict[str, Any]:
    """DB-driven sweep over the FORWARD eligible sample. Source tables read-only; read-model writes
    the results TABLE into the given db (persist). The GLOBAL report is written ONLY when
    write_report_file is True — DEFAULTS TO (db is None), so a test/temp db never overwrites the
    production report. Never writes proposed_signals / signal_outcomes / final_r."""
    from src.config import load_config
    from src.storage.file_store import FileStore
    from src.execution.paper_shadow_engine import _load_candles
    cfg_proj = load_config()
    fs = FileStore(cfg_proj)
    cfg = load_calibration_config()
    cap = limit or int((cfg.get("parameter_sweep") or {}).get("max_signals", 400))
    path = db or str(cfg_proj.db_path)
    conn = sqlite3.connect(path)
    persisted_rows = None
    try:
        sample = _load_forward_sample(conn, limit=cap, asset_class=asset_class, mode=mode,
                                      entry_mode=entry_mode, branch=branch, window=window, since=since)
        per_sig = []
        used = 0
        for s in sample:
            fee_profile = ("stock_etf_default" if str(s.get("asset_class") or "").lower().startswith("stock")
                           else "bybit_non_vip_usdt_perp")
            candles, _ = _load_candles(fs, cfg_proj, s.get("symbol"), s.get("mode"),
                                       s.get("asset_class"), s.get("exchange_focus"), s.get("created_at"))
            if candles is None or getattr(candles, "empty", True):
                continue
            geom = {"direction": s.get("direction"), "entry_low": _f(s.get("entry_low")),
                    "entry_high": _f(s.get("entry_high")), "entry_trigger": _f(s.get("entry_trigger")),
                    "entry": _f(s.get("suggested_entry")), "stop": _f(s.get("stop_used")),
                    "tp1": _f(s.get("tp1")), "tp2": _f(s.get("tp2")), "tp3": _f(s.get("tp3")),
                    "entry_mode": s.get("entry_mode"), "symbol": s.get("symbol")}
            per_sig.append(sweep_signal(geom, candles, cfg, fee_profile=fee_profile))
            used += 1
        agg = _agg(per_sig)
        coverage_status = "OK" if used >= MIN_SWEPT_FOR_CONCLUSION else "INSUFFICIENT_COVERAGE"
        result = {"db_path": str(path), "generated_at": datetime.now(timezone.utc).isoformat(),
                  "persisted": bool(persist),
                  "source": {"branch": branch, "window": window, "asset_class": asset_class,
                             "mode": mode, "entry_mode": entry_mode, "since": since},
                  "signals_swept": used, "signals_sampled": len(sample),
                  "coverage_status": coverage_status,
                  "min_swept_for_conclusion": MIN_SWEPT_FOR_CONCLUSION, **agg}
        if persist:
            conn.execute("DROP TABLE IF EXISTS entry_mode_parameter_sweep_results")
            conn.execute(_DDL)
            for v in agg["variants"]:
                conn.execute("INSERT OR REPLACE INTO entry_mode_parameter_sweep_results VALUES (?,?,?,?,?,?,?,?,?)",
                             (result["generated_at"], v["param"], v["variant"], v["trades"], v["skipped"],
                              v["net_usd"], v["net_r"], v["winrate"], v["profit_factor"]))
            conn.commit()
            # read the table back so the report can attest it matches what was persisted
            persisted_rows = conn.execute(
                "SELECT count(*), max(generated_at) FROM entry_mode_parameter_sweep_results").fetchone()
    finally:
        conn.close()
    result["matches_persisted_table"] = bool(
        persist and persisted_rows and persisted_rows[0] == len(agg["variants"])
        and persisted_rows[1] == result["generated_at"])
    do_report = (db is None) if write_report_file is None else bool(write_report_file)
    if do_report:
        write_report(result, out_dir=report_dir)
    return result


def render_markdown(result: dict) -> str:
    mark = "PERSISTED (read-model table written)" if result.get("persisted") else "DRY-RUN (nothing written)"
    src = result.get("source", {})
    swept = result.get("signals_swept", 0)
    cov = result.get("coverage_status", "OK")
    insufficient = cov == "INSUFFICIENT_COVERAGE"
    L = ["# Entry-Mode Parameter Sweep (read-model — NEVER auto-applied)", "",
         f"- db_path: `{result.get('db_path')}`",
         f"- generated_at: `{result['generated_at']}`  ·  **{mark}**",
         f"- matches persisted table: **{str(bool(result.get('matches_persisted_table'))).lower()}**",
         f"- signals_swept: **{swept}** / signals_sampled: {result.get('signals_sampled')} "
         "(forward evidence only; backfill excluded by default)",
         f"- coverage_status: **{cov}** (min {result.get('min_swept_for_conclusion', 30)} to draw a conclusion)",
         f"- source tables READ-ONLY: paper_shadow_execution_outcomes (branch={src.get('branch')}, "
         f"window={src.get('window')}) joined proposed_signals; filters "
         f"asset={src.get('asset_class')} mode={src.get('mode')} entry_mode={src.get('entry_mode')} "
         f"since={src.get('since')}",
         "- Each parameter varied one-at-a-time; others at `current`. Mode-specific fills + Model-F "
         "protection. maker_trade_through_bps affects the FILL condition, not a cost hack.", ""]
    if insufficient:
        L.append(f"> **INSUFFICIENT COVERAGE — ranking diagnostic only; NOT enough evidence for a "
                 f"trading conclusion (swept {swept} < {result.get('min_swept_for_conclusion', 30)}). "
                 f"No variant is marked 'best'.**")
        L.append("")
    by_param: dict[str, list] = {}
    for v in result.get("variants", []):
        by_param.setdefault(v["param"], []).append(v)
    for param, rows in sorted(by_param.items()):
        L.append(f"## {param}")
        L.append("")
        L.append("| variant | trades | skipped | net USD | net R | winrate | PF |")
        L.append("|---|--:|--:|--:|--:|--:|--:|")
        # only star a 'best' when coverage is sufficient — otherwise it's not a trading conclusion
        best = (max(rows, key=lambda r: r["net_usd"]) if rows and not insufficient else None)
        for r in sorted(rows, key=lambda r: -r["net_usd"]):
            star = " *(best)*" if best and r["variant"] == best["variant"] else ""
            wr = "" if r["winrate"] is None else f"{r['winrate']:.2f}"
            pf = "" if r["profit_factor"] is None else f"{r['profit_factor']:.2f}"
            L.append(f"| `{r['variant']}`{star} | {r['trades']} | {r['skipped']} | {r['net_usd']:.0f} | "
                     f"{r['net_r']:.2f} | {wr} | {pf} |")
        L.append("")
    return "\n".join(L)


def write_report(result: dict, out_dir: str | None = None) -> str:
    base = Path(out_dir) if out_dir else (_root() / "reports")
    base.mkdir(parents=True, exist_ok=True)
    out = base / "ENTRY_MODE_PARAMETER_SWEEP.md"
    with out.open("w", encoding="utf-8") as fh:
        fh.write(render_markdown(result))
    return str(out)


__all__ = ["sweep_signal", "refresh", "render_markdown", "write_report", "_variant_geometry",
           "_load_forward_sample"]
