"""Operational deployment wiring tests (deploy stage PARTS 1/4/5/6).

Covers: scheduler includes the 3 new non-fatal steps; OHLCV archive is append-only
and dedups timestamps; coverage report is honest when empty; replay prefers the
archive over the rolling cache.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


def test_scheduler_includes_new_nonfatal_steps():
    import scripts.run_default_market_schedule as s
    steps = s.build_cycle_steps(
        now=datetime(2026, 6, 17, 14, 0, tzinfo=timezone.utc),
        crypto_only=False, include_long_horizon=False, monitor_minutes=90,
        skip_reports=False)
    labels = {label: kind for label, _argv, kind, _dur in steps}
    for needed in ("catalyst integrity scan", "ohlcv archive (5m/15m)",
                   "open intraday lifecycle review"):
        assert needed in labels, f"missing scheduler step: {needed}"
        assert labels[needed] == "command_nonfatal", f"{needed} must be non-fatal"
    # catalyst integrity must come AFTER the catalyst scan
    order = [label for label, *_ in steps]
    assert order.index("catalyst integrity scan") > order.index("catalyst / narrative scan")


def _write_csv(path: Path, start_min: int, n: int):
    base = datetime(2026, 6, 17, 0, 0, tzinfo=timezone.utc)
    ts = [base.replace(minute=0) for _ in range(n)]
    rows = {
        "timestamp": [pd.Timestamp(base) + pd.Timedelta(minutes=5 * (start_min + i)) for i in range(n)],
        "open": [100.0] * n, "high": [101.0] * n, "low": [99.0] * n,
        "close": [100.5] * n, "volume": [10.0] * n,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(path, index=False)


def test_archive_append_dedups_and_is_idempotent(tmp_path, monkeypatch):
    import scripts.archive_ohlcv_history as arch
    monkeypatch.setattr(arch, "CACHE", tmp_path / "raw" / "ohlcv")
    monkeypatch.setattr(arch, "ARCHIVE", tmp_path / "archive" / "ohlcv")
    monkeypatch.setattr(arch, "EXCHANGES", ("binance",))
    # window 1: candles 0..9
    _write_csv(arch.CACHE / "binance" / "5m" / "BTC_USDT.csv", 0, 10)
    r1 = arch.run_archive(["5m"], ["binance"], dry_run=False)
    assert r1["per_tf"]["5m"]["archive_candles"] == 10
    # window 2: candles 5..14 (5 overlap, 5 new)
    _write_csv(arch.CACHE / "binance" / "5m" / "BTC_USDT.csv", 5, 10)
    r2 = arch.run_archive(["5m"], ["binance"], dry_run=False)
    assert r2["per_tf"]["5m"]["archive_candles"] == 15  # 10 + 5 new, deduped
    assert r2["per_tf"]["5m"]["appended"] == 5
    # re-run identical → 0 new (idempotent)
    r3 = arch.run_archive(["5m"], ["binance"], dry_run=False)
    assert r3["per_tf"]["5m"]["appended"] == 0
    # no duplicate timestamps in the archive
    df = pd.read_csv(arch.ARCHIVE / "binance" / "5m" / "BTC_USDT.csv")
    assert df["timestamp"].duplicated().sum() == 0


def test_archive_dry_run_does_not_write(tmp_path, monkeypatch):
    import scripts.archive_ohlcv_history as arch
    monkeypatch.setattr(arch, "CACHE", tmp_path / "raw" / "ohlcv")
    monkeypatch.setattr(arch, "ARCHIVE", tmp_path / "archive" / "ohlcv")
    monkeypatch.setattr(arch, "EXCHANGES", ("binance",))
    _write_csv(arch.CACHE / "binance" / "5m" / "BTC_USDT.csv", 0, 10)
    arch.run_archive(["5m"], ["binance"], dry_run=True)
    assert not (arch.ARCHIVE / "binance" / "5m" / "BTC_USDT.csv").exists()


def test_coverage_report_honest_when_empty(tmp_path, monkeypatch):
    import scripts.archive_ohlcv_history as arch
    monkeypatch.setattr(arch, "ARCHIVE", tmp_path / "archive" / "ohlcv")
    rep = arch.coverage_report(["5m"], ["binance"])
    assert "empty" in rep.lower() or "no archive" in rep.lower()


def test_replay_prefers_archive_over_cache(tmp_path, monkeypatch):
    import scripts.replay_profit_protection_path_aware as rp
    monkeypatch.setattr(rp, "ARCHIVE_DIR", tmp_path / "archive" / "ohlcv")
    monkeypatch.setattr(rp, "CACHE_DIR", tmp_path / "raw" / "ohlcv")
    cache_p = rp.CACHE_DIR / "binance" / "5m" / "BTC_USDT.csv"
    arch_p = rp.ARCHIVE_DIR / "binance" / "5m" / "BTC_USDT.csv"
    cache_p.parent.mkdir(parents=True, exist_ok=True)
    cache_p.write_text("x")
    # only cache exists → cache chosen
    assert rp._ohlcv_path("binance", "5m", "BTC_USDT") == cache_p
    arch_p.parent.mkdir(parents=True, exist_ok=True)
    arch_p.write_text("x")
    # both exist → archive preferred
    assert rp._ohlcv_path("binance", "5m", "BTC_USDT") == arch_p
