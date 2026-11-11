"""EarningsRiskAgent — classify earnings proximity risk per symbol per mode.

Inputs: events from EarningsCalendarCollector + the mode-specific rules in
config/stocks/risk.yaml. The agent doesn't fetch on its own; the caller
supplies an event list so this can be unit-tested without network.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from typing import Any

from src.stocks.agents.base import StocksBaseAgent
from src.stocks.data_collectors.earnings_calendar_collector import EarningsEvent


@dataclass
class EarningsRisk:
    symbol: str
    next_earnings_date: str | None
    days_ahead: int | None
    report_time: str
    severity: str    # active / next_session / this_week / safe / unknown
    note: str        # human-readable summary
    blocks_swing: bool
    intraday_high_risk: bool


class EarningsRiskAgent(StocksBaseAgent):
    name = "earnings_risk"

    def run(
        self,
        events: list[EarningsEvent],
        *,
        symbols: list[str] | None = None,
        mode: str = "intraday",
        today: date | None = None,
    ) -> dict[str, Any]:
        today = today or datetime.now(timezone.utc).date()
        symbols = symbols or list(self.stocks_config.default_symbols)

        # Pick the next future earnings per symbol.
        future_by_symbol: dict[str, EarningsEvent] = {}
        for ev in events:
            d = _parse_date(ev.date)
            if d is None or d < today:
                continue
            current = future_by_symbol.get(ev.symbol.upper())
            if current is None or _parse_date(current.date) > d:  # type: ignore[operator]
                future_by_symbol[ev.symbol.upper()] = ev

        rule_intraday = self.stocks_config.earnings_rule("intraday")
        rule_swing = self.stocks_config.earnings_rule("swing")
        rule_invest = self.stocks_config.earnings_rule("invest")

        risks: list[EarningsRisk] = []
        for symbol in symbols:
            up = symbol.upper()
            # PART 18 — ETFs / broad-market indices do not report earnings.
            # The pre-fix path emitted "earnings UNKNOWN — undated event risk"
            # for SPY/QQQ/IWM/DIA/SMH/XLK/XL* and similar, which is a
            # false-positive that quietly weighed against every ETF idea.
            if self.stocks_config.is_etf(up):
                risks.append(
                    EarningsRisk(
                        symbol=up,
                        next_earnings_date=None,
                        days_ahead=None,
                        report_time="n/a",
                        severity="not_applicable",
                        note="ETF — does not report earnings",
                        blocks_swing=False,
                        intraday_high_risk=False,
                    )
                )
                continue
            ev = future_by_symbol.get(up)
            if ev is None:
                risks.append(
                    EarningsRisk(
                        symbol=up,
                        next_earnings_date=None,
                        days_ahead=None,
                        report_time="unknown",
                        severity="unknown",
                        note="no earnings date known",
                        blocks_swing=False,
                        intraday_high_risk=False,
                    )
                )
                continue
            days = (_parse_date(ev.date) - today).days  # type: ignore[operator]
            severity, note = self._severity(days, ev.report_time, mode)

            blocks_swing = (
                bool(rule_swing.get("block_if_days_ahead_le") is not None)
                and days <= int(rule_swing.get("block_if_days_ahead_le", -1))
            )
            intraday_high_risk = (
                days <= int(rule_intraday.get("high_risk_warning_if_days_ahead_le", 0))
            )

            risks.append(
                EarningsRisk(
                    symbol=up,
                    next_earnings_date=ev.date,
                    days_ahead=days,
                    report_time=ev.report_time,
                    severity=severity,
                    note=note,
                    blocks_swing=blocks_swing,
                    intraday_high_risk=intraday_high_risk,
                )
            )

        payload = {
            "mode": mode,
            "as_of_date": today.isoformat(),
            "rules": {
                "intraday": rule_intraday,
                "swing": rule_swing,
                "invest": rule_invest,
            },
            "risks": [asdict(r) for r in risks],
            "blocks_swing": [r.symbol for r in risks if r.blocks_swing],
            "intraday_warnings": [r.symbol for r in risks if r.intraday_high_risk],
        }
        self.save_output(payload)
        return payload

    @staticmethod
    def _severity(days: int, report_time: str, mode: str) -> tuple[str, str]:
        if days <= 0:
            return "active", f"earnings today ({report_time})"
        if days == 1:
            return "next_session", f"earnings next session ({report_time})"
        if days <= 5:
            return "this_week", f"earnings in {days} trading-ish days ({report_time})"
        return "safe", f"next earnings in {days} days"


def _parse_date(value: str) -> date | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None
