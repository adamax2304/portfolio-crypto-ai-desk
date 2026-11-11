"""NEXT STEP — paper-shadow A/B execution engine tests (measurement only, no network/live)."""
from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd

from src.execution.paper_shadow_engine import _walk, _entry_fill, simulate_branch, entry_deadline_for


def _bars(rows, start="2026-06-20 10:00"):
    ts = pd.date_range(start, periods=len(rows), freq="15min", tz="UTC")
    return pd.DataFrame({"timestamp": ts,
                         "open": [r[0] for r in rows], "high": [r[1] for r in rows],
                         "low": [r[2] for r in rows], "close": [r[3] for r in rows]})


def _bars_at(specs):
    """specs: list of (timestamp_str, open, high, low, close) -- arbitrary, non-uniform spacing."""
    ts = pd.to_datetime([s[0] for s in specs], utc=True)
    return pd.DataFrame({"timestamp": ts, "open": [s[1] for s in specs], "high": [s[2] for s in specs],
                         "low": [s[3] for s in specs], "close": [s[4] for s in specs]})


def test_breakout_fills_when_pullback_misses():
    # price never pulls back into [98,99] but breaks up through trigger 101 → breakout fills, pullback doesn't
    rows = [(100, 100.5, 99.8, 100.3), (100.4, 101.5, 100.2, 101.2), (101.3, 103, 101.1, 102.8)]
    cs = _bars(rows)
    pull = _walk(direction="long", entry_mode="PULLBACK_LIMIT", entry_low=98, entry_high=99,
                 entry_trigger=101, suggested=None, tp1=104, tp2=106, tp3=108, stop0=97,
                 stop_after_tp1=None, stop_after_tp2=None, candles=cs)
    brk = _walk(direction="long", entry_mode="BREAKOUT_CONTINUATION", entry_low=98, entry_high=99,
                entry_trigger=101, suggested=None, tp1=104, tp2=106, tp3=108, stop0=97,
                stop_after_tp1=None, stop_after_tp2=None, candles=cs)
    assert pull.entered is False         # pullback zone never touched
    assert brk.entered is True           # breakout entered on the level break
    assert brk.entry_px == 101


def test_no_chase_skip_does_not_enter():
    fill, otype, _at_open = _entry_fill("NO_CHASE_SKIP", {"high": 110, "low": 100, "open": 105, "close": 108},
                              long=True, entry_low=100, entry_high=101, entry_trigger=None,
                              suggested=None, is_first=True)
    assert fill is None and otype == "none"


def test_new_logic_shadow_skips_policy_disabled_crypto_pullback():
    ov = {"entry_mode": {}, "preentry_mode": {"entry_mode": "PULLBACK_LIMIT", "data_quality": "ok",
                                                  "source": "entry_path"}, "paper_tp": {},
          "stop_plan": {}, "stock_dir": {}}
    sig = {"signal_id": "sig_policy_disabled", "symbol": "BTC/USDT", "direction": "long",
           "mode": "intraday", "asset_class": "crypto", "entry_low": 99, "entry_high": 100,
           "entry_trigger": 100, "stop0": 95, "tp1": 102, "tp2": 104, "tp3": 106}
    rec, _ = simulate_branch("new_logic_shadow", sig, ov, candles=None,
                             fee_profile="bybit_non_vip_usdt_perp")
    assert rec["entry_fill_status"] == "skipped"
    assert rec["skipped_shadow_reason"] == "crypto_entry_mode_disabled_by_policy"


def test_new_logic_shadow_never_falls_back_to_post_entry_mode_for_crypto():
    ov = {"entry_mode": {"entry_mode": "BREAKOUT_CONTINUATION"}, "preentry_mode": {},
          "paper_tp": {}, "stop_plan": {}, "stock_dir": {}}
    sig = {"signal_id": "sig_missing_pre", "symbol": "BTC/USDT", "direction": "long",
           "mode": "intraday", "asset_class": "crypto", "entry_low": 99, "entry_high": 100,
           "entry_trigger": 100, "stop0": 95, "tp1": 102, "tp2": 104, "tp3": 106}
    rec, _ = simulate_branch("new_logic_shadow", sig, ov, candles=None,
                             fee_profile="bybit_non_vip_usdt_perp")
    assert rec["entry_fill_status"] == "skipped"
    assert rec["skipped_shadow_reason"] == "preentry_mode_unavailable"
    assert rec["entry_mode_source"] == "preentry"


