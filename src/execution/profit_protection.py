"""Shared entry-fill + profit-protection simulator (PAPER / READ-MODEL / ACCOUNTING ONLY).

Single source of truth for (a) MODE-SPECIFIC entry fills that mirror paper_shadow_engine,
and (b) applying the authoritative "Model F" profit protection (early_mfe_protection_v1)
to ANY entry-mode simulation used by the calibration and parameter-sweep read-models.

Entry fills are entry_mode-aware (NOT just a touch zone), faithful to
paper_shadow_engine._entry_fill / _walk:
  - PULLBACK_LIMIT        : resting maker limit; fills only on a genuine TRADE-THROUGH of
                            the zone edge (maker_trade_through_bps), not a mere touch.
  - STRUCTURAL_RETEST     : maker limit at the structural/suggested level (point zone).
  - BREAKOUT_CONTINUATION : taker through the breakout trigger/level (stop entry).
  - MOMENTUM_TAKER_NOW    : immediate taker on the first available price after created_at.
  - LIMIT_THEN_TAKER_TIMEOUT: maker limit first; taker fallback ONLY after `timeout_bars`.
  - NO_CHASE_SKIP         : never fills (avoided trade).

Model F protection REUSES the pure `compute_paper_execution` from
paper_execution_accounting.py so simulated exits match the authoritative paper book:
  initial stop = invalidation/structural stop; MFE>=+0.6R -> breakeven; MFE>=+1.0R -> lock +0.5R;
  TP3 runner; reversal-after-protection closes at the protected level; expired-armed closes at
  protected level; same-candle stop/TP conservative. Realistic net USD + exact R.

Baselines reported (honestly named):
  - no_protection_r      : TRUE no-protection — original stop held throughout, base partial-TP
                           model, NO breakeven / lock / trailing.
  - legacy_touch_r       : the pre-Model-F accounting = R of the highest TP touched.
  delta_vs_no_protection_* compares protected vs the TRUE no-protection baseline.
  delta_vs_legacy_touch_* compares protected vs the legacy touch baseline.

NEVER writes the DB; NEVER touches proposed_signals / signal_outcomes / final_r / live / orders.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from typing import Any

from src.execution.paper_execution_accounting import (
    ARM_BE_AT_R, LOCK_AT_R, LOCK_LEVEL_R, compute_paper_execution, legacy_touch_r, r_multiple,
)
from src.execution.fees import trade_costs
from src.execution.position_sizing import size_position

PROTECTION_MODELS = (
    "legacy_touch", "first_tp_close", "early_mfe_protection_v1",
    "structural_stop_with_profit_protection_v1",
)
DEFAULT_PROTECTION_MODEL = "early_mfe_protection_v1"

EQUITY_USD = 5000.0
RISK_PCT = 0.005
MAX_LEV = 5
PARTIALS = {1: 0.33, 2: 0.33, 3: 0.34}
DEFAULT_MAKER_TRADE_THROUGH_BPS = 0.0005   # mirrors paper_shadow_engine._MAKER_TRADE_THROUGH_BPS
DEFAULT_MAKER_TIMEOUT_BARS = 8             # mirrors paper_shadow_engine._MAKER_TIMEOUT_BARS
LIMIT_MODES = (
    "PULLBACK_LIMIT", "STRUCTURAL_RETEST", "LIMIT_THEN_TAKER_TIMEOUT",
    "PULLBACK_CONFIRMED_RETEST", "FIB_IMPULSE_RETEST",
)


def _f(v) -> float | None:
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return None


def _iter_ohlcv(candles: Any) -> list[dict]:
    if candles is None:
        return []
    rows = []
    if hasattr(candles, "iterrows"):
        for _, r in candles.iterrows():
            rows.append({"open": _f(r.get("open")), "high": _f(r.get("high")),
                         "low": _f(r.get("low")), "close": _f(r.get("close")),
                         "timestamp": r.get("timestamp")})
    else:
        for r in candles:
            rows.append({"open": _f(r.get("open")), "high": _f(r.get("high")),
                         "low": _f(r.get("low")), "close": _f(r.get("close")),
                         "timestamp": r.get("timestamp")})
    return rows


def _utc_dt(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc) if value.tzinfo else value.replace(tzinfo=timezone.utc)
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed.astimezone(timezone.utc) if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None


# --------------------------------------------------------------------------- mode-specific fill
def entry_fill_bar(mode: str, bar: dict, *, long: bool, entry_low, entry_high, entry_trigger,
                   suggested, is_first: bool, bps: float = DEFAULT_MAKER_TRADE_THROUGH_BPS):
    """(fill_price, order_type, at_open) for this bar under `mode`, else (None, 'none', False).
    Faithful mirror of paper_shadow_engine._entry_fill (incl. maker trade-through). `at_open` is
    True only when the fill price IS the bar open (fill happened at the very start of the candle) —
    the only case where a same-candle TP touch can be trusted to be AFTER entry."""
    hi, lo = bar["high"], bar["low"]
    op = bar["open"] if bar["open"] is not None else bar["close"]
    cl = bar["close"]
    if hi is None or lo is None:
        return None, "none", False
    m = (mode or "PULLBACK_LIMIT").upper()
    if m == "NO_CHASE_SKIP":
        return None, "none", False
    if m == "MOMENTUM_TAKER_NOW":
        px = op if is_first else cl
        return (float(px) if px is not None else None), "taker", bool(is_first)  # first-bar = at open
    if m == "BREAKOUT_CONTINUATION":
        trig = entry_trigger if entry_trigger is not None else (entry_high if long else entry_low)
        if trig is None:
            return None, "none", False
        if (long and hi >= trig) or (not long and lo <= trig):
            return float(trig), "taker", False                    # intrabar trigger cross, NOT at open
        return None, "none", False
    # limit modes
    if m == "STRUCTURAL_RETEST" and suggested is not None:
        z_lo = z_hi = float(suggested)
    else:
        if entry_low is None or entry_high is None:
            return None, "none", False
        z_lo, z_hi = min(entry_low, entry_high), max(entry_low, entry_high)
    if op is not None and z_lo <= op <= z_hi:
        return float(op), "maker", True                           # opened inside zone -> at open
    if long and lo <= z_hi * (1.0 - bps):                         # traded through the buy limit
        return float(z_hi), "maker", False                        # intrabar trade-through, NOT at open
    if (not long) and hi >= z_lo * (1.0 + bps):                   # traded through the sell limit
        return float(z_lo), "maker", False
    return None, "none", False                                    # only touched the edge -> miss


# --------------------------------------------------------------------------- walk
@dataclass
class WalkResult:
    entered: bool = False
    entry_price: float | None = None
    entry_order_type: str = "none"
    reached_tp1: bool = False
    reached_tp2: bool = False
    reached_tp3: bool = False
    hit_stop: bool = False
    expired: bool = False
    mfe_r: float = 0.0
    mae_r: float = 0.0
    same_candle_ambiguous: bool = False
    entry_at_open: bool = False
    bars_to_entry: int | None = None
    pre_entry_invalidation: bool = False
    entry_expired: bool = False
    maker_entry_posted: int = 0
    maker_entry_filled: int = 0
    maker_entry_missed: int = 0
    taker_fallback_used: int = 0


def walk(
    *,
    direction: str,
    entry_mode: str,
    entry_low: float | None,
    entry_high: float | None,
    entry_trigger: float | None,
    suggested: float | None,
    stop: float | None,
    tp1: float | None,
    tp2: float | None,
    tp3: float | None,
    candles: Any,
    timeout_bars: int | None = None,
    entry_expiry_bars: int | None = None,
    entry_expires_at: datetime | str | None = None,
    bar_minutes: int | None = None,
    maker_trade_through_bps: float = DEFAULT_MAKER_TRADE_THROUGH_BPS,
) -> WalkResult:
    """Conservative, lookahead-safe, MODE-SPECIFIC entry + Model-F-input walk.
    `candles` must already be time-filtered by the caller (>= decision instant).

    ``entry_expires_at`` is a pre-entry deadline only: it prevents a stale
    signal from filling on a later candle, but never truncates monitoring after
    a valid entry. A candle is eligible only when its close is at or before the
    deadline, avoiding an optimistic fill inside a partially elapsed candle.
    """
    res = WalkResult()
    long = str(direction or "long").lower() != "short"
    rows = _iter_ohlcv(candles)
    if not rows or stop is None:
        return res
    m = (entry_mode or "PULLBACK_LIMIT").upper()
    if m in LIMIT_MODES:
        res.maker_entry_posted = 1
    if m == "LIMIT_THEN_TAKER_TIMEOUT" and timeout_bars is None:
        timeout_bars = DEFAULT_MAKER_TIMEOUT_BARS
    expiry = _utc_dt(entry_expires_at)
    minutes = max(0, int(bar_minutes or 0))

    entry_px = None
    for idx, c in enumerate(rows):
        hi, lo = c["high"], c["low"]
        if hi is None or lo is None:
            continue
        if not res.entered:
            if expiry is not None:
                bar_start = _utc_dt(c.get("timestamp"))
                # A timestamp-less candle cannot establish that the proposed
                # entry was still valid. Fail closed only when a deadline was
                # explicitly requested; legacy callers keep their old behavior.
                if bar_start is None or bar_start + timedelta(minutes=minutes) > expiry:
                    if res.maker_entry_posted:
                        res.maker_entry_missed = 1
                    res.entry_expired = True
                    return res
            if entry_expiry_bars is not None and idx > int(entry_expiry_bars):
                # A confirmed setup whose retest did not arrive in its stated
                # validity window is a no-entry, not a fill at a later market.
                if res.maker_entry_posted:
                    res.maker_entry_missed = 1
                res.entry_expired = True
                return res
            fill, otype, at_open = entry_fill_bar(m, c, long=long, entry_low=entry_low, entry_high=entry_high,
                                                  entry_trigger=entry_trigger, suggested=suggested,
                                                  is_first=(idx == 0), bps=maker_trade_through_bps)
            if fill is None and m == "LIMIT_THEN_TAKER_TIMEOUT" and timeout_bars is not None and idx >= timeout_bars:
                op = c["open"] if c["open"] is not None else c["close"]
                if op is not None:
                    fill, otype, at_open = float(op), "taker", True   # taker fallback fills at bar open
                    res.taker_fallback_used = 1
            if fill is None:
                # pre-entry invalidation: stop breached before a fill
                if (long and lo <= stop) or (not long and hi >= stop):
                    if res.maker_entry_posted:
                        res.maker_entry_missed = 1
                    res.pre_entry_invalidation = True
                    return res
                continue
            entry_px = fill
            res.entered, res.entry_price, res.entry_order_type = True, fill, otype
            res.entry_at_open = bool(at_open)
            res.bars_to_entry = idx
            if otype == "maker":
                res.maker_entry_filled = 1
            # NO `continue`: fall through so stop/TP are evaluated on the ENTRY candle too.
        # in trade (entry candle included)
        risk = abs(entry_px - stop) or 1e-9
        stop_touched = (lo <= stop) if long else (hi >= stop)
        t1 = tp1 is not None and ((hi >= tp1) if long else (lo <= tp1))
        t2 = tp2 is not None and ((hi >= tp2) if long else (lo <= tp2))
        t3 = tp3 is not None and ((hi >= tp3) if long else (lo <= tp3))
        # CONSERVATIVE entry candle for a NON-open fill (maker trade-through / breakout trigger):
        # intrabar order of the fill vs the favorable extreme is unknown, so we NEVER credit a
        # same-candle TP or its MFE — we only honor the adverse side (stop-first). A TP touch on this
        # bar just flags ambiguity and the trade stays open for a later, unambiguous TP.
        if idx == res.bars_to_entry and not res.entry_at_open:
            res.mae_r = min(res.mae_r, -(((entry_px - lo) if long else (hi - entry_px)) / risk))
            if stop_touched:
                if t1 or t2 or t3:
                    res.same_candle_ambiguous = True
                res.hit_stop = True
                return res
            if t1 or t2 or t3:
                res.same_candle_ambiguous = True   # TP touched but not credited (ambiguous vs entry)
            continue
        fav = (hi - entry_px) if long else (entry_px - lo)
        adv = (entry_px - lo) if long else (hi - entry_px)
        res.mfe_r = max(res.mfe_r, fav / risk)
        res.mae_r = min(res.mae_r, -(adv / risk))
        if stop_touched and (t1 or t2 or t3):
            res.same_candle_ambiguous = True
            res.reached_tp1 = res.reached_tp1 or t1
            res.reached_tp2 = res.reached_tp2 or t2
            res.reached_tp3 = res.reached_tp3 or t3
            res.hit_stop = True
            return res
        if t1:
            res.reached_tp1 = True
        if t2:
            res.reached_tp2 = True
        if t3:
            res.reached_tp3 = True
        if stop_touched:
            res.hit_stop = True
            return res
        if res.reached_tp3:
            return res
    if res.entered:
        res.expired = True
    return res


# --------------------------------------------------------------------------- baselines
def no_protection_r(*, reached_tp1, reached_tp2, reached_tp3, hit_stop, R1, R2, R3) -> float:
    """TRUE no-protection: original stop held the whole time, base partial-TP model, no BE/lock/
    trailing. Partials book at each TP reached; any remainder exits at the ORIGINAL stop (-1R) if
    the stop was hit, else 0 (expired flat)."""
    r = 0.0
    remaining = 1.0
    if reached_tp1:
        r += PARTIALS[1] * R1
        remaining -= PARTIALS[1]
    if reached_tp2:
        r += PARTIALS[2] * R2
        remaining -= PARTIALS[2]
    if reached_tp3:
        r += PARTIALS[3] * R3
        remaining -= PARTIALS[3]
    if remaining > 1e-9 and hit_stop:
        r += remaining * (-1.0)
    return round(r, 4)


# --------------------------------------------------------------------------- protect + USD
@dataclass
class ProtectedResult:
    protection_model: str
    entered: bool
    entry_order_type: str = "none"
    skipped: bool = False
    skip_reason: str | None = None
    taker_fallback_used: int = 0
    net_r: float | None = None
    net_usd: float | None = None
    gross_r: float | None = None
    risk_usd: float | None = None
    fees_usd: float | None = None
    exit_price: float | None = None
    close_reason: str | None = None
    protection_armed: bool = False
    lock_armed: bool = False
    breakeven_exit: bool = False
    profit_lock_exit: bool = False
    tp3_runner: bool = False
    giveback: bool = False
    highest_tp_touched: int = 0
    same_candle_ambiguous: bool = False
    legacy_touch_r: float | None = None
    first_tp_close_r: float | None = None
    no_protection_r: float | None = None
    delta_vs_no_protection_r: float | None = None
    delta_vs_no_protection_usd: float | None = None
    delta_vs_legacy_touch_r: float | None = None
    delta_vs_legacy_touch_usd: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _exit_slices_for(highest_tp: int) -> list:
    slices, remaining = [], 1.0
    for i in range(1, highest_tp + 1):
        slices.append((PARTIALS[i], "maker"))
        remaining -= PARTIALS[i]
    if remaining > 1e-9:
        slices.append((round(remaining, 4), "taker"))
    return slices or [(1.0, "taker")]


def net_usd_from_r(
    *, r: float, entry: float, stop: float, direction: str, symbol: str, fee_profile: str,
    entry_order_type: str = "taker", highest_tp: int = 0, equity: float = EQUITY_USD,
    risk_pct: float = RISK_PCT, max_leverage: int = MAX_LEV,
) -> tuple[float, float, float, float]:
    """Realistic net USD for a paper trade closed at `r` R. Exit notional is derived from the
    IMPLIED exit price (entry +/- r*risk_per_unit), not the entry notional.
    Returns (net_usd, fees_usd, risk_usd, exit_price)."""
    long = str(direction).lower() != "short"
    sz = size_position(equity_usdt=equity, entry_price=entry, stop_price=stop,
                       direction=direction, risk_pct=risk_pct, max_leverage=max_leverage)
    risk_usd = float(sz.actual_risk_usdt)
    qty = float(sz.qty)
    entry_notional = float(sz.notional_usdt)
    risk_per_unit = abs(entry - stop)
    exit_price = (entry + r * risk_per_unit) if long else (entry - r * risk_per_unit)
    exit_notional = qty * exit_price
    gross_usd = r * risk_usd
    cost = trade_costs(notional_usdt=entry_notional, exit_notional_usdt=exit_notional, symbol=symbol,
                       fee_profile=fee_profile, entry_order_type=entry_order_type,
                       exit_order_type="taker", exit_slices=_exit_slices_for(highest_tp))
    return (round(gross_usd - cost.total_cost_usdt, 4), round(cost.total_cost_usdt, 4),
            round(risk_usd, 4), round(exit_price, 8))


def protect(
    *, direction: str, entry: float | None, stop: float | None, tp1, tp2, tp3,
    walk_result: WalkResult, protection_model: str = DEFAULT_PROTECTION_MODEL,
    symbol: str = "", fee_profile: str = "bybit_non_vip_usdt_perp", entry_mode: str | None = None,
    equity: float = EQUITY_USD, risk_pct: float = RISK_PCT,
) -> ProtectedResult:
    if str(entry_mode or "").upper() == "NO_CHASE_SKIP":
        return ProtectedResult(protection_model=protection_model, entered=False, skipped=True,
                               skip_reason="no_chase_skip")
    if not walk_result.entered or entry is None or stop is None:
        return ProtectedResult(protection_model=protection_model, entered=False, skipped=True,
                               skip_reason="no_entry")
    entry = float(walk_result.entry_price if walk_result.entry_price is not None else entry)
    core = ("early_mfe_protection_v1"
            if protection_model in ("early_mfe_protection_v1",
                                    "structural_stop_with_profit_protection_v1")
            else protection_model)
    kw = dict(direction=direction, entry=entry, stop=stop, tp1=tp1, tp2=tp2, tp3=tp3,
              reached_tp1=walk_result.reached_tp1, reached_tp2=walk_result.reached_tp2,
              reached_tp3=walk_result.reached_tp3, hit_stop=walk_result.hit_stop,
              expired=walk_result.expired, entered=True, mfe_r=walk_result.mfe_r,
              same_candle_ambiguous=walk_result.same_candle_ambiguous)
    rec = compute_paper_execution(risk_model=core, **kw)
    legacy = compute_paper_execution(risk_model="legacy_touch", **kw)
    first_tp = compute_paper_execution(risk_model="first_tp_close", **kw)
    r = rec.get("paper_execution_r")
    if r is None:
        return ProtectedResult(protection_model=protection_model, entered=True, skipped=False,
                               skip_reason="unresolved", entry_order_type=walk_result.entry_order_type,
                               taker_fallback_used=walk_result.taker_fallback_used)
    R1 = r_multiple(entry, stop, tp1, direction) or 0.0
    R2 = r_multiple(entry, stop, tp2, direction) or 0.0
    R3 = r_multiple(entry, stop, tp3, direction) or 0.0
    nop = no_protection_r(reached_tp1=walk_result.reached_tp1, reached_tp2=walk_result.reached_tp2,
                          reached_tp3=walk_result.reached_tp3, hit_stop=walk_result.hit_stop,
                          R1=R1, R2=R2, R3=R3)
    ht = int(rec.get("highest_tp_touched") or 0)
    net_usd, fees_usd, risk_usd, exit_price = net_usd_from_r(
        r=r, entry=entry, stop=stop, direction=direction, symbol=symbol, fee_profile=fee_profile,
        entry_order_type=walk_result.entry_order_type or "taker", highest_tp=ht,
        equity=equity, risk_pct=risk_pct)
    legacy_r = legacy.get("paper_execution_r")
    d_nop_r = round(r - nop, 4)
    d_leg_r = round(r - legacy_r, 4) if legacy_r is not None else None
    cr = str(rec.get("close_reason") or "")
    return ProtectedResult(
        protection_model=protection_model, entered=True, skipped=False,
        entry_order_type=walk_result.entry_order_type, taker_fallback_used=walk_result.taker_fallback_used,
        net_r=round(r, 4), net_usd=net_usd, gross_r=round(r, 4), risk_usd=risk_usd, fees_usd=fees_usd,
        exit_price=exit_price, close_reason=cr,
        protection_armed=bool(rec.get("protection_armed")), lock_armed=bool(rec.get("lock_armed")),
        breakeven_exit=(cr == "breakeven_stop"), profit_lock_exit=(cr == "profit_lock_stop"),
        tp3_runner=(cr == "tp3_runner"), giveback=bool(rec.get("giveback")),
        highest_tp_touched=ht, same_candle_ambiguous=bool(rec.get("same_candle_ambiguous")),
        legacy_touch_r=(round(legacy_r, 4) if legacy_r is not None else None),
        first_tp_close_r=(round(first_tp.get("paper_execution_r"), 4)
                          if first_tp.get("paper_execution_r") is not None else None),
        no_protection_r=nop,
        delta_vs_no_protection_r=d_nop_r,
        delta_vs_no_protection_usd=(round(d_nop_r * risk_usd, 4) if risk_usd is not None else None),
        delta_vs_legacy_touch_r=d_leg_r,
        delta_vs_legacy_touch_usd=(round(d_leg_r * risk_usd, 4) if (d_leg_r is not None and risk_usd) else None),
    )


def simulate_from_geometry(
    *, direction: str, entry_low, entry_high, entry_trigger, stop, tp1, tp2, tp3, candles,
    suggested=None, entry_mode: str | None = None, protection_model: str = DEFAULT_PROTECTION_MODEL,
    symbol: str = "", fee_profile: str = "bybit_non_vip_usdt_perp", timeout_bars: int | None = None,
    maker_trade_through_bps: float = DEFAULT_MAKER_TRADE_THROUGH_BPS,
    equity: float = EQUITY_USD, risk_pct: float = RISK_PCT,
) -> ProtectedResult:
    """Full pipeline: MODE-SPECIFIC walk on real candles -> Model-F protect -> net USD.
    NO_CHASE_SKIP short-circuits to a skipped (avoided-trade) result with no PnL."""
    if str(entry_mode or "").upper() == "NO_CHASE_SKIP":
        return ProtectedResult(protection_model=protection_model, entered=False, skipped=True,
                               skip_reason="no_chase_skip")
    wr = walk(direction=direction, entry_mode=entry_mode or "PULLBACK_LIMIT", entry_low=entry_low,
              entry_high=entry_high, entry_trigger=entry_trigger, suggested=suggested, stop=stop,
              tp1=tp1, tp2=tp2, tp3=tp3, candles=candles, timeout_bars=timeout_bars,
              maker_trade_through_bps=maker_trade_through_bps)
    if not wr.entered:
        res = ProtectedResult(protection_model=protection_model, entered=False, skipped=True,
                              skip_reason="pre_entry_invalidation" if wr.pre_entry_invalidation else "no_fill",
                              entry_order_type=wr.entry_order_type)
        return res
    return protect(direction=direction, entry=wr.entry_price, stop=stop, tp1=tp1, tp2=tp2, tp3=tp3,
                   walk_result=wr, protection_model=protection_model, symbol=symbol,
                   fee_profile=fee_profile, entry_mode=entry_mode, equity=equity, risk_pct=risk_pct)


__all__ = [
    "PROTECTION_MODELS", "DEFAULT_PROTECTION_MODEL", "EQUITY_USD", "RISK_PCT", "LIMIT_MODES",
    "ARM_BE_AT_R", "LOCK_AT_R", "LOCK_LEVEL_R", "DEFAULT_MAKER_TRADE_THROUGH_BPS",
    "DEFAULT_MAKER_TIMEOUT_BARS", "WalkResult", "ProtectedResult", "entry_fill_bar", "walk",
    "protect", "net_usd_from_r", "no_protection_r", "simulate_from_geometry",
]
