"""Move 1 — deep-history store + paginated backfill pager + settings replay.

Scope guardrails: everything here is offline/read-model. The deep store is a
SEPARATE tree; the pager and replay never touch the live rolling cache, live
collectors, proposed_signals, signal_outcomes / final_r, or any live path.
"""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pandas as pd

from src.backtest import historical_store as hist
from src.backtest import settings_replay as sr
from src.data_collectors.historical_ohlcv_backfill import HistoricalOHLCVBackfiller

_STEP_15M = 900_000


def _cfg(tmp_path) -> SimpleNamespace:
    # historical_store only needs raw_dir; the deep loader also uses anchor_exchange.
    return SimpleNamespace(raw_dir=tmp_path / "data" / "raw", anchor_exchange="binance")


def _frame(start_ms, n, step=_STEP_15M, base=100.0):
    rows = [[start_ms + i * step, base, base + 1, base - 1, base + 0.5, 1.0] for i in range(n)]
    f = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
    f["timestamp"] = pd.to_datetime(f["timestamp"], unit="ms", utc=True)
    return f


# ------------------------------------------------------------------ store
def test_store_merge_dedups_and_sorts(tmp_path):
    cfg = _cfg(tmp_path)
    a = _frame(1_000_000_000_000, 100)
    b = _frame(1_000_000_000_000 + 50 * _STEP_15M, 100)   # 50-bar overlap with a
    hist.save_merge(cfg, "binance", "BTC/USDT", "15m", a)
    r = hist.save_merge(cfg, "binance", "BTC/USDT", "15m", b)
    loaded = hist.load(cfg, "binance", "BTC/USDT", "15m")
    assert len(loaded) == 150                              # 100 + 100 - 50 overlap, deduped
    assert loaded["timestamp"].is_monotonic_increasing     # sorted
    assert loaded["timestamp"].is_unique                   # no dup timestamps
    assert r["rows_after"] == 150 and r["added"] == 50


def test_store_separate_tree_from_rolling_cache(tmp_path):
    cfg = _cfg(tmp_path)
    p = hist.history_path(cfg, "binance", "BTC/USDT", "15m")
    assert "history" in p.parts and "raw" not in p.parts   # never under data/raw/ohlcv


# ------------------------------------------------------------------ pager
class _FakeEx:
    """fetch_ohlcv returns partial pages (<limit) — the case a naive pager stops on."""
    def __init__(self, start_ms, n, step=_STEP_15M, page=999):
        self.bars = [[start_ms + i * step, 100, 101, 99, 100, 1.0] for i in range(n)]
        self.page = page
        self.markets = {"BTC/USDT": {}}
        self.calls = 0

    def fetch_ohlcv(self, symbol, timeframe=None, since=None, limit=1000):
        self.calls += 1
        rows = [b for b in self.bars if b[0] >= since]
        return rows[: min(limit, self.page)]


def test_pager_loops_past_partial_pages(tmp_path):
    start = 1_000_000_000_000
    n = 2500
    fake = _FakeEx(start, n, page=999)                     # 999 < 1000 limit ⇒ partial pages
    bf = HistoricalOHLCVBackfiller(_cfg(tmp_path))
    rows = bf._fetch_paged(fake, "BTC/USDT", "15m", start, start + (n - 1) * _STEP_15M)
    uniq = {r[0] for r in rows}
    assert len(uniq) == n                                  # every bar collected despite partial pages
    assert fake.calls >= 3                                 # forced to page multiple times


class _StuckEx:
    markets = {"BTC/USDT": {}}
    def fetch_ohlcv(self, symbol, timeframe=None, since=None, limit=1000):
        return [[1_000, 1, 1, 1, 1, 1]]                    # never advances


def test_pager_stops_when_cursor_not_advancing(tmp_path):
    bf = HistoricalOHLCVBackfiller(_cfg(tmp_path), max_requests_per_series=50)
    rows = bf._fetch_paged(_StuckEx(), "BTC/USDT", "15m", 1_000, 9_999_999)
    assert rows                                            # returned something
    # did not spin to the request cap: broke on non-advancing cursor
    assert len(rows) <= 3


def test_backfill_writes_deep_store_not_live_cache(tmp_path, monkeypatch):
    start = 1_700_000_000_000
    fake = _FakeEx(start, 300, page=999)
    cfg = SimpleNamespace(raw_dir=tmp_path / "data" / "raw", anchor_exchange="binance",
                          exchange_ccxt_id=lambda e: e, exchange_alias=lambda e, s: s)
    bf = HistoricalOHLCVBackfiller(cfg)
    monkeypatch.setattr(bf, "_build_exchange", lambda ex: fake)
    summ = bf.backfill(["BTC/USDT"], timeframes=("15m",), days=5, now_ms=start + 300 * _STEP_15M).as_dict()
    assert summ["symbols_fetched"] == 1 and summ["bars_added"] == 300
    # landed in the deep store, and NOT in the live rolling cache tree
    assert hist.load(cfg, "binance", "BTC/USDT", "15m") is not None
    assert not (cfg.raw_dir / "ohlcv").exists()


# ------------------------------------------------------------------ deep loader
def test_deep_loader_slices_to_created_at(tmp_path):
    cfg = _cfg(tmp_path)
    start = 1_600_000_000_000
    hist.save_merge(cfg, "binance", "ETH/USDT", "15m", _frame(start, 400))
    created = pd.to_datetime(start + 200 * _STEP_15M, unit="ms", utc=True).isoformat()
    full, ex, tf = sr.load_deep_frame(cfg, "ETH/USDT", "scalp", "")
    assert ex == "binance" and tf in ("5m", "15m", "1h") and len(full) == 400
    post, _, _ = sr.load_deep_candles(cfg, "ETH/USDT", "scalp", "", created)
    assert post is not None and len(post) == 200          # only candles at/after creation


# ------------------------------------------------------------------ read-only / no live surface
def test_modules_have_no_live_or_write_surface():
    for mod in (hist, sr):
        src = Path(mod.__file__).read_text(encoding="utf-8").lower()
        for bad in ("create_order", "place_order", "submit_order", "auto_live", "manual_live",
                    "final_r =", "insert into proposed_signals", "update proposed_signals",
                    "insert into signal_outcomes", "update signal_outcomes"):
            assert bad not in src, (mod.__name__, bad)


def test_settings_replay_opens_source_read_only():
    src = Path(sr.__file__).read_text(encoding="utf-8")
    assert "mode=ro" in src                                # proposed_signals read strictly read-only
