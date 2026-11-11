from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
from typing import Any

from src.agents.catalyst_agent import CatalystAgent
from src.agents.coverage_audit_agent import CoverageAuditAgent
from src.agents.critic_agent import CriticAgent
from src.agents.crowd_attention_agent import CrowdAttentionAgent
from src.agents.crowd_leader_agent import CrowdLeaderAgent
from src.agents.derivatives_agent import DerivativesAgent
from src.agents.exchange_fusion_agent import ExchangeFusionAgent
from src.agents.macro_geopolitics_agent import MacroGeopoliticsAgent
from src.agents.market_regime_agent import MarketRegimeAgent
from src.agents.momentum_scanner_agent import MomentumScannerAgent
from src.agents.multi_exchange_derivatives_agent import MultiExchangeDerivativesAgent
from src.agents.narrative_agent import NarrativeAgent
from src.agents.news_agent import NewsAgent
from src.agents.risk_agent import RiskAgent
from src.agents.review_agent import ReviewAgent
from src.agents.scoring_agent import ScoringAgent
from src.agents.social_attention_agent import SocialAttentionAgent
from src.agents.technical_setup_agent import TechnicalSetupAgent
from src.agents.trade_idea_agent import TradeIdeaAgent
from src.config import ProjectConfig
from src.diagnostics import stage_timer as _timing
from src.data_collectors.binance_derivatives_collector import BinanceDerivativesCollector
from src.data_collectors.binance_collector import BinanceOHLCVCollector, CollectionSummary
from src.data_collectors.binance_universe_collector import BinanceUniverseCollector
from src.data_collectors.bybit_collector import BybitOHLCVCollector
from src.data_collectors.bybit_derivatives_collector import BybitDerivativesCollector
from src.data_collectors.mexc_collector import MEXCOHLCVCollector
from src.data_collectors.exchange_ohlcv_collector import ExchangeCollectionSummary
from src.data_collectors.manual_events_loader import load_manual_events
from src.data_collectors.manual_notes_loader import (
    load_manual_narrative_notes,
    load_manual_social_notes,
)
from src.data_collectors.news_trader_bridge import NewsTraderBridge
from src.data_collectors.multi_exchange_derivatives_collector import MultiExchangeDerivativesCollector
from src.data_collectors.multi_exchange_universe_collector import MultiExchangeUniverseCollector
from src.data_collectors.rss_news_collector import RSSNewsCollector
from src.data_collectors.social_collector import SocialCollector
from src.reports.report_builder import ReportBuilder
from src.reports.charts import ChartBuilder
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore
from src.utils.time import utc_now
from src.utils.validation import model_to_dict


def should_suppress_setup_telegram(asset_class: str, mode: str) -> bool:
    """Whether an immediate Telegram SETUP alert should be suppressed.

    2026-08-31 operator-noise policy: setup/watchlist ideas are journal and
    dashboard data, not phone alerts. Telegram is reserved for live-routed
    entries/fills/closes plus critical health/watchdog notices.
    """
    return True


