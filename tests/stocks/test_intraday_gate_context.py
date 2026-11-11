"""Integration-bug fixes for the SI-1..SI-5 gate context:
  #1 DataFrame truthiness — `df = _load(...) or _load(...)` raised ValueError whenever 15m data
     existed, so the gates silently fail-opened. The fixed explicit None-fallback must not raise.
  #6 Market-context freshness — a stale archive (yesterday's SPY/QQQ, or a too-old bar) must NOT
     present as a confirmed regime; status becomes 'stale' and the gate demotes.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pandas as pd

from src.stocks import intraday_actionability_gates as g
from src.stocks import intraday_gate_context as igc

UTC = timezone.utc
CFG = {"index_return_conflict_pct": 0.15, "market_context_max_age_sec": 1800, "max_data_age_sec": 900}


def _bars(start_utc, n=4, base=100.0, up=True):
    """n 15m bars on a single UTC day, gently trending up/down."""
    rows = []
    for i in range(n):
        px = base + (i * 0.5 if up else -i * 0.5)
        rows.append({"timestamp": start_utc + timedelta(minutes=15 * i),
                     "open": base, "high": px + 1, "low": base - 1, "close": px, "volume": 1000 + i})
    return pd.DataFrame(rows)


def test_market_context_does_not_raise_on_dataframe(monkeypatch):
    # The core regression: with real 15m data present, market_context must compute — not raise.
    now = datetime(2026, 7, 8, 17, 0, tzinfo=UTC)          # ~13:00 NY (RTH)
    fresh = datetime(2026, 7, 8, 16, 0, tzinfo=UTC)        # same NY day, last bar ~15m before now
    monkeypatch.setattr(igc, "_fs", lambda: SimpleNamespace())
    monkeypatch.setattr(igc, "_load", lambda fs, sym, tf: _bars(fresh, up=True))
    igc._MARKET_CACHE.clear()
    out = igc.market_context(now, CFG)                     # must NOT raise ValueError
    assert out["status"] == "ok"
    assert out["market_context_age_status"] == "fresh"


def test_market_context_stale_when_data_is_yesterday(monkeypatch):
    now = datetime(2026, 7, 8, 17, 0, tzinfo=UTC)
    stale = datetime(2026, 7, 7, 16, 0, tzinfo=UTC)        # prior NY day → stale
    monkeypatch.setattr(igc, "_fs", lambda: SimpleNamespace())
    monkeypatch.setattr(igc, "_load", lambda fs, sym, tf: _bars(stale, up=True))
    igc._MARKET_CACHE.clear()
    out = igc.market_context(now, CFG)
    assert out["status"] == "stale"
    status, reason = g.market_context_gate(direction="long", market_ctx=out, cfg=CFG)
    assert reason == "market_context_unknown_or_stale"     # stale demotes


def test_market_context_stale_when_one_leg_is_yesterday(monkeypatch):
    # SPY fresh (today) but QQQ from yesterday → the freshness check is PER-SYMBOL, so the stale leg
    # must win: status != 'ok' (never take the newest of the two).
    now = datetime(2026, 7, 8, 17, 0, tzinfo=UTC)
    fresh = datetime(2026, 7, 8, 16, 0, tzinfo=UTC)     # SPY: current NY day
    stale = datetime(2026, 7, 7, 16, 0, tzinfo=UTC)     # QQQ: prior NY day
    monkeypatch.setattr(igc, "_fs", lambda: SimpleNamespace())
    monkeypatch.setattr(igc, "_load", lambda fs, sym, tf: _bars(fresh if sym == "SPY" else stale))
    igc._MARKET_CACHE.clear()
    out = igc.market_context(now, CFG)
    assert out["status"] != "ok"                        # stale QQQ leg blocks a confirmed regime
    assert out["status"] == "stale"


def test_market_context_stale_when_bar_too_old_same_day(monkeypatch):
    now = datetime(2026, 7, 8, 19, 0, tzinfo=UTC)
    old = datetime(2026, 7, 8, 15, 0, tzinfo=UTC)          # same NY day but last bar ~2.5h old
    monkeypatch.setattr(igc, "_fs", lambda: SimpleNamespace())
    monkeypatch.setattr(igc, "_load", lambda fs, sym, tf: _bars(old, up=True))
    igc._MARKET_CACHE.clear()
    out = igc.market_context(now, {"market_context_max_age_sec": 1800})
    assert out["status"] == "stale"


def test_market_context_ignores_future_bars_for_historical_now(monkeypatch):
    """An as-of replay must never read bars later than its injected clock."""
    now = datetime(2026, 7, 8, 17, 0, tzinfo=UTC)
    visible = _bars(datetime(2026, 7, 8, 16, 0, tzinfo=UTC), n=4, up=True)
    future = _bars(datetime(2026, 7, 8, 17, 15, tzinfo=UTC), n=2, base=999.0, up=False)
    bars = pd.concat([visible, future], ignore_index=True)
    monkeypatch.setattr(igc, "_fs", lambda: SimpleNamespace())
    monkeypatch.setattr(igc, "_load", lambda fs, sym, tf: bars)
    igc._MARKET_CACHE.clear()

    out = igc.market_context(now, CFG)

    assert out["status"] == "ok"
    assert out["spy_last_ts"] == "2026-07-08T16:45:00+00:00"
    assert out["qqq_last_ts"] == "2026-07-08T16:45:00+00:00"


def test_market_context_rechecks_after_new_benchmark_bar_next_minute(monkeypatch):
    """An early-session unknown must not stay cached for the rest of the hour."""
    start = datetime(2026, 7, 8, 13, 30, tzinfo=UTC)
    frames = {"value": _bars(start, n=1, up=True)}
    calls = {"n": 0}

    def _dynamic_load(fs, sym, tf):
        calls["n"] += 1
        return frames["value"]

    monkeypatch.setattr(igc, "_fs", lambda: SimpleNamespace())
    monkeypatch.setattr(igc, "_load", _dynamic_load)
    igc._MARKET_CACHE.clear()

    early = igc.market_context(datetime(2026, 7, 8, 13, 35, tzinfo=UTC), CFG)
    assert early["status"] == "unknown"

    frames["value"] = _bars(start, n=2, up=True)
    # The second row opens at 13:45 and is valid only after its 14:00 close.
    later = igc.market_context(datetime(2026, 7, 8, 14, 1, tzinfo=UTC), CFG)
    assert later["status"] == "ok"
    assert later["spy_last_ts"] == "2026-07-08T13:45:00+00:00"
    assert calls["n"] >= 4


def test_market_context_still_dedupes_candidates_within_same_minute(monkeypatch):
    now = datetime(2026, 7, 8, 17, 0, 30, tzinfo=UTC)
    calls = {"n": 0}

    def _counted_load(fs, sym, tf):
        calls["n"] += 1
        return _bars(datetime(2026, 7, 8, 16, 0, tzinfo=UTC), up=True)

    monkeypatch.setattr(igc, "_fs", lambda: SimpleNamespace())
    monkeypatch.setattr(igc, "_load", _counted_load)
    igc._MARKET_CACHE.clear()
    first = igc.market_context(now, CFG)
    second = igc.market_context(now.replace(second=55), CFG)

    assert first == second
    assert calls["n"] == 2


def test_sector_context_does_not_raise_on_dataframe(monkeypatch):
    # Force a sector ETF to resolve so the fixed line 135 fallback is actually exercised with a
    # real DataFrame (in production stocks_config is None so this path is otherwise latent).
    import src.config as _cfgmod
    fake_sc = SimpleNamespace(sector_etf_for=lambda s: "SMH")
    monkeypatch.setattr(_cfgmod, "load_config", lambda: SimpleNamespace(stocks_config=fake_sc))
    now = datetime(2026, 7, 8, 17, 0, tzinfo=UTC)
    monkeypatch.setattr(igc, "_load", lambda fs, sym, tf: _bars(datetime(2026, 7, 8, 16, 0, tzinfo=UTC)))
    out = igc.sector_context(SimpleNamespace(), "NVDA", "long", {"rs_vs_spy": 1.0}, now,
                             {"sector_return_conflict_pct": 0.15})     # must NOT raise ValueError
    assert out["sector_etf"] == "SMH"
    assert out["status"] in ("confirmed", "weak", "conflict", "unknown")


def test_sector_context_uses_configured_etf_and_same_session_15m_rs(monkeypatch):
    now = datetime(2026, 7, 8, 17, 0, tzinfo=UTC)

    def frame(start, closes):
        return pd.DataFrame({
            "timestamp": [start, start + timedelta(minutes=15)],
            "open": [100.0, 100.0], "high": [101.0, closes[-1] + 0.5],
            "low": [99.5, 99.5], "close": closes, "volume": [1_000, 1_200],
        })

    start = datetime(2026, 7, 8, 16, 0, tzinfo=UTC)
    frames = {
        "AAPL": frame(start, [100.0, 102.0]),
        "SPY": frame(start, [100.0, 100.5]),
        "XLK": frame(start, [100.0, 100.8]),
    }
    monkeypatch.setattr(igc, "_load", lambda _fs, sym, _tf: frames.get(sym))
    out = igc.sector_context(SimpleNamespace(), "AAPL", "long", {}, now,
                             {"sector_return_conflict_pct": 0.15})
    assert out["sector_etf"] == "XLK"
    assert out["rs_timeframe"] == "15m_rth_same_session"
    assert out["rs_vs_spy"] > 0 and out["rs_vs_sector"] > 0
    assert out["status"] == "confirmed"


def test_liquidity_uses_time_of_day_15m_rvol_not_technical_hourly_ratio(monkeypatch):
    now = datetime(2026, 7, 8, 13, 46, tzinfo=UTC)
    bars = pd.DataFrame([
        {"timestamp": "2026-07-07T13:30:00+00:00", "open": 100, "high": 101,
         "low": 99, "close": 100, "volume": 100},
        {"timestamp": "2026-07-08T13:30:00+00:00", "open": 100, "high": 101,
         "low": 99, "close": 100, "volume": 200},
    ])
    monkeypatch.setattr(igc, "_load", lambda _fs, _sym, _tf: bars)
    out = igc.liquidity_from_ohlcv(SimpleNamespace(), "AAPL", {"volume_ratio": 0.1}, now,
                                   {"max_data_age_sec": 900})
    assert out["rvol"] == 2.0
    assert out["spread_estimation_method"] == "intrabar_range_proxy_not_bid_ask"
    assert out["data_freshness_status"] == "fresh"
    assert out["data_age_seconds"] == 60.0
    assert out["last_closed_bar_at"] == "2026-07-08T13:45:00+00:00"


def test_liquidity_ignores_incomplete_current_bar_and_ages_from_bar_close(monkeypatch):
    now = datetime(2026, 7, 8, 13, 50, tzinfo=UTC)
    bars = pd.DataFrame([
        {"timestamp": "2026-07-07T13:30:00+00:00", "open": 100, "high": 101,
         "low": 99, "close": 100, "volume": 100},
        {"timestamp": "2026-07-08T13:30:00+00:00", "open": 100, "high": 101,
         "low": 99, "close": 100, "volume": 200},
        # Partial 13:45 bar must not inflate RVOL before it closes at 14:00.
        {"timestamp": "2026-07-08T13:45:00+00:00", "open": 100, "high": 110,
         "low": 90, "close": 109, "volume": 10000},
    ])
    monkeypatch.setattr(igc, "_load", lambda _fs, _sym, _tf: bars)

    out = igc.liquidity_from_ohlcv(
        SimpleNamespace(), "AAPL", {}, now, {"max_data_age_sec": 900}
    )

    assert out["rvol"] == 2.0
    assert out["last_closed_bar_at"] == "2026-07-08T13:45:00+00:00"
    assert out["data_age_seconds"] == 300.0
    assert out["data_freshness_status"] == "fresh"


def test_liquidity_stale_boundary_uses_elapsed_time_after_bar_close(monkeypatch):
    bars = pd.DataFrame([
        {"timestamp": "2026-07-07T13:30:00+00:00", "open": 100, "high": 101,
         "low": 99, "close": 100, "volume": 100},
        {"timestamp": "2026-07-08T13:30:00+00:00", "open": 100, "high": 101,
         "low": 99, "close": 100, "volume": 200},
    ])
    monkeypatch.setattr(igc, "_load", lambda _fs, _sym, _tf: bars)

    fresh = igc.liquidity_from_ohlcv(
        SimpleNamespace(), "AAPL", {},
        datetime(2026, 7, 8, 14, 0, tzinfo=UTC), {"max_data_age_sec": 900},
    )
    stale = igc.liquidity_from_ohlcv(
        SimpleNamespace(), "AAPL", {},
        datetime(2026, 7, 8, 14, 1, tzinfo=UTC), {"max_data_age_sec": 900},
    )

    assert fresh["data_age_seconds"] == 900.0
    assert fresh["data_freshness_status"] == "fresh"
    assert stale["data_age_seconds"] == 960.0
    assert stale["data_freshness_status"] == "stale"
