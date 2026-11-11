"""Settings-backtest: re-run the existing parameter-sweep variants over the FULL
signal history on DEEP price paths (Move 1).

Why this is honest (not look-ahead):
  * The signals are REAL rows from ``proposed_signals`` — we do not invent entries.
  * We only vary how each real signal's exit/protection/entry-mode/fill would have
    been handled, and score it on the real subsequent price path.
  * That answers the SETTINGS question (Model-F params, fill mechanics, stop/TP/RR,
    fee sensitivity) — which is a function of the path given an entry — for the whole
    history at once, instead of waiting months for forward accumulation.

What it deliberately does NOT do:
  * It does not claim the desk's live signal SELECTION has edge (that stays forward).
  * It does not model live fills/latency (forward-only).
  * It does not promote anything. Promotion stays forward + post-fee + positive +
    sign-off. This is a ranking/pruning tool.

Data source: the SEPARATE deep-history store (``src.backtest.historical_store``),
backfilled by ``historical_ohlcv_backfill``. The live rolling cache is never read
here, so a settings replay can reach signals far older than the 9-day window.

I/O discipline: ``proposed_signals`` is read-only; the only write is the read-model
table ``settings_backtest_results`` (+ an optional report file). Never touches
``signal_outcomes`` / ``final_r`` / live execution.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from src.backtest import historical_store as hist
from src.execution.entry_mode_parameter_sweep import _agg, _f, sweep_signal
from src.execution.entry_mode_calibration import load_calibration_config
from src.execution.preentry_classifier import classify_preentry_from_candles, closed_candles
from src.signals.tracker import TIMEFRAME_PREFERENCE


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


# ------------------------------------------------------------------ deep candle loader
def _exchange_order(config, exchange_focus: str) -> list[str]:
    order: list[str] = []
    if exchange_focus:
        order.append(exchange_focus.lower())
    anchor = (getattr(config, "anchor_exchange", None) or "binance").lower()
    for ex in (anchor, "binance", "bybit", "mexc"):
        if ex not in order:
            order.append(ex)
    return order


def load_deep_frame(config, symbol: str, mode: str,
                    exchange_focus: str) -> tuple[pd.DataFrame | None, str, str]:
    """Full deep history (both sides of created_at). Mirrors tracker._load_ohlcv_for_signal's
    exchange+timeframe preference but reads the deep store (not the 9-day rolling cache).
    Returns (full_df, exchange, timeframe) or (None, '', '')."""
    tf_pref = TIMEFRAME_PREFERENCE.get(mode or "intraday", TIMEFRAME_PREFERENCE["intraday"])
    for exchange in _exchange_order(config, exchange_focus or ""):
        for tf in tf_pref:
            frame = hist.load(config, exchange, symbol, tf)
            if frame is None or frame.empty:
                continue
            df = frame.copy()
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
            return df.reset_index(drop=True), exchange, tf
    return None, "", ""


def load_deep_candles(config, symbol: str, mode: str, exchange_focus: str,
                      created_at: str) -> tuple[pd.DataFrame | None, str, str]:
    """Deep history sliced to created_at forward (the walk path). Convenience wrapper."""
    df, ex, tf = load_deep_frame(config, symbol, mode, exchange_focus)
    if df is None:
        return None, "", ""
    if created_at:
        df = df[df["timestamp"] >= pd.to_datetime(created_at, utc=True)]
    return (df.reset_index(drop=True) if not df.empty else None), ex, tf


# ------------------------------------------------------------------ signal source (read-only)
def _load_signals(conn, *, asset_class: str, limit: int, since: str | None) -> list[dict]:
    where = ["asset_class = ?", "symbol IS NOT NULL", "suggested_entry IS NOT NULL"]
    args: list = [asset_class]
    if since:
        where.append("created_at >= ?")
        args.append(since)
    sql = f"""
      SELECT signal_id, symbol, direction, mode, asset_class, exchange_focus, created_at,
             entry_low, entry_high, entry_trigger, suggested_entry,
             COALESCE(invalidation, stop_loss) AS stop_used, tp1, tp2, tp3,
             validity_window_hours, expires_at
      FROM proposed_signals
      WHERE {' AND '.join(where)}
      ORDER BY created_at DESC LIMIT ?
    """
    args.append(int(limit))
    cols = [d[0] for d in conn.execute(sql, args).description]
    return [dict(zip(cols, r)) for r in conn.execute(sql, args).fetchall()]


# A trade is walked only over its intended life — expires_at if present, else
# created_at + validity_window_hours, else a mode default. This matches how the
# live desk treats a signal AND keeps the walk bounded (deep history would
# otherwise walk weeks of bars per scalp signal — slow and unfaithful).
_MODE_MAX_HOURS = {"scalp": 24, "intraday": 72, "swing": 336, "invest": 720}


def _horizon_end(signal: dict, created):
    exp = signal.get("expires_at")
    if exp:
        try:
            return pd.to_datetime(exp, utc=True)
        except Exception:
            pass
    hrs = signal.get("validity_window_hours")
    try:
        hrs = float(hrs) if hrs not in (None, "") else None
    except (TypeError, ValueError):
        hrs = None
    if hrs is None:
        hrs = _MODE_MAX_HOURS.get(str(signal.get("mode") or "intraday").lower(), 72)
    return pd.to_datetime(created, utc=True) + pd.Timedelta(hours=hrs)


_DDL = """
CREATE TABLE IF NOT EXISTS settings_backtest_results (
  generated_at TEXT, param TEXT, variant TEXT, trades INTEGER, skipped INTEGER,
  net_usd REAL, net_r REAL, winrate REAL, profit_factor REAL,
  signals_total INTEGER, signals_covered INTEGER, history_days INTEGER,
  PRIMARY KEY (param, variant)
);
"""

# Deep history gives far more sample than the 9-day forward window, so require a
# higher bar before calling any variant 'best' — same spirit as the sweep's gate.
MIN_COVERED_FOR_CONCLUSION = 100


def refresh(*, db: str | None = None, asset_class: str = "crypto", days: int = 60,
            limit: int = 5000, since: str | None = None, persist: bool = True,
            write_report_file: bool | None = None, report_dir: str | None = None,
            now_iso: str | None = None) -> dict[str, Any]:
    """Replay all settings variants over the full signal history on deep candles.

    The GLOBAL report is written only when write_report_file is True — DEFAULTS TO
    (db is None) so a temp/test db never overwrites the production report.
    """
    from src.config import load_config
    cfg_proj = load_config()
    cfg = load_calibration_config()
    path = db or str(cfg_proj.db_path)
    now_dt = datetime.now(timezone.utc) if now_iso is None else datetime.fromisoformat(now_iso)
    nine_day_cutoff = (now_dt - timedelta(days=9)).isoformat()

    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)   # source strictly read-only
    try:
        signals = _load_signals(conn, asset_class=asset_class, limit=limit, since=since)
    finally:
        conn.close()

    fee_profile = ("stock_etf_default" if str(asset_class).lower().startswith("stock")
                   else "bybit_non_vip_usdt_perp")
    per_sig: list[dict] = []
    covered = 0
    covered_recent = 0        # of those the 9-day cache would ALSO have covered
    per_mode: dict[str, int] = {}
    per_entry_mode: dict[str, int] = {}
    frame_cache: dict[tuple, tuple] = {}      # (symbol, mode, focus) -> (full_df, ex, tf); 997 sigs / 139 syms
    for s in signals:
        ckey = (s.get("symbol"), s.get("mode"), s.get("exchange_focus"))
        if ckey not in frame_cache:
            frame_cache[ckey] = load_deep_frame(cfg_proj, s.get("symbol"), s.get("mode"),
                                                s.get("exchange_focus"))
        full, _ex, tf = frame_cache[ckey]
        if full is None or full.empty:
            continue
        created = s.get("created_at")
        if created:
            start = pd.to_datetime(created, utc=True)
            end = _horizon_end(s, created)             # bound the walk to the signal's life
            post = full[(full["timestamp"] >= start) & (full["timestamp"] <= end)]
        else:
            post = full
        if post.empty:
            continue                                   # no forward path to walk
        # Lookahead-safe entry_mode: classify from candles CLOSED at/before creation only.
        pre_df = closed_candles(full, tf, created)
        pre = ([] if pre_df is None or getattr(pre_df, "empty", True) else
               [{"open": _f(r.get("open")), "high": _f(r.get("high")),
                 "low": _f(r.get("low")), "close": _f(r.get("close"))}
                for _, r in pre_df.iterrows()])
        cls = classify_preentry_from_candles(
            direction=s.get("direction"), entry_low=_f(s.get("entry_low")),
            entry_high=_f(s.get("entry_high")), entry=_f(s.get("suggested_entry")),
            stop=_f(s.get("stop_used")), candles=pre)
        entry_mode = cls.get("entry_mode")
        covered += 1
        per_mode[s.get("mode") or "?"] = per_mode.get(s.get("mode") or "?", 0) + 1
        per_entry_mode[entry_mode or "?"] = per_entry_mode.get(entry_mode or "?", 0) + 1
        if str(created or "") >= nine_day_cutoff:
            covered_recent += 1
        geom = {"direction": s.get("direction"), "entry_low": _f(s.get("entry_low")),
                "entry_high": _f(s.get("entry_high")), "entry_trigger": _f(s.get("entry_trigger")),
                "entry": _f(s.get("suggested_entry")), "stop": _f(s.get("stop_used")),
                "tp1": _f(s.get("tp1")), "tp2": _f(s.get("tp2")), "tp3": _f(s.get("tp3")),
                "entry_mode": entry_mode, "symbol": s.get("symbol")}
        per_sig.append(sweep_signal(geom, post.reset_index(drop=True), cfg, fee_profile=fee_profile))

    agg = _agg(per_sig)
    coverage_status = "OK" if covered >= MIN_COVERED_FOR_CONCLUSION else "INSUFFICIENT_COVERAGE"
    generated_at = now_dt.isoformat()
    result = {
        "db_path": str(path), "generated_at": generated_at, "persisted": bool(persist),
        "asset_class": asset_class, "history_days": days,
        "signals_total": len(signals), "signals_covered": covered,
        "signals_covered_by_9d_cache": covered_recent,
        "deep_history_unlock": max(0, covered - covered_recent),
        "coverage_status": coverage_status,
        "min_covered_for_conclusion": MIN_COVERED_FOR_CONCLUSION,
        "per_mode_covered": per_mode, "per_entry_mode_covered": per_entry_mode, **agg,
    }

    persisted_rows = None
    if persist:
        wconn = sqlite3.connect(path)
        try:
            wconn.execute("DROP TABLE IF EXISTS settings_backtest_results")
            wconn.execute(_DDL)
            for v in agg["variants"]:
                wconn.execute(
                    "INSERT OR REPLACE INTO settings_backtest_results VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (generated_at, v["param"], v["variant"], v["trades"], v["skipped"],
                     v["net_usd"], v["net_r"], v["winrate"], v["profit_factor"],
                     len(signals), covered, days))
            wconn.commit()
            persisted_rows = wconn.execute(
                "SELECT count(*), max(generated_at) FROM settings_backtest_results").fetchone()
        finally:
            wconn.close()
    result["matches_persisted_table"] = bool(
        persist and persisted_rows and persisted_rows[0] == len(agg["variants"])
        and persisted_rows[1] == generated_at)

    do_report = (db is None) if write_report_file is None else bool(write_report_file)
    if do_report:
        write_report(result, out_dir=report_dir)
    return result


def render_markdown(result: dict) -> str:
    mark = "PERSISTED (read-model table written)" if result.get("persisted") else "DRY-RUN (nothing written)"
    cov = result.get("coverage_status", "OK")
    insufficient = cov == "INSUFFICIENT_COVERAGE"
    total = result.get("signals_total", 0)
    covered = result.get("signals_covered", 0)
    L = ["# Settings Backtest — full signal history on DEEP OHLCV (read-model, NEVER auto-applied)", "",
         f"- db_path: `{result.get('db_path')}`",
         f"- generated_at: `{result['generated_at']}`  ·  **{mark}**",
         f"- matches persisted table: **{str(bool(result.get('matches_persisted_table'))).lower()}**",
         f"- asset_class: **{result.get('asset_class')}** · history_days: {result.get('history_days')}",
         f"- signals covered: **{covered}** / {total} total  "
         f"(deep history unlocked **{result.get('deep_history_unlock')}** signals the 9-day cache "
         f"could not replay; only {result.get('signals_covered_by_9d_cache')} were within 9 days)",
         f"- coverage_status: **{cov}** (min {result.get('min_covered_for_conclusion')} to draw a conclusion)",
         "",
         "> **SETTINGS question only.** Real signals, varied handling, scored on real deep paths. "
         "This ranks/prunes settings — it does NOT prove live signal edge, model live fills/latency, "
         "or promote anything. Promotion stays forward + post-fee + positive + sign-off.", ""]
    pm = result.get("per_mode_covered") or {}
    if pm:
        L.append("Covered by mode: " + ", ".join(f"{k}={v}" for k, v in sorted(pm.items())))
        L.append("")
    pem = result.get("per_entry_mode_covered") or {}
    if pem:
        L.append("Covered by entry_mode (lookahead-safe pre-entry classify): "
                 + ", ".join(f"{k}={v}" for k, v in sorted(pem.items())))
        L.append("")
    if insufficient:
        L.append(f"> **INSUFFICIENT COVERAGE — ranking diagnostic only (covered {covered} < "
                 f"{result.get('min_covered_for_conclusion')}). No variant marked 'best'.**")
        L.append("")
    by_param: dict[str, list] = {}
    for v in result.get("variants", []):
        by_param.setdefault(v["param"], []).append(v)
    for param, rows in sorted(by_param.items()):
        L.append(f"## {param}")
        L.append("")
        L.append("| variant | trades | skipped | net USD | net R | winrate | PF |")
        L.append("|---|--:|--:|--:|--:|--:|--:|")
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
    out = base / "SETTINGS_BACKTEST.md"
    with out.open("w", encoding="utf-8") as fh:
        fh.write(render_markdown(result))
    return str(out)


__all__ = ["refresh", "render_markdown", "write_report", "load_deep_candles"]
