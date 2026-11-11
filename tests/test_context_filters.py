from __future__ import annotations

import io
import json
import sqlite3
import zipfile
from datetime import date, datetime, timedelta, timezone

from src.execution import crypto_quality_overlay as cqo
from src.execution import stocks_catalyst_rs_shadow as catalyst_rs
from src.execution import stocks_market_context_overlay as stocks_overlay
from src.intelligence import market_risk_context, options_context, token_unlock_context
from src.intelligence.context_store import connect, insert_named, insert_unlock
from src.risk.risk_guards import paper_risk_floor
from src.stocks import insider_context


UTC = timezone.utc


def _insert_quotes(db, table, columns, rows):
    with connect(db) as conn:
        for row in rows:
            insert_named(conn, table, row, columns)
        conn.commit()


def test_context_schema_is_idempotent_and_isolated(tmp_path):
    db = tmp_path / "intelligence.sqlite"
    with connect(db) as conn:
        conn.execute("INSERT INTO context_filter_decisions "
                     "(signal_id,filter_name,filter_version,decision_at,action,shadow_only) "
                     "VALUES ('x','f','v1','2026-07-16T00:00:00+00:00','FULL_SIZE',1)")
        conn.commit()
    with connect(db) as conn:
        assert conn.execute("SELECT COUNT(*) FROM context_filter_decisions").fetchone()[0] == 1
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"token_unlock_events", "stablecoin_peg_snapshots", "cross_exchange_quote_snapshots",
            "options_context_snapshots", "insider_transactions", "context_filter_decisions"} <= tables
    assert "proposed_signals" not in tables
    assert "signal_outcomes" not in tables


def test_token_unlock_is_point_in_time_and_shadow_by_default(tmp_path):
    db = tmp_path / "unlock.sqlite"
    now = datetime(2026, 7, 16, 12, tzinfo=UTC)
    with connect(db) as conn:
        insert_unlock(conn, {
            "source": "fixture", "source_event_id": "u1", "observed_at": (now - timedelta(hours=1)).isoformat(),
            "asset_symbol": "ABC", "unlock_at": (now + timedelta(days=2)).isoformat(),
            "unlock_tokens": 10, "unlock_usd": 1_000_000, "pct_circulating": 8.0,
            "avg_daily_volume_usd": 200_000, "unlock_adv_days": 5.0,
            "recipient_type": "vc", "unlock_type": "cliff", "quality_status": "ok", "raw_json": {},
        })
        conn.commit()
    cfg = {"paper_routing_enabled": False, "max_source_age_hours": 36,
           "min_pct_circulating": 5, "min_unlock_adv_days": 3,
           "warning_days": 30, "half_size_days": 14, "shadow_only_days": 3}
    unseen = token_unlock_context.context("ABC/USDT", as_of=now - timedelta(hours=2), db_path=db, cfg=cfg)
    seen = token_unlock_context.context("ABC/USDT", as_of=now, db_path=db, cfg=cfg)
    assert unseen["status"] == "unknown"
    assert seen["would_action"] == "SHADOW_ONLY"
    assert seen["action"] == "FULL_SIZE"


def test_defillama_public_calendar_normalizes_future_cliffs_only():
    now = datetime(2026, 7, 16, 12, tzinfo=UTC)
    payload = {"props": {"pageProps": {"emissions": [{
        "protocolSlug": "ton", "name": "TON", "circSupply": 1_000,
        "tSymbol": "GRAM", "events": [
            {"timestamp": (now + timedelta(days=2)).timestamp(), "noOfTokens": [40],
             "category": "insiders", "unlockType": "cliff"},
            {"timestamp": (now + timedelta(days=2)).timestamp(), "noOfTokens": [20],
             "category": "privateSale", "unlockType": "cliff"},
            {"timestamp": (now + timedelta(days=1)).timestamp(), "noOfTokens": [999],
             "category": "emissions", "unlockType": "linear"},
            {"timestamp": (now - timedelta(days=1)).timestamp(), "noOfTokens": [999],
             "category": "insiders", "unlockType": "cliff"},
        ],
    }]}}}
    rows = token_unlock_context._public_calendar_events(
        payload, now=now,
        cfg={"public_horizon_days": 45, "include_unlock_types": ["cliff"],
             "symbol_overrides": {"ton": "TON"}},
    )
    assert len(rows) == 1
    assert rows[0]["asset_symbol"] == "TON"
    assert rows[0]["unlock_tokens"] == 60
    assert rows[0]["pct_circulating"] == 6
    assert rows[0]["quality_status"] == "provisional_public_calendar"


