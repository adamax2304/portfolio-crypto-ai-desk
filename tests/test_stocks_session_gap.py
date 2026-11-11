"""Stocks realtime provider + session-gap classification (2026-07-05). Read-only; no live."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from src.stocks import realtime_provider as rp

# 2026-07-06 is a Monday (not an NYSE holiday); 14:00 UTC = 10:00 ET → inside RTH (09:30-16:00).
RTH = datetime(2026, 7, 6, 14, 0, tzinfo=timezone.utc)
PREMARKET = datetime(2026, 7, 6, 12, 0, tzinfo=timezone.utc)   # 08:00 ET
WEEKEND = datetime(2026, 7, 4, 14, 0, tzinfo=timezone.utc)     # Saturday


def test_session_gap_outside_rth_is_session_gap():
    assert rp.classify_session_gap(PREMARKET)["classification"] == "SESSION_GAP"
    assert rp.classify_session_gap(WEEKEND)["classification"] == "SESSION_GAP"


def test_in_session_no_bar_is_data_gap_late():
    r = rp.classify_session_gap(RTH, first_bar_ts=None)
    assert r["classification"] == "DATA_GAP_LATE"


def test_in_session_late_first_bar_is_data_gap_late():
    r = rp.classify_session_gap(RTH, first_bar_ts=RTH + timedelta(minutes=45))
    assert r["classification"] == "DATA_GAP_LATE" and r["first_bar_gap_min"] == 45.0


def test_in_session_fresh_bar_is_ok():
    r = rp.classify_session_gap(RTH, first_bar_ts=RTH + timedelta(minutes=5))
    assert r["classification"] == "OK" and r["first_bar_gap_min"] == 5.0


def test_provider_statuses_yfinance_not_live_grade(monkeypatch):
    for env in ("FINNHUB_API_KEY", "ALPACA_API_KEY", "POLYGON_API_KEY", "IEX_API_KEY", "IBKR_ACCOUNT"):
        # Empty is intentional: the provider helper loads local .env for real workers, but an
        # explicitly empty test environment must exercise the no-credential fallback.
        monkeypatch.setenv(env, "")
    st = {s.name: s for s in rp.provider_statuses()}
    assert st["yfinance"].live_grade is False and st["yfinance"].enabled is True
    if "alpaca" in st:
        assert st["alpaca"].enabled is False           # no key → disabled
    # active provider falls back to yfinance (not live-grade) when no live key present
    assert rp.active_provider().name == "yfinance"
    assert rp.active_provider().live_grade is False


def test_env_gated_live_provider_enables_with_key(monkeypatch):
    monkeypatch.setenv("ALPACA_API_KEY", "key")
    monkeypatch.setenv("ALPACA_API_SECRET", "secret")
    st = {s.name: s for s in rp.provider_statuses()}
    if "alpaca" in st:
        assert st["alpaca"].enabled is True and st["alpaca"].live_grade is True
        assert rp.active_provider().name == "alpaca"    # live-grade provider preferred when enabled


def test_alpaca_requires_both_key_and_secret(monkeypatch):
    monkeypatch.setenv("ALPACA_API_KEY", "key")
    monkeypatch.setenv("ALPACA_API_SECRET", "")
    st = {s.name: s for s in rp.provider_statuses()}
    assert st["alpaca"].enabled is False
    assert "ALPACA_API_SECRET" in st["alpaca"].reason


def test_stocks_intraday_promotion_stays_blocked():
    st = rp.stocks_intraday_status()
    assert st["promotion_blocked"] is True              # hard-locked regardless of latency


def test_stocks_status_uses_recent_ab_data_gap_not_lifetime_history(monkeypatch):
    from types import SimpleNamespace
    from src.signals import latency_readmodel, latency_sla

    monkeypatch.setattr(rp, "active_provider", lambda: rp.ProviderStatus(
        "alpaca", True, True, "test provider"))
    monkeypatch.setattr(rp, "provider_statuses", lambda: [
        rp.ProviderStatus("finnhub", True, True, "test quote")])
    monkeypatch.setattr(latency_readmodel, "data_gap_diagnostics", lambda *a, **kw: {
        "by_mode": [{
            "asset_class": "stocks", "mode": "intraday",
            "actionable_data_gap_late_share": 0.33,
            "recent_actionable_data_gap_late_share": 0.0,
            "recent_actionable_n": 57,
        }]
    })
    monkeypatch.setattr(latency_sla, "sla_report", lambda *a, **kw: {
        "acceptance": {"stocks_intraday": {
            "after_bar_close_lower_bound_sec": {"p90": 35.0}}},
        "sla_thresholds": {"stocks_intraday_entry_detect_p90_sec": 300},
    })

    status = rp.stocks_intraday_status(db="unused-test-db")
    assert status["live_promotion_blocked"] is True
    assert status["data_gap_late_share"] == 0.0
    assert status["data_gap_late_share_all_time"] == 0.33
    assert status["data_gap_recent_sample_n"] == 57
    assert status["paper_forward_testing_allowed"] is True
    assert not any("DATA_GAP_LATE" in reason for reason in status["reasons"])
