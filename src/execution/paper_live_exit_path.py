"""Point-in-time Paper exit simulation that mirrors the live exit contract.

The legacy Paper ledger reduced an entire post-entry path to aggregate TP/stop
touch flags. That cannot observe a breakeven/profit-lock stop touched before a
later TP3, and it credited the whole position at TP3 even though live scales
out in three legs. This module walks closed execution candles in order and
uses the same 0.6R/1.0R Model-F thresholds as live.

It is Paper/accounting only. It never writes orders or changes live controls.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


VERSION = "live_exit_parity_v3_incremental"
TP_FRACTIONS = (0.33, 0.33, 0.34)


def _number(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _rows(candles: Any) -> list[dict[str, Any]]:
    if candles is None:
        return []
    if hasattr(candles, "iterrows"):
        return [dict(row) for _, row in candles.iterrows()]
    return [dict(row) for row in candles]


def _timestamp(row: dict[str, Any]) -> str | None:
    value = row.get("timestamp")
    if value in (None, ""):
        return None
    try:
        return value.isoformat()
    except AttributeError:
        return str(value)


def _parse_timestamp(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _bool_state(state: dict[str, Any], name: str, fallback: bool = False) -> bool:
    value = state.get(name)
    return fallback if value is None else bool(value)


def simulate_live_exit_path(
    *,
    direction: str,
    entry: float,
    stop: float,
    tp1: float | None,
    tp2: float | None,
    tp3: float | None,
    candles: Any,
    initial_state: dict[str, Any] | None = None,
    path_start_at: str | None = None,
    max_gap_seconds: float = 180.0,
    arm_breakeven_at_r: float = 0.6,
    lock_profit_at_r: float = 1.0,
    lock_level_r: float = 0.5,
) -> dict[str, Any]:
    """Walk closed candles using the live three-leg + Model-F contract.

    Stop/target ambiguity inside one candle is resolved stop-first. A newly
    reached protection threshold becomes active on the next candle, avoiding
    lookahead about the intrabar order of the favorable and adverse extremes.
    """
    side = str(direction or "long").lower()
    if side not in {"long", "short"}:
        raise ValueError("unsupported direction")
    entry, stop = float(entry), float(stop)
    risk = (entry - stop) if side == "long" else (stop - entry)
    if risk <= 0:
        raise ValueError("invalid directional geometry")

    targets = [_number(tp1), _number(tp2), _number(tp3)]
    target_r = [
        (((level - entry) if side == "long" else (entry - level)) / risk)
        if level is not None else None
        for level in targets
    ]
    state = dict(initial_state or {})
    highest = int(_number(state.get("highest_tp_touched")) or 0)
    filled = [
        _bool_state(state, f"path_tp{index + 1}_filled", highest >= index + 1)
        for index in range(3)
    ]
    realized_r = _number(state.get("path_realized_r"))
    if realized_r is None:
        realized_r = _number(state.get("realized_partial_r")) or 0.0
    remaining = _number(state.get("path_remaining_fraction"))
    if remaining is None:
        remaining = max(
            0.0,
            1.0 - sum(TP_FRACTIONS[index] for index, hit in enumerate(filled) if hit),
        )
    remaining = min(1.0, max(0.0, remaining))
    active_stop_r = _number(state.get("stop_current_r"))
    active_stop_r = -1.0 if active_stop_r is None else active_stop_r
    max_mfe_r = _number(state.get("path_max_mfe_r"))
    if max_mfe_r is None:
        max_mfe_r = _number(state.get("mfe_r")) or 0.0
    last_candle_at = str(state.get("path_last_candle_at") or "") or None
    protection_stage = (
        "PROFIT_LOCK" if active_stop_r > 0
        else "BREAKEVEN" if active_stop_r == 0
        else "ORIGINAL_STOP"
    )

    def result(
        *,
        terminal: bool,
        total_r: float | None = None,
        outcome: str = "open",
        close_reason: str | None = None,
        close_event: str | None = None,
        exit_at: str | None = None,
        exit_at_source: str | None = None,
        ambiguous: bool = False,
        data_quality: str = "complete",
        gap_seconds: float | None = None,
    ) -> dict[str, Any]:
        return {
            "version": VERSION,
            "terminal": terminal,
            "paper_execution_r": None if total_r is None else round(total_r, 4),
            "paper_execution_outcome": outcome,
            "close_reason": close_reason,
            "close_event": close_event,
            "exit_at": exit_at,
            "exit_at_source": exit_at_source,
            "highest_tp_touched": sum(filled),
            "stop_current_r": active_stop_r,
            "protection_stage": protection_stage,
            "protection_armed": active_stop_r >= 0,
            "lock_armed": active_stop_r > 0,
            "mfe_r": round(max_mfe_r, 6),
            "realized_partial_r": round(realized_r, 6),
            "remaining_fraction": round(remaining, 6),
            "same_candle_ambiguous": ambiguous,
            "path_realized_r": round(realized_r, 6),
            "path_remaining_fraction": round(remaining, 6),
            "path_last_candle_at": last_candle_at,
            "path_tp1_filled": filled[0],
            "path_tp2_filled": filled[1],
            "path_tp3_filled": filled[2],
            "path_max_mfe_r": round(max_mfe_r, 6),
            "path_data_quality": data_quality,
            "path_gap_seconds": gap_seconds,
        }

    previous_at = _parse_timestamp(last_candle_at or path_start_at)
    rows = _rows(candles)
    if last_candle_at:
        persisted_at = _parse_timestamp(last_candle_at)
        if persisted_at is not None:
            rows = [
                row for row in rows
                if (_parse_timestamp(_timestamp(row)) is None
                    or _parse_timestamp(_timestamp(row)) > persisted_at)
            ]

    for row in rows:
        high, low = _number(row.get("high")), _number(row.get("low"))
        if high is None or low is None:
            continue
        at = _timestamp(row)
        candle_at = _parse_timestamp(at)
        if (previous_at is not None and candle_at is not None
                and (candle_at - previous_at).total_seconds() > max_gap_seconds):
            gap_seconds = (candle_at - previous_at).total_seconds()
            return result(
                terminal=False,
                data_quality="gap",
                gap_seconds=round(gap_seconds, 3),
            )
        if at:
            last_candle_at = at
        if candle_at is not None:
            previous_at = candle_at
        stop_price = entry + active_stop_r * risk if side == "long" else entry - active_stop_r * risk
        stop_touched = low <= stop_price if side == "long" else high >= stop_price
        newly_hit = [
            bool(not filled[index] and level is not None and (
                high >= level if side == "long" else low <= level
            ))
            for index, level in enumerate(targets)
        ]

        # Native stop and close-limit target order is unknowable from OHLC.
        # Stop-first is the conservative, reproducible assumption.
        if stop_touched:
            total_r = realized_r + remaining * active_stop_r
            realized_r = total_r
            remaining = 0.0
            outcome = "win" if total_r > 0 else "breakeven" if abs(total_r) < 1e-12 else "loss"
            return result(
                terminal=True,
                total_r=total_r,
                outcome=outcome,
                close_reason=(
                    "original_stop" if active_stop_r < 0
                    else "breakeven_stop" if active_stop_r == 0
                    else "profit_lock_stop"
                ),
                close_event="stop" if active_stop_r < 0 else "moved_stop",
                exit_at=at,
                exit_at_source="closed_1m_path_stop_first",
                ambiguous=bool(any(newly_hit)),
            )

        for index, hit in enumerate(newly_hit):
            if not hit or target_r[index] is None:
                continue
            fraction = min(TP_FRACTIONS[index], remaining)
            realized_r += fraction * float(target_r[index])
            remaining = max(0.0, remaining - fraction)
            filled[index] = True

        if remaining <= 1e-9 or filled[2]:
            # TP3 closes whatever remains after exchange-volume rounding.
            if remaining > 1e-9 and target_r[2] is not None:
                realized_r += remaining * float(target_r[2])
                remaining = 0.0
            return result(
                terminal=True,
                total_r=realized_r,
                outcome="win",
                close_reason="three_leg_tp3",
                close_event="tp3",
                exit_at=at,
                exit_at_source="closed_1m_path_tp3",
            )

        favorable = (high - entry) if side == "long" else (entry - low)
        max_mfe_r = max(max_mfe_r, favorable / risk)
        if max_mfe_r >= lock_profit_at_r:
            active_stop_r = float(lock_level_r)
            protection_stage = "PROFIT_LOCK"
        elif max_mfe_r >= arm_breakeven_at_r:
            active_stop_r = 0.0
            protection_stage = "BREAKEVEN"

    return result(terminal=False)


__all__ = ["VERSION", "TP_FRACTIONS", "simulate_live_exit_path"]
