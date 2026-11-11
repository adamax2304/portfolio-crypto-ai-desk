"""Move 4 — backtest↔forward reconciliation (READ-MODEL / evaluation-only).

The whole plan rests on trusting the backtest to PRUNE/RANK faster than forward. This module earns
that trust per mode by measuring how well the backtest actually predicts forward on the SAME trades:

  * FORWARD  = the authoritative live rolling-cache lane (paper_shadow_execution_outcomes).
  * BACKTEST = the Move-1/3 deep-history lane (paper_shadow_wide_outcomes), same signals & engine.

For each signal filled in BOTH lanes (branch new_logic_shadow), compare net_r. Per (asset_class,
mode) report: n, mean/median |Δ net_r|, sign-agreement rate, correlation, and a trust verdict:

  * TRACKS   — small divergence AND high sign-agreement → the backtest predicts forward well, so this
               mode may EARN a shorter forward window (backtest ranking can be trusted more).
  * PARTIAL  — mixed: usable for coarse ranking, not for a shortened gate.
  * DIVERGES — backtest and forward disagree (like the B lane once did) → KEEP THE FULL forward gate;
               do not trust the backtest to shorten testing for this mode.
  * NEED_MORE_DATA — too few paired trades to judge.

This does NOT promote anything and does NOT change any gate — it OUTPUTS which modes have earned the
right to a shorter forward window, for the operator to apply. Reads two read-model lanes; writes ONLY
backtest_forward_reconciliation (+ report). Never touches proposed_signals / final_r / live.
"""

from __future__ import annotations

import math
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# trust thresholds (config-light; conservative by design)
MAX_MEAN_ABS_DIV_R = 0.35      # mean |Δ net_r| at/under this = close tracking
MIN_SIGN_AGREEMENT = 0.70      # ≥70% of trades agree on win/loss sign
MIN_N_FOR_VERDICT = 20         # below this → NEED_MORE_DATA


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_pairs(conn) -> dict[tuple, list[dict]]:
    """Per (asset_class, mode): [{signal_id, fwd_r, bt_r}] for new_logic_shadow signals FILLED in
    BOTH the forward (primary) and backtest (wide) lanes."""
    def _has(t):
        return bool(conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (t,)).fetchone())
    if not (_has("paper_shadow_execution_outcomes") and _has("paper_shadow_wide_outcomes")):
        return {}
    fwd = {r[0]: r[1] for r in conn.execute(
        "SELECT e.signal_id, e.net_r FROM paper_shadow_execution_outcomes e "
        "WHERE e.branch='new_logic_shadow' AND e.entry_fill_status='filled' "
        "AND e.window='forward_since_activation' AND e.net_r IS NOT NULL")}
    rows = conn.execute(
        "SELECT signal_id, net_r, asset_class, mode FROM paper_shadow_wide_outcomes "
        "WHERE branch='new_logic_shadow' AND entry_fill_status='filled' AND net_r IS NOT NULL")
    groups: dict[tuple, list[dict]] = {}
    for sid, bt_r, ac, mode in rows:
        if sid in fwd:
            groups.setdefault((str(ac or "?"), str(mode or "?")), []).append(
                {"signal_id": sid, "fwd_r": fwd[sid], "bt_r": bt_r})
    return groups


def _corr(xs, ys) -> float | None:
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return None
    return round(sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy), 3)


def _verdict(n, mean_abs_div, sign_agree) -> str:
    if n < MIN_N_FOR_VERDICT:
        return "NEED_MORE_DATA"
    if mean_abs_div <= MAX_MEAN_ABS_DIV_R and sign_agree >= MIN_SIGN_AGREEMENT:
        return "TRACKS"
    if mean_abs_div <= MAX_MEAN_ABS_DIV_R * 2 and sign_agree >= 0.55:
        return "PARTIAL"
    return "DIVERGES"


_DDL = """
CREATE TABLE IF NOT EXISTS backtest_forward_reconciliation (
  generated_at TEXT, asset_class TEXT, mode TEXT, n INTEGER, mean_abs_div_r REAL, median_abs_div_r REAL,
  sign_agreement REAL, correlation REAL, fwd_sum_r REAL, bt_sum_r REAL, verdict TEXT,
  PRIMARY KEY (asset_class, mode)
);
"""


