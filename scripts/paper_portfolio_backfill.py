"""PART 10 — Historical paper-portfolio backfill (derived, read-only).

Reconstructs a $5000 paper equity curve over the deduped ACTIONABLE paper book,
chronologically, with 0.5%-of-equity risk, position sizing, dynamic leverage, and
fees/slippage — across several fee profiles. Writes equity-curve + ledger CSVs and
persists the default-profile ledger into `paper_portfolio_ledger`. NEVER mutates
`signal_outcomes`.
"""
from __future__ import annotations
import csv, json, os, sqlite3
from datetime import datetime, timezone

from src.execution.paper_execution_accounting import (
    backfill_all, build_record_from_signal, ensure_table as ensure_execution_table,
)
from src.execution.paper_actionability import build_maps, resolve_paper_actionability
from src.execution.paper_portfolio import load_cfg, simulate_portfolio, ensure_tables, replace_ledger
from src.execution.position_sizing import size_position  # noqa: F401 (kept for parity)

DB = "db/crypto_ai_desk.sqlite"
STOCKS_SWING_EVENT_RS_PROFILES = {
    "stocks_swing_event_rs_pullback_quality_paper_v1",
    "stocks_swing_event_rs_pullback_flow_paper_v1",
}


def _connect():
    # The scheduler and short-lived market-data monitors share this SQLite DB.
    # Wait for their bounded write transactions instead of dropping a complete
    # ledger rebuild after the expensive simulation has already finished.
    con = sqlite3.connect(DB, timeout=120.0)
    con.execute("PRAGMA busy_timeout=120000")
    return con


def _f(v):
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return None


def _raw_payload(signal):
    if not isinstance(signal, dict):
        return {}
    raw = signal.get("raw_idea_json")
    if isinstance(raw, dict):
        return dict(raw)
    try:
        parsed = json.loads(raw or "{}")
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def _stock_swing_event_rs_profile(signal) -> str:
    if not isinstance(signal, dict):
        return ""
    direct = str(signal.get("paper_entry_profile") or "").strip()
    if direct:
        return direct
    return str(_raw_payload(signal).get("paper_entry_profile") or "").strip()


def actionable(asset, mode, tier, signal=None):
    if (tier or "").upper() not in ("A", "B"):
        return False
    if asset == "crypto" and mode == "scalp":
        return False
    if asset == "stocks" and mode == "swing":
        return _stock_swing_event_rs_profile(signal) in STOCKS_SWING_EVENT_RS_PROFILES
    if asset == "stocks" and mode == "invest":
        return False
    return True


def authoritative_execution_provenance(row):
    """Legacy rows stay visible; newly classified rows require a verified price."""
    basis = row.get("entry_time_basis")
    return basis in (None, "") or int(row.get("current_price_revalidated") or 0) == 1


