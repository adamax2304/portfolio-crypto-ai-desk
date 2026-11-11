"""Thin wrapper around yfinance for OHLCV fetches.

yfinance is unofficial, free, and rate-limited. Documented limits we care
about:
  - 15m bars: max 60 days of history per request
  - 1h bars: max ~730 days (request 729d to avoid boundary drift)
  - 1d bars: years of history, effectively unbounded for our needs
  - 1wk bars: same as 1d

We avoid bulk Tickers() calls to keep failures granular (one symbol erroring
shouldn't poison the batch). Each call uses Ticker(symbol).history() and
falls back to yf.download() on shape failures.
"""

from __future__ import annotations

import time
import os
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
from typing import Any

import pandas as pd

from src.logger import get_logger

_LOG = get_logger("stocks.yf_client")
_ALPACA_AUTH_DISABLED_UNTIL = 0.0
_ALPACA_AUTH_BACKOFF_SECONDS = 15 * 60.0

# yfinance period strings tuned to the API caps for each interval.
DEFAULT_PERIODS: dict[str, str] = {
    "15m": "60d",
    "30m": "60d",
    # Yahoo rejects some 730d requests when endpoint rounding makes the
    # computed start/end span a few seconds wider than its hard limit.
    "1h": "729d",
    "1d": "5y",
    "1wk": "10y",
    "1mo": "max",
}


@dataclass(frozen=True)
class OHLCVResult:
    symbol: str
    interval: str
    rows: int
    last_close: float | None
    last_timestamp: str
    dataframe: pd.DataFrame
    source: str = "yfinance"


def _alpaca_auth_disabled() -> bool:
    return time.monotonic() < _ALPACA_AUTH_DISABLED_UNTIL


def _disable_alpaca_auth_temporarily() -> None:
    global _ALPACA_AUTH_DISABLED_UNTIL
    _ALPACA_AUTH_DISABLED_UNTIL = time.monotonic() + _ALPACA_AUTH_BACKOFF_SECONDS


def _normalize_interval(interval: str) -> str:
    # yfinance uses 'wk' and 'mo' instead of 'w'/'M' — accept either.
    mapping = {
        "1w": "1wk",
        "1M": "1mo",
        "60m": "1h",
    }
    return mapping.get(interval, interval)


def fetch_ohlcv(
    symbol: str,
    interval: str,
    *,
    period: str | None = None,
    retries: int = 2,
    sleep_between: float = 0.4,
) -> OHLCVResult | None:
    """Fetch OHLCV bars for `symbol` at `interval`. Returns None on failure.

    Output DataFrame has columns: open, high, low, close, volume; index is
    a tz-aware DatetimeIndex (UTC for intraday, naive midnight for daily).
    """

    yf_interval = _normalize_interval(interval)
    yf_period = period or DEFAULT_PERIODS.get(yf_interval, "1y")

    # The configured primary is optional. A failed/empty response never manufactures a bar: the
    # explicit yfinance fallback remains available and downstream freshness decides eligibility.
    primary = _fetch_primary(symbol, yf_interval, yf_period)
    if primary is not None:
        source, live = primary
        return OHLCVResult(
            symbol=symbol,
            interval=yf_interval,
            rows=len(live),
            last_close=float(live["close"].iloc[-1]) if "close" in live else None,
            last_timestamp=str(live.index[-1]),
            dataframe=live,
            source=source,
        )

    import yfinance as yf

    last_err: Exception | None = None
    for attempt in range(retries + 1):
        try:
            ticker = yf.Ticker(symbol)
            frame = ticker.history(
                period=yf_period,
                interval=yf_interval,
                auto_adjust=False,
                actions=False,
            )
            if frame is None or frame.empty:
                # Try yf.download as a secondary path — some indices
                # (e.g. ^VIX) misbehave through Ticker.history.
                frame = yf.download(
                    symbol,
                    period=yf_period,
                    interval=yf_interval,
                    auto_adjust=False,
                    progress=False,
                    threads=False,
                )
            if frame is None or frame.empty:
                last_err = RuntimeError("yfinance returned empty frame")
                time.sleep(sleep_between)
                continue
            frame = _normalize_frame(frame)
            last_ts = str(frame.index[-1])
            last_close = float(frame["close"].iloc[-1]) if "close" in frame else None
            _LOG.info("yfinance %s/%s -> %d rows", symbol, yf_interval, len(frame))
            return OHLCVResult(
                symbol=symbol,
                interval=yf_interval,
                rows=len(frame),
                last_close=last_close,
                last_timestamp=last_ts,
                dataframe=frame,
                source="yfinance",
            )
        except Exception as exc:  # noqa: BLE001 — yfinance raises many kinds
            last_err = exc
            time.sleep(sleep_between)
    _LOG.warning("yfinance fetch failed for %s/%s after %d attempts: %s",
                 symbol, yf_interval, retries + 1, last_err)
    return None


