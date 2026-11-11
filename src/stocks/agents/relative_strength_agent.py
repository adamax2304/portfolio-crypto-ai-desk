"""StockRelativeStrengthAgent — per-symbol RS vs SPY, QQQ, and sector ETF.

For each symbol in the analysis universe, compute 5d/20d returns and
relative-strength differentials against the indices and the symbol's
configured sector ETF. Classify as leader / follower / laggard / weak.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from src.indicators.technicals import pct_return
from src.stocks.agents.base import StocksBaseAgent
from src.stocks.data_collectors.stock_ohlcv_collector import StockOHLCVCollector


@dataclass
class RSSnapshot:
    symbol: str
    sector: str
    sector_etf: str
    return_5d: float | None
    return_20d: float | None
    rs_vs_spy_20d: float | None
    rs_vs_qqq_20d: float | None
    rs_vs_sector_20d: float | None
    classification: str  # leader / follower / laggard / weak / unknown


class StockRelativeStrengthAgent(StocksBaseAgent):
    name = "stock_relative_strength"
    PRIMARY_BENCHMARKS = ("SPY", "QQQ")

    def run(self, symbols: list[str] | None = None) -> dict[str, Any]:
        symbols = symbols or list(self.stocks_config.default_symbols)
        loader = StockOHLCVCollector(self.config, self.stocks_config)

        bench_r20: dict[str, float | None] = {}
        for b in self.PRIMARY_BENCHMARKS:
            f = loader.load_cached(b, "1d")
            bench_r20[b] = pct_return(f, 20) if f is not None else None

        results: list[RSSnapshot] = []
        for symbol in symbols:
            frame = loader.load_cached(symbol, "1d")
            if frame is None or len(frame) < 30:
                continue
            r5 = pct_return(frame, 5)
            r20 = pct_return(frame, 20)
            sector = self.stocks_config.sector_for(symbol)
            sector_etf = self.stocks_config.sector_etf_for(symbol)
            sector_r20 = None
            if sector_etf:
                sf = loader.load_cached(sector_etf, "1d")
                sector_r20 = pct_return(sf, 20) if sf is not None else None

            rs_spy = _diff(r20, bench_r20.get("SPY"))
            rs_qqq = _diff(r20, bench_r20.get("QQQ"))
            rs_sector = _diff(r20, sector_r20)
            classification = self._classify(rs_spy, rs_qqq, rs_sector)

            results.append(
                RSSnapshot(
                    symbol=symbol,
                    sector=sector,
                    sector_etf=sector_etf,
                    return_5d=r5,
                    return_20d=r20,
                    rs_vs_spy_20d=rs_spy,
                    rs_vs_qqq_20d=rs_qqq,
                    rs_vs_sector_20d=rs_sector,
                    classification=classification,
                )
            )

        results.sort(key=lambda r: (r.rs_vs_spy_20d or -999), reverse=True)
        payload = {
            "benchmarks_return_20d": bench_r20,
            "rows": [asdict(r) for r in results],
            "leaders": [r.symbol for r in results if r.classification == "leader"][:10],
            "laggards": [r.symbol for r in results if r.classification == "laggard"][:10],
        }
        self.save_output(payload)
        return payload

    @staticmethod
    def _classify(
        rs_spy: float | None,
        rs_qqq: float | None,
        rs_sector: float | None,
    ) -> str:
        anchors = [v for v in (rs_spy, rs_qqq) if v is not None]
        if not anchors:
            return "unknown"
        index_avg = sum(anchors) / len(anchors)
        # Sector RS is informational; we don't require it for classification.
        if index_avg >= 5.0:
            return "leader"
        if index_avg >= 1.5:
            return "follower"
        if index_avg <= -5.0:
            return "weak"
        return "laggard"


def _diff(a: float | None, b: float | None) -> float | None:
    if a is None or b is None:
        return None
    return round(a - b, 3)
