"""PART 5/8 — Integrated paper backfill: mechanical-taker (A) vs structural +
maker-first + fee-aware + 2x (B). Derived, read-only; never touches signal_outcomes.

B re-prices the SAME Model-F R base with: maker-first fee rates (maker on pullback
entry + TP exits), fee-aware skips (EXTREME_FEE_DRAG / TIGHT_STOP dropped), 2x-safe
sizing, and an attached structural TP set (round-number/ATR structure in the
backfill; full swing/VP structure applies to FORWARD trades via the live engine).
"""
from __future__ import annotations
import csv, os, sqlite3
from datetime import datetime, timezone

from scripts.paper_portfolio_backfill import load_trades
from src.execution.paper_portfolio import (load_cfg, simulate_portfolio, ensure_tables,
                                           replace_ledger, resolve_cost_context, _funding_for_trade,
                                           _load_funding_index)
from src.execution.position_sizing import size_position
from src.execution.fees import trade_costs
from src.execution.fee_aware_execution import assess_fees
from src.execution.maker_first_execution import plan_for
from src.execution.structural_tp_engine import generate_structural_tps

DB = "db/crypto_ai_desk.sqlite"
_PULLBACK = {"crypto_swing_narrative_rs_momentum", "crypto_failed_bounce_short",
             "stocks_swing_watchlist_rs_rotation"}


def simulate_b(trades, cfg, fee_profile, now_iso):
    trades = list(trades)
    cfg = dict(cfg)
    _load_funding_index(cfg, trades, fee_profile)
    equity = float(cfg["initial_equity_usdt"]); peak = equity; max_dd = 0.0
    ledger = []; wins = losses = be = 0
    fees_tot = skipped = maker_fills = maker_miss = struct_used = 0
    for t in trades:
        per = t.get("paper_execution_r"); entry = t.get("entry"); stop = t.get("stop")
        if per is None or not entry or not stop or abs(entry - stop) <= 0:
            continue
        long = (t.get("direction") or "long").lower() != "short"
        risk_abs = abs(entry - stop)
        sz = size_position(equity_usdt=equity, entry_price=entry, stop_price=stop,
                           direction=t.get("direction") or "long", risk_pct=float(cfg["risk_per_trade_pct"]),
                           max_leverage=int(cfg["max_leverage"]), max_margin_pct=float(cfg["max_margin_per_trade_pct"]),
                           max_notional_pct=float(cfg["max_notional_per_trade_pct"]),
                           liquidation_buffer_to_stop=float(cfg["liquidation_buffer_to_stop"]))
        # structural TP (round/ATR in backfill; forward uses live candles)
        stp = generate_structural_tps(entry=entry, stop=stop, direction=t.get("direction") or "long",
                                      candles=None, atr=risk_abs, market_regime=t.get("regime"),
                                      playbook=t.get("playbook"), mechanical_tp1=t.get("tp1"))
        if stp.tp_set_label in ("STRUCTURAL", "HYBRID"):
            struct_used += 1
        # maker-first plan
        reached_tp = per > 0
        pb = t.get("playbook") or ""
        is_pullback = (pb in _PULLBACK) or any(k in pb.lower() for k in ("swing", "failed_bounce", "retest", "pullback", "bounce"))
        plan = plan_for(playbook=pb, setup_is_pullback=is_pullback, is_urgent=not is_pullback,
                        reached_tp=reached_tp, expired=("expired" in str(t.get("close_reason") or "")),
                        invalid_or_stale=("stop" in str(t.get("close_reason") or "")))
        if plan.maker_fill_status == "maker_filled":
            maker_fills += 1
        if plan.maker_entry_missed:
            maker_miss += 1
        exit_price = entry + (per * risk_abs if long else -per * risk_abs)
        exit_notional = sz.qty * exit_price
        # asset-aware cost model (SAME selection as the A-book): stocks → equity/ETF profile +
        # stock slippage + funding 0; crypto → futures profile + crypto slippage + approx funding.
        # No relabelling: cost.fee_source is the HONEST model actually applied.
        eff_profile, eff_slip, eff_majors, fund_arg = resolve_cost_context(
            asset_class=t.get("asset_class"), mode=t.get("mode"),
            notional_usdt=sz.notional_usdt, fee_profile=fee_profile, cfg=cfg)
        funding = _funding_for_trade(t, notional_usdt=sz.notional_usdt,
                                     fee_profile=fee_profile, approximate=fund_arg, cfg=cfg)
        fund_arg = funding["funding_usdt"]
        # fee-aware gate
        fa = assess_fees(notional_usdt=sz.notional_usdt, exit_notional_usdt=exit_notional,
                         risk_usdt=sz.actual_risk_usdt or 1e-9, symbol=t.get("symbol") or "",
                         fee_profile=eff_profile, entry_order_type=plan.entry_order_type,
                         exit_order_type=plan.exit_order_type, slip_cfg=eff_slip, majors=eff_majors,
                         tp1_r=stp.tp1_r, stop_distance_pct=sz.stop_distance_pct, expected_gross_r=per,
                         max_fee_r_cost=0.35, skip_extreme_fee_drag=True)
        if fa.action == "paper_skipped_fee_drag":
            skipped += 1
            continue
        cost = trade_costs(notional_usdt=sz.notional_usdt, exit_notional_usdt=exit_notional,
                           symbol=t.get("symbol") or "", fee_profile=eff_profile,
                           entry_order_type=plan.entry_order_type, exit_order_type=plan.exit_order_type,
                           slip_cfg=eff_slip, majors=eff_majors, funding_usdt=fund_arg)
        gross = per * sz.actual_risk_usdt
        net = gross - cost.total_cost_usdt
        eb = equity; equity = round(equity + net, 6); peak = max(peak, equity)
        max_dd = max(max_dd, (peak - equity) / peak if peak else 0.0)
        if net > 0: wins += 1
        elif net < 0: losses += 1
        else: be += 1
        fees_tot += cost.fee_usdt + cost.slippage_usdt
        ledger.append({
            "signal_id": t.get("signal_id"), "economic_trade_key": t.get("economic_trade_key"),
            "timestamp": t.get("entry_at"), "event_type": "exit", "equity_before": round(eb, 4),
            "equity_after": round(equity, 4), "realized_pnl_usdt": round(net, 4), "unrealized_pnl_usdt": 0.0,
            "gross_pnl_usdt": round(gross, 4), "fees_usdt": cost.fee_usdt, "slippage_usdt": cost.slippage_usdt,
            "funding_usdt": cost.funding_usdt, "net_pnl_usdt": round(net, 4), "risk_usdt": sz.actual_risk_usdt,
            "risk_pct": sz.actual_risk_pct, "position_notional_usdt": sz.notional_usdt,
            "margin_used_usdt": sz.margin_used_usdt, "leverage_used": sz.leverage_used, "qty": sz.qty,
            "entry_price": entry, "exit_price": round(exit_price, 10), "stop_initial": stop,
            "stop_current": t.get("stop_current_r"), "paper_execution_r": round(per, 4),
            "close_reason": (t.get("close_reason") or "") + f"|{plan.entry_order_type}E/{plan.exit_order_type}X|{stp.tp_set_label}",
            "risk_model": "structural_maker_first_2x", "fee_profile": fee_profile,
            "expiry_close_price": None, "expiry_close_price_source": None,
            "fee_estimated": int(cost.fee_estimated), "fee_source": cost.fee_source,
            "funding_source": funding["source"], "funding_estimated": funding["estimated"],
            "funding_event_count": funding["events"], "created_at": now_iso,
        })
    n = wins + losses + be
    summ = {"final_equity_usdt": round(equity, 2), "net_pnl_usdt": round(equity - float(cfg["initial_equity_usdt"]), 2),
            "return_pct": round((equity / float(cfg["initial_equity_usdt"]) - 1) * 100, 2),
            "max_drawdown_pct": round(max_dd * 100, 2), "fees_slip_usdt": round(fees_tot, 2),
            "trades": n, "wins": wins, "losses": losses, "be": be, "skipped_fee_drag": skipped,
            "maker_fills": maker_fills, "maker_missed": maker_miss, "structural_tp_used": struct_used}
    return {"summary": summ, "ledger": ledger}