def test_token_unlock_context_selects_material_event_not_first_small_event(tmp_path):
    db = tmp_path / "unlock-priority.sqlite"
    now = datetime(2026, 7, 16, 12, tzinfo=UTC)
    with connect(db) as conn:
        for event_id, days, pct in (("small", 1, .1), ("material", 2, 8.0)):
            insert_unlock(conn, {
                "source": "fixture", "source_event_id": event_id,
                "observed_at": (now - timedelta(hours=1)).isoformat(), "asset_symbol": "ABC",
                "unlock_at": (now + timedelta(days=days)).isoformat(), "pct_circulating": pct,
                "recipient_type": "team", "unlock_type": "cliff", "quality_status": "ok",
                "raw_json": {"event": event_id},
            })
        conn.commit()
    result = token_unlock_context.context(
        "ABC/USDT", as_of=now, db_path=db,
        cfg={"paper_routing_enabled": False, "max_source_age_hours": 36,
             "min_pct_circulating": 5, "min_unlock_adv_days": 3,
             "warning_days": 30, "half_size_days": 14, "shadow_only_days": 3},
    )
    assert result["would_action"] == "SHADOW_ONLY"
    assert result["pct_circulating"] == 8
    assert result["events_considered"] == 2


def test_public_unlock_fallback_reuses_only_fresh_cache(tmp_path, monkeypatch):
    now = datetime(2026, 7, 16, 12, tzinfo=UTC)
    payload = {"props": {"pageProps": {"emissions": [{
        "protocolSlug": "abc", "name": "ABC", "circSupply": 1_000, "tSymbol": "ABC",
        "events": [{"timestamp": (now + timedelta(days=2)).timestamp(),
                    "noOfTokens": [100], "category": "insiders", "unlockType": "cliff"}],
    }]}}}

    class Response:
        content = b"ok"
        text = ("<script id=\"__NEXT_DATA__\" type=\"application/json\">" +
                json.dumps(payload) + "</script>")

        @staticmethod
        def raise_for_status():
            return None

    cfg = {"public_fallback_enabled": True, "public_fallback_url": "https://fixture.invalid",
           "public_cache_path": str(tmp_path / "unlock-cache.json"), "public_horizon_days": 45,
           "public_cache_max_age_hours": 48, "include_unlock_types": ["cliff"]}
    monkeypatch.setattr(token_unlock_context.requests, "get", lambda *args, **kwargs: Response())
    rows, status, fetched = token_unlock_context._public_fallback_rows(cfg, now=now)
    assert len(rows) == 1 and status == "ok_public_fallback" and fetched == now.isoformat()

    def offline(*args, **kwargs):
        raise RuntimeError("offline")

    monkeypatch.setattr(token_unlock_context.requests, "get", offline)
    cached, cached_status, cached_fetched = token_unlock_context._public_fallback_rows(
        cfg, now=now + timedelta(hours=1))
    assert len(cached) == 1
    assert cached_status == "ok_cached_public_fallback:RuntimeError"
    assert cached_fetched == fetched


