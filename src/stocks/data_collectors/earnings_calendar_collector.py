"""EarningsCalendarCollector — read earnings dates from yfinance + manual CSV.

Order of precedence (newer wins on conflict):
  1. Manual CSV at data/manual/stocks/earnings_calendar.csv
  2. yfinance Ticker.calendar (best-effort; coverage is patchy)

The collector returns a list of normalized event dicts. It does NOT write
to the events SQLite table by default — that's the caller's job, so the
collector stays side-effect-free and easy to test.
"""

from __future__ import annotations

import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from src.config import ProjectConfig
from src.logger import get_logger
from src.stocks.configs.loader import StocksConfig
from src.stocks.data_collectors.yf_client import fetch_calendar

_LOG = get_logger("stocks.earnings_collector")


@dataclass
class EarningsEvent:
    date: str         # YYYY-MM-DD
    symbol: str
    report_time: str  # BMO / AMC / DMT / unknown
    eps_estimate: float | None = None
    revenue_estimate: float | None = None
    source: str = "yfinance"
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_date": self.date,
            "ticker": self.symbol,
            "event": "earnings",
            "event_type": "earnings",
            "source": self.source,
            "importance": 8.0,  # earnings are high-importance by default
            "asset_class": "stocks",
            "report_time": self.report_time,
            "eps_estimate": self.eps_estimate,
            "revenue_estimate": self.revenue_estimate,
            "notes": self.notes,
        }


@dataclass
class EarningsCollectionSummary:
    events: list[EarningsEvent] = field(default_factory=list)
    failed_symbols: list[str] = field(default_factory=list)
    manual_count: int = 0
    yfinance_count: int = 0


class EarningsCalendarCollector:
    name = "earnings_calendar_collector"

    def __init__(self, project_config: ProjectConfig, stocks_config: StocksConfig):
        self.project_config = project_config
        self.stocks_config = stocks_config

    def manual_csv_path(self) -> Path:
        return (
            self.project_config.root
            / "data"
            / "manual"
            / "stocks"
            / "earnings_calendar.csv"
        )

    def load_manual(self) -> list[EarningsEvent]:
        path = self.manual_csv_path()
        if not path.exists():
            return []
        events: list[EarningsEvent] = []
        try:
            with path.open("r", encoding="utf-8", newline="") as fh:
                reader = csv.DictReader(
                    (line for line in fh if not line.lstrip().startswith("#"))
                )
                for row in reader:
                    sym = (row.get("symbol") or "").strip().upper()
                    dt = (row.get("date") or "").strip()
                    if not sym or not dt:
                        continue
                    events.append(
                        EarningsEvent(
                            date=dt,
                            symbol=sym,
                            report_time=(row.get("report_time") or "unknown").strip(),
                            eps_estimate=_parse_float(row.get("eps_estimate")),
                            revenue_estimate=_parse_float(row.get("revenue_estimate")),
                            source="manual",
                            notes=(row.get("notes") or "").strip(),
                        )
                    )
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("manual earnings_calendar.csv parse failed: %s", exc)
        return events

    def fetch_yfinance(
        self,
        symbols: list[str],
        *,
        max_workers: int = 1,
    ) -> tuple[list[EarningsEvent], list[str]]:
        events: list[EarningsEvent] = []
        failed: list[str] = []

        def _fetch_one(symbol: str) -> tuple[EarningsEvent | None, str | None]:
            # Broad-market and sector ETFs have no issuer earnings. Calling
            # ``Ticker.calendar`` for them produces noisy quoteSummary 404s
            # in yfinance while contributing no decision data.
            if self.stocks_config.is_etf(symbol):
                return None, None
            payload = fetch_calendar(symbol)
            if not payload:
                return None, symbol
            event_date = _extract_first(payload, ("Earnings Date", "earnings_date"))
            if not event_date:
                return None, symbol
            iso = _to_iso_date(event_date)
            if not iso:
                return None, symbol
            return EarningsEvent(
                date=iso,
                symbol=symbol,
                report_time="unknown",
                eps_estimate=_to_float(
                    _extract_first(payload, ("EPS Estimate", "earnings_average"))
                ),
                revenue_estimate=_to_float(
                    _extract_first(payload, ("Revenue Estimate", "revenue_average"))
                ),
                source="yfinance",
            ), None

        workers = max(1, int(max_workers))
        if workers == 1:
            for symbol in symbols:
                event, failed_symbol = _fetch_one(symbol)
                if event is not None:
                    events.append(event)
                if failed_symbol:
                    failed.append(failed_symbol)
        else:
            with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="stocks-earnings") as pool:
                futures = [pool.submit(_fetch_one, symbol) for symbol in symbols]
                for future in as_completed(futures):
                    event, failed_symbol = future.result()
                    if event is not None:
                        events.append(event)
                    if failed_symbol:
                        failed.append(failed_symbol)
        events.sort(key=lambda event: (event.date, event.symbol))
        failed.sort()
        return events, failed

    def collect(
        self,
        *,
        symbols: list[str] | None = None,
        include_yfinance: bool = True,
        max_workers: int = 1,
    ) -> EarningsCollectionSummary:
        symbols = symbols or list(self.stocks_config.default_symbols)
        summary = EarningsCollectionSummary()

        manual = self.load_manual()
        summary.manual_count = len(manual)

        yf_events: list[EarningsEvent] = []
        yf_failed: list[str] = []
        if include_yfinance:
            yf_events, yf_failed = self.fetch_yfinance(symbols, max_workers=max_workers)
        summary.yfinance_count = len(yf_events)
        summary.failed_symbols = yf_failed

        # Merge: manual entries win on (date, symbol) conflict so users can
        # override or correct yfinance's flaky coverage by hand.
        seen: set[tuple[str, str]] = set()
        merged: list[EarningsEvent] = []
        for ev in manual:
            key = (ev.date, ev.symbol)
            if key in seen:
                continue
            seen.add(key)
            merged.append(ev)
        for ev in yf_events:
            key = (ev.date, ev.symbol)
            if key in seen:
                continue
            seen.add(key)
            merged.append(ev)
        summary.events = sorted(merged, key=lambda e: (e.date, e.symbol))
        return summary

    @staticmethod
    def days_until(event_date: str, *, today: date | None = None) -> int | None:
        """Trading-day-agnostic calendar distance (negative = past)."""

        today = today or datetime.now(timezone.utc).date()
        try:
            target = datetime.strptime(event_date, "%Y-%m-%d").date()
        except ValueError:
            return None
        return (target - today).days


def _parse_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return None


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, list):
        for item in value:
            v = _to_float(item)
            if v is not None:
                return v
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _extract_first(payload: dict[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        if key in payload and payload[key] not in (None, "", []):
            value = payload[key]
            if isinstance(value, list) and value:
                return value[0]
            return value
    return None


def _to_iso_date(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        # accept already-iso strings or 'YYYY-MM-DD HH:MM:SS'
        head = value[:10]
        try:
            datetime.strptime(head, "%Y-%m-%d")
            return head
        except ValueError:
            return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return None