def _load_trades_legacy():
    con = _connect(); con.row_factory = sqlite3.Row
    maps = build_maps(con)                    # alert payload / counterfactual / point-in-time decisions
    stats = {"full": 0, "half": 0, "shadow_excluded": 0, "by_source": {}}
    rows = con.execute(
        """
        WITH latest AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY signal_id ORDER BY checked_at DESC, id DESC) rn FROM signal_outcomes)
        SELECT o.*, p.symbol,p.direction,p.mode,p.tier,p.asset_class,p.setup_type,p.created_at,
               p.suggested_entry,p.entry_trigger,p.entry_low,p.stop_loss,p.invalidation,p.tp1,p.tp2,p.tp3,
               p.raw_idea_json
        FROM latest o JOIN proposed_signals p ON p.signal_id=o.signal_id
        WHERE o.rn=1 AND o.entry_triggered=1
        """
    ).fetchall()
    prio = {"win": 5, "loss": 5, "ambiguous": 4, "expired": 3, "not_triggered": 1, None: 0}
    best = {}
    for r in rows:
        d = dict(r)
        entry = _f(d.get("entry_trigger")) or _f(d.get("suggested_entry")) or _f(d.get("entry_low"))
        stop = _f(d.get("invalidation")) or _f(d.get("stop_loss"))
        eat = d.get("entry_triggered_at") or d.get("created_at") or ""
        key = "|".join(str(x) for x in (d["symbol"], (d.get("direction") or "").lower(),
              (d.get("mode") or "").lower(), (d.get("tier") or "").upper(),
              round(entry or 0, 8), str(eat)[:10]))
        if not actionable(d.get("asset_class"), (d.get("mode") or "").lower(), d.get("tier"), d):
            continue
        if key in best and prio.get(d.get("final_outcome"), 0) <= prio.get(best[key]["final_outcome"], 0):
            continue
        sid, _k, rec = build_record_from_signal(d, d)
        d["_entry"], d["_stop"], d["_eat"], d["_key"], d["_rec"] = entry, stop, eat, key, rec
        best[key] = d
    trades = []
    for d in best.values():
        rec = d["_rec"]
        # Authoritative paper action/size for this signal. SHADOW_ONLY/BLOCK (size_weight<=0) are
        # EXCLUDED from the actionable paper book — they must not inflate/deflate paper PnL.
        pa = resolve_paper_actionability(con, d["signal_id"], d.get("asset_class"),
                                         (d.get("mode") or "").lower(), d.get("tier"),
                                         maps=maps, signal=d)
        stats["by_source"][pa["source"]] = stats["by_source"].get(pa["source"], 0) + 1
        if float(pa.get("size_weight") or 0.0) <= 0.0:
            stats["shadow_excluded"] += 1
            continue
        if float(pa["size_weight"]) < 1.0:
            stats["half"] += 1
        else:
            stats["full"] += 1
        trades.append({
            "signal_id": d["signal_id"], "economic_trade_key": d["_key"], "symbol": d["symbol"],
            "asset_class": d["asset_class"], "mode": (d.get("mode") or "").lower(),  # #10: funding intervals
            "direction": (d.get("direction") or "long").lower(),
            "entry": d["_entry"], "stop": d["_stop"], "tp1": _f(d.get("tp1")), "tp2": _f(d.get("tp2")),
            "tp3": _f(d.get("tp3")), "paper_execution_r": rec.get("paper_execution_r"),
            "close_reason": rec.get("close_reason"), "stop_current_r": rec.get("stop_current_r"),
            "entry_at": d["_eat"], "mfe_r": _f(d.get("max_favorable_excursion_r")),
            "exit_at": (d.get("stop_hit_at") if d.get("stop_hit") else
                        d.get("tp3_hit_at") if d.get("tp3_hit") else d.get("checked_at")),
            "mae_r": _f(d.get("max_adverse_excursion_r")),
            # PART 4: tracked TP hits → maker-TP / taker-stop exit slices
            "tp1_hit": d.get("tp1_hit"), "tp2_hit": d.get("tp2_hit"), "tp3_hit": d.get("tp3_hit"),
            "playbook": d.get("setup_type") or "", "regime": d.get("market_regime") or "",
            # overlay-authoritative paper sizing (2026-07-08) — consumed by simulate_portfolio + ledger.
            "size_weight": float(pa["size_weight"]), "paper_action": pa["paper_action"],
            "size_reason": pa["reason"], "actionability_source": pa["source"],
            "overlay_version": pa.get("overlay_version"),
        })
    trades.sort(key=lambda t: t["entry_at"] or "")
    con.close()
    return trades, stats


