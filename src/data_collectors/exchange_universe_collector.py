"""Generic ccxt-backed universe-discovery + ranking for any exchange.

The original ``BinanceUniverseCollector`` did this only for Binance. This
module factors the same logic into a per-exchange class so Bybit and MEXC can
participate. The orchestrator (``MultiExchangeUniverseCollector``) is in a
separate module to keep responsibilities clean.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from statistics import median
from typing import Any

import pandas as pd

from src.config import ProjectConfig
from src.indicators.relative_strength import relative_strength_return
from src.indicators.technicals import enrich_ohlcv, pct_return, recent_range
from src.indicators.volume_anomaly import volume_ratio
from src.logger import get_logger
from src.storage.file_store import FileStore
from src.utils.symbols import normalize_symbol
from src.utils.time import utc_now
from src.utils.validation import clamp


VALID_UNIVERSE_SYMBOL = re.compile(r"^[A-Z0-9]+/[A-Z0-9]+$")


@dataclass
class ExchangeUniverseResult:
    exchange: str
    symbols: list[str] = field(default_factory=list)
    records: list[dict[str, Any]] = field(default_factory=list)
    excluded: list[dict[str, str]] = field(default_factory=list)
    failed: dict[str, str] = field(default_factory=dict)
    counts: dict[str, int] = field(default_factory=dict)


class ExchangeUniverseCollector:
    """Discover and rank a USDT universe on a single exchange via ccxt.

    Stage 1 reads markets + 24h tickers, filters junk, returns a normalized
    record per symbol.

    Stage 2 fetches lightweight OHLCV on the rough-filtered top names and
    builds an opportunity score against the venue's BTC frame.
    """

    def __init__(self, exchange: str, config: ProjectConfig, store: FileStore):
        self.exchange = exchange.lower()
        self.config = config
        self.store = store
        self.logger = get_logger(f"{self.__class__.__name__}[{self.exchange}]")

    @property
    def ccxt_id(self) -> str:
        return self.config.exchange_ccxt_id(self.exchange)

    def _build_exchange(self, market_type: str = "spot") -> Any:
        try:
            import ccxt
        except ImportError as exc:
            raise RuntimeError("ccxt is not installed.") from exc
        exchange_class = getattr(ccxt, self.ccxt_id, None)
        if exchange_class is None:
            raise RuntimeError(
                f"ccxt does not expose adapter `{self.ccxt_id}` for exchange {self.exchange}."
            )
        default_type = "future" if market_type in {"futures", "perpetual", "swap"} else "spot"
        return exchange_class({"enableRateLimit": True, "options": {"defaultType": default_type}})

    def discover(self, market_type: str | None = None) -> ExchangeUniverseResult:
        market_type = market_type or str(self.config.universe_setting("market_type", "spot"))
        quote = str(self.config.universe_setting("quote_currency", "USDT")).upper()
        result = ExchangeUniverseResult(exchange=self.exchange)
        try:
            exchange = self._build_exchange(market_type)
            markets = exchange.load_markets()
            try:
                tickers = exchange.fetch_tickers()
            except Exception as exc:
                self.logger.info("%s fetch_tickers failed (%s); proceeding without volume data", self.exchange, exc)
                tickers = {}
        except Exception as exc:
            self.logger.warning("%s discover failed: %s", self.exchange, exc)
            result.failed["__exchange__"] = str(exc)
            return result

        for exchange_symbol, market in markets.items():
            normalized = self._normalize_market_symbol(market, exchange_symbol)
            reason = self._exclusion_reason(normalized, market, market_type, quote)
            ticker = tickers.get(exchange_symbol) or tickers.get(normalized) or {}
            record = {
                "exchange": self.exchange,
                "symbol": normalized,
                "exchange_symbol": exchange_symbol,
                "market_type": market_type,
                "base": str(market.get("base") or ""),
                "quote": str(market.get("quote") or ""),
                "active": bool(market.get("active", True)),
                "quote_volume": round(self._quote_volume(ticker), 2),
                "last": self._to_float(ticker.get("last")),
                "bid": self._to_float(ticker.get("bid")),
                "ask": self._to_float(ticker.get("ask")),
                "spread_pct": self._spread_pct(ticker),
                "change_24h": self._to_float(ticker.get("percentage")),
                "accepted": reason is None,
                "exclude_reason": reason,
            }
            result.records.append(record)
            if reason is None:
                result.symbols.append(normalized)
            else:
                result.excluded.append({"symbol": normalized, "reason": reason})

        result.symbols = sorted(set(result.symbols))
        result.records.sort(key=lambda item: item.get("quote_volume") or 0, reverse=True)
        result.counts = {
            "accepted": len(result.symbols),
            "excluded": len(result.excluded),
            "total_records": len(result.records),
        }
        return result

    def rank_candidates(
        self,
        records: list[dict[str, Any]],
        mode: str = "intraday",
        max_rank_scan: int | None = None,
        discovery: bool = False,
    ) -> list[dict[str, Any]]:
        """Stage 2 ranking for this venue. Returns scored candidate rows."""
        trade_mode = mode if mode in self.config.universe.get("modes", {}) else "intraday"
        mode_config = self.config.universe.get("modes", {}).get(trade_mode, {})
        timeframes = [str(item) for item in mode_config.get("timeframes", ["15m", "1h", "4h"])]
        primary_tf = str(mode_config.get("primary_timeframe", "1h"))
        accepted = [row for row in records if row.get("accepted") and row.get("exchange") == self.exchange]
        rough = self._rough_filter(accepted, mode=trade_mode, max_rank_scan=max_rank_scan, discovery=discovery)
        try:
            exchange = self._build_exchange(str(records[0].get("market_type") or "spot")) if records else self._build_exchange()
        except Exception as exc:
            self.logger.warning("%s ranking aborted: %s", self.exchange, exc)
            return []
        try:
            btc_frames = self._fetch_symbol_frames(exchange, "BTC/USDT", timeframes, limit=120)
        except Exception:
            btc_frames = {}
        rows: list[dict[str, Any]] = []
        for item in rough:
            symbol = str(item["symbol"])
            try:
                frames = self._fetch_symbol_frames(exchange, symbol, timeframes, limit=120)
                row = self._rank_row(symbol, item, frames, btc_frames, mode, primary_tf)
            except Exception as exc:
                row = {
                    "exchange": self.exchange,
                    "symbol": symbol,
                    "opportunity_score": 0.0,
                    "risk_flags": [f"rank_data_error: {exc}"],
                }
            rows.append(row)
        rows.sort(key=lambda row: row.get("opportunity_score", 0.0), reverse=True)
        for index, row in enumerate(rows, start=1):
            row["rank_on_exchange"] = index
            row["exchange"] = self.exchange
        return rows

    def _rough_filter(
        self,
        records: list[dict[str, Any]],
        mode: str,
        max_rank_scan: int | None = None,
        discovery: bool = False,
    ) -> list[dict[str, Any]]:
        min_volume = self.config.min_24h_volume_for_exchange(self.exchange, discovery=discovery)
        max_spread = float(self.config.universe_setting("max_spread_pct", 0.35))
        preferred = {
            normalize_symbol(symbol)
            for symbol in self.config.universe_setting("preferred_symbols", []) or self.config.symbols
        }
        rows: list[dict[str, Any]] = []
        for row in records:
            quote_volume = float(row.get("quote_volume") or 0)
            spread = row.get("spread_pct")
            if quote_volume < min_volume and row.get("symbol") not in preferred:
                continue
            if spread is not None and float(spread) > max_spread:
                continue
            rough_score = self._rough_score(row)
            rows.append({**row, "rough_score": rough_score})
        rows.sort(key=lambda item: item["rough_score"], reverse=True)
        setting_fn = self.config.universe_setting_for_discovery if discovery else self.config.universe_setting
        limit = int(max_rank_scan or setting_fn("max_symbols_for_rank_scan", 120))
        preferred_rows = [row for row in rows if row.get("symbol") in preferred]
        other_rows = [row for row in rows if row.get("symbol") not in preferred]
        return [*preferred_rows, *other_rows][:limit]

    def _exclusion_reason(
        self, symbol: str, market: dict[str, Any], market_type: str, quote: str
    ) -> str | None:
        if not VALID_UNIVERSE_SYMBOL.match(symbol):
            return "invalid_or_non_ascii_symbol"
        if self.config.universe_setting("exclude_inactive", True) and not bool(market.get("active", True)):
            return "inactive"
        if str(market.get("quote", "")).upper() != quote:
            return "wrong_quote"
        if market_type == "spot" and not market.get("spot"):
            return "not_spot"
        if market_type in {"futures", "perpetual", "swap"} and not market.get("swap"):
            return "not_perpetual"
        if symbol in {normalize_symbol(item) for item in self.config.universe_setting("excluded_symbols", []) or []}:
            return "explicitly_excluded"
        base = str(market.get("base", "")).upper()
        if base in {str(item).upper() for item in self.config.universe_setting("stable_or_fiat_bases", []) or []}:
            return "stable_or_fiat_base"
        keywords = [str(item).upper() for item in self.config.universe_setting("excluded_keywords", []) or []]
        raw = f"{symbol} {base} {market.get('id', '')}".upper()
        if any(keyword in raw for keyword in keywords):
            return "leveraged_or_low_quality_keyword"
        return None

    def _fetch_symbol_frames(
        self, exchange: Any, symbol: str, timeframes: list[str], limit: int = 120
    ) -> dict[str, pd.DataFrame]:
        frames: dict[str, pd.DataFrame] = {}
        native = self.config.exchange_alias(self.exchange, symbol)
        for timeframe in timeframes:
            try:
                rows = exchange.fetch_ohlcv(native, timeframe=timeframe, limit=limit)
            except Exception:
                continue
            if rows:
                frames[timeframe] = self._frame_from_rows(rows)
        return frames

    @staticmethod
    def _frame_from_rows(rows: list[list[float]]) -> pd.DataFrame:
        frame = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], unit="ms", utc=True)
        for column in ["open", "high", "low", "close", "volume"]:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
        return frame.dropna().sort_values("timestamp").reset_index(drop=True)

    @staticmethod
    def _normalize_market_symbol(market: dict[str, Any], exchange_symbol: str) -> str:
        symbol = str(market.get("symbol") or exchange_symbol)
        if ":" in symbol:
            symbol = symbol.split(":")[0]
        return normalize_symbol(symbol)

    @staticmethod
    def _quote_volume(ticker: dict[str, Any]) -> float:
        for key in ("quoteVolume", "quote_volume"):
            value = ticker.get(key)
            if value is not None:
                return ExchangeUniverseCollector._to_float(value) or 0.0
        info = ticker.get("info") or {}
        for key in ("quoteVolume", "quote_volume"):
            value = info.get(key)
            if value is not None:
                return ExchangeUniverseCollector._to_float(value) or 0.0
        return 0.0

    @staticmethod
    def _to_float(value: Any) -> float | None:
        try:
            if value in (None, ""):
                return None
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _spread_pct(ticker: dict[str, Any]) -> float | None:
        bid = ExchangeUniverseCollector._to_float(ticker.get("bid"))
        ask = ExchangeUniverseCollector._to_float(ticker.get("ask"))
        if bid is None or ask is None or bid <= 0 or ask <= 0:
            return None
        mid = (bid + ask) / 2
        return round((ask - bid) / mid * 100, 4) if mid else None

    @staticmethod
    def _rough_score(row: dict[str, Any]) -> float:
        volume = float(row.get("quote_volume") or 0)
        change = abs(float(row.get("change_24h") or 0))
        spread = row.get("spread_pct")
        spread_penalty = 0 if spread is None else min(float(spread) * 12, 25)
        return min(volume / 1_000_000, 80) + min(change * 3, 45) - spread_penalty

    def _rank_row(
        self,
        symbol: str,
        ticker_row: dict[str, Any],
        frames: dict[str, pd.DataFrame],
        btc_frames: dict[str, pd.DataFrame],
        mode: str,
        primary_tf: str,
    ) -> dict[str, Any]:
        primary = frames.get(primary_tf)
        if primary is None or len(primary) < 35:
            return {
                "exchange": self.exchange,
                "symbol": symbol,
                "opportunity_score": 0.0,
                "risk_flags": ["insufficient_candles"],
            }
        enriched = enrich_ohlcv(primary)
        last = enriched.iloc[-1]
        close = float(last["close"])
        atr = float(last["atr14"]) if pd.notna(last["atr14"]) else 0.0
        atr_percent = (atr / close * 100) if close else 0.0
        v_ratio = volume_ratio(primary, 20) or 0.0
        recent_quote_volume = float(primary.iloc[-1]["volume"]) * close
        btc_primary = btc_frames.get(primary_tf)
        rs_btc = (
            relative_strength_return(primary, btc_primary, self._lookback_periods(primary_tf, mode))
            if btc_primary is not None and symbol != "BTC/USDT"
            else 0.0
        )
        range_high, range_low = recent_range(primary, 20)
        breakout = bool(range_high is not None and close > range_high)
        breakdown = bool(range_low is not None and close < range_low)
        range_expansion = self._range_expansion(primary)
        change_1h = self._change_for_horizon(frames, "1h")
        change_4h = self._change_for_horizon(frames, "4h")
        change_24h = self._change_for_horizon(frames, "24h")
        trend_score = self._trend_score(enriched, change_1h, change_4h, change_24h, rs_btc, breakout, breakdown)
        liquidity_score = self._liquidity_score(float(ticker_row.get("quote_volume") or 0), ticker_row.get("spread_pct"))
        volatility_score = clamp((atr_percent / max(float(self._min_atr_percent(mode)), 0.01)) * 35, 0, 100)
        volume_score = clamp(v_ratio * 35)
        opportunity_score = clamp(
            trend_score * 0.34
            + liquidity_score * 0.18
            + volume_score * 0.2
            + volatility_score * 0.16
            + clamp((rs_btc or 0) * 5 + 50) * 0.12
        )
        risk_flags = self._risk_flags(ticker_row, recent_quote_volume, atr_percent, v_ratio, range_expansion, mode)
        if abs(float(last.get("close", close)) - float(last.get("ema20", close))) > 2.5 * atr and atr > 0:
            risk_flags.append("extended_from_ema20")
            opportunity_score -= 8
        if ticker_row.get("spread_pct") is None:
            risk_flags.append("spread_unavailable")
        return {
            "exchange": self.exchange,
            "symbol": symbol,
            "mode": mode,
            "change_1h": round(change_1h, 2) if change_1h is not None else None,
            "change_4h": round(change_4h, 2) if change_4h is not None else None,
            "change_24h": round(change_24h, 2) if change_24h is not None else None,
            "volume_anomaly": round(v_ratio, 2),
            "atr_percent": round(atr_percent, 3),
            "relative_strength_btc": round(rs_btc, 2) if rs_btc is not None else None,
            "trend_score": round(trend_score, 1),
            "liquidity_score": round(liquidity_score, 1),
            "opportunity_score": round(clamp(opportunity_score), 1),
            "quote_volume_24h": round(float(ticker_row.get("quote_volume") or 0), 2),
            "recent_candle_quote_volume": round(recent_quote_volume, 2),
            "spread_pct": ticker_row.get("spread_pct"),
            "breakout": breakout,
            "breakdown": breakdown,
            "range_expansion": round(range_expansion, 2),
            "risk_flags": sorted(set(risk_flags)),
        }

    def _risk_flags(
        self,
        row: dict[str, Any],
        recent_quote_volume: float,
        atr_percent: float,
        v_ratio: float,
        range_expansion: float,
        mode: str,
    ) -> list[str]:
        flags: list[str] = []
        min_volume = self.config.min_24h_volume_for_exchange(self.exchange)
        if float(row.get("quote_volume") or 0) < min_volume:
            flags.append("low_24h_quote_volume")
        recent_min = self.config.universe_setting("min_recent_candle_quote_volume", {})
        if isinstance(recent_min, dict):
            min_recent = float(recent_min.get(mode, recent_min.get("intraday", 75_000)))
        else:
            min_recent = float(recent_min)
        if recent_quote_volume < min_recent:
            flags.append("low_recent_candle_volume")
        spread = row.get("spread_pct")
        if spread is not None and float(spread) > float(self.config.universe_setting("max_spread_pct", 0.35)):
            flags.append("wide_spread")
        if atr_percent < self._min_atr_percent(mode):
            flags.append("low_atr_percent")
        if v_ratio < 0.5:
            flags.append("quiet_volume")
        if range_expansion >= 1.8:
            flags.append("range_expansion")
        return flags

    def _min_atr_percent(self, mode: str) -> float:
        payload = self.config.universe_setting("min_atr_percent", 0.35)
        if isinstance(payload, dict):
            return float(payload.get(mode, payload.get("intraday", 0.35)))
        return float(payload)

    @staticmethod
    def _lookback_periods(timeframe: str, mode: str) -> int:
        if mode == "scalp":
            return 12 if timeframe == "5m" else 8
        if timeframe == "4h":
            return 6
        if timeframe == "15m":
            return 16
        return 24

    @staticmethod
    def _range_expansion(frame: pd.DataFrame) -> float:
        enriched = enrich_ohlcv(frame)
        if len(enriched) < 20:
            return 0.0
        ranges = (enriched["high"] - enriched["low"]).tail(20).tolist()
        baseline = median(ranges[:-1]) if len(ranges) > 1 else 0.0
        return float(ranges[-1] / baseline) if baseline else 0.0

    @staticmethod
    def _trend_score(
        enriched: pd.DataFrame,
        change_1h: float | None,
        change_4h: float | None,
        change_24h: float | None,
        rs_btc: float | None,
        breakout: bool,
        breakdown: bool,
    ) -> float:
        last = enriched.iloc[-1]
        close = float(last["close"])
        ema20 = float(last["ema20"]) if pd.notna(last["ema20"]) else close
        ema50 = float(last["ema50"]) if pd.notna(last["ema50"]) else close
        score = 45.0
        if close > ema20 > ema50:
            score += 18
        if close < ema20 < ema50:
            score -= 12
        for change, weight in [(change_1h, 2.5), (change_4h, 1.8), (change_24h, 0.9), (rs_btc, 1.8)]:
            if change is not None:
                score += max(min(change, 12), -12) * weight
        if breakout:
            score += 12
        if breakdown:
            score -= 8
        return clamp(score)

    @staticmethod
    def _liquidity_score(quote_volume: float, spread_pct: float | None) -> float:
        score = clamp((quote_volume / 50_000_000) * 70)
        if quote_volume >= 100_000_000:
            score = max(score, 85)
        if spread_pct is not None:
            score -= min(spread_pct * 35, 30)
        return clamp(score)

    def _change_for_horizon(self, frames: dict[str, pd.DataFrame], horizon: str) -> float | None:
        if horizon == "1h":
            if "1m" in frames:
                return pct_return(frames["1m"], 60)
            if "5m" in frames:
                return pct_return(frames["5m"], 12)
            if "15m" in frames:
                return pct_return(frames["15m"], 4)
            if "1h" in frames:
                return pct_return(frames["1h"], 1)
        if horizon == "4h":
            if "5m" in frames:
                return pct_return(frames["5m"], 48)
            if "15m" in frames:
                return pct_return(frames["15m"], 16)
            if "1h" in frames:
                return pct_return(frames["1h"], 4)
            if "4h" in frames:
                return pct_return(frames["4h"], 1)
        if horizon == "24h":
            if "15m" in frames:
                return pct_return(frames["15m"], 96)
            if "1h" in frames:
                return pct_return(frames["1h"], 24)
            if "4h" in frames:
                return pct_return(frames["4h"], 6)
            if "1d" in frames:
                return pct_return(frames["1d"], 1)
        return None