def main():
    cfg = load_cfg(); now = datetime.now(timezone.utc); date = now.date().isoformat()
    trades = load_trades()
    print(f"=== {len(trades)} deduped actionable paper trades ===")
    profiles = ["zero", "bybit_non_vip_usdt_perp", "mexc_default_futures", "conservative_taker"]
    print(f"\n{'profile':26}{'A_mech_taker$':>14}{'B_struct_maker$':>16}{'A_fees':>9}{'B_fees':>9}{'B_skip':>7}{'B_makerFill':>12}")
    persist = None
    for fp in profiles:
        a = simulate_portfolio(trades, cfg=cfg, fee_profile=fp, now_iso=now.isoformat())["summary"]
        b = simulate_b(trades, cfg, fp, now.isoformat())
        bs = b["summary"]
        print(f"{fp:26}{a['final_equity_usdt']:>14}{bs['final_equity_usdt']:>16}"
              f"{a['total_fees_slippage_usdt']:>9}{bs['fees_slip_usdt']:>9}{bs['skipped_fee_drag']:>7}{bs['maker_fills']:>12}")
        if fp == cfg["fee_profile"]:
            persist = b
    print(f"\nB struct/maker detail (active profile): structural_tp_used={persist['summary']['structural_tp_used']} "
          f"maker_fills={persist['summary']['maker_fills']} maker_missed={persist['summary']['maker_missed']} "
          f"skipped_fee_drag={persist['summary']['skipped_fee_drag']} maxDD={persist['summary']['max_drawdown_pct']}%")
    # persist B under a distinct profile key so the app can show structural/maker-first
    # dedup by economic_trade_key (ledger UNIQUE(key,event_type,fee_profile))
    seen = {}
    for r in persist["ledger"]:
        r = dict(r); r["fee_profile"] = "bybit_structural_maker_first"   # relabel to persist key
        seen[r["economic_trade_key"]] = r
    deduped = list(seen.values())
    con = sqlite3.connect(DB); ensure_tables(con)
    n = replace_ledger(con, deduped, "bybit_structural_maker_first")
    con.commit()
    print(f"persisted {n} B rows (fee_profile=bybit_structural_maker_first)")
    os.makedirs("data/research", exist_ok=True)
    out = f"data/research/structural_maker_comparison_{date}.csv"
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["profile", "A_mech_taker_final", "B_struct_maker_final", "A_fees", "B_fees", "B_skipped", "B_maker_fills"])
        for fp in profiles:
            a = simulate_portfolio(trades, cfg=cfg, fee_profile=fp)["summary"]
            b = simulate_b(trades, cfg, fp, now.isoformat())["summary"]
            w.writerow([fp, a["final_equity_usdt"], b["final_equity_usdt"], a["total_fees_slippage_usdt"], b["fees_slip_usdt"], b["skipped_fee_drag"], b["maker_fills"]])
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
