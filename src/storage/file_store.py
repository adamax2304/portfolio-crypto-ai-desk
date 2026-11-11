from __future__ import annotations

import json
import os
import uuid
from pathlib import Path
from typing import Any

import pandas as pd

from src.config import ProjectConfig
from src.utils.symbols import filename_to_symbol, symbol_to_filename


class FileStore:
    def __init__(self, config: ProjectConfig):
        self.config = config

    def ensure_directories(self) -> None:
        directories = [
            self.config.raw_dir / "ohlcv",
            self.config.raw_dir / "funding",
            self.config.raw_dir / "open_interest",
            self.config.raw_dir / "news",
            self.config.raw_dir / "events",
            self.config.raw_dir / "social",
            self.config.processed_dir / "market_summary",
            self.config.processed_dir / "candidates",
            self.config.processed_dir / "agent_outputs",
            self.config.reports_dir / "daily",
            self.config.reports_dir / "intraday",
            self.config.reports_dir / "reviews",
            self.config.reports_dir / "charts",
            self.config.db_path.parent,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def ohlcv_path(self, exchange: str, symbol: str, timeframe: str) -> Path:
        return (
            self.config.raw_dir
            / "ohlcv"
            / exchange
            / timeframe
            / f"{symbol_to_filename(symbol)}.csv"
        )

    def save_ohlcv(
        self, exchange: str, symbol: str, timeframe: str, frame: pd.DataFrame
    ) -> Path:
        path = self.ohlcv_path(exchange, symbol, timeframe)
        path.parent.mkdir(parents=True, exist_ok=True)
        if frame.empty:
            raise ValueError("refusing to replace OHLCV cache with an empty frame")
        # Preserve the last known-good cache if a write is interrupted (for
        # example, by a full disk). os.replace is atomic on the same volume.
        tmp = path.with_name(f".{path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp")
        try:
            with tmp.open("w", encoding="utf-8", newline="") as fh:
                frame.to_csv(fh, index=False)
                fh.flush()
                os.fsync(fh.fileno())
            if tmp.stat().st_size == 0:
                raise OSError("refusing to replace OHLCV cache with an empty CSV")
            os.replace(tmp, path)
        finally:
            try:
                tmp.unlink(missing_ok=True)
            except OSError:
                pass
        return path

    def load_ohlcv(
        self, exchange: str, symbol: str, timeframe: str
    ) -> pd.DataFrame | None:
        path = self.ohlcv_path(exchange, symbol, timeframe)
        if not path.exists():
            return None
        try:
            frame = pd.read_csv(path)
        except (OSError, UnicodeDecodeError, pd.errors.EmptyDataError, pd.errors.ParserError):
            # Cache data is disposable. A malformed cache is unavailable data,
            # never a process-wide tracker failure.
            return None
        if frame.empty:
            return None
        if "timestamp" in frame.columns:
            frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
        return frame

    # ------------------------------------------------------------------
    # Stocks OHLCV (separate path layout: data/raw/stocks/{tf}/{SYMBOL}.csv).
    # Used by the signal tracker when signal.asset_class == 'stocks'.
    # ------------------------------------------------------------------
    def stocks_ohlcv_path(self, symbol: str, timeframe: str) -> Path:
        return self.config.raw_dir / "stocks" / timeframe / f"{symbol.upper()}.csv"

    def load_stocks_ohlcv(
        self, symbol: str, timeframe: str
    ) -> pd.DataFrame | None:
        """Load a stocks OHLCV CSV and normalize to the shape the tracker
        expects: lowercase columns + a 'timestamp' column with UTC timestamps.

        The stocks cache is written by yfinance via StockOHLCVCollector with
        the DatetimeIndex as column 0 and OHLCV columns capitalized. The
        crypto cache is written with a 'timestamp' column and lowercase OHLCV.
        This loader converts the stocks layout into the crypto-tracker shape.
        """
        path = self.stocks_ohlcv_path(symbol, timeframe)
        if not path.exists():
            return None
        try:
            frame = pd.read_csv(path, index_col=0, parse_dates=True)
        except Exception:
            return None
        if frame.empty:
            return None
        frame = frame.reset_index()
        # The index column name varies by yfinance version: 'Date', 'Datetime',
        # 'index'. Normalize to 'timestamp'.
        for candidate in ("Date", "Datetime", "index", "Unnamed: 0"):
            if candidate in frame.columns and "timestamp" not in frame.columns:
                frame = frame.rename(columns={candidate: "timestamp"})
                break
        frame = frame.rename(columns={c: c.lower() for c in frame.columns})
        if "timestamp" in frame.columns:
            frame["timestamp"] = pd.to_datetime(
                frame["timestamp"], utc=True, errors="coerce"
            )
            frame = frame.dropna(subset=["timestamp"]).reset_index(drop=True)
        return frame

    def load_market_data(
        self,
        exchange: str,
        symbols: list[str],
        timeframes: list[str],
    ) -> dict[str, dict[str, pd.DataFrame]]:
        market_data: dict[str, dict[str, pd.DataFrame]] = {}
        for symbol in symbols:
            tf_data: dict[str, pd.DataFrame] = {}
            for timeframe in timeframes:
                frame = self.load_ohlcv(exchange, symbol, timeframe)
                if frame is not None and not frame.empty:
                    tf_data[timeframe] = frame
            if tf_data:
                market_data[symbol] = tf_data
        return market_data

    def discovered_symbols(self, exchange: str, timeframe: str) -> list[str]:
        base = self.config.raw_dir / "ohlcv" / exchange / timeframe
        if not base.exists():
            return []
        return sorted(filename_to_symbol(path.stem) for path in base.glob("*.csv"))

    def save_json(self, relative_path: str | Path, payload: Any) -> Path:
        path = self.config.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        return path

    def read_json(self, relative_path: str | Path) -> Any:
        path = self.config.root / relative_path
        if not path.exists():
            return None
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save_markdown(self, relative_path: str | Path, content: str) -> Path:
        path = self.config.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path
