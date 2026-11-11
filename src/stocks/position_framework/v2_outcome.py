"""Next-session, gap-aware outcome engine for Stocks Position Swing V2."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable
from zoneinfo import ZoneInfo

try:
    import pandas as pd
except Exception:  # pragma: no cover
    pd = None

from . import v2_store
from .v2_config import load_config

NY = ZoneInfo("America/New_York")


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _market_date(value: Any):
    if pd is None:
        return None
    try:
        dt = pd.to_datetime(value, utc=True, errors="coerce")
        return None if pd.isna(dt) else dt.tz_convert(NY).date()
    except Exception:
        return None


def first_bar_after_scan(df, created_at: str) -> int | None:
    try:
        scan = datetime.fromisoformat(str(created_at).replace("Z", "+00:00"))
        scan_date = scan.astimezone(NY).date() if scan.tzinfo else scan.date()
    except Exception:
        return None
    for idx in range(len(df)):
        bar_date = _market_date(df.index[idx])
        if bar_date is not None and bar_date > scan_date:
            return idx
    return None


def _coverage_status(df, start_idx: int) -> tuple[bool, str]:
    if pd is None or df is None or start_idx is None:
        return False, "NO_FRAME"
    required = {"open", "high", "low", "close", "volume"}
    if not required.issubset(set(df.columns)):
        return False, "MISSING_OHLCV_COLUMNS"
    if not df.index.is_unique:
        return False, "DUPLICATE_BAR_INDEX"
    if start_idx >= len(df):
        return False, "NO_FORWARD_SESSION"
    forward = df.iloc[start_idx:]
    if forward[["open", "high", "low", "close"]].isna().any().any():
        return False, "FORWARD_OHLC_MISSING"
    return True, "CLEAN"


def _cost(fill: float, qty: float, execution: dict[str, Any]) -> tuple[float, float]:
    fee = float(execution.get("commission_per_share", 0.0)) * abs(qty)
    slip = float(execution.get("slippage_bps", 7)) / 1e4 * abs(fill) * abs(qty)
    return fee, slip


def simulate(
    df,
    start_idx: int,
    candidate: dict[str, Any],
    execution: dict[str, Any],
) -> dict[str, Any]:
    base = {
        "status": "pending",
        "entry_date": None,
        "exit_date": None,
        "entry_px": None,
        "exit_px": None,
        "close_reason": None,
        "gross_pnl_usd": None,
        "fees_usd": None,
        "slippage_usd": None,
        "funding_usd": 0.0,
        "net_pnl_usd": None,
        "net_pct": None,
        "max_favorable_excursion_r": None,
        "max_adverse_excursion_r": None,
        "holding_days": 0,
        "gap_loss_r": None,
        "same_bar_ambiguous": False,
        "data_clean": True,
        "coverage_status": "CLEAN",
    }
    if pd is None or df is None:
        base.update(status="invalid", close_reason="NO_FRAME", data_clean=False,
                    coverage_status="NO_FRAME")
        return base
    clean, coverage = _coverage_status(df, start_idx)
    if not clean:
        base.update(status="invalid", close_reason=coverage, data_clean=False,
                    coverage_status=coverage)
        return base

    entry = _f(candidate.get("entry_price"))
    stop = _f(candidate.get("stop_price"))
    atr = _f(candidate.get("atr14"))
    qty = _f(candidate.get("qty"))
    tp1 = _f(candidate.get("tp1"))
    tp2 = _f(candidate.get("tp2"))
    if not all(value is not None for value in (entry, stop, atr, qty)) or entry <= stop:
        base.update(status="invalid", close_reason="INVALID_PLAN", data_clean=False,
                    coverage_status="INVALID_PLAN")
        return base
    if len(df) - start_idx < int(execution.get("min_forward_bars", 3)):
        base["close_reason"] = "INSUFFICIENT_FORWARD_BARS"
        return base

    valid_sessions = int(execution.get("entry_valid_sessions", 3))
    max_chase = float(execution.get("max_chase_atr", 0.5)) * atr
    fill_idx = None
    fill_px = None
    chase_skips = 0
    for idx in range(start_idx, min(len(df), start_idx + valid_sessions)):
        row = df.iloc[idx]
        op, hi, lo = float(row["open"]), float(row["high"]), float(row["low"])
        if op < stop:
            base.update(status="no_entry", close_reason="GAP_INVALIDATED_BEFORE_ENTRY")
            return base
        if hi < entry:
            continue
        if op > entry + max_chase:
            chase_skips += 1
            continue
        fill_idx = idx
        fill_px = max(op, entry)
        break
    if fill_idx is None:
        base.update(
            status="no_entry",
            close_reason="EXCESSIVE_GAP_CHASE" if chase_skips else "ENTRY_NOT_REACHED",
        )
        return base

    risk = fill_px - stop
    if risk <= 0:
        base.update(status="invalid", close_reason="NON_POSITIVE_ACTUAL_RISK",
                    data_clean=False, coverage_status="INVALID_ACTUAL_RISK")
        return base
    planned_risk = entry - stop
    entry_gap_r = max(0.0, (fill_px - entry) / planned_risk) if planned_risk > 0 else 0.0
    entry_fee, entry_slip = _cost(fill_px, qty, execution)
    fees, slippage, gross = entry_fee, entry_slip, 0.0
    remaining = qty
    tp1_done = tp2_done = False
    mfe, mae = fill_px, fill_px
    close_reason = None
    exit_idx = None
    exit_px = None
    same_bar_ambiguous = False
    close = df["close"]
    ema_days = int(candidate.get("trail_ema_days") or 21)
    hard_days = int(candidate.get("hard_exit_sma_days") or 50)
    ema = close.ewm(span=ema_days, adjust=False).mean()
    sma = close.rolling(hard_days).mean()
    max_hold = int(candidate.get("max_holding_days") or 40)
    tp1_pct = float(candidate.get("tp1_pct") or 0.5)
    tp2_pct = float(candidate.get("tp2_pct") or 0.25)

    def book(px: float, close_qty: float) -> None:
        nonlocal gross, fees, slippage
        gross += (px - fill_px) * close_qty
        fee, slip = _cost(px, close_qty, execution)
        fees += fee
        slippage += slip

    for idx in range(fill_idx, min(len(df), fill_idx + max_hold + 1)):
        row = df.iloc[idx]
        op, hi, lo, cl = map(float, (row["open"], row["high"], row["low"], row["close"]))
        mfe, mae = max(mfe, hi), min(mae, lo)
        stop_hit = lo <= stop
        entry_and_stop_same_bar = idx == fill_idx and stop_hit and hi >= entry
        if entry_and_stop_same_bar:
            same_bar_ambiguous = True
        if stop_hit:
            px = op if op < stop else stop
            book(px, remaining)
            remaining = 0.0
            close_reason = "SAME_BAR_STOP_FIRST" if same_bar_ambiguous else "STOP"
            exit_idx, exit_px = idx, px
            break
        if not tp1_done and tp1 is not None and hi >= tp1:
            px = op if op > tp1 else tp1
            close_qty = qty * tp1_pct
            book(px, close_qty)
            remaining -= close_qty
            tp1_done = True
        if not tp2_done and tp2 is not None and hi >= tp2:
            px = op if op > tp2 else tp2
            close_qty = qty * tp2_pct
            book(px, close_qty)
            remaining -= close_qty
            tp2_done = True
        held = idx - fill_idx
        if remaining > 1e-9 and pd.notna(sma.iloc[idx]) and cl < float(sma.iloc[idx]):
            book(cl, remaining)
            remaining = 0.0
            close_reason, exit_idx, exit_px = "BELOW_50D", idx, cl
            break
        if (
            remaining > 1e-9
            and tp1_done
            and pd.notna(ema.iloc[idx])
            and cl < float(ema.iloc[idx])
        ):
            book(cl, remaining)
            remaining = 0.0
            close_reason, exit_idx, exit_px = "EMA21_TRAIL", idx, cl
            break
        if remaining > 1e-9 and held >= max_hold:
            book(cl, remaining)
            remaining = 0.0
            close_reason, exit_idx, exit_px = "MAX_HOLD", idx, cl
            break

    entry_date = str(_market_date(df.index[fill_idx]))
    if remaining > 1e-9 and close_reason is None:
        base.update(
            status="pending",
            entry_date=entry_date,
            entry_px=round(fill_px, 6),
            qty=qty,
            notional_usd=round(fill_px * qty, 2),
            max_favorable_excursion_r=round((mfe - fill_px) / risk, 4),
            max_adverse_excursion_r=round((mae - fill_px) / risk, 4),
            holding_days=max(0, len(df) - 1 - fill_idx),
            gap_loss_r=round(entry_gap_r, 4),
            close_reason="OPEN",
        )
        return base

    net = gross - fees - slippage
    notional = fill_px * qty
    base.update(
        status="closed",
        entry_date=entry_date,
        exit_date=str(_market_date(df.index[exit_idx])),
        entry_px=round(fill_px, 6),
        exit_px=round(float(exit_px), 6),
        close_reason=close_reason,
        qty=qty,
        notional_usd=round(notional, 2),
        gross_pnl_usd=round(gross, 4),
        fees_usd=round(fees, 4),
        slippage_usd=round(slippage, 4),
        net_pnl_usd=round(net, 2),
        net_pct=round(net / notional, 6) if notional else None,
        max_favorable_excursion_r=round((mfe - fill_px) / risk, 4),
        max_adverse_excursion_r=round((mae - fill_px) / risk, 4),
        holding_days=int(exit_idx - fill_idx),
        gap_loss_r=round(entry_gap_r, 4),
        same_bar_ambiguous=same_bar_ambiguous,
    )
    return base


def refresh(
    *,
    price_provider: Callable[[str], Any],
    cfg: dict[str, Any] | None = None,
    db_path=None,
) -> dict[str, Any]:
    cfg = cfg or load_config()
    execution = cfg.get("execution") or {}
    checked_at = datetime.now(timezone.utc).isoformat()
    counts = {"scanned": 0, "closed": 0, "pending": 0, "no_entry": 0, "invalid": 0}
    for candidate in v2_store.open_candidates(db_path):
        counts["scanned"] += 1
        try:
            frame = price_provider(str(candidate["symbol"]))
        except Exception:
            frame = None
        if frame is None or not len(frame):
            result = {
                "status": "pending",
                "close_reason": "NO_DAILY_BARS",
                "data_clean": False,
                "coverage_status": "NO_DAILY_BARS",
            }
        else:
            start_idx = first_bar_after_scan(frame, str(candidate["created_at"]))
            if start_idx is None:
                result = {
                    "status": "pending",
                    "close_reason": "NO_NEXT_SESSION_BAR",
                    "data_clean": True,
                    "coverage_status": "AWAITING_NEXT_SESSION",
                }
            else:
                expanded = dict(candidate)
                expanded["trail_ema_days"] = int((cfg.get("exits") or {}).get("trail_ema_days", 21))
                expanded["hard_exit_sma_days"] = int((cfg.get("exits") or {}).get("hard_exit_sma_days", 50))
                result = simulate(frame, start_idx, expanded, execution)
        status = str(result.get("status") or "pending")
        counts[status] = counts.get(status, 0) + 1
        notes = {
            "strategy_id": cfg.get("strategy_id"),
            "profile_version": cfg.get("profile_version"),
            "execution_profile": execution.get("profile_id"),
            "shadow_only": True,
            "same_bar_policy": execution.get("same_bar_policy", "stop_first"),
        }
        fields = {key: value for key, value in result.items() if key != "status"}
        fields["notes"] = notes
        v2_store.upsert_outcome(
            str(candidate["candidate_id"]),
            checked_at=checked_at,
            status=status,
            fields=fields,
            db_path=db_path,
        )
    counts["checked_at"] = checked_at
    counts["shadow_only"] = True
    return counts