def fetch_ohlcv_batch(
    symbols: list[str],
    interval: str,
    *,
    period: str | None = None,
    chunk_size: int = 25,
) -> dict[str, OHLCVResult]:
    """Fetch a bounded multi-symbol bar batch.

    The fast stock-reclaim lane needs a newly closed 15m universe bar before
    it can discover candidates. Alpaca's documented multi-symbol endpoint
    avoids one HTTP request per ticker. If Alpaca is unavailable or rejects its
    credentials, one threaded yfinance batch keeps the Paper lane operational;
    its source label remains explicit so it is never mistaken for live-grade.
    """
    unique = list(dict.fromkeys(str(symbol).upper() for symbol in symbols if symbol))
    try:
        from src.stocks.realtime_provider import _load_local_env, active_provider

        _load_local_env()
        if active_provider().name.lower() != "alpaca" or _alpaca_auth_disabled():
            return _fetch_yfinance_batch(unique, interval, period=period)
    except Exception:
        return _fetch_yfinance_batch(unique, interval, period=period)
    key = os.environ.get("ALPACA_API_KEY", "").strip()
    secret = os.environ.get("ALPACA_API_SECRET", "").strip()
    timeframe = {"1m": "1Min", "5m": "5Min", "15m": "15Min",
                 "30m": "30Min", "1h": "1Hour", "1d": "1Day"}.get(
                     _normalize_interval(interval))
    if not key or not secret or timeframe is None:
        return _fetch_yfinance_batch(unique, interval, period=period)

    import requests

    end = datetime.now(timezone.utc)
    start = end - _period_delta(period or DEFAULT_PERIODS.get(interval, "5d"), interval)
    base_url = os.environ.get("ALPACA_DATA_BASE_URL", "https://data.alpaca.markets/v2").rstrip("/")
    headers = {"APCA-API-KEY-ID": key, "APCA-API-SECRET-KEY": secret}
    collected: dict[str, list[dict[str, Any]]] = {symbol: [] for symbol in unique}
    size = max(1, min(int(chunk_size), 100))
    abort_alpaca = False
    for offset in range(0, len(unique), size):
        if abort_alpaca:
            break
        chunk = unique[offset:offset + size]
        page_token: str | None = None
        for _ in range(20):
            params: dict[str, Any] = {
                "symbols": ",".join(chunk), "timeframe": timeframe,
                "start": start.isoformat(), "end": end.isoformat(),
                "limit": 10000, "feed": "iex", "adjustment": "raw", "sort": "asc",
            }
            if page_token:
                params["page_token"] = page_token
            try:
                response = requests.get(
                    f"{base_url}/stocks/bars", params=params, headers=headers, timeout=15,
                )
                response.raise_for_status()
                payload = response.json() or {}
            except Exception as exc:
                status = getattr(getattr(exc, "response", None), "status_code", None)
                _LOG.warning("Alpaca batch %s/%s failed: %s%s", interval, len(chunk),
                             type(exc).__name__, f" status={status}" if status else "")
                if status in {401, 403}:
                    _disable_alpaca_auth_temporarily()
                    abort_alpaca = True
                break
            for symbol, rows in dict(payload.get("bars") or {}).items():
                if symbol in collected:
                    collected[symbol].extend(rows or [])
            page_token = payload.get("next_page_token")
            if not page_token:
                break

    results: dict[str, OHLCVResult] = {}
    for symbol, rows in collected.items():
        if not rows:
            continue
        frame = pd.DataFrame(rows).rename(columns={
            "t": "timestamp", "o": "open", "h": "high", "l": "low",
            "c": "close", "v": "volume",
        })
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
        frame = frame.dropna(subset=["timestamp", "close"]).drop_duplicates("timestamp")
        frame = frame.set_index("timestamp").sort_index()[["open", "high", "low", "close", "volume"]]
        if frame.empty:
            continue
        results[symbol] = OHLCVResult(
            symbol=symbol, interval=_normalize_interval(interval), rows=len(frame),
            last_close=float(frame["close"].iloc[-1]), last_timestamp=str(frame.index[-1]),
            dataframe=frame, source="alpaca_batch",
        )
    missing = [symbol for symbol in unique if symbol not in results]
    if missing:
        results.update(_fetch_yfinance_batch(missing, interval, period=period))
    return results


