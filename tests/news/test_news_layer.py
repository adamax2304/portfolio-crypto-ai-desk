"""News-layer hardening tests (2026-07-03) — source health, EDGAR, earnings/advisory, providers,
symbol audit, and the no-score/tier-mutation guardrail. All read-model; no network/live."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.news import source_health, symbol_audit, edgar, advisory, providers


def _news_db(tmp_path, rows):
    db = str(Path(tmp_path) / "news.sqlite")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE news_items (id INTEGER PRIMARY KEY, title TEXT, source TEXT, url TEXT UNIQUE, "
              "published_at TEXT, detected_symbols_json TEXT, detected_narratives_json TEXT, "
              "importance REAL, asset_class TEXT, raw_json TEXT)")
    for i, (title, src, ac, syms, imp, ago_h) in enumerate(rows):
        ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        c.execute("INSERT INTO news_items (title, source, url, published_at, detected_symbols_json, "
                  "importance, asset_class) VALUES (?,?,?,?,?,?,?)",
                  (title, src, f"u{i}", f"datetime('now','-{ago_h} hours')", syms, imp, ac))
        # store an actual recent timestamp so the freshness window matches
        c.execute("UPDATE news_items SET published_at = datetime('now', ?) WHERE url=?",
                  (f"-{ago_h} hours", f"u{i}"))
    c.commit(); c.close()
    return db


# ---- item 1: source health detects an enabled-but-dead configured source ----
def test_source_health_detects_dead_and_disabled(tmp_path):
    # a fresh row for a real config source (CNBC Markets) → OK; every other enabled source has 0 rows
    db = _news_db(tmp_path, [("Fed holds rates", "CNBC Markets", "stocks", '["AAPL"]', 2.0, 1)])
    h = source_health.compute_source_health(db)
    by = {r["source"]: r for r in h["sources"]}
    assert by["CNBC Markets"]["stale_status"] == "OK"
    # Reuters' old endpoint is now disabled explicitly after a confirmed 404;
    # a known-broken feed must not remain an active DEAD alarm.
    assert by["Reuters Business"]["stale_status"] == "DISABLED"
    assert any("404" in w for w in by["Reuters Business"]["warnings"])
    # Coinbase Blog is disabled in config → DISABLED (with its reason)
    assert by["Coinbase Blog"]["stale_status"] == "DISABLED"
    assert h["summary"]["dead"] >= 1 and h["summary"]["disabled"] >= 1


# ---- item 2: SEC EDGAR normalized filing event (pure) ----
def test_edgar_normalize_filing():
    rec = edgar.normalize_filing(ticker="aapl", cik="0000320193", form="8-K",
                                 filed_at="2026-07-01", accession="0000320193-26-000012",
                                 primary_doc="a8k.htm")
    import json
    assert rec["source"] == "SEC EDGAR" and rec["asset_class"] == "stocks"
    assert rec["importance"] == 2.6                                   # 8-K = material
    assert json.loads(rec["detected_symbols_json"]) == ["AAPL"]
    raw = json.loads(rec["raw_json"])
    assert raw["event_type"] == "filing" and raw["form_type"] == "8-K" and raw["cik"] == "0000320193"
    assert "sec.gov/Archives/edgar/data/320193/" in rec["url"]


def test_edgar_diagnostics_flags_unknown_cik(tmp_path):
    # with an empty CIK map, all tickers are unknown → a warning is produced (never a crash)
    import src.news.edgar as e
    orig = e.load_cik_map
    e.load_cik_map = lambda: {}                                       # force empty map
    try:
        d = e.diagnostics(["AAPL", "ZZZZ"])
        assert d["known_cik"] == 0 and "AAPL" in d["unknown_cik"] and d["warning"]
    finally:
        e.load_cik_map = orig


# ---- item 3: earnings advisory near an earnings date ----
def test_earnings_advisory_flags_symbol_under_risk(tmp_path):
    db = str(Path(tmp_path) / "ev.sqlite")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, event_date TEXT, ticker TEXT, event TEXT, "
              "event_type TEXT, source TEXT, importance REAL, asset_class TEXT, raw_json TEXT)")
    today = datetime.now(timezone.utc).date().isoformat()
    c.execute("INSERT INTO events (event_date, ticker, event_type) VALUES (?, 'NVDA', 'earnings')", (today,))
    c.commit(); c.close()
    adv = advisory.earnings_advisory(db)
    assert "NVDA" in adv["earnings_today"]
    assert "NVDA" in adv["symbols_under_earnings_risk"]
    assert "AVOID" in adv["advisory"]
    assert adv["changes_score"] is False and adv["changes_actionability"] is False


# ---- item 5: providers disabled cleanly when no API key ----
def test_providers_disabled_without_key(monkeypatch):
    for p in providers.PROVIDERS:
        monkeypatch.delenv(p.env_var, raising=False)
    st = providers.provider_statuses()
    assert st and all(not s["enabled"] for s in st)
    assert all("disabled" in s["reason"].lower() for s in st)
    # a disabled provider fetch is a clean no-op, never a hard failure
    assert providers.PROVIDERS[0].fetch() == []


def test_provider_enabled_with_key(monkeypatch):
    monkeypatch.setenv("BENZINGA_API_KEY", "x")
    st = {s["source"]: s for s in providers.provider_statuses()}
    assert st["Benzinga News API"]["enabled"] is True


# ---- item 7: symbol match-rate + asset_class mismatch ----
def test_symbol_audit_match_rate_and_mismatch(tmp_path):
    db = _news_db(tmp_path, [
        ("AAPL beats earnings", "CNBC Markets", "stocks", '["AAPL"]', 2.0, 1),
        ("Random macro headline", "CNBC Markets", "stocks", "[]", 1.0, 1),
        ("BTC pumps on stocks feed", "CNBC Markets", "stocks", '["BTC/USDT"]', 1.5, 1)])
    a = symbol_audit.audit(db, hours=24)
    assert a["rows_window"] == 3 and a["rows_with_symbols"] == 2
    assert abs(a["overall_match_rate"] - round(2 / 3, 3)) < 1e-6
    # crypto-style symbol on a stocks row → cross-tag candidate flagged (never auto-fixed)
    kinds = {m["kind"] for m in a["asset_class_mismatch_candidates"]}
    assert "crypto_symbol_in_stocks_row" in kinds


# ---- item 8/9: advisory + shadow eval never mutate score/tier/actionability ----
def test_news_advisory_is_display_only(tmp_path):
    db = _news_db(tmp_path, [("x", "CNBC Markets", "stocks", "[]", 1.0, 1)])
    adv = advisory.news_advisory(db)
    assert adv["advisory_only"] is True
    assert adv["changes_score"] is False and adv["changes_tier"] is False
    assert adv["changes_actionability"] is False
    md = advisory.render_advisory_block(adv)
    assert "does NOT change score" in md


# ---- item 3: SEC EDGAR structured metadata persists in news_items.raw_json ----
def test_edgar_raw_json_persists_structured_metadata(tmp_path):
    import json
    from src.storage.sqlite import SQLiteStore
    store = SQLiteStore(Path(tmp_path) / "n.sqlite")
    store.init_db()
    rec = edgar.normalize_filing(ticker="AAPL", cik="0000320193", form="8-K", filed_at="2026-07-01",
                                 accession="0000320193-26-000012", primary_doc="a8k.htm")
    store.save_news_rows([rec], asset_class="stocks")
    c = sqlite3.connect(str(Path(tmp_path) / "n.sqlite"))
    row = c.execute("SELECT asset_class, raw_json FROM news_items WHERE source='SEC EDGAR'").fetchone()
    c.close()
    assert row is not None and row[0] == "stocks"
    raw = json.loads(row[1])
    assert raw["form_type"] == "8-K" and raw["cik"] == "0000320193"
    assert raw["event_type"] == "filing" and raw["filing_url"] and raw["source_quality"]


# ---- item 5: source-health parses mixed published_at formats correctly ----
def test_source_health_parses_mixed_timestamps(tmp_path):
    from datetime import datetime, timezone
    now = datetime(2026, 7, 4, 12, 0, tzinfo=timezone.utc)
    db = str(Path(tmp_path) / "ts.sqlite")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE news_items (id INTEGER PRIMARY KEY, title TEXT, source TEXT, url TEXT UNIQUE, "
              "published_at TEXT, detected_symbols_json TEXT, detected_narratives_json TEXT, "
              "importance REAL, asset_class TEXT, raw_json TEXT)")
    tss = [
        "2026-07-04T10:29:00+00:00",   # offset, ~1.5h ago → 24h
        "2026-07-04T09:00:00Z",        # Z suffix → 24h
        "2026-07-04 08:00:00",         # SQLite space format → 24h
        "2026-07-02",                  # date-only, 60h ago → 72h not 24h
        "date_unavailable",            # invalid → unknown bucket, excluded
    ]
    for i, ts in enumerate(tss):
        c.execute("INSERT INTO news_items (title, source, url, published_at, detected_symbols_json, "
                  "asset_class) VALUES ('t','CNBC Markets',?,?,'[\"AAPL\"]','stocks')", (f"u{i}", ts))
    c.commit(); c.close()
    h = source_health.compute_source_health(db, now=now)
    cnbc = next(r for r in h["sources"] if r["source"] == "CNBC Markets")
    assert cnbc["rows_24h"] == 3        # offset + Z + space, all within 24h
    assert cnbc["rows_72h"] == 4        # + the date-only (60h)
    assert cnbc["rows_total"] == 5      # invalid still counted in total, not in windows
    # a purely invalid timestamp must not crash and must parse to None
    assert source_health._parse_ts("date_unavailable") is None
    assert source_health._parse_ts("2026-07-04T09:00:00Z") is not None


# ---- item 2: Windows-safe CLI print helper never raises on unicode ----
def test_safe_print_survives_unicode(capsys):
    from src.cli import _safe_print
    _safe_print("net −0.25R · WR ≥50% → verdict [SOURCE] filings…")   # must NOT raise
    out = capsys.readouterr().out
    assert out  # something was written


# ============================================================================
# Production data-layer expansion (2026-07-04)
# ============================================================================
def _events_db(tmp_path, rows):
    """rows: (title, source, asset_class, symbols_json, importance, published_at)"""
    db = str(Path(tmp_path) / "ev.sqlite")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE news_items (id INTEGER PRIMARY KEY, title TEXT, source TEXT, url TEXT UNIQUE, "
              "published_at TEXT, detected_symbols_json TEXT, detected_narratives_json TEXT, "
              "importance REAL, asset_class TEXT, raw_json TEXT)")
    for i, (title, src, ac, syms, imp, pub) in enumerate(rows):
        c.execute("INSERT INTO news_items (title, source, url, published_at, detected_symbols_json, "
                  "importance, asset_class) VALUES (?,?,?,?,?,?,?)",
                  (title, src, f"u{i}", pub, syms, imp, ac))
    c.commit(); c.close()
    return db


def test_risk_advisory_effects_are_risk_only(tmp_path):
    from src.news import risk_advisory as ra
    from datetime import datetime, timezone
    now = datetime(2026, 7, 4, 12, 0, tzinfo=timezone.utc)
    today = now.date().isoformat()
    db = str(Path(tmp_path) / "r.sqlite")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, event_date TEXT, ticker TEXT, event_type TEXT)")
    c.execute("INSERT INTO events (event_date, ticker, event_type) VALUES (?, 'NVDA', 'earnings')", (today,))
    c.execute("CREATE TABLE news_items (id INTEGER PRIMARY KEY, title TEXT, source TEXT, url TEXT UNIQUE, "
              "published_at TEXT, detected_symbols_json TEXT, importance REAL, asset_class TEXT)")
    c.execute("INSERT INTO news_items (title, source, url, published_at, detected_symbols_json, asset_class) "
              "VALUES ('UnitedHealth faces DOJ investigation into fraud', 'CBS', 'x', ?, '[\"UNH\"]', 'stocks')",
              (now.isoformat(),))
    c.commit(); c.close()
    rw = ra.compute_risk_warnings(db, now=now)
    # every emitted effect is in the allowed risk-only set — never a buy/sell/score/tier
    assert all(w["effect"] in ra.ALLOWED_EFFECTS for w in rw["warnings"])
    assert rw["changes_score"] is False and rw["changes_tier"] is False
    assert rw["generates_trade"] is False
    # earnings → do_not_chase + operator-review; legal → operator-review block
    assert "NVDA" in rw["symbols_requiring_operator_review"]
    assert "UNH" in rw["symbols_requiring_operator_review"]
    effs = {w["effect"] for w in rw["warnings"] if w["symbol"] == "NVDA"}
    assert "do_not_chase_warning" in effs


def test_normalized_events_taxonomy_dedupe_conflict(tmp_path):
    from src.news.events import normalized_events
    # relative to now so the 48h window never drops the fixtures on a later real date (determinism).
    pub = (datetime.now(timezone.utc).replace(microsecond=0) - timedelta(hours=2)).isoformat()
    db = _events_db(tmp_path, [
        ("Nvidia beats earnings, revenue surges", "CNBC Markets", "stocks", '["NVDA"]', 2.0, pub),
        ("Nvidia beats earnings, revenue surges", "CNBC Markets", "stocks", '["NVDA"]', 2.0, pub),  # dup
        ("SEC charges firm in fraud lawsuit", "SEC EDGAR", "stocks", '["UNH"]', 2.5, pub),
        ("BTC plunges as ETF outflows spike", "CoinDesk", "crypto", '["BTC/USDT"]', 1.5, pub),
        ("BTC surges to record high on inflows", "CoinDesk", "crypto", '["BTC/USDT"]', 1.5, pub),
    ])
    e = normalized_events(db, hours=48)
    assert e["available"] and e["count"] == 4          # one exact-dup removed
    by_sym = {tuple(x["symbols"]): x for x in e["events"]}
    assert by_sym[("NVDA",)]["event_type"] == "earnings"
    assert by_sym[("NVDA",)]["direction_hint"] == "bullish"
    assert next(x for x in e["events"] if x["source"] == "SEC EDGAR")["source_quality"] == "regulator"
    assert "BTC" in e["conflicting_symbols"]            # bullish + bearish in window


def test_defillama_normalizer_pure():
    from src.news.defillama import normalize_protocol_event
    import json
    rec = normalize_protocol_event(name="Aave", symbol="AAVE", tvl=1.2e10, change_1d_pct=-11.0,
                                   category="Lending", chain="Ethereum", day="2026-07-04",
                                   tradable={"AAVE"})
    assert rec["source"] == "DefiLlama" and rec["asset_class"] == "crypto"
    assert json.loads(rec["detected_symbols_json"]) == ["AAVE/USDT"]
    raw = json.loads(rec["raw_json"])
    assert raw["event_type"] == "tvl_change" and raw["direction_hint"] == "bearish"
    assert raw["source_quality"] == "primary"


def test_retag_is_union_only(tmp_path):
    from src.news.retag import retag
    recent = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    db = _events_db(tmp_path, [
        ("Nvidia unveils new AI chip", "CNBC Markets", "stocks", "[]", 1.0, recent),
        ("Random macro headline no ticker", "CNBC Markets", "stocks", '["AAPL"]', 1.0, recent),
    ])
    d = retag(db, hours=999, dry_run=False)
    assert d["newly_tagged"] >= 1                       # Nvidia headline now tagged NVDA
    c = sqlite3.connect(db)
    aapl = c.execute("SELECT detected_symbols_json FROM news_items WHERE title LIKE 'Random%'").fetchone()[0]
    c.close()
    assert "AAPL" in aapl                               # existing symbol never removed


def test_providers_keyless_and_key_gated(monkeypatch):
    from src.news import providers
    for p in providers.PROVIDERS:
        monkeypatch.delenv(p.env_var, raising=False)
    allst = {s["source"]: s for s in providers.all_provider_statuses()}
    assert allst["FRED (macro rates/yields/DXY)"]["enabled"] is False   # key-gated, no key
    assert allst["DefiLlama"]["enabled"] is True                        # keyless free provider


def test_news_modules_have_no_write_or_live_sql():
    import src.news.source_health as sh
    import src.news.symbol_audit as sa
    import src.news.shadow_eval as se
    import src.news.events as ev
    import src.news.risk_advisory as ra
    import src.news.defillama as dl
    # retag DOES write news_items.detected_symbols_json (union-only enrichment) — excluded from the
    # "no UPDATE" scan but still must never touch score/tier/proposed_signals/live (checked below).
    for mod in (sh, sa, se, advisory, ev, ra, dl):
        src = Path(mod.__file__).read_text(encoding="utf-8").lower()
        for bad in ("update proposed_signals", "insert into proposed_signals", "update signal_outcomes",
                    "insert into signal_outcomes", "update signals set", "final_r =", "create_order",
                    "place_order", "actionable = true", "auto_promote"):
            assert bad not in src, f"{mod.__name__} must be read-only: {bad!r}"


# ============================================================================
# Production news read-model fixes (2026-07-05)
# ============================================================================
def _win_db(tmp_path, rows):
    """rows: (title, source, asset_class, symbols_json, importance, published_at_literal)."""
    db = str(Path(tmp_path) / "win.sqlite")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE news_items (id INTEGER PRIMARY KEY, title TEXT, source TEXT, url TEXT UNIQUE, "
              "published_at TEXT, detected_symbols_json TEXT, importance REAL, asset_class TEXT, "
              "raw_json TEXT)")
    for i, (title, src, ac, syms, imp, pub) in enumerate(rows):
        c.execute("INSERT INTO news_items (title, source, url, published_at, detected_symbols_json, "
                  "importance, asset_class) VALUES (?,?,?,?,?,?,?)", (title, src, f"u{i}", pub, syms, imp, ac))
    c.commit(); c.close()
    return db


def test_parse_ts_formats():
    from src.news.source_health import _parse_ts
    for s in ("2026-07-04T12:00:00Z", "2026-07-04T12:00:00+00:00", "2026-07-04 12:00:00", "2026-07-04"):
        dt = _parse_ts(s)
        assert dt is not None and dt.tzinfo is not None, s
    for bad in ("date_unavailable", None, "", "not-a-date", "null"):
        assert _parse_ts(bad) is None, bad


def test_window_news_rows_excludes_invalid_and_limits_after_filter(tmp_path):
    from src.news.source_health import window_news_rows
    now = datetime(2026, 7, 5, 12, 0, tzinfo=timezone.utc)
    rows = [
        ("h1", "S", "crypto", "[]", 1.0, (now - timedelta(hours=1)).isoformat()),
        ("h30", "S", "crypto", "[]", 1.0, (now - timedelta(hours=30)).isoformat()),
        ("h60", "S", "crypto", "[]", 1.0, (now - timedelta(hours=60)).isoformat()),
        ("bad", "S", "crypto", "[]", 1.0, "date_unavailable"),
        ("none", "S", "crypto", "[]", 1.0, None),
        ("junk", "S", "crypto", "[]", 1.0, "not-a-date"),
    ]
    db = _win_db(tmp_path, rows)
    c = sqlite3.connect(db); c.row_factory = sqlite3.Row
    w24 = window_news_rows(c, hours=24, now=now)
    w48 = window_news_rows(c, hours=48, now=now)
    w72 = window_news_rows(c, hours=72, now=now)
    lim = window_news_rows(c, hours=72, now=now, limit=1)
    c.close()
    assert [r["title"] for r in w24] == ["h1"]
    assert {r["title"] for r in w48} == {"h1", "h30"}
    assert {r["title"] for r in w72} == {"h1", "h30", "h60"}
    # invalid / date_unavailable / None excluded from every window
    for w in (w24, w48, w72):
        assert not ({"bad", "none", "junk"} & {r["title"] for r in w})
    # LIMIT applied AFTER filter+sort desc → the single NEWEST parsed row
    assert [r["title"] for r in lim] == ["h1"]


def test_normalized_events_window_differs_and_limit_after_filter(tmp_path):
    from src.news.events import normalized_events
    now = datetime(2026, 7, 5, 12, 0, tzinfo=timezone.utc)
    rows = [(f"Recent {i} launches", "CNBC Markets", "stocks", "[]", 1.0,
             (now - timedelta(hours=1 + i)).isoformat()) for i in range(5)]
    rows += [(f"Older {i} launches", "CNBC Markets", "stocks", "[]", 1.0,
              (now - timedelta(hours=30 + i)).isoformat()) for i in range(5)]
    db = _win_db(tmp_path, rows)
    e24 = normalized_events(db, hours=24, now=now)
    e48 = normalized_events(db, hours=48, now=now)
    # The reported bug: 24h and 48h returned identical LIMITed slices. They must now differ.
    assert e24["count"] == 5 and e48["count"] == 10 and e24["count"] != e48["count"]
    # LIMIT after filter+sort: the 3 newest over a 48h window are all the "Recent" rows.
    e_lim = normalized_events(db, hours=48, limit=3, now=now)
    assert e_lim["count"] == 3
    assert all("Recent" in x["title"] for x in e_lim["events"])


def test_symbol_audit_excludes_invalid_ts(tmp_path):
    from src.news.symbol_audit import audit
    now = datetime(2026, 7, 5, 12, 0, tzinfo=timezone.utc)
    rows = [
        ("AAPL beats earnings", "CNBC", "stocks", '["AAPL"]', 2.0, (now - timedelta(hours=1)).isoformat()),
        ("stale headline", "CNBC", "stocks", '["MSFT"]', 1.0, "date_unavailable"),
        ("old headline", "CNBC", "stocks", "[]", 1.0, (now - timedelta(hours=100)).isoformat()),
    ]
    db = _win_db(tmp_path, rows)
    a = audit(db, hours=24, now=now)
    assert a["rows_window"] == 1          # only the fresh, parseable row
    assert a["rows_72h"] == 1             # 100h-old + date_unavailable both excluded from 72h too


def test_source_health_providers_defillama_and_stooq(tmp_path):
    from src.news.source_health import compute_source_health
    now = datetime(2026, 7, 5, 12, 0, tzinfo=timezone.utc)
    # DefiLlama IS ingesting (a fresh row); Stooq has none.
    rows = [("Aave TVL +12% to $12000M", "DefiLlama", "crypto", '["AAVE/USDT"]', 1.6,
             (now - timedelta(hours=2)).isoformat())]
    db = _win_db(tmp_path, rows)
    h = compute_source_health(db, now=now)
    by = {r["source"]: r for r in h["sources"]}
    dfl = by["DefiLlama"]
    assert dfl["rows_24h"] >= 1 and dfl["stale_status"] == "OK"           # real rows, counted
    stooq = next(r for k, r in by.items() if k.startswith("Stooq"))
    assert stooq["enabled"] is True and stooq["stale_status"] == "CONFIGURED"  # enabled, 0 rows → NOT OK
    assert stooq["rows_24h"] == 0 and stooq["rows_72h"] == 0
    # DefiLlama rows must NOT also show up as an unregistered source (no double-count).
    assert all(u["source"] != "DefiLlama" for u in h.get("unregistered", []))
    assert h["summary"].get("configured", 0) >= 1


def test_defillama_symbol_validation():
    from src.news.defillama import normalize_protocol_event
    uni = {"AAVE", "BTC", "UNI"}

    def sym(rec):
        return json.loads(rec["detected_symbols_json"])

    for bad in ("-", "?", "", None, "BTC-USD"):     # invalid shapes → never written
        rec = normalize_protocol_event(name="X", symbol=bad, tvl=1e9, change_1d_pct=10.0,
                                       category=None, chain=None, day="2026-07-04", tradable=uni)
        assert sym(rec) == [], bad
    for nt in ("SYRUP", "BARD", "TORN"):            # clean shape but NOT tradable → not written
        rec = normalize_protocol_event(name="X", symbol=nt, tvl=1e9, change_1d_pct=10.0,
                                       category=None, chain=None, day="2026-07-04", tradable=uni)
        assert sym(rec) == [], nt
        raw = json.loads(rec["raw_json"])
        assert raw["protocol_symbol"] == nt and raw["symbol_tradable"] is False
    rec = normalize_protocol_event(name="Aave", symbol="aave", tvl=1e9, change_1d_pct=-11.0,
                                   category="Lending", chain="Ethereum", day="2026-07-04", tradable=uni)
    assert sym(rec) == ["AAVE/USDT"] and json.loads(rec["raw_json"])["symbol_tradable"] is True


def test_defillama_cleanup_removes_old_non_tradable_symbols(tmp_path):
    from src.news.defillama import cleanup_symbol_pollution
    db = _win_db(tmp_path, [
        ("Old dirty DefiLlama row", "DefiLlama", "crypto", '["-/USDT", "BARD/USDT", "AAVE/USDT"]',
         1.8, "2026-07-05T00:00:00+00:00"),
    ])
    c = sqlite3.connect(db)
    c.execute("UPDATE news_items SET raw_json=? WHERE source='DefiLlama'",
              (json.dumps({"provider": "DefiLlama", "event_type": "tvl_change"}),))
    c.commit(); c.close()
    d = cleanup_symbol_pollution(db, dry_run=False)
    assert d["updated"] == 1 and d["removed"] == 2
    c = sqlite3.connect(db)
    row = c.execute("SELECT detected_symbols_json, raw_json FROM news_items WHERE source='DefiLlama'").fetchone()
    c.close()
    assert json.loads(row[0]) == ["AAVE/USDT"]
    raw = json.loads(row[1])
    assert sorted(raw["removed_detected_symbols"]) == ["-/USDT", "BARD/USDT"]
    assert raw["symbol_tradable"] is True


def test_risk_advisory_resolves_asset_class_from_symbol_universe(tmp_path):
    from src.news import risk_advisory as ra
    now = datetime(2026, 7, 5, 12, 0, tzinfo=timezone.utc)
    db = _win_db(tmp_path, [
        ("DOJ Probe Extends to Optum Rx Medicare Billing Practices", "FierceHealthcare",
         "crypto", '["UNH"]', 2.0, (now - timedelta(hours=2)).isoformat()),
    ])
    rw = ra.compute_risk_warnings(db, hours=24, now=now)
    unh = next(w for w in rw["warnings"] if w["symbol"] == "UNH")
    assert unh["asset_class"] == "stocks"


def test_symbol_audit_excludes_defillama_context_only_from_kpi(tmp_path):
    from src.news.symbol_audit import audit
    now = datetime(2026, 7, 5, 12, 0, tzinfo=timezone.utc)
    db = _win_db(tmp_path, [
        ("AAPL beats earnings", "CNBC", "stocks", '["AAPL"]', 2.0, (now - timedelta(hours=1)).isoformat()),
        ("Arrakis Modular TVL +120%", "DefiLlama", "crypto", "[]", 1.9,
         (now - timedelta(hours=1)).isoformat()),
    ])
    c = sqlite3.connect(db)
    c.execute("UPDATE news_items SET raw_json=? WHERE source='DefiLlama'",
              (json.dumps({"provider": "DefiLlama", "symbol_tradable": False}),))
    c.commit(); c.close()
    a = audit(db, hours=24, now=now)
    assert a["rows_window"] == 1
    assert a["rows_with_symbols"] == 1
    assert a["context_only_rows_excluded"] == 1
    assert not any(u["source"] == "DefiLlama" for u in a["top_unmatched_high_importance"])


def test_source_health_sec_edgar_weekend_not_dead_primary(tmp_path):
    now = datetime(2026, 7, 5, 12, 0, tzinfo=timezone.utc)  # Sunday
    db = _win_db(tmp_path, [])
    h = source_health.compute_source_health(db, now=now)
    by = {r["source"]: r for r in h["sources"]}
    assert by["SEC EDGAR"]["stale_status"] == "STALE"
    assert "SEC EDGAR" not in h["summary"]["dead_primary"]
