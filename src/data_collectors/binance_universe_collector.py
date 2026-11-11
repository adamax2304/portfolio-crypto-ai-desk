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
from src.utils.symbols import normalize_symbol, symbol_to_filename
from src.utils.time import utc_now
from src.utils.validation import clamp


VALID_UNIVERSE_SYMBOL = re.compile(r"^[A-Z0-9]+/[A-Z0-9]+$")


@dataclass
class UniverseSelection:
    symbols: list[str] = field(default_factory=list)
    liquid_symbols: list[str] = field(default_factory=list)
    lower_volume_symbols: list[str] = field(default_factory=list)
    records: list[dict[str, Any]] = field(default_factory=list)
    failed: dict[str, str] = field(default_factory=dict)


class BinanceUniverseCollector:
    """Two-stage Binance universe scanner.

    Stage 1 discovers all active USDT markets and saves the broad universe.
    Stage 2 cheaply ranks a subset, then selects the best names for deeper
    OHLCV/agent analysis. Bybit/OKX can be added later behind the same shape.
    """

    def __init__(self, config: ProjectConfig, store: FileStore):
        self.config = config
        self.store = store
        self.logger = get_logger(self.__class__.__name__)

    def discover_broad_universe(self, market_type: str | None = None) -> dict[str, Any]:
        market_type = market_type or str(self.config.universe_setting("market_type", "spot"))
        exchange = self._build_exchange(market_type)
        markets = exchange.load_markets()
        tickers = exchange.fetch_tickers()
        quote = str(self.config.universe_setting("quote_currency", "USDT")).upper()
        records: list[dict[str, Any]] = []
        accepted: list[str] = []
        excluded: list[dict[str, str]] = []

        for exchange_symbol, market in markets.items():
            normalized = self._normalize_market_symbol(market, exchange_symbol)
            reason = self._exclusion_reason(normalized, market, market_type, quote)
            ticker = tickers.get(exchange_symbol) or tickers.get(normalized) or {}
            record = {
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
            records.append(record)
            if reason is None:
                accepted.append(normalized)
            else:
                excluded.append({"symbol": normalized, "reason": reason})

        accepted = sorted(set(accepted))
        payload = {
            "generated_at": utc_now().isoformat(),
            "exchange": self.config.exchange_id,
            "market_type": market_type,
            "quote_currency": quote,
            "symbols": accepted,
            "records": sorted(records, key=lambda item: item.get("quote_volume") or 0, reverse=True),
            "excluded": excluded[:500],
            "counts": {
                "accepted": len(accepted),
                "excluded": len(excluded),
                "total_records": len(records),
            },
            "note": "Broad universe uses Binance public market metadata and 24h tickers.",
        }
        self.store.save_json(Path("data") / "processed" / "symbol_universe.json", payload)
        return payload

    def rank_candidates(self, mode: str = "intraday", refresh: bool = False) -> list[dict[str, Any]]:
        universe = self.discover_broad_universe() if refresh else self._load_or_discover_universe()
        records = [row for row in universe.get("records", []) if row.get("accepted")]
        mode_config = self.config.universe.get("modes", {}).get(mode, {})
        timeframes = [str(item) for item in mode_config.get("timeframes", ["15m", "1h", "4h"])]
        primary_tf = str(mode_config.get("primary_timeframe", "1h"))
        rough = self._rough_filter(records, mode=mode)
        exchange = self._build_exchange(str(universe.get("market_type") or self.config.universe_setting("market_type", "spot")))
        btc_frames = self._fetch_symbol_frames(exchange, "BTC/USDT", timeframes, limit=120)
        rows: list[dict[str, Any]] = []

        for item in rough:
            symbol = str(item["symbol"])
            try:
                frames = self._fetch_symbol_frames(exchange, symbol, timeframes, limit=120)
                row = self._rank_row(symbol, item, frames, btc_frames, mode, primary_tf)
            except Exception as exc:
                row = {
                    "symbol": symbol,
                    "opportunity_score": 0.0,
                    "risk_flags": [f"rank_data_error: {exc}"],
                }
            rows.append(row)

        rows.sort(key=lambda row: row.get("opportunity_score", 0.0), reverse=True)
        for index, row in enumerate(rows, start=1):
            row["rank"] = index

        selected_deep = [
            row["symbol"]
            for row in rows
            if not self._has_blocking_risk(row)
        ][: int(self.config.universe_setting("max_symbols_for_deep_analysis", 30))]
        selected_full = selected_deep[: int(self.config.universe_setting("max_symbols_for_trade_ideas", 15))]
        payload = {
            "generated_at": utc_now().isoformat(),
            "mode": mode,
            "selected_for_deep_analysis": selected_deep,
            "selected_for_full_agent_analysis": selected_full,
            "candidates": rows,
        }
        self.store.save_json(
            Path("data") / "processed" / "candidates" / f"universe_ranked_candidates_{mode}.json",
            payload,
        )
        self.store.save_json(
            Path("data") / "processed" / "candidates" / "universe_ranked_candidates.json",
            payload,
        )
        self._save_legacy_universe_view(selected_deep, rows)
        return rows

    def select(self, seed_symbols: list[str] | None = None, mode: str = "intraday") -> UniverseSelection:
        ranked_payload = self._load_ranked_payload(mode)
        ranked_symbols = ranked_payload.get("selected_for_deep_analysis") or []
        if ranked_symbols:
            return UniverseSelection(
                symbols=list(dict.fromkeys([*(seed_symbols or []), *ranked_symbols])),
                records=ranked_payload.get("candidates", []),
            )

        universe = self._load_or_discover_universe()
        records = [row for row in universe.get("records", []) if row.get("accepted")]
        rows = self._rough_filter(records, mode="intraday")
        max_symbols = int(self.config.universe_setting("max_symbols_for_deep_analysis", 30))
        symbols: list[str] = []
        for symbol in seed_symbols or self.config.symbols:
            self._append_unique(symbols, normalize_symbol(symbol), max_symbols)
        for row in rows:
            self._append_unique(symbols, str(row["symbol"]), max_symbols)
        self._save_legacy_universe_view(symbols, rows)
        return UniverseSelection(symbols=symbols, records=rows)

    def selected_symbols_for_mode(self, mode: str = "intraday") -> list[str]:
        self.rank_candidates(mode=mode)
        payload = self._load_ranked_payload(mode)
        return [str(symbol) for symbol in payload.get("selected_for_deep_analysis", [])]

    def _load_ranked_payload(self, mode: str) -> dict[str, Any]:
        mode_payload = self.store.read_json(
            Path("data") / "processed" / "candidates" / f"universe_ranked_candidates_{mode}.json"
        ) or {}
        if mode_payload:
            return mode_payload
        latest_payload = self.store.read_json(
            Path("data") / "processed" / "candidates" / "universe_ranked_candidates.json"
        ) or {}
        if latest_payload.get("mode") == mode:
            return latest_payload
        return {}

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
                "symbol": symbol,
                "opportunity_score": 0.0,
                "risk_flags": ["insufficient_candles"],
            }

        enriched = enrich_ohlcv(primary)
        last = enriched.iloc[-1]
        close = float(last["close"])
        atr = float(last["atr14"]) if pd.notna(last["atr14"]) else 0.0
        atr_percent = (atr / close * 100) if close else 0.0
        volume_anomaly = volume_ratio(primary, 20) or 0.0
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
        volume_score = clamp(volume_anomaly * 35)
        catalyst_score = self._news_bonus(symbol)
        opportunity_score = clamp(
            trend_score * 0.34
            + liquidity_score * 0.18
            + volume_score * 0.2
            + volatility_score * 0.16
            + clamp((rs_btc or 0) * 5 + 50) * 0.08
            + catalyst_score
        )

        risk_flags = self._risk_flags(
            ticker_row,
            recent_quote_volume,
            atr_percent,
            volume_anomaly,
            range_expansion,
            mode,
        )
        if abs(float(last.get("close", close)) - float(last.get("ema20", close))) > 2.5 * atr and atr > 0:
            risk_flags.append("extended_from_ema20")
            opportunity_score -= 8
        if ticker_row.get("spread_pct") is None:
            risk_flags.append("spread_unavailable")
        return {
            "symbol": symbol,
            "mode": mode,
            "change_1h": round(change_1h, 2) if change_1h is not None else None,
            "change_4h": round(change_4h, 2) if change_4h is not None else None,
            "change_24h": round(change_24h, 2) if change_24h is not None else None,
            "volume_anomaly": round(volume_anomaly, 2),
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
            "news_mentions": self._news_mentions(symbol),
            "risk_flags": sorted(set(risk_flags)),
        }

    def _rough_filter(self, records: list[dict[str, Any]], mode: str) -> list[dict[str, Any]]:
        min_volume = float(self.config.universe_setting("min_24h_quote_volume", 2_000_000))
        max_spread = float(self.config.universe_setting("max_spread_pct", 0.35))
        preferred = {normalize_symbol(symbol) for symbol in self.config.universe_setting("preferred_symbols", []) or self.config.symbols}
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
        limit = int(self.config.universe_setting("max_symbols_for_rank_scan", 90))
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

    def _build_exchange(self, market_type: str = "spot") -> Any:
        try:
            import ccxt
        except ImportError as exc:
            raise RuntimeError("ccxt is not installed. Run `pip install -r requirements.txt` first.") from exc

        exchange_class = getattr(ccxt, self.config.exchange_id)
        default_type = "future" if market_type in {"futures", "perpetual", "swap"} else "spot"
        return exchange_class({"enableRateLimit": True, "options": {"defaultType": default_type}})

    def _load_or_discover_universe(self) -> dict[str, Any]:
        payload = self.store.read_json(Path("data") / "processed" / "symbol_universe.json")
        if payload:
            return payload
        return self.discover_broad_universe()

    def _fetch_symbol_frames(
        self, exchange: Any, symbol: str, timeframes: list[str], limit: int = 120
    ) -> dict[str, pd.DataFrame]:
        frames: dict[str, pd.DataFrame] = {}
        for timeframe in timeframes:
            rows = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
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
    def _append_unique(items: list[str], symbol: str, max_items: int) -> None:
        if len(items) >= max_items:
            return
        if symbol not in items:
            items.append(symbol)

    @staticmethod
    def _quote_volume(ticker: dict[str, Any]) -> float:
        for key in ("quoteVolume", "quote_volume"):
            value = ticker.get(key)
            if value is not None:
                return BinanceUniverseCollector._to_float(value) or 0.0
        info = ticker.get("info") or {}
        for key in ("quoteVolume", "quote_volume"):
            value = info.get(key)
            if value is not None:
                return BinanceUniverseCollector._to_float(value) or 0.0
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
        bid = BinanceUniverseCollector._to_float(ticker.get("bid"))
        ask = BinanceUniverseCollector._to_float(ticker.get("ask"))
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

    def _risk_flags(
        self,
        row: dict[str, Any],
        recent_quote_volume: float,
        atr_percent: float,
        volume_anomaly: float,
        range_expansion: float,
        mode: str,
    ) -> list[str]:
        flags: list[str] = []
        if float(row.get("quote_volume") or 0) < float(self.config.universe_setting("min_24h_quote_volume", 2_000_000)):
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
        if volume_anomaly < 0.5:
            flags.append("quiet_volume")
        if range_expansion >= 1.8:
            flags.append("range_expansion")
        return flags

    def _min_atr_percent(self, mode: str) -> float:
        payload = self.config.universe_setting("min_atr_percent", 0.35)
        if isinstance(payload, dict):
            return float(payload.get(mode, payload.get("intraday", 0.35)))
        return float(payload)

    def _has_blocking_risk(self, row: dict[str, Any]) -> bool:
        flags = set(row.get("risk_flags", []))
        return bool({"low_24h_quote_volume", "wide_spread", "insufficient_candles"} & flags)

    def _news_mentions(self, symbol: str) -> int:
        payload = self.store.read_json(Path("data") / "raw" / "news" / "rss_latest.json") or {}
        ticker = symbol.split("/")[0].upper()
        count = 0
        for item in payload.get("items", []) or []:
            if ticker in [str(value).upper() for value in item.get("detected_symbols", [])]:
                count += 1
        return count

    def _news_bonus(self, symbol: str) -> float:
        return min(self._news_mentions(symbol) * 2.5, 8.0)

    def _save_legacy_universe_view(self, symbols: list[str], rows: list[dict[str, Any]]) -> None:
        self.store.save_json(
            Path("data") / "processed" / "market_summary" / "universe_latest.json",
            {
                "generated_at": utc_now().isoformat(),
                "symbols": symbols,
                "liquid_symbols": [row["symbol"] for row in rows[:20]],
                "lower_volume_symbols": [row["symbol"] for row in rows[20:]],
                "records": rows,
                "failed": {},
                "note": "Compatibility view. Full broad universe is in data/processed/symbol_universe.json.",
            },
        )
