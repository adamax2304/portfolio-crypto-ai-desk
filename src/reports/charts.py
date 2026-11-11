from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import ProjectConfig
from src.indicators.technicals import enrich_ohlcv
from src.models import TradeIdea
from src.utils.symbols import symbol_to_filename
from src.utils.time import utc_now


class ChartBuilder:
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.chart_dir = config.reports_dir / "charts"
        self.chart_dir.mkdir(parents=True, exist_ok=True)

    def generate_for_ideas(
        self,
        ideas: list[TradeIdea],
        market_data: dict[str, dict[str, pd.DataFrame]],
        limit: int = 5,
    ) -> dict[str, str]:
        paths: dict[str, str] = {}
        selected = [
            idea for idea in ideas
            if idea.direction in {"long", "short", "watchlist only"}
        ][:limit]
        for idea in selected:
            frame = market_data.get(idea.symbol, {}).get("1h")
            if frame is None or frame.empty:
                continue
            try:
                paths[idea.symbol] = self._plot_idea(idea, frame)
            except Exception:
                continue
        return paths

    def _plot_idea(self, idea: TradeIdea, frame: pd.DataFrame) -> str:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        setup = idea.raw.get("setup", {})
        chart_frame = enrich_ohlcv(frame).tail(120).copy()
        filename = (
            f"{utc_now().strftime('%Y%m%d_%H%M')}_"
            f"{symbol_to_filename(idea.symbol)}.png"
        )
        output_path = self.chart_dir / filename

        fig, (ax_price, ax_volume) = plt.subplots(
            2,
            1,
            figsize=(12, 7),
            sharex=True,
            gridspec_kw={"height_ratios": [4, 1]},
        )
        ax_price.plot(chart_frame["timestamp"], chart_frame["close"], label="Close", color="#111827", linewidth=1.4)
        ax_price.plot(chart_frame["timestamp"], chart_frame["ema20"], label="EMA20", color="#2563eb", linewidth=1)
        ax_price.plot(chart_frame["timestamp"], chart_frame["ema50"], label="EMA50", color="#9333ea", linewidth=1)

        self._hline(ax_price, setup.get("entry_low"), "Entry low", "#16a34a")
        self._hline(ax_price, setup.get("entry_high"), "Entry high", "#22c55e")
        self._hline(ax_price, setup.get("invalidation"), "Invalidation", "#dc2626")
        self._hline(ax_price, setup.get("tp1"), "TP1", "#f59e0b")
        self._hline(ax_price, setup.get("tp2"), "TP2", "#d97706")
        self._hline(ax_price, setup.get("tp3"), "TP3", "#b45309")

        ax_price.set_title(f"{idea.symbol} {idea.direction.upper()} | Score {idea.score}/100")
        ax_price.grid(alpha=0.2)
        ax_price.legend(loc="upper left", fontsize=8)
        ax_volume.bar(
            chart_frame["timestamp"],
            chart_frame["volume"],
            color="#9ca3af",
            width=0.02,
        )
        ax_volume.set_ylabel("Volume")
        ax_volume.grid(alpha=0.15)
        fig.autofmt_xdate()
        fig.tight_layout()
        fig.savefig(output_path, dpi=140)
        plt.close(fig)
        return f"../charts/{filename}"

    @staticmethod
    def _hline(ax, value: object, label: str, color: str) -> None:
        if value is None:
            return
        try:
            numeric = float(value)
        except Exception:
            return
        ax.axhline(numeric, linestyle="--", linewidth=0.9, color=color, alpha=0.85, label=label)
