"""SI-7 post-trade classifier — deterministic outcome + failure/success reasoning."""
from __future__ import annotations

import sqlite3

from src.stocks import intraday_post_trade_classifier as pt


def test_loss_market_reversal_primary():
    c = pt.classify_trade({"paper_execution_r": -1.0, "close_reason": "original_stop",
                           "market_context_status": "conflict", "sector_confirmation_status": "confirmed",
                           "liquidity_status": "ok", "catalyst_quality": "strong"})
    assert c["outcome"] == "loss" and c["failure_reason_primary"] == "market_reversal"


def test_loss_data_gap_late_primary():
    c = pt.classify_trade({"paper_execution_r": -1.0, "close_reason": "original_stop",
                           "liquidity_status": "data_gap_late_blocked", "market_context_status": "ok"})
    assert c["failure_reason_primary"] == "data_gap_late"


def test_loss_weak_catalyst_and_late():
    c = pt.classify_trade({"paper_execution_r": -0.8, "close_reason": "original_stop",
                           "market_context_status": "ok", "sector_confirmation_status": "confirmed",
                           "liquidity_status": "ok", "catalyst_quality": "weak", "session_phase": "last_30m"})
    assert c["failure_reason_primary"] == "weak_or_stale_catalyst"
    assert c["failure_reason_secondary"] == "late_entry"


def test_expired_no_followthrough():
    c = pt.classify_trade({"paper_execution_r": 0.0, "close_reason": "expired_flat",
                           "catalyst_quality": "none"})
    assert c["outcome"] == "expired" and c["failure_reason_primary"] == "no_volume_followthrough"


def test_loss_no_gate_context_is_honest():
    # A trade that predates the SI-1..5 gates (no market/sector/session/liquidity/catalyst recorded)
    # must NOT be blamed on a fabricated cause (e.g. weak catalyst) — it is no_gate_context.
    c = pt.classify_trade({"paper_execution_r": -1.0, "close_reason": "original_stop"})
    assert c["outcome"] == "loss" and c["failure_reason_primary"] == "no_gate_context"
    assert c["failure_reason_secondary"] is None


def test_expired_no_gate_context():
    c = pt.classify_trade({"paper_execution_r": 0.0, "close_reason": "expired_flat"})
    assert c["outcome"] == "expired" and c["failure_reason_primary"] == "no_gate_context"


def test_win_catalyst_followthrough():
    c = pt.classify_trade({"paper_execution_r": 2.0, "close_reason": "tp3_runner",
                           "catalyst_quality": "strong"})
    assert c["outcome"] == "win" and c["success_reason_primary"] == "catalyst_followthrough"


def test_refresh_end_to_end(tmp_path):
    db = str(tmp_path / "pt.sqlite")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, asset_class TEXT, mode TEXT, "
              "setup_type TEXT, raw_idea_json TEXT)")
    c.execute("CREATE TABLE paper_execution_outcomes (signal_id TEXT, paper_execution_r REAL, "
              "close_reason TEXT, paper_execution_outcome TEXT, computed_at TEXT)")
    raw = '{"intraday_actionability": {"session_phase": "morning", "market_context_status": "conflict", ' \
          '"sector_confirmation_status": "weak", "liquidity_status": "ok", "catalyst_quality": "none"}}'
    c.execute("INSERT INTO proposed_signals VALUES ('s1','stocks','intraday','pullback', ?)", (raw,))
    c.execute("INSERT INTO paper_execution_outcomes VALUES ('s1', -1.0, 'original_stop', 'loss', '2026-07-08')")
    # a crypto row that must be ignored
    c.execute("INSERT INTO proposed_signals VALUES ('c1','crypto','intraday','x', NULL)")
    c.execute("INSERT INTO paper_execution_outcomes VALUES ('c1', -1.0, 'original_stop', 'loss', '2026-07-08')")
    c.commit(); c.close()
    res = pt.refresh(db=db)
    assert res["updated"] == 1                    # only the stock-intraday row
    c = sqlite3.connect(db)
    row = c.execute("SELECT outcome, market_context_status, failure_reason_primary "
                    "FROM stocks_intraday_post_trade_diagnostics WHERE signal_id='s1'").fetchone()
    c.close()
    assert row == ("loss", "conflict", "market_reversal")


_RAW = '{"intraday_actionability": {"session_phase":"morning","market_context_status":"ok",' \
       '"sector_confirmation_status":"confirmed","liquidity_status":"ok","catalyst_quality":"strong"}}'


def _ledger_db(tmp_path):
    db = str(tmp_path / "pt_usd.sqlite")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, asset_class TEXT, mode TEXT, "
              "setup_type TEXT, raw_idea_json TEXT)")
    c.execute("CREATE TABLE paper_execution_outcomes (signal_id TEXT, paper_execution_r REAL, "
              "close_reason TEXT, paper_execution_outcome TEXT, computed_at TEXT)")
    c.execute("CREATE TABLE paper_portfolio_ledger (signal_id TEXT, event_type TEXT, net_pnl_usdt REAL, "
              "timestamp TEXT, created_at TEXT, fee_profile TEXT)")
    return db, c


