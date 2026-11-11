"""Read-only audit builder for the last N days (default 7). Emits the master dataset
(CSV) + aggregate JSON the markdown reports are authored from. NEVER writes to the
trading DB; opens it read-only. Pure analysis — no strategy/scoring/TP/SL changes."""
from __future__ import annotations
import sqlite3, json, csv, sys, collections
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "db" / "crypto_ai_desk.sqlite"
OUT = ROOT / "reports"
DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 7
NOW = datetime.now(timezone.utc)
CUT = (NOW - timedelta(days=DAYS)).isoformat()


def conn():
    c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=20)
    c.row_factory = sqlite3.Row
    return c


def parse(ts):
    if not ts:
        return None
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    except Exception:
        return None


def hrs(a, b):
    da, db = parse(a), parse(b)
    if not da or not db:
        return None
    return round((db - da).total_seconds() / 3600, 2)


def main():
    c = conn()
    # latest outcome per signal
    sigs = c.execute(
        "SELECT * FROM proposed_signals WHERE created_at>=? ORDER BY created_at", (CUT,)
    ).fetchall()
    # index latest outcome + latest paper_entry payload
    outs = {}
    for r in c.execute(
        "SELECT o.* FROM signal_outcomes o JOIN (SELECT signal_id, MAX(checked_at) mx "
        "FROM signal_outcomes GROUP BY signal_id) l ON l.signal_id=o.signal_id AND l.mx=o.checked_at"
    ):
        outs[r["signal_id"]] = r
    alerts = {}
    for r in c.execute(
        "SELECT signal_id, sent_at, telegram_status, payload_json FROM signal_alerts "
        "WHERE alert_type='paper_entry' ORDER BY sent_at"
    ):
        alerts[r["signal_id"]] = r  # last wins

    rows = []
    for s in sigs:
        sid = s["signal_id"]
        o = outs.get(sid)
        a = alerts.get(sid)
        payload = {}
        if a and a["payload_json"]:
            try:
                payload = json.loads(a["payload_json"])
            except Exception:
                payload = {}
        entry_trig_at = o["entry_triggered_at"] if o else None
        exit_at = None
        if o:
            exit_at = (o["stop_hit_at"] or o["tp3_hit_at"] or o["tp2_hit_at"]
                       or o["tp1_hit_at"])
        held = hrs(entry_trig_at, exit_at) if entry_trig_at else None
        carried = False
        if entry_trig_at and (exit_at or NOW):
            d0 = parse(entry_trig_at)
            d1 = parse(exit_at) if exit_at else NOW
            if d0 and d1 and d0.date() != d1.date():
                carried = True
        ttstop = hrs(entry_trig_at, o["stop_hit_at"]) if (o and o["stop_hit_at"]) else None
        tttp = hrs(entry_trig_at, o["tp1_hit_at"]) if (o and o["tp1_hit_at"]) else None
        det_lag = hrs(s["created_at"], entry_trig_at) if entry_trig_at else None
        row = {
            "signal_id": sid, "symbol": s["symbol"], "asset_class": s["asset_class"],
            "mode": s["mode"], "tier": s["tier"], "direction": s["direction"],
            "score": s["score"], "created_at": s["created_at"],
            "entry_planned": s["entry_trigger"] or s["suggested_entry"] or s["entry_low"],
            "entry_triggered_at": entry_trig_at,
            "entry_actual": (o["entry_price_used"] if o else None),
            "stop": s["stop_loss"], "tp1": s["tp1"], "tp2": s["tp2"], "tp3": s["tp3"],
            "status": s["status"],
            "final_outcome": (o["final_outcome"] if o else None),
            "exit_at": exit_at,
            "result_R": (o["final_r"] if o else None),
            "mfe_r": (o["max_favorable_excursion_r"] if o else None),
            "mae_r": (o["max_adverse_excursion_r"] if o else None),
            "time_to_stop_h": ttstop, "time_to_tp_h": tttp, "held_hours": held,
            "overnight_carried": carried,
            "freshness_label": payload.get("entry_freshness", ""),
            "detection_lag_h": det_lag,
            "alert_sent_at": (a["sent_at"] if a else None),
            "telegram_status": (a["telegram_status"] if a else None),
            "shadow_reason": _shadow_reason(s, a, payload),
            "concentration_status": payload.get("concentration_status"),
            "concentration_reason": payload.get("concentration_reason"),
            "size_weight": payload.get("size_weight"),
            "playbook": payload.get("playbook"),
            "news_supported": s["news_supported"],
            "oi_context": s["oi_context"], "funding_context": s["funding_context"],
            "market_regime": s["market_regime"], "narrative": s["narrative"],
            "validity_hours": s["validity_window_hours"],
        }
        rows.append(row)
    c.close()

    # ---- write CSV ----
    cols = list(rows[0].keys()) if rows else []
    with (OUT / "LAST_3_7D_TRADE_AND_SHADOW_AUDIT_DATASET.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    agg = _aggregates(rows)
    (OUT / "_audit_3_7d_agg.json").open("w", encoding="utf-8").write(json.dumps(agg, indent=1, default=str))
    print(json.dumps(agg, indent=1, default=str))


def _shadow_reason(s, a, payload):
    ts = (a["telegram_status"] if a else "") or ""
    cs = payload.get("concentration_status") or ""
    if (s["asset_class"] == "crypto" and s["mode"] == "scalp"):
        return "crypto_scalp_shadow"
    if (s["asset_class"] == "stocks" and s["mode"] == "scalp"):
        return "stocks_scalp_research"
    if "sector_cap" in cs:
        return "sector_cap_shadow"
    if "proxy_duplicate" in cs:
        return "proxy_duplicate_shadow"
    if ts == "late_shadow":
        return "late_shadow"
    if str(s["tier"]).upper() == "C":
        return "c_tier"
    if ts == "shadow_only":
        return "shadow_only"
    return ""


def _bucket(rows, keyfn):
    g = collections.defaultdict(list)
    for r in rows:
        g[keyfn(r)].append(r)
    out = {}
    for k, items in sorted(g.items(), key=lambda kv: -len(kv[1])):
        trig = [r for r in items if r["entry_triggered_at"]]
        closed = [r for r in trig if r["result_R"] is not None]
        wins = [r for r in closed if (r["result_R"] or 0) > 0]
        losses = [r for r in closed if (r["result_R"] or 0) < 0]
        exp = [r for r in closed if r["final_outcome"] == "expired"]
        sumR = round(sum((r["result_R"] or 0) for r in closed), 2)
        gp = sum((r["result_R"] or 0) for r in wins)
        gl = abs(sum((r["result_R"] or 0) for r in losses))
        out[str(k)] = {
            "signals": len(items), "triggered": len(trig), "closed": len(closed),
            "win": len(wins), "loss": len(losses), "expired_0R": len(exp),
            "winrate_excl_exp": round(len(wins) / max(1, len(wins) + len(losses)), 3),
            "sumR": sumR, "avgR": round(sumR / max(1, len(closed)), 3),
            "PF": round(gp / gl, 2) if gl else None,
        }
    return out


def _aggregates(rows):
    by_am = _bucket(rows, lambda r: f"{r['asset_class']}/{r['mode']}")
    by_shadow = _bucket([r for r in rows if r["shadow_reason"]], lambda r: r["shadow_reason"])
    # crypto losers last 3d
    c3 = (NOW - timedelta(days=3)).isoformat()
    crypto_losers = [r for r in rows if r["asset_class"] == "crypto" and r["entry_triggered_at"]
                     and (r["result_R"] or 0) < 0 and r["created_at"] >= c3]
    # overnight carried (intraday) triggered
    carried = [r for r in rows if r["overnight_carried"] and r["mode"] == "intraday" and r["entry_triggered_at"]]
    # expired-after-entry (triggered then expired 0R)
    exp_after = [r for r in rows if r["entry_triggered_at"] and r["final_outcome"] == "expired"]
    # regime x direction (crypto intraday triggered)
    reg = collections.Counter()
    for r in rows:
        if r["asset_class"] == "crypto" and r["mode"] == "intraday" and r["entry_triggered_at"]:
            reg[f"{r['market_regime']}|{r['direction']}|{('WIN' if (r['result_R'] or 0)>0 else 'LOSS' if (r['result_R'] or 0)<0 else 'EXP')}"] += 1
    # stops per UTC day (crypto)
    stops_day = collections.Counter()
    for r in rows:
        if r["asset_class"] == "crypto" and (r["result_R"] or 0) < 0 and r["exit_at"]:
            stops_day[str(parse(r["exit_at"]).date())] += 1
    # sector cap occurrences
    cap = collections.Counter(r["concentration_status"] for r in rows if r["concentration_status"])
    return {
        "window_days": DAYS, "now": NOW.isoformat()[:19], "total_signals": len(rows),
        "by_asset_mode": by_am,
        "by_shadow_reason": by_shadow,
        "crypto_losers_last3d_count": len(crypto_losers),
        "crypto_losers_last3d": [
            {"symbol": r["symbol"], "mode": r["mode"], "dir": r["direction"], "regime": r["market_regime"],
             "R": r["result_R"], "mae_r": r["mae_r"], "mfe_r": r["mfe_r"],
             "ttstop_h": r["time_to_stop_h"], "held_h": r["held_hours"], "carried": r["overnight_carried"],
             "created": r["created_at"][:16], "fresh": r["freshness_label"][:30]}
            for r in sorted(crypto_losers, key=lambda x: x["created_at"])],
        "overnight_carried_intraday_count": len(carried),
        "overnight_carried_intraday": [
            {"symbol": r["symbol"], "asset": r["asset_class"], "dir": r["direction"], "R": r["result_R"],
             "outcome": r["final_outcome"], "held_h": r["held_hours"], "created": r["created_at"][:16],
             "exit": (r["exit_at"] or "")[:16]} for r in carried],
        "expired_after_entry_count": len(exp_after),
        "expired_after_entry_by_mode": dict(collections.Counter(f"{r['asset_class']}/{r['mode']}" for r in exp_after)),
        "crypto_intraday_regime_dir_outcome": dict(reg),
        "crypto_stops_per_utc_day": dict(sorted(stops_day.items())),
        "concentration_status_counts": dict(cap),
    }


if __name__ == "__main__":
    main()