class Supervisor:
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.file_store = FileStore(config)
        self.db = SQLiteStore(config.db_path)
        self.file_store.ensure_directories()
        self.db.init_db()

    def update_data(
        self, symbols: list[str] | None = None, timeframes: list[str] | None = None
    ) -> CollectionSummary:
        selected_symbols = self._resolve_universe(symbols)

        # ── Parallel fetch (P1 timeout fix, 2026-06-07) ────────────────────
        # The independent OHLCV + derivatives network fetches used to run
        # sequentially (~40 min total), pushing daytime cycles past the 2700 s
        # report timeout. They write distinct cache files and share no mutable
        # state, so we run them with BOUNDED concurrency (max_workers=4). This
        # changes ONLY fetch scheduling — identical symbols, identical data,
        # identical downstream agents/scoring. SQLite writes (save_symbols,
        # news) stay on the main thread. One slow/broken source degrades that
        # source only (logged), never blocking the others or the report.
        # Two waves so the OHLCV→fetched_symbols dependency is preserved.

        # Wave 1 — OHLCV (Binance anchor + enabled secondaries), concurrent.
        ohlcv_tasks: dict[str, Any] = {}
        ohlcv_tasks["binance"] = lambda: BinanceOHLCVCollector(self.config, self.file_store).fetch(
            symbols=selected_symbols, timeframes=timeframes
        )
        for exchange, collector_cls in (("bybit", BybitOHLCVCollector), ("mexc", MEXCOHLCVCollector)):
            if exchange == self.config.exchange_id or not self.config.exchange_enabled(exchange):
                continue
            if exchange not in self.config.enabled_exchanges:
                continue
            ohlcv_tasks[exchange] = (
                lambda cls=collector_cls: cls(self.config, self.file_store).fetch(
                    symbols=selected_symbols, timeframes=timeframes
                )
            )
        ohlcv_results = self._parallel_fetch(
            ohlcv_tasks, label_prefix="ohlcv", symbols=len(selected_symbols)
        )

        summary = ohlcv_results.get("binance")
        if summary is None:
            # Binance anchor failed — degrade gracefully; secondary OHLCV (if any)
            # still feeds the report via _load_market_data fallback.
            self._log_secondary_failure(
                "binance OHLCV anchor", RuntimeError("anchor fetch returned no summary")
            )
            summary = CollectionSummary(
                exchange=self.config.exchange_id, failed={"__exchange__": "anchor fetch failed"}
            )
        fetched_symbols = sorted({item.split(" ")[0] for item in summary.fetched})
        self.db.save_symbols(fetched_symbols, self.config.exchange_id)

        secondary_summaries: dict[str, ExchangeCollectionSummary] = {}
        for exchange in ("bybit", "mexc"):
            if exchange not in ohlcv_tasks:
                continue
            res = ohlcv_results.get(exchange)
            secondary_summaries[exchange] = res if res is not None else ExchangeCollectionSummary(
                exchange=exchange, failed={"__exchange__": "fetch failed/timed out"}
            )

        # Wave 2 — derivatives collectors, concurrent.
        derivatives_symbols = symbols or fetched_symbols or selected_symbols
        deriv_tasks: dict[str, Any] = {
            "binance": lambda: BinanceDerivativesCollector(self.config, self.file_store).fetch(
                symbols=derivatives_symbols
            ),
            "multi": lambda: MultiExchangeDerivativesCollector(self.config, self.file_store).fetch(
                symbols=derivatives_symbols
            ),
            "bybit_history": lambda: BybitDerivativesCollector(self.config, self.file_store).fetch(
                symbols=derivatives_symbols
            ),
        }
        deriv_results = self._parallel_fetch(
            deriv_tasks, label_prefix="deriv", symbols=len(derivatives_symbols)
        )
        derivative_summary = deriv_results.get("binance")
        if derivative_summary is None:
            derivative_summary = CollectionSummary(
                exchange=self.config.exchange_id, failed={"__exchange__": "fetch failed/timed out"}
            )
        multi_derivatives_summary = deriv_results.get("multi")
        if multi_derivatives_summary is None:
            multi_derivatives_summary = ExchangeCollectionSummary(
                exchange="multi", failed={"__exchange__": "fetch failed/timed out"}
            )
        bybit_derivatives_summary = deriv_results.get("bybit_history")

        # Persist every derivatives fetch immediately.  Previously only the
        # daily-report path archived Binance plus a malformed ``multi`` row,
        # while the richer Bybit history was discarded after JSON caching.
        # This is best-effort and cannot interrupt OHLCV/news/report work.
        try:
            from src.data_collectors.derivatives_archive import archive_derivatives_records
            archive_derivatives_records(
                self.db, getattr(derivative_summary, "records", {}) or {}, exchange="binance",
                source_file="data/raw/open_interest/binance_futures_latest.json",
            )
            archive_derivatives_records(
                self.db, getattr(multi_derivatives_summary, "records", {}) or {}, exchange="multi",
                source_file="data/raw/open_interest/multi_exchange_derivatives_latest.json",
            )
            if bybit_derivatives_summary is not None:
                archive_derivatives_records(
                    self.db, getattr(bybit_derivatives_summary, "records", {}) or {}, exchange="bybit",
                    source_file="data/raw/open_interest/bybit_derivatives_latest.json",
                )
        except Exception as exc:
            self._log_secondary_failure("derivatives point-in-time archive", exc)

        # News (writes to SQLite) + social stay on the MAIN thread.
        with _timing.stage("news_rss"):
            news_summary = RSSNewsCollector(self.config, self.file_store, self.db).fetch()
        with _timing.stage("social"):
            social_summary = SocialCollector(self.config, self.file_store).fetch()
        manual_events = load_manual_events(self.config.root / "data" / "raw" / "events" / "manual_events.yaml")
        saved_events = self.db.save_events(manual_events)
        self.file_store.save_json(
            Path("data") / "processed" / "market_summary" / "last_update.json",
            {
                "run_at": utc_now().isoformat(),
                "exchange": summary.exchange,
                "configured_symbols": self.config.symbols,
                "active_symbols": selected_symbols,
                "dynamic_universe_enabled": bool(self.config.universe_setting("enabled", False)) and symbols is None,
                "enabled_exchanges": self.config.enabled_exchanges,
                "fetched": summary.fetched,
                "failed": summary.failed,
                "secondary_exchanges": {
                    exchange: {
                        "fetched": s.fetched,
                        "failed": s.failed,
                    }
                    for exchange, s in secondary_summaries.items()
                },
                "derivatives_fetched": derivative_summary.fetched,
                "derivatives_failed": derivative_summary.failed,
                "multi_exchange_derivatives_fetched": multi_derivatives_summary.fetched,
                "multi_exchange_derivatives_failed": multi_derivatives_summary.failed,
                "bybit_derivatives_fetched": bybit_derivatives_summary.fetched if bybit_derivatives_summary else [],
                "bybit_derivatives_failed": bybit_derivatives_summary.failed if bybit_derivatives_summary else {},
                "news_sources": news_summary.fetched_sources,
                "news_failures": news_summary.failed_sources,
                "social_sources": social_summary.fetched_sources,
                "social_failures": social_summary.failed_sources,
                "social_mentions": len(social_summary.mentions),
                "manual_events_saved": saved_events,
            },
        )
        return summary

    def _parallel_fetch(
        self,
        tasks: dict[str, Any],
        *,
        label_prefix: str,
        symbols: int | None = None,
        max_workers: int = 4,
    ) -> dict[str, Any]:
        """Run independent network-fetch thunks concurrently with bounded workers.

        Each value in ``tasks`` is a zero-arg callable returning its collector
        summary. Returns ``{name: result_or_None}``; a source that raises or
        exceeds the per-source wall-clock budget yields ``None`` and is logged —
        it degrades that source ONLY and never blocks the others. Total wall-time
        ≈ the slowest single source instead of the sum.

        Safety: thunks must do pure network→file work (no SQLite writes — those
        stay on the main thread). Each collector writes its own distinct cache
        path, so concurrent file writes do not collide. Per-source budget is
        ``report_setting('fetch_source_timeout_s', 600)``; collectors are also
        internally bounded by their ccxt/HTTP request timeouts. Per-source timing
        is recorded in the diagnostics log via ``stage_timer``.
        """
        results: dict[str, Any] = {name: None for name in tasks}
        if not tasks:
            return results
        try:
            timeout_s = float(self.config.report_setting("fetch_source_timeout_s", 600))
        except Exception:
            timeout_s = 600.0
        workers = max(1, min(int(max_workers), len(tasks)))

        def _runner(name: str, fn):
            with _timing.stage(f"{label_prefix}_{name}", symbols=symbols):
                return fn()

        with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="ccd-fetch") as pool:
            futures = {pool.submit(_runner, name, fn): name for name, fn in tasks.items()}
            for fut, name in futures.items():
                try:
                    results[name] = fut.result(timeout=timeout_s)
                except Exception as exc:  # noqa: BLE001 - degrade this source only
                    _timing.mark(
                        f"SOURCE_FAIL {label_prefix}_{name}: {type(exc).__name__}: {exc}"
                    )
                    self._log_secondary_failure(f"{label_prefix} {name}", exc)
                    results[name] = None
        return results

    def update_universe(self, market_type: str | None = None) -> dict[str, Any]:
        # Prefer multi-exchange aggregator when more than one exchange is on.
        enabled = self.config.enabled_exchanges
        if len(enabled) > 1:
            return MultiExchangeUniverseCollector(self.config, self.file_store).discover(
                market_type=market_type
            )
        return BinanceUniverseCollector(self.config, self.file_store).discover_broad_universe(
            market_type=market_type
        )

    def rank_universe_candidates(
        self, mode: str = "intraday", refresh_universe: bool = False, discovery: bool = False
    ) -> list[dict[str, Any]]:
        enabled = self.config.enabled_exchanges
        if len(enabled) > 1:
            return MultiExchangeUniverseCollector(self.config, self.file_store).rank_candidates(
                mode=mode,
                refresh=refresh_universe,
                discovery=discovery,
            )
        return BinanceUniverseCollector(self.config, self.file_store).rank_candidates(
            mode=mode,
            refresh=refresh_universe,
        )

    def exchange_status(self) -> dict[str, Any]:
        per: dict[str, Any] = {}
        latest = self.file_store.read_json(
            Path("data") / "processed" / "market_summary" / "last_update.json"
        ) or {}
        for exchange in self.config.enabled_exchanges:
            universe_payload = self.file_store.read_json(
                Path("data") / "processed" / "universe" / f"{exchange}.json"
            ) or {}
            block: dict[str, Any] = {
                "enabled": self.config.exchange_enabled(exchange),
                "role": self.config.exchange_role(exchange),
                "ccxt_id": self.config.exchange_ccxt_id(exchange),
                "trust": self.config.exchange_trust(exchange),
                "weight": self.config.exchange_weight(exchange),
                "high_risk": exchange in self.config.high_risk_exchanges,
                "universe_symbols": len(universe_payload.get("symbols") or []),
                "universe_generated_at": universe_payload.get("generated_at"),
                "universe_failed": universe_payload.get("failed", {}),
            }
            if exchange == self.config.exchange_id:
                block["ohlcv_fetched"] = len(latest.get("fetched", []))
                block["ohlcv_failed"] = latest.get("failed", {})
            else:
                secondary = (latest.get("secondary_exchanges") or {}).get(exchange) or {}
                block["ohlcv_fetched"] = len(secondary.get("fetched", []) or [])
                block["ohlcv_failed"] = secondary.get("failed", {})
            per[exchange] = block
        return {
            "anchor_exchange": self.config.anchor_exchange,
            "enabled_exchanges": self.config.enabled_exchanges,
            "last_update_at": latest.get("run_at"),
            "per_exchange": per,
        }

    def candidate_debug(self, symbol: str, mode: str = "intraday") -> dict[str, Any]:
        symbol = symbol.upper().replace("-", "/").replace("_", "/")
        if "/" not in symbol and symbol.endswith("USDT"):
            symbol = f"{symbol[:-4]}/USDT"
        ranked = self.file_store.read_json(
            Path("data") / "processed" / "candidates" / f"universe_ranked_candidates_{mode}.json"
        ) or {}
        candidates = ranked.get("candidates") or []
        match = next((row for row in candidates if str(row.get("symbol")) == symbol), None)
        latest_candidates = self.file_store.read_json(
            Path("data") / "processed" / "candidates" / "latest_candidates.json"
        ) or []
        latest_match = next(
            (item for item in latest_candidates if str(item.get("symbol")) == symbol), None
        )
        per_exchange_universe = {}
        for exchange in self.config.enabled_exchanges:
            payload = self.file_store.read_json(
                Path("data") / "processed" / "universe" / f"{exchange}.json"
            ) or {}
            row = next(
                (item for item in payload.get("records", []) if str(item.get("symbol")) == symbol),
                None,
            )
            per_exchange_universe[exchange] = row
        return {
            "symbol": symbol,
            "mode": mode,
            "ranked_match": match,
            "momentum_candidate": latest_match,
            "per_exchange_universe": per_exchange_universe,
            "in_fused_universe": match is not None,
        }

    def auto_universe_report(
        self, mode: str = "intraday", kind: str = "intraday", discovery: bool = False
    ) -> Path:
        _timing.set_report(kind)
        _timing.mark(f"==== auto_universe_report mode={mode} kind={kind} discovery={discovery} ====")
        enabled = self.config.enabled_exchanges
        with _timing.stage("rank_candidates", exchanges=len(enabled), discovery=discovery):
            if len(enabled) > 1:
                rows = MultiExchangeUniverseCollector(self.config, self.file_store).rank_candidates(
                    mode=mode, refresh=True, discovery=discovery
                )
            else:
                rows = BinanceUniverseCollector(self.config, self.file_store).rank_candidates(
                    mode=mode, refresh=True
                )
        selected = self._selected_ranked_symbols(rows)
        if not selected:
            selected = self.config.symbols
        timeframes = self._mode_timeframes(mode)
        with _timing.stage("update_data", symbols=len(selected), tfs=len(timeframes or [])):
            self.update_data(symbols=selected, timeframes=timeframes)
        with _timing.stage("daily_report", symbols=len(selected)):
            return self.daily_report(symbols=selected, kind=kind, mode=mode)

    def swing_report(self, symbols: list[str] | None = None, discovery: bool = False) -> Path:
        return self.auto_universe_report(mode="swing", kind="swing", discovery=discovery)

    def _load_market_data(self, symbols: list[str] | None = None) -> dict[str, Any]:
        selected = symbols or self._active_symbols_from_cache()
        anchor = self.config.exchange_id
        market_data = self.file_store.load_market_data(
            anchor, selected, self.config.timeframes
        )
        # Fall back to secondary exchanges for symbols missing from anchor cache.
        missing = [symbol for symbol in selected if symbol not in market_data]
        if not missing:
            return market_data
        for exchange in self.config.enabled_exchanges:
            if exchange == anchor or not missing:
                continue
            secondary = self.file_store.load_market_data(
                exchange, missing, self.config.timeframes
            )
            for symbol, frames in secondary.items():
                if symbol not in market_data and frames:
                    market_data[symbol] = frames
            missing = [symbol for symbol in missing if symbol not in market_data]
        return market_data

    def daily_report(
        self,
        symbols: list[str] | None = None,
        kind: str = "daily",
        mode: str = "intraday",
        allow_network_fallback: bool = True,
    ) -> Path:
        with _timing.stage("load_market_data"):
            market_data = self._load_market_data(symbols)
        if not market_data and allow_network_fallback:
            with _timing.stage("update_data_fallback"):
                self.update_data(symbols=symbols)
            market_data = self._load_market_data(symbols)
        if not market_data:
            raise RuntimeError("No market data available. Check network access and watchlist symbols.")

        with _timing.stage("regime"):
            regime = MarketRegimeAgent(self.config, self.file_store, self.db).run(market_data)
        with _timing.stage("momentum_scan", symbols=len(market_data)):
            candidates = MomentumScannerAgent(self.config, self.file_store, self.db).run(
                market_data, symbols=list(market_data.keys())
            )
        derivatives_records = self._load_derivatives_records()
        if not derivatives_records and allow_network_fallback:
            derivatives_records = BinanceDerivativesCollector(self.config, self.file_store).fetch(
                symbols=list(market_data.keys())
            ).records
        # PART 14b — fetch multi-exchange (MEXC/Bybit/OKX) ONLY for symbols
        # whose Binance record is missing or carries an error. This keeps
        # scalp report fast (no extra HTTPs for the 80+ symbols Binance
        # already covers) while still removing the "derivatives data
        # unavailable" rejection for low-cap alts that only list on MEXC.
        fallback_symbols = [
            sym for sym in market_data
            if not derivatives_records.get(sym)
            or derivatives_records.get(sym, {}).get("error")
        ]
        external_records: dict[str, Any] = {}
        if fallback_symbols and allow_network_fallback:
            try:
                external_records = MultiExchangeDerivativesCollector(
                    self.config, self.file_store
                ).fetch(symbols=fallback_symbols).records
            except Exception as exc:
                self._log_secondary_failure("derivatives fallback fetch", exc)
        derivatives = DerivativesAgent(self.config, self.file_store, self.db).run(
            market_data, derivatives_records, external_records=external_records
        )
        # 2026-06-15 catalyst safe-fix PART 2: append-only funding/OI archive.
        # Best-effort write of the snapshots we just fetched for scoring, so a
        # historical time series exists for future replay / funding-cost
        # modelling. NOT read by scoring; failures are swallowed.
        try:
            from src.data_collectors.derivatives_archive import archive_derivatives_records
            archive_derivatives_records(
                self.db, derivatives_records, exchange="binance",
                source_file="data/raw/funding/binance_futures_latest.json",
            )
            if external_records:
                archive_derivatives_records(
                    self.db, external_records, exchange="multi",
                    source_file="multi_exchange_derivatives",
                )
        except Exception as exc:
            self._log_secondary_failure("derivatives archive", exc)
        # Time-window (not latest-100 tail) so a busy feed hour can't hide older-but-recent catalysts.
        # NewsAgent already caps per-symbol ([:8]) and top-N ([:15]) downstream, so the wider window stays
        # prompt-bounded.
        news_rows = self.db.load_news_window(hours=72, limit=3000, asset_class="crypto")
        if not news_rows and allow_network_fallback:
            RSSNewsCollector(self.config, self.file_store, self.db).fetch()
            news_rows = self.db.load_news_window(hours=72, limit=3000, asset_class="crypto")
        news_output = NewsAgent(self.config, self.file_store, self.db).run(news_rows)
        manual_events = load_manual_events(self.config.root / "data" / "raw" / "events" / "manual_events.yaml")
        if manual_events:
            self.db.save_events(manual_events)
        events = self.db.load_events(limit=200)
        catalysts = CatalystAgent(self.config, self.file_store, self.db).run(
            list(market_data.keys()), events, news_output
        )
        narratives = NarrativeAgent(self.config, self.file_store, self.db).run(
            candidates, news_output, catalysts
        )
        social_mentions = self._load_social_mentions()
        if not social_mentions and allow_network_fallback:
            social_mentions = SocialCollector(self.config, self.file_store).fetch().mentions
        social_attention = SocialAttentionAgent(self.config, self.file_store, self.db).run(
            social_mentions, candidates
        )
        crowd_watch = CrowdLeaderAgent(self.config, self.file_store, self.db).run(social_mentions)
        macro = MacroGeopoliticsAgent(self.config, self.file_store, self.db).run(news_output)
        multi_derivatives_records = self._load_multi_exchange_derivatives_records()
        if not multi_derivatives_records and allow_network_fallback:
            multi_derivatives_records = MultiExchangeDerivativesCollector(
                self.config, self.file_store
            ).fetch(symbols=list(market_data.keys())).records
        bybit_history_records = self._load_bybit_derivatives_records()
        if not bybit_history_records and allow_network_fallback:
            try:
                bybit_history_records = BybitDerivativesCollector(self.config, self.file_store).fetch(
                    symbols=list(market_data.keys())
                ).records
            except Exception as exc:
                self._log_secondary_failure("bybit derivatives lazy fetch", exc)
                bybit_history_records = {}
        try:
            from src.data_collectors.derivatives_archive import archive_derivatives_records
            if bybit_history_records:
                archive_derivatives_records(
                    self.db, bybit_history_records, exchange="bybit",
                    source_file="data/raw/open_interest/bybit_derivatives_latest.json",
                )
        except Exception as exc:
            self._log_secondary_failure("bybit derivatives history archive", exc)
        multi_derivatives = MultiExchangeDerivativesAgent(self.config, self.file_store, self.db).run(
            multi_derivatives_records, bybit_history=bybit_history_records
        )
        latest_update = self.file_store.read_json(
            Path("data") / "processed" / "market_summary" / "last_update.json"
        ) or {}
        coverage = CoverageAuditAgent(self.config, self.file_store, self.db).run(
            latest_update,
            market_data,
            derivatives,
            social_attention,
            multi_derivatives_records,
        )
        setup_limit = max(
            int(self.config.report_setting("max_trade_ideas", 5))
            + int(self.config.report_setting("max_watchlist", 10)),
            int(self.config.universe_setting("max_symbols_for_trade_ideas", 15)),
            12,
        )
        with _timing.stage("technical_setups", candidates=len(candidates)):
            setups = TechnicalSetupAgent(self.config, self.file_store, self.db).run(
                candidates, market_data, regime, limit=setup_limit
            )
        risks = RiskAgent(self.config, self.file_store, self.db).run(
            setups, candidates, regime, derivatives, catalysts
        )
        critiques = CriticAgent(self.config, self.file_store, self.db).run(
            setups, candidates, regime, derivatives, catalysts, risks
        )
        # --- Exchange fusion + crowd attention (multi-exchange context) ---
        fused_payload = self.file_store.read_json(
            Path("data") / "processed" / "candidates" / "universe_ranked_candidates.json"
        ) or {}
        fused_candidates = fused_payload.get("candidates") or []
        exchange_symbol_map_payload = self.file_store.read_json(
            Path("data") / "processed" / "exchange_symbol_map.json"
        ) or {}
        exchange_confirmations = ExchangeFusionAgent(self.config, self.file_store, self.db).run(
            fused_candidates, exchange_symbol_map_payload.get("by_symbol", {})
        )
        manual_social = load_manual_social_notes(self.config.root)
        manual_narratives = load_manual_narrative_notes(self.config.root)
        # Pull live Telegram + macro signals from the news_trader project
        # (read-only). Errors degrade gracefully — no news_trader, no crash.
        news_trader_notes: list[dict[str, Any]] = []
        news_trader_pulse: dict[str, Any] = {}
        try:
            bridge = NewsTraderBridge()
            if bridge.available:
                tickers = [c.symbol for c in candidates]
                aggregated = bridge.aggregate(lookback_minutes=240, tickers_of_interest=tickers)
                news_trader_notes = bridge.to_manual_social_notes(aggregated)
                news_trader_pulse = bridge.macro_pulse(lookback_minutes=240)
                self.file_store.save_json(
                    Path("data") / "processed" / "news_trader_bridge_latest.json",
                    {
                        "fetched_at": utc_now().isoformat(),
                        "pulse": news_trader_pulse,
                        "tickers": {
                            ticker: {
                                "mention_count": att.mention_count,
                                "telegram_mention_count": att.telegram_mention_count,
                                "strong_tier_count": att.strong_tier_count,
                                "attention_score": att.attention_score,
                                "net_sentiment": att.net_sentiment,
                                "sources": att.sources,
                                "top_headlines": att.top_headlines,
                                "categories": dict(att.categories),
                            }
                            for ticker, att in aggregated.items()
                        },
                    },
                )
        except Exception as exc:
            self._log_secondary_failure("news_trader bridge", exc)
        # Merge bridge notes into manual_social so CrowdAttentionAgent sees them.
        combined_social = list(manual_social) + list(news_trader_notes)
        crowd_attention = CrowdAttentionAgent(self.config, self.file_store, self.db).run(
            candidates, social_attention, combined_social, derivatives
        )

        with _timing.stage("scoring", setups=len(setups)):
            scores = ScoringAgent(self.config, self.file_store, self.db).run(
                setups,
                candidates,
                regime,
                derivatives,
                catalysts,
                risks,
                critiques,
                narratives,
                exchange_confirmations=exchange_confirmations,
                mode=mode,
            )
        # --- Weekend Mode overlay (safe: no-op when not active or on failure) ---
        weekend_adjustments: dict[str, Any] = {}
        try:
            from src.analysis import weekend_mode as _weekend_mode

            weekend_cfg = _weekend_mode.load_config(self.config.root)
            weekend_status = _weekend_mode.current_status(weekend_cfg, self.config.settings)
            adjustments = _weekend_mode.apply_overlay(
                scores=scores,
                setups=setups,
                status=weekend_status,
                mode=mode,
                candidates=candidates,
            )
            weekend_adjustments = {sym: rec.to_dict() for sym, rec in adjustments.items()}
            if weekend_adjustments:
                self.file_store.save_json(
                    Path("data") / "processed" / "weekend_mode_latest.json",
                    {
                        "status": weekend_status.to_dict(),
                        "adjustments": weekend_adjustments,
                    },
                )
        except Exception as exc:  # pragma: no cover - overlay must never break the pipeline
            self._log_secondary_failure("weekend mode overlay", exc)

        # --- Session Risk Guard (Asia dead-zone 00–06 UTC) — always-on, hour-based ---
        # 2026-07-06 audit: 00–06 UTC is the worst crypto window (avgR +0.04, stop
        # 37.9%); intraday/scalp bleed there (intraday 47% stop) while swing tolerates
        # it. This demotes scalp/intraday out of actionable A/B inside the window so
        # they never register to proposed_signals / never alert. Swing untouched.
        # Pure overlay (same in-place tier mutation the weekend overlay uses, applied
        # BEFORE TradeIdeaAgent + registration); no-op when disabled / out of window /
        # on failure. Never touches direction, TP/SL, sizing, or the live locks.
        session_guard_adjustments: dict[str, Any] = {}
        try:
            from src.analysis import session_guard as _session_guard

            guard_cfg = _session_guard.load_config(self.config.root)
            guard_now = utc_now()
            guard_records = _session_guard.apply_to_scores(
                scores=scores,
                mode=mode,
                asset_class="crypto",
                now_utc=guard_now,
                cfg=guard_cfg,
            )
            session_guard_adjustments = {
                sym: rec.to_dict() for sym, rec in guard_records.items()
            }
            if session_guard_adjustments:
                self.file_store.save_json(
                    Path("data") / "processed" / "session_guard_latest.json",
                    {
                        "decision": _session_guard.guard_decision(
                            guard_now, mode, "crypto", guard_cfg
                        ).to_dict(),
                        "adjustments": session_guard_adjustments,
                    },
                )
        except Exception as exc:  # pragma: no cover - overlay must never break the pipeline
            self._log_secondary_failure("session guard overlay", exc)

        # 2026-06-09 — Crypto Signal Expansion v1.
        # Read-only discovery layer that surfaces additional candidates from
        # RS / catalyst / narrative / volume / short-breakdown sources beyond
        # the top-N setups cap. Does NOT register proposed_signals; the result
        # is rendered as an "Expansion Watchlist" section + persisted to JSON
        # for LLM-packet consumption. See reports/CRYPTO_SIGNAL_EXPANSION_REPORT.md.
        expansion_result = None
        try:
            from src.agents.discovery_expansion_agent import DiscoveryExpansionAgent
            expansion_result = DiscoveryExpansionAgent().run(
                candidates=candidates,
                narratives=narratives,
                catalysts=catalysts,
                derivatives=derivatives,
                top_setup_symbols=[s.get("symbol") if isinstance(s, dict) else getattr(s, "symbol", "")
                                   for s in (setups or [])],
                mode=mode,
            )
            self.file_store.save_json(
                Path("data") / "processed" / "agent_outputs"
                / "crypto_expansion_watchlist.json",
                expansion_result.to_dict(),
            )
        except Exception as exc:  # pragma: no cover - never block the cycle on discovery
            self._log_secondary_failure("discovery expansion", exc)

        trade_idea_agent = TradeIdeaAgent(self.config, self.file_store, self.db)
        ideas = trade_idea_agent.run(
            setups,
            candidates,
            scores,
            regime,
            derivatives,
            catalysts,
            risks,
            critiques,
            narratives,
            exchange_confirmations=exchange_confirmations,
            mode=mode,
        )
        rejected_ideas = trade_idea_agent.last_rejected
        chart_paths = ChartBuilder(self.config).generate_for_ideas(ideas, market_data)
        for idea in ideas:
            if idea.symbol in chart_paths:
                idea.raw["chart_path"] = chart_paths[idea.symbol]

        report_id = f"{kind}-{utc_now().strftime('%Y%m%d-%H%M%S')}"
        self.db.save_trade_ideas(report_id, ideas)
        self.db.save_rejected_ideas(report_id, rejected_ideas)
        # PART 1 fix: register BEFORE alert, so every Telegram alert links to a
        # proposed_signal row. Ideas that fail to register (missing
        # entry/invalidation, etc) are NOT sent to Telegram via this path —
        # this is what was creating untracked legacy alerts.
        registered = self._maybe_register_signals(
            ideas,
            mode=mode,
            report_id=report_id,
            regime_label=getattr(regime, "label", "") or "",
        )
        self._maybe_send_trade_alerts(
            ideas,
            mode=mode,
            report_id=report_id,
            registered_signal_ids=registered,
        )

        builder = ReportBuilder(self.config)
        freshness = self._data_freshness(market_data)
        candidate_funnel = fused_payload.get("candidate_funnel") if fused_payload else None
        exchange_status_payload = self.exchange_status()
        content = builder.build_daily(
            regime,
            candidates,
            ideas,
            freshness,
            derivatives,
            news_output,
            catalysts,
            narratives,
            macro,
            social_attention,
            crowd_watch,
            multi_derivatives,
            coverage,
            exchange_confirmations=exchange_confirmations,
            crowd_attention=crowd_attention,
            rejected_ideas=rejected_ideas,
            candidate_funnel=candidate_funnel,
            exchange_status=exchange_status_payload,
            mode=mode,
            expansion_result=expansion_result,
        )
        report_path = self.file_store.save_markdown(builder.report_path(kind), content)
        context = builder.build_context_for_llm(
            regime,
            candidates,
            ideas,
            freshness,
            derivatives,
            news_output,
            catalysts,
            narratives,
            macro,
            social_attention,
            crowd_watch,
            multi_derivatives,
            coverage,
            exchange_confirmations=exchange_confirmations,
            crowd_attention=crowd_attention,
            rejected_ideas=rejected_ideas,
            candidate_funnel=candidate_funnel,
            exchange_status=exchange_status_payload,
            mode=mode,
            expansion_result=expansion_result,
        )
        self.file_store.save_markdown(
            Path(self.config.report_setting("context_file", "data/processed/context_for_llm.md")),
            context,
        )
        self.file_store.save_json(
            Path("data") / "processed" / "candidates" / "latest_candidates.json",
            [model_to_dict(candidate) for candidate in candidates],
        )
        return report_path

    def intraday_report(self, symbols: list[str] | None = None, update: bool = True) -> Path:
        if update:
            self.update_data(
                symbols=symbols,
                timeframes=["15m", "1h"],
            )
        return self.daily_report(
            symbols=symbols,
            kind="intraday",
            mode="intraday",
            allow_network_fallback=update,
        )

    def scalp_report(self, symbols: list[str] | None = None, discovery: bool = False) -> Path:
        return self.auto_universe_report(mode="scalp", kind="scalp", discovery=discovery)

    def review(self) -> Path:
        market_data = self._load_market_data()
        content = ReviewAgent(self.config, self.file_store, self.db).run(market_data)
        filename = f"{utc_now().strftime('%Y-%m-%d_%H-%M')}_review.md"
        return self.file_store.save_markdown(Path("data") / "reports" / "reviews" / filename, content)

    def ask(self, query: str, refresh: bool | None = None) -> dict[str, Any]:
        """Route a plain-language desk request to the matching local workflow."""
        normalized = query.lower()
        action = self._infer_action(normalized)
        should_refresh = self._should_refresh(normalized) if refresh is None else refresh

        if action == "update-data":
            summary = self.update_data()
            return {
                "action": action,
                "message": f"Fetched {len(summary.fetched)} symbol/timeframe sets.",
                "failed": summary.failed,
            }
        if action == "review":
            path = self.review()
            return {"action": action, "path": str(path)}
        if action == "intraday-report":
            path = self.intraday_report(update=should_refresh)
            return {"action": action, "path": str(path)}
        if action == "scan":
            if should_refresh:
                self.update_data()
            rows = self.scan()
            return {"action": action, "rows": rows[:20]}

        if should_refresh:
            self.update_data()
        path = self.daily_report()
        return {"action": "daily-report", "path": str(path)}

    def scan(self, symbols: list[str] | None = None) -> list[dict[str, Any]]:
        market_data = self._load_market_data(symbols)
        candidates = MomentumScannerAgent(self.config, self.file_store, self.db).run(
            market_data, symbols=list(market_data.keys())
        )
        return [model_to_dict(candidate) for candidate in candidates]

    def status(self) -> dict[str, Any]:
        market_data = self._load_market_data()
        return {
            "project_root": str(self.config.root),
            "exchange": self.config.exchange_id,
            "configured_symbols": len(self.config.symbols),
            "active_symbols": len(self._active_symbols_from_cache()),
            "cached_symbols": len(market_data),
            "db_path": str(self.config.db_path),
            "db_counts": self.db.counts(),
            "latest_data": self._data_freshness(market_data),
            "latest_daily_report": str(self.latest_report("daily") or ""),
            "latest_intraday_report": str(self.latest_report("intraday") or ""),
            "latest_review": str(self.latest_report("reviews") or ""),
            "context_for_llm": str(self.config.root / self.config.report_setting("context_file", "data/processed/context_for_llm.md")),
        }

    def doctor(self) -> dict[str, Any]:
        latest_update = self.file_store.read_json(
            Path("data") / "processed" / "market_summary" / "last_update.json"
        ) or {}
        checks = {
            "python": sys.version.split()[0],
            "project_root_exists": self.config.root.exists(),
            "db_exists": self.config.db_path.exists(),
            "configured_symbols": len(self.config.symbols),
            "active_symbols": len(self._active_symbols_from_cache()),
            "cached_symbols": len(self._load_market_data()),
            "latest_data": self._data_freshness(self._load_market_data()),
            "latest_daily_report": str(self.latest_report("daily") or ""),
            "context_exists": (self.config.root / self.config.report_setting("context_file", "data/processed/context_for_llm.md")).exists(),
            "last_update_failures": latest_update.get("failed", {}),
            "last_derivatives_failures": latest_update.get("derivatives_failed", {}),
            "last_multi_exchange_derivatives_failures": latest_update.get("multi_exchange_derivatives_failed", {}),
            "last_news_failures": latest_update.get("news_failures", {}),
            "last_social_failures": latest_update.get("social_failures", {}),
        }
        checks["ready"] = bool(
            checks["db_exists"]
            and checks["cached_symbols"]
            and checks["latest_daily_report"]
            and checks["context_exists"]
        )
        return checks

    def latest_report(self, kind: str = "daily") -> Path | None:
        directory_map = {
            "daily": self.config.reports_dir / "daily",
            "intraday": self.config.reports_dir / "intraday",
            "scalp": self.config.reports_dir / "scalp",
            "review": self.config.reports_dir / "reviews",
            "reviews": self.config.reports_dir / "reviews",
        }
        directory = directory_map.get(kind, self.config.reports_dir / kind)
        if not directory.exists():
            return None
        reports = sorted(directory.glob("*.md"), key=lambda path: path.stat().st_mtime, reverse=True)
        return reports[0] if reports else None

    def _load_derivatives_records(self) -> dict[str, dict[str, Any]]:
        payload = self.file_store.read_json(
            Path("data") / "raw" / "open_interest" / "binance_futures_latest.json"
        )
        if not payload:
            return {}
        return payload.get("records", {})

    def _maybe_send_trade_alerts(
        self,
        ideas,
        mode: str,
        report_id: str,
        registered_signal_ids: dict[str, str] | None = None,
    ) -> None:
        """Send A/B-tier ideas to Telegram if a chat_id is configured.

        PART 1 fix: when ``registered_signal_ids`` is provided, ONLY ideas
        whose signal was registered to ``proposed_signals`` are alerted.
        This guarantees every Telegram alert is trackable; ideas missing
        entry/invalidation are skipped instead of becoming untracked
        legacy alerts.
        """
        try:
            from src.notifiers.telegram import TelegramNotConfigured
            from src.notifiers.trade_telegram import notifier_for
        except Exception:
            return
        notifier = notifier_for(self.config.root)
        if not notifier.enabled or not notifier.chat_id:
            return
        cooldown_min = notifier.cooldown_minutes
        registered_map = registered_signal_ids or {}
        for idea in ideas:
            if idea.tier not in {"A", "B"} or idea.direction not in {"long", "short"}:
                continue
            # PART 1: require a proposed_signal exists for this idea before
            # alerting. If caller passed an explicit map, gate strictly on it.
            signal_id = registered_map.get(idea.symbol)
            if registered_signal_ids is not None and not signal_id:
                self._log_secondary_failure(
                    f"telegram alert {idea.symbol} skipped",
                    RuntimeError("no proposed_signal — alert would be untracked"),
                )
                continue
            last = self.db.last_alert_for(idea.symbol)
            if last is not None:
                try:
                    from datetime import datetime, timezone
                    sent_at = datetime.fromisoformat(str(last["sent_at"]).replace("Z", "+00:00"))
                    if sent_at.tzinfo is None:
                        sent_at = sent_at.replace(tzinfo=timezone.utc)
                    age_min = (datetime.now(timezone.utc) - sent_at).total_seconds() / 60
                    if age_min < cooldown_min and last.get("new_tier") == idea.tier:
                        continue
                except Exception:
                    pass
            text = self._format_idea_alert(
                idea, mode=mode, report_id=report_id, signal_id=signal_id
            )
            # 2026-08-31: setup ideas stay in the journal/dashboard. Phone
            # alerts are live-only so disabled/research modes such as scalp
            # cannot keep spamming Telegram.
            suppress_setup = should_suppress_setup_telegram(
                idea.asset_class or "crypto", mode
            )
            try:
                if not suppress_setup:
                    # Plain text — the new template uses brackets/emoji which
                    # break Telegram Markdown parsing. parse_mode="" is the safe
                    # delivery path.
                    notifier.send(text, parse_mode="")
            except TelegramNotConfigured:
                return
            except Exception as exc:
                self._log_secondary_failure(f"telegram alert {idea.symbol}", exc)
                continue
            self.db.record_watchlist_alert(
                symbol=idea.symbol,
                previous_tier="report",
                new_tier=idea.tier,
                score=float(idea.score),
                direction=idea.direction,
                mode=mode,
                payload={
                    "report_id": report_id,
                    "thesis": idea.thesis[:300],
                    "signal_id": signal_id or "",
                    # Telegram delivery channel for this setup alert.
                    "telegram_channel": "journal_only" if suppress_setup else "telegram",
                },
            )

    @staticmethod
    def _format_idea_alert(idea, mode: str, report_id: str,
                            signal_id: str | None = None) -> str:
        """Standardized setup-waiting alert (plain text).

        Delegates to ``src.notifiers.setup_alert.render_setup_alert``.
        The legacy Markdown template was removed 2026-06-14 — see
        reports/TELEGRAM_ALERT_STANDARDIZATION_IMPLEMENTATION_REPORT.md.
        """
        from src.notifiers.setup_alert import render_setup_alert

        setup = (idea.raw or {}).get("setup") or {}
        derivatives = (idea.raw or {}).get("derivatives") or {}
        if not isinstance(derivatives, dict):
            derivatives = {}
        signal: dict[str, object] = {
            "asset_class": idea.asset_class or "crypto",
            "symbol": idea.symbol,
            "direction": idea.direction,
            "mode": mode,
            "tier": idea.tier,
            "score": idea.score,
            "primary_exchange": idea.exchange_focus,
            "data_confidence": idea.data_confidence,
            "news_supported": (idea.raw or {}).get("news_supported", 0),
            "thesis": idea.thesis or "",
            "setup_type": (idea.raw or {}).get("setup_type") or "",
            "entry_low": setup.get("entry_low"),
            "entry_high": setup.get("entry_high"),
            "entry_trigger": setup.get("entry_trigger"),
            "stop_loss": setup.get("invalidation"),
            "invalidation": setup.get("invalidation"),
            "tp1": setup.get("tp1"),
            "tp2": setup.get("tp2"),
            "tp3": setup.get("tp3"),
            "signal_id": signal_id or "",
            "report_id": report_id,
            "derivatives_at_proposal": derivatives,
            "funding_context": (
                f"funding={derivatives.get('funding_rate')}, "
                f"crowding={derivatives.get('crowding_risk')}"
                if derivatives.get("data_available") else ""
            ),
            "oi_context": str(derivatives.get("interpretation") or ""),
        }
        return render_setup_alert(signal)

    def _maybe_register_signals(
        self,
        ideas,
        *,
        mode: str,
        report_id: str,
        regime_label: str,
    ) -> dict[str, str]:
        """Passive signal tracking. Errors here must never block reports.

        Returns a map ``{symbol: signal_id}`` for ideas that were registered.
        Callers can use this map to gate Telegram alerts on registration
        (so no alert is ever sent for an untrackable idea).
        """

        try:
            from src.signals.config import load_signal_tracking_config
            from src.signals.registry import build_signal_from_idea, register_ideas
        except Exception as exc:
            self._log_secondary_failure("signal tracking import", exc)
            return {}
        try:
            config = load_signal_tracking_config(self.config.root)
            if not config.enabled:
                return {}
            weekend_active = False
            try:
                from src.analysis import weekend_mode

                weekend_status = weekend_mode.current_status(
                    weekend_mode.load_config(self.config.root),
                    self.config.settings,
                )
                weekend_active = bool(getattr(weekend_status, "active", False))
            except Exception:
                weekend_active = False
            result = register_ideas(
                self.db,
                ideas,
                config=config,
                report_id=report_id,
                market_regime=regime_label,
                weekend_mode_active=weekend_active,
            )
            # Map symbol → signal_id by re-deriving signal_id for each idea.
            # build_signal_from_idea is deterministic on (symbol, mode,
            # direction, tier, entry, invalidation, created_at, report_id);
            # for our purpose we just need to know WHICH ideas registered.
            inserted_ids = set(result.signal_ids or [])
            symbol_to_signal: dict[str, str] = {}
            for idea in ideas:
                try:
                    signal = build_signal_from_idea(
                        idea,
                        config=config,
                        report_id=report_id,
                        market_regime=regime_label,
                        weekend_mode_active=weekend_active,
                    )
                except Exception:
                    signal = None
                if signal is None:
                    continue
                # Either this is a freshly inserted id, or it was already
                # present (dedupe). Either way the row exists now.
                if signal.signal_id in inserted_ids:
                    symbol_to_signal[idea.symbol] = signal.signal_id
                else:
                    # Pre-existing row — still trackable.
                    symbol_to_signal[idea.symbol] = signal.signal_id
            return symbol_to_signal
        except Exception as exc:
            self._log_secondary_failure("signal tracking register", exc)
            return {}

    def _log_secondary_failure(self, name: str, exc: Exception) -> None:
        import logging
        logging.getLogger("crypto_ai_desk").warning("%s failed: %s", name, exc)

    def _load_bybit_derivatives_records(self) -> dict[str, dict[str, Any]]:
        payload = self.file_store.read_json(
            Path("data") / "raw" / "open_interest" / "bybit_derivatives_latest.json"
        )
        if not payload:
            return {}
        return payload.get("records", {})

    def _load_multi_exchange_derivatives_records(self) -> dict[str, dict[str, Any]]:
        payload = self.file_store.read_json(
            Path("data") / "raw" / "open_interest" / "multi_exchange_derivatives_latest.json"
        )
        if not payload:
            return {}
        return payload.get("records", {})

    def _load_social_mentions(self) -> list[dict[str, Any]]:
        payload = self.file_store.read_json(
            Path("data") / "raw" / "social" / "social_latest.json"
        )
        if not payload:
            return []
        return payload.get("mentions", [])

    def _resolve_universe(self, symbols: list[str] | None = None) -> list[str]:
        if symbols is not None:
            return symbols
        selection = BinanceUniverseCollector(self.config, self.file_store).select(
            self.config.symbols,
            mode="intraday",
        )
        return selection.symbols or self.config.symbols

    def _selected_ranked_symbols(self, rows: list[dict[str, Any]]) -> list[str]:
        payload = self.file_store.read_json(
            Path("data") / "processed" / "candidates" / "universe_ranked_candidates.json"
        ) or {}
        selected = payload.get("selected_for_deep_analysis") or []
        if selected:
            return [str(symbol) for symbol in selected]
        return [
            str(row["symbol"])
            for row in rows
            if not set(row.get("risk_flags", [])) & {"low_24h_quote_volume", "wide_spread", "insufficient_candles"}
        ][: int(self.config.universe_setting("max_symbols_for_deep_analysis", 30))]

    def _mode_timeframes(self, mode: str) -> list[str]:
        payload = self.config.universe.get("modes", {}).get(mode, {})
        timeframes = [str(item) for item in payload.get("timeframes", [])]
        if mode == "scalp" and "1h" not in timeframes:
            timeframes.append("1h")
        return timeframes or self.config.timeframes

    def _active_symbols_from_cache(self) -> list[str]:
        payload = self.file_store.read_json(
            Path("data") / "processed" / "market_summary" / "universe_latest.json"
        ) or {}
        symbols = payload.get("symbols") or []
        if symbols:
            return [str(symbol) for symbol in symbols]
        discovered = self.file_store.discovered_symbols(
            self.config.exchange_id, self.config.settings.get("execution", {}).get("setup_timeframe", "1h")
        )
        if bool(self.config.universe_setting("enabled", False)) and discovered:
            configured = list(self.config.symbols)
            for symbol in discovered:
                if symbol not in configured:
                    configured.append(symbol)
            return configured
        return self.config.symbols

    @staticmethod
    def _infer_action(normalized_query: str) -> str:
        if any(term in normalized_query for term in ["review", "worked", "failed", "what worked", "что сработало", "ревью", "обзор идей"]):
            return "review"
        if any(term in normalized_query for term in ["intraday", "morning", "still valid", "valid", "утро", "интрадей", "актуаль"]):
            return "intraday-report"
        if any(term in normalized_query for term in ["update", "refresh", "обнов", "fresh data"]):
            return "update-data"
        if any(term in normalized_query for term in ["scanner", "scan", "скан"]):
            return "scan"
        return "daily-report"

    @staticmethod
    def _should_refresh(normalized_query: str) -> bool:
        return any(
            term in normalized_query
            for term in ["today", "current", "fresh", "update", "refresh", "now", "сегодня", "сейчас", "обнов"]
        )

    @staticmethod
    def _data_freshness(market_data: dict[str, dict[str, Any]]) -> str:
        latest = None
        for frames in market_data.values():
            for frame in frames.values():
                if frame is None or frame.empty or "timestamp" not in frame.columns:
                    continue
                value = frame["timestamp"].iloc[-1]
                if latest is None or value > latest:
                    latest = value
        return str(latest) if latest is not None else "no cached candles found"