def load_trades():
    """Load only immutable, terminal paper-execution records.

    The legacy loader above is kept for research compatibility; the production
    paper ledger uses this lifecycle-safe source and frozen signal geometry.
    """
    con = _connect(); con.row_factory = sqlite3.Row
    ensure_execution_table(con)
    maps = build_maps(con)
    stats = {"full": 0, "half": 0, "shadow_excluded": 0,
             "latency_unverified_excluded": 0, "invalid_execution_excluded": 0,
             "unverified_stock_intraday_excluded": 0,
             "mexc_stock_futures_closed": 0, "by_source": {}}
    rows = con.execute(
        """
        SELECT pe.*,
               p.symbol AS p_symbol, p.direction AS p_direction, p.mode AS p_mode,
               p.tier AS p_tier, p.asset_class AS p_asset_class,
               p.setup_type AS p_setup_type, p.created_at AS p_created_at,
               p.suggested_entry AS p_suggested_entry, p.entry_trigger AS p_entry_trigger,
               p.entry_low AS p_entry_low, p.stop_loss AS p_stop_loss,
               p.invalidation AS p_invalidation, p.tp1 AS p_tp1, p.tp2 AS p_tp2, p.tp3 AS p_tp3,
               p.raw_idea_json AS p_raw_idea_json
        FROM paper_execution_outcomes pe
        JOIN proposed_signals p ON p.signal_id=pe.signal_id
        WHERE pe.paper_execution_r IS NOT NULL
          AND pe.lifecycle_state='CLOSED'
        ORDER BY pe.entry_at ASC, pe.signal_id ASC
        """
    ).fetchall()
    best = {}
    for row in rows:
        d = dict(row)
        is_stock_intraday = (
            str(d.get("p_asset_class") or "").lower().startswith("stock")
            and str(d.get("p_mode") or "").lower() == "intraday"
        )
        validity = str(d.get("execution_validity") or "")
        if is_stock_intraday and validity != "valid":
            # Pre-fix rows without an explicit session verdict cannot prove
            # same-day execution. Retain them in the audit table, never in the
            # authoritative Paper balance.
            if not validity:
                stats["unverified_stock_intraday_excluded"] += 1
            else:
                stats["invalid_execution_excluded"] += 1
            continue
        if validity and validity != "valid":
            stats["invalid_execution_excluded"] += 1
            continue
        # Rows created after latency provenance shipped carry an explicit
        # basis. A candle-range-only reconstruction remains valid research,
        # but it is not an authoritative Paper execution and must not move the
        # displayed balance. Legacy NULL rows are retained for historical
        # continuity until they are separately reclassified.
        if not authoritative_execution_provenance(d):
            stats["latency_unverified_excluded"] += 1
            continue
        try:
            snapshot = json.loads(d.get("signal_snapshot_json") or "{}")
        except Exception:
            snapshot = {}
        signal = {
            "signal_id": d["signal_id"], "symbol": d.get("p_symbol"),
            "direction": d.get("p_direction"), "mode": d.get("p_mode"),
            "tier": d.get("p_tier"), "asset_class": d.get("p_asset_class"),
            "setup_type": d.get("p_setup_type"), "created_at": d.get("p_created_at"),
            "suggested_entry": d.get("p_suggested_entry"), "entry_trigger": d.get("p_entry_trigger"),
            "entry_low": d.get("p_entry_low"), "stop_loss": d.get("p_stop_loss"),
            "invalidation": d.get("p_invalidation"), "tp1": d.get("p_tp1"),
            "tp2": d.get("p_tp2"), "tp3": d.get("p_tp3"),
            "raw_idea_json": d.get("p_raw_idea_json"),
        }
        signal.update({k: v for k, v in snapshot.items() if v is not None})
        entry = (_f(d.get("entry_price_used")) or _f(signal.get("entry_trigger"))
                 or _f(signal.get("suggested_entry")) or _f(signal.get("entry_low")))
        stop = _f(signal.get("invalidation")) or _f(signal.get("stop_loss"))
        entry_at = d.get("entry_at") or signal.get("created_at") or ""
        key = d.get("economic_trade_key") or d["signal_id"]
        if not actionable(signal.get("asset_class"), (signal.get("mode") or "").lower(), signal.get("tier"), signal):
            continue
        if key in best:
            continue
        best[key] = (d, signal, entry, stop, entry_at)

    trades = []
    for key, (d, signal, entry, stop, entry_at) in best.items():
        pa = resolve_paper_actionability(
            con, d["signal_id"], signal.get("asset_class"),
            (signal.get("mode") or "").lower(), signal.get("tier"), maps=maps, signal=signal)
        stats["by_source"][pa["source"]] = stats["by_source"].get(pa["source"], 0) + 1
        if float(pa.get("size_weight") or 0.0) <= 0.0:
            stats["shadow_excluded"] += 1
            continue
        stats["half" if float(pa["size_weight"]) < 1.0 else "full"] += 1
        highest = int(d.get("highest_tp_touched") or 0)
        trades.append({
            "signal_id": d["signal_id"], "economic_trade_key": key, "symbol": signal["symbol"],
            "asset_class": signal["asset_class"], "mode": (signal.get("mode") or "").lower(),
            "direction": (signal.get("direction") or "long").lower(),
            "entry": entry, "stop": stop, "tp1": _f(signal.get("tp1")),
            "tp2": _f(signal.get("tp2")), "tp3": _f(signal.get("tp3")),
            "paper_execution_r": d.get("paper_execution_r"), "close_reason": d.get("close_reason"),
            "stop_current_r": d.get("stop_current_r"), "entry_at": entry_at,
            "exit_at": d.get("exit_at"), "exit_at_source": d.get("exit_at_source"),
            "decision_at": d.get("decision_at"),
            "first_executable_price": d.get("first_executable_price"),
            "entry_drift_bps": d.get("entry_drift_bps"),
            "tp1_hit": highest >= 1, "tp2_hit": highest >= 2, "tp3_hit": highest >= 3,
            "playbook": signal.get("setup_type") or "", "regime": signal.get("market_regime") or "",
            "size_weight": float(pa["size_weight"]), "paper_action": pa["paper_action"],
            "size_reason": pa["reason"], "actionability_source": pa["source"],
            "overlay_version": pa.get("overlay_version"),
            "overlay_config_hash": pa.get("overlay_config_hash"),
        })
    # This lane has its own immutable MEXC-candle lifecycle and never writes
    # paper_execution_outcomes. Append only terminal rows to the common Paper
    # accounting input so its USD PnL appears in the same balance/calendar.
    from src.stocks.mexc_stock_futures_paper import closed_trade_rows

    mexc_stock_trades = closed_trade_rows(con)
    trades.extend(mexc_stock_trades)
    stats["mexc_stock_futures_closed"] = len(mexc_stock_trades)
    trades.sort(key=lambda t: t["entry_at"] or "")
    con.close()
    return trades, stats


