"""Tests for the 2026-06-16 Option B coverage fix: pending-symbol OHLCV refresh +
timeframe-aware freshness + audit join correctness."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.signals.pending_symbol_universe import select_pending_tracking_symbols, pending_symbols
from src.signals.pending_monitor import needed_timeframes
from src.notifiers.paper_entry import entry_freshness

ROOT = Path(__file__).resolve().parents[1]


def _store(tmp_path):
    from src.storage.sqlite import SQLiteStore
    st = SQLiteStore(tmp_path / "t.sqlite"); st.init_db(); return st


def _insert(st, sid, symbol, tier, status, asset="crypto", mode="intraday", created="2026-06-16T13:00:00+00:00"):
    with st.connect() as c:
        c.execute(
            "INSERT INTO proposed_signals(signal_id, created_at, updated_at, symbol, "
            "direction, mode, tier, score, asset_class, status) VALUES(?,?,?,?,?,?,?,?,?,?)",
            (sid, created, created, symbol, "long", mode, tier, 70.0, asset, status),
        )
        c.commit()


# ---- pending-symbol universe ----------------------------------------------

def test_1_includes_discovery_alt_ab_waiting(tmp_path):
    st = _store(tmp_path)
    _insert(st, "s1", "ASTER/USDT", "B", "waiting_for_entry")
    _insert(st, "s2", "HMSTR/USDT", "A", "triggered", mode="swing")
    syms = set(pending_symbols(st, asset_class="crypto"))
    assert "ASTER/USDT" in syms and "HMSTR/USDT" in syms


def test_2_excludes_c_tier(tmp_path):
    st = _store(tmp_path)
    _insert(st, "s1", "RIF/USDT", "C", "waiting_for_entry")
    assert "RIF/USDT" not in set(pending_symbols(st, asset_class="crypto"))


def test_3_excludes_terminal_statuses(tmp_path):
    st = _store(tmp_path)
    _insert(st, "s1", "XPL/USDT", "B", "expired")
    _insert(st, "s2", "ALLO/USDT", "B", "stopped")
    _insert(st, "s3", "ZEC/USDT", "B", "tp3_hit")
    assert set(pending_symbols(st, asset_class="crypto")) == set()


def test_4_distinct_symbols_and_metadata(tmp_path):
    st = _store(tmp_path)
    _insert(st, "s1", "WLD/USDT", "B", "waiting_for_entry")
    _insert(st, "s2", "WLD/USDT", "B", "triggered")   # dup symbol → one entry
    rows = select_pending_tracking_symbols(st, asset_class="crypto")
    assert len([r for r in rows if r["norm"] == "WLD/USDT"]) == 1
    assert rows[0]["tier"] == "B" and rows[0]["mode"] in {"intraday", "swing"}


def test_5_scalp_included_but_toggleable_and_deprioritized(tmp_path):
    st = _store(tmp_path)
    _insert(st, "s1", "SOL/USDT", "B", "waiting_for_entry", mode="scalp")
    _insert(st, "s2", "SUI/USDT", "B", "waiting_for_entry", mode="intraday")
    syms = pending_symbols(st, asset_class="crypto")
    assert "SOL/USDT" in syms                                   # scalp included (research)
    assert syms.index("SUI/USDT") < syms.index("SOL/USDT")      # non-scalp prioritized
    assert "SOL/USDT" not in pending_symbols(st, asset_class="crypto", include_scalp=False)


def test_6_store_error_fails_safe():
    class _Bad:
        def load_active_signals(self): raise RuntimeError("db down")
    assert select_pending_tracking_symbols(_Bad()) == []     # no crash


# ---- timeframe-aware freshness --------------------------------------------

def _ago(minutes):
    return (datetime.now(timezone.utc) - timedelta(minutes=minutes)).isoformat()


def test_7_crypto_intraday_thresholds_unchanged(tmp_path):
    # 1.5m fresh, 4m acceptable, 12m late, 20m very_late (actionable=False)
    assert entry_freshness(_ago(1.5), asset_class="crypto", mode="intraday")[2] is True
    lbl, _, act = entry_freshness(_ago(20), asset_class="crypto", mode="intraday")
    assert act is False and "very late" in lbl


def test_8_crypto_scalp_thresholds_tight(tmp_path):
    lbl, _, act = entry_freshness(_ago(20), asset_class="crypto", mode="scalp")
    assert act is False  # scalp stays tight (shadow anyway)


def test_9_stocks_intraday_16_24m_not_very_late(tmp_path):
    # 16–24m detection on 15m-candle stocks must be actionable (not very_late)
    for mins in (16, 20, 24):
        lbl, _, act = entry_freshness(_ago(mins), asset_class="stocks", mode="intraday")
        assert act is True, (mins, lbl)
        assert "candle floor" in lbl          # mandatory price-check note present
    # but a genuinely stale 50m stock entry IS very_late
    assert entry_freshness(_ago(50), asset_class="stocks", mode="intraday")[2] is False


def test_10_default_threshold_unchanged_for_unknown(tmp_path):
    # unknown mode falls back to tight 2/5/15 default
    assert entry_freshness(_ago(20), asset_class="crypto", mode="???")[2] is False


# ---- structural guards -----------------------------------------------------

def test_11_refresh_runs_before_pending_tracker_in_cli():
    src = (ROOT / "src" / "cli.py").read_text(encoding="utf-8")
    i_refresh = src.find("pending OHLCV refresh")
    i_track = src.find("track_pending_entries(")
    assert 0 < i_refresh < i_track  # refresh block precedes the tracker call


def test_12_latency_audit_joins_by_signal_id():
    src = (ROOT / "scripts" / "audit_latency_expired.py").read_text(encoding="utf-8")
    # paper_entry alert linkage must be GROUP BY signal_id, not symbol+mode
    assert "alert_type='paper_entry' GROUP BY signal_id" in src
    assert "symbol=? AND mode=?" not in src


def test_pending_monitor_keeps_1m_for_crypto_intraday_execution_provenance(tmp_path):
    st = _store(tmp_path)
    _insert(st, "s1", "ETH/USDT", "A", "waiting_for_entry", mode="intraday")
    assert needed_timeframes(st, ["1m", "5m", "15m", "1h"]) == ["1m", "15m", "1h"]