def test_legacy_crypto_forward_pairs_are_demoted_from_evidence(tmp_path):
    import sqlite3
    from src.execution.paper_shadow_engine import ensure_tables, demote_legacy_crypto_forward_evidence
    db = str(tmp_path / "shadow.sqlite")
    c = sqlite3.connect(db)
    ensure_tables(c)
    rows = [
        ("old", "old_paper", "crypto", "forward_since_activation", None),
        ("old", "new_logic_shadow", "crypto", "forward_since_activation", None),
        ("new", "old_paper", "crypto", "forward_since_activation", "legacy_shadow_v1"),
        ("new", "new_logic_shadow", "crypto", "forward_since_activation", "preentry_v2"),
        ("stock", "new_logic_shadow", "stocks", "forward_since_activation", None),
    ]
    for row in rows:
        c.execute("INSERT INTO paper_shadow_execution_outcomes "
                  "(signal_id,branch,asset_class,window,entry_mode_version,fee_profile) VALUES (?,?,?,?,?,?)",
                  (*row, "bybit_non_vip_usdt_perp"))
    assert demote_legacy_crypto_forward_evidence(c) == 2
    got = {(r[0], r[1]): r[2] for r in c.execute(
        "SELECT signal_id,branch,window FROM paper_shadow_execution_outcomes")}
    c.close()
    assert got[("old", "old_paper")] == "historical_backfill"
    assert got[("old", "new_logic_shadow")] == "historical_backfill"
    assert got[("new", "old_paper")] == "forward_since_activation"
    assert got[("new", "new_logic_shadow")] == "forward_since_activation"
    assert got[("stock", "new_logic_shadow")] == "forward_since_activation"


def test_stock_candidate_v2_demotes_every_pre_activation_forward_row(tmp_path):
    import sqlite3
    from src.execution.paper_shadow_engine import (
        ensure_tables, demote_legacy_stock_candidate_forward_evidence,
    )
    db = sqlite3.connect(str(tmp_path / "stock_v2.sqlite"))
    ensure_tables(db)
    rows = [
        ("old", "stocks_intraday_forward", "2026-09-01T14:00:00+00:00"),
        ("fresh", "stocks_intraday_forward", "2026-09-28T14:00:00+00:00"),
        ("other", "ab_main", "2026-09-01T14:00:00+00:00"),
    ]
    for sid, lane, created in rows:
        db.execute(
            "INSERT INTO paper_shadow_execution_outcomes "
            "(signal_id,branch,shadow_lane,window,created_at) VALUES (?,?,?,?,?)",
            (sid, "new_logic_shadow", lane, "forward_since_activation", created),
        )
    changed = demote_legacy_stock_candidate_forward_evidence(
        db, "2026-09-27T12:00:00+00:00")
    got = {row[0]: row[1] for row in db.execute(
        "SELECT signal_id,window FROM paper_shadow_execution_outcomes")}
    assert changed == 1
    assert got == {
        "old": "historical_backfill",
        "fresh": "forward_since_activation",
        "other": "forward_since_activation",
    }


def test_momentum_taker_enters_immediately():
    fill, otype, _at_open = _entry_fill("MOMENTUM_TAKER_NOW", {"high": 110, "low": 100, "open": 105, "close": 108},
                              long=True, entry_low=None, entry_high=None, entry_trigger=None,
                              suggested=None, is_first=True)
    assert fill == 105 and otype == "taker"


def test_b_branch_skips_on_stock_neutral_direction(monkeypatch):
    import src.execution.paper_shadow_engine as m
    sig = {"signal_id": "s1", "symbol": "AAPL", "direction": "long", "asset_class": "stocks",
           "playbook": "x", "entry_low": 100, "entry_high": 101, "entry_trigger": None,
           "stop0": 98, "tp1": 104, "tp2": 106, "tp3": 108, "economic_trade_key": "k"}
    ov = {"entry_mode": {"entry_mode": "PULLBACK_LIMIT"}, "paper_tp": {},
          "stop_plan": {}, "stock_dir": {"direction": "neutral", "is_point_in_time": 1}}
    rec, _ev = simulate_branch("new_logic_shadow", sig, ov, _bars([(100.5, 101, 100, 100.5)]), "bybit_non_vip_usdt_perp")
    assert rec["entry_fill_status"] == "skipped"
    assert rec["skipped_shadow_reason"] == "stock_direction_neutral"


