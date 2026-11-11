"""Production news entity/narrative resolver + downstream catalyst fixes. READ-MODEL / enrichment only:
never writes signal_outcomes / final_r / live; only additive union enrichment + news_supported 0→1.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone

from src.news import entity_resolver as er

NOW = datetime(2026, 7, 8, 15, 0, tzinfo=timezone.utc)


# ---- A. entity resolver ------------------------------------------------------------------------
def test_resolver_reads_title_and_body_and_slug():
    row = {"title": "Quiet headline", "asset_class": "crypto",
           "raw_json": json.dumps({"summary": "Ethereum upgrade ships"}),
           "url": "https://x.com/why-solana-soared"}
    tf = er.extract_text_fields(row)
    assert "Ethereum upgrade" in tf["combined"] and "solana soared" in tf["combined"].lower()
    r = er.resolve_row(row)
    assert "ETH/USDT" in r["detected_symbols"] and "SOL/USDT" in r["detected_symbols"]


def test_resolver_crypto_and_stock_alias_and_cross_asset():
    assert "XRP/USDT" in er.resolve_row(
        {"title": "Ripple wins MiCA license", "asset_class": "crypto", "url": ""})["detected_symbols"]
    assert "INTC" in er.resolve_row(
        {"title": "Intel stock soared", "asset_class": "stocks", "url": ""})["detected_symbols"]
    # cross-asset: a stock named in a crypto-classified row still resolves (COIN is a stock ticker).
    r = er.resolve_row({"title": "Coinbase gets UK license", "asset_class": "crypto", "url": ""})
    assert "COIN" in r["detected_symbols"] and r["asset_impact_scope"] in ("sector", "symbol")


def test_resolver_vetted_stock_headline_alias_is_trusted_but_social_is_not():
    vetted = er.resolve_row({
        "title": "Oracle wins $7 billion Pentagon contract", "asset_class": "stocks",
        "source": "The Motley Fool Investing", "url": "",
    })
    assert "ORCL" in vetted["detected_symbols"]
    assert "ORCL" in vetted["trusted_symbols"]
    social = er.resolve_row({
        "title": "oracle rumor spreads", "asset_class": "stocks", "source": "t.me/marketfeed", "url": "",
    })
    assert "ORCL" not in social["trusted_symbols"]


def test_resolver_maps_current_reputable_stock_headline_names():
    cases = {
        "Nike Stock Is Down 76% From Its High": "NKE",
        "Apple Added About $1.5 Trillion in Market Value": "AAPL",
        "AMD's Data Center Business Is Skyrocketing": "AMD",
    }
    for title, ticker in cases.items():
        resolved = er.resolve_row({
            "title": title,
            "asset_class": "stocks",
            "source": "The Motley Fool Investing",
            "url": "",
        })
        assert ticker in resolved["trusted_symbols"]


def test_resolver_listing_parser():
    r = er.resolve_row({"title": "MEXC to Move CZUSDT from Innovation Zone to Main Board",
                        "asset_class": "crypto", "url": ""})
    assert "listing" in r["event_tags"] and r["tradability_status"] == "untracked_entity"
    # a TRACKED listing ticker becomes a tradable symbol
    r2 = er.resolve_row({"title": "Binance will list ARB perpetual", "asset_class": "crypto", "url": ""})
    assert "ARB/USDT" in r2["detected_symbols"]


def test_stock_listing_word_is_not_a_crypto_listing_event():
    r = er.resolve_row({"title": "Acme marks one year after its NASDAQ listing", "asset_class": "stocks", "url": ""})
    assert "listing" not in r["event_tags"]
    assert not any(entity["kind"] == "untracked_entity" for entity in r["detected_entities"])


def test_crypto_classified_stock_headline_is_not_a_crypto_listing_event():
    r = er.resolve_row({"title": "GameSquare faces NASDAQ delisting risk", "asset_class": "crypto", "url": ""})
    assert "listing" not in r["event_tags"]
    assert not any(entity["kind"] == "untracked_entity" for entity in r["detected_entities"])


def test_listing_parser_splits_pair_and_preserves_dynamic_exchange_candidate():
    """A non-curated listing is recognised but cannot bypass the trusted curated universe."""
    hits = er._listing_symbols("MEXC to list VEXAIUSDT perpetual futures", {}, {"VEXAI"})
    assert hits == [{"symbol": None, "ticker": "VEXAI", "tradable": False,
                     "market": "perpetual", "dynamic_universe": True}]
    unknown = er._listing_symbols("MEXC to list VEXAIUSDT perpetual futures", {}, set())
    assert any(item["ticker"] == "VEXAI" and not item["tradable"] and not item["dynamic_universe"]
               for item in unknown)


def test_structured_sec_issuer_ticker_is_trusted_but_article_ticker_is_not():
    """Raw ticker/CIK is powerful official provenance, not a blanket trust bypass for articles."""
    official = er.resolve_row({
        "title": "Form 8-K filing", "source": "SEC EDGAR", "asset_class": "stocks",
        "raw_json": json.dumps({"ticker": "MSTR", "cik": "0001050446", "event_type": "filing",
                                 "source_quality": "primary_or_regulator"}),
    })
    assert "MSTR" in official["trusted_symbols"] and "issuer_cik" in official["entity_match_source"]
    article = er.resolve_row({
        "title": "An article with a structured value", "source": "random blog", "asset_class": "stocks",
        "raw_json": json.dumps({"ticker": "MSTR"}),
    })
    assert "MSTR" in article["detected_symbols"]
    assert "MSTR" not in article["trusted_symbols"]


def test_finnhub_company_query_symbol_is_trusted_but_market_news_tag_is_not():
    company = er.resolve_row({
        "title": "Strategy Inc quarterly update", "source": "Finnhub company-news",
        "asset_class": "stocks", "detected_symbols_json": '["MSTR"]', "raw_json": "{}",
    })
    assert company["trusted_symbols"] == ["MSTR"]
    assert "provider_symbol" in company["entity_match_source"]

    market = er.resolve_row({
        "title": "A broad market article", "source": "Finnhub market-news",
        "asset_class": "stocks", "detected_symbols_json": '["MSTR"]', "raw_json": "{}",
    })
    assert "MSTR" not in market["trusted_symbols"]


def test_multiversx_alias_and_explicit_egld_cashtag_are_trusted():
    by_name = er.resolve_row({"title": "MultiversX network upgrade", "asset_class": "crypto"})
    by_tag = er.resolve_row({"title": "Bithumb suspends $EGLD withdrawals", "asset_class": "crypto"})
    assert "EGLD/USDT" in by_name["trusted_symbols"]
    assert "EGLD/USDT" in by_tag["trusted_symbols"]


def test_vetted_issuer_subsidiary_and_established_crypto_aliases_are_trusted():
    jpm = er.resolve_row({
        "title": "Campbell Global appoints a new head", "asset_class": "stocks",
        "content_text": "Campbell Global is a subsidiary of J.P. Morgan Asset Management (NYSE: JPM).",
    })
    assert "JPM" in jpm["trusted_symbols"]
    hbar = er.resolve_row({"title": "Hedera resumes HBAR withdrawals", "asset_class": "crypto"})
    assert "HBAR/USDT" in hbar["trusted_symbols"]
    generic = er.resolve_row({"title": "A magic trick surprises attendees", "asset_class": "crypto"})
    assert "MAGIC/USDT" not in generic["trusted_symbols"]


def test_resolver_macro_no_forced_symbol():
    r = er.resolve_row({"title": "Fed holds rates steady as inflation cools", "asset_class": "crypto", "url": ""})
    assert r["detected_symbols"] == [] and r["tradability_status"] == "macro_only"
    assert "fed" in r["event_tags"] and "inflation" in r["event_tags"]


def test_stock_crypto_treasury_story_keeps_token_as_context_not_direct_catalyst():
    resolved = er.resolve_row({
        "title": "$MSTR buys more Bitcoin for its corporate treasury",
        "asset_class": "stocks", "source": "Reuters", "url": "",
    })

    assert "MSTR" in resolved["trusted_symbols"]
    assert "BTC/USDT" in resolved["detected_symbols"]
    assert "BTC/USDT" not in resolved["trusted_symbols"]
    assert "corporate_crypto_treasury" in resolved["event_tags"]
    assert "context_not_direct_token_catalyst" in resolved["entity_match_reason"]


def test_resolver_common_word_false_positive_safety():
    for title in ("Stay near the entry zone", "Only one thing matters", "Follow the link below"):
        assert er.resolve_row({"title": title, "asset_class": "crypto", "url": ""})["detected_symbols"] == []


# ---- B. schema migration -----------------------------------------------------------------------
def _news_db(tmp_path, *, with_new_cols=False):
    db = str(tmp_path / "news.sqlite")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE news_items (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, source TEXT, "
              "url TEXT, published_at TEXT, detected_symbols_json TEXT, detected_narratives_json TEXT, "
              "importance REAL, asset_class TEXT, raw_json TEXT)")
    return db, c


def test_schema_migration_additive_idempotent(tmp_path):
    db, c = _news_db(tmp_path)
    ts = NOW.isoformat()
    c.execute("INSERT INTO news_items (title, source, asset_class, published_at, detected_symbols_json) "
              "VALUES ('Intel soared','Fool','stocks',?, '[]')", (ts,))
    c.commit()
    er.ensure_news_entity_columns(c); er.ensure_news_entity_columns(c)   # idempotent
    cols = {r[1] for r in c.execute("PRAGMA table_info(news_items)")}
    for col, _ in er._NEW_COLUMNS:
        assert col in cols
    assert c.execute("SELECT COUNT(*) FROM news_items").fetchone()[0] == 1   # no row loss
    c.close()


def test_refresh_union_only_never_removes(tmp_path):
    db, c = _news_db(tmp_path)
    c.execute("INSERT INTO news_items (title, source, asset_class, published_at, detected_symbols_json) "
              "VALUES ('Intel and Nvidia rally','Fool','stocks',?, '[\"NVDA\"]')", (NOW.isoformat(),))
    c.commit(); c.close()
    er.refresh(db=db, hours=72, now_iso=NOW.isoformat())
    c = sqlite3.connect(db)
    syms = json.loads(c.execute("SELECT detected_symbols_json FROM news_items").fetchone()[0])
    ctx = c.execute("SELECT resolver_version, asset_impact_scope FROM news_items").fetchone()
    c.close()
    assert "NVDA" in syms and "INTC" in syms          # union: kept existing + added new
    assert ctx[0] == er.RESOLVER_VERSION


# ---- C. catalyst_label_refresh (stocks) --------------------------------------------------------
def test_stock_signal_flips_news_supported(tmp_path):
    from src.signals.catalyst_label_refresh import direct_news_for_signal
    db = str(tmp_path / "cl.sqlite")
    c = sqlite3.connect(db); c.row_factory = sqlite3.Row
    c.execute("CREATE TABLE news_items (title TEXT, source TEXT, published_at TEXT, "
              "detected_symbols_json TEXT, importance REAL, asset_class TEXT)")
    pub = (NOW - timedelta(hours=1)).isoformat()
    c.execute("INSERT INTO news_items VALUES ('Apple unveils new chip','Reuters',?, '[\"AAPL\"]',2.0,'stocks')", (pub,))
    c.commit()
    # stocks asset_class → finds the stock news (crypto-only would return None)
    hit = direct_news_for_signal(c, "AAPL", NOW.isoformat(), asset_class="stocks")
    assert hit is not None and "Apple" in hit["headline"]
    # crypto signal for the same ticker (no crypto news) → None (crypto behavior unchanged)
    assert direct_news_for_signal(c, "AAPL", NOW.isoformat(), asset_class="crypto") is None
    c.close()


def test_no_substring_fabrication(tmp_path):
    from src.signals.catalyst_label_refresh import direct_news_for_signal
    db = str(tmp_path / "cl2.sqlite")
    c = sqlite3.connect(db); c.row_factory = sqlite3.Row
    c.execute("CREATE TABLE news_items (title TEXT, source TEXT, published_at TEXT, "
              "detected_symbols_json TEXT, importance REAL, asset_class TEXT)")
    # title contains 'AAPL' substring but detected_symbols does NOT list it → must not match.
    c.execute("INSERT INTO news_items VALUES ('AAPLE juice recall','X',?, '[\"KO\"]',2.0,'stocks')",
              ((NOW - timedelta(hours=1)).isoformat(),))
    c.commit()
    assert direct_news_for_signal(c, "AAPL", NOW.isoformat(), asset_class="stocks") is None
    c.close()


# ---- D. catalyst collector (asset-aware fallback) ----------------------------------------------
def test_collector_fallback_asset_aware():
    from src.catalysts.collector import _row_to_event
    from src.catalysts.entity_aliases import get_matcher, get_stocks_matcher
    cm, sm = get_matcher("."), get_stocks_matcher(".")
    ev = _row_to_event({"title": "Nvidia unveils new AI chip", "source": "Reuters",
                        "url": "http://x/n", "asset_class": "stocks", "detected_symbols_json": "[]"},
                       rejected_test=[], rejected_missing=[], crypto_matcher=cm, stocks_matcher=sm)
    assert ev and "NVDA" in (ev[0].symbol or "") + ",".join(ev[0].related_symbols or [])
    ev2 = _row_to_event({"title": "Ripple wins MiCA license", "source": "CoinDesk",
                         "url": "http://x/r", "asset_class": "crypto", "detected_symbols_json": "[]"},
                        rejected_test=[], rejected_missing=[], crypto_matcher=cm, stocks_matcher=sm)
    assert ev2 and "XRP/USDT" in (ev2[0].symbol or "") + ",".join(ev2[0].related_symbols or [])


# ---- E. store load_news_window -----------------------------------------------------------------
def test_load_news_window_is_time_window(tmp_path):
    from src.storage.sqlite import SQLiteStore
    store = SQLiteStore(tmp_path / "s.sqlite")
    store.init_db()
    with store.connect() as c:
        # 1 recent + 1 old (mixed formats: Z vs +00:00)
        c.execute("INSERT INTO news_items (title, source, url, published_at, asset_class) "
                  "VALUES ('recent','R','u1',?, 'crypto')", ((datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ"),))
        c.execute("INSERT INTO news_items (title, source, url, published_at, asset_class) "
                  "VALUES ('old','R','u2',?, 'crypto')", ((datetime.now(timezone.utc) - timedelta(days=10)).isoformat(),))
        c.commit()
    rows = store.load_news_window(hours=48, asset_class="crypto")
    titles = {r["title"] for r in rows}
    assert "recent" in titles and "old" not in titles     # time window, not latest-N


# ---- F. trust layer — untrusted preexisting tags must not drive catalyst linkage --------------
def test_dia_approval_false_positive_not_trusted():
    """Regression: 'King Copper Discovery Receives DIA Approval' = a regulatory/agency approval, NOT the
    Dow-Jones ETF DIA. A bare acronym must never become a *trusted* catalyst symbol, and the resolver
    must not report it as a clean stocks resolution."""
    r = er.resolve_row({"title": "King Copper Discovery Receives DIA Approval for Its Copper Mine",
                        "asset_class": "stocks", "url": ""})
    assert "DIA" not in r["trusted_symbols"]
    assert r["entity_match_source"] in ("no_match", "macro_tagger")   # never a fake 'alias_stocks'/'none'


def test_real_dia_cashtag_and_alias_are_trusted():
    """A REAL Dow-ETF reference — cashtag $DIA or an explicit ETF/company alias — IS a trusted symbol."""
    assert "DIA" in er.resolve_row(
        {"title": "$DIA breaks out as the Dow rallies", "asset_class": "stocks", "url": ""})["trusted_symbols"]
    assert "DIA" in er.resolve_row(
        {"title": "SPDR Dow Jones ETF sees record inflows", "asset_class": "stocks", "url": ""})["trusted_symbols"]


def test_refresh_marks_untrusted_preexisting(tmp_path):
    """A row arriving with a preexisting bare 'DIA' ingest tag but no trusted match is written as
    resolution_status='preexisting_unverified' with trusted_symbols_json='[]'. The union keeps DIA
    (never destructive) but it is NOT trusted."""
    db, c = _news_db(tmp_path)
    c.execute("INSERT INTO news_items (title, source, asset_class, published_at, detected_symbols_json) "
              "VALUES ('King Copper Discovery Receives DIA Approval','GlobeNewswire','stocks',?, '[\"DIA\"]')",
              ((NOW - timedelta(hours=1)).isoformat(),))
    c.commit(); c.close()
    er.refresh(db=db, hours=72, now_iso=NOW.isoformat())
    c = sqlite3.connect(db)
    row = c.execute("SELECT detected_symbols_json, trusted_symbols_json, resolution_status "
                    "FROM news_items").fetchone()
    c.close()
    assert "DIA" in json.loads(row[0])       # union-only, never dropped
    assert json.loads(row[1]) == []          # but NOT trusted
    assert row[2] == "preexisting_unverified"


def test_untrusted_preexisting_stock_tag_does_not_flip(tmp_path):
    """A stock signal must NOT flip news_supported off an untrusted preexisting 'DIA' tag; a trusted row
    for the same ticker DOES match."""
    from src.signals.catalyst_label_refresh import direct_news_for_signal
    db = str(tmp_path / "trust_stock.sqlite")
    c = sqlite3.connect(db); c.row_factory = sqlite3.Row
    c.execute("CREATE TABLE news_items (title TEXT, source TEXT, published_at TEXT, "
              "detected_symbols_json TEXT, importance REAL, asset_class TEXT, trusted_symbols_json TEXT)")
    pub = (NOW - timedelta(hours=1)).isoformat()
    c.execute("INSERT INTO news_items VALUES ('King Copper Receives DIA Approval','GlobeNewswire',?, "
              "'[\"DIA\"]',2.0,'stocks','[]')", (pub,))
    c.commit()
    assert direct_news_for_signal(c, "DIA", NOW.isoformat(), asset_class="stocks") is None
    # a trusted row (resolver put DIA in trusted_symbols_json) for the same ticker DOES match.
    c.execute("INSERT INTO news_items VALUES ('SPDR Dow Jones ETF hits record','Reuters',?, "
              "'[\"DIA\"]',2.0,'stocks','[\"DIA\"]')", (pub,))
    c.commit()
    assert direct_news_for_signal(c, "DIA", NOW.isoformat(), asset_class="stocks") is not None
    c.close()


def test_untrusted_preexisting_crypto_tag_does_not_flip(tmp_path):
    """Crypto side of the same gate: an old/source-none crypto row with a bare 'ARB' tag but no trusted
    provenance does not flip news_supported; an explicit cashtag in the title rescues it."""
    from src.signals.catalyst_label_refresh import direct_news_for_signal
    db = str(tmp_path / "trust_crypto.sqlite")
    c = sqlite3.connect(db); c.row_factory = sqlite3.Row
    c.execute("CREATE TABLE news_items (title TEXT, source TEXT, published_at TEXT, "
              "detected_symbols_json TEXT, importance REAL, asset_class TEXT, trusted_symbols_json TEXT)")
    pub = (NOW - timedelta(hours=1)).isoformat()
    c.execute("INSERT INTO news_items VALUES ('one arb opportunity in defi lending','blog',?, "
              "'[\"ARB\"]',2.0,'crypto','[]')", (pub,))
    c.commit()
    assert direct_news_for_signal(c, "ARB", NOW.isoformat(), asset_class="crypto") is None
    # explicit cashtag in the title is trusted even on an otherwise-unresolved row.
    c.execute("INSERT INTO news_items VALUES ('$ARB surges on Arbitrum upgrade','CoinDesk',?, "
              "'[\"ARB\"]',2.0,'crypto','[]')", (pub,))
    c.commit()
    assert direct_news_for_signal(c, "ARB", NOW.isoformat(), asset_class="crypto") is not None
    c.close()


def _trust_db(tmp_path, name):
    """A news_items table WITH the trust-layer column present (post-migration schema)."""
    db = str(tmp_path / name)
    c = sqlite3.connect(db); c.row_factory = sqlite3.Row
    c.execute("CREATE TABLE news_items (title TEXT, source TEXT, published_at TEXT, "
              "detected_symbols_json TEXT, importance REAL, asset_class TEXT, trusted_symbols_json TEXT)")
    return c


def test_null_trusted_symbols_json_not_trusted(tmp_path):
    """Trust-layer column present but the row is NOT yet resolved (trusted_symbols_json IS NULL,
    resolution_status IS NULL) → must NOT flip news_supported when there is no cashtag."""
    from src.signals.catalyst_label_refresh import direct_news_for_signal
    c = _trust_db(tmp_path, "null_trust.sqlite")
    pub = (NOW - timedelta(hours=1)).isoformat()
    c.execute("INSERT INTO news_items VALUES ('Apple ships a new chip','Reuters',?, "
              "'[\"AAPL\"]',2.0,'stocks',NULL)", (pub,))
    c.commit()
    assert direct_news_for_signal(c, "AAPL", NOW.isoformat(), asset_class="stocks") is None
    c.close()


def test_stock_hashtag_does_not_flip_but_cashtag_does(tmp_path):
    """Stocks policy: on an untrusted row only '$TICKER' is a trusted fallback; '#TICKER' is social noise."""
    from src.signals.catalyst_label_refresh import direct_news_for_signal
    c = _trust_db(tmp_path, "stock_tag.sqlite")
    pub = (NOW - timedelta(hours=1)).isoformat()
    c.execute("INSERT INTO news_items VALUES ('Traders watch #DIA into the close','X',?, "
              "'[\"DIA\"]',2.0,'stocks','[]')", (pub,))
    c.commit()
    assert direct_news_for_signal(c, "DIA", NOW.isoformat(), asset_class="stocks") is None   # #DIA → no flip
    c.execute("INSERT INTO news_items VALUES ('$DIA breaks out as the Dow rallies','Reuters',?, "
              "'[\"DIA\"]',2.0,'stocks','[]')", (pub,))
    c.commit()
    assert direct_news_for_signal(c, "DIA", NOW.isoformat(), asset_class="stocks") is not None  # $DIA → flips
    c.close()


def test_crypto_hashtag_and_cashtag_both_flip(tmp_path):
    """Crypto policy: on an untrusted row BOTH '$TICKER' and '#TICKER' are trusted fallbacks."""
    from src.signals.catalyst_label_refresh import direct_news_for_signal
    c = _trust_db(tmp_path, "crypto_tag.sqlite")
    pub = (NOW - timedelta(hours=1)).isoformat()
    c.execute("INSERT INTO news_items VALUES ('#ARB rallies on the Arbitrum upgrade','CoinDesk',?, "
              "'[\"ARB\"]',2.0,'crypto','[]')", (pub,))
    c.commit()
    assert direct_news_for_signal(c, "ARB", NOW.isoformat(), asset_class="crypto") is not None  # #ARB → flips
    c.close()


# ---- G. guardrails -----------------------------------------------------------------------------
def test_resolver_is_enrichment_only():
    import pathlib
    src = pathlib.Path(er.__file__).read_text(encoding="utf-8").lower()
    for bad in ("create_order(", "final_r =", "update signal_outcomes", "update proposed_signals",
                "insert into signal_outcomes", "update paper_execution"):
        assert bad not in src, bad


# ---- H. entity resolver health (freshness / coverage read-model) -------------------------------
def test_entity_health_flags_unresolved_backlog(tmp_path):
    """The health read-model counts resolved / unresolved-symbol-tagged / trusted / preexisting_unverified
    per window and raises severity when a symbol-tagged row sits unresolved beyond one scheduler cycle."""
    from src.news import entity_health as eh
    db, c = _news_db(tmp_path)
    er.ensure_news_entity_columns(c)                      # post-migration schema (trust layer present)
    fresh = (NOW - timedelta(minutes=30)).isoformat()
    old = (NOW - timedelta(hours=5)).isoformat()
    c.execute("INSERT INTO news_items (title, source, asset_class, published_at, detected_symbols_json, "
              "trusted_symbols_json, resolution_status, resolved_at) VALUES "
              "('Apple ships chip','R','stocks',?, '[\"AAPL\"]','[\"AAPL\"]','resolver_confirmed',?)", (fresh, fresh))
    c.execute("INSERT INTO news_items (title, source, asset_class, published_at, detected_symbols_json, "
              "trusted_symbols_json, resolution_status, resolved_at) VALUES "
              "('King Copper DIA Approval','G','stocks',?, '[\"DIA\"]','[]','preexisting_unverified',?)", (fresh, fresh))
    # an OLD symbol-tagged row the resolver has NOT processed (resolution_status NULL) → the backlog.
    c.execute("INSERT INTO news_items (title, source, asset_class, published_at, detected_symbols_json) VALUES "
              "('Old headline mentioning NVDA','R','stocks',?, '[\"NVDA\"]')", (old,))
    c.commit(); c.close()
    h = eh.compute_entity_health(db, now=NOW)
    assert h["trust_layer_present"] is True
    assert h["windows"]["72h"]["unresolved_symbol_tagged"] == 1     # the old NVDA row
    assert h["windows"]["72h"]["trusted_symbol_tagged"] == 1        # AAPL
    assert h["windows"]["72h"]["preexisting_unverified"] == 1       # DIA
    assert h["max_unresolved_age_minutes"] > eh.SCHEDULER_CYCLE_MINUTES
    assert h["severity"] in ("WARN", "CRITICAL")


def test_entity_health_ok_when_all_resolved(tmp_path):
    """No unresolved symbol-tagged rows → severity OK."""
    from src.news import entity_health as eh
    db, c = _news_db(tmp_path)
    er.ensure_news_entity_columns(c)
    fresh = (NOW - timedelta(minutes=20)).isoformat()
    c.execute("INSERT INTO news_items (title, source, asset_class, published_at, detected_symbols_json, "
              "trusted_symbols_json, resolution_status, resolved_at) VALUES "
              "('Microsoft news','R','stocks',?, '[\"MSFT\"]','[\"MSFT\"]','resolver_confirmed',?)", (fresh, fresh))
    c.commit(); c.close()
    h = eh.compute_entity_health(db, now=NOW)
    assert h["windows"]["24h"]["unresolved_symbol_tagged"] == 0
    assert h["severity"] == "OK"


# ---- I. entity health alerting (2026-07-13 audit: this diagnostic could never notify anyone) ----
def test_entity_health_alert_transitions_and_dedupes(monkeypatch, tmp_path):
    """CRITICAL transition sends once; a repeat CRITICAL within the cooldown is suppressed;
    recovery sends its own message. Fail-open: never raises even without Telegram configured."""
    from src.news import entity_health as eh

    calls: list[str] = []

    class FakeNotifier:
        enabled = True
        chat_id = "123"

        def send(self, message, parse_mode="Markdown"):
            calls.append(message)
            return {"ok": True}

    monkeypatch.setattr(eh, "_notifier_for", lambda _root: FakeNotifier())
    first = eh._maybe_alert({"severity": "CRITICAL", "severity_reason": "resolver stalled"}, tmp_path)
    second = eh._maybe_alert({"severity": "CRITICAL", "severity_reason": "resolver stalled"}, tmp_path)
    recovered = eh._maybe_alert({"severity": "OK", "severity_reason": "caught up"}, tmp_path)
    assert len(first) == 1 and "CRITICAL" in first[0]
    assert second == []                              # deduped within cooldown
    assert len(recovered) == 1 and "RECOVERED" in recovered[0]
    assert len(calls) == 2                            # CRITICAL once + RECOVERED once, no repeat


def test_entity_health_alert_fails_open_without_telegram_configured(tmp_path):
    from src.news import entity_health as eh
    # No config/notifications.yaml under tmp_path -> _notifier_for's real TelegramNotifier construction
    # should fail closed (or construct a disabled notifier); either way this must never raise.
    sent = eh._maybe_alert({"severity": "CRITICAL", "severity_reason": "x"}, tmp_path)
    assert sent == []