def _fetch_yfinance_batch(symbols: list[str], interval: str,
                          *, period: str | None = None) -> dict[str, OHLCVResult]:
    """Best-effort multi-ticker fallback with honest delayed-source labels."""
    unique = list(dict.fromkeys(str(symbol).upper() for symbol in symbols if symbol))
    if not unique:
        return {}
    try:
        import yfinance as yf

        normalized_interval = _normalize_interval(interval)
        frame = yf.download(
            tickers=unique,
            period=period or DEFAULT_PERIODS.get(normalized_interval, "5d"),
            interval=normalized_interval,
            auto_adjust=False,
            progress=False,
            threads=True,
            group_by="ticker",
        )
    except Exception as exc:  # noqa: BLE001 - unofficial fallback boundary
        _LOG.warning("yfinance batch %s/%s failed: %s", interval, len(unique), type(exc).__name__)
        return {}
    if frame is None or frame.empty:
        return {}

    results: dict[str, OHLCVResult] = {}
    for symbol in unique:
        try:
            if isinstance(frame.columns, pd.MultiIndex):
                level0 = {str(value).upper() for value in frame.columns.get_level_values(0)}
                level1 = {str(value).upper() for value in frame.columns.get_level_values(1)}
                if symbol in level0:
                    item = frame.xs(symbol, axis=1, level=0)
                elif symbol in level1:
                    item = frame.xs(symbol, axis=1, level=1)
                else:
                    continue
            elif len(unique) == 1:
                item = frame
            else:
                continue
            item = _normalize_frame(item.copy())
            if item.empty or "close" not in item:
                continue
            item.index = pd.to_datetime(item.index, utc=True, errors="coerce")
            item = item[~item.index.isna()].sort_index()
            if item.empty:
                continue
            results[symbol] = OHLCVResult(
                symbol=symbol, interval=normalized_interval, rows=len(item),
                last_close=float(item["close"].iloc[-1]),
                last_timestamp=str(item.index[-1]), dataframe=item,
                source="yfinance_batch",
            )
        except Exception as exc:  # noqa: BLE001 - one ticker cannot poison the batch
            _LOG.warning("yfinance batch normalize failed for %s/%s: %s",
                         symbol, interval, type(exc).__name__)
    return results


