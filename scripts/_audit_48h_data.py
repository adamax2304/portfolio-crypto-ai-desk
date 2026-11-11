"""Read-only data gathering for 48h trade audit. Emits CSV + JSON for downstream MD reports.

NO writes to SQLite. NO mutations. NO Telegram. NO auto-trade.
"""
from __future__ import annotations

import csv
import json
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from collections import Counter, defaultdict

REPO = Path(__file__).resolve().parent.parent
DB = REPO / "db" / "crypto_ai_desk.sqlite"
OUT_CSV = REPO / "reports" / "TRADE_UNIVERSE_48H_AFTER_RECENT_FIXES.csv"
OUT_JSON = REPO / "reports" / "_audit_48h_data.json"

sys.stdout.reconfigure(encoding="utf-8")

CUTOFF = (datetime.now(timezone.utc) - timedelta(hours=48)).isoformat(timespec="seconds")
NOW_ISO = datetime.now(timezone.utc).isoformat(timespec="seconds")


def tv_link(asset_class: str, symbol: str) -> str:
    if asset_class == "crypto":
        return f"https://www.tradingview.com/chart/?symbol=BINANCE:{symbol.replace('/','')}"
    return f"https://www.tradingview.com/chart/?symbol={symbol}"


def playbook_for(row: dict) -> str:
    """Mirror src.signals.playbooks.label_for routing rules without importing config."""
    asset = (row.get("asset_class") or "crypto").lower()
    mode = (row.get("mode") or "intraday").lower()
    direction = (row.get("direction") or "long").lower()
    news = bool(row.get("news_supported"))
    if asset == "stocks":
        if mode == "intraday":
            return "stocks_intraday_rth_momentum"
        if mode == "swing":
            return "stocks_swing_watchlist_rs_rotation"
        return "stocks_invest_watchlist_30d_thesis"
    if mode == "scalp":
        return "crypto_scalp_momentum_continuation"
    if mode == "intraday":
        if direction == "short":
            return "crypto_failed_bounce_short"
        return "crypto_intraday_catalyst_or_momentum"
    if mode == "swing":
        if direction == "short":
            return "crypto_failed_bounce_short"
        return "crypto_swing_narrative_rs_momentum"
    return "crypto_swing_narrative_rs_momentum"


