"""Deep-history OHLCV store — a SEPARATE tree from the live rolling cache.

Layout mirrors the rolling cache so the same parser / symbol filenames apply,
but lives under ``data/history/ohlcv/{exchange}/{timeframe}/{symbol}.csv`` so:

  * the live rolling collector (``FileStore.save_ohlcv`` → ``data/raw/ohlcv/...``)
    keeps overwriting its 9-day window untouched — forward evidence stays clean;
  * this store is written ONLY by the historical backfiller and grows over time
    (merge-on-write: append + dedup + sort), giving months of real history for
    offline settings replay.

Nothing here reads or writes the live cache, the DB, or any signal table.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import ProjectConfig
from src.utils.symbols import filename_to_symbol, symbol_to_filename

_COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]


def history_root(config: ProjectConfig) -> Path:
    """`data/history` — sibling of `data/raw`, so it is never touched by the
    rolling collector which writes under `data/raw/ohlcv`."""
    return config.raw_dir.parent / "history"


def history_path(config: ProjectConfig, exchange: str, symbol: str, timeframe: str) -> Path:
    return (
        history_root(config)
        / "ohlcv"
        / exchange.lower()
        / timeframe
        / f"{symbol_to_filename(symbol)}.csv"
    )


def _normalize(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    # tolerate either a 'timestamp' column or a ccxt ms-int first column
    if "timestamp" not in frame.columns:
        return pd.DataFrame(columns=_COLUMNS)
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
    for col in ("open", "high", "low", "close", "volume"):
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce")
        else:
            frame[col] = pd.NA
    frame = frame[_COLUMNS].dropna(subset=["timestamp", "open", "high", "low", "close"])
    frame = frame.drop_duplicates(subset=["timestamp"], keep="last")
    return frame.sort_values("timestamp").reset_index(drop=True)


def load(config: ProjectConfig, exchange: str, symbol: str, timeframe: str) -> pd.DataFrame | None:
    """Deep history for (exchange, symbol, timeframe) or None if absent/empty."""
    path = history_path(config, exchange, symbol, timeframe)
    if not path.exists():
        return None
    try:
        frame = pd.read_csv(path)
    except Exception:
        return None
    frame = _normalize(frame)
    return frame if not frame.empty else None


def save_merge(
    config: ProjectConfig, exchange: str, symbol: str, timeframe: str, frame: pd.DataFrame
) -> dict:
    """Merge `frame` into the stored history (append + dedup on timestamp + sort).

    Idempotent: re-running the backfill only extends coverage, never truncates.
    Returns a small summary dict for logging/attestation.
    """
    incoming = _normalize(frame)
    path = history_path(config, exchange, symbol, timeframe)
    existing = load(config, exchange, symbol, timeframe)
    before = 0 if existing is None else len(existing)
    if existing is not None and not existing.empty:
        merged = _normalize(pd.concat([existing, incoming], ignore_index=True))
    else:
        merged = incoming
    path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(path, index=False)
    first = merged["timestamp"].min() if not merged.empty else None
    last = merged["timestamp"].max() if not merged.empty else None
    return {
        "exchange": exchange.lower(),
        "symbol": symbol,
        "timeframe": timeframe,
        "rows_before": before,
        "rows_after": len(merged),
        "added": max(0, len(merged) - before),
        "first_ts": None if first is None else first.isoformat(),
        "last_ts": None if last is None else last.isoformat(),
        "path": str(path),
    }


def coverage(config: ProjectConfig, exchange: str, symbol: str, timeframe: str) -> dict | None:
    frame = load(config, exchange, symbol, timeframe)
    if frame is None or frame.empty:
        return None
    return {
        "rows": len(frame),
        "first_ts": frame["timestamp"].min().isoformat(),
        "last_ts": frame["timestamp"].max().isoformat(),
    }


def discovered_symbols(config: ProjectConfig, exchange: str, timeframe: str) -> list[str]:
    base = history_root(config) / "ohlcv" / exchange.lower() / timeframe
    if not base.exists():
        return []
    return sorted(filename_to_symbol(p.stem) for p in base.glob("*.csv"))