def _fetch_primary(symbol: str, interval: str, period: str) -> tuple[str, pd.DataFrame] | None:
    """Best-effort configured primary market-data adapter.

    This function never invents bars and never makes an order request.  It is
    deliberately small so a missing key, unsupported interval, or provider
    outage falls back to yfinance and is still visible to the coverage gate.
    """
    try:
        from src.stocks.realtime_provider import _load_local_env, active_provider
        _load_local_env()
        provider = active_provider().name.lower()
    except Exception:
        return None
    if provider not in {"finnhub", "polygon", "alpaca"}:
        return None

    import requests

    end = datetime.now(timezone.utc)
    days = 60 if interval in {"1m", "5m", "15m", "30m", "1h"} else 365 * 5
    start = end - timedelta(days=days)
    try:
        if provider == "finnhub":
            key = os.environ.get("FINNHUB_API_KEY", "").strip()
            if not key:
                return None
            resolution = {"1m": "1", "5m": "5", "15m": "15", "30m": "30",
                          "1h": "60", "1d": "D", "1wk": "W", "1mo": "M"}.get(interval)
            if resolution is None or symbol.startswith("^") or "-" in symbol:
                return None
            end = datetime.now(timezone.utc)
            start = end - _period_delta(period, interval)
            response = requests.get(
                "https://finnhub.io/api/v1/stock/candle",
                params={"symbol": symbol, "resolution": resolution, "from": int(start.timestamp()),
                        "to": int(end.timestamp()), "token": key},
                timeout=12,
            )
            response.raise_for_status()
            payload = response.json() or {}
            if str(payload.get("s") or "").lower() != "ok":
                return None
            frame = pd.DataFrame({
                "timestamp": payload.get("t") or [], "open": payload.get("o") or [],
                "high": payload.get("h") or [], "low": payload.get("l") or [],
                "close": payload.get("c") or [], "volume": payload.get("v") or [],
            })
            if frame.empty:
                return None
            frame["timestamp"] = pd.to_datetime(frame["timestamp"], unit="s", utc=True, errors="coerce")
            frame = frame.dropna(subset=["timestamp", "close"]).drop_duplicates("timestamp").sort_values("timestamp")
            frame = frame.set_index("timestamp")[["open", "high", "low", "close", "volume"]]
            return ("finnhub", frame) if not frame.empty else None

        if provider == "polygon":
            key = os.environ.get("POLYGON_API_KEY", "").strip()
            if not key:
                return None
            mult, unit = _polygon_interval(interval)
            url = (f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/"
                   f"{mult}/{unit}/{start.date().isoformat()}/{end.date().isoformat()}")
            payload = requests.get(url, params={"adjusted": "false", "sort": "asc",
                                                 "limit": 50000, "apiKey": key}, timeout=12).json()
            rows = payload.get("results") or []
            if not rows:
                return None
            frame = _bars_frame(rows, timestamp_key="t", scale=1_000)
            return ("polygon", frame) if not frame.empty else None

        key = os.environ.get("ALPACA_API_KEY", "").strip()
        secret = os.environ.get("ALPACA_API_SECRET", "").strip()
        if not key or not secret or _alpaca_auth_disabled():
            return None
        timeframe = {"1m": "1Min", "5m": "5Min", "15m": "15Min",
                     "30m": "30Min", "1h": "1Hour", "1d": "1Day"}.get(interval)
        if timeframe is None:
            return None
        data_base_url = os.environ.get(
            "ALPACA_DATA_BASE_URL", "https://data.alpaca.markets/v2"
        ).rstrip("/")
        r = requests.get(
            f"{data_base_url}/stocks/{symbol}/bars",
            params={"timeframe": timeframe, "start": start.isoformat(), "end": end.isoformat(),
                    "limit": 10000, "feed": "iex", "adjustment": "raw",
                    # Alpaca can paginate a long range below the requested
                    # limit. Ask for the newest page so freshness is preserved;
                    # the DataFrame is sorted ascending immediately below.
                    "sort": "desc"},
            headers={"APCA-API-KEY-ID": key, "APCA-API-SECRET-KEY": secret}, timeout=12,
        )
        if getattr(r, "status_code", None) in {401, 403}:
            _disable_alpaca_auth_temporarily()
        r.raise_for_status()
        rows = (r.json() or {}).get("bars") or []
        if not rows:
            return None
        frame = pd.DataFrame(rows).rename(columns={"t": "timestamp", "o": "open", "h": "high",
                                                    "l": "low", "c": "close", "v": "volume"})
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
        frame = frame.set_index("timestamp").sort_index()[["open", "high", "low", "close", "volume"]]
        return ("alpaca", frame) if not frame.empty else None
    except Exception as exc:  # provider failures remain non-fatal
        _LOG.warning("primary stocks provider %s failed for %s/%s: %s", provider, symbol, interval, type(exc).__name__)
        return None


