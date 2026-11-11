"""StocksMarketRegimeAgent — classify the broad market regime.

Inputs: cached daily bars for SPY, QQQ, IWM, DIA (+ ^VIX if available).
Output: regime label and per-index trend / breadth payload that downstream
agents and scoring can consume.

Regime labels (stock-specific — distinct from crypto regimes):
  bullish, risk_on, risk_off, chop, transition, high_volatility, low_volatility
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import pandas as pd

from src.indicators.technicals import ema, pct_return
from src.stocks.agents.base import StocksBaseAgent
from src.stocks.data_collectors.stock_ohlcv_collector import StockOHLCVCollector


@dataclass
class IndexSnapshot:
    symbol: str
    trend: str             # uptrend / downtrend / range
    return_5d: float | None
    return_20d: float | None
    above_ema20: bool
    above_ema50: bool
    last_close: float | None


@dataclass
class StocksRegime:
    label: str
    bias: str              # long / short / neutral
    risk_on: bool
    high_volatility: bool
    breadth_above_ema20: float | None
    breadth_above_ema50: float | None
    vix_level: float | None
    explanation: str
    indices: list[IndexSnapshot]


class StocksMarketRegimeAgent(StocksBaseAgent):
    name = "stocks_market_regime"

    # VIX thresholds (rough but reasonable defaults).
    VIX_HIGH = 25.0
    VIX_LOW = 14.0

    def run(self) -> dict[str, Any]:
        snapshots: list[IndexSnapshot] = []
        loader = StockOHLCVCollector(self.config, self.stocks_config)
        for symbol in self.stocks_config.indices:
            frame = loader.load_cached(symbol, "1d")
            if frame is None or len(frame) < 60:
                continue
            snapshots.append(self._snapshot(symbol, frame))

        vix_level: float | None = None
        vol_symbol = self.stocks_config.volatility_index
        if vol_symbol:
            vix_frame = loader.load_cached(vol_symbol, "1d")
            if vix_frame is not None and not vix_frame.empty:
                vix_level = float(vix_frame["close"].iloc[-1])

        breadth20 = self._fraction_above_ema(snapshots, "above_ema20")
        breadth50 = self._fraction_above_ema(snapshots, "above_ema50")
        regime = self._classify(snapshots, vix_level, breadth20, breadth50)

        payload = {
            "regime": asdict(regime),
            "indices": [asdict(s) for s in snapshots],
        }
        self.save_output(payload)
        return payload

    def _snapshot(self, symbol: str, frame: pd.DataFrame) -> IndexSnapshot:
        close = frame["close"]
        ema20 = ema(close, 20).iloc[-1]
        ema50 = ema(close, 50).iloc[-1]
        last = float(close.iloc[-1])
        r5 = pct_return(frame, 5)
        r20 = pct_return(frame, 20)
        # Trend by EMA stack + slope direction.
        ema20_now = float(ema20)
        ema20_prev = float(ema(close, 20).iloc[-5]) if len(frame) >= 6 else ema20_now
        if last > ema20_now > ema20_prev and last > ema50:
            trend = "uptrend"
        elif last < ema20_now < ema20_prev and last < ema50:
            trend = "downtrend"
        else:
            trend = "range"
        return IndexSnapshot(
            symbol=symbol,
            trend=trend,
            return_5d=r5,
            return_20d=r20,
            above_ema20=bool(last > ema20_now),
            above_ema50=bool(last > float(ema50)),
            last_close=last,
        )

    @staticmethod
    def _fraction_above_ema(snapshots: list[IndexSnapshot], field: str) -> float | None:
        if not snapshots:
            return None
        hits = sum(1 for s in snapshots if getattr(s, field))
        return round(hits / len(snapshots), 3)

    def _classify(
        self,
        snapshots: list[IndexSnapshot],
        vix_level: float | None,
        breadth20: float | None,
        breadth50: float | None,
    ) -> StocksRegime:
        if not snapshots:
            return StocksRegime(
                label="unknown",
                bias="neutral",
                risk_on=False,
                high_volatility=False,
                breadth_above_ema20=None,
                breadth_above_ema50=None,
                vix_level=vix_level,
                explanation="No index data available.",
                indices=[],
            )

        uptrends = sum(1 for s in snapshots if s.trend == "uptrend")
        downtrends = sum(1 for s in snapshots if s.trend == "downtrend")
        total = len(snapshots)
        breadth = breadth20 if breadth20 is not None else 0.0
        longer_breadth = breadth50 if breadth50 is not None else 0.0

        high_vol = vix_level is not None and vix_level >= self.VIX_HIGH
        low_vol = vix_level is not None and vix_level <= self.VIX_LOW

        if uptrends == total and breadth >= 0.75:
            label = "bullish"
            bias = "long"
            risk_on = True
        elif uptrends >= total - 1 and breadth >= 0.5 and not high_vol:
            label = "risk_on"
            bias = "long"
            risk_on = True
        # A shallow pullback is not a risk-off market.  The previous rule treated
        # one weak EMA20 breadth snapshot as risk-off even while every index was
        # above its EMA50 and none was in a downtrend.  That mislabeled ordinary
        # intraday consolidation as a bearish regime and pushed the pipeline into
        # low-quality short ideas.  Require either broad downtrends or weakness
        # across both the short and medium trend horizons before declaring risk-off.
        elif downtrends >= total - 1 or (breadth <= 0.25 and longer_breadth <= 0.50):
            label = "risk_off"
            bias = "short"
            risk_on = False
        elif high_vol:
            label = "high_volatility"
            bias = "neutral"
            risk_on = False
        elif low_vol and uptrends >= 2:
            label = "low_volatility"
            bias = "long"
            risk_on = True
        elif (uptrends >= 1 and downtrends >= 1) or (
            uptrends >= 1 and downtrends == 0 and longer_breadth >= 0.75
        ):
            label = "transition"
            bias = "neutral"
            risk_on = False
        else:
            label = "chop"
            bias = "neutral"
            risk_on = False

        bits = [
            f"{uptrends}/{total} indices trending up",
            f"breadth_above_ema20={breadth20}",
            f"breadth_above_ema50={breadth50}",
        ]
        if vix_level is not None:
            bits.append(f"VIX={vix_level:.2f}")
        explanation = "; ".join(bits)

        return StocksRegime(
            label=label,
            bias=bias,
            risk_on=risk_on,
            high_volatility=high_vol,
            breadth_above_ema20=breadth20,
            breadth_above_ema50=breadth50,
            vix_level=vix_level,
            explanation=explanation,
            indices=snapshots,
        )
