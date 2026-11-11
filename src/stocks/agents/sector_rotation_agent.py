"""SectorRotationAgent — rank sector ETFs by momentum / relative strength.

Inputs: cached daily bars for each sector ETF (XLK, SMH, XLF, ...) and
the benchmark SPY for RS.
Output: per-sector momentum and a ranked strongest/weakest list, plus a
status label (strong / mixed / weak) per sector.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import pandas as pd

from src.indicators.technicals import ema, pct_return
from src.stocks.agents.base import StocksBaseAgent
from src.stocks.data_collectors.stock_ohlcv_collector import StockOHLCVCollector


@dataclass
class SectorSnapshot:
    sector: str            # e.g. 'technology'
    etf: str               # e.g. 'XLK'
    return_5d: float | None
    return_20d: float | None
    rs_vs_spy_20d: float | None
    above_ema50: bool
    status: str            # strong / mixed / weak


class SectorRotationAgent(StocksBaseAgent):
    name = "sector_rotation"
    BENCHMARK = "SPY"

    def run(self) -> dict[str, Any]:
        loader = StockOHLCVCollector(self.config, self.stocks_config)
        bench_frame = loader.load_cached(self.BENCHMARK, "1d")
        bench_r20 = pct_return(bench_frame, 20) if bench_frame is not None else None

        snapshots: list[SectorSnapshot] = []
        for sector, etf in self.stocks_config.sector_etfs.items():
            frame = loader.load_cached(etf, "1d")
            if frame is None or len(frame) < 50:
                continue
            snapshots.append(self._snapshot(sector, etf, frame, bench_r20))

        snapshots.sort(key=lambda s: (s.rs_vs_spy_20d or -999), reverse=True)
        strongest = snapshots[:3]
        weakest = snapshots[-3:][::-1]

        payload = {
            "benchmark": self.BENCHMARK,
            "benchmark_return_20d": bench_r20,
            "sectors": [asdict(s) for s in snapshots],
            "strongest": [asdict(s) for s in strongest],
            "weakest": [asdict(s) for s in weakest],
        }
        self.save_output(payload)
        return payload

    def _snapshot(
        self,
        sector: str,
        etf: str,
        frame: pd.DataFrame,
        bench_r20: float | None,
    ) -> SectorSnapshot:
        r5 = pct_return(frame, 5)
        r20 = pct_return(frame, 20)
        rs = (r20 - bench_r20) if (r20 is not None and bench_r20 is not None) else None
        ema50_last = float(ema(frame["close"], 50).iloc[-1])
        last_close = float(frame["close"].iloc[-1])
        above50 = last_close > ema50_last

        if rs is not None:
            if rs >= 3.0 and above50:
                status = "strong"
            elif rs <= -3.0 and not above50:
                status = "weak"
            else:
                status = "mixed"
        else:
            status = "mixed"

        return SectorSnapshot(
            sector=sector,
            etf=etf,
            return_5d=r5,
            return_20d=r20,
            rs_vs_spy_20d=rs,
            above_ema50=above50,
            status=status,
        )