def test_persistent_multivenue_depeg_routes_new_crypto_entry_to_shadow(tmp_path):
    db = tmp_path / "peg.sqlite"
    now = datetime(2026, 7, 16, 12, tzinfo=UTC)
    rows = []
    for stamp in (now - timedelta(minutes=10), now):
        for venue in ("coinbase", "kraken"):
            rows.append({"provider_ts": stamp.isoformat(), "received_at": stamp.isoformat(),
                         "exchange": venue, "stablecoin": "USDC", "quote_currency": "USD",
                         "bid": .974, "ask": .976, "mid": .975, "quality_status": "ok", "raw_json": {}})
    _insert_quotes(db, "stablecoin_peg_snapshots", market_risk_context.PEG_COLS, rows)
    cfg = {"paper_routing_enabled": True, "stablecoins": ["USDC"],
           "trusted_venues": ["coinbase", "kraken"], "max_quote_age_seconds": 300,
           "min_confirming_venues": 2, "persistence_minutes": 10,
           "watch_deviation_pct": .5, "stress_deviation_pct": 1, "crisis_deviation_pct": 2,
           "stress_action": "SHADOW_ONLY", "crisis_action": "SHADOW_ONLY"}
    state = market_risk_context.stablecoin_state(as_of=now, db_path=db, cfg=cfg)
    assert state["state"] == "CRISIS"
    assert state["persistent"] is True
    assert state["action"] == "SHADOW_ONLY"
    floor = paper_risk_floor(
        {"stablecoin_guard_state": state["state"], "stablecoin_guard_action": state["action"],
         "stablecoin_guard_persistent": True, "stablecoin_guard_asset": "USDC"},
        {"asset_class": "crypto", "mode": "intraday"},
        cfg={"enabled": True, "paper_only": True, "live_enabled": False,
             "crypto_modes": ("intraday", "swing"), "circuit_breaker": {"enabled": False}},
    )
    assert floor["paper_risk_floor_action"] == "SHADOW_ONLY"
    assert floor["paper_risk_floor_source"] == "paper_risk_guard_stablecoin_depeg"
    short_floor = paper_risk_floor(
        {"stablecoin_guard_state": "CRISIS", "stablecoin_guard_action": "SHADOW_ONLY",
         "stablecoin_guard_persistent": True, "stablecoin_guard_asset": "USDC"},
        {"asset_class": "crypto", "mode": "short"},
        cfg={"enabled": True, "paper_only": True, "live_enabled": False,
             "crypto_modes": ("intraday", "swing"), "circuit_breaker": {"enabled": False}},
    )
    assert short_floor["paper_risk_floor_action"] == "SHADOW_ONLY"


def test_cross_exchange_guard_requires_persistence_and_never_upgrades(tmp_path):
    db = tmp_path / "venues.sqlite"
    now = datetime(2026, 7, 16, 12, tzinfo=UTC)
    rows = []
    for stamp in (now - timedelta(minutes=5), now):
        for venue, mid in (("binance", 100.0), ("bybit", 103.0)):
            rows.append({"provider_ts": stamp.isoformat(), "received_at": stamp.isoformat(),
                         "exchange": venue, "symbol": "BTC/USDT", "bid": mid - .1, "ask": mid + .1,
                         "mid": mid, "mark_price": mid, "index_price": mid,
                         "quote_volume_24h": 1_000_000, "quality_status": "ok", "raw_json": {}})
    _insert_quotes(db, "cross_exchange_quote_snapshots", market_risk_context.QUOTE_COLS, rows)
    cfg = {"paper_routing_enabled": True, "trusted_venues": ["binance", "bybit"],
           "max_quote_age_seconds": 600, "min_fresh_trusted_venues": 2, "persistence_samples": 2,
           "major_symbols": ["BTC"], "half_divergence_bps_major": 25,
           "shadow_divergence_bps_major": 75, "half_divergence_bps_alt": 50,
           "shadow_divergence_bps_alt": 150}
    result = market_risk_context.cross_exchange_state("BTCUSDT", as_of=now, db_path=db, cfg=cfg)
    assert result["persistent"] is True
    assert result["action"] == "SHADOW_ONLY"
    missing = market_risk_context.cross_exchange_state("ETH/USDT", as_of=now, db_path=db, cfg=cfg)
    assert missing["action"] == "FULL_SIZE"


def test_crypto_overlay_composes_execution_guard_without_changing_geometry():
    cand = {"signal_id": "s", "symbol": "BTC/USDT", "mode": "intraday", "side": "long",
            "score": 80, "entry_mode": "PULLBACK_LIMIT", "timestamp": "2026-07-16T12:00:00Z"}
    mkt = {"status": "ok", "btc_regime_state": "trend", "btc_15m_return": .2,
           "btc_1h_return": .3, "btc_ema_slope_state": "up", "eth_confirm_state": "up"}
    sym = {"volume_rvol": 2, "funding_state": "normal", "spread_bps": 2,
           "cross_exchange_status": "ok", "cross_exchange_action": "HALF_SIZE",
           "cross_exchange_reason": "cross_exchange_divergence"}
    session = {"session_bucket_utc": "europe", "session_quality_state": "strong"}
    cfg = cqo.load_cfg()
    decision = cqo.evaluate(cand, mkt, sym, session, {}, {"by_symbol_mode": {}}, cfg)
    assert decision.action == "HALF_SIZE"
    assert any("cross_exchange_guard" in reason for reason in decision.reasons)