def test_b_branch_direction_flip_recorded(monkeypatch):
    sig = {"signal_id": "s2", "symbol": "MSTR", "direction": "long", "asset_class": "stocks",
           "playbook": "x", "entry_low": 100, "entry_high": 101, "entry_trigger": None,
           "stop0": 98, "tp1": 104, "tp2": 106, "tp3": 108, "economic_trade_key": "k"}
    ov = {"entry_mode": {"entry_mode": "PULLBACK_LIMIT"}, "paper_tp": {},
          "stop_plan": {}, "stock_dir": {"direction": "short", "is_point_in_time": 1}}
    rec, _ev = simulate_branch("new_logic_shadow", sig, ov, _bars([(100.5, 101, 100, 100.5)]), "bybit_non_vip_usdt_perp")
    assert rec["direction_changed"] == 1 and rec["side"] == "short" and rec["old_side"] == "long"


def test_stock_direction_overlay_requires_point_in_time_evidence():
    sig = {"signal_id": "late_score", "symbol": "AAPL", "direction": "long",
           "asset_class": "stocks", "playbook": "x", "entry_low": 100, "entry_high": 101,
           "entry_trigger": None, "stop0": 98, "tp1": 104, "tp2": 106, "tp3": 108}
    ov = {"entry_mode": {"entry_mode": "PULLBACK_LIMIT"}, "paper_tp": {},
          "stop_plan": {}, "stock_dir": {"direction": "short", "is_point_in_time": 0}}
    rec, _ = simulate_branch("new_logic_shadow", sig, ov, _bars([(100.5, 101, 100, 100.5)]),
                             "stock_etf_default")
    assert rec["entry_fill_status"] == "skipped"
    assert rec["skipped_shadow_reason"] == "stock_direction_not_point_in_time"


def test_stock_new_logic_never_falls_back_when_direction_score_is_missing():
    sig = {"signal_id": "missing_score", "symbol": "AAPL", "direction": "long",
           "asset_class": "stocks", "playbook": "x", "entry_low": 100, "entry_high": 101,
           "entry_trigger": None, "stop0": 98, "tp1": 104, "tp2": 106, "tp3": 108}
    ov = {"entry_mode": {"entry_mode": "PULLBACK_LIMIT"}, "paper_tp": {},
          "stop_plan": {}, "stock_dir": {}}
    rec, _ = simulate_branch("new_logic_shadow", sig, ov, _bars([(100.5, 101, 100, 100.5)]),
                             "stock_etf_default")
    assert rec["entry_fill_status"] == "skipped"
    assert rec["skipped_shadow_reason"] == "stock_direction_missing"


def test_stock_direction_flip_rebuilds_stop_and_targets():
    from src.execution.paper_shadow_engine import _branch_inputs
    sig = {"signal_id": "flip_geometry", "symbol": "AAPL", "direction": "long",
           "asset_class": "stocks", "entry_low": 100, "entry_high": 101,
           "entry_trigger": None, "stop0": 98, "tp1": 104, "tp2": 106, "tp3": 108}
    ov = {"entry_mode": {"entry_mode": "PULLBACK_LIMIT"}, "paper_tp": {}, "stop_plan": {},
          "stock_dir": {"direction": "short", "is_point_in_time": 1}}
    inp = _branch_inputs("new_logic_shadow", sig, ov)
    assert inp["direction"] == "short"
    assert inp["stop0"] == 103
    assert (inp["tp1"], inp["tp2"], inp["tp3"]) == (97, 95, 93)


def test_stock_candidate_lane_uses_setup_hint_for_entry_mode():
    """Forward stock candidates must test the current setup, not default every row to pullback."""
    from src.execution.paper_shadow_engine import _branch_inputs
    sig = {"signal_id": "candidate", "symbol": "AAPL", "direction": "long",
           "asset_class": "stocks", "mode": "intraday", "playbook": "breakout",
           "entry_mode_hint": "breakout", "candidate_lane": True,
           "entry_low": 100, "entry_high": 101, "entry_trigger": 102, "stop0": 98,
           "tp1": 104, "tp2": 106, "tp3": 108}
    inp = _branch_inputs("new_logic_shadow", sig,
                         {"entry_mode": {}, "paper_tp": {}, "stop_plan": {}, "stock_dir": {}})
    assert inp["entry_mode"] == "BREAKOUT_CONTINUATION"
    assert inp["entry_mode_source"] == "candidate_setup_hint"