def _period_delta(period: str, interval: str) -> timedelta:
    """Translate the existing yfinance-style period to a bounded Finnhub request window."""
    text = str(period or "").strip().lower()
    if text == "max":
        return timedelta(days=3650)
    try:
        count = int(text[:-1])
        unit = text[-1:]
        if unit == "d":
            return timedelta(days=count)
        if unit == "y":
            return timedelta(days=count * 365)
        if unit == "m":
            return timedelta(days=count * 30)
        if unit == "w":
            return timedelta(days=count * 7)
    except (TypeError, ValueError):
        pass
    return timedelta(days=60 if interval in {"1m", "5m", "15m", "30m", "1h"} else 365 * 5)


def _polygon_interval(interval: str) -> tuple[int, str]:
    mapping = {"1m": (1, "minute"), "5m": (5, "minute"), "15m": (15, "minute"),
               "30m": (30, "minute"), "1h": (1, "hour"), "1d": (1, "day")}
    return mapping.get(interval, (1, "day"))


def _bars_frame(rows: list[dict], *, timestamp_key: str, scale: int) -> pd.DataFrame:
    frame = pd.DataFrame(rows).rename(columns={timestamp_key: "timestamp", "o": "open", "h": "high",
                                                "l": "low", "c": "close", "v": "volume"})
    frame["timestamp"] = pd.to_datetime(frame["timestamp"] * scale, unit="ns", utc=True,
                                         errors="coerce")
    return frame.set_index("timestamp").sort_index()[["open", "high", "low", "close", "volume"]]


def _normalize_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Coerce yfinance frame into lowercase OHLCV with a clean index."""

    # yf.download under multi-symbol returns a MultiIndex on columns; for our
    # single-symbol call paths it's a flat Index, but be defensive anyway.
    if isinstance(frame.columns, pd.MultiIndex):
        # Drop the symbol level so we get plain Open/High/Low/Close/Volume.
        frame = frame.copy()
        frame.columns = [c[0] if isinstance(c, tuple) else c for c in frame.columns]
    cols = {c: c.lower() for c in frame.columns}
    frame = frame.rename(columns=cols)
    keep = [c for c in ("open", "high", "low", "close", "volume") if c in frame.columns]
    frame = frame[keep].dropna(how="all")
    return frame


def fetch_calendar(symbol: str) -> dict[str, Any] | None:
    """Try to read the earnings calendar entry from yfinance.

    Returns None if the field is unavailable (common — yfinance's calendar
    coverage is inconsistent and small/mid caps often have nothing).
    """

    import yfinance as yf

    try:
        ticker = yf.Ticker(symbol)
        cal = ticker.calendar
    except Exception as exc:  # noqa: BLE001
        _LOG.warning("yfinance calendar fetch failed for %s: %s", symbol, exc)
        return None
    if cal is None:
        return None
    # yfinance returns a dict in newer versions, a DataFrame in older ones.
    if isinstance(cal, pd.DataFrame):
        if cal.empty:
            return None
        try:
            return cal.to_dict(orient="list")
        except Exception:
            return None
    if isinstance(cal, dict) and cal:
        # Coerce datetime / Timestamp values to ISO strings for storage.
        out: dict[str, Any] = {}
        for k, v in cal.items():
            if isinstance(v, (pd.Timestamp,)):
                out[str(k)] = v.isoformat()
            elif isinstance(v, list):
                out[str(k)] = [
                    item.isoformat() if isinstance(item, pd.Timestamp) else item
                    for item in v
                ]
            else:
                out[str(k)] = v
        return out
    return None
