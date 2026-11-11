"""StocksPipeline — orchestrate the 9-agent chain end-to-end.

Mirrors the role of src/agents/supervisor.py for the crypto module, but
focused on stocks/indices. Does not import or call crypto agents.

The pipeline is read-mostly: it pulls data via the stocks collectors,
runs each agent in order, builds a report (Markdown) and an LLM packet,
and persists A/B trade ideas through the existing signal registry with
asset_class='stocks'.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Callable

from src.config import ProjectConfig
from src.logger import get_logger
from src.signals.config import load_signal_tracking_config
from src.signals.registry import register_ideas
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore
from src.stocks.agents import (
    CompanyNewsAgent,
    EarningsRiskAgent,
    SectorRotationAgent,
    StockRelativeStrengthAgent,
    StockRiskAgent,
    StockScoringAgent,
    StockTechnicalAgent,
    StockTradeIdeaAgent,
    StocksMarketRegimeAgent,
)
from src.stocks.configs.loader import StocksConfig, load_stocks_config
from src.stocks.data_collectors import (
    EarningsCalendarCollector,
    MarketIndexCollector,
    SectorETFCollector,
    StockOHLCVCollector,
    StockOHLCVSummary,
)
from src.stocks.data_collectors.earnings_calendar_collector import (
    EarningsCollectionSummary,
    EarningsEvent,
)
from src.models import TradeIdea

_LOG = get_logger("stocks.pipeline")


@dataclass
class StocksDataSummary:
    indices: StockOHLCVSummary | None = None
    sectors: StockOHLCVSummary | None = None
    symbols: StockOHLCVSummary | None = None
    earnings_count: int = 0
    earnings_failed: list[str] = field(default_factory=list)

    @property
    def total_ok(self) -> int:
        return (
            (self.indices.ok if self.indices else 0)
            + (self.sectors.ok if self.sectors else 0)
            + (self.symbols.ok if self.symbols else 0)
        )

    @property
    def total_failed(self) -> int:
        return (
            (self.indices.fail if self.indices else 0)
            + (self.sectors.fail if self.sectors else 0)
            + (self.symbols.fail if self.symbols else 0)
        )


@dataclass
class StocksPipelineResult:
    mode: str
    asset_class: str = "stocks"
    decision_at: str = ""
    regime: dict[str, Any] = field(default_factory=dict)
    sectors: dict[str, Any] = field(default_factory=dict)
    rs: dict[str, Any] = field(default_factory=dict)
    earnings: dict[str, Any] = field(default_factory=dict)
    news: dict[str, Any] = field(default_factory=dict)
    technical: dict[str, Any] = field(default_factory=dict)
    risk: dict[str, Any] = field(default_factory=dict)
    scoring: dict[str, Any] = field(default_factory=dict)
    ideas_payload: dict[str, Any] = field(default_factory=dict)
    ideas: list[TradeIdea] = field(default_factory=list)
    data_summary: StocksDataSummary = field(default_factory=StocksDataSummary)
    report_path: Path | None = None
    signal_ids: list[str] = field(default_factory=list)


class StocksPipeline:
    """Orchestrator for the stocks/indices analysis pipeline."""

    def __init__(
        self,
        config: ProjectConfig,
        stocks_config: StocksConfig | None = None,
    ):
        self.config = config
        self.stocks_config = stocks_config or load_stocks_config(config.root)
        self.file_store = FileStore(config)
        self.db = SQLiteStore(config.db_path)
        self.file_store.ensure_directories()
        self.db.init_db()

    # ------------------------------------------------------------------
    # Data collection
    # ------------------------------------------------------------------
    def update_data(
        self,
        *,
        mode: str = "intraday",
        symbols: list[str] | None = None,
        include_indices: bool = True,
        include_sectors: bool = True,
        intervals: list[str] | None = None,
        include_earnings: bool = True,
        fast_data_update: bool = False,
    ) -> StocksDataSummary:
        symbols = symbols or list(self.stocks_config.default_symbols)
        intervals = list(intervals or self.stocks_config.timeframes_for(mode))
        summary = StocksDataSummary()

        if include_indices:
            indices = MarketIndexCollector(self.config, self.stocks_config)
            summary.indices = indices.collect(intervals=["1d", "1h"], include_vix=True)

        if include_sectors:
            sectors = SectorETFCollector(self.config, self.stocks_config)
            summary.sectors = sectors.collect(intervals=["1d"])

        ohlcv = StockOHLCVCollector(self.config, self.stocks_config)
        summary.symbols = ohlcv.collect(
            symbols,
            intervals,
            throttle_seconds=0.0 if fast_data_update else 0.3,
            max_workers=4 if fast_data_update else 1,
        )

        if include_earnings:
            ec = EarningsCalendarCollector(self.config, self.stocks_config)
            # Persist earnings events into shared events table so they're visible
            # to downstream packet builders and to manual queries.
            result = ec.collect(
                symbols=symbols,
                include_yfinance=True,
                max_workers=4 if fast_data_update else 1,
            )
            summary.earnings_count = len(result.events)
            summary.earnings_failed = result.failed_symbols
            if result.events:
                self.db.save_events(
                    [ev.to_dict() for ev in result.events],
                    asset_class="stocks",
                )
        return summary

    # ------------------------------------------------------------------
    # Full analysis chain
    # ------------------------------------------------------------------
    def run_report(
        self,
        *,
        mode: str = "intraday",
        symbols: list[str] | None = None,
        skip_data_update: bool = False,
        shadow_only: bool = False,
        now: datetime | None = None,
        on_decision: Callable[["StocksPipeline", StocksPipelineResult], None] | None = None,
        fast_data_update: bool = False,
        refresh_earnings: bool | None = None,
        apply_intraday_guards: bool = True,
    ) -> StocksPipelineResult:
        # HARD GUARD: the old stocks swing/invest pipeline is DEPRECATED/REMOVED. Even a direct
        # call must not fetch, score, save trade_ideas, or register proposed_signals for these
        # modes. Raise BEFORE any side effect. Use the shadow-only stocks_position_framework
        # (`stocks-position-scan`) instead. Stocks intraday is unaffected.
        if mode in ("swing", "invest"):
            raise ValueError(
                "old stocks swing/invest pipeline deprecated/removed; use stocks-position-scan "
                "(shadow-only stocks_position_framework)"
            )
        symbols = symbols or list(self.stocks_config.default_symbols)
        # Earnings calendars change slowly compared with intraday bars. A
        # fast monitor pass uses the durable snapshot; scheduled and pre-open
        # passes refresh it explicitly through yfinance.
        if refresh_earnings is None:
            refresh_earnings = not fast_data_update
        # The timestamp is fixed immediately before the final idea decision.
        # This keeps the session gate and registration clock identical while
        # avoiding a decision timestamp that has gone stale during data fetch.
        requested_now = now
        result = StocksPipelineResult(mode=mode)

        if not skip_data_update:
            result.data_summary = self.update_data(
                mode=mode,
                symbols=symbols,
                include_indices=not fast_data_update,
                include_sectors=not fast_data_update,
                intervals=["15m"] if fast_data_update else None,
                # The canonical earnings pass below persists once per report.
                # Do not fetch the same calendar twice in one pipeline run.
                include_earnings=False,
                fast_data_update=fast_data_update,
            )

        # Build agents
        regime_agent = StocksMarketRegimeAgent(
            self.config, self.stocks_config, self.file_store, self.db
        )
        sector_agent = SectorRotationAgent(
            self.config, self.stocks_config, self.file_store, self.db
        )
        rs_agent = StockRelativeStrengthAgent(
            self.config, self.stocks_config, self.file_store, self.db
        )
        earnings_agent = EarningsRiskAgent(
            self.config, self.stocks_config, self.file_store, self.db
        )
        news_agent = CompanyNewsAgent(
            self.config, self.stocks_config, self.file_store, self.db
        )
        tech_agent = StockTechnicalAgent(
            self.config, self.stocks_config, self.file_store, self.db
        )
        risk_agent = StockRiskAgent(
            self.config, self.stocks_config, self.file_store, self.db
        )
        scoring_agent = StockScoringAgent(
            self.config, self.stocks_config, self.file_store, self.db
        )
        idea_agent = StockTradeIdeaAgent(
            self.config, self.stocks_config, self.file_store, self.db
        )

        # Run chain
        _LOG.info("Stocks pipeline starting (mode=%s, symbols=%d)", mode, len(symbols))
        result.regime = regime_agent.run()
        result.sectors = sector_agent.run()
        result.rs = rs_agent.run(symbols=symbols)

        # Scheduled/pre-open passes refresh manual + yfinance and persist the
        # result. Fast RTH reports consume that durable snapshot so a slow
        # calendar endpoint cannot turn a fresh setup into a late entry.
        if refresh_earnings:
            ec = EarningsCalendarCollector(self.config, self.stocks_config)
            ec_summary = ec.collect(
                symbols=symbols,
                include_yfinance=True,
                max_workers=4 if fast_data_update else 1,
            )
            if ec_summary.events:
                self.db.save_events(
                    [event.to_dict() for event in ec_summary.events],
                    asset_class="stocks",
                )
        else:
            ec_summary = EarningsCollectionSummary(
                events=self._cached_earnings_events(symbols)
            )
        result.data_summary.earnings_count = len(ec_summary.events)
        result.earnings = earnings_agent.run(ec_summary.events, symbols=symbols, mode=mode)

        result.news = news_agent.run(symbols=symbols)
        result.technical = tech_agent.run(symbols=symbols, mode=mode)
        result.risk = risk_agent.run(
            regime_payload=result.regime,
            sector_payload=result.sectors,
            rs_payload=result.rs,
            earnings_payload=result.earnings,
            technical_payload=result.technical,
            mode=mode,
        )
        result.scoring = scoring_agent.run(
            regime_payload=result.regime,
            sector_payload=result.sectors,
            rs_payload=result.rs,
            technical_payload=result.technical,
            news_payload=result.news,
            risk_payload=result.risk,
            mode=mode,
        )
        decision_at = requested_now or datetime.now(timezone.utc)
        if decision_at.tzinfo is None:
            decision_at = decision_at.replace(tzinfo=timezone.utc)
        else:
            decision_at = decision_at.astimezone(timezone.utc)
        result.decision_at = decision_at.isoformat()
        result.ideas_payload = idea_agent.run(
            scoring_payload=result.scoring,
            technical_payload=result.technical,
            news_payload=result.news,
            earnings_payload=result.earnings,
            rs_payload=result.rs,
            regime_payload=result.regime,
            sector_payload=result.sectors,
            risk_payload=result.risk,
            mode=mode,
            now=decision_at,
            apply_intraday_guards=apply_intraday_guards,
        )

        # Materialize TradeIdea objects from the agent payload so the signal
        # registry can serialize them properly.
        result.ideas = []
        for entry in result.ideas_payload.get("ideas") or []:
            try:
                raw = dict(entry.get("raw") or {})
                raw["decision_at"] = result.decision_at
                entry["raw"] = raw
                result.ideas.append(TradeIdea(**entry))
            except Exception as exc:  # noqa: BLE001
                _LOG.warning("dropping malformed idea payload: %s", exc)

        # Shadow callers may reuse the exact analysis chain for an isolated
        # research universe, but must never create trade ideas or signals in
        # the authoritative Paper pipeline.
        report_id = f"stocks_{mode}_{_iso_stamp()}"
        if result.ideas and not shadow_only:
            self.db.save_trade_ideas(report_id, result.ideas, asset_class="stocks")

        # Register A/B (and C-with-trigger) ideas as proposed signals BEFORE
        # rendering the Markdown report so the Recent Signal Performance
        # section reflects this run's just-registered signals. This matches
        # the crypto supervisor's order (see src/agents/supervisor.py).
        # source_report_path is filled in after _save_report; we backfill it
        # via a follow-up UPDATE so the registry row points at the saved
        # report file even though registration happened first.
        tracking_cfg = load_signal_tracking_config(self.config.root)
        if tracking_cfg.enabled and result.ideas and not shadow_only:
            regime_label = (result.regime.get("regime") or {}).get("label", "")
            registration = register_ideas(
                self.db,
                result.ideas,
                config=tracking_cfg,
                report_id=report_id,
                market_regime=regime_label,
                source_report_path=None,  # backfilled below after save
                asset_class="stocks",
                created_at=result.decision_at,
            )
            result.signal_ids = list(registration.signal_ids)
            # Preserve the exact decision that was available to Paper now.
            # A later after-hours refresh may legitimately re-score the same
            # row as planning-only; it must not erase this point-in-time fact.
            try:
                from src.stocks.paper_funnel import snapshot_signals

                snapshot_signals(
                    self.config.db_path, result.signal_ids, now=decision_at
                )
            except Exception as exc:  # noqa: BLE001 - observability cannot stop Paper
                _LOG.warning("could not capture stocks Paper decision snapshots: %s", exc)

        # Latency-sensitive consumers may register isolated profile rows as
        # soon as the point-in-time decision exists. Large report rendering is
        # observability, not an execution prerequisite.
        if on_decision is not None:
            try:
                on_decision(self, result)
            except Exception as exc:  # noqa: BLE001
                _LOG.warning("stocks on-decision hook failed: %s", exc)

        # The shadow caller owns its report and its separate tables. Avoid
        # replacing the operator-facing stocks intraday report with a wider
        # research-universe run.
        if not shadow_only:
            from src.stocks.reports.stocks_report_builder import build_stocks_report

            report_text = build_stocks_report(result, config=self.config)
            result.report_path = self._save_report(mode, report_text)

        # Backfill source_report_path for the signals we just registered.
        if result.signal_ids and result.report_path is not None:
            try:
                with self.db.connect() as conn:
                    qmarks = ",".join("?" for _ in result.signal_ids)
                    conn.execute(
                        f"UPDATE proposed_signals SET source_report_path = ? "
                        f"WHERE signal_id IN ({qmarks})",
                        (str(result.report_path), *result.signal_ids),
                    )
            except Exception as exc:  # noqa: BLE001
                _LOG.warning(
                    "could not backfill source_report_path for stocks signals: %s",
                    exc,
                )

        return result

    def _cached_earnings_events(self, symbols: list[str]) -> list[EarningsEvent]:
        """Load persisted stock earnings without adding network latency.

        The method is intentionally limited to the fast intraday loop. A
        scheduled or pre-open report refreshes the same table first; if the
        cache is unavailable, the downstream earnings agent emits its normal
        ``unknown`` state rather than inventing an earnings date.
        """
        wanted = {str(symbol).upper() for symbol in symbols}
        events: list[EarningsEvent] = []
        seen: set[tuple[str, str]] = set()
        try:
            rows = self.db.load_events(limit=max(1_000, len(wanted) * 12))
        except Exception as exc:  # noqa: BLE001 - preserve the existing unknown path
            _LOG.warning("could not load cached stock earnings: %s", exc)
            return events
        for row in rows:
            if str(row.get("asset_class") or "").lower() != "stocks":
                continue
            if str(row.get("event_type") or "").lower() != "earnings":
                continue
            symbol = str(row.get("ticker") or "").upper()
            if symbol not in wanted:
                continue
            raw = row.get("raw_json")
            try:
                payload = json.loads(raw) if raw else {}
            except (TypeError, ValueError):
                payload = {}
            event_date = str(payload.get("event_date") or row.get("event_date") or "")
            if not event_date:
                continue
            key = (event_date, symbol)
            if key in seen:
                continue
            seen.add(key)
            events.append(EarningsEvent(
                date=event_date,
                symbol=symbol,
                report_time=str(payload.get("report_time") or "unknown"),
                eps_estimate=payload.get("eps_estimate"),
                revenue_estimate=payload.get("revenue_estimate"),
                source=str(payload.get("source") or row.get("source") or "cached"),
                notes=str(payload.get("notes") or ""),
            ))
        return sorted(events, key=lambda event: (event.date, event.symbol))

    # ------------------------------------------------------------------
    # Candidate debug
    # ------------------------------------------------------------------
    def debug_symbol(
        self,
        symbol: str,
        *,
        mode: str = "intraday",
        skip_data_update: bool = True,
    ) -> dict[str, Any]:
        """Run the chain for a single symbol and return a flattened summary."""

        result = self.run_report(
            mode=mode, symbols=[symbol.upper()], skip_data_update=skip_data_update
        )
        sym = symbol.upper()

        def _by(rows: list[dict[str, Any]], key: str = "symbol") -> dict[str, Any] | None:
            for row in rows or []:
                if str(row.get(key, "")).upper() == sym:
                    return row
            return None

        return {
            "symbol": sym,
            "mode": mode,
            "regime": (result.regime.get("regime") or {}).get("label"),
            "rs": _by(result.rs.get("rows") or []),
            "earnings": _by(result.earnings.get("risks") or []),
            "technical": _by(result.technical.get("setups") or []),
            "risk": (result.risk.get("by_symbol") or {}).get(sym),
            "scoring": _by(result.scoring.get("scores") or []),
            "report_path": str(result.report_path) if result.report_path else None,
        }

    # ------------------------------------------------------------------
    # Earnings scan (lightweight CLI helper)
    # ------------------------------------------------------------------
    def earnings_scan(
        self,
        *,
        symbols: list[str] | None = None,
        mode: str = "swing",
    ) -> dict[str, Any]:
        symbols = symbols or list(self.stocks_config.default_symbols)
        ec = EarningsCalendarCollector(self.config, self.stocks_config)
        summary = ec.collect(symbols=symbols, include_yfinance=True)
        if summary.events:
            self.db.save_events(
                [ev.to_dict() for ev in summary.events],
                asset_class="stocks",
            )
        agent = EarningsRiskAgent(
            self.config, self.stocks_config, self.file_store, self.db
        )
        payload = agent.run(summary.events, symbols=symbols, mode=mode)
        payload["raw_events"] = [
            {
                "date": e.date,
                "symbol": e.symbol,
                "report_time": e.report_time,
                "source": e.source,
            }
            for e in summary.events
        ]
        return payload

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _save_report(self, mode: str, text: str) -> Path:
        dt = datetime.now(timezone.utc)
        stamp = dt.strftime("%Y-%m-%d_%H-%M")
        target = (
            self.config.reports_dir
            / "stocks"
            / mode
            / f"{stamp}_stocks_{mode}_report.md"
        )
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        _LOG.info("Stocks report saved: %s", target)
        return target


def _iso_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
