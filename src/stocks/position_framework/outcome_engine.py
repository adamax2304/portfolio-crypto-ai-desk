"""Phase 1 outcome engine — SHADOW / READ-MODEL only.

Simulates realistic daily-bar execution for a shadow candidate and reports **USD net PnL** (never
final_r / touch-R). Long-only. Honesty rules:
  * NO fake fills — a trade only fills if a daily bar actually trades through the entry; if there
    aren't enough forward bars the outcome stays `pending`.
  * Gaps through the entry or the stop fill at the realistic OPEN, not an ideal price.
  * Stop is checked before targets within a bar (pessimistic — we can't see intrabar order).
  * Partials (+2R / +3R) only book if price actually reached them; results are NOT rounded to
    whole R.
  * Fees + slippage use a US-equity model (commission-free + a few bps slippage; no perp funding).

Pure functions (`simulate_trade`, `aggregate`) are unit-testable offline. `compute_outcomes` does
the IO (reads candidates, pulls daily bars, writes the shadow outcomes table).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable
from zoneinfo import ZoneInfo

try:
    import pandas as pd
except Exception:  # pragma: no cover
    pd = None

from . import shadow_store
from .config import load_config


_US_MARKET_TZ = ZoneInfo("America/New_York")


def _num(v):
    try:
        return None if v is None else float(v)
    except (TypeError, ValueError):
        return None


def _leg_costs(fill_px: float, qty: float, cfg_exec: dict) -> tuple[float, float]:
    """(commission_usd, slippage_usd) for one fill leg — US equity model."""
    commission = float(cfg_exec.get("commission_per_share", 0.0)) * abs(qty)
    slippage = float(cfg_exec.get("slippage_bps", 5)) / 1e4 * abs(fill_px) * abs(qty)
    return round(commission, 4), round(slippage, 4)


def simulate_trade(df, start_idx: int, plan: dict, cfg_exec: dict | None = None) -> dict[str, Any]:
    """Simulate one long candidate over daily bars. `df` is the FULL daily OHLCV (ascending) with
    enough history for EMA21/SMA50; `start_idx` is the first bar eligible for entry (bar at/after
    the scan). Returns a per-trade dict (status: closed / pending / no_entry).
    """
    cfg_exec = cfg_exec or {}
    entry = _num(plan.get("entry_price"))
    stop = _num(plan.get("stop_price"))
    tp1, tp2 = _num(plan.get("tp1")), _num(plan.get("tp2"))
    tp1_pct = float(plan.get("tp1_pct", 0.5))
    tp2_pct = float(plan.get("tp2_pct", 0.25))
    qty = _num(plan.get("qty"))
    max_hold = int(plan.get("max_holding_days", 40))
    entry_valid = int(cfg_exec.get("entry_valid_days", 5))
    min_fwd = int(cfg_exec.get("min_forward_bars", 3))

    base = {"status": "pending", "exit_reason": None, "entry_date": None, "exit_date": None,
            "entry_px": None, "exit_px": None, "qty": qty, "notional_usd": None,
            "gross_usd": None, "fees_usd": None, "slippage_usd": None, "net_usd": None,
            "net_pct": None, "mfe_r": None, "mae_r": None, "holding_days": 0,
            "setup_type": plan.get("setup_variant"), "sector": plan.get("sector"),
            "symbol": plan.get("symbol")}
    if pd is None or df is None or entry is None or stop is None or qty is None or entry <= stop:
        base["exit_reason"] = "invalid inputs"
        return base
    n = len(df)
    if n - start_idx < min_fwd:
        base["exit_reason"] = "insufficient forward bars"
        return base

    close = df["close"]
    ema21 = close.ewm(span=21, adjust=False).mean()
    sma50 = close.rolling(50).mean()

    # ---- entry ----
    # breakout / continuation are BUY-STOPS (fill as price clears the level from below); a gap-up
    # OPEN above the entry still fills at the open (worse), it is NOT a no-entry. pullback / reclaim
    # are BUY-LIMITS (fill as price dips to the level); a gap-down OPEN below fills at the open.
    variant = plan.get("setup_variant") or ""
    is_stop_entry = variant in ("breakout", "consolidation_continuation")
    fill_idx = None
    fill_px = None
    for i in range(start_idx, min(start_idx + entry_valid, n)):
        lo, hi, op = float(df["low"].iloc[i]), float(df["high"].iloc[i]), float(df["open"].iloc[i])
        if is_stop_entry:
            if hi >= entry:
                fill_px = op if op > entry else entry     # gap-up through the buy-stop → pay the open
                fill_idx = i
                break
        else:
            if lo <= entry:
                fill_px = op if op < entry else entry      # gap-down through the buy-limit → get the open
                fill_idx = i
                break
    if fill_idx is None:
        base["status"] = "no_entry"
        base["exit_reason"] = "entry not reached in window"
        return base

    # ACTUAL per-share risk uses the REAL fill (a gap fill above the planned entry cuts real R).
    # Used only for the auxiliary MFE/MAE-in-R metrics; USD net stays authoritative.
    actual_risk = fill_px - stop
    r_ref = actual_risk if actual_risk > 0 else (entry - stop)

    entry_comm, entry_slip = _leg_costs(fill_px, qty, cfg_exec)
    commission = entry_comm
    slippage = entry_slip
    gross = 0.0
    remaining = qty
    tp1_done = tp2_done = False
    mfe = mae = fill_px
    exit_reason = None
    exit_idx = None
    final_exit_px = None
    last_close = fill_px

    def _book(exit_px: float, q: float):
        nonlocal gross, commission, slippage
        gross += (exit_px - fill_px) * q
        c, s = _leg_costs(exit_px, q, cfg_exec)
        commission += c
        slippage += s

    for j in range(fill_idx, min(fill_idx + max_hold + 1, n)):
        lo, hi, op, cl = (float(df["low"].iloc[j]), float(df["high"].iloc[j]),
                          float(df["open"].iloc[j]), float(df["close"].iloc[j]))
        last_close = cl
        mfe = max(mfe, hi)
        mae = min(mae, lo)
        # 1) stop first (pessimistic). Gap-down through stop → exit at the OPEN; else at the stop.
        if lo <= stop:
            exit_px = op if op < stop else stop
            _book(exit_px, remaining)
            remaining = 0.0
            exit_reason, exit_idx, final_exit_px = "stop", j, exit_px
            break
        # 2) partial targets (only if actually reached; gap-up fills better at open)
        if not tp1_done and tp1 is not None and hi >= tp1:
            px = op if op > tp1 else tp1
            q = qty * tp1_pct
            _book(px, q)
            remaining -= q
            tp1_done = True
        if not tp2_done and tp2 is not None and hi >= tp2:
            px = op if op > tp2 else tp2
            q = qty * tp2_pct
            _book(px, q)
            remaining -= q
            tp2_done = True
        # 3) structure / trail / time exits fill on the CLOSE (for the remainder)
        s50 = sma50.iloc[j]
        e21 = ema21.iloc[j]
        held = j - fill_idx
        if remaining > 1e-9:
            if pd.notna(s50) and cl < float(s50):
                _book(cl, remaining); remaining = 0.0; exit_reason, exit_idx, final_exit_px = "below_50d", j, cl; break
            if tp1_done and pd.notna(e21) and cl < float(e21):
                _book(cl, remaining); remaining = 0.0; exit_reason, exit_idx, final_exit_px = "ema21_trail", j, cl; break
            if held >= max_hold:
                _book(cl, remaining); remaining = 0.0; exit_reason, exit_idx, final_exit_px = "max_hold", j, cl; break

    if remaining > 1e-9 and exit_reason is None:
        # ran out of available bars before an exit condition → still OPEN (honest: no forced fill)
        base["status"] = "pending"
        base["exit_reason"] = "open (insufficient forward bars to resolve)"
        base["entry_date"] = str(df.index[fill_idx].date()) if hasattr(df.index[fill_idx], "date") else str(df.index[fill_idx])
        base["entry_px"] = round(fill_px, 4)
        base["notional_usd"] = round(fill_px * qty, 2)
        base["mfe_r"] = round((mfe - fill_px) / r_ref, 4)
        base["mae_r"] = round((mae - fill_px) / r_ref, 4)
        base["holding_days"] = int(n - 1 - fill_idx)
        return base

    fees = round(commission, 4)
    slip = round(slippage, 4)
    net = round(gross - fees - slip, 2)
    notional = fill_px * qty
    exit_bar = exit_idx if exit_idx is not None else (n - 1)
    exit_dt = df.index[exit_bar]
    entry_dt = df.index[fill_idx]
    base.update({
        "status": "closed", "exit_reason": exit_reason or "window_end",
        "entry_date": str(entry_dt.date()) if hasattr(entry_dt, "date") else str(entry_dt),
        "exit_date": str(exit_dt.date()) if hasattr(exit_dt, "date") else str(exit_dt),
        "entry_px": round(fill_px, 4),
        # actual closing FILL price (stop / open-on-gap / close-on-structure-exit), never bar close
        "exit_px": round(final_exit_px if final_exit_px is not None else last_close, 4),
        "notional_usd": round(notional, 2), "gross_usd": round(gross, 2),
        "fees_usd": fees, "slippage_usd": slip, "net_usd": net,
        "net_pct": round(net / notional, 5) if notional else None,
        "mfe_r": round((mfe - fill_px) / r_ref, 4),
        "mae_r": round((mae - fill_px) / r_ref, 4),
        "holding_days": int(exit_bar - fill_idx),
    })
    return base


def aggregate(trades: list[dict]) -> dict[str, Any]:
    """Portfolio metrics over CLOSED trades. USD net is authoritative."""
    closed = [t for t in trades if t.get("status") == "closed" and t.get("net_usd") is not None]
    out: dict[str, Any] = {
        "closed_trades": len(closed), "pending": sum(1 for t in trades if t.get("status") == "pending"),
        "no_entry": sum(1 for t in trades if t.get("status") == "no_entry"),
        "total_net_usd": 0.0, "avg_net_usd": None, "winrate": None, "profit_factor": None,
        "expectancy_usd": None, "max_drawdown_usd": None, "by_sector": {}, "by_setup": {},
    }
    if not closed:
        return out
    nets = [t["net_usd"] for t in closed]
    wins = [x for x in nets if x > 0]
    losses = [x for x in nets if x < 0]
    total = round(sum(nets), 2)
    out["total_net_usd"] = total
    out["avg_net_usd"] = round(total / len(nets), 2)
    out["winrate"] = round(len(wins) / len(nets), 4)
    gross_win = sum(wins)
    gross_loss = abs(sum(losses))
    out["profit_factor"] = round(gross_win / gross_loss, 3) if gross_loss > 0 else (None if not wins else float("inf"))
    out["expectancy_usd"] = round(total / len(nets), 2)
    # max drawdown on the ordered (by exit_date) equity curve
    ordered = sorted(closed, key=lambda t: t.get("exit_date") or "")
    equity = 0.0
    peak = 0.0
    max_dd = 0.0
    for t in ordered:
        equity += t["net_usd"]
        peak = max(peak, equity)
        max_dd = min(max_dd, equity - peak)
    out["max_drawdown_usd"] = round(max_dd, 2)
    for key, field in (("by_sector", "sector"), ("by_setup", "setup_type")):
        agg: dict[str, dict] = {}
        for t in closed:
            k = t.get(field) or "unknown"
            a = agg.setdefault(k, {"n": 0, "net_usd": 0.0})
            a["n"] += 1
            a["net_usd"] = round(a["net_usd"] + t["net_usd"], 2)
        out[key] = agg
    return out


def _start_idx_for(df, created_at: str) -> int | None:
    """First bar index at/after the scan date.

    Cached daily CSVs can contain mixed DST offsets (``-04:00`` / ``-05:00``).
    Pandas then leaves the index as strings. Normalize both the scan timestamp
    and bars to the US market date: an after-close scan can be the next UTC day
    while still belonging to the same US trading session.
    """
    try:
        created = datetime.fromisoformat(str(created_at).replace("Z", "+00:00"))
        cutoff = (created.astimezone(_US_MARKET_TZ).date() if created.tzinfo else created.date())
    except Exception:
        return None
    for i in range(len(df)):
        try:
            if pd is not None:
                d = pd.to_datetime(df.index[i], utc=True, errors="coerce")
                dd = d.tz_convert(_US_MARKET_TZ).date() if not pd.isna(d) else None
            else:  # pragma: no cover - outcome simulation itself requires pandas
                d = df.index[i]
                dd = d.date() if hasattr(d, "date") else None
        except (TypeError, ValueError):
            dd = None
        if dd is not None and dd >= cutoff:
            return i
    return None


def compute_outcomes(*, price_provider: Callable[[str], Any], cfg: dict | None = None,
                     db_path=None) -> dict[str, Any]:
    """Simulate outcomes for all open shadow candidates and persist them. `price_provider(symbol)`
    returns a daily OHLCV DataFrame (ascending) or None. Returns the aggregate summary. Honest:
    candidates without enough forward data are written as `pending` (no fake PnL)."""
    cfg = cfg or load_config()
    cfg_exec = cfg.get("execution") or {}
    now = datetime.now(timezone.utc).isoformat()
    trades: list[dict] = []
    for cand in shadow_store.open_candidates(db_path=db_path):
        sym = cand.get("symbol")
        df = None
        try:
            df = price_provider(sym)
        except Exception:
            df = None
        if df is None or not len(df):
            shadow_store.upsert_outcome(cand["candidate_id"], checked_at=now, status="pending",
                                        fields={"notes": {"reason": "no daily bars"}}, db_path=db_path)
            continue
        # recompute qty from the stored risk budget (risk_usd / per-share risk)
        entry, stop = _num(cand.get("entry_price")), _num(cand.get("stop_price"))
        risk_usd = _num(cand.get("risk_usd"))
        qty = (risk_usd / (entry - stop)) if (entry and stop and risk_usd and entry > stop) else None
        plan = {**cand, "qty": qty}
        start = _start_idx_for(df, cand.get("created_at"))
        if start is None:
            shadow_store.upsert_outcome(cand["candidate_id"], checked_at=now, status="pending",
                                        fields={"notes": {"reason": "scan date not in bars"}}, db_path=db_path)
            continue
        res = simulate_trade(df, start, plan, cfg_exec)
        trades.append(res)
        # Terminal outcome → flip the candidate out of the open list (open/closed consistency).
        _terminal = {"closed": "shadow_closed", "no_entry": "shadow_no_entry"}
        if res["status"] in _terminal:
            shadow_store.set_candidate_status(cand["candidate_id"], _terminal[res["status"]], db_path=db_path)
        shadow_store.upsert_outcome(
            cand["candidate_id"], checked_at=now, status=res["status"],
            fields={"close_reason": res.get("exit_reason"), "last_price": res.get("exit_px") or res.get("entry_px"),
                    "realized_pnl_usd": res.get("net_usd"), "net_pnl_usd": res.get("net_usd"),
                    "max_favorable_excursion_r": res.get("mfe_r"), "max_adverse_excursion_r": res.get("mae_r"),
                    "holding_days": res.get("holding_days"),
                    "notes": {k: res.get(k) for k in ("entry_date", "exit_date", "entry_px", "exit_px",
                                                       "qty", "notional_usd", "gross_usd", "fees_usd",
                                                       "slippage_usd", "net_pct", "setup_type", "sector")}},
            db_path=db_path)
    summary = aggregate(trades)
    summary["computed_at"] = now
    summary["shadow_only"] = True
    return summary