def test_load_signals_includes_untriggered_stock_intraday_ab_candidates(tmp_path):
    import sqlite3
    from src.execution.paper_shadow_engine import _load_signals
    db = sqlite3.connect(str(tmp_path / "candidate.sqlite"))
    db.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, direction TEXT, mode TEXT, "
               "asset_class TEXT, setup_type TEXT, market_regime TEXT, created_at TEXT, "
               "suggested_entry REAL, entry_trigger REAL, entry_low REAL, entry_high REAL, "
               "stop_loss REAL, invalidation REAL, tp1 REAL, tp2 REAL, tp3 REAL, tier TEXT, status TEXT)")
    db.execute("CREATE TABLE signal_outcomes (id INTEGER PRIMARY KEY, signal_id TEXT, checked_at TEXT, "
               "entry_triggered INTEGER, entry_triggered_at TEXT)")
    db.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
               ("st_candidate", "AAPL", "long", "intraday", "stocks", "breakout", "trend",
                "2026-07-06T14:00:00+00:00", 100, 102, 100, 101, 98, 98, 104, 106, 108, "A", "waiting_for_entry"))
    db.commit()
    rows = _load_signals(db, None, limit=20, include_stock_intraday_candidates=True)
    db.close()
    assert len(rows) == 1 and rows[0]["candidate_lane"] is True
    assert rows[0]["tier"] == "A" and rows[0]["status"] == "waiting_for_entry"


def test_stock_candidate_lane_is_not_added_to_paired_ab_books(tmp_path, monkeypatch):
    """B-only stock candidates must have independent stats, never a fake A/B delta."""
    import sqlite3
    import src.execution.paper_shadow_engine as engine

    db = str(tmp_path / "candidate_stats.sqlite")
    sqlite3.connect(db).close()
    now = datetime.now(timezone.utc).isoformat()
    candidate = {"signal_id": "candidate_stats", "symbol": "AAPL", "direction": "long",
                 "mode": "intraday", "asset_class": "stocks", "playbook": "breakout",
                 "entry_mode_hint": "breakout", "candidate_lane": True, "created_at": now,
                 "exchange_focus": "",
                 "entry_low": 100.0, "entry_high": 101.0, "entry_trigger": 102.0, "stop0": 98.0,
                 "tp1": 104.0, "tp2": 106.0, "tp3": 108.0, "economic_trade_key": "candidate_stats"}
    monkeypatch.setattr(engine, "_load_signals", lambda *args, **kwargs: [candidate])
    monkeypatch.setattr(engine, "_load_candles", lambda *args, **kwargs: (None, None))
    monkeypatch.setattr(engine, "prune_shadow_scope", lambda conn: {})
    monkeypatch.setattr(engine, "_stock_intraday_candidate_cfg", lambda: {
        "enabled": True, "branches": ["new_logic_shadow"],
        "entry_modes": ["BREAKOUT_CONTINUATION"],
        "require_rth_created": False,
        "activation_meta_key": "candidate_stats_activation",
    })
    monkeypatch.setattr(engine, "simulate_branch", lambda branch, sig, ov, candles, fp: ({
        "signal_id": sig["signal_id"], "branch": branch, "asset_class": "stocks",
        "symbol": sig["symbol"], "entry_mode": "BREAKOUT_CONTINUATION",
        "entry_fill_status": "filled", "net_r": 2.0, "net_pnl_usdt": 50.0,
        "fees_usdt": 1.0, "slippage_usdt": 0.5, "gross_r": 2.1,
    }, []))

    stats = engine.refresh(lookback_hours=None, rebuild=True, db=db)

    assert stats["candidate_filled"] == 1
    assert stats["candidate_net_r"] == 2.0
    assert stats["candidate_net_usd"] == 50.0
    assert stats["candidate_by_mode"]["BREAKOUT_CONTINUATION"]["filled"] == 1
    assert stats["A_filled"] == 0 and stats["B_filled"] == 0
    assert stats["forward_since_activation"]["B_filled"] == 0
    assert stats["by_asset"]["stocks"]["B_filled"] == 0