def main() -> int:
    db = sqlite3.connect(DB, timeout=60)
    db.row_factory = sqlite3.Row

    print(f"# cutoff = {CUTOFF}")
    print(f"# now    = {NOW_ISO}")

    rows = db.execute(
        """
        SELECT ps.signal_id, ps.asset_class, ps.symbol, ps.mode, ps.tier,
               ps.direction, ps.score, ps.created_at, ps.expires_at,
               ps.entry_low, ps.entry_high, ps.entry_trigger,
               ps.stop_loss, ps.invalidation, ps.tp1, ps.tp2, ps.tp3,
               ps.news_supported, ps.no_entry_conditions_json,
               ps.raw_idea_json, ps.source_report_path,
               ps.status,
               so.final_outcome, so.final_r,
               so.entry_triggered, so.entry_triggered_at, so.entry_price_used,
               so.stop_hit, so.stop_hit_at,
               so.tp1_hit, so.tp1_hit_at, so.tp2_hit, so.tp2_hit_at,
               so.max_favorable_excursion_r as mfe_r,
               so.max_adverse_excursion_r as mae_r,
               so.notes as outcome_notes, so.checked_at
        FROM proposed_signals ps
        LEFT JOIN signal_outcomes so
          ON so.signal_id = ps.signal_id
         AND so.id = (SELECT MAX(id) FROM signal_outcomes WHERE signal_id = ps.signal_id)
        WHERE ps.created_at >= ? OR ps.updated_at >= ?
        ORDER BY ps.created_at DESC
        """,
        (CUTOFF, CUTOFF),
    ).fetchall()

    print(f"# signals in 48h window: {len(rows)}")

    # Build enriched rows
    enriched: list[dict] = []
    for r in rows:
        d = dict(r)
        d["playbook"] = playbook_for(d)
        d["tv_link"] = tv_link(d["asset_class"], d["symbol"])
        # Cap reasons pulled from raw_idea_json (the original TradeIdea snapshot).
        try:
            raw = json.loads(d.get("raw_idea_json") or "{}")
            d["cap_reasons"] = raw.get("cap_reasons") or []
        except Exception:
            d["cap_reasons"] = []
        # Annotations
        notes = d.get("outcome_notes") or ""
        d["ann_intrabar_entry_stop"] = "intrabar_entry_stop" in notes
        d["ann_intrabar_entry_tp"] = "intrabar_entry_tp" in notes
        d["ann_pre_entry_invalidation"] = "pre_entry_invalidation=1" in notes
        # Parse gap-slip
        d["ann_gap_slip_stop"] = 0
        d["ann_gap_slip_tp"] = 0
        for piece in notes.split(";"):
            piece = piece.strip()
            if piece.startswith("gap_slip_stop_pct_of_risk="):
                try:
                    d["ann_gap_slip_stop"] = int(piece.split("=")[1])
                except Exception:
                    pass
            elif piece.startswith("gap_slip_tp_pct_of_risk="):
                try:
                    d["ann_gap_slip_tp"] = int(piece.split("=")[1])
                except Exception:
                    pass
        # Revalidator note?
        d["revalidator_note"] = next(
            (p.strip() for p in notes.split(";")
             if "revalidator:" in p), ""
        )
        enriched.append(d)

    # CSV
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    headers = [
        "signal_id", "asset_class", "symbol", "playbook", "mode", "tier", "direction",
        "score", "created_at", "expires_at", "status",
        "entry_low", "entry_high", "entry_trigger", "stop_loss", "invalidation",
        "tp1", "tp2", "tp3",
        "entry_triggered", "entry_triggered_at", "entry_price_used",
        "stop_hit", "stop_hit_at", "tp1_hit", "tp1_hit_at", "tp2_hit", "tp2_hit_at",
        "final_outcome", "final_r", "mfe_r", "mae_r",
        "news_supported",
        "ann_intrabar_entry_stop", "ann_intrabar_entry_tp",
        "ann_pre_entry_invalidation", "ann_gap_slip_stop", "ann_gap_slip_tp",
        "revalidator_note", "outcome_notes",
        "cap_reasons_str", "source_report_path", "tv_link",
    ]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        for d in enriched:
            d_out = {h: d.get(h, "") for h in headers}
            d_out["cap_reasons_str"] = " | ".join(str(c) for c in (d.get("cap_reasons") or []))
            w.writerow(d_out)
    print(f"# wrote CSV: {OUT_CSV.name}")

    # JSON summary for downstream MD
    summary = {
        "cutoff": CUTOFF,
        "now": NOW_ISO,
        "total_signals": len(enriched),
        "by_asset_class": dict(Counter(d["asset_class"] for d in enriched)),
        "by_tier": dict(Counter(d["tier"] for d in enriched)),
        "by_mode": dict(Counter(d["mode"] for d in enriched)),
        "by_playbook": dict(Counter(d["playbook"] for d in enriched)),
        "by_status": dict(Counter(d["status"] for d in enriched)),
        "by_final_outcome": dict(Counter(d.get("final_outcome") or "pending" for d in enriched)),
        "by_revalidator_status": {
            "stale_before_entry": sum(1 for d in enriched if d["status"] == "stale_before_entry"),
            "entry_moved_away": sum(1 for d in enriched if d["status"] == "entry_moved_away"),
            "waiting_for_entry": sum(1 for d in enriched if d["status"] == "waiting_for_entry"),
        },
        "execution_annotations": {
            "intrabar_entry_stop": sum(1 for d in enriched if d["ann_intrabar_entry_stop"]),
            "intrabar_entry_tp": sum(1 for d in enriched if d["ann_intrabar_entry_tp"]),
            "pre_entry_invalidation": sum(1 for d in enriched if d["ann_pre_entry_invalidation"]),
            "gap_slip_stop_pct_gt_10": sum(1 for d in enriched if d["ann_gap_slip_stop"] >= 10),
            "gap_slip_tp_pct_gt_10": sum(1 for d in enriched if d["ann_gap_slip_tp"] >= 10),
        },
    }

    # Per-playbook performance (A/B only, closed/expired/not_triggered)
    perf: dict[str, dict] = defaultdict(lambda: {
        "n": 0, "triggered": 0, "wins": 0, "losses": 0, "expired": 0,
        "waiting": 0, "stale": 0, "moved_away": 0, "not_triggered": 0,
        "ambiguous": 0, "netR": 0.0, "winR": 0.0, "lossR": 0.0,
        "mfe_sum": 0.0, "mfe_n": 0, "mae_sum": 0.0, "mae_n": 0,
        "top_winners": [], "top_losers": [],
    })
    for d in enriched:
        if d["tier"] not in ("A", "B"):
            continue
        pb = d["playbook"]
        s = perf[pb]
        s["n"] += 1
        if d["entry_triggered"] == 1:
            s["triggered"] += 1
        fo = d.get("final_outcome")
        if fo == "win":
            s["wins"] += 1
            s["netR"] += (d.get("final_r") or 0)
            s["winR"] += (d.get("final_r") or 0)
            s["top_winners"].append((d["symbol"], d.get("final_r")))
        elif fo == "loss":
            s["losses"] += 1
            s["netR"] += (d.get("final_r") or 0)
            s["lossR"] += abs(d.get("final_r") or 0)
            s["top_losers"].append((d["symbol"], d.get("final_r")))
        elif fo == "expired":
            s["expired"] += 1
        elif fo == "not_triggered":
            s["not_triggered"] += 1
        if d["status"] == "waiting_for_entry":
            s["waiting"] += 1
        if d["status"] == "stale_before_entry":
            s["stale"] += 1
        if d["status"] == "entry_moved_away":
            s["moved_away"] += 1
        if d["ann_intrabar_entry_stop"] or d["ann_intrabar_entry_tp"]:
            s["ambiguous"] += 1
        if d.get("mfe_r") is not None:
            s["mfe_sum"] += d["mfe_r"]
            s["mfe_n"] += 1
        if d.get("mae_r") is not None:
            s["mae_sum"] += d["mae_r"]
            s["mae_n"] += 1

    for pb, s in perf.items():
        closed = s["wins"] + s["losses"]
        s["WR"] = (s["wins"] / closed * 100) if closed else 0.0
        s["PF"] = (s["winR"] / s["lossR"]) if s["lossR"] else (float("inf") if s["winR"] else 0.0)
        s["avgR"] = (s["netR"] / closed) if closed else 0.0
        s["mfe_avg"] = (s["mfe_sum"] / s["mfe_n"]) if s["mfe_n"] else 0.0
        s["mae_avg"] = (s["mae_sum"] / s["mae_n"]) if s["mae_n"] else 0.0
        # Top 3
        s["top_winners"] = sorted(s["top_winners"], key=lambda x: -(x[1] or 0))[:3]
        s["top_losers"] = sorted(s["top_losers"], key=lambda x: (x[1] or 0))[:3]
        # JSON-friendly
        s["PF"] = "inf" if s["PF"] == float("inf") else round(s["PF"], 2)
        s["WR"] = round(s["WR"], 1)
        s["avgR"] = round(s["avgR"], 2)
        s["mfe_avg"] = round(s["mfe_avg"], 2)
        s["mae_avg"] = round(s["mae_avg"], 2)
        s["netR"] = round(s["netR"], 1)

    summary["playbook_performance"] = dict(perf)

    OUT_JSON.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print(f"# wrote JSON: {OUT_JSON.name}")

    # Read expansion watchlist
    exp_path = REPO / "data" / "processed" / "agent_outputs" / "crypto_expansion_watchlist.json"
    if exp_path.exists():
        exp = json.loads(exp_path.read_text(encoding="utf-8"))
        print(f"# expansion candidates: {len(exp.get('candidates', []))}, "
              f"sources: {exp.get('counts_by_source')}, "
              f"skipped_scalp: {exp.get('skipped_scalp')}, "
              f"in_top: {exp.get('skipped_in_top_setups')}")
    else:
        print("# no expansion watchlist file")

    # Untracked legacy alerts
    untracked = db.execute(
        """
        SELECT COUNT(*) FROM watchlist_alerts wa
        WHERE wa.asset_class='crypto' AND wa.sent_at >= ?
          AND NOT EXISTS (
            SELECT 1 FROM proposed_signals ps
            WHERE ps.symbol = wa.symbol
              AND ABS((julianday(ps.created_at) - julianday(wa.sent_at)) * 24) < 6
          )
        """,
        (CUTOFF,),
    ).fetchone()[0]
    print(f"# untracked legacy crypto alerts (48h): {untracked}")

    # Latest opus review
    opus = sorted(REPO.glob("OPUS_ENRICHED_REVIEW_AUTO_*.md"))
    latest_opus = opus[-1].name if opus else None
    print(f"# latest opus review: {latest_opus}")

    # LLM packets
    for name in ("llm_analysis_packet.md", "llm_stocks_packet.md"):
        p = REPO / "data" / "processed" / name
        if p.exists():
            mtime = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).isoformat(timespec="seconds")
            print(f"# {name}: mtime={mtime}")

    db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
