from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

import pandas as pd

from src.execution.shadow_strategy_common import simulate_confirmed_close_entry


@dataclass
class SimulationResult:
    status: str
    exit_at: str | None
    close_reason: str | None
    gross_pnl_usd: float | None
    net_pnl_usd: float | None
    fees_usd: float
    slippage_usd: float
    funding_usd: float
    net_r: float | None
    mfe_r: float | None
    mae_r: float | None
    highest_tp: int
    bars_held: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _bars(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    if "timestamp" not in out.columns and "bar_open_at" in out.columns:
        out["timestamp"] = out["bar_open_at"]
    return out


def simulate(*, direction: str, entry: float, stop: float, targets_r: list[float],
             bars: pd.DataFrame, risk_usd: float, taker_fee_rate: float,
             maker_fee_rate: float, slippage_bps: float, model_f: dict[str, Any] | None = None,
             force_exit_at_end: bool = False) -> SimulationResult:
    risk = abs(float(entry) - float(stop))
    if risk <= 0:
        return SimulationResult("skipped", None, "invalid_geometry", None, None, 0.0, 0.0, 0.0, None, None, None, 0, 0)
    long = str(direction).lower() != "short"
    values = list(targets_r or [1.3, 2.3, 3.6])
    while len(values) < 3:
        values.append(values[-1] + 1.0)
    targets = [float(entry) + r * risk if long else float(entry) - r * risk for r in values[:3]]
    result = simulate_confirmed_close_entry(
        direction=direction,
        entry=float(entry),
        stop=float(stop),
        tp1=targets[0],
        tp2=targets[1],
        tp3=targets[2],
        future_candles=_bars(bars),
        symbol="",
        fee_profile="bybit_non_vip_usdt_perp",
        entry_at=None,
        bar_minutes=15,
        force_close=force_exit_at_end,
        equity_usd=float(risk_usd) / 0.005 if risk_usd else 5000.0,
        risk_pct=0.005,
    )
    data = result.to_dict()
    return SimulationResult(
        status=str(data.get("status") or "open"),
        exit_at=data.get("exit_ts"),
        close_reason=data.get("close_reason"),
        gross_pnl_usd=data.get("gross_pnl_usd"),
        net_pnl_usd=data.get("net_pnl_usd"),
        fees_usd=float(data.get("fees_usd") or 0.0),
        slippage_usd=float(data.get("slippage_usd") or 0.0),
        funding_usd=float(data.get("funding_usd") or 0.0),
        net_r=data.get("net_r"),
        mfe_r=data.get("mfe_r"),
        mae_r=data.get("mae_r"),
        highest_tp=int(data.get("highest_tp_touched") or 0),
        bars_held=int(data.get("bars_held") or 0),
    )

