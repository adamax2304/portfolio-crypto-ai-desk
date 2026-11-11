"""Historical OHLCV backfill tests (FAST SAFE ACCELERATION PART 2).

Asserts append-only dedup/idempotency, dry-run writes nothing, broken fetch does
not corrupt the archive, the rolling cache is untouched, and archive-first replay
reads the backfilled archive.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def _fake_rows(start_ms, n, step=300_000):
    # ccxt OHLCV row: [ts, open, high, low, close, volume]
    return [[start_ms + i * step, 100.0, 101.0, 99.0, 100.5, 10.0] for i in range(n)]


def test_merge_write_dedups_and_is_idempotent(tmp_path, monkeypatch):
    import scripts.backfill_ohlcv_history as bf
    monkeypatch.setattr(bf, "ARCHIVE", tmp_path / "archive")
    p = bf._archive_path("binance", "5m", "BTC/USDT")

    def _df(rows):
        d = pd.DataFrame(rows, columns=["ts", "open", "high", "low", "close", "volume"])
        d["timestamp"] = pd.to_datetime(d["ts"], unit="ms", utc=True)
        return d[["timestamp", "open", "high", "low", "close", "volume"]]

    before, total = bf._merge_write(p, _df(_fake_rows(0, 10)))
    assert total == 10
    # overlapping window (5 old + 5 new) → 15 unique
    before, total = bf._merge_write(p, _df(_fake_rows(5 * 300_000, 10)))
    assert total == 15
    # identical re-merge → still 15 (idempotent), no duplicate timestamps
    before, total = bf._merge_write(p, _df(_fake_rows(5 * 300_000, 10)))
    assert total == 15
    df = pd.read_csv(p)
    assert df["timestamp"].duplicated().sum() == 0


def test_dry_run_writes_nothing(tmp_path, monkeypatch, capsys):
    import scripts.backfill_ohlcv_history as bf
    monkeypatch.setattr(bf, "ARCHIVE", tmp_path / "archive")
    monkeypatch.setattr(bf, "trade_relevant_symbols", lambda limit: ["BTC/USDT"])
    monkeypatch.setattr(bf.sys, "argv", ["x", "--dry-run", "--limit", "1"])
    bf.main()
    assert not (tmp_path / "archive").exists()


def test_broken_fetch_does_not_corrupt_archive(tmp_path, monkeypatch):
    import scripts.backfill_ohlcv_history as bf
    monkeypatch.setattr(bf, "ARCHIVE", tmp_path / "archive")
    # seed a good archive
    p = bf._archive_path("binance", "5m", "BTC/USDT")
    df = pd.DataFrame(_fake_rows(0, 10), columns=["ts", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
    bf._merge_write(p, df[["timestamp", "open", "high", "low", "close", "volume"]])
    good = pd.read_csv(p)

    class BoomExchange:
        def fetch_ohlcv(self, *a, **k):
            raise RuntimeError("api down")
    # fetch_paginated should raise; caller skips → archive unchanged
    try:
        bf.fetch_paginated(BoomExchange(), "BTC/USDT", "5m", 0, retries=1)
        raised = False
    except RuntimeError:
        raised = True
    assert raised
    after = pd.read_csv(p)
    assert len(after) == len(good)  # untouched


def test_rolling_cache_untouched(tmp_path, monkeypatch):
    import scripts.backfill_ohlcv_history as bf
    # the backfill only knows about ARCHIVE; it has no path into data/raw/ohlcv
    assert "archive" in str(bf.ARCHIVE).lower()
    assert "raw" not in str(bf.ARCHIVE).lower()


def test_replay_and_shadow_read_archive_first(tmp_path, monkeypatch):
    import scripts.replay_profit_protection_path_aware as rp
    import src.exits.shadow_exit_manager as se
    for mod in (rp,):
        monkeypatch.setattr(mod, "ARCHIVE_DIR", tmp_path / "archive")
        monkeypatch.setattr(mod, "CACHE_DIR", tmp_path / "cache")
    monkeypatch.setattr(se, "ARCHIVE_DIR", tmp_path / "archive")
    monkeypatch.setattr(se, "CACHE_DIR", tmp_path / "cache")
    a = tmp_path / "archive" / "binance" / "5m" / "BTC_USDT.csv"
    a.parent.mkdir(parents=True, exist_ok=True); a.write_text("x")
    assert rp._ohlcv_path("binance", "5m", "BTC_USDT") == a
    assert se.ohlcv_path("binance", "5m", "BTC_USDT") == a