def test_crypto_filter_decisions_persist_in_sidecar_only(tmp_path):
    db = tmp_path / "intelligence.sqlite"
    decision = cqo.OverlayDecision(
        signal_id="sig-ctx", symbol="BTC/USDT", mode="intraday", action="HALF_SIZE",
        reasons=["cross_exchange_guard"], ctx={
            "token_unlock_status": "ok", "token_unlock_would_action": "HALF_SIZE",
            "token_unlock_reason": "material_token_unlock_near",
            "cross_exchange_status": "ok", "cross_exchange_action": "HALF_SIZE",
            "cross_exchange_would_action": "HALF_SIZE", "cross_exchange_reason": "divergence",
            "options_status": "ok", "options_iv30": 40, "options_rv30": 35,
        })
    assert cqo.persist_context_filter_decisions(decision, db_path=db) == 3
    with connect(db) as conn:
        names = {r[0] for r in conn.execute(
            "SELECT filter_name FROM context_filter_decisions WHERE signal_id='sig-ctx'")}
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert names == {"token_unlock", "cross_exchange_consistency", "crypto_iv_rv"}
    assert "proposed_signals" not in tables


def test_options_context_and_gex_are_advisory_by_default(tmp_path):
    db = tmp_path / "options.sqlite"
    now = datetime(2026, 7, 16, 12, tzinfo=UTC)
    row = {"provider_ts": now.isoformat(), "received_at": now.isoformat(), "asset_class": "stocks",
           "underlying": "SPY", "source": "fixture", "context_type": "gex_vrp",
           "spot_price": 100, "iv30": 24, "rv30": 18, "iv_rank": 75, "vrp": 6,
           "net_gex": 1_000_000, "gamma_flip": 98, "call_wall": 100.5, "put_wall": 95,
           "zero_dte_share": .4, "oi_as_of": now.isoformat(), "quality_status": "point_in_time",
           "raw_json": {}}
    _insert_quotes(db, "options_context_snapshots", options_context.OPTION_COLS, [row])
    result = stocks_overlay.evaluate(
        {"signal_id": "stk", "asset_class": "stocks", "mode": "intraday",
         "entry_mode": "BREAKOUT_CONTINUATION", "suggested_entry": 100, "atr14": 2},
        as_of=now, context_db_path=db,
        gex_cfg={"enabled": True, "paper_routing_enabled": False,
                 "near_wall_atr": .5, "positive_gamma_breakout_action": "HALF_SIZE"},
    )
    assert result["would_action"] == "HALF_SIZE"
    assert result["action"] == "FULL_SIZE"
    assert result["vrp"] == 6


def _bulk_zip() -> bytes:
    files = {
        "SUBMISSION.tsv": [
            ["ACCESSION_NUMBER", "FILING_DATE", "DOCUMENT_TYPE", "ISSUERCIK", "ISSUERTRADINGSYMBOL", "AFF10B5ONE"],
            ["a1", "2026-07-10", "4", "1", "TEST", "0"],
        ],
        "REPORTINGOWNER.tsv": [
            ["ACCESSION_NUMBER", "RPTOWNERCIK", "RPTOWNERNAME", "RPTOWNER_RELATIONSHIP", "RPTOWNER_TITLE"],
            ["a1", "o1", "Owner One", "Director", "Director"],
        ],
        "NONDERIV_TRANS.tsv": [
            ["ACCESSION_NUMBER", "TRANS_DATE", "TRANS_CODE", "TRANS_SHARES", "TRANS_PRICEPERSHARE",
             "TRANS_ACQUIRED_DISP_CD", "SHRS_OWND_FOLWNG_TRANS", "DIRECT_INDIRECT_OWNERSHIP"],
            ["a1", "2026-07-09", "P", "1000", "20", "A", "2000", "D"],
        ],
    }
    target = io.BytesIO()
    with zipfile.ZipFile(target, "w") as zf:
        for name, rows in files.items():
            zf.writestr(name, "\n".join("\t".join(row) for row in rows) + "\n")
    return target.getvalue()


