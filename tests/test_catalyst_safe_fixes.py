"""Tests for catalyst/news/derivatives safe additive fixes (2026-06-15)."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from src.signals.catalyst_labels import compute_labels, telegram_block, move_type
from src.notifiers.setup_alert import render_setup_alert
from src.notifiers.paper_entry import decide_paper_entry


# ---- PART 1: stocks news_supported label ---------------------------------

def _stock_idea(news_count: int):
    from src.models import TradeIdea
    return TradeIdea(
        symbol="AAPL", direction="long", score=72.0, confidence="medium",
        risk_level="medium", timeframe="15m/1h", tier="B", mode="intraday",
        asset_class="stocks", exchange_focus="US", exchanges_confirmed=["US"],
        data_confidence="medium", thesis="AAPL momentum", evidence=["e"],
        counterarguments=["c"], entry_plan="zone", invalidation="251",
        targets=["257"], what_to_monitor=["SPY"], avoid_conditions=[],
        data_sources_used=["yfinance", "rss_news"],
        raw={
            "setup": {"entry_low": 254.0, "entry_high": 254.5, "invalidation": 251.0,
                      "tp1": 257.0, "tp2": 259.0, "tp3": 263.0},
            "news_count": news_count,
            "catalyst_meta": {"headline_short": "AAPL upgrade", "source": "CNBC",
                              "published_at": "2026-06-15T08:00:00+00:00"},
        },
    )


def test_1_registry_sets_news_supported_for_stocks_with_news():
    """A stocks idea carrying ticker-specific news_count>0 → news_supported=1."""
    from src.signals.registry import build_signal_from_idea
    from src.signals.config import load_signal_tracking_config
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    sig = build_signal_from_idea(_stock_idea(3), config=cfg, report_id="r1",
                                 market_regime="bullish", weekend_mode_active=False)
    assert sig is not None
    assert bool(sig.news_supported) is True


def test_2_registry_no_news_supported_without_news():
    from src.signals.registry import build_signal_from_idea
    from src.signals.config import load_signal_tracking_config
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    sig = build_signal_from_idea(_stock_idea(0), config=cfg, report_id="r1",
                                 market_regime="bullish", weekend_mode_active=False)
    assert sig is not None
    assert bool(sig.news_supported) is False


# ---- PART 2: funding/OI archive ------------------------------------------

def _fresh_store(tmp_path):
    from src.storage.sqlite import SQLiteStore
    st = SQLiteStore(tmp_path / "arch.sqlite")
    st.init_db()
    return st


def test_3_funding_snapshot_insert_and_dedup(tmp_path):
    st = _fresh_store(tmp_path)
    ins = st.record_funding_snapshot(
        fetched_at="2026-06-15T10:00:00+00:00", exchange="binance",
        symbol="ZEC/USDT", funding_rate=0.0001, crowding_label="normal")
    dup = st.record_funding_snapshot(
        fetched_at="2026-06-15T10:00:00+00:00", exchange="binance", symbol="ZEC/USDT")
    assert ins is True
    assert dup is False
    with st.connect() as c:
        assert c.execute("SELECT COUNT(*) FROM funding_snapshots").fetchone()[0] == 1


def test_4_oi_snapshot_insert(tmp_path):
    st = _fresh_store(tmp_path)
    ins = st.record_oi_snapshot(
        fetched_at="2026-06-15T10:00:00+00:00", exchange="binance",
        symbol="ZEC/USDT", oi_value=1000.0, oi_change_pct=5.0)
    assert ins is True
    with st.connect() as c:
        assert c.execute("SELECT COUNT(*) FROM oi_snapshots").fetchone()[0] == 1


def test_5_archive_helper_best_effort_no_raise(tmp_path):
    """archive_derivatives_records never raises and skips failed records."""
    from src.data_collectors.derivatives_archive import archive_derivatives_records
    st = _fresh_store(tmp_path)
    records = {
        "ZEC/USDT": {"fetched_at": "2026-06-15T10:00:00+00:00",
                     "premium_index": {"lastFundingRate": "0.0001", "markPrice": "42.1"},
                     "open_interest": {"openInterest": "1000"},
                     "long_short_ratio": [{"longShortRatio": "1.2"}]},
        "BAD/USDT": {"data_available": False, "error": "no market"},
    }
    out = archive_derivatives_records(st, records, exchange="binance")
    assert out["funding"] == 1  # BAD skipped
    assert out["oi"] == 1
    # None store → no raise
    out2 = archive_derivatives_records(None, records, exchange="binance")
    assert out2["funding"] == 0


def test_6_archive_not_read_by_scoring():
    """No production scoring module imports the archive helper."""
    import re
    root = Path(__file__).resolve().parents[1]
    for fname in ("src/agents/scoring_agent.py", "src/stocks/agents/scoring_agent.py"):
        text = (root / fname).read_text(encoding="utf-8")
        assert "derivatives_archive" not in text
        assert "funding_snapshots" not in text
        assert "oi_snapshots" not in text


# ---- PART 3/4: catalyst labels + telegram --------------------------------

def _crypto_catalyst_signal():
    return {
        "asset_class": "crypto", "symbol": "ZEC/USDT", "direction": "long",
        "mode": "swing", "tier": "B", "score": 74.0, "news_supported": 1,
        "funding_context": "funding=0.0001, crowding=normal",
        "oi_context": "price up + OI up: fresh positioning",
        "entry_low": 42.0, "entry_high": 42.3, "stop_loss": 40.8,
        "tp1": 43.2, "tp2": 44.5, "tp3": 46.0, "setup_type": "breakout",
        "signal_id": "sig_cat",
        "raw_idea_json": json.dumps({"catalyst_meta": {
            "headline_short": "ZEC listing", "source": "CoinDesk",
            # ~2h before now so freshness is deterministically "recent" (not
            # wall-clock-dependent on a fixed date).
            "published_at": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
            "importance": 6}}),
    }


def test_7_crypto_catalyst_labels():
    lab = compute_labels(_crypto_catalyst_signal())
    assert lab.catalyst_freshness.startswith(("fresh", "recent"))
    assert lab.source_quality == "reputable"
    assert lab.derivatives_label == "OI-up"
    assert lab.symbol_mapping == "exact"


def test_8_technical_signal_labels_none():
    tech = {"asset_class": "crypto", "news_supported": 0,
            "funding_context": "funding=0.0001, crowding=normal", "oi_context": "no squeeze"}
    lab = compute_labels(tech)
    assert lab.catalyst_freshness == "none"
    assert lab.derivatives_label != "squeeze-risk"  # "no squeeze" must NOT be risk
    assert move_type(tech) == "technical momentum"


def test_9_telegram_block_catalyst_backed():
    block = telegram_block(_crypto_catalyst_signal())
    assert any("Catalyst:" in l and "none" not in l for l in block)
    assert any("Move type: catalyst-backed" in l for l in block)


def test_10_telegram_block_stocks_not_available():
    stk = {"asset_class": "stocks", "news_supported": 1,
           "raw_idea_json": json.dumps({"catalyst_meta": {"headline_short": "AAPL up",
                                                          "source": "CNBC",
                                                          "published_at": "2026-06-15T08:00:00+00:00"}})}
    block = telegram_block(stk)
    assert any("not available for stocks" in l for l in block)


def test_11_setup_alert_includes_catalyst_block():
    msg = render_setup_alert(_crypto_catalyst_signal())
    assert "Catalyst:" in msg
    assert "Funding (8h):" in msg
    assert "Open interest:" in msg
    assert "Move type:" in msg
    # crypto setup still has its header + disclaimer
    assert "SETUP — WAITING FOR ENTRY" in msg
    assert "No paper entry yet." in msg


def test_12_paper_entry_includes_catalyst_block_and_disclaimer():
    d = decide_paper_entry(_crypto_catalyst_signal(), prev_status="waiting_for_entry",
                           entry_triggered=True,
                           entry_triggered_at="2026-06-15T15:00:00+00:00",
                           entry_price_used=42.15)
    assert d.should_send is True
    assert "Catalyst:" in d.message
    assert "Paper entry recorded. MEXC execution is confirmed separately after preflight." in d.message


def test_13_technical_setup_alert_shows_catalyst_none():
    tech = {**_crypto_catalyst_signal(), "news_supported": 0, "signal_id": "sig_t",
            "raw_idea_json": json.dumps({})}
    msg = render_setup_alert(tech)
    assert "Catalyst: none" in msg


# ---- invariants ----------------------------------------------------------

def test_14_label_helper_is_pure_no_score_fields():
    """compute_labels never returns or mutates score/tier."""
    sig = _crypto_catalyst_signal()
    before = dict(sig)
    compute_labels(sig)
    assert sig == before  # not mutated