def test_prune_shadow_scope_removes_orphan_event_streams(tmp_path):
    import sqlite3
    from src.execution.paper_shadow_engine import ensure_tables, prune_shadow_scope

    db = str(tmp_path / "orphan_events.sqlite")
    conn = sqlite3.connect(db)
    ensure_tables(conn)
    conn.execute("CREATE TABLE proposed_signals (signal_id TEXT, asset_class TEXT, mode TEXT)")
    conn.execute("INSERT INTO paper_shadow_execution_outcomes (signal_id, branch) VALUES ('live', 'old_paper')")
    conn.execute("INSERT INTO paper_shadow_events (signal_id, branch, seq, event) VALUES ('live', 'old_paper', 1, 'entry')")
    conn.execute("INSERT INTO paper_shadow_events (signal_id, branch, seq, event) VALUES ('ghost', 'old_paper', 1, 'entry')")
    conn.commit()

    removed = prune_shadow_scope(conn)

    assert removed["orphan_events"] == 1
    assert conn.execute("SELECT COUNT(*) FROM paper_shadow_events").fetchone()[0] == 1
    conn.close()


def test_fees_reduce_net_below_gross():
    sig = {"signal_id": "s3", "symbol": "BTC/USDT", "direction": "long", "asset_class": "crypto",
           "playbook": "x", "entry_low": 99.5, "entry_high": 100.5, "entry_trigger": None,
           "stop0": 98, "tp1": 102, "tp2": 104, "tp3": 106, "economic_trade_key": "k"}
    ov = {"entry_mode": {}, "paper_tp": {}, "stop_plan": {}, "stock_dir": {}}
    cs = _bars([(100, 100.2, 99.6, 100), (100, 103, 100, 102.5), (102.5, 107, 102, 106.5)])
    rec, _ev = simulate_branch("old_paper", sig, ov, cs, "bybit_non_vip_usdt_perp")
    if rec["entry_fill_status"] == "filled" and rec["gross_r"] and rec["gross_r"] > 0:
        assert rec["fees_usdt"] >= 0
        assert rec["net_r"] <= rec["gross_r"]   # fees + slippage drag


# ---- item 1 (2026-07-03): per-asset PAPER fee profile (cost model only, no A/B logic change) ----
def test_select_fee_profile_per_asset():
    from src.execution.paper_shadow_engine import select_fee_profile, STOCK_FEE_PROFILE, CRYPTO_FEE_PROFILE
    for a in ("stocks", "stock", "Equities", "ETF", "etfs"):
        assert select_fee_profile(a) == STOCK_FEE_PROFILE == "stock_etf_default"
    for a in ("crypto", "", None, "usdt_perp"):
        assert select_fee_profile(a) == CRYPTO_FEE_PROFILE == "bybit_non_vip_usdt_perp"


