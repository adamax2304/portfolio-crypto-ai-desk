"""Aggregate per-exchange universes into a unified discovery + ranking surface.

Each enabled exchange (Binance, Bybit, MEXC) contributes its own discovery
result. The aggregator:

1. Saves the per-exchange records under ``data/processed/universe/<exchange>.json``.
2. Builds a canonical map ``exchange_symbol_map.json`` so every base asset
   knows which venues list it.
3. Writes ``symbol_universe.json`` (canonical accepted symbols with the
   exchanges that list each one).
4. Ranks candidates per-exchange and fuses into a single
   ``universe_ranked_candidates.json``.

Falls back gracefully if a venue is unreachable: failures are logged into the
payload so reports can show coverage gaps without crashing.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from src.config import ProjectConfig
from src.data_collectors.exchange_universe_collector import (
    ExchangeUniverseCollector,
    ExchangeUniverseResult,
)
from src.logger import get_logger
from src.storage.file_store import FileStore
from src.utils.symbols import normalize_symbol, symbol_to_ticker
from src.utils.time import utc_now


class MultiExchangeUniverseCollector:
    def __init__(self, config: ProjectConfig, store: FileStore):
        self.config = config
        self.store = store
        self.logger = get_logger(self.__class__.__name__)

    @property
    def enabled_exchanges(self) -> list[str]:
        return [
            exchange
            for exchange in self.config.enabled_exchanges
            if self.config.exchange_enabled(exchange)
        ]

    def discover(self, market_type: str | None = None) -> dict[str, Any]:
        per_exchange: dict[str, ExchangeUniverseResult] = {}
        for exchange in self.enabled_exchanges:
            collector = ExchangeUniverseCollector(exchange, self.config, self.store)
            result = collector.discover(market_type=market_type)
            per_exchange[exchange] = result
            self.store.save_json(
                Path("data") / "processed" / "universe" / f"{exchange}.json",
                {
                    "generated_at": utc_now().isoformat(),
                    "exchange": exchange,
                    "symbols": result.symbols,
                    "records": result.records[:1000],
                    "excluded": result.excluded[:500],
                    "failed": result.failed,
                    "counts": result.counts,
                },
            )

        symbol_map = self._build_symbol_map(per_exchange)
        all_symbols = sorted(symbol_map.keys())
        universe_payload = {
            "generated_at": utc_now().isoformat(),
            "enabled_exchanges": self.enabled_exchanges,
            "anchor_exchange": self.config.anchor_exchange,
            "symbols": all_symbols,
            "symbol_count": len(all_symbols),
            "exchanges_by_symbol": symbol_map,
            "per_exchange_counts": {
                exchange: result.counts for exchange, result in per_exchange.items()
            },
            "failures": {
                exchange: result.failed for exchange, result in per_exchange.items() if result.failed
            },
            "note": "Canonical multi-exchange universe. Each symbol lists exchanges that carry it.",
        }
        self.store.save_json(Path("data") / "processed" / "symbol_universe.json", universe_payload)
        self.store.save_json(
            Path("data") / "processed" / "exchange_symbol_map.json",
            {
                "generated_at": utc_now().isoformat(),
                "by_symbol": symbol_map,
                "by_ticker": self._invert_to_ticker(symbol_map),
            },
        )
        return universe_payload

    def rank_candidates(
        self,
        mode: str = "intraday",
        refresh: bool = False,
        discovery: bool = False,
    ) -> list[dict[str, Any]]:
        if refresh:
            self.discover()
        per_exchange: dict[str, list[dict[str, Any]]] = {}
        for exchange in self.enabled_exchanges:
            payload = self.store.read_json(
                Path("data") / "processed" / "universe" / f"{exchange}.json"
            ) or {}
            records = payload.get("records", [])
            if not records:
                self.logger.info("No cached %s universe; running discover() lazily.", exchange)
                discover_result = ExchangeUniverseCollector(exchange, self.config, self.store).discover()
                records = discover_result.records
            collector = ExchangeUniverseCollector(exchange, self.config, self.store)
            per_exchange[exchange] = collector.rank_candidates(records, mode=mode, discovery=discovery)
            suffix = f"{mode}_discovery" if discovery else mode
            self.store.save_json(
                Path("data") / "processed" / "candidates" / f"ranked_{exchange}_{suffix}.json",
                {
                    "generated_at": utc_now().isoformat(),
                    "exchange": exchange,
                    "mode": mode,
                    "discovery": discovery,
                    "candidates": per_exchange[exchange],
                },
            )

        fused = self._fuse_candidates(per_exchange)
        fused.sort(key=lambda row: row.get("opportunity_score", 0.0), reverse=True)
        for index, row in enumerate(fused, start=1):
            row["rank"] = index

        setting_fn = self.config.universe_setting_for_discovery if discovery else self.config.universe_setting
        deep_n = int(setting_fn("max_symbols_for_deep_analysis", 30))
        full_n = int(setting_fn("max_symbols_for_trade_ideas", 15))
        # Prefer anchor-listed symbols so the trade-idea pipeline (which loads
        # anchor OHLCV cache) has data. Non-anchor symbols still surface but
        # only after the anchor list is filled.
        candidates_clean = [row for row in fused if not self._blocking_risk(row)]
        anchor_listed = [row for row in candidates_clean if row.get("anchor_listed")]
        non_anchor = [row for row in candidates_clean if not row.get("anchor_listed")]
        selected_deep = [row["symbol"] for row in anchor_listed[:deep_n]]
        remaining = max(deep_n - len(selected_deep), 0)
        selected_deep.extend(row["symbol"] for row in non_anchor[:remaining])
        # PART 21: reserve extra deep slots for the biggest losers (prime
        # shorts) that opportunity_score buried below the cut.
        short_reserve_n = int(setting_fn("max_short_reserved_candidates", 8))
        selected_deep = self._reserve_short_slots(
            selected_deep, anchor_listed, short_reserve_n, cap=deep_n + short_reserve_n
        )
        # Always include BTC + ETH so MarketRegimeAgent has data to read.
        for must_have in ("BTC/USDT", "ETH/USDT"):
            if must_have not in selected_deep:
                selected_deep.insert(0, must_have)
        selected_full = selected_deep[:full_n]
        payload = {
            "generated_at": utc_now().isoformat(),
            "mode": mode,
            "discovery": discovery,
            "enabled_exchanges": self.enabled_exchanges,
            "selected_for_deep_analysis": selected_deep,
            "selected_for_full_agent_analysis": selected_full,
            "candidates": fused,
            "candidate_funnel": self._funnel_stats(per_exchange, fused, selected_deep, selected_full),
        }
        suffix = f"{mode}_discovery" if discovery else mode
        self.store.save_json(
            Path("data") / "processed" / "candidates" / f"universe_ranked_candidates_{suffix}.json",
            payload,
        )
        # Only overwrite the default cache when not in discovery mode so the
        # standard pipeline always has a clean non-discovery baseline to read.
        if not discovery:
            self.store.save_json(
                Path("data") / "processed" / "candidates" / "universe_ranked_candidates.json",
                payload,
            )
        self._save_legacy_universe_view(selected_deep, fused)
        return fused

    @staticmethod
    def _blocking_risk(row: dict[str, Any]) -> bool:
        flags = set(row.get("risk_flags", []))
        return bool({"low_24h_quote_volume", "wide_spread", "insufficient_candles"} & flags)

    @staticmethod
    def _reserve_short_slots(
        selected_deep: list[str],
        anchor_listed: list[dict[str, Any]],
        reserve_n: int,
        cap: int,
    ) -> list[str]:
        """PART 21 — guarantee the strongest SHORT candidates reach deep analysis.

        ``opportunity_score`` rewards rising coins, so in a selloff the biggest
        losers are pushed below the deep cut and never get analysed (and never
        get their MEXC/Bybit derivatives fallback fetched). We append up to
        ``reserve_n`` anchor-listed symbols that are actually falling
        (``change_24h < 0``), ranked most-negative first, without exceeding
        ``cap``. Pure / deterministic so it is unit-testable.
        """

        if reserve_n <= 0:
            return selected_deep
        selected = list(selected_deep)
        selected_set = set(selected)

        def _short_rank(row: dict[str, Any]) -> float:
            chg = row.get("change_24h")
            rs = row.get("relative_strength_btc")
            return (float(chg) if chg is not None else 0.0) + (
                float(rs) if rs is not None else 0.0
            )

        fallers = sorted(
            (
                row
                for row in anchor_listed
                if row.get("symbol") not in selected_set
                and (row.get("change_24h") or 0.0) < 0
            ),
            key=_short_rank,
        )
        for row in fallers[:reserve_n]:
            if len(selected) >= cap:
                break
            symbol = row.get("symbol")
            if symbol and symbol not in selected_set:
                selected.append(symbol)
                selected_set.add(symbol)
        return selected

    def _fuse_candidates(self, per_exchange: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
        by_symbol: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
        for exchange, rows in per_exchange.items():
            for row in rows:
                symbol = str(row.get("symbol"))
                by_symbol[symbol][exchange] = row
        anchor = self.config.anchor_exchange
        high_risk = self.config.high_risk_exchanges
        fused: list[dict[str, Any]] = []
        for symbol, per_venue in by_symbol.items():
            ranked_venues = sorted(
                per_venue.items(),
                key=lambda pair: (pair[0] != anchor, -float(pair[1].get("opportunity_score") or 0)),
            )
            best_exchange, best_row = ranked_venues[0]
            # Weighted opportunity score across exchanges.
            total_weight = 0.0
            total_score = 0.0
            for exchange, row in per_venue.items():
                weight = self.config.exchange_weight(exchange)
                total_weight += weight
                total_score += float(row.get("opportunity_score") or 0.0) * weight
            fused_score = total_score / total_weight if total_weight else float(best_row.get("opportunity_score") or 0)
            exchanges_present = sorted(per_venue.keys())
            only_high_risk = all(exchange in high_risk for exchange in exchanges_present)
            risk_flags = sorted(
                {
                    flag
                    for row in per_venue.values()
                    for flag in row.get("risk_flags", [])
                }
            )
            if only_high_risk:
                risk_flags.append("mexc_only")
            fused.append(
                {
                    "symbol": symbol,
                    "ticker": symbol_to_ticker(symbol),
                    "exchanges": exchanges_present,
                    "best_exchange": best_exchange,
                    "anchor_listed": anchor in per_venue,
                    "high_risk_only": only_high_risk,
                    "opportunity_score": round(fused_score, 1),
                    "per_exchange": per_venue,
                    "change_1h": best_row.get("change_1h"),
                    "change_4h": best_row.get("change_4h"),
                    "change_24h": best_row.get("change_24h"),
                    "volume_anomaly": best_row.get("volume_anomaly"),
                    "atr_percent": best_row.get("atr_percent"),
                    "relative_strength_btc": best_row.get("relative_strength_btc"),
                    "trend_score": best_row.get("trend_score"),
                    "liquidity_score": best_row.get("liquidity_score"),
                    "risk_flags": risk_flags,
                }
            )
        return fused

    def _funnel_stats(
        self,
        per_exchange: dict[str, list[dict[str, Any]]],
        fused: list[dict[str, Any]],
        deep: list[str],
        full: list[str],
    ) -> dict[str, Any]:
        per_exchange_scanned = {exchange: len(rows) for exchange, rows in per_exchange.items()}
        passed_liquidity = sum(
            1
            for row in fused
            if "low_24h_quote_volume" not in row.get("risk_flags", [])
            and "wide_spread" not in row.get("risk_flags", [])
        )
        passed_momentum = sum(
            1
            for row in fused
            if not {"insufficient_candles", "quiet_volume"} & set(row.get("risk_flags", []))
        )
        return {
            "per_exchange_scanned": per_exchange_scanned,
            "after_liquidity_filter": passed_liquidity,
            "after_momentum_filter": passed_momentum,
            "fused_candidates": len(fused),
            "selected_for_deep_analysis": len(deep),
            "selected_for_full_agent_analysis": len(full),
        }

    @staticmethod
    def _build_symbol_map(per_exchange: dict[str, ExchangeUniverseResult]) -> dict[str, list[str]]:
        symbol_map: dict[str, list[str]] = defaultdict(list)
        for exchange, result in per_exchange.items():
            for symbol in result.symbols:
                canonical = normalize_symbol(symbol)
                if exchange not in symbol_map[canonical]:
                    symbol_map[canonical].append(exchange)
        return {symbol: sorted(exchanges) for symbol, exchanges in sorted(symbol_map.items())}

    @staticmethod
    def _invert_to_ticker(symbol_map: dict[str, list[str]]) -> dict[str, list[str]]:
        out: dict[str, list[str]] = defaultdict(list)
        for symbol, exchanges in symbol_map.items():
            ticker = symbol_to_ticker(symbol)
            for exchange in exchanges:
                if exchange not in out[ticker]:
                    out[ticker].append(exchange)
        return {ticker: sorted(exchanges) for ticker, exchanges in sorted(out.items())}

    def _save_legacy_universe_view(self, symbols: list[str], rows: list[dict[str, Any]]) -> None:
        # Keep backward compat for existing Supervisor code that reads universe_latest.json.
        self.store.save_json(
            Path("data") / "processed" / "market_summary" / "universe_latest.json",
            {
                "generated_at": utc_now().isoformat(),
                "symbols": symbols,
                "liquid_symbols": [row["symbol"] for row in rows[:20]],
                "lower_volume_symbols": [row["symbol"] for row in rows[20:]],
                "records": rows,
                "failed": {},
                "note": "Multi-exchange fused universe (compat view).",
            },
        )