def test_refresh_writes_authoritative_usd_pnl_from_active_profile(tmp_path, monkeypatch):
    # net_pnl_usdt must come from the ACTIVE fee profile's terminal exit row; a signal with no
    # active-profile exit leaves net_pnl_usdt NULL (never fabricated / never another profile).
    monkeypatch.setattr(pt, "_active_fee_profile", lambda: "bybit_non_vip_usdt_perp")
    db, c = _ledger_db(tmp_path)
    c.execute("INSERT INTO proposed_signals VALUES ('s1','stocks','intraday','pullback', ?)", (_RAW,))
    c.execute("INSERT INTO paper_execution_outcomes VALUES ('s1', 1.4, 'tp2_hit', 'win', '2026-07-08')")
    # active-profile exits: two rows; the terminal (latest rowid) wins
    c.execute("INSERT INTO paper_portfolio_ledger VALUES ('s1','exit', -5.0, '2026-07-08T14:00:00+00:00', NULL, 'bybit_non_vip_usdt_perp')")
    c.execute("INSERT INTO paper_portfolio_ledger VALUES ('s1','exit', 42.5, '2026-07-08T15:30:00+00:00', NULL, 'bybit_non_vip_usdt_perp')")
    # a non-active profile row for the SAME signal must be ignored even though its PnL differs
    c.execute("INSERT INTO paper_portfolio_ledger VALUES ('s1','exit', 999.0, '2026-07-08T16:00:00+00:00', NULL, 'zero')")
    # s2 has ONLY a non-active-profile exit → net_pnl_usdt stays NULL
    c.execute("INSERT INTO proposed_signals VALUES ('s2','stocks','intraday','pullback', ?)", (_RAW,))
    c.execute("INSERT INTO paper_execution_outcomes VALUES ('s2', -1.0, 'original_stop', 'loss', '2026-07-08')")
    c.execute("INSERT INTO paper_portfolio_ledger VALUES ('s2','exit', -7.0, '2026-07-08T14:00:00+00:00', NULL, 'conservative_taker')")
    c.commit(); c.close()
    res = pt.refresh(db=db)
    assert res["updated"] == 2
    c = sqlite3.connect(db)
    r1 = c.execute("SELECT net_pnl_usdt, notes_json FROM stocks_intraday_post_trade_diagnostics WHERE signal_id='s1'").fetchone()
    r2 = c.execute("SELECT net_pnl_usdt, notes_json FROM stocks_intraday_post_trade_diagnostics WHERE signal_id='s2'").fetchone()
    c.close()
    assert r1[0] == 42.5                                        # active-profile terminal exit, NOT 999.0
    assert "bybit_non_vip_usdt_perp" in r1[1]
    assert r2[0] is None                                        # no active-profile exit → NULL
    assert "unavailable_active_profile_missing" in r2[1]


def test_usd_pnl_is_deterministic_across_fee_profiles(tmp_path, monkeypatch):
    # Same signal_id, SAME timestamp, DIFFERENT fee_profile/PnL — the classifier must deterministically
    # pick the active profile, never a random one.
    monkeypatch.setattr(pt, "_active_fee_profile", lambda: "bybit_non_vip_usdt_perp")
    db, c = _ledger_db(tmp_path)
    c.execute("INSERT INTO proposed_signals VALUES ('s1','stocks','intraday','pullback', ?)", (_RAW,))
    c.execute("INSERT INTO paper_execution_outcomes VALUES ('s1', 1.0, 'tp1_hit', 'win', '2026-07-08')")
    ts = "2026-07-08T15:30:00+00:00"
    for prof, pnl in (("zero", 0.0), ("bybit_non_vip_usdt_perp", 30.0), ("conservative_taker", 12.3),
                      ("mexc_default_futures", 25.0)):
        c.execute("INSERT INTO paper_portfolio_ledger VALUES ('s1','exit', ?, ?, NULL, ?)", (pnl, ts, prof))
    c.commit(); c.close()
    for _ in range(3):                                          # deterministic across repeated runs
        pt.refresh(db=db)
        c = sqlite3.connect(db)
        val = c.execute("SELECT net_pnl_usdt FROM stocks_intraday_post_trade_diagnostics WHERE signal_id='s1'").fetchone()[0]
        c.close()
        assert val == 30.0                                     # always the active profile's PnL


def test_classifier_read_model_only():
    import pathlib
    src = pathlib.Path(pt.__file__).read_text(encoding="utf-8").lower()
    for bad in ("create_order(", "auto_live", "final_r =", "update proposed_signals",
                "insert into proposed_signals", "update signal_outcomes"):
        assert bad not in src, bad
    assert "insert or replace into stocks_intraday_post_trade_diagnostics" in src
