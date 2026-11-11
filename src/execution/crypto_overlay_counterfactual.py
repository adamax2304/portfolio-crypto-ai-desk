"""Crypto quality overlay — counterfactual (baseline vs overlay) + weak-session profit-protection sim.
READ-MODEL ONLY. Answers "what would the overlay have changed?" over CLOSED crypto paper trades,
WITHOUT ever changing a real paper exit / final_r / signal_outcomes / live.

For each closed crypto trade the overlay decision is reconstructed LOOKAHEAD-SAFE: market context is
sliced to the trade's created_at (BTC/ETH OHLCV close-time ≤ created_at), and cooldowns are rebuilt
from only the trades that closed BEFORE this trade's entry. Baseline = full size (actual net USD);
overlay = size×net USD (HALF→0.5, SHADOW/BLOCK→0). Winners lost to the overlay are counted explicitly
(missed_tp3_runner / missed_profit_lock / would_have_blocked_winner) so a guard that kills runners is
visible and rejectable.

Writes ONLY crypto_quality_counterfactual. Profit is paper USD (active fee profile) + paper_execution_r.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Any

from src.execution import crypto_quality_overlay as cqo
from src.execution.paper_execution_accounting import EVIDENCE_FORWARD, EVIDENCE_BACKFILL

VERSION = "cqo_cf_v1"

_DDL = """
CREATE TABLE IF NOT EXISTS crypto_quality_counterfactual (
  signal_id TEXT PRIMARY KEY, symbol TEXT, mode TEXT, entry_mode TEXT, side TEXT, score REAL,
  created_at TEXT, close_reason TEXT, paper_execution_r REAL, session_bucket TEXT,
  baseline_action TEXT, overlay_action TEXT, baseline_size REAL, overlay_size REAL,
  baseline_pnl_usd REAL, overlay_simulated_pnl_usd REAL, avoided_loss_usd REAL, missed_profit_usd REAL,
  net_overlay_delta_usd REAL, missed_tp3_runner_flag INTEGER, missed_profit_lock_flag INTEGER,
  overlay_would_have_blocked_winner INTEGER, overlay_would_have_reduced_loser INTEGER,
  overlay_would_have_reduced_winner INTEGER, quality_reasons_json TEXT,
  wspp_saved_loss_usd REAL, wspp_missed_runner_usd REAL, wspp_net_delta_usd REAL,
  computed_at TEXT, version TEXT
);
"""

# ALTER TABLE migration for any DB created before evidence_class existed (mirrors
# paper_execution_accounting._NEW_COLUMNS — never touches signal_outcomes/final_r).
_NEW_COLUMNS = (("evidence_class", "TEXT"),)

_SIZE = {cqo.FULL_SIZE: 1.0, cqo.HALF_SIZE: 0.5, cqo.SHADOW_ONLY: 0.0, cqo.BLOCK: 0.0}


def _has(conn, t):
    return bool(conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (t,)).fetchone())


def _ensure_table(conn) -> None:
    conn.execute(_DDL)
    existing = {r[1] for r in conn.execute("PRAGMA table_info(crypto_quality_counterfactual)")}
    for col, typ in _NEW_COLUMNS:
        if col not in existing:
            try:
                conn.execute(f"ALTER TABLE crypto_quality_counterfactual ADD COLUMN {col} {typ}")
            except Exception:
                pass


def _num(v):
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return None


def _parse(ts):
    try:
        t = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        return t.replace(tzinfo=timezone.utc) if t.tzinfo is None else t
    except Exception:
        return None


def _closed_rows(conn):
    """Canonical closed-crypto query (active-fee-profile USD + entry_mode + MFE + session).
    evidence_class (forward_postfreeze/backfill_pretrained, Model F) is joined defensively — older
    DBs/test fixtures may predate the column, in which case every row is left unclassified."""
    usd = cqo._usd_map(conn)
    em = cqo._entry_mode_for(conn)
    mfe = {}
    if _has(conn, "signal_outcomes"):
        for sid, m in conn.execute(
            "SELECT signal_id, MAX(max_favorable_excursion_r) FROM signal_outcomes GROUP BY signal_id"):
            mfe[sid] = _num(m)
    has_evidence = any(r[1] == "evidence_class" for r in conn.execute("PRAGMA table_info(paper_execution_outcomes)"))
    evidence_col = "o.evidence_class" if has_evidence else "NULL"
    rows = conn.execute(
        "SELECT p.signal_id, p.symbol, p.mode, p.direction, p.score, p.news_supported, p.created_at, "
        f"o.close_reason, o.paper_execution_r, {evidence_col} "
        "FROM paper_execution_outcomes o JOIN proposed_signals p ON p.signal_id=o.signal_id "
        "WHERE p.asset_class='crypto' AND o.close_reason NOT IN ('open','no_entry') "
        "ORDER BY o.computed_at ASC").fetchall()
    out = []
    for sid, sym, mode, direction, score, news, created, close, r, evid in rows:
        out.append({"signal_id": sid, "symbol": sym, "mode": mode, "side": direction, "score": _num(score),
                    "news_supported": news, "created_at": created, "close": str(close or ""),
                    "r": _num(r), "usd": usd.get(sid), "mfe_r": mfe.get(sid), "entry_mode": em.get(sid),
                    "evidence_class": evid, "t": _parse(created)})
    return out


def _point_in_time_cooldowns(prior, cand_t, mode, bucket, symbol, cfg):
    """Rebuild active session+symbol cooldowns from ONLY trades closed before cand_t (lookahead-safe)."""
    sc = cfg.get("session_cooldown") or {}
    yc = cfg.get("symbol_cooldown") or {}
    sess_lb = float(sc.get("lookback_hours", 8.0)); sym_lb = float(yc.get("lookback_hours", 36.0))
    sess_recs, sym_recs = [], []
    for p in prior:
        pt = p["t"]
        if pt is None or pt >= cand_t:
            continue
        rec = {"close": p["close"], "r": p["r"], "usd": p["usd"], "t": pt}
        if p["mode"] == mode and cqo.session_bucket(pt, cfg) == bucket and (cand_t - pt).total_seconds() <= sess_lb * 3600:
            sess_recs.append(rec)
        if p["symbol"] == symbol and p["mode"] == mode and (cand_t - pt).total_seconds() <= sym_lb * 3600:
            sym_recs.append(rec)
    cds = {}
    if cfg.get("session_cooldown_enabled", True) and sess_recs:
        row = cqo._session_cooldown_row(mode, bucket, sorted(sess_recs, key=lambda x: x["t"]), sc, cand_t.isoformat())
        if row["cooldown_active"]:
            cds[("session", mode, bucket)] = {"reason": row["cooldown_reason"], "expires": None}
    if cfg.get("symbol_cooldown_enabled", True) and sym_recs:
        row = cqo._symbol_cooldown_row(symbol, mode, sorted(sym_recs, key=lambda x: x["t"]), yc, cand_t.isoformat())
        if row["cooldown_active"]:
            cds[("symbol", symbol, mode)] = {"reason": row["cooldown_reason"], "expires": None}
    return cds


def _wspp(row, cfg):
    """weak_session_profit_protection_v1 — DIAGNOSTIC ONLY (never applied to a real exit). If MFE armed
    (>= arm_after_r) the protected stop (BE / -0.25R) would change the outcome: a loss becomes
    protected_stop_r (saved loss) but a runner/lock win is capped at protected_stop_r (missed runner)."""
    w = cfg.get("weak_session_profit_protection") or {}
    if not w.get("enabled", True):
        return (0.0, 0.0, 0.0)
    mfe = row["mfe_r"]; r = row["r"]; usd = row["usd"]
    if mfe is None or r is None or usd is None:
        return (0.0, 0.0, 0.0)
    arm = float(w.get("arm_after_r", 0.5)); prot = float(w.get("protected_stop_r", 0.0))
    if mfe < arm:
        return (0.0, 0.0, 0.0)                 # never armed → protection changes nothing
    per_r = abs(usd / r) if r not in (0, None) else None
    if per_r is None or per_r == 0:
        return (0.0, 0.0, 0.0)
    protected_usd = prot * per_r
    delta = protected_usd - usd                 # protected minus actual
    saved = round(delta, 2) if delta > 0 else 0.0       # loss reduced
    missed = round(-delta, 2) if delta < 0 else 0.0     # runner capped
    return (saved, missed, round(delta, 2))


def refresh(*, db: str | None = None, now_iso: str | None = None, persist: bool = True) -> dict[str, Any]:
    from src.config import load_config
    cfg = cqo.load_cfg()
    path = db or str(load_config().db_path)
    now = datetime.fromisoformat(now_iso) if now_iso else datetime.now(timezone.utc)
    fs = cqo._fs()
    conn = sqlite3.connect(path)
    try:
        _ensure_table(conn)
        if not (_has(conn, "proposed_signals") and _has(conn, "paper_execution_outcomes")):
            return {"evaluated": 0}
        rows = _closed_rows(conn)
        results = []
        for i, row in enumerate(rows):
            cand_t = row["t"] or now
            bucket = cqo.session_bucket(cand_t, cfg)
            session = {"session_bucket_utc": bucket, "session_quality_state": cqo.session_quality(bucket, cand_t, cfg)}
            mkt = cqo.market_context(cand_t, cfg, fs=fs, as_of=cand_t)      # lookahead-safe
            symc = cqo.symbol_context(fs, row["symbol"], row["mode"], cfg, as_of=cand_t)
            cds = _point_in_time_cooldowns(rows[:i], cand_t, row["mode"], bucket, row["symbol"], cfg)
            cand = {"signal_id": row["signal_id"], "symbol": row["symbol"], "mode": row["mode"],
                    "side": row["side"], "score": row["score"], "entry_mode": row["entry_mode"],
                    "news_supported": row["news_supported"], "timestamp": row["created_at"]}
            d = cqo.evaluate(cand, mkt, symc, session, cds,
                             {"intraday_open": 0, "by_symbol_mode": {}, "alt_long": 0, "alt_short": 0}, cfg)
            base_usd = row["usd"]
            osize = _SIZE.get(d.action, 1.0)
            if base_usd is None:
                res = {**row, "overlay_action": d.action, "reasons": d.reasons, "bucket": bucket,
                       "base_usd": None, "over_usd": None, "delta": None, "avoided": None, "missed": None,
                       "wspp": (0.0, 0.0, 0.0)}
            else:
                over_usd = round(base_usd * osize, 2)
                delta = round(over_usd - base_usd, 2)
                avoided = delta if (base_usd < 0 and delta > 0) else 0.0
                missed = round(-delta, 2) if (base_usd > 0 and delta < 0) else 0.0
                res = {**row, "overlay_action": d.action, "reasons": d.reasons, "bucket": bucket,
                       "base_usd": base_usd, "over_usd": over_usd, "delta": delta,
                       "avoided": avoided, "missed": missed, "wspp": _wspp(row, cfg)}
            results.append(res)
            if persist:
                reduced = d.action in (cqo.HALF_SIZE, cqo.SHADOW_ONLY, cqo.BLOCK)
                gone = d.action in (cqo.SHADOW_ONLY, cqo.BLOCK)
                win = (base_usd is not None and base_usd > 0)
                loss = (base_usd is not None and base_usd < 0)
                conn.execute(
                    "INSERT OR REPLACE INTO crypto_quality_counterfactual VALUES (" + ",".join("?" * 31) + ")",
                    (row["signal_id"], row["symbol"], row["mode"], row["entry_mode"], row["side"], row["score"],
                     row["created_at"], row["close"], row["r"], bucket, cqo.FULL_SIZE, d.action, 1.0, osize,
                     res["base_usd"], res["over_usd"], res["avoided"], res["missed"], res["delta"],
                     int(row["close"] == "tp3_runner" and gone), int(row["close"] == "profit_lock_stop" and reduced),
                     int(win and gone), int(loss and reduced), int(win and reduced),
                     json.dumps(d.reasons), res["wspp"][0], res["wspp"][1], res["wspp"][2],
                     now.isoformat(), VERSION, row["evidence_class"]))
        if persist:
            conn.commit()
        return _summary(results, now)
    finally:
        conn.close()


def _pf(vals):
    g = sum(v for v in vals if v and v > 0); l = -sum(v for v in vals if v and v < 0)
    return (float("inf") if g > 0 else None) if l <= 0 else round(g / l, 3)


def _evidence_bucket(have):
    """forward_postfreeze = the underlying trade entered at/after the Model-F freeze -> usable as
    forward edge evidence. backfill_pretrained/unclassified = hypothesis/context only, NEVER cited
    as proof this overlay (or its wspp diagnostic) is profitable."""
    fwd = [r for r in have if r.get("evidence_class") == EVIDENCE_FORWARD]
    bfd = [r for r in have if r.get("evidence_class") == EVIDENCE_BACKFILL]
    unc = [r for r in have if r.get("evidence_class") not in (EVIDENCE_FORWARD, EVIDENCE_BACKFILL)]
    def bucket_stats(rows):
        rs = [r["r"] for r in rows if r.get("r") is not None]
        return {"n": len(rows), "resolved": len(rs), "net_r_sum": round(sum(rs), 4) if rs else None}
    return {"evidence_forward_postfreeze": bucket_stats(fwd), "evidence_backfill_pretrained": bucket_stats(bfd),
            "evidence_unclassified": bucket_stats(unc)}


def _summary(results, now, window_days: int | None = None) -> dict[str, Any]:
    if window_days is not None:
        cut = now - timedelta(days=window_days)
        results = [r for r in results if (r["t"] or now) >= cut]
    have = [r for r in results if r["base_usd"] is not None]
    forward = [r for r in have if r.get("evidence_class") == EVIDENCE_FORWARD]
    base = [r["base_usd"] for r in have]
    over = [r["over_usd"] for r in have]
    forward_base = [r["base_usd"] for r in forward]
    forward_over = [r["over_usd"] for r in forward]
    base_stops = sum(1 for r in have if r["close"] == "original_stop")
    over_stops = sum(1 for r in have if r["close"] == "original_stop" and _SIZE.get(r["overlay_action"], 1.0) > 0)
    missed_runners = sum(1 for r in have if r["close"] == "tp3_runner" and _SIZE.get(r["overlay_action"], 1.0) == 0)
    total_runners = sum(1 for r in have if r["close"] == "tp3_runner")
    missed_winners = sum(1 for r in have if r["base_usd"] > 0 and _SIZE.get(r["overlay_action"], 1.0) == 0)
    kept_full = sum(1 for r in have if r["overlay_action"] == cqo.FULL_SIZE)
    return {
        "evaluated": len(results), "with_usd": len(have),
        "baseline_pnl_usd": round(sum(base), 2), "overlay_pnl_usd": round(sum(over), 2),
        "net_overlay_delta_usd": round(sum(over) - sum(base), 2),
        "avoided_loss_usd": round(sum(r["avoided"] for r in have), 2),
        "missed_profit_usd": round(sum(r["missed"] for r in have), 2),
        "baseline_pf": _pf(base), "overlay_pf": _pf(over),
        "forward_with_usd": len(forward),
        "forward_baseline_pnl_usd": round(sum(forward_base), 2),
        "forward_overlay_pnl_usd": round(sum(forward_over), 2),
        "forward_net_overlay_delta_usd": round(sum(forward_over) - sum(forward_base), 2),
        "forward_baseline_pf": _pf(forward_base),
        "forward_overlay_pf": _pf(forward_over),
        "baseline_original_stops": base_stops, "overlay_original_stops_kept": over_stops,
        "original_stop_reduction": base_stops - over_stops,
        "missed_tp3_runners": missed_runners, "total_tp3_runners": total_runners,
        "runner_capture_delta": (total_runners - missed_runners) - total_runners,  # negative = runners lost
        "missed_winners": missed_winners, "kept_full_size": kept_full,
        "trade_count_delta": -sum(1 for r in have if _SIZE.get(r["overlay_action"], 1.0) == 0),
        "wspp_saved_usd": round(sum(r["wspp"][0] for r in have), 2),
        "wspp_missed_runner_usd": round(sum(r["wspp"][1] for r in have), 2),
        "generated_at": now.isoformat(),
        **_evidence_bucket(have),
    }


def _summary_with_slices(results: list[dict[str, Any]], now: datetime,
                         window_days: int | None) -> dict[str, Any]:
    summary = _summary(results, now, window_days)
    if window_days is not None:
        cutoff = now - timedelta(days=window_days)
        rows = [row for row in results if (row.get("t") or now) >= cutoff]
    else:
        rows = list(results)
    by_mode_side: dict[str, list[dict[str, Any]]] = {}
    by_session: dict[str, list[dict[str, Any]]] = {}
    reason_stats: dict[str, dict[str, float | int]] = {}
    for row in rows:
        by_mode_side.setdefault(
            f"{row.get('mode') or '?'}:{row.get('side') or '?'}", []
        ).append(row)
        by_session.setdefault(str(row.get("bucket") or "unknown"), []).append(row)
        for reason in row.get("reasons") or []:
            rec = reason_stats.setdefault(str(reason), {"n": 0, "forward_n": 0, "delta_usd": 0.0})
            rec["n"] = int(rec["n"]) + 1
            if row.get("evidence_class") == EVIDENCE_FORWARD:
                rec["forward_n"] = int(rec["forward_n"]) + 1
                rec["delta_usd"] = round(float(rec["delta_usd"]) + float(row.get("delta") or 0.0), 2)
    summary["by_mode_side"] = {
        key: _summary(value, now, None) for key, value in sorted(by_mode_side.items())
    }
    summary["by_session"] = {
        key: _summary(value, now, None) for key, value in sorted(by_session.items())
    }
    summary["reason_effect_forward"] = dict(sorted(
        reason_stats.items(), key=lambda item: (-int(item[1]["forward_n"]), item[0])
    ))
    return summary


def window_summaries(*, db: str | None = None, now_iso: str | None = None) -> dict[str, Any]:
    """Recompute + return 48h / 7d / 14d overlay-delta summaries (no persist beyond the base refresh)."""
    from src.config import load_config
    path = db or str(load_config().db_path)
    now = datetime.fromisoformat(now_iso) if now_iso else datetime.now(timezone.utc)
    refresh(db=path, now_iso=now.isoformat(), persist=True)
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        rows = []
        if _has(conn, "crypto_quality_counterfactual"):
            for sid, mode, side, bucket, reasons, created, close, action, base_usd, over_usd, avoided, missed, delta, wsp_s, wsp_m, r, evid in conn.execute(
                "SELECT signal_id, mode, side, session_bucket, quality_reasons_json, created_at, close_reason, overlay_action, baseline_pnl_usd, "
                "overlay_simulated_pnl_usd, avoided_loss_usd, missed_profit_usd, net_overlay_delta_usd, "
                "wspp_saved_loss_usd, wspp_missed_runner_usd, paper_execution_r, evidence_class "
                "FROM crypto_quality_counterfactual"):
                try:
                    reason_list = json.loads(reasons or "[]")
                except (TypeError, ValueError, json.JSONDecodeError):
                    reason_list = []
                rows.append({"signal_id": sid, "mode": mode, "side": side, "bucket": bucket,
                             "reasons": reason_list if isinstance(reason_list, list) else [],
                             "created_at": created, "close": close, "overlay_action": action,
                             "base_usd": base_usd, "over_usd": over_usd, "avoided": avoided or 0.0,
                             "missed": missed or 0.0, "delta": delta, "wspp": (wsp_s or 0.0, wsp_m or 0.0, 0.0),
                             "r": r, "evidence_class": evid, "t": _parse(created)})
    finally:
        conn.close()
    return {"d2": _summary_with_slices(rows, now, 2),
            "d7": _summary_with_slices(rows, now, 7),
            "d14": _summary_with_slices(rows, now, 14),
            "all": _summary_with_slices(rows, now, None)}


__all__ = ["refresh", "window_summaries", "VERSION"]