def test_sec_form4_parser_and_opportunistic_cluster(tmp_path):
    parsed = insider_context.parse_bulk_zip(_bulk_zip(), universe={"TEST"})
    assert len(parsed) == 1
    assert parsed[0]["transaction_code"] == "P"
    db = tmp_path / "insider.sqlite"
    now = datetime(2026, 7, 16, tzinfo=UTC)
    rows = []
    for owner, value in (("o1", 60_000), ("o2", 70_000)):
        rows.append({**parsed[0], "accession_number": f"current-{owner}", "owner_cik": owner,
                     "owner_name": owner, "filing_at": "2026-07-10", "transaction_at": "2026-07-09",
                     "transaction_value_usd": value, "shares": value / 20})
    for year in (2023, 2024, 2025):
        rows.append({**parsed[0], "accession_number": f"old-{year}", "owner_cik": "o1",
                     "filing_at": f"{year}-07-10", "transaction_at": f"{year}-07-09",
                     "transaction_value_usd": 10_000})
    _insert_quotes(db, "insider_transactions", insider_context.INSIDER_COLS, rows)
    result = insider_context.ticker_context(
        "TEST", as_of=now, db_path=db,
        cfg={"cluster_window_days": 30, "history_years": 3, "min_cluster_insiders": 2,
             "min_total_purchase_usd": 50_000, "require_transaction_code": "P",
             "exclude_10b5_1": True, "paper_routing_enabled": False},
    )
    assert result["cluster_confirmed"] is True
    assert result["opportunistic_purchase_count"] == 1


def test_overnight_filter_uses_only_same_day_features_and_remains_counterfactual():
    cfg = {"min_close_location": .8, "require_above_vwap": True,
           "require_positive_relative_strength": True, "exclude_friday": True,
           "excluded_event_types": ["earnings", "legal_risk"]}
    eligible, reasons, features = catalyst_rs.overnight_eligibility(
        session_date=date(2026, 7, 14), event_type="partnership", close_price=109,
        day_low=100, day_high=110, day_vwap=105, rs_spy=2, rs_sector=1,
        event_valid_next_session=True, cfg=cfg)
    assert eligible is True and reasons == []
    assert features["close_location"] == .9
    friday, reasons, _ = catalyst_rs.overnight_eligibility(
        session_date=date(2026, 7, 17), event_type="partnership", close_price=109,
        day_low=100, day_high=110, day_vwap=105, rs_spy=2, rs_sector=1,
        event_valid_next_session=True, cfg=cfg)
    assert friday is False and "FRIDAY_EXCLUDED" in reasons


def test_realized_vol_is_deterministic():
    closes = [100 + i * .5 for i in range(31)]
    first = options_context.realized_vol_from_closes(closes)
    second = options_context.realized_vol_from_closes(closes)
    assert first is not None and first == second


def test_gex_proxy_is_deterministic_and_explicitly_model_based():
    now = datetime(2026, 7, 16, 12, tzinfo=UTC)
    expiration = (now + timedelta(days=30)).isoformat()
    contracts = [
        {"option_type": "call", "expiration": expiration, "strike": 100,
         "iv": .25, "open_interest": 5_000},
        {"option_type": "call", "expiration": expiration, "strike": 105,
         "iv": .27, "open_interest": 2_000},
        {"option_type": "put", "expiration": expiration, "strike": 95,
         "iv": .28, "open_interest": 500},
    ]
    first = options_context.calculate_gex_proxy(contracts, spot=100, as_of=now)
    second = options_context.calculate_gex_proxy(contracts, spot=100, as_of=now)
    assert first == second
    assert first["net_gex"] > 0
    assert first["call_wall"] == 100
    assert first["put_wall"] == 95
    assert first["contracts_used"] == 3
    assert "proxy" in first["method"]


def test_scheduler_orders_risk_refresh_before_tracker_and_schedules_shadow_contexts():
    from scripts.run_default_market_schedule import build_cycle_steps
    steps = build_cycle_steps(
        now=datetime(2026, 7, 16, 12, tzinfo=UTC), crypto_only=False,
        include_long_horizon=True, monitor_minutes=1, skip_reports=False)
    labels = [step[0] for step in steps]
    commands = [" ".join(step[1]) for step in steps]
    assert labels.index("stablecoin + cross-exchange risk context") < labels.index("track-signals (pre)")
    assert labels.index("options context (IV/RV + GEX)") < labels.index("track-signals (pre)")
    assert labels.index("token unlock context (shadow advisory)") < labels.index("track-signals (pre)")
    assert any("context-options-refresh" in cmd for cmd in commands)
    assert any("context-token-unlock-refresh" in cmd for cmd in commands)
    assert any("context-insider-refresh" in cmd for cmd in commands)
    assert any("context-filters-report" in cmd for cmd in commands)