def _seed_shadow_db(tmp_path):
    """Minimal DB with one stock + one crypto entry-triggered signal so refresh() can run offline."""
    import sqlite3
    from pathlib import Path
    p = Path(tmp_path) / "shadow.sqlite"
    c = sqlite3.connect(str(p))
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, direction TEXT, mode TEXT, "
              "asset_class TEXT, setup_type TEXT, market_regime TEXT, exchange_focus TEXT, "
              "created_at TEXT, suggested_entry REAL, entry_trigger REAL, entry_low REAL, "
              "entry_high REAL, stop_loss REAL, invalidation REAL, tp1 REAL, tp2 REAL, tp3 REAL)")
    c.execute("CREATE TABLE signal_outcomes (id INTEGER PRIMARY KEY, signal_id TEXT, checked_at TEXT, "
              "entry_triggered INTEGER, entry_triggered_at TEXT)")
    rows = [
        ("stk1", "ZZZZ", "long", "swing", "stocks"),   # swing: in shadow scope (intraday is excluded)
        ("cry1", "ZZZ/USDT", "long", "intraday", "crypto"),
    ]
    for sid, sym, d, mode, ac in rows:
        c.execute("INSERT INTO proposed_signals (signal_id,symbol,direction,mode,asset_class,"
                  "created_at,entry_low,entry_high,invalidation,tp1,tp2,tp3) "
                  "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (sid, sym, d, mode, ac, "2026-06-01T10:00:00+00:00", 100.0, 101.0, 98.0, 104, 106, 108))
        c.execute("INSERT INTO signal_outcomes (signal_id,checked_at,entry_triggered,entry_triggered_at) "
                  "VALUES (?,?,?,?)", (sid, "2026-06-01T11:00:00+00:00", 1, "2026-06-01T10:30:00+00:00"))
    c.commit()
    c.close()
    return str(p)


def test_refresh_assigns_stock_profile_and_crypto_profile(tmp_path):
    import sqlite3
    from src.execution.paper_shadow_engine import refresh
    db = _seed_shadow_db(tmp_path)
    stats = refresh(lookback_hours=None, rebuild=True, db=db)
    c = sqlite3.connect(db)
    c.row_factory = sqlite3.Row
    prof = {r["symbol"]: (r["fee_profile"], r["cost_model_asset_class"], r["fee_profile_selected"])
            for r in c.execute("SELECT symbol, fee_profile, cost_model_asset_class, fee_profile_selected "
                               "FROM paper_shadow_execution_outcomes").fetchall()}
    c.close()
    # stock signal → stock_etf_default; crypto signal → bybit_non_vip_usdt_perp
    assert prof["ZZZZ"][0] == "stock_etf_default"
    assert prof["ZZZZ"][1] == "stocks" and prof["ZZZZ"][2] == "stock_etf_default"
    assert prof["ZZZ/USDT"][0] == "bybit_non_vip_usdt_perp"
    assert prof["ZZZ/USDT"][1] == "crypto"
    # refresh reports per-asset fee profile mapping
    assert stats["fee_profile_by_asset"] == {"crypto": "bybit_non_vip_usdt_perp",
                                             "stocks": "stock_etf_default"}
    assert "by_asset" in stats and "delta_net_r" in stats["by_asset"]["stocks"]


def test_mark_stale_cost_model_flags_wrong_stock_rows(tmp_path):
    import sqlite3
    from src.execution.paper_shadow_engine import ensure_tables, mark_stale_cost_model, STOCK_FEE_PROFILE
    from pathlib import Path
    db = str(Path(tmp_path) / "stale.sqlite")
    c = sqlite3.connect(db)
    ensure_tables(c)
    # a stock row written under the WRONG (crypto) fee profile — the historical distortion
    c.execute("INSERT INTO paper_shadow_execution_outcomes (signal_id,branch,symbol,asset_class,"
              "fee_profile,cost_model_status) VALUES ('x','old_paper','AAPL','stocks',"
              "'bybit_non_vip_usdt_perp','current')")
    # a stock row under the correct profile + a crypto row — must stay untouched
    c.execute("INSERT INTO paper_shadow_execution_outcomes (signal_id,branch,symbol,asset_class,"
              "fee_profile,cost_model_status) VALUES ('y','old_paper','MSFT','stocks',?,'current')",
              (STOCK_FEE_PROFILE,))
    c.execute("INSERT INTO paper_shadow_execution_outcomes (signal_id,branch,symbol,asset_class,"
              "fee_profile,cost_model_status) VALUES ('z','old_paper','BTC/USDT','crypto',"
              "'bybit_non_vip_usdt_perp','current')")
    c.commit()
    n = mark_stale_cost_model(c)
    c.commit()
    assert n == 1
    got = {r[0]: r[1] for r in c.execute(
        "SELECT signal_id, cost_model_status FROM paper_shadow_execution_outcomes")}
    c.close()
    assert got["x"] == "stale_cost_model"     # wrong-profile stock row flagged
    assert got["y"] == "current"              # correct stock row untouched
    assert got["z"] == "current"              # crypto row untouched


# ============================ expiry-aware entry simulation (audit item #3 follow-up) ============

def test_entry_deadline_for_prefers_expires_at_then_validity_hours_then_mode_default():
    d1 = entry_deadline_for({"created_at": "2026-06-20T10:00:00+00:00",
                             "expires_at": "2026-06-20T11:00:00+00:00",
                             "validity_window_hours": 24, "mode": "scalp"})
    assert d1 == datetime(2026, 6, 20, 11, 0, tzinfo=timezone.utc)   # expires_at wins outright

    d2 = entry_deadline_for({"created_at": "2026-06-20T10:00:00+00:00", "expires_at": None,
                             "validity_window_hours": 3, "mode": "scalp"})
    assert d2 == datetime(2026, 6, 20, 13, 0, tzinfo=timezone.utc)   # created_at + validity_window_hours

    d3 = entry_deadline_for({"created_at": "2026-06-20T10:00:00+00:00", "expires_at": None,
                             "validity_window_hours": None, "mode": "scalp"})
    assert d3 == datetime(2026, 6, 20, 12, 0, tzinfo=timezone.utc)   # mode default: scalp=2h

    d4 = entry_deadline_for({"created_at": "2026-06-20T10:00:00+00:00", "expires_at": None,
                             "validity_window_hours": None, "mode": "intraday"})
    assert d4 == datetime(2026, 6, 21, 10, 0, tzinfo=timezone.utc)   # mode default: intraday=24h

    d5 = entry_deadline_for({"created_at": "2026-06-20T10:00:00+00:00", "expires_at": None,
                             "validity_window_hours": None, "mode": "swing"})
    assert d5 == datetime(2026, 6, 27, 10, 0, tzinfo=timezone.utc)   # mode default: swing=168h (7d)

    assert entry_deadline_for({"created_at": None, "expires_at": None}) is None  # no anchor at all


def test_stock_shadow_ignores_impossible_previous_session_expiry():
    deadline = entry_deadline_for({
        "asset_class": "stocks",
        "mode": "intraday",
        "created_at": "2026-07-28T22:00:00+00:00",
        "expires_at": "2026-07-28T20:00:00+00:00",
    })
    assert deadline == datetime(2026, 7, 29, 20, 0, tzinfo=timezone.utc)


def test_stock_intraday_shadow_is_trimmed_at_same_day_rth_close():
    sig = {"signal_id": "stock_eod", "symbol": "AAPL", "direction": "long", "mode": "intraday",
           "asset_class": "stocks", "candidate_lane": True, "entry_mode_hint": "pullback",
           "created_at": "2026-07-08T19:00:00+00:00", "entry_low": 99.0, "entry_high": 100.0,
           "entry_trigger": None, "stop0": 98.0, "tp1": 104.0, "tp2": 106.0, "tp3": 108.0}
    candles = _bars_at([
        ("2026-07-08 19:15", 100.0, 100.5, 99.0, 100.0),
        ("2026-07-09 13:30", 100.0, 110.0, 100.0, 109.0),
    ])
    rec, events = simulate_branch("new_logic_shadow", sig,
                                      {"entry_mode": {}, "paper_tp": {}, "stop_plan": {},
                                       "stock_dir": {"direction": "long", "is_point_in_time": 1}},
                                      candles, "stock_etf_default")
    assert rec["entry_fill_status"] == "filled"
    assert rec["close_reason"] == "expired_exit"
    assert all("2026-07-09" not in str(event.get("timestamp")) for event in events)


def test_walk_blocks_scalp_entry_that_would_only_fill_14_days_later():
    # scalp signal, 2h validity -> deadline 12:00. Price never touches [98,99] within the window,
    # but DOES touch it 14 days later (reproduces the historical bug this fix targets).
    deadline = datetime(2026, 6, 20, 12, 0, tzinfo=timezone.utc)
    cs = _bars_at([
        ("2026-06-20 10:15", 100.5, 100.6, 100.2, 100.4),   # within window, no touch
        ("2026-06-20 11:00", 100.3, 100.4, 100.1, 100.2),   # within window, no touch
        ("2026-07-04 09:00", 99.5, 99.6, 98.5, 99.0),        # 14 days later -- would trade through
    ])
    w = _walk(direction="long", entry_mode="PULLBACK_LIMIT", entry_low=98, entry_high=99,
              entry_trigger=None, suggested=None, tp1=104, tp2=106, tp3=108, stop0=97,
              stop_after_tp1=None, stop_after_tp2=None, candles=cs, entry_deadline=deadline)
    assert w.entered is False
    assert w.blocked_by_expiry is True
    assert w.outcome == "no_entry" and w.close_reason == "expired_no_fill"


def test_walk_allows_entry_within_validity_window():
    # same zone, but the touch happens BEFORE the deadline -> must fill normally.
    deadline = datetime(2026, 6, 20, 12, 0, tzinfo=timezone.utc)
    cs = _bars_at([
        ("2026-06-20 10:15", 100.5, 100.6, 100.2, 100.4),
        ("2026-06-20 10:45", 99.2, 99.3, 98.5, 98.8),   # within window -- trades through the zone
        ("2026-06-20 11:15", 99.0, 99.2, 98.9, 99.1),
    ])
    w = _walk(direction="long", entry_mode="PULLBACK_LIMIT", entry_low=98, entry_high=99,
              entry_trigger=None, suggested=None, tp1=104, tp2=106, tp3=108, stop0=97,
              stop_after_tp1=None, stop_after_tp2=None, candles=cs, entry_deadline=deadline)
    assert w.entered is True
    assert w.blocked_by_expiry is False


def test_walk_intraday_expiry_blocks_late_fill():
    # intraday: 24h validity from 2026-06-20T00:00 -> deadline 2026-06-21T00:00.
    deadline = datetime(2026, 6, 21, 0, 0, tzinfo=timezone.utc)
    cs = _bars_at([
        ("2026-06-20 05:00", 100.5, 100.6, 100.2, 100.4),   # within window, no touch
        ("2026-06-25 09:00", 99.5, 99.6, 98.5, 99.0),        # 5 days later -- past 24h deadline
    ])
    w = _walk(direction="long", entry_mode="PULLBACK_LIMIT", entry_low=98, entry_high=99,
              entry_trigger=None, suggested=None, tp1=104, tp2=106, tp3=108, stop0=97,
              stop_after_tp1=None, stop_after_tp2=None, candles=cs, entry_deadline=deadline)
    assert w.entered is False
    assert w.blocked_by_expiry is True


def test_simulate_branch_marks_late_fill_missed_with_after_expiry_blocked_status():
    sig = {"signal_id": "sig_test_expiry", "symbol": "BTCUSDT", "direction": "long", "mode": "scalp",
          "asset_class": "crypto", "created_at": "2026-06-20T10:00:00+00:00",
          "expires_at": None, "validity_window_hours": 2,
          "entry_low": 98, "entry_high": 99, "entry_trigger": None, "suggested_entry": None,
          "tp1": 104, "tp2": 106, "tp3": 108, "stop0": 97, "economic_trade_key": "k_expiry_test"}
    cs = _bars_at([
        ("2026-06-20 10:15", 100.5, 100.6, 100.2, 100.4),
        ("2026-07-04 09:00", 99.5, 99.6, 98.5, 99.0),
    ])
    rec, events = simulate_branch("old_paper", sig, {}, cs, "bybit_non_vip_usdt_perp")
    assert rec["entry_fill_status"] == "missed"              # NEVER 'filled' past expiry
    assert rec["entry_late_status"] == "after_expiry_blocked"
    assert rec["net_pnl_usdt"] == 0.0 and rec["net_r"] == 0.0


def test_simulate_branch_ordinary_miss_is_not_mislabeled_as_after_expiry_blocked():
    # price never comes anywhere near the zone at all (not even past expiry) -> plain "missed".
    sig = {"signal_id": "sig_test_plain_miss", "symbol": "BTCUSDT", "direction": "long", "mode": "scalp",
          "asset_class": "crypto", "created_at": "2026-06-20T10:00:00+00:00",
          "expires_at": None, "validity_window_hours": 2,
          "entry_low": 98, "entry_high": 99, "entry_trigger": None, "suggested_entry": None,
          "tp1": 104, "tp2": 106, "tp3": 108, "stop0": 97, "economic_trade_key": "k_plain_miss"}
    cs = _bars_at([
        ("2026-06-20 10:15", 105.0, 105.2, 104.8, 105.1),
        ("2026-06-20 11:00", 106.0, 106.3, 105.7, 106.1),
    ])
    rec, events = simulate_branch("old_paper", sig, {}, cs, "bybit_non_vip_usdt_perp")
    assert rec["entry_fill_status"] == "missed"
    assert rec["entry_late_status"] == "missed"               # NOT after_expiry_blocked
