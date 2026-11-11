"""Tests: market dashboard Opus parser + fallback (PAPER/display)."""
import sqlite3
import tempfile, os

from src.market.market_dashboard import (extract_market_block, parse_and_store,
                                          deterministic_fallback, ensure_table)

_SAMPLE = '''Enriched review prose here.
Some analysis.

```json
{"market_dashboard_update": {
  "timestamp": "2026-06-24T17:00:00Z",
  "crypto_fear_greed": 52,
  "crypto_market_mode": "chop",
  "stocks_market_mode": "risk_off",
  "crypto_main_risk": "BTC capped under 108k",
  "stocks_main_risk": "yields rising",
  "today_important_news": [{"title":"CPI","asset_or_sector":"macro","impact":"negative","horizon":"today","confidence":0.7,"why_it_matters":"rate path"}],
  "long_term_important_news": [{"title":"ETF flows","asset_or_sector":"BTC","impact":"positive","horizon":"long","confidence":0.6,"why_it_matters":"structural demand"}],
  "crypto_regime": "chop", "stocks_regime": "risk_off",
  "confidence": 0.65, "source_summary": "opus enriched review"
}}
```
'''


def _tmpdb():
    fd, path = tempfile.mkstemp(suffix=".sqlite"); os.close(fd)
    con = sqlite3.connect(path)
    con.execute("CREATE TABLE IF NOT EXISTS proposed_signals (signal_id TEXT, asset_class TEXT, market_regime TEXT, created_at TEXT)")
    con.commit(); con.close()
    return path


def test_extract_block_from_markdown():
    b = extract_market_block(_SAMPLE)
    assert b is not None
    assert b["crypto_market_mode"] == "chop"
    assert b["crypto_fear_greed"] == 52
    assert len(b["today_important_news"]) == 1


def test_extract_returns_none_on_missing():
    assert extract_market_block("no block here") is None
    assert extract_market_block('{"market_dashboard_update": {invalid') is None


def test_parse_and_store_persists_snapshot():
    db = _tmpdb()
    res = parse_and_store(_SAMPLE, db)
    assert res["stored"] is True
    con = sqlite3.connect(db); con.row_factory = sqlite3.Row
    row = dict(con.execute("SELECT * FROM market_dashboard_snapshots ORDER BY id DESC LIMIT 1").fetchone())
    assert row["crypto_market_mode"] == "chop"
    assert row["generated_by"] == "opus_enriched_review"
    assert "CPI" in (row["today_news"] or "")
    con.close(); os.remove(db)


def test_fetch_market_extras_shape_failopen():
    """fetch_market_extras returns the VIX/SPY/QQQ/ETH-BTC keys and never raises
    (values may be None offline — fail-open)."""
    from src.market.market_dashboard import fetch_market_extras
    ex = fetch_market_extras()
    for k in ("vix", "vix_source", "spy_trend", "qqq_trend", "eth_btc", "btc_dominance"):
        assert k in ex
    assert isinstance(ex["vix_source"], str)


def test_parse_and_store_backfills_vix_when_null(monkeypatch):
    db = _tmpdb()
    import src.market.market_dashboard as md
    monkeypatch.setattr(md, "fetch_market_extras", lambda: {
        "vix": 18.5, "vix_source": "stub", "spy_trend": "down", "qqq_trend": "down",
        "eth_btc": 0.026, "btc_dominance": None})
    res = md.parse_and_store(_SAMPLE, db, fill_extras=True)
    assert res["stored"] is True and res.get("vix") == 18.5
    import sqlite3
    con = sqlite3.connect(db); con.row_factory = sqlite3.Row
    row = dict(con.execute("SELECT * FROM market_dashboard_snapshots ORDER BY id DESC LIMIT 1").fetchone())
    assert row["vix"] == 18.5 and row["spy_trend"] == "down"
    con.close(); os.remove(db)


def test_fallback_when_no_block():
    db = _tmpdb()
    res = parse_and_store("review with no json", db)
    assert res["stored"] is False
    fb = deterministic_fallback(db)
    assert fb["stored"] is True and fb["fallback"] is True
    os.remove(db)