def refresh(*, db: str | None = None, persist: bool = True,
            write_report_file: bool | None = None, report_dir: str | None = None,
            now_iso: str | None = None) -> dict[str, Any]:
    from src.config import load_config
    cfg = load_config()
    path = db or str(cfg.db_path)
    generated_at = now_iso or datetime.now(timezone.utc).isoformat()

    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        groups = _load_pairs(conn)
    finally:
        conn.close()

    out_rows: list[dict] = []
    for (ac, mode), items in sorted(groups.items()):
        n = len(items)
        divs = [abs(it["fwd_r"] - it["bt_r"]) for it in items]
        mean_abs = sum(divs) / n if n else 0.0
        sdivs = sorted(divs)
        median_abs = (sdivs[n // 2] if n % 2 else (sdivs[n // 2 - 1] + sdivs[n // 2]) / 2) if n else 0.0
        sign_agree = (sum(1 for it in items
                          if (it["fwd_r"] > 0) == (it["bt_r"] > 0)) / n) if n else 0.0
        corr = _corr([it["fwd_r"] for it in items], [it["bt_r"] for it in items])
        out_rows.append({
            "asset_class": ac, "mode": mode, "n": n,
            "mean_abs_div_r": round(mean_abs, 4), "median_abs_div_r": round(median_abs, 4),
            "sign_agreement": round(sign_agree, 4), "correlation": corr,
            "fwd_sum_r": round(sum(it["fwd_r"] for it in items), 3),
            "bt_sum_r": round(sum(it["bt_r"] for it in items), 3),
            "verdict": _verdict(n, mean_abs, sign_agree),
        })

    result = {"db_path": str(path), "generated_at": generated_at, "persisted": bool(persist),
              "thresholds": {"max_mean_abs_div_r": MAX_MEAN_ABS_DIV_R,
                             "min_sign_agreement": MIN_SIGN_AGREEMENT, "min_n": MIN_N_FOR_VERDICT},
              "modes_evaluated": len(out_rows), "modes": out_rows}

    persisted_rows = None
    if persist:
        wconn = sqlite3.connect(path)
        try:
            wconn.execute("DROP TABLE IF EXISTS backtest_forward_reconciliation")
            wconn.execute(_DDL)
            for r in out_rows:
                wconn.execute(
                    "INSERT OR REPLACE INTO backtest_forward_reconciliation VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (generated_at, r["asset_class"], r["mode"], r["n"], r["mean_abs_div_r"],
                     r["median_abs_div_r"], r["sign_agreement"], r["correlation"],
                     r["fwd_sum_r"], r["bt_sum_r"], r["verdict"]))
            wconn.commit()
            persisted_rows = wconn.execute(
                "SELECT count(*), max(generated_at) FROM backtest_forward_reconciliation").fetchone()
        finally:
            wconn.close()
    result["matches_persisted_table"] = bool(
        persist and persisted_rows and persisted_rows[0] == len(out_rows)
        and persisted_rows[1] == generated_at)

    do_report = (db is None) if write_report_file is None else bool(write_report_file)
    if do_report:
        write_report(result, out_dir=report_dir)
    return result


def render_markdown(result: dict) -> str:
    mark = "PERSISTED (read-model table written)" if result.get("persisted") else "DRY-RUN"
    t = result.get("thresholds", {})
    L = ["# Backtest ↔ Forward Reconciliation (read-model, evaluation-only)", "",
         f"- db_path: `{result.get('db_path')}`",
         f"- generated_at: `{result['generated_at']}`  ·  **{mark}**",
         f"- matches persisted table: **{str(bool(result.get('matches_persisted_table'))).lower()}**",
         f"- FORWARD = live rolling-cache lane · BACKTEST = deep-history lane · new_logic_shadow "
         "filled in BOTH",
         f"- TRACKS if mean |Δnet_r| ≤ {t.get('max_mean_abs_div_r')} AND sign-agreement ≥ "
         f"{t.get('min_sign_agreement')} (min n={t.get('min_n')})", "",
         "> A mode that **TRACKS** may EARN a shorter forward window (its backtest predicts forward). "
         "**DIVERGES** → keep the full forward gate; the backtest must not shorten testing there. "
         "This module only reports trust — it changes no gate and promotes nothing.", "",
         "| asset | mode | n | mean|Δ|R | median|Δ|R | sign-agree | corr | fwd ΣR | bt ΣR | verdict |",
         "|---|---|--:|--:|--:|--:|--:|--:|--:|:--|"]
    order = {"TRACKS": 0, "PARTIAL": 1, "DIVERGES": 2, "NEED_MORE_DATA": 3}
    for r in sorted(result.get("modes", []), key=lambda r: (order.get(r["verdict"], 9), r["asset_class"], r["mode"])):
        corr = "" if r["correlation"] is None else f"{r['correlation']:+.2f}"
        L.append(f"| {r['asset_class']} | {r['mode']} | {r['n']} | {r['mean_abs_div_r']:.2f} | "
                 f"{r['median_abs_div_r']:.2f} | {r['sign_agreement']:.2f} | {corr} | "
                 f"{r['fwd_sum_r']:+.1f} | {r['bt_sum_r']:+.1f} | **{r['verdict']}** |")
    return "\n".join(L)


def write_report(result: dict, out_dir: str | None = None) -> str:
    base = Path(out_dir) if out_dir else (_root() / "reports")
    base.mkdir(parents=True, exist_ok=True)
    out = base / "BACKTEST_FORWARD_RECONCILIATION.md"
    with out.open("w", encoding="utf-8") as fh:
        fh.write(render_markdown(result))
    return str(out)


__all__ = ["refresh", "render_markdown", "write_report", "_verdict"]