def main(*, refresh_counterfactual: bool = False,
         refresh_execution: bool = True):
    cfg = load_cfg()
    now = datetime.now(timezone.utc)
    date = now.date().isoformat()
    # The full overlay counterfactual is intentionally a separate 2x/day
    # scheduler step. Replaying it on every ledger refresh can hold the SQLite
    # writer lock for minutes and leave the visible Paper balance stale. The
    # ledger consumes the last completed point-in-time reconstruction; callers
    # that explicitly need a new replay can opt in below.
    if refresh_counterfactual:
        try:
            from src.execution import crypto_overlay_counterfactual as _cf
            _cf.refresh()
        except Exception as e:  # noqa: BLE001
            print(f"(crypto counterfactual refresh skipped, non-fatal: {e})")
    if refresh_execution:
        con = _connect(); con.row_factory = sqlite3.Row
        try:
            pe_stats = backfill_all(con, now_iso=now.isoformat())
            con.commit()
            print(f"(paper execution refreshed: {pe_stats})")
        finally:
            con.close()
    else:
        print("(paper execution refresh skipped: scheduler already refreshed the bounded batch)")
    trades, stats = load_trades()
    print(f"=== {len(trades)} deduped actionable paper trades (chronological) ===")
    print(f"    overlay sizing: full={stats['full']} half={stats['half']} "
          f"shadow_excluded={stats['shadow_excluded']} "
          f"latency_unverified_excluded={stats['latency_unverified_excluded']} "
          f"| by_source={stats['by_source']}")

    profiles = ["zero", "bybit_non_vip_usdt_perp", "mexc_default_futures", "conservative_taker"]
    summaries = {}
    runs = {}
    default_run = None
    for fp in profiles:
        run = simulate_portfolio(trades, cfg=cfg, fee_profile=fp, now_iso=now.isoformat())
        summaries[fp] = run["summary"]
        runs[fp] = run
        if fp == cfg["fee_profile"]:
            default_run = run

    print(f"\n{'fee_profile':24}{'final$':>10}{'net$':>10}{'ret%':>8}{'maxDD%':>8}{'fees$':>9}{'W/L/BE':>12}")
    for fp, s in summaries.items():
        print(f"{fp:24}{s['final_equity_usdt']:>10}{s['net_pnl_usdt']:>10}{s['return_pct']:>8}"
              f"{s['max_drawdown_pct']:>8}{s['total_fees_slippage_usdt']:>9}"
              f"{str(s['wins'])+'/'+str(s['losses'])+'/'+str(s['breakeven']):>12}")

    os.makedirs("data/research", exist_ok=True)
    curve_path = f"data/research/paper_portfolio_equity_curve_{date}.csv"
    ledger_path = f"data/research/paper_portfolio_ledger_{date}.csv"
    with open(curve_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["timestamp", "equity", "symbol", "net_pnl_usdt"])
        for p in default_run["equity_curve"]:
            w.writerow([p["timestamp"], p["equity"], p["symbol"], p["net_pnl_usdt"]])
    with open(ledger_path, "w", newline="", encoding="utf-8") as fh:
        cols = list(default_run["ledger"][0].keys()) if default_run["ledger"] else []
        w = csv.writer(fh); w.writerow(cols)
        for r in default_run["ledger"]:
            w.writerow([r.get(c) for c in cols])
    print(f"\nwrote {curve_path}\nwrote {ledger_path}")

    # persist ALL profile ledgers; drop any orphaned legacy profiles first so the
    # backend never sums across profiles. replace_ledger is idempotent per profile.
    # KEEP the structural/maker-first B book (built by scripts.structural_maker_backfill).
    keep = profiles + ["bybit_structural_maker_first"]
    con = _connect()
    ensure_tables(con)
    ph = ",".join("?" * len(keep))
    con.execute(f"DELETE FROM paper_portfolio_ledger WHERE fee_profile NOT IN ({ph})", tuple(keep))
    con.commit()
    total = 0
    for fp in profiles:
        total += replace_ledger(con, runs[fp]["ledger"], fp)
        # A fee profile is the atomic read unit in the UI. Commit each profile
        # separately so rebuilding four books never monopolizes SQLite while a
        # fresh Paper entry is waiting to be recorded.
        con.commit()
    print(f"persisted {total} ledger rows across {len(profiles)} fee profiles "
          f"(active={cfg['fee_profile']}) into paper_portfolio_ledger")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Rebuild the derived Paper portfolio ledger.")
    parser.add_argument("--refresh-counterfactual", action="store_true",
                        help="also run the heavy crypto overlay counterfactual replay")
    parser.add_argument("--skip-execution-refresh", action="store_true",
                        help="reuse the latest paper_execution_outcomes instead of recomputing them")
    args = parser.parse_args()
    main(
        refresh_counterfactual=args.refresh_counterfactual,
        refresh_execution=not args.skip_execution_refresh,
    )
